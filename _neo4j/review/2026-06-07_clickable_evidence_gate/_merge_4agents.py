import csv
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
AGENTS = ["CEG-R1", "CEG-R2", "CEG-R3", "CEG-R4"]
rows, ops = [], []
for a in AGENTS:
    rows.extend(csv.DictReader((HERE / "ledger" / f"rehunt_{a}.csv").open(encoding="utf-8")))
    p = HERE / "patches" / f"rehunt_{a}.patch.jsonl"
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            ops.append(json.loads(line))

with (HERE / "REHUNT_LEDGER_v2.csv").open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
with (HERE / "patches/ceg_rehunt_4agents.patch.jsonl").open("w", encoding="utf-8") as fh:
    for op in ops:
        fh.write(json.dumps(op, ensure_ascii=False) + "\n")

rec = sum(1 for r in rows if r["result"] == "RECOVERED")
modes = Counter(r["mode"] for r in rows if r["result"] == "RECOVERED")
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
lines = [
    "# CEG 4-Agent Re-Hunt Report", "", f"**Generated:** {NOW}", "",
    "## Results",
    f"- Claims processed: **{len(rows)}**",
    f"- Recovered: **{rec}** ({100 * rec / len(rows):.1f}%)",
    f"- Patch ops: **{len(ops)}** (proposal only, not applied)", "",
    "## Recovery mode",
]
for k, v in modes.most_common():
    lines.append(f"- {k}: {v}")
lines += ["", "## Per agent"]
for a in AGENTS:
    n = sum(1 for r in rows if r.get("agent_id") == a)
    ok = sum(1 for r in rows if r.get("agent_id") == a and r.get("result") == "RECOVERED")
    lines.append(f"- **{a}**: {n} processed, {ok} recovered")
(HERE / "REHUNT_4AGENTS_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"recovered {rec}/{len(rows)}, {len(ops)} ops")
subprocess.call([
    sys.executable, str(REPO / "_scripts/apply_neo4j_review_patch.py"),
    "--patch", str(HERE / "patches/ceg_rehunt_4agents.patch.jsonl"), "--dry-run",
], cwd=str(REPO))
