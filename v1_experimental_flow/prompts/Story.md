# Story_GPT

## Hiring Manager Story Contract

This file is the evidence bank for V1. Use it like a senior hiring manager would: pick only the stories that match the target JD, then turn them into qualifications instead of keyword lists.

Every usable story must support this formula:

- Keyword: the exact JD term or close role-family term.
- What: the system, workflow, service, dashboard, pipeline, model, or release work.
- How: the primary technologies and engineering method used.
- Where: the application, platform, API, dashboard, data workflow, deployment path, or user workflow.
- Why: the plain-English reason a nontechnical recruiter, stakeholder, researcher, or manager would care.

Big Tech and senior-manager hiring signals from the role matrix:

- Backend and platform: production APIs, distributed systems, microservices, event-driven processing, data consistency, reliability, testing, observability, cloud, CI/CD, and release ownership.
- Full stack: React or Angular plus backend APIs, user workflows, auth, data validation, production dashboards, testing, and user-facing outcomes.
- AI/ML: Python, data pipelines, model training, evaluation, inference integration, validated outputs, API integration, dashboards, and nontechnical explanation of model value.
- Forward deployed and AI tooling: customer or stakeholder requirements, integrations, demos, workflow automation, debugging, production deployment, and feedback loops.
- Consulting and enterprise delivery: SDLC, Agile, UAT, stakeholder communication, documentation, release readiness, production support, and repeatable delivery.

Default V1 experience structure:

- For Backend, Full Stack, platform, AI tooling, data, DevOps, and general SWE resumes, use exactly three experience entries: Software Engineer II at Tata Consultancy Services, Software Engineer at Tata Consultancy Services, and Software Engineer at Global Health Impact.
- For AI/ML resumes, use exactly two experience entries: one merged Tata Consultancy Services entry and one full Global Health Impact entry.
- Never omit Global Health Impact. It is the primary proof for Python data pipelines, research APIs, React dashboards, ML prediction workflows, GCP, data validation, and stakeholder-facing technical delivery.
- TCS bullet topics can be shuffled between Software Engineer II and Software Engineer to hit the 75 percent first-experience coverage target, but do not turn both TCS entries into Software Engineer II.
- Projects and skills can support the story, but experience ATS coverage must come from experience entries.

Transcript-derived writing rules:

- Recruiters are qualification hunting, not keyword hunting. A skill listed without how, where, and why does not count.
- The first bullet must pass a 20-second skim: role fit, production context, core stack, and business reason should be visible immediately.
- Each experience bullet should naturally carry 3 to 6 important JD keywords while still sounding readable.
- Avoid dense tool piles, parenthetical tool dumps, unexplained acronyms, unsupported metrics, and expert-only wording.
- Prefer plain business reasons: faster user workflow, reliable data, fewer tickets, safer release, better debugging, lower manual work, clearer research analysis, secure access, or stable production behavior.
- Use concrete action instead of vague filler. Prefer designed, built, implemented, validated, debugged, deployed, documented, reviewed, coordinated, or worked with.

## Story 01: TCS Java File Upload Platform

At Tata Consultancy Services, I led a four-engineer redesign of a legacy file-upload application that could not reliably support concurrent users or high volumes of file submissions. I owned the backend design and delivery under an Agile SDLC process, translating stakeholder requirements for faster uploads and higher scale into Java and Spring Boot REST APIs that let users submit, track, and manage files through a single application.

I re-architected the service layer with object-oriented design, reusable design patterns, and optimized data structures and algorithms so the application could evolve without tightly coupling upload handling, data access, notifications, and user-facing status updates. I used Hibernate and Spring Data JPA to connect application workflows with MongoDB, MySQL, PostgreSQL, and Oracle, allowing the platform to work with the data stores already used by connected enterprise systems.

I introduced Kafka-backed asynchronous processing so file ingestion did not block users while downstream work completed. The design routed file storage through microservices connected to Amazon S3, preserved processing order, and sent file-status events to users and external applications through real-time updates, email, and SMS notifications. The new workflow gave stakeholders a scalable upload service that could handle increased traffic and larger file volumes without relying on the legacy application's limited synchronous path.

## Story 02: TCS File Upload Reliability, Security, Testing, and Release Ownership

For the Java file-upload application, I designed retry and rollback behavior for failed distributed workflows so a partially completed upload would not leave documents, status records, or downstream systems in an inconsistent state. The workflow preserved ordering constraints while retrying recoverable failures, which mattered because users needed stored documents and status information to remain reliable even when dependent operations failed.

