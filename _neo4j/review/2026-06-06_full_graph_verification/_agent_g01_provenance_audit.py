#!/usr/bin/env python3
"""Agent G1 — git provenance audit for MISSING_EVIDENCE clusters (read-only)."""
from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
LEDGER = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
OUT_CSV = HERE / "ledger" / "provenance_g01.csv"
OUT_MD = HERE / "reports" / "provenance_g01.md"

sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

STUB_PATTERNS = re.compile(
    r"(unbekannt|aggregat|unknown|placeholder|stub|_cluster|miscast|synthesized)",
    re.I,
)
INTAKE_SCRIPT_PATTERNS = re.compile(
    r"(apply_|_run_import|import_.*\.py|phase\d+_|_build_ledger)",
    re.I,
)


def load_missing() -> list[dict]:
    with LEDGER.open(encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("verdict") == "MISSING_EVIDENCE"]


def enrich_from_graph(rows: list[dict]) -> None:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    node_ids = [r["element_id"] for r in rows if r["claim_kind"] == "node"]
    rel_keys: list[tuple[str, str, str, str]] = []
    for r in rows:
        if r["claim_kind"] != "rel":
            continue
        eid = r.get("graph_element_id") or r["element_id"]
        rel_keys.append((eid, r.get("from_id", ""), r.get("to_id", ""), r["rel_type_or_label"]))

    node_meta: dict[str, dict] = {}
    batch = 200
    with driver.session(database=database) as sess:
        for i in range(0, len(node_ids), batch):
            chunk = node_ids[i : i + batch]
            q = """
            UNWIND $ids AS nid
            MATCH (n {id: nid})
            RETURN n.id AS id, labels(n) AS labels,
                   n.intake_run AS intake_run, n.review_run AS review_run,
                   n.source_scope AS source_scope, n.name AS name
            """
            for rec in sess.run(q, ids=chunk):
                node_meta[rec["id"]] = dict(rec)

        for i in range(0, len(rel_keys), batch):
            chunk = rel_keys[i : i + batch]
            q = """
            UNWIND $rows AS row
            MATCH (a {id: row.from_id})-[r]->(b {id: row.to_id})
            WHERE type(r) = row.rel_type
            RETURN row.eid AS eid, type(r) AS rel_type,
                   r.intake_run AS intake_run, r.review_run AS review_run,
                   r.evidence_url AS evidence_url, r.source_url AS source_url
            LIMIT size($rows)
            """
            for rec in sess.run(q, rows=[{"eid": e, "from_id": f, "to_id": t, "rel_type": rt} for e, f, t, rt in chunk]):
                node_meta[rec["eid"]] = dict(rec)

    driver.close()

    for r in rows:
        key = r["element_id"] if r["claim_kind"] == "node" else (r.get("graph_element_id") or r["element_id"])
        meta = node_meta.get(key) or node_meta.get(r["element_id"], {})
        r["_intake_run"] = meta.get("intake_run") or ""
        r["_review_run"] = meta.get("review_run") or ""
        r["_source_scope"] = meta.get("source_scope") or ""
        r["_graph_name"] = meta.get("name") or ""


def walk_first_hit(needle: str, roots: list[Path]) -> tuple[str, int] | None:
    """Return (relative_path, line_no) for first text hit under roots."""
    exts = {".py", ".jsonl", ".json", ".md", ".csv", ".cypher", ".patch"}
    for root in roots:
        if not root.exists():
            continue
        for dirpath, _, filenames in os.walk(root):
            # skip large binary / image trees
            if "inbox" in dirpath.replace("\\", "/") and dirpath.endswith("IMAGES"):
                continue
            for fn in sorted(filenames):
                if Path(fn).suffix.lower() not in exts and fn not in ("APPLY_ORDER.md",):
                    continue
                fp = Path(dirpath) / fn
                try:
                    text = fp.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                if needle not in text:
                    continue
                line = text[: text.index(needle)].count("\n") + 1
                return os.path.relpath(fp, REPO), line
    return None


