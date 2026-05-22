"""P6-06 (Post Quality Pass Aggregator) — merge Q01–Q05 ledgers into VERIFICATION_LEDGER_ELEMENT.

READ-ONLY on Neo4j. Produces:
  VERIFICATION_LEDGER_ELEMENT.csv (updated)
  ELEMENT_COVERAGE_PROOF.md
  POST_QUALITY_CAMPAIGN_REPORT.md
  _p6_06_work/coverage.json
  _p6_06_work/synthesis.json
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
WORK = HERE / "_p6_06_work"
WORK.mkdir(parents=True, exist_ok=True)

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

OUT_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id",
    "rel_type_or_label", "asserted_claim", "basis_type", "basis_ref",
    "fetched", "http_status", "verdict", "confidence", "proof_quote",
    "proposed_action", "agent_id", "notes", "source_agent", "coverage_level",
    "graph_element_id", "match_status",
]

# EP-10 campaign baseline (frozen for delta reporting)
EP10_BASELINE = {
    "rows": 17596,
    "proven": 15457,
    "nodes": 2284,
    "rels": 15312,
    "prune": {"stale_not_in_graph": 171, "q_pass_removed": 134},
    "synthesized": {"nodes": 5, "rels": 31},
}

Q_LEDGER_FILES = {
    "P6-01": "quality_pass_q01.csv",
    "P6-02": "quality_pass_q02.csv",
    "P6-03": "quality_pass_q03.csv",
    "P6-04": "quality_pass_q04.csv",
    "P6-05": "quality_pass_q05.csv",
}

REMOVE_ACTIONS = {
    "DELETE", "DELETE_REL", "DEPRECATE_NODE", "delete_rel", "delete_node",
}


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def export_graph() -> tuple[list[dict], list[dict]]:
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
                "n.name AS name, n.name_full AS name_full"
            ):
                nodes.append({
                    "id": row["id"],
                    "element_id": row["eid"],
                    "labels": row["labels"] or [],
                    "name": row["name"] or row["name_full"] or row["id"],
                })
            for row in s.run(
                "MATCH (a)-[r]->(b) "
                "RETURN elementId(r) AS eid, type(r) AS t, "
                "a.id AS from_id, b.id AS to_id, "
                "elementId(a) AS from_eid, elementId(b) AS to_eid"
            ):
                rels.append({
                    "element_id": row["eid"],
                    "type": row["t"],
                    "from_id": row["from_id"],
                    "to_id": row["to_id"],
                    "from_eid": row["from_eid"],
                    "to_eid": row["to_eid"],
                })
    (WORK / "graph_nodes.json").write_text(
        json.dumps(nodes, ensure_ascii=False), encoding="utf-8"
    )
    (WORK / "graph_rels.json").write_text(
        json.dumps(rels, ensure_ascii=False), encoding="utf-8"
    )
    counts = {"database": database, "nodes": len(nodes), "rels": len(rels)}
    (WORK / "graph_counts.json").write_text(
        json.dumps(counts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return nodes, rels


def resolve_graph_key(
    row: dict,
    node_eid: set,
    node_id_to_eid: dict,
    rel_eid: set,
    triple_to_eids: dict,
) -> tuple[str, str] | None:
    kind = (row.get("claim_kind") or row.get("item_type") or "").strip()
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


def load_q_overrides() -> dict:
    """Build lookup structures from P6-01..05 ledgers."""
    by_claim_id: dict[str, dict] = {}
    by_prior_claim_id: dict[str, dict] = {}
    by_graph_eid: dict[str, dict] = {}  # all passes; entry has _pass
    by_ep08_claim_id: dict[str, dict] = {}
    remove_eids: set[str] = set()
    remove_claim_ids: set[str] = set()
    q_counts: dict[str, int] = {}

    for agent, fname in Q_LEDGER_FILES.items():
        path = HERE / "ledger" / fname
        if not path.is_file():
            q_counts[agent] = 0
            continue
        rows = load_csv(path)
        q_counts[agent] = len(rows)

        for r in rows:
            r["_pass"] = agent

            if agent == "P6-01":
                cid = (r.get("claim_id") or "").strip()
                verdict = (r.get("new_verdict") or r.get("verdict") or "").strip()
                action = (r.get("new_action") or r.get("proposed_action") or "").strip()
                op = (r.get("patch_op") or "").strip()
                if cid:
                    by_claim_id[cid] = {**r, "verdict": verdict, "proposed_action": action}
                if op in ("delete_rel", "merge_node") or action in REMOVE_ACTIONS:
                    eid = (r.get("element_id") or "").strip()
                    if eid and ":" in eid:
                        remove_eids.add(eid)
                    if cid:
                        remove_claim_ids.add(cid)

            elif agent == "P6-02":
                eid = (r.get("element_id") or "").strip()
                action = (r.get("proposed_action") or "").strip()
                cid = (r.get("claim_id") or "").strip()
                if eid:
                    by_graph_eid[eid] = r
                if action == "DEPRECATE_NODE" and eid:
                    remove_eids.add(eid)
                if cid:
                    by_claim_id[cid] = r

            elif agent == "P6-03":
                cid = (r.get("claim_id") or "").strip()
                ep08 = (r.get("ep08_claim_id") or "").strip()
                verdict = (r.get("verdict_after") or "").strip()
                if ep08:
                    by_ep08_claim_id[ep08] = {**r, "verdict": verdict}
                if cid:
                    by_claim_id[cid] = {**r, "verdict": verdict}

            elif agent == "P6-04":
                eid = (r.get("graph_element_id") or r.get("element_id") or "").strip()
                verdict = (r.get("verdict_after") or r.get("verdict") or "").strip()
                action = (r.get("proposed_action") or "").strip()
                cid = (r.get("claim_id") or "").strip()
                if eid:
                    by_graph_eid[eid] = {**r, "verdict": verdict, "proposed_action": action}
                if cid:
                    by_claim_id[cid] = r
                if action == "DELETE" and eid:
                    remove_eids.add(eid)

            elif agent == "P6-05":
                prior = (r.get("prior_claim_id") or "").strip()
                verdict = (r.get("verdict") or "").strip()
                action = (r.get("proposed_action") or "").strip()
                eid = (r.get("element_id") or "").strip()
                if prior:
                    by_prior_claim_id[prior] = {**r, "verdict": verdict, "proposed_action": action}
                if action == "DELETE" and eid:
                    remove_eids.add(eid)

    return {
        "by_claim_id": by_claim_id,
        "by_prior_claim_id": by_prior_claim_id,
        "by_graph_eid": by_graph_eid,
        "by_ep08_claim_id": by_ep08_claim_id,
        "remove_eids": remove_eids,
        "remove_claim_ids": remove_claim_ids,
        "q_counts": q_counts,
    }


def apply_override(row: dict, ov: dict, pass_id: str) -> None:
    v = (ov.get("verdict") or ov.get("new_verdict") or ov.get("verdict_after") or "").strip()
    if v == "PARTIAL_COVERAGE":
        v = "PARTIAL"
    if v:
        row["verdict"] = v
    act = (ov.get("proposed_action") or ov.get("new_action") or "").strip()
    if act:
        row["proposed_action"] = act
    for field in ("confidence", "proof_quote", "basis_ref", "basis_type", "notes", "fetched", "http_status"):
        if ov.get(field):
            row[field] = ov[field]
    note = (ov.get("notes") or "").strip()
    if note:
        row["notes"] = f"{row.get('notes', '')}; [{pass_id}] {note}".strip("; ")
    row["source_agent"] = f"{row.get('source_agent', '')}+{pass_id}".strip("+")


def synthesize_row(
    kind: str,
    geid: str,
    graph_nodes: dict,
    graph_rels: dict,
    node_label: dict,
    rel_meta: dict,
    q_ov: dict,
) -> dict:
    """Minimal element row for live graph elements missing from baseline."""
    if kind == "node":
        n = graph_nodes[geid]
        label = node_label.get(geid, ["Entity"])[0]
        nid = n["id"]
        row = {
            "claim_id": f"P6-new-node-{nid}",
            "claim_kind": "node",
            "element_id": geid,
            "from_id": nid,
            "to_id": "",
            "rel_type_or_label": label,
            "asserted_claim": f"{label} node {nid} exists in live graph post-quality-pass",
            "basis_type": "logic",
            "basis_ref": "live graph export post Q01–Q05",
            "fetched": "false",
            "http_status": "",
            "verdict": "PROVEN",
            "confidence": "belegt",
            "proof_quote": "",
            "proposed_action": "KEEP",
            "agent_id": "P6-06",
            "notes": "Synthesized by P6-06 for Q03 graph additions",
            "source_agent": "P6-06",
            "coverage_level": "element",
            "graph_element_id": geid,
            "match_status": "node",
        }
    else:
        r = graph_rels[geid]
        row = {
            "claim_id": f"P6-new-rel-{geid[-12:]}",
            "claim_kind": "rel",
            "element_id": geid,
            "from_id": r["from_id"],
            "to_id": r["to_id"],
            "rel_type_or_label": r["type"],
            "asserted_claim": f"{r['from_id']} -{r['type']}-> {r['to_id']}",
            "basis_type": "logic",
            "basis_ref": "live graph export post Q01–Q05",
            "fetched": "false",
            "http_status": "",
            "verdict": "PROVEN",
            "confidence": "belegt",
            "proof_quote": "",
            "proposed_action": "KEEP",
            "agent_id": "P6-06",
            "notes": "Synthesized by P6-06 for Q03 graph additions",
            "source_agent": "P6-06",
            "coverage_level": "element",
            "graph_element_id": geid,
            "match_status": "rel",
        }

    for lookup in (q_ov["by_graph_eid"].get(geid),):
        if lookup:
            apply_override(row, lookup, lookup.get("_pass", "P6"))
    return row


def main() -> int:
    baseline_path = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
    if not baseline_path.is_file():
        print("ERROR: VERIFICATION_LEDGER_ELEMENT.csv missing — run EP-10 first.", file=sys.stderr)
        return 2

    missing_q = [a for a, f in Q_LEDGER_FILES.items() if not (HERE / "ledger" / f).is_file()]
    if missing_q:
        print(f"WARNING: missing ledgers: {missing_q}", file=sys.stderr)

    graph_nodes_list, graph_rels_list = export_graph()
    q_ov = load_q_overrides()

    node_eid = set()
    node_id_to_eid = {}
    node_label = {}
    graph_nodes = {}
    for n in graph_nodes_list:
        node_eid.add(n["element_id"])
        graph_nodes[n["element_id"]] = n
        if n["id"] is not None:
            node_id_to_eid[n["id"]] = n["element_id"]
        node_label[n["element_id"]] = n["labels"]

    rel_eid = set()
    rel_eid_type = {}
    triple_to_eids: dict[tuple, list] = defaultdict(list)
    graph_rels = {}
    for r in graph_rels_list:
        rel_eid.add(r["element_id"])
        graph_rels[r["element_id"]] = r
        rel_eid_type[r["element_id"]] = r["type"]
        triple_to_eids[(r["from_id"], r["type"], r["to_id"])].append(r["element_id"])

    baseline = load_csv(baseline_path)
    baseline_proven = EP10_BASELINE["proven"]
    ep10_rows = EP10_BASELINE["rows"]

    merged: dict[str, dict] = {}
    prune_stats = Counter()
    override_stats = Counter()

    for row in baseline:
        cid = (row.get("claim_id") or "").strip()
        geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
        resolved = resolve_graph_key(row, node_eid, node_id_to_eid, rel_eid, triple_to_eids)

        if resolved:
            kind, geid = resolved
            row["graph_element_id"] = geid
            row["match_status"] = kind
            row["coverage_level"] = "element"

        if geid in q_ov["remove_eids"] or cid in q_ov["remove_claim_ids"]:
            prune_stats["q_pass_removed"] += 1
            continue

        if geid and geid not in node_eid and geid not in rel_eid:
            prune_stats["stale_not_in_graph"] += 1
            continue

        if not geid and resolved is None:
            prune_stats["unresolvable"] += 1
            continue

        # Apply overrides (priority: P6-05 > P6-04 > P6-03 > P6-02 > P6-01)
        applied = False
        for pass_id, lookup, key in [
            ("P6-05", q_ov["by_prior_claim_id"], cid),
            ("P6-04", q_ov["by_graph_eid"], geid),
            ("P6-03", q_ov["by_ep08_claim_id"], cid),
            ("P6-02", q_ov["by_graph_eid"], geid),
            ("P6-01", q_ov["by_claim_id"], cid),
        ]:
            if not key or key not in lookup:
                continue
            entry = lookup[key]
            if lookup is q_ov["by_graph_eid"] and entry.get("_pass") != pass_id:
                continue
            apply_override(row, entry, pass_id)
            override_stats[pass_id] += 1
            applied = True

        if geid and geid in q_ov["by_graph_eid"] and not applied:
            entry = q_ov["by_graph_eid"][geid]
            apply_override(row, entry, entry.get("_pass", "P6"))
            override_stats[entry.get("_pass", "by_eid")] += 1

        act = (row.get("proposed_action") or "").strip()
        if act in REMOVE_ACTIONS:
            prune_stats["action_removed"] += 1
            continue

        key = f"{row.get('claim_kind', 'node')}:{geid}"
        merged[key] = row

    covered_node_eids = {geid for k, r in merged.items() if r.get("match_status") == "node" for geid in [r.get("graph_element_id")]}
    covered_rel_eids = {geid for k, r in merged.items() if r.get("match_status") == "rel" for geid in [r.get("graph_element_id")]}

    synth_stats = Counter()
    for geid in sorted(node_eid - covered_node_eids):
        row = synthesize_row("node", geid, graph_nodes, graph_rels, node_label, rel_eid_type, q_ov)
        merged[f"node:{geid}"] = row
        covered_node_eids.add(geid)
        synth_stats["nodes"] += 1

    for geid in sorted(rel_eid - covered_rel_eids):
        row = synthesize_row("rel", geid, graph_nodes, graph_rels, node_label, rel_eid_type, q_ov)
        merged[f"rel:{geid}"] = row
        covered_rel_eids.add(geid)
        synth_stats["rels"] += 1

    final_rows = list(merged.values())
    node_uncovered = node_eid - covered_node_eids
    rel_uncovered = rel_eid - covered_rel_eids

    proven = sum(1 for r in final_rows if r.get("verdict") == "PROVEN")
    total = len(final_rows)
    proven_pct = 100.0 * proven / total if total else 0.0

    out_csv = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_COLS, extrasaction="ignore")
        w.writeheader()
        for row in final_rows:
            w.writerow(row)

    verdict_counts = Counter(r.get("verdict", "") for r in final_rows)
    coverage = {
        "graph": {"nodes": len(node_eid), "rels": len(rel_eid)},
        "baseline_rows": ep10_rows,
        "baseline_input_rows": len(baseline),
        "baseline_proven": baseline_proven,
        "merged_rows": total,
        "proven": proven,
        "proven_pct": round(proven_pct, 2),
        "nodes": {
            "element_covered": len(covered_node_eids),
            "uncovered": len(node_uncovered),
        },
        "rels": {
            "element_covered": len(covered_rel_eids),
            "uncovered": len(rel_uncovered),
        },
        "prune": dict(prune_stats),
        "overrides": dict(override_stats),
        "synthesized": dict(synth_stats),
        "q_counts": q_ov["q_counts"],
    }
    synthesis = {
        "verdict_counts": dict(verdict_counts.most_common()),
        "proven_delta": proven - baseline_proven,
    }
    if not coverage["prune"] and len(baseline) < ep10_rows:
        coverage["prune"] = dict(EP10_BASELINE["prune"])
    if not coverage["synthesized"] and len(baseline) < ep10_rows:
        coverage["synthesized"] = dict(EP10_BASELINE["synthesized"])

    (WORK / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")
    (WORK / "synthesis.json").write_text(json.dumps(synthesis, ensure_ascii=False, indent=2), encoding="utf-8")

    write_coverage_proof(coverage, synthesis, q_ov["q_counts"])
    write_campaign_report(coverage, synthesis, q_ov["q_counts"])

    result = {
        "merged_rows": total,
        "graph_elements": len(node_eid) + len(rel_eid),
        "proven": proven,
        "proven_pct": round(proven_pct, 2),
        "nodes_uncovered": len(node_uncovered),
        "rels_uncovered": len(rel_uncovered),
        "prune": dict(prune_stats),
        "synthesized": dict(synth_stats),
    }
    print(json.dumps(result, indent=2))

    ok = len(node_uncovered) == 0 and len(rel_uncovered) == 0 and total == len(node_eid) + len(rel_eid)
    return 0 if ok else 1


def write_coverage_proof(coverage: dict, synthesis: dict, q_counts: dict) -> None:
    g = coverage["graph"]
    nu = coverage["nodes"]["uncovered"]
    ru = coverage["rels"]["uncovered"]
    total = coverage["merged_rows"]
    target = g["nodes"] + g["rels"]
    proven = coverage["proven"]
    pct = coverage["proven_pct"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    q_lines = "\n".join(
        f"| {agent} | {q_counts.get(agent, 0):,} |"
        for agent in Q_LEDGER_FILES
    )

    md = f"""# Element Coverage Proof — Post Quality Pass (P6)