I created role-based access control for dynamic role management and implemented Okta OAuth 2.0 authentication so users could access only authorized file operations, views, and application functions. I used JUnit and Mockito for automated REST API and workflow testing, completed integration and non-production validation, managed Git and GitHub release activity, prepared technical documentation for UAT approval, and delivered the production release with a rollback plan.

I conducted code reviews for user stories, coordinated delivery with the team and stakeholders, and built Datadog observability for error tracking, monitoring, and alerting in the production environment. This gave the team a way to expand the application while keeping security, release quality, and operational follow-up under control.

## Story 03: TCS Concurrent SharePoint Upload Performance

I designed and shipped a concurrent Java workflow for large 3D files uploaded to Microsoft SharePoint after enterprise users experienced approximately 60-second upload times. I split large files into parts, used multithreading and concurrency to upload portions in parallel through SharePoint APIs, evaluated multiple implementation approaches, and documented the selected design before release.

I validated the workflow through production testing and UAT, then deployed it as a live feature for a large enterprise-user environment. The concurrent upload path reduced processing time from about 60 seconds to 10 seconds, giving users a noticeably faster way to complete large-file workflows while demonstrating performance engineering, API integration, and end-to-end release ownership.

## Story 04: TCS Java Payment APIs, Kafka, and Data Consistency

I designed Java and Spring Boot REST APIs for payment-related workflows that required several connected applications to exchange transaction state across relational and non-relational data stores. In this workflow, SQL, MySQL, Oracle, Microsoft SQL Server, NoSQL stores, and Redis supported different parts of the business process, so the backend design had to preserve correctness while systems processed work asynchronously.

I used Kafka to decouple payment processing and event delivery, implemented locking to protect concurrent updates, and created notification workflows so downstream systems could react to transaction-state changes. I owned design documentation, implementation, API testing, integration testing, UAT, and production release for these backend features, making sure data consistency was validated before users depended on the workflow.

The work improved API latency by 30%, reduced operational support load by 40%, improved cross-application data consistency across three Java and Spring Boot applications, and helped nine engineering teams coordinate API and data behavior. The result was a safer payment workflow for concurrent business activity, rather than a system that relied on manual reconciliation after conflicting updates.

## Story 05: TCS Legacy Java Recovery and Modernization

I recovered a legacy Java application that was blocked by outdated dependencies and could not operate as production-ready software. I upgraded the application to Java 11, resolved dependency conflicts, redesigned communication with connected applications, and added Redis-backed caching to improve repeated access patterns.

I used REST APIs and distributed application communication to reconnect the service with the surrounding platform while debugging the dependency and runtime issues that had prevented stable operation. The application returned to a supportable, production-ready state within two months, giving the organization a usable foundation for future backend integration instead of maintaining a blocked legacy system.

## Story 06: TCS CI/CD, Testing, UAT, and Production Release Delivery

I built and improved GitLab CI/CD and Jenkins pipelines for Java, Spring Boot, React, and related enterprise applications that needed repeatable production releases. I connected code changes to automated validation using JUnit, Mockito, Spring Boot Test, integration tests, API tests, Pytest, Jest, Mocha, and Vitest so application teams could detect issues before production rather than relying only on manual release checks.

I worked across the full delivery path: Git-based source control, Dockerized application workflows, QA validation, UAT coordination, release-readiness checks, production deployment, rollback planning, and post-release verification. The release process supported more than seven enterprise applications and more than forty production deployments, reducing deployment risk and making release quality more consistent across the application portfolio.

## Story 07: TCS Standardized Multi-Server Deployment and Rollback

I standardized a GitLab CI/CD workflow for applications that required coordinated deployment across multiple servers. I integrated Ruby deployment scripts into the pipeline so build, validation, deployment, and rollback activities could run from one repeatable workflow instead of depending on manual server-by-server coordination.

I introduced staged validation checks and a one-command rollback path for release issues, then documented the approach so other application teams could adopt it. The standardized process reduced deployment effort, improved release consistency, reduced release-related downtime, and became a unit-wide practice for applications with frequent production changes.

## Story 08: TCS AWS, Linux, Docker, Kubernetes, and Cloud Operations

I supported the migration of more than seven enterprise applications from CentOS to Amazon Linux 2 and contributed to upgrade planning for Amazon Linux 2023. I investigated missing Linux packages and environment issues with Amazon engineers, created repeatable upgrade procedures, and helped teams move applications to supported operating environments without interrupting users.

