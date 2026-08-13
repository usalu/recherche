"""Stage 0: dump the legacy Model's internals as the parity oracle for Stage 2+.

Run from the scratchpad dir: python netz/tests/dump_snapshot.py
Writes netz/tests/golden/model_snapshot.json. Legacy-only script -- imports
the OLD net_lib/netplate/gen_abb chain, never imported by netz/ itself.
"""
import sys, os, json

SP = r"E:/recherche/_neo4j/netz"
sys.path.insert(0, SP)

import gen_abb as G   # noqa: E402  (builds the legacy Model with overlays+audit+prune already applied)

m = G.m
n = m.n

snap = {
    "actor_count": len(n.actors),
    "project_count": len(n.projects),
    "land_fixed": n.land_fixed,
    "extra_peer_pairs": n.extra_peer_pairs,
    "new_eids_count": len(n.new_eids),
    "countries": m.countries,
    "unplaced_count": len(m.unplaced),
    "inferred": sorted(m.inferred),
    "cc": {e: v for e, v in sorted(m.cc.items())},
    "tid": {e: v for e, v in sorted(m.tid.items())},
    "panels": {
        cc: {
            "A": pan["A"],                     # already sorted by name in Model
            "P": pan["P"],
            "E": [list(k) for k in pan["E"]],   # canonical order now (Stage 0 fix)
        }
        for cc, pan in sorted(m.panels.items())
    },
    "aset_size": len(m.aset),
    "prune_eids_count": len(G._prune_eids),
}

out_path = os.path.join(SP, "netz", "tests", "golden", "model_snapshot.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(snap, f, ensure_ascii=False, indent=1, sort_keys=True)

print(f"actors={snap['actor_count']} projects={snap['project_count']} "
      f"land_fixed={snap['land_fixed']} extra_peer_pairs={snap['extra_peer_pairs']} "
      f"countries={len(snap['countries'])} inferred={len(snap['inferred'])} "
      f"unplaced={snap['unplaced_count']} prune={snap['prune_eids_count']}")
print("wrote", out_path)
