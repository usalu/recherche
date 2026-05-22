"""Agent 15b — merge agent_06b ledger into VERIFICATION_LEDGER.csv.

Extends Agent 15 (_agent15_aggregate.py) by appending shard 06b and recomputing
coverage + synthesis. No Neo4j writes.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(10_000_000)

HERE = Path(__file__).resolve().parent
LEDGER_DIR = HERE / "ledger"
WORK = HERE / "_agent15_work"
WORK.mkdir(parents=True, exist_ok=True)

ORIG_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id",
    "rel_type_or_label", "asserted_claim", "basis_type", "basis_ref",
    "fetched", "http_status", "verdict", "confidence", "proof_quote",
    "proposed_action", "agent_id", "notes",
]
ADD_COLS = ["source_agent", "coverage_level", "graph_element_id", "match_status"]

REL_TYPES: set[str] = set()

graph_nodes = json.loads((WORK / "graph_nodes.json").read_text(encoding="utf-8"))
graph_rels = json.loads((WORK / "graph_rels.json").read_text(encoding="utf-8"))

node_id_to_eid: dict[str, str] = {}
node_eid: set[str] = set()
node_label: dict[str, list[str]] = {}
for n in graph_nodes:
    node_eid.add(n["element_id"])
    if n["id"] is not None:
        node_id_to_eid[n["id"]] = n["element_id"]
    node_label[n["element_id"]] = n["labels"]

rel_eid: set[str] = set()
rel_eid_type: dict[str, str] = {}
triple_to_eids: dict[tuple[str, str, str], list[str]] = defaultdict(list)
rel_type_counts: Counter[str] = Counter()
for r in graph_rels:
    rel_eid.add(r["element_id"])
    rel_eid_type[r["element_id"]] = r["type"]
    REL_TYPES.add(r["type"])
    rel_type_counts[r["type"]] += 1
    triple_to_eids[(r["from_id"], r["type"], r["to_id"])].append(r["element_id"])

SHARD_FILES = [LEDGER_DIR / f"agent_{i:02d}.csv" for i in range(1, 15)]
SHARD_FILES.append(LEDGER_DIR / "agent_06b.csv")

all_rows: list[dict[str, str]] = []
for f in SHARD_FILES:
    if not f.exists():
        print(f"WARN missing shard {f}", file=sys.stderr)
        continue
    agent_tag = "06b" if f.name == "agent_06b.csv" else f.stem.split("_", 1)[1]
    with f.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            row["source_agent"] = agent_tag
            all_rows.append(row)

covered_node_eids: set[str] = set()
covered_rel_eids: set[str] = set()
type_level_rel_types: set[str] = set()


def resolve_row(row: dict[str, str]) -> tuple[str, str, str]:
    kind = (row.get("claim_kind") or "").strip()
    eid = (row.get("element_id") or "").strip()
    rtype = (row.get("rel_type_or_label") or "").strip()
    fid = (row.get("from_id") or "").strip()
    tid = (row.get("to_id") or "").strip()

    if kind == "invariant":
        return "invariant", "", "invariant"

    if kind == "node":
        if eid in node_eid:
            covered_node_eids.add(eid)
            return "node", eid, "element"
        if eid in node_id_to_eid:
            geid = node_id_to_eid[eid]
            covered_node_eids.add(geid)
            return "node", geid, "element"
        if eid.startswith("_") or eid.endswith("_GROUP"):
            return "node-group", "", "type"
        return "node", "", "unmatched"

    if kind == "rel":
        if eid.startswith("agg:") or (eid in REL_TYPES and not fid and not tid):
            t = eid.split(":", 1)[1] if eid.startswith("agg:") else eid
            if t in REL_TYPES:
                type_level_rel_types.add(t)
            return "rel-type", "", "type"
        if eid in rel_eid:
            covered_rel_eids.add(eid)
            return "rel", eid, "element"
        if fid and tid and rtype:
            key = (fid, rtype, tid)
            eids = triple_to_eids.get(key)
            if eids:
                for e in eids:
                    covered_rel_eids.add(e)
                return "rel", ";".join(eids), "element"
        if eid.startswith("r_") and "__" in eid and rtype:
            return "rel", "", "unmatched"
        return "rel", "", "unmatched"

    return kind or "unknown", "", "unmatched"


for row in all_rows:
    cov_level_kind, geid, match = resolve_row(row)
    row["coverage_level"] = match
    row["graph_element_id"] = geid
    row["match_status"] = cov_level_kind

out = HERE / "VERIFICATION_LEDGER.csv"
with out.open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=ORIG_COLS + ADD_COLS, extrasaction="ignore")
    w.writeheader()
    for row in all_rows:
        w.writerow(row)

type_level_rel_eids: set[str] = set()
for r in graph_rels:
    if r["type"] in type_level_rel_types:
        type_level_rel_eids.add(r["element_id"])

rel_elem_only = covered_rel_eids
rel_type_expanded = type_level_rel_eids - covered_rel_eids
rel_uncovered = rel_eid - covered_rel_eids - type_level_rel_eids

node_elem = covered_node_eids
node_uncovered = node_eid - covered_node_eids


def label_of(eid: str) -> str:
    labs = node_label.get(eid, [])
    return labs[0] if labs else "(none)"


uncovered_node_by_label = Counter(label_of(e) for e in node_uncovered)
covered_node_by_label = Counter(label_of(e) for e in node_elem)


def rel_cov_by_type() -> dict:
    out_d: dict = {}
    for t in sorted(REL_TYPES):
        total = rel_type_counts[t]
        elem = sum(1 for e in covered_rel_eids if rel_eid_type[e] == t)
        typed = total if t in type_level_rel_types else 0
        out_d[t] = {
            "total": total,
            "element_level": elem,
            "type_level_only": (typed - elem) if t in type_level_rel_types else 0,
            "uncovered": total - elem - ((typed - elem) if t in type_level_rel_types else 0),
        }
    return out_d


coverage = {
    "graph": {"nodes": len(node_eid), "rels": len(rel_eid)},
    "nodes": {
        "element_covered": len(node_elem),
        "uncovered": len(node_uncovered),
        "uncovered_by_label": dict(uncovered_node_by_label.most_common()),
        "covered_by_label": dict(covered_node_by_label.most_common()),
        "uncovered_ids": sorted(
            [next((n["id"] for n in graph_nodes if n["element_id"] == e), e) for e in node_uncovered]
        )[:500],
    },
    "rels": {
        "element_covered": len(rel_elem_only),
        "type_level_only": len(rel_type_expanded),
        "uncovered": len(rel_uncovered),
        "by_type": rel_cov_by_type(),
        "type_level_rel_types": sorted(type_level_rel_types),
    },
    "merged_shards": len(SHARD_FILES),
    "merged_rows": len(all_rows),
    "agent_06b_rows": sum(1 for r in all_rows if r["source_agent"] == "06b"),
}
(WORK / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")

verdict_counts: Counter[str] = Counter()
action_counts: Counter[str] = Counter()
verdict_by_agent: dict[str, Counter[str]] = defaultdict(Counter)
for row in all_rows:
    v = (row.get("verdict") or "").strip() or "(blank)"
    a = row["source_agent"]
    verdict_counts[v] += 1
    action_counts[(row.get("proposed_action") or "").strip() or "(blank)"] += 1
    verdict_by_agent[a][v] += 1

synthesis = {
    "total_rows": len(all_rows),
    "verdict_counts": dict(verdict_counts.most_common()),
    "action_counts": dict(action_counts.most_common()),
    "verdict_by_agent": {k: dict(v.most_common()) for k, v in sorted(verdict_by_agent.items())},
}
(WORK / "synthesis.json").write_text(json.dumps(synthesis, ensure_ascii=False, indent=2), encoding="utf-8")

NEG_VERDICTS = {
    "UNSUPPORTED", "CONTRADICTION", "SCHEMA_VIOLATION", "DEAD_LINK",
    "MISSING_EVIDENCE", "PARTIAL", "UNVERIFIABLE",
}
findings = []
for row in all_rows:
    v = (row.get("verdict") or "").strip()
    act = (row.get("proposed_action") or "").strip()
    if v in NEG_VERDICTS or (act and act != "KEEP"):
        findings.append({
            "claim_id": row.get("claim_id"),
            "agent": row.get("source_agent"),
            "kind": row.get("claim_kind"),
            "element_id": row.get("element_id"),
            "graph_element_id": row.get("graph_element_id"),
            "from_id": row.get("from_id"),
            "to_id": row.get("to_id"),
            "type": row.get("rel_type_or_label"),
            "verdict": v,
            "action": act,
            "match_status": row.get("match_status"),
            "notes": row.get("notes"),
            "proof_quote": row.get("proof_quote"),
        })
(WORK / "findings.json").write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")

print("merged_rows:", len(all_rows))
print("agent_06b_rows:", coverage["agent_06b_rows"])
print("verdicts:", dict(verdict_counts.most_common()))
print("actions:", dict(action_counts.most_common()))
print("findings:", len(findings))
print("NODE cov: element", len(node_elem), "uncovered", len(node_uncovered))
print("REL cov: element", len(rel_elem_only), "type_only", len(rel_type_expanded), "uncovered", len(rel_uncovered))
print("uncovered_node_by_label:", dict(uncovered_node_by_label.most_common()))
verb_cov = rel_cov_by_type().get("VERBUNDEN_MIT_AKTEUR", {})
print("VERBUNDEN_MIT_AKTEUR:", verb_cov)
