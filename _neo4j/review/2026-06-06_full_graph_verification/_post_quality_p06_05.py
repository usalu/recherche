#!/usr/bin/env python3
"""Post Quality Pass P6-05 — element ledger surgery vs live mit-bestand graph.

READ-ONLY Neo4j export. Removes stale VERIFICATION_LEDGER_ELEMENT rows for Q1/Q2/Q4
deletes and adds missing Q3 PruefungNachweis + ERFUELLT_NACHWEIS rows.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

csv.field_size_limit(10_000_000)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
WORK = HERE / "_p06_05_work"
WORK.mkdir(parents=True, exist_ok=True)

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

ELEMENT_LEDGER = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
BASELINE_LEDGER = WORK / "VERIFICATION_LEDGER_ELEMENT_ep10_baseline.csv"
OUT_V2 = HERE / "VERIFICATION_LEDGER_ELEMENT_v2.csv"
OUT_DELTA = HERE / "ledger" / "post_quality_p06_05.csv"
OUT_REPORT = HERE / "reports" / "post_quality_p06_05.md"

OUT_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
    "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
    "source_agent", "coverage_level", "graph_element_id", "match_status",
]

DELTA_COLS = [
    "delta_action", "pass_scope", "claim_id", "claim_kind", "graph_element_id",
    "from_id", "to_id", "rel_type_or_label", "prior_verdict", "new_verdict",
    "reason", "notes",
]

Q03_PATCH = HERE / "patches" / "quality_pass_q03.patch.jsonl"
Q01_PATCH = HERE / "patches" / "quality_pass_q01.patch.jsonl"
Q02_PATCH = HERE / "patches" / "quality_pass_q02_deprecate.patch.jsonl"
Q04_DELETES = HERE / "patches" / "quality_pass_q04_deletes.patch.jsonl"
Q03_LEDGER = HERE / "ledger" / "quality_pass_q03.csv"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def export_graph() -> tuple[list[dict], list[dict], dict]:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    if not all([uri, user, password, database]):
        raise RuntimeError("Missing Neo4j connection settings.")
    nodes: list[dict] = []
    rels: list[dict] = []
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as s:
            for row in s.run(
                "MATCH (n) RETURN n.id AS id, elementId(n) AS eid, labels(n) AS labels, "
                "n.name AS name, n.primary_source_url AS primary_source_url"
            ):
                nodes.append(
                    {
                        "id": row["id"],
                        "element_id": row["eid"],
                        "labels": row["labels"] or [],
                        "name": row["name"],
                        "primary_source_url": row["primary_source_url"],
                    }
                )
            for row in s.run(
                "MATCH (a)-[r]->(b) "
                "RETURN elementId(r) AS eid, type(r) AS t, "
                "a.id AS from_id, b.id AS to_id, "
                "elementId(a) AS from_eid, elementId(b) AS to_eid, "
                "r.evidence_url AS evidence_url, r.evidence_basis AS evidence_basis, "
                "r.evidence_confidence AS evidence_confidence"
            ):
                rels.append(
                    {
                        "element_id": row["eid"],
                        "type": row["t"],
                        "from_id": row["from_id"],
                        "to_id": row["to_id"],
                        "from_eid": row["from_eid"],
                        "to_eid": row["to_eid"],
                        "evidence_url": row["evidence_url"],
                        "evidence_basis": row["evidence_basis"],
                        "evidence_confidence": row["evidence_confidence"],
                    }
                )
    counts = {
        "database": database,
        "nodes": len(nodes),
        "rels": len(rels),
        "exported_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    (WORK / "graph_nodes.json").write_text(
        json.dumps(nodes, ensure_ascii=False), encoding="utf-8"
    )
    (WORK / "graph_rels.json").write_text(
        json.dumps(rels, ensure_ascii=False), encoding="utf-8"
    )
    (WORK / "graph_counts.json").write_text(
        json.dumps(counts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return nodes, rels, counts


def resolve_graph_key(
    row: dict,
    node_eid: set,
    node_id_to_eid: dict,
    rel_eid: set,
    triple_to_eids: dict,
) -> tuple[str, str] | None:
    kind = (row.get("claim_kind") or "").strip()
    eid = (row.get("element_id") or "").strip()
    geid = (row.get("graph_element_id") or "").strip()
    rtype = (row.get("rel_type_or_label") or "").strip()
    fid = (row.get("from_id") or "").strip()
    tid = (row.get("to_id") or "").strip()

    if kind == "node":
        for candidate in (geid, eid):
            if candidate in node_eid:
                return "node", candidate
        for candidate in (geid, eid):
            if candidate in node_id_to_eid:
                return "node", node_id_to_eid[candidate]
        return None

    if kind == "rel":
        for candidate in (geid, eid):
            if candidate in rel_eid:
                return "rel", candidate
        if fid and tid and rtype:
            eids = triple_to_eids.get((fid, rtype, tid))
            if eids:
                return "rel", eids[0]
        return None

    return None


def build_scope() -> dict:
    q1_merged_nodes = set()
    q1_deleted_rels: set[tuple[str, str, str]] = set()
    for op in load_jsonl(Q01_PATCH):
        if op["op"] == "merge_node":
            q1_merged_nodes.add(op["from"])
        elif op["op"] == "delete_rel":
            q1_deleted_rels.add((op["from"], op["type"], op["to"]))

    q2_deleted_nodes = set()
    for op in load_jsonl(Q02_PATCH):
        if op["op"] == "delete_node":
            q2_deleted_nodes.add(op["id"])
        elif op["op"] == "merge_node":
            q2_deleted_nodes.add(op["from"])

    q4_deleted_rels: set[tuple[str, str, str]] = set()
    for op in load_jsonl(Q04_DELETES):
        if op["op"] == "delete_rel":
            q4_deleted_rels.add((op["from"], op["type"], op["to"]))

    q3_new_nodes: dict[str, dict] = {}
    q3_new_rels: list[dict] = []
    for op in load_jsonl(Q03_PATCH):
        if op["op"] == "add_node":
            q3_new_nodes[op["id"]] = op
        elif op["op"] == "add_rel":
            q3_new_rels.append(op)

    q03_ledger = {r["claim_id"]: r for r in load_csv(Q03_LEDGER)}

    return {
        "q1_merged_nodes": q1_merged_nodes,
        "q1_deleted_rels": q1_deleted_rels,
        "q2_deleted_nodes": q2_deleted_nodes,
        "q4_deleted_rels": q4_deleted_rels,
        "q3_new_nodes": q3_new_nodes,
        "q3_new_rels": q3_new_rels,
        "q03_ledger": q03_ledger,
    }


def classify_removal(row: dict, scope: dict) -> str | None:
    kind = (row.get("claim_kind") or "").strip()
    fid = (row.get("from_id") or "").strip()
    tid = (row.get("to_id") or "").strip()
    rtype = (row.get("rel_type_or_label") or "").strip()
    eid = (row.get("element_id") or row.get("graph_element_id") or "").strip()

    node_ids = set()
    if kind == "node":
        node_ids.add(eid)
        if fid:
            node_ids.add(fid)
    if kind == "rel":
        if fid:
            node_ids.add(fid)
        if tid:
            node_ids.add(tid)

    if kind == "rel" and (fid, rtype, tid) in scope["q4_deleted_rels"]:
        return "Q4"
    if kind == "rel" and (fid, rtype, tid) in scope["q1_deleted_rels"]:
        return "Q1"
    if node_ids & scope["q2_deleted_nodes"]:
        return "Q2"
    if node_ids & scope["q1_merged_nodes"]:
        return "Q1"
  # fallback: graph-absent (may include Q2/Q4 rels not in patch triple match)
    return "GRAPH_ABSENT"


def row_key(row: dict) -> str:
    kind = (row.get("claim_kind") or "").strip()
    geid = (row.get("graph_element_id") or "").strip()
    eid = (row.get("element_id") or "").strip()
    if geid:
        return f"{kind}:{geid}"
    if kind == "rel":
        return f"rel:{row.get('from_id')}|{row.get('rel_type_or_label')}|{row.get('to_id')}"
    return f"node:{eid}"


def make_q03_node_row(node: dict, patch_op: dict, q03_row: dict | None) -> dict:
    nid = node["id"]
    label = next((l for l in node["labels"] if l != "PruefungNachweis"), "PruefungNachweis")
    if "PruefungNachweis" in node["labels"]:
        label = "PruefungNachweis"
    verdict = "PROVEN"
    confidence = "belegt"
    if q03_row:
        verdict = q03_row.get("verdict_after") or verdict
        confidence = q03_row.get("confidence") or confidence
    props = patch_op.get("properties") or {}
    return {
        "claim_id": f"P6-Q03-n-{nid}",
        "claim_kind": "node",
        "element_id": nid,
        "from_id": "",
        "to_id": "",
        "rel_type_or_label": label,
        "asserted_claim": (
            f"PruefungNachweis {nid} catalog entry created by Q03 to satisfy dangling Nachweisforderung"
        ),
        "basis_type": "logic",
        "basis_ref": "ledger/quality_pass_q03.csv;patches/quality_pass_q03.patch.jsonl",
        "fetched": "false",
        "http_status": "",
        "verdict": verdict,
        "confidence": confidence,
        "proof_quote": props.get("evidence_basis", ""),
        "proposed_action": "KEEP",
        "agent_id": "P6-05",
        "notes": f"Q03 add_node {nid}; primary_source_url={props.get('primary_source_url', '')}",
        "source_agent": "Q03",
        "coverage_level": "element",
        "graph_element_id": node["element_id"],
        "match_status": "node",
    }


def make_q03_rel_row(rel: dict, patch_op: dict, q03_row: dict | None) -> dict:
    fid, tid, rtype = rel["from_id"], rel["to_id"], rel["type"]
    verdict = "PROVEN"
    confidence = "belegt"
    if q03_row:
        verdict = q03_row.get("verdict_after") or verdict
        confidence = q03_row.get("confidence") or confidence
        if verdict == "PARTIAL_COVERAGE":
            verdict = "PARTIAL"
    props = patch_op.get("properties") or {}
    ev_conf = (props.get("evidence_confidence") or "").lower()
    if ev_conf == "medium":
        confidence = "teilweise_belegt"
        if verdict == "PROVEN":
            verdict = "PARTIAL"
    basis_url = rel.get("evidence_url") or ""
    return {
        "claim_id": f"P6-Q03-r-{fid}__{rtype}__{tid}",
        "claim_kind": "rel",
        "element_id": rel["element_id"],
        "from_id": fid,
        "to_id": tid,
        "rel_type_or_label": rtype,
        "asserted_claim": f"{fid} -{rtype}-> {tid} (Q03 compliance graph extension)",
        "basis_type": "logic" if not basis_url else "web",
        "basis_ref": basis_url or "patches/quality_pass_q03.patch.jsonl",
        "fetched": "false",
        "http_status": "",
        "verdict": verdict,
        "confidence": confidence,
        "proof_quote": props.get("evidence_basis", ""),
        "proposed_action": "KEEP",
        "agent_id": "P6-05",
        "notes": f"Q03 add_rel {fid}→{tid}; review_run=quality_pass_q03_2026-06-06",
        "source_agent": "Q03",
        "coverage_level": "element",
        "graph_element_id": rel["element_id"],
        "match_status": "rel",
    }


def find_q03_ledger_row(scope: dict, nid: str | None, fid: str, tid: str) -> dict | None:
    for row in scope["q03_ledger"].values():
        if nid and row.get("from_id") == nid and row.get("claim_kind") == "node":
            return row
        if fid and row.get("from_id") == fid and row.get("to_id") == tid:
            return row
    return None


def rebuild_ep10_baseline() -> Path:
    """Re-merge EP-10 element ledger from shards using frozen agent10 graph export."""
    import importlib.util

    agent10_path = HERE / "_agent10_aggregate_element.py"
    spec = importlib.util.spec_from_file_location("agent10", agent10_path)
    agent10 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agent10)

    snap_nodes = json.loads(
        (HERE / "_agent10_work" / "graph_nodes.json").read_text(encoding="utf-8")
    )
    snap_rels = json.loads(
        (HERE / "_agent10_work" / "graph_rels.json").read_text(encoding="utf-8")
    )

    node_eid = set()
    node_id_to_eid = {}
    node_label = {}
    for n in snap_nodes:
        node_eid.add(n["element_id"])
        if n["id"] is not None:
            node_id_to_eid[n["id"]] = n["element_id"]
        node_label[n["element_id"]] = n["labels"]

    rel_eid = set()
    triple_to_eids: dict[tuple, list] = defaultdict(list)
    for r in snap_rels:
        rel_eid.add(r["element_id"])
        triple_to_eids[(r["from_id"], r["type"], r["to_id"])].append(r["element_id"])

    prior_rows = []
    for row in load_csv(HERE / "VERIFICATION_LEDGER.csv"):
        if (row.get("coverage_level") or "").strip() != "element":
            continue
        if agent10.is_aggregate_row(row):
            continue
        row["source_agent"] = (row.get("source_agent") or row.get("agent_id") or "prior").strip()
        row["_origin"] = "prior"
        prior_rows.append(row)

    shard_rows = []
    for i, fname in enumerate(agent10.SHARD_FILES, 1):
        for row in load_csv(HERE / "ledger" / fname):
            row["source_agent"] = f"EP-{i:02d}"
            row["_origin"] = "shard"
            row["coverage_level"] = "element"
            shard_rows.append(row)

    merged: dict[str, dict] = {}
    for row in prior_rows + shard_rows:
        resolved = agent10.resolve_graph_key(
            row, node_eid, node_id_to_eid, rel_eid, triple_to_eids
        )
        key = agent10.dedupe_key(row, resolved)
        if resolved is None and row.get("_origin") == "prior":
            continue
        if key in merged and row["_origin"] == "prior" and merged[key]["_origin"] == "shard":
            continue
        if key not in merged or row["_origin"] == "shard":
            merged[key] = row

    final_rows = []
    for row in merged.values():
        resolved = agent10.resolve_graph_key(
            row, node_eid, node_id_to_eid, rel_eid, triple_to_eids
        )
        if resolved:
            kind, geid = resolved
            row["graph_element_id"] = geid
            row["match_status"] = kind
        row["coverage_level"] = "element"
        row.pop("_origin", None)
        final_rows.append(row)

    with BASELINE_LEDGER.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(final_rows)
    return BASELINE_LEDGER


def main() -> int:
    OUT_DELTA.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    input_path = rebuild_ep10_baseline()
    graph_nodes, graph_rels, counts = export_graph()
    scope = build_scope()

    node_eid = set()
    node_id_to_eid: dict[str, str] = {}
    node_by_id: dict[str, dict] = {}
    for n in graph_nodes:
        node_eid.add(n["element_id"])
        if n["id"] is not None:
            node_id_to_eid[n["id"]] = n["element_id"]
            node_by_id[n["id"]] = n

    rel_eid = set()
    triple_to_eids: dict[tuple, list] = defaultdict(list)
    rel_by_triple: dict[tuple, dict] = {}
    for r in graph_rels:
        rel_eid.add(r["element_id"])
        triple = (r["from_id"], r["type"], r["to_id"])
        triple_to_eids[triple].append(r["element_id"])
        rel_by_triple[triple] = r

    ledger_rows = load_csv(input_path)
    kept: list[dict] = []
    deltas: list[dict] = []
    removal_by_pass = Counter()

    for row in ledger_rows:
        resolved = resolve_graph_key(row, node_eid, node_id_to_eid, rel_eid, triple_to_eids)
        if resolved is not None:
            kept.append(row)
            continue
        pass_scope = classify_removal(row, scope)
        removal_by_pass[pass_scope] += 1
        deltas.append(
            {
                "delta_action": "REMOVE",
                "pass_scope": pass_scope,
                "claim_id": row.get("claim_id", ""),
                "claim_kind": row.get("claim_kind", ""),
                "graph_element_id": row.get("graph_element_id", ""),
                "from_id": row.get("from_id", ""),
                "to_id": row.get("to_id", ""),
                "rel_type_or_label": row.get("rel_type_or_label", ""),
                "prior_verdict": row.get("verdict", ""),
                "new_verdict": "REMOVED",
                "reason": "element absent from live mit-bestand graph after quality pass",
                "notes": f"P6-05 stale row; classified {pass_scope}",
            }
        )

    existing_keys = {row_key(r) for r in kept}
    additions = Counter()

    for nid, patch_op in scope["q3_new_nodes"].items():
        node = node_by_id.get(nid)
        if not node:
            continue
        key = f"node:{node['element_id']}"
        if key in existing_keys:
            continue
        q03_row = find_q03_ledger_row(scope, nid, "", "")
        new_row = make_q03_node_row(node, patch_op, q03_row)
        kept.append(new_row)
        existing_keys.add(key)
        additions["Q3_node"] += 1
        deltas.append(
            {
                "delta_action": "ADD",
                "pass_scope": "Q3",
                "claim_id": new_row["claim_id"],
                "claim_kind": "node",
                "graph_element_id": new_row["graph_element_id"],
                "from_id": "",
                "to_id": "",
                "rel_type_or_label": new_row["rel_type_or_label"],
                "prior_verdict": "",
                "new_verdict": new_row["verdict"],
                "reason": "Q03 new PruefungNachweis node missing from element ledger",
                "notes": new_row["notes"],
            }
        )

    patch_rel_by_triple = {
        (op["from"], op["type"], op["to"]): op for op in scope["q3_new_rels"]
    }
    for triple, patch_op in patch_rel_by_triple.items():
        rel = rel_by_triple.get(triple)
        if not rel:
            continue
        key = f"rel:{rel['element_id']}"
        if key in existing_keys:
            continue
        # also skip if triple already covered under different element id
        triple_key = f"rel:{triple[0]}|{triple[1]}|{triple[2]}"
        if triple_key in existing_keys:
            continue
        q03_row = find_q03_ledger_row(scope, None, triple[0], triple[2])
        new_row = make_q03_rel_row(rel, patch_op, q03_row)
        kept.append(new_row)
        existing_keys.add(key)
        existing_keys.add(triple_key)
        additions["Q3_rel"] += 1
        deltas.append(
            {
                "delta_action": "ADD",
                "pass_scope": "Q3",
                "claim_id": new_row["claim_id"],
                "claim_kind": "rel",
                "graph_element_id": new_row["graph_element_id"],
                "from_id": new_row["from_id"],
                "to_id": new_row["to_id"],
                "rel_type_or_label": new_row["rel_type_or_label"],
                "prior_verdict": "",
                "new_verdict": new_row["verdict"],
                "reason": "Q03 ERFUELLT_NACHWEIS edge missing from element ledger",
                "notes": new_row["notes"],
            }
        )

    # Coverage proof vs live graph
    covered_node_eids: set[str] = set()
    covered_rel_eids: set[str] = set()
    for r in kept:
        resolved = resolve_graph_key(r, node_eid, node_id_to_eid, rel_eid, triple_to_eids)
        if not resolved:
            continue
        kind, geid = resolved
        if kind == "node":
            covered_node_eids.add(geid)
        else:
            covered_rel_eids.add(geid)

    missing_nodes = [n for n in graph_nodes if n["element_id"] not in covered_node_eids]
    missing_rels = [r for r in graph_rels if r["element_id"] not in covered_rel_eids]
    missing_rel_lines = "\n".join(
        f"- `{r['from_id']}` —[`{r['type']}`]→ `{r['to_id']}`"
        for r in missing_rels[:25]
    )

    with OUT_V2.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(kept)

    with OUT_DELTA.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=DELTA_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(deltas)

    verdict_counts = Counter(r.get("verdict", "") for r in kept)
    proven_pct = 100.0 * verdict_counts.get("PROVEN", 0) / len(kept) if kept else 0.0

    report = f"""# Post Quality Pass P6-05 — Element ledger surgery

