"""Normalize minimal source status on fact relationships.

This run does not invent URLs. It only classifies already-present source
bindings into the compact states:

- exact: concrete, valid source_url is already on the relationship
- candidate: only candidate_source_urls exist
- missing: relationship is already marked for source URL review, or points to
  an invalid URL endpoint

Markdown/container nodes remain lineage only. Their URL inventories are not
promoted by this script.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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

MIGRATION = "mig_source_status_normalization_2026_05_28"
NOW = datetime.now(timezone.utc).isoformat()
URL_RE = r"https?://[^\s<>]+\.[^\s<>]+.*"
NON_FACT_REL_TYPES = [
    "ANCHORED_BY",
    "CITED_FROM_DOSSIER",
    "CONCERNS",
    "HAS_DATA_ISSUE",
    "HAS_SOURCE_LINK",
    "EXACT_MATCH_CANDIDATE",
]

REPORT_JSON = REPORT_DIR / "source_status_normalization_report.json"
REPORT_MD = REPORT_DIR / "source_status_normalization_report.md"
PRE_LEDGER = LOG_DIR / "pre_source_status_inventory.json"
POST_LEDGER = LOG_DIR / "post_source_status_inventory.json"
INVALID_ENDPOINTS = LOG_DIR / "invalid_direct_url_endpoints.jsonl"


def rows(session, cypher: str, **params: Any) -> list[dict[str, Any]]:
    result = session.run(cypher, **params)
    keys = result.keys()
    return [{key: record[key] for key in keys} for record in result]


def scalar(session, cypher: str, key: str = "count", **params: Any) -> Any:
    data = rows(session, cypher, **params)
    if not data:
        return None
    return data[0].get(key)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, payload: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in payload:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True, default=str))
            fh.write("\n")


def inventory(session) -> dict[str, Any]:
    return {
        "zitiert_remaining": scalar(
            session,
            "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS count",
        ),
        "relationship_source_totals": rows(
            session,
            """
            MATCH ()-[r]->()
            WHERE type(r) <> 'ZITIERT_QUELLE'
              AND NOT type(r) IN $non_fact_rel_types
            RETURN count(r) AS total,
                   count(CASE WHEN r.source_url IS NOT NULL THEN 1 END) AS exact_url,
                   count(CASE WHEN r.candidate_source_urls IS NOT NULL
                                  AND size(r.candidate_source_urls) > 0
                              THEN 1 END) AS candidate_urls,
                   count(CASE WHEN r.review_status = 'needs_source_url_review'
                                  OR r.source_resolution_status = 'needs_source_url_review'
                              THEN 1 END) AS needs_review,
                   count(CASE WHEN r.source_status IS NOT NULL THEN 1 END) AS with_source_status
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
        )[0],
        "source_status_by_type": rows(
            session,
            """
            MATCH ()-[r]->()
            WHERE type(r) <> 'ZITIERT_QUELLE'
            RETURN type(r) AS rel_type,
                   coalesce(r.source_status, '<null>') AS source_status,
                   count(r) AS count
            ORDER BY count DESC, rel_type, source_status
            LIMIT 200
            """,
        ),
        "direct_url_endpoint_unstamped": rows(
            session,
            """
            MATCH (a)-[r]->(b)
            WHERE type(r) <> 'ZITIERT_QUELLE'
              AND b.url IS NOT NULL
              AND r.source_url IS NULL
            RETURN type(r) AS rel_type,
                   labels(a) AS start_labels,
                   labels(b) AS end_labels,
                   b.url AS endpoint_url,
                   count(r) AS count
            ORDER BY count DESC, rel_type, endpoint_url
            LIMIT 100
            """,
        ),
        "review_by_type": rows(
            session,
            """
            MATCH ()-[r]->()
            WHERE r.review_status = 'needs_source_url_review'
               OR r.source_resolution_status = 'needs_source_url_review'
            RETURN type(r) AS rel_type,
                   count(r) AS count,
                   count(CASE WHEN r.candidate_source_urls IS NOT NULL
                                  AND size(r.candidate_source_urls) > 0
                              THEN 1 END) AS candidate_count
            ORDER BY count DESC
            LIMIT 80
            """,
        ),
    }


