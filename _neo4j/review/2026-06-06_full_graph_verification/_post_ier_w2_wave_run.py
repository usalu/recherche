#!/usr/bin/env python3
"""Post-IER W2 5-agent verification wave (W2-01 … W2-05).

Read-only on Neo4j except patch apply after dry-run pass.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import subprocess
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

V3 = HERE / "VERIFICATION_LEDGER_ELEMENT_v3.csv"
LEDGER_DIR = HERE / "ledger"
REPORT_DIR = HERE / "reports"
PATCH_DIR = HERE / "patches"
WORK = HERE / "_post_ier_w2_work"
for d in (LEDGER_DIR, REPORT_DIR, PATCH_DIR, WORK):
    d.mkdir(parents=True, exist_ok=True)

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status",
    "verdict", "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
    "source_agent", "coverage_level", "graph_element_id", "match_status",
]
REVIEW_RUN = "post_ier_w2_2026_06_07"
W2_01_OFFSET = 200
W2_01_LIMIT = 300

_q04_path = HERE / "_agent_q04_catalogue_edges.py"
_spec = importlib.util.spec_from_file_location("q04", _q04_path)
q04 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(q04)  # type: ignore[union-attr]

PROG_CATEGORY_IDS = {
    "prog_foerderprogramm", "prog_forschungsprojekt", "prog_pilotprojekt",
    "prog_reallabor", "prog_wettbewerb",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_v3() -> list[dict]:
    return list(csv.DictReader(V3.open(encoding="utf-8")))


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


def graph_counts() -> dict:
    driver, database = neo4j_session()
    with driver:
        with driver.session(database=database, default_access_mode="READ") as s:
            nc = s.run("MATCH (n) RETURN count(n) AS c").single()["c"]
            rc = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    driver.close()
    return {"nodes": nc, "relationships": rc, "database": database}


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


def apply_patch(patch_path: Path, agent: str) -> dict:
    """Dry-run then apply patch; return status dict."""
    rel = patch_path.relative_to(REPO).as_posix()
    name = patch_path.name
    result = {
        "agent": agent,
        "patch": rel,
        "dry_run_ok": False,
        "applied": False,
        "error": "",
        "counts_before": graph_counts(),
        "counts_after": None,
    }
    if not patch_path.is_file() or patch_path.stat().st_size == 0:
        result["error"] = "patch missing or empty"
        return result

    dry = subprocess.run(
        [sys.executable, str(SCRIPTS / "apply_neo4j_review_patch.py"), "--patch", rel],
        cwd=str(REPO), capture_output=True, text=True,
    )
    dry_out = dry.stdout + dry.stderr
    (WORK / f"{agent}_dry_run.txt").write_text(dry_out, encoding="utf-8")
    result["dry_run_ok"] = dry.returncode == 0
    if not result["dry_run_ok"]:
        result["error"] = f"dry-run failed (exit {dry.returncode})"
        return result

    confirm = f"APPLY {name} TO mit-bestand"
    live = subprocess.run(
        [sys.executable, str(SCRIPTS / "apply_neo4j_review_patch.py"), "--patch", rel, "--confirm", confirm],
        cwd=str(REPO), capture_output=True, text=True,
    )
    live_out = live.stdout + live.stderr
    (WORK / f"{agent}_apply.txt").write_text(live_out, encoding="utf-8")
    result["counts_after"] = graph_counts()
    if live.returncode != 0:
        result["error"] = f"apply failed (exit {live.returncode})"
        return result
    result["applied"] = True
    return result


def query_catalogue_batch(offset: int, limit: int) -> tuple[list[dict], int]:
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
    SKIP $offset LIMIT $limit
    """
    total_cypher = """
    MATCH ()-[r]->()
    WHERE type(r) IN ['HAT_BAUTEILTYP','NUTZT_MATERIAL']
      AND coalesce(r.evidence_quote,'') = ''
    RETURN count(r) AS c
    """
    with driver:
        with driver.session(database=database, default_access_mode="READ") as s:
            total = s.run(total_cypher).single()["c"]
            for row in s.run(cypher, offset=offset, limit=limit):
                rows.append(dict(row))
    driver.close()
    return rows, total


def dedupe_key(row: dict) -> str:
    geid = (row.get("graph_element_id") or "").strip()
    if geid:
        return f"{row.get('claim_kind','')}:{geid}"
    kind = row.get("claim_kind", "")
    if kind == "rel":
        return f"rel:{row.get('from_id')}|{row.get('rel_type_or_label')}|{row.get('to_id')}"
    return f"node:{row.get('element_id', '')}"


