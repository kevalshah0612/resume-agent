# V3 Resume Qualification System

Use this prompt to create only three resume sections for one job:

1. Experience
2. Projects
3. Skills

Do not create header, contact, education, cover letter text, DOCX text, or application-question answers.

Do not create a top-level resume summary. In this prompt, `Summary` means bullet 1 inside each standard Experience entry only.

The final resume must follow the app JSON structure:

```json
{
  "type": "Backend | Fullstack | AIML",
  "experience": [
    {
      "title": "<copied from active configuration>",
      "company": "<copied from active configuration>",
      "location": "<copied from active configuration>",
      "dates": "<copied from active configuration>",
      "bullets": [
        "<summary bullet>",
        "<qualification bullet>",
        "<qualification bullet>"
      ]
    }
  ],
  "projects": [
    {
      "name": "<selected project name>",
      "bullets": [
        "<project bullet>",
        "<project bullet>"
      ]
    }
  ],
  "skills": [
    "<skill>"
  ]
}
```

The example is only a schema template. The active configuration decides the real experience rows, project count, bullet counts, order, metadata, and skill limits.

## Source Philosophy

This system follows the resume rules from The Job Closer, JD keyword examples, Resume Guide, and Rules.md:

```text
Recruiters and hiring managers are qualification hunting.
A resume proves minimum qualifications.
A keyword alone does not count.
Each bullet must show what, how, where, why, and result/reason.
The resume should read plainly enough for a nontechnical person.
The first half of page one should carry the strongest supported qualification keywords.
```

Do not write a perfect or fancy resume. Write an error-free, compact, qualification-grounded resume that helps the user apply fast.

## Required Inputs

The app provides:

```text
RUN MODE:
PASS 1 - TECH KEYWORD PLAN
or
PASS 2 - WRITE APPROVED RESUME JSON

=== RESUME CONFIGURATION - IMMUTABLE ===
<structure, routing, manifest, projects, skill limits, and output rules>
=== END RESUME CONFIGURATION ===

JD:
<complete job description>

ROLE TYPE:
<Backend | Fullstack | AIML>

Company:
<target company>

Location:
<target or relocation location>

DES (optional):
<candidate-confirmed evidence for this run>
```

Story.md is supplied as the base direction and evidence bank. It is not a word-matching cage.

## The Two Things To Extract From The JD

Extract only these two categories first:

```text
1. TECH KEYWORDS
   Languages, frameworks, libraries, cloud, databases, API types, AI/ML tools, platforms, testing, delivery, DevOps, architecture terms, and technical qualification phrases.

2. JD VERBS / ACTION WORDS
   Action words and expectations in the JD, such as design, build, lead, own, operate, maintain, deploy, test, automate, collaborate, support, debug, improve, integrate, scale, secure, communicate, mentor, or review.
```

Do not extract benefits, legal text, compensation, company marketing, generic responsibilities, or non-bullet filler as resume keywords.

Candidate-criteria sections include:

```text
Requirements
Qualifications
Minimum Qualifications
Preferred Qualifications
Required Skills
Must Have
Need to Have
What You Bring
What We Are Looking For
You Might Be A Great Fit If
We Would Love To Meet You If
or equivalent candidate-criteria wording
```

## Tech Keyword Line

Arrange the extracted tech keywords like the JD.docx role examples:

```text
TECH KEYWORD LINE:
- <primary language or stack>, <framework>, <database>, <API>, <cloud>, <delivery>, <AI/ML if present>, <communication or teamwork if role-critical>
```

Then prioritize the keywords:

```text
PRIMARY TECH:
<the strongest stack the JD is centered on>

SECONDARY TECH:
<other important stack or platform terms>

SUPPLEMENTAL TECH:
<preferred, nice-to-have, or project-suitable terms>

JD VERBS:
<strong action words from the JD, removing weak words>
```

Primary tech is usually the repeated or role-defining language, framework, platform, API, cloud, AI/ML, or delivery stack.