I worked across AWS services including EC2, S3, Lambda, IAM, and CloudWatch, while using Linux, Docker, Kubernetes, Python, Bash, and GitLab CI/CD to support application deployment, server cleanup, automation, and environment readiness. The migration completed with zero downtime, the upgrade workflow became a reusable unit practice, and cloud cleanup plus automated maintenance reduced client-environment costs by approximately $30,000 per month.

## Story 09: TCS Python Ticket Platform and Cross-Application Orchestration

I led a nine-developer team that designed and delivered a Python, Django, and FastAPI platform for external users to create and manage high-volume tasks across multiple dependent applications. The platform replaced manual cross-application coordination with a centralized SaaS workflow, allowing users to submit a task in seconds while the system handled the required downstream work.

I designed REST APIs, data pipelines, and validation workflows that integrated SQL, MySQL, PostgreSQL, and MongoDB data sources. The platform ingested, normalized, validated, and reconciled information from connected applications before processing user requests, so data-quality issues were identified early rather than propagating into dependent workflows.

I implemented a centralized orchestration layer where dependent API calls could run in parallel through asynchronous processing and queues. Retry and rollback mechanisms handled failed requests, preserved data consistency across connected services, and improved fault tolerance when one system was temporarily unavailable. The platform reduced ticket volume by 45% after launch by making a complex multi-application process more reliable and easier for external users to complete.

## Story 10: TCS Python Data Validation, Test Automation, and Deployment

For the Python ticket platform, I built FastAPI REST APIs and automated validation services for each integrated application. I used Redis caching, pandas, and NumPy to clean and validate data, identify invalid records, and reduce unnecessary repeated work before data was used by dependent services.

I containerized the platform with Docker and Kubernetes for repeatable deployments across AWS and Azure environments. GitLab CI/CD automated validation and deployment steps, Ansible supported environment configuration and end-to-end workflow checks, AWS RDS supported database workloads, and Kafka handled asynchronous events.

I worked with senior engineers on code reviews, implemented Pytest-based test coverage, prepared API integration and UAT documentation, and configured Datadog for alerts, error reporting, and production visibility. This created a delivery path where API, data, and deployment problems could be detected before production and debugged quickly after release.

## Story 11: TCS Python Operational Automation and Dashboards

I built Python automation for server cleanup, health checks, notification delivery, recurring maintenance, operational dashboards, and environment-readiness checks across application environments. The work addressed repetitive operational tasks that consumed engineering time and delayed the discovery of environment problems before releases.

I used Linux, AWS, Docker, Kubernetes, Datadog, CloudWatch, and GitLab CI/CD to automate routine checks and surface operational signals through dashboards and notifications. The automation reduced manual health-check effort by 90%, improved release readiness and debugging visibility, and gave teams a more reliable process for maintaining application environments.

## Story 12: TCS C#/.NET Enterprise Portal Architecture

I contributed to the design, development, and deployment of an enterprise business portal using C#, .NET Core, ASP.NET Core, Web APIs, Entity Framework, SQL Server, HTML, and CSS. Working in a seven-member Agile team, I helped translate business requirements into a centralized portal where users could submit, track, validate, and manage business requests rather than relying on disconnected manual processes.

I developed backend services and REST API endpoints for portal workflows, user actions, data retrieval, validation, and business-process automation. I applied object-oriented programming and object-oriented design to separate business logic from data-access layers, then used Entity Framework and SQL Server to support reliable database operations. The portal gave users a smoother way to manage business requests while giving the team a maintainable backend structure for future workflow changes.

## Story 13: TCS C#/.NET Portal Security and Controlled Deployment

For the enterprise portal, I implemented OAuth-based authentication, Azure Key Vault secret management, and role-based access control so users could access only the functions and data approved for their roles. Azure Key Vault kept credentials, connection details, and sensitive configuration outside source code and static application settings.

I supported deployment through Azure and Windows Server environments and contributed to CI/CD workflows for build, validation, and release activities. I worked with the team on code review, testing validation, release coordination, and production support so releases remained stable, secure, and aligned with business requirements. The result was a centralized portal with stronger access governance and a controlled delivery process.

## Story 14: TCS React and TypeScript File Workflow Dashboard

I built a React and TypeScript dashboard for the Java and Spring Boot file-upload platform using reusable components, lazy loading, HTML, CSS, JavaScript, Material UI, and Bootstrap. The component architecture and deferred loading improved maintainability, responsiveness, and page-load behavior for users working with file-processing workflows.

I connected the dashboard to REST APIs so users could track file-upload status, perform file-related actions, manage alerts, and receive live notification updates from the Kafka-backed backend workflow. Frontend validation reduced invalid submissions before requests reached backend services, while OAuth 2.0 and role-based access control limited file actions and dashboard views to authorized users. The dashboard gave users a clearer, safer way to monitor and manage file activity without needing to inspect multiple backend systems.

## Story 15: TCS Angular Operations and Ticket Management Dashboard

I developed an Angular-based dashboard with TypeScript, JavaScript, HTML, CSS, Bootstrap, and Material UI-style components for Python backend applications. The dashboard brought application status, ticket workflows, alerts, requests, payment-state visibility, notifications, and operational data into one interface so users did not need to switch between multiple systems.

I integrated the UI with Python REST APIs, backend data services, Datadog monitoring, CloudWatch views, live request data, notification workflows, and RBAC-enabled authentication. Responsive UI behavior and asynchronous API integration let users see updates while backend services processed dependent work. The dashboard improved workflow transparency and made it easier for users and support teams to identify operational issues from one place.

## Story 16: TCS Full-Stack Banking and Transfer Workflow

I led development of a banking application that combined Node.js and Express backend services with Angular and React user interfaces. The application used REST APIs, microservice workflows, MongoDB, Oracle, Kafka-backed queues, and TypeScript-based UI components to support high-volume transfer requests and bulk-transfer workflows.

I designed database structures and applied design patterns across backend and frontend components, then built user-facing pages with HTML, CSS, TypeScript, and Material UI. For latency-sensitive functions, I used C and C++ implementation paths intended to execute more quickly than the surrounding application stack. I also created an observability portal so support teams could monitor service health and operational behavior. The application gave stakeholders a new transfer workflow designed for faster responses, higher request volume, and better support visibility.

## Story 17: TCS SharePoint Authentication Recovery

I led production triage when a Microsoft change to the SharePoint authentication process broke a live workflow. I traced the issue across frontend, backend, data, and SharePoint API layers, coordinated with Microsoft developers, external engineering teams, and internal stakeholders, and identified the authentication-flow change as the root cause.

I designed a reusable internal authentication module with Java, Spring Boot, Spring Security, OAuth 2.0, and SharePoint APIs to centralize authentication and later API access. I validated the solution across lower environments, QA, and UAT before deploying the production fix within forty-eight hours. The reusable module restored the immediate workflow and reduced the likelihood that future SharePoint API calls would fail for the same reason.

## Story 18: TCS Role-Based Access Control Across Enterprise Applications

I implemented role-based access control workflows across ten enterprise applications by integrating internal APIs with relational and non-relational data stores. The design enforced consistent permissions across application workflows, allowing teams to manage authorization through reusable controls instead of handling user access as disconnected manual exceptions.

I used Java, Spring Boot, Spring Security, OAuth 2.0, REST APIs, SQL, NoSQL, IAM, API testing, integration testing, and UAT to validate the access-control behavior before release. The implementation improved access governance, reduced access-request tickets by 22%, and gave enterprise users a more consistent experience across connected applications.

## Story 19: TCS TLS Certificate Lifecycle Automation

I managed TLS and SSL certificate updates across application environments and built a Python script that parameterized certificate replacement and renewal. The script allowed engineers to rotate certificates with minimal rework as expiration dates approached, rather than repeating a manual update process for every application and environment.

I documented the renewal process and helped standardize certificate-rotation practices across the unit. The automation reduced manual certificate-maintenance work, lowered the risk of expiration-related incidents, and gave teams a repeatable process for maintaining certificate-based security.

## Story 20: TCS Dependency Remediation and Secure Release Readiness

I used Polaris and Black Duck to identify vulnerable dependencies and code-quality issues in React, Java, Spring, and Spring Security applications. I prioritized remediation work, upgraded affected dependencies, cleaned vulnerable or low-quality code paths, and validated the changes through testing before production deployment.

I also developed Python- and Java-based automation to streamline vulnerability and code-quality triage across three applications. The work closed SAST findings before release, improved secure-release readiness, and helped teams resolve dependency risk as part of normal engineering delivery rather than after a production issue.

## Story 21: TCS Observability, Monitoring, and Production Debugging

I implemented Datadog monitoring workflows, connected CloudWatch telemetry, configured alerts, and created dashboard views over live requests, application data, errors, and service behavior. The monitoring covered connected applications where support teams needed visibility into request flows, data movement, failures, and operational health.

