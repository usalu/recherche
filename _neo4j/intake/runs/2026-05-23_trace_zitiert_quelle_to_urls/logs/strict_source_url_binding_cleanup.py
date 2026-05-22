"""Enforce strict source URL semantics.

Anything that is only a document-level URL set is not a proven URL binding for
the fact relationship. Move those broad sets into candidate_source_urls and
require review before they can become source_url/source_urls.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
LOG_DIR = RUN_DIR / "logs"
REPORT_DIR = RUN_DIR / "reports"

sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MIGRATION_ORIGIN = "mig_strict_source_url_binding_cleanup_2026_05_23"
TRACE_MIGRATION = "mig_trace_zitiert_quelle_to_urls_2026_05_23"
NOW = datetime.now(timezone.utc).isoformat()
REPORT_JSON = REPORT_DIR / "strict_source_url_binding_cleanup.json"
REVIEW_JSONL = LOG_DIR / "strict_candidate_source_url_review.jsonl"

NODE_LABELS = [
    "Projekt",
    "Bauwerk",
    "Akteur",
    "Bauteilgruppe",
    "Bauteiltyp",
    "Material",
    "Kennwert",
    "Huerde",
    "Methode",
    "Norm",
    "ResearchDocument",
    "Dossier",
    "Programm",
    "ReuseRule",
    "PruefungNachweis",
    "Aufbereitungsverfahren",
    "Leistungsanforderung",
    "Materialdepot",
    "RechtlicheBedingung",
    "Wiederverwendungskette",
    "Software",
    "Verbindungstechnik",
    "Zertifizierungssystem",
]


def rows(session, cypher: str, **params) -> list[dict]:
    result = session.run(cypher, **params)
    keys = result.keys()
    return [{key: record[key] for key in keys} for record in result]


def write_jsonl(path: Path, payload: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in payload:
            fh.write(json.dumps(row, ensure_ascii=False, default=str, sort_keys=True))
            fh.write("\n")


def main() -> int:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    try:
        with driver.session(database=database) as session:
            stats = {}

            review_rows = rows(
                session,
                """
                MATCH (a)-[r]->(b)
                WHERE r.source_resolution_status = 'evidence_source_id_url_set_requires_row_review'
                  AND r.source_urls IS NOT NULL
                  AND size(r.source_urls) > 0
                RETURN elementId(r) AS rel_element_id,
                       type(r) AS rel_type,
                       a.id AS start_id,
                       labels(a) AS start_labels,
                       b.id AS end_id,
                       labels(b) AS end_labels,
                       r.evidence_source_id AS evidence_source_id,
                       r.evidence_origin AS evidence_origin,
                       r.evidence_basis AS evidence_basis,
                       r.evidence_excerpt AS evidence_excerpt,
                       r.source_urls AS candidate_source_urls,
                       r.source_url_node_ids AS candidate_source_url_node_ids
                ORDER BY rel_type, start_id, end_id, rel_element_id
                """,
            )
            write_jsonl(REVIEW_JSONL, review_rows)
            stats["candidate_review_rows_exported"] = len(review_rows)

            stats["relationships_candidate_demoted"] = rows(
                session,
                """
                MATCH (a)-[r]->(b)
                WHERE r.source_resolution_status = 'evidence_source_id_url_set_requires_row_review'
                  AND r.source_urls IS NOT NULL
                  AND size(r.source_urls) > 0
                SET r.candidate_source_urls = r.source_urls,
                    r.candidate_source_url_node_ids = r.source_url_node_ids,
                    r.candidate_source_basis = 'evidence_source_id_document_url_set',
                    r.source_resolution_status = 'needs_source_url_review',
                    r.review_status = 'needs_source_url_review',
                    r.strict_source_url_cleanup = $migration_origin,
                    r.strict_source_url_cleanup_at = $now
                REMOVE r.source_urls, r.source_url_node_ids
                MERGE (di:DataIssue {id: 'di_source_url_review__' + elementId(r)})
                SET di.kind = 'relationship_candidate_urls_need_review',
                    di.severity = CASE
                      WHEN r.evidence_origin = 'source_curated' THEN 'high'
                      ELSE 'medium'
                    END,
                    di.status = 'review_required',
                    di.review_status = 'needs_source_url_review',
                    di.source_scope = 'source_trace_review',
                    di.source_trace_migration = $trace_migration,
                    di.migration_origin = $migration_origin,
                    di.created_at = coalesce(di.created_at, $now),
                    di.rel_type = type(r),
                    di.rel_element_id = elementId(r),
                    di.start_id = a.id,
                    di.end_id = b.id,
                    di.evidence_source_id = r.evidence_source_id,
                    di.evidence_origin = r.evidence_origin,
                    di.candidate_source_count = size(r.candidate_source_urls),
                    di.description = 'Candidate URL set came from the source document as a whole; no exact fact-to-URL binding is asserted until review.'
                MERGE (di)-[ca:CONCERNS]->(a)
                SET ca.id = coalesce(ca.id, 'r_' + di.id + '__CONCERNS__' + coalesce(a.id, elementId(a))),
                    ca.source_scope = 'source_trace_review',
                    ca.migration_origin = $migration_origin
                MERGE (di)-[cb:CONCERNS]->(b)
                SET cb.id = coalesce(cb.id, 'r_' + di.id + '__CONCERNS__' + coalesce(b.id, elementId(b))),
                    cb.source_scope = 'source_trace_review',
                    cb.migration_origin = $migration_origin
                RETURN count(r) AS count
                """,
                migration_origin=MIGRATION_ORIGIN,
                trace_migration=TRACE_MIGRATION,
                now=NOW,
            )[0]["count"]

            stats["domain_nodes_source_urls_cleared"] = rows(
                session,
                """
                MATCH (n)
                WHERE any(label IN labels(n) WHERE label IN $labels)
                REMOVE n.source_urls, n.source_count, n.primary_source_url
                RETURN count(n) AS count
                """,
                labels=NODE_LABELS,
            )[0]["count"]

            stats["domain_nodes_trusted_sources_recomputed"] = rows(
                session,
                """
                MATCH (n)
                WHERE any(label IN labels(n) WHERE label IN $labels)
                CALL {
                  WITH n
                  MATCH (n)-[r]-()
                  WHERE r.source_url IS NOT NULL
                  WITH DISTINCT r.source_url AS url
                  RETURN collect(url) AS urls
                }
                WITH n, urls
                WHERE size(urls) > 0
                SET n.source_urls = urls,
                    n.source_count = size(urls),
                    n.primary_source_url = urls[0],
                    n.source_resolution_status = 'trusted_incident_relationship_source_urls',
                    n.strict_source_url_cleanup = $migration_origin,
                    n.strict_source_url_cleanup_at = $now
                RETURN count(n) AS count
                """,
                labels=NODE_LABELS,
                migration_origin=MIGRATION_ORIGIN,
                now=NOW,
            )[0]["count"]

            stats["domain_nodes_candidate_sources_recomputed"] = rows(
                session,
                """
                MATCH (n)
                WHERE any(label IN labels(n) WHERE label IN $labels)
                CALL {
                  WITH n
                  MATCH (n)-[r]-()
                  WHERE r.candidate_source_urls IS NOT NULL
                    AND size(r.candidate_source_urls) > 0
                  UNWIND r.candidate_source_urls AS url
                  WITH DISTINCT url
                  RETURN collect(url) AS urls
                }
                WITH n, urls
                WHERE size(urls) > 0
                SET n.candidate_source_urls = urls,
                    n.candidate_source_count = size(urls),
                    n.candidate_source_status = 'needs_fact_url_review',
                    n.strict_source_url_cleanup = coalesce(n.strict_source_url_cleanup, $migration_origin),
                    n.strict_source_url_cleanup_at = coalesce(n.strict_source_url_cleanup_at, $now)
                RETURN count(n) AS count
                """,
                labels=NODE_LABELS,
                migration_origin=MIGRATION_ORIGIN,
                now=NOW,
            )[0]["count"]

            stats["node_gaps_marked"] = rows(
                session,
                """
                MATCH (n)
                WHERE any(label IN labels(n) WHERE label IN $labels)
                  AND n.source_url IS NULL
                  AND (n.source_urls IS NULL OR size(n.source_urls) = 0)
                  AND coalesce(n.source_resolution_status, '') <> 'needs_source_url_review'
                SET n.source_resolution_status = 'needs_source_url_review',
                    n.review_status = coalesce(n.review_status, 'needs_source_url_review'),
                    n.source_scope = coalesce(n.source_scope, 'source_trace_review'),
                    n.strict_source_url_cleanup = coalesce(n.strict_source_url_cleanup, $migration_origin),
                    n.strict_source_url_cleanup_at = coalesce(n.strict_source_url_cleanup_at, $now)
                MERGE (di:DataIssue {id: 'di_node_source_url_review__' + n.id})
                SET di.kind = 'node_missing_concrete_source_url',
                    di.severity = 'medium',
                    di.status = 'review_required',
                    di.review_status = 'needs_source_url_review',
                    di.source_scope = 'source_trace_review',
                    di.source_trace_migration = $trace_migration,
                    di.migration_origin = $migration_origin,
                    di.created_at = coalesce(di.created_at, $now),
                    di.ref_id = n.id,
                    di.ref_labels = labels(n),
                    di.description = 'Node has no trusted concrete source_url/source_urls after strict source binding cleanup.'
                MERGE (di)-[c:CONCERNS]->(n)
                SET c.id = coalesce(c.id, 'r_' + di.id + '__CONCERNS__' + n.id),
                    c.source_scope = 'source_trace_review',
                    c.migration_origin = $migration_origin
                RETURN count(n) AS count
                """,
                labels=NODE_LABELS,
                migration_origin=MIGRATION_ORIGIN,
                trace_migration=TRACE_MIGRATION,
                now=NOW,
            )[0]["count"]

            stats["bad_candidate_still_in_source_urls"] = rows(
                session,
                """
                MATCH ()-[r]->()
                WHERE r.source_resolution_status = 'needs_source_url_review'
                  AND r.source_urls IS NOT NULL
                  AND size(r.source_urls) > 0
                RETURN count(r) AS count
                """,
            )[0]["count"]

            stats["trusted_source_url_relationships"] = rows(
                session,
                """
                MATCH ()-[r]->()
                WHERE r.source_url IS NOT NULL
                RETURN count(r) AS count
                """,
            )[0]["count"]

            stats["candidate_relationships"] = rows(
                session,
                """
                MATCH ()-[r]->()
                WHERE r.candidate_source_urls IS NOT NULL
                  AND size(r.candidate_source_urls) > 0
                RETURN count(r) AS count
                """,
            )[0]["count"]

            stats["zitiert_quelle_remaining"] = rows(
                session,
                "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS count",
            )[0]["count"]
    finally:
        driver.close()

    REPORT_JSON.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(stats, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
