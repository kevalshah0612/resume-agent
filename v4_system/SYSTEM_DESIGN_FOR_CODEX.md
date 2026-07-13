# Codex Build Guide — Evidence-Grounded Resume Prompt System

Build the system from these files. Do not copy business rules into application code or duplicate them across prompts.

## Canonical files

### V4 filename migration

The legacy one-step V4 file `v4_system/JD.md` is retired. Its replacement is the supplied
`prompts/01_JD_Analyzer.md`, which is the only JD-analyzer prompt V4 may load. The contents
are different, so this is a prompt-contract migration rather than a filename alias. Do not
restore or read `JD.md` in the V4 runtime.

- `system_config.json` — single source of truth for model settings, modes, priorities, DES, counts, scoring, writing rules, and validation gates.
- `prompts/01_JD_Analyzer.md` — JD Analyzer prompt supplied by the user, with its prior error branch replaced by a normal empty-result contract.
- `prompts/02_Story_Mapper.md` — keyword mapping, story selection, project selection, and DES planning.
- `prompts/03_Experience_Writer.md` — experience bullets only.
- `prompts/04_Project_Writer.md` — project bullets only.
- `prompts/05_Validator_Repair.md` — final validation and repair.
- `schemas/*.schema.json` — strict guided-JSON output contracts; do not recreate these in application code.
- `candidate_profile.json` — locked candidate identity, employment, and education.
- `story.md` — canonical approved story evidence.
- `approved_des_evidence.json` — persistent candidate-approved technical keyword evidence.

Future policy changes must be made in `system_config.json`. Prompt files should describe behavior generically and read values from the injected configuration.

## Call architecture

Use a brand-new NVIDIA chat context for every call. Never append stages to one conversation.

```text
Call 1: JD Analyzer
    input: complete JD
    output: JD_ANALYSIS

Call 2: Story Mapper
    input: config + JD analysis + candidate profile + story catalog + prior DES approvals
    output: MAPPER_PLAN

If mapper status = des_required:
    show numbered DES questions and stop
    parse candidate reply
    persist approvals
    rerun Call 2 in a new context

Call 3A: Experience Writer ┐
                           ├ run concurrently in separate new contexts
Call 3B: Project Writer    ┘

Call 4: Validator/Repair
    input: all authoritative sources + both writer outputs
    output: final repaired resume content

```

This is four stages and five prompt files because Experience and Project writing are intentionally separate.
The Mapper is the only DES gate. Validator/Repair returns only `valid` or
`repaired` and never creates a late user pause.

## DOCX and PDF rendering

Document rendering is a deterministic post-processing step and does not add a model call.

- Keep `05_resume_output.json` unchanged as the validated V4 model output.
- Build `06_v4_renderer_input.json` by combining that output with locked identity and education from `candidate_profile.json`.
- Convert V4 bullet objects to plain bullet strings only in this renderer input.
- Render DOCX with the existing `v3_experimental_flow/manager_Updated.py` file.
- Convert and archive PDF with the same V3 renderer file.
- Never use the renderer input as evidence or feed it back into Mapper, Writers, or Validator.

## Runtime inputs and outputs

### JD Analyzer

Input:

```json
{"JOB_DESCRIPTION":"complete page text"}
```

Output: use the exact guided schema associated with `prompts/01_JD_Analyzer.md`, including role, level, filters, and Buckets 5–2.

### Story Mapper

Input keys:

```text
SYSTEM_CONFIG
JD_ANALYSIS
CANDIDATE_PROFILE
STORY_CATALOG
APPROVED_DES_EVIDENCE
DES_REPLY
```

Output keys:

```text
status
resume_mode
role
level
keyword_plan
experience_plan
project_plan
skills_keyword_ids
des_questions
coverage
```

### Experience Writer

Input keys:

```text
SYSTEM_CONFIG
CANDIDATE_PROFILE
MAPPER_PLAN
SELECTED_EXPERIENCE_STORIES
APPROVED_DES_EVIDENCE
```

Output keys:

```text
experience
used_keyword_ids
unused_keyword_ids
```

