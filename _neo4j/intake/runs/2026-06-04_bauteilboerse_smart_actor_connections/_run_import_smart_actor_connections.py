from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

URI = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
USER = (os.environ.get("NEO4J_USER") or os.environ.get("NEO4J_USERNAME") or "neo4j").strip()
DATABASE = os.environ.get("NEO4J_DATABASE", "mit-bestand").strip()
PASSWORD_FILE = Path(".neo4j_password")

RUN = "bauteilboerse_smart_actor_connections_2026_06_04"
SOURCE_FILE = "_neo4j/intake/runs/2026-06-04_bauteilboerse_smart_actor_connections"

SOURCES = [
    {
        "url": "https://baumab-kassel.de/",
        "title": "Bauteilboerse Kassel homepage",
        "basis": "Homepage names SURAP as partner for ecological footprint / resource-analysis data and states Stadt Kassel funding.",
    },
    {
        "url": "https://baumab-kassel.de/konzept/",
        "title": "BauMaB Kassel concept",
        "basis": "Concept page says BauMaB was initiated within Stadt Kassel climate strategy and describes the gGmbH platform/store model.",
    },
    {
        "url": "https://baumab-kassel.de/impressum/",
        "title": "BauMaB Kassel imprint",
        "basis": "Imprint identifies BauMaB Kassel gGmbH and states funding by Stadt Kassel.",
    },
    {
        "url": "https://www.surap.de/",
        "title": "SURAP homepage",
        "basis": "SURAP homepage identifies SURAP GmbH as software/data provider for environmental assessment of building projects.",
    },
    {
        "url": "https://www.zirkulie.net/impressum",
        "title": "ZirkuLIE imprint",
        "basis": "Imprint identifies ZirkuLIE as Stiftung Lebenswertes Liechtenstein and names the Triesen centre contact.",
    },
    {
        "url": "https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen/bauteile-spenden",
        "title": "ZirkuLIE bauteile spenden",
        "basis": "Donation page says ZirkuLIE collects windows together with Verein Re-Win.",
    },
]

NEW_ACTORS = [
    {
        "id": "stadt_kassel",
        "name": "Stadt Kassel",
        "land": "land_deutschland",
        "types": ["at_oeffentliche_institution"],
        "roles": ["ar_oeffentliche_hand_foerderung", "ar_reuse_zirkularitaetsberatung"],
        "evidence_url": "https://baumab-kassel.de/impressum/",
        "evidence_basis": "BauMaB pages name Stadt Kassel as funding/initiating public actor for the Bauteilboerse.",
    },
    {
        "id": "surap_gmbh",
        "name": "SURAP GmbH",
        "land": "land_deutschland",
        "types": ["at_unternehmen", "at_software_tool_anbieter"],
        "roles": ["ar_software_digitalisierung", "ar_nachhaltigkeitsberatung"],
        "evidence_url": "https://www.surap.de/",
        "evidence_basis": "SURAP homepage identifies software/data tools for environmental assessment and building LCA.",
    },
    {
        "id": "stiftung_lebenswertes_liechtenstein",
        "name": "Stiftung Lebenswertes Liechtenstein",
        "land": "land_liechtenstein",
        "types": ["at_organisation", "at_ngo_verband_netzwerk"],
        "roles": ["ar_reuse_zirkularitaetsberatung", "ar_bildung_wissenstransfer"],
        "evidence_url": "https://www.zirkulie.net/impressum",
        "evidence_basis": "ZirkuLIE imprint identifies Stiftung Lebenswertes Liechtenstein as the legal body behind ZirkuLIE.",
    },
]

CONNECTIONS = [
    {
        "src": "baumab_kassel",
        "type": "VERBUNDEN_MIT_AKTEUR",
        "tgt": "stadt_kassel",
        "confidence": "belegt",
        "url": "https://baumab-kassel.de/konzept/",
        "basis": "BauMaB concept page says the project was initiated within Stadt Kassel climate strategy; footer/imprint also state Stadt Kassel funding.",
    },
    {
        "src": "baumab_kassel",
        "type": "VERBUNDEN_MIT_AKTEUR",
        "tgt": "surap_gmbh",
        "confidence": "belegt",
        "url": "https://baumab-kassel.de/",
        "basis": "BauMaB homepage says environmental footprint/resource-analysis data are provided with help from partner SURAP.",
    },
    {
        "src": "zirkulie_bauteilboerse_triesen",
        "type": "BETRIEBEN_VON",
        "tgt": "stiftung_lebenswertes_liechtenstein",
        "confidence": "belegt",
        "url": "https://www.zirkulie.net/impressum",
        "basis": "ZirkuLIE imprint identifies ZirkuLIE as Stiftung Lebenswertes Liechtenstein.",
    },
    {
        "src": "zirkulie_bauteilboerse_triesen",
        "type": "VERBUNDEN_MIT_AKTEUR",
        "tgt": "re_win",
        "confidence": "belegt",
        "url": "https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen/bauteile-spenden",
        "basis": "ZirkuLIE donation page says it collects windows together with Verein Re-Win.",
    },
]


