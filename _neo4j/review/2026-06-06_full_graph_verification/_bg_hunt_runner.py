#!/usr/bin/env python3
"""Generic BG hunter runner for BG-01..BG-06."""

from __future__ import annotations

import argparse
import json
import sys
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
    load_v6_index,
    load_bg_projekt_map,
    write_ledger,
    write_report,
)

AGENT_CONFIG = {
    "BG-01": {"scope": "scope_h1_a", "mission": "H1 catalogue A", "ledger": "bg_hunt_01.csv", "report": "bg_hunt_01_report.md"},
    "BG-02": {"scope": "scope_h1_b", "mission": "H1 catalogue B", "ledger": "bg_hunt_02.csv", "report": "bg_hunt_02_report.md"},
    "BG-03": {"scope": "scope_h2", "mission": "H2 process axis", "ledger": "bg_hunt_03.csv", "report": "bg_hunt_03_report.md"},
    "BG-04": {"scope": "scope_h3", "mission": "H3 regulation", "ledger": "bg_hunt_04.csv", "report": "bg_hunt_04_report.md"},
    "BG-05": {"scope": "scope_h4", "mission": "H4 spatial", "ledger": "bg_hunt_05.csv", "report": "bg_hunt_05_report.md"},
    "BG-06": {"scope": "scope_h5", "mission": "H5 material taxonomy", "ledger": "bg_hunt_06.csv", "report": "bg_hunt_06_report.md"},
}


def run_agent(agent_id: str) -> dict:
    cfg = AGENT_CONFIG[agent_id]
    scope_path = WORK / f"{cfg['scope']}.json"
    if not scope_path.is_file():
        raise FileNotFoundError(f"Run BG-00 first: missing {scope_path}")

    scope = json.loads(scope_path.read_text(encoding="utf-8"))
    edges = scope.get("edges", [])
    mission_total = scope.get("meta", {}).get("total_in_mission", len(edges))

    v6 = load_v6_index()
    vocab = load_vocab_names()
    geo_index, bg_urls = load_geo_index()
    dossier_index, by_projekt = load_dossier_index()
    bg_projekt = load_bg_projekt_map()
    live_names = load_live_bg_names()
    cache: dict = {}

    rows = []
    blockers: list[str] = []
    fetch_errors = 0

    for i, edge in enumerate(edges):
        geid = edge.get("element_id", "")
        v6_row = v6.get(geid) or v6.get(f"claim:{geid}")
        try:
            row = hunt_edge(
                edge,
                v6_row,
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
            if v6_row:
                rows.append({**{k: v6_row.get(k, "") for k in v6_row}, "agent_id": agent_id, "verdict_before": v6_row.get("verdict", ""), "verdict_after": v6_row.get("verdict", ""), "notes": f"error:{exc}"})

    for url, fe in cache.items():
        if fe.get("error") and "429" in str(fe.get("error", "")):
            blockers.append(f"rate_limit:{url}")
        if fe.get("error") and not fe.get("fetched"):
            fetch_errors += 1
    if fetch_errors > len(edges) // 2 and edges:
        blockers.append(f"high_fetch_failure_rate:{fetch_errors}/{len(cache)} urls")

    ledger_path = HERE / "ledger" / cfg["ledger"]
    report_path = HERE / "reports" / cfg["report"]
    write_ledger(ledger_path, rows)
    write_report(report_path, agent_id, cfg["mission"], rows, mission_total, blockers)

    from collections import Counter
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