I used these signals to debug multi-application issues and help engineering teams investigate production behavior more quickly. The dashboards reduced issue diagnosis from hours to minutes, improved post-release follow-up, and gave teams a shared operational view instead of relying on fragmented logs and manual status checks.

## Story 22: TCS Technical Leadership, Mentorship, and Delivery Discipline

I guided a nine-developer team for more than two years, directly mentored five junior engineers, and delivered technical sessions for more than forty junior developers. The sessions covered code review, object-oriented design, design patterns, Java and Spring Boot practices, API design, debugging, Agile delivery, SDLC, and production-release discipline.

I used code reviews, design guidance, release coordination, and stakeholder communication to improve team delivery without holding a people-manager title. This work strengthened onboarding, design consistency, code quality, and production readiness across a multi-application portfolio, and I received more than three recognitions for coding practice and delivery quality.

## Story 23: Global Health Impact Data Pipeline

At Global Health Impact, I worked on a six-engineer research platform that analyzed how pharmaceutical interventions affected disease burden across tuberculosis, malaria, HIV/AIDS, and neglected tropical diseases. I led data-processing work that transformed raw WHO and research data from CSV and Excel sources into validated datasets for analytics, dashboards, APIs, and machine-learning workflows.

I built Python data pipelines with pandas and NumPy to extract disease, drug, country, and health-impact data; standardize inconsistent formats; handle missing or invalid values; and identify malformed records, duplicate values, inconsistent names, missing fields, and invalid numeric values before data moved downstream. I loaded validated records into PostgreSQL, MySQL, and MongoDB according to the query, reporting, and flexible-document needs of each workflow.

The pipeline processed more than ten million weekly health records and reduced manual data preparation by 90%. It replaced spreadsheet-heavy preparation with repeatable ingestion, validation, storage, and analysis workflows so researchers could spend more time interpreting results and less time cleaning source files.

## Story 24: Global Health Impact Backend APIs and Research Integrations

I built RESTful Python backend services that exposed validated health data, research parameters, dashboard analytics, and model outputs through consistent API contracts. The services connected processed data to frontend applications and downstream research workflows, allowing researchers and approved external integrations to use reusable backend endpoints instead of receiving one-off spreadsheet exports.

I implemented API validation and testing with Postman, debugged data-processing and API issues, used Git and GitLab for collaboration and release management, and supported GCP deployment. I structured the backend as reusable service components and built microservice-style integration paths for sharing data with other applications or external users. RBAC protected approved workflows, and backend validation reduced invalid requests before they could affect research data.

## Story 25: Global Health Impact Research Dashboard and Visualization

I developed React, JavaScript, HTML, and CSS dashboards that connected researchers to processed health data, backend APIs, model outputs, historical trends, graphs, and interactive world-map views. The interface supported disease, drug, country, year, and parameter selection with validation feedback and responsive updates, giving users one application for research tasks that had previously required multiple spreadsheets and disconnected data sources.

I integrated the frontend with REST APIs to retrieve dynamic data and display country-level information across more than 150 countries. Role-based access control limited the application to approved users, while frontend and backend validation helped protect research workflows from invalid actions. The dashboard reduced reporting and query work from hours to approximately 30 seconds and gave researchers a faster way to compare country-level results and intervention data.

## Story 26: Global Health Impact Machine Learning and Prediction Integration

I prepared machine-learning datasets from validated WHO and research records by standardizing categorical values, handling missing or invalid data, preparing numerical inputs, and aligning disease, drug, country, and time-based features. I separated data-preparation logic from model logic so the team could rerun processing, retrain models, and validate output quality as source data changed.

I led the development of Python-based prediction workflows using model training, K-fold cross-validation, model evaluation, and hyperparameter tuning. The model used disease, drug, country, and health-data inputs to generate country-level disease-impact predictions, and the selected workflow achieved approximately 93% validation accuracy for the defined task.

I integrated validated model outputs into backend APIs, React dashboards, and world-map visualizations so researchers could generate and compare predictions within the application instead of running separate manual analyses. I also supported debugging across the data pipeline, model workflow, backend APIs, and frontend visualization layers. For any resume use, confirm that validation accuracy is the appropriate metric for the final prediction task before presenting the number.

## Story 27: Global Health Impact Stakeholder Delivery

I translated research and stakeholder needs into technical workflows for data ingestion, backend APIs, dashboards, visualizations, and machine-learning features. I worked with backend, frontend, data, and ML contributors to define data inputs, application behavior, reporting needs, country-level analysis requirements, and user feedback loops.

