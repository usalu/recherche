"""Stage-gated regression harness for the netz refactor.

Run from the scratchpad dir: python netz/tests/run_checks.py [--stage N]

Stage 0 (current): byte-diff the legacy generators' output against the frozen
goldens (proves the canonicalization fix is stable / re-runnable), plus a
determinism self-check (regenerate twice in-process via subprocess, compare).
Later stages append: model-parity diff (Stage 2+), byte-diff of the netz/
package's own output against the same goldens (Stage 3+), a validation
report (Stage 6). This file grows additive checks; it never removes an
earlier stage's check, so `run_checks.py` always re-validates everything
achieved so far.
"""
import sys, os, json, subprocess, hashlib, ast, re

SP = r"E:/recherche/_neo4j/netz"
GOLD = os.path.join(SP, "netz", "tests", "golden")
if SP not in sys.path:
    sys.path.insert(0, SP)

FAILS = []


def check(name, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}" + (f" -- {detail}" if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def stage0_byte_diff():
    """Regenerate the legacy fragments fresh and diff against golden."""
    for gen, frag, golden in [
        ("gen_abb.py", "figs/frag_abb.tex", "frag_abb.tex"),
        ("gen_tables2.py", "figs/frag_tables2.tex", "frag_tables2.tex"),
    ]:
        r = subprocess.run([sys.executable, gen], cwd=SP, capture_output=True, text=True)
        ok = r.returncode == 0
        check(f"stage0.regen.{gen}", ok, r.stderr[-800:] if not ok else "")
        if not ok:
            continue
        got = sha(os.path.join(SP, frag))
        want = sha(os.path.join(GOLD, golden))
        check(f"stage0.golden.{golden}", got == want, f"{got[:12]} != {want[:12]}")


def stage0_determinism():
    """Regenerate twice in separate processes; both must match golden (already
    covers process-to-process determinism, since golden itself came from a
    fresh process in the Stage 0 canonicalization run)."""
    hashes = {"frag_abb.tex": set(), "frag_tables2.tex": set()}
    for _ in range(2):
        subprocess.run([sys.executable, "gen_abb.py"], cwd=SP, capture_output=True)
        subprocess.run([sys.executable, "gen_tables2.py"], cwd=SP, capture_output=True)
        hashes["frag_abb.tex"].add(sha(os.path.join(SP, "figs", "frag_abb.tex")))
        hashes["frag_tables2.tex"].add(sha(os.path.join(SP, "figs", "frag_tables2.tex")))
    for frag, hs in hashes.items():
        check(f"stage0.determinism.{frag}", len(hs) == 1, f"{len(hs)} distinct hashes across 2 processes")


def stage0_snapshot_present():
    path = os.path.join(GOLD, "model_snapshot.json")
    ok = os.path.exists(path)
    check("stage0.snapshot.exists", ok)
    if ok:
        snap = json.load(open(path, encoding="utf-8"))
        check("stage0.snapshot.land_fixed==5", snap.get("land_fixed") == 5, str(snap.get("land_fixed")))
        check("stage0.snapshot.extra_peer_pairs==175", snap.get("extra_peer_pairs") == 175, str(snap.get("extra_peer_pairs")))
        check("stage0.snapshot.countries==11", len(snap.get("countries", [])) == 11, str(len(snap.get("countries", []))))


