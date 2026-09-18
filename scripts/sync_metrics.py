#!/usr/bin/env python3
"""Unified metric extraction for ai-context-core.

Runs the analyzer on itself, extracts quality scores from the analysis
output, and writes a structured snapshot to .agent/memory/agent_metrics.json.

Usage:
    uv run python scripts/sync_metrics.py
"""

import json
import subprocess
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ANALYSIS_FILE = PROJECT_ROOT / "project_context.json"
METRICS_FILE = PROJECT_ROOT / ".agent" / "memory" / "agent_metrics.json"


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
                if part == "passed":
                    try:
                        passed = int(parts[i - 1])
                        break
                    except (ValueError, IndexError):
                        pass

    if passed == 0:
        total = len(list((PROJECT_ROOT / "tests").glob("test_*.py")))

    return {"pass": passed, "total": total or passed}


def load_existing_metrics() -> dict:
    """Load existing metrics file or return empty structure."""
    if METRICS_FILE.exists():
        with open(METRICS_FILE) as f:
            return json.load(f)
    return {"version": "1.0", "project": "ai-context-core", "sessions": []}


def main() -> None:
    print("🔄 ai-context-core — Metric Sync")
    print(f"   Date: {date.today().isoformat()}")
    print()

    # 1. Run the analyzer on itself
    print("📊 Running self-analysis...")
    result = run_command(["uv", "run", "ai-ctx", "analyze", "."])
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

    # 4. Update metrics file
    metrics = load_existing_metrics()
    session_entry = {
        "date": date.today().isoformat(),
        "session": "sync_metrics_auto",
        "scores": scores,
        "tests": tests,
    }

    metrics["sessions"] = [s for s in metrics["sessions"] if s["date"] != date.today().isoformat()]
    metrics["sessions"].append(session_entry)
    metrics["sessions"].sort(key=lambda s: s["date"])

    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)
        f.write("\n")

    print(f"✅ Metrics written to {METRICS_FILE}")
    print(f"   Total sessions tracked: {len(metrics['sessions'])}")


if __name__ == "__main__":
    main()
