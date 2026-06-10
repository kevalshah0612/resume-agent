# Keval Shah Story Bank - Clean Version
## Evidence-only source of truth for JD-driven resume generation

Purpose:
This file stores authenticated evidence for JD-driven resume tailoring. It is not final resume wording.
The resume prompt must select only the stories that match the JD.

Core rule:
JD decides what matters. Story decides what is allowed.

Do not invent:
- tools, metrics, users, outcomes, domains, roles, dates, project claims, leadership scope, or architecture ownership
- dollar amounts in final resume output
- direct domain experience when evidence is only adjacent

Evidence labels:
- HIGH = system + technology + action + scope/metric/outcome
- MEDIUM = professional use confirmed but metric, exact scope, or outcome is incomplete
- LOW = exposure or limited detail
- CANNOT = not enough proof to use

Resume-use labels:
- P1 = production experience proof
- P2 = project proof
- P3 = current-run Des proof
- P4 = skill only
- P5 = cannot defend

---

# 1. Locked profile

Name:
Keval Shah

Contact:
New York, NY | (607) 235-1181 | keval.shah61298@gmail.com | linkedin.com/in/keval-shah0612 | github.com/kevalshah0612

LinkedIn:
https://www.linkedin.com/in/keval-shah0612

GitHub:
https://github.com/kevalshah0612

Education:
1. Binghamton University, State University of New York
   - Master of Science, Computer Science (AI Specialization), GPA: 4.00
   - Binghamton, NY
   - Jan 2025 - May 2026

2. Gujarat Technological University
   - Bachelor of Engineering, Computer Engineering, GPA: 3.85
   - Ahmedabad, India
   - Aug 2016 - Sep 2020

Professional experience:
1. Global Health Impact
   - Software Engineering Intern
   - New York, NY
   - Jun 2025 - Aug 2025

2. Tata Consultancy Services
   - Software Engineer II
   - Client: Wabtec Corporation (Fortune 500)
   - Gandhinagar, India
   - Oct 2022 - Dec 2024

3. Tata Consultancy Services
   - Software Engineer
   - Client: Wabtec Corporation (Fortune 500)
   - Gandhinagar, India
   - Mar 2021 - Sep 2022

Projects:
1. JobPulse
   - https://github.com/kevalshah0612/jobpulse

2. FraudSift
   - https://github.com/kevalshah0612/fraudsift

3. ReviewBot
   - https://github.com/kevalshah0612/reviewbot

4. FilingQuery
   - https://github.com/kevalshah0612/filingquery

5. EvalTrace
   - https://github.com/kevalshah0612/evaltrace

---

# 2. Master technology index

Use this index only for evidence lookup. Do not automatically place every term in the resume.

## Languages

Java:
- TCS1-API-DATA
- TCS1-CICD
- TCS2-JAVA-CONCURRENCY
- TCS2-SECURITY-IDENTITY
- PROJ-JOBPULSE

Python:
- TCS2-CLOUD-PLATFORM
- TCS2-OBSERVABILITY
- TCS-OPERATIONS-AUTOMATION
- TCS-CICD-RUBY-GITLAB-AUTOMATION
- GHI-PIPELINE
- PROJ-FRAUDSIFT
- PROJ-FILINGQUERY
- PROJ-EVALTRACE

JavaScript:
- TCS2-FRONTEND
- TCS2-OBSERVABILITY
- GHI-DASHBOARD
- PROJ-JOBPULSE

TypeScript:
- TCS2-FRONTEND
- TCS2-OBSERVABILITY
- PROJ-JOBPULSE

C#:
- TCS-CSHARP-DOTNET
- Use when JD asks C#, .NET, Microsoft stack, enterprise apps, internal tools, APIs, or custom UI

.NET:
- TCS-CSHARP-DOTNET
- Use as .NET / C# professional experience only when JD asks Microsoft stack or .NET

Ruby:
- TCS-CICD-RUBY-GITLAB-AUTOMATION
- Use when JD asks Ruby, scripting, CI/CD automation, GitLab, developer productivity, release engineering, or internal tools

C++:
- TCS2-JAVA-CONCURRENCY
- TCS-LOW-LEVEL-SYSTEMS
- EDU-TA
- Use for performance, memory management, file processing, OOP, or systems-adjacent roles

C:
- TCS2-JAVA-CONCURRENCY
- TCS-LOW-LEVEL-SYSTEMS
- Use only for systems/performance/support wording, not compiler/kernel ownership unless current-run Des gives exact proof

## Frontend

React:
- TCS2-FRONTEND
- TCS2-OBSERVABILITY
- GHI-DASHBOARD
- PROJ-JOBPULSE
- PROJ-FRAUDSIFT

Angular:
- TCS2-FRONTEND

HTML / CSS:
- TCS2-FRONTEND
- GHI-DASHBOARD

Bootstrap:
- TCS2-FRONTEND

Material UI:
- TCS-UIUX
- Use as Material UI or design-system implementation only
- Do not claim Google Material Design principles unless current-run Des confirms

UI/UX implementation:
- TCS-UIUX
- TCS-CSHARP-DOTNET
- GHI-DASHBOARD
- Use for custom UI, dashboards, role-based workflows, and internal tools
- Do not claim user research unless current-run Des confirms

## Backend / APIs / Identity

REST APIs:
- TCS1-API-DATA
- TCS2-SECURITY-IDENTITY
- GHI-API

Spring Boot:
- TCS1-API-DATA
- TCS2-SECURITY-IDENTITY
- PROJ-JOBPULSE

Spring Security:
- TCS2-SECURITY-IDENTITY
- TCS-SAST-QUALITY

