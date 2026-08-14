"""Independent post-apply validation for the strict actor-network migration."""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


RUN = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
REVIEW = ROOT / "_neo4j" / "review" / "2026-08_akteursnetz_faktencheck"
SCRIPTS = ROOT / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    final = load(REVIEW / "klassifikation_final.json")
    actor_project = set(load(REVIEW / "klassifikation_actor_project_final.json"))
    programmes = set(load(REVIEW / "programme_strict_final.json"))
    prune = set(load(REVIEW / "prune_strict_final.json"))
    redirects = load(REVIEW / "merge_redirects_strict.json")
    edge_rows = load(REVIEW / "kanten_klassifikation.json")
    keep_edges = {tuple(sorted(pair)) for pair in load(REVIEW / "keep_kanten_final.json")}
    expected_edges = {
        pair for pair in keep_edges if pair[0] in final and pair[1] in final
    }
    expected_edge_ids = {
        edge_id
        for edge_id, row in edge_rows.items()
        if tuple(sorted(row["pair"])) in expected_edges
    }

    uri, user, password, database = resolve_connection()
    if database != "mit-bestand":
        raise SystemExit(f"Unexpected database: {database}")
    from neo4j import GraphDatabase

    errors = []
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as session:
            node_rows = list(session.run(
                "MATCH (n) WHERE n.strict_review_key IN $keys "
                "OPTIONAL MATCH (n)-[rr:HAT_AKTEURROLLE]->(role:Akteurrolle) "
                "OPTIONAL MATCH (n)-[:LIEGT_IN_LAND]->(land:Land) "
                "RETURN n.strict_review_key AS key, elementId(n) AS eid, labels(n) AS labels, "
                "properties(n) AS properties, collect(DISTINCT role.name) AS roles, "
                "collect(DISTINCT land.country_iso2) AS countries, "
                "collect(DISTINCT {url: rr.evidence_url, quote: rr.evidence_quote}) AS role_evidence",
                keys=list(final),
            ))
            by_key = {}
            duplicates = []
            for record in node_rows:
                key = record["key"]
                if key in by_key:
                    duplicates.append(key)
                by_key[key] = record
            if duplicates:
                errors.append(f"duplicate strict_review_key values: {sorted(set(duplicates))}")

            kind_counts = Counter()
            for key, expected in final.items():
                record = by_key.get(key)
                if not record:
                    errors.append(f"missing node: {key}")
                    continue
                properties = dict(record["properties"])
                expected_kind = "Programm" if key in programmes else (
                    "Projekt" if (expected.get("rolle") or "").startswith("Referenzprojekt")
                    else "Akteur"
                )
                kind_counts[expected_kind] += 1
                if expected_kind not in record["labels"]:
                    errors.append(f"wrong label: {key} -> {record['labels']}")
                if properties.get("name") != expected.get("name"):
                    errors.append(f"wrong name: {key}")
                if properties.get("reuse_relevance") != expected.get("relevanz"):
                    errors.append(f"wrong relevance: {key}")
                if properties.get("primary_source_url") != expected.get("beleg_url"):
                    errors.append(f"wrong primary source: {key}")
                if record["countries"] != [expected.get("cc")]:
                    errors.append(f"wrong country relationship: {key} -> {record['countries']}")
                expected_roles = sorted(expected.get("rollen") or []) if expected_kind == "Akteur" else []
                actual_roles = sorted(role for role in record["roles"] if role is not None)
                if actual_roles != expected_roles:
                    errors.append(f"wrong roles: {key} -> {actual_roles} expected {expected_roles}")
                if expected_kind == "Akteur":
                    for evidence in record["role_evidence"]:
                        if evidence.get("url") is None and evidence.get("quote") is None:
                            continue
                        if not evidence.get("url") or not evidence.get("quote"):
                            errors.append(f"incomplete role evidence: {key}")

            relationship_rows = list(session.run(
                "MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR|BETEILIGT_AN|BETRIEBEN_VON]->(b) "
                "WHERE a.strict_review_key IN $keys AND b.strict_review_key IN $keys "
                "RETURN a.strict_review_key AS start, b.strict_review_key AS end, "
                "type(r) AS type, r.edge_review_id AS edge_review_id, "
                "r.evidence_url AS evidence_url, r.evidence_quote AS evidence_quote",
                keys=list(final),
            ))
            actual_pairs = {
                tuple(sorted((row["start"], row["end"]))) for row in relationship_rows
            }
            actual_edge_ids = {row["edge_review_id"] for row in relationship_rows}
            if actual_pairs != expected_edges:
                errors.append(
                    f"edge-pair mismatch missing={len(expected_edges-actual_pairs)} "
                    f"extra={len(actual_pairs-expected_edges)}"
                )
            if actual_edge_ids != expected_edge_ids:
                errors.append(
                    f"edge-id mismatch missing={len(expected_edge_ids-actual_edge_ids)} "
                    f"extra={len(actual_edge_ids-expected_edge_ids)}"
                )
            for row in relationship_rows:
                if not row["evidence_url"] or not row["evidence_quote"]:
                    errors.append(f"incomplete edge evidence: {row['edge_review_id']}")

            live_removed = session.run(
                "UNWIND $ids AS eid OPTIONAL MATCH (n) WHERE elementId(n) = eid "
                "RETURN count(n) AS count",
                ids=[key for key in prune if not key.startswith("NEW:")],
            ).single()["count"]
            if live_removed:
                errors.append(f"reviewed removed live nodes still exist: {live_removed}")
            merge_sources = session.run(
                "UNWIND $ids AS eid OPTIONAL MATCH (n) WHERE elementId(n) = eid "
                "RETURN count(n) AS count",
                ids=[key for key in redirects if not key.startswith("NEW:")],
            ).single()["count"]
            if merge_sources:
                errors.append(f"live merge sources still exist: {merge_sources}")

            totals = session.run(
                "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() "
                "RETURN nodes, count(r) AS relationships"
            ).single()

    report = {
        "schema_version": 1,
        "validated_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "global_counts": {
            "nodes": int(totals["nodes"]),
            "relationships": int(totals["relationships"]),
        },
        "strict_scope": {
            "nodes": len(by_key),
            "actors": kind_counts["Akteur"],
            "projects": kind_counts["Projekt"],
            "programmes": kind_counts["Programm"],
            "actor_project_nodes": len(actor_project),
            "relationships": len(relationship_rows),
            "expected_relationships": len(expected_edges),
        },
        "errors": errors,
        "success": not errors,
    }
    (RUN / "live_validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
