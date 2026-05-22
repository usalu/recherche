"""
Import the remaining web-evidenced Bauteilboerse actor-enrichment edges from
`_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json`.

Selects edges where:
  - properties.enrichment_run is one of the three unimported slices, AND
  - properties.evidence_url is present and does NOT start with 'internal:'

Guardrails:
  - All (source.id, target.id) must exist in DB (precheck).
  - For HAT_MARKTMODELL / LIEGT_IN_LAND (schema cardinality 1):
        skip the row if the source already has an edge of that type to a
        different target.
  - For every type: skip the row if a relationship of the same type already
        exists between the same source and target with a different id
        (parallel-edge prevention).

Connection:
  NEO4J_URI env override, defaults to neo4j://127.0.0.1:7687
  NEO4J_USER / NEO4J_USERNAME env override, defaults to neo4j
  NEO4J_DATABASE env override, defaults to mit-bestand
  Password: NEO4J_PASSWORD env or first non-comment line of .neo4j_password
"""
from __future__ import annotations

import csv
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

from neo4j import GraphDatabase

URI = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
USER = (os.environ.get("NEO4J_USER") or os.environ.get("NEO4J_USERNAME") or "neo4j").strip()
DATABASE = os.environ.get("NEO4J_DATABASE", "mit-bestand").strip()
PASSWORD_FILE = Path(".neo4j_password")

SOURCE_JSON = Path(
    "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json"
)
RUN_DIR = Path("_neo4j/intake/runs/2026-06-02_bauteilboerse_actor_enrichment_import")
SKIPPED_CSV = RUN_DIR / "SKIPPED.csv"

REVIEW_RUN = "bauteilboerse_actor_enrichment_import_2026_06_02"
SLICES = {
    "actor_edge_enrichment_existing_types_2026_06_01",
    "actor_edge_enrichment_deep_existing_types_2026_06_01",
    "edge_enrichment_deeper_existing_node_types_2026_06_01",
}
EXPECTED_SELECTED = 383
SINGLETON_TYPES = {"HAT_MARKTMODELL", "LIEGT_IN_LAND"}


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
    node_lookup = {
        n["elementId"]: (n["labels"][0], n["properties"].get("id"), n["properties"].get("name"))
        for n in data["nodes"]
    }
    rows: list[dict] = []
    for edge in data.get("edges", []):
        p = edge.get("properties") or {}
        if p.get("enrichment_run") not in SLICES:
            continue
        url = (p.get("evidence_url") or "").strip()
        if not url or url.startswith("internal:"):
            continue
        src = node_lookup.get(edge["source"])
        tgt = node_lookup.get(edge["target"])
        if not src or not tgt:
            continue
        rows.append({
            "id": p["id"],
            "type": edge["type"],
            "src_label": src[0],
            "src_id": src[1],
            "src_name": src[2],
            "tgt_label": tgt[0],
            "tgt_id": tgt[1],
            "tgt_name": tgt[2],
            "evidence_confidence": p.get("evidence_confidence"),
            "evidence_basis": p.get("evidence_basis"),
            "evidence_url": url,
            "scope_note": p.get("scope_note"),
            "via_bauteilgruppe_id": p.get("via_bauteilgruppe_id"),
            "enrichment_run": p.get("enrichment_run"),
            "created_at_utc": p.get("created_at_utc"),
        })
    rows.sort(key=lambda r: (r["enrichment_run"], r["type"], r["src_id"], r["tgt_id"]))
    if len(rows) != EXPECTED_SELECTED:
        raise RuntimeError(
            f"Expected {EXPECTED_SELECTED} selected edges, got {len(rows)}. "
            "Selection logic may need review."
        )
    return rows


PRECHECK_NODES_QUERY = """
UNWIND $rows AS row
OPTIONAL MATCH (s {id: row.src_id})
OPTIONAL MATCH (t {id: row.tgt_id})
WITH row, s, t
WHERE s IS NULL OR t IS NULL
RETURN row.id AS rel_id,
       row.src_id AS src_id,
       row.tgt_id AS tgt_id,
       s IS NULL AS src_missing,
       t IS NULL AS tgt_missing
"""

