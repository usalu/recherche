"""Probe 3 — clarify destinations and dossier wiring."""
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

# Destinations of the 404 master BELEGT_IN edges, broken down by destination label
out["master_belegt_in_dest_labels"] = q(
    """
    MATCH (a)-[r:BELEGT_IN]->(b)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN labels(b) AS dest_labels, count(r) AS c
    ORDER BY c DESC
    """
)

# Source labels of master BELEGT_IN
out["master_belegt_in_source_labels"] = q(
    """
    MATCH (a)-[r:BELEGT_IN]->(b)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN labels(a) AS src_labels, count(r) AS c
    ORDER BY c DESC
    """
)

# Sample with both labels in detail
out["master_belegt_in_full_samples"] = q(
    """
    MATCH (a)-[r:BELEGT_IN]->(b)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN labels(a) AS a_labels, a.id AS a_id, a.name AS a_name,
           labels(b) AS b_labels, b.id AS b_id, b.name AS b_name,
           properties(r) AS r_props
    LIMIT 10
    """
)

# Is there a curated BELEGT_IN from Projekt to ANY Quelle?
out["projekt_belegt_in_any_curated"] = q(
    """
    MATCH (p:Projekt)-[bel:BELEGT_IN]->(q)
    WHERE bel.evidence_origin='curated'
    RETURN labels(q) AS dest_labels, q.quelltyp AS quelltyp, count(*) AS c
    ORDER BY c DESC
    """
)

# Or, is the dossier evidence keyed by reverse? p_ -> dossier doesn't exist; how about reverse?
# Look for any link between Projekt and its case_markdown dossier
out["projekt_dossier_topology"] = q(
    """
    MATCH (p:Projekt)
    OPTIONAL MATCH (p)-[r]-(qmd:Quelle {quelltyp:'case_markdown'})
    RETURN type(r) AS rel_type, count(r) AS c
    ORDER BY c DESC
    """
)

# Check the FROM_DONOR / INTO_RECEIVER edges' evidence shape
out["from_donor_evidence"] = q(
    """
    MATCH ()-[r:FROM_DONOR]->()
    RETURN r.evidence_origin AS origin, r.evidence_basis AS basis,
           r.evidence_confidence AS conf, count(*) AS c
    ORDER BY c DESC
    """
)
out["into_receiver_evidence"] = q(
    """
    MATCH ()-[r:INTO_RECEIVER]->()
    RETURN r.evidence_origin AS origin, r.evidence_basis AS basis,
           r.evidence_confidence AS conf, count(*) AS c
    ORDER BY c DESC
    """
)

# What dossier IS each BG anchored on (via FROM_DONOR/INTO_RECEIVER source_id)?
out["bg_dossier_via_edges"] = q(
    """
    MATCH (bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()}
    OPTIONAL MATCH (bg)-[r1:FROM_DONOR]->()
    OPTIONAL MATCH (bg)-[r2:INTO_RECEIVER]->()
    RETURN bg.id AS bg_id,
           collect(DISTINCT r1.evidence_source_id) AS from_donor_sources,
           collect(DISTINCT r2.evidence_source_id) AS into_receiver_sources
    LIMIT 10
    """
)

