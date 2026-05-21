"""Probe 6 — diagnose the 4 post-migration audit failures."""
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

# 11 remaining curated_no_excerpt
out["curated_no_excerpt_remaining"] = q(
    """
    MATCH (a)-[r]->(b)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
    RETURN type(r) AS t, r.evidence_basis AS basis,
           r.evidence_source_id AS src,
           labels(a) AS a_labels, a.id AS a_id, a.name AS a_name,
           labels(b) AS b_labels, b.id AS b_id, b.name AS b_name,
           properties(r) AS r_props
    """
)

# 22 origin_enum violations
out["origin_enum_violations"] = q(
    """
    MATCH (a)-[r]->(b)
    WHERE r.evidence_origin IS NOT NULL
      AND NOT r.evidence_origin IN ['curated','inferred','derived']
    RETURN r.evidence_origin AS bad_origin, type(r) AS t, count(*) AS c
    ORDER BY c DESC
    """
)
out["origin_enum_samples"] = q(
    """
    MATCH (a)-[r]->(b)
    WHERE r.evidence_origin IS NOT NULL
      AND NOT r.evidence_origin IN ['curated','inferred','derived']
    RETURN type(r) AS t, r.evidence_origin AS bad_origin,
           labels(a) AS a_labels, a.id AS a_id,
           labels(b) AS b_labels, b.id AS b_id,
           properties(r) AS r_props
    LIMIT 10
    """
)

# 22 confidence_enum violations
out["confidence_enum_violations"] = q(
    """
    MATCH (a)-[r]->(b)
    WHERE r.evidence_confidence IS NOT NULL
      AND NOT r.evidence_confidence IN ['belegt','teilweise_belegt','unklar','inferiert','bookkeeping']
    RETURN r.evidence_confidence AS bad_conf, type(r) AS t, count(*) AS c
    ORDER BY c DESC
    """
)
out["confidence_enum_samples"] = q(
    """
    MATCH (a)-[r]->(b)
    WHERE r.evidence_confidence IS NOT NULL
      AND NOT r.evidence_confidence IN ['belegt','teilweise_belegt','unklar','inferiert','bookkeeping']
    RETURN type(r) AS t, r.evidence_confidence AS bad_conf,
           labels(a) AS a_labels, a.id AS a_id,
           labels(b) AS b_labels, b.id AS b_id,
           properties(r) AS r_props
    LIMIT 10
    """
)

# 243 citation_basis_enum violations
out["citation_basis_violations"] = q(
    """
    MATCH (a)-[r]->(b)
    WHERE type(r) IN [
      'BELEGT_IN','BETEILIGT_AN','ASSOZIIERT_MIT_PROJEKT',
      'AUS_BAUWERK','FROM_DONOR','EINGEBAUT_IN','INTO_RECEIVER',
      'HAT_BAUTEILGRUPPE','HAT_HUERDE','HAT_AKTEURROLLE'
    ]
    AND NOT r.evidence_basis IN ['cell_citation','registry_stub','propagated','controlled_vocab']
    RETURN type(r) AS t, r.evidence_basis AS bad_basis, count(*) AS c
    ORDER BY c DESC
    """
)
out["citation_basis_samples"] = q(
    """
    MATCH (a)-[r]->(b)
    WHERE type(r) IN [
      'BELEGT_IN','BETEILIGT_AN','ASSOZIIERT_MIT_PROJEKT',
      'AUS_BAUWERK','FROM_DONOR','EINGEBAUT_IN','INTO_RECEIVER',
      'HAT_BAUTEILGRUPPE','HAT_HUERDE','HAT_AKTEURROLLE'
    ]
    AND NOT r.evidence_basis IN ['cell_citation','registry_stub','propagated','controlled_vocab']
    RETURN type(r) AS t, r.evidence_basis AS bad_basis,
           labels(a) AS a_labels, a.id AS a_id,
           labels(b) AS b_labels, b.id AS b_id,
           r.evidence_origin AS origin,
           r.evidence_source_id AS src,
           left(coalesce(r.evidence_excerpt,''), 120) AS excerpt_head
    LIMIT 20
    """
)

print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
(RUN_DIR / "logs/repair_d_probe6.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
)
driver.close()
