#!/usr/bin/env python3
"""BG Hunt Rework — fix scorer, full dossier mining, web discovery, v9 aggregator."""

from __future__ import annotations

import argparse
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
WORK = HERE / "_bg_hunt_work"
LEDGER = HERE / "ledger"
PATCHES = HERE / "patches"
REPORTS = HERE / "reports"
APPLY_REPORTS = HERE / "apply_reports"
APPLY_SCRIPT = SCRIPTS / "apply_neo4j_review_patch.py"
V8 = HERE / "VERIFICATION_LEDGER_ELEMENT_v8.csv"
V9 = HERE / "VERIFICATION_LEDGER_ELEMENT_v9.csv"
CACHE_PATH = WORK / "url_fetch_cache_rework.json"
REVIEW_RUN = "bg_hunt_rework_2026_06_07"

sys.path.insert(0, str(WORK))
sys.path.insert(0, str(SCRIPTS))

from quote_scorer import is_valid_quote  # noqa: E402
from bg_hunt_common import (  # noqa: E402
    LEDGER_COLS,
    V8 as V8_PATH,
    hunt_edge_rework,
    load_bg_projekt_map,
    load_dossier_index,
    load_geo_index,
    load_live_bg_names,
    load_vocab_names,
    utc_now,
    write_ledger,
    write_report,
)
from neo4j_env import resolve_connection  # noqa: E402


def load_v8_rows() -> list[dict]:
    rows = []
    with V8.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            rows.append(row)
    return rows


def catalogue_non_proven_keys(v8_rows: list[dict]) -> set[str]:
    keys: set[str] = set()
    for row in v8_rows:
        if row.get("claim_kind") != "rel":
            continue
        if row.get("verdict") == "PROVEN":
            continue
        rel = row.get("rel_type_or_label", "")
        if rel not in {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"}:
            continue
        f, t = row.get("from_id", ""), row.get("to_id", "")
        if not (f.startswith("bg_") or t.startswith("bg_")):
            continue
        geid = row.get("graph_element_id") or row.get("element_id", "")
        if geid:
            keys.add(geid)
    return keys


def export_catalogue_edges() -> list[dict]:
    from neo4j import GraphDatabase

    uri, user, password, _ = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    edges: list[dict] = []
    with driver.session(database="mit-bestand") as session:
        q = """
        MATCH (bg:Bauteilgruppe)-[r]->(t)
        WHERE type(r) IN ['HAT_BAUTEILTYP', 'NUTZT_MATERIAL']
        RETURN elementId(r) AS element_id, bg.id AS from_id, t.id AS to_id,
               type(r) AS rel_type, bg.name AS bg_name
        ORDER BY bg.id, type(r)
        """
        for rec in session.run(q):
            edges.append(dict(rec))
    driver.close()
    return edges


def cluster_by_projekt(edges: list[dict], bg_projekt: dict) -> list[dict]:
    def proj_key(e: dict) -> str:
        bg = e["from_id"] if e["from_id"].startswith("bg_") else e["to_id"]
        return bg_projekt.get(bg, {}).get("projekt_id", bg)

    return sorted(edges, key=lambda e: (proj_key(e), e.get("rel_type", ""), e.get("from_id", "")))


def load_cache() -> dict:
    if CACHE_PATH.is_file():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_cache(cache: dict) -> None:
    slim = {k: {kk: vv for kk, vv in v.items() if kk != "text"} for k, v in cache.items()}
    CACHE_PATH.write_text(json.dumps(slim, ensure_ascii=False), encoding="utf-8")


def build_v8_index(v8_rows: list[dict]) -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for row in v8_rows:
        geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
        if geid:
            idx[geid] = row
    return idx


def run_phase(
    phase: str,
    edges: list[dict],
    v8_index: dict[str, dict],
    *,
    enable_web: bool,
    bundle_escalate: bool,
    cache: dict,
    shared: dict,
) -> list[dict]:
    rows: list[dict] = []
    agent_id = f"BG-RW-{phase.upper()}"
    for edge in edges:
        geid = edge.get("element_id", "")
        ledger_row = v8_index.get(geid)
        row = hunt_edge_rework(
            edge,
            ledger_row,
            vocab_names=shared["vocab"],
            geo_index=shared["geo"],
            bg_urls=shared["bg_urls"],
            dossier_index=shared["dossier_index"],
            by_projekt=shared["by_projekt"],
            bg_projekt=shared["bg_projekt"],
            live_names=shared["live_names"],
            cache=cache,
            agent_id=agent_id,
            enable_web=enable_web,
            bundle_escalate=bundle_escalate,
        )
        rows.append(row)
    return rows


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
        quote = props.get("evidence_quote", "")
        if not quote or not is_valid_quote(quote):
            continue
        patches.append({
            "op": "set_rel_properties",
            "from": row.get("from_id", ""),
            "type": row.get("rel_type_or_label", ""),
            "to": row.get("to_id", ""),
            "properties": props,
            "reason": f"BG rework {row.get('agent_id')} score={row.get('alias_score', '')}",
        })
    return patches


def dry_run_patch(patch_path: Path) -> dict:
    if not patch_path.is_file() or patch_path.stat().st_size == 0:
        return {"status": "empty", "returncode": 0}
    cmd = [sys.executable, str(APPLY_SCRIPT), "--patch", str(patch_path), "--database", "mit-bestand"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO))
    return {"status": "ok" if proc.returncode == 0 else "error", "returncode": proc.returncode}


