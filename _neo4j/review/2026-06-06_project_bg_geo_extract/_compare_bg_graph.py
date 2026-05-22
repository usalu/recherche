"""Compare reuse_geo_graph BG-per-project counts vs Neo4j mit-bestand."""

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

REUSE = Path(__file__).resolve().parent / "reuse_geo_graph.json"
reuse = json.loads(REUSE.read_text(encoding="utf-8"))

export_by: dict[str, int] = defaultdict(int)
export_bg_ids: set[str] = set()
for bg in reuse["nodes"]["bauteilgruppen"]:
    export_bg_ids.add(bg["id"])
    pid = (bg.get("relationships") or {}).get("projekt_id") or (
        (bg.get("receiver") or {}).get("projekt") or {}
    ).get("id")
    if pid:
        export_by[pid] += 1

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))

with driver.session(database=db) as session:
    n_proj = session.run("MATCH (p:Projekt) RETURN count(p) AS n").single()["n"]
    n_bg = session.run("MATCH (bg:Bauteilgruppe) RETURN count(bg) AS n").single()["n"]
    graph_bg_ids = {r["id"] for r in session.run("MATCH (bg:Bauteilgruppe) RETURN bg.id AS id")}

    bg_proj_rels = [
        dict(r)
        for r in session.run(
            """
            MATCH (bg:Bauteilgruppe)-[r]-(p:Projekt)
            RETURN type(r) AS rel, count(*) AS n
            ORDER BY n DESC
            """
        )
    ]

    bg_keys = [
        dict(r)
        for r in session.run(
            """
            MATCH (bg:Bauteilgruppe)
            UNWIND keys(bg) AS k
            RETURN k, count(*) AS n
            ORDER BY n DESC LIMIT 20
            """
        )
    ]

    # Strategy A: property on BG
    by_prop: dict[str, int] = defaultdict(int)
    bg_no_prop = 0
    for r in session.run(
        """
        MATCH (bg:Bauteilgruppe)
        RETURN bg.id AS id, bg.projekt_id AS pid
        """
    ):
        if r["pid"]:
            by_prop[r["pid"]] += 1
        else:
            bg_no_prop += 1

    # Strategy B: BETEILIGT_AN reverse (BG -> Projekt unusual) or Projekt <- BG
    by_beteiligt: dict[str, int] = defaultdict(int)
    for r in session.run(
        """
        MATCH (bg:Bauteilgruppe)-[:BETEILIGT_AN]->(p:Projekt)
        RETURN p.id AS pid, count(bg) AS n
        """
    ):
        by_beteiligt[r["pid"]] = r["n"]

    # Strategy C: common pattern Projekt <- BG via EINGEBAUT_IN / ZU_PROJEKT / etc.
    by_inbound: dict[str, int] = defaultdict(int)
    for r in session.run(
        """
        MATCH (p:Projekt)<-[r]-(bg:Bauteilgruppe)
        RETURN p.id AS pid, type(r) AS rel, count(bg) AS n
        ORDER BY n DESC
        """
    ):
        by_inbound[r["pid"]] += r["n"]

    inbound_rels = [
        dict(r)
        for r in session.run(
            """
            MATCH (p:Projekt)<-[r]-(bg:Bauteilgruppe)
            RETURN type(r) AS rel, count(*) AS n
            ORDER BY n DESC
        """
        )
    ]

driver.close()

only_export = export_bg_ids - graph_bg_ids
only_graph = graph_bg_ids - export_bg_ids

print("=== TOTALS ===")
print(f"reuse_geo_graph: {len(reuse['nodes']['projekte'])} projekte, {len(export_bg_ids)} BGs")
print(f"neo4j:           {n_proj} projekte, {n_bg} BGs")
print(f"BG id set: export-only {len(only_export)}, graph-only {len(only_graph)}")
if only_export:
    print("  sample export-only:", sorted(only_export)[:5])
if only_graph:
    print("  sample graph-only:", sorted(only_graph)[:5])

print("\n=== BG-Projekt linkage in Neo4j ===")
print("rel types (any direction):", bg_proj_rels)
print("inbound BG->Projekt rel types:", inbound_rels)
print("BGs with projekt_id property:", sum(by_prop.values()), "| without:", bg_no_prop)
print("BG -[:BETEILIGT_AN]-> Projekt:", sum(by_beteiligt.values()))

print("\n=== Per-project BG count: export vs graph.projekt_id ===")
all_pids = sorted(set(export_by) | set(by_prop))
mismatch = [(pid, export_by.get(pid, 0), by_prop.get(pid, 0)) for pid in all_pids if export_by.get(pid, 0) != by_prop.get(pid, 0)]
print(f"projects: {len(all_pids)} | match: {len(all_pids)-len(mismatch)} | mismatch: {len(mismatch)}")
for pid, e, g in mismatch[:30]:
    print(f"  {pid}: export={e} graph={g}")
if len(mismatch) > 30:
    print(f"  ... +{len(mismatch)-30}")

print("\n=== export projekte with BG vs graph projekt_id ===")
zero_in_graph = [pid for pid, c in export_by.items() if c and not by_prop.get(pid)]
print(f"export has BG but graph projekt_id=0: {len(zero_in_graph)}", zero_in_graph[:10])
