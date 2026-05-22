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

RUN = "bauteile_ibs_graph_addition_2026_06_04"
SOURCE_FILE = "_neo4j/intake/runs/2026-06-04_bauteile_ibs_graph_addition"
ANCHOR_ID = "bauteilkatalog_immobilien_basel_stadt"
ANCHOR_NAME = "Bauteilkatalog Immobilien Basel-Stadt"


def md5_id(url: str) -> str:
    return "q_url_" + hashlib.md5(url.encode("utf-8")).hexdigest()


SOURCES = [
    {
        "url": "https://bauteile-ibs.ch/",
        "title": "Immobilien Basel-Stadt Bauteilkatalog zur Wiederverwendung",
        "basis": "Homepage/title and navigation expose catalogue, categories, component listings, login, and cart.",
    },
    {
        "url": "https://bauteile-ibs.ch/info",
        "title": "Bauteile IBS project information",
        "basis": "Project page states circular-economy purpose and restricted availability to cantonal projects / competition participants.",
    },
    {
        "url": "https://bauteile-ibs.ch/components",
        "title": "Bauteile IBS component catalogue",
        "basis": "Component catalogue lists categories and concrete reusable components.",
    },
    {
        "url": "https://bauteile-ibs.ch/componentsmine",
        "title": "Bauteile IBS Bauteilminen",
        "basis": "Bauteilminen page lists source mines including Messehalle 3, Busdepot Rankhof, and Areal Klybeck.",
    },
    {
        "url": "https://bauteile-ibs.ch/contact",
        "title": "Bauteile IBS contact and imprint",
        "basis": "Contact page names Immobilien Basel-Stadt, Zirkular GmbH, and digvis GmbH roles.",
    },
    {
        "url": "https://zirkular.net/de/projekt/bauteilkatalog-immobilien-basel-stadt",
        "title": "Zirkular: Bauteilkatalog Immobilien Basel-Stadt",
        "basis": "Zirkular project page states Zirkular catalogued Re-Use components for Immobilien Basel-Stadt from current Basel-Stadt deconstruction objects.",
    },
    {
        "url": "https://bauteile-ibs.ch/components/163-msh0012-passerelle-fenster",
        "title": "MSH001.2 Passerelle Fenster",
        "basis": "Detail page names Passerelle Fenster, glass description, dimensions, quantity, CO2 values, Bauteilpass download, and cart action.",
    },
    {
        "url": "https://bauteile-ibs.ch/components/114-msh002-stahltragwerk",
        "title": "MSH002 Stahltragwerk",
        "basis": "Detail page names Stahltragwerk, Fachwerktraeger, HEA/HEB profiles, Stuetzen, dimensions, quantity, CO2 values, and Bauteilpass.",
    },
    {
        "url": "https://bauteile-ibs.ch/components/193-msh005-holzbalkendecke-halle",
        "title": "MSH005 Holzbalkendecke Halle",
        "basis": "Detail page names Holzbalkendecke and component parts Holzbalken / Holzbretter.",
    },
    {
        "url": "https://bauteile-ibs.ch/components/144-msh030-waermedaemmung",
        "title": "MSH030 Waermedaemmung",
        "basis": "Detail page names Waermedaemmung, EPS, dimensions, quantity, CO2 values, and Bauteilpass.",
    },
    {
        "url": "https://bauteile-ibs.ch/components/203-ran-gr10-sandwichpaneele",
        "title": "RAN-GR10 Sandwichpaneele",
        "basis": "Detail page names Sandwichpaneele, component lengths, quantity, and source Bauteilmine.",
    },
    {
        "url": "https://bauteile-ibs.ch/components/180-kly-gr08-alu-fassadenplatten",
        "title": "KLY-GR08 Alu-Fassadenplatten",
        "basis": "Detail page names Alu-Fassadenplatten, aluminium modelling basis, dimensions, quantity, CO2 values, and Bauteilgruppe download.",
    },
]

for src in SOURCES:
    src["qid"] = md5_id(src["url"])

BELEGT_IN_URLS = [
    "https://bauteile-ibs.ch/",
    "https://bauteile-ibs.ch/info",
    "https://bauteile-ibs.ch/components",
    "https://bauteile-ibs.ch/componentsmine",
    "https://bauteile-ibs.ch/contact",
]

