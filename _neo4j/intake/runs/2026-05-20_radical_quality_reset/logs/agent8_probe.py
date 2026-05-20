"""Agent 8 — Phase 4c pre-flight probe (read-only)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # type: ignore
from neo4j import GraphDatabase  # type: ignore


def main() -> int:
    uri, user, password, database = resolve_connection()
    if database != "mit-bestand":
        database = "mit-bestand"
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    out: dict = {}
    with driver.session(database=database) as s:
        q = s.run
        out["total_nodes"] = q("MATCH (n) RETURN count(n) AS c").single()["c"]
        out["total_rels"] = q("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
        out["quelle_total"] = q("MATCH (q:Quelle) RETURN count(q) AS c").single()["c"]
        out["quelle_with_external_sources"] = q(
            "MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) AS c"
        ).single()["c"]
        out["zitiert_quelle_total"] = q(
            "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS c"
        ).single()["c"]
        out["zitiert_quelle_mig_2_7"] = q(
            "MATCH ()-[r:ZITIERT_QUELLE]->() WHERE r.evidence_basis = 'external_sources_array' "
            "RETURN count(r) AS c"
        ).single()["c"]
        out["quelle_quelltyp_breakdown"] = {
            r["q"]: r["c"]
            for r in q(
                "MATCH (q:Quelle) RETURN coalesce(q.quelltyp,'<null>') AS q, count(q) AS c "
                "ORDER BY c DESC"
            )
        }
        out["projekt_belegt_actor_registry"] = q(
            "MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle) "
            "WHERE q.quelltyp = 'external_link_from_actor_registry' "
            "RETURN count(r) AS c"
        ).single()["c"]
        out["akteur_belegt_actor_registry"] = q(
            "MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle) "
            "WHERE q.quelltyp = 'external_link_from_actor_registry' "
            "RETURN count(r) AS c"
        ).single()["c"]
        out["quelle_actor_registry_total"] = q(
            "MATCH (q:Quelle) WHERE q.quelltyp = 'external_link_from_actor_registry' "
            "RETURN count(q) AS c"
        ).single()["c"]
        # edge property pollution — names that contain url/http/source_file
        out["edges_with_url_prop"] = q(
            "MATCH ()-[r]->() WITH r, [k IN keys(r) WHERE toLower(k) CONTAINS 'url'] AS keys_with_url "
            "WHERE size(keys_with_url) > 0 RETURN count(r) AS c"
        ).single()["c"]
        out["edges_with_http_prop"] = q(
            "MATCH ()-[r]->() WITH r, [k IN keys(r) WHERE toLower(k) CONTAINS 'http'] AS keys_with_http "
            "WHERE size(keys_with_http) > 0 RETURN count(r) AS c"
        ).single()["c"]
        out["edges_with_source_file_prop"] = q(
            "MATCH ()-[r]->() WITH r, [k IN keys(r) WHERE toLower(k) CONTAINS 'source_file'] AS keys "
            "WHERE size(keys) > 0 RETURN count(r) AS c"
        ).single()["c"]
        out["edges_with_external_sources_prop"] = q(
            "MATCH ()-[r]->() WITH r, [k IN keys(r) WHERE toLower(k) CONTAINS 'external_sources'] AS keys "
            "WHERE size(keys) > 0 RETURN count(r) AS c"
        ).single()["c"]
        # collect distinct illegal key names for inspection
        out["distinct_illegal_rel_keys"] = sorted({
            r["k"]
            for r in q(
                "MATCH ()-[r]->() UNWIND keys(r) AS k "
                "WITH DISTINCT k WHERE toLower(k) CONTAINS 'url' "
                "  OR toLower(k) CONTAINS 'http' "
                "  OR toLower(k) CONTAINS 'source_file' "
                "  OR toLower(k) CONTAINS 'external_sources' "
                "RETURN k"
            )
        })
        # also: how many BELEGT_IN edges total from Projekt to Quelle (sanity)
        out["projekt_belegt_total"] = q(
            "MATCH (p:Projekt)-[r:BELEGT_IN]->(:Quelle) RETURN count(r) AS c"
        ).single()["c"]
    driver.close()
    print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
