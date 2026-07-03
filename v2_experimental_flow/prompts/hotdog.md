# Hotdog Review and Repair

Use this prompt to review and repair a generated V2 resume JSON.

The goal is to remove unsupported claims, keyword stuffing, repeated proof, vague value, and hotdogs while preserving the configured structure.

Do not create a resume summary section. The only allowed JSON keys are `type`, `experience`, `projects`, and `skills`. In this prompt, `Summary` means bullet 1 inside each Standard Experience entry only.

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

CANDIDATE DES INPUT:
<candidate-confirmed evidence typed before PASS 1>

APPROVAL / APPROVED DES:
<approved DES IDs and optional scoped explanation>

PASS 1 TARGETS / DES CANDIDATE BANK (optional):
<compact PASS 1 plan, ordered experience targets, DES candidates, and approval text>

RESUME GENERATION PROCESS / HOTDOG HANDOFF (optional):
<PASS 2 analysis, keyword rationale, and generated resume process text>

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
JD defines relevant qualification keywords.
Story.md and Project Bank prove facts.
DES proves only its named current-run scope.
PASS 1 targets define the intended JD keyword plan and bullet-slot priorities.
Resume Generation Process and HOTDOG HANDOFF explain why the draft kept a JD keyword or capability translation. They are planning context, not evidence by themselves.
Current Resume JSON is text to audit. It is not evidence by itself.
```

Do not guess, infer, broaden, rename, upgrade, or transfer evidence.

Do not treat job titles, project names, Skills items, or generated wording as proof.

Approved DES and approval-box explanations are current-run evidence when they are scoped by DES ID, Experience ID, or Project ID and are relevant to the JD. Preserve that approved evidence in the repaired JSON when it is important for the JD, but remove any extra claim that broadens beyond the approved scope. If the approval text is vague or cannot be tied to a scope, do not use it as evidence.

When DES is approved and scoped, do not remove it merely because it was not in Story.md. Treat it as candidate-confirmed current-run evidence for that scope. Remove only unsupported extensions beyond the approved wording, contradictions, or JD-irrelevant extras.

Story.md and Project Bank are evidence banks, not checklists. A generated bullet fails when it dumps supported tools, databases, frameworks, platforms, or keywords that are not needed for the assigned JD keyword group.

Do not delete a JD keyword only because the exact phrase is not written in Story.md. If the same scoped evidence truthfully supports the JD capability, preserve that keyword or rewrite it into a close recruiter-readable capability phrase. If the exact named tool is unsupported in that scope, replace it with the supported broad capability, move it to the correct scoped entry, or report it as DES needed.

If PASS 1 assigned a JD keyword to an Experience bullet and the keyword is supported by Story.md, Project Bank, or approved DES for that same scope, preserve the keyword plan while repairing the wording. Hotdog should rewrite unsupported attachments around the keyword before deleting the keyword itself.

Use the Resume Generation Process / HOTDOG HANDOFF to understand the draft writer's intent:

```text
- If the handoff says a JD keyword was added from Story.md or approved DES, verify that source and keep the keyword in compressed form when truthful.
- If the handoff uses safe capability translation, verify the underlying scoped evidence and keep the broad capability when it helps the JD.
- If the handoff tries to justify an unsupported named tool, metric, user group, production scope, or cross-scope transfer, remove that claim and report the issue.
- Do not copy long PASS 2 wording. Rewrite to the same keyword target with fewer words.
```

If a JD keyword is supported only in another Experience entry or Project, keep it in that correct scope and report it as lower-entry-only or project-only. Do not erase useful JD alignment just because it cannot count for the first Experience.

For every bullet, enforce this selection order:

```text
1. JD requirement or qualification keyword.
2. Matching Story.md, Project Bank, or approved DES evidence.
3. Smallest supported tool/practice/context subset needed to prove WHAT, HOW, WHERE, and WHY.
4. Remove every supported-but-not-JD-relevant extra.
```

Safe capability translation may remain only when it is truthful, JD-relevant, and grounded in candidate evidence. Java may support object-oriented design. Verified Node.js, JavaScript, or TypeScript evidence may support JavaScript/TypeScript ecosystem experience. Verified API framework work may support backend API experience. Do not keep a specific named technology in a specific Experience or Project bullet unless that technology is supported for that same scope or approved DES.

If a tool, practice, outcome, user group, metric, AI workflow, cloud platform, security claim, ownership claim, or leadership claim is not explicitly tied to the same Experience entry or Project in Story.md, Project Bank, or approved DES, remove it or replace it with directly supported evidence from the same scope.

If a bullet has WHAT, HOW, and WHERE from the same Story.md, Project Bank, or approved DES scope but the WHY is missing or too technical, repair it with the closest plain nontechnical reason from that same story context. Do not invent metrics, users, domains, business outcomes, production level, or scale.

## Preservation Rules

Preserve the Current Resume JSON structure when it matches the active configuration:

```text
- Keep the same top-level keys: type, experience, projects, skills.
- Keep the same Experience entries, order, titles, companies, locations, and dates.
- Keep the same Project entries and order.
- Correct Project names to the clear canonical Story.md project title when the draft used only a short alias. Examples: `JobPulse: Multi-Tenant Job Aggregation and Semantic Search`, `FraudSift: Transaction Analytics and ML Risk Detection`, `FilingQuery: Citation-Grounded SEC Filing Intelligence`, `EvalTrace: RAG Evaluation and CI Quality Gates`, `ReviewBot: Multi-Agent Pull Request Review`, `Resume Agent: Evidence-Grounded AI Resume Automation`, `JobFill AI: Browser Application Automation`, and `Bistro AI: Structured AI Restaurant Ordering`.
- Keep project links separate in `github_url` if present; never put a URL inside `name`.
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
- supported tool, database, framework, platform, or keyword names that are not needed for the assigned JD keyword group;
- feature lists with no qualification focus;
- raw technical metrics or benchmarks with no human reason;
- vague endings such as for scalability, for reliability, for performance, or for operational excellence;
- repeated tools or JD keyword groups inside the same entry;
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

