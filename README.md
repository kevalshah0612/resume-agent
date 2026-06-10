# Resume Agent

Resume Agent is a desktop workflow for tailoring a resume to a job description using a compact multi-agent LLM process. It turns a pasted JD into a grounded resume JSON, runs an optional recruiter-style review, builds a DOCX, and archives the final PDF.

## What It Does

- Accepts company, role title, job description, keywords, mode overrides, and optional DES evidence.
- Runs a resume-generation agent that reads the prompt and story bank.
- Produces a short DES Candidate Bank instead of a long audit.
- Lets the user approve DES evidence with simple text such as `Approved: DES 1 to 6` or `1,2,3`.
- Generates a final resume JSON.
- Optionally runs a recruiter-review agent to fix red flags and validate the JSON.
- Builds a DOCX resume.
- Converts the reviewed DOCX to PDF, archives the PDF, and deletes the DOCX.
- Supports concurrent applications using GUI tabs.

## Agent Flow

The system uses prompt files in `new_flow/` as the agent instructions and evidence source.

### 1. Resume Generation Agent

Files:

- `new_flow/prompt.md`
- `new_flow/prompt_short.md`
- `new_flow/story.md`

Purpose:

- Reads the JD and story bank.
- Classifies role fit, keywords, evidence coverage, and gaps.
- Outputs a compact DES Candidate Bank.
- Generates the final resume JSON after DES approval.

PASS 1 is intentionally short:

```text
COVERAGE SUMMARY
DES CANDIDATE BANK
APPROVAL
```

Each DES line is formatted like:

```text
DES 1 | keyword: ... | use when: ... | bullet: ... | story/context: ... | number: ... | safe wording: ...
```

### 2. Recruiter Review Agent

Files:

- `new_flow/recruiter.md`
- `new_flow/recruiter_short.md`

Purpose:

- Reviews the generated resume JSON like a recruiter and hiring manager.
- Checks JD coverage, top-bullet strength, skills traceability, red flags, and schema validity.
- Produces the final recruiter-reviewed JSON used for DOCX generation.

### 3. Document Manager

File:

- `manager.py`

Purpose:

- Converts final JSON to DOCX.
- Converts DOCX to PDF using Microsoft Word first, then LibreOffice fallback.
- Archives PDFs under `archives/YYYY-MM-DD/`.
- Deletes the working DOCX after PDF conversion.
- Clears generated DOCX/PDF files from the project root.

## How To Use

### Setup

Install dependencies:

```powershell
pip install -r requirements.txt
```

Set your Anthropic API key:

```powershell
$env:ANTHROPIC_API_KEY="your_key_here"
```

Optional local config:

```powershell
Copy-Item pipeline_config.example.json pipeline_config.json
```

Do not commit `pipeline_config.json`; it is ignored because it may contain secrets.

### Start The App

```powershell
python gui.py
```

### GUI Workflow

1. Paste the company, title, JD, optional words, optional mode, and optional DES.
2. Click `Run PASS 1`.
3. Review the compact DES Candidate Bank.
4. Approve DES evidence:

```text
Approved: DES 1 to 6
```

or:

```text
1,2,3
```

or:

```text
Confirm
```

5. Click `Generate JSON`.
6. Optional: click `Recruiter Review`.
7. Click `Build DOCX`.
8. Review and save the DOCX in Word.
9. Click `PDF + Archive`.

## Concurrent Applications

The GUI supports multiple applications in one window.

- `New Application Tab` starts a separate job.
- `Duplicate Current` copies the current tab inputs into a new tab.
- Each tab runs independently in a background thread.
- You can run PASS 1 for multiple companies at the same time.

## Mode Behavior

Mode is optional and blank by default.

If blank, the prompt infers the resume type and layout from the JD.

Use Mode only when you want to force a direction:

- `mid + backend`
- `entry + backend`
- `mid + fullstack`
- `aiml_entry`
- `aitool_mid`
- `internship`

Keywords such as `Kafka`, `MySQL`, `Linux`, or `Solr` should go in Words, not Mode.

## Saved Files

Each application is saved under:

```text
requests/<company>_<timestamp>/
```

Typical files:

- `00_request.txt`
- `01_jd.txt`
- `02_pass1_des_bank.txt`
- `03_approval.txt`
- `04_final_raw.txt`
- `05_final_resume.json`
- `06_recruiter_raw.txt`
- `07_recruiter_final_resume.json`
- `06_docx_build.txt`
- `07_pdf_archive.txt`

These generated folders are ignored by Git.

## CLI Commands

Build DOCX from JSON:

```powershell
python manager.py requests/company_timestamp/07_recruiter_final_resume.json "Company Name"
```

Convert DOCX to PDF and archive:

```powershell
python manager.py Keval_Shah_Company_Resume.docx "Company Name"
```

Clear root DOCX/PDF files:

```powershell
python manager.py clear
```

## Quality Controls

The project includes several guardrails:

- DES approval before final JSON.
- Story-bank evidence grounding.
- Recruiter-review pass.
- JSON schema validation.
- Banned-key detection.
- Duplicate opening-verb repair.
- Bullet period cleanup.
- DOCX/PDF archive automation.

## Resume Project Description

You can describe this project as:

> Built a desktop AI resume-tailoring agent that converts job descriptions into evidence-grounded resume JSON, uses DES approval to prevent hallucinated claims, runs a recruiter-style validation pass, and automates DOCX/PDF generation with archival workflow support.

Short bullet version:

> Developed a multi-agent resume automation tool using Python, Anthropic API, Tkinter, and python-docx, supporting JD analysis, DES evidence approval, recruiter review, JSON validation, DOCX generation, and PDF archival.

## Security Notes

- Never commit API keys.
- Use `ANTHROPIC_API_KEY` as an environment variable.
- `pipeline_config.json`, generated resumes, PDFs, archives, and request logs are ignored by Git.
