"""Classify `akteur/<id>/` folders as organisation vs natural person (:Person).

Organisation rows get their Neo4j **primary label** from §6.1 (`akteur_org_neo4j_label.py`);
only persons are `:Person` here; organisations are never all lumped under a single `:Akteur`
unless the slug resolver falls back to `:Akteur`.
"""

from __future__ import annotations

import re
from pathlib import Path


def is_person_akteur_folder(database_root: Path, actor_id: str) -> bool:
    """True when `_database/akteur/<id>/` represents a natural person (not an organisation)."""
    idx = database_root / "akteur" / actor_id / "index.md"
    if not idx.is_file():
        return False
    text = idx.read_text(encoding="utf-8", errors="replace")[:12000]
    if re.search(r'legacy_type:\s*["\']Person["\']', text):
        return True
    if "akteurtyp/Person" in text:
        return True
    return False


def split_akteur_ids(database_root: Path, akteur_ids: list[str]) -> tuple[list[str], list[str]]:
    persons: list[str] = []
    orgs: list[str] = []
    for aid in sorted(akteur_ids):
        if is_person_akteur_folder(database_root, aid):
            persons.append(aid)
        else:
            orgs.append(aid)
    return persons, orgs
