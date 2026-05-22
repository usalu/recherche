"""Apply Rotor DC reuse bubble evidence-backed patches to mit-bestand."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[4]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))

from neo4j import GraphDatabase

from apply_neo4j_review_patch import run as run_patch_apply  # noqa: E402
from neo4j_env import resolve_connection  # noqa: E402

RUN = "2026-06-05_rotor_dc_reuse_bubble"
OUT = Path(__file__).resolve().parent
PATCHES = OUT / "patches"
PHASES = [
    "phase0_sources_and_dossier.patch.jsonl",
    "phase1_ecosystem_spine.patch.jsonl",
    "phase1b_publication_hub.patch.jsonl",
    "phase2_oxy_hub.patch.jsonl",
    "phase3_material_path_upgrades.patch.jsonl",
]

CONNECTIVITY = [
    (
        "T0_opalis_verbunden_degree",
        """
        MATCH (o:Akteur {id: 'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
        RETURN count(DISTINCT a) AS value, collect(DISTINCT a.id) AS neighbors
        """,
    ),
    (
        "T1_prog_preuse_partners",
        """
        MATCH (p:Programm {id: 'prog_preuse'})<-[:BETEILIGT_AN]-(a)
        RETURN collect(a.id) AS value
        """,
    ),
    (
        "T2_spine_mesh",
        """
        MATCH (opalis:Akteur {id:'opalis'})-[r1:VERBUNDEN_MIT_AKTEUR]-(rotordc:Akteur {id:'rotordc'})
        MATCH (opalis)-[r2:VERBUNDEN_MIT_AKTEUR]-(bellastock:Akteur {id:'bellastock'})
        RETURN count(r1) + count(r2) AS value
        """,
    ),
    (
        "T3_oxy_hub",
        """
        MATCH (p:Projekt {id:'p_oxy_centre_monnaie'})<-[:BETEILIGT_AN]-(a)
        RETURN collect(a.id) AS value
        """,
    ),
    (
        "T4_generale_multi_path",
        """
        MATCH (p:Projekt {id:'p_multi_brussels_reuse_in_multi'})-[:HAT_BAUWERK]->(bw:Bauwerk {id:'bw_generale_de_banque_brussels'})
        RETURN count(*) AS value
        """,
    ),
    (
        "T5_bubble_edges",
        """
        MATCH ()-[r]->()
        WHERE r.review_run = 'rotor_dc_reuse_bubble_2026_06_05'
        RETURN count(r) AS value
        """,
    ),
]


def connectivity_snapshot(session) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name, cypher in CONNECTIVITY:
        row = session.run(cypher).single()
        if row is None:
            out[name] = None
            continue
        data = dict(row)
        if "value" in data and len(data) == 1:
            out[name] = data["value"]
        else:
            out[name] = data
    return out


def graph_counts(session) -> dict[str, int]:
    row = session.run(
        "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels"
    ).single()
    return {"nodes": row["nodes"], "relationships": row["rels"]}


def apply_phases(commit: bool, database: str) -> dict[str, Any]:
    uri, user, password, default_db = resolve_connection()
    db = database or default_db
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "run": RUN,
        "commit": commit,
        "database": db,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "phases": [],
    }
    try:
        driver.verify_connectivity()
        with driver.session(database=db) as session:
            report["counts_before"] = graph_counts(session)
            report["connectivity_before"] = connectivity_snapshot(session)

        for phase_file in PHASES:
            patch_path = PATCHES / phase_file
            if not patch_path.is_file():
                raise FileNotFoundError(patch_path)

            class Args:
                patch = patch_path
                database = db
                dry_run = not commit
                confirm = "" if not commit else f"APPLY {phase_file} TO {db}"
                report_dir = OUT / "apply_reports"

            phase_result = run_patch_apply(Args())
            phase_summary = {
                "phase": phase_file,
                "dry_run": phase_result.get("dry_run"),
                "summary": phase_result.get("summary"),
                "counts_before": phase_result.get("counts_before"),
                "counts_after_actual": phase_result.get("counts_after_actual"),
                "counts_after_expected": phase_result.get("counts_after_expected"),
                "report_files": phase_result.get("report_files"),
            }
            summary = phase_result.get("summary") or {}
            hard_fail = {
                k: summary[k]
                for k in ("invalid", "missing_node", "missing_rel", "rejected", "unsupported")
                if summary.get(k)
            }
            if hard_fail and commit:
                raise RuntimeError(f"Phase {phase_file} has rejected records: {hard_fail}")
            missing_ep = summary.get("missing_endpoint", 0)
            if missing_ep and commit:
                raise RuntimeError(
                    f"Phase {phase_file} has {missing_ep} missing_endpoint — run prior phases first or fix ids"
                )
            report["phases"].append(phase_summary)

        with driver.session(database=db) as session:
            report["counts_after"] = graph_counts(session)
            report["connectivity_after"] = connectivity_snapshot(session)
    finally:
        driver.close()

    out_path = OUT / "connectivity_report.json"
    existing = {}
    if out_path.is_file():
        existing = json.loads(out_path.read_text(encoding="utf-8"))
    merged = {**existing, **report}
    out_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report["connectivity_report"] = str(out_path)
    (OUT / "apply_summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true", help="Apply to Neo4j (default dry-run)")
    parser.add_argument("--database", default="", help="Override NEO4J_DATABASE")
    args = parser.parse_args()
    result = apply_phases(commit=args.commit, database=args.database)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
