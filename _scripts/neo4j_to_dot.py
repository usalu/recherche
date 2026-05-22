"""Turn a Cypher result into a print-ready Graphviz DOT document.

Library module. `render_neo4j_diagram.py` is the CLI on top of it.

Two input shapes are supported:

*graph mode* — the query returns nodes, relationships or paths. Whatever the
    column layout, every Node and Relationship found anywhere in the result
    (including inside lists and paths) is collected.

*aggregate mode* — the query returns plain rows with `source` and `target`
    columns (optionally `type` and `count`). Used for schema-level maps where
    one drawn edge stands for many real ones.

Queries are read-only by contract: anything that could mutate the graph is
rejected before it reaches the driver.
"""

from __future__ import annotations

import math
import re
import sys
import textwrap
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402
from semio_style import (  # noqa: E402
    SEMIO,
    DiagramPaint,
    load_tokens,
    magnitude_fill,
    node_style,
    primary_label,
    print_pt,
    tokens_digest,
)

# Every visual constant below comes out of the semio token snapshot. Nothing in a
# rendered diagram may introduce a colour, family or width that is not token-derived —
# see .claude/skills/semio-styling/SKILL.md.
SANS = SEMIO.font("sans")
MONO = SEMIO.font("mono")

# Print points, from `print/tex/semio-tokens.sty` — not the screen-pixel metrics.
BODY_PT = print_pt("chrome@font@body")      # 9.6
CHIP_PT = print_pt("chrome@font@chip")      # 7.2
HAIRLINE = print_pt("stroke@hairline")      # 0.75
STROKE = print_pt("stroke@default")         # 1.5
FOCUS_STROKE = print_pt("stroke@focus")     # 2.25

NODE_PT = BODY_PT
EDGE_PT = CHIP_PT
TITLE_PT = BODY_PT
LEGEND_PT = CHIP_PT

#: Paper sizes in inches, portrait (width, height).
#:
#: The `latex-*` entries are not sheets — they are the semio LaTeX document's own
#: content boxes, measured from the compiled Zukunft Bau report
#: (`E:/semio/print/dist/_cur/zwischenbericht.log`, geometry verbose output). A
#: diagram rendered at one of these drops into the document at 1:1 with no
#: `\includegraphics` scaling, so its type lands at the size it was laid out for.
PAPER_SIZES: dict[str, tuple[float, float]] = {
    "A5": (5.83, 8.27),
    "A4": (8.27, 11.69),
    "A3": (11.69, 16.54),
    "A2": (16.54, 23.39),
    "A1": (23.39, 33.11),
    "A0": (33.11, 46.81),
    "letter": (8.5, 11.0),
    "legal": (8.5, 14.0),
    "tabloid": (11.0, 17.0),
    # \textwidth 432.48pt x \textheight 720.46pt — A4, 2.5cm margins, 8mm binding.
    "latex-body": (6.007, 10.006),
    # The same minus a window's two hairlines and two 5.5pt body pads (12.5pt).
    "latex-window": (5.833, 9.833),
    # \newgeometry{1.5cm} cover pages: 512.15pt x 759.69pt.
    "latex-cover": (7.113, 10.551),
    # type=flyer: A4 landscape, 1.2cm margins (186 x 273mm). Stored portrait like
    # every other entry — pass --orientation landscape to get the real flyer box.
    "latex-flyer": (7.323, 10.748),
}

#: Papers that are already a content box: the document's margins are baked in, so
#: adding a page margin on top would shrink the drawing below the column it must fill.
CONTENT_BOX_PAPERS = frozenset({"latex-body", "latex-window", "latex-cover", "latex-flyer"})

#: Rejected outright — this tool never writes to the graph.
_WRITE_CLAUSE = re.compile(
    r"(?<![\w.])(CREATE|MERGE|DELETE|DETACH\s+DELETE|SET|REMOVE|DROP|FOREACH|"
    r"LOAD\s+CSV|CALL\s+\{[^}]*\b(CREATE|MERGE|DELETE|SET)\b)(?![\w.])",
    re.IGNORECASE,
)

#: Node caption is taken from the first property present here.
CAPTION_PROPERTIES = ("name", "titel", "title", "bezeichnung", "label", "id", "key")


class UnsafeQueryError(ValueError):
    """Raised when a query contains a clause that could mutate the graph."""


