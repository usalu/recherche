"""Read-only post-migration verification probe (Agent 5)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, r"E:/recherche/_scripts")

from neo4j import GraphDatabase  # type: ignore

from neo4j_env import resolve_connection  # type: ignore

OUT = Path(r"E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset/logs/agent5_verify.json")


def main() -> int:
    uri, user, password, _ = resolve_connection()
    drv = GraphDatabase.driver(uri, auth=(user, password))
    out: dict = {}
    with drv.session(database="mit-bestand") as s:
        out["status_nodes"] = [dict(r) for r in s.run(
            "MATCH (n:Status) "
            "OPTIONAL MATCH (n)<-[r:HAT_STATUS]-() "
            "RETURN n.id AS id, n.name AS name, n.kind AS kind, "
            "       n.aliases AS aliases, count(r) AS in_hat_status "
            "ORDER BY in_hat_status DESC"
        )]
        out["wva_facets"] = [dict(r) for r in s.run(
            "MATCH (n:WiederverwendungsArt) "
            "RETURN n.facet AS facet, collect(n.id) AS ids ORDER BY facet"
        )]
        out["akteurrolle_post"] = [dict(r) for r in s.run(
            "MATCH (n:Akteurrolle) WHERE n.id IN "
            "['ar_reuse_beratung','ar_reuse_zirkularitaetsberatung'] "
            "RETURN n.id AS id, n.aliases AS aliases"
        )]
        out["raw_role_evidence_stats"] = dict(s.run(
            "MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL "
            "RETURN count(a) AS akteurs, "
            "       sum(size(a.raw_role_evidence)) AS total_strings, "
            "       min(size(a.raw_role_evidence)) AS min_per_akteur, "
            "       max(size(a.raw_role_evidence)) AS max_per_akteur"
        ).single())
        out["bauteiltyp_brand_layer"] = [dict(r) for r in s.run(
            "MATCH (b:Bauteiltyp) "
            "RETURN b.brand_layer AS layer, collect(b.id) AS bauteiltypen ORDER BY layer"
        )]
        out["projekt_lca_module_scope"] = [dict(r) for r in s.run(
            "MATCH (p:Projekt) WHERE p.lca_module_scope IS NOT NULL "
            "RETURN p.id AS projekt_id, p.lca_module_scope AS modules ORDER BY p.id"
        )]
        out["projekt_certifications"] = [dict(r) for r in s.run(
            "MATCH (p:Projekt) WHERE p.certifications IS NOT NULL "
            "RETURN p.id AS projekt_id, p.certifications AS certifications ORDER BY p.id"
        )]
        out["legal_conditions_by_label"] = [dict(r) for r in s.run(
            "MATCH (n) WHERE n.legal_conditions IS NOT NULL "
            "RETURN labels(n) AS labels, count(n) AS n, "
            "       sum(size(n.legal_conditions)) AS total_entries ORDER BY n DESC"
        )]
        out["software_kind_distribution"] = [dict(r) for r in s.run(
            "MATCH (n:Software) RETURN n.kind AS kind, count(n) AS n ORDER BY n DESC"
        )]
        out["software_label_overlap"] = list(s.run(
            "MATCH (n:Software) RETURN size([l IN labels(n) WHERE l = 'Tool']) AS still_tool, "
            "       count(n) AS total_software"
        ).single().data().items())
        out["edge_counts"] = dict(s.run(
            "RETURN "
            "  count{ ()-[:HAT_STATUS]->() } AS hat_status,"
            "  count{ ()-[:HAT_WIEDERVERWENDUNGSART]->() } AS hat_wva,"
            "  count{ ()-[:BETEILIGT_AN]->() } AS beteiligt_an,"
            "  count{ ()-[:HAT_AKTEURROLLE]->() } AS hat_akteurrolle,"
            "  count{ ()-[:TEILT_LAYER]->() } AS teilt_layer,"
            "  count{ ()-[:BERECHNET_NACH_MODUL]->() } AS berechnet_nach_modul,"
            "  count{ ()-[:METHODENGRUNDLAGE_NORM]->() } AS methodengrundlage_norm,"
            "  count{ ()-[:HAT_RECHTLICHE_BEDINGUNG]->() } AS hat_rb,"
            "  count{ ()-[:HAT_ZERTIFIZIERUNG]->() } AS hat_zert,"
            "  count{ ()-[:NUTZT_TOOL]->() } AS nutzt_tool,"
            "  count{ ()-[:NUTZT_SOFTWARE]->() } AS nutzt_software,"
            "  count{ ()-[:REFERENZIERT_NORM]->() } AS referenziert_norm,"
            "  count{ ()-[r:REFERENZIERT_NORM]->() WHERE r.evidence_basis = 'lca_module_demote' } AS rn_lca_derived"
        ).single())
        out["node_label_counts"] = [dict(r) for r in s.run(
            "MATCH (n) UNWIND labels(n) AS l RETURN l AS label, count(*) AS n "
            "ORDER BY n DESC"
        )]
        out["totals"] = dict(s.run(
            "MATCH (n) WITH count(n) AS nodes "
            "MATCH ()-[r]->() RETURN nodes, count(r) AS rels"
        ).single())
        out["beteiligt_an_rolle_text_remaining"] = s.run(
            "MATCH ()-[r:BETEILIGT_AN]->() WHERE r.rolle_text IS NOT NULL RETURN count(r) AS c"
        ).single()["c"]
        out["bauwerk_legacy_status_props"] = dict(s.run(
            "MATCH (b:Bauwerk) "
            "RETURN sum(CASE WHEN b.bauwerkstatus IS NOT NULL THEN 1 ELSE 0 END) AS bauwerkstatus, "
            "       sum(CASE WHEN b.status_text IS NOT NULL THEN 1 ELSE 0 END) AS status_text"
        ).single())
        out["bg_legacy_counts_props"] = dict(s.run(
            "MATCH (bg:Bauteilgruppe) "
            "RETURN sum(CASE WHEN bg.counts_as_direct_reuse IS NOT NULL THEN 1 ELSE 0 END) AS direct_reuse, "
            "       sum(CASE WHEN bg.counts_as_bestandserhalt IS NOT NULL THEN 1 ELSE 0 END) AS bestandserhalt, "
            "       sum(CASE WHEN bg.counts_as_recycling IS NOT NULL THEN 1 ELSE 0 END) AS recycling, "
            "       sum(CASE WHEN bg.counts_as_remanufacturing IS NOT NULL THEN 1 ELSE 0 END) AS reman, "
            "       sum(CASE WHEN bg.counts_as_surplus IS NOT NULL THEN 1 ELSE 0 END) AS surplus"
        ).single())
    drv.close()
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