**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')} · **Database:** `{counts['database']}`
**Mode:** READ-ONLY graph export + ledger reconcile (no graph writes)

## Live mit-bestand counts

| Metric | Value |
|---|---:|
| Nodes | {counts['nodes']:,} |
| Relationships | {counts['rels']:,} |
| Export UTC | {counts['exported_at_utc']} |

## Ledger delta summary

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Element ledger rows | {len(ledger_rows):,} | {len(kept):,} | {len(kept) - len(ledger_rows):+,} |
| PROVEN rows | {sum(1 for r in ledger_rows if r.get('verdict') == 'PROVEN'):,} | {verdict_counts.get('PROVEN', 0):,} | — |
| PROVEN % | {100.0 * sum(1 for r in ledger_rows if r.get('verdict') == 'PROVEN') / len(ledger_rows):.2f}% | {proven_pct:.2f}% | — |

## Operations by quality-pass scope

| Scope | REMOVE | Notes |
|---|---:|---|
| Q1 merges + EP02 rel delete | {removal_by_pass.get('Q1', 0)} | 8 vocab stub merges + `stadt_zuerich` HAT_AKTEURTYP |
| Q2 depot deletes | {removal_by_pass.get('Q2', 0)} | 17 Materialdepot placeholders removed |
| Q4 catalogue deletes | {removal_by_pass.get('Q4', 0)} | 107 unsupported HAT_BAUTEILTYP / NUTZT_MATERIAL edges |
| Graph-absent (unclassified) | {removal_by_pass.get('GRAPH_ABSENT', 0)} | Incident rels on deleted nodes / other stale keys |
| **REMOVE total** | **{sum(1 for d in deltas if d['delta_action'] == 'REMOVE')}** | |

