"""Which nodes count as "genuinely networked" for edge-drawing purposes.
Verbatim port of netplate.drawn_nodes.

A hub with more than FAN_THRESH degree-1 leaves is a directory-style fan (a
materials directory with many one-tie members) -- its leaves are excluded
from edge-drawing so the graph doesn't render a giant star. Any remaining
fragment smaller than min_comp (an isolated pair, a lone triangle-less edge)
is also excluded. The RETURNED SET is order-independent (it's a set, built
via set union of connected components) -- safe under Stage 0's determinism
rules without further sorting.
"""
import networkx as nx

FAN_THRESH = 8


def drawn_edge_nodes(panel, min_comp: int = 3, drop_fans: bool = True) -> set:
    nodes = set(panel.actors) | set(panel.projects)
    g = nx.Graph(); g.add_nodes_from(nodes); g.add_edges_from(panel.edges)
    if drop_fans:
        deg = dict(g.degree())
        leaves = set()
        for hub in nodes:
            lv = [w for w in g.neighbors(hub) if deg[w] == 1]
            if len(lv) > FAN_THRESH:
                leaves.update(lv)
        nodes -= leaves
        g = g.subgraph(nodes)
    if not nodes:
        return set()
    return set().union(*[c for c in nx.connected_components(g) if len(c) >= min_comp])
