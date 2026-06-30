# Blind Recruiter Review and JSON Repair

## Inputs

```text
JD:
<paste complete job description>

Current Resume JSON:
<paste the generated JSON>
```

Use only these two inputs.

Do not use external knowledge, prior reasoning, Story files, DES, Skills as evidence, job titles as evidence, or assumptions about the candidate.

The Current Resume JSON is the factual boundary.

You may remove, shorten, reorder, or combine facts already stated in the same Experience entry or Project.

You must not add a technology, responsibility, result, metric, user, workflow, business outcome, or JD qualification that is not already explicitly supported by the Current Resume JSON.

Do not change titles, companies, locations, dates, project names, or JSON structure.

---

## Goal

Review the JSON as a recruiter reviewing a resume for this JD.

The goal is to maximize **clear, qualification-based ATS coverage**, mainly through Experience, while removing keyword dumps, repeated terms, vague claims, and unrelated “hot dogs.”

A bullet is valid only when it clearly communicates:

```text
What was done
+ How the relevant JD terms were used
+ Where or in what system/workflow it happened
+ Why it mattered in plain-language, nontechnical terms
```

The nontechnical reason is mandatory.

---

## JD Extraction Rule

Extract qualification groups only from explicit JD candidate-criteria sections, such as:

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
or equivalent candidate-criteria headings
```

Do not create qualification targets from:

```text
Responsibilities
Duties
What You Will Do
Company information
Benefits
Compensation
Legal text
```

Responsibilities may help judge whether a bullet sounds role-relevant, but they do not count as ATS qualification groups.

---

## Blind Recruiter Review

For each literal, bullet-provable JD qualification group, classify it as:

```text
EXPERIENCE-PROVEN:
Clearly stated and qualified in an Experience bullet.

PROJECT-PROVEN:
Clearly stated and qualified only in a Project bullet.

SKILLS-ONLY:
Appears only in Skills. Does not count as qualification proof.

NOT-PROVEN:
Not clearly proven in the JSON.
```

Calculate:

```text
Experience ATS Coverage =
number of literal JD qualification groups clearly proven in Experience bullets
/
number of bullet-provable JD qualification groups
```

Do not count a keyword merely because it appears. It counts only when the bullet shows What, How, Context, and nontechnical Why.

---

## Hot-Dog Rule

A “hot dog” is a detail that may be technically real but does not help:

```text
- prove a literal JD qualification;
- explain how that qualification was used;
- provide necessary work context; or
- explain the plain-language, nontechnical reason it mattered.
```

Remove hot dogs before adding or preserving secondary detail.

A technology list, benchmark, metric, framework, database, tool, or adjacent accomplishment is a hot dog when it does not serve one of those four jobs.

---

## Entry Rules

### Experience summaries

The first bullet in each Experience entry must:

```text
- use 1 to 3 highest-priority JD qualification groups;
- give a simple role-level summary;
- include What, How, Context, and nontechnical Why;
- avoid a technology inventory.
```

### Later Experience and Project bullets

Every later Experience bullet and every Project bullet must:

```text
- use 3 to 6 distinct, meaningful JD qualification groups when the JSON supports them;
- prove a distinct work slice;
- include What, How, Context, and nontechnical Why;
- avoid keyword dumping.
```

### Repeat locks

Within the same Experience or Project entry, do not repeat meaningful terms already used in an earlier bullet:

```text
language
framework
database
cloud provider
queue or cache
API type
security/access term
testing or delivery tool
primary JD qualification group
```

Treat acronyms, full names, aliases, and equivalent spellings as the same group.

Normal words such as application, workflow, service, user, or team may repeat when necessary.

---

## Repair Rules

Review each bullet as `PASS`, `REPAIR`, or `REMOVE`.

```text
PASS:
The bullet clearly proves relevant qualifications and follows all rules.

REPAIR:
The bullet can be corrected using only facts already stated in the same Experience
entry or Project.

REMOVE:
The bullet cannot be made qualification-based without adding a new unsupported fact.
```

Repair only bullets marked `REPAIR`.

Keep passing bullets unchanged.

You may repair related bullets in the same entry only when necessary to remove repeated locked terms or restore distinct qualification coverage.

A repaired bullet must:

```text
- use only facts already present in the same Experience entry or Project;
- preserve factual meaning;
- remove hot dogs;
- state What, How, Context, and nontechnical Why;
- use exact JD terms only when they are already explicit in the JSON;
- avoid repeating locked groups;
- use past tense;
- contain one sentence, one period maximum, and 25 words or fewer;
- use one direct action verb;
- avoid stacked verbs, buzzwords, AI-sounding language, em dashes,
  unexplained acronym chains, and vague endings.
```

If a plain-language reason is not explicitly available in the JSON, do not invent one. Remove the bullet if it cannot be repaired honestly.

Do not add an unproven JD term to increase coverage.

---

## Skills Repair

Rebuild Skills after repairing Experience and Projects.

Keep only terms that:

```text
- appear in a final Experience or Project bullet; and
- are relevant to the JD.
```

Do not use Skills to repair missing Experience evidence.

Remove duplicates, aliases, unsupported terms, and unrelated technologies.

---

## Required Output

Return exactly two parts.

### Part 1: BLIND RECRUITER REVIEW

```text
BLIND RECRUITER REVIEW

ROLE TARGET:
<target role>

JD QUALIFICATION GROUPS:
<comma-separated groups>

EXPERIENCE ATS COVERAGE:
<proven>/<total> | <percentage>

BULLET REVIEW:
<Experience or Project> | Bullet <number> | PASS / REPAIR / REMOVE
- Missing element: <What / How / Context / Nontechnical Why / None>
- Hot dog removed: <exact phrase or None>
- Repeated group: <term or None>
- JD qualification retained: <group or None>

GAPS:
<JD qualification groups not proven in JSON, or None>

REPAIR SUMMARY:
<bullets changed, removed, or unchanged>
```

Do not reveal hidden reasoning.

### Part 2: CORRECTED JSON

Return the corrected JSON with the exact same top-level schema as the input JSON.

Before returning it, verify:

```text
[ ] Experience remains the main source of ATS coverage.
[ ] Every summary uses 1 to 3 primary JD groups.
[ ] Every later Experience and Project bullet uses 3 to 6 groups when supported.
[ ] Every final bullet contains What, How, Context, and nontechnical Why.
[ ] No hot dogs remain.
[ ] No new factual claim was added.
[ ] No meaningful term repeats within an Experience or Project entry.
[ ] Skills come only from final bullets.
[ ] Titles, companies, locations, dates, project names, and JSON structure are unchanged.
```
