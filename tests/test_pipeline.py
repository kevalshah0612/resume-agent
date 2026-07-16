import asyncio
import json
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import app_properties
import pipeline


EMPTY_USAGE = {
    "input_tokens": 0,
    "output_tokens": 0,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
}


def valid_resume_response(
    recruiter_message: str = "Hi [Name], I applied. Could you point me to the recruiter for this role?",
    hiring_manager_message: str = "Hi [Name], I applied. Is platform reliability a key focus for this hire?",
) -> str:
    return (
        "CONFIDENCE SUMMARY:\n- HIGH\n\n"
        f"Recruiter LinkedIn Message:\n{recruiter_message}\n\n"
        f"Hiring Manager LinkedIn Message:\n{hiring_manager_message}\n\n"
        "Recruiter/HM Search Strings:\n"
        "site:linkedin.com/in recruiter company\n\n"
        "```json\n{\"ok\": true}\n```"
    )


def valid_compact_response() -> str:
    return (
        "FINAL JSON:\n"
        "```json\n"
        "{"
        "\"type\": \"Backend\", "
        "\"level\": \"mid\", "
        "\"experience\": [{\"title\": \"Software Engineer II\", \"company\": \"Tata Consultancy Services\", \"bullets\": [\"Built Java APIs for users.\"]}], "
        "\"projects\": [{\"name\": \"JobPulse\", \"bullets\": [\"Built Fastify APIs for job search.\"]}], "
        "\"technical_skills\": [[\"Languages\", [\"Java\", \"Python\"]], [\"Backend and APIs\", [\"Spring Boot\", \"REST APIs\"]]]"
        "}\n"
        "```"
    )


class LinkedinMessageTests(unittest.TestCase):
    def test_extracts_only_message(self):
        response = valid_resume_response("Hi [Name], concise recruiter message.")
        self.assertEqual(
            pipeline.extract_linkedin_message(response, "recruiter"),
            "Hi [Name], concise recruiter message.",
        )

    def test_hard_limit_shortens_both_messages_and_preserves_search_strings(self):
        response = valid_resume_response("recruiter " * 100, "manager " * 100)
        limited = pipeline.enforce_linkedin_message_limit(response)
        self.assertLessEqual(len(pipeline.extract_linkedin_message(limited, "recruiter")), 300)
        self.assertLessEqual(len(pipeline.extract_linkedin_message(limited, "hiring_manager")), 300)
        self.assertIn("Recruiter/HM Search Strings:", limited)
        self.assertIn("site:linkedin.com/in recruiter company", limited)

    def test_validator_rejects_long_message(self):
        error = pipeline.validate_resume_response(valid_resume_response("x" * 301))
        self.assertIn("maximum is 300", error or "")

    def test_validator_rejects_long_dash(self):
        error = pipeline.validate_resume_response(
            valid_resume_response("I build APIs \u2014 and production systems.")
        )
        self.assertIn("em dash or en dash", error or "")

    def test_recruiter_request_includes_exact_target_identity_and_two_messages(self):
        with (
            patch("pipeline.read_prompt", return_value="prompt"),
            patch("pipeline.call_model", new=AsyncMock(return_value=valid_resume_response())) as call_mock,
        ):
            asyncio.run(
                pipeline.run_recruiter_review(
                    jd="Build secure signing systems.",
                    resume1_json={"ok": True},
                    company="MathWorks",
                    title="Software Engineer - Code Signing",
                )
            )
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("TARGET COMPANY:\nMathWorks", user_text)
        self.assertIn("TARGET TITLE:\nSoftware Engineer - Code Signing", user_text)
        self.assertIn("RECRUITER LINKEDIN MESSAGE", user_text)
        self.assertIn("HIRING MANAGER LINKEDIN MESSAGE", user_text)


