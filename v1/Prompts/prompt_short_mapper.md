# V1 Evidence Mapping Stage Controller

`RUN MODE: EVIDENCE_MAPPING` is the only active stage for this call. The complete Prompt 2 system context and `story.md` remain authoritative.

- Treat the company, title, location, and JD as the target application, not as candidate employment evidence.
- Use only the current JD analysis, current request inputs, `story.md`, and prepared DES rules.
- Preserve Prompt 1's normalized user, model, and consensus keyword sets. Give consensus terms extra ranking attention without treating them as evidence or restoring scanner headings, explanations, scores, percentages, counts, ratios, duplicates, or non-JD noise.
- Preserve literal AND/OR logic. For OR presentation, target two supported members and cap at three while recognizing that one member satisfies a literal one-of requirement; for AND and combined stacks, evaluate every member independently.
- Create DES only for important missing named technologies or concrete technical practices with plausible story-local confirmation. Every DES must state logic type/group, literal minimum, resume target, current supported members, priority source, consensus boost, and exact placement.
- Default-approve nontechnical keywords without creating DES, but place exact wording with high confidence only when one selected story supports the meaning; leave unsupported nontechnical terms context-only rather than inventing experience.
- Return plain printable ASCII characters only. Normalize every copied range, change, fact, and metric without imposing a wording pattern; concise forms such as `from 60 to 10 seconds` are valid, but vary phrasing naturally and never use Unicode symbols or arrow shorthand.
- Read every story from the first line through the last line before selecting evidence. Derive the current story count and IDs from `story.md`, return the complete `story_scan` receipt, do not stop after finding enough plausible matches, and do not use a top-story retrieval limit.
- For each requirement, classify evidence across the entire story bank before applying role or section preference: direct evidence outranks close evidence, including when the direct evidence is a project and the close evidence is professional experience. Use experience priority only to break ties between evidence of the same strength.
- Enforce story origins: TA uses only `TA-*`, GHI only `GHI-*`, TCS roles may use `TCS-I-*` or `TCS-II-*`, and projects use only `PROJ-*`. Never move TCS evidence into TA or GHI.
- Cover every analyzed requirement exactly as Prompt 2 requires and bind every configured bullet slot to one truthful story purpose.
- Keep every slot independently writable with one coherent achievement, one method group, at most one performance outcome selected for the strongest central JD requirement, at most one essential scope value, no more than three planned JD keyword units, one exact supported JD alignment anchor or truthful close-match replacement, and ranked evidence-supported action intents.
- Keep technologies as separate terms so the composer writes `Java, Spring Boot`, `C#, .NET`, and `Python, FastAPI`; never plan `Java Spring Boot`, `Java/Spring Boot`, `C# .NET`, `Python FastAPI`, or `SQL/NoSQL`. Preserve established names such as `CI/CD` and `A/B testing`.
- Keep every DES approval and fallback bound to the same story ID as its planned bullet slot; never attach a different-story DES fallback to a locked slot.
- Never create DES when direct evidence exists anywhere in `story.md`. Tool availability does not prove candidate usage; attach named tools or AI-assisted practices to a role only when that role's story or a role-local approved DES proves actual use.
- Plan every bullet for 18 to 22 words and never more than 24 words. Carry only the single best JD-relevant performance outcome and any essential scope value, not every available fact or metric from the story.
- Preserve exact configured role order, bullet counts, project counts, evidence boundaries, and output schema.
- Do not write final resume bullets, a resume, Markdown, commentary, or explanations.
- Complete Prompt 2's silent self-check and return exactly one valid JSON object matching its Required Output Contract, with no code fence or text before or after it.
