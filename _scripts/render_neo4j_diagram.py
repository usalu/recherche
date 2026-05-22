"""render_neo4j_diagram.py — render Neo4j subgraphs as printable diagrams.

Cypher in, vector PDF and SVG out, via Graphviz. Colours come from
`_neo4j/neo4j_style.grass`, so a printed sheet matches the Browser view. No
browser, screenshot tool or PDF-conversion library is involved.

Named views from the catalog (`_neo4j/diagrams/views.json`):

    python _scripts/render_neo4j_diagram.py --list
    python _scripts/render_neo4j_diagram.py --view schema-overview
    python _scripts/render_neo4j_diagram.py --view projekt-detail --param name="Zirkulit"
    python _scripts/render_neo4j_diagram.py --all

Ad-hoc query:

    python _scripts/render_neo4j_diagram.py \\
        --name akteure \\
        --cypher "MATCH (a:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]->(b) RETURN a, r, b" \\
        --paper A2 --orientation landscape --engine sfdp

Output goes to `_neo4j/exports/diagrams/` as `<name>.pdf`, `<name>.svg` and
`<name>.dot` (the DOT is kept so any diagram can be re-rendered or hand-tuned).

Queries are read-only by contract — write clauses are rejected before they reach
the driver. Setup notes: `_neo4j/diagrams/README.md`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from graphviz_env import GraphvizNotFoundError, render  # noqa: E402
from neo4j_env import resolve_connection  # noqa: E402
from neo4j_to_dot import (  # noqa: E402
    ALL_ENGINES,
    BODY_PT,
    CHIP_PT,
    PAPER_SIZES,
    GraphTooLargeError,
    PrintOptions,
    UnsafeQueryError,
    build_dot,
    build_matrix_dot,
    choose_layout,
    drawing_size,
    fetch_aggregate,
    fetch_graph,
    fetch_matrix,
    page_scale,
)

VIEWS_PATH = _REPO / "_neo4j" / "diagrams" / "views.json"
DEFAULT_OUT_DIR = _REPO / "_neo4j" / "exports" / "diagrams"
ENGINES = ("auto",) + ALL_ENGINES

#: Above this many edges, per-edge type labels stop being readable in print.
EDGE_LABEL_LIMIT = 45

#: Captions below this rendered point size are not worth printing.
LEGIBLE_PT = 6.0


def _fill(text: str, params: dict) -> str:
    """Allow `{name}`-style placeholders in view titles and subtitles."""
    try:
        return str(text).format(**params)
    except (KeyError, IndexError, ValueError):
        return str(text)


def load_views(path: Path = VIEWS_PATH) -> dict[str, dict]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {view["name"]: view for view in data.get("views", [])}


def options_from(view: dict, args: argparse.Namespace) -> PrintOptions:
    """View defaults, overridden by any flag the caller passed explicitly."""

    def pick(flag_value, key, fallback):
        if flag_value is not None:
            return flag_value
        return view.get(key, fallback)

    params = {**(view.get("params") or {}), **(args.param or {})}
    return PrintOptions(
        title=_fill(pick(args.title, "title", view.get("name", "")), params),
        subtitle=_fill(pick(args.subtitle, "subtitle", ""), params),
        paper=pick(args.paper, "paper", "A3"),
        orientation=pick(args.orientation, "orientation", "landscape"),
        engine=pick(args.engine, "engine", "dot"),
        rankdir=pick(args.rankdir, "rankdir", "auto"),
        legend=not args.no_legend and view.get("legend", True),
        edge_labels=not args.no_edge_labels and view.get("edge_labels", True),
        ratio=pick(args.ratio, "ratio", ""),
        splines=pick(args.splines, "splines", "true"),
        wrap=pick(args.wrap, "wrap", 22),
        header_wrap=view.get("header_wrap", 9),
        chips=not args.no_chips and view.get("chips", True),
        clusters=args.clusters or view.get("clusters", False),
        margin_in=pick(args.margin, "margin", 0.4),
    )


def render_one(view: dict, args: argparse.Namespace, database: str) -> int:
    """Fetch, build DOT, and write every requested format. Returns an exit code."""
    name = view["name"]
    options = options_from(view, args)
    params = dict(view.get("params") or {})
    params.update(args.param or {})
    max_nodes = args.max_nodes if args.max_nodes is not None else view.get("max_nodes", 300)
    mode = args.mode or view.get("mode", "graph")

    if mode == "matrix":
        return _render_matrix(view, args, options, params, database, max_nodes)

    fetch = fetch_aggregate if mode == "aggregate" else fetch_graph
    try:
        nodes, edges = fetch(
            view["cypher"], params=params, database=database, max_nodes=max_nodes
        )
    except (UnsafeQueryError, GraphTooLargeError, ValueError) as exc:
        print(f"FAIL [{name}]: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # driver/connection failures
        print(f"FAIL [{name}]: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    if not nodes:
        print(f"SKIP [{name}]: the query returned no nodes.", file=sys.stderr)
        return 1

    # Dense diagrams drown in edge labels; the relationship type is in the subtitle.
    if options.edge_labels and not args.edge_labels and len(edges) > EDGE_LABEL_LIMIT:
        if len({e.type for e in edges}) > 1:
            options.edge_labels = False

    requested_engine = options.engine
    if options.engine == "auto" or options.rankdir == "auto":
        engines = ALL_ENGINES if options.engine == "auto" else (options.engine,)
        rankdirs = ("LR", "TB") if options.rankdir == "auto" else (options.rankdir,)
        options.engine, options.rankdir, _ = choose_layout(
            nodes, edges, options, database=database, engines=engines, rankdirs=rankdirs
        )

    dot = build_dot(nodes, edges, options, database=database)
    scale = page_scale(options, *drawing_size(dot, options.engine))
    effective_pt = options.node_fontsize * scale
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    dot_path = out_dir / f"{name}.dot"
    dot_path.write_text(dot, encoding="utf-8")

    written: list[str] = []
    for fmt in args.format:
        extra = [f"-Gdpi={args.dpi}"] if fmt in ("png", "jpg", "jpeg") else None
        try:
            out = render(
                dot, out_dir / f"{name}.{fmt}", fmt=fmt, engine=options.engine, extra_args=extra
            )
        except GraphvizNotFoundError as exc:
            print(f"FAIL [{name}]: {exc}", file=sys.stderr)
            return 2
        except RuntimeError as exc:
            print(f"FAIL [{name}]: {exc}", file=sys.stderr)
            return 1
        written.append(f"{out.name} ({out.stat().st_size:,} B)")

    layout = options.engine + (f"/{options.rankdir}" if options.engine == "dot" else "")
    paper = f"{options.paper} {options.orientation}"
    print(
        f"OK  {name:<28} {len(nodes):>4} nodes {len(edges):>5} edges  "
        f"{layout:<9} {paper:<16} {effective_pt:4.1f}pt  {', '.join(written)}",
        flush=True,
    )
    if options.embeds_in_document:
        # What the diagram sits next to: semio-window.sty narrows body text to the
        # chip size inside a window, so a windowed figure is judged against 7.2pt
        # and a bare one against the document's 9.6pt.
        surrounding = CHIP_PT if options.paper == "latex-window" else BODY_PT
        if effective_pt < surrounding:
            print(
                f"    ! captions land at {effective_pt:.1f}pt against {surrounding}pt "
                f"surrounding text ({options.paper} shrank to {scale:.0%}) — narrow the "
                f"query, or place it on a full page instead of in the text column.",
                file=sys.stderr,
                flush=True,
            )
    elif effective_pt < LEGIBLE_PT:
        hint = "print larger (--paper A2/A1/A0) or narrow the query"
        if requested_engine != "auto":
            hint += "; --engine auto may find a tighter layout"
        print(
            f"    ! captions land at {effective_pt:.1f}pt on {options.paper} — {hint}.",
            file=sys.stderr,
            flush=True,
        )
    return 0


def _render_matrix(view, args, options, params, database, max_nodes) -> int:
    """A matrix is one HTML-table node — no layout engine, so no fitting pass."""
    name = view["name"]
    try:
        matrix = fetch_matrix(
            view["cypher"], params=params, database=database, max_nodes=max_nodes
        )
    except (UnsafeQueryError, GraphTooLargeError, ValueError) as exc:
        print(f"FAIL [{name}]: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"FAIL [{name}]: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    if not matrix["rows"]:
        print(f"SKIP [{name}]: the query returned no rows.", file=sys.stderr)
        return 1

    dot = build_matrix_dot(
        matrix, options, database=database,
        totals=view.get("totals", True),
        plain_cols=tuple(view.get("plain_cols", ())),
    )
    scale = page_scale(options, *drawing_size(dot, "dot"))
    effective_pt = options.node_fontsize * scale

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{name}.dot").write_text(dot, encoding="utf-8")

    written: list[str] = []
    for fmt in args.format:
        extra = [f"-Gdpi={args.dpi}"] if fmt in ("png", "jpg", "jpeg") else None
        try:
            out = render(dot, out_dir / f"{name}.{fmt}", fmt=fmt, engine="dot", extra_args=extra)
        except GraphvizNotFoundError as exc:
            print(f"FAIL [{name}]: {exc}", file=sys.stderr)
            return 2
        except RuntimeError as exc:
            print(f"FAIL [{name}]: {exc}", file=sys.stderr)
            return 1
        written.append(f"{out.name} ({out.stat().st_size:,} B)")

    filled = len(matrix["cells"])
    shape = f"{len(matrix['rows'])}x{len(matrix['cols'])}"
    paper = f"{options.paper} {options.orientation}"
    print(
        f"OK  {name:<28} {shape:>9} matrix {filled:>4} cells  "
        f"{'-':<9} {paper:<16} {effective_pt:4.1f}pt  {', '.join(written)}",
        flush=True,
    )
    if options.embeds_in_document and scale < 0.995:
        surrounding = CHIP_PT if options.paper == "latex-window" else BODY_PT
        if effective_pt < surrounding:
            print(
                f"    ! cells land at {effective_pt:.1f}pt against {surrounding}pt "
                f"surrounding text ({options.paper} shrank to {scale:.0%}) — drop columns "
                f"or shorten the row labels.",
                file=sys.stderr,
                flush=True,
            )
    return 0


def parse_params(values: list[str] | None) -> dict:
    params: dict = {}
    for item in values or []:
        if "=" not in item:
            raise argparse.ArgumentTypeError(f"--param expects key=value, got {item!r}")
        key, _, raw = item.partition("=")
        params[key.strip()] = _coerce(raw)
    return params


def _coerce(raw: str):
    text = raw.strip()
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            pass
    if text.lower() in ("true", "false"):
        return text.lower() == "true"
    return text


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Render Neo4j subgraphs as printable PDF/SVG diagrams.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    source = ap.add_mutually_exclusive_group()
    source.add_argument("--view", help="Name of a view from _neo4j/diagrams/views.json")
    source.add_argument("--all", action="store_true", help="Render every view in the catalog")
    source.add_argument("--cypher", help="Ad-hoc Cypher query (read-only)")
    source.add_argument("--cypher-file", type=Path, help="File holding a read-only Cypher query")
    source.add_argument("--list", action="store_true", help="List the catalog and exit")

    ap.add_argument("--name", help="Output basename for an ad-hoc query")
    ap.add_argument(
        "--mode", choices=("graph", "aggregate", "matrix"),
        help="Result shape (default: graph). 'matrix' expects row/col/value columns.",
    )
    ap.add_argument("--param", action="append", help="Cypher parameter, key=value (repeatable)")
    ap.add_argument("--database", help="Override the database from neo4j_env")

    ap.add_argument("--paper", choices=sorted(PAPER_SIZES), help="Sheet size (default: A3)")
    ap.add_argument("--orientation", choices=("portrait", "landscape"))
    ap.add_argument("--engine", choices=ENGINES, help="Graphviz layout engine")
    ap.add_argument(
        "--rankdir", choices=("auto", "LR", "TB", "RL", "BT"),
        help="dot direction; 'auto' trial-lays out LR and TB and keeps the better page fit",
    )
    ap.add_argument("--ratio", help='Graphviz ratio, e.g. "compress" or "fill"')
    ap.add_argument(
        "--splines", choices=("true", "ortho", "line", "polyline", "curved", "spline"),
        help="Edge routing. 'ortho' = right angles, 'line' = straight diagonals.",
    )
    ap.add_argument("--margin", type=float, help="Page margin in inches (default: 0.4)")
    ap.add_argument("--wrap", type=int, help="Caption wrap width in characters (default: 22)")
    ap.add_argument("--max-nodes", type=int, help="Printable node budget (default: 300)")
    ap.add_argument("--title")
    ap.add_argument("--subtitle")
    ap.add_argument("--no-legend", action="store_true")
    ap.add_argument(
        "--clusters", action="store_true",
        help="Box nodes of the same kind into named groups. Makes a wide layer readable.",
    )
    ap.add_argument(
        "--no-chips", action="store_true",
        help="Drop the per-node kind chip. On a plate of one kind it is pure repetition, "
             "and it roughly doubles node height.",
    )
    ap.add_argument("--no-edge-labels", action="store_true")
    ap.add_argument(
        "--edge-labels", action="store_true",
        help=f"Keep per-edge type labels even above {EDGE_LABEL_LIMIT} edges",
    )

    ap.add_argument(
        "--format", nargs="+", default=["pdf", "svg"],
        help="Output formats (default: pdf svg). png also honours --dpi.",
    )
    ap.add_argument("--dpi", type=int, default=300, help="Raster DPI for png (default: 300)")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)

    args = ap.parse_args()
    try:
        args.param = parse_params(args.param)
    except argparse.ArgumentTypeError as exc:
        ap.error(str(exc))

    views = load_views()

    if args.list:
        if not views:
            print(f"No view catalog at {VIEWS_PATH}")
            return 1
        print(f"{len(views)} views in {VIEWS_PATH.relative_to(_REPO)}\n")
        for name, view in views.items():
            paper = f"{view.get('paper', 'A3')} {view.get('orientation', 'landscape')}"
            print(f"  {name:<28} {view.get('engine', 'dot'):<6} {paper:<16} {view.get('description', '')}")
            if view.get("params"):
                print(f"  {'':<28} params: {', '.join(view['params'])}")
        return 0

    _, _, _, default_db = resolve_connection()
    database = args.database or default_db

    if args.all:
        targets = list(views.values())
        if not targets:
            print(f"No view catalog at {VIEWS_PATH}", file=sys.stderr)
            return 1
    elif args.view:
        if args.view not in views:
            print(
                f"Unknown view {args.view!r}. Known: {', '.join(views) or '(none)'}",
                file=sys.stderr,
            )
            return 1
        targets = [views[args.view]]
    elif args.cypher or args.cypher_file:
        # utf-8-sig: editors and PowerShell's Out-File write a BOM, which Cypher
        # rejects as an invalid character at column 1.
        cypher = args.cypher or args.cypher_file.read_text(encoding="utf-8-sig")
        name = args.name or (args.cypher_file.stem if args.cypher_file else "adhoc-diagram")
        targets = [{"name": name, "cypher": cypher, "title": args.title or name}]
    else:
        ap.error("choose one of --view, --all, --cypher, --cypher-file or --list")

    print(f"database: {database}   out: {args.out_dir}\n")
    failures = 0
    for view in targets:
        failures += 1 if render_one(view, args, database) else 0
    if failures:
        print(f"\n{failures} of {len(targets)} view(s) failed.", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