class PromptProfileTests(unittest.TestCase):
    def test_default_prompt_profile_is_stable(self):
        self.assertEqual(app_properties.DEFAULT_PROMPT_PROFILE, "stable")

    def test_resume_rules_prefer_local_rules(self):
        rules = pipeline.read_resume_rules()
        self.assertTrue(rules)
        self.assertIn("use Experience evidence first", rules)
        self.assertIn("Projects complement Experience", rules)

    def test_v3_prompt_contract_matches_local_resume_rules(self):
        prompt = pipeline.read_prompt("prompt.md", "v3")
        prompt_short = pipeline.read_prompt("prompt_short.md", "v3")
        hotdog = pipeline.read_prompt("hotdog.md", "v3")
        story = pipeline.read_prompt("Story.md", "v3")

        self.assertIn("PASS 1 - COMPANY + JD PLAN", prompt)
        self.assertIn("PASS 1 Must Print", prompt_short)
        for text in (prompt, prompt_short):
            self.assertIn("PROJECT SELECTION PLAN", text)
            self.assertIn("WHY/CONTEXT + WHAT + HOW + BENEFIT/OUTCOME", text)
            self.assertIn("SKILLS TRACEABILITY PLAN", text)
            self.assertIn("METRIC LEDGER", text)
            self.assertIn("Final JSON Source", text)

        self.assertIn('"max_skills_per_category": 6', prompt)
        self.assertIn('"title": "Teaching Assistant"', prompt)
        self.assertIn("DES candidates are questions, not evidence", prompt)
        self.assertIn("Metric values are protected", prompt)
        self.assertIn("Final resume bullets must not use arrow notation", prompt)
        self.assertIn("same-scope", prompt)
        self.assertIn("HOTDOG REPAIR JSON", hotdog)
        self.assertIn("technical_skills = grouped rows", hotdog)
        self.assertIn("final JSON exactly as printed", hotdog)
        self.assertIn("Project bullet <=28 words", hotdog)
        self.assertIn("# Story.md", story)
        self.assertIn("Java File Ingestion and Status Platform", story)
        self.assertIn("TA Code Review and Review Automation", story)

    def test_v1_short_controller_preserves_existing_bullet_contract(self):
        jd_controller = pipeline.read_prompt("prompt_short_jd.md", "v1")
        mapper_controller = pipeline.read_prompt("prompt_short_mapper.md", "v1")
        composer_controller = pipeline.read_prompt("prompt_short_composer.md", "v1")
        mapper = pipeline.read_prompt("02_Evidence_Mapper_DES_Planner.md", "v1")
        composer = pipeline.read_prompt("03_Evidence_Locked_Resume_Composer.md", "v1")
        self.assertIn("JD_INTELLIGENCE", jd_controller)
        self.assertIn("Do not write resume bullets", jd_controller)
        self.assertNotIn("Preferred engineering and evidence verb bank", jd_controller)
        self.assertNotIn("RESUME_COMPOSITION", jd_controller)
        self.assertIn("EVIDENCE_MAPPING", mapper_controller)
        self.assertIn("Do not write final resume bullets", mapper_controller)
        self.assertNotIn("Preferred engineering and evidence verb bank", mapper_controller)
        self.assertNotIn("RESUME_COMPOSITION", mapper_controller)
        self.assertIn("RESUME_COMPOSITION", composer_controller)
        self.assertIn("Target 18 to 24 words", composer_controller)
        self.assertIn("never accept a bullet above 28 words", composer_controller)
        self.assertIn("no more than three visible JD keyword units", composer_controller)
        self.assertIn("For every bullet, silently repeat this loop", composer_controller)
        self.assertIn("exact supported JD alignment anchor", composer_controller)
        self.assertIn("resume-wide ledger", composer_controller)
        self.assertIn("Exact JD Alignment Anchor Planning", mapper)
        self.assertIn("two or three distinct, evidence-supported action intents", mapper)
        self.assertIn("Preferred opening verbs are unique", mapper)
        self.assertIn("Exact JD Alignment Anchor", composer)
        self.assertIn("Never repeat an opening verb", composer)
        self.assertIn("Draft and validate exactly one bullet at a time", composer)
        self.assertIn("reject and rewrite every bullet above 28 words", composer)
        self.assertIn("Do not open a project result bullet with `Self-tested`", composer)

    def test_v1_short_controller_is_sent_to_all_three_stages(self):
        inp = pipeline.ResumeInput(
            company="Acme",
            title="Backend Engineer",
            jd="Build reliable APIs.",
            words="Boston, MA",
        )
        with patch(
            "pipeline.call_model",
            new=AsyncMock(side_effect=["{}", "{}"]),
        ) as pass1_call:
            asyncio.run(pipeline.run_v1_pass1(inp))

        analyzer_text = pass1_call.await_args_list[0].kwargs["messages"][0]["content"]
        mapper_text = pass1_call.await_args_list[1].kwargs["messages"][0]["content"]
        self.assertIn("RUN MODE: JD_INTELLIGENCE", analyzer_text)
        self.assertIn("RUN MODE: EVIDENCE_MAPPING", mapper_text)
        self.assertIn("# V1 JD Intelligence Stage Controller", analyzer_text)
        self.assertNotIn("Resume Composition Stage Controller", analyzer_text)
        self.assertNotIn("Preferred engineering and evidence verb bank", analyzer_text)
        self.assertIn("# V1 Evidence Mapping Stage Controller", mapper_text)
        self.assertNotIn("Resume Composition Stage Controller", mapper_text)
        self.assertNotIn("Preferred engineering and evidence verb bank", mapper_text)

        pass1_text = json.dumps({"jd_analysis": {}, "evidence_map": {}})
        with patch(
            "pipeline.call_model",
            new=AsyncMock(return_value="{}"),
        ) as composer_call:
            asyncio.run(pipeline.run_v1_pass2(inp, pass1_text, "No DES"))

        composer_text = composer_call.await_args.kwargs["messages"][0]["content"]
        self.assertIn("RUN MODE: RESUME_COMPOSITION", composer_text)
        self.assertIn("# V1 Resume Composition Stage Controller", composer_text)
        self.assertNotIn("JD Intelligence Stage Controller", composer_text)
        self.assertNotIn("Evidence Mapping Stage Controller", composer_text)
        self.assertIsNone(composer_call.await_args.kwargs["output_validator"])
        self.assertEqual(1, composer_call.await_args.kwargs["nvidia_max_attempts_override"])

    def test_v1_short_controller_rejects_unknown_stage(self):
        with self.assertRaisesRegex(ValueError, "Unsupported V1 run mode"):
            pipeline.v1_short_controller("UNKNOWN")


    def test_prompt_profile_options_resolve_to_stable_and_v3(self):
        labels = pipeline.prompt_profile_options()
        self.assertEqual(
            {pipeline.resolve_prompt_profile_label(label) for label in labels},
            {"stable", "v3"},
        )
        self.assertIn("Stable", labels)
        self.assertIn("V3", labels)
        self.assertEqual(pipeline.resolve_prompt_profile_label("v3_experimental_flow"), "v3")
        self.assertEqual(pipeline.resolve_prompt_profile_label("unknown"), "stable")




    def test_v3_pass1_includes_metric_and_keyword_plan_without_python_validator(self):
        with patch("pipeline.call_model", new=AsyncMock(return_value="COMPANY RESEARCH:\n- ok")) as call_mock:
            asyncio.run(
                pipeline.run_pass1(
                    pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs", words="Boston, MA"),
                    prompt_profile="v3",
                )
            )
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("RUN MODE:\nPASS 1 - COMPANY + JD PLAN", user_text)
        self.assertIn("METRIC LEDGER", user_text)
        self.assertIn("SKILLS TRACEABILITY PLAN", user_text)
        self.assertIsNone(call_mock.await_args.kwargs["output_validator"])





    def test_v3_prompt_uses_v3_prompt_story_and_approved_plan_flow(self):
        with patch("pipeline.call_model", new=AsyncMock(return_value=valid_compact_response())) as call_mock:
            asyncio.run(
                pipeline.run_pass2(
                    pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs", words="Boston, MA", des="Use API work"),
                    pass1_text="FULL RESUME COVERAGE\n- Every PRIMARY/SECONDARY keyword placed or explained: YES",
                    approval_text="1,2",
                    prompt_profile="v3",
                )
            )
        system_text = "\n".join(block["text"] for block in call_mock.await_args.kwargs["system_blocks"])
        messages = call_mock.await_args.kwargs["messages"]
        user_text = messages[0]["content"]
        self.assertIn("Evidence-Locked JD Resume Compiler", system_text)
        self.assertIn("# Story.md", system_text)
        self.assertIn("COMPANY RESEARCH:", user_text)
        self.assertIn("RUN MODE:\nPASS 1 - COMPANY + JD PLAN", user_text)
        self.assertIn("COMPANY:\nAcme", user_text)
        self.assertIn("JD:\nBuild APIs", user_text)
        self.assertEqual(messages[1]["role"], "assistant")
        self.assertIn("FULL RESUME COVERAGE", messages[1]["content"])
        self.assertIn("RUN MODE:\nPASS 2 - WRITE APPROVED RESUME JSON", messages[2]["content"])
        self.assertIn("APPROVED DES:", messages[2]["content"])
        self.assertIn("PASS 1 PLAN:", messages[2]["content"])
        self.assertIn("1,2", messages[2]["content"])
        self.assertIsNone(call_mock.await_args.kwargs["output_validator"])


    def test_v3_hotdog_uses_v3_story_rules_and_current_json(self):
        with patch("pipeline.call_model", new=AsyncMock(return_value=valid_compact_response())) as call_mock:
            asyncio.run(
                pipeline.run_recruiter_review(
                    jd="Build APIs",
                    resume1_json={
                        "config": {"type": "backend", "prompt_profile": "v3"},
                        "professional_experience": [{"title": "Software Engineer II", "company": "Tata Consultancy Services", "bullets": ["Designed Java APIs."]}],
                        "projects": [],
                        "technical_skills": {"Backend": "Java, Spring Boot"},
                    },
                    company="Acme",
                    title="Backend Engineer",
                    des="1,2",
                    inp=pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs", words="Boston, MA", des="Use API work"),
                    prompt_profile="v3",
                    pass1_audit="ORDERED EXPERIENCE TARGETS:\nTCS-BACKEND-DATA-WORKFLOW:\nSummary: Java, APIs",
                    resume_generation_process="HOTDOG HANDOFF:\n- TCS B1: keywords=Java, APIs; source=TCS-BACKEND-DATA-WORKFLOW",
                )
            )
        system_text = "\n".join(block["text"] for block in call_mock.await_args.kwargs["system_blocks"])
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("Hotdog Validator and Repair Compiler", system_text)
        self.assertIn("final JSON exactly as printed", system_text)
        self.assertIn("RUN MODE:\nHOTDOG REPAIR JSON", user_text)
        self.assertIn("PASS 1 PLAN:", user_text)
        self.assertIn("COMPANY RESEARCH:", user_text)
        self.assertIn("APPROVED DES:", user_text)
        self.assertIn("GENERATED RESUME JSON:", user_text)
        self.assertIn('"experience"', user_text)
        self.assertIsNone(call_mock.await_args.kwargs["output_validator"])


    def test_v3_questions_use_v3_prompt_with_jd_questions_and_final_json(self):
        resume_json = {
            "config": {"prompt_profile": "v3"},
            "professional_experience": [
                {
                    "title": "Software Engineer II",
                    "company": "Tata Consultancy Services",
                    "bullets": ["Designed Java API workflows for stakeholders."],
                }
            ],
            "projects": [],
            "technical_skills": {"Skills": "Java, Spring Boot"},
        }
        with patch("pipeline.call_model", new=AsyncMock(return_value="1. Why this role?\nThis role matches my Java API experience.")) as call_mock:
            asyncio.run(
                pipeline.run_application_answers(
                    company="Acme",
                    title="Backend Engineer",
                    jd="Build Java APIs",
                    questions="Why this role?",
                    resume_json=resume_json,
                    prompt_profile="v3",
                )
            )
        system_text = "\n".join(block["text"] for block in call_mock.await_args.kwargs["system_blocks"])
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("V3 Application Questions Prompt", system_text)
        self.assertIn("Prompt Profile: v3", user_text)
        self.assertIn("Candidate Resume JSON:", user_text)
        self.assertIn("Job Description:\nBuild Java APIs", user_text)

    def test_v1_questions_use_v1_prompt(self):
        with patch("pipeline.call_model", new=AsyncMock(return_value="1. Why this role?\nRelevant experience.")) as call_mock:
            asyncio.run(
                pipeline.run_application_answers(
                    company="Acme",
                    title="Backend Engineer",
                    jd="Build Java APIs",
                    questions="Why this role?",
                    resume_json={"professional_experience": []},
                    company_research="Official engineering page: builds agent orchestration systems.",
                    prompt_profile="v1",
                )
            )
        system_text = "\n".join(block["text"] for block in call_mock.await_args.kwargs["system_blocks"])
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("V1 Application Questions Prompt", system_text)
        self.assertIn("Prompt Profile: v1", user_text)
        self.assertIn("Company Research (live web search results):", user_text)
        self.assertIn("builds agent orchestration systems", user_text)

    def test_company_research_extracts_named_results_and_urls(self):
        page = """
        <a rel="nofollow" class="result__a" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.netic.ai%2Fengineering&amp;rut=x">Netic Engineering | Building the Agentic Brain</a>
        <a class="result__snippet" href="x">Netic builds an &lt;b&gt;orchestration&lt;/b&gt; layer for AI agents.</a>
        """
        with patch("pipeline.fetch_public_search_html", return_value=page):
            research = pipeline.research_company_for_questions("Netic", "Software Engineer")
        self.assertIn("Netic Engineering | Building the Agentic Brain", research)
        self.assertIn("https://www.netic.ai/engineering", research)
        self.assertIn("orchestration", research)

    def test_v1_questions_research_company_when_not_supplied(self):
        with (
            patch(
                "pipeline.research_company_for_questions",
                return_value="Verified company research result.",
            ) as research_mock,
            patch("pipeline.call_model", new=AsyncMock(return_value="Answer")) as call_mock,
        ):
            asyncio.run(
                pipeline.run_application_answers(
                    company="Netic",
                    title="Software Engineer",
                    jd="Build agent orchestration systems.",
                    questions="Why Netic?",
                    resume_json={"professional_experience": []},
                    prompt_profile="v1",
                )
            )
        research_mock.assert_called_once_with("Netic", "Software Engineer")
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("Verified company research result.", user_text)

    def test_v1_linkedin_uses_v1_prompt_and_current_inputs(self):
        response = valid_resume_response("r" * 350, "m" * 350)
        with patch("pipeline.call_model", new=AsyncMock(return_value=response)) as call_mock:
            result = asyncio.run(
                pipeline.run_linkedin_outreach(
                    company="Acme",
                    title="Backend Engineer",
                    location="New York, NY",
                    jd="Build Java APIs",
                    resume_json={"professional_experience": []},
                    prompt_profile="v1",
                )
            )
        system_text = "\n".join(block["text"] for block in call_mock.await_args.kwargs["system_blocks"])
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("V1 LinkedIn Outreach Prompt", system_text)
        self.assertIn("Company: Acme", user_text)
        self.assertIn("Title: Backend Engineer", user_text)
        self.assertIn("Location: New York, NY", user_text)
        self.assertLessEqual(len(pipeline.extract_linkedin_message(result, "recruiter")), 300)
        self.assertLessEqual(len(pipeline.extract_linkedin_message(result, "hiring_manager")), 300)

    def test_v3_compact_to_resume_json_marks_v3_profile(self):
        compact = pipeline.extract_json(valid_compact_response())
        mapped = pipeline.compact_to_resume_json(
            compact,
            pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs"),
            "v3",
        )
        self.assertEqual(mapped["config"]["prompt_profile"], "v3")
        self.assertEqual(mapped["config"]["experience_order"], "json_order")
        self.assertEqual(mapped["education"][0]["university"], "Binghamton University, State University of New York (SUNY)")
        self.assertEqual(mapped["education"][0]["degree"], "Master of Science, Computer Science, AI Specialization")
        self.assertEqual(mapped["education"][1]["university"], "Gujarat Technological University (GTU)")
        self.assertEqual(mapped["education"][1]["degree"], "Bachelor of Engineering, Computer Engineering")

    def test_v3_compact_to_resume_json_preserves_level_summary_and_ta_row(self):
        mapped = pipeline.compact_to_resume_json(
            {
                "type": "Fullstack",
                "level": "mid",
                "summary": "Full-stack engineer focused on reliable Java and React workflows.",
                "experience": [
                    {
                        "id": "TA",
                        "title": "Teaching Assistant",
                        "company": "Binghamton University",
                        "bullets": ["Reviewed Java and SQL assignments for students."],
                    }
                ],
                "projects": [],
                "technical_skills": [["Languages", ["Java", "React"]]],
            },
            pipeline.ResumeInput(company="Acme", title="Fullstack Engineer", jd="Build Java and React systems"),
            "v3",
        )

        self.assertEqual(mapped["config"]["type"], "backend")
        self.assertEqual(mapped["config"]["level"], 3)
        self.assertEqual(mapped["summary"], "Full-stack engineer focused on reliable Java and React workflows.")
        self.assertEqual(mapped["professional_experience"][0]["location"], "Binghamton, NY")
        self.assertEqual(mapped["professional_experience"][0]["dates"], "Aug 2025 - Present")

    def test_candidate_profile_locks_experience_identity_and_education(self):
        mapped = pipeline.compact_to_resume_json(
            {
                "type": "entry_swe",
                "experience": [
                    {
                        "id": "TA",
                        "title": "Wrong TA Title",
                        "company": "Wrong University",
                        "location": "Wrong Location",
                        "dates": "Wrong Dates",
                        "bullets": ["Reviewed Java assignments using the approved rubric."],
                    },
                    {
                        "id": "GHI",
                        "title": "Wrong GHI Title",
                        "company": "Wrong GHI Company",
                        "location": "Wrong Location",
                        "dates": "Wrong Dates",
                        "bullets": ["Validated research data for analyst dashboards."],
                    },
                    {
                        "id": "TCS_SWE_II",
                        "title": "Wrong TCS II Title",
                        "company": "Wrong TCS Company",
                        "location": "Wrong Location",
                        "dates": "Wrong Dates",
                        "bullets": ["Designed Java services for verified workflows."],
                    },
                    {
                        "id": "TCS_SWE_I",
                        "title": "Wrong TCS I Title",
                        "company": "Wrong TCS Company",
                        "location": "Wrong Location",
                        "dates": "Wrong Dates",
                        "bullets": ["Implemented Java APIs for verified workflows."],
                    },
                ],
                "education": [{"university": "Wrong University"}],
                "projects": [],
                "technical_skills": [],
            },
            pipeline.ResumeInput(company="Acme", title="Software Engineer", jd="Build APIs"),
            "v1",
        )

        jobs = {item["id"]: item for item in mapped["professional_experience"]}
        self.assertEqual(
            (jobs["TA"]["title"], jobs["TA"]["company"], jobs["TA"]["location"], jobs["TA"]["dates"]),
            ("Teaching Assistant", "Binghamton University", "Binghamton, NY", "Aug 2025 - Present"),
        )
        self.assertEqual(
            (jobs["GHI"]["title"], jobs["GHI"]["company"], jobs["GHI"]["location"], jobs["GHI"]["dates"]),
            ("Software Engineering Intern", "Global Health Impact", "New York, NY", "May 2025 - Jun 2025"),
        )
        self.assertEqual(
            (jobs["TCS_SWE_II"]["title"], jobs["TCS_SWE_II"]["company"], jobs["TCS_SWE_II"]["location"], jobs["TCS_SWE_II"]["dates"]),
            ("Software Engineer II", "Tata Consultancy Services", "Gandhinagar, India", "Oct 2022 - Dec 2024"),
        )
        self.assertEqual(
            (jobs["TCS_SWE_I"]["title"], jobs["TCS_SWE_I"]["company"], jobs["TCS_SWE_I"]["location"], jobs["TCS_SWE_I"]["dates"]),
            ("Software Engineer I", "Tata Consultancy Services", "Gandhinagar, India", "Mar 2021 - Sep 2022"),
        )
        self.assertEqual(jobs["TA"]["bullets"], ["Reviewed Java assignments using the approved rubric."])
        self.assertEqual(mapped["education"], app_properties.CANDIDATE_PROFILE["education"])

    def test_candidate_profile_locks_combined_tcs_identity(self):
        mapped = pipeline.compact_to_resume_json(
            {
                "type": "entry_aiml",
                "experience": [
                    {
                        "id": "TCS_COMBINED",
                        "title": "Wrong Combined Title",
                        "company": "Wrong Combined Company",
                        "location": "Wrong Location",
                        "dates": "Wrong Dates",
                        "bullets": ["Automated a verified engineering workflow."],
                    }
                ],
                "projects": [],
                "technical_skills": [],
            },
            pipeline.ResumeInput(company="Acme", title="AI Engineer", jd="Build AI systems"),
            "v1",
        )

        job = mapped["professional_experience"][0]
        self.assertEqual(job["title"], "Software Engineer II")
        self.assertEqual(job["company"], "Tata Consultancy Services")
        self.assertEqual(job["location"], "Gandhinagar, India")
        self.assertEqual(job["dates"], "Mar 2021 - Dec 2024")


    def test_v3_compact_to_resume_json_preserves_grouped_skill_rows_with_limits(self):
        mapped = pipeline.compact_to_resume_json(
            {
                "type": "Backend",
                "level": "mid",
                "experience": [],
                "projects": [],
                "technical_skills": {
                    "Languages": ["Java", "Python", "SQL", "Java"],
                    "Backend and APIs": ["Spring Boot", "REST APIs", "FastAPI", "Flask", "Node.js", "GraphQL", "gRPC"],
                    "Cloud and Delivery": ["AWS", "Docker"],
                    "Data": ["PostgreSQL"],
                    "Quality": ["JUnit"],
                    "Extra": ["Should not render"],
                },
            },
            pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs"),
            "v3",
        )

        self.assertEqual(
            mapped["technical_skills"],
            [
                ["Languages", ["Java", "Python", "SQL"]],
                ["Backend and APIs", ["Spring Boot", "REST APIs", "FastAPI", "Flask", "Node.js", "GraphQL"]],
                ["Cloud and Delivery", ["AWS", "Docker"]],
                ["Data", ["PostgreSQL"]],
                ["Quality", ["JUnit"]],
            ],
        )

    def test_v3_compact_to_resume_json_splits_flat_skill_category_string(self):
        mapped = pipeline.compact_to_resume_json(
            {
                "type": "Backend",
                "level": "mid",
                "experience": [],
                "projects": [],
                "technical_skills": (
                    "Languages: Java, Python, C#, C++, JavaScript, "
                    "Backend & APIs: Spring Boot, REST APIs, OAuth 2.0, RBAC, Node.js, "
                    "Cloud & Infrastructure: AWS, Azure, Docker, Kubernetes, GitLab CI/CD, Terraform, "
                    "Data & Observability: PostgreSQL, MongoDB, Redis, Datadog, CloudWatch, "
                    "AI & Automation: LLM Agents, Python Automation, GitHub Actions"
                ),
            },
            pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs"),
            "v3",
        )

        self.assertEqual(
            mapped["technical_skills"],
            [
                ["Languages", ["Java", "Python", "C#", "C++", "JavaScript"]],
                ["Backend & APIs", ["Spring Boot", "REST APIs", "OAuth 2.0", "RBAC", "Node.js"]],
                ["Cloud & Infrastructure", ["AWS", "Azure", "Docker", "Kubernetes", "GitLab CI/CD", "Terraform"]],
                ["Data & Observability", ["PostgreSQL", "MongoDB", "Redis", "Datadog", "CloudWatch"]],
                ["AI & Automation", ["LLM Agents", "Python Automation", "GitHub Actions"]],
            ],
        )


    def test_compact_validator_rejects_missing_experience(self):
        bad_response = (
            "```json\n"
            "{\"technical_skills\": {\"row1\": [\"React\", \"TypeScript\"], \"row2\": [\"Java\"]}}\n"
            "```"
        )
        error = pipeline.validate_compact_resume_response(bad_response)
        self.assertIn("include experience", error or "")

    def test_compact_validator_accepts_compact_schema(self):
        self.assertIsNone(pipeline.validate_compact_resume_response(valid_compact_response()))

    def test_compact_validator_accepts_compact_schema_without_type(self):
        response = valid_compact_response().replace("\"type\": \"Backend\", ", "")
        self.assertIsNone(pipeline.validate_compact_resume_response(response))

    def test_compact_validator_accepts_extra_metadata_and_optional_skills(self):
        response = (
            "```json\n"
            "{\"analysis\": \"ok\", \"experience\": [], \"projects\": [], \"notes\": \"diagnostic\"}\n"
            "```"
        )
        self.assertIsNone(pipeline.validate_compact_resume_response(response))

    def test_json_validator_fetches_v3_json_without_content_rules(self):
        response = {
            "type": "Backend",
            "level": "mid",
            "summary": "Backend engineer focused on Java systems.",
            "experience": [
                {"id": "TA", "title": "Teaching Assistant", "company": "Binghamton University", "bullets": ["Reviewed SQL assignments for ten students using rubrics that improved feedback quality for classroom project submissions."] * 2},
                {"id": "GHI", "title": "Software Engineering Intern", "company": "Global Health Impact", "bullets": ["Built Python data checks for research workflows using pandas validation that improved dashboard quality for analysts."] * 3},
                {"id": "TCS", "title": "Software Engineer II", "company": "Tata Consultancy Services", "bullets": ["Migrated 7+ applications with zero downtime using release validation that kept dependent teams ready for production handoff."] * 5},
            ],
            "projects": [
                {"name": "JobPulse", "bullets": ["Created job-search APIs using PostgreSQL and Redis indexing that improved search speed for ten thousand postings."]},
                {"name": "EvalTrace", "bullets": ["Built evaluation workflows using Python automation that compared model outputs for repeatable review decisions."]},
            ],
            "technical_skills": [["Languages", ["Java", "Python"]]],
        }
        self.assertIsNone(pipeline.validate_json_response(json.dumps(response)))

    def test_compact_mapper_accepts_professional_experience_shape(self):
        mapped = pipeline.compact_to_resume_json(
            {
                "professional_experience": [
                    {
                        "title": "Software Engineer II",
                        "company": "Tata Consultancy Services",
                        "bullets": ["Built Java APIs for users."],
                    }
                ],
                "projects": [],
                "technical_skills": {"Skills": "Java, Spring Boot"},
            },
            pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs"),
        )
        self.assertEqual(mapped["professional_experience"][0]["title"], "Software Engineer II")
        self.assertEqual(mapped["technical_skills"], [["Skills", ["Java", "Spring Boot"]]])

    def test_compact_to_resume_json_adds_locked_resume_fields(self):
        compact = pipeline.extract_json(valid_compact_response())
        mapped = pipeline.compact_to_resume_json(
            compact,
            pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs", words="Boston, MA"),
        )
        self.assertEqual(mapped["config"]["prompt_profile"], "v3")
        self.assertEqual(mapped["config"]["company"], "Acme")
        self.assertIn("(607) 235-1181", mapped["contact"])
        self.assertEqual(mapped["location"], "New York, NY | Moving to Boston, MA")
        self.assertEqual(mapped["professional_experience"][0]["dates"], "Oct 2022 - Dec 2024")
        self.assertEqual(mapped["projects"][0]["github_url"], "https://github.com/kevalshah0612/jobpulse")

    def test_compact_resume_location_defaults_to_current_location(self):
        compact = pipeline.extract_json(valid_compact_response())
        mapped = pipeline.compact_to_resume_json(
            compact,
            pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs"),
        )
        self.assertEqual("New York, NY", mapped["location"])


    def test_des_facts_file_replaces_existing_request_block(self):
        inp = pipeline.ResumeInput(
            company="Acme",
            title="Backend Engineer",
            jd="Build APIs",
            words="Boston, MA",
            des="I used Kafka in TCS SWE II.",
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "global_des_facts.md"
            pipeline.update_des_facts_file(
                path,
                request_id="Acme_Backend_20260630_120000",
                inp=inp,
                prompt_profile="v3",
                pass1_text="DES 1 | keyword: Kafka | use when: event processing",
                approval_text="Approved: 1",
            )
            pipeline.update_des_facts_file(
                path,
                request_id="Acme_Backend_20260630_120000",
                inp=inp,
                prompt_profile="v3",
                pass1_text="DES 2 | keyword: AWS | use when: cloud deployment",
                approval_text="CONFIRM",
            )

            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count("## Acme_Backend_20260630_120000"), 1)
            self.assertIn("I used Kafka in TCS SWE II.", text)
            self.assertIn("DES 2 | keyword: AWS", text)
            self.assertIn("CONFIRM", text)
            self.assertNotIn("DES 1 | keyword: Kafka", text)



