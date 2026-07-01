# Hotdog Review and Repair

Use this prompt to review and repair a generated V2 resume JSON.

The goal is to remove unsupported claims, keyword stuffing, repeated proof, vague value, and hotdogs while preserving the configured structure.

Return only:

1. `ANALYSIS`
2. One valid JSON object with exactly `type`, `experience`, `projects`, and `skills`

Do not use Markdown fences. Do not write anything after JSON.

## Required Inputs

The app provides:

```text
=== RESUME CONFIGURATION - IMMUTABLE ===
<active structure, plans, projects, and limits>
=== END RESUME CONFIGURATION ===

JD:
<complete job description>

DES (optional):
<candidate-confirmed evidence>

STORY.md:
<evidence bank>

PROJECT BANK:
<optional verified project evidence>

CURRENT RESUME JSON:
<JSON produced by the V2 prompt>
```

## Source Rules

Use sources only for their assigned job:

```text
Configuration locks structure, order, metadata, bullet counts, project count, and skills limits.
JD defines relevant qualification signals.
Story.md and Project Bank prove facts.
DES proves only its named current-run scope.
Current Resume JSON is text to audit. It is not evidence by itself.
```

Do not guess, infer, broaden, rename, upgrade, or transfer evidence.

Do not treat job titles, project names, Skills items, or generated wording as proof.

## Preservation Rules

Preserve the Current Resume JSON structure when it matches the active configuration:

```text
- Keep the same top-level keys: type, experience, projects, skills.
- Keep the same Experience entries, order, titles, companies, locations, and dates.
- Keep the same Project entries, order, and names.
- Keep the same bullet count in each Experience entry and Project.
- Change only bullet strings and skills.
```

If the JSON structure conflicts with the active configuration, explain the conflict in ANALYSIS and still return the closest corrected JSON only when it can be made valid without inventing entries. If it cannot, return ANALYSIS with `REPAIR RESULT: BLOCKED` and no JSON.

## Qualification Standard

A valid bullet proves:

```text
WHAT  - what was built, delivered, fixed, tested, released, supported, or handled
HOW   - how the JD-relevant method, tool, or practice was used
WHERE - the real system, service, workflow, release path, integration, data flow, or project
WHY   - the verified plain-language reason it mattered
```

A keyword alone does not count. Skills alone do not count.

## Hotdog Definition

A hotdog is any phrase that may sound technical or impressive but does not help prove the job qualification.

Keep a phrase only when it does one of these jobs:

1. proves the assigned JD qualification;
2. explains HOW;
3. gives necessary WHERE/context; or
4. states a verified nontechnical WHY.

Delete phrases that do none of those jobs.

Hotdogs include:

```text
- tool inventories with no context or value;
- feature lists with no qualification focus;
- raw technical metrics or benchmarks with no human reason;
- vague endings such as for scalability, for reliability, for performance, or for operational excellence;
- repeated tools or JD signals inside the same entry;
- generic collaboration with no requirement, decision, or result;
- vague ownership or leadership labels with no scoped system, decision, review, release, or issue;
- weak responsibility wording such as developed and maintained, worked on, responsible for, or helped with;
- AI-sounding verbs such as utilized, leveraged, enhanced, optimized, streamlined, spearheaded, or pioneered;
- buzzword adjectives such as robust, scalable, seamless, innovative, cutting-edge, dynamic, mission-critical, end-to-end, or impactful;
- implied production, scale, cloud, security, RAG, agents, ML, MLOps, ownership, user, or business-value claims.
```

## Repair Rules

Review one bullet at a time.

For each bullet:

1. Identify the JD signal it is trying to prove.
2. Check every claim against Story.md, Project Bank, or DES for the same Experience ID or Project ID.
3. Keep the strongest supported accomplishment.
4. Remove unsupported claims and hotdogs phrase by phrase.
5. Rewrite into one sentence with WHAT, HOW, WHERE, and WHY.
6. Check repetition against earlier bullets in the same entry or Project.
7. Check length, tense, one-period format, and readability.
8. Replace weak openings with a stronger evidence-backed action verb when the facts support it.

You may replace a weak generated bullet with a different directly supported work slice from the same Experience ID or Project ID when that is needed to preserve the configured bullet count.

For SWE roles, preserve or add ownership, leadership, and teamwork only when the source proves the actual action:

```text
ownership = scoped system, feature, release, defect, migration, or workflow carried to completion
leadership = reviews, standards, release decisions, debugging direction, planning, or technical tradeoffs
teamwork = coordination with engineers, QA, operations, researchers, stakeholders, or users
```

If the bullet says `collaborated`, `led`, `owned`, or `guided`, it must also state what was coordinated or owned, with whom when relevant, and why it mattered.

You may not:

```text
- move Project evidence into Experience;
- move one employer's evidence into another employer;
- add a named JD tool that is not supported;
- add a metric, user, outcome, domain, or deployment claim that is not supported;
- change configured metadata;
- add or delete bullets.
```

