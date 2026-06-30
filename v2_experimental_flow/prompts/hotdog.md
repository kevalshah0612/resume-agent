# Blind Recruiter Review and JSON Repair Prompt

## Inputs

```text
JD:
<paste the complete job description>

Current Resume JSON:
<paste the generated resume JSON>
```

Use only these two inputs.

Do not use Story files, DES, prior analysis, external knowledge, assumptions, job titles, project names, or Skills as evidence.

The Current Resume JSON is the factual boundary.

You may use facts already stated within the same Experience entry or the same Project to improve a bullet, but only when the JSON clearly connects those facts to the same work.

Do not add a technology, responsibility, result, metric, user, workflow, business outcome, qualification, or claim that is not explicitly present in the Current Resume JSON.

Do not change:

```text
- top-level JSON structure;
- title, company, location, dates, or project name;
- number of Experience entries;
- number of Projects;
- number, order, or position of bullets inside any Experience entry or Project.
```

---

## Goal

Review the resume as a recruiter would review it for this JD.

The goal is to maximize clear, qualification-based ATS coverage, mainly through Experience, while repairing:

```text
- hot dogs;
- keyword dumps;
- repeated meaningful technologies or qualifications;
- vague wording;
- missing context;
- missing nontechnical reason;
- weak recruiter readability;
- bullets that do not clearly prove the JD qualification.
```

A valid Experience or Project bullet must communicate:

```text
What was done
+ How the relevant JD terms were used
+ Where or in what system/workflow it happened
+ Why it mattered in plain-language, nontechnical terms
```

The nontechnical reason should explain what improved for users, operations, stakeholders, security, compliance, customers, researchers, or delivery teams.

---

## Blind Review Boundary

This is a blind recruiter review.

You do not know whether a claim is true outside the Current Resume JSON.

Therefore:

```text
- Judge whether a claim is clear, relevant, specific, and qualification-based.
- Do not judge whether a claim is factually true outside the JSON.
- Do not add missing evidence.
- Do not infer a capability from a similar tool, job title, project name, or nearby keyword.
- Do not convert an implied capability into an explicit claim.
- Do not use Skills as proof of a qualification.
```

You may remove, shorten, reorder, or rewrite facts already present in the same Experience entry or Project.

You must preserve the factual meaning of the remaining content.

---

## JD Qualification Extraction

Extract bullet qualification groups only from explicit JD candidate-criteria sections.

Examples include sections that clearly introduce:

```text
Requirements
Qualifications
Required Skills
Specific Skills
Minimum Qualifications
Preferred Qualifications
Must Have
Need to Have
What You Bring
What You Need
or equivalent candidate-criteria language
```

Do not create ATS qualification groups from:

```text
Responsibilities
Duties
What You Will Do
About the Role
Company information
Benefits
Compensation
Legal text
Application instructions
```

Responsibilities may help judge whether a bullet sounds role-relevant, but they do not count as ATS qualification groups.

Classify JD items as:

```text
BULLET-PROVABLE:
A skill, practice, system, tool, or capability that can be shown in Experience or Projects.

PROFILE FACT:
Degree, years, location, work authorization, relocation, compensation, or similar fact.
Do not count it in bullet ATS coverage.

NOT BULLET-PROVABLE:
A requirement that cannot reasonably be proven through a resume bullet.
```

---

## ATS Coverage Calculation

For every literal bullet-provable JD qualification group, classify it as:

```text
EXPERIENCE-PROVEN:
Clearly proven in an Experience bullet through What, How, Context, and nontechnical Why.

PROJECT-PROVEN:
Clearly proven only in a Project bullet.

SKILLS-ONLY:
Appears only in Skills. Does not count as qualification proof.

NOT-PROVEN:
Not clearly proven in the Current Resume JSON.
```

Calculate:

```text
Experience ATS Coverage =
number of literal bullet-provable JD qualification groups proven in Experience
/
number of literal bullet-provable JD qualification groups in the JD
```

Do not count a keyword merely because it appears.

A term counts only when the bullet clearly shows:

```text
What was done
How the term was used
Where or in what workflow it was used
Why it mattered in plain language
```

