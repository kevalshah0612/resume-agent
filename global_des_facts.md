# DES Facts

Collected from DES inputs, PASS 1 suggestions, and approval text.

Treat PASS 1 suggestions as review items until you confirm them. Move only reviewed facts into Story.md.

<!-- DES_FACTS_START:Google_Software_Engineer_20260630_225132 -->
## Google_Software_Engineer_20260630_225132

- Recorded: 2026-06-30 22:59:00
- Prompt profile: v2
- Company: Google
- Title: Software Engineer
- Location: Reston, VA

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
AIML | AIML | Mid

ACTIVE OUTPUT MANIFEST:
- ghi_se | Standard | 3
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
Projects: 3 | fraudsift, evaltrace, reviewbot

JD SIGNALS:
- Software development in programming languages (Python, C, C++, Java, JavaScript) | PRIMARY
- Data structures and algorithms | PRIMARY
- Implementing core ML concepts | PRIMARY
- Full-stack software development (front-end UI + back-end services) | PRIMARY
- Write product/system development code | PRIMARY
- Design and code reviews (style guidelines, testability, efficiency) | PRIMARY
- Triage/debug/resolve issues (analyzing sources, impact on hardware/network/service operations/quality) | PRIMARY
- Apply foundational ML concepts to specialized ML areas | PRIMARY
- Design, develop, deliver high-quality code for security products/systems | PRIMARY
- Master's/PhD in CS | PROFILE FACT
- Accessible technologies experience | PREFERRED
- Collaboration with peers/stakeholders | CORE

EXPERIENCE COVERAGE PLAN:
- ghi_se: 4/9 | 44%
  Planned signals: Implementing core ML concepts, Full-stack software development, Apply foundational ML concepts to specialized ML areas, Collaboration with peers/stakeholders
- tcs_se_ii: 6/9 | 67%
  Planned signals: Software development in programming languages, Full-stack software development, Write product/system development code, Design and code reviews, Triage/debug/resolve issues, Design/develop/deliver high-quality code for security products/systems
- tcs_se: 6/9 | 67%
  Planned signals: Software development in programming languages, Full-stack software development, Write product/system development code, Design and code reviews, Triage/debug/resolve issues, Design/develop/deliver high-quality code for security products/systems

OVERALL PROJECTED EXPERIENCE COVERAGE:
8/9 | 89%

PROJECT SELECTION:
- fraudsift: ML implementation (anomaly detection, forecasting), full-stack (Python FastAPI + React), model inference — covers ML concepts, full-stack, Python
- evaltrace: RAG evaluation harness, CI/CD quality gates (DeepEval, pytest, GitHub Actions), benchmark datasets — covers ML evaluation, testing discipline, CI/CD
- reviewbot: Multi-agent PR review orchestrator, security scanning (Bandit, pylint), code review automation — covers code reviews, security, AI agents

MISSING OR PARTIAL SIGNALS:
- Data structures and algorithms | PRIMARY | PARTIAL | JD minimum qualification requires 1 year experience; no direct evidence in allowed stories for any display entry (Story 26 Teaching Assistant not included in plan)
- Accessible technologies experience | PREFERRED | MISSING | JD preferred qualification; no evidence in Story.md

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: data structures and algorithms | story match: Story 20 (technical leadership) references data structures/algorithms in Teaching Assistant context but not in allowed stories for this entry; Story 35 mentions debugging/testing but not DS&A | short story: Used data structures and algorithms to optimize file ingestion workflow performance in Java Spring Boot platform | use when: JD minimum qualification requires 1 year experience with data structures and algorithms | approve text: Approved: 1
DES 2 | scope: ghi_se | keyword: accessible technologies | story match: No direct Story.md match; needs candidate confirmation | short story: Implemented WCAG-compliant React dashboard components for health research platform | use when: JD preferred qualification mentions accessible technologies experience | approve text: Approved: 2

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1,2
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Google_Software_Engineer_20260630_225132 -->

<!-- DES_FACTS_START:ScaleAI_Software_Engineer_20260630_225601 -->
## ScaleAI_Software_Engineer_20260630_225601

- Recorded: 2026-06-30 23:00:39
- Prompt profile: v2
- Company: ScaleAI
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
IAM controls, microservice deployment did in TCS SWE II and I, across all the experience I did OAuth 2.0, OIDC, SAML, and JWT. Also work with Topaz and OpenFGA in TCS SWE I role. Led the development with stackholders with  complex technical concepts to non-technical stakeholders during TCS SWE II
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | JobPulse, ReviewBot

JD SIGNALS:
- Identity infrastructure design and implementation | PRIMARY
- Authentication mechanisms: SSO, MFA, federated identity (SAML, OAuth, OIDC) | PRIMARY
- Authorization mechanisms: ReBAC, ABAC, RBAC | PRIMARY
- Identity governance policies, compliance (NIST, SOC2, ISO 27001) | PRIMARY
- Infrastructure expertise: IAM controls, Infrastructure as Code (Terraform, Pulumi), microservice deployment | PRIMARY
- Hands-on experience with OpenFGA, Authzed, Cedar, Topaz, or similar authorization frameworks at scale | PRIMARY
- Strong understanding of Zanzibar-based ReBAC models, relationship tuples, and access control evaluation | PRIMARY
- Strong knowledge of authentication standards: OAuth 2.0, OIDC, SAML, JWT | PRIMARY
- Extensive experience in distributed systems and public cloud platforms (AWS preferred) | PRIMARY
- Track record of independent ownership of successful engineering projects | PRIMARY
- Excellent communication: translate complex technical concepts to non-technical stakeholders | PRIMARY
- Experience securing API access and implementing access control at application level | CORE
- Multi-cloud infrastructure experience (AWS, Azure, GCP) | CORE
- Proficiency integrating IAM solutions with Java, Python, Node.js, or .NET frameworks | CORE
- 4+ years full-time engineering experience post-graduation with infrastructure/identity specialties | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 6/14 | 43%
  Planned signals: Authentication (OAuth 2.0, OIDC, SAML, JWT), Authorization (RBAC), IAM controls, Microservice deployment, Distributed systems (AWS), Independent ownership, Communication to non-technical stakeholders, API access control (partial)
- tcs_se: 5/14 | 36%
  Planned signals: Authorization (ReBAC via Topaz/OpenFGA), Zanzibar ReBAC models (via Topaz/OpenFGA), IAM controls, Microservice deployment, Multi-cloud (Azure), IAM integration (.NET, Java)
- ghi_se: 3/14 | 21%
  Planned signals: Authorization (RBAC), Distributed systems (GCP), Communication (stakeholder delivery), IAM integration (Python)

OVERALL PROJECTED EXPERIENCE COVERAGE:
11/14 | 79%

PROJECT SELECTION:
- JobPulse: Multi-tenant platform with tenant-scoped data isolation, authentication/authorization patterns, PostgreSQL, Redis, Prisma, Node.js/Fastify — proves multi-tenancy, identity-relevant data isolation, and cloud deployment
- ReviewBot: Multi-agent PR review with GitHub webhooks, LangGraph, Redis, Bandit security scanning, GitHub Actions CI/CD — proves security scanning integration, automated workflow orchestration, and developer-facing auth via GitHub APIs

MISSING OR PARTIAL SIGNALS:
- Identity governance policies, compliance (NIST, SOC2, ISO 27001) | PRIMARY | MISSING | No Story.md or DES evidence for formal compliance frameworks; JD requires this for identity infrastructure work
- Infrastructure as Code (Terraform, Pulumi) | PRIMARY | PARTIAL | Story 06/07 show GitLab CI/CD and AWS operations but no Terraform/Pulumi; JD explicitly requires IaC for identity systems
- OpenFGA/Authzed/Cedar/Topaz at scale | PRIMARY | PARTIAL | DES confirms Topaz/OpenFGA in TCS SWE I but not "at scale" qualification
- Zanzibar-based ReBAC models, relationship tuples, access control evaluation | PRIMARY | PARTIAL | DES confirms Topaz/OpenFGA (Zanzibar-based) but no explicit tuple schema or evaluation design evidence
- API access control at application level | CORE | PARTIAL | Story 16/17 show Spring Security OAuth 2.0 resource server and RBAC on REST APIs; needs stronger confirmation for "application-level" scope

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: Identity governance and compliance (NIST, SOC2, ISO 27001) | story match: Story 02 production deployment with Datadog monitoring, Story 16 production triage and UAT validation | short story: Implemented identity governance controls aligned with NIST/SOC2 frameworks during production deployment and audit preparation | use when: JD requires compliance experience for identity infrastructure | approve text: Approved: 1
DES 2 | scope: tcs_se | keyword: Terraform or Pulumi Infrastructure as Code | story match: Story 06 GitLab CI/CD deployment automation, Story 07 AWS cloud operations | short story: Used Terraform to provision and manage AWS identity infrastructure resources including IAM roles, policies, and federation configurations | use when: JD explicitly requires IaC for identity systems | approve text: Approved: 2
DES 3 | scope: tcs_se | keyword: OpenFGA or Topaz at scale | story match: DES confirms Topaz and OpenFGA in TCS SWE I role | short story: Deployed and operated Topaz authorization service at scale for microservice permission checks across multiple production applications | use when: JD requires hands-on experience with Zanzibar-based authorization frameworks at scale | approve text: Approved: 3
DES 4 | scope: tcs_se | keyword: Zanzibar-based ReBAC models and relationship tuples | story match: DES confirms Topaz and OpenFGA in TCS SWE I role | short story: Designed relationship tuple schemas and ReBAC policies using Topaz for fine-grained access control across interconnected microservices | use when: JD requires strong understanding of Zanzibar ReBAC models | approve text: Approved: 4
DES 5 | scope: tcs_se_ii | keyword: API access control at application level | story match: Story 16 SharePoint authentication recovery with Spring Security, Story 17 enterprise RBAC across REST APIs | short story: Implemented application-level API access control using Spring Security OAuth 2.0 resource server with JWT validation and RBAC enforcement for enterprise workflows | use when: JD nice-to-have asks for API access control experience | approve text: Approved: 5

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1 to 5
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:ScaleAI_Software_Engineer_20260630_225601 -->

<!-- DES_FACTS_START:CoinBase_Software_Engineer_20260630_230704 -->
## CoinBase_Software_Engineer_20260630_230704

- Recorded: 2026-06-30 23:14:55
- Prompt profile: v2
- Company: CoinBase
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | evaltrace, reviewbot

JD SIGNALS:
- Build and operate production software (2+ years) | PRIMARY
- Distributed systems fundamentals | PRIMARY
- Ship backend/platform features with ownership through production | PRIMARY
- Operational instincts: reliability, security, observability | PRIMARY
- Developer infrastructure/platform domain: CI/CD, build systems, deployment/release tooling, test infrastructure | PRIMARY
- Kubernetes, AWS, GitHub Actions, Terraform, or containers (Docker/OCI) | PRIMARY
- Observability and performance tooling (e.g., Datadog) | PRIMARY
- Clear communication, drive scoped projects, collaborate across teams | CORE
- Customer-focused mindset: impact on other engineers | CORE
- Technical design discussions, independent work | CORE
- Knowledge sharing, code reviews, raising quality bar | CORE
- Generative AI responsibly | PREFERRED
- Proficiency in Go or similar language | PROFILE FACT
- 2+ years experience | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 5/7 | 71%
  Planned signals: Build/operate production software, Distributed systems, Ship platform features with ownership, Developer infrastructure (CI/CD, deployment automation, Docker, Kubernetes, AWS), Observability (Datadog, CloudWatch)
- tcs_se: 3/7 | 43%
  Planned signals: Build/operate production software, Distributed systems, Ship backend features with ownership
- ghi_se: 3/7 | 43%
  Planned signals: Build/operate production software, Developer infrastructure (GCP, GitLab, microservices), Customer-focused mindset

OVERALL PROJECTED EXPERIENCE COVERAGE:
8/11 | 73%

PROJECT SELECTION:
- evaltrace: GitHub Actions CI/CD, automated RAG evaluation, quality gates, DeepEval, pytest, benchmark datasets — proves developer infrastructure, CI/CD, testing, observability, GitHub Actions
- reviewbot: GitHub Actions, GitHub webhooks/API, multi-agent PR review, security scanning (Bandit), style analysis (pylint), Docker — proves developer platform, GitHub Actions, security, code review automation, containers

MISSING OR PARTIAL SIGNALS:
- GitHub Actions | PRIMARY | PARTIAL | Story.md has GitLab CI/CD and Jenkins; evaltrace and reviewbot projects use GitHub Actions but need experience-level proof
- Terraform | PRIMARY | MISSING | No Terraform evidence in Story.md or projects
- Go language | PRIMARY | PARTIAL | Candidate has Java, Python, C#, Node.js, TypeScript; JD accepts "Go or similar" with ramp ability
- Generative AI responsibly | PREFERRED | PARTIAL | Story 35 shows AI-assisted engineering workflow; reviewbot uses OpenAI API for review agents

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: GitHub Actions | story match: Story 05 (GitLab CI/CD, Jenkins pipelines) and Story 06 (GitLab CI/CD deployment automation) | short story: Used GitHub Actions for CI/CD pipeline definition and workflow automation in a production service | use when: JD explicitly requires GitHub Actions experience; project evidence exists but experience-level proof needed | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: Terraform | story match: Story 07 (AWS, EC2, S3, Lambda, IAM, CloudWatch infrastructure work) | short story: Used Terraform to provision and manage AWS infrastructure resources for application environments | use when: JD explicitly lists Terraform; strong AWS infrastructure background but no Terraform evidence | approve text: Approved: 2
DES 3 | scope: tcs_se_ii | keyword: Go language | story match: Story 01, 02, 03 (Java/Spring Boot production services) and Story 15 (Node.js/Express backend) | short story: Ramped to Go for a new backend service, applying Java and Node.js production patterns to deliver a reliable platform component | use when: JD requires "Go or similar" proficiency; candidate has 4+ years in comparable backend languages | approve text: Approved: 3
DES 4 | scope: reviewbot | keyword: Generative AI responsibly | story match: Story 31 (ReviewBot uses OpenAI API for multi-agent code review with structured outputs) | short story: Integrated OpenAI API into ReviewBot PR review agents with human oversight, structured output validation, and cost tracking to ensure responsible generative AI use | use when: JD prefers generative AI responsibility; reviewbot demonstrates controlled LLM integration in a developer tool | approve text: Approved: 4

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1,3,4
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:CoinBase_Software_Engineer_20260630_230704 -->

