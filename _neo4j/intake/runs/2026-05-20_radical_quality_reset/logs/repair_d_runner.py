"""Repair Agent D runner — applies mig_repair_4_1_curated_excerpts_and_q1.cypher
to mit-bestand, captures before/after counts, and writes audit JSON/JSONL.

Idempotent: each Cypher statement only acts on edges that don't already
satisfy the post-condition.
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ENTWERFENMITBESTAND")
DB = "mit-bestand"

RUN_DIR = Path(r"E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset")
MIGRATION_FILE = RUN_DIR / "migrations/mig_repair_4_1_curated_excerpts_and_q1.cypher"
AUDIT_JSON = RUN_DIR / "logs/repair_d_runner.json"
AUDIT_JSONL = RUN_DIR / "logs/repair_d_runner.jsonl"
PROGRESS_LOG = RUN_DIR / "logs/repair_d_progress.log"

sys.stdout.reconfigure(encoding="utf-8")


def log(msg: str) -> None:
    line = f"[{datetime.now(timezone.utc).isoformat(timespec='seconds')}] {msg}"
    print(line)
    with PROGRESS_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def jsonl_append(path: Path, record: dict) -> None:
    record = {"_ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), **record}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def strip_line_comments(text: str) -> str:
    """Strip Cypher // line comments without touching // inside string literals."""
    out: list[str] = []
    i = 0
    n = len(text)
    in_str: str | None = None  # current string quote char, if any
    while i < n:
        ch = text[i]
        if in_str:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in ("'", '"', "`"):
            in_str = ch
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            # skip until end-of-line
            j = text.find("\n", i + 2)
            if j == -1:
                break
            i = j
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def split_statements(cypher_text: str) -> list[str]:
    """Split a Cypher migration file into individual statements on `;` boundaries,
    while respecting quoted strings (single, double, backtick) and skipping
    `//` line comments."""
    cleaned = strip_line_comments(cypher_text)
    statements: list[str] = []
    buf: list[str] = []
    in_str: str | None = None
    i = 0
    n = len(cleaned)
    while i < n:
        ch = cleaned[i]
        if in_str:
            buf.append(ch)
            if ch == "\\" and i + 1 < n:
                buf.append(cleaned[i + 1])
                i += 2
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in ("'", '"', "`"):
            in_str = ch
            buf.append(ch)
            i += 1
            continue
        if ch == ";":
            stmt = "".join(buf).strip()
            if stmt:
                statements.append(stmt)
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    tail = "".join(buf).strip()
    if tail:
        statements.append(tail)
    return statements


def is_audit_statement(stmt: str) -> bool:
    """Audit statements RETURN something; mutating statements end with SET/REMOVE/CREATE/DELETE."""
    has_return = re.search(r"\bRETURN\b", stmt, re.IGNORECASE) is not None
    has_mutation = re.search(r"\b(SET|REMOVE|CREATE|DELETE|MERGE)\b", stmt, re.IGNORECASE) is not None
    return has_return and not has_mutation


def run_query(driver, cypher: str, mode: str = "WRITE") -> tuple[list[dict], dict[str, Any]]:
    """Run a single cypher statement; return (rows, counters_dict)."""
    with driver.session(database=DB, default_access_mode=mode) as session:
        result = session.run(cypher)
        rows = [dict(r) for r in result]
        summary = result.consume()
        c = summary.counters
        counters = {
            "properties_set": c.properties_set,
            "relationships_created": c.relationships_created,
            "relationships_deleted": c.relationships_deleted,
            "nodes_created": c.nodes_created,
            "nodes_deleted": c.nodes_deleted,
            "labels_added": c.labels_added,
            "labels_removed": c.labels_removed,
            "contains_updates": c.contains_updates,
        }
    return rows, counters


# ---------- Baseline (before) ----------