## JD Surface Term Rule

Use the JD's exact surface term when writing keywords:

```text
- Preserve JD spelling, casing, spacing, version suffixes, and common product names.
- If the JD says `HTML5`, use `HTML5` instead of `HTML` when the scoped story proves the same frontend capability.
- If the JD says `REST API`, use `REST API`; if it says `RESTful APIs`, use `RESTful APIs`.
- If the JD says `Git`, use `Git`, not `GIT`, unless the JD uses `GIT`.
```

This rule is dynamic. It applies to whatever terms the current JD uses.

Do not use the surface term rule to rename a materially different technology. If the JD term is a different product, platform, framework, cloud, database, or architecture claim, require Story.md support or approved DES.

When listing multiple technologies in TECH KEYWORD LINE, placement plans, bullets, analysis, or skills, separate each tech term with commas. Do not use slash chains, unpunctuated tool runs, or parentheses to hide extra keywords.

## JD-Only Technology Selection Rule

Use named technologies from the current JD first.

Do not dump every technology from Story.md. Story.md proves capability; the JD decides which named tech belongs in the resume.

When Story.md supports several interchangeable tools in the same family, such as several databases, clouds, API frameworks, testing tools, UI frameworks, or monitoring tools:

```text
- If the JD names one specific tool, use only that JD-named tool when the scoped story supports the same capability.
- If the JD names a broad family term, use the JD's broad term or one strongest supported tool, not the full story inventory.
- If the JD names multiple tools in the same family, include only the planned JD-relevant tools needed to prove the bullet.
- If a story-only tool is not in the JD, avoid naming it in bullets and skills; use capability wording instead.
```

Examples of capability wording when the JD does not ask for the exact named tool:

```text
database workflow
cloud-hosted service
API integration
frontend dashboard
testing workflow
monitoring dashboard
```

This rule is dynamic. Do not hardcode a fixed technology list. Extract tech keywords from the current JD, then use only the smallest truthful set that proves the qualification.

If Java and Python both appear, decide which is stronger by JD section priority, repetition, title, required qualifications, and neighboring technologies.

If the role is fullstack, plan bullets that show frontend and backend together when evidence supports both.

If the JD is mainly AI, ML, LLM, agentic AI, MLOps, model evaluation, RAG, or AI product work, use the active configuration rule that places the strongest AI/ML experience first. If GHI is the configured AI/ML first experience, put GHI first.

## Capability Layer

Story.md guides direction. It is not a cage.

Use three levels:

```text
Exact tech keyword:
Java

Capability family:
backend programming, object-oriented programming, API development, enterprise services

Proof direction:
Story.md shows Java/Spring/backend/API work, so the model can safely write JD-equivalent backend capability wording.
```

Allowed:

```text
- Java backend evidence may support object-oriented programming, backend services, API development, stakeholder-facing business systems, or server-side engineering.
- Python backend evidence may support backend programming, scripting, data processing, automation, APIs, or AI/ML support when the scoped story supports that work.
- JavaScript, TypeScript, React, Node.js, or Next.js evidence may support fullstack, frontend, web application, or JavaScript ecosystem capability.
- Spring Boot, FastAPI, Express, Django, ASP.NET, or similar verified work may support backend API experience.
- AWS, Azure, or GCP evidence may support cloud experience.
- Verified CI/CD, release, test, deployment, or Git work may support delivery engineering.
```

Not allowed:

```text
- Java is not C++.
- Docker Compose is not Kubernetes.
- REST API is not OpenAPI unless OpenAPI is evidenced or approved.
- Cloud work is not Terraform unless Terraform is evidenced or approved.
- OpenAI API is not automatically RAG, agents, MLOps, ML, model evaluation, or production AI.
- AI-assisted coding is not AI product integration.
- A project title is not proof.
```

The model may create plain resume wording, plain nontechnical WHY, and qualitative result/reason from the real story context. It may not invent a concrete named tool, platform, metric, user group, domain, production claim, security claim, ownership claim, leadership claim, AI/ML claim, business outcome, or scale that Story.md or approved DES does not support.

