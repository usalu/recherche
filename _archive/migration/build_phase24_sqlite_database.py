from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATABASE_ROOT = ROOT / "_database"
NODE_INVENTORY = DATABASE_ROOT / "_system" / "node_inventory.csv"
CLEAN_EDGES = DATABASE_ROOT / "_edges" / "clean_confirmed_edges.csv"
EDGE_REVIEW = DATABASE_ROOT / "_edges" / "clean_edge_review_queue.csv"
SQLITE_PATH = DATABASE_ROOT / "_system" / "reuse_ontology.sqlite"
REPORT_PATH = ROOT / "_migration" / "24_SQLite_Build_Report.md"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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
        key = key.strip()
        value = value.strip().strip('"')
        if key:
            data[key] = value
    return data


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA foreign_keys = ON;

        DROP TABLE IF EXISTS edge_review;
        DROP TABLE IF EXISTS edges;
        DROP TABLE IF EXISTS nodes;

        CREATE TABLE nodes (
          entity TEXT NOT NULL,
          id TEXT NOT NULL,
          typed_path TEXT NOT NULL UNIQUE,
          title TEXT,
          build_status TEXT,
          markdown_path TEXT NOT NULL,
          markdown_body TEXT,
          frontmatter_json TEXT,
          dateien_file_count INTEGER DEFAULT 0,
          imported_source_count INTEGER DEFAULT 0,
          PRIMARY KEY (entity, id)
        );

        CREATE TABLE edges (
          source_entity TEXT NOT NULL,
          source_id TEXT NOT NULL,
          relation TEXT NOT NULL,
          target_entity TEXT NOT NULL,
          target_id TEXT NOT NULL,
          field TEXT,
          raw_label TEXT,
          confidence TEXT,
          resolution_rule TEXT,
          legacy_path TEXT,
          original_source TEXT,
          original_relation TEXT,
          original_target TEXT,
          edge_cleaning TEXT,
          FOREIGN KEY (source_entity, source_id) REFERENCES nodes(entity, id),
          FOREIGN KEY (target_entity, target_id) REFERENCES nodes(entity, id)
        );

        CREATE TABLE edge_review (
          source TEXT,
          relation TEXT,
          target TEXT,
          review_reason TEXT,
          suggested_source TEXT,
          suggested_relation TEXT,
          suggested_target TEXT,
          field TEXT,
          raw_label TEXT,
          confidence TEXT,
          resolution_rule TEXT,
          legacy_path TEXT
        );

        CREATE INDEX idx_edges_source ON edges(source_entity, source_id);
        CREATE INDEX idx_edges_target ON edges(target_entity, target_id);
        CREATE INDEX idx_edges_relation ON edges(relation);
        CREATE INDEX idx_nodes_entity ON nodes(entity);
        """
    )


def build_database() -> dict[str, int]:
    if SQLITE_PATH.exists():
        SQLITE_PATH.unlink()

    node_rows = read_csv(NODE_INVENTORY)
    edge_rows = read_csv(CLEAN_EDGES)
    review_rows = read_csv(EDGE_REVIEW)

    conn = sqlite3.connect(SQLITE_PATH)
    try:
        create_schema(conn)

        for row in node_rows:
            markdown_path = ROOT / row["markdown_path"]
            markdown_body = read_text(markdown_path)
            frontmatter_json = json.dumps(parse_frontmatter(markdown_body), ensure_ascii=False, sort_keys=True)
            conn.execute(
                """
                INSERT INTO nodes (
                  entity, id, typed_path, title, build_status, markdown_path,
                  markdown_body, frontmatter_json, dateien_file_count, imported_source_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["entity"],
                    row["id"],
                    row["typed_path"],
                    row.get("title", ""),
                    row.get("build_status", ""),
                    row["markdown_path"],
                    markdown_body,
                    frontmatter_json,
                    int(row.get("dateien_file_count") or 0),
                    int(row.get("imported_source_count") or 0),
                ),
            )

        for row in edge_rows:
            conn.execute(
                """
                INSERT INTO edges (
                  source_entity, source_id, relation, target_entity, target_id,
                  field, raw_label, confidence, resolution_rule, legacy_path,
                  original_source, original_relation, original_target, edge_cleaning
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["source_entity"],
                    row["source_id"],
                    row["relation"],
                    row["target_entity"],
                    row["target_id"],
                    row.get("field", ""),
                    row.get("raw_label", ""),
                    row.get("confidence", ""),
                    row.get("resolution_rule", ""),
                    row.get("legacy_path", ""),
                    row.get("original_source", ""),
                    row.get("original_relation", ""),
                    row.get("original_target", ""),
                    row.get("edge_cleaning", ""),
                ),
            )

        for row in review_rows:
            conn.execute(
                """
                INSERT INTO edge_review (
                  source, relation, target, review_reason, suggested_source,
                  suggested_relation, suggested_target, field, raw_label,
                  confidence, resolution_rule, legacy_path
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row.get("source", ""),
                    row.get("relation", ""),
                    row.get("target", ""),
                    row.get("review_reason", ""),
                    row.get("suggested_source", ""),
                    row.get("suggested_relation", ""),
                    row.get("suggested_target", ""),
                    row.get("field", ""),
                    row.get("raw_label", ""),
                    row.get("confidence", ""),
                    row.get("resolution_rule", ""),
                    row.get("legacy_path", ""),
                ),
            )

        dangling_sources = conn.execute(
            """
            SELECT COUNT(*)
            FROM edges e
            LEFT JOIN nodes n
              ON e.source_entity = n.entity AND e.source_id = n.id
            WHERE n.entity IS NULL
            """
        ).fetchone()[0]
        dangling_targets = conn.execute(
            """
            SELECT COUNT(*)
            FROM edges e
            LEFT JOIN nodes n
              ON e.target_entity = n.entity AND e.target_id = n.id
            WHERE n.entity IS NULL
            """
        ).fetchone()[0]

        conn.commit()
        return {
            "nodes": len(node_rows),
            "edges": len(edge_rows),
            "edge_review": len(review_rows),
            "dangling_sources": dangling_sources,
            "dangling_targets": dangling_targets,
        }
    finally:
        conn.close()


def write_report(counts: dict[str, int]) -> None:
    report = [
        "# Phase 24 SQLite Build Report",
        "",
        "## Output",
        "",
        f"- SQLite file: `{SQLITE_PATH.relative_to(ROOT).as_posix()}`",
        "",
        "## Counts",
        "",
        f"- Nodes: {counts['nodes']}",
        f"- Clean edges: {counts['edges']}",
        f"- Edge-review rows: {counts['edge_review']}",
        f"- Dangling edge sources: {counts['dangling_sources']}",
        f"- Dangling edge targets: {counts['dangling_targets']}",
        "",
        "## Tables",
        "",
        "- `nodes`",
        "- `edges`",
        "- `edge_review`",
    ]
    REPORT_PATH.write_text("\n".join(report) + "\n", encoding="utf-8")
    (DATABASE_ROOT / "_system" / "sqlite_build_report.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    counts = build_database()
    write_report(counts)
    print(f"Wrote {SQLITE_PATH}")
    print(f"Wrote {REPORT_PATH}")
