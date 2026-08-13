"""Loader for the FR/BE de-duplication removal list (prune_eids.json)."""
import json, io


def load_prune(path: str) -> frozenset:
    return frozenset(json.load(io.open(path, encoding="utf-8")))
