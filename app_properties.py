from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).parent

# ---------------------------------------------------------------------------
# Editable V1 candidate profile
# ---------------------------------------------------------------------------
# A new candidate should update this file and v1/Prompts/story.md only.
# Keep the stable role IDs because the V1 prompt flow uses them as structural
# identifiers. Titles, employers, dates, story ownership, project names, and
# links are all data and may be changed here.
CANDIDATE_PROFILE: dict[str, Any] = {
    "schema_version": "candidate_profile_v1",
    "candidate": {
        "name": "Keval Shah",
        "location": "San Francisco, California",
        "phone": "(607) 235-1181",
        "email": "keval.shah098@gmail.com",
        "linkedin_url": "https://www.linkedin.com/in/keval-shah0612",
        "linkedin_display": "linkedin.com/in/keval-shah0612",
        "github_url": "https://github.com/kevalshah0612",
        "github_display": "github.com/kevalshah0612",
        "portfolio_url": "",
        "portfolio_display": "",
        "resume_stem": "Keval_Shah",
        # Preserve the current visible V1 contact line. Add "github_display" or
        # "portfolio_display" here if either link should also be shown.
        "contact_display_fields": ["phone", "email", "linkedin_display"],
    },
    "experience": [
        {
            "role_id": "TA",
            "resume_output_id": "TA",
            "aliases": ["TA", "Teaching Assistant", "Binghamton University"],
            "story_prefixes": ["TA-"],
            "title": "Teaching Assistant",
            "company": "Binghamton University",
            "location": "Binghamton, NY",
            "dates": "Aug 2025 - Present",
            "current": True,
            "employment_note": "",
        },
        {
            "role_id": "GHI",
            "resume_output_id": "GHI",
            "aliases": ["GHI", "Global Health Impact"],
            "story_prefixes": ["GHI-"],
            "title": "Software Engineering Intern",
            "company": "Global Health Impact",
            "location": "New York, NY",
            "dates": "May 2025 - Jun 2025",
            "current": False,
            "employment_note": "",
        },
        {
            "role_id": "TCS_SWE_II",
            "resume_output_id": "TCS-SWE-II",
            "aliases": ["TCS_SWE_II", "TCS-SWE-II", "TCS II", "Software Engineer II"],
            "story_prefixes": ["TCS-I-", "TCS-II-"],
            "title": "Software Engineer II",
            "company": "Tata Consultancy Services",
            "location": "Gandhinagar, India",
            "dates": "Oct 2022 - Dec 2024",
            "current": False,
            "employment_note": "",
        },
        {
            "role_id": "TCS_SWE_I",
            "resume_output_id": "TCS-SWE",
            "aliases": ["TCS_SWE_I", "TCS-SWE", "TCS I", "Software Engineer I"],
            "story_prefixes": ["TCS-I-", "TCS-II-"],
            "title": "Software Engineer I",
            "company": "Tata Consultancy Services",
            "location": "Gandhinagar, India",
            "dates": "Mar 2021 - Sep 2022",
            "current": False,
            "employment_note": "",
        },
        {
            "role_id": "TCS_COMBINED",
            "resume_output_id": "TCS-COMBINED",
            "aliases": ["TCS_COMBINED", "TCS-COMBINED"],
            "story_prefixes": ["TCS-I-", "TCS-II-"],
            "source_role_ids": ["TCS_SWE_I", "TCS_SWE_II"],
            "title": "Software Engineer II",
            "company": "Tata Consultancy Services",
            "location": "Gandhinagar, India",
            "dates": "Mar 2021 - Dec 2024",
            "current": False,
            "employment_note": "",
        },
    ],
    "education": [
        {
            "university": "Binghamton University, State University of New York (SUNY)",
            "degree": "Master of Science, Computer Science, AI Specialization",
            "location": "Binghamton, NY",
            "graduation": "Expected Aug 2026",
        },
        {
            "university": "Gujarat Technological University (GTU)",
            "degree": "Bachelor of Engineering, Computer Engineering",
            "location": "Ahmedabad, India",
            "graduation": "Graduated Sep 2020",
        },
    ],
    "education_settings": {
        "primary_education_index": 0,
        "verified_gpa": "4.00/4.00",
        "coursework_selection": {
            "minimum": 2,
            "maximum": 4,
            "preferred_minimum": 2,
            "preferred_maximum": 3,
        },
        "verified_coursework": [
            "Database Systems",
            "Programming Languages",
            "Design and Analysis of Computer Algorithms",
            "Programming Systems and Tools",
            "Introduction to Machine Learning",
            "Programming for the Web",
            "Systems Programming",
            "Introduction to Computer Vision",
            "Introduction to Artificial Intelligence",
            "Natural Language Processing",
        ],
    },
    "projects": [
        {
            "story_id": "PROJ-01",
            "name": "JobPulse: Job Ingestion and Semantic Search Platform",
            "aliases": ["jobpulse"],
            "url": "https://github.com/kevalshah0612/jobpulse",
        },
        {
            "story_id": "PROJ-02",
            "name": "FraudSift: Transaction Analytics and Anomaly Detection",
            "aliases": ["fraudsift"],
            "url": "https://github.com/kevalshah0612/fraudsift",
        },
        {
            "story_id": "PROJ-03",
            "name": "FilingQuery: Citation-Grounded SEC Filing Retrieval",
            "aliases": ["filingquery"],
            "url": "https://github.com/kevalshah0612/filingquery",
        },
        {
            "story_id": "PROJ-04",
            "name": "EvalTrace: RAG Evaluation and CI Quality Gates",
            "aliases": ["evaltrace"],
            "url": "https://github.com/kevalshah0612/evaltrace",
        },
        {
            "story_id": "PROJ-05",
            "name": "ReviewBot: AI-Assisted Pull-Request Review",
            "aliases": ["reviewbot"],
            "url": "https://github.com/kevalshah0612/reviewbot",
        },
        {
            "story_id": "PROJ-06",
            "name": "Resume Agent: Evidence-Grounded Resume Automation",
            "aliases": ["resume agent", "resumeagent"],
            "url": "https://github.com/kevalshah0612/resume-agent",
        },
        {
            "story_id": "PROJ-07",
            "name": "JobFill AI: Browser-Based Application Automation",
            "aliases": ["jobfill", "jobfill ai"],
            "url": "https://github.com/kevalshah0612/jobfill-ai-extension",
        },
        {
            "story_id": "PROJ-08",
            "name": "Bistro AI: Structured AI Ordering Workflow",
            "aliases": ["bistro", "bistro ai"],
            "url": "https://github.com/kevalshah0612/bistro-ai",
        },
        {
            "story_id": "PROJ-09",
            "name": "AI-Assisted Engineering Workflow",
            "aliases": ["ai-assisted engineering workflow", "ai assisted engineering workflow"],
            "url": "",
        },
    ],
}


