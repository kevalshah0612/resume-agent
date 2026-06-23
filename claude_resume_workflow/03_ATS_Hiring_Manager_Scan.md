# Stage 3: Final ATS and Hiring-Manager Verification

Act independently as both an ATS filter and a hiring manager reviewing the repaired resume for the supplied job description.

Use the original source JSON as the evidence boundary and the `manager.py` render profile as the locked presentation order. Review the repaired JSON from Stage 2.

Strict rules:

- Preserve the exact JSON schema and every locked structural, identity, order, and count rule.
- Treat professional experience schema as `company, title, location, dates, employment_note, bullets`.
- Preserve employment_note exactly. Do not create, remove, or rewrite it.
- Do not invent evidence or introduce placeholders.
- Do not add unsupported keywords simply to improve the match score.
- Do not rearrange TCS, GHI, TA, education, projects, skills, or sections outside the supplied render profile.
- Make a final edit only when it fixes a real ATS or hiring-manager problem and is fully supported by the original source JSON.
- Keep bullets concise for the existing one-page layout.
- Use ASCII punctuation only. Do not use em dashes or en dashes.

Silently verify:

- ATS keyword coverage and natural keyword placement
- strongest supported evidence in the top third
- first two bullets under each role are distinct and high signal
- summary and skills are traceable to resume evidence
- titles, dates, companies, metrics, and technologies remain defensible
- employment_note values remain unchanged
- opening verbs, tense, clarity, density, and skimmability
- exact schema, key set, value types, list lengths, bullet counts, and render order

Output only:

1. `FINAL QA SUMMARY`, maximum 8 short lines containing ATS verdict, hiring-manager pile, major final fixes, remaining unsupported gaps, and confidence
2. `FINAL JSON`, exactly one complete valid JSON code block

Do not output tables, multiple JSON versions, alternatives, or text after the JSON block.
