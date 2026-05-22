"""
Import all 91 project-part-actor BETEILIGT_AN edges from the 2026-06-01
enriched bauteilboerse export into Neo4j, while explicitly marking them for
later evidence delivery.

Connection:
  NEO4J_URI env override, defaults to neo4j://127.0.0.1:7687
  NEO4J_USER / NEO4J_USERNAME env override, defaults to neo4j
  NEO4J_DATABASE env override, defaults to mit-bestand
Password:
  Uses NEO4J_PASSWORD if set, otherwise reads .neo4j_password from repo root.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from neo4j import GraphDatabase

URI = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
USER = (os.environ.get("NEO4J_USER") or os.environ.get("NEO4J_USERNAME") or "neo4j").strip()
DATABASE = os.environ.get("NEO4J_DATABASE", "mit-bestand").strip()
PASSWORD_FILE = Path(".neo4j_password")

BASE = Path("_neo4j/intake/runs/2026-06-01_project_part_actor_import_all")
SOURCE_JSON = Path("_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json")
REVIEW_RUN = "project_part_actor_import_all_2026_06_01"
SOURCE_SLICE = "project_part_actor_edge_enrichment_existing_node_types_2026_06_01"
EXPECTED_EDGE_COUNT = 91


def read_password() -> str:
    env_password = (os.environ.get("NEO4J_PASSWORD") or "").strip()
    if env_password:
        return env_password

    for line in PASSWORD_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    raise RuntimeError("No password found in NEO4J_PASSWORD or .neo4j_password")


def load_rows() -> list[dict]:
    data = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    rows: list[dict] = []

    for edge in data.get("edges", []):
        props = edge.get("properties") or {}
        if props.get("enrichment_run") != SOURCE_SLICE:
            continue
        rows.append(
            {
                "id": props["id"],
                "evidence_confidence": props.get("evidence_confidence"),
                "connection_kind": props.get("connection_kind"),
                "source_project_id": props.get("source_project_id"),
                "source_project_name": props.get("source_project_name"),
                "actor_id": props.get("actor_id"),
                "actor_name": props.get("actor_name"),
                "bauteilgruppe_id": props.get("bauteilgruppe_id"),
                "bauteilgruppe_name": props.get("bauteilgruppe_name"),
                "shared_bauteiltyp_ids": props.get("shared_bauteiltyp_ids") or [],
                "shared_material_ids": props.get("shared_material_ids") or [],
                "basis_project_edge_type": props.get("basis_project_edge_type"),
                "basis_project_edge_id": props.get("basis_project_edge_id"),
                "evidence_basis": props.get("evidence_basis"),
                "evidence_urls": props.get("evidence_urls") or [],
                "enrichment_run": props.get("enrichment_run"),
                "created_at_utc": props.get("created_at_utc"),
                "dedupe_key": props.get("dedupe_key"),
                "scope_note": props.get("scope_note"),
            }
        )

    rows.sort(key=lambda row: (row["source_project_id"], row["actor_id"], row["bauteilgruppe_id"]))

    if len(rows) != EXPECTED_EDGE_COUNT:
        raise RuntimeError(
            f"Expected {EXPECTED_EDGE_COUNT} edges from {SOURCE_SLICE}, found {len(rows)}"
        )

    return rows


PRECHECK_QUERY = """
UNWIND $rows AS row
OPTIONAL MATCH (a:Akteur {id: row.actor_id})
OPTIONAL MATCH (bg:Bauteilgruppe {id: row.bauteilgruppe_id})
WITH row, a, bg
WHERE a IS NULL OR bg IS NULL
RETURN row.id AS rel_id,
       row.actor_id AS actor_id,
       row.bauteilgruppe_id AS bauteilgruppe_id,
       CASE WHEN a IS NULL THEN true ELSE false END AS actor_missing,
       CASE WHEN bg IS NULL THEN true ELSE false END AS bauteilgruppe_missing
ORDER BY rel_id
"""


IMPORT_QUERY = """
UNWIND $rows AS row
MATCH (a:Akteur {id: row.actor_id})
MATCH (bg:Bauteilgruppe {id: row.bauteilgruppe_id})
MERGE (a)-[r:BETEILIGT_AN {id: row.id}]->(bg)
ON CREATE SET r.created_at_utc = row.created_at_utc
SET r.import_original_evidence_confidence = row.evidence_confidence,
    r.evidence_confidence = 'abgeleitet',
    r.connection_kind = row.connection_kind,
    r.source_project_id = row.source_project_id,
    r.source_project_name = row.source_project_name,
    r.actor_id = row.actor_id,
    r.actor_name = row.actor_name,
    r.bauteilgruppe_id = row.bauteilgruppe_id,
    r.bauteilgruppe_name = row.bauteilgruppe_name,
    r.shared_bauteiltyp_ids = row.shared_bauteiltyp_ids,
    r.shared_material_ids = row.shared_material_ids,
    r.basis_project_edge_type = row.basis_project_edge_type,
    r.basis_project_edge_id = row.basis_project_edge_id,
    r.evidence_basis = row.evidence_basis,
    r.evidence_urls = row.evidence_urls,
    r.enrichment_run = row.enrichment_run,
    r.dedupe_key = row.dedupe_key,
    r.scope_note = row.scope_note,
    r.review_run = $review_run,
    r.import_decision = 'import_all_for_now',
    r.review_status = 'needs_source_url_review',
    r.source_resolution_status = 'needs_source_url_review',
    r.source_status = 'candidate',
    r.source_status_reason = 'candidate_urls_need_fact_review',
    r.candidate_source_urls = row.evidence_urls,
    r.candidate_source_basis = $review_run,
    r.import_source_file = $source_file,
    r.import_source_slice = $source_slice
RETURN count(r) AS touched
"""


POSTCHECK_QUERY = """
MATCH ()-[r:BETEILIGT_AN {review_run: $review_run}]->()
RETURN count(r) AS imported_edges
"""


def main() -> int:
    rows = load_rows()
    password = read_password()

    print(f"Connecting: {URI}  db={DATABASE}  user={USER}")
    print(f"Source JSON: {SOURCE_JSON}")
    print(f"Source slice: {SOURCE_SLICE}")
    print(f"Expected edges: {EXPECTED_EDGE_COUNT}")

    driver = GraphDatabase.driver(URI, auth=(USER, password))
    try:
        driver.verify_connectivity()
    except Exception as exc:
        print(f"[FAIL] Connection failed: {exc}")
        return 2

    with driver.session(database=DATABASE) as session:
        missing = [dict(record) for record in session.run(PRECHECK_QUERY, rows=rows)]
        if missing:
            print(f"[FAIL] Precheck found {len(missing)} missing node matches. Aborting import.")
            for item in missing[:10]:
                print(item)
            return 1

        touched = session.run(
            IMPORT_QUERY,
            rows=rows,
            review_run=REVIEW_RUN,
            source_file=SOURCE_JSON.name,
            source_slice=SOURCE_SLICE,
        ).single()["touched"]

        imported_edges = session.run(POSTCHECK_QUERY, review_run=REVIEW_RUN).single()["imported_edges"]

    driver.close()

    print(f"[OK] Import query touched {touched} relationships.")
    print(f"[OK] review_run={REVIEW_RUN} now resolves to {imported_edges} BETEILIGT_AN edges.")

    if imported_edges != EXPECTED_EDGE_COUNT:
        print(
            f"[FAIL] Imported edge count mismatch: expected {EXPECTED_EDGE_COUNT}, got {imported_edges}"
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())