# Story.md — Keval Shah Experience and Project Story Bank

All facts and numbers in this file are approved for resume use.

---

# Tata Consultancy Services — Software Engineer II

## TCS-II-01 — High-Throughput File Ingestion, Concurrency, and Reliability

### Engineering story

Keval led development of a Java and Spring Boot file-ingestion and status platform for large 3D drawing workflows. The platform used concurrent multipart uploads, Kafka-backed ordered processing, SharePoint-connected storage, REST APIs, SQL/NoSQL data flows, OAuth 2.0, and RBAC to manage authorization, intake, storage, status, notification, and downstream communication.

The system handled 12,000–14,000 daily uploads for 9,000+ concurrent users across 4+ downstream services. It sustained 1,200 uploads per hour and files up to 500MB. The redesign reduced transfer latency from 60 seconds to 10 seconds, lowered failed uploads from 18% to 5%, and reduced related support tickets by 33%.

### FAANG framing dimensions

- System: distributed file-ingestion and lifecycle platform
- Scale: 12,000–14,000 daily uploads; 9,000+ concurrent users; 4+ downstream services
- Throughput: 1,200 uploads/hour
- Data size: files up to 500MB
- Performance: 60 seconds to 10 seconds; 83% latency reduction
- Reliability: failure rate from 18% to 5%; support tickets down 33%
- Mechanism: Java concurrency, multipart processing, Kafka ordering, retry, rollback, OAuth 2.0, RBAC, REST APIs

### Resume keywords

Java, Spring Boot, concurrency, multithreading, Kafka, REST APIs, distributed systems, high throughput, low latency, performance optimization, scalability, retry, rollback, fault tolerance, SharePoint, OAuth 2.0, RBAC, SQL, NoSQL, file processing.

---

## TCS-II-02 — SharePoint Authentication Recovery and Reusable Identity Integration

### Engineering story

A Microsoft authentication behavior change disrupted a live SharePoint workflow. Keval traced the failure across application and API layers, coordinated with Microsoft and internal engineering teams, and implemented an OAuth 2.0 and Spring Security recovery path. The solution restored access for 10,000+ users within 48 hours across 3 affected applications.

The reusable authentication flow reduced access-support tickets by 22% and improved token failure rate from 14% to 2%. The work included production triage, root-cause analysis, implementation, lower-environment testing, UAT, release coordination, and production validation.

### FAANG framing dimensions

- Incident: external authentication change broke a production workflow
- Scale: 10,000+ users; 3 affected applications
- Recovery: restored within 48 hours
- Reliability: token failure rate from 14% to 2%
- User impact: access-support tickets down 22%
- Ownership: diagnosis through production recovery

### Resume keywords

OAuth 2.0, Spring Security, authentication, authorization, SharePoint APIs, production incident, root-cause analysis, debugging, identity integration, API security, UAT, cross-functional collaboration, operational excellence.

---

## TCS-II-03 — Enterprise RBAC and Access Governance

### Engineering story

Keval implemented OAuth 2.0 and RBAC workflows across 3 connected applications, integrating role behavior with relational and non-relational data stores. The system governed 12 roles for 10,000+ users and synchronized access behavior across application workflows.

The implementation reduced manual access changes by 30% and made role-based actions more consistent across applications. Work covered access-model design, API integration, testing across environments, UAT, deployment, and production support.

### FAANG framing dimensions

- System: distributed application access-control workflow
- Scale: 12 roles; 3 applications; 10,000+ users
- Impact: manual access changes down 30%
- Mechanism: OAuth 2.0, RBAC, Spring Security, APIs, SQL/NoSQL integration

### Resume keywords

RBAC, OAuth 2.0, authentication, authorization, access control, identity, Spring Security, API integration, relational databases, NoSQL, security, governance, distributed workflows.

---

## TCS-II-04 — Multi-Server Release Automation and Rollback

### Engineering story

Keval built Ruby-backed GitLab CI/CD workflows for 10+ applications, replacing manual multi-server release steps with repeatable validation, environment setup, deployment, and rollback stages. The automation reduced manual deployment work by 95%, cut environment spin-up from days to under 5 minutes, and reduced rollback time to 5 minutes.

