"""Stage 2 parity checks: semantic model (Network) vs model_snapshot.json,
field by field. Callable standalone or imported by run_checks.py.
"""
import sys, os, json

SP = r"E:/recherche/_neo4j/netz"
if SP not in sys.path:
    sys.path.insert(0, SP)

from netz.sources import DEFAULT
from netz.data.prune import load_prune
from netz.model.concepts import build_network
from netz.mechanisms.connectivity import drawn_edge_nodes


def run(check_fn):
    snap_path = os.path.join(SP, "netz", "tests", "golden", "model_snapshot.json")
    snap = json.load(open(snap_path, encoding="utf-8"))

    exclude = load_prune(DEFAULT.prune_path)
    net = build_network(DEFAULT, exclude=exclude)

    check_fn("stage2.land_fixed==snapshot", net.raw.land_fixed == snap["land_fixed"],
              f"{net.raw.land_fixed} != {snap['land_fixed']}")
    check_fn("stage2.extra_peer_pairs==snapshot", net.audit_edges_applied == snap["extra_peer_pairs"],
              f"{net.audit_edges_applied} != {snap['extra_peer_pairs']}")
    check_fn("stage2.new_eids_count==snapshot", len(net.new_eids) == snap["new_eids_count"],
              f"{len(net.new_eids)} != {snap['new_eids_count']}")
    check_fn("stage2.aset_size==snapshot", len(net.aset) == snap["aset_size"],
              f"{len(net.aset)} != {snap['aset_size']}")
    check_fn("stage2.unplaced_count==snapshot", len(net.res.unplaced) == snap["unplaced_count"],
              f"{len(net.res.unplaced)} != {snap['unplaced_count']}")
    check_fn("stage2.countries==snapshot", net.countries == snap["countries"],
              f"{net.countries} != {snap['countries']}")
    check_fn("stage2.inferred==snapshot", sorted(net.res.inferred) == snap["inferred"],
              f"{len(net.res.inferred)} eids differ from snapshot's {len(snap['inferred'])}")
    check_fn("stage2.cc==snapshot", net.res.cc == snap["cc"],
              f"{len(net.res.cc)} entries, {sum(1 for k in net.res.cc if net.res.cc.get(k)!=snap['cc'].get(k))} differ")
    check_fn("stage2.tid==snapshot", net.tid == snap["tid"],
              f"{len(net.tid)} entries, {sum(1 for k in net.tid if net.tid.get(k)!=snap['tid'].get(k))} differ")

    panel_ok = True
    panel_detail = []
    for cc, pan_snap in snap["panels"].items():
        pan = net.panels.get(cc)
        if pan is None:
            panel_ok = False; panel_detail.append(f"{cc}: MISSING")
            continue
        if pan.actors != pan_snap["A"]:
            panel_ok = False; panel_detail.append(f"{cc}.A differs")
        if pan.projects != pan_snap["P"]:
            panel_ok = False; panel_detail.append(f"{cc}.P differs")
        got_e = [list(k) for k in pan.edges]
        if got_e != pan_snap["E"]:
            panel_ok = False; panel_detail.append(f"{cc}.E differs ({len(got_e)} vs {len(pan_snap['E'])})")
    check_fn("stage2.panels==snapshot (A/P/E incl. order)", panel_ok, "; ".join(panel_detail))

    # connectivity mechanism vs legacy netplate.drawn_nodes (not in the
    # snapshot -- compared directly against a fresh legacy Model here).
    try:
        import netplate as _legacy_netplate
        import gen_abb as _legacy_gen_abb
        legacy_m = _legacy_gen_abb.m
        conn_ok = True
        conn_detail = []
        for cc in net.countries:
            new_keep = drawn_edge_nodes(net.panels[cc])
            old_keep = _legacy_netplate.drawn_nodes(cc, legacy_m)
            if new_keep != old_keep:
                conn_ok = False
                conn_detail.append(f"{cc}: {len(new_keep)} vs {len(old_keep)}")
        check_fn("stage2.connectivity.drawn_edge_nodes==legacy (all 11 countries)", conn_ok, "; ".join(conn_detail))
    except Exception as exc:  # pragma: no cover -- legacy import shouldn't normally fail
        check_fn("stage2.connectivity.drawn_edge_nodes==legacy (all 11 countries)", False, str(exc))


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
