"""Agent 11 — second probe: Bauteilgruppe relationships, Bauwerk-Projekt links, donor materialdepot."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j/intake/runs/2026-05-20_radical_quality_reset"
OUT = RUN_ROOT / "logs/agent11_probe2.json"


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
            out["bauteilgruppe_outgoing_edges"] = [
                {"type": r["t"], "right_labels": r["lbls"], "count": r["c"]}
                for r in s.run(
                    """
                    MATCH (bg:Bauteilgruppe)-[r]->(x)
                    RETURN type(r) AS t, labels(x) AS lbls, count(r) AS c
                    ORDER BY c DESC
                    """
                )
            ]
            out["bauteilgruppe_incoming_edges"] = [
                {"type": r["t"], "left_labels": r["lbls"], "count": r["c"]}
                for r in s.run(
                    """
                    MATCH (x)-[r]->(bg:Bauteilgruppe)
                    RETURN type(r) AS t, labels(x) AS lbls, count(r) AS c
                    ORDER BY c DESC
                    """
                )
            ]
            out["bauwerk_outgoing_edges"] = [
                {"type": r["t"], "right_labels": r["lbls"], "count": r["c"]}
                for r in s.run(
                    """
                    MATCH (b:Bauwerk)-[r]->(x)
                    RETURN type(r) AS t, labels(x) AS lbls, count(r) AS c
                    ORDER BY c DESC
                    """
                )
            ]
            out["bauwerk_incoming_edges"] = [
                {"type": r["t"], "left_labels": r["lbls"], "count": r["c"]}
                for r in s.run(
                    """
                    MATCH (x)-[r]->(b:Bauwerk)
                    RETURN type(r) AS t, labels(x) AS lbls, count(r) AS c
                    ORDER BY c DESC
                    """
                )
            ]
            out["materialdepot_outgoing_edges"] = [
                {"type": r["t"], "right_labels": r["lbls"], "count": r["c"]}
                for r in s.run(
                    """
                    MATCH (m:Materialdepot)-[r]->(x)
                    RETURN type(r) AS t, labels(x) AS lbls, count(r) AS c
                    ORDER BY c DESC
                    """
                )
            ]
            out["materialdepot_incoming_edges"] = [
                {"type": r["t"], "left_labels": r["lbls"], "count": r["c"]}
                for r in s.run(
                    """
                    MATCH (x)-[r]->(m:Materialdepot)
                    RETURN type(r) AS t, labels(x) AS lbls, count(r) AS c
                    ORDER BY c DESC
                    """
                )
            ]
            out["materialdepot_property_keys"] = sorted(
                set(
                    r["k"]
                    for r in s.run(
                        "MATCH (m:Materialdepot) UNWIND keys(m) AS k RETURN DISTINCT k AS k"
                    )
                )
            )
            out["materialdepot_nodes"] = [
                dict(r["m"])
                for r in s.run(
                    "MATCH (m:Materialdepot) RETURN m ORDER BY m.id LIMIT 50"
                )
            ]

            # Project ↔ Bauwerk relationships?
            out["projekt_bauwerk_paths"] = [
                {"type": r["t"], "count": r["c"]}
                for r in s.run(
                    """
                    MATCH (p:Projekt)-[r]-(b:Bauwerk)
                    RETURN type(r) AS t, count(r) AS c
                    ORDER BY c DESC
                    """
                )
            ]

            # Sample BG without AUS_BAUWERK
            out["bg_with_material_no_bauwerk"] = s.run(
                """
                MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material)
                WHERE NOT exists{(bg)-[:AUS_BAUWERK]->(:Bauwerk)}
                RETURN count(DISTINCT bg) AS c
                """
            ).single()["c"]
            out["bg_with_material_and_bauwerk"] = s.run(
                """
                MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material)
                WHERE exists{(bg)-[:AUS_BAUWERK]->(:Bauwerk)}
                RETURN count(DISTINCT bg) AS c
                """
            ).single()["c"]

            # Approximate Bauteilgruppe→Bauwerk via Projekt
            out["bg_via_projekt_to_bauwerk_candidate"] = s.run(
                """
                MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
                MATCH (p)-[r]-(b:Bauwerk)
                RETURN count(DISTINCT bg) AS c
                """
            ).single()["c"]
            out["bg_via_projekt_bauwerk_edge_types"] = [
                {"type": r["t"], "count": r["c"]}
                for r in s.run(
                    """
                    MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
                    MATCH (p)-[r]-(b:Bauwerk)
                    RETURN type(r) AS t, count(DISTINCT bg) AS c
                    ORDER BY c DESC
                    """
                )
            ]

            # Material name list to align names from the source markdown
            out["material_name_index"] = {
                r["name"]: r["id"]
                for r in s.run("MATCH (m:Material) RETURN m.id AS id, m.name AS name")
            }

            # ---- HAT_SCHADSTOFF endpoints (sample with bg or projekt id)
            out["hat_schadstoff_samples_all"] = [
                {
                    "left_id": r["lid"],
                    "left_labels": list(r["l_lbls"]),
                    "right_id": r["rid"],
                    "props": dict(r["props"]),
                }
                for r in s.run(
                    """
                    MATCH (a)-[r:HAT_SCHADSTOFF]->(b)
                    RETURN coalesce(a.id, elementId(a)) AS lid,
                           labels(a) AS l_lbls,
                           coalesce(b.id, elementId(b)) AS rid,
                           properties(r) AS props
                    """
                )
            ]
    finally:
        drv.close()

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    print(json.dumps({k: v for k, v in out.items() if not isinstance(v, list)}, indent=2))
    print("bg_with_material_and_bauwerk =", out["bg_with_material_and_bauwerk"])
    print("bg_with_material_no_bauwerk =", out["bg_with_material_no_bauwerk"])
    print("bg_via_projekt_to_bauwerk_candidate =", out["bg_via_projekt_to_bauwerk_candidate"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