# ---------------------------------------------------------------------------
# Editable V1 resume contract
# ---------------------------------------------------------------------------
# These values are consumed by the prompts, Python validation, compact-to-full
# conversion, and rendering flow. Define them once here to prevent drift.
V1_CONFIG: dict[str, Any] = {
    "schema_version": "v1",
    "supported_modes": {
        "entry_swe": {
            "role_family": "software_engineering",
            "renderer_strategy_type": "Entry",
            "renderer_level": 2,
            "renderer_layout_profile": "professional_entry",
            "renderer_config_type": "backend",
            "summary_enabled": False,
            "summary_max_words": 0,
            "resume_section_order": ["education", "experience", "projects", "technical_skills"],
            "experience_search_priority": ["TA", "GHI", "TCS_SWE_II", "TCS_SWE_I"],
            "experience_display_order": ["TA", "GHI", "TCS_SWE_II", "TCS_SWE_I"],
            "bullet_counts": {"TA": 2, "GHI": 3, "TCS_SWE_II": 3, "TCS_SWE_I": 2},
            "project_count": 2,
            "project_bullets_each": 2,
            "show_gpa": True,
            "show_coursework": True,
        },
        "entry_aiml": {
            "role_family": "ai_ml_engineering",
            "renderer_strategy_type": "Entry",
            "renderer_level": 2,
            "renderer_layout_profile": "aiml_entry",
            "renderer_config_type": "aiml",
            "summary_enabled": False,
            "summary_max_words": 0,
            "resume_section_order": ["education", "experience", "projects", "technical_skills"],
            "experience_search_priority": ["TA", "GHI", "TCS_COMBINED"],
            "experience_display_order": ["TA", "GHI", "TCS_COMBINED"],
            "bullet_counts": {"TA": 2, "GHI": 3, "TCS_COMBINED": 3},
            "project_count": 3,
            "project_bullets_each": 2,
            "show_gpa": True,
            "show_coursework": True,
        },
        "mid_swe": {
            "role_family": "software_engineering",
            "renderer_strategy_type": "Mid",
            "renderer_level": 3,
            "renderer_layout_profile": "mid",
            "renderer_config_type": "backend",
            "summary_enabled": True,
            "summary_max_words": 40,
            "resume_section_order": ["summary", "experience", "projects", "education", "technical_skills"],
            "experience_search_priority": ["TCS_SWE_II", "TCS_SWE_I", "GHI", "TA"],
            "experience_display_order": ["TCS_SWE_II", "TCS_SWE_I", "TA", "GHI"],
            "bullet_counts": {"TCS_SWE_II": 4, "TCS_SWE_I": 2, "TA": 1, "GHI": 2},
            "project_count": 2,
            "project_bullets_each": 1,
            "show_gpa": False,
            "show_coursework": False,
        },
    },
    "writing_policy": {
        "tense": "past",
        "voice": "active",
        "target_bullet_words": "18-22",
        "hard_maximum_bullet_words": 24,
        "maximum_jd_keyword_units_per_bullet": 3,
        "maximum_performance_outcomes_per_bullet": 1,
        "maximum_essential_scope_values_per_bullet": 1,
        "one_result_group_per_bullet": True,
        "one_sentence_per_bullet": True,
        "em_dash_allowed": False,
        "first_person_allowed": False,
        "passive_voice_allowed": False,
        "filler_allowed": False,
        "buzzwords_allowed": False,
        "technology_inventory_bullets_allowed": False,
        "unsupported_facts_allowed": False,
        "cross_story_fact_mixing_allowed": False,
    },
    "skills_policy": {
        "maximum_categories": 5,
        "empty_categories_allowed": False,
        "duplicate_terms_allowed": False,
        "jd_irrelevant_terms_allowed": False,
        "unsupported_terms_allowed": False,
        "source": "MAPPER_PLAN.skills_plan only",
    },
    "schema_contract": {
        "top_level_keys": [
            "type",
            "summary",
            "coursework",
            "experience",
            "projects",
            "technical_skills",
            "bullet_checks",
        ],
        "experience_keys": ["id", "title", "company", "location", "dates", "bullets"],
        "project_keys": ["story_id", "name", "tech", "bullets"],
        "skills_keys": ["category", "skills"],
        "bullet_check_keys": [
            "ref",
            "story_id",
            "requirement_id",
            "alignment",
            "word_count",
            "questions_answered",
        ],
        "question_labels": ["what", "how", "with_what", "result", "amount"],
    },
    "render_order_presets": {
        "tcs_first": {
            "label": "TCS first",
            "deferred_role_ids": ["GHI"],
        },
        "ghi_first": {
            "label": "Internship/GHI first",
            "priority_role_ids": ["GHI"],
        },
    },
    "evidence_policies": [
        {
            "policy_id": "dated_ai_implementation_boundary",
            "restricted_role_ids": ["TCS_SWE_I", "TCS_SWE_II", "TCS_COMBINED"],
            "implementation_role_ids": ["GHI", "TA"],
            "project_implementation_allowed": True,
            # These concise reinforcements preserve the current high-salience
            # wording while keeping it editable beside the policy it enforces.
            "mapper_prompt_reinforcement": (
                "Never create a TCS DES for generative AI, LLMs, AI agents, agentic development, RAG, "
                "embeddings, vector search, prompt engineering, chatbots, conversational AI, dialog engines, "
                "model development, or AI-specific observability and analytics. Map all AI and ML "
                "implementation requirements to chronology-safe GHI, TA, or project evidence; if none is "
                "plausible, record the gap without asking a speculative TCS implementation question."
            ),
            "mapper_controller_reinforcement": (
                "Map AI and ML implementation requirements only to chronology-safe configured roles or "
                "projects; never create a speculative implementation DES for a restricted role."
            ),
            "composer_prompt_reinforcement": (
                "Enforce the candidate-specific AI chronology boundary as a final safety check, using the "
                "restricted and allowed roles defined by this policy."
            ),
            "instruction": (
                "The restricted roles may use verified, period-appropriate general engineering evidence and "
                "clearly labeled AI or machine-learning conceptual exposure only when a role-local story or "
                "chronology-safe approved DES explicitly confirms it. Never convert conceptual exposure into "
                "a claim that the candidate built, trained, customized, evaluated, integrated, served, operated, "
                "or launched an AI/ML system in a restricted role. Do not place generative-AI, LLM, AI-agent, "
                "agentic-development, RAG, embedding, vector-search, prompt-engineering, chatbot, conversational-AI, "
                "dialog-engine, model-development, model-customization, model-evaluation, model-serving, "
                "LLM-observability, prompt-metric, or conversation-analytics implementation work in a restricted "
                "role. Apply the same restriction to Slack, Microsoft Teams, web chat, notifications, tracing, or "
                "analytics when the JD frames them as parts of an AI assistant, agent, or conversational system. "
                "Map AI/ML implementation evidence only to an allowed configured experience role or project story."
            ),
        }
    ],
    "stage_reasoning_budgets": {
        "jd_analysis": 4096,
        "evidence_mapping": 8192,
        "resume_composition": 20480,
        "post_ats_audit": 8192,
        "post_optimizer": 6144,
    },
}


