# V3 Story.md - Compact Evidence Bank

This file is the evidence source for V3 resume writing.

It is not final resume wording.
It is not a keyword dictionary.
It is not a role profile.
It is not permission to use every fact in every resume.

Profile facts, dates, contact details, JSON shape, JD keyword extraction, and output formatting belong to the runtime input, Prompt.md, and Hotdog.md. This file only answers: what work is supportable, how it worked, why it mattered, and what must not be claimed.

## Core Rules

The JD decides what matters.
Story.md decides what is supportable.
Prompt.md decides structure and pass flow.
Hotdog.md removes unsupported claims, weak phrasing, repeated terms, and keyword stuffing.

Use JD wording from the active JD when the capability is supported, but do not store fixed JD terms here.

Do not use numeric scale claims in resume bullets by default. Use scale language instead: stakeholder-facing workflow, business-critical service, multi-team release path, cross-system integration, research-facing data platform, production support workflow, repeatable deployment path, high-volume file processing, controlled access workflow, reusable engineering pattern.

Use exact numbers only when the user approves a current-run DES item for that exact scope. Even then, prefer the clearest nonnumeric scale language when it reads stronger.

Never mention monetary impact.
Never use friend resumes as Keval evidence.
Never invent tools, platforms, stakeholder groups, domains, architecture ownership, security scope, AI scope, business impact, or production status.
Never describe work with generic big-company wording when a concrete system, workflow, API, dashboard, pipeline, release path, or stakeholder problem is available.

## Bullet Evidence Standard

Every final bullet must be traceable to one card below or an approved DES item.

Each bullet should be compact, past tense, and recruiter-readable while still answering:

- WHAT changed
- HOW it worked technically
- WHERE it fit in the system or workflow
- WHY it mattered for stakeholders
- RESULT or reason, written as outcome language when metrics are not approved

Good outcome language:

- improved reliability for stakeholder-facing workflows
- reduced manual coordination during releases
- restored access to a blocked workflow
- made operational issues easier to diagnose
- improved data quality for research decisions
- turned unstructured requests into controlled system actions
- gave engineering teams a repeatable path for deployment, testing, or recovery

Avoid weak openers when a stronger evidence-backed verb fits. Prefer verbs such as designed, owned, led, integrated, standardized, restored, validated, automated, optimized, coordinated, debugged, hardened, reviewed, mentored, and documented.

## Experience Evidence

### TCS-BACKEND-DATA-WORKFLOW

Scope:
Tata Consultancy Services, Software Engineer and Software Engineer II.

System:
Java and Spring Boot services that moved business data across connected internal systems, database layers, and file workflows used by operational stakeholders.

What I did:
Designed service logic, API contracts, data validation paths, and recovery behavior for backend workflows that needed consistent handoff between systems.

How it worked:
Used Java, Spring Boot, REST APIs, SQL and NoSQL data access, caching patterns, validation logic, logging, and integration testing. Treated each boundary as a contract so downstream workflows received predictable data instead of ambiguous payloads.

Why it mattered:
Stakeholders depended on these workflows to move work forward without manual reconciliation. The engineering value was reliability, clearer ownership at service boundaries, and faster debugging when upstream or downstream systems changed.

Scale language:
business-critical backend workflow; cross-system data movement; stakeholder-facing operational path; reusable API and validation pattern.

Safe capabilities:
backend services, API contracts, distributed workflow, data validation, persistence, caching, debugging, integration testing, stakeholder delivery.

Do not claim:
formal architect title, payment ownership unless DES confirms, public consumer traffic, cloud-native platform ownership, or unsupported database products.

### TCS-CONCURRENT-FILE-STATUS

Scope:
Tata Consultancy Services, Software Engineer II.

System:
File ingestion and processing workflow where stakeholders needed clear status, reliable processing, and fewer stalled handoffs.

What I did:
Improved backend processing, status tracking, and error handling so file work moved through the system with clearer state transitions.

How it worked:
Used Java concurrency patterns, Spring Boot service logic, Redis-style caching where supported, structured status updates, retry-aware handling, and logging to make processing behavior more predictable.

Why it mattered:
Stakeholders could see progress instead of waiting on manual checks, and engineers had better signals when files failed, retried, or needed support.

Scale language:
high-volume file processing; stakeholder-visible status workflow; asynchronous backend processing; operational reliability path.