EDGES = [
    ("HAT_AKTEURTYP", "at_materialhub_bauteilboerse", "abgeleitet", "https://bauteile-ibs.ch/components", "Catalogue exposes reusable building components as a materialhub/bauteilboerse-style actor."),
    ("LIEGT_IN_LAND", "land_schweiz", "belegt", "https://bauteile-ibs.ch/contact", "Contact/imprint addresses Basel, Switzerland."),
    ("HAT_MARKTMODELL", "mm_kauf_gebraucht", "abgeleitet", "https://bauteile-ibs.ch/components", "Catalogue exposes used/reuse components with cart action; not modelled as multi-vendor marketplace."),
    ("HAT_GESCHAEFTSMODELL", "gm_dienstleistung_urban_mining", "abgeleitet", "https://zirkular.net/de/projekt/bauteilkatalog-immobilien-basel-stadt", "Zirkular catalogued Re-Use components from current deconstruction objects for IBS."),
    ("HAT_AKTEURROLLE", "ar_materialbroker", "abgeleitet", "https://bauteile-ibs.ch/components", "Catalogue mediates access to reusable components."),
    ("HAT_AKTEURROLLE", "ar_materiallieferung_markt", "abgeleitet", "https://bauteile-ibs.ch/components", "Component catalogue and cart action support material supply/procurement workflow."),
    ("HAT_AKTEURROLLE", "ar_software_digitalisierung", "abgeleitet", "https://bauteile-ibs.ch/contact", "Digital catalogue implemented by digvis and designed/conceived by Zirkular."),
    ("HAT_AKTEURROLLE", "ar_rueckbau_bauteilernte_logistik", "abgeleitet", "https://zirkular.net/de/projekt/bauteilkatalog-immobilien-basel-stadt", "Components come from current deconstruction objects; Bauteilboerse Basel named for dismantling/logistics."),
    ("HAT_AKTEURROLLE", "ar_reuse_zirkularitaetsberatung", "abgeleitet", "https://bauteile-ibs.ch/info", "Catalogue purpose is circular economy and reuse of building materials."),
    ("HAT_AKTEURROLLE", "ar_forschung_dokumentation", "abgeleitet", "https://bauteile-ibs.ch/components/114-msh002-stahltragwerk", "Component detail pages provide documented dimensions, quantities, CO2 values, and downloads."),
    ("HAT_AKTEURROLLE", "ar_aufbereitung_refurbishment", "abgeleitet", "https://zirkular.net/de/projekt/bauteilkatalog-immobilien-basel-stadt", "Schema fingerprint for urban-mining/service catalogue; review if a stricter non-refurbishment reading is desired."),
    ("HAT_METHODE", "meth_urban_mining_und_scouting", "abgeleitet", "https://bauteile-ibs.ch/componentsmine", "Catalogue uses Bauteilminen/source objects and reusable component scouting."),
    ("HAT_METHODE", "meth_bestands_und_reuse_assessment", "abgeleitet", "https://bauteile-ibs.ch/components/114-msh002-stahltragwerk", "Detail pages assess existing components with descriptions, dimensions, quantity, source, and emissions."),
    ("HAT_METHODE", "meth_dokumentation_und_monitoring", "abgeleitet", "https://bauteile-ibs.ch/components/114-msh002-stahltragwerk", "Detail pages provide Bauteilpass/download evidence and structured component documentation."),
    ("HAT_METHODE", "meth_zirkulaere_beschaffung", "abgeleitet", "https://bauteile-ibs.ch/info", "Components are made available to competition teams / cantonal projects for reuse procurement."),
    ("NUTZT_SOFTWARE", "tool_bauteilkatalog", "belegt", "https://bauteile-ibs.ch/contact", "The site is a programmed digital Bauteilkatalog / component catalogue."),
    ("BETRIEBEN_VON", "immobilien_basel_stadt", "belegt", "https://bauteile-ibs.ch/contact", "Contact page names Immobilien Basel-Stadt as catalogue contact; site title is Immobilien Basel-Stadt catalogue."),
    ("VERBUNDEN_MIT_AKTEUR", "zirkular", "belegt", "https://bauteile-ibs.ch/contact", "Contact/imprint and Zirkular project page identify Zirkular role in catalogue conception/cataloguing."),
    ("VERBUNDEN_MIT_AKTEUR", "digvis_gmbh", "belegt", "https://bauteile-ibs.ch/contact", "Contact page names digvis GmbH as programming provider."),
    ("VERBUNDEN_MIT_AKTEUR", "bauteilboerse_basel_overall", "belegt", "https://zirkular.net/de/projekt/bauteilkatalog-immobilien-basel-stadt", "Zirkular page names Bauteilboerse Basel for demontage and logistics."),
    ("BETEILIGT_AN", "p_elementa_walkeweg", "belegt", "https://zirkular.net/de/projekt/bauteilkatalog-immobilien-basel-stadt", "Zirkular page links the catalogue to Walkeweg competition/project context."),
]