def md5_id(url: str) -> str:
    return "q_url_" + hashlib.md5(url.encode("utf-8")).hexdigest()


def read_password() -> str:
    env_password = (os.environ.get("NEO4J_PASSWORD") or "").strip()
    if env_password:
        return env_password
    for line in PASSWORD_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    raise RuntimeError("No password found in NEO4J_PASSWORD or .neo4j_password")


def rel_id(src: str, rel_type: str, tgt: str) -> str:
    return f"r_{src}__{rel_type}__{tgt}"


def main() -> int:
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    driver = GraphDatabase.driver(URI, auth=(USER, read_password()))
    with driver:
        driver.verify_connectivity()
        with driver.session(database=DATABASE) as session:
            print(f"Connecting: {URI} db={DATABASE} user={USER}")

            qid_by_url: dict[str, str] = {}
            for src in SOURCES:
                existing = session.run(
                    "MATCH (q:Quelle {url:$url}) RETURN q.id AS id LIMIT 1",
                    url=src["url"],
                ).single()
                if existing:
                    qid = existing["id"]
                    session.run(
                        "MATCH (q:Quelle {id:$qid}) SET q.title=coalesce(q.title,$title), q.quelltyp=coalesce(q.quelltyp,'external_link')",
                        qid=qid,
                        title=src["title"],
                    ).consume()
                else:
                    qid = md5_id(src["url"])
                    session.run(
                        """
                        MERGE (q:Quelle:ExternalLink {id:$qid})
                        ON CREATE SET q.url=$url,
                                      q.title=$title,
                                      q.quelltyp='external_link'
                        SET q.url=coalesce(q.url,$url),
                            q.title=coalesce(q.title,$title),
                            q.quelltyp=coalesce(q.quelltyp,'external_link')
                        """,
                        qid=qid,
                        url=src["url"],
                        title=src["title"],
                    ).consume()
                qid_by_url[src["url"]] = qid

            for actor in NEW_ACTORS:
                aid = actor["id"]
                session.run(
                    """
                    MERGE (a:Akteur {id:$id})
                    ON CREATE SET a.name=$name
                    SET a.name=$name,
                        a.source_scope=coalesce(a.source_scope,'actor_registry_context')
                    """,
                    id=aid,
                    name=actor["name"],
                ).consume()

                session.run(
                    """
                    MATCH (a:Akteur {id:$aid}), (l:Land {id:$land})
                    MERGE (a)-[r:LIEGT_IN_LAND {id:$rid}]->(l)
                    ON CREATE SET r.created_at_utc=$created_at
                    SET r.evidence_confidence='belegt',
                        r.evidence_basis=$basis,
                        r.evidence_url=$url,
                        r.review_run=$run,
                        r.import_source_file=$source_file
                    """,
                    aid=aid,
                    land=actor["land"],
                    rid=rel_id(aid, "LIEGT_IN_LAND", actor["land"]),
                    created_at=created_at,
                    basis=actor["evidence_basis"],
                    url=actor["evidence_url"],
                    run=RUN,
                    source_file=SOURCE_FILE,
                ).consume()

                for tid in actor["types"]:
                    session.run(
                        """
                        MATCH (a:Akteur {id:$aid}), (t:Akteurtyp {id:$tid})
                        MERGE (a)-[r:HAT_AKTEURTYP {id:$rid}]->(t)
                        ON CREATE SET r.created_at_utc=$created_at
                        SET r.evidence_confidence='abgeleitet',
                            r.evidence_basis=$basis,
                            r.evidence_url=$url,
                            r.review_run=$run,
                            r.import_source_file=$source_file
                        """,
                        aid=aid,
                        tid=tid,
                        rid=rel_id(aid, "HAT_AKTEURTYP", tid),
                        created_at=created_at,
                        basis=actor["evidence_basis"],
                        url=actor["evidence_url"],
                        run=RUN,
                        source_file=SOURCE_FILE,
                    ).consume()

                for rid_target in actor["roles"]:
                    session.run(
                        """
                        MATCH (a:Akteur {id:$aid}), (role:Akteurrolle {id:$role})
                        MERGE (a)-[r:HAT_AKTEURROLLE {id:$rid}]->(role)
                        ON CREATE SET r.created_at_utc=$created_at
                        SET r.evidence_confidence='abgeleitet',
                            r.evidence_basis=$basis,
                            r.evidence_url=$url,
                            r.review_run=$run,
                            r.import_source_file=$source_file
                        """,
                        aid=aid,
                        role=rid_target,
                        rid=rel_id(aid, "HAT_AKTEURROLLE", rid_target),
                        created_at=created_at,
                        basis=actor["evidence_basis"],
                        url=actor["evidence_url"],
                        run=RUN,
                        source_file=SOURCE_FILE,
                    ).consume()

                qid = qid_by_url[actor["evidence_url"]]
                session.run(
                    """
                    MATCH (a:Akteur {id:$aid}), (q:Quelle {id:$qid})
                    MERGE (a)-[r:BELEGT_IN {id:$rid}]->(q)
                    ON CREATE SET r.created_at_utc=$created_at
                    SET r.evidence_confidence='belegt',
                        r.evidence_basis=$basis,
                        r.evidence_url=$url,
                        r.review_run=$run,
                        r.import_source_file=$source_file
                    """,
                    aid=aid,
                    qid=qid,
                    rid=rel_id(aid, "BELEGT_IN", qid),
                    created_at=created_at,
                    basis=actor["evidence_basis"],
                    url=actor["evidence_url"],
                    run=RUN,
                    source_file=SOURCE_FILE,
                ).consume()

            for conn in CONNECTIONS:
                exists = session.run(
                    "MATCH (s {id:$src}) MATCH (t {id:$tgt}) RETURN labels(s) AS sl, labels(t) AS tl",
                    src=conn["src"],
                    tgt=conn["tgt"],
                ).single()
                if not exists:
                    raise RuntimeError(f"Missing connection endpoint: {conn['src']} -> {conn['tgt']}")
                query = f"""
                MATCH (s {{id:$src}})
                MATCH (t {{id:$tgt}})
                MERGE (s)-[r:`{conn['type']}` {{id:$rid}}]->(t)
                ON CREATE SET r.created_at_utc=$created_at
                SET r.evidence_confidence=$confidence,
                    r.evidence_basis=$basis,
                    r.evidence_url=$url,
                    r.review_run=$run,
                    r.import_source_file=$source_file
                """
                session.run(
                    query,
                    src=conn["src"],
                    tgt=conn["tgt"],
                    rid=rel_id(conn["src"], conn["type"], conn["tgt"]),
                    created_at=created_at,
                    confidence=conn["confidence"],
                    basis=conn["basis"],
                    url=conn["url"],
                    run=RUN,
                    source_file=SOURCE_FILE,
                ).consume()

            touched = session.run(
                "MATCH ()-[r {review_run:$run}]->() RETURN count(r) AS n",
                run=RUN,
            ).single()["n"]
            missing_ids = session.run(
                """
                MATCH (a)-[r]->()
                WHERE a.id IN ['baumab_kassel','zirkulie_bauteilboerse_triesen','stadt_kassel','surap_gmbh','stiftung_lebenswertes_liechtenstein']
                  AND r.id IS NULL
                RETURN count(r) AS n
                """
            ).single()["n"]

            print(f"Relationships touched with review_run={RUN}: {touched}")
            print(f"Relevant outgoing relationships missing r.id: {missing_ids}")

            for row in session.run(
                """
                MATCH (b)-[r]->(a:Akteur)
                WHERE b.id IN ['baumab_kassel','zirkulie_bauteilboerse_triesen']
                  AND type(r) IN ['VERBUNDEN_MIT_AKTEUR','BETRIEBEN_VON']
                  AND r.review_run=$run
                RETURN b.id AS bauteilboerse, type(r) AS rel, a.id AS actor, r.evidence_url AS evidence_url
                ORDER BY bauteilboerse, rel, actor
                """,
                run=RUN,
            ):
                print(dict(row))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