Projects may add supplemental coverage, but Experience remains the primary source of proof.

---

## Hot-Dog Rule

A hot dog is a technically real detail that does not help:

```text
- prove a literal JD qualification;
- explain how that qualification was used;
- provide necessary work context; or
- explain the plain-language, nontechnical reason it mattered.
```

A tool, framework, database, metric, benchmark, implementation detail, or adjacent accomplishment is a hot dog when it does not serve one of those four jobs.

Remove hot dogs at the phrase level.

Never remove an entire bullet because it contains hot dogs.

### Good and Bad Examples

```text
Bad:
Built <tool A>, <tool B>, <tool C>, and <tool D> services.

Why it fails:
It is a technology list. It does not show the work context or why it mattered.

Good:
Built <JD capability> with <tool A> and <tool B> for <workflow>,
allowing <user or team> to <plain-language outcome>.

Why it works:
It shows What, How, Context, and nontechnical Why.
```

```text
Bad:
Improved <technical metric> using <tool A>, <tool B>, and <tool C>.

Why it fails:
The reader cannot understand the work context or the real business reason.

Good:
Automated <JD workflow> with <tool A> in <verified context>,
reducing manual <task> for <stakeholder group>.

Why it works:
The qualification, context, and plain-language value are clear.
```

---

## Experience and Project Rules

### Experience Summary Bullet

The first bullet in each Experience entry must:

```text
- use 1 to 3 highest-priority JD qualification groups when supported by the JSON;
- summarize the candidate’s role-relevant work simply;
- include What, How, Context, and nontechnical Why;
- avoid a technology inventory;
- use past tense;
- contain one sentence, no more than one period, and 25 words or fewer.
```

### Later Experience Bullets

Every later Experience bullet must:

```text
- use 3 to 6 distinct, meaningful JD qualification groups when the JSON supports them;
- prove a different work slice;
- include What, How, Context, and nontechnical Why;
- use past tense;
- contain one sentence, no more than one period, and 25 words or fewer;
- avoid keyword dumping.
```

### Project Bullets

Every Project bullet must:

```text
- use 3 to 6 distinct, meaningful JD qualification groups when the JSON supports them;
- prove a distinct project work slice;
- include What, How, Context, and nontechnical Why;
- use past tense;
- contain one sentence, no more than one period, and 25 words or fewer;
- avoid feature lists and technology inventories.
```

Do not invent terms merely to reach the preferred qualification-group range.

---

## Repeat Locks

Within the same Experience entry or Project, do not repeat a meaningful group already used in an earlier bullet when a truthful alternative exists.

Meaningful groups include:

```text
programming language
framework
database
cloud provider
queue or cache
API type
security or access term
testing or delivery tool
primary JD qualification group
```

Treat acronyms, full names, aliases, alternate spellings, and equivalent names as one group.

Normal grammar words may repeat when needed:

```text
application
service
workflow
user
team
data
release
request
```

Do not make writing unnatural merely to avoid normal words.

---

## Bullet Preservation Rule

Preserve every bullet.

```text
- Never delete, blank, merge, move, or replace a bullet with a placeholder.
- Never remove an Experience entry or Project.
- Every input bullet must have one corrected output bullet in the same entry and position.
- Preserve the exact bullet count and bullet order.
- Remove hot-dog phrases only at phrase level.
- Retain at least one substantive accomplishment from every original bullet.
```

When a bullet is weak:

```text
1. Keep its strongest verified accomplishment.
2. Keep the highest-value JD qualification already present in the bullet.
3. Remove unrelated hot-dog phrases, extra tools, decorative metrics, or vague language.
4. Reorder the remaining facts to make What, How, Context, and Why clear.
5. Use a factual operational outcome already stated in the same bullet or same entry only
   when the JSON clearly connects it to the same work.
6. Rewrite the bullet as a concise recruiter-readable qualification.
```

If the JSON does not contain enough information for a full nontechnical reason:

```text
- do not invent a user, business benefit, workflow, metric, or outcome;
- retain and improve the bullet anyway;
- use the closest supported operational value;
- mark the limitation as CONSTRAINED in the review.
```