REQUESTS_DIR_NAME = "requests"
WORD_DIR_NAME = "Resume-word"
PDF_DIR_NAME = "Resume-pdf"
ARCHIVES_DIR_NAME = "archives"
DES_FACTS_FILE_NAME = "global_des_facts.md"

REQUESTS_DIR = ROOT / REQUESTS_DIR_NAME
WORD_DIR = ROOT / WORD_DIR_NAME
PDF_DIR = ROOT / PDF_DIR_NAME
DES_FACTS_PATH = ROOT / DES_FACTS_FILE_NAME

PROMPT_PROFILE_LABELS = {
    "v1": "V1",
    "stable": "Stable",
    "v3": "V3",
}
DEFAULT_PROMPT_PROFILE = "v1"


def _profile_key(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())


def _candidate_value(name: str, default: str = "") -> str:
    return str(CANDIDATE_PROFILE["candidate"].get(name) or default)


CANDIDATE_NAME = _candidate_value("name")
RESUME_STEM = _candidate_value("resume_stem") or re.sub(r"[^A-Za-z0-9]+", "_", CANDIDATE_NAME).strip("_")
PRIMARY_PHONE = _candidate_value("phone")
PRIMARY_EMAIL = _candidate_value("email")
CURRENT_LOCATION = _candidate_value("location")
LINKEDIN_URL = _candidate_value("linkedin_url")
LINKEDIN_DISPLAY = _candidate_value("linkedin_display")
GITHUB_URL = _candidate_value("github_url")
GITHUB_DISPLAY = _candidate_value("github_display")
PORTFOLIO_URL = _candidate_value("portfolio_url")
PORTFOLIO_DISPLAY = _candidate_value("portfolio_display")