The workflow used GitLab, Ruby, Git, Linux, Bash, Docker, and Kubernetes to replicate changes consistently across environments and servers.

### FAANG framing dimensions

- System: multi-application release platform
- Scope: 10+ applications
- Developer productivity: manual deployment work down 95%
- Provisioning: days to under 5 minutes
- Recovery: 5-minute rollback
- Mechanism: Ruby automation, GitLab CI/CD, Docker, Kubernetes, Linux

### Resume keywords

GitLab CI/CD, Ruby, deployment automation, release engineering, developer productivity, Docker, Kubernetes, Linux, Bash, rollback, environment provisioning, infrastructure automation.

---

## TCS-II-05 — Cross-Application Task Orchestration and Validation

### Engineering story

Keval coordinated dependent requests across 5 applications using Python, Django, FastAPI, REST APIs, SQL/NoSQL data sources, validation layers, queues, and retry/rollback behavior. The workflow processed 500+ task requests per week, reduced manual handoffs by 35%, and cut validation time from 20 minutes to 5 minutes.

A related FastAPI validation and monitoring path screened 10,000+ weekly records, reduced invalid-record incidents by 25%, and improved diagnosis time from 2 hours to 10 minutes by surfacing what failed and where correction was required.

### FAANG framing dimensions

- System: dependency-aware orchestration and validation platform
- Scope: 5 dependent applications; 500+ weekly tasks; 10,000+ weekly records
- Workflow efficiency: manual handoffs down 35%; validation 20 minutes to 5 minutes
- Reliability: invalid-record incidents down 25%
- Diagnosability: 2 hours to 10 minutes

### Resume keywords

Python, Django, FastAPI, REST APIs, distributed systems, orchestration, asynchronous processing, queues, retry, rollback, data validation, SQL, NoSQL, production monitoring, debugging.

---

## TCS-II-06 — Operations Automation and Environment Readiness

### Engineering story

Keval automated system-health checks, server cleanup, notifications, and environment-readiness workflows across 10+ applications using Python, Linux, Docker, Kubernetes, and operational dashboards. The automation covered 4 environments, reduced daily checks from 3 hours to 18 minutes, and lowered manual review by 90%.

The workflow surfaced readiness problems before release and stakeholder validation, improving repeatability across non-production and production delivery paths.

### FAANG framing dimensions

- Scope: 10+ applications; 4 environments
- Operational efficiency: 3 hours to 18 minutes
- Automation: manual review down 90%
- Mechanism: Python, Linux, dashboards, Docker, Kubernetes, notifications

### Resume keywords

Python automation, Linux, health checks, environment readiness, operational tooling, Docker, Kubernetes, monitoring, notifications, production support, developer productivity.

---

## TCS-II-07 — React File-Workflow Dashboard

### Engineering story

Keval delivered React and TypeScript views for file submission, validation, alerts, notifications, status tracking, and REST API actions. The dashboard connected users to the underlying file-ingestion lifecycle and role-based workflows without requiring manual status checks across systems.

The interface supported 800+ users, reduced status-check time from 10 minutes to 2 minutes, and lowered invalid submissions by 30% through frontend validation and clearer workflow state.

### FAANG framing dimensions

- Product surface: API-driven workflow dashboard
- Scale: 800+ users
- User efficiency: status checks 10 minutes to 2 minutes
- Data quality: invalid submissions down 30%
- Mechanism: React, TypeScript, REST APIs, validation, OAuth/RBAC

### Resume keywords

React, TypeScript, JavaScript, HTML, CSS, REST API integration, frontend validation, dashboards, asynchronous workflows, role-based UI, user experience, full-stack development.

---

## TCS-II-08 — Angular Operations and Ticket Dashboard

### Engineering story

Keval built Angular and TypeScript dashboard workflows that combined ticket, application, alert, payment-status, and notification data into a single operational view. The dashboard supported 6+ workflows across 3 data sources and reduced status lookup from 15 minutes to 3 minutes.

The system improved triage by connecting frontend views to APIs, monitoring signals, authentication controls, and dependent application data.

### FAANG framing dimensions

