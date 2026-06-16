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

from pipeline import (
    CostEvent,
    ResumeInput,
    extract_json,
    load_config,
    normalize_approval,
    run_application_answers,
    run_pass1,
    run_pass2,
    run_recruiter_review,
    save_json,
    save_text,
    slug,
)


ROOT = Path(__file__).parent
REQUESTS_DIR = ROOT / "requests"
WORD_DIR = ROOT / "Resume-word"


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
        self.docx_path: Path | None = None
        self.cost_events: list[CostEvent] = []
        self.cost_usd = 0.0
        self.request_id = name
        self.stage = "Ready"
        self.pass1_raw = ""

        self._build()

    def _build(self) -> None:
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        toolbar.columnconfigure(10, weight=1)

        self.pass1_btn = ttk.Button(toolbar, text="Run PASS 1", command=self.on_pass1)
        self.pass1_btn.grid(row=0, column=0, padx=(0, 6))
        self.auto_btn = ttk.Button(toolbar, text="Auto JSON", command=self.on_auto_json)
        self.auto_btn.grid(row=0, column=1, padx=(0, 6))
        self.json_btn = ttk.Button(toolbar, text="Generate JSON", command=self.on_generate_json)
        self.json_btn.grid(row=0, column=2, padx=(0, 6))
        self.recruiter_btn = ttk.Button(toolbar, text="Recruiter Review", command=self.on_recruiter_review)
        self.recruiter_btn.grid(row=0, column=3, padx=(0, 6))
        self.docx_btn = ttk.Button(toolbar, text="Build DOCX", command=self.on_build_docx)
        self.docx_btn.grid(row=0, column=4, padx=(0, 6))
        self.pdf_btn = ttk.Button(toolbar, text="PDF + Archive", command=self.on_pdf_archive)
        self.pdf_btn.grid(row=0, column=5, padx=(0, 6))
        self.questions_btn = ttk.Button(toolbar, text="Answer Questions", command=self.on_answer_questions)
        self.questions_btn.grid(row=0, column=6, padx=(0, 6))
        ttk.Button(toolbar, text="Open Request", command=self.on_open_request).grid(row=0, column=7, padx=(0, 6))
        ttk.Button(toolbar, text="Clear Tab", command=self.on_clear_tab).grid(row=0, column=8, padx=(0, 6))
        self.cost_label = ttk.Label(toolbar, text="$0.0000")
        self.cost_label.grid(row=0, column=9, sticky="e", padx=(8, 8))
        self.status = ttk.Label(toolbar, text="Ready")
        self.status.grid(row=0, column=10, sticky="e")

        left = ttk.Frame(self)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 6))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(9, weight=1)

        self.company = self._labeled_text(left, "Company", 0, height=2)
        self.title_text = self._labeled_text(left, "Title", 2, height=2)
        self.title_text.insert("1.0", "Software Engineer")
        self.words = self._labeled_text(left, "Words / Keywords", 4, height=2)
        self.mode = self._labeled_text(left, "Mode", 6, height=2)
        self.des = self._labeled_text(left, "DES / Existing Evidence", 8, height=3)

        ttk.Label(left, text="Job Description").grid(row=10, column=0, sticky="w", pady=(8, 0))
        self.jd = tk.Text(left, wrap="word", undo=True, height=8)
        self.jd.grid(row=11, column=0, sticky="ew")

        right = ttk.Frame(self)
        right.grid(row=1, column=1, sticky="nsew", padx=(6, 0))
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=5)
        right.rowconfigure(7, weight=1)

        ttk.Label(right, text="Organized PASS 1: DES Candidate Bank").grid(row=0, column=0, sticky="w")
        self.pass1 = tk.Text(right, wrap="word", undo=True)
        self.pass1.grid(row=1, column=0, sticky="nsew")

        ttk.Label(right, text="Approval: Approved: DES 1 to 6  |  1,2,3  |  Confirm").grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )
        self.approval = tk.Text(right, wrap="word", undo=True, height=5)
        self.approval.insert("1.0", "Approved: ")
        self.approval.grid(row=3, column=0, sticky="nsew")

        ttk.Label(right, text="Application Questions").grid(row=4, column=0, sticky="w", pady=(8, 0))
        self.app_questions = tk.Text(right, wrap="word", undo=True, height=5)
        self.app_questions.grid(row=5, column=0, sticky="nsew")

        ttk.Label(right, text="Application Answers").grid(row=6, column=0, sticky="w", pady=(8, 0))
        self.app_answers = tk.Text(right, wrap="word", undo=True)
        self.app_answers.grid(row=7, column=0, sticky="nsew")

    def _labeled_text(self, parent: ttk.Frame, label: str, row: int, height: int) -> tk.Text:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        box = tk.Text(parent, wrap="word", undo=True, height=height)
        box.grid(row=row + 1, column=0, sticky="ew", pady=(0, 4))
        return box

    def text_value(self, box: tk.Text) -> str:
        return box.get("1.0", "end").strip()

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

    def make_input(self) -> ResumeInput:
        company = self.text_value(self.company)
        jd = self.text_value(self.jd)
        if not company:
            raise ValueError("Company is required.")
        if len(jd) < 50:
            raise ValueError("Paste the full JD first.")
        return ResumeInput(
            company=company,
            title=self.text_value(self.title_text) or "Software Engineer",
            jd=jd,
            words=self.text_value(self.words),
            mode=self.text_value(self.mode),
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
        save_text(
            self.request_dir / "00_request.txt",
            "\n".join([
                f"Request ID: {self.request_id}",
                f"Company: {inp.company}",
                f"Title: {inp.title}",
                f"Words: {inp.words}",
                f"Mode: {inp.mode}",
                f"DES: {inp.des}",
            ]),
        )
        save_text(self.request_dir / "01_jd.txt", inp.jd)
        self.app.rename_tab(self, self.tab_caption())
        self.app.update_tab_status(self)
        return self.request_dir

    def set_busy(self, busy: bool, message: str) -> None:
        state = "disabled" if busy else "normal"
        for button in (
            self.pass1_btn,
            self.auto_btn,
            self.json_btn,
            self.recruiter_btn,
            self.docx_btn,
            self.pdf_btn,
            self.questions_btn,
        ):
            button.config(state=state)
        self.set_stage(message)

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
                        }
                        for e in self.cost_events
                    ],
                },
            )

    def on_pass1(self) -> None:
        try:
            inp = self.make_input()
            request_dir = self.ensure_request_dir(inp)
        except Exception as exc:
            messagebox.showerror("Input needed", str(exc), parent=self)
            return

        self.set_busy(True, "PASS 1 running...")

        def task():
            events: list[CostEvent] = []
            result = asyncio.run(run_pass1(inp, cost_cb=events.append, request_label=self.request_label(inp)))
            return result, events

        def done(result, err):
            self.set_busy(False, "PASS 1 ready" if not err else "PASS 1 failed")
            if err:
                messagebox.showerror("PASS 1 failed", str(err), parent=self)
                return
            result, events = result
            self.pass1_raw = result
            self.pass1.delete("1.0", "end")
            self.pass1.insert("1.0", self.format_pass1_display(result))
            save_text(request_dir / "02_pass1_des_bank.txt", result)
            self.add_cost_events(events)

        run_bg(self.app, task, done)

    def on_generate_json(self) -> None:
        try:
            inp = self.make_input()
            request_dir = self.ensure_request_dir(inp)
            pass1_text = self.pass1_raw or self.text_value(self.pass1)
            if not pass1_text:
                raise ValueError("Run PASS 1 first.")
            approval_raw = self.text_value(self.approval)
            approval = normalize_approval(approval_raw)
        except Exception as exc:
            messagebox.showerror("Missing step", str(exc), parent=self)
            return

        save_text(request_dir / "03_approval.txt", approval_raw + "\n\nNormalized:\n" + approval)
        self.set_busy(True, "Generating JSON...")

        def task():
            events: list[CostEvent] = []
            raw = asyncio.run(run_pass2(
                inp,
                pass1_text,
                approval,
                cost_cb=events.append,
                request_label=self.request_label(inp),
            ))
            data = extract_json(raw)
            return raw, data, events

        def done(result, err):
            self.set_busy(False, "JSON ready" if not err else "JSON failed")
            if err:
                messagebox.showerror("Generate JSON failed", str(err), parent=self)
                return
            raw, data, events = result
            save_text(request_dir / "04_final_raw.txt", raw)
            self.final_json_path = request_dir / "05_final_resume.json"
            save_json(self.final_json_path, data)
            self.add_cost_events(events)
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
        except Exception as exc:
            messagebox.showerror("Input needed", str(exc), parent=self)
            return

        self.set_busy(True, "AUTO running PASS 1...")

        def task():
            events: list[CostEvent] = []
            pass1_raw = asyncio.run(run_pass1(inp, cost_cb=events.append, request_label=self.request_label(inp)))
            approval_raw = self.approve_all_des_text(pass1_raw)
            approval = normalize_approval(approval_raw)
            pass2_raw = asyncio.run(run_pass2(
                inp,
                pass1_raw,
                approval,
                cost_cb=events.append,
                request_label=self.request_label(inp),
            ))
            data = extract_json(pass2_raw)
            return pass1_raw, approval_raw, approval, pass2_raw, data, events

        def done(result, err):
            self.set_busy(False, "AUTO JSON ready" if not err else "AUTO failed")
            if err:
                messagebox.showerror("Auto JSON failed", str(err), parent=self)
                return
            pass1_raw, approval_raw, approval, pass2_raw, data, events = result
            self.pass1_raw = pass1_raw
            self.pass1.delete("1.0", "end")
            self.pass1.insert("1.0", self.format_pass1_display(pass1_raw))
            self.approval.delete("1.0", "end")
            self.approval.insert("1.0", approval_raw)
            save_text(request_dir / "02_pass1_des_bank.txt", pass1_raw)
            save_text(request_dir / "03_approval.txt", approval_raw + "\n\nNormalized:\n" + approval)
            save_text(request_dir / "04_final_raw.txt", pass2_raw)
            self.final_json_path = request_dir / "05_final_resume.json"
            save_json(self.final_json_path, data)
            self.add_cost_events(events)
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
            resume_json = json.loads(self.final_json_path.read_text(encoding="utf-8"))
            approval = self.text_value(self.approval)
        except Exception as exc:
            messagebox.showerror("Recruiter review needs input", str(exc), parent=self)
            return

        self.set_busy(True, "Recruiter review running...")

        def task():
            events: list[CostEvent] = []
            raw = asyncio.run(run_recruiter_review(
                jd=inp.jd,
                resume1_json=resume_json,
                des=approval,
                cost_cb=events.append,
                request_label=self.request_label(inp),
            ))
            data = extract_json(raw)
            return raw, data, events

        def done(result, err):
            self.set_busy(False, "Recruiter JSON ready" if not err else "Recruiter failed")
            if err:
                messagebox.showerror("Recruiter review failed", str(err), parent=self)
                return
            raw, data, events = result
            save_text(request_dir / "06_recruiter_raw.txt", raw)
            self.recruiter_json_path = request_dir / "07_recruiter_final_resume.json"
            save_json(self.recruiter_json_path, data)
            self.final_json_path = self.recruiter_json_path
            self.add_cost_events(events)
            self.set_stage(f"Recruiter JSON: {self.recruiter_json_path.name}")

        run_bg(self.app, task, done)

    def best_resume_json_path(self) -> Path | None:
        if self.recruiter_json_path and self.recruiter_json_path.exists():
            return self.recruiter_json_path
        if self.final_json_path and self.final_json_path.exists():
            return self.final_json_path
        return None

    def on_answer_questions(self) -> None:
        try:
            inp = self.make_input()
            request_dir = self.ensure_request_dir(inp)
            questions = self.text_value(self.app_questions)
            if not questions:
                raise ValueError("Paste application questions first.")
            json_path = self.best_resume_json_path()
            if not json_path:
                raise ValueError("Generate JSON first. Recruiter JSON is used when available; otherwise final PASS 2 JSON is used.")
            resume_json = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as exc:
            messagebox.showerror("Application answers need input", str(exc), parent=self)
            return

        save_text(request_dir / "08_application_questions.txt", questions)
        self.set_busy(True, "Answering application questions...")

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
            ))
            return answers, events, json_path

        def done(result, err):
            self.set_busy(False, "Application answers ready" if not err else "Questions failed")
            if err:
                messagebox.showerror("Application answers failed", str(err), parent=self)
                return
            answers, events, used_json_path = result
            self.app_answers.delete("1.0", "end")
            self.app_answers.insert("1.0", answers)
            save_text(
                request_dir / "09_application_answers.txt",
                f"Source JSON: {used_json_path.name}\n\n{answers}",
            )
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
            docx_path = WORD_DIR / f"Keval_Shah_{slug(company)}_Resume.docx"
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
                save_text(self.request_dir / "06_docx_build.txt", stdout)
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
                save_text(self.request_dir / "07_pdf_archive.txt", result)
            messagebox.showinfo("PDF archived", result, parent=self)

        run_bg(self.app, task, done)

    def on_open_request(self) -> None:
        if self.request_dir and self.request_dir.exists():
            open_path(self.request_dir)
        else:
            REQUESTS_DIR.mkdir(exist_ok=True)
            open_path(REQUESTS_DIR)

    def on_clear_tab(self) -> None:
        for box in (
            self.company,
            self.words,
            self.des,
            self.jd,
            self.pass1,
            self.approval,
            self.app_questions,
            self.app_answers,
        ):
            box.delete("1.0", "end")
        self.title_text.delete("1.0", "end")
        self.title_text.insert("1.0", "Software Engineer")
        self.mode.delete("1.0", "end")
        self.approval.insert("1.0", "Approved: ")
        self.request_dir = None
        self.final_json_path = None
        self.recruiter_json_path = None
        self.docx_path = None
        self.cost_events = []
        self.cost_usd = 0.0
        self.request_id = self.name
        self.pass1_raw = ""
        self.cost_label.config(text="$0.0000")
        self.set_stage("Ready")


class ResumeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resume Agent")
        self.geometry("1220x820")
        self.minsize(1060, 720)

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
            (current.mode, new.mode),
            (current.des, new.des),
            (current.jd, new.jd),
            (current.app_questions, new.app_questions),
        ]:
            target.delete("1.0", "end")
            target.insert("1.0", source.get("1.0", "end").strip())

    def close_current(self) -> None:
        tab_id = self.notebook.select()
        if tab_id and len(self.notebook.tabs()) > 1:
            if self.status_tree.exists(tab_id):
                self.status_tree.delete(tab_id)
            self.notebook.forget(tab_id)

    def clear_docx_pdf(self) -> None:
        if not messagebox.askyesno("Clear files", "Delete DOCX/PDF files in project root, Resume-word, and Resume-pdf?", parent=self):
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
