"""Ensure bubble evidence lives on correct node/rel properties in mit-bestand."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from apply_neo4j_review_patch import run as run_patch_apply
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

ROOT = Path(__file__).resolve().parents[3]
REVIEW = Path(__file__).resolve().parent
RUNS = [
    "swiss_reuse_bubble_2026_06_05",
    "germany_reuse_bubble_2026_06_05",
    "france_reuse_bubble_2026_06_05",
    "netherlands_reuse_bubble_2026_06_05",
    "rotor_dc_reuse_bubble_2026_06_05",
]
RUN_DIRS = [
    ROOT / "_neo4j/intake/runs/2026-06-05_swiss_reuse_bubble",
    ROOT / "_neo4j/intake/runs/2026-06-05_germany_reuse_bubble",
    ROOT / "_neo4j/intake/runs/2026-06-05_france_reuse_bubble",
    ROOT / "_neo4j/intake/runs/2026-06-05_netherlands_reuse_bubble",
    ROOT / "_neo4j/intake/runs/2026-06-05_rotor_dc_reuse_bubble",
]
DROP_REL_PROPS = [
    "evidence_source_id",
    "secondary_evidence_source_ids",
    "archive_source_id",
    "metadata_sidecar_key",
    "evidence_claim_ids",
]

# phase1c intentional deletes — remove stale add_rel from phase1 patches if still present
DELETE_REL_IDS = {
    "r_mobius_reemploi__verbunden_mit_akteur__cycle_up",
    "r_cycle_up__verbunden_mit_akteur__mobius_reemploi",
    "r_raedificare__verbunden_mit_akteur__backacia",
    "r_backacia__verbunden_mit_akteur__raedificare",
    "r_association_reavie__verbunden_mit_akteur__mobius_reemploi",
    "r_mobius_reemploi__verbunden_mit_akteur__association_reavie",
    "r_circular_structural_design__verbunden_mit_akteur__bauteilboerse_hannover",
    "r_bauteilboerse_hannover__verbunden_mit_akteur__circular_structural_design",
    "r_haus_der_materialisierung__verbunden_mit_akteur__bauteilboerse_bremen",
    "r_bauteilboerse_bremen__verbunden_mit_akteur__haus_der_materialisierung",
    "r_haus_der_materialisierung__verbunden_mit_akteur__bauteilboerse_hannover",
    "r_bauteilboerse_hannover__verbunden_mit_akteur__haus_der_materialisierung",
    "r_haus_der_materialisierung__verbunden_mit_akteur__madaster_epea",
    "r_madaster_epea__verbunden_mit_akteur__haus_der_materialisierung",
}


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def dump_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + ("\n" if rows else ""),
        encoding="utf-8",
    )


def clean_rel_props(props: dict) -> dict:
    out = dict(props)
    for key in DROP_REL_PROPS:
        out.pop(key, None)
    return out


def collect_urls_from_backups() -> dict[str, set[str]]:
    node_urls: dict[str, set[str]] = {}
    quelle_urls: dict[str, str] = {}
    for run_dir in RUN_DIRS:
        for bak in sorted((run_dir / "patches").glob("*.patch.jsonl.bak")):
            for rec in load_jsonl(bak):
                if rec.get("op") == "add_node" and "Quelle" in (rec.get("labels") or []):
                    url = (rec.get("properties") or {}).get("url")
                    if url:
                        quelle_urls[rec["id"]] = url
                if rec.get("op") == "add_rel" and rec.get("type") == "BELEGT_IN":
                    nid = rec.get("from")
                    props = rec.get("properties") or {}
                    url = props.get("evidence_url") or quelle_urls.get(rec.get("to", ""), "")
                    if nid and url:
                        node_urls.setdefault(nid, set()).add(url)
        for path in sorted((run_dir / "patches").glob("*.patch.jsonl")):
            if path.name.endswith(".bak") or path.name.startswith("phase0"):
                continue
            for rec in load_jsonl(path):
                if rec.get("op") == "set_node_properties":
                    props = rec.get("properties") or {}
                    for url in props.get("source_urls") or []:
                        node_urls.setdefault(rec["id"], set()).add(url)
                    if props.get("primary_source_url"):
                        node_urls.setdefault(rec["id"], set()).add(props["primary_source_url"])
    return node_urls


def sync_patch_files() -> dict:
    changed: dict[str, int] = {}
    for run_dir in RUN_DIRS:
        for path in sorted((run_dir / "patches").glob("*.patch.jsonl")):
            if path.name.endswith(".bak"):
                continue
            rows = load_jsonl(path)
            new_rows = []
            n = 0
            for rec in rows:
                if rec.get("op") == "add_rel":
                    rid = (rec.get("properties") or {}).get("id")
                    if rid in DELETE_REL_IDS:
                        n += 1
                        continue
                    rec = dict(rec)
                    rec["properties"] = clean_rel_props(rec.get("properties") or {})
                    new_rows.append(rec)
                elif rec.get("op") == "set_rel_properties":
                    rec = dict(rec)
                    rec["properties"] = clean_rel_props(rec.get("properties") or {})
                    new_rows.append(rec)
                else:
                    new_rows.append(rec)
            if n or any(clean_rel_props(r.get("properties") or {}) != (r.get("properties") or {}) for r in rows if r.get("op") in {"add_rel", "set_rel_properties"}):
                dump_jsonl(path, new_rows)
                changed[str(path.relative_to(ROOT))] = n
    return changed


def build_node_url_patch(node_urls: dict[str, set[str]]) -> Path:
    rows = []
    for node_id in sorted(node_urls):
        urls = sorted(node_urls[node_id])
        rows.append(
            {
                "id": node_id,
                "op": "set_node_properties",
                "properties": {"source_urls": urls, "primary_source_url": urls[0]},
            }
        )
    patch = REVIEW / "patches" / "bubble_node_source_urls.patch.jsonl"
    patch.parent.mkdir(parents=True, exist_ok=True)
    dump_jsonl(patch, rows)
    return patch


def build_missing_rel_patch() -> Path:
    """Germany phase1c bauteilnetz edges that should exist."""
    rows = []
    for rec in load_jsonl(
        ROOT / "_neo4j/intake/runs/2026-06-05_germany_reuse_bubble/patches/phase1c_evidence_hardening.patch.jsonl"
    ):
        if rec.get("op") == "add_rel":
            rec = dict(rec)
            rec["properties"] = clean_rel_props(rec.get("properties") or {})
            rows.append(rec)
    patch = REVIEW / "patches" / "bubble_missing_rels.patch.jsonl"
    dump_jsonl(patch, rows)
    return patch


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()

    report: dict = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "commit": args.commit,
    }
    report["patch_sync"] = sync_patch_files()
    node_urls = collect_urls_from_backups()
    report["node_url_targets"] = len(node_urls)

    uri, u, pw, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(u, pw))
    try:
        with driver.session(database=db) as s:
            report["counts_before"] = {
                "nodes": s.run("MATCH (n) RETURN count(n) AS c").single()["c"],
                "relationships": s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"],
            }
            if args.commit:
                removed = ", ".join(f"r.{p}" for p in DROP_REL_PROPS)
                s.run(
                    f"MATCH ()-[r]->() WHERE r.review_run IN $runs REMOVE {removed}",
                    runs=RUNS,
                )
    finally:
        driver.close()

    patches = [build_node_url_patch(node_urls), build_missing_rel_patch()]
    apply_reports = []
    for patch in patches:
        class Args:
            pass

        a = Args()
        a.patch = patch
        a.database = db
        a.dry_run = not args.commit
        a.confirm = "" if not args.commit else f"APPLY {patch.name} TO {db}"
        a.report_dir = REVIEW / "apply_reports"
        a.report_dir.mkdir(parents=True, exist_ok=True)
        rep = run_patch_apply(a)
        apply_reports.append({"patch": str(patch.relative_to(ROOT)), "summary": rep.get("summary")})
    report["apply_reports"] = apply_reports

    driver = GraphDatabase.driver(uri, auth=(u, pw))
    try:
        with driver.session(database=db) as s:
            report["counts_after"] = {
                "nodes": s.run("MATCH (n) RETURN count(n) AS c").single()["c"],
                "relationships": s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"],
            }
            report["verification"] = {
                "pointer_props": s.run(
                    """
                    MATCH ()-[r]->()
                    WHERE r.review_run IN $runs
                      AND (r.evidence_source_id IS NOT NULL OR r.metadata_sidecar_key IS NOT NULL)
                    RETURN count(r) AS c
                    """,
                    runs=RUNS,
                ).single()["c"],
                "rels_missing_evidence": s.run(
                    """
                    MATCH ()-[r]->()
                    WHERE r.review_run IN $runs
                      AND (r.evidence_url IS NULL OR r.evidence_quote IS NULL OR r.evidence_confidence IS NULL)
                    RETURN count(r) AS c
                    """,
                    runs=RUNS,
                ).single()["c"],
                "bubble_nodes_no_urls": s.run(
                    """
                    MATCH (n)-[r]->()
                    WHERE r.review_run IN $runs
                    WITH DISTINCT n
                    WHERE n.primary_source_url IS NULL AND n.source_urls IS NULL
                    RETURN count(n) AS c
                    """,
                    runs=RUNS,
                ).single()["c"],
            }
    finally:
        driver.close()

    out = REVIEW / "evidence_property_fix_report.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(out)
    print(json.dumps(report["verification"], indent=2))


if __name__ == "__main__":
    main()
