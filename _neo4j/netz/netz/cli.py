"""netz CLI: builds the Network once (no import-time side effects, unlike the
legacy generators) and dispatches to a renderer. `python -m netz.cli abb`.
"""
import sys, os, argparse, shutil

SP = r"E:/recherche/_neo4j/netz"

from .sources import DEFAULT
from .data.prune import load_prune, load_edge_exclude
from .data.corrections import load_country_overrides
from .data.strict_review import load_strict_review
from .model.concepts import build_network
from .render.latex.graph_tikz import (country_figure, load_image_manifest,
                                      load_edge_kinds, manifest_rows)
from .render.latex.framing import assemble_graph_fragment, GRAPH_LEGEND
from .render.latex.table_long import country_table, role_frequency, TABLE_LEGEND
from .render.latex.framing import assemble_spread_fragment
from .render.latex.fragments import write_fragment
from .render.latex.table_grid import build_grid_fragment
from .render.latex.programme_table import build_programme_fragment

GRAPH_SECTION_TITLE = "Akteursnetze nach Land"
TABLE_SECTION_TITLE = "Akteursbeziehungen"


def build_graph_fragment(net, out_path: str, images=None, countries=None, edge_kinds=None):
    order = [cc for cc in net.countries
             if cc in net.panels and (net.panels[cc].actors or net.panels[cc].projects)]
    if countries:
        requested = set(countries)
        order = [cc for cc in order if cc in requested]
    figures = []
    tot = 0
    for cc in order:
        r = country_figure(net, cc, images=images, edge_kinds=edge_kinds)
        if not r:
            continue
        frag, nA, nP, nd, nfill = r
        figures.append(frag)
        tot += nd
    text = assemble_graph_fragment(GRAPH_SECTION_TITLE, GRAPH_LEGEND, figures)
    write_fragment(out_path, text)
    return tot, len(order)


def build_table_fragment(net, out_path: str):
    rf = role_frequency(net)
    order = [cc for cc in net.countries if cc in net.panels]
    tables = []
    for cc in order:
        t = country_table(net, cc, rf)
        if t:
            tables.append(t)
    text = assemble_spread_fragment(TABLE_SECTION_TITLE, TABLE_LEGEND, tables)
    write_fragment(out_path, text)
    return len(tables)


def load_network():
    strict = load_strict_review(
        DEFAULT.strict_manifest_path,
        DEFAULT.prune_strict_path,
        DEFAULT.merge_strict_path,
        DEFAULT.report_overrides_strict_path,
        DEFAULT.klassifikation_final_path,
    )
    exclude = (load_prune(DEFAULT.prune_path) |
               load_prune(DEFAULT.prune_faktencheck_path) |
               strict.exclude |
               strict.programmes)
    edge_exclude = (load_edge_exclude(DEFAULT.unklar_edges_path) |
                    load_edge_exclude(DEFAULT.prune_kanten_final_path) |
                    load_edge_exclude(DEFAULT.prune_beziehungsprofil_final_path))
    country_overrides = load_country_overrides(DEFAULT.latex_country_overrides_path)
    return build_network(DEFAULT, exclude=exclude, edge_exclude=edge_exclude,
                         strict_review=strict, country_overrides=country_overrides)


def sync_images(manifest_path: str, asset_root: str):
    """Copy the freigegebene Logos into the report's own asset tree.

    The report keeps its images next to itself (`asset/projekt/`,
    `asset/logo/`, `asset/katalog/`) and names them relatively; the review
    workspace is transport, not a place the built document may reach into.
    So the fragments must never carry an `E:/recherche/...` path, and this
    step is what makes that true rather than a promise.

    Dateiname bleibt `<CC>/<TID>.png` aus dem Manifest, NICHT die im Bericht
    gedruckte ID: die Pruefung, ihre Pruefboegen und ihre SHA-256-Liste sind
    ueber TID gefuehrt, und die gedruckte ID wandert bei jeder Neubelegung
    des Netzes. Ein `-dark`-Nachbar wird mitkopiert, weil semio-logo.sty ihn
    ueber genau diesen Namen aufloest.

    Idempotent: Dateien, die das Manifest nicht mehr nennt, werden entfernt.
    """
    rows = manifest_rows(manifest_path)
    base = os.path.dirname(os.path.abspath(manifest_path))
    want, copied, dark = set(), 0, 0
    for row in rows:
        src = os.path.join(base, *row["asset_path"].split("/"))
        if not os.path.isfile(src):
            continue
        for s_path, rel in ((src, "%s/%s.png" % (row["cc"], row["tid"])),
                            (os.path.join(base, *(row.get("dark_asset_path") or "").split("/"))
                             if row.get("dark_asset_path") else None,
                             "%s/%s-dark.png" % (row["cc"], row["tid"]))):
            if not s_path or not os.path.isfile(s_path):
                continue
            dst = os.path.join(asset_root, *rel.split("/"))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(s_path, dst)
            want.add(os.path.normcase(os.path.abspath(dst)))
            if rel.endswith("-dark.png"):
                dark += 1
            else:
                copied += 1
    removed = 0
    for root, _, files in os.walk(asset_root):
        for f in files:
            full = os.path.join(root, f)
            if os.path.normcase(os.path.abspath(full)) not in want:
                os.remove(full)
                removed += 1
    return copied, dark, removed