def overlay_v9(v8_rows: list[dict], merged: list[dict]) -> tuple[list[dict], dict]:
    overlay: dict[str, dict] = {}
    for row in merged:
        geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
        if geid:
            overlay[geid] = row

    out_rows: list[dict] = []
    v8_cols = list(v8_rows[0].keys()) if v8_rows else []
    deltas = Counter()

    for row in v8_rows:
        geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
        new_row = dict(row)
        if geid in overlay:
            o = overlay[geid]
            before = row.get("verdict", "")
            after = o.get("verdict_after", before)
            if after != before:
                deltas[f"{before}->{after}"] += 1
            new_row["verdict"] = after
            if o.get("proof_quote"):
                new_row["proof_quote"] = o["proof_quote"]
            if o.get("basis_ref"):
                new_row["basis_ref"] = o["basis_ref"]
            new_row["agent_id"] = o.get("agent_id", row.get("agent_id", ""))
            new_row["notes"] = o.get("notes", row.get("notes", ""))
            new_row["proposed_action"] = o.get("proposed_action", row.get("proposed_action", ""))
        out_rows.append(new_row)

    return out_rows, dict(deltas)


def bg_stats(rows: list[dict]) -> dict:
    bg_rels = [
        r for r in rows
        if r.get("claim_kind") == "rel"
        and (r.get("from_id", "").startswith("bg_") or r.get("to_id", "").startswith("bg_"))
    ]
    vc = Counter(r.get("verdict", "") for r in bg_rels)
    total = len(bg_rels) or 1
    return {"total": len(bg_rels), "proven": vc.get("PROVEN", 0), "pct": 100 * vc.get("PROVEN", 0) / total, "verdicts": dict(vc)}


def regression_check_proven_catalogue(
    all_edges: list[dict],
    v8_index: dict[str, dict],
    shared: dict,
    cache: dict,
) -> list[dict]:
    """Re-score v8 PROVEN catalogue bg_ edges; must stay PROVEN."""
    proven_edges = [
        e for e in all_edges
        if v8_index.get(e["element_id"], {}).get("verdict") == "PROVEN"
    ]
    failures = []
    for edge in proven_edges[:50]:  # sample cap for speed
        row = hunt_edge_rework(
            edge, v8_index.get(edge["element_id"]),
            vocab_names=shared["vocab"], geo_index=shared["geo"], bg_urls=shared["bg_urls"],
            dossier_index=shared["dossier_index"], by_projekt=shared["by_projekt"],
            bg_projekt=shared["bg_projekt"], live_names=shared["live_names"],
            cache=cache, agent_id="BG-RW-REG", enable_web=False, bundle_escalate=False,
        )
        if row.get("verdict_after") != "PROVEN":
            failures.append({
                "element_id": edge["element_id"],
                "verdict_after": row.get("verdict_after"),
                "from_id": edge.get("from_id"),
                "to_id": edge.get("to_id"),
            })
    return failures


