#!/usr/bin/env python3
"""
40_apply_edge_remap.py - Edge remap engine for the canonical-schema cleanup.

Reads:  _database/_edges/clean_confirmed_edges.csv (UTF-8 BOM allowed)
Writes: _database/_edges/clean_confirmed_edges.csv (UTF-8 no BOM)
        _migration/40_remap_diff_<batch>.csv (diff report per run)

Each batch is a function below. Add a batch by writing a function that
takes a row dict and returns either the same dict (no change) or a
modified dict; then add it to BATCHES.

Convention: a batch should
  - bump confidence to 'manual_high' when the fix is mechanically certain,
  - rewrite resolution_rule to 'manual_<batch_name>',
  - leave raw_label unchanged so audit trail is preserved.
"""

from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDGES = ROOT / "_database" / "_edges" / "clean_confirmed_edges.csv"
DIFF_DIR = ROOT / "_migration"

EDGE_COLUMNS = [
    "source", "source_entity", "source_id",
    "relation", "target", "target_entity", "target_id",
    "field", "raw_label", "confidence", "resolution_rule",
    "legacy_path", "original_source", "original_relation", "original_target",
    "edge_cleaning",
]


# ---------------------------------------------------------------------------
# Batch 40a: rule_low Stahlbeton-flavored labels routed to material/Stahl
# ---------------------------------------------------------------------------

STAHLBETON_TOKENS = (
    "stahlbeton", "spannbeton", "fertigbeton", "stahlbetonfertigteil",
    "stahlbetonplatte", "ortbeton",
)


def is_stahlbeton_label(raw: str) -> bool:
    rl = raw.lower()
    return any(tok in rl for tok in STAHLBETON_TOKENS)


def batch_40a_stahlbeton_remap(row: dict) -> dict | None:
    """Re-route rule_low uses_material edges with Stahlbeton-flavored labels
    from material/Stahl -> material/Stahlbeton."""
    if row["confidence"] != "rule_low":
        return None
    if row["relation"] != "uses_material":
        return None
    if row["target"] != "material/Stahl":
        return None
    if not is_stahlbeton_label(row["raw_label"]):
        return None
    new = dict(row)
    new["target"] = "material/Stahlbeton"
    new["target_entity"] = "material"
    new["target_id"] = "Stahlbeton"
    new["confidence"] = "manual_high"
    new["resolution_rule"] = "manual_40a_stahlbeton_substring_fix"
    new["edge_cleaning"] = "manual_remap_40a"
    return new


# ---------------------------------------------------------------------------
# Batch 40b: bauteiltyp consolidation (schema §5 mechanical part)
# ---------------------------------------------------------------------------

BAUTEILTYP_MAP = {
    # renames (folder also renamed in a separate folder-cleanup phase)
    "bauteiltyp/Innenausbau":            "bauteiltyp/Ausbau",
    "bauteiltyp/Technik_TGA":            "bauteiltyp/Technik",
    # merges into Ausbau
    "bauteiltyp/Festes_Einbauteil":      "bauteiltyp/Ausbau",
    "bauteiltyp/Akustikelement":         "bauteiltyp/Ausbau",
    # merges into Technik
    "bauteiltyp/Sanitaerobjekt":         "bauteiltyp/Technik",
    "bauteiltyp/Leuchte":                "bauteiltyp/Technik",
    "bauteiltyp/PV_Anlage":              "bauteiltyp/Technik",
    # other mechanical merges
    "bauteiltyp/Gitterrost":             "bauteiltyp/Boden",
    "bauteiltyp/Beschattung_Sonnenschutz": "bauteiltyp/Fassade",
}


def batch_40b_bauteiltyp_consolidation(row: dict) -> dict | None:
    if row["target"] not in BAUTEILTYP_MAP:
        return None
    new_target = BAUTEILTYP_MAP[row["target"]]
    new = dict(row)
    new["target"] = new_target
    _, new_id = new_target.split("/", 1)
    new["target_id"] = new_id
    new["resolution_rule"] = f"manual_40b_consolidate_{row['target_id']}"
    new["edge_cleaning"] = "manual_remap_40b"
    # confidence policy: only bump if it was a low/medium auto-rule
    if row["confidence"] in ("rule_low", "rule_medium"):
        new["confidence"] = "manual_high"
    return new


# ---------------------------------------------------------------------------
# Batch 40c: material consolidation (schema §6 mechanical part)
# ---------------------------------------------------------------------------

MATERIAL_MAP = {
    "material/Brettschichtholz": "material/Holz",
    "material/Brettsperrholz":   "material/Holz",
    "material/Sekundaerstahl":   "material/Stahl",
    "material/Mineralwolle":     "material/Daemmstoff",
    "material/Polystyrol":       "material/Daemmstoff",
    "material/Sanitarkeramik":   "material/Keramik",
    "material/Granit":           "material/Naturstein",
    "material/Marmor":           "material/Naturstein",
    "material/Faserzement":      "material/Beton",
}


