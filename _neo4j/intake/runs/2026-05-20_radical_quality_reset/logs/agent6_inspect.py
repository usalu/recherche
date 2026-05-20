"""Quick post-crash inspection for Agent 6."""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # type: ignore
from neo4j import GraphDatabase  # type: ignore

uri, user, pw, db = resolve_connection()
db = "mit-bestand"
drv = GraphDatabase.driver(uri, auth=(user, pw))
with drv.session(database=db) as s:
    def q(c):
        return list(s.run(c))

    print("projekt_with_year_completed:", q("MATCH (p:Projekt) WHERE p.year_completed IS NOT NULL RETURN count(p) AS c")[0]["c"])
    print("projekt_with_area_m2_gross:", q("MATCH (p:Projekt) WHERE p.area_m2_gross IS NOT NULL RETURN count(p) AS c")[0]["c"])
    print("projekt_with_cost_facts_nonempty:", q("MATCH (p:Projekt) WHERE size(coalesce(p.cost_facts,[])) > 0 RETURN count(p) AS c")[0]["c"])
    print("projekt_with_co2_facts_nonempty:", q("MATCH (p:Projekt) WHERE size(coalesce(p.co2_facts,[])) > 0 RETURN count(p) AS c")[0]["c"])
    print("projekt_with_reuse_share_facts_nonempty:", q("MATCH (p:Projekt) WHERE size(coalesce(p.reuse_share_facts,[])) > 0 RETURN count(p) AS c")[0]["c"])
    print("projekt_with_raw_year_fields:", q("MATCH (p:Projekt) WHERE p.raw_year_fields IS NOT NULL RETURN count(p) AS c")[0]["c"])
    print("projekt_with_jahr_fertigstellung_still:", q("MATCH (p:Projekt) WHERE p.jahr_fertigstellung IS NOT NULL RETURN count(p) AS c")[0]["c"])
    print("projekt_with_flaeche_m2_still:", q("MATCH (p:Projekt) WHERE p.flaeche_m2 IS NOT NULL RETURN count(p) AS c")[0]["c"])
    print("projekt_with_baukosten_eur_still:", q("MATCH (p:Projekt) WHERE p.baukosten_eur IS NOT NULL RETURN count(p) AS c")[0]["c"])
    print("projekt_with_co2_einsparung_t_still:", q("MATCH (p:Projekt) WHERE p.co2_einsparung_t IS NOT NULL RETURN count(p) AS c")[0]["c"])
    print("projekt_with_reuse_anteil_prozent_still:", q("MATCH (p:Projekt) WHERE p.reuse_anteil_prozent IS NOT NULL RETURN count(p) AS c")[0]["c"])
    print("projekt_with_archive:", q("MATCH (p:Projekt) WHERE p._archive IS NOT NULL RETURN count(p) AS c")[0]["c"])
    print("bg_with_menge_source_mig_2_4:", q("MATCH (bg:Bauteilgruppe) WHERE bg.menge_source = 'projekt_counter_migration_mig_2_4' RETURN count(bg) AS c")[0]["c"])
    print("projekt_with_any_anzahl_key:", q("MATCH (p:Projekt) WHERE any(k IN keys(p) WHERE k ENDS WITH '_anzahl' OR k STARTS WITH 'anzahl_') RETURN count(p) AS c")[0]["c"])
    print("quelle_with_external_sources:", q("MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) AS c")[0]["c"])
    print("zitiert_quelle_count:", q("MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS c")[0]["c"])
    print("polluted_edges_with_origin_null:", q("MATCH ()-[r]->() WHERE (r.source IS NOT NULL OR r.evidence IS NOT NULL OR r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL) AND r.evidence_origin IS NULL RETURN count(r) AS c")[0]["c"])
    print("akteur_with_raw_role_evidence:", q("MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL RETURN count(a) AS c")[0]["c"])
    sample_facts = q("MATCH (p:Projekt) WHERE size(coalesce(p.cost_facts,[]))>0 RETURN p.id, p.cost_facts LIMIT 3")
    print("sample cost_facts:")
    for r in sample_facts:
        print(" ", r["p.id"], r["p.cost_facts"])
    sample_year = q("MATCH (p:Projekt) WHERE p.raw_year_fields IS NOT NULL AND p.year_completed IS NOT NULL RETURN p.id, p.year_completed, p.raw_year_fields LIMIT 3")
    print("sample year:")
    for r in sample_year:
        print(" ", r["p.id"], r["p.year_completed"], r["p.raw_year_fields"])
drv.close()