Safe capabilities:
concurrency, backend processing, status tracking, caching, retry handling, observability, Java service design.

Do not claim:
message broker ownership, event streaming platform ownership, exact throughput metrics, or production traffic volume without approved DES.

### TCS-SHAREPOINT-AUTH-RECOVERY

Scope:
Tata Consultancy Services, Software Engineer II.

System:
SharePoint-connected workflow that depended on secure integration between internal systems and Microsoft services.

What I did:
Restored a blocked authentication path and turned the recovery into a reusable integration pattern for related workflows.

How it worked:
Traced failures across frontend, backend, API, and data paths; coordinated with Microsoft and internal stakeholders; validated an OAuth-based access flow; and tested the fix through QA and UAT before release.

Why it mattered:
The work restored stakeholder access, reduced repeated troubleshooting, and gave the team a safer path for future authentication changes.

Scale language:
blocked workflow recovery; cross-team integration; reusable authentication component; stakeholder access restoration.

Safe capabilities:
OAuth-based integration, SharePoint APIs, authentication recovery, API debugging, stakeholder coordination, QA, UAT, release readiness.

Do not claim:
cybersecurity product work, threat detection, Zero Trust ownership, incident response ownership, or identity-platform architecture.

### TCS-RBAC-ACCESS-CONTROL

Scope:
Tata Consultancy Services, Software Engineer II.

System:
Role-based access workflows used to control stakeholder actions across internal tools.

What I did:
Integrated access-control logic with backend APIs, data stores, and UI paths so stakeholders saw the right actions for their role.

How it worked:
Used Java, Spring Security concepts where supported, REST APIs, relational and document-oriented data access, frontend checks, and test validation to keep access behavior consistent across layers.

Why it mattered:
The work reduced ambiguous permissions, made workflows easier to support, and helped stakeholders trust that sensitive actions followed defined rules.

Scale language:
controlled access workflow; cross-layer authorization path; stakeholder permission model; reusable access pattern.

Safe capabilities:
RBAC, authentication, authorization, backend APIs, UI integration, data access, testing, compliance-aware workflow.

Do not claim:
security engineering ownership, audit platform ownership, IAM architecture, or compliance certification work.

### TCS-CICD-RELEASE-QUALITY

Scope:
Tata Consultancy Services, Software Engineer and Software Engineer II.

System:
Release paths for Java, Spring Boot, React, Python, and related services across development, QA, UAT, and production support environments.

What I did:
Standardized build, validation, deployment, and rollback practices so releases were easier to repeat and safer for stakeholders.

How it worked:
Used Jenkins, GitLab CI/CD, Git, script automation, QA coordination, UAT validation, release documentation, dependency checks, and rollback planning.

Why it mattered:
Engineering teams spent less effort rediscovering release steps, stakeholders received more predictable delivery, and production support had clearer recovery paths.

Scale language:
multi-team release path; repeatable deployment workflow; quality gate; release readiness; production support handoff.

Safe capabilities:
CI/CD, GitLab, Jenkins, Git, release automation, testing gates, rollback planning, documentation, stakeholder delivery.

Do not claim:
platform engineer title, full DevOps ownership, Kubernetes deployment ownership, SRE ownership, or canary release strategy unless DES confirms.

### TCS-LINUX-CLOUD-OPERATIONS

Scope:
Tata Consultancy Services, Software Engineer and Software Engineer II.

System:
Linux and cloud-hosted service environments that required package compatibility, deployment readiness, and operational debugging.

What I did:
Supported migration and runtime readiness work by diagnosing operating-system, dependency, deployment, and environment issues.

How it worked:
Used Linux administration, shell scripting, AWS and Azure exposure where supported, Docker and Kubernetes exposure where supported, package debugging, environment validation, and coordination with cloud support teams.

Why it mattered:
Stakeholders received a more reliable service environment, and engineers gained clearer procedures for upgrades, deployment readiness, and support.

Scale language:
service migration path; environment readiness workflow; cloud operations support; dependency compatibility work.

Safe capabilities:
Linux, AWS, Azure, Docker, Kubernetes, shell scripting, package debugging, deployment validation, cloud support coordination.

Do not claim:
cloud platform ownership, infrastructure architecture, Terraform ownership, Kubernetes cluster administration, or SRE responsibility unless approved DES confirms.

### TCS-PYTHON-ORCHESTRATION

Scope:
Tata Consultancy Services, Software Engineer.