class GraphTooLargeError(ValueError):
    """Raised when a result exceeds the printable node budget."""


@dataclass
class DiagramNode:
    key: str
    labels: list[str]
    caption: str
    properties: dict = field(default_factory=dict)


@dataclass
class DiagramEdge:
    source: str
    target: str
    type: str
    count: int = 1
    #: Element ids of the relationships collapsed into this edge. A multi-hop
    #: OPTIONAL MATCH returns the same relationship once per result row, so
    #: multiplicity has to be counted per relationship, not per row.
    rel_ids: set[str] = field(default_factory=set)


@dataclass
class PrintOptions:
    """Everything that controls how the DOT lays out on paper."""

    title: str = ""
    subtitle: str = ""
    paper: str = "A3"
    orientation: str = "landscape"
    margin_in: float = 0.4
    engine: str = "dot"
    rankdir: str = "LR"
    font: str = SANS
    node_fontsize: float = NODE_PT
    edge_fontsize: float = EDGE_PT
    title_fontsize: float = TITLE_PT
    legend: bool = True
    edge_labels: bool = True
    ratio: str = ""
    #: Graphviz spline mode. "ortho" gives right-angled edges, which suits a layered
    #: chain and semio's square geometry; "line" gives straight diagonals.
    splines: str = "true"
    wrap: int = 22
    header_wrap: int = 9
    chips: bool = True
    #: Box nodes of the same kind together. Turns a rank of 91 norms into 11 named
    #: groups, which is what makes a wide layer readable rather than a wall.
    clusters: bool = False
    appearance: str = "light"

    def canvas_inches(self) -> tuple[float, float]:
        """Usable drawing area after margins, honouring orientation."""
        width, height = PAPER_SIZES.get(self.paper, PAPER_SIZES["A3"])
        if self.orientation == "landscape":
            width, height = height, width
        # A latex-* paper is already the document's content box; its margins are
        # the document's, so no further page margin may be subtracted.
        margin = 0.0 if self.paper in CONTENT_BOX_PAPERS else self.margin_in
        return (max(1.0, width - 2 * margin), max(1.0, height - 2 * margin))

    @property
    def embeds_in_document(self) -> bool:
        return self.paper in CONTENT_BOX_PAPERS

    @property
    def effective_margin(self) -> float:
        """Graphviz page margin. Zero for a content box — the document owns the margins."""
        return 0.0 if self.embeds_in_document else self.margin_in


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------

def assert_read_only(cypher: str) -> None:
    """Reject any query that could mutate the graph."""
    match = _WRITE_CLAUSE.search(_strip_strings_and_comments(cypher))
    if match:
        raise UnsafeQueryError(
            f"Query contains the write clause {match.group(1).upper()!r}. "
            "This renderer is read-only — use the intake/patch tooling for changes."
        )


def fetch_graph(
    cypher: str,
    *,
    params: dict | None = None,
    database: str | None = None,
    max_nodes: int = 300,
) -> tuple[list[DiagramNode], list[DiagramEdge]]:
    """Run `cypher` and collect every Node/Relationship anywhere in the result."""
    assert_read_only(cypher)
    from neo4j import GraphDatabase
    from neo4j.graph import Node, Relationship

    uri, user, password, default_db = resolve_connection()
    if not all([uri, user, password]):
        raise RuntimeError(
            "Missing Neo4j connection settings. Set NEO4J_URI / NEO4J_USERNAME / "
            "NEO4J_PASSWORD or provide them in .cursor/mcp.json."
        )

    nodes: dict[str, DiagramNode] = {}
    edges: dict[tuple[str, str, str], DiagramEdge] = {}

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(
            database=database or default_db, default_access_mode="READ"
        ) as session:
            for record in session.run(cypher, params or {}):
                for value in record.values():
                    _walk(value, nodes, edges, Node, Relationship)
    finally:
        driver.close()

    # Edges whose endpoints were not returned would dangle; drop them.
    kept = [e for e in edges.values() if e.source in nodes and e.target in nodes]
    _assert_printable(len(nodes), max_nodes)
    return list(nodes.values()), kept