VERIFIED_GRADUATE_COURSEWORK = tuple(
    str(item) for item in CANDIDATE_PROFILE["education_settings"].get("verified_coursework", [])
)
VERIFIED_GRADUATE_GPA = str(CANDIDATE_PROFILE["education_settings"].get("verified_gpa") or "")


def candidate_experience_profiles() -> list[dict[str, Any]]:
    return copy.deepcopy(CANDIDATE_PROFILE["experience"])


def candidate_experience_by_id(role_id: object) -> dict[str, Any] | None:
    key = _profile_key(role_id)
    if not key:
        return None
    for item in CANDIDATE_PROFILE["experience"]:
        known = {
            _profile_key(item.get("role_id")),
            _profile_key(item.get("resume_output_id")),
            *(_profile_key(alias) for alias in item.get("aliases", [])),
        }
        if key in known:
            return copy.deepcopy(item)
    return None


def candidate_role_id(
    role_id: object = "",
    company: object = "",
    title: object = "",
) -> str:
    direct = candidate_experience_by_id(role_id)
    if direct:
        return str(direct["role_id"])

    company_key = _profile_key(company)
    title_key = _profile_key(title)
    exact_matches: list[dict[str, Any]] = []
    alias_matches: list[dict[str, Any]] = []
    for item in CANDIDATE_PROFILE["experience"]:
        if (
            company_key
            and company_key == _profile_key(item.get("company"))
            and title_key == _profile_key(item.get("title"))
        ):
            exact_matches.append(item)
        searchable = {
            _profile_key(item.get("company")),
            _profile_key(item.get("title")),
            *(_profile_key(alias) for alias in item.get("aliases", [])),
        }
        # Accept configured aliases inside longer labels emitted by a model or
        # stored in an older resume (for example, "Global Health Impact
        # Project" for the configured "Global Health Impact" alias).
        if any(
            known
            and (
                known == company_key
                or known == title_key
                or (company_key and known in company_key)
                or (title_key and known in title_key)
            )
            for known in searchable
        ):
            alias_matches.append(item)

    matches = exact_matches or alias_matches
    return str(matches[0]["role_id"]) if matches else ""


