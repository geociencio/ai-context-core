#!/usr/bin/env python3
"""Unified metric extraction for ai-context-core.

Runs the analyzer on itself, extracts quality scores from the analysis
output, and writes a structured snapshot to .agent-state/memory/agent_metrics.json
using the schema expected by the framework metrics engine (``forge metrics``):
a ``summary`` object plus ``last_session``/``history`` for trend reporting.

Usage:
    uv run python scripts/sync_metrics.py
"""

import json
import subprocess
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ANALYSIS_FILE = PROJECT_ROOT / "project_context.json"
METRICS_FILE = PROJECT_ROOT / ".agent-state" / "memory" / "agent_metrics.json"


def run_command(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    return subprocess.run(cmd, cwd=cwd or PROJECT_ROOT, capture_output=True, text=True)


def extract_scores() -> dict:
    """Extract quality metrics from the analyzer output."""
    if not ANALYSIS_FILE.exists():
        print(f"⚠ Analysis results not found at {ANALYSIS_FILE}")
        print("  Run: uv run ai-ctx analyze .")
        return {}

    with open(ANALYSIS_FILE) as f:
        data = json.load(f)

    metrics = data.get("metrics", {})
    return {
        "quality_score": round(metrics.get("quality_score", 0), 1),
        "maintainability": round(metrics.get("avg_maintenance_index", 0), 1),
        "avg_complexity": round(metrics.get("average_complexity", 0), 2),
        "max_complexity": round(metrics.get("max_complexity", 0), 2),
    }


def count_tests() -> dict:
    """Count passing tests via pytest."""
    result = run_command(["uv", "run", "pytest", "-q", "--tb=no"])
    output = result.stdout + result.stderr
    passed = 0
    total = 0
    for line in output.splitlines():
        if "passed" in line:
            parts = line.split()
            for i, part in enumerate(parts):
                if "passed" in part:
                    try:
                        passed = int(parts[i - 1])
                        break
                    except (ValueError, IndexError):
                        pass

    if passed == 0:
        total = len(list((PROJECT_ROOT / "tests").glob("test_*.py")))

    return {"pass": passed, "total": total or passed}


def load_existing_metrics() -> dict:
    """Load existing metrics file or return an empty structure."""
    if METRICS_FILE.exists():
        with open(METRICS_FILE) as f:
            return json.load(f)
    return {"version": "1.0", "project": "ai-context-core"}


def _migrate_history(existing: dict) -> list[dict]:
    """Build a history list from legacy ``sessions`` plus any prior ``history``."""
    history = [h for h in existing.get("history", []) if isinstance(h, dict)]

    for s in existing.get("sessions", []):
        history.append(
            {
                "date": s.get("date"),
                "session": s.get("session", "sync_metrics_auto"),
                "quality_score": s.get("scores", {}).get("quality_score"),
                "tests_ok": s.get("tests", {}).get("pass"),
            }
        )

    seen = set()
    deduped = []
    for entry in history:
        key = (entry.get("date"), entry.get("session") or entry.get("topic") or "")
        if key in seen:
            continue
        seen.add(key)
        deduped.append(entry)
    return deduped


def main() -> None:
    print("🔄 ai-context-core — Metric Sync")
    print(f"   Date: {date.today().isoformat()}")
    print()

    # 1. Run the analyzer on itself
    print("📊 Running self-analysis...")
    result = run_command(["uv", "run", "ai-ctx", "analyze", "--path", "."])
    if result.returncode != 0:
        print(f"⚠ Analysis completed with warnings (exit code {result.returncode})")
    else:
        print("   Analysis complete.")

    # 2. Extract scores
    scores = extract_scores()
    if scores:
        print(f"   Quality Score: {scores['quality_score']}/100")
        print(f"   Maintainability: {scores['maintainability']}/100")
        print(f"   Avg Complexity: {scores['avg_complexity']}")
    else:
        print("   ⚠ Could not extract scores. Skipping score snapshot.")

    # 3. Count tests
    tests = count_tests()
    print(f"   Tests: {tests['pass']}/{tests['total']} passing")
    print()

    # 4. Update metrics file with the framework-compatible schema
    existing = load_existing_metrics()
    history = _migrate_history(existing)
    today = date.today().isoformat()
    history = [h for h in history if h.get("date") != today]

    metrics = {
        "version": "1.0",
        "project": "ai-context-core",
        "summary": {
            "test_count": tests["pass"],
            "tests_ok": tests["pass"],
            "quality_score_latest": scores.get("quality_score"),
            "maintainability_score": scores.get("maintainability"),
            "avg_complexity": scores.get("avg_complexity"),
            "max_complexity": scores.get("max_complexity"),
        },
        "last_session": {
            "date": today,
            "topic": "sync_metrics_auto",
            "tests_ok": tests["pass"],
            "quality_score": scores.get("quality_score"),
            "status": "SUCCESS",
        },
        "history": history,
    }

    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)
        f.write("\n")

    print(f"✅ Metrics written to {METRICS_FILE}")
    print(f"   Total history entries: {len(history)}")


if __name__ == "__main__":
    main()
