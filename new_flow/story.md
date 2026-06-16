# Story.md — Keval Shah Evidence Bank vFinal Safe

## 0. Control Rules
This file is the single evidence source for JD-driven resume generation.
It is not final resume wording.
It is not a biography.
It is not permission to use every fact in every resume.

Core rule:
The JD decides what matters.
Story.md decides what is allowed.
If a JD term is not supported in ACTIVE EVIDENCE, create a DES candidate and wait for approval.

Prompt.md controls structure, schema, config, layout, project count, TA placement, header format, and output behavior.
Story.md controls evidence only.
Do not use Story.md to override Prompt.md structure rules.

Use only ACTIVE EVIDENCE sections for resume claims.
Use COMPRESSED RAW ARCHIVE only to understand context or propose DES.
Do not write resume bullets directly from raw archive notes.

Evidence strength:
HIGH = system + technology + action + scope/metric/outcome
MEDIUM = confirmed professional use, but exact scope/outcome incomplete
LOW = exposure or limited detail
CANNOT = not enough proof to use

Resume-use labels:
P1 = professional production proof
P2 = project proof
P3 = approved current-run DES proof
P4 = skill-only or partial proof
P5 = cannot defend

Never invent:
tools, testing types, metrics, users, outcomes, domains, dates, titles, leadership scope, architecture ownership, production status, AI/ML claims, cloud ownership, scale, or business value

Never mention dollar values in final resume output.
Never call TA a Software Engineer role.
Never use `vibe coding` in resume output.
Use `AI-assisted development` only for AI tooling/devtools roles when relevant.

## 1. Required Story Reading Report
Before PASS 1, the resume creator must output:
- Story.md found: YES/NO
- Active evidence cards scanned: count
- Metric map scanned: YES/NO
- Technology map scanned: YES/NO
- DES-needed claims scanned: YES/NO
- Forbidden claims scanned: YES/NO
- Evidence IDs selected for this JD
- Evidence IDs rejected for this JD
- JD terms not found in active story

Every summary sentence, skill row, experience bullet, and project bullet must trace to an Evidence ID or approved DES ID.
If a claim has no Evidence ID or approved DES ID, exclude it.

## 2. Locked Profile
Name: Keval Shah

Default contact:
New York, NY | (607) 235-1181 | keval.shah61298@gmail.com | linkedin.com/in/keval-shah0612 | github.com/kevalshah0612

LinkedIn: https://www.linkedin.com/in/keval-shah0612
GitHub: https://github.com/kevalshah0612

Header guidance:
- Final resume header should render as:
  1. Name
  2. Target Role | New York, NY | relocation/work-location signal
  3. phone | email | LinkedIn | GitHub
- For strict onsite roles outside New York: `[Target Role] | New York, NY | Open to relocate to [Target City, State]`
- For state/region roles: `[Target Role] | New York, NY | Open to relocate to [Target State/Region]`
- For broad U.S. roles: `[Target Role] | New York, NY | Open to relocate across the U.S.`
- For remote U.S. roles: `[Target Role] | New York, NY | Open to remote U.S. roles`
- For New York / NYC roles: `[Target Role] | New York, NY`
- Do not write target city as current city unless it is true
- Do not replace GitHub URL with only `GitHub`

Education:
1. Binghamton University, State University of New York
   - Master of Science, Computer Science, AI Specialization, GPA: 4.00
   - Binghamton, NY
   - Jan 2025 - May 2026
   - Use AI specialization prominently for AI tooling, AI/ML, automation, and new-grad roles

2. Gujarat Technological University
   - Bachelor of Engineering, Computer Engineering, GPA: 3.85
   - Ahmedabad, India
   - Graduation: Sep 2020
   - Resume compact form may use: Bachelor of Engineering, Computer Engineering | 2020

Professional experience:
1. Global Health Impact
   - Software Engineering Intern
   - New York, NY
   - Jun 2025 - Aug 2025

2. Tata Consultancy Services
   - Software Engineer II
   - Gandhinagar, India
   - Oct 2022 - Dec 2024
   - Client context: Wabtec Corporation, Fortune 500; use only inside bullets when relevant

3. Tata Consultancy Services
   - Software Engineer
   - Gandhinagar, India
   - Mar 2021 - Sep 2022
   - Remote, India may be used only if true for that period
   - Client context: Wabtec Corporation, Fortune 500; use only inside bullets when relevant

4. Binghamton University
   - Teaching Assistant, Database Systems and Object-Oriented Programming
   - Binghamton, NY
   - Aug 2025 - Present
   - Use as experience only for entry/new-grad/internship/code-review/teaching-heavy roles
   - TA proof is evidence only and must not be written under Education
   - Final JSON must keep all `education.ta_bullet` values empty
   - If TA is needed, use a separate Professional Experience object for Binghamton University

Projects:
- JobPulse: https://github.com/kevalshah0612/jobpulse
- FraudSift: https://github.com/kevalshah0612/fraudsift
- ReviewBot: https://github.com/kevalshah0612/reviewbot
- FilingQuery: https://github.com/kevalshah0612/filingquery
- EvalTrace: https://github.com/kevalshah0612/evaltrace
- Resume Agent: https://github.com/kevalshah0612/resume-agent
- JobFill AI Extension: https://github.com/kevalshah0612/jobfill-ai-extension

## 3. Resume Family Routing
Backend / platform roles:
Use TCS API, CI/CD, cloud, Linux, observability, Java/Spring Boot, Redis, SQL/NoSQL, production support, release ownership.

Full-stack roles:
Use TCS frontend/dashboard, REST APIs, auth/RBAC, GHI dashboard, JobPulse, JobFill, Resume Agent if automation/product tooling helps.

AI tooling / developer productivity roles:
Use Resume Agent, JobFill, ReviewBot, EvalTrace, FilingQuery, AI-assisted development process, CI/CD automation, Python tooling, GHI when relevant.