I supported technical discovery, validation, implementation, testing, debugging, documentation, deployment, and end-user delivery across the research platform. I used Cursor and Codex during development and testing while keeping validation and final workflow decisions grounded in the underlying research requirements. The resulting application connected validated data, dashboards, and predictive analysis to the real questions researchers needed to answer.

## Story 28: Academic Software Engineering and Teaching Assistantship

As a Teaching Assistant for Database Systems and Object-Oriented Programming at Binghamton University, I reviewed Java and C++ assignments, evaluated SQL and database projects, and helped students debug code, query correctness, concurrency concepts, design patterns, data structures, and algorithms.

I used the role as academic software-engineering practice by giving technical feedback on object-oriented design, database behavior, query optimization, and implementation decisions. I supported more than 120 students, strengthening my mentoring, code-review, database, debugging, and technical-communication skills.

## Story 29: JobPulse Job Aggregation and Semantic Search Platform

I built JobPulse, a multi-tenant job-aggregation platform that collects job postings from Greenhouse, Lever, and Ashby, normalizes job, skill, company, and location data, and exposes semantic search through a React dashboard and REST APIs. The platform solved the problem of searching disconnected applicant-tracking systems by giving users a single place to discover, compare, and filter roles.

I designed the TypeScript backend with Node.js and Fastify, PostgreSQL and pgvector for structured storage and vector similarity search, Prisma for database access, Redis for caching job lists and search results, and BullMQ workers for asynchronous ingestion, skill extraction, embedding generation, and background processing. I integrated OpenAI APIs to convert unstructured job descriptions into structured skill tags and vector embeddings, allowing natural-language searches to return semantically related jobs instead of relying only on exact phrase matching.

I implemented tenant middleware and tenant-scoped database queries so each tenant had separate job data, filtering behavior, configuration, and Redis cache namespaces. I added Zod request validation, pagination, filtering, health checks, structured logging, error handling, cache TTLs, React and TypeScript dashboard components, Vite, TanStack Query, Tailwind CSS, Docker, and Docker Compose. The result was a controlled multi-service architecture for job search, search-result relevance, and reliable local development across the API, workers, database, cache, and frontend.

## Story 30: FraudSift Transaction Analytics and ML Risk Detection

I built FraudSift, a full-stack financial analytics application that accepted uploaded bank-transaction CSV files, processed them through an asynchronous backend workflow, and returned categorized transactions, anomaly signals, fraud indicators, spending forecasts, and a financial-health score. The product converted raw financial exports into decision-ready views so users could identify unusual activity and spending patterns without manually sorting large transaction files.

I built a Node.js and Express backend for multipart CSV uploads, parsing, asynchronous processing jobs, polling endpoints, API rate limiting, and integration with a separate Python service. The Python FastAPI service exposed health and prediction endpoints and processed raw transaction records in memory with pandas and NumPy for data preprocessing and feature preparation.

I implemented TF-IDF vectorization and Logistic Regression for transaction categorization, IsolationForest for anomaly detection, and Linear Regression for four-week spend forecasting. I also included rules for unusually large transactions, unusual transaction times, abnormal daily transaction volume, merchant-risk scoring, high-risk keyword detection, transaction bursts, and monthly category-drift alerts. A Hugging Face transaction-categorization dataset served as the primary training source, with fallback keyword templates when the external dataset was unavailable. The Node backend translated FastAPI results into dashboard data, and React, TypeScript, and Vite presented categories, flagged activity, forecasts, risk signals, and financial-health insights.

## Story 31: Resume Agent Evidence-Grounded Resume Automation

I built Resume Agent, a Python desktop application that transformed pasted job descriptions and verified candidate evidence into structured resume JSON, recruiter-reviewed output, tailored application responses, LinkedIn outreach drafts, DOCX files, and PDF deliverables. The application addressed a practical risk in resume automation: generated content can introduce unsupported claims unless it is checked against real candidate evidence before final output.

I designed a multi-stage workflow with Python and Tkinter that supported NVIDIA-hosted models through the OpenAI SDK and Claude through the Anthropic SDK. Users could select supported models, configure thinking behavior, and run independent application workflows in separate tabs. The first prompt stage analyzed job descriptions, identified ATS gaps, and generated candidate evidence statements for human review or an automated approval path.

