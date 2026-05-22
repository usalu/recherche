"""Analytical query battery for the Zukunft-Bau Vorstudie report.

Writes results to analysis_results.json for the report writer.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from neo4j import GraphDatabase

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

HERE = Path(__file__).resolve().parent

QUERIES: dict[str, str] = {
    # --- Schema reality: how well are components actually described? ---
    "bg_total": "MATCH (bg:Bauteilgruppe) RETURN count(bg) AS n",
    "bg_real_total": """
        MATCH (bg:Bauteilgruppe) WHERE bg.alte_funktion IS NOT NULL OR bg.reuse_status IS NOT NULL
        RETURN count(bg) AS n
    """,
    "bg_field_coverage": """
        MATCH (bg:Bauteilgruppe)
        RETURN
          count(bg) AS total,
          count(bg.bg_kind) AS bg_kind,
          count(bg.reuse_status) AS reuse_status,
          count(bg.bauteilebene) AS bauteilebene,
          count(bg.alte_funktion) AS alte_funktion,
          count(bg.neue_funktion) AS neue_funktion,
          count(bg.funktionswechsel) AS funktionswechsel,
          count(bg.tragend) AS tragend,
          count(bg.tragwerksprinzip) AS tragwerksprinzip,
          count(bg.bauproduktstatus) AS bauproduktstatus,
          count(bg.wiederverwendungsort) AS wiederverwendungsort
    """,
    "bg_rel_coverage": """
        MATCH (bg:Bauteilgruppe)
        RETURN
          count(bg) AS total,
          count { (bg)-[:HAT_BAUTEILTYP]->() } AS hat_bauteiltyp_edges,
          count { (bg)-[:NUTZT_MATERIAL]->() } AS nutzt_material_edges,
          count { (bg)-[:AUS_SPENDER]->() } AS aus_spender_edges,
          count { (bg)-[:IN_EMPFANGSOBJEKT]->() } AS in_empfang_edges,
          count { (bg)-[:ERFORDERT_NACHWEIS]->() } AS nachweis_edges,
          count { (bg)-[:HAT_HUERDE]->() } AS huerde_edges
    """,
    "bg_with_typ": "MATCH (bg:Bauteilgruppe) WHERE (bg)-[:HAT_BAUTEILTYP]->() RETURN count(DISTINCT bg) AS n",
    "bg_with_material": "MATCH (bg:Bauteilgruppe) WHERE (bg)-[:NUTZT_MATERIAL]->() RETURN count(DISTINCT bg) AS n",
    "bg_with_spender": "MATCH (bg:Bauteilgruppe) WHERE (bg)-[:AUS_SPENDER]->() RETURN count(DISTINCT bg) AS n",
    "bg_with_tragend": "MATCH (bg:Bauteilgruppe) WHERE bg.tragend IS NOT NULL RETURN count(bg) AS n",

    # --- Function change: does reuse repurpose components? ---
    "funktionswechsel_split": """
        MATCH (bg:Bauteilgruppe) WHERE bg.funktionswechsel IS NOT NULL
        RETURN bg.funktionswechsel AS funktionswechsel, count(*) AS n ORDER BY n DESC
    """,
    "funktionswechsel_examples": """
        MATCH (bg:Bauteilgruppe)
        WHERE bg.funktionswechsel = true AND bg.alte_funktion IS NOT NULL AND bg.neue_funktion IS NOT NULL
        RETURN bg.alte_funktion AS alt, bg.neue_funktion AS neu LIMIT 15
    """,

    # --- Which proofs / questions dominate (automation priority) ---
    "top_nachweis": """
        MATCH (bg:Bauteilgruppe)-[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
        RETURN nf.name AS nachweis, count(DISTINCT bg) AS bauteilgruppen
        ORDER BY bauteilgruppen DESC
    """,
    "top_regfrage": """
        MATCH (bg:Bauteilgruppe)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
        RETURN rf.name AS frage, count(DISTINCT bg) AS bauteilgruppen
        ORDER BY bauteilgruppen DESC
    """,

    # --- Component vocabulary ranking ---
    "top_bauteiltyp": """
        MATCH (bg:Bauteilgruppe)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
        RETURN bt.name AS bauteiltyp, count(DISTINCT bg) AS bauteilgruppen
        ORDER BY bauteilgruppen DESC
    """,
    "top_material": """
        MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
        RETURN m.name AS material, count(DISTINCT bg) AS bauteilgruppen
        ORDER BY bauteilgruppen DESC
    """,

    # --- Performance data model (Kennwert) -> informs LCA/Tragwerk tool + Auflage h ---
    "kennwert_category": """
        MATCH (k:Kennwert) RETURN k.category AS category, count(*) AS n ORDER BY n DESC
    """,
    "kennwert_named": """
        MATCH (k:Kennwert) RETURN k.kennwert AS kennwert, count(*) AS n ORDER BY n DESC LIMIT 25
    """,
    "kennwert_units": """
        MATCH (k:Kennwert) WHERE k.einheit IS NOT NULL
        RETURN k.einheit AS einheit, count(*) AS n ORDER BY n DESC LIMIT 20
    """,
    "kennwert_method": """
        MATCH (k:Kennwert) WHERE k.method IS NOT NULL
        RETURN k.method AS method, count(*) AS n ORDER BY n DESC LIMIT 15
    """,
    "kennwert_bilanzgrenze": """
        MATCH (k:Kennwert) WHERE k.bilanzgrenze IS NOT NULL
        RETURN k.bilanzgrenze AS bilanzgrenze, count(*) AS n ORDER BY n DESC LIMIT 15
    """,
    "kennwert_numeric_share": """
        MATCH (k:Kennwert)
        RETURN count(*) AS total, count(k.wert) AS mit_zahlwert
    """,

    # --- Bauteilbörsen / multiplicator profiles (integration priority) ---
    "boerse_profiles": """
        MATCH (a:Akteur)
        WHERE a.id IN ['concular','madaster','bauteilnetz_deutschland','opalis','cirkla','restado']
        OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(land:Land)
        RETURN a.id AS id, a.name AS name, land.name AS land,
               count { (a)-[:VERBUNDEN_MIT_AKTEUR]-() } AS grad,
               count { (a)-[:NUTZT_SOFTWARE]->() } AS software,
               count { (a)-[:NUTZT_TOOL]->() } AS tools,
               count { (a)-[:HAT_GESCHAEFTSMODELL]->() } AS geschaeftsmodelle,
               [(a)-[:HAT_AKTEURROLLE]->(r) | r.name] AS rollen
        ORDER BY grad DESC
    """,

    # --- Geschäftsmodelle landscape (supports §8.1 spin-off / cost compensation) ---
    "geschaeftsmodelle": """
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g)
        RETURN coalesce(g.name,g.id) AS geschaeftsmodell, count(DISTINCT a) AS akteure
        ORDER BY akteure DESC
    """,

    # --- Software / tools landscape (competitive context for the tool) ---
    "software_usage": """
        MATCH (x)-[:NUTZT_SOFTWARE|NUTZT_TOOL]->(s)
        RETURN coalesce(s.name,s.id) AS software, count(DISTINCT x) AS nutzer
        ORDER BY nutzer DESC LIMIT 20
    """,

    # --- Test-case candidates for AP-Validierung: best-documented projects ---
    "testcase_candidates": """
        MATCH (p:Projekt)
        OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]->(land:Land)
        WITH p, land,
             count { (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe) } AS bauteilgruppen,
             count { (p)-[:HAT_KENNWERT]->(:Kennwert) } AS kennwerte,
             count { (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:AUS_SPENDER]->(:Bauwerk) } AS spender_links,
             count { (p)-[:ERFORDERT_NACHWEIS]->() } AS nachweise
        WITH p, land, bauteilgruppen, kennwerte, spender_links, nachweise,
             (bauteilgruppen*2 + kennwerte + spender_links*2 + nachweise) AS score
        RETURN p.id AS id, coalesce(p.name,p.id) AS name, land.name AS land,
               bauteilgruppen, kennwerte, spender_links, nachweise, score
        ORDER BY score DESC LIMIT 12
    """,

    # --- Material reality in actual flows (what is really reused) ---
    "flow_materials": """
        MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER]->(:Bauwerk)
        MATCH (bg)-[:NUTZT_MATERIAL]->(m:Material)
        RETURN m.name AS material, count(DISTINCT bg) AS bauteilgruppen
        ORDER BY bauteilgruppen DESC LIMIT 15
    """,

    # --- Hürde by component material (which materials are hardest) ---
    "huerde_by_material": """
        MATCH (m:Material)<-[:NUTZT_MATERIAL]-(bg:Bauteilgruppe)-[:HAT_HUERDE]->(h:Huerde)
        RETURN m.name AS material, count(*) AS huerde_nennungen
        ORDER BY huerde_nennungen DESC LIMIT 12
    """,

    # --- Norm coverage per country (gaps?) ---
    "norm_per_country": """
        MATCH (law)-[:GILT_IN_LAND]->(land:Land)
        WHERE any(l IN labels(law) WHERE l ENDS WITH 'recht')
        RETURN land.name AS land, count(*) AS normknoten
        ORDER BY normknoten DESC
    """,
}


def main() -> None:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    out: dict = {}
    with driver.session(database=database) as session:
        for name, cypher in QUERIES.items():
            rows = [dict(r) for r in session.run(cypher)]
            out[name] = rows
            print(f"\n=== {name} ({len(rows)} rows) ===")
            for r in rows[:14]:
                print("  ", r)
    driver.close()
    (HERE / "analysis_results.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nWrote analysis_results.json")


if __name__ == "__main__":
    main()
