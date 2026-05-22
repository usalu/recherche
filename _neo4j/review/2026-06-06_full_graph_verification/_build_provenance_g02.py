"""Agent G2 — git provenance for PARTIAL HAT_BAUTEILTYP / NUTZT_MATERIAL catalogue edges."""
from __future__ import annotations

import csv
import json
import subprocess
from collections import Counter
from pathlib import Path

from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parents[3]
REVIEW = Path(__file__).resolve().parent
LEDGER_EP03 = REVIEW / "ledger" / "element_proof_agent_03.csv"
LEDGER_R07 = REVIEW / "ledger" / "remediation_r07.csv"
NETWORK_JSON = ROOT / "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json"
ENRICH_DIRS = [
    ROOT / "_neo4j/intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results",
    ROOT / "_neo4j/intake/inbox/research/bauteilboersen_deep_enrichment_results",
    ROOT / "_neo4j/intake/inbox/research/bauteilboersen_finalest_verified_reuse_evidence_2026-05-31"
    / "bauteilboersen_finalest_verified_reuse_evidence_2026-05-31/json_per_actor",
]
OUT_CSV = REVIEW / "ledger" / "provenance_g02.csv"
OUT_MD = REVIEW / "reports" / "provenance_g02.md"

REL_TYPES = {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"}

ORIGIN_RULES = [
    ("enrichment_import_2026_06_02", "bauteilboerse_actor_enrichment_import_2026_06_02", "_neo4j/intake/runs/2026-06-02_bauteilboerse_actor_enrichment_import/_run_import_actor_enrichment_edges.py"),
    ("deep_enrichment_slice", "actor_edge_enrichment_deep_existing_types_2026_06_01", "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json"),
    ("existing_types_slice", "actor_edge_enrichment_existing_types_2026_06_01", "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json"),
    ("deeper_node_types_slice", "edge_enrichment_deeper_existing_node_types_2026_06_01", "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json"),
    ("finalest_30_strict", "bauteilboersen_finalest_30_2026_05_31", "_neo4j/intake/runs/2026-05-31_bauteilboersen_finalest_30/RUN_MIGRATION.cypher"),
    ("schema_compatible_2026_06_01", "schema_compatible_bauteilboersen_update_2026_06_01", "_neo4j/intake/inbox/research/FINAL_schema_compatible_bauteilboersen_update_2026-06-01/final_schema_compatible_bauteilboersen_update_2026-06-01/cypher/IMPORT_SCHEMA_COMPATIBLE_BAUTEILBOERSEN.cypher"),
    ("deeper_material_draft_cypher", "GRAPH_IMPORT_CYPHER_REVIEW_ONLY", "_neo4j/intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results/GRAPH_IMPORT_CYPHER_REVIEW_ONLY.cypher"),
]


def read_password() -> str:
    for line in (ROOT / ".neo4j_password").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    raise RuntimeError("no password")


def git_oneline(path: str) -> str:
    rel = path.replace("\\", "/")
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%h %cs %s", "--", rel],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return out or "no git history"
    except subprocess.CalledProcessError:
        return "no git history"


def load_partial_ep03() -> list[dict]:
    rows = []
    with LEDGER_EP03.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("verdict") == "PARTIAL" and row.get("rel_type_or_label") in REL_TYPES:
                rows.append(row)
    return rows


def load_r07_index() -> dict[tuple, dict]:
    idx = {}
    with LEDGER_R07.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["rel_type_or_label"], row["from_id"], row["to_id"])
            idx[key] = row
    return idx