Microservices / service-to-service communication:
- TCS1-API-DATA
- TCS2-CLOUD-PLATFORM
- TCS2-JAVA-CONCURRENCY

API Gateway:
- TCS1-API-DATA
- TCS2-CLOUD-PLATFORM

Redis:
- TCS1-API-DATA
- PROJ-JOBPULSE

OAuth 2.0 / OIDC / JWT / SSO:
- TCS2-SECURITY-IDENTITY
- TCS-AUTH-STORAGE

OKTA:
- TCS-AUTH-STORAGE
- Use when JD asks identity, Okta, enterprise authentication, IAM, SSO, OIDC, or access control

RBAC:
- TCS2-SECURITY-IDENTITY

TLS/SSL:
- TCS2-SECURITY-IDENTITY
- TCS1-LINUX-MIGRATION

## Data / Storage

SQL:
- TCS1-API-DATA
- TCS-DATABASES
- GHI-PIPELINE

MySQL:
- TCS1-API-DATA
- TCS-DATABASES

Oracle:
- TCS-DATABASES

Microsoft SQL Server / Microsoft database:
- TCS-DATABASES

NoSQL:
- TCS1-API-DATA
- TCS-DATABASES
- GHI-PIPELINE

PostgreSQL:
- GHI-PIPELINE
- PROJ-JOBPULSE
- PROJ-FILINGQUERY
- PROJ-FRAUDSIFT

MongoDB:
- GHI-PIPELINE

AWS S3:
- TCS-AUTH-STORAGE
- Use when JD asks AWS storage, object storage, file processing, or backend storage

Microsoft SharePoint:
- TCS2-SECURITY-IDENTITY
- TCS2-JAVA-CONCURRENCY
- TCS-AUTH-STORAGE
- Use for file storage, authentication incident, enterprise document/file workflows

## Cloud / Infrastructure / Operations

AWS:
- TCS2-CLOUD-PLATFORM
- TCS1-LINUX-MIGRATION
- TCS1-API-DATA
- TCS-AUTH-STORAGE
- GHI-API

Azure:
- TCS2-CLOUD-PLATFORM
- TCS1-LINUX-MIGRATION

Google Cloud / GCP:
- TCS2-CLOUD-PLATFORM

Docker:
- TCS2-CLOUD-PLATFORM
- TCS1-CICD
- TCS-OPERATIONS-AUTOMATION
- PROJ-FRAUDSIFT
- PROJ-FILINGQUERY

Kubernetes:
- TCS2-CLOUD-PLATFORM
- TCS1-CICD
- TCS-OPERATIONS-AUTOMATION

Red Hat OpenShift:
- TCS2-CLOUD-PLATFORM
- TCS1-CICD

Terraform:
- TCS2-CLOUD-PLATFORM
- TCS1-LINUX-MIGRATION

Linux:
- TCS1-LINUX-MIGRATION
- TCS2-CLOUD-PLATFORM
- TCS-LOW-LEVEL-SYSTEMS

Bash / Shell scripting:
- TCS1-LINUX-MIGRATION
- TCS1-CICD
- TCS2-CLOUD-PLATFORM

Load balancers / Security groups:
- TCS2-CLOUD-PLATFORM
- TCS1-LINUX-MIGRATION
- Use for cloud operations, deployments, and environment support
- Do not claim network architecture ownership unless current-run Des confirms

Non-production and production environments:
- TCS1-CICD
- TCS2-CLOUD-PLATFORM
- TCS-OPERATIONS-AUTOMATION
- TCS-OWNERSHIP-LEADERSHIP

## Quality / Delivery / Collaboration

Git:
- TCS1-CICD
- TCS-CICD-RUBY-GITLAB-AUTOMATION
- TCS-OWNERSHIP-LEADERSHIP
- PROJ-REVIEWBOT
- PROJ-EVALTRACE

Version control:
- TCS1-CICD
- TCS-CICD-RUBY-GITLAB-AUTOMATION
- TCS-OWNERSHIP-LEADERSHIP

GitLab:
- TCS1-CICD
- TCS-CICD-RUBY-GITLAB-AUTOMATION

GitLab CI/CD:
- TCS1-CICD
- TCS-CICD-RUBY-GITLAB-AUTOMATION

Jenkins:
- TCS1-CICD

GitHub Actions:
- TCS1-CICD
- PROJ-REVIEWBOT
- PROJ-EVALTRACE

Automated testing / test gates:
- TCS1-CICD
- PROJ-EVALTRACE
- PROJ-REVIEWBOT

Datadog:
- TCS2-OBSERVABILITY

CloudWatch:
- TCS2-OBSERVABILITY

Observability / telemetry dashboards:
- TCS2-OBSERVABILITY
- TCS-OPERATIONS-AUTOMATION

Production debugging:
- TCS2-SECURITY-IDENTITY
- TCS2-OBSERVABILITY
- TCS1-API-DATA
- TCS1-LINUX-MIGRATION

SAST / Polaris / Black Duck:
- TCS-SAST-QUALITY

Rally:
- TCS-OWNERSHIP-LEADERSHIP
- Use for Agile tracking, stakeholder delivery tracking, and release planning

Code reviews:
- TCS-OWNERSHIP-LEADERSHIP
- TCS1-CICD
- EDU-TA
- PROJ-REVIEWBOT

Design reviews / documentation:
- TCS-OWNERSHIP-LEADERSHIP
- TCS-DOCUMENTATION

Stakeholder communication:
- TCS-CLIENT-COMMUNICATION
- TCS-OWNERSHIP-LEADERSHIP