def fetch_aggregate(
    cypher: str,
    *,
    params: dict | None = None,
    database: str | None = None,
    max_nodes: int = 300,
) -> tuple[list[DiagramNode], list[DiagramEdge]]:
    """Run `cypher` returning `source`/`target` (+ optional `type`, `count`) rows."""
    assert_read_only(cypher)
    from neo4j import GraphDatabase

    uri, user, password, default_db = resolve_connection()
    nodes: dict[str, DiagramNode] = {}
    edges: dict[tuple[str, str, str], DiagramEdge] = {}

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(
            database=database or default_db, default_access_mode="READ"
        ) as session:
            for record in session.run(cypher, params or {}):
                row = dict(record)
                source = str(row.get("source", "")).strip()
                target = str(row.get("target", "")).strip()
                if not source or not target:
                    raise ValueError(
                        "Aggregate queries must return 'source' and 'target' columns; "
                        f"got columns {sorted(row)}."
                    )
                rel_type = str(row.get("type") or "")
                count = int(row.get("count") or 1)
                # Optional *_label columns colour the box by domain when the caption
                # is an entity name rather than a label name.
                for name, label in (
                    (source, row.get("source_label")),
                    (target, row.get("target_label")),
                ):
                    nodes.setdefault(
                        name,
                        DiagramNode(key=name, labels=[str(label or name)], caption=name),
                    )
                key = (source, target, rel_type)
                if key in edges:
                    edges[key].count += count
                else:
                    edges[key] = DiagramEdge(source, target, rel_type, count)
    finally:
        driver.close()

    _assert_printable(len(nodes), max_nodes)
    return list(nodes.values()), list(edges.values())


def fetch_matrix(
    cypher: str,
    *,
    params: dict | None = None,
    database: str | None = None,
    max_nodes: int = 300,
) -> dict:
    """Run a query returning `row`/`col`/`value` (+ optional `row_group`, `col_order`).

    A cross-tabulation, not a node set: 88 relationships between 11 rows and 15
    columns is a hairball drawn as edges and a legible grid drawn as cells.
    """
    assert_read_only(cypher)
    from neo4j import GraphDatabase

    uri, user, password, default_db = resolve_connection()
    cells: dict[tuple[str, str], float] = {}
    row_group: dict[str, str] = {}
    row_order: list[str] = []
    col_order: list[str] = []
    col_rank: dict[str, float] = {}

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(
            database=database or default_db, default_access_mode="READ"
        ) as session:
            for record in session.run(cypher, params or {}):
                data = dict(record)
                for required in ("row", "col", "value"):
                    if required not in data:
                        raise ValueError(
                            "Matrix queries must return 'row', 'col' and 'value' "
                            f"columns; got {sorted(data)}."
                        )
                row, col = str(data["row"]), str(data["col"])
                cells[(row, col)] = float(data["value"] or 0)
                if row not in row_order:
                    row_order.append(row)
                if col not in col_order:
                    col_order.append(col)
                if data.get("row_group") is not None:
                    row_group[row] = str(data["row_group"])
                if data.get("col_order") is not None:
                    col_rank[col] = float(data["col_order"])
    finally:
        driver.close()

    if col_rank:
        col_order.sort(key=lambda c: (col_rank.get(c, 0), c))
    # Group the rows here rather than trusting query order: a UNION returns its
    # branches concatenated, which would emit the same group band several times.
    if row_group:
        row_order.sort(key=lambda r: (row_group.get(r, ""), r))
    _assert_printable(len(row_order) + len(col_order), max_nodes)
    return {
        "rows": row_order,
        "cols": col_order,
        "cells": cells,
        "row_group": row_group,
    }


