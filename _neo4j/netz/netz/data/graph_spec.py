"""Declarative description of how to interpret a Neo4j export into a
RawGraph. This is what makes the loader (neo4j_export.py) generic: kind
resolution, the display-name fallback, and each relationship type's semantic
role used to be a hardcoded 6-branch if/elif chain -- one export, one graph.
A GraphSpec turns that ontology into DATA, so a differently-shaped Neo4j
export (different labels, different relationship types) is a new spec, not
new code. The live DB behind this document has 57 node labels and 52
relationship types; this document's export uses 6 of them (see
ACTOR_NETWORK_SPEC in neo4j_export.py) -- the spec is what lets a future
export use a different 6 (or 60) without touching load_export.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class KindRule:
    """A node carrying `label` anywhere in its label list resolves to `kind`.
    Rules are tried in order; first match wins. Testing LIST MEMBERSHIP (not
    exact list equality) fixes a real bug in the original loader: it tested
    `labels == ["Akteur"]`, so any node carrying a second label would have
    silently vanished from every kind bucket. No node in the current export
    carries more than one label (verified against the live file), so the fix
    changes no counts today -- it only protects a future export that does."""
    label: str
    kind: str


@dataclass(frozen=True)
class RelRule:
    """How one relationship type is folded into a RawGraph bucket.

    role:
      "edge"      -- kept as adjacency pairs in `bucket`
      "attribute" -- target's resolved display name becomes a scalar in
                     `bucket[source]` (last write wins if the type recurs)
      "tag"       -- target's resolved display name becomes a member of the
                     set `bucket[source]`
      "drop"      -- present in the export, deliberately unused by this
                     document

    An UNLISTED relationship type raises at load time rather than being
    silently ignored -- every type present in an export is a conscious
    "edge / attribute / tag / drop" decision, never an accidental no-op.

    direction (role="edge" only):
      "forward"    -- kept as stored (e.g. an actor participating in a
                       project)
      "undirected" -- inserted symmetrically; a self-loop (source == target)
                       is dropped
    """
    bucket: str
    role: str
    direction: str = "forward"


@dataclass(frozen=True)
class GraphSpec:
    kinds: tuple            # KindRule, ... tried in order, first match wins
    default_kind: str
    name_props: tuple        # display-name fallback chain, e.g. ("name",)
    rels: dict                 # relationship type -> RelRule
    property_fallback: dict      # bucket -> node property name; merged in for
                                   # a node whose grouping relationship never
                                   # fired but which carries the equivalent
                                   # property directly (the "hub node OR
                                   # scalar property" pattern -- this export
                                   # has both: LIEGT_IN_LAND edges for most
                                   # actors, a bare `land` property for 5)