Mentoring / junior developer guidance:
- TCS-OWNERSHIP-LEADERSHIP
- EDU-TA

---

# 3. Locked metric and scope table

Use metrics only with the matching evidence block.

| Metric / scope | Evidence block | Allowed use |
|---|---|---|
| 10,000+ enterprise users | TCS2-SECURITY-IDENTITY, TCS2-JAVA-CONCURRENCY | authentication, access, large-file upload, enterprise reliability |
| 48 hours / 2 days | TCS2-SECURITY-IDENTITY | Microsoft SharePoint authentication production incident |
| 60 seconds to 10 seconds | TCS2-JAVA-CONCURRENCY | large 3D file upload or transfer time |
| 83% reduction | TCS2-JAVA-CONCURRENCY | derived from 60 seconds to 10 seconds |
| 40 to 50 seconds saved per file | TCS2-JAVA-CONCURRENCY | large 3D file upload |
| 5 member team | TCS2-JAVA-CONCURRENCY | multithreaded Java upload feature |
| 9 developer team | TCS-OWNERSHIP-LEADERSHIP, TCS1-CICD | team guidance, release delivery, development workflow |
| 5 junior developers | TCS-OWNERSHIP-LEADERSHIP | mentoring, technical guidance |
| 40+ production releases | TCS1-CICD, TCS-OWNERSHIP-LEADERSHIP | production delivery, CI/CD, SDLC |
| 40+ production-ready code deployments | TCS-OWNERSHIP-LEADERSHIP | delivery quality and ownership |
| 7+ applications | TCS1-CICD, TCS1-LINUX-MIGRATION, TCS-OWNERSHIP-LEADERSHIP | release automation, migration, application ownership |
| 10+ applications | TCS-CICD-RUBY-GITLAB-AUTOMATION, TCS1-LINUX-MIGRATION, TCS-OPERATIONS-AUTOMATION | CI/CD, migration, dashboards, automation |
| 10 enterprise applications | TCS2-SECURITY-IDENTITY, TCS2-CLOUD-PLATFORM | RBAC, cloud automation, operational workflows |
| 22% reduction | TCS2-SECURITY-IDENTITY | access-request ticket reduction |
| 30% improvement | TCS-CSHARP-DOTNET, TCS-OPERATIONS-AUTOMATION, TCS2-CLOUD-PLATFORM | API/admin panel performance, team performance, infrastructure overhead |
| 95% reduction | TCS-CICD-RUBY-GITLAB-AUTOMATION | manual deployment time reduction |
| 90% reduction | TCS-OPERATIONS-AUTOMATION, GHI-PIPELINE | manual health checks / data preparation |
| 3 connected applications | TCS2-OBSERVABILITY | monitoring, telemetry, API dashboards |
| hours to minutes | TCS2-OBSERVABILITY | incident diagnosis or triage |
| 3 Java/Spring Boot applications | TCS1-API-DATA | REST API integration and data consistency |
| 9 engineering teams | TCS1-API-DATA | independent deployments and data consistency |
| 2 months | TCS1-API-DATA | Java 11 rebuild and Redis caching |
| zero downtime | TCS1-CICD, TCS1-LINUX-MIGRATION | releases or migrations |
| 3+ client appreciations | TCS-AWARDS | quality recognition |
| 150+ countries | GHI-API | disease burden API queries |
| hours to 30 seconds | GHI-API | reporting turnaround |
| 6 research teams | GHI-DASHBOARD | React dashboard replacing spreadsheet exports |
| 10M+ weekly WHO health records | GHI-PIPELINE | backend data processing |
| 10,000+ job postings | PROJ-JOBPULSE | job ingestion |
| 22,000+ transactions | PROJ-FRAUDSIFT | transaction analysis |
| 5,000+ SEC filings | PROJ-FILINGQUERY | document search / RAG |
| 23% to 4% | PROJ-EVALTRACE | hallucination reduction |
| 120+ students | EDU-TA | teaching assistant work |

Forbidden in final resume:
- Do not mention dollar values
- Do not mention product financial value
- Do not invent exact savings beyond allowed non-dollar metrics

---

# 4. TCS evidence blocks

## TCS-OWNERSHIP-LEADERSHIP

Role:
Tata Consultancy Services, Software Engineer / Software Engineer II

Confidence:
HIGH

Supported JD terms:
ownership, leadership, end-to-end development, code reviews, design reviews, mentoring, SDLC, Agile, Rally, production delivery, stakeholder communication, technical decision-making, documentation, production releases

Facts:
- Guided a 9 developer team over 2+ years
- Mentored and guided 5 junior developers during TCS Software Engineer II period
- Delivered 40+ production releases for Wabtec Corporation applications
- Had 40+ production-ready code deployments across multiple enterprise applications
- Took ownership of stakeholder meetings, requirements understanding, design decisions, development planning, documentation, QA support, and production delivery when tied to selected technical story
- Used Rally to track development, sprint work, requirements, and delivery progress
- Reviewed code and coding practices for junior developers
- Took technical sessions for junior developers
- Received 3+ client or HR appreciations for coding practice and delivery quality

Best use:
Mid-level SWE, backend, full-stack, platform, DevOps, leadership, ownership, client-facing, code review, documentation, Agile/SDLC roles

Limits:
- Do not claim formal engineering manager role
- Do not claim people-manager title
- Do not claim product owner title
- Do not claim formal architect title
- Use “guided,” “led development,” “coordinated,” or “owned delivery” only when the selected system story supports it

---

## TCS-CLIENT-COMMUNICATION

Role:
TCS / Wabtec Corporation client work

Confidence:
HIGH

