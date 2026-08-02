# Prompt 5: Custom Cover Letter Per Role

## Candidate reference for this cover letter

Use only facts in the current uploaded resume or final resume JSON. The current resume/final JSON controls every identity, contact, education, experience, skill, and outcome value.

```text
Write a cover letter for this role. Rules:

1. First paragraph: Name the company and role.
Reference one specific thing about the company
that made you want to apply (a recent product
launch, a news article, a company value that
resonates). Do NOT be generic.

2. Second paragraph: Pick the 2-3 requirements
from the job description where my experience
is strongest. For each, give one concrete
result from my resume (with numbers).

3. Third paragraph: Address the biggest gap
between my resume and the job description
head-on. Explain how my transferable skills
or adjacent experience covers it. Do not
pretend the gap does not exist.

4. Closing: One sentence. Ask for the interview.
No fluff. No 'I look forward to the
oportunity to discuss.'

Total length: Under 250 words.
Tone: Confident, specific, human.
Do NOT sound like AI wrote it.
```

## PDF output requirement for the cover letter

After drafting and checking the cover letter, create one polished one-page PDF named:

```text
[Configured_Resume_Stem]_[Company]_Cover_Letter.pdf
```

Use a clean business-letter layout:

```text
[Candidate name from final resume JSON]
[Candidate contact line from final resume JSON]

[Date]

Hiring Team
[Company]

Dear Hiring Team,

[Three short cover-letter paragraphs]

Sincerely,
[Candidate name from final resume JSON]
```

PDF rules:

- Use a standard readable font and one-column layout
- No graphics, icons, tables, text boxes, columns, or ATS-style keyword blocks
- Keep the letter to one page
- Use only facts supported by the current resume/final JSON and JD
- If a specific company fact is not verified, do not invent one; use a JD-based reason for interest instead
- If PDF creation is unavailable, return the final cover-letter text only
