"""Draft gated remediation patches from agent_06b ledger.

Outputs (dry-run only — no apply):
  patches/agent06b_delete_self_loop.patch.jsonl
  patches/agent06b_relabel_connection_kind.patch.jsonl
  patches/agent06b_merge_duplicate_reverse.patch.jsonl
  patches/agent06b_add_node_sources.patch.jsonl
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
node_by_id = {n["id"]: n for n in nodes if n["id"]}
agent15_ids: set[str] = set()
p15 = PATCHES / "agent15_add_node_sources.patch.jsonl"
if p15.exists():
    for line in p15.read_text(encoding="utf-8").splitlines():
        if line.strip():
            agent15_ids.add(json.loads(line)["id"])

rows = list(csv.DictReader((HERE / "ledger" / "agent_06b.csv").open(encoding="utf-8")))


def isurl(s: str | None) -> bool:
    return isinstance(s, str) and s.strip().lower().startswith("http")


# 1. DELETE self-loop
delete_ops = []
for r in rows:
    if r["proposed_action"] == "DELETE" and r["claim_kind"] == "rel":
        delete_ops.append({
            "op": "delete_rel",
            "from": r["from_id"],
            "type": r["rel_type_or_label"],
            "to": r["to_id"],
            "reason": (
                f"Agent 06b {r['claim_id']}: {r['notes'][:200]}"
            ),
        })

# 2. RELABEL connection_kind (edges where 06b notes recommend downgrade)
relabel_ops = []
for r in rows:
    notes = (r.get("notes") or "").lower()
    if r["claim_kind"] != "rel":
        continue
    if "relabel connection_kind to consortium_co_membership" not in notes:
        continue
    relabel_ops.append({
        "op": "set_rel_properties",
        "from": r["from_id"],
        "type": r["rel_type_or_label"],
        "to": r["to_id"],
        "properties": {
            "connection_kind": "consortium_co_membership",
            "evidence_url": r["basis_ref"].strip() if isurl(r["basis_ref"]) else None,
            "evidence_quote": (r.get("proof_quote") or "")[:500] or None,
            "evidence_confidence": "teilweise_belegt",
            "evidence_basis": "recreate_consortium_co_listing",
            "review_run": "agent_06b_non_bubble_actor_networks_2026_06_06",
        },
        "reason": (
            f"Agent 06b {r['claim_id']}: downgrade connection_kind to consortium_co_membership; "
            f"{r['notes'][:160]}"
        ),
    })
    # drop None property values
    relabel_ops[-1]["properties"] = {
        k: v for k, v in relabel_ops[-1]["properties"].items() if v is not None
    }

# 3. MERGE_DUPLICATE reverse legs (destructive delete_rel on bidir_reverse)
merge_ops = []
for r in rows:
    if r["proposed_action"] != "MERGE_DUPLICATE" or r["claim_kind"] != "rel":
        continue
    merge_ops.append({
        "op": "delete_rel",
        "from": r["from_id"],
        "type": r["rel_type_or_label"],
        "to": r["to_id"],
        "reason": (
            f"Agent 06b {r['claim_id']}: bidirectional reverse twin — collapse to canonical direction. "
            f"{r['notes'][:160]}"
        ),
    })

# 4. PROVEN node sources from 06b not in agent15 patch (nodes lacking on-graph source)
add_source_ops: OrderedDict[str, dict] = OrderedDict()
for r in rows:
    if r["claim_kind"] != "node" or r["verdict"] != "PROVEN" or not isurl(r["basis_ref"]):
        continue
    nid = r["element_id"]
    if nid in agent15_ids or nid in add_source_ops:
        continue
    gn = node_by_id.get(nid)
    if not gn:
        continue
    props = gn.get("props") or {}
    has_source = bool(
        props.get("primary_source_url")
        or props.get("source_url")
        or props.get("source_urls")
    )
    if has_source:
        continue
    url = r["basis_ref"].strip()
    add_source_ops[nid] = {
        "op": "set_node_properties",
        "id": nid,
        "properties": {
            "primary_source_url": url,
            "source_urls": [url],
        },
        "reason": (
            f"Agent 06b {r['claim_id']} verified entity at {url} (verdict PROVEN); "
            f"node lacks on-graph source_urls. proof: {(r.get('proof_quote') or '')[:120]}"
        ),
    }


def write_patch(name: str, ops: list[dict]) -> Path:
    path = PATCHES / name
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for rec in ops:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"wrote {len(ops)} -> {path.name}")
    return path


write_patch("agent06b_delete_self_loop.patch.jsonl", delete_ops)
write_patch("agent06b_relabel_connection_kind.patch.jsonl", relabel_ops)
write_patch("agent06b_merge_duplicate_reverse.patch.jsonl", merge_ops)
write_patch("agent06b_add_node_sources.patch.jsonl", list(add_source_ops.values()))
