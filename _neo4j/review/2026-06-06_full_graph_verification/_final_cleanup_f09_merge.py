"""F09 — Final Cleanup ledger re-merge (plan F4).

READ-ONLY Neo4j. Waits for ledger/final_cleanup_f01..f08.csv, merges into
VERIFICATION_LEDGER_ELEMENT.csv, prunes rau_architects stale keys.

Outputs:
  VERIFICATION_LEDGER_ELEMENT.csv (updated)
  ledger/final_cleanup_f09.csv (merge log)
  reports/final_cleanup_f09.md
  _f09_work/coverage.json
"""

from __future__ import annotations

import csv
import json
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

csv.field_size_limit(10_000_000)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
LEDGER = HERE / "ledger"
REPORTS = HERE / "reports"
WORK = HERE / "_f09_work"
WORK.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

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

# Load low→high so later passes win in by_graph_eid lookups.
F_LEDGER_FILES = [
    ("F01", "final_cleanup_f01.csv"),
    ("F02", "final_cleanup_f02.csv"),
    ("F03", "final_cleanup_f03.csv"),
    ("F04", "final_cleanup_f04.csv"),
    ("F05", "final_cleanup_f05.csv"),
    ("F08", "final_cleanup_f08.csv"),
]

P6_LEDGER_FILES = [
    ("P6-05", "post_quality_p06_05.csv"),
    ("P6-04", "post_quality_p06_04.csv"),
    ("P6-03", "post_quality_p06_03.csv"),
    ("P6-02", "post_quality_p06_02.csv"),
    ("P6-01", "post_quality_p06_01.csv"),
]

NON_ELEMENT_F = {"F06", "F07"}

REMOVE_ACTIONS = {
    "DELETE", "DELETE_REL", "DEPRECATE_NODE", "delete_rel", "delete_node",
    "MERGE_DUPLICATE", "PRUNE", "F4_PRUNE",
}

VALID_VERDICTS = {
    "PROVEN", "PARTIAL", "UNVERIFIABLE", "MISSING_EVIDENCE", "SCHEMA_VIOLATION",
    "CONTRADICTION", "UNSUPPORTED", "REMEDIATED", "PARTIAL_COVERAGE",
}

POLL_INTERVAL_SEC = 60
POLL_MAX_SEC = 30 * 60

