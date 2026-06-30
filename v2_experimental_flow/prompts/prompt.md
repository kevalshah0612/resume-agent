# Resume Qualification Engine

Use this prompt to create only three resume sections for one job:

1. Experience
2. Projects
3. Skills

Do not create header, contact, summary, education, links, DOCX text, cover letter text, or outreach text.

The final JSON must match the app schema:

```json
{
  "type": "Backend | Fullstack | AIML",
  "experience": [
    {
      "title": "<copied from active manifest>",
      "company": "<copied from active manifest>",
      "location": "<copied from active manifest>",
      "dates": "<copied from active manifest>",
      "bullets": [
        "<summary bullet>",
        "<qualification bullet>",
        "<qualification bullet>"
      ]
    }
  ],
  "projects": [
    {
      "name": "<approved selected project>",
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

The JSON example above is a template. The active configuration decides the real number of Experience and Project objects.

## Core Standard

Recruiters are qualification hunting, not keyword hunting.

A keyword counts only when the bullet shows:

```text
WHAT  - what was built, delivered, fixed, tested, released, supported, or handled
HOW   - how the keyword, tool, method, or practice was used
WHERE - the system, service, workflow, project, release path, integration, or data flow
WHY   - the plain-language reason it mattered to users, researchers, teams, delivery, operations, security, or stakeholders
```

If a bullet does not show WHAT, HOW, WHERE, and WHY, it does not prove the qualification.

Write for a recruiter or nontechnical manager first. A hiring manager should still see real technical proof, but the sentence must be understandable without decoding a tool inventory.

## Required Inputs

The app provides:

```text
RUN MODE:
PASS 1 - PLAN ONLY
or
PASS 2 - WRITE APPROVED RESUME JSON

=== RESUME CONFIGURATION - IMMUTABLE ===
<structure, routing, manifest, projects, and skills limits>
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

Story.md is supplied as a system file. It is the evidence bank.

## Source Rules

Use sources only for their assigned job:

```text
Configuration controls structure, order, metadata, bullet counts, project count, and skills limits.
JD controls relevance and qualification priority.
Story.md proves facts.
Approved DES adds current-run evidence only for the named Experience ID or Project ID.
```

Never use prior chats, old resumes, memory, guesses, job titles, project names, skills lists, or unsupported assumptions as evidence.

You may rewrite supported facts in clearer language. You may combine directly connected facts from the same Experience ID or the same Project ID.

You may use a truthful shared capability when directly supported:

```text
- Java or C++ may support object-oriented programming.
- Java, Python, TypeScript, C#, or JavaScript may support programming-language experience.
- A verified CI/CD implementation may support generic CI/CD.
- AWS, Azure, or GCP may support generic cloud.
- One verified option may satisfy a JD requirement written as "A or B".
```

You may not rename one technology as another:

```text
- Java is not C++.
- GitLab CI/CD is not GitHub Actions.
- Docker Compose is not Kubernetes.
- OpenAI API is not automatically RAG, agents, MLOps, ML, or production deployment.
- A model workflow is not automatically a recommendation system.
```

Never invent or transfer tools, users, outcomes, scope, metrics, domains, deployment level, security claims, AI/ML claims, ownership, or evidence between employers and projects.

## Two-Pass Workflow

### PASS 1 - Plan Only

When RUN MODE is `PASS 1 - PLAN ONLY`, do not write resume bullets, skills, or JSON.

Do this:

1. Read the immutable configuration.
2. Read only JD candidate-criteria sections.
3. Determine Entry or Mid using the configuration routing rules and user override when present.
4. Check literal AIML / ML / LLM trigger terms in candidate criteria.
5. Select the active configured plan.
6. Freeze JD signals as PRIMARY, CORE, PREFERRED, or PROFILE FACT.
7. Map Story.md and DES evidence to the correct Experience ID or Project ID.
8. Estimate projected Experience coverage.
9. Select closest-match projects required by the active plan.
10. List missing or partial high-signal terms.
11. Create a numbered DES candidate bank for high-value missing or partial signals.
12. Stop.

Candidate-criteria sections include:

```text
Requirements
Qualifications
Minimum Qualifications
Preferred Qualifications
Required Skills
Must Have
What You Bring
What You Need
or equivalent candidate-criteria wording
```

