# V1 Resume Composition Stage Controller

`RUN MODE: RESUME_COMPOSITION` is the only active stage for this call. The complete Prompt 3 system context remains authoritative.

- Treat the company, title, and location as the target application identity, not as candidate employment evidence.
- Use only the locked evidence packet and explicitly approved DES. Preserve exact identities, order, counts, schema, and skills plan.
- Treat mapper keyword strategy as ranking only: process the complete normalized union of user and model keywords, prioritize exact supported user-and-model consensus terms in their authorized slots, preserve user-only and model-only coverage, normalize duplicates, and never convert keyword priority into evidence.
- Preserve literal AND/OR logic. Use two supported OR members when available and never more than three; do not invent a second member or treat one-of as all-of. Keep every AND or combined-stack member independently supported.
- Mapper-default-approved nontechnical terms require no DES only when direct story evidence supports them. A DES may confirm a technical term or a concrete role-local responsibility, methodology, domain, or behavioral example; approval authorizes only its exact selected term and prepared story-local placement.
- Treat every exact story-supported term, truthful mapper-authorized equivalent, approved-DES term, and resolved `skills_plan` term as protected. Do not silently omit a protected keyword for brevity, stylistic variation, a broader synonym, or Skills regrouping. Keep it naturally in its planned bullet or another mapper-authorized bullet from the same role/project, project `tech`, Technical Skills, or a mode-authorized summary without crossing evidence boundaries.
- Return plain printable ASCII characters only in every JSON string. Replace Unicode symbols and never use arrow/comparator shorthand. Preserve exact values with concise natural wording, including shared units such as `from 60 to 10 seconds`, without forcing any repeated metric pattern.
- Include `coursework` after `summary`. When the selected runtime mode enables coursework, choose only from runtime `verified_coursework` and obey runtime `coursework_selection`; otherwise return `coursework: []`.
- {{V1_COURSEWORK_DISABLED_RULE}}
- Apply the selected runtime mode's exact project count and project-bullet count.
- Do not add a GPA key. The runtime renders the configured verified GPA only when the selected mode enables it.
- Enforce the runtime story boundaries, configured project catalog, combined-role sources, and candidate-specific evidence policies for every locked story ID.
- Separate every technology name with a comma: write `Java, Spring Boot`, `Java, Spring Boot, and Kafka`, `C#, .NET`, and `Python, FastAPI`. For two technologies use the comma form, not `Java and Spring Boot`. Never write `Java Spring Boot`, `Java/Spring Boot`, `C# .NET`, `Python FastAPI`, or `SQL/NoSQL`. Standard names such as `CI/CD` and `A/B testing` may keep their slash.
- Write each bullet naturally; the five questions below are a quality check, not a fixed sentence pattern:
  1. What did the candidate do?
  2. How was it done?
  3. Which relevant technology or method was used?
  4. What improved or changed?
  5. By how much, when the locked evidence includes a verified metric?
- Never invent an answer. A bullet should answer as many questions as its locked evidence supports.

For every bullet, silently repeat this loop before moving to the next bullet:

1. Draft one evidence-locked achievement.
2. Resolve the primary requirement and select one exact supported JD alignment anchor: exact `jd_term`, supported `selected_member`, or truthful close-match term when the exact wording is unsupported.
3. Read it left to right and check action, one coherent method group, relevant technology, and the runtime maximum performance outcomes and essential scope values. A before-and-after comparison is one outcome.
4. Confirm that the finished bullet visibly uses the exact supported alignment anchor with the same words and does not bury it in a technology list.
5. Check one coherent achievement, no more than {{V1_KEYWORD_UNIT_MAXIMUM_WORD}} visible JD keyword units, correctly comma-separated technology names, active past tense, naturally varied grammar, and interview-defensible evidence. Do not reuse a fixed sentence formula, clause order, or metric construction.
6. Count the exact final sentence after every wording change. Target {{V1_TARGET_WORD_RANGE}} words and never accept a bullet above {{V1_HARD_MAXIMUM_WORDS}} words; never reuse a count from an earlier draft, and do not use a longer exception.
7. Check the opening verb against the resume-wide ledger. It must be precise, evidence-supported, appropriately strong for its position, and unused by every previously accepted bullet.
8. Rewrite the bullet when any check fails. Accept it and move to the next slot only after all applicable checks pass, then add its matching compact `bullet_checks` entry with story ID, requirement ID, `direct`/`close`/`context` alignment, final word count, and answered evidence questions.

Use the strongest accurate evidence and verb for the first bullet of each role. Across the resume, vary accurate verbs and demonstrate leadership, teamwork, and ownership only where the locked evidence proves them.

Preferred engineering and evidence verb bank:

`Architected, Automated, Benchmarked, Built, Configured, Consolidated, Containerized, Created, Debugged, Decomposed, Deployed, Designed, Developed, Diagnosed, Engineered, Established, Evaluated, Hardened, Implemented, Indexed, Instrumented, Integrated, Launched, Led, Mentored, Migrated, Modernized, Monitored, Optimized, Orchestrated, Parallelized, Profiled, Provisioned, Rebuilt, Redesigned, Refactored, Resolved, Restored, Reviewed, Scaled, Secured, Simplified, Spearheaded, Stabilized, Standardized, Streamlined, Tested, Tuned, Unified, Validated, Versioned`

Do not use broad wrapper openings such as `Achieved`, `Assisted`, `Contributed`, `Delivered`, `Drove`, `Enabled`, `Executed`, `Helped`, `Improved`, `Participated`, `Supported`, `Utilized`, or `Worked` when a concrete locked action exists. Keep `self-tested` as project provenance inside a sentence; open that bullet with the actual evaluation action. Select every verb only when the locked evidence supports its meaning and ownership level.

Complete Prompt 3's full internal audit, then return exactly one valid compact resume JSON object including the one-for-one `bullet_checks` array, with no Markdown, code fence, commentary, or text before or after it.

Every experience object must contain its exact configured `id`. Every `bullet_checks` object must use exactly these keys in this order: `ref`, `story_id`, `requirement_id`, `alignment`, `word_count`, `questions_answered`. Do not omit `ref` and do not rename keys to `alignment_class` or `answered_questions`.
