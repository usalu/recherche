"""Repair Agent D — probe live state of curated-without-excerpt and HAT_BAUTEILGRUPPE.

Read-only. Writes JSON to logs/repair_d_probe.json.
"""
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

# Totals
out["total_curated"] = q(
    "MATCH ()-[r]->() WHERE r.evidence_origin='curated' RETURN count(r) AS c"
)[0]["c"]
out["curated_no_excerpt"] = q(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt = '')
    RETURN count(r) AS c
    """
)[0]["c"]
out["curated_with_excerpt"] = q(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_origin='curated'
      AND r.evidence_excerpt IS NOT NULL AND r.evidence_excerpt <> ''
    RETURN count(r) AS c
    """
)[0]["c"]

# Breakdown by (type, evidence_basis, evidence_source_id)
out["curated_no_excerpt_breakdown"] = q(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt = '')
    WITH type(r) AS t, r.evidence_basis AS basis,
         CASE WHEN r.evidence_source_id STARTS WITH 'q_actor_' THEN 'q_actor_*' ELSE r.evidence_source_id END AS src,
         count(*) AS c
    RETURN t, basis, src, c ORDER BY c DESC, t, src
    """
)

# Sample edges per major category
samples = {}
for cat_name, type_filter, src_filter in [
    ("belegt_in_master", "BELEGT_IN", "q_akteursliste_master_md"),
    ("belegt_in_actor_sref", "BELEGT_IN", "q_actor_*"),
    ("hat_akteurrolle_master", "HAT_AKTEURROLLE", "q_akteursliste_master_md"),
    ("verbunden_mit_akteur_master", "VERBUNDEN_MIT_AKTEUR", "q_akteursliste_master_md"),
    ("liegt_in_land_master", "LIEGT_IN_LAND", "q_akteursliste_master_md"),
    ("hat_akteurtyp_master", "HAT_AKTEURTYP", "q_akteursliste_master_md"),
    ("assoziiert_mit_projekt_master", "ASSOZIIERT_MIT_PROJEKT", "q_akteursliste_master_md"),
    ("built_in_era_year_inferred", "BUILT_IN_ERA", None),
    ("requires_verification_for_rollup", "REQUIRES_VERIFICATION_FOR", None),
]:
    if src_filter == "q_actor_*":
        rows = q(
            f"""
            MATCH (a)-[r:{type_filter}]->(b)
            WHERE r.evidence_origin='curated'
              AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
              AND r.evidence_source_id STARTS WITH 'q_actor_'
            RETURN labels(a) AS a_labels, a.id AS a_id,
                   labels(b) AS b_labels, b.id AS b_id, b.url AS b_url, b.titel AS b_titel,
                   properties(r) AS r_props
            LIMIT 5
            """
        )
    elif src_filter:
        rows = q(
            f"""
            MATCH (a)-[r:{type_filter}]->(b)
            WHERE r.evidence_origin='curated'
              AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
              AND r.evidence_source_id='{src_filter}'
            RETURN labels(a) AS a_labels, a.id AS a_id,
                   labels(b) AS b_labels, b.id AS b_id,
                   properties(r) AS r_props
            LIMIT 5
            """
        )
    else:
        rows = q(
            f"""
            MATCH (a)-[r:{type_filter}]->(b)
            WHERE r.evidence_origin='curated'
              AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
            RETURN labels(a) AS a_labels, a.id AS a_id,
                   labels(b) AS b_labels, b.id AS b_id,
                   a.baujahr AS a_baujahr, b.start_year AS b_start_year, b.end_year AS b_end_year,
                   properties(r) AS r_props
            LIMIT 5
            """
        )
    samples[cat_name] = rows
out["samples"] = samples

# HAT_BAUTEILGRUPPE current state
out["hat_bg_total"] = q(
    "MATCH ()-[r:HAT_BAUTEILGRUPPE]->() RETURN count(r) AS c"
)[0]["c"]
out["hat_bg_curated"] = q(
    """
    MATCH ()-[r:HAT_BAUTEILGRUPPE]->()
    WHERE r.evidence_origin='curated'
    RETURN count(r) AS c
    """
)[0]["c"]
out["hat_bg_origin_breakdown"] = q(
    """
    MATCH ()-[r:HAT_BAUTEILGRUPPE]->()
    RETURN r.evidence_origin AS origin, r.evidence_basis AS basis,
           r.evidence_confidence AS conf, count(*) AS c
    ORDER BY c DESC
    """
)

# How many BG have both FROM_DONOR and INTO_RECEIVER (dossier-backed topology)?
out["bg_with_donor_and_receiver"] = q(
    """
    MATCH (bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()}
    RETURN count(bg) AS c
    """
)[0]["c"]

# How many (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg) pairs where bg has both donor + receiver?
out["hat_bg_with_dossier_topology"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()}
    RETURN count(r) AS c
    """
)[0]["c"]