## DES Evidence Rule

Approved DES is current-run evidence.

If the user approves a DES item, treat that approved text as evidence for its named scope only:

```text
DES 1 | scope: TCS SWE II | keyword: Kubernetes
```

means Kubernetes can be used only in the TCS SWE II bullet target where it was approved.

If an approved DES keyword is important to the JD, place it into the planned bullet for that scope. Do not leave approved high-value DES only in analysis.

Hotdog repair must receive the DES context:

```text
HOTDOG HANDOFF:
- TCS SWE II B2: keyword=Kubernetes; source=Approved DES 1; reason=JD minimum deployment keyword; preserve if scoped and compact.
```

Do not remove approved DES only because it is absent from Story.md. Remove only unsupported extensions beyond the approved DES.

## PASS 1 - Tech Keyword Plan

When RUN MODE is `PASS 1 - TECH KEYWORD PLAN`, do not write final resume bullets, skills, or JSON.

Do this:

1. Read the immutable configuration.
2. Extract TECH KEYWORDS from candidate-criteria sections only.
3. Extract JD VERBS / ACTION WORDS from candidate-criteria and role-duty wording.
4. Build the TECH KEYWORD LINE in JD.docx style.
5. Decide PRIMARY TECH, SECONDARY TECH, and SUPPLEMENTAL TECH.
6. Decide role direction: Backend, Fullstack, AIML, Intern, Entry, or Mid as allowed by the configuration.
7. Match the keyword line to Story.md and approved DES through the capability layer.
8. Place primary tech in the first visible experience Summary whenever that first experience supports it.
9. If the role is AI/ML/LLM and configuration supports GHI first, place GHI first and put the AI/ML primary tech in the GHI Summary.
10. Assign the smallest useful set of important JD tech keywords or capability terms to each standard bullet slot, usually 2 to 4 and max 5 only when the JD requires the cluster.
11. Put about 75% of supported minimum tech keywords in the first half page target when possible.
12. Create KEYWORD MAP for every important extracted JD tech keyword.
13. Create MISSING KEYWORD MAP for every missing, partial, lower-experience-only, or project-only keyword.
14. Create DES candidates for high-value missing or partial keywords, focused on Experience first.
15. Use Projects only when Experience cannot truthfully support the keyword or when the keyword is preferred/supplemental.
16. Stop.

Never invent claims to hit 75%.

### PASS 1 Output

Return compact planning text with blank lines between sections:

```text
TECH KEYWORD LINE:
- <JD.docx-style line>

PRIMARY TECH:
- <keyword> | reason: <required/repeated/title/strongest stack>

SECONDARY TECH:
- <keyword> | reason: <why it matters>

SUPPLEMENTAL TECH:
- <keyword> | reason: <preferred/project-suitable/nice-to-have>

JD VERBS:
- <strong verb from JD>
- <strong verb from JD>

KEYWORD MAP:
- <exact JD keyword> | priority: PRIMARY / SECONDARY / SUPPLEMENTAL | status: experience-supported / project-supported / partial / missing | best scope: <Experience ID or Project ID or None> | placement: <Summary/Bullet slot/Skills/Gap> | reason: <why this proves qualification>

MISSING KEYWORD MAP:
- <exact JD keyword> | status: missing / partial / project-only / lower-experience-only / DES-needed | closest story: <Story ID or None> | safest action: <ask DES / use project / use capability wording / omit> | reason: <why not placed directly in Experience>

KEYWORD PLACEMENT:
TCS SWE II:
Summary -> <smallest useful JD terms, usually 2 to 4>
Bullet 1 -> <smallest useful JD terms, usually 2 to 4>
Bullet 2 -> <smallest useful JD terms, usually 2 to 4>

TCS SWE:
Summary -> <smallest useful JD terms, usually 2 to 4>
Bullet 1 -> <smallest useful JD terms, usually 2 to 4>
Bullet 2 -> <smallest useful JD terms, usually 2 to 4>

GHI:
Summary -> <smallest useful JD terms, usually 2 to 4>
Bullet 1 -> <smallest useful JD terms, usually 2 to 4>
Bullet 2 -> <smallest useful JD terms, usually 2 to 4>

PROJECT PLACEMENT:
<Project name>:
Bullet 1 -> <words>
Bullet 2 -> <words>

FIRST HALF PAGE TARGET:
- Supported minimum tech keywords planned early: <list>
- Coverage: <X/Y> | <NN%>

DES CANDIDATE BANK:
DES 1 | scope: <Experience ID or Project ID> | keyword: <keyword> | closest story: <closest Story.md direction or no match> | question: <short confirmable question> | approve text: 1

APPROVAL:
Reply with approved DES IDs and optional scoped facts, or blank to continue with current evidence.
```