def _walk(value, nodes, edges, Node, Relationship) -> None:
    """Recursively pull Nodes and Relationships out of an arbitrary result value."""
    if isinstance(value, Node):
        key = value.element_id
        if key not in nodes:
            props = dict(value)
            nodes[key] = DiagramNode(
                key=key,
                labels=sorted(value.labels),
                caption=_caption(props, sorted(value.labels)),
                properties=props,
            )
        return
    if isinstance(value, Relationship):
        start = value.start_node.element_id if value.start_node else None
        end = value.end_node.element_id if value.end_node else None
        if start and end:
            key = (start, end, value.type)
            rel_id = value.element_id
            if key in edges:
                edge = edges[key]
                if rel_id not in edge.rel_ids:
                    edge.rel_ids.add(rel_id)
                    edge.count = len(edge.rel_ids)
            else:
                edges[key] = DiagramEdge(start, end, value.type, 1, {rel_id})
            for endpoint in (value.start_node, value.end_node):
                _walk(endpoint, nodes, edges, Node, Relationship)
        return
    # Paths expose .nodes and .relationships; lists/dicts are walked element-wise.
    if hasattr(value, "relationships") and hasattr(value, "nodes"):
        for item in list(value.nodes) + list(value.relationships):
            _walk(item, nodes, edges, Node, Relationship)
        return
    if isinstance(value, (list, tuple, set)):
        for item in value:
            _walk(item, nodes, edges, Node, Relationship)
        return
    if isinstance(value, dict):
        for item in value.values():
            _walk(item, nodes, edges, Node, Relationship)


def _caption(props: dict, labels: list[str]) -> str:
    for key in CAPTION_PROPERTIES:
        value = props.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, (int, float)):
            return str(value)
    return labels[0] if labels else "?"


def _assert_printable(node_count: int, max_nodes: int) -> None:
    if max_nodes and node_count > max_nodes:
        raise GraphTooLargeError(
            f"The query returned {node_count} nodes; the printable budget is {max_nodes}. "
            "Narrow the query, or raise --max-nodes and print on a larger sheet "
            "(A1/A0) — beyond a few hundred nodes captions stop being legible."
        )


def _strip_strings_and_comments(cypher: str) -> str:
    """Blank out string literals and comments so the write-clause scan sees only code."""
    without_block = re.sub(r"/\*.*?\*/", " ", cypher, flags=re.DOTALL)
    without_line = re.sub(r"//[^\n]*", " ", without_block)
    return re.sub(r"'[^']*'|\"[^\"]*\"|`[^`]*`", " ", without_line)


# --------------------------------------------------------------------------
# DOT generation
# --------------------------------------------------------------------------

