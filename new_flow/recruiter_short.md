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
4. Show OLD -> NEW for every changed bullet
5. Do not add new tools, metrics, domains, users, testing types, projects, titles, dates, or leadership claims
6. Print coverage report with exact JD terms and final placement
7. Output one final valid JSON block only at the end

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