def sync_fragments(anhang_root: str):
    """Copy the generated fragments into the report's anhang/ directory.

    Same reason as sync_images: the two repositories have no shared build, so
    the handoff was a manual copy. A forgotten copy prints an old state
    silently -- the report compiles perfectly either way.
    """
    done, missing = [], []
    for src_name, dst_name in DEFAULT.report_fragments:
        src = os.path.join(SP, "figs", src_name)
        if not os.path.isfile(src):
            missing.append(src_name)
            continue
        shutil.copy2(src, os.path.join(anhang_root, dst_name))
        done.append(dst_name)
    return done, missing


def _asset_mode(args):
    """(asset_root, asset_ref) for load_image_manifest, or (None, None)."""
    if args.image_paths == "absolute":
        return None, None
    return args.asset_root or DEFAULT.report_asset_root, DEFAULT.report_asset_ref


def main():
    ap = argparse.ArgumentParser(prog="netz")
    ap.add_argument("cmd", choices=["abb", "tables", "tables-grid", "programme",
                                    "sync-images", "sync-fragments"])
    ap.add_argument("--out", default=None)
    ap.add_argument("--images-manifest", default=None,
                    help="accepted image transport manifest; defaults to "
                         "sources.images_manifest_path for sync-images")
    ap.add_argument("--asset-root", default=None,
                    help="report asset directory the logos are copied into "
                         "(sync-images) and resolved against (abb/tables-grid)")
    ap.add_argument("--image-paths", choices=["report", "absolute"], default="report",
                    help="'report' (default) emits asset/akteur/<CC>/<TID>.png, "
                         "resolved by the report's own TeX run. 'absolute' emits "
                         "the review-workspace path, for standalone compiles "
                         "outside the report tree.")
    ap.add_argument("--countries", default=None,
                    help="comma-separated ISO2 panel filter (abb only)")
    args = ap.parse_args()

    if args.cmd == "sync-images":
        n, d, r = sync_images(args.images_manifest or DEFAULT.images_manifest_path,
                              args.asset_root or DEFAULT.report_asset_root)
        print(f"synced {n} logos (+{d} dark) into "
              f"{args.asset_root or DEFAULT.report_asset_root}, removed {r} stale")
        return

    if args.cmd == "sync-fragments":
        done, missing = sync_fragments(DEFAULT.report_anhang_root)
        print(f"synced {len(done)} fragments into {DEFAULT.report_anhang_root}: "
              + ", ".join(done))
        if missing:
            print("not generated yet, skipped: " + ", ".join(missing))
        return

    if args.cmd == "programme":
        out = args.out or os.path.join(SP, "figs", "frag_programme.tex")
        n = build_programme_fragment(DEFAULT, out)
        print(f"wrote {out}: {n} programmes")
        return

    net = load_network()
    if args.cmd == "abb":
        out = args.out or os.path.join(SP, "figs", "frag_abb_netz.tex")
        images = load_image_manifest(args.images_manifest, *_asset_mode(args))
        countries = ([c.strip().upper() for c in args.countries.split(",") if c.strip()]
                     if args.countries else None)
        unknown = sorted(set(countries or []) - set(net.panels))
        if unknown:
            ap.error("unknown country panel(s): %s" % ", ".join(unknown))
        edge_kinds = load_edge_kinds(
            DEFAULT.kanten_klassifikation_path,
            net,
            DEFAULT.merge_strict_path,
            DEFAULT.expansion_kanten_path,
        )
        tot, n = build_graph_fragment(net, out, images=images, countries=countries, edge_kinds=edge_kinds)
        print(f"wrote {out}: {tot} nodes across {n} country figures")
    elif args.cmd == "tables":
        out = args.out or os.path.join(SP, "figs", "frag_tables_netz.tex")
        n = build_table_fragment(net, out)
        print(f"wrote {out}: {n} country tables")
    elif args.cmd == "tables-grid":
        out = args.out or os.path.join(SP, "figs", "frag_tables_grid.tex")
        n_items, n_pages = build_grid_fragment(
            net, out, DEFAULT.klassifikation_actor_project_path,
            DEFAULT.kanten_klassifikation_path,
            load_image_manifest(args.images_manifest, *_asset_mode(args)),
            DEFAULT.merge_strict_path,
            DEFAULT.expansion_klassifikation_path,
            DEFAULT.expansion_kanten_path)
        print(f"wrote {out}: {n_items} rows/headers across {n_pages} pages")


if __name__ == "__main__":
    main()
