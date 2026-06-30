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
NVIDIA_MODEL=nvidia/nemotron-3-ultra-550b-a55b
NVIDIA_THINKING=true
NVIDIA_MAX_ATTEMPTS=5
NVIDIA_REASONING_BUDGET=49152
FALLBACK_TO_ANTHROPIC=false
ANTHROPIC_API_KEY=your_key
```

NVIDIA retries are artifact-based. PASS 1 retries only when parseable DES candidates are missing. PASS 2 and recruiter review retry only when valid JSON is missing. Application-question calls run once. Recruiter and hiring-manager LinkedIn messages are each limited to 300 characters; overlong messages are shortened locally and do not rerun the resume request. Use the per-tab **Stop** button to cancel the current NVIDIA stream or retry chain, then start that step again manually. Claude remains available through `PROVIDER_MODE=2`, but automatic NVIDIA-to-Claude fallback is disabled by default.

The per-tab model dropdown contains only these two NVIDIA models:

- `nvidia/nemotron-3-ultra-550b-a55b`
- `deepseek-ai/deepseek-v4-pro`

Each model has `Thinking ON` and `Thinking OFF` options. Nemotron uses streaming with `enable_thinking`; its reasoning budget is sent only when thinking is on. DeepSeek follows its NVIDIA profile with non-streaming output and the `thinking` chat-template setting. The same `NVIDIA_API_KEY` and base URL are used for every option. Selection is per application tab and is locked while that tab is running, so concurrent tabs can safely use different profiles.

`NVIDIA_MODEL` and `NVIDIA_THINKING` define the initial dropdown choice. To add another model later, add one `NvidiaModelSpec` entry in `pipeline.py`; the ON/OFF dropdown choices are generated automatically.

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

The tab uses one large scrollable `Output` area with an artifact dropdown. Entries are grouped as `Model Process`, `Output`, `LinkedIn`, `Input`, or `Log`, so any saved result can be reopened without searching the request folder. After PASS 1, the left Job Description box changes to the organized missing-coverage and DES view; the original JD remains saved and continues to drive every later model call.

The prompt dropdown is per tab:

- `Stable` is the default production flow and uses `main_flow/`.
- `V1` uses `v1_experimental_flow/prompts/prompt.md`, `prompt_short.md`, `Story.md`, and `hotdog.md`.
- `V2` uses `v2_experimental_flow/prompts/prompt.md`, `prompt_short.md`, `Story.md`, and `hotdog.md`.
- In V1/V2, `Prompt` sends company, JD, location, role type, and optional DES and accepts compact resume JSON. Python adds locked contact, education, dates, links, and renderer fields. `Hotdog` sends JD plus the generated JSON for a blind cleanup pass.

LinkedIn outreach is role-specific rather than generic:

- Recruiter message: names the exact title and company, uses one supported proof point, and politely asks for the correct recruiter or for the resume to be passed along when appropriate.
- Hiring-manager message: names the exact title and company, connects one supported proof point to a JD priority, and asks one concise question about the team or role.
- Each message has an independent 300-character maximum and uses ASCII punctuation.

`Load Request` selects an existing `requests/<request_id>/` folder and restores its company, title, JD, DES, approval, questions, PASS 1 output, cost, and available JSON artifacts into the current tab. Recruiter, Final QA, Questions, DOCX, and PDF can then continue from the best saved artifact without rerunning earlier steps. `Open Folder` opens the active request folder in File Explorer.

Manual path:

1. Paste company, title, JD, words, and optional DES evidence.
2. Click `PASS 1`.
3. Review the organized DES Candidate Bank.
4. Approve DES with `Approved: DES 1 to 6`, `1,2,3`, or `Confirm`.
5. Click `Generate JSON`.
6. Optional: click `Recruiter`.
7. Optional: click `Final QA` for the three-stage evidence-safe final review.
8. Click `DOCX`.
9. Review the DOCX.
10. Click `PDF`.

Fast path:

1. Paste the input.
2. Click `Auto JSON`.
3. The app runs PASS 1, approves all DES candidates, and generates JSON.
4. Recruiter review remains optional.

## Final QA

`Final QA` stays inside the current application tab and always uses the configured NVIDIA endpoint. It never calls Anthropic. One click runs three dependent NVIDIA stages in order:

1. **Audit:** read-only recruiter and ATS review of the selected input JSON.
2. **Repair:** create an evidence-safe candidate JSON in memory. This is intermediate work, not a deliverable.
3. **Final scan:** independently verify the candidate and produce the usable Final QA JSON.

The latest JSON is selected automatically: Final QA JSON, then recruiter JSON, then PASS 2 JSON. `manager.py` generates a render profile containing the exact level, layout, section order, experience order, project order, TA placement, skill rows, and bullet counts. NVIDIA receives the source JSON, JD, and this profile; no intermediate DOCX or PDF is generated.

Identity and renderer-locked values are deterministically restored from the input JSON if the model accidentally changes them. Remaining structural changes, such as altered list lengths, role order, project order, or bullet counts, are rejected and written clearly to the Final QA process file. The accepted JSON becomes the DOCX source, so document generation still occurs only once.

Final QA saves only two new files:

- `11_final_qa_process.txt`: render plan, audit explanation, repair summary, final-scan summary, restored-lock report, or exact failure reason.
- `12_final_qa_output.json`: final validated resume JSON.

Older request folders containing separate source, profile, audit, repair, and scan files remain compatible. The GUI combines them under `Model Process | Final QA`.

The per-tab `Stop` button stops the sequence. The status board shows `Final QA 1/3`, `2/3`, and `3/3`, allowing concurrent applications to remain visible from the main window.

Application questions:

1. Paste salary, sponsorship, work authorization, or other application questions into `Application Questions`.
2. Click `Answer Questions`.
3. The app uses Final QA JSON when available, then recruiter JSON, then the PASS 2 final JSON.
4. Answers are short, human, and grounded in the JD plus resume JSON.

## DES Display

PASS 1 model output is saved exactly as returned by the model:

```text
requests/<request_id>/02_pass1_des_process.txt
```

The left Job Description area displays the same DES candidates in a readable format:

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
00_request_details.txt
01_job_description.txt
02_pass1_des_process.txt
03_des_approval.txt
04_resume_generation_process.txt
05_resume_output.json
06_recruiter_review_process.txt
07_recruiter_resume_output.json
08_application_questions.txt
09_application_answers.txt
10_linkedin_outreach.txt
10_recruiter_linkedin_message.txt
10_hiring_manager_linkedin_message.txt
10_recruiter_hm_search_strings.txt
11_final_qa_process.txt
12_final_qa_output.json
13_docx_build_log.txt
14_pdf_archive_log.txt
costs.json
```

## CLI

Build DOCX:

```powershell
python manager.py requests/company_timestamp/07_recruiter_resume_output.json "Company Name"
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

The GUI tracks estimated cost per tab and session. Claude calls use token usage returned by the Anthropic API. NVIDIA calls record the selected model and thinking mode. Streaming models may not return token usage, so the app can show `$0.00` when usage metadata is unavailable.

To show an estimated remaining balance, set this in `pipeline_config.json`:

```json
{
  "manual_starting_balance_usd": 5
}
```

## Project Summary

Built a Python/Tkinter resume automation agent that converts job descriptions into evidence-grounded resume JSON, supports DES approval or automated DES acceptance, optional recruiter review, three-stage NVIDIA final QA with renderer-locked structure, application-question answers, per-tab status tracking, API cost estimates, and DOCX/PDF generation with organized output folders.

## Security

- Never commit API keys.
- Keep `.env` and `pipeline_config.json` local.
- Generated requests, resumes, PDFs, and archives are ignored by Git.
