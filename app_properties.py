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
}


def candidate_contact_line() -> str:
    return f"{PRIMARY_PHONE} | {PRIMARY_EMAIL} | {LINKEDIN_DISPLAY}"
