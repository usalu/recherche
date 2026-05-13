#!/usr/bin/env python3
"""Export all clean_confirmed_edges rows touching a case id substring (inventory-driven).

Example:
  python _scripts/export_case_edge_slice.py K118_Kopfbau_Halle_118_Winterthur
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "_database" / "_system" / "node_inventory.csv"
EDGES = ROOT / "_database" / "_edges" / "clean_confirmed_edges.csv"
OUT_DIR = ROOT / "_migration"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("case_substring", help="Substring of typed_path, e.g. K118_Kopfbau_Halle_118_Winterthur")
    ap.add_argument("--slug", default="", help="Output file slug (default: case_substring)")
    args = ap.parse_args()
    case = args.case_substring.strip()
    if not case:
        print("empty case_substring", file=sys.stderr)
        return 2
    slug = (args.slug or case).replace("/", "_")
    out_md = OUT_DIR / f"case_{slug}_REPORT.md"
    out_tsv = OUT_DIR / f"case_{slug}_edges.tsv"

    nodes_by_entity: dict[str, list[tuple[str, str]]] = defaultdict(list)
    nodes: set[str] = set()
    with INV.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            tp = (row.get("typed_path") or "").strip()
            if case in tp:
                nodes.add(tp)
                nodes_by_entity[row.get("entity", "")].append((tp, (row.get("title") or "")[:100]))

    edge_rows: list[dict[str, str]] = []
    fieldnames: list[str] = []
    with EDGES.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        for row in reader:
            s = (row.get("source") or "").strip()
            t = (row.get("target") or "").strip()
            if s in nodes or t in nodes:
                edge_rows.append(row)

    ct = Counter(r.get("relation", "") for r in edge_rows)
    both_ends = sum(1 for r in edge_rows if r.get("source", "") in nodes and r.get("target", "") in nodes)
    anchors = [
        tp for tp in sorted(nodes)
        if tp.startswith(("fallstudie/", "projekt/", "bauobjekt/")) and tp.endswith(case)
    ]

    lines: list[str] = []
    lines.append(f"# Case graph extract: `{case}`\n\n")
    lines.append(
        "**Scope:** Every `typed_path` in `node_inventory.csv` that contains this substring, "
        "plus every row in `clean_confirmed_edges.csv` where **source** or **target** is in that node set.\n\n"
    )
    lines.append("**Primary Fallbeispiel / Projekt / Bauwerk anchors (inventory):**\n\n")
    for a in anchors:
        lines.append(f"- `{a}`\n")
    if not anchors:
        lines.append("- _(none matching fallstudie|projekt|bauobjekt + exact id suffix — check substring)_\n")
    lines.append("\n## Counts\n\n")
    lines.append("| Metric | Value |\n|---:|---:|\n")
    lines.append(f"| Case-related inventory nodes | {len(nodes)} |\n")
    lines.append(f"| CSV edges (at least one endpoint in scope) | {len(edge_rows)} |\n")
    lines.append(f"| CSV edges (both endpoints in scope) | {both_ends} |\n")
    lines.append(f"| Distinct `relation` in this slice | {len(ct)} |\n")
    lines.append("\n## Edges by `relation`\n\n")
    lines.append("| Count | relation |\n|---:|---|\n")
    for rel, c in ct.most_common():
        lines.append(f"| {c} | `{rel}` |\n")

    lines.append("\n## Inventory nodes by `entity`\n\n")
    for ent in sorted(nodes_by_entity.keys()):
        rows_ent = sorted(nodes_by_entity[ent])
        lines.append(f"### `{ent}` ({len(rows_ent)})\n\n")
        for tp, title in rows_ent:
            lines.append(f"- `{tp}` — {title}\n")
        lines.append("\n")

    rel_name = out_tsv.name
    lines.append("## Machine-readable edge list\n\n")
    lines.append(
        f"TSV ({len(edge_rows)} rows, same columns as `clean_confirmed_edges.csv`): [`{rel_name}`]({rel_name})\n\n"
    )
    lines.append(
        "## Neo4j note\n\n"
        "After import, predicates are **folded** (e.g. `belongs_to_fallstudie` → `GEHÖRT_ZU`, "
        "`has_logistik` → `HAT` with `art=logistik`, `uses_material` → `BENUTZT`). "
        "Use this CSV slice for **predicate-level** comparison to another document; use Browser for **folded** shape.\n"
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_md.write_text("".join(lines), encoding="utf-8")
    with out_tsv.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=fieldnames)
        w.writeheader()
        for row in edge_rows:
            w.writerow(row)

    print(f"Wrote {out_md.relative_to(ROOT)}")
    print(f"Wrote {out_tsv.relative_to(ROOT)}")
    print(f"nodes={len(nodes)} edges={len(edge_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