## Bullet Length and Style

```text
- Past tense, including current roles.
- One direct opening verb.
- One sentence.
- Exactly one ending period.
- No bold markers or Markdown.
- No em dash.
- No buzzwords, hype, passive voice, stacked opening verbs, weak responsibility wording, AI-sounding verbs, or dense acronym chains.
- No more than three rendered lines.
```

Targets:

```text
Summary bullets: 20-26 words, hard max 28 words / 190 characters.
Other Experience bullets: 22-28 words, hard max 30 words / 215 characters.
Teaching Assistant bullets: 18-26 words, hard max 28 words / 200 characters.
Project bullets: 20-28 words, hard max 30 words / 215 characters.
```

DOCX layout target:

```text
- Font: Arial, approximately 10.5 pt body text.
- Left margin: 1.0 inch.
- Right margin: 1.0 inch.
- Bullet indent: approximately 0.5 inch.
- Line spacing: 1.5.
- A bullet must fit within three rendered lines.
```

Before accepting each repaired bullet, silently calculate:

```text
- word count;
- visible character count, including spaces and punctuation;
- whether long technology names, slash terms, parentheticals, or comma chains make the bullet likely to render to four lines.
```

Do not print this audit. If the bullet may reach four rendered lines, rewrite it before returning JSON.

When compressing, preserve WHAT, HOW, WHERE, WHY, and the highest JD signal. Remove repeated tools, extra database/framework/cloud/library/platform names, filler adjectives, AI-sounding verbs, duplicate context, secondary metrics, vague result phrases, and then the least important JD term.

Use numbers only when verified and useful to a nontechnical reader. Avoid raw percentages, latency, model accuracy, and benchmark values unless the JD and evidence make them necessary.

## Repetition Rules

Within the same Experience entry or Project, do not repeat a meaningful term after it appears in a passing earlier bullet.

Locked terms include languages, frameworks, databases, cloud providers, queues/caches, API types, authentication terms, testing tools, delivery tools, primary JD signals, and core system phrases.

Normal words may repeat when needed: user, team, system, service, workflow, data, release, request.

## Skills Repair

Rebuild skills after bullets are final.

```text
- Include only short, technical, JD-relevant skills.
- A skill must appear in a final bullet or be narrowly supported by approved DES.
- Skills do not increase Experience coverage.
- Remove aliases, soft skills, buzzwords, broad inventories, duplicates, and discarded tools.
- Obey the active configuration's skills minimum and maximum.
```

## LinkedIn Outreach

Return LinkedIn outreach outside the corrected JSON.

Place it after `ANALYSIS` and before the final JSON:

```text
LINKEDIN OUTREACH
Recruiter LinkedIn Message:
<300 characters or fewer>

Hiring Manager LinkedIn Message:
<300 characters or fewer>

Recruiter/HM Search Strings:
<4 search strings>
```

Rules:

```text
- Use only proof from the corrected final JSON, JD, company, and title.
- Each message must be under 300 characters including spaces.
- Keep messages short, direct, and specific.
- Do not use em dashes, buzzwords, generic praise, desperation, or technology lists.
- Do not put LinkedIn text inside JSON.
```

## ANALYSIS Shape

Return this before JSON:

```text
ANALYSIS
--------
ACTIVE PLAN:
<Plan ID> | <Backend / Fullstack / AIML>

EXPERIENCE COVERAGE:
- <Experience entry>: <X/Y> | <NN%>
  Proven signals: <signals visible in final bullets>

OVERALL EXPERIENCE COVERAGE:
<X/Y> | <NN%>

BULLET REVIEW:
- <Experience or Project> | Bullet <number> | PASS / REWRITE
  Hotdogs removed: <short phrase list or None>
  Constraint: <None or concise issue>

PROJECTS ADD:
<project-only supplemental signals or None>

GAPS:
<missing JD signals or None>

REPAIR RESULT:
READY
--------
```

## Final JSON Shape

Return the corrected JSON immediately after `LINKEDIN OUTREACH`:

```json
{
  "type": "Backend | Fullstack | AIML",
  "experience": [
    {
      "title": "<unchanged>",
      "company": "<unchanged>",
      "location": "<unchanged>",
      "dates": "<unchanged>",
      "bullets": [
        "<corrected bullet>"
      ]
    }
  ],
  "projects": [
    {
      "name": "<unchanged>",
      "bullets": [
        "<corrected bullet>"
      ]
    }
  ],
  "skills": [
    "<corrected skill>"
  ]
}
```

The template is instructional. Final JSON must include every existing configured Experience and Project object, not only one example.

Before returning, silently verify:

```text
- JSON parses.
- No extra top-level keys exist.
- Configured structure and bullet counts are preserved.
- Every final bullet has WHAT, HOW, WHERE, and WHY.
- No unsupported claim or hotdog remains.
- No meaningful repeated term remains inside the same entry or Project unless essential.
- Skills are minimal, JD-relevant, and traceable.
```
