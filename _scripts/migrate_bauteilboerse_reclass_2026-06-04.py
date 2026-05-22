# -*- coding: utf-8 -*-
"""Reclassify 13 actors wrongly registered as / reduced from Bauteilbörse.

STRICT taxonomy compliance:
  - only MERGEs onto EXISTING Akteurtyp/Geschaeftsmodell/Marktmodell nodes
    (no new taxonomy nodes are created),
  - touches NO new property keys.

Reversible: writes a full before-state dump (every HAT_AKTEURTYP / HAT_GESCHAEFTSMODELL /
HAT_MARKTMODELL / HAT_AKTEURROLLE edge + node properties) for the 13 ids before any change.

See _neo4j/review/2026-06-04_bauteilboerse_reclass/actor_profiles.md for the rationale.
"""
from __future__ import annotations
import json, sys, io
from datetime import datetime, timezone
from pathlib import Path
from neo4j import GraphDatabase

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

URI = "neo4j://127.0.0.1:7687"
USER = "neo4j"
DATABASE = "mit-bestand"
PW = Path(".neo4j_password").read_text(encoding="utf-8").strip()
OUTDIR = Path("_neo4j/review/2026-06-04_bauteilboerse_reclass")

# Per-actor operations. typ/gm/mm = Akteurtyp/Geschaeftsmodell/Marktmodell.
# Only category VALUES that already exist in the taxonomy are referenced.
OPS = {
    "opalis":                              {"typ_add": ["NGO_Verband_Netzwerk"], "typ_del": ["Software_Tool_Anbieter"], "mm_del": ["Plattform-Kauf"]},
    "reuse_and_trade":                     {"typ_add": ["Unternehmen"], "gm_add": ["Multi-Vendor-Marktplatz"], "mm_add": ["Plattform-Kauf"]},
    "la_fabrique_de_bordeaux_metropole":   {},  # Oeffentliche_Institution already correct
    "mobius_reemploi":                     {"typ_add": ["Unternehmen"], "typ_del": ["Materialhub_Bauteilboerse"]},
    "madaster":                            {"typ_add": ["Unternehmen"], "gm_add": ["SaaS-Inventarplattform"]},
    "new_horizon":                         {},  # Unternehmen already correct
    "new_horizon_urban_mining":            {"typ_add": ["Unternehmen"], "typ_del": ["Materialhub_Bauteilboerse"]},  # duplicate of new_horizon
    "loopfront":                           {"typ_add": ["Software_Tool_Anbieter"], "gm_add": ["SaaS-Inventarplattform"]},
    "syphon_ag_bauteilboerse_biel_bruegg": {"typ_add": ["Unternehmen"], "typ_del": ["Materialhub_Bauteilboerse"]},  # liquidiert 2024-08-26
    "cleveland_steel_tubes":               {"typ_del": ["Materialhub_Bauteilboerse"]},  # keeps Unternehmen
    "heyne_tillett_steel":                 {},  # HTS Stockmatcher is a Tool node; engineer stays Unternehmen
    "material_reuse_portal":               {"typ_add": ["Software_Tool_Anbieter"], "gm_add": ["Netzwerk / Aggregator / Redistribution"]},
    "salvo_ltd":                           {"typ_add": ["NGO_Verband_Netzwerk", "Organisation"], "typ_del": ["Materialhub_Bauteilboerse"],
                                            "gm_del": ["Multi-Vendor-Marktplatz"], "mm_del": ["Plattform-Kauf"]},  # exchange = salvoweb
    "materialnomaden":                     {"typ_add": ["Unternehmen"], "typ_del": ["Materialhub_Bauteilboerse"]},
}

REL = {"typ": ("HAT_AKTEURTYP", "Akteurtyp"),
       "gm":  ("HAT_GESCHAEFTSMODELL", "Geschaeftsmodell"),
       "mm":  ("HAT_MARKTMODELL", "Marktmodell")}


def snapshot(tx, ids):
    rows = {}
    for i in ids:
        rec = tx.run("MATCH (a:Akteur {id:$id}) RETURN properties(a) AS p", id=i).single()
        if not rec:
            rows[i] = None
            continue
        edges = {}
        for key in ("HAT_AKTEURTYP", "HAT_GESCHAEFTSMODELL", "HAT_MARKTMODELL", "HAT_AKTEURROLLE"):
            res = tx.run(f"MATCH (a:Akteur {{id:$id}})-[:{key}]->(t) RETURN t.name AS n ORDER BY n", id=i)
            edges[key] = [x["n"] for x in res]
        rows[i] = {"props": rec["p"], "edges": edges}
    return rows


def apply_ops(tx, i, ops):
    # validate every referenced value exists, then MERGE/DELETE
    for short, names in ops.items():
        dim, action = short.split("_", 1)
        rt, lbl = REL[dim]
        for name in names:
            exists = tx.run(f"MATCH (t:{lbl} {{name:$n}}) RETURN count(t) AS c", n=name).single()["c"]
            if exists == 0:
                raise RuntimeError(f"ABORT: '{name}' is not an existing {lbl} node — refusing to create taxonomy.")
            if action == "add":
                tx.run(f"MATCH (a:Akteur {{id:$id}}), (t:{lbl} {{name:$n}}) MERGE (a)-[:{rt}]->(t)", id=i, n=name)
            else:  # del
                tx.run(f"MATCH (a:Akteur {{id:$id}})-[r:{rt}]->(t:{lbl} {{name:$n}}) DELETE r", id=i, n=name)


def types_of(tx, i):
    return [x["n"] for x in tx.run("MATCH (a:Akteur {id:$id})-[:HAT_AKTEURTYP]->(t) RETURN t.name AS n ORDER BY n", id=i)]


def main():
    d = GraphDatabase.driver(URI, auth=(USER, PW))
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ids = list(OPS)
    with d.session(database=DATABASE) as s:
        before = s.execute_read(snapshot, ids)
        snap_path = OUTDIR / f"before_state_{ts}.json"
        snap_path.write_text(json.dumps(before, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"before-state dumped -> {snap_path}")

        missing = [i for i in ids if before[i] is None]
        if missing:
            print("WARNING: ids not found:", missing)

        print("\n--- applying ---")
        for i in ids:
            if before[i] is None or not OPS[i]:
                print(f"  {i:42} (no change)")
                continue
            t0 = before[i]["edges"]["HAT_AKTEURTYP"]
            s.execute_write(apply_ops, i, OPS[i])
            t1 = s.execute_read(types_of, i)
            print(f"  {i:42} {t0} -> {t1}")

        # verification
        print("\n--- verification: remaining Materialhub_Bauteilboerse among the 13 ---")
        still = s.execute_read(lambda tx: [x["id"] for x in tx.run(
            "MATCH (a:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp {name:'Materialhub_Bauteilboerse'}) "
            "WHERE a.id IN $ids RETURN a.id AS id ORDER BY id", ids=ids)])
        print("  ", still or "none")
        total = s.execute_read(lambda tx: tx.run(
            "MATCH (:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp {name:'Materialhub_Bauteilboerse'}) RETURN count(*) AS c").single()["c"])
        print(f"  total Materialhub_Bauteilboerse-typed actors now: {total}")
    d.close()
    print("\nDONE. Rollback: re-create deleted edges / delete added edges per", snap_path.name)


if __name__ == "__main__":
    main()
