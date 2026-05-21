"""Probe 2 — find the canonical case_markdown dossier per Projekt and the
exact promotable HAT_BAUTEILGRUPPE candidates."""
from __future__ import annotations

import json
from pathlib import Path

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ENTWERFENMITBESTAND")
DB = "mit-bestand"

RUN_DIR = Path(r"E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset")
driver = GraphDatabase.driver(URI, auth=AUTH)


def q(query, **params):
    with driver.session(database=DB, default_access_mode="READ") as s:
        return [dict(r) for r in s.run(query, **params)]


out: dict = {}

# Projekt that have at least one curated BELEGT_IN to a case_markdown Quelle
out["projekt_with_case_markdown_curated_belegt"] = q(
    """
    MATCH (p:Projekt)-[bel:BELEGT_IN]->(qmd:Quelle {quelltyp:'case_markdown'})
    WHERE bel.evidence_origin='curated'
    RETURN count(DISTINCT p) AS c
    """
)[0]["c"]

# Show a sample of those projects and the dossier id
out["projekt_to_dossier_sample"] = q(
    """
    MATCH (p:Projekt)-[bel:BELEGT_IN]->(qmd:Quelle {quelltyp:'case_markdown'})
    WHERE bel.evidence_origin='curated'
    RETURN p.id AS projekt_id, collect(DISTINCT qmd.id) AS dossiers
    ORDER BY projekt_id
    LIMIT 30
    """
)

# How many HAT_BAUTEILGRUPPE edges are "fully dossier-backed":
# (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
#   AND bg has FROM_DONOR AND INTO_RECEIVER
#   AND p has curated BELEGT_IN to a case_markdown Quelle
out["hat_bg_fully_dossier_backed"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()}
      AND exists{(bg)-[:INTO_RECEIVER]->()}
      AND exists{
        (p)-[bel:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})
        WHERE bel.evidence_origin='curated'
      }
    RETURN count(r) AS c
    """
)[0]["c"]

# Same but FROM_DONOR OR INTO_RECEIVER (looser)
out["hat_bg_partial_dossier_backed"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE (exists{(bg)-[:FROM_DONOR]->()} OR exists{(bg)-[:INTO_RECEIVER]->()})
      AND exists{
        (p)-[bel:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})
        WHERE bel.evidence_origin='curated'
      }
    RETURN count(r) AS c
    """
)[0]["c"]

# Sample of fully-backed HAT_BG candidates with their canonical dossier id
out["fully_backed_sample"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()}
      AND exists{(bg)-[:INTO_RECEIVER]->()}
      AND exists{
        (p)-[bel:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})
        WHERE bel.evidence_origin='curated'
      }
    OPTIONAL MATCH (p)-[bel:BELEGT_IN]->(qmd:Quelle {quelltyp:'case_markdown'})
    WHERE bel.evidence_origin='curated'
    WITH p, bg, r, collect(DISTINCT qmd.id) AS dossiers
    RETURN p.id AS p_id, bg.id AS bg_id, dossiers
    ORDER BY p_id, bg_id
    LIMIT 20
    """
)

# Probe Akteurrolle ids -> name mapping check
out["sample_akteurrolle"] = q(
    """
    MATCH (role:Akteurrolle) RETURN role.id AS id, role.name AS name
    ORDER BY id LIMIT 20
    """
)

# Get all distinct Akteurrolle.id to .name pairs (for completeness in excerpt)
out["all_akteurrolle"] = q(
    """
    MATCH (role:Akteurrolle) RETURN role.id AS id, role.name AS name
    """
)

# Get all Land.id -> name and Akteurtyp.id -> name (small vocabs)
out["all_land"] = q("MATCH (l:Land) RETURN l.id AS id, l.name AS name")
out["all_akteurtyp"] = q("MATCH (t:Akteurtyp) RETURN t.id AS id, t.name AS name")

# Verify Akteur names are populated for excerpt formation
out["akteur_with_name_count"] = q(
    "MATCH (a:Akteur) WHERE a.name IS NOT NULL AND a.name<>'' RETURN count(a) AS c"
)[0]["c"]
out["akteur_total"] = q("MATCH (a:Akteur) RETURN count(a) AS c")[0]["c"]

# Verify Projekt names are populated for excerpts
out["projekt_with_name_count"] = q(
    "MATCH (p:Projekt) WHERE p.name IS NOT NULL AND p.name<>'' RETURN count(p) AS c"
)[0]["c"]
out["projekt_total"] = q("MATCH (p:Projekt) RETURN count(p) AS c")[0]["c"]

# Pre-check: how many master BELEGT_IN actually go to Quelle (OntologyAnchor target should be ignored)
out["master_belegt_in_to_quelle"] = q(
    """
    MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN count(r) AS c
    """
)[0]["c"]
out["master_belegt_in_to_ontologyanchor"] = q(
    """
    MATCH (a:Akteur)-[r:BELEGT_IN]->(b:OntologyAnchor)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN count(r) AS c
    """
)[0]["c"]
out["master_belegt_in_other"] = q(
    """
    MATCH (a)-[r:BELEGT_IN]->(b)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
      AND NOT b:Quelle AND NOT b:OntologyAnchor
    RETURN labels(b) AS b_labels, count(r) AS c
    """
)

# Land.code probe
out["land_with_code"] = q(
    "MATCH (l:Land) RETURN l.id AS id, properties(l) AS props LIMIT 25"
)

print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
(Path(RUN_DIR) / "logs/repair_d_probe2.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
)
driver.close()
