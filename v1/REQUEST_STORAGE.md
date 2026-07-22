# V1 Request Storage Contract

Each V1 request must have its own request folder. Preserve provider-returned reasoning separately from JSON, consolidated into one request-level reasoning file with one labeled section per prompt.

```text
00_request.json
01_job_description.txt
02_jd_intelligence.json
03_evidence_map.json
04_des_approval.txt
05_resume_v3_composer.json
05_composer.json
05_resume_v3.json
05.json
06_ats_gap_report.md
06_reasoning.txt
07_resume_v3_optimized.json
```

## Storage rules

1. Save the exact parsed JSON returned by each prompt.
2. Save the exact provider-returned reasoning for each prompt under its labeled section in `06_reasoning.txt`.
3. Never place reasoning inside a stage JSON response.
4. Never synthesize or invent reasoning when the provider does not return it. Write `Reasoning was not returned by the selected model.` instead.
5. Do not create a separate raw-response file when the raw response is identical to the saved JSON.
6. If a response cannot be parsed as JSON, preserve that response as `<stage>_parse_error_raw.txt` for diagnosis. This is error preservation, not an automatic retry.
7. `Compose` saves its immutable compact source as `05_resume_v3_composer.json` and its expanded V1 source, including contact/type/education fields, as `05_composer.json`. It initially makes the same content canonical at `05_resume_v3.json` and `05.json`.
8. `Validate` is a separate, explicitly triggered post-V1 flow. It must not rerun or alter JD Intelligence, Evidence Mapping, DES approval, or Resume Composition.
9. Save the read-only ATS report as `06_ats_gap_report.md` and the exact parsed optimizer JSON as `07_resume_v3_optimized.json`.
10. Promote the parsed optimizer result to canonical `05_resume_v3.json` and regenerate canonical expanded `05.json`. Never overwrite either Composer backup, so the original and optimized expanded resumes retain the same V1 contact/type fields.
11. Prompt 3 remains the final owner of the original V1 composition. Post-V1 validation may recover only mapper-authorized, same-slot evidence and must preserve the composer artifact.
12. `05.json` is the expanded renderer compatibility object generated from the current canonical compact JSON.
13. Do not create automatic model-retry, Python validation, or Python repair artifacts for the post-V1 flow.
14. On a provider failure, save a stage-specific sanitized `*_api_error.json` containing status, elapsed time, request ID and safe headers when available, account label, model, and sanitized request parameters. Never save API keys.
