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
import copy
import json
import os
import re
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import anthropic

from app_properties import PROMPT_PROFILE_LABELS
from manager import build_render_profile


ROOT = Path(__file__).parent
PROMPT_DIR = ROOT / "new_flow"
PROMPT_V1_DIR = ROOT / "Prompt_V1"
FINAL_QA_PROMPT_DIR = ROOT / "claude_resume_workflow"
RUNS_DIR = ROOT / "runs"
CFG_FILE = ROOT / "pipeline_config.json"
ENV_FILE = ROOT / ".env"

DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_NVIDIA_MODEL = "nvidia/nemotron-3-ultra-550b-a55b"
DEFAULT_NVIDIA_MAX_ATTEMPTS = 5
DEFAULT_NVIDIA_REASONING_BUDGET = 16384

_log_cb = None

PROMPT_PROFILES = dict(PROMPT_PROFILE_LABELS)

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
Perform all audits silently. Output only these sections in this order:
1. CONFIDENCE SUMMARY: maximum 5 short lines
2. RECRUITER LINKEDIN MESSAGE: exactly one recruiter cold outreach, maximum 300 characters including spaces
3. HIRING MANAGER LINKEDIN MESSAGE: exactly one hiring-manager cold outreach, maximum 300 characters including spaces
4. RECRUITER/HM SEARCH STRINGS: exactly 4 search strings
5. FINAL JSON: exactly one complete valid JSON code block
Do not print audit tables, coverage tables, diagnostics, scratch work, or a follow-up message.
Do not add anything after the JSON block.
Both messages must name the exact target title and company, use one evidence-supported proof point, and use ASCII punctuation only.
Recruiter message: politely ask for the correct recruiter or for the resume to be passed along if the recipient is not responsible for the role.
Hiring-manager message: connect the proof point to a real JD priority and ask one low-friction question about the team or role.
Do not use em dashes or en dashes. Do not use "would love to connect," generic praise, desperation, or a list of technologies.
"""

RECRUITER_COMPACT_INSTRUCTION = """
RECRUITER OUTPUT OVERRIDE FOR THIS APP:
Perform every recruiter, ATS, evidence, bullet, skills, schema, and quality check silently.
Output only:
1. RECRUITER SUMMARY: maximum 8 short lines covering picked resume, major fixes, remaining risks, and confidence
2. RECRUITER LINKEDIN MESSAGE: one role-specific message, maximum 300 characters
3. HIRING MANAGER LINKEDIN MESSAGE: one role-specific message, maximum 300 characters
4. RECRUITER/HM SEARCH STRINGS: exactly 4 search strings
5. FINAL JSON: exactly one complete valid JSON code block
Both messages must name TARGET TITLE and TARGET COMPANY and use only a proof point supported by the selected final JSON.
Recruiter message may politely ask for the correct recruiter or for the resume to be passed along.
Hiring-manager message must connect one proof point to a JD priority and ask one concise team- or role-specific question.
Use ASCII punctuation. Avoid generic `would love to connect` language, flattery, desperation, and technology lists.
Do not output audit tables, OLD -> NEW tables, coverage matrices, quality-gate tables, or long explanations.
Do not add anything after the JSON block.
"""

FINAL_QA_CONTRACT = """
You are the final evidence-safe resume quality gate for this application.

SOURCE OF TRUTH AND EDITING RULES:
- The supplied source resume JSON is the only editable resume source.
- The job description is a targeting reference, never evidence that the candidate has a skill.
- The render profile is authoritative for section order, level, layout, experience order, project order, TA placement, and visible counts.
- Never invent or infer a metric, technology, framework, domain, user count, business result, title, employer, date, project, degree, location, leadership claim, or responsibility.
- Never emit placeholders such as [FILL IN], TBD, TODO, optional, or invented estimates.
- Preserve the exact JSON schema, key set, value types, list lengths, config object, identity/contact fields, role identities, role array order, project identities/order, education identities/order, employment_note values, and bullet counts.
- Preserve employment_note exactly. Do not create, remove, or rewrite it.
- Do not move evidence between roles or projects.
- You may improve summary text, reorder supported skill terms within existing fields, and rewrite existing bullets using only facts already visible in the source JSON.
- Keep rewritten bullets concise and no longer than needed. Do not expand content in a way likely to change the one-page layout.
- Use ASCII punctuation. Do not use em dashes or en dashes.
- Return complete output. If JSON is requested, close every object and array and output exactly one complete JSON code block.
"""

FINAL_QA_REPAIR_OUTPUT = """
Apply only the audit fixes that are supported by the source JSON and compatible with the locked render profile.
Preserve employment_note exactly. Do not create, remove, or rewrite it.
Output only:
1. REPAIR SUMMARY: maximum 8 short lines
2. FINAL JSON: exactly one complete valid JSON code block
Do not output tables, placeholders, alternatives, or text after the JSON block.
"""

FINAL_QA_SCAN_OUTPUT = """
Independently scan the repaired JSON against the JD, original audit, source JSON, and locked render profile.
Fix only remaining evidence-supported problems. Preserve every locked structural and identity rule.
Preserve employment_note exactly. Do not create, remove, or rewrite it.
Output only:
1. FINAL QA SUMMARY: maximum 8 short lines including ATS verdict, hiring-manager pile, remaining risk, and confidence
2. FINAL JSON: exactly one complete valid JSON code block
Do not output tables, alternatives, or text after the JSON block.
"""

HUMAN_TEXT_STYLE_RULE = """
Output style rule:
- Use ASCII punctuation only in LinkedIn messages, recruiter outreach, cover letters, and application answers.
- Do not use em dashes or en dashes.
- Use commas, periods, semicolons, parentheses, or simple hyphens instead.
"""

NVIDIA_RETRY_INSTRUCTION = """
RETRY OUTPUT OVERRIDE:
The previous attempt was rejected because it was incomplete or failed an output rule.
Regenerate the full answer from scratch. Keep all analysis internal and keep visible text minimal.
If JSON is required, output one complete valid JSON code block and finish every array/object.
Do not emit audit tables. Do not repeat the prior response. Do not add text after the JSON block.
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
    attempts: int = 1
    finish_reason: str = ""


