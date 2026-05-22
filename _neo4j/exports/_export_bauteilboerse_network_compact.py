"""Compact export — the originally-suggested 1+2+4 scope:

  Layer 1 (Core):       all 54 anchors + Akteurtyp + Akteurrolle +
                        Geschaeftsmodell + Marktmodell + Methode + Land
  Layer 2 (Stock):     + Material + Bauteiltyp
  Layer 4 (Network):   + connected Akteur/Software (operators, partners,
                         founders) via BETRIEBEN_VON, VERBUNDEN_MIT_AKTEUR,
                         NUTZT_SOFTWARE, GEHÖRT_ZU
                       + Projekt + Programm via BETEILIGT_AN

  SKIPPED Layer 3:     no Quelle / evidence URL nodes (use the full export
                       bauteilboerse_network_2026-06-01.json for those).

Result target: ~150 nodes and ~750 edges.
"""
from __future__ import annotations
import json, os
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter, defaultdict
from neo4j import GraphDatabase

URI      = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
USER     = os.environ.get("NEO4J_USER", "neo4j").strip()
DATABASE = os.environ.get("NEO4J_DATABASE", "mit-bestand").strip()
PWPATH   = Path(".neo4j_password")
OUT      = Path("_neo4j/exports/bauteilboerse_network_compact_2026-06-01.json")

# Labels we include
KEEP_LABELS = {
    "Akteur", "Software",                            # anchors + connected operators/partners
    "Akteurtyp", "Akteurrolle", "Methode",           # classification vocab
    "Geschaeftsmodell", "Marktmodell",
    "Material", "Bauteiltyp",                        # stock vocab
    "Land",                                          # geography
    "Projekt", "Programm",                           # project participation
}
# Edges we include (anything connecting two KEEP_LABELS nodes is implicitly included)
KEEP_EDGE_TYPES = {
    "HAT_AKTEURTYP", "HAT_AKTEURROLLE", "HAT_METHODE",
    "HAT_GESCHAEFTSMODELL", "HAT_MARKTMODELL",
    "NUTZT_MATERIAL", "HAT_BAUTEILTYP",
    "LIEGT_IN_LAND",
    "VERBUNDEN_MIT_AKTEUR", "BETRIEBEN_VON", "NUTZT_SOFTWARE", "GEHÖRT_ZU",
    "BETEILIGT_AN", "STUB_PROJECT_LINK",
}


def to_jsonable(v):
    if v is None: return None
    if isinstance(v, (str, int, float, bool)): return v
    if isinstance(v, (list, tuple)): return [to_jsonable(x) for x in v]
    if hasattr(v, "iso_format"): return v.iso_format()
    return str(v)