- Product surface: consolidated operations dashboard
- Scope: 6+ workflows; 3 data sources
- User efficiency: status lookup 15 minutes to 3 minutes
- Mechanism: Angular, TypeScript, APIs, monitoring, RBAC

### Resume keywords

Angular, TypeScript, JavaScript, HTML, CSS, dashboards, API integration, operational tooling, data integration, monitoring, authentication, full-stack engineering.

---

## TCS-II-09 — Transfer Visibility and Operational Self-Service

### Engineering story

Keval implemented transfer-state visibility across status tracking, bulk actions, notifications, and monitoring workflows. The system handled 5,000+ weekly transfer requests, reduced support lookup from 12 minutes to 4 minutes, and lowered manual follow-ups by 30%.

The work made transfer state visible to users, support teams, and downstream services without requiring repeated checks across multiple systems.

### FAANG framing dimensions

- Scale: 5,000+ weekly transfer requests
- User efficiency: lookup 12 minutes to 4 minutes
- Operational impact: manual follow-ups down 30%
- System: status, bulk-action, notification, and monitoring workflow

### Resume keywords

workflow visibility, high-volume requests, bulk operations, notifications, monitoring, operational self-service, REST APIs, production support, user workflows.

---

## TCS-II-10 — Observability and Production Debugging

### Engineering story

Keval instrumented Datadog and CloudWatch telemetry across 3 connected applications and built dashboard views for API traffic, user requests, alerts, logs, and application health. The observability workflow consolidated 8 alert sources and monitored 25 incidents per month.

The system reduced mean time to resolution from 2 hours to 20 minutes and changed incident diagnosis from an hours-long multi-system investigation into a guided telemetry workflow.

### FAANG framing dimensions

- Scope: 3 connected applications; 8 alert sources; 25 monthly incidents
- Reliability: MTTR 2 hours to 20 minutes
- Mechanism: Datadog, CloudWatch, logs, metrics, alerts, dashboards
- Ownership: instrumentation, production triage, and debugging

### Resume keywords

Datadog, CloudWatch, observability, monitoring, telemetry, alerting, logs, metrics, MTTR, incident triage, production debugging, operational excellence.

---

## TCS-II-11 — Certificate and Dependency Remediation

### Engineering story

Keval remediated certificate, dependency, and code-quality risks across Java, Spring Security, and React release paths. He used SAST and dependency-scanning tools including Polaris and Black Duck, closed 40+ findings, renewed 12 certificates, and reduced security-blocked releases by 50%.

He also created a repeatable Python-based certificate-update workflow so application teams could rotate certificates with less manual rework.

### FAANG framing dimensions

- Scope: 40+ findings; 12 certificates
- Release impact: security-blocked releases down 50%
- Mechanism: SAST, dependency scanning, TLS/SSL, Python automation
- Quality: repeatable remediation before deployment

### Resume keywords

SAST, Polaris, Black Duck, dependency remediation, TLS/SSL, certificate rotation, secure coding, Spring Security, React, Python automation, code quality, release validation.

---

## TCS-II-12 — C#/.NET Enterprise Portal Performance

### Engineering story

Keval developed and improved C#/.NET portal APIs, service logic, SQL data-access paths, admin workflows, and custom UI behavior across 4+ business workflows. Service-layer and query improvements increased performance by 30%, reduced p95 response time from 600ms to 300ms, and supported 800+ internal users.

The portal used C#, .NET, ASP.NET Core, Web API, Entity Framework, SQL Server, Oracle, MySQL, OAuth, RBAC, Azure, HTML, and CSS.

### FAANG framing dimensions

- Scope: 4+ business workflows; 800+ users
- Performance: 30% improvement; p95 600ms to 300ms
- Mechanism: C#/.NET services, APIs, SQL query/data-access optimization
- Product: centralized enterprise workflow portal

### Resume keywords

C#, .NET, ASP.NET Core, Web API, REST APIs, Entity Framework, SQL Server, Oracle, MySQL, Azure, API performance, p95 latency, enterprise applications, OOP.

---

## TCS-II-13 — Portal Access Control and Configuration Security

### Engineering story

