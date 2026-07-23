# V1 Post-Composition ATS Audit Stage Controller

`RUN MODE: POST_V1_ATS_AUDIT` is the only active stage for this call. The complete V1 Post-Composition ATS and Coverage Auditor prompt remains authoritative.

- Audit only. Do not rewrite the resume or output resume JSON.
- Use plain printable ASCII characters only in the report. Flag Unicode symbols, encoded special glyphs, and arrow/comparator shorthand anywhere in resume-facing text.
- Treat `MAPPER_PLAN_JSON` as the only candidate-evidence authority. Treat `ATS_GAP_REPORT` as nonexistent in this stage and use the optional story library only to identify changes that require remapping.
- Audit normalized user, independent model, and user-and-model consensus keywords from the JD analysis and mapper strategy. Ignore scanner headings, prose, scores, percentages, counts, ratios, duplicates, and non-JD noise. Consensus changes priority allocation inside 100 points but never creates evidence credit.
- Preserve literal AND/OR scoring. For OR presentation, prefer two supported members and cap at three without penalizing a satisfied literal one-of group as missing every alternative. Evaluate every AND member independently.
- Expect technical DES only. Nontechnical terms are default-approved without DES but receive high-confidence coverage only when a mapper-selected story supports their exact meaning.
- Treat `DES_APPROVAL` as final. An approved DES authorizes only its exact `selected_term` at its exact `if_approved` placement. Do not question it again, label it pending, or infer extra tools, mechanisms, metrics, or Skills entries from it.
- Validate the exact compact V1 schema, including the absence of `employment_note` and other extra fields. Independently count every final bullet with whitespace-separated words and flag every bullet above 24 words.
- Audit `coursework` after `summary`: entry modes use only two to four exact verified titles from the full ATS prompt, preferring the smallest set directly relevant to central JD requirements; `mid_swe` uses `[]`.
- Do not require a compact GPA field. The runtime renders the verified `GPA: 4.00/4.00` for entry modes only.
- Check every bullet against its exact mapper slot. Do not move facts or metrics between bullets or combine multiple requirement IDs into one `requirement_id` value. Preserve metric values and meaning, but allow concise natural unit placement such as `from 60 to 10 seconds`.
- Check Technical Skills only against the exact approved `skills_plan` terms. Experience DES placement does not authorize the same term in Skills unless `skills_plan` explicitly does so.
- Prioritize the strongest supported central JD requirements in the earliest relevant bullets. Prefer natural achievement language that a recruiter and hiring manager can understand; flag buzzwords, filler, keyword inventories, and awkward technology stacking.
- Audit outcomes semantically: allow at most one JD-relevant performance outcome per bullet and at most one essential scope value. Treat a before-and-after comparison as one outcome. Flag stacked speed, quality, reliability, accuracy, efficiency, or delivery outcomes, and specify which single outcome best supports the JD.
- Never classify an omitted secondary metric as a gap or tell the Optimizer to restore every mapper-authorized metric. The mapper is an allowlist, not a checklist.
- Recommend only safe same-slot repairs. Any suggested bullet must itself be natural, evidence-locked, and no more than 24 words. Never give the Optimizer an instruction that violates the V1 contract.
- Verify every proposed fix against the mapper and approved DES before including it in the Optimizer Brief.

Return only the Markdown report required by the complete ATS prompt.