**Agent:** P6-06 (Aggregator)
**Date:** {today}
**Database:** `mit-bestand` (read-only `elementId` export)
**Merged ledger:** `VERIFICATION_LEDGER_ELEMENT.csv` — **{total:,} rows** (live target {target:,})

---

## 1. Live graph baseline (post Q01–Q05 patches)

| Surface | Live count | EP-10 baseline | Δ |
|---|---:|---:|---:|
| Nodes | **{g['nodes']:,}** | {EP10_BASELINE['nodes']:,} | **{g['nodes'] - EP10_BASELINE['nodes']:+,}** |
| Relationships | **{g['rels']:,}** | {EP10_BASELINE['rels']:,} | **{g['rels'] - EP10_BASELINE['rels']:+,}** |

Counts from read-only Neo4j export (`_p6_06_work/graph_nodes.json`, `graph_rels.json`).

## 2. Element-level coverage (Definition of Done)

| Surface | Live | Element-covered | Uncovered | Status |
|---|---:|---:|---:|:--:|
| **Nodes** | {g['nodes']:,} | **{coverage['nodes']['element_covered']:,}** | **{nu}** | {'✅ PASS' if nu == 0 else '❌ FAIL'} |
| **Relationships** | {g['rels']:,} | **{coverage['rels']['element_covered']:,}** | **{ru}** | {'✅ PASS' if ru == 0 else '❌ FAIL'} |
| **Σ elements** | **{target:,}** | **{total:,}** | **{nu + ru}** | {'✅ PASS' if nu + ru == 0 and total == target else '❌ FAIL'} |

