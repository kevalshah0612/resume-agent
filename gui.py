"""
Tabbed GUI for the compact DES-first resume flow.

Use:
  python gui.py
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from pipeline import (
    ResumeInput,
    extract_json,
    normalize_approval,
    run_pass1,
    run_pass2,
    run_recruiter_review,
    repair_repeated_verbs,
    save_json,
    save_text,
    slug,
    validate_resume_json,
)


ROOT = Path(__file__).parent
REQUESTS_DIR = ROOT / "requests"


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
            app.after(0, lambda: done(result, None))
        except Exception as exc:
            app.after(0, lambda: done(None, exc))

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

        self._build()

    def _build(self) -> None:
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        toolbar.columnconfigure(9, weight=1)

        self.pass1_btn = ttk.Button(toolbar, text="Run PASS 1", command=self.on_pass1)
        self.pass1_btn.grid(row=0, column=0, padx=(0, 6))
        self.json_btn = ttk.Button(toolbar, text="Generate JSON", command=self.on_generate_json)
        self.json_btn.grid(row=0, column=1, padx=(0, 6))
        self.recruiter_btn = ttk.Button(toolbar, text="Recruiter Review", command=self.on_recruiter_review)
        self.recruiter_btn.grid(row=0, column=2, padx=(0, 6))
        self.docx_btn = ttk.Button(toolbar, text="Build DOCX", command=self.on_build_docx)
        self.docx_btn.grid(row=0, column=3, padx=(0, 6))
        self.pdf_btn = ttk.Button(toolbar, text="PDF + Archive", command=self.on_pdf_archive)
        self.pdf_btn.grid(row=0, column=4, padx=(0, 6))
        ttk.Button(toolbar, text="Open Request", command=self.on_open_request).grid(row=0, column=5, padx=(0, 6))
        ttk.Button(toolbar, text="Clear Tab", command=self.on_clear_tab).grid(row=0, column=6, padx=(0, 6))
        self.status = ttk.Label(toolbar, text="Ready")
        self.status.grid(row=0, column=9, sticky="e")

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
        self.jd = tk.Text(left, wrap="word", undo=True)
        self.jd.grid(row=11, column=0, sticky="nsew")
        left.rowconfigure(11, weight=1)

        right = ttk.Frame(self)
        right.grid(row=1, column=1, sticky="nsew", padx=(6, 0))
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)
        right.rowconfigure(3, weight=1)

        ttk.Label(right, text="Compact PASS 1: DES Candidate Bank").grid(row=0, column=0, sticky="w")
        self.pass1 = tk.Text(right, wrap="word", undo=True)
        self.pass1.grid(row=1, column=0, sticky="nsew")

        ttk.Label(right, text="Approval: Approved: DES 1 to 6  |  1,2,3  |  Confirm").grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )
        self.approval = tk.Text(right, wrap="word", undo=True, height=5)
        self.approval.insert("1.0", "Approved: ")
        self.approval.grid(row=3, column=0, sticky="nsew")

    def _labeled_text(self, parent: ttk.Frame, label: str, row: int, height: int) -> tk.Text:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        box = tk.Text(parent, wrap="word", undo=True, height=height)
        box.grid(row=row + 1, column=0, sticky="ew", pady=(0, 4))
        return box

    def text_value(self, box: tk.Text) -> str:
        return box.get("1.0", "end").strip()

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

    def ensure_request_dir(self, inp: ResumeInput) -> Path:
        if self.request_dir:
            return self.request_dir
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.request_dir = REQUESTS_DIR / f"{slug(inp.company)}_{stamp}"
        self.request_dir.mkdir(parents=True, exist_ok=True)
        save_text(
            self.request_dir / "00_request.txt",
            "\n".join([
                f"Company: {inp.company}",
                f"Title: {inp.title}",
                f"Words: {inp.words}",
                f"Mode: {inp.mode}",
                f"DES: {inp.des}",
            ]),
        )
        save_text(self.request_dir / "01_jd.txt", inp.jd)
        self.app.rename_current_tab(f"{inp.company} *")
        return self.request_dir

    def set_busy(self, busy: bool, message: str) -> None:
        state = "disabled" if busy else "normal"
        for button in (self.pass1_btn, self.json_btn, self.recruiter_btn, self.docx_btn, self.pdf_btn):
            button.config(state=state)
        self.status.config(text=message)

    def on_pass1(self) -> None:
        try:
            inp = self.make_input()
            request_dir = self.ensure_request_dir(inp)
        except Exception as exc:
            messagebox.showerror("Input needed", str(exc), parent=self)
            return

        self.set_busy(True, "PASS 1 running...")

        def task():
            return asyncio.run(run_pass1(inp))

        def done(result, err):
            self.set_busy(False, "PASS 1 ready" if not err else "PASS 1 failed")
            if err:
                messagebox.showerror("PASS 1 failed", str(err), parent=self)
                return
            self.pass1.delete("1.0", "end")
            self.pass1.insert("1.0", result)
            save_text(request_dir / "02_pass1_des_bank.txt", result)

        run_bg(self.app, task, done)

    def on_generate_json(self) -> None:
        try:
            inp = self.make_input()
            request_dir = self.ensure_request_dir(inp)
            pass1_text = self.text_value(self.pass1)
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
            raw = asyncio.run(run_pass2(inp, pass1_text, approval))
            data = extract_json(raw)
            data = repair_repeated_verbs(data)
            errors = validate_resume_json(data)
            if errors:
                save_text(request_dir / "04_final_raw_failed.txt", raw)
                save_json(request_dir / "05_final_failed.json", data)
                raise RuntimeError("JSON failed local gates:\n- " + "\n- ".join(errors))
            return raw, data

        def done(result, err):
            self.set_busy(False, "JSON ready" if not err else "JSON failed")
            if err:
                messagebox.showerror("Generate JSON failed", str(err), parent=self)
                return
            raw, data = result
            save_text(request_dir / "04_final_raw.txt", raw)
            self.final_json_path = request_dir / "05_final_resume.json"
            save_json(self.final_json_path, data)
            self.status.config(text=f"JSON: {self.final_json_path.name}")

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
            raw = asyncio.run(run_recruiter_review(
                jd=inp.jd,
                resume1_json=resume_json,
                des=approval,
            ))
            data = extract_json(raw)
            data = repair_repeated_verbs(data)
            errors = validate_resume_json(data)
            if errors:
                save_text(request_dir / "06_recruiter_raw_failed.txt", raw)
                save_json(request_dir / "07_recruiter_failed.json", data)
                raise RuntimeError("Recruiter JSON failed local gates:\n- " + "\n- ".join(errors))
            return raw, data

        def done(result, err):
            self.set_busy(False, "Recruiter JSON ready" if not err else "Recruiter failed")
            if err:
                messagebox.showerror("Recruiter review failed", str(err), parent=self)
                return
            raw, data = result
            save_text(request_dir / "06_recruiter_raw.txt", raw)
            self.recruiter_json_path = request_dir / "07_recruiter_final_resume.json"
            save_json(self.recruiter_json_path, data)
            self.final_json_path = self.recruiter_json_path
            self.status.config(text=f"Recruiter JSON: {self.recruiter_json_path.name}")

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
            return result.stdout, ROOT / f"Keval_Shah_{slug(company)}_Resume.docx"

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
                initialdir=str(ROOT),
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
        for box in (self.company, self.words, self.des, self.jd, self.pass1, self.approval):
            box.delete("1.0", "end")
        self.title_text.delete("1.0", "end")
        self.title_text.insert("1.0", "Software Engineer")
        self.mode.delete("1.0", "end")
        self.approval.insert("1.0", "Approved: ")
        self.request_dir = None
        self.final_json_path = None
        self.recruiter_json_path = None
        self.docx_path = None
        self.status.config(text="Ready")


class ResumeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resume Agent")
        self.geometry("1220x820")
        self.minsize(1060, 720)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        top = ttk.Frame(self, padding=(8, 8, 8, 4))
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(4, weight=1)

        ttk.Button(top, text="New Application Tab", command=self.add_tab).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(top, text="Duplicate Current", command=self.duplicate_current).grid(row=0, column=1, padx=(0, 6))
        ttk.Button(top, text="Close Current", command=self.close_current).grid(row=0, column=2, padx=(0, 6))
        ttk.Button(top, text="Clear DOCX/PDF", command=self.clear_docx_pdf).grid(row=0, column=3, padx=(0, 6))
        ttk.Label(top, text="Each tab can run independently. Start PASS 1 in multiple tabs for concurrent resumes.").grid(
            row=0, column=4, sticky="e"
        )

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.tab_counter = 0
        self.add_tab()

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

    def rename_current_tab(self, name: str) -> None:
        tab_id = self.notebook.select()
        if tab_id:
            self.notebook.tab(tab_id, text=name[:28])

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
        ]:
            target.delete("1.0", "end")
            target.insert("1.0", source.get("1.0", "end").strip())

    def close_current(self) -> None:
        tab_id = self.notebook.select()
        if tab_id and len(self.notebook.tabs()) > 1:
            self.notebook.forget(tab_id)

    def clear_docx_pdf(self) -> None:
        if not messagebox.askyesno("Clear files", "Delete DOCX/PDF files in the project root?", parent=self):
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
