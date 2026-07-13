import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from jsonschema import Draft202012Validator

import pipeline
from v4_system import runtime


def empty_bucket():
    return {
        "required": {"tech": [], "nontech": []},
        "core": {"tech": [], "nontech": []},
        "preferred": {"tech": [], "nontech": []},
    }


def jd_output():
    return {
        "role": "Software Engineer",
        "level": "entry",
        "filters": [],
        "5": empty_bucket(),
        "4": empty_bucket(),
        "3": empty_bucket(),
        "2": empty_bucket(),
    }


def mapper_output(status="ready"):
    questions = []
    if status == "des_required":
        questions = [{
            "des_id": 1,
            "keyword_id": "K001",
            "keyword": "Terraform",
            "bucket": 5,
            "closest_story_id": "TCS-II-04",
            "proposed_use": "release automation",
            "question": "Did you personally use Terraform in this work?",
        }]
    return {
        "status": status,
        "resume_mode": "entry_swe",
        "role": "Software Engineer",
        "level": "entry",
        "keyword_plan": [],
        "experience_plan": [
            {"role_id": "TA", "slots": [
                {"slot": 1, "story_id": "TA-01", "keyword_ids": []},
                {"slot": 2, "story_id": "TA-01", "keyword_ids": []},
            ]},
            {"role_id": "GHI", "slots": [
                {"slot": 1, "story_id": "GHI-01", "keyword_ids": []},
                {"slot": 2, "story_id": "GHI-02", "keyword_ids": []},
                {"slot": 3, "story_id": "GHI-03", "keyword_ids": []},
            ]},
            {"role_id": "TCS_SWE_II", "slots": [
                {"slot": 1, "story_id": "TCS-II-01", "keyword_ids": []},
                {"slot": 2, "story_id": "TCS-II-02", "keyword_ids": []},
                {"slot": 3, "story_id": "TCS-II-03", "keyword_ids": []},
                {"slot": 4, "story_id": "TCS-II-04", "keyword_ids": []},
            ]},
            {"role_id": "TCS_SWE_I", "slots": [
                {"slot": 1, "story_id": "TCS-I-01", "keyword_ids": []},
                {"slot": 2, "story_id": "TCS-I-02", "keyword_ids": []},
            ]},
        ],
        "project_plan": [
            {"rank": 1, "story_id": "PROJ-01", "keyword_ids": [], "score": 10},
            {"rank": 2, "story_id": "PROJ-02", "keyword_ids": [], "score": 9},
        ],
        "skills_keyword_ids": [],
        "des_questions": questions,
        "coverage": {
            "total_keywords": 0,
            "direct": 0,
            "supported_equivalent": 0,
            "candidate_approved": 0,
            "confirmation_required": 0,
            "missing": 0,
            "not_selected": 0,
        },
    }


def writer_output(stage):
    if stage == "experience_writer":
        return {"experience": [], "used_keyword_ids": [], "unused_keyword_ids": []}
    return {"projects": [], "used_keyword_ids": [], "unused_keyword_ids": []}


def final_output():
    return {
        "status": "valid",
        "summary": "",
        "experience": [],
        "projects": [],
        "technical_skills": [],
        "coverage": {
            "placed_keyword_ids": [],
            "skills_only_keyword_ids": [],
            "missing_keyword_ids": [],
            "not_selected_keyword_ids": [],
        },
        "des_questions": [],
        "repairs": [],
    }