Supported JD terms:
stakeholder communication, client communication, vendor collaboration, cross-functional collaboration, requirements, technical discussions, production incident response, design decisions

Facts:
- Communicated with US client Wabtec Corporation during feature delivery and production support
- Participated in stakeholder meetings for requirements, technical decisions, status, and delivery planning
- Worked with Microsoft engineers during Microsoft SharePoint authentication production failure
- Worked with Amazon engineers during Amazon Linux migration and package dependency resolution
- Supported client-facing delivery across multiple enterprise applications

Best use:
Roles requiring stakeholder collaboration, production ownership, client-facing engineering, incident response, requirement translation, and design alignment

Limits:
- Do not write generic collaboration bullets
- Pair communication with a technical system, decision, or outcome

---

## TCS-CSHARP-DOTNET

Role:
Tata Consultancy Services

Confidence:
HIGH for professional use of C#/.NET across TCS enterprise applications
MEDIUM for exact per-application scope unless current-run JD needs more detail

Supported JD terms:
C#, .NET, Microsoft stack, enterprise applications, backend APIs, frontend/backend development, custom UI, admin panel, internal tools, performance improvement

Facts:
- Used C# and .NET during TCS enterprise application work
- Worked across frontend and backend areas for multiple TCS applications
- Built or enhanced enterprise admin panel features and custom UI workflows
- Improved API or application/admin-panel performance by 30% when using the C#/.NET/admin-panel story
- Integrated custom UI workflows with backend APIs and enterprise application logic

Best use:
C#/.NET roles, Microsoft stack roles, full-stack roles, admin panels, enterprise internal tools, API performance, custom UI

Limits:
- Do not claim .NET Core, ASP.NET MVC, WPF, WinForms, or Blazor unless current-run Des confirms
- Do not claim ownership of all C#/.NET applications unless current-run Des confirms exact scope
- Do not lead with C# unless JD prioritizes C#/.NET or Microsoft stack

---

## TCS-CICD-RUBY-GITLAB-AUTOMATION

Role:
Tata Consultancy Services

Confidence:
HIGH

Supported JD terms:
Ruby, Git, version control, GitLab, GitLab CI/CD, CI/CD pipelines, release automation, deployment automation, scripting, developer productivity, internal tools, DevOps, platform engineering

Facts:
- Used Git and version control in TCS development and release workflows
- Used GitLab and GitLab CI/CD across enterprise application delivery
- Created GitLab CI/CD pipelines from scratch for more than 10 applications
- Used Ruby scripts in custom GitLab / CI/CD automation workflows
- Reduced manual deployment time by 95%
- Created automated release/deployment workflows that supported consistent production delivery
- Used CI/CD automation with testing and deployment checks before release
- Improved team performance by 30% when paired with automation and workflow standardization story

Best use:
DevOps, platform, backend, full-stack, release engineering, developer productivity, CI/CD, GitLab, Git, Ruby scripting roles

Limits:
- Do not claim company-wide CI/CD ownership
- Do not claim formal release manager title
- Do not use Ruby as a primary backend language unless JD asks and the bullet clearly says scripting/automation

---

## TCS-OPERATIONS-AUTOMATION

Role:
Tata Consultancy Services

Confidence:
HIGH

Supported JD terms:
Python, automation, monitoring, health checks, developer notifications, operational dashboards, cloud operations, server management, Docker, Kubernetes, AWS, infrastructure optimization

Facts:
- Created Python automation scripts to monitor system health and notify developers
- Reduced manual health-check or manual verification effort by 90%
- Automated server cleanup workflows across enterprise applications
- Created dashboards to manage or monitor applications and server details across environments
- Built a dashboard workflow where applications could be selected or dragged/dropped and bound to AWS details for operational visibility
- Rebuilt or refreshed servers using Docker and Kubernetes workflows
- Managed non-production servers and supported production environment workflows
- Supported cloud cleanup and operational automation that reduced infrastructure overhead by 30%

Best use:
Cloud, DevOps, platform, SRE-adjacent, automation, Python, monitoring, internal tools, operational dashboards, production support

Limits:
- Do not claim full SRE ownership unless current-run Des confirms on-call ownership
- Do not claim Kubernetes cluster administration unless current-run Des confirms
- Do not claim exact cloud cost dollar savings in final resume

---

## TCS-AUTH-STORAGE

Role:
Tata Consultancy Services

Confidence:
HIGH for SharePoint authentication and enterprise storage workflows
MEDIUM for Okta/OIDC exact scope unless JD requires detailed identity proof

Supported JD terms:
AWS S3, SharePoint, authentication, custom authentication, Okta, OIDC, OAuth 2.0, SSO, access control, storage, enterprise file workflows, identity integration

Facts:
- Used Microsoft SharePoint for enterprise file storage and large 3D file workflows
- Used AWS S3 in TCS storage/application workflows
- Built or supported custom authentication across multiple enterprise applications
- Used Okta authentication and OIDC authentication in multiple applications
- Worked with OAuth 2.0, JWT, SSO, TLS/SSL, and Spring Security concepts in access-control workflows
- Supported authentication for APIs and application flows across existing and upcoming clients

Best use:
Identity, backend, platform, cloud storage, enterprise SaaS, file processing, access control, C#/.NET Microsoft ecosystem, AWS roles

Limits:
- Do not claim IAM administrator role
- Do not claim Okta admin ownership unless current-run Des confirms
- Do not claim compliance ownership
- Do not claim payment or healthcare identity domain unless JD and evidence support adjacency

---

## TCS-LOW-LEVEL-SYSTEMS

Role:
Tata Consultancy Services

Confidence:
MEDIUM to HIGH for C/C++ memory/performance support around 3D file processing
LOW for kernel-level ownership unless current-run Des gives exact details