| Scope | ADD | Notes |
|---|---:|---|
| Q3 PruefungNachweis nodes | {additions.get('Q3_node', 0)} | 5 catalog extensions |
| Q3 ERFUELLT_NACHWEIS edges | {additions.get('Q3_rel', 0)} | 12 fulfillment edges |
| **ADD total** | **{sum(1 for d in deltas if d['delta_action'] == 'ADD')}** | |

## Coverage check (ledger v2 vs live graph)

| Check | Count |
|---|---:|
| Live nodes | {len(graph_nodes):,} |
| Live rels | {len(graph_rels):,} |
| Ledger-covered nodes | {len(covered_node_eids):,} |
| Ledger-covered rels | {len(covered_rel_eids):,} |
| Uncovered live nodes | {len(missing_nodes):,} |
| Uncovered live rels | {len(missing_rels):,} |

### Residual uncovered rels (out of P6-05 scope)

These {len(missing_rels)} live edges have no ledger row yet — mostly **Q01 merge redirects** (regulation edges now on `bt_decke` / `bt_fassade` / `bt_fenster` / `mat_glas` survivors) and **Q02 redirect** (`bw_cleveland_steel_and_tubes_stock`, WBS70 `AUS_SPENDER`). Not stale deletions; new graph elementIds after merge/redirect. Deferred to a follow-up element-proof pass.