def write_campaign_report(
    path: Path,
    *,
    scope_count: int,
    phase_a: list[dict],
    phase_b: list[dict],
    merged: list[dict],
    v8_bg: dict,
    v9_bg: dict,
    deltas: dict,
    patches: list[dict],
    dry_run: dict,
    regressions: list[dict],
) -> None:
    va = Counter(r.get("verdict_after") for r in phase_a)
    vb = Counter(r.get("verdict_after") for r in phase_b) if phase_b else Counter()
    vm = Counter(r.get("verdict_after") for r in merged)
    upgrades = sum(1 for r in merged if r.get("proposed_action") == "UPGRADE")
    escalate = sum(1 for r in merged if r.get("proposed_action") == "ESCALATE_HUMAN")
    proven_new = [r for r in merged if r.get("verdict_after") == "PROVEN" and r.get("verdict_before") != "PROVEN"]

    lines = [
        "# BG Hunt Rework Campaign Report",
        "",
        f"**Generated:** {utc_now()} · **Database:** `mit-bestand`",
        "",
        "## Scope",
        f"- Non-PROVEN catalogue bg_ edges: **{scope_count}**",
        "",
        "## Phase A (dossier re-score, no network)",
        f"| verdict | count |",
        f"|---|---:|",
    ]
    for k, v in va.most_common():
        lines.append(f"| {k} | {v} |")
    if phase_b:
        lines += ["", "## Phase B (web discovery)", "| verdict | count |", "|---|---:|"]
        for k, v in vb.most_common():
            lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Merged outcomes",
        "| verdict | count |",
        "|---|---:|",
    ]
    for k, v in vm.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        f"- PROVEN upgrades (patch-eligible): **{upgrades}**",
        f"- ESCALATE_HUMAN (bundle policy): **{escalate}**",
        f"- New PROVEN (from non-PROVEN): **{len(proven_new)}**",
        "",
        "## v8 → v9 bg_ rels",
        f"- v8 PROVEN: **{v8_bg['proven']}** ({v8_bg['pct']:.2f}%)",
        f"- v9 PROVEN: **{v9_bg['proven']}** ({v9_bg['pct']:.2f}%)",
        "",
        "## Verdict deltas (overlay)",
        "| transition | count |",
        "|---|---:|",
    ]
    for k, v in sorted(deltas.items(), key=lambda x: -x[1]):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Patch dry-run",
        f"- Ops: **{len(patches)}** · status: **{dry_run.get('status', 'n/a')}**",
        "",
        "## Regression (prior applied PROVEN)",
        f"- Failures: **{len(regressions)}**",
    ]
    if regressions[:5]:
        for f in regressions[:5]:
            lines.append(f"- `{f['element_id']}` → {f['verdict_after']}")
    lines += [
        "",
        "## Sample new PROVEN (audit)",
        "",
    ]
    for r in proven_new[:15]:
        lines.append(
            f"- `{r.get('from_id')}` → `{r.get('to_id')}` ({r.get('rel_type_or_label')}): "
            f"\"{str(r.get('proof_quote', ''))[:80]}...\""
        )
    lines += [
        "",
        "## Artifacts",
        f"- `{LEDGER / 'bg_hunt_rework_a.csv'}`",
        f"- `{LEDGER / 'bg_hunt_rework_b.csv'}`",
        f"- `{LEDGER / 'bg_hunt_rework_merged.csv'}`",
        f"- `{PATCHES / 'bg_hunt_rework_upgrades.patch.jsonl'}`",
        f"- `{V9}`",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-web", action="store_true", help="Phase A only (dossier re-score)")
    args = parser.parse_args()

    v8_rows = load_v8_rows()
    v8_index = build_v8_index(v8_rows)
    target_keys = catalogue_non_proven_keys(v8_rows)

    all_edges = export_catalogue_edges()
    bg_projekt = load_bg_projekt_map()
    scoped = [e for e in cluster_by_projekt(all_edges, bg_projekt) if e["element_id"] in target_keys]

    # Clear dossier bundle cache when re-running after code changes
    import bg_hunt_common as _bhc  # noqa: E402
    _bhc._DOSSIER_BUNDLE_CACHE.clear()

    dossier_index, by_projekt = load_dossier_index()
    geo_index, bg_urls = load_geo_index()
    shared = {
        "vocab": load_vocab_names(),
        "geo": geo_index,
        "bg_urls": bg_urls,
        "dossier_index": dossier_index,
        "by_projekt": by_projekt,
        "bg_projekt": bg_projekt,
        "live_names": load_live_bg_names(),
    }
    cache = load_cache()

    print(f"scope: {len(scoped)} non-PROVEN catalogue edges")

    # Phase A: dossier only
    phase_a = run_phase("A", scoped, v8_index, enable_web=False, bundle_escalate=False, cache=cache, shared=shared)
    write_ledger(LEDGER / "bg_hunt_rework_a.csv", phase_a)
    write_report(REPORTS / "bg_hunt_rework_a_report.md", "BG-RW-A", "Dossier re-score", phase_a, len(scoped), [])

    still_unsupported = {r["graph_element_id"] for r in phase_a if r.get("verdict_after") == "UNSUPPORTED"}
    phase_b_edges = [e for e in scoped if e["element_id"] in still_unsupported]
    phase_b: list[dict] = []

    if not args.skip_web and phase_b_edges:
        phase_b = run_phase("B", phase_b_edges, v8_index, enable_web=True, bundle_escalate=True, cache=cache, shared=shared)
        write_ledger(LEDGER / "bg_hunt_rework_b.csv", phase_b)
        write_report(REPORTS / "bg_hunt_rework_b_report.md", "BG-RW-B", "Web discovery", phase_b, len(phase_b_edges), [])
        save_cache(cache)

    # Merge: phase_b wins over phase_a for same geid
    merged_map: dict[str, dict] = {r["graph_element_id"]: r for r in phase_a}
    for r in phase_b:
        merged_map[r["graph_element_id"]] = r
    merged = list(merged_map.values())
    write_ledger(LEDGER / "bg_hunt_rework_merged.csv", merged)

    regressions = regression_check_proven_catalogue(all_edges, v8_index, shared, cache)

    patches = emit_patches(merged)
    patch_path = PATCHES / "bg_hunt_rework_upgrades.patch.jsonl"
    PATCHES.mkdir(parents=True, exist_ok=True)
    with patch_path.open("w", encoding="utf-8") as fh:
        for p in patches:
            fh.write(json.dumps(p, ensure_ascii=False) + "\n")

    dry_run = dry_run_patch(patch_path)

    v9_rows, deltas = overlay_v9(v8_rows, merged)
    v8_bg = bg_stats(v8_rows)
    v9_bg = bg_stats(v9_rows)

    if v9_rows:
        with V9.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(v9_rows[0].keys()), extrasaction="ignore")
            w.writeheader()
            w.writerows(v9_rows)

    write_campaign_report(
        REPORTS / "BG_HUNT_REWORK_REPORT.md",
        scope_count=len(scoped),
        phase_a=phase_a,
        phase_b=phase_b,
        merged=merged,
        v8_bg=v8_bg,
        v9_bg=v9_bg,
        deltas=deltas,
        patches=patches,
        dry_run=dry_run,
        regressions=regressions,
    )

    summary = {
        "scope": len(scoped),
        "phase_a": dict(Counter(r.get("verdict_after") for r in phase_a)),
        "phase_b": dict(Counter(r.get("verdict_after") for r in phase_b)) if phase_b else {},
        "merged": dict(Counter(r.get("verdict_after") for r in merged)),
        "upgrades": len(patches),
        "dry_run": dry_run,
        "v8_bg_proven_pct": round(v8_bg["pct"], 2),
        "v9_bg_proven_pct": round(v9_bg["pct"], 2),
        "regressions": len(regressions),
    }
    (WORK / "rework_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
