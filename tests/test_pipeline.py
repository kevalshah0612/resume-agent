import asyncio
import json
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

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
    def test_prompt_profile_options_resolve_to_stable_and_v1(self):
        labels = pipeline.prompt_profile_options()
        self.assertEqual(
            {pipeline.resolve_prompt_profile_label(label) for label in labels},
            {"stable", "v1"},
        )
        self.assertIn("Stable", labels)
        self.assertIn("V1", labels)
        self.assertEqual(pipeline.resolve_prompt_profile_label("v1_experimental_flow"), "v1")
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
        self.assertIn("Resume Generation Prompt", system_text)
        self.assertIn("Hiring Manager Story Contract", system_text)
        self.assertIn("JD:\nBuild APIs", user_text)
        self.assertIn("Company:\nAcme", user_text)
        self.assertIn("Location:\nBoston, MA", user_text)
        self.assertIn("DES (optional):\nUse API work", user_text)

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

    def test_v1_validator_rejects_full_schema(self):
        bad_response = (
            "```json\n"
            "{\"technical_skills\": {\"row1\": [\"React\", \"TypeScript\"], \"row2\": [\"Java\"]}}\n"
            "```"
        )
        error = pipeline.validate_v1_compact_response(bad_response)
        self.assertIn("type, experience, projects, and skills", error or "")

    def test_v1_validator_accepts_compact_schema(self):
        self.assertIsNone(pipeline.validate_v1_compact_response(valid_v1_compact_response()))

    def test_v1_compact_to_resume_json_adds_locked_resume_fields(self):
        compact = pipeline.extract_json(valid_v1_compact_response())
        mapped = pipeline.v1_compact_to_resume_json(
            compact,
            pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Build APIs", words="Boston, MA"),
        )
        self.assertEqual(mapped["config"]["prompt_profile"], "v1")
        self.assertEqual(mapped["config"]["company"], "Acme")
        self.assertIn("(518) 328-3697", mapped["contact"])
        self.assertIn("Moving to Boston by July 2026", mapped["location"])
        self.assertEqual(mapped["professional_experience"][0]["dates"], "Oct 2022 - Present")
        self.assertEqual(mapped["projects"][0]["github_url"], "https://github.com/kevalshah0612/jobpulse")
        self.assertTrue(any(label.startswith("Languages") for label in mapped["technical_skills"]))
        self.assertNotIn("PostgreSQL", json.dumps(mapped["technical_skills"]))

    def test_v1_skills_are_pruned_to_final_bullet_evidence(self):
        compact = {
            "type": "Backend",
            "experience": [
                {
                    "title": "Software Engineer II",
                    "company": "Tata Consultancy Services",
                    "bullets": ["Built Java Spring Boot APIs with JUnit tests and Datadog alerts for release teams."],
                }
            ],
            "projects": [],
            "skills": ["Java", "Spring Boot", "Python", "PostgreSQL", "JUnit", "Datadog", "Code review", "SDLC"],
        }
        mapped = pipeline.v1_compact_to_resume_json(
            compact,
            pipeline.ResumeInput(company="Acme", title="Backend Engineer", jd="Java APIs"),
        )
        rendered = json.dumps(mapped["technical_skills"])
        self.assertIn("Java", rendered)
        self.assertIn("Spring Boot", rendered)
        self.assertIn("JUnit", rendered)
        self.assertIn("Datadog", rendered)
        self.assertNotIn("Python", rendered)
        self.assertNotIn("PostgreSQL", rendered)
        self.assertNotIn("Code review", rendered)
        self.assertLessEqual(sum(len(v.split(", ")) for v in mapped["technical_skills"].values()), 14)


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
            patch("pipeline.get_nvidia_reasoning_budget", return_value=16384),
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
                "reasoning_budget": 16384,
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
