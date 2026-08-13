"""The semantic Network: composes data (loaders + overlay merge) with the
country/identity mechanisms into the one object the renderer consumes.
Mirrors netplate.Model.__init__ end-to-end (verbatim-equivalent construction
order), but as an explicit pipeline of named steps instead of one constructor.
"""
from dataclasses import dataclass

from ..data.neo4j_export import load_export, RawGraph
from ..data.overlays import apply_overlays
from ..data.audit_edges import load_peer_edges
from ..data.strict_review import StrictReviewBundle, apply_strict_review
from ..mechanisms.countries import (
    resolve_countries, whitelist_countries, partition, cross_border_edges,
    is_person, CountryResolution, Panel,
)
from ..mechanisms.identity import assign_num, assign_ids


@dataclass
class Network:
    raw: RawGraph
    aset: set                    # drawn-eligible actors (post prune)
    new_eids: set                 # overlay-added (researched) actor/project eids
    new_proj_cc: dict              # harvested project eid -> ISO2
    res: CountryResolution          # country assignment
    countries: list                  # whitelisted, ranked
    panels: dict                      # country -> Panel
    drawn: set                         # globally-claimed edge keys
    cross: list                         # cross-border edges (listed, not drawn)
    num: dict                            # internal tie-break numbers
    tid: dict                             # public id (graph label == table key)
    audit_edges_applied: int               # existence-filtered count (parity: 175)
    overlay_reports: list                   # per-overlay OverlayReport


def build_network(sources, exclude: frozenset = frozenset(),
                   edge_exclude: frozenset = frozenset(),
                   strict_review: StrictReviewBundle | None = None) -> Network:
    strict_review = strict_review or StrictReviewBundle()
    raw = load_export(sources.export_path)
    new_eids, new_proj_cc, overlay_reports = apply_overlays(raw, sources.overlay_paths)
    apply_strict_review(raw, new_proj_cc, strict_review)

    # known<->known peer edges (second-audit findings) -- existence-filtered,
    # exactly like netplate.Model's `extra_peers` handling.
    audit_pairs = load_peer_edges(sources.audit_edges_path)
    applied = 0
    for a, b in audit_pairs:
        if a in raw.by and b in raw.by and a != b:
            raw.peers[a].add(b); raw.peers[b].add(a)
            applied += 1

    aset = {a["eid"] for a in raw.actors if a["eid"] not in exclude}

    res = resolve_countries(raw, aset, new_proj_cc, exclude)
    countries = whitelist_countries(res)
    panels, drawn = partition(raw, res, countries, aset, edge_exclude)
    cross = cross_border_edges(raw, aset, res, drawn)

    num = assign_num(raw, panels)
    tid = assign_ids(raw, panels, res.cc, is_person)

    return Network(raw=raw, aset=aset, new_eids=new_eids, new_proj_cc=new_proj_cc,
                    res=res, countries=countries, panels=panels, drawn=drawn,
                    cross=cross, num=num, tid=tid, audit_edges_applied=applied,
                    overlay_reports=overlay_reports)
