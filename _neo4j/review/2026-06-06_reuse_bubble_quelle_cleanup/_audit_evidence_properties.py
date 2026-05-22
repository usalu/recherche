"""Audit bubble evidence on node/rel properties; find gaps vs patch backups."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

ROOT = Path(__file__).resolve().parents[3]
RUNS = [
    "swiss_reuse_bubble_2026_06_05",
    "germany_reuse_bubble_2026_06_05",
    "france_reuse_bubble_2026_06_05",
    "netherlands_reuse_bubble_2026_06_05",
    "rotor_dc_reuse_bubble_2026_06_05",
]
RUN_DIRS = {
    "swiss_reuse_bubble_2026_06_05": ROOT / "_neo4j/intake/runs/2026-06-05_swiss_reuse_bubble",
    "germany_reuse_bubble_2026_06_05": ROOT / "_neo4j/intake/runs/2026-06-05_germany_reuse_bubble",
    "france_reuse_bubble_2026_06_05": ROOT / "_neo4j/intake/runs/2026-06-05_france_reuse_bubble",
    "netherlands_reuse_bubble_2026_06_05": ROOT / "_neo4j/intake/runs/2026-06-05_netherlands_reuse_bubble",
    "rotor_dc_reuse_bubble_2026_06_05": ROOT / "_neo4j/intake/runs/2026-06-05_rotor_dc_reuse_bubble",
}

REQUIRED_REL = ("evidence_url", "evidence_quote", "evidence_confidence", "evidence_basis", "review_run")


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def expected_from_patches(run_dir: Path) -> dict:
    node_urls: dict[str, set[str]] = {}
    rels: dict[str, dict] = {}
    quelle_urls: dict[str, str] = {}

    for bak in sorted((run_dir / "patches").glob("*.patch.jsonl.bak")):
        for rec in load_jsonl(bak):
            if rec.get("op") == "add_node" and "Quelle" in (rec.get("labels") or []):
                props = rec.get("properties") or {}
                if props.get("url"):
                    quelle_urls[rec["id"]] = props["url"]
            if rec.get("op") == "add_rel" and rec.get("type") == "BELEGT_IN":
                nid = rec.get("from")
                props = rec.get("properties") or {}
                url = props.get("evidence_url") or quelle_urls.get(rec.get("to", ""), "")
                if nid and url:
                    node_urls.setdefault(nid, set()).add(url)

    for path in sorted((run_dir / "patches").glob("*.patch.jsonl")):
        if path.name.endswith(".bak"):
            continue
        for rec in load_jsonl(path):
            if rec.get("op") == "set_node_properties":
                props = rec.get("properties") or {}
                urls = set(props.get("source_urls") or [])
                if props.get("primary_source_url"):
                    urls.add(props["primary_source_url"])
                if urls:
                    node_urls.setdefault(rec["id"], set()).update(urls)
            if rec.get("op") == "add_rel" and rec.get("type") != "BELEGT_IN":
                props = rec.get("properties") or {}
                rid = props.get("id")
                if rid:
                    rels[rid] = props

    return {"node_urls": {k: sorted(v) for k, v in node_urls.items()}, "rels": rels}


uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
report: dict = {"database": db, "by_run": {}, "totals": {}}
try:
    with driver.session(database=db) as s:
        for run in RUNS:
            run_report: dict = {
                "rels_in_graph": 0,
                "rels_missing_in_graph": [],
                "rels_property_gaps": [],
                "nodes_url_gaps": [],
                "nodes_missing_in_graph": [],
            }
            expected = expected_from_patches(RUN_DIRS[run])

            for rid, props in expected["rels"].items():
                row = s.run(
                    """
                    MATCH ()-[r]->()
                    WHERE r.id = $id
                    RETURN r.id AS id, type(r) AS typ,
                           r.evidence_url AS evidence_url,
                           r.evidence_quote AS evidence_quote,
                           r.evidence_confidence AS evidence_confidence,
                           r.evidence_basis AS evidence_basis,
                           r.review_run AS review_run,
                           r.evidence_source_id AS evidence_source_id,
                           r.metadata_sidecar_key AS metadata_sidecar_key
                    """,
                    id=rid,
                ).single()
                if row is None:
                    run_report["rels_missing_in_graph"].append(rid)
                    continue
                run_report["rels_in_graph"] += 1
                gaps = []
                for key in REQUIRED_REL:
                    if not row[key]:
                        gaps.append(key)
                if row["evidence_source_id"] or row["metadata_sidecar_key"]:
                    gaps.append("stale_pointer_props")
                if gaps:
                    run_report["rels_property_gaps"].append(
                        {"id": rid, "gaps": gaps, "expected": {k: props.get(k) for k in REQUIRED_REL}}
                    )

            for nid, urls in expected["node_urls"].items():
                row = s.run(
                    """
                    MATCH (n {id: $id})
                    RETURN n.id AS id, labels(n) AS labels,
                           n.primary_source_url AS primary_source_url,
                           n.source_urls AS source_urls
                    """,
                    id=nid,
                ).single()
                if row is None:
                    run_report["nodes_missing_in_graph"].append(nid)
                    continue
                have = set(row["source_urls"] or [])
                if row["primary_source_url"]:
                    have.add(row["primary_source_url"])
                missing = [u for u in urls if u not in have]
                if missing or not row["primary_source_url"]:
                    run_report["nodes_url_gaps"].append(
                        {
                            "id": nid,
                            "missing_urls": missing,
                            "expected_urls": urls,
                            "have": sorted(have),
                        }
                    )

            # Bubble rels without patch id match — scan orphans
            orphans = s.run(
                """
                MATCH ()-[r]->()
                WHERE r.review_run = $run
                RETURN r.id AS id, r.evidence_url AS evidence_url,
                       r.evidence_quote AS evidence_quote,
                       r.evidence_confidence AS evidence_confidence
                """,
                run=run,
            )
            orphan_gaps = []
            for row in orphans:
                if not row["evidence_url"] or not row["evidence_quote"] or not row["evidence_confidence"]:
                    orphan_gaps.append(dict(row))
            run_report["orphan_rel_gaps"] = orphan_gaps
            report["by_run"][run] = run_report

        report["totals"] = {
            "rels_missing": sum(len(v["rels_missing_in_graph"]) for v in report["by_run"].values()),
            "rels_property_gaps": sum(len(v["rels_property_gaps"]) for v in report["by_run"].values()),
            "nodes_url_gaps": sum(len(v["nodes_url_gaps"]) for v in report["by_run"].values()),
            "orphan_rel_gaps": sum(len(v["orphan_rel_gaps"]) for v in report["by_run"].values()),
        }
finally:
    driver.close()

out = Path(__file__).resolve().parent / "evidence_property_audit.json"
out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(out)
print(json.dumps(report["totals"], indent=2))