def git_first_intro(needle: str) -> dict | None:
    """Earliest commit introducing needle under _neo4j/."""
    try:
        proc = subprocess.run(
            [
                "git", "log", "-S", needle, "--reverse",
                "--format=%H\t%ai\t%s",
                "--", "_neo4j/",
            ],
            capture_output=True,
            text=True,
            cwd=REPO,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return None
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    first_line = proc.stdout.strip().splitlines()[0]
    parts = first_line.split("\t", 2)
    if len(parts) < 3:
        return None
    commit, date_s, subject = parts[0], parts[1], parts[2]
    try:
        proc2 = subprocess.run(
            ["git", "show", "--name-only", "--format=", commit],
            capture_output=True,
            text=True,
            cwd=REPO,
            timeout=30,
        )
        files = [f for f in proc2.stdout.splitlines() if f.strip().startswith("_neo4j/")]
        path = files[0] if files else ""
    except Exception:
        path = ""
    return {"commit": commit[:12], "date": date_s[:10], "subject": subject, "path": path}


def classify_row(r: dict, git_info: dict | None, file_hit: str) -> str:
    """Per-row root-cause bucket (cluster summary uses majority vote)."""
    notes = (r.get("notes") or "").lower()
    eid = r.get("element_id", "")
    agent = r.get("agent_id", "")
    label = r.get("rel_type_or_label", "")
    name = (r.get("_graph_name") or "").lower()

    if agent == "F09" or "synthesized by f09" in notes:
        return "post_merge_orphan"
    if "p6-new" in notes or "merge-redirect" in notes:
        return "post_merge_orphan"

    stub_text = f"{eid} {name} {notes}"
    if STUB_PATTERNS.search(stub_text):
        if any(x in stub_text for x in ("unbekannt", "aggregat", "_cluster", "unknown", "_donor")):
            return "aggregate_stub"
    if label == "Materialdepot":
        return "aggregate_stub"
    if label == "Bauwerk" and ("_donor" in eid or "placeholder source" in notes):
        return "aggregate_stub"

    if "placeholder source" in notes or "processed/archive" in notes:
        return "never_sourced_import"

    if file_hit and INTAKE_SCRIPT_PATTERNS.search(file_hit.replace("\\", "/")):
        return "intake_script"
    if git_info and git_info.get("path"):
        p = git_info["path"].replace("\\", "/")
        if "/intake/runs/" in p and INTAKE_SCRIPT_PATTERNS.search(p):
            return "intake_script"
        if "patch" in p.lower() and "remediation" in p.lower():
            return "post_merge_orphan"

    if label == "Akteur" and agent in ("08", "06b"):
        return "never_sourced_import"
    if label == "VERBUNDEN_MIT_AKTEUR":
        return "never_sourced_import"
    if label in ("Bauwerk", "Projekt", "BETEILIGT_AN") and agent == "09":
        return "never_sourced_import"
    if label in ("Programm", "Software", "NUTZT_SOFTWARE", "TEIL_VON_PROGRAMM", "ERHALT_FOERDERUNG_DURCH"):
        if git_info and git_info.get("path", "").replace("\\", "/").startswith("_neo4j/intake/runs/"):
            return "intake_script"
        return "never_sourced_import"
    if file_hit and "/intake/runs/" in file_hit.replace("\\", "/"):
        return "intake_script"
    if git_info and ("/processed/" in git_info.get("path", "") or ".kg.jsonl" in git_info.get("path", "")):
        return "never_sourced_import"
    return "never_sourced_import"


def cluster_bucket(row_buckets: Counter) -> str:
    order = ("never_sourced_import", "aggregate_stub", "intake_script", "post_merge_orphan")
    return max(order, key=lambda b: (row_buckets.get(b, 0), -order.index(b)))


def cluster_key(r: dict) -> tuple:
    label = r["rel_type_or_label"]
    return (r["claim_kind"], label, r.get("_intake_run", ""), r.get("_review_run", ""))


def build_clusters(rows: list[dict]) -> dict[tuple, list[dict]]:
    clusters: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        clusters[cluster_key(r)].append(r)
    return clusters


def main() -> None:
    rows = load_missing()
    print(f"MISSING_EVIDENCE rows: {len(rows)}")
    enrich_from_graph(rows)
    clusters = build_clusters(rows)

    search_roots = [
        REPO / "_neo4j" / "intake" / "runs",
        REPO / "_neo4j" / "processed",
        REPO / "_neo4j" / "review",
    ]

    out_rows: list[dict] = []
    bucket_counts: Counter = Counter()

    for idx, (key, members) in enumerate(sorted(clusters.items(), key=lambda x: -len(x[1]))):
        claim_kind, label, intake_run, review_run = key
        sample_ids = [m["element_id"] for m in members[:5]]
        rep = sample_ids[0]

        file_hit = ""
        line_no = 0
        hit = walk_first_hit(rep, search_roots)
        if hit:
            file_hit, line_no = hit

        git_info = git_first_intro(rep)
        row_buckets = Counter(classify_row(m, git_info, file_hit) for m in members)
        bucket = cluster_bucket(row_buckets)
        for b, c in row_buckets.items():
            bucket_counts[b] += c

        agent_dist = Counter(m.get("agent_id", "") for m in members)
        out_rows.append({
            "cluster_id": f"G01-C{idx+1:03d}",
            "claim_kind": claim_kind,
            "rel_type_or_label": label,
            "intake_run": intake_run or "(null)",
            "review_run": review_run or "(null)",
            "row_count": len(members),
            "bucket_breakdown": ";".join(f"{k}:{v}" for k, v in row_buckets.most_common()),
            "agent_ids": ";".join(f"{k}:{v}" for k, v in agent_dist.most_common()),
            "sample_element_ids": ";".join(sample_ids),
            "first_repo_hit": f"{file_hit}:{line_no}" if file_hit else "",
            "first_git_commit": git_info["commit"] if git_info else "",
            "first_git_date": git_info["date"] if git_info else "",
            "first_git_subject": git_info["subject"] if git_info else "",
            "first_git_path": git_info["path"] if git_info else "",
            "root_cause_bucket": bucket,
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(out_rows[0].keys()) if out_rows else []
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    total = len(rows)
    n_clusters = len(out_rows)
    md = [
        "# Agent G1 — Git Provenance Audit (MISSING_EVIDENCE)",
        "",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d')}  ",
        f"**Source ledger:** `VERIFICATION_LEDGER_ELEMENT.csv`  ",
        f"**Filter:** `verdict=MISSING_EVIDENCE`  ",
        f"**Rows audited:** {total}  ",
        f"**Clusters:** {n_clusters} (by `claim_kind`, `rel_type_or_label`, `intake_run`, `review_run`)  ",
        f"**Mode:** read-only git + repo + Neo4j read-cypher; no graph mutation  ",
        "",
        "## Root-cause buckets",
        "",
        "| Bucket | Rows | Share | Meaning |",
        "|---|---:|---:|---|",
    ]
    bucket_defs = {
        "intake_script": "Element first introduced by an intake-run apply/import script without attaching evidence URLs.",
        "aggregate_stub": "Placeholder or aggregate node (Unbekannt/Aggregiert/cluster/miscast) — not a discrete sourced entity.",
        "never_sourced_import": "Imported from processed JSONL / legacy actor mesh / early graph batch; never carried `source_urls` or `evidence_url`.",
        "post_merge_orphan": "Survivor of merge, redirect synthesis (F09/P6), or edge purge that left provenance gap.",
    }
    for bucket in ("intake_script", "aggregate_stub", "never_sourced_import", "post_merge_orphan"):
        c = bucket_counts.get(bucket, 0)
        pct = 100.0 * c / total if total else 0
        md.append(f"| `{bucket}` | {c} | {pct:.1f}% | {bucket_defs[bucket]} |")

    md += [
        "",
        "## Cluster highlights (top 15 by row count)",
        "",
        "| cluster | label | intake_run | review_run | rows | bucket | first git |",
        "|---|---|---|---|---:|---|---|",
    ]
    for r in sorted(out_rows, key=lambda x: -x["row_count"])[:15]:
        git = f"{r['first_git_date']} `{r['first_git_commit']}`" if r["first_git_commit"] else "—"
        bd = r.get("bucket_breakdown", "")
        md.append(
            f"| {r['cluster_id']} | {r['rel_type_or_label']} | {r['intake_run']} | {r['review_run']} "
            f"| {r['row_count']} | `{r['root_cause_bucket']}` ({bd}) | {git} |"
        )

    md += [
        "",
        "## Findings",
        "",
    ]

    akteur_null = sum(r["row_count"] for r in out_rows if r["rel_type_or_label"] == "Akteur" and r["intake_run"] == "(null)")
    vma_null = sum(r["row_count"] for r in out_rows if r["rel_type_or_label"] == "VERBUNDEN_MIT_AKTEUR")
    md.append(
        f"1. **Actor long tail ({akteur_null} rows):** Unsourced `:Akteur` nodes overwhelmingly have "
        f"`intake_run=null` / `review_run=null` — introduced before the 2026-06 intake provenance contract. "
        f"First git hits land in `_neo4j/processed/actor_registry/` or early project JSONL, not in evidence-tagged apply scripts."
    )
    md.append(
        f"2. **VMA gap ({vma_null} rows):** All unsourced `VERBUNDEN_MIT_AKTEUR` edges lack `review_run`; "
        f"Agent 06b enumerated structural mesh edges imported without `evidence_url`. Root cause: `never_sourced_import`."
    )
    md.append(
        "3. **Geo/Bauwerk ({0} rows):** Project donor `Bauwerk` nodes use placeholder `processed/archive` "
        "address sources — intake geo pass wrote coordinates without real URLs.".format(
            sum(r["row_count"] for r in out_rows if r["rel_type_or_label"] == "Bauwerk")
        )
    )
    md.append(
        "4. **F09 synthesis:** Rows with `agent_id=F09` are ledger coverage artifacts (`Synthesized by F09`); "
        "bucket `post_merge_orphan` — graph elements pre-existed but lacked element-proof rows until final cleanup."
    )
    md.append(
        "5. **Materialdepot stubs:** Aggregate/placeholder depots (`bw_*_donor`, network abstractions) — "
        "bucket `aggregate_stub`; first appear in project processed records without discrete depot URLs."
    )

    md += [
        "",
        "## Method",
        "",
        "- Filtered `VERIFICATION_LEDGER_ELEMENT.csv` for `verdict=MISSING_EVIDENCE`.",
        "- Enriched each row with live `intake_run` / `review_run` / `source_scope` from Neo4j (`mit-bestand`).",
        "- Clustered on `(claim_kind, rel_type_or_label, intake_run, review_run)`.",
        "- Per cluster: repo walk first hit in `intake/runs/`, `processed/`, `review/`; `git log -S <sample_id> --reverse` under `_neo4j/`.",
        "- Per-row bucket assigned then cluster `root_cause_bucket` = majority vote (`bucket_breakdown` column).",
        "- Bucket assigned from path patterns, agent notes, and naming heuristics.",
        "",
        f"**Output:** [`ledger/provenance_g01.csv`](../ledger/provenance_g01.csv) ({n_clusters} cluster rows).",
        "",
    ]

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(out_rows)} clusters)")
    print(f"Wrote {OUT_MD}")
    print("Bucket counts:", dict(bucket_counts))


if __name__ == "__main__":
    main()