@dataclass
class NvidiaResponse:
    text: str
    usage: dict[str, int]
    finish_reason: str


@dataclass(frozen=True)
class NvidiaModelSpec:
    display_name: str
    model_id: str
    thinking_key: str
    stream: bool


NVIDIA_MODEL_SPECS = (
    NvidiaModelSpec(
        display_name="Nemotron 3 Ultra",
        model_id="nvidia/nemotron-3-ultra-550b-a55b",
        thinking_key="enable_thinking",
        stream=True,
    ),
    NvidiaModelSpec(
        display_name="DeepSeek V4 Pro",
        model_id="deepseek-ai/deepseek-v4-pro",
        thinking_key="thinking",
        stream=False,
    ),
)


@dataclass
class FinalReviewResult:
    audit_raw: str
    repair_raw: str
    repaired_json: dict[str, Any]
    final_scan_raw: str
    final_json: dict[str, Any]
    render_profile: dict[str, Any]
    restored_locks: list[str]


class OperationCancelled(RuntimeError):
    pass


def raise_if_cancelled(cancel_event: threading.Event | None) -> None:
    if cancel_event and cancel_event.is_set():
        raise OperationCancelled("Operation stopped by user.")


async def wait_before_retry(seconds: int, cancel_event: threading.Event | None) -> None:
    for _ in range(seconds * 10):
        raise_if_cancelled(cancel_event)
        await asyncio.sleep(0.1)


MODEL_PRICING_PER_MTOK = {
    "claude-sonnet-4-6": {"input": 3.0, "cache_write": 3.75, "cache_read": 0.30, "output": 15.0},
    "claude-sonnet-4-5": {"input": 3.0, "cache_write": 3.75, "cache_read": 0.30, "output": 15.0},
    "claude-haiku-4-5": {"input": 1.0, "cache_write": 1.25, "cache_read": 0.10, "output": 5.0},
    "nvidia/nemotron-3-ultra-550b-a55b": {"input": 0.0, "cache_write": 0.0, "cache_read": 0.0, "output": 0.0},
    "deepseek-ai/deepseek-v4-pro": {"input": 0.0, "cache_write": 0.0, "cache_read": 0.0, "output": 0.0},
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
        "NVIDIA_THINKING": "nvidia_thinking",
        "NVIDIA_BASE_URL": "nvidia_base_url",
        "NVIDIA_MAX_ATTEMPTS": "nvidia_max_attempts",
        "NVIDIA_REASONING_BUDGET": "nvidia_reasoning_budget",
        "FALLBACK_TO_ANTHROPIC": "fallback_to_anthropic",
        "ANTHROPIC_API_KEY": "anthropic_api_key",
    }
    for env_key, cfg_key in env_to_cfg.items():
        if env_values.get(env_key):
            cfg[cfg_key] = env_values[env_key]
    return cfg


def config_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def config_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(parsed, maximum))


def get_nvidia_max_attempts() -> int:
    cfg = load_config()
    return config_int(cfg.get("nvidia_max_attempts"), DEFAULT_NVIDIA_MAX_ATTEMPTS, 1, 10)


def get_nvidia_reasoning_budget() -> int:
    cfg = load_config()
    configured = config_int(
        cfg.get("nvidia_reasoning_budget"),
        DEFAULT_NVIDIA_REASONING_BUDGET,
        0,
        16384,
    )
    return configured


def get_nvidia_thinking() -> bool:
    return config_bool(load_config().get("nvidia_thinking"), True)


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


def get_nvidia_model_spec(model: str) -> NvidiaModelSpec:
    spec = next((item for item in NVIDIA_MODEL_SPECS if item.model_id == model), None)
    if not spec:
        allowed = ", ".join(item.model_id for item in NVIDIA_MODEL_SPECS)
        raise ValueError(f"Unsupported NVIDIA model: {model}. Allowed models: {allowed}")
    return spec


def nvidia_model_option_label(model: str, thinking: bool) -> str:
    spec = get_nvidia_model_spec(model)
    return f"{spec.display_name} | Thinking {'ON' if thinking else 'OFF'}"