<!-- DES_FACTS_START:Amazon_Software_Engineer_20260630_230801 -->
## Amazon_Software_Engineer_20260630_230801

- Recorded: 2026-06-30 23:15:38
- Prompt profile: v2
- Company: Amazon
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
AIML-01 | AIML | Mid

ACTIVE OUTPUT MANIFEST:
- Software Engineer II | Tata Consultancy Services | Standard | 3 bullets
- Software Engineer | Tata Consultancy Services | Standard | 3 bullets
- Software Engineer | Global Health Impact | Standard | 3 bullets
- Teaching Assistant | Binghamton University | Teaching Assistant | 2 bullets
Projects: 3 | Selected: ReviewBot (Story 31), FilingQuery (Story 29), EvalTrace (Story 30)

JD SIGNALS:
- 3+ years non-internship software development experience | PRIMARY
- 2+ years design/architecture (design patterns, reliability, scaling) | PRIMARY
- Programming language proficiency (Java, Python, C#, TypeScript, etc.) | PRIMARY
- Full SDLC: coding standards, code reviews, source control, CI/CD, testing, operational excellence | PRIMARY
- 3+ years full SDLC (coding standards, code reviews, source control, build, testing, operations) | CORE
- Large-scale distributed systems, multi-tiered, SOA | CORE
- Communication with users, technical teams, management (requirements, features, designs) | CORE
- LLM production deployment, Agentic AI tools/agents/workflows/integration patterns | PRIMARY (role-defining for AI & Strategic Partner Engineering)
- Bachelor's degree or equivalent | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- Software Engineer II | Tata Consultancy Services: 6/8 | 75%
  Planned signals: 3+ years SWE, design/architecture, Java/Spring Boot, full SDLC (CI/CD, testing, code review), distributed systems (microservices, Kafka), operational excellence (observability, debugging), security (OAuth, RBAC, cert automation), technical leadership (code review, mentoring)
- Software Engineer | Tata Consultancy Services: 5/8 | 63%
  Planned signals: 3+ years SWE (early tenure), design/architecture, Java/C#, full SDLC, distributed systems, SQL/NoSQL, REST APIs
- Software Engineer | Global Health Impact: 6/8 | 75%
  Planned signals: Python/FastAPI/Django, full SDLC (CI/CD, testing, deployment), REST APIs, microservices, data pipelines (pandas, NumPy), ML model training/evaluation (K-fold, hyperparameter tuning), RAG integration (Story 24), stakeholder communication, GCP/GitLab
- Teaching Assistant | Binghamton University: 2/8 | 25%
  Planned signals: Code review, debugging, technical communication, Java/C++, SQL, OOP/design patterns

OVERALL PROJECTED EXPERIENCE COVERAGE:
6/8 | 75%

PROJECT SELECTION:
- ReviewBot (Story 31): Multi-agent PR review orchestrator with LangGraph, FastAPI, Redis, GitHub webhooks/API, OpenAI API, Docker, GitHub Actions, Bandit, pylint. Proves: Agentic AI workflows, multi-agent orchestration, LLM integration patterns, CI/CD integration, security/style tooling — directly matches "Agentic AI tools, agents, workflows, integration patterns" and "LLM production deployment".
- FilingQuery (Story 29): RAG over SEC filings with hybrid retrieval (BM25 + pgvector), CrossEncoder reranking, sentence-transformer embeddings, citation-grounded answers, FastAPI, PostgreSQL, Docker. Proves: Production RAG patterns, hybrid retrieval, citation grounding, vector search, containerized deployment — directly matches "LLM production deployment" and "integration patterns".
- EvalTrace (Story 30): Automated RAG evaluation harness with DeepEval, pytest, GitHub Actions, benchmark datasets, merge-blocking quality gates (answer relevancy, faithfulness, contextual recall/precision, hallucination detection). Proves: AI quality gates in CI/CD, systematic evaluation, benchmark-driven development — directly matches "operational excellence", "testing", "CI/CD" for AI systems.

MISSING OR PARTIAL SIGNALS:
- Large-scale distributed systems (SOA) at significant scale | CORE | PARTIAL | TCS stories show microservices/Kafka but scale not quantified; GHI shows microservices but smaller scale. DES candidate for scale confirmation.
- LLM production deployment with real traffic/ops | PRIMARY | PARTIAL | Projects 29, 30, 31 demonstrate production-grade patterns (containerization, CI, evaluation) but not confirmed serving live production traffic. DES candidate for production deployment confirmation.
- Stakeholder communication (users, technical teams, management) | CORE | PARTIAL | Stories 16, 20, 25 show coordination; DES candidate for explicit stakeholder-facing examples.
- 3+ years full SDLC (preferred) | CORE | PARTIAL | TCS covers ~3 years; DES candidate to confirm breadth across coding standards, code reviews, source control, build, testing, operations.

DES CANDIDATE BANK:
DES 1 | scope: Software Engineer II | Tata Consultancy Services | keyword: Large-scale distributed systems / SOA at scale | story match: Story 01 (Java microservices, Kafka, multi-DB) and Story 03 (payment workflows, Kafka, locking) | short story: Designed Java/Kafka microservices handling high-volume file ingestion and payment workflows across Oracle, SQL Server, MongoDB with partitioned Kafka topics for ordering guarantees. | use when: JD emphasizes "large-scale systems in multi-tiered distributed environment" — confirms scale beyond prototype. | approve text: Approved: 1
DES 2 | scope: ReviewBot (Story 31) | keyword: LLM production deployment / Agentic AI in production | story match: Story 31 (LangGraph multi-agent, FastAPI, Docker, GitHub Actions, OpenAI API) | short story: Deployed multi-agent PR review system as containerized FastAPI service with GitHub Actions CI, Redis state, and OpenAI API integration — runs on pull-request webhooks in real repositories. | use when: JD requires "experience developing or deploying Large Language Models in production" — confirms production deployment pattern. | approve text: Approved: 2
DES 3 | scope: Software Engineer II | Tata Consultancy Services | keyword: Full SDLC breadth (coding standards, code reviews, source control, build, testing, operations) | story match: Stories 05 (GitLab CI/CD, JUnit/Mockito/Pytest/Jest, UAT, rollback), 06 (GitLab CI/CD, Ruby deploy, validation, rollback), 18 (Polaris/Black Duck SAST, dependency upgrades, CI/CD), 19 (Datadog/CloudWatch observability), 20 (code review, design patterns, release coordination) | short story: Owned GitLab CI/CD pipelines with multi-language test stages (Java, Python, JS), automated security scans, staged deployments with rollback, Datadog/CloudWatch observability, and mandatory code-review gates across TCS portfolio. | use when: JD preferred qualification asks for "3+ years full software development life cycle" — confirms end-to-end ownership. | approve text: Approved: 3
DES 4 | scope: Software Engineer | Global Health Impact | keyword: Stakeholder communication (users, technical teams, management) | story match: Story 25 (stakeholder communication, requirements gathering, technical discovery, user feedback loops across backend, frontend, data, ML) | short story: Partnered with researchers and cross-functional contributors to define data inputs, API contracts, dashboard requirements, and model evaluation criteria — translated health-domain questions into validated pipelines, APIs, and visualizations. | use when: JD emphasizes "communicating with users, other technical teams, and management to collect requirements, describe features, and technical designs" — confirms product-facing communication. | approve text: Approved: 4

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM 1,2,3,4
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Amazon_Software_Engineer_20260630_230801 -->

<!-- DES_FACTS_START:Meta_Software_Engineer_20260630_230532 -->
## Meta_Software_Engineer_20260630_230532

- Recorded: 2026-06-30 23:19:24
- Prompt profile: v2
- Company: Meta
- Title: Software Engineer
- Location: Sunnyvale, CA

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
AIML | AIML | Mid

ACTIVE OUTPUT MANIFEST:
- ghi_se | Standard | 3
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
Projects: 3 | Selected: JobPulse, FilingQuery, ReviewBot

JD SIGNALS:
- 1+ years hands-on ML, recommendation systems, LLMs, or AI | PRIMARY
- Scripting languages: Python, JavaScript | PRIMARY
- Developing ML models at scale from inception to business impact | PRIMARY
- Technical direction, consensus, cross-functional partnerships | PRIMARY
- Recommendation systems (collaborative filtering, content-based, hybrid, personalization at scale) | PRIMARY
- LLMs (BERT, GPT, similar), fine-tuning, integration, production | PRIMARY
- C/C++, Java, Python, scripting languages | CORE
- Building/shipping high quality work, high reliability | CORE
- Code reviews, testing, rollout, monitoring, proactive changes | CORE
- Large scale software architecture patterns | CORE
- PyTorch and TensorFlow experience | CORE
- AI tools integration to optimize/redesign workflows, measurable impact | CORE
- Publications, patents, open-source in recommendations/LLM space | PREFERRED
- Responsible AI practices (risk assessment, bias mitigation, quality reviews) | PREFERRED
- Prompt/context engineering, agent orchestration, emerging AI | PREFERRED
- Bachelor's degree CS/equivalent | PROFILE FACT
- 2+ years programming experience | PROFILE FACT
- Masters/PhD in CS/ML | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- ghi_se: 4/6 PRIMARY+CORE | 67%
  Planned signals: ML model training/evaluation/production integration (Story 24), Python/JS scripting (Story 24,25), ML models at scale inception to impact (Story 24), Technical direction/cross-functional (Story 25), C/C++/Java/Python (Story 24 Python), Quality/reliability (Story 22,25), Code reviews/testing/rollout/monitoring (Story 22,25), Large scale architecture (Story 22), AI tools integration (Story 35)
- tcs_se_ii: 5/6 PRIMARY+CORE | 83%
  Planned signals: Python/JS scripting (Story 08,15), Technical direction/cross-functional (Story 01,02), C/C++/Java/Python (Story 01,03,08,15), Quality/reliability (Story 02,05,09), Code reviews/testing/rollout/monitoring (Story 02,05,19), Large scale architecture (Story 01,03,08,15), AI tools integration (Story 35)
- tcs_se: 4/6 PRIMARY+CORE | 67%
  Planned signals: Technical direction/cross-functional (Story 01,02), C/C++/Java/Python (Story 01,03,15,17), Quality/reliability (Story 05), Code reviews/testing/rollout/monitoring (Story 05,17), Large scale architecture (Story 03), AI tools integration (Story 35)

OVERALL PROJECTED EXPERIENCE COVERAGE:
9/12 | 75%

PROJECT SELECTION:
- JobPulse: Semantic search, vector embeddings (OpenAI), pgvector, personalization at scale — covers PRIMARY recommendation systems, PRIMARY Python/JS, CORE large scale architecture
- FilingQuery: RAG, sentence-transformers (BERT-based), hybrid retrieval (BM25+pgvector), CrossEncoder reranking, FastAPI production, citation grounding — covers PRIMARY LLMs/production, PRIMARY ML models at scale, CORE PyTorch (via sentence-transformers), CORE AI tools integration
- ReviewBot: LangGraph multi-agent orchestration, OpenAI API, GitHub webhooks/API, automated code review (architecture/security/style), GitHub Actions CI, Bandit/pylint — covers PRIMARY LLMs/production, CORE AI tools integration, PREFERRED agent orchestration, PREFERRED open-source contributions

MISSING OR PARTIAL SIGNALS:
- Recommendation systems (collaborative filtering, content-based, hybrid, personalization at scale) | PRIMARY | PARTIAL | Covered in JobPulse project (semantic search/personalization) but not in Experience; JD requires proven experience designing/building/deploying recsys
- LLMs (BERT, GPT, similar), fine-tuning, integration, production | PRIMARY | PARTIAL | Covered in FilingQuery/ReviewBot projects (sentence-transformers, OpenAI API, LangGraph) but not in Experience; Story 24 is traditional ML not LLM; Story 35 is using AI tools not building with LLMs
- PyTorch and TensorFlow experience | CORE | MISSING | No explicit PyTorch/TensorFlow in Experience stories; Story 24 says "Python-based model training" without framework; FilingQuery uses sentence-transformers (PyTorch-based) but is a project
- Responsible AI practices (risk assessment, bias mitigation, quality reviews) | PREFERRED | MISSING | No evidence in Story.md
- Publications, patents, open-source in recommendations/LLM space | PREFERRED | PARTIAL | Projects are open-source but no publications/patents mentioned

DES CANDIDATE BANK:
DES 1 | scope: ghi_se | keyword: Recommendation systems (collaborative filtering, content-based, hybrid, personalization at scale) | story match: Story 24 (ML prediction for disease impact) — closest but is predictive modeling not recsys | short story: Built a recommendation or personalization system using collaborative filtering or content-based methods for research or health domain to improve user engagement and decision-making | use when: JD PRIMARY signal requires proven recsys experience; Experience has ML prediction but not recsys | approve text: Approved: 1
DES 2 | scope: ghi_se | keyword: LLMs (BERT, GPT, similar), fine-tuning, integration, production | story match: Story 24 (model training, inference integration into APIs/dashboards) — traditional ML not LLM; Story 35 (AI-assisted engineering) — using not building | short story: Fine-tuned or integrated LLMs (BERT, GPT, or similar) into production Python APIs or workflows for research predictions or dashboard features | use when: JD PRIMARY signal requires hands-on LLM fine-tuning/production; Experience has ML production but not LLM-specific | approve text: Approved: 2
DES 3 | scope: ghi_se | keyword: PyTorch and TensorFlow experience | story match: Story 24 (Python model training, K-fold CV, hyperparameter tuning) — framework not specified | short story: Used PyTorch or TensorFlow to train, evaluate, and deploy ML models for disease impact prediction in production research platform | use when: JD CORE signal explicitly requires PyTorch/TensorFlow; Experience mentions Python ML but not framework | approve text: Approved: 3
DES 4 | scope: tcs_se_ii | keyword: LLMs (BERT, GPT, similar), fine-tuning, integration, production | story match: Story 08,09 (Python/FastAPI services) — no LLM; Story 15 (Node.js/React observability) — no LLM; Story 35 (AI-assisted engineering) — using not building | short story: Deployed LLM-powered features (embeddings, classification, or generation) in production Java or Python services for payment, file, or banking workflows | use when: JD PRIMARY signal requires LLM production experience; TCS Experience has ML-adjacent but not LLM | approve text: Approved: 4
DES 5 | scope: tcs_se_ii | keyword: PyTorch and TensorFlow experience | story match: Story 08,09 (Python data pipelines, validation, FastAPI) — no ML framework | short story: Used PyTorch or TensorFlow in Python services for model training or inference serving within TCS platforms | use when: JD CORE signal requires PyTorch/TensorFlow; TCS Python work is data/API not ML framework | approve text: Approved: 5

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1 to 5
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Meta_Software_Engineer_20260630_230532 -->

<!-- DES_FACTS_START:Amazon_SDE_Amazon_Connect_AWS_AI_Voice_Apps_AWS_Amazon_Connect_20260630_233341 -->
## Amazon_SDE_Amazon_Connect_AWS_AI_Voice_Apps_AWS_Amazon_Connect_20260630_233341

- Recorded: 2026-06-30 23:49:53
- Prompt profile: v2
- Company: Amazon
- Title: SDE Amazon Connect (AWS) - AI Voice Apps, AWS Amazon Connect
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | jobpulse, evaltrace

JD SIGNALS:
- Design/architecture with design patterns, reliability, and scaling (2+ years) | PRIMARY
- Large-scale, multi-tiered, multi-threaded, distributed systems using C#, C++, Java, or Perl (1+ years) | PRIMARY
- Object Oriented Design (1+ years) | CORE
- Full SDLC: coding standards, code reviews, source control, build processes, testing, operations (3+ years) | CORE
- 3+ years professional software development experience | PROFILE FACT
- Bachelor's degree in Computer Science, Engineering, Mathematics, or related field | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 4/4 | 100%
  Planned signals: Design/architecture (patterns, reliability, scaling), Distributed systems (Java, C#), Object Oriented Design, Full SDLC (CI/CD, testing, code review, release)
- tcs_se: 4/4 | 100%
  Planned signals: Design/architecture (patterns, reliability, scaling), Distributed systems (Java, C#), Object Oriented Design, Full SDLC (CI/CD, testing, code review, release)
- ghi_se: 1/4 | 25%
  Planned signals: Full SDLC (testing, deployment, stakeholder delivery) — limited Java/C#/distributed/OOD relevance

OVERALL PROJECTED EXPERIENCE COVERAGE:
4/4 | 100%

PROJECT SELECTION:
- jobpulse: Multi-tenant backend with Node.js/Fastify, PostgreSQL, pgvector, Redis, BullMQ workers, Prisma, Docker — proves distributed systems, multi-tiered architecture, async worker queues, containerized deployment
- evaltrace: RAG evaluation harness with Python, DeepEval, pytest, GitHub Actions, CI/CD quality gates, benchmark datasets — proves full SDLC, automated testing, CI/CD pipelines, code review integration, release gates

MISSING OR PARTIAL SIGNALS:
- C++ experience: PARTIAL | Story 15 mentions "selected C and C++ implementation paths for latency-sensitive functions" but scope and ownership unclear | matters for PRIMARY signal "C#, C++, Java, or Perl" completeness
- Perl experience: MISSING | No Story.md evidence | not required since Java and C# satisfy the OR condition

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: C++ implementation for latency-sensitive functions | story match: Story 15 — "selected C and C++ implementation paths for latency-sensitive functions" | short story: Owned C++ modules for low-latency payment processing in banking workflow to meet strict timing requirements | use when: Confirms C++ depth for PRIMARY signal "C#, C++, Java, or Perl" | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: Design patterns and reliability engineering at scale | story match: Story 01 — "reorganized service layer with object-oriented design and reusable patterns", Story 02 — "retry and rollback behavior", Story 03 — "locking for concurrent updates" | short story: Applied circuit-breaker and retry patterns in Java/Kafka file platform to handle downstream failures without data loss | use when: Strengthens PRIMARY signal "design patterns, reliability and scaling" with concrete pattern names | approve text: Approved: 2

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1,2
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Amazon_SDE_Amazon_Connect_AWS_AI_Voice_Apps_AWS_Amazon_Connect_20260630_233341 -->

<!-- DES_FACTS_START:Amazon_Software_Dev_Engineer_II_Enterprise_Security_Products_20260630_233243 -->
## Amazon_Software_Dev_Engineer_II_Enterprise_Security_Products_20260630_233243

- Recorded: 2026-06-30 23:49:28
- Prompt profile: v2
- Company: Amazon
- Title: Software Dev Engineer II, Enterprise Security Products
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
AIML | AIML | Mid

ACTIVE OUTPUT MANIFEST:
- ghi_se | Standard | 3
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
Projects: 3 | reviewbot, evaltrace, jobpulse

JD SIGNALS:
- Design/architecture (design patterns, reliability, scaling) of new and existing systems | PRIMARY
- Large-scale, multi-tiered, multi-threaded, distributed software applications using Java | PRIMARY
- AI assisted or agentic coding practices | PRIMARY
- Building agentic coding processes (Ralph loop, parallelized agentic development) | PRIMARY
- Full SDLC (coding standards, code reviews, source control, build processes, testing, operations) | CORE
- 3+ years non-internship professional software development experience | PROFILE FACT
- 2+ years non-internship design or architecture experience | PROFILE FACT
- 1+ years designing and developing large-scale distributed systems using Java/C#/C++/Perl | PROFILE FACT
- Bachelor's degree in computer science or equivalent | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- ghi_se: 3/5 | 60%
  Planned signals: AI assisted coding practices (Story 25, 35), Full SDLC (Story 25), Design/architecture partial (Story 22 microservices, Story 24 ML pipeline)
- tcs_se_ii: 5/5 | 100%
  Planned signals: Design/architecture (Story 01, 02, 17), Large-scale distributed Java (Story 01, 03), AI assisted coding (Story 35), Building agentic processes partial (Story 35 tool usage), Full SDLC (Story 05, 20)
- tcs_se: 5/5 | 100%
  Planned signals: Design/architecture (Story 01, 02, 17), Large-scale distributed Java (Story 01, 03), AI assisted coding (Story 35), Building agentic processes partial (Story 35 tool usage), Full SDLC (Story 05, 06, 09, 10, 20)

OVERALL PROJECTED EXPERIENCE COVERAGE:
5/5 | 100%

PROJECT SELECTION:
- reviewbot: Building agentic coding processes (multi-agent PR review with LangGraph), AI assisted coding practices (OpenAI agents), Full SDLC (GitHub Actions CI/CD, security scanning)
- evaltrace: AI evaluation/quality gates (DeepEval, RAG metrics), Full SDLC (pytest, GitHub Actions merge-blocking), AI assisted coding practices (RAG evaluation harness)
- jobpulse: Large-scale distributed systems (multi-tenant, async workers with BullMQ), AI assisted coding (OpenAI embeddings, semantic search), Full SDLC (Docker, structured logging, health checks)

MISSING OR PARTIAL SIGNALS:
- Building agentic coding processes | PRIMARY | PARTIAL in Experience (Story 35 shows AI tool usage for development acceleration, no evidence of building agentic coding processes/runners in any experience entry) | Strongly proven in reviewbot project; experience bullets will emphasize AI-assisted development practices while project carries the building proof
- Large-scale distributed Java | PRIMARY | FULL in tcs_se_ii and tcs_se | Not in ghi_se but covered across portfolio
- Design/architecture | PRIMARY | FULL in tcs_se_ii and tcs_se | Partial in ghi_se (microservices, ML pipeline design)

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: Building agentic coding processes | story match: Story 35 (AI-assisted engineering workflow: used Cursor, Codex, Claude Code for implementation, debugging, testing) | short story: Built an internal agentic coding workflow at TCS using LangGraph or similar to automate code review, test generation, or migration tasks | use when: Strengthens PRIMARY signal 4 in experience where only tool usage is documented | approve text: Approved: 1
DES 2 | scope: tcs_se | keyword: Building agentic coding processes | story match: Story 35 (AI-assisted engineering workflow: used Cursor, Codex, Claude Code for implementation, debugging, testing) | short story: Created a parallelized agentic development process at TCS for boilerplate generation, test scaffolding, or legacy code migration | use when: Adds concrete building evidence for PRIMARY signal 4 in second TCS entry | approve text: Approved: 2
DES 3 | scope: ghi_se | keyword: Building agentic coding processes | story match: Story 25 (used Cursor and Codex during implementation and testing while retaining responsibility for architecture decisions) | short story: Designed a reusable agentic coding pattern at GHI for research pipeline code generation or validation workflows | use when: Gives the most recent experience entry a building claim for PRIMARY signal 4 | approve text: Approved: 3

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 3
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Amazon_Software_Dev_Engineer_II_Enterprise_Security_Products_20260630_233243 -->

<!-- DES_FACTS_START:Amazon_Software_Development_Engineer_II_AWS_EBS_Backup_Snapshot_Edge_20260630_233408 -->
## Amazon_Software_Development_Engineer_II_AWS_EBS_Backup_Snapshot_Edge_20260630_233408

- Recorded: 2026-06-30 23:50:17
- Prompt profile: v2
- Company: Amazon
- Title: Software Development Engineer II, AWS EBS Backup Snapshot & Edge
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend-3Exp-2Proj | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- TCS-SE2 | Standard | 3
- TCS-SE1 | Standard | 3
- GHI-SE | Standard | 3
Projects: 2 | JobPulse, FilingQuery

JD SIGNALS:
- 2+ years non-internship professional software development experience | PROFILE FACT
- 2+ years non-internship design/architecture (design patterns, reliability and scaling) | PRIMARY
- Experience programming with at least one software programming language | PRIMARY
- 3+ years full software development life cycle (coding standards, code reviews, source control, build processes, testing, operations) | CORE
- Bachelor's degree in computer science or equivalent | PROFILE FACT
- Design, implement, and operate distributed services at AWS scale across multiple regions | PRIMARY
- Own features end-to-end — design, implementation, testing, deployment, launch | PRIMARY
- Contribute to system architecture decisions, balancing trade-offs between performance, availability, durability, and cost | PRIMARY
- Collaborate with engineers across multiple teams for cross-service integrations and platform improvements | CORE
- Drive improvements including performance optimizations, infrastructure modernization, and technical debt reduction | CORE
- Write and review design documents, participate in code reviews, raise the bar for engineering quality | CORE
- Mentor junior engineers and contribute to a team culture of continuous learning and improvement | CORE

EXPERIENCE COVERAGE PLAN:
- TCS-SE2: 8/10 | 80%
  Planned signals: Design/architecture patterns/reliability/scaling, Programming languages (Java), Distributed services at scale (partial), Own features end-to-end, Architecture trade-offs, Cross-team collaboration, Drive improvements (reliability/security), Design docs/code reviews/engineering quality, Mentor juniors/learning culture
- TCS-SE1: 7/10 | 70%
  Planned signals: Design/architecture (Python platform), Programming languages (Python), Distributed services at scale (partial), Own features end-to-end, Drive improvements (infra modernization), Full SDLC (CI/CD/testing/operations), Design docs/code reviews/testing
- GHI-SE: 5/10 | 50%
  Planned signals: Programming languages (Python/JavaScript), Own features end-to-end, Cross-team collaboration, Full SDLC (testing/deployment), Drive improvements (deployment)

OVERALL PROJECTED EXPERIENCE COVERAGE:
10/10 | 100%

PROJECT SELECTION:
- JobPulse: Distributed backend (Node.js/TypeScript, Fastify, PostgreSQL/pgvector, Redis, BullMQ, Docker, multi-tenancy, OpenAI embeddings) — proves distributed services, async processing, vector search, containerized deployment, multi-tenant data isolation
- FilingQuery: RAG backend (Python, FastAPI, hybrid retrieval BM25/pgvector, CrossEncoder reranking, PostgreSQL, Docker, SEC EDGAR ingestion) — proves data-intensive backend, vector databases, hybrid search, containerized ML pipeline, citation-grounded APIs

MISSING OR PARTIAL SIGNALS:
- Distributed services at AWS scale across multiple regions | PRIMARY | PARTIAL | Have AWS, Docker/K8s, multi-env deployments, but not explicit multi-region AWS-scale operation; could strengthen with DES confirmation
- Architecture trade-offs: durability and cost at scale | PRIMARY | PARTIAL | Have Kafka vs polling (cost/performance), retry/rollback (durability), async vs sync (availability); cost trade-offs less explicit

DES CANDIDATE BANK:
DES 1 | scope: TCS-SE2 | keyword: Distributed services at AWS scale across multiple regions | story match: Story 07 (AWS, EC2, S3, Lambda, CloudWatch, Linux, Docker, Kubernetes, migration, multi-env) | short story: Operated multi-region AWS services (EC2, S3, Lambda) with CloudWatch monitoring across production environments | use when: Proves AWS multi-region operations at scale for PRIMARY signal | approve text: Approved: 1
DES 2 | scope: TCS-SE2 | keyword: Architecture trade-offs: durability and cost | story match: Story 01 (Kafka vs DB polling for cost/performance, partition keys for ordering durability) | short story: Chose Kafka over DB polling to reduce read pressure and cost while preserving per-file ordering durability | use when: Makes cost/durability trade-off explicit for PRIMARY signal | approve text: Approved: 2
DES 3 | scope: TCS-SE1 | keyword: Full SDLC: coding standards, code reviews, source control, build, test, operations | story match: Story 05 (GitLab CI/CD, Jenkins, JUnit, Mockito, Spring Boot Test, Pytest, Jest, Mocha, Vitest, QA, UAT, rollback) | short story: Enforced coding standards and code reviews in GitLab CI/CD with multi-language test gates and automated rollback | use when: Confirms 3+ years full SDLC ownership for CORE signal | approve text: Approved: 3

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1 to 3
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Amazon_Software_Development_Engineer_II_AWS_EBS_Backup_Snapshot_Edge_20260630_233408 -->

<!-- DES_FACTS_START:Apple_Software_Engineer_20260630_235300 -->
## Apple_Software_Engineer_20260630_235300

- Recorded: 2026-07-01 00:01:52
- Prompt profile: v2
- Company: Apple
- Title: Software Engineer
- Location: Cupertino, CA

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | FraudSift, JobPulse

JD SIGNALS:
- Python (2+ years) | PRIMARY
- Data pipelines / data applications (2+ years) | PRIMARY
- Major cloud platform (AWS) (1+ years) | PRIMARY
- REST APIs | PRIMARY
- SQL | PRIMARY
- NoSQL databases | PRIMARY
- Data modeling, schema design, database performance optimization | PRIMARY
- Git | CORE
- Software design patterns and system design principles (scalability, reliability, modularity, separation of concerns) | CORE
- SDLC and engineering best practices | CORE
- Distributed data processing frameworks (Spark, Airflow, Kafka, or equivalent) | CORE
- Data warehousing, ETL/ELT patterns, large-scale analytics workflows | CORE
- End-to-end system design including trade-offs (performance, cost, maintainability) | CORE
- BS + 3 years experience | PROFILE FACT
- Fast-moving ambiguous environments | PROFILE FACT
- AI/LLM tools curiosity | PREFERRED
- Internal tooling / lightweight web interfaces (React, Flask, FastAPI) | PREFERRED
- Communication skills | PROFILE FACT
- Builder mentality | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 7/13 | 54%
  Planned signals: Python, Data pipelines, AWS, REST APIs, SQL, NoSQL, Data modeling/schema/performance, Git, Design patterns, SDLC, Kafka, ETL, End-to-end design
- tcs_se: 6/13 | 46%
  Planned signals: Python, Data pipelines, AWS, REST APIs, SQL, NoSQL, Data modeling/schema/performance, Git, Design patterns, SDLC, Kafka, ETL, End-to-end design
- ghi_se: 6/13 | 46%
  Planned signals: Python, Data pipelines, Cloud (GCP), REST APIs, SQL, NoSQL, Data modeling/schema/performance, Git, Design patterns, SDLC, ETL, End-to-end design

OVERALL PROJECTED EXPERIENCE COVERAGE:
13/13 | 100%

PROJECT SELECTION:
- FraudSift: Python, FastAPI, pandas, NumPy, scikit-learn, REST APIs, anomaly detection, forecasting, React/Node.js integration — proves Python data processing, analytics pipelines, REST APIs, ML-adjacent work
- JobPulse: TypeScript, Node.js, Fastify, PostgreSQL, pgvector, Redis, BullMQ, Prisma, REST APIs, OpenAI embeddings, Docker, multi-tenancy — proves SQL, NoSQL (Redis), queue-based async processing (Kafka equivalent), multi-tenant system design, REST APIs, containerized deployment

MISSING OR PARTIAL SIGNALS:
- AWS (specific) | PRIMARY | PARTIAL | tcs_se_ii has AWS (Story 07, 09, 10); ghi_se used GCP; need explicit AWS confirmation for tcs_se_ii
- Spark / Airflow | CORE | PARTIAL | tcs_se_ii has Kafka (Story 01, 02, 03, 08, 15); no Spark or Airflow in Story.md; JD accepts "or equivalent" — Kafka may satisfy but should confirm
- Data warehousing | CORE | PARTIAL | tcs_se_ii has ETL (Story 08, 09, 15); ghi_se has analytics DBs (Story 21, 22); explicit warehousing term not used; confirm scope

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: AWS cloud platform | story match: Story 07 (AWS EC2, S3, Lambda, IAM, CloudWatch), Story 09 (AWS, AWS RDS), Story 10 (AWS) | short story: Used AWS EC2, S3, Lambda, IAM, CloudWatch, and RDS to deploy, monitor, and operate production services. | use when: JD requires 1+ years AWS; confirms PRIMARY cloud signal for tcs_se_ii | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: Spark or Airflow (distributed data processing) | story match: Story 08 (Kafka, async queues, parallel orchestration); no direct Spark/Airflow match | short story: Designed Kafka-backed async orchestration with retry/rollback for cross-service data workflows, serving as the primary distributed processing framework. | use when: JD lists Spark, Airflow, Kafka as equivalents; Kafka evidence exists but explicit confirmation strengthens CORE signal | approve text: Approved: 2
DES 3 | scope: ghi_se | keyword: Data warehousing / ETL-ELT at scale | story match: Story 21 (pandas/NumPy pipelines into PostgreSQL, MySQL, MongoDB), Story 22 (validated data via REST APIs for analytics) | short story: Built Python ETL pipelines with pandas/NumPy that standardized, validated, and loaded WHO health data into PostgreSQL, MySQL, and MongoDB for research analytics. | use when: JD calls out data warehousing and large-scale analytics; confirms CORE signal with concrete warehouse-targeted loading | approve text: Approved: 3

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1 to 3
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Apple_Software_Engineer_20260630_235300 -->

<!-- DES_FACTS_START:Amazon_Software_Development_Engineer_Sponsored_Product_and_Brands_Sourcing_Delivery_20260630_235119 -->
## Amazon_Software_Development_Engineer_Sponsored_Product_and_Brands_Sourcing_Delivery_20260630_235119

- Recorded: 2026-07-01 00:01:15
- Prompt profile: v2
- Company: Amazon
- Title: Software Development Engineer, Sponsored Product and Brands Sourcing Delivery
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
AIML | AIML | Mid

ACTIVE OUTPUT MANIFEST:
- ghi_se | Standard | 3
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
Projects: 3 | selected closest-match project names: FilingQuery, JobPulse, EvalTrace

JD SIGNALS:
- Design or architecture (design patterns, reliability and scaling) | PRIMARY
- Full software development life cycle (coding standards, code reviews, source control, build processes, testing, operations) | PRIMARY
- Data & AI related technologies (AI/ML, GenAI, Analytics, Database, Storage) | PRIMARY
- High-throughput low-latency distributed systems (billions requests/day, millisecond response) | PRIMARY
- Massive datasets using distributed frameworks | PRIMARY
- Search architecture, information retrieval, NLP, deep learning | PRIMARY
- Production support, troubleshooting, SLA | PRIMARY
- Programming language experience | CORE
- Ad searching, selection, matching systems | CORE
- Mentor junior engineers, technical leadership | CORE
- 3+ years non-internship professional software development experience | PROFILE FACT
- 2+ years non-internship design or architecture experience | PROFILE FACT
- Bachelor's degree in computer science or equivalent | PROFILE FACT
- Cross-functional collaboration | PREFERRED

EXPERIENCE COVERAGE PLAN:
- ghi_se: 6/10 | 60%
  Planned signals: Data & AI technologies (AI/ML, Analytics), Full SDLC, Massive datasets distributed frameworks, Programming language, Mentoring technical leadership, Database Storage
- tcs_se_ii: 7/10 | 70%
  Planned signals: Design architecture, Full SDLC, Distributed systems high-throughput, Production support troubleshooting SLA, Database Storage, Programming language, Mentoring technical leadership
- tcs_se: 6/10 | 60%
  Planned signals: Design architecture, Full SDLC, Distributed systems high-throughput, Production support troubleshooting SLA, Database Storage, Programming language

OVERALL PROJECTED EXPERIENCE COVERAGE:
8/10 | 80%

PROJECT SELECTION:
- FilingQuery: Search architecture, information retrieval, NLP, deep learning (RAG, hybrid retrieval BM25 pgvector CrossEncoder), citation-grounded QA — directly addresses missing PRIMARY signal 6
- JobPulse: Semantic search, vector embeddings (OpenAI pgvector), multi-tenant job matching, async skill extraction — covers search architecture IR and ad-matching-like selection (signal 6, signal 9)
- EvalTrace: RAG evaluation harness (DeepEval, answer relevancy faithfulness recall precision hallucination), CI/CD quality gates — covers AI/ML evaluation and MLOps, strengthens Data & AI technologies signal

MISSING OR PARTIAL SIGNALS:
- Search architecture, information retrieval, NLP, deep learning | PRIMARY | PARTIAL | ghi_se Story 24 shows ML model training but not explicit search/IR/NLP/deep learning for ad matching; projects FilingQuery JobPulse cover this
- Ad searching, selection, matching systems | CORE | MISSING | No Experience evidence for ad/search/matching; JobPulse FraudSift show semantic search categorization but Experience gap remains
- High-throughput low-latency distributed systems at billions requests/day | PRIMARY | PARTIAL | tcs_se_ii Story 01 shows Kafka microservices async processing but not explicit billion-request scale metrics
- Massive datasets using distributed frameworks | PRIMARY | PARTIAL | ghi_se Story 21 shows Python pandas pipelines across databases; 'distributed frameworks' (Spark/Flink) not explicitly confirmed

DES CANDIDATE BANK:
DES 1 | scope: ghi_se | keyword: search architecture, information retrieval, NLP, deep learning | story match: Story 24 (machine learning model training, feature engineering, K-fold cross-validation for country-level disease prediction) | short story: Applied NLP techniques or deep learning models in disease prediction pipelines for research platform | use when: JD PRIMARY signal for search architecture, IR, NLP, deep learning; Experience shows ML but not explicit search/IR/NLP | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: high-throughput low-latency distributed systems billions of requests | story match: Story 01 (Java Spring Boot microservices, Kafka async processing, file ingestion platform) | short story: Operated Java Kafka microservices handling high-concurrency file ingestion with sub-second response targets | use when: JD PRIMARY signal for distributed systems at massive scale; Story 01 shows architecture but not explicit billion-request scale | approve text: Approved: 2
DES 3 | scope: tcs_se_ii | keyword: ad searching selection matching systems | story match: No direct Story.md match; needs candidate confirmation | short story: Designed or optimized search ranking matching algorithms for user-facing sponsored content delivery | use when: JD CORE signal for ad search selection matching; no Experience evidence; projects show semantic search but Experience gap remains | approve text: Approved: 3
DES 4 | scope: ghi_se | keyword: massive datasets distributed frameworks | story match: Story 21 (Python pandas NumPy data pipelines processing WHO CSV Excel into PostgreSQL MySQL MongoDB) | short story: Built distributed data pipelines processing large-scale health datasets across PostgreSQL MySQL MongoDB using Python | use when: JD PRIMARY signal for massive datasets distributed frameworks; Story 21 shows pipelines but distributed frameworks may need Spark/Flink confirmation | approve text: Approved: 4

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1,2,4
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Amazon_Software_Development_Engineer_Sponsored_Product_and_Brands_Sourcing_Delivery_20260630_235119 -->

<!-- DES_FACTS_START:benchling_Software_Engineer_20260701_000226 -->
## benchling_Software_Engineer_20260701_000226

- Recorded: 2026-07-01 00:06:25
- Prompt profile: v2
- Company: benchling
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | jobpulse, fraudsift

JD SIGNALS:
- 3+ years software engineering experience | PROFILE FACT
- Product-first approach, ship code quickly, real-world impact | PRIMARY
- Expertise with at least one web framework, preferably Node or Python | PRIMARY
- Enjoy ownership and building key pieces of product | PRIMARY
- Strong problem solving and iterating on feedback | CORE
- Empathy for customers and curiosity about their challenges | CORE
- Interest in learning life science (desire to learn required) | PREFERRED

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 5/5 | 100%
  Planned signals: product-first/shipping/impact, Node.js web framework (Story 15), ownership/building product, problem solving/iterating, customer empathy (Story 15 user-facing)
- tcs_se: 5/5 | 100%
  Planned signals: product-first/shipping/impact, Node.js web framework (Story 15), ownership/building product, problem solving/iterating, customer empathy (Story 13, 14)
- ghi_se: 5/5 | 100%
  Planned signals: product-first/shipping/impact, Python web framework (FastAPI/Django), ownership/building product, problem solving/iterating, customer empathy

OVERALL PROJECTED EXPERIENCE COVERAGE:
5/5 | 100%

PROJECT SELECTION:
- jobpulse: Node.js/Fastify backend, multi-tenant job aggregation, OpenAI embeddings, vector search, Docker — proves Node.js web framework expertise, product-first shipping, semantic search problem solving, customer empathy for job seekers
- fraudsift: Python/FastAPI backend, scikit-learn ML models (anomaly detection, forecasting), React/TypeScript frontend — proves Python web framework expertise, ML/data science alignment with life science interest, product-first financial analytics, customer empathy for financial users

MISSING OR PARTIAL SIGNALS:
- None for PRIMARY/CORE. Life science interest (PREFERRED) covered at GHI (Story 21-25). Node.js depth at TCS (Story 15 only) is partial but supplemented by GHI Python and projects.

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: Node.js web framework expertise | story match: Story 15 (banking application with Node.js/Express backend) | short story: Built Node.js/Express backend services for banking transfer workflow with Kafka, MongoDB, Oracle, and React/Angular frontend | use when: JD prefers Node or Python; TCS primary stack is Java, so confirming Node.js depth strengthens web framework signal | approve text: Approved: 1
DES 2 | scope: tcs_se | keyword: Node.js web framework expertise | story match: Story 15 (banking application with Node.js/Express backend) | short story: Led Node.js/Express backend development for high-volume banking application with bulk transfers, Kafka queues, and observability portal | use when: JD prefers Node or Python; confirming Node.js ownership at SE level supports web framework expertise claim | approve text: Approved: 2

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1,2
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:benchling_Software_Engineer_20260701_000226 -->

<!-- DES_FACTS_START:Workday_Software_Engineer_20260701_000319 -->
## Workday_Software_Engineer_20260701_000319

- Recorded: 2026-07-01 00:09:29
- Prompt profile: v2
- Company: Workday
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend-Mid | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- Software Engineer II | Tata Consultancy Services | Oct 2022 - Dec 2024 | Standard | 3 bullets
- Software Engineer | Tata Consultancy Services | Mar 2021 - Sep 2022 | Standard | 3 bullets
- Software Engineer | Global Health Impact | Jun 2025 - Aug 2025 | Standard | 3 bullets
Projects: 2 | JobPulse, EvalTrace

JD SIGNALS:
- 4+ years MySQL/PostgreSQL/CloudSQL/cloud-native databases | PRIMARY
- 4+ years backend development (Golang, Python, Java) incl. architecture/design | PRIMARY
- 4+ years AWS/GCP/Azure hands-on | PRIMARY
- 4+ years managing clustered HA database services on Linux | PRIMARY
- 4+ years DevOps/container orchestration (K8s, Docker), deployment, monitoring, scaling | PRIMARY
- Familiarity with AWS GovCloud | PREFERRED
- Knowledge of Terraform, Chef, Ansible | CORE
- Familiarity with Ceph, Gluster, Orchestrator for MySQL, Percona MHA/Galera, Vitess, Pure Storage | PREFERRED
- Experience with database architecture, design, replication, clustering, HA/DR | PRIMARY
- Strong analytical/interpersonal skills | PROFILE FACT
- Self-starter, motivated, quick learner | PROFILE FACT
- Excellent team player, communication | PROFILE FACT
- BS/MS Computer Science | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- Software Engineer II (TCS): 4/7 | 57%
  Planned signals: MySQL/PostgreSQL/cloud-native DBs, Java/Python backend, AWS/Azure, DevOps/K8s/Docker/monitoring, Ansible, DB architecture/HA/DR
- Software Engineer (TCS): 3/7 | 43%
  Planned signals: MySQL/PostgreSQL/cloud-native DBs, Python backend, AWS/Azure, DevOps/K8s/Docker/monitoring, Ansible
- Software Engineer (Global Health Impact): 3/7 | 43%
  Planned signals: MySQL/PostgreSQL/cloud-native DBs, Python backend, GCP, DevOps/GitLab

OVERALL PROJECTED EXPERIENCE COVERAGE:
5/7 | 71%

PROJECT SELECTION:
- JobPulse: PostgreSQL, pgvector, Redis, Docker, multi-tenant REST APIs, Node.js/TypeScript backend — proves cloud-native DB, containerized deployment, backend architecture
- EvalTrace: GitHub Actions CI/CD, pytest, DeepEval quality gates, benchmark datasets — proves automated deployment pipelines, monitoring/validation gates, DevOps automation

MISSING OR PARTIAL SIGNALS:
- Clustered HA database services on Linux (self-managed) | PRIMARY | PARTIAL | Candidate uses managed RDS/CloudSQL; no direct evidence of self-managed clustering, replication, failover on Linux
- Terraform (IaC) | CORE | MISSING | Only Ansible appears in Story 09; no Terraform/Chef evidence
- Database replication/clustering/HA/DR design | PRIMARY | PARTIAL | Story 01/03/09 show multi-DB usage and RDS; no explicit replication topology, Patroni/Vitess, or DR runbooks
- Golang backend experience | PRIMARY | MISSING | JD lists Golang as example; candidate has Java/Python only
- AWS GovCloud | PREFERRED | MISSING | No GovCloud mention in stories
- Ceph/Gluster/Vitess/Percona/Pure Storage | PREFERRED | MISSING | Not present in any story

DES CANDIDATE BANK:
DES 1 | scope: Software Engineer II (TCS) | keyword: Clustered HA database services on Linux | story match: Story 07 (Kubernetes, Linux, Docker) but no self-managed DB clustering | short story: Used Kubernetes Operators (e.g., Patroni, Vitess) to manage PostgreSQL/MySQL HA clusters on Linux, handling replication, automatic failover, and backup/restore | use when: JD requires direct experience with self-managed clustered databases on Linux | approve text: Approved: 1
DES 2 | scope: Software Engineer II (TCS) | keyword: Terraform | story match: Story 09 (Ansible, GitLab CI/CD) but no Terraform | short story: Provisioned AWS RDS, EKS, and VPC networking with Terraform modules integrated into GitLab CI/CD pipelines | use when: JD lists Terraform as automation tool; candidate has Ansible only | approve text: Approved: 2
DES 3 | scope: Software Engineer (TCS) | keyword: Database replication/clustering/HA/DR | story match: Story 08 (async orchestration, retry/rollback) and Story 09 (RDS) but no self-managed replication | short story: Designed PostgreSQL streaming replication with synchronous standby and automated failover using Patroni on Linux VMs; documented DR runbooks and tested quarterly | use when: JD emphasizes database architecture, replication, clustering, HA/DR | approve text: Approved: 3
DES 4 | scope: Software Engineer II (TCS) | keyword: Golang | story match: No Go in any story | short story: Built a Go microservice for high-throughput file metadata extraction, replacing a Java component to reduce latency and memory footprint | use when: JD lists Golang as a primary language; candidate can confirm Go production work | approve text: Approved: 4

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1 to 4
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Workday_Software_Engineer_20260701_000319 -->

<!-- DES_FACTS_START:transperfect_Software_Engineer_20260701_000859 -->
## transperfect_Software_Engineer_20260701_000859

- Recorded: 2026-07-01 00:13:18
- Prompt profile: v2
- Company: transperfect
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | jobpulse, evaltrace

JD SIGNALS:
- Sitecore Apps development (2 years) | PRIMARY
- REST framework (creating and consuming APIs) | PRIMARY
- C# | PRIMARY
- SQL (with Microsoft stack / C# / .NET | PRIMARY
- SQL, designing, creating, managing databases | PRIMARY
- IDEs (Visual Studio Code, IntelliJ) | CORE
- Source code version control (Subversion, Bitbucket) | CORE
- Identifying bugs and testing bug fixes | CORE
- Communicating with development team and clients | CORE
- Bachelor degree + 2 years software development | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 5/8 | 63%
  Planned signals: C#, REST APIs, SQL/SQL Server, Entity Framework, CI/CD, code review, Azure deployment, stakeholder coordination
- tcs_se: 4/8 | 50%
  Planned signals: Java/Spring Boot REST APIs, multi-database (Oracle, SQL Server, MySQL), Kafka event-driven, payment workflows, locking/concurrency, testing, legacy modernization, Redis, production debugging
- ghi_se: 4/8 | 50%
  Planned signals: Python REST APIs, data pipelines, PostgreSQL/MySQL/MongoDB, API validation, GCP deployment, RBAC, debugging, stakeholder communication, requirements gathering

OVERALL PROJECTED EXPERIENCE COVERAGE:
5/8 | 63%

PROJECT SELECTION:
- jobpulse: REST APIs (Fastify), PostgreSQL, Prisma ORM, Docker, multi-tenant architecture, background workers, Redis caching, structured logging — distinct proof slice: API design, database modeling, containerized deployment
- evaltrace: Automated RAG evaluation harness, pytest, DeepEval, GitHub Actions CI/CD, quality gates, benchmark datasets — distinct proof slice: test automation, CI/CD pipelines, quality measurement, GitHub Actions

MISSING OR PARTIAL SIGNALS:
- Sitecore Apps development | PRIMARY | MISSING | Hard requirement; no Story.md evidence for Sitecore CMS platform
- IDEs (Visual Studio Code, IntelliJ) | CORE | PARTIAL | Story 35 mentions Cursor/Codex/Claude Code; no direct VS Code or IntelliJ evidence
- Source code version control (Subversion, Bitbucket) | CORE | PARTIAL | Story.md shows Git/GitHub/GitLab; Subversion and Bitbucket not documented

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: Sitecore Apps development | story match: Story 16 (SharePoint authentication recovery with Java/Spring Boot/OAuth) shows CMS API integration pattern but not Sitecore | short story: Built or maintained Sitecore components using C# and .NET in a multi-site content delivery workflow to support marketing content updates | use when: JD explicitly requires 2 years Sitecore experience; this is the single highest-signal gap | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: Visual Studio Code, IntelliJ | story match: Story 35 (Cursor, Codex, Claude Code, Git for AI-assisted engineering) | short story: Used Visual Studio Code daily for C# .NET Core development, debugging, and Git integration across enterprise portal work | use when: JD lists specific IDEs; candidate can confirm routine use even if not in Story.md | approve text: Approved: 2
DES 3 | scope: tcs_se | keyword: Subversion, Bitbucket | story match: Story 02 (Git, GitHub), Story 05 (GitLab CI/CD), Story 06 (Git), Story 09 (Git, GitLab), Story 22 (Git, GitLab) | short story: Used Bitbucket for source control and pull-request workflows on a .NET Framework service while migrating repositories from Subversion | use when: JD names Subversion and Bitbucket specifically; Git/GitLab evidence is close but not exact | approve text: Approved: 3

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 2,3
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:transperfect_Software_Engineer_20260701_000859 -->

<!-- DES_FACTS_START:Bloomberg_Software_Engineer_20260701_001015 -->
## Bloomberg_Software_Engineer_20260701_001015

- Recorded: 2026-07-01 00:13:53
- Prompt profile: v2
- Company: Bloomberg
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | selected closest-match project names: reviewbot, jobpulse

JD SIGNALS:
- Infrastructure automation at scale | PRIMARY
- Python programming (or object-oriented language) | PRIMARY
- Infrastructure automation/orchestration tools (Ansible, Airflow, Terraform, Chef, Salt) | PRIMARY
- Reliable systems: built, tested, deployed, monitored, improved | CORE
- Infrastructure-as-code / data modeling / source-of-truth systems | CORE
- Observability/telemetry (Splunk, Grafana, Humio, or similar) | CORE
- CI/CD tools and modern software delivery practices | CORE
- Network platforms (Juniper, Nokia, Arista, Cisco, disaggregated) | PREFERRED
- Messaging systems (Kafka, RabbitMQ) | PREFERRED
- 4+ years experience in relevant roles | PROFILE FACT
- Bachelor's/master's degree in CS/Engineering/Math or equivalent | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 5/7 | 71%
  Planned signals: Infrastructure automation at scale, Python programming, Ansible (orchestration tool), Reliable systems lifecycle, CI/CD and modern delivery
- tcs_se: 4/7 | 57%
  Planned signals: Infrastructure automation at scale, Python programming, Reliable systems lifecycle, CI/CD and modern delivery
- ghi_se: 2/7 | 29%
  Planned signals: Python programming, CI/CD (GitLab/GCP)

OVERALL PROJECTED EXPERIENCE COVERAGE:
7/7 | 100%

PROJECT SELECTION:
- reviewbot: CI/CD (GitHub Actions), Python, FastAPI, Redis, Docker, security scanning (Bandit), code review automation, GitHub webhooks — distinct proof for CI/CD automation and security tooling
- jobpulse: Docker, Redis, BullMQ (queue), PostgreSQL, pgvector, multi-tenancy, TypeScript/Node.js — distinct proof for containerization, queuing/caching, multi-tenant infrastructure, and object-oriented language

MISSING OR PARTIAL SIGNALS:
- Infrastructure automation/orchestration tools (Airflow, Terraform, Chef, Salt) | PRIMARY | PARTIAL | Only Ansible evidenced; other listed tools not shown
- Observability/telemetry (Splunk, Grafana, Humio) | CORE | PARTIAL | Datadog and CloudWatch evidenced; Splunk/Grafana/Humio not shown
- Infrastructure-as-code / source-of-truth | CORE | PARTIAL | Ansible for environment config evidenced; Terraform or declarative IaC not shown
- Network platforms (Juniper, Nokia, Arista, Cisco) | PREFERRED | MISSING | No evidence in Story.md
- Messaging systems (RabbitMQ) | PREFERRED | PARTIAL | Kafka evidenced (Stories 03, 08); RabbitMQ not shown

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: Terraform / infrastructure-as-code | story match: Story 09 (Ansible for environment config) and Story 07 (infrastructure automation, repeatable procedures) | short story: Used Terraform to provision AWS cloud resources and manage infrastructure state for production services. | use when: Proves declarative IaC beyond Ansible, directly supports PRIMARY orchestration tools and CORE IaC signals | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: Grafana / observability | story match: Story 19 (Datadog, CloudWatch dashboards, alerting) and Story 09 (Datadog alerts) | short story: Built Grafana dashboards for service-level metrics and connected them to alerting rules for on-call visibility. | use when: Covers CORE observability signal for Grafana specifically, complementary to Datadog/CloudWatch | approve text: Approved: 2
DES 3 | scope: tcs_se_ii | keyword: Airflow / orchestration | story match: Story 08 (async orchestration layer, parallel API calls, retry/rollback) and Story 10 (Python automation, scheduled maintenance) | short story: Designed Airflow DAGs to orchestrate daily data pipelines and infrastructure workflows with retry and dependency management. | use when: Addresses PRIMARY orchestration tools gap for Airflow specifically, shows workflow orchestration at scale | approve text: Approved: 3

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1-infrastructure-as-code and 2- observability, 3- orchestration
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Bloomberg_Software_Engineer_20260701_001015 -->

<!-- DES_FACTS_START:asurion_Software_Engineer_20260701_000416 -->
## asurion_Software_Engineer_20260701_000416

- Recorded: 2026-07-01 00:17:43
- Prompt profile: v2
- Company: asurion
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Fullstack | Fullstack | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | Selected: JobPulse, Bistro AI

JD SIGNALS:
- Full-stack experience (Node.js, React, TypeScript, Python) with deeper backend strength | PRIMARY
- Real-world integrations: webhooks, third-party APIs, installation/configuration flows, failure/edge-case handling | PRIMARY
- Event-driven architecture: Kafka producers/consumers, delivery guarantees, operational safety in distributed systems | PRIMARY
- Non-relational databases (MongoDB) and Redis with practical indexing/query design | PRIMARY
- Production operations and observability: logs, metrics, traces to diagnose and improve | PRIMARY
- Clean, maintainable, traceable code with clear boundaries and abstractions in integration-heavy codebases | PRIMARY
- Cloud-native architectural patterns impacting reliability, scalability, cost | CORE
- CS fundamentals (data structures, algorithms, software design) applied to production | CORE
- AI Coding Agents (Claude Code, Cursor) for reliable software development | PREFERRED
- Real-time communication platforms (LiveKit, WebRTC, voice/video/audio streaming) | PREFERRED
- 3+ years Full Stack/Backend with JavaScript/TypeScript focus | PROFILE FACT
- 3+ years cloud-deployed web applications | PROFILE FACT
- Bachelor's degree in Computer Science or related | PROFILE FACT
- Ownership, autonomy, speed/quality trade-offs under pressure | PROFILE FACT
- Ethical, user-first decision-making | PROFILE FACT
- Inclusive, respectful collaboration | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 6/8 | 75%
  Planned signals: Full-stack (Node/React/TS via Story 15), Integrations (Story 08 cross-system orchestration), Event-driven Kafka (Stories 01, 03, 08, 15), MongoDB/Redis (Stories 03, 08, 09, 15), Observability (Datadog/CloudWatch Stories 02, 07, 09), Cloud-native (AWS/K8s/Docker Stories 05, 06, 07)
- tcs_se: 5/8 | 63%
  Planned signals: Event-driven Kafka (Stories 01, 03), MongoDB/Redis (Stories 01, 03), Integrations (SharePoint API Story 16, OAuth/RBAC Stories 02, 12, 17), Observability (Datadog Story 02), Cloud-native deployment automation (Story 06), Clean abstractions (OOP/design patterns Stories 11, 15)
- ghi_se: 6/8 | 75%
  Planned signals: Full-stack Python/React (Stories 22, 23, 24), Integrations (Research APIs Story 22, data pipelines Story 21), MongoDB (Stories 21, 22), Observability (deployment monitoring Story 25), Cloud-native GCP (Story 22), CS fundamentals applied (ML algorithms Story 24)

OVERALL PROJECTED EXPERIENCE COVERAGE:
6/8 | 75%

PROJECT SELECTION:
- JobPulse: Full-stack Node.js/React/TypeScript, PostgreSQL, Redis, BullMQ async workers, OpenAI embeddings, third-party API integrations (Greenhouse/Lever/Ashby), Docker, multi-tenancy — proves full-stack, integrations, async/event-driven, Redis, AI-assisted search
- Bistro AI: TypeScript/Node.js/Express, React Native, PostgreSQL/Prisma, REST APIs, Anthropic Claude structured AI outputs, Zod validation, Docker, caching/retry/timeout handling — proves full-stack, AI integration, API design, resilience patterns, cloud-native deployment

MISSING OR PARTIAL SIGNALS:
- Kafka delivery guarantees (exactly-once, idempotent consumers) | PRIMARY | PARTIAL | Story 01 uses partition keys for ordering but does not explicitly prove delivery-guarantee design
- MongoDB practical indexing and query design | PRIMARY | PARTIAL | Stories 01, 03, 08, 21 use MongoDB but do not detail index strategy or query optimization
- Redis practical indexing and query design | PRIMARY | PARTIAL | Stories 03, 09 use Redis caching but do not detail data structures or query patterns
- Distributed tracing (OpenTelemetry, Jaeger, Zipkin) | PRIMARY | PARTIAL | Datadog/CloudWatch cover metrics/logs; traces not explicitly evidenced
- AI Coding Agents in production workflows | PREFERRED | PARTIAL | Story 35 mentions Cursor/Codex/Claude Code but not production integration or reliability practices
- Real-time communication (LiveKit, WebRTC) | PREFERRED | MISSING | No direct Story.md match
- Installation/configuration flows for third-party integrations | PRIMARY | PARTIAL | SharePoint auth recovery (Story 16) shows one config flow; broader pattern not evidenced

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: Kafka delivery guarantees | story match: Story 01 (Kafka partition keys for file-ID ordering) | short story: Designed idempotent Kafka consumers with exactly-once semantics for payment workflow to prevent duplicate transaction processing | use when: JD requires delivery guarantees and operational safety in event-driven systems | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: MongoDB indexing and query design | story match: Story 01 (MongoDB for file metadata across microservices) | short story: Created compound indexes on file-id and status fields and optimized aggregation pipelines for dashboard queries reducing latency | use when: JD requires practical MongoDB indexing/query design | approve text: Approved: 2
DES 3 | scope: tcs_se_ii | keyword: Redis data structures and query patterns | story match: Story 09 (Redis caching for repeated data access in ticket platform) | short story: Used Redis sorted sets for rate-limiting windows and hash structures for session caching with TTL-based eviction | use when: JD requires practical Redis indexing/query design beyond basic caching | approve text: Approved: 3
DES 4 | scope: tcs_se_ii | keyword: Distributed tracing | story match: Story 07 (CloudWatch, Datadog for metrics/logs) | short story: Integrated OpenTelemetry instrumentation across Python and Java services to propagate trace context through Kafka and HTTP calls | use when: JD requires logs, metrics, and traces for production diagnosis | approve text: Approved: 4
DES 5 | scope: ghi_se | keyword: AI Coding Agents in production workflows | story match: Story 35 (Cursor, Codex, Claude Code for implementation) | short story: Used Cursor and Claude Code to generate and refactor FastAPI endpoint code, then validated via pytest and CI before production deployment | use when: JD prefers familiarity with AI coding agents for reliable software development | approve text: Approved: 5
DES 6 | scope: tcs_se | keyword: Third-party installation/configuration flows | story match: Story 16 (SharePoint OAuth 2.0 authentication recovery) | short story: Built reusable configuration service for OAuth 2.0 client credentials, token refresh, and webhook registration across multiple SharePoint tenants | use when: JD requires experience with installation/configuration flows for third-party APIs | approve text: Approved: 6

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1 to 6
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:asurion_Software_Engineer_20260701_000416 -->

<!-- DES_FACTS_START:Microsoft_Software_Engineer_20260701_000731 -->
## Microsoft_Software_Engineer_20260701_000731

- Recorded: 2026-07-01 00:17:12
- Prompt profile: v2
- Company: Microsoft
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | jobpulse, reviewbot

JD SIGNALS:
- Building/testing/maintaining production-quality software in collaborative engineering environment | PRIMARY
- Industry experience building and maintaining open-source software (OSS) | PRIMARY
- Design, produce, deliver software for cloud service reliability, scalability, performance, security, efficiency | PRIMARY
- Fixing, enhancing, supporting services in production including periodic on-call duties | PRIMARY
- Participate actively in code reviews, bug/issue triage, support informed decisions | PRIMARY
- Solid understanding of data structures, algorithms, systems fundamentals | CORE
- Working with PostgreSQL | CORE
- Proficient analytical skills with systematic/structured approaches to software design | CORE
- Collaborate with colleagues globally for enterprise-grade services | CORE
- Review and influence ongoing design, architecture, standards, methods for operating services/systems | CORE
- Bachelor's Degree in CS or related + experience in C/C++/C#/Java/JavaScript/Python | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 7/10 | 70%
  Planned signals: production software delivery, cloud service reliability, production support/on-call, code reviews/triage, PostgreSQL, global collaboration, design/architecture influence
- tcs_se: 6/10 | 60%
  Planned signals: production software delivery, cloud service reliability, production support, code reviews, data structures/algorithms, PostgreSQL
- ghi_se: 6/10 | 60%
  Planned signals: production software delivery, cloud service reliability, data structures/algorithms, PostgreSQL, systematic design, design/architecture influence

OVERALL PROJECTED EXPERIENCE COVERAGE:
9/10 | 90%

PROJECT SELECTION:
- jobpulse: PostgreSQL, Node.js/TypeScript, REST APIs, multi-tenant production architecture, Docker, structured logging, health checks, OpenAI embeddings — proves OSS experience, PostgreSQL, production-quality delivery, systematic design
- reviewbot: Python, LangGraph, FastAPI, GitHub webhooks/API, AI agents, Docker, GitHub Actions, Bandit, pylint — proves code review/triage automation, CI/CD quality gates, security scanning, design standards enforcement

MISSING OR PARTIAL SIGNALS:
- Fixing/enhancing/supporting services in production including periodic on-call duties | PRIMARY | PARTIAL | Story.md shows production support, debugging, release coordination, post-release follow-up but not explicit on-call rotation participation
- Industry experience building/maintaining OSS | PRIMARY | PARTIAL | Professional OSS contributions not documented in Story.md; personal projects will cover in Projects section
- Proficient analytical skills with systematic/structured software design | CORE | PARTIAL | Story 21 shows pipeline design; could strengthen with explicit framework/standardization example

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: on-call production support | story match: Story 02 (production ownership, Datadog monitoring, coordinated production release) and Story 19 (production debugging, post-release follow-up) | short story: Participated in on-call rotation for file ingestion and payment services, responding to production alerts and coordinating incident resolution with stakeholders. | use when: JD explicitly requires periodic on-call duties for cloud service support | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: open-source software contribution in professional capacity | story match: No direct Story.md match; needs candidate confirmation | short story: Contributed to or maintained an open-source project used in production at TCS, such as a shared library, tool, or framework adopted by multiple teams. | use when: JD prefers industry experience building/maintaining OSS; professional OSS strengthens this signal beyond personal projects | approve text: Approved: 2
DES 3 | scope: ghi_se | keyword: systematic software design for data pipelines | story match: Story 21 (led data-processing work, built Python pipelines with pandas/NumPy, standardized formats, handled missing values) | short story: Designed a reusable data pipeline framework with standardized validation, error handling, and monitoring that reduced data-quality incidents across research workflows. | use when: JD prefers proficient analytical skills with systematic/structured approaches to software design | approve text: Approved: 3

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1,3
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Microsoft_Software_Engineer_20260701_000731 -->

<!-- DES_FACTS_START:Stripe_Software_Engineer_Product_Security_Data_Platforms_20260701_000809 -->
## Stripe_Software_Engineer_Product_Security_Data_Platforms_20260701_000809

- Recorded: 2026-07-01 00:16:46
- Prompt profile: v2
- Company: Stripe
- Title: Software Engineer, Product Security Data Platforms
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | JobPulse, ReviewBot

JD SIGNALS:
- Data engineering & distributed systems / high-throughput data pipelines (Kafka, Flink, Spark) | PRIMARY
- Strong programming fundamentals in Java, C++, or Rust | PRIMARY
- Operational mindset / business-critical services / high availability / on-call rotation / observability & debugging | PRIMARY
- Communication, collaboration, technical writing, mentoring, non-technical stakeholders | CORE
- Security domain knowledge / security analytics / threat detection / observability platforms | PREFERRED
- Platform engineering / as-a-service infrastructure | PREFERRED
- Cloud native infrastructure / AWS / Kubernetes / Terraform | PREFERRED
- Product intuition / 0-to-1 initiatives | PREFERRED
- Front-end / full stack / React / TypeScript | PREFERRED
- 2+ years professional software development experience | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 3/4 | 75%
  Planned signals: Data engineering & distributed systems (Kafka), Strong programming (Java), Operational mindset & observability
- tcs_se: 3/4 | 75%
  Planned signals: Data engineering & distributed systems (Kafka), Strong programming (Java, C#), Operational mindset & observability
- ghi_se: 2/4 | 50%
  Planned signals: Communication & stakeholder collaboration, Data pipelines (partial, batch not streaming)

OVERALL PROJECTED EXPERIENCE COVERAGE:
4/4 | 100%

PROJECT SELECTION:
- JobPulse: Data engineering (multi-source ingestion, normalization, async workers), Platform engineering (multi-tenant job aggregation as a service), React/TypeScript frontend, Distributed systems (BullMQ/Redis workers, microservice architecture)
- ReviewBot: Security domain (Bandit security scanning, security agent), Platform engineering (PR review as a service), CI/CD quality gates (GitHub Actions, merge-blocking), Observability (evaluation artifacts, baseline comparison)

MISSING OR PARTIAL SIGNALS:
- On-call rotation (explicit) | PRIMARY | PARTIAL | JD explicitly requires on-call rotation; stories show production support, debugging, observability, rollback, but not explicit on-call rotation schedule
- Design document authorship (technical writing) | CORE | PARTIAL | Story 05 mentions technical documentation; need explicit design document drafting for architecture decisions
- Mentoring junior engineers | CORE | PARTIAL | Story 02 shows code reviews and coordination; Story 35 shows architecture decisions; no explicit mentoring in allowed stories for tcs_se_ii/tcs_se

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: on-call rotation | story match: Story 07 (AWS, Linux, Docker, Kubernetes, Cloud Operations - production support, troubleshooting) and Story 16 (SharePoint Authentication Recovery - production triage, root-cause analysis) | short story: Participated in on-call rotation for business-critical Java services, responding to Datadog/CloudWatch alerts and coordinating incident resolution | use when: JD explicitly requires on-call rotation experience for operational mindset signal | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: design document authorship | story match: Story 01 (Java File Ingestion Platform - designed REST APIs, service layer, Kafka workflow) and Story 05 (CI/CD, Testing, UAT - prepared technical documentation) | short story: Authored design documents for Java/Kafka file ingestion platform covering API contracts, data flow, retry/rollback behavior, and deployment architecture | use when: JD requires excellent technical writing for design documents; strengthens CORE communication signal | approve text: Approved: 2
DES 3 | scope: tcs_se | keyword: mentoring junior engineers | story match: Story 02 (File Workflow Reliability - conducted code reviews, coordinated delivery with engineers) and Story 35 (AI-Assisted Engineering Workflow - architecture decisions, implementation iteration) | short story: Mentored junior engineers through code reviews, design guidance on Java/Spring Boot patterns, and debugging sessions for production issues | use when: JD requires ability to mentor other engineers; strengthens CORE communication signal | approve text: Approved: 3

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1 to 3, on call rotational on monthly basis and mentoring junior engineers more than 40+ juniors
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Stripe_Software_Engineer_Product_Security_Data_Platforms_20260701_000809 -->

<!-- DES_FACTS_START:fiserv_Software_Engineer_20260701_001122 -->
## fiserv_Software_Engineer_20260701_001122

- Recorded: 2026-07-01 00:16:02
- Prompt profile: v2
- Company: fiserv
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
AIML | AIML | Mid

ACTIVE OUTPUT MANIFEST:
- ghi_se | Standard | 3
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
Projects: 3 | JobPulse, FraudSift, EvalTrace

JD SIGNALS:
- Full Stack Java development | PRIMARY
- ETL pipeline design/build/maintain | PRIMARY
- Spring framework (Core, Boot, Batch) | PRIMARY
- Angular framework (frontend) | PRIMARY
- Oracle, PostgreSQL, Snowflake databases | PRIMARY
- Snowflake data warehouse (modeling, optimization, query tuning) | PRIMARY
- AWS Services (S3, EC2, RDS, Lambda, Glue) | PRIMARY
- CI/CD Pipelines (Git, Docker, Jenkins, Harness) | PRIMARY
- Snowflake ML and AI features | PRIMARY
- Data processing | CORE
- Data warehouse and application maintenance | CORE
- Stored procedures and functions | CORE
- Bachelor's degree | PROFILE FACT
- Years of experience (4/3/2 years) | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- ghi_se: 3/12 | 25%
  Planned signals: Data processing, ETL pipelines, PostgreSQL, React frontend, ML model training/evaluation/inference, feature engineering
- tcs_se_ii: 6/12 | 50%
  Planned signals: Full Stack Java, ETL pipelines, Spring framework, Angular, Oracle/PostgreSQL, AWS (EC2/S3/Lambda/RDS), CI/CD (Git/Docker/Jenkins)
- tcs_se: 6/12 | 50%
  Planned signals: Full Stack Java, ETL pipelines, Spring framework, Angular, Oracle/PostgreSQL, AWS (EC2/S3/Lambda/RDS), CI/CD (Git/Docker/Jenkins)

OVERALL PROJECTED EXPERIENCE COVERAGE:
7/12 | 58%

PROJECT SELECTION:
- JobPulse: Closest JD signals — data ingestion/normalization (ETL), PostgreSQL, React frontend, Docker, AI embeddings/semantic search; distinct proof slice — multi-tenant job aggregation with vector search
- FraudSift: Closest JD signals — ML risk detection (Snowflake ML/AI analog), data processing/ETL, full-stack React/Node.js, forecasting; distinct proof slice — transaction analytics with scikit-learn models
- EvalTrace: Closest JD signals — RAG evaluation (ML/AI evaluation), CI/CD GitHub Actions quality gates, automated testing; distinct proof slice — ML model evaluation harness with merge-blocking gates

MISSING OR PARTIAL SIGNALS:
- Snowflake (database, data warehouse, ML/AI features) | PRIMARY | MISSING | JD requires 4 years Snowflake, 3 years warehouse, 2 years ML features; no Story.md evidence for Snowflake
- AWS Glue | PRIMARY | MISSING | JD requires 3 years Glue; Story.md shows AWS EC2/S3/Lambda/RDS but not Glue
- Harness CI/CD | PRIMARY | MISSING | JD requires 3 years Harness; Story.md shows Jenkins/GitLab CI/CD but not Harness
- Stored procedures and functions | CORE | MISSING | JD requires 4 years; Story.md shows Oracle/SQL but not explicit stored procedure work
- Snowflake data warehouse modeling/optimization/tuning | PRIMARY | MISSING | JD requires 3 years; no Snowflake evidence in Story.md
- Snowflake ML and AI features | PRIMARY | MISSING | JD requires 2 years; ghi_se has general ML but not Snowflake-specific

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: Snowflake (database, data warehouse, ML/AI features) | story match: Story 01, 03, 08 show Oracle, PostgreSQL, MySQL, data pipelines, but no Snowflake | short story: Used Snowflake for data warehousing and ML features in TCS enterprise workflows to support analytics and reporting | use when: JD requires 4 years Snowflake, 3 years warehouse, 2 years ML features — top missing PRIMARY signal | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: AWS Glue | story match: Story 07, 09, 10 show AWS EC2, S3, Lambda, RDS, CloudWatch, but no Glue | short story: Built ETL pipelines with AWS Glue for cloud data integration at TCS to replace manual data movement | use when: JD requires 3 years Glue; completes AWS PRIMARY signal coverage | approve text: Approved: 2
DES 3 | scope: tcs_se_ii | keyword: Harness CI/CD | story match: Story 05, 06 show Jenkins, GitLab CI/CD, Docker, but no Harness | short story: Implemented Harness pipelines for Java/Spring Boot deployments at TCS to standardize release automation | use when: JD requires 3 years Harness; completes CI/CD PRIMARY signal coverage | approve text: Approved: 3
DES 4 | scope: tcs_se_ii | keyword: Stored procedures and functions | story match: Story 01, 03 show Oracle, SQL Server, Hibernate, but no explicit stored procedure development | short story: Wrote and maintained Oracle stored procedures for payment and batch workflows at TCS to encapsulate business logic in the database | use when: JD requires 4 years stored procedures; only CORE signal completely missing | approve text: Approved: 4
DES 5 | scope: ghi_se | keyword: Snowflake ML and AI features | story match: Story 24 shows Python ML training, evaluation, inference with scikit-learn, but not Snowflake ML | short story: Used Snowflake ML functions for model training and inference in research platform to keep analytics in the data warehouse | use when: JD requires 2 years Snowflake ML/AI; ghi_se has closest ML evidence | approve text: Approved: 5

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2,3,4,5
--------
```

### Approval / extra evidence

```text
CONFIRM:1 to 5
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:fiserv_Software_Engineer_20260701_001122 -->

<!-- DES_FACTS_START:salesforce_Software_Engineer_20260701_001254 -->
## salesforce_Software_Engineer_20260701_001254

- Recorded: 2026-07-01 00:18:18
- Prompt profile: v2
- Company: salesforce
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | jobpulse, evaltrace

JD SIGNALS:
- Professional experience with Go, PHP/Hacklang, Python, Ruby, or Java | PRIMARY
- Distributed data storage systems at scale (MySQL/Postgres, Kafka, Cassandra, ElasticSearch) | PRIMARY
- Deployed and operated server software on Linux at scale, debugged, analyzed and optimized performance | PRIMARY
performance | PRIMARY
- Operating cloud infrastructure, especially AWS | PRIMARY
- Deployment automation/configuration management tools (Chef, Terraform, Ansible, Puppet) | CORE
- 3+ years in Database, SRE, or infrastructure-owning teams with increasing responsibility | PROFILE FACT
- Write clear, maintainable code | PREFERRED
- Excited to learn, explain trade-offs, find best solutions | PREFERRED
- Curious, eager and able to fix broken things | PREFERRED

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 4/5 | 80%
  Planned signals: Java/Python/Ruby languages, Kafka/PostgreSQL/MongoDB/Redis distributed storage, Linux production ops/debugging/performance, AWS cloud infrastructure, GitLab CI/CD/Jenkins/Ansible deployment automation
- tcs_se: 4/5 | 80%
  Planned signals: Java/Python languages, Kafka/PostgreSQL/MySQL/MongoDB distributed storage, Linux production ops/debugging, AWS cloud infrastructure, GitLab CI/CD/Jenkins deployment automation
- ghi_se: 2/5 | 40%
  Planned signals: Python language, PostgreSQL/MySQL/MongoDB distributed storage, GitLab CI/CD deployment automation

OVERALL PROJECTED EXPERIENCE COVERAGE:
5/5 | 100%

PROJECT SELECTION:
- jobpulse: PostgreSQL, pgvector, Redis, BullMQ, Docker, multi-tenant background workers, REST APIs — proves distributed data storage, async processing, containerized deployment
- evaltrace: DeepEval, pytest, GitHub Actions, CI/CD quality gates, benchmark datasets — proves deployment automation, evaluation harnesses, merge-blocking quality gates

MISSING OR PARTIAL SIGNALS:
- Go language | PRIMARY | PARTIAL | JD lists Go first; Story.md shows Java, Python, Ruby, C#, Node.js, TypeScript but no Go
- PHP/Hacklang | PRIMARY | PARTIAL | JD lists as option; no Story.md evidence
- Terraform | CORE | PARTIAL | JD lists as example; Story.md shows Ansible, GitLab CI/CD, Jenkins but no Terraform
- Chef, Puppet | CORE | PARTIAL | JD lists as examples; no Story.md evidence
- Cassandra, ElasticSearch | PRIMARY | PARTIAL | JD lists as examples; Story.md shows Kafka, PostgreSQL, MySQL, MongoDB, Redis but not Cassandra or ElasticSearch

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: Go | story match: No direct Story.md match; needs candidate confirmation | short story: Used Go in a TCS internal tool or migration to build a lightweight service for operational automation. | use when: JD lists Go as first language option; proving Go would strengthen language coverage | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: Terraform | story match: No direct Story.md match; needs candidate confirmation | short story: Used Terraform to provision AWS infrastructure (EC2, S3, IAM, RDS) for a TCS application environment. | use when: JD explicitly calls out Terraform in deployment automation; Ansible is covered but Terraform is a common AWS pairing | approve text: Approved: 2
DES 3 | scope: jobpulse | keyword: Cassandra or ElasticSearch | story match: Story 27 JobPulse uses PostgreSQL, pgvector, Redis; no Cassandra or ElasticSearch | short story: Added ElasticSearch to JobPulse for full-text job search indexing alongside pgvector semantic search. | use when: JD lists Cassandra/ElasticSearch as distributed storage examples; project can demonstrate adjacent search/storage technology | approve text: Approved: 3

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:salesforce_Software_Engineer_20260701_001254 -->

<!-- DES_FACTS_START:Travelers_Software_Engineer_20260701_011417 -->
## Travelers_Software_Engineer_20260701_011417

- Recorded: 2026-07-01 01:17:34
- Prompt profile: v2
- Company: Travelers
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | fraudsift, evaltrace

JD SIGNALS:
- 4+ years hands-on software development building and maintaining enterprise applications | PRIMARY
- Production-quality code in object-oriented languages (Java, C#, Python, JavaScript) | PRIMARY
- Designing and implementing RESTful APIs and integrating systems through web services | PRIMARY
- Full software development lifecycle (requirements through deployment and maintenance) | PRIMARY
- Version control systems and modern development tools and practices | PRIMARY
- Agile/Scrum environments and cross-functional team collaboration | PRIMARY
- History of successfully learning and adapting to new technologies and platforms | CORE
- Salesforce development experience (Apex, Lightning Web Components, Salesforce APIs) | PREFERRED
- Bachelor's degree in computer science, related STEM field, or equivalent | PROFILE FACT
- 4 additional years of software engineering experience | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 7/7 | 100%
  Planned signals: Enterprise applications, OO code (Java, C#), REST APIs and integration, Full SDLC (CI/CD, deployment, testing), Version control and modern tools (GitLab, Jenkins, Docker), Agile/Scrum and cross-functional collaboration, Learning and adapting (Java 11 upgrade, new tech adoption)
- tcs_se: 6/7 | 86%
  Planned signals: Enterprise applications, OO code (Python, JavaScript), REST APIs and integration, Full SDLC (cloud deployment, CI/CD), Version control and modern tools (GitLab, Docker, Kubernetes), Learning and adapting (React, Angular, Python, cloud)
- ghi_se: 7/7 | 100%
  Planned signals: Enterprise applications (research platform), OO code (Python), REST APIs and integration, Full SDLC (testing, deployment, monitoring), Version control and modern tools (GitLab, GCP), Agile/Scrum and cross-functional collaboration, Learning and adapting (ML, new platform)

OVERALL PROJECTED EXPERIENCE COVERAGE:
7/7 | 100%

PROJECT SELECTION:
- fraudsift: Enterprise applications, OO code (Python, JavaScript), REST APIs, system integration, learning new tech | Distinct proof: Financial analytics, ML anomaly detection, transaction processing, Forecasting — directly relevant to insurance/financial services domain
- evaltrace: Full SDLC, version control and modern tools, Agile/CI/CD, learning | Distinct proof: Automated RAG evaluation harness with GitHub Actions merge-blocking quality gates, DeepEval, pytest — demonstrates CI/CD maturity and engineering rigor

MISSING OR PARTIAL SIGNALS:
- Salesforce development (Apex, Lightning Web Components, Salesforce APIs) | PREFERRED | PARTIAL | No Story.md evidence; Travelers lists as strong plus; proof would directly address a preferred qualification

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: Salesforce development (Apex, Lightning Web Components, Salesforce APIs) | story match: No direct Story.md match; needs candidate confirmation | short story: Used Apex and Lightning Web Components in a TCS enterprise module to customize Salesforce workflows for insurance claim processing. | use when: Travelers values Salesforce as strong plus; proof would directly address a preferred qualification | approve text: Approved: 1

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1
--------
```

### Approval / extra evidence

```text
CONFIRM
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Travelers_Software_Engineer_20260701_011417 -->

<!-- DES_FACTS_START:Mercor_Software_Engineer_20260701_011523 -->
## Mercor_Software_Engineer_20260701_011523

- Recorded: 2026-07-01 01:18:21
- Prompt profile: v2
- Company: Mercor
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Backend | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | jobpulse, evaltrace

JD SIGNALS:
- Build and operate reliable backend systems in production | PRIMARY
- System design, performance, reliability, data modeling judgment | PRIMARY
- High-throughput APIs, distributed systems, asynchronous workflows | PRIMARY
- Translate product/marketplace requirements into clean technical systems | PRIMARY
- High engineering standards, bias toward simple durable abstractions | CORE
- Event-driven architecture, queues, caching, observability tooling | CORE
- Search, recommendation, matching, scheduling, marketplace systems | PREFERRED
- ML-powered products, integrating model inference into production | PREFERRED

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 4/6 | 67%
  Planned signals: Build/operate reliable backend systems; System design/reliability/data modeling; High-throughput APIs/distributed systems/async workflows; Event-driven architecture/queues/caching/observability
- tcs_se: 3/6 | 50%
  Planned signals: Build/operate reliable backend systems; High-throughput APIs/distributed systems/async workflows; Translate product requirements into clean technical systems
- ghi_se: 2/6 | 33%
  Planned signals: Build/operate reliable backend systems; Translate product requirements into clean technical systems

OVERALL PROJECTED EXPERIENCE COVERAGE:
9/18 | 50%

PROJECT SELECTION:
- jobpulse: High-throughput Node.js/Fastify backend, PostgreSQL/pgvector, Redis/BullMQ async workers, OpenAI embeddings, semantic search, multi-tenancy, Docker — covers high-throughput APIs, async workflows, search/recommendation (preferred), event-driven architecture
- evaltrace: Python/DeepEval/pytest/GitHub Actions RAG evaluation harness with CI quality gates — covers ML-powered product integration (preferred), observability/evaluation, CI/CD, engineering standards

MISSING OR PARTIAL SIGNALS:
- Marketplace systems | PREFERRED | PARTIAL | JobPulse covers multi-tenant job aggregation (marketplace-adjacent) but no direct marketplace/matching/scheduling evidence in Experience
- ML model inference in production | PREFERRED | PARTIAL | GHI Story 24 integrates model outputs into APIs/dashboards but is a 3-month internship; no TCS production ML inference evidence
- High-throughput APIs at scale | PRIMARY | PARTIAL | Stories mention "high request volume" (Story 15) and "growing submission volume" (Story 01) but no concrete scale metrics in evidence
- Simple durable abstractions | CORE | PARTIAL | Story 01 mentions reusable patterns, Story 20 mentions design patterns, but no explicit "simple durable abstractions" proof in Experience bullets yet

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: High-throughput APIs at scale | story match: Story 15 (banking/transfer workflow, high request volume, bulk transfers) | short story: Owned Node.js/Express backend handling high-volume transfer requests with Kafka queues and MongoDB/Oracle | use when: Proves PRIMARY signal "high-throughput APIs" with concrete scale context | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: Simple durable abstractions | story match: Story 01 (reusable patterns, object-oriented design, separated upload/storage/status/notification) | short story: Designed Spring Boot service layer with reusable patterns separating ingestion, storage, status, notifications for independent evolution | use when: Proves CORE signal "bias toward simple durable abstractions" with concrete design evidence | approve text: Approved: 2
DES 3 | scope: ghi_se | keyword: ML model inference in production | story match: Story 24 (model training, evaluation, integration into backend APIs and React dashboards) | short story: Integrated trained disease-impact models into FastAPI endpoints and React dashboards for researcher predictions | use when: Proves PREFERRED signal "ML-powered products / model inference in production" with end-to-end evidence | approve text: Approved: 3
DES 4 | scope: jobpulse | keyword: Marketplace systems | story match: Story 27 (multi-tenant job aggregation from Greenhouse/Lever/Ashby, semantic search, skill extraction) | short story: Built multi-tenant job aggregation platform normalizing postings from multiple ATS sources with semantic search | use when: Proves PREFERRED signal "marketplace systems" with concrete multi-source aggregation evidence | approve text: Approved: 4

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 1 to 4
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:Mercor_Software_Engineer_20260701_011523 -->

<!-- DES_FACTS_START:gleanwork_Software_Engineer_20260701_011454 -->
## gleanwork_Software_Engineer_20260701_011454

- Recorded: 2026-07-01 01:17:59
- Prompt profile: v2
- Company: gleanwork
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
backend_mid | Backend | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | selected closest-match project names: jobpulse, reviewbot

JD SIGNALS:
- Platform/infrastructure/cloud-focused roles | PRIMARY
- Backend engineering fundamentals | PRIMARY
- Cloud infrastructure in AWS, GCP | PRIMARY
- Terraform or other infrastructure as code tools | PRIMARY
- Deployment automation, onboarding workflows, internal cloud platforms, customer-environment setup systems | PRIMARY
- Work across infrastructure-heavy systems | CORE
- Strong networking fundamentals (VPCs, subnets, routing, proxies, private connectivity) | CORE
- Balance engineering rigor with pragmatism, communicate clearly, collaborate across functions, take ownership in evolving environment | CORE
- 4+ years professional software engineering experience | PROFILE FACT

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 3/5 | 60%
  Planned signals: Platform/infra/cloud roles (Story 07), Backend fundamentals (Stories 01,03,04), AWS cloud infrastructure (Story 07), Deployment automation/platforms (Stories 05,06), Infra-heavy systems (Stories 01,03,07), Ownership/communication (Stories 02,16,20)
- tcs_se: 3/5 | 60%
  Planned signals: Platform/infra/cloud roles (Stories 09,10), Backend fundamentals (Story 08), AWS/Azure cloud infrastructure (Stories 09,10), Deployment automation/platforms (Stories 09,10), Infra-heavy systems (Stories 08,09), Ownership/communication (Story 12), Terraform/IaC partial via Ansible (Story 09)
- ghi_se: 2/5 | 40%
  Planned signals: Backend fundamentals (Story 22), GCP cloud infrastructure (Story 22), Ownership/communication (Story 25)

OVERALL PROJECTED EXPERIENCE COVERAGE:
6/8 | 75%

PROJECT SELECTION:
- jobpulse: TypeScript/Node.js/Fastify backend, PostgreSQL, Redis, BullMQ, Prisma, REST APIs, Docker, multi-tenancy — proves platform/backend engineering, cloud databases, async processing, containerized deployment
- reviewbot: Python/FastAPI, Redis, GitHub webhooks/API, Docker, GitHub Actions, CI/CD integration, multi-agent orchestration — proves developer platform tooling, CI/CD quality gates, API integration, containerized services

MISSING OR PARTIAL SIGNALS:
- Terraform or other infrastructure as code tools | PRIMARY | PARTIAL | Story 09 mentions Ansible for environment config; Story 06 mentions Ruby deployment scripts in GitLab CI/CD. No explicit Terraform. JD explicitly names Terraform.
- Strong networking fundamentals (VPCs, subnets, routing, proxies, private connectivity) | CORE | PARTIAL | Story 07 uses AWS (EC2, Lambda, IAM, CloudWatch) which implies VPC context but does not call out VPC/subnet/routing/proxy work. Story 09 mentions AWS/Azure but not specific networking primitives.
- Internal cloud platform or customer-environment setup system ownership | PRIMARY | MISSING | JD calls out "built or improved deployment automation, onboarding workflows, internal cloud platforms, or customer-environment setup systems." Stories 05/06/09/10 show deployment automation but not a dedicated internal platform or customer-environment onboarding product.

DES CANDIDATE BANK:
DES 1 | scope: tcs_se_ii | keyword: Terraform or other infrastructure as code tools | story match: Story 06 (GitLab CI/CD with Ruby deployment scripts) and Story 07 (AWS, Docker, Kubernetes, infrastructure automation) | short story: Used Terraform to define and version AWS VPC, subnet, and EKS cluster resources for the file platform, replacing manual console configuration. | use when: JD explicitly requires Terraform/IaC; candidate can confirm Terraform or equivalent IaC ownership in TCS SE II scope. | approve text: Approved: 1
DES 2 | scope: tcs_se_ii | keyword: Strong networking fundamentals (VPCs, subnets, routing, proxies, private connectivity) | story match: Story 07 (AWS EC2, Lambda, IAM, CloudWatch, infrastructure automation) | short story: Designed and managed VPC peering, private subnet routing, and NAT gateway configuration for secure cross-account service connectivity in the file ingestion platform. | use when: JD requires explicit VPC/subnet/routing/proxy experience; candidate can confirm hands-on network topology work in TCS SE II scope. | approve text: Approved: 2
DES 3 | scope: tcs_se | keyword: Terraform or other infrastructure as code tools | story match: Story 09 (Ansible for environment configuration, AWS, Azure, Docker, Kubernetes, GitLab CI/CD) | short story: Authored Terraform modules for RDS, ECS, and VPC resources to standardize environment provisioning across AWS and Azure for the ticket platform. | use when: JD requires Terraform/IaC; candidate can confirm Terraform authorship in TCS SE scope alongside Ansible. | approve text: Approved: 3
DES 4 | scope: tcs_se_ii | keyword: Internal cloud platform or customer-environment setup systems | story match: Story 05 (GitLab CI/CD, Jenkins, Docker, automated validation, QA, UAT, rollback) and Story 06 (multi-server deployment automation, validation, rollback) | short story: Built an internal developer platform service that automated tenant onboarding, environment provisioning, and service deployment via GitLab CI/CD pipelines and Terraform, reducing setup time from days to hours. | use when: JD emphasizes internal platform/onboarding automation; candidate can confirm platform product ownership in TCS SE II scope. | approve text: Approved: 4

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2
--------
```

### Approval / extra evidence

```text
CONFIRM: 2,4
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:gleanwork_Software_Engineer_20260701_011454 -->

<!-- DES_FACTS_START:mixpanel_Software_Engineer_20260701_011637 -->
## mixpanel_Software_Engineer_20260701_011637

- Recorded: 2026-07-01 01:34:52
- Prompt profile: v2
- Company: mixpanel
- Title: Software Engineer
- Location: New York, NY

### Candidate DES input / confirmed facts

```text
(none)
```

### PASS 1 model suggestions to review

```text
PLANNING ANALYSIS
--------
ACTIVE PLAN:
Fullstack | Fullstack | Mid

ACTIVE OUTPUT MANIFEST:
- tcs_se_ii | Standard | 3
- tcs_se | Standard | 3
- ghi_se | Standard | 3
Projects: 2 | fraudsift, reviewbot

JD SIGNALS:
- Full-stack fundamentals (frontend, backend, data layers) | PRIMARY
- 2-5+ years professional software engineering experience | PROFILE FACT
- Excellent debugging and technical investigation skills | PRIMARY
- Strong technical communication, async remote collaboration | PRIMARY
- Ownership in ambiguous/greenfield problem spaces | PRIMARY
- Data-driven mindset, curiosity about analytics tools usage | PRIMARY
- Bachelor's degree CS/Math/related or equivalent | PROFILE FACT
- Leveraging AI to drive product improvement | CORE
- React/TypeScript experience | CORE
- Django/Python experience | CORE
- Analytics/observability platforms familiarity | CORE
- Experience building with LLMs, AI agents, or tool-use frameworks | PREFERRED
- Interest in information retrieval, anomaly detection, statistical analysis | PREFERRED

EXPERIENCE COVERAGE PLAN:
- tcs_se_ii: 9/9 | 100%
  Planned signals: Full-stack, Debugging, Communication, Ownership, Data-driven, AI leverage, React/TypeScript, Django/Python, Analytics/observability
- tcs_se: 9/9 | 100%
  Planned signals: Full-stack, Debugging, Communication, Ownership, Data-driven, AI leverage, React/TypeScript, Django/Python, Analytics/observability
- ghi_se: 9/9 | 100%
  Planned signals: Full-stack, Debugging, Communication, Ownership, Data-driven, AI leverage, React/TypeScript, Django/Python, Analytics/observability

OVERALL PROJECTED EXPERIENCE COVERAGE:
9/9 | 100%

PROJECT SELECTION:
- fraudsift: Python FastAPI ML backend (scikit-learn, IsolationForest, forecasting) + React/TypeScript/Node.js frontend; proves React/TypeScript, Django/Python (FastAPI), anomaly detection, statistical analysis, full-stack ownership
- reviewbot: Python LangGraph multi-agent PR review orchestrator (FastAPI, Redis, GitHub webhooks/API, OpenAI, Bandit, pylint, GitHub Actions CI/CD); proves AI agents, tool-use frameworks, Python, CI/CD, developer-tool automation

MISSING OR PARTIAL SIGNALS:
- React/TypeScript at GHI | CORE | PARTIAL | Story 23 shows React/JavaScript/HTML/CSS; TypeScript not explicit
- Django at GHI | CORE | PARTIAL | Story 22/24/25 use Python/FastAPI; Django not explicit
- LLM/AI agent building experience | PREFERRED | PARTIAL | Story 35 covers AI-assisted workflow (using tools); Story 24 covers ML model training; no explicit LLM/agent building in experience

DES CANDIDATE BANK:
DES 1 | scope: ghi_se | keyword: React/TypeScript | story match: Story 23 (React dashboards with JavaScript) | short story: Built React dashboard components with TypeScript for type-safe API integration and fewer runtime errors. | use when: JD explicitly requires React/TypeScript experience | approve text: Approved: 1
DES 2 | scope: ghi_se | keyword: Django/Python | story match: Story 22 (Python REST APIs with FastAPI) | short story: Built Django REST APIs for research data access with authentication, validation, and PostgreSQL models. | use when: JD lists Django/Python as bonus; FastAPI may not map directly | approve text: Approved: 2
DES 3 | scope: fraudsift | keyword: anomaly detection, statistical analysis | story match: Story 28 (FraudSift - IsolationForest anomaly detection, Linear Regression forecasting) | short story: Implemented IsolationForest anomaly detection and Linear Regression spend forecasting on transaction data to surface fraud risk and financial health trends. | use when: JD bonus calls out anomaly detection and statistical analysis; project proves both | approve text: Approved: 3
DES 4 | scope: reviewbot | keyword: AI agents, tool-use frameworks | story match: Story 31 (ReviewBot - LangGraph multi-agent workflow with GitHub API, Bandit, pylint tools) | short story: Built LangGraph multi-agent workflow where specialized agents call GitHub API, Bandit, and pylint as tools to review PRs and post structured feedback. | use when: JD bonus calls out AI agents and tool-use frameworks; project proves agent orchestration with external tools | approve text: Approved: 4

NEXT STEP:
Reply CONFIRM to write with current evidence, or approve DES by ID:
Approved: 1,2,3,4
--------
```

### Approval / extra evidence

```text
CONFIRM: 1,2,3,4
```

Review this block before moving anything into Story.md.
<!-- DES_FACTS_END:mixpanel_Software_Engineer_20260701_011637 -->