class V4CanonicalSystemTests(unittest.TestCase):
    def test_all_design_files_exist_and_legacy_jd_is_removed(self):
        config = runtime.read_json(runtime.V4_ROOT / "system_config.json")
        required = [
            "SYSTEM_DESIGN_FOR_CODEX.md",
            "candidate_profile.json",
            "story.md",
            "approved_des_evidence.json",
            *config["prompt_paths"].values(),
            *config["auxiliary_prompt_paths"].values(),
            *config["output_schema_paths"].values(),
        ]
        for relative in required:
            self.assertTrue((runtime.V4_ROOT / relative).is_file(), relative)
        self.assertFalse((runtime.V4_ROOT / "JD.md").exists())
        design = (runtime.V4_ROOT / "SYSTEM_DESIGN_FOR_CODEX.md").read_text(encoding="utf-8")
        self.assertIn("prompts/01_JD_Analyzer.md", design)
        self.assertIn("legacy one-step V4 file", design)

    def test_v4_questions_are_exact_v3_copy_and_linkedin_is_separate(self):
        v3_questions = (
            runtime.V4_ROOT.parent / "v3_experimental_flow" / "prompts" / "questions.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(
            v3_questions,
            (runtime.V4_ROOT / "questions.md").read_text(encoding="utf-8"),
        )
        linkedin = (runtime.V4_ROOT / "linkedin.md").read_text(encoding="utf-8")
        self.assertIn("RECRUITER LINKEDIN MESSAGE", linkedin)
        self.assertIn("HIRING MANAGER LINKEDIN MESSAGE", linkedin)
        self.assertIn("RECRUITER/HM SEARCH STRINGS", linkedin)

    def test_v4_recruiter_action_uses_standalone_linkedin_prompt(self):
        captured = {}

        async def fake_call_model(**kwargs):
            captured.update(kwargs)
            return "RECRUITER LINKEDIN MESSAGE\nReady"

        resume_input = pipeline.ResumeInput(
            company="Acme",
            title="Software Engineer",
            jd="Build React.js applications.",
            words="New York, NY",
        )
        with patch("pipeline.call_model", new=fake_call_model):
            result = asyncio.run(pipeline.run_recruiter_review(
                jd=resume_input.jd,
                resume1_json={"summary": "Built React.js applications."},
                company=resume_input.company,
                title=resume_input.title,
                inp=resume_input,
                prompt_profile="v4",
            ))

        self.assertEqual("RECRUITER LINKEDIN MESSAGE\nReady", result)
        self.assertIn("V4 LinkedIn Outreach", captured["system_blocks"][0]["text"])
        user_text = captured["messages"][0]["content"]
        self.assertIn("Acme", user_text)
        self.assertIn("Software Engineer", user_text)
        self.assertIn("Build React.js applications.", user_text)
        self.assertIsNone(captured["output_validator"])

    def test_all_five_schemas_are_valid_and_jd_has_bucket_two_without_error_branch(self):
        config = runtime.read_json(runtime.V4_ROOT / "system_config.json")
        for relative in config["output_schema_paths"].values():
            Draft202012Validator.check_schema(runtime.read_json(runtime.V4_ROOT / relative))
        jd_schema = runtime.read_json(runtime.V4_ROOT / config["output_schema_paths"]["jd_analyzer"])
        self.assertEqual(["role", "level", "filters", "5", "4", "3", "2"], jd_schema["required"])
        self.assertNotIn("oneOf", jd_schema)

    def test_story_parser_reads_every_supplied_story(self):
        story_text = (runtime.V4_ROOT / "story.md").read_text(encoding="utf-8")
        catalog = runtime.parse_story_catalog(story_text)
        self.assertEqual(35, len(catalog))
        self.assertEqual("TCS_SWE_II", catalog[0]["role_id"])
        self.assertEqual("PROJ-09", catalog[-1]["story_id"])
        self.assertIn("12,000–14,000 daily uploads", catalog[0]["engineering_story"])

    def test_selected_story_exposes_only_current_mapper_keyword_vocabulary(self):
        context = runtime.load_system_snapshot(
            application_id="story-vocabulary",
            jd="Use React.js",
            model="nvidia/test",
            thinking=True,
        )
        plan = mapper_output()
        plan["keyword_plan"] = [{
            "id": "K001", "keyword": "React.js", "story_id": "TCS-II-04",
        }]
        next(
            role for role in plan["experience_plan"] if role["role_id"] == "TCS_SWE_II"
        )["slots"][3]["keyword_ids"] = ["K001"]

        selected = runtime.selected_stories(context, ["TCS-II-04"], plan)

        self.assertEqual(["React.js"], selected[0]["resume_keywords"])
        self.assertNotIn("Kubernetes", selected[0]["resume_keywords"])

    def test_combined_tcs_profile_is_locked_to_user_values(self):
        profile = runtime.read_json(runtime.V4_ROOT / "candidate_profile.json")
        combined = next(item for item in profile["experience"] if item["role_id"] == "TCS_COMBINED")
        self.assertEqual("Software Engineer II", combined["title"])
        self.assertEqual("Tata Consultancy Services", combined["company"])
        self.assertEqual("Gandhinagar, India", combined["location"])
        self.assertEqual("Mar 2021 - Dec 2024", combined["dates"])

    def test_snapshot_records_all_prompt_and_config_hashes(self):
        snapshot = runtime.load_system_snapshot(
            application_id="test",
            jd="Build APIs",
            model="nvidia/nemotron-3-ultra-550b-a55b",
            thinking=True,
        )
        self.assertEqual(5, len(snapshot["prompts"]))
        self.assertEqual(5, len(snapshot["schemas"]))
        self.assertEqual(64, len(snapshot["config_sha256"]))
        self.assertTrue(all(len(item["sha256"]) == 64 for item in snapshot["prompts"].values()))
        self.assertNotIn("api_key", json.dumps(snapshot).casefold())

    def test_changed_prompt_contract_invalidates_saved_context_and_stage(self):
        with tempfile.TemporaryDirectory() as temporary:
            request_dir = Path(temporary) / "request"
            request_dir.mkdir()
            orchestrator = runtime.V4Orchestrator(
                request_dir=request_dir,
                application_id="fresh-contract",
                model="nvidia/test",
                thinking=True,
            )
            current = orchestrator.ensure_context("Build APIs")
            stale = json.loads(json.dumps(current))
            stale["prompts"]["story_mapper"]["sha256"] = "0" * 64
            runtime.atomic_write_json(orchestrator.context_path, stale)
            runtime.atomic_write_json(orchestrator.pending_des_path, {"questions": []})
            runtime.atomic_write_json(orchestrator.latest_path("story_mapper"), {
                "diagnostics": {
                    "config_sha256": current["config_sha256"],
                    "prompt_sha256": "0" * 64,
                    "output_schema_sha256": current["schemas"]["story_mapper"]["sha256"],
                },
                "output": mapper_output(),
            })

            refreshed = orchestrator.ensure_context("Build APIs")

            self.assertEqual(
                current["prompts"]["story_mapper"]["sha256"],
                refreshed["prompts"]["story_mapper"]["sha256"],
            )
            self.assertFalse(orchestrator.pending_des_path.exists())
            self.assertIsNone(orchestrator.load_stage("story_mapper", refreshed))

    def test_renderer_adapter_uses_locked_profile_and_plain_v3_bullets(self):
        context = runtime.load_system_snapshot(
            application_id="renderer",
            jd="Build Python APIs",
            model="nvidia/nemotron-3-ultra-550b-a55b",
            thinking=True,
        )
        plan = mapper_output()
        plan["keyword_plan"] = [{
            "id": "K001",
            "keyword": "Python",
            "bucket": 5,
            "requirement_status": "required",
            "category": "tech",
            "priority": 100,
            "evidence_state": "direct",
            "confidence": 1,
            "story_id": "PROJ-01",
            "evidence": "Python implementation",
            "target": "project",
        }]
        output = final_output()
        output["experience"] = [{
            "role_id": "TA",
            "title": "Teaching Assistant",
            "company": "Binghamton University",
            "location": "Binghamton, NY",
            "dates": "Aug 2025 - Present",
            "bullets": [{
                "story_id": "TA-01",
                "text": "Guided students through tested software engineering assignments.",
                "keyword_ids": [],
                "word_count": 8,
            }],
        }]
        output["projects"] = [{
            "story_id": "PROJ-01",
            "name": "Bistro AI",
            "bullets": [{
                "story_id": "PROJ-01",
                "text": "Built a Python workflow for structured recommendation evaluation.",
                "keyword_ids": ["K001"],
                "word_count": 9,
            }],
        }]
        output["technical_skills"] = [{"category": "Languages", "keywords": ["Python"]}]
        output["summary"] = "Evidence-grounded summary."

        renderer = runtime.build_v4_renderer_input(context, plan, output)

        self.assertEqual("Keval Shah", renderer["name"])
        self.assertEqual(context["candidate_profile"]["education"], renderer["education"])
        self.assertEqual(
            ["Guided students through tested software engineering assignments."],
            renderer["experience"][0]["bullets"],
        )
        self.assertEqual(["Python"], renderer["projects"][0]["tech"])
        self.assertEqual(["Python"], renderer["technical_skills"][0]["terms"])
        self.assertEqual("Evidence-grounded summary.", renderer["summary"])
        self.assertEqual("v4_v3_renderer_input_v1", renderer["schema_version"])


