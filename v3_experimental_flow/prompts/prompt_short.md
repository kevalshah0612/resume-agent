# V3 Short Instructions

Read `prompt.md` first and follow it exactly.

Use this profile only for Experience, Projects, Skills, LinkedIn outreach, and the visible V3 bullet checks.

Do not create a top-level resume summary. `Summary` means bullet 1 inside each standard Experience entry only.

## PASS 1

When RUN MODE is `PASS 1 - TECH KEYWORD PLAN`, do not write final bullets, skills, or JSON.

Do this:

1. Extract only TECH KEYWORDS and JD VERBS / ACTION WORDS.
2. Build a JD.docx-style `TECH KEYWORD LINE`.
3. Decide `PRIMARY TECH`, `SECONDARY TECH`, and `SUPPLEMENTAL TECH`.
4. Match JD words to Story.md through the capability layer.
5. Put primary tech in the first visible Experience Summary when supported.
6. If the JD is AI/ML/LLM-focused and the configuration supports GHI first, put the AI/ML primary tech in the GHI Summary.
7. Assign the smallest useful JD terms to each Summary, Bullet 1, and Bullet 2 target, usually 2 to 4 and max 5 only when required.
8. Put about 75% of supported minimum tech keywords in the first half page target when possible.
9. Create KEYWORD MAP for every important extracted JD tech keyword.
10. Create MISSING KEYWORD MAP for every missing, partial, lower-experience-only, or project-only keyword.
11. Create scoped DES candidates for important missing or partial words.
12. Stop.

PASS 1 output must use this compact shape with blank lines between sections:

```text
TECH KEYWORD LINE:
- <JD.docx-style line>

PRIMARY TECH:
- <keyword> | reason: <why>

SECONDARY TECH:
- <keyword> | reason: <why>

SUPPLEMENTAL TECH:
- <keyword> | reason: <why>

JD VERBS:
- <strong verb>

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

KEYWORD MAP and MISSING KEYWORD MAP are required. Do not replace them with a short coverage summary.

## Capability Layer

Story.md guides direction. It is not a word-matching cage.

## JD Surface Terms

Use the current JD's exact surface term when the scoped evidence supports the same capability.

```text
Preserve JD spelling, casing, spacing, version suffixes, and product names.
If the JD uses a versioned or specific term and Story.md proves the same capability, write the JD term.
If the JD term is a materially different technology, platform, product, framework, cloud, database, or architecture claim, require Story.md support or approved DES.
```

Separate every tech term with commas in keyword lines, placement plans, bullets, analysis, and skills. Do not use slash chains, unpunctuated tool runs, or parentheses to pack extra tools.

## JD-Only Technology Selection

Use named technologies from the current JD first.

Do not dump every technology from Story.md. Story.md proves capability; the JD decides which named tech belongs in bullets and skills.

When Story.md supports several interchangeable tools in the same family, such as databases, clouds, API frameworks, testing tools, UI frameworks, or monitoring tools:

```text
- If the JD names one specific tool, use only that JD-named tool when the scoped story supports the same capability.
- If the JD names a broad family term, use the JD's broad term or one strongest supported tool, not the full story inventory.
- If the JD names multiple tools in the same family, include only the planned JD-relevant tools needed to prove the bullet.
- If a story-only tool is not in the JD, avoid naming it in bullets and skills; use capability wording instead.
```

This rule is dynamic. Do not hardcode a fixed technology list. Extract tech keywords from the current JD, then use only the smallest truthful set that proves the qualification.

Allowed:

```text
Java backend evidence may support object-oriented programming, backend services, API development, stakeholder-facing business systems, or server-side engineering.
Python evidence may support backend programming, scripting, data processing, automation, APIs, or AI/ML support when the scoped story supports that work.
JavaScript, TypeScript, React, Node.js, or Next.js evidence may support fullstack, frontend, web application, or JavaScript ecosystem capability.
Verified API framework work may support backend API experience.
AWS, Azure, or GCP evidence may support cloud experience.
Verified CI/CD, release, test, deployment, or Git work may support delivery engineering.
```

Not allowed:

```text
Do not rename one specific technology as another.
Do not turn Docker Compose into Kubernetes.
Do not turn REST API into OpenAPI unless evidenced or approved.
Do not turn cloud work into Terraform unless evidenced or approved.
Do not turn OpenAI API into RAG, agents, MLOps, ML, model evaluation, or production AI unless evidenced or approved.
Do not turn AI-assisted coding into AI product integration.
```

The model may create plain wording, nontechnical WHY, and qualitative result/reason from real story context. It may not invent concrete named tools, platforms, metrics, user groups, domains, production claims, security claims, AI/ML claims, business outcomes, leadership claims, or scale.

## DES

Approved DES is evidence for its named scope only.

If an approved DES keyword is important to the JD, place it into the planned bullet for that scope.

Hotdog must preserve approved DES when it is scoped, JD-relevant, compact, and not contradicted.

Use handoff:

```text
HOTDOG HANDOFF:
- <Experience ID or Project> B<n>: keywords=<smallest useful planned JD terms>; source=<Story label or Approved DES ID>; preserve=<why>
```

## PASS 2

When RUN MODE is `PASS 2 - WRITE APPROVED RESUME JSON`, use the approved PASS 1 plan and approved DES.

Write as a FAANG senior engineering manager. Verify as a recruiter and nontechnical hiring manager.

Build:

1. Experience
2. Projects
3. Skills

Each bullet must answer:

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

The bullet must show the outcome, not just tell the story.

The WHY and RESULT/REASON must be a clear nontechnical user, stakeholder, team, or business reason.

Do not write a bullet that only lists technologies. Connect actual work to a mechanism and a user, stakeholder, team, or business impact.

Use the smallest useful set of important JD tech keywords or capability terms when supported. Prefer 2 to 4 JD tech keywords in a 22 to 25 word bullet. Use 5 only when the JD truly requires the cluster and the sentence still reads naturally. Never stuff.

## Strong Verbs Only

Prefer:

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

Never open bullets with:

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

## Visible Checks

After each final bullet in PASS 2 analysis, print:

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

If any check fails, rewrite the bullet before showing it. Do not show failed drafts.

## Compact Style

```text
All resume bullets: target 22 to 25 words.
Hard max: 25 words.
If a bullet needs more than 25 words, remove extra tech, adjectives, or process detail before dropping WHAT, HOW, WHERE, WHY, or RESULT.
```

Use past tense, one sentence, exactly one period, strong verb, plain language, user/business impact, and no buzzwords.

Avoid unnecessary numbers. Use metrics only when real, supported, and useful.

## Output

PASS 2 returns exactly:

1. `ANALYSIS`
2. `LINKEDIN OUTREACH`
3. One valid JSON object

Leave blank lines between major sections.

Do not wrap JSON in Markdown fences. Do not write anything after JSON.

JSON top-level keys must be exactly:

```text
type
experience
projects
skills
```

No top-level summary.