Supported JD terms:
C, C++, memory management, low-level systems, systems programming, file processing, performance optimization, Linux, server optimization, diagnostics

Facts:
- Used C and C++ in TCS engineering work
- Used C++ and C in performance-oriented support around large 3D file workflows where files were divided into parts
- Worked on memory management considerations for large 3D files and upload workflows
- Supported system-level Linux/server troubleshooting and performance-oriented diagnostics
- Work was connected to enterprise file processing, server behavior, and backend performance support

Best use:
Systems-adjacent SWE roles, C/C++ roles, performance optimization, large-file processing, Linux/server roles

Limits:
- Do not claim kernel engineering unless current-run Des includes exact kernel module, system call, driver, or kernel debugging proof
- Do not claim compiler, embedded, GPU, or OS internals ownership
- Use “systems-adjacent,” “memory-aware,” or “performance-oriented” unless exact low-level proof is required and supplied

---

## TCS1-API-DATA

Role:
Tata Consultancy Services, Software Engineer, Mar 2021 - Sep 2022

Confidence:
HIGH

Supported JD terms:
Java, Java 11, Spring Boot, REST APIs, microservices, API Gateway, SQL, NoSQL, MySQL, Oracle, Microsoft database, Redis, caching, distributed systems, database integration, service-to-service communication, production reliability

Facts:
- Rebuilt a broken/failing production Java application by upgrading dependencies and moving to Java 11
- Improved throughput using Redis caching
- Restored production readiness within 2 months
- Designed REST API integrations across 3 Java / Spring Boot applications
- Integrated systems using mixed SQL, NoSQL, and MySQL databases
- Enabled user changes in one application to reflect across connected systems
- Enabled 9 engineering teams to deploy independently without data inconsistencies
- Standardized API contracts across Java applications
- Deployed services into AWS infrastructure using CI/CD and Docker

Best use:
Backend, Java, Spring Boot, API, database, microservices, distributed systems, reliability, Redis, SQL/NoSQL, enterprise systems

Limits:
- Do not claim GraphQL, gRPC, or event streaming unless project evidence is used
- Do not claim DBA ownership

---

## TCS1-CICD

Role:
Tata Consultancy Services, Software Engineer, Mar 2021 - Sep 2022

Confidence:
HIGH

Supported JD terms:
Git, version control, GitLab CI/CD, Jenkins, GitHub Actions, CI/CD pipelines, Docker, Kubernetes, OpenShift, Linux, Bash, Shell scripting, automated testing, release automation, deployment automation, zero downtime releases, Agile, SDLC

Facts:
- Standardized CI/CD pipelines with automated test gates across 7+ applications
- Used Git, version control, GitLab CI/CD, Jenkins, and GitHub Actions in delivery workflows
- Enabled 9 developer team to ship 40+ zero-downtime production releases
- Used Docker, Kubernetes, and OpenShift in validation and deployment workflow contexts
- Used Linux and Bash/Shell scripting for automation support
- Supported SDLC and Agile workflows
- Received 3+ client appreciation awards from Wabtec Corporation

Best use:
CI/CD, DevOps, platform, release automation, developer productivity, backend engineering, quality engineering, Agile/SDLC roles

Limits:
- Do not claim sole company-wide CI/CD ownership
- Do not claim formal release manager title

---

## TCS1-LINUX-MIGRATION

Role:
Tata Consultancy Services, Software Engineer

Confidence:
HIGH

Supported JD terms:
Linux, AWS, Azure, Terraform, Bash, Shell scripting, TLS/SSL, load balancing, security groups, package dependencies, cloud operations, migration, server upgrade, standard procedures

Facts:
- Migrated enterprise workloads from CentOS to Amazon Linux 2 across 7+ applications
- Later led Amazon Linux 2 to Amazon Linux 3 upgrade across the unit/applications
- Resolved missing package dependencies across 10+ applications
- Completed migration with zero downtime
- Collaborated with Amazon engineers to debug package dependency issues
- Created standard procedure for future upgrade workflows
- Used Linux, shell scripting, cloud infrastructure, TLS/SSL, load balancing, and security group concepts during migration and validation
- Supported non-production and production environment workflows

Best use:
Linux, cloud migration, infrastructure, platform, backend operations, production support, reliability roles

Limits:
- Do not claim deep network engineering
- Do not claim full cloud architecture ownership unless current-run Des confirms

---

## TCS2-SECURITY-IDENTITY

Role:
Tata Consultancy Services, Software Engineer II, Oct 2022 - Dec 2024

Confidence:
HIGH

Supported JD terms:
OAuth 2.0, OIDC, JWT, SSO, Okta, TLS/SSL, Spring Security, RBAC, authentication, authorization, access control, enterprise security, production debugging, platform reliability

Facts:
- Resolved live Microsoft SharePoint authentication failure after Microsoft changed authentication behavior
- Production issue affected 10,000+ enterprise users
- Restored access within 48 hours / 2 days
- Partnered with Microsoft engineers
- Created custom authentication solution for existing and upcoming clients
- Deployed custom OAuth 2.0 authentication layer
- Supported OIDC and Okta authentication across multiple application flows where relevant
- Designed Spring Security access controls across 10 enterprise applications
- Supported instant role-change synchronization
- Reduced user access support tickets by 22%
- Used JWT, SSO, TLS/SSL, authentication, and authorization concepts

Best use:
Security, identity, backend, platform, cloud, enterprise SaaS, access control, production incident, IAM-adjacent roles

