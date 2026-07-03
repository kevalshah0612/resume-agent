# V3 Hotdog Review and Repair

Use this prompt to enforce the V3 resume rules after a V3 resume JSON is generated.

This is the strict repair layer for the rules from The Job Closer, JD.docx keyword examples, Resume Guide, and Rules.md.

The goal is not to make the resume fancy. The goal is to make every bullet prove the job qualifications clearly, compactly, and truthfully.

Return only:

1. `ANALYSIS`
2. One valid JSON object with exactly `type`, `experience`, `projects`, and `skills`

Do not include LinkedIn outreach in hotdog output.

Do not use Markdown fences. Do not write anything after the JSON.

## Required Inputs

The app provides:

```text
=== RESUME CONFIGURATION - IMMUTABLE ===
<active structure, plans, projects, and limits>
=== END RESUME CONFIGURATION ===

JD:
<complete job description>

PASS 1 TECH KEYWORD PLAN:
<TECH KEYWORD LINE, PRIMARY TECH, SECONDARY TECH, JD VERBS, KEYWORD PLACEMENT, missing words, DES candidates>

APPROVAL / APPROVED DES:
<approved DES IDs and optional scoped explanation>

STORY.md:
<base story direction and evidence>

PROJECT BANK:
<optional verified project evidence>

RESUME GENERATION ANALYSIS / HOTDOG HANDOFF:
<bullet checks, source notes, approved DES notes, keyword rationale>

CURRENT RESUME JSON:
<JSON produced by V3 prompt>
```

## Source Roles

Use each source for only its job:

```text
Configuration:
Locks structure, order, metadata, bullet counts, project count, and skill limits.

JD:
Defines exact tech terms, JD verbs, qualification priority, and target language.

PASS 1 TECH KEYWORD PLAN:
Defines primary tech, secondary tech, supplemental tech, placement, and intended keyword targets.

Story.md:
Guides direction and proves base work context.

Approved DES:
Adds current-run evidence for its named scope only.

Current Resume JSON:
Text to audit and repair. It is not evidence.
```

Never use old resumes, job titles alone, project names alone, skills alone, prior chats, memory, or unstated assumptions as proof.

## JD Surface Term Enforcement

Use the JD's exact surface terms whenever the scoped evidence supports the same capability.

```text
- Preserve JD spelling.
- Preserve JD casing.
- Preserve JD spacing.
- Preserve JD version suffixes.
- Preserve JD product and platform names.
```

If Story.md says a compatible broader term and the JD uses a specific equivalent surface term, repair the bullet to use the JD term.

Do this dynamically from the current JD. Do not hardcode a fixed list of replacements.

Examples of the rule:

```text
If the JD says HTML5 and the scoped story proves frontend HTML capability, prefer HTML5.
If the JD says RESTful APIs and the scoped story proves REST API work, prefer RESTful APIs.
If the JD says Git, use Git unless the JD itself uses different casing.
```

Do not use this rule to rename materially different technologies.

```text
Do not turn Docker Compose into Kubernetes.
Do not turn REST API into OpenAPI.
Do not turn AWS Lambda into DynamoDB.
Do not turn cloud into Terraform.
Do not turn OpenAI API into RAG, agents, MLOps, ML, or model evaluation.
Do not turn AI-assisted coding into AI product integration.
```

If the JD surface term is materially different and not supported, remove it or mark it as a gap in ANALYSIS.

## JD-Only Technology Selection

Use named technologies from the current JD first.

Do not preserve story-only technology inventories. Story.md proves capability; the JD decides which named tech belongs in the repaired resume.

When Story.md supports several interchangeable tools in the same family, such as databases, clouds, API frameworks, testing tools, UI frameworks, or monitoring tools:

```text
- If the JD names one specific tool, keep only that JD-named tool when scoped evidence supports the same capability.
- If the JD names a broad family term, use the JD's broad term or one strongest supported tool, not the full story inventory.
- If the JD names multiple tools in the same family, keep only the planned JD-relevant tools needed to prove the bullet.
- If a story-only tool is not in the JD, remove the name from bullets and skills unless approved DES explicitly requires it.
```

Use capability wording such as database workflow, cloud-hosted service, API integration, frontend dashboard, testing workflow, or monitoring dashboard when the JD does not ask for the exact named tool.

This rule is dynamic. Do not hardcode a fixed technology list.

## Comma Rule For Tech

Every list of tech terms must use commas:

```text
Java, Spring Boot, RESTful APIs, SQL, Git
```

Repair or remove:

```text
Java/Spring/SQL
Java Spring SQL
Java (Spring, SQL, Git, Docker, AWS)
dense acronym chains
parentheses used to pack extra tools
```

When a bullet names three or more technologies, separate them with commas and `and` before the final term.

Do not add extra tech only to make a list longer. Compact proof beats dense lists.

## Qualification Standard

Every bullet must prove a qualification with all five elements:

```text
WHAT:
What was built, fixed, designed, tested, released, automated, integrated, reviewed, owned, or coordinated?

HOW:
Which JD-relevant term, method, tool, language, framework, platform, or practice was used?

WHERE:
Which system, service, workflow, release path, data flow, project, team process, or integration did this happen in?

WHY:
Why did it matter in plain nontechnical language?

RESULT / REASON:
What outcome, result, reason, risk reduction, user value, business value, team value, delivery value, quality value, or operational value came from the work?
```

A bullet that misses any one of these fails and must be rewritten from the same scoped evidence.

The WHY and RESULT/REASON must be clear nontechnical user, stakeholder, team, or business impact. They may be conservative plain-language wording from the real story context. Do not invent metrics, user groups, domains, production level, business value, or scale.

A bullet that only lists technologies fails, even if every technology is supported.

## Book And Guide Enforcement

Enforce these rules:

```text
- The resume exists to get interviews by proving minimum qualifications.
- Recruiters and hiring managers scan for qualifications quickly.
- Minimum qualifications beat preferred qualifications.
- Keywords must appear as qualification proof, not keyword stuffing.
- Named technologies must come from the current JD, approved DES, or the smallest necessary same-scope proof.
- Strongest supported tech must appear early.
- About 75% of supported minimum tech keywords should appear in the first half page target when possible.
- Skills stay compact and near the bottom.
- Bullets stay plain enough for a nontechnical reader.
- Use past tense.
- Avoid unnecessary numbers.
- Use metrics only when real, supported, and useful.
- Keep the resume clear, compact, and error-free instead of perfect/fancy.
```

## DES Preservation

Approved DES is evidence for its named scope only.

If the approved DES supports an important JD keyword, preserve it in the repaired bullet when it is scoped, compact, JD-relevant, and not contradicted.

Do not delete approved DES merely because Story.md does not contain it.

Remove only:

```text
- extensions beyond the approved DES;
- unsupported metrics or scale added around the DES;
- cross-scope movement;
- JD-irrelevant use of the DES;
- contradictions.
```

Hotdog must use the handoff:

```text
HOTDOG HANDOFF:
- <Experience ID or Project> B<n>: keywords=<3 to 5 words>; source=<Story label or Approved DES ID>; preserve=<why>
```

## Capability Layer

Story.md guides direction. It is not a word-matching cage.

Safe capability translation is allowed only when the scoped evidence proves the real capability and the JD asks for that capability.

Allowed dynamically:

```text
- A verified language can support programming-language experience.
- Verified Java backend work can support backend services, object-oriented programming, API development, and enterprise service work.
- Verified Python work can support backend, scripting, automation, data processing, or AI/ML support when the story proves that direction.
- Verified JavaScript, TypeScript, React, Node.js, or Next.js work can support frontend, fullstack, web application, or JavaScript ecosystem capability.
- Verified API framework work can support backend API experience.
- Verified AWS, Azure, or GCP work can support cloud experience.
- Verified CI/CD, release, testing, deployment, or Git work can support delivery engineering.
```

Not allowed:

```text
- specific named tool claims without same-scope evidence or approved DES;
- production, scale, security, AI/ML, cloud, ownership, leadership, domain, user, or metric claims without support;
- moving project proof into experience;
- moving one employer's proof into another employer;
- treating project names or job titles as proof.
```

## Verb Enforcement

Every bullet must start with a strong verb that matches the evidence.

Preferred verbs include:

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

Never keep these as opening verbs:

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

If a weak opener appears, rewrite the bullet with a stronger evidence-backed verb.

## Hotdog Definition

A hotdog is any phrase that may sound related but does not help prove the target JD qualification.

Remove hotdogs:

```text
- tool inventories;
- story-only technology inventories not requested by the JD;
- feature lists with no qualification focus;
- repeated tech inside the same entry;
- supported-but-not-JD-relevant tools;
- unsupported exact JD terms;
- vague endings such as for scalability, for reliability, for performance, or for operational excellence;
- generic teamwork with no team, action, decision, or result;
- vague ownership or leadership labels;
- raw technical metrics with no human or operational reason;
- buzzwords, hype, and dense acronym chains;
- implied production, scale, security, AI, ML, MLOps, RAG, agents, cloud, ownership, or business-value claims.
```

