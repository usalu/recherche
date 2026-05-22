"""Run reuse network catalog queries against live mit-bestand (read-only)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

OUT = Path(__file__).resolve().parent / "query_results.json"

QUERIES: dict[str, dict] = {
    "baseline": {
        "title": "Graph baseline",
        "cypher": """
            MATCH (n)
            WITH count(n) AS nodes
            MATCH ()-[r]->()
            RETURN nodes, count(r) AS rels
        """,
    },
    "n1_actor_constellation_stats": {
        "title": "Actor reuse constellation stats",
        "cypher": """
            MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]->()
            WHERE r.review_run IS NOT NULL
            RETURN count(r) AS directed_tagged,
                   count(DISTINCT r.review_run) AS review_runs
        """,
    },
    "n1_actor_by_country_on_network": {
        "title": "Actors in reuse network by country",
        "cypher": """
            MATCH (a:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]-()
            WHERE r.review_run IS NOT NULL
            OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(l:Land)
            WITH DISTINCT a, l
            RETURN coalesce(l.name, '(no country edge)') AS country,
                   count(DISTINCT a) AS actors
            ORDER BY actors DESC, country
        """,
    },
    "n2_all_actors_by_country": {
        "title": "All actors by country",
        "cypher": """
            MATCH (a:Akteur)
            OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(l:Land)
            RETURN coalesce(l.name, '(no country edge)') AS country,
                   count(DISTINCT a) AS actors
            ORDER BY actors DESC, country
        """,
    },
    "n3_projects_by_country": {
        "title": "Projects by country",
        "cypher": """
            MATCH (p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
            RETURN l.name AS country, count(DISTINCT p) AS projects
            ORDER BY projects DESC, country
        """,
    },
    "n3_cross_border_actors": {
        "title": "Actors active in multiple countries via projects",
        "cypher": """
            MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
            WITH a, collect(DISTINCT l.name) AS countries, count(DISTINCT p) AS projects
            WHERE size(countries) > 1
            RETURN a.id AS actor, a.name AS name, countries, projects
            ORDER BY size(countries) DESC, projects DESC, actor
            LIMIT 20
        """,
    },
    "n3_top_actors_per_country": {
        "title": "Top actors by project count per country",
        "cypher": """
            MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
            WITH l.name AS country, a.id AS actor, a.name AS actor_name, count(DISTINCT p) AS projects
            ORDER BY country, projects DESC, actor
            WITH country, collect({actor: actor, name: actor_name, projects: projects})[0..5] AS top5
            RETURN country, top5
            ORDER BY country
        """,
    },
    "n4_role_frequency": {
        "title": "Actor role frequency",
        "cypher": """
            MATCH (:Akteur)-[:HAT_AKTEURROLLE]->(ar:Akteurrolle)
            RETURN ar.id AS role_id, ar.name AS role_name, count(*) AS assignments
            ORDER BY assignments DESC, role_id
            LIMIT 25
        """,
    },
    "n4_multi_role_actors": {
        "title": "Most multi-role actors",
        "cypher": """
            MATCH (a:Akteur)-[:HAT_AKTEURROLLE]->(ar:Akteurrolle)
            WITH a, collect(DISTINCT ar.name) AS roles
            WHERE size(roles) >= 3
            RETURN a.id AS actor, a.name AS name, roles, size(roles) AS role_count
            ORDER BY role_count DESC, actor
            LIMIT 20
        """,
    },
    "n5_type_role_matrix": {
        "title": "Actor type x role co-occurrence",
        "cypher": """
            MATCH (a:Akteur)-[:HAT_AKTEURTYP]->(at:Akteurtyp),
                  (a)-[:HAT_AKTEURROLLE]->(ar:Akteurrolle)
            RETURN at.name AS actor_type, ar.name AS role, count(DISTINCT a) AS actors
            ORDER BY actors DESC, actor_type, role
            LIMIT 30
        """,
    },
    "n6_norms_by_country": {
        "title": "Typed law nodes per country",
        "cypher": """
            MATCH (rw)-[:GILT_IN_LAND]->(l:Land)
            WHERE any(lbl IN labels(rw) WHERE lbl ENDS WITH 'recht')
            RETURN l.name AS country, count(DISTINCT rw) AS law_nodes
            ORDER BY law_nodes DESC, country
        """,
    },
    "n6_multi_country_norms": {
        "title": "Standards spanning multiple countries",
        "cypher": """
            MATCH (rw)-[:GILT_IN_LAND]->(l:Land)
            WHERE any(lbl IN labels(rw) WHERE lbl ENDS WITH 'recht')
            WITH rw, collect(DISTINCT l.name) AS countries
            WHERE size(countries) > 1
            RETURN rw.id AS law_id, rw.name AS law_name,
                   [lbl IN labels(rw) WHERE lbl ENDS WITH 'recht'][0] AS primary_label,
                   countries, size(countries) AS country_count
            ORDER BY country_count DESC, law_id
            LIMIT 20
        """,
    },
    "n6_norms_by_domain": {
        "title": "Law nodes by domain label",
        "cypher": """
            MATCH (rw)
            WHERE any(lbl IN labels(rw) WHERE lbl ENDS WITH 'recht')
            UNWIND [lbl IN labels(rw) WHERE lbl ENDS WITH 'recht'] AS domain
            RETURN domain, count(DISTINCT rw) AS law_nodes
            ORDER BY law_nodes DESC, domain
        """,
    },
    "n7_regulation_chain_sample": {
        "title": "Regulation chain: Bauteilgruppe to law to country (Holbein steel, summarized)",
        "cypher": """
            MATCH (bg:Bauteilgruppe {id:'bg_stahl_mehrere_holbein_structural'})
                  -[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
                  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
                  -[:GESTUETZT_AUF_REGELWERK]->(rw)
                  -[:GILT_IN_LAND]->(l:Land)
            RETURN rf.name AS question, nf.name AS proof_required,
                   count(DISTINCT rw) AS standards, collect(DISTINCT l.name) AS countries
            ORDER BY question, proof_required
        """,
    },
    "n7_regulation_chain_detail": {
        "title": "Regulation chain detail sample (Holbein steel, first 15 rows)",
        "cypher": """
            MATCH (bg:Bauteilgruppe {id:'bg_stahl_mehrere_holbein_structural'})
                  -[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
                  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
                  -[:GESTUETZT_AUF_REGELWERK]->(rw)
                  -[:GILT_IN_LAND]->(l:Land)
            RETURN bg.name AS component, rf.name AS question, nf.name AS proof_required,
                   rw.name AS standard, [lbl IN labels(rw) WHERE lbl ENDS WITH 'recht'][0] AS domain,
                   l.name AS country
            ORDER BY question, standard, country
            LIMIT 15
        """,
    },
    "n7_regulation_chain_counts": {
        "title": "Regulation chain coverage",
        "cypher": """
            MATCH (bg:Bauteilgruppe)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
            WITH count(DISTINCT bg) AS bgs_with_questions
            MATCH (bg:Bauteilgruppe)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
                  -[:ERFORDERT_NACHWEIS]->(:Nachweisforderung)-[:GESTUETZT_AUF_REGELWERK]->(rw)
            RETURN bgs_with_questions,
                   count(DISTINCT bg) AS bgs_with_law_links,
                   count(DISTINCT rw) AS standards_reached
        """,
    },
    "n8_bauteilgruppen_by_project": {
        "title": "Bauteilgruppen per project (top projects)",
        "cypher": """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
            WITH p, count(DISTINCT bg) AS bg_count, collect(bg.name)[0..3] AS sample_bgs
            RETURN p.id AS project_id, p.name AS project, bg_count, sample_bgs
            ORDER BY bg_count DESC, project_id
            LIMIT 20
        """,
    },
    "n8_bauteilgruppen_by_bauteiltyp": {
        "title": "Bauteilgruppen by Bauteiltyp",
        "cypher": """
            MATCH (bg:Bauteilgruppe)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
            RETURN bt.name AS bauteiltyp, count(DISTINCT bg) AS bauteilgruppen
            ORDER BY bauteilgruppen DESC, bauteiltyp
            LIMIT 20
        """,
    },
    "n9_donor_receiver_chains": {
        "title": "Donor to receiver flows via Bauteilgruppe and Bauwerk",
        "cypher": """
            MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER]->(donor:Bauwerk),
                  (bg)-[:IN_EMPFANGSOBJEKT]->(recv:Bauwerk)
            OPTIONAL MATCH (bg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)
            RETURN bg.name AS component, donor.name AS donor_building, recv.name AS receiver_building,
                   p.name AS project
            ORDER BY project, component
            LIMIT 25
        """,
    },
    "n9_cross_country_donor_flows": {
        "title": "Cross-country donor flows via Bauteilgruppe",
        "cypher": """
            MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER]->(donor:Bauwerk),
                  (bg)-[:IN_EMPFANGSOBJEKT]->(recv:Bauwerk)
            MATCH (donor)-[:LIEGT_IN_LAND]->(dl:Land)
            MATCH (recv)-[:LIEGT_IN_LAND]->(rl:Land)
            WHERE dl <> rl
            OPTIONAL MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)
            RETURN bg.name AS component, donor.name AS donor_building, dl.name AS from_country,
                   recv.name AS receiver_building, rl.name AS to_country, p.name AS project
            ORDER BY from_country, to_country, project
            LIMIT 20
        """,
    },
    "n10_top_materials": {
        "title": "Most reused materials across projects",
        "cypher": """
            MATCH (p:Projekt)-[:NUTZT_MATERIAL]->(m:Material)
            RETURN m.name AS material, count(DISTINCT p) AS projects
            ORDER BY projects DESC, material
            LIMIT 20
        """,
    },
    "n10_top_bauteiltypen_projects": {
        "title": "Most common Bauteiltypen across projects",
        "cypher": """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
            RETURN bt.name AS bauteiltyp, count(DISTINCT p) AS projects, count(DISTINCT bg) AS bauteilgruppen
            ORDER BY projects DESC, bauteiltyp
            LIMIT 20
        """,
    },
    "n11_huerden_by_project": {
        "title": "Most common reuse barriers (Huerden)",
        "cypher": """
            MATCH (p:Projekt)-[:HAT_HUERDE]->(h:Huerde)
            RETURN h.name AS barrier, count(DISTINCT p) AS projects
            ORDER BY projects DESC, barrier
            LIMIT 20
        """,
    },
    "n11_huerden_by_country": {
        "title": "Barriers by country",
        "cypher": """
            MATCH (p:Projekt)-[:HAT_HUERDE]->(h:Huerde)
            MATCH (p)-[:LIEGT_IN_LAND]->(l:Land)
            WITH l.name AS country, h.name AS barrier, count(DISTINCT p) AS projects
            ORDER BY country, projects DESC
            WITH country, collect({barrier: barrier, projects: projects})[0..5] AS top_barriers
            RETURN country, top_barriers
            ORDER BY country
        """,
    },
    "n12_hub_degree": {
        "title": "Top reuse actor hubs by partner count",
        "cypher": """
            MATCH (n:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]-(m:Akteur)
            WHERE r.review_run IS NOT NULL
            RETURN n.id AS actor, n.name AS name, count(DISTINCT m) AS partners
            ORDER BY partners DESC, actor
            LIMIT 12
        """,
    },
    "n12_bridge_nodes": {
        "title": "Bridge nodes spanning multiple review runs",
        "cypher": """
            MATCH (n:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]-()
            WHERE r.review_run IS NOT NULL
            WITH n, collect(DISTINCT r.review_run) AS bubbles, count(DISTINCT r) AS deg
            WHERE size(bubbles) > 1
            RETURN n.id AS actor, n.name AS name, size(bubbles) AS bubbles_spanned,
                   bubbles, deg AS connections
            ORDER BY bubbles_spanned DESC, connections DESC, actor
            LIMIT 15
        """,
    },
    "n12_connection_mechanisms": {
        "title": "Connection kinds grouped by mechanism",
        "cypher": """
            MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]->()
            WHERE r.review_run IS NOT NULL
            WITH r.connection_kind AS k, count(*) AS n
            RETURN
              CASE
                WHEN k CONTAINS 'director' OR k CONTAINS 'listing' OR k CONTAINS 'supplier'
                  THEN '1. Catalogue / directory'
                WHEN k CONTAINS 'research' OR k CONTAINS 'consortium' OR k CONTAINS 'programme' OR k CONTAINS 'lab'
                  THEN '2. Research / standards'
                WHEN k CONTAINS 'partnership' OR k CONTAINS 'commissioner' OR k CONTAINS 'operator' OR k CONTAINS 'family'
                  THEN '3. Formal / commercial'
                WHEN k CONTAINS 'mesh' OR k CONTAINS 'ecosystem' OR k CONTAINS 'network' OR k CONTAINS 'peer'
                  THEN '4. Ecosystem peer'
                ELSE '5. Other / lineage'
              END AS mechanism,
              sum(n) AS connections
            ORDER BY connections DESC
        """,
    },
    "n12_shortest_path_useagain_cstb": {
        "title": "Cross-border path useagain to CSTB (if connected)",
        "cypher": """
            MATCH (a:Akteur {id:'useagain_bauteilclick'}), (b:Akteur {id:'cstb'})
            OPTIONAL MATCH p = shortestPath((a)-[:VERBUNDEN_MIT_AKTEUR*..12]-(b))
            RETURN CASE WHEN p IS NULL THEN '(no path within 12 hops)' ELSE [n IN nodes(p) | n.id] END AS hops,
                   CASE WHEN p IS NULL THEN null ELSE length(p) END AS distance
        """,
    },
    "n12_useagain_neighbors": {
        "title": "useagain direct reuse-network neighbors",
        "cypher": """
            MATCH (a:Akteur {id:'useagain_bauteilclick'})-[r:VERBUNDEN_MIT_AKTEUR]-(m:Akteur)
            WHERE r.review_run IS NOT NULL
            RETURN m.id AS neighbor, r.connection_kind AS kind, r.review_run AS bubble
            ORDER BY bubble, neighbor
        """,
    },
    "n12_software_network": {
        "title": "Software used across projects",
        "cypher": """
            MATCH (p:Projekt)-[:NUTZT_SOFTWARE]->(sw)
            RETURN sw.name AS software, count(DISTINCT p) AS projects
            ORDER BY projects DESC, software
            LIMIT 15
        """,
    },
    "n12_geschaeftsmodelle": {
        "title": "Business models across actors (reuse operators)",
        "cypher": """
            MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(gm:Geschaeftsmodell)
            RETURN coalesce(gm.name, gm.id) AS model, count(DISTINCT a) AS actors
            ORDER BY actors DESC, model
            LIMIT 15
        """,
    },
    "swiss_bubble_review_runs": {
        "title": "Connections per review_run bubble",
        "cypher": """
            MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]->()
            WHERE r.review_run IS NOT NULL
            RETURN r.review_run AS bubble, count(r) AS connections
            ORDER BY connections DESC
        """,
    },
}


def serialize(value):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        return [serialize(v) for v in value]
    if isinstance(value, dict):
        return {str(k): serialize(v) for k, v in value.items()}
    return str(value)


def main() -> None:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    results: dict[str, object] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "queries": {},
    }
    with driver.session(database=database) as session:
        for key, spec in QUERIES.items():
            rows = [dict(r) for r in session.run(spec["cypher"])]
            results["queries"][key] = {
                "title": spec["title"],
                "cypher": spec["cypher"].strip(),
                "rows": serialize(rows),
                "row_count": len(rows),
            }
            print(f"{key}: {len(rows)} rows")
    driver.close()
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
