# V1 JD Intelligence Stage Controller

`RUN MODE: JD_INTELLIGENCE` is the only active stage for this call. The complete Prompt 1 system context remains authoritative.

- `TARGET APPLICATION COMPANY` and `TARGET APPLICATION TITLE` identify the job being targeted. They are not claims that the candidate currently works for that company or already holds that role.
- Analyze only the current target company, target title, location, mode override, initial DES / user keyword input, and target job description.
- The Initial DES / Existing field may contain JobAlytics, Simplify, or several scanner reports pasted together. Treat them as one keyword-discovery source. Independently extract the JD's important keywords before comparison. Ignore source headings, explanatory prose, scores, percentages, counts, ratios such as `3/12`, checkmarks, and the scanner's `matches`, `missing`, `high`, or `low` status; those labels are not candidate evidence or authoritative JD priority. Normalize and case-insensitively deduplicate actual keyword lines and discard only terms absent from and not faithfully equivalent to the JD.
- Give a one-point capped consensus boost only when both the user and independent model analysis identify the same base-priority 3-to-5 JD keyword. Preserve model-only and user-only signals separately.
- Treat the normalized union of every JD-valid user keyword and every independent model keyword as the complete downstream targeting inventory. Consensus controls ranking attention, not whether a valid user-only or model-only keyword is processed.
- Resolve exactly one configured mode and preserve every important JD requirement, relationship, named technology, exact JD term, and priority.
- Preserve literal AND/OR satisfaction. For OR presentation, target two supported members and cap at three without inventing coverage or changing a literal minimum of one; record the logic and targets for the mapper.
- Return plain printable ASCII characters only. Normalize Unicode arrows, dash variants, smart punctuation, and mathematical symbols into words or ordinary ASCII punctuation; never use arrow shorthand such as `60s->10s`.
- Preserve the complete runtime writing-capacity policy exactly, including its target range, hard maximum, and maximum visible JD keyword units per final bullet.
- Do not write resume bullets, a resume, an evidence map, candidate experience, suggested accomplishments, placeholders, Markdown, or commentary.
- Do not ask for a resume. Candidate evidence is not required in this stage.
- Complete Prompt 1's silent self-check and return exactly one valid JSON object matching its Required Output Contract, with no code fence or text before or after it.