def build_dot(
    nodes: list[DiagramNode],
    edges: list[DiagramEdge],
    options: PrintOptions,
    *,
    database: str = "",
) -> str:
    """Render nodes and edges as a DOT document sized for `options.paper`."""
    width, height = options.canvas_inches()
    appearance = options.appearance
    theme = load_tokens(appearance)
    surface = theme.board("rasterClear")
    foreground = theme.canvas("labelFill")
    edge_base = theme.board("edgeStroke")

    node_ids = {node.key: f"n{index}" for index, node in enumerate(nodes)}
    used_labels: dict[str, int] = {}

    # When every edge is the same type, repeating it on each edge is noise —
    # name it once in the subtitle and leave only the multiplicities on the edges.
    edge_types = {e.type for e in edges if e.type}
    uniform_type = edge_types.pop() if len(edge_types) == 1 else ""
    subtitle = options.subtitle
    if uniform_type and options.edge_labels and uniform_type not in subtitle:
        subtitle = f"{subtitle} · {uniform_type}" if subtitle else uniform_type

    lines: list[str] = []
    # Provenance for the styling gate: which appearance painted this and from which
    # token snapshot, so a sheet can be checked without guessing.
    lines.append(f"// semio-appearance: {appearance}")
    lines.append(f"// semio-tokens: {tokens_digest()}")
    lines.append("digraph recherche {")
    lines.append(f'  graph [ charset="UTF-8"')
    lines.append(f'         , size="{width:.2f},{height:.2f}"')
    lines.append(f"         , margin={options.effective_margin}")
    lines.append(f'         , fontname="{options.font}"')
    if options.ratio:
        lines.append(f'         , ratio="{options.ratio}"')
    if options.engine == "dot":
        lines.append(f'         , rankdir="{options.rankdir}"')
        lines.append("         , nodesep=0.35, ranksep=0.75")
    else:
        lines.append('         , overlap="prism", overlap_scaling=-6')
        lines.append('         , sep="+18", esep="+8", K=1.1')
        # Fixed seed: force-directed engines otherwise place nodes differently on
        # every run, so the same query would print differently each time.
        lines.append("         , start=1")
    lines.append(
        f'         , splines="{options.splines}", concentrate=false, bgcolor="{surface}"'
    )
    if options.title:
        header = _escape(options.title)
        if subtitle:
            header += r"\n" + _escape(subtitle)
        lines.append(f'         , label="{header}", labelloc="t", labeljust="l"')
        lines.append(f'         , fontsize={options.title_fontsize}, fontcolor="{foreground}"')
    lines.append("  ];")
    # Square corners at the print hairline. semio sets tcolorbox `arc=0mm`
    # everywhere and its 5,259-line stylesheet contains no non-zero radius —
    # nothing in this identity is rounded.
    lines.append(
        f'  node [ shape="box", style="filled", fontname="{options.font}"'
        f', fontsize={options.node_fontsize}, penwidth={HAIRLINE}'
        ', margin="0.10,0.05" ];'
    )
    lines.append(
        f'  edge [ fontname="{options.font}", fontsize={options.edge_fontsize}'
        f', penwidth={HAIRLINE}, arrowsize=0.6, arrowhead="vee", color="{edge_base}" ];'
    )
    lines.append("")

    def node_line(node: DiagramNode, indent: str = "  ") -> str:
        paint = node_style(node.labels, appearance)
        label = primary_label(node.labels)
        tooltip = _escape(f"{'|'.join(node.labels)}: {node.caption}")
        attrs = [
            # Inside a cluster the group box already names the kind, so the per-node
            # chip would repeat it on every member.
            f"label={_node_label(node, None if options.clusters else label, paint, options)}",
            f'fillcolor="{paint.fill}"',
            f'color="{paint.border}"',
            f'fontcolor="{paint.font_color}"',
            f'tooltip="{tooltip}"',
        ]
        if paint.emphasis == "focus":
            attrs.append(f"penwidth={FOCUS_STROKE}")
        return f"{indent}{node_ids[node.key]} [ {', '.join(attrs)} ];"

    for node in nodes:
        label = primary_label(node.labels)
        if label:
            used_labels[label] = used_labels.get(label, 0) + 1

    if options.clusters:
        grouped: dict[str, list[DiagramNode]] = {}
        for node in nodes:
            grouped.setdefault(primary_label(node.labels) or "—", []).append(node)
        for index, (group, members) in enumerate(sorted(grouped.items())):
            lines.append(f"  subgraph cluster_{index} {{")
            lines.append(
                f'    label="{_escape(group)}"; labeljust="l"; labelloc="t";'
                f' fontname="{options.font}"; fontsize={CHIP_PT};'
                f' fontcolor="{theme.chrome("mutedForeground")}";'
                f' color="{theme.chrome("borderNormal")}"; penwidth={HAIRLINE};'
                f' style="solid"; margin=8;'
            )
            for node in members:
                lines.append(node_line(node, "    "))
            lines.append("  }")
    else:
        for node in nodes:
            lines.append(node_line(node))

    lines.append("")
    for edge in edges:
        source = node_ids.get(edge.source)
        target = node_ids.get(edge.target)
        if not source or not target:
            continue
        color = _edge_color(edge, nodes, appearance, edge_base)
        attrs = [f'color="{color}"']
        text = ""
        if options.edge_labels and edge.type and not uniform_type:
            text = edge.type if edge.count == 1 else f"{edge.type} ×{edge.count}"
        elif edge.count > 1:
            text = f"×{edge.count}"
        if text:
            attrs.append(f'label="{_escape(text)}"')
            attrs.append(f'fontcolor="{theme.board("labelFill")}"')
        if edge.count > 1:
            # Multiplicity steps hairline → default → focus, the three print widths.
            attrs.append(f"penwidth={STROKE if edge.count < 4 else FOCUS_STROKE}")
        lines.append(f"  {source} -> {target} [ {', '.join(attrs)} ];")

    if options.legend and used_labels:
        lines.append("")
        lines.append(_legend_block(used_labels, options, theme, database, len(nodes), len(edges)))

    lines.append("}")
    return "\n".join(lines) + "\n"


def _node_label(node: DiagramNode, kind: str | None, paint, options: PrintOptions) -> str:
    """A kind chip above the caption, in semio's muted-head / bright-tail pattern.

    Kind is stated typographically because semio's board has one neutral node
    fill and no per-kind colour at all. This is the same device as its window
    title tabs and heading key chips.
    """
    caption = _html(" ".join(str(node.caption).split()) or "?")
    wrapped = _html_wrap(caption, options.wrap)
    rows = []
    if kind and options.chips:
        rows.append(
            f'<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="{CHIP_PT}" '
            f'COLOR="{paint.chip_color}">{_html(kind)}</FONT></TD></TR>'
        )
    rows.append(f'<TR><TD ALIGN="LEFT">{wrapped}</TD></TR>')
    return (
        '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">'
        + "".join(rows)
        + "</TABLE>>"
    )


