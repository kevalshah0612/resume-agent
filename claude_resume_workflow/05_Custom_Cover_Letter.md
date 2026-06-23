# Prompt 5: Custom Cover Letter Per Role

## Candidate reference for this cover letter

Use these facts only when they are accurate to the current uploaded resume or final resume JSON. If there is any conflict, the current resume/final JSON controls.

```text
Name: Keval Shah
Current location: Binghamton, NY
Education: Completing an M.S. in Computer Science with an AI specialization at Binghamton University, GPA 4.00, expected Aug 2026
Prior experience: 3+ years of software engineering experience at Tata Consultancy Services
Recent U.S. experience: Software Engineer, Global Health Impact Project, New York, NY
Teaching: Teaching Assistant for Database Systems and Object-Oriented Programming
Core proven areas: Java, Spring Boot, REST APIs, distributed systems, CI/CD, cloud operations, observability, production debugging, React/TypeScript workflows, SQL/NoSQL, data pipelines, AI/ML and AI-tooling projects where supported by the resume
Representative proven outcomes: reduced a Java upload workflow from 60 seconds to 10 seconds for 10,000+ users; supported 40+ production releases; reduced incident diagnosis from hours to minutes across connected applications; processed 10M+ weekly WHO health records into PostgreSQL and MongoDB pipelines; reduced reporting turnaround to 30 seconds across 150+ countries
```

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
Keval_Shah_[Company]_Cover_Letter.pdf
```

Use a clean business-letter layout:

```text
Keval Shah
Binghamton, NY | (607) 235-1181 | keval.shah61298@gmail.com

[Date]

Hiring Team
[Company]

Dear Hiring Team,

[Three short cover-letter paragraphs]

Sincerely,
Keval Shah
```

PDF rules:

- Use a standard readable font and one-column layout
- No graphics, icons, tables, text boxes, columns, or ATS-style keyword blocks
- Keep the letter to one page
- Use only facts supported by the current resume/final JSON and JD
- If a specific company fact is not verified, do not invent one; use a JD-based reason for interest instead
- If PDF creation is unavailable, return the final cover-letter text only
