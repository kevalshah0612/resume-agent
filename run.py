"""
Interactive runner for the new resume flow.

Flow 1:
  Company/JD input -> PASS 1 -> DES approval / CONFIRM -> final resume JSON

Flow 2:
  Optional recruiter review -> final JSON -> DOCX
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

from pipeline import (
    RUNS_DIR,
    ResumeInput,
    build_docx,
    extract_json,
    load_config,
    meaningful_stem,
    run_pass1,
    run_pass2,
    run_recruiter_review,
    save_json,
    save_text,
    slug,
    timestamp,
    validate_resume_json,
    write_run_artifacts,
)


ROOT = Path(__file__).parent


def hr(char: str = "-", width: int = 72) -> None:
    print(char * width)


def ask(prompt: str, default: str = "") -> str:
    value = input(prompt).strip()
    return value if value else default


def paste_block(label: str, terminator: str = "===") -> str:
    print(f"Paste {label}. Type {terminator} on its own line when done:")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == terminator:
            break
        lines.append(line)
    return "\n".join(lines).strip()


def open_file(path: Path) -> None:
    try:
        if sys.platform == "win32":
            os.startfile(str(path))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        else:
            subprocess.run(["xdg-open", str(path)], check=False)
    except Exception as exc:
        print(f"Could not auto-open {path}: {exc}")


def load_optional_json(path_text: str) -> dict | None:
    if not path_text.strip():
        return None
    path = Path(path_text.strip()).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        print(f"Resume 2 not found: {path}")
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def setup_api_key() -> None:
    cfg = load_config()
    if not os.environ.get("ANTHROPIC_API_KEY") and cfg.get("anthropic_api_key"):
        os.environ["ANTHROPIC_API_KEY"] = cfg["anthropic_api_key"]


async def run_one_job() -> None:
    hr("=")
    print("NEW RESUME FLOW")
    hr("=")

    company = ask("Company: ")
    if company.upper() == "Q":
        raise KeyboardInterrupt
    if not company:
        print("Skipped: company is required.")
        return

    title = ask("Title [Software Engineer]: ", "Software Engineer")
    print()
    jd = paste_block("JD")
    if len(jd) < 50:
        print("Skipped: JD is too short.")
        return

    words = ask("Words [optional]: ")
    mode = ask("Mode [optional, e.g. mid + backend]: ")
    des = ask("DES [optional]: ")

    stem = meaningful_stem(company, title)
    run_dir = RUNS_DIR / f"{slug(company)}_{timestamp()}"
    run_dir.mkdir(parents=True, exist_ok=True)

    inp = ResumeInput(
        company=company,
        title=title,
        jd=jd,
        words=words,
        mode=mode,
        des=des,
    )

    save_text(run_dir / "00_input.txt", "\n".join([
        f"Company: {company}",
        f"Title: {title}",
        f"Words: {words}",
        f"Mode: {mode}",
        f"DES: {des}",
        "",
        "JD:",
        jd,
    ]))

    print()
    hr()
    print("Running PASS 1. The static prompt/story files are cached by Anthropic.")
    hr()
    pass1 = await run_pass1(inp)
    write_run_artifacts(run_dir=run_dir, pass1_text=pass1)

    print()
    print(pass1)
    print()
    hr()
    print("Reply with CONFIRM, or approve DES IDs like: Apply DES-1, DES-3 CONFIRM")
    hr()

    approval = paste_block("approval / DES response")
    if "CONFIRM" not in approval.upper():
        print("Stopped before final JSON. PASS 1 was saved for later.")
        print(f"Run folder: {run_dir}")
        return

    print()
    hr()
    print("Running PASS 2 final JSON.")
    hr()
    pass2 = await run_pass2(inp, pass1, approval)
    resume_json = extract_json(pass2)
    errors = validate_resume_json(resume_json)
    if errors:
        write_run_artifacts(run_dir=run_dir, pass2_text=pass2, resume_json=resume_json)
        raise RuntimeError("PASS 2 JSON failed local quality gates:\n- " + "\n- ".join(errors))
    resume_json_path = run_dir / "03_resume_json.json"
    write_run_artifacts(
        run_dir=run_dir,
        pass2_text=pass2,
        resume_json=resume_json,
    )
    save_json(ROOT / f"{stem}_resume.json", resume_json)

    print()
    print(pass2)
    print()

    final_json = resume_json
    final_json_path = resume_json_path

    review = ask("Run recruiter review? [Y/n]: ", "Y").lower()
    if review != "n":
        resume2_path = ask("Optional Resume 2 JSON path [Enter to skip]: ")
        resume2_json = load_optional_json(resume2_path)
        recruiter_des = approval if approval.strip() != "CONFIRM" else des

        print()
        hr()
        print("Running recruiter review.")
        hr()
        recruiter_text = await run_recruiter_review(
            jd=jd,
            des=recruiter_des,
            resume1_json=resume_json,
            resume2_json=resume2_json,
        )
        recruiter_json = extract_json(recruiter_text)
        errors = validate_resume_json(recruiter_json)
        if errors:
            write_run_artifacts(
                run_dir=run_dir,
                recruiter_text=recruiter_text,
                recruiter_json=recruiter_json,
            )
            raise RuntimeError("Recruiter JSON failed local quality gates:\n- " + "\n- ".join(errors))
        write_run_artifacts(
            run_dir=run_dir,
            recruiter_text=recruiter_text,
            recruiter_json=recruiter_json,
        )
        final_json = recruiter_json
        final_json_path = run_dir / "05_recruiter_final_json.json"
        save_json(ROOT / f"{stem}_final.json", final_json)

        print()
        print(recruiter_text)
        print()

    out_docx = f"{stem}.docx"
    docx = build_docx(final_json_path, out_docx)
    print()
    print(f"DOCX saved: {docx}")
    print(f"Run folder: {run_dir}")
    open_file(docx)


async def main() -> None:
    setup_api_key()
    print()
    hr("=")
    print("Resume Agent - New Flow")
    print("Type Q at the company prompt by pressing Ctrl+C to quit anytime.")
    hr("=")

    while True:
        try:
            await run_one_job()
            again = ask("\nCreate another resume? [y/N]: ", "N").lower()
            if again != "y":
                break
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as exc:
            print(f"\nERROR: {exc}")
            again = ask("Try another job? [y/N]: ", "N").lower()
            if again != "y":
                break


if __name__ == "__main__":
    asyncio.run(main())
