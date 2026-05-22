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

RUN = "more_bauteilboersen_graph_addition_2026_06_04"
SOURCE_FILE = "_neo4j/intake/runs/2026-06-04_more_bauteilboersen_graph_addition"


def md5_id(url: str) -> str:
    return "q_url_" + hashlib.md5(url.encode("utf-8")).hexdigest()


ACTORS = [
    {
        "id": "baumab_kassel",
        "name": "BauMaB Kassel / Bauteilbörse Kassel",
        "land": {"id": "land_deutschland", "name": "Deutschland", "create": False},
        "sources": [
            ("https://baumab-kassel.de/", "BauMaB Kassel homepage", "Homepage states used building materials/components can be bought and sold online and in Kassel Hafenquartier."),
            ("https://baumab-kassel.de/bauteilboerse/", "BauMaB Kassel offers", "Offer list exposes product categories, prices, dimensions, condition, availability, hazard suspicion, BIM filter, and pickup/no-shipping signal."),
            ("https://baumab-kassel.de/kaufen/", "BauMaB Kassel buy workflow", "Buy page describes online offers, reservation before deconstruction/demolition, cart, reserve/direct purchase, and physical retail location."),
            ("https://baumab-kassel.de/verkaufen/", "BauMaB Kassel sell workflow", "Sell page names windows, doors, electronics/building services, sanitary objects and describes pre-demolition capture and publication."),
            ("https://baumab-kassel.de/konzept/", "BauMaB Kassel concept", "Concept page says the gGmbH operates a physical retail place and digital platform to record, evaluate, mediate, and temporarily store building materials/components."),
            ("https://baumab-kassel.de/impressum/", "BauMaB Kassel imprint", "Imprint identifies BauMaB Kassel gGmbH at Hafenstrasse 76, 34125 Kassel."),
        ],
        "belegt_in": [
            "https://baumab-kassel.de/",
            "https://baumab-kassel.de/bauteilboerse/",
            "https://baumab-kassel.de/kaufen/",
            "https://baumab-kassel.de/verkaufen/",
            "https://baumab-kassel.de/impressum/",
        ],
        "edges": [
            ("HAT_AKTEURTYP", "at_materialhub_bauteilboerse", "belegt", "https://baumab-kassel.de/", "First-party homepage identifies the Bauteilboerse as buy/sell platform for used building materials/components."),
            ("HAT_MARKTMODELL", "mm_kauf_gebraucht", "belegt", "https://baumab-kassel.de/kaufen/", "Buy page supports reserve/direct purchase and cart workflow for used components."),
            ("HAT_GESCHAEFTSMODELL", "gm_marketplace_vermittlung", "belegt", "https://baumab-kassel.de/kaufen/", "Platform mediates offers from providers to buyers, including pre-demolition reservation."),
            ("HAT_GESCHAEFTSMODELL", "gm_shop_eigenstock", "belegt", "https://baumab-kassel.de/", "Homepage and concept page describe physical sales/storage location in Kassel."),
            ("HAT_GESCHAEFTSMODELL", "gm_dienstleistung_urban_mining", "abgeleitet", "https://baumab-kassel.de/konzept/", "Concept page describes recording, evaluating, mediating, and temporary storage of components/materials."),
            ("HAT_AKTEURROLLE", "ar_materialbroker", "belegt", "https://baumab-kassel.de/kaufen/", "Platform mediates components from offer to reuse."),
            ("HAT_AKTEURROLLE", "ar_materiallieferung_markt", "belegt", "https://baumab-kassel.de/bauteilboerse/", "Concrete priced offers are visible in the online catalogue."),
            ("HAT_AKTEURROLLE", "ar_software_digitalisierung", "belegt", "https://baumab-kassel.de/bauteilboerse/", "Digital catalogue exposes filters, listings, cart and online offer workflow."),
            ("HAT_AKTEURROLLE", "ar_rueckbau_bauteilernte_logistik", "abgeleitet", "https://baumab-kassel.de/kaufen/", "Buy page coordinates reservation and deconstruction windows before demolition/rueckbau."),
            ("HAT_AKTEURROLLE", "ar_reuse_zirkularitaetsberatung", "abgeleitet", "https://baumab-kassel.de/konzept/", "Concept page frames reuse as circular-economy climate strategy."),
            ("HAT_AKTEURROLLE", "ar_aufbereitung_refurbishment", "abgeleitet", "https://baumab-kassel.de/konzept/", "Physical/social retail place plus recording/evaluating/storing workflow supports preparation for reuse."),
            ("HAT_AKTEURROLLE", "ar_bildung_wissenstransfer", "belegt", "https://baumab-kassel.de/", "Homepage names open workshop and news/workshop activity."),
            ("HAT_METHODE", "meth_urban_mining_und_scouting", "abgeleitet", "https://baumab-kassel.de/verkaufen/", "Sell workflow captures components before demolition and publishes offers."),
            ("HAT_METHODE", "meth_bestands_und_reuse_assessment", "abgeleitet", "https://baumab-kassel.de/verkaufen/", "Sell page asks for component-specific description, geometry, colour, condition and function."),
            ("HAT_METHODE", "meth_dokumentation_und_monitoring", "abgeleitet", "https://baumab-kassel.de/bauteilboerse/", "Offer filters include dimensions, condition, availability, hazard suspicion and BIM."),
            ("HAT_METHODE", "meth_zirkulaere_beschaffung", "abgeleitet", "https://baumab-kassel.de/kaufen/", "Buy workflow enables reuse procurement with reservation/direct purchase."),
        ],
        "strict": [
            ("NUTZT_MATERIAL", "mat_beton", "belegt", "https://baumab-kassel.de/bauteilboerse/", "Betondachsteine are visible in the offer list."),
            ("NUTZT_MATERIAL", "mat_holz", "belegt", "https://baumab-kassel.de/bauteilboerse/", "Zimmertueren Holz / Holzfurnier are visible in the offer list."),
            ("NUTZT_MATERIAL", "mat_glas", "belegt", "https://baumab-kassel.de/bauteilboerse/", "Fenster 2-fach verglast is visible in the offer list."),
            ("HAT_BAUTEILTYP", "bt_dach", "belegt", "https://baumab-kassel.de/bauteilboerse/", "Betondachsteine are visible in the offer list."),
            ("HAT_BAUTEILTYP", "bt_fenster", "belegt", "https://baumab-kassel.de/bauteilboerse/", "Fenster category and window offers are visible."),
            ("HAT_BAUTEILTYP", "bt_tuer", "belegt", "https://baumab-kassel.de/bauteilboerse/", "Tueren category and Zimmertuer offers are visible."),
            ("HAT_BAUTEILTYP", "bt_technik", "belegt", "https://baumab-kassel.de/verkaufen/", "Elektronik/Gebaeudetechnik and sanitary/armature offers are named."),
        ],
    },
    {
        "id": "zirkulie_bauteilboerse_triesen",
        "name": "ZirkuLIE Bauteilbörse Triesen",
        "land": {"id": "land_liechtenstein", "name": "Liechtenstein", "create": True},
        "sources": [
            ("https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen", "ZirkuLIE centre and Bauteilboerse", "Page states the Triesen Bauteilboerse provides used components for Liechtenstein and Eastern Switzerland and links to the webshop."),
            ("https://shop.zirkulie.net/", "ZirkuLIE webshop", "Webshop exposes component categories, filters, prices, cart actions and Triesen contact/location."),
            ("https://shop.zirkulie.net/produkt-kategorie/gebaeudehuelle-2/fenster-gebaeudehuelle-2/", "ZirkuLIE window offers", "Window category lists material filters, product cards, prices, and cart actions."),
            ("https://shop.zirkulie.net/produkt-kategorie/innenausbau-2/tuere-innenausbau-2/", "ZirkuLIE door offers", "Door category lists products, material filters, prices, and cart actions."),
            ("https://shop.zirkulie.net/produkt-kategorie/konstruktion-gebaeude-2/daemmung-konstruktion-gebaeude-2/", "ZirkuLIE insulation offers", "Insulation category lists Heraklith and stone-wool products with prices and cart actions."),
            ("https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen/bauteile-spenden", "ZirkuLIE donation workflow", "Donation page asks for photos/descriptions of used components and describes construction waste as reuse potential."),
            ("https://www.zirkulie.net/impressum", "ZirkuLIE imprint", "Imprint identifies Stiftung Lebenswertes Liechtenstein and Triesen centre contact."),
        ],
        "belegt_in": [
            "https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen",
            "https://shop.zirkulie.net/",
            "https://shop.zirkulie.net/produkt-kategorie/gebaeudehuelle-2/fenster-gebaeudehuelle-2/",
            "https://shop.zirkulie.net/produkt-kategorie/innenausbau-2/tuere-innenausbau-2/",
            "https://www.zirkulie.net/impressum",
        ],
        "edges": [
            ("HAT_AKTEURTYP", "at_materialhub_bauteilboerse", "belegt", "https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen", "First-party page identifies a Bauteilboerse for Liechtenstein and Eastern Switzerland."),
            ("HAT_MARKTMODELL", "mm_kauf_gebraucht", "belegt", "https://shop.zirkulie.net/", "Webshop shows priced reused components and cart actions."),
            ("HAT_GESCHAEFTSMODELL", "gm_shop_eigenstock", "belegt", "https://shop.zirkulie.net/", "Webshop and physical Triesen centre show depot/shop-style stock."),
            ("HAT_AKTEURROLLE", "ar_materialbroker", "belegt", "https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen", "Bauteilboerse provides access to used components."),
            ("HAT_AKTEURROLLE", "ar_materiallieferung_markt", "belegt", "https://shop.zirkulie.net/", "Webshop provides priced component offers."),
            ("HAT_AKTEURROLLE", "ar_software_digitalisierung", "belegt", "https://shop.zirkulie.net/", "Digital webshop provides categories, filters and cart actions."),
            ("HAT_AKTEURROLLE", "ar_reuse_zirkularitaetsberatung", "abgeleitet", "https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen", "Centre supports circular building and reuse."),
            ("HAT_AKTEURROLLE", "ar_bildung_wissenstransfer", "belegt", "https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen", "Centre is an event/contact point for circular building."),
            ("HAT_METHODE", "meth_zirkulaere_beschaffung", "belegt", "https://shop.zirkulie.net/", "Webshop enables procurement of reused components."),
            ("HAT_METHODE", "meth_urban_mining_und_scouting", "abgeleitet", "https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen/bauteile-spenden", "Donation workflow captures used components for reuse."),
        ],
        "strict": [
            ("NUTZT_MATERIAL", "mat_aluminium", "belegt", "https://shop.zirkulie.net/produkt-kategorie/gebaeudehuelle-2/fenster-gebaeudehuelle-2/", "Window category filter names Aluminium."),
            ("NUTZT_MATERIAL", "mat_glas", "belegt", "https://shop.zirkulie.net/produkt-kategorie/gebaeudehuelle-2/fenster-gebaeudehuelle-2/", "Window category filter names Glas and product cards list windows/glass."),
            ("NUTZT_MATERIAL", "mat_holz", "belegt", "https://shop.zirkulie.net/produkt-kategorie/gebaeudehuelle-2/fenster-gebaeudehuelle-2/", "Window/door categories name Holz."),
            ("NUTZT_MATERIAL", "mat_kunststoff", "belegt", "https://shop.zirkulie.net/produkt-kategorie/gebaeudehuelle-2/fenster-gebaeudehuelle-2/", "Window category filter names Kunststoff."),
            ("NUTZT_MATERIAL", "mat_daemmstoff", "belegt", "https://shop.zirkulie.net/produkt-kategorie/konstruktion-gebaeude-2/daemmung-konstruktion-gebaeude-2/", "Insulation category lists Daemmung/Steinwolle."),
            ("HAT_BAUTEILTYP", "bt_fenster", "belegt", "https://shop.zirkulie.net/produkt-kategorie/gebaeudehuelle-2/fenster-gebaeudehuelle-2/", "Window category lists concrete Fenster offers."),
            ("HAT_BAUTEILTYP", "bt_tuer", "belegt", "https://shop.zirkulie.net/produkt-kategorie/innenausbau-2/tuere-innenausbau-2/", "Door category lists concrete Tuer offers."),
            ("HAT_BAUTEILTYP", "bt_daemmung", "belegt", "https://shop.zirkulie.net/produkt-kategorie/konstruktion-gebaeude-2/daemmung-konstruktion-gebaeude-2/", "Daemmung category lists Heraklithplatten and Steinwolle."),
            ("HAT_BAUTEILTYP", "bt_dach", "belegt", "https://shop.zirkulie.net/", "Shop category tree includes Dach / Dachhaut, Dachziegel."),
            ("HAT_BAUTEILTYP", "bt_fassade", "belegt", "https://shop.zirkulie.net/", "Shop category tree includes Fassadenelemente."),
            ("HAT_BAUTEILTYP", "bt_technik", "belegt", "https://shop.zirkulie.net/", "Shop category tree includes Gebaeudetechnik and sanitary/technical categories."),
            ("HAT_BAUTEILTYP", "bt_boden", "belegt", "https://shop.zirkulie.net/", "Shop category tree includes Bodenbelag."),
            ("HAT_BAUTEILTYP", "bt_treppe", "belegt", "https://shop.zirkulie.net/", "Shop category tree includes Treppen."),
        ],
    },
]