Keval secured portal release behavior with OAuth, RBAC, and controlled configuration management. The implementation governed 12 roles, centralized 20+ secrets through Azure Key Vault, and reduced access-related failures by 25%.

The work connected identity, configuration, and deployment controls so role-sensitive functionality remained consistent across environments.

### FAANG framing dimensions

- Scope: 12 roles; 20+ secrets
- Reliability: access-related failures down 25%
- Mechanism: OAuth, RBAC, Azure Key Vault, configuration controls, CI/CD

### Resume keywords

OAuth, RBAC, Azure Key Vault, secrets management, access control, configuration management, C#, .NET, CI/CD, enterprise security.

---

## TCS-II-14 — Technical Leadership and Full Development Cycle

### Engineering story

Keval guided a 9-developer team, mentored 5 junior engineers, supported 45+ production releases, and received 3+ client or HR appreciations for coding practice and delivery quality. He used Rally to manage user stories, progress, stakeholder visibility, and delivery status.

For assigned user stories, he participated across the full development cycle: stakeholder communication, requirements gathering, technical and application design, workflow and schema design, technology selection, team planning, implementation, code review, unit and integration testing, QA, UAT, deployment, rollback planning, and production validation. The delivery process targeted 90% test coverage, reduced review rework by 30%, and improved onboarding from 4 weeks to 2 weeks.

### FAANG framing dimensions

- Team: 9 developers; 5 junior engineers mentored
- Delivery: 45+ production releases
- Quality: 90% test-coverage target; review rework down 30%
- Team productivity: onboarding 4 weeks to 2 weeks
- Recognition: 3+ appreciations
- Ownership: requirements through production release

### Resume keywords

technical leadership, mentoring, full development cycle, end-to-end SDLC, requirements, technical design, system design, code review, testing, UAT, production launch, Agile, Rally, stakeholder communication, cross-functional collaboration.

---

# Tata Consultancy Services — Software Engineer I

## TCS-I-01 — Transaction-State APIs and Cross-System Consistency

### Engineering story

Keval coordinated transaction-state API contracts across 3 Java and Spring Boot applications and 9 engineering teams. The services connected relational and NoSQL systems through JDBC, Hibernate, Kafka, Redis, and REST APIs so connected applications could rely on consistent workflow state.

The APIs protected 27,000 daily transactions, kept p95 response time under 100ms, and reduced manual reconciliation by 18%. The work included API design, database communication, concurrency controls, validation, deployment coordination, and production support.

### FAANG framing dimensions

- Scope: 3 applications; 9 engineering teams; 27,000 daily transactions
- Performance: p95 under 100ms
- Data correctness: manual reconciliation down 18%
- Mechanism: Java, Spring Boot, APIs, Kafka, Redis, SQL/NoSQL

### Resume keywords

Java, Spring Boot, REST APIs, distributed systems, transaction state, data consistency, Kafka, Redis, JDBC, Hibernate, SQL, NoSQL, concurrency, p95 latency, backend services.

---

## TCS-I-02 — Legacy Java Recovery and Modernization

### Engineering story

Keval recovered a dependency-blocked Java service that could not reach production readiness. He upgraded the service from Java 8 to Java 11, resolved dependency and integration conflicts, repaired cross-application communication, and added Redis caching.

The service was recovered within 2 months, API response time improved by 17%, and the Redis-backed cache reached an 83% hit rate.

### FAANG framing dimensions

- Problem: legacy dependency and integration failure
- Delivery: production readiness restored within 2 months
- Performance: API response time improved 17%
- Caching: 83% cache-hit rate
- Mechanism: Java 8 to 11 migration, Redis, dependency remediation, debugging

### Resume keywords

Java 11, modernization, legacy systems, Redis, caching, dependency management, REST APIs, debugging, production readiness, performance optimization, distributed communication.

---

## TCS-I-03 — CI/CD, Testing, UAT, and Release Delivery

### Engineering story

Keval standardized GitLab and Jenkins CI/CD workflows across 7+ applications and 45+ production releases. The pipelines incorporated build validation, automated quality gates, unit and integration tests, API tests, UAT support, environment deployment, and rollback behavior.