def main():
    pw = PWPATH.read_text(encoding="utf-8").strip()
    driver = GraphDatabase.driver(URI, auth=(USER, pw))
    nodes_by_eid: dict[str, dict] = {}
    edges_by_eid: dict[str, dict] = {}

    with driver.session(database=DATABASE) as s:
        anchor_eids = [r["eid"] for r in s.run(
            "MATCH (a)-[:HAT_GESCHAEFTSMODELL]->() RETURN DISTINCT elementId(a) AS eid")]
        print(f"Anchors: {len(anchor_eids)}")

        # ---------- Pull anchors + direct neighbours, filtered by KEEP_LABELS ----------
        print("Pulling Layer 1+2+4 ...")
        for record in s.run("""
            UNWIND $eids AS eid
            MATCH (a) WHERE elementId(a) = eid
            OPTIONAL MATCH (a)-[r]->(t)
            WHERE any(lbl IN labels(t) WHERE lbl IN $keep)
            RETURN a, collect({r: r, n: t}) AS out_n
        """, eids=anchor_eids, keep=list(KEEP_LABELS)):
            a = record["a"]
            if a is not None:
                nodes_by_eid[a.element_id] = {
                    "elementId": a.element_id,
                    "labels": list(a.labels),
                    "properties": {k: to_jsonable(v) for k, v in dict(a).items()},
                }
            for item in record["out_n"]:
                r, t = item["r"], item["n"]
                if r is None or t is None: continue
                # Filter edge types as well
                if r.type not in KEEP_EDGE_TYPES: continue
                edges_by_eid[r.element_id] = {
                    "elementId": r.element_id,
                    "type": r.type,
                    "source": r.start_node.element_id,
                    "target": r.end_node.element_id,
                    "properties": {k: to_jsonable(v) for k, v in dict(r).items()},
                }
                nodes_by_eid[t.element_id] = {
                    "elementId": t.element_id,
                    "labels": list(t.labels),
                    "properties": {k: to_jsonable(v) for k, v in dict(t).items()},
                }
        print(f"  after outgoing: {len(nodes_by_eid)} nodes / {len(edges_by_eid)} edges")

        # ---------- Incoming edges of same kept-types ----------
        for record in s.run("""
            UNWIND $eids AS eid
            MATCH (a) WHERE elementId(a) = eid
            OPTIONAL MATCH (src)-[r]->(a)
            WHERE any(lbl IN labels(src) WHERE lbl IN $keep)
            RETURN a, collect({r: r, n: src}) AS in_n
        """, eids=anchor_eids, keep=list(KEEP_LABELS)):
            for item in record["in_n"]:
                r, src = item["r"], item["n"]
                if r is None or src is None: continue
                if r.type not in KEEP_EDGE_TYPES: continue
                edges_by_eid[r.element_id] = {
                    "elementId": r.element_id,
                    "type": r.type,
                    "source": r.start_node.element_id,
                    "target": r.end_node.element_id,
                    "properties": {k: to_jsonable(v) for k, v in dict(r).items()},
                }
                nodes_by_eid[src.element_id] = {
                    "elementId": src.element_id,
                    "labels": list(src.labels),
                    "properties": {k: to_jsonable(v) for k, v in dict(src).items()},
                }
        print(f"  after incoming: {len(nodes_by_eid)} nodes / {len(edges_by_eid)} edges")

        # ---------- Densify: edges between collected nodes only (kept types) ----------
        print("Densifying internal edges ...")
        all_eids = list(nodes_by_eid.keys())
        added = 0
        BATCH = 300
        for i in range(0, len(all_eids), BATCH):
            chunk = all_eids[i:i+BATCH]
            for record in s.run("""
                UNWIND $eids AS eid
                MATCH (x) WHERE elementId(x) = eid
                MATCH (x)-[r]->(y)
                WHERE elementId(y) IN $all_eids AND type(r) IN $keep_edges
                RETURN r
            """, eids=chunk, all_eids=all_eids, keep_edges=list(KEEP_EDGE_TYPES)):
                r = record["r"]
                if r is None or r.element_id in edges_by_eid: continue
                edges_by_eid[r.element_id] = {
                    "elementId": r.element_id, "type": r.type,
                    "source": r.start_node.element_id, "target": r.end_node.element_id,
                    "properties": {k: to_jsonable(v) for k, v in dict(r).items()},
                }
                added += 1
        print(f"  +{added} densified edges")

    driver.close()

    # ---------- Strip nodes whose label is not in KEEP_LABELS (safety) ----------
    before = len(nodes_by_eid)
    nodes_by_eid = {
        eid: n for eid, n in nodes_by_eid.items()
        if any(lbl in KEEP_LABELS for lbl in n["labels"])
    }
    print(f"  pruned {before - len(nodes_by_eid)} off-scope nodes")
    valid_eids = set(nodes_by_eid.keys())
    edges_by_eid = {
        eid: e for eid, e in edges_by_eid.items()
        if e["source"] in valid_eids and e["target"] in valid_eids
    }

    # ---------- Aggregate node/edge type stats ----------
    nt_descr = {
        "Akteur": "Operator / company (Bauteilbörse anchor or partner/operator/founder)",
        "Software": "Software product node (e.g. Restado, Loopfront)",
        "Akteurtyp": "Actor-type vocabulary",
        "Akteurrolle": "Functional-role vocabulary",
        "Geschaeftsmodell": "Business-model archetype (5 clusters)",
        "Marktmodell": "Transaction-type vocabulary",
        "Methode": "Method vocabulary (urban mining, audit, inventory, ...)",
        "Material": "Closed-set material vocabulary (mat_*)",
        "Bauteiltyp": "Closed-set component vocabulary (bt_*)",
        "Land": "Country vocabulary",
        "Projekt": "Reuse project",
        "Programm": "Programme (funding / research)",
    }
    nt_counter = Counter()
    for n in nodes_by_eid.values():
        for lbl in n["labels"]:
            nt_counter[lbl] += 1
    et_counter = Counter()
    et_endpoints = defaultdict(lambda: {"from_labels": set(), "to_labels": set()})
    for e in edges_by_eid.values():
        et_counter[e["type"]] += 1
        et_endpoints[e["type"]]["from_labels"].update(nodes_by_eid[e["source"]]["labels"])
        et_endpoints[e["type"]]["to_labels"].update(nodes_by_eid[e["target"]]["labels"])

    doc = {
        "metadata": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "database": DATABASE,
            "scope": "Layers 1+2+4 — Bauteilbörse anchors + classification vocab + stock vocab + connected actors/projects. NO Quelle/evidence URL nodes (see full export for those).",
            "anchor_count": len(anchor_eids),
            "node_count":   len(nodes_by_eid),
            "edge_count":   len(edges_by_eid),
            "kept_labels":  sorted(KEEP_LABELS),
            "kept_edgetypes": sorted(KEEP_EDGE_TYPES),
        },
        "nodetypes": [
            {"label": lbl, "count": cnt, "description": nt_descr.get(lbl, "")}
            for lbl, cnt in sorted(nt_counter.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
        "edgetypes": [
            {
                "type": t,
                "count": et_counter[t],
                "from_labels": sorted(et_endpoints[t]["from_labels"]),
                "to_labels":   sorted(et_endpoints[t]["to_labels"]),
            }
            for t in sorted(et_counter.keys(), key=lambda k: (-et_counter[k], k))
        ],
        "nodes": sorted(
            list(nodes_by_eid.values()),
            key=lambda n: (n["labels"][0] if n["labels"] else "", n["properties"].get("id") or n["elementId"]),
        ),
        "edges": sorted(
            list(edges_by_eid.values()),
            key=lambda e: (e["type"], e["source"], e["target"]),
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    size_kb = OUT.stat().st_size / 1024
    print(f"\nWritten {OUT}")
    print(f"  size: {size_kb:.1f} KB")
    print(f"  nodes: {len(nodes_by_eid)}  edges: {len(edges_by_eid)}")
    print(f"  nodetypes: {len(nt_counter)}  edgetypes: {len(et_counter)}")
    print("\nNodetypes:")
    for lbl, n in sorted(nt_counter.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {lbl:20s} {n}")
    print("\nEdgetypes:")
    for t, n in sorted(et_counter.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {t:25s} {n}")


if __name__ == "__main__":
    main()