SINGLETON_CHECK_QUERY = """
UNWIND $rows AS row
MATCH (s {id: row.src_id})-[r]->(t)
WHERE type(r) = row.type AND t.id <> row.tgt_id
RETURN row.id   AS rel_id,
       row.type AS type,
       row.src_id AS src_id,
       row.tgt_id AS proposed_tgt_id,
       t.id      AS existing_tgt_id
"""

PARALLEL_CHECK_QUERY = """
UNWIND $rows AS row
MATCH (s {id: row.src_id})-[r]->(t {id: row.tgt_id})
WHERE type(r) = row.type AND coalesce(r.id, '') <> row.id
RETURN row.id   AS rel_id,
       row.type AS type,
       row.src_id AS src_id,
       row.tgt_id AS tgt_id,
       coalesce(r.id, '<no_id>') AS existing_rel_id
"""

IMPORT_QUERY_TEMPLATE = """
UNWIND $rows AS row
MATCH (s {id: row.src_id})
MATCH (t {id: row.tgt_id})
MERGE (s)-[r:`__TYPE__` {id: row.id}]->(t)
ON CREATE SET r.created_at_utc = row.created_at_utc
SET r.import_original_evidence_confidence = row.evidence_confidence,
    r.evidence_confidence = 'abgeleitet',
    r.evidence_basis      = row.evidence_basis,
    r.evidence_url        = row.evidence_url,
    r.scope_note          = row.scope_note,
    r.via_bauteilgruppe_id = row.via_bauteilgruppe_id,
    r.enrichment_run      = row.enrichment_run,
    r.review_run          = $review_run,
    r.import_decision     = 'import_all_for_now',
    r.review_status       = 'needs_source_url_review',
    r.source_resolution_status = 'needs_source_url_review',
    r.source_status       = 'candidate',
    r.source_status_reason = 'candidate_url_needs_fact_review',
    r.candidate_source_urls = [row.evidence_url],
    r.candidate_source_basis = $review_run,
    r.import_source_file  = $source_file,
    r.import_source_slice = row.enrichment_run
RETURN count(r) AS touched
"""

POSTCHECK_QUERY = """
MATCH ()-[r {review_run: $review_run}]->()
RETURN count(r) AS imported_edges,
       collect(DISTINCT type(r)) AS types
"""

SCHEMA_CHECK_QUERY = """
UNWIND $ids AS aid
MATCH (a {id: aid})
WITH a
OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t)        WITH a, count(t) AS n_typ
OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(l)        WITH a, n_typ, count(l) AS n_land
OPTIONAL MATCH (a)-[:HAT_MARKTMODELL]->(m)      WITH a, n_typ, n_land, count(m) AS n_mm
OPTIONAL MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g) WITH a, n_typ, n_land, n_mm, count(g) AS n_gm
OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(rr)     WITH a, n_typ, n_land, n_mm, n_gm, count(rr) AS n_roles
OPTIONAL MATCH (a)-[:BELEGT_IN]->(q)            WITH a, n_typ, n_land, n_mm, n_gm, n_roles, count(q) AS n_ev
RETURN a.id AS id, labels(a) AS lbls,
       n_typ, n_land, n_mm, n_gm, n_roles, n_ev
"""


def write_skipped(skipped: list[dict]) -> None:
    SKIPPED_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = ["rel_id", "reason", "src_id", "type", "tgt_id", "detail"]
    with SKIPPED_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in skipped:
            w.writerow({k: row.get(k, "") for k in fields})