def candidate_experience_profile(
    role_id: object = "",
    company: object = "",
    title: object = "",
) -> dict[str, Any] | None:
    """Return the canonical candidate experience row for a generated resume row."""

    resolved_id = candidate_role_id(role_id, company, title)
    return candidate_experience_by_id(resolved_id)


def candidate_experience_identities() -> dict[str, dict[str, str]]:
    keys = ("title", "company", "location", "dates")
    return {
        str(item["role_id"]): {key: str(item.get(key) or "") for key in keys}
        for item in CANDIDATE_PROFILE["experience"]
    }


def candidate_education_profile() -> list[dict[str, Any]]:
    """Return editable canonical education rows without exposing shared state."""

    return copy.deepcopy(CANDIDATE_PROFILE["education"])


def primary_education_profile() -> dict[str, Any]:
    education = CANDIDATE_PROFILE["education"]
    if not education:
        return {}
    try:
        index = int(CANDIDATE_PROFILE["education_settings"].get("primary_education_index", 0))
    except (TypeError, ValueError):
        index = 0
    if not 0 <= index < len(education):
        index = 0
    return copy.deepcopy(education[index])


DEFAULT_GRADUATION = str(primary_education_profile().get("graduation") or "")


def candidate_contact_line() -> str:
    candidate = CANDIDATE_PROFILE["candidate"]
    fields = candidate.get("contact_display_fields") or ["phone", "email", "linkedin_display"]
    return " | ".join(str(candidate.get(field) or "").strip() for field in fields if str(candidate.get(field) or "").strip())


def candidate_project_profiles() -> list[dict[str, Any]]:
    return copy.deepcopy(CANDIDATE_PROFILE["projects"])


def candidate_project_profile(story_id: object = "", name: object = "") -> dict[str, Any] | None:
    story_key = _profile_key(story_id)
    name_key = _profile_key(name)
    for item in CANDIDATE_PROFILE["projects"]:
        if story_key and story_key == _profile_key(item.get("story_id")):
            return copy.deepcopy(item)
        candidates = {
            _profile_key(item.get("name")),
            *(_profile_key(alias) for alias in item.get("aliases", [])),
        }
        if name_key and any(candidate and candidate in name_key for candidate in candidates):
            return copy.deepcopy(item)
    return None


# Compatibility map used by stable/V3 helpers. V1 project lookup uses the
# structured project catalog above.
PROJECT_URLS = {
    str(alias): str(project.get("url") or "")
    for project in CANDIDATE_PROFILE["projects"]
    for alias in project.get("aliases", [])[:1]
    if str(project.get("url") or "")
}


def v1_mode_config(mode: object) -> dict[str, Any] | None:
    value = V1_CONFIG["supported_modes"].get(str(mode or "").strip())
    return copy.deepcopy(value) if value else None


