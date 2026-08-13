# -*- coding: utf-8 -*-
"""Build the complete, human-auditable inventory used by the edge campaign.

Output: kanten_review_inventory.json (one record for each of the 570 drawn
candidate edges, including endpoint names, prior fact-check evidence, and the
fresh URL/quotation recheck result).
"""
from datetime import datetime, timezone
import json
import os
import sys
import tempfile


BASE = os.path.dirname(os.path.abspath(__file__))
NETZ = os.path.abspath(os.path.join(BASE, "..", "..", "netz"))
if NETZ not in sys.path:
    sys.path.insert(0, NETZ)

from netz.sources import DEFAULT  # noqa: E402
from netz.data.prune import load_edge_exclude, load_prune  # noqa: E402
from netz.model.concepts import build_network  # noqa: E402


OUTPUT = os.path.join(BASE, "kanten_review_inventory.json")


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def write_atomic(path, value):
    fd, tmp = tempfile.mkstemp(prefix=os.path.basename(path) + ".",
                               suffix=".tmp", dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def main():
    index = load(os.path.join(BASE, "kanten_batches", "_index.json"))
    verdicts = load(os.path.join(BASE, "verdicts.json"))
    worklist = load(os.path.join(BASE, "worklist.json"))
    recheck = load(os.path.join(BASE, "kanten_source_recheck.json"))

    exclude = load_prune(DEFAULT.prune_path) | load_prune(DEFAULT.prune_faktencheck_path)
    network = build_network(
        DEFAULT,
        exclude=exclude,
        edge_exclude=load_edge_exclude(DEFAULT.unklar_edges_path),
    )
    key_to_eid = {
        (packet["cc"], node["tid"]): node["eid"]
        for packet in worklist["packets"] for node in packet.get("nodes", [])
    }
    verdict_by_pair = {}
    for verdict in verdicts["edges"]:
        a = key_to_eid.get((verdict["cc"], verdict["a_tid"]))
        b = key_to_eid.get((verdict["cc"], verdict["b_tid"]))
        if a and b:
            verdict_by_pair[tuple(sorted((a, b)))] = verdict

    records = []
    for batch in index["batches"]:
        for edge in batch["edges"]:
            pair = tuple(sorted(edge["pair"]))
            verdict = verdict_by_pair.get(pair, {})
            nodes = []
            for eid, is_project in zip(edge["pair"],
                                       (edge["a_is_project"], edge["b_is_project"])):
                raw = network.raw.by[eid]
                nodes.append({
                    "eid": eid,
                    "name": raw.get("properties", {}).get("name", eid),
                    "type": network.raw.types.get(eid),
                    "is_project": is_project,
                })
            records.append({
                "id": edge["id"],
                "batch": batch["batch"],
                "country": batch["cc"],
                "kind": edge["kind"],
                "pair": list(pair),
                "node_a": nodes[0],
                "node_b": nodes[1],
                "status": edge["status"],
                "prior_edge_degree": verdict.get("edge_degree"),
                "prior_relation_code": verdict.get("relation_soll"),
                "prior_relation_description": verdict.get("relation_ist"),
                "evidence_url": edge.get("evidence_url") or None,
                "evidence_quote": edge.get("evidence_quote") or None,
                "source_recheck": recheck.get("edges", {}).get(edge["id"]),
            })

    payload = {
        "review_run": index.get("review_run"),
        "built_at": datetime.now(timezone.utc).isoformat(),
        "source_snapshot": index.get("source_snapshot", {}).get("snapshot_id"),
        "total_edges": len(records),
        "records": records,
    }
    write_atomic(OUTPUT, payload)
    print(f"written: {OUTPUT}")
    print(f"records: {len(records)} | checked: "
          f"{sum(r['status'] == 'GEPRUEFT' for r in records)} | unchecked: "
          f"{sum(r['status'] == 'UNGEPRUEFT' for r in records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