The workflow ran 150+ tests per release, reduced deployment time from 2 hours to 5 minutes, supported one-click rollback, and delivered releases with zero downtime. Java stories used JUnit and Mockito; Python workflows used Pytest; user-facing changes used UAT and A/B testing when applicable.

### FAANG framing dimensions

- Scope: 7+ applications; 45+ releases
- Quality: 150+ tests per release
- Delivery speed: 2 hours to 5 minutes
- Reliability: zero downtime; one-click rollback
- Mechanism: GitLab, Jenkins, JUnit, Mockito, Pytest, Docker, CI/CD

### Resume keywords

CI/CD, GitLab, Jenkins, JUnit, Mockito, Pytest, automated testing, integration testing, API testing, UAT, A/B testing, quality gates, deployment automation, rollback, zero downtime, release engineering.

---

## TCS-I-04 — Linux Migration and Cloud Environment Standardization

### Engineering story

Keval migrated 7+ applications from CentOS to Amazon Linux with zero downtime. He resolved 25+ package blockers, validated application behavior across environments, reduced environment-readiness checks from 4 hours to 30 minutes, and documented 12 reusable upgrade steps.

The repeatable migration procedure became a reusable operating pattern for future upgrades. The work included collaboration with Amazon engineers on missing packages and dependency behavior, along with AWS/GCP environment setup based on deployment requirements.

### FAANG framing dimensions

- Scope: 7+ applications; 25+ dependency blockers
- Reliability: zero downtime
- Operational efficiency: readiness checks 4 hours to 30 minutes
- Reuse: 12 documented upgrade steps
- Mechanism: CentOS, Amazon Linux, AWS, Linux packages, Bash, Docker

### Resume keywords

Linux, CentOS, Amazon Linux, AWS, GCP, cloud migration, package dependencies, Bash, environment validation, zero downtime, operational excellence, technical documentation.

---

## TCS-I-05 — Cross-Database Design and Query Optimization

### Engineering story

Across TCS backend, portal, reporting, and workflow systems, Keval worked with Oracle, MongoDB, MySQL, PostgreSQL, Microsoft SQL Server, SQL, and NoSQL data models. He contributed to schema design, database communication, query behavior, and application-level data access through JDBC, Hibernate, and service-layer integrations.

Database-design and query improvements increased query performance by 30% across the associated workflows.

### FAANG framing dimensions

- Data systems: five relational/document database technologies
- Performance: query behavior improved 30%
- Mechanism: schema design, query optimization, JDBC, Hibernate, application data access

### Resume keywords

Oracle, MongoDB, MySQL, PostgreSQL, Microsoft SQL Server, SQL, NoSQL, schema design, query optimization, JDBC, Hibernate, data modeling, database performance.

---

## TCS-I-06 — Full-Stack Framework and Tested Feature Delivery

### Engineering story

Across TCS user stories, Keval built backend, frontend, and full-stack workflows using Java, Spring MVC, Hibernate, JDBC, JavaScript, TypeScript, Node.js, Next.js, jQuery, Angular, React, HTML, and CSS. He integrated user interfaces with REST APIs, databases, authentication controls, application state, and release workflows.

Feature delivery followed unit and integration testing, code review, CI validation, QA, UAT, and production deployment. Java work used JUnit and Mockito, Python work used Pytest, and frontend or workflow changes used appropriate test cases and A/B comparison when required.

### FAANG framing dimensions

- Scope: full-stack feature delivery across multiple enterprise applications
- Mechanism: frontend, backend, API, database, identity, testing, and CI/CD integration
- Quality: repeatable testing and release lifecycle

### Resume keywords

React, Angular, TypeScript, JavaScript, Node.js, Next.js, Java, Spring MVC, Hibernate, JDBC, HTML, CSS, REST APIs, full-stack development, testing, CI/CD, UAT.

---

# Global Health Impact — Software Engineering Intern

## GHI-01 — Health-Data Ingestion and Quality Pipeline

### Engineering story

Keval built Python data-ingestion and validation workflows that processed 10M+ weekly WHO health records from CSV and Excel into PostgreSQL and MongoDB. The pipeline standardized disease, drug, country, and year data; handled invalid and missing records; and prepared datasets for APIs, dashboards, analytics, and prediction workflows.