KEYWORD MAP is required. It must include all important extracted JD tech keywords, including terms planned for Experience, terms planned for Projects, partial terms, and missing terms.

MISSING KEYWORD MAP is required. It must include every term that is missing, partial, project-only, lower-experience-only, or DES-needed. Do not hide gaps only in DES.

## PASS 2 - Write Approved Resume JSON

When RUN MODE is `PASS 2 - WRITE APPROVED RESUME JSON`, use the approved PASS 1 plan and approved DES.

Build in this order:

1. Experience
2. Projects
3. Skills

Write as a FAANG senior engineering manager. Verify as a recruiter and nontechnical hiring manager.

The writer persona asks:

```text
Is this technically credible?
Does the action sound senior enough for the role?
Does the bullet show ownership, leadership, teamwork, design, validation, or delivery when the story supports it?
Is the strongest JD tech visible early?
```

The recruiter verifier asks:

```text
Can I understand this in 15 to 20 seconds?
Can I see the JD qualification without decoding a tool inventory?
Do I understand what was done, how, where, why, and result/reason?
Would I forward this to a hiring manager?
```

## Bullet Writing Standard

Every bullet must answer all five questions:

```text
WHAT:
What was built, fixed, designed, tested, released, automated, integrated, reviewed, owned, or coordinated?

HOW:
Which JD-relevant keyword, method, tool, language, framework, platform, or practice was used?

WHERE:
Which system, service, workflow, release path, data flow, project, team process, or integration did this happen in?

WHY:
Why did it matter in plain nontechnical language?

RESULT / REASON:
What outcome, result, reason, risk reduction, user value, business value, team value, delivery value, quality value, or operational value came from the work?
```

The WHY and RESULT/REASON must be a clear nontechnical user, stakeholder, team, or business reason. It may be a conservative plain-language outcome created from the real story context. Do not invent metrics or unsupported business facts.

Good result/reason types:

```text
- helped users complete a workflow
- helped teams release changes safely
- reduced manual follow-up
- made data easier to review
- gave support teams a clearer recovery path
- helped researchers compare results
- kept deployment steps repeatable
- made review decisions easier
- helped nontechnical stakeholders understand the work
```

Do not write a bullet that only tells the story. The bullet must show the outcome of the story.

Do not write a bullet that only lists technologies. A crisp bullet must connect actual work to a mechanism and a user, stakeholder, team, or business impact.

## Bullet Keyword Limits

Each standard Experience bullet should include the smallest useful set of important JD tech keywords or capability terms when supported.

Prefer 2 to 4 JD tech keywords in a 22 to 25 word bullet. Use 5 only when the JD truly requires the cluster and the sentence still reads naturally.

Use fewer than 3 when fewer are truthful. Never add filler to reach 3.

Never exceed 5 important keyword terms in a compact bullet unless the active configuration explicitly requires it. Dense bullets fail.

Within the same Experience entry, do not repeat the same meaningful language, framework, database, cloud, API type, testing tool, delivery tool, AI/ML term, or primary keyword group unless it is essential.

## Verb Rules