def nvidia_model_options() -> list[str]:
    return [
        nvidia_model_option_label(spec.model_id, thinking)
        for spec in NVIDIA_MODEL_SPECS
        for thinking in (True, False)
    ]


def resolve_nvidia_model_option(label: str) -> tuple[str, bool]:
    for spec in NVIDIA_MODEL_SPECS:
        for thinking in (True, False):
            if label == nvidia_model_option_label(spec.model_id, thinking):
                return spec.model_id, thinking
    return get_nvidia_model(), get_nvidia_thinking()


def get_default_nvidia_model_option() -> str:
    model = get_nvidia_model()
    if not any(spec.model_id == model for spec in NVIDIA_MODEL_SPECS):
        model = DEFAULT_NVIDIA_MODEL
    return nvidia_model_option_label(model, get_nvidia_thinking())


def normalize_prompt_profile(value: str | None) -> str:
    raw = (value or "").strip().lower()
    if raw in {"v1", "prompt_v1", "experimental", "v1 experimental"}:
        return "v1"
    return "stable"


def prompt_profile_label(profile: str) -> str:
    return PROMPT_PROFILES[normalize_prompt_profile(profile)]


def prompt_profile_options() -> list[str]:
    return list(PROMPT_PROFILES.values())


def resolve_prompt_profile_label(label: str) -> str:
    for key, value in PROMPT_PROFILES.items():
        if label == value:
            return key
    return normalize_prompt_profile(label)


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
    thinking: bool,
    max_tokens: int,
    cancel_event: threading.Event | None = None,
) -> NvidiaResponse:
    raise_if_cancelled(cancel_event)
    client = get_nvidia_client()
    spec = get_nvidia_model_spec(model)
    extra_body: dict[str, Any] = {
        "chat_template_kwargs": {spec.thinking_key: thinking},
    }
    if thinking and spec.model_id == "nvidia/nemotron-3-ultra-550b-a55b":
        extra_body["reasoning_budget"] = get_nvidia_reasoning_budget()
    completion = client.chat.completions.create(
        model=model,
        messages=openai_messages(system_blocks, messages),
        temperature=1,
        top_p=0.95,
        max_tokens=max_tokens,
        extra_body=extra_body,
        stream=spec.stream,
    )
    usage_data = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }

    if not spec.stream:
        raise_if_cancelled(cancel_event)
        usage = getattr(completion, "usage", None)
        if usage is not None:
            usage_data["input_tokens"] = int(getattr(usage, "prompt_tokens", 0) or 0)
            usage_data["output_tokens"] = int(getattr(usage, "completion_tokens", 0) or 0)
        choice = completion.choices[0]
        return NvidiaResponse(
            text=(getattr(choice.message, "content", None) or "").strip(),
            usage=usage_data,
            finish_reason=str(getattr(choice, "finish_reason", "") or ""),
        )

    parts: list[str] = []
    finish_reason = ""
    for chunk in completion:
        if cancel_event and cancel_event.is_set():
            close_stream = getattr(completion, "close", None)
            if callable(close_stream):
                try:
                    close_stream()
                except Exception:
                    pass
            raise OperationCancelled("Operation stopped by user.")
        usage = getattr(chunk, "usage", None)
        if usage is not None:
            usage_data["input_tokens"] = int(getattr(usage, "prompt_tokens", 0) or 0)
            usage_data["output_tokens"] = int(getattr(usage, "completion_tokens", 0) or 0)
        if not chunk.choices:
            continue
        choice = chunk.choices[0]
        chunk_finish_reason = getattr(choice, "finish_reason", None)
        if chunk_finish_reason:
            finish_reason = str(chunk_finish_reason)
        content = getattr(choice.delta, "content", None)
        if content is not None:
            parts.append(content)
    return NvidiaResponse(
        text="".join(parts).strip(),
        usage=usage_data,
        finish_reason=finish_reason,
    )


def prompt_dir_for_profile(prompt_profile: str | None = None) -> Path:
    return PROMPT_V1_DIR if normalize_prompt_profile(prompt_profile) == "v1" else PROMPT_DIR


def read_prompt(name: str, prompt_profile: str | None = None) -> str:
    prompt_dir = prompt_dir_for_profile(prompt_profile)
    path = prompt_dir / name
    if not path.exists():
        matches = [candidate for candidate in prompt_dir.iterdir() if candidate.name.lower() == name.lower()]
        if not matches:
            raise FileNotFoundError(f"Missing prompt file: {path}")
        path = matches[0]
    return path.read_text(encoding="utf-8")


def read_final_qa_prompt(name: str) -> str:
    path = FINAL_QA_PROMPT_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing Final QA workflow prompt: {path}")
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


