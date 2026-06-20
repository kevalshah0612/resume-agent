# Resume Agent

Desktop resume automation for turning a pasted job description into resume JSON, optional recruiter-reviewed JSON, DOCX, PDF, and short application-question answers.

## Providers

Only two providers are supported:

- `PROVIDER_MODE=1` = NVIDIA endpoint through the OpenAI SDK
- `PROVIDER_MODE=2` = direct Claude through the Anthropic SDK

Create `.env` from the example:

```powershell
Copy-Item .env.example .env
```

NVIDIA setup:

```text
PROVIDER_MODE=1
NVIDIA_API_KEY=your_nvidia_api_key
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL=nvidia/nemotron-3-super-120b-a12b
NVIDIA_MAX_ATTEMPTS=5
NVIDIA_REASONING_BUDGET=16384
FALLBACK_TO_ANTHROPIC=false
ANTHROPIC_API_KEY=your_key
```

NVIDIA retries are artifact-based. PASS 1 retries only when parseable DES candidates are missing. PASS 2 and recruiter review retry only when valid JSON is missing. Application-question calls run once. LinkedIn messages over 300 characters are shortened locally and do not rerun the resume request. Use the per-tab **Stop AI** button to cancel the current NVIDIA stream or retry chain, then start that step again manually. Claude remains available through `PROVIDER_MODE=2`, but automatic NVIDIA-to-Claude fallback is disabled by default.

To change NVIDIA models, edit only:

```text
NVIDIA_MODEL=nvidia/your-other-model
```

Claude-only setup:

```text
PROVIDER_MODE=2
ANTHROPIC_API_KEY=your_key
```

## Setup

```powershell
pip install -r requirements.txt
python gui.py
```

Local secret/config files are ignored by Git:

- `.env`
- `pipeline_config.json`

## GUI Flow

Each tab is one application. Tabs run independently in background threads.

Manual path:

1. Paste company, title, JD, words, mode, and optional DES evidence.
2. Click `Run PASS 1`.
3. Review the organized DES Candidate Bank.
4. Approve DES with `Approved: DES 1 to 6`, `1,2,3`, or `Confirm`.
5. Click `Generate JSON`.
6. Optional: click `Recruiter Review`.
7. Click `Build DOCX`.
8. Review the DOCX.
9. Click `PDF + Archive`.

Fast path:

1. Paste the input.
2. Click `Auto JSON`.
3. The app runs PASS 1, approves all DES candidates, and generates JSON.
4. Recruiter review remains optional.

Application questions:

1. Paste salary, sponsorship, work authorization, or other application questions into `Application Questions`.
2. Click `Answer Questions`.
3. The app uses recruiter JSON if available; otherwise it uses the PASS 2 final JSON.
4. Answers are short, human, and grounded in the JD plus resume JSON.

## DES Display

PASS 1 raw output is saved exactly as returned by the model:

```text
requests/<request_id>/02_pass1_des_bank.txt
```

The GUI displays the same DES candidates in a readable format:

```text
DES 1
  Keyword: ...
  Use when: ...
  Bullet: ...
  Story/context: ...
  Number: ...
  Safe wording: ...
```

The raw PASS 1 text is still used for PASS 2 so formatting the display does not weaken the model flow.

## Status Tracking

Every request gets a readable ID:

```text
<company>_<title>_<timestamp>
```

The top status board shows:

- request ID
- company
- title
- current stage
- tab cost

Double-click a row to jump to that tab. `Print Status` writes the same summary to PowerShell.

Model log lines also include request ID, company, and title, so concurrent jobs are easier to trace.

## Output Folders

Generated resume documents are not stored in the project root.

- DOCX files: `Resume-word/`
- final PDFs: `Resume-pdf/`
- PDF archive copies: `Resume-pdf/archives/YYYY-MM-DD/`
- request logs and JSON: `requests/<request_id>/`

The manager deletes the working DOCX after successful PDF conversion.

## Saved Request Files

Typical request folder:

```text
00_request.txt
01_jd.txt
02_pass1_des_bank.txt
03_approval.txt
04_final_raw.txt
05_final_resume.json
06_recruiter_raw.txt
07_recruiter_final_resume.json
08_application_questions.txt
09_application_answers.txt
costs.json
```

## CLI

Build DOCX:

```powershell
python manager.py requests/company_timestamp/07_recruiter_final_resume.json "Company Name"
```

Convert DOCX to PDF and archive:

```powershell
python manager.py Resume-word/Keval_Shah_Company_Resume.docx "Company Name"
```

Clear generated DOCX/PDF files:

```powershell
python manager.py clear
```

## Cost Tracking

The GUI tracks estimated cost per tab and session. Claude calls use token usage returned by the Anthropic API. NVIDIA streaming calls may not return token usage, so the app records provider/model but can show `$0.00` when usage metadata is unavailable.

To show an estimated remaining balance, set this in `pipeline_config.json`:

```json
{
  "manual_starting_balance_usd": 5
}
```

## Project Summary

Built a Python/Tkinter resume automation agent that converts job descriptions into evidence-grounded resume JSON, supports DES approval or automated DES acceptance, optional recruiter review, application-question answers, per-tab status tracking, API cost estimates, and DOCX/PDF generation with organized output folders.

## Security

- Never commit API keys.
- Keep `.env` and `pipeline_config.json` local.
- Generated requests, resumes, PDFs, and archives are ignored by Git.