P6_BASELINE = {"rows": 17327, "proven": 15468, "proven_pct": 89.27}


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def wait_for_f_ledgers() -> None:
    required = [LEDGER / fname for _, fname in F_LEDGER_FILES] + [
        LEDGER / "final_cleanup_f06.csv",
        LEDGER / "final_cleanup_f07.csv",
    ]
    deadline = time.time() + POLL_MAX_SEC
    while time.time() < deadline:
        missing = [p.name for p in required if not p.is_file()]
        if not missing:
            print("All F01–F08 ledgers present.")
            return
        print(f"Waiting for {len(missing)} ledgers: {', '.join(missing)}")
        time.sleep(POLL_INTERVAL_SEC)
    missing = [p.name for p in required if not p.is_file()]
    raise RuntimeError(f"Timeout after {POLL_MAX_SEC}s — still missing: {missing}")


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
                "a.id AS from_id, b.id AS to_id"
            ):
                rels.append({
                    "element_id": row["eid"],
                    "type": row["t"],
                    "from_id": row["from_id"],
                    "to_id": row["to_id"],
                })
            counts = s.run(
                "MATCH (n) WITH count(n) AS nodes "
                "MATCH ()-[r]->() RETURN nodes, count(r) AS rels, "
                "nodes + count(r) AS elements"
            ).single()
    counts_dict = {
        "database": database,
        "nodes": counts["nodes"],
        "rels": counts["rels"],
        "elements": counts["elements"],
    }
    (WORK / "graph_nodes.json").write_text(
        json.dumps(nodes, ensure_ascii=False), encoding="utf-8"
    )
    (WORK / "graph_rels.json").write_text(
        json.dumps(rels, ensure_ascii=False), encoding="utf-8"
    )
    (WORK / "graph_counts.json").write_text(
        json.dumps(counts_dict, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return nodes, rels, counts_dict


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


def is_element_row(row: dict) -> bool:
    cov = (row.get("coverage_level") or "").strip()
    if cov and cov != "element":
        return False
    kind = (row.get("claim_kind") or row.get("item_type") or "").strip()
    if kind in ("node", "rel"):
        return True
    geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
    return bool(geid and ":" in geid)


def normalize_f_row(row: dict) -> dict:
    """Repair F04 node rows with an extra empty CSV column before label."""
    r = dict(row)
    label = (row.get("rel_type_or_label") or "").strip()
    claim = (row.get("asserted_claim") or "").strip()
    if not label and claim in ("Akteur", "Projekt", "Bauteilgruppe", "Materialdepot"):
        r["rel_type_or_label"] = claim
        r["asserted_claim"] = (row.get("basis_type") or "").strip()
        r["basis_type"] = (row.get("basis_ref") or "").strip()
        r["basis_ref"] = (row.get("fetched") or "").strip()
        r["fetched"] = (row.get("http_status") or "").strip()
        r["http_status"] = (row.get("verdict") or "").strip()
        r["verdict"] = (row.get("confidence") or "").strip()
        r["confidence"] = (row.get("proof_quote") or "").strip()
        r["proof_quote"] = (row.get("proposed_action") or "").strip()
        r["proposed_action"] = (row.get("agent_id") or "").strip()
        r["agent_id"] = (row.get("notes") or "").strip()
    return r


def apply_override(row: dict, ov: dict, pass_id: str) -> None:
    ov = normalize_f_row(ov) if ov.get("_pass", "").startswith("F") else ov
    v = (ov.get("verdict") or ov.get("new_verdict") or ov.get("verdict_after") or "").strip()
    if v == "PARTIAL_COVERAGE":
        v = "PARTIAL"
    if v and (v in VALID_VERDICTS or not v.isdigit()):
        row["verdict"] = v
    act = (ov.get("proposed_action") or ov.get("new_action") or "").strip()
    if act:
        row["proposed_action"] = act
    for field in ("confidence", "proof_quote", "basis_ref", "basis_type", "notes",
                  "fetched", "http_status", "asserted_claim", "claim_id"):
        val = ov.get(field)
        if val is not None and str(val).strip():
            row[field] = val
    note = (ov.get("notes") or "").strip()
    if note:
        prev = (row.get("notes") or "").strip()
        row["notes"] = f"{prev}; [{pass_id}] {note}".strip("; ")
    row["source_agent"] = f"{row.get('source_agent', '')}+{pass_id}".strip("+")


def load_f_overrides() -> dict:
    by_graph_eid: dict[str, dict] = {}
    by_claim_id: dict[str, dict] = {}
    by_prior_claim_id: dict[str, dict] = {}
    prune_eids: set[str] = set()
    prune_node_ids: set[str] = set()
    f_counts: dict[str, int] = {}
    f_element_counts: dict[str, int] = {}

    for agent, fname in F_LEDGER_FILES:
        path = LEDGER / fname
        rows = load_csv(path) if path.is_file() else []
        f_counts[agent] = len(rows)
        norm_rows = [
            normalize_f_row(raw) if agent in ("F02", "F03", "F04", "F05", "F08") else raw
            for raw in rows
        ]
        elem_rows = [r for r in norm_rows if is_element_row(r)]
        f_element_counts[agent] = len(elem_rows)

        for r in norm_rows:
            r["_pass"] = agent
            action = (r.get("proposed_action") or "").strip()
            geid = (r.get("graph_element_id") or r.get("element_id") or "").strip()
            cid = (r.get("claim_id") or "").strip()
            fid = (r.get("from_id") or "").strip()
            tid = (r.get("to_id") or "").strip()

            if agent == "F01":
                verdict = (r.get("verdict") or "").strip()
                if (
                    action in REMOVE_ACTIONS
                    or verdict == "STALE"
                    or cid.startswith("F01-PRUNE-")
                ):
                    if geid:
                        prune_eids.add(geid)
                    if fid == "rau_architects" or tid == "rau_architects":
                        if geid:
                            prune_eids.add(geid)
                prune_list = (r.get("prune_element_ids") or r.get("prune_eids") or "").strip()
                if prune_list:
                    for part in prune_list.replace(";", ",").split(","):
                        part = part.strip()
                        if part:
                            prune_eids.add(part)

            if not is_element_row(r):
                continue

            if action in REMOVE_ACTIONS and geid:
                prune_eids.add(geid)

            if geid:
                by_graph_eid[geid] = r
            if cid:
                by_claim_id[cid] = r
            prior = (r.get("prior_claim_id") or "").strip()
            if prior:
                by_prior_claim_id[prior] = r

    prune_node_ids.add("rau_architects")

    return {
        "by_graph_eid": by_graph_eid,
        "by_claim_id": by_claim_id,
        "by_prior_claim_id": by_prior_claim_id,
        "prune_eids": prune_eids,
        "prune_node_ids": prune_node_ids,
        "f_counts": f_counts,
        "f_element_counts": f_element_counts,
    }


def load_p6_overrides() -> dict:
    by_claim_id: dict[str, dict] = {}
    by_prior_claim_id: dict[str, dict] = {}
    by_graph_eid: dict[str, dict] = {}
    by_ep08_claim_id: dict[str, dict] = {}
    remove_eids: set[str] = set()
    remove_claim_ids: set[str] = set()
    p6_counts: dict[str, int] = {}

    for agent, fname in P6_LEDGER_FILES:
        path = LEDGER / fname
        if not path.is_file():
            p6_counts[agent] = 0
            continue
        rows = load_csv(path)
        p6_counts[agent] = len(rows)
        for r in rows:
            r["_pass"] = agent
            cid = (r.get("claim_id") or "").strip()
            eid = (r.get("graph_element_id") or r.get("element_id") or "").strip()
            action = (r.get("proposed_action") or r.get("new_action") or "").strip()
            if agent == "P6-05":
                prior = (r.get("prior_claim_id") or "").strip()
                if prior:
                    by_prior_claim_id[prior] = r
                if action == "DELETE" and eid:
                    remove_eids.add(eid)
            elif agent == "P6-04":
                if eid:
                    by_graph_eid[eid] = r
                if cid:
                    by_claim_id[cid] = r
                if action == "DELETE" and eid:
                    remove_eids.add(eid)
            elif agent == "P6-03":
                ep08 = (r.get("ep08_claim_id") or "").strip()
                if ep08:
                    by_ep08_claim_id[ep08] = r
                if cid:
                    by_claim_id[cid] = r
            elif agent == "P6-02":
                if eid:
                    by_graph_eid[eid] = r
                if action == "DEPRECATE_NODE" and eid:
                    remove_eids.add(eid)
            elif agent == "P6-01":
                if cid:
                    by_claim_id[cid] = r
                op = (r.get("patch_op") or "").strip()
                if op in ("delete_rel", "merge_node") or action in REMOVE_ACTIONS:
                    if eid and ":" in eid:
                        remove_eids.add(eid)
                    if cid:
                        remove_claim_ids.add(cid)

    return {
        "by_claim_id": by_claim_id,
        "by_prior_claim_id": by_prior_claim_id,
        "by_graph_eid": by_graph_eid,
        "by_ep08_claim_id": by_ep08_claim_id,
        "remove_eids": remove_eids,
        "remove_claim_ids": remove_claim_ids,
        "p6_counts": p6_counts,
    }


def should_prune_row(row: dict, geid: str, f_ov: dict) -> str | None:
    cid = (row.get("claim_id") or "").strip()
    fid = (row.get("from_id") or "").strip()
    tid = (row.get("to_id") or "").strip()
    if geid in f_ov["prune_eids"]:
        return "f01_prune_eid"
    if fid in f_ov["prune_node_ids"] or tid in f_ov["prune_node_ids"]:
        return "rau_architects_stale"
    if geid and geid not in f_ov["prune_eids"]:
        if fid == "rau_architects" or tid == "rau_architects":
            return "rau_architects_endpoint"
    return None


def synthesize_row(kind: str, geid: str, graph_nodes: dict, graph_rels: dict,
                   node_label: dict) -> dict:
    if kind == "node":
        n = graph_nodes[geid]
        label = node_label.get(geid, ["Entity"])[0]
        nid = n["id"]
        return {
            "claim_id": f"F09-new-node-{nid}",
            "claim_kind": "node",
            "element_id": geid,
            "from_id": nid,
            "to_id": "",
            "rel_type_or_label": label,
            "asserted_claim": f"{label} node {nid} exists in live graph post-F1",
            "basis_type": "logic",
            "basis_ref": "live graph export post final cleanup F1",
            "fetched": "false",
            "http_status": "",
            "verdict": "MISSING_EVIDENCE",
            "confidence": "",
            "proof_quote": "",
            "proposed_action": "KEEP",
            "agent_id": "F09",
            "notes": "Synthesized by F09 for uncovered live element",
            "source_agent": "F09",
            "coverage_level": "element",
            "graph_element_id": geid,
            "match_status": "node",
        }
    r = graph_rels[geid]
    return {
        "claim_id": f"F09-new-rel-{geid[-12:]}",
        "claim_kind": "rel",
        "element_id": geid,
        "from_id": r["from_id"],
        "to_id": r["to_id"],
        "rel_type_or_label": r["type"],
        "asserted_claim": f"{r['from_id']} -{r['type']}-> {r['to_id']}",
        "basis_type": "logic",
        "basis_ref": "live graph export post final cleanup F1",
        "fetched": "false",
        "http_status": "",
        "verdict": "MISSING_EVIDENCE",
        "confidence": "",
        "proof_quote": "",
        "proposed_action": "KEEP",
        "agent_id": "F09",
        "notes": "Synthesized by F09 for uncovered live element",
        "source_agent": "F09",
        "coverage_level": "element",
        "graph_element_id": geid,
        "match_status": "rel",
    }


def write_merge_log(merge_log: list[dict]) -> None:
    log_cols = [
        "log_id", "action", "graph_element_id", "claim_id", "source_pass",
        "prior_verdict", "new_verdict", "reason",
    ]
    with (LEDGER / "final_cleanup_f09.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=log_cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(merge_log)


def write_report(
    counts: dict,
    prune_stats: Counter,
    override_stats: Counter,
    synth_stats: Counter,
    verdict_hist: Counter,
    final_rows: list[dict],
    f_ov: dict,
    merge_log: list[dict],
) -> None:
    proven = verdict_hist.get("PROVEN", 0)
    total = len(final_rows)
    proven_pct = 100.0 * proven / total if total else 0.0
    delta_proven = proven - P6_BASELINE["proven"]
    delta_pct = proven_pct - P6_BASELINE["proven_pct"]

    md = f"""# Final Cleanup F09 — Ledger Re-merge Report

**Agent:** F09 (plan F4)  
**Date:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}  
**Database:** `{counts.get("database", "mit-bestand")}`  
**Mode:** READ-ONLY Neo4j

## Headline

| Metric | P6-06 baseline | Post-F09 merge | Δ |
|---|---:|---:|---:|
| Live nodes | 2,264 | **{counts["nodes"]:,}** | {counts["nodes"] - 2264:+,} |
| Live rels | 15,063 | **{counts["rels"]:,}** | {counts["rels"] - 15063:+,} |
| Element rows | {P6_BASELINE["rows"]:,} | **{total:,}** | {total - P6_BASELINE["rows"]:+,} |
| PROVEN | {P6_BASELINE["proven"]:,} ({P6_BASELINE["proven_pct"]:.2f}%) | **{proven:,}** ({proven_pct:.2f}%) | {delta_proven:+,} ({delta_pct:+.2f}pp) |

**Plan target (pre-merge):** 17,326 (= 2,263 nodes + 15,063 rels). **Live at merge:** {counts['elements']:,} (= {counts['nodes']:,} + {counts['rels']:,}; F1 merge deduped 3 rels). **Ledger:** {total:,} ({'PASS' if total == counts['elements'] else 'CHECK'}).

## Input ledgers

| Agent | Total rows | Element overrides |
|---|---:|---:|
"""
    for agent in ["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08"]:
        agent_rows = f_ov["f_counts"].get(agent, 0)
        if agent in ("F06", "F07") and agent_rows == 0:
            p = LEDGER / f"final_cleanup_{agent.lower()}.csv"
            if p.is_file():
                agent_rows = len(load_csv(p))
        elem = f_ov["f_element_counts"].get(agent, 0)
        md += f"| {agent} | {agent_rows:,} | {elem:,} |\n"

    md += f"""
## Prune tallies

| Reason | Count |
|---|---:|
"""
    if prune_stats:
        for reason, n in sorted(prune_stats.items()):
            md += f"| {reason} | {n:,} |\n"
    else:
        md += "| (none this pass — baseline already post-F1 pruned) | 0 |\n"

    md += f"""
## Override tallies

| Pass | Count |
|---|---:|
"""
    for pass_id, n in sorted(override_stats.items()):
        md += f"| {pass_id} | {n:,} |\n"

    md += f"""
## Synthesize tallies

| Kind | Count |
|---|---:|
| nodes | {synth_stats.get("nodes", 0):,} |
| rels | {synth_stats.get("rels", 0):,} |

## Verdict histogram

| Verdict | Count | Share |
|---|---:|---:|
"""
    for v, n in verdict_hist.most_common():
        md += f"| {v} | {n:,} | {100.0 * n / total:.2f}% |\n"

    empty_quote_proven = sum(
        1 for r in final_rows
        if r.get("verdict") in ("PROVEN", "PARTIAL") and not (r.get("proof_quote") or "").strip()
    )
    md += f"""
## Evidence Gate spot-check

- PROVEN/PARTIAL with empty `proof_quote`: **{empty_quote_proven}** (target 0 after F08)
- `rau_architects` stale keys pruned: **{prune_stats.get("rau_architects_stale", 0) + prune_stats.get("rau_architects_endpoint", 0) + prune_stats.get("f01_prune_eid", 0)}**
- Merge log rows: **{len(merge_log):,}** → `ledger/final_cleanup_f09.csv`

## Outputs

- `VERIFICATION_LEDGER_ELEMENT.csv` — canonical element ledger ({total:,} rows)
- `ledger/final_cleanup_f09.csv` — merge audit log
- `_f09_work/coverage.json` — machine-readable coverage proof inputs for F10
"""
    (REPORTS / "final_cleanup_f09.md").write_text(md, encoding="utf-8")


def main() -> int:
    if "--no-wait" not in sys.argv:
        wait_for_f_ledgers()

    baseline_path = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
    if not baseline_path.is_file():
        print("ERROR: VERIFICATION_LEDGER_ELEMENT.csv missing.", file=sys.stderr)
        return 2

    graph_nodes_list, graph_rels_list, counts = export_graph()
    f_ov = load_f_overrides()
    p6_ov = load_p6_overrides()

    node_eid: set[str] = set()
    node_id_to_eid: dict[str, str] = {}
    node_label: dict[str, list] = {}
    graph_nodes: dict[str, dict] = {}
    for n in graph_nodes_list:
        node_eid.add(n["element_id"])
        graph_nodes[n["element_id"]] = n
        if n["id"] is not None:
            node_id_to_eid[n["id"]] = n["element_id"]
        node_label[n["element_id"]] = n["labels"]

    rel_eid: set[str] = set()
    triple_to_eids: dict[tuple, list] = defaultdict(list)
    graph_rels: dict[str, dict] = {}
    for r in graph_rels_list:
        rel_eid.add(r["element_id"])
        graph_rels[r["element_id"]] = r
        triple_to_eids[(r["from_id"], r["type"], r["to_id"])].append(r["element_id"])

    baseline = load_csv(baseline_path)
    merged: dict[str, dict] = {}
    prune_stats: Counter = Counter()
    override_stats: Counter = Counter()
    merge_log: list[dict] = []
    log_i = 0

    def log(action: str, row: dict | None, source: str, reason: str,
            prior_v: str = "", new_v: str = "") -> None:
        nonlocal log_i
        log_i += 1
        merge_log.append({
            "log_id": f"F09-LOG-{log_i:05d}",
            "action": action,
            "graph_element_id": (row or {}).get("graph_element_id", ""),
            "claim_id": (row or {}).get("claim_id", ""),
            "source_pass": source,
            "prior_verdict": prior_v,
            "new_verdict": new_v,
            "reason": reason,
        })

    for row in baseline:
        cid = (row.get("claim_id") or "").strip()
        geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
        prior_verdict = (row.get("verdict") or "").strip()
        resolved = resolve_graph_key(row, node_eid, node_id_to_eid, rel_eid, triple_to_eids)

        if resolved:
            kind, geid = resolved
            row["graph_element_id"] = geid
            row["match_status"] = kind
            row["coverage_level"] = "element"

        prune_reason = should_prune_row(row, geid, f_ov)
        if prune_reason or geid in p6_ov["remove_eids"] or cid in p6_ov["remove_claim_ids"]:
            reason = prune_reason or "p6_remove"
            prune_stats[reason] += 1
            log("PRUNE", row, "baseline", reason, prior_verdict, "")
            continue

        if geid and geid not in node_eid and geid not in rel_eid:
            prune_stats["stale_not_in_graph"] += 1
            log("PRUNE", row, "baseline", "stale_not_in_graph", prior_verdict, "")
            continue

        if not geid and resolved is None:
            prune_stats["unresolvable"] += 1
            continue

        applied_pass = None
        for pass_id, lookup, key in [
            ("F08", f_ov["by_graph_eid"], geid),
            ("F05", f_ov["by_graph_eid"], geid),
            ("F04", f_ov["by_graph_eid"], geid),
            ("F03", f_ov["by_graph_eid"], geid),
            ("F02", f_ov["by_graph_eid"], geid),
            ("F01", f_ov["by_graph_eid"], geid),
            ("P6-05", p6_ov["by_prior_claim_id"], cid),
            ("P6-04", p6_ov["by_graph_eid"], geid),
            ("P6-03", p6_ov["by_ep08_claim_id"], cid),
            ("P6-02", p6_ov["by_graph_eid"], geid),
            ("P6-01", p6_ov["by_claim_id"], cid),
        ]:
            if not key or key not in lookup:
                continue
            entry = lookup[key]
            if lookup is f_ov["by_graph_eid"] and entry.get("_pass") != pass_id:
                continue
            if lookup is p6_ov["by_graph_eid"] and entry.get("_pass") != pass_id:
                continue
            apply_override(row, entry, pass_id)
            override_stats[pass_id] += 1
            applied_pass = pass_id
            break

        if applied_pass:
            log("OVERRIDE", row, applied_pass, "verdict/fields updated",
                prior_verdict, row.get("verdict", ""))

        act = (row.get("proposed_action") or "").strip()
        if act in REMOVE_ACTIONS:
            prune_stats["action_removed"] += 1
            log("PRUNE", row, applied_pass or "baseline", "action_removed", prior_verdict, "")
            continue

        key = f"{row.get('claim_kind', 'node')}:{geid}"
        if key in merged:
            prune_stats["duplicate_key"] += 1
        merged[key] = row

    covered_node = {r["graph_element_id"] for r in merged.values() if r.get("match_status") == "node"}
    covered_rel = {r["graph_element_id"] for r in merged.values() if r.get("match_status") == "rel"}

    synth_stats: Counter = Counter()
    for geid in sorted(node_eid - covered_node):
        row = synthesize_row("node", geid, graph_nodes, graph_rels, node_label)
        entry = f_ov["by_graph_eid"].get(geid)
        if entry:
            apply_override(row, entry, entry.get("_pass", "F"))
            override_stats[entry.get("_pass", "F")] += 1
        merged[f"node:{geid}"] = row
        synth_stats["nodes"] += 1
        log("SYNTHESIZE", row, "F09", "uncovered live node")

    for geid in sorted(rel_eid - covered_rel):
        row = synthesize_row("rel", geid, graph_nodes, graph_rels, node_label)
        for pass_id in ("F08", "F05", "F03", "F02"):
            entry = f_ov["by_graph_eid"].get(geid)
            if entry and entry.get("_pass") == pass_id:
                apply_override(row, entry, pass_id)
                override_stats[pass_id] += 1
        merged[f"rel:{geid}"] = row
        synth_stats["rels"] += 1
        log("SYNTHESIZE", row, "F09", "uncovered live rel")

    for geid, entry in f_ov["by_graph_eid"].items():
        if geid in node_eid and f"node:{geid}" not in merged:
            row = synthesize_row("node", geid, graph_nodes, graph_rels, node_label)
            apply_override(row, entry, entry.get("_pass", "F"))
            merged[f"node:{geid}"] = row
            synth_stats["nodes"] += 1
            log("ADD_OVERRIDE", row, entry.get("_pass", "F"), "F ledger row for live node not in baseline")
        elif geid in rel_eid and f"rel:{geid}" not in merged:
            row = synthesize_row("rel", geid, graph_nodes, graph_rels, node_label)
            apply_override(row, entry, entry.get("_pass", "F"))
            merged[f"rel:{geid}"] = row
            synth_stats["rels"] += 1
            log("ADD_OVERRIDE", row, entry.get("_pass", "F"), "F ledger row for live rel not in baseline")

    final_rows = list(merged.values())
    verdict_hist = Counter(r.get("verdict", "") for r in final_rows)

    out_csv = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_COLS, extrasaction="ignore")
        w.writeheader()
        for r in sorted(final_rows, key=lambda x: (x.get("claim_kind", ""), x.get("graph_element_id", ""))):
            w.writerow({c: r.get(c, "") for c in OUT_COLS})

    write_merge_log(merge_log)
    write_report(counts, prune_stats, override_stats, synth_stats, verdict_hist,
                 final_rows, f_ov, merge_log)

    coverage = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "live": counts,
        "ledger_rows": len(final_rows),
        "target_rows": counts["elements"],
        "row_match": len(final_rows) == counts["elements"],
        "uncovered_nodes": len(node_eid - {r["graph_element_id"] for r in final_rows if r.get("match_status") == "node"}),
        "uncovered_rels": len(rel_eid - {r["graph_element_id"] for r in final_rows if r.get("match_status") == "rel"}),
        "stale_only": prune_stats.get("stale_not_in_graph", 0),
        "prune_stats": dict(prune_stats),
        "override_stats": dict(override_stats),
        "synth_stats": dict(synth_stats),
        "verdict_hist": dict(verdict_hist),
        "proven_pct": round(100.0 * verdict_hist.get("PROVEN", 0) / len(final_rows), 4) if final_rows else 0,
    }
    (WORK / "coverage.json").write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"F09 merge complete: {len(final_rows)} rows, PROVEN {verdict_hist.get('PROVEN', 0)} "
          f"({coverage['proven_pct']}%), live elements {counts['elements']}")
    if len(final_rows) != counts["elements"]:
        print(
            f"WARNING: row count {len(final_rows)} != live elements {counts['elements']}",
            file=sys.stderr,
        )
    return 0 if len(final_rows) == counts["elements"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
