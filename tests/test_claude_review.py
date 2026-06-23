import asyncio
import copy
import json
import unittest
from unittest.mock import AsyncMock, patch

import manager
import pipeline


def sample_resume() -> dict:
    return {
        "config": {
            "type": "backend",
            "level": 2,
            "layout_profile": "student_entry",
            "ta_active": False,
        },
        "name": "Keval Shah",
        "contact": "Software Engineer | New York, NY\nphone | email | LinkedIn | GitHub",
        "linkedin_url": "https://linkedin.example",
        "github_url": "https://github.example",
        "summary": "Software engineer building production systems",
        "skills": {
            "row1_label": "Languages",
            "row1_terms": ["Java", "Python"],
        },
        "education": [
            {
                "university": "Binghamton University",
                "location": "Binghamton, NY",
                "degree": "MS Computer Science",
                "graduation": "Expected Aug 2026",
                "ta_bullet": "",
            }
        ],
        "professional_experience": [
            {
                "company": "Tata Consultancy Services",
                "title": "Software Engineer II",
                "location": "",
                "dates": "Oct 2022 - Present",
                "employment_note": "On approved academic leave in Binghamton, NY for M.S. in Computer Science, AI Specialization",
                "bullets": ["Built Java services", "Supported production releases"],
            },
            {
                "company": "Global Health Impact Project",
                "title": "Software Engineer",
                "location": "New York, NY",
                "dates": "2025",
                "employment_note": "",
                "bullets": ["Built health data pipelines", "Improved reporting workflows"],
            },
            {
                "company": "Binghamton University",
                "title": "Teaching Assistant",
                "location": "Binghamton, NY",
                "dates": "2025",
                "employment_note": "",
                "bullets": ["Taught database systems"],
            },
        ],
        "projects": [
            {
                "name": "Resume Agent",
                "tech_label": "Python",
                "github_url": "https://github.example/resume",
                "bullets": ["Built a resume workflow", "Generated structured JSON"],
            }
        ],
    }


class RenderProfileTests(unittest.TestCase):
    def test_student_layout_uses_renderer_section_and_experience_order(self):
        profile = manager.build_render_profile(sample_resume())

        self.assertEqual(
            profile["rendered_section_order"],
            ["education", "skills", "experience", "projects"],
        )
        self.assertEqual(
            [item["company"] for item in profile["experience_order"]],
            ["Global Health Impact Project", "Tata Consultancy Services", "Binghamton University"],
        )
        self.assertFalse(profile["ta_bullet_rendered_under_education"])


class FinalQACandidateValidationTests(unittest.TestCase):
    def test_allows_supported_text_rewrites_with_same_structure(self):
        source = sample_resume()
        candidate = copy.deepcopy(source)
        candidate["summary"] = "Backend engineer building production Java systems"
        candidate["professional_experience"][0]["bullets"][0] = "Built production Java services"

        pipeline.validate_final_review_candidate(source, candidate)

    def test_rejects_changed_role_identity(self):
        source = sample_resume()
        candidate = copy.deepcopy(source)
        candidate["professional_experience"][0]["title"] = "Senior Software Engineer"

        with self.assertRaisesRegex(ValueError, "locked experience field"):
            pipeline.validate_final_review_candidate(source, candidate)

    def test_rejects_changed_bullet_count(self):
        source = sample_resume()
        candidate = copy.deepcopy(source)
        candidate["professional_experience"][0]["bullets"].append("Added unsupported bullet")

        with self.assertRaisesRegex(ValueError, "list length"):
            pipeline.validate_final_review_candidate(source, candidate)

    def test_rejects_changed_layout_config(self):
        source = sample_resume()
        candidate = copy.deepcopy(source)
        candidate["config"]["layout_profile"] = "mid"

        with self.assertRaisesRegex(ValueError, "locked config"):
            pipeline.validate_final_review_candidate(source, candidate)

    def test_restores_accidental_identity_mutation_and_keeps_safe_edits(self):
        source = sample_resume()
        candidate = copy.deepcopy(source)
        candidate["contact"] = candidate["contact"].replace("phone", "wrong phone")
        candidate["summary"] = "Backend engineer building production Java systems"

        restored, changes = pipeline.restore_final_review_locks(source, candidate)

        self.assertEqual(restored["contact"], source["contact"])
        self.assertEqual(restored["summary"], candidate["summary"])
        self.assertIn("contact", changes)
        pipeline.validate_final_review_candidate(source, restored)


class FinalReviewFlowTests(unittest.TestCase):
    def test_runs_three_nvidia_stages_and_returns_final_json(self):
        source = sample_resume()
        repaired = copy.deepcopy(source)
        repaired["summary"] = "Backend engineer building production Java systems"
        final = copy.deepcopy(repaired)
        final["professional_experience"][0]["bullets"][0] = "Built production Java services"
        final["contact"] = final["contact"].replace("phone", "wrong phone")
        responses = [
            "RESUME AUDIT\nMatch score: 82/100",
            "REPAIR SUMMARY\n- Tightened summary\n```json\n" + json.dumps(repaired) + "\n```",
            "FINAL QA SUMMARY\n- ATS verdict: PASS\n```json\n" + json.dumps(final) + "\n```",
        ]
        progress = []
        artifacts = []

        with (
            patch("pipeline.call_model", new=AsyncMock(side_effect=responses)) as call_mock,
            patch("pipeline.get_nvidia_model", return_value="nvidia/test"),
        ):
            result = asyncio.run(
                pipeline.run_final_review(
                    jd="Backend Java role " * 10,
                    source_resume_json=source,
                    progress_cb=lambda step, message: progress.append((step, message)),
                    artifact_cb=lambda kind, value: artifacts.append(kind),
                )
            )

        expected_final = copy.deepcopy(final)
        expected_final["contact"] = source["contact"]
        self.assertEqual(result.final_json, expected_final)
        self.assertEqual(result.restored_locks, ["contact"])
        self.assertEqual(call_mock.await_count, 3)
        for call in call_mock.await_args_list:
            self.assertEqual(call.kwargs["provider_override"], "nvidia")
            self.assertEqual(call.kwargs["model_override"], "nvidia/test")
        self.assertEqual([step for step, _message in progress], [1, 2, 3, 3])
        self.assertEqual(
            artifacts,
            ["render_profile", "audit_raw", "repair_raw", "repaired_json", "final_scan_raw", "final_json"],
        )


if __name__ == "__main__":
    unittest.main()