def load_network_index() -> dict[str, dict]:
    data = json.loads(NETWORK_JSON.read_text(encoding="utf-8"))
    node_lookup = {n["elementId"]: n["properties"].get("id") for n in data["nodes"]}
    by_rel_id: dict[str, dict] = {}
    by_triple: dict[tuple, dict] = {}
    for e in data.get("edges", []):
        if e["type"] not in REL_TYPES:
            continue
        props = e.get("properties") or {}
        src = node_lookup.get(e["source"])
        tgt = node_lookup.get(e["target"])
        rec = {
            "rel_id": props.get("id", ""),
            "type": e["type"],
            "src": src,
            "tgt": tgt,
            "evidence_url": props.get("evidence_url"),
            "evidence_quote": props.get("evidence_quote"),
            "enrichment_run": props.get("enrichment_run"),
            "evidence_basis": props.get("evidence_basis"),
        }
        if rec["rel_id"]:
            by_rel_id[rec["rel_id"]] = rec
        if src and tgt:
            by_triple[(e["type"], src, tgt)] = rec
    return {"by_rel_id": by_rel_id, "by_triple": by_triple}


def load_enrichment_index() -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for base in ENRICH_DIRS:
        if not base.exists():
            continue
        for p in base.glob("*.json"):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if not isinstance(data, dict):
                continue
            aid = data.get("anchor_id") or p.stem.split(".")[0]
            idx[aid] = data
    return idx


def dossier_item(enrich: dict, rel: str, to_id: str) -> dict | None:
    key = "bauteiltypen" if rel == "HAT_BAUTEILTYP" else "materials"
    for item in enrich.get(key, []):
        if item.get("target_id") == to_id:
            return item
    return None


def classify_origin(rel_id: str, graph: dict, network: dict | None) -> tuple[str, str, str]:
    """Return (origin_run, origin_script, origin_notes)."""
    review_run = graph.get("review_run") or ""
    enrichment_run = graph.get("enrichment_run") or ""
    import_slice = graph.get("import_source_slice") or ""

    if review_run == "bauteilboerse_actor_enrichment_import_2026_06_02":
        return (
            "2026-06-02_bauteilboerse_actor_enrichment_import",
            "_neo4j/intake/runs/2026-06-02_bauteilboerse_actor_enrichment_import/_run_import_actor_enrichment_edges.py",
            f"import_source_slice={import_slice or enrichment_run}; sets evidence_url, not evidence_quote",
        )
    if review_run == "bauteilboersen_finalest_30_2026_05_31":
        return (
            "2026-05-31_bauteilboersen_finalest_30",
            "_neo4j/intake/runs/2026-05-31_bauteilboersen_finalest_30/RUN_MIGRATION.cypher",
            "pass8 strict STEPs 6A/6B; evidence_basis only on create",
        )
    if review_run == "schema_compatible_bauteilboersen_update_2026_06_01":
        return (
            "FINAL_schema_compatible_bauteilboersen_update_2026-06-01",
            "_neo4j/intake/inbox/research/FINAL_schema_compatible_bauteilboersen_update_2026-06-01/.../IMPORT_SCHEMA_COMPATIBLE_BAUTEILBOERSEN.cypher",
            "CSV strict import with evidence_url + evidence_quote",
        )
    if rel_id.startswith("r_deep_"):
        return (
            "network_json deep enrichment slice (pre-2026-06-02 import)",
            "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json",
            "enrichment_run=actor_edge_enrichment_deep_existing_types_2026_06_01",
        )
    if rel_id.startswith("r_deeper_"):
        return (
            "network_json deeper node-types slice",
            "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json",
            "enrichment_run=edge_enrichment_deeper_existing_node_types_2026_06_01",
        )
    if network and network.get("enrichment_run"):
        return (
            f"network_json slice {network['enrichment_run']}",
            "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json",
            "edge row in project_part_actor_edges export",
        )
    if not review_run and not enrichment_run and graph.get("confidence") == 0.9:
        return (
            "baseline bauteilboerse network catalogue merge (untagged)",
            "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json",
            "rel_id r_{actor}__ pattern; no enrichment_run; legacy confidence=0.9; no evidence_url/quote on graph",
        )
    if review_run in ("remediation_r07_2026_06_06", "quality_pass_q04_2026_06_06"):
        return (
            f"post-verification patch ({review_run})",
            "_neo4j/review/2026-06-06_full_graph_verification/_agent_r07_work/remediate_r07.py",
            "R07/Q04 remediation — not original intake",
        )
    return (
        "unknown / multi-hop",
        "",
        f"review_run={review_run!r} enrichment_run={enrichment_run!r} rel_id={rel_id!r}",
    )


