#!/usr/bin/env python3
"""BG-W2-00 — Build wave-2 catalogue hunt scopes (offsets 400/550/700)."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "_bg_hunt_work"
REPO = HERE.parents[2]
sys.path.insert(0, str(WORK))
sys.path.insert(0, str(REPO / "_scripts"))

from bg_hunt_common import load_bg_projekt_map, utc_now  # noqa: E402
from neo4j_env import resolve_connection  # noqa: E402

V7 = HERE / "VERIFICATION_LEDGER_ELEMENT_v7.csv"
CATALOGUE_TYPES = ["HAT_BAUTEILTYP", "NUTZT_MATERIAL"]

W2_BATCHES = [
    ("scope_w2_01", "BG-W2-01", 400, 150),
    ("scope_w2_02", "BG-W2-02", 550, 150),
    ("scope_w2_03", "BG-W2-03", 700, 9999),
]


def load_v7_unsupported_keys() -> set[str]:
    keys: set[str] = set()
    with V7.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("claim_kind") != "rel" or row.get("verdict") != "UNSUPPORTED":
                continue
            if row.get("rel_type_or_label") not in CATALOGUE_TYPES:
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
        WHERE type(r) IN $rel_types
        RETURN elementId(r) AS element_id, bg.id AS from_id, t.id AS to_id,
               type(r) AS rel_type, bg.name AS bg_name
        ORDER BY bg.id, type(r)
        """
        for rec in session.run(q, rel_types=CATALOGUE_TYPES):
            edges.append(dict(rec))
    driver.close()
    return edges


def cluster_by_projekt(edges: list[dict], bg_projekt: dict) -> list[dict]:
    def proj_key(e: dict) -> str:
        bg = e["from_id"] if e["from_id"].startswith("bg_") else e["to_id"]
        return bg_projekt.get(bg, {}).get("projekt_id", bg)

    return sorted(edges, key=lambda e: (proj_key(e), e.get("rel_type", ""), e.get("from_id", "")))


def main() -> None:
    uns_keys = load_v7_unsupported_keys()
    bg_projekt = load_bg_projekt_map()
    all_edges = export_catalogue_edges()
    pool = [e for e in all_edges if e["element_id"] in uns_keys]
    pool = cluster_by_projekt(pool, bg_projekt)

    stats: dict[str, dict] = {}
    for scope_name, agent, offset, batch in W2_BATCHES:
        scoped = pool[offset : offset + batch]
        out_path = WORK / f"{scope_name}.json"
        out_path.write_text(
            json.dumps(
                {
                    "meta": {
                        "agent": agent,
                        "scope": scope_name,
                        "generated_at": utc_now(),
                        "total_in_mission": len(pool),
                        "batch_offset": offset,
                        "batch_size": batch,
                    },
                    "edges": scoped,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        stats[scope_name] = {"agent": agent, "offset": offset, "scoped": len(scoped)}

    print(json.dumps({"pool_total": len(pool), "scopes": stats}, indent=2))


if __name__ == "__main__":
    main()
