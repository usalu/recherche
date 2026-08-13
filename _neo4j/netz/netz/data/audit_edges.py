"""Loader for the second-audit known<->known peer edges (audit2_peer_edges.json).

Pure load only -- existence-filtering against the graph (the legacy
`extra_peer_pairs` count) happens when these are APPLIED, which is a
Network-construction concern (Stage 2), not a loading concern.
"""
import json, io


def load_peer_edges(path: str) -> list:
    """Returns [(a, b), ...] in file order (deterministic -- JSON array order,
    not a set, so no sorting is needed here)."""
    d = json.load(io.open(path, encoding="utf-8"))
    return [(e["a"], e["b"]) for e in d["edges"]]