System:
Python workflow that coordinated tickets, validation steps, external handoffs, and backend processing for operational stakeholders.

What I did:
Implemented orchestration logic, validation scripts, API integrations, and status handling so dependent workflows could move through a controlled path.

How it worked:
Used Python, Flask or similar backend patterns where supported, REST APIs, SQL, file validation, structured error handling, logging, and deployment support.

Why it mattered:
Stakeholders gained a single workflow path instead of relying on scattered manual coordination across systems.

Scale language:
cross-system orchestration; stakeholder ticket workflow; validation pipeline; controlled operational handoff.

Safe capabilities:
Python, REST APIs, SQL, validation, orchestration, logging, automation, backend workflow design.

Do not claim:
FastAPI, Airflow, Spark, event streaming, or production platform ownership without approved DES.

### TCS-PYTHON-OPS-AUTOMATION

Scope:
Tata Consultancy Services, Software Engineer.

System:
Operational automation for health checks, environment readiness, support preparation, and recurring engineering checks.

What I did:
Automated repeatable checks and support tasks so engineers could identify environment or workflow problems earlier.

How it worked:
Used Python, shell scripts, SQL checks, API calls, logging, lightweight dashboards or reports where supported, and documentation for handoff.

Why it mattered:
Engineering teams spent less time on manual checks, and stakeholders benefited from faster issue detection before work was blocked.

Scale language:
operations automation; environment readiness; support workflow; recurring engineering check.

Safe capabilities:
Python automation, scripting, SQL validation, health checks, logging, support readiness, documentation.

Do not claim:
observability platform ownership, SRE ownership, autonomous remediation, or exact efficiency gains without approved DES.

### TCS-FRONTEND-DASHBOARDS

Scope:
Tata Consultancy Services, Software Engineer and Software Engineer II.

System:
React and Angular dashboards that surfaced workflow status, operational context, role-based actions, and backend data for stakeholders.

What I did:
Built and maintained UI workflows that connected frontend state, backend APIs, validation logic, and role-aware actions.

How it worked:
Used React, Angular, JavaScript, TypeScript where supported, HTML, CSS, REST API integration, form validation, dashboard views, and testing with backend teams.

Why it mattered:
Stakeholders could review work status, take permitted actions, and understand backend workflow state without asking engineers for manual updates.

Scale language:
stakeholder-facing dashboard; operational visibility; cross-system status view; role-aware workflow.

Safe capabilities:
React, Angular, JavaScript, TypeScript, HTML, CSS, REST APIs, frontend validation, dashboards, RBAC-aware UI.

Do not claim:
design system ownership, accessibility ownership, product design ownership, or unsupported frontend frameworks.

### TCS-OBSERVABILITY-DEBUGGING

Scope:
Tata Consultancy Services, Software Engineer II.

System:
Production support workflows for services, APIs, dashboards, and integrations where engineers needed faster diagnosis.

What I did:
Added and used logs, dashboards, alerts, and structured troubleshooting paths to identify root causes across frontend, backend, data, and service boundaries.

How it worked:
Used Datadog, CloudWatch, application logs, request tracing where supported, dashboard views, API testing, database checks, and stakeholder issue reports.

Why it mattered:
Engineering teams could move from vague symptoms to specific failure points faster, which reduced support friction for stakeholders.

Scale language:
production support workflow; service health visibility; cross-layer debugging; operational diagnosis path.

Safe capabilities:
observability, logging, monitoring, debugging, Datadog, CloudWatch, API tracing, root-cause analysis, stakeholder support.

Do not claim:
SRE ownership, on-call ownership, incident commander role, formal SLA ownership, or full monitoring platform design.

### TCS-SECURE-DEPENDENCY-QUALITY

Scope:
Tata Consultancy Services, Software Engineer II.

System:
Maintenance and quality work across Java, Spring Security, React, certificates, dependencies, and release readiness.

What I did:
Updated dependencies, remediated certificate or authentication issues, reviewed code changes, and validated fixes before release.

How it worked:
Used dependency analysis, Spring Security concepts where supported, certificate troubleshooting, code review, unit or integration testing where supported, QA coordination, and documentation.

Why it mattered:
Stakeholders received more stable workflows, and engineering teams reduced preventable release or runtime failures.

Scale language:
secure maintenance workflow; release-readiness quality check; dependency hygiene; authentication support path.