The pipeline reduced manual data preparation by 90%, cut ingestion runtime from 6 hours to 45 minutes, and reduced invalid records by 35%.

### FAANG framing dimensions

- Data scale: 10M+ weekly records
- Pipeline performance: 6 hours to 45 minutes
- Data quality: invalid records down 35%
- Automation: manual preparation down 90%
- Mechanism: Python, CSV/Excel, PostgreSQL, MongoDB, validation

### Resume keywords

Python, data pipelines, ETL, data ingestion, data validation, data quality, PostgreSQL, MongoDB, CSV, Excel, healthcare data, WHO data, analytics workflows.

---

## GHI-02 — Health-Data APIs and Research Queries

### Engineering story

Keval developed API-backed workflows for disease, drug, country, and year analysis across 150+ countries. The services exposed processed health data and dashboard-ready results through consistent query and API contracts.

The system handled 2,000+ research queries per week with p95 latency under 1 second and reduced reporting turnaround from hours to 30 seconds.

### FAANG framing dimensions

- Geographic scope: 150+ countries
- Traffic: 2,000+ research queries/week
- Performance: p95 under 1 second
- User efficiency: hours to 30 seconds
- Mechanism: Python, REST APIs, PostgreSQL, MongoDB, AWS

### Resume keywords

Python, REST APIs, backend services, API design, PostgreSQL, MongoDB, p95 latency, research platforms, health data, scalable queries, reporting automation.

---

## GHI-03 — Research Dashboard and Visualization

### Engineering story

Keval delivered React dashboards for 6 research teams, replacing spreadsheet exports with interactive disease, drug, country, year, graph, and world-map workflows. The frontend connected filter and visualization state to API-backed analysis and health-data stores.

Dashboard load time improved from 8 seconds to 2 seconds, allowing researchers to explore validated data and prediction outputs without switching between disconnected spreadsheets.

### FAANG framing dimensions

- Users: 6 research teams
- Performance: dashboard load 8 seconds to 2 seconds
- Product impact: spreadsheet workflows replaced with interactive analysis
- Mechanism: React, JavaScript, HTML, CSS, REST APIs, maps, graphs

### Resume keywords

React, JavaScript, HTML, CSS, dashboards, data visualization, world maps, REST API integration, research tooling, frontend performance, user workflows.

---

## GHI-04 — Machine-Learning Prediction Integration

### Engineering story

Keval worked on country-level health prediction workflows spanning data preparation, feature engineering, model evaluation, inference integration, APIs, and dashboard visualization. The workflow used an 80/20 data split and task-appropriate F1, AUC, or RMSE evaluation according to the prediction problem, with an inference target around 500ms.

Model outputs were connected to API and world-map workflows so researchers could compare country-level results using disease, drug, and health-data parameters.

### FAANG framing dimensions

- ML lifecycle: preparation, features, evaluation, inference, API integration, visualization
- Evaluation: 80/20 split; F1/AUC/RMSE according to task
- Serving target: approximately 500ms inference
- Product integration: model output connected to country-level dashboard workflows

### Resume keywords

machine learning, Python, data preprocessing, feature engineering, model evaluation, F1, AUC, RMSE, inference, APIs, healthcare analytics, prediction workflows, data visualization.

---

## GHI-05 — Research Stakeholder Delivery

### Engineering story

Keval translated researcher requirements into data-ingestion, API, dashboard, visualization, and prediction tasks. He supported 6 research teams, delivered 10+ scoped changes, and reduced clarification cycles by 50% by converting research questions into explicit technical workflows and acceptance criteria.

The work covered technical discovery, implementation, testing, debugging, documentation, deployment support, and feedback-driven iteration.

Keval used GitHub Copilot and Cursor as AI-assisted development tools for implementation support, debugging, test scaffolding, and technical documentation. He reviewed generated changes before integration and validated the final work through testing, researcher acceptance criteria, and feedback-driven iteration.

### FAANG framing dimensions