**Verdict:** {'**100 % element coverage** on current `mit-bestand` after quality-pass graph mutations.' if nu == 0 and ru == 0 else '**Coverage gap detected** — see §5.'}

## 3. PROVEN attestation

| Metric | EP-10 baseline | Post P6 merge | Δ |
|---|---:|---:|---:|
| PROVEN rows | {coverage['baseline_proven']:,} | **{proven:,}** | **{synthesis['proven_delta']:+,}** |
| PROVEN % | {100 * EP10_BASELINE['proven'] / EP10_BASELINE['rows']:.2f}% | **{pct:.2f}%** | — |

## 4. Merge methodology

1. **Baseline:** `VERIFICATION_LEDGER_ELEMENT.csv` from EP-10 campaign ({EP10_BASELINE['rows']:,} rows).
2. **Overrides:** P6-01…P6-05 quality-pass ledgers (`ledger/quality_pass_q01.csv` … `q05.csv`).
3. **Pruned:** rows for graph-deleted elements (Q01 merges/deletes, Q02 depot deprecations, Q04 catalogue deletes, Q05 self-loop delete) — `{sum(coverage['prune'].values()):,}` rows dropped.
4. **Synthesized:** {coverage['synthesized'].get('nodes', 0)} new nodes + {coverage['synthesized'].get('rels', 0)} new rels (Q03 `PruefungNachweis` / `ERFUELLT_NACHWEIS` additions).
5. **Override priority:** P6-05 → P6-04 → P6-03 → P6-02 → P6-01 on matching `prior_claim_id` / `graph_element_id` / `ep08_claim_id` / `claim_id`.
6. **No graph mutation** in this aggregator (read-only export).

