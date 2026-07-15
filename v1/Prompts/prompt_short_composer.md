# V1 Resume Composition Stage Controller

`RUN MODE: RESUME_COMPOSITION` is the only active stage for this call. The complete Prompt 3 system context remains authoritative.

- Treat the company, title, and location as the target application identity, not as candidate employment evidence.
- Use only the locked evidence packet and explicitly approved DES. Preserve exact identities, order, counts, schema, and skills plan.
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
3. Read it left to right and check action, method, relevant technology, result or scope, and verified metric when available.
4. Confirm that the finished bullet visibly uses the exact supported alignment anchor with the same words and does not bury it in a technology list.
5. Check one coherent achievement, no more than three visible JD keyword units, active past tense, natural grammar, and interview-defensible evidence.
6. Count the words. Target 18 to 24 words; compress every bullet above 24 words; never accept a bullet above 28 words.
7. Check the opening verb against the resume-wide ledger. It must be precise, evidence-supported, appropriately strong for its position, and unused by every previously accepted bullet.
8. Rewrite the bullet when any check fails. Accept it and move to the next slot only after all applicable checks pass.

Use the strongest accurate evidence and verb for the first bullet of each role. Across the resume, vary accurate verbs and demonstrate leadership, teamwork, and ownership only where the locked evidence proves them.

Preferred engineering and evidence verb bank:

`Architected, Automated, Benchmarked, Built, Configured, Consolidated, Containerized, Created, Debugged, Decomposed, Deployed, Designed, Developed, Diagnosed, Engineered, Established, Evaluated, Hardened, Implemented, Indexed, Instrumented, Integrated, Launched, Led, Mentored, Migrated, Modernized, Monitored, Optimized, Orchestrated, Parallelized, Profiled, Provisioned, Rebuilt, Redesigned, Refactored, Resolved, Restored, Reviewed, Scaled, Secured, Simplified, Spearheaded, Stabilized, Standardized, Streamlined, Tested, Tuned, Unified, Validated, Versioned`

Do not use broad wrapper openings such as `Achieved`, `Assisted`, `Contributed`, `Delivered`, `Drove`, `Enabled`, `Executed`, `Helped`, `Improved`, `Participated`, `Supported`, `Utilized`, or `Worked` when a concrete locked action exists. Keep `self-tested` as project provenance inside a sentence; open that bullet with the actual evaluation action. Select every verb only when the locked evidence supports its meaning and ownership level.

Complete Prompt 3's full internal audit, then return exactly one valid compact resume JSON object with no Markdown, code fence, commentary, or text before or after it.
