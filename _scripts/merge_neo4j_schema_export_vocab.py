#!/usr/bin/env python3
"""Merge controlled taxonomy vocabulary into neo4j_schema_export.json (compact).

Only Stammdaten / bounded knot folders — excludes case instances, actors, sources,
components, metrics, etc. Format: one sorted list of typed_path strings.

Run from repo root:
  python _scripts/merge_neo4j_schema_export_vocab.py

Reads:
  _database/_system/node_inventory.csv
  _database/_system/neo4j_schema_export.json
  _database/_edges/clean_confirmed_edges.csv (relation tokens only)

Removes legacy verbose keys if present (controlled_vocabulary, inventory_entity_graph_policy, …).
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import import_database_folder_to_neo4j as imp  # noqa: E402
from neo4j_relation_fold import SKIP_RELATIONS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "_database" / "_system" / "node_inventory.csv"
EDGES = ROOT / "_database" / "_edges" / "clean_confirmed_edges.csv"
EXPORT = ROOT / "_database" / "_system" / "neo4j_schema_export.json"

# Inventory `entity` values that are bounded taxonomy / knot vocabulary (not cases, actors, quellen, …).
CONTROLLED_VOCAB_ENTITIES: frozenset[str] = frozenset(
    {
        "akteurrolle",
        "aufbereitungsverfahren",
        "bauaufgabe_intervention",
        "bauobjektklasse",
        "bauobjektrolle",
        "bauobjektstatus",
        "bausystem",
        "bauteilebene",
        "bauteiltyp",
        "bauteilzustand",
        "bauweise",
        "beschaffungsweg",
        "bewertungslogik_abgrenzung",
        "datenqualitaet",
        "foerderprogramm",
        "fuegung_verbindung",
        "funktionswechsel",
        "huerde",
        "kontextmerkmal",
        "leistungsanforderung",
        "logistik",
        "material",
        "methode",
        "norm",
        "nutzung",
        "programm_kontext",
        "prozessphase",
        "pruefung_nachweis",
        "rechtliche_bedingung",
        "ressourcenquelle",
        "reuse_einsatzstatus",
        "reuse_kette",
        "reuse_strategie",
        "rueckbauverfahren",
        "schadstoff",
        "tragwerksprinzip",
        "wirtschaft",
        "zertifizierung_bewertungssystem",
    }
)

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


def load_controlled_paths() -> tuple[list[str], dict[str, int]]:
    """Return sorted typed_path list + per-entity counts (controlled entities only)."""
    by_ent: dict[str, list[str]] = {e: [] for e in sorted(CONTROLLED_VOCAB_ENTITIES)}
    with INVENTORY.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            ent = (row.get("entity") or "").strip()
            if ent not in CONTROLLED_VOCAB_ENTITIES:
                continue
            tp = (row.get("typed_path") or "").strip()
            if tp:
                by_ent[ent].append(tp)
    counts = {e: len(by_ent[e]) for e in sorted(by_ent)}
    paths: list[str] = []
    for e in sorted(by_ent):
        paths.extend(sorted(by_ent[e], key=str.lower))
    paths.sort(key=str.lower)
    return paths, counts


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

    paths, ent_counts = load_controlled_paths()
    ts = datetime.now(timezone.utc).isoformat()

    # Drop legacy bulky blocks from earlier export runs
    data.pop("inventory_entity_graph_policy", None)
    old_cv = data.pop("controlled_vocabulary", None)
    data.pop("csv_edge_relation_vocabulary", None)
    data.pop("hat_art_allowlist", None)
    data.pop("gehoert_zu_rolle_allowlist", None)
    data.pop("csv_relations_skipped_from_graph", None)

    data["controlled_vocab"] = {
        "t": ts,
        "src": str(INVENTORY.relative_to(ROOT)).replace("\\", "/"),
        "n": len(paths),
        "omit": sorted(
            {
                "akteur",
                "akteur_beteiligung",
                "bauobjekt",
                "datenmodell",
                "datenpunkt",
                "dokumenttyp",
                "fallstudie",
                "kennwertdefinition",
                "ort",
                "projekt",
                "quelle",
                "reuse_einsatz",
                "reuse_kettenstation",
                "software_digitaltool",
                "tooltyp",
                "tragwerkstyp",
            }
        ),
        "c": ent_counts,
        "p": paths,
    }
    data["hat_art"] = HAT_ART_ALLOWLIST
    data["gzu_rolle"] = GEHOERT_ZU_ROLLE_ALLOWLIST
    data["csv_rel_skip"] = sorted(SKIP_RELATIONS)
    rel_tokens = load_csv_relation_tokens()
    data["csv_rel"] = rel_tokens

    static_map = {k: v for k, v in imp.ENTITY_LABEL.items()}
    data["inventory_entity_to_neo4j_label"] = static_map
    data["inventory_entity_to_neo4j_label_notes"] = {
        "akteur": "dynamic §6.1",
        "ort": "Land|Stadt",
        "software_digitaltool": "Software|Tool",
        "datenmodell": "no vertex",
        "tooltyp": "no vertex",
    }

    with EXPORT.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    dropped = "(no prior controlled_vocabulary)" if old_cv is None else "replaced verbose controlled_vocabulary"
    print(
        f"Wrote {EXPORT.relative_to(ROOT)}: compact JSON, {len(paths)} paths, "
        f"{len(CONTROLLED_VOCAB_ENTITIES)} entity kinds; {dropped}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