AI/ML entry roles:
Use MS CS AI specialization, GHI ML/data pipeline, FraudSift, FilingQuery, EvalTrace, Resume Agent, JobPulse as relevant.

Entry/new-grad SWE roles:
Education first, Technical Skills second, GHI first when recent U.S. internship is strongest, combined TCS second, TA as Professional Experience if relevant, project count controlled by Prompt.md layout contract.

Mid-level SWE roles:
Summary first, Technical Skills second, TCS SWE II first, TCS SWE second, GHI short, normally 2 projects by Prompt.md layout contract, Education bottom.

Internship roles:
Education first, Technical Skills second, GHI/TA/projects emphasized, TCS included only when it helps the JD.

## 4. Section Order Rules
student_entry:
Education -> Technical Skills -> Professional Experience -> Projects

professional_entry:
Summary -> Technical Skills -> Professional Experience -> Projects -> Education

mid:
Summary -> Technical Skills -> Professional Experience -> Projects -> Education

aiml_entry:
Education -> Technical Skills -> Projects -> Professional Experience

aitool_mid:
Summary -> Technical Skills -> Professional Experience -> Projects -> Education

internship:
Education -> Technical Skills -> Professional Experience -> Projects

## 5. Summary Strategy
Entry summary:
MS Computer Science candidate specializing in AI with 3+ years of prior software engineering experience. Focus on JD stack, current U.S. education, internship/project proof, and production transferability.

Mid summary:
Software engineer with 3+ years building production APIs, full-stack workflows, CI/CD pipelines, observability, security/access-control, and enterprise systems. Mention MS CS AI specialization only as additive depth.

AI tooling summary:
Software engineer and MS Computer Science AI specialization candidate building LLM-assisted automation, developer tooling, workflow systems, and production software.

Do not claim direct AI/ML engineer identity unless the JD and evidence support it.
Do not claim cybersecurity/fintech/healthcare/product domain ownership unless evidence is direct.

## 6. Metric Map
10,000+ users -> TCS2-SECURITY-IDENTITY, TCS2-JAVA-CONCURRENCY
48 hours / 2 days -> TCS2-SECURITY-IDENTITY
60 seconds to 10 seconds -> TCS2-JAVA-CONCURRENCY
83% reduction -> TCS2-JAVA-CONCURRENCY
40 to 50 seconds saved per file -> TCS2-JAVA-CONCURRENCY
5-member team -> TCS2-JAVA-CONCURRENCY
9-developer team -> TCS-OWNERSHIP-LEADERSHIP, TCS1-CICD
5 junior developers -> TCS-OWNERSHIP-LEADERSHIP
40+ production releases -> TCS1-CICD, TCS-OWNERSHIP-LEADERSHIP
40+ production-ready deployments -> TCS-OWNERSHIP-LEADERSHIP
7+ applications -> TCS1-CICD, TCS1-LINUX-MIGRATION, TCS-OWNERSHIP-LEADERSHIP
10+ applications -> TCS2-CLOUD-PLATFORM, TCS-OPERATIONS-AUTOMATION, TCS-CICD-RUBY-GITLAB-AUTOMATION
10 enterprise applications -> TCS2-SECURITY-IDENTITY, TCS2-CLOUD-PLATFORM
22% ticket reduction -> TCS2-SECURITY-IDENTITY
30% improvement -> TCS2-CLOUD-PLATFORM, TCS-OPERATIONS-AUTOMATION, TCS-CSHARP-DOTNET
95% manual deployment reduction -> TCS-CICD-RUBY-GITLAB-AUTOMATION
90% manual health/data-prep reduction -> TCS-OPERATIONS-AUTOMATION, GHI-PIPELINE
3 connected applications -> TCS2-OBSERVABILITY
hours to minutes -> TCS2-OBSERVABILITY
3 Java/Spring Boot applications -> TCS1-API-DATA
9 engineering teams -> TCS1-API-DATA
2 months -> TCS1-API-DATA
zero downtime -> TCS1-CICD, TCS1-LINUX-MIGRATION
3+ appreciations -> TCS-AWARDS
150+ countries -> GHI-API
hours to 30 seconds -> GHI-API
6 research teams -> GHI-DASHBOARD
10M+ weekly WHO health records -> GHI-PIPELINE
10,000+ job postings -> PROJ-JOBPULSE
22,000+ transactions -> PROJ-FRAUDSIFT
5,000+ SEC filings -> PROJ-FILINGQUERY
23% to 4% hallucination reduction -> PROJ-EVALTRACE
120+ students -> EDU-TA-CODE-REVIEW

Forbidden metric use:
- Do not use dollar values in final resume
- Do not mention $1.2M or $30K monthly in resume
- Do not invent exact savings beyond allowed non-dollar metrics

