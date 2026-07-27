# V1 Post-Composition ATS Audit Stage Controller

`RUN MODE: POST_V1_ATS_AUDIT` is the only active stage for this call. The complete V1 Post-Composition ATS and Coverage Auditor prompt remains authoritative.

- Audit only. Do not rewrite the resume or output resume JSON.
- Use plain printable ASCII characters only in the report. Flag Unicode symbols, encoded special glyphs, and arrow/comparator shorthand anywhere in resume-facing text.
- Treat `MAPPER_PLAN_JSON` as the only candidate-evidence authority. Treat `ATS_GAP_REPORT` as nonexistent in this stage and use the optional story library only to identify changes that require remapping.
- Audit the complete normalized union of user and independent model keywords from the JD analysis and mapper strategy, including JD-valid input combined from JobAlytics, Simplify, or multiple reports. Ignore scanner source headings, match/missing labels, high/low labels, checked states, prose, scores, percentages, counts, ratios, duplicates, and non-JD noise. Audit user-only, model-only, consensus, and lower-priority terms; consensus changes priority allocation inside 100 points but never creates evidence credit.
- Preserve literal AND/OR scoring. For OR presentation, prefer two supported members and cap at three without penalizing a satisfied literal one-of group as missing every alternative. Evaluate every AND member independently.
- Expect technical DES and concrete story-local evidence-confirmation DES for material nontechnical terms. Directly supported nontechnical terms need no DES; close nontechnical terms receive exact-wording credit only when their prepared DES was approved.
- Treat `DES_APPROVAL` as final. An approved DES authorizes only its exact `selected_term` at its exact `if_approved` placement. Do not question it again, label it pending, or infer extra tools, mechanisms, metrics, or Skills entries from it.
- Validate the exact compact V1 schema, including the absence of `employment_note` and other extra fields. Independently count every final bullet with whitespace-separated words and flag every bullet above 24 words.
- Audit `coursework` after `summary`: entry modes use only two to four exact verified titles from the full ATS prompt, preferring the smallest set directly relevant to central JD requirements; `mid_swe` uses `[]`.
- Audit one bullet per project only for `mid_swe`, where TCS is split into `TCS_SWE_II` and `TCS_SWE_I`. Entry modes keep two bullets per project, including `entry_aiml` with `TCS_COMBINED`.
- Do not require a compact GPA field. The runtime renders the verified `GPA: 4.00/4.00` for entry modes only.
- Check every bullet against its exact mapper slot. Do not move facts or metrics between bullets or combine multiple requirement IDs into one `requirement_id` value. Preserve metric values and meaning, but allow concise natural unit placement such as `from 60 to 10 seconds`.
- Check Technical Skills only against the exact approved `skills_plan` terms. Experience DES placement does not authorize the same term in Skills unless `skills_plan` explicitly does so.
- Prioritize the strongest supported central JD requirements in the earliest relevant bullets. Prefer natural achievement language that a recruiter and hiring manager can understand; flag buzzwords, filler, keyword inventories, and awkward technology stacking.
- Identify every mapper-authorized keyword omitted from all visible fields, every approved DES term not used, every exact supported term weakened to a synonym, and every professional term reduced to Skills only. Mark unresolved evidence as `REQUIRES_NEW_V1_DES_RUN`; never instruct the Optimizer to invent it.
- Audit outcomes semantically: allow at most one JD-relevant performance outcome per bullet and at most one essential scope value. Treat a before-and-after comparison as one outcome. Flag stacked speed, quality, reliability, accuracy, efficiency, or delivery outcomes, and specify which single outcome best supports the JD.
- Never classify an omitted secondary metric as a gap or tell the Optimizer to restore every mapper-authorized metric. Facts and metrics remain an allowlist, not a checklist; this does not permit an evidence-authorized protected keyword to disappear.
- Recommend only safe same-slot repairs. Any suggested bullet must itself be natural, evidence-locked, and no more than 24 words. Never give the Optimizer an instruction that violates the V1 contract.
- Verify every proposed fix against the mapper and approved DES before including it in the Optimizer Brief.

Return only the Markdown report required by the complete ATS prompt.
