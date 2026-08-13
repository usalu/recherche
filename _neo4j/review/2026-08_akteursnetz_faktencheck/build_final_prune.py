# -*- coding: utf-8 -*-
"""
Final deletion list for the akteursnetz report, per the user's standing rule:
"Any non belegt information after these runs has to be deleted if it means
false information. Only evidence-packed stuff stays" -- applied concretely as
"delete all ohne_beleg nodes" (2026-08-13 decision, including the
nicht_pruefbar-flagged ones), plus the separately computed R1 (duplicate) and
R3 (wrong country) removal candidates, which are not necessarily ohne_beleg.

This is broader than prune_faktencheck.json (which only holds R1-R3 computed
candidates, i.e. R2 requires ohne_beleg + structural isolation) -- the user's
rule has no isolation requirement, so all 86 ohne_beleg nodes are included
regardless of whether they carry a drawn edge.

Also emits the edge-side counterpart: every `unklar`-graded edge, as a
normalized (min-eid, max-eid) pair, for netz's `partition()` `edge_exclude`
param -- "only evidence-packed stuff stays" applies to edges the same way.

Input: verdicts.json, prune_faktencheck_provenance.json, worklist.json (all
in this folder)
Output: prune_faktencheck_final.json -- plain array of eids, drops into
netz/data/prune.py's load_prune() unchanged.
Output: unklar_edges_final.json -- array of [eid_a, eid_b] pairs.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return json.load(f)


def build_node_meta(wl):
    node_meta = {}
    for pkt in wl["packets"]:
        cc = pkt["cc"]
        for n in pkt.get("nodes", []):
            node_meta[(cc, n["tid"])] = n["eid"]
    return node_meta


def main():
    v = load("verdicts.json")
    prov = load("prune_faktencheck_provenance.json")
    wl = load("worklist.json")
    node_meta = build_node_meta(wl)

    unklar_pairs = set()
    unklar_missing = []
    for e in v["edges"]:
        if e.get("edge_degree") != "unklar":
            continue
        cc = e["cc"]
        ea, eb = node_meta.get((cc, e["a_tid"])), node_meta.get((cc, e["b_tid"]))
        if not ea or not eb:
            unklar_missing.append((cc, e["a_tid"], e["b_tid"]))
            continue
        unklar_pairs.add(tuple(sorted((ea, eb))))

    edges_out_path = os.path.join(BASE, "unklar_edges_final.json")
    with open(edges_out_path, "w", encoding="utf-8") as f:
        json.dump(sorted(unklar_pairs), f, indent=2, ensure_ascii=False)
    print(f"unklar edges: {sum(1 for e in v['edges'] if e.get('edge_degree') == 'unklar')}")
    print(f"resolved eid pairs: {len(unklar_pairs)}"
          + (f"  ! {len(unklar_missing)} unresolved: {unklar_missing}" if unklar_missing else ""))
    print(f"Written: {edges_out_path}")

    eids = set()
    no_eid = []
    for n in v["nodes"]:
        if n.get("actor_degree") == "ohne_beleg":
            if n.get("eid"):
                eids.add(n["eid"])
            else:
                no_eid.append((n["cc"], n["tid"]))
    for c in prov["entries"]:
        if c.get("eid"):
            eids.add(c["eid"])
        else:
            no_eid.append((c["cc"], c["tid"]))

    out_path = os.path.join(BASE, "prune_faktencheck_final.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(sorted(eids), f, indent=2, ensure_ascii=False)

    print(f"ohne_beleg nodes: {sum(1 for n in v['nodes'] if n.get('actor_degree') == 'ohne_beleg')}")
    print(f"R1+R3 candidates (from provenance): {len(prov['entries'])}")
    print(f"Final unique eids to delete: {len(eids)}")
    if no_eid:
        print(f"  ! {len(no_eid)} entries had no eid, skipped: {no_eid}")
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
