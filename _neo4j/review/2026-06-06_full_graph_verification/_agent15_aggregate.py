"""Agent 15 (Aggregator) — merge ledgers, prove coverage, synthesize findings.

Pure local processing of the 14 shard ledgers + the read-only graph id export.
No Neo4j writes. Produces:
  VERIFICATION_LEDGER.csv         (merged, normalized, provenance-preserving)
  _agent15_work/coverage.json     (coverage stats for COVERAGE_PROOF.md)
  _agent15_work/synthesis.json    (verdict / severity / heatmap stats)
  _agent15_work/findings.json     (actionable rows for remediation + patches)
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

REL_TYPES = set()  # filled from graph

# ---------------------------------------------------------------- load graph
graph_nodes = json.loads((WORK / "graph_nodes.json").read_text(encoding="utf-8"))
graph_rels = json.loads((WORK / "graph_rels.json").read_text(encoding="utf-8"))

node_id_to_eid = {}
node_eid = set()
node_label = {}
for n in graph_nodes:
    node_eid.add(n["element_id"])
    if n["id"] is not None:
        node_id_to_eid[n["id"]] = n["element_id"]
    node_label[n["element_id"]] = n["labels"]

rel_eid = set()
rel_eid_type = {}
triple_to_eids = defaultdict(list)
rel_type_counts = Counter()
for r in graph_rels:
    rel_eid.add(r["element_id"])
    rel_eid_type[r["element_id"]] = r["type"]
    REL_TYPES.add(r["type"])
    rel_type_counts[r["type"]] += 1
    triple_to_eids[(r["from_id"], r["type"], r["to_id"])].append(r["element_id"])

# ---------------------------------------------------------------- load ledgers
all_rows = []
for i in range(1, 15):
    f = LEDGER_DIR / f"agent_{i:02d}.csv"
    with f.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            row["source_agent"] = f"{i:02d}"
            all_rows.append(row)

# ---------------------------------------------------------------- resolve coverage
# element-level coverage sets
covered_node_eids = set()
covered_rel_eids = set()
# type-level coverage (whole rel-type proven structurally, not per element)
type_level_rel_types = set()


def resolve_row(row):
    kind = (row.get("claim_kind") or "").strip()
    eid = (row.get("element_id") or "").strip()
    rtype = (row.get("rel_type_or_label") or "").strip()
    fid = (row.get("from_id") or "").strip()
    tid = (row.get("to_id") or "").strip()

    if kind == "invariant":
        return "invariant", "", "invariant"

    if kind == "node":
        # real eid?
        if eid in node_eid:
            covered_node_eids.add(eid)
            return "node", eid, "element"
        # logical id?
        if eid in node_id_to_eid:
            geid = node_id_to_eid[eid]
            covered_node_eids.add(geid)
            return "node", geid, "element"
        # group/synthetic node summary rows (e.g. _NF_SATISFIABLE_GROUP)
        if eid.startswith("_") or eid.endswith("_GROUP"):
            return "node-group", "", "type"
        return "node", "", "unmatched"

    if kind == "rel":
        # aggregate / type-level rows
        if eid.startswith("agg:") or (eid in REL_TYPES and not fid and not tid):
            t = eid.split(":", 1)[1] if eid.startswith("agg:") else eid
            if t in REL_TYPES:
                type_level_rel_types.add(t)
            return "rel-type", "", "type"
        # real eid?
        if eid in rel_eid:
            covered_rel_eids.add(eid)
            return "rel", eid, "element"
        # triple match
        if fid and tid and rtype:
            key = (fid, rtype, tid)
            eids = triple_to_eids.get(key)
            if eids:
                for e in eids:
                    covered_rel_eids.add(e)
                return "rel", ";".join(eids), "element"
        # synthetic r_FROM__TYPE__TO with no from/to columns: try parse
        if eid.startswith("r_") and "__" in eid and rtype:
            # cannot reliably split; attempt by rtype lower marker
            return "rel", "", "unmatched"
        return "rel", "", "unmatched"

    return kind or "unknown", "", "unmatched"


for row in all_rows:
    cov_level_kind, geid, match = resolve_row(row)
    row["coverage_level"] = match  # element | type | invariant | unmatched
    row["graph_element_id"] = geid
    row["match_status"] = cov_level_kind

# ---------------------------------------------------------------- write merged ledger
out = HERE / "VERIFICATION_LEDGER.csv"
with out.open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=ORIG_COLS + ADD_COLS, extrasaction="ignore")
    w.writeheader()
    for row in all_rows:
        w.writerow(row)

# ---------------------------------------------------------------- coverage proof
# element-level rel coverage including the type-level expansion (reported separately)
type_level_rel_eids = set()
for r in graph_rels:
    if r["type"] in type_level_rel_types:
        type_level_rel_eids.add(r["element_id"])

rel_elem_only = covered_rel_eids
rel_type_expanded = type_level_rel_eids - covered_rel_eids
rel_uncovered = rel_eid - covered_rel_eids - type_level_rel_eids

node_elem = covered_node_eids
node_uncovered = node_eid - covered_node_eids

# node coverage by label
def label_of(eid):
    labs = node_label.get(eid, [])
    return labs[0] if labs else "(none)"

uncovered_node_by_label = Counter(label_of(e) for e in node_uncovered)
covered_node_by_label = Counter(label_of(e) for e in node_elem)

# rel coverage by type
def rel_cov_by_type():
    out = {}
    for t in sorted(REL_TYPES):
        total = rel_type_counts[t]
        elem = sum(1 for e in covered_rel_eids if rel_eid_type[e] == t)
        typed = total if t in type_level_rel_types else 0
        out[t] = {
            "total": total,
            "element_level": elem,
            "type_level_only": (typed - elem) if t in type_level_rel_types else 0,
            "uncovered": total - elem - ((typed - elem) if t in type_level_rel_types else 0),
        }
    return out

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
}
(WORK / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")

# ---------------------------------------------------------------- synthesis
verdict_counts = Counter()
action_counts = Counter()
verdict_by_agent = defaultdict(Counter)
verdict_by_type = defaultdict(Counter)
for row in all_rows:
    v = (row.get("verdict") or "").strip() or "(blank)"
    a = row.get("source_agent")
    verdict_counts[v] += 1
    action_counts[(row.get("proposed_action") or "").strip() or "(blank)"] += 1
    verdict_by_agent[a][v] += 1
    verdict_by_type[(row.get("rel_type_or_label") or "").strip() or "(none)"][v] += 1

# review_run heatmap (from notes/basis where present is unreliable; use proof on bubble agents 01-06)
synthesis = {
    "total_rows": len(all_rows),
    "verdict_counts": dict(verdict_counts.most_common()),
    "action_counts": dict(action_counts.most_common()),
    "verdict_by_agent": {k: dict(v.most_common()) for k, v in sorted(verdict_by_agent.items())},
}
(WORK / "synthesis.json").write_text(json.dumps(synthesis, ensure_ascii=False, indent=2), encoding="utf-8")

# ---------------------------------------------------------------- findings (actionable)
NEG_VERDICTS = {"UNSUPPORTED", "CONTRADICTION", "SCHEMA_VIOLATION", "DEAD_LINK",
                "MISSING_EVIDENCE", "PARTIAL", "UNVERIFIABLE"}
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

action_finding_counts = Counter(f["action"] for f in findings)
print("merged_rows:", len(all_rows))
print("verdicts:", dict(verdict_counts.most_common()))
print("actions:", dict(action_counts.most_common()))
print("findings:", len(findings), "by_action:", dict(action_finding_counts.most_common()))
print("NODE cov: element", len(node_elem), "uncovered", len(node_uncovered))
print("REL cov: element", len(rel_elem_only), "type_only", len(rel_type_expanded), "uncovered", len(rel_uncovered))
print("type_level_rel_types:", sorted(type_level_rel_types))
print("uncovered_node_by_label:", dict(uncovered_node_by_label.most_common()))
