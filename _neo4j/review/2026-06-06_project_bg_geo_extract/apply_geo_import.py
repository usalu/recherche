"""Apply geo import patches to mit-bestand (dry-run default)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[3]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))

from apply_neo4j_review_patch import run as run_patch_apply  # noqa: E402
from neo4j_env import resolve_connection  # noqa: E402

RUN = "2026-06-06_project_bg_geo_extract"
OUT = Path(__file__).resolve().parent
PATCHES = OUT / "patches"
PHASES = [
    "phase1_projekte_geo.patch.jsonl",
    "phase2_bauwerke_geo.patch.jsonl",
    "phase3_staedte_geo.patch.jsonl",
    "phase4_new_donor_bauwerke.patch.jsonl",
]

COVERAGE_QUERIES = {
    "projekte_with_adresse": "MATCH (p:Projekt) WHERE p.adresse IS NOT NULL RETURN count(p) AS value",
    "bauwerke_with_adresse": "MATCH (bw:Bauwerk) WHERE bw.adresse IS NOT NULL RETURN count(bw) AS value",
    "staedte_with_latitude": "MATCH (s:Stadt) WHERE s.latitude IS NOT NULL RETURN count(s) AS value",
    "low_confidence_projekte": (
        "MATCH (p:Projekt) WHERE p.geo_confidence = 'low' "
        "RETURN count(p) AS value, collect(p.id) AS ids"
    ),
    "superlocal_chain": """
        MATCH (bg:Bauteilgruppe {id:'bg_mehrere_mehrere_superlocal_beton_wohnungsteile'})
              -[:AUS_SPENDER]->(d:Bauwerk)
        MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)
        RETURN d.adresse AS donor_adresse, p.adresse AS receiver_adresse,
               d.latitude AS donor_lat, p.latitude AS receiver_lat
    """,
}


def graph_counts(session) -> dict[str, int]:
    row = session.run(
        "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels"
    ).single()
    return {"nodes": row["nodes"], "relationships": row["rels"]}


def coverage_snapshot(session) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name, cypher in COVERAGE_QUERIES.items():
        rows = [dict(r) for r in session.run(cypher)]
        if len(rows) == 1 and "value" in rows[0] and len(rows[0]) <= 2:
            out[name] = rows[0].get("value")
            if "ids" in rows[0]:
                out[f"{name}_ids"] = rows[0]["ids"]
        else:
            out[name] = rows
    return out


def snapshot_geo_properties(session) -> dict[str, Any]:
    rows = session.run(
        """
        MATCH (n)
        WHERE (n:Projekt OR n:Bauwerk OR n:Stadt)
          AND (n.adresse IS NOT NULL OR n.latitude IS NOT NULL OR n.longitude IS NOT NULL
               OR n.geo_confidence IS NOT NULL OR n.geo_import_run IS NOT NULL)
        RETURN labels(n) AS labels, n.id AS id, properties(n) AS props
        ORDER BY id
        """
    )
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "nodes": [
            {
                "id": r["id"],
                "labels": list(r["labels"]),
                "properties": {
                    k: r["props"][k]
                    for k in r["props"]
                    if k.startswith("geo_") or k in ("adresse", "latitude", "longitude", "metadata_sidecar_key", "source_urls")
                },
            }
            for r in rows
        ],
    }


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
            report["coverage_before"] = coverage_snapshot(session)
            if commit:
                before = snapshot_geo_properties(session)
                (OUT / "geo_import_before.json").write_text(
                    json.dumps(before, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )

        for phase_file in PHASES:
            patch_path = PATCHES / phase_file
            if not patch_path.is_file():
                report["phases"].append({"phase": phase_file, "status": "skipped_missing"})
                continue
            if patch_path.stat().st_size == 0:
                report["phases"].append({"phase": phase_file, "status": "skipped_empty"})
                continue

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
                raise RuntimeError(f"Phase {phase_file} has rejected records: {hard_fail}")

            report["phases"].append(
                {
                    "phase": phase_file,
                    "dry_run": phase_result.get("dry_run"),
                    "summary": summary,
                    "counts_before": phase_result.get("counts_before"),
                    "counts_after_actual": phase_result.get("counts_after_actual"),
                    "report_files": phase_result.get("report_files"),
                }
            )

        with driver.session(database=db) as session:
            report["counts_after"] = graph_counts(session)
            report["coverage_after"] = coverage_snapshot(session)
    finally:
        driver.close()

    (OUT / "apply_summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
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
