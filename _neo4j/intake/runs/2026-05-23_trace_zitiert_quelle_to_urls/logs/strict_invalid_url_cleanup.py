"""Demote malformed source_url values so they are not treated as trusted."""

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

MIGRATION_ORIGIN = "mig_strict_invalid_url_cleanup_2026_05_23"
TRACE_MIGRATION = "mig_trace_zitiert_quelle_to_urls_2026_05_23"
NOW = datetime.now(timezone.utc).isoformat()
REPORT_JSON = REPORT_DIR / "strict_invalid_url_cleanup.json"
INVALID_JSONL = LOG_DIR / "strict_invalid_source_url_review.jsonl"
URL_RE = r"https?://[^ ]+\.[^ ]+"

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
            invalid = rows(
                session,
                """
                MATCH (a)-[r]->(b)
                WHERE r.source_url IS NOT NULL
                  AND NOT r.source_url =~ $url_re
                RETURN elementId(r) AS rel_element_id,
                       type(r) AS rel_type,
                       a.id AS start_id,
                       labels(a) AS start_labels,
                       b.id AS end_id,
                       labels(b) AS end_labels,
                       r.source_url AS invalid_source_url,
                       r.source_url_node_id AS source_url_node_id,
                       r.evidence_source_id AS evidence_source_id,
                       r.evidence_origin AS evidence_origin,
                       r.evidence_basis AS evidence_basis,
                       r.evidence_excerpt AS evidence_excerpt
                ORDER BY rel_type, start_id, end_id, rel_element_id
                """,
                url_re=URL_RE,
            )
            write_jsonl(INVALID_JSONL, invalid)
            stats["invalid_source_url_rows_exported"] = len(invalid)

            stats["invalid_relationships_demoted"] = rows(
                session,
                """
                MATCH (a)-[r]->(b)
                WHERE r.source_url IS NOT NULL
                  AND NOT r.source_url =~ $url_re
                SET r.invalid_source_url = r.source_url,
                    r.invalid_source_url_node_id = r.source_url_node_id,
                    r.source_resolution_status = 'needs_source_url_review',
                    r.review_status = 'needs_source_url_review',
                    r.strict_invalid_url_cleanup = $migration_origin,
                    r.strict_invalid_url_cleanup_at = $now
                REMOVE r.source_url, r.source_url_node_id,
                       r.source_url_status, r.source_url_http_code,
                       r.source_url_wayback_snapshot, r.source_url_last_checked_at
                MERGE (di:DataIssue {id: 'di_invalid_source_url__' + elementId(r)})
                SET di.kind = 'relationship_invalid_source_url',
                    di.severity = 'high',
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
                    di.invalid_source_url = r.invalid_source_url,
                    di.description = 'Malformed source_url was demoted and must not be used as evidence.'
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
                url_re=URL_RE,
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
                    AND r.source_url =~ $url_re
                  WITH DISTINCT r.source_url AS url
                  RETURN collect(url) AS urls
                }
                WITH n, urls
                WHERE size(urls) > 0
                SET n.source_urls = urls,
                    n.source_count = size(urls),
                    n.primary_source_url = urls[0],
                    n.source_resolution_status = 'trusted_incident_relationship_source_urls',
                    n.strict_invalid_url_cleanup = $migration_origin,
                    n.strict_invalid_url_cleanup_at = $now
                RETURN count(n) AS count
                """,
                labels=NODE_LABELS,
                url_re=URL_RE,
                migration_origin=MIGRATION_ORIGIN,
                now=NOW,
            )[0]["count"]

            stats["malformed_trusted_remaining"] = rows(
                session,
                """
                MATCH ()-[r]->()
                WHERE r.source_url IS NOT NULL
                  AND NOT r.source_url =~ $url_re
                RETURN count(r) AS count
                """,
                url_re=URL_RE,
            )[0]["count"]

            stats["malformed_node_source_urls_remaining"] = rows(
                session,
                """
                MATCH (n)
                WHERE n.source_urls IS NOT NULL
                UNWIND n.source_urls AS url
                WITH url
                WHERE NOT url =~ $url_re
                RETURN count(url) AS count
                """,
                url_re=URL_RE,
            )[0]["count"]

            stats["trusted_relationships"] = rows(
                session,
                """
                MATCH ()-[r]->()
                WHERE r.source_url IS NOT NULL
                RETURN count(r) AS count
                """,
            )[0]["count"]

            stats["zq_remaining"] = rows(
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