## 7. Technology Map
Java -> TCS1-API-DATA, TCS2-JAVA-CONCURRENCY, TCS2-SECURITY-IDENTITY, EDU-TA-CODE-REVIEW
Python -> TCS2-CLOUD-PLATFORM, TCS-OPERATIONS-AUTOMATION, GHI-PIPELINE, PROJ-FRAUDSIFT, PROJ-FILINGQUERY, PROJ-EVALTRACE, PROJ-RESUME-AGENT
JavaScript -> TCS2-FRONTEND, TCS2-OBSERVABILITY, GHI-DASHBOARD, PROJ-JOBPULSE, PROJ-JOBFILL
TypeScript -> TCS2-FRONTEND, TCS2-OBSERVABILITY, PROJ-JOBPULSE, PARTIAL-TCS-TS-PRODUCTS
Node.js -> PROJ-JOBPULSE, PROJ-RESUME-AGENT if applicable, PARTIAL-TCS-NODE-WORKFLOWS
PHP -> PARTIAL-TCS-PHP-WORK
C#/.NET -> TCS-CSHARP-DOTNET
Ruby -> TCS-CICD-RUBY-GITLAB-AUTOMATION
C++ -> EDU-TA-CODE-REVIEW, TCS2-JAVA-CONCURRENCY, TCS-LOW-LEVEL-SYSTEMS
C -> TCS-LOW-LEVEL-SYSTEMS
React -> TCS2-FRONTEND, TCS2-OBSERVABILITY, GHI-DASHBOARD, PROJ-JOBPULSE, PROJ-FRAUDSIFT
Angular -> TCS2-FRONTEND
HTML/CSS -> TCS2-FRONTEND, GHI-DASHBOARD, PROJ-JOBFILL
Bootstrap -> TCS2-FRONTEND
Material UI -> TCS-UIUX
REST APIs -> TCS1-API-DATA, TCS2-SECURITY-IDENTITY, GHI-API, PROJ-JOBPULSE
Spring Boot -> TCS1-API-DATA, TCS2-SECURITY-IDENTITY
Spring Security -> TCS2-SECURITY-IDENTITY, TCS-SAST-QUALITY
Microservices -> TCS1-API-DATA, TCS2-CLOUD-PLATFORM
Distributed systems -> TCS1-API-DATA, TCS2-JAVA-CONCURRENCY, TCS2-SECURITY-IDENTITY
Redis -> TCS1-API-DATA, PROJ-JOBPULSE
OAuth 2.0 / OIDC / JWT / SSO -> TCS2-SECURITY-IDENTITY, TCS-AUTH-STORAGE
RBAC -> TCS2-SECURITY-IDENTITY
TLS/SSL -> TCS2-SECURITY-IDENTITY, TCS1-LINUX-MIGRATION
SQL -> TCS1-API-DATA, TCS-DATABASES, GHI-PIPELINE, EDU-TA-CODE-REVIEW
MySQL -> TCS1-API-DATA, TCS-DATABASES
Oracle -> TCS-DATABASES, TCS-OPERATIONS-AUTOMATION
Microsoft SQL Server -> TCS-DATABASES
NoSQL -> TCS1-API-DATA, TCS-DATABASES, GHI-PIPELINE, EDU-TA-CODE-REVIEW
PostgreSQL -> GHI-PIPELINE, PROJ-JOBPULSE, PROJ-FRAUDSIFT, PROJ-FILINGQUERY
MongoDB -> GHI-PIPELINE
AWS -> TCS2-CLOUD-PLATFORM, TCS1-LINUX-MIGRATION, TCS1-API-DATA, TCS-AUTH-STORAGE, GHI-API
Azure -> TCS2-CLOUD-PLATFORM, TCS1-LINUX-MIGRATION
GCP -> TCS2-CLOUD-PLATFORM
Docker -> TCS1-CICD, TCS2-CLOUD-PLATFORM, TCS-OPERATIONS-AUTOMATION, PROJ-FRAUDSIFT, PROJ-FILINGQUERY
Kubernetes -> TCS1-CICD, TCS2-CLOUD-PLATFORM, TCS-OPERATIONS-AUTOMATION
OpenShift -> TCS1-CICD, TCS2-CLOUD-PLATFORM
Terraform -> TCS2-CLOUD-PLATFORM, TCS1-LINUX-MIGRATION
Linux -> TCS1-LINUX-MIGRATION, TCS2-CLOUD-PLATFORM, TCS-LOW-LEVEL-SYSTEMS
Bash/Shell -> TCS1-LINUX-MIGRATION, TCS1-CICD, TCS2-CLOUD-PLATFORM
Git -> TCS1-CICD, TCS-OWNERSHIP-LEADERSHIP, EDU-TA-CODE-REVIEW, PROJ-REVIEWBOT, PROJ-EVALTRACE
GitLab -> TCS1-CICD, TCS-CICD-RUBY-GITLAB-AUTOMATION
GitLab CI/CD -> TCS1-CICD, TCS-CICD-RUBY-GITLAB-AUTOMATION
Jenkins -> TCS1-CICD
GitHub Actions -> PROJ-REVIEWBOT, PROJ-EVALTRACE
Datadog -> TCS2-OBSERVABILITY
CloudWatch -> TCS2-OBSERVABILITY
SAST / Polaris / Black Duck -> TCS-SAST-QUALITY
JUnit -> PARTIAL-TCS-JUNIT-TESTING
Pytest -> PARTIAL-GHI-PYTEST-TESTING, PROJ-FRAUDSIFT, PROJ-FILINGQUERY if true
Jest / Node testing -> PARTIAL-TCS-NODE-TESTING, PARTIAL-PROJ-NODE-TESTING
Machine Learning -> GHI-ML-MODEL, PROJ-FRAUDSIFT, PARTIAL-TCS-ML-SPEND-TRACKING
RAG / embeddings / vector search -> PROJ-FILINGQUERY, PROJ-EVALTRACE
LLM evaluation -> PROJ-EVALTRACE
AI-assisted development -> AI-ASSISTED-DEVELOPMENT-PROCESS
Codex / Cursor / Claude Code / MCP -> AI-ASSISTED-DEVELOPMENT-PROCESS
Chrome extension -> PROJ-JOBFILL
Tkinter / python-docx -> PROJ-RESUME-AGENT

## 8. TCS Evidence Cards

### ID: TCS-OWNERSHIP-LEADERSHIP
Proof: P1 HIGH
Best for: ownership, leadership, code reviews, mentoring, SDLC, Agile, stakeholder delivery, mid-level SWE
Facts: Guided 9-developer team over 2+ years; mentored 5 junior developers; supported stakeholder meetings, requirements, design decisions, development planning, documentation, QA support, and production delivery; used Rally for Agile tracking
Metrics: 9 developers, 5 juniors, 40+ production releases, 40+ deployments, 3+ appreciations
JD terms: ownership, leadership, code reviews, design reviews, mentoring, SDLC, Agile, production delivery, stakeholder communication
Limits: Do not claim engineering manager, people manager, product owner, or architect title
Allowed verbs: Led, Owned, Guided, Coordinated, Reviewed, Delivered, Shipped