def validation(session) -> dict[str, Any]:
    return {
        "zitiert_remaining": scalar(
            session,
            "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS count",
        ),
        "exact_url_without_exact_status": scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE NOT type(r) IN $non_fact_rel_types
              AND r.source_url IS NOT NULL
              AND coalesce(r.source_status, '') <> 'exact'
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
        ),
        "candidate_urls_without_candidate_status": scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE NOT type(r) IN $non_fact_rel_types
              AND r.source_url IS NULL
              AND r.candidate_source_urls IS NOT NULL
              AND size(r.candidate_source_urls) > 0
              AND coalesce(r.source_status, '') <> 'candidate'
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
        ),
        "needs_review_without_candidate_or_missing": scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE NOT type(r) IN $non_fact_rel_types
              AND (r.review_status = 'needs_source_url_review'
                OR r.source_resolution_status = 'needs_source_url_review')
              AND r.source_url IS NULL
              AND (r.candidate_source_urls IS NULL OR size(r.candidate_source_urls) = 0)
              AND coalesce(r.source_status, '') <> 'missing'
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
        ),
        "review_relationship_with_trusted_url": scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE NOT type(r) IN $non_fact_rel_types
              AND (r.review_status = 'needs_source_url_review'
                OR r.source_resolution_status = 'needs_source_url_review')
              AND r.source_url IS NOT NULL
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
        ),
        "malformed_exact_source_url": scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE NOT type(r) IN $non_fact_rel_types
              AND r.source_url IS NOT NULL
              AND NOT r.source_url =~ $url_re
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
            url_re=URL_RE,
        ),
        "malformed_candidate_source_urls": rows(
            session,
            """
            MATCH ()-[r]->()
            WHERE NOT type(r) IN $non_fact_rel_types
              AND r.candidate_source_urls IS NOT NULL
            WITH r, [u IN r.candidate_source_urls WHERE NOT u =~ $url_re] AS bad
            WHERE size(bad) > 0
            RETURN count(r) AS relationships, sum(size(bad)) AS bad_urls
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
            url_re=URL_RE,
        )[0],
        "direct_valid_endpoint_unstamped_non_audit": scalar(
            session,
            """
            MATCH (a)-[r]->(b)
            WHERE type(r) <> 'ZITIERT_QUELLE'
              AND NOT type(r) IN $non_fact_rel_types
              AND NOT a:DataIssue
              AND b.url IS NOT NULL
              AND b.url =~ $url_re
              AND r.source_url IS NULL
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
            url_re=URL_RE,
        ),
    }