1. Identify the JD keyword group it is trying to prove.
2. Check every claim against Story.md, Project Bank, or DES for the same Experience ID or Project ID.
3. Filter the evidence through the JD and keep only the fewest supported keywords, tools, databases, frameworks, platforms, or practices needed for that keyword group.
4. Keep the strongest supported accomplishment.
5. Remove unsupported claims and hotdogs phrase by phrase.
6. Rewrite into one sentence with WHAT, HOW, WHERE, and WHY.
7. Check repetition against earlier bullets in the same entry or Project.
8. Check JD relevance, 3 to 6 supported JD keywords or capability terms when possible, minimum keywords before preferred keywords, verb choice, tense, one-period format, length, rendered-line risk, readability, and comma-separated technology formatting.
9. If any check fails, rewrite and check the same bullet again before moving to the next bullet.
10. Replace weak openings with a stronger evidence-backed action verb when the facts support it.

Length is a hard quality gate. Never preserve JD alignment by expanding a bullet beyond the word/character targets. If a bullet is too long, keep the highest-priority 3 to 6 JD keywords, convert extra tool lists into a broad supported capability phrase, and remove lower-priority terms.

You may replace a weak generated bullet with a different directly supported work slice from the same Experience ID or Project ID when that is needed to preserve the configured bullet count.

For SWE roles, preserve or add ownership, leadership, and teamwork only when the source proves the actual action:

```text
ownership = scoped system, feature, release, defect, migration, or workflow carried to completion
leadership = reviews, standards, release decisions, debugging direction, planning, or technical tradeoffs
teamwork = coordination with engineers, QA, operations, researchers, stakeholders, or users
```

If the bullet says `collaborated`, `led`, `owned`, or `guided`, it must also state what was coordinated or owned, with whom when relevant, and why it mattered.

For each Standard Experience summary bullet, prefer the strongest supported leadership, ownership, or teamwork signal for that entry. If none exists, use the strongest supported Quality / Release or Technical Execution signal. Do not leave a summary as generic task execution when the same entry proves a stronger responsibility signal.

Each summary must prove the strongest supported current-JD keyword group for that Experience entry. Do not leave a summary as a generic role description or a keyword/tool inventory.

The first Standard Experience entry is the first recruiter scan line. If the JD's highest-impact minimum keyword cluster is supported by Story.md or approved DES for that first entry, the first entry Summary or Bullet 2 must prove it. If the current JSON buries that cluster in a lower Experience, Project, Skills row, or outreach text while first-entry evidence exists, rewrite the first entry to carry it. If first-entry evidence does not exist, do not transfer evidence; report the cluster as lower-entry-only or project-only in ANALYSIS.

