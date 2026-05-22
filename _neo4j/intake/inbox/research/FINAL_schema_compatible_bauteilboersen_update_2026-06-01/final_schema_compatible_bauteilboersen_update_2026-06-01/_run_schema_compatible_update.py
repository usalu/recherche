"""
Executor for schema_compatible_bauteilboersen_update_2026_06_01.

Adds 16 new Bauteilbörsen (14 Swiss + salza promotion + baumatpool_ch),
following the schema in BAUTEILBOERSE_SUBGRAPH_SCHEMA.md.
Reads the two import CSVs directly via the Python driver (no LOAD CSV needed).
"""
from __future__ import annotations

import csv
import os
import sys
from pathlib import Path
from neo4j import GraphDatabase

URI      = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
USER     = os.environ.get("NEO4J_USER", "neo4j").strip()
DATABASE = os.environ.get("NEO4J_DATABASE", "mit-bestand").strip()
PWPATH   = Path(".neo4j_password")

BASE      = Path("_neo4j/intake/inbox/research/FINAL_schema_compatible_bauteilboersen_update_2026-06-01/final_schema_compatible_bauteilboersen_update_2026-06-01")
ANCHORS_F = BASE / "csv" / "GRAPH_IMPORT_ACTORS_REQUIRED_EDGES.csv"
STRICT_F  = BASE / "csv" / "GRAPH_IMPORT_STRICT_MATERIAL_BAUTEILTYP_EDGES.csv"

RUN_TAG = "schema_compatible_bauteilboersen_update_2026_06_01"


def read_password() -> str:
    for line in PWPATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    raise RuntimeError("no password in .neo4j_password")


def fmt_counters(c) -> str:
    parts = []
    for k in ("nodes_created", "nodes_deleted", "relationships_created",
              "relationships_deleted", "labels_added", "properties_set"):
        v = getattr(c, k)
        if v:
            short = {"nodes_created":"n+","nodes_deleted":"n-",
                     "relationships_created":"r+","relationships_deleted":"r-",
                     "labels_added":"lbl+","properties_set":"p+"}[k]
            parts.append(f"{short}={v}")
    return " ".join(parts) or "{}"


