#!/usr/bin/env python3
"""BG-W2 runner — catalogue hunt batches BG-W2-01..03 with shared URL cache."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "_bg_hunt_work"
REPO = HERE.parents[2]
sys.path.insert(0, str(WORK))
sys.path.insert(0, str(REPO / "_scripts"))

from bg_hunt_common import (  # noqa: E402
    hunt_edge,
    load_dossier_index,
    load_geo_index,
    load_live_bg_names,
    load_vocab_names,
    load_bg_projekt_map,
    write_ledger,
    write_report,
)

V7 = HERE / "VERIFICATION_LEDGER_ELEMENT_v7.csv"
CACHE_PATH = WORK / "url_fetch_cache_w2.json"

AGENT_CONFIG = {
    "BG-W2-01": {"scope": "scope_w2_01", "mission": "W2 catalogue batch 1 (offset 400)", "ledger": "bg_hunt_w2_01.csv", "report": "bg_hunt_w2_01_report.md"},
    "BG-W2-02": {"scope": "scope_w2_02", "mission": "W2 catalogue batch 2 (offset 550)", "ledger": "bg_hunt_w2_02.csv", "report": "bg_hunt_w2_02_report.md"},
    "BG-W2-03": {"scope": "scope_w2_03", "mission": "W2 catalogue batch 3 (offset 700)", "ledger": "bg_hunt_w2_03.csv", "report": "bg_hunt_w2_03_report.md"},
}


def load_v7_index() -> dict[str, dict]:
    idx: dict[str, dict] = {}
    with V7.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
            if geid:
                idx[geid] = row
            cid = row.get("claim_id", "")
            if cid:
                idx[f"claim:{cid}"] = row
    return idx


def load_cache() -> dict:
    if CACHE_PATH.is_file():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    slim = {k: {kk: vv for kk, vv in v.items() if kk != "text"} for k, v in cache.items()}
    CACHE_PATH.write_text(json.dumps(slim, ensure_ascii=False), encoding="utf-8")


def run_agent(agent_id: str, cache: dict | None = None) -> dict:
    cfg = AGENT_CONFIG[agent_id]
    scope_path = WORK / f"{cfg['scope']}.json"
    if not scope_path.is_file():
        raise FileNotFoundError(f"Run _bg_hunt_w2_build.py first: missing {scope_path}")

    scope = json.loads(scope_path.read_text(encoding="utf-8"))
    edges = scope.get("edges", [])
    mission_total = scope.get("meta", {}).get("total_in_mission", len(edges))

    v7 = load_v7_index()
    vocab = load_vocab_names()
    geo_index, bg_urls = load_geo_index()
    dossier_index, by_projekt = load_dossier_index()
    bg_projekt = load_bg_projekt_map()
    live_names = load_live_bg_names()
    if cache is None:
        cache = load_cache()

    rows: list[dict] = []
    blockers: list[str] = []
    fetch_errors = 0

    for edge in edges:
        geid = edge.get("element_id", "")
        v7_row = v7.get(geid) or v7.get(f"claim:{geid}")
        try:
            row = hunt_edge(
                edge,
                v7_row,
                vocab_names=vocab,
                geo_index=geo_index,
                bg_urls=bg_urls,
                dossier_index=dossier_index,
                by_projekt=by_projekt,
                bg_projekt=bg_projekt,
                live_names=live_names,
                cache=cache,
                agent_id=agent_id,
            )
            rows.append(row)
        except Exception as exc:
            blockers.append(f"edge {geid}: {exc}")
            if v7_row:
                rows.append(
                    {
                        **{k: v7_row.get(k, "") for k in v7_row},
                        "agent_id": agent_id,
                        "verdict_before": v7_row.get("verdict", ""),
                        "verdict_after": v7_row.get("verdict", ""),
                        "notes": f"error:{exc}",
                    }
                )

    for url, fe in cache.items():
        if fe.get("error") and "429" in str(fe.get("error", "")):
            blockers.append(f"rate_limit:{url}")
        if fe.get("error") and not fe.get("fetched"):
            fetch_errors += 1
    if fetch_errors > len(edges) // 2 and edges:
        blockers.append(f"high_fetch_failure_rate:{fetch_errors}/{len(cache)} urls")

    save_cache(cache)

    ledger_path = HERE / "ledger" / cfg["ledger"]
    report_path = HERE / "reports" / cfg["report"]
    write_ledger(ledger_path, rows)
    write_report(report_path, agent_id, cfg["mission"], rows, mission_total, blockers)

    vc = Counter(r.get("verdict_after") for r in rows)
    upgrades = sum(1 for r in rows if r.get("proposed_action") == "UPGRADE")
    return {
        "agent": agent_id,
        "processed": len(rows),
        "proven": vc.get("PROVEN", 0),
        "upgrades": upgrades,
        "partial": vc.get("PARTIAL", 0),
        "unsupported": vc.get("UNSUPPORTED", 0),
        "cache_urls": len(cache),
        "blockers": blockers[:10],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("agent_id", choices=list(AGENT_CONFIG))
    args = p.parse_args()
    result = run_agent(args.agent_id)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