def linkedin_message_span(text: str, audience: str = "") -> tuple[int, int] | None:
    audience_prefix = ""
    if audience == "recruiter":
        audience_prefix = r"recruiter[ \t]+"
    elif audience in {"hiring_manager", "hm"}:
        audience_prefix = r"(?:hiring[ \t]+manager|hm)[ \t]+"
    heading = re.search(
        r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?(?:\*\*)?" + audience_prefix
        + r"linkedin(?: connection)? message"
        r"(?: under 300 characters)?(?:\*\*)?[ \t]*:?[ \t]*\r?$",
        text,
    )
    if not heading and not audience:
        heading = re.search(
            r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?(?:\*\*)?linkedin(?: connection)? message"
            r"(?: under 300 characters)?(?:\*\*)?[ \t]*:?[ \t]*\r?$",
            text,
        )
    if not heading:
        return None
    content_start = heading.end()
    if content_start < len(text) and text[content_start] == "\r":
        content_start += 1
    if content_start < len(text) and text[content_start] == "\n":
        content_start += 1
    remainder = text[content_start:]
    next_section = re.search(
        r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?(?:\*\*)?"
        r"(?:(?:recruiter|hiring manager|hm)[ \t]+linkedin(?: connection)? message|"
        r"recruiter(?:/hm)? search strings?|hiring manager search strings?|search strings?|"
        r"follow-?up message|final json|```json)",
        remainder,
    )
    content_end = content_start + (next_section.start() if next_section else len(remainder))
    while content_start < content_end and text[content_start].isspace():
        content_start += 1
    while content_end > content_start and text[content_end - 1].isspace():
        content_end -= 1
    return (content_start, content_end) if content_start < content_end else None


def extract_linkedin_message(text: str, audience: str = "") -> str:
    span = linkedin_message_span(text, audience)
    if not span:
        return ""
    message = re.sub(r"\s+", " ", text[span[0]:span[1]]).strip()
    return message.strip("* ")


def shorten_linkedin_message(message: str, limit: int = 300) -> str:
    message = re.sub(r"\s+", " ", message).strip()
    if len(message) <= limit:
        return message
    sentence_candidates = [
        match.end()
        for match in re.finditer(r"[.!?](?=\s|$)", message[: limit + 1])
    ]
    if sentence_candidates:
        shortened = message[: sentence_candidates[-1]].strip()
        if len(shortened) >= 120:
            return shortened
    cutoff = max(1, limit - 1)
    shortened = message[:cutoff].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return (shortened or message[:cutoff]).rstrip(".!?") + "."


def enforce_linkedin_message_limit(text: str, limit: int = 300) -> str:
    spans: list[tuple[int, int]] = []
    for audience in ("recruiter", "hiring_manager"):
        span = linkedin_message_span(text, audience)
        if span and span not in spans:
            spans.append(span)
    if not spans:
        legacy_span = linkedin_message_span(text)
        if legacy_span:
            spans.append(legacy_span)
    for start, end in sorted(spans, reverse=True):
        message = re.sub(r"\s+", " ", text[start:end]).strip().strip("* ")
        text = text[:start] + shorten_linkedin_message(message, limit) + text[end:]
    return text


def validate_json_response(text: str) -> str | None:
    try:
        extract_json(text)
    except Exception as exc:
        return f"invalid or incomplete JSON: {exc}"
    return None


def validate_v1_resume_response(text: str) -> str | None:
    json_error = validate_json_response(text)
    if json_error:
        return json_error
    data = extract_json(text)
    technical_skills = data.get("technical_skills")
    if not isinstance(technical_skills, dict):
        return "technical_skills must be a flat object with dynamic skill-category titles"
    for key, value in technical_skills.items():
        if re.fullmatch(r"row\d+(?:_(?:label|terms))?", str(key).strip(), flags=re.IGNORECASE):
            return "technical_skills must use dynamic category titles, not row1/row2 keys"
        if isinstance(value, (list, dict)):
            return "technical_skills values must be comma-separated strings, not arrays or objects"
        if not str(key).strip() or not str(value).strip():
            return "technical_skills keys and values must be non-empty"
    return None


def validate_nonempty_response(text: str) -> str | None:
    return None if text.strip() else "missing required response"


def validate_pass1_response(text: str) -> str | None:
    if not re.search(r"(?im)^\s*DES CANDIDATE BANK\s*:?\s*$", text):
        return "missing DES CANDIDATE BANK heading"
    if not re.search(r"(?im)^\s*DES\s*-?\s*\d+\s*\|", text):
        return "missing parseable DES candidate lines"
    return None


def validate_resume_response(text: str) -> str | None:
    json_error = validate_json_response(text)
    if json_error:
        return json_error
    messages = {
        "Recruiter LinkedIn message": extract_linkedin_message(text, "recruiter"),
        "Hiring manager LinkedIn message": extract_linkedin_message(text, "hiring_manager"),
    }
    for label, message in messages.items():
        if not message:
            return f"missing {label}"
        if len(message) > 300:
            return f"{label} is {len(message)} characters; maximum is 300"
        if "\u2014" in message or "\u2013" in message:
            return f"{label} contains an em dash or en dash"
    return None


