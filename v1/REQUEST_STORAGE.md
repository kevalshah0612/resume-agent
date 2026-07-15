# V1 Request Storage Contract

Each V1 request must have its own request folder. Preserve provider-returned reasoning separately from JSON, consolidated into one request-level reasoning file with one labeled section per prompt.

```text
00_request.json
01_job_description.txt
02_jd_intelligence.json
03_evidence_map.json
04_des_approval.txt
05_resume_v3.json
06_reasoning.txt
```

## Storage rules

1. Save the exact parsed JSON returned by each prompt.
2. Save the exact provider-returned reasoning for each prompt under its labeled section in `06_reasoning.txt`.
3. Never place reasoning inside a stage JSON response.
4. Never synthesize or invent reasoning when the provider does not return it. Write `Reasoning was not returned by the selected model.` instead.
5. Do not create a separate raw-response file when the raw response is identical to the saved JSON.
6. If a response cannot be parsed as JSON, preserve that response as `<stage>_parse_error_raw.txt` for diagnosis. This is error preservation, not an automatic retry.
7. Do not overwrite a completed stage artifact except when the user explicitly resumes that incomplete stage; the newly completed result becomes current while the prior API error artifact remains diagnostic history.
8. Do not create Python quality-validation reports, Python repair artifacts, automatic retry artifacts, or test artifacts.
9. Prompt 3 performs the final resume quality and structure review internally before returning `05_resume_v3.json`.
10. Do not save derived renderer JSON. Generate it temporarily from `05_resume_v3.json` when DOCX is requested.
11. On a provider failure, save a stage-specific sanitized `*_api_error.json` containing status, elapsed time, request ID and safe headers when available, account label, model, and sanitized request parameters. Never save API keys.
