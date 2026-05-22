#!/usr/bin/env python3
"""BG-W2-04 — Merge W2 shards, emit patches, apply if clean, overlay v8 ledger."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

csv.field_size_limit(10_000_000)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
LEDGER = HERE / "ledger"
PATCHES = HERE / "patches"
REPORTS = HERE / "reports"
APPLY_REPORTS = HERE / "apply_reports"
APPLY_SCRIPT = SCRIPTS / "apply_neo4j_review_patch.py"
V7 = HERE / "VERIFICATION_LEDGER_ELEMENT_v7.csv"
V8 = HERE / "VERIFICATION_LEDGER_ELEMENT_v8.csv"
W1_PATCH = PATCHES / "bg_hunt_upgrades.patch.jsonl"

SHARDS = [
    ("BG-W2-01", "bg_hunt_w2_01.csv"),
    ("BG-W2-02", "bg_hunt_w2_02.csv"),
    ("BG-W2-03", "bg_hunt_w2_03.csv"),
]

OUT_MERGED = LEDGER / "bg_hunt_w2_merged.csv"
OUT_PATCH = PATCHES / "bg_hunt_upgrades_w2.patch.jsonl"
OUT_PATCH_ALL = PATCHES / "bg_hunt_upgrades_all.patch.jsonl"
OUT_REPORT = REPORTS / "BG_HUNT_W2_REPORT.md"
REVIEW_RUN = "bg_hunt_w2_2026_06_07"

V7_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
    "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
    "source_agent", "coverage_level", "graph_element_id", "match_status",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def load_shards() -> tuple[list[dict], dict[str, int], list[dict]]:
    merged: list[dict] = []
    stats: dict[str, int] = {}
    conflicts: list[dict] = []
    seen: dict[str, dict] = {}
    for agent, fname in SHARDS:
        path = LEDGER / fname
        if not path.is_file():
            raise FileNotFoundError(f"Missing shard {path}")
        rows = load_csv(path)
        stats[agent] = len(rows)
        for row in rows:
            geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
            if geid in seen:
                conflicts.append({"element_id": geid, "agents": [seen[geid].get("agent_id"), row.get("agent_id")]})
            else:
                seen[geid] = row
                merged.append(row)
    return merged, stats, conflicts


def emit_patches(rows: list[dict]) -> list[dict]:
    patches: list[dict] = []
    for row in rows:
        if row.get("proposed_action") != "UPGRADE" or row.get("verdict_after") != "PROVEN":
            continue
        basis = row.get("basis_ref", "")
        evidence_url = basis if str(basis).startswith("http") else ""
        props = {
            "evidence_quote": row.get("proof_quote", "")[:300],
            "evidence_confidence": "high" if row.get("confidence") == "belegt" else "medium",
            "evidence_basis": "bg_hunt_alias_match",
            "review_run": REVIEW_RUN,
        }
        if evidence_url:
            props["evidence_url"] = evidence_url
        if not props.get("evidence_quote"):
            continue
        patches.append({
            "op": "set_rel_properties",
            "from": row.get("from_id", ""),
            "type": row.get("rel_type_or_label", ""),
            "to": row.get("to_id", ""),
            "properties": props,
            "reason": f"BG hunt W2 upgrade {row.get('agent_id')} score={row.get('alias_score', '')} basis={basis[:80]}",
        })
    return patches


def dry_run_patch(patch_path: Path) -> dict:
    if not patch_path.is_file() or patch_path.stat().st_size == 0:
        return {"status": "empty", "returncode": 0, "missing_rel": 0, "stdout": "", "stderr": ""}
    cmd = [sys.executable, str(APPLY_SCRIPT), "--patch", str(patch_path), "--database", "mit-bestand"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO))
    ok = proc.returncode == 0
    missing = 0
    try:
        report_json = APPLY_REPORTS / f"{patch_path.name}.apply_report.json"
        if report_json.is_file():
            rep = json.loads(report_json.read_text(encoding="utf-8"))
            missing = rep.get("summary", {}).get("missing_rel", 0)
    except Exception:
        pass
    status = "ok" if ok and missing == 0 else ("partial" if ok else "error")
    return {"status": status, "returncode": proc.returncode, "missing_rel": missing, "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-2000:]}


def apply_patch(patch_path: Path) -> dict:
    if not patch_path.is_file() or patch_path.stat().st_size == 0:
        return {"status": "empty", "applied": 0}
    cmd = [
        sys.executable,
        str(APPLY_SCRIPT),
        "--patch",
        str(patch_path),
        "--database",
        "mit-bestand",
        "--confirm",
        f"APPLY {patch_path.name} TO mit-bestand",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO))
    report_json = APPLY_REPORTS / f"{patch_path.name}.apply_report.json"
    applied = 0
    counts = {}
    if report_json.is_file():
        rep = json.loads(report_json.read_text(encoding="utf-8"))
        applied = (
            rep.get("summary", {}).get("updated_rel", 0)
            or rep.get("summary", {}).get("would_update_rel", 0)
            or rep.get("summary", {}).get("applied_rel", 0)
        )
        counts = rep.get("counts", {})
    return {
        "status": "ok" if proc.returncode == 0 else "error",
        "returncode": proc.returncode,
        "applied": applied,
        "counts": counts,
    }


def overlay_v8(merged: list[dict]) -> tuple[list[dict], dict]:
    by_geid = {
        (r.get("graph_element_id") or r.get("element_id", "")).strip(): r
        for r in merged
        if r.get("graph_element_id") or r.get("element_id")
    }
    v7_rows = load_csv(V7)
    out_rows = []
    changes = Counter()
    for row in v7_rows:
        geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
        hunt = by_geid.get(geid)
        if hunt and hunt.get("verdict_after"):
            new = dict(row)
            old_v = row.get("verdict", "")
            new_v = hunt.get("verdict_after", old_v)
            if new_v != old_v:
                changes[f"{old_v}->{new_v}"] += 1
            new["verdict"] = new_v
            if hunt.get("proof_quote"):
                new["proof_quote"] = hunt["proof_quote"]
            if hunt.get("basis_ref") and str(hunt["basis_ref"]).startswith("http"):
                new["basis_ref"] = hunt["basis_ref"]
                new["fetched"] = hunt.get("fetched", "true")
                new["http_status"] = hunt.get("http_status", "")
            if hunt.get("evidence_basis"):
                new["notes"] = (row.get("notes", "") + f"; evidence_basis={hunt['evidence_basis']}").strip("; ")
            new["agent_id"] = hunt.get("agent_id", row.get("agent_id", ""))
            new["proposed_action"] = hunt.get("proposed_action", row.get("proposed_action", ""))
            out_rows.append(new)
        else:
            out_rows.append(row)

    bg_rows = [r for r in out_rows if r.get("claim_kind") == "rel" and (r.get("from_id", "").startswith("bg_") or r.get("to_id", "").startswith("bg_"))]
    proven = sum(1 for r in bg_rows if r.get("verdict") == "PROVEN")
    stats = {
        "total_rows": len(out_rows),
        "bg_rows": len(bg_rows),
        "bg_proven": proven,
        "bg_proven_pct": round(100 * proven / len(bg_rows), 2) if bg_rows else 0,
        "changes": dict(changes),
    }
    return out_rows, stats


def graph_counts() -> dict:
    sys.path.insert(0, str(SCRIPTS))
    from neo4j_env import resolve_connection
    from neo4j import GraphDatabase

    uri, user, password, _ = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session(database="mit-bestand") as session:
        nodes = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        rels = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    driver.close()
    return {"nodes": nodes, "relationships": rels}


def main() -> None:
    merged, shard_stats, conflicts = load_shards()
    OUT_MERGED.parent.mkdir(parents=True, exist_ok=True)
    PATCHES.mkdir(parents=True, exist_ok=True)

    hunt_cols = list(merged[0].keys()) if merged else []
    with OUT_MERGED.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=hunt_cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(merged)

    patches = emit_patches(merged)
    with OUT_PATCH.open("w", encoding="utf-8") as fh:
        for p in patches:
            fh.write(json.dumps(p, ensure_ascii=False) + "\n")

    # combined patch file (wave 1 + wave 2)
    combined: list[str] = []
    if W1_PATCH.is_file():
        combined.extend(W1_PATCH.read_text(encoding="utf-8").splitlines())
    combined.extend(json.dumps(p, ensure_ascii=False) for p in patches)
    with OUT_PATCH_ALL.open("w", encoding="utf-8") as fh:
        fh.write("\n".join(line for line in combined if line.strip()) + ("\n" if combined else ""))

    dry = dry_run_patch(OUT_PATCH)
    apply_result = None
    if dry["status"] == "ok" and patches:
        apply_result = apply_patch(OUT_PATCH)
    elif not patches:
        apply_result = {"status": "empty", "applied": 0}

    v8_rows, v8_stats = overlay_v8(merged)
    with V8.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=V7_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(v8_rows)

    v7 = load_csv(V7)
    bg_v7 = [r for r in v7 if r.get("claim_kind") == "rel" and (r.get("from_id", "").startswith("bg_") or r.get("to_id", "").startswith("bg_"))]
    uns_v7 = sum(1 for r in bg_v7 if r.get("verdict") == "UNSUPPORTED")
    uns_v8 = sum(1 for r in v8_rows if r.get("claim_kind") == "rel" and (r.get("from_id", "").startswith("bg_") or r.get("to_id", "").startswith("bg_")) and r.get("verdict") == "UNSUPPORTED")

    va = Counter(r.get("verdict_after") for r in merged)
    upgrades = sum(1 for r in merged if r.get("proposed_action") == "UPGRADE")
    counts = graph_counts()

    lines = [
        "# BG Hunt Wave 2 Report",
        "",
        f"**Generated:** {utc_now()} · **Database:** `mit-bestand`",
        "",
        "## Fleet summary",
        "",
        "| Agent | processed |",
        "|---|---:|",
    ]
    for agent, n in shard_stats.items():
        lines.append(f"| {agent} | {n} |")
    lines += [
        "",
        f"**Merged rows:** {len(merged)}",
        f"**Conflicts:** {len(conflicts)}",
        "",
        "## Verdict outcomes (hunted edges)",
        "",
        "| verdict_after | count |",
        "|---|---:|",
    ]
    for k, v in va.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Upgrade metrics",
        f"- PROVEN upgrades (patch-eligible): **{upgrades}**",
        f"- W2 patch ops emitted: **{len(patches)}**",
        f"- Dry-run status: **{dry['status']}**",
    ]
    if apply_result:
        lines.append(f"- W2 apply status: **{apply_result.get('status')}** · ops applied: **{apply_result.get('applied', 0)}**")
    lines += [
        "",
        "## v7 → v8 bg_ UNSUPPORTED",
        f"- v7 UNSUPPORTED bg_ rels: **{uns_v7}**",
        f"- v8 UNSUPPORTED bg_ rels: **{uns_v8}**",
        f"- Reduction (wave 2 hunt overlay): **{uns_v7 - uns_v8}**",
        "",
        "## v8 PROVEN % (bg_ rels)",
        f"- bg_ rel rows: **{v8_stats['bg_rows']}**",
        f"- PROVEN: **{v8_stats['bg_proven']}** ({v8_stats['bg_proven_pct']}%)",
        "",
        "## Graph counts (final)",
        f"- Nodes: **{counts['nodes']}**",
        f"- Relationships: **{counts['relationships']}**",
        "",
        "## Artifacts",
        f"- `{OUT_MERGED}`",
        f"- `{OUT_PATCH}`",
        f"- `{OUT_PATCH_ALL}`",
        f"- `{V8}`",
    ]
    if conflicts:
        lines += ["", "## Conflicts (first 10)", ""]
        for c in conflicts[:10]:
            lines.append(f"- {c}")

    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "merged": len(merged),
                "patches": len(patches),
                "dry_run": dry["status"],
                "apply": apply_result,
                "uns_v7": uns_v7,
                "uns_v8": uns_v8,
                "v8_proven_pct": v8_stats["bg_proven_pct"],
                "graph_counts": counts,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