### ID: TCS1-API-DATA
Proof: P1 HIGH
Best for: backend, REST APIs, Spring Boot, distributed systems, data consistency, Redis, SQL/NoSQL
Facts: Designed REST API contracts across 3 Java/Spring Boot applications; connected systems using relational and NoSQL databases; supported internal data transfer and consistency; rebuilt broken dependency-heavy application using Java 11 and Redis caching within 2 months
Metrics: 3 applications, 9 engineering teams, 2 months, independent deployments, data consistency
JD terms: REST APIs, Spring Boot, backend services, distributed systems, Redis, SQL, NoSQL, data consistency, system design
Limits: Do not claim public API platform or external developer API ownership unless DES confirms

### ID: TCS1-CICD
Proof: P1 HIGH
Best for: CI/CD, GitLab, Jenkins, Docker, Kubernetes, OpenShift, release automation, test gates
Facts: Standardized CI/CD pipelines across 7+ enterprise applications; configured GitLab/Jenkins workflows; integrated deployment automation and quality gates; supported production release flow
Metrics: 7+ applications, 40+ production releases, zero downtime
JD terms: CI/CD pipelines, GitLab CI/CD, Jenkins, Docker, Kubernetes, OpenShift, automated testing, deployment automation, release ownership
Limits: Do not claim full platform engineering ownership across entire enterprise

### ID: TCS-CICD-RUBY-GITLAB-AUTOMATION
Proof: P1 HIGH
Best for: Ruby, GitLab CI/CD, scripting, release automation, developer productivity
Facts: Created GitLab CI/CD pipelines from scratch for 10+ applications; used Ruby scripts for custom GitLab automation; reduced manual deployment work
Metrics: 10+ applications, 95% manual deployment reduction when using this specific story
JD terms: Ruby, GitLab, CI/CD, automation, scripting, developer productivity, internal tools
Limits: Use Ruby only when JD asks or when automation story is central

### ID: TCS1-LINUX-MIGRATION
Proof: P1 HIGH
Best for: Linux migration, AWS Linux, cloud operations, dependency debugging, zero downtime
Facts: Migrated 7+ applications from CentOS to Amazon Linux 2; supported AL2 to AL3 upgrade procedures; resolved package dependencies; collaborated with Amazon engineers on missing packages and migration blockers
Metrics: 7+ applications, zero downtime
JD terms: Linux, AWS, Amazon Linux, cloud migration, package dependencies, production migration, system administration
Limits: Do not claim cloud architecture ownership beyond migration and operations workflow

### ID: TCS2-SECURITY-IDENTITY
Proof: P1 HIGH
Best for: security-adjacent roles, IAM, OAuth, RBAC, auth recovery, access control, production incident response
Facts: Restored Microsoft SharePoint authentication after a production behavior change; built custom OAuth 2.0 authentication flow; implemented RBAC workflows across 10 applications; integrated internal APIs for access control across relational and non-relational systems
Metrics: 10,000+ users, 48 hours, 10 applications, 22% access-ticket reduction
JD terms: OAuth 2.0, authentication, authorization, RBAC, access control, production incident, API security, identity, SSO, JWT
Limits: Do not claim cybersecurity product experience, threat detection, or Zero Trust domain unless DES confirms

### ID: TCS2-JAVA-CONCURRENCY
Proof: P1 HIGH
Best for: Java, multithreading, concurrency, performance, file processing, SharePoint upload workflow
Facts: Designed Java multithreaded upload workflow for large 3D files; split uploads into concurrent parts; verified methods; deployed to production; integrated with Microsoft SharePoint
Metrics: 60s to 10s per file, 40–50 seconds saved, 83% reduction, 10,000+ users, 5-member team
JD terms: Java, concurrency, multithreading, performance optimization, file processing, distributed workflow, SharePoint
Limits: Do not claim storage-platform ownership beyond upload workflow

### ID: TCS2-FRONTEND
Proof: P1 HIGH
Best for: full-stack, frontend, enterprise dashboards, React, TypeScript, Angular, internal tools
Facts: Built or enhanced dashboard and UI workflows across connected enterprise applications; used React, TypeScript, JavaScript, Angular, HTML/CSS, Bootstrap; integrated UI workflows with APIs and role-based access
Metrics: multiple connected applications; use 10 applications only when tied to RBAC/auth/platform story
JD terms: React, TypeScript, JavaScript, Angular, HTML5, CSS3, dashboards, UI workflows, REST API integration, full-stack
Limits: Do not claim advanced WCAG/accessibility, frontend architecture, or design-system ownership unless DES confirms

### ID: TCS2-OBSERVABILITY
Proof: P1 HIGH
Best for: monitoring, debugging, production support, Datadog, CloudWatch, dashboards
Facts: Instrumented application performance and telemetry dashboards; integrated Datadog and CloudWatch views; monitored workflows, alerts, user requests, and data across connected applications; debugged multi-application issues
Metrics: 3 connected applications, incident diagnosis from hours to minutes
JD terms: Datadog, CloudWatch, observability, monitoring, production debugging, alerts, telemetry, incident triage
Limits: Do not claim SRE ownership unless JD and DES support it

### ID: TCS2-CLOUD-PLATFORM
Proof: P1 HIGH
Best for: cloud operations, AWS/Azure/GCP exposure, Docker, Kubernetes, Terraform, automation, infrastructure overhead reduction
Facts: Worked on cloud operations across enterprise applications; automated server cleanup and operational workflows; used Docker/Kubernetes for rebuild and deployment workflows; managed application environments before production
Metrics: 10 applications, 30% infrastructure overhead reduction when using the approved cloud-operations story
JD terms: AWS, Azure, GCP, Docker, Kubernetes, Terraform, cloud operations, infrastructure automation, environments
Limits: Do not mention dollar savings; do not claim cloud architect role

