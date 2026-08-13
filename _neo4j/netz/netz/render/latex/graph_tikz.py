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
from ...model.variants import node_role, PLAIN
from ...mechanisms.connectivity import drawn_edge_nodes
from ...mechanisms.layout import force_layout, DEFAULT_FRAME
from .vocab import CC_NAME


def node_tikz(net, e, x, y, label=True):
    role = node_role(net, e)
    opt = "" if role is PLAIN else "[state=%s]" % role.state
    tid = net.tid[e] if label else ""
    return r"\SemioGraphNode%s{%.2f,%.2f}{%s}" % (opt, x, y, tid)


def country_figure(net, cc, frame=DEFAULT_FRAME):
    pan = net.panels[cc]
    nodes = list(pan.actors) + list(pan.projects)
    if not nodes:
        return None
    keep = drawn_edge_nodes(pan)
    P, edges = force_layout(pan, keep, frame)
    nA = len(pan.actors)
    nP = len(pan.projects)
    s = [r"\begin{GraphFigure}[title={%s \textperiodcentered\ %d Organisationen \textperiodcentered\ %d Projekte}, width=%.2f, height=%.2f]"
         % (CC_NAME.get(cc, cc), nA, nP, frame.w, frame.h)]
    for a, b in edges:
        ax, ay = P[a]; bx, by = P[b]
        s.append(r"\SemioGraphEdge{%.2f,%.2f}{%.2f,%.2f}" % (ax, ay, bx, by))
    for e in nodes:
        px, py = P[e]
        s.append(node_tikz(net, e, px, py, label=True))
    s.append(r"\end{GraphFigure}")
    return "\n".join(s), nA, nP, len(nodes), 0
