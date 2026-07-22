import asyncio
import json
import unittest
from unittest.mock import AsyncMock, patch

import pipeline


OPENING_VERBS = [
    "Built",
    "Developed",
    "Engineered",
    "Designed",
    "Automated",
    "Implemented",
    "Optimized",
    "Diagnosed",
    "Reviewed",
    "Integrated",
    "Evaluated",
    "Validated",
    "Configured",
    "Deployed",
]


def mapper_fixture():
    roles = []
    verb_index = 0
    for role_id, bullet_count in pipeline.V1_POST_MODE_CONFIG["entry_swe"]["roles"]:
        slots = []
        for slot in range(1, bullet_count + 1):
            slots.append({
                "slot": slot,
                "story_id": f"{role_id}-STORY-{slot}",
                "match_strength": "exact",
                "primary_requirement_ids": ["R001"],
                "allowed_technology_terms": ["Python"],
                "allowed_fact_fragments": [f"{OPENING_VERBS[verb_index]} verified workflow"],
                "allowed_metrics": [],
            })
            verb_index += 1
        roles.append({"role_id": role_id, "bullets": slots})
    projects = []
    for project_index in range(2):
        slots = []
        for slot in range(1, 3):
            slots.append({
                "slot": slot,
                "primary_requirement_ids": ["R001"],
                "allowed_fact_fragments": [f"{OPENING_VERBS[verb_index]} verified workflow"],
                "allowed_metrics": [],
            })
            verb_index += 1
        projects.append({
            "rank": project_index + 1,
            "story_id": f"PROJ-{project_index + 1:02d}",
            "name": f"Project {project_index + 1}",
            "allowed_technology_terms": ["Python"],
            "bullets": slots,
        })
    return {
        "resolved_mode": "entry_swe",
        "des_questions": [],
        "experience_plan": roles,
        "project_plan": projects,
        "skills_plan": [
            {
                "category": "Languages",
                "terms": [
                    {
                        "term": "Python",
                        "requirement_ids": ["R001"],
                        "evidence_story_ids": ["TA-STORY-1"],
                        "approved_des_ids": [],
                    }
                ],
            }
        ],
        "summary_plan": {"enabled": False},
    }


def resume_fixture(mapper):
    experiences = []
    checks = []
    verb_index = 0
    mapper_roles = {item["role_id"]: item for item in mapper["experience_plan"]}
    for role_id, bullet_count in pipeline.V1_POST_MODE_CONFIG["entry_swe"]["roles"]:
        identity = pipeline.V1_LOCKED_EXPERIENCE_IDENTITY[role_id]
        bullets = []
        for slot in range(1, bullet_count + 1):
            bullet = f"{OPENING_VERBS[verb_index]} verified workflow"
            bullets.append(bullet)
            checks.append({
                "ref": f"{role_id}.{slot}",
                "story_id": mapper_roles[role_id]["bullets"][slot - 1]["story_id"],
                "requirement_id": "R001",
                "alignment": "direct",
                "word_count": 3,
                "questions_answered": ["what", "how"],
            })
            verb_index += 1
        experiences.append({
            "id": role_id,
            "title": identity["title"],
            "company": identity["company"],
            "location": identity["location"],
            "dates": identity["dates"],
            "bullets": bullets,
        })
    projects = []
    for mapper_project in mapper["project_plan"]:
        bullets = []
        for slot in range(1, 3):
            bullet = f"{OPENING_VERBS[verb_index]} verified workflow"
            bullets.append(bullet)
            checks.append({
                "ref": f"{mapper_project['story_id']}.{slot}",
                "story_id": mapper_project["story_id"],
                "requirement_id": "R001",
                "alignment": "direct",
                "word_count": 3,
                "questions_answered": ["what", "how"],
            })
            verb_index += 1
        projects.append({
            "story_id": mapper_project["story_id"],
            "name": mapper_project["name"],
            "tech": ["Python"],
            "bullets": bullets,
        })
    return {
        "type": "entry_swe",
        "summary": "",
        "coursework": ["Database Systems", "Programming Languages"],
        "experience": experiences,
        "projects": projects,
        "technical_skills": [{"category": "Languages", "skills": ["Python"]}],
        "bullet_checks": checks,
    }


class V1PostValidationFlowTests(unittest.TestCase):
    def test_post_short_controllers_preserve_existing_v1_contract(self):
        ats_controller = pipeline.v1_post_short_controller("POST_V1_ATS_AUDIT")
        optimizer_controller = pipeline.v1_post_short_controller("POST_V1_OPTIMIZATION")

        self.assertIn("RUN MODE: POST_V1_ATS_AUDIT", ats_controller)
        self.assertIn("Audit only", ats_controller)
        self.assertIn("Audit `coursework` after `summary`", ats_controller)
        self.assertIn("above 24 words", ats_controller)
        self.assertIn("approved DES authorizes only its exact", ats_controller)
        self.assertIn("RUN MODE: POST_V1_OPTIMIZATION", optimizer_controller)
        self.assertIn("exactly the same keys", optimizer_controller)
        self.assertIn("Preserve `coursework` after `summary`", optimizer_controller)
        self.assertIn("maximum of 24 words", optimizer_controller)
        self.assertIn("Do not add, remove, or rename keys", optimizer_controller)

        with self.assertRaisesRegex(ValueError, "Unsupported V1 post-composition run mode"):
            pipeline.v1_post_short_controller("UNKNOWN")

    def test_runs_ats_then_optimizer_and_returns_validated_json(self):
        mapper = mapper_fixture()
        resume = resume_fixture(mapper)
        artifacts = []
        with (
            patch(
                "pipeline.call_model",
                new=AsyncMock(side_effect=["# V1 ATS, COVERAGE, AND GAP REPORT", json.dumps(resume)]),
            ) as call_mock,
            patch("pipeline.read_prompt", return_value="story library"),
            patch(
                "pipeline.validate_v1_optimized_resume",
                side_effect=AssertionError("post-Optimizer Python validation must not run"),
            ) as validation_mock,
        ):
            result = asyncio.run(pipeline.run_v1_post_validation(
                pipeline.ResumeInput(
                    company="Acme",
                    title="Software Engineer",
                    jd="Build reliable Python services with production testing and operational ownership.",
                ),
                {"requirements": [{"id": "R001"}]},
                mapper,
                "No DES",
                resume,
                stage_artifact_cb=lambda stage, data, reasoning: artifacts.append(stage),
            ))

        self.assertEqual(2, call_mock.await_count)
        validation_mock.assert_not_called()
        self.assertEqual(resume, result.optimized_resume)
        self.assertEqual(["ats_audit", "optimizer"], artifacts)
        ats_user_text = call_mock.await_args_list[0].kwargs["messages"][0]["content"]
        optimizer_user_text = call_mock.await_args_list[1].kwargs["messages"][0]["content"]
        self.assertIn("RUN MODE: POST_V1_ATS_AUDIT", ats_user_text)
        self.assertIn("# V1 Post-Composition ATS Audit Stage Controller", ats_user_text)
        self.assertIn("RUN MODE: POST_V1_OPTIMIZATION", optimizer_user_text)
        self.assertIn("# V1 Post-Audit Optimizer Stage Controller", optimizer_user_text)
        self.assertIn("ATS_GAP_REPORT", optimizer_user_text)
        self.assertIn("# V1 ATS, COVERAGE, AND GAP REPORT", optimizer_user_text)


if __name__ == "__main__":
    unittest.main()