### ID: TCS-OPERATIONS-AUTOMATION
Proof: P1 HIGH
Best for: Python automation, server cleanup, health checks, operational dashboards, DevOps-adjacent roles
Facts: Created Python scripts and automation for server cleanup, system health checks, notifications, and dashboard-driven operations; reduced manual operational work across application environments
Metrics: 90% manual health-check reduction, 10+ applications, 30% team or operational performance improvement when directly tied to story
JD terms: Python, automation, Linux, operations, dashboards, health checks, developer productivity, scripting
Limits: Use as operations automation, not full platform ownership

### ID: TCS-DATABASES
Proof: P1 HIGH
Best for: SQL, Oracle, MySQL, Microsoft SQL Server, NoSQL, query optimization, backend data roles
Facts: Worked with Oracle, MySQL, Microsoft SQL Server, and NoSQL databases across enterprise systems; designed data movement and API consistency workflows; supported query and schema decisions
Metrics: use specific metrics only from TCS1-API-DATA or access-control stories
JD terms: SQL, Oracle, MySQL, Microsoft SQL Server, NoSQL, schema design, data consistency, query optimization
Limits: Do not claim DBA ownership unless DES confirms

### ID: TCS-SAST-QUALITY
Proof: P1 HIGH
Best for: secure coding, code quality, SAST, Black Duck, Polaris, dependency cleanup
Facts: Used Polaris and Black Duck SAST/security tools to identify vulnerabilities and improve code quality; upgraded vulnerable code across applications with Spring/Spring Security/React stack where relevant
Metrics: use 3 applications only when tied to vulnerability cleanup story
JD terms: SAST, secure coding, vulnerability remediation, code quality, dependency scanning, Spring Security
Limits: Do not claim security engineer title

### ID: TCS-CSHARP-DOTNET
Proof: P1 HIGH for professional use; MEDIUM for exact app scope
Best for: C#, .NET, Microsoft stack, enterprise apps, admin panels, custom UI, APIs
Facts: Used C# and .NET across TCS enterprise application work; built/enhanced admin panel and custom UI workflows; integrated UI with backend APIs
Metrics: 30% performance improvement only when using this story
JD terms: C#, .NET, Microsoft stack, enterprise applications, admin panel, backend APIs, custom UI
Limits: Do not claim .NET Core, ASP.NET MVC, WPF, WinForms, or Blazor unless DES confirms

### ID: TCS-UIUX
Proof: P1 MEDIUM
Best for: UI implementation, dashboards, Material UI, design-system implementation
Facts: Implemented UI workflows, dashboards, and Material UI-style components for enterprise applications
Metrics: use only if tied to frontend story
JD terms: Material UI, UI implementation, dashboards, component library, design system
Limits: Do not claim user research, product design, or accessibility ownership unless DES confirms

### ID: TCS-AUTH-STORAGE
Proof: P1 MEDIUM
Best for: SSO/OIDC, Okta, AWS S3, SharePoint, enterprise file/auth workflows
Facts: Worked with authentication and enterprise storage/file workflows including SharePoint and identity integrations
Metrics: use only with TCS2-SECURITY-IDENTITY or TCS2-JAVA-CONCURRENCY
JD terms: Okta, SSO, OIDC, SharePoint, AWS S3, enterprise authentication, file storage
Limits: Use Okta only when true/confirmed for specific role or DES

### ID: TCS-LOW-LEVEL-SYSTEMS
Proof: P1 LOW to MEDIUM
Best for: C/C++, memory/performance-adjacent, systems-adjacent roles
Facts: Has C/C++ exposure through coursework, TA, and performance/concurrency-adjacent work
Metrics: no standalone metric
JD terms: C, C++, systems programming, memory, performance
Limits: Do not claim kernel, compiler, embedded, or low-level production ownership unless DES confirms

### ID: TCS-AWARDS
Proof: P1 HIGH
Best for: quality recognition, client appreciation
Facts: Received 3+ client/HR appreciations for coding practice and delivery quality
Metrics: 3+ appreciations
JD terms: quality, delivery, recognition, ownership
Limits: Use only if space and JD values ownership/quality

## 9. Global Health Impact Evidence Cards

### ID: GHI-DASHBOARD
Proof: P1 HIGH
Best for: React, dashboards, research workflows, data visualization, U.S. internship, entry roles
Facts: Built React dashboard for disease, drug, country, and year workflows; created UI using React, HTML, CSS; enabled disease-wise exploration, graphs, world-map views, parameters, and drug selection
Metrics: 6 research teams, eliminated spreadsheet exports
JD terms: React, dashboard, frontend, data visualization, research tools, filters, UI workflows
Limits: Do not claim commercial SaaS production unless DES confirms

### ID: GHI-PIPELINE
Proof: P1 HIGH
Best for: Python, data pipelines, PostgreSQL, MongoDB, CSV/WHO data, health datasets
Facts: Processed CSV/WHO health records into PostgreSQL and MongoDB pipelines; extracted disease/drug data from files prepared by data team; supported dashboard and analytics workflows
Metrics: 10M+ weekly WHO health records, 90% manual data-prep reduction
JD terms: Python, data pipeline, PostgreSQL, MongoDB, CSV processing, ETL, healthcare data, WHO data
Limits: Do not claim full data science ownership beyond pipeline/model work described

### ID: GHI-API
Proof: P1 HIGH
Best for: API queries, reporting turnaround, health data backend
Facts: Supported API/query workflows for disease burden and country/drug reporting
Metrics: 150+ countries, hours to 30 seconds
JD terms: API, backend, reporting, health data, query workflows
Limits: Use only if JD asks data APIs or reporting workflows

### ID: GHI-ML-MODEL
Proof: P1 MEDIUM
Best for: AI/ML entry, predictive modeling, healthcare analytics, world-map predictions
Facts: Created machine learning models using GHI data to predict values and display country-wise results on world map
Metrics: no fixed model metric unless DES supplies it
JD terms: machine learning, predictive model, healthcare analytics, model training, data science
Limits: Need DES for algorithm names, accuracy, deployment status, or production ML claims

