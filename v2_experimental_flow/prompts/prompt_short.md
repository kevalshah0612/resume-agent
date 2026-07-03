# Short Instructions

Read `prompt.md` first and follow it exactly. Use this profile only for Experience, Projects, and Skills.

Do not create a resume summary section. If a top-level resume summary field exists later in the app, it must remain empty. `Summary` below means bullet 1 inside each Standard Experience entry only.

The app's `Location` field is header metadata only. If it differs from `New York, NY`, the app renders `New York, NY | Moving to <Location>` after the contact line. Do not put relocation text in bullets, projects, skills, or analysis.

## PASS 1

When RUN MODE is `PASS 1 - PLAN ONLY`:

1. Select the active configured plan from the JD and configuration.
2. Extract exact JD keywords from candidate-criteria sections only.
3. Classify keyword groups as MINIMUM, PREFERRED, or PROFILE FACT.
4. Map Story.md and DES evidence to the correct Experience ID or Project ID.
5. Show minimum keyword coverage, preferred keyword add-on, and closest-match projects.
6. Show `EXPERIENCE TARGETS` for every Experience entry: Summary, Bullet 2, and Bullet 3 each get 3 to 6 JD keywords or capability terms when supported.
7. Show missing high-value keywords.
8. Create a numbered `DES CANDIDATE BANK`.
9. Stop. Do not write bullets, skills, or JSON.

The projected Experience coverage target is 75% or higher for MINIMUM keyword groups. Preferred keywords are an add-on after minimum keywords are covered. Do not invent claims to reach coverage.

The first Standard Experience entry must carry the JD's highest-impact supported minimum keyword cluster in its Summary or Bullet 2 whenever Story.md or approved DES supports that cluster for the first entry. If the cluster is only supported in a lower Experience or Project, mark it `FIRST EXPERIENCE DES NEEDED` and create a DES candidate scoped to the first Experience entry. Do not move Project evidence, lower Experience evidence, or another employer's evidence into the first Experience.

Within the first Standard Experience entry, move the strongest supported work slice into Summary or Bullet 2 before using a weaker secondary slice. Reorder bullets inside the same Experience entry when needed. For both TCS entries, keep each role's evidence separate; do not move proof from one TCS role into the other.

Also plan for the first half of page one: Skills plus the first Standard Experience Summary, Bullet 2, and Bullet 3 should visibly cover about 75% of supported minimum JD keywords when evidence allows. Projects and lower Experience entries do not satisfy this first-half-page target.

PASS 1 must be compact. Use this visible shape:

```text
COVERAGE SNAPSHOT:
- Plan: <Plan ID> | <Backend / Fullstack / AIML> | <Entry / Mid / Intern>
- Minimum in Experience: <X/Y>, <NN%>
- First-half-page target: <comma-separated keywords planned for Skills plus first Experience Summary/Bullet 2/Bullet 3>
- Project-only minimums: <comma-separated list or None>
- Risk: LOW | MEDIUM | HIGH

ORDERED EXPERIENCE TARGETS:
<Experience ID>:
Summary: <3 to 6 JD keywords or capability terms, highest to lowest>
Bullet 2: <3 to 6 different JD keywords or capability terms, highest to lowest>
Bullet 3: <3 to 6 different JD keywords or capability terms, highest to lowest>

PROJECT TARGETS - SUPPLEMENTAL ONLY:
<canonical Project name>: Bullet 1: <preferred/supplemental proof slice>; Bullet 2: <different proof slice>
```

Project targets do not count toward minimum Experience coverage. If a minimum JD keyword is only supported by a Project, mark it as `PARTIAL (Project only)` or `MISSING FROM EXPERIENCE`.

DES candidates must be ID-based and scoped:

```text
DES 1 | scope: <Experience ID or Project ID> | keyword: <JD keyword> | story match: <Story label and closest evidence> | short story: <candidate-confirmable story> | use when: <why it matters> | approve text: 1
```

The short story is not evidence yet. It is the exact kind of fact the user can confirm. If Story.md has no close match, say `No direct Story.md match; needs candidate confirmation`.

The user can approve with `1,2`, `1 to 4`, `DES 1 and DES 3`, or `1 to 4, <optional candidate-confirmed explanation>`. Blank approval means use current evidence only. Do not require `CONFIRM`. Approved DES is current-run evidence for the named scope and must be preserved by hotdog when it is JD-relevant and not contradicted.

## PASS 2

When RUN MODE is `PASS 2 - WRITE APPROVED RESUME JSON`:

1. Use the approved PASS 1 plan.
2. If approval names DES IDs, use the matching PASS 1 DES candidate lines as current-run DES evidence for their named scopes only.
3. Use approved free-form DES only when it clearly names the Experience ID or Project ID or can be tied to the approved DES scope.
4. Write Experience first, Projects second, Skills last.
5. Validate and repair each bullet before drafting the next bullet, including first-half-page coverage, first-Experience keyword priority, every summary's strongest major JD group, and verb strength.
6. Return ANALYSIS, LinkedIn outreach, then one valid JSON object with only `type`, `experience`, `projects`, and `skills`.
7. Keep word counts, character counts, rendered-line estimates, draft bullets, and hidden audit details internal. Do not print counting or compression math in ANALYSIS or process output.

In ANALYSIS, include a compact `HOTDOG HANDOFF` section so the repair model knows why important JD keywords were kept:

```text
HOTDOG HANDOFF:
- <Experience ID or Project> B<n>: keywords=<3 to 6 JD keywords>; source=<Story label or approved DES ID/scope>; translation=<None or safe capability wording used>
```

This is planning context only, not resume content. Use it to explain safe capability translation, not to justify unsupported named tools or cross-scope evidence.

## Bullet Standard

Every bullet must show:

```text
WHAT + HOW + WHERE + verified nontechnical WHY
```

Bullet 1 of each Standard Experience entry is the summary. It uses 3 to 6 supported JD keywords or capability terms when possible and explains the job in simple language.

Never use more than 6 JD keywords or capability terms in one bullet target or one final bullet. If fewer than three are supported, use fewer and mark the missing high-value keyword as DES needed in PASS 1.

Every Standard Experience summary should use the strongest supported leadership, ownership, or teamwork signal for that entry when one exists. If none exists, use the strongest supported Quality / Release or Technical Execution signal.

Every summary and bullet must be written for the current JD requirement it is proving. Do not reuse generic job wording and do not dump available Story.md keywords.

Story.md is an evidence bank, not a checklist. Use only the smallest supported subset of tools, databases, frameworks, platforms, or keywords needed to prove the assigned JD keyword group.

Story.md context can support truthful adjacent capability wording when the JD asks for that capability. Do not delete or avoid a JD keyword only because the exact phrase is not written in Story.md. If the same scoped evidence clearly proves the capability, keep the JD wording or a close recruiter-readable version. If a specific named tool is not supported in that scope, replace it with the supported broad capability or ask for DES.

Every Standard Experience summary, Bullet 2, and Bullet 3 should follow the PASS 1 keyword target for that entry. Use 3 to 6 meaningful JD keywords or capability terms when supported, prioritize minimum keywords before preferred keywords, and never add terms just to reach three.

Within each Standard Experience entry, order targets highest to lowest: Summary gets the strongest supported minimum keyword cluster, Bullet 2 gets the next strongest group, and Bullet 3 gets a different remaining group. Apply this especially to both TCS entries. Do not let later summaries become generic.

If a JD keyword is supported in another Experience entry or Project, keep it in the correct scoped target instead of deleting it from the plan. Mark it as lower-entry-only or project-only when it cannot count for first Experience or Experience coverage.

Bullets 2 and 3 prove different qualification slices.

Use past tense, one direct opening verb, one sentence, one period, and no more than three rendered lines.

For SWE roles, include ownership, leadership, or teamwork when Story.md or approved DES supports it. This must be technical proof, not soft-skill filler:

```text
Led code reviews...
Owned release debugging...
Coordinated backend checks with QA and operations...
Guided implementation decisions...
```

Do not write vague soft-skill bullets such as `Collaborated with cross-functional teams` or `Demonstrated ownership`.

Choose verbs from the evidence. Prefer precise verbs such as Led, Owned, Designed, Integrated, Restored, Validated, Coordinated, Standardized, Automated, Protected, Reviewed, Guided, Migrated, Tested, and Deployed.

Treat Built, Developed, Implemented, and Delivered as weak default openers. Before finalizing any bullet, try to replace them with the precise proven action: Led, Owned, Designed, Integrated, Restored, Validated, Coordinated, Standardized, Automated, Protected, Reviewed, Guided, Migrated, Tested, or Deployed. Keep Built or Implemented only as a fallback for non-summary bullets when no stronger verb matches the proof. Do not use weak fallback openers in the first Experience summary or first Project bullet.

Avoid weak or AI-sounding wording:

```text
Developed and maintained
Worked on
Responsible for
Helped with
Utilized
Leveraged
Enhanced
Optimized
Streamlined
Spearheaded
robust
scalable
seamless
innovative
cutting-edge
dynamic
mission-critical
end-to-end
```

Length limits:

```text
Summary: 20-26 words, hard max 28 words / 190 characters.
Other Experience bullets: 22-28 words, hard max 30 words / 215 characters.
Teaching Assistant bullets: 18-26 words, hard max 28 words / 200 characters.
Project bullets: 20-28 words, hard max 30 words / 215 characters.
```

DOCX layout target: Arial 10.5 pt, 1.0 inch left margin, 1.0 inch right margin, 0.5 inch bullet indent, and 1.5 line spacing. A bullet must fit within three rendered lines.