def validate_same_json_shape(reference: Any, candidate: Any, path: str = "$") -> None:
    if type(reference) is not type(candidate):
        raise ValueError(
            f"Final QA changed the JSON type at {path}: "
            f"{type(reference).__name__} -> {type(candidate).__name__}"
        )
    if isinstance(reference, dict):
        if set(reference) != set(candidate):
            missing = sorted(set(reference) - set(candidate))
            added = sorted(set(candidate) - set(reference))
            raise ValueError(f"Final QA changed keys at {path}; missing={missing}, added={added}")
        for key in reference:
            validate_same_json_shape(reference[key], candidate[key], f"{path}.{key}")
    elif isinstance(reference, list):
        if len(reference) != len(candidate):
            raise ValueError(
                f"Final QA changed list length at {path}: {len(reference)} -> {len(candidate)}"
            )
        for index, (before, after) in enumerate(zip(reference, candidate)):
            validate_same_json_shape(before, after, f"{path}[{index}]")


def validate_final_review_candidate(reference: dict[str, Any], candidate: dict[str, Any]) -> None:
    validate_same_json_shape(reference, candidate)

    if reference.get("config") != candidate.get("config"):
        raise ValueError("Final QA changed the locked config object")

    for key in ("name", "contact", "linkedin_url", "github_url"):
        if reference.get(key) != candidate.get(key):
            raise ValueError(f"Final QA changed locked identity field: {key}")

    def compare_records(
        collection_names: tuple[str, ...],
        locked_fields: tuple[str, ...],
        label: str,
    ) -> None:
        collection_name = next((name for name in collection_names if name in reference), collection_names[0])
        before_items = reference.get(collection_name) or []
        after_items = candidate.get(collection_name) or []
        for index, (before, after) in enumerate(zip(before_items, after_items)):
            for field in locked_fields:
                if before.get(field) != after.get(field):
                    raise ValueError(
                        f"Final QA changed locked {label} field at index {index}: {field}"
                    )

    compare_records(
        ("experience", "professional_experience"),
        ("company", "title", "location", "dates", "employment_note"),
        "experience",
    )
    compare_records(
        ("projects",),
        ("name", "github_url", "tech_label", "tech"),
        "project",
    )
    compare_records(
        ("education",),
        ("university", "location", "degree", "graduation"),
        "education",
    )

    before_skills = reference.get("skills")
    after_skills = candidate.get("skills")
    if isinstance(before_skills, dict) and isinstance(after_skills, dict):
        for key, value in before_skills.items():
            if key.endswith("_label") and after_skills.get(key) != value:
                raise ValueError(f"Final QA changed locked skill-row label: {key}")