Limits:
- Do not claim SOC, threat intelligence, compliance ownership, or Okta admin ownership
- Do not claim cybersecurity product ownership unless JD allows access-control adjacency

---

## TCS2-JAVA-CONCURRENCY

Role:
Tata Consultancy Services, Software Engineer II

Confidence:
HIGH

Supported JD terms:
Java, C, C++, memory management, concurrency, multithreading, backend services, microservices, performance, scalability, load balancing, caching, large file processing, distributed systems, enterprise reliability

Facts:
- Led a 5 member team on a multithreaded Java upload service
- Designed workflow to upload large 3D files into Microsoft SharePoint in concurrent parts
- Used memory-aware large-file handling and part-based upload design for 3D engineering files
- Used C/C++ in performance-oriented support around file handling, memory management, diagnostics, or server optimization where relevant
- Reduced large 3D file transfer time from 60 seconds to 10 seconds
- Saved 40 to 50 seconds per file upload
- Supported 10,000+ enterprise users
- Improved reliability for high-volume 3D engineering assets
- Used load balancing and service reliability concepts around backend traffic and upload workflows
- Created final documentation and yearly analysis for the feature

Best use:
Backend, distributed systems, Java, concurrency, performance, C/C++, systems-adjacent, large-file processing, platform roles

Limits:
- Do not claim kernel engineering, compiler work, embedded systems, GPU, or OS internals
- Do not mention dollar values or product financial value
- Do not claim formal architecture title

---

## TCS2-CLOUD-PLATFORM

Role:
Tata Consultancy Services, Software Engineer II

Confidence:
HIGH

Supported JD terms:
AWS, Azure, GCP, Docker, Kubernetes, Red Hat OpenShift, Terraform, Linux, Bash, Shell scripting, API Gateway, load balancing, security groups, cloud-native infrastructure, deployment automation, platform operations

Facts:
- Worked across cloud-native enterprise applications using Docker, Kubernetes, Red Hat OpenShift, and cloud platforms
- Used Terraform and scripting for repeatable infrastructure and environment workflows
- Supported API Gateway, load balancing, and security group concepts for backend services and enterprise traffic
- Automated cleanup and operational workflows across 10 enterprise applications
- Reduced infrastructure overhead by 30% across AWS and Google Cloud environments
- Used Azure in TCS cloud/application support contexts
- Managed non-production servers and supported production environment delivery workflows

Best use:
Cloud, platform, DevOps, backend infrastructure, SRE-adjacent, deployment automation, Linux roles

Limits:
- Do not claim full SRE ownership
- Do not claim Kubernetes cluster administration unless current-run Des confirms
- Do not claim cloud architect title

---

## TCS2-OBSERVABILITY

Role:
Tata Consultancy Services, Software Engineer II

Confidence:
HIGH

Supported JD terms:
Datadog, CloudWatch, observability, telemetry dashboards, monitoring, developer notifications, React, TypeScript, JavaScript, API traffic, error alerts, incident response, operational visibility, production debugging

Facts:
- Built or enhanced monitoring dashboards for live API traffic and error alerts
- Used Datadog and CloudWatch observability signals for production systems
- Covered 3 connected applications
- Reduced incident diagnosis time from hours to minutes
- Built React/TypeScript/JavaScript dashboard views where relevant
- Created dashboard views to monitor Datadog signals, user live requests, API health, and data across applications
- Supported developer notifications through automated health-check workflows where relevant

Best use:
Observability, telemetry, platform operations, backend reliability, full-stack internal tools, production debugging

Limits:
- Do not claim full observability platform ownership
- Do not claim SRE ownership unless current-run Des confirms

---

## TCS2-FRONTEND

Role:
Tata Consultancy Services, Software Engineer II

Confidence:
HIGH

Supported JD terms:
Angular, React, JavaScript, TypeScript, HTML, CSS, Bootstrap, Material UI, design systems, custom UI, dashboards, role-based workflows, operational dashboards, REST API integration

Facts:
- Built or enhanced enterprise dashboards and internal web applications
- Used Angular, React, JavaScript, TypeScript, HTML, CSS, Bootstrap, Material UI, and design-system patterns
- Built custom UI workflows for enterprise applications and admin panels
- Integrated frontend workflows with REST APIs and role-based access controls
- Supported dashboard workflows for API health, access, monitoring, and operational issues
- Developed multiple high-usage dashboards across connected applications

Best use:
Full-stack, frontend, Angular, React, custom UI, dashboard, internal tools, enterprise product roles

Limits:
- Do not claim advanced accessibility unless current-run Des confirms
- Do not claim Next.js, Vue, Figma, user research, or frontend architecture ownership unless current-run Des confirms

---

## TCS-SAST-QUALITY

Role:
Tata Consultancy Services

Confidence:
MEDIUM to HIGH

Supported JD terms:
SAST, code quality, vulnerability remediation, security scanning, Polaris, Black Duck, dependency cleanup, secure coding, modernization

Facts:
- Used SAST tools including Polaris and Black Duck
- Monitored code quality and vulnerabilities
- Identified vulnerabilities in existing codebases across 3 applications
- Upgraded codebases using React, Spring, Java, and Spring Security where relevant

Best use:
Security-adjacent SWE, quality, code review, secure development, enterprise modernization

Limits:
- Do not claim SOC, threat detection, compliance ownership, or exact vulnerability count unless current-run Des confirms

---

# 5. Global Health Impact evidence blocks

## GHI-API

Role:
Global Health Impact, Software Engineering Intern

Confidence:
HIGH

Supported JD terms:
AWS, REST APIs, backend services, data APIs, scalable web applications, analytics platforms, global data, healthcare data, research tooling

