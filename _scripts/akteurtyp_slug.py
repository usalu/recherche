"""Legacy module: plan §6.1 uses Neo4j **primary labels**, not an `akteurtyp` property.

Use `akteur_org_neo4j_label.neo4j_label_for_akteur_folder` for import / generators.
"""

from __future__ import annotations

from pathlib import Path

from akteur_org_neo4j_label import SLUG_TO_LABEL

# Canonical organisation slugs that map to a typed primary label (subset check).
AKTEURTYP_CANONICAL: frozenset[str] = frozenset(SLUG_TO_LABEL.keys())


def akteurtyp_for_akteur_folder(_database_root: Path, _actor_id: str) -> str | None:
    """
    Deprecated — returns **None** so callers do not set `akteurtyp` on Neo4j nodes.
    Previously returned a canonical slug for `(:Akteur)`; organisation kind is now the label only.
    """
    return None