Safe capabilities:
Spring Security, dependency upgrades, certificate troubleshooting, code review, testing, QA, release readiness.

Do not claim:
security program ownership, vulnerability research, threat modeling ownership, penetration testing, or compliance audit ownership.

### TCS-DOTNET-MICROSOFT-STACK

Scope:
Tata Consultancy Services, Software Engineer and Software Engineer II.

System:
Microsoft-stack portal and admin workflows connected to APIs, databases, authentication, and stakeholder operations.

What I did:
Contributed backend and full-stack features, access-aware workflows, API integrations, and deployment support.

How it worked:
Used C Sharp, .NET, Web API, SQL Server, Entity Framework where supported, Azure exposure, authentication flows, backend validation, and frontend integration.

Why it mattered:
Stakeholders received controlled workflows for managing operational data and approvals through a maintainable Microsoft-stack system.

Scale language:
Microsoft-stack workflow; admin platform; access-aware operational tool; backend and UI integration.

Safe capabilities:
C Sharp, .NET, Web API, SQL Server, Entity Framework, Azure exposure, REST APIs, authentication, RBAC, full-stack development.

Do not claim:
Azure architecture ownership, microservices platform ownership, or full product ownership without DES.

### TCS-LEADERSHIP-DELIVERY

Scope:
Tata Consultancy Services, Software Engineer II.

System:
Team delivery across backend, frontend, release, support, QA, and stakeholder communication.

What I did:
Owned workstreams, reviewed code, mentored junior engineers, coordinated QA/UAT, documented release paths, and communicated risk or tradeoffs to stakeholders.

How it worked:
Combined technical implementation with planning, code review, release validation, handoff notes, and cross-functional coordination.

Why it mattered:
The team delivered with clearer ownership, fewer repeated mistakes, and better alignment between engineering work and stakeholder needs.

Scale language:
team ownership; cross-functional delivery; stakeholder alignment; engineering quality practice; mentoring and code review.

Safe capabilities:
technical leadership, mentoring, code review, Agile delivery, QA/UAT coordination, documentation, stakeholder communication.

Do not claim:
people manager title, hiring authority, staff engineer scope, org-level roadmap ownership, or budget ownership.

### GHI-DATA-PIPELINE

Scope:
Global Health Impact, Software Engineering Intern.

System:
Research-facing data pipeline that prepared health, country, intervention, and outcome data for analysis and stakeholder review.

What I did:
Cleaned, validated, transformed, and integrated research data so downstream APIs and dashboards could use consistent records.

How it worked:
Used Python, SQL, data cleaning scripts, schema checks, validation rules, normalized records, documentation, and collaboration with research stakeholders.

Why it mattered:
Research stakeholders could work from cleaner data and spend less effort resolving inconsistent spreadsheet or source-data issues.

Scale language:
research-facing data pipeline; multi-source data preparation; validated analysis workflow; stakeholder research support.

Safe capabilities:
Python, SQL, ETL-style processing, data validation, schema checks, data quality, documentation, stakeholder collaboration.

Do not claim:
production data engineering ownership, healthcare compliance ownership, patient data, cloud data warehouse ownership, or exact data volume.

### GHI-API-RESEARCH-INTEGRATION

Scope:
Global Health Impact, Software Engineering Intern.

System:
APIs and backend integration paths that exposed validated research data to dashboards and analysis workflows.

What I did:
Implemented or improved API paths, backend data access, validation, and integration behavior for research stakeholders.

How it worked:
Used Python or JavaScript backend patterns where supported, REST APIs, SQL, schema validation, backend filtering, documentation, and testing with dashboard needs in mind.

Why it mattered:
Stakeholders could access structured research data through reusable system interfaces instead of isolated manual exports.

Scale language:
research data API; reusable analysis interface; dashboard integration path; stakeholder-facing data access.

Safe capabilities:
REST APIs, backend integration, SQL, schema validation, filtering, documentation, testing, stakeholder delivery.

Do not claim:
public API ownership, monetized product, clinical workflow, or production healthcare platform.

### GHI-DASHBOARD-VISUALIZATION

Scope:
Global Health Impact, Software Engineering Intern.

System:
Dashboard and visualization workflow for disease, drug, country, intervention, and research analysis.

What I did:
Built or improved dashboard views that connected validated data with stakeholder-facing analysis workflows.

How it worked:
Used React or JavaScript frontend work where supported, API integration, chart or map visualization, filtering, validation, and collaboration with research stakeholders.