def validate_v1_configuration() -> None:
    """Fail early with an actionable message when an edited V1 profile drifts."""

    role_ids = [str(item.get("role_id") or "").strip() for item in CANDIDATE_PROFILE["experience"]]
    if not all(role_ids) or len(role_ids) != len(set(role_ids)):
        raise ValueError("Every CANDIDATE_PROFILE experience row needs a unique nonempty role_id.")
    known_roles = set(role_ids)
    for item in CANDIDATE_PROFILE["experience"]:
        missing_sources = set(item.get("source_role_ids", [])) - known_roles
        if missing_sources:
            raise ValueError(
                f"Experience {item['role_id']} has unknown source_role_ids: {sorted(missing_sources)}"
            )

    for mode, config in V1_CONFIG["supported_modes"].items():
        display_order = list(config.get("experience_display_order", []))
        search_order = list(config.get("experience_search_priority", []))
        bullet_roles = set(config.get("bullet_counts", {}))
        unknown_roles = (set(display_order) | set(search_order) | bullet_roles) - known_roles
        if unknown_roles:
            raise ValueError(f"V1 mode {mode} references unknown role IDs: {sorted(unknown_roles)}")
        if len(display_order) != len(set(display_order)):
            raise ValueError(f"V1 mode {mode} contains duplicate experience_display_order IDs.")
        if bullet_roles != set(display_order):
            raise ValueError(
                f"V1 mode {mode} bullet_counts keys must exactly match experience_display_order."
            )
        if int(config.get("project_count", 0)) < 1 or int(config.get("project_bullets_each", 0)) < 1:
            raise ValueError(f"V1 mode {mode} project counts must be positive integers.")

    projects = CANDIDATE_PROFILE["projects"]
    project_ids = [str(item.get("story_id") or "").strip() for item in projects]
    if not all(project_ids) or len(project_ids) != len(set(project_ids)):
        raise ValueError("Every configured project needs a unique nonempty story_id.")
    if any(not str(item.get("name") or "").strip() for item in projects):
        raise ValueError("Every configured project needs a nonempty name.")

    coursework = CANDIDATE_PROFILE["education_settings"]["coursework_selection"]
    minimum = int(coursework["minimum"])
    maximum = int(coursework["maximum"])
    preferred_minimum = int(coursework["preferred_minimum"])
    preferred_maximum = int(coursework["preferred_maximum"])
    if not (0 <= minimum <= preferred_minimum <= preferred_maximum <= maximum):
        raise ValueError(
            "coursework_selection must satisfy minimum <= preferred_minimum <= "
            "preferred_maximum <= maximum."
        )


def v1_runtime_configuration() -> dict[str, Any]:
    """Return the authoritative prompt/runtime V1 configuration."""

    validate_v1_configuration()
    return {
        "schema_version": V1_CONFIG["schema_version"],
        "candidate_name": CANDIDATE_NAME,
        "supported_modes": copy.deepcopy(V1_CONFIG["supported_modes"]),
        "locked_experience_identity": candidate_experience_identities(),
        "experience_story_boundaries": {
            str(item["role_id"]): list(item.get("story_prefixes", []))
            for item in CANDIDATE_PROFILE["experience"]
        },
        "combined_experience_sources": {
            str(item["role_id"]): list(item.get("source_role_ids", []))
            for item in CANDIDATE_PROFILE["experience"]
            if item.get("source_role_ids")
        },
        "project_catalog": [
            {
                "story_id": str(item.get("story_id") or ""),
                "name": str(item.get("name") or ""),
                "url": str(item.get("url") or ""),
            }
            for item in CANDIDATE_PROFILE["projects"]
        ],
        "primary_education": primary_education_profile(),
        "verified_gpa": VERIFIED_GRADUATE_GPA,
        "verified_coursework": list(VERIFIED_GRADUATE_COURSEWORK),
        "coursework_selection": copy.deepcopy(
            CANDIDATE_PROFILE["education_settings"]["coursework_selection"]
        ),
        "writing_policy": copy.deepcopy(V1_CONFIG["writing_policy"]),
        "skills_policy": copy.deepcopy(V1_CONFIG["skills_policy"]),
        "schema_contract": copy.deepcopy(V1_CONFIG["schema_contract"]),
        "evidence_policies": copy.deepcopy(V1_CONFIG["evidence_policies"]),
    }