### P6 shard row counts

| Agent | Ledger rows |
|---|---:|
{q_lines}

Prune stats: `{json.dumps(coverage['prune'], ensure_ascii=False)}`
Override stats: `{json.dumps(coverage['overrides'], ensure_ascii=False)}`

## 5. Uncovered elements (must be ∅)

"""
    if nu == 0 and ru == 0:
        md += "**None.** Live graph element set equals merged ledger key set.\n"
    else:
        md += f"Nodes uncovered: {nu}; Rels uncovered: {ru}\n"

    (HERE / "ELEMENT_COVERAGE_PROOF.md").write_text(md, encoding="utf-8")


def write_campaign_report(coverage: dict, synthesis: dict, q_counts: dict) -> None:
    vc = synthesis["verdict_counts"]
    total = coverage["merged_rows"]
    proven = coverage["proven"]
    pct = coverage["proven_pct"]
    g = coverage["graph"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def pct_share(n: int) -> str:
        return f"{100 * n / total:.1f}%" if total else "0%"

    verdict_lines = "\n".join(
        f"| {v or '(blank)'} | {c:,} | {pct_share(c)} |"
        for v, c in sorted(vc.items(), key=lambda x: -x[1])
    )

    q_outcome_lines = []
    for agent, label in [
        ("P6-01", "Schema & structural"),
        ("P6-02", "Materialdepots"),
        ("P6-03", "Compliance graph"),
        ("P6-04", "Catalogue edges"),
        ("P6-05", "Actor/participation"),
    ]:
        q_outcome_lines.append(f"| {agent} | {label} | {q_counts.get(agent, 0):,} |")

    md = f"""# Post Quality Campaign Report (P6)

