# Short Instructions

Read `prompt.md` first and follow it exactly. Use this profile only for Experience, Projects, and Skills.

## PASS 1

When RUN MODE is `PASS 1 - PLAN ONLY`:

1. Select the active configured plan from the JD and configuration.
2. Freeze JD signals from candidate-criteria sections only.
3. Classify signals as PRIMARY, CORE, PREFERRED, or PROFILE FACT.
4. Map Story.md and DES evidence to the correct Experience ID or Project ID.
5. Show projected Experience coverage and closest-match projects.
6. Show missing high-signal terms.
7. Create a numbered `DES CANDIDATE BANK`.
8. Stop. Do not write bullets, skills, or JSON.

The projected Experience coverage target is 75% or higher for PRIMARY and CORE signals. Do not invent claims to reach it.

DES candidates must be ID-based and scoped:

```text
DES 1 | scope: <Experience ID or Project ID> | keyword: <JD signal> | story match: <Story label and closest evidence> | short story: <candidate-confirmable story> | use when: <why it matters> | approve text: Approved: 1
```

The short story is not evidence yet. It is the exact kind of fact the user can confirm. If Story.md has no close match, say `No direct Story.md match; needs candidate confirmation`.

The user can approve with `Approved: 1,2`, `Approved: DES 1 and DES 3`, `CONFIRM`, or `CONFIRM: <candidate-confirmed fact>`.

## PASS 2

When RUN MODE is `PASS 2 - WRITE APPROVED RESUME JSON`:

1. Use the approved PASS 1 plan.
2. If approval names DES IDs, use the matching PASS 1 DES candidate lines as current-run DES evidence for their named scopes only.
3. Use approved free-form DES only when it clearly names the Experience ID or Project ID.
4. Write Experience first, Projects second, Skills last.
5. Return ANALYSIS, then one valid JSON object with only `type`, `experience`, `projects`, and `skills`.

## Bullet Standard

Every bullet must show:

```text
WHAT + HOW + WHERE + verified nontechnical WHY
```

Bullet 1 of each Standard Experience entry is the summary. It uses 1 to 3 highest-signal JD terms and explains the job in simple language.

Bullets 2 and 3 prove different qualification slices. Use 3 to 6 meaningful JD terms only when natural. Never add terms just to reach three.

Use past tense, one direct opening verb, one sentence, one period, and no more than three rendered lines.

For SWE roles, include ownership, leadership, or teamwork when Story.md or approved DES supports it. This must be technical proof, not soft-skill filler:

```text
Led code reviews...
Owned release debugging...
Coordinated backend checks with QA and operations...
Guided implementation decisions...
```

Do not write vague soft-skill bullets such as `Collaborated with cross-functional teams` or `Demonstrated ownership`.

Use strong plain verbs such as Led, Owned, Designed, Built, Shipped, Delivered, Automated, Standardized, Integrated, Restored, Debugged, Reviewed, Coordinated, Guided, Migrated, Validated, Protected, Tested, and Deployed.

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

When compressing, preserve WHAT, HOW, WHERE, WHY, and the highest JD signal. Remove repeated tools, extra tool names, filler adjectives, AI-sounding verbs, duplicate context, secondary metrics, vague result phrases, and then the least important JD term.

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

Safe capability translation is allowed only when true: Java or C++ may support object-oriented programming, and a verified language may support programming-language experience.

Do not rename technologies or infer unsupported claims. Never move evidence between Experience entries or from Projects to Experience.

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

The active manifest decides the real number of Experience and Project objects. AIML uses exactly 3 projects. Non-AIML uses the active plan's required project count.
