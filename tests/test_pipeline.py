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


def valid_v1_compact_response() -> str:
    return (
        "FINAL JSON:\n"
        "```json\n"
        "{"
        "\"type\": \"Backend\", "
        "\"experience\": [{\"title\": \"Software Engineer II\", \"company\": \"Tata Consultancy Services\", \"bullets\": [\"Built Java APIs for users.\"]}], "
        "\"projects\": [{\"name\": \"JobPulse\", \"bullets\": [\"Built Fastify APIs for job search.\"]}], "
        "\"skills\": [\"Java\", \"Spring Boot\", \"PostgreSQL\"]"
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
    def test_default_prompt_profile_is_v3(self):
        self.assertEqual(app_properties.DEFAULT_PROMPT_PROFILE, "v3")

    def test_prompt_profile_options_resolve_to_stable_v1_v2_and_v3(self):
        labels = pipeline.prompt_profile_options()
        self.assertEqual(
            {pipeline.resolve_prompt_profile_label(label) for label in labels},
            {"stable", "v1", "v2", "v3"},
        )
        self.assertIn("Stable", labels)
        self.assertIn("V1", labels)
        self.assertIn("V2", labels)
        self.assertIn("V3", labels)
        self.assertEqual(pipeline.resolve_prompt_profile_label("v1_experimental_flow"), "v1")
        self.assertEqual(pipeline.resolve_prompt_profile_label("v2_experimental_flow"), "v2")
        self.assertEqual(pipeline.resolve_prompt_profile_label("v3_experimental_flow"), "v3")
        self.assertEqual(pipeline.resolve_prompt_profile_label("unknown"), "stable")

    def test_v1_prompt_uses_prompt_story_and_direct_inputs(self):
        with patch("pipeline.call_model", new=AsyncMock(return_value=valid_v1_compact_response())) as call_mock:
            asyncio.run(
                pipeline.run_pass2(
                    pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs", words="Boston, MA", des="Use API work"),
                    pass1_text="",
                    approval_text="",
                    prompt_profile="v1",
                )
            )
        system_text = "\n".join(block["text"] for block in call_mock.await_args.kwargs["system_blocks"])
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("Resume Bullet Writer", system_text)
        self.assertIn("Career Story Bank", system_text)
        self.assertIn("=== RESUME CONFIGURATION - IMMUTABLE ===", user_text)
        self.assertIn("JD:\nBuild APIs", user_text)
        self.assertIn("ROLE TYPE:\nBackend", user_text)
        self.assertIn("Company:\nAcme", user_text)
        self.assertIn("Location:\nBoston, MA", user_text)
        self.assertIn("DES (optional):\nUse API work", user_text)
        self.assertIsNone(call_mock.await_args.kwargs["output_validator"])

    def test_v1_hotdog_routes_to_hotdog_prompt_with_compact_json(self):
        with patch("pipeline.call_model", new=AsyncMock(return_value=valid_v1_compact_response())) as call_mock:
            asyncio.run(
                pipeline.run_recruiter_review(
                    jd="Build APIs",
                    resume1_json={
                        "config": {"type": "backend"},
                        "professional_experience": [{"title": "Software Engineer II", "company": "Tata Consultancy Services", "bullets": ["Built Java APIs."]}],
                        "projects": [],
                        "technical_skills": {"Backend": "Java, Spring Boot"},
                    },
                    company="Acme",
                    title="Backend Engineer",
                    prompt_profile="v1",
                )
            )
        system_text = "\n".join(block["text"] for block in call_mock.await_args.kwargs["system_blocks"])
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("Blind Recruiter Review", system_text)
        self.assertIn("Current Resume JSON:", user_text)
        self.assertIn('"experience"', user_text)
        self.assertNotIn("professional_experience", user_text)
        self.assertIn("FINAL CHECK", call_mock.await_args.kwargs["label"])
        self.assertIsNone(call_mock.await_args.kwargs["output_validator"])

    def test_v2_hotdog_includes_configuration_story_and_current_json(self):
        with patch("pipeline.call_model", new=AsyncMock(return_value=valid_v1_compact_response())) as call_mock:
            asyncio.run(
                pipeline.run_recruiter_review(
                    jd="Build APIs",
                    resume1_json={
                        "config": {"type": "backend"},
                        "professional_experience": [{"title": "Software Engineer II", "company": "Tata Consultancy Services", "bullets": ["Built Java APIs."]}],
                        "projects": [],
                        "technical_skills": {"Backend": "Java, Spring Boot"},
                    },
                    company="Acme",
                    title="Backend Engineer",
                    des="Use API work",
                    inp=pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs", words="Boston, MA", des="Use API work"),
                    prompt_profile="v2",
                    pass1_audit="ORDERED EXPERIENCE TARGETS:\ntcs_se_ii:\nSummary: backend APIs",
                    resume_generation_process="HOTDOG HANDOFF:\n- tcs_se_ii B1: keywords=backend APIs; source=Story 01; translation=None",
                )
            )
        system_text = "\n".join(block["text"] for block in call_mock.await_args.kwargs["system_blocks"])
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("Hotdog Review and Repair", system_text)
        self.assertIn("=== RESUME CONFIGURATION - IMMUTABLE ===", user_text)
        self.assertIn("=== INPUT START ===", user_text)
        self.assertIn("JD:\nBuild APIs", user_text)
        self.assertIn("CANDIDATE DES INPUT:\nUse API work", user_text)
        self.assertIn("APPROVAL / APPROVED DES:\nUse API work", user_text)
        self.assertIn("PASS 1 TARGETS / DES CANDIDATE BANK:", user_text)
        self.assertIn("ORDERED EXPERIENCE TARGETS", user_text)
        self.assertIn("RESUME GENERATION PROCESS / HOTDOG HANDOFF:", user_text)
        self.assertIn("keywords=backend APIs", user_text)
        self.assertIn("STORY.md:\n# Story.md", user_text)
        self.assertIn("PROJECT BANK:", user_text)
        self.assertIn("CURRENT RESUME JSON:", user_text)
        self.assertIn('"experience"', user_text)
        self.assertNotIn("professional_experience", user_text)
        self.assertIsNone(call_mock.await_args.kwargs["output_validator"])

    def test_v2_pass1_includes_configuration_and_uses_no_des_validator(self):
        with patch("pipeline.call_model", new=AsyncMock(return_value="PLANNING ANALYSIS\n--------\n")) as call_mock:
            asyncio.run(
                pipeline.run_pass1(
                    pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs", words="Boston, MA", des="Use API work"),
                    prompt_profile="v2",
                )
            )
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("RUN MODE:\nPASS 1 - PLAN ONLY", user_text)
        self.assertIn("=== RESUME CONFIGURATION - IMMUTABLE ===", user_text)
        self.assertIn("Plan ID: AIML", user_text)
        self.assertIn("Required project count: 3", user_text)
        self.assertIsNone(call_mock.await_args.kwargs["output_validator"])

    def test_v2_prompt_uses_v2_prompt_story_and_direct_inputs(self):
        with patch("pipeline.call_model", new=AsyncMock(return_value=valid_v1_compact_response())) as call_mock:
            asyncio.run(
                pipeline.run_pass2(
                    pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs", words="Boston, MA", des="Use API work"),
                    pass1_text="PLANNING ANALYSIS\n--------\nACTIVE PLAN:\nBackend",
                    approval_text="CONFIRM",
                    prompt_profile="v2",
                )
            )
        system_text = "\n".join(block["text"] for block in call_mock.await_args.kwargs["system_blocks"])
        messages = call_mock.await_args.kwargs["messages"]
        user_text = messages[0]["content"]
        self.assertIn("Resume Qualification Engine", system_text)
        self.assertIn("Story.md", system_text)
        self.assertEqual(messages[1]["role"], "assistant")
        self.assertIn("PLANNING ANALYSIS", messages[1]["content"])
        self.assertIn("RUN MODE:\nPASS 2 - WRITE APPROVED RESUME JSON", messages[2]["content"])
        self.assertIn("CONFIRM", messages[2]["content"])
        self.assertIn("DES CANDIDATE BANK", messages[2]["content"])
        self.assertIn("HOTDOG HANDOFF", messages[2]["content"])
        self.assertIn("=== RESUME CONFIGURATION - IMMUTABLE ===", user_text)
        self.assertIn("JD:\nBuild APIs", user_text)
        self.assertIn("ROLE TYPE:\nAuto", user_text)
        self.assertIn("Company:\nAcme", user_text)
        self.assertIn("Location:\nBoston, MA", user_text)
        self.assertIsNone(call_mock.await_args.kwargs["output_validator"])

    def test_v2_questions_use_v2_prompt_with_jd_questions_and_final_json(self):
        resume_json = {
            "config": {"prompt_profile": "v2"},
            "professional_experience": [
                {
                    "title": "Software Engineer II",
                    "company": "Tata Consultancy Services",
                    "bullets": ["Led Java API work for payment workflows."],
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
                    prompt_profile="v2",
                )
            )
        system_text = "\n".join(block["text"] for block in call_mock.await_args.kwargs["system_blocks"])
        user_text = call_mock.await_args.kwargs["messages"][0]["content"]
        self.assertIn("V2 Application Questions Prompt", system_text)
        self.assertIn("Prompt Profile: v2", user_text)
        self.assertIn("Candidate Resume JSON:", user_text)
        self.assertIn('"professional_experience"', user_text)
        self.assertIn("Job Description:\nBuild Java APIs", user_text)
        self.assertIn("Company: Acme", user_text)
        self.assertIn("Title: Backend Engineer", user_text)
        self.assertIn("Application Questions:\nWhy this role?", user_text)

    def test_v2_compact_to_resume_json_marks_v2_profile(self):
        compact = pipeline.extract_json(valid_v1_compact_response())
        mapped = pipeline.v1_compact_to_resume_json(
            compact,
            pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs"),
            "v2",
        )
        self.assertEqual(mapped["config"]["prompt_profile"], "v2")
        self.assertEqual(mapped["config"]["experience_order"], "json_order")
        self.assertEqual(mapped["education"][0]["university"], "Binghamton University, State University of New York (SUNY)")
        self.assertEqual(mapped["education"][0]["degree"], "Master of Science, Computer Science, AI Specialization")
        self.assertEqual(mapped["education"][1]["university"], "Gujarat Technological University (GTU)")
        self.assertEqual(mapped["education"][1]["degree"], "Bachelor of Engineering, Computer Engineering")

    def test_v3_prompt_uses_v3_prompt_story_and_approved_plan_flow(self):
        with patch("pipeline.call_model", new=AsyncMock(return_value=valid_v1_compact_response())) as call_mock:
            asyncio.run(
                pipeline.run_pass2(
                    pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs", words="Boston, MA", des="Use API work"),
                    pass1_text="COVERAGE SNAPSHOT\n- Plan: Backend",
                    approval_text="1,2",
                    prompt_profile="v3",
                )
            )
        system_text = "\n".join(block["text"] for block in call_mock.await_args.kwargs["system_blocks"])
        messages = call_mock.await_args.kwargs["messages"]
        user_text = messages[0]["content"]
        self.assertIn("V3 Resume Qualification System", system_text)
        self.assertIn("V3 Story.md - Compact Evidence Bank", system_text)
        self.assertIn("V3 PASS 1 OUTPUT OVERRIDE", user_text)
        self.assertIn("KEYWORD MAP:", user_text)
        self.assertIn("MISSING KEYWORD MAP:", user_text)
        self.assertIn("RUN MODE:\nPASS 1 - PLAN ONLY", user_text)
        self.assertEqual(messages[1]["role"], "assistant")
        self.assertIn("COVERAGE SNAPSHOT", messages[1]["content"])
        self.assertIn("RUN MODE:\nPASS 2 - WRITE APPROVED RESUME JSON", messages[2]["content"])
        self.assertIn("1,2", messages[2]["content"])
        self.assertIn("HOTDOG HANDOFF", messages[2]["content"])
        self.assertIsNone(call_mock.await_args.kwargs["output_validator"])

    def test_v3_hotdog_uses_v3_story_rules_and_current_json(self):
        with patch("pipeline.call_model", new=AsyncMock(return_value=valid_v1_compact_response())) as call_mock:
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
        self.assertIn("V3 Hotdog Review and Repair", system_text)
        self.assertIn("STORY.md:\n# V3 Story.md - Compact Evidence Bank", user_text)
        self.assertIn("RESUME RULES FROM rules/Rules.md:", user_text)
        self.assertIn("CURRENT RESUME JSON:", user_text)
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

    def test_v3_compact_to_resume_json_marks_v3_profile(self):
        compact = pipeline.extract_json(valid_v1_compact_response())
        mapped = pipeline.v1_compact_to_resume_json(
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

    def test_v2_compact_to_resume_json_preserves_ghi_first_for_docx(self):
        compact = {
            "type": "AIML",
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "Global Health Impact",
                    "bullets": ["Built Python model workflows for researchers."],
                },
                {
                    "title": "Software Engineer II",
                    "company": "Tata Consultancy Services",
                    "bullets": ["Built Java services for enterprise users."],
                },
            ],
            "projects": [],
            "skills": ["Python", "Java"],
        }
        mapped = pipeline.v1_compact_to_resume_json(
            compact,
            pipeline.ResumeInput(company="Acme", title="AI Engineer", jd="Build ML systems"),
            "v2",
        )

        self.assertEqual(mapped["config"]["experience_order"], "json_order")
        self.assertEqual(mapped["professional_experience"][0]["company"], "Global Health Impact")

    def test_v1_validator_rejects_missing_experience(self):
        bad_response = (
            "```json\n"
            "{\"technical_skills\": {\"row1\": [\"React\", \"TypeScript\"], \"row2\": [\"Java\"]}}\n"
            "```"
        )
        error = pipeline.validate_v1_compact_response(bad_response)
        self.assertIn("include experience", error or "")

    def test_v1_validator_accepts_compact_schema(self):
        self.assertIsNone(pipeline.validate_v1_compact_response(valid_v1_compact_response()))

    def test_v1_validator_accepts_compact_schema_without_type(self):
        response = valid_v1_compact_response().replace("\"type\": \"Backend\", ", "")
        self.assertIsNone(pipeline.validate_v1_compact_response(response))

    def test_v1_validator_accepts_extra_metadata_and_optional_skills(self):
        response = (
            "```json\n"
            "{\"analysis\": \"ok\", \"experience\": [], \"projects\": [], \"notes\": \"diagnostic\"}\n"
            "```"
        )
        self.assertIsNone(pipeline.validate_v1_compact_response(response))

    def test_v1_mapper_accepts_professional_experience_shape(self):
        mapped = pipeline.v1_compact_to_resume_json(
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
        self.assertEqual(mapped["technical_skills"], {"Skills": "Java, Spring Boot"})

    def test_v1_compact_to_resume_json_adds_locked_resume_fields(self):
        compact = pipeline.extract_json(valid_v1_compact_response())
        mapped = pipeline.v1_compact_to_resume_json(
            compact,
            pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs", words="Boston, MA"),
        )
        self.assertEqual(mapped["config"]["prompt_profile"], "v1")
        self.assertEqual(mapped["config"]["company"], "Acme")
        self.assertIn("(518) 328-3697", mapped["contact"])
        self.assertIn(f"Moving to Boston, MA in {pipeline.next_month_label()}; available to move sooner if needed", mapped["location"])
        self.assertEqual(mapped["professional_experience"][0]["dates"], "Oct 2022 - Dec 2024")
        self.assertEqual(mapped["projects"][0]["github_url"], "https://github.com/kevalshah0612/jobpulse")

    def test_v1_resume_location_defaults_to_current_location(self):
        compact = pipeline.extract_json(valid_v1_compact_response())
        mapped = pipeline.v1_compact_to_resume_json(
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
                prompt_profile="v2",
                pass1_text="DES 1 | keyword: Kafka | use when: event processing",
                approval_text="Approved: 1",
            )
            pipeline.update_des_facts_file(
                path,
                request_id="Acme_Backend_20260630_120000",
                inp=inp,
                prompt_profile="v2",
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

    def test_dropdown_contains_only_two_models_with_both_thinking_modes(self):
        options = pipeline.nvidia_model_options()
        self.assertEqual(len(options), 4)
        self.assertIn("Nemo-on", options)
        self.assertIn("Nemo-off", options)
        resolved = {pipeline.resolve_nvidia_model_option(option) for option in options}
        self.assertEqual(
            resolved,
            {
                ("nvidia/nemotron-3-ultra-550b-a55b", True),
                ("nvidia/nemotron-3-ultra-550b-a55b", False),
                ("deepseek-ai/deepseek-v4-pro", True),
                ("deepseek-ai/deepseek-v4-pro", False),
            },
        )

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
                max_tokens=16384,
            )
        kwargs = create.call_args.kwargs
        self.assertFalse(kwargs["stream"])
        self.assertEqual(kwargs["extra_body"], {"chat_template_kwargs": {"thinking": False}})
        self.assertEqual(response.text, "DeepSeek answer")

    def test_nemotron_streams_with_thinking_and_reasoning_budget(self):
        chunks = [
            SimpleNamespace(
                choices=[SimpleNamespace(
                    delta=SimpleNamespace(content="Nemotron answer"),
                    finish_reason="stop",
                )],
                usage=None,
            )
        ]
        client, create = self.fake_client(chunks)
        with (
            patch("pipeline.get_nvidia_client", return_value=client),
            patch("pipeline.get_nvidia_reasoning_budget", return_value=49152),
        ):
            response = pipeline.call_nvidia_sync(
                system_blocks=[],
                messages=[{"role": "user", "content": "hello"}],
                model="nvidia/nemotron-3-ultra-550b-a55b",
                thinking=True,
                max_tokens=16384,
            )
        kwargs = create.call_args.kwargs
        self.assertTrue(kwargs["stream"])
        self.assertEqual(
            kwargs["extra_body"],
            {
                "chat_template_kwargs": {"enable_thinking": True},
                "reasoning_budget": 49152,
            },
        )
        self.assertEqual(response.text, "Nemotron answer")

    def test_nemotron_thinking_off_omits_reasoning_budget(self):
        client, create = self.fake_client([])
        with patch("pipeline.get_nvidia_client", return_value=client):
            pipeline.call_nvidia_sync(
                system_blocks=[],
                messages=[{"role": "user", "content": "hello"}],
                model="nvidia/nemotron-3-ultra-550b-a55b",
                thinking=False,
                max_tokens=16384,
            )
        self.assertEqual(
            create.call_args.kwargs["extra_body"],
            {"chat_template_kwargs": {"enable_thinking": False}},
        )


class NvidiaRetryTests(unittest.TestCase):
    def run_call(self, responses, validator=pipeline.validate_json_response, cancel_event=None):
        with (
            patch("pipeline.get_provider", return_value="nvidia"),
            patch("pipeline.get_nvidia_model", return_value="nvidia/test"),
            patch("pipeline.get_nvidia_max_attempts", return_value=3),
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

    def test_accepts_complete_json_with_length_finish_reason(self):
        complete = pipeline.NvidiaResponse(
            text=valid_resume_response(),
            usage=EMPTY_USAGE,
            finish_reason="length",
        )
        result, calls = self.run_call([complete])
        self.assertEqual(calls, 1)
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