### ID: GHI-AI-ASSISTED-DEVELOPMENT
Proof: P1 MEDIUM / process proof
Best for: AI tooling, developer productivity, AI-assisted coding roles
Facts: Used AI-assisted coding tools during GHI/project development workflows; tools include Codex, Cursor, Claude Code, MCP, and agentic coding workflows when relevant
Metrics: no metric
JD terms: AI-assisted development, Codex, Cursor, Claude Code, MCP, agentic workflows, developer productivity
Limits: Do not write `vibe coding`; do not claim shipped AI product feature unless the project/evidence supports it

## 10. Teaching Assistant Evidence Cards

### ID: EDU-TA-CODE-REVIEW
Proof: P1 HIGH for teaching/code review; not SWE employment
Best for: entry, internship, Java, C++, SQL, OOP, code review, debugging, mentoring, communication
Facts: Teaching Assistant for Database Systems and Object-Oriented Programming; reviewed Java and C++ submissions; evaluated SQL/database projects; explained OOP, debugging, data structures, relational/NoSQL concepts, optimization, and concurrency
Metrics: 120+ students
JD terms: code review, debugging, Java, C++, SQL, OOP, database systems, mentoring, technical communication
Limits: Do not call this Software Engineer; do not use as production SWE proof; for mid roles usually omit or keep only if mentoring/code review is central
Allowed professional bullets:
- Reviewed Java and C++ submissions for 120+ students, identifying OOP, debugging, and data-structure issues before grading
- Evaluated SQL and database projects for query correctness, schema design, concurrency handling, and relational/NoSQL tradeoffs
- Guided SQL optimization and concurrency reviews across database projects, improving relational and non-relational design quality

## 11. Project Evidence Cards

### ID: PROJ-JOBPULSE
Proof: P2 HIGH
Best for: full-stack, backend, job data, React, TypeScript, Node.js, Kafka, PostgreSQL, Redis
Facts: Built job-posting ingestion and analysis project; normalized skill/company/location data; rendered dashboards for demand analysis
Metrics: 10,000+ job postings, 3 seconds to under 1 second if using dashboard/batch analysis story
Tech: Node.js, React, TypeScript, Kafka, PostgreSQL, Redis
JD terms: Node.js, React, TypeScript, Kafka, PostgreSQL, Redis, dashboards, data ingestion, job analytics
Limits: Project proof only; do not claim production users or ATS vendor integration

### ID: PROJ-FRAUDSIFT
Proof: P2 HIGH
Best for: fraud, anomaly detection, transactions, FastAPI, React, Docker, PostgreSQL, ML-adjacent roles
Facts: Built anomaly/risk detection project over transaction data; processed transactions and visualized suspicious activity in React dashboard
Metrics: 22,000+ transactions, 12 categories
Tech: React, FastAPI, Node.js, Docker, PostgreSQL
JD terms: fraud detection, anomaly detection, FastAPI, React, Docker, PostgreSQL, transaction analytics, real-time dashboard
Limits: Do not claim banking, payment network, or regulated finance production experience

### ID: PROJ-FILINGQUERY
Proof: P2 HIGH
Best for: RAG, document search, SEC filings, retrieval, FastAPI, PostgreSQL, vector search
Facts: Built document query project for SEC filings; supported retrieval/search over filings; useful for finance-document, RAG, and backend API roles
Metrics: 5,000+ SEC filings
Tech: Python, FastAPI, PostgreSQL, vector search/pgvector if true, RAG
JD terms: RAG, retrieval, embeddings, vector search, SEC filings, document search, FastAPI, PostgreSQL
Limits: Do not claim investment advice, trading system, or production finance platform

### ID: PROJ-EVALTRACE
Proof: P2 HIGH
Best for: LLM evaluation, RAG quality, hallucination reduction, eval harnesses, AI reliability
Facts: Built evaluation workflow for AI/RAG output quality; tracked hallucination reduction and evaluation traces
Metrics: hallucination rate from 23% to 4%
Tech: Python, evaluation workflows, LLM/RAG tooling
JD terms: LLM evaluation, hallucination reduction, RAG reliability, model evaluation, eval harness, AI quality
Limits: Do not claim formal MLOps platform unless DES confirms

### ID: PROJ-REVIEWBOT
Proof: P2 HIGH
Best for: developer tools, code review, GitHub Actions, AI-assisted review, automation
Facts: Built code-review automation project; useful for developer productivity, code-quality, and AI tooling roles
Metrics: no fixed metric unless DES supplies
Tech: GitHub Actions, automation, code review tooling, AI-assisted workflows if true
JD terms: code review, developer tools, GitHub Actions, automation, AI-assisted coding, CI quality
Limits: Do not claim enterprise deployment unless DES confirms

### ID: PROJ-RESUME-AGENT
Proof: P2 HIGH
Best for: AI tooling, LLM agents, desktop automation, resume workflow, JSON validation, DOCX/PDF generation
Facts: Built resume automation workflow that accepts JD input, generates grounded resume JSON, proposes DES candidates, optionally runs recruiter review, validates schema, creates DOCX/PDF outputs, archives generated resumes, and supports concurrent application workflows
Metrics: no external user metric
Tech: Python, Anthropic API, Tkinter, python-docx, JSON validation, agent workflow
JD terms: AI agents, LLM workflow, automation, Python, document generation, JSON validation, recruiter review, desktop tooling, developer productivity
Limits: Project proof only; do not claim commercial product or ATS integration unless DES confirms

### ID: PROJ-JOBFILL
Proof: P2 HIGH
Best for: Chrome extensions, browser automation, frontend tooling, Workday forms, AI-assisted application workflows
Facts: Built Chrome Manifest V3 extension that stores profile/resume data locally, parses resume data, scans job forms, supports Workday-style and generic autofill, and optionally uses Claude for custom application answers
Metrics: no external user metric
Tech: JavaScript, Chrome Manifest V3, HTML, CSS, local storage, Anthropic Claude
JD terms: Chrome extension, JavaScript, browser automation, Workday automation, form autofill, local storage, Claude, frontend tooling
Limits: Do not claim official Workday partnership, ATS access, or bypassing systems; phrase as form automation only

