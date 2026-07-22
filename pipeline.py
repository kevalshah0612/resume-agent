"""
New resume flow.

Flow 1:
  PASS 1 -> DES approval / CONFIRM -> final resume JSON

Flow 2:
  recruiter review -> final JSON for DOCX

V1 is the default three-prompt flow. Stable and V3 remain available as explicit profiles.
The provider layer uses NVIDIA first when configured, with direct Claude
fallback only for profiles that allow it.
"""

from __future__ import annotations

import asyncio
import copy
import json
import os
import random
import re
import subprocess
import sys
import threading
import time
from html import unescape
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qs, quote_plus, urlparse
from urllib.request import Request, urlopen

import anthropic

from app_properties import (
    CANDIDATE_NAME,
    CURRENT_LOCATION,
    GITHUB_URL,
    LINKEDIN_URL,
    PROMPT_PROFILE_LABELS,
    PROJECT_URLS,
    VERIFIED_GRADUATE_COURSEWORK,
    VERIFIED_GRADUATE_GPA,
    candidate_contact_line,
    candidate_education_profile,
    candidate_experience_profile,
)
from manager import build_render_profile


ROOT = Path(__file__).parent
PROMPT_DIR = ROOT / "main_flow"
PROMPT_V1_DIR = ROOT / "V1" / "Prompts"
V1_POST_STAGE_DIR = ROOT / "v1" / "2 stage"
PROMPT_V3_DIR = ROOT / "v3_experimental_flow"
FINAL_QA_PROMPT_DIR = ROOT / "3_stage_validation"
RUNS_DIR = ROOT / "runs"
CFG_FILE = ROOT / "pipeline_config.json"
ENV_FILE = ROOT / ".env"

DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_NVIDIA_MODEL = "nvidia/nemotron-3-ultra-550b-a55b"
DEFAULT_NVIDIA_MAX_ATTEMPTS = 5
DEFAULT_NVIDIA_MAX_CONCURRENT_REQUESTS = 2
DEFAULT_NVIDIA_MAX_CONCURRENT_REQUESTS_PER_ACCOUNT = 1
DEFAULT_NVIDIA_TIMEOUT_SECONDS = 0.0
DEFAULT_NVIDIA_TEMPERATURE = 1.0
DEFAULT_NVIDIA_TOP_P = 0.95
DEFAULT_NVIDIA_SEED = 42
DEFAULT_NVIDIA_VALIDATOR_SEED = 43
DEFAULT_NVIDIA_REASONING_BUDGET = 32768
DEFAULT_RESPONSE_MAX_TOKENS = 65536
WORKER_LOCAL_TOTAL_REQUEST_LIMIT_ERROR = "Worker local total request limit reached"

_log_cb = None
_nvidia_gate_lock = threading.Lock()
_nvidia_gate: threading.BoundedSemaphore | None = None
_nvidia_gate_limit: int | None = None
_nvidia_account_lock = threading.Lock()
_nvidia_account_cursor = 0
_nvidia_account_gates: dict[str, tuple[int, threading.BoundedSemaphore]] = {}

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
class V1PostValidationResult:
    ats_report: str
    optimized_resume: dict[str, Any]


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
    reasoning: str
    usage: dict[str, int]
    finish_reason: str
    queue_wait_seconds: float = 0.0
    provider_response_seconds: float = 0.0
    account_label: str = ""


@dataclass(frozen=True)
class NvidiaAccount:
    label: str
    api_key: str


@dataclass(frozen=True)
class NvidiaModelSpec:
    display_name: str
    model_id: str
    thinking_key: str | None
    stream: bool
    thinking_modes: tuple[bool, ...] | None = None
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
    seed: int | None = None

    def thinking_options(self) -> tuple[bool, ...]:
        if self.thinking_modes is not None:
            return self.thinking_modes
        return (True, False) if self.thinking_key else (False,)


