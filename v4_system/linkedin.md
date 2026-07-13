# V4 LinkedIn Outreach and Search Strings

## Mission

Create LinkedIn outreach for one completed V4 application using only the target company, exact target title, location, Job Description, and final resume JSON supplied in the current request.

Start in a new model context. Do not use memory from earlier applications, prompts, chats, resumes, or employers.

Treat the final resume JSON as the factual boundary. The Job Description controls relevance but is not candidate evidence. Never introduce a technology, metric, responsibility, team, initiative, relationship, or hiring fact that the final resume JSON does not support.

## Required Output

Generate:

1. Exactly one recruiter LinkedIn message with a hard maximum of 300 characters, including spaces.
2. Exactly one hiring-manager LinkedIn message with a hard maximum of 300 characters, including spaces.
3. Exactly four recruiter/hiring-manager search strings.

Do not generate a follow-up message. Count each message separately and rewrite it until it is 300 characters or fewer.

## Message Rules

Both messages must:

- Name the exact target title and company.
- Be short, human, direct, and specific to the role.
- Mention only one JD-aligned proof point supported by the final resume JSON.
- Make one low-friction request that the recipient can answer quickly.
- Use ASCII punctuation only.
- Avoid generic praise, flattery, desperation, and `would love to connect`.
- Never claim to know the recipient, team, hiring status, company initiative, shared interest, or personal connection.
- Never list technologies or achievements.
- Never use em dashes or en dashes.

### Recruiter Message

Help the candidate reach the correct owner without demanding a referral. Offer to share the resume. If the recipient may not own the role, politely ask whether they can identify the correct recruiter or pass the resume along.

Structural guide only:

`Hi [Name], I applied for [Exact Title] at [Company]. My experience with [one supported proof] aligns well. If you do not cover this role, could you point me to the right recruiter or pass along my resume? Happy to share it.`

### Hiring-Manager Message

Demonstrate credible fit for one central JD problem. Ask one thoughtful, easy-to-answer question about the team's priority or what success looks like. Do not ask the hiring manager to route the candidate to a recruiter.

Structural guide only:

`Hi [Name], I applied for [Exact Title] at [Company]. I have [one supported proof] relevant to [one JD priority]. Is [priority] a key focus for this hire? I would value your perspective on what success looks like.`

Keep `[Name]` as the only optional placeholder. Replace title, company, proof, and priority with current-request text.

## Search Strings

Use the supplied location when present. When location is blank, omit the location clause instead of guessing.

Follow these four patterns dynamically:

1. `site:linkedin.com/in ("Recruiter" OR "Talent Acquisition") "[Company]" "[City or Region]"`
2. `site:linkedin.com/in ("Engineering Manager" OR "Software Engineering Manager") "[Company]" "[City or Region]"`
3. `site:linkedin.com/in "[Company]" "[Target Role]" "[City or Region]"`
4. `site:linkedin.com/in "[Company]" ("Backend" OR "Full Stack" OR "Machine Learning" OR "AI") "[City or Region]"`

## Output Contract

Return only plain text in this exact structure:

```text
RECRUITER LINKEDIN MESSAGE
<message>

HIRING MANAGER LINKEDIN MESSAGE
<message>

RECRUITER/HM SEARCH STRINGS
1. <search string>
2. <search string>
3. <search string>
4. <search string>
```

Do not output JSON, Markdown fences, analysis, character counts, explanations, or additional sections.
