"""Deep probe: actor location signals beyond BETEILIGT_AN."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

ORPHANS = [
    "edith_maryon_stift",
    "gillion_construct",
    "gtd_consulting",
    "heinrich_boell_stiftung",
    "interreg_nwe",
    "koimo_development",
    "ld2_architecture",
    "mamout_architectes",
    "mobat_ingenierie",
    "stephanie_willocx",
    "superuse_on_site",
]

uri, user, password, database = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, password))
out: dict = {"database": database, "orphans": {}, "rel_types_from_akteur": [], "sample_paths": []}

with driver.session(database=database) as session:
    out["rel_types_from_akteur"] = [
        r["t"]
        for r in session.run(
            "MATCH (:Akteur)-[r]-() RETURN DISTINCT type(r) AS t ORDER BY t"
        )
    ]

    for aid in ORPHANS:
        row = session.run(
            """
            MATCH (a:Akteur {id: $id})
            OPTIONAL MATCH (a)-[r]-(n)
            RETURN a.id AS id, a.name AS name, properties(a) AS props,
                   collect(DISTINCT {
                     rel: type(r),
                     dir: CASE WHEN startNode(r)=a THEN 'out' ELSE 'in' END,
                     labels: labels(n),
                     nid: n.id,
                     nname: coalesce(n.name, n.id),
                     nprops: properties(n)
                   }) AS rels
            """,
            id=aid,
        ).single()
        rels = []
        for rel in row["rels"] or []:
            if not rel.get("nid"):
                continue
            np = rel.get("nprops") or {}
            geo = {k: np.get(k) for k in ("adresse", "latitude", "longitude") if np.get(k) is not None}
            rels.append(
                {
                    "rel": rel["rel"],
                    "dir": rel["dir"],
                    "labels": rel["labels"],
                    "id": rel["nid"],
                    "name": rel["nname"],
                    "geo": geo or None,
                }
            )
        out["orphans"][aid] = {
            "name": row["name"],
            "props": {k: v for k, v in (row["props"] or {}).items() if k != "metadata_sidecar_key"},
            "relationships": rels,
        }

    # Name co-occurrence: actors sharing projekte with orphans
    out["molenbeek_projekt_candidates"] = [
        dict(r)
        for r in session.run(
            """
            MATCH (p:Projekt)
            WHERE toLower(p.name) CONTAINS 'molenbeek'
               OR toLower(p.id) CONTAINS 'molenbeek'
               OR toLower(p.name) CONTAINS 'charles malis'
               OR toLower(p.id) CONTAINS 'charles_malis'
               OR toLower(p.name) CONTAINS 'karreveld'
            RETURN p.id AS id, p.name AS name, p.adresse AS adresse,
                   p.latitude AS lat, p.longitude AS lng
            """
        )
    ]

    out["kindl_boell_candidates"] = [
        dict(r)
        for r in session.run(
            """
            MATCH (p:Projekt)
            WHERE toLower(p.name) CONTAINS 'kindl'
               OR toLower(p.id) CONTAINS 'kindl'
               OR toLower(p.name) CONTAINS 'boell'
               OR toLower(p.id) CONTAINS 'boell'
               OR toLower(p.name) CONTAINS 'edith maryon'
            RETURN p.id AS id, p.name AS name, p.adresse AS adresse,
                   p.latitude AS lat, p.longitude AS lng
            """
        )
    ]

    out["bauwerk_karreveld"] = [
        dict(r)
        for r in session.run(
            """
            MATCH (b:Bauwerk)
            WHERE toLower(b.id) CONTAINS 'karreveld'
               OR toLower(b.name) CONTAINS 'karreveld'
               OR toLower(b.name) CONTAINS 'charles malis'
               OR toLower(b.name) CONTAINS 'molenbeek'
            RETURN b.id AS id, b.name AS name, b.adresse AS adresse,
                   b.latitude AS lat, b.longitude AS lng
            """
        )
    ]

    # Actors linked to same bauwerk/projekt as mamout via 1-hop
    out["mamout_network"] = [
        dict(r)
        for r in session.run(
            """
            MATCH (a:Akteur {id: 'mamout_architectes'})-[r1]-(x)-[r2]-(other:Akteur)
            WHERE other.id <> 'mamout_architectes'
            RETURN DISTINCT other.id AS id, other.name AS name,
                   type(r1) AS r1, labels(x) AS mid_labels, x.id AS mid_id,
                   type(r2) AS r2
            LIMIT 30
            """
        )
    ]

driver.close()

out_path = Path(__file__).resolve().parent / "akteur_deep_probe.json"
out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k != "orphans"}, indent=2))
for aid, data in out["orphans"].items():
    print(f"\n{aid}: {len(data['relationships'])} rels, props={list(data['props'].keys())}")
