"""One-shot snapshot of rels/properties for nodes about to be deleted/merged.

Reads a list of node ids from --ids; for each, outputs node properties + all rels
(type, direction, neighbor id+name+labels, rel properties) to a JSON file.

Used as the safety pre-step for batch2 v2 Phase 1a (deletes) and 1b/1c (merges).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402


def snapshot(ids: list[str]) -> list[dict]:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    out: list[dict] = []
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            for nid in ids:
                entry: dict = {"id": nid, "found": False, "labels": [], "properties": {}, "rels": []}
                row = session.run(
                    "MATCH (n {id:$id}) RETURN labels(n) AS labels, properties(n) AS props",
                    id=nid,
                ).single()
                if not row:
                    out.append(entry)
                    continue
                entry["found"] = True
                entry["labels"] = list(row["labels"])
                entry["properties"] = dict(row["props"])
                rel_rows = list(session.run(
                    """MATCH (n {id:$id})-[r]->(m) RETURN type(r) AS rt, properties(r) AS rprops, 'OUT' AS dir, m.id AS nid, m.name AS nname, labels(m) AS nlabels
                       UNION ALL
                       MATCH (n {id:$id})<-[r]-(m) RETURN type(r) AS rt, properties(r) AS rprops, 'IN' AS dir, m.id AS nid, m.name AS nname, labels(m) AS nlabels""",
                    id=nid,
                ))
                entry["rels"] = [
                    {
                        "type": r["rt"],
                        "direction": r["dir"],
                        "neighbor_id": r["nid"],
                        "neighbor_name": r["nname"],
                        "neighbor_labels": list(r["nlabels"]),
                        "properties": dict(r["rprops"]) if r["rprops"] else {},
                    }
                    for r in rel_rows
                ]
                out.append(entry)
    finally:
        driver.close()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ids", required=True, help="Comma-separated node ids")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    ids = [s.strip() for s in args.ids.split(",") if s.strip()]
    data = snapshot(ids)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    found = sum(1 for d in data if d["found"])
    print(f"Snapshot of {len(ids)} ids: {found} found. Written to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
