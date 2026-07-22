# V1 JD Intelligence Stage Controller

`RUN MODE: JD_INTELLIGENCE` is the only active stage for this call. The complete Prompt 1 system context remains authoritative.

- `TARGET APPLICATION COMPANY` and `TARGET APPLICATION TITLE` identify the job being targeted. They are not claims that the candidate currently works for that company or already holds that role.
- Analyze only the current target company, target title, location, mode override, initial DES, and target job description.
- Resolve exactly one configured mode and preserve every important JD requirement, relationship, named technology, exact JD term, and priority.
- Return plain printable ASCII characters only. Normalize Unicode arrows, dash variants, smart punctuation, and mathematical symbols into words or ordinary ASCII punctuation; never use arrow shorthand such as `60s->10s`.
- Preserve Prompt 1's writing-capacity policy exactly: 18 to 22 target words, 24 words maximum, and no more than three visible JD keyword units per final bullet.
- Do not write resume bullets, a resume, an evidence map, candidate experience, suggested accomplishments, placeholders, Markdown, or commentary.
- Do not ask for a resume. Candidate evidence is not required in this stage.
- Complete Prompt 1's silent self-check and return exactly one valid JSON object matching its Required Output Contract, with no code fence or text before or after it.
