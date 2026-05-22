"""Receiver Showcase view — exploratory probes against the live Neo4j DB.

Iterative tool: each section asks one question of the graph and prints results
compactly. Re-run sections by editing the SECTION variable.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402


def heading(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def rows(session, cypher: str, **params):
    return session.run(cypher, **params).data()


def run_section(section: str, session) -> None:
    if section == "0_universe":
        heading("[0] Universe: project counts + recent vs older")
        r = rows(session, "MATCH (p:Projekt) RETURN count(p) AS n")
        print("Total Projekt:", r[0]["n"])
        r = rows(
            session,
            "MATCH (p:Projekt) WHERE p.year_completed IS NOT NULL "
            "RETURN count(p) AS n_with_year, min(p.year_completed) AS min_y, "
            "max(p.year_completed) AS max_y",
        )
        print("With year_completed:", r[0])
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "WITH p, (CASE WHEN p.year_completed IS NULL THEN 'unknown' "
            "WHEN p.year_completed < 2000 THEN '<2000' "
            "WHEN p.year_completed < 2010 THEN '2000-2009' "
            "WHEN p.year_completed < 2020 THEN '2010-2019' "
            "ELSE '2020+' END) AS bucket "
            "RETURN bucket, count(*) AS n ORDER BY bucket",
        )
        print("Buckets:")
        for x in r:
            print(f"  {x['bucket']:>10s}: {x['n']}")

    elif section == "1_properties":
        heading("[1] Projekt property coverage (which props are filled?)")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "RETURN "
            "  count(p) AS n_total, "
            "  count(p.name) AS n_name, "
            "  count(p.name_full) AS n_name_full, "
            "  count(p.year_completed) AS n_year, "
            "  count(p.source_count) AS n_source_count, "
            "  count(p.description) AS n_description, "
            "  count(p.source_status) AS n_source_status",
        )
        print(json.dumps(r[0], indent=2))

        # Show all distinct property keys on Projekt
        r = rows(
            session,
            "MATCH (p:Projekt) WITH p LIMIT 200 "
            "UNWIND keys(p) AS k RETURN DISTINCT k ORDER BY k",
        )
        print("Distinct property keys seen on Projekt (sample of 200):")
        for x in r:
            print(" ", x["k"])

    elif section == "2_geography":
        heading("[2] Geography: where are receiver projects located?")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]->(l:Land) "
            "RETURN coalesce(l.name, '<unknown>') AS land, count(p) AS n "
            "ORDER BY n DESC",
        )
        print("By country (direct LIEGT_IN_LAND):")
        for x in r:
            print(f"  {x['land']:>16s}: {x['n']}")

        # Indirect via Bauwerk / Stadt
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "OPTIONAL MATCH (p)-[:NUTZT_BAUWERK]->(:Bauwerk)-[:LIEGT_IN_LAND]->(l:Land) "
            "WITH p, collect(DISTINCT l.name) AS lands "
            "RETURN size(lands) AS n_lands, count(p) AS n_projects",
        )
        print("Projects by # of countries (via Bauwerk):")
        for x in r:
            print(f"  {x['n_lands']} land(s): {x['n_projects']} projects")

    elif section == "3_intervention":
        heading("[3] Intervention type distribution")
        r = rows(
            session,
            "MATCH (p:Projekt)-[:HAT_INTERVENTION]->(i:BauaufgabeIntervention) "
            "RETURN i.name AS intervention, count(p) AS n ORDER BY n DESC",
        )
        for x in r:
            print(f"  {x['intervention']:>30s}: {x['n']}")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "WHERE NOT EXISTS {(p)-[:HAT_INTERVENTION]->(:BauaufgabeIntervention)} "
            "RETURN count(p) AS n",
        )
        print(f"  {'<none>':>30s}: {r[0]['n']}")

    elif section == "4_reuse_type":
        heading("[4] Reuse type (WiederverwendungsArt) per project")
        r = rows(
            session,
            "MATCH (p:Projekt)-[:HAT_WIEDERVERWENDUNGSART]->(w:WiederverwendungsArt) "
            "RETURN w.name AS art, count(DISTINCT p) AS n_projects ORDER BY n_projects DESC",
        )
        for x in r:
            print(f"  {x['art']:>40s}: {x['n_projects']}")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "WHERE NOT EXISTS {(p)-[:HAT_WIEDERVERWENDUNGSART]->()} "
            "RETURN count(p) AS n",
        )
        print(f"  {'<no reuse type>':>40s}: {r[0]['n']}")

    elif section == "5_reuse_share":
        heading("[5] Reuse intensity — Kennwert reuse_anteil_prozent")
        r = rows(
            session,
            "MATCH (p:Projekt)-[:HAT_KENNWERT]->(k:Kennwert) "
            "WHERE toLower(coalesce(k.kennwert,'')) CONTAINS 'reuse_anteil' "
            "   OR toLower(coalesce(k.kennwert,'')) CONTAINS 'reuse-anteil' "
            "   OR toLower(coalesce(k.kennwert,'')) CONTAINS 'wiederverwendung' "
            "RETURN p.name AS project, k.kennwert AS metric, k.wert AS value, "
            "       k.method AS method "
            "ORDER BY coalesce(k.wert, -1) DESC LIMIT 30",
        )
        print(f"Top reuse-share kennwerte (max 30): {len(r)} rows")
        for x in r:
            wert = x.get("value")
            wert_s = f"{wert}" if wert is not None else "n/a"
            print(f"  {x['project'][:42]:<42s} | {x['metric'][:24]:<24s} | {wert_s}")

        # Count distinct projects with ANY reuse-share kennwert
        r = rows(
            session,
            "MATCH (p:Projekt)-[:HAT_KENNWERT]->(k:Kennwert) "
            "WHERE toLower(coalesce(k.kennwert,'')) CONTAINS 'reuse_anteil' "
            "   OR toLower(coalesce(k.kennwert,'')) CONTAINS 'reuse-anteil' "
            "   OR toLower(coalesce(k.kennwert,'')) CONTAINS 'wiederverwendung' "
            "RETURN count(DISTINCT p) AS n_projects",
        )
        print(f"Distinct Projekt with reuse-share Kennwert: {r[0]['n_projects']}")

    elif section == "6_component_richness":
        heading("[6] Component richness per project (how detailed is the doc?)")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) "
            "WITH p, count(bg) AS n_bg "
            "RETURN p.name AS project, n_bg ORDER BY n_bg DESC LIMIT 20",
        )
        print("Top 20 projects by # Bauteilgruppe:")
        for x in r:
            print(f"  {x['project'][:50]:<50s} | {x['n_bg']:>3d} bg")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) "
            "WITH p, count(bg) AS n_bg "
            "RETURN (CASE WHEN n_bg = 0 THEN '0' "
            "WHEN n_bg < 3 THEN '1-2' "
            "WHEN n_bg < 6 THEN '3-5' "
            "WHEN n_bg < 11 THEN '6-10' "
            "ELSE '11+' END) AS bucket, count(*) AS n "
            "ORDER BY bucket",
        )
        print("Histogram:")
        for x in r:
            print(f"  {x['bucket']:>6s}: {x['n']}")

    elif section == "7_status_mix":
        heading("[7] Project lifecycle Status distribution")
        r = rows(
            session,
            "MATCH (p:Projekt)-[:HAT_STATUS]->(s:Status) "
            "RETURN s.name AS status, s.kind AS kind, count(DISTINCT p) AS n "
            "ORDER BY n DESC",
        )
        for x in r:
            print(f"  {x['status']:>16s} ({x['kind']:>10s}): {x['n']}")

    elif section == "8_donor_count":
        heading("[8] How many donor Bauwerke does each project pull from?")
        r = rows(
            session,
            "MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)"
            "-[:FROM_DONOR]->(d:Bauwerk) "
            "WITH p, count(DISTINCT d) AS n_donors "
            "RETURN p.name AS project, n_donors ORDER BY n_donors DESC LIMIT 15",
        )
        print("Top 15 projects by # donor Bauwerke:")
        for x in r:
            print(f"  {x['project'][:50]:<50s} | {x['n_donors']:>3d}")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:FROM_DONOR]->(d:Bauwerk) "
            "WITH p, count(DISTINCT d) AS nd "
            "RETURN (CASE WHEN nd=0 THEN '0' WHEN nd=1 THEN '1' "
            "WHEN nd<5 THEN '2-4' ELSE '5+' END) AS bucket, count(*) AS n "
            "ORDER BY bucket",
        )
        print("Histogram:")
        for x in r:
            print(f"  {x['bucket']:>5s}: {x['n']}")

    elif section == "10_facts_props":
        heading("[10] Facts-as-properties: reuse_share_facts, co2_facts, cost_facts")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "RETURN "
            "  count(p.reuse_share_facts) AS n_reuse, "
            "  count(p.co2_facts) AS n_co2, "
            "  count(p.cost_facts) AS n_cost, "
            "  count(p.quality_tier_facts) AS n_qtier, "
            "  count(p.source_freshness_summary) AS n_fresh, "
            "  count(p.source_quality_summary) AS n_qual, "
            "  count(p.source_trust_score) AS n_trust",
        )
        print(json.dumps(r[0], indent=2))
        # Inspect one sample value of reuse_share_facts
        r = rows(
            session,
            "MATCH (p:Projekt) WHERE p.reuse_share_facts IS NOT NULL "
            "RETURN p.name AS project, p.reuse_share_facts AS facts LIMIT 5",
        )
        print("\nSample reuse_share_facts values:")
        for x in r:
            print(f"  {x['project'][:30]}: {str(x['facts'])[:120]}")
        r = rows(
            session,
            "MATCH (p:Projekt) WHERE p.co2_facts IS NOT NULL "
            "RETURN p.name AS project, p.co2_facts AS facts LIMIT 5",
        )
        print("\nSample co2_facts values:")
        for x in r:
            print(f"  {x['project'][:30]}: {str(x['facts'])[:120]}")
        r = rows(
            session,
            "MATCH (p:Projekt) WHERE p.cost_facts IS NOT NULL "
            "RETURN p.name AS project, p.cost_facts AS facts LIMIT 5",
        )
        print("\nSample cost_facts values:")
        for x in r:
            print(f"  {x['project'][:30]}: {str(x['facts'])[:120]}")

    elif section == "11_category_size":
        heading("[11] project_category + area_m2_gross + bewertung + quality_tier")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "RETURN p.project_category AS cat, count(*) AS n ORDER BY n DESC",
        )
        print("project_category distribution:")
        for x in r:
            print(f"  {str(x['cat'])[:40]:>40s}: {x['n']}")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "RETURN "
            "  count(p.area_m2_gross) AS n_area, "
            "  count(p.area_m2_range_min) AS n_amin, "
            "  count(p.bewertung) AS n_bew, "
            "  count(p.quality_tier) AS n_qt",
        )
        print(json.dumps(r[0], indent=2))
        r = rows(
            session,
            "MATCH (p:Projekt) WHERE p.quality_tier IS NOT NULL "
            "RETURN p.quality_tier AS qt, count(*) AS n ORDER BY n DESC",
        )
        print("\nquality_tier distribution:")
        for x in r:
            print(f"  {x['qt']:>20s}: {x['n']}")
        r = rows(
            session,
            "MATCH (p:Projekt) WHERE p.bewertung IS NOT NULL "
            "RETURN p.bewertung AS b, count(*) AS n ORDER BY n DESC LIMIT 20",
        )
        print("\nbewertung values:")
        for x in r:
            print(f"  {str(x['b'])[:50]:>50s}: {x['n']}")

    elif section == "12_programs":
        heading("[12] Programmes (TEIL_VON_PROGRAMM)")
        r = rows(
            session,
            "MATCH (p:Projekt)-[:TEIL_VON_PROGRAMM]->(pr:Programm) "
            "RETURN pr.name AS programme, count(DISTINCT p) AS n_projects "
            "ORDER BY n_projects DESC",
        )
        for x in r:
            print(f"  {x['programme'][:50]:>50s}: {x['n_projects']}")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "WHERE NOT EXISTS {(p)-[:TEIL_VON_PROGRAMM]->()} "
            "RETURN count(p) AS n",
        )
        print(f"  {'<no programme>':>50s}: {r[0]['n']}")

    elif section == "13_actors":
        heading("[13] Actor role mix on receiver projects")
        r = rows(
            session,
            "MATCH (p:Projekt)<-[:BETEILIGT_AN]-(a:Akteur)-[:HAT_AKTEURROLLE]->(role:Akteurrolle) "
            "RETURN role.name AS role, count(DISTINCT a) AS n_distinct_actors, "
            "       count(DISTINCT p) AS n_projects "
            "ORDER BY n_projects DESC",
        )
        for x in r:
            print(
                f"  {x['role'][:30]:>30s}: {x['n_distinct_actors']:>4d} actors "
                f"across {x['n_projects']} projects"
            )
        # How many distinct actors per project, on average
        r = rows(
            session,
            "MATCH (p:Projekt)<-[:BETEILIGT_AN]-(a:Akteur) "
            "WITH p, count(DISTINCT a) AS na "
            "RETURN min(na) AS mn, max(na) AS mx, avg(na) AS avg",
        )
        print(f"\nActors per project (BETEILIGT_AN): min={r[0]['mn']} max={r[0]['mx']} avg={r[0]['avg']:.1f}")

    elif section == "14_richness_score":
        heading("[14] Composite richness score = candidate ambition proxy")
        # Build a composite ambition score per project:
        # 0.4 * normalized(n_bauteilgruppe)
        # 0.2 * has_reuse_share_kennwert
        # 0.2 * normalized(n_donors)
        # 0.1 * n_actors
        # 0.1 * has_kennwert_for_co2
        q = (
            "MATCH (p:Projekt) "
            "OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) "
            "WITH p, count(bg) AS n_bg "
            "OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:FROM_DONOR]->(d:Bauwerk) "
            "WITH p, n_bg, count(DISTINCT d) AS n_d "
            "OPTIONAL MATCH (p)<-[:BETEILIGT_AN]-(a:Akteur) "
            "WITH p, n_bg, n_d, count(DISTINCT a) AS n_a "
            "OPTIONAL MATCH (p)-[:HAT_KENNWERT]->(k1:Kennwert) "
            "WHERE toLower(coalesce(k1.kennwert,'')) CONTAINS 'reuse_anteil' OR "
            "      toLower(coalesce(k1.kennwert,'')) CONTAINS 'reuse-anteil' "
            "WITH p, n_bg, n_d, n_a, count(k1) > 0 AS has_reuse_kw "
            "OPTIONAL MATCH (p)-[:HAT_KENNWERT]->(k2:Kennwert) "
            "WHERE toLower(coalesce(k2.kennwert,'')) CONTAINS 'co2' "
            "WITH p, n_bg, n_d, n_a, has_reuse_kw, count(k2) > 0 AS has_co2_kw "
            "RETURN p.name AS project, n_bg, n_d, n_a, has_reuse_kw, has_co2_kw, "
            "       p.year_completed AS year "
            "ORDER BY n_bg DESC, n_d DESC, n_a DESC LIMIT 25"
        )
        r = rows(session, q)
        print(f"Top 25 by component+donor+actor richness:")
        print(
            f"  {'project':<40s} | {'yr':>4s} | {'bg':>3s} | {'don':>3s} | "
            f"{'act':>3s} | {'r%':>3s} | {'co2':>3s}"
        )
        for x in r:
            yr = str(x.get("year") or "?")[:4]
            print(
                f"  {x['project'][:40]:<40s} | {yr:>4s} | {x['n_bg']:>3d} | "
                f"{x['n_d']:>3d} | {x['n_a']:>3d} | "
                f"{'Y' if x['has_reuse_kw'] else '-':>3s} | "
                f"{'Y' if x['has_co2_kw'] else '-':>3s}"
            )

    elif section == "15_tier_vs_richness":
        heading("[15] quality_tier × component richness × reuse_kw")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) "
            "WITH p, count(bg) AS n_bg "
            "OPTIONAL MATCH (p)-[:HAT_KENNWERT]->(k:Kennwert) "
            "WHERE toLower(coalesce(k.kennwert,'')) CONTAINS 'reuse_anteil' OR "
            "      toLower(coalesce(k.kennwert,'')) CONTAINS 'reuse-anteil' "
            "WITH p, n_bg, count(k) > 0 AS has_reuse_kw "
            "RETURN p.quality_tier AS tier, "
            "       count(*) AS n_proj, "
            "       avg(n_bg) AS avg_bg, "
            "       max(n_bg) AS max_bg, "
            "       sum(CASE WHEN n_bg = 0 THEN 1 ELSE 0 END) AS n_zero_bg, "
            "       sum(CASE WHEN has_reuse_kw THEN 1 ELSE 0 END) AS n_with_reuse_kw "
            "ORDER BY tier",
        )
        for x in r:
            print(
                f"  {x['tier']:>28s} | n={x['n_proj']:>3d} | "
                f"avg_bg={x['avg_bg']:.1f} | max_bg={x['max_bg']:>3d} | "
                f"zero_bg={x['n_zero_bg']:>2d} | with_reuse_kw={x['n_with_reuse_kw']:>2d}"
            )

    elif section == "16_sources_per_project":
        heading("[16] Source evidence density per project")
        # Quelle attached via BELEGT_IN (relationship-level) or CONCERNS
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "OPTIONAL MATCH (p)-[:BELEGT_IN]->(q:Quelle) "
            "WITH p, count(DISTINCT q) AS n_quelle "
            "OPTIONAL MATCH (p)-[:BELEGT_IN]->(d:Dossier) "
            "WITH p, n_quelle, count(DISTINCT d) AS n_dossier "
            "RETURN p.quality_tier AS tier, count(*) AS n_proj, "
            "       avg(n_quelle) AS avg_q, "
            "       avg(n_dossier) AS avg_d, "
            "       sum(CASE WHEN n_quelle=0 AND n_dossier=0 THEN 1 ELSE 0 END) AS n_no_source "
            "ORDER BY tier",
        )
        for x in r:
            print(
                f"  {x['tier']:>28s} | n={x['n_proj']:>3d} | "
                f"avg_quelle={x['avg_q']:.1f} | avg_dossier={x['avg_d']:.1f} | "
                f"no_source_node={x['n_no_source']:>2d}"
            )

        # And source_count property
        r = rows(
            session,
            "MATCH (p:Projekt) WHERE p.source_count IS NOT NULL "
            "RETURN p.quality_tier AS tier, "
            "       count(*) AS n, avg(p.source_count) AS avg_sc, "
            "       max(p.source_count) AS max_sc "
            "ORDER BY tier",
        )
        print("\nproperty source_count (where present):")
        for x in r:
            print(f"  {x['tier']:>28s}: n={x['n']:>3d} avg={x['avg_sc']:.1f} max={x['max_sc']}")

    elif section == "17_ecosystem_completeness":
        heading("[17] Actor-ecosystem completeness per project")
        # Define core roles for a complete ecosystem
        core_roles = [
            "Bauherr_Auftraggeber",
            "Entwurf_Planung",
            "Fachplanung_Nachweis",
            "Bauausfuehrung_Fertigung",
            "Reuse_Zirkularitaetsberatung",
        ]
        for role in core_roles:
            r = rows(
                session,
                "MATCH (p:Projekt) "
                "WHERE EXISTS { (p)<-[:BETEILIGT_AN]-(:Akteur)"
                "-[:HAT_AKTEURROLLE]->(r:Akteurrolle {name:$role}) } "
                "RETURN count(p) AS n",
                role=role,
            )
            print(f"  has {role:>32s}: {r[0]['n']:>3d}/101")

        # How many projects have ALL 5 core roles?
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "OPTIONAL MATCH (p)<-[:BETEILIGT_AN]-(:Akteur)-[:HAT_AKTEURROLLE]->(role:Akteurrolle) "
            "WITH p, collect(DISTINCT role.name) AS roles "
            "WITH p, [r IN $core WHERE r IN roles] AS hits "
            "RETURN size(hits) AS n_core_present, count(*) AS n_projects "
            "ORDER BY n_core_present DESC",
            core=core_roles,
        )
        print("\nDistribution of # of 5 core roles present:")
        for x in r:
            print(f"  {x['n_core_present']}/5 core roles: {x['n_projects']} projects")

    elif section == "18_perfect_showcase":
        heading("[18] Perfect Showcase candidates (tier_1 + rich + multi-sourced)")
        r = rows(
            session,
            "MATCH (p:Projekt) "
            "OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) "
            "WITH p, count(bg) AS n_bg "
            "OPTIONAL MATCH (p)<-[:BETEILIGT_AN]-(a:Akteur) "
            "WITH p, n_bg, count(DISTINCT a) AS n_a "
            "OPTIONAL MATCH (p)-[:BELEGT_IN]->(q:Quelle) "
            "WITH p, n_bg, n_a, count(DISTINCT q) AS n_q "
            "OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:FROM_DONOR]->(d:Bauwerk) "
            "WITH p, n_bg, n_a, n_q, count(DISTINCT d) AS n_d "
            "OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]->(l:Land) "
            "WITH p, n_bg, n_a, n_q, n_d, l "
            "OPTIONAL MATCH (p)-[:HAT_INTERVENTION]->(i:BauaufgabeIntervention) "
            "WITH p, n_bg, n_a, n_q, n_d, l, collect(DISTINCT i.name) AS interventions "
            "OPTIONAL MATCH (p)-[:HAT_WIEDERVERWENDUNGSART]->(w:WiederverwendungsArt) "
            "WITH p, n_bg, n_a, n_q, n_d, l, interventions, collect(DISTINCT w.name) AS reuse_types "
            "WHERE p.quality_tier = 'tier_1_decision_grade' "
            "RETURN p.name AS project, p.year_completed AS year, l.name AS land, "
            "       n_bg, n_d, n_a, n_q, "
            "       p.bewertung AS rating, p.source_trust_score AS trust, "
            "       interventions, reuse_types "
            "ORDER BY n_bg DESC",
        )
        print(f"All tier_1_decision_grade projects ({len(r)} total):\n")
        for x in r:
            yr = str(x.get("year") or "?")
            land = x.get("land") or "?"
            iv = ",".join(x.get("interventions") or [])[:30]
            rt = ",".join(x.get("reuse_types") or [])[:30]
            print(
                f"  {x['project'][:35]:<35s} | {yr:>4s} | {land[:14]:<14s} | "
                f"bg={x['n_bg']:>2d} d={x['n_d']:>2d} a={x['n_a']:>2d} q={x['n_q']:>2d} | "
                f"⭐={x.get('rating')} trust={x.get('trust')}"
            )
            print(f"      interventions: {iv}")
            print(f"      reuse types  : {rt}")

    elif section == "9_one_project_full":
        heading("[9] One sample receiver project: full edge fingerprint")
        # Pick a project with high Bauteilgruppe count (storyable)
        r = rows(
            session,
            "MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) "
            "WITH p, count(bg) AS n_bg ORDER BY n_bg DESC LIMIT 1 "
            "RETURN p.id AS pid, p.name AS name, n_bg",
        )
        if not r:
            print("No project found with Bauteilgruppe edges.")
            return
        pid = r[0]["pid"]
        print(f"Sampled project: {pid} ({r[0]['name']}) — {r[0]['n_bg']} Bauteilgruppe")

        r = rows(
            session,
            "MATCH (p:Projekt {id:$pid})-[r]-(n) "
            "RETURN type(r) AS rel, labels(n) AS labels, count(*) AS n "
            "ORDER BY n DESC",
            pid=pid,
        )
        print("Relationship fingerprint:")
        for x in r:
            print(f"  {x['rel']:>30s} -> {','.join(x['labels'])[:30]:<30s}: {x['n']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--sections",
        default="all",
        help="comma-separated section keys, or 'all'",
    )
    args = ap.parse_args()

    all_sections = [
        "0_universe",
        "1_properties",
        "2_geography",
        "3_intervention",
        "4_reuse_type",
        "5_reuse_share",
        "6_component_richness",
        "7_status_mix",
        "8_donor_count",
        "9_one_project_full",
        "10_facts_props",
        "11_category_size",
        "12_programs",
        "13_actors",
        "14_richness_score",
    ]
    if args.sections == "all":
        sections = all_sections
    else:
        sections = [s.strip() for s in args.sections.split(",") if s.strip()]

    uri, user, pw, db = resolve_connection()
    if not uri:
        print("ERROR: no NEO4J_URI; check .cursor/mcp.json or env.")
        return 1
    print(f"Connecting to {uri} db={db} as {user!r}")
    driver = GraphDatabase.driver(uri, auth=(user, pw))
    try:
        with driver.session(database=db) as session:
            for s in sections:
                run_section(s, session)
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
