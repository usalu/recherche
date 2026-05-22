#!/usr/bin/env python3
"""BG-W2 orchestrator — build scopes, run 3 hunters + aggregator."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent

STEPS = [
    ("BG-W2-00", [sys.executable, str(HERE / "_bg_hunt_w2_build.py")]),
    ("BG-W2-01", [sys.executable, str(HERE / "_bg_hunt_w2_runner.py"), "BG-W2-01"]),
    ("BG-W2-02", [sys.executable, str(HERE / "_bg_hunt_w2_runner.py"), "BG-W2-02"]),
    ("BG-W2-03", [sys.executable, str(HERE / "_bg_hunt_w2_runner.py"), "BG-W2-03"]),
    ("BG-W2-04", [sys.executable, str(HERE / "_bg_hunt_w2_aggregate.py")]),
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
        for line in reversed(proc.stdout.strip().split("\n")):
            try:
                results[agent] = json.loads(line)
                break
            except json.JSONDecodeError:
                continue
        else:
            results[agent] = {"ok": True}

    summary_path = HERE / "reports" / "bg_hunt_w2_orchestrator_summary.json"
    summary_path.write_text(json.dumps({"generated_at": utc_now(), "results": results}, indent=2), encoding="utf-8")
    print(json.dumps({"status": "complete", "results": results}, indent=2))


if __name__ == "__main__":
    main()
