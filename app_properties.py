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
TCS_II_EMPLOYMENT_NOTE = "On approved academic leave in Binghamton, NY for M.S. in Computer Science, AI Specialization"
GHI_EMPLOYMENT_NOTE = ""

V1_PROJECT_URLS = {
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

REQUESTS_DIR = ROOT / REQUESTS_DIR_NAME
WORD_DIR = ROOT / WORD_DIR_NAME
PDF_DIR = ROOT / PDF_DIR_NAME

PROMPT_PROFILE_LABELS = {
    "stable": "Stable",
    "v1": "V1",
    "v2": "V2",
}
DEFAULT_PROMPT_PROFILE = "v1"


def candidate_contact_line() -> str:
    return f"{PRIMARY_PHONE} | {PRIMARY_EMAIL} | {LINKEDIN_DISPLAY}"