- Stakeholders: 6 research teams
- Delivery: 10+ scoped changes
- Execution efficiency: clarification cycles down 50%
- Ownership: discovery through delivery and feedback
- AI-assisted development: GitHub Copilot and Cursor with human review, testing, and stakeholder validation

### Resume keywords

stakeholder requirements, cross-functional collaboration, technical discovery, API delivery, dashboard delivery, research software, full development cycle, AI-assisted development, GitHub Copilot, Cursor, documentation, debugging, test scaffolding, human validation, iterative delivery.

---

# Binghamton University — Teaching Assistant

## TA-01 — Code Review, Database Systems, and Review Automation

### Engineering story

As a Teaching Assistant for Database Systems and Object-Oriented Programming, Keval reviewed Java, C++, SQL, database, data-structure, and system-design coursework for 120+ students. He provided code-review feedback on OOP, debugging, clean-code practices, relational and non-relational design, query optimization, concurrency, and implementation correctness.

He automated 12 Python review checks, reduced review time from 15 minutes to 1 minute per submission, and reviewed 1,000+ submissions per semester. He also conducted lab sessions on clean code, data structures, system-design reasoning, debugging, and database implementation.

He used Codex, Cursor, and Claude Code as AI-assisted development tools while refining Python review automation, debugging checks, preparing test cases, and drafting technical documentation. He retained final implementation and review ownership by inspecting generated changes and validating them against course requirements and representative submissions.

### FAANG framing dimensions

- Scale: 120+ students; 1,000+ submissions/semester
- Automation: 12 Python review checks
- Developer productivity: review time 15 minutes to 1 minute
- Technical depth: Java, C++, SQL, databases, OOP, data structures, concurrency, system design
- Collaboration: mentoring, code review, technical communication
- AI-assisted development: Codex, Cursor, and Claude Code with human review and submission-based validation

### Resume keywords

Java, C++, SQL, Python, databases, OOP, data structures, system design, code review, debugging, clean code, query optimization, concurrency, mentoring, technical communication, automation, AI-assisted development, Codex, Cursor, Claude Code, test support, documentation, human validation.

---

# Personal Projects


## PROJ-01 — JobPulse: Job Ingestion and Semantic Search Platform

### Engineering story

Keval built a full-stack job-ingestion and semantic-search platform using React, TypeScript, Node.js/Fastify, Kafka, PostgreSQL/pgvector, Redis, background workers, and embeddings. The system normalized job, company, skill, and location data and supported search, filtering, analytics, and skill extraction.

It was self-tested on 10,000+ public job postings, improved dashboard and batch-analysis time from 3 seconds to under 1 second, indexed 2,000 postings per minute, and kept search p95 latency at 300ms.

### Resume keywords

React, TypeScript, Node.js, Fastify, Kafka, PostgreSQL, pgvector, Redis, embeddings, vector search, semantic search, data ingestion, background processing, p95 latency, Docker.

---

## PROJ-02 — FraudSift: Transaction Analytics and Anomaly Detection

### Engineering story

Keval built a full-stack transaction-analysis and anomaly-detection system using Python, FastAPI, scikit-learn, React, Node.js, Docker, and PostgreSQL. The workflow combined transaction categorization, anomaly detection, risk signals, API inference, and dashboard visualization.

It was self-tested on 22,000+ public or sample transactions across 12 categories and achieved 0.86 precision, 0.81 recall, 0.83 F1, and 120ms p95 inference latency.

### Resume keywords

Python, FastAPI, scikit-learn, anomaly detection, classification, feature engineering, inference, React, Node.js, Docker, PostgreSQL, precision, recall, F1, p95 latency.

---

## PROJ-03 — FilingQuery: Citation-Grounded SEC Filing Retrieval

### Engineering story

Keval built a citation-grounded retrieval system over 5,000+ public SEC filings using Python, FastAPI, PostgreSQL/pgvector, embeddings, vector search, keyword retrieval, reranking, and RAG. The system returned source-linked answers so users could trace generated responses to filing evidence.

Self-tested p95 query latency was 1.8 seconds and citation accuracy reached 92%.

### Resume keywords

Python, FastAPI, PostgreSQL, pgvector, embeddings, vector search, RAG, retrieval, reranking, citations, document intelligence, SEC filings, p95 latency, evaluation.