Why it mattered:
Stakeholders could explore research data in context instead of reading disconnected tables or asking engineering for manual extracts.

Scale language:
research dashboard; stakeholder-facing visualization; data exploration workflow; API-backed analysis view.

Safe capabilities:
React, JavaScript, dashboarding, data visualization, API integration, filtering, frontend validation, stakeholder collaboration.

Do not claim:
formal product analytics ownership, executive reporting platform, or unsupported visualization libraries.

### GHI-ML-PREDICTION

Scope:
Global Health Impact, Software Engineering Intern.

System:
Machine learning exploration connected to research data workflows.

What I did:
Supported model-oriented analysis by preparing data, validating features, and connecting prediction outputs to stakeholder review where supported.

How it worked:
Used Python, data preprocessing, feature validation, model evaluation concepts, documented assumptions, and review with research stakeholders.

Why it mattered:
The work helped stakeholders reason about prediction outputs with clearer data preparation and review boundaries.

Scale language:
research ML workflow; model-support pipeline; prediction review path; validated feature workflow.

Safe capabilities:
Python, machine learning, data preprocessing, feature validation, model evaluation, research collaboration.

Do not claim:
production ML system, MLOps ownership, model deployment ownership, exact accuracy metrics, clinical prediction, or AI product ownership unless approved DES confirms.

### GHI-STAKEHOLDER-DELIVERY

Scope:
Global Health Impact, Software Engineering Intern.

System:
Internship delivery across research, engineering, data quality, APIs, dashboards, and stakeholder feedback.

What I did:
Translated research needs into technical tasks, clarified data assumptions, communicated progress, and adjusted implementation based on feedback.

How it worked:
Worked across data preparation, backend integration, dashboard views, documentation, and stakeholder review.

Why it mattered:
The work connected technical implementation to research decisions instead of producing isolated code.

Scale language:
research stakeholder delivery; cross-functional intern ownership; feedback-driven engineering; data-to-dashboard workflow.

Safe capabilities:
requirements clarification, stakeholder collaboration, documentation, API/dashboard delivery, data quality, technical communication.

Do not claim:
program ownership, research authorship, medical decision ownership, or production product management.

### EDU-TEACHING-ASSISTANT

Scope:
Binghamton University teaching assistant work.

System:
Course support for database systems and object-oriented programming.

What I did:
Reviewed assignments, explained programming and database concepts, helped students debug, and reinforced software design expectations.

How it worked:
Used SQL, database design concepts, object-oriented programming, Java-style reasoning where supported, grading rubrics, feedback, and office-hour support.

Why it mattered:
Students received clearer technical feedback, and course staff had consistent support for evaluating software assignments.

Scale language:
academic code review; student support workflow; software-design coaching; database learning support.

Safe capabilities:
SQL, database systems, OOP, code review, debugging, teaching, feedback, technical communication.

Do not claim:
faculty role, curriculum ownership, research supervision, or production engineering work.

## Project Evidence

Use projects only when the JD keyword is important and professional experience does not prove it cleanly. Project bullets must not overpower professional experience unless the role is explicitly AI, ML, developer tooling, full-stack product, or project-heavy.

### PROJ-JOBPULSE

System:
Job aggregation and semantic search project for collecting, normalizing, ranking, and exploring job postings.

What I did:
Designed ingestion, search, ranking, dashboard, and workflow logic so job data could move from raw posting sources into a searchable product experience.

How it worked:
Used backend APIs, database storage, search or embedding concepts where supported, deduplication, filtering, dashboard UI, and job-matching logic.

Why it mattered:
Turned scattered job data into a structured workflow for search, comparison, and faster application decisions.

Scale language:
multi-source job ingestion; searchable workflow; ranking and filtering system; candidate-facing product workflow.

Safe capabilities:
backend APIs, search, embeddings if supported by current repo/story, deduplication, ranking, dashboard, automation, full-stack product.

Do not claim:
official ATS integration, real employer partnership, commercial traffic, or exact posting volume unless DES confirms.

### PROJ-FRAUDSIFT

System:
Fraud and transaction analytics project for detecting suspicious patterns and explaining risk signals.

What I did:
Built data preparation, feature extraction, risk scoring, and dashboard workflows for transaction analysis.

How it worked:
Used Python, machine learning concepts, SQL or data storage where supported, feature engineering, evaluation, explainability views, and API/dashboard integration.