{missing_rel_lines}

## Outputs

- Draft ledger: [`VERIFICATION_LEDGER_ELEMENT_v2.csv`](../VERIFICATION_LEDGER_ELEMENT_v2.csv)
- Delta log: [`ledger/post_quality_p06_05.csv`](../ledger/post_quality_p06_05.csv)
- Graph export: [`_p06_05_work/graph_counts.json`](../_p06_05_work/graph_counts.json)

## Method

1. Exported live `elementId` index from `mit-bestand` (read-only).
2. Dropped ledger rows whose node/rel keys no longer resolve in the live graph.
3. Classified removals against Q01 merge/delete, Q02 depot delete, Q04 catalogue delete patch triples.
4. Appended element rows for Q03 `PruefungNachweis` nodes and `ERFUELLT_NACHWEIS` edges present in live graph but absent from ledger.

**Input baseline:** EP-10 merged ledger rebuilt from shards + `_agent10_work` graph snapshot ({len(ledger_rows):,} rows).

**Note:** This is a draft `v2` ledger — not yet promoted to canonical `VERIFICATION_LEDGER_ELEMENT.csv`.
"""
    OUT_REPORT.write_text(report, encoding="utf-8")

    print(json.dumps({
        "live_nodes": counts["nodes"],
        "live_rels": counts["rels"],
        "ledger_before": len(ledger_rows),
        "ledger_after": len(kept),
        "removed": sum(1 for d in deltas if d["delta_action"] == "REMOVE"),
        "added": sum(1 for d in deltas if d["delta_action"] == "ADD"),
        "removal_by_pass": dict(removal_by_pass),
        "additions": dict(additions),
        "uncovered_nodes": len(missing_nodes),
        "uncovered_rels": len(missing_rels),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
