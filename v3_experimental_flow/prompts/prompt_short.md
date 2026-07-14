# Short Runtime Instructions — Current

Read `prompt.md` first. This file is only a compact reminder and must not override `prompt.md`.

## Mission

Generate JD-specific resume JSON from verified evidence only:

```text
prompt default structure + current runtime fields + Story.md + approved DES + JD/company signals
```

Do not guess. Do not hardcode company, story, project, or bullet choices. Story.md controls facts. The JD controls emphasis. The JD is never evidence.

## Simple JSON Type

Final JSON uses exactly one strategy type: `NewGrad`, `Entry`, or `Mid`.

`NewGrad` = new-grad/campus/0-1 year strategy.

```json
{"type":"NewGrad","section_order":["summary","technical_skills","education","projects","professional_experience"],"experience_order":["TA","GHI","TCS-SWE-II","TCS-SWE"]}
```

`Entry` = default cold-apply chronological strategy.

```json
{"type":"Entry","section_order":["summary","technical_skills","professional_experience","education","projects"],"experience_order":["TA","GHI","TCS-SWE-II","TCS-SWE"]}
```

`Mid` = production-first strategy for 3+ / platform / backend / reliability JDs.

```json
{"type":"Mid","section_order":["summary","technical_skills","professional_experience","projects","education"],"experience_order":["TCS-SWE-II","TCS-SWE","GHI","TA"]}
```

Default to `Entry` unless the JD clearly indicates `NewGrad` or `Mid`. Preserve wrapper config and keep it consistent.

## Source Order

1. Prompt defaults and current runtime fields.
2. Current-run approved DES for exact scope.
3. Same-scope Story.md verified evidence.
4. PASS 1 plan and ledgers.
5. JD/company signals.

Old resumes, old runs, examples, and generated bullets are not evidence.

## Official Company Research

Use official/runtime company sources only for company goals, future plans, revenue, product direction, or roadmap. If unavailable, print that official company research is not provided and use the JD only.

Company research can shape summary emphasis and bullet priority. It cannot create candidate facts.

## PASS 1 Must Print

Use readable dividers, spacing, and section results. Stop after PASS 1. Do not write final JSON.

Required sections:

```text
SECTION 01 — COMPANY + ROLE SNAPSHOT
SECTION 02 — JD MAP
SECTION 03 — MODE + ORDER DECISION
SECTION 04 — SUPPORTED KEYWORDS
SECTION 05 — MISSING IMPORTANT KEYWORDS
SECTION 06 — PARTIAL / RISKY CLAIMS
SECTION 07 — DO-NOT-USE CLAIM LEDGER
SECTION 08 — DES NEEDED
SECTION 09 — HIGHEST SIGNAL MAP
SECTION 10 — BULLET SLOT PLAN
SECTION 11 — PROJECT SELECTION PLAN
SECTION 12 — SKILLS TRACEABILITY PLAN
SECTION 13 — METRIC LEDGER
SECTION 14 — BEHAVIOR LEDGER
SECTION 15 — PRE-WRITE RISK FLAGS
```

Use compact tables only when cells are short. DES must use compact rows first; use mini-cards only when a DES row is too long. Use card blocks for long risk explanations.

## OR-Skill Rule

If JD says `A, B, C, or similar/comparable`, classify the group, not every tool as mandatory.

Example: `Python, Go, Node.js, Rust, or comparable` can be satisfied by verified Python/Java/C# backend evidence. Go/Rust become missing but not blocking unless the JD explicitly requires them.

Never write `Next.js-ready`, `Go-ready`, `Rust-ready`, `Azure-ready`, or `production-ready`.

## DES

DES candidates are questions, not evidence. Do not stop for input; continue with safe evidence.

DES must be compact and readable. First print one-line rows:

```text
DES ID | Keyword / claim | JD importance + branch | Priority | Section priority | Story | Question | Fallback
```

