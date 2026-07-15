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
            self.assertEqual("New York, NY", metadata["location"])
            self.assertEqual("Kafka evidence", metadata["initial des"])
            self.assertEqual("False", metadata["nvidia thinking"])
            self.assertFalse(gui.saved_setting_enabled(metadata["nvidia thinking"]))
            self.assertEqual(
                "Build reliable backend services and distributed systems.",
                jd,
            )
            self.assertNotIn("must_not_be_loaded", jd)

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
