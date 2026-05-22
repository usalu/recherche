"""Filter malformed URLs out of candidate_source_urls arrays."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
REPORT_DIR = RUN_DIR / "reports"

sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MIGRATION_ORIGIN = "mig_strict_candidate_url_array_cleanup_2026_05_23"
NOW = datetime.now(timezone.utc).isoformat()
REPORT_JSON = REPORT_DIR / "strict_candidate_url_array_cleanup.json"
URL_RE = r"https?://[^ ]+\.[^ ]+"


def rows(session, cypher: str, **params) -> list[dict]:
    result = session.run(cypher, **params)
    keys = result.keys()
    return [{key: record[key] for key in keys} for record in result]


def main() -> int:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    try:
        with driver.session(database=database) as session:
            stats = {}
            stats["relationships_filtered"] = rows(
                session,
                """
                MATCH ()-[r]->()
                WHERE r.candidate_source_urls IS NOT NULL
                WITH r,
                     [url IN r.candidate_source_urls WHERE url =~ $url_re] AS valid_urls,
                     [url IN r.candidate_source_urls WHERE NOT url =~ $url_re] AS invalid_urls
                WHERE size(invalid_urls) > 0
                SET r.invalid_candidate_source_urls =
                      coalesce(r.invalid_candidate_source_urls, []) + invalid_urls,
                    r.candidate_source_urls = valid_urls,
                    r.candidate_source_count = size(valid_urls),
                    r.strict_candidate_url_array_cleanup = $migration_origin,
                    r.strict_candidate_url_array_cleanup_at = $now
                RETURN count(r) AS count, sum(size(invalid_urls)) AS invalid_urls
                """,
                url_re=URL_RE,
                migration_origin=MIGRATION_ORIGIN,
                now=NOW,
            )[0]

            stats["relationship_empty_candidate_arrays_cleared"] = rows(
                session,
                """
                MATCH ()-[r]->()
                WHERE r.candidate_source_urls IS NOT NULL
                  AND size(r.candidate_source_urls) = 0
                REMOVE r.candidate_source_urls, r.candidate_source_count
                RETURN count(r) AS count
                """,
            )[0]["count"]

            stats["nodes_filtered"] = rows(
                session,
                """
                MATCH (n)
                WHERE n.candidate_source_urls IS NOT NULL
                WITH n,
                     [url IN n.candidate_source_urls WHERE url =~ $url_re] AS valid_urls,
                     [url IN n.candidate_source_urls WHERE NOT url =~ $url_re] AS invalid_urls
                WHERE size(invalid_urls) > 0
                SET n.invalid_candidate_source_urls =
                      coalesce(n.invalid_candidate_source_urls, []) + invalid_urls,
                    n.candidate_source_urls = valid_urls,
                    n.candidate_source_count = size(valid_urls),
                    n.strict_candidate_url_array_cleanup = $migration_origin,
                    n.strict_candidate_url_array_cleanup_at = $now
                RETURN count(n) AS count, sum(size(invalid_urls)) AS invalid_urls
                """,
                url_re=URL_RE,
                migration_origin=MIGRATION_ORIGIN,
                now=NOW,
            )[0]

            stats["node_empty_candidate_arrays_cleared"] = rows(
                session,
                """
                MATCH (n)
                WHERE n.candidate_source_urls IS NOT NULL
                  AND size(n.candidate_source_urls) = 0
                REMOVE n.candidate_source_urls, n.candidate_source_count,
                       n.candidate_source_status
                RETURN count(n) AS count
                """,
            )[0]["count"]

            stats["malformed_relationship_candidate_urls_remaining"] = rows(
                session,
                """
                MATCH ()-[r]->()
                WHERE r.candidate_source_urls IS NOT NULL
                UNWIND r.candidate_source_urls AS url
                WITH url WHERE NOT url =~ $url_re
                RETURN count(url) AS count
                """,
                url_re=URL_RE,
            )[0]["count"]

            stats["malformed_node_candidate_urls_remaining"] = rows(
                session,
                """
                MATCH (n)
                WHERE n.candidate_source_urls IS NOT NULL
                UNWIND n.candidate_source_urls AS url
                WITH url WHERE NOT url =~ $url_re
                RETURN count(url) AS count
                """,
                url_re=URL_RE,
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