---

## Repair Status

Review every Experience and Project bullet using only these statuses:

```text
PASS:
The bullet already meets the rules and remains unchanged.

REPAIR:
The bullet must be rewritten, shortened, reordered, or clarified using only facts
already present in the same Experience entry or Project.
```

Do not use a `REMOVE` status.

Repair every bullet marked `REPAIR`.

Keep `PASS` bullets unchanged unless a minimal change is necessary to resolve a repeated meaningful term within that same entry.

---

## Repair Requirements

A repaired bullet must:

```text
- use only facts already present in the same Experience entry or Project;
- preserve factual meaning;
- retain at least one substantive accomplishment from the original bullet;
- remove hot dogs at phrase level;
- state What clearly;
- state How the relevant qualification was used;
- state Where or in what system/workflow it happened;
- state the strongest supported plain-language nontechnical Why;
- use exact JD terms only when they already appear explicitly in the JSON;
- avoid repeating locked meaningful groups when a truthful rewrite is possible;
- use past tense;
- start with one direct action verb;
- contain one sentence, no more than one period, and 25 words or fewer;
- avoid stacked opening verbs;
- avoid buzzwords, generic corporate filler, AI-sounding phrasing, em dashes,
  unexplained acronym chains, and vague endings.
```

Do not add an unproven JD term to increase ATS coverage.

Do not add a new tool, outcome, system, user, responsibility, metric, or business reason.

---

## Skills Repair

Rebuild Skills after Experience and Projects are repaired.

Keep only Skills that:

```text
- appear directly in a final Experience or Project bullet; and
- are relevant to the target JD.
```

Do not use Skills to repair missing Experience evidence.

Remove:

```text
duplicates
aliases
unsupported terms
unrelated technologies
terms that appear only in the original Skills list
```

Do not change the JSON schema.

---

## Required Output

Return exactly two parts.

### Part 1: BLIND RECRUITER REVIEW

```text
BLIND RECRUITER REVIEW

ROLE TARGET:
<target role>

JD QUALIFICATION GROUPS:
<comma-separated bullet-provable qualification groups>

EXPERIENCE ATS COVERAGE:
<proven>/<total> | <percentage>

PROJECT COVERAGE:
<distinct groups proven only in Projects or None>

BULLET REVIEW:
<Experience or Project> | Bullet <number> | PASS / REPAIR
- Missing element: <What / How / Context / Nontechnical Why / None>
- Hot dog phrase removed: <exact phrase or None>
- Repeated group corrected: <term or None>
- JD qualification retained: <group or None>
- Constraint: <None or "Nontechnical reason cannot be fully verified from JSON alone">

GAPS:
<JD qualification groups not clearly proven in the JSON, or None>

REPAIR SUMMARY:
<bullets changed and concise reason>
```

Do not reveal hidden reasoning.

### Part 2: CORRECTED JSON

Return the corrected JSON using the exact same top-level schema as the input JSON.

---

## Final Validation

Before returning the corrected JSON, verify:

```text
[ ] The exact number and order of Experience and Project bullets were preserved.
[ ] No bullet, Experience entry, or Project was deleted, merged, blanked, moved,
    or replaced with a placeholder.
[ ] Titles, companies, locations, dates, project names, and JSON structure are unchanged.
[ ] Experience remains the primary source of ATS coverage.
[ ] Every summary uses 1 to 3 primary JD qualification groups when supported.
[ ] Every later Experience and Project bullet uses 3 to 6 groups when supported.
[ ] Every final bullet clearly includes What, How, and Context.
[ ] Every final bullet uses the strongest supported plain-language nontechnical Why.
[ ] Any missing nontechnical Why is marked CONSTRAINED rather than invented.
[ ] Hot dogs were removed at phrase level without deleting bullets.
[ ] No new factual claim was added.
[ ] No meaningful term repeats within an Experience or Project entry when a truthful
    repair was possible.
[ ] Skills were rebuilt only from final Experience and Project evidence.
[ ] ATS coverage was calculated from qualification proof, not keyword presence.
```