---

## PROJ-04 — EvalTrace: RAG Evaluation and CI Quality Gates

### Engineering story

Keval built a Python-based RAG evaluation and CI quality-gate workflow using Pytest, DeepEval, and GitHub Actions. The system measured relevance, faithfulness, recall, precision, hallucination, and schema conformance, and blocked low-quality changes before merge.

Testing across 200 prompts and 3 model or prompt variants reduced hallucination from 23% to 4%, completed CI evaluation in 4 minutes, and achieved a 95% schema-pass rate.

### Resume keywords

Python, RAG evaluation, LLM evaluation, DeepEval, Pytest, GitHub Actions, hallucination reduction, faithfulness, relevance, recall, precision, CI quality gates, schema validation.

---

## PROJ-05 — ReviewBot: AI-Assisted Pull-Request Review

### Engineering story

Keval built an AI-assisted pull-request review workflow covering architecture, security, style, static analysis, and test-quality checks. The project used Python, LangGraph, FastAPI, Redis, GitHub webhooks/APIs, Bandit, pylint, Docker, and GitHub Actions.

It was self-tested on 50 pull requests, reduced manual review time by 30%, and surfaced 80% of seeded issues.

### Resume keywords

Python, LangGraph, FastAPI, AI agents, code review, developer tools, GitHub Actions, static analysis, security checks, CI/CD, Redis, Docker, webhooks.

---

## PROJ-06 — Resume Agent: Evidence-Grounded Resume Automation

### Engineering story

Keval built a Python desktop agent that converts job descriptions into evidence-grounded resume JSON, DOCX, and PDF artifacts. The workflow includes JD analysis, structured generation, validation, recruiter review, human approval, concurrent execution, artifact tracking, and final quality checks.

It was tested on 100 job descriptions, reduced tailoring time from 45 minutes to 8 minutes, and achieved a 98% schema-validation pass rate.

### Resume keywords

Python, LLM workflows, AI agents, prompt engineering, structured JSON, evidence grounding, human-in-the-loop, schema validation, workflow orchestration, concurrency, DOCX/PDF generation, evaluation.

---

## PROJ-07 — JobFill AI: Browser-Based Application Automation

### Engineering story

Keval built a Chrome Manifest V3 extension that stores candidate data locally, parses resume information, detects fields, and autofills generic and Workday-style application forms. The extension uses JavaScript, HTML, CSS, service workers, content scripts, Chrome storage, and optional Claude-generated custom answers with user review.

It was tested on 40 forms, achieved 85% field-detection success, and reduced repeated data-entry time from 12 minutes to 3 minutes per application.

### Resume keywords

JavaScript, Chrome Manifest V3, browser automation, service workers, content scripts, local storage, form detection, resume parsing, Claude API, human-in-the-loop, frontend tooling.

---

## PROJ-08 — Bistro AI: Structured AI Ordering Workflow

### Engineering story

Keval built a full-stack restaurant-ordering application using TypeScript, Node.js, Express, React Native/Expo, Prisma, PostgreSQL, Docker, and Claude. The AI workflow translated natural-language requests into validated `ADD`, `REMOVE`, and `UPDATE_QTY` cart actions with schema validation, menu constraints, caching, retries, timeouts, and invalid-request handling.

It was self-tested on 150 orders, achieved 96% valid JSON/action success, and kept p95 response time under 1.2 seconds.

### Resume keywords

TypeScript, Node.js, Express, React Native, Expo, PostgreSQL, Prisma, structured AI outputs, function-like actions, Zod validation, retries, timeouts, caching, Docker, p95 latency.

---

## PROJ-09 — AI-Assisted Engineering Workflow

### Engineering story

Across personal projects, Keval used Codex, Cursor, Claude Code, Git, MCP, and agentic coding workflows to accelerate implementation, refactoring, testing support, debugging, and documentation while retaining final architecture, validation, and delivery ownership.

The workflow reduced personal prototype development time by 40% across 5 projects.

### Resume keywords

AI-assisted development, Codex, Cursor, Claude Code, MCP, agentic coding, developer productivity, debugging, refactoring, testing support, Git.

---
