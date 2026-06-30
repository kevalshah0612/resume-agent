# Resume Generation Prompt — V11: Core Qualification Bullet Engine

## Purpose

Generate only the **Experience**, **Projects**, and **Skills** content for one role-targeted resume.

The goal is simple:

> **Maximize truthful JD qualification coverage in Experience first, while making every bullet a clear qualification rather than a keyword list.**

Do not try to prove every technology in the evidence bank. Do not write a generic resume. Do not use unrelated technical detail merely because it is real.

A resume bullet is valid only when it proves a relevant qualification through:

```text
WHAT:
What was built, changed, delivered, handled, tested, released, or fixed.

HOW:
How the relevant JD terms were used through verified technology, method, or practice.

WHERE / CONTEXT:
Where the work happened: application, service, workflow, integration, data process,
release path, user journey, or project.

WHY:
The plain-language, nontechnical reason it mattered:
what improved for users, stakeholders, operations, security, compliance, customers,
researchers, or delivery teams.
```

The four elements may appear in any natural order. The nontechnical reason is required. A technical result alone is not enough.

---

## Inputs

```text
JD:
<paste the complete job description>

Company:
<paste the company name>

DES (optional):
<paste plain-English candidate-confirmed evidence, missing tools, work context,
or emphasis instructions relevant to this application>
```

Python supplies these immutable inputs separately:

```text
Candidate Profile:
- titles, employers, locations, dates, education, work authorization, relocation,
  and approved header facts.

Resume Configuration:
- Experience entries and order;
- whether consecutive roles are merged for AIML output;
- required project count;
- bullet count per entry.

Evidence Bank:
- Story.md;
- verified Project Bank.
```

Do not change Candidate Profile or Resume Configuration.

---

## Source Rules: Verify Before Writing

Use only:

```text
1. Literal JD qualification criteria;
2. Candidate-confirmed DES;
3. Verified Evidence Bank;
4. Candidate Profile for profile facts only.
```

Never guess, infer, broaden, substitute, or upgrade a claim.

```text
- A similar tool does not prove the named JD tool.
- A generic category does not prove one specific member of that category.
- A project name, title, Skills item, dependency list, or adjacent story is not proof.
- A technology mentioned in one job cannot be moved to another job without direct evidence.
```

### Dynamic DES Rule

DES is candidate-confirmed evidence written in plain English.

Use only the scope the candidate explicitly states.

```text
- If DES names a high-priority JD term and the relevant Experience entry or Project,
  prioritize it in that entry.
- If DES provides enough What, How, Context, and Why, the term may appear in a bullet.
- If DES confirms only minor tool familiarity without usable context, it may appear in
  Skills only when it is JD-relevant and linked to a specific entry.
- Do not expand a DES-confirmed tool into unconfirmed workflows, outcomes, or related capabilities.
```

### Evidence Ledger

Before drafting, create an internal ledger for every selected JD group:

```text
JD group | exact JD wording | evidence source | allowed Experience/Project entry | priority
```

A JD group without a verified source is a gap. Do not use it.

Do not reveal chain-of-thought. In visible analysis, show only a concise evidence and allocation summary.

---

## JD Qualification Extraction

Extract bullet qualifications only from explicit JD **candidate-criteria** sections, such as sections that state:

```text
requirements
qualifications
required skills
specific skills
minimum qualifications
preferred qualifications
must have
need to have
what the candidate brings
what the candidate needs
```

Use the meaning of the heading, not an exact heading name.

Do not create qualification groups from:

```text
responsibilities
duties
what the person will do
company description
benefits
compensation
legal notices
application instructions
```

Responsibilities may help describe the work context, but they never create ATS keyword targets, coverage groups, Skills, or unsupported bullet claims.

Classify extracted JD items:

```text
A. Bullet Evidence Terms:
   Skills, tools, practices, systems, and capabilities that can be proven in bullets.

B. Profile Facts:
   Degree, years, location, work authorization, relocation, compensation, and similar
   facts controlled by Candidate Profile. Do not force these into bullets.

C. Gaps:
   Terms without Story Bank or DES evidence. Do not invent them.
```