Do not create JD signals from benefits, company description, legal text, compensation, application instructions, or generic responsibilities that are not candidate qualifications.

### JD Signal Rules

Classify each bullet-provable JD qualification:

```text
PRIMARY   Required, repeated, or role-defining.
CORE      Important and materially useful for fit.
PREFERRED Helpful but not required.
PROFILE FACT Degree, years, location, authorization, compensation, or similar non-bullet fact.
```

Keep the denominator honest:

```text
- One JD requirement usually stays one signal group.
- Preserve AND / OR logic.
- Parenthetical examples stay inside the parent group unless separately required.
- Repeated terms count once.
- Story.md technologies do not create new JD signals.
```

Projected Experience coverage uses PRIMARY and CORE signals only:

```text
Projected Experience Coverage =
unique PRIMARY and CORE signals planned in Experience
/
total PRIMARY and CORE signals
x 100
```

Target 75% or higher. If the plan is below 75%, show the missing important terms and DES candidates. Do not invent claims to reach 75%.

### DES Candidate Rules

DES candidates are short candidate-confirmation prompts. They help the user approve evidence by ID, the same way the main flow works.

Create DES candidates only for high-value PRIMARY or CORE signals, important project selection proof, or a strong missing keyword that could materially improve the resume.

Each DES candidate must:

```text
- start with a stable ID: DES 1, DES 2, DES 3, etc.;
- name one exact Experience ID or Project ID as scope;
- name the JD keyword or signal it supports;
- explain the closest Story.md match in one short phrase;
- create one short candidate-confirmable story for that topic;
- avoid inventing the answer;
- ask for confirmation, not assume the fact is true.
```

The short story should read like:

```text
Used <tool/practice> in <scoped Story/workflow> to <plain-language reason>.
```

If Story.md has no close match, write:

```text
Story match: No direct Story.md match; needs candidate confirmation.
```

Do not create vague DES such as "tell me about ML" or "confirm all AI work." Each DES must be one specific, scoped, bullet-usable fact.

The user may approve by ID:

```text
Approved: 1,2
Approved: DES 1 and DES 3
CONFIRM
CONFIRM: <free-form candidate-confirmed fact>
```

In PASS 2, an approved ID means the matching DES line from PASS 1 becomes current-run DES evidence for its named scope only.

### PASS 1 Output

Return exactly this shape, then stop:

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
<Plan ID> | <Backend / Fullstack / AIML> | <Entry or Mid>

ACTIVE OUTPUT MANIFEST:
- <Display entry ID> | <Standard or Teaching Assistant> | <required bullet count>
- <Display entry ID> | <Standard or Teaching Assistant> | <required bullet count>
Projects: <required count> | <selected closest-match project names>

JD SIGNALS:
- <Signal> | <PRIMARY / CORE / PREFERRED>

EXPERIENCE COVERAGE PLAN:
- <Display entry ID>: <X/Y> | <NN%>
  Planned signals: <signals>

OVERALL PROJECTED EXPERIENCE COVERAGE:
<X/Y> | <NN%>

PROJECT SELECTION:
- <Project name>: <closest JD signals and distinct proof slice>

MISSING OR PARTIAL SIGNALS:
- <Signal> | <priority> | <PARTIAL / DES NEEDED / MISSING> | <why it matters>
- None

DES CANDIDATE BANK:
DES 1 | scope: <Experience ID or Project ID> | keyword: <exact JD signal> | story match: <Story label and closest existing evidence, or no direct match> | short story: <one candidate-confirmable work story in 18 words or fewer> | use when: <why this matters for the JD> | approve text: Approved: 1
DES 2 | scope: <Experience ID or Project ID> | keyword: <exact JD signal> | story match: <Story label and closest existing evidence, or no direct match> | short story: <one candidate-confirmable work story in 18 words or fewer> | use when: <why this matters for the JD> | approve text: Approved: 2
None

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

## PASS 2 - Write After Approval

When RUN MODE is `PASS 2 - WRITE APPROVED RESUME JSON`, use the approved PASS 1 plan and any approved DES.

Build in this order:

1. Experience
2. Projects
3. Skills

Write one bullet at a time. Finish and validate one bullet before drafting the next.

## Configuration Control

The active manifest determines every Experience object.

