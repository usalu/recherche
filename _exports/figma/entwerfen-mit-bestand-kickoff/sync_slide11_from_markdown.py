#!/usr/bin/env python3
"""Build Slide 11 pipeline cell payloads from archive markdown split files."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARCHIVE = (
    Path(__file__).resolve().parents[3]
    / "_archive/research/plattform/entwurf/Presenattion/04 - import examples/3_examples_bauteilboerse_split"
)

# Screenshot node IDs: rows × cols (Rippenplatte, Stahlträger, Holzbalken)
CELL_NODES: list[list[str]] = [
    ["377:3209", "377:3210", "377:3211"],  # Input-Typen
    ["377:3212", "377:3213", "377:3214"],  # Raw Extraction
    ["377:3215", "377:3216", "377:3217"],  # Normalisierung
    ["377:3218", "377:3219", "377:3220"],  # Klassifikation
    ["377:3221", "377:3222", "377:3223"],  # Abgeleitete Daten
    ["377:3224", "377:3225", "377:3226"],  # Schema-Mapping
]

ROW_FILES = [
    "01_input-typen.md",
    "02_raw-extraction.md",
    "03_normalisierung.md",
    "04_klassifikation.md",
    "05_abgeleitete-daten.md",
    "06_schema-mapping.md",
]

COL_HEADINGS = [
    "Rippenplatte / Spannbeton",
    "Stahlträger HEB 140",
    "Historische Holzbalken aus Altbausanierung",
]


def extract_yaml_blocks(section_text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"```yaml\n(.*?)```", section_text, re.S)]


def split_columns(md_text: str) -> list[str]:
    body = re.sub(r"^#[^\n]*\n+", "", md_text.strip(), count=1)
    sections = re.split(r"(?:^|\n)## \d+\. ", body)
    sections = [s.strip() for s in sections if s.strip()]
    if len(sections) != 3:
        raise ValueError(f"expected 3 column sections, got {len(sections)} in {md_text[:60]!r}")
    return sections


def column_yaml(section: str, with_subheadings: bool = False) -> str:
    if with_subheadings and "#### " in section:
        out: list[str] = []
        for part in re.split(r"\n#### ", section):
            if not part.strip():
                continue
            heading, _, body = part.partition("\n")
            blocks = extract_yaml_blocks(body)
            if blocks:
                out.append(f"## {heading.strip()}\n\n" + "\n\n".join(blocks))
        if out:
            return "\n\n".join(out)
    blocks = extract_yaml_blocks(section)
    if not blocks:
        raise ValueError(f"no yaml blocks in section starting: {section[:80]!r}")
    return "\n\n".join(blocks)


def build_cells() -> list[dict]:
    cells: list[dict] = []
    for row_idx, fname in enumerate(ROW_FILES):
        md = (ARCHIVE / fname).read_text(encoding="utf-8")
        cols = split_columns(md)
        for col_idx, section in enumerate(cols):
            with_heads = fname.startswith("06_")
            cells.append(
                {
                    "row": row_idx,
                    "col": col_idx,
                    "rowLabel": ROW_FILES[row_idx].replace(".md", "").split("_", 1)[1],
                    "columnHeading": COL_HEADINGS[col_idx],
                    "nodeId": CELL_NODES[row_idx][col_idx],
                    "yaml": column_yaml(section, with_subheadings=with_heads),
                }
            )
    return cells


def main() -> None:
    cells = build_cells()
    out = ROOT / "slide11_pipeline_cells.json"
    out.write_text(json.dumps(cells, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(cells)} cells -> {out}")


if __name__ == "__main__":
    main()