---

## Coverage Plan

Create one canonical list of literal, bullet-provable JD qualification groups.

```text
Experience coverage =
number of JD groups proven in Experience bullets
÷
number of bullet-provable JD groups in the JD
```

Target approximately 75% **when verified evidence supports it**. The target is a diagnostic, never permission to invent, stretch, or stuff terms.

### Allocation Order

1. Cover the highest-priority verified JD groups in Experience.
2. Put the strongest high-priority proof in the first configured Experience entry.
3. Use later Experience entries for different verified JD groups or distinct verified stack evidence.
4. Use Projects only for distinct remaining gaps or complementary evidence.
5. Build Skills last.

When multiple languages, stacks, or technologies are literal JD requirements, different Experience entries may specialize in different verified terms. Do not force one stack into every entry.

---

## Experience Structure

Each Experience entry follows the configured bullet count. Normally it has three bullets.

### Bullet 1: Experience Summary

The first bullet is a simple role summary.

It must:

```text
- use 1 to 3 primary JD qualification groups;
- state what the candidate delivered or handled;
- state how the primary qualification was used;
- state the work context;
- state a plain-language, nontechnical reason it mattered;
- be past tense, one sentence, one period maximum, and 25 words or fewer;
- be understandable to a nontechnical reader;
- avoid low-priority tools, several databases, and technology inventories.
```

The summary is not required to use 3 to 6 groups.

### Later Experience Bullets

Every non-summary Experience bullet must:

```text
- use 3 to 6 distinct, meaningful JD qualification groups;
- prove a different verified work slice;
- include What, How, Where/Context, and a plain-language nontechnical Why;
- be past tense, one sentence, one period maximum, and 25 words or fewer;
- begin with one direct action verb;
- use only terms assigned to that bullet.
```

Do not add a later bullet unless a distinct, verified qualification slice exists.

---

## Project Structure

Projects are supplemental, not replacements for relevant Experience.

Select only configured-count projects that add a distinct, role-relevant, verified context. Return fewer only when another project would be irrelevant or unverified.

Every Project bullet follows the same formula and validation rules as a later Experience bullet:

```text
- 3 to 6 distinct, meaningful JD qualification groups;
- What, How, Where/Context, and plain-language nontechnical Why;
- one sentence, one period maximum, past tense, 25 words or fewer;
- a distinct verified project slice from the other bullet.
```

Do not use a project as a feature list, technology inventory, or a substitute for missing professional evidence.

---

## Exact Terms, Acronyms, and Punctuation

### Exact-Term Rule

Use a named technology, method, or capability only when:

```text
- it is a literal JD qualification; or
- it is necessary verified support for explaining the selected JD qualification.
```

Do not add adjacent tools simply because they appear in the same story.

### Acronym Rule

Use the full term and acronym together only at the first meaningful proof point when the expansion is standard and supported.

```text
<Full Term> (<ACRONYM>)
```

Treat the full term and acronym as one qualification group. Do not repeat the acronym or full term in another bullet within the same entry.

### Punctuation Rule

Clearly separate distinct named technologies.

```text
Good:
Built <JD capability> with <tool A>, <tool B>, and <tool C> for <workflow>.

Bad:
Built <tool A> <tool B> <tool C> services for <workflow>.
```

Use commas between three or more named terms and `and` before the final item.

---

## Hot-Dog Rule

A “hot dog” is a technically real detail that does not help prove the allocated JD qualification.

Keep a phrase only when it does at least one of these jobs:

```text
- proves an allocated JD qualification;
- explains how the qualification was used;
- provides necessary work context;
- explains the plain-language nontechnical reason it mattered.
```

Remove the phrase when it does none of these jobs.

### Good and Bad Examples

```text
Bad:
Built <tool A>, <tool B>, <tool C>, and <tool D> services.

Why it fails:
It is a tool list. It does not show the work context or why anyone benefited.

Good:
Built <JD capability> with <tool A> and <tool B> in <workflow>,
allowing <user or team> to <plain-language outcome>.

Why it works:
It shows What, How, Where, and nontechnical Why, while keeping only the tools
needed for the qualification.
```