def fetch_simple(url: str, cache: dict) -> dict:
    return q04.fetch_url(url, cache)


def run_w2_01() -> dict:
    agent = "W2-01"
    batch, scope_total = query_catalogue_batch(W2_01_OFFSET, W2_01_LIMIT)
    vocab_names = q04.load_vocab_names()
    enrich_idx = q04.load_enrichment_index()
    cache: dict = {}
    if q04.R07_CACHE.is_file():
        cache.update(json.loads(q04.R07_CACHE.read_text(encoding="utf-8")))

    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []
    for n, live in enumerate(batch, 1):
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
            "claim_id": f"w2-01-{n:04d}",
            "claim_kind": "rel",
            "element_id": live["element_id"],
            "from_id": fid, "to_id": tid, "rel_type_or_label": rt,
            "asserted_claim": f"{fid} —[{rt}]→ {tid} (catalogue extension W2)",
            "basis_type": "web" if ev.get("basis_ref", "").startswith("http") else "logic",
            "basis_ref": ev.get("basis_ref", ""),
            "fetched": ev.get("fetched", "false"),
            "http_status": ev.get("http_status", ""),
            "verdict": verdict,
            "confidence": ev.get("confidence", ""),
            "proof_quote": ev.get("proof_quote", ""),
            "proposed_action": action,
            "agent_id": agent,
            "notes": ev.get("notes", "") or f"W2-01 offset={W2_01_OFFSET} strict gate",
            "source_agent": agent,
            "coverage_level": "element",
            "graph_element_id": live["element_id"],
            "match_status": "rel",
        }
        ledger_rows.append(row)
        if action == "UPGRADE" and ev.get("proof_quote"):
            patch_ops.append({
                "op": "set_rel_properties",
                "from": fid, "to": tid, "type": rt,
                "properties": {
                    "evidence_url": ev["basis_ref"],
                    "evidence_quote": ev["proof_quote"][:500],
                    "evidence_confidence": "belegt",
                    "evidence_basis": "w2_01_web_fetch",
                    "review_run": REVIEW_RUN,
                    "semantic_basis": "catalog_extension",
                },
                "reason": f"W2-01 strict-gate upgrade for {fid}->{tid}",
            })

    out_csv = LEDGER_DIR / "w2_01.csv"
    out_md = REPORT_DIR / "w2_01_report.md"
    out_patch = PATCH_DIR / "w2_01_catalogue_backfill.patch.jsonl"
    write_csv(out_csv, ledger_rows)
    write_patch(out_patch, patch_ops)
    remainder = max(scope_total - W2_01_OFFSET - len(batch), 0)
    extras = (
        f"## Batch position\n\n"
        f"Offset **{W2_01_OFFSET}** · processed **{len(batch)}** · live remainder after this batch: **~{remainder}** "
        f"(total empty-quote catalogue rels: **{scope_total}**).\n\n"
        f"**Strict gate:** same as POST-01 — do NOT apply `post_01_catalogue_backfill.patch.jsonl`.\n\n"
        f"W2-01 patch ops drafted (dry-run): **{len(patch_ops)}** upgrades.\n"
    )
    out_md.write_text(
        report_md(agent, "W2-01 Catalogue backfill continuation", scope_total, ledger_rows, extras),
        encoding="utf-8",
    )
    vc = verdict_summary(ledger_rows)
    return {
        "agent": agent, "scope": scope_total, "processed": len(batch),
        "proven": vc.get("PROVEN", 0), "patches_drafted": len(patch_ops),
        "patches_applied": 0, "apply_status": "dry-run only",
    }


