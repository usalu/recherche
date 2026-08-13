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

    # Packet -> country comes from the packet itself, never from the file name:
    # grouped shards (shard_DK-SE-*.json, shard_FI-NO-*.json) carry two countries
    # in one file, and a name-derived cc would silently file every SE verdict
    # under DK.
    packets_by_cc = defaultdict(list)     # cc -> [packet_id]
    seen_packets = set()
    failed_somewhere = set()

    node_verdicts = {}   # (cc,tid) -> verdict dict
    edge_verdicts = {}   # (cc,a,b frozenset) -> verdict dict
    adjacency = defaultdict(list)  # (cc,tid) -> list of edge_degree
    gaps = []            # {cc, packet_id, tid, why}

    for path in sorted(glob.glob(os.path.join(RAW, "shard_*.json"))):
        data = load(path)
        result = data.get("result", data)
        for pkt in result.get("packets", []):
            pid = pkt.get("packet_id", "?")
            cc = pkt.get("cc") or os.path.basename(path)[len("shard_"):-len(".json")].split("-")[0]
            if pid in seen_packets:
                print(f"  ! packet {pid} appears in more than one raw file -- later file wins")
            seen_packets.add(pid)
            packets_by_cc[cc].append(pid)

            for n in pkt.get("nodes", []):
                node_verdicts[(cc, n["tid"])] = n
            for e in pkt.get("edges", []):
                a, b = e["a_tid"], e["b_tid"]
                edge_verdicts[(cc, frozenset((a, b)))] = e
                deg = e.get("edge_degree")
                adjacency[(cc, a)].append(deg)
                adjacency[(cc, b)].append(deg)

            # plan's anti-silent-truncation assertion: assigned == graded + gaps
            assigned = pkt.get("assigned_nodes") or []
            graded = {n["tid"] for n in pkt.get("nodes", [])}
            unchecked = set(pkt.get("ungeprueft_tids") or [])
            for tid in assigned:
                if tid not in graded:
                    gaps.append({"cc": cc, "packet_id": pid, "tid": tid,
                                 "why": "ungeprueft_tids" if tid in unchecked else "nicht zurueckgemeldet"})
            missing = [t for t in assigned if t not in graded]
            if assigned and len(graded) + len(missing) != len(assigned):
                print(f"  ! packet {pid}: assigned={len(assigned)} graded={len(graded)} gaps={len(missing)}")

        # A packet that failed in one run was usually re-run later, so only
        # report the ones still missing after every raw file is read.
        failed_somewhere.update(result.get("ausgefallen", []) or [])

    for pid in sorted(failed_somewhere - seen_packets):
        print(f"  ! packet {pid} failed and was never successfully re-run")

    files_by_cc = packets_by_cc

    # Adversarial verify-pass disposition (manual, one-time): demotions for
    # confirmed-fabricated citations, and reconciliation notes for citations
    # that were unreachable at verify time but independently reconfirmed on
    # manual follow-up. Applied before rule computation so R1-R3 see the
    # corrected degree.
    overrides_path = os.path.join(BASE, "verify_overrides.json")
    if os.path.exists(overrides_path):
        overrides = load(overrides_path)
        for d in overrides.get("demote", []):
            key = (d["cc"], d["tid"])
            v = node_verdicts.get(key)
            if v is None:
                print(f"  ! verify_overrides.json: demote target {key} not in node_verdicts")
                continue
            v["actor_degree"] = d["to_degree"]
            v["verify_note"] = d["reason"]
            print(f"  verify demote: {key} {d['from_degree']} -> {d['to_degree']}")
        for r in overrides.get("reconcile", []):
            key = (r["cc"], r["tid"])
            v = node_verdicts.get(key)
            if v is None:
                print(f"  ! verify_overrides.json: reconcile target {key} not in node_verdicts")
                continue
            v["verify_note"] = r["note"]

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

    # Manual R3 addition: merge_verdicts.py's R3 rule checks land_soll, which
    # by construction is always a drawn panel, so R3 can structurally never
    # fire (see docstring). Not fixed generally -- of the 7 falsches_land
    # flags, 2 (NL BlueCity, Workspot) are stored-URL mixups with same-named
    # foreign companies, not real country errors, and a naive land_ist swap
    # would wrongly nominate them too. Exactly one case is a genuine R3 match:
    # NL/U25 "EDGE (SXB S.a r.l.)" -- flagged land_ist=LU, and LU is not one
    # of the 11 drawn panels. Added by hand, reasoning verified against the
    # flag's own beleg_url/beleg_zitat.
    MANUAL_R3 = [("NL", "U25", "SXB S.a r.l. is registered in Luxembourg (land_ist=LU); "
                                "Luxembourg is not a drawn panel")]
    for cc, tid, why in MANUAL_R3:
        key = (cc, tid)
        if any(c["cc"] == cc and c["tid"] == tid for c in candidates):
            continue
        meta = node_meta.get(key, {})
        v = node_verdicts.get(key, {})
        candidates.append({
            "cc": cc, "tid": tid, "eid": meta.get("eid", ""), "name": meta.get("name", tid),
            "actor_degree": v.get("actor_degree"),
            "reasons": [f"R3 wrong country (manual: {why})"],
        })
        # this node was flagged but reasonless under the buggy general rule,
        # so the main loop already put it in kept_flagged -- it's a candidate
        # now, remove the stale duplicate entry.
        kept_flagged[:] = [k for k in kept_flagged if not (k["cc"] == cc and k["tid"] == tid)]

    # coverage -- over ALL countries in the worklist, not just the ones with a
    # raw file, so untouched panels show as 0/N instead of vanishing.
    coverage = {}
    incomplete = []
    for cc in sorted(country_node_count):
        graded = sum(1 for k in node_verdicts if k[0] == cc)
        total = country_node_count[cc]
        coverage[cc] = f"{graded}/{total}"
        if graded < total:
            incomplete.append(cc)
    complete = not incomplete
    total_nodes = sum(country_node_count.values())

    out = {
        "countries_done": sorted(files_by_cc.keys()),
        "coverage_complete": complete,
        "coverage_incomplete_ccs": incomplete,
        "coverage_nodes": coverage,
        "coverage_total": f"{len(node_verdicts)}/{total_nodes}",
        "total_graded_nodes": len(node_verdicts),
        "total_candidates": len(candidates),
        "candidates": sorted(candidates, key=lambda c: (c["cc"], c["tid"])),
        "kept_flagged_not_candidates": sorted(kept_flagged, key=lambda c: (c["cc"], c["tid"])),
    }

    out_path = os.path.join(BASE, "prune_candidates_preview.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    # canonical merged verdicts (audit trail, input to emit_review.py)
    verdicts_path = os.path.join(BASE, "verdicts.json")
    with open(verdicts_path, "w", encoding="utf-8") as f:
        json.dump({
            "coverage_complete": complete,
            "coverage_nodes": coverage,
            "nodes": [dict(v, cc=k[0], eid=node_meta.get(k, {}).get("eid", ""),
                           name=v.get("name") or node_meta.get(k, {}).get("name", ""))
                      for k, v in sorted(node_verdicts.items())],
            "edges": [dict(v, cc=k[0]) for k, v in sorted(edge_verdicts.items(), key=lambda kv: (kv[0][0], sorted(kv[0][1])))],
        }, f, indent=2, ensure_ascii=False)

    # everything not reached, and why
    coverage_path = os.path.join(BASE, "coverage_log.json")
    packets_done = {pid for pids in packets_by_cc.values() for pid in pids}
    packets_open = sorted(p["packet_id"] for p in wl["packets"] if p["packet_id"] not in packets_done)
    with open(coverage_path, "w", encoding="utf-8") as f:
        json.dump({
            "coverage_nodes": coverage,
            "packets_open": packets_open,
            "ungeprueft": sorted(gaps, key=lambda g: (g["cc"], g["packet_id"], g["tid"])),
        }, f, indent=2, ensure_ascii=False)

    # The applicable removal list is only written once every panel is graded --
    # a partial prune list is exactly the silent country-drop the plan warns about.
    prune_path = os.path.join(BASE, "prune_faktencheck.json")
    if complete:
        eids = sorted({c["eid"] for c in candidates if c["eid"]})
        with open(prune_path, "w", encoding="utf-8") as f:
            json.dump(eids, f, indent=2, ensure_ascii=False)
        with open(os.path.join(BASE, "prune_faktencheck_provenance.json"), "w", encoding="utf-8") as f:
            json.dump({"generated_from": "verdicts.json", "rules": ["R1", "R2", "R3"],
                       "entries": sorted(candidates, key=lambda c: (c["cc"], c["tid"]))},
                      f, indent=2, ensure_ascii=False)

    print(f"Countries done: {out['countries_done']}")
    print(f"Coverage: {coverage}")
    print(f"Graded nodes: {out['total_graded_nodes']}/{total_nodes}")
    print(f"Ungeprueft (assigned but no verdict): {len(gaps)}")
    print(f"Removal candidates: {out['total_candidates']}")
    by_rule = defaultdict(int)
    for c in candidates:
        for r in c["reasons"]:
            by_rule[r.split(" ",1)[0]] += 1
    print("By rule:", dict(by_rule))
    print(f"Written: {out_path}")
    print(f"Written: {verdicts_path}")
    print(f"Written: {coverage_path}")
    if complete:
        print(f"Written: {prune_path} (+ provenance)")
    else:
        print(f"NOT written: prune_faktencheck.json -- coverage incomplete for {incomplete}")
        print(f"  open packets: {len(packets_open)}")

if __name__ == "__main__":
    main()
