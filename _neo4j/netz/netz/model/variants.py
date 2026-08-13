"""Node roles: the one semantic classification consumed by BOTH the graph
circle styling and the (future) table markers. Computed once here instead of
the legacy pattern of two independent if-chains (gen_abb.node_tikz vs
gen_tables2.row) that happened to encode the same three states differently.

`state` is the semio-graph vocabulary word (print/tex/semio-graph.sty) --
an ABSTRACT visual-semantic role (base/focal/attested/hypo), never a dataset
word. It is the ONLY styling knowledge left on the Python side: everything a
state actually looks like (border, fill, radius, dash pattern, label
emphasis) lives in the .sty. `ROLES` is simultaneously the precedence order
(see below) and the legend order -- adding a role is editing this one tuple,
nothing downstream needs a second edit.

Precedence (exact match to the legacy behavior): a Projekt is always styled
as focal, even if it happens to also be newly-researched or country-inferred.
Otherwise "attested" (researched) beats "hypo" (country-inferred) -- an
overlay-added actor with an inferred country is still shown as researched,
not as inferred (see the `and not is_new` in the legacy `is_inf` check).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class NodeRole:
    key: str        # internal id (also the future table marker column)
    state: str      # semio-graph state name; "" = the base state
    legend_de: str  # what this role means in THIS document


PLAIN = NodeRole("default", "", "")
FOCAL = NodeRole("project", "focal", "Projekt")
ATTESTED = NodeRole("researched", "attested", "neu recherchiert")
HYPO = NodeRole("country-inferred", "hypo", "Land erschlossen")

ROLES = (FOCAL, ATTESTED, HYPO)


def node_role(net, e: str) -> NodeRole:
    if e in net.res.proj_cc:
        return FOCAL
    if e in net.new_eids:
        return ATTESTED
    if e in net.res.inferred:
        return HYPO
    return PLAIN
