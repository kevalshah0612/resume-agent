"""
New resume flow.

Flow 1:
  PASS 1 -> DES approval / CONFIRM -> final resume JSON

Flow 2:
  recruiter review -> final JSON for DOCX

The Markdown prompt files are loaded as-is from new_flow. The provider layer is
kept intentionally small: NVIDIA first when configured, direct Claude fallback
when enabled.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import anthropic


ROOT = Path(__file__).parent
PROMPT_DIR = ROOT / "new_flow"
RUNS_DIR = ROOT / "runs"
CFG_FILE = ROOT / "pipeline_config.json"
ENV_FILE = ROOT / ".env"

DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_NVIDIA_MODEL = "nvidia/nemotron-3-super-120b-a12b"

_log_cb = None

PASS1_COMPACT_INSTRUCTION = """
PASS 1 OUTPUT OVERRIDE FOR THIS APP:
Return a short DES candidate bank only. Do not print the long PASS 1 audit.

Output exactly these sections:

COVERAGE SUMMARY:
- Coverage confidence: HIGH | MEDIUM | LOW, NN%
- Covered keywords: comma-separated exact JD terms with story evidence
- Partial keywords: comma-separated exact JD terms with partial/adjacent evidence
- Needs DES: comma-separated exact JD terms that need user approval
- Apply risk: LOW | MEDIUM | HIGH

DES CANDIDATE BANK:
One line per DES only. Use this exact compact format:
DES 1 | keyword: <exact JD keyword> | use when: <why it matters> | bullet: <Experience/Project + slot suggestion> | story/context: <evidence block or user-confirmable context> | number: <metric/scope or none> | safe wording: <one bullet-ready sentence>

