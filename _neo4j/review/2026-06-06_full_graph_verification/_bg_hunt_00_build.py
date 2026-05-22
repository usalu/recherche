#!/usr/bin/env python3
"""BG-00 — Tooling: alias tables, scope export, slug decomposition smoke test."""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REVIEW = HERE
WORK = REVIEW / "_bg_hunt_work"
REPO = REVIEW.parents[1]
sys.path.insert(0, str(WORK))
sys.path.insert(0, str(REPO / "_scripts"))

from bg_slug_decompose import decompose_bg_id  # noqa: E402
from bg_hunt_common import (  # noqa: E402
    V6,
    load_bg_projekt_map,
    load_live_bg_names,
    utc_now,
    write_report,
)
from neo4j_env import resolve_connection  # noqa: E402

V6_PATH = V6
OUT_REPORT = REVIEW / "reports" / "bg_hunt_00_report.md"

MISSIONS = {
    "scope_h1_a": {
        "agent": "BG-01",
        "rel_types": ["HAT_BAUTEILTYP", "NUTZT_MATERIAL"],
        "batch": 200,
        "batch_offset": 0,
        "unsupported_only": True,
        "inbound_hat_bauteilgruppe": False,
    },
    "scope_h1_b": {
        "agent": "BG-02",
        "rel_types": ["HAT_BAUTEILTYP", "NUTZT_MATERIAL"],
        "batch": 200,
        "batch_offset": 200,
        "unsupported_only": True,
        "inbound_hat_bauteilgruppe": False,
    },
    "scope_h2": {
        "agent": "BG-03",
        "rel_types": ["HAT_PROZESSPHASE", "HAT_BESCHAFFUNGSWEG", "HAT_LOGISTIK"],
        "batch": 150,
        "batch_offset": 0,
        "unsupported_only": True,
        "inbound_hat_bauteilgruppe": False,
    },
    "scope_h3": {
        "agent": "BG-04",
        "rel_types": ["ERFORDERT_NACHWEIS", "TRIGGERS_REGULIERUNGSFRAGE"],
        "batch": 150,
        "batch_offset": 0,
        "unsupported_only": True,
        "inbound_hat_bauteilgruppe": False,
    },
    "scope_h4": {
        "agent": "BG-05",
        "rel_types": ["AUS_SPENDER", "IN_EMPFANGSOBJEKT"],
        "batch": 9999,
        "batch_offset": 0,
        "unsupported_only": True,
        "inbound_hat_bauteilgruppe": True,
    },
    "scope_h5": {
        "agent": "BG-06",
        "rel_types": ["HAT_MATERIALGRUPPE", "HAT_RUECKBAUVERFAHREN", "HAT_AUFBEREITUNG"],
        "batch": 9999,
        "batch_offset": 0,
        "unsupported_only": True,
        "inbound_hat_bauteilgruppe": False,
    },
}


def load_v6_unsupported_keys() -> set[str]:
    keys: set[str] = set()
    with V6_PATH.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("claim_kind") != "rel" or row.get("verdict") != "UNSUPPORTED":
                continue
            f, t = row.get("from_id", ""), row.get("to_id", "")
            if not (f.startswith("bg_") or t.startswith("bg_")):
                continue
            geid = row.get("graph_element_id") or row.get("element_id", "")
            if geid:
                keys.add(geid)
    return keys


def export_graph_edges(rel_types: list[str], inbound_bg: bool) -> list[dict]:
    from neo4j import GraphDatabase

    uri, user, password, _ = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    edges: list[dict] = []
    with driver.session(database="mit-bestand") as session:
        if inbound_bg:
            q = """
            MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
            RETURN elementId(r) AS element_id, p.id AS from_id, bg.id AS to_id,
                   type(r) AS rel_type, bg.name AS bg_name
            ORDER BY p.id, bg.id
            """
            for rec in session.run(q):
                edges.append(dict(rec))
        else:
            q = """
            MATCH (bg:Bauteilgruppe)-[r]->(t)
            WHERE type(r) IN $rel_types
            RETURN elementId(r) AS element_id, bg.id AS from_id, t.id AS to_id,
                   type(r) AS rel_type, bg.name AS bg_name
            ORDER BY bg.id, type(r)
            """
            for rec in session.run(q, rel_types=rel_types):
                edges.append(dict(rec))
    driver.close()
    return edges


