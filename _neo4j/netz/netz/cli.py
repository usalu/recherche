"""netz CLI: builds the Network once (no import-time side effects, unlike the
legacy generators) and dispatches to a renderer. `python -m netz.cli abb`.
"""
import sys, os, argparse

SP = r"E:/recherche/_neo4j/netz"

from .sources import DEFAULT
from .data.prune import load_prune, load_edge_exclude
from .data.corrections import load_country_overrides
from .data.strict_review import load_strict_review
from .model.concepts import build_network
from .render.latex.graph_tikz import country_figure, load_image_manifest
from .render.latex.framing import assemble_graph_fragment, GRAPH_LEGEND
from .render.latex.table_long import country_table, role_frequency, TABLE_LEGEND
from .render.latex.framing import assemble_spread_fragment
from .render.latex.fragments import write_fragment
from .render.latex.table_grid import build_grid_fragment
from .render.latex.programme_table import build_programme_fragment

GRAPH_SECTION_TITLE = "Akteursnetze nach Land"
TABLE_SECTION_TITLE = "Akteurstabellen nach Land"


def build_graph_fragment(net, out_path: str, images=None, countries=None):
    order = [cc for cc in net.countries
             if cc in net.panels and (net.panels[cc].actors or net.panels[cc].projects)]
    if countries:
        requested = set(countries)
        order = [cc for cc in order if cc in requested]
    figures = []
    tot = 0
    for cc in order:
        r = country_figure(net, cc, images=images)
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
                    load_edge_exclude(DEFAULT.prune_kanten_final_path))
    country_overrides = load_country_overrides(DEFAULT.latex_country_overrides_path)
    return build_network(DEFAULT, exclude=exclude, edge_exclude=edge_exclude,
                         strict_review=strict, country_overrides=country_overrides)


def main():
    ap = argparse.ArgumentParser(prog="netz")
    ap.add_argument("cmd", choices=["abb", "tables", "tables-grid", "programme"])
    ap.add_argument("--out", default=None)
    ap.add_argument("--images-manifest", default=None,
                    help="optional accepted pilot-image transport manifest")
    ap.add_argument("--countries", default=None,
                    help="comma-separated ISO2 panel filter (abb only)")
    args = ap.parse_args()

    if args.cmd == "programme":
        out = args.out or os.path.join(SP, "figs", "frag_programme.tex")
        n = build_programme_fragment(DEFAULT, out)
        print(f"wrote {out}: {n} programmes")
        return

    net = load_network()
    if args.cmd == "abb":
        out = args.out or os.path.join(SP, "figs", "frag_abb_netz.tex")
        images = load_image_manifest(args.images_manifest)
        countries = ([c.strip().upper() for c in args.countries.split(",") if c.strip()]
                     if args.countries else None)
        unknown = sorted(set(countries or []) - set(net.panels))
        if unknown:
            ap.error("unknown country panel(s): %s" % ", ".join(unknown))
        tot, n = build_graph_fragment(net, out, images=images, countries=countries)
        print(f"wrote {out}: {tot} nodes across {n} country figures")
    elif args.cmd == "tables":
        out = args.out or os.path.join(SP, "figs", "frag_tables_netz.tex")
        n = build_table_fragment(net, out)
        print(f"wrote {out}: {n} country tables")
    elif args.cmd == "tables-grid":
        out = args.out or os.path.join(SP, "figs", "frag_tables_grid.tex")
        n_items, n_pages = build_grid_fragment(
            net, out, DEFAULT.klassifikation_actor_project_path,
            DEFAULT.kanten_klassifikation_path, load_image_manifest(args.images_manifest))
        print(f"wrote {out}: {n_items} rows/headers across {n_pages} pages")


if __name__ == "__main__":
    main()
