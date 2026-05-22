"""Build REUSE_NETWORK_CATALOG.md from query_results.json."""

from __future__ import annotations

import json
from pathlib import Path

from _graph_queries import GRAPH_NETWORKS, GRAPH_QUERIES

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "query_results.json"
OUT = ROOT / "REUSE_NETWORK_CATALOG.md"


def q(key: str, data: dict) -> dict:
    return data["queries"][key]


def table(rows: list[dict], columns: list[tuple[str, str]]) -> str:
    if not rows:
        return "_No rows returned._\n"
    header = "| " + " | ".join(c[1] for c in columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        cells = []
        for key, _ in columns:
            val = row.get(key, "")
            if isinstance(val, list):
                val = ", ".join(str(v) for v in val)
            elif isinstance(val, dict):
                val = json.dumps(val, ensure_ascii=False)
            cells.append(str(val).replace("|", "\\|").replace("\n", " "))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def cypher_block(cypher: str) -> str:
    return f"```cypher\n{cypher.strip()}\n```\n"


def section(title: str, graph_key: str, body: str) -> str:
    graph = GRAPH_QUERIES[graph_key]
    return (
        f"## {title}\n\n"
        "**Graph query (Neo4j Browser → Graph view):**\n\n"
        + cypher_block(graph)
        + body
        + "\n"
    )


def main() -> None:
    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    baseline = q("baseline", data)["rows"][0]
    stats = q("n1_actor_constellation_stats", data)["rows"][0]
    swiss = q("swiss_bubble_review_runs", data)["rows"]
    swiss_row = next(r for r in swiss if r["bubble"] == "swiss_reuse_bubble_2026_06_05")
    reg_counts = q("n7_regulation_chain_counts", data)["rows"][0]
    path_row = q("n12_shortest_path_useagain_cstb", data)["rows"][0]

    top_rows = []
    for row in q("n3_top_actors_per_country", data)["rows"]:
        for item in row["top5"][:3]:
            top_rows.append({
                "country": row["country"],
                "actor": item["name"],
                "projects": item["projects"],
            })

    parts: list[str] = [
        "# Semantic Reuse Network Catalog\n\n"
        f"> Live graph snapshot: **{baseline['nodes']} nodes / {baseline['rels']} relationships** "
        f"in `{data['database']}` — generated {data['generated_at'][:10]}.\n\n"
        "Each section has a **graph query** (`RETURN` nodes/relationships/paths for Neo4j Browser Graph view), "
        "executed stats, and a short reading. Paste the Cypher block, run it, switch to **Graph** (not Table). "
        "Extends [`PRESENTATION_REUSE_NETWORKS.md`](../2026-06-06_cross_bubble_extension/PRESENTATION_REUSE_NETWORKS.md).\n",
        section(
            "1. Actor reuse constellation (all countries)",
            "1",
            "**What it shows:** Evidence-tagged reuse coordination links between actors.\n\n"
            f"**Headline:** {stats['directed_tagged']} directed tagged connections across "
            f"{stats['review_runs']} research runs.\n\n"
            "**Stats — actors in network by country:**\n\n"
            + table(
                q("n1_actor_by_country_on_network", data)["rows"],
                [("country", "Country"), ("actors", "Actors in network")],
            )
            + "**Reading:** Dense national clumps joined by long cross-border edges. "
            "Switzerland and Germany dominate; 27 actors lack `LIEGT_IN_LAND`."
        ),
        section(
            "2. Swiss reuse bubble (star network around Cirkla)",
            "2",
            "**What it shows:** Swiss coordination as a centralised star — Cirkla as national directory.\n\n"
            f"**Headline:** {swiss_row['connections']} connections in `swiss_reuse_bubble_2026_06_05`.\n\n"
            "**Stats — all bubbles:**\n\n"
            + table(swiss, [("bubble", "review_run"), ("connections", "Connections")])
            + "**Reading:** Star topology — Cirkla lists depots, consultancies, software. "
            "Zirkular, baubüro in situ, Matériuum orbit the hub."
        ),
        section(
            "3. Actors by country (full registry)",
            "3",
            "**What it shows:** Every geolocated actor linked to its country (`LIEGT_IN_LAND`).\n\n"
            "**Stats — actor counts:**\n\n"
            + table(
                q("n2_all_actors_by_country", data)["rows"],
                [("country", "Country"), ("actors", "Actors")],
            )
            + "**Reading:** 355 actors have no country edge (project-only dossier actors). "
            "CH (111), DE (69), BE (33), NL (32), FR (31) lead among geolocated actors."
        ),
        section(
            "4. Projects × country × actors",
            "4",
            "**What it shows:** Full tripartite network — who participates in which project in which country.\n\n"
            "**Tip:** Large hairball; filter e.g. `WHERE l.name = 'Deutschland'` in Browser.\n\n"
            "**Stats — projects by country:**\n\n"
            + table(
                q("n3_projects_by_country", data)["rows"],
                [("country", "Country"), ("projects", "Projects")],
            )
            + "**Cross-border actors:**\n\n"
            + table(
                q("n3_cross_border_actors", data)["rows"],
                [("name", "Actor"), ("countries", "Countries"), ("projects", "Projects")],
            )
            + "**Reading:** DE/BE/NL lead project counts. Only **Arup** spans UK + Netherlands."
        ),
        section(
            "5. Top actors per country (example: Switzerland)",
            "5",
            "**What it shows:** Actor–project–country subgraph for one country (Schweiz). "
            "Change `Land {name: …}` for other countries.\n\n"
            "**Stats — top 3 actors per country (sample):**\n\n"
            + table(top_rows[:15], [("country", "Country"), ("actor", "Actor"), ("projects", "Projects")])
            + "**Reading:** National champions — Zirkular (4 projects) in CH, Rotor/RotorDC in BE, "
            "Cleveland Steel & Tubes in UK."
        ),
        section(
            "6. Actor–role map",
            "6",
            "**What it shows:** Actors with ≥3 roles and their `HAT_AKTEURROLLE` edges.\n\n"
            "**Stats — top roles:**\n\n"
            + table(
                q("n4_role_frequency", data)["rows"][:10],
                [("role_name", "Role"), ("assignments", "Assignments")],
            )
            + "**Stats — most multi-role actors:**\n\n"
            + table(
                [{"actor": r["name"], "roles": r["role_count"]}
                 for r in q("n4_multi_role_actors", data)["rows"][:8]],
                [("actor", "Actor"), ("roles", "Role count")],
            )
            + "**Reading:** Material hubs (Concular, Matériuum, Bauteilkatalog Basel) carry 6–7 roles — "
            "full-stack reuse operators."
        ),
        section(
            "7. Actor type × role matrix (Materialhub slice)",
            "7",
            "**What it shows:** How `Materialhub_Bauteilboerse` actors combine type and role edges.\n\n"
            "**Stats — top type×role pairs (all types):**\n\n"
            + table(
                q("n5_type_role_matrix", data)["rows"][:12],
                [("actor_type", "Actor type"), ("role", "Role"), ("actors", "Actors")],
            )
            + "**Reading:** Material hubs almost always combine marketplace operator, market supply, "
            "and software/digitalisation."
        ),
        section(
            "8. Norms by country (typed law nodes)",
            "8",
            "**What it shows:** All 91 typed law nodes and their `GILT_IN_LAND` jurisdiction edges.\n\n"
            "**Stats — laws per country:**\n\n"
            + table(
                q("n6_norms_by_country", data)["rows"],
                [("country", "Country"), ("law_nodes", "Law nodes")],
            )
            + "**Multi-country standards (top 5):**\n\n"
            + table(
                q("n6_multi_country_norms", data)["rows"][:5],
                [("law_name", "Standard"), ("country_count", "Countries")],
            )
            + "**Reading:** Germany/EU scopes dominate. 48/91 standards are multi-label across legal domains."
        ),
        section(
            "9. Component → norm regulation chain",
            "9",
            "**What it shows:** Holbein structural steel — path from Bauteilgruppe through "
            "Regulierungsfrage → Nachweisforderung → Tragwerksrecht → Land.\n\n"
            f"**Coverage:** {reg_counts['bgs_with_questions']} Bauteilgruppen trigger questions; "
            f"{reg_counts['bgs_with_law_links']} reach law nodes.\n\n"
            "**Full chain (all domains, more paths):**\n\n"
            + cypher_block(next(n["cypher"] for n in GRAPH_NETWORKS if n["id"] == "09_regulation_chain_holbein"))
            + "**Stats — question/proof summary:**\n\n"
            + table(
                q("n7_regulation_chain_sample", data)["rows"][:8],
                [("question", "Question"), ("proof_required", "Proof"), ("standards", "Standards")],
            )
            + "**Reading:** One steel component triggers Tragwerk, Schadstoff, Bauprodukt, Genehmigung "
            "simultaneously — deepest semantic chain for reuse legitimacy."
        ),
        section(
            "10. Bauteilgruppen from which projects",
            "10",
            "**What it shows:** K.118 project and its Bauteilgruppen + Bauteiltypen.\n\n"
            "**Alternate — top project by component count:**\n\n"
            + cypher_block(next(n["cypher"] for n in GRAPH_NETWORKS if n["id"] == "10b_bauteilgruppen_meduni"))
            + "**Stats — top projects:**\n\n"
            + table(
                [{"project": r["project"], "bg_count": r["bg_count"]}
                 for r in q("n8_bauteilgruppen_by_project", data)["rows"][:8]],
                [("project", "Project"), ("bg_count", "Bauteilgruppen")],
            )
            + "**Reading:** Facades and walls dominate; MedUni Wien (20) and K.118 (16) are best entry points."
        ),
        section(
            "11. Donor → receiver material flows",
            "11",
            "**What it shows:** Bauteilgruppe donor/receiver buildings (`AUS_SPENDER` / `IN_EMPFANGSOBJEKT`).\n\n"
            "**Cross-country subgraph:**\n\n"
            + cypher_block(next(n["cypher"] for n in GRAPH_NETWORKS if n["id"] == "11b_cross_country_donor_flows"))
            + "**Stats — sample flows:**\n\n"
            + table(
                [{"component": r["component"][:40], "project": (r["project"] or "")[:30]}
                 for r in q("n9_donor_receiver_chains", data)["rows"][:6]],
                [("component", "Component"), ("project", "Project")],
            )
            + "**Reading:** Mostly intra-country. Standout: UMAR door handles BE → CH."
        ),
        section(
            "12. Material & Bauteiltyp reuse patterns",
            "12",
            "**What it shows:** Projects linked to envelope/structure Bauteilgruppen and Bauteiltypen.\n\n"
            "**Materials subgraph:**\n\n"
            + cypher_block(next(n["cypher"] for n in GRAPH_NETWORKS if n["id"] == "12b_materials"))
            + "**Stats:**\n\n"
            + table(
                q("n10_top_bauteiltypen_projects", data)["rows"][:8],
                [("bauteiltyp", "Bauteiltyp"), ("projects", "Projects")],
            )
            + "**Reading:** Wand/Fassade in 44+ projects; material tagging sparser than Bauteiltyp."
        ),
        section(
            "13. Reuse barriers (Hürden) network",
            "13",
            "**What it shows:** Projects and their documented reuse obstacles.\n\n"
            "**Stats — top barriers:**\n\n"
            + table(
                q("n11_huerden_by_project", data)["rows"],
                [("barrier", "Barrier"), ("projects", "Projects")],
            )
            + "**Reading:** **Verfügbarkeitsproblem** #1 (16 projects) — reuse is a coordination problem."
        ),
        section(
            "14. Hubs, bridges & synthesis",
            "14",
            "**What it shows:** Core hub actors and their tagged reuse connections.\n\n"
            "**Full tagged constellation:**\n\n"
            + cypher_block(GRAPH_QUERIES["1"])
            + "**Bridge nodes (span ≥2 bubbles):**\n\n"
            + table(
                [{"name": r["name"], "bubbles_spanned": r["bubbles_spanned"]}
                 for r in q("n12_bridge_nodes", data)["rows"][:6]],
                [("name", "Actor"), ("bubbles_spanned", "Bubbles spanned")],
            )
            + f"**Path useagain → CSTB:** `{path_row['hops']}`\n\n"
            "**Reading:** Cirkla & Opalis span 4 bubbles each. Continental bridging remains fragile."
        ),
        "## 14b. Software network\n\n"
        "**Graph query:**\n\n"
        + cypher_block(GRAPH_QUERIES["14b_software"])
        + "**Stats:**\n\n"
        + table(
            q("n12_software_network", data)["rows"][:6],
            [("software", "Software"), ("projects", "Projects")],
        )
        + "\n",
        "## 14c. Business-model network (actors)\n\n"
        "**Graph query:**\n\n"
        + cypher_block(GRAPH_QUERIES["14c_geschaeftsmodell"])
        + "**Stats:**\n\n"
        + table(
            q("n12_geschaeftsmodelle", data)["rows"],
            [("model", "Model"), ("actors", "Actors")],
        )
        + "\n",
        "## Appendix — Quick reference\n\n"
        "| § | Graph pattern | Key rels |\n"
        "|---|---|---|\n"
        "| 1–2 | Actor hubs | `VERBUNDEN_MIT_AKTEUR` |\n"
        "| 3 | Actor → Land | `LIEGT_IN_LAND` |\n"
        "| 4–5 | Actor → Projekt → Land | `BETEILIGT_AN` |\n"
        "| 6–7 | Actor → Rolle/Typ | `HAT_AKTEURROLLE`, `HAT_AKTEURTYP` |\n"
        "| 8 | Law → Land | `GILT_IN_LAND` |\n"
        "| 9 | BG → RF → NF → law → Land | regulation chain |\n"
        "| 10 | Projekt → Bauteilgruppe → Bauteiltyp | `HAT_BAUTEILGRUPPE` |\n"
        "| 11 | BG → donor/recv Bauwerk | `AUS_SPENDER`, `IN_EMPFANGSOBJEKT` |\n"
        "| 12–13 | Projekt → Material/Hürde | `NUTZT_MATERIAL`, `HAT_HUERDE` |\n"
        "| 14 | Hub subgraph | `VERBUNDEN_MIT_AKTEUR` |\n\n"
        "Regenerate stats: `python _run_catalog_queries.py` then `python _build_catalog_md.py`.\n"
        "Export graph JSON (one file per network): `python _export_graph_networks.py` → "
        "[`graph_networks/`](graph_networks/) (see [`manifest.json`](graph_networks/manifest.json)).\n",
    ]

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