def restore_final_review_locks(
    reference: dict[str, Any],
    candidate: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    """Restore identity and renderer-locked values without discarding safe text edits."""
    restored = copy.deepcopy(candidate)
    changes: list[str] = []

    def restore_value(container: dict[str, Any], source: dict[str, Any], key: str, path: str) -> None:
        if source.get(key) != container.get(key):
            container[key] = copy.deepcopy(source.get(key))
            changes.append(path)

    restore_value(restored, reference, "config", "config")
    for key in ("name", "contact", "linkedin_url", "github_url"):
        restore_value(restored, reference, key, key)

    def restore_records(
        collection_names: tuple[str, ...],
        locked_fields: tuple[str, ...],
    ) -> None:
        collection_name = next((name for name in collection_names if name in reference), collection_names[0])
        before_items = reference.get(collection_name) or []
        after_items = restored.get(collection_name) or []
        for index, (before, after) in enumerate(zip(before_items, after_items)):
            if not isinstance(before, dict) or not isinstance(after, dict):
                continue
            for field in locked_fields:
                restore_value(after, before, field, f"{collection_name}[{index}].{field}")

    restore_records(
        ("experience", "professional_experience"),
        ("company", "title", "location", "dates", "employment_note"),
    )
    restore_records(("projects",), ("name", "github_url", "tech_label", "tech"))
    restore_records(
        ("education",),
        ("university", "location", "degree", "graduation"),
    )

    before_skills = reference.get("skills")
    after_skills = restored.get("skills")
    if isinstance(before_skills, dict) and isinstance(after_skills, dict):
        for key, value in before_skills.items():
            if key.endswith("_label") and after_skills.get(key) != value:
                after_skills[key] = copy.deepcopy(value)
                changes.append(f"skills.{key}")

    return restored, changes


async def call_model(
    *,
    system_blocks: list[dict[str, Any]],
    messages: list[dict[str, str]],
    label: str,
    max_tokens: int = 16384,
    cost_cb=None,
    output_validator: Callable[[str], str | None] | None = None,
    retry_instruction: str = NVIDIA_RETRY_INSTRUCTION,
    cancel_event: threading.Event | None = None,
    provider_override: str | None = None,
    model_override: str | None = None,
    nvidia_thinking_override: bool | None = None,
) -> str:
    provider = provider_override or get_provider()
    if provider == "nvidia":
        model = model_override or get_nvidia_model()
    else:
        model = get_model()
    nvidia_thinking = (
        get_nvidia_thinking()
        if nvidia_thinking_override is None
        else nvidia_thinking_override
    )
    t0 = time.monotonic()

    text = ""
    input_tokens = 0
    output_tokens = 0
    cache_create = 0
    cache_read = 0
    attempts_used = 1
    finish_reason = ""
    last_error: Exception | None = None
    rejection_reason = ""
    cancel_after_accounting = False

    if provider == "nvidia":
        max_attempts = get_nvidia_max_attempts() if output_validator else 1
        for attempt in range(1, max_attempts + 1):
            raise_if_cancelled(cancel_event)
            attempts_used = attempt
            if attempt > 1:
                await wait_before_retry(min(2 ** (attempt - 2), 8), cancel_event)
            attempt_messages = list(messages)
            if attempt > 1:
                detail = f"Rejection reason: {rejection_reason}" if rejection_reason else ""
                attempt_messages.append({
                    "role": "user",
                    "content": "\n\n".join(part for part in [retry_instruction.strip(), detail] if part),
                })
            try:
                response = await asyncio.to_thread(
                    call_nvidia_sync,
                    system_blocks=system_blocks,
                    messages=attempt_messages,
                    model=model,
                    thinking=nvidia_thinking,
                    max_tokens=max_tokens,
                    cancel_event=cancel_event,
                )
            except OperationCancelled:
                raise
            except Exception as exc:
                last_error = exc
                rejection_reason = f"API error: {exc}"
                log(f"{label}: NVIDIA attempt {attempt}/{max_attempts} failed: {exc}")
                continue

            text = response.text
            finish_reason = response.finish_reason
            input_tokens += response.usage["input_tokens"]
            output_tokens += response.usage["output_tokens"]
            cache_create += response.usage["cache_creation_input_tokens"]
            cache_read += response.usage["cache_read_input_tokens"]

            problems: list[str] = []
            if output_validator:
                validator_error = output_validator(text)
                if validator_error:
                    problems.append(validator_error)
            if not problems:
                rejection_reason = ""
                break
            rejection_reason = "; ".join(problems)
            log(
                f"{label}: NVIDIA attempt {attempt}/{max_attempts} rejected: "
                f"{rejection_reason}"
            )

        if rejection_reason or (last_error and not text):
            fallback_enabled = config_bool(load_config().get("fallback_to_anthropic"), False)
            if fallback_enabled:
                log(f"{label}: NVIDIA attempts exhausted; falling back to direct Anthropic.")
                provider = "anthropic"
                model = get_model()
            elif not text:
                raise RuntimeError(
                    f"{label}: NVIDIA failed after {attempts_used} attempts: {last_error}"
                ) from last_error
            else:
                log(
                    f"{label}: NVIDIA attempts exhausted; returning final rejected response "
                    f"for raw-output diagnostics ({rejection_reason})."
                )

    if provider == "anthropic":
        raise_if_cancelled(cancel_event)
        client = get_client()
        resp = await client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_blocks,
            messages=messages,
        )
        text = resp.content[0].text.strip()
        cancel_after_accounting = bool(cancel_event and cancel_event.is_set())
        usage = resp.usage
        input_tokens = usage.input_tokens
        output_tokens = usage.output_tokens
        cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
        cache_create = getattr(usage, "cache_creation_input_tokens", 0) or 0

    estimated_cost = estimate_cost_usd(
        model,
        input_tokens,
        output_tokens,
        cache_create,
        cache_read,
    )
    elapsed = time.monotonic() - t0
    thinking_log = f" thinking={'on' if nvidia_thinking else 'off'}" if provider == "nvidia" else ""
    log(
        f"{label}: provider={provider} model={model}{thinking_log} "
        f"in={input_tokens} out={output_tokens} "
        f"cache_read={cache_read} cache_create={cache_create} "
        f"attempts={attempts_used} finish_reason={finish_reason or 'unknown'} "
        f"cost=${estimated_cost:.4f} elapsed={elapsed:.1f}s"
    )
    if cost_cb:
        cost_cb(CostEvent(
            label=label,
            model=(
                f"{provider}:{model}:thinking={'on' if nvidia_thinking else 'off'}"
                if provider == "nvidia"
                else f"{provider}:{model}"
            ),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_creation_input_tokens=cache_create,
            cache_read_input_tokens=cache_read,
            estimated_cost_usd=estimated_cost,
            attempts=attempts_used,
            finish_reason=finish_reason,
        ))
    if cancel_after_accounting:
        raise OperationCancelled("Operation stopped by user.")
    return text


def pass1_system(prompt_profile: str | None = None) -> list[dict[str, Any]]:
    if normalize_prompt_profile(prompt_profile) == "v1":
        return [
            cached_text_block(read_prompt("pass_1.md", prompt_profile)),
            cached_text_block(read_prompt("story.md", prompt_profile)),
        ]
    return [
        cached_text_block(read_prompt("prompt.md", prompt_profile)),
        cached_text_block(read_prompt("story.md", prompt_profile)),
    ]


def pass2_system(prompt_profile: str | None = None) -> list[dict[str, Any]]:
    if normalize_prompt_profile(prompt_profile) == "v1":
        return [
            cached_text_block(read_prompt("pass_2.md", prompt_profile)),
            cached_text_block(read_prompt("story.md", prompt_profile)),
        ]
    return pass1_system(prompt_profile)


