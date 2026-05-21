"""Probe 4 — diagnose label issues for master BELEGT_IN destinations."""
from __future__ import annotations
import json, sys
from pathlib import Path
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ENTWERFENMITBESTAND")
DB = "mit-bestand"
RUN_DIR = Path(r"E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset")
driver = GraphDatabase.driver(URI, auth=AUTH)
sys.stdout.reconfigure(encoding="utf-8")


def q(query, **params):
    with driver.session(database=DB, default_access_mode="READ") as s:
        return [dict(r) for r in s.run(query, **params)]


out: dict = {}

# Count again: BELEGT_IN where source = master, group by destination label set
out["dest_label_sets"] = q(
    """
    MATCH (a)-[r:BELEGT_IN]->(b)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    WITH labels(b) AS dest_labels, count(*) AS c
    RETURN dest_labels, c
    """
)

# Count grouped by relationship type-only (no destination filter)
out["all_curated_no_excerpt_by_type"] = q(
    """
    MATCH (a)-[r]->(b)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
    WITH type(r) AS t, count(*) AS c
    RETURN t, c
    ORDER BY c DESC
    """
)

# Count by source field
out["curated_no_excerpt_by_source"] = q(
    """
    MATCH (a)-[r]->(b)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
    WITH r.evidence_source_id AS src, count(*) AS c
    RETURN src, c
    ORDER BY c DESC
    LIMIT 40
    """
)

# Check the q_akteursliste_master_md node(s) themselves
out["master_md_nodes"] = q(
    """
    MATCH (n {id:'q_akteursliste_master_md'})
    RETURN labels(n) AS labels, id(n) AS internal_id, properties(n) AS props
    """
)

# Find BELEGT_IN from any (Akteur) to any (q_akteursliste_master_md node)
out["akteur_to_master"] = q(
    """
    MATCH (a:Akteur)-[r:BELEGT_IN]->(b {id:'q_akteursliste_master_md'})
    WHERE r.evidence_origin='curated'
    WITH labels(b) AS dest_labels, count(*) AS c
    RETURN dest_labels, c
    """
)

# Exhaustive: top relationships from akteur b/master_md (any direction)
out["akteur_master_md_any_rel"] = q(
    """
    MATCH (a:Akteur)-[r]-(b {id:'q_akteursliste_master_md'})
    WITH type(r) AS t, count(*) AS c
    RETURN t, c ORDER BY c DESC
    """
)

# Check if any BELEGT_IN edges actually have source pointing to master but go to non-Quelle, non-OntologyAnchor destinations
out["master_dest_any"] = q(
    """
    MATCH (a)-[r:BELEGT_IN]->(b)
    WHERE r.evidence_source_id='q_akteursliste_master_md'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_origin='curated'
    RETURN DISTINCT labels(b) AS dest_labels, count(*) AS c
    """
)

print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
(RUN_DIR / "logs/repair_d_probe4.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
)
driver.close()
