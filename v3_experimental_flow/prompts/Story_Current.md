# Story.md — Keval Shah Verified Story Bank

## TCS — Java, Spring Boot, Kafka, File Workflows, and Backend APIs

### Story 01 — Java File Ingestion and Status Platform
**Tech:** Java, Spring Boot, Kafka, SharePoint, REST APIs, SQL, NoSQL, OAuth 2.0, RBAC.

**Story:** At Tata Consultancy Services, Keval worked on a Java and Spring Boot file-ingestion and status platform for large 3D drawing workflows. The system handled 12K-14K daily 3D drawing uploads for 9K+ concurrent users across 4+ downstream services. Keval worked on ordered Kafka-backed processing, file-transfer status tracking, SharePoint-connected storage workflows, REST API actions, and access-controlled status updates so users and downstream systems could track the file lifecycle without repeated manual follow-up. The work cut transfer time from 60 seconds to 10 seconds, reduced failed uploads from 18% to 5%, supported 1.2K uploads/hour at peak, and handled files up to 500MB.

### Story 02 — File Workflow Reliability and Access Control
**Tech:** Java, Spring Boot, Kafka, OAuth 2.0, RBAC, retry logic, rollback workflows, SharePoint.

**Story:** Keval worked on a file workflow that depended on authorization, intake, storage, status tracking, notification, and downstream communication. He improved the workflow by adding retry handling, rollback behavior, OAuth 2.0 authentication, and RBAC controls around file actions and status changes. The workflow covered 6 dependent steps, reduced failure rate from 18% to 5%, and reduced related support tickets by 33%.

### Story 03 — Java Transaction-State APIs and Data Consistency
**Tech:** Java, Spring Boot, REST APIs, Kafka, JDBC, Hibernate, SQL, NoSQL, Oracle, MySQL, Microsoft SQL Server, Redis.

**Story:** Keval coordinated transaction-state API work across 3 Java and Spring Boot applications and 9 engineering teams. The work connected SQL and NoSQL workflows, protected 27K daily transactions, kept p95 API response time under 100ms, and reduced manual reconciliation by 18%. Keval worked on API contracts, data-state transitions, database communication, reconciliation logic, and backend consistency so teams could rely on the same transaction status across connected applications.

### Story 04 — Legacy Java Recovery and Modernization
**Tech:** Java 8, Java 11, Spring Boot, Redis, REST APIs, SQL, dependency remediation.

**Story:** Keval recovered a dependency-blocked Java service that could not move forward because old dependencies and integration conflicts were preventing production readiness. He upgraded the service from Java 8 to Java 11, resolved dependency conflicts, repaired integration behavior, and added Redis caching. The recovery was completed within 2 months. API response time improved 17%, and the Redis-backed cache reached an 83% hit rate.

### Story 05 — Java Testing, CI/CD, UAT, and Release Delivery
**Tech:** Java, Spring Boot, GitLab, Jenkins, JUnit, Mockito, Pytest, UAT, A/B testing, CI/CD, rollback workflows.

**Story:** Keval standardized release workflows across 7+ applications and 45+ production releases. The CI/CD path used GitLab and Jenkins, ran 150+ validation tests per release, supported unit testing and UAT, and included rollback-ready deployment behavior. Java stories used JUnit and Mockito for test coverage, Python workflows used Pytest where applicable, and UI or workflow changes were validated through UAT and A/B testing when the user story required comparison. Deployment time fell from 2 hours to 5 minutes, releases completed with zero downtime, and rollback could be triggered with 1 click.

## TCS — Deployment Automation, Cloud, Linux, and Operations

### Story 06 — Multi-Server Deployment Automation and Rollback
**Tech:** Ruby, GitLab CI/CD, Docker, Kubernetes, Linux, Bash, deployment automation, rollback workflows.

**Story:** Keval automated multi-server releases for 10+ applications using Ruby-backed GitLab workflows. The automation replaced manual deployment steps with repeatable validation, environment setup, deployment, and rollback behavior. Manual deployment work was reduced by 95%. Environment spin-up improved from days to under 5 minutes, and rollback time fell to 5 minutes, helping teams replicate changes quickly across multiple servers.