class V4DesTests(unittest.TestCase):
    def test_des_parser_accepts_ranges_lists_and_trailing_english(self):
        self.assertEqual(([1, 2, 3, 4], "used during releases"), runtime.parse_des_approval("DES 1 to 4 used during releases"))
        self.assertEqual(([1, 3, 5], ""), runtime.parse_des_approval("1, 3, 5"))
        self.assertEqual(([2, 3, 4], "confirmed"), runtime.parse_des_approval("DES 2-4, confirmed"))

    def test_des_persistence_uses_mapper_story_and_deduplicates(self):
        with tempfile.TemporaryDirectory() as temporary:
            approval_path = Path(temporary) / "approved.json"
            approval_path.write_text('{"schema_version":"approved_des_evidence_v1","approvals":[]}', encoding="utf-8")
            questions = mapper_output("des_required")["des_questions"]
            with patch.object(runtime, "DES_APPROVAL_FILE", approval_path):
                created = runtime.persist_des_approvals("1 confirmed", questions)
                repeated = runtime.persist_des_approvals("DES 1", questions)
            self.assertEqual(1, len(created))
            self.assertEqual([], repeated)
            approval = runtime.read_json(approval_path)["approvals"][0]
            self.assertEqual("Terraform", approval["keyword"])
            self.assertEqual("TCS-II-04", approval["story_id"])
            self.assertEqual(1.0, approval["confidence"])

    def test_approval_bank_is_scoped_to_current_jd_and_exact_story(self):
        context = runtime.load_system_snapshot(
            application_id="scope",
            jd="Use React.js",
            model="nvidia/test",
            thinking=True,
        )
        jd = jd_output()
        jd["5"]["required"]["tech"] = ["React.js"]
        approvals = [
            {"keyword": "React.js", "story_id": "PROJ-01"},
            {"keyword": "React.js", "story_id": "PROJ-02"},
            {"keyword": "EKS", "story_id": "TCS-II-04"},
        ]

        jd_scoped = runtime.scope_approvals_to_jd(approvals, jd, context["system_config"])
        self.assertEqual(2, len(jd_scoped))
        self.assertNotIn("EKS", {item["keyword"] for item in jd_scoped})

        plan = mapper_output()
        plan["keyword_plan"] = [{
            "id": "K001", "keyword": "React.js", "bucket": 5,
            "requirement_status": "required", "category": "tech", "priority": 150,
            "evidence_state": "candidate_approved", "confidence": 1,
            "story_id": "PROJ-01", "evidence": "approved", "target": "project",
        }]
        plan_scoped = runtime.scope_approvals_to_plan(jd_scoped, plan)
        self.assertEqual(["PROJ-01"], [item["story_id"] for item in plan_scoped])


