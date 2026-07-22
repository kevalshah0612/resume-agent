import json
import tempfile
import unittest
from pathlib import Path

import gui


class RequestCombinerTests(unittest.TestCase):

    def test_reads_v1_json_request_inputs_without_generated_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            request_dir = Path(tmp)
            (request_dir / "00_request.json").write_text(
                '{"request_id":"old","company":"Acme","title":"Backend Engineer",'
                '"link":"https://example.com/jobs/123",'
                '"location":"New York, NY","initial_des":"Kafka evidence",'
                '"prompt_profile":"v1","nvidia_model":"z-ai/glm-5.2",'
                '"nvidia_thinking":false}',
                encoding="utf-8",
            )
            (request_dir / "01_job_description.txt").write_text(
                "Build reliable backend services and distributed systems.",
                encoding="utf-8",
            )
            (request_dir / "05_resume_v3.json").write_text(
                '{"must_not_be_loaded":true}',
                encoding="utf-8",
            )

            metadata, jd = gui.read_saved_request_inputs(request_dir)

            self.assertEqual("Acme", metadata["company"])
            self.assertEqual("Backend Engineer", metadata["title"])
            self.assertEqual("https://example.com/jobs/123", metadata["link"])
            self.assertEqual("New York, NY", metadata["location"])
            self.assertEqual("Kafka evidence", metadata["initial des"])
            self.assertEqual("False", metadata["nvidia thinking"])
            self.assertFalse(gui.saved_setting_enabled(metadata["nvidia thinking"]))
            self.assertEqual(
                "Build reliable backend services and distributed systems.",
                jd,
            )
            self.assertNotIn("must_not_be_loaded", jd)

    def test_formats_and_saves_the_entire_v1_resume_object(self):
        compact_resume = {
            "type": "mid_swe",
            "summary": "Backend engineer building reliable distributed systems.",
            "coursework": [],
            "experience": [
                {
                    "id": "TCS_SWE_II",
                    "title": "Software Engineer II",
                    "company": "Tata Consultancy Services",
                    "location": "Gandhinagar, India",
                    "dates": "Oct 2022 - Dec 2024",
                    "bullets": ["Built reliable Java services for production workflows."],
                }
            ],
            "projects": [
                {
                    "story_id": "PROJ-JOBPULSE",
                    "name": "JobPulse",
                    "tech": ["Java", "PostgreSQL"],
                    "bullets": ["Developed job-search APIs backed by PostgreSQL."],
                }
            ],
            "technical_skills": [
                {"category": "Languages", "skills": ["Java", "Python", "SQL"]}
            ],
            "bullet_checks": [
                {
                    "ref": "TCS_SWE_II.1",
                    "story_id": "TCS-II-01",
                    "requirement_id": "R001",
                    "alignment": "direct",
                    "word_count": 8,
                    "questions_answered": ["what", "with_what", "result"],
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmp:
            request_dir = Path(tmp)
            compact_path, full_path = gui.save_v1_resume_files(
                request_dir,
                compact_resume,
                gui.ResumeInput(
                    company="Acme",
                    title="Backend Engineer",
                    jd="Build reliable backend services and distributed systems.",
                    words="Boston, MA",
                ),
            )
            saved_compact = json.loads(compact_path.read_text(encoding="utf-8"))
            saved_json = full_path.read_text(encoding="utf-8")
            full_resume = json.loads(saved_json)
            display = gui.format_v1_resume_output(
                "Acme",
                "Backend Engineer",
                "https://example.com/jobs/123",
                saved_json,
            )
            preferred_path = gui.existing_request_file_for_key(request_dir, "v1_resume_json")

        header, displayed_json = display.split("Resume JSON:\n", 1)
        self.assertEqual(
            header,
            (
                "Company Name: Acme\n"
                "Title: Backend Engineer\n"
                "Link: https://example.com/jobs/123\n\n"
            ),
        )
        self.assertEqual(saved_compact, compact_resume)
        self.assertEqual(json.loads(displayed_json), full_resume)
        self.assertEqual(full_resume["type"], "Mid")
        self.assertEqual(full_resume["config"]["strategy_type"], "Mid")
        self.assertEqual(full_resume["config"]["prompt_profile"], "v1")
        self.assertEqual(full_resume["name"], "Keval Shah")
        self.assertEqual(
            full_resume["contact"],
            (
                "New York, NY | Moving to Boston, MA | "
                "(607) 235-1181 | keval.shah098@gmail.com | "
                "linkedin.com/in/keval-shah0612"
            ),
        )
        self.assertTrue(full_resume["education"])
        self.assertEqual(full_resume["summary"], compact_resume["summary"])
        self.assertTrue(full_resume["professional_experience"])
        self.assertTrue(full_resume["projects"])
        self.assertTrue(full_resume["technical_skills"])
        self.assertEqual(preferred_path, full_path)

    def test_preserves_expanded_composer_and_optimized_v1_contact_and_type(self):
        composer_resume = {
            "type": "mid_swe",
            "summary": "Original composer summary.",
            "coursework": [],
            "experience": [],
            "projects": [],
            "technical_skills": [],
            "bullet_checks": [],
        }
        optimized_resume = dict(composer_resume)
        optimized_resume["summary"] = "Optimized summary."
        inp = gui.ResumeInput(
            company="Acme",
            title="Backend Engineer",
            jd="Build reliable backend services.",
            words="Boston, MA",
        )

        with tempfile.TemporaryDirectory() as tmp:
            request_dir = Path(tmp)
            composer_compact_path, composer_full_path = gui.save_v1_composer_files(
                request_dir,
                composer_resume,
                inp,
            )
            optimized_compact_path, optimized_full_path = gui.save_v1_resume_files(
                request_dir,
                optimized_resume,
                inp,
            )

            saved_composer_compact = json.loads(composer_compact_path.read_text(encoding="utf-8"))
            saved_composer_full = json.loads(composer_full_path.read_text(encoding="utf-8"))
            saved_optimized_compact = json.loads(optimized_compact_path.read_text(encoding="utf-8"))
            saved_optimized_full = json.loads(optimized_full_path.read_text(encoding="utf-8"))

        self.assertEqual(saved_composer_compact["summary"], "Original composer summary.")
        self.assertEqual(saved_optimized_compact["summary"], "Optimized summary.")
        self.assertEqual(saved_composer_full["summary"], "Original composer summary.")
        self.assertEqual(saved_optimized_full["summary"], "Optimized summary.")
        self.assertEqual(saved_composer_full["contact"], saved_optimized_full["contact"])
        self.assertEqual(saved_composer_full["type"], saved_optimized_full["type"])
        self.assertEqual(saved_composer_full["config"], saved_optimized_full["config"])

    def test_reads_legacy_text_request_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            request_dir = Path(tmp)
            (request_dir / "00_request_details.txt").write_text(
                "Request ID: old\nCompany: Acme\nTitle: Software Engineer\n"
                "Words: Java, SQL\nDES: Existing proof\nPrompt Profile: stable\n",
                encoding="utf-8",
            )
            (request_dir / "01_job_description.txt").write_text(
                "A sufficiently long saved job description for the re-run workflow.",
                encoding="utf-8",
            )

            metadata, jd = gui.read_saved_request_inputs(request_dir)

            self.assertEqual("Acme", metadata["company"])
            self.assertEqual("Java, SQL", metadata["words"])
            self.assertEqual("Existing proof", metadata["des"])
            self.assertIn("saved job description", jd)

    def test_saved_request_inputs_require_metadata_and_jd(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "request details and a job description"):
                gui.read_saved_request_inputs(Path(tmp))



    def test_combines_existing_02_to_07_request_artifacts_in_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            request_dir = Path(tmp)
            (request_dir / "00_request_details.txt").write_text("metadata", encoding="utf-8")
            (request_dir / "01_job_description.txt").write_text("JD text", encoding="utf-8")
            (request_dir / "02_pass1_des_process.txt").write_text("PASS 1 text", encoding="utf-8")
            (request_dir / "03_des_approval.txt").write_text("approval text", encoding="utf-8")
            (request_dir / "04_resume_generation_process.txt").write_text("PASS 2 text", encoding="utf-8")
            (request_dir / "05_resume_output.json").write_text('{"resume": true}', encoding="utf-8")
            (request_dir / "06_recruiter_review_process.txt").write_text("hotdog text", encoding="utf-8")
            (request_dir / "07_recruiter_resume_output.json").write_text('{"final": true}', encoding="utf-8")
            (request_dir / "08_application_questions.txt").write_text("questions", encoding="utf-8")

            combined_path = gui.combine_request_02_to_07(request_dir)

            self.assertEqual(request_dir / gui.COMBINED_02_TO_07_FILE, combined_path)
            combined = combined_path.read_text(encoding="utf-8")
            self.assertIn("===== 02_pass1_des_process.txt =====\nPASS 1 text", combined)
            self.assertIn("===== 05_resume_output.json =====\n{\"resume\": true}", combined)
            self.assertIn("===== 07_recruiter_resume_output.json =====\n{\"final\": true}", combined)
            self.assertNotIn("00_request_details", combined)
            self.assertNotIn("01_job_description", combined)
            self.assertNotIn("08_application_questions", combined)
            self.assertLess(combined.index("02_pass1_des_process"), combined.index("07_recruiter_resume_output"))

    def test_combines_legacy_alias_names_when_current_name_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            request_dir = Path(tmp)
            (request_dir / "02_pass1_des_bank.txt").write_text("legacy PASS 1", encoding="utf-8")

            combined_path = gui.combine_request_02_to_07(request_dir)

            self.assertIsNotNone(combined_path)
            combined = combined_path.read_text(encoding="utf-8")
            self.assertIn("===== 02_pass1_des_bank.txt =====\nlegacy PASS 1", combined)



if __name__ == "__main__":
    unittest.main()