### Story 07 — Linux Migration and Cloud Operations
**Tech:** Linux, CentOS, Amazon Linux, AWS, GCP, Docker, Kubernetes, Terraform, Bash, package remediation.

**Story:** Keval migrated 7+ applications from CentOS to Amazon Linux with zero downtime. He resolved 25+ package blockers, repaired environment-readiness issues, validated application behavior after migration, and documented 12 reusable upgrade steps. Environment-readiness checks improved from 4 hours to 30 minutes. Across TCS work, server setup and cloud environment support used AWS or GCP depending on stakeholder license and deployment target, with Docker images and CI/CD pipelines used to replicate application changes across servers.

### Story 08 — Cross-Application Task Orchestration
**Tech:** Python, Django, FastAPI, REST APIs, SQL, NoSQL, Kafka, retry logic, rollback workflows.

**Story:** Keval coordinated task requests across 5 dependent applications using Python, Django, and FastAPI workflows. The orchestration handled validation, routing, status checks, retry behavior, and communication between applications. The workflow processed 500+ weekly task requests, reduced manual handoffs by 35%, and cut validation time from 20 minutes to 5 minutes.

### Story 09 — Python Validation, Deployment, and Production Monitoring
**Tech:** Python, FastAPI, Pytest, SQL, monitoring dashboards, deployment validation.

**Story:** Keval worked on Python validation and monitoring workflows that screened 10K+ weekly records before downstream processing. The validation flow helped teams identify incorrect records, deployment issues, and data mistakes before they affected dependent systems. Invalid-record incidents fell 25%, and diagnosis time improved from 2 hours to 10 minutes because the monitoring workflow surfaced what failed, where it failed, and what needed correction.

### Story 10 — Python Operations Automation and Environment Readiness
**Tech:** Python, Linux, dashboards, Docker, Kubernetes, health checks, operational automation.

**Story:** Keval automated health checks and operational readiness workflows across 10+ applications using Python, Linux, and dashboards. The automation covered 4 environments and replaced repetitive manual review work. Daily checks improved from 3 hours to 18 minutes, manual review dropped 90%, and teams could detect environment-readiness problems earlier before release or stakeholder validation.

## TCS — C#, .NET, Databases, Frontend, Identity, and Security

### Story 11 — C#/.NET Enterprise Portal Architecture
**Tech:** C#, .NET, ASP.NET Core, Web API, Entity Framework, SQL, Microsoft SQL Server, Oracle, MySQL.

**Story:** Keval worked on C# and .NET portal APIs, service logic, and SQL data-access workflows supporting 4+ business workflows. He improved API and SQL data-access performance by 30% through service-layer and database-query improvements. p95 response time fell from 600ms to 300ms, and the portal supported 800+ internal users.

### Story 12 — Portal Access Control and Controlled Deployment
**Tech:** C#, .NET, OAuth, RBAC, Azure Key Vault, controlled configuration, CI/CD.

**Story:** Keval secured portal release behavior through OAuth, RBAC, and controlled configuration workflows. The system protected 12 roles, centralized 20+ secrets, and reduced access-related failures by 25%. The work connected access control with controlled deployment so releases could protect role-specific behavior and configuration-sensitive workflows.

### Story 13 — React File Workflow Dashboard
**Tech:** React, TypeScript, JavaScript, HTML, CSS, REST APIs, SharePoint, frontend validation.

**Story:** Keval delivered React and TypeScript file-status views for file submission, alerts, notifications, and REST API actions. The dashboard supported 800+ users, cut status-check time from 10 minutes to 2 minutes, and reduced invalid submissions by 30%. The frontend connected users to file workflow status, validation behavior, role-based actions, and backend APIs so support teams and users could see transfer progress without manual lookups.

### Story 14 — Angular Operations and Ticket Dashboard
**Tech:** Angular, TypeScript, JavaScript, HTML, CSS, REST APIs, SQL, dashboard workflows.

**Story:** Keval built Angular dashboard workflows that combined ticket, application, alert, payment, and notification data. The dashboard supported 6+ operational workflows, combined 3 data sources, and reduced status lookup from 15 minutes to 3 minutes. The story shows frontend and operations work where the UI connected multiple backend sources into 1 view for faster triage.

