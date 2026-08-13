"""Stage 1 parity checks: pure data layer vs the Stage 0 model_snapshot.json
oracle. Callable standalone or imported by run_checks.py.
"""
import sys, os, json

SP = r"E:/recherche/_neo4j/netz"
if SP not in sys.path:
    sys.path.insert(0, SP)

from netz.sources import DEFAULT
from netz.data.neo4j_export import load_export
from netz.data.overlays import apply_overlays
from netz.data.audit_edges import load_peer_edges
from netz.data.prune import load_prune


def run(check_fn):
    """check_fn(name, ok, detail) -- injected by the caller (run_checks.py) so
    this module has no print-vs-assert duplication with the main harness."""
    raw = load_export(DEFAULT.export_path)
    check_fn("stage1.raw.actor_count==677", len(raw.actors) == 677, str(len(raw.actors)))
    check_fn("stage1.raw.project_count==74", len(raw.projects) == 74, str(len(raw.projects)))
    check_fn("stage1.raw.land_fixed==5", raw.land_fixed == 5, str(raw.land_fixed))

    new_eids, new_proj_cc, reports = apply_overlays(raw, DEFAULT.overlay_paths)
    expected_entities = [56, 83, 444]
    for i, (rpt, exp) in enumerate(zip(reports, expected_entities)):
        check_fn(f"stage1.overlay[{i}].entities_added=={exp}", rpt.entities_added == exp,
                  str(rpt.entities_added))
    total_new = sum(r.entities_added for r in reports)
    check_fn("stage1.overlay.total_entities==583", total_new == 583, str(total_new))

    snap_path = os.path.join(SP, "netz", "tests", "golden", "model_snapshot.json")
    snap = json.load(open(snap_path, encoding="utf-8"))
    check_fn("stage1.new_eids_count==snapshot", len(new_eids) == snap["new_eids_count"],
              f"{len(new_eids)} != {snap['new_eids_count']}")
    check_fn("stage1.actor_count_after_overlay==snapshot", len(raw.actors) == snap["actor_count"],
              f"{len(raw.actors)} != {snap['actor_count']}")

    edges = load_peer_edges(DEFAULT.audit_edges_path)
    check_fn("stage1.audit_edges.raw_count==175", len(edges) == 175, str(len(edges)))

    pruned = load_prune(DEFAULT.prune_path)
    check_fn("stage1.prune.count==87", len(pruned) == 87, str(len(pruned)))

    # observability: overlay name-join misses the legacy code silently drops
    misses = sum(len(r.unresolved_to_known_names) for r in reports)
    print(f"  (info) unresolved to_known name-joins across overlays: {misses}")


if __name__ == "__main__":
    fails = []

    def _check(name, ok, detail=""):
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail and not ok else ""))
        if not ok:
            fails.append(name)

    run(_check)
    print()
    print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)}: {', '.join(fails)})")
    sys.exit(0 if not fails else 1)
