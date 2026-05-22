"""Apply France reuse bubble evidence-backed patches to mit-bestand."""
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

RUN = "2026-06-05_france_reuse_bubble"
OUT = Path(__file__).resolve().parent
PATCHES = OUT / "patches"
PHASES = [
    "phase0_sources_and_dossier.patch.jsonl",
    "phase1_france_marketplace_spine.patch.jsonl",
    "phase2_idf_civic_links.patch.jsonl",
]
HARDENING_PHASES = [
    "phase1c_evidence_hardening.patch.jsonl",
]

CONNECTIVITY = [
    (
        "T0_bellastock_ecosystem_verbunden",
        """
        MATCH (b:Akteur {id: 'bellastock'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
        WHERE NOT a.id IN ['hugo_topalov', 'sarah_westerfeld', 'frederic_denise']
        RETURN count(DISTINCT a) AS value, collect(DISTINCT a.id) AS neighbors
        """,
    ),
    (
        "T1_opalis_ecosystem_verbunden",
        """
        MATCH (o:Akteur {id: 'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
        WHERE NOT a.id IN ['maarten_gielen']
        RETURN count(DISTINCT a) AS value, collect(DISTINCT a.id) AS neighbors
        """,
    ),
    (
        "T2_cycle_up_spine",
        """
        MATCH (c:Akteur {id: 'cycle_up'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
        RETURN collect(DISTINCT a.id) AS value
        """,
    ),
    (
        "T3_backacia_spine",
        """
        MATCH (b:Akteur {id: 'backacia'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
        RETURN collect(DISTINCT a.id) AS value
        """,
    ),
    (
        "T4_mobius_spine",
        """
        MATCH (m:Akteur {id: 'mobius_reemploi'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
        WHERE NOT a.id IN ['frederic_denise']
        RETURN collect(DISTINCT a.id) AS value
        """,
    ),
    (
        "T5_opalis_backacia",
        """
        MATCH (o:Akteur {id: 'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(b:Akteur {id: 'backacia'})
        RETURN count(r) AS value
        """,
    ),
    (
        "T6_mobius_cstb",
        """
        MATCH (m:Akteur {id: 'mobius_reemploi'})-[r:VERBUNDEN_MIT_AKTEUR]-(c:Akteur {id: 'cstb'})
        RETURN count(r) AS value
        """,
    ),
    (
        "T7_association_reavie_bellastock",
        """
        MATCH (r:Akteur {id: 'association_reavie'})-[x:VERBUNDEN_MIT_AKTEUR]-(b:Akteur {id: 'bellastock'})
        RETURN count(x) AS value
        """,
    ),
    (
        "T8_bubble_edges",
        """
        MATCH ()-[r]->()
        WHERE r.review_run = 'france_reuse_bubble_2026_06_05'
        RETURN count(r) AS value
        """,
    ),
    (
        "T9_opalis_reavie",
        """
        MATCH (o:Akteur {id: 'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur {id: 'association_reavie'})
        RETURN count(r) AS value
        """,
    ),
    (
        "T10_mineka_spine",
        """
        MATCH (m:Akteur {id: 'mineka'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
        RETURN collect(DISTINCT a.id) AS value
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


def apply_phases(commit: bool, database: str, hardening_only: bool = False) -> dict[str, Any]:
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

        phase_list = HARDENING_PHASES if hardening_only else PHASES
        for phase_file in phase_list:
            patch_path = PATCHES / phase_file
            class Args:
                patch = patch_path
                database = db
                dry_run = not commit
                confirm = "" if not commit else f"APPLY {phase_file} TO {db}"
                report_dir = OUT / "apply_reports"

            phase_result = run_patch_apply(Args())
            summary = phase_result.get("summary") or {}
            hard_fail = {
                k: summary[k]
                for k in ("invalid", "missing_node", "missing_rel", "rejected", "unsupported")
                if summary.get(k)
            }
            if hard_fail and commit:
                raise RuntimeError(f"Phase {phase_file} rejected: {hard_fail}")
            missing_ep = summary.get("missing_endpoint", 0)
            if missing_ep and commit:
                raise RuntimeError(f"Phase {phase_file} missing_endpoint={missing_ep}")
            report["phases"].append({
                "phase": phase_file,
                "dry_run": phase_result.get("dry_run"),
                "summary": summary,
                "counts_after_actual": phase_result.get("counts_after_actual"),
                "report_files": phase_result.get("report_files"),
            })

        with driver.session(database=db) as session:
            report["counts_after"] = graph_counts(session)
            report["connectivity_after"] = connectivity_snapshot(session)
    finally:
        driver.close()

    out_path = OUT / "connectivity_report.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "apply_summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--hardening-only", action="store_true", help="Run phase1c evidence hardening only")
    parser.add_argument("--database", default="")
    args = parser.parse_args()
    print(json.dumps(apply_phases(commit=args.commit, database=args.database, hardening_only=args.hardening_only), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