class V4StageJsonValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = runtime.load_system_snapshot(
            application_id="checks",
            jd="Build APIs",
            model="nvidia/nemotron-3-ultra-550b-a55b",
            thinking=True,
        )

    def test_stage_validator_accepts_schema_valid_json_without_quality_rejection(self):
        output = jd_output()
        output["5"]["required"]["tech"] = ["Python"]
        output["4"]["core"]["tech"] = ["python"]
        schema = self.context["schemas"]["jd_analyzer"]["schema"]
        validator = runtime.make_stage_validator(
            "jd_analyzer",
            schema,
            self.context,
            {"JOB_DESCRIPTION": "Python"},
        )
        self.assertIsNone(validator(json.dumps(output)))

    def test_experience_schema_accepts_optional_employment_note(self):
        output = writer_output("experience_writer")
        output["experience"].append({
            "role_id": "TCS_SWE_II",
            "title": "Software Engineer II",
            "company": "Tata Consultancy Services",
            "location": "Gandhinagar, India",
            "dates": "Mar 2021 - Dec 2024",
            "employment_note": "Full-time",
            "bullets": [{
                "slot": 1,
                "story_id": "TCS-II-01",
                "text": "Built Java APIs.",
                "keyword_ids": [],
                "word_count": 999,
            }],
        })
        schema = self.context["schemas"]["experience_writer"]["schema"]
        validator = runtime.make_stage_validator(
            "experience_writer",
            schema,
            self.context,
            {
                "SYSTEM_CONFIG": self.context["system_config"],
                "CANDIDATE_PROFILE": self.context["candidate_profile"],
                "MAPPER_PLAN": mapper_output(),
                "SELECTED_EXPERIENCE_STORIES": [],
                "APPROVED_DES_EVIDENCE": [],
            },
        )
        self.assertIsNone(validator(json.dumps(output)))

    def test_mapper_cannot_pause_for_nontechnical_or_nonblocking_des(self):
        output = mapper_output("des_required")
        output["keyword_plan"] = [{
            "id": "K001",
            "keyword": "collaboration",
            "bucket": 3,
            "requirement_status": "core",
            "category": "nontech",
            "priority": 80,
            "evidence_state": "confirmation_required",
            "confidence": 0,
            "story_id": "TCS-II-14",
            "evidence": "",
            "target": "missing",
        }]
        output["coverage"]["total_keywords"] = 1
        output["coverage"]["confirmation_required"] = 1
        errors = runtime.mapper_deterministic_errors(output, self.context, {})
        self.assertTrue(any("nontechnical" in error for error in errors))
        self.assertTrue(any("not blocking" in error for error in errors))

    def test_metric_checker_requires_verbatim_story_metric(self):
        story = next(item for item in self.context["story_catalog"] if item["story_id"] == "TCS-II-01")
        valid = runtime.metric_errors(
            "Reduced transfer latency from 60 seconds to 10 seconds.",
            story["engineering_story"],
            story["story_id"],
        )
        invalid = runtime.metric_errors(
            "Reduced transfer latency from 60 seconds to 8 seconds.",
            story["engineering_story"],
            story["story_id"],
        )
        self.assertEqual([], valid)
        self.assertTrue(any("8 seconds" in error for error in invalid))

    def test_mapper_normalization_restores_exact_jd_wording_and_reuses_same_story_approval(self):
        jd = jd_output()
        jd["5"]["required"]["tech"] = ["React.js"]
        output = mapper_output()
        output["keyword_plan"] = [{
            "id": "K001", "keyword": "React", "bucket": 3,
            "requirement_status": "preferred", "category": "nontech", "priority": 1,
            "evidence_state": "confirmation_required", "confidence": 0,
            "story_id": "PROJ-01", "evidence": "candidate approval", "target": "project",
        }]
        output["skills_keyword_ids"] = []

        normalized = runtime.normalize_stage_output(
            "story_mapper",
            output,
            self.context,
            {
                "JD_ANALYSIS": jd,
                "APPROVED_DES_EVIDENCE": [{"keyword": "react.js", "story_id": "PROJ-01"}],
            },
        )

        keyword = normalized["keyword_plan"][0]
        self.assertEqual("React.js", keyword["keyword"])
        self.assertEqual("tech", keyword["category"])
        self.assertEqual("candidate_approved", keyword["evidence_state"])
        self.assertEqual("ready", normalized["status"])
        self.assertEqual([], normalized["des_questions"])
        self.assertEqual(["K001"], normalized["skills_keyword_ids"])

    def test_mapper_moves_only_blocking_confirmation_to_the_single_des_gate(self):
        jd = jd_output()
        jd["5"]["required"]["tech"] = ["Terraform"]
        jd["3"]["preferred"]["tech"] = ["GraphQL"]
        output = mapper_output()
        output["keyword_plan"] = [
            {
                "id": keyword_id, "keyword": keyword, "bucket": bucket,
                "requirement_status": requirement, "category": "tech", "priority": 1,
                "evidence_state": "confirmation_required", "confidence": 0,
                "story_id": "TCS-II-04", "evidence": "", "target": "missing",
            }
            for keyword_id, keyword, bucket, requirement in (
                ("K001", "Terraform", 5, "required"),
                ("K002", "GraphQL", 3, "preferred"),
            )
        ]

        normalized = runtime.normalize_mapper_output(
            output,
            self.context,
            {"JD_ANALYSIS": jd, "APPROVED_DES_EVIDENCE": []},
        )

        self.assertEqual("des_required", normalized["status"])
        self.assertEqual(["K001"], [item["keyword_id"] for item in normalized["des_questions"]])
        self.assertEqual("missing", normalized["keyword_plan"][1]["evidence_state"])

    def test_validator_filters_skills_to_mapper_ids_and_removes_late_des(self):
        plan = mapper_output()
        plan["keyword_plan"] = [
            {
                "id": "K001", "keyword": "Python", "category": "tech",
                "evidence_state": "direct", "story_id": "PROJ-01",
            },
            {
                "id": "K002", "keyword": "C++", "category": "tech",
                "evidence_state": "supported_equivalent", "story_id": "PROJ-02",
            },
        ]
        plan["skills_keyword_ids"] = ["K001", "K002"]
        output = final_output()
        output["status"] = "des_required"
        output["summary"] = "This must be removed for entry mode."
        output["des_questions"] = [{
            "des_id": 1, "keyword_id": "K999", "keyword": "EKS",
            "closest_story_id": "TCS-II-04", "question": "Used EKS?",
        }]
        output["technical_skills"] = [
            {"category": "Languages", "keywords": ["Python", "EKS"]},
            {"category": "Cloud", "keywords": ["Karpenter", "Python"]},
            {"category": "Languages", "keywords": ["C++"]},
        ]

        normalized = runtime.normalize_validator_output(
            output,
            self.context,
            {"MAPPER_PLAN": plan},
        )

        self.assertEqual("repaired", normalized["status"])
        self.assertEqual("", normalized["summary"])
        self.assertEqual([], normalized["des_questions"])
        self.assertEqual(
            ["Python", "C++"],
            [term for group in normalized["technical_skills"] for term in group["keywords"]],
        )
        self.assertNotIn("EKS", json.dumps(normalized))
        self.assertNotIn("Karpenter", json.dumps(normalized))

    def test_mid_level_summary_uses_dynamic_configured_word_range(self):
        summary = (
            "Software engineer with experience building reliable distributed services, improving production workflows, "
            "collaborating across teams, and delivering scalable systems through disciplined testing, automation, "
            "performance analysis, clear communication, ownership, and careful attention to customer and operational outcomes."
        )
        self.assertEqual(35, runtime.word_count(summary))
        plan = mapper_output()
        plan["resume_mode"] = "mid_swe"
        output = final_output()
        output["summary"] = summary

        normalized = runtime.normalize_validator_output(output, self.context, {"MAPPER_PLAN": plan})
        errors = runtime.stage_contract_errors(
            "validator_repair", normalized, self.context, {"MAPPER_PLAN": plan}
        )

        self.assertEqual(summary, normalized["summary"])
        self.assertEqual([], errors)


