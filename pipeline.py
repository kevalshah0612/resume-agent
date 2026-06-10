"""
New resume flow.

Flow 1:
  PASS 1 -> DES approval / CONFIRM -> final resume JSON

Flow 2:
  recruiter review -> final JSON for DOCX

The Markdown prompt files are loaded as-is from new_flow. Large static
prompt/story blocks use Anthropic prompt caching; only the job input changes
between calls.
"""

from __future__ import annotations

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

DEFAULT_MODEL = "claude-sonnet-4-6"

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
2. one JSON code block
Do not print long audits or extra tables.
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
}


def load_config() -> dict[str, Any]:
    if CFG_FILE.exists():
        return json.loads(CFG_FILE.read_text(encoding="utf-8"))
    return {}


def get_client() -> anthropic.AsyncAnthropic:
    cfg = load_config()
    key = os.environ.get("ANTHROPIC_API_KEY") or cfg.get("anthropic_api_key", "")
    if not key:
        raise RuntimeError(
            "No Anthropic API key found. Set ANTHROPIC_API_KEY or add it to pipeline_config.json."
        )
    return anthropic.AsyncAnthropic(api_key=key)


def get_model() -> str:
    cfg = load_config()
    return cfg.get("model_resume") or cfg.get("model_sonnet") or DEFAULT_MODEL


def estimate_cost_usd(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_creation_input_tokens: int = 0,
    cache_read_input_tokens: int = 0,
) -> float:
    rates = MODEL_PRICING_PER_MTOK.get(model, MODEL_PRICING_PER_MTOK["claude-sonnet-4-6"])
    return (
        input_tokens * rates["input"]
        + cache_creation_input_tokens * rates["cache_write"]
        + cache_read_input_tokens * rates["cache_read"]
        + output_tokens * rates["output"]
    ) / 1_000_000


