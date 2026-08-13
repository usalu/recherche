# -*- coding: utf-8 -*-
"""
Merge raw shard verdicts into a canonical verdicts file and derive removal
candidates by fixed, deterministic rules (never agent-judged).

Can be run at any point on whatever countries are done so far in raw/ --
prints a coverage caveat for anything not yet covered.

Rules (per the approved plan, `idempotent-drifting-river.md`):
  R1  duplicate            -> flagged 'duplikat' => candidate (keep the target)
  R2  unsupported+isolated -> actor_degree=='ohne_beleg' AND every incident
                               drawn edge (if any) is 'unklar' (vacuously true
                               if it has none) => candidate
  R3  wrong country        -> flagged 'falsches_land' AND the correct country
                               is not itself one of the 11 drawn panels => candidate
  Never a candidate by themselves: nicht_pruefbar, kern, bezug, defunkt-alone.
"""
import json, glob, os, sys
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw")
WL_PATH = os.path.join(BASE, "worklist.json")

DRAWN_PANELS = {"CH", "DE", "FR", "BE", "GB", "NL", "DK", "SE", "FI", "NO", "AT"}

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def main():
    wl = load(WL_PATH)
    node_meta = {}   # (cc,tid) -> {eid, name, is_isolated, typ}
    country_node_count = defaultdict(int)
    country_edge_count = defaultdict(int)
    for pkt in wl["packets"]:
        cc = pkt["cc"]
        for n in pkt.get("nodes", []):
            node_meta[(cc, n["tid"])] = {
                "eid": n["eid"], "name": n["name"],
                "is_isolated": n.get("is_isolated", False),
                "typ": n.get("typ"),
            }
            country_node_count[cc] += 1
        country_edge_count[cc] += len(pkt.get("edges", []))

    files_by_cc = defaultdict(list)
    for path in glob.glob(os.path.join(RAW, "shard_*.json")):
        base = os.path.basename(path)[len("shard_"):-len(".json")]
        cc = base.split("-")[0]
        files_by_cc[cc].append(path)

    node_verdicts = {}   # (cc,tid) -> verdict dict
    edge_verdicts = {}   # (cc,a,b frozenset) -> verdict dict
    adjacency = defaultdict(list)  # (cc,tid) -> list of edge_degree

    for cc, paths in files_by_cc.items():
        for p in paths:
            data = load(p)
            result = data.get("result", data)
            for pkt in result.get("packets", []):
                for n in pkt.get("nodes", []):
                    key = (cc, n["tid"])
                    node_verdicts[key] = n
                for e in pkt.get("edges", []):
                    a, b = e["a_tid"], e["b_tid"]
                    edge_verdicts[(cc, frozenset((a, b)))] = e
                    deg = e.get("edge_degree")
                    adjacency[(cc, a)].append(deg)
                    adjacency[(cc, b)].append(deg)

    candidates = []
    kept_flagged = []  # flagged but not removal candidates (e.g. defunkt-alone, nicht_pruefbar)

    for key, v in node_verdicts.items():
        cc, tid = key
        meta = node_meta.get(key, {})
        name = meta.get("name", tid)
        eid = meta.get("eid", "")
        flags = [f.get("flag") if isinstance(f, dict) else f for f in (v.get("flags") or [])]
        deg = v.get("actor_degree")
        reasons = []

        # R1 duplicate
        if "duplikat" in flags:
            dup_fl = next(f for f in (v.get("flags") or []) if (f.get("flag") if isinstance(f,dict) else f) == "duplikat")
            dup_of_tid = dup_fl.get("duplikat_von", "") if isinstance(dup_fl, dict) else ""
            dup_of_name = node_meta.get((cc, dup_of_tid), {}).get("name", dup_of_tid)
            reasons.append(f"R1 duplicate of '{dup_of_name}' ({dup_of_tid})")

        # R2 unsupported + isolated/all-unklar
        if deg == "ohne_beleg":
            incident = adjacency.get(key, [])
            if not incident or all(d == "unklar" for d in incident):
                reasons.append("R2 ohne_beleg + " + ("structurally isolated" if not incident else "all incident edges unklar"))

        # R3 wrong country
        if "falsches_land" in flags:
            fl = next(f for f in (v.get("flags") or []) if (f.get("flag") if isinstance(f,dict) else f) == "falsches_land")
            land_soll = fl.get("land_soll", "") if isinstance(fl, dict) else ""
            if land_soll and land_soll.upper() not in DRAWN_PANELS:
                reasons.append(f"R3 wrong country (belongs to '{land_soll}', not a drawn panel)")

        if reasons:
            candidates.append({
                "cc": cc, "tid": tid, "eid": eid, "name": name,
                "actor_degree": deg, "reasons": reasons,
            })
        elif flags:
            kept_flagged.append({"cc": cc, "tid": tid, "name": name, "actor_degree": deg, "flags": flags})

    # coverage
    coverage = {}
    for cc in files_by_cc:
        graded = sum(1 for k in node_verdicts if k[0] == cc)
        total = country_node_count.get(cc, 0)
        coverage[cc] = f"{graded}/{total}"

    out = {
        "countries_done": sorted(files_by_cc.keys()),
        "coverage_nodes": coverage,
        "total_graded_nodes": len(node_verdicts),
        "total_candidates": len(candidates),
        "candidates": sorted(candidates, key=lambda c: (c["cc"], c["tid"])),
        "kept_flagged_not_candidates": sorted(kept_flagged, key=lambda c: (c["cc"], c["tid"])),
    }

    out_path = os.path.join(BASE, "prune_candidates_preview.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"Countries done: {out['countries_done']}")
    print(f"Coverage: {coverage}")
    print(f"Graded nodes: {out['total_graded_nodes']}")
    print(f"Removal candidates: {out['total_candidates']}")
    by_rule = defaultdict(int)
    for c in candidates:
        for r in c["reasons"]:
            by_rule[r.split(" ",1)[0]] += 1
    print("By rule:", dict(by_rule))
    print(f"Written: {out_path}")

if __name__ == "__main__":
    main()
