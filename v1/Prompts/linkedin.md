# V1 LinkedIn Outreach Prompt

## Mission

Create concise LinkedIn outreach for the current application and search queries that help the candidate find the appropriate recruiter and hiring manager.

Use only the supplied final resume JSON, job description, company, title, and location.

## Truth Boundary

Do not use Story.md, DES files, old requests, prior conversations, outside company knowledge, or assumptions.

Do not invent a recipient name, relationship, referral, hiring status, team name, company fact, achievement, metric, technology, or responsibility.

`[Name]` is the only allowed placeholder.

## Messages

Create exactly two messages:

1. Recruiter LinkedIn Message
2. Hiring Manager LinkedIn Message

Each message must:

- be no more than 300 characters including spaces
- target 200 characters or fewer when the idea remains complete
- use the exact target title and company
- contain one resume-supported proof point aligned with the JD
- state why the candidate is reaching out
- end with one low-friction question or request
- use ASCII punctuation only

Recruiter message purpose:

- Say that the candidate applied for the exact role.
- Briefly establish relevance with one supported proof point.
- Ask whether the recipient owns the search or can direct the candidate to the correct recruiter.

Hiring manager message purpose:

- Say that the candidate applied for the exact role.
- Briefly connect one supported proof point to a central JD responsibility.
- Ask one thoughtful, easy-to-answer question about the role's current priority or success criteria.

Do not use generic praise, flattery, desperation, a technology dump, fake familiarity, or phrases such as:

- I hope you are well
- I would love to connect
- perfect fit
- passionate about
- excited to leverage
- impressive company
- dream opportunity

Do not ask for a referral, interview, call, or resume review in the first message.

## Search Strings

Create exactly four Google search strings. Every string must begin with:

```text
site:linkedin.com/in
```

Cover these four search intents:

1. Company recruiter or talent acquisition contact
2. Company engineering or hiring manager contact
3. Company plus the exact target title
4. Company plus the JD's central technical discipline or team function

Use quoted multiword company and title terms where useful. Include the supplied location only when it narrows the search. Do not guess people's names or internal team names.

## Final Check

Before returning the output, silently verify:

1. There are exactly two messages and four search strings.
2. Each message is 300 characters or fewer including spaces.
3. Every proof point is present in the final resume JSON.
4. The title and company match the current request exactly.
5. The two messages have different purposes and are not minor rewrites of each other.
6. Every query starts with `site:linkedin.com/in`.

## Output Format

Return only this structure, with no markdown fences, character counts, analysis, or closing note:

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
