#!/usr/bin/env python3
"""
42_promote_prose_to_index.py - Option A: lift staging prose into index.md.

For each _database/<entity>/<id>/, replace the 20-line stub index.md with
the rich German prose currently sitting in DATEIEN/*.staging_index.md.

Rules:
  - Frontmatter: clean canonical (entity, id, title, build_status) plus
    selected provenance (legacy_type, legacy_paths, source_table).
  - Body: staging_index.md body, with migration boilerplate sections
    stripped (## Migration, ## Clean Node, ## Imported Staging Nodes).
  - Multiple staging files: concatenated, each preceded by "## Quelle: <name>".
  - Legacy-only DATEIEN (quelle/* nodes): treat the legacy file as the body.
  - Encoding: UTF-8 without BOM, LF line endings.
  - Backup: DATEIEN/*.staging_index.md is kept as-is (provenance untouched).

Idempotent: reading the new index.md back produces the same output, so
re-running on already-promoted nodes is a no-op.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATABASE = ROOT / "_database"

BOILERPLATE_HEADERS = {
    "## Migration",
    "## Clean Node",
    "## Imported Staging Nodes",
}

# These section headers wrap content we WANT to keep. Just strip the header line.
UNWRAP_HEADERS = {
    "## Extracted Row",
}

# Frontmatter keys we keep on the promoted node (others become provenance prose
# only if needed). Anything case-graph-specific is preserved verbatim.
PRESERVE_FM_KEYS = {
    "id", "entity", "title", "node_kind", "legacy_type", "legacy_paths",
    "source_table",
    # case-graph extracted fields (reuse_einsatz, datenpunkt, akteur_beteiligung)
    "alte_funktion", "neue_funktion", "menge_umfang",
    "bauteil_label", "material_label", "herkunft_label",
    "bauobjekt", "fallstudie", "projekt",
    "huerde_label", "norm_recht_label", "pruefung_label", "quelle_label",
    "akteur", "akteurrolle", "field", "wert", "einheit", "kennwertdefinition",
    "datenqualitaet",
}

DROP_FM_KEYS = {
    "migration_status", "migration_action", "target_primary",
    "target_roles", "risk_flags", "node_kind",  # node_kind is implicit from path
}


def parse_frontmatter(text: str) -> tuple[dict[str, list[str]], str]:
    """Return ({key: [value_lines]}, body_after_frontmatter)."""
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if len(lines) < 2:
        return {}, text
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return {}, text
    fm: dict[str, list[str]] = {}
    current_key = None
    for line in lines[1:end_idx]:
        # YAML list continuation
        if line.startswith("  -") or line.startswith("    -"):
            if current_key:
                fm[current_key].append(line)
            continue
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            current_key = key
            fm[key] = [value] if value else []
        elif current_key and line.startswith("  "):
            fm[current_key].append(line)
    body = "\n".join(lines[end_idx + 1:])
    return fm, body


def strip_value_quotes(v: str) -> str:
    v = v.strip()
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    return v


def render_frontmatter(fm: dict[str, list[str]]) -> str:
    """Emit YAML frontmatter — values are wrapped in quotes if they contain
    special chars. Lists (key with no value, multiple bullet sub-lines) emit
    in YAML block-list style."""
    def is_list(values: list[str]) -> bool:
        if not values:
            return False
        return any(v.strip().startswith("-") for v in values)

    lines = ["---"]
    for key, values in fm.items():
        if not values:
            lines.append(f"{key}:")
            continue
        if is_list(values):
            lines.append(f"{key}:")
            for item in values:
                stripped = item.strip()
                if stripped.startswith("- "):
                    val = strip_value_quotes(stripped[2:])
                elif stripped.startswith("-"):
                    val = strip_value_quotes(stripped[1:].strip())
                else:
                    val = strip_value_quotes(stripped)
                lines.append(f'  - "{val}"')
        else:
            v = strip_value_quotes(values[0])
            lines.append(f'{key}: "{v}"')
    lines.append("---")
    return "\n".join(lines)


def strip_boilerplate(body: str) -> str:
    """Drop boilerplate sections from the body. A section runs from its ## header
    to the next ## or end-of-file. Also strips:
      - leading `# Title` (we re-emit it ourselves)
      - embedded `---` frontmatter blocks (from legacy-content-was-pasted-in)
    """
    # Strip embedded frontmatter blocks: any `---` ... `---` pair at line start
    body = re.sub(r"^---\n.*?\n---\n", "", body, count=10, flags=re.MULTILINE | re.DOTALL)

    # Strip leading `# Title` H1 (we'll re-emit one)
    lines = body.splitlines()
    while lines and (not lines[0].strip() or lines[0].lstrip().startswith("# ")):
        lines.pop(0)
    body = "\n".join(lines)

    # Tokenize by ## headers
    chunks: list[str] = []
    current = []
    skip_current = False
    unwrap_current = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            if current:
                if not skip_current:
                    if unwrap_current:
                        chunks.append("\n".join(current[1:]))
                    else:
                        chunks.append("\n".join(current))
            current = [line]
            skip_current = stripped in BOILERPLATE_HEADERS
            unwrap_current = stripped in UNWRAP_HEADERS
            if stripped.startswith("## Legacy Content:"):
                unwrap_current = True
        else:
            current.append(line)
    if current:
        if not skip_current:
            if unwrap_current:
                chunks.append("\n".join(current[1:]))
            else:
                chunks.append("\n".join(current))
    out = "\n".join(chunks).strip()
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


def slugify_title_from_id(node_id: str) -> str:
    return node_id.replace("_", " ")


def promote_node(entity: str, node_id: str, node_dir: Path, stats: dict) -> None:
    dat = node_dir / "DATEIEN"
    index_md = node_dir / "index.md"
    staging_files = []
    legacy_files = []
    if dat.exists():
        for f in sorted(dat.iterdir()):
            if not f.is_file():
                continue
            if f.name.endswith("staging_index.md"):
                staging_files.append(f)
            else:
                legacy_files.append(f)

    if not staging_files and not legacy_files:
        stats["skipped_no_dateien"] += 1
        return

    # Determine title
    existing_fm, _ = parse_frontmatter(index_md.read_text(encoding="utf-8-sig") if index_md.exists() else "")
    title = strip_value_quotes(existing_fm.get("title", [node_id])[0]) if existing_fm.get("title") else node_id

    if staging_files:
        primary_fm, primary_body = parse_frontmatter(staging_files[0].read_text(encoding="utf-8"))
        # Title from staging is cleaner (no mojibake)
        if primary_fm.get("title"):
            title = strip_value_quotes(primary_fm["title"][0])
        body_chunks = [strip_boilerplate(primary_body)]
        # Append additional staging sources as Quelle sections
        for extra in staging_files[1:]:
            extra_fm, extra_body = parse_frontmatter(extra.read_text(encoding="utf-8"))
            extra_clean = strip_boilerplate(extra_body)
            if extra_clean.strip():
                body_chunks.append(f"## Quelle: {extra.stem}\n\n{extra_clean}")
        body = "\n\n".join(c for c in body_chunks if c.strip())
        # Build clean frontmatter
        new_fm: dict[str, list[str]] = {
            "entity": [entity],
            "id": [node_id],
            "title": [title],
            "build_status": ["promoted_phase42"],
        }
        for key in PRESERVE_FM_KEYS:
            if key in primary_fm and key not in {"entity", "id", "title"}:
                new_fm[key] = primary_fm[key]
        stats["promoted_with_staging"] += 1
    else:
        # legacy-only DATEIEN: e.g. quelle/* nodes
        primary = legacy_files[0]
        text = primary.read_text(encoding="utf-8", errors="replace")
        legacy_fm, legacy_body = parse_frontmatter(text)
        body_chunks = [strip_boilerplate(legacy_body)]
        for extra in legacy_files[1:]:
            t = extra.read_text(encoding="utf-8", errors="replace")
            efm, ebody = parse_frontmatter(t)
            cleaned = strip_boilerplate(ebody)
            if cleaned.strip():
                body_chunks.append(f"## Quelle: {extra.stem}\n\n{cleaned}")
        body = "\n\n".join(c for c in body_chunks if c.strip())
        new_fm = {
            "entity": [entity],
            "id": [node_id],
            "title": [strip_value_quotes(legacy_fm.get("title", [title])[0]) if legacy_fm.get("title") else title],
            "build_status": ["promoted_phase42"],
            "source_filename": [primary.name],
        }
        if "type" in legacy_fm:
            new_fm["legacy_type"] = legacy_fm["type"]
        stats["promoted_legacy_only"] += 1

    out = render_frontmatter(new_fm) + "\n\n# " + title + "\n\n" + body + "\n"
    index_md.write_text(out, encoding="utf-8", newline="\n")


def main(argv: list[str]) -> int:
    sample_only = "--sample" in argv
    only_entities = [a for a in argv[1:] if not a.startswith("--")]

    stats = {
        "promoted_with_staging": 0,
        "promoted_legacy_only": 0,
        "skipped_no_dateien": 0,
    }
    sample_count = 0
    SAMPLE_LIMIT = 5

    for entity_dir in sorted(DATABASE.iterdir()):
        if not entity_dir.is_dir() or entity_dir.name.startswith("_"):
            continue
        entity = entity_dir.name
        if only_entities and entity not in only_entities:
            continue
        for node_dir in sorted(entity_dir.iterdir()):
            if not node_dir.is_dir():
                continue
            if sample_only and sample_count >= SAMPLE_LIMIT:
                break
            promote_node(entity, node_dir.name, node_dir, stats)
            sample_count += 1
        if sample_only and sample_count >= SAMPLE_LIMIT:
            break

    print(f"Promoted with staging file: {stats['promoted_with_staging']}")
    print(f"Promoted from legacy file:  {stats['promoted_legacy_only']}")
    print(f"Skipped (no DATEIEN):       {stats['skipped_no_dateien']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
