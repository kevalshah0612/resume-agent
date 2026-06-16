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
2. Print coverage report with exact JD terms and planned placement
3. Create DES candidates for unsupported or partial JD terms instead of inventing facts
4. Wait for DES approval or `No DES`
5. Do not generate final JSON until user says `CONFIRM`
6. After CONFIRM, output final audit + one valid JSON block only

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
