"""Build single unified geo JSON with nodes, relationships, and addresses."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT_DIR = Path(__file__).resolve().parent


def load_json(name: str):
    return json.loads((OUT_DIR / name).read_text(encoding="utf-8"))


def addr_node(record: dict, role: str) -> dict:
    return {
        "address": record.get("address") or "",
        "latitude": record.get("latitude"),
        "longitude": record.get("longitude"),
        "confidence": record.get("confidence") or "",
        "evidence_status": record.get("evidence_status") or "",
        "source_url": record.get("source_url") or "",
        "role": role,
    }


def main() -> None:
    projekte = {p["projekt_id"]: p for p in load_json("projekte_addresses.json")}
    donors = {d["bauwerk_id"]: d for d in load_json("donor_bauwerke_addresses.json")}
    bgs_raw = load_json("bauteilgruppen.json")
    orphan_evidence = load_json("evidence_deep_dive.json").get("orphan_bauteilgruppen", {})

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    rels: dict[str, list[dict]] = {}
    receiver_bauwerke: dict[str, dict] = {}
    with driver.session(database=database) as session:
        rel_queries = {
            "HAT_BAUTEILGRUPPE": """
                MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
                RETURN p.id AS from_id, bg.id AS to_id
            """,
            "AUS_SPENDER": """
                MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER]->(bw:Bauwerk)
                RETURN bg.id AS from_id, bw.id AS to_id
            """,
            "IN_EMPFANGSOBJEKT": """
                MATCH (bg:Bauteilgruppe)-[:IN_EMPFANGSOBJEKT]->(bw:Bauwerk)
                RETURN bg.id AS from_id, bw.id AS to_id
            """,
            "LIEGT_IN_STADT_PROJEKT": """
                MATCH (p:Projekt)-[:LIEGT_IN_STADT]->(s:Stadt)
                RETURN p.id AS from_id, s.id AS to_id, s.name AS to_name
            """,
            "LIEGT_IN_STADT_BAUWERK": """
                MATCH (bw:Bauwerk)-[:LIEGT_IN_STADT]->(s:Stadt)
                RETURN bw.id AS from_id, s.id AS to_id, s.name AS to_name
            """,
        }
        for rel_type, q in rel_queries.items():
            rels[rel_type] = [dict(r) for r in session.run(q)]

        for row in session.run(
            """
            MATCH (bg:Bauteilgruppe)-[:IN_EMPFANGSOBJEKT]->(bw:Bauwerk)
            OPTIONAL MATCH (bw)-[:LIEGT_IN_STADT]->(s:Stadt)
            OPTIONAL MATCH (bw)-[:LIEGT_IN_LAND]->(l:Land)
            RETURN bw.id AS id, bw.name AS name,
                   collect(DISTINCT s.name) AS staedte,
                   collect(DISTINCT l.name) AS laender
            """
        ):
            receiver_bauwerke[row["id"]] = dict(row)

    driver.close()

    # Index relationships
    projekt_to_bg: dict[str, list[str]] = {}
    for r in rels["HAT_BAUTEILGRUPPE"]:
        projekt_to_bg.setdefault(r["from_id"], []).append(r["to_id"])

    bg_to_donor: dict[str, list[str]] = {}
    for r in rels["AUS_SPENDER"]:
        bg_to_donor.setdefault(r["from_id"], []).append(r["to_id"])

    bg_to_receiver_bw: dict[str, list[str]] = {}
    for r in rels["IN_EMPFANGSOBJEKT"]:
        bg_to_receiver_bw.setdefault(r["from_id"], []).append(r["to_id"])

    bg_to_projekt: dict[str, str] = {}
    for r in rels["HAT_BAUTEILGRUPPE"]:
        bg_to_projekt[r["to_id"]] = r["from_id"]

    receiver_bw_geo: dict[str, dict] = {}
    for bgid, rbids in bg_to_receiver_bw.items():
        pid = bg_to_projekt.get(bgid)
        if not pid or pid not in projekte:
            continue
        geo = addr_node(projekte[pid], "receiver_bauwerk")
        for rbid in rbids:
            receiver_bw_geo.setdefault(rbid, geo)

    # Build Bauteilgruppe nodes with embedded relationship refs
    bauteilgruppen: list[dict] = []
    for b in bgs_raw:
        bgid = b["bauteilgruppe_id"]
        pid = b["projekt_ids"][0] if b["projekt_ids"] else None
        p = projekte.get(pid, {}) if pid else {}

        donor_ids = bg_to_donor.get(bgid, [])
        receiver_bw_ids = bg_to_receiver_bw.get(bgid, [])

        orphan = orphan_evidence.get(bgid) if not pid else None

        entry = {
            "id": bgid,
            "name": b["bauteilgruppe_name"],
            "reuse_status": b.get("reuse_status"),
            "wiederverwendungsort": b.get("wiederverwendungsort") or [],
            "relationships": {
                "projekt_id": pid,
                "donor_bauwerk_ids": donor_ids,
                "receiver_bauwerk_ids": receiver_bw_ids,
            },
            "receiver": {
                "projekt": {
                    "id": pid,
                    "name": p.get("projekt_name") or (b["projekt_names"][0] if b["projekt_names"] else ""),
                    "staedte": p.get("staedte") or ";".join(b.get("projekt_staedte") or []),
                    "geo": addr_node(p, "receiver_projekt") if pid else None,
                }
                if pid
                else None,
                "bauwerke": [
                    {
                        "id": rbid,
                        "name": receiver_bauwerke.get(rbid, {}).get("name", ""),
                        "staedte": receiver_bauwerke.get(rbid, {}).get("staedte") or [],
                        "geo": receiver_bw_geo.get(rbid),
                    }
                    for rbid in receiver_bw_ids
                ],
            },
            "donors": [
                {
                    "bauwerk_id": did,
                    "name": donors[did]["bauwerk_name"] if did in donors else "",
                    "geo": addr_node(donors[did], "donor_bauwerk") if did in donors else None,
                }
                for did in donor_ids
            ],
        }
        if orphan and not pid:
            entry["orphan_evidence"] = {
                "linked_program": orphan.get("linked_program", ""),
                "geo": addr_node(
                    {
                        "address": orphan.get("address", ""),
                        "latitude": None,
                        "longitude": None,
                        "confidence": orphan.get("confidence", "low"),
                        "evidence_status": orphan.get("evidence_status", ""),
                        "source_url": orphan.get("source_url", ""),
                    },
                    "orphan_program",
                ),
            }
        bauteilgruppen.append(entry)

    # Projekt nodes with nested BG refs
    projekt_nodes = []
    for pid, p in sorted(projekte.items()):
        bg_ids = sorted(projekt_to_bg.get(pid, []))
        projekt_nodes.append(
            {
                "id": pid,
                "name": p["projekt_name"],
                "staedte": p.get("staedte", ""),
                "geo": addr_node(p, "projekt_site"),
                "relationships": {"bauteilgruppe_ids": bg_ids},
            }
        )

    # Bauwerk nodes (donors + receivers from graph)
    all_bw_ids = set(donors) | set(receiver_bauwerke)
    bauwerk_nodes = []
    for bid in sorted(all_bw_ids):
        is_donor = bid in donors
        d = donors.get(bid, {})
        rb = receiver_bauwerke.get(bid, {})
        linked_bgs_donor = [r["from_id"] for r in rels["AUS_SPENDER"] if r["to_id"] == bid]
        linked_bgs_recv = [r["from_id"] for r in rels["IN_EMPFANGSOBJEKT"] if r["to_id"] == bid]
        donor_geo = addr_node(d, "donor_bauwerk") if is_donor else None
        recv_geo = receiver_bw_geo.get(bid)
        bauwerk_nodes.append(
            {
                "id": bid,
                "name": d.get("bauwerk_name") or rb.get("name", ""),
                "roles": {
                    "donor_for_bauteilgruppe_ids": linked_bgs_donor,
                    "receiver_for_bauteilgruppe_ids": linked_bgs_recv,
                },
                "staedte": d.get("staedte") or ";".join(rb.get("staedte") or []),
                "laender": d.get("laender") or ";".join(rb.get("laender") or []),
                "geo": {
                    "donor": donor_geo,
                    "receiver": recv_geo,
                },
            }
        )

    # Flat relationship list (for map/graph tools)
    relationships = []
    for rel_type, rows in rels.items():
        for r in rows:
            relationships.append(
                {
                    "type": rel_type,
                    "from_id": r["from_id"],
                    "to_id": r["to_id"],
                    **({"to_name": r["to_name"]} if "to_name" in r else {}),
                }
            )

    summary = load_json("address_summary.json")

    unified = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "database": database,
            "description": "Unified reuse geo graph: Projekte, Bauteilgruppen, donor/receiver Bauwerke with addresses",
        },
        "summary": summary,
        "nodes": {
            "projekte": projekt_nodes,
            "bauteilgruppen": bauteilgruppen,
            "bauwerke": bauwerk_nodes,
        },
        "relationships": relationships,
        "reuse_chains": [
            {
                "bauteilgruppe_id": bg["id"],
                "bauteilgruppe_name": bg["name"],
                "donor_bauwerk_ids": bg["relationships"]["donor_bauwerk_ids"],
                "receiver_projekt_id": bg["relationships"]["projekt_id"],
                "receiver_bauwerk_ids": bg["relationships"]["receiver_bauwerk_ids"],
                "donor_addresses": [d["geo"]["address"] for d in bg["donors"] if d.get("geo")],
                "receiver_address": (
                    bg["receiver"]["projekt"]["geo"]["address"]
                    if bg["receiver"] and bg["receiver"].get("projekt")
                    else (
                        next(
                            (
                                bw["geo"]["address"]
                                for bw in (bg["receiver"] or {}).get("bauwerke", [])
                                if bw.get("geo")
                            ),
                            "",
                        )
                    )
                ),
                "donor_coordinates": [
                    {"latitude": d["geo"]["latitude"], "longitude": d["geo"]["longitude"]}
                    for d in bg["donors"]
                    if d.get("geo") and d["geo"].get("latitude") is not None
                ],
                "receiver_coordinates": (
                    {
                        "latitude": bg["receiver"]["projekt"]["geo"]["latitude"],
                        "longitude": bg["receiver"]["projekt"]["geo"]["longitude"],
                    }
                    if bg["receiver"]
                    and bg["receiver"].get("projekt")
                    and bg["receiver"]["projekt"]["geo"].get("latitude") is not None
                    else next(
                        (
                            {
                                "latitude": bw["geo"]["latitude"],
                                "longitude": bw["geo"]["longitude"],
                            }
                            for bw in (bg["receiver"] or {}).get("bauwerke", [])
                            if bw.get("geo") and bw["geo"].get("latitude") is not None
                        ),
                        None,
                    )
                ),
            }
            for bg in bauteilgruppen
            if bg["relationships"]["donor_bauwerk_ids"] or bg["relationships"]["projekt_id"]
        ],
    }

    out_path = OUT_DIR / "reuse_geo_graph.json"
    out_path.write_text(json.dumps(unified, indent=2, ensure_ascii=False), encoding="utf-8")

    stats = {
        "projekte": len(projekt_nodes),
        "bauteilgruppen": len(bauteilgruppen),
        "bauwerke": len(bauwerk_nodes),
        "relationships": len(relationships),
        "reuse_chains": len(unified["reuse_chains"]),
        "output": str(out_path),
    }
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