I built a second-stage JSON generation workflow that converted approved evidence into structured resume content, followed by a three-stage final QA process with an audit, evidence-safe repair, and independent validation. I added recruiter-review workflows, application-question generation, recruiter and hiring-manager outreach drafts, artifact logging, per-request folders, cost tracking, request restoration, concurrent execution, cancellation controls, and document-generation workflows. I kept API keys, pipeline configuration, generated resumes, request artifacts, and PDF archives out of version control to support secure local configuration and traceable output management.

## Story 32: JobFill AI Browser Application Automation

I built JobFill AI, a Chrome Manifest V3 extension that scans job-application pages, identifies form fields, stores candidate profile data locally, uploads saved resumes, and autofills Workday-specific and generic job-application workflows. The extension reduced repetitive application-form work while keeping core profile data, resumes, parsed structures, and user settings in browser-local storage rather than requiring a dedicated backend.

I designed the extension with JavaScript, HTML, CSS, Chrome extension APIs, service workers, content scripts, popup interfaces, and Chrome local storage. I implemented browser-side support for PDF, DOC, DOCX, TXT, and LaTeX resumes, including parsing supported LaTeX files into structured contact details, skills, work history, education, projects, and summary data. The application converted work experience and education into date-aware structures for multi-page Workday forms.

I implemented dedicated Workday automation for personal information, education, skills, work history, resume upload, LinkedIn fields, disclosure pages, custom questions, and signature steps. Generic fallback logic used text labels, placeholders, field names, and input types when a page did not match a known workflow. I added optional Anthropic Claude integration for free-response questions, built candidate context from locally stored resume data, generated suggested answers, and required user review before applying output. Configurable default-answer mappings handled recurring questions without requiring changes to the core form-fill engine.

## Story 33: Bistro AI Structured Restaurant Ordering Application

I built Bistro AI, a full-stack restaurant-ordering application that combined a mobile-first ordering interface, PostgreSQL-backed menu and order workflows, REST APIs, and an AI waiter that translated natural-language requests into structured cart actions. The application let users describe an order in normal language while keeping cart changes bounded to validated operations rather than free-form text.

I developed the backend with TypeScript, Node.js, Express, Prisma, and PostgreSQL. The API supported health checks, menu retrieval, category filtering, order creation, recent-order retrieval, one-shot AI parsing, and multi-turn AI chat. Zod validation checked AI and API request structures, while typed `ADD`, `REMOVE`, and `UPDATE_QTY` actions allowed the AI workflow to return safe, structured cart changes that the frontend could apply to application state.

I integrated Anthropic Claude into the API layer for natural-language order interpretation and implemented layered caching to reduce repeated model calls. The backend used disk and memory caching with configurable TTLs, while the mobile application used in-memory per-session caching. I added timeouts and retry settings to improve external-model-call resilience, then built the client with Expo, Expo Router, React Native, TypeScript, Zustand stores, and shared types. The application supported menu browsing, cart management, tax estimation, checkout, recent orders, AI chat, action-based updates, and order-status display. I containerized the API and PostgreSQL services with Docker and Docker Compose, added an Nginx-backed web demo flow, and supported local mobile testing through Expo Go.

## Story 34: Project Development Workflow

Across my personal projects, I used Cursor, Codex, Claude Code, and Git to support implementation, debugging, testing, and iteration. I used these tools to accelerate development work while retaining responsibility for system design, validation, test results, and final technical decisions.

## Personal Project Selection Metadata

Use the detailed project stories above as factual evidence. This section decides whether a project is eligible for a specific resume. A project name, repository, language, or dependency list alone is not evidence.

### Global Project Rules

1. Select a maximum of two projects.
2. Select the two closest projects when two safe, role-relevant project slices exist.
3. Do not omit a project merely because Experience already proves the same language, database, API pattern, or workflow.
4. Evaluate the usable slice of each project, not the entire repository stack. Many projects include backend, frontend, data, automation, and AI pieces.
5. A project may reinforce a qualification only when it proves a different system context, user workflow, or supporting capability.
6. Each selected project bullet must show what was built, how it worked, project context, and a plain-language reason it mattered.
7. For Backend and Fullstack resumes, remove AI, ML, model, inference, RAG, embedding, semantic search, LLM, OpenAI, agent, prediction, and evaluation language unless the JD explicitly asks for it.
8. Do not reject a mixed-stack project solely because an unused slice contains frontend, backend, AI, ML, or a secondary language.
9. Do not select a project from this section unless its detailed story above verifies the claim.
10. Do not use a project only to fill the projects array. Use it because it is the closest truthful support for the JD.
11. Do not use more than one database, cloud provider, framework, or language in a bullet unless each is relevant to the JD and necessary to explain the work.