def fetch_graph(driver, element_ids: list[str]) -> dict[str, dict]:
    q = """
    UNWIND $ids AS eid
    MATCH ()-[r]->()
    WHERE elementId(r) = eid
    MATCH (a)-[r]->(t)
    RETURN elementId(r) AS element_id,
           a.id AS from_id, type(r) AS rel_type, t.id AS to_id,
           coalesce(r.id,'') AS rel_id,
           r.review_run AS review_run,
           r.enrichment_run AS enrichment_run,
           r.import_source_slice AS import_source_slice,
           r.import_source_file AS import_source_file,
           r.evidence_url AS evidence_url,
           r.evidence_quote AS evidence_quote,
           r.evidence_basis AS evidence_basis,
           r.evidence_confidence AS evidence_confidence,
           r.confidence AS confidence
    """
    out = {}
    with driver.session(database="mit-bestand") as session:
        for row in session.run(q, ids=element_ids):
            out[row["element_id"]] = dict(row)
    return out


def main() -> None:
    partial = load_partial_ep03()
    r07_idx = load_r07_index()
    net = load_network_index()
    enrich_idx = load_enrichment_index()

    pw = read_password()
    driver = GraphDatabase.driver("neo4j://127.0.0.1:7687", auth=("neo4j", pw))
    try:
        graph = fetch_graph(driver, [r["element_id"] for r in partial])
    finally:
        driver.close()

    fieldnames = [
        "g02_id", "ep03_claim_id", "r07_claim_id", "element_id", "from_id", "to_id", "rel_type",
        "ep03_verdict", "r07_verdict", "basis_ref", "graph_evidence_url", "graph_evidence_quote",
        "graph_review_run", "graph_rel_id", "origin_intake_run", "origin_script_path",
        "origin_git_head", "network_json_evidence_url", "network_json_evidence_quote",
        "network_enrichment_run", "enrichment_json_path", "enrichment_evidence_url",
        "enrichment_evidence_quote", "r07_recovery_source", "r07_notes", "weak_evidence_class", "provenance_notes",
    ]

    rows_out = []
    origin_counts: Counter = Counter()
    weak_class: Counter = Counter()

    for i, ep in enumerate(partial, 1):
        eid = ep["element_id"]
        g = graph.get(eid, {})
        fid, tid, rt = ep["from_id"], ep["to_id"], ep["rel_type_or_label"]
        rel_id = g.get("rel_id", "")
        net_row = net["by_rel_id"].get(rel_id) or net["by_triple"].get((rt, fid, tid))
        r07 = r07_idx.get((rt, fid, tid), {})
        enrich = enrich_idx.get(fid, {})
        ditem = dossier_item(enrich, rt, tid) if enrich else None

        origin_run, origin_script, origin_notes = classify_origin(rel_id, g, net_row)
        origin_counts[origin_run] += 1

        if not g.get("evidence_url") and not g.get("evidence_quote"):
            if net_row and net_row.get("evidence_url") and not net_row.get("evidence_quote"):
                wc = "url_in_json_no_quote_never_imported_to_graph"
            elif origin_run.startswith("2026-06-02"):
                wc = "url_imported_no_quote_by_enrichment_importer"
            elif g.get("confidence") == 0.9:
                wc = "baseline_merge_confidence_only_no_url_no_quote"
            else:
                wc = "no_url_no_quote_other"
        elif g.get("evidence_url") and not g.get("evidence_quote"):
            wc = "graph_has_url_no_quote"
        else:
            wc = "partial_despite_some_evidence"
        weak_class[wc] += 1

        enrich_path = ""
        if ditem:
            for base in ENRICH_DIRS:
                for pat in (f"{fid}.enrichment.json", f"{fid}.finalest.evidence.json"):
                    p = base / pat
                    if p.exists():
                        enrich_path = str(p.relative_to(ROOT)).replace("\\", "/")
                        break

        rows_out.append({
            "g02_id": f"G02-{i:04d}",
            "ep03_claim_id": ep.get("claim_id", ""),
            "r07_claim_id": r07.get("claim_id", ""),
            "element_id": eid,
            "from_id": fid,
            "to_id": tid,
            "rel_type": rt,
            "ep03_verdict": ep.get("verdict", ""),
            "r07_verdict": r07.get("verdict", ""),
            "basis_ref": ep.get("basis_ref", ""),
            "graph_evidence_url": g.get("evidence_url") or "",
            "graph_evidence_quote": g.get("evidence_quote") or "",
            "graph_review_run": g.get("review_run") or "",
            "graph_rel_id": rel_id,
            "origin_intake_run": origin_run,
            "origin_script_path": origin_script,
            "origin_git_head": git_oneline(origin_script) if origin_script else "",
            "network_json_evidence_url": (net_row or {}).get("evidence_url") or "",
            "network_json_evidence_quote": (net_row or {}).get("evidence_quote") or "",
            "network_enrichment_run": (net_row or {}).get("enrichment_run") or "",
            "enrichment_json_path": enrich_path,
            "enrichment_evidence_url": ";".join((ditem or {}).get("evidence_urls") or []),
            "enrichment_evidence_quote": (ditem or {}).get("evidence_quote") or "",
            "r07_recovery_source": (r07.get("notes") or "").split(";")[0].replace("recovery=", ""),
            "r07_notes": r07.get("notes", ""),
            "weak_evidence_class": wc,
            "provenance_notes": origin_notes,
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows_out)

    # Report
    git_lines = []
    for _, _, script in ORIGIN_RULES:
        git_lines.append(f"- `{script}` — {git_oneline(script)}")

    md = f"""# Provenance report — Agent G2 (catalogue-edge PARTIAL backlog)

**Date:** 2026-06-06 · **Database:** `mit-bestand`  
**Ledger:** [`ledger/provenance_g02.csv`](../ledger/provenance_g02.csv)  
**Scope:** EP-03 / R07 / Q04 actor catalogue edges — `HAT_BAUTEILTYP` + `NUTZT_MATERIAL` with verdict **PARTIAL**

## Summary

| Metric | Count |
|---|---:|
| PARTIAL rows (EP-03 ledger) | **{len(partial)}** |
| HAT_BAUTEILTYP | **{sum(1 for r in partial if r['rel_type_or_label']=='HAT_BAUTEILTYP')}** |
| NUTZT_MATERIAL | **{sum(1 for r in partial if r['rel_type_or_label']=='NUTZT_MATERIAL')}** |
| Matched in remediation_r07.csv | **{sum(1 for r in rows_out if r['r07_claim_id'])}** |
| R07 recovery via actor homepage (`actor_node_source_urls`) | **{sum(1 for r in rows_out if 'actor_node_source_urls' in r['r07_notes'])}** |
| R07 recovery via enrichment JSON | **{sum(1 for r in rows_out if 'bauteilboersen_enrichment_json' in r['r07_notes'])}** |

## Root cause — which intake created weak `evidence_url` without quotes

**Primary creator (url without quote on graph):**  
[`_neo4j/intake/runs/2026-06-02_bauteilboerse_actor_enrichment_import/_run_import_actor_enrichment_edges.py`](../../intake/runs/2026-06-02_bauteilboerse_actor_enrichment_import/_run_import_actor_enrichment_edges.py)

That importer MERGEs 383 edges from [`bauteilboerse_network_2026-06-01_project_part_actor_edges.json`](../../intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json) and **writes `evidence_url` + `evidence_basis` but never `evidence_quote`**. It tags `review_status=needs_source_url_review` by design.

**Larger untagged backlog (no url, no quote):**  
239 live Akteur catalogue edges still carry legacy `confidence=0.9`, null `review_run`, and **no** `evidence_url` / `evidence_quote`. These use `rel_id` pattern `r_{{actor}}__HAT_BAUTEILTYP__{{bt}}` from the same network JSON rows **without** `enrichment_run` (460-edge baseline catalogue slice). They predate the June enrichment import and were merged without evidence properties.

**Draft-only / not the live weak-url source:**  
[`GRAPH_IMPORT_CYPHER_REVIEW_ONLY.cypher`](../../intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results/GRAPH_IMPORT_CYPHER_REVIEW_ONLY.cypher) documents URLs in comments but MERGE uses only `{{confidence:'belegt'}}` — review-only; enrichment JSON is the recoverable quote reservoir.

**Strict counterexample (has quotes):**  
[`IMPORT_SCHEMA_COMPATIBLE_BAUTEILBOERSEN.cypher`](../../intake/inbox/research/FINAL_schema_compatible_bauteilboersen_update_2026-06-01/final_schema_compatible_bauteilboersen_update_2026-06-01/cypher/IMPORT_SCHEMA_COMPATIBLE_BAUTEILBOERSEN.cypher) sets both `evidence_url` and `evidence_quote` from CSV.

## Origin class distribution (143 PARTIAL rows)

| Origin intake / class | Rows |
|---|---:|
"""
    for k, v in origin_counts.most_common():
        md += f"| {k} | {v} |\n"

    md += """
## Weak evidence class

| Class | Rows |
|---|---:|
"""
    for k, v in weak_class.most_common():
        md += f"| {k} | {v} |\n"

    md += """
## Git provenance (head commit per artefact)

"""
    md += "\n".join(git_lines)

    md += """

## Remediation trace (R07 → EP-03)

1. Agent 14 `needs_source_url_review` backlog → **R07** ([`ledger/remediation_r07.csv`](../ledger/remediation_r07.csv)): 145 catalogue edges in scope; **143** remain PARTIAL after fetch.
2. R07 applied **137** `ADD_SOURCE` patches ([`patches/remediation_r07_add_rel_sources.patch.jsonl`](../patches/remediation_r07_add_rel_sources.patch.jsonl)) with `review_run=remediation_r07_2026_06_06`.
3. EP-03 element proof re-adjudicated the same 143 as PARTIAL ([`ledger/element_proof_agent_03.csv`](../ledger/element_proof_agent_03.csv)); Q04 later downgraded 13 overlapping rows to `evidence_confidence=niedrig` ([`ledger/post_quality_p06_01.csv`](../ledger/post_quality_p06_01.csv)).

## Enrichment JSON crosswalk

Per-actor `*.enrichment.json` under [`bauteilboersen_deeper_material_bauteiltyp_results`](../../intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results/) holds recoverable `evidence_urls` + `evidence_quote` for many actors. R07 used these where dossier rows exist; **137/143** PARTIAL rows fell back to **actor `primary_source_url` / `source_urls`** (homepage), which fails the strict verbatim quote gate.

## Recommended recovery order

1. Re-import quotes from matching `*.enrichment.json` / `*.finalest.evidence.json` where `target_id` matches.
2. For `r_deep_*` / baseline `confidence=0.9` rows, either prove from enrichment dossier or delete (Q04 pattern).
3. Do not treat `2026-06-02` importer `evidence_url`-only edges as PROVEN without adding `evidence_quote`.
"""
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"Wrote {len(rows_out)} rows -> {OUT_CSV}")
    print(f"Wrote report -> {OUT_MD}")
    print("Origin:", dict(origin_counts.most_common(5)))
    print("Weak class:", dict(weak_class.most_common(5)))


if __name__ == "__main__":
    main()