### Story 15 — Transfer Workflow and Operational Visibility
**Tech:** Java, Spring Boot, React, TypeScript, REST APIs, notifications, monitoring, bulk actions.

**Story:** Keval worked on high-volume transfer visibility across status tracking, bulk actions, notifications, and monitoring. The workflow handled 5K+ weekly transfer requests, cut support lookup time from 12 minutes to 4 minutes, and reduced manual follow-ups by 30%. The system helped users, support teams, and downstream workflows understand transfer state without manually checking multiple systems.

### Story 16 — SharePoint Authentication Recovery
**Tech:** Java, Spring Boot, Spring Security, OAuth 2.0, SharePoint, TLS, JWT, access-control debugging.

**Story:** Keval restored SharePoint authentication for 10K+ users within 48 hours after a production behavior change disrupted access. He diagnosed the authentication failure, repaired OAuth 2.0 and Spring Security behavior, validated token handling, and restored access across 3 affected applications. Access-support tickets fell 22%, and token failure rate improved from 14% to 2%.

### Story 17 — Enterprise RBAC and Access Governance
**Tech:** OAuth 2.0, RBAC, Spring Security, Java, access-control workflows, role governance.

**Story:** Keval implemented OAuth 2.0 and RBAC workflows across connected applications. The access-control work covered 12 roles, 3 applications, and 10K+ users. Manual access changes were reduced 30% because role-based behavior became more consistent across applications, making access workflows easier to validate and maintain.

### Story 18 — Certificate and Dependency Remediation
**Tech:** Java, Spring Security, React, TLS/SSL, dependency remediation, SAST, release validation.

**Story:** Keval remediated certificate and dependency risks across Java, Spring Security, and React release paths. He closed 40+ findings, renewed 12 certificates, and reduced security-blocked releases by 50%. The work helped release teams avoid blocked deployments caused by expired certificates, vulnerable dependencies, and failed security validation.

### Story 19 — Observability and Production Debugging
**Tech:** Datadog, CloudWatch, React, TypeScript, JavaScript, APIs, logs, alerts, monitoring dashboards.

**Story:** Keval instrumented Datadog and CloudWatch telemetry across 3 connected applications. He consolidated 8 alert sources, monitored 25 monthly incidents, and cut MTTR from 2 hours to 20 minutes. The observability dashboards helped teams diagnose API traffic, live requests, alerts, and production issues in minutes instead of hours.

### Story 20 — Technical Leadership, Mentoring, and Delivery Discipline
**Tech:** Git, GitLab, Rally, code reviews, design reviews, SDLC, Agile, CI/CD, UAT, documentation.

**Story:** Keval guided a 9-developer team, mentored 5 juniors, supported 40+ production releases, and earned 3+ client or HR appreciations. He used Rally to track user stories, team progress, stakeholder visibility, and delivery status. For assigned user stories, he communicated with stakeholders, gathered requirements, planned application design, designed workflow and schema changes, selected the tech stack with the team, coordinated implementation, reviewed code, supported QA, completed UAT approval, and helped deploy releases. Review rework dropped 30%, onboarding improved from 4 weeks to 2 weeks, and TCS user stories targeted 90% test coverage.

## TCS — Database, Full-Stack, and Engineering Foundation Stories

### Story 21 — Cross-Database Design and Query Improvement
**Tech:** Oracle, MongoDB, MySQL, PostgreSQL, Microsoft SQL Server, SQL, NoSQL, database design, query optimization.

**Story:** Across TCS work, Keval used Oracle, MongoDB, MySQL, PostgreSQL, and Microsoft SQL Server across backend, portal, reporting, and workflow systems. He worked on database design, schema design, SQL and NoSQL data flows, query behavior, and application-level data access. Query results improved by 30% through database design and query improvements. At Global Health Impact, he also used MongoDB and PostgreSQL for health-data pipelines and research-query workflows.

### Story 22 — Full-Stack Frameworks and Tested User Stories
**Tech:** Hibernate, JDBC, Spring MVC, jQuery, JavaScript, TypeScript, Angular, Node.js, Next.js, React.js, HTML, CSS, JUnit, Mockito, Pytest.