def cluster_by_projekt(edges: list[dict], bg_projekt: dict) -> list[dict]:
    """Sort edges by projekt_id for fetch-cache clustering."""
    def proj_key(e: dict) -> str:
        bg = e["from_id"] if e["from_id"].startswith("bg_") else e["to_id"]
        return bg_projekt.get(bg, {}).get("projekt_id", bg)

    return sorted(edges, key=lambda e: (proj_key(e), e.get("rel_type", ""), e.get("from_id", "")))


def filter_scope(edges: list[dict], cfg: dict, uns_keys: set[str], bg_projekt: dict) -> list[dict]:
    if cfg["unsupported_only"]:
        edges = [e for e in edges if e["element_id"] in uns_keys]
    edges = cluster_by_projekt(edges, bg_projekt)
    off = cfg["batch_offset"]
    batch = cfg["batch"]
    return edges[off : off + batch]


def build_alias_export(bg_names: dict[str, str], bg_projekt: dict) -> list[dict]:
    rows = []
    for bg_id, bg_name in sorted(bg_names.items()):
        decomp = decompose_bg_id(bg_id, bg_name)
        proj = bg_projekt.get(bg_id, {})
        rows.append({
            **decomp,
            "bg_name": bg_name,
            "projekt_id": proj.get("projekt_id", ""),
            "projekt_name": proj.get("projekt_name", ""),
        })
    return rows


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    uns_keys = load_v6_unsupported_keys()
    bg_projekt = load_bg_projekt_map()
    bg_names = load_live_bg_names()

    alias_rows = build_alias_export(bg_names, bg_projekt)
    alias_path = WORK / "alias_tables_bg_export.jsonl"
    with alias_path.open("w", encoding="utf-8") as fh:
        for row in alias_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    scope_stats: dict[str, dict] = {}
    for scope_name, cfg in MISSIONS.items():
        edges = export_graph_edges(cfg["rel_types"], cfg["inbound_hat_bauteilgruppe"])
        scoped = filter_scope(edges, cfg, uns_keys, bg_projekt)
        out_path = WORK / f"{scope_name}.json"
        out_path.write_text(json.dumps({
            "meta": {"agent": cfg["agent"], "scope": scope_name, "generated_at": utc_now(), "total_in_mission": len(edges)},
            "edges": scoped,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        scope_stats[scope_name] = {
            "agent": cfg["agent"],
            "mission_total": len(edges),
            "scoped": len(scoped),
            "unsupported_pool": sum(1 for e in edges if e["element_id"] in uns_keys),
        }

    write_report(
        OUT_REPORT,
        "BG-00",
        "Tooling + scope export",
        [],
        scope_count=sum(s["scoped"] for s in scope_stats.values()),
        blockers=[],
    )
    # append scope table
    lines = OUT_REPORT.read_text(encoding="utf-8").splitlines()
    lines += ["", "## Scope files", "", "| scope | agent | mission_total | scoped | unsupported_pool |", "|---|---|---:|---:|---:|"]
    for name, st in scope_stats.items():
        lines.append(f"| `{name}.json` | {st['agent']} | {st['mission_total']} | {st['scoped']} | {st['unsupported_pool']} |")
    lines += [
        "",
        "## Artifacts",
        f"- `{WORK / 'bg_slug_decompose.py'}`",
        f"- `{WORK / 'alias_tables.json'}`",
        f"- `{WORK / 'quote_scorer.py'}`",
        f"- `{alias_path}`",
    ]
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"scope_stats": scope_stats, "alias_rows": len(alias_rows)}, indent=2))


if __name__ == "__main__":
    main()
