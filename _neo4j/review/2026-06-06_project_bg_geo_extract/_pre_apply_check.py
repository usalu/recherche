"""Pre-apply audit for geo import: baseline, ID reconciliation, overwrite guard."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT_DIR = Path(__file__).resolve().parent
RUN = "2026-06-06_project_bg_geo_extract"
BASELINE_NODES = 2273
BASELINE_RELS = 15118
GEO_KEYS = ("adresse", "latitude", "longitude")


def load_unified() -> dict:
    return json.loads((OUT_DIR / "reuse_geo_graph.json").read_text(encoding="utf-8"))


def node_exists(session, node_id: str) -> bool:
    row = session.run("MATCH (n {id: $id}) RETURN n.id AS id LIMIT 1", id=node_id).single()
    return row is not None


def geo_overwrite_count(session, label: str) -> dict[str, int]:
    row = session.run(
        f"""
        MATCH (n:{label})
        RETURN
          count(n) AS total,
          count(CASE WHEN n.adresse IS NOT NULL THEN 1 END) AS with_adresse,
          count(CASE WHEN n.latitude IS NOT NULL THEN 1 END) AS with_latitude,
          count(CASE WHEN n.longitude IS NOT NULL THEN 1 END) AS with_longitude
        """
    ).single()
    return dict(row)


def main() -> None:
    unified = load_unified()
    projekt_ids = [p["id"] for p in unified["nodes"]["projekte"]]
    bauwerk_ids = [b["id"] for b in unified["nodes"]["bauwerke"]]
    donor_ids = [
        b["id"]
        for b in unified["nodes"]["bauwerke"]
        if b["roles"]["donor_for_bauteilgruppe_ids"]
    ]

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    report: dict = {
        "run": RUN,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "baseline_expected": {"nodes": BASELINE_NODES, "relationships": BASELINE_RELS},
        "export_counts": {
            "projekte": len(projekt_ids),
            "bauwerke": len(bauwerk_ids),
            "donor_bauwerke": len(donor_ids),
        },
    }

    with driver.session(database=database) as session:
        counts = session.run(
            "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels"
        ).single()
        report["counts_live"] = {"nodes": counts["nodes"], "relationships": counts["rels"]}
        report["baseline_ok"] = (
            counts["nodes"] == BASELINE_NODES and counts["rels"] == BASELINE_RELS
        )

        apply_p: list[str] = []
        skip_p: list[dict] = []
        for pid in projekt_ids:
            if node_exists(session, pid):
                apply_p.append(pid)
            else:
                skip_p.append({"id": pid, "reason": "not_in_graph"})

        apply_bw: list[str] = []
        skip_bw: list[dict] = []
        for bid in bauwerk_ids:
            if node_exists(session, bid):
                apply_bw.append(bid)
            else:
                skip_bw.append({"id": bid, "reason": "not_in_graph"})

        missing_donors = [bid for bid in donor_ids if bid not in apply_bw]
        report["projekte"] = {
            "apply": apply_p,
            "skip": skip_p,
            "apply_count": len(apply_p),
            "skip_count": len(skip_p),
        }
        report["bauwerke"] = {
            "apply": apply_bw,
            "skip": skip_bw,
            "apply_count": len(apply_bw),
            "skip_count": len(skip_bw),
            "missing_donor_ids": missing_donors,
        }

        graph_projekt_ids = [
            r["id"]
            for r in session.run("MATCH (p:Projekt) RETURN p.id AS id ORDER BY id")
        ]
        export_set = set(projekt_ids)
        report["deferred_no_geo"] = sorted(set(graph_projekt_ids) - export_set)

        report["overwrite_guard"] = {
            "Projekt": geo_overwrite_count(session, "Projekt"),
            "Bauwerk": geo_overwrite_count(session, "Bauwerk"),
            "Stadt": geo_overwrite_count(session, "Stadt"),
        }
        report["overwrite_ok"] = all(
            report["overwrite_guard"][label]["with_adresse"] == 0
            and report["overwrite_guard"][label]["with_latitude"] == 0
            and report["overwrite_guard"][label]["with_longitude"] == 0
            for label in ("Projekt", "Bauwerk")
        )

    driver.close()

    report["ready"] = (
        report["overwrite_ok"]
        and len(report["bauwerke"]["missing_donor_ids"]) == 0
        and report["projekte"]["apply_count"] > 0
    )
    if not report["baseline_ok"]:
        report["baseline_note"] = (
            "Graph counts differ from FINAL_AUDIT_REPORT.md — "
            "proceed if intentional (later intakes); geo import is property-only."
        )

    out_path = OUT_DIR / "pre_apply_report.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