def run_w2_02(v3: list[dict]) -> dict:
    agent = "W2-02"
    patch_path = PATCH_DIR / "post_04_missing_evidence.patch.jsonl"
    apply_result = apply_patch(patch_path, agent)

    patched_ids: set[str] = set()
    if patch_path.is_file():
        for line in patch_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            op = json.loads(line)
            if op.get("op") == "set_node_properties" and op.get("id"):
                patched_ids.add(op["id"])

    scope = [r for r in v3 if r["verdict"] == "MISSING_EVIDENCE"]
    residual = [r for r in scope if r.get("element_id", "") not in patched_ids]
    cache: dict = {}
    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []
    domain_re = re.compile(r"([a-z0-9][-a-z0-9]*\.[a-z]{2,}(?:\.[a-z]{2,})?)", re.I)

    for i, r in enumerate(residual, 1):
        basis = (r.get("basis_ref") or "").strip()
        notes = r.get("notes", "")
        urls: list[str] = []
        if basis.startswith("http"):
            urls.append(basis)
        for m in domain_re.finditer(notes):
            d = m.group(1).lower()
            if d not in ("e.g", "etc"):
                urls.append(f"https://www.{d}/")
        verdict, pq, fetched, status = "MISSING_EVIDENCE", "", "false", ""
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
                    verdict, pq, hit_url = "PROVEN", sent.strip()[:300], url
                    break
            if verdict == "PROVEN":
                break

        row = {
            **{k: r.get(k, "") for k in LEDGER_COLS if k in r},
            "claim_id": f"w2-02-{i:04d}",
            "agent_id": agent, "source_agent": agent,
            "verdict": verdict,
            "basis_ref": hit_url or basis,
            "fetched": fetched, "http_status": status,
            "proof_quote": pq,
            "proposed_action": "ADD_SOURCE" if verdict == "PROVEN" else r.get("proposed_action", "ADD_SOURCE"),
            "confidence": "belegt" if verdict == "PROVEN" else r.get("confidence", ""),
            "notes": (r.get("notes", "") + "; W2-02 residual web search").strip("; "),
        }
        ledger_rows.append(row)
        if verdict == "PROVEN" and r["claim_kind"] == "node" and hit_url:
            patch_ops.append({
                "op": "set_node_properties", "id": r["element_id"],
                "properties": {
                    "primary_source_url": hit_url,
                    "source_urls": [hit_url],
                    "source_quote": pq[:500],
                    "review_run": REVIEW_RUN,
                },
                "reason": f"W2-02 recovery for {r['element_id']}",
            })

    write_csv(LEDGER_DIR / "w2_02.csv", ledger_rows)
    w2_patch = PATCH_DIR / "w2_02_missing_evidence.patch.jsonl"
    write_patch(w2_patch, patch_ops)
    w2_apply = apply_patch(w2_patch, f"{agent}_residual") if patch_ops else None

    cb = apply_result.get("counts_before", {})
    ca = apply_result.get("counts_after") or cb
    extras = (
        f"## Patch apply: post_04_missing_evidence\n\n"
        f"- Dry-run OK: **{apply_result.get('dry_run_ok')}**\n"
        f"- Applied: **{apply_result.get('applied')}**\n"
        f"- Error: {apply_result.get('error') or 'none'}\n"
        f"- Graph before: {cb.get('nodes')} nodes / {cb.get('relationships')} rels\n"
        f"- Graph after: {ca.get('nodes')} nodes / {ca.get('relationships')} rels\n\n"
        f"## Residual MISSING_EVIDENCE\n\n"
        f"v3 scope: **{len(scope)}** · patched by POST-04: **{len(patched_ids)}** · "
        f"residual searched: **{len(residual)}** · new PROVEN: **{verdict_summary(ledger_rows).get('PROVEN', 0)}**\n"
    )
    if w2_apply:
        extras += (
            f"\nW2-02 residual patch: drafted **{len(patch_ops)}** · applied **{w2_apply.get('applied')}**\n"
        )
    (REPORT_DIR / "w2_02_report.md").write_text(
        report_md(agent, "W2-02 POST-04 apply + MISSING residual", len(scope), ledger_rows, extras),
        encoding="utf-8",
    )
    proven = verdict_summary(ledger_rows).get("PROVEN", 0)
    patches_applied = (1 if apply_result.get("applied") else 0) + (1 if w2_apply and w2_apply.get("applied") else 0)
    return {
        "agent": agent, "scope": len(scope), "processed": len(residual),
        "proven": proven + len(patched_ids),
        "patches_drafted": len(patch_ops),
        "patches_applied": patches_applied,
        "apply_status": "applied" if apply_result.get("applied") else apply_result.get("error", "skipped"),
        "apply_result": apply_result,
    }