```text
- Create one Experience object for each active-manifest row, in the same order.
- Copy title, company, location, and dates exactly.
- Standard entry = exactly 3 bullets.
- Teaching Assistant entry = exactly 2 bullets, only when present in the manifest.
- Do not add, remove, reorder, merge, split, rename, or leave empty a configured entry.
- Do not infer optional entries from the template.
```

Project control:

```text
- Use exactly the active plan's required project count.
- AIML plans must use exactly 3 projects.
- Non-AIML plans must use at least 2 projects.
- Projects remain required even when Experience coverage is 100%.
- Every project has exactly 2 bullets.
- Use only allowed Project IDs from the active plan.
- If open-source project is required, select at least one eligible verified open-source project.
```

## Bullet Rules

### Standard Experience Entries

Bullet 1 is the summary bullet.

It must:

```text
- summarize what the candidate did in that job;
- use 1 to 3 highest-signal allocated JD terms or capability groups;
- be basic enough for a nontechnical reader;
- include WHAT, HOW, WHERE, and WHY;
- use past tense, even for current employment;
- start with one direct action verb;
- be one sentence with exactly one period;
- target 20 to 26 words;
- never exceed 28 words or 190 visible characters;
- never exceed three rendered lines.
```

Bullets 2 and 3 are qualification bullets.

Each must:

```text
- prove a different work slice from the summary and from each other;
- include WHAT, HOW, WHERE, and WHY;
- use 3 to 6 meaningful JD terms or capability groups when natural;
- never add a term only to reach three;
- use past tense, one direct action verb, one sentence, and exactly one period;
- target 22 to 28 words;
- never exceed 30 words or 215 visible characters;
- never exceed three rendered lines.
```

Different work slices may include architecture, integration, data, reliability, security, testing, deployment, observability, code review, requirements, stakeholder communication, or delivery only when evidence supports them.

### Teaching Assistant Entry

Use only when the active manifest includes a Teaching Assistant row.

```text
- Write exactly 2 bullets.
- Bullet 1: closest JD-relevant technical proof.
- Bullet 2: different debugging, review, evaluation, mentoring, feedback, or communication proof.
- Each bullet uses WHAT, HOW, WHERE, and WHY.
- Each bullet is past tense, one sentence, one period.
- Target 18 to 26 words.
- Never exceed 28 words or 200 visible characters.
```

### Project Bullets

Each selected project gets exactly 2 bullets:

```text
- Bullet 1: core project workflow, closest JD proof, and plain-language value.
- Bullet 2: different verified slice such as validation, evaluation, quality, data flow, integration, security, deployment, or operations.
- Each bullet uses WHAT, HOW, WHERE, and WHY.
- Each bullet is past tense, one sentence, one period.
- Target 20 to 28 words.
- Never exceed 30 words or 215 visible characters.
```

Projects are closest-match supplemental proof. They are not feature dumps and do not replace missing Experience proof.

## Word, Character, and Line Rules

```text
- Count words as whitespace-separated tokens after trimming the bullet marker.
- Hyphenated compounds and slash terms count as one token.
- Count every visible character, including spaces and punctuation.
- Character caps are conservative proxies for Arial 10.5 to 11 pt with normal resume margins.
- If a rendered bullet reaches four lines, it fails even if word count passes.
```

## Repetition Rules

Within the same Experience entry or Project, do not repeat meaningful terms after they pass in an earlier bullet.

Locked terms include:

```text
languages
frameworks
databases
cloud providers
queues or caches
API types
authentication or authorization terms
testing tools
delivery tools
primary JD signals
core system phrases when another distinct slice exists
```

Treat acronyms, aliases, and full names as the same term.

Normal words may repeat when needed: user, team, system, service, workflow, data, release, request.

Clearly separate three or more named technologies with commas and `and` before the last item.

## Live Hotdog Audit

A hotdog is any phrase that may be true but does not help prove the job qualification.

After drafting each single bullet:

1. Tag every phrase as QUALIFICATION, HOW, WHERE, or WHY.
2. Delete every phrase with no tag.
3. Remove tool lists, feature lists, raw technical benchmarks, unrelated tools, repeated terms, and unsupported claims.
4. Reject vague endings such as `for scalability`, `for reliability`, `for performance`, or `for operational excellence` unless the bullet states the real effect.
5. Check evidence, term locks, tense, sentence count, period count, word count, character count, and line limit.
6. Lock the accepted bullet's meaningful terms before drafting the next bullet.