**Story:** Across TCS user stories, Keval used Hibernate, JDBC, Spring MVC, jQuery, JavaScript, TypeScript, Angular, Node.js, Next.js, React.js, HTML, and CSS across backend, frontend, and full-stack work. Java user stories used Mockito and JUnit, Python workflows used Pytest, and work was tested through test cases before release. HTML and CSS were also used across TCS, GHI, and personal projects wherever user-facing dashboards, forms, or web workflows were required.

### Story 23 — Git, Rally, Ownership, UAT, A/B Testing, and Cloud Release Ownership
**Tech:** Git, GitLab, Rally, UAT, A/B testing, unit testing, AWS, GCP, Docker, Kubernetes, CI/CD.

**Story:** Across TCS, GHI, and projects, Keval used Git for version control, and at TCS he used GitLab and Rally for user-story tracking, team progress, and stakeholder visibility. TCS user stories followed an ownership cycle: stakeholder communication, information gathering, application design, workflow design, schema design, technology planning, team coordination, implementation, test coverage, UAT approval, and deployment. The standard delivery path included unit testing, UAT, A/B testing where applicable, 90% test coverage targets, server setup on AWS or GCP depending on stakeholder license, Docker image creation, and CI/CD pipelines that deployed code through Kubernetes to replicate changes across servers.

## Global Health Impact — Data, APIs, Dashboards, and AI/ML

### Story 24 — Health-Data Pipeline
**Tech:** Python, CSV, Excel, PostgreSQL, MongoDB, data ingestion, data validation.

**Story:** At Global Health Impact, Keval processed 10M+ weekly WHO records from CSV and Excel into PostgreSQL and MongoDB. The pipeline reduced manual data preparation by 90%, cut ingestion runtime from 6 hours to 45 minutes, and reduced invalid records by 35%. The work made health data easier for research teams to query by disease, drug, country, and year.

### Story 25 — Health-Data APIs and Research Queries
**Tech:** Python, AWS, REST APIs, PostgreSQL, MongoDB, disease queries, country queries.

**Story:** Keval supported disease, drug, country, and year queries across 150+ countries through API-backed research workflows. Reporting turnaround improved from hours to 30 seconds. The API workflow handled 2K+ research queries per week with p95 latency under 1 second, helping researchers run analysis without waiting for spreadsheet exports or manual data preparation.

### Story 26 — Research Dashboard and Visualization
**Tech:** React, JavaScript, HTML, CSS, data visualization, maps, graphs, REST APIs.

**Story:** Keval delivered React dashboards for 6 research teams, replacing spreadsheet exports with interactive workflows for disease, drug, country, year, graph, and map analysis. Dashboard load time improved from 8 seconds to 2 seconds. The dashboard helped research teams explore data visually and connect frontend filters to API-backed analysis.

### Story 27 — Machine Learning and Prediction Integration
**Tech:** Python, machine learning, feature engineering, model evaluation, inference, health-data prediction workflows.

**Story:** Keval worked on country-level prediction workflows over health data. The work involved data preparation, feature engineering, model evaluation, and inference integration around health datasets. The model workflow used an 80/20 split, tracked F1, AUC, or RMSE depending on the task, and targeted inference latency around 500ms.

### Story 28 — Research Stakeholder Delivery
**Tech:** Python, REST APIs, React, PostgreSQL, MongoDB, dashboard delivery, visualization workflows.

**Story:** Keval translated researcher requirements into data, API, dashboard, visualization, and prediction tasks. He supported 6 teams, delivered 10+ scoped changes, and reduced clarification cycles by 50%. The story shows stakeholder-facing engineering work where requirements became usable software workflows for research teams.

## Binghamton University — Teaching Assistant, Code Review, and Automation

### Story 29 — TA Code Review and Review Automation
**Tech:** Python, Java, C++, SQL, databases, OOP, data structures, system design, code review.

**Story:** As a Teaching Assistant for Databases and Object-Oriented Programming at Binghamton University, Keval reviewed Java, C++, SQL, and database coursework for 120+ students. He automated 12 Python review checks, reduced review time from 15 minutes to 1 minute per submission, and reviewed 1K+ submissions per semester. During labs, he reviewed code, improved students' system-design and data-structure logic, and conducted sessions on writing clean code.

