#!/usr/bin/env python3
"""
41_apply_folder_cleanup.py - Folder-cleanup engine for canonical-schema migration.

Companion to 40_apply_edge_remap.py:
  - 40 rewrites EDGES so they point at canonical targets.
  - 41 renames + archives FOLDERS so node_inventory matches.

Then the SQLite rebuild is consistent.

Reads:  _database/<entity>/<old_id>/
Writes: _database/<entity>/<new_id>/      (rename)
        _archive/dropped_knots/<entity>/<old_id>/   (archive of dropped)
        _database/_system/node_inventory.csv  (regenerated)
"""

from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATABASE = ROOT / "_database"
ARCHIVE = ROOT / "_archive" / "dropped_knots"
INVENTORY = DATABASE / "_system" / "node_inventory.csv"

# (entity, old_id, new_id_or_None)
# new_id = None means: archive this folder (no surviving target in same entity).
# new_id = "X" means: rename folder old_id -> X. If X already exists (a merge),
#         move the dropped folder into _archive then nothing more is needed
#         because the surviving folder already exists.

FOLDER_OPS = [
    # Bauteiltyp consolidation (matches batch_40b)
    ("bauteiltyp", "Innenausbau",            "Ausbau"),    # rename
    ("bauteiltyp", "Technik_TGA",            "Technik"),   # rename
    ("bauteiltyp", "Festes_Einbauteil",      "Ausbau"),    # merge -> archive source
    ("bauteiltyp", "Akustikelement",         "Ausbau"),
    ("bauteiltyp", "Sanitaerobjekt",         "Technik"),
    ("bauteiltyp", "Leuchte",                "Technik"),
    ("bauteiltyp", "PV_Anlage",              "Technik"),
    ("bauteiltyp", "Gitterrost",             "Boden"),
    ("bauteiltyp", "Beschattung_Sonnenschutz","Fassade"),
    # Material consolidation (matches batch_40c)
    ("material", "Brettschichtholz", "Holz"),
    ("material", "Brettsperrholz",   "Holz"),
    ("material", "Sekundaerstahl",   "Stahl"),
    ("material", "Mineralwolle",     "Daemmstoff"),
    ("material", "Polystyrol",       "Daemmstoff"),
    ("material", "Sanitarkeramik",   "Keramik"),
    ("material", "Granit",           "Naturstein"),
    ("material", "Marmor",           "Naturstein"),
    ("material", "Faserzement",      "Beton"),
]


def parse_frontmatter(markdown: str) -> dict[str, str]:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def regenerate_inventory() -> None:
    """Walk _database/<entity>/<id>/index.md and rebuild node_inventory.csv."""
    rows: list[dict] = []
    for entity_dir in sorted(DATABASE.iterdir()):
        if not entity_dir.is_dir() or entity_dir.name.startswith("_"):
            continue
        entity = entity_dir.name
        for node_dir in sorted(entity_dir.iterdir()):
            if not node_dir.is_dir():
                continue
            node_id = node_dir.name
            index_md = node_dir / "index.md"
            if not index_md.exists():
                continue
            fm = parse_frontmatter(index_md.read_text(encoding="utf-8"))
            dateien_dir = node_dir / "DATEIEN"
            dateien_count = 0
            if dateien_dir.exists():
                dateien_count = sum(1 for _ in dateien_dir.iterdir() if _.is_file())
            rows.append({
                "entity": entity,
                "id": node_id,
                "typed_path": f"{entity}/{node_id}",
                "title": fm.get("title", node_id),
                "build_status": fm.get("build_status", "clean_phase20"),
                "markdown_path": f"_database/{entity}/{node_id}/index.md",
                "dateien_file_count": str(dateien_count),
                "imported_source_count": str(dateien_count),
            })

    fields = list(rows[0].keys())
    with INVENTORY.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"  Inventory regenerated: {len(rows)} nodes")


def apply_folder_ops() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for entity, old_id, new_id in FOLDER_OPS:
        src = DATABASE / entity / old_id
        if not src.exists():
            print(f"  SKIP missing: {entity}/{old_id}")
            continue
        target = DATABASE / entity / new_id
        if not target.exists():
            # Pure rename
            src.rename(target)
            print(f"  RENAME {entity}/{old_id} -> {entity}/{new_id}")
        else:
            # Merge: target exists, archive source for provenance
            archive_dest = ARCHIVE / entity / old_id
            if archive_dest.exists():
                shutil.rmtree(archive_dest)
            archive_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(archive_dest))
            print(f"  ARCHIVE {entity}/{old_id} (merged into {entity}/{new_id})")


def main() -> int:
    print("Applying folder operations:")
    apply_folder_ops()
    print()
    print("Regenerating node inventory:")
    regenerate_inventory()
    print()
    print("Done. Run python _migration/build_phase24_sqlite_database.py to rebuild SQLite.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