def main() -> int:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()

    report: dict[str, Any] = {
        "database": database,
        "migration": MIGRATION,
        "started_at": NOW,
        "url_regex": URL_RE,
        "rule": "Only concrete URL on the fact is exact; candidate URLs stay candidate.",
    }

    with driver.session(database=database) as session:
        pre = inventory(session)
        write_json(PRE_LEDGER, pre)
        report["pre"] = pre

        invalid = rows(
            session,
            """
            MATCH (a)-[r]->(b)
            WHERE type(r) <> 'ZITIERT_QUELLE'
              AND b.url IS NOT NULL
              AND r.source_url IS NULL
              AND NOT b.url =~ $url_re
            RETURN elementId(r) AS rel_element_id,
                   type(r) AS rel_type,
                   a.id AS start_id,
                   labels(a) AS start_labels,
                   b.id AS end_id,
                   labels(b) AS end_labels,
                   b.url AS invalid_endpoint_url
            ORDER BY rel_type, start_id, end_id, rel_element_id
            """,
            url_re=URL_RE,
        )
        write_jsonl(INVALID_ENDPOINTS, invalid)
        report["invalid_direct_url_endpoint_rows"] = len(invalid)

        stats: dict[str, Any] = {}

        stats["direct_valid_endpoint_relationships_stamped"] = scalar(
            session,
            """
            MATCH (a)-[r]->(b)
            WHERE type(r) <> 'ZITIERT_QUELLE'
              AND NOT type(r) IN $non_fact_rel_types
              AND NOT a:DataIssue
              AND b.url IS NOT NULL
              AND b.url =~ $url_re
              AND r.source_url IS NULL
            SET r.source_url = b.url,
                r.source_url_node_id = b.id,
                r.source_status = 'exact',
                r.source_status_reason = 'direct_valid_url_endpoint',
                r.source_resolution_status = coalesce(r.source_resolution_status, 'direct_url_endpoint'),
                r.source_status_migration = $migration,
                r.source_status_normalized_at = $now
            RETURN count(r) AS count
            """,
            url_re=URL_RE,
            non_fact_rel_types=NON_FACT_REL_TYPES,
            migration=MIGRATION,
            now=NOW,
        )

        stats["invalid_endpoint_fact_relationships_marked_missing"] = scalar(
            session,
            """
            MATCH (a)-[r]->(b)
            WHERE type(r) <> 'ZITIERT_QUELLE'
              AND NOT type(r) IN $non_fact_rel_types
              AND NOT a:DataIssue
              AND b.url IS NOT NULL
              AND r.source_url IS NULL
              AND NOT b.url =~ $url_re
            SET r.source_status = 'missing',
                r.review_status = 'needs_source_url_review',
                r.source_resolution_status = 'needs_source_url_review',
                r.invalid_source_url = b.url,
                r.source_status_reason = 'invalid_direct_url_endpoint',
                r.source_status_migration = $migration,
                r.source_status_normalized_at = $now
            RETURN count(r) AS count
            """,
            url_re=URL_RE,
            non_fact_rel_types=NON_FACT_REL_TYPES,
            migration=MIGRATION,
            now=NOW,
        )

        stats["relationships_marked_exact"] = scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE type(r) <> 'ZITIERT_QUELLE'
              AND NOT type(r) IN $non_fact_rel_types
              AND r.source_url IS NOT NULL
              AND coalesce(r.review_status, '') <> 'needs_source_url_review'
              AND coalesce(r.source_resolution_status, '') <> 'needs_source_url_review'
            SET r.source_status = 'exact',
                r.source_status_reason = coalesce(r.source_status_reason, 'concrete_source_url_on_fact'),
                r.source_status_migration = $migration,
                r.source_status_normalized_at = $now
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
            migration=MIGRATION,
            now=NOW,
        )

        stats["relationships_marked_candidate"] = scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE type(r) <> 'ZITIERT_QUELLE'
              AND NOT type(r) IN $non_fact_rel_types
              AND r.source_url IS NULL
              AND r.candidate_source_urls IS NOT NULL
              AND size(r.candidate_source_urls) > 0
            SET r.source_status = 'candidate',
                r.review_status = coalesce(r.review_status, 'needs_source_url_review'),
                r.source_resolution_status = coalesce(r.source_resolution_status, 'needs_source_url_review'),
                r.source_status_reason = coalesce(r.source_status_reason, 'candidate_urls_need_fact_review'),
                r.source_status_migration = $migration,
                r.source_status_normalized_at = $now
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
            migration=MIGRATION,
            now=NOW,
        )

        stats["relationships_marked_missing"] = scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE type(r) <> 'ZITIERT_QUELLE'
              AND NOT type(r) IN $non_fact_rel_types
              AND r.source_url IS NULL
              AND (r.candidate_source_urls IS NULL OR size(r.candidate_source_urls) = 0)
              AND (r.review_status = 'needs_source_url_review'
                OR r.source_resolution_status = 'needs_source_url_review')
            SET r.source_status = 'missing',
                r.source_status_reason = coalesce(r.source_status_reason, 'no_exact_url_binding_needs_review'),
                r.source_status_migration = $migration,
                r.source_status_normalized_at = $now
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
            migration=MIGRATION,
            now=NOW,
        )

        report["stats"] = stats

        post = inventory(session)
        gates = validation(session)
        report["post"] = post
        report["gates"] = gates
        write_json(POST_LEDGER, post)
        write_json(REPORT_JSON, report)

    lines = [
        "# Source Status Normalization Report",
        "",
        f"- Database: `{database}`",
        f"- Migration: `{MIGRATION}`",
        f"- Started: `{NOW}`",
        "",
        "## Rule",
        "",
        "`exact` means a concrete valid URL is already on the fact relationship. "
        "`candidate` means only review leads exist. `missing` means no exact URL "
        "binding is known and review is required.",
        "",
        "## Writes",
        "",
    ]
    for key, value in report["stats"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Gates", ""])
    for key, value in report["gates"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- No `.md` container or Dossier/ResearchDocument node was promoted to source truth.",
            "- Invalid direct URL endpoints were exported for review and marked `missing` only when they were non-audit fact relationships.",
            "- Candidate URL arrays remain candidates and are not counted as exact source coverage.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(report["stats"], ensure_ascii=False, indent=2, sort_keys=True))
    print(json.dumps(report["gates"], ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
