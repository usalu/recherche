"""Export the full mit-bestand graph as a token-friendly text digest for ChatGPT upload.

Read-only. Connects via neo4j_env (same settings as MCP / backup scripts).

Usage:
  python _scripts/export_neo4j_chatgpt_digest.py
  python _scripts/export_neo4j_chatgpt_digest.py --with-descriptions --out _neo4j/exports/custom.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root, resolve_connection  # noqa: E402

SHORT_PROP_NAMES = {
    "alte_funktion": "alte",
    "neue_funktion": "neue",
    "projektstatus_text": "status_text",
    "entwurfsbeschreibung": "beschreibung",
}

LABEL_EXTRA_PROPS: dict[str, list[str]] = {
    "Bauteilgruppe": [
        "reuse_status",
        "alte_funktion",
        "neue_funktion",
        "bg_kind",
        "tragend",
        "status",
    ],
    "Projekt": [
        "name_full",
        "year_completed",
        "area_m2_gross",
        "adresse",
        "nutzung_text",
        "projektstatus_text",
        "status",
        "entwurfsbeschreibung",
    ],
    "Kennwert": [
        "kennwert",
        "wert",
        "wert_text",
        "einheit",
        "category",
        "method",
        "bilanzgrenze",
    ],
    "Bauwerk": ["name_full", "nutzung_text"],
}

OPTIONAL_SHORT_TEXT_PROPS = ("name_full", "beschreibung")
MAX_SHORT_TEXT_LEN = 120

DROP_NODE_PROPS = frozenset(
    {
        "id",
        "metadata_sidecar_key",
        "source_titles",
        "source_urls",
        "source_url",
        "source_quote",
        "primary_source_url",
        "latitude",
        "longitude",
        "geo_aktualisiert_am_utc",
        "geo_import_run",
        "geo_confidence",
        "entwurfsbeschreibung_quelle",
        "entwurfsqualitaet_run",
        "entwurfsqualitaet_am_utc",
        "entwurfsqualitaet_vokabular_version",
        "vokabular_version",
        "review_status",
        "review_run",
        "intake_run",
        "aktualisiert_am_utc",
        "created_at",
        "updated_at",
        "created_at_utc",
        "updated_at_utc",
        "confidence",
        "source_scope",
        "deprecated_am_utc",
        "deprecated_reason",
        "dedupe_key",
        "dedup_run",
    }
)

DROP_PROP_PREFIXES = (
    "evidence_",
    "review_",
    "intake_",
    "dedupe",
)

DROP_PROP_SUFFIXES = (
    "_run",
    "_utc",
)


def primary_label(labels: list[str]) -> str:
    clean = sorted(lbl for lbl in labels if lbl != "DEPRECATED")
    return clean[0] if clean else "Unknown"


def all_labels_text(labels: list[str]) -> str | None:
    clean = sorted(lbl for lbl in labels if lbl != "DEPRECATED")
    if len(clean) <= 1:
        return None
    return ",".join(clean)


def display_name(labels: list[str], props: dict[str, Any]) -> str:
    name = props.get("name")
    if name not in (None, ""):
        return str(name).strip()
    if "Kennwert" in labels:
        parts = [props.get("kennwert"), props.get("wert_text"), props.get("einheit")]
        text = " ".join(str(p).strip() for p in parts if p not in (None, ""))
        if text:
            return text
    node_id = props.get("id")
    if node_id not in (None, ""):
        return str(node_id)
    return "?"


def should_drop_prop(key: str) -> bool:
    if key in DROP_NODE_PROPS:
        return True
    if any(key.startswith(prefix) for prefix in DROP_PROP_PREFIXES):
        return True
    if any(key.endswith(suffix) for suffix in DROP_PROP_SUFFIXES):
        return True
    return False


def format_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (list, tuple)):
        return ",".join(format_value(v) for v in value if v not in (None, ""))
    text = str(value).replace("\n", " ").replace("\r", " ").strip()
    text = re.sub(r"\s+", " ", text)
    return text.replace(";", ",")


def collect_node_props(
    labels: list[str],
    props: dict[str, Any],
    *,
    with_descriptions: bool,
    with_geo: bool,
) -> list[tuple[str, str]]:
    kept: list[tuple[str, str]] = []
    seen: set[str] = set()

    label_set = set(labels)
    for label in sorted(label_set):
        for key in LABEL_EXTRA_PROPS.get(label, []):
            if key == "entwurfsbeschreibung" and not with_descriptions:
                continue
            if key in seen or should_drop_prop(key):
                continue
            value = format_value(props.get(key))
            if not value:
                continue
            short_key = SHORT_PROP_NAMES.get(key, key)
            kept.append((short_key, value))
            seen.add(key)

    if with_geo:
        for key in ("latitude", "longitude"):
            value = format_value(props.get(key))
            if value:
                short_key = SHORT_PROP_NAMES.get(key, key)
                if short_key not in seen:
                    kept.append((short_key, value))
                    seen.add(short_key)

    for key in OPTIONAL_SHORT_TEXT_PROPS:
        if key in seen or should_drop_prop(key):
            continue
        raw = props.get(key)
        if raw in (None, ""):
            continue
        text = format_value(raw)
        if len(text) > MAX_SHORT_TEXT_LEN:
            continue
        short_key = SHORT_PROP_NAMES.get(key, key)
        kept.append((short_key, text))
        seen.add(key)

    labels_text = all_labels_text(labels)
    if labels_text:
        kept.insert(0, ("labels", labels_text))

    return kept


def format_node_line(
    node_id: int,
    labels: list[str],
    props: dict[str, Any],
    *,
    with_descriptions: bool,
    with_geo: bool,
) -> str:
    name = display_name(labels, props)
    extras = collect_node_props(
        labels, props, with_descriptions=with_descriptions, with_geo=with_geo
    )
    line = f"{node_id} {name}"
    if extras:
        line += " | " + "; ".join(f"{k}={v}" for k, v in extras)
    return line


def fetch_graph(
    session,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    node_rows = [
        {
            "element_id": rec["element_id"],
            "labels": list(rec["labels"]),
            "properties": dict(rec["properties"]),
        }
        for rec in session.run(
            """
            MATCH (n)
            WHERE NOT n:DEPRECATED
            RETURN elementId(n) AS element_id, labels(n) AS labels, properties(n) AS properties
            """
        )
    ]
    rel_rows = [
        {
            "from_element_id": rec["from_element_id"],
            "to_element_id": rec["to_element_id"],
            "type": rec["type"],
        }
        for rec in session.run(
            """
            MATCH (a)-[r]->(b)
            WHERE NOT a:DEPRECATED AND NOT b:DEPRECATED
            RETURN elementId(a) AS from_element_id,
                   elementId(b) AS to_element_id,
                   type(r) AS type
            ORDER BY type(r), elementId(a), elementId(b)
            """
        )
    ]
    return node_rows, rel_rows


def build_digest(
    node_rows: list[dict[str, Any]],
    rel_rows: list[dict[str, str]],
    *,
    database: str,
    with_descriptions: bool,
    with_geo: bool,
) -> str:
    sorted_nodes = sorted(
        node_rows,
        key=lambda row: (
            primary_label(row["labels"]),
            display_name(row["labels"], row["properties"]).casefold(),
            row["element_id"],
        ),
    )

    element_to_id = {
        row["element_id"]: idx + 1 for idx, row in enumerate(sorted_nodes)
    }

    by_label: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    for row in sorted_nodes:
        by_label[primary_label(row["labels"])].append(
            (element_to_id[row["element_id"]], row)
        )

    edges_by_type: dict[str, list[str]] = defaultdict(list)
    skipped_edges = 0
    for rel in rel_rows:
        src = element_to_id.get(rel["from_element_id"])
        dst = element_to_id.get(rel["to_element_id"])
        if src is None or dst is None:
            skipped_edges += 1
            continue
        edges_by_type[rel["type"]].append(f"{src}>{dst}")

    edge_count = sum(len(v) for v in edges_by_type.values())

    lines: list[str] = [
        f"# {database} graph digest — {len(sorted_nodes)} nodes, {edge_count} edges",
        "## Legend: node line = \"<id> <name> [| key=val; ...]\"; edges = \"<TYPE>: src>dst src>dst ...\"",
        "",
        "## Nodes",
    ]

    for label in sorted(by_label):
        entries = by_label[label]
        lines.append(f"### {label} ({len(entries)})")
        for node_id, row in entries:
            lines.append(
                format_node_line(
                    node_id,
                    row["labels"],
                    row["properties"],
                    with_descriptions=with_descriptions,
                    with_geo=with_geo,
                )
            )
        lines.append("")

    lines.append("## Edges")
    for rel_type in sorted(edges_by_type):
        pairs = edges_by_type[rel_type]
        lines.append(f"{rel_type}: {' '.join(pairs)}")

    if skipped_edges:
        lines.append("")
        lines.append(f"# skipped_edges={skipped_edges}")

    return "\n".join(lines) + "\n", edge_count


def default_out_path(database: str) -> Path:
    safe_db = re.sub(r"[^A-Za-z0-9_.-]+", "_", database or "neo4j")
    stamp = date.today().isoformat()
    return repo_root() / "_neo4j" / "exports" / f"{safe_db}_digest_{stamp}.md"


def export_digest(
    out_path: Path,
    *,
    with_descriptions: bool = False,
    with_geo: bool = False,
) -> dict[str, Any]:
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise SystemExit("Install: pip install -r requirements-neo4j.txt") from exc

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise SystemExit("Missing Neo4j connection settings.")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            node_rows, rel_rows = fetch_graph(session)
            digest, edge_count = build_digest(
                node_rows,
                rel_rows,
                database=database,
                with_descriptions=with_descriptions,
                with_geo=with_geo,
            )
    finally:
        driver.close()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(digest, encoding="utf-8")

    size_bytes = out_path.stat().st_size
    return {
        "out_path": str(out_path),
        "database": database,
        "nodes": len(node_rows),
        "relationships_in_db": len(rel_rows),
        "edge_pairs_exported": edge_count,
        "bytes": size_bytes,
        "approx_tokens": round(size_bytes / 4),
        "with_descriptions": with_descriptions,
        "with_geo": with_geo,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output path (default: _neo4j/exports/<db>_digest_<date>.md)",
    )
    parser.add_argument(
        "--with-descriptions",
        action="store_true",
        help="Include long entwurfsbeschreibung text on Projekt nodes",
    )
    parser.add_argument(
        "--with-geo",
        action="store_true",
        help="Include latitude/longitude on nodes that have them",
    )
    args = parser.parse_args()

    _, _, _, database = resolve_connection()
    out_path = args.out or default_out_path(database)
    result = export_digest(
        out_path,
        with_descriptions=args.with_descriptions,
        with_geo=args.with_geo,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
