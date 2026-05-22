#!/usr/bin/env python3
"""BG Hunt 8-agent orchestrator — tooling, hunters BG-01..06, aggregator BG-07."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

STEPS = [
    ("BG-00", [sys.executable, str(HERE / "_bg_hunt_00_build.py")]),
    ("BG-01", [sys.executable, str(HERE / "_bg_hunt_runner.py"), "BG-01"]),
    ("BG-02", [sys.executable, str(HERE / "_bg_hunt_runner.py"), "BG-02"]),
    ("BG-03", [sys.executable, str(HERE / "_bg_hunt_runner.py"), "BG-03"]),
    ("BG-04", [sys.executable, str(HERE / "_bg_hunt_runner.py"), "BG-04"]),
    ("BG-05", [sys.executable, str(HERE / "_bg_hunt_runner.py"), "BG-05"]),
    ("BG-06", [sys.executable, str(HERE / "_bg_hunt_runner.py"), "BG-06"]),
    ("BG-07", [sys.executable, str(HERE / "_bg_hunt_07_aggregate.py")]),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    results: dict[str, dict] = {}
    for agent, cmd in STEPS:
        print(f"\n=== Running {agent} ===", flush=True)
        proc = subprocess.run(cmd, cwd=str(HERE), capture_output=True, text=True)
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        if proc.returncode != 0:
            print(f"FAILED {agent} exit={proc.returncode}", file=sys.stderr)
            sys.exit(proc.returncode)
        try:
            results[agent] = json.loads(proc.stdout.strip().split("\n")[-1]) if proc.stdout.strip().startswith("{") else {"stdout_tail": proc.stdout[-500:]}
        except json.JSONDecodeError:
            # multi-line json at end
            for line in reversed(proc.stdout.strip().split("\n")):
                try:
                    results[agent] = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue
            else:
                results[agent] = {"ok": True}

    summary_path = HERE / "reports" / "bg_hunt_orchestrator_summary.json"
    summary_path.write_text(json.dumps({"generated_at": utc_now(), "results": results}, indent=2), encoding="utf-8")
    print(json.dumps({"status": "complete", "results": results}, indent=2))


if __name__ == "__main__":
    main()