## 12. DES-Needed / Partial Evidence Cards
Use these only to generate DES candidates. Do not place directly in resume without user approval unless a stronger active evidence card already supports the claim.

### ID: PARTIAL-TCS-NODE-WORKFLOWS
Status: PARTIAL
Potential use: Node.js in TCS customer/product workflows
Known: User stated Node.js used in TCS to build products/workflows for customers
Need DES: exact application, backend/service/UI context, scope, outcome, testing/deployment status
Safe fallback: Skills only if JD asks Node.js and project evidence also supports Node.js

### ID: PARTIAL-TCS-TS-PRODUCTS
Status: PARTIAL to MEDIUM
Potential use: TypeScript in TCS enterprise product/customer workflows
Known: User stated TypeScript was used in TCS to build customer products
Need DES: exact dashboard/workflow, users/apps, whether React/Angular, outcome
Safe fallback: Use TCS2-FRONTEND for TypeScript dashboards if JD is full-stack

### ID: PARTIAL-TCS-PHP-WORK
Status: PARTIAL
Potential use: PHP roles or secondary skill
Known: User stated PHP was used
Need DES: exact system, app, dates, role, outcome
Safe fallback: Do not use unless JD asks PHP

### ID: PARTIAL-TCS-ML-SPEND-TRACKING
Status: PARTIAL
Potential use: AI/ML, spend tracking, analytics, forecasting
Known: User stated machine learning algorithms were used to track spends
Need DES: dataset, model type, target, evaluation, deployment, business/user outcome
Safe fallback: Create DES; do not place as production ML unless approved

### ID: PARTIAL-TCS-JUNIT-TESTING
Status: PARTIAL
Potential use: Java testing, unit testing, CI/CD gates
Known: User stated testing frameworks used in TCS
Need DES: JUnit version/type, unit vs integration, CI/CD use, app scope
Safe fallback: mention testing gates only through TCS1-CICD if supported

### ID: PARTIAL-GHI-PYTEST-TESTING
Status: PARTIAL
Potential use: Python testing, pytest, data/API validation
Known: User stated Pytest/testing used in GHI
Need DES: exact tests, pipeline/API coverage, CI/local, outcome
Safe fallback: Create DES before using Pytest in professional experience

### ID: PARTIAL-TCS-NODE-TESTING
Status: PARTIAL
Potential use: Node.js testing, Jest/Mocha/Vitest/Node test runner
Known: User stated Node.js testing used
Need DES: exact framework, system, scope, outcome
Safe fallback: Do not name framework unless confirmed

### ID: PARTIAL-GRAPHQL
Status: PARTIAL/CANNOT
Potential use: GraphQL roles
Known: Not currently supported by active evidence
Need DES: exact project/professional use
Safe fallback: Do not use unless user approves DES

### ID: PARTIAL-KAFKA-AIRFLOW-SPARK
Status: PARTIAL/PROJECT_ONLY depending JD
Potential use: data engineering, streaming, workflow orchestration
Known: Kafka supported in JobPulse project; Airflow/Spark not active professional proof unless DES confirms
Need DES: exact use, scale, system
Safe fallback: Use Kafka only in JobPulse project unless professional DES exists

### ID: AI-ASSISTED-DEVELOPMENT-PROCESS
Status: PROCESS_ONLY
Best for: AI tooling, developer productivity, coding assistants, agentic development workflows
Known: User uses Codex, Cursor, Claude Code, MCP, and agentic coding workflows across GHI and personal projects for code generation, refactoring, testing support, validation, and development acceleration
Use: Mention only for AI tooling/devtools roles or project/process proof; phrase as AI-assisted development workflow
Limits: Do not write `vibe coding`; do not claim shipped AI product feature, model ownership, or production AI platform unless another evidence card or DES supports it

### ID: PARTIAL-PROJ-NODE-TESTING
Status: PARTIAL
Potential use: Node.js testing in projects
Known: User stated Node.js testing/testing frameworks were used, but exact project framework and coverage are not fully locked
Need DES: exact project, framework such as Jest/Mocha/Vitest/Node test runner, test type, CI/local usage, and outcome
Safe fallback: Do not name a Node testing framework unless current-run DES confirms it

## 13. Forbidden Claims
Do not claim the following unless current-run DES explicitly confirms:
- direct cybersecurity product experience
- Zero Trust product ownership
- threat detection / incident response security analyst work
- formal SRE ownership
- formal architect title
- engineering manager or people-manager title
- product owner title
- accessibility/WCAG ownership
- design-system architecture ownership
- frontend performance metrics such as INP unless measured
- GraphQL production experience
- Temporal/Cadence/Airflow production ownership
- Spark/Flink production ownership
- Kubernetes platform ownership beyond deployment/operations workflow
- AWS/GCP/Azure architect role
- production ML model serving/MLOps unless confirmed
- fine-tuning or model training at production scale unless confirmed
- ATS bypassing or unauthorized automation
- official Workday/Ashby/Greenhouse integration
- commercial SaaS users for personal projects
- regulated fintech production work
- healthcare production product ownership beyond GHI research initiative
- dollar savings or financial product value in resume output

## 14. Bullet Construction Rules
Preferred formula:
Action verb + system/problem + technical method + scope/context + result

Google-style compression:
Accomplished X, measured by Y, by doing Z

STAR compression:
Situation/problem + action + result

Experience bullet target: 18 to 28 words
Project bullet target: 18 to 30 words
Summary target: 35 to 50 words
Skills row target: 6 to 10 terms

First 8 to 10 words should show:
verb + core system + JD stack

Avoid weak openings:
Worked on, helped, assisted, responsible for, participated in, contributed to, involved in, supported with, leveraged, utilized

Avoid AI-sounding filler:
robust, seamless, cutting-edge, innovative, impactful, transformative, mission-critical, world-class, best-in-class, next-generation, state-of-the-art