```text
Bad:
Improved <technical metric> with <tool A>, <tool B>, and <tool C>.

Why it fails:
The technical metric does not explain the business purpose or user benefit.

Good:
Automated <JD workflow> with <tool A> in <verified context>,
reducing manual <task> for <stakeholder group>.

Why it works:
The qualification is clear, the context is clear, and the nontechnical value is clear.
```

---

## Entry-Level Repeat Locks

Before drafting an Experience or Project entry, allocate distinct qualification groups to its bullets.

After a bullet passes validation, lock its meaningful terms for the rest of that entry:

```text
- programming languages;
- frameworks;
- databases;
- cloud providers;
- queues and caches;
- API types;
- authentication and authorization terms;
- testing and delivery tools;
- primary JD qualification groups;
- meaningful core system phrases when another distinct work slice is available.
```

Treat an acronym, full name, alternate spelling, and equivalent alias as the same group.

Do not repeat a locked meaningful term in the same entry.

Ordinary grammar words may repeat only when needed for clear writing:

```text
user, team, application, service, workflow, data, release, request
```

Avoid repeating the same opening verb within an entry or adjacent bullets when a natural truthful alternative exists. Do not force globally unique verbs across the whole resume.

---

## Immediate Draft-and-Validate Loop

Write one bullet at a time.

### Step 1: Allocate

For the current Experience or Project entry:

```text
- select verified JD groups;
- assign distinct groups to each bullet;
- identify the exact Story Bank or DES evidence;
- identify the nontechnical reason each bullet matters;
- create the initial term-lock list.
```

### Step 2: Draft

Write one completed bullet using only its allocated qualification groups and evidence.

### Step 3: Validate Before Moving On

Reject and rewrite the bullet unless every check passes:

```text
EVIDENCE
[ ] Every technology, outcome, metric, user, and ownership claim is directly verified.
[ ] Every term stays within the stated DES scope when DES is the source.
[ ] No similar, adjacent, implied, or guessed term appears.
[ ] Every retained tool is a literal JD term or necessary support for one.

QUALIFICATION
[ ] Summary: 1 to 3 primary JD groups.
[ ] Other Experience or Project bullet: 3 to 6 meaningful JD groups.
[ ] What is clear.
[ ] How the JD terms were used is clear.
[ ] Where or in what system/workflow it happened is clear.
[ ] The plain-language, nontechnical reason it mattered is clear.

HOT-DOG AND REPEAT CHECK
[ ] Every meaningful phrase proves the qualification, explains How, provides Context,
    or explains nontechnical Why.
[ ] No unrelated technical detail, tool inventory, or decorative metric remains.
[ ] No locked meaningful term or alias repeats from an earlier bullet in this entry.

WRITING
[ ] Past tense.
[ ] One sentence and one period maximum.
[ ] 25 words or fewer.
[ ] One direct action verb at the start.
[ ] No stacked opening verbs.
[ ] No em dash.
[ ] No dense unexplained acronym chain.
[ ] No buzzwords, hype, generic corporate filler, or AI-sounding language.
[ ] No vague ending such as “for performance,” “for reliability,” or “for scalability”
    without explaining the real effect on people, work, security, or operations.
[ ] Distinct named terms are comma-separated when needed.
```

If any check fails, rewrite the same bullet. Do not draft the next bullet.

### Step 4: Lock

Only after the bullet passes:

```text
1. Add its meaningful terms to the entry term-lock list.
2. Remove those groups from later bullet allocations.
3. Draft the next bullet.
```

### Step 5: Entry Check

After the entry is complete:

```text
[ ] Each bullet proves a distinct qualification slice.
[ ] The summary is a role summary, not a tool list.
[ ] No meaningful qualification repeats within the entry.
[ ] The entry tells one coherent, role-relevant story.
[ ] The bullets maximize verified JD coverage without hot dogs.
```

---

## Human Writing Rules

Use direct, natural past-tense verbs when true.

Do not use:

```text
- stacked openings such as “Designed and built”;
- em dashes;
- hype, buzzwords, or generic corporate filler;
- vague claims without a plain-language result;
- long technical benchmark dumps;
- dense, unexplained technology chains.
```

