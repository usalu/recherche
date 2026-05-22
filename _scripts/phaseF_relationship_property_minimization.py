"""Phase F: minimize relationship properties (keep-list complement).

Round 2 cleanup. Relationships carry ~312k property occurrences (~12/edge) of
provenance/cache/migration bookkeeping that mirrors the junk removed from nodes.

Strategy:
  1. MIGRATE (preserve evidence links): every edge whose id-bearing provenance
     property (evidence_source_id / source_url_node_id / archive_source_id)
     points to a real source node that the origin node is not already linked to
     gets a node-level (origin)-[:BELEGT_IN]->(source) edge. No evidence trace
     is lost - the granular per-edge pointer becomes a first-class BELEGT_IN.
  2. SAFETY GATE: after migration, the count of edges that would lose a real
     source pointer must be 0, otherwise the drop is refused.
  3. DROP: from every relationship remove every property key that is not on the
     keep-list (the 46-key bookkeeping complement).

Dry-run by default. Live requires:  --confirm "PHASE_F TO mit-bestand"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

# The only relationship properties allowed to remain (semantic / real evidence).
KEEP_KEYS = {
    "id", "datenqualitaet", "evidence_confidence", "evidence_quote", "evidence_url",
    "original_source_excerpt", "pollutant_basis", "rolle", "role",
    "connection_kind", "association_basis", "reversibility", "property_name",
    "inference_basis", "individual_project_lead_uncertain",
    "not_confirmed_project_participation",
}

# Bookkeeping complement removed from every edge (computed from the live distinct
# key set on 2026-06-01; superset is harmless because REMOVE of an absent key is
# a no-op).
DROP_KEYS = [
    "archive_source_id",
    "cleanup_bauteilboersen_bidirectional_dedup_run",
    "cleanup_bauteilboersen_inverse_ledger",
    "cleanup_bauteilboersen_removed_inverse_rel_ids",
    "derivation_note",
    "evidence_basis",
    "evidence_cleanup_run",
    "evidence_confidence_status",
    "evidence_excerpt",
    "evidence_note",
    "evidence_origin",
    "evidence_quality",
    "evidence_source_id",
    "invalid_candidate_source_urls",
    "invalid_source_url",
    "invalid_source_url_node_id",
    "is_bookkeeping",
    "needs_verification",
    "previous_evidence_confidence",
    "review_run",
    "review_status",
    "source_resolution_status",
    "source_resolution_status_correction_previous",
    "source_review_status_correction_previous",
    "source_role",
    "source_scope",
    "source_status",
    "source_status_correction",
    "source_status_correction_previous",
    "source_status_correction_reason",
    "source_status_migration",
    "source_status_reason",
    "source_url",
    "source_url_http_code",
    "source_url_node_id",
    "source_url_status",
    "source_url_wayback_snapshot",
    "strict_candidate_url_array_cleanup",
    "strict_invalid_url_cleanup",
    "strict_source_url_cleanup",
    "verification_attempts",
    "verification_body_md5",
    "verification_method",
    "verification_notes",
    "verification_score",
    "verification_status",
]

# Migrate these id-bearing provenance properties to BELEGT_IN before dropping.
MIGRATE_PROPS = ["evidence_source_id", "source_url_node_id", "archive_source_id"]

PROBE = {
    "rels": "MATCH ()-[r]->() RETURN count(r) AS c",
    "prop_occurrences": "MATCH ()-[r]->() RETURN sum(size(keys(r))) AS c",
    "belegt_in": "MATCH ()-[r:BELEGT_IN]->() RETURN count(r) AS c",
}


def lose_pointer_query(prop: str) -> str:
    return (
        f"MATCH (s)-[r]->() WHERE r.`{prop}` IS NOT NULL "
        f"WITH s, r.`{prop}` AS sid "
        "WHERE EXISTS {{ (x {{id: sid}}) }} "
        "AND NOT EXISTS {{ (s)-[:BELEGT_IN]->({{id: sid}}) }} "
        "RETURN count(*) AS c"
    ).replace("{{", "{").replace("}}", "}")


def migrate_query(prop: str) -> str:
    return (
        f"MATCH (s)-[r]->() WHERE r.`{prop}` IS NOT NULL "
        f"WITH DISTINCT s, r.`{prop}` AS sid "
        "WHERE EXISTS { (x {id: sid}) } "
        "CALL (s, sid) { "
        "  MATCH (src {id: sid}) "
        "  MERGE (s)-[b:BELEGT_IN]->(src) "
        "  ON CREATE SET b.id = 'r_' + s.id + '__BELEGT_IN__' + sid "
        "} IN TRANSACTIONS OF 1000 ROWS"
    )


def drop_query() -> str:
    removes = ", ".join(f"r.`{k}`" for k in DROP_KEYS)
    return (
        "MATCH ()-[r]->() "
        f"CALL (r) {{ REMOVE {removes} }} IN TRANSACTIONS OF 5000 ROWS"
    )


def probe(session) -> dict:
    out = {k: session.run(q).single()["c"] for k, q in PROBE.items()}
    out["edges_losing_real_source_pointer"] = sum(
        session.run(lose_pointer_query(p)).single()["c"] for p in MIGRATE_PROPS
    )
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--confirm", default=None)
    args = ap.parse_args()

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    expected = f"PHASE_F TO {database}"
    live = args.confirm == expected
    if args.confirm and not live:
        raise SystemExit(f"Confirm must equal: {expected!r}")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            before = probe(session)
            result = {
                "mode": "live" if live else "dry-run",
                "keep_keys": sorted(KEEP_KEYS),
                "drop_keys_count": len(DROP_KEYS),
                "before": before,
            }
            if live:
                migrated = {}
                for prop in MIGRATE_PROPS:
                    session.run(migrate_query(prop)).consume()
                    migrated[prop] = "migrated"
                # Safety gate: no edge may still point to an unlinked real source.
                mid = probe(session)
                result["after_migration"] = mid
                if mid["edges_losing_real_source_pointer"] != 0:
                    result["aborted"] = (
                        "Safety gate failed: edges still lose a real source "
                        "pointer; drop refused."
                    )
                    print(json.dumps(result, indent=2))
                    return 1
                session.run(drop_query()).consume()
                result["after"] = probe(session)
            print(json.dumps(result, indent=2))
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
