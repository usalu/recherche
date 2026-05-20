"""Read-only probe for Agent 5 (Phases 2.1, 2.2, 2.3, 2.5).

Captures live node lists, edge counts, and property-key inventories needed
to design the migrations precisely against the actual database.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, r"E:/recherche/_scripts")

from neo4j import GraphDatabase  # type: ignore

from neo4j_env import resolve_connection  # type: ignore

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-20_radical_quality_reset"
OUT = RUN_ROOT / "logs" / "agent5_probe.json"


def main() -> int:
    uri, user, password, _ = resolve_connection()
    drv = GraphDatabase.driver(uri, auth=(user, password))
    out: dict = {}
    with drv.session(database="mit-bestand") as s:
        out["status_nodes"] = [
            dict(r) for r in s.run(
                "MATCH (n:Status) "
                "OPTIONAL MATCH (n)<-[r:HAT_STATUS]-() "
                "RETURN n.id AS id, n.name AS name, n.kind AS kind, "
                "       count(r) AS in_hat_status, properties(n) AS props "
                "ORDER BY in_hat_status DESC"
            )
        ]
        out["wva_nodes"] = [
            dict(r) for r in s.run(
                "MATCH (n:WiederverwendungsArt) "
                "OPTIONAL MATCH (n)<-[r:HAT_WIEDERVERWENDUNGSART]-() "
                "RETURN n.id AS id, n.name AS name, n.facet AS facet, "
                "       count(r) AS in_hwa, properties(n) AS props "
                "ORDER BY in_hwa DESC"
            )
        ]
        out["bauwerk_status_prop_counts"] = dict(s.run(
            "MATCH (b:Bauwerk) "
            "RETURN sum(CASE WHEN b.bauwerkstatus IS NOT NULL THEN 1 ELSE 0 END) AS bauwerkstatus_prop, "
            "       sum(CASE WHEN b.status_text IS NOT NULL THEN 1 ELSE 0 END) AS status_text_prop, "
            "       count(b) AS bauwerk_total"
        ).single())
        out["bg_counts_prop_counts"] = dict(s.run(
            "MATCH (bg:Bauteilgruppe) "
            "RETURN sum(CASE WHEN bg.counts_as_direct_reuse IS NOT NULL THEN 1 ELSE 0 END) AS direct_reuse, "
            "       sum(CASE WHEN bg.counts_as_bestandserhalt IS NOT NULL THEN 1 ELSE 0 END) AS bestandserhalt, "
            "       sum(CASE WHEN bg.counts_as_recycling IS NOT NULL THEN 1 ELSE 0 END) AS recycling, "
            "       sum(CASE WHEN bg.counts_as_remanufacturing IS NOT NULL THEN 1 ELSE 0 END) AS reman, "
            "       sum(CASE WHEN bg.counts_as_surplus IS NOT NULL THEN 1 ELSE 0 END) AS surplus, "
            "       count(bg) AS bg_total"
        ).single())
        out["akteurrolle_target"] = [
            dict(r) for r in s.run(
                "MATCH (n:Akteurrolle) WHERE n.id IN "
                "['ar_reuse_beratung','ar_reuse_zirkularitaetsberatung'] "
                "OPTIONAL MATCH (n)<-[r:HAT_AKTEURROLLE]-() "
                "RETURN n.id AS id, n.name AS name, count(r) AS deg_in, properties(n) AS props"
            )
        ]
        out["beteiligt_an_rolle_text_count"] = s.run(
            "MATCH ()-[r:BETEILIGT_AN]->() "
            "WHERE r.rolle_text IS NOT NULL "
            "RETURN count(r) AS n"
        ).single()["n"]
        out["beteiligt_an_rolle_text_sample"] = [
            dict(r) for r in s.run(
                "MATCH (a:Akteur)-[r:BETEILIGT_AN]->(t) "
                "WHERE r.rolle_text IS NOT NULL "
                "RETURN a.id AS akteur_id, type(r) AS rtype, "
                "       coalesce(t.id, t.name) AS target_id, "
                "       r.rolle_text AS rolle_text "
                "LIMIT 12"
            )
        ]
        out["beteiligt_an_subject_label_dist"] = [
            dict(r) for r in s.run(
                "MATCH (a)-[r:BETEILIGT_AN]->() "
                "WHERE r.rolle_text IS NOT NULL "
                "RETURN labels(a) AS labels, count(*) AS n "
                "ORDER BY n DESC"
            )
        ]
        out["layer_nodes"] = [
            dict(r) for r in s.run(
                "MATCH (n:Layer) "
                "OPTIONAL MATCH (b:Bauteiltyp)-[r:TEILT_LAYER]->(n) "
                "RETURN n.id AS id, n.name AS name, "
                "       collect({bauteiltyp_id: b.id, bauteiltyp_name: b.name}) AS bauteiltypen, "
                "       properties(n) AS props"
            )
        ]
        out["layer_edges_full"] = [
            dict(r) for r in s.run(
                "MATCH (b:Bauteiltyp)-[r:TEILT_LAYER]->(l:Layer) "
                "RETURN b.id AS bt_id, b.name AS bt_name, l.id AS layer_id, "
                "       l.name AS layer_name, properties(r) AS edge_props"
            )
        ]
        out["lzm_nodes"] = [
            dict(r) for r in s.run(
                "MATCH (n:LebenszyklusModul) "
                "OPTIONAL MATCH (p:Projekt)-[bm:BERECHNET_NACH_MODUL]->(n) "
                "OPTIONAL MATCH (n)-[mn:METHODENGRUNDLAGE_NORM]->(norm:Norm) "
                "RETURN n.id AS id, n.name AS name, "
                "       collect(DISTINCT {projekt_id: p.id, edge: properties(bm)}) AS projekte, "
                "       collect(DISTINCT {norm_id: norm.id, norm_name: norm.name, edge: properties(mn)}) AS norms, "
                "       properties(n) AS props"
            )
        ]
        out["rb_nodes"] = [
            dict(r) for r in s.run(
                "MATCH (n:RechtlicheBedingung) "
                "OPTIONAL MATCH (src)-[hr:HAT_RECHTLICHE_BEDINGUNG]->(n) "
                "OPTIONAL MATCH (n)-[gl:GILT_IN_LAND]->(land:Land) "
                "RETURN n.id AS id, n.name AS name, "
                "       collect(DISTINCT {src_id: src.id, src_labels: labels(src), edge: properties(hr)}) AS sources, "
                "       collect(DISTINCT {land_id: land.id, land_name: land.name, edge: properties(gl)}) AS countries, "
                "       properties(n) AS props"
            )
        ]
        out["zert_nodes"] = [
            dict(r) for r in s.run(
                "MATCH (n:ZertifizierungBewertungssystem) "
                "OPTIONAL MATCH (p:Projekt)-[hz:HAT_ZERTIFIZIERUNG]->(n) "
                "RETURN n.id AS id, n.name AS name, "
                "       collect(DISTINCT {projekt_id: p.id, edge: properties(hz)}) AS projekte, "
                "       properties(n) AS props"
            )
        ]
        out["tool_nodes"] = [
            dict(r) for r in s.run(
                "MATCH (n:Tool) "
                "RETURN n.id AS id, n.name AS name, labels(n) AS labels, properties(n) AS props"
            )
        ]
        out["tool_edges_in"] = [
            dict(r) for r in s.run(
                "MATCH (src)-[r:NUTZT_TOOL]->(t:Tool) "
                "RETURN labels(src) AS src_labels, src.id AS src_id, type(r) AS rtype, "
                "       t.id AS tool_id, t.name AS tool_name, properties(r) AS edge_props "
                "ORDER BY src.id, t.id"
            )
        ]
        out["tool_edges_out"] = [
            dict(r) for r in s.run(
                "MATCH (t:Tool)-[r]->(other) "
                "RETURN t.id AS tool_id, t.name AS tool_name, type(r) AS rtype, "
                "       labels(other) AS other_labels, coalesce(other.id, other.name) AS other_ref, "
                "       properties(r) AS edge_props "
                "ORDER BY t.id, type(r)"
            )
        ]
        out["software_nodes_count"] = s.run(
            "MATCH (n:Software) RETURN count(n) AS n, "
            "sum(CASE WHEN n.kind IS NOT NULL THEN 1 ELSE 0 END) AS with_kind"
        ).single().data()
        out["bauteiltyp_brand_layer_pre"] = s.run(
            "MATCH (b:Bauteiltyp) "
            "RETURN sum(CASE WHEN b.brand_layer IS NOT NULL THEN 1 ELSE 0 END) AS already_set, "
            "       count(b) AS total"
        ).single().data()
        out["projekt_year_completed_count"] = s.run(
            "MATCH (p:Projekt) WHERE p.lca_module_scope IS NOT NULL RETURN count(p) AS n"
        ).single()["n"]
        out["projekt_certifications_count"] = s.run(
            "MATCH (p:Projekt) WHERE p.certifications IS NOT NULL RETURN count(p) AS n"
        ).single()["n"]
        out["raw_role_evidence_count"] = s.run(
            "MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL RETURN count(a) AS n"
        ).single()["n"]
        out["nutzt_tool_count"] = s.run(
            "MATCH ()-[r:NUTZT_TOOL]->() RETURN count(r) AS n"
        ).single()["n"]
        out["nutzt_software_count"] = s.run(
            "MATCH ()-[r:NUTZT_SOFTWARE]->() RETURN count(r) AS n"
        ).single()["n"]
        out["apoc_available"] = s.run(
            "RETURN apoc.version() AS v"
        ).single()["v"]
    drv.close()
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