# Find ANY edge between Projekt p and BG bg, all with their evidence shape
out["sample_p_bg_with_dossier_links"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()}
    OPTIONAL MATCH (bg)-[fd:FROM_DONOR]->()
    OPTIONAL MATCH (bg)-[ir:INTO_RECEIVER]->()
    WITH p, bg, r,
         collect(DISTINCT fd.evidence_source_id) AS fd_sources,
         collect(DISTINCT ir.evidence_source_id) AS ir_sources
    RETURN p.id AS p_id, bg.id AS bg_id,
           fd_sources, ir_sources
    LIMIT 10
    """
)

# What's the case_markdown Quelle id for p_55_great_suffolk_street_london (an example)?
out["case_markdown_for_55_great_suffolk"] = q(
    """
    MATCH (p:Projekt {id:'p_55_great_suffolk_street_london'})
    OPTIONAL MATCH (p)-[r]-(q:Quelle)
    RETURN type(r) AS rel_type, q.id AS quelle_id, q.quelltyp AS quelltyp, properties(r) AS r_props
    LIMIT 20
    """
)

# Find BELEGT_IN edges with case_markdown as their evidence_source_id (regardless of curated/excerpt)
out["belegt_in_with_case_markdown_source"] = q(
    """
    MATCH (a)-[r:BELEGT_IN]->(b)
    WHERE r.evidence_source_id STARTS WITH 'q_'
      AND r.evidence_source_id ENDS WITH '_md'
      AND r.evidence_source_id <> 'q_akteursliste_master_md'
    RETURN labels(a)[0] AS a_label, labels(b)[0] AS b_label, count(*) AS c
    ORDER BY c DESC
    LIMIT 20
    """
)

# Does the dossier loader create a (Projekt)-[BELEGT_IN]->(qmd) link?
out["projekt_belegt_in_md_anchor"] = q(
    """
    MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle)
    WHERE q.id STARTS WITH 'q_' AND q.id ENDS WITH '_md'
    RETURN q.quelltyp AS quelltyp, count(r) AS c, r.evidence_origin AS origin
    ORDER BY c DESC
    """
)

# Show some specific examples
out["projekt_belegt_in_md_samples"] = q(
    """
    MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle)
    WHERE q.id STARTS WITH 'q_' AND q.id ENDS WITH '_md'
    RETURN p.id AS p_id, q.id AS q_id, q.quelltyp AS quelltyp,
           properties(r) AS r_props
    LIMIT 10
    """
)

# Now: BGs known via dossier - how do they connect back to a dossier id?
out["bg_evidence_source_ids"] = q(
    """
    MATCH (bg:Bauteilgruppe)
    OPTIONAL MATCH ()-[r:HAT_BAUTEILGRUPPE]->(bg)
    RETURN bg.id AS bg_id, collect(DISTINCT r.evidence_source_id) AS rel_sources,
           bg.source_dossier_id AS bg_src_doss,
           bg.source_id AS bg_src
    LIMIT 5
    """
)

# Check if any link relates BG -> dossier directly
out["bg_to_quelle_paths"] = q(
    """
    MATCH (bg:Bauteilgruppe)
    OPTIONAL MATCH (bg)-[r]-(q:Quelle)
    RETURN type(r) AS rel_type, q.quelltyp AS quelltyp, count(*) AS c
    ORDER BY c DESC
    """
)

# Important: the dossier loader sometimes wrote BELEGT_IN edges WITH excerpts via cell text. Let me find sample curated BELEGT_IN that DO have excerpts (the 2803).
out["existing_curated_with_excerpt_sample"] = q(
    """
    MATCH (a)-[r:BELEGT_IN]->(b)
    WHERE r.evidence_origin='curated'
      AND r.evidence_excerpt IS NOT NULL AND r.evidence_excerpt <> ''
    RETURN labels(a)[0] AS a_label, a.id AS a_id, labels(b)[0] AS b_label, b.id AS b_id,
           r.evidence_basis AS basis, r.evidence_source_id AS src,
           left(r.evidence_excerpt, 200) AS excerpt_head
    LIMIT 10
    """
)

# Are there Projekt -> dossier links with excerpt (e.g. Section-8 facts)?
out["projekt_to_dossier_with_excerpt"] = q(
    """
    MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle {quelltyp:'case_markdown'})
    RETURN p.id AS p_id, q.id AS q_id, r.evidence_origin AS origin,
           r.evidence_basis AS basis, r.evidence_confidence AS conf,
           left(r.evidence_excerpt, 200) AS excerpt_head
    LIMIT 10
    """
)

# Show structure of dossier-related s-ref Quelle (q_<slug>_sNN)
out["sref_quelle_sample"] = q(
    """
    MATCH (q:Quelle)
    WHERE q.id =~ 'q_.*_s[0-9]+'
    RETURN q.id AS q_id, q.quelltyp AS quelltyp, q.url AS url, q.titel AS titel,
           properties(q) AS props
    LIMIT 5
    """
)

# What relationship type connects Projekt to dossier-Section-8 facts?
out["section8_attachment_paths"] = q(
    """
    MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})
    OPTIONAL MATCH (p)-[r:BELEGT_IN]->(target)
    RETURN type(r) AS rel_type, labels(target)[0] AS target_label, target.id AS target_id,
           r.evidence_origin AS origin, r.evidence_basis AS basis,
           r.evidence_confidence AS conf,
           left(r.evidence_excerpt, 200) AS excerpt_head
    LIMIT 20
    """
)

(Path(RUN_DIR) / "logs/repair_d_probe3.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
)
import sys
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
driver.close()
