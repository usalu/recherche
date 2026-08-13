"""netz CLI: builds the Network once (no import-time side effects, unlike the
legacy generators) and dispatches to a renderer. `python -m netz.cli abb`.
"""
import sys, os, argparse

SP = r"E:/recherche/_neo4j/netz"

from .sources import DEFAULT
from .data.prune import load_prune
from .model.concepts import build_network
from .render.latex.graph_tikz import country_figure
from .render.latex.framing import assemble_graph_fragment, GRAPH_LEGEND
from .render.latex.table_long import country_table, role_frequency, TABLE_LEGEND
from .render.latex.framing import assemble_spread_fragment
from .render.latex.fragments import write_fragment
from .render.latex.table_grid import build_grid_fragment

GRAPH_SECTION_TITLE = "Akteursnetze nach Land"
TABLE_SECTION_TITLE = "Akteurstabellen nach Land"


def build_graph_fragment(net, out_path: str):
    order = [cc for cc in net.countries
             if cc in net.panels and (net.panels[cc].actors or net.panels[cc].projects)]
    figures = []
    tot = 0
    for cc in order:
        r = country_figure(net, cc)
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
    exclude = load_prune(DEFAULT.prune_path) | load_prune(DEFAULT.prune_faktencheck_path)
    return build_network(DEFAULT, exclude=exclude)


def main():
    ap = argparse.ArgumentParser(prog="netz")
    ap.add_argument("cmd", choices=["abb", "tables", "tables-grid"])
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    net = load_network()
    if args.cmd == "abb":
        out = args.out or os.path.join(SP, "figs", "frag_abb_netz.tex")
        tot, n = build_graph_fragment(net, out)
        print(f"wrote {out}: {tot} nodes across {n} country figures")
    elif args.cmd == "tables":
        out = args.out or os.path.join(SP, "figs", "frag_tables_netz.tex")
        n = build_table_fragment(net, out)
        print(f"wrote {out}: {n} country tables")
    elif args.cmd == "tables-grid":
        out = args.out or os.path.join(SP, "figs", "frag_tables_grid.tex")
        n_items, n_pages = build_grid_fragment(net, out)
        print(f"wrote {out}: {n_items} rows/headers across {n_pages} pages")


if __name__ == "__main__":
    main()
