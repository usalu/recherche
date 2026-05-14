"""Scan `_database/_edges/*.csv` for `relation` columns and map tokens to Neo4j types (plan §7.1).

Writes `_database/_system/RELATION_CATALOG_NEO4J.md` (regenerate after edge CSV changes).

Usage (from repo root):
  python _scripts/extract_database_relations.py
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from neo4j_relation_fold import SKIP_RELATIONS, fold_csv_relation


def _read_edges_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        return [], []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        if "relation" not in fieldnames:
            return fieldnames, []
        rows = list(reader)
    return fieldnames, rows


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    edge_dir = repo / "research" / "_edges"
    out_path = repo / "research" / "_system" / "RELATION_CATALOG_NEO4J.md"

    scan_names = [
        "clean_confirmed_edges.csv",
    ]

    counts: dict[str, Counter[str]] = {}
    example_row: dict[str, dict[str, str]] = {}

    for name in scan_names:
        path = edge_dir / name
        _hdr, rows = _read_edges_csv(path)
        if not rows:
            continue
        c: Counter[str] = Counter()
        for row in rows:
            rel = (row.get("relation") or "").strip()
            if not rel:
                continue
            c[rel] += 1
            if rel not in example_row:
                example_row[rel] = dict(row)
        counts[name] = c

    canonical = "clean_confirmed_edges.csv"
    all_relations = sorted(set(example_row.keys()))

    lines: list[str] = []
    lines.append("# Relation catalogue — `_database/_edges` → Neo4j (plan §7.1)")
    lines.append("")
    lines.append(
        f"Generated **{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}** by "
        "`_scripts/extract_database_relations.py`."
    )
    lines.append("")
    lines.append(
        "Normative folding: `_scripts/neo4j_relation_fold.py` (same logic as "
        "`import_database_folder_to_neo4j.py`). "
        "Rows whose endpoints are skipped by the importer are still listed here for vocabulary completeness."
    )
    lines.append("")
    lines.append("## Files scanned")
    lines.append("")
    for name in scan_names:
        path = edge_dir / name
        n = sum(counts.get(name, Counter()).values()) if name in counts else 0
        lines.append(f"- `{path.relative_to(repo).as_posix()}` — **{n}** rows with a `relation` value")
    lines.append("")
    lines.append(f"## All distinct `relation` values ({len(all_relations)})")
    lines.append("")
    lines.append("| `relation` | rows | Neo4j type | Fold props (audit) |")
    lines.append("| --- | ---: | --- | --- |")
    for rel in all_relations:
        row = example_row[rel]
        neo, extra = fold_csv_relation(row)
        if neo is None:
            neo_disp = "— (no edge)"
            if rel in SKIP_RELATIONS:
                neo_disp = "— (`SKIP_RELATIONS`)"
            extra_disp = ""
        else:
            neo_disp = f"`{neo}`"
            extra_disp = ", ".join(f"`{k}={v}`" for k, v in sorted(extra.items()))
        n_clean = counts.get(canonical, Counter()).get(rel, 0)
        lines.append(f"| `{rel}` | {n_clean} | {neo_disp} | {extra_disp} |")
    lines.append("")
    lines.append("## Importer endpoint skips (not shown per row)")
    lines.append("")
    lines.append(
        "Edges are dropped before folding when `source_entity` / `target_entity` is in "
        "`SKIP_NODE_ENTITIES`, or `datenmodell` / `tooltyp`, or path "
        "`fuegung_verbindung/Reversible_Fuegung` — see `import_database_folder_to_neo4j.py`."
    )
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", out_path.relative_to(repo), "relations", len(all_relations))


if __name__ == "__main__":
    main()
