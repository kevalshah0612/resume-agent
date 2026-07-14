from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).parent

CANDIDATE_NAME = "Keval Shah"
RESUME_STEM = "Keval_Shah"

PRIMARY_PHONE = "(518) 328-3697"
PRIMARY_EMAIL = "keval.shah098@gmail.com"
PREVIOUS_PHONE = "(607) 235-1181"
PREVIOUS_EMAIL = "keval.shah61298@gmail.com"

CURRENT_LOCATION = "New York, NY"
LINKEDIN_URL = "https://www.linkedin.com/in/keval-shah0612"
LINKEDIN_DISPLAY = "linkedin.com/in/keval-shah0612"
GITHUB_URL = "https://github.com/kevalshah0612"
GITHUB_DISPLAY = "github.com/kevalshah0612"

DEFAULT_BINGHAMTON_GRADUATION = "Expected Aug 2026"
GUJARAT_GRADUATION = "Graduated Sep 2020"
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
    "stable": "Stable",
    "v3": "V3",
}
DEFAULT_PROMPT_PROFILE = "stable"


def candidate_contact_line() -> str:
    return f"{PRIMARY_PHONE} | {PRIMARY_EMAIL} | {LINKEDIN_DISPLAY}"
