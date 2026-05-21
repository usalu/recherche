"""Repair Agent D — post-migration live verification (read-only)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ENTWERFENMITBESTAND")
DB = "mit-bestand"
RUN_DIR = Path(r"E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset")

sys.stdout.reconfigure(encoding="utf-8")
driver = GraphDatabase.driver(URI, auth=AUTH)


def qval(cypher: str):
    with driver.session(database=DB, default_access_mode="READ") as s:
        rec = s.run(cypher).single()
        return next(iter(rec.values())) if rec else None


out = {
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "database": DB,
    "checks": {},
}

out["checks"]["curated_no_excerpt"] = {
    "count": qval(
        """
        MATCH ()-[r]->()
        WHERE r.evidence_origin='curated'
          AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
        RETURN count(r) AS c
        """
    ),
    "expected": 0,
    "pass": True,
}

out["checks"]["origin_enum_violations"] = {
    "count": qval(
        """
        MATCH ()-[r]->()
        WHERE r.evidence_origin IS NOT NULL
          AND NOT r.evidence_origin IN ['curated','inferred','derived']
        RETURN count(r) AS c
        """
    ),
    "expected": 0,
    "pass": True,
}

out["checks"]["confidence_enum_violations"] = {
    "count": qval(
        """
        MATCH ()-[r]->()
        WHERE r.evidence_confidence IS NOT NULL
          AND NOT r.evidence_confidence IN ['belegt','teilweise_belegt','unklar','inferiert','bookkeeping']
        RETURN count(r) AS c
        """
    ),
    "expected": 0,
    "pass": True,
}

out["checks"]["citation_basis_enum_violations"] = {
    "count": qval(
        """
        MATCH ()-[r]->()
        WHERE type(r) IN [
          'BELEGT_IN','BETEILIGT_AN','ASSOZIIERT_MIT_PROJEKT',
          'AUS_BAUWERK','FROM_DONOR','EINGEBAUT_IN','INTO_RECEIVER',
          'HAT_BAUTEILGRUPPE','HAT_HUERDE','HAT_AKTEURROLLE'
        ]
        AND NOT r.evidence_basis IN ['cell_citation','registry_stub','propagated','controlled_vocab']
        RETURN count(r) AS c
        """
    ),
    "expected": 0,
    "pass": True,
}

out["checks"]["q1_canonical"] = {
    "rows": qval(
        """
        MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),
              (bg)<-[r:HAT_BAUTEILGRUPPE]-(p:Projekt)
        WHERE r.evidence_origin='curated'
        RETURN count(*) AS c
        """
    ),
    "expected_min": 1,
    "pass": True,
}

out["checks"]["hat_bg_curated"] = {
    "count": qval(
        "MATCH ()-[r:HAT_BAUTEILGRUPPE]->() WHERE r.evidence_origin='curated' RETURN count(r) AS c"
    ),
    "expected_min": 1,
    "pass": True,
}

out["checks"]["invariants_4c"] = {
    "quelle_external_sources": qval("MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) AS c"),
    "rel_url_props": qval(
        """
        MATCH ()-[r]->()
        WITH r, [k IN keys(r) WHERE k IN ['url','http','source_file','external_sources']] AS bad
        WHERE size(bad) > 0 RETURN count(r) AS c
        """
    ),
    "projekt_belegt_actor_url": qval(
        """
        MATCH (:Projekt)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
        RETURN count(r) AS c
        """
    ),
    "zitiert_quelle_total": qval("MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS c"),
    "pass": True,
}

# Set pass flags from actual counts
for key in ("curated_no_excerpt", "origin_enum_violations", "confidence_enum_violations", "citation_basis_enum_violations"):
    out["checks"][key]["pass"] = out["checks"][key]["count"] == 0

out["checks"]["q1_canonical"]["pass"] = (out["checks"]["q1_canonical"]["rows"] or 0) >= 1
out["checks"]["hat_bg_curated"]["pass"] = (out["checks"]["hat_bg_curated"]["count"] or 0) >= 1
inv = out["checks"]["invariants_4c"]
inv["pass"] = (
    inv["quelle_external_sources"] == 0
    and inv["rel_url_props"] == 0
    and inv["projekt_belegt_actor_url"] == 0
    and (inv["zitiert_quelle_total"] or 0) >= 1470
)

out["overall_pass"] = all(c.get("pass") for c in out["checks"].values())

# fill actual values
out["checks"]["curated_no_excerpt"]["count"] = qval(
    "MATCH ()-[r]->() WHERE r.evidence_origin='curated' AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='') RETURN count(r) AS c"
)
out["checks"]["curated_no_excerpt"]["pass"] = out["checks"]["curated_no_excerpt"]["count"] == 0
out["checks"]["origin_enum_violations"]["count"] = qval(
    "MATCH ()-[r]->() WHERE r.evidence_origin IS NOT NULL AND NOT r.evidence_origin IN ['curated','inferred','derived'] RETURN count(r) AS c"
)
out["checks"]["origin_enum_violations"]["pass"] = out["checks"]["origin_enum_violations"]["count"] == 0
out["checks"]["confidence_enum_violations"]["count"] = qval(
    "MATCH ()-[r]->() WHERE r.evidence_confidence IS NOT NULL AND NOT r.evidence_confidence IN ['belegt','teilweise_belegt','unklar','inferiert','bookkeeping'] RETURN count(r) AS c"
)
out["checks"]["confidence_enum_violations"]["pass"] = out["checks"]["confidence_enum_violations"]["count"] == 0
out["checks"]["citation_basis_enum_violations"]["count"] = qval(
    """
    MATCH ()-[r]->()
    WHERE type(r) IN ['BELEGT_IN','BETEILIGT_AN','ASSOZIIERT_MIT_PROJEKT','AUS_BAUWERK','FROM_DONOR','EINGEBAUT_IN','INTO_RECEIVER','HAT_BAUTEILGRUPPE','HAT_HUERDE','HAT_AKTEURROLLE']
    AND NOT r.evidence_basis IN ['cell_citation','registry_stub','propagated','controlled_vocab']
    RETURN count(r) AS c
    """
)
out["checks"]["citation_basis_enum_violations"]["pass"] = out["checks"]["citation_basis_enum_violations"]["count"] == 0
out["checks"]["q1_canonical"]["rows"] = qval(
    """
    MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),
          (bg)<-[r:HAT_BAUTEILGRUPPE]-(p:Projekt)
    WHERE r.evidence_origin='curated'
    RETURN count(*) AS c
    """
)
out["checks"]["q1_canonical"]["pass"] = (out["checks"]["q1_canonical"]["rows"] or 0) >= 1
out["checks"]["hat_bg_curated"]["count"] = qval(
    "MATCH ()-[r:HAT_BAUTEILGRUPPE]->() WHERE r.evidence_origin='curated' RETURN count(r) AS c"
)
out["checks"]["hat_bg_curated"]["pass"] = (out["checks"]["hat_bg_curated"]["count"] or 0) >= 1
inv = out["checks"]["invariants_4c"]
inv["quelle_external_sources"] = qval("MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) AS c")
inv["rel_url_props"] = qval(
    "MATCH ()-[r]->() WITH r, [k IN keys(r) WHERE k IN ['url','http','source_file','external_sources']] AS bad WHERE size(bad)>0 RETURN count(r) AS c"
)
inv["projekt_belegt_actor_url"] = qval(
    "MATCH (:Projekt)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'}) RETURN count(r) AS c"
)
inv["zitiert_quelle_total"] = qval("MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS c")
inv["pass"] = inv["quelle_external_sources"] == 0 and inv["rel_url_props"] == 0 and inv["projekt_belegt_actor_url"] == 0 and (inv["zitiert_quelle_total"] or 0) >= 1470
out["overall_pass"] = all(c.get("pass") for c in out["checks"].values())

print(json.dumps(out, indent=2, ensure_ascii=False))
(RUN_DIR / "logs/repair_d_verify.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
driver.close()
