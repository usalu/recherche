"""Graph renderer: one node/edge emitter + one figure assembler per country.

Stage 6: emits calls into the semio-graph mechanism (print/tex/semio-graph.sty,
a first-class package registered in semio.cls -- no longer a spliced preamble
fragment) instead of TikZ style-name literals. The renderer no longer knows
what a "project" looks like at all -- it passes the abstract state name
(model.variants.node_role) and the .sty decides border/fill/radius/dash. This
changes rendered LaTeX BYTES (gate = PDF pixel parity, not byte-diff; see
netz/tests/golden/frag_abb_stage3_reference.tex for the frozen Stage 3 proof
that the underlying model/mechanism pipeline was already byte-exact before
Stage 4/6's renderer changes).
"""
import json
import os

from ...model.variants import node_role, PLAIN
from ...mechanisms.connectivity import drawn_edge_nodes
from ...mechanisms.layout import force_layout, DEFAULT_FRAME
from .vocab import CC_NAME
from .table_grid import load_kanten


def load_image_manifest(path):
    """Return accepted, existing pilot assets keyed by eid.

    The transport manifest is deliberately optional. Invalid or incomplete
    rows never change the historical rendering path; they are ignored here
    and reported by the dedicated pilot validator instead.
    """
    if not path:
        return {}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    base = os.path.dirname(os.path.abspath(path))
    result = {}
    for row in data.get("nodes", []):
        if row.get("review_status") != "accepted" or row.get("result") != "logo":
            continue
        asset = row.get("asset_path") or ""
        if not asset:
            continue
        resolved = asset if os.path.isabs(asset) else os.path.join(base, asset)
        if os.path.isfile(resolved) and row.get("eid"):
            result[row["eid"]] = os.path.abspath(resolved).replace("\\", "/")
    return result


def load_edge_kinds(kanten_path, net, redirects_path=None):
    """(eid, eid) sorted pair -> \\SemioGraphEdge kind for every DRAWN edge.

    Two classes, taken straight from the relationship classification's own
    `kind` field -- no new judgment made here:
      AKTEUR-BAUVORHABEN (project role)      -> plain (unchanged, the default)
      AKTEUR-AKTEUR      (organisational tie) -> muted (semio-graph.sty,
                                                 already defined, never used)

    Reuses table_grid.load_kanten for the membership test itself: that
    function is what turned up (and fixed) the case where a "known" edge
    wasn't actually drawn, so this lookup is built the same way rather than
    re-deriving drawn-ness a second time.
    """
    by_cc = load_kanten(kanten_path, net, redirects_path)
    kinds = {}
    for cc in by_cc:
        for k in by_cc[cc]:
            if k.get("kind") == "AKTEUR-AKTEUR":
                kinds[tuple(sorted(k["pair"]))] = "muted"
    return kinds


def node_tikz(net, e, x, y, label=True, images=None):
    role = node_role(net, e)
    options = [] if role is PLAIN else ["state=%s" % role.state]
    image = (images or {}).get(e)
    if image:
        options.append("image={%s}" % image)
    opt = "[%s]" % ",".join(options) if options else ""
    tid = net.tid[e] if label else ""
    return r"\SemioGraphNode%s{%.2f,%.2f}{%s}" % (opt, x, y, tid)


def country_figure(net, cc, frame=DEFAULT_FRAME, images=None, edge_kinds=None):
    pan = net.panels[cc]
    nodes = list(pan.actors) + list(pan.projects)
    if not nodes:
        return None
    # The reviewed LaTeX graph is evidence-complete: a valid relationship is
    # visible even when it forms only a two-node component.
    keep = drawn_edge_nodes(pan, min_comp=2)
    P, edges = force_layout(pan, keep, frame)
    nA = len(pan.actors)
    nP = len(pan.projects)
    s = [r"\begin{GraphFigure}[title={%s \textperiodcentered\ %d Organisationen \textperiodcentered\ %d Projekte}, width=%.2f, height=%.2f]"
         % (CC_NAME.get(cc, cc), nA, nP, frame.w, frame.h)]
    for a, b in edges:
        ax, ay = P[a]; bx, by = P[b]
        kind = (edge_kinds or {}).get(tuple(sorted((a, b))))
        opt = "[kind=%s]" % kind if kind else ""
        s.append(r"\SemioGraphEdge%s{%.2f,%.2f}{%.2f,%.2f}" % (opt, ax, ay, bx, by))
    for e in nodes:
        px, py = P[e]
        # Projects remain image-free even if a malformed manifest contains
        # their eid. Only organisation rows may activate the optional key.
        node_images = images if e in pan.actors else None
        s.append(node_tikz(net, e, px, py, label=True, images=node_images))
    s.append(r"\end{GraphFigure}")
    return "\n".join(s), nA, nP, len(nodes), 0