Before accepting each bullet, silently calculate word count, visible character count including spaces and punctuation, and whether long technology names or comma chains may wrap to four lines.

Do not print this audit. If a bullet may reach four rendered lines, rewrite it before continuing.

When compressing, preserve WHAT, HOW, WHERE, WHY, and the highest JD keyword group. Remove repeated tools, extra tool names, filler adjectives, AI-sounding verbs, duplicate context, secondary metrics, vague result phrases, and then the least important JD term.

When naming three or more technologies, separate them with commas and `and` before the last item. Do not use slash chains, parentheses, or unpunctuated tool runs to pack extra tools into a bullet.

Named technologies must be JD-relevant and necessary. If Story.md supports many databases or tools, do not list all of them. Use the one strongest supported JD-relevant term, a supported broad capability phrase, or omit the tool when it does not prove the assigned JD keyword group.

Silent bullet gate:

```text
1. Pick the assigned PASS 1 keyword target for this entry and bullet slot, prioritizing MINIMUM before PREFERRED.
2. Confirm exact Story.md or approved DES evidence in the same Experience ID or Project ID.
3. Filter evidence through the JD and keep only the fewest supported keywords, tools, databases, frameworks, platforms, or practices needed.
4. Draft one natural sentence.
5. Check JD relevance, evidence, WHAT/HOW/WHERE/WHY, hotdog, repetition, verb, tense, sentence count, period count, length, rendered-line risk, and comma-separated technology formatting.
6. If any check fails, rewrite and recheck before moving on.
```

## Hotdog Rule

Audit one bullet before writing the next.

Keep a phrase only when it:

1. proves the assigned JD qualification;
2. explains HOW;
3. gives essential WHERE/context; or
4. states a verified nontechnical WHY.

Delete everything else.

Remove tool lists, feature lists, raw technical benchmark dumps, vague endings, unsupported claims, and repeated meaningful terms.

Also remove weak responsibility phrasing, AI-sounding verbs, buzzwords, vague ownership claims, and generic teamwork claims that do not state what was coordinated, with whom, and why it mattered.

## Evidence Rules

Configuration controls structure. JD controls relevance. Story.md and approved DES prove facts.

Do not use an existing resume, job title, project name, or Skills list as proof.

If a bullet has WHAT, HOW, and WHERE from the same Story.md or approved DES scope but the WHY is not written in resume language, create the closest plain nontechnical reason from that same story context. Do not invent metrics, users, domains, business outcomes, production level, or scale.

Safe capability translation is allowed only when true: Java or C++ may support object-oriented programming, a verified language may support programming-language experience, verified Node.js/JavaScript/TypeScript evidence may support JavaScript/TypeScript ecosystem experience, and verified API framework work may support backend API experience.

Do not claim a specific named technology in a specific Experience or Project bullet unless that technology is supported for the same scope or approved DES. Broad capability language is allowed only when it is truthful, JD-relevant, and grounded in candidate evidence.

Do not rename technologies or infer unsupported claims. Never move evidence between Experience entries or from Projects to Experience. Never assume tools, metrics, users, domains, AI workflows, cloud platforms, ownership, leadership, or outcomes that are not explicitly tied to the same Experience ID or Project ID.

Project names are not proof. Project bullet 1 must explain what the project is in plain language while proving the closest JD keyword group; project bullet 2 must prove a different JD-relevant slice.

Project JSON names must use the clear canonical Story.md project title, not the short alias. Keep the link separate in `github_url` when that field is available; never put the URL in `name`. Use names such as `JobPulse: Multi-Tenant Job Aggregation and Semantic Search`, `FraudSift: Transaction Analytics and ML Risk Detection`, `FilingQuery: Citation-Grounded SEC Filing Intelligence`, `EvalTrace: RAG Evaluation and CI Quality Gates`, `ReviewBot: Multi-Agent Pull Request Review`, `Resume Agent: Evidence-Grounded AI Resume Automation`, `JobFill AI: Browser Application Automation`, and `Bistro AI: Structured AI Restaurant Ordering`.

## Output Reminder

PASS 1 returns planning text only.

PASS 2 returns ANALYSIS, LinkedIn outreach, and strict JSON. Put LinkedIn outreach after ANALYSIS and before JSON:

```text
LINKEDIN OUTREACH
Recruiter LinkedIn Message:
<300 characters or fewer>

Hiring Manager LinkedIn Message:
<300 characters or fewer>

Recruiter/HM Search Strings:
<4 search strings>
```

Use only final JSON, JD, company, and title. Keep messages direct and specific. Do not use em dashes, buzzwords, generic praise, desperation, or technology lists. Do not put LinkedIn text inside JSON.

The JSON schema is:

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
      "name": "<canonical Story.md project title>",
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

The active manifest decides the real number of Experience and Project objects. AIML uses exactly 3 projects. Non-AIML uses the active plan's required project count.
