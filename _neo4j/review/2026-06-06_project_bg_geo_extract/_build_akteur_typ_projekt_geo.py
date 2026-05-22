"""Export Akteure: HAT_AKTEURTYP + BETEILIGT_AN→Projekt + full location data."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT_DIR = Path(__file__).resolve().parent
GEO_SOURCE = "akteur_geo_graph.json"
OUT_FILE = "akteur_typ_projekt_geo.json"

TYPE_PRIORITY = [
    "at_materialhub_bauteilboerse",
    "at_foerdergeber_programmtraeger",
    "at_software_tool_anbieter",
    "at_oeffentliche_institution",
    "at_forschung_lehre",
    "at_ngo_verband_netzwerk",
    "at_unternehmen",
    "at_person",
    "at_organisation",
    "at_unbekannt",
]


def pick_primary_type(types: list[dict]) -> dict | None:
    if not types:
        return None
    by_id = {t["id"]: t for t in types}
    for tid in TYPE_PRIORITY:
        if tid in by_id:
            return by_id[tid]
    return sorted(types, key=lambda t: t["id"])[0]


def precision_from_location(loc: dict | None) -> str:
    if not loc or not loc.get("address"):
        return "none"
    addr = loc["address"]
    if loc.get("latitude") is None:
        return "unknown"
    if any(ch.isdigit() for ch in addr):
        return "street"
    return "city"


def main() -> None:
    geo_path = OUT_DIR / GEO_SOURCE
    if not geo_path.exists():
        raise SystemExit(f"Missing {GEO_SOURCE}; run _build_akteur_geo_graph.py first.")

    geo_data = json.loads(geo_path.read_text(encoding="utf-8"))
    geo_by_id = {a["id"]: a for a in geo_data["nodes"]["akteure"]}

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    graph_rows: dict[str, dict] = {}
    links: list[dict] = []

    with driver.session(database=database) as session:
        for row in session.run(
            """
            MATCH (a:Akteur)
            OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t:Akteurtyp)
            OPTIONAL MATCH (a)-[r:BETEILIGT_AN]->(p:Projekt)
            RETURN a.id AS id, a.name AS name,
                   collect(DISTINCT {id: t.id, name: t.name}) AS typen,
                   collect(DISTINCT {
                     projekt_id: p.id,
                     projekt_name: p.name,
                     adresse: p.adresse,
                     latitude: p.latitude,
                     longitude: p.longitude,
                     geo_confidence: p.geo_confidence
                   }) AS projekte
            ORDER BY a.id
            """
        ):
            aid = row["id"]
            typen = [t for t in (row["typen"] or []) if t.get("id")]
            typen = sorted(typen, key=lambda t: t["id"])
            projekte_raw = [p for p in (row["projekte"] or []) if p.get("projekt_id")]
            projekte = []
            for p in sorted(projekte_raw, key=lambda x: x["projekt_id"]):
                geo = {
                    "address": p.get("adresse"),
                    "latitude": p.get("latitude"),
                    "longitude": p.get("longitude"),
                    "confidence": p.get("geo_confidence"),
                }
                entry = {
                    "id": p["projekt_id"],
                    "name": p.get("projekt_name"),
                    "geo": geo,
                }
                projekte.append(entry)
                links.append(
                    {
                        "type": "BETEILIGT_AN",
                        "from_id": aid,
                        "to_id": p["projekt_id"],
                        "to_kind": "Projekt",
                    }
                )
            graph_rows[aid] = {
                "id": aid,
                "name": row["name"],
                "akteurtypen": typen,
                "primary_akteurtyp": pick_primary_type(typen),
                "projekte": projekte,
            }

    driver.close()

    akteure: list[dict] = []
    by_type: dict[str, int] = {}
    with_graph_projekt = 0

    for aid in sorted(geo_by_id.keys()):
        g = graph_rows.get(aid, {})
        geo_actor = geo_by_id[aid]
        primary = geo_actor.get("primary_location")
        primary_type = g.get("primary_akteurtyp")
        if primary_type:
            by_type[primary_type["id"]] = by_type.get(primary_type["id"], 0) + 1
        if g.get("projekte"):
            with_graph_projekt += 1

        akteure.append(
            {
                "id": aid,
                "name": g.get("name") or geo_actor.get("name"),
                "akteurtypen": g.get("akteurtypen", []),
                "primary_akteurtyp": primary_type,
                "locations": geo_actor.get("locations", []),
                "primary_location": primary,
                "location_count": geo_actor.get("location_count", 0),
                "pin": {
                    "latitude": (primary or {}).get("latitude"),
                    "longitude": (primary or {}).get("longitude"),
                    "confidence": (primary or {}).get("confidence"),
                    "precision": precision_from_location(primary),
                },
                "projekte": g.get("projekte", []),
            }
        )

    # Actors only in graph query but missing from geo (should not happen)
    for aid in sorted(set(graph_rows) - set(geo_by_id)):
        g = graph_rows[aid]
        akteure.append(
            {
                "id": aid,
                "name": g["name"],
                "akteurtypen": g["akteurtypen"],
                "primary_akteurtyp": g["primary_akteurtyp"],
                "locations": [],
                "primary_location": None,
                "location_count": 0,
                "pin": {"latitude": None, "longitude": None, "confidence": None, "precision": "none"},
                "projekte": g["projekte"],
            }
        )

    export = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "database": database,
            "description": "Akteure for map: HAT_AKTEURTYP + BETEILIGT_AN→Projekt + location data",
            "location_source": GEO_SOURCE,
            "graph_edges": "BETEILIGT_AN→Projekt only (no inferred program/URL links)",
        },
        "summary": {
            "akteure_total": len(akteure),
            "with_locations": sum(1 for a in akteure if a["location_count"] > 0),
            "with_graph_projekt_link": with_graph_projekt,
            "links_total": len(links),
            "by_primary_akteurtyp": by_type,
        },
        "akteure": akteure,
        "links": links,
    }

    out_path = OUT_DIR / OUT_FILE
    out_path.write_text(json.dumps(export, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(export["summary"], indent=2))


if __name__ == "__main__":
    main()