def read_prompt(name: str) -> str:
    path = PROMPT_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing prompt file: {path}")
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
    client = get_client()
    model = get_model()
    t0 = time.monotonic()
    resp = await client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_blocks,
        messages=messages,
    )
    text = resp.content[0].text.strip()
    usage = resp.usage
    cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
    cache_create = getattr(usage, "cache_creation_input_tokens", 0) or 0
    estimated_cost = estimate_cost_usd(
        model,
        usage.input_tokens,
        usage.output_tokens,
        cache_create,
        cache_read,
    )
    elapsed = time.monotonic() - t0
    log(
        f"{label}: in={usage.input_tokens} out={usage.output_tokens} "
        f"cache_read={cache_read} cache_create={cache_create} "
        f"cost=${estimated_cost:.4f} elapsed={elapsed:.1f}s"
    )
    if cost_cb:
        cost_cb(CostEvent(
            label=label,
            model=model,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
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


async def run_pass1(inp: ResumeInput, cost_cb=None) -> str:
    user_message = "\n\n".join([
        read_prompt("prompt_short.md"),
        PASS1_COMPACT_INSTRUCTION,
        input_to_text(inp),
    ])
    return await call_model(
        system_blocks=flow1_system(),
        messages=[{"role": "user", "content": user_message}],
        label="PASS 1",
        max_tokens=3500,
        cost_cb=cost_cb,
    )


async def run_pass2(inp: ResumeInput, pass1_text: str, approval_text: str, cost_cb=None) -> str:
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
        label="PASS 2",
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
) -> str:
    parts = [
        read_prompt("recruiter_short.md"),
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
        label="RECRUITER REVIEW",
        max_tokens=12000,
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


REPAIR_VERBS = [
    "Optimized",
    "Delivered",
    "Implemented",
    "Developed",
    "Integrated",
    "Automated",
    "Refactored",
    "Stabilized",
    "Improved",
    "Deployed",
    "Standardized",
    "Resolved",
    "Architected",
    "Instrumented",
]


def repair_repeated_verbs(data: dict[str, Any]) -> dict[str, Any]:
    """Fix duplicate opening verbs by changing only the first word of later bullets."""
    used: set[str] = set()

    def repair_bullet(text: Any) -> str:
        bullet = str(text or "").strip()
        if not bullet:
            return bullet
        parts = bullet.split(maxsplit=1)
        first = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        verb_key = re.sub(r"[^A-Za-z-]", "", first).lower()
        if verb_key and verb_key not in used:
            used.add(verb_key)
            return bullet.rstrip(".")
        for replacement in REPAIR_VERBS:
            key = replacement.lower()
            if key not in used:
                used.add(key)
                return f"{replacement} {rest}".strip().rstrip(".")
        return bullet.rstrip(".")

    for section in ("professional_experience", "projects"):
        for item in data.get(section) or []:
            item["bullets"] = [repair_bullet(b) for b in (item.get("bullets") or [])]

    for edu in data.get("education") or []:
        if str(edu.get("ta_bullet") or "").strip():
            edu["ta_bullet"] = repair_bullet(edu["ta_bullet"])

    return data


def validate_resume_json(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    top_keys = [
        "config",
        "name",
        "contact",
        "linkedin_url",
        "github_url",
        "summary",
        "education",
        "technical_skills",
        "professional_experience",
        "projects",
    ]
    config_keys = [
        "type",
        "level",
        "layout_profile",
        "output",
        "bold_markers",
        "ta_active",
        "company",
        "role",
    ]
    if list(data.keys()) != top_keys:
        errors.append("Top-level keys or key order do not match the new schema.")
    cfg = data.get("config")
    if not isinstance(cfg, dict) or list(cfg.keys()) != config_keys:
        errors.append("Config keys or key order do not match the new schema.")
    if not isinstance(data.get("technical_skills"), dict):
        errors.append("technical_skills must be an object/dictionary.")

    for idx, edu in enumerate(data.get("education") or [], 1):
        if list(edu.keys()) != ["university", "degree", "location", "graduation", "ta_bullet"]:
            errors.append(f"Education item {idx} has invalid keys.")

    for idx, job in enumerate(data.get("professional_experience") or [], 1):
        if list(job.keys()) != ["company", "title", "location", "dates", "bullets"]:
            errors.append(f"Professional experience item {idx} has invalid keys.")

    for idx, project in enumerate(data.get("projects") or [], 1):
        if list(project.keys()) != ["name", "tech", "github_url", "bullets"]:
            errors.append(f"Project item {idx} has invalid keys.")

    banned = {
        "institution",
        "gpa",
        "ta",
        "client",
        "url",
        "link",
        "repository",
        "technologies",
    }

    def walk(value: Any, path: str = "$") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in banned:
                    errors.append(f"Banned key found at {path}.{key}")
                walk(child, f"{path}.{key}")
        elif isinstance(value, list):
            for i, child in enumerate(value):
                walk(child, f"{path}[{i}]")

    walk(data)

    verbs: dict[str, str] = {}
    for section in ("professional_experience", "projects"):
        for i, item in enumerate(data.get(section) or [], 1):
            for j, bullet in enumerate(item.get("bullets") or [], 1):
                words = str(bullet).strip().split()
                if not words:
                    errors.append(f"Empty bullet at {section}[{i}].bullets[{j}]")
                    continue
                verb = re.sub(r"[^A-Za-z-]", "", words[0]).lower()
                location = f"{section}[{i}].bullets[{j}]"
                if verb in verbs:
                    errors.append(f"Repeated opening verb '{words[0]}' at {verbs[verb]} and {location}.")
                verbs[verb] = location
                if str(bullet).strip().endswith("."):
                    errors.append(f"Bullet ends with a period at {location}.")

    for i, edu in enumerate(data.get("education") or [], 1):
        ta_bullet = str(edu.get("ta_bullet") or "").strip()
        if ta_bullet:
            words = ta_bullet.split()
            verb = re.sub(r"[^A-Za-z-]", "", words[0]).lower()
            location = f"education[{i}].ta_bullet"
            if verb in verbs:
                errors.append(f"Repeated opening verb '{words[0]}' at {verbs[verb]} and {location}.")
            verbs[verb] = location
            if ta_bullet.endswith("."):
                errors.append(f"TA bullet ends with a period at {location}.")

    return errors


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return cleaned or "Resume"


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M")


def meaningful_stem(company: str, role: str = "") -> str:
    role_part = slug(role or "Software_Engineer")
    return f"Keval_Shah_{slug(company)}_{role_part}_{timestamp()}"


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
        if line.startswith("DOCX saved:"):
            return ROOT / line.split("DOCX saved:", 1)[1].strip()
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
