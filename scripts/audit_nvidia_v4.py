from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pipeline


def request_field(details: str, name: str, default: str = "") -> str:
    prefix = f"{name}:"
    for line in details.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return default


def fixture_from_directory(path: Path) -> dict[str, str]:
    details = (path / "00_request_details.txt").read_text(encoding="utf-8")
    jd = (path / "01_job_description.txt").read_text(encoding="utf-8").strip()
    return {
        "source_directory": str(path.resolve()),
        "company": request_field(details, "Company", path.name.split("_", 1)[0]),
        "title": request_field(details, "Title", "Software Engineer"),
        "jd": jd,
    }


async def run_fixture(fixture: dict[str, str], step: int) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {}
    print(f"Step {step}/3 | {fixture['company']} | Running NVIDIA JD parse")
    raw = await pipeline.run_pass1(
        pipeline.ResumeInput(
            company=fixture["company"],
            title=fixture["title"],
            jd=fixture["jd"],
        ),
        request_label=f"AUDIT {fixture['company']}",
        prompt_profile="v4",
        diagnostics=diagnostics,
    )
    schema_error = pipeline.validate_v4_jd_response(raw)
    result = {
        **fixture,
        "final_json": pipeline.extract_json(raw),
        "raw_response": raw,
        "diagnostics": diagnostics,
        "response_time_seconds": diagnostics["total_response_time_seconds"],
        "api_call_count": diagnostics["api_calls"],
        "retry_count": diagnostics["retries"],
        "schema_validation_result": "PASS" if schema_error is None else f"FAIL: {schema_error}",
    }
    print(
        f"Step {step}/3 | {fixture['company']} | {result['schema_validation_result']} | "
        f"calls={result['api_call_count']} retries={result['retry_count']} "
        f"time={result['response_time_seconds']:.3f}s"
    )
    return result


async def main() -> int:
    parser = argparse.ArgumentParser(description="Run a sanitized NVIDIA V4 JD-parser audit.")
    parser.add_argument("request_directories", nargs=3, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    fixtures = [fixture_from_directory(path) for path in args.request_directories]
    runs = []
    for index, fixture in enumerate(fixtures, start=1):
        runs.append(await run_fixture(fixture, index))

    output = args.output or (
        pipeline.ROOT
        / "requests"
        / f"V4_NVIDIA_JD_PARSER_AUDIT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    payload = {
        "created_at": datetime.now().astimezone().isoformat(),
        "effective_configuration": {
            "provider": pipeline.get_provider(),
            "model": pipeline.get_nvidia_model(),
            "thinking": pipeline.get_nvidia_thinking(),
            "medium_effort": pipeline.get_nvidia_medium_effort(),
            "temperature": pipeline.get_nvidia_temperature(),
            "top_p": pipeline.get_nvidia_top_p(),
            "seed": pipeline.get_nvidia_seed(),
            "stream": pipeline.get_nvidia_stream(),
            "max_tokens": pipeline.get_response_max_tokens(),
            "reasoning_budget": pipeline.get_nvidia_reasoning_budget(),
            "guided_json": pipeline.get_nvidia_guided_json(),
            "validation_pass": pipeline.get_nvidia_validation_pass(),
            "fallback_to_anthropic": pipeline.config_bool(
                pipeline.load_config().get("fallback_to_anthropic"), False
            ),
        },
        "sanitized_final_nvidia_request_payload": runs[-1]["diagnostics"].get(
            "sanitized_request_payload"
        ),
        "runs": runs,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Complete | Sanitized audit artifact: {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
