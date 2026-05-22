#!/usr/bin/env python3
"""Post-IER W3 10-agent verification wave (W3-01 … W3-10).

Read-only on Neo4j except non-destructive patch apply after dry-run pass.
DELETE patches are drafted only — never auto-applied.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
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

V4 = HERE / "VERIFICATION_LEDGER_ELEMENT_v4.csv"
LEDGER_DIR = HERE / "ledger"
REPORT_DIR = HERE / "reports"
PATCH_DIR = HERE / "patches"
WORK = HERE / "_post_ier_w3_work"
for d in (LEDGER_DIR, REPORT_DIR, PATCH_DIR, WORK):
    d.mkdir(parents=True, exist_ok=True)

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status",
    "verdict", "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
    "source_agent", "coverage_level", "graph_element_id", "match_status",
]
REVIEW_RUN = "post_ier_w3_2026_06_07"

CATALOGUE_BATCHES = [
    ("W3-01", 500, 190, "w3_01"),
    ("W3-02", 690, 190, "w3_02"),
    ("W3-03", 880, 190, "w3_03"),
    ("W3-04", 1070, 500, "w3_04"),
]

UPGRADE_OPS = {"set_rel_properties", "set_node_properties"}
DELETE_OPS = {"delete_rel", "delete_node"}

_q04_path = HERE / "_agent_q04_catalogue_edges.py"
_spec = importlib.util.spec_from_file_location("q04", _q04_path)
q04 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(q04)  # type: ignore[union-attr]

_q05_path = HERE / "_quality_pass_q05.py"
_spec5 = importlib.util.spec_from_file_location("q05", _q05_path)
q05 = importlib.util.module_from_spec(_spec5)
_spec5.loader.exec_module(q05)  # type: ignore[union-attr]

PROG_CATEGORY_IDS = {
    "prog_foerderprogramm", "prog_forschungsprojekt", "prog_pilotprojekt",
    "prog_reallabor", "prog_wettbewerb",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_v4() -> list[dict]:
    return list(csv.DictReader(V4.open(encoding="utf-8")))


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


def split_patch_ops(ops: list[dict]) -> tuple[list[dict], list[dict]]:
    upgrades, deletes = [], []
    for op in ops:
        if op.get("op") in UPGRADE_OPS:
            upgrades.append(op)
        elif op.get("op") in DELETE_OPS:
            deletes.append(op)
    return upgrades, deletes


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
            for row in s.run(
                "MATCH (n) RETURN n.id AS id, elementId(n) AS eid, labels(n) AS labels, n.name AS name"
            ):
                nodes.append(dict(row))
            for row in s.run(
                "MATCH (a)-[r]->(b) RETURN elementId(r) AS eid, type(r) AS t, "
                "a.id AS from_id, b.id AS to_id, a.name AS from_name, b.name AS to_name, "
                "properties(r) AS props"
            ):
                rels.append(dict(row))
    counts = {"nodes": len(nodes), "relationships": len(rels), "database": database}
    (WORK / "graph_counts.json").write_text(json.dumps(counts, indent=2), encoding="utf-8")
    driver.close()
    return nodes, rels, counts


def apply_patch(patch_path: Path, agent: str, auto_apply: bool = True) -> dict:
    """Dry-run patch; auto-apply upgrade ops only when auto_apply=True."""
    rel = patch_path.relative_to(REPO).as_posix()
    name = patch_path.name
    result = {
        "agent": agent,
        "patch": rel,
        "dry_run_ok": False,
        "applied": False,
        "upgrade_ops": 0,
        "delete_ops_drafted": 0,
        "error": "",
        "counts_before": graph_counts(),
        "counts_after": None,
    }
    if not patch_path.is_file() or patch_path.stat().st_size == 0:
        result["error"] = "patch missing or empty"
        return result

    all_ops = [json.loads(line) for line in patch_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    upgrades, deletes = split_patch_ops(all_ops)
    result["upgrade_ops"] = len(upgrades)
    result["delete_ops_drafted"] = len(deletes)

    apply_path = patch_path
    if deletes and not upgrades:
        dry = subprocess.run(
            [sys.executable, str(SCRIPTS / "apply_neo4j_review_patch.py"), "--patch", rel],
            cwd=str(REPO), capture_output=True, text=True,
        )
        (WORK / f"{agent}_dry_run.txt").write_text(dry.stdout + dry.stderr, encoding="utf-8")
        result["dry_run_ok"] = dry.returncode == 0
        result["error"] = "DELETE-only patch — drafted, not applied (W3 policy)"
        return result

    if deletes and upgrades:
        apply_path = WORK / f"{agent}_upgrades_only.patch.jsonl"
        write_patch(apply_path, upgrades)
        rel = apply_path.relative_to(REPO).as_posix()
        name = apply_path.name

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

    if not auto_apply or not upgrades:
        result["error"] = "dry-run only" if not upgrades else "auto_apply disabled"
        return result

    confirm = f"APPLY {name} TO mit-bestand"
    live = subprocess.run(
        [sys.executable, str(SCRIPTS / "apply_neo4j_review_patch.py"), "--patch", rel, "--confirm", confirm],
        cwd=str(REPO), capture_output=True, text=True,
    )
    (WORK / f"{agent}_apply.txt").write_text(live.stdout + live.stderr, encoding="utf-8")
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
           r.evidence_url AS evidence_url,
           coalesce(r.source_url, r.evidence_url) AS source_url
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


def query_vma_weak() -> list[dict]:
    driver, database = neo4j_session()
    rows = []
    cypher = """
    MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
    WHERE coalesce(r.evidence_quote,'') = '' AND coalesce(r.evidence_url,'') = ''
    RETURN elementId(r) AS element_id, a.id AS from_id, a.name AS from_name,
           b.id AS to_id, b.name AS to_name, type(r) AS rel_type,
           coalesce(a.primary_source_url, head(coalesce(a.source_urls,[]))) AS actor_primary_url,
           coalesce(b.primary_source_url, head(coalesce(b.source_urls,[]))) AS target_primary_url,
           coalesce(a.source_urls,[]) AS actor_source_urls,
           coalesce(b.source_urls,[]) AS target_source_urls
    ORDER BY from_id, to_id
    """
    with driver:
        with driver.session(database=database, default_access_mode="READ") as s:
            for row in s.run(cypher):
                rows.append(dict(row))
    driver.close()
    return rows


def dedupe_key(row: dict) -> str:
    geid = (row.get("graph_element_id") or "").strip()
    if geid:
        return f"{row.get('claim_kind','')}:{geid}"
    kind = row.get("claim_kind", "")
    if kind == "rel":
        return f"rel:{row.get('from_id')}|{row.get('rel_type_or_label')}|{row.get('to_id')}"
    return f"node:{row.get('element_id', '')}"


def first_alpha(eid: str) -> str:
    for c in (eid or "").lower():
        if c.isalpha():
            return c
    return "z"


def fetch_simple(url: str, cache: dict) -> dict:
    return q04.fetch_url(url, cache)


def run_catalogue_agent(agent: str, offset: int, limit: int, slug: str, cache: dict) -> dict:
    batch, scope_total = query_catalogue_batch(offset, limit)
    vocab_names = q04.load_vocab_names()
    enrich_idx = q04.load_enrichment_index()

    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []
    delete_ops: list[dict] = []

    for n, live in enumerate(batch, 1):
        fid, tid, rt = live["from_id"], live["to_id"], live["rel_type"]
        pseudo = {
            "from_id": fid, "to_id": tid, "rel_type_or_label": rt,
            "verdict": "PARTIAL", "basis_ref": live.get("source_url") or "", "fetched": "false",
            "http_status": "", "confidence": "teilweise_belegt",
        }
        ev = q04.evaluate_row(pseudo, None, enrich_idx, vocab_names, live, cache)
        verdict = ev["verdict_after"]
        action = ev["proposed_action"]
        if verdict == "UNSUPPORTED" or action == "DELETE":
            action = "DELETE"
            verdict = "UNSUPPORTED"
            delete_ops.append({
                "op": "delete_rel", "from": fid, "to": tid, "type": rt,
                "reason": f"{agent} strict gate: no verbatim catalogue quote",
            })

        row = {
            "claim_id": f"{slug}-{n:04d}",
            "claim_kind": "rel",
            "element_id": live["element_id"],
            "from_id": fid, "to_id": tid, "rel_type_or_label": rt,
            "asserted_claim": f"{fid} —[{rt}]→ {tid} (catalogue W3)",
            "basis_type": "web" if str(ev.get("basis_ref", "")).startswith("http") else "logic",
            "basis_ref": ev.get("basis_ref", ""),
            "fetched": ev.get("fetched", "false"),
            "http_status": ev.get("http_status", ""),
            "verdict": verdict,
            "confidence": ev.get("confidence", ""),
            "proof_quote": ev.get("proof_quote", ""),
            "proposed_action": action,
            "agent_id": agent,
            "notes": ev.get("notes", "") or f"{agent} offset={offset} strict gate",
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
                    "evidence_basis": f"{slug}_web_fetch",
                    "review_run": REVIEW_RUN,
                    "semantic_basis": "catalog_extension",
                },
                "reason": f"{agent} strict-gate upgrade for {fid}->{tid}",
            })

    out_csv = LEDGER_DIR / f"{slug}.csv"
    out_md = REPORT_DIR / f"{slug}_report.md"
    out_patch = PATCH_DIR / f"{slug}_catalogue_backfill.patch.jsonl"
    all_patch = patch_ops + delete_ops
    write_csv(out_csv, ledger_rows)
    write_patch(out_patch, all_patch)
    apply_result = apply_patch(out_patch, agent) if all_patch else None

    remainder = max(scope_total - offset - len(batch), 0)
    extras = (
        f"## Batch position\n\n"
        f"Offset **{offset}** · processed **{len(batch)}** · remainder after batch: **~{remainder}** "
        f"(total empty-quote catalogue rels: **{scope_total}**).\n\n"
        f"Upgrades drafted: **{len(patch_ops)}** · DELETE drafted: **{len(delete_ops)}** (not applied).\n"
    )
    if apply_result:
        cb = apply_result.get("counts_before", {})
        ca = apply_result.get("counts_after") or cb
        extras += (
            f"\n## Patch apply\n\n"
            f"- Dry-run OK: **{apply_result.get('dry_run_ok')}**\n"
            f"- Upgrades applied: **{apply_result.get('applied')}**\n"
            f"- DELETE ops drafted (not applied): **{apply_result.get('delete_ops_drafted')}**\n"
            f"- Graph before: {cb.get('nodes')} / {cb.get('relationships')}\n"
            f"- Graph after: {ca.get('nodes')} / {ca.get('relationships')}\n"
        )
    out_md.write_text(
        report_md(agent, f"{agent} Catalogue backfill", scope_total, ledger_rows, extras),
        encoding="utf-8",
    )
    vc = verdict_summary(ledger_rows)
    return {
        "agent": agent, "scope": scope_total, "processed": len(batch),
        "proven": vc.get("PROVEN", 0),
        "unsupported": vc.get("UNSUPPORTED", 0),
        "patches_drafted": len(all_patch),
        "upgrades_drafted": len(patch_ops),
        "deletes_drafted": len(delete_ops),
        "patches_applied": 1 if apply_result and apply_result.get("applied") else 0,
        "apply_status": "applied" if apply_result and apply_result.get("applied") else (
            apply_result.get("error", "none") if apply_result else "empty"
        ),
    }


def run_w3_05(cache: dict) -> dict:
    agent = "W3-05"
    slug = "w3_05"
    batch = query_vma_weak()
    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []
    delete_ops: list[dict] = []

    for n, live in enumerate(batch, 1):
        fid, tid, rt = live["from_id"], live["to_id"], live["rel_type"]
        from_name = live.get("from_name") or fid
        to_name = live.get("to_name") or tid
        urls: list[str] = []
        key = (rt, fid, tid)
        for u in q05.VMA_CANDIDATES.get(key, []):
            if u not in urls:
                urls.append(u)
        for src in (
            live.get("actor_primary_url"),
            live.get("target_primary_url"),
        ):
            if src and str(src).startswith("http") and src not in urls:
                urls.append(str(src))
        for u in (live.get("actor_source_urls") or []) + (live.get("target_source_urls") or []):
            if u and u.startswith("http") and u not in urls:
                urls.append(u)

        verdict, pq, hit_url, fetched, status = "UNSUPPORTED", "", "", "false", ""
        action = "DELETE"
        for url in urls[:5]:
            fe = fetch_simple(url, cache)
            if not fe.get("fetched"):
                continue
            fetched = "true"
            status = fe.get("http_status", "")
            ok, quote = q05.actor_org_affiliation(fid, from_name, tid, to_name, fe.get("text", ""))
            if ok and quote:
                verdict, pq, hit_url, action = "PROVEN", quote, url, "UPGRADE"
                break

        row = {
            "claim_id": f"{slug}-{n:04d}",
            "claim_kind": "rel",
            "element_id": live["element_id"],
            "from_id": fid, "to_id": tid, "rel_type_or_label": rt,
            "asserted_claim": f"{fid} —[{rt}]→ {tid} (live VMA weak)",
            "basis_type": "web" if hit_url else "none",
            "basis_ref": hit_url,
            "fetched": fetched, "http_status": status,
            "verdict": verdict,
            "confidence": "belegt" if verdict == "PROVEN" else "unbelegt",
            "proof_quote": pq,
            "proposed_action": action,
            "agent_id": agent,
            "notes": f"live graph scan; urls_tried={len(urls)}",
            "source_agent": agent,
            "coverage_level": "element",
            "graph_element_id": live["element_id"],
            "match_status": "rel",
        }
        ledger_rows.append(row)
        if action == "UPGRADE" and pq:
            patch_ops.append({
                "op": "set_rel_properties",
                "from": fid, "to": tid, "type": rt,
                "properties": {
                    "evidence_url": hit_url,
                    "evidence_quote": pq[:500],
                    "evidence_confidence": "belegt",
                    "evidence_basis": "w3_05_vma_web",
                    "review_run": REVIEW_RUN,
                },
                "reason": f"W3-05 VMA upgrade {fid}->{tid}",
            })
        else:
            delete_ops.append({
                "op": "delete_rel", "from": fid, "to": tid, "type": rt,
                "reason": f"W3-05: VMA without two-endpoint web proof",
            })

    out_patch = PATCH_DIR / f"{slug}_vma.patch.jsonl"
    write_csv(LEDGER_DIR / f"{slug}.csv", ledger_rows)
    write_patch(out_patch, patch_ops + delete_ops)
    apply_result = apply_patch(out_patch, agent) if (patch_ops or delete_ops) else None

    extras = f"Live VMA weak edges: **{len(batch)}** · upgrades **{len(patch_ops)}** · DELETE drafted **{len(delete_ops)}**\n"
    if apply_result:
        extras += f"Upgrades applied: **{apply_result.get('applied')}**\n"
    (REPORT_DIR / f"{slug}_report.md").write_text(
        report_md(agent, "W3-05 VMA weak edges (live graph)", len(batch), ledger_rows, extras),
        encoding="utf-8",
    )
    vc = verdict_summary(ledger_rows)
    return {
        "agent": agent, "scope": len(batch), "processed": len(batch),
        "proven": vc.get("PROVEN", 0), "unsupported": vc.get("UNSUPPORTED", 0),
        "patches_drafted": len(patch_ops) + len(delete_ops),
        "upgrades_drafted": len(patch_ops), "deletes_drafted": len(delete_ops),
        "patches_applied": 1 if apply_result and apply_result.get("applied") else 0,
        "apply_status": apply_result.get("error", "none") if apply_result else "empty",
    }


def run_missing_evidence(agent: str, slug: str, v4: list[dict], bucket: str, cache: dict) -> dict:
    scope = [r for r in v4 if r["verdict"] == "MISSING_EVIDENCE"]
    if bucket == "a-m":
        batch = [r for r in scope if first_alpha(r.get("element_id", "")) <= "m"]
    else:
        batch = [r for r in scope if first_alpha(r.get("element_id", "")) > "m"]

    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []
    domain_re = re.compile(r"([a-z0-9][-a-z0-9]*\.[a-z]{2,}(?:\.[a-z]{2,})?)", re.I)

    for i, r in enumerate(batch, 1):
        basis = (r.get("basis_ref") or "").strip()
        notes = r.get("notes", "")
        eid = r.get("element_id", "")
        urls: list[str] = []
        if basis.startswith("http"):
            urls.append(basis)
        hints = q05.PROJECT_SOURCE_HINTS.get(eid, [])
        for u in hints:
            if u not in urls:
                urls.append(u)
        for m in domain_re.finditer(notes + " " + r.get("asserted_claim", "")):
            d = m.group(1).lower()
            if d not in ("e.g", "etc"):
                u = f"https://www.{d}/"
                if u not in urls:
                    urls.append(u)
        if eid.startswith("prog_") and "https://ec.europa.eu/" not in urls:
            urls.append("https://ec.europa.eu/info/funding-tenders/opportunities/portal/")

        verdict, pq, fetched, status = "MISSING_EVIDENCE", "", "false", ""
        hit_url = ""
        for url in urls[:4]:
            fe = fetch_simple(url, cache)
            text = fe.get("text") or ""
            if not fe.get("fetched"):
                continue
            status = fe.get("http_status", "")
            fetched = "true"
            plain = q04.strip_html(text)
            name = eid if r["claim_kind"] == "node" else r.get("from_id", "")
            tokens = [t for t in re.split(r"[\s_]+", name.replace("prog_", "").replace("bw_", "")) if len(t) >= 4]
            for sent in re.split(r"(?<=[.!?])\s+", plain):
                sn = q04.norm_text(sent)
                if any(q04.norm_text(t) in sn for t in tokens[:4]) and q04.is_valid_quote(sent):
                    verdict, pq, hit_url = "PROVEN", sent.strip()[:300], url
                    break
            if verdict == "PROVEN":
                break

        row = {
            **{k: r.get(k, "") for k in LEDGER_COLS if k in r},
            "claim_id": f"{slug}-{i:04d}",
            "agent_id": agent, "source_agent": agent,
            "verdict": verdict,
            "basis_ref": hit_url or basis,
            "fetched": fetched, "http_status": status,
            "proof_quote": pq,
            "proposed_action": "ADD_SOURCE" if verdict == "PROVEN" else r.get("proposed_action", "ADD_SOURCE"),
            "confidence": "belegt" if verdict == "PROVEN" else r.get("confidence", ""),
            "notes": (r.get("notes", "") + f"; {agent} web ladder").strip("; "),
        }
        ledger_rows.append(row)
        if verdict == "PROVEN" and r["claim_kind"] == "node" and hit_url:
            patch_ops.append({
                "op": "set_node_properties", "id": eid,
                "properties": {
                    "primary_source_url": hit_url,
                    "source_urls": [hit_url],
                    "source_quote": pq[:500],
                    "review_run": REVIEW_RUN,
                },
                "reason": f"{agent} recovery for {eid}",
            })

    out_patch = PATCH_DIR / f"{slug}_missing_evidence.patch.jsonl"
    write_csv(LEDGER_DIR / f"{slug}.csv", ledger_rows)
    write_patch(out_patch, patch_ops)
    apply_result = apply_patch(out_patch, agent) if patch_ops else None

    proven = verdict_summary(ledger_rows).get("PROVEN", 0)
    extras = f"Bucket **{bucket}** · scope **{len(batch)}** / total MISSING **{len(scope)}** · new PROVEN **{proven}**\n"
    if apply_result:
        extras += f"Patches applied: **{apply_result.get('applied')}**\n"
    (REPORT_DIR / f"{slug}_report.md").write_text(
        report_md(agent, f"{agent} MISSING_EVIDENCE ({bucket})", len(scope), ledger_rows, extras),
        encoding="utf-8",
    )
    return {
        "agent": agent, "scope": len(scope), "processed": len(batch),
        "proven": proven, "unsupported": 0,
        "patches_drafted": len(patch_ops), "upgrades_drafted": len(patch_ops), "deletes_drafted": 0,
        "patches_applied": 1 if apply_result and apply_result.get("applied") else 0,
        "apply_status": apply_result.get("error", "none") if apply_result else "empty",
    }


def run_w3_08(v4: list[dict], cache: dict) -> dict:
    agent = "W3-08"
    slug = "w3_08"
    scope = [r for r in v4 if r["verdict"] == "PARTIAL"]
    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []
    delete_ops: list[dict] = []

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
        elif rt == "VERBUNDEN_MIT_AKTEUR" and r["claim_kind"] == "rel":
            fid = r.get("from_id", "")
            if not basis.startswith("http") or "category inference" in notes.lower():
                action, verdict = "DELETE", "UNSUPPORTED"
                delete_ops.append({
                    "op": "delete_rel",
                    "from": r["from_id"], "to": r["to_id"], "type": rt,
                    "reason": "W3-08: unsupported VMA without web basis",
                })
        elif basis.startswith("http") and r["claim_kind"] == "node":
            fe = fetch_simple(basis, cache)
            if fe.get("fetched"):
                plain = q04.strip_html(fe.get("text", ""))
                name_tok = q04.norm_text(eid.replace("p_", "").replace("bw_", "").replace("_", " "))
                for sent in re.split(r"(?<=[.!?])\s+", plain):
                    if name_tok[:10] in q04.norm_text(sent) and q04.is_valid_quote(sent):
                        verdict, pq, action = "PROVEN", sent.strip()[:300], "KEEP"
                        patch_ops.append({
                            "op": "set_node_properties", "id": eid,
                            "properties": {
                                "primary_source_url": basis,
                                "source_quote": pq[:500],
                                "review_run": REVIEW_RUN,
                            },
                            "reason": f"W3-08 PARTIAL upgrade {eid}",
                        })
                        break
        elif basis.startswith("http") and r["claim_kind"] == "rel":
            fe = fetch_simple(basis, cache)
            if fe.get("fetched") and rt == "VERBUNDEN_MIT_AKTEUR":
                ok, quote = q05.actor_org_affiliation(
                    r["from_id"], r.get("from_id", ""), r["to_id"], r.get("to_id", ""), fe.get("text", "")
                )
                if ok and quote:
                    verdict, pq, action = "PROVEN", quote, "UPGRADE"
                    patch_ops.append({
                        "op": "set_rel_properties",
                        "from": r["from_id"], "to": r["to_id"], "type": rt,
                        "properties": {
                            "evidence_url": basis,
                            "evidence_quote": quote[:500],
                            "evidence_confidence": "belegt",
                            "review_run": REVIEW_RUN,
                        },
                        "reason": f"W3-08 VMA upgrade",
                    })

        ledger_rows.append({
            **{k: r.get(k, "") for k in LEDGER_COLS if k in r},
            "claim_id": f"{slug}-{i:04d}",
            "agent_id": agent, "source_agent": agent,
            "verdict": verdict, "proof_quote": pq, "proposed_action": action,
        })

    out_patch = PATCH_DIR / f"{slug}_partial.patch.jsonl"
    write_csv(LEDGER_DIR / f"{slug}.csv", ledger_rows)
    write_patch(out_patch, patch_ops + delete_ops)
    apply_result = apply_patch(out_patch, agent) if (patch_ops or delete_ops) else None

    vc = verdict_summary(ledger_rows)
    extras = f"DELETE drafted: **{len(delete_ops)}** · upgrades drafted: **{len(patch_ops)}**\n"
    (REPORT_DIR / f"{slug}_report.md").write_text(
        report_md(agent, "W3-08 PARTIAL residual", len(scope), ledger_rows, extras),
        encoding="utf-8",
    )
    return {
        "agent": agent, "scope": len(scope), "processed": len(ledger_rows),
        "proven": vc.get("PROVEN", 0), "unsupported": vc.get("UNSUPPORTED", 0),
        "patches_drafted": len(patch_ops) + len(delete_ops),
        "upgrades_drafted": len(patch_ops), "deletes_drafted": len(delete_ops),
        "patches_applied": 1 if apply_result and apply_result.get("applied") else 0,
        "apply_status": apply_result.get("error", "none") if apply_result else "empty",
    }


def run_w3_09(v4: list[dict]) -> dict:
    agent = "W3-09"
    slug = "w3_09"
    contra = [r for r in v4 if r["verdict"] == "CONTRADICTION"]
    schema = [r for r in v4 if r["verdict"] == "SCHEMA_VIOLATION"]
    unver_persons = [
        r for r in v4
        if r["verdict"] == "UNVERIFIABLE" and r.get("element_id", "").startswith("p_")
    ]
    scope = contra + schema + unver_persons

    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []

    for i, r in enumerate(scope, 1):
        verdict = r["verdict"]
        action = r.get("proposed_action", "ESCALATE_HUMAN")
        notes = r.get("notes", "")

        if verdict == "CONTRADICTION":
            action = "FIX_PROPERTY"
            notes = (notes + "; W3-09 human-merge proposal for geo contradiction").strip("; ")
        elif verdict == "SCHEMA_VIOLATION":
            eid = r.get("element_id", "")
            if eid in PROG_CATEGORY_IDS or r.get("to_id") in PROG_CATEGORY_IDS:
                action = "DEPRECATED" if r["claim_kind"] == "node" else "DELETED"
            else:
                action = "ESCALATE_HUMAN"
            notes = (notes + "; W3-09 tier-D schema review").strip("; ")
        elif verdict == "UNVERIFIABLE":
            action = "DEPRECATE"
            notes = (notes + "; W3-09 person node unverifiable — deprecate proposal").strip("; ")
            if r["claim_kind"] == "node":
                patch_ops.append({
                    "op": "set_node_properties",
                    "id": r["element_id"],
                    "properties": {"review_status": "deprecated_unverifiable", "review_run": REVIEW_RUN},
                    "reason": f"W3-09 deprecate unverifiable person {r['element_id']}",
                })

        ledger_rows.append({
            **{k: r.get(k, "") for k in LEDGER_COLS if k in r},
            "claim_id": f"{slug}-{i:04d}",
            "agent_id": agent, "source_agent": agent,
            "proposed_action": action, "notes": notes,
        })

    out_patch = PATCH_DIR / f"{slug}_tier_d.patch.jsonl"
    write_csv(LEDGER_DIR / f"{slug}.csv", ledger_rows)
    write_patch(out_patch, patch_ops)
    apply_result = apply_patch(out_patch, agent) if patch_ops else None

    extras = (
        f"CONTRADICTION: **{len(contra)}** · SCHEMA: **{len(schema)}** · "
        f"UNVERIFIABLE persons: **{len(unver_persons)}**\n"
        f"Deprecate patches drafted: **{len(patch_ops)}** (non-destructive node props only)\n"
    )
    (REPORT_DIR / f"{slug}_report.md").write_text(
        report_md(agent, "W3-09 CONTRADICTION + SCHEMA + UNVERIFIABLE persons", len(scope), ledger_rows, extras),
        encoding="utf-8",
    )
    return {
        "agent": agent, "scope": len(scope), "processed": len(ledger_rows),
        "proven": 0, "unsupported": 0,
        "patches_drafted": len(patch_ops), "upgrades_drafted": len(patch_ops), "deletes_drafted": 0,
        "patches_applied": 1 if apply_result and apply_result.get("applied") else 0,
        "apply_status": apply_result.get("error", "none") if apply_result else "empty",
    }


def run_w3_10(v4: list[dict], nodes: list[dict], rels: list[dict], agent_stats: list[dict]) -> dict:
    agent = "W3-10"
    rel_eid = {r["eid"] for r in rels}
    node_eid = {n["eid"] for n in nodes}
    triple = {(r["from_id"], r["t"], r["to_id"]) for r in rels}

    overlay_files = [LEDGER_DIR / f"w3_{i:02d}.csv" for i in range(1, 10)]
    overlays: dict[str, dict] = {}
    for path in overlay_files:
        if not path.is_file():
            continue
        for row in csv.DictReader(path.open(encoding="utf-8")):
            overlays[dedupe_key(row)] = row

    merged: dict[str, dict] = {}
    stale = 0
    for r in v4:
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
            if ov.get("claim_kind") == "rel" and ov.get("graph_element_id"):
                merged[key] = dict(ov)
            continue
        base = merged[key]
        for fld in ("verdict", "proof_quote", "proposed_action", "basis_ref", "fetched", "http_status", "confidence"):
            if ov.get(fld):
                base[fld] = ov[fld]
        base["source_agent"] = (base.get("source_agent", "") + "+" + ov.get("source_agent", "")).strip("+")
        merged[key] = base

    v5_rows = list(merged.values())
    v5_path = HERE / "VERIFICATION_LEDGER_ELEMENT_v5.csv"
    write_csv(v5_path, v5_rows)

    vc = verdict_summary(v5_rows)
    total = len(v5_rows)
    proven_n = vc.get("PROVEN", 0)
    proven_pct = 100 * proven_n / max(total, 1)
    v4_vc = verdict_summary(v4)
    v4_proven = v4_vc.get("PROVEN", 0)
    v4_pct = 100 * v4_proven / max(len(v4), 1)
    delta = proven_pct - v4_pct

    counts = graph_counts()
    audit_row = {
        "claim_id": "w3-10-agg",
        "claim_kind": "meta",
        "element_id": "",
        "verdict": "AGGREGATED",
        "agent_id": agent,
        "source_agent": agent,
        "notes": f"v5 merge; delta PROVEN {delta:+.2f}pp",
    }
    write_csv(LEDGER_DIR / "w3_10.csv", [audit_row])

    total_upgrades = sum(st.get("upgrades_drafted", 0) for st in agent_stats)
    total_deletes = sum(st.get("deletes_drafted", 0) for st in agent_stats)
    total_applied = sum(st.get("patches_applied", 0) for st in agent_stats)

    campaign_lines = [
        "# POST-IER W3 Campaign Report",
        "",
        f"**Date:** {now_utc()} · **Database:** `mit-bestand`",
        f"**Graph (final):** {counts['nodes']} nodes / {counts['relationships']} relationships",
        f"**Ledger v4:** {len(v4)} rows · **{v4_pct:.2f}% PROVEN** ({v4_proven})",
        f"**Ledger v5:** {total} rows · **{proven_pct:.2f}% PROVEN** ({proven_n}) · **Δ {delta:+.2f} pp**",
        f"**Stale v4 rows pruned:** {stale}",
        "",
        "## Agent summary",
        "",
        "| Agent | Scope | Processed | PROVEN | UNSUPPORTED | Upgrades drafted | DELETE drafted | Patches applied |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for st in agent_stats:
        campaign_lines.append(
            f"| {st['agent']} | {st['scope']} | {st['processed']} | {st.get('proven', 0)} | "
            f"{st.get('unsupported', 0)} | {st.get('upgrades_drafted', 0)} | "
            f"{st.get('deletes_drafted', 0)} | {st.get('patches_applied', 0)} |"
        )
    campaign_lines += [
        "",
        f"**Total upgrade ops drafted:** {total_upgrades} · **DELETE ops drafted (not applied):** {total_deletes}",
        f"**Patch apply rounds (upgrade-only):** {total_applied}",
        "",
        "## v5 verdict distribution",
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
        "- `VERIFICATION_LEDGER_ELEMENT_v5.csv`",
        "- `ledger/w3_01.csv` … `ledger/w3_10.csv`",
        "- `reports/w3_01_report.md` … `reports/w3_10_report.md`",
        "- `reports/POST_IER_W3_REPORT.md`",
        "- `patches/w3_01_catalogue_backfill.patch.jsonl` … `patches/w3_09_tier_d.patch.jsonl`",
        "",
        "## Apply policy",
        "",
        "- Non-destructive upgrades (`set_rel_properties`, `set_node_properties`) auto-applied when dry-run clean.",
        "- DELETE patches drafted only — **not applied** in W3.",
        "",
        "## Remaining blockers",
        "",
    ]
    blockers = []
    rem_unsup = vc.get("UNSUPPORTED", 0)
    rem_missing = vc.get("MISSING_EVIDENCE", 0)
    rem_partial = vc.get("PARTIAL", 0)
    rem_contra = vc.get("CONTRADICTION", 0)
    rem_unver = vc.get("UNVERIFIABLE", 0)
    if rem_unsup:
        blockers.append(f"- **UNSUPPORTED ({rem_unsup}):** catalogue strict-gate failures + VMA DELETE drafts pending human review.")
    if rem_missing:
        blockers.append(f"- **MISSING_EVIDENCE ({rem_missing}):** nodes without recoverable web source.")
    if rem_partial:
        blockers.append(f"- **PARTIAL ({rem_partial}):** weak entity gate or dossier-only address.")
    if rem_contra:
        blockers.append(f"- **CONTRADICTION ({rem_contra}):** geo human-merge proposals in w3_09.")
    if rem_unver:
        blockers.append(f"- **UNVERIFIABLE ({rem_unver}):** persons and opaque nodes.")
    if total_deletes:
        blockers.append(f"- **DELETE drafts ({total_deletes}):** require explicit approval before apply.")
    if not blockers:
        campaign_lines.append("- None.")
    else:
        campaign_lines.extend(blockers)

    (REPORT_DIR / "POST_IER_W3_REPORT.md").write_text("\n".join(campaign_lines) + "\n", encoding="utf-8")
    (REPORT_DIR / "w3_10_report.md").write_text(
        report_md(agent, "W3-10 Aggregator", len(v4), [audit_row],
                  f"v5: **{total}** rows · **{proven_pct:.2f}% PROVEN** (Δ **{delta:+.2f} pp** vs v4)."),
        encoding="utf-8",
    )
    return {
        "agent": agent, "scope": len(v4), "processed": total,
        "proven": proven_n, "proven_pct": proven_pct, "v4_proven_pct": v4_pct,
        "delta_pp": delta, "patches_drafted": 0,
        "patches_applied": 0, "stale_pruned": stale,
        "unsupported": vc.get("UNSUPPORTED", 0),
    }


def main() -> int:
    print("Exporting live graph…")
    nodes, rels, counts_start = export_graph()
    print(f"Graph start: {counts_start}")

    v4 = load_v4()
    print(f"v4 ledger: {len(v4)} rows")

    cache: dict = {}
    if q04.R07_CACHE.is_file():
        cache.update(json.loads(q04.R07_CACHE.read_text(encoding="utf-8")))

    stats = []
    for agent, offset, limit, slug in CATALOGUE_BATCHES:
        print(f"{agent}…")
        stats.append(run_catalogue_agent(agent, offset, limit, slug, cache))
        if len(cache) > 100:
            q04.R07_CACHE.parent.mkdir(parents=True, exist_ok=True)
            q04.R07_CACHE.write_text(json.dumps(cache, ensure_ascii=False)[:5_000_000], encoding="utf-8")

    print("W3-05…")
    stats.append(run_w3_05(cache))
    print("W3-06…")
    stats.append(run_missing_evidence("W3-06", "w3_06", v4, "a-m", cache))
    print("W3-07…")
    stats.append(run_missing_evidence("W3-07", "w3_07", v4, "n-z", cache))
    print("W3-08…")
    stats.append(run_w3_08(v4, cache))
    print("W3-09…")
    stats.append(run_w3_09(v4))

    nodes, rels, _ = export_graph()
    print("W3-10…")
    w310 = run_w3_10(v4, nodes, rels, stats)
    stats.append(w310)

    counts_final = graph_counts()
    summary = {
        "generated_at": now_utc(),
        "graph_counts_start": counts_start,
        "graph_counts_final": counts_final,
        "agents": stats,
        "v4_proven_pct": w310.get("v4_proven_pct"),
        "v5_proven_pct": w310.get("proven_pct"),
        "delta_pp": w310.get("delta_pp"),
    }
    (WORK / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
