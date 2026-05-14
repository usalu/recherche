#!/usr/bin/env python3
"""
43_apply_manual_review_decisions.py - apply schema decisions for the 27
manual-review nodes by processing the 228 held-back edges.

Reads:
  _database/_edges/clean_edge_review_queue.csv
  _database/_edges/clean_confirmed_edges.csv

Decisions per schema §5/§6 + worksheet recommendations:
  - delete_from_final: drop the edge entirely
  - move (single target): rewrite target, promote to confirmed
  - split per case: dispatch via raw_label heuristics; promote to confirmed
  - create new node: promote node folder from _manual_review or stub-create,
    then promote edge to confirmed
  - keep_review: leave in queue (case needs human eyes)

Writes:
  _database/_edges/clean_confirmed_edges.csv (with promoted edges appended)
  _database/_edges/clean_edge_review_queue.csv (with applied rows removed)
  _migration/43_decision_log.csv (full audit trail)
  _database/<entity>/<new_id>/ (any newly created/promoted node folders)
"""

from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATABASE = ROOT / "_database"
MANUAL = ROOT / "_manual_review" / "nodes"
CONFIRMED = DATABASE / "_edges" / "clean_confirmed_edges.csv"
QUEUE = DATABASE / "_edges" / "clean_edge_review_queue.csv"
LOG = ROOT / "_migration" / "43_decision_log.csv"

CONFIRMED_COLUMNS = [
    "source", "source_entity", "source_id",
    "relation", "target", "target_entity", "target_id",
    "field", "raw_label", "confidence", "resolution_rule",
    "legacy_path", "original_source", "original_relation", "original_target",
    "edge_cleaning",
]


# ---------------------------------------------------------------------------
# Per-target decisions (matches schema §5/§6 + worksheet recommendations)
# ---------------------------------------------------------------------------

# Hard drops: target is dropped from the ontology entirely
DELETE_TARGETS = {
    "material/Metall",
    "bauteiltyp/Bauwerksteil",
    "bauteiltyp/Landschaftselement",
}

# Single-target moves
MOVE_TARGETS = {
    "bauteiltyp/Kueche":         "bauteiltyp/Ausbau",
    "bauteiltyp/Treppenwange":   "bauteiltyp/Treppe",
    "bauteiltyp/Feuerschutztuer":"bauteiltyp/Tuer",
    "material/Erde":             "material/Lehm",
    "material/Guss":             "material/Gusseisen",   # creates folder
    "material/Recyclingbeton":   "material/Recyclingbeton",  # creates folder (promote from manual_review)
}

# Targets needing per-case dispatch via raw_label heuristics
SPLIT_TARGETS = {
    "bauteiltyp/Tragstruktur",
    "bauteiltyp/Performance_Nachweis",  # safety: not actually a bauteiltyp
    "huerde/Performance_Nachweis",
    "huerde/Logistikproblem",
    "bauteiltyp/Fliese",
    "bauteiltyp/Kern",
    "bauteiltyp/Bruestung",
    "bauteiltyp/Auflager_Widerlager",
    "bauteiltyp/Dachziegel",
}


def dispatch_split(target: str, raw_label: str) -> str | None:
    lo = raw_label.lower()
    if target == "huerde/Logistikproblem":
        if "lager" in lo or "depot" in lo or "platz" in lo: return "huerde/Fehlende_Lagerflaeche"
        if "verfügbar" in lo or "verfuegbar" in lo or "available" in lo: return "huerde/Verfuegbarkeitsproblem"
        if "termin" in lo or "zeit" in lo: return "huerde/Terminunsicherheit"
        if "transport" in lo: return "huerde/Verfuegbarkeitsproblem"  # closest existing
        return "huerde/Verfuegbarkeitsproblem"  # default for logistics issues
    if target == "huerde/Performance_Nachweis":
        if "nachweis" in lo or "norm" in lo or "zertif" in lo: return "huerde/Technische_Freigabe"
        if "daten" in lo or "fehlen" in lo or "unbekannt" in lo: return "huerde/Datenluecke"
        if "qualit" in lo or "zustand" in lo: return "huerde/Materialqualitaet_Unklar"
        return "huerde/Technische_Freigabe"  # default
    if target == "bauteiltyp/Tragstruktur":
        if "stahl" in lo: return "tragwerkstyp/Stahltragwerk"
        if "holz" in lo: return "tragwerkstyp/Holztragwerk"
        if "beton" in lo: return "tragwerkstyp/Betontragwerk"
        if "tragwerk" in lo or "structure" in lo: return "tragwerkstyp/Stahltragwerk"  # default
        return "bauteiltyp/Traeger"  # if it's a single tragend element
    if target == "bauteiltyp/Fliese":
        if "boden" in lo or "floor" in lo or "pflaster" in lo: return "bauteiltyp/Boden"
        if "dach" in lo or "roof" in lo: return "bauteiltyp/Dach"
        if "wand" in lo or "wall" in lo: return "bauteiltyp/Wand"
        return "bauteiltyp/Wand"  # default
    if target == "bauteiltyp/Kern":
        if "wand" in lo: return "bauteiltyp/Wand"
        if "tragwerk" in lo or "structural" in lo: return "tragwerksprinzip/Skeletttragwerk"
        return "bauteiltyp/Wand"
    if target == "bauteiltyp/Bruestung":
        if "fassade" in lo or "facade" in lo: return "bauteiltyp/Fassade"
        return "bauteiltyp/Gelaender"
    if target == "bauteiltyp/Auflager_Widerlager":
        if "fundament" in lo or "foundation" in lo or "widerlager" in lo: return "bauteiltyp/Fundament"
        return "bauteiltyp/Fundament"
    if target == "bauteiltyp/Dachziegel":
        return "bauteiltyp/Dach"
    return None


