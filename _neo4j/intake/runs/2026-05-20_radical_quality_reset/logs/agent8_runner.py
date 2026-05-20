"""Agent 8 — Wave 3, Phase 4c runner (mit-bestand).

Scope (per plan §4c):
  4c.1  If any :Quelle still carries `external_sources`, unfold into
        :ZITIERT_QUELLE child :Quelle nodes (idempotent — Agent 6 already
        ran this during Phase 2.7.b for 60 source :Quelle / 270 links).
  4c.3  Detach the wrong (Projekt)-[:BELEGT_IN]->(Quelle) edges that point
        at quelltyp='external_link_from_actor_registry' Quelle nodes.
        Keep the (Akteur)-[:BELEGT_IN]->(same Quelle) edges intact.
  edge  Verify no relationship carries a property whose name contains
        `url`, `http`, `source_file`, or `external_sources`. URLs live
        ONLY on :Quelle.url. Strip any survivors with a snapshot journal.

Idempotency: every step probes live state before acting; re-runs are
no-ops and only re-issue the PHASE_4C_DONE.flag.
"""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "runs"
    / "2026-05-20_radical_quality_reset"
)
LOG_DIR = RUN_ROOT / "logs"
DEL_DIR = RUN_ROOT / "deleted"
MIG_DIR = RUN_ROOT / "migrations"
REPORTS_DIR = RUN_ROOT / "reports"

PROGRESS_LOG = LOG_DIR / "agent8_progress.log"
RESULT_JSON = LOG_DIR / "agent8_result.json"
FLAG_4C = RUN_ROOT / "PHASE_4C_DONE.flag"
JOURNAL_4C_3 = DEL_DIR / "phase4c_3_projekt_actor_registry_belegt.jsonl"
JOURNAL_4C_1 = DEL_DIR / "phase4c_1_external_sources.jsonl"
JOURNAL_EDGES = DEL_DIR / "phase4c_edge_strip.jsonl"


URL_RE = re.compile(r"(https?://[^\s)>\]]+)", re.IGNORECASE)
SLUG_RE = re.compile(r"[^a-z0-9]+")