def _edge_color(edge, nodes, appearance: str, fallback: str) -> str:
    """One edge colour for the whole sheet — semio's board has a single edgeStroke."""
    return fallback


def _legend_block(
    used: dict[str, int],
    options: PrintOptions,
    theme,
    database: str,
    node_count: int,
    edge_count: int,
) -> str:
    """A kind register plus provenance footer, built like a semio window.

    Not a colour key: with one neutral node fill there is nothing to key. This is
    the register semio prints for every document kind — the counts of what is on
    the sheet — inside a hairline frame with a title tab, and a machine-set
    provenance line in Share Tech Mono.
    """
    surface = theme.chrome("canvas")
    border = theme.chrome("borderNormal")
    text = theme.chrome("foreground")
    muted = theme.chrome("mutedForeground")
    tab_fill = theme.chrome("panel")

    rows: list[str] = []
    for label in sorted(used):
        rows.append(
            f'      <TR><TD ALIGN="LEFT"><FONT COLOR="{text}">{_html(label)}</FONT></TD>'
            f'<TD ALIGN="RIGHT"><FONT FACE="{MONO}" COLOR="{muted}">'
            f"{used[label]}</FONT></TD></TR>"
        )
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    footer = _html(f"{database or 'neo4j'} · {node_count} · {edge_count} · {stamp}")
    title = _html("Verzeichnis der Arten")
    return (
        "  subgraph cluster_legend {\n"
        f'    label=""; color="{border}"; penwidth={HAIRLINE}; style="solid"; margin=0;\n'
        f'    legend [ shape=none, margin=0, fillcolor="{surface}", style="filled",'
        f' fontname="{options.font}", label=<\n'
        f'    <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">\n'
        # Title tab: sits on the register, sharing its top rule — semio's window
        # header, where the tab must sit ON the component rather than float above.
        f'      <TR><TD COLSPAN="2" ALIGN="LEFT" BGCOLOR="{tab_fill}">'
        f'<FONT POINT-SIZE="{CHIP_PT}" COLOR="{text}">{title}</FONT></TD></TR>\n'
        + "\n".join(rows)
        + "\n"
        '      <TR><TD COLSPAN="2" ALIGN="LEFT">'
        f'<FONT FACE="{MONO}" POINT-SIZE="{CHIP_PT}" COLOR="{muted}">{footer}</FONT>'
        "</TD></TR>\n"
        "    </TABLE>\n"
        "    > ];\n"
        "  }"
    )