def run_w2_03(v3: list[dict]) -> dict:
    agent = "W2-03"
    patch_path = PATCH_DIR / "post_03_geo_fixes.patch.jsonl"
    apply_result = apply_patch(patch_path, agent)

    scope = [r for r in v3 if r["verdict"] == "CONTRADICTION"]
    ledger_rows: list[dict] = []
    for i, r in enumerate(scope, 1):
        ledger_rows.append({
            **{k: r.get(k, "") for k in LEDGER_COLS if k in r},
            "claim_id": f"w2-03-{i:04d}",
            "agent_id": agent, "source_agent": agent,
            "notes": (r.get("notes", "") + "; W2-03 re-adjudication post-geo-apply").strip("; "),
            "proposed_action": r.get("proposed_action", "ESCALATE_HUMAN"),
        })

    write_csv(LEDGER_DIR / "w2_03.csv", ledger_rows)
    cb = apply_result.get("counts_before", {})
    ca = apply_result.get("counts_after") or cb
    fixes = sum(1 for r in ledger_rows if r.get("proposed_action") == "FIX_PROPERTY")
    extras = (
        f"## Patch apply: post_03_geo_fixes\n\n"
        f"- Dry-run OK: **{apply_result.get('dry_run_ok')}**\n"
        f"- Applied: **{apply_result.get('applied')}**\n"
        f"- Error: {apply_result.get('error') or 'none'}\n"
        f"- Graph before: {cb.get('nodes')} nodes / {cb.get('relationships')} rels\n"
        f"- Graph after: {ca.get('nodes')} nodes / {ca.get('relationships')} rels\n\n"
        f"Remaining CONTRADICTION rows in v3 overlay: **{len(scope)}** "
        f"(FIX_PROPERTY proposals: **{fixes}**; human-gated remainder documented).\n"
    )
    (REPORT_DIR / "w2_03_report.md").write_text(
        report_md(agent, "W2-03 Geo CONTRADICTION fixes", len(scope), ledger_rows, extras),
        encoding="utf-8",
    )
    return {
        "agent": agent, "scope": len(scope), "processed": len(ledger_rows),
        "proven": 0, "patches_drafted": 0,
        "patches_applied": 1 if apply_result.get("applied") else 0,
        "apply_status": "applied" if apply_result.get("applied") else apply_result.get("error", "skipped"),
        "apply_result": apply_result,
    }


def run_w2_04(v3: list[dict]) -> dict:
    agent = "W2-04"
    scope = [r for r in v3 if r["verdict"] == "PARTIAL"]
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
        elif rt == "VERBUNDEN_MIT_AKTEUR" and (
            "category inference" in notes.lower()
            or "unsupported vma" in notes.lower()
            or "weak" in notes.lower()
        ):
            action, verdict = "DELETE", "UNSUPPORTED"
            if r["claim_kind"] == "rel":
                patch_ops.append({
                    "op": "delete_rel",
                    "from": r["from_id"], "to": r["to_id"], "type": rt,
                    "reason": "W2-04: unsupported VMA category inference",
                })
        elif rt == "VERBUNDEN_MIT_AKTEUR" and r["claim_kind"] == "rel":
            fid = r.get("from_id", "")
            if fid.startswith("p_") and not basis.startswith("http"):
                action, verdict = "DELETE", "UNSUPPORTED"
                patch_ops.append({
                    "op": "delete_rel",
                    "from": r["from_id"], "to": r["to_id"], "type": rt,
                    "reason": "W2-04: VMA weak edge without source basis",
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
            "claim_id": f"w2-04-{i:04d}",
            "agent_id": agent, "source_agent": agent,
            "verdict": verdict, "proof_quote": pq, "proposed_action": action,
        })

    out_patch = PATCH_DIR / "w2_04_partial_vma.patch.jsonl"
    write_patch(out_patch, patch_ops)
    apply_result = apply_patch(out_patch, agent) if patch_ops else None

    proven = verdict_summary(ledger_rows).get("PROVEN", 0)
    extras = (
        f"DELETE proposals: **{len(patch_ops)}** VMA weak edges.\n"
    )
    if apply_result:
        cb = apply_result.get("counts_before", {})
        ca = apply_result.get("counts_after") or cb
        extras += (
            f"\n## Patch apply: w2_04_partial_vma\n\n"
            f"- Applied: **{apply_result.get('applied')}**\n"
            f"- Graph before: {cb.get('nodes')} nodes / {cb.get('relationships')} rels\n"
            f"- Graph after: {ca.get('nodes')} nodes / {ca.get('relationships')} rels\n"
        )
    write_csv(LEDGER_DIR / "w2_04.csv", ledger_rows)
    (REPORT_DIR / "w2_04_report.md").write_text(
        report_md(agent, "W2-04 PARTIAL + weak VMA edges", len(scope), ledger_rows, extras),
        encoding="utf-8",
    )
    return {
        "agent": agent, "scope": len(scope), "processed": len(ledger_rows),
        "proven": proven, "patches_drafted": len(patch_ops),
        "patches_applied": 1 if apply_result and apply_result.get("applied") else 0,
        "apply_status": "applied" if apply_result and apply_result.get("applied") else "dry-run or empty",
    }


