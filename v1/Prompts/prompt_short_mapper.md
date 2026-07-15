# V1 Evidence Mapping Stage Controller

`RUN MODE: EVIDENCE_MAPPING` is the only active stage for this call. The complete Prompt 2 system context and `story.md` remain authoritative.

- Treat the company, title, location, and JD as the target application, not as candidate employment evidence.
- Use only the current JD analysis, current request inputs, `story.md`, and prepared DES rules.
- Cover every analyzed requirement exactly as Prompt 2 requires and bind every configured bullet slot to one truthful story purpose.
- Keep every slot independently writable, with one coherent achievement, no more than three planned JD keyword units, one exact supported JD alignment anchor or truthful close-match replacement, and ranked evidence-supported action intents.
- Preserve exact configured role order, bullet counts, project counts, evidence boundaries, and output schema.
- Do not write final resume bullets, a resume, Markdown, commentary, or explanations.
- Complete Prompt 2's silent self-check and return exactly one valid JSON object matching its Required Output Contract, with no code fence or text before or after it.
