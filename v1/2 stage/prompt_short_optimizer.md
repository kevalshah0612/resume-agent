# V1 Post-Audit Optimizer Stage Controller

`RUN MODE: POST_V1_OPTIMIZATION` is the only active stage for this call. The complete V1 Evidence-Locked Post-Audit Optimizer and Validator prompt remains authoritative.

- Start with `CURRENT_V1_RESUME_JSON` and return one complete JSON object with exactly the same keys, key order, value types, array order, array lengths, role identities, project identities, and bullet-check structure. Do not add, remove, or rename keys.
- Return plain printable ASCII characters only in every JSON string. Replace Unicode symbols and arrow/comparator shorthand with concise natural language. Preserve values and meaning; shared units may appear once, as in `from 60 to 10 seconds`, but do not impose that or any other repeated pattern.
- Preserve `coursework` after `summary`. When enabled by the selected runtime mode, keep only runtime-verified titles and obey runtime `coursework_selection`; otherwise return `[]`.
- Preserve the selected runtime mode's exact project-bullet count.
- Apply the runtime hard maximum of {{V1_HARD_MAXIMUM_WORDS}} words to every bullet.
- Do not add or edit GPA. The runtime renders the configured verified GPA outside the compact JSON only when the selected mode enables it.
- Apply only safe ATS wording improvements supported by the mapper and approved DES. The ATS report is advice, not evidence.
- Process the complete normalized union of mapper-preserved user and model keywords while ignoring scanner source headings, match/missing labels, high/low labels, checked states, prose, scores, percentages, counts, ratios, duplicates, and non-JD noise. Prioritize exact supported user-and-model consensus keywords over otherwise equal terms, but preserve evidence-authorized user-only, model-only, and lower-priority terms. Consensus ranking never authorizes evidence.
- Preserve literal AND/OR logic. Use two supported OR members when available and never more than three; keep every AND member independently supported.
- Apply every approved DES only to its exact selected term and prepared story-local placement. Use mapper-default-approved nontechnical wording without DES only where the selected story directly supports the meaning; close nontechnical wording requires its prepared evidence-confirmation DES approval.
- Treat every approved DES as final and use it only in its authorized mapper placement. Do not label approved content pending or invent supporting details.
- Keep the strongest supported JD terms in the earliest relevant bullets, but write natural achievement-first sentences without keyword stuffing, buzzwords, filler, or technology lists.
- Build a protected-keyword ledger from exact and equivalent mapper evidence, approved DES, resolved Skills terms, and valid protected terms already in the V1 JSON. Do not reduce this coverage. If a protected term leaves one bullet, retain it naturally in another mapper-authorized location from the same evidence boundary, project `tech`, or Technical Skills; otherwise preserve the current valid wording.
- Never delete a protected keyword merely for brevity, a smoother synonym, lower priority, related-tool overlap, or Skills regrouping. Remove only unsupported, contradicted, unapproved, cross-story, non-JD, or duplicate-canonical wording.
- Apply the runtime performance-outcome and essential-scope limits, selecting what best supports the strongest central JD requirement. A before-and-after comparison is one outcome. Remove secondary performance metrics even when the mapper authorizes them.
- Vary sentence structure, metric phrasing, and clause order naturally. Do not rewrite every bullet into the same action-method-result or `from ... to ...` construction.
- Apply the runtime target word range and never exceed the runtime hard maximum.
- After editing, update each existing `bullet_checks` object to match its final bullet without changing the check keys or array order.
- Copy every unchanged field exactly from the input JSON. Return only the final JSON, with no Markdown or explanation.

Return only the final valid JSON object required by the complete Optimizer prompt.
