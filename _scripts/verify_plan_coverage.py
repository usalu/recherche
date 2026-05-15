"""LEGACY REVIEW REQUIRED.

Read-only checks for the retired folder-first workflow (`research/` inventory + edge fold).

Exit 0 if all checks pass; prints issues and exits 1 otherwise.

Usage (repo root):
  python _scripts/verify_plan_coverage.py

Neo4j is now the source of truth. Keep this only for controlled legacy review;
do not treat a passing result here as current graph authority.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import import_database_folder_to_neo4j as imp  # noqa: E402
from neo4j_relation_fold import SKIP_RELATIONS, fold_csv_relation  # noqa: E402


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    inv_path = root / "research" / "_system" / "node_inventory.csv"
    edge_path = root / "research" / "_edges" / "clean_confirmed_edges.csv"
    errs: list[str] = []

    allowed = (
        set(imp.ENTITY_LABEL)
        | {"ort", "akteur", "software_digitaltool", "datenmodell", "tooltyp"}
        | imp.SKIP_NODE_ENTITIES
    )
    inv_entities: set[str] = set()
    with inv_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            inv_entities.add(row["entity"])
    unknown = sorted(inv_entities - allowed)
    if unknown:
        errs.append(f"node_inventory.csv has entities not allowed by importer: {unknown}")

    bad_fold: list[str] = []
    with edge_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rel = (row.get("relation") or "").strip()
            if not rel:
                continue
            neo, _ = fold_csv_relation(row)
            if neo is None and rel not in SKIP_RELATIONS:
                bad_fold.append(rel)
    if bad_fold:
        from collections import Counter

        c = Counter(bad_fold)
        errs.append(f"CSV relations that fold to skip but are not in SKIP_RELATIONS: {dict(c)}")

    if errs:
        print("verify_plan_coverage: FAILED", file=sys.stderr)
        for e in errs:
            print(" ", e, file=sys.stderr)
        return 1
    print(
        "verify_plan_coverage: OK -",
        len(inv_entities),
        "inventory entities,",
        "edge file clean_confirmed_edges.csv relation tokens all mapped (IST/HAT/... or explicit SKIP).",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