Rules:
- Generate only high-value DES candidates, usually 3 to 8.
- Each DES must fit on one line.
- Do not output tables.
- Do not output final JSON.
- End with: APPROVAL: Reply Approved: DES 1 to 3, or Approved: 1,2,3, or Confirm with no DES.
"""

PASS2_COMPACT_INSTRUCTION = """
Generate the final resume JSON now using the approved DES IDs below.
Output only:
1. a short confidence summary under 8 lines
2. LinkedIn message and recruiter/HM search strings when requested by the main prompt
3. one JSON code block
Do not print long audits or extra tables.
Style rule for LinkedIn/message text: use ASCII punctuation only. Do not use em dashes or en dashes. Use commas, periods, semicolons, or simple hyphens instead.
"""

HUMAN_TEXT_STYLE_RULE = """
Output style rule:
- Use ASCII punctuation only in LinkedIn messages, recruiter outreach, cover letters, and application answers.
- Do not use em dashes or en dashes.
- Use commas, periods, semicolons, parentheses, or simple hyphens instead.
"""


def set_log_callback(cb):
    global _log_cb
    _log_cb = cb


def log(msg: str):
    print(msg)
    if _log_cb:
        _log_cb(msg)


@dataclass
class ResumeInput:
    company: str
    jd: str
    title: str = "Software Engineer"
    words: str = ""
    mode: str = ""
    des: str = ""


@dataclass
class CostEvent:
    label: str
    model: str
    input_tokens: int
    output_tokens: int
    cache_creation_input_tokens: int
    cache_read_input_tokens: int
    estimated_cost_usd: float


MODEL_PRICING_PER_MTOK = {
    "claude-sonnet-4-6": {"input": 3.0, "cache_write": 3.75, "cache_read": 0.30, "output": 15.0},
    "claude-sonnet-4-5": {"input": 3.0, "cache_write": 3.75, "cache_read": 0.30, "output": 15.0},
    "claude-haiku-4-5": {"input": 1.0, "cache_write": 1.25, "cache_read": 0.10, "output": 5.0},
    "nvidia/nemotron-3-super-120b-a12b": {"input": 0.0, "cache_write": 0.0, "cache_read": 0.0, "output": 0.0},
}


def load_env_file() -> dict[str, str]:
    values: dict[str, str] = {}
    if not ENV_FILE.exists():
        return values
    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        values[key] = value
        os.environ[key] = value
    return values


def load_config() -> dict[str, Any]:
    env_values = load_env_file()
    if CFG_FILE.exists():
        cfg = json.loads(CFG_FILE.read_text(encoding="utf-8"))
    else:
        cfg = {}
    env_to_cfg = {
        "PROVIDER_MODE": "provider_mode",
        "RESUME_AGENT_PROVIDER": "provider",
        "NVIDIA_API_KEY": "nvidia_api_key",
        "NVIDIA_MODEL": "model_nvidia",
        "NVIDIA_BASE_URL": "nvidia_base_url",
        "ANTHROPIC_API_KEY": "anthropic_api_key",
    }
    for env_key, cfg_key in env_to_cfg.items():
        if env_values.get(env_key):
            cfg[cfg_key] = env_values[env_key]
    return cfg


def get_client() -> anthropic.AsyncAnthropic:
    cfg = load_config()
    key = os.environ.get("ANTHROPIC_API_KEY") or cfg.get("anthropic_api_key", "")
    if not key:
        raise RuntimeError(
            "No Anthropic API key found. Set ANTHROPIC_API_KEY or add it to pipeline_config.json."
        )
    return anthropic.AsyncAnthropic(api_key=key)


def get_provider() -> str:
    cfg = load_config()
    mode = str(cfg.get("provider_mode", "") or os.environ.get("PROVIDER_MODE", "")).strip().lower()
    mode_map = {
        "1": "nvidia",
        "nvidia": "nvidia",
        "nemotron": "nvidia",
        "2": "anthropic",
        "claude": "anthropic",
        "anthropic": "anthropic",
    }
    if mode in mode_map:
        return mode_map[mode]
    provider = str(cfg.get("provider", "") or os.environ.get("RESUME_AGENT_PROVIDER", "")).lower().strip()
    if provider in {"anthropic", "nvidia"}:
        return provider
    if cfg.get("model_nvidia") or os.environ.get("NVIDIA_API_KEY"):
        return "nvidia"
    return "anthropic"


def get_model() -> str:
    cfg = load_config()
    return cfg.get("model_resume") or cfg.get("model_sonnet") or DEFAULT_MODEL


def get_nvidia_model() -> str:
    cfg = load_config()
    return cfg.get("model_nvidia") or os.environ.get("NVIDIA_MODEL") or DEFAULT_NVIDIA_MODEL


def get_nvidia_client():
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("openai is required for NVIDIA provider. Run: pip install openai") from exc

    cfg = load_config()
    key = cfg.get("nvidia_api_key", "") or os.environ.get("NVIDIA_API_KEY", "")
    if not key:
        raise RuntimeError("NVIDIA provider selected but NVIDIA_API_KEY is missing.")
    base_url = cfg.get("nvidia_base_url") or os.environ.get("NVIDIA_BASE_URL") or "https://integrate.api.nvidia.com/v1"
    return OpenAI(base_url=base_url, api_key=key)


def estimate_cost_usd(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_creation_input_tokens: int = 0,
    cache_read_input_tokens: int = 0,
) -> float:
    if model in MODEL_PRICING_PER_MTOK:
        rates = MODEL_PRICING_PER_MTOK[model]
    elif model.startswith("nvidia/"):
        rates = MODEL_PRICING_PER_MTOK[DEFAULT_NVIDIA_MODEL]
    else:
        rates = MODEL_PRICING_PER_MTOK["claude-sonnet-4-6"]
    return (
        input_tokens * rates["input"]
        + cache_creation_input_tokens * rates["cache_write"]
        + cache_read_input_tokens * rates["cache_read"]
        + output_tokens * rates["output"]
    ) / 1_000_000


def system_text(system_blocks: list[dict[str, Any]]) -> str:
    return "\n\n".join(str(block.get("text", "")) for block in system_blocks if str(block.get("text", "")).strip())


def openai_messages(system_blocks: list[dict[str, Any]], messages: list[dict[str, str]]) -> list[dict[str, str]]:
    system = system_text(system_blocks)
    result: list[dict[str, str]] = []
    if system:
        result.append({"role": "system", "content": system})
    result.extend(messages)
    return result


def call_nvidia_sync(
    *,
    system_blocks: list[dict[str, Any]],
    messages: list[dict[str, str]],
    model: str,
    max_tokens: int,
) -> tuple[str, dict[str, int]]:
    client = get_nvidia_client()
    stream = client.chat.completions.create(
        model=model,
        messages=openai_messages(system_blocks, messages),
        temperature=1,
        top_p=0.95,
        max_tokens=max_tokens,
        extra_body={
            "chat_template_kwargs": {"enable_thinking": True},
            "reasoning_budget": min(max_tokens, 16384),
        },
        stream=True,
    )
    parts: list[str] = []
    for chunk in stream:
        if not chunk.choices:
            continue
        content = getattr(chunk.choices[0].delta, "content", None)
        if content is not None:
            parts.append(content)
    return "".join(parts).strip(), {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }


def read_prompt(name: str) -> str:
    path = PROMPT_DIR / name
    if not path.exists():
        matches = [candidate for candidate in PROMPT_DIR.iterdir() if candidate.name.lower() == name.lower()]
        if not matches:
            raise FileNotFoundError(f"Missing prompt file: {path}")
        path = matches[0]
    return path.read_text(encoding="utf-8")


def cached_text_block(text: str) -> dict[str, Any]:
    return {
        "type": "text",
        "text": text,
        "cache_control": {"type": "ephemeral"},
    }


def input_to_text(inp: ResumeInput) -> str:
    return "\n".join(
        [
            f"Company: {inp.company}",
            f"Title: {inp.title or 'Software Engineer'}",
            "JD:",
            inp.jd.strip(),
            "",
            f"Words: {inp.words}",
            f"Mode: {inp.mode}",
            f"Des: {inp.des}",
        ]
    )


def normalize_approval(text: str) -> str:
    raw = text.strip()
    if not raw:
        return "CONFIRM"
    lowered = raw.lower()
    numbers: list[int] = []

    for start, end in re.findall(r"(?:des\s*)?(\d+)\s*(?:to|-)\s*(?:des\s*)?(\d+)", lowered):
        a, b = int(start), int(end)
        lo, hi = sorted((a, b))
        numbers.extend(range(lo, hi + 1))

    cleaned = re.sub(r"(?:des\s*)?\d+\s*(?:to|-)\s*(?:des\s*)?\d+", " ", lowered)
    for n in re.findall(r"(?:des\s*)?(\d+)", cleaned):
        numbers.append(int(n))

    unique = sorted(set(numbers))
    if not unique and "confirm" in lowered:
        return "CONFIRM"
    if not unique:
        return raw if "CONFIRM" in raw.upper() else f"{raw}\nCONFIRM"
    approved = ", ".join(f"DES-{n}" for n in unique)
    return f"Apply {approved}\nCONFIRM"


async def call_model(
    *,
    system_blocks: list[dict[str, Any]],
    messages: list[dict[str, str]],
    label: str,
    max_tokens: int = 8192,
    cost_cb=None,
) -> str:
    provider = get_provider()
    if provider == "nvidia":
        model = get_nvidia_model()
    else:
        model = get_model()
    t0 = time.monotonic()

    try:
        if provider == "nvidia":
            text, usage_data = await asyncio.to_thread(
                call_nvidia_sync,
                system_blocks=system_blocks,
                messages=messages,
                model=model,
                max_tokens=max_tokens,
            )
            input_tokens = usage_data["input_tokens"]
            output_tokens = usage_data["output_tokens"]
            cache_create = usage_data["cache_creation_input_tokens"]
            cache_read = usage_data["cache_read_input_tokens"]
        else:
            client = get_client()
            resp = await client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_blocks,
                messages=messages,
            )
            text = resp.content[0].text.strip()
            usage = resp.usage
            input_tokens = usage.input_tokens
            output_tokens = usage.output_tokens
            cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
            cache_create = getattr(usage, "cache_creation_input_tokens", 0) or 0
    except Exception:
        cfg = load_config()
        fallback_enabled = bool(cfg.get("fallback_to_anthropic", True))
        if provider == "nvidia" and fallback_enabled:
            log(f"{label}: {provider} failed; falling back to direct Anthropic.")
            client = get_client()
            model = get_model()
            provider = "anthropic"
            resp = await client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_blocks,
                messages=messages,
            )
            text = resp.content[0].text.strip()
            usage = resp.usage
            input_tokens = usage.input_tokens
            output_tokens = usage.output_tokens
            cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
            cache_create = getattr(usage, "cache_creation_input_tokens", 0) or 0
        else:
            raise

    estimated_cost = estimate_cost_usd(
        model,
        input_tokens,
        output_tokens,
        cache_create,
        cache_read,
    )
    elapsed = time.monotonic() - t0
    log(
        f"{label}: provider={provider} model={model} in={input_tokens} out={output_tokens} "
        f"cache_read={cache_read} cache_create={cache_create} "
        f"cost=${estimated_cost:.4f} elapsed={elapsed:.1f}s"
    )
    if cost_cb:
        cost_cb(CostEvent(
            label=label,
            model=f"{provider}:{model}",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_creation_input_tokens=cache_create,
            cache_read_input_tokens=cache_read,
            estimated_cost_usd=estimated_cost,
        ))
    return text


def flow1_system() -> list[dict[str, Any]]:
    return [
        cached_text_block(read_prompt("prompt.md")),
        cached_text_block(read_prompt("story.md")),
    ]


def recruiter_system() -> list[dict[str, Any]]:
    return [cached_text_block(read_prompt("recruiter.md"))]


def labeled_step(request_label: str, step: str) -> str:
    return f"{request_label} | {step}" if request_label else step


async def run_pass1(inp: ResumeInput, cost_cb=None, request_label: str = "") -> str:
    user_message = "\n\n".join([
        read_prompt("prompt_short.md"),
        PASS1_COMPACT_INSTRUCTION,
        input_to_text(inp),
    ])
    return await call_model(
        system_blocks=flow1_system(),
        messages=[{"role": "user", "content": user_message}],
        label=labeled_step(request_label, "PASS 1"),
        max_tokens=3500,
        cost_cb=cost_cb,
    )


async def run_pass2(
    inp: ResumeInput,
    pass1_text: str,
    approval_text: str,
    cost_cb=None,
    request_label: str = "",
) -> str:
    first_user = "\n\n".join([
        read_prompt("prompt_short.md"),
        PASS1_COMPACT_INSTRUCTION,
        input_to_text(inp),
    ])
    normalized_approval = normalize_approval(approval_text)
    return await call_model(
        system_blocks=flow1_system(),
        messages=[
            {"role": "user", "content": first_user},
            {"role": "assistant", "content": pass1_text},
            {"role": "user", "content": PASS2_COMPACT_INSTRUCTION + "\n\n" + normalized_approval},
        ],
        label=labeled_step(request_label, "PASS 2"),
        max_tokens=12000,
        cost_cb=cost_cb,
    )


async def run_recruiter_review(
    *,
    jd: str,
    resume1_json: dict[str, Any],
    des: str = "",
    resume2_json: dict[str, Any] | None = None,
    cost_cb=None,
    request_label: str = "",
) -> str:
    parts = [
        read_prompt("recruiter_short.md"),
        HUMAN_TEXT_STYLE_RULE.strip(),
        "",
        "JD:",
        jd.strip(),
        "",
    ]
    if des.strip():
        parts += ["Des:", des.strip(), ""]
    parts += ["Resume 1:", json.dumps(resume1_json, indent=2)]
    if resume2_json:
        parts += ["", "Resume 2:", json.dumps(resume2_json, indent=2)]
    return await call_model(
        system_blocks=recruiter_system(),
        messages=[{"role": "user", "content": "\n".join(parts)}],
        label=labeled_step(request_label, "RECRUITER REVIEW"),
        max_tokens=12000,
        cost_cb=cost_cb,
    )


async def run_application_answers(
    *,
    company: str,
    title: str,
    jd: str,
    questions: str,
    resume_json: dict[str, Any],
    cost_cb=None,
    request_label: str = "",
) -> str:
    system_blocks = [cached_text_block(read_prompt("questions.md"))]
    user_message = "\n".join([
        HUMAN_TEXT_STYLE_RULE.strip(),
        "",
        "Candidate Resume JSON:",
        json.dumps(resume_json, indent=2),
        "",
        "Job Description:",
        jd.strip(),
        "",
        f"Company: {company}",
        f"Title: {title}",
        "",
        "Application Questions:",
        questions.strip(),
        "",
        "Cover Letter:",
        "Only if explicitly requested in Application Questions.",
        "",
        "Candidate Profile / Fixed Answers:",
        "Use only details explicitly included in Application Questions or resume JSON. If missing, output NEED USER INPUT.",
    ])
    return await call_model(
        system_blocks=system_blocks,
        messages=[{"role": "user", "content": user_message}],
        label=labeled_step(request_label, "APPLICATION QA"),
        max_tokens=3500,
        cost_cb=cost_cb,
    )


def extract_json(text: str) -> dict[str, Any]:
    blocks = re.findall(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    candidates = blocks or re.findall(r"(\{.*\})", text, flags=re.DOTALL)
    last_error: Exception | None = None
    for candidate in reversed(candidates):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as exc:
            last_error = exc
    raise ValueError(f"Could not extract valid JSON from model output: {last_error}")


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return cleaned or "Resume"


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M")


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def build_docx(json_path: Path, out_docx: str) -> Path:
    manager_py = ROOT / "manager.py"
    cmd = [sys.executable, str(manager_py), str(json_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"manager.py failed:\n{result.stderr or result.stdout}")
    log(result.stdout.strip())
    for line in result.stdout.splitlines():
        if line.startswith("DOCX saved"):
            return ROOT / line.split(":", 1)[1].strip()
    return ROOT / out_docx


def write_run_artifacts(
    *,
    run_dir: Path,
    pass1_text: str | None = None,
    pass2_text: str | None = None,
    resume_json: dict[str, Any] | None = None,
    recruiter_text: str | None = None,
    recruiter_json: dict[str, Any] | None = None,
) -> None:
    if pass1_text is not None:
        save_text(run_dir / "01_pass1.txt", pass1_text)
    if pass2_text is not None:
        save_text(run_dir / "02_pass2_raw.txt", pass2_text)
    if resume_json is not None:
        save_json(run_dir / "03_resume_json.json", resume_json)
    if recruiter_text is not None:
        save_text(run_dir / "04_recruiter_raw.txt", recruiter_text)
    if recruiter_json is not None:
        save_json(run_dir / "05_recruiter_final_json.json", recruiter_json)