def stage1_import_purity():
    """`data/` (and `model/` once it exists) must never import LaTeX/renderer
    code (net_lib.py's esc()/TYPE_ABBR, or netz.render.*) -- data describes
    what differs, not how it's drawn. Static AST scan, not a runtime import
    (avoids false negatives from lazy/conditional imports)."""
    forbidden_modules = {"net_lib", "gen_abb", "gen_tables2", "netplate"}
    data_dir = os.path.join(SP, "netz", "data")
    violations = []
    for fn in sorted(os.listdir(data_dir)):
        if not fn.endswith(".py"):
            continue
        path = os.path.join(data_dir, fn)
        tree = ast.parse(open(path, encoding="utf-8").read(), filename=fn)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in forbidden_modules or "render" in alias.name:
                        violations.append(f"{fn}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                if mod.split(".")[0] in forbidden_modules or "render" in mod:
                    violations.append(f"{fn}: from {mod} import ...")
    check("stage1.import_purity.no_latex_in_data", not violations, "; ".join(violations))


def stage1_data_layer():
    from netz.tests import check_stage1
    check_stage1.run(check)


def stage2_model_parity():
    from netz.tests import check_stage2
    check_stage2.run(check)


def stage3_graph_byte_parity():
    """Stage 3's live-regen-vs-golden byte-diff was the achievement gate WHILE
    graph_tikz.py still emitted literal legacy strings. Stage 4 intentionally
    switches it to style-name references (same rendered result, different
    bytes -- see stage4_pixel_parity), so re-running that same live comparison
    against current code would fail by design, not by regression. What stays
    checkable forever is the frozen historical proof: the Stage-3 snapshot
    (frag_abb_stage3_reference.tex, taken right before the Stage 4 edits)
    still matches the Stage 0 golden byte-for-byte."""
    got = sha(os.path.join(GOLD, "frag_abb_stage3_reference.tex"))
    want = sha(os.path.join(GOLD, "frag_abb.tex"))
    check("stage3.frozen_reference_matches_golden", got == want, f"{got[:12]} != {want[:12]}")

    r = subprocess.run([sys.executable, "-m", "netz.cli", "abb"], cwd=SP, capture_output=True, text=True)
    check("stage3.regen.netz.cli.abb", r.returncode == 0, r.stderr[-800:] if r.returncode else "")
    if r.returncode != 0:
        return
    hashes = set()
    for _ in range(2):
        subprocess.run([sys.executable, "-m", "netz.cli", "abb"], cwd=SP, capture_output=True)
        hashes.add(sha(os.path.join(SP, "figs", "frag_abb_netz.tex")))
    check("stage3.determinism.frag_abb_netz.tex", len(hashes) == 1, f"{len(hashes)} distinct hashes")


TECTONIC = r"E:/semio/.repo/cache/tectonic/0.16.9/tectonic.exe"
REPORT_DIR = r"E:/semio/mit-bestand/bericht/zwischenbericht"
FIGS = os.path.join(SP, "figs")


SEMIO_GRAPH_STY = r"E:/semio/print/tex/semio-graph.sty"


def stage6_pixel_parity():
    """Regenerate the graph fragment against print/tex/semio-graph.sty -- a
    first-class package (registered in semio.cls), not a spliced preamble
    fragment -- compile it, and raster-diff against the frozen Stage 5
    baseline PDF. This replaces stage4_pixel_parity: Stage 4's mechanism
    (preamble_netz.tex + \\SemioNetzWidePageBegin/End) no longer exists, so
    the check that gated it is retired rather than kept green for a macro
    that was deleted. Bytes differ from Stage 4 (semio-graph state names vs
    semio-netz style-name literals; the node radius also moves from a
    Python-rounded literal to an exact LaTeX token, see stage6_token_sync)
    but the styles expand to the same visual result, so the gate is pixel
    parity, not byte-diff."""
    r = subprocess.run([sys.executable, "-m", "netz.cli", "abb"], cwd=SP, capture_output=True, text=True)
    check("stage6.regen.netz.cli.abb", r.returncode == 0, r.stderr[-800:] if r.returncode else "")
    if r.returncode != 0:
        return

    r = subprocess.run([sys.executable, "build.py", "_abb_stage6.tex", "frag_abb_netz.tex"],
                        cwd=SP, capture_output=True, text=True)
    check("stage6.assemble", r.returncode == 0, (r.stdout + r.stderr)[-800:] if r.returncode else "")
    if r.returncode != 0:
        return

    tex_path = os.path.join(FIGS, "_abb_stage6.tex")
    pdf_path = os.path.join(FIGS, "_abb_stage6.pdf")
    r = subprocess.run([TECTONIC, "--keep-logs", "-Z", "search-path=E:/semio/print/tex",
                         "--outdir", FIGS, tex_path], cwd=REPORT_DIR, capture_output=True, text=True)
    check("stage6.compile", os.path.exists(pdf_path), (r.stdout + r.stderr)[-800:] if not os.path.exists(pdf_path) else "")
    if not os.path.exists(pdf_path):
        return

    from netz_pixeldiff import diff
    golden_pdf = os.path.join(GOLD, "baseline_abb.pdf")
    ok = diff(golden_pdf, pdf_path, dpi=150)
    check("stage6.pixel_parity", ok, f"{golden_pdf} vs {pdf_path}")


def stage7_graph_spec_generality():
    """The two real bugs fixed by turning the loader's ontology into a
    GraphSpec: (1) a node carrying more than one label used to silently
    vanish from every kind bucket (exact list-equality test); (2) an
    unlisted relationship type used to be silently ignored. Neither is
    exercisable against the current actors_network.json (no node in it
    carries two labels -- verified directly against the file), so both are
    proven here against synthetic minimal exports instead of relying on the
    live data to happen to trigger them."""
    import tempfile
    from netz.data.neo4j_export import load_export, ACTOR_NETWORK_SPEC

    multi_label = {
        "nodes": [
            {"eid": "a1", "labels": ["Akteur", "ExtraLabel"], "properties": {"name": "A"}},
        ],
        "relationships": [],
    }
    path = tempfile.mktemp(suffix=".json")
    json.dump(multi_label, open(path, "w", encoding="utf-8"))
    raw = load_export(path, ACTOR_NETWORK_SPEC)
    check("stage7.kind_resolution.multi_label_node_not_dropped", len(raw.actors) == 1,
          f"expected 1 actor, got {len(raw.actors)}")
    os.remove(path)

    unlisted_rel = {
        "nodes": [
            {"eid": "a1", "labels": ["Akteur"], "properties": {"name": "A"}},
            {"eid": "t1", "labels": ["Unmapped"], "properties": {"name": "X"}},
        ],
        "relationships": [{"type": "TOTALLY_UNSPECIFIED_REL", "start": "a1", "end": "t1"}],
    }
    path = tempfile.mktemp(suffix=".json")
    json.dump(unlisted_rel, open(path, "w", encoding="utf-8"))
    try:
        load_export(path, ACTOR_NETWORK_SPEC)
        check("stage7.unlisted_relationship_type_raises", False, "no error raised")
    except ValueError:
        check("stage7.unlisted_relationship_type_raises", True)
    os.remove(path)


def stage6_token_sync():
    """layout.NODE_R is the collision radius feeding the force sim's MIN_D;
    \\semio@graph@node@radius is the drawn radius. They are two languages'
    views of one design token and nothing enforces they agree except this
    check -- the pixel gate can't see it, since it only manifests as
    overlapping circles on FUTURE data with different node counts/spacing."""
    from netz.mechanisms import layout
    sty = open(SEMIO_GRAPH_STY, encoding="utf-8").read()
    m = re.search(r"\\providecommand\{\\semio@graph@node@radius\}\{([0-9.]+)mm\}", sty)
    ok = bool(m) and abs(float(m.group(1)) - layout.NODE_R) < 1e-9
    check("stage6.token_sync.node_radius", ok,
          f"sty={m and m.group(1)} python={layout.NODE_R}")


def stage8_node_parity():
    """The drawn nodes must be EXACTLY the strict review's approved set --
    not a superset (a leaked prune/programme) and not a subset (something
    silently dropped). Checked once by hand during the fact-check
    integration (620 == 620, zero leaks); this is that same check made
    permanent so a future data change can't regress it unnoticed."""
    from netz.sources import DEFAULT
    from netz.cli import load_network
    from netz.data.prune import load_prune

    net = load_network()
    drawn = set()
    for pan in net.panels.values():
        drawn |= set(pan.actors) | set(pan.projects)

    approved = set(json.load(open(DEFAULT.klassifikation_actor_project_path, encoding="utf-8")))
    programmes = set(json.load(open(DEFAULT.programme_path, encoding="utf-8")))
    pruned = load_prune(DEFAULT.prune_strict_path) | load_prune(DEFAULT.prune_faktencheck_path)

    check("stage8.nodes.drawn==approved", drawn == approved,
          f"missing={len(approved - drawn)} extra={len(drawn - approved)}")
    check("stage8.nodes.no_programme_leak", not (drawn & programmes),
          f"{len(drawn & programmes)} programme eid(s) drawn")
    check("stage8.nodes.no_prune_leak", not (drawn & pruned),
          f"{len(drawn & pruned)} pruned eid(s) drawn")


def stage8_table_figure_edge_parity():
    """The relationship table and the graph figure must show the SAME edges.
    Found manually by counting both to 268 and still finding a 1-for-1
    mismatch (a cross-border pair in the table but not the figure, a
    merge-redirected pair in the figure but not the table) -- the totals
    agreeing hid it completely, so this checks the actual SET, not the count.
    Root causes, both fixed in table_grid.load_kanten: edges were checked
    against `set(net.tid)` (everything the pipeline knows) instead of
    `net.drawn` (what partition() actually draws across a panel boundary),
    and eids weren't canonicalized through the strict review's merge
    redirects before the join."""
    from netz.sources import DEFAULT
    from netz.cli import load_network
    from netz.render.latex.table_grid import load_kanten

    net = load_network()
    drawn_pairs = {tuple(sorted(p)) for p in net.drawn}

    kanten = load_kanten(DEFAULT.kanten_klassifikation_path, net, DEFAULT.merge_strict_path)
    table_pairs = {tuple(sorted(k["pair"])) for cc in kanten for k in kanten[cc]}

    check("stage8.edges.table==figure", drawn_pairs == table_pairs,
          f"in figure only={len(drawn_pairs - table_pairs)} in table only={len(table_pairs - drawn_pairs)}")


def main():
    print("=== Stage 0: canonicalization + golden freeze + determinism ===")
    stage0_snapshot_present()
    stage0_byte_diff()
    stage0_determinism()

    print()
    print("=== Stage 1: data layer (pure loaders + overlay merge) ===")
    stage1_import_purity()
    stage1_data_layer()

    print()
    print("=== Stage 2: semantic model + identity/country/connectivity mechanisms ===")
    stage2_model_parity()

    print()
    print("=== Stage 3: graph slice, byte parity ===")
    stage3_graph_byte_parity()

    print()
    print("=== Stage 7: generic Neo4j import (GraphSpec) ===")
    stage7_graph_spec_generality()

    print()
    print("=== Stage 6: semio-graph.sty mechanism (network styles + wide-page macros), pixel parity ===")
    stage6_pixel_parity()
    stage6_token_sync()

    print()
    print("=== Stage 8: akteursnetz fact-check integration -- node/edge set parity ===")
    stage8_node_parity()
    stage8_table_figure_edge_parity()

    print()
    if FAILS:
        print(f"RESULT: FAIL ({len(FAILS)} check(s) failed: {', '.join(FAILS)})")
        sys.exit(1)
    else:
        print("RESULT: PASS (all checks green)")


if __name__ == "__main__":
    main()