NVIDIA_MODEL_SPECS = (
    NvidiaModelSpec(
        display_name="Nemo",
        model_id="nvidia/nemotron-3-ultra-550b-a55b",
        thinking_key="enable_thinking",
        stream=True,
        thinking_modes=(True,),
    ),
    NvidiaModelSpec(
        display_name="DS",
        model_id="deepseek-ai/deepseek-v4-pro",
        thinking_key="thinking",
        stream=False,
        thinking_modes=(True,),
    ),
    NvidiaModelSpec(
        display_name="Minimax",
        model_id="minimaxai/minimax-m3",
        thinking_key=None,
        stream=False,
    ),
    NvidiaModelSpec(
        display_name="GLM",
        model_id="z-ai/glm-5.2",
        thinking_key=None,
        stream=True,
        temperature=1.0,
        top_p=1.0,
        max_tokens=16384,
        seed=42,
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


async def wait_before_retry(seconds: float, cancel_event: threading.Event | None) -> None:
    remaining = max(0.0, float(seconds))
    while remaining > 0:
        raise_if_cancelled(cancel_event)
        interval = min(0.1, remaining)
        await asyncio.sleep(interval)
        remaining -= interval


MODEL_PRICING_PER_MTOK = {
    "claude-sonnet-4-6": {"input": 3.0, "cache_write": 3.75, "cache_read": 0.30, "output": 15.0},
    "claude-sonnet-4-5": {"input": 3.0, "cache_write": 3.75, "cache_read": 0.30, "output": 15.0},
    "claude-haiku-4-5": {"input": 1.0, "cache_write": 1.25, "cache_read": 0.10, "output": 5.0},
    "nvidia/nemotron-3-ultra-550b-a55b": {"input": 0.0, "cache_write": 0.0, "cache_read": 0.0, "output": 0.0},
    "deepseek-ai/deepseek-v4-pro": {"input": 0.0, "cache_write": 0.0, "cache_read": 0.0, "output": 0.0},
    "minimaxai/minimax-m3": {"input": 0.0, "cache_write": 0.0, "cache_read": 0.0, "output": 0.0},
    "z-ai/glm-5.2": {"input": 0.0, "cache_write": 0.0, "cache_read": 0.0, "output": 0.0},
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
        "NVIDIA_API_KEY_1": "nvidia_api_key_1",
        "NVIDIA_API_KEY_2": "nvidia_api_key_2",
        "NVIDIA_MODEL": "model_nvidia",
        "NVIDIA_THINKING": "nvidia_thinking",
        "NVIDIA_MEDIUM_EFFORT": "nvidia_medium_effort",
        "NVIDIA_TEMPERATURE": "nvidia_temperature",
        "NVIDIA_TOP_P": "nvidia_top_p",
        "NVIDIA_SEED": "nvidia_seed",
        "NVIDIA_REASONING_BUDGET": "nvidia_reasoning_budget",
        "NVIDIA_BASE_URL": "nvidia_base_url",
        "NVIDIA_MAX_ATTEMPTS": "nvidia_max_attempts",
        "NVIDIA_MAX_CONCURRENT_REQUESTS": "nvidia_max_concurrent_requests",
        "NVIDIA_MAX_CONCURRENT_REQUESTS_PER_ACCOUNT": "nvidia_max_concurrent_requests_per_account",
        "NVIDIA_TIMEOUT_SECONDS": "nvidia_timeout_seconds",
        "NVIDIA_GUIDED_JSON": "nvidia_guided_json",
        "NVIDIA_VALIDATION_PASS": "nvidia_validation_pass",
        "NVIDIA_VALIDATOR_SEED": "nvidia_validator_seed",
        "RESPONSE_MAX_TOKENS": "response_max_tokens",
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


def config_positive_int(value: Any, default: int, minimum: int = 1) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, parsed)


def config_float(value: Any, default: float, minimum: float, maximum: float) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(parsed, maximum))


def get_nvidia_max_attempts() -> int:
    cfg = load_config()
    return config_int(cfg.get("nvidia_max_attempts"), DEFAULT_NVIDIA_MAX_ATTEMPTS, 1, 10)


def get_nvidia_max_concurrent_requests() -> int:
    cfg = load_config()
    return config_int(
        cfg.get("nvidia_max_concurrent_requests"),
        DEFAULT_NVIDIA_MAX_CONCURRENT_REQUESTS,
        1,
        32,
    )


def get_nvidia_max_concurrent_requests_per_account() -> int:
    cfg = load_config()
    return config_int(
        cfg.get("nvidia_max_concurrent_requests_per_account"),
        DEFAULT_NVIDIA_MAX_CONCURRENT_REQUESTS_PER_ACCOUNT,
        1,
        16,
    )


def get_nvidia_timeout_seconds() -> float:
    """Return zero when the NVIDIA HTTP client should have no timeout."""
    return config_float(
        load_config().get("nvidia_timeout_seconds"),
        DEFAULT_NVIDIA_TIMEOUT_SECONDS,
        0.0,
        1800.0,
    )


def nvidia_request_gate() -> threading.BoundedSemaphore:
    global _nvidia_gate, _nvidia_gate_limit
    limit = get_nvidia_max_concurrent_requests()
    with _nvidia_gate_lock:
        if _nvidia_gate is None or _nvidia_gate_limit != limit:
            _nvidia_gate = threading.BoundedSemaphore(limit)
            _nvidia_gate_limit = limit
        return _nvidia_gate


def nvidia_account_gate(label: str) -> threading.BoundedSemaphore:
    limit = get_nvidia_max_concurrent_requests_per_account()
    with _nvidia_gate_lock:
        current = _nvidia_account_gates.get(label)
        if current is None or current[0] != limit:
            current = (limit, threading.BoundedSemaphore(limit))
            _nvidia_account_gates[label] = current
        return current[1]


def get_response_max_tokens() -> int:
    return config_positive_int(
        load_config().get("response_max_tokens"),
        DEFAULT_RESPONSE_MAX_TOKENS,
    )


def get_nvidia_thinking() -> bool:
    return config_bool(load_config().get("nvidia_thinking"), True)


def get_nvidia_medium_effort() -> bool:
    return config_bool(load_config().get("nvidia_medium_effort"), False)


def get_nvidia_temperature() -> float:
    return config_float(load_config().get("nvidia_temperature"), DEFAULT_NVIDIA_TEMPERATURE, 0.0, 1.0)


def get_nvidia_top_p() -> float:
    return config_float(load_config().get("nvidia_top_p"), DEFAULT_NVIDIA_TOP_P, 0.0, 1.0)


def get_nvidia_seed() -> int:
    return config_int(load_config().get("nvidia_seed"), DEFAULT_NVIDIA_SEED, 0, 2_147_483_647)


def get_nvidia_validator_seed() -> int:
    return config_int(load_config().get("nvidia_validator_seed"), DEFAULT_NVIDIA_VALIDATOR_SEED, 0, 2_147_483_647)


def get_nvidia_reasoning_budget() -> int:
    return config_int(load_config().get("nvidia_reasoning_budget"), DEFAULT_NVIDIA_REASONING_BUDGET, 0, 32768)


def get_nvidia_guided_json() -> bool:
    return config_bool(load_config().get("nvidia_guided_json"), True)


def get_nvidia_validation_pass() -> bool:
    return config_bool(load_config().get("nvidia_validation_pass"), True)


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
    if cfg.get("model_nvidia") or get_nvidia_accounts():
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
    if not spec.thinking_key:
        return spec.display_name
    effective_thinking = thinking if thinking in spec.thinking_options() else spec.thinking_options()[0]
    return f"{spec.display_name}-{'on' if effective_thinking else 'off'}"


def nvidia_model_options() -> list[str]:
    return [
        nvidia_model_option_label(spec.model_id, thinking)
        for spec in NVIDIA_MODEL_SPECS
        for thinking in spec.thinking_options()
    ]


def resolve_nvidia_model_option(label: str) -> tuple[str, bool]:
    for spec in NVIDIA_MODEL_SPECS:
        for thinking in spec.thinking_options():
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
    if raw in {"v1", "prompt_v1", "v1_flow", "v1 flow"}:
        return "v1"
    if raw in {"v3", "prompt_v3", "v3_experimental_flow", "v3 experimental"}:
        return "v3"
    return "stable"


def is_experimental_prompt_profile(value: str | None) -> bool:
    return normalize_prompt_profile(value) == "v3"


def prompt_profile_label(profile: str) -> str:
    return PROMPT_PROFILES[normalize_prompt_profile(profile)]


def prompt_profile_options() -> list[str]:
    return list(PROMPT_PROFILES.values())


def resolve_prompt_profile_label(label: str) -> str:
    for key, value in PROMPT_PROFILES.items():
        if label == value:
            return key
    return normalize_prompt_profile(label)


def get_nvidia_accounts() -> list[NvidiaAccount]:
    """Return configured NVIDIA credentials without exposing them to logs or diagnostics."""
    cfg = load_config()
    configured = [
        ("account_1", cfg.get("nvidia_api_key_1") or os.environ.get("NVIDIA_API_KEY_1", "")),
        ("account_2", cfg.get("nvidia_api_key_2") or os.environ.get("NVIDIA_API_KEY_2", "")),
    ]
    legacy = cfg.get("nvidia_api_key") or os.environ.get("NVIDIA_API_KEY", "")
    if legacy:
        configured.append(("account_default", legacy))

    accounts: list[NvidiaAccount] = []
    seen: set[str] = set()
    for label, raw_key in configured:
        key = str(raw_key or "").strip()
        if not key or key in seen:
            continue
        accounts.append(NvidiaAccount(label=label, api_key=key))
        seen.add(key)
    return accounts


def choose_nvidia_account() -> NvidiaAccount:
    global _nvidia_account_cursor
    accounts = get_nvidia_accounts()
    if not accounts:
        raise RuntimeError(
            "NVIDIA provider selected but no API key is configured. Set "
            "NVIDIA_API_KEY_1 and/or NVIDIA_API_KEY_2."
        )
    with _nvidia_account_lock:
        account = accounts[_nvidia_account_cursor % len(accounts)]
        _nvidia_account_cursor = (_nvidia_account_cursor + 1) % len(accounts)
    return account


def acquire_nvidia_account(
    cancel_event: threading.Event | None = None,
) -> tuple[NvidiaAccount, threading.BoundedSemaphore]:
    """Lease the next available account, using round-robin only to break ties."""
    global _nvidia_account_cursor
    while True:
        raise_if_cancelled(cancel_event)
        accounts = get_nvidia_accounts()
        if not accounts:
            return choose_nvidia_account(), threading.BoundedSemaphore(1)
        with _nvidia_account_lock:
            start = _nvidia_account_cursor % len(accounts)
        for offset in range(len(accounts)):
            index = (start + offset) % len(accounts)
            account = accounts[index]
            gate = nvidia_account_gate(account.label)
            if gate.acquire(blocking=False):
                with _nvidia_account_lock:
                    _nvidia_account_cursor = (index + 1) % len(accounts)
                return account, gate
        time.sleep(0.05)


def get_nvidia_client(account: NvidiaAccount | None = None):
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("openai is required for NVIDIA provider. Run: pip install openai") from exc

    cfg = load_config()
    selected = account or choose_nvidia_account()
    base_url = cfg.get("nvidia_base_url") or os.environ.get("NVIDIA_BASE_URL") or "https://integrate.api.nvidia.com/v1"
    return OpenAI(
        base_url=base_url,
        api_key=selected.api_key,
        timeout=(get_nvidia_timeout_seconds() or None),
        max_retries=0,
    )


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


def build_nvidia_request_payload(
    *,
    system_blocks: list[dict[str, Any]],
    messages: list[dict[str, str]],
    model: str,
    thinking: bool,
    max_tokens: int,
    seed_override: int | None = None,
    guided_json_schema: dict[str, Any] | None = None,
    reasoning_budget_override: int | None = None,
) -> dict[str, Any]:
    spec = get_nvidia_model_spec(model)
    extra_body: dict[str, Any] = {}
    if spec.thinking_key:
        extra_body["chat_template_kwargs"] = {spec.thinking_key: thinking}
    if model == DEFAULT_NVIDIA_MODEL:
        if get_nvidia_medium_effort():
            extra_body.setdefault("chat_template_kwargs", {})["medium_effort"] = True
        if thinking:
            configured_budget = (
                get_nvidia_reasoning_budget()
                if reasoning_budget_override is None
                else max(0, int(reasoning_budget_override))
            )
            budget = min(configured_budget, max(0, max_tokens - 1))
            if budget:
                extra_body["reasoning_budget"] = budget
    if guided_json_schema:
        extra_body["nvext"] = {"guided_json": guided_json_schema}
    payload: dict[str, Any] = {
        "model": model,
        "messages": openai_messages(system_blocks, messages),
        "temperature": spec.temperature if spec.temperature is not None else get_nvidia_temperature(),
        "top_p": spec.top_p if spec.top_p is not None else get_nvidia_top_p(),
        "seed": (
            seed_override
            if seed_override is not None
            else spec.seed if spec.seed is not None else get_nvidia_seed()
        ),
        "max_tokens": spec.max_tokens if spec.max_tokens is not None else max_tokens,
        "stream": spec.stream,
    }
    if extra_body:
        payload["extra_body"] = extra_body
    return payload


def compact_json(data: Any) -> str:
    """Serialize model handoffs without whitespace while preserving saved JSON readability."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def model_error_diagnostics(exc: Exception, diagnostics: dict[str, Any]) -> dict[str, Any]:
    """Build a credential-free diagnostic record for a failed provider call."""
    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", None)
    safe_headers: dict[str, str] = {}
    if headers is not None:
        for name in (
            "date",
            "server",
            "retry-after",
            "x-request-id",
            "request-id",
            "nvidia-request-id",
            "cf-ray",
        ):
            value = headers.get(name) or headers.get(name.title())
            if value:
                safe_headers[name] = str(value)
    request_id = (
        getattr(exc, "request_id", None)
        or safe_headers.get("x-request-id")
        or safe_headers.get("request-id")
        or safe_headers.get("nvidia-request-id")
        or ""
    )
    response_text = ""
    if response is not None:
        try:
            response_text = str(getattr(response, "text", "") or "")[:4000]
        except Exception:
            response_text = ""
    return {
        "error_type": type(exc).__name__,
        "message": str(exc),
        "status_code": getattr(exc, "status_code", None),
        "request_id": str(request_id),
        "response_headers": safe_headers,
        "response_body": response_text,
        "partial_response": str(getattr(exc, "nvidia_partial_response", "") or "")[:12000],
        "partial_reasoning": str(getattr(exc, "nvidia_partial_reasoning", "") or "")[:12000],
        "effective_provider": diagnostics.get("effective_provider", ""),
        "effective_model": diagnostics.get("effective_model", ""),
        "nvidia_accounts": list(diagnostics.get("nvidia_accounts") or []),
        "elapsed_seconds": round(float(diagnostics.get("total_response_time_seconds") or 0.0), 3),
        "sanitized_request_payload": diagnostics.get("sanitized_request_payload", {}),
    }


def sanitize_nvidia_request_payload(payload: dict[str, Any]) -> dict[str, Any]:
    sanitized = copy.deepcopy(payload)
    sanitized["messages"] = [
        {
            "role": message.get("role", ""),
            "content": f"<omitted {len(str(message.get('content', '')))} characters>",
        }
        for message in payload.get("messages", [])
    ]
    return sanitized


def is_retryable_nvidia_error(exc: Exception) -> bool:
    status_code = getattr(exc, "status_code", None)
    if status_code in {408, 409, 425, 429} or (isinstance(status_code, int) and status_code >= 500):
        return True
    name = type(exc).__name__.lower()
    module = type(exc).__module__.lower()
    retryable_names = ("timeout", "connection", "ratelimit", "apierror", "internalserver")
    return any(token in name for token in retryable_names) or (
        module.startswith("openai") and "error" in name and status_code not in {400, 401, 403, 404, 422}
    )


def nvidia_retry_delay_seconds(attempt: int, exc: Exception | None = None) -> float:
    """Honor provider Retry-After when available, otherwise back off with jitter."""
    response = getattr(exc, "response", None) if exc is not None else None
    headers = getattr(response, "headers", None)
    if headers is not None:
        retry_after = headers.get("retry-after") or headers.get("Retry-After")
        try:
            if retry_after is not None:
                return min(60.0, max(0.0, float(retry_after)))
        except (TypeError, ValueError):
            pass
    exponential = min(60.0, float(2 ** max(0, attempt - 1)))
    return exponential + random.uniform(0.0, min(1.0, exponential * 0.25))


def call_nvidia_sync(
    *,
    system_blocks: list[dict[str, Any]],
    messages: list[dict[str, str]],
    model: str,
    thinking: bool,
    max_tokens: int,
    seed_override: int | None = None,
    guided_json_schema: dict[str, Any] | None = None,
    reasoning_budget_override: int | None = None,
    cancel_event: threading.Event | None = None,
) -> NvidiaResponse:
    raise_if_cancelled(cancel_event)
    queue_started = time.monotonic()
    account, account_gate = acquire_nvidia_account(cancel_event)
    client = get_nvidia_client(account)
    payload = build_nvidia_request_payload(
        system_blocks=system_blocks,
        messages=messages,
        model=model,
        thinking=thinking,
        max_tokens=max_tokens,
        seed_override=seed_override,
        guided_json_schema=guided_json_schema,
        reasoning_budget_override=reasoning_budget_override,
    )
    stream = bool(payload["stream"])
    gate = nvidia_request_gate()
    try:
        while not gate.acquire(timeout=0.25):
            raise_if_cancelled(cancel_event)
    except Exception:
        account_gate.release()
        raise
    queue_wait_seconds = time.monotonic() - queue_started
    provider_started = time.monotonic()
    try:
        completion = client.chat.completions.create(**payload)
    except Exception as exc:
        try:
            setattr(exc, "nvidia_account_label", account.label)
            setattr(exc, "nvidia_queue_wait_seconds", queue_wait_seconds)
            setattr(exc, "nvidia_provider_response_seconds", time.monotonic() - provider_started)
        except Exception:
            pass
        gate.release()
        account_gate.release()
        raise
    usage_data = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "reasoning_tokens": 0,
    }

    if not stream:
        try:
            raise_if_cancelled(cancel_event)
            usage = getattr(completion, "usage", None)
            if usage is not None:
                usage_data["input_tokens"] = int(getattr(usage, "prompt_tokens", 0) or 0)
                usage_data["output_tokens"] = int(getattr(usage, "completion_tokens", 0) or 0)
                details = getattr(usage, "completion_tokens_details", None)
                usage_data["reasoning_tokens"] = int(getattr(details, "reasoning_tokens", 0) or 0)
            choice = completion.choices[0]
            return NvidiaResponse(
                text=(getattr(choice.message, "content", None) or "").strip(),
                reasoning=(getattr(choice.message, "reasoning_content", None) or "").strip(),
                usage=usage_data,
                finish_reason=str(getattr(choice, "finish_reason", "") or ""),
                queue_wait_seconds=queue_wait_seconds,
                provider_response_seconds=time.monotonic() - provider_started,
                account_label=account.label,
            )
        finally:
            gate.release()
            account_gate.release()

    parts: list[str] = []
    reasoning_parts: list[str] = []
    finish_reason = ""
    try:
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
                details = getattr(usage, "completion_tokens_details", None)
                usage_data["reasoning_tokens"] = int(getattr(details, "reasoning_tokens", 0) or 0)
            if not chunk.choices:
                continue
            choice = chunk.choices[0]
            chunk_finish_reason = getattr(choice, "finish_reason", None)
            if chunk_finish_reason:
                finish_reason = str(chunk_finish_reason)
            content = getattr(choice.delta, "content", None)
            if content is not None:
                parts.append(content)
            reasoning_content = getattr(choice.delta, "reasoning_content", None)
            if reasoning_content is not None:
                reasoning_parts.append(reasoning_content)
        return NvidiaResponse(
            text="".join(parts).strip(),
            reasoning="".join(reasoning_parts).strip(),
            usage=usage_data,
            finish_reason=finish_reason,
            queue_wait_seconds=queue_wait_seconds,
            provider_response_seconds=time.monotonic() - provider_started,
            account_label=account.label,
        )
    except Exception as exc:
        try:
            setattr(exc, "nvidia_account_label", account.label)
            setattr(exc, "nvidia_queue_wait_seconds", queue_wait_seconds)
            setattr(exc, "nvidia_provider_response_seconds", time.monotonic() - provider_started)
            setattr(exc, "nvidia_partial_response", "".join(parts))
            setattr(exc, "nvidia_partial_reasoning", "".join(reasoning_parts))
        except Exception:
            pass
        raise
    finally:
        gate.release()
        account_gate.release()


def prompt_dir_for_profile(prompt_profile: str | None = None) -> Path:
    profile = normalize_prompt_profile(prompt_profile)
    if profile == "v1":
        return PROMPT_V1_DIR
    if profile == "v3":
        return PROMPT_V3_DIR / "prompts"
    return PROMPT_DIR


def read_prompt(name: str, prompt_profile: str | None = None) -> str:
    prompt_dir = prompt_dir_for_profile(prompt_profile)
    path = prompt_dir / name
    if not path.exists():
        matches = [candidate for candidate in prompt_dir.iterdir() if candidate.name.lower() == name.lower()]
        if not matches:
            raise FileNotFoundError(f"Missing prompt file: {path}")
        path = matches[0]
    return path.read_text(encoding="utf-8")


def read_prompt_with_fallback(name: str, prompt_profile: str | None = None) -> str:
    try:
        return read_prompt(name, prompt_profile)
    except FileNotFoundError:
        return read_prompt(name, "stable")


def read_resume_rules() -> str:
    for path in (ROOT / "local" / "rules" / "Rules.md", ROOT / "rules" / "Rules.md"):
        if path.exists():
            return path.read_text(encoding="utf-8")
    return ""


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


def validate_compact_resume_response(text: str) -> str | None:
    json_error = validate_json_response(text)
    if json_error:
        return json_error
    data = extract_json(text)
    lower_keys = {str(key).lower() for key in data}
    if "experience" not in lower_keys and "professional_experience" not in lower_keys:
        return "Compact JSON must include experience"

    def first_present(*keys: str) -> Any:
        for key in keys:
            if key in data:
                return data[key]
        return None

    experience = first_present("experience", "Experience", "professional_experience", "Professional_Experience")
    if not isinstance(experience, list):
        return "Compact JSON experience must be a list"
    projects = first_present("projects", "Projects")
    if projects is not None and not isinstance(projects, list):
        return "Compact JSON projects must be a list when present"
    skills = first_present("skills", "Skills", "technical_skills", "Technical_Skills")
    if skills is not None and not isinstance(skills, (list, dict, str)):
        return "Compact JSON skills must be a list, object, or string when present"
    return None


def compact_config_type(value: Any) -> str:
    raw = str(value or "").strip().lower()
    if raw == "aiml":
        return "aiml"
    if raw == "fullstack":
        return "fullstack"
    return "backend"


def compact_type_label(value: Any) -> str:
    return {"backend": "Backend", "fullstack": "Fullstack", "aiml": "AIML"}[compact_config_type(value)]


def compact_level_config(value: Any) -> tuple[int, str]:
    raw = str(value or "").strip().lower()
    if raw in {"newgrad", "new grad", "new-grad", "campus", "campus-hire", "campushire", "student"}:
        return 2, "student_entry"
    if raw in {"entry", "entry-level", "intern", "internship", "2", "4"}:
        return 2, "professional_entry"
    return 3, "mid"


def compact_strategy_type(value: Any) -> str:
    raw = str(value or "").strip().lower()
    if raw in {"newgrad", "new grad", "new-grad", "campus", "campus-hire", "campushire", "student"}:
        return "NewGrad"
    if raw in {"mid", "production-first", "production_first", "tcs-first", "tcs_first"}:
        return "Mid"
    return "Entry"


def compact_strategy_level(value: Any) -> tuple[int, str]:
    return compact_level_config(compact_strategy_type(value))


def normalize_experience_order_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    raw = str(value or "").strip()
    if not raw:
        return []
    if "," in raw:
        return [part.strip() for part in raw.split(",") if part.strip()]
    normalized = raw.lower().replace("-", "_").replace(" ", "_")
    if normalized in {"tcs", "tcs_first", "professional_first", "mid", "production_first"}:
        return ["TCS-SWE-II", "TCS-SWE", "GHI", "TA"]
    if normalized in {"ghi", "ghi_first", "internship_first", "entry", "chronological"}:
        return ["TA", "GHI", "TCS-SWE-II", "TCS-SWE"]
    return []


def experience_order_rank(order: list[str]) -> dict[str, int]:
    aliases: dict[str, str] = {
        "ta": "TA",
        "teachingassistant": "TA",
        "binghamtonuniversity": "TA",
        "ghi": "GHI",
        "globalhealthimpact": "GHI",
        "tcssweii": "TCS-SWE-II",
        "softwareengineerii": "TCS-SWE-II",
        "tcsii": "TCS-SWE-II",
        "tcsswe": "TCS-SWE",
        "softwareengineer": "TCS-SWE",
        "tcs": "TCS-SWE",
    }
    rank: dict[str, int] = {}
    for index, item in enumerate(order):
        key = re.sub(r"[^a-z0-9]+", "", item.lower())
        canonical = aliases.get(key, item)
        rank[canonical] = index
    return rank


def experience_identity(job: dict[str, Any]) -> str:
    job_id = str(job.get("id") or job.get("ID") or "").strip()
    title = str(job.get("title") or job.get("Title") or "").strip().lower()
    company = str(job.get("company") or job.get("Company") or "").strip().lower()
    if job_id:
        return job_id
    if "binghamton university" in company or "teaching assistant" in title:
        return "TA"
    if "global health impact" in company:
        return "GHI"
    if "tata consultancy services" in company and "ii" in title:
        return "TCS-SWE-II"
    if "tata consultancy services" in company:
        return "TCS-SWE"
    return ""


def strategy_from_order(order: list[str], fallback: Any = "") -> str:
    explicit = compact_strategy_type(fallback)
    if explicit == "NewGrad":
        return explicit
    normalized = [re.sub(r"[^a-z0-9]+", "", item.lower()) for item in order]
    if normalized[:4] == ["tcssweii", "tcsswe", "ghi", "ta"]:
        return "Mid"
    if normalized[:4] == ["ta", "ghi", "tcssweii", "tcsswe"]:
        return "Entry"
    return explicit


def canonical_strategy_section_order(strategy_type: str) -> list[str]:
    if strategy_type == "Mid":
        return ["summary", "professional_experience", "projects", "education", "technical_skills"]
    return ["education", "professional_experience", "projects", "technical_skills"]


def canonical_strategy_experience_order(strategy_type: str) -> list[str]:
    if strategy_type == "Mid":
        return ["TCS-SWE-II", "TCS-SWE", "GHI", "TA"]
    return ["TA", "GHI", "TCS-SWE-II", "TCS-SWE"]


def normalize_section_order_value(value: Any) -> list[str]:
    aliases = {
        "summary": "summary",
        "technicalskills": "technical_skills",
        "skills": "technical_skills",
        "education": "education",
        "projects": "projects",
        "project": "projects",
        "professionalexperience": "professional_experience",
        "experience": "professional_experience",
    }
    raw_items = value if isinstance(value, list) else str(value or "").split(",")
    order: list[str] = []
    for item in raw_items:
        key = re.sub(r"[^a-z0-9]+", "", str(item).lower())
        canonical = aliases.get(key)
        if canonical and canonical not in order:
            order.append(canonical)
    return order


def experimental_role_label(value: Any) -> str:
    return compact_type_label(value) if str(value or "").strip() else "Auto"


def experimental_level_label(inp: ResumeInput) -> str:
    jd_title = f"{inp.title}\n{inp.jd}".lower()
    if re.search(r"\b(mid|senior|sr\.?|staff|lead|principal)\b", jd_title):
        return "mid"
    if re.search(r"\b(intern|internship|co-op|coop|new grad|entry[- ]level|university grad|early career)\b", jd_title):
        return "entry"
    return "auto"


def experimental_resume_configuration(inp: ResumeInput, prompt_profile: str | None = None) -> str:
    profile = normalize_prompt_profile(prompt_profile)
    role_type = experimental_role_label(inp.mode)
    explicit_override = role_type if role_type != "Auto" else "None"
    level = experimental_level_label(inp)
    allowed_projects = ", ".join(sorted(PROJECT_URLS))
    project_names = {
        "bistro": "Bistro AI",
        "evaltrace": "EvalTrace",
        "filingquery": "FilingQuery",
        "fraudsift": "FraudSift",
        "jobfill": "JobFill AI Extension",
        "jobpulse": "JobPulse",
        "resume agent": "Resume Agent",
        "reviewbot": "ReviewBot",
    }
    project_catalog = "\n".join(
        f"- Project ID: {key}\n  Approved project name: {project_names.get(key, key)}\n  Allowed evidence labels: Story 27 through Story 34 when that story names this project"
        for key in sorted(PROJECT_URLS)
    )
    if profile == "v3":
        return f"""=== RESUME CONFIGURATION - IMMUTABLE ===

RESUME_STRUCTURE:
{{
  "type_allowed": ["Backend", "Fullstack", "AIML"],
  "level_allowed": ["entry", "mid"],
  "requested_type": "{role_type}",
  "requested_level": "{level}",
  "summary_policy": {{
    "entry": "omit unless configured",
    "mid": "include 25-35 words"
  }},
  "experience": [
    {{
      "id": "TA",
      "include": true,
      "required": true,
      "title": "Teaching Assistant",
      "company": "Binghamton University",
      "location": "Binghamton, NY",
      "dates": "Aug 2025 - Present",
      "bullet_count": 2,
      "allowed_evidence_labels": ["EDU-TA-CODE-REVIEW"]
    }},
    {{
      "id": "GHI",
      "include": true,
      "title": "Software Engineering Intern",
      "company": "Global Health Impact",
      "location": "New York, NY",
      "dates": "Jun 2025 - Aug 2025",
      "bullet_count": 3,
      "allowed_evidence_labels": ["GHI-*"]
    }},
    {{
      "id": "TCS",
      "include": true,
      "title": "Software Engineer II",
      "company": "Tata Consultancy Services",
      "location": "Gandhinagar, India",
      "dates": "Mar 2021 - Dec 2024",
      "bullet_count": 5,
      "allowed_evidence_labels": ["TCS*"]
    }}
  ],
  "projects": {{
    "count": 2,
    "bullet_count_each": 1,
    "allowed_project_ids": [{", ".join(json.dumps(key) for key in sorted(PROJECT_URLS))}],
    "selection_rule": "Select the two configured projects that best cover JD gaps or strongest role evidence."
  }},
  "technical_skills": {{
    "format": "grouped category rows",
    "json_shape": "[[\"Category\", [\"skill\", \"skill\"]]]",
    "max_categories": 5,
    "max_skills_per_category": 6,
    "source_rule": "JD-relevant and traceable to Story.md, final bullets, or approved DES"
  }}
}}

FINAL_RESUME_JSON_TEMPLATE:
{{
  "type": "<Backend | Fullstack | AIML>",
  "level": "<entry | mid>",
  "summary": "<include only when level is mid or configuration requires it>",
  "experience": [
    {{
      "id": "TA",
      "title": "Teaching Assistant",
      "company": "Binghamton University",
      "location": "Binghamton, NY",
      "dates": "Aug 2025 - Present",
      "bullets": ["<bullet 1>", "<bullet 2>"]
    }},
    {{
      "id": "GHI",
      "title": "Software Engineering Intern",
      "company": "Global Health Impact",
      "location": "New York, NY",
      "dates": "Jun 2025 - Aug 2025",
      "bullets": ["<bullet 1>", "<bullet 2>", "<bullet 3>"]
    }},
    {{
      "id": "TCS",
      "title": "Software Engineer II",
      "company": "Tata Consultancy Services",
      "location": "Gandhinagar, India",
      "dates": "Mar 2021 - Dec 2024",
      "bullets": ["<bullet 1>", "<bullet 2>", "<bullet 3>", "<bullet 4>", "<bullet 5>"]
    }}
  ],
  "projects": [
    {{"name": "<selected configured project>", "bullets": ["<one project bullet>"]}},
    {{"name": "<selected configured project>", "bullets": ["<one project bullet>"]}}
  ],
  "technical_skills": [
    ["<Category>", ["<skill>", "<skill>"]]
  ]
}}

CANDIDATE EXPERIENCE CATALOG
- Experience ID: TA
  Canonical title: Teaching Assistant
  Company: Binghamton University
  Location: Binghamton, NY
  Dates: Aug 2025 - Present
  Allowed evidence labels: EDU-TA-CODE-REVIEW
- Experience ID: GHI
  Canonical title: Software Engineering Intern
  Company: Global Health Impact
  Location: New York, NY
  Dates: Jun 2025 - Aug 2025
  Allowed evidence labels: GHI evidence cards in Story.md
- Experience ID: TCS
  Canonical title: Software Engineer II
  Company: Tata Consultancy Services
  Location: Gandhinagar, India
  Dates: Mar 2021 - Dec 2024
  Allowed evidence labels: TCS evidence cards in Story.md

PROJECT CATALOG
{project_catalog}

ROUTING PRIORITY
- Requested role type: {role_type}
- Requested level: {level}
- Plan selection order: AIML when the JD candidate criteria explicitly require AI, ML, LLM, model, inference, evaluation, or data science; otherwise Fullstack when the JD candidate criteria explicitly require frontend plus backend; otherwise Backend.
- Fallback type: Backend
- Fallback level: mid unless the JD/title clearly says entry, new grad, internship, co-op, or early career.
- Any explicit type override: {explicit_override}

OUTPUT RULES
- Top-level JSON keys: type, level, optional summary, experience, projects, technical_skills.
- Experience order follows RESUME_STRUCTURE.
- TA is an experience row only when included; never write TA under Education.
- GHI has 3 bullets.
- TCS has exactly 5 bullets unless configuration overrides.
- Projects: exactly 2 projects, 1 bullet each.
- Skills: grouped into at most 5 category rows with at most 6 skills per row; compact, JD-relevant, evidence-traceable.

=== END RESUME CONFIGURATION ==="""

    return f"""=== RESUME CONFIGURATION - IMMUTABLE ===

CANDIDATE EXPERIENCE CATALOG
- Experience ID: tcs_se_ii
  Canonical title: Software Engineer II
  Company: Tata Consultancy Services
  Location:
  Dates: Oct 2022 - Dec 2024
  Allowed evidence labels: Story 01 through Story 12, Story 15 through Story 17, Story 35
- Experience ID: tcs_se
  Canonical title: Software Engineer
  Company: Tata Consultancy Services
  Location: Gandhinagar, India
  Dates: Mar 2021 - Sep 2022
  Allowed evidence labels: Story 01 through Story 17, Story 35
- Experience ID: ghi_se
  Canonical title: Software Engineer
  Company: Global Health Impact
  Location: New York, NY
  Dates: Jun 2025 - Aug 2025
  Allowed evidence labels: Story 21 through Story 25, Story 35

PROJECT CATALOG
{project_catalog}

ROUTING PRIORITY
- Requested role type: {role_type}
- Plan selection order: AIML when the JD candidate criteria explicitly require AI, ML, LLM, model, inference, evaluation, or data science; otherwise Fullstack when the JD candidate criteria explicitly require frontend plus backend; otherwise Backend.
- Fallback plan: Backend
- AIML / ML / LLM trigger terms: AI, ML, machine learning, LLM, model, inference, evaluation, data science
- Entry-level trigger terms: intern, internship, new grad, entry level
- Any explicit override: {explicit_override}

DISPLAY PLANS
- Plan ID: Backend
  Applies when: requested role type is Backend or fallback applies
  Display entries, in exact output order:
  - Display entry ID: tcs_se_ii
    Source Experience IDs: tcs_se_ii
    Output title: Software Engineer II
    Output company: Tata Consultancy Services
    Output location:
    Output dates: Oct 2022 - Dec 2024
    Maximum bullets: 3
  - Display entry ID: tcs_se
    Source Experience IDs: tcs_se
    Output title: Software Engineer
    Output company: Tata Consultancy Services
    Output location: Gandhinagar, India
    Output dates: Mar 2021 - Sep 2022
    Maximum bullets: 3
  - Display entry ID: ghi_se
    Source Experience IDs: ghi_se
    Output title: Software Engineer
    Output company: Global Health Impact
    Output location: New York, NY
    Output dates: Jun 2025 - Aug 2025
    Maximum bullets: 3
  Project selection:
    Required project count: 2
    Allowed Project IDs: {allowed_projects}
    Open-source project required: Yes
    Required bullets per project: 2
  Teaching Assistant rule: Do not include Teaching Assistant as an experience entry.
- Plan ID: Fullstack
  Applies when: requested role type is Fullstack, or JD candidate criteria require both frontend/client and backend/API qualifications
  Display entries, in exact output order:
  - Display entry ID: tcs_se_ii
    Source Experience IDs: tcs_se_ii
    Output title: Software Engineer II
    Output company: Tata Consultancy Services
    Output location:
    Output dates: Oct 2022 - Dec 2024
    Maximum bullets: 3
  - Display entry ID: tcs_se
    Source Experience IDs: tcs_se
    Output title: Software Engineer
    Output company: Tata Consultancy Services
    Output location: Gandhinagar, India
    Output dates: Mar 2021 - Sep 2022
    Maximum bullets: 3
  - Display entry ID: ghi_se
    Source Experience IDs: ghi_se
    Output title: Software Engineer
    Output company: Global Health Impact
    Output location: New York, NY
    Output dates: Jun 2025 - Aug 2025
    Maximum bullets: 3
  Project selection:
    Required project count: 2
    Allowed Project IDs: {allowed_projects}
    Open-source project required: Yes
    Required bullets per project: 2
  Teaching Assistant rule: Do not include Teaching Assistant as an experience entry.
- Plan ID: AIML
  Applies when: requested role type is AIML, or JD candidate criteria explicitly require AI, ML, LLM, model, inference, evaluation, or data science
  Display entries, in exact output order:
  - Display entry ID: ghi_se
    Source Experience IDs: ghi_se
    Output title: Software Engineer
    Output company: Global Health Impact
    Output location: New York, NY
    Output dates: Jun 2025 - Aug 2025
    Maximum bullets: 3
  - Display entry ID: tcs_se_ii
    Source Experience IDs: tcs_se_ii
    Output title: Software Engineer II
    Output company: Tata Consultancy Services
    Output location:
    Output dates: Oct 2022 - Dec 2024
    Maximum bullets: 3
  - Display entry ID: tcs_se
    Source Experience IDs: tcs_se
    Output title: Software Engineer
    Output company: Tata Consultancy Services
    Output location: Gandhinagar, India
    Output dates: Mar 2021 - Sep 2022
    Maximum bullets: 3
  Project selection:
    Required project count: 3
    Allowed Project IDs: {allowed_projects}
    Open-source project required: Yes
    Required bullets per project: 2
  Teaching Assistant rule: Do not include Teaching Assistant as an experience entry.

SKILLS
- Minimum skills: 8
- Maximum skills: 14

=== END RESUME CONFIGURATION ==="""


def split_skill_terms(value: Any) -> list[str]:
    def explode(text: str) -> list[str]:
        expanded = re.sub(r"([A-Za-z0-9+#. /-]+)\(([^)]*)\)", r"\1, \2", text)
        return re.split(r",|;", expanded)

    if isinstance(value, dict):
        raw_items: list[Any] = []
        for item in value.values():
            raw_items.extend(item if isinstance(item, list) else explode(str(item or "")))
    elif isinstance(value, list):
        raw_items = []
        for item in value:
            raw_items.extend(explode(str(item or "")))
    else:
        raw_items = explode(str(value or ""))
    terms: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        cleaned = re.sub(r"\s+", " ", str(item or "")).strip()
        key = cleaned.lower()
        if cleaned and key not in seen:
            terms.append(cleaned)
            seen.add(key)
    return terms


def compact_model_skills_to_technical_skills(skills: Any) -> list[list[Any]]:
    def rows_to_skill_array(rows: dict[str, str]) -> list[list[Any]]:
        return [[label, split_skill_terms(terms)] for label, terms in rows.items()]

    def parse_category_string(value: str) -> dict[str, str]:
        text = re.sub(r"\s+", " ", value or "").strip()
        matches = list(re.finditer(r"(?:^|,\s*)([^,:]{1,50}):\s*", text))
        if not matches:
            return {}
        rows: dict[str, str] = {}
        for index, match in enumerate(matches):
            if len(rows) >= 5:
                break
            label = re.sub(r"\s+", " ", match.group(1)).strip()
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            terms = text[start:end].strip(" ,")
            add_category(rows, label, terms)
        return rows

    def clean_skill_terms(value: Any) -> list[str]:
        if isinstance(value, list):
            raw_terms: list[Any] = []
            for item in value:
                if isinstance(item, (list, tuple)):
                    raw_terms.extend(item)
                else:
                    raw_terms.append(item)
        else:
            raw_terms = split_skill_terms(value)
        terms: list[str] = []
        seen: set[str] = set()
        for item in raw_terms:
            cleaned = re.sub(r"\s+", " ", str(item or "")).strip()
            key = cleaned.lower()
            if cleaned and key not in seen:
                terms.append(cleaned)
                seen.add(key)
        return terms

    def add_category(rows: dict[str, str], label: Any, value: Any) -> None:
        if len(rows) >= 5:
            return
        category = re.sub(r"\s+", " ", str(label or "")).strip()
        if not category or category.lower() in {"skills", "technical skills"}:
            category = "Skills"
        terms = clean_skill_terms(value)[:6]
        if terms:
            rows[category] = ", ".join(terms)

    if isinstance(skills, str):
        rows = parse_category_string(skills)
        if rows:
            return rows_to_skill_array(rows)

    if isinstance(skills, dict):
        rows: dict[str, str] = {}
        for index in range(1, 6):
            label = skills.get(f"row{index}_label")
            terms = skills.get(f"row{index}_terms")
            if label or terms:
                add_category(rows, label, terms)
        if rows:
            return rows_to_skill_array(rows)

        for label, terms in skills.items():
            add_category(rows, label, terms)
        if rows:
            return rows_to_skill_array(rows)

    if isinstance(skills, list) and any(isinstance(item, dict) for item in skills):
        rows = {}
        for item in skills:
            if not isinstance(item, dict):
                continue
            label = item.get("category") or item.get("label") or item.get("name") or item.get("title")
            terms = item.get("skills") or item.get("terms") or item.get("items")
            add_category(rows, label, terms)
        if rows:
            return rows_to_skill_array(rows)

    if isinstance(skills, list) and any(isinstance(item, (list, tuple)) for item in skills):
        rows = {}
        for item in skills:
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue
            add_category(rows, item[0], item[1])
        if rows:
            return rows_to_skill_array(rows)

    if isinstance(skills, list):
        terms = clean_skill_terms(skills)
    else:
        terms = split_skill_terms(skills)
    return [["Skills", terms[:6]]] if terms else []


def compact_experience_lock(role_id: str, company: str, title: str) -> dict[str, Any] | None:
    return candidate_experience_profile(role_id, company, title)


def compact_project_url(name: str) -> str:
    lower = name.lower()
    normalized = re.sub(r"[^a-z0-9]+", "", lower)
    for key, url in PROJECT_URLS.items():
        normalized_key = re.sub(r"[^a-z0-9]+", "", key.lower())
        if key in lower or (normalized_key and normalized_key in normalized):
            return url
    return ""


def header_location(inp: ResumeInput) -> str:
    target = str(inp.words or "").strip()
    if target and target.lower() != CURRENT_LOCATION.lower():
        return f"{CURRENT_LOCATION} | Moving to {target}"
    return CURRENT_LOCATION


def compact_to_resume_json(compact: dict[str, Any], inp: ResumeInput, prompt_profile: str = "v3") -> dict[str, Any]:
    profile = normalize_prompt_profile(prompt_profile)
    type_value = compact.get("type") or compact.get("Type")
    v1_mode = str(type_value or "").strip().lower() if profile == "v1" else ""
    summary_text = str(compact.get("summary") or compact.get("Summary") or "").strip()
    raw_order_value = compact.get("experience_order") or compact.get("Experience_Order")
    provided_section_order = normalize_section_order_value(compact.get("section_order") or compact.get("Section_Order"))
    provided_experience_order = normalize_experience_order_value(raw_order_value)
    if v1_mode in {"entry_swe", "entry_aiml", "mid_swe"}:
        strategy_type = "Mid" if v1_mode == "mid_swe" else "Entry"
        requested_order = provided_experience_order or [
            str(item.get("id") or "").strip()
            for item in compact.get("experience") or []
            if isinstance(item, dict) and str(item.get("id") or "").strip()
        ]
        section_order = provided_section_order or canonical_strategy_section_order(strategy_type)
        level, layout_profile = {
            "entry_swe": (2, "professional_entry"),
            "entry_aiml": (2, "aiml_entry"),
            "mid_swe": (3, "mid"),
        }[v1_mode]
    else:
        strategy_type = strategy_from_order(provided_experience_order, type_value)
        section_order = provided_section_order or canonical_strategy_section_order(strategy_type)
        requested_order = provided_experience_order or canonical_strategy_experience_order(strategy_type)
        level_value = compact.get("level") or compact.get("Level") or strategy_type
        level, layout_profile = compact_strategy_level(strategy_type) if str(type_value or "").strip().lower().replace("-", "").replace(" ", "") in {"newgrad", "entry", "mid"} and not (compact.get("level") or compact.get("Level")) else compact_level_config(level_value)
    jobs: list[dict[str, Any]] = []
    source_experience = (
        compact.get("experience")
        or compact.get("Experience")
        or compact.get("professional_experience")
        or compact.get("Professional_Experience")
        or []
    )
    for item in source_experience:
        if not isinstance(item, dict):
            continue
        role_id = str(
            item.get("id")
            or item.get("ID")
            or item.get("role_id")
            or item.get("story_id")
            or ""
        ).strip()
        title = str(item.get("title") or item.get("Title") or "").strip()
        company = str(item.get("company") or item.get("Company") or "").strip()
        lock = compact_experience_lock(role_id, company, title)
        if lock:
            title = str(lock["title"])
            company = str(lock["company"])
            location = str(lock["location"])
            dates = str(lock["dates"])
            employment_note = str(lock.get("employment_note") or "")
        else:
            location = str(item.get("location") or item.get("Location") or "").strip()
            dates = str(item.get("dates") or item.get("Dates") or "").strip()
            employment_note = str(item.get("employment_note") or "").strip()
        jobs.append({
            "id": role_id,
            "title": title,
            "company": company,
            "location": location,
            "dates": dates,
            "bullets": [str(b).strip() for b in (item.get("bullets") or item.get("Bullets") or []) if str(b).strip()],
            "employment_note": employment_note,
        })

    if requested_order:
        rank = experience_order_rank(requested_order)
        jobs.sort(key=lambda job: rank.get(experience_identity(job), len(rank)))

    projects: list[dict[str, Any]] = []
    for item in compact.get("projects") or compact.get("Projects") or []:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("Name") or item.get("title") or item.get("Title") or "").strip()
        projects.append({
            "story_id": str(item.get("story_id") or "").strip(),
            "title": name,
            "name": name,
            "tech": item.get("tech") or [],
            "location": "",
            "dates": "",
            "github_url": compact_project_url(name),
            "bullets": [str(b).strip() for b in (item.get("bullets") or item.get("Bullets") or []) if str(b).strip()],
        })

    config = {
        "type": (
            "aiml"
            if v1_mode == "entry_aiml"
            else compact_config_type(compact.get("role_type") or compact.get("Role_Type") or compact.get("role_family") or compact.get("Role_Family"))
        ),
        "level": level,
        "layout_profile": layout_profile,
        "output": "",
        "bold_markers": False,
        "ta_active": False,
        "company": inp.company,
        "role": inp.title or "Software Engineer",
        "prompt_profile": profile,
        "strategy_type": strategy_type,
    }
    if section_order:
        config["section_order"] = section_order
    raw_experience_order = str(raw_order_value or "").strip().lower()
    normalized_order = raw_experience_order.replace("-", "_").replace(" ", "_")
    if requested_order:
        config["experience_order"] = "json_order"
    elif normalized_order in {"tcs", "tcs_first", "ghi", "ghi_first", "json", "json_order"}:
        config["experience_order"] = {"tcs": "tcs_first", "ghi": "ghi_first", "json": "json_order"}.get(normalized_order, normalized_order)
    elif profile == "v3":
        config["experience_order"] = "json_order"

    education = candidate_education_profile()
    if v1_mode in {"entry_swe", "entry_aiml"}:
        education[0]["gpa"] = VERIFIED_GRADUATE_GPA
        allowed_coursework = {
            course.casefold(): course for course in VERIFIED_GRADUATE_COURSEWORK
        }
        selected_coursework: list[str] = []
        raw_coursework = compact.get("coursework") or []
        if isinstance(raw_coursework, list):
            for item in raw_coursework:
                canonical = allowed_coursework.get(str(item).strip().casefold())
                if canonical and canonical not in selected_coursework:
                    selected_coursework.append(canonical)
                if len(selected_coursework) == 4:
                    break
        if selected_coursework:
            education[0]["coursework"] = selected_coursework

    resume_header_location = header_location(inp)
    return normalize_resume_json({
        "type": strategy_type,
        "section_order": section_order,
        "experience_order": requested_order,
        "config": config,
        "name": CANDIDATE_NAME,
        "contact": (
            f"{resume_header_location} | {candidate_contact_line()}"
            if profile == "v1"
            else candidate_contact_line()
        ),
        "location": resume_header_location,
        "linkedin_url": LINKEDIN_URL,
        "github_url": GITHUB_URL,
        "summary": summary_text,
        "education": education,
        "professional_experience": jobs,
        "projects": projects,
        "technical_skills": compact_model_skills_to_technical_skills(
            compact.get("technical_skills")
            or compact.get("Technical_Skills")
            or compact.get("skills")
            or compact.get("Skills")
        ),
    })


def resume_json_to_compact(data: dict[str, Any]) -> dict[str, Any]:
    if all(key in data for key in ("type", "experience", "projects")) and (
        "technical_skills" in data or "skills" in data
    ):
        return data
    cfg = data.get("config") or {}
    jobs = [
        item
        for item in data.get("professional_experience") or data.get("experience") or []
        if isinstance(item, dict)
    ]
    order = normalize_experience_order_value(data.get("experience_order") or cfg.get("experience_order"))
    if not order:
        order = [experience_identity(item) for item in jobs]
    order = [item for item in order if item]
    strategy_type = str(data.get("type") or cfg.get("strategy_type") or "").strip() or strategy_from_order(
        order,
        "Mid" if int(cfg.get("level") or 2) == 3 else "Entry",
    )
    return {
        "type": strategy_type,
        "section_order": normalize_section_order_value(
            data.get("section_order") or cfg.get("section_order")
        ) or canonical_strategy_section_order(strategy_type),
        "experience_order": order,
        "summary": str(data.get("summary") or "").strip(),
        "experience": [
            {
                "id": experience_identity(item),
                "title": item.get("title", ""),
                "company": item.get("company", ""),
                "location": item.get("location", ""),
                "dates": item.get("dates", ""),
                "bullets": item.get("bullets") or [],
            }
            for item in jobs
        ],
        "projects": [
            {
                "name": item.get("name") or item.get("title") or "",
                "bullets": item.get("bullets") or [],
            }
            for item in data.get("projects") or []
            if isinstance(item, dict)
        ],
        "technical_skills": compact_model_skills_to_technical_skills(
            data.get("technical_skills") or data.get("skills") or {}
        ),
    }


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
    max_tokens: int | None = None,
    cost_cb=None,
    output_validator: Callable[[str], str | None] | None = None,
    retry_instruction: str = NVIDIA_RETRY_INSTRUCTION,
    cancel_event: threading.Event | None = None,
    provider_override: str | None = None,
    model_override: str | None = None,
    nvidia_thinking_override: bool | None = None,
    nvidia_reasoning_budget_override: int | None = None,
    rejected_response_cb: Callable[[int, str, str], None] | None = None,
    diagnostics: dict[str, Any] | None = None,
    guided_json_schema_override: dict[str, Any] | None = None,
    nvidia_validation_pass_override: bool | None = None,
    nvidia_max_attempts_override: int | None = None,
    provider_fallback_override: bool | None = None,
) -> str:
    provider = provider_override or get_provider()
    if provider == "nvidia":
        model = model_override or get_nvidia_model()
    else:
        model = get_model()
    resolved_max_tokens = max_tokens if max_tokens is not None else get_response_max_tokens()
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
    reasoning_tokens = 0
    provider_reasoning_parts: list[str] = []
    queue_wait_seconds = 0.0
    provider_response_seconds = 0.0
    attempts_used = 1
    finish_reason = ""
    last_error: Exception | None = None
    rejection_reason = ""
    cancel_after_accounting = False

    if diagnostics is not None:
        diagnostics.clear()
        diagnostics.update({
            "effective_provider": provider,
            "effective_model": model,
            "guided_json_enabled": False,
            "validation_enabled": False,
            "api_calls": 0,
            "retries": 0,
            "finish_reason": "",
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "reasoning_tokens": 0,
            "reasoning": "",
            "queue_wait_seconds": 0.0,
            "provider_response_seconds": 0.0,
            "total_response_time_seconds": 0.0,
            "schema_validation_result": "NOT_RUN",
            "nvidia_accounts": [],
        })

    if provider == "nvidia":
        nvidia_validation_pass = (
            get_nvidia_validation_pass()
            if nvidia_validation_pass_override is None
            else bool(nvidia_validation_pass_override)
        )
        guided_json_schema = (
            guided_json_schema_override
            if guided_json_schema_override is not None
            else guided_json_schema_for_validator(output_validator)
        )
        max_attempts = (
            max(1, int(nvidia_max_attempts_override))
            if nvidia_max_attempts_override is not None
            else get_nvidia_max_attempts()
        )
        if diagnostics is not None:
            diagnostics["guided_json_enabled"] = guided_json_schema is not None
            diagnostics["validation_enabled"] = bool(output_validator and nvidia_validation_pass)
        for attempt in range(1, max_attempts + 1):
            raise_if_cancelled(cancel_event)
            attempts_used = attempt
            if attempt > 1:
                if diagnostics is not None:
                    diagnostics["retries"] += 1
                await wait_before_retry(
                    nvidia_retry_delay_seconds(attempt - 1, last_error),
                    cancel_event,
                )
            attempt_messages = list(messages)
            if attempt > 1:
                detail = f"Rejection reason: {rejection_reason}" if rejection_reason else ""
                attempt_messages.append({
                    "role": "user",
                    "content": "\n\n".join(part for part in [retry_instruction.strip(), detail] if part),
                })
            try:
                if diagnostics is not None:
                    diagnostics["api_calls"] += 1
                    diagnostics["sanitized_request_payload"] = sanitize_nvidia_request_payload(
                        build_nvidia_request_payload(
                            system_blocks=system_blocks,
                            messages=attempt_messages,
                            model=model,
                            thinking=nvidia_thinking,
                            max_tokens=resolved_max_tokens,
                            guided_json_schema=guided_json_schema,
                            reasoning_budget_override=nvidia_reasoning_budget_override,
                        )
                    )
                response = await asyncio.to_thread(
                    call_nvidia_sync,
                    system_blocks=system_blocks,
                    messages=attempt_messages,
                    model=model,
                    thinking=nvidia_thinking,
                    max_tokens=resolved_max_tokens,
                    guided_json_schema=guided_json_schema,
                    reasoning_budget_override=nvidia_reasoning_budget_override,
                    cancel_event=cancel_event,
                )
            except OperationCancelled:
                raise
            except Exception as exc:
                if diagnostics is not None:
                    account_label = str(getattr(exc, "nvidia_account_label", "") or "")
                    if account_label:
                        diagnostics["nvidia_accounts"].append(account_label)
                    diagnostics["queue_wait_seconds"] = round(
                        float(getattr(exc, "nvidia_queue_wait_seconds", 0.0) or 0.0), 3
                    )
                    diagnostics["provider_response_seconds"] = round(
                        float(getattr(exc, "nvidia_provider_response_seconds", 0.0) or 0.0), 3
                    )
                    diagnostics["total_response_time_seconds"] = round(time.monotonic() - t0, 3)
                    diagnostics["provider_error"] = model_error_diagnostics(exc, diagnostics)
                if not is_retryable_nvidia_error(exc):
                    raise
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
            reasoning_tokens += response.usage.get("reasoning_tokens", 0)
            if response.reasoning:
                provider_reasoning_parts.append(response.reasoning)
            queue_wait_seconds += response.queue_wait_seconds
            provider_response_seconds += response.provider_response_seconds
            if diagnostics is not None and response.account_label:
                diagnostics["nvidia_accounts"].append(response.account_label)

            problems: list[str] = []
            if finish_reason.lower() in {"length", "max_tokens"}:
                problems.append(f"truncated response (finish_reason={finish_reason})")
            if output_validator:
                validator_error = output_validator(text)
                if validator_error:
                    problems.append(validator_error)
            if not problems and output_validator and nvidia_validation_pass:
                validation_messages = [
                    *messages,
                    {"role": "assistant", "content": text},
                    {
                        "role": "user",
                        "content": (
                            "VALIDATION PASS:\n"
                            "Independently verify the previous response against the original instructions and input. "
                            "Correct any omission, schema problem, unsupported addition, or formatting defect. "
                            "Return the complete final response only, with no validation commentary."
                        ),
                    },
                ]
                try:
                    if diagnostics is not None:
                        diagnostics["api_calls"] += 1
                    validated_response = await asyncio.to_thread(
                        call_nvidia_sync,
                        system_blocks=system_blocks,
                        messages=validation_messages,
                        model=model,
                        thinking=nvidia_thinking,
                        max_tokens=resolved_max_tokens,
                        seed_override=get_nvidia_validator_seed(),
                        guided_json_schema=guided_json_schema,
                        reasoning_budget_override=nvidia_reasoning_budget_override,
                        cancel_event=cancel_event,
                    )
                    input_tokens += validated_response.usage["input_tokens"]
                    output_tokens += validated_response.usage["output_tokens"]
                    cache_create += validated_response.usage["cache_creation_input_tokens"]
                    cache_read += validated_response.usage["cache_read_input_tokens"]
                    reasoning_tokens += validated_response.usage.get("reasoning_tokens", 0)
                    if validated_response.reasoning:
                        provider_reasoning_parts.append(validated_response.reasoning)
                    queue_wait_seconds += validated_response.queue_wait_seconds
                    provider_response_seconds += validated_response.provider_response_seconds
                    if diagnostics is not None and validated_response.account_label:
                        diagnostics["nvidia_accounts"].append(validated_response.account_label)
                    validation_error = output_validator(validated_response.text)
                    if validation_error:
                        problems.append(f"validation pass rejected: {validation_error}")
                    else:
                        text = validated_response.text
                        finish_reason = validated_response.finish_reason or finish_reason
                except OperationCancelled:
                    raise
                except Exception as exc:
                    problems.append(f"validation pass API error: {exc}")
            if not problems:
                rejection_reason = ""
                break
            rejection_reason = "; ".join(problems)
            if rejected_response_cb:
                rejected_response_cb(attempt, text, rejection_reason)
            log(
                f"{label}: NVIDIA attempt {attempt}/{max_attempts} rejected: "
                f"{rejection_reason}"
            )

        if rejection_reason or (last_error and not text):
            fallback_enabled = (
                bool(provider_fallback_override)
                if provider_fallback_override is not None
                else config_bool(load_config().get("fallback_to_anthropic"), False)
            )
            if fallback_enabled:
                log(f"{label}: NVIDIA attempts exhausted; falling back to direct Anthropic.")
                provider = "anthropic"
                model = get_model()
            elif not text:
                if diagnostics is not None:
                    diagnostics["total_response_time_seconds"] = round(time.monotonic() - t0, 3)
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
            max_tokens=resolved_max_tokens,
            system=system_blocks,
            messages=messages,
        )
        text_parts: list[str] = []
        for block in resp.content:
            block_type = str(getattr(block, "type", "") or "")
            if block_type == "thinking":
                thinking_text = str(getattr(block, "thinking", "") or "").strip()
                if thinking_text:
                    provider_reasoning_parts.append(thinking_text)
            else:
                block_text = str(getattr(block, "text", "") or "").strip()
                if block_text:
                    text_parts.append(block_text)
        text = "\n\n".join(text_parts).strip()
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
    if diagnostics is not None:
        final_validation_error = output_validator(text) if output_validator else None
        if finish_reason.lower() in {"length", "max_tokens"}:
            schema_validation_result = "TRUNCATED"
        elif output_validator:
            schema_validation_result = (
                "PASS" if not final_validation_error else f"FAIL: {final_validation_error}"
            )
        else:
            schema_validation_result = "NOT_RUN"
        diagnostics.update({
            "effective_provider": provider,
            "effective_model": model,
            "finish_reason": finish_reason or "unknown",
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "reasoning_tokens": reasoning_tokens,
            "reasoning": "\n\n".join(provider_reasoning_parts).strip(),
            "queue_wait_seconds": round(queue_wait_seconds, 3),
            "provider_response_seconds": round(provider_response_seconds, 3),
            "total_response_time_seconds": round(elapsed, 3),
            "schema_validation_result": schema_validation_result,
        })
    thinking_log = f" thinking={'on' if nvidia_thinking else 'off'}" if provider == "nvidia" else ""
    timing_log = (
        f" queue={queue_wait_seconds:.1f}s provider_time={provider_response_seconds:.1f}s"
        if provider == "nvidia"
        else ""
    )
    account_log = ""
    if provider == "nvidia" and diagnostics is not None:
        used_accounts = list(dict.fromkeys(diagnostics.get("nvidia_accounts", [])))
        if used_accounts:
            account_log = f" accounts={','.join(used_accounts)}"
    log(
        f"{label}: provider={provider} model={model}{thinking_log} "
        f"in={input_tokens} out={output_tokens} "
        f"cache_read={cache_read} cache_create={cache_create} "
        f"attempts={attempts_used} finish_reason={finish_reason or 'unknown'} "
        f"cost=${estimated_cost:.4f} elapsed={elapsed:.1f}s{timing_log}{account_log}"
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


def is_worker_local_total_request_limit_error(exc: Exception) -> bool:
    """Match only the worker-local request-limit failure, including wrapped errors."""
    pending: list[BaseException] = [exc]
    seen: set[int] = set()
    while pending:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        if WORKER_LOCAL_TOTAL_REQUEST_LIMIT_ERROR in str(current):
            return True
        response = getattr(current, "response", None)
        if response is not None:
            try:
                if WORKER_LOCAL_TOTAL_REQUEST_LIMIT_ERROR in str(
                    getattr(response, "text", "") or ""
                ):
                    return True
            except Exception:
                pass
        for nested in (current.__cause__, current.__context__):
            if nested is not None:
                pending.append(nested)
    return False


async def call_v1_stage_model(
    *,
    cancel_event: threading.Event | None = None,
    **call_kwargs: Any,
) -> str:
    """Restart the active V1 stage immediately for the worker-local limit only."""
    while True:
        raise_if_cancelled(cancel_event)
        try:
            return await call_model(cancel_event=cancel_event, **call_kwargs)
        except OperationCancelled:
            raise
        except Exception as exc:
            if not is_worker_local_total_request_limit_error(exc):
                raise
            log(
                f"{call_kwargs.get('label', 'V1 stage')}: "
                "worker-local total request limit reached; restarting stage immediately."
            )


def pass1_system(prompt_profile: str | None = None) -> list[dict[str, Any]]:
    if is_experimental_prompt_profile(prompt_profile):
        return [
            cached_text_block(read_prompt("prompt.md", prompt_profile)),
            cached_text_block(read_prompt("Story.md", prompt_profile)),
        ]
    return [
        cached_text_block(read_prompt("prompt.md", prompt_profile)),
        cached_text_block(read_prompt("story.md", prompt_profile)),
    ]


def pass2_system(prompt_profile: str | None = None) -> list[dict[str, Any]]:
    return pass1_system(prompt_profile)


def recruiter_system(prompt_profile: str | None = None) -> list[dict[str, Any]]:
    profile = normalize_prompt_profile(prompt_profile)
    if profile == "v3":
        return [
            cached_text_block(read_prompt("prompt.md", profile)),
            cached_text_block(read_prompt("Story.md", profile)),
            cached_text_block(read_prompt("hotdog.md", profile)),
        ]
    return [cached_text_block(read_prompt("recruiter.md", prompt_profile))]


def v1_reasoning_text(diagnostics: dict[str, Any]) -> str:
    reasoning = str(diagnostics.get("reasoning") or "").strip()
    return reasoning or "Reasoning was not returned by the selected model."


def v1_api_error_data(exc: Exception, diagnostics: dict[str, Any]) -> dict[str, Any]:
    provider_error = diagnostics.get("provider_error")
    if isinstance(provider_error, dict):
        result = dict(provider_error)
        result["message"] = str(exc)
        return result
    return model_error_diagnostics(exc, diagnostics)


def v1_api_error_reasoning(diagnostics: dict[str, Any], fallback: str) -> str:
    provider_error = diagnostics.get("provider_error")
    if isinstance(provider_error, dict):
        partial = str(provider_error.get("partial_reasoning") or "").strip()
        if partial:
            return partial
    return fallback


def v1_common_input(inp: ResumeInput) -> list[str]:
    return [
        f"CURRENT COMPANY\n{inp.company.strip()}",
        f"CURRENT JOB TITLE\n{(inp.title or 'Software Engineer').strip()}",
        f"CURRENT JOB LOCATION\n{inp.words.strip() or 'Not provided.'}",
        f"USER MODE OVERRIDE\n{inp.mode.strip() or 'Not provided.'}",
        f"CURRENT INITIAL DES, IF PROVIDED\n{inp.des.strip() or 'Not provided.'}",
        f"CURRENT JOB DESCRIPTION\n{inp.jd.strip()}",
    ]


def v1_composer_input(inp: ResumeInput) -> list[str]:
    return [
        f"CURRENT COMPANY\n{inp.company.strip()}",
        f"CURRENT JOB TITLE\n{(inp.title or 'Software Engineer').strip()}",
        f"CURRENT JOB LOCATION\n{inp.words.strip() or 'Not provided.'}",
    ]


V1_POST_MODE_CONFIG: dict[str, dict[str, Any]] = {
    "entry_swe": {
        "roles": [("TA", 2), ("GHI", 3), ("TCS_SWE_II", 3), ("TCS_SWE_I", 2)],
        "projects": 2,
        "summary_max_words": 0,
    },
    "entry_aiml": {
        "roles": [("TA", 2), ("GHI", 3), ("TCS_COMBINED", 3)],
        "projects": 3,
        "summary_max_words": 0,
    },
    "mid_swe": {
        "roles": [("TCS_SWE_II", 4), ("TCS_SWE_I", 2), ("TA", 1), ("GHI", 2)],
        "projects": 2,
        "summary_max_words": 40,
    },
}

V1_LOCKED_EXPERIENCE_IDENTITY: dict[str, dict[str, str]] = {
    "TA": {
        "title": "Teaching Assistant",
        "company": "Binghamton University",
        "location": "Binghamton, NY",
        "dates": "Aug 2025 - Present",
    },
    "GHI": {
        "title": "Software Engineering Intern",
        "company": "Global Health Impact",
        "location": "New York, NY",
        "dates": "May 2025 - Jun 2025",
    },
    "TCS_SWE_II": {
        "title": "Software Engineer II",
        "company": "Tata Consultancy Services",
        "location": "Gandhinagar, India",
        "dates": "Oct 2022 - Dec 2024",
    },
    "TCS_SWE_I": {
        "title": "Software Engineer I",
        "company": "Tata Consultancy Services",
        "location": "Gandhinagar, India",
        "dates": "Mar 2021 - Sep 2022",
    },
    "TCS_COMBINED": {
        "title": "Software Engineer II",
        "company": "Tata Consultancy Services",
        "location": "Gandhinagar, India",
        "dates": "Mar 2021 - Dec 2024",
    },
}

V1_TOP_LEVEL_KEYS = [
    "type",
    "summary",
    "coursework",
    "experience",
    "projects",
    "technical_skills",
    "bullet_checks",
]
V1_EXPERIENCE_KEYS = ["id", "title", "company", "location", "dates", "bullets"]
V1_PROJECT_KEYS = ["story_id", "name", "tech", "bullets"]
V1_SKILLS_KEYS = ["category", "skills"]
V1_BULLET_CHECK_KEYS = [
    "ref",
    "story_id",
    "requirement_id",
    "alignment",
    "word_count",
    "questions_answered",
]
V1_QUESTION_LABELS = ["what", "how", "with_what", "result", "amount"]


def read_v1_post_stage_prompt(name: str) -> str:
    path = V1_POST_STAGE_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing V1 post-composition prompt: {path}")
    return path.read_text(encoding="utf-8")


def v1_post_short_controller(run_mode: str) -> str:
    prompt_files = {
        "POST_V1_ATS_AUDIT": "prompt_short_ats.md",
        "POST_V1_OPTIMIZATION": "prompt_short_optimizer.md",
    }
    try:
        prompt_file = prompt_files[run_mode]
    except KeyError as exc:
        raise ValueError(f"Unsupported V1 post-composition run mode: {run_mode}") from exc
    return f"RUN MODE: {run_mode}\n\n{read_v1_post_stage_prompt(prompt_file)}"


def v1_bullet_word_count(text: str) -> int:
    return len(str(text or "").split())


def extract_exact_json_object(text: str) -> dict[str, Any]:
    """Extract one model JSON object without applying renderer normalization."""

    stripped = str(text or "").strip()
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, dict):
        return parsed

    decoder = json.JSONDecoder()
    candidates: list[dict[str, Any]] = []
    for match in re.finditer(r"\{", stripped):
        try:
            candidate, _end = decoder.raw_decode(stripped[match.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            candidates.append(candidate)
    if candidates:
        return candidates[-1]
    raise ValueError("Could not extract one valid JSON object from model output.")


def normalized_des_ids(approval_text: str) -> set[str]:
    return {
        f"DES{int(number):03d}"
        for number in re.findall(r"\bDES\s*-?\s*0*(\d+)\b", approval_text or "", re.IGNORECASE)
    }


def _exact_key_errors(value: Any, expected: list[str], path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object."]
    actual = list(value.keys())
    if actual == expected:
        return []
    return [f"{path} keys must be exactly {expected}; received {actual}."]


def _slot_des_terms(
    mapper_plan: dict[str, Any],
    approval_text: str,
) -> dict[tuple[str, int], set[str]]:
    approved = normalized_des_ids(approval_text)
    result: dict[tuple[str, int], set[str]] = {}
    for item in mapper_plan.get("des_questions") or []:
        if not isinstance(item, dict) or str(item.get("id") or "").upper() not in approved:
            continue
        placement = item.get("if_approved") or {}
        if not isinstance(placement, dict) or placement.get("placement_section") != "experience":
            continue
        role_id = str(placement.get("role_id") or "")
        try:
            slot = int(placement.get("slot"))
        except (TypeError, ValueError):
            continue
        term = str(placement.get("selected_term") or item.get("exact_jd_term") or "").strip()
        if role_id and slot > 0 and term:
            result.setdefault((role_id, slot), set()).add(term)
    return result


def _numeric_tokens(text: str) -> set[str]:
    return {
        token.rstrip(".,")
        for token in re.findall(r"\d[\d,.]*(?:\+|%|ms|MB|GB|TB|s)?", str(text or ""), re.IGNORECASE)
    }


def validate_v1_optimized_resume(
    current_resume: dict[str, Any],
    optimized_resume: dict[str, Any],
    mapper_plan: dict[str, Any],
    approval_text: str,
) -> list[str]:
    """Return exact structural and evidence-boundary errors for a post-V1 result."""

    errors = _exact_key_errors(optimized_resume, V1_TOP_LEVEL_KEYS, "resume")
    if not isinstance(optimized_resume, dict):
        return errors

    mode = str(mapper_plan.get("resolved_mode") or "").strip()
    config = V1_POST_MODE_CONFIG.get(mode)
    if not config:
        errors.append(f"Unsupported or missing mapper resolved_mode: {mode or '<empty>'}.")
        return errors
    if optimized_resume.get("type") != mode:
        errors.append(f"resume.type must equal mapper resolved_mode {mode!r}.")

    summary = optimized_resume.get("summary")
    if not isinstance(summary, str):
        errors.append("resume.summary must be a string.")
    elif config["summary_max_words"] == 0 and summary != "":
        errors.append(f"{mode} summary must be an empty string.")
    elif config["summary_max_words"] and v1_bullet_word_count(summary) > config["summary_max_words"]:
        errors.append(f"{mode} summary exceeds {config['summary_max_words']} words.")

    mapper_roles = {
        str(role.get("role_id") or ""): role
        for role in mapper_plan.get("experience_plan") or []
        if isinstance(role, dict)
    }
    experiences = optimized_resume.get("experience")
    if not isinstance(experiences, list):
        errors.append("resume.experience must be an array.")
        experiences = []
    expected_roles: list[tuple[str, int]] = config["roles"]
    if len(experiences) != len(expected_roles):
        errors.append(f"resume.experience must contain {len(expected_roles)} roles; received {len(experiences)}.")

    slot_ledger: list[dict[str, Any]] = []
    opening_verbs: dict[str, str] = {}
    slot_des_terms = _slot_des_terms(mapper_plan, approval_text)

    for index, (role_id, expected_bullets) in enumerate(expected_roles):
        if index >= len(experiences):
            continue
        experience = experiences[index]
        path = f"experience[{index}]"
        errors.extend(_exact_key_errors(experience, V1_EXPERIENCE_KEYS, path))
        if not isinstance(experience, dict):
            continue
        if experience.get("id") != role_id:
            errors.append(f"{path}.id must be {role_id!r}.")
        identity = V1_LOCKED_EXPERIENCE_IDENTITY[role_id]
        for key, expected in identity.items():
            if experience.get(key) != expected:
                errors.append(f"{path}.{key} must remain {expected!r}.")
        bullets = experience.get("bullets")
        if not isinstance(bullets, list):
            errors.append(f"{path}.bullets must be an array.")
            bullets = []
        if len(bullets) != expected_bullets:
            errors.append(f"{path}.bullets must contain {expected_bullets} bullets; received {len(bullets)}.")
        mapper_slots = {
            int(slot.get("slot")): slot
            for slot in (mapper_roles.get(role_id, {}).get("bullets") or [])
            if isinstance(slot, dict) and str(slot.get("slot") or "").isdigit()
        }
        for bullet_index, bullet in enumerate(bullets, start=1):
            bullet_path = f"{path}.bullets[{bullet_index - 1}]"
            if not isinstance(bullet, str) or not bullet.strip():
                errors.append(f"{bullet_path} must be a nonempty string.")
                continue
            words = v1_bullet_word_count(bullet)
            if words > 24:
                errors.append(f"{bullet_path} has {words} words; maximum is 24.")
            if "\u2013" in bullet or "\u2014" in bullet:
                errors.append(f"{bullet_path} contains an em dash or en dash.")
            verb = bullet.split()[0].strip(".,:;()[]{}").lower()
            if verb in opening_verbs:
                errors.append(f"{bullet_path} repeats opening verb {verb!r} used by {opening_verbs[verb]}.")
            else:
                opening_verbs[verb] = bullet_path
            mapper_slot = mapper_slots.get(bullet_index, {})
            if not mapper_slot:
                errors.append(f"Mapper slot missing for {role_id}.{bullet_index}.")
            allowed_text = " ".join(
                str(value)
                for key in ("allowed_fact_fragments", "allowed_metrics", "allowed_technology_terms")
                for value in (mapper_slot.get(key) or [])
            )
            allowed_text += " " + " ".join(slot_des_terms.get((role_id, bullet_index), set()))
            for token in _numeric_tokens(bullet):
                if token not in _numeric_tokens(allowed_text):
                    errors.append(f"{bullet_path} uses numeric token {token!r} outside its mapper slot allowlist.")
            slot_ledger.append({
                "ref": f"{role_id}.{bullet_index}",
                "story_id": str(mapper_slot.get("story_id") or ""),
                "primary_requirement_ids": [
                    str(item) for item in (mapper_slot.get("primary_requirement_ids") or [])
                ],
                "bullet": bullet,
            })

    mapper_projects = [
        item for item in mapper_plan.get("project_plan") or [] if isinstance(item, dict)
    ]
    projects = optimized_resume.get("projects")
    if not isinstance(projects, list):
        errors.append("resume.projects must be an array.")
        projects = []
    expected_project_count = int(config["projects"])
    if len(projects) != expected_project_count:
        errors.append(f"resume.projects must contain {expected_project_count} projects; received {len(projects)}.")
    if len(mapper_projects) != expected_project_count:
        errors.append(
            f"mapper project_plan must contain {expected_project_count} projects; received {len(mapper_projects)}."
        )
    for index in range(min(len(projects), len(mapper_projects), expected_project_count)):
        project = projects[index]
        mapper_project = mapper_projects[index]
        path = f"projects[{index}]"
        errors.extend(_exact_key_errors(project, V1_PROJECT_KEYS, path))
        if not isinstance(project, dict):
            continue
        story_id = str(mapper_project.get("story_id") or "")
        if project.get("story_id") != story_id:
            errors.append(f"{path}.story_id must be {story_id!r}.")
        expected_name = str(mapper_project.get("name") or "")
        if project.get("name") != expected_name:
            errors.append(f"{path}.name must remain {expected_name!r}.")
        allowed_tech = {str(item) for item in (mapper_project.get("allowed_technology_terms") or [])}
        tech = project.get("tech")
        if not isinstance(tech, list) or any(not isinstance(item, str) for item in tech):
            errors.append(f"{path}.tech must be an array of strings.")
        else:
            unsupported = [item for item in tech if item not in allowed_tech]
            if unsupported:
                errors.append(f"{path}.tech contains mapper-unauthorized terms: {unsupported}.")
            if len(tech) != len(set(tech)):
                errors.append(f"{path}.tech contains duplicate terms.")
        bullets = project.get("bullets")
        if not isinstance(bullets, list):
            errors.append(f"{path}.bullets must be an array.")
            bullets = []
        if len(bullets) != 2:
            errors.append(f"{path}.bullets must contain exactly 2 bullets; received {len(bullets)}.")
        mapper_slots = {
            int(slot.get("slot")): slot
            for slot in (mapper_project.get("bullets") or [])
            if isinstance(slot, dict) and str(slot.get("slot") or "").isdigit()
        }
        for bullet_index, bullet in enumerate(bullets, start=1):
            bullet_path = f"{path}.bullets[{bullet_index - 1}]"
            if not isinstance(bullet, str) or not bullet.strip():
                errors.append(f"{bullet_path} must be a nonempty string.")
                continue
            words = v1_bullet_word_count(bullet)
            if words > 24:
                errors.append(f"{bullet_path} has {words} words; maximum is 24.")
            if "\u2013" in bullet or "\u2014" in bullet:
                errors.append(f"{bullet_path} contains an em dash or en dash.")
            verb = bullet.split()[0].strip(".,:;()[]{}").lower()
            if verb in opening_verbs:
                errors.append(f"{bullet_path} repeats opening verb {verb!r} used by {opening_verbs[verb]}.")
            else:
                opening_verbs[verb] = bullet_path
            mapper_slot = mapper_slots.get(bullet_index, {})
            if not mapper_slot:
                errors.append(f"Mapper slot missing for {story_id}.{bullet_index}.")
            allowed_text = " ".join(
                str(value)
                for key in ("allowed_fact_fragments", "allowed_metrics")
                for value in (mapper_slot.get(key) or [])
            )
            for token in _numeric_tokens(bullet):
                if token not in _numeric_tokens(allowed_text):
                    errors.append(f"{bullet_path} uses numeric token {token!r} outside its mapper slot allowlist.")
            slot_ledger.append({
                "ref": f"{story_id}.{bullet_index}",
                "story_id": story_id,
                "primary_requirement_ids": [
                    str(item) for item in (mapper_slot.get("primary_requirement_ids") or [])
                ],
                "bullet": bullet,
            })

    approved_des = normalized_des_ids(approval_text)
    allowed_skills: dict[str, set[str]] = {}
    for category in mapper_plan.get("skills_plan") or []:
        if not isinstance(category, dict):
            continue
        category_name = str(category.get("category") or "")
        allowed_terms: set[str] = set()
        for item in category.get("terms") or []:
            if not isinstance(item, dict):
                continue
            dependencies = {str(value).upper() for value in (item.get("approved_des_ids") or [])}
            if dependencies and not dependencies.issubset(approved_des):
                continue
            term = str(item.get("term") or "").strip()
            if term:
                allowed_terms.add(term)
        allowed_skills[category_name] = allowed_terms
    technical_skills = optimized_resume.get("technical_skills")
    if not isinstance(technical_skills, list):
        errors.append("resume.technical_skills must be an array.")
        technical_skills = []
    if len(technical_skills) > 5:
        errors.append("resume.technical_skills may contain at most 5 categories.")
    seen_categories: set[str] = set()
    seen_terms: set[str] = set()
    for index, category in enumerate(technical_skills):
        path = f"technical_skills[{index}]"
        errors.extend(_exact_key_errors(category, V1_SKILLS_KEYS, path))
        if not isinstance(category, dict):
            continue
        category_name = category.get("category")
        if not isinstance(category_name, str) or category_name not in allowed_skills:
            errors.append(f"{path}.category is not present in mapper skills_plan: {category_name!r}.")
            continue
        if category_name in seen_categories:
            errors.append(f"{path}.category duplicates {category_name!r}.")
        seen_categories.add(category_name)
        skills = category.get("skills")
        if not isinstance(skills, list) or not skills or any(not isinstance(item, str) for item in skills):
            errors.append(f"{path}.skills must be a nonempty array of strings.")
            continue
        for skill in skills:
            if skill not in allowed_skills[category_name]:
                errors.append(f"{path}.skills contains mapper-unauthorized term {skill!r}.")
            if skill in seen_terms:
                errors.append(f"Technical skill {skill!r} is duplicated.")
            seen_terms.add(skill)

    checks = optimized_resume.get("bullet_checks")
    if not isinstance(checks, list):
        errors.append("resume.bullet_checks must be an array.")
        checks = []
    if len(checks) != len(slot_ledger):
        errors.append(f"resume.bullet_checks must contain {len(slot_ledger)} entries; received {len(checks)}.")
    question_rank = {label: index for index, label in enumerate(V1_QUESTION_LABELS)}
    for index in range(min(len(checks), len(slot_ledger))):
        check = checks[index]
        expected = slot_ledger[index]
        path = f"bullet_checks[{index}]"
        errors.extend(_exact_key_errors(check, V1_BULLET_CHECK_KEYS, path))
        if not isinstance(check, dict):
            continue
        if check.get("ref") != expected["ref"]:
            errors.append(f"{path}.ref must be {expected['ref']!r}.")
        if check.get("story_id") != expected["story_id"]:
            errors.append(f"{path}.story_id must be {expected['story_id']!r}.")
        allowed_requirements = expected["primary_requirement_ids"] or [""]
        if check.get("requirement_id") not in allowed_requirements:
            errors.append(f"{path}.requirement_id must be one of {allowed_requirements}.")
        if check.get("alignment") not in {"direct", "close", "context"}:
            errors.append(f"{path}.alignment must be direct, close, or context.")
        actual_words = v1_bullet_word_count(expected["bullet"])
        if check.get("word_count") != actual_words:
            errors.append(f"{path}.word_count must be {actual_words}.")
        questions = check.get("questions_answered")
        if not isinstance(questions, list) or any(item not in question_rank for item in questions):
            errors.append(f"{path}.questions_answered contains an invalid label.")
        elif len(questions) != len(set(questions)) or questions != sorted(questions, key=question_rank.get):
            errors.append(f"{path}.questions_answered must be unique and in logical order.")

    if isinstance(current_resume, dict):
        current_mode = str(current_resume.get("type") or "")
        if current_mode and current_mode != mode:
            errors.append(f"Current composer mode {current_mode!r} conflicts with mapper mode {mode!r}.")
    return errors


async def run_v1_post_validation(
    inp: ResumeInput,
    jd_analysis: dict[str, Any],
    mapper_plan: dict[str, Any],
    approval_text: str,
    current_resume: dict[str, Any],
    *,
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
    stage_artifact_cb: Callable[[str, Any, str], None] | None = None,
) -> V1PostValidationResult:
    story_library = read_prompt("story.md", "v1")
    ats_input = "\n\n".join([
        v1_post_short_controller("POST_V1_ATS_AUDIT"),
        f"CURRENT_DATE\n{datetime.now().astimezone().date().isoformat()}",
        f"JOB_DESCRIPTION\n{inp.jd.strip()}",
        "JD_ANALYSIS_JSON\n" + compact_json(jd_analysis),
        "MAPPER_PLAN_JSON\n" + compact_json(mapper_plan),
        f"OPTIONAL_STORY_LIBRARY\n{story_library}",
        f"DES_APPROVAL\n{approval_text.strip() or 'No DES'}",
        "V1_RESUME_JSON\n" + compact_json(current_resume),
        "OPTIONAL_MARKET_CONTEXT\nNot supplied. Use the JD and V1 artifacts only.",
    ])
    ats_diagnostics: dict[str, Any] = {}
    try:
        ats_report = await call_v1_stage_model(
            system_blocks=[cached_text_block(read_v1_post_stage_prompt("ATS.md"))],
            messages=[{"role": "user", "content": ats_input}],
            label=labeled_step(request_label, "V1 ATS GAP AUDIT"),
            cost_cb=cost_cb,
            output_validator=None,
            retry_instruction="",
            cancel_event=cancel_event,
            model_override=nvidia_model,
            nvidia_thinking_override=nvidia_thinking,
            diagnostics=ats_diagnostics,
            nvidia_validation_pass_override=False,
            nvidia_max_attempts_override=1,
            provider_fallback_override=False,
        )
    except Exception as exc:
        if stage_artifact_cb:
            stage_artifact_cb(
                "ats_audit_api_error",
                v1_api_error_data(exc, ats_diagnostics),
                v1_api_error_reasoning(
                    ats_diagnostics,
                    "Provider request failed before ATS audit reasoning was returned.",
                ),
            )
        raise
    if stage_artifact_cb:
        stage_artifact_cb("ats_audit", ats_report, v1_reasoning_text(ats_diagnostics))

    optimizer_input = "\n\n".join([
        v1_post_short_controller("POST_V1_OPTIMIZATION"),
        f"JOB_DESCRIPTION\n{inp.jd.strip()}",
        "JD_ANALYSIS_JSON\n" + compact_json(jd_analysis),
        "MAPPER_PLAN_JSON\n" + compact_json(mapper_plan),
        f"DES_APPROVAL\n{approval_text.strip() or 'No DES'}",
        "CURRENT_V1_RESUME_JSON\n" + compact_json(current_resume),
        f"ATS_GAP_REPORT\n{ats_report.strip()}",
    ])
    optimizer_diagnostics: dict[str, Any] = {}
    try:
        optimizer_raw = await call_v1_stage_model(
            system_blocks=[cached_text_block(read_v1_post_stage_prompt("optimizer.md"))],
            messages=[{"role": "user", "content": optimizer_input}],
            label=labeled_step(request_label, "V1 EVIDENCE-LOCKED OPTIMIZER"),
            cost_cb=cost_cb,
            output_validator=None,
            retry_instruction="",
            cancel_event=cancel_event,
            model_override=nvidia_model,
            nvidia_thinking_override=nvidia_thinking,
            diagnostics=optimizer_diagnostics,
            nvidia_validation_pass_override=False,
            nvidia_max_attempts_override=1,
            provider_fallback_override=False,
        )
    except Exception as exc:
        if stage_artifact_cb:
            stage_artifact_cb(
                "optimizer_api_error",
                v1_api_error_data(exc, optimizer_diagnostics),
                v1_api_error_reasoning(
                    optimizer_diagnostics,
                    "Provider request failed before optimizer reasoning was returned.",
                ),
            )
        raise
    try:
        optimized_resume = extract_exact_json_object(optimizer_raw)
    except Exception:
        if stage_artifact_cb:
            stage_artifact_cb(
                "optimizer_parse_error",
                {"raw": optimizer_raw},
                v1_reasoning_text(optimizer_diagnostics),
            )
        raise
    if stage_artifact_cb:
        stage_artifact_cb("optimizer", optimized_resume, v1_reasoning_text(optimizer_diagnostics))

    return V1PostValidationResult(
        ats_report=ats_report,
        optimized_resume=optimized_resume,
    )


def v1_short_controller(run_mode: str) -> str:
    prompt_files = {
        "JD_INTELLIGENCE": "prompt_short_jd.md",
        "EVIDENCE_MAPPING": "prompt_short_mapper.md",
        "RESUME_COMPOSITION": "prompt_short_composer.md",
    }
    try:
        prompt_file = prompt_files[run_mode]
    except KeyError as exc:
        raise ValueError(f"Unsupported V1 run mode: {run_mode}") from exc
    return f"RUN MODE: {run_mode}\n\n{read_prompt(prompt_file, 'v1')}"


def v1_pass1_bundle(text: str) -> tuple[dict[str, Any], dict[str, Any]]:
    data = extract_json(text)
    analysis = data.get("jd_analysis")
    mapper = data.get("evidence_map")
    if not isinstance(analysis, dict) or not isinstance(mapper, dict):
        raise ValueError("V1 PASS 1 bundle must contain jd_analysis and evidence_map objects.")
    return analysis, mapper


async def run_v1_pass1(
    inp: ResumeInput,
    *,
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
    stage_artifact_cb: Callable[[str, dict[str, Any], str], None] | None = None,
) -> str:
    analysis_diagnostics: dict[str, Any] = {}
    try:
        analysis_raw = await call_v1_stage_model(
            system_blocks=[cached_text_block(read_prompt("01_JD_Intelligence_Analyzer.md", "v1"))],
            messages=[{
                "role": "user",
                "content": "\n\n".join([
                    v1_short_controller("JD_INTELLIGENCE"),
                    *v1_common_input(inp),
                ]),
            }],
            label=labeled_step(request_label, "V1 JD INTELLIGENCE"),
            cost_cb=cost_cb,
            output_validator=None,
            retry_instruction="",
            cancel_event=cancel_event,
            model_override=nvidia_model,
            nvidia_thinking_override=nvidia_thinking,
            diagnostics=analysis_diagnostics,
            nvidia_validation_pass_override=False,
            nvidia_max_attempts_override=1,
            provider_fallback_override=False,
        )
    except Exception as exc:
        if stage_artifact_cb:
            stage_artifact_cb(
                "jd_intelligence_api_error",
                v1_api_error_data(exc, analysis_diagnostics),
                v1_api_error_reasoning(
                    analysis_diagnostics,
                    "Provider request failed before JD Intelligence reasoning was returned.",
                ),
            )
        raise
    try:
        analysis = extract_json(analysis_raw)
    except Exception:
        if stage_artifact_cb:
            stage_artifact_cb(
                "jd_intelligence_parse_error",
                {"raw": analysis_raw},
                v1_reasoning_text(analysis_diagnostics),
            )
        raise
    if stage_artifact_cb:
        stage_artifact_cb("jd_intelligence", analysis, v1_reasoning_text(analysis_diagnostics))

    mapper = await run_v1_evidence_mapping(
        inp,
        analysis,
        cost_cb=cost_cb,
        request_label=request_label,
        cancel_event=cancel_event,
        nvidia_model=nvidia_model,
        nvidia_thinking=nvidia_thinking,
        stage_artifact_cb=stage_artifact_cb,
    )

    return json.dumps(
        {
            "schema_version": "v1",
            "stage": "v1_pass1",
            "jd_analysis": analysis,
            "evidence_map": mapper,
        },
        indent=2,
    )


async def run_v1_evidence_mapping(
    inp: ResumeInput,
    analysis: dict[str, Any],
    *,
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
    stage_artifact_cb: Callable[[str, dict[str, Any], str], None] | None = None,
) -> dict[str, Any]:
    mapper_diagnostics: dict[str, Any] = {}
    mapper_input = [
        v1_short_controller("EVIDENCE_MAPPING"),
        *v1_common_input(inp),
        "JD ANALYSIS FROM PROMPT 1\n" + compact_json(analysis),
    ]
    try:
        mapper_raw = await call_v1_stage_model(
            system_blocks=[
                cached_text_block(read_prompt("02_Evidence_Mapper_DES_Planner.md", "v1")),
                cached_text_block(read_prompt("story.md", "v1")),
            ],
            messages=[{"role": "user", "content": "\n\n".join(mapper_input)}],
            label=labeled_step(request_label, "V1 EVIDENCE MAPPING"),
            cost_cb=cost_cb,
            output_validator=None,
            retry_instruction="",
            cancel_event=cancel_event,
            model_override=nvidia_model,
            nvidia_thinking_override=nvidia_thinking,
            diagnostics=mapper_diagnostics,
            nvidia_validation_pass_override=False,
            nvidia_max_attempts_override=1,
            provider_fallback_override=False,
        )
    except Exception as exc:
        if stage_artifact_cb:
            stage_artifact_cb(
                "evidence_map_api_error",
                v1_api_error_data(exc, mapper_diagnostics),
                v1_api_error_reasoning(
                    mapper_diagnostics,
                    "Provider request failed before Evidence Mapping reasoning was returned.",
                ),
            )
        raise
    try:
        mapper = extract_json(mapper_raw)
    except Exception:
        if stage_artifact_cb:
            stage_artifact_cb(
                "evidence_map_parse_error",
                {"raw": mapper_raw},
                v1_reasoning_text(mapper_diagnostics),
            )
        raise
    if stage_artifact_cb:
        stage_artifact_cb("evidence_map", mapper, v1_reasoning_text(mapper_diagnostics))
    return mapper


async def run_v1_pass2(
    inp: ResumeInput,
    pass1_text: str,
    approval_text: str,
    *,
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
    stage_artifact_cb: Callable[[str, dict[str, Any], str], None] | None = None,
) -> str:
    analysis, mapper = v1_pass1_bundle(pass1_text)
    composer_input = [
        v1_short_controller("RESUME_COMPOSITION"),
        *v1_composer_input(inp),
        "LOCKED EVIDENCE PACKET FROM PROMPT 2\n" + compact_json(mapper),
        f"USER DES APPROVAL\n{approval_text.strip() or 'No DES'}",
    ]
    composer_diagnostics: dict[str, Any] = {}
    try:
        composer_raw = await call_v1_stage_model(
            system_blocks=[
                cached_text_block(read_prompt("03_Evidence_Locked_Resume_Composer.md", "v1")),
            ],
            messages=[{"role": "user", "content": "\n\n".join(composer_input)}],
            label=labeled_step(request_label, "V1 RESUME COMPOSITION"),
            cost_cb=cost_cb,
            output_validator=None,
            retry_instruction="",
            cancel_event=cancel_event,
            model_override=nvidia_model,
            nvidia_thinking_override=nvidia_thinking,
            diagnostics=composer_diagnostics,
            nvidia_validation_pass_override=False,
            nvidia_max_attempts_override=1,
            provider_fallback_override=False,
        )
    except Exception as exc:
        if stage_artifact_cb:
            stage_artifact_cb(
                "resume_composer_api_error",
                v1_api_error_data(exc, composer_diagnostics),
                v1_api_error_reasoning(
                    composer_diagnostics,
                    "Provider request failed before Resume Composer reasoning was returned.",
                ),
            )
        raise
    try:
        resume = extract_json(composer_raw)
    except Exception:
        if stage_artifact_cb:
            stage_artifact_cb(
                "resume_composer_parse_error",
                {"raw": composer_raw},
                v1_reasoning_text(composer_diagnostics),
            )
        raise
    if stage_artifact_cb:
        stage_artifact_cb("resume_composer", resume, v1_reasoning_text(composer_diagnostics))
    return json.dumps(resume, indent=2)


def labeled_step(request_label: str, step: str) -> str:
    return f"{request_label} | {step}" if request_label else step


def v3_runtime_input(
    inp: ResumeInput,
    *,
    run_mode: str,
    approval_text: str = "",
    pass1_text: str = "",
    resume_json: dict[str, Any] | None = None,
) -> str:
    parts = [
        read_prompt("prompt_short.md", "v3"),
        f"RUN MODE:\n{run_mode}",
        f"COMPANY:\n{inp.company.strip()}",
        f"TITLE:\n{inp.title.strip()}",
        f"JD:\n{inp.jd.strip()}",
        "COMPANY RESEARCH:\nNot provided.",
        "GITHUB PROJECT RESEARCH:\nNot provided.",
    ]
    if inp.words.strip():
        parts.append(f"LOCATION:\n{inp.words.strip()}")
    if inp.des.strip():
        parts.append(f"DES:\n{inp.des.strip()}")
    if pass1_text.strip():
        parts.append(f"PASS 1 PLAN:\n{pass1_text.strip()}")
    if approval_text.strip():
        parts.append(f"APPROVED DES:\n{approval_text.strip()}")
    if resume_json is not None:
        parts.append(
            "GENERATED RESUME JSON:\n"
            + json.dumps(resume_json_to_compact(resume_json), indent=2)
        )
    return "\n\n".join(parts)


def guided_json_schema_for_validator(
    validator: Callable[[str], str | None] | None,
) -> dict[str, Any] | None:
    if not validator or not get_nvidia_guided_json():
        return None
    if validator in {validate_json_response, validate_compact_resume_response}:
        return {"type": "object"}
    return None


async def run_pass1(
    inp: ResumeInput,
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
    prompt_profile: str = "v1",
    diagnostics: dict[str, Any] | None = None,
    stage_artifact_cb: Callable[[str, dict[str, Any], str], None] | None = None,
) -> str:
    profile = normalize_prompt_profile(prompt_profile)
    if profile == "v1":
        return await run_v1_pass1(
            inp,
            cost_cb=cost_cb,
            request_label=request_label,
            cancel_event=cancel_event,
            nvidia_model=nvidia_model,
            nvidia_thinking=nvidia_thinking,
            stage_artifact_cb=stage_artifact_cb,
        )
    if profile == "v3":
        user_message = v3_runtime_input(inp, run_mode="PASS 1 - COMPANY + JD PLAN")
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
        cost_cb=cost_cb,
        output_validator=None if profile == "v3" else validate_pass1_response,
        retry_instruction=(None if profile == "v3" else (
            NVIDIA_RETRY_INSTRUCTION +
            "\nReturn the required DES CANDIDATE BANK with parseable lines starting DES 1 |."
        )
        ),
        cancel_event=cancel_event,
        model_override=nvidia_model,
        nvidia_thinking_override=nvidia_thinking,
        diagnostics=diagnostics,
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
    prompt_profile: str = "v1",
    rejected_response_cb: Callable[[int, str, str], None] | None = None,
    stage_artifact_cb: Callable[[str, dict[str, Any], str], None] | None = None,
) -> str:
    profile = normalize_prompt_profile(prompt_profile)
    if profile == "v1":
        return await run_v1_pass2(
            inp,
            pass1_text,
            approval_text,
            cost_cb=cost_cb,
            request_label=request_label,
            cancel_event=cancel_event,
            nvidia_model=nvidia_model,
            nvidia_thinking=nvidia_thinking,
            stage_artifact_cb=stage_artifact_cb,
        )
    normalized_approval = approval_text.strip() if is_experimental_prompt_profile(profile) else normalize_approval(approval_text)
    if profile == "v3":
        first_user = v3_runtime_input(inp, run_mode="PASS 1 - COMPANY + JD PLAN")
        second_user = v3_runtime_input(
            inp,
            run_mode="PASS 2 - WRITE APPROVED RESUME JSON",
            approval_text=normalized_approval or "Use current evidence only.",
            pass1_text=pass1_text,
        )
        messages = [
            {"role": "user", "content": first_user},
            {"role": "assistant", "content": pass1_text.strip()},
            {"role": "user", "content": second_user},
        ]
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
        cost_cb=cost_cb,
        output_validator=None if profile == "v3" else validate_json_response,
        cancel_event=cancel_event,
        model_override=nvidia_model,
        nvidia_thinking_override=nvidia_thinking,
        rejected_response_cb=rejected_response_cb,
    )


async def run_recruiter_review(
    *,
    jd: str,
    resume1_json: dict[str, Any],
    company: str = "",
    title: str = "",
    des: str = "",
    inp: ResumeInput | None = None,
    resume2_json: dict[str, Any] | None = None,
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
    prompt_profile: str = "stable",
    pass1_audit: str = "",
    resume_generation_process: str = "",
    rejected_response_cb: Callable[[int, str, str], None] | None = None,
) -> str:
    profile = normalize_prompt_profile(prompt_profile)
    if profile == "v3":
        resume_input = inp or ResumeInput(company=company, title=title, jd=jd, des=des)
        if not resume_input.company.strip():
            resume_input.company = company
        if not resume_input.title.strip():
            resume_input.title = title
        if not resume_input.jd.strip():
            resume_input.jd = jd
        parts = [
            v3_runtime_input(
                resume_input,
                run_mode="HOTDOG REPAIR JSON",
                approval_text=des,
                pass1_text=pass1_audit,
                resume_json=resume1_json,
            )
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
        label=labeled_step(
            request_label,
            "FINAL CHECK" if is_experimental_prompt_profile(profile)
            else "RECRUITER REVIEW",
        ),
        cost_cb=cost_cb,
        output_validator=None if profile == "v3" else validate_json_response,
        cancel_event=cancel_event,
        model_override=nvidia_model,
        nvidia_thinking_override=nvidia_thinking,
        rejected_response_cb=rejected_response_cb,
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
    company_research: str = "",
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
    prompt_profile: str = "stable",
) -> str:
    profile = normalize_prompt_profile(prompt_profile)
    if profile == "v1" and not company_research.strip():
        company_research = await asyncio.to_thread(
            research_company_for_questions,
            company,
            title,
            questions,
        )
    system_blocks = [cached_text_block(read_prompt_with_fallback("questions.md", profile))]
    user_message = "\n".join([
        HUMAN_TEXT_STYLE_RULE.strip(),
        "",
        f"Prompt Profile: {profile}",
        "",
        "Candidate Resume JSON:",
        json.dumps(resume_json, indent=2),
        "",
        "Job Description:",
        jd.strip(),
        "",
        "Company Research (live web search results):",
        company_research.strip() or "No live company research was available. Use the Job Description only for company facts.",
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
        "Use only personal facts explicitly included in Application Questions or resume JSON. For researchable questions such as compensation, use the JD and live research or a safe flexible answer. Never guess legal or identity facts.",
    ])
    return await call_model(
        system_blocks=system_blocks,
        messages=[{"role": "user", "content": user_message}],
        label=labeled_step(request_label, "APPLICATION QA"),
        cost_cb=cost_cb,
        cancel_event=cancel_event,
        model_override=nvidia_model,
        nvidia_thinking_override=nvidia_thinking,
    )


async def run_linkedin_outreach(
    *,
    company: str,
    title: str,
    location: str,
    jd: str,
    resume_json: dict[str, Any],
    cost_cb=None,
    request_label: str = "",
    cancel_event: threading.Event | None = None,
    nvidia_model: str | None = None,
    nvidia_thinking: bool | None = None,
    prompt_profile: str = "v1",
) -> str:
    profile = normalize_prompt_profile(prompt_profile)
    if profile == "v1":
        raise ValueError(
            f"{profile.upper()} LinkedIn prompting was removed. "
            "Use the GUI Link field and Resume JSON output."
        )
    system_blocks = [cached_text_block(read_prompt_with_fallback("linkedin.md", profile))]
    user_message = "\n".join([
        HUMAN_TEXT_STYLE_RULE.strip(),
        "",
        f"Prompt Profile: {profile}",
        "",
        "Candidate Resume JSON:",
        json.dumps(resume_json, indent=2),
        "",
        "Job Description:",
        jd.strip(),
        "",
        f"Company: {company}",
        f"Title: {title}",
        f"Location: {location.strip() or 'Not provided'}",
    ])
    response = await call_model(
        system_blocks=system_blocks,
        messages=[{"role": "user", "content": user_message}],
        label=labeled_step(request_label, "LINKEDIN OUTREACH"),
        cost_cb=cost_cb,
        cancel_event=cancel_event,
        model_override=nvidia_model,
        nvidia_thinking_override=nvidia_thinking,
    )
    return enforce_linkedin_message_limit(response)


def fetch_public_search_html(url: str, timeout_seconds: float = 12.0) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        return response.read().decode("utf-8", errors="replace")


def clean_search_result_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", unescape(value))
    return re.sub(r"\s+", " ", value).strip()


def decode_duckduckgo_result_url(value: str) -> str:
    href = unescape(value).strip()
    if href.startswith("//"):
        href = "https:" + href
    parsed = urlparse(href)
    if parsed.netloc.endswith("duckduckgo.com"):
        target = parse_qs(parsed.query).get("uddg", [""])[0]
        if target:
            return target
    return href


def research_company_for_questions(
    company: str,
    title: str,
    questions: str = "",
    *,
    max_results: int = 6,
) -> str:
    queries = [
        (
            "Company and role research",
            f'"{company.strip()}" official engineering product blog documentation "{title.strip()}"'.strip(),
        )
    ]
    if re.search(r"\b(?:salary|compensation|pay|base pay|pay range|wage|remuneration)\b", questions, re.IGNORECASE):
        queries.append(
            (
                "Compensation research",
                f'"{company.strip()}" "{title.strip()}" salary range compensation base pay job posting'.strip(),
            )
        )

    pattern = re.compile(
        r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>'
        r'.*?'
        r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>',
        flags=re.DOTALL | re.IGNORECASE,
    )
    seen_urls: set[str] = set()
    sections: list[str] = []
    errors: list[str] = []
    per_query_limit = max(1, max_results // len(queries))
    for label, query in queries:
        search_url = "https://html.duckduckgo.com/html/?q=" + quote_plus(query)
        try:
            page = fetch_public_search_html(search_url)
        except Exception as exc:
            errors.append(f"{label}: {type(exc).__name__}")
            continue

        results: list[str] = []
        for href, raw_title, raw_snippet in pattern.findall(page):
            result_url = decode_duckduckgo_result_url(href)
            parsed = urlparse(result_url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc or result_url in seen_urls:
                continue
            result_title = clean_search_result_text(raw_title)
            snippet = clean_search_result_text(raw_snippet)
            if not result_title:
                continue
            seen_urls.add(result_url)
            results.append(
                "\n".join([
                    f"Result {len(results) + 1}: {result_title}",
                    f"URL: {result_url}",
                    f"Search excerpt: {snippet or 'No excerpt available.'}",
                ])
            )
            if len(results) >= per_query_limit:
                break
        if results:
            sections.append("\n\n".join([f"{label} query: {query}", *results]))

    if not sections:
        if errors:
            return f"Live company research unavailable: {'; '.join(errors)}. Use the Job Description only for company facts."
        return "Live company research returned no usable results. Use the Job Description only for company facts."
    return "\n\n".join([
        "Use these search excerpts as research leads. Prefer an explicit range in the JD or an official company job posting. Do not claim facts beyond the displayed title, URL, and excerpt.",
        *sections,
    ])


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
    stripped = text.strip()
    try:
        complete = json.loads(stripped)
    except json.JSONDecodeError:
        complete = None
    if isinstance(complete, dict):
        return normalize_resume_json(complete)

    blocks = re.findall(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    candidates: list[str] = list(blocks)
    if not candidates:
        decoder = json.JSONDecoder()
        for match in re.finditer(r"\{", text):
            try:
                parsed, end = decoder.raw_decode(text[match.start():])
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                candidates.append(text[match.start():match.start() + end])
    last_error: Exception | None = None
    fallback: dict[str, Any] | None = None
    for candidate in reversed(candidates):
        try:
            data = json.loads(candidate)
            if not isinstance(data, dict):
                continue
            if fallback is None:
                fallback = data
            lower_keys = {str(key).lower() for key in data}
            if "experience" in lower_keys or "professional_experience" in lower_keys:
                return normalize_resume_json(data)
        except json.JSONDecodeError as exc:
            last_error = exc
    if fallback is not None:
        return normalize_resume_json(fallback)
    raise ValueError(f"Could not extract valid JSON from model output: {last_error}")


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return cleaned or "Resume"


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M")


def _facts_section(title: str, value: str) -> str:
    text = (value or "").strip()
    body = text if text else "(none)"
    return f"### {title}\n\n```text\n{body}\n```"


def format_des_facts_entry(
    *,
    request_id: str,
    inp: ResumeInput,
    prompt_profile: str,
    pass1_text: str = "",
    approval_text: str = "",
) -> str:
    recorded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"## {request_id}",
        "",
        f"- Recorded: {recorded_at}",
        f"- Prompt profile: {normalize_prompt_profile(prompt_profile)}",
        f"- Company: {inp.company}",
        f"- Title: {inp.title}",
        f"- Location: {inp.words.strip() or CURRENT_LOCATION}",
        "",
        _facts_section("Candidate DES input / confirmed facts", inp.des),
        "",
        _facts_section("PASS 1 model suggestions to review", pass1_text),
        "",
        _facts_section("Approval / extra evidence", approval_text),
        "",
        "Review this block before moving anything into Story.md.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def update_des_facts_file(
    path: Path,
    *,
    request_id: str,
    inp: ResumeInput,
    prompt_profile: str,
    pass1_text: str = "",
    approval_text: str = "",
) -> None:
    safe_request_id = slug(request_id)
    start = f"<!-- DES_FACTS_START:{safe_request_id} -->"
    end = f"<!-- DES_FACTS_END:{safe_request_id} -->"
    entry = "\n".join([
        start,
        format_des_facts_entry(
            request_id=request_id,
            inp=inp,
            prompt_profile=prompt_profile,
            pass1_text=pass1_text,
            approval_text=approval_text,
        ).rstrip(),
        end,
        "",
    ])
    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = (
            "# DES Facts\n\n"
            "Collected from DES inputs, PASS 1 suggestions, and approval text. "
            "Treat PASS 1 suggestions as review items until you confirm them.\n\n"
        )
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n?", flags=re.DOTALL)
    if pattern.search(text):
        updated = pattern.sub(entry, text)
    else:
        updated = text.rstrip() + "\n\n" + entry
    save_text(path, updated)


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
