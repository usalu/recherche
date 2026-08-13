"""Loader for the FR/BE de-duplication removal list (prune_eids.json) and the
fact-check's node/edge exclusion lists."""
import json, io


def load_prune(path: str) -> frozenset:
    return frozenset(json.load(io.open(path, encoding="utf-8")))


def load_edge_exclude(path: str) -> frozenset:
    """[eid_a, eid_b] pairs -> normalized (min, max) tuples, matching how
    `partition()` keys its own edges."""
    pairs = json.load(io.open(path, encoding="utf-8"))
    return frozenset(tuple(sorted(p)) for p in pairs)