Facts:
- Built AWS REST API for real-time disease burden queries
- Served disease burden queries across 150+ countries
- Reduced reporting turnaround from hours to 30 seconds
- Supported drug, country, disease, and year based research queries

Best use:
Full-stack, backend, cloud API, analytics platform, healthcare data, research tooling, recent US experience

Limits:
- Do not claim production ownership beyond internship scope
- Do not claim gaming, payments, or Trust & Safety domain

---

## GHI-DASHBOARD

Role:
Global Health Impact, Software Engineering Intern

Confidence:
HIGH

Supported JD terms:
React, JavaScript, HTML, CSS, frontend, dashboards, analytics platforms, data visualization, world map workflow, research tools, UI implementation

Facts:
- Built React research dashboard for disease burden data
- Enabled filtering by drug, country, disease, and year
- Built world map workflow where users could explore country-wise data
- Eliminated manual spreadsheet exports for 6 research teams
- Built UI where users could explore disease-wise data, graphs, countries, drugs, and parameters

Best use:
Full-stack, frontend, dashboard, analytics, research tooling, product-facing roles, recent US experience

Limits:
- Do not claim TypeScript unless current-run Des confirms
- Do not claim enterprise production scale beyond research teams
- Do not claim user research unless current-run Des confirms

---

## GHI-PIPELINE

Role:
Global Health Impact, Software Engineering Intern

Confidence:
HIGH

Supported JD terms:
Python, backend pipelines, CSV processing, PostgreSQL, MongoDB, data extraction, data processing, data modeling, analytics platforms, scalable backend services, WHO health records

Facts:
- Engineered backend pipeline for WHO health records
- Processed 10M+ weekly WHO health records
- Loaded data into PostgreSQL and MongoDB
- Reduced manual data preparation by 90%
- Built CSV extraction scripts for diseases and drugs based on data team inputs
- Supported country, drug, disease, and year based queries

Best use:
Backend, data platform, full-stack, analytics, API, database, healthcare data roles

Limits:
- Do not claim ML model training from this block
- Do not claim independent data science research ownership

---

## GHI-ML

Role:
Global Health Impact, Software Engineering Intern

Confidence:
LOW to MEDIUM

Supported JD terms:
machine learning, prediction, healthcare analytics, country-wise prediction, model-powered dashboard

Facts:
- Team created machine learning models using processed health data
- Model predicted numbers shown country-wise on world map
- Exact algorithm, validation metric, deployment scope, and personal model contribution are not yet specified

Best use:
Use in PASS 1 as a Des request for ML roles

Limits:
- Do not place in final resume unless current-run Des confirms:
  - model type
  - personal contribution
  - prediction target
  - data used
  - validation method or metric
  - deployment or user impact

---

# 6. Project evidence blocks

## PROJ-JOBPULSE

Confidence:
HIGH

Supported JD terms:
Java, Spring Boot, Kafka, PostgreSQL, Redis, pgvector, React, TypeScript, OpenAI API, LLM extraction, job analytics, skill extraction, normalized data models, full-stack platform

Facts:
- Built Kafka pipeline ingesting 10,000+ job postings from 3 sources into PostgreSQL
- Used LLM step to extract structured skills
- Reduced batch processing time from 3 seconds to under 1 second
- Built React and TypeScript analytics dashboard
- Users can compare job demand by skill, location, and company
- Designed PostgreSQL data models for job, company, skill, and location trends
- Unified Kafka ingestion, PostgreSQL storage, Redis, and React visualization

Limits:
- Do not claim production company users unless current-run Des confirms

---

## PROJ-FRAUDSIFT

Confidence:
HIGH

Supported JD terms:
Python, FastAPI, Node.js, Docker, PostgreSQL, scikit-learn, React, fraud detection, anomaly detection, transactions, risk workflows, real-time alerts, monitoring dashboard

Facts:
- Built FastAPI backend processing 22,000+ transactions
- Flagged spending anomalies across 12 categories in real time
- Replaced manual transaction review
- Deployed Dockerized fraud detection service
- Built React dashboard for suspicious transactions, category risk, and account activity
- Integrated FastAPI, Node.js, and Docker services

Limits:
- Do not claim bank production deployment
- Do not claim regulated payment system ownership

---

## PROJ-REVIEWBOT

Confidence:
HIGH

Supported JD terms:
AI-powered code review, GitHub Actions, CI/CD quality gates, pull request automation, LLM explanations, static analysis, developer workflows, security checks, testing checks, AI agents, LangGraph, FastAPI

Facts:
- Built AI-powered code review assistant
- Scans pull requests
- Explains risky changes
- Posts actionable feedback through GitHub Actions before merge
- Designed CI/CD quality gate for security, testing, and relevance checks
- Integrated static analysis, LLM explanations, and CI/CD checks into repeatable developer workflow

Limits:
- Do not claim enterprise deployment unless current-run Des confirms

---

## PROJ-FILINGQUERY

Confidence:
HIGH

Supported JD terms:
Python, LangChain, HuggingFace, pgvector, FastAPI, Docker, RAG, retrieval, SEC filings, financial question answering, citations, semantic search, keyword retrieval

Facts:
- Built document search system over 5,000+ SEC filings
- Answers financial questions with cited sources
- Reduced analyst lookup time from hours to under 30 seconds
- Implemented RAG pipeline with LangChain, pgvector, and PostgreSQL
- Retrieves filing evidence and attaches source citations
- Supports semantic search and keyword retrieval

Limits:
- Do not claim regulated financial advisory system
- Do not claim production analyst team unless current-run Des confirms

---

## PROJ-EVALTRACE

Confidence:
HIGH

