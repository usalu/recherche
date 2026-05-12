"""Classify inventory `ort/<id>/` rows as Neo4j :Land vs :Stadt (plan §5.1a)."""

from __future__ import annotations

# Country / macro-region slugs used as `ort/` ids in this corpus → :Land.
# Extend when new country-level `ort/` ids appear in node_inventory.csv.
LAND_IDS: frozenset[str] = frozenset(
    {
        "Deutschland",
        "Schweiz",
        "Europa",
    }
)


def neo4j_label_for_ort_id(ort_id: str) -> str:
    return "Land" if ort_id in LAND_IDS else "Stadt"
