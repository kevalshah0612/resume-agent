Read `recruiter.md` first and follow it exactly. Do not print Thinking, Reading documents, scratchpad, tool notes, or hidden reasoning.

I will provide:

JD:
[paste JD]

Des:
[paste approved DES or remove this section]

Resume 1:
[paste ChatGPT/Claude/Gemini JSON]

Resume 2: optional
[paste second JSON or omit]

Important:
You do not have story.md. Act like a real recruiter-style reviewer and judge only what is visible in the JD, Resume 1, optional Resume 2, and optional Des. This is a red-flag repair and validation step, not a story.md truth audit.

Task:

1. Pick the stronger resume, or review Resume 1 only if Resume 2 is missing
2. Check JD sentence coverage, ATS exact wording, OR requirements, call-pile proof, top-bullet order, summary strength, and skill classification
3. Find all blocker red flags first, then up to 15 meaningful JD/recruiter/HM/schema red flags
4. Fix only those red flags
5. Show OLD → NEW for every changed bullet
6. Preserve meaning unless the old claim is weak, unsupported, stuffed, or not JD-aligned
7. Do not add new facts, tools, metrics, domains, ownership, leadership, or outcomes
8. Use exact JD wording only when visible resume or Des evidence supports it
9. Keep JSON keys, key order, contact, education, company names, titles, dates, project names, and URLs unchanged, except remove `client` if present
10. Final professional_experience keys must be exactly `company`, `title`, `location`, `dates`, `bullets`
11. Experience bullets must use 1 to 2 technical terms, maximum 3
12. Classify each skill as CORE_JD, PREFERRED_JD, SUPPORTED_SECONDARY, or UNSUPPORTED; central JD skills need bullet proof, supported secondary skills may stay in skills
13. Projects should only fill JD gaps, not overpower production experience
14. Final JSON must parse cleanly and must not include `client`

Final output must include:

* PICKED JSON
* WHY PICKED
* VISA CHECK
* CALL-PILE REVIEW
* TOP-BULLET CHECK
* SUMMARY CHECK
* SKILL CLASSIFICATION CHECK
* JD SENTENCE COVERAGE
* OR REQUIREMENT COVERAGE
* RED FLAGS
* RED FLAGS FIXED with OLD → NEW
* ATS WORDING FIXES
* SKILLS TRACEABILITY
* QUALITY GATES
* FINAL SCORES
* KEY TERMS EXCLUDED OR NEED DES
* FINAL JSON

Do not rewrite the whole resume for style.
Fix JD, ATS, recruiter, HM, evidence, stuffing, call-pile, top-bullet, summary, skill-classification, and schema red flags only. Summary must be 35 to 45 words preferred and must avoid target-title inflation.
Do not add anything after the final JSON block.
