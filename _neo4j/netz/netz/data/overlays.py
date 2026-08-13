"""Overlay merge: research-harvested entities/edges layered onto a RawGraph.

Verbatim port of net_lib.Net._merge_overlay, applied in file order
["", "2", "3"]. First-wins name-join semantics preserved. Unlike the legacy
version (which silently drops an unresolved `to_known` name-join), this
module SURFACES misses in the returned OverlayReport -- observability only,
does not change what gets merged (parity-safe).
"""
import json, io
from dataclasses import dataclass, field
from .neo4j_export import RawGraph
from ._identity import ISO_INV, ROLE_DE, ROLE_INV


@dataclass
class OverlayReport:
    entities_added: int = 0
    edges_resolved: int = 0
    edges_dropped_no_src: int = 0        # ed["src"] not in this overlay's entity keymap
    edges_dropped_no_target: int = 0     # to_known name or to_new key didn't resolve
    edges_dropped_self_loop: int = 0
    unresolved_to_known_names: list = field(default_factory=list)  # observability


def load_overlay_json(path: str) -> dict:
    return json.load(io.open(path, encoding="utf-8"))


def apply_overlay(raw: RawGraph, overlay: dict, new_eids: set, new_proj_cc: dict) -> OverlayReport:
    """Mutates `raw` (nodes/by/actors/roles/types/land/peers) and the caller's
    `new_eids`/`new_proj_cc` accumulators in place -- mirrors the legacy
    in-place mutation style so the ported logic stays line-for-line
    comparable. Returns a report for this one overlay."""
    rpt = OverlayReport()
    keymap = {}
    for ent in overlay["entities"]:
        eid = "NEW:" + ent["key"]
        keymap[ent["key"]] = eid
        is_proj = ent.get("is_project", False)
        node = {"eid": eid, "labels": ["Projekt" if is_proj else "Akteur"],
                "properties": {"id": ent["key"], "name": ent["name"]}}
        raw.by[eid] = node
        raw.nodes.append(node)
        if not is_proj:
            raw.actors.append(node)
        new_eids.add(eid)
        rpt.entities_added += 1
        cc_full = ISO_INV.get(ent["cc"])
        if cc_full:
            raw.land[eid] = cc_full
        if is_proj and ent.get("cc"):
            new_proj_cc[eid] = ent["cc"]
        for r in ent.get("rollen", []):
            canon = r if r in ROLE_DE else ROLE_INV.get(r, r)
            raw.roles[eid].add(canon)
        raw.types[eid] = ent["typ"]

    # resolve known targets by name -> eid (first-wins over actor insertion order)
    name2eid = {}
    for a in raw.actors:
        name2eid.setdefault(a["properties"]["name"], a["eid"])

    for ed in overlay["edges"]:
        s = keymap.get(ed["src"])
        if not s:
            rpt.edges_dropped_no_src += 1
            continue
        if "to_known" in ed:
            t = name2eid.get(ed["to_known"])
            if t is None:
                rpt.unresolved_to_known_names.append(ed["to_known"])
        else:
            t = keymap.get(ed["to_new"])
        if not t:
            rpt.edges_dropped_no_target += 1
            continue
        if t == s:
            rpt.edges_dropped_self_loop += 1
            continue
        raw.peers[s].add(t); raw.peers[t].add(s)
        rpt.edges_resolved += 1
    return rpt


def apply_overlays(raw: RawGraph, overlay_paths) -> tuple:
    """Apply overlays in the given path order. Returns (new_eids: set,
    new_proj_cc: dict, reports: list[OverlayReport])."""
    new_eids = set()
    new_proj_cc = {}
    reports = []
    for path in overlay_paths:
        overlay = load_overlay_json(path)
        reports.append(apply_overlay(raw, overlay, new_eids, new_proj_cc))
    return new_eids, new_proj_cc, reports
