"""Emit :DataIssue nodes for domain nodes with source_urls = [] (QE-2)."""
from __future__ import annotations
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # type: ignore
from neo4j import GraphDatabase

DENYLIST = [
    "Quelle", "Dossier", "ExternalLink", "ResearchDocument", "SectionRef",
    "OntologyAnchor", "DataIssue", "DeprecatedType", "GraphVersion",
    "Land", "Stadt",
]

CYPHER = """
MATCH (n) WHERE n.source_urls IS NOT NULL AND size(n.source_urls) = 0
  AND n.migration_origin CONTAINS 'mig_qext_b_source_urls'
WITH n, [lbl IN labels(n) WHERE NOT lbl IN $deny] AS domain_lbls
WHERE size(domain_lbls) > 0
WITH n, domain_lbls[0] AS primary_lbl
MERGE (di:DataIssue {id: 'di_no_src_' + coalesce(n.id, toString(id(n)))})
ON CREATE SET
  di.kind = 'node_no_source_url',
  di.severity = 'low',
  di.subject_id = coalesce(n.id, ''),
  di.subject_label = primary_lbl,
  di.detected_at = date(),
  di.message = 'No source URLs found via citation graph for ' + primary_lbl + ' node: ' + coalesce(n.id, ''),
  di.migration_origin = 'mig_qext_b_source_urls'
MERGE (n)-[:HAS_DATA_ISSUE]->(di)
RETURN count(di) AS issues_created
"""

uri, user, pwd, _ = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pwd))
with driver.session(database="mit-bestand") as s:
    rows = list(s.run(CYPHER, deny=DENYLIST))
    print("DataIssue nodes created/merged:", rows[0]["issues_created"])
driver.close()
