Read the project files first:

1. `prompt.md`
2. `story.md`

Follow `prompt.md` exactly. Use `story.md` as the proof bank, not the resume identity. The JD decides the resume identity.

Do not print Thinking, Reading documents, scratchpad, tool notes, or hidden reasoning.

Use only the current run input and visible earlier messages in this same active chat when relevant. Do not use saved memory, prior chats, old resumes, or `base.json`.

Input for this run:

Company:
JD:
Title: optional, default `Software Engineer` unless JD clearly states a more exact title
Words: optional
Mode: optional
Des: optional

Mode examples:

* `entry + backend`
* `mid + fullstack`
* `internship`
* `aiml_entry`
* `aitool_mid`
* `backend`
* `entry`
* `mid`

Workflow:

1. First run PASS 1 only
2. I may approve DES IDs, for example `Apply DES-1, DES-3`, `Apply DES-4 fallback`, or `Skip DES-2`
3. If I approve a DES ID, treat it as true, interview-defensible, high-priority current-run evidence
4. Place approved DES in professional experience bullets first when it unlocks a minimum, responsibility, or ownership term
5. Do not write final JSON until I reply `CONFIRM`

PASS 1 must include:

1. Source verification, one line
2. Input quality gate
3. Visa check
4. Recruiter screen-in gate with red flags
5. Call-pile test and DONE-IT / CAN-DO-IT-HERE classification
6. JD problem thesis, role mode, layout profile, and strategy
7. JD sentence coverage table
8. Keyword placement table
9. Missing/partial evidence with DES Candidate Bank
10. Final resume slot plan
11. Approval box
12. `CHECKPOINT: Mode/schema/JD-stack/DES/slot-plan validation = PASS or RISK`

Dynamic JD-first rule:
Extract `JD_ROLE_IDENTITY`, `JD_PRIMARY_STACK`, `JD_SECONDARY_STACK`, `JD_ACTION_VERBS`, minimum sentences, responsibility sentences, ownership signals, and domain signals from the current JD. Make the summary, skills row 1, first experience bullet, second experience bullet, and selected projects match that exact JD identity.

Screen-in proof rule:
The top third must answer: I have done the closest version of this job, at similar complexity or production level, and can do it again for this company. Do not keyword dump. Show problem + how solved + scope/result. Enforce top-signal ranking and first-two-bullet gates: bullet 1 = closest JD core work, bullet 2 = production/risk/scale/ownership reducer. JD priority beats metric size.

DES Candidate Bank rule:
DES expansion limit: approved DES may be polished but must not add new tools, tests, metrics, domains, ownership, or outcomes beyond current DES/story evidence.
Do not ask me to fill blank DES forms first. Generate suggested resume wording for missing or partial JD terms. I will approve using IDs.

Schema rule:
Final JSON must use the exact nested schema from `prompt.md`.

Do not rename any keys:

* education must use `university`, `degree`, `location`, `graduation`, `ta_bullet`
* technical_skills must be an object/dictionary, not an array
* professional_experience must use `company`, `title`, `location`, `dates`, `bullets`
* projects must use `name`, `tech`, `github_url`, `bullets`
* config must use only `type`, `level`, `layout_profile`, `output`, `bold_markers`, `ta_active`, `company`, `role`

Never use wrong keys like `institution`, `gpa`, `education dates`, `ta`, `row`, `skills` as nested array keys, `client`, `url`, `link`, `repository`, or `technologies`.

Bullet and verb rules:
Experience bullets must use 1 to 2 technical terms, maximum 3. All opening verbs must be unique across the entire resume, including experience, projects, and TA bullets. Prefer strong JD action verbs when defensible.

Bullet meaning rule:
Every lead bullet must show problem/system + how solved + scope/result. Reject bullets that only list tools, responsibilities, or metrics without context. The summary must target 35 to 45 words, avoid target-title inflation, and show how the candidate can contribute to the JD team.

After CONFIRM, generate final JSON only after:

* JD sentence coverage
* OR requirement satisfaction
* approved DES placement
* dynamic JD-primary stack focus
* input quality gate
* call-pile test
* top-signal ranking and first two bullet check
* title/date evidence gate
* DONE-IT / CAN-DO-IT-HERE classification
* ATS JD Match Score
* recruiter 7 to 15 second scan
* hiring manager proof
* anti-stuffing
* anti-over-optimization
* skills traceability
* bullet tech density
* bullet meaning check
* domain gap check
* date sanity check
* unique verb ledger
* exact nested schema validation twice
* banned-key check
* no `client` key check
* exact title/contact preservation
* project gap-filler logic
* JSON validation

Final output order:

1. FINAL AUDIT SUMMARY
2. Diagnostic scores as text only
3. One final JSON block only

Do not print a draft JSON and then correct it. Fix internally before output.
Use exact JD wording only where authentic and defensible.
Prioritize believable hiring-manager proof over maximum keyword count.
Do not claim the resume guarantees recruiter selection.