def main() -> int:
    pw = read_password()
    print(f"Connecting: {URI}  db={DATABASE}  user={USER}")
    driver = GraphDatabase.driver(URI, auth=(USER, pw))
    driver.verify_connectivity()

    anchors = list(csv.DictReader(open(ANCHORS_F, encoding="utf-8")))
    strict  = list(csv.DictReader(open(STRICT_F,  encoding="utf-8")))
    mat_rows = [r for r in strict if r["rel_type"] == "NUTZT_MATERIAL"]
    bt_rows  = [r for r in strict if r["rel_type"] == "HAT_BAUTEILTYP"]
    print(f"Loaded {len(anchors)} anchors, {len(mat_rows)} mat rows, {len(bt_rows)} bt rows")

    with driver.session(database=DATABASE) as s:
        # --- STEP 1: anchor nodes -----------------------------------------
        print("\n--- STEP 1: anchor nodes ---")
        q = """
        UNWIND $rows AS row
        MERGE (a:Akteur {id: row.anchor_id})
        ON CREATE SET a.name = row.name,
                      a.source_scope = row.source_scope,
                      a.review_run = $tag
        ON MATCH SET a.name = coalesce(a.name, row.name),
                     a.review_run = $tag
        """
        c = s.run(q, rows=anchors, tag=RUN_TAG).consume().counters
        print(f"  anchors merged: {fmt_counters(c)}")

        # --- STEP 2: LIEGT_IN_LAND ---------------------------------------
        q = """
        UNWIND $rows AS row
        MATCH (a:Akteur {id: row.anchor_id})
        MATCH (l:Land {id: row.land_id})
        MERGE (a)-[:LIEGT_IN_LAND]->(l)
        """
        c = s.run(q, rows=anchors).consume().counters
        print(f"  LIEGT_IN_LAND: {fmt_counters(c)}")

        # --- STEP 3: HAT_MARKTMODELL -------------------------------------
        q = """
        UNWIND $rows AS row
        MATCH (a:Akteur {id: row.anchor_id})
        MATCH (m:Marktmodell {id: row.marktmodell_id})
        MERGE (a)-[:HAT_MARKTMODELL]->(m)
        """
        c = s.run(q, rows=anchors).consume().counters
        print(f"  HAT_MARKTMODELL: {fmt_counters(c)}")

        # --- STEP 4: HAT_AKTEURTYP (multi) -------------------------------
        rows_typ = []
        for r in anchors:
            for tid in r["akteurtyp_ids"].split(";"):
                tid = tid.strip()
                if tid:
                    rows_typ.append({"anchor_id": r["anchor_id"], "tid": tid})
        q = """
        UNWIND $rows AS row
        MATCH (a:Akteur {id: row.anchor_id})
        MATCH (t:Akteurtyp {id: row.tid})
        MERGE (a)-[:HAT_AKTEURTYP]->(t)
        """
        c = s.run(q, rows=rows_typ).consume().counters
        print(f"  HAT_AKTEURTYP ({len(rows_typ)} pairs): {fmt_counters(c)}")

        # --- STEP 5: HAT_GESCHAEFTSMODELL --------------------------------
        rows_gm = []
        for r in anchors:
            for gid in r["geschaeftsmodell_ids"].split(";"):
                gid = gid.strip()
                if gid:
                    rows_gm.append({"anchor_id": r["anchor_id"], "gid": gid})
        q = """
        UNWIND $rows AS row
        MATCH (a:Akteur {id: row.anchor_id})
        MATCH (g:Geschaeftsmodell {id: row.gid})
        MERGE (a)-[r:HAT_GESCHAEFTSMODELL]->(g)
        ON CREATE SET r.review_run = $tag
        """
        c = s.run(q, rows=rows_gm, tag=RUN_TAG).consume().counters
        print(f"  HAT_GESCHAEFTSMODELL ({len(rows_gm)} pairs): {fmt_counters(c)}")

        # --- STEP 6: BELEGT_IN evidence URLs -----------------------------
        rows_ev = []
        for r in anchors:
            urls = [u.strip() for u in r["evidence_urls"].split(";") if u.strip()]
            qids = [q.strip() for q in r["evidence_qids"].split(";") if q.strip()]
            for url, qid in zip(urls, qids):
                rows_ev.append({"anchor_id": r["anchor_id"], "url": url, "qid": qid})
        q = """
        UNWIND $rows AS row
        MATCH (a:Akteur {id: row.anchor_id})
        MERGE (q:Quelle {id: row.qid})
        ON CREATE SET q.url = row.url, q.quelltyp = 'external_link'
        ON MATCH SET q.url = coalesce(q.url, row.url),
                     q.quelltyp = coalesce(q.quelltyp, 'external_link')
        MERGE (a)-[:BELEGT_IN]->(q)
        """
        c = s.run(q, rows=rows_ev).consume().counters
        print(f"  BELEGT_IN ({len(rows_ev)} url pairs): {fmt_counters(c)}")

        # --- STEP 7: fingerprint roles per Geschäftsmodell ---------------
        print("\n--- STEP 7: fingerprint roles/methods ---")
        fingerprint_role = {
            "gm_shop_eigenstock": ["ar_materialbroker"],
            "gm_marketplace_vermittlung": ["ar_materialbroker", "ar_software_digitalisierung"],
            "gm_dienstleistung_urban_mining": [
                "ar_rueckbau_bauteilernte_logistik","ar_aufbereitung_refurbishment",
                "ar_materiallieferung_markt","ar_reuse_zirkularitaetsberatung"],
            "gm_saas_inventar_plattform": ["ar_software_digitalisierung","ar_forschung_dokumentation"],
            "gm_netzwerk_aggregator": ["ar_bildung_wissenstransfer","ar_forschung_dokumentation","ar_materialbroker"],
        }
        fingerprint_meth = {
            "gm_dienstleistung_urban_mining": ["meth_urban_mining","meth_pre_deconstruction_audit","meth_bauteilkatalogisierung"],
            "gm_saas_inventar_plattform": ["meth_materialinventur","meth_bauteilkatalogisierung","meth_abrissmonitoring"],
        }
        for gm, roles in fingerprint_role.items():
            q = """
            MATCH (a:Akteur {review_run:$tag})-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:$gm})
            UNWIND $roles AS rid
            MATCH (r:Akteurrolle {id: rid})
            MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
            ON CREATE SET rel.review_run = $tag
            """
            c = s.run(q, gm=gm, roles=roles, tag=RUN_TAG).consume().counters
            print(f"  roles for {gm:35s}: {fmt_counters(c)}")
        for gm, meths in fingerprint_meth.items():
            q = """
            MATCH (a:Akteur {review_run:$tag})-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:$gm})
            UNWIND $meths AS mid
            MATCH (m:Methode {id: mid})
            MERGE (a)-[rel:HAT_METHODE]->(m)
            ON CREATE SET rel.review_run = $tag
            """
            c = s.run(q, gm=gm, meths=meths, tag=RUN_TAG).consume().counters
            print(f"  methods for {gm:33s}: {fmt_counters(c)}")

        # --- STEP 8: strict NUTZT_MATERIAL imports -----------------------
        print("\n--- STEP 8: strict imports ---")
        q = """
        UNWIND $rows AS row
        MATCH (a:Akteur {id: row.anchor_id})
        MATCH (m:Material {id: row.target_id})
        MERGE (a)-[r:NUTZT_MATERIAL]->(m)
        ON CREATE SET r.evidence_confidence='belegt',
                      r.review_run=$tag,
                      r.evidence_url=row.canonical_evidence_url,
                      r.evidence_quote=row.evidence_quote
        """
        c = s.run(q, rows=mat_rows, tag=RUN_TAG).consume().counters
        print(f"  NUTZT_MATERIAL ({len(mat_rows)} rows): {fmt_counters(c)}")

        # --- STEP 9: strict HAT_BAUTEILTYP imports -----------------------
        q = """
        UNWIND $rows AS row
        MATCH (a:Akteur {id: row.anchor_id})
        MATCH (b:Bauteiltyp {id: row.target_id})
        MERGE (a)-[r:HAT_BAUTEILTYP]->(b)
        ON CREATE SET r.evidence_confidence='belegt',
                      r.review_run=$tag,
                      r.evidence_url=row.canonical_evidence_url,
                      r.evidence_quote=row.evidence_quote
        """
        c = s.run(q, rows=bt_rows, tag=RUN_TAG).consume().counters
        print(f"  HAT_BAUTEILTYP ({len(bt_rows)} rows): {fmt_counters(c)}")

        # --- STEP 10: validation ----------------------------------------
        print("\n--- VALIDATION ---")
        q = """
        MATCH (a:Akteur {review_run:$tag})
        OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t:Akteurtyp)
        WITH a, count(t) AS n_typ
        OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(l:Land)
        WITH a, n_typ, count(l) AS n_land
        OPTIONAL MATCH (a)-[:HAT_MARKTMODELL]->(m:Marktmodell)
        WITH a, n_typ, n_land, count(m) AS n_mm
        OPTIONAL MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g)
        WITH a, n_typ, n_land, n_mm, count(g) AS n_gm
        OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(r:Akteurrolle)
        WITH a, n_typ, n_land, n_mm, n_gm, count(r) AS n_roles
        OPTIONAL MATCH (a)-[:BELEGT_IN]->(q:Quelle)
        WITH a, n_typ, n_land, n_mm, n_gm, n_roles, count(q) AS n_evidence
        OPTIONAL MATCH (a)-[:NUTZT_MATERIAL]->(mm:Material)
        WITH a, n_typ, n_land, n_mm, n_gm, n_roles, n_evidence, count(mm) AS n_mat
        OPTIONAL MATCH (a)-[:HAT_BAUTEILTYP]->(bb:Bauteiltyp)
        WITH a, n_typ, n_land, n_mm, n_gm, n_roles, n_evidence, n_mat, count(bb) AS n_bt
        RETURN a.id AS actor, n_typ, n_land, n_mm, n_gm, n_roles, n_evidence, n_mat, n_bt,
               CASE WHEN n_typ>=1 AND n_land=1 AND n_mm=1 AND n_gm>=1 AND n_roles>=3 AND n_evidence>=2
                    THEN 'OK' ELSE 'MISSING' END AS check
        ORDER BY actor
        """
        ok, miss = 0, 0
        for r in s.run(q, tag=RUN_TAG):
            d_ = dict(r)
            tag = "[OK]" if d_["check"] == "OK" else "[FAIL]"
            if d_["check"] == "OK": ok += 1
            else: miss += 1
            print(f"  {tag} {d_['actor']:50s} typ={d_['n_typ']} land={d_['n_land']} mm={d_['n_mm']} gm={d_['n_gm']} roles={d_['n_roles']} evidence={d_['n_evidence']} mat={d_['n_mat']} bt={d_['n_bt']}")

        # totals
        for q, label in [
            ("MATCH ()-[r:NUTZT_MATERIAL {review_run:$tag}]->() RETURN count(r) AS n", "new NUTZT_MATERIAL"),
            ("MATCH ()-[r:HAT_BAUTEILTYP {review_run:$tag}]->() RETURN count(r) AS n", "new HAT_BAUTEILTYP"),
            ("MATCH ()-[r:HAT_GESCHAEFTSMODELL {review_run:$tag}]->() RETURN count(r) AS n", "new HAT_GESCHAEFTSMODELL"),
            ("MATCH (a:Akteur {review_run:$tag}) RETURN count(a) AS n", "Akteur with run_tag"),
        ]:
            row = s.run(q, tag=RUN_TAG).single()
            print(f"  {label}: {row['n']}")

        print(f"\n=== SUMMARY: {ok}/{ok+miss} actors passed schema_check ===")
    driver.close()
    return 0 if miss == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