def _log(line: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    msg = f"[{stamp}] {line}"
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        print(msg.encode(enc, errors="replace").decode(enc), flush=True)
    PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with PROGRESS_LOG.open("a", encoding="utf-8") as fp:
        fp.write(msg + "\n")


def _resolve_connection() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise RuntimeError("Neo4j connection missing.")
    if database != "mit-bestand":
        _log(f"WARN: overriding NEO4J_DATABASE='{database}' to 'mit-bestand'")
        database = "mit-bestand"
    return uri, user, password, database


def extract_url(raw: str) -> str | None:
    if not isinstance(raw, str):
        return None
    m = URL_RE.search(raw)
    if not m:
        return None
    return m.group(1).rstrip(".,;:")


def slugify_url(url: str) -> str:
    s = url.lower()
    s = re.sub(r"^https?://", "", s)
    s = re.sub(r"^www\.", "", s)
    s = SLUG_RE.sub("_", s).strip("_")
    if len(s) > 120:
        head = s[:60]
        tail = s[-55:]
        s = f"{head}__{tail}"
    return f"q_ext_{s}"


def extract_title(raw: str, url: str | None) -> str:
    if not isinstance(raw, str):
        return ""
    text = raw
    if url:
        text = text.replace(url, "")
    text = re.sub(r"^\s*(\[?\*{0,2}S?\d+[\]:.]?\*{0,2})\s*[:\-—–]?\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip(" -–—:")
    return text[:240]


# --------------------------------------------------------------------------
# Snapshot
# --------------------------------------------------------------------------

def snapshot_state(session) -> dict[str, Any]:
    out: dict[str, Any] = {}
    out["total_nodes"] = session.run(
        "MATCH (n) RETURN count(n) AS c"
    ).single()["c"]
    out["total_rels"] = session.run(
        "MATCH ()-[r]->() RETURN count(r) AS c"
    ).single()["c"]
    out["quelle_total"] = session.run(
        "MATCH (q:Quelle) RETURN count(q) AS c"
    ).single()["c"]
    out["quelle_with_external_sources"] = session.run(
        "MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) AS c"
    ).single()["c"]
    out["zitiert_quelle_total"] = session.run(
        "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS c"
    ).single()["c"]
    out["quelle_actor_registry_total"] = session.run(
        "MATCH (q:Quelle) WHERE q.quelltyp = 'external_link_from_actor_registry' "
        "RETURN count(q) AS c"
    ).single()["c"]
    out["projekt_belegt_actor_registry"] = session.run(
        "MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle) "
        "WHERE q.quelltyp = 'external_link_from_actor_registry' RETURN count(r) AS c"
    ).single()["c"]
    out["akteur_belegt_actor_registry"] = session.run(
        "MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle) "
        "WHERE q.quelltyp = 'external_link_from_actor_registry' RETURN count(r) AS c"
    ).single()["c"]
    out["edges_with_illegal_keys"] = session.run(
        "MATCH ()-[r]->() "
        "WITH r, [k IN keys(r) WHERE toLower(k) CONTAINS 'url' "
        "         OR toLower(k) CONTAINS 'http' "
        "         OR toLower(k) CONTAINS 'source_file' "
        "         OR toLower(k) CONTAINS 'external_sources'] AS bad "
        "WHERE size(bad) > 0 RETURN count(r) AS c"
    ).single()["c"]
    out["distinct_illegal_rel_keys"] = sorted({
        rec["k"]
        for rec in session.run(
            "MATCH ()-[r]->() UNWIND keys(r) AS k WITH DISTINCT k "
            "WHERE toLower(k) CONTAINS 'url' "
            "   OR toLower(k) CONTAINS 'http' "
            "   OR toLower(k) CONTAINS 'source_file' "
            "   OR toLower(k) CONTAINS 'external_sources' "
            "RETURN k"
        )
    })
    return out


# --------------------------------------------------------------------------
# 4c.1
# --------------------------------------------------------------------------

def run_phase_4c_1(driver, database: str) -> dict[str, Any]:
    _log("PHASE 4c.1 — external_sources -> ZITIERT_QUELLE — START")
    res: dict[str, Any] = {
        "source_quelle_processed": 0,
        "zitiert_quelle_links_created": 0,
        "target_quelle_created_or_merged": 0,
        "skipped_already_done": False,
    }
    with driver.session(database=database) as session:
        live = session.run(
            "MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL "
            "RETURN count(q) AS c"
        ).single()["c"]
        if live == 0:
            _log("  no Quelle.external_sources arrays remain — Agent 6 / prior run "
                 "already migrated all 60 (270 :ZITIERT_QUELLE existing). Skip.")
            res["skipped_already_done"] = True
            return res

        ext_rows = list(session.run(
            "MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL "
            "RETURN q.id AS id, q.external_sources AS extsrc"
        ))
        _log(f"  external_sources migration: {len(ext_rows)} source :Quelle to unfold")
        JOURNAL_4C_1.parent.mkdir(parents=True, exist_ok=True)
        JOURNAL_4C_1.write_text("", encoding="utf-8")
        seen_targets: set[str] = set()
        with JOURNAL_4C_1.open("a", encoding="utf-8") as journal:
            for src_row in ext_rows:
                src_id = src_row["id"]
                entries = src_row["extsrc"] or []
                migrated_links: list[dict[str, Any]] = []
                for raw in entries:
                    url = extract_url(raw)
                    if not url:
                        migrated_links.append({
                            "raw": raw, "url": None,
                            "target_id": None,
                            "skipped_reason": "no_url_in_string"
                        })
                        continue
                    target_id = slugify_url(url)
                    title = extract_title(raw, url)
                    with session.begin_transaction() as tx:
                        tx.run(
                            """
                            MERGE (target:Quelle {id: $target_id})
                            ON CREATE SET target.url = $url,
                                          target.quelltyp = 'external_link',
                                          target.name = $title,
                                          target.source_scope = 'mig_4c_1_external_sources',
                                          target._created_by  = 'mig_4c_1'
                            WITH target
                            MATCH (src:Quelle {id: $src_id})
                            MERGE (src)-[r:ZITIERT_QUELLE]->(target)
                            ON CREATE SET r.evidence_origin     = 'derived',
                                          r.evidence_basis      = 'external_sources_array',
                                          r.evidence_source_id  = 'mig_4c_1',
                                          r.evidence_confidence = 'unklar',
                                          r.evidence_excerpt    = $raw
                            """,
                            {"target_id": target_id, "url": url, "title": title,
                             "src_id": src_id, "raw": raw},
                        )
                        tx.commit()
                    migrated_links.append({"raw": raw, "url": url, "target_id": target_id})
                    res["zitiert_quelle_links_created"] += 1
                    if target_id not in seen_targets:
                        seen_targets.add(target_id)
                        res["target_quelle_created_or_merged"] += 1
                with session.begin_transaction() as tx:
                    tx.run(
                        "MATCH (src:Quelle {id: $src_id}) REMOVE src.external_sources",
                        {"src_id": src_id},
                    )
                    tx.commit()
                res["source_quelle_processed"] += 1
                journal.write(json.dumps({
                    "source_quelle_id": src_id,
                    "migrated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "raw_entries": entries,
                    "migrated_links": migrated_links,
                }, ensure_ascii=False) + "\n")
        _log(f"  4c.1 done: {res['zitiert_quelle_links_created']} ZITIERT_QUELLE created, "
             f"{res['target_quelle_created_or_merged']} target :Quelle merged")
    return res


# --------------------------------------------------------------------------
# 4c.3
# --------------------------------------------------------------------------

def run_phase_4c_3(driver, database: str) -> dict[str, Any]:
    _log("PHASE 4c.3 — detach wrong Projekt-[:BELEGT_IN]->Quelle(actor_registry) — START")
    res: dict[str, Any] = {
        "projekt_edges_deleted": 0,
        "akteur_edges_kept_check": 0,
        "skipped_already_done": False,
    }
    with driver.session(database=database) as session:
        live = session.run(
            "MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle) "
            "WHERE q.quelltyp = 'external_link_from_actor_registry' RETURN count(r) AS c"
        ).single()["c"]
        if live == 0:
            _log("  no Projekt->actor_registry BELEGT_IN edges remain — skip.")
            res["skipped_already_done"] = True
            akteur = session.run(
                "MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle) "
                "WHERE q.quelltyp = 'external_link_from_actor_registry' RETURN count(r) AS c"
            ).single()["c"]
            res["akteur_edges_kept_check"] = akteur
            return res

        # Forensic snapshot — capture every edge we are about to delete
        rows = list(session.run(
            """
            MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle)
            WHERE q.quelltyp = 'external_link_from_actor_registry'
            RETURN p.id AS projekt_id, q.id AS quelle_id, q.url AS quelle_url,
                   properties(r) AS rel_props
            """
        ))
        _log(f"  to delete: {len(rows)} Projekt->actor_registry BELEGT_IN edges")
        JOURNAL_4C_3.parent.mkdir(parents=True, exist_ok=True)
        with JOURNAL_4C_3.open("w", encoding="utf-8") as fp:
            for r in rows:
                fp.write(json.dumps({
                    "deleted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "rel_type": "BELEGT_IN",
                    "projekt_id": r["projekt_id"],
                    "quelle_id": r["quelle_id"],
                    "quelle_url": r["quelle_url"],
                    "rel_props": dict(r["rel_props"] or {}),
                }, ensure_ascii=False, default=str) + "\n")

        with session.begin_transaction() as tx:
            del_rec = tx.run(
                """
                MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle)
                WHERE q.quelltyp = 'external_link_from_actor_registry'
                WITH r, count(r) AS _
                DELETE r
                RETURN count(_) AS c
                """
            ).single()
            tx.commit()
        res["projekt_edges_deleted"] = del_rec["c"]
        # Verify Akteur edges still intact
        akteur = session.run(
            "MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle) "
            "WHERE q.quelltyp = 'external_link_from_actor_registry' RETURN count(r) AS c"
        ).single()["c"]
        res["akteur_edges_kept_check"] = akteur
        _log(f"  4c.3 done: deleted {res['projekt_edges_deleted']} Projekt edges, "
             f"kept {res['akteur_edges_kept_check']} Akteur edges")
    return res


# --------------------------------------------------------------------------
# Edge property strip
# --------------------------------------------------------------------------

def run_edge_strip(driver, database: str) -> dict[str, Any]:
    _log("EDGE STRIP — remove url/http/source_file/external_sources props on edges")
    res: dict[str, Any] = {
        "edges_touched": 0,
        "keys_stripped_total": 0,
        "skipped_already_done": False,
        "distinct_keys_stripped": [],
    }
    with driver.session(database=database) as session:
        bad_keys = sorted({
            rec["k"]
            for rec in session.run(
                "MATCH ()-[r]->() UNWIND keys(r) AS k WITH DISTINCT k "
                "WHERE toLower(k) CONTAINS 'url' "
                "   OR toLower(k) CONTAINS 'http' "
                "   OR toLower(k) CONTAINS 'source_file' "
                "   OR toLower(k) CONTAINS 'external_sources' "
                "RETURN k"
            )
        })
        if not bad_keys:
            _log("  no illegal rel keys found — clean.")
            res["skipped_already_done"] = True
            return res

        _log(f"  illegal rel keys to remove: {bad_keys}")
        JOURNAL_EDGES.parent.mkdir(parents=True, exist_ok=True)
        rows = list(session.run(
            """
            MATCH ()-[r]->()
            WITH r, [k IN keys(r) WHERE toLower(k) CONTAINS 'url'
                     OR toLower(k) CONTAINS 'http'
                     OR toLower(k) CONTAINS 'source_file'
                     OR toLower(k) CONTAINS 'external_sources'] AS bad_keys
            WHERE size(bad_keys) > 0
            RETURN id(r) AS rid, type(r) AS rtype,
                   startNode(r).id AS s_id, endNode(r).id AS e_id,
                   bad_keys AS bad_keys, properties(r) AS props
            """
        ))
        with JOURNAL_EDGES.open("w", encoding="utf-8") as fp:
            for r in rows:
                fp.write(json.dumps({
                    "stripped_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "rel_id": r["rid"],
                    "rel_type": r["rtype"],
                    "start_id": r["s_id"],
                    "end_id": r["e_id"],
                    "bad_keys": r["bad_keys"],
                    "props_before": dict(r["props"] or {}),
                }, ensure_ascii=False, default=str) + "\n")

        with session.begin_transaction() as tx:
            for k in bad_keys:
                # safe parameterised property removal via apoc
                rec = tx.run(
                    """
                    MATCH ()-[r]->()
                    WHERE r[$k] IS NOT NULL
                    WITH r, count(r) AS _
                    CALL apoc.create.removeRelProperties(r, [$k]) YIELD rel
                    RETURN count(rel) AS c
                    """,
                    {"k": k},
                ).single()
                res["keys_stripped_total"] += rec["c"]
                _log(f"    removed key '{k}' from {rec['c']} edges")
            tx.commit()
        res["edges_touched"] = len(rows)
        res["distinct_keys_stripped"] = bad_keys
        _log(f"  edge strip done: touched {res['edges_touched']} edges, "
             f"stripped {res['keys_stripped_total']} key occurrences")
    return res


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def write_flag(flag_path: Path, phase: str, before: dict, after: dict, payload: dict) -> None:
    body = {
        "phase": phase,
        "completed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "before": before,
        "after": after,
        "payload": payload,
    }
    flag_path.write_text(
        json.dumps(body, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    _log(f"wrote done flag: {flag_path.name}")


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    DEL_DIR.mkdir(parents=True, exist_ok=True)
    MIG_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    from neo4j import GraphDatabase  # type: ignore

    uri, user, password, database = _resolve_connection()
    _log(f"connecting to {uri} db='{database}' as user='{user}'")
    started = time.perf_counter()
    started_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()

        with driver.session(database=database) as session:
            before = snapshot_state(session)
        _log(
            f"BEFORE: nodes={before['total_nodes']} rels={before['total_rels']}  "
            f"quelle={before['quelle_total']}  "
            f"ext_sources_remaining={before['quelle_with_external_sources']}  "
            f"zitiert_quelle={before['zitiert_quelle_total']}  "
            f"projekt_belegt_actor_reg={before['projekt_belegt_actor_registry']}  "
            f"akteur_belegt_actor_reg={before['akteur_belegt_actor_registry']}  "
            f"illegal_rel_keys={before['edges_with_illegal_keys']}"
        )

        payload_41 = run_phase_4c_1(driver, database)
        payload_43 = run_phase_4c_3(driver, database)
        payload_es = run_edge_strip(driver, database)

        with driver.session(database=database) as session:
            after = snapshot_state(session)

        # Post-conditions
        assert after["quelle_with_external_sources"] == 0, (
            f"expected 0 :Quelle.external_sources, got {after['quelle_with_external_sources']}"
        )
        assert after["projekt_belegt_actor_registry"] == 0, (
            f"expected 0 Projekt->actor_registry BELEGT_IN, got "
            f"{after['projekt_belegt_actor_registry']}"
        )
        assert after["edges_with_illegal_keys"] == 0, (
            f"expected 0 edges with url/http/source_file/external_sources keys, "
            f"got {after['edges_with_illegal_keys']}; keys: {after['distinct_illegal_rel_keys']}"
        )
        # Akteur edges to actor-registry Quelle must remain intact
        assert after["akteur_belegt_actor_registry"] == before["akteur_belegt_actor_registry"], (
            f"Akteur BELEGT_IN to actor_registry Quelle changed: "
            f"{before['akteur_belegt_actor_registry']} -> "
            f"{after['akteur_belegt_actor_registry']}"
        )

        payload = {
            "phase_4c_1": payload_41,
            "phase_4c_3": payload_43,
            "edge_strip": payload_es,
        }
        write_flag(FLAG_4C, "4c", before, after, payload)

        elapsed = time.perf_counter() - started
        result = {
            "started_at": started_iso,
            "finished_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "elapsed_seconds": elapsed,
            "before": before,
            "after": after,
            "payload": payload,
        }
        RESULT_JSON.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )
        _log(
            f"DONE  nodes {before['total_nodes']}->{after['total_nodes']}  "
            f"rels {before['total_rels']}->{after['total_rels']}  elapsed={elapsed:.2f}s"
        )
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
