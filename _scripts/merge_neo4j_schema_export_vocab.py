#!/usr/bin/env python3
"""Merge controlled vocabulary from node_inventory into neo4j_schema_export.json.

Run from repo root after inventory or taxonomy changes:
  python _scripts/merge_neo4j_schema_export_vocab.py

Reads:
  _database/_system/node_inventory.csv
  _database/_system/neo4j_schema_export.json (must exist; preserves live_graph etc.)

Writes the same JSON path with added/updated keys:
  controlled_vocabulary, hat_art_allowlist, gehoert_zu_rolle_allowlist,
  csv_relations_skipped_from_graph, inventory_entity_graph_policy
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import import_database_folder_to_neo4j as imp  # noqa: E402
from neo4j_relation_fold import SKIP_RELATIONS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "_database" / "_system" / "node_inventory.csv"
EDGES = ROOT / "_database" / "_edges" / "clean_confirmed_edges.csv"
EXPORT = ROOT / "_database" / "_system" / "neo4j_schema_export.json"

HAT_ART_ALLOWLIST = sorted(
    {
        "akteur",
        "entwurf",
        "huerde",
        "intervention",
        "kontextmerkmal",
        "logistik",
        "norm",
        "nutzung",
        "person",
        "pruefung",
        "prozessphase",
        "recht",
        "ressourcenquelle",
        "reversibilitaet",
        "schadstoff",
        "status",
        "verbindungstechnik",
        "wirtschaft",
        "wiederverwendungsart",
        "zertifizierung",
    }
)

GEHOERT_ZU_ROLLE_ALLOWLIST = sorted(
    {
        "einbauort",
        "fallbeispiel",
        "herkunft",
        "kette",
        "land",
        "programm",
        "software",
        "stadt",
        "transport",
        "verarbeitung",
        "zwischenlager",
    }
)


def load_inventory_by_entity() -> dict[str, list[dict[str, str]]]:
    by_ent: dict[str, list[dict[str, str]]] = defaultdict(list)
    with INVENTORY.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            ent = (row.get("entity") or "").strip()
            if not ent:
                continue
            by_ent[ent].append(
                {
                    "id": (row.get("id") or "").strip(),
                    "typed_path": (row.get("typed_path") or "").strip(),
                    "title": (row.get("title") or "").strip(),
                }
            )
    for ent in by_ent:
        by_ent[ent].sort(key=lambda x: x["id"].lower())
    return dict(sorted(by_ent.items(), key=lambda kv: kv[0].lower()))


def entity_graph_policy(entity: str) -> dict[str, str | None]:
    """How this inventory entity maps to Neo4j (plan §5.2 / §5.4 + importer)."""
    if entity in imp.SKIP_NODE_ENTITIES:
        return {
            "vertex_kind": "none",
            "neo4j_label": None,
            "note": "plan §5.4 SKIP_NODE_ENTITIES — no standalone graph vertex from this folder",
        }
    if entity == "datenmodell":
        return {
            "vertex_kind": "none",
            "neo4j_label": None,
            "note": "importer skips :Datenmodell nodes; has_datenmodell edges folded away",
        }
    if entity == "tooltyp":
        return {
            "vertex_kind": "none",
            "neo4j_label": None,
            "note": "importer skips :Tooltyp; tool categories as properties on Software/Tool",
        }
    if entity == "akteur":
        return {
            "vertex_kind": "dynamic",
            "neo4j_label": None,
            "note": "resolved per row via akteur_org_neo4j_label.py (§6.1 org labels or Akteur)",
        }
    if entity == "ort":
        return {
            "vertex_kind": "dynamic",
            "neo4j_label": None,
            "note": "resolved per row via ort_geo_label.py → Land or Stadt",
        }
    if entity == "software_digitaltool":
        return {
            "vertex_kind": "dynamic",
            "neo4j_label": None,
            "note": "resolved per row via software_tool_label.py → Software or Tool",
        }
    if entity in imp.ENTITY_LABEL:
        return {
            "vertex_kind": "static",
            "neo4j_label": imp.ENTITY_LABEL[entity],
            "note": "ENTITY_LABEL in import_database_folder_to_neo4j.py",
        }
    return {
        "vertex_kind": "unknown",
        "neo4j_label": None,
        "note": "entity present in node_inventory.csv but not in ENTITY_LABEL — extend importer if needed",
    }


def load_csv_relation_tokens() -> list[str]:
    rels: set[str] = set()
    with EDGES.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            r = (row.get("relation") or "").strip()
            if r:
                rels.add(r)
    return sorted(rels, key=str.lower)


def main() -> int:
    if not EXPORT.exists():
        print(f"Missing {EXPORT}", file=sys.stderr)
        return 1
    with EXPORT.open(encoding="utf-8") as f:
        data = json.load(f)

    by_entity = load_inventory_by_entity()
    entities = sorted(by_entity.keys(), key=str.lower)

    data["controlled_vocabulary"] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_file": str(INVENTORY.relative_to(ROOT)).replace("\\", "/"),
        "entry_count": sum(len(v) for v in by_entity.values()),
        "entities": entities,
        "entries_by_entity": by_entity,
    }
    data["hat_art_allowlist"] = HAT_ART_ALLOWLIST
    data["gehoert_zu_rolle_allowlist"] = GEHOERT_ZU_ROLLE_ALLOWLIST
    data["csv_relations_skipped_from_graph"] = sorted(SKIP_RELATIONS)
    data["inventory_entity_graph_policy"] = {
        ent: entity_graph_policy(ent) for ent in entities
    }
    rel_tokens = load_csv_relation_tokens()
    data["csv_edge_relation_vocabulary"] = {
        "generated_at": data["controlled_vocabulary"]["generated_at"],
        "source_file": str(EDGES.relative_to(ROOT)).replace("\\", "/"),
        "relation_count": len(rel_tokens),
        "relations": rel_tokens,
    }

    # Complete static label map for entities that use ENTITY_LABEL (no dynamic rows)
    static_map = {k: v for k, v in imp.ENTITY_LABEL.items()}
    data["inventory_entity_to_neo4j_label"] = static_map
    data["inventory_entity_to_neo4j_label_notes"] = {
        "akteur": "dynamic — see inventory_entity_graph_policy",
        "ort": "dynamic — Land|Stadt",
        "software_digitaltool": "dynamic — Software|Tool",
        "datenmodell": "no vertex",
        "tooltyp": "no vertex",
    }

    with EXPORT.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(
        f"Wrote {EXPORT.relative_to(ROOT)}: "
        f"{data['controlled_vocabulary']['entry_count']} vocabulary entries, "
        f"{len(entities)} entities."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