def recruiter_system(prompt_profile: str | None = None) -> list[dict[str, Any]]:
    if normalize_prompt_profile(prompt_profile) == "v1":
        return [cached_text_block(read_prompt("final_check.md", prompt_profile))]
    return [cached_text_block(read_prompt("recruiter.md", prompt_profile))]


def labeled_step(request_label: str, step: str) -> str:
    return f"{request_label} | {step}" if request_label else step


async def run_pass1(
    inp: ResumeInput,
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
    prompt_profile: str = "stable",
) -> str:
    profile = normalize_prompt_profile(prompt_profile)
    if profile == "v1":
        user_message = input_to_text(inp)
    else:
        user_message = "\n\n".join([
            read_prompt("prompt_short.md", profile),
            PASS1_COMPACT_INSTRUCTION,
            input_to_text(inp),
        ])
    return await call_model(
        system_blocks=pass1_system(profile),
        messages=[{"role": "user", "content": user_message}],
        label=labeled_step(request_label, "PASS 1"),
        max_tokens=16384,
        cost_cb=cost_cb,
        output_validator=validate_pass1_response,
        retry_instruction=(
            NVIDIA_RETRY_INSTRUCTION
            + "\nReturn the required DES CANDIDATE BANK with parseable lines starting DES 1 |."
        ),
        cancel_event=cancel_event,
        model_override=nvidia_model,
        nvidia_thinking_override=nvidia_thinking,
    )


async def run_pass2(
    inp: ResumeInput,
    pass1_text: str,
    approval_text: str,
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
    prompt_profile: str = "stable",
) -> str:
    profile = normalize_prompt_profile(prompt_profile)
    normalized_approval = normalize_approval(approval_text)
    if profile == "v1":
        messages = [{
            "role": "user",
            "content": "\n\n".join([
                "ORIGINAL INPUT:",
                input_to_text(inp),
                "PASS 1 OUTPUT:",
                pass1_text.strip(),
                "APPROVED DES:",
                normalized_approval,
            ]),
        }]
    else:
        first_user = "\n\n".join([
            read_prompt("prompt_short.md", profile),
            PASS1_COMPACT_INSTRUCTION,
            input_to_text(inp),
        ])
        messages = [
            {"role": "user", "content": first_user},
            {"role": "assistant", "content": pass1_text},
            {"role": "user", "content": PASS2_COMPACT_INSTRUCTION + "\n\n" + normalized_approval},
        ]
    return await call_model(
        system_blocks=pass2_system(profile),
        messages=messages,
        label=labeled_step(request_label, "PASS 2"),
        max_tokens=16384,
        cost_cb=cost_cb,
        output_validator=validate_v1_resume_response if profile == "v1" else validate_json_response,
        cancel_event=cancel_event,
        model_override=nvidia_model,
        nvidia_thinking_override=nvidia_thinking,
    )


async def run_recruiter_review(
    *,
    jd: str,
    resume1_json: dict[str, Any],
    company: str = "",
    title: str = "",
    des: str = "",
    resume2_json: dict[str, Any] | None = None,
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
    prompt_profile: str = "stable",
    pass1_audit: str = "",
) -> str:
    profile = normalize_prompt_profile(prompt_profile)
    if profile == "v1":
        render_profile = build_render_profile(normalize_resume_json(copy.deepcopy(resume1_json)))
        parts = [
            HUMAN_TEXT_STYLE_RULE.strip(),
            "",
            "Original JD:",
            jd.strip(),
            "",
            "Source resume JSON:",
            json.dumps(resume1_json, indent=2),
            "",
            "Stage 1 audit:",
            pass1_audit.strip() or "Not available.",
            "",
            "Render profile from manager.py:",
            json.dumps(render_profile, indent=2),
        ]
    else:
        parts = [
            read_prompt("recruiter_short.md", profile),
            RECRUITER_COMPACT_INSTRUCTION.strip(),
            "",
            HUMAN_TEXT_STYLE_RULE.strip(),
            "",
            "TARGET COMPANY:",
            company.strip(),
            "TARGET TITLE:",
            title.strip(),
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
        system_blocks=recruiter_system(profile),
        messages=[{"role": "user", "content": "\n".join(parts)}],
        label=labeled_step(request_label, "FINAL CHECK" if profile == "v1" else "RECRUITER REVIEW"),
        max_tokens=16384,
        cost_cb=cost_cb,
        output_validator=validate_v1_resume_response if profile == "v1" else validate_json_response,
        cancel_event=cancel_event,
        model_override=nvidia_model,
        nvidia_thinking_override=nvidia_thinking,
    )