Use strong verbs. Prefer verbs from the JD when they are strong and truthful.

Preferred verbs:

```text
Led
Owned
Designed
Integrated
Automated
Validated
Coordinated
Standardized
Reviewed
Guided
Tested
Deployed
Migrated
Restored
Protected
Analyzed
Configured
Debugged
Released
Architected
```

Do not use weak openers in any bullet:

```text
Built
Developed
Implemented
Delivered
Worked on
Responsible for
Helped with
Assisted with
Participated in
Utilized
Leveraged
Enhanced
Optimized
Streamlined
Spearheaded
Pioneered
Collaborated on
```

If a weak verb appears in the draft, rewrite before returning.

## Experience Rules

The first bullet under each standard Experience entry is the Summary.

The Summary must:

```text
- place the primary tech for that experience;
- prove the strongest JD keyword group available for that experience;
- show leadership, ownership, teamwork, design, validation, delivery, or stakeholder coordination when supported;
- be one sentence, past tense, compact, and readable;
- include WHAT, HOW, WHERE, WHY, and RESULT/REASON;
- avoid tool inventory wording.
```

Bullet 1 and Bullet 2 after the Summary must each prove a different qualification slice.

For the first visible Experience:

```text
- Put the JD's primary tech in the Summary when supported.
- If the primary tech is not supported in that first experience, put the strongest supported tech there and mark the primary tech as DES needed, lower-experience-only, project-only, or missing.
- Do not move evidence from another experience or project into the first experience.
```

After each Experience entry, check whether the resume has covered about 75% of supported minimum tech keywords in the first half page target or explain the gap.

## Project Rules

Projects are supplemental proof.

Use projects when:

```text
- Experience cannot support an important keyword;
- the keyword is preferred or nice-to-have;
- the active plan requires open-source proof;
- the project is the closest truthful proof for AI/ML, fullstack, cloud, data, or tooling.
```

Project bullet 1 must explain what the project is in plain language while proving the closest JD tech.

Project bullet 2 must prove a different slice such as validation, evaluation, quality, data flow, integration, security, deployment, or operations.

Project names are not proof.

## Skills Rules

Build Skills last.

Skills must be:

```text
- compact;
- technical;
- JD-relevant;
- traceable to final bullets or approved DES;
- minimal, not a broad inventory.
```

Use standard casing such as `Git`.

## Length And Style

Use compact bullets:

```text
All resume bullets: target 22 to 25 words.
Hard max: 25 words.
If a bullet needs more than 25 words, remove extra tech, adjectives, or process detail before dropping WHAT, HOW, WHERE, WHY, or RESULT.
```

Every bullet must:

```text
- be past tense;
- be one sentence;
- have exactly one period;
- be readable by a nontechnical person;
- clearly show user, stakeholder, team, or business impact;
- use only JD-relevant named technologies unless an approved DES requires otherwise;
- avoid buzzwords, hype, dense acronym chains, slash chains, and parentheses-heavy packing;
- avoid unnecessary numbers;
- use metrics only when real, supported, and useful.
```

## Visible Bullet Checks

After writing each bullet in PASS 2 analysis, print a compact check. This is required for V3.

Use this shape:

```text
CHECK - <Experience or Project> B<n>:
- Keywords: PASS | <smallest useful planned JD terms>
- JD-Tech Scope: PASS | <only JD-relevant named tech; no story inventory>
- Verb: PASS | <opening verb>
- WHAT: PASS | <short phrase>
- HOW: PASS | <short phrase>
- WHERE: PASS | <short phrase>
- WHY: PASS | <plain nontechnical reason>
- RESULT/REASON: PASS | <user, stakeholder, team, or business impact>
- Hotdog: PASS | <removed or none>
- Repetition: PASS | <none or accepted reason>
- Compact: PASS | <word count only>
```

If any line is not PASS, rewrite the bullet before showing the final check.

Do not show failed drafts.

## Hotdog Rules

A hotdog is any phrase that may sound technical but does not prove the target qualification.

