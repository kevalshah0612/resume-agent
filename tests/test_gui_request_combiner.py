import tempfile
import unittest
from pathlib import Path

import gui


class RequestCombinerTests(unittest.TestCase):
    def test_v4_jd_parse_uses_canonical_saved_artifact(self):
        self.assertEqual(("02_jd_parse_output.json",), gui.REQUEST_FILE_ALIASES["jd_parse"])

    def test_v4_uses_v3_docx_pdf_renderer_and_renderer_artifact(self):
        self.assertEqual(
            gui.ROOT / "v3_experimental_flow" / "manager_Updated.py",
            gui.manager_script_for_profile("v4"),
        )
        self.assertEqual(("06_v4_renderer_input.json",), gui.REQUEST_FILE_ALIASES["v4_renderer"])

    def test_v4_start_message_uses_des_and_saved_checkpoint_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            request_dir = Path(tmp)
            checkpoints = request_dir / "v4_checkpoints"
            checkpoints.mkdir()
            self.assertTrue(gui.v4_start_message(request_dir).startswith("Step 1/4"))
            (checkpoints / "01_jd_analyzer.json").touch()
            self.assertTrue(gui.v4_start_message(request_dir).startswith("Step 2/4"))
            (checkpoints / "02_story_mapper.json").touch()
            self.assertTrue(gui.v4_start_message(request_dir).startswith("Step 3/4"))
            self.assertTrue(gui.v4_start_message(request_dir, "DES 1 confirmed").startswith("Step 2/4"))

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
