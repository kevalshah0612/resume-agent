Read these files first:
1. `Prompt.md`
2. `Story.md`

Follow `Prompt.md` exactly. Use `Story.md` as the evidence bank, not the resume identity. The JD decides what matters; Story.md decides what is allowed.

Do not print hidden reasoning, scratchpad, tool notes, or internal validation narration.

Input:
Company:
Title:
JD:
Words:
Mode:
Des:

Workflow:
1. First run PASS 1 only
2. Print only the compact COVERAGE SUMMARY and parseable DES CANDIDATE BANK required by Prompt.md
3. Create DES candidates for unsupported or partial JD terms instead of inventing facts
4. Wait for DES approval or `No DES`
5. Do not generate final JSON until user says `CONFIRM`
6. After CONFIRM, output the required confidence summary, recruiter LinkedIn message, hiring-manager LinkedIn message, recruiter/HM search strings, and one valid JSON block only

Critical rules:
- Use exact JD wording only when Story.md or approved DES supports it
- Central JD skills must appear in summary or bullets, not only Technical Skills
- Skills row 1 must mirror JD primary stack
- First two bullets must be highest JD signal
- Entry/new-grad may use GHI first and TA as Professional Experience
- Mid uses TCS SWE II first unless JD is clearly AI/GHI/project-heavy
- TA must not be called Software Engineer
- Projects fill gaps only
- No unsupported tools, metrics, domains, tests, leadership, or production claims
- Final JSON must use the exact schema from Prompt.md


Additional strict controls:
- Config must follow Prompt.md Config and Layout Contract
- Project count must match selected `layout_profile`
- `mid` uses exactly 2 projects by default
- TA must never be written under Education
- `education.ta_bullet` must always be empty
- If TA is used, it must be a Professional Experience object
- Header must be: `Target Role | New York, NY | relocation/work-location signal`
- Contact field must contain `\n` between role/location line and contact details line
- Top two bullets of every experience must be strongest JD signals and different proof types
- Cross-stack bullets must describe one connected workflow, not a tool list
- Opening verbs must be audited and should not repeat

Additional critical rules:
- Target 90% natural JD keyword coverage without forced or unsupported placement
- Supported PRIMARY JD keywords should appear 2 to 3 times naturally, with production/professional placement when evidence exists
- No opening verb may repeat across the entire final resume
- Binghamton graduation must be `Jan 2025 - Dec 2026` for internship/co-op/student intern roles and `Jan 2025 - May 2026` for non-internship full-time roles
- Story.md evidence must be interpreted with FAANG-level clarity: system, mechanism, scope, outcome, and limits
- Final output after CONFIRM must include separate recruiter and hiring-manager LinkedIn messages plus recruiter/HM search strings outside JSON
- Do not force keywords that fail the Natural Fit Test; use DES, exclusion, or suggestions instead

Output format controls:
- PASS 1 must contain 3 to 8 one-line candidates beginning exactly with `DES <number> |`
- PASS 2 after CONFIRM must output only:
  1. CONFIDENCE SUMMARY
  2. RECRUITER LINKEDIN MESSAGE
  3. HIRING MANAGER LINKEDIN MESSAGE
  4. RECRUITER/HM SEARCH STRINGS
  5. FINAL JSON CODE BLOCK ONLY
- LinkedIn messages must each be 300 characters or fewer
- Do not output audit tables after CONFIRM
- Do not write anything after the final JSON code block
