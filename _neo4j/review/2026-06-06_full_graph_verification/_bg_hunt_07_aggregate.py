#!/usr/bin/env python3
"""BG-07 — Aggregator: merge bg_hunt shards, emit patches, dry-run, v7 ledger overlay."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

csv.field_size_limit(10_000_000)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
LEDGER = HERE / "ledger"
PATCHES = HERE / "patches"
REPORTS = HERE / "reports"
APPLY_SCRIPT = SCRIPTS / "apply_neo4j_review_patch.py"
V6 = HERE / "VERIFICATION_LEDGER_ELEMENT_v6.csv"
V7 = HERE / "VERIFICATION_LEDGER_ELEMENT_v7.csv"

SHARDS = [
    ("BG-01", "bg_hunt_01.csv"),
    ("BG-02", "bg_hunt_02.csv"),
    ("BG-03", "bg_hunt_03.csv"),
    ("BG-04", "bg_hunt_04.csv"),
    ("BG-05", "bg_hunt_05.csv"),
    ("BG-06", "bg_hunt_06.csv"),
]

OUT_MERGED = LEDGER / "bg_hunt_merged.csv"
OUT_PATCH = PATCHES / "bg_hunt_upgrades.patch.jsonl"
OUT_REPORT = REPORTS / "BG_HUNT_CAMPAIGN_REPORT.md"
REVIEW_RUN = "bg_hunt_2026_06_07"

V6_COLS = [
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
            "reason": f"BG hunt upgrade {row.get('agent_id')} score={row.get('alias_score', '')} basis={basis[:80]}",
        })
    return patches


def dry_run_patch(patch_path: Path) -> dict:
    if not patch_path.is_file() or patch_path.stat().st_size == 0:
        return {"status": "empty", "stdout": "", "stderr": ""}
    cmd = [
        sys.executable,
        str(APPLY_SCRIPT),
        "--patch", str(patch_path),
        "--database", "mit-bestand",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO))
    ok = proc.returncode == 0
    missing = 0
    try:
        report_json = patch_path.parent.parent / "apply_reports" / f"{patch_path.name}.apply_report.json"
        if report_json.is_file():
            rep = json.loads(report_json.read_text(encoding="utf-8"))
            missing = rep.get("summary", {}).get("missing_rel", 0)
    except Exception:
        pass
    status = "ok" if ok and missing == 0 else ("partial" if ok else "error")
    return {"status": status, "returncode": proc.returncode, "missing_rel": missing, "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-2000:]}


def overlay_v7(merged: list[dict]) -> tuple[list[dict], dict]:
    by_geid = {(r.get("graph_element_id") or r.get("element_id", "")).strip(): r for r in merged if r.get("graph_element_id") or r.get("element_id")}
    v6_rows = load_csv(V6)
    out_rows = []
    changes = Counter()
    for row in v6_rows:
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


def main() -> None:
    merged, shard_stats, conflicts = load_shards()
    OUT_MERGED.parent.mkdir(parents=True, exist_ok=True)
    PATCHES.mkdir(parents=True, exist_ok=True)

    # write merged with hunt columns
    hunt_cols = list(merged[0].keys()) if merged else []
    with OUT_MERGED.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=hunt_cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(merged)

    patches = emit_patches(merged)
    with OUT_PATCH.open("w", encoding="utf-8") as fh:
        for p in patches:
            fh.write(json.dumps(p, ensure_ascii=False) + "\n")

    dry = dry_run_patch(OUT_PATCH)
    v7_rows, v7_stats = overlay_v7(merged)
    with V7.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=V6_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(v7_rows)

    # baseline v6 bg unsupported
    v6 = load_csv(V6)
    bg_v6 = [r for r in v6 if r.get("claim_kind") == "rel" and (r.get("from_id", "").startswith("bg_") or r.get("to_id", "").startswith("bg_"))]
    uns_v6 = sum(1 for r in bg_v6 if r.get("verdict") == "UNSUPPORTED")
    uns_after = sum(1 for r in v7_rows if r.get("claim_kind") == "rel" and (r.get("from_id", "").startswith("bg_") or r.get("to_id", "").startswith("bg_")) and r.get("verdict") == "UNSUPPORTED")

    va = Counter(r.get("verdict_after") for r in merged)
    upgrades = sum(1 for r in merged if r.get("proposed_action") == "UPGRADE")

    lines = [
        "# BG Hunt Campaign Report",
        "",
        f"**Generated:** {utc_now()} · **Database:** `mit-bestand` · **Mode:** dry-run only",
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
        f"**Conflicts (duplicate element_id):** {len(conflicts)}",
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
        f"- Patch ops emitted: **{len(patches)}**",
        f"- Dry-run status: **{dry['status']}** (returncode={dry.get('returncode', 'n/a')})",
        "",
        "## v6 → v7 bg_ UNSUPPORTED",
        f"- v6 UNSUPPORTED bg_ rels: **{uns_v6}**",
        f"- v7 UNSUPPORTED bg_ rels: **{uns_after}**",
        f"- Reduction: **{uns_v6 - uns_after}** ({round(100*(uns_v6-uns_after)/uns_v6,1) if uns_v6 else 0}%)",
        "",
        "## v7 PROVEN % (bg_ rels)",
        f"- bg_ rel rows: **{v7_stats['bg_rows']}**",
        f"- PROVEN: **{v7_stats['bg_proven']}** ({v7_stats['bg_proven_pct']}%)",
        "",
        "## Artifacts",
        f"- `{OUT_MERGED}`",
        f"- `{OUT_PATCH}`",
        f"- `{V7}`",
        "",
        "## Dry-run tail",
        "```",
        dry.get("stdout", "")[-2000:],
        "```",
    ]
    if conflicts:
        lines += ["", "## Conflicts (first 10)", ""]
        for c in conflicts[:10]:
            lines.append(f"- {c}")

    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "merged": len(merged),
        "patches": len(patches),
        "dry_run": dry["status"],
        "uns_v6": uns_v6,
        "uns_after": uns_after,
        "v7_proven_pct": v7_stats["bg_proven_pct"],
    }, indent=2))


if __name__ == "__main__":
    main()
