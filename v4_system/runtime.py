from __future__ import annotations

import asyncio
import copy
import hashlib
import json
import os
import re
import threading
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

import pipeline


V4_ROOT = Path(__file__).resolve().parent
CHECKPOINT_DIR_NAME = "v4_checkpoints"
FINAL_FILE_NAME = "05_resume_output.json"
RENDERER_FILE_NAME = "06_v4_renderer_input.json"
DES_APPROVAL_FILE = V4_ROOT / "approved_des_evidence.json"

STAGES = (
    "jd_analyzer",
    "story_mapper",
    "experience_writer",
    "project_writer",
    "validator_repair",
)

STAGE_NUMBERS = {
    "jd_analyzer": "1",
    "story_mapper": "2",
    "experience_writer": "3A",
    "project_writer": "3B",
    "validator_repair": "4",
}

STAGE_FILES = {
    "jd_analyzer": "01_jd_analyzer.json",
    "story_mapper": "02_story_mapper.json",
    "experience_writer": "03a_experience_writer.json",
    "project_writer": "03b_project_writer.json",
    "validator_repair": "04_validator_repair.json",
}

PUBLIC_STAGE_FILES = {
    "jd_analyzer": "02_jd_parse_output.json",
    "story_mapper": "03_v4_mapper_plan.json",
    "experience_writer": "04_v4_experience_output.json",
    "project_writer": "04_v4_project_output.json",
    "validator_repair": "04_v4_validator_output.json",
}

_DES_LOCK = threading.Lock()