def build_matrix_dot(
    matrix: dict,
    options: PrintOptions,
    *,
    database: str = "",
    totals: bool = True,
    row_total_label: str = "Summe",
    plain_cols: tuple[str, ...] = (),
) -> str:
    """Render a cross-tabulation as one HTML-table node — a matrix, not a graph.

    The whole figure is a single Graphviz node, so there is no layout engine
    involved and no wasted whitespace: every millimetre carries a cell. Grid lines
    come from letting the sheet surface show through `CELLSPACING`, the way semio
    tables separate cells with fills rather than ruling every box.
    """
    theme = load_tokens(options.appearance)
    surface = theme.board("rasterClear")
    text = theme.chrome("foreground")
    muted = theme.chrome("mutedForeground")
    band = theme.chrome("panel")
    border = theme.chrome("borderNormal")

    rows, cols, cells = matrix["rows"], matrix["cols"], matrix["cells"]
    groups = matrix.get("row_group", {})
    scaled = [v for (r, c), v in cells.items() if c not in plain_cols]
    maximum = max(scaled) if scaled else 0
    span = len(cols) + (2 if totals else 1)

    def cell(content: str, *, fill: str, color: str, align: str = "CENTER",
             size: float = CHIP_PT, colspan: int = 1) -> str:
        attrs = f' BGCOLOR="{fill}" ALIGN="{align}"'
        if colspan > 1:
            attrs += f' COLSPAN="{colspan}"'
        # Graphviz rejects an empty <FONT> element, so a blank cell still needs a glyph.
        body = content if content else "&nbsp;"
        return f"<TD{attrs}><FONT POINT-SIZE=\"{size}\" COLOR=\"{color}\">{body}</FONT></TD>"

    lines: list[str] = []
    # Header: row-label gutter, then one narrow column per category, then the total.
    header = [cell("", fill=surface, color=muted)]
    # A header sets its column's width, so a long one wastes the whole column.
    # Wrapping keeps the grid narrow without abbreviating past recognition.
    header += [cell(_html_break(c, options.header_wrap), fill=surface, color=muted) for c in cols]
    if totals:
        header.append(
            cell(_html_break(row_total_label, options.header_wrap), fill=surface, color=muted)
        )
    lines.append("      <TR>" + "".join(header) + "</TR>")

    current_group = None
    for row in rows:
        group = groups.get(row)
        if group is not None and group != current_group:
            current_group = group
            lines.append(
                "      <TR>"
                + cell(_html(group), fill=band, color=text, align="LEFT", colspan=span)
                + "</TR>"
            )
        cell_row = [cell(_html(row), fill=surface, color=text, align="LEFT", size=BODY_PT)]
        total = 0.0
        for col in cols:
            value = cells.get((row, col), 0)
            body = _fmt(value) if value else ""
            if col in plain_cols:
                # A summary column counts something else than the matrix cells do;
                # shading it on their scale would invite a comparison that is wrong.
                cell_row.append(cell(body, fill=surface, color=text))
                continue
            total += value
            fill, fontcolor = magnitude_fill(value, maximum, options.appearance)
            cell_row.append(cell(body, fill=fill, color=fontcolor))
        if totals:
            cell_row.append(cell(_fmt(total), fill=surface, color=text))
        lines.append("      <TR>" + "".join(cell_row) + "</TR>")

    subtitle = options.subtitle
    head: list[str] = []
    if options.title:
        head.append(
            f'    <TR><TD COLSPAN="{span}" ALIGN="LEFT"><FONT POINT-SIZE="{TITLE_PT}"'
            f' COLOR="{text}">{_html(options.title)}</FONT></TD></TR>'
        )
    if subtitle:
        head.append(
            f'    <TR><TD COLSPAN="{span}" ALIGN="LEFT"><FONT POINT-SIZE="{CHIP_PT}"'
            f' COLOR="{muted}">{_html(subtitle)}</FONT></TD></TR>'
        )
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    foot = (
        f'    <TR><TD COLSPAN="{span}" ALIGN="LEFT"><FONT FACE="{MONO}"'
        f' POINT-SIZE="{CHIP_PT}" COLOR="{muted}">'
        f'{_html(f"{database or chr(45)} · {len(rows)}×{len(cols)} · {stamp}")}'
        "</FONT></TD></TR>"
    )

    width, height = options.canvas_inches()
    return (
        f"// semio-appearance: {options.appearance}\n"
        f"// semio-tokens: {tokens_digest()}\n"
        "digraph recherche {\n"
        f'  graph [ charset="UTF-8", size="{width:.2f},{height:.2f}"'
        f", margin={options.effective_margin}"
        f', bgcolor="{surface}", fontname="{options.font}" ];\n'
        f'  node [ shape="plaintext", fontname="{options.font}" ];\n'
        "  matrix [ label=<\n"
        # Outer wrapper carries title/foot on the plain surface — no grid colour,
        # or its cell spacing paints a heavy band around the whole figure.
        f'  <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="2"'
        f' BGCOLOR="{surface}">\n'
        + "\n".join(head)
        + ("\n" if head else "")
        + f'    <TR><TD COLSPAN="{span}">\n'
        # Only the matrix itself uses the border colour, showing through 1pt of cell
        # spacing as hairline gridlines — semio separates cells with fills, not rules.
        f'    <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="1" CELLPADDING="3"'
        f' BGCOLOR="{border}">\n'
        + "\n".join(lines)
        + "\n    </TABLE>\n    </TD></TR>\n"
        + foot
        + "\n  </TABLE>\n  > ];\n}\n"
    )


def _fmt(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:g}"


