"""Graph-network Cypher queries for the reuse catalog (no row limits)."""

from __future__ import annotations

# Each entry: stable export id, catalog section, title, Cypher returning graph elements.
GRAPH_NETWORKS: list[dict[str, str]] = [
    {
        "id": "01_actor_constellation",
        "section": "1",
        "title": "Actor reuse constellation (all countries)",
        "cypher": """
MATCH (a:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
WHERE r.review_run IS NOT NULL
RETURN a, r, b;
""",
    },
    {
        "id": "02_swiss_bubble",
        "section": "2",
        "title": "Swiss reuse bubble (Cirkla star)",
        "cypher": """
MATCH (a:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
WHERE r.review_run = 'swiss_reuse_bubble_2026_06_05'
RETURN a, r, b;
""",
    },
    {
        "id": "03_actors_by_country",
        "section": "3",
        "title": "Actors by country (LIEGT_IN_LAND)",
        "cypher": """
MATCH (a:Akteur)-[r:LIEGT_IN_LAND]->(l:Land)
RETURN a, r, l;
""",
    },
    {
        "id": "04_projects_country_actors",
        "section": "4",
        "title": "Projects × country × actors",
        "cypher": """
MATCH (a:Akteur)-[r1:BETEILIGT_AN]->(p:Projekt)-[r2:LIEGT_IN_LAND]->(l:Land)
RETURN a, r1, p, r2, l;
""",
    },
    {
        "id": "05_switzerland_project_actors",
        "section": "5",
        "title": "Switzerland project × actor subgraph",
        "cypher": """
MATCH (l:Land {name: 'Schweiz'})<-[r2:LIEGT_IN_LAND]-(p:Projekt)<-[r1:BETEILIGT_AN]-(a:Akteur)
RETURN a, r1, p, r2, l;
""",
    },
    {
        "id": "06_actor_role_map",
        "section": "6",
        "title": "Multi-role actors (≥3 roles)",
        "cypher": """
MATCH (a:Akteur)
WHERE COUNT { (a)-[:HAT_AKTEURROLLE]->() } >= 3
MATCH (a)-[r:HAT_AKTEURROLLE]->(ar:Akteurrolle)
RETURN a, r, ar;
""",
    },
    {
        "id": "07_actor_type_role_materialhub",
        "section": "7",
        "title": "Materialhub actor type × role",
        "cypher": """
MATCH (a:Akteur)-[rt:HAT_AKTEURTYP]->(at:Akteurtyp),
      (a)-[rr:HAT_AKTEURROLLE]->(ar:Akteurrolle)
WHERE at.id = 'at_materialhub_bauteilboerse'
RETURN a, rt, at, rr, ar;
""",
    },
    {
        "id": "08_norms_by_country",
        "section": "8",
        "title": "Typed law nodes × country",
        "cypher": """
MATCH (rw)-[r:GILT_IN_LAND]->(l:Land)
WHERE any(lbl IN labels(rw) WHERE lbl ENDS WITH 'recht')
RETURN rw, r, l;
""",
    },
    {
        "id": "09_regulation_chain_holbein",
        "section": "9",
        "title": "Holbein steel regulation chain (all paths)",
        "cypher": """
MATCH path = (bg:Bauteilgruppe {id: 'bg_stahl_mehrere_holbein_structural'})
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
      -[:ERFORDERT_NACHWEIS]->(:Nachweisforderung)
      -[:GESTUETZT_AUF_REGELWERK]->(rw)
      -[:GILT_IN_LAND]->(:Land)
WHERE any(lbl IN labels(rw) WHERE lbl ENDS WITH 'recht')
RETURN path;
""",
    },
    {
        "id": "10_bauteilgruppen_k118",
        "section": "10",
        "title": "K.118 Bauteilgruppen × Bauteiltypen",
        "cypher": """
MATCH (p:Projekt {id: 'p_k118_kopfbau_halle_118_winterthur'})-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
OPTIONAL MATCH (bg)-[t:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
RETURN p, r, bg, t, bt;
""",
    },
    {
        "id": "10b_bauteilgruppen_meduni",
        "section": "10",
        "title": "MedUni Wien Bauteilgruppen × Bauteiltypen",
        "cypher": """
MATCH (p:Projekt {id: 'p_meduni_campus_mariannengasse'})-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
OPTIONAL MATCH (bg)-[t:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
RETURN p, r, bg, t, bt;
""",
    },
    {
        "id": "11_donor_receiver_flows",
        "section": "11",
        "title": "Donor → receiver material flows",
        "cypher": """
MATCH (bg:Bauteilgruppe)-[rs:AUS_SPENDER]->(donor:Bauwerk),
      (bg)-[re:IN_EMPFANGSOBJEKT]->(recv:Bauwerk)
OPTIONAL MATCH (p:Projekt)-[hp:HAT_BAUTEILGRUPPE]->(bg)
RETURN bg, rs, donor, re, recv, p, hp;
""",
    },
    {
        "id": "11b_cross_country_donor_flows",
        "section": "11",
        "title": "Cross-country donor → receiver flows",
        "cypher": """
MATCH (bg:Bauteilgruppe)-[rs:AUS_SPENDER]->(donor:Bauwerk)-[:LIEGT_IN_LAND]->(dl:Land),
      (bg)-[re:IN_EMPFANGSOBJEKT]->(recv:Bauwerk)-[:LIEGT_IN_LAND]->(rl:Land)
WHERE dl <> rl
OPTIONAL MATCH (p:Projekt)-[hp:HAT_BAUTEILGRUPPE]->(bg)
RETURN bg, rs, donor, dl, re, recv, rl, p, hp;
""",
    },
    {
        "id": "12_bauteiltypen_envelope_structure",
        "section": "12",
        "title": "Envelope/structure Bauteiltypen across projects",
        "cypher": """
MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[t:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
WHERE bt.name IN ['Fassade', 'Wand', 'Traeger', 'Fenster', 'Stuetze']
RETURN p, r, bg, t, bt;
""",
    },
    {
        "id": "12b_materials",
        "section": "12",
        "title": "Project × material subgraph",
        "cypher": """
MATCH (p:Projekt)-[r:NUTZT_MATERIAL]->(m:Material)
RETURN p, r, m;
""",
    },
    {
        "id": "13_huerden",
        "section": "13",
        "title": "Reuse barriers (Hürden) network",
        "cypher": """
MATCH (p:Projekt)-[r:HAT_HUERDE]->(h:Huerde)
RETURN p, r, h;
""",
    },
    {
        "id": "14_hub_subgraph",
        "section": "14",
        "title": "Core hub actors subgraph",
        "cypher": """
MATCH (a:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]-(b:Akteur)
WHERE r.review_run IS NOT NULL
  AND (
    a.id IN ['cirkla', 'opalis', 'zirkular', 'concular', 'rotordc', 'useagain_bauteilclick']
    OR b.id IN ['cirkla', 'opalis', 'zirkular', 'concular', 'rotordc', 'useagain_bauteilclick']
  )
RETURN a, r, b;
""",
    },
    {
        "id": "14b_software",
        "section": "14b",
        "title": "Software used in projects",
        "cypher": """
MATCH (p:Projekt)-[r:NUTZT_SOFTWARE]->(sw)
RETURN p, r, sw;
""",
    },
    {
        "id": "14c_geschaeftsmodell",
        "section": "14c",
        "title": "Actor business-model network",
        "cypher": """
MATCH (a:Akteur)-[r:HAT_GESCHAEFTSMODELL]->(gm:Geschaeftsmodell)
RETURN a, r, gm;
""",
    },
]

# Back-compat dict keyed by section id for markdown builder.
GRAPH_QUERIES: dict[str, str] = {
    "1": GRAPH_NETWORKS[0]["cypher"],
    "2": GRAPH_NETWORKS[1]["cypher"],
    "3": GRAPH_NETWORKS[2]["cypher"],
    "4": GRAPH_NETWORKS[3]["cypher"],
    "5": GRAPH_NETWORKS[4]["cypher"],
    "6": GRAPH_NETWORKS[5]["cypher"],
    "7": GRAPH_NETWORKS[6]["cypher"],
    "8": GRAPH_NETWORKS[7]["cypher"],
    "9": GRAPH_NETWORKS[8]["cypher"],
    "10": GRAPH_NETWORKS[9]["cypher"],
    "11": GRAPH_NETWORKS[11]["cypher"],
    "12": GRAPH_NETWORKS[13]["cypher"],
    "13": GRAPH_NETWORKS[15]["cypher"],
    "14": GRAPH_NETWORKS[16]["cypher"],
    "14b_software": GRAPH_NETWORKS[17]["cypher"],
    "14c_geschaeftsmodell": GRAPH_NETWORKS[18]["cypher"],
}
