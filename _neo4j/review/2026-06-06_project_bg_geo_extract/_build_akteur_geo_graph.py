"""Build unified Akteur location JSON from graph + geo extract."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT_DIR = Path(__file__).resolve().parent
RUN = "2026-06-06_akteur_geo_extract"

def load_evidence_registry() -> dict:
    return load_json("akteur_evidence_registry.json")

LAND_CAPITAL: dict[str, dict] = {
    "land_deutschland": {"address": "Berlin, Germany", "lat": 52.52, "lng": 13.405, "stadt_id": "stadt_berlin"},
    "land_schweiz": {"address": "Bern, Switzerland", "lat": 46.948, "lng": 7.4474, "stadt_id": "stadt_bern"},
    "land_niederlande": {"address": "Amsterdam, Netherlands", "lat": 52.3730796, "lng": 4.8924534, "stadt_id": "stadt_amsterdam"},
    "land_belgien": {"address": "Brussels, Belgium", "lat": 50.8465573, "lng": 4.351697, "stadt_id": "stadt_bruessel"},
    "land_frankreich": {"address": "Paris, France", "lat": 48.8566, "lng": 2.3522, "stadt_id": "stadt_paris"},
    "land_vereinigtes_koenigreich": {"address": "London, UK", "lat": 51.5074, "lng": -0.1278, "stadt_id": "stadt_london"},
    "land_daenemark": {"address": "Copenhagen, Denmark", "lat": 55.6761, "lng": 12.5683, "stadt_id": "stadt_copenhagen"},
    "land_finland": {"address": "Helsinki, Finland", "lat": 60.1699, "lng": 24.9384, "stadt_id": "stadt_helsinki"},
    "land_oesterreich": {"address": "Vienna, Austria", "lat": 48.2082, "lng": 16.3738, "stadt_id": "stadt_wien"},
    "land_usa": {"address": "United States", "lat": 38.9072, "lng": -77.0369, "stadt_id": None},
    "land_norwegen": {"address": "Oslo, Norway", "lat": 59.9139, "lng": 10.7522, "stadt_id": "stadt_oslo"},
    "land_italien": {"address": "Rome, Italy", "lat": 41.9028, "lng": 12.4964, "stadt_id": None},
    "land_luxemburg": {"address": "Luxembourg", "lat": 49.6116, "lng": 6.1319, "stadt_id": "stadt_luxemburg"},
    "land_irland": {"address": "Dublin, Ireland", "lat": 53.3498, "lng": -6.2603, "stadt_id": None},
    "land_spanien": {"address": "Madrid, Spain", "lat": 40.4168, "lng": -3.7038, "stadt_id": None},
    "land_portugal": {"address": "Lisbon, Portugal", "lat": 38.7223, "lng": -9.1393, "stadt_id": None},
    "land_tschechien": {"address": "Prague, Czechia", "lat": 50.0755, "lng": 14.4378, "stadt_id": None},
    "land_polen": {"address": "Warsaw, Poland", "lat": 52.2297, "lng": 21.0122, "stadt_id": None},
    "land_finnland": {"address": "Helsinki, Finland", "lat": 60.1699, "lng": 24.9384, "stadt_id": "stadt_helsinki"},
}

COUNTRY_NAME_TOKENS: dict[str, str] = {
    "switzerland": "land_schweiz",
    "schweiz": "land_schweiz",
    "deutschland": "land_deutschland",
    "germany": "land_deutschland",
    "belgium": "land_belgien",
    "belgien": "land_belgien",
    "netherlands": "land_niederlande",
    "niederlande": "land_niederlande",
    "france": "land_frankreich",
    "frankreich": "land_frankreich",
    "finland": "land_finnland",
    "finnland": "land_finnland",
    "denmark": "land_daenemark",
    "daenemark": "land_daenemark",
    "austria": "land_oesterreich",
    "oesterreich": "land_oesterreich",
}

PROJEKT_SLUG_MAP: dict[str, str] = {
    "building-k-118": "p_k118_kopfbau_halle_118_winterthur",
    "k-118-kopfbau-halle-118": "p_k118_kopfbau_halle_118_winterthur",
    "culture-commercial-center-elys": "p_elys_kultur_gewerbehaus_basel",
    "lysp8": "p_lysp8_basel",
    "recycling-center-juch-areal": "p_juch_areal_recyclingzentrum_zuerich",
    "recyclingzentrum-juch-areal": "p_juch_areal_recyclingzentrum_zuerich",
    "erz-juchareal": "p_juch_areal_recyclingzentrum_zuerich",
    "crclr-house-berlin": "p_crclr_house_impact_hub_berlin",
    "bluecity-offices": "p_bluecity_offices_rotterdam",
    "stuttgart-210": "p_stuttgart_210_hft",
}

TLD_COUNTRY: dict[str, str] = {
    ".ch": "land_schweiz",
    ".de": "land_deutschland",
    ".nl": "land_niederlande",
    ".fr": "land_frankreich",
    ".be": "land_belgien",
    ".fi": "land_finnland",
    ".dk": "land_daenemark",
    ".at": "land_oesterreich",
}

MANUAL_CITIES: dict[str, dict] = {
    "triesen": {
        "address": "Triesen, Liechtenstein",
        "lat": 47.107,
        "lng": 9.528,
        "confidence": "medium",
        "source": "city token in actor id (Bauteilbörse Triesen)",
    },
    "liechtenstein": {
        "address": "Vaduz, Liechtenstein",
        "lat": 47.141,
        "lng": 9.521,
        "confidence": "low",
        "source": "country token in actor id/name",
    },
}


def norm_token(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_json(name: str):
    return json.loads((OUT_DIR / name).read_text(encoding="utf-8"))


def build_projekt_url_index(projekte: dict) -> list[tuple[str, str]]:
    index: list[tuple[str, str]] = []
    for pid, p in projekte.items():
        urls = list(p.get("source_urls") or [])
        if p.get("source_url"):
            urls.append(p["source_url"])
        for u in urls:
            if u:
                index.append((u.lower().rstrip("/"), pid))
    return index


def projekte_from_source_urls(actor_urls: list[str], url_index: list[tuple[str, str]]) -> set[str]:
    matched: set[str] = set()
    for au in actor_urls or []:
        au_norm = (au or "").lower().rstrip("/")
        if not au_norm:
            continue
        slug = au_norm.split("/")[-1]
        if slug in PROJEKT_SLUG_MAP:
            matched.add(PROJEKT_SLUG_MAP[slug])
        for pu, pid in url_index:
            if au_norm == pu or au_norm in pu or pu in au_norm:
                matched.add(pid)
            elif slug and len(slug) >= 6 and slug in pu:
                matched.add(pid)
    return matched


def land_from_tlds(actor_urls: list[str]) -> set[str]:
    lands: set[str] = set()
    for au in actor_urls or []:
        low = (au or "").lower()
        for tld, lid in TLD_COUNTRY.items():
            if tld in low:
                lands.add(lid)
    return lands


def loc_entry(
    role: str,
    address: str,
    lat: float | None = None,
    lng: float | None = None,
    confidence: str = "low",
    source: str = "",
    source_url: str = "",
    **extra,
) -> dict:
    return {
        "role": role,
        "address": address,
        "latitude": lat,
        "longitude": lng,
        "confidence": confidence,
        "source": source,
        "source_url": source_url or "",
        **extra,
    }


def pick_primary(locations: list[dict]) -> dict | None:
    if not locations:
        return None
    rank = {"high": 3, "medium": 2, "low": 1}
    role_rank = {
        "known_office": 7,
        "archive_case_site": 6,
        "linked_projekt": 5,
        "bauwerk_geo": 5,
        "source_url_projekt": 4,
        "program_projekt": 4,
        "co_actor_location": 3,
        "city_in_name": 3,
        "country_in_name": 2,
        "land_capital": 1,
    }

    def score(loc: dict) -> tuple:
        has_coords = 1 if loc.get("latitude") is not None else 0
        street = 1 if re.search(r"\d", loc.get("address", "")) else 0
        return (
            rank.get(loc.get("confidence", "low"), 0),
            role_rank.get(loc.get("role", ""), 0),
            street,
            has_coords,
        )

    return max(locations, key=score)


def fetch_graph_extras(session) -> tuple[dict, dict, dict, dict]:
    program_map: dict[str, list[str]] = {}
    for row in session.run(
        """
        MATCH (a:Akteur)-[:BETEILIGT_AN]->(pr:Programm)
        OPTIONAL MATCH (p:Projekt)-[:TEIL_VON_PROGRAMM]->(pr)
        WITH a, collect(DISTINCT p.id) AS pids
        RETURN a.id AS aid, [x IN pids WHERE x IS NOT NULL] AS projekt_ids
        """
    ):
        if row["projekt_ids"]:
            program_map[row["aid"]] = row["projekt_ids"]

    verbunden_map: dict[str, list[str]] = {}
    for row in session.run(
        """
        MATCH (a:Akteur)-[:VERBUNDEN_MIT_AKTEUR]-(b:Akteur)
        RETURN a.id AS aid, collect(DISTINCT b.id) AS peers
        """
    ):
        verbunden_map[row["aid"]] = row["peers"]

    bauwerk_map: dict[str, list[dict]] = {}
    for row in session.run(
        """
        MATCH (a:Akteur)-[:NUTZT_BAUWERK|HAT_BAUWERK]->(b:Bauwerk)
        WHERE b.adresse IS NOT NULL
        RETURN a.id AS aid,
               collect(DISTINCT {id: b.id, adresse: b.adresse, lat: b.latitude, lng: b.longitude}) AS bw
        """
    ):
        bauwerk_map[row["aid"]] = row["bw"]

    program_ids_map: dict[str, list[str]] = {}
    for row in session.run(
        """
        MATCH (a:Akteur)-[:BETEILIGT_AN]->(pr:Programm)
        RETURN a.id AS aid, collect(DISTINCT pr.id) AS program_ids
        """
    ):
        program_ids_map[row["aid"]] = row["program_ids"]

    return program_map, verbunden_map, bauwerk_map, program_ids_map


def main() -> None:
    evidence = load_evidence_registry()
    known_offices: dict[str, dict] = evidence.get("known_offices", {})
    archive_cases: dict[str, dict] = evidence.get("archive_case_sites", {})
    program_proxy: dict[str, dict] = evidence.get("program_projekt_proxy", {})
    actor_archive_cases: dict[str, list[str]] = {}
    for case_id, case in archive_cases.items():
        for actor_id in case.get("actor_ids", []):
            actor_archive_cases.setdefault(actor_id, []).append(case_id)

    projekte = {p["projekt_id"]: p for p in load_json("projekte_addresses.json")}
    url_index = build_projekt_url_index(projekte)
    staedte = {s["stadt_id"]: s for s in load_json("staedte_geocoded.json")}
    stadt_by_token: dict[str, str] = {}
    for sid, s in staedte.items():
        for token in re.split(r"[/,\s]+", s["stadt_name"].lower()):
            t = norm_token(token)
            if len(t) >= 4:
                stadt_by_token[t] = sid

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    actors: list[dict] = []
    relationships: list[dict] = []

    with driver.session(database=database) as session:
        program_map, verbunden_map, bauwerk_map, program_ids_map = fetch_graph_extras(session)
        rows = session.run(
            """
            MATCH (a:Akteur)
            OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t:Akteurtyp)
            OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(r:Akteurrolle)
            OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(l:Land)
            OPTIONAL MATCH (a)-[:BETEILIGT_AN]->(p:Projekt)
            RETURN a.id AS id, a.name AS name, a.source_urls AS source_urls,
                   a.source_titles AS source_titles,
                   collect(DISTINCT t.name) AS types,
                   collect(DISTINCT r.name) AS roles,
                   collect(DISTINCT l.id) AS land_ids,
                   collect(DISTINCT l.name) AS land_names,
                   collect(DISTINCT p.id) AS projekt_ids
            ORDER BY a.id
            """
        )
        for row in rows:
            aid = row["id"]
            locations: list[dict] = []

            if aid in known_offices:
                k = known_offices[aid]
                locations.append(
                    loc_entry(
                        "known_office",
                        k["address"],
                        k.get("latitude"),
                        k.get("longitude"),
                        k.get("confidence", "medium"),
                        k.get("source", "curated_registry"),
                        k.get("source_url", ""),
                    )
                )

            for case_id in actor_archive_cases.get(aid, []):
                case = archive_cases[case_id]
                locations.append(
                    loc_entry(
                        "archive_case_site",
                        case["address"],
                        case.get("latitude"),
                        case.get("longitude"),
                        case.get("confidence", "medium"),
                        case.get("source", f"archive case {case_id}"),
                        case.get("source_url", ""),
                        archive_case_id=case_id,
                        related_projekt_id=case.get("related_projekt_id"),
                    )
                )
                relationships.append(
                    {
                        "type": "ARCHIVE_CASE",
                        "from_id": aid,
                        "to_id": case_id,
                        "related_projekt_id": case.get("related_projekt_id"),
                    }
                )

            linked_pids = set(row["projekt_ids"] or [])
            linked_pids |= projekte_from_source_urls(list(row["source_urls"] or []), url_index)
            linked_pids |= set(program_map.get(aid, []))
            for prog_id in program_ids_map.get(aid, []):
                proxy = program_proxy.get(prog_id, {})
                linked_pids |= set(proxy.get("projekt_ids", []))

            for bw in bauwerk_map.get(aid, []):
                locations.append(
                    loc_entry(
                        "bauwerk_geo",
                        bw["adresse"],
                        bw.get("lat"),
                        bw.get("lng"),
                        "medium",
                        f"NUTZT_BAUWERK/HAT_BAUWERK → {bw['id']}",
                        bauwerk_id=bw["id"],
                    )
                )
                relationships.append(
                    {"type": "BAUWERK_GEO", "from_id": aid, "to_id": bw["id"], "has_bauwerk_geo": True}
                )

            for pid in sorted(linked_pids):
                p = projekte.get(pid)
                if not p or not p.get("address"):
                    continue
                via_graph = pid in (row["projekt_ids"] or [])
                via_program = pid in set(program_map.get(aid, []))
                via_proxy = any(
                    pid in program_proxy.get(prog_id, {}).get("projekt_ids", [])
                    for prog_id in program_ids_map.get(aid, [])
                )
                if via_graph:
                    role, source = "linked_projekt", f"BETEILIGT_AN → {pid}"
                elif via_program:
                    role, source = "program_projekt", f"Programm → TEIL_VON_PROGRAMM → {pid}"
                elif via_proxy:
                    role, source = "program_projekt", f"Programm proxy → {pid}"
                else:
                    role, source = "source_url_projekt", f"source_url overlap → {pid}"
                locations.append(
                    loc_entry(
                        role,
                        p["address"],
                        p.get("latitude"),
                        p.get("longitude"),
                        p.get("confidence", "medium"),
                        source,
                        p.get("source_url", ""),
                        linked_projekt_id=pid,
                        linked_projekt_name=p.get("projekt_name", ""),
                    )
                )
                if via_graph:
                    relationships.append(
                        {"type": "BETEILIGT_AN", "from_id": aid, "to_id": pid, "has_projekt_geo": True}
                    )
                else:
                    relationships.append(
                        {"type": "INFERRED_PROJEKT_GEO", "from_id": aid, "to_id": pid, "has_projekt_geo": True}
                    )

            for lid, lname in zip(row["land_ids"] or [], row["land_names"] or []):
                relationships.append({"type": "LIEGT_IN_LAND", "from_id": aid, "to_id": lid, "to_name": lname})
                cap = LAND_CAPITAL.get(lid)
                if cap:
                    locations.append(
                        loc_entry(
                            "land_capital",
                            cap["address"],
                            cap["lat"],
                            cap["lng"],
                            "low",
                            f"LIEGT_IN_LAND → {lname}",
                            stadt_id=cap.get("stadt_id"),
                            land_id=lid,
                        )
                    )

            hay = f"{aid} {row['name']} {' '.join(row['source_urls'] or [])}".lower()
            hay_norm = norm_token(hay)

            matched_cities: set[str] = set()
            for token, sid in stadt_by_token.items():
                if token in hay_norm and sid not in matched_cities:
                    matched_cities.add(sid)
                    s = staedte[sid]
                    locations.append(
                        loc_entry(
                            "city_in_name",
                            s.get("display_name") or s["stadt_name"],
                            s.get("lat"),
                            s.get("lng"),
                            "medium",
                            f"city token '{token}' in actor id/name/urls",
                            stadt_id=sid,
                        )
                    )

            for token, mc in MANUAL_CITIES.items():
                if token in hay_norm:
                    locations.append(
                        loc_entry(
                            "city_in_name",
                            mc["address"],
                            mc["lat"],
                            mc["lng"],
                            mc.get("confidence", "low"),
                            mc.get("source", f"manual city token '{token}'"),
                        )
                    )

            inferred_lands: set[str] = set()
            for token, lid in COUNTRY_NAME_TOKENS.items():
                if token in hay_norm:
                    inferred_lands.add(lid)
            inferred_lands |= land_from_tlds(list(row["source_urls"] or []))
            for lid in inferred_lands:
                cap = LAND_CAPITAL.get(lid)
                if cap:
                    locations.append(
                        loc_entry(
                            "country_in_name",
                            cap["address"],
                            cap["lat"],
                            cap["lng"],
                            "low",
                            f"country inference → {lid}",
                            land_id=lid,
                            stadt_id=cap.get("stadt_id"),
                        )
                    )

            # Deduplicate locations by address+role
            seen: set[str] = set()
            deduped: list[dict] = []
            for loc in locations:
                key = f"{loc['role']}|{loc['address']}"
                if key in seen:
                    continue
                seen.add(key)
                deduped.append(loc)

            primary = pick_primary(deduped)
            actors.append(
                {
                    "id": aid,
                    "name": row["name"],
                    "types": sorted(set(row["types"] or [])),
                    "roles": sorted(set(row["roles"] or [])),
                    "source_urls": list(row["source_urls"] or []),
                    "relationships": {
                        "land_ids": sorted(set(row["land_ids"] or [])),
                        "program_ids": sorted(set(program_ids_map.get(aid, []))),
                        "verbunden_actor_ids": sorted(set(verbunden_map.get(aid, []))),
                        "projekt_ids": sorted(linked_pids),
                    },
                    "locations": deduped,
                    "primary_location": primary,
                    "location_count": len(deduped),
                }
            )

    driver.close()

    primary_by_id = {a["id"]: a["primary_location"] for a in actors if a["primary_location"]}
    for actor in actors:
        if actor["location_count"] > 0:
            continue
        for peer_id in actor["relationships"].get("verbunden_actor_ids", []):
            peer_loc = primary_by_id.get(peer_id)
            if not peer_loc:
                continue
            actor["locations"].append(
                loc_entry(
                    "co_actor_location",
                    peer_loc["address"],
                    peer_loc.get("latitude"),
                    peer_loc.get("longitude"),
                    "low",
                    f"VERBUNDEN_MIT_AKTEUR → {peer_id}",
                    co_actor_id=peer_id,
                )
            )
            relationships.append(
                {"type": "INHERITED_FROM_AKTEUR", "from_id": actor["id"], "to_id": peer_id}
            )
            break
        if actor["locations"]:
            actor["location_count"] = len(actor["locations"])
            actor["primary_location"] = pick_primary(actor["locations"])
            primary_by_id[actor["id"]] = actor["primary_location"]

    without_location = [a["id"] for a in actors if a["location_count"] == 0]
    with_coords = sum(1 for a in actors if a["primary_location"] and a["primary_location"].get("latitude") is not None)
    with_address = sum(1 for a in actors if a["primary_location"] and a["primary_location"].get("address"))
    with_street = sum(
        1
        for a in actors
        if a["primary_location"] and re.search(r"\d", a["primary_location"].get("address", ""))
    )
    multi_loc = sum(1 for a in actors if a["location_count"] > 1)

    unified = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "database": database,
            "run": RUN,
            "description": "Akteur locations: graph paths, evidence registry, archive cases, program proxies, Bauwerk geo, co-actor inheritance",
            "evidence_registry": "akteur_evidence_registry.json",
        },
        "summary": {
            "akteure_total": len(actors),
            "with_primary_location": with_address,
            "with_coordinates": with_coords,
            "with_street_address": with_street,
            "with_multiple_locations": multi_loc,
            "without_location": len(without_location),
            "without_location_ids": without_location,
            "known_office_registry": len(known_offices),
            "archive_case_sites": len(archive_cases),
            "by_primary_role": {},
        },
        "nodes": {"akteure": actors},
        "relationships": relationships,
    }

    role_counts: dict[str, int] = {}
    for a in actors:
        if a["primary_location"]:
            r = a["primary_location"]["role"]
            role_counts[r] = role_counts.get(r, 0) + 1
    unified["summary"]["by_primary_role"] = role_counts

    out_path = OUT_DIR / "akteur_geo_graph.json"
    out_path.write_text(json.dumps(unified, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Compact CSV for quick review
    csv_lines = ["akteur_id,name,primary_role,address,latitude,longitude,confidence,location_count"]
    for a in actors:
        pl = a["primary_location"] or {}
        csv_lines.append(
            ",".join(
                [
                    a["id"],
                    json.dumps(a["name"], ensure_ascii=False),
                    pl.get("role", ""),
                    json.dumps(pl.get("address", ""), ensure_ascii=False),
                    str(pl.get("latitude") or ""),
                    str(pl.get("longitude") or ""),
                    pl.get("confidence", ""),
                    str(a["location_count"]),
                ]
            )
        )
    (OUT_DIR / "akteure_locations.csv").write_text("\n".join(csv_lines) + "\n", encoding="utf-8")
    if without_location:
        (OUT_DIR / "akteure_without_location.csv").write_text(
            "akteur_id\n" + "\n".join(without_location) + "\n", encoding="utf-8"
        )

    print(json.dumps({k: v for k, v in unified["summary"].items() if k != "without_location_ids"}, indent=2))


if __name__ == "__main__":
    main()
