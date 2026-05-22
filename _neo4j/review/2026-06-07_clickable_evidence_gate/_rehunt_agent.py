"""Run one CEG re-hunt agent shard (CEG-R1..R4)."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(HERE))

from neo4j_env import resolve_connection  # noqa: E402
import verify_clickable_evidence as ceg  # noqa: E402
import ceg_rehunt_common as crc  # noqa: E402

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_graph_context(rows: list[dict]) -> dict[str, dict]:
    from neo4j import GraphDatabase

    rel_eids = [r["eid"] for r in rows if r["kind"] == "rel"]
    node_eids = [r["eid"] for r in rows if r["kind"] == "node"]
    ctx: dict[str, dict] = {}

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session(database=database) as s:
            for eid in rel_eids:
                rec = s.run(
                    "MATCH (a)-[rel]->(b) WHERE elementId(rel)=$eid "
                    "OPTIONAL MATCH (a)-[*1..2]-(p:Projekt) "
                    "WITH a,b,rel, collect(DISTINCT p) AS ps "
                    "RETURN a.id AS fid, b.id AS tid, type(rel) AS t, rel.id AS rid, "
                    "a.source_urls AS asu, a.primary_source_url AS apu, b.source_urls AS bsu, "
                    "[x IN ps | x.id] AS pids, [x IN ps | x.source_urls] AS psu, "
                    "[x IN ps | x.primary_source_url] AS ppu",
                    eid=eid,
                ).single()
                if not rec:
                    continue
                cands: list[str] = []
                for v in [rec["apu"]] + (rec["ppu"] or []):
                    if v and str(v).startswith("http"):
                        cands.append(v)
                for lst in [rec["asu"], rec["bsu"]] + (rec["psu"] or []):
                    for v in (lst or []):
                        if v and str(v).startswith("http"):
                            cands.append(v)
                dossier = crc.load_dossier_urls(rec["pids"] or [])
                ctx[eid] = {
                    "from": rec["fid"], "to": rec["tid"], "type": rec["t"],
                    "rid": rec["rid"], "cands": list(dict.fromkeys(cands)),
                    "dossier_urls": dossier,
                }
            for eid in node_eids:
                rec = s.run(
                    "MATCH (n) WHERE elementId(n)=$eid "
                    "RETURN n.id AS nid, n.source_urls AS su, n.primary_source_url AS pu",
                    eid=eid,
                ).single()
                if not rec:
                    continue
                cands = [v for v in ([rec["pu"]] + (rec["su"] or [])) if v and str(v).startswith("http")]
                ctx[eid] = {"nid": rec["nid"], "cands": list(dict.fromkeys(cands)), "dossier_urls": []}
    finally:
        driver.close()
    return ctx


def to_patch(hit: dict, ctx: dict) -> dict | None:
    if hit["result"] != "RECOVERED":
        return None
    props = {
        "evidence_status": "CLICKABLE_VERIFIED",
        "evidence_checked_at": NOW,
    }
    if hit["kind"] == "rel":
        c = ctx.get(hit["eid"], {})
        sel = {"id": c["rid"]} if c.get("rid") else {"from": c["from"], "type": c["type"], "to": c["to"]}
        props["evidence_url"] = hit["new_url"]
        if hit.get("new_quote"):
            props["evidence_quote"] = hit["new_quote"]
        return {
            "op": "set_rel_properties", **sel,
            "properties": props,
            "reason": f"CEG {hit.get('agent_id')} {hit.get('mode')} {hit.get('score')}",
        }
    c = ctx.get(hit["eid"], {})
    props["primary_source_url"] = hit["new_url"]
    return {
        "op": "set_node_properties", "id": c.get("nid", ""),
        "properties": props,
        "reason": f"CEG {hit.get('agent_id')} {hit.get('mode')} {hit.get('score')}",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True, choices=list(crc.AGENT_FILTERS))
    args = ap.parse_args()

    rows = crc.load_scope(args.agent)
    print(f"{args.agent}: scope {len(rows)} claims")
    ctx = load_graph_context(rows)

    cache_path = HERE / f"_fetch_cache_{args.agent}.json"
    cache: dict = {}
    if cache_path.is_file():
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    if ceg.CACHE_PATH.is_file():
        shared = json.loads(ceg.CACHE_PATH.read_text(encoding="utf-8"))
        cache = {**shared, **cache}

    out_rows, patches = [], []
    recovered = 0
    for i, row in enumerate(rows, 1):
        c = ctx.get(row["eid"], {"cands": [], "dossier_urls": []})
        hit = crc.hunt_claim(row, c, cache)
        hit["agent_id"] = args.agent
        out_rows.append(hit)
        if hit["result"] == "RECOVERED":
            recovered += 1
            p = to_patch(hit, ctx)
            if p:
                patches.append(p)
        if i % 10 == 0:
            print(f"  {i}/{len(rows)} recovered {recovered}")
            cache_path.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
            time.sleep(0.15)

    cache_path.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    ledger = HERE / "ledger" / f"rehunt_{args.agent}.csv"
    patch = HERE / "patches" / f"rehunt_{args.agent}.patch.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    patch.parent.mkdir(parents=True, exist_ok=True)

    if out_rows:
        with ledger.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
            w.writeheader()
            w.writerows(out_rows)
    with patch.open("w", encoding="utf-8") as fh:
        for p in patches:
            fh.write(json.dumps(p, ensure_ascii=False) + "\n")

    print(f"{args.agent} done: recovered {recovered}/{len(rows)}")
    print(f"  ledger: {ledger}")
    print(f"  patch:  {patch} ({len(patches)} ops)")


if __name__ == "__main__":
    main()