# ---------------------------------------------------------------------------
# Node folder management
# ---------------------------------------------------------------------------

def ensure_node_folder(typed_path: str) -> bool:
    """Ensure _database/<entity>/<id>/ exists. Returns True if created/promoted."""
    entity, node_id = typed_path.split("/", 1)
    target_dir = DATABASE / entity / node_id
    if target_dir.exists():
        return False
    # Try promoting from _manual_review
    manual_src = MANUAL / entity / node_id
    if manual_src.exists():
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(manual_src), str(target_dir))
        # Re-promote prose if a staging file exists
        return True
    # Create stub
    target_dir.mkdir(parents=True)
    (target_dir / "DATEIEN").mkdir()
    (target_dir / "index.md").write_text(
        f"---\nentity: \"{entity}\"\nid: \"{node_id}\"\ntitle: \"{node_id.replace('_', ' ')}\"\n"
        f"build_status: \"stub_phase43\"\n---\n\n"
        f"# {node_id.replace('_', ' ')}\n\n"
        f"_Canonical knot created during manual-review application._\n",
        encoding="utf-8", newline="\n",
    )
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    confirmed_existing: list[dict] = []
    with CONFIRMED.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            confirmed_existing.append(row)

    queue: list[dict] = []
    with QUEUE.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            queue.append(row)

    decisions: list[dict] = []
    new_confirmed: list[dict] = []
    new_queue: list[dict] = []
    folders_created: set[str] = set()

    for row in queue:
        target = row["target"]
        source = row["source"]
        reason = row["review_reason"]
        decision = "keep_review"
        new_target = ""
        note = ""

        # Pseudo-node placeholders
        if "/index" in source or "/index" in target:
            decision = "delete"
            note = "pseudo-node placeholder"

        # source_manual_review: the 2 misclassified datenpunkts
        elif reason == "source_manual_review":
            decision = "delete"
            note = "duplicate of canonical reuse_einsatz; original case data lives there"

        # Hard drops
        elif target in DELETE_TARGETS:
            decision = "delete"
            note = f"target {target} dropped per schema"

        # Single-target moves
        elif target in MOVE_TARGETS:
            new_target = MOVE_TARGETS[target]
            if ensure_node_folder(new_target):
                folders_created.add(new_target)
            decision = "move"

        # Per-case splits
        elif target in SPLIT_TARGETS:
            new_target = dispatch_split(target, row.get("raw_label", ""))
            if new_target:
                if ensure_node_folder(new_target):
                    folders_created.add(new_target)
                decision = "split"
            else:
                decision = "keep_review"
                note = "no dispatcher rule matched"

        # Anything else: keep in review
        else:
            decision = "keep_review"
            note = f"no rule for target {target}"

        decisions.append({
            "source": source,
            "relation": row["relation"],
            "old_target": target,
            "new_target": new_target,
            "decision": decision,
            "raw_label": row.get("raw_label", ""),
            "note": note,
        })

        if decision in ("move", "split"):
            new_ent, new_id = new_target.split("/", 1)
            src_ent, _, src_id = source.partition("/")
            new_row = {
                "source": source,
                "source_entity": src_ent,
                "source_id": src_id,
                "relation": row["relation"],
                "target": new_target,
                "target_entity": new_ent,
                "target_id": new_id,
                "field": row.get("field", ""),
                "raw_label": row.get("raw_label", ""),
                "confidence": "manual_high",
                "resolution_rule": f"manual_43_{decision}_{target.split('/')[-1]}",
                "legacy_path": row.get("legacy_path", ""),
                "original_source": source,
                "original_relation": row["relation"],
                "original_target": target,
                "edge_cleaning": "manual_remap_43",
            }
            new_confirmed.append(new_row)
        elif decision == "keep_review":
            new_queue.append(row)
        # delete: drop entirely

    # Dedup confirmed (some splits may collide with existing edges)
    seen = set()
    final_confirmed = []
    for row in confirmed_existing + new_confirmed:
        key = (row["source"], row["relation"], row["target"])
        if key in seen:
            continue
        seen.add(key)
        final_confirmed.append(row)

    # Backup
    bak = CONFIRMED.with_suffix(".csv.before_43")
    if not bak.exists():
        shutil.copy2(CONFIRMED, bak)

    # Write new confirmed
    with CONFIRMED.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CONFIRMED_COLUMNS, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        for row in final_confirmed:
            writer.writerow({k: row.get(k, "") for k in CONFIRMED_COLUMNS})

    # Write new queue
    queue_columns = list(queue[0].keys()) if queue else []
    with QUEUE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=queue_columns, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        for row in new_queue:
            writer.writerow(row)

    # Write decision log
    with LOG.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["source","relation","old_target","new_target","decision","raw_label","note"],
            quoting=csv.QUOTE_ALL, lineterminator="\n",
        )
        writer.writeheader()
        for row in decisions:
            writer.writerow(row)

    # Summary
    from collections import Counter
    by_decision = Counter(d["decision"] for d in decisions)
    print(f"Held-back edges processed: {len(decisions)}")
    for k, n in by_decision.most_common():
        print(f"  {k:<15} {n}")
    print(f"Edges promoted to confirmed: {len(new_confirmed)}")
    print(f"Edges remaining in queue:    {len(new_queue)}")
    print(f"Final confirmed edges:       {len(final_confirmed)}")
    print(f"New canonical folders created/promoted: {len(folders_created)}")
    for f in sorted(folders_created):
        print(f"  + {f}")
    print(f"Decision log: {LOG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
