"""Agent 11 — pre-Phase 3 probe.

Inspect what the graph currently has w.r.t. Phase 3 (eras, schadstoff,
reuse rules). Pure read.

Output: agent11_probe.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "runs"
    / "2026-05-20_radical_quality_reset"
)
OUT = RUN_ROOT / "logs" / "agent11_probe.json"


def _resolve() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, pw, db = resolve_connection()
    if db != "mit-bestand":
        db = "mit-bestand"
    return uri, user, pw, db


def main() -> int:
    from neo4j import GraphDatabase  # type: ignore

    uri, user, pw, db = _resolve()
    drv = GraphDatabase.driver(uri, auth=(user, pw))
    out: dict = {}
    try:
        with drv.session(database=db) as s:
            # ---- general counts
            out["total_nodes"] = s.run("MATCH (n) RETURN count(n) AS c").single()["c"]
            out["total_rels"] = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]

            # ---- Bauwerk / BauwerkEra
            out["bauwerk_total"] = s.run(
                "MATCH (b:Bauwerk) RETURN count(b) AS c"
            ).single()["c"]
            out["bauwerk_era_total"] = s.run(
                "MATCH (e:BauwerkEra) RETURN count(e) AS c"
            ).single()["c"]
            out["bauwerk_era_nodes"] = [
                dict(r["e"]) for r in s.run("MATCH (e:BauwerkEra) RETURN e ORDER BY e.id")
            ]
            out["built_in_era_total"] = s.run(
                "MATCH (:Bauwerk)-[r:BUILT_IN_ERA]->(:BauwerkEra) RETURN count(r) AS c"
            ).single()["c"]
            out["bauwerk_with_year"] = s.run(
                "MATCH (b:Bauwerk) WHERE b.baujahr IS NOT NULL OR b.jahr_errichtet IS NOT NULL "
                "RETURN count(b) AS c"
            ).single()["c"]
            out["bauwerk_year_property_examples"] = [
                {k: v for k, v in r["b"].items() if k in ("id", "name", "baujahr", "jahr_errichtet")}
                for r in s.run(
                    "MATCH (b:Bauwerk) WHERE b.baujahr IS NOT NULL OR b.jahr_errichtet IS NOT NULL "
                    "RETURN b LIMIT 25"
                )
            ]
            # Discover any year-like property name on Bauwerk
            out["bauwerk_property_keys"] = sorted(
                set(
                    k
                    for r in s.run(
                        "MATCH (b:Bauwerk) UNWIND keys(b) AS k RETURN DISTINCT k AS k"
                    )
                    for k in [r["k"]]
                )
            )
            out["bauwerk_era_edge_types"] = [
                {"type": r["t"], "count": r["c"]}
                for r in s.run(
                    "MATCH (:BauwerkEra)-[r]-() RETURN type(r) AS t, count(r) AS c ORDER BY c DESC"
                )
            ]
            out["bauwerk_era_unknown_count"] = s.run(
                "MATCH (b:Bauwerk) WHERE b.era_unknown = true RETURN count(b) AS c"
            ).single()["c"]
            out["materialdepot_total"] = s.run(
                "MATCH (m:Materialdepot) RETURN count(m) AS c"
            ).single()["c"]
            out["materialdepot_era_unknown_count"] = s.run(
                "MATCH (m:Materialdepot) WHERE m.era_unknown = true RETURN count(m) AS c"
            ).single()["c"]

            # ---- Schadstoff
            out["schadstoff_total"] = s.run(
                "MATCH (s:Schadstoff) RETURN count(s) AS c"
            ).single()["c"]
            out["schadstoff_nodes"] = [
                {"id": r["id"], "name": r["name"]}
                for r in s.run(
                    "MATCH (s:Schadstoff) RETURN s.id AS id, s.name AS name ORDER BY s.id"
                )
            ]
            out["typisch_bei_material_total"] = s.run(
                "MATCH (:Schadstoff)-[r:TYPISCH_BEI_MATERIAL]->(:Material) RETURN count(r) AS c"
            ).single()["c"]
            out["typisch_bei_era_total"] = s.run(
                "MATCH (:Schadstoff)-[r:TYPISCH_BEI_ERA]->(:BauwerkEra) RETURN count(r) AS c"
            ).single()["c"]
            out["typisch_bei_material_pairs"] = [
                {"schadstoff": r["sid"], "material": r["mname"]}
                for r in s.run(
                    "MATCH (s:Schadstoff)-[:TYPISCH_BEI_MATERIAL]->(m:Material) "
                    "RETURN s.id AS sid, m.name AS mname ORDER BY sid, mname"
                )
            ]
            out["typisch_bei_era_pairs"] = [
                {"schadstoff": r["sid"], "era": r["eid"]}
                for r in s.run(
                    "MATCH (s:Schadstoff)-[:TYPISCH_BEI_ERA]->(e:BauwerkEra) "
                    "RETURN s.id AS sid, e.id AS eid ORDER BY sid, eid"
                )
            ]

            # ---- HAT_SCHADSTOFF -> HAS_RISK_POLLUTANT
            out["hat_schadstoff_total"] = s.run(
                "MATCH ()-[r:HAT_SCHADSTOFF]->() RETURN count(r) AS c"
            ).single()["c"]
            out["hat_schadstoff_endpoints"] = [
                {
                    "left_labels": list(r["left_labels"]),
                    "right_labels": list(r["right_labels"]),
                    "count": r["c"],
                }
                for r in s.run(
                    "MATCH (a)-[r:HAT_SCHADSTOFF]->(b) RETURN labels(a) AS left_labels, "
                    "labels(b) AS right_labels, count(r) AS c"
                )
            ]
            out["hat_schadstoff_samples"] = [
                {
                    "left_id": r["lid"],
                    "right_id": r["rid"],
                    "props": dict(r["props"]),
                }
                for r in s.run(
                    "MATCH (a)-[r:HAT_SCHADSTOFF]->(b) "
                    "RETURN coalesce(a.id, elementId(a)) AS lid, "
                    "       coalesce(b.id, elementId(b)) AS rid, "
                    "       properties(r) AS props LIMIT 15"
                )
            ]
            out["has_risk_pollutant_total"] = s.run(
                "MATCH ()-[r:HAS_RISK_POLLUTANT]->() RETURN count(r) AS c"
            ).single()["c"]
            out["requires_verification_for_total"] = s.run(
                "MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->() RETURN count(r) AS c"
            ).single()["c"]

            # ---- Bauteilgruppe ↔ Bauwerk ↔ Material
            out["bauteilgruppe_total"] = s.run(
                "MATCH (bg:Bauteilgruppe) RETURN count(bg) AS c"
            ).single()["c"]
            out["nutzt_material_total"] = s.run(
                "MATCH (:Bauteilgruppe)-[r:NUTZT_MATERIAL]->(:Material) RETURN count(r) AS c"
            ).single()["c"]
            out["aus_bauwerk_total"] = s.run(
                "MATCH (:Bauteilgruppe)-[r:AUS_BAUWERK]->(:Bauwerk) RETURN count(r) AS c"
            ).single()["c"]
            out["hat_bauteilgruppe_total"] = s.run(
                "MATCH (:Projekt)-[r:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe) RETURN count(r) AS c"
            ).single()["c"]

            # Inference candidate counts
            out["era_and_material_candidate"] = s.run(
                """
                MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
                       <-[:TYPISCH_BEI_MATERIAL]-(s:Schadstoff)
                       -[:TYPISCH_BEI_ERA]->(e:BauwerkEra)
                MATCH (bg)-[:AUS_BAUWERK]->(b:Bauwerk)-[:BUILT_IN_ERA]->(e)
                RETURN count(DISTINCT [bg, s]) AS c
                """
            ).single()["c"]
            out["material_only_candidate"] = s.run(
                """
                MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material)
                       <-[:TYPISCH_BEI_MATERIAL]-(s:Schadstoff)
                RETURN count(DISTINCT [bg, s]) AS c
                """
            ).single()["c"]

            # ---- Land / Material / Norm anchors needed for Phase 3.3
            out["land_total"] = s.run("MATCH (l:Land) RETURN count(l) AS c").single()["c"]
            out["land_nodes"] = [
                {
                    "id": r["id"],
                    "name": r["name"],
                    "iso": r["iso"],
                    "country_iso": r["country_iso"],
                }
                for r in s.run(
                    "MATCH (l:Land) RETURN l.id AS id, l.name AS name, l.iso AS iso, "
                    "l.country_iso AS country_iso ORDER BY l.id"
                )
            ]
            out["material_total"] = s.run(
                "MATCH (m:Material) RETURN count(m) AS c"
            ).single()["c"]
            out["material_nodes"] = [
                {"id": r["id"], "name": r["name"]}
                for r in s.run(
                    "MATCH (m:Material) RETURN m.id AS id, m.name AS name ORDER BY m.id"
                )
            ]
            out["norm_total"] = s.run("MATCH (n:Norm) RETURN count(n) AS c").single()["c"]
            out["norm_property_keys"] = sorted(
                set(
                    r["k"]
                    for r in s.run(
                        "MATCH (n:Norm) UNWIND keys(n) AS k RETURN DISTINCT k AS k"
                    )
                )
            )
            out["norm_nodes"] = [
                {"id": r["id"], "name": r["name"]}
                for r in s.run(
                    "MATCH (n:Norm) RETURN n.id AS id, n.name AS name ORDER BY n.id LIMIT 200"
                )
            ]
            out["reuse_rule_total"] = s.run(
                "MATCH (r:ReuseRule) RETURN count(r) AS c"
            ).single()["c"]
    finally:
        drv.close()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    print(
        json.dumps(
            {
                k: out[k]
                for k in (
                    "total_nodes",
                    "total_rels",
                    "bauwerk_total",
                    "bauwerk_with_year",
                    "bauwerk_era_total",
                    "built_in_era_total",
                    "materialdepot_total",
                    "schadstoff_total",
                    "typisch_bei_material_total",
                    "typisch_bei_era_total",
                    "hat_schadstoff_total",
                    "has_risk_pollutant_total",
                    "requires_verification_for_total",
                    "era_and_material_candidate",
                    "material_only_candidate",
                    "land_total",
                    "material_total",
                    "norm_total",
                    "reuse_rule_total",
                )
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