@dataclass
class V4RunResult:
    status: str
    step_number: str
    message: str
    output: dict[str, Any] | None
    des_questions: list[dict[str, Any]]
    final_path: str = ""
    renderer_path: str = ""
    retry_after_seconds: int = 0


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{threading.get_ident()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def resolve_v4_path(relative_path: str) -> Path:
    path = (V4_ROOT / relative_path).resolve()
    if path != V4_ROOT and V4_ROOT not in path.parents:
        raise ValueError(f"V4 path escapes the system directory: {relative_path}")
    if not path.is_file():
        raise FileNotFoundError(f"Missing canonical V4 file: {relative_path}")
    return path


def story_role_id(story_id: str) -> str:
    if story_id.startswith("TCS-II-"):
        return "TCS_SWE_II"
    if story_id.startswith("TCS-I-"):
        return "TCS_SWE_I"
    if story_id.startswith("GHI-"):
        return "GHI"
    if story_id.startswith("TA-"):
        return "TA"
    if story_id.startswith("PROJ-"):
        return "PROJECT"
    return ""


def section_text(block: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^###\s+{re.escape(heading)}\s*$\n(.*?)(?=^###\s+|^##\s+|^#\s+|\Z)",
        block,
    )
    return match.group(1).strip() if match else ""


def parse_story_catalog(story_text: str) -> list[dict[str, Any]]:
    heading_pattern = re.compile(r"(?m)^##\s+([A-Z]+(?:-[A-Z]+)?-\d{2})\s+[—-]\s+(.+?)\s*$")
    matches = list(heading_pattern.finditer(story_text))
    catalog: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(story_text)
        block = story_text[match.end():end]
        engineering_story = section_text(block, "Engineering story")
        resume_keywords = section_text(block, "Resume keywords")
        if not engineering_story or not resume_keywords:
            raise ValueError(f"Story {match.group(1)} is missing Engineering story or Resume keywords")
        keyword_values = [item.strip().rstrip(".") for item in resume_keywords.replace("\n", " ").split(",") if item.strip()]
        metrics = [
            line[2:].strip()
            for line in section_text(block, "FAANG framing dimensions").splitlines()
            if line.startswith("- ")
        ]
        catalog.append({
            "story_id": match.group(1),
            "role_id": story_role_id(match.group(1)),
            "title": match.group(2).strip(),
            "engineering_story": engineering_story,
            "resume_keywords": keyword_values,
            "approved_metrics": metrics,
        })
    if not catalog:
        raise ValueError("No story headings were found in canonical V4 story.md")
    ids = [story["story_id"] for story in catalog]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate story IDs found in canonical V4 story.md")
    return catalog


def load_system_snapshot(
    *,
    application_id: str,
    jd: str,
    model: str,
    thinking: bool,
) -> dict[str, Any]:
    config_path = resolve_v4_path("system_config.json")
    system_config = read_json(config_path)
    candidate_path = resolve_v4_path(system_config["input_paths"]["candidate_profile"])
    story_path = resolve_v4_path(system_config["input_paths"]["story_bank"])
    approvals_path = resolve_v4_path(system_config["input_paths"]["approved_des_evidence"])
    candidate_profile = read_json(candidate_path)
    story_text = story_path.read_text(encoding="utf-8")

    prompts: dict[str, Any] = {}
    schemas: dict[str, Any] = {}
    for stage in STAGES:
        prompt_relative = system_config["prompt_paths"][stage]
        prompt_path = resolve_v4_path(prompt_relative)
        prompt_text = prompt_path.read_text(encoding="utf-8")
        prompts[stage] = {
            "path": prompt_relative.replace("\\", "/"),
            "sha256": sha256_text(prompt_text),
            "text": prompt_text,
        }
        schema_relative = system_config["output_schema_paths"][stage]
        schema_path = resolve_v4_path(schema_relative)
        schema = read_json(schema_path)
        Draft202012Validator.check_schema(schema)
        schemas[stage] = {
            "path": schema_relative.replace("\\", "/"),
            "sha256": sha256_text(canonical_json(schema)),
            "id": schema.get("$id", ""),
            "schema": schema,
        }

    story_catalog = parse_story_catalog(story_text)
    profile_roles = {item["role_id"] for item in candidate_profile.get("experience", [])}
    configured_roles = {
        role_id
        for mode in system_config["resume_modes"].values()
        for role_id in mode["experience_display_order"]
    }
    missing_roles = sorted(configured_roles - profile_roles)
    if missing_roles:
        raise ValueError(f"candidate_profile.json is missing configured role IDs: {', '.join(missing_roles)}")

    return {
        "application_id": application_id,
        "created_at": utc_now(),
        "jd_sha256": sha256_text(jd),
        "system_config": system_config,
        "config_sha256": sha256_text(canonical_json(system_config)),
        "candidate_profile": candidate_profile,
        "candidate_profile_sha256": sha256_text(canonical_json(candidate_profile)),
        "story_text": story_text,
        "story_sha256": sha256_text(story_text),
        "story_catalog": story_catalog,
        "approved_des_source": approvals_path.name,
        "prompts": prompts,
        "schemas": schemas,
        "model_settings": {
            "provider": "nvidia",
            "model": model,
            "thinking": bool(thinking),
            "temperature": pipeline.get_nvidia_temperature(),
            "top_p": pipeline.get_nvidia_top_p(),
            "seed": pipeline.get_nvidia_seed(),
            "stream": pipeline.get_nvidia_stream(),
            "reasoning_budget": pipeline.get_nvidia_reasoning_budget(),
            "max_tokens": pipeline.get_response_max_tokens(),
            "max_concurrent_requests": pipeline.get_nvidia_max_concurrent_requests(),
            "guided_json": pipeline.get_nvidia_guided_json(),
            "validation_pass": False,
        },
    }


def context_contract_fingerprint(context: dict[str, Any]) -> str:
    contract = {
        "jd_sha256": context.get("jd_sha256"),
        "config_sha256": context.get("config_sha256"),
        "candidate_profile_sha256": context.get("candidate_profile_sha256"),
        "story_sha256": context.get("story_sha256"),
        "prompts": {
            stage: item.get("sha256")
            for stage, item in context.get("prompts", {}).items()
        },
        "schemas": {
            stage: item.get("sha256")
            for stage, item in context.get("schemas", {}).items()
        },
        "model_settings": context.get("model_settings", {}),
    }
    return sha256_text(canonical_json(contract))


def validate_required_keys(value: dict[str, Any], required: tuple[str, ...], label: str) -> None:
    if set(value) != set(required):
        raise ValueError(f"{label} input keys must be exactly {list(required)}")


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[./+#&-][A-Za-z0-9]+)*", text))


def normalized_term(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()


def flattened_jd_keywords(
    jd_analysis: dict[str, Any],
    system_config: dict[str, Any],
) -> list[dict[str, Any]]:
    flattened: list[dict[str, Any]] = []
    for priority_key in system_config["keyword_priority"]["processing_order"]:
        bucket, requirement_status = priority_key.split(".", 1)
        group = jd_analysis.get(bucket, {}).get(requirement_status, {})
        for category in ("tech", "nontech"):
            for keyword in group.get(category, []):
                flattened.append({
                    "id": f"K{len(flattened) + 1:03d}",
                    "keyword": str(keyword),
                    "bucket": int(bucket),
                    "requirement_status": requirement_status,
                    "category": category,
                })
    return flattened


def scope_approvals_to_jd(
    approvals: list[dict[str, Any]],
    jd_analysis: dict[str, Any],
    system_config: dict[str, Any],
) -> list[dict[str, Any]]:
    allowed = {
        normalized_term(item["keyword"])
        for item in flattened_jd_keywords(jd_analysis, system_config)
        if item["category"] == "tech"
    }
    return [
        copy.deepcopy(approval)
        for approval in approvals
        if normalized_term(approval.get("keyword")) in allowed
    ]


def scope_approvals_to_plan(
    approvals: list[dict[str, Any]],
    mapper_plan: dict[str, Any],
) -> list[dict[str, Any]]:
    allowed_pairs = {
        (normalized_term(item.get("keyword")), str(item.get("story_id", "")).strip())
        for item in mapper_plan.get("keyword_plan", [])
        if item.get("category") == "tech" and item.get("story_id")
    }
    return [
        copy.deepcopy(approval)
        for approval in approvals
        if (normalized_term(approval.get("keyword")), str(approval.get("story_id", "")).strip())
        in allowed_pairs
    ]


def mapper_blocking_key(item: dict[str, Any]) -> str:
    return f"{item.get('bucket')}.{item.get('requirement_status')}.tech"


def normalize_mapper_output(
    data: dict[str, Any],
    context: dict[str, Any],
    inputs: dict[str, Any],
) -> dict[str, Any]:
    config = context["system_config"]
    expected = {
        item["id"]: item
        for item in flattened_jd_keywords(inputs.get("JD_ANALYSIS", {}), config)
    }
    approvals = {
        (normalized_term(item.get("keyword")), str(item.get("story_id", "")).strip())
        for item in inputs.get("APPROVED_DES_EVIDENCE", [])
    }
    plan_by_id: dict[str, dict[str, Any]] = {}
    normalized_plan: list[dict[str, Any]] = []
    for item in data.get("keyword_plan", []):
        if not isinstance(item, dict):
            continue
        expected_item = expected.get(str(item.get("id", "")))
        if not expected_item:
            continue
        normalized = copy.deepcopy(item)
        for key in ("keyword", "bucket", "requirement_status", "category"):
            normalized[key] = expected_item[key]
        pair = (normalized_term(normalized["keyword"]), str(normalized.get("story_id", "")).strip())
        if pair in approvals:
            normalized["evidence_state"] = "candidate_approved"
            normalized["confidence"] = float(config["des"]["approval_confidence"])
        plan_by_id[normalized["id"]] = normalized
        normalized_plan.append(normalized)
    data["keyword_plan"] = normalized_plan

    blocking = config["des"]["blocking_policy"]
    blocking_items: list[dict[str, Any]] = []
    for item in normalized_plan:
        if item.get("category") != "tech" or item.get("evidence_state") != "confirmation_required":
            continue
        if blocking.get(mapper_blocking_key(item), False):
            blocking_items.append(item)
        else:
            item["evidence_state"] = "missing"
            item["target"] = "missing"

    existing_questions = {
        str(question.get("keyword_id", "")): question
        for question in data.get("des_questions", [])
        if isinstance(question, dict)
    }
    start = int(config["des"]["numbering_starts_at"])
    questions: list[dict[str, Any]] = []
    for offset, item in enumerate(blocking_items):
        question = copy.deepcopy(existing_questions.get(item["id"], {}))
        question.update({
            "des_id": start + offset,
            "keyword_id": item["id"],
            "keyword": item["keyword"],
            "bucket": item["bucket"],
            "closest_story_id": str(item.get("story_id", "")),
        })
        question.setdefault("proposed_use", str(item.get("evidence", "")).strip() or "current JD requirement")
        question.setdefault("question", f"Did you personally use {item['keyword']} in this work?")
        questions.append(question)
    data["status"] = "des_required" if questions else "ready"
    data["des_questions"] = questions

    allowed_skill_states = set(config["skills"]["allowed_sources"])
    eligible_skill_ids = [
        keyword_id
        for keyword_id, item in plan_by_id.items()
        if item.get("category") == "tech"
        and item.get("evidence_state") in allowed_skill_states
    ]
    if config["skills"].get("include_all_eligible_current_jd_terms", False):
        data["skills_keyword_ids"] = eligible_skill_ids
    else:
        data["skills_keyword_ids"] = list(dict.fromkeys(
            keyword_id
            for keyword_id in data.get("skills_keyword_ids", [])
            if keyword_id in eligible_skill_ids
        ))
    coverage = {state: 0 for state in (
        "direct", "supported_equivalent", "candidate_approved",
        "confirmation_required", "missing", "not_selected",
    )}
    for item in normalized_plan:
        state = item.get("evidence_state")
        if state in coverage:
            coverage[state] += 1
    coverage["total_keywords"] = len(normalized_plan)
    data["coverage"] = coverage
    return data


def planned_keyword_ids(mapper_plan: dict[str, Any]) -> set[str]:
    return {
        str(item.get("id"))
        for item in mapper_plan.get("keyword_plan", [])
        if item.get("id")
    }


def normalize_writer_output(stage: str, data: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    plan = inputs.get("MAPPER_PLAN", {})
    all_assigned: set[str] = set()
    used: set[str] = set()
    if stage == "experience_writer":
        allowed: dict[tuple[str, int, str], set[str]] = {}
        for role in plan.get("experience_plan", []):
            role_id = str(role.get("role_id", ""))
            for slot in role.get("slots", []):
                key = (role_id, int(slot.get("slot", 0)), str(slot.get("story_id", "")))
                ids = set(slot.get("keyword_ids", []))
                allowed[key] = ids
                all_assigned.update(ids)
        for role in data.get("experience", []):
            role_id = str(role.get("role_id", ""))
            for bullet in role.get("bullets", []):
                key = (role_id, int(bullet.get("slot", 0)), str(bullet.get("story_id", "")))
                bullet["keyword_ids"] = list(dict.fromkeys(
                    item for item in bullet.get("keyword_ids", []) if item in allowed.get(key, set())
                ))
                bullet["word_count"] = word_count(str(bullet.get("text", "")))
                used.update(bullet["keyword_ids"])
    else:
        allowed = {}
        for project in plan.get("project_plan", []):
            key = (int(project.get("rank", 0)), str(project.get("story_id", "")))
            ids = set(project.get("keyword_ids", []))
            allowed[key] = ids
            all_assigned.update(ids)
        for project in data.get("projects", []):
            key = (int(project.get("rank", 0)), str(project.get("story_id", "")))
            for bullet in project.get("bullets", []):
                bullet["keyword_ids"] = list(dict.fromkeys(
                    item for item in bullet.get("keyword_ids", []) if item in allowed.get(key, set())
                ))
                bullet["word_count"] = word_count(str(bullet.get("text", "")))
                used.update(bullet["keyword_ids"])
    data["used_keyword_ids"] = sorted(used)
    data["unused_keyword_ids"] = sorted(all_assigned - used)
    return data


def normalize_validator_output(
    data: dict[str, Any],
    context: dict[str, Any],
    inputs: dict[str, Any],
) -> dict[str, Any]:
    config = context["system_config"]
    plan = inputs.get("MAPPER_PLAN", {})
    keyword_by_id = {
        str(item.get("id")): item
        for item in plan.get("keyword_plan", [])
        if item.get("id")
    }
    experience_allowed: dict[tuple[str, str], set[str]] = {}
    for role in plan.get("experience_plan", []):
        role_id = str(role.get("role_id", ""))
        for slot in role.get("slots", []):
            key = (role_id, str(slot.get("story_id", "")))
            experience_allowed.setdefault(key, set()).update(slot.get("keyword_ids", []))
    project_allowed = {
        str(project.get("story_id", "")): set(project.get("keyword_ids", []))
        for project in plan.get("project_plan", [])
    }

    placed: set[str] = set()
    for role in data.get("experience", []):
        role_id = str(role.get("role_id", ""))
        for bullet in role.get("bullets", []):
            bullet.pop("slot", None)
            allowed = experience_allowed.get((role_id, str(bullet.get("story_id", ""))), set())
            bullet["keyword_ids"] = list(dict.fromkeys(
                item for item in bullet.get("keyword_ids", []) if item in allowed
            ))
            bullet["word_count"] = word_count(str(bullet.get("text", "")))
            placed.update(bullet["keyword_ids"])
    for project in data.get("projects", []):
        story_id = str(project.get("story_id", ""))
        allowed = project_allowed.get(story_id, set())
        for bullet in project.get("bullets", []):
            bullet.pop("slot", None)
            bullet.setdefault("story_id", story_id)
            bullet["keyword_ids"] = list(dict.fromkeys(
                item for item in bullet.get("keyword_ids", []) if item in allowed
            ))
            bullet["word_count"] = word_count(str(bullet.get("text", "")))
            placed.update(bullet["keyword_ids"])

    allowed_skill_states = set(config["skills"]["allowed_sources"])
    allowed_skill_ids = [
        keyword_id
        for keyword_id in dict.fromkeys(plan.get("skills_keyword_ids", []))
        if keyword_id in keyword_by_id
        and keyword_by_id[keyword_id].get("category") == "tech"
        and keyword_by_id[keyword_id].get("evidence_state") in allowed_skill_states
    ]
    canonical_skills = {
        normalized_term(keyword_by_id[keyword_id]["keyword"]): keyword_by_id[keyword_id]["keyword"]
        for keyword_id in allowed_skill_ids
    }
    seen_skills: set[str] = set()
    skill_groups: list[dict[str, Any]] = []
    for group in data.get("technical_skills", []):
        if not isinstance(group, dict):
            continue
        terms: list[str] = []
        for value in group.get("keywords", []):
            normalized = normalized_term(value)
            if normalized not in canonical_skills or normalized in seen_skills:
                continue
            seen_skills.add(normalized)
            terms.append(canonical_skills[normalized])
        if terms:
            skill_groups.append({"category": str(group.get("category", "")).strip(), "keywords": terms})
    data["technical_skills"] = skill_groups

    skill_ids = {
        keyword_id
        for keyword_id in allowed_skill_ids
        if normalized_term(keyword_by_id[keyword_id]["keyword"]) in seen_skills
    }
    missing = {
        keyword_id
        for keyword_id, item in keyword_by_id.items()
        if item.get("evidence_state") in {"missing", "confirmation_required"}
    }
    skills_only = skill_ids - placed - missing
    all_ids = set(keyword_by_id)
    not_selected = all_ids - placed - skills_only - missing
    data["coverage"] = {
        "placed_keyword_ids": sorted(placed),
        "skills_only_keyword_ids": sorted(skills_only),
        "missing_keyword_ids": sorted(missing),
        "not_selected_keyword_ids": sorted(not_selected),
    }

    mode = config["resume_modes"].get(plan.get("resume_mode"), {})
    summary_config = mode.get("summary", {})
    if not summary_config.get("enabled", False):
        data["summary"] = ""
    else:
        data["summary"] = re.sub(r"\s+", " ", str(data.get("summary", "")).strip())
    if plan.get("status") == "ready":
        if data.get("status") == "des_required":
            data["status"] = "repaired"
        data["des_questions"] = []
    return data


def normalize_stage_output(
    stage: str,
    data: dict[str, Any],
    context: dict[str, Any],
    inputs: dict[str, Any],
) -> dict[str, Any]:
    normalized = copy.deepcopy(data)
    if stage == "story_mapper":
        return normalize_mapper_output(normalized, context, inputs)
    if stage in {"experience_writer", "project_writer"}:
        return normalize_writer_output(stage, normalized, inputs)
    if stage == "validator_repair":
        return normalize_validator_output(normalized, context, inputs)
    return normalized


def exact_keyword_contract_errors(
    stage: str,
    data: dict[str, Any],
    inputs: dict[str, Any],
) -> list[str]:
    plan = inputs.get("MAPPER_PLAN", {})
    keyword_by_id = {
        str(item.get("id")): str(item.get("keyword", ""))
        for item in plan.get("keyword_plan", [])
        if item.get("id")
    }
    errors: list[str] = []
    collections: list[dict[str, Any]] = []
    if stage == "experience_writer":
        collections = [bullet for role in data.get("experience", []) for bullet in role.get("bullets", [])]
    elif stage == "project_writer":
        collections = [bullet for project in data.get("projects", []) for bullet in project.get("bullets", [])]
    elif stage == "validator_repair":
        collections = [
            *[bullet for role in data.get("experience", []) for bullet in role.get("bullets", [])],
            *[bullet for project in data.get("projects", []) for bullet in project.get("bullets", [])],
        ]
    for bullet in collections:
        text = str(bullet.get("text", ""))
        for keyword_id in bullet.get("keyword_ids", []):
            keyword = keyword_by_id.get(keyword_id, "")
            if keyword and keyword not in text:
                errors.append(f"{keyword_id} must appear with exact JD wording: {keyword}")
    return errors


def stage_contract_errors(
    stage: str,
    data: dict[str, Any],
    context: dict[str, Any],
    inputs: dict[str, Any],
) -> list[str]:
    errors = exact_keyword_contract_errors(stage, data, inputs)
    if stage == "story_mapper":
        expected_ids = {
            item["id"]
            for item in flattened_jd_keywords(inputs.get("JD_ANALYSIS", {}), context["system_config"])
        }
        actual_ids = {str(item.get("id")) for item in data.get("keyword_plan", [])}
        if actual_ids != expected_ids:
            errors.append("keyword_plan must contain every JD Analyzer keyword exactly once")
    if stage == "validator_repair":
        plan = inputs.get("MAPPER_PLAN", {})
        keyword_by_id = {
            str(item.get("id")): item
            for item in plan.get("keyword_plan", [])
            if item.get("id")
        }
        allowed_states = set(context["system_config"]["skills"]["allowed_sources"])
        expected_skills = {
            str(keyword_by_id[keyword_id]["keyword"])
            for keyword_id in plan.get("skills_keyword_ids", [])
            if keyword_id in keyword_by_id
            and keyword_by_id[keyword_id].get("category") == "tech"
            and keyword_by_id[keyword_id].get("evidence_state") in allowed_states
        }
        actual_skills = {
            str(skill)
            for group in data.get("technical_skills", [])
            for skill in group.get("keywords", [])
        }
        if actual_skills != expected_skills:
            errors.append("technical_skills must exactly match MAPPER_PLAN.skills_keyword_ids")
        mode = context["system_config"]["resume_modes"].get(plan.get("resume_mode"), {})
        summary_config = mode.get("summary", {})
        summary_words = word_count(str(data.get("summary", "")))
        if summary_config.get("enabled", False):
            minimum = int(summary_config.get("minimum_words", 0))
            maximum = int(summary_config.get("maximum_words", 0))
            if not minimum <= summary_words <= maximum:
                errors.append(f"summary must contain {minimum}-{maximum} words")
        elif summary_words:
            errors.append("summary must be empty for this resume mode")
    return errors


def opening_verb(text: str) -> str:
    match = re.match(r"\s*([A-Za-z]+)", text)
    return match.group(1).casefold() if match else ""


METRIC_PATTERN = re.compile(
    r"(?<![A-Za-z])(?:p\d+\s+)?\d[\d,]*(?:\.\d+)?(?:[MK])?\+?%?"
    r"(?:\s*(?:–|-|to)\s*\d[\d,]*(?:\.\d+)?(?:[MK])?\+?%?)?"
    r"(?:\s*(?:ms|milliseconds?|seconds?|minutes?|hours?|days?|weeks?|months?|years?|users?|records?|"
    r"applications?|services?|roles?|teams?|developers?|engineers?|students?|submissions?|requests?|"
    r"transactions?|workflows?|sources?|countries|releases?|findings?|certificates?|forms?|orders?|prompts?|variants?))?",
    re.IGNORECASE,
)


def metric_errors(text: str, evidence: str, story_id: str) -> list[str]:
    errors: list[str] = []
    for match in METRIC_PATTERN.finditer(text):
        metric = match.group(0).strip()
        if metric and metric not in evidence:
            errors.append(f"metric '{metric}' is not verbatim in story {story_id}")
    return errors


def schema_errors(data: Any, schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema)
    return [
        f"schema {'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path))[:12]
    ]


def jd_deterministic_errors(data: dict[str, Any], _context: dict[str, Any], _inputs: dict[str, Any]) -> list[str]:
    keywords: list[str] = []
    for bucket in ("5", "4", "3", "2"):
        for status in ("required", "core", "preferred"):
            for category in ("tech", "nontech"):
                keywords.extend(data[bucket][status][category])
    normalized = [re.sub(r"\s+", " ", item.strip()).casefold() for item in keywords]
    errors: list[str] = []
    if len(keywords) > 35:
        errors.append("JD analysis contains more than 35 keywords")
    if len(normalized) != len(set(normalized)):
        errors.append("JD analysis contains duplicate normalized keywords")
    return errors


def mapper_deterministic_errors(data: dict[str, Any], context: dict[str, Any], _inputs: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    config = context["system_config"]
    mode = config["resume_modes"].get(data.get("resume_mode"))
    if not mode:
        return ["mapper selected an unknown resume_mode"]
    story_ids = {story["story_id"] for story in context["story_catalog"]}
    expected_roles = mode["experience_display_order"]
    actual_roles = [item["role_id"] for item in data["experience_plan"]]
    if actual_roles != expected_roles:
        errors.append(f"experience role order must be {expected_roles}")
    for role in data["experience_plan"]:
        expected_count = mode["experience_bullets"].get(role["role_id"])
        if len(role["slots"]) != expected_count:
            errors.append(f"{role['role_id']} must contain {expected_count} slots")
        for slot in role["slots"]:
            if slot["story_id"] not in story_ids:
                errors.append(f"unknown experience story ID {slot['story_id']}")
    expected_projects = mode["projects"]["count"]
    if len(data["project_plan"]) != expected_projects:
        errors.append(f"project plan must contain {expected_projects} projects")
    for project in data["project_plan"]:
        if project["story_id"] not in story_ids:
            errors.append(f"unknown project story ID {project['story_id']}")
        elif not project["story_id"].startswith("PROJ-"):
            errors.append(f"project story must use a PROJ ID: {project['story_id']}")
    if data["status"] == "des_required" and not data["des_questions"]:
        errors.append("des_required mapper output must include DES questions")
    if data["status"] == "ready" and data["des_questions"]:
        errors.append("ready mapper output must not include DES questions")
    keyword_by_id = {item["id"]: item for item in data["keyword_plan"]}
    blocking = config["des"]["blocking_policy"]
    for question in data["des_questions"]:
        keyword = keyword_by_id.get(question["keyword_id"])
        if not keyword:
            errors.append(f"DES question references unknown keyword ID {question['keyword_id']}")
            continue
        if keyword["category"] != "tech":
            errors.append(f"DES question cannot target nontechnical keyword {question['keyword_id']}")
        policy_key = f"{keyword['bucket']}.{keyword['requirement_status']}.tech"
        if data["status"] == "des_required" and not blocking.get(policy_key, False):
            errors.append(f"DES question is not blocking under configuration: {question['keyword_id']}")
    coverage = data["coverage"]
    state_total = sum(coverage[key] for key in (
        "direct", "supported_equivalent", "candidate_approved", "confirmation_required", "missing", "not_selected"
    ))
    if coverage["total_keywords"] != state_total or coverage["total_keywords"] != len(data["keyword_plan"]):
        errors.append("mapper coverage counts do not match keyword_plan")
    return errors


def role_map(context: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["role_id"]: item for item in context["candidate_profile"]["experience"]}


def story_map(context: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["story_id"]: item for item in context["story_catalog"]}


def validate_bullet(
    bullet: dict[str, Any],
    *,
    story: dict[str, Any],
    minimum: int,
    maximum: int,
) -> list[str]:
    errors: list[str] = []
    actual_count = word_count(bullet["text"])
    if bullet["word_count"] != actual_count:
        errors.append(f"reported word_count {bullet['word_count']} does not equal {actual_count}")
    if not minimum <= actual_count <= maximum:
        errors.append(f"bullet word count {actual_count} is outside {minimum}-{maximum}")
    evidence = story["engineering_story"] + "\n" + "\n".join(story["approved_metrics"])
    errors.extend(metric_errors(bullet["text"], evidence, story["story_id"]))
    return errors


def experience_deterministic_errors(data: dict[str, Any], context: dict[str, Any], inputs: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    config = context["system_config"]
    plan = inputs["MAPPER_PLAN"]
    mode = config["resume_modes"][plan["resume_mode"]]
    roles = role_map(context)
    stories = story_map(context)
    expected_plans = {item["role_id"]: item for item in plan["experience_plan"]}
    if [item["role_id"] for item in data["experience"]] != mode["experience_display_order"]:
        errors.append("experience writer role order does not match configured display order")
    verbs: list[str] = []
    for output_role in data["experience"]:
        role_id = output_role["role_id"]
        locked = roles.get(role_id)
        plan_role = expected_plans.get(role_id)
        if not locked or not plan_role:
            errors.append(f"unexpected experience role {role_id}")
            continue
        for key in ("title", "company", "location", "dates"):
            if output_role[key] != locked[key]:
                errors.append(f"locked field changed: {role_id}.{key}")
        if len(output_role["bullets"]) != mode["experience_bullets"][role_id]:
            errors.append(f"wrong bullet count for {role_id}")
        slot_map = {slot["slot"]: slot for slot in plan_role["slots"]}
        for bullet in output_role["bullets"]:
            planned = slot_map.get(bullet["slot"])
            if not planned or bullet["story_id"] != planned["story_id"]:
                errors.append(f"experience story mismatch in {role_id} slot {bullet['slot']}")
                continue
            if not set(bullet["keyword_ids"]).issubset(planned["keyword_ids"]):
                errors.append(f"unassigned keyword ID in {role_id} slot {bullet['slot']}")
            errors.extend(validate_bullet(
                bullet,
                story=stories[bullet["story_id"]],
                minimum=config["writing"]["bullet_min_words"],
                maximum=config["writing"]["bullet_max_words"],
            ))
            verbs.append(opening_verb(bullet["text"]))
    if len(verbs) != len(set(verbs)):
        errors.append("experience opening verbs are not unique")
    return errors


def project_deterministic_errors(data: dict[str, Any], context: dict[str, Any], inputs: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    config = context["system_config"]
    plan = inputs["MAPPER_PLAN"]
    mode = config["resume_modes"][plan["resume_mode"]]
    stories = story_map(context)
    expected = {item["rank"]: item for item in plan["project_plan"]}
    if len(data["projects"]) != mode["projects"]["count"]:
        errors.append("project writer returned the wrong project count")
    verbs: list[str] = []
    for project in data["projects"]:
        planned = expected.get(project["rank"])
        if not planned or project["story_id"] != planned["story_id"]:
            errors.append(f"project rank {project['rank']} does not match mapper plan")
            continue
        if len(project["bullets"]) != mode["projects"]["bullets_each"]:
            errors.append(f"wrong bullet count for project rank {project['rank']}")
        for bullet in project["bullets"]:
            if not set(bullet["keyword_ids"]).issubset(planned["keyword_ids"]):
                errors.append(f"unassigned keyword ID in project rank {project['rank']}")
            errors.extend(validate_bullet(
                bullet,
                story=stories[project["story_id"]],
                minimum=config["writing"]["bullet_min_words"],
                maximum=config["writing"]["bullet_max_words"],
            ))
            verbs.append(opening_verb(bullet["text"]))
    if len(verbs) != len(set(verbs)):
        errors.append("project opening verbs are not unique")
    return errors


def validator_deterministic_errors(data: dict[str, Any], context: dict[str, Any], inputs: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    config = context["system_config"]
    plan = inputs["MAPPER_PLAN"]
    mode = config["resume_modes"][plan["resume_mode"]]
    roles = role_map(context)
    stories = story_map(context)
    keyword_by_id = {item["id"]: item for item in plan["keyword_plan"]}
    keyword_ids = set(keyword_by_id)
    expected_experience = {item["role_id"]: item for item in plan["experience_plan"]}
    expected_projects = {item["story_id"]: item for item in plan["project_plan"]}
    if [item["role_id"] for item in data["experience"]] != mode["experience_display_order"]:
        errors.append("validator experience order does not match configuration")
    verbs: list[str] = []
    placed_ids: set[str] = set()
    for output_role in data["experience"]:
        role_id = output_role["role_id"]
        locked = roles.get(role_id)
        planned = expected_experience.get(role_id)
        if not locked or not planned:
            errors.append(f"validator returned unexpected role {role_id}")
            continue
        for key in ("title", "company", "location", "dates"):
            if output_role[key] != locked[key]:
                errors.append(f"validator changed locked field {role_id}.{key}")
        if len(output_role["bullets"]) != mode["experience_bullets"][role_id]:
            errors.append(f"validator returned wrong bullet count for {role_id}")
        allowed_stories = {slot["story_id"] for slot in planned["slots"]}
        for bullet in output_role["bullets"]:
            if bullet["story_id"] not in allowed_stories:
                errors.append(f"validator used unplanned story {bullet['story_id']} for {role_id}")
                continue
            if not set(bullet["keyword_ids"]).issubset(keyword_ids):
                errors.append(f"validator used unknown keyword ID in {role_id}")
            placed_ids.update(bullet["keyword_ids"])
            errors.extend(validate_bullet(
                bullet,
                story=stories[bullet["story_id"]],
                minimum=config["writing"]["bullet_min_words"],
                maximum=config["writing"]["bullet_max_words"],
            ))
            verbs.append(opening_verb(bullet["text"]))
    if len(data["projects"]) != mode["projects"]["count"]:
        errors.append("validator returned wrong project count")
    for project in data["projects"]:
        planned = expected_projects.get(project["story_id"])
        if not planned:
            errors.append(f"validator used unplanned project {project['story_id']}")
            continue
        if len(project["bullets"]) != mode["projects"]["bullets_each"]:
            errors.append(f"validator returned wrong bullet count for {project['story_id']}")
        for bullet in project["bullets"]:
            if not set(bullet["keyword_ids"]).issubset(keyword_ids):
                errors.append(f"validator used unknown project keyword ID in {project['story_id']}")
            placed_ids.update(bullet["keyword_ids"])
            errors.extend(validate_bullet(
                bullet,
                story=stories[project["story_id"]],
                minimum=config["writing"]["bullet_min_words"],
                maximum=config["writing"]["bullet_max_words"],
            ))
            verbs.append(opening_verb(bullet["text"]))
    if len(verbs) != len(set(verbs)):
        errors.append("opening verbs are not unique across Experience and Projects")
    for coverage_ids in data["coverage"].values():
        if not set(coverage_ids).issubset(keyword_ids):
            errors.append("validator coverage contains unknown keyword IDs")
    coverage_groups = [set(values) for values in data["coverage"].values()]
    combined_coverage = set().union(*coverage_groups) if coverage_groups else set()
    if sum(len(values) for values in coverage_groups) != len(combined_coverage):
        errors.append("validator coverage groups contain duplicate keyword IDs")
    if set(data["coverage"]["placed_keyword_ids"]) != placed_ids:
        errors.append("placed_keyword_ids do not match keyword IDs used in bullets")
    allowed_skill_states = set(config["skills"]["allowed_sources"])
    for group in data["technical_skills"]:
        for skill in group["keywords"]:
            matches = [
                item for item in plan["keyword_plan"]
                if item["keyword"].strip().casefold() == skill.strip().casefold()
            ]
            if not matches:
                errors.append(f"technical skill is not in mapper keyword plan: {skill}")
            elif not any(
                item["category"] == "tech" and item["evidence_state"] in allowed_skill_states
                for item in matches
            ):
                errors.append(f"technical skill lacks an approved technical evidence state: {skill}")
    if data["des_questions"]:
        errors.append("validator must not return DES questions; Story Mapper owns the only DES gate")
    return errors


def make_stage_validator(
    stage: str,
    schema: dict[str, Any],
    context: dict[str, Any],
    inputs: dict[str, Any],
) -> Callable[[str], str | None]:
    def validate(text: str) -> str | None:
        try:
            data = pipeline.extract_json(text)
        except Exception as exc:
            return f"invalid JSON: {exc}"
        data = normalize_stage_output(stage, data, context, inputs)
        problems = schema_errors(data, schema)
        if not problems:
            problems.extend(stage_contract_errors(stage, data, context, inputs))
        return "; ".join(problems[:10]) if problems else None

    return validate


def parse_des_approval(reply: str) -> tuple[list[int], str]:
    match = re.match(
        r"^\s*(?:DES\s*)?(\d+(?:\s*(?:,|to|-)\s*(?:DES\s*)?\d+)*)",
        reply,
        flags=re.IGNORECASE,
    )
    if not match:
        raise ValueError("Enter a DES range or list, such as 1 to 4 or 1, 3, 5.")
    expression = re.sub(r"\bDES\b", "", match.group(1), flags=re.IGNORECASE).strip()
    ids: list[int] = []
    for part in re.split(r"\s*,\s*", expression):
        range_match = re.fullmatch(r"(\d+)\s*(?:to|-)\s*(\d+)", part, flags=re.IGNORECASE)
        if range_match:
            start, end = int(range_match.group(1)), int(range_match.group(2))
            if end < start or end - start > 100:
                raise ValueError("DES ranges must be ascending and contain at most 101 items.")
            ids.extend(range(start, end + 1))
        else:
            ids.append(int(part))
    unique = list(dict.fromkeys(ids))
    note = reply[match.end():].strip(" ,;:-")
    return unique, note


def load_approved_des() -> dict[str, Any]:
    with _DES_LOCK:
        return read_json(DES_APPROVAL_FILE)


def persist_des_approvals(reply: str, questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    approved_ids, note = parse_des_approval(reply)
    by_id = {int(question["des_id"]): question for question in questions}
    unknown = [des_id for des_id in approved_ids if des_id not in by_id]
    if unknown:
        raise ValueError(f"Unknown DES number(s): {', '.join(str(item) for item in unknown)}")
    created: list[dict[str, Any]] = []
    with _DES_LOCK:
        document = read_json(DES_APPROVAL_FILE)
        approvals = document.setdefault("approvals", [])
        existing = {
            (str(item.get("keyword", "")).strip().casefold(), str(item.get("story_id", "")).strip())
            for item in approvals
        }
        for des_id in approved_ids:
            question = by_id[des_id]
            story_id = question.get("closest_story_id", "")
            key = (str(question["keyword"]).strip().casefold(), str(story_id).strip())
            if key in existing:
                continue
            approval = {
                "keyword": question["keyword"],
                "story_id": story_id,
                "confidence": 1.0,
                "source": "candidate_des_approval",
                "note": note,
                "approved_at": utc_now(),
            }
            approvals.append(approval)
            created.append(approval)
            existing.add(key)
        atomic_write_json(DES_APPROVAL_FILE, document)
    return created


def selected_stories(
    context: dict[str, Any],
    story_ids: list[str],
    mapper_plan: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    stories = story_map(context)
    missing = sorted(set(story_ids) - set(stories))
    if missing:
        raise ValueError(f"Unknown selected story IDs: {', '.join(missing)}")
    selected = [copy.deepcopy(stories[story_id]) for story_id in dict.fromkeys(story_ids)]
    if mapper_plan is not None:
        keyword_by_id = {
            str(item.get("id")): str(item.get("keyword", "")).strip()
            for item in mapper_plan.get("keyword_plan", [])
            if item.get("id") and str(item.get("keyword", "")).strip()
        }
        allowed_ids_by_story: dict[str, list[str]] = {}
        for role in mapper_plan.get("experience_plan", []):
            for slot in role.get("slots", []):
                story_id = str(slot.get("story_id", ""))
                allowed_ids_by_story.setdefault(story_id, []).extend(slot.get("keyword_ids", []))
        for project in mapper_plan.get("project_plan", []):
            story_id = str(project.get("story_id", ""))
            allowed_ids_by_story.setdefault(story_id, []).extend(project.get("keyword_ids", []))
        for story in selected:
            story["resume_keywords"] = list(dict.fromkeys(
                keyword_by_id[keyword_id]
                for keyword_id in allowed_ids_by_story.get(story["story_id"], [])
                if keyword_id in keyword_by_id
            ))
    return selected


def v3_renderer_type(mapper_plan: dict[str, Any]) -> str:
    if mapper_plan.get("resume_mode") == "entry_ai_ml":
        return "aiml"
    role = str(mapper_plan.get("role", "")).casefold()
    if "full stack" in role or "fullstack" in role or "frontend" in role:
        return "fullstack"
    return "backend"


def build_v4_renderer_input(
    context: dict[str, Any],
    mapper_plan: dict[str, Any],
    final_output: dict[str, Any],
) -> dict[str, Any]:
    """Adapt validated V4 content to the existing V3 DOCX renderer contract."""
    candidate_profile = context["candidate_profile"]
    candidate = candidate_profile["candidate"]
    roles = role_map(context)
    keyword_plan = {
        item["id"]: item
        for item in mapper_plan.get("keyword_plan", [])
        if isinstance(item, dict) and item.get("id")
    }

    experience = []
    experience_order = []
    for role in final_output.get("experience", []):
        locked = roles[role["role_id"]]
        output_id = locked.get("resume_output_id") or role["role_id"]
        experience_order.append(output_id)
        experience.append({
            "id": output_id,
            "role_id": role["role_id"],
            "title": role["title"],
            "company": role["company"],
            "location": role["location"],
            "dates": role["dates"],
            "employment_note": locked.get("employment_note", ""),
            "bullets": [bullet["text"] for bullet in role.get("bullets", [])],
        })

    projects = []
    for project in final_output.get("projects", []):
        keyword_ids = [
            keyword_id
            for bullet in project.get("bullets", [])
            for keyword_id in bullet.get("keyword_ids", [])
        ]
        tech = []
        for keyword_id in dict.fromkeys(keyword_ids):
            keyword = keyword_plan.get(keyword_id, {})
            if keyword.get("category") == "tech" and keyword.get("keyword"):
                tech.append(keyword["keyword"])
        projects.append({
            "id": project["story_id"],
            "story_id": project["story_id"],
            "name": project["name"],
            "tech": tech,
            "github_url": "",
            "bullets": [bullet["text"] for bullet in project.get("bullets", [])],
        })

    mode = mapper_plan.get("resume_mode", "entry_swe")
    level = 3 if mode == "mid_swe" or mapper_plan.get("level") == "mid" else 2
    layout_profile = {
        "entry_ai_ml": "aiml_entry",
        "mid_swe": "mid",
    }.get(mode, "professional_entry")
    section_order = ["summary", "education", "experience", "projects", "skills"]

    return {
        "schema_version": "v4_v3_renderer_input_v1",
        "name": candidate["name"],
        "contact": candidate["contact_line"],
        "location": candidate["location"],
        "linkedin_url": candidate.get("linkedin_url", ""),
        "github_url": candidate.get("github_url", ""),
        "summary": str(final_output.get("summary", "")).strip(),
        "education": copy.deepcopy(candidate_profile.get("education", [])),
        "experience": experience,
        "experience_order": experience_order,
        "projects": projects,
        "technical_skills": [
            {
                "category": group["category"],
                "terms": list(group.get("keywords", [])),
            }
            for group in final_output.get("technical_skills", [])
        ],
        "section_order": section_order,
        "config": {
            "type": v3_renderer_type(mapper_plan),
            "level": level,
            "layout_profile": layout_profile,
            "section_order": section_order,
            "experience_order": experience_order,
            "bold_markers": True,
            "output": "Keval_Shah_V4_Resume.docx",
        },
    }


def ensure_v4_renderer_input(request_dir: Path) -> Path:
    request_dir = request_dir.resolve()
    context_path = request_dir / CHECKPOINT_DIR_NAME / "00_context.json"
    mapper_path = request_dir / CHECKPOINT_DIR_NAME / STAGE_FILES["story_mapper"]
    final_path = request_dir / FINAL_FILE_NAME
    missing = [path.name for path in (context_path, mapper_path, final_path) if not path.is_file()]
    if missing:
        raise ValueError(
            "Complete V4 before building DOCX. Missing saved artifact(s): " + ", ".join(missing)
        )
    context = read_json(context_path)
    mapper_record = read_json(mapper_path)
    final_output = read_json(final_path)
    renderer_path = request_dir / RENDERER_FILE_NAME
    atomic_write_json(
        renderer_path,
        build_v4_renderer_input(context, mapper_record["output"], final_output),
    )
    return renderer_path


class V4Orchestrator:
    def __init__(
        self,
        *,
        request_dir: Path,
        application_id: str,
        model: str,
        thinking: bool,
        cost_cb=None,
        cancel_event: threading.Event | None = None,
        stage_cb: Callable[[str, str], None] | None = None,
    ):
        self.request_dir = request_dir.resolve()
        self.application_id = application_id
        self.model = model
        self.thinking = thinking
        self.cost_cb = cost_cb
        self.cancel_event = cancel_event
        self.stage_cb = stage_cb
        self.checkpoint_dir = self.request_dir / CHECKPOINT_DIR_NAME
        self.history_dir = self.checkpoint_dir / "history"
        self.context_path = self.checkpoint_dir / "00_context.json"
        self.pending_des_path = self.checkpoint_dir / "pending_des.json"
        self.retry_path = self.checkpoint_dir / "retry_pending.json"
        self.renderer_path = self.request_dir / RENDERER_FILE_NAME
        self.current_stage = "startup"

    def ensure_context(self, jd: str) -> dict[str, Any]:
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        current = load_system_snapshot(
            application_id=self.application_id,
            jd=jd,
            model=self.model,
            thinking=self.thinking,
        )
        if self.context_path.exists():
            saved = read_json(self.context_path)
            if saved["jd_sha256"] != sha256_text(jd):
                raise ValueError("The saved V4 application uses a different Job Description.")
            if context_contract_fingerprint(saved) == context_contract_fingerprint(current):
                return saved
            if self.pending_des_path.exists():
                self.pending_des_path.unlink()
        atomic_write_json(self.context_path, current)
        return current

    def latest_path(self, stage: str) -> Path:
        return self.checkpoint_dir / STAGE_FILES[stage]

    def load_stage(self, stage: str, context: dict[str, Any] | None = None) -> dict[str, Any] | None:
        path = self.latest_path(stage)
        if not path.exists():
            return None
        record = read_json(path)
        if context is None:
            return record
        diagnostics = record.get("diagnostics", {})
        expected = {
            "config_sha256": context["config_sha256"],
            "prompt_sha256": context["prompts"][stage]["sha256"],
            "output_schema_sha256": context["schemas"][stage]["sha256"],
        }
        if any(diagnostics.get(key) != value for key, value in expected.items()):
            return None
        return record

    def save_stage(self, stage: str, record: dict[str, Any]) -> None:
        atomic_write_json(self.latest_path(stage), record)
        atomic_write_json(self.request_dir / PUBLIC_STAGE_FILES[stage], record["output"])
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        atomic_write_json(self.history_dir / f"{stamp}_{STAGE_FILES[stage]}", record)

    def save_renderer_input(
        self,
        context: dict[str, Any],
        mapper_plan: dict[str, Any],
        final_output: dict[str, Any],
    ) -> Path:
        atomic_write_json(
            self.renderer_path,
            build_v4_renderer_input(context, mapper_plan, final_output),
        )
        return self.renderer_path

    async def call_stage(
        self,
        stage: str,
        inputs: dict[str, Any],
        required_keys: tuple[str, ...],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        self.current_stage = stage
        if self.stage_cb:
            self.stage_cb(STAGE_NUMBERS[stage], stage)
        validate_required_keys(inputs, required_keys, stage)
        prompt = context["prompts"][stage]
        schema_info = context["schemas"][stage]
        schema = schema_info["schema"]
        validator = make_stage_validator(stage, schema, context, inputs)
        diagnostics: dict[str, Any] = {}
        raw = await pipeline.call_model(
            system_blocks=[pipeline.cached_text_block(prompt["text"])],
            messages=[{"role": "user", "content": json.dumps(inputs, ensure_ascii=False, separators=(",", ":"))}],
            label=f"{self.application_id} | V4 STEP {STAGE_NUMBERS[stage]} | {stage}",
            cost_cb=self.cost_cb,
            output_validator=validator,
            retry_instruction=(
                "The prior stage output was not valid JSON for this stage schema. "
                "Return only the complete JSON object for the current stage."
            ),
            cancel_event=self.cancel_event,
            provider_override="nvidia",
            model_override=context["model_settings"]["model"],
            nvidia_thinking_override=context["model_settings"]["thinking"],
            diagnostics=diagnostics,
            guided_json_schema_override=schema,
            nvidia_validation_pass_override=False,
        )
        output = pipeline.extract_json(raw)
        output = normalize_stage_output(stage, output, context, inputs)
        final_error = validator(raw)
        if final_error:
            raise ValueError(f"Stage output remained invalid after retries: {stage}")
        stage_status = str(output.get("status", "complete"))
        diagnostics.update({
            "application_id": self.application_id,
            "stage": stage,
            "step_number": STAGE_NUMBERS[stage],
            "prompt_path": prompt["path"],
            "prompt_sha256": prompt["sha256"],
            "config_sha256": context["config_sha256"],
            "input_schema_version": "runtime_contract_v1",
            "output_schema_path": schema_info["path"],
            "output_schema_version": schema_info["id"],
            "output_schema_sha256": schema_info["sha256"],
            "schema_result": "PASS",
            "stage_status": stage_status,
        })
        record = {
            "stage": stage,
            "step_number": STAGE_NUMBERS[stage],
            "completed_at": utc_now(),
            "inputs": inputs,
            "raw_output": raw,
            "output": output,
            "diagnostics": diagnostics,
        }
        self.save_stage(stage, record)
        return record

    def mapper_input(
        self,
        *,
        context: dict[str, Any],
        jd_analysis: dict[str, Any],
        des_reply: str,
    ) -> dict[str, Any]:
        approvals = scope_approvals_to_jd(
            load_approved_des().get("approvals", []),
            jd_analysis,
            context["system_config"],
        )
        return {
            "SYSTEM_CONFIG": context["system_config"],
            "JD_ANALYSIS": jd_analysis,
            "CANDIDATE_PROFILE": context["candidate_profile"],
            "STORY_CATALOG": context["story_catalog"],
            "APPROVED_DES_EVIDENCE": approvals,
            "DES_REPLY": des_reply.strip(),
        }

    def pause_for_des(self, stage: str, questions: list[dict[str, Any]]) -> V4RunResult:
        pending = {
            "source_stage": stage,
            "created_at": utc_now(),
            "questions": questions,
        }
        atomic_write_json(self.pending_des_path, pending)
        return V4RunResult(
            status="des_required",
            step_number=STAGE_NUMBERS[stage],
            message=f"Step {STAGE_NUMBERS[stage]} of 4 requires candidate DES approval.",
            output=None,
            des_questions=questions,
        )

    async def run(self, *, jd: str, des_reply: str = "") -> V4RunResult:
        context = self.ensure_context(jd)
        try:
            final_path = self.request_dir / FINAL_FILE_NAME
            if final_path.exists() and not des_reply.strip():
                final_output = read_json(final_path)
                mapper_record = self.load_stage("story_mapper", context)
                validator_record = self.load_stage("validator_repair", context)
                if mapper_record is None or validator_record is None:
                    final_output = None
                if final_output is None:
                    pass
                else:
                    renderer_path = self.save_renderer_input(context, mapper_record["output"], final_output)
                    return V4RunResult(
                        status=final_output["status"],
                        step_number="4",
                        message=f"Step 4 of 4 complete: {final_output['status']}.",
                        output=final_output,
                        des_questions=[],
                        final_path=str(final_path),
                        renderer_path=str(renderer_path),
                    )
            if self.pending_des_path.exists() and not des_reply.strip():
                pending = read_json(self.pending_des_path)
                return self.pause_for_des(pending["source_stage"], pending["questions"])
            if des_reply.strip():
                if not self.pending_des_path.exists():
                    raise ValueError("No saved DES questions are waiting for approval.")
                pending = read_json(self.pending_des_path)
                persist_des_approvals(des_reply, pending["questions"])

            jd_record = self.load_stage("jd_analyzer", context)
            if jd_record is None:
                jd_record = await self.call_stage(
                    "jd_analyzer",
                    {"JOB_DESCRIPTION": jd},
                    ("JOB_DESCRIPTION",),
                    context,
                )
            jd_analysis = jd_record["output"]

            mapper_record = None if des_reply.strip() else self.load_stage("story_mapper", context)
            if mapper_record is None:
                mapper_inputs = self.mapper_input(
                    context=context,
                    jd_analysis=jd_analysis,
                    des_reply=des_reply,
                )
                mapper_record = await self.call_stage(
                    "story_mapper",
                    mapper_inputs,
                    (
                        "SYSTEM_CONFIG", "JD_ANALYSIS", "CANDIDATE_PROFILE", "STORY_CATALOG",
                        "APPROVED_DES_EVIDENCE", "DES_REPLY",
                    ),
                    context,
                )
            mapper_plan = mapper_record["output"]
            if mapper_plan["status"] == "des_required":
                return self.pause_for_des("story_mapper", mapper_plan["des_questions"])

            if self.pending_des_path.exists():
                self.pending_des_path.unlink()

            approved_des = scope_approvals_to_plan(
                load_approved_des().get("approvals", []),
                mapper_plan,
            )
            experience_story_ids = [
                slot["story_id"]
                for role in mapper_plan["experience_plan"]
                for slot in role["slots"]
            ]
            project_story_ids = [project["story_id"] for project in mapper_plan["project_plan"]]
            experience_inputs = {
                "SYSTEM_CONFIG": context["system_config"],
                "CANDIDATE_PROFILE": context["candidate_profile"],
                "MAPPER_PLAN": mapper_plan,
                "SELECTED_EXPERIENCE_STORIES": selected_stories(
                    context, experience_story_ids, mapper_plan
                ),
                "APPROVED_DES_EVIDENCE": approved_des,
            }
            project_inputs = {
                "SYSTEM_CONFIG": context["system_config"],
                "MAPPER_PLAN": mapper_plan,
                "SELECTED_PROJECT_STORIES": selected_stories(
                    context, project_story_ids, mapper_plan
                ),
                "APPROVED_DES_EVIDENCE": approved_des,
            }

            experience_record = self.load_stage("experience_writer", context) if not des_reply.strip() else None
            project_record = self.load_stage("project_writer", context) if not des_reply.strip() else None
            tasks = []
            task_names = []
            if experience_record is None:
                tasks.append(self.call_stage(
                    "experience_writer",
                    experience_inputs,
                    ("SYSTEM_CONFIG", "CANDIDATE_PROFILE", "MAPPER_PLAN", "SELECTED_EXPERIENCE_STORIES", "APPROVED_DES_EVIDENCE"),
                    context,
                ))
                task_names.append("experience")
            if project_record is None:
                tasks.append(self.call_stage(
                    "project_writer",
                    project_inputs,
                    ("SYSTEM_CONFIG", "MAPPER_PLAN", "SELECTED_PROJECT_STORIES", "APPROVED_DES_EVIDENCE"),
                    context,
                ))
                task_names.append("project")
            if tasks:
                task_results = await asyncio.gather(*tasks)
                for name, record in zip(task_names, task_results):
                    if name == "experience":
                        experience_record = record
                    else:
                        project_record = record
            assert experience_record is not None and project_record is not None

            selected_all = selected_stories(
                context, experience_story_ids + project_story_ids, mapper_plan
            )
            validator_inputs = {
                "SYSTEM_CONFIG": context["system_config"],
                "CANDIDATE_PROFILE": context["candidate_profile"],
                "JD_ANALYSIS": jd_analysis,
                "MAPPER_PLAN": mapper_plan,
                "SELECTED_STORIES": selected_all,
                "APPROVED_DES_EVIDENCE": approved_des,
                "EXPERIENCE_OUTPUT": experience_record["output"],
                "PROJECT_OUTPUT": project_record["output"],
            }
            validator_record = await self.call_stage(
                "validator_repair",
                validator_inputs,
                (
                    "SYSTEM_CONFIG", "CANDIDATE_PROFILE", "JD_ANALYSIS", "MAPPER_PLAN", "SELECTED_STORIES",
                    "APPROVED_DES_EVIDENCE", "EXPERIENCE_OUTPUT", "PROJECT_OUTPUT",
                ),
                context,
            )
            final_output = validator_record["output"]
            final_path = self.request_dir / FINAL_FILE_NAME
            atomic_write_json(final_path, final_output)
            renderer_path = self.save_renderer_input(context, mapper_plan, final_output)
            if self.retry_path.exists():
                self.retry_path.unlink()
            return V4RunResult(
                status=final_output["status"],
                step_number="4",
                message=f"Step 4 of 4 complete: {final_output['status']}.",
                output=final_output,
                des_questions=[],
                final_path=str(final_path),
                renderer_path=str(renderer_path),
            )
        except pipeline.OperationCancelled:
            raise
        except ValueError as exc:
            if str(exc).startswith(("Enter a DES", "Unknown DES", "No saved DES", "The saved V4")):
                raise
            retry = {
                "application_id": self.application_id,
                "stage": self.current_stage,
                "scheduled_at": utc_now(),
                "retry_after_seconds": 30,
                "reason_type": type(exc).__name__,
            }
            atomic_write_json(self.retry_path, retry)
            return V4RunResult(
                status="retry_scheduled",
                step_number=STAGE_NUMBERS.get(self.current_stage, "0"),
                message=f"Step {STAGE_NUMBERS.get(self.current_stage, '0')} will retry automatically.",
                output=None,
                des_questions=[],
                retry_after_seconds=30,
            )
        except Exception as exc:
            retry = {
                "application_id": self.application_id,
                "stage": self.current_stage,
                "scheduled_at": utc_now(),
                "retry_after_seconds": 30,
                "reason_type": type(exc).__name__,
            }
            atomic_write_json(self.retry_path, retry)
            return V4RunResult(
                status="retry_scheduled",
                step_number=STAGE_NUMBERS.get(self.current_stage, "0"),
                message=f"Step {STAGE_NUMBERS.get(self.current_stage, '0')} will retry automatically.",
                output=None,
                des_questions=[],
                retry_after_seconds=30,
            )


async def run_v4_application(
    *,
    request_dir: Path,
    application_id: str,
    jd: str,
    des_reply: str = "",
    model: str | None = None,
    thinking: bool | None = None,
    cost_cb=None,
    cancel_event: threading.Event | None = None,
    stage_cb: Callable[[str, str], None] | None = None,
) -> V4RunResult:
    orchestrator = V4Orchestrator(
        request_dir=request_dir,
        application_id=application_id,
        model=model or pipeline.get_nvidia_model(),
        thinking=pipeline.get_nvidia_thinking() if thinking is None else thinking,
        cost_cb=cost_cb,
        cancel_event=cancel_event,
        stage_cb=stage_cb,
    )
    return await orchestrator.run(jd=jd, des_reply=des_reply)


def format_des_questions(questions: list[dict[str, Any]], step_number: str) -> str:
    lines = [
        "V4 RESUME SYSTEM",
        "",
        f"Step {step_number} of 4: DES approval required",
        "",
    ]
    for question in questions:
        lines.append(f"DES {question['des_id']} - {question['keyword']}")
        closest = question.get("closest_story_id", "")
        if closest:
            lines.append(f"  Closest story: {closest}")
        proposed = question.get("proposed_use", "")
        if proposed:
            lines.append(f"  Proposed use: {proposed}")
        lines.append(f"  {question['question']}")
        lines.append("")
    lines.extend([
        "Write only approvals you can factually support in the DES Approval field.",
        "One item: DES 1: Used this technology in the proposed closest story to deliver the described work.",
        "Several items: DES 1, 3, 5 Confirmed for each proposed closest story.",
        "Use separate runs when different DES items need different evidence notes.",
        "Then click Continue V4 to save the approval and rerun the model stages.",
    ])
    return "\n".join(lines)


def format_final_output(output: dict[str, Any]) -> str:
    lines = [
        "V4 RESUME SYSTEM",
        "",
        "Step 4 of 4: Complete",
        f"Status: {str(output.get('status', '')).replace('_', ' ').title()}",
        "",
        "PROFESSIONAL EXPERIENCE",
    ]
    for role in output.get("experience", []):
        lines.extend(["", f"{role['title']} | {role['company']}", f"{role['location']} | {role['dates']}"])
        lines.extend(f"- {bullet['text']}" for bullet in role.get("bullets", []))
    lines.extend(["", "PROJECTS"])
    for project in output.get("projects", []):
        lines.extend(["", project["name"]])
        lines.extend(f"- {bullet['text']}" for bullet in project.get("bullets", []))
    lines.extend(["", "TECHNICAL SKILLS"])
    for group in output.get("technical_skills", []):
        lines.append(f"{group['category']}: {', '.join(group['keywords'])}")
    repairs = output.get("repairs", [])
    lines.extend(["", f"Repairs applied: {', '.join(repairs) if repairs else 'None'}"])
    return "\n".join(lines)


def format_mapper_output(output: dict[str, Any]) -> str:
    if output.get("status") == "des_required":
        return format_des_questions(output.get("des_questions", []), "2")
    coverage = output.get("coverage", {})
    lines = [
        "V4 RESUME SYSTEM",
        "",
        "Step 2 of 4: Story mapping complete",
        f"Status: {str(output.get('status', '')).replace('_', ' ').title()}",
        f"Resume mode: {str(output.get('resume_mode', '')).replace('_', ' ').title()}",
        f"Role: {output.get('role', '')}",
        f"Level: {str(output.get('level', '')).replace('_', ' ').title()}",
        "",
        "COVERAGE",
        f"Total keywords: {coverage.get('total_keywords', 0)}",
        f"Direct: {coverage.get('direct', 0)}",
        f"Supported equivalent: {coverage.get('supported_equivalent', 0)}",
        f"Candidate approved: {coverage.get('candidate_approved', 0)}",
        f"Missing: {coverage.get('missing', 0)}",
        f"Not selected: {coverage.get('not_selected', 0)}",
        "",
        "EXPERIENCE PLAN",
    ]
    for role in output.get("experience_plan", []):
        lines.append(f"{role['role_id']}: {len(role.get('slots', []))} bullets")
        for slot in role.get("slots", []):
            lines.append(
                f"  Slot {slot['slot']}: {slot['story_id']} | {', '.join(slot['keyword_ids']) or 'No keywords'}"
            )
    lines.extend(["", "PROJECT PLAN"])
    for project in output.get("project_plan", []):
        lines.append(
            f"{project['rank']}. {project['story_id']} | score {project['score']} | "
            f"{', '.join(project['keyword_ids']) or 'No keywords'}"
        )
    return "\n".join(lines)


def format_experience_output(output: dict[str, Any]) -> str:
    lines = ["V4 RESUME SYSTEM", "", "Step 3A of 4: Experience writing complete"]
    for role in output.get("experience", []):
        lines.extend(["", f"{role['title']} | {role['company']}", f"{role['location']} | {role['dates']}"])
        lines.extend(f"- {bullet['text']}" for bullet in role.get("bullets", []))
    unused = output.get("unused_keyword_ids", [])
    lines.extend(["", f"Unused keyword IDs: {', '.join(unused) if unused else 'None'}"])
    return "\n".join(lines)


def format_project_output(output: dict[str, Any]) -> str:
    lines = ["V4 RESUME SYSTEM", "", "Step 3B of 4: Project writing complete"]
    for project in output.get("projects", []):
        lines.extend(["", f"{project['rank']}. {project['name']} ({project['story_id']})"])
        lines.extend(f"- {bullet['text']}" for bullet in project.get("bullets", []))
    unused = output.get("unused_keyword_ids", [])
    lines.extend(["", f"Unused keyword IDs: {', '.join(unused) if unused else 'None'}"])
    return "\n".join(lines)