class NvidiaModelProfileTests(unittest.TestCase):
    def fake_client(self, response):
        create = MagicMock(return_value=response)
        client = SimpleNamespace(
            chat=SimpleNamespace(completions=SimpleNamespace(create=create))
        )
        return client, create

    def fake_stream(self, content="Nemotron answer", reasoning="", reasoning_tokens=0):
        return [
            SimpleNamespace(
                choices=[SimpleNamespace(
                    delta=SimpleNamespace(content=content, reasoning_content=reasoning),
                    finish_reason="stop",
                )],
                usage=SimpleNamespace(
                    prompt_tokens=10,
                    completion_tokens=20,
                    completion_tokens_details=SimpleNamespace(reasoning_tokens=reasoning_tokens),
                ),
            )
        ]

    def test_generation_settings_load_from_config(self):
        cfg = {
            "nvidia_medium_effort": False,
            "nvidia_temperature": 1.0,
            "nvidia_top_p": 0.95,
            "nvidia_seed": 42,
            "nvidia_reasoning_budget": 32768,
            "response_max_tokens": 65536,
            "nvidia_max_attempts": 5,
            "nvidia_max_concurrent_requests": 10,
            "nvidia_max_concurrent_requests_per_account": 5,
            "nvidia_timeout_seconds": 0,
            "nvidia_guided_json": True,
            "nvidia_validation_pass": True,
            "nvidia_validator_seed": 43,
        }
        with patch("pipeline.load_config", return_value=cfg):
            self.assertFalse(pipeline.get_nvidia_medium_effort())
            self.assertEqual(1.0, pipeline.get_nvidia_temperature())
            self.assertEqual(0.95, pipeline.get_nvidia_top_p())
            self.assertEqual(42, pipeline.get_nvidia_seed())
            self.assertEqual(32768, pipeline.get_nvidia_reasoning_budget())
            self.assertEqual(65536, pipeline.get_response_max_tokens())
            self.assertEqual(5, pipeline.get_nvidia_max_attempts())
            self.assertEqual(10, pipeline.get_nvidia_max_concurrent_requests())
            self.assertEqual(5, pipeline.get_nvidia_max_concurrent_requests_per_account())
            self.assertEqual(0, pipeline.get_nvidia_timeout_seconds())
            self.assertTrue(pipeline.get_nvidia_guided_json())
            self.assertTrue(pipeline.get_nvidia_validation_pass())
            self.assertEqual(43, pipeline.get_nvidia_validator_seed())

    def test_provider_mode_one_and_model_setting_select_nvidia(self):
        cfg = {
            "provider_mode": "1",
            "model_nvidia": "nvidia/nemotron-3-ultra-550b-a55b",
        }
        with patch("pipeline.load_config", return_value=cfg):
            self.assertEqual("nvidia", pipeline.get_provider())
            self.assertEqual(
                "nvidia/nemotron-3-ultra-550b-a55b",
                pipeline.get_nvidia_model(),
            )


    def test_two_nvidia_accounts_are_loaded_in_order_and_legacy_duplicate_is_removed(self):
        cfg = {
            "nvidia_api_key_1": "key-one",
            "nvidia_api_key_2": "key-two",
            "nvidia_api_key": "key-one",
        }
        with patch("pipeline.load_config", return_value=cfg):
            accounts = pipeline.get_nvidia_accounts()

        self.assertEqual(["account_1", "account_2"], [item.label for item in accounts])
        self.assertEqual(["key-one", "key-two"], [item.api_key for item in accounts])

    def test_account_selection_round_robins_without_exposing_keys(self):
        accounts = [
            pipeline.NvidiaAccount("account_1", "secret-one"),
            pipeline.NvidiaAccount("account_2", "secret-two"),
        ]
        with (
            patch("pipeline.get_nvidia_accounts", return_value=accounts),
            patch.object(pipeline, "_nvidia_account_cursor", 0),
        ):
            labels = [pipeline.choose_nvidia_account().label for _ in range(4)]

        self.assertEqual(["account_1", "account_2", "account_1", "account_2"], labels)
        self.assertNotIn("secret", json.dumps(labels))

    def test_retry_after_header_controls_retry_delay(self):
        error = RuntimeError("service unavailable")
        error.response = SimpleNamespace(headers={"Retry-After": "7"})
        self.assertEqual(7.0, pipeline.nvidia_retry_delay_seconds(3, error))

    def test_dropdown_contains_supported_models_with_profile_modes(self):
        options = pipeline.nvidia_model_options()
        self.assertEqual(len(options), 4)
        self.assertIn("Nemo-on", options)
        self.assertNotIn("Nemo-off", options)
        self.assertIn("DS-on", options)
        self.assertNotIn("DS-off", options)
        self.assertIn("Minimax", options)
        self.assertIn("GLM", options)
        self.assertEqual(
            "Nemo-on",
            pipeline.nvidia_model_option_label(
                "nvidia/nemotron-3-ultra-550b-a55b",
                False,
            ),
        )
        self.assertEqual(
            "DS-on",
            pipeline.nvidia_model_option_label("deepseek-ai/deepseek-v4-pro", False),
        )
        resolved = {pipeline.resolve_nvidia_model_option(option) for option in options}
        self.assertEqual(
            resolved,
            {
                ("nvidia/nemotron-3-ultra-550b-a55b", True),
                ("deepseek-ai/deepseek-v4-pro", True),
                ("minimaxai/minimax-m3", False),
                ("z-ai/glm-5.2", False),
            },
        )

    def test_glm_uses_official_streaming_generation_profile(self):
        completion = self.fake_stream(content="GLM answer")
        client, create = self.fake_client(completion)
        with patch("pipeline.get_nvidia_client", return_value=client):
            response = pipeline.call_nvidia_sync(
                system_blocks=[],
                messages=[{"role": "user", "content": "hello"}],
                model="z-ai/glm-5.2",
                thinking=False,
                max_tokens=65536,
            )

        kwargs = create.call_args.kwargs
        self.assertTrue(kwargs["stream"])
        self.assertEqual(1.0, kwargs["temperature"])
        self.assertEqual(1.0, kwargs["top_p"])
        self.assertEqual(16384, kwargs["max_tokens"])
        self.assertEqual(42, kwargs["seed"])
        self.assertNotIn("extra_body", kwargs)
        self.assertEqual("GLM answer", response.text)

    def test_deepseek_uses_non_streaming_thinking_parameter(self):
        completion = SimpleNamespace(
            choices=[SimpleNamespace(
                message=SimpleNamespace(content="DeepSeek answer"),
                finish_reason="stop",
            )],
            usage=SimpleNamespace(prompt_tokens=10, completion_tokens=20),
        )
        client, create = self.fake_client(completion)
        with patch("pipeline.get_nvidia_client", return_value=client):
            response = pipeline.call_nvidia_sync(
                system_blocks=[],
                messages=[{"role": "user", "content": "hello"}],
                model="deepseek-ai/deepseek-v4-pro",
                thinking=False,
                max_tokens=65536,
            )
        kwargs = create.call_args.kwargs
        self.assertFalse(kwargs["stream"])
        self.assertEqual(kwargs["extra_body"], {"chat_template_kwargs": {"thinking": False}})
        self.assertEqual(response.text, "DeepSeek answer")

    def test_nemotron_uses_model_streaming_reasoning_payload(self):
        completion = self.fake_stream(reasoning="Reasoning", reasoning_tokens=7)
        client, create = self.fake_client(completion)
        with patch("pipeline.get_nvidia_client", return_value=client):
            response = pipeline.call_nvidia_sync(
                system_blocks=[],
                messages=[{"role": "user", "content": "hello"}],
                model="nvidia/nemotron-3-ultra-550b-a55b",
                thinking=True,
                max_tokens=65536,
            )
        kwargs = create.call_args.kwargs
        self.assertTrue(kwargs["stream"])
        self.assertEqual(kwargs["temperature"], 1.0)
        self.assertEqual(kwargs["top_p"], 0.95)
        self.assertEqual(kwargs["seed"], 42)
        self.assertEqual(
            kwargs["extra_body"],
            {
                "chat_template_kwargs": {"enable_thinking": True},
                "reasoning_budget": 32768,
            },
        )
        self.assertEqual(response.text, "Nemotron answer")
        self.assertEqual(7, response.usage["reasoning_tokens"])

    def test_nemotron_accepts_per_call_reasoning_budget_override(self):
        completion = self.fake_stream(content="Budgeted answer")
        client, create = self.fake_client(completion)
        with patch("pipeline.get_nvidia_client", return_value=client):
            pipeline.call_nvidia_sync(
                system_blocks=[],
                messages=[{"role": "user", "content": "hello"}],
                model="nvidia/nemotron-3-ultra-550b-a55b",
                thinking=True,
                max_tokens=12000,
                reasoning_budget_override=7000,
            )

        self.assertEqual(7000, create.call_args.kwargs["extra_body"]["reasoning_budget"])

    def test_nemotron_thinking_off_omits_reasoning_budget(self):
        completion = self.fake_stream()
        client, create = self.fake_client(completion)
        with patch("pipeline.get_nvidia_client", return_value=client):
            pipeline.call_nvidia_sync(
                system_blocks=[],
                messages=[{"role": "user", "content": "hello"}],
                model="nvidia/nemotron-3-ultra-550b-a55b",
                thinking=False,
                max_tokens=65536,
            )
        self.assertEqual(
            create.call_args.kwargs["extra_body"],
            {"chat_template_kwargs": {"enable_thinking": False}},
        )

    def test_guided_json_schema_is_sent_through_nvext(self):
        completion = self.fake_stream(content='{"ok":true}')
        client, create = self.fake_client(completion)
        schema = {"type": "object", "required": ["ok"]}
        with patch("pipeline.get_nvidia_client", return_value=client):
            pipeline.call_nvidia_sync(
                system_blocks=[],
                messages=[{"role": "user", "content": "hello"}],
                model="nvidia/nemotron-3-ultra-550b-a55b",
                thinking=True,
                max_tokens=65536,
                guided_json_schema=schema,
            )

        self.assertEqual(schema, create.call_args.kwargs["extra_body"]["nvext"]["guided_json"])

    def test_medium_effort_true_is_sent(self):
        completion = self.fake_stream()
        client, create = self.fake_client(completion)
        with (
            patch("pipeline.get_nvidia_client", return_value=client),
            patch("pipeline.get_nvidia_medium_effort", return_value=True),
        ):
            pipeline.call_nvidia_sync(
                system_blocks=[],
                messages=[{"role": "user", "content": "hello"}],
                model="nvidia/nemotron-3-ultra-550b-a55b",
                thinking=True,
                max_tokens=65536,
            )
        self.assertTrue(
            create.call_args.kwargs["extra_body"]["chat_template_kwargs"]["medium_effort"]
        )

    def test_sanitized_payload_omits_message_content(self):
        payload = pipeline.build_nvidia_request_payload(
            system_blocks=[{"type": "text", "text": "system secret-like content"}],
            messages=[{"role": "user", "content": "private JD text"}],
            model="nvidia/nemotron-3-ultra-550b-a55b",
            thinking=True,
            max_tokens=65536,
            guided_json_schema={"type": "object"},
        )
        sanitized = pipeline.sanitize_nvidia_request_payload(payload)
        rendered = json.dumps(sanitized)
        self.assertNotIn("system secret-like content", rendered)
        self.assertNotIn("private JD text", rendered)
        self.assertEqual({"type": "object"}, sanitized["extra_body"]["nvext"]["guided_json"])

    def test_minimax_uses_non_streaming_profile_without_thinking_payload(self):
        completion = SimpleNamespace(
            choices=[SimpleNamespace(
                message=SimpleNamespace(content="MiniMax answer"),
                finish_reason="stop",
            )],
            usage=SimpleNamespace(prompt_tokens=10, completion_tokens=20),
        )
        client, create = self.fake_client(completion)
        with patch("pipeline.get_nvidia_client", return_value=client):
            response = pipeline.call_nvidia_sync(
                system_blocks=[],
                messages=[{"role": "user", "content": "hello"}],
                model="minimaxai/minimax-m3",
                thinking=True,
                max_tokens=65536,
            )
        kwargs = create.call_args.kwargs
        self.assertFalse(kwargs["stream"])
        self.assertEqual(kwargs["max_tokens"], 65536)
        self.assertEqual(kwargs["seed"], 42)
        self.assertNotIn("extra_body", kwargs)
        self.assertEqual(response.text, "MiniMax answer")