### Project P01: JobPulse

Primary stack: TypeScript, Node.js, Fastify, PostgreSQL, Redis, BullMQ, React, Docker Compose.

Best fit: Backend Node.js, Fullstack, AI Engineer, Forward Deployed Engineer, backend API/database/search workflow roles, and roles asking for REST APIs, PostgreSQL, Redis, async processing, validation, logging, Docker, or multi-service architecture.

Use cautiously for Python-only, Java-only, or C#/.NET-only Backend roles: do not present Node.js or TypeScript as the primary qualification, but the project may be selected when its API, PostgreSQL, Redis, BullMQ, validation, logging, tenant-isolation, or Docker evidence is one of the two closest supports for the JD.

Non-AI resume variant: Focus only on Fastify REST APIs, PostgreSQL storage, Redis caching, BullMQ workers, tenant isolation, request validation, logging, health checks, and Docker Compose. Remove semantic-search and AI language.

### Project P02: FraudSift

Primary stack: Python, FastAPI, pandas, NumPy, Node.js, Express, React, TypeScript.

Best fit: ML Engineer, AI Engineer, Python data-processing roles, financial analytics roles, backend upload-processing roles, and jobs asking for FastAPI, CSV processing, pandas, NumPy, asynchronous jobs, API polling, rate limiting, or dashboard-ready data.

Use cautiously for Backend or Fullstack resumes that do not request AI or ML: remove model, prediction, anomaly, and forecasting claims, then use only CSV upload, Python FastAPI processing, pandas/NumPy preprocessing, Node.js API orchestration, polling, rate limiting, and dashboard data if those are JD-relevant.

### Project P03: Resume Agent

Primary stack: Python, Tkinter, structured JSON generation, validation, concurrent workflows, document generation, local configuration management.

Best fit: AI Engineer, AI tooling, developer productivity, Forward Deployed Engineer, or Python automation roles.

Conditional fit: Backend Python only when the JD values workflow automation, structured data handling, internal tools, validation, or concurrent task execution.

Use cautiously for traditional API-first Backend roles when stronger direct API or database project evidence is available. It may still be selected as the second project when Python workflow automation, structured JSON validation, review checkpoints, concurrency, document generation, or local configuration management is the closest remaining support for the JD.

Non-AI resume variant: Focus on Python workflow orchestration, structured JSON validation, review checkpoints, artifact organization, concurrent execution, cancellation handling, document generation, and local secret management.

### Project P04: JobFill AI Extension

Primary stack: JavaScript, HTML, CSS, Chrome Manifest V3, service workers, content scripts, Chrome storage, browser-side parsing.

Best fit: Fullstack, Frontend, Forward Deployed Engineer, browser automation, and workflow automation roles.

Use cautiously for Backend-only roles unless the JD values automation, integrations, workflow tools, form processing, document parsing, browser APIs, or client-side workflow design.

Non-AI resume variant: Focus on form detection, local storage, configurable mappings, document parsing, Workday workflows, generic fallback logic, and user-reviewed autofill.

### Project P05: Bistro AI

Primary stack: TypeScript, Node.js, Express, Prisma, PostgreSQL, REST APIs, Zod, Docker, React Native.

Best fit: Backend Node.js, Fullstack, mobile product engineering, AI Engineer roles, and jobs asking for REST APIs, PostgreSQL, Prisma, validation, caching, retries, Docker, menu/order workflows, or product-facing API design.

Use cautiously for Python-only, Java-only, or C#/.NET-only Backend roles: do not present Node.js or TypeScript as the primary qualification, but the project may be selected when its REST API, PostgreSQL, Prisma, Zod validation, caching, retry, Docker, or order-workflow evidence is one of the two closest supports for the JD.

Non-AI resume variant: Focus on Express APIs, PostgreSQL menu and order workflows, Prisma data access, Zod validation, health checks, caching, retries, Docker Compose, and mobile checkout flows.

### New GitHub Repository Gate

A repository not listed above may become eligible only when Story_GPT contains a factual project record with all of the following:

* Project name
* Actual stack
* What was built
* How the system worked
* User or workflow context
* Plain-language reason it mattered
* Role fit
* Roles or stacks for which it must not be selected
* AI and ML exclusion guidance when needed

Do not select repositories from a project name, README-only claim, dependency file, or assumed architecture.
