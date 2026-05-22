"""Remove bubble-run Quelle nodes; keep evidence on entity/rel properties."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

REVIEW_RUNS = [
    "swiss_reuse_bubble_2026_06_05",
    "germany_reuse_bubble_2026_06_05",
    "france_reuse_bubble_2026_06_05",
    "netherlands_reuse_bubble_2026_06_05",
    "rotor_dc_reuse_bubble_2026_06_05",
]

DROP_REL_PROPS = [
    "evidence_source_id",
    "secondary_evidence_source_ids",
    "archive_source_id",
    "metadata_sidecar_key",
    "evidence_claim_ids",
]


def counts(session) -> dict:
    return {
        "nodes": session.run("MATCH (n) RETURN count(n) AS c").single()["c"],
        "relationships": session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()

    uri, u, pw, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(u, pw))
    report: dict = {
        "database": db,
        "commit": args.commit,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "review_runs": REVIEW_RUNS,
    }
    try:
        with driver.session(database=db) as s:
            report["counts_before"] = counts(s)

            belegt_rows = [
                dict(r)
                for r in s.run(
                    """
                    MATCH (n)-[r:BELEGT_IN]->(q:Quelle)
                    WHERE q.review_run IN $runs
                    RETURN n.id AS node_id, coalesce(r.evidence_url, q.url) AS url
                    """,
                    runs=REVIEW_RUNS,
                )
            ]
            url_map: dict[str, set[str]] = {}
            for row in belegt_rows:
                if row.get("node_id") and row.get("url"):
                    url_map.setdefault(row["node_id"], set()).add(row["url"])

            quellen = [
                r["id"]
                for r in s.run(
                    "MATCH (q:Quelle) WHERE q.review_run IN $runs RETURN q.id AS id ORDER BY id",
                    runs=REVIEW_RUNS,
                )
            ]
            report["quellen_to_delete"] = quellen
            report["belegt_in_to_delete"] = len(belegt_rows)
            report["node_url_merges"] = {k: sorted(v) for k, v in sorted(url_map.items())}

            if args.commit:
                for node_id, urls in url_map.items():
                    s.run(
                        """
                        MATCH (n {id: $id})
                        SET n.source_urls = CASE
                          WHEN n.source_urls IS NULL THEN $urls
                          ELSE [u IN n.source_urls WHERE u IS NOT NULL] + [x IN $urls WHERE NOT x IN coalesce(n.source_urls, [])]
                        END,
                        n.primary_source_url = coalesce(n.primary_source_url, $primary)
                        """,
                        id=node_id,
                        urls=sorted(urls),
                        primary=sorted(urls)[0],
                    )

                removed = ", ".join(f"r.{p}" for p in DROP_REL_PROPS)
                s.run(
                    f"""
                    MATCH ()-[r]->()
                    WHERE r.review_run IN $runs
                    REMOVE {removed}
                    """,
                    runs=REVIEW_RUNS,
                )

                belegt_result = s.run(
                    """
                    MATCH (n)-[r:BELEGT_IN]->(q:Quelle)
                    WHERE q.review_run IN $runs
                    DELETE r
                    """,
                    runs=REVIEW_RUNS,
                )
                quelle_result = s.run(
                    """
                    MATCH (q:Quelle)
                    WHERE q.review_run IN $runs
                    DETACH DELETE q
                    """,
                    runs=REVIEW_RUNS,
                )
                report["deleted"] = {
                    "belegt_in": belegt_result.consume().counters.relationships_deleted,
                    "quellen": quelle_result.consume().counters.nodes_deleted,
                }

            report["counts_after"] = counts(s)
    finally:
        driver.close()

    out = Path(__file__).resolve().parent / "cleanup_apply_report.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(out)
    print(json.dumps({k: report[k] for k in ("belegt_in_to_delete", "quellen_to_delete", "deleted", "counts_before", "counts_after") if k in report}, indent=2))


if __name__ == "__main__":
    main()