class NvidiaRetryTests(unittest.TestCase):
    def run_call(self, responses, validator=pipeline.validate_json_response, cancel_event=None):
        with (
            patch("pipeline.get_provider", return_value="nvidia"),
            patch("pipeline.get_nvidia_model", return_value="nvidia/test"),
            patch("pipeline.get_nvidia_max_attempts", return_value=3),
            patch("pipeline.get_nvidia_validation_pass", return_value=False),
            patch("pipeline.call_nvidia_sync", side_effect=responses) as call_mock,
            patch("pipeline.asyncio.sleep", new=AsyncMock()),
        ):
            result = asyncio.run(
                pipeline.call_model(
                    system_blocks=[],
                    messages=[{"role": "user", "content": "generate"}],
                    label="TEST",
                    max_tokens=1000,
                    output_validator=validator,
                    cancel_event=cancel_event,
                )
            )
        return result, call_mock.call_count

    def test_call_model_passes_explicit_guided_schema_override(self):
        response = pipeline.NvidiaResponse(
            text='{"ok":true}',
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        schema = {
            "type": "object",
            "properties": {"ok": {"type": "boolean"}},
            "required": ["ok"],
            "additionalProperties": False,
        }
        with (
            patch("pipeline.get_nvidia_max_attempts", return_value=3),
            patch("pipeline.get_nvidia_validation_pass", return_value=False),
            patch("pipeline.call_nvidia_sync", return_value=response) as call_mock,
        ):
            result = asyncio.run(pipeline.call_model(
                system_blocks=[],
                messages=[{"role": "user", "content": "generate"}],
                label="TEST",
                max_tokens=1000,
                output_validator=lambda _text: None,
                provider_override="nvidia",
                model_override="nvidia/test",
                guided_json_schema_override=schema,
            ))

        self.assertEqual('{"ok":true}', result)
        self.assertEqual(schema, call_mock.call_args.kwargs["guided_json_schema"])

    def test_retries_malformed_json(self):
        malformed = pipeline.NvidiaResponse(
            text="LinkedIn Message:\nHi.\n\n```json\n{bad}\n```",
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        valid = pipeline.NvidiaResponse(
            text=valid_resume_response(),
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        result, calls = self.run_call([malformed, valid])
        self.assertEqual(calls, 2)
        self.assertIsNone(pipeline.validate_json_response(result))

    def test_rejected_response_callback_receives_raw_attempt_text(self):
        malformed = pipeline.NvidiaResponse(
            text="I need the role type before writing JSON.",
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        valid = pipeline.NvidiaResponse(
            text=valid_resume_response(),
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        rejected = []
        with (
            patch("pipeline.get_provider", return_value="nvidia"),
            patch("pipeline.get_nvidia_model", return_value="nvidia/test"),
            patch("pipeline.get_nvidia_max_attempts", return_value=3),
            patch("pipeline.get_nvidia_validation_pass", return_value=False),
            patch("pipeline.call_nvidia_sync", side_effect=[malformed, valid]),
            patch("pipeline.asyncio.sleep", new=AsyncMock()),
        ):
            asyncio.run(
                pipeline.call_model(
                    system_blocks=[],
                    messages=[{"role": "user", "content": "generate"}],
                    label="TEST",
                    max_tokens=1000,
                    output_validator=pipeline.validate_json_response,
                    rejected_response_cb=lambda attempt, text, reason: rejected.append((attempt, text, reason)),
                )
            )
        self.assertEqual(rejected[0][0], 1)
        self.assertIn("role type", rejected[0][1])
        self.assertIn("Could not extract valid JSON", rejected[0][2])

    def test_validation_pass_uses_validator_seed_and_corrected_output(self):
        primary = pipeline.NvidiaResponse(
            text=valid_resume_response("primary"),
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        validated = pipeline.NvidiaResponse(
            text=valid_resume_response("validated"),
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        with (
            patch("pipeline.get_provider", return_value="nvidia"),
            patch("pipeline.get_nvidia_model", return_value="nvidia/nemotron-3-ultra-550b-a55b"),
            patch("pipeline.get_nvidia_max_attempts", return_value=3),
            patch("pipeline.get_nvidia_validation_pass", return_value=True),
            patch("pipeline.get_nvidia_validator_seed", return_value=43),
            patch("pipeline.call_nvidia_sync", side_effect=[primary, validated]) as call_mock,
        ):
            result = asyncio.run(pipeline.call_model(
                system_blocks=[],
                messages=[{"role": "user", "content": "generate"}],
                label="TEST",
                max_tokens=1000,
                output_validator=pipeline.validate_json_response,
            ))

        self.assertIn("validated", result)
        self.assertEqual(2, call_mock.call_count)
        self.assertIsNone(call_mock.call_args_list[0].kwargs.get("seed_override"))
        self.assertEqual(43, call_mock.call_args_list[1].kwargs["seed_override"])
        self.assertIn("VALIDATION PASS", call_mock.call_args_list[1].kwargs["messages"][-1]["content"])

    def test_retries_complete_json_with_length_finish_reason(self):
        complete = pipeline.NvidiaResponse(
            text=valid_resume_response(),
            usage=EMPTY_USAGE,
            finish_reason="length",
        )
        stopped = pipeline.NvidiaResponse(
            text=valid_resume_response(),
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        result, calls = self.run_call([complete, stopped])
        self.assertEqual(calls, 2)
        self.assertIsNone(pipeline.validate_json_response(result))

    def test_retries_rate_limit_error(self):
        error = RuntimeError("rate limited")
        error.status_code = 429
        valid = pipeline.NvidiaResponse(
            text=valid_resume_response(),
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        result, calls = self.run_call([error, valid])
        self.assertEqual(2, calls)
        self.assertIsNone(pipeline.validate_json_response(result))

    def test_retries_length_response_only_when_json_is_missing(self):
        truncated = pipeline.NvidiaResponse(
            text='```json\n{"ok":',
            usage=EMPTY_USAGE,
            finish_reason="length",
        )
        valid = pipeline.NvidiaResponse(
            text=valid_resume_response(),
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        result, calls = self.run_call([truncated, valid])
        self.assertEqual(calls, 2)
        self.assertIsNone(pipeline.validate_json_response(result))

    def test_does_not_retry_complete_json_for_long_linkedin_message(self):
        complete = pipeline.NvidiaResponse(
            text=valid_resume_response("x" * 334),
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        result, calls = self.run_call([complete])
        self.assertEqual(calls, 1)
        self.assertIsNone(pipeline.validate_json_response(result))
        self.assertIsNotNone(pipeline.validate_resume_response(result))

    def test_valid_schema_output_is_not_retried_for_quality(self):
        complete = pipeline.NvidiaResponse(
            text=valid_resume_response("brief"),
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        diagnostics = {}
        with (
            patch("pipeline.get_provider", return_value="nvidia"),
            patch("pipeline.get_nvidia_model", return_value="nvidia/nemotron-3-ultra-550b-a55b"),
            patch("pipeline.get_nvidia_validation_pass", return_value=False),
            patch("pipeline.call_nvidia_sync", return_value=complete) as call_mock,
        ):
            result = asyncio.run(pipeline.call_model(
                system_blocks=[],
                messages=[{"role": "user", "content": "generate"}],
                label="TEST",
                max_tokens=1000,
                output_validator=pipeline.validate_json_response,
                diagnostics=diagnostics,
            ))
        self.assertIsNone(pipeline.validate_json_response(result))
        self.assertEqual(1, call_mock.call_count)
        self.assertEqual(1, diagnostics["api_calls"])
        self.assertEqual(0, diagnostics["retries"])
        self.assertFalse(diagnostics["validation_enabled"])

    def test_nonretryable_programming_error_is_not_retried(self):
        with (
            patch("pipeline.get_provider", return_value="nvidia"),
            patch("pipeline.get_nvidia_model", return_value="nvidia/test"),
            patch("pipeline.get_nvidia_max_attempts", return_value=3),
            patch("pipeline.call_nvidia_sync", side_effect=ValueError("bad local argument")) as call_mock,
        ):
            with self.assertRaises(ValueError):
                asyncio.run(pipeline.call_model(
                    system_blocks=[],
                    messages=[{"role": "user", "content": "generate"}],
                    label="TEST",
                    output_validator=pipeline.validate_json_response,
                ))
        self.assertEqual(1, call_mock.call_count)

    def test_retries_pass1_only_when_des_candidates_are_missing(self):
        missing = pipeline.NvidiaResponse(
            text="COVERAGE SUMMARY:\nCoverage confidence: MEDIUM",
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        valid = pipeline.NvidiaResponse(
            text="COVERAGE SUMMARY:\nCoverage confidence: MEDIUM\n\nDES CANDIDATE BANK:\nDES 1 | Kafka | Use when relevant",
            usage=EMPTY_USAGE,
            finish_reason="stop",
        )
        result, calls = self.run_call(
            [missing, valid],
            validator=pipeline.validate_pass1_response,
        )
        self.assertEqual(calls, 2)
        self.assertIsNone(pipeline.validate_pass1_response(result))

    def test_pre_cancelled_operation_never_calls_provider(self):
        cancel_event = threading.Event()
        cancel_event.set()
        with (
            patch("pipeline.get_provider", return_value="nvidia"),
            patch("pipeline.get_nvidia_model", return_value="nvidia/test"),
            patch("pipeline.get_nvidia_max_attempts", return_value=3),
            patch("pipeline.call_nvidia_sync") as call_mock,
        ):
            with self.assertRaises(pipeline.OperationCancelled):
                asyncio.run(
                    pipeline.call_model(
                        system_blocks=[],
                        messages=[{"role": "user", "content": "generate"}],
                        label="TEST",
                        output_validator=pipeline.validate_json_response,
                        cancel_event=cancel_event,
                    )
                )
        call_mock.assert_not_called()

    def test_no_validator_uses_one_attempt(self):
        with (
            patch("pipeline.get_provider", return_value="nvidia"),
            patch("pipeline.get_nvidia_model", return_value="nvidia/test"),
            patch("pipeline.get_nvidia_max_attempts", return_value=5),
            patch("pipeline.call_nvidia_sync", side_effect=RuntimeError("offline")) as call_mock,
            patch("pipeline.load_config", return_value={"fallback_to_anthropic": False}),
        ):
            with self.assertRaises(RuntimeError):
                asyncio.run(
                    pipeline.call_model(
                        system_blocks=[],
                        messages=[{"role": "user", "content": "answer"}],
                        label="QUESTIONS",
                    )
                )
        self.assertEqual(call_mock.call_count, 1)

    def test_does_not_call_claude_when_fallback_is_disabled(self):
        with (
            patch("pipeline.get_provider", return_value="nvidia"),
            patch("pipeline.get_nvidia_model", return_value="nvidia/test"),
            patch("pipeline.get_nvidia_max_attempts", return_value=2),
            patch("pipeline.call_nvidia_sync", side_effect=RuntimeError("offline")),
            patch("pipeline.load_config", return_value={"fallback_to_anthropic": False}),
            patch("pipeline.get_client") as claude_client,
            patch("pipeline.asyncio.sleep", new=AsyncMock()),
        ):
            with self.assertRaises(RuntimeError):
                asyncio.run(
                    pipeline.call_model(
                        system_blocks=[],
                        messages=[{"role": "user", "content": "generate"}],
                        label="TEST",
                    )
                )
        claude_client.assert_not_called()


if __name__ == "__main__":
    unittest.main()