Supported JD terms:
Python, DeepEval, LangChain, GitHub Actions, FastAPI, LLM evaluation, hallucination reduction, relevance thresholds, regression testing, RAG pipelines, CI/CD, code quality

Facts:
- Built LLM quality evaluation pipeline
- Runs automated tests through GitHub Actions CI/CD on every pull request
- Reduced hallucination rate from 23% to 4%
- Enforced relevance thresholds that block low-quality LLM changes before merge
- Standardized LLM regression testing and answer quality checks

Limits:
- Do not claim model training
- Do not claim research publication

---

# 7. Education evidence

## EDU-TA

Role:
Teaching Assistant, Binghamton University

Confidence:
HIGH

Supported JD terms:
Java, C++, OOP, code reviews, SQL, database systems, relational databases, non-relational databases, data structures, debugging, mentoring, teaching, lab support, concurrency concepts

Facts:
- Guided 120+ students
- Supported Database Management Systems in Fall semester
- Trained students on database optimization, concurrency, relational and non-relational projects
- Supported Object-Oriented Programming in current semester
- Reviewed code and explained OOP concepts in C++ and Java
- Supported debugging sessions
- Improved submission quality by 30% over one semester

Best use:
Student_entry, internship, Java/C++/DSA/SQL/code-review-heavy entry roles

Limits:
- Do not use TA bullet for mid-level layouts unless JD strongly values teaching, code review, mentoring, or education
- Do not overstate as professional software engineering experience

---

# 8. Role priority guide

## Backend / platform / cloud / DevOps / security

Prefer:
1. TCS2-SECURITY-IDENTITY
2. TCS1-API-DATA
3. TCS2-JAVA-CONCURRENCY
4. TCS-CICD-RUBY-GITLAB-AUTOMATION
5. TCS2-CLOUD-PLATFORM
6. TCS-OPERATIONS-AUTOMATION
7. TCS2-OBSERVABILITY
8. TCS1-CICD
9. TCS1-LINUX-MIGRATION
10. TCS-OWNERSHIP-LEADERSHIP

Use GHI for recent US API/data proof.
Use projects only to fill stack or domain gaps.

## Full-stack / product applications

Prefer:
1. TCS-CSHARP-DOTNET when JD asks C#/.NET
2. TCS1-API-DATA
3. TCS2-FRONTEND
4. TCS2-OBSERVABILITY
5. TCS2-SECURITY-IDENTITY
6. TCS-UIUX
7. GHI-DASHBOARD
8. GHI-API

Use JobPulse or FraudSift only for JD gaps.

## Systems / C++ / performance

Prefer:
1. TCS2-JAVA-CONCURRENCY
2. TCS-LOW-LEVEL-SYSTEMS
3. TCS1-LINUX-MIGRATION
4. TCS2-CLOUD-PLATFORM
5. EDU-TA

Avoid kernel/compiler wording unless current-run Des provides exact proof.

## AI/ML product

Prefer:
1. GHI-PIPELINE
2. GHI-API
3. GHI-DASHBOARD
4. PROJ-FILINGQUERY
5. PROJ-EVALTRACE
6. PROJ-REVIEWBOT
7. PROJ-FRAUDSIFT
8. TCS production engineering proof

## AI platform / MLOps / backend-heavy AI

Prefer:
1. TCS1-CICD
2. TCS2-CLOUD-PLATFORM
3. TCS2-OBSERVABILITY
4. GHI-PIPELINE
5. PROJ-EVALTRACE
6. PROJ-FILINGQUERY
7. PROJ-JOBPULSE

## AI tooling / developer productivity

Prefer:
1. PROJ-REVIEWBOT
2. PROJ-EVALTRACE
3. TCS-CICD-RUBY-GITLAB-AUTOMATION
4. TCS1-CICD
5. TCS2-OBSERVABILITY
6. TCS2-CLOUD-PLATFORM
7. TCS-OWNERSHIP-LEADERSHIP

---

# 9. Must-not-claim list unless current-run Des confirms

Do not claim these unless user provides specific evidence for the current JD:

- Go
- Rust
- Scala
- GraphQL
- gRPC
- WebSockets
- Next.js
- Vue
- mobile iOS/Android
- production ML model ownership
- fine-tuning ownership
- model-serving ownership
- Kubernetes cluster administration
- full SRE/on-call ownership
- SOC/security operations ownership
- threat intelligence
- compliance ownership
- direct gaming systems
- multiplayer/live-service game operations
- payment processor production ownership
- regulated financial advisory system
- kernel engineering ownership
- compiler engineering
- GPU systems
- embedded systems
- Figma
- user research
- accessibility ownership
- Google Material Design principles
- formal engineering manager role
- formal product owner role
- formal architect title
- direct data center operations
- custody chain systems
- Vertex AI
- TPU usage
- Google Global Networking

---

# 10. Resume selection rules

When creating a JD-specific resume:
1. Start with the JD's minimum screen terms
2. Use production evidence first
3. Use GHI for recent US experience and healthcare/data proof
4. Use projects only to fill exact stack or domain gaps
5. Use exact JD words only when the selected story can defend them
6. Keep unsupported terms out of bullets
7. Use skill-only placement for MEDIUM evidence if the JD term is not central
8. If a JD term is central and only MEDIUM/LOW evidence exists, ask for Des
9. Do not put every technology from this file into one resume
10. Keep the resume top third focused on the role thesis

DES suggestion rule:
If the JD requires a term that is partial in this story bank, ask the user with numbered DES suggestions. The user can reply “Apply 1, 2, 3” only if true. Upgrade to HIGH only when the Des includes system, technology, action, and scope/outcome.