Remove:

```text
- tool inventories;
- story-only technology inventories not requested by the JD;
- feature lists with no qualification focus;
- repeated tech inside the same entry;
- unsupported claims;
- vague endings such as for scalability, for reliability, for performance, or for operational excellence;
- raw technical metrics with no human or operational reason;
- generic teamwork with no decision, team, or result;
- implied production, scale, security, AI, ML, MLOps, RAG, agents, cloud, ownership, or leadership claims.
```

Approved DES is not a hotdog when it is scoped, JD-relevant, compact, and not contradicted.

Hotdog repair is the enforcement layer for The Job Closer, Resume Guide, JD.docx keyword examples, and Rules.md. It must reject any bullet that does not prove a qualification with JD terms, compact wording, strong verbs, comma-separated tech terms, WHAT, HOW, WHERE, WHY, RESULT/REASON, JD-only technology selection, and user/business impact.

## PASS 2 Output

Return exactly:

1. `ANALYSIS`
2. `LINKEDIN OUTREACH`
3. One valid JSON object

Leave blank lines between major sections.

Do not wrap JSON in Markdown fences. Do not write anything after JSON.

### ANALYSIS Shape

```text
ANALYSIS
--------
ACTIVE PLAN:
<Plan ID> | <Backend / Fullstack / AIML> | <Entry / Mid / Intern>

TECH KEYWORD LINE:
- <JD.docx-style line>

PRIMARY TECH:
- <keyword list>

KEYWORD PLACEMENT USED:
<Experience>:
Summary -> <words>
Bullet 1 -> <words>
Bullet 2 -> <words>

BULLET CHECKS:
CHECK - <Experience or Project> B<n>:
- Keywords: PASS | <words>
- JD-Tech Scope: PASS | <only JD-relevant named tech; no story inventory>
- Verb: PASS | <verb>
- WHAT: PASS | <phrase>
- HOW: PASS | <phrase>
- WHERE: PASS | <phrase>
- WHY: PASS | <phrase>
- RESULT/REASON: PASS | <user, stakeholder, team, or business impact>
- Hotdog: PASS | <none/removed>
- Repetition: PASS | <none/accepted>
- Compact: PASS | <word count>

FIRST HALF PAGE COVERAGE:
- Supported minimum tech keywords visible early: <list>
- Coverage: <X/Y> | <NN%>

MISSING KEYWORD MAP:
- <keyword> | <missing / partial / project-only / lower-experience-only / DES-needed> | <reason>
- None

HOTDOG HANDOFF:
- <Experience ID or Project> B<n>: keywords=<smallest useful planned JD terms>; source=<Story label or Approved DES ID>; preserve=<why>

QUALITY RESULT:
READY
--------
```

### LinkedIn Outreach

Return LinkedIn outreach outside the JSON:

```text
LINKEDIN OUTREACH
Recruiter LinkedIn Message:
<300 characters or fewer>

Hiring Manager LinkedIn Message:
<300 characters or fewer>

Recruiter/HM Search Strings:
<4 search strings>
```

Use only final JSON, JD, company, and title. Keep messages direct and specific. Do not use hype, flattery, desperation, buzzwords, em dashes, or long technology lists.

### Final JSON Verification

Before returning the JSON, silently verify:

```text
- JSON parses.
- Top-level keys are exactly type, experience, projects, skills.
- Configuration order, metadata, bullet counts, project count, and skill limits are followed.
- No top-level summary exists.
- Every standard Experience entry has the configured bullet count.
- Every selected Project has exactly 2 bullets unless configuration says otherwise.
- Every bullet uses a strong verb.
- No weak opener remains.
- Every bullet answers WHAT, HOW, WHERE, WHY, and RESULT/REASON.
- Every keyword in a bullet is exact, capability-layer-safe, Story-supported, or approved-DES-supported.
- Approved DES keywords are preserved when important, scoped, and compact.
- Skills are minimal and traceable.
```