def batch_40c_material_consolidation(row: dict) -> dict | None:
    if row["target"] not in MATERIAL_MAP:
        return None
    new_target = MATERIAL_MAP[row["target"]]
    new = dict(row)
    new["target"] = new_target
    _, new_id = new_target.split("/", 1)
    new["target_id"] = new_id
    new["resolution_rule"] = f"manual_40c_consolidate_{row['target_id']}"
    new["edge_cleaning"] = "manual_remap_40c"
    if row["confidence"] in ("rule_low", "rule_medium"):
        new["confidence"] = "manual_high"
    return new


# ---------------------------------------------------------------------------
# Post-batch dedup
# ---------------------------------------------------------------------------

def dedup(rows: list[dict]) -> tuple[list[dict], int]:
    """Drop exact (source, relation, target) duplicates that may arise after
    merges. Keep the row with the strongest confidence; otherwise the first."""
    confidence_rank = {
        "exact": 5, "manual_high": 4, "structural": 3,
        "rule_high": 2, "manual_split": 2,
        "rule_medium": 1, "rule_low": 0,
    }
    keep: dict[tuple, dict] = {}
    for row in rows:
        key = (row["source"], row["relation"], row["target"])
        if key not in keep:
            keep[key] = row
        else:
            existing = keep[key]
            if confidence_rank.get(row["confidence"], 0) > confidence_rank.get(existing["confidence"], 0):
                keep[key] = row
    out = list(keep.values())
    return out, len(rows) - len(out)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

BATCHES = {
    "40a_stahlbeton": batch_40a_stahlbeton_remap,
    "40b_bauteiltyp": batch_40b_bauteiltyp_consolidation,
    "40c_material":   batch_40c_material_consolidation,
}


def load_rows() -> list[dict]:
    with EDGES.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return rows


def write_rows(rows: list[dict]) -> None:
    # UTF-8 without BOM, LF line endings, all values quoted (matches existing format)
    tmp = EDGES.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=EDGE_COLUMNS,
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in EDGE_COLUMNS})
    tmp.replace(EDGES)


def write_diff(batch_name: str, changes: list[tuple[dict, dict]]) -> Path:
    diff_path = DIFF_DIR / f"40_remap_diff_{batch_name}.csv"
    with diff_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writerow([
            "source", "relation",
            "old_target", "new_target",
            "raw_label", "old_confidence", "new_confidence",
            "old_resolution_rule", "new_resolution_rule",
        ])
        for old, new in changes:
            writer.writerow([
                old["source"], old["relation"],
                old["target"], new["target"],
                old["raw_label"], old["confidence"], new["confidence"],
                old["resolution_rule"], new["resolution_rule"],
            ])
    return diff_path


def run_batch(batch_name: str, batch_fn, rows: list[dict]) -> tuple[list[dict], list[tuple[dict, dict]]]:
    changes = []
    out = []
    for row in rows:
        new = batch_fn(row)
        if new is None:
            out.append(row)
        else:
            changes.append((row, new))
            out.append(new)
    return out, changes


def main(argv: list[str]) -> int:
    selected = argv[1:] or list(BATCHES.keys())
    unknown = [b for b in selected if b not in BATCHES]
    if unknown:
        print(f"Unknown batches: {unknown}", file=sys.stderr)
        print(f"Available: {list(BATCHES.keys())}", file=sys.stderr)
        return 2

    rows = load_rows()
    print(f"Loaded {len(rows)} edges from {EDGES.relative_to(ROOT)}")

    total_changes = 0
    for batch_name in selected:
        rows, changes = run_batch(batch_name, BATCHES[batch_name], rows)
        diff = write_diff(batch_name, changes)
        print(f"  Batch {batch_name}: {len(changes)} edges remapped")
        print(f"    Diff written to {diff.relative_to(ROOT)}")
        total_changes += len(changes)

    if total_changes == 0:
        print("No changes; not rewriting the edge file.")
        return 0

    # Dedup post-merge
    rows, dropped = dedup(rows)
    if dropped:
        print(f"  Deduped {dropped} duplicate edges created by merges")

    # Backup before write
    backup = EDGES.with_suffix(".csv.before_40")
    if not backup.exists():
        shutil.copy2(EDGES, backup)
        print(f"  Backup: {backup.relative_to(ROOT)}")

    write_rows(rows)
    print(f"  Wrote {len(rows)} edges back to {EDGES.relative_to(ROOT)} (UTF-8, no BOM)")
    print(f"  Total changes: {total_changes}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