def drawing_size(dot: str, engine: str = "dot") -> tuple[float, float]:
    """Lay `dot` out without rendering and return the drawing size in inches.

    `-Tplain` emits `graph <scale> <width> <height>` as its first line.
    """
    from graphviz_env import run_graphviz

    run = run_graphviz(["-Tplain"], engine=engine, source=dot)
    if not run.ok:
        return (0.0, 0.0)
    first = run.stdout.decode("utf-8", errors="replace").splitlines()
    if not first:
        return (0.0, 0.0)
    parts = first[0].split()
    if len(parts) < 4 or parts[0] != "graph":
        return (0.0, 0.0)
    try:
        return (float(parts[2]), float(parts[3]))
    except ValueError:
        return (0.0, 0.0)


ALL_ENGINES = ("dot", "neato", "fdp", "sfdp", "circo", "twopi")


def page_scale(options: PrintOptions, width: float, height: float) -> float:
    """How far Graphviz must shrink a `width`x`height` drawing to fit the sheet.

    Graphviz's `size` only ever shrinks, so a scale of 1.0 means the drawing
    already fits and nothing is lost.
    """
    if width <= 0 or height <= 0:
        return 0.0
    page_width, page_height = options.canvas_inches()
    return min(1.0, page_width / width, page_height / height)


def choose_layout(
    nodes: list[DiagramNode],
    edges: list[DiagramEdge],
    options: PrintOptions,
    *,
    database: str = "",
    engines: tuple[str, ...] | None = None,
    rankdirs: tuple[str, ...] = ("LR", "TB"),
) -> tuple[str, str, float]:
    """Trial-lay out each candidate and keep whichever stays largest on the page.

    Aspect ratio is not the goal — legibility is. A drawing that has to shrink to a
    third of its size takes the captions down with it, so the objective is simply to
    maximise the on-page scale factor. Returns `(engine, rankdir, scale)`.
    """
    candidates = tuple(engines) if engines else (options.engine,)
    best = (options.engine, options.rankdir, 0.0)
    for engine in candidates:
        for rankdir in (rankdirs if engine == "dot" else ("LR",)):
            # Probe the real thing — legend and title change the proportions, so a
            # trial without them can pick a layout that loses once they are added.
            probe = replace(options, engine=engine, rankdir=rankdir)
            try:
                dot = build_dot(nodes, edges, probe, database=database)
                width, height = drawing_size(dot, engine)
            except Exception:
                continue
            scale = page_scale(options, width, height)
            if scale > best[2]:
                best = (engine, rankdir, scale)
    return best if best[2] > 0 else (options.engine, rankdirs[0], 0.0)


def _html_break(text: str, width: int) -> str:
    """Escape and wrap a short caption onto centred `<BR/>` lines.

    A `|` in the source is an explicit break point, because German compounds have
    to be split at a syllable the author chose — `Bauteil|gruppen`, never
    `Bauteilg|ruppen`. Without one, wrapping only ever happens at whitespace: a
    long single word makes its column wide, which is a layout problem to solve by
    shortening the header, not by mutilating it.
    """
    raw = " ".join(str(text).split())
    if "|" in raw:
        return "<BR/>".join(_html(part.strip()) for part in raw.split("|") if part.strip())
    if width <= 0 or len(raw) <= width:
        return _html(raw)
    lines = textwrap.wrap(raw, width=width, break_long_words=False, max_lines=3, placeholder="…")
    return "<BR/>".join(_html(line) for line in lines)


def _html_wrap(escaped: str, width: int) -> str:
    """Wrap already-escaped text onto `<BR/>` lines for an HTML-like label."""
    if width <= 0 or len(escaped) <= width:
        return escaped
    lines = textwrap.wrap(escaped, width=width, break_long_words=True, max_lines=4, placeholder="…")
    return '<BR ALIGN="LEFT"/>'.join(lines)


def _wrap(text: str, width: int) -> str:
    """Wrap a caption onto DOT line breaks so ellipses stay compact in print."""
    clean = " ".join(str(text).split())
    if not clean:
        return "?"
    if width <= 0 or len(clean) <= width:
        return _escape(clean)
    lines = textwrap.wrap(clean, width=width, break_long_words=True, max_lines=4, placeholder="…")
    return r"\n".join(_escape(line) for line in lines)


def _escape(text: str) -> str:
    return str(text).replace("\\", "\\\\").replace('"', '\\"')


def _html(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