def baseline_snapshot(driver) -> dict:
    log("Capturing baseline snapshot (read-only)...")
    out: dict = {}
    with driver.session(database=DB, default_access_mode="READ") as s:
        out["curated_no_excerpt_total"] = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.evidence_origin='curated'
              AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
            RETURN count(r) AS c
            """
        ).single()["c"]

        out["curated_no_excerpt_by_type"] = [
            dict(r)
            for r in s.run(
                """
                MATCH ()-[r]->()
                WHERE r.evidence_origin='curated'
                  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
                RETURN type(r) AS t, r.evidence_basis AS basis,
                       CASE WHEN r.evidence_source_id STARTS WITH 'q_actor_' THEN 'q_actor_*'
                            ELSE r.evidence_source_id END AS src,
                       count(*) AS c
                ORDER BY c DESC, t, src
                """
            )
        ]

        out["hat_bg_total"] = s.run(
            "MATCH ()-[r:HAT_BAUTEILGRUPPE]->() RETURN count(r) AS c"
        ).single()["c"]
        out["hat_bg_curated"] = s.run(
            "MATCH ()-[r:HAT_BAUTEILGRUPPE]->() WHERE r.evidence_origin='curated' RETURN count(r) AS c"
        ).single()["c"]

        out["q1_canonical_rows"] = s.run(
            """
            MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),
                  (bg)<-[r:HAT_BAUTEILGRUPPE]-(p:Projekt)
            WHERE r.evidence_origin='curated'
            RETURN count(*) AS c
            """
        ).single()["c"]

        out["bg_with_donor_and_receiver"] = s.run(
            """
            MATCH (bg:Bauteilgruppe)
            WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()}
            RETURN count(bg) AS c
            """
        ).single()["c"]

        out["origin_distribution"] = [
            dict(r)
            for r in s.run(
                """
                MATCH ()-[r]->()
                RETURN r.evidence_origin AS origin, count(*) AS c
                ORDER BY c DESC
                """
            )
        ]

        out["confidence_distribution"] = [
            dict(r)
            for r in s.run(
                """
                MATCH ()-[r]->()
                RETURN r.evidence_confidence AS conf, count(*) AS c
                ORDER BY c DESC
                """
            )
        ]

        out["invariants_4c"] = {
            "quelle_with_external_sources": s.run(
                "MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) AS c"
            ).single()["c"],
            "rels_with_url_or_source_file": s.run(
                """
                MATCH ()-[r]->()
                WITH r, [k IN keys(r) WHERE k IN ['url','http','source_file','external_sources']] AS bad
                WHERE size(bad) > 0
                RETURN count(r) AS c
                """
            ).single()["c"],
            "projekt_belegt_actor_url": s.run(
                """
                MATCH (:Projekt)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
                RETURN count(r) AS c
                """
            ).single()["c"],
            "akteur_belegt_actor_url": s.run(
                """
                MATCH (:Akteur)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
                RETURN count(r) AS c
                """
            ).single()["c"],
            "zitiert_quelle_total": s.run(
                "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS c"
            ).single()["c"],
        }

    return out


# ---------- Migration driver ----------

def apply_migration(driver, statements: list[str]) -> list[dict]:
    log(f"Applying migration: {len(statements)} statements.")
    records: list[dict] = []
    for idx, stmt in enumerate(statements, start=1):
        is_audit = is_audit_statement(stmt)
        kind = "audit" if is_audit else "mutation"
        head = re.sub(r"\s+", " ", stmt[:160]).strip()
        log(f"  [{idx:02d}/{len(statements)}] {kind}: {head}{'...' if len(stmt) > 160 else ''}")
        t0 = time.time()
        try:
            rows, counters = run_query(
                driver, stmt, mode=("READ" if is_audit else "WRITE")
            )
        except Exception as exc:
            log(f"  ERROR in statement {idx}: {exc}")
            records.append({
                "idx": idx,
                "kind": kind,
                "head": head,
                "error": str(exc),
                "elapsed_s": round(time.time() - t0, 3),
            })
            jsonl_append(AUDIT_JSONL, records[-1])
            raise
        elapsed = round(time.time() - t0, 3)
        rec = {
            "idx": idx,
            "kind": kind,
            "head": head,
            "rows": rows,
            "counters": counters,
            "elapsed_s": elapsed,
        }
        records.append(rec)
        jsonl_append(AUDIT_JSONL, rec)
        log(
            f"     -> rows={len(rows)}, props_set={counters['properties_set']}, "
            f"contains_updates={counters['contains_updates']}, elapsed={elapsed}s"
        )
    return records


# ---------- Post-checks ----------

POSITIVE_AUDIT_RULE = "audit_q1_canonical_rows"


def check_audits(audit_records: list[dict]) -> tuple[bool, list[dict]]:
    """Verify every 'audit_*' rule returns 0 violations except the positive Q1
    audit which must be >= 1."""
    findings: list[dict] = []
    overall_ok = True
    for rec in audit_records:
        if rec.get("kind") != "audit":
            continue
        for row in rec.get("rows", []):
            rule = row.get("rule")
            if not rule:
                continue
            if rule == POSITIVE_AUDIT_RULE:
                row_count = row.get("row_count_must_be_ge_1")
                ok = row_count is not None and row_count >= 1
                findings.append({
                    "rule": rule,
                    "value": row_count,
                    "expected": ">= 1",
                    "ok": ok,
                })
                overall_ok &= ok
            else:
                violations = row.get("violations", 0)
                ok = violations == 0
                findings.append({
                    "rule": rule,
                    "value": violations,
                    "expected": "0",
                    "ok": ok,
                })
                overall_ok &= ok
    return overall_ok, findings


def main() -> int:
    PROGRESS_LOG.unlink(missing_ok=True)
    AUDIT_JSONL.unlink(missing_ok=True)
    log("Repair Agent D — migration runner starting.")
    log(f"Database: {DB}; URI: {URI}")
    log(f"Migration: {MIGRATION_FILE}")

    cypher_text = MIGRATION_FILE.read_text(encoding="utf-8")
    statements = split_statements(cypher_text)
    log(f"Parsed {len(statements)} cypher statements from migration file.")

    driver = GraphDatabase.driver(URI, auth=AUTH)
    try:
        before = baseline_snapshot(driver)
        jsonl_append(AUDIT_JSONL, {"phase": "baseline_before", "snapshot": before})
        log(
            "Baseline: curated_no_excerpt="
            f"{before['curated_no_excerpt_total']}, "
            f"hat_bg_curated={before['hat_bg_curated']}, "
            f"q1_canonical={before['q1_canonical_rows']}, "
            f"bg_donor_receiver={before['bg_with_donor_and_receiver']}"
        )

        audit_records = apply_migration(driver, statements)

        after = baseline_snapshot(driver)
        jsonl_append(AUDIT_JSONL, {"phase": "baseline_after", "snapshot": after})
        log(
            "After:    curated_no_excerpt="
            f"{after['curated_no_excerpt_total']}, "
            f"hat_bg_curated={after['hat_bg_curated']}, "
            f"q1_canonical={after['q1_canonical_rows']}, "
            f"bg_donor_receiver={after['bg_with_donor_and_receiver']}"
        )

        ok, findings = check_audits(audit_records)
        for f in findings:
            mark = "OK" if f["ok"] else "FAIL"
            log(f"  audit {mark}: {f['rule']} = {f['value']} (expected {f['expected']})")

        result = {
            "status": "PASS" if ok else "FAIL",
            "started_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "before": before,
            "after": after,
            "audit_findings": findings,
            "statement_count": len(statements),
            "writes_summary": {
                "total_properties_set": sum(
                    r["counters"]["properties_set"] for r in audit_records
                ),
                "total_relationships_created": sum(
                    r["counters"]["relationships_created"] for r in audit_records
                ),
                "total_relationships_deleted": sum(
                    r["counters"]["relationships_deleted"] for r in audit_records
                ),
            },
        }
        AUDIT_JSON.write_text(
            json.dumps(result, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        jsonl_append(AUDIT_JSONL, {"phase": "final_summary", "result": result})
        log(f"Final status: {result['status']}")
        log(f"Audit JSON written: {AUDIT_JSON}")
        return 0 if ok else 2
    finally:
        driver.close()


if __name__ == "__main__":
    sys.exit(main())