def read_password() -> str:
    env_password = (os.environ.get("NEO4J_PASSWORD") or "").strip()
    if env_password:
        return env_password
    for line in PASSWORD_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    raise RuntimeError("No password found in NEO4J_PASSWORD or .neo4j_password")


def rel_id(aid: str, rel_type: str, target_id: str) -> str:
    return f"r_{aid}__{rel_type}__{target_id}"


def main() -> int:
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    driver = GraphDatabase.driver(URI, auth=(USER, read_password()))
    with driver:
        driver.verify_connectivity()
        with driver.session(database=DATABASE) as session:
            print(f"Connecting: {URI} db={DATABASE} user={USER}")

            for actor in ACTORS:
                aid = actor["id"]
                print(f"Importing {aid}")
                land = actor["land"]
                if land.get("create"):
                    session.run(
                        "MERGE (l:Land {id:$id}) ON CREATE SET l.name=$name SET l.name=coalesce(l.name,$name)",
                        id=land["id"],
                        name=land["name"],
                    ).consume()

                session.run(
                    """
                    MERGE (a:Akteur {id:$id})
                    ON CREATE SET a.name=$name
                    SET a.name=$name,
                        a.source_scope='actor_registry_context'
                    """,
                    id=aid,
                    name=actor["name"],
                ).consume()

                qid_by_url = {}
                for url, title, _basis in actor["sources"]:
                    existing = session.run(
                        "MATCH (q:Quelle {url:$url}) RETURN q.id AS id LIMIT 1",
                        url=url,
                    ).single()
                    if existing:
                        qid = existing["id"]
                        session.run(
                            "MATCH (q:Quelle {id:$qid}) SET q.title=coalesce(q.title,$title), q.quelltyp=coalesce(q.quelltyp,'external_link')",
                            qid=qid,
                            title=title,
                        ).consume()
                    else:
                        qid = md5_id(url)
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
                            url=url,
                            title=title,
                        ).consume()
                    qid_by_url[url] = qid

                for url in actor["belegt_in"]:
                    qid = qid_by_url[url]
                    basis = next(b for u, _t, b in actor["sources"] if u == url)
                    session.run(
                        """
                        MATCH (a:Akteur {id:$aid})
                        MATCH (q:Quelle {id:$qid})
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
                        basis=basis,
                        url=url,
                        run=RUN,
                        source_file=SOURCE_FILE,
                    ).consume()

                session.run(
                    """
                    MATCH (a:Akteur {id:$aid})
                    MATCH (l:Land {id:$land_id})
                    MERGE (a)-[r:LIEGT_IN_LAND {id:$rid}]->(l)
                    ON CREATE SET r.created_at_utc=$created_at
                    SET r.evidence_confidence='belegt',
                        r.evidence_basis=$basis,
                        r.evidence_url=$url,
                        r.review_run=$run,
                        r.import_source_file=$source_file
                    """,
                    aid=aid,
                    land_id=land["id"],
                    rid=rel_id(aid, "LIEGT_IN_LAND", land["id"]),
                    created_at=created_at,
                    basis=f"First-party imprint/contact identifies country as {land['name']}.",
                    url=actor["belegt_in"][-1],
                    run=RUN,
                    source_file=SOURCE_FILE,
                ).consume()

                for rel_type, target_id, confidence, url, basis in actor["edges"] + actor["strict"]:
                    exists = session.run("MATCH (n {id:$id}) RETURN labels(n) AS labels LIMIT 1", id=target_id).single()
                    if not exists:
                        raise RuntimeError(f"Missing target {target_id} for {aid} {rel_type}")
                    query = f"""
                    MATCH (a:Akteur {{id:$aid}})
                    MATCH (n {{id:$target_id}})
                    MERGE (a)-[r:`{rel_type}` {{id:$rid}}]->(n)
                    ON CREATE SET r.created_at_utc=$created_at
                    SET r.evidence_confidence=$confidence,
                        r.evidence_basis=$basis,
                        r.evidence_url=$url,
                        r.review_run=$run,
                        r.import_source_file=$source_file
                    """
                    session.run(
                        query,
                        aid=aid,
                        target_id=target_id,
                        rid=rel_id(aid, rel_type, target_id),
                        created_at=created_at,
                        confidence=confidence,
                        basis=basis,
                        url=url,
                        run=RUN,
                        source_file=SOURCE_FILE,
                    ).consume()

            rows = session.run(
                """
                UNWIND $ids AS aid
                MATCH (a:Akteur {id:aid})
                OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t:Akteurtyp)
                WITH a, count(t) AS n_typ
                OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(l:Land)
                WITH a, n_typ, count(l) AS n_land
                OPTIONAL MATCH (a)-[:HAT_MARKTMODELL]->(m:Marktmodell)
                WITH a, n_typ, n_land, count(m) AS n_mm
                OPTIONAL MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g:Geschaeftsmodell)
                WITH a, n_typ, n_land, n_mm, count(g) AS n_gm
                OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(r:Akteurrolle)
                WITH a, n_typ, n_land, n_mm, n_gm, count(r) AS n_roles
                OPTIONAL MATCH (a)-[:BELEGT_IN]->(q:Quelle)
                WITH a, n_typ, n_land, n_mm, n_gm, n_roles, count(q) AS n_evidence
                OPTIONAL MATCH (a)-[:NUTZT_MATERIAL]->(mat:Material)
                WITH a, n_typ, n_land, n_mm, n_gm, n_roles, n_evidence, count(mat) AS n_mat
                OPTIONAL MATCH (a)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
                RETURN a.id AS id, n_typ, n_land, n_mm, n_gm, n_roles, n_evidence, n_mat, count(bt) AS n_bt,
                       CASE WHEN n_typ >= 1 AND n_land = 1 AND n_mm = 1 AND n_gm >= 1 AND n_roles >= 3 AND n_evidence >= 2
                            THEN 'OK' ELSE 'MISSING_REQUIRED' END AS schema_check
                ORDER BY id
                """,
                ids=[a["id"] for a in ACTORS],
            )
            for row in rows:
                print(dict(row))

            touched = session.run("MATCH ()-[r {review_run:$run}]->() RETURN count(r) AS n", run=RUN).single()["n"]
            missing_ids = session.run(
                """
                MATCH (a:Akteur)-[r]->()
                WHERE a.id IN $ids AND r.id IS NULL
                RETURN count(r) AS n
                """,
                ids=[a["id"] for a in ACTORS],
            ).single()["n"]
            print(f"Relationships touched with review_run={RUN}: {touched}")
            print(f"New anchors outgoing relationships missing r.id: {missing_ids}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