Approved DES is not a hotdog when it is scoped and JD-relevant.

## Repair Process

Review one bullet at a time.

For each bullet:

1. Identify its planned keyword target from PASS 1.
2. Confirm the JD exact surface terms for those keywords.
3. Confirm Story.md, Project Bank, or approved DES support in the same scope.
4. Use JD exact terms when the scoped evidence supports the same capability.
5. Remove or replace unsupported exact terms.
6. Keep only the smallest useful set of JD-relevant named technologies, usually 2 to 4 terms; use 5 only when the JD truly requires the cluster.
7. Rewrite to answer WHAT, HOW, WHERE, WHY, and RESULT/REASON.
8. Use a strong opening verb.
9. Apply the comma rule for every tech list.
10. Check repetition within the same experience or project.
11. Check 22 to 25 words, past tense, one sentence, and one period.
12. Check that RESULT/REASON states user, stakeholder, team, or business impact.
13. Recheck as a recruiter: can a nontechnical person understand the qualification quickly?

Do not preserve JD alignment by making a bullet dense or unsafe. If a bullet cannot safely support the planned keyword, use the closest truthful same-scope keyword and list the missing word in ANALYSIS.

## Structure Preservation

Preserve the configured structure:

```text
- Top-level keys exactly: type, experience, projects, skills.
- Same configured Experience entries, order, metadata, and bullet counts.
- Same configured Project count and bullet counts.
- No top-level summary.
- Change only bullet strings and skills unless a project name must be corrected to the configured canonical name.
```

If structure cannot be repaired without inventing entries, return ANALYSIS with `REPAIR RESULT: BLOCKED` and no JSON.

## Skills Repair

Rebuild skills after bullets are final.

Skills must be:

```text
- compact;
- technical;
- JD-relevant;
- comma-separated when represented as a line;
- traceable to final bullets or approved DES;
- minimal.
```

Remove soft skills, buzzwords, aliases, broad inventories, and terms not used or evidenced.

Use the JD's surface term for skill names when same-scope evidence supports the capability.

## ANALYSIS Shape

Return concise analysis before JSON:

```text
ANALYSIS
--------
ACTIVE PLAN:
<Plan ID> | <Backend / Fullstack / AIML> | <Entry / Mid / Intern>

RULE ENFORCEMENT:
- The Job Closer: PASS | qualification proof, not perfection
- JD.docx: PASS | tech keyword line and exact JD terms
- Resume Guide: PASS | what/how/where/why/result, compact bullets
- Rules.md: PASS | smallest useful JD terms, strong verbs, comma tech, no repeats

JD SURFACE TERMS:
- Preserved: <terms>
- Repaired: <old -> JD term>
- Missing or unsupported: <terms or None>

BULLET REVIEW:
- <Experience or Project> B<n>: PASS / REWRITE
  Keywords: <smallest useful planned JD terms>
  JD-Tech Scope: PASS / REWRITE | <only JD-relevant named tech; no story inventory>
  Verb: <verb>
  WHAT/HOW/WHERE/WHY/RESULT: PASS
  User/Business Impact: PASS / REWRITE | <plain outcome>
  Hotdogs removed: <short list or None>
  DES preserved: <Approved DES ID or None>
  Compact: PASS / REWRITE | <word count>

FIRST HALF PAGE COVERAGE:
- Supported minimum tech keywords visible early: <list>
- Coverage: <X/Y> | <NN%>

GAPS:
- <missing / partial / lower-experience-only / project-only terms or None>

REPAIR RESULT:
READY
--------
```

Do not include hidden reasoning, failed drafts, word-count math beyond concise compactness notes, or long audits.

## Final JSON Verification

Before returning, silently verify:

```text
- JSON parses.
- Top-level keys are exactly type, experience, projects, skills.
- No top-level summary exists.
- Configured structure and bullet counts are preserved.
- Every bullet starts with a strong verb.
- No banned weak opener remains.
- Every bullet has WHAT, HOW, WHERE, WHY, and RESULT/REASON.
- Every bullet is 22 to 25 words.
- Every bullet shows user, stakeholder, team, or business impact.
- JD surface terms are preserved when support exists.
- No materially different technology is renamed.
- Every named technology is JD-relevant, scoped, and comma-separated when listed.
- No story-only technology inventory remains.
- Approved DES is preserved when scoped and important.
- No unsupported claim or hotdog remains.
- No repeated meaningful tech remains inside the same entry unless essential.
- Skills are minimal, JD-relevant, and traceable.
```
