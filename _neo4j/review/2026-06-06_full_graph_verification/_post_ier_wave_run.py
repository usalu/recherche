#!/usr/bin/env python3
"""Post-IER 6-agent verification wave (POST-01 … POST-06).

Read-only on Neo4j except patch JSONL drafts (dry-run). Run after IER apply.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

csv.field_size_limit(10_000_000)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j import GraphDatabase  # noqa: E402
from neo4j_env import resolve_connection  # noqa: E402

V2 = HERE / "VERIFICATION_LEDGER_ELEMENT_v2.csv"
LEDGER_DIR = HERE / "ledger"
REPORT_DIR = HERE / "reports"
PATCH_DIR = HERE / "patches"
WORK = HERE / "_post_ier_work"
for d in (LEDGER_DIR, REPORT_DIR, PATCH_DIR, WORK):
    d.mkdir(parents=True, exist_ok=True)

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status",
    "verdict", "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
    "source_agent", "coverage_level", "graph_element_id", "match_status",
]
REVIEW_RUN = "post_ier_2026_06_07"
POST01_BATCH = 200

# Load Q04 helpers for catalogue adjudication
_q04_path = HERE / "_agent_q04_catalogue_edges.py"
_spec = importlib.util.spec_from_file_location("q04", _q04_path)
q04 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(q04)  # type: ignore[union-attr]

PARKING_MARKERS = (
    "coming soon", "domain is coming", "parked", "under construction",
    "website coming", "buy this domain",
)
PROG_CATEGORY_IDS = {
    "prog_foerderprogramm", "prog_forschungsprojekt", "prog_pilotprojekt",
    "prog_reallabor", "prog_wettbewerb",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_v2() -> list[dict]:
    return list(csv.DictReader(V2.open(encoding="utf-8")))


def write_csv(path: Path, rows: list[dict], cols: list[str] | None = None) -> None:
    cols = cols or LEDGER_COLS
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def write_patch(path: Path, ops: list[dict]) -> int:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for op in ops:
            fh.write(json.dumps(op, ensure_ascii=False) + "\n")
    return len(ops)


def verdict_summary(rows: list[dict]) -> Counter:
    return Counter(r.get("verdict", "") for r in rows)


def report_md(agent: str, title: str, scope_n: int, rows: list[dict], extras: str = "") -> str:
    vc = verdict_summary(rows)
    pa = Counter(r.get("proposed_action", "") for r in rows)
    proven = vc.get("PROVEN", 0)
    lines = [
        f"# {title}",
        "",
        f"**Date:** {now_utc()} · **Agent:** {agent} · **Database:** `mit-bestand`",
        f"**Scope size:** {scope_n} · **Rows emitted:** {len(rows)}",
        "",
        "## Verdict counts",
        "",
        "| verdict | count |",
        "|---|---:|",
    ]
    for k, v in vc.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        f"**PROVEN in scope:** {proven} ({100 * proven / max(len(rows), 1):.1f}%)",
        "",
        "## Proposed actions",
        "",
        "| action | count |",
        "|---|---:|",
    ]
    for k, v in pa.most_common():
        lines.append(f"| {k} | {v} |")
    if extras:
        lines += ["", extras]
    return "\n".join(lines) + "\n"


def neo4j_session():
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver, database


def export_graph() -> tuple[list[dict], list[dict], dict]:
    driver, database = neo4j_session()
    nodes, rels = [], []
    with driver:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as s:
            for row in s.run("MATCH (n) RETURN n.id AS id, elementId(n) AS eid, labels(n) AS labels, n.name AS name"):
                nodes.append(dict(row))
            for row in s.run(
                "MATCH (a)-[r]->(b) RETURN elementId(r) AS eid, type(r) AS t, "
                "a.id AS from_id, b.id AS to_id, properties(r) AS props"
            ):
                rels.append(dict(row))
    counts = {"nodes": len(nodes), "relationships": len(rels), "database": database}
    (WORK / "graph_counts.json").write_text(json.dumps(counts, indent=2), encoding="utf-8")
    driver.close()
    return nodes, rels, counts


def query_catalogue_batch(limit: int) -> list[dict]:
    driver, database = neo4j_session()
    rows = []
    cypher = """
    MATCH (a)-[r]->(b)
    WHERE type(r) IN ['HAT_BAUTEILTYP','NUTZT_MATERIAL']
      AND coalesce(r.evidence_quote,'') = ''
    RETURN elementId(r) AS element_id, a.id AS from_id, a.name AS from_name,
           b.id AS to_id, b.name AS to_name, type(r) AS rel_type,
           coalesce(a.primary_source_url, head(coalesce(a.source_urls,[]))) AS actor_primary_url,
           coalesce(a.source_urls,[]) AS actor_source_urls,
           r.evidence_url AS evidence_url
    ORDER BY rel_type, from_id, to_id
    LIMIT $limit
    """
    with driver:
        with driver.session(database=database, default_access_mode="READ") as s:
            for row in s.run(cypher, limit=limit):
                rows.append(dict(row))
    driver.close()
    return rows


def run_post_01() -> dict:
    agent = "POST-01"
    scope_total_cypher = 1262  # documented from live count
    batch = query_catalogue_batch(POST01_BATCH)
    vocab_names = q04.load_vocab_names()
    enrich_idx = q04.load_enrichment_index()
    cache: dict = {}
    if q04.R07_CACHE.is_file():
        cache.update(json.loads(q04.R07_CACHE.read_text(encoding="utf-8")))

    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []
    n = 0
    for live in batch:
        n += 1
        fid, tid, rt = live["from_id"], live["to_id"], live["rel_type"]
        pseudo = {
            "from_id": fid, "to_id": tid, "rel_type_or_label": rt,
            "verdict": "PARTIAL", "basis_ref": "", "fetched": "false",
            "http_status": "", "confidence": "teilweise_belegt",
        }
        ev = q04.evaluate_row(pseudo, None, enrich_idx, vocab_names, live, cache)
        verdict = ev["verdict_after"]
        action = ev["proposed_action"]
        row = {
            "claim_id": f"post01-{n:04d}",
            "claim_kind": "rel",
            "element_id": live["element_id"],
            "from_id": fid,
            "to_id": tid,
            "rel_type_or_label": rt,
            "asserted_claim": f"{fid} —[{rt}]→ {tid} (catalogue extension)",
            "basis_type": "web" if ev.get("basis_ref", "").startswith("http") else "logic",
            "basis_ref": ev.get("basis_ref", ""),
            "fetched": ev.get("fetched", "false"),
            "http_status": ev.get("http_status", ""),
            "verdict": verdict,
            "confidence": ev.get("confidence", ""),
            "proof_quote": ev.get("proof_quote", ""),
            "proposed_action": action,
            "agent_id": agent,
            "notes": ev.get("notes", "") or "batch catalogue backfill; empty evidence_quote on live rel",
            "source_agent": agent,
            "coverage_level": "element",
            "graph_element_id": live["element_id"],
            "match_status": "rel",
        }
        ledger_rows.append(row)
        if action == "UPGRADE" and ev.get("proof_quote"):
            patch_ops.append({
                "op": "set_rel_properties",
                "from": fid,
                "to": tid,
                "type": rt,
                "properties": {
                    "evidence_url": ev["basis_ref"],
                    "evidence_quote": ev["proof_quote"][:500],
                    "evidence_confidence": "belegt",
                    "evidence_basis": "post_01_web_fetch",
                    "review_run": REVIEW_RUN,
                    "semantic_basis": "catalog_extension",
                },
                "reason": f"POST-01 strict-gate upgrade for {fid}->{tid}",
            })

    out_csv = LEDGER_DIR / "post_01.csv"
    out_md = REPORT_DIR / "post_01_report.md"
    out_patch = PATCH_DIR / "post_01_catalogue_backfill.patch.jsonl"
    write_csv(out_csv, ledger_rows)
    write_patch(out_patch, patch_ops)
    extras = (
        f"## Remainder\n\n"
        f"Live catalogue rels without `evidence_quote`: **~{scope_total_cypher}** total; "
        f"this run processed **{len(batch)}** (batch cap {POST01_BATCH}).\n\n"
        f"Patch ops drafted (dry-run): **{len(patch_ops)}** upgrades.\n"
    )
    out_md.write_text(
        report_md(agent, "POST-01 Catalogue quote backfill", scope_total_cypher, ledger_rows, extras),
        encoding="utf-8",
    )
    vc = verdict_summary(ledger_rows)
    return {"agent": agent, "scope": scope_total_cypher, "processed": len(batch), "proven": vc.get("PROVEN", 0), "patches": len(patch_ops)}


def run_post_02(v2: list[dict]) -> dict:
    agent = "POST-02"
    scope = [r for r in v2 if r["verdict"] == "SCHEMA_VIOLATION"]
    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []
    for i, r in enumerate(scope, 1):
        eid = r.get("graph_element_id") or r.get("element_id", "")
        fid, tid, rt = r.get("from_id", ""), r.get("to_id", ""), r.get("rel_type_or_label", "")
        is_prog_edge = rt == "TEIL_VON_PROGRAMM" and tid in PROG_CATEGORY_IDS
        is_prog_node = r["claim_kind"] == "node" and fid.startswith("prog_") and fid in PROG_CATEGORY_IDS
        if is_prog_edge:
            action, verdict = "DELETE", "SCHEMA_VIOLATION"
            patch_ops.append({
                "op": "delete_rel", "from": fid, "to": tid, "type": rt,
                "reason": f"POST-02: TEIL_VON_PROGRAMM to category-word node {tid}",
            })
        elif is_prog_node:
            action, verdict = "DEPRECATE_NODE", "SCHEMA_VIOLATION"
            patch_ops.append({
                "op": "set_node_properties", "id": fid,
                "properties": {"review_status": "deprecated_category_stub", "review_run": REVIEW_RUN},
                "reason": f"POST-02: generic Programme category node {fid}",
            })
        else:
            action = r.get("proposed_action", "ESCALATE_HUMAN")
            verdict = "SCHEMA_VIOLATION"
        ledger_rows.append({
            **{k: r.get(k, "") for k in LEDGER_COLS if k in r},
            "claim_id": f"post02-{i:04d}",
            "agent_id": agent,
            "source_agent": agent,
            "verdict": verdict,
            "proposed_action": action,
            "notes": (r.get("notes", "") + f"; [POST-02] tier-D schema fix proposal").strip("; "),
        })

    write_csv(LEDGER_DIR / "post_02.csv", ledger_rows)
    write_patch(PATCH_DIR / "post_02_schema_violation.patch.jsonl", patch_ops)
    (REPORT_DIR / "post_02_report.md").write_text(
        report_md(agent, "POST-02 SCHEMA_VIOLATION tier-D", len(scope), ledger_rows,
                  f"Patch ops (dry-run): **{len(patch_ops)}** delete_rel / deprecate."),
        encoding="utf-8",
    )
    return {"agent": agent, "scope": len(scope), "processed": len(ledger_rows), "proven": 0, "patches": len(patch_ops)}


def run_post_03(v2: list[dict]) -> dict:
    agent = "POST-03"
    scope = [r for r in v2 if r["verdict"] == "CONTRADICTION"]
    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []
    stadt_re = re.compile(r"stadt_([a-z0-9_]+)")
    land_re = re.compile(r"land_([a-z0-9_]+)")

    for i, r in enumerate(scope, 1):
        fid, tid, rt = r.get("from_id", ""), r.get("to_id", ""), r.get("rel_type_or_label", "")
        notes = r.get("notes", "")
        pq = r.get("proof_quote", "")
        action = "ESCALATE_HUMAN"
        fix_target = ""
        if "stadt_" in notes.lower() or "more correct stadt" in notes.lower():
            m = re.search(r"\(stadt_([a-z0-9_]+)\)", pq)
            if m:
                fix_target = f"stadt_{m.group(1)}"
                action = "FIX_PROPERTY"
        elif rt == "LIEGT_IN_LAND" and "address names" in pq.lower():
            # infer land from address tail
            if "belgium" in pq.lower() or "belgien" in pq.lower():
                fix_target = "land_belgien"
            elif "switzerland" in pq.lower() or "schweiz" in pq.lower():
                fix_target = "land_schweiz"
            elif "germany" in pq.lower() or "deutschland" in pq.lower():
                fix_target = "land_deutschland"
            elif "netherlands" in pq.lower() or "niederlande" in pq.lower():
                fix_target = "land_niederlande"
            if fix_target and fix_target != tid:
                action = "FIX_PROPERTY"

        if action == "FIX_PROPERTY" and fix_target:
            patch_ops.append({
                "op": "delete_rel", "from": fid, "to": tid, "type": rt,
                "reason": f"POST-03: remove contradictory {rt} {fid}->{tid}",
            })
            patch_ops.append({
                "op": "add_rel", "from": fid, "to": fix_target, "type": rt,
                "properties": {"review_run": REVIEW_RUN, "evidence_basis": "post_03_geo_fix"},
                "reason": f"POST-03: re-link {fid} to {fix_target} per address evidence",
            })

        ledger_rows.append({
            **{k: r.get(k, "") for k in LEDGER_COLS if k in r},
            "claim_id": f"post03-{i:04d}",
            "agent_id": agent,
            "source_agent": agent,
            "proposed_action": action,
            "notes": f"{notes}; fix_target={fix_target or 'none'}",
        })

    write_csv(LEDGER_DIR / "post_03.csv", ledger_rows)
    write_patch(PATCH_DIR / "post_03_geo_fixes.patch.jsonl", patch_ops)
    fixes = sum(1 for r in ledger_rows if r["proposed_action"] == "FIX_PROPERTY")
    (REPORT_DIR / "post_03_report.md").write_text(
        report_md(agent, "POST-03 CONTRADICTION geo", len(scope), ledger_rows,
                  f"Geo fix proposals: **{fixes}** · patch ops: **{len(patch_ops)}** (dry-run)."),
        encoding="utf-8",
    )
    return {"agent": agent, "scope": len(scope), "processed": len(ledger_rows), "proven": 0, "patches": len(patch_ops)}


def fetch_simple(url: str, cache: dict) -> dict:
    return q04.fetch_url(url, cache)


def run_post_04(v2: list[dict]) -> dict:
    agent = "POST-04"
    scope = [r for r in v2 if r["verdict"] == "MISSING_EVIDENCE"]
    cache: dict = {}
    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []
    domain_re = re.compile(r"([a-z0-9][-a-z0-9]*\.[a-z]{2,}(?:\.[a-z]{2,})?)", re.I)

    for i, r in enumerate(scope, 1):
        basis = (r.get("basis_ref") or "").strip()
        notes = r.get("notes", "")
        urls: list[str] = []
        if basis.startswith("http"):
            urls.append(basis)
        for m in domain_re.finditer(notes):
            d = m.group(1).lower()
            if d not in ("e.g", "etc"):
                urls.append(f"https://www.{d}/")
        verdict, pq, fetched, status, action = "MISSING_EVIDENCE", "", "false", "", r.get("proposed_action", "ADD_SOURCE")
        hit_url = ""
        for url in urls[:3]:
            fe = fetch_simple(url, cache)
            text = fe.get("text") or ""
            if not fe.get("fetched"):
                continue
            status = fe.get("http_status", "")
            fetched = "true"
            plain = q04.strip_html(text)
            name = r.get("element_id", "") if r["claim_kind"] == "node" else r.get("from_id", "")
            tokens = [t for t in re.split(r"[\s_]+", name) if len(t) >= 4]
            for sent in re.split(r"(?<=[.!?])\s+", plain):
                sn = q04.norm_text(sent)
                if any(q04.norm_text(t) in sn for t in tokens[:3]) and q04.is_valid_quote(sent):
                    verdict, pq, action, hit_url = "PROVEN", sent.strip()[:300], "ADD_SOURCE", url
                    break
            if verdict == "PROVEN":
                break

        row = {
            **{k: r.get(k, "") for k in LEDGER_COLS if k in r},
            "claim_id": f"post04-{i:04d}",
            "agent_id": agent,
            "source_agent": agent,
            "verdict": verdict,
            "basis_ref": hit_url or basis,
            "fetched": fetched,
            "http_status": status,
            "proof_quote": pq,
            "proposed_action": action,
            "confidence": "belegt" if verdict == "PROVEN" else r.get("confidence", ""),
        }
        ledger_rows.append(row)
        if verdict == "PROVEN" and r["claim_kind"] == "node" and hit_url:
            patch_ops.append({
                "op": "set_node_properties",
                "id": r["element_id"],
                "properties": {
                    "primary_source_url": hit_url,
                    "source_urls": [hit_url],
                    "source_quote": pq[:500],
                    "review_run": REVIEW_RUN,
                },
                "reason": f"POST-04 recovery for {r['element_id']}",
            })

    write_csv(LEDGER_DIR / "post_04.csv", ledger_rows)
    write_patch(PATCH_DIR / "post_04_missing_evidence.patch.jsonl", patch_ops)
    proven = verdict_summary(ledger_rows).get("PROVEN", 0)
    (REPORT_DIR / "post_04_report.md").write_text(
        report_md(agent, "POST-04 MISSING_EVIDENCE recovery", len(scope), ledger_rows,
                  f"Upgraded to PROVEN: **{proven}** · patch ops: **{len(patch_ops)}**."),
        encoding="utf-8",
    )
    return {"agent": agent, "scope": len(scope), "processed": len(ledger_rows), "proven": proven, "patches": len(patch_ops)}


def run_post_05(v2: list[dict]) -> dict:
    agent = "POST-05"
    scope = [r for r in v2 if r["verdict"] == "PARTIAL"]
    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []
    cache: dict = {}

    for i, r in enumerate(scope, 1):
        eid = r.get("element_id", "")
        rt = r.get("rel_type_or_label", "")
        basis = (r.get("basis_ref") or "").strip()
        notes = r.get("notes", "")
        verdict = "PARTIAL"
        action = r.get("proposed_action", "KEEP")
        pq = r.get("proof_quote", "")

        if eid.startswith("nf_") and "dangling requirement" in notes.lower():
            action = "KEEP"
        elif rt == "VERBUNDEN_MIT_AKTEUR" and "category inference" in notes.lower():
            action, verdict = "DELETE", "UNSUPPORTED"
            if r["claim_kind"] == "rel":
                patch_ops.append({
                    "op": "delete_rel",
                    "from": r["from_id"], "to": r["to_id"], "type": rt,
                    "reason": "POST-05: unsupported VMA category inference",
                })
        elif basis.startswith("http") and r["claim_kind"] == "node":
            fe = fetch_simple(basis, cache)
            if fe.get("fetched"):
                plain = q04.strip_html(fe.get("text", ""))
                name_tok = q04.norm_text(eid.replace("p_", "").replace("_", " "))
                for sent in re.split(r"(?<=[.!?])\s+", plain):
                    if name_tok[:12] in q04.norm_text(sent) and q04.is_valid_quote(sent):
                        verdict, pq, action = "PROVEN", sent.strip()[:300], "KEEP"
                        break

        ledger_rows.append({
            **{k: r.get(k, "") for k in LEDGER_COLS if k in r},
            "claim_id": f"post05-{i:04d}",
            "agent_id": agent,
            "source_agent": agent,
            "verdict": verdict,
            "proof_quote": pq,
            "proposed_action": action,
        })

    write_csv(LEDGER_DIR / "post_05.csv", ledger_rows)
    write_patch(PATCH_DIR / "post_05_partial.patch.jsonl", patch_ops)
    proven = verdict_summary(ledger_rows).get("PROVEN", 0)
    (REPORT_DIR / "post_05_report.md").write_text(
        report_md(agent, "POST-05 PARTIAL residual", len(scope), ledger_rows,
                  f"Upgraded: **{proven}** · DELETE proposals: **{len(patch_ops)}**."),
        encoding="utf-8",
    )
    return {"agent": agent, "scope": len(scope), "processed": len(ledger_rows), "proven": proven, "patches": len(patch_ops)}


def is_parking_proof(row: dict) -> bool:
    pq = (row.get("proof_quote") or "").lower()
    sq = (row.get("notes") or "").lower()
    combined = pq + " " + sq
    return any(m in combined for m in PARKING_MARKERS)


def dedupe_key(row: dict) -> str:
    geid = (row.get("graph_element_id") or "").strip()
    if geid:
        return f"{row.get('claim_kind','')}:{geid}"
    kind = row.get("claim_kind", "")
    if kind == "rel":
        return f"rel:{row.get('from_id')}|{row.get('rel_type_or_label')}|{row.get('to_id')}"
    return f"node:{row.get('element_id', '')}"


def run_post_06(v2: list[dict], nodes: list[dict], rels: list[dict], agent_stats: list[dict]) -> dict:
    agent = "POST-06"
    rel_eid = {r["eid"] for r in rels}
    node_eid = {n["eid"] for n in nodes}
    triple = {(r["from_id"], r["t"], r["to_id"]) for r in rels}

    # Weak PROVEN audit on v2 + overlays from post_01..05
    overlay_files = [
        LEDGER_DIR / "post_01.csv",
        LEDGER_DIR / "post_02.csv",
        LEDGER_DIR / "post_03.csv",
        LEDGER_DIR / "post_04.csv",
        LEDGER_DIR / "post_05.csv",
    ]
    overlays: dict[str, dict] = {}
    for path in overlay_files:
        if not path.is_file():
            continue
        for row in csv.DictReader(path.open(encoding="utf-8")):
            overlays[dedupe_key(row)] = row

    audit_rows: list[dict] = []
    downgrades = 0
    for i, r in enumerate(v2, 1):
        if r["verdict"] != "PROVEN":
            continue
        key = dedupe_key(r)
        ov = overlays.get(key)
        check = ov or r
        if is_parking_proof(check) or (
            check.get("element_id", "") in ("embuild", "franck")
            and "coming soon" in (check.get("proof_quote") or "").lower()
        ):
            downgrades += 1
            audit_rows.append({
                "claim_id": f"post06-audit-{downgrades:04d}",
                "claim_kind": r["claim_kind"],
                "element_id": r.get("element_id", ""),
                "from_id": r.get("from_id", ""),
                "to_id": r.get("to_id", ""),
                "rel_type_or_label": r.get("rel_type_or_label", ""),
                "asserted_claim": r.get("asserted_claim", ""),
                "basis_type": check.get("basis_type", ""),
                "basis_ref": check.get("basis_ref", ""),
                "fetched": check.get("fetched", ""),
                "http_status": check.get("http_status", ""),
                "verdict": "PARTIAL",
                "confidence": "teilweise_belegt",
                "proof_quote": check.get("proof_quote", ""),
                "proposed_action": "RESOURCE",
                "agent_id": agent,
                "notes": "domain parking / coming-soon page; downgrade from PROVEN",
                "source_agent": agent,
                "coverage_level": "element",
                "graph_element_id": r.get("graph_element_id", ""),
                "match_status": r.get("match_status", ""),
            })

    write_csv(LEDGER_DIR / "post_06.csv", audit_rows)

    # Merge v3
    merged: dict[str, dict] = {}
    stale = 0
    for r in v2:
        key = dedupe_key(r)
        kind = r.get("claim_kind", "")
        geid = r.get("graph_element_id", "")
        if kind == "rel":
            fid, rt, tid = r.get("from_id"), r.get("rel_type_or_label"), r.get("to_id")
            if geid and geid not in rel_eid and (fid, rt, tid) not in triple:
                stale += 1
                continue
        elif kind == "node" and geid and geid not in node_eid:
            stale += 1
            continue
        merged[key] = dict(r)

    for key, ov in overlays.items():
        if key in merged:
            base = merged[key]
            if ov.get("verdict"):
                base["verdict"] = ov["verdict"]
            if ov.get("proof_quote"):
                base["proof_quote"] = ov["proof_quote"]
            if ov.get("proposed_action"):
                base["proposed_action"] = ov["proposed_action"]
            if ov.get("basis_ref"):
                base["basis_ref"] = ov["basis_ref"]
            if ov.get("fetched"):
                base["fetched"] = ov["fetched"]
            if ov.get("http_status"):
                base["http_status"] = ov["http_status"]
            base["source_agent"] = (base.get("source_agent", "") + "+" + ov.get("source_agent", "")).strip("+")
            merged[key] = base

    for ar in audit_rows:
        key = dedupe_key(ar)
        if key in merged:
            merged[key].update({
                "verdict": ar["verdict"],
                "proposed_action": ar["proposed_action"],
                "notes": (merged[key].get("notes", "") + "; " + ar["notes"]).strip("; "),
                "source_agent": merged[key].get("source_agent", "") + "+POST-06",
            })

    v3_rows = list(merged.values())
    v3_path = HERE / "VERIFICATION_LEDGER_ELEMENT_v3.csv"
    write_csv(v3_path, v3_rows)

    vc = verdict_summary(v3_rows)
    total = len(v3_rows)
    proven_n = vc.get("PROVEN", 0)
    proven_pct = 100 * proven_n / max(total, 1)

    campaign_lines = [
        "# POST-IER Campaign Report",
        "",
        f"**Date:** {now_utc()} · **Database:** `mit-bestand`",
        f"**Graph:** {len(nodes)} nodes / {len(rels)} relationships",
        f"**Ledger v3:** {total} element rows · **{proven_pct:.2f}% PROVEN** ({proven_n})",
        f"**Stale v2 rows pruned:** {stale} (IER-deleted rels + orphans)",
        f"**Weak PROVEN downgrades:** {downgrades}",
        "",
        "## Agent summary",
        "",
        "| Agent | Scope | Processed | PROVEN | Patches |",
        "|---|---:|---:|---:|---:|",
    ]
    for st in agent_stats:
        campaign_lines.append(
            f"| {st['agent']} | {st['scope']} | {st['processed']} | {st['proven']} | {st['patches']} |"
        )
    campaign_lines += [
        "",
        "## v3 verdict distribution",
        "",
        "| verdict | count | share |",
        "|---|---:|---:|",
    ]
    for k, v in vc.most_common():
        campaign_lines.append(f"| {k} | {v} | {100*v/total:.2f}% |")
    campaign_lines += [
        "",
        "## Outputs",
        "",
        "- `VERIFICATION_LEDGER_ELEMENT_v3.csv`",
        "- `ledger/post_01.csv` … `ledger/post_06.csv`",
        "- `reports/post_01_report.md` … `reports/post_06_report.md`",
        "- `patches/post_0N_*.patch.jsonl` (dry-run drafts)",
    ]
    (REPORT_DIR / "POST_IER_CAMPAIGN_REPORT.md").write_text("\n".join(campaign_lines) + "\n", encoding="utf-8")
    (REPORT_DIR / "post_06_report.md").write_text(
        report_md(agent, "POST-06 Weak PROVEN audit + aggregator", downgrades, audit_rows,
                  f"v3: **{total}** rows · **{proven_pct:.2f}% PROVEN** · stale pruned **{stale}**."),
        encoding="utf-8",
    )
    return {
        "agent": agent,
        "scope": downgrades,
        "processed": len(audit_rows),
        "proven": proven_n,
        "proven_pct": proven_pct,
        "v3_rows": total,
        "stale_pruned": stale,
        "patches": 0,
    }


def main() -> int:
    print("Exporting live graph…")
    nodes, rels, counts = export_graph()
    print(f"Graph: {counts}")

    v2 = load_v2()
    print(f"v2 ledger: {len(v2)} rows")

    stats = []
    print("POST-01…")
    stats.append(run_post_01())
    print("POST-02…")
    stats.append(run_post_02(v2))
    print("POST-03…")
    stats.append(run_post_03(v2))
    print("POST-04…")
    stats.append(run_post_04(v2))
    print("POST-05…")
    stats.append(run_post_05(v2))
    print("POST-06…")
    post06 = run_post_06(v2, nodes, rels, stats)
    stats.append(post06)

    summary = {
        "generated_at": now_utc(),
        "graph_counts": counts,
        "agents": stats,
        "v3_proven_pct": post06.get("proven_pct"),
    }
    (WORK / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
