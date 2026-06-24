Read `Recruiter.md` first and follow it exactly.

You will receive:
JD:
Des: optional
Resume 1:
Resume 2: optional

Blind rule:
Do not use Story.md, memory, old resumes, prior chats, or assumptions. Judge only the visible JD, Resume JSON, optional Resume 2, and optional Des.

Task:
1. Pick stronger JSON, or review Resume 1 only
2. Check hard filters, JD coverage, exact wording, call-pile strength, top two bullets, summary, skills traceability, projects, TA usage, and schema
3. Fix only meaningful red flags
4. Keep OLD -> NEW reasoning internal unless the final prompt explicitly asks for it
5. Do not add new tools, metrics, domains, users, testing types, projects, titles, dates, or leadership claims
6. Keep coverage and quality-gate analysis internal
7. Output the required summary, recruiter LinkedIn message, hiring-manager LinkedIn message, recruiter/HM search strings, and one final valid JSON block only

Final JSON must preserve exact schema from Recruiter.md and must not include banned keys.
Do not add anything after the final JSON block.


Additional strict repair rules:
- Repair config, header, TA placement, project count, bullet order, and repeated opening verbs when visible JSON evidence allows it
- Keep `education.ta_bullet` empty
- Keep `config.ta_active` false
- Header must use `Target Role | New York, NY | relocation/work-location signal` plus a second contact-details line separated by `\n`
- Top two bullets of every experience must be strongest JD signals and different proof types
- Cross-stack bullets must describe a real connected workflow, not a keyword list
- Do not invent missing projects to satisfy project count
- If project count cannot be fixed blindly, flag `NEEDS CREATOR REGENERATION`

Additional critical rules:
- Target 90% natural JD keyword coverage from visible JSON/DES only
- Supported PRIMARY JD keywords should appear 2 to 3 times naturally when visible evidence allows
- No opening verb may repeat across the final resume
- Preserve visible experience records and projects by default; do not delete entire records/projects unless duplicate, empty, schema-breaking, unsupported beyond repair, or explicitly requested
- Repair internship vs non-internship Binghamton graduation date when JD/title makes it obvious
- Flag `NEEDS CREATOR REGENERATION` if a fix requires unseen Story.md evidence
- Detect AI-sounding bullets, keyword stuffing, skills-only primary terms, repeated verbs, weak summaries, bad header/location, TA under Education, and project count mismatch

Output format controls:
- Output only:
  1. RECRUITER SUMMARY
  2. RECRUITER LINKEDIN MESSAGE
  3. HIRING MANAGER LINKEDIN MESSAGE
  4. RECRUITER/HM SEARCH STRINGS
  5. FINAL JSON
- LinkedIn messages must each be 300 characters or fewer
- Use ASCII punctuation only
- Do not output audit tables, OLD -> NEW tables, coverage matrices, or quality-gate tables
