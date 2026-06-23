# Stage 2: Evidence-Safe JSON Repair

Repair the supplied source resume JSON using the Stage 1 audit, exact job description, and locked render profile.

Strict rules:

- Return the same complete JSON schema.
- Preserve every key, value type, list length, bullet count, and config value.
- Treat professional experience schema as `company, title, location, dates, employment_note, bullets`.
- Preserve identity/contact fields, role identities and array order, employment_note values, project identities/order, education identities/order, skill-row labels, and renderer-defined output order.
- Preserve employment_note exactly. Do not create, remove, or rewrite it.
- Do not add, remove, merge, or move a role, project, education item, skill row, or bullet.
- Do not move evidence between TCS, GHI, TA, projects, or education.
- Never invent metrics, tools, frameworks, users, domains, dates, titles, responsibilities, or outcomes.
- Never output `[FILL IN]`, TBD, TODO, optional language, or realistic guesses.
- Include a JD keyword only when the source JSON already contains defensible evidence for it.
- Improve existing bullets with a concise accomplishment, result, and method structure where the source evidence supports all three.
- Strong action verbs are required, but opening verbs should not repeat.
- Keep each rewritten bullet concise and no longer than needed for the existing one-page layout.
- Use ASCII punctuation only. Do not use em dashes or en dashes.

Allowed repairs:

- strengthen or tighten the summary using existing evidence
- reorder supported terms inside existing skill fields
- rewrite existing experience and project bullets without changing their count
- improve JD alignment, clarity, specificity, tense, and impact using existing evidence
- remove unsupported or duplicated wording

Output only:

1. `REPAIR SUMMARY`, maximum 8 short lines
2. `FINAL JSON`, exactly one complete valid JSON code block

Do not output tables, alternatives, placeholders, draft JSON, or text after the JSON block.