Use ownership verbs only with proof:
Led -> explicit team/scope
Owned -> end-to-end accountability
Guided -> junior developers/students/team
Reviewed -> code/design/review work
Coordinated -> cross-team/vendor delivery
Delivered/Shipped -> production release/outcome

## 15. Skill Section Rules
Technical Skills must be near top for cold apply.
Row 1 must mirror JD primary stack only.
Core JD skills must appear in Summary or Experience/Projects, not only in Technical Skills.
Do not use broad inventory.
Do not include unsupported tools.
At least 90% of skills must trace to evidence cards or approved DES.

Suggested row labels:
- Languages and Frameworks
- Backend and APIs
- Cloud, Data, and Infrastructure
- Quality, Observability, and Delivery
- AI, Automation, and Developer Tools when relevant

## 16. Project Selection Rules
Projects fill JD gaps only.
Do not overpower production experience for mid-level roles.
Project counts are controlled by Prompt.md Config and Layout Contract.
Story.md provides project evidence only.

Default project evidence guidance:
- `student_entry`: normally 3 projects
- `professional_entry`: normally 2 projects, 3 only when JD gaps require project proof
- `mid`: normally 2 projects
- `aiml_entry`: normally 3 projects, 4 only when AI/ML/LLM proof is mostly project-based
- `aitool_mid`: normally 2 projects
- `internship`: normally 3 projects

Do not use Story.md to override Prompt.md project count.
Do not reduce mid-level resumes to 1 project unless Prompt.md PROJECT COUNT EXCEPTION is explicitly approved.

Project routing:
Backend/full-stack/product -> JobPulse, Resume Agent, JobFill, FraudSift as relevant
Risk/fraud/transaction -> FraudSift
RAG/retrieval/document search -> FilingQuery
Developer tools/code review/agents -> ReviewBot, Resume Agent, JobFill
LLM evaluation/RAG reliability -> EvalTrace
AI workflow automation -> Resume Agent, JobFill

## 17. COMPRESSED RAW ARCHIVE — DO NOT USE DIRECTLY
This section preserves original context. Resume creator cannot use raw archive directly in bullets. If raw details are needed, create DES candidate.

Raw TCS leadership context:
Led/guided a 9-developer team over 2+ years, delivered 40+ production releases to US client Wabtec Corporation, created CI/CD pipelines in GitLab across 7+ applications, built dashboards with high usage across connected applications, used Oracle, MySQL, Microsoft databases, and NoSQL, handled SDLC/Agile delivery, code reviews, documentation, QA support, and received appreciations for coding practice and delivery quality.

Raw TCS 2021 context:
First major task involved fixing a broken application with old dependencies, upgrading to Java 11, improving architecture/distributed communication with other applications, and adding Redis caching. Work turned a broken application into production-ready code within about two months.

Raw TCS 2022 API/data context:
Handled 3 Java/Spring Boot applications. Designed REST APIs to transfer data internally between systems using NoSQL and MySQL. Goal was keeping changes reflected across applications instantly. Worked with distributed systems, AWS infrastructure, Redis, CI/CD, and Docker.

Raw TCS 2022 observability context:
Implemented Datadog monitoring and workflows to test configurations, monitor errors/alerts, debug multi-application issues, and create React dashboard views over Datadog, live user requests, and data.

Raw TCS migration context:
Upgraded servers for 7+ applications from CentOS to Amazon Linux 2. Increased security and created repeatable future-upgrade workflow that became standard practice in the unit. Later supported AL2 to AL3 work with Amazon engineers to resolve missing package/debug issues.

Raw TCS 2023 concurrency/auth context:
Handled 7+ applications with 5 junior developers. Designed multithreaded system to upload large 3D files into Microsoft SharePoint. Microsoft changed authentication process, causing production environment failure. Worked with Microsoft developers and delivered custom authentication within 2 days for existing and upcoming clients.

Raw TCS performance context:
Created concurrent multipart upload workflow for large files, verified methods, deployed production feature, saved 40 to 50 seconds per upload, improved one-file upload from about 1 minute to 10 seconds. Dollar value was discussed in raw story but must not appear in final resume.

Raw TCS quality/security context:
Used SAST tools Polaris and Black Duck for code quality/security. Identified vulnerabilities in existing codebase for applications. Upgraded stack in React, Spring, Java, implemented Spring Security, and cleaned code in measurable time.

Raw TCS 2024 RBAC context:
Built role-based access control across 10 applications, integrating internal APIs across relational and non-relational databases. Built, tested, deployed across multiple environments with QA and production release. Reduced user access request tickets by 22%.

Raw TCS operations context:
Used GitLab/CI/CD built by team, managed servers across applications, created dashboards, Python cleanup scripts, Docker/Kubernetes rebuild workflows, and periodic automated operational processes.

Raw GHI context:
Global Health Impact is a research initiative measuring how pharmaceutical drugs reduce disease burden for TB, malaria, HIV/AIDS, and neglected tropical diseases. Internship work involved a team of 6 developers, processing CSV/WHO health data, extracting disease/drug data, building React/HTML/CSS dashboards, world maps, parameter tuning, drug selection, and ML models for country-wise predictions.

Raw TA context:
TA for Database Systems and Object-Oriented Programming. Trained/reviewed students on database optimization, concurrency, relational/non-relational projects, OOP, C++, Java, debugging, code review, and 120+ students.

Raw skill hierarchy:
Must include when relevant: Java, Python, REST APIs, backend development, SQL/relational databases, cloud exposure, testing, CI/CD, GitLab/Git, debugging, impact numbers, collaboration/ownership.
Strongly recommended when proven: microservices, distributed systems, Docker, Linux, NoSQL, system design, monitoring/observability, performance optimization, code reviews, technical documentation, Agile/SDLC.
Optional role-specific: React, TypeScript, Node.js, Kubernetes, LLM/RAG/MLOps, GraphQL, AI-assisted tools, ETL/NiFi/Kafka/Spark/Airflow, C++/low-level systems.