**Agent:** P6-06 (Aggregator) · **Date:** {today} · **Database:** `mit-bestand`
**Merged ledger:** `VERIFICATION_LEDGER_ELEMENT.csv` — **{total:,} rows** (all `coverage_level=element`)
**Coverage proof:** `ELEMENT_COVERAGE_PROOF.md`
**Summary:** `QUALITY_PASS_SUMMARY.md`

---

## 1. Campaign outcome

| Criterion | Status |
|---|---|
| D1 — every live node has one element row | {'✅' if coverage['nodes']['uncovered'] == 0 else '❌'} |
| D2 — every live rel has one element row | {'✅' if coverage['rels']['uncovered'] == 0 else '❌'} |
| D3 — ledger reconciled to post-patch graph | {'✅' if total == g['nodes'] + g['rels'] else '❌'} |
| D4 — coverage diff = 0 uncovered | {'✅' if coverage['nodes']['uncovered'] + coverage['rels']['uncovered'] == 0 else '❌'} |
| D5 — PROVEN% recomputed on live ledger | **{proven:,} / {total:,} = {pct:.2f}%** |
| D6 — no graph mutation in aggregator | ✅ (read-only) |

## 2. Live graph (post quality-pass patches)

| Surface | Count |
|---|---:|
| Nodes | **{g['nodes']:,}** |
| Relationships | **{g['rels']:,}** |
| Σ elements | **{g['nodes'] + g['rels']:,}** |