class V4OrchestrationTests(unittest.TestCase):
    def test_call_stage_reports_the_actual_step_before_the_model_call(self):
        reported = []
        with tempfile.TemporaryDirectory() as temporary:
            request_dir = Path(temporary) / "request"
            request_dir.mkdir()
            orchestrator = runtime.V4Orchestrator(
                request_dir=request_dir,
                application_id="status",
                model="nvidia/test",
                thinking=True,
                stage_cb=lambda step, stage: reported.append((step, stage)),
            )
            context = orchestrator.ensure_context("Build APIs")
            with patch(
                "v4_system.runtime.pipeline.call_model",
                new=AsyncMock(return_value=json.dumps(jd_output())),
            ):
                asyncio.run(orchestrator.call_stage(
                    "jd_analyzer",
                    {"JOB_DESCRIPTION": "Build APIs"},
                    ("JOB_DESCRIPTION",),
                    context,
                ))

        self.assertEqual([("1", "jd_analyzer")], reported)

    def test_complete_flow_runs_writers_concurrently_and_saves_stage_checkpoints(self):
        calls = []
        active_writers = 0
        maximum_writers = 0

        async def fake_call(orchestrator, stage, inputs, required_keys, context):
            nonlocal active_writers, maximum_writers
            calls.append(stage)
            if stage in {"experience_writer", "project_writer"}:
                active_writers += 1
                maximum_writers = max(maximum_writers, active_writers)
                await asyncio.sleep(0.01)
                active_writers -= 1
            outputs = {
                "jd_analyzer": jd_output(),
                "story_mapper": mapper_output(),
                "experience_writer": writer_output(stage),
                "project_writer": writer_output(stage),
                "validator_repair": final_output(),
            }
            record = {
                "stage": stage,
                "step_number": runtime.STAGE_NUMBERS[stage],
                "completed_at": runtime.utc_now(),
                "inputs": inputs,
                "raw_output": json.dumps(outputs[stage]),
                "output": outputs[stage],
                "diagnostics": {
                    "stage_status": outputs[stage].get("status", "complete"),
                    "config_sha256": context["config_sha256"],
                    "prompt_sha256": context["prompts"][stage]["sha256"],
                    "output_schema_sha256": context["schemas"][stage]["sha256"],
                },
            }
            orchestrator.save_stage(stage, record)
            return record

        with tempfile.TemporaryDirectory() as temporary:
            request_dir = Path(temporary) / "request"
            request_dir.mkdir()
            approvals = Path(temporary) / "approvals.json"
            approvals.write_text('{"schema_version":"approved_des_evidence_v1","approvals":[]}', encoding="utf-8")
            with (
                patch.object(runtime, "DES_APPROVAL_FILE", approvals),
                patch.object(runtime.V4Orchestrator, "call_stage", new=fake_call),
            ):
                result = asyncio.run(runtime.run_v4_application(
                    request_dir=request_dir,
                    application_id="acme",
                    jd="Build APIs",
                    model="nvidia/nemotron-3-ultra-550b-a55b",
                    thinking=True,
                ))
            self.assertEqual("valid", result.status)
            self.assertEqual(2, maximum_writers)
            self.assertEqual(
                ["jd_analyzer", "story_mapper", "experience_writer", "project_writer", "validator_repair"],
                calls,
            )
            self.assertTrue((request_dir / "05_resume_output.json").is_file())
            self.assertTrue((request_dir / "06_v4_renderer_input.json").is_file())
            checkpoints = request_dir / "v4_checkpoints"
            stage_files = [path for path in checkpoints.glob("*.json") if path.name != "00_context.json"]
            self.assertEqual(5, len(stage_files))
            renderer = runtime.read_json(request_dir / "06_v4_renderer_input.json")
            self.assertEqual("v4_v3_renderer_input_v1", renderer["schema_version"])

    def test_mapper_des_pause_is_the_only_stop_and_resume_reuses_jd_checkpoint(self):
        calls = []
        mapper_calls = 0

        async def fake_call(orchestrator, stage, inputs, required_keys, context):
            nonlocal mapper_calls
            calls.append(stage)
            if stage == "story_mapper":
                mapper_calls += 1
            outputs = {
                "jd_analyzer": jd_output(),
                "story_mapper": mapper_output("des_required" if mapper_calls == 1 else "ready"),
                "experience_writer": writer_output(stage),
                "project_writer": writer_output(stage),
                "validator_repair": final_output(),
            }
            record = {
                "stage": stage,
                "step_number": runtime.STAGE_NUMBERS[stage],
                "completed_at": runtime.utc_now(),
                "inputs": inputs,
                "raw_output": json.dumps(outputs[stage]),
                "output": outputs[stage],
                "diagnostics": {
                    "stage_status": outputs[stage].get("status", "complete"),
                    "config_sha256": context["config_sha256"],
                    "prompt_sha256": context["prompts"][stage]["sha256"],
                    "output_schema_sha256": context["schemas"][stage]["sha256"],
                },
            }
            orchestrator.save_stage(stage, record)
            return record

        with tempfile.TemporaryDirectory() as temporary:
            request_dir = Path(temporary) / "request"
            request_dir.mkdir()
            approvals = Path(temporary) / "approvals.json"
            approvals.write_text('{"schema_version":"approved_des_evidence_v1","approvals":[]}', encoding="utf-8")
            with (
                patch.object(runtime, "DES_APPROVAL_FILE", approvals),
                patch.object(runtime.V4Orchestrator, "call_stage", new=fake_call),
            ):
                first = asyncio.run(runtime.run_v4_application(
                    request_dir=request_dir,
                    application_id="acme",
                    jd="Build APIs",
                ))
                second = asyncio.run(runtime.run_v4_application(
                    request_dir=request_dir,
                    application_id="acme",
                    jd="Build APIs",
                    des_reply="DES 1 confirmed",
                ))
            self.assertEqual("des_required", first.status)
            self.assertEqual("valid", second.status)
            self.assertEqual(1, calls.count("jd_analyzer"))
            self.assertEqual(2, calls.count("story_mapper"))
            self.assertFalse((request_dir / "v4_checkpoints" / "pending_des.json").exists())


if __name__ == "__main__":
    unittest.main()