Rules:
- `JD importance + branch` must mention AND, OR_GROUP, PREFERRED, RESPONSIBILITY, or VALUE.
- `Section priority` must say Experience first, Project only, Skills after proof, Summary restriction, or Omit unless approved.
- `Story` must be Story number, TCS shared pool, Project name, or `None` for missing evidence.
- Missing keywords go into DES with `Story: None`; do not write a long separate missing section.
- Keep questions short. The user will write the DES answer.
- One DES = one scope + one claim family.

Priority:
- REQUIRED only for true blockers or claims the resume plans to make.
- RECOMMENDED for preferred keywords or OR-list gaps.
- OPTIONAL for nice-to-have proof.
- NOT_RECOMMENDED for broad user-fill or already-covered claims.

## Highest Signal Rule

Rank evidence by hard requirement match, repeated keyword match, production strength, metric strength, recency, recruiter readability, hiring-manager credibility, and risk.

TCS-SWE-II B1/B2 must carry the strongest production proof. Project 1 must cover the highest-value JD gap not covered by Experience.

## Bullet Rules

Every bullet needs:

```text
WHY/CONTEXT + WHAT + HOW + BENEFIT/OUTCOME
```

Experience bullets <=25 words. Project bullets <=28 words.

Use one workstream, one strong unique opening verb, one main method/stack group, and one primary outcome/metric.

Avoid repeated AI rhythm: `Verb + tech + metric + reducing + metric`.

## Personal Projects

Projects are personal/self-built/self-tested/prototype unless evidence proves production deployment.

Project bullets must explain:

1. what the project does,
2. what workflow/problem it helps,
3. how it is built,
4. one validation proof only when useful.

Use 0-1 metric by default. Use 2 metrics only when one is scope and one is outcome. Avoid 3+ metrics.

Good titles:

```text
FilingQuery - SEC filing question-answering platform
EvalTrace - RAG evaluation quality-gate pipeline
```

## Arrow-Free Metrics

Final JSON must not contain `→`, `->`, `=>`, `↔`, or `⇒`.

Convert `23%→4%` to `from 23% to 4%` and `8s→2s` to `from 8s to 2s` while preserving exact values.

## Summary

Summary target: 28-36 words. Hard range: 25-40 words.

Summary must be contribution-focused:

- role family,
- verified strengths,
- how those strengths help the target team.

Do not write:

- seeking to contribute,
- excited to work,
- I want,
- passionate,
- expertise in a tool not proven in final Experience/Project.

Summary must not contradict final JSON. If Next.js/Azure/Go/Rust are not proven in Experience/Project or verified Story.md, they cannot appear in Summary.

## Skills

Every skill must trace to final Experience bullet, final Project bullet, verified Story.md, or approved DES used in Experience/Project first. Remove unsupported or user-fill/edit-verify skills without approval.

## PASS 2 Must Print Checks

Before final JSON, print checks with readable dividers:

```text
SECTION 01 — DES usage
SECTION 02 — Missing important keywords
SECTION 03 — Do-not-use ledger
SECTION 04 — Highest signal placement
SECTION 05 — First-two-bullet score
SECTION 06 — Project proof score
SECTION 07 — Skill traceability
SECTION 08 — Verb ledger
SECTION 09 — Outcome phrase ledger
SECTION 10 — Sentence rhythm check
SECTION 11 — Number overload check
SECTION 12 — Metric token table
SECTION 13 — Final JSON word-count table
SECTION 14 — Wrapper preservation note
SECTION 15 — Human recruiter trust check
SECTION 16 — Repair log
SECTION 17 — Quality result
```

## Final JSON Source of Truth

All checks must be calculated from final JSON exactly as printed, not draft bullets or analysis text.

After every repair, rerun checks on final JSON:

- word count,
- summary contradiction,
- skill traceability,
- arrow-free metrics,
- project metric density,
- do-not-use claims.

Do not reuse pre-repair PASS values.

Also rerun:
- JD branch / OR logic
- exact JD wording
- top-third placement
- experience-first keyword placement
- DES compactness and story/None field

Quality result choices:

```text
READY
READY_WITH_DES_GAPS
REPAIRED_READY
SAFE_FALLBACK_WITH_DES_REQUIRED
```
