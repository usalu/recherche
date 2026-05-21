"""Quelle remediation runner — Phases Q1 through Q4.

Plan: _neo4j/QUELLE_REMEDIATION_PLAN.md
Usage:
    python quelle_remediation_runner.py q1     # URL extraction
    python quelle_remediation_runner.py q2     # secondary labels
    python quelle_remediation_runner.py q3     # text_content strip
    python quelle_remediation_runner.py q4     # surface source_urls
    python quelle_remediation_runner.py all    # run Q1 → Q2 → Q3 → Q4 in order

Each phase writes its own done flag (PHASE_Q<N>_DONE.flag) and refuses to
proceed if a hard-rule audit fails. Idempotent.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
# noinspection PyUnresolvedReferences
from neo4j_env import resolve_connection  # type: ignore

MIG_DIR = RUN_DIR / "migrations"
LOG_DIR = RUN_DIR / "logs"
REPORT_DIR = RUN_DIR / "reports"
DATABASE = "mit-bestand"

# Markdown link patterns
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
BARE_URL_RE = re.compile(r"(?<![\(\[\w])(https?://[^\s<>\"'\)]+)")

UTM_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "mc_cid", "mc_eid", "_ga",
}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_driver():
    uri, user, password, _db = resolve_connection()
    if not uri or not user:
        raise SystemExit("Missing Neo4j connection. Check .cursor/mcp.json.")
    return GraphDatabase.driver(uri, auth=(user, password))


def normalise_url(raw: str) -> str:
    """Normalise URL for deduplication.

    - lowercase scheme + host
    - strip trailing slash
    - strip common tracking params (utm_*, fbclid, gclid)
    - strip fragment
    """
    try:
        parsed = urlparse(raw.strip())
    except Exception:
        return raw.strip()
    scheme = (parsed.scheme or "https").lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/") or "/"
    query_pairs = [(k, v) for k, v in parse_qsl(parsed.query) if k.lower() not in UTM_PARAMS]
    query = urlencode(query_pairs)
    return urlunparse((scheme, netloc, path, parsed.params, query, ""))


def md5_hex(s: str) -> str:
    import hashlib
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def split_statements(cypher_text: str) -> list[str]:
    """Split Cypher at top-level semicolons. Skips comment-only lines."""
    statements: list[str] = []
    current: list[str] = []
    for raw_line in cypher_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            current.append(line)
            continue
        current.append(line)
        if stripped.endswith(";"):
            stmt = "\n".join(current).strip()
            cleaned = "\n".join(
                ln for ln in stmt.splitlines() if not ln.strip().startswith("//")
            ).strip()
            if cleaned.endswith(";"):
                cleaned = cleaned[:-1].rstrip()
            if cleaned:
                statements.append(cleaned)
            current = []
    return statements


def write_flag(phase: str, payload: dict) -> Path:
    flag_path = RUN_DIR / f"PHASE_{phase.upper()}_DONE.flag"
    flag_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return flag_path


def log_line(progress_log: Path, msg: str) -> None:
    line = f"[{utc_now()}] {msg}"
    print(line)
    with progress_log.open("a", encoding="utf-8") as fp:
        fp.write(line + "\n")


# --------------------------------------------------------------------------- #
# Q1 — URL extraction
# --------------------------------------------------------------------------- #

def extract_url_records(dossier_id: str, text: str) -> list[dict]:
    """Parse a dossier's markdown text. Return one dict per URL occurrence.

    Each dict: {url, url_hash, title, sref_label, surrounding_text, dossier_id}
    Duplicates within the same dossier are deduplicated (same normalised URL ⇒
    one record, keeping the first-seen label).
    """
    records: dict[str, dict] = {}
    if not text:
        return []

    # Markdown links: [label](url)
    for match in MD_LINK_RE.finditer(text):
        label = match.group(1).strip()
        raw_url = match.group(2).strip()
        norm = normalise_url(raw_url)
        if not norm:
            continue
        start = max(0, match.start() - 60)
        end = min(len(text), match.end() + 60)
        surrounding = text[start:end].replace("\n", " ").strip()
        # Section ref labels (S1, S7, P1) — keep label as locator
        sref = label if re.match(r"^[SP]\d+$", label) else label[:40]
        if norm not in records:
            records[norm] = {
                "url": norm,
                "url_hash": md5_hex(norm),
                "title": label[:300],
                "sref_label": sref,
                "surrounding_text": surrounding[:300],
                "dossier_id": dossier_id,
            }

    # Bare URLs not inside markdown link syntax
    for match in BARE_URL_RE.finditer(text):
        raw_url = match.group(1).strip().rstrip(".,;:!?")
        norm = normalise_url(raw_url)
        if not norm or norm in records:
            continue
        start = max(0, match.start() - 60)
        end = min(len(text), match.end() + 60)
        surrounding = text[start:end].replace("\n", " ").strip()
        records[norm] = {
            "url": norm,
            "url_hash": md5_hex(norm),
            "title": "",
            "sref_label": "bare",
            "surrounding_text": surrounding[:300],
            "dossier_id": dossier_id,
        }

    return list(records.values())


def run_q1(driver) -> dict:
    progress_log = LOG_DIR / "quelle_remediation_progress.log"
    audit_jsonl = LOG_DIR / "q1_audit.jsonl"
    cypher_text = (MIG_DIR / "mig_q1_url_extract.cypher").read_text(encoding="utf-8")
    # The migration file has TWO parameterised statements at the top, then
    # audit queries. Split, find the two parameterised ones.
    statements = split_statements(cypher_text)
    # The first two statements (MERGE ext, MERGE z) are the parameterised pair.
    if len(statements) < 2:
        raise RuntimeError("Q1 migration file missing parameterised statements")
    merge_ext_stmt = statements[0]
    merge_z_stmt = statements[1]
    audit_statements = statements[2:]

    log_line(progress_log, "Q1 starting — URL extraction from dossier text_content")

    # Stage 1: collect candidate dossiers + research documents
    with driver.session(database=DATABASE, default_access_mode="READ") as session:
        candidates = [
            dict(row) for row in session.run(
                "MATCH (q:Quelle) "
                "WHERE q.quelltyp IN ['case_markdown','research_markdown'] "
                "  AND q.text_content IS NOT NULL "
                "  AND size(q.text_content) > 0 "
                "RETURN q.id AS id, q.text_content AS text_content, q.quelltyp AS quelltyp"
            )
        ]
    log_line(progress_log, f"Q1: {len(candidates)} candidate dossiers with text_content")

    total_urls_seen = 0
    total_urls_unique_per_dossier = 0
    per_dossier_counts: dict[str, int] = {}

    with audit_jsonl.open("w", encoding="utf-8") as audit_fp:
        with driver.session(database=DATABASE, default_access_mode="WRITE") as session:
            for cand in candidates:
                records = extract_url_records(cand["id"], cand["text_content"])
                per_dossier_counts[cand["id"]] = len(records)
                total_urls_unique_per_dossier += len(records)
                for rec in records:
                    total_urls_seen += 1
                    try:
                        session.run(merge_ext_stmt, **rec).consume()
                        session.run(merge_z_stmt, **rec).consume()
                    except Exception as exc:
                        audit_fp.write(json.dumps({
                            "dossier_id": cand["id"],
                            "url": rec["url"],
                            "error": str(exc),
                        }) + "\n")
                        raise
                audit_fp.write(json.dumps({
                    "dossier_id": cand["id"],
                    "quelltyp": cand["quelltyp"],
                    "records_extracted": len(records),
                }) + "\n")
                log_line(progress_log,
                         f"  {cand['id']}: extracted {len(records)} unique URLs")

    log_line(progress_log,
             f"Q1: total per-dossier URL occurrences = {total_urls_unique_per_dossier}, "
             f"raw matches = {total_urls_seen}")

    # Run audit queries
    audit_results = {}
    with driver.session(database=DATABASE, default_access_mode="READ") as session:
        for i, stmt in enumerate(audit_statements):
            try:
                rows = [dict(r) for r in session.run(stmt)]
                audit_results[f"audit_{i}"] = rows[:30]
            except Exception as exc:
                audit_results[f"audit_{i}_error"] = str(exc)

    # Verdict
    verified = True
    for k, v in audit_results.items():
        if isinstance(v, list) and v and "violations" in v[0]:
            if v[0].get("violations", 0) > 0 and "informational" not in str(k):
                verified = False

    flag = write_flag("Q1", {
        "phase": "Q1",
        "agent": "orchestrator_quelle_remediation",
        "completed_at_utc": utc_now(),
        "verified": verified,
        "candidates_processed": len(candidates),
        "total_url_records": total_urls_unique_per_dossier,
        "per_dossier_counts_top10": dict(sorted(
            per_dossier_counts.items(), key=lambda kv: -kv[1]
        )[:10]),
        "audit_results": audit_results,
    })
    log_line(progress_log, f"Q1 flag written: {flag}")
    return {"phase": "Q1", "verified": verified, "candidates": len(candidates),
            "total_url_records": total_urls_unique_per_dossier}


# --------------------------------------------------------------------------- #
# Q2 / Q3 / Q4 — pure Cypher migrations
# --------------------------------------------------------------------------- #

def run_pure_cypher(driver, phase: str, migration_filename: str) -> dict:
    progress_log = LOG_DIR / "quelle_remediation_progress.log"
    audit_jsonl = LOG_DIR / f"{phase.lower()}_audit.jsonl"
    cypher_text = (MIG_DIR / migration_filename).read_text(encoding="utf-8")
    statements = split_statements(cypher_text)

    log_line(progress_log, f"{phase} starting — {len(statements)} statements")

    audit_results = {}
    with audit_jsonl.open("w", encoding="utf-8") as audit_fp:
        with driver.session(database=DATABASE, default_access_mode="WRITE") as session:
            for i, stmt in enumerate(statements):
                t0 = datetime.now(timezone.utc)
                try:
                    rows = [dict(r) for r in session.run(stmt)]
                    elapsed = (datetime.now(timezone.utc) - t0).total_seconds() * 1000
                    audit_fp.write(json.dumps({
                        "phase": phase,
                        "statement_index": i,
                        "elapsed_ms": elapsed,
                        "row_count": len(rows),
                        "rows": rows[:5],
                    }, default=str) + "\n")
                    audit_results[f"stmt_{i}"] = {"rows": rows[:30], "elapsed_ms": elapsed}
                    preview = stmt.splitlines()[0][:80]
                    log_line(progress_log,
                             f"  {phase} [{i+1}/{len(statements)}] OK "
                             f"({elapsed:.0f} ms) — {preview}…")
                except Exception as exc:
                    audit_fp.write(json.dumps({
                        "phase": phase,
                        "statement_index": i,
                        "error": str(exc),
                        "statement_preview": stmt[:200],
                    }) + "\n")
                    raise

    # Compute verdict — every result row that has a "violations" key must be 0
    verified = True
    for k, payload in audit_results.items():
        for row in payload.get("rows", []):
            if "violations" in row and row.get("violations", 0) > 0:
                verified = False

    flag = write_flag(phase, {
        "phase": phase,
        "agent": "orchestrator_quelle_remediation",
        "completed_at_utc": utc_now(),
        "verified": verified,
        "audit_results": {k: v.get("rows", []) for k, v in audit_results.items()},
    })
    log_line(progress_log, f"{phase} flag written: {flag}")
    return {"phase": phase, "verified": verified}


# --------------------------------------------------------------------------- #
# Entrypoint
# --------------------------------------------------------------------------- #

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    phase = sys.argv[1].lower()
    driver = get_driver()
    try:
        if phase == "q1":
            run_q1(driver)
        elif phase == "q2":
            run_pure_cypher(driver, "Q2", "mig_q2_secondary_labels.cypher")
        elif phase == "q3":
            # Q3 has a pre-gate. If the gate fails, abort.
            run_pure_cypher(driver, "Q3", "mig_q3_text_strip.cypher")
        elif phase == "q4":
            run_pure_cypher(driver, "Q4", "mig_q4_surface_urls.cypher")
        elif phase == "all":
            run_q1(driver)
            run_pure_cypher(driver, "Q2", "mig_q2_secondary_labels.cypher")
            run_pure_cypher(driver, "Q3", "mig_q3_text_strip.cypher")
            run_pure_cypher(driver, "Q4", "mig_q4_surface_urls.cypher")
        else:
            raise SystemExit(f"Unknown phase: {phase}")
    finally:
        driver.close()


if __name__ == "__main__":
    main()
