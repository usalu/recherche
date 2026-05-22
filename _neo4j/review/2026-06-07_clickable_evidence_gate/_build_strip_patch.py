"""Phase 2a — stamp evidence_status on all URL-bearing claims + strip bad rel links.

Policy (after ground-truthing the gate):
  * STAMP evidence_status on every URL-bearing claim (reversible, lets you filter).
  * STRIP evidence_url ONLY from relationships whose link clearly fails to show the
    fact: QUOTE_MISMATCH, HOMEPAGE_ONLY, or truly-dead (404 / connection error).
  * KEEP (never strip):
      - ENTITY_HOMEPAGE  (a node pointing at its own org homepage is valid)
      - LIKELY_REVIEW    (deep page, partial match — flag, don't delete)
      - CLICKABLE_VERIFIED
      - bot-blocked dead (403/401/503/429) -> stamped NEEDS_RECHECK, link kept
  * Nodes are never stripped in this phase (entity links are low-risk); concept-node
    mismatches are stamped NEEDS_RECHECK for a later, gentler pass.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
sys.path.insert(0, str(SCRIPTS))
from neo4j_env import resolve_connection  # noqa: E402

csv.field_size_limit(10_000_000)
BASELINE = HERE / "CLICKABLE_EVIDENCE_BASELINE.csv"
OUT = HERE / "patches" / "ceg_status_and_strip.patch.jsonl"
BOT_BLOCKED = {"403", "401", "503", "429"}
STRIP_REL = {"QUOTE_MISMATCH", "HOMEPAGE_ONLY"}
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    rows = list(csv.DictReader(BASELINE.open(encoding="utf-8")))
    rel_eids = [r["eid"] for r in rows if r["kind"] == "rel"]
    node_eids = [r["eid"] for r in rows if r["kind"] == "node"]

    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    rel_map: dict[str, dict] = {}
    node_map: dict[str, str] = {}
    try:
        with driver.session(database=database) as s:
            for rec in s.run(
                "MATCH (a)-[r]->(b) WHERE elementId(r) IN $e "
                "RETURN elementId(r) AS eid, a.id AS fid, b.id AS tid, type(r) AS t, r.id AS rid",
                e=rel_eids,
            ):
                rel_map[rec["eid"]] = {"from": rec["fid"], "to": rec["tid"],
                                       "type": rec["t"], "rid": rec["rid"]}
            for rec in s.run(
                "MATCH (n) WHERE elementId(n) IN $e RETURN elementId(n) AS eid, n.id AS nid",
                e=node_eids,
            ):
                node_map[rec["eid"]] = rec["nid"]
    finally:
        driver.close()

    ops: list[dict] = []
    c = {"stamp_rel": 0, "stamp_node": 0, "strip_rel": 0, "recheck": 0, "unresolved": 0}
    for r in rows:
        status = r["evidence_status"]
        http = r["http_status"]
        recheck = status == "LINK_DEAD" and http in BOT_BLOCKED
        final = "NEEDS_RECHECK" if recheck else status
        if r["kind"] == "rel":
            loc = rel_map.get(r["eid"])
            if not loc or not loc.get("from") or not loc.get("to"):
                c["unresolved"] += 1
                continue
            sel = {"id": loc["rid"]} if loc.get("rid") else {
                "from": loc["from"], "type": loc["type"], "to": loc["to"]}
            strip = status in STRIP_REL or (status == "LINK_DEAD" and not recheck)
            if strip:
                ops.append({"op": "remove_rel_properties", **sel,
                            "properties": ["evidence_url"],
                            "reason": f"CEG strip: {status} (http {http or 'conn_err'})"})
                c["strip_rel"] += 1
            ops.append({"op": "set_rel_properties", **sel,
                        "properties": {"evidence_status": final, "evidence_checked_at": NOW},
                        "reason": f"CEG stamp {final}"})
            c["stamp_rel"] += 1
            if recheck:
                c["recheck"] += 1
        else:
            nid = node_map.get(r["eid"])
            if not nid:
                c["unresolved"] += 1
                continue
            ops.append({"op": "set_node_properties", "id": nid,
                        "properties": {"evidence_status": final, "evidence_checked_at": NOW},
                        "reason": f"CEG stamp {final}"})
            c["stamp_node"] += 1
            if recheck:
                c["recheck"] += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as fh:
        for op in ops:
            fh.write(json.dumps(op, ensure_ascii=False) + "\n")
    print("ops:", len(ops), c)
    print("patch:", OUT)


if __name__ == "__main__":
    main()
