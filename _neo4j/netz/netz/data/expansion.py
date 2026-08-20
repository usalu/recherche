"""Read-only activation of the approved LaTeX actor-network expansion."""
from __future__ import annotations

import json
from pathlib import Path

from ._identity import ISO_INV


def apply_expansion(raw, new_proj_cc: dict, path: str) -> set[str]:
    file = Path(path)
    if not file.exists():
        return set()
    data = json.loads(file.read_text(encoding="utf-8"))
    if not data.get("approved_for_latex"):
        return set()

    added = set()
    actor_ids = {row["eid"] for row in raw.actors}
    for row in data.get("nodes", []):
        eid = row["eid"]
        if eid in raw.by:
            raise RuntimeError(f"expansion EID already exists: {eid}")
        kind = row["kind"]
        if kind not in {"actor", "project"}:
            raise RuntimeError(f"invalid expansion node kind: {eid}: {kind}")
        node = {
            "eid": eid,
            "labels": ["Akteur" if kind == "actor" else "Projekt"],
            "properties": {
                "name": row["name"],
                "primary_source_url": row["source_url"],
            },
        }
        raw.nodes.append(node)
        raw.by[eid] = node
        raw.roles[eid] = set(row.get("roles") or [])
        if kind == "actor":
            raw.actors.append(node)
            actor_ids.add(eid)
            raw.types[eid] = row["type"]
            raw.land[eid] = ISO_INV[row["cc"]]
        else:
            raw.projects.append(eid)
            new_proj_cc[eid] = row["cc"]
        added.add(eid)

    raw.projects = sorted(set(raw.projects), key=lambda eid: (raw.name(eid), eid))
    project_ids = set(raw.projects)
    seen = set()
    for edge in data.get("edges", []):
        source, target = edge["pair"]
        if source not in actor_ids or target not in project_ids:
            raise RuntimeError(
                f"invalid expansion edge endpoints: {edge.get('id')}: "
                f"{source} -> {target}"
            )
        pair = (source, target)
        if pair in seen or target in raw.part[source]:
            raise RuntimeError(f"duplicate expansion edge: {pair}")
        seen.add(pair)
        raw.part[source].add(target)
    return added