def main() -> int:
    rows = load_rows()
    password = read_password()

    print(f"Connecting: {URI}  db={DATABASE}  user={USER}")
    print(f"Source JSON: {SOURCE_JSON}")
    print(f"Selected rows (post-filter): {len(rows)}")
    type_breakdown = Counter(r["type"] for r in rows)
    for t, n in type_breakdown.most_common():
        print(f"  {n:4d}  {t}")

    driver = GraphDatabase.driver(URI, auth=(USER, password))
    try:
        driver.verify_connectivity()
    except Exception as exc:
        print(f"[FAIL] Connection failed: {exc}")
        return 2

    skipped: list[dict] = []
    skip_ids: set[str] = set()

    with driver.session(database=DATABASE) as session:
        # 1) Node-existence precheck
        missing = [dict(rec) for rec in session.run(PRECHECK_NODES_QUERY, rows=rows)]
        if missing:
            print(f"[FAIL] {len(missing)} rows reference missing nodes. Aborting.")
            for item in missing[:10]:
                print(" ", item)
            return 1
        print("[OK] All source/target node IDs exist in DB.")

        # 2) Singleton-cardinality guard (HAT_MARKTMODELL, LIEGT_IN_LAND)
        singleton_rows = [r for r in rows if r["type"] in SINGLETON_TYPES]
        if singleton_rows:
            conflicts = list(session.run(SINGLETON_CHECK_QUERY, rows=singleton_rows))
            for rec in conflicts:
                d = dict(rec)
                skip_ids.add(d["rel_id"])
                skipped.append({
                    "rel_id": d["rel_id"],
                    "reason": "cardinality_1_conflict",
                    "src_id": d["src_id"],
                    "type": d["type"],
                    "tgt_id": d["proposed_tgt_id"],
                    "detail": f"existing target: {d['existing_tgt_id']}",
                })
            print(f"[INFO] {len(conflicts)} singleton-cardinality conflicts detected.")

        # 3) Parallel-edge guard (same src/type/tgt with a different id already exists)
        parallel = list(session.run(PARALLEL_CHECK_QUERY, rows=rows))
        for rec in parallel:
            d = dict(rec)
            if d["rel_id"] in skip_ids:
                continue
            skip_ids.add(d["rel_id"])
            skipped.append({
                "rel_id": d["rel_id"],
                "reason": "parallel_edge_exists",
                "src_id": d["src_id"],
                "type": d["type"],
                "tgt_id": d["tgt_id"],
                "detail": f"existing rel id: {d['existing_rel_id']}",
            })
        print(f"[INFO] {len(parallel)} parallel-edge collisions detected.")

        # 4) Import survivors, grouped by relationship type (Cypher can't param a rel type)
        survivors = [r for r in rows if r["id"] not in skip_ids]
        print(f"[INFO] Survivors after guards: {len(survivors)} / {len(rows)}")
        write_skipped(skipped)
        print(f"[INFO] Wrote {len(skipped)} skipped rows to {SKIPPED_CSV}")

        by_type: dict[str, list[dict]] = defaultdict(list)
        for r in survivors:
            by_type[r["type"]].append(r)

        total_touched = 0
        for rtype, batch in sorted(by_type.items()):
            q = IMPORT_QUERY_TEMPLATE.replace("__TYPE__", rtype)
            touched = session.run(
                q,
                rows=batch,
                review_run=REVIEW_RUN,
                source_file=SOURCE_JSON.name,
            ).single()["touched"]
            total_touched += touched
            print(f"  imported {touched:4d}  {rtype}")

        # 5) Postcheck total
        pc = session.run(POSTCHECK_QUERY, review_run=REVIEW_RUN).single()
        print(f"[OK] review_run={REVIEW_RUN} -> {pc['imported_edges']} edges, types={pc['types']}")

        # 6) Schema check on touched anchors
        touched_anchors = sorted({r["src_id"] for r in survivors})
        sc_rows = [dict(rec) for rec in session.run(SCHEMA_CHECK_QUERY, ids=touched_anchors)]
        ok = 0
        fails: list[dict] = []
        for d in sc_rows:
            is_soft = bool({"Software", "Tool"} & set(d["lbls"]))
            valid = (
                (d["n_typ"] >= 1 or is_soft)
                and d["n_land"] >= 1
                and d["n_mm"] == 1
                and d["n_gm"] >= 1
                and d["n_roles"] >= 3
                and d["n_ev"] >= 2
            )
            if valid:
                ok += 1
            else:
                fails.append(d)
        print(f"[SCHEMA] {ok}/{len(sc_rows)} touched anchors pass full schema check.")
        for f in fails:
            print(
                f"  [FAIL] {f['id']:35s} {f['lbls']} typ={f['n_typ']} land={f['n_land']} "
                f"mm={f['n_mm']} gm={f['n_gm']} roles={f['n_roles']} ev={f['n_ev']}"
            )

    driver.close()

    expected_touched = len(rows) - len(skip_ids)
    if total_touched != expected_touched:
        print(f"[WARN] Touched {total_touched}, expected {expected_touched}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