Why it mattered:
Made transaction patterns easier to review by combining model signals with human-readable context.

Scale language:
risk analytics workflow; model-supported review; transaction pattern analysis; explainable ML project.

Safe capabilities:
Python, ML, feature engineering, risk scoring, evaluation, APIs, dashboards, data analysis.

Do not claim:
bank production deployment, fraud prevention authority, compliance ownership, real customer transactions, or financial impact.

### PROJ-FILINGQUERY

System:
SEC filing intelligence project for retrieving source-grounded answers from long financial documents.

What I did:
Built retrieval, citation grounding, query handling, and answer validation workflows.

How it worked:
Used Python, RAG concepts, embeddings, vector search, document chunking, retrieval ranking, citation extraction, and evaluation checks.

Why it mattered:
Helped stakeholders inspect long filings through grounded answers instead of untraceable summaries.

Scale language:
document intelligence workflow; citation-grounded retrieval; financial document search; source-backed answer path.

Safe capabilities:
RAG, embeddings, vector search, retrieval, document parsing, citation grounding, Python, evaluation.

Do not claim:
investment advice, production financial platform, official SEC integration, or legal/accounting accuracy guarantees.

### PROJ-EVALTRACE

System:
RAG evaluation project for checking answer quality, citation grounding, and regression behavior.

What I did:
Created evaluation workflows that compared model outputs against expected behavior and highlighted failures.

How it worked:
Used benchmark prompts, retrieval checks, citation validation, scoring logic, CI-style quality gates where supported, and structured reports.

Why it mattered:
Made AI quality easier to review before changes reached stakeholders.

Scale language:
AI evaluation workflow; regression guardrail; citation-quality check; model-output review path.

Safe capabilities:
RAG evaluation, test cases, quality gates, retrieval validation, citation checks, structured reporting.

Do not claim:
formal research benchmark, production MLOps platform, or exact hallucination-rate improvement unless DES confirms.

### PROJ-REVIEWBOT

System:
Multi-agent pull request review project for code analysis, feedback, and developer workflow support.

What I did:
Designed agent-style review flow that inspected code changes, produced structured feedback, and supported developer decisions.

How it worked:
Used LLM prompting, repository context, diff analysis, structured output, review rules, and developer workflow integration where supported.

Why it mattered:
Helped developers catch issues earlier and turn review feedback into a more repeatable workflow.

Scale language:
developer-tool workflow; agentic code review; structured feedback loop; repository-aware analysis.

Safe capabilities:
LLMs, agents, prompt engineering, code review, diff analysis, structured outputs, developer tooling.

Do not claim:
replacement for human review, production adoption, security scanner ownership, or guaranteed bug detection.

### PROJ-RESUME-AGENT

System:
Evidence-grounded resume automation system for turning job descriptions, rules, story evidence, and JSON outputs into tailored resume artifacts.

What I did:
Built prompt flows, evidence checks, JSON contracts, reviewer passes, and document-generation support.

How it worked:
Used Python, prompt engineering, structured JSON, validation logic, resume rules, document rendering, workflow orchestration, and iterative repair prompts.

Why it mattered:
Turned resume tailoring into a controlled workflow that preserved evidence boundaries while adapting to JD requirements.

Scale language:
evidence-grounded AI workflow; structured resume pipeline; prompt orchestration; rule-driven document generation.

Safe capabilities:
Python, LLM workflows, prompt engineering, JSON validation, document generation, review agents, evidence grounding.

Do not claim:
official hiring partnership, guaranteed interview outcomes, ATS vendor access, or production SaaS traffic.

### PROJ-JOBFILL

System:
Browser automation project for job application workflows.

What I did:
Built extension-style workflows that helped read page context, populate forms, and guide application steps.

How it worked:
Used browser extension concepts, DOM interaction, structured form data, automation logic, and AI-assisted matching where supported.

Why it mattered:
Reduced repetitive form work and made application steps more consistent.

Scale language:
browser automation workflow; application assistance; form-filling system; candidate workflow tool.

Safe capabilities:
browser extension, JavaScript, DOM automation, workflow automation, structured data, AI-assisted form filling.

Do not claim:
automatic submission without review, employer system integration, credential handling, or real hiring-platform partnership.

### PROJ-BISTRO-AI

System:
Full-stack restaurant ordering project with a mobile UI, backend API, PostgreSQL data model, and AI waiter flow that turns natural language into controlled cart actions.

What I did:
Implemented API, mobile, database, and AI-ordering paths so a menu request could become validated cart updates instead of free-form model text.

How it worked:
Used TypeScript, Express, Prisma, PostgreSQL, REST APIs, Zod validation, Anthropic Claude, Expo, React Native, Zustand-style state, Docker demo support, server caching, mobile caching, retries, and timeout handling where supported by the repo.

Why it mattered:
The project showed how to wrap an AI experience with typed contracts, validation, cache boundaries, and constrained actions so stakeholders could trust the system behavior.

Scale language:
structured AI ordering workflow; typed cart-action system; mobile-to-API product flow; bounded AI integration.

Safe capabilities:
TypeScript, Express, Prisma, PostgreSQL, REST APIs, Zod, Claude, React Native, Expo, Docker, caching, retries, AI integration.

Do not claim:
real restaurant deployment, payment processing, delivery logistics, production customers, or commercial usage.

### PROJ-AI-ENGINEERING-WORKFLOW

System:
Personal engineering workflow using AI tools for coding, review, prompt iteration, documentation, and debugging support.

What I did:
Used AI-assisted development to speed up exploration, compare implementation options, and review code while keeping final responsibility on human validation.

How it worked:
Used prompt iteration, repository context, test runs, code review, structured outputs, and manual verification.

Why it mattered:
Improved the speed and quality of engineering iteration without treating AI output as automatically correct.

Scale language:
AI-assisted engineering workflow; human-validated coding loop; prompt-driven implementation support; review-backed development.

Safe capabilities:
AI-assisted coding, prompt engineering, code review, testing, documentation, developer tooling.

Do not claim:
AI tools at TCS unless approved DES confirms, autonomous production changes, or unreviewed AI-generated code.

## DES Needed Or Partial Evidence

Ask DES before using these as strong claims:

- exact numeric metrics, volumes, percentages, monetary values, or named counts
- FastAPI in professional experience
- Node.js or TypeScript in professional experience
- Airflow, Spark, Flink, Terraform, GraphQL, or formal MLOps
- Kubernetes cluster administration
- AWS or Azure architecture ownership
- production ML model deployment
- formal security engineering, threat detection, IAM architecture, or compliance audit work
- payment system ownership
- public customer traffic
- accessibility ownership or design-system ownership
- official ATS integration or employer partnership
- real restaurant deployment for Bistro AI

## Project Selection Guidance

Backend Java or infrastructure JD:
Use TCS backend, release quality, Linux/cloud operations, observability, and leadership evidence first. Use projects only for missing AI, search, or product keywords.

Backend Python JD:
Use TCS Python orchestration and operations automation first, then GHI data/API evidence. Use projects for FastAPI, RAG, or AI only if professional evidence does not support the JD term.

Full-stack JD:
Use TCS frontend dashboards, backend workflows, RBAC/access control, and GHI dashboard/API evidence. Use Bistro AI, JobFill, or Resume Agent when the JD values product-style full-stack delivery.

AI or ML JD:
Use GHI ML only for research ML support, then use FilingQuery, EvalTrace, ReviewBot, Resume Agent, FraudSift, JobPulse, or Bistro AI based on the closest JD capability.

Forward-deployed or customer-facing JD:
Use TCS stakeholder delivery, SharePoint recovery, Python orchestration, GHI stakeholder delivery, Resume Agent, JobFill, and Bistro AI when the JD emphasizes requirements, workflow design, integration, and demos.

## Forbidden Resume Claims

Never claim these unless the user approves a scoped DES item for the exact role, project, and wording:

- numeric impact or exact scale metrics
- monetary impact
- public customer volume
- formal manager title
- staff engineer or architect title
- SRE ownership
- security program ownership
- compliance certification ownership
- production MLOps ownership
- cloud architecture ownership
- Kubernetes platform ownership
- Terraform ownership
- GraphQL, Airflow, Spark, Flink, or Kafka as professional experience unless the selected story or DES proves it
- AI-assisted coding at TCS
- commercial SaaS adoption for personal projects
- friend resume facts

## Final Reminder

Write story-backed bullets that sound like a strong engineer explaining a real system to a recruiter and hiring manager:

specific system, concrete mechanism, stakeholder reason, defensible outcome.

No keyword stuffing.
No metric theater.
No inflated titles.
No generic big-company phrasing.
