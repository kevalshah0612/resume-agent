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
4. Track changes silently and summarize only meaningful repair categories
5. Do not add new tools, metrics, domains, users, testing types, projects, titles, dates, or leadership claims
6. Evaluate coverage silently and mention only major unresolved risk in the short summary
7. Output a recruiter summary of no more than 8 short lines, separate recruiter and hiring-manager LinkedIn messages, 4 search strings, then one complete parseable JSON block with every object and array closed

Outreach rules:
- each message has an independent hard maximum of 300 characters including spaces
- both messages must name the exact TARGET TITLE and TARGET COMPANY supplied in the request
- use one proof point supported by the selected final JSON, never a technology or achievement list
- recruiter message may politely ask for the correct recruiter or for the resume to be passed along
- hiring-manager message must connect the proof to one JD priority and ask one concise question about the team or role
- avoid generic `would love to connect` language, flattery, desperation, and em dashes

Final JSON must preserve exact schema from Recruiter.md and must not include banned keys.
Do not add anything after the final JSON block.
Do not output audit tables, coverage matrices, OLD -> NEW tables, or quality-gate tables.


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
