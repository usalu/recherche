"""Spec-driven loader for a Neo4j graph export.

No LaTeX, no display vocabulary (German short labels, escaping) -- those are
renderer concerns (render/latex/vocab.py, render/latex/escape.py). This
module produces a RawGraph shaped for the actor-network document family
(actors/roles/types/land/part/peers/projects), but HOW an arbitrary export's
labels/relationship-types map onto those buckets is entirely driven by a
GraphSpec (graph_spec.py) -- load_export() itself never mentions "Akteur" or
"HAT_AKTEURROLLE". ACTOR_NETWORK_SPEC below is this document's spec; a
different Neo4j export needs a different spec, not different code.
"""
import json, io, collections
from dataclasses import dataclass

from .graph_spec import GraphSpec, KindRule, RelRule

# region ActorNetworkSpec
# 🕸 Reproduces exactly the ontology the loader used to hardcode as a 6-branch
# if/elif chain (see the Stage-3 frozen reference, netz/tests/golden/
# frag_abb_stage3_reference.tex, for the byte-exact proof this spec preserves
# the original behavior). The live Neo4j DB has 57 node labels and 52
# relationship types; this spec only names the 6 this document draws from --
# every OTHER relationship type present in the export is unlisted and will
# raise at load time rather than being silently ignored.
ACTOR_NETWORK_SPEC = GraphSpec(
    kinds=(
        KindRule("Akteur", "actor"),
        KindRule("Projekt", "project"),
    ),
    default_kind="other",
    name_props=("name",),
    rels={
        "HAT_AKTEURROLLE": RelRule(bucket="roles", role="tag"),
        "HAT_AKTEURTYP": RelRule(bucket="types", role="attribute"),
        "LIEGT_IN_LAND": RelRule(bucket="land", role="attribute"),
        "BETEILIGT_AN": RelRule(bucket="part", role="edge", direction="forward"),
        "VERBUNDEN_MIT_AKTEUR": RelRule(bucket="peers", role="edge", direction="undirected"),
        "BETRIEBEN_VON": RelRule(bucket="peers", role="edge", direction="undirected"),
    },
    property_fallback={"land": "land"},
)
# endregion ActorNetworkSpec


@dataclass
class RawGraph:
    by: dict            # eid -> node dict
    nodes: list          # all nodes (mutable; overlay merge appends to it)
    actors: list         # node dicts of kind "actor" (spec-resolved)
    roles: dict          # eid -> set[str]  (canonical role strings)
    types: dict           # eid -> str       (canonical typ string)
    land: dict            # eid -> str       (German country name, as stated in source)
    part: dict             # eid -> set[eid]  (BETEILIGT_AN targets)
    peers: dict              # eid -> set[eid]  (undirected peer edges)
    land_fixed: int           # count of actors repaired via the property-fallback rule
    projects: list              # eid list, deterministically sorted (name, eid)

    def name(self, e):
        return self.by[e]["properties"].get("name", "?") if e in self.by else "?"


def _kind_of(spec: GraphSpec, node: dict) -> str:
    labels = node.get("labels", [])
    for rule in spec.kinds:
        if rule.label in labels:
            return rule.kind
    return spec.default_kind


def _name_of(spec: GraphSpec, by: dict, e: str) -> str:
    if e not in by:
        return "?"
    props = by[e]["properties"]
    for prop in spec.name_props:
        if props.get(prop):
            return props[prop]
    return "?"


def load_export(path: str, spec: GraphSpec = ACTOR_NETWORK_SPEC) -> RawGraph:
    d = json.load(io.open(path, encoding="utf-8"))
    by = {n["eid"]: n for n in d["nodes"]}
    nodes = list(d["nodes"])
    actors = [n for n in nodes if _kind_of(spec, n) == "actor"]

    tags = collections.defaultdict(lambda: collections.defaultdict(set))
    scalars = collections.defaultdict(dict)
    for r in d["relationships"]:
        t, s, e = r["type"], r["start"], r["end"]
        rule = spec.rels.get(t)
        if rule is None:
            raise ValueError(
                f"unspecified relationship type {t!r} -- add a RelRule to the "
                f"GraphSpec (role='drop' if intentionally unused by this document)")
        if rule.role == "drop":
            continue
        target_name = _name_of(spec, by, e)
        if rule.role == "tag":
            tags[rule.bucket][s].add(target_name)
        elif rule.role == "attribute":
            scalars[rule.bucket][s] = target_name
        elif rule.role == "edge":
            if rule.direction == "undirected":
                if s != e:
                    tags[rule.bucket][s].add(e)
                    tags[rule.bucket][e].add(s)
            else:
                tags[rule.bucket][s].add(e)

    roles = tags["roles"]
    types = scalars["types"]
    part = tags["part"]
    peers = tags["peers"]

    # Property-fallback repair (ported verbatim from net_lib.Net for this
    # spec: 5 actors carry a `land` property but no LIEGT_IN_LAND edge) --
    # generic over any scalar bucket the spec names, not just "land".
    land_fixed = 0
    for bucket_name, prop_name in spec.property_fallback.items():
        target = scalars[bucket_name]
        for a in actors:
            if a["eid"] not in target and prop_name in a["properties"]:
                target[a["eid"]] = a["properties"][prop_name]
                land_fixed += 1
    land = dict(scalars["land"])

    # Projects: BETEILIGT_AN targets resolved (by the spec's kind rules) to
    # "project". Secondary key `e` (eid) breaks ties deterministically --
    # `part[...]` is a set, so two projects sharing an identical display name
    # would otherwise tie-break in hash-random per-process order (Stage 0
    # finding).
    projects = sorted(
        {e for a in actors for e in part[a["eid"]] if _kind_of(spec, by[e]) == "project"},
        key=lambda e: (_name_of(spec, by, e), e),
    )

    return RawGraph(by=by, nodes=nodes, actors=actors, roles=roles, types=types,
                     land=land, part=part, peers=peers, land_fixed=land_fixed,
                     projects=projects)