Within a single Experience entry, move the strongest supported work slice into Summary or Bullet 2 when the JD needs it there. For both TCS entries, keep each role's evidence separate; do not move proof from one TCS role into the other.

First-half-page rule: Skills plus the first Standard Experience Summary, Bullet 2, and Bullet 3 should visibly carry about 75% of supported minimum JD keywords when the evidence allows. Projects and lower Experience entries do not count toward this first-half-page target.

Every Standard Experience summary must carry that entry's strongest major JD keyword group. Do not repair only the first entry while leaving second or third summaries generic.

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

Treat `Built`, `Developed`, `Implemented`, and `Delivered` as weak default openers. Replace them whenever the same evidence supports a more precise action such as `Led`, `Owned`, `Designed`, `Integrated`, `Restored`, `Validated`, `Coordinated`, `Standardized`, `Automated`, `Protected`, `Reviewed`, `Guided`, `Migrated`, `Tested`, or `Deployed`. Keep `Built` or `Implemented` only as a fallback for non-summary bullets when no stronger verb fits and the sentence names the concrete system, method, and reason. Do not keep weak fallback openers in the first Experience summary or first Project bullet.

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

When compressing, preserve WHAT, HOW, WHERE, WHY, and the highest JD keyword group. Remove repeated tools, extra database/framework/cloud/library/platform names, filler adjectives, AI-sounding verbs, duplicate context, secondary metrics, vague result phrases, and then the least important JD term.

Never preserve more than 6 JD keywords or capability terms in one repaired bullet. If a draft carries more than 6, keep the highest-priority minimum keywords first, then important preferred keywords, and remove the rest unless they are essential HOW/WHERE words.

When Story.md supports many databases or tools, do not keep all of them. Keep one strongest JD-relevant named term, a supported broad capability phrase, or no tool/database term when it does not help prove the assigned JD keyword group.

Use numbers only when verified and useful to a nontechnical reader. Avoid raw percentages, latency, model accuracy, and benchmark values unless the JD and evidence make them necessary.

When naming three or more technologies, separate them with commas and `and` before the last item. Do not use slash chains, parentheses, or unpunctuated tool runs to pack extra tools into a bullet.

## Repetition Rules

Within the same Experience entry or Project, do not repeat a meaningful term after it appears in a passing earlier bullet.

Locked terms include languages, frameworks, databases, cloud providers, queues/caches, API types, authentication terms, testing tools, delivery tools, primary JD keyword groups, and core system phrases.

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

## ANALYSIS Shape

Return this before JSON:

Keep ANALYSIS concise. Do not include word counts, character counts, rendered-line estimates, draft bullets, hidden audit details, or bullet-by-bullet length math. The counting and compression process must stay internal.

```text
ANALYSIS
--------
ACTIVE PLAN:
<Plan ID> | <Backend / Fullstack / AIML>

EXPERIENCE COVERAGE:
- <Experience entry>: <X/Y> | <NN%>
  Proven keywords: <minimum and preferred keywords visible in final bullets>

OVERALL EXPERIENCE COVERAGE:
<X/Y> | <NN%>
Project-only minimum keywords: <list or None; these do not count as covered>
First-half-page minimum keywords: <list visible in Skills plus first Experience or gap>

BULLET REVIEW:
- <Experience or Project> | Bullet <number> | PASS / REWRITE
  Hotdogs removed: <short phrase list or None>
  Constraint: <None or concise non-count issue>

PROJECTS ADD:
<project-only supplemental keywords or None>

GAPS:
<missing JD keywords or None>

HOTDOG HANDOFF USED:
<PASS 1 / PASS 2 rationale preserved, compressed, moved, or rejected in one short line>

REPAIR RESULT:
READY
--------
```

## Final JSON Shape

Return the corrected JSON immediately after `ANALYSIS`. Do not include LinkedIn outreach in hotdog repair output.

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
      "name": "<canonical Story.md project title>",
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
- The first Standard Experience Summary or Bullet 2 proves the JD's highest-impact supported minimum keyword cluster for that entry, or ANALYSIS explains why it is not supported there.
- Skills plus the first Experience bullets carry the strongest supported minimum keywords for the first half of page one.
- Every Standard Experience summary proves that entry's strongest major JD keyword group.
- Every final bullet has WHAT, HOW, WHERE, and WHY.
- No unsupported claim or hotdog remains.
- No meaningful repeated term remains inside the same entry or Project unless essential.
- Skills are minimal, JD-relevant, and traceable.
```
