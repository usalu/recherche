"""Agent 12 probe 2 — verify additional acceptance state."""
from __future__ import annotations
import json, sys, traceback
from pathlib import Path
REPO_ROOT = Path(r"E:/recherche")
OUT = REPO_ROOT / "_neo4j/intake/runs/2026-05-20_radical_quality_reset/logs/agent12_probe2.json"


def main():
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection
    from neo4j import GraphDatabase
    uri, user, pw, db = resolve_connection()
    db = "mit-bestand"
    out = {}
    try:
        drv = GraphDatabase.driver(uri, auth=(user, pw))
        with drv.session(database=db) as s:
            def one(q, **p):
                r = s.run(q, **p).single()
                return r.value() if r else None
            def rows(q, **p):
                return [dict(r) for r in s.run(q, **p)]
            out["from_donor_total"] = one("MATCH ()-[r:FROM_DONOR]->() RETURN count(r)")
            out["into_receiver_total"] = one("MATCH ()-[r:INTO_RECEIVER]->() RETURN count(r)")
            out["hat_bg_curated"] = one(
                "MATCH ()-[r:HAT_BAUTEILGRUPPE]->() WHERE r.evidence_origin='curated' RETURN count(r)"
            )
            out["hat_bg_total"] = one("MATCH ()-[r:HAT_BAUTEILGRUPPE]->() RETURN count(r)")
            out["bg_with_donor_or_receiver"] = one(
                "MATCH (b:Bauteilgruppe) WHERE exists{(b)-[:FROM_DONOR]->()} OR exists{(b)-[:INTO_RECEIVER]->()} RETURN count(b)"
            )
            out["bg_with_donor_and_receiver"] = one(
                "MATCH (b:Bauteilgruppe) WHERE exists{(b)-[:FROM_DONOR]->()} AND exists{(b)-[:INTO_RECEIVER]->()} RETURN count(b)"
            )
            out["sample_hat_bg_curated"] = rows(
                "MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(b:Bauteilgruppe) "
                "WHERE r.evidence_origin='curated' "
                "RETURN p.id AS pid, b.id AS bid, r.evidence_excerpt AS excerpt LIMIT 5"
            )
            out["q1_alt_rows"] = rows(
                "MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) "
                "WHERE r.evidence_origin='curated' "
                "RETURN p.id AS pid, bg.id AS bid LIMIT 10"
            )
            # Tier 1 cohort
            out["tier1_projects"] = rows(
                "MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'}) "
                "RETURN p.id AS id, p.name AS name, p.year_completed AS yc, "
                "p.quality_tier_n_bg AS n_bg, p.quality_tier_n_bg_quantified AS n_bg_q, "
                "p.quality_tier_n_curated_evidence AS n_ev "
                "ORDER BY n_ev DESC"
            )
            # Schadstoff count
            out["has_risk_pollutant_total"] = one("MATCH ()-[r:HAS_RISK_POLLUTANT]->() RETURN count(r)")
            out["requires_verification_for_total"] = one("MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->() RETURN count(r)")
            out["reuse_rule_total"] = one("MATCH (r:ReuseRule) RETURN count(r)")
            # Phase 1 deletion bookkeeping
            out["wiederverwendungskette_total"] = one("MATCH (w:Wiederverwendungskette) RETURN count(w)")
            out["materialdepot_total"] = one("MATCH (m:Materialdepot) RETURN count(m)")
            out["ontology_anchor_total"] = one("MATCH (o:OntologyAnchor) RETURN count(o)")
            out["anchored_by_total"] = one("MATCH ()-[r:ANCHORED_BY]->() RETURN count(r)")
            # Phase 2 schema
            out["status_total"] = one("MATCH (s:Status) RETURN count(s)")
            out["layer_total"] = one("MATCH (l:Layer) RETURN count(l)")
            out["lebenszyklusmodul_total"] = one("MATCH (l:LebenszyklusModul) RETURN count(l)")
            out["rechtlichebedingung_total"] = one("MATCH (l:RechtlicheBedingung) RETURN count(l)")
            out["zertifizierungbewertungssystem_total"] = one("MATCH (l:ZertifizierungBewertungssystem) RETURN count(l)")
            out["tool_total"] = one("MATCH (t:Tool) RETURN count(t)")
            out["software_total"] = one("MATCH (s:Software) RETURN count(s)")
            out["norm_total"] = one("MATCH (n:Norm) RETURN count(n)")
            out["quelle_total"] = one("MATCH (q:Quelle) RETURN count(q)")
            # Phase 4 evidence shape
            out["curated_excerpt_share"] = rows(
                "MATCH ()-[r]->() WHERE r.evidence_origin IS NOT NULL "
                "RETURN r.evidence_origin AS origin, count(r) AS c ORDER BY c DESC"
            )
            out["edges_with_external_sources_property"] = one(
                "MATCH ()-[r]->() WHERE r.external_sources IS NOT NULL RETURN count(r)"
            )
            # Akteur counts
            out["akteur_total"] = one("MATCH (a:Akteur) RETURN count(a)")
            out["programm_total"] = one("MATCH (p:Programm) RETURN count(p)")
            out["projekt_total"] = one("MATCH (p:Projekt) RETURN count(p)")
            out["bauteilgruppe_total"] = one("MATCH (b:Bauteilgruppe) RETURN count(b)")
            out["bauwerk_total"] = one("MATCH (b:Bauwerk) RETURN count(b)")
            # Rule B audit for new labels
            out["reuse_rule_min_deg"] = one(
                "MATCH (r:ReuseRule) WITH r, size([(r)--() | 1]) AS d RETURN min(d)"
            )
            out["materialdepot_min_deg"] = one(
                "MATCH (m:Materialdepot) WITH m, size([(m)--() | 1]) AS d RETURN min(d)"
            )
            out["ontology_anchor_min_deg"] = one(
                "MATCH (o:OntologyAnchor) WITH o, size([(o)--() | 1]) AS d RETURN min(d)"
            )
            # External sources unfold check
            out["edges_with_url_property"] = one(
                "MATCH ()-[r]->() WHERE r.url IS NOT NULL RETURN count(r)"
            )
            # Has dominant marktmodell / akzeptanz
            out["has_dominant_marktmodell_total"] = one(
                "MATCH ()-[r:HAT_DOMINANT_MARKTMODELL]->() RETURN count(r)"
            )
            out["has_dominant_akzeptanz_total"] = one(
                "MATCH ()-[r:HAT_DOMINANT_AKZEPTANZ]->() RETURN count(r)"
            )
            out["hat_schadstoff_total"] = one(
                "MATCH ()-[r:HAT_SCHADSTOFF]->() RETURN count(r)"
            )
            out["built_in_era_total"] = one(
                "MATCH ()-[r:BUILT_IN_ERA]->() RETURN count(r)"
            )
            out["applies_in_total"] = one(
                "MATCH (:ReuseRule)-[r:APPLIES_IN]->() RETURN count(r)"
            )
            out["applies_to_total"] = one(
                "MATCH (:ReuseRule)-[r:APPLIES_TO]->() RETURN count(r)"
            )
            out["referenziert_norm_from_rule"] = one(
                "MATCH (:ReuseRule)-[r:REFERENZIERT_NORM]->() RETURN count(r)"
            )
            out["beteiligt_an_total"] = one("MATCH ()-[r:BETEILIGT_AN]->() RETURN count(r)")
            out["liegt_in_land_total"] = one("MATCH ()-[r:LIEGT_IN_LAND]->() RETURN count(r)")
            # Top tier_1 projects with curated evidence and BG quantified
            out["tier1_actor_distinct_count"] = one(
                "MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt {quality_tier:'tier_1_decision_grade'}) "
                "RETURN count(DISTINCT a)"
            )
            out["any_actor_to_tier1_count"] = one(
                "MATCH (a:Akteur)-[r]->(p:Projekt {quality_tier:'tier_1_decision_grade'}) "
                "RETURN count(DISTINCT a)"
            )
            out["beteiligt_an_to_tier1_total"] = one(
                "MATCH (:Akteur)-[r:BETEILIGT_AN]->(:Projekt {quality_tier:'tier_1_decision_grade'}) "
                "RETURN count(r)"
            )
            # tier_3 IDs
            out["tier3_ids"] = rows(
                "MATCH (p:Projekt {quality_tier:'tier_3_stub'}) "
                "RETURN p.id AS id, p.name AS name, "
                "p.quality_tier_n_bg AS n_bg, p.quality_tier_has_year AS has_year, "
                "p.quality_tier_has_land AS has_land, "
                "p.quality_tier_has_metric AS has_metric, "
                "p.quality_tier_has_evidence AS has_evidence "
                "ORDER BY id"
            )
        drv.close()
        out["status"] = "ok"
    except Exception:
        out["status"] = "error"
        out["error"] = traceback.format_exc()
    finally:
        OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        print("wrote", OUT)


if __name__ == "__main__":
    main()
