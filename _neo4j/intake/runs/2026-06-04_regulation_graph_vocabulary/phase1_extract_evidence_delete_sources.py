"""Phase 1: extract evidence to properties and delete the source-node layer.

Dry-run by default. Commit mode:
  1. snapshots the full source layer and deleted relationships,
  2. copies BELEGT_IN target URLs/titles onto cited non-source nodes,
  3. migrates categorical evidence_confidence to numeric confidence,
  4. deletes Quelle/ExternalLink/SectionRef/Dossier/ResearchDocument source nodes,
  5. deletes OntologyAnchor scaffolding and source-pointer relationships.

Usage:
  python phase1_extract_evidence_delete_sources.py
  python phase1_extract_evidence_delete_sources.py --commit
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[4]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402

OUT = Path(__file__).resolve().parent
SOURCE_LABELS = ["Quelle", "ExternalLink", "SectionRef", "Dossier", "ResearchDocument"]
SCAFFOLD_LABELS = ["OntologyAnchor"]
RUN = "regulation_graph_vocab_2026_06_04_phase1"


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v is not None and str(v).strip()]
    text = str(value).strip()
    return [text] if text else []


def normalize_url(url: str) -> str:
    """Normalize only for deduping; keep original URL as stored evidence."""
    text = url.strip()
    if not text:
        return ""
    try:
        parts = urlsplit(text)
    except ValueError:
        return text.rstrip("/")
    if not parts.scheme or not parts.netloc:
        return text.rstrip("/")
    query = [
        (k, v)
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if not k.lower().startswith("utm_")
    ]
    return urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path.rstrip("/") or "/",
            urlencode(query, doseq=True),
            "",
        )
    )


def dedupe_preserve(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        key = normalize_url(value) if value.startswith(("http://", "https://")) else value.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


def source_title(props: dict[str, Any]) -> str | None:
    for key in ("title", "titel", "name"):
        value = props.get(key)
        if value:
            return str(value)
    return None


def collect_state(session) -> dict[str, Any]:
    counts = session.run(
        """
        MATCH (n)
        WITH count(n) AS nodes
        MATCH ()-[r]->()
        RETURN nodes, count(r) AS relationships
        """
    ).single()
    label_counts = {
        label: session.run(f"MATCH (n:`{label}`) RETURN count(n) AS c").single()["c"]
        for label in SOURCE_LABELS + SCAFFOLD_LABELS
    }
    rel_counts = {
        rel_type: session.run(f"MATCH ()-[r:`{rel_type}`]->() RETURN count(r) AS c").single()["c"]
        for rel_type in ("BELEGT_IN", "HAS_SOURCE_LINK", "ANCHORED_BY")
    }
    confidence_count = session.run(
        "MATCH ()-[r]->() WHERE r.evidence_confidence IS NOT NULL RETURN count(r) AS c"
    ).single()["c"]
    return {
        "nodes": int(counts["nodes"]),
        "relationships": int(counts["relationships"]),
        "label_counts": {k: int(v) for k, v in label_counts.items()},
        "relationship_counts": {k: int(v) for k, v in rel_counts.items()},
        "evidence_confidence_edges": int(confidence_count),
    }


def snapshot_deleted_layer(session, path: Path) -> dict[str, Any]:
    source_nodes = [
        record.data()
        for record in session.run(
            """
            MATCH (n)
            WHERE any(label IN labels(n) WHERE label IN $labels)
            RETURN elementId(n) AS element_id, labels(n) AS labels, properties(n) AS properties
            ORDER BY elementId(n)
            """,
            labels=SOURCE_LABELS + SCAFFOLD_LABELS,
        )
    ]
    deleted_rels = [
        record.data()
        for record in session.run(
            """
            MATCH (a)-[r]->(b)
            WHERE type(r) IN ['BELEGT_IN','HAS_SOURCE_LINK','ANCHORED_BY']
               OR any(label IN labels(a) WHERE label IN $labels)
               OR any(label IN labels(b) WHERE label IN $labels)
            RETURN elementId(r) AS element_id,
                   type(r) AS type,
                   elementId(a) AS from_element_id,
                   a.id AS from_id,
                   labels(a) AS from_labels,
                   elementId(b) AS to_element_id,
                   b.id AS to_id,
                   labels(b) AS to_labels,
                   properties(r) AS properties
            ORDER BY elementId(r)
            """,
            labels=SOURCE_LABELS + SCAFFOLD_LABELS,
        )
    ]
    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_labels": SOURCE_LABELS,
        "scaffold_labels": SCAFFOLD_LABELS,
        "source_nodes": source_nodes,
        "deleted_relationships": deleted_rels,
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return {"source_nodes": len(source_nodes), "deleted_relationships": len(deleted_rels)}


def build_extractions(session) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """Build source_urls/source_titles updates for cited non-source nodes."""
    updates: dict[str, dict[str, Any]] = {}
    stats = {
        "belegt_in_edges_seen": 0,
        "cited_nodes_seen": 0,
        "cited_non_source_nodes": 0,
        "cited_non_source_nodes_with_url": 0,
        "cited_source_nodes_skipped": 0,
        "distinct_cited_urls": set(),
        "url_less_citations": 0,
    }
    records = session.run(
        """
        MATCH (x)-[:BELEGT_IN]->(q:Quelle)
        RETURN elementId(x) AS x_eid,
               labels(x) AS x_labels,
               properties(x) AS x_props,
               properties(q) AS q_props
        """
    )
    cited_nodes: set[str] = set()
    for record in records:
        stats["belegt_in_edges_seen"] += 1
        x_eid = record["x_eid"]
        cited_nodes.add(x_eid)
        x_labels = set(record["x_labels"])
        if x_labels.intersection(SOURCE_LABELS):
            stats["cited_source_nodes_skipped"] += 1
            continue
        q_props = dict(record["q_props"] or {})
        x_props = dict(record["x_props"] or {})
        url = q_props.get("url")
        title = source_title(q_props)
        if url:
            stats["distinct_cited_urls"].add(normalize_url(str(url)))
        else:
            stats["url_less_citations"] += 1

        entry = updates.setdefault(
            x_eid,
            {
                "source_urls": as_list(x_props.get("source_urls"))
                + as_list(x_props.get("source_url"))
                + as_list(x_props.get("primary_source_url")),
                "source_titles": as_list(x_props.get("source_titles")),
            },
        )
        if url:
            entry["source_urls"].append(str(url))
        if title:
            entry["source_titles"].append(title)

    stats["cited_nodes_seen"] = len(cited_nodes)
    stats["cited_non_source_nodes"] = len(updates)
    for entry in updates.values():
        entry["source_urls"] = dedupe_preserve(entry["source_urls"])
        # Titles are not normalized as URLs; exact dedup only.
        entry["source_titles"] = dedupe_preserve(entry["source_titles"])
    stats["cited_non_source_nodes_with_url"] = sum(
        1 for entry in updates.values() if entry["source_urls"]
    )
    stats["distinct_cited_urls"] = len(stats["distinct_cited_urls"])
    return updates, stats


def confidence_case() -> str:
    return """
    MATCH ()-[r]->()
    WHERE r.evidence_confidence IS NOT NULL
    WITH r, r.evidence_confidence AS ec
    SET r.confidence = CASE
      WHEN ec = 'belegt' THEN 0.9
      WHEN ec = 'teilweise_belegt' THEN 0.6
      WHEN ec = 'wahrscheinlich' THEN 0.5
      WHEN ec = 'abgeleitet' THEN 0.4
      WHEN ec = 'abgeleitet_aus_bestehender_bauteilgruppe' THEN 0.4
      WHEN ec = 'inferiert' THEN 0.25
      WHEN ec = 'unsicher' THEN 0.2
      WHEN ec = 'unklar' THEN r.confidence
      ELSE r.confidence
    END
    REMOVE r.evidence_confidence
    RETURN count(r) AS c
    """


def run(commit: bool) -> dict[str, Any]:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "phase": "phase1_extract_evidence_delete_sources",
        "database": database,
        "commit": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    snapshot_path = OUT / "phase1_before.json"

    with driver.session(database=database) as session:
        before = collect_state(session)
        updates, extraction_stats = build_extractions(session)
        report["before"] = before
        report["extraction"] = {
            **extraction_stats,
            "non_source_nodes_to_update": len(updates),
            "source_url_values_to_write": sum(len(v["source_urls"]) for v in updates.values()),
        }
        report["planned"] = {
            "delete_source_nodes": before["label_counts"],
            "delete_source_relationships": before["relationship_counts"],
            "migrate_evidence_confidence_edges": before["evidence_confidence_edges"],
        }

        if commit:
            report["snapshot"] = snapshot_deleted_layer(session, snapshot_path)
            for eid, payload in updates.items():
                session.run(
                    """
                    MATCH (n)
                    WHERE elementId(n) = $eid
                    SET n.source_urls = CASE
                      WHEN size($source_urls) = 0 THEN n.source_urls
                      ELSE $source_urls
                    END
                    SET n.source_titles = CASE
                      WHEN size($source_titles) = 0 THEN n.source_titles
                      ELSE $source_titles
                    END
                    """,
                    eid=eid,
                    source_urls=payload["source_urls"],
                    source_titles=payload["source_titles"],
                ).consume()

            confidence_migrated = session.run(confidence_case()).single()["c"]
            report["confidence_migrated"] = int(confidence_migrated)

            session.run("MATCH ()-[r:HAS_SOURCE_LINK]->() DELETE r").consume()
            session.run("MATCH ()-[r:ANCHORED_BY]->() DELETE r").consume()
            session.run("MATCH ()-[r:BELEGT_IN]->() DELETE r").consume()
            session.run(
                """
                MATCH (n)
                WHERE any(label IN labels(n) WHERE label IN $labels)
                DETACH DELETE n
                """,
                labels=SOURCE_LABELS + SCAFFOLD_LABELS,
            ).consume()
            after = collect_state(session)
            report["after"] = after
            report["acceptance"] = acceptance(session, extraction_stats)
        else:
            report["snapshot_would_write"] = str(snapshot_path)
            report["confidence_migrated"] = 0
            report["acceptance_preview"] = {
                "source_layer_will_be_deleted": True,
                "evidence_confidence_edges_will_be_zero": True,
                "non_source_nodes_receive_source_urls": len(updates),
            }

    driver.close()
    report_path = OUT / ("phase1_report.json" if commit else "phase1_dry_run_report.json")
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return report


def acceptance(session, extraction_stats: dict[str, Any]) -> dict[str, Any]:
    source_counts = {
        label: session.run(f"MATCH (n:`{label}`) RETURN count(n) AS c").single()["c"]
        for label in SOURCE_LABELS + SCAFFOLD_LABELS
    }
    rel_counts = {
        rel_type: session.run(f"MATCH ()-[r:`{rel_type}`]->() RETURN count(r) AS c").single()["c"]
        for rel_type in ("BELEGT_IN", "HAS_SOURCE_LINK", "ANCHORED_BY")
    }
    evidence_confidence_edges = session.run(
        "MATCH ()-[r]->() WHERE r.evidence_confidence IS NOT NULL RETURN count(r) AS c"
    ).single()["c"]
    duplicate_source_url_arrays = session.run(
        """
        MATCH (n)
        WHERE n.source_urls IS NOT NULL
        WITH n, n.source_urls AS urls
        WHERE size(urls) > 1
          AND any(i IN range(0, size(urls)-2)
                  WHERE any(j IN range(i+1, size(urls)-1) WHERE urls[i] = urls[j]))
        RETURN count(n) AS c
        """
    ).single()["c"]
    # Avoid requiring APOC for the main no-loss check; compare URL-bearing nodes after extraction.
    source_url_nodes = session.run(
        "MATCH (n) WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0 RETURN count(n) AS c"
    ).single()["c"]
    return {
        "source_label_counts": {k: int(v) for k, v in source_counts.items()},
        "source_relationship_counts": {k: int(v) for k, v in rel_counts.items()},
        "evidence_confidence_edges": int(evidence_confidence_edges),
        "source_url_nodes": int(source_url_nodes),
        "expected_min_source_url_nodes": int(
            extraction_stats["cited_non_source_nodes_with_url"]
        ),
        "url_less_citations_not_counted_as_real_evidence": int(
            extraction_stats["url_less_citations"]
        ),
        "duplicate_source_url_arrays": int(duplicate_source_url_arrays),
        "passed": all(int(v) == 0 for v in source_counts.values())
        and all(int(v) == 0 for v in rel_counts.values())
        and int(evidence_confidence_edges) == 0
        and int(source_url_nodes)
        >= int(extraction_stats["cited_non_source_nodes_with_url"])
        and int(duplicate_source_url_arrays) == 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true", help="Write Phase 1 changes.")
    args = parser.parse_args()
    report = run(args.commit)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 0 if (not args.commit or report.get("acceptance", {}).get("passed")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