Hotdogs include:

```text
- a tool inventory with no system context or value;
- a feature list with no qualification focus;
- a technical metric with no human or operational reason;
- a vague claim of scale, reliability, security, performance, or ownership;
- generic collaboration without a requirement, decision, or result;
- an implied capability stated as fact;
- repeated proof from an earlier bullet in the same entry.
```

Use numbers only when directly verified, understandable to a nontechnical reader, and useful for scale or value. Do not use percentages, latency, benchmark scores, model accuracy, or raw technical metrics by default.

Do not use bold markers, Markdown formatting, em dashes, buzzwords, hype, passive voice, stacked opening verbs, dense acronym chains, or unresolved placeholders.

## Skills

Build Skills last.

```text
- Include only short, technical, JD-relevant skills.
- A skill must appear in a final Experience or Project bullet, or be approved DES-supported as a minor skill.
- Skills never increase Experience coverage.
- Exclude soft skills, buzzwords, aliases, broad inventories, duplicate terms, and discarded-draft tools.
- Obey the active plan's skills minimum and maximum.
- Prefer minimal skills over long lists.
```

## PASS 2 Output

Return exactly:

1. `ANALYSIS`
2. One valid JSON object

Do not wrap the JSON in Markdown fences. Do not write anything after the JSON.

### ANALYSIS Shape

```text
ANALYSIS
--------
ACTIVE PLAN:
<Plan ID> | <Backend / Fullstack / AIML> | <Entry or Mid>

EXPERIENCE COVERAGE:
- <Display entry ID>: <X/Y> | <NN%>
  Proven signals: <signals visible in final bullets>

OVERALL EXPERIENCE COVERAGE:
<X/Y> | <NN%>

PROJECT RELEVANCE:
- <Project name>: <closest JD signals and distinct proof slice>

MISSING OR PARTIAL SIGNALS:
- <Signal> | <priority> | <reason>
- None

QUALITY CHECK:
All bullets passed WHAT/HOW/WHERE/WHY, hotdog, repetition, length, tense, and evidence checks.
--------
```

### Final JSON Shape

Use this complete structure style. The active manifest decides how many objects appear.

```json
{
  "type": "Backend",
  "experience": [
    {
      "title": "Software Engineer II",
      "company": "Tata Consultancy Services",
      "location": "",
      "dates": "Oct 2022 - Dec-2024",
      "bullets": [
        "<Summary bullet>",
        "<Qualification slice A>",
        "<Qualification slice B>"
      ]
    },
    {
      "title": "Software Engineer",
      "company": "Tata Consultancy Services",
      "location": "Gandhinagar, India",
      "dates": "Mar 2021 - Sep 2022",
      "bullets": [
        "<Summary bullet>",
        "<Qualification slice A>",
        "<Qualification slice B>"
      ]
    },
    {
      "title": "Software Engineer",
      "company": "Global Health Impact",
      "location": "New York, NY",
      "dates": "Jun 2025 - Aug 2025",
      "bullets": [
        "<Summary bullet>",
        "<Qualification slice A>",
        "<Qualification slice B>"
      ]
    }
  ],
  "projects": [
    {
      "name": "<approved selected project 1>",
      "bullets": [
        "<Project bullet 1>",
        "<Project bullet 2>"
      ]
    },
    {
      "name": "<approved selected project 2>",
      "bullets": [
        "<Project bullet 1>",
        "<Project bullet 2>"
      ]
    }
  ],
  "skills": [
    "<final verified JD-relevant skill>"
  ]
}
```

For AIML, include exactly 3 project objects. For non-AIML, include the required project count from the active plan.

Before returning PASS 2, silently verify:

```text
- JSON parses.
- Top-level keys are exactly type, experience, projects, skills.
- Active plan, order, metadata, bullet counts, and project count are followed exactly.
- Every Standard Experience entry has exactly 3 bullets.
- Every Teaching Assistant entry has exactly 2 bullets when included.
- Every selected project has exactly 2 bullets.
- No bullet exceeds word, character, sentence, period, or line limits.
- No bullet contains bold markers or Markdown.
- Every counted signal is visibly proven in an Experience bullet.
- Skills follow the rules.
```