## Projects — Product, AI, RAG, Evaluation, and Automation

### Story 30 — JobPulse
**Tech:** React, Kafka, PostgreSQL, Redis, JavaScript, backend ingestion, dashboard analytics.

**Story:** Keval self-tested JobPulse with 10K+ public job postings. The project used React, Kafka, PostgreSQL, and Redis to support job ingestion, search, and dashboard analysis. Dashboard and batch-analysis time improved from 3 seconds to under 1 second. The indexing rate reached 2K postings/min, and search p95 latency was 300ms.

### Story 31 — FraudSift
**Tech:** FastAPI, React, Docker, PostgreSQL, Python, anomaly detection, machine learning.

**Story:** Keval self-tested FraudSift on 22K+ public or sample transactions across 12 categories. The project used FastAPI, React, Docker, and PostgreSQL for transaction analysis and anomaly detection. The self-tested model reached 0.86 precision, 0.81 recall, 0.83 F1, and p95 inference latency of 120ms.

### Story 32 — FilingQuery
**Tech:** Python, FastAPI, PostgreSQL, embeddings, vector search, RAG, citation-grounded retrieval.

**Story:** Keval self-built FilingQuery as citation-grounded retrieval over 5K+ public SEC filings. The project used Python, FastAPI, PostgreSQL, embeddings, and vector search to return source-linked answers from filing documents. Self-tested p95 query latency was 1.8 seconds, and citation accuracy reached 92%.

### Story 33 — EvalTrace
**Tech:** Python, RAG evaluation, LLM evaluation, GitHub Actions, CI quality gates, schema validation.

**Story:** Keval self-tested EvalTrace as a RAG evaluation and CI quality-gate workflow. The evaluation reduced hallucination from 23% to 4% on a 200-prompt evaluation set. CI evaluation runtime was 4 minutes, the project compared 3 model or prompt variants, and schema-pass rate reached 95%.

### Story 34 — ReviewBot
**Tech:** AI-assisted code review, GitHub Actions, architecture checks, security checks, style checks, test-quality checks.

**Story:** Keval self-built ReviewBot to support AI-assisted pull-request review across architecture, security, style, and test-quality checks. The project was tested on 50 PRs, reduced manual review time by 30%, and surfaced 80% of seeded issues. The project focused on developer-tooling work around code review automation, architecture checks, security checks, style checks, and test-quality checks.

### Story 35 — Resume Agent
**Tech:** Python, JSON, DOCX, PDF generation, schema validation, JD parsing, evidence-grounded generation.

**Story:** Keval built Resume Agent to generate evidence-grounded resume JSON, DOCX, and PDF outputs from job descriptions. The project was tested on 100 JDs, reduced tailoring time from 45 minutes to 8 minutes, and achieved a 98% schema-validation pass rate. The workflow focused on structured resume generation grounded in verified stories rather than generic keyword stuffing.

### Story 36 — JobFill AI
**Tech:** Chrome Manifest V3, JavaScript, form automation, local storage, Workday-style forms.

**Story:** Keval built JobFill AI as a Chrome MV3 application autofill tool for generic and Workday-style forms. The project was tested on 40 forms, achieved 85% field-detection success, and reduced repeated entry time from 12 minutes to 3 minutes per application. The project focused on form automation, browser-extension behavior, local storage, and Workday-style form patterns.

### Story 37 — Bistro AI
**Tech:** AI workflow automation, structured JSON actions, validated cart actions, retries, timeouts, invalid-request handling.

**Story:** Keval built Bistro AI as a structured AI ordering workflow with validated cart actions, menu constraints, retries, timeouts, and invalid-request handling. The project was tested on 150 orders, reached 96% valid JSON/action success, and kept p95 response time under 1.2 seconds.

### Story 38 — AI-Assisted Engineering Workflow
**Tech:** Codex, Cursor, Claude Code, AI-assisted development, testing support, debugging, refactoring.

**Story:** Keval used Codex, Cursor, and Claude Code to support implementation while retaining final design, testing, debugging, and delivery ownership. The workflow reduced personal prototype build time by 40% across 5 projects. The workflow focused on AI-assisted engineering process, developer productivity, implementation support, testing support, debugging, and refactoring.
