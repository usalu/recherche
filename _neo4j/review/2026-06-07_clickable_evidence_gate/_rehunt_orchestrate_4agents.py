"""Orchestrate CEG 4-agent re-hunt, merge results, dry-run consolidated patch."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
AGENTS = ["CEG-R1", "CEG-R2", "CEG-R3", "CEG-R4"]
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_agent(agent: str) -> int:
    cmd = [sys.executable, str(HERE / "_rehunt_agent.py"), "--agent", agent]
    print(f"launch {agent}...")
    return subprocess.call(cmd, cwd=str(REPO))


def merge_caches() -> None:
    import verify_clickable_evidence as ceg

    merged: dict = {}
    if ceg.CACHE_PATH.is_file():
        merged.update(json.loads(ceg.CACHE_PATH.read_text(encoding="utf-8")))
    for agent in AGENTS:
        p = HERE / f"_fetch_cache_{agent}.json"
        if p.is_file():
            merged.update(json.loads(p.read_text(encoding="utf-8")))
    ceg.CACHE_PATH.write_text(json.dumps(merged, ensure_ascii=False), encoding="utf-8")
    print(f"merged fetch cache: {len(merged)} urls")


def main() -> None:
    running = {
        agent: subprocess.Popen(
            [sys.executable, str(HERE / "_rehunt_agent.py"), "--agent", agent],
            cwd=str(REPO),
        )
        for agent in AGENTS
    }
    print("launched:", ", ".join(AGENTS))
    procs = []
    for agent, proc in running.items():
        procs.append((agent, proc.wait()))

    failed = [a for a, rc in procs if rc != 0]
    if failed:
        print("agents failed:", failed)

    merge_caches()

    all_rows: list[dict] = []
    all_ops: list[dict] = []
    for agent in AGENTS:
        ledger = HERE / "ledger" / f"rehunt_{agent}.csv"
        patch = HERE / "patches" / f"rehunt_{agent}.patch.jsonl"
        if ledger.is_file():
            all_rows.extend(list(csv.DictReader(ledger.open(encoding="utf-8"))))
        if patch.is_file():
            for line in patch.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    all_ops.append(json.loads(line))

    merged_ledger = HERE / "REHUNT_LEDGER_v2.csv"
    merged_patch = HERE / "patches" / "ceg_rehunt_4agents.patch.jsonl"
    if all_rows:
        with merged_ledger.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(all_rows[0].keys()))
            w.writeheader()
            w.writerows(all_rows)
    with merged_patch.open("w", encoding="utf-8") as fh:
        for op in all_ops:
            fh.write(json.dumps(op, ensure_ascii=False) + "\n")

    rec = sum(1 for r in all_rows if r.get("result") == "RECOVERED")
    modes = Counter(r.get("mode", "") for r in all_rows if r.get("result") == "RECOVERED")
    report = HERE / "REHUNT_4AGENTS_REPORT.md"
    report.write_text(
        f"# CEG 4-Agent Re-Hunt Report\n\n"
        f"**Generated:** {NOW}\n\n"
        f"## Scope\n"
        f"- Agents: {', '.join(AGENTS)}\n"
        f"- Claims processed: **{len(all_rows)}**\n"
        f"- Recovered: **{rec}** ({100*rec/max(1,len(all_rows)):.1f}%)\n\n"
        f"## Recovery mode\n"
        + "".join(f"- {k}: {v}\n" for k, v in modes.most_common())
        + f"\n## Per agent\n"
        + "".join(
            f"- **{a}**: {sum(1 for r in all_rows if r.get('agent_id')==a)} processed, "
            f"{sum(1 for r in all_rows if r.get('agent_id')==a and r.get('result')=='RECOVERED')} recovered\n"
            for a in AGENTS
        )
        + f"\n## Artifacts\n"
        f"- `{merged_ledger.name}`\n"
        f"- `{merged_patch.name}` ({len(all_ops)} ops)\n"
        f"- Per-agent: `ledger/rehunt_CEG-R*.csv`, `patches/rehunt_CEG-R*.patch.jsonl`\n",
        encoding="utf-8",
    )

    print(f"\nmerged: {rec}/{len(all_rows)} recovered, {len(all_ops)} patch ops")
    print(f"report: {report}")

    dry = subprocess.call(
        [sys.executable, str(REPO / "_scripts/apply_neo4j_review_patch.py"),
         "--patch", str(merged_patch), "--dry-run"],
        cwd=str(REPO),
    )
    print(f"dry-run exit: {dry}")


if __name__ == "__main__":
    main()