async def run_final_review(
    *,
    jd: str,
    source_resume_json: dict[str, Any],
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    progress_cb: Callable[[int, str], None] | None = None,
    artifact_cb: Callable[[str, Any], None] | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
) -> FinalReviewResult:
    source_resume_json = normalize_resume_json(source_resume_json)
    render_profile = build_render_profile(source_resume_json)
    if artifact_cb:
        artifact_cb("render_profile", render_profile)
    shared_context = "\n\n".join([
        "JOB DESCRIPTION:",
        jd.strip(),
        "RENDER PROFILE GENERATED BY manager.py:",
        json.dumps(render_profile, indent=2),
        "SOURCE RESUME JSON:",
        json.dumps(source_resume_json, indent=2),
    ])
    common_system = [
        cached_text_block(FINAL_QA_CONTRACT.strip()),
        cached_text_block(shared_context),
    ]
    model = nvidia_model or get_nvidia_model()
    thinking = get_nvidia_thinking() if nvidia_thinking is None else nvidia_thinking

    def progress(step: int, message: str) -> None:
        if progress_cb:
            progress_cb(step, message)

    progress(1, "Final QA 1/3: auditing")
    audit_raw = await call_model(
        system_blocks=common_system + [cached_text_block(read_final_qa_prompt("01_Resume_Audit.md"))],
        messages=[{
            "role": "user",
            "content": (
                "Run the read-only resume audit now. Analyze the source JSON as it will render under "
                "the supplied render profile. Do not rewrite the resume and do not output resume JSON."
            ),
        }],
        label=labeled_step(request_label, "FINAL QA 1/3 AUDIT"),
        max_tokens=16384,
        cost_cb=cost_cb,
        cancel_event=cancel_event,
        output_validator=validate_nonempty_response,
        provider_override="nvidia",
        model_override=model,
        nvidia_thinking_override=thinking,
    )
    if not audit_raw.strip():
        raise ValueError("Final QA audit returned no output")
    if artifact_cb:
        artifact_cb("audit_raw", audit_raw)

    progress(2, "Final QA 2/3: repairing JSON")
    repair_raw = await call_model(
        system_blocks=common_system + [cached_text_block(read_final_qa_prompt("02_Experience_Rewrite.md"))],
        messages=[{
            "role": "user",
            "content": "\n\n".join([
                "AUDIT FROM STAGE 1:",
                audit_raw,
                FINAL_QA_REPAIR_OUTPUT.strip(),
            ]),
        }],
        label=labeled_step(request_label, "FINAL QA 2/3 REPAIR"),
        max_tokens=16384,
        cost_cb=cost_cb,
        cancel_event=cancel_event,
        output_validator=validate_json_response,
        provider_override="nvidia",
        model_override=model,
        nvidia_thinking_override=thinking,
    )
    if artifact_cb:
        artifact_cb("repair_raw", repair_raw)
    repaired_json = extract_json(repair_raw)
    repaired_json, repair_restored = restore_final_review_locks(source_resume_json, repaired_json)
    validate_final_review_candidate(source_resume_json, repaired_json)
    if artifact_cb:
        artifact_cb("repaired_json", repaired_json)

    progress(3, "Final QA 3/3: final scan")
    final_scan_raw = await call_model(
        system_blocks=common_system + [cached_text_block(read_final_qa_prompt("03_ATS_Hiring_Manager_Scan.md"))],
        messages=[{
            "role": "user",
            "content": "\n\n".join([
                "ORIGINAL AUDIT:",
                audit_raw,
                "REPAIRED JSON FROM STAGE 2:",
                json.dumps(repaired_json, indent=2),
                FINAL_QA_SCAN_OUTPUT.strip(),
            ]),
        }],
        label=labeled_step(request_label, "FINAL QA 3/3 FINAL SCAN"),
        max_tokens=16384,
        cost_cb=cost_cb,
        cancel_event=cancel_event,
        output_validator=validate_json_response,
        provider_override="nvidia",
        model_override=model,
        nvidia_thinking_override=thinking,
    )
    if artifact_cb:
        artifact_cb("final_scan_raw", final_scan_raw)
    final_json = extract_json(final_scan_raw)
    final_json, scan_restored = restore_final_review_locks(source_resume_json, final_json)
    validate_final_review_candidate(source_resume_json, final_json)
    if artifact_cb:
        artifact_cb("final_json", final_json)
    progress(3, "Final QA JSON ready")
    return FinalReviewResult(
        audit_raw=audit_raw,
        repair_raw=repair_raw,
        repaired_json=repaired_json,
        final_scan_raw=final_scan_raw,
        final_json=final_json,
        render_profile=render_profile,
        restored_locks=sorted(set(repair_restored + scan_restored)),
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
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
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
        max_tokens=16384,
        cost_cb=cost_cb,
        cancel_event=cancel_event,
        model_override=nvidia_model,
        nvidia_thinking_override=nvidia_thinking,
    )


def normalize_resume_json(data: dict[str, Any]) -> dict[str, Any]:
    for collection_name in ("experience", "professional_experience"):
        jobs = data.get(collection_name)
        if not isinstance(jobs, list):
            continue
        for job in jobs:
            if isinstance(job, dict):
                job.setdefault("employment_note", "")
    return data


def extract_json(text: str) -> dict[str, Any]:
    blocks = re.findall(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    candidates = blocks or re.findall(r"(\{.*\})", text, flags=re.DOTALL)
    last_error: Exception | None = None
    for candidate in reversed(candidates):
        try:
            return normalize_resume_json(json.loads(candidate))
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
