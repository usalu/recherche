#!/usr/bin/env python3
"""
Automated slice of EDGE_QUALITY_AUDIT.md §3: stratified sample + file/trace checks.

Usage (repo root):
  python _scripts/run_edge_quality_trace.py
  python _scripts/run_edge_quality_trace.py --out _migration/edge_quality_trace_report.md
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EDGES = ROOT / "_database" / "_edges" / "clean_confirmed_edges.csv"


def norm(s: str) -> str:
    s = s or ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.casefold()


def typed_path_to_index(typed_path: str) -> Path:
    if "/" not in typed_path:
        raise ValueError(f"Bad typed_path: {typed_path!r}")
    ent, rest = typed_path.split("/", 1)
    return ROOT / "_database" / ent / rest / "index.md"


def raw_label_evidence(raw: str, body: str) -> tuple[bool, str]:
    """Heuristic: long token from raw_label appears in body (both normalized)."""
    raw_n, body_n = norm(raw), norm(body)
    if not raw.strip():
        return False, "empty_raw_label"
    if len(raw_n) >= 8 and raw_n in body_n:
        return True, "substring_match"
    tokens = re.split(r"[^\wäöüß]+", raw, flags=re.IGNORECASE)
    for t in tokens:
        t = t.strip()
        if len(t) >= 6 and norm(t) in body_n:
            return True, f"token:{t[:40]}"
    return False, "no_token_match_6chars"


def pick_first(rows: list[dict], relation: str, n: int) -> list[dict]:
    out = []
    for row in rows:
        if row.get("relation") == relation:
            out.append(row)
            if len(out) >= n:
                break
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "_migration" / "edge_quality_trace_report.md")
    args = ap.parse_args()

    if not EDGES.is_file():
        print(f"Missing {EDGES}", file=sys.stderr)
        return 1

    with EDGES.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    # Twelve core rows (audit doc): structural + heavy + metrics; new types appended.
    sample: list[tuple[str, dict]] = []
    for rel in (
        "belongs_to_fallstudie",
        "installed_in_bauobjekt",
        "has_huerde",
        "has_rechtliche_bedingung",
        "has_logistik",
        "measured_on_bauobjekt",
    ):
        for row in pick_first(rows, rel, 2):
            sample.append((rel, row))
    for row in pick_first(rows, "measures_kennwertdefinition", 2):
        sample.append(("measures_kennwertdefinition", row))
    for row in pick_first(rows, "has_ressourcenquelle", 2):
        sample.append(("has_ressourcenquelle", row))
    for row in pick_first(rows, "has_methode", 2):
        sample.append(("has_methode", row))

    lines: list[str] = []
    lines.append("# Edge quality trace — automated run\n")
    lines.append(f"- Edges file: `{EDGES.relative_to(ROOT).as_posix()}`\n")
    lines.append(f"- Sample size: **{len(sample)}** rows\n")
    lines.append("\n## Per-row checks\n")
    lines.append("\n| # | relation | source_exists | target_exists | raw_in_source | note |\n")
    lines.append("|---:|---|:---:|:---:|:---:|---|\n")

    sys.path.insert(0, str(ROOT / "_scripts"))
    from neo4j_relation_fold import SKIP_RELATIONS, fold_csv_relation  # noqa: E402

    greens = 0
    for i, (band_rel, row) in enumerate(sample, 1):
        src_tp = (row.get("source") or "").strip()
        tgt_tp = (row.get("target") or "").strip()
        raw = (row.get("raw_label") or "").strip()
        field = (row.get("field") or "").strip()
        rel = (row.get("relation") or "").strip()

        src_path = typed_path_to_index(src_tp)
        tgt_path = typed_path_to_index(tgt_tp)
        se = src_path.is_file()
        te = tgt_path.is_file()

        ev_ok, ev_note = False, "n/a"
        if se:
            body = src_path.read_text(encoding="utf-8", errors="replace")
            ev_ok, ev_note = raw_label_evidence(raw, body)

        neo, fold_props = fold_csv_relation(row)
        if rel in SKIP_RELATIONS:
            fold_ok = True
            fold_note = "Neo4j_SKIP(intended)"
        else:
            fold_ok = neo is not None
            fold_note = neo or "SKIP(unexpected)"
        if fold_props:
            fold_note += f" {fold_props}"

        green = se and te and ev_ok and fold_ok
        if green:
            greens += 1

        lines.append(
            f"| {i} | `{row.get('relation','')}` | {'Y' if se else '**N**'} | "
            f"{'Y' if te else '**N**'} | {'Y' if ev_ok else '**N**'} | "
            f"{ev_note}; {fold_note}; field=`{field[:40]}` |\n"
        )

    lines.append("\n## Summary\n\n")
    lines.append(
        f"- **Green count** (source `index.md` exists, target `index.md` exists, "
        f"raw-label heuristic found in source body, Neo4j fold OK or intentional SKIP): **{greens} / {len(sample)}**\n"
    )
    lines.append("- Rule of thumb from audit doc: **≥9/12** green → keep and extend; this run uses a slightly larger sample.\n")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {args.out.relative_to(ROOT)}")
    print(f"Green {greens}/{len(sample)}")
    threshold = max(9, int(len(sample) * 0.5) + 1)
    if greens < threshold:
        print(f"WARN: green count below soft threshold ({threshold})", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
