"""Probe which auxiliary nodes are EXCLUSIVE to each cascade-delete project vs SHARED.

For each project id in CASCADE_IDS, list every directly-connected neighbour with
its label set and the count of OTHER (non-this-project) projects/programmes that
connect to the same neighbour. Exclusives have other_project_degree=0.
"""
from __future__ import annotations
import json, os
from pathlib import Path
from neo4j import GraphDatabase  # type: ignore

PASSWORD = Path(".neo4j_password").read_text(encoding="utf-8").strip().splitlines()[0]
URI = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687")
DB = os.environ.get("NEO4J_DATABASE", "mit-bestand")

CASCADE_IDS = ["p_circle_house", "p_obk_27", "p_careno_becircular", "p_eggshell_pavilion", "p_granby_workshop", "p_eth_circular_construction_student_reuse_project"]

driver = GraphDatabase.driver(URI, auth=("neo4j", PASSWORD))
with driver.session(database=DB, default_access_mode="READ") as sess:
    out: dict[str, list[dict]] = {}
    for pid in CASCADE_IDS:
        # All neighbours (both directions), with neighbour labels + how many OTHER reuse-entities
        # (Projekt|Programm|Tool|Marktmodell|Software|Methode) connect to the same neighbour.
        rows = sess.run(
            """
            MATCH (p {id:$pid})-[r]-(n)
            WITH p, r, n
            OPTIONAL MATCH (other)-[r2]-(n)
              WHERE other.id <> $pid
                AND (
                  'Projekt' IN labels(other) OR 'Programm' IN labels(other)
                  OR 'Tool' IN labels(other) OR 'Marktmodell' IN labels(other)
                  OR 'Software' IN labels(other) OR 'Methode' IN labels(other)
                )
            RETURN type(r) AS rel_type,
                   startNode(r).id = $pid AS is_outbound,
                   n.id AS neighbour_id,
                   labels(n) AS neighbour_labels,
                   coalesce(n.name, '') AS neighbour_name,
                   count(DISTINCT other) AS other_reuse_entities_using_neighbour
            ORDER BY rel_type, neighbour_id
            """,
            pid=pid,
        )
        out[pid] = [dict(r) for r in rows]

driver.close()

for pid, neighbours in out.items():
    print(f"\n========== {pid} ({len(neighbours)} edges) ==========")
    by_label: dict[str, list[dict]] = {}
    for n in neighbours:
        key = "+".join(sorted(n["neighbour_labels"]))
        by_label.setdefault(key, []).append(n)
    for label_key in sorted(by_label):
        items = by_label[label_key]
        print(f"\n  -- {label_key} ({len(items)} neighbours) --")
        for it in items:
            arrow = "->" if it["is_outbound"] else "<-"
            exclusive = "EXCLUSIVE" if it["other_reuse_entities_using_neighbour"] == 0 else f"shared({it['other_reuse_entities_using_neighbour']})"
            print(f"    {arrow} {it['rel_type']:25s} {it['neighbour_id']:55s} {it['neighbour_name'][:40]:40s} {exclusive}")
