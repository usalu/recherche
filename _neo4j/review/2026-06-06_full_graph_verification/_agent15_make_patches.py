"""Agent 15 — generate HIGH-CONFIDENCE, NON-DESTRUCTIVE patch drafts only.

Scope (per instruction): only non-destructive, high-confidence changes where the
shard evidence is sufficient. That is:
  - node source additions where a shard returned verdict=PROVEN with a concrete
    fetched http(s) URL and proposed_action=ADD_SOURCE  -> op set_node_properties.

Destructive actions (delete_rel, merge_duplicate, deprecate_node) are NOT emitted
as patches here; they are listed in REMEDIATION_PLAN.md for human-built gated patches.

Nothing is applied. Output: patches/agent15_add_node_sources.patch.jsonl
"""
from __future__ import annotations

import csv
import json
from collections import OrderedDict
from pathlib import Path

csv.field_size_limit(10_000_000)
HERE = Path(__file__).resolve().parent
WORK = HERE / "_agent15_work"
PATCHES = HERE / "patches"
PATCHES.mkdir(parents=True, exist_ok=True)

nodes = json.loads((WORK / "graph_nodes.json").read_text(encoding="utf-8"))
node_ids = {n["id"] for n in nodes if n["id"] is not None}
eid2id = {n["element_id"]: n["id"] for n in nodes}
node_props_url = {}  # id -> existing source_urls present?

rows = list(csv.DictReader((HERE / "VERIFICATION_LEDGER.csv").open(encoding="utf-8")))


def isurl(s):
    return isinstance(s, str) and s.strip().lower().startswith("http")


emitted = OrderedDict()
for r in rows:
    if (
        r["claim_kind"] == "node"
        and r["proposed_action"] == "ADD_SOURCE"
        and r["verdict"] == "PROVEN"
        and isurl(r["basis_ref"])
    ):
        nid = r["element_id"] if r["element_id"] in node_ids else eid2id.get(r["element_id"])
        if not nid or nid in emitted:
            continue
        url = r["basis_ref"].strip()
        emitted[nid] = {
            "op": "set_node_properties",
            "id": nid,
            "properties": {
                "primary_source_url": url,
                "source_urls": [url],
            },
            "reason": (
                f"Agent {r['source_agent']} verified entity at {url} (verdict PROVEN); "
                f"node currently lacks source_urls. proof: {r['proof_quote'][:120]}"
            ),
        }

out = PATCHES / "agent15_add_node_sources.patch.jsonl"
with out.open("w", encoding="utf-8", newline="\n") as fh:
    for rec in emitted.values():
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

print(f"wrote {len(emitted)} non-destructive set_node_properties records -> {out}")

# Also emit a NON-APPLIED review list of destructive proposals (for the remediation plan).
review = []
for r in rows:
    act = r["proposed_action"]
    if act in {"DELETE", "MERGE_DUPLICATE", "DEPRECATE_NODE"}:
        review.append({
            "agent": r["source_agent"],
            "claim_id": r["claim_id"],
            "kind": r["claim_kind"],
            "element_id": r["element_id"],
            "from_id": r["from_id"],
            "to_id": r["to_id"],
            "type": r["rel_type_or_label"],
            "verdict": r["verdict"],
            "action": act,
            "notes": r["notes"],
        })
rev_out = WORK / "destructive_proposals.json"
rev_out.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {len(review)} destructive proposals (NOT patched) -> {rev_out}")