STRICT_EDGES = [
    ("NUTZT_MATERIAL", "mat_stahl", "belegt", "https://bauteile-ibs.ch/components/114-msh002-stahltragwerk", "Stahltragwerk and Stahltraeger/HEA/HEB profiles are named in the catalogue."),
    ("NUTZT_MATERIAL", "mat_holz", "belegt", "https://bauteile-ibs.ch/components/193-msh005-holzbalkendecke-halle", "Holzbalkendecke, Holzbalken, and Holzbretter are named in the catalogue."),
    ("NUTZT_MATERIAL", "mat_daemmstoff", "belegt", "https://bauteile-ibs.ch/components/144-msh030-waermedaemmung", "Waermedaemmung/EPS is named in the catalogue."),
    ("NUTZT_MATERIAL", "mat_aluminium", "belegt", "https://bauteile-ibs.ch/components/180-kly-gr08-alu-fassadenplatten", "Alu-Fassadenplatten and Aluminium modelling basis are named in the catalogue."),
    ("NUTZT_MATERIAL", "mat_glas", "belegt", "https://bauteile-ibs.ch/components/163-msh0012-passerelle-fenster", "Verglasung and IV Glaeser are named in the catalogue."),
    ("HAT_BAUTEILTYP", "bt_fenster", "belegt", "https://bauteile-ibs.ch/components/163-msh0012-passerelle-fenster", "Passerelle Fenster is a listed component."),
    ("HAT_BAUTEILTYP", "bt_traeger", "belegt", "https://bauteile-ibs.ch/components/114-msh002-stahltragwerk", "Fachwerktraeger and HEA/HEB Traeger are named in the catalogue."),
    ("HAT_BAUTEILTYP", "bt_decke", "belegt", "https://bauteile-ibs.ch/components/193-msh005-holzbalkendecke-halle", "Holzbalkendecke is a listed component."),
    ("HAT_BAUTEILTYP", "bt_daemmung", "belegt", "https://bauteile-ibs.ch/components/144-msh030-waermedaemmung", "Waermedaemmung is a listed component."),
    ("HAT_BAUTEILTYP", "bt_fassade", "belegt", "https://bauteile-ibs.ch/components/180-kly-gr08-alu-fassadenplatten", "Alu-Fassadenplatten and facade panels are listed components."),
    ("HAT_BAUTEILTYP", "bt_treppe", "belegt", "https://bauteile-ibs.ch/components", "Aussentreppe is listed in the component catalogue."),
    ("HAT_BAUTEILTYP", "bt_gelaender", "belegt", "https://bauteile-ibs.ch/components", "Gelaender is listed in the component catalogue."),
    ("HAT_BAUTEILTYP", "bt_technik", "belegt", "https://bauteile-ibs.ch/components", "Kabeltrasse and Lueftungsrohre are listed in the component catalogue."),
    ("HAT_BAUTEILTYP", "bt_stuetze", "belegt", "https://bauteile-ibs.ch/components/114-msh002-stahltragwerk", "HEB 300 Stuetzen are named in the Stahltragwerk detail page."),
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


def rel_id(rel_type: str, target_id: str) -> str:
    return f"r_{ANCHOR_ID}__{rel_type}__{target_id}"


def main() -> int:
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    password = read_password()
    driver = GraphDatabase.driver(URI, auth=(USER, password))

    with driver:
        driver.verify_connectivity()
        with driver.session(database=DATABASE) as session:
            print(f"Connecting: {URI} db={DATABASE} user={USER}")
            print(f"Anchor: {ANCHOR_ID}")

            session.run(
                """
                MERGE (a:Akteur {id: $id})
                ON CREATE SET a.name = $name
                SET a.name = $name,
                    a.source_scope = 'actor_registry_context'
                """,
                id=ANCHOR_ID,
                name=ANCHOR_NAME,
            ).consume()

            qid_by_url: dict[str, str] = {}
            for src in SOURCES:
                existing = session.run(
                    "MATCH (q:Quelle {url: $url}) RETURN q.id AS id LIMIT 1",
                    url=src["url"],
                ).single()
                if existing:
                    qid = existing["id"]
                    session.run(
                        """
                        MATCH (q:Quelle {id: $qid})
                        SET q.title = coalesce(q.title, $title),
                            q.quelltyp = coalesce(q.quelltyp, 'external_link')
                        """,
                        qid=qid,
                        title=src["title"],
                    ).consume()
                else:
                    qid = src["qid"]
                    session.run(
                        """
                        MERGE (q:Quelle:ExternalLink {id: $qid})
                        ON CREATE SET q.url = $url,
                                      q.title = $title,
                                      q.quelltyp = 'external_link'
                        SET q.url = coalesce(q.url, $url),
                            q.title = coalesce(q.title, $title),
                            q.quelltyp = coalesce(q.quelltyp, 'external_link')
                        """,
                        qid=qid,
                        url=src["url"],
                        title=src["title"],
                    ).consume()
                qid_by_url[src["url"]] = qid

            for url in BELEGT_IN_URLS:
                qid = qid_by_url[url]
                session.run(
                    """
                    MATCH (a:Akteur {id: $aid})
                    MATCH (q:Quelle {id: $qid})
                    MERGE (a)-[r:BELEGT_IN {id: $rid}]->(q)
                    ON CREATE SET r.created_at_utc = $created_at
                    SET r.evidence_confidence = 'belegt',
                        r.evidence_basis = $basis,
                        r.evidence_url = $url,
                        r.review_run = $run,
                        r.import_source_file = $source_file
                    """,
                    aid=ANCHOR_ID,
                    qid=qid,
                    rid=rel_id("BELEGT_IN", qid),
                    created_at=created_at,
                    basis=next(s["basis"] for s in SOURCES if s["url"] == url),
                    url=url,
                    run=RUN,
                    source_file=SOURCE_FILE,
                ).consume()

            all_edges = EDGES + STRICT_EDGES
            skipped: list[tuple[str, str, str]] = []
            for rel_type, target_id, confidence, url, basis in all_edges:
                exists = session.run(
                    "MATCH (t {id: $target_id}) RETURN labels(t) AS labels LIMIT 1",
                    target_id=target_id,
                ).single()
                if not exists:
                    skipped.append((rel_type, target_id, "target_missing"))
                    continue
                query = f"""
                    MATCH (a:Akteur {{id: $aid}})
                    MATCH (t {{id: $target_id}})
                    MERGE (a)-[r:`{rel_type}` {{id: $rid}}]->(t)
                    ON CREATE SET r.created_at_utc = $created_at
                    SET r.evidence_confidence = $confidence,
                        r.evidence_basis = $basis,
                        r.evidence_url = $url,
                        r.review_run = $run,
                        r.import_source_file = $source_file
                """
                session.run(
                    query,
                    aid=ANCHOR_ID,
                    target_id=target_id,
                    rid=rel_id(rel_type, target_id),
                    created_at=created_at,
                    confidence=confidence,
                    basis=basis,
                    url=url,
                    run=RUN,
                    source_file=SOURCE_FILE,
                ).consume()

            if skipped:
                print("Skipped edges:")
                for item in skipped:
                    print(f"  {item[0]} -> {item[1]}: {item[2]}")

            result = session.run(
                """
                MATCH (a:Akteur {id: $aid})
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
                RETURN a.id AS id,
                       n_typ, n_land, n_mm, n_gm, n_roles, n_evidence,
                       n_mat, count(bt) AS n_bt,
                       CASE WHEN n_typ >= 1 AND n_land = 1 AND n_mm = 1
                                 AND n_gm >= 1 AND n_roles >= 3 AND n_evidence >= 2
                            THEN 'OK' ELSE 'MISSING_REQUIRED' END AS schema_check
                """,
                aid=ANCHOR_ID,
            ).single()

            touched = session.run(
                "MATCH ()-[r {review_run: $run}]->() RETURN count(r) AS n",
                run=RUN,
            ).single()["n"]

            missing_ids = session.run(
                """
                MATCH (a:Akteur {id: $aid})-[r]->()
                WHERE r.id IS NULL
                RETURN count(r) AS n
                """,
                aid=ANCHOR_ID,
            ).single()["n"]

            print(f"Relationships touched with review_run={RUN}: {touched}")
            print(f"Anchor outgoing relationships missing r.id: {missing_ids}")
            print(dict(result))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