Write for a recruiter, manager, executive, or eight-year-old at the business-purpose level, while preserving the technical proof a hiring manager needs.

Use numbers only when verified, explainable in an interview, and necessary to show meaningful user, business, team, or operational scale. Prefer plain-language value over technical benchmark numbers.

For non-AIML roles, remove AI/ML claims unless the JD explicitly requires them.

---

## Skills

Build Skills only after Experience and Projects are final.

A skill may appear only when:

```text
1. It appears directly in a final Experience or Project bullet and is verified; or
2. It is a DES-confirmed, JD-relevant minor tool linked to a specific Experience or Project,
   but lacks enough context for an honest bullet.
```

A Skills-only item does not count as bullet-proven ATS coverage.

Keep Skills short, technical, role-specific, and deduplicated.

Return only 8 to 14 total skills unless the JD clearly requires more.

Prefer literal JD qualification terms that also appear in final Experience or Project bullets.

Do not include every technology from Story.md. Do not include tools used only in weak, unrelated, or removed bullet drafts.

Do not include soft skills, generic phrases, unsupported tools, approximate claims, or aliases used to inflate coverage.

---

## Concise Analysis Output

Return a short `ANALYSIS` before JSON:

```text
ANALYSIS

JD QUALIFICATIONS:
<comma-separated Bullet Evidence Terms only>

EVIDENCE AND ALLOCATION:
Experience 1: Summary <groups>; Bullet 2 <groups>; Bullet 3 <groups>
Experience 2: Summary <groups>; Bullet 2 <groups>; Bullet 3 <groups>
Experience 3: Summary <groups>; Bullet 2 <groups>; Bullet 3 <groups>
Projects: <project and groups, or None>

ATS COVERAGE:
Experience: <proven>/<bullet-provable JD groups> | <NN%>
Projects add: <distinct supplemental groups or None>

GAPS:
<unverified JD terms or None>

FINAL VALIDATION:
Every final bullet passed evidence, formula, hot-dog, punctuation, term-lock,
and writing checks.
```

Do not show hidden reasoning or draft bullet alternatives.

---

## JSON Output

Return valid JSON immediately after ANALYSIS, with exactly these top-level keys in this order:

```json
{
  "type": "Backend | Fullstack | AIML",
  "experience": [
    {
      "title": "<Candidate Profile title>",
      "company": "<Candidate Profile company>",
      "location": "<Candidate Profile location>",
      "dates": "<Candidate Profile dates>",
      "bullets": [
        "<final bullet>",
        "<final bullet>",
        "<final bullet>"
      ]
    }
  ],
  "projects": [
    {
      "name": "<verified project name>",
      "bullets": [
        "<final bullet>",
        "<final bullet>"
      ]
    }
  ],
  "skills": [
    "<verified skill>"
  ]
}
```

---

## Final Gate

Do not return JSON until the final text, not just the plan, passes all checks:

```text
[ ] JD groups came only from explicit candidate-criteria sections.
[ ] Candidate Profile facts were not turned into bullet claims.
[ ] Every claim came from the Evidence Bank or DES.
[ ] Every DES claim stayed within its explicit scope.
[ ] Experience carries maximum verified JD coverage before Projects.
[ ] Summary bullets use 1 to 3 primary groups.
[ ] Other Experience and Project bullets use 3 to 6 distinct groups.
[ ] Every bullet includes What, How, Where/Context, and a plain-language,
    nontechnical Why.
[ ] Every bullet is past tense, one sentence, one period maximum, and 25 words or fewer.
[ ] No hot dogs remain.
[ ] No meaningful terms repeat within an Experience or Project entry.
[ ] Named terms are exact and clearly punctuated.
[ ] Skills are traceable to final bullets or permitted DES-confirmed Skills-only evidence.
[ ] ATS coverage is calculated from bullet-proven Experience evidence, not Skills.
[ ] No unsupported claim, metric, tool, project detail, or profile fact appears.
[ ] JSON contains only type, experience, projects, and skills.
```

If a requirement cannot be met without guessing, omit it and list it under GAPS.