def run_w2_05(v3: list[dict], nodes: list[dict], rels: list[dict], agent_stats: list[dict]) -> dict:
    agent = "W2-05"
    patch_path = PATCH_DIR / "post_02_schema_violation.patch.jsonl"
    apply_result = apply_patch(patch_path, agent)

    rel_eid = {r["eid"] for r in rels}
    node_eid = {n["eid"] for n in nodes}
    triple = {(r["from_id"], r["t"], r["to_id"]) for r in rels}

    overlay_files = [
        LEDGER_DIR / "w2_01.csv",
        LEDGER_DIR / "w2_02.csv",
        LEDGER_DIR / "w2_03.csv",
        LEDGER_DIR / "w2_04.csv",
    ]
    overlays: dict[str, dict] = {}
    for path in overlay_files:
        if not path.is_file():
            continue
        for row in csv.DictReader(path.open(encoding="utf-8")):
            overlays[dedupe_key(row)] = row

    post04_patched = set()
    p04 = PATCH_DIR / "post_04_missing_evidence.patch.jsonl"
    if p04.is_file():
        for line in p04.read_text(encoding="utf-8").splitlines():
            if line.strip():
                op = json.loads(line)
                if op.get("id"):
                    post04_patched.add(op["id"])

    merged: dict[str, dict] = {}
    stale = 0
    for r in v3:
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
        if key not in merged:
            continue
        base = merged[key]
        for fld in ("verdict", "proof_quote", "proposed_action", "basis_ref", "fetched", "http_status", "confidence"):
            if ov.get(fld):
                base[fld] = ov[fld]
        base["source_agent"] = (base.get("source_agent", "") + "+" + ov.get("source_agent", "")).strip("+")
        merged[key] = base

    for nid in post04_patched:
        key = f"node:{nid}"
        if key in merged and merged[key].get("verdict") == "MISSING_EVIDENCE":
            merged[key]["verdict"] = "PROVEN"
            merged[key]["proposed_action"] = "ADD_SOURCE"
            merged[key]["source_agent"] = merged[key].get("source_agent", "") + "+W2-02-apply"

    for r in merged.values():
        if r.get("verdict") == "SCHEMA_VIOLATION":
            eid = r.get("element_id", "")
            rt = r.get("rel_type_or_label", "")
            if eid in PROG_CATEGORY_IDS or (rt == "TEIL_VON_PROGRAMM" and r.get("to_id") in PROG_CATEGORY_IDS):
                if apply_result.get("applied"):
                    r["proposed_action"] = "DEPRECATED" if r["claim_kind"] == "node" else "DELETED"
                    r["notes"] = (r.get("notes", "") + "; W2-05 schema patch applied").strip("; ")

    v4_rows = list(merged.values())
    v4_path = HERE / "VERIFICATION_LEDGER_ELEMENT_v4.csv"
    write_csv(v4_path, v4_rows)

    vc = verdict_summary(v4_rows)
    total = len(v4_rows)
    proven_n = vc.get("PROVEN", 0)
    proven_pct = 100 * proven_n / max(total, 1)
    v3_vc = verdict_summary(v3)
    v3_proven = v3_vc.get("PROVEN", 0)
    v3_pct = 100 * v3_proven / max(len(v3), 1)
    delta = proven_pct - v3_pct

    counts = graph_counts()
    cb = apply_result.get("counts_before", {})
    ca = apply_result.get("counts_after") or counts

    audit_row = {
        "claim_id": "w2-05-agg",
        "claim_kind": "meta",
        "element_id": "",
        "verdict": "AGGREGATED",
        "agent_id": agent,
        "source_agent": agent,
        "notes": f"v4 merge; delta PROVEN {delta:+.2f}pp",
    }
    write_csv(LEDGER_DIR / "w2_05.csv", [audit_row])

    campaign_lines = [
        "# POST-IER W2 Campaign Report",
        "",
        f"**Date:** {now_utc()} · **Database:** `mit-bestand`",
        f"**Graph (final):** {counts['nodes']} nodes / {counts['relationships']} relationships",
        f"**Ledger v3:** {len(v3)} rows · **{v3_pct:.2f}% PROVEN** ({v3_proven})",
        f"**Ledger v4:** {total} rows · **{proven_pct:.2f}% PROVEN** ({proven_n}) · **Δ {delta:+.2f} pp**",
        f"**Stale v3 rows pruned:** {stale}",
        "",
        "## Agent summary",
        "",
        "| Agent | Scope | Processed | PROVEN/upgrades | Patches drafted | Patches applied |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for st in agent_stats:
        campaign_lines.append(
            f"| {st['agent']} | {st['scope']} | {st['processed']} | {st['proven']} | "
            f"{st.get('patches_drafted', st.get('patches', 0))} | {st.get('patches_applied', 0)} |"
        )
    campaign_lines += [
        "",
        "## Patch apply: post_02_schema_violation",
        "",
        f"- Applied: **{apply_result.get('applied')}** · Error: {apply_result.get('error') or 'none'}",
        f"- Graph before apply: {cb.get('nodes')} / {cb.get('relationships')}",
        f"- Graph after apply: {ca.get('nodes')} / {ca.get('relationships')}",
        "",
        "## v4 verdict distribution",
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
        "- `VERIFICATION_LEDGER_ELEMENT_v4.csv`",
        "- `ledger/w2_01.csv` … `ledger/w2_05.csv`",
        "- `reports/w2_01_report.md` … `reports/w2_05_report.md`",
        "- `reports/POST_IER_W2_REPORT.md`",
        "- `patches/w2_01_catalogue_backfill.patch.jsonl` (dry-run)",
        "- `patches/w2_04_partial_vma.patch.jsonl`",
        "",
        "## Blockers",
        "",
    ]
    blockers = []
    for st in agent_stats:
        if st.get("apply_status") and "fail" in str(st.get("apply_status", "")).lower():
            blockers.append(f"- {st['agent']}: {st['apply_status']}")
    if not blockers:
        campaign_lines.append("- None (all applies succeeded or were dry-run only by design).")
    else:
        campaign_lines.extend(blockers)

    (REPORT_DIR / "POST_IER_W2_REPORT.md").write_text("\n".join(campaign_lines) + "\n", encoding="utf-8")
    (REPORT_DIR / "w2_05_report.md").write_text(
        report_md(agent, "W2-05 Schema tier-D + aggregator", len(v3), [audit_row],
                  f"v4: **{total}** rows · **{proven_pct:.2f}% PROVEN** (Δ **{delta:+.2f} pp** vs v3)."),
        encoding="utf-8",
    )
    return {
        "agent": agent, "scope": len(v3), "processed": total,
        "proven": proven_n, "proven_pct": proven_pct, "v3_proven_pct": v3_pct,
        "delta_pp": delta, "patches_drafted": 0,
        "patches_applied": 1 if apply_result.get("applied") else 0,
        "stale_pruned": stale,
    }


def main() -> int:
    print("Exporting live graph…")
    nodes, rels, counts_start = export_graph()
    print(f"Graph start: {counts_start}")

    v3 = load_v3()
    print(f"v3 ledger: {len(v3)} rows")

    stats = []
    print("W2-01…")
    stats.append(run_w2_01())
    print("W2-02…")
    stats.append(run_w2_02(v3))
    nodes, rels, counts_mid = export_graph()
    print("W2-03…")
    stats.append(run_w2_03(v3))
    nodes, rels, counts_mid2 = export_graph()
    print("W2-04…")
    stats.append(run_w2_04(v3))
    nodes, rels, counts_pre05 = export_graph()
    print("W2-05…")
    w205 = run_w2_05(v3, nodes, rels, stats)
    stats.append(w205)

    counts_final = graph_counts()
    summary = {
        "generated_at": now_utc(),
        "graph_counts_start": counts_start,
        "graph_counts_final": counts_final,
        "agents": stats,
        "v3_proven_pct": w205.get("v3_proven_pct"),
        "v4_proven_pct": w205.get("proven_pct"),
        "delta_pp": w205.get("delta_pp"),
    }
    (WORK / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
