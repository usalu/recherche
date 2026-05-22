"""Agent G5: git provenance for SCHEMA_VIOLATION rows in final ledger."""
from __future__ import annotations

import csv
import json
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2].parent  # repo root (e:/recherche)
REVIEW = Path(__file__).resolve().parent
LEDGER = REVIEW / "VERIFICATION_LEDGER_ELEMENT.csv"
OUT_CSV = REVIEW / "ledger" / "provenance_g05.csv"

GLOBS = ["*.jsonl", "*.csv", "*.py", "*.cypher", "*.patch.jsonl", "*.md"]


def run(cmd: list[str]) -> str:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=120)
        return (p.stdout or "").strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return ""


def first_pickaxe(needle: str) -> dict:
    cmd = ["git", "log", "--reverse", "--format=%H|%ai|%an|%s", "-S", needle, "--all", "--", *GLOBS]
    lines = [l for l in run(cmd).split("\n") if l]
    if not lines:
        cmd2 = ["git", "log", "--reverse", "--format=%H|%ai|%an|%s", "-S", needle, "--all"]
        lines = [l for l in run(cmd2).split("\n") if l]
    if not lines:
        return {}
    h, ai, an, subj = lines[0].split("|", 3)
    files = run(["git", "show", "--name-only", "--pretty=format:", h]).split("\n")
    files = [f for f in files if f.strip()][:8]
    return {
        "first_commit": h[:12],
        "first_date": ai[:10],
        "first_author": an,
        "first_subject": subj,
        "first_files": "; ".join(files),
    }


def files_containing(needle: str, limit: int = 5) -> str:
    if not needle:
        return ""
    out = run(["git", "grep", "-l", "-F", needle, "--", "_neo4j", "_scripts"])
    paths = [p for p in out.split("\n") if p.strip()][:limit]
    return "; ".join(paths)


def load_violations() -> list[dict]:
    rows = []
    with open(LEDGER, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("verdict") == "SCHEMA_VIOLATION":
                rows.append(row)
    return rows


def classify(row: dict) -> str:
    cid = row["claim_id"]
    rel = row.get("rel_type_or_label") or row.get("rel_type") or ""
    if cid.startswith("A14-ORPH"):
        return "orphan_actor"
    if cid.startswith("A06B-node"):
        return "duplicate_actor"
    if cid.startswith("A10-N-"):
        return "generic_programm_vocab"
    if cid.startswith("A12-rel"):
        return "stadt_zuerich_domain"
    if cid == "A10-R-047":
        return "software_self_wiring"
    if cid.startswith("A10-R-") and "TEIL_VON_PROGRAMM" in rel:
        return "teil_von_generic_programm"
    return "other"


def origin_pipeline(vclass: str) -> str:
    mapping = {
        "orphan_actor": "reuse_bubble_actor_import",
        "duplicate_actor": "actor_registry_mesh",
        "generic_programm_vocab": "project_vocab_seed",
        "stadt_zuerich_domain": "geo_project_import+phase_r_backfill",
        "software_self_wiring": "project_vocab_controlled_terms",
        "teil_von_generic_programm": "project_batch_import",
    }
    return mapping.get(vclass, "unknown")


def main() -> None:
    rows = load_violations()
    out_rows = []
    for i, row in enumerate(rows, 1):
        fid = row.get("from_id") or ""
        tid = row.get("to_id") or ""
        eid = row.get("element_id") or ""
        rel = row.get("rel_type_or_label") if row.get("claim_kind") == "rel" else ""
        if not rel:
            rel = row.get("rel_type") or ""
        kind = row.get("element_kind") or row.get("claim_kind") or ""
        if kind == "node" and not fid:
            fid = eid
        vclass = classify(row)
        needles = []
        if fid:
            needles.append(fid)
        if tid:
            needles.append(tid)
        if rel and fid and tid:
            needles.append(f"r_{fid}__{rel}__{tid}")
        git = {}
        for n in needles:
            git = first_pickaxe(n)
            if git:
                break
        live_files = files_containing(needles[0]) if needles else ""
        out_rows.append(
            {
                "g05_id": f"G05-{i:03d}",
                "claim_id": row["claim_id"],
                "element_kind": kind,
                "from_id": fid,
                "to_id": tid,
                "rel_type": rel,
                "violation_class": vclass,
                "origin_pipeline": origin_pipeline(vclass),
                "ledger_verdict": row.get("verdict", ""),
                "ledger_action": row.get("proposed_action", ""),
                "ledger_agent": row.get("agent_id", ""),
                "git_first_commit": git.get("first_commit", ""),
                "git_first_date": git.get("first_date", ""),
                "git_first_author": git.get("first_author", ""),
                "git_first_subject": git.get("first_subject", ""),
                "git_first_files": git.get("first_files", ""),
                "repo_files_now": live_files,
                "notes": (row.get("notes") or "")[:200],
            }
        )
    fieldnames = list(out_rows[0].keys()) if out_rows else []
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)
    print(f"Wrote {len(out_rows)} rows to {OUT_CSV}")
    summary = defaultdict(int)
    for r in out_rows:
        summary[r["violation_class"]] += 1
    print(json.dumps(dict(summary), indent=2))


if __name__ == "__main__":
    main()