### Project Writer

Input keys:

```text
SYSTEM_CONFIG
MAPPER_PLAN
SELECTED_PROJECT_STORIES
APPROVED_DES_EVIDENCE
```

Output keys:

```text
projects
used_keyword_ids
unused_keyword_ids
```

### Validator/Repair

Input keys:

```text
SYSTEM_CONFIG
CANDIDATE_PROFILE
JD_ANALYSIS
MAPPER_PLAN
SELECTED_STORIES
APPROVED_DES_EVIDENCE
EXPERIENCE_OUTPUT
PROJECT_OUTPUT
```

Output keys:

```text
status
summary
experience
projects
technical_skills
coverage
des_questions
repairs
```

The orchestrator scopes the persisted DES bank before Mapper input. Only a
current-JD technical keyword is visible, and reuse requires the same normalized
keyword and story. The Mapper is the only DES owner; Writers and the final
Validator never create a second or late approval pause.

The selected resume mode controls Summary behavior. A disabled mode emits an
empty string. An enabled mode emits one paragraph within that mode's configured
word range.

Technical Skills is not copied from the story bank or candidate inventory. It
is resolved only from `MAPPER_PLAN.skills_keyword_ids`, using the exact current
JD Analyzer spelling and punctuation once across the whole section. Eligibility
and whether all eligible current-JD terms are included are configuration-driven.

## Story loading

Parse `story.md` deterministically by story heading. Story IDs are headings such as `TCS-II-01`, `GHI-04`, and `PROJ-03`.

For Mapper input, send a compact catalog containing:

```text
story_id
role_id
story title
engineering story
resume keywords
approved metrics
```

For each Writer, send only stories selected by the Mapper. Do not send all stories or the raw JD to Writers.

## DES parser

Parse approvals in application code, not with another model call.

Accept:

```text
DES 1 to 4
1 to 4
DES 1-4
1-4
DES 1, 3, 5
1, 3, 5
Any accepted range/list followed by English text
```

Every referenced number becomes an approval with:

```json
{
  "keyword": "",
  "story_id": "mapper proposed closest story",
  "confidence": 1.0,
  "source": "candidate_des_approval",
  "note": "optional trailing English",
  "approved_at": "ISO-8601 timestamp"
}
```

Append it to `approved_des_evidence.json`. A later application should reuse the approval when the same normalized keyword and story are relevant.

Do not ask DES for nontechnical competencies or configured exempt practices. Approval authorizes the technology in the proposed story but does not authorize new metrics or outcomes.

## Guided JSON

Load the matching strict schema from `schemas/` for each prompt. Set it as NVIDIA guided JSON. Do not duplicate or reconstruct schemas in application code.

The JD schema must require Buckets `5`, `4`, `3`, and `2` and must not include an error branch.

## Recovery

- Retry only network, timeout, rate-limit, truncation, invalid-JSON, and schema failures.
- Preserve completed stage outputs as checkpoints.
- Never show raw exceptions, `failed`, or `needs review` to the user.
- After retry exhaustion, keep the checkpoint and schedule an automatic retry.
- The only intentional user pause is `des_required`.
- Never use Anthropic fallback unless configuration is explicitly changed.

## Runtime checks before and after model calls

Before calls:

- Validate required input keys.
- Load config once and inject the same immutable snapshot into all calls for that application.
- Hash every prompt and config snapshot for diagnostics.

After calls:

- Validate that the model returned JSON matching the current stage schema.
- Do not reject a valid stage-shaped JSON response for bullet wording, word-count arithmetic, metric wording, opening verbs, or other writing-quality judgments in Python.
- Let the prompts and Validator/Repair stage handle resume-writing quality.

Do not implement resume-writing decisions in code. Mapping, writing, and repair remain prompt responsibilities governed by configuration.

## Required diagnostics

Record per stage without secrets:

```text
application_id
prompt path and SHA-256
config SHA-256
model and settings
input/output schema version
API calls and retries
response time
token usage
schema result
stage status
```

Never record API keys or authorization headers.