# How many such Projekt have any BELEGT_IN -> Quelle with evidence_origin='curated' (dossier evidence)?
out["projekt_with_curated_belegt_in"] = q(
    """
    MATCH (p:Projekt)
    WHERE exists{ (p)-[bel:BELEGT_IN]->(:Quelle) WHERE bel.evidence_origin='curated' }
    RETURN count(p) AS c
    """
)[0]["c"]

# Projekt - HAT_BAUTEILGRUPPE - BG where BG has donor+receiver AND Projekt has curated dossier evidence
out["promotable_hat_bg_count"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE (exists{(bg)-[:FROM_DONOR]->()} OR exists{(bg)-[:INTO_RECEIVER]->()})
      AND exists{ (p)-[bel:BELEGT_IN]->(:Quelle) WHERE bel.evidence_origin='curated' }
    RETURN count(r) AS c
    """
)[0]["c"]

# Sample existing HAT_BAUTEILGRUPPE props
out["hat_bg_sample"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()}
    RETURN p.id AS p_id, bg.id AS bg_id, properties(r) AS r_props
    LIMIT 5
    """
)

# BUILT_IN_ERA details
out["built_in_era_details"] = q(
    """
    MATCH (b:Bauwerk)-[r:BUILT_IN_ERA]->(era)
    WHERE r.evidence_origin='curated'
    RETURN b.id AS b_id, b.baujahr AS baujahr, era.id AS era_id,
           era.start_year AS start_year, era.end_year AS end_year,
           properties(r) AS r_props
    """
)

# REQUIRES_VERIFICATION_FOR project_rollup
out["requires_verification_rollup_details"] = q(
    """
    MATCH (a)-[r:REQUIRES_VERIFICATION_FOR]->(p)
    WHERE r.evidence_origin='curated' AND r.evidence_basis='project_rollup'
    RETURN labels(a) AS a_labels, a.id AS a_id,
           labels(p) AS p_labels, p.id AS p_id,
           properties(r) AS r_props
    """
)

# Actor S-ref BELEGT_IN: check the destination Quelle and Akteur details (registry-citation form)
out["actor_sref_destinations"] = q(
    """
    MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id STARTS WITH 'q_actor_'
    RETURN a.id AS a_id, q.id AS q_id, q.url AS q_url, q.titel AS q_titel, q.quelltyp AS quelltyp,
           r.evidence_source_id AS src
    LIMIT 10
    """
)

# Akteursliste master destination Quelle for BELEGT_IN
out["master_belegt_in_destinations"] = q(
    """
    MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN a.id AS a_id, a.name AS a_name, q.id AS q_id, q.url AS q_url, q.titel AS q_titel,
           q.quelltyp AS quelltyp
    LIMIT 5
    """
)

