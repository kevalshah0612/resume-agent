# V1 Evidence Mapping Stage Controller

`RUN MODE: EVIDENCE_MAPPING` is the only active stage for this call. The complete Prompt 2 system context and `story.md` remain authoritative.

- Treat the company, title, location, and JD as the target application, not as candidate employment evidence.
- Use only the current JD analysis, current request inputs, `story.md`, and prepared DES rules.
- Read every story from the first line through the last line before selecting evidence. Derive the current story count and IDs from `story.md`, return the complete `story_scan` receipt, do not stop after finding enough plausible matches, and do not use a top-story retrieval limit.
- Enforce story origins: TA uses only `TA-*`, GHI only `GHI-*`, TCS roles may use `TCS-I-*` or `TCS-II-*`, and projects use only `PROJ-*`. Never move TCS evidence into TA or GHI.
- Cover every analyzed requirement exactly as Prompt 2 requires and bind every configured bullet slot to one truthful story purpose.
- Keep every slot independently writable with one coherent achievement, one method group, one result or scope group, no more than two numeric expressions, no more than three planned JD keyword units, one exact supported JD alignment anchor or truthful close-match replacement, and ranked evidence-supported action intents.
- Keep technologies as separate terms so the composer writes `Java, Spring Boot`, `C#, .NET`, and `Python, FastAPI`; never plan `Java Spring Boot`, `Java/Spring Boot`, `C# .NET`, `Python FastAPI`, or `SQL/NoSQL`. Preserve established names such as `CI/CD` and `A/B testing`.
- Keep every DES approval and fallback bound to the same story ID as its planned bullet slot; never attach a different-story DES fallback to a locked slot.
- Plan every bullet for 18 to 22 words and never more than 24 words. Carry only the selected facts and metrics needed for that bullet, not every available detail from the story.
- Preserve exact configured role order, bullet counts, project counts, evidence boundaries, and output schema.
- Do not write final resume bullets, a resume, Markdown, commentary, or explanations.
- Complete Prompt 2's silent self-check and return exactly one valid JSON object matching its Required Output Contract, with no code fence or text before or after it.
