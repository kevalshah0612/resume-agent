from __future__ import annotations

import copy
import re
from pathlib import Path


ROOT = Path(__file__).parent

CANDIDATE_PROFILE = {
    "schema_version": "candidate_profile_v1",
    "candidate": {
        "name": "Keval Shah",
        "location": "New York, NY",
        "phone": "(607) 235-1181",
        "email": "keval.shah098@gmail.com",
    },
    "experience": [
        {
            "role_id": "TA",
            "resume_output_id": "TA",
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
}

# Verified from the Binghamton University unofficial transcript supplied by the candidate.
# Resume prompts may select only the smallest JD-relevant subset of these courses.
VERIFIED_GRADUATE_COURSEWORK = (
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
)
VERIFIED_GRADUATE_GPA = "4.00/4.00"

CANDIDATE_NAME = CANDIDATE_PROFILE["candidate"]["name"]
RESUME_STEM = "Keval_Shah"

PRIMARY_PHONE = CANDIDATE_PROFILE["candidate"]["phone"]
PRIMARY_EMAIL = CANDIDATE_PROFILE["candidate"]["email"]
PREVIOUS_PHONE = "(607) 235-1181"
PREVIOUS_EMAIL = "keval.shah61298@gmail.com"

CURRENT_LOCATION = CANDIDATE_PROFILE["candidate"]["location"]
LINKEDIN_URL = "https://www.linkedin.com/in/keval-shah0612"
LINKEDIN_DISPLAY = "linkedin.com/in/keval-shah0612"
GITHUB_URL = "https://github.com/kevalshah0612"
GITHUB_DISPLAY = "github.com/kevalshah0612"

DEFAULT_BINGHAMTON_GRADUATION = CANDIDATE_PROFILE["education"][0]["graduation"]
GUJARAT_GRADUATION = CANDIDATE_PROFILE["education"][1]["graduation"]
TCS_II_EMPLOYMENT_NOTE = ""
GHI_EMPLOYMENT_NOTE = ""

PROJECT_URLS = {
    "jobpulse": "https://github.com/kevalshah0612/jobpulse",
    "fraudsift": "https://github.com/kevalshah0612/fraudsift",
    "reviewbot": "https://github.com/kevalshah0612/reviewbot",
    "filingquery": "https://github.com/kevalshah0612/filingquery",
    "evaltrace": "https://github.com/kevalshah0612/evaltrace",
    "resume agent": "https://github.com/kevalshah0612/resume-agent",
    "jobfill": "https://github.com/kevalshah0612/jobfill-ai-extension",
    "bistro": "https://github.com/kevalshah0612/bistro-ai",
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


def candidate_experience_profile(
    role_id: object = "",
    company: object = "",
    title: object = "",
) -> dict | None:
    """Return the canonical candidate experience row for a generated resume row."""

    role_key = _profile_key(role_id)
    company_key = _profile_key(company)
    title_key = _profile_key(title)

    if role_key == "tcs":
        role_key = "tcssweii" if title_key.endswith("ii") else "tcsswei"

    if role_key:
        for item in CANDIDATE_PROFILE["experience"]:
            known_keys = {
                _profile_key(item.get("role_id")),
                _profile_key(item.get("resume_output_id")),
            }
            if role_key in known_keys:
                return copy.deepcopy(item)

    for item in CANDIDATE_PROFILE["experience"]:
        item_company = _profile_key(item.get("company"))
        item_title = _profile_key(item.get("title"))
        if company_key and company_key == item_company and title_key == item_title:
            return copy.deepcopy(item)

    if "binghamtonuniversity" in company_key or "teachingassistant" in title_key:
        return copy.deepcopy(CANDIDATE_PROFILE["experience"][0])
    if "globalhealthimpact" in company_key:
        return copy.deepcopy(CANDIDATE_PROFILE["experience"][1])
    if "tataconsultancyservices" in company_key:
        index = 2 if title_key.endswith("ii") else 3
        return copy.deepcopy(CANDIDATE_PROFILE["experience"][index])
    return None


def candidate_education_profile() -> list[dict]:
    """Return editable canonical education rows without exposing shared state."""

    return copy.deepcopy(CANDIDATE_PROFILE["education"])


def candidate_contact_line() -> str:
    return f"{PRIMARY_PHONE} | {PRIMARY_EMAIL} | {LINKEDIN_DISPLAY}"