# Akteursliste master HAT_AKTEURROLLE samples (controlled_vocab)
out["master_hat_akteurrolle_destinations"] = q(
    """
    MATCH (a:Akteur)-[r:HAT_AKTEURROLLE]->(role)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN a.id AS a_id, a.name AS a_name, labels(role) AS r_labels, role.id AS role_id, role.name AS role_name
    LIMIT 5
    """
)

# VERBUNDEN_MIT_AKTEUR samples
out["master_verbunden_destinations"] = q(
    """
    MATCH (a:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN a.id AS a_id, a.name AS a_name, b.id AS b_id, b.name AS b_name, properties(r) AS r_props
    LIMIT 5
    """
)

# LIEGT_IN_LAND samples
out["master_liegt_in_land_destinations"] = q(
    """
    MATCH (a:Akteur)-[r:LIEGT_IN_LAND]->(land)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN a.id AS a_id, a.name AS a_name, labels(land) AS land_labels, land.id AS land_id, land.code AS land_code, land.name AS land_name
    LIMIT 5
    """
)

# HAT_AKTEURTYP samples
out["master_hat_akteurtyp_destinations"] = q(
    """
    MATCH (a:Akteur)-[r:HAT_AKTEURTYP]->(typ)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN a.id AS a_id, a.name AS a_name, labels(typ) AS typ_labels, typ.id AS typ_id, typ.name AS typ_name
    LIMIT 5
    """
)

# ASSOZIIERT_MIT_PROJEKT samples
out["master_assoz_destinations"] = q(
    """
    MATCH (a:Akteur)-[r:ASSOZIIERT_MIT_PROJEKT]->(p:Projekt)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN a.id AS a_id, a.name AS a_name, p.id AS p_id, p.name AS p_name, properties(r) AS r_props
    LIMIT 5
    """
)

# Check if any HAT_AKTEURROLLE master edges actually have excerpts (mixed loader pass)
out["master_hat_akteurrolle_with_excerpt"] = q(
    """
    MATCH (a:Akteur)-[r:HAT_AKTEURROLLE]->(role)
    WHERE r.evidence_origin='curated'
      AND r.evidence_excerpt IS NOT NULL AND r.evidence_excerpt <> ''
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN count(r) AS c
    """
)[0]["c"]

# Total enum compliance now
out["enum_violations_origin"] = q(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_origin IS NOT NULL AND NOT r.evidence_origin IN ['curated','inferred','derived']
    RETURN count(r) AS c
    """
)[0]["c"]
out["enum_violations_confidence"] = q(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_confidence IS NOT NULL
      AND NOT r.evidence_confidence IN ['belegt','teilweise_belegt','unklar','inferiert','bookkeeping']
    RETURN count(r) AS c
    """
)[0]["c"]

# 4c invariants
out["invariants_4c"] = {
    "quelle_with_external_sources": q(
        "MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) AS c"
    )[0]["c"],
    "rels_with_url_or_source_file": q(
        """
        MATCH ()-[r]->()
        WITH r, [k IN keys(r) WHERE k IN ['url','http','source_file','external_sources']] AS bad
        WHERE size(bad) > 0
        RETURN count(r) AS c
        """
    )[0]["c"],
    "projekt_belegt_actor_url": q(
        """
        MATCH (:Projekt)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
        RETURN count(r) AS c
        """
    )[0]["c"],
    "akteur_belegt_actor_url": q(
        """
        MATCH (:Akteur)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
        RETURN count(r) AS c
        """
    )[0]["c"],
    "zitiert_quelle_total": q("MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS c")[0]["c"],
}

# Q1 canonical now (before repair)
out["q1_canonical_before"] = q(
    """
    MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),
          (bg)<-[r:HAT_BAUTEILGRUPPE]-(p:Projekt)
    WHERE r.evidence_origin='curated'
    RETURN count(*) AS c
    """
)[0]["c"]


print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
(Path(RUN_DIR) / "logs/repair_d_probe.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
)

driver.close()
