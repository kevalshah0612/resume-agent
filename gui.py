"""
Tabbed GUI for the compact DES-first resume flow.

Use:
  python gui.py
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from app_properties import REQUESTS_DIR, RESUME_STEM, WORD_DIR
from pipeline import (
    CostEvent,
    FinalReviewResult,
    OperationCancelled,
    ResumeInput,
    enforce_linkedin_message_limit,
    extract_json,
    extract_linkedin_message,
    load_config,
    get_default_nvidia_model_option,
    nvidia_model_option_label,
    nvidia_model_options,
    normalize_approval,
    normalize_resume_json,
    prompt_profile_label,
    prompt_profile_options,
    resolve_prompt_profile_label,
    resolve_nvidia_model_option,
    run_application_answers,
    run_final_review,
    run_pass1,
    run_pass2,
    run_recruiter_review,
    save_json,
    save_text,
    slug,
)


ROOT = Path(__file__).parent

REQUEST_FILE_ALIASES = {
    "request": ("00_request_details.txt", "00_request.txt"),
    "jd": ("01_job_description.txt", "01_jd.txt"),
    "des": ("02_pass1_des_process.txt", "02_pass1_des_bank.txt"),
    "approval": ("03_des_approval.txt", "03_approval.txt"),
    "resume_process": ("04_resume_generation_process.txt", "04_final_raw.txt"),
    "resume_json": ("05_resume_output.json", "05_final_resume.json"),
    "recruiter_process": ("06_recruiter_review_process.txt", "06_recruiter_raw.txt"),
    "recruiter_json": ("07_recruiter_resume_output.json", "07_recruiter_final_resume.json"),
    "questions": ("08_application_questions.txt",),
    "answers": ("09_application_answers.txt",),
    "linkedin_combined": ("10_linkedin_outreach.txt", "10_recruiter_linkedin_outreach.txt"),
    "linkedin_recruiter": ("10_recruiter_linkedin_message.txt",),
    "linkedin_manager": ("10_hiring_manager_linkedin_message.txt",),
    "linkedin_search": ("10_recruiter_hm_search_strings.txt",),
    "final_qa_process": ("11_final_qa_process.txt",),
    "final_qa_json": ("12_final_qa_output.json", "18_final_qa_resume.json"),
    "docx_log": ("13_docx_build_log.txt", "06_docx_build.txt"),
    "pdf_log": ("14_pdf_archive_log.txt", "07_pdf_archive.txt"),
}


def open_path(path: Path) -> None:
    try:
        if sys.platform == "win32":
            os.startfile(str(path))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        else:
            subprocess.run(["xdg-open", str(path)], check=False)
    except Exception:
        pass


def run_bg(app: tk.Tk, fn, done) -> None:
    def worker():
        try:
            result = fn()
            app.after(0, lambda result=result: done(result, None))
        except Exception as exc:
            app.after(0, lambda exc=exc: done(None, exc))

    threading.Thread(target=worker, daemon=True).start()


class JobTab(ttk.Frame):
    def __init__(self, app: "ResumeApp", name: str):
        super().__init__(app.notebook, padding=8)
        self.app = app
        self.name = name
        self.request_dir: Path | None = None
        self.final_json_path: Path | None = None
        self.recruiter_json_path: Path | None = None
        self.final_qa_json_path: Path | None = None
        self.docx_path: Path | None = None
        self.cost_events: list[CostEvent] = []
        self.cost_usd = 0.0
        self.request_id = name
        self.stage = "Ready"
        self.pass1_raw = ""
        self.job_description = ""
        self.jd_showing_des = False
        self.cancel_event = threading.Event()

        self._build()

    def _build(self) -> None:
        self.columnconfigure(0, weight=1, uniform="job_panes")
        self.columnconfigure(1, weight=1, uniform="job_panes")
        self.rowconfigure(1, weight=1)

        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        toolbar.columnconfigure(12, weight=1)

        self.pass1_btn = ttk.Button(toolbar, text="PASS 1", command=self.on_pass1)
        self.pass1_btn.grid(row=0, column=0, padx=(0, 6))
        self.auto_btn = ttk.Button(toolbar, text="Auto JSON", command=self.on_auto_json)
        self.auto_btn.grid(row=0, column=1, padx=(0, 6))
        self.json_btn = ttk.Button(toolbar, text="Generate JSON", command=self.on_generate_json)
        self.json_btn.grid(row=0, column=2, padx=(0, 6))
        self.recruiter_btn = ttk.Button(toolbar, text="Recruiter", command=self.on_recruiter_review)
        self.recruiter_btn.grid(row=0, column=3, padx=(0, 6))
        self.final_qa_btn = ttk.Button(toolbar, text="Final QA", command=self.on_final_review)
        self.final_qa_btn.grid(row=0, column=4, padx=(0, 6))
        self.questions_btn = ttk.Button(toolbar, text="Questions", command=self.on_answer_questions)
        self.questions_btn.grid(row=0, column=5, padx=(0, 6))
        self.docx_btn = ttk.Button(toolbar, text="DOCX", command=self.on_build_docx)
        self.docx_btn.grid(row=0, column=6, padx=(0, 6))
        self.pdf_btn = ttk.Button(toolbar, text="PDF", command=self.on_pdf_archive)
        self.pdf_btn.grid(row=0, column=7, padx=(0, 6))
        self.stop_btn = ttk.Button(toolbar, text="Stop", command=self.on_stop_ai, state="disabled")
        self.stop_btn.grid(row=0, column=8, padx=(0, 6))
        ttk.Button(toolbar, text="Load Request", command=self.on_open_request).grid(row=0, column=9, padx=(0, 6))
        ttk.Button(toolbar, text="Open Folder", command=self.on_open_folder).grid(row=0, column=10, padx=(0, 6))
        ttk.Button(toolbar, text="Clear", command=self.on_clear_tab).grid(row=0, column=11, padx=(0, 6))
        self.cost_label = ttk.Label(toolbar, text="$0.0000")
        self.cost_label.grid(row=0, column=13, sticky="e", padx=(8, 8))
        self.status = ttk.Label(toolbar, text="Ready", width=28, anchor="e")
        self.status.grid(row=0, column=14, sticky="e")

        left = ttk.Frame(self)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 6))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(2, weight=1)

        quick_fields = ttk.Frame(left)
        quick_fields.grid(row=0, column=0, sticky="ew")
        quick_fields.columnconfigure(0, weight=1, uniform="quick_fields")
        quick_fields.columnconfigure(1, weight=1, uniform="quick_fields")
        quick_fields.columnconfigure(2, weight=1, uniform="quick_fields")

        self.company = self._field_cell(quick_fields, "Company", 0, 0, height=1)
        self.title_text = self._field_cell(quick_fields, "Title", 0, 1, height=1)
        self.title_text.insert("1.0", "Software Engineer")
        self.words = self._field_cell(quick_fields, "Words / Keywords", 0, 2, height=1)
        self.mode_value = ""
        self.des = self._field_cell(quick_fields, "DES / Existing Evidence", 1, 0, height=2)
        self.approval = self._field_cell(
            quick_fields,
            "DES Approval: 1 to 6 | 1,2,3 | Confirm",
            1,
            1,
            height=2,
        )
        self.approval.insert("1.0", "Approved: ")
        self.app_questions = self._field_cell(quick_fields, "Application Questions", 1, 2, height=2)

        self.jd_title = tk.StringVar(value="Job Description")
        ttk.Label(left, textvariable=self.jd_title).grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.jd = self._text_box(left, 2, height=24, sticky="nsew")

        right = ttk.Frame(self)
        right.grid(row=1, column=1, sticky="nsew", padx=(6, 0))
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        output_header = ttk.Frame(right)
        output_header.grid(row=0, column=0, sticky="ew")
        output_header.columnconfigure(1, weight=1)
        output_header.columnconfigure(6, weight=1)
        self.output_title = tk.StringVar(value="Output")
        ttk.Label(output_header, textvariable=self.output_title).grid(row=0, column=0, sticky="w")
        ttk.Label(output_header, text="Prompt").grid(row=0, column=2, sticky="e", padx=(4, 3))
        self.prompt_selector = ttk.Combobox(
            output_header,
            state="readonly",
            width=8,
            values=prompt_profile_options(),
        )
        self.prompt_selector.grid(row=0, column=3, sticky="e", padx=(0, 4))
        self.prompt_selector.set(prompt_profile_label("stable"))
        self.prompt_selector.bind("<<ComboboxSelected>>", self.on_prompt_profile_selected)
        ttk.Label(output_header, text="Model").grid(row=0, column=4, sticky="e", padx=(4, 3))
        self.model_selector = ttk.Combobox(
            output_header,
            state="readonly",
            width=24,
            values=nvidia_model_options(),
        )
        self.model_selector.grid(row=0, column=5, sticky="e", padx=(0, 4))
        self.model_selector.set(get_default_nvidia_model_option())
        self.model_selector.bind("<<ComboboxSelected>>", self.on_model_selected)
        self.output_selector = ttk.Combobox(output_header, state="readonly", width=24)
        self.output_selector.grid(row=0, column=6, sticky="ew")
        self.output_selector.bind("<<ComboboxSelected>>", self.on_output_selected)
        self.output = self._text_box(right, 1, height=28, sticky="nsew")

    def _labeled_text(self, parent: ttk.Frame, label: str, row: int, height: int) -> tk.Text:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        return self._text_box(parent, row + 1, height=height)

    def _field_cell(self, parent: ttk.Frame, label: str, row: int, column: int, height: int) -> tk.Text:
        cell = ttk.Frame(parent)
        cell.grid(row=row, column=column, sticky="ew", padx=(0 if column == 0 else 6, 6 if column == 0 else 0))
        cell.columnconfigure(0, weight=1)
        ttk.Label(cell, text=label).grid(row=0, column=0, sticky="w")
        box = tk.Text(cell, wrap="word", undo=True, height=height, width=1)
        box.grid(row=1, column=0, sticky="ew", pady=(0, 4))
        self._bind_text_scroll(box)
        return box

    def _text_box(self, parent: ttk.Frame, row: int, height: int, sticky: str = "ew") -> tk.Text:
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky=sticky, pady=(0, 4))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        box = tk.Text(frame, wrap="word", undo=True, height=height, width=1)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=box.yview)
        box.configure(yscrollcommand=scrollbar.set)
        box.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._bind_text_scroll(box)
        return box

    def _bind_text_scroll(self, box: tk.Text) -> None:
        def on_mousewheel(event):
            if event.delta:
                box.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        def on_linux_scroll_up(_event):
            box.yview_scroll(-1, "units")
            return "break"

        def on_linux_scroll_down(_event):
            box.yview_scroll(1, "units")
            return "break"

        box.bind("<MouseWheel>", on_mousewheel)
        box.bind("<Button-4>", on_linux_scroll_up)
        box.bind("<Button-5>", on_linux_scroll_down)

    def text_value(self, box: tk.Text) -> str:
        return box.get("1.0", "end").strip()

    def selected_nvidia_profile(self) -> tuple[str, bool]:
        return resolve_nvidia_model_option(self.model_selector.get())

    def selected_prompt_profile(self) -> str:
        return resolve_prompt_profile_label(self.prompt_selector.get())

    def on_prompt_profile_selected(self, _event=None) -> None:
        self.recruiter_btn.config(
            text="Final Check" if self.selected_prompt_profile() == "v1" else "Recruiter"
        )
        if not self.request_dir:
            return
        self.update_request_metadata({
            "prompt profile": f"Prompt Profile: {self.selected_prompt_profile()}",
        })

    def on_model_selected(self, _event=None) -> None:
        if not self.request_dir:
            return
        model, thinking = self.selected_nvidia_profile()
        self.update_request_metadata({
            "nvidia model": f"NVIDIA Model: {model}",
            "nvidia thinking": f"NVIDIA Thinking: {'ON' if thinking else 'OFF'}",
        })

    def update_request_metadata(self, updates: dict[str, str]) -> None:
        metadata_path = self.existing_request_file("request") or self.request_file("request")
        lines = metadata_path.read_text(encoding="utf-8").splitlines() if metadata_path.exists() else []
        found: set[str] = set()
        for index, line in enumerate(lines):
            key = line.partition(":")[0].strip().lower()
            if key in updates:
                lines[index] = updates[key]
                found.add(key)
        lines.extend(value for key, value in updates.items() if key not in found)
        save_text(metadata_path, "\n".join(lines))

    def existing_request_file(self, key: str, request_dir: Path | None = None) -> Path | None:
        folder = request_dir or self.request_dir
        if not folder:
            return None
        for name in REQUEST_FILE_ALIASES[key]:
            path = folder / name
            if path.exists():
                return path
        return None

    def request_file(self, key: str, request_dir: Path | None = None) -> Path:
        folder = request_dir or self.request_dir
        if not folder:
            raise ValueError("Create or load a request first.")
        return folder / REQUEST_FILE_ALIASES[key][0]

    def show_des_in_jd(self, pass1_text: str) -> None:
        if not self.jd_showing_des:
            current_jd = self.text_value(self.jd)
            if current_jd:
                self.job_description = current_jd
        self.jd.delete("1.0", "end")
        self.jd.insert("1.0", self.format_pass1_display(pass1_text))
        self.jd.see("1.0")
        self.jd_showing_des = True
        self.jd_title.set("PASS 1 - Missing Coverage / DES Suggestions")

    def show_job_description(self, jd: str) -> None:
        self.job_description = jd
        self.jd_showing_des = False
        self.jd_title.set("Job Description")
        self.jd.delete("1.0", "end")
        self.jd.insert("1.0", jd)
        self.jd.see("1.0")

    def artifact_choices(self) -> list[tuple[str, list[Path]]]:
        if not self.request_dir:
            return []
        definitions = [
            ("Model Process | PASS 1 DES", "des"),
            ("Model Process | Resume Generation", "resume_process"),
            ("Output | Resume JSON", "resume_json"),
            ("Model Process | Recruiter Review", "recruiter_process"),
            ("Output | Recruiter Resume JSON", "recruiter_json"),
            ("Input | Application Questions", "questions"),
            ("Output | Application Answers", "answers"),
            ("LinkedIn | Combined Outreach", "linkedin_combined"),
            ("LinkedIn | Recruiter Message", "linkedin_recruiter"),
            ("LinkedIn | Hiring Manager Message", "linkedin_manager"),
            ("LinkedIn | Search Strings", "linkedin_search"),
            ("Model Process | Final QA", "final_qa_process"),
            ("Output | Final QA JSON", "final_qa_json"),
            ("Log | DOCX Build", "docx_log"),
            ("Log | PDF Archive", "pdf_log"),
        ]
        choices: list[tuple[str, list[Path]]] = []
        for label, key in definitions:
            path = self.existing_request_file(key)
            if path:
                choices.append((label, [path]))

        if not self.existing_request_file("final_qa_process"):
            legacy_names = (
                "12_final_qa_render_profile.json",
                "13_final_qa_audit_raw.txt",
                "14_final_qa_repair_raw.txt",
                "16_final_qa_scan_raw.txt",
                "17_final_qa_summary.txt",
            )
            legacy_paths = [self.request_dir / name for name in legacy_names if (self.request_dir / name).exists()]
            if legacy_paths:
                insert_at = next(
                    (index for index, (label, _paths) in enumerate(choices) if label == "Output | Final QA JSON"),
                    len(choices),
                )
                choices.insert(insert_at, ("Model Process | Final QA", legacy_paths))
        return choices

    def refresh_output_choices(self) -> None:
        current = self.output_selector.get()
        values = [label for label, _paths in self.artifact_choices()]
        self.output_selector.configure(values=values)
        if current in values:
            self.output_selector.set(current)
        elif values:
            self.output_selector.set(values[-1])
        else:
            self.output_selector.set("")

    def on_output_selected(self, _event=None) -> None:
        selected = self.output_selector.get()
        entry = next((item for item in self.artifact_choices() if item[0] == selected), None)
        if not entry:
            return
        _label, paths = entry
        sections: list[str] = []
        for path in paths:
            text = path.read_text(encoding="utf-8")
            if len(paths) > 1:
                text = self.response_summary(text)
                sections.append(f"{path.name}\n{'=' * len(path.name)}\n{text}")
            else:
                sections.append(text)
        self.show_output(selected, "\n\n".join(sections), refresh_choices=False)

    def select_output_artifact(self, label: str) -> None:
        self.refresh_output_choices()
        if label in set(self.output_selector.cget("values")):
            self.output_selector.set(label)
            self.on_output_selected()

    def format_pass1_display(self, text: str) -> str:
        lines = text.splitlines()
        coverage: list[str] = []
        des_blocks: list[str] = []
        tail: list[str] = []

        for line in lines:
            stripped = line.strip()
            match = re.match(r"^DES\s*-?\s*(\d+)\s*\|\s*(.*)$", stripped, flags=re.IGNORECASE)
            if not match:
                if des_blocks:
                    tail.append(stripped)
                elif stripped:
                    coverage.append(stripped)
                continue

            des_id, rest = match.groups()
            fields: dict[str, str] = {}
            for part in rest.split(" | "):
                if ":" in part:
                    key, value = part.split(":", 1)
                    fields[key.strip().lower()] = value.strip()

            block = [f"DES {des_id}"]
            for label, key in [
                ("Keyword", "keyword"),
                ("Use when", "use when"),
                ("Bullet", "bullet"),
                ("Story/context", "story/context"),
                ("Number", "number"),
                ("Safe wording", "safe wording"),
            ]:
                value = fields.get(key, "")
                if value:
                    block.append(f"  {label}: {value}")
            if len(block) == 1:
                block.append(f"  {rest.strip()}")
            des_blocks.append("\n".join(block))

        if not des_blocks:
            return text

        output: list[str] = []
        if coverage:
            output.append("COVERAGE SUMMARY")
            output.append("\n".join(coverage).strip())
        output.append("DES CANDIDATES")
        output.append("\n\n".join(des_blocks))
        cleaned_tail = [line for line in tail if line and not line.upper().startswith("DES CANDIDATE BANK")]
        if cleaned_tail:
            output.append("\n".join(cleaned_tail))
        return "\n\n".join(part for part in output if part.strip())

    def extract_linkedin_outreach(self, text: str) -> str:
        without_json = re.sub(r"```json\s*\{.*?\}\s*```", "", text, flags=re.DOTALL | re.IGNORECASE)
        lines = without_json.splitlines()

        def normalized(line: str) -> str:
            clean = re.sub(r"^\s*(?:#+\s*)?(?:\d+[\).]\s*)?", "", line).strip().lower()
            return clean.strip("*: ")

        def is_outreach_heading(line: str) -> bool:
            clean = normalized(line)
            return (
                ("linkedin" in clean and ("message" in clean or "outreach" in clean or "connection" in clean))
                or ("connection message" in clean)
                or ("message under 300" in clean)
                or ("recruiter" in clean and "search" in clean and "string" in clean)
                or ("hiring manager" in clean and "search" in clean and "string" in clean)
                or ("hm" in clean and "search" in clean and "string" in clean)
                or clean.startswith("search string")
                or clean.startswith("recruiter search string")
                or ("follow" in clean and "message" in clean)
            )

        start_idx: int | None = None
        for i, line in enumerate(lines):
            if is_outreach_heading(line):
                start_idx = i
                break

        if start_idx is None:
            linkedin_lines = [line for line in lines if "site:linkedin.com/in" in line.lower()]
            return "\n".join(linkedin_lines).strip()

        selected: list[str] = []
        for line in lines[start_idx:]:
            clean = normalized(line)
            if clean.startswith("final json") or line.strip().lower().startswith("```json"):
                break
            selected.append(line.rstrip())
        return "\n".join(selected).strip()

    def clean_paste_text(self, text: str) -> str:
        replacements = {
            "\u2014": "-",
            "\u2013": "-",
            "\u2212": "-",
            "\u2018": "'",
            "\u2019": "'",
            "\u201c": '"',
            "\u201d": '"',
            "\u2026": "...",
            "\u00a0": " ",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def show_output(self, title: str, text: str, refresh_choices: bool = True) -> None:
        self.output_title.set(title)
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text.strip())
        self.output.see("1.0")
        if refresh_choices:
            self.refresh_output_choices()

    def response_summary(self, raw_text: str) -> str:
        without_json = re.sub(
            r"```json\s*\{.*?\}\s*```",
            "",
            raw_text,
            flags=re.DOTALL | re.IGNORECASE,
        )
        return self.clean_paste_text(without_json).strip()

    def show_and_save_linkedin_outreach(
        self,
        request_dir: Path,
        raw_text: str,
        filename: str = "10_linkedin_outreach.txt",
    ) -> bool:
        outreach = self.clean_paste_text(self.extract_linkedin_outreach(raw_text))
        outreach = enforce_linkedin_message_limit(outreach)
        if not outreach:
            return False
        self.show_output("LinkedIn Outreach / Recruiter Search", outreach)
        save_text(request_dir / filename, outreach)
        recruiter_message = extract_linkedin_message(outreach, "recruiter")
        hiring_manager_message = extract_linkedin_message(outreach, "hiring_manager")
        search_strings = "\n".join(
            line.strip() for line in outreach.splitlines() if "site:linkedin.com/in" in line.lower()
        )
        if recruiter_message:
            save_text(request_dir / "10_recruiter_linkedin_message.txt", recruiter_message)
        if hiring_manager_message:
            save_text(request_dir / "10_hiring_manager_linkedin_message.txt", hiring_manager_message)
        if search_strings:
            save_text(request_dir / "10_recruiter_hm_search_strings.txt", search_strings)
        self.refresh_output_choices()
        return True

    def make_input(self) -> ResumeInput:
        company = self.text_value(self.company)
        if self.jd_showing_des:
            jd = self.job_description
        else:
            jd = self.text_value(self.jd)
            self.job_description = jd
        if not company:
            raise ValueError("Company is required.")
        if len(jd) < 50:
            raise ValueError("Paste the full JD first.")
        return ResumeInput(
            company=company,
            title=self.text_value(self.title_text) or "Software Engineer",
            jd=jd,
            words=self.text_value(self.words),
            mode=self.mode_value,
            des=self.text_value(self.des),
        )

    def request_label(self, inp: ResumeInput | None = None) -> str:
        if inp is None:
            company = self.text_value(self.company) or "Company"
            title = self.text_value(self.title_text) or "Software Engineer"
        else:
            company = inp.company
            title = inp.title
        return f"{self.request_id} | {company} | {title}"

    def tab_caption(self) -> str:
        stage = self.stage.replace(" running...", "").replace(" ready", "").replace(" failed", " failed")
        return f"{self.request_id} | {stage}"[:36]

    def set_stage(self, message: str) -> None:
        self.stage = message
        self.status.config(text=message)
        self.app.rename_tab(self, self.tab_caption())
        self.app.update_tab_status(self)
        print(f"STATUS | {self.request_label()} | {message}")

    def ensure_request_dir(self, inp: ResumeInput) -> Path:
        if self.request_dir:
            return self.request_dir
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.request_id = f"{slug(inp.company)}_{slug(inp.title or 'Software_Engineer')}_{stamp}"
        self.request_dir = REQUESTS_DIR / self.request_id
        self.request_dir.mkdir(parents=True, exist_ok=True)
        nvidia_model, nvidia_thinking = self.selected_nvidia_profile()
        prompt_profile = self.selected_prompt_profile()
        save_text(
            self.request_file("request"),
            "\n".join([
                f"Request ID: {self.request_id}",
                f"Company: {inp.company}",
                f"Title: {inp.title}",
                f"Words: {inp.words}",
                f"DES: {inp.des}",
                f"Prompt Profile: {prompt_profile}",
                f"NVIDIA Model: {nvidia_model}",
                f"NVIDIA Thinking: {'ON' if nvidia_thinking else 'OFF'}",
            ]),
        )
        save_text(self.request_file("jd"), inp.jd)
        self.app.rename_tab(self, self.tab_caption())
        self.app.update_tab_status(self)
        return self.request_dir

    def set_busy(self, busy: bool, message: str, cancellable: bool = False) -> None:
        state = "disabled" if busy else "normal"
        for button in (
            self.pass1_btn,
            self.auto_btn,
            self.json_btn,
            self.recruiter_btn,
            self.final_qa_btn,
            self.docx_btn,
            self.pdf_btn,
            self.questions_btn,
        ):
            button.config(state=state)
        self.model_selector.configure(state="disabled" if busy else "readonly")
        self.prompt_selector.configure(state="disabled" if busy else "readonly")
        if busy and cancellable:
            self.cancel_event.clear()
            self.stop_btn.config(state="normal")
        else:
            self.stop_btn.config(state="disabled")
        self.set_stage(message)

    def on_stop_ai(self) -> None:
        if self.stop_btn.instate(["disabled"]):
            return
        self.cancel_event.set()
        self.stop_btn.config(state="disabled")
        self.set_stage("Stopping AI...")

    def handle_cancelled(self, err: Exception | None) -> bool:
        if not isinstance(err, OperationCancelled):
            return False
        self.set_busy(False, "Stopped. You can retry manually.")
        return True

    def add_cost_events(self, events: list[CostEvent]) -> None:
        if not events:
            return
        self.cost_events.extend(events)
        added = sum(e.estimated_cost_usd for e in events)
        self.cost_usd += added
        self.cost_label.config(text=f"${self.cost_usd:.4f}")
        self.app.add_session_cost(added)
        self.app.update_tab_status(self)
        if self.request_dir:
            save_json(
                self.request_dir / "costs.json",
                {
                    "tab_total_usd": round(self.cost_usd, 6),
                    "events": [
                        {
                            "label": e.label,
                            "model": e.model,
                            "input_tokens": e.input_tokens,
                            "output_tokens": e.output_tokens,
                            "cache_creation_input_tokens": e.cache_creation_input_tokens,
                            "cache_read_input_tokens": e.cache_read_input_tokens,
                            "estimated_cost_usd": round(e.estimated_cost_usd, 6),
                            "attempts": e.attempts,
                            "finish_reason": e.finish_reason,
                        }
                        for e in self.cost_events
                    ],
                },
            )

    def on_pass1(self) -> None:
        try:
            inp = self.make_input()
            request_dir = self.ensure_request_dir(inp)
            nvidia_model, nvidia_thinking = self.selected_nvidia_profile()
            prompt_profile = self.selected_prompt_profile()
        except Exception as exc:
            messagebox.showerror("Input needed", str(exc), parent=self)
            return

        self.set_busy(True, "PASS 1 running...", cancellable=True)

        def task():
            events: list[CostEvent] = []
            result = asyncio.run(run_pass1(
                inp,
                cost_cb=events.append,
                request_label=self.request_label(inp),
                cancel_event=self.cancel_event,
                nvidia_model=nvidia_model,
                nvidia_thinking=nvidia_thinking,
                prompt_profile=prompt_profile,
            ))
            return result, events

        def done(result, err):
            if self.handle_cancelled(err):
                return
            self.set_busy(False, "PASS 1 ready" if not err else "PASS 1 failed")
            if err:
                messagebox.showerror("PASS 1 failed", str(err), parent=self)
                return
            result, events = result
            self.pass1_raw = result
            self.show_des_in_jd(result)
            save_text(self.request_file("des", request_dir), result)
            self.show_output("PASS 1", "PASS 1 complete. DES suggestions are pinned in the left panel.")
            self.add_cost_events(events)

        run_bg(self.app, task, done)

    def on_generate_json(self) -> None:
        try:
            inp = self.make_input()
            request_dir = self.ensure_request_dir(inp)
            pass1_text = self.pass1_raw or self.text_value(self.output)
            if not pass1_text:
                raise ValueError("Run PASS 1 first.")
            approval_raw = self.text_value(self.approval)
            approval = normalize_approval(approval_raw)
            nvidia_model, nvidia_thinking = self.selected_nvidia_profile()
            prompt_profile = self.selected_prompt_profile()
        except Exception as exc:
            messagebox.showerror("Missing step", str(exc), parent=self)
            return

        save_text(self.request_file("approval", request_dir), approval_raw + "\n\nNormalized:\n" + approval)
        self.set_busy(True, "Generating JSON...", cancellable=True)

        def task():
            events: list[CostEvent] = []
            raw = asyncio.run(run_pass2(
                inp,
                pass1_text,
                approval,
                cost_cb=events.append,
                request_label=self.request_label(inp),
                cancel_event=self.cancel_event,
                nvidia_model=nvidia_model,
                nvidia_thinking=nvidia_thinking,
                prompt_profile=prompt_profile,
            ))
            save_text(self.request_file("resume_process", request_dir), raw)
            try:
                data = extract_json(raw)
                return raw, data, events, ""
            except Exception as exc:
                save_text(request_dir / "04_resume_generation_error.txt", str(exc))
                return raw, None, events, str(exc)

        def done(result, err):
            if self.handle_cancelled(err):
                return
            self.set_busy(False, "JSON ready" if not err else "Generate call failed")
            if err:
                messagebox.showerror("Generate JSON call failed", str(err), parent=self)
                return
            raw, data, events, parse_error = result
            if not self.show_and_save_linkedin_outreach(request_dir, raw):
                self.show_output("PASS 2 Result", self.response_summary(raw) or "Final resume JSON is ready.")
            self.add_cost_events(events)
            if parse_error:
                self.set_stage("Raw response saved; JSON not extracted")
                return
            self.final_json_path = self.request_file("resume_json", request_dir)
            save_json(self.final_json_path, data)
            self.recruiter_json_path = None
            self.final_qa_json_path = None
            self.docx_path = None
            self.select_output_artifact("Output | Resume JSON")
            self.set_stage(f"JSON: {self.final_json_path.name}")

        run_bg(self.app, task, done)

    def approve_all_des_text(self, pass1_text: str) -> str:
        numbers = [int(n) for n in re.findall(r"(?im)^\s*DES\s*-?\s*(\d+)\b", pass1_text)]
        if not numbers:
            numbers = [int(n) for n in re.findall(r"\bDES\s*-?\s*(\d+)\b", pass1_text, flags=re.IGNORECASE)]
        unique = sorted(set(numbers))
        if not unique:
            return "Confirm"
        return "Approved: " + ",".join(str(n) for n in unique)

    def on_auto_json(self) -> None:
        try:
            inp = self.make_input()
            request_dir = self.ensure_request_dir(inp)
            nvidia_model, nvidia_thinking = self.selected_nvidia_profile()
            prompt_profile = self.selected_prompt_profile()
        except Exception as exc:
            messagebox.showerror("Input needed", str(exc), parent=self)
            return

        self.set_busy(True, "AUTO running PASS 1...", cancellable=True)

        def task():
            events: list[CostEvent] = []
            pass1_raw = asyncio.run(run_pass1(
                inp,
                cost_cb=events.append,
                request_label=self.request_label(inp),
                cancel_event=self.cancel_event,
                nvidia_model=nvidia_model,
                nvidia_thinking=nvidia_thinking,
                prompt_profile=prompt_profile,
            ))
            approval_raw = self.approve_all_des_text(pass1_raw)
            approval = normalize_approval(approval_raw)
            pass2_raw = asyncio.run(run_pass2(
                inp,
                pass1_raw,
                approval,
                cost_cb=events.append,
                request_label=self.request_label(inp),
                cancel_event=self.cancel_event,
                nvidia_model=nvidia_model,
                nvidia_thinking=nvidia_thinking,
                prompt_profile=prompt_profile,
            ))
            save_text(self.request_file("resume_process", request_dir), pass2_raw)
            try:
                data = extract_json(pass2_raw)
                return pass1_raw, approval_raw, approval, pass2_raw, data, events, ""
            except Exception as exc:
                save_text(request_dir / "04_resume_generation_error.txt", str(exc))
                return pass1_raw, approval_raw, approval, pass2_raw, None, events, str(exc)

        def done(result, err):
            if self.handle_cancelled(err):
                return
            self.set_busy(False, "AUTO JSON ready" if not err else "AUTO call failed")
            if err:
                messagebox.showerror("Auto JSON call failed", str(err), parent=self)
                return
            pass1_raw, approval_raw, approval, pass2_raw, data, events, parse_error = result
            self.pass1_raw = pass1_raw
            self.approval.delete("1.0", "end")
            self.approval.insert("1.0", approval_raw)
            save_text(self.request_file("des", request_dir), pass1_raw)
            save_text(self.request_file("approval", request_dir), approval_raw + "\n\nNormalized:\n" + approval)
            self.show_des_in_jd(pass1_raw)
            if not self.show_and_save_linkedin_outreach(request_dir, pass2_raw):
                self.show_output("AUTO JSON Result", self.response_summary(pass2_raw) or "Final resume JSON is ready.")
            self.add_cost_events(events)
            if parse_error:
                self.set_stage("AUTO raw response saved; JSON not extracted")
                return
            self.final_json_path = self.request_file("resume_json", request_dir)
            save_json(self.final_json_path, data)
            self.recruiter_json_path = None
            self.final_qa_json_path = None
            self.docx_path = None
            self.select_output_artifact("Output | Resume JSON")
            self.set_stage(f"AUTO JSON: {self.final_json_path.name}")

        run_bg(self.app, task, done)

    def on_recruiter_review(self) -> None:
        if not self.final_json_path or not self.final_json_path.exists():
            path = filedialog.askopenfilename(
                title="Choose resume JSON for recruiter review",
                filetypes=[("JSON", "*.json")],
                initialdir=str(self.request_dir or REQUESTS_DIR),
            )
            if not path:
                return
            self.final_json_path = Path(path)

        try:
            inp = self.make_input()
            request_dir = self.ensure_request_dir(inp)
            resume_json = normalize_resume_json(json.loads(self.final_json_path.read_text(encoding="utf-8")))
            approval = self.text_value(self.approval)
            nvidia_model, nvidia_thinking = self.selected_nvidia_profile()
            prompt_profile = self.selected_prompt_profile()
        except Exception as exc:
            messagebox.showerror("Recruiter review needs input", str(exc), parent=self)
            return

        self.set_busy(
            True,
            "Final check running..." if prompt_profile == "v1" else "Recruiter review running...",
            cancellable=True,
        )

        def task():
            events: list[CostEvent] = []
            raw = asyncio.run(run_recruiter_review(
                jd=inp.jd,
                resume1_json=resume_json,
                company=inp.company,
                title=inp.title,
                des=approval,
                cost_cb=events.append,
                request_label=self.request_label(inp),
                cancel_event=self.cancel_event,
                nvidia_model=nvidia_model,
                nvidia_thinking=nvidia_thinking,
                prompt_profile=prompt_profile,
                pass1_audit=self.pass1_raw,
            ))
            save_text(self.request_file("recruiter_process", request_dir), raw)
            try:
                data = extract_json(raw)
                return raw, data, events, ""
            except Exception as exc:
                save_text(request_dir / "06_recruiter_review_error.txt", str(exc))
                return raw, None, events, str(exc)

        def done(result, err):
            if self.handle_cancelled(err):
                return
            ready_message = "Final check JSON ready" if prompt_profile == "v1" else "Recruiter JSON ready"
            failed_message = "Final check failed" if prompt_profile == "v1" else "Recruiter call failed"
            self.set_busy(False, ready_message if not err else failed_message)
            if err:
                title = "Final check failed" if prompt_profile == "v1" else "Recruiter review call failed"
                messagebox.showerror(title, str(err), parent=self)
                return
            raw, data, events, parse_error = result
            if not self.show_and_save_linkedin_outreach(request_dir, raw):
                title = "Final Check" if prompt_profile == "v1" else "Recruiter Review"
                fallback = "Final check JSON is ready." if prompt_profile == "v1" else "Recruiter JSON is ready."
                self.show_output(title, self.response_summary(raw) or fallback)
            self.add_cost_events(events)
            if parse_error:
                self.set_stage("Final check raw response saved; JSON not extracted" if prompt_profile == "v1" else "Recruiter raw response saved; JSON not extracted")
                return
            self.recruiter_json_path = self.request_file("recruiter_json", request_dir)
            save_json(self.recruiter_json_path, data)
            self.final_qa_json_path = None
            self.final_json_path = self.recruiter_json_path
            self.select_output_artifact("Output | Recruiter Resume JSON")
            label = "Final check JSON" if prompt_profile == "v1" else "Recruiter JSON"
            self.set_stage(f"{label}: {self.recruiter_json_path.name}")

        run_bg(self.app, task, done)

    def best_resume_json_path(self) -> Path | None:
        if self.final_qa_json_path and self.final_qa_json_path.exists():
            return self.final_qa_json_path
        if self.recruiter_json_path and self.recruiter_json_path.exists():
            return self.recruiter_json_path
        if self.final_json_path and self.final_json_path.exists():
            return self.final_json_path
        return None

    def format_final_review_display(
        self,
        result: FinalReviewResult,
        source_path: Path,
        final_path: Path,
    ) -> str:
        def summary_only(raw: str) -> str:
            return re.sub(r"```json.*?```", "", raw, flags=re.DOTALL | re.IGNORECASE).strip()

        profile = result.render_profile
        experience_order = "\n".join(
            f"  {item['position']}. {item['company']} - {item['title']}"
            for item in profile.get("experience_order", [])
        ) or "  None"
        lock_note = (
            "Locked fields restored automatically: " + ", ".join(result.restored_locks)
            if result.restored_locks
            else "Locked fields restored automatically: none"
        )
        return "\n\n".join([
            "FINAL QA PROCESS",
            f"Input resume: {source_path.name}",
            "Render plan used by manager.py:\n"
            f"  Type: {profile.get('resume_type')}\n"
            f"  Level: {profile.get('level')} ({profile.get('level_label')})\n"
            f"  Layout: {profile.get('layout_profile')}\n"
            f"  Sections: {', '.join(profile.get('rendered_section_order', []))}\n"
            f"  Experience order:\n{experience_order}",
            "STEP 1 - AUDIT (read-only review):\n" + result.audit_raw.strip(),
            "STEP 2 - REPAIR (candidate edits):\n" + summary_only(result.repair_raw),
            "STEP 3 - FINAL SCAN (independent verification):\n" + summary_only(result.final_scan_raw),
            lock_note,
            f"Final usable output: {final_path.name}",
        ])

    def on_final_review(self) -> None:
        try:
            inp = self.make_input()
            request_dir = self.ensure_request_dir(inp)
            source_path = self.best_resume_json_path()
            if not source_path:
                raise ValueError("Generate resume JSON first. Recruiter JSON is preferred when available.")
            source_json = normalize_resume_json(json.loads(source_path.read_text(encoding="utf-8")))
            nvidia_model, nvidia_thinking = self.selected_nvidia_profile()
        except Exception as exc:
            messagebox.showerror("Final QA needs input", str(exc), parent=self)
            return

        self.set_busy(True, "Final QA 1/3: auditing", cancellable=True)

        def task():
            artifacts: dict[str, object] = {}

            def save_process(status: str, error: Exception | None = None) -> None:
                parts = [
                    "FINAL QA PROCESS",
                    f"Input resume: {source_path.name}",
                    "Step 1: audit the rendered resume without editing it.",
                    "Step 2: repair only evidence-supported text in a candidate JSON.",
                    "Step 3: independently scan the repaired candidate and produce the final JSON.",
                    f"Status: {status}",
                ]
                profile = artifacts.get("render_profile")
                if isinstance(profile, dict):
                    parts.append(
                        "RENDER PLAN\n"
                        f"Type: {profile.get('resume_type')}\n"
                        f"Level: {profile.get('level')} ({profile.get('level_label')})\n"
                        f"Layout: {profile.get('layout_profile')}\n"
                        f"Sections: {', '.join(profile.get('rendered_section_order', []))}"
                    )
                for heading, key in (
                    ("STEP 1 - AUDIT", "audit_raw"),
                    ("STEP 2 - REPAIR", "repair_raw"),
                    ("STEP 3 - FINAL SCAN", "final_scan_raw"),
                ):
                    value = artifacts.get(key)
                    if value:
                        summary = re.sub(
                            r"```json.*?```",
                            "",
                            str(value),
                            flags=re.DOTALL | re.IGNORECASE,
                        ).strip()
                        parts.append(f"{heading}\n{summary}")
                if error:
                    parts.append(f"ERROR\n{type(error).__name__}: {error}")
                save_text(self.request_file("final_qa_process", request_dir), "\n\n".join(parts))

            def progress(_step: int, message: str) -> None:
                self.app.after(0, lambda value=message: self.set_stage(value))

            def record_cost(event: CostEvent) -> None:
                self.app.after(0, lambda value=event: self.add_cost_events([value]))

            def save_artifact(kind: str, value) -> None:
                artifacts[kind] = value
                if kind == "final_json" and isinstance(value, dict):
                    save_json(self.request_file("final_qa_json", request_dir), value)
                save_process(f"Completed {kind.replace('_', ' ')}")

            try:
                result = asyncio.run(run_final_review(
                    jd=inp.jd,
                    source_resume_json=source_json,
                    cost_cb=record_cost,
                    request_label=self.request_label(inp),
                    cancel_event=self.cancel_event,
                    progress_cb=progress,
                    artifact_cb=save_artifact,
                    nvidia_model=nvidia_model,
                    nvidia_thinking=nvidia_thinking,
                ))
                return result
            except Exception as exc:
                save_process("Failed", exc)
                raise

        def done(result, err):
            if self.handle_cancelled(err):
                return
            self.set_busy(False, "Final QA JSON ready" if not err else "Final QA failed")
            if err:
                self.show_output(
                    "Final QA - Failed",
                    f"Final QA stopped before completion.\n\n{type(err).__name__}: {err}\n\n"
                    f"See {self.request_file('final_qa_process', request_dir).name} for completed steps.",
                )
                messagebox.showerror("Final QA failed", str(err), parent=self)
                return

            review_result = result
            final_path = self.request_file("final_qa_json", request_dir)
            display = self.format_final_review_display(review_result, source_path, final_path)
            save_text(self.request_file("final_qa_process", request_dir), display)
            self.show_output("Final QA", display)
            self.final_qa_json_path = final_path
            self.final_json_path = final_path
            self.docx_path = None
            self.select_output_artifact("Output | Final QA JSON")
            self.set_stage(f"Final QA JSON: {final_path.name}")

        run_bg(self.app, task, done)

    def on_answer_questions(self) -> None:
        try:
            inp = self.make_input()
            request_dir = self.ensure_request_dir(inp)
            questions = self.text_value(self.app_questions)
            if not questions:
                raise ValueError("Paste application questions first.")
            json_path = self.best_resume_json_path()
            if not json_path:
                raise ValueError(
                    "Generate JSON first. Final QA JSON is preferred, then recruiter JSON, then PASS 2 JSON."
                )
            resume_json = normalize_resume_json(json.loads(json_path.read_text(encoding="utf-8")))
            nvidia_model, nvidia_thinking = self.selected_nvidia_profile()
        except Exception as exc:
            messagebox.showerror("Application answers need input", str(exc), parent=self)
            return

        save_text(self.request_file("questions", request_dir), questions)
        self.set_busy(True, "Answering application questions...", cancellable=True)

        def task():
            events: list[CostEvent] = []
            answers = asyncio.run(run_application_answers(
                company=inp.company,
                title=inp.title,
                jd=inp.jd,
                questions=questions,
                resume_json=resume_json,
                cost_cb=events.append,
                request_label=self.request_label(inp),
                cancel_event=self.cancel_event,
                nvidia_model=nvidia_model,
                nvidia_thinking=nvidia_thinking,
            ))
            return answers, events, json_path

        def done(result, err):
            if self.handle_cancelled(err):
                return
            self.set_busy(False, "Application answers ready" if not err else "Questions failed")
            if err:
                messagebox.showerror("Application answers failed", str(err), parent=self)
                return
            answers, events, used_json_path = result
            clean_answers = self.clean_paste_text(answers)
            self.show_output("Application Answers", clean_answers)
            save_text(
                self.request_file("answers", request_dir),
                f"Source JSON: {used_json_path.name}\n\n{clean_answers}",
            )
            self.select_output_artifact("Output | Application Answers")
            self.add_cost_events(events)
            self.set_stage("Application answers ready")

        run_bg(self.app, task, done)

    def on_build_docx(self) -> None:
        if not self.final_json_path or not self.final_json_path.exists():
            path = filedialog.askopenfilename(
                title="Choose final resume JSON",
                filetypes=[("JSON", "*.json")],
                initialdir=str(self.request_dir or REQUESTS_DIR),
            )
            if not path:
                return
            self.final_json_path = Path(path)

        company = self.text_value(self.company) or "Company"
        self.set_busy(True, "Building DOCX...")

        def task():
            result = subprocess.run(
                [sys.executable, str(ROOT / "manager.py"), str(self.final_json_path), company],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode != 0:
                raise RuntimeError(result.stderr or result.stdout)
            docx_path = WORD_DIR / f"{RESUME_STEM}_{slug(company)}_Resume.docx"
            for line in result.stdout.splitlines():
                if line.startswith("DOCX saved"):
                    _, value = line.split(":", 1)
                    docx_path = ROOT / value.strip()
                    break
            return result.stdout, docx_path

        def done(result, err):
            self.set_busy(False, "DOCX ready" if not err else "DOCX failed")
            if err:
                messagebox.showerror("Build DOCX failed", str(err), parent=self)
                return
            stdout, path = result
            self.docx_path = path
            if self.request_dir:
                save_text(self.request_file("docx_log"), stdout)
            self.show_output("DOCX Build", stdout)
            open_path(path)

        run_bg(self.app, task, done)

    def on_pdf_archive(self) -> None:
        if not self.docx_path or not self.docx_path.exists():
            path = filedialog.askopenfilename(
                title="Choose reviewed DOCX",
                filetypes=[("Word document", "*.docx")],
                initialdir=str(WORD_DIR),
            )
            if not path:
                return
            self.docx_path = Path(path)

        company = self.text_value(self.company) or "Company"
        self.set_busy(True, "PDF archive running...")

        def task():
            result = subprocess.run(
                [sys.executable, str(ROOT / "manager.py"), str(self.docx_path), company],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode != 0:
                raise RuntimeError(result.stderr or result.stdout)
            return result.stdout

        def done(result, err):
            self.set_busy(False, "PDF archived" if not err else "PDF failed")
            if err:
                messagebox.showerror("PDF archive failed", str(err), parent=self)
                return
            if self.request_dir:
                save_text(self.request_file("pdf_log"), result)
            self.show_output("PDF + Archive", result)

        run_bg(self.app, task, done)

    def on_open_request(self) -> None:
        REQUESTS_DIR.mkdir(exist_ok=True)
        selected = filedialog.askdirectory(
            title="Open saved resume request",
            initialdir=str(self.request_dir.parent if self.request_dir else REQUESTS_DIR),
            mustexist=True,
        )
        if not selected:
            return
        try:
            self.load_request(Path(selected))
        except Exception as exc:
            messagebox.showerror("Open request failed", str(exc), parent=self)

    def on_open_folder(self) -> None:
        REQUESTS_DIR.mkdir(exist_ok=True)
        open_path(self.request_dir if self.request_dir and self.request_dir.exists() else REQUESTS_DIR)

    def load_request(self, request_dir: Path) -> None:
        metadata_path = self.existing_request_file("request", request_dir)
        jd_path = self.existing_request_file("jd", request_dir)
        if not metadata_path or not jd_path:
            raise ValueError("Choose a request folder containing request details and a job description.")

        metadata: dict[str, str] = {}
        for line in metadata_path.read_text(encoding="utf-8").splitlines():
            key, separator, value = line.partition(":")
            if separator:
                metadata[key.strip().lower()] = value.strip()

        def replace(box: tk.Text, value: str) -> None:
            box.delete("1.0", "end")
            box.insert("1.0", value)

        replace(self.company, metadata.get("company", ""))
        replace(self.title_text, metadata.get("title", "") or "Software Engineer")
        replace(self.words, metadata.get("words", ""))
        replace(self.des, metadata.get("des", ""))
        saved_profile = metadata.get("prompt profile", "stable")
        self.prompt_selector.set(prompt_profile_label(saved_profile))
        self.on_prompt_profile_selected()
        saved_model = metadata.get("nvidia model", "")
        saved_thinking = metadata.get("nvidia thinking", "ON").upper() != "OFF"
        if saved_model:
            try:
                self.model_selector.set(nvidia_model_option_label(saved_model, saved_thinking))
            except ValueError:
                self.model_selector.set(get_default_nvidia_model_option())
        self.show_job_description(jd_path.read_text(encoding="utf-8"))
        self.mode_value = ""

        approval_path = self.existing_request_file("approval", request_dir)
        approval = "Approved: "
        if approval_path:
            approval = approval_path.read_text(encoding="utf-8").split("\n\nNormalized:", 1)[0].strip()
        replace(self.approval, approval)

        questions_path = self.existing_request_file("questions", request_dir)
        replace(
            self.app_questions,
            questions_path.read_text(encoding="utf-8") if questions_path else "",
        )

        pass1_path = self.existing_request_file("des", request_dir)
        self.pass1_raw = pass1_path.read_text(encoding="utf-8") if pass1_path else ""
        self.request_dir = request_dir
        self.request_id = metadata.get("request id", request_dir.name) or request_dir.name
        pass2_path = self.existing_request_file("resume_json", request_dir)
        recruiter_path = self.existing_request_file("recruiter_json", request_dir)
        final_qa_path = self.existing_request_file("final_qa_json", request_dir)
        self.recruiter_json_path = recruiter_path
        self.final_qa_json_path = final_qa_path
        self.final_json_path = next(
            (path for path in (self.final_qa_json_path, self.recruiter_json_path, pass2_path) if path),
            None,
        )
        self.docx_path = None

        costs_path = request_dir / "costs.json"
        self.cost_events = []
        self.cost_usd = 0.0
        if costs_path.exists():
            costs = json.loads(costs_path.read_text(encoding="utf-8"))
            self.cost_usd = float(costs.get("tab_total_usd", 0) or 0)
        self.cost_label.config(text=f"${self.cost_usd:.4f}")

        if self.pass1_raw:
            self.show_des_in_jd(self.pass1_raw)

        self.refresh_output_choices()
        preferred_outputs = (
            "Output | Final QA JSON",
            "Output | Recruiter Resume JSON",
            "Output | Resume JSON",
            "Output | Application Answers",
            "LinkedIn | Combined Outreach",
            "Model Process | PASS 1 DES",
        )
        available = set(self.output_selector.cget("values"))
        selected_output = next((label for label in preferred_outputs if label in available), "")
        if selected_output:
            self.output_selector.set(selected_output)
            self.on_output_selected()
        else:
            self.show_output("Output", "Saved request loaded. Select any available next step.")

        source_name = self.final_json_path.name if self.final_json_path else "inputs only"
        self.set_stage(f"Loaded: {source_name}")

    def on_clear_tab(self) -> None:
        for box in (
            self.company,
            self.words,
            self.des,
            self.jd,
            self.approval,
            self.app_questions,
            self.output,
        ):
            box.delete("1.0", "end")
        self.title_text.delete("1.0", "end")
        self.title_text.insert("1.0", "Software Engineer")
        self.mode_value = ""
        self.approval.insert("1.0", "Approved: ")
        self.request_dir = None
        self.final_json_path = None
        self.recruiter_json_path = None
        self.final_qa_json_path = None
        self.docx_path = None
        self.cost_events = []
        self.cost_usd = 0.0
        self.request_id = self.name
        self.pass1_raw = ""
        self.job_description = ""
        self.jd_showing_des = False
        self.jd_title.set("Job Description")
        self.output_title.set("Output")
        self.output_selector.configure(values=())
        self.output_selector.set("")
        self.prompt_selector.set(prompt_profile_label("stable"))
        self.on_prompt_profile_selected()
        self.model_selector.set(get_default_nvidia_model_option())
        self.cost_label.config(text="$0.0000")
        self.set_stage("Ready")


class ResumeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resume Agent")
        self.geometry("1400x850")
        self.minsize(1260, 720)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        top = ttk.Frame(self, padding=(8, 8, 8, 4))
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(7, weight=1)

        ttk.Button(top, text="New Application Tab", command=self.add_tab).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(top, text="Duplicate Current", command=self.duplicate_current).grid(row=0, column=1, padx=(0, 6))
        ttk.Button(top, text="Close Current", command=self.close_current).grid(row=0, column=2, padx=(0, 6))
        ttk.Button(top, text="Clear DOCX/PDF", command=self.clear_docx_pdf).grid(row=0, column=3, padx=(0, 6))
        ttk.Button(top, text="Print Status", command=self.print_status).grid(row=0, column=4, padx=(0, 6))
        self.session_cost_usd = 0.0
        cfg = load_config()
        self.manual_balance_usd = float(cfg.get("manual_starting_balance_usd", 0) or 0)
        self.session_cost_label = ttk.Label(top, text="Session cost: $0.0000")
        self.session_cost_label.grid(row=0, column=5, padx=(8, 6), sticky="w")
        balance_text = "Balance: not connected" if self.manual_balance_usd <= 0 else f"Est. remaining: ${self.manual_balance_usd:.2f}"
        self.balance_label = ttk.Label(top, text=balance_text)
        self.balance_label.grid(row=0, column=6, padx=(8, 6), sticky="w")
        ttk.Label(top, text="Each tab can run independently. Start PASS 1 in multiple tabs for concurrent resumes.").grid(
            row=0, column=7, sticky="e"
        )

        status_frame = ttk.Frame(self, padding=(8, 0, 8, 6))
        status_frame.grid(row=1, column=0, sticky="ew")
        status_frame.columnconfigure(0, weight=1)
        self.status_tree = ttk.Treeview(
            status_frame,
            columns=("id", "company", "title", "stage", "cost"),
            show="headings",
            height=5,
        )
        for col, text, width in [
            ("id", "Request ID", 220),
            ("company", "Company", 150),
            ("title", "Title", 240),
            ("stage", "Stage", 260),
            ("cost", "Cost", 80),
        ]:
            self.status_tree.heading(col, text=text)
            self.status_tree.column(col, width=width, anchor="w", stretch=True)
        self.status_tree.grid(row=0, column=0, sticky="ew")
        self.status_tree.bind("<Double-1>", self.on_status_open)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.tab_counter = 0
        self.add_tab()

    def add_session_cost(self, amount: float) -> None:
        self.session_cost_usd += amount
        self.session_cost_label.config(text=f"Session cost: ${self.session_cost_usd:.4f}")
        if self.manual_balance_usd > 0:
            self.balance_label.config(text=f"Est. remaining: ${max(self.manual_balance_usd - self.session_cost_usd, 0):.2f}")

    def current_tab(self) -> JobTab | None:
        tab_id = self.notebook.select()
        if not tab_id:
            return None
        widget = self.nametowidget(tab_id)
        return widget if isinstance(widget, JobTab) else None

    def add_tab(self) -> None:
        self.tab_counter += 1
        tab = JobTab(self, f"Job {self.tab_counter}")
        self.notebook.add(tab, text=tab.name)
        self.notebook.select(tab)
        self.update_tab_status(tab)

    def rename_current_tab(self, name: str) -> None:
        tab_id = self.notebook.select()
        if tab_id:
            self.notebook.tab(tab_id, text=name[:28])

    def rename_tab(self, tab: JobTab, name: str) -> None:
        self.notebook.tab(tab, text=name[:36])

    def update_tab_status(self, tab: JobTab) -> None:
        iid = str(tab)
        values = (
            tab.request_id,
            tab.text_value(tab.company) or "",
            tab.text_value(tab.title_text) or "",
            tab.stage,
            f"${tab.cost_usd:.4f}",
        )
        if self.status_tree.exists(iid):
            self.status_tree.item(iid, values=values)
        else:
            self.status_tree.insert("", "end", iid=iid, values=values)

    def print_status(self) -> None:
        print("\n=== Resume Agent Status ===")
        for tab_id in self.notebook.tabs():
            tab = self.nametowidget(tab_id)
            if isinstance(tab, JobTab):
                self.update_tab_status(tab)
                print(
                    f"{tab.request_id} | company={tab.text_value(tab.company) or '-'} | "
                    f"title={tab.text_value(tab.title_text) or '-'} | stage={tab.stage} | cost=${tab.cost_usd:.4f}"
                )
        print("===========================\n")

    def on_status_open(self, _event=None) -> None:
        selected = self.status_tree.selection()
        if not selected:
            return
        iid = selected[0]
        try:
            tab = self.nametowidget(iid)
        except KeyError:
            return
        self.notebook.select(tab)

    def duplicate_current(self) -> None:
        current = self.current_tab()
        self.add_tab()
        new = self.current_tab()
        if not current or not new:
            return
        for source, target in [
            (current.company, new.company),
            (current.title_text, new.title_text),
            (current.words, new.words),
            (current.des, new.des),
            (current.app_questions, new.app_questions),
        ]:
            target.delete("1.0", "end")
            target.insert("1.0", source.get("1.0", "end").strip())
        source_jd = current.job_description if current.jd_showing_des else current.text_value(current.jd)
        new.show_job_description(source_jd)
        new.model_selector.set(current.model_selector.get())

    def close_current(self) -> None:
        tab_id = self.notebook.select()
        if tab_id and len(self.notebook.tabs()) > 1:
            if self.status_tree.exists(tab_id):
                self.status_tree.delete(tab_id)
            self.notebook.forget(tab_id)

    def clear_docx_pdf(self) -> None:
        if not messagebox.askyesno("Clear files", "Delete generated DOCX/PDF files from project output folders?", parent=self):
            return

        def task():
            result = subprocess.run(
                [sys.executable, str(ROOT / "manager.py"), "clear"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode != 0:
                raise RuntimeError(result.stderr or result.stdout)
            return result.stdout

        def done(result, err):
            if err:
                messagebox.showerror("Clear failed", str(err), parent=self)
            else:
                messagebox.showinfo("Clear complete", result, parent=self)

        run_bg(self, task, done)


if __name__ == "__main__":
    app = ResumeApp()
    app.mainloop()