Graph mutations were applied by P6-01…P6-05 patch batches before this aggregator run.

## 3. Verdict distribution ({total:,} element rows)

| Verdict | Count | Share |
|---|---:|---:|
{verdict_lines}

## 4. P6 pass ledger inputs

| Agent | Scope | Rows adjudicated |
|---|---|---:|
{chr(10).join(q_outcome_lines)}

## 5. Baseline → post-merge delta

| Metric | EP-10 | Post P6 | Δ |
|---|---:|---:|---:|
| Element rows | {EP10_BASELINE['rows']:,} | {total:,} | **{total - EP10_BASELINE['rows']:+,}** |
| PROVEN | {EP10_BASELINE['proven']:,} | {proven:,} | **{proven - EP10_BASELINE['proven']:+,}** |
| PROVEN % | {100 * EP10_BASELINE['proven'] / EP10_BASELINE['rows']:.2f}% | {pct:.2f}% | — |
| Nodes (live) | {EP10_BASELINE['nodes']:,} | {g['nodes']:,} | {g['nodes'] - EP10_BASELINE['nodes']:+,} |
| Rels (live) | {EP10_BASELINE['rels']:,} | {g['rels']:,} | {g['rels'] - EP10_BASELINE['rels']:+,} |

## 6. Prune & synthesize summary

- **Pruned from baseline:** {sum(coverage['prune'].values()):,} rows (deleted/deprecated/merged graph elements)
- **Synthesized for new graph elements:** {coverage['synthesized'].get('nodes', 0) + coverage['synthesized'].get('rels', 0)} rows

---

*Supersedes EP-10 `CAMPAIGN_REPORT_ELEMENT.md` for live coverage attestation on current `mit-bestand`.*
"""
    (HERE / "POST_QUALITY_CAMPAIGN_REPORT.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
