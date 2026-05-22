from __future__ import annotations

import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

URI = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
USER = (os.environ.get("NEO4J_USER") or os.environ.get("NEO4J_USERNAME") or "neo4j").strip()
DATABASE = os.environ.get("NEO4J_DATABASE", "mit-bestand").strip()
PASSWORD_FILE = Path(".neo4j_password")

RUN = "evidence_connections_300_2026_06_04"
SOURCE_JSON = Path(
    "_neo4j/intake/inbox/research/"
    "bauteilboerse_network_2026-06-01_existing_graph_connections_PRIORITY_DEEPER_KEEPALL.json"
)
RUN_DIR = Path("_neo4j/intake/runs/2026-06-04_300_evidence_connections")
SELECTED_JSONL = RUN_DIR / "selected_edges.jsonl"
IMPORT_REPORT_JSON = RUN_DIR / "import_report.json"

SKIP_TYPES = {"HAT_METHODE", "HAT_MARKTMODELL"}
MIN_EXPECTED = 300
IMPORT_CONFIRMATION_ENV = "CONFIRM_BAUTEILBOERSE_300_IMPORT"


def read_password() -> str:
    env_password = (os.environ.get("NEO4J_PASSWORD") or "").strip()
    if env_password:
        return env_password
    for line in PASSWORD_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    raise RuntimeError("No password found in NEO4J_PASSWORD or .neo4j_password")


def evidence_url(props: dict[str, Any]) -> str | None:
    for key in ("evidence_url", "source_url"):
        value = props.get(key)
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            return value
    for key in ("candidate_source_urls", "evidence_urls"):
        value = props.get(key)
        if isinstance(value, list):
            for url in value:
                if isinstance(url, str) and url.startswith(("http://", "https://")):
                    return url
    return None


def scalarish(value: Any) -> bool:
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if isinstance(value, list):
        return all(item is None or isinstance(item, (str, int, float, bool)) for item in value)
    return False


def clean_props(props: dict[str, Any], *, created_node: bool = False) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}
    for key, value in props.items():
        if isinstance(key, str) and scalarish(value):
            cleaned[key] = value
    if created_node:
        cleaned["source_scope"] = RUN
    return cleaned


def cypher_labels(labels: list[str]) -> str:
    safe = []
    for label in labels:
        if isinstance(label, str) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", label):
            safe.append(label)
    if not safe:
        safe = ["Entity"]
    return ":" + ":".join(dict.fromkeys(safe))


def rel_id(row: dict[str, Any]) -> str:
    rid = row["props"].get("id")
    if isinstance(rid, str) and rid:
        return rid
    return f"r_{row['src_id']}__{row['type']}__{row['tgt_id']}"


def load_payload() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    data = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    nodes = {node["elementId"]: node for node in data["nodes"]}
    rows: list[dict[str, Any]] = []
    for edge in data["edges"]:
        props = edge.get("properties") or {}
        url = evidence_url(props)
        if not url:
            continue
        typ = edge.get("type")
        if typ in SKIP_TYPES:
            continue
        src = nodes.get(edge.get("source"))
        tgt = nodes.get(edge.get("target"))
        if not src or not tgt:
            continue
        src_props = src.get("properties") or {}
        tgt_props = tgt.get("properties") or {}
        src_id = src_props.get("id")
        tgt_id = tgt_props.get("id")
        if not isinstance(src_id, str) or not isinstance(tgt_id, str):
            continue
        rows.append(
            {
                "type": typ,
                "src_id": src_id,
                "src_labels": src.get("labels") or [],
                "src_props": clean_props(src_props, created_node=True),
                "tgt_id": tgt_id,
                "tgt_labels": tgt.get("labels") or [],
                "tgt_props": clean_props(tgt_props, created_node=True),
                "props": props,
                "evidence_url": url,
                "evidence_basis": props.get("evidence_basis")
                or props.get("evidence_excerpt")
                or props.get("scope_note")
                or "URL-backed candidate from PRIORITY_DEEPER_KEEPALL payload.",
            }
        )
    return nodes, rows


def main() -> int:
    if os.environ.get(IMPORT_CONFIRMATION_ENV, "").strip() != "YES":
        print(
            json.dumps(
                {
                    "status": "blocked_pending_user_confirmation",
                    "reason": (
                        "This run is not confirmed for import. Set "
                        f"{IMPORT_CONFIRMATION_ENV}=YES only after the corrected "
                        "candidate list has been reviewed and approved."
                    ),
                    "candidate_file": str(RUN_DIR / "selected_edges.filtered.jsonl"),
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 2

    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    _nodes, raw_rows = load_payload()
    driver = GraphDatabase.driver(URI, auth=(USER, read_password()))

    with driver:
        driver.verify_connectivity()
        with driver.session(database=DATABASE) as session:
            rel_types = {
                row["type"]
                for row in session.run("MATCH ()-[r]->() RETURN DISTINCT type(r) AS type")
            }
            quelle_id_by_url = {
                row["url"]: row["id"]
                for row in session.run(
                    """
                    MATCH (q:Quelle)
                    WHERE q.url IS NOT NULL AND q.id IS NOT NULL
                    RETURN q.url AS url, q.id AS id
                    """
                )
                if isinstance(row["url"], str) and isinstance(row["id"], str)
            }
            existing_rel_ids = {
                row["id"]
                for row in session.run("MATCH ()-[r]->() WHERE r.id IS NOT NULL RETURN r.id AS id")
                if isinstance(row["id"], str)
            }
            existing_triples = {
                (row["sid"], row["type"], row["tid"])
                for row in session.run(
                    """
                    MATCH (s)-[r]->(t)
                    WHERE s.id IS NOT NULL AND t.id IS NOT NULL
                    RETURN s.id AS sid, type(r) AS type, t.id AS tid
                    """
                )
                if isinstance(row["sid"], str) and isinstance(row["tid"], str)
            }
            live_node_ids = {
                row["id"]
                for row in session.run("MATCH (n) WHERE n.id IS NOT NULL RETURN n.id AS id")
                if isinstance(row["id"], str)
            }
            bauteilboerse_actor_ids = {
                row["id"]
                for row in session.run(
                    """
                    MATCH (a:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})
                    RETURN a.id AS id
                    """
                )
                if isinstance(row["id"], str)
            }

            selected: list[dict[str, Any]] = []
            skipped = Counter()
            seen_rel_ids: set[str] = set()
            seen_triples: set[tuple[str, str, str]] = set()
            for row in raw_rows:
                if "Quelle" in row["src_labels"]:
                    url = row["src_props"].get("url")
                    if isinstance(url, str) and url in quelle_id_by_url:
                        row["src_id"] = quelle_id_by_url[url]
                        row["src_props"]["id"] = row["src_id"]
                if "Quelle" in row["tgt_labels"]:
                    url = row["tgt_props"].get("url")
                    if isinstance(url, str) and url in quelle_id_by_url:
                        row["tgt_id"] = quelle_id_by_url[url]
                        row["tgt_props"]["id"] = row["tgt_id"]
                typ = row["type"]
                rid = rel_id(row)
                triple = (row["src_id"], typ, row["tgt_id"])
                if (
                    "Akteur" in row["src_labels"]
                    and "Bauteilgruppe" in row["tgt_labels"]
                    and row["src_id"] not in bauteilboerse_actor_ids
                ):
                    skipped["non_bauteilboerse_akteur_to_bauteilgruppe"] += 1
                    continue
                if typ not in rel_types:
                    skipped["relationship_type_not_live"] += 1
                    continue
                if rid in existing_rel_ids or triple in existing_triples:
                    skipped["already_in_graph"] += 1
                    continue
                if rid in seen_rel_ids or triple in seen_triples:
                    skipped["duplicate_in_payload"] += 1
                    continue
                row["id"] = rid
                row["src_exists_before"] = row["src_id"] in live_node_ids
                row["tgt_exists_before"] = row["tgt_id"] in live_node_ids
                selected.append(row)
                seen_rel_ids.add(rid)
                seen_triples.add(triple)

            if len(selected) < MIN_EXPECTED:
                raise RuntimeError(f"Selected only {len(selected)} edges, expected at least {MIN_EXPECTED}.")

            RUN_DIR.mkdir(parents=True, exist_ok=True)
            with SELECTED_JSONL.open("w", encoding="utf-8") as handle:
                for row in selected:
                    handle.write(
                        json.dumps(
                            {
                                "id": row["id"],
                                "type": row["type"],
                                "src_id": row["src_id"],
                                "src_labels": row["src_labels"],
                                "tgt_id": row["tgt_id"],
                                "tgt_labels": row["tgt_labels"],
                                "evidence_url": row["evidence_url"],
                                "evidence_basis": row["evidence_basis"],
                                "src_exists_before": row["src_exists_before"],
                                "tgt_exists_before": row["tgt_exists_before"],
                            },
                            ensure_ascii=False,
                        )
                        + "\n"
                    )

            nodes_to_create: dict[str, dict[str, Any]] = {}
            for row in selected:
                if not row["src_exists_before"]:
                    nodes_to_create[row["src_id"]] = {
                        "id": row["src_id"],
                        "labels": row["src_labels"],
                        "props": row["src_props"],
                    }
                if not row["tgt_exists_before"]:
                    nodes_to_create[row["tgt_id"]] = {
                        "id": row["tgt_id"],
                        "labels": row["tgt_labels"],
                        "props": row["tgt_props"],
                    }

            node_label_counter = Counter()
            for node in nodes_to_create.values():
                labels = cypher_labels(node["labels"])
                node_label_counter["+".join(node["labels"]) or "Entity"] += 1
                query = f"""
                MERGE (n{labels} {{id: $id}})
                SET n += $props
                """
                session.run(query, id=node["id"], props=node["props"]).consume()

            rel_counter = Counter()
            rows_by_type: dict[str, list[dict[str, Any]]] = {}
            for row in selected:
                rows_by_type.setdefault(row["type"], []).append(row)

            for typ, rows in rows_by_type.items():
                query = f"""
                UNWIND $rows AS row
                MATCH (s {{id: row.src_id}})
                MATCH (t {{id: row.tgt_id}})
                MERGE (s)-[r:`{typ}` {{id: row.id}}]->(t)
                ON CREATE SET r.created_at_utc = $created_at
                SET r.evidence_confidence = coalesce(row.evidence_confidence, 'abgeleitet'),
                    r.evidence_basis = row.evidence_basis,
                    r.evidence_url = row.evidence_url,
                    r.review_run = $run,
                    r.import_source_file = $source_file,
                    r.import_source_slice = 'PRIORITY_DEEPER_KEEPALL',
                    r.source_resolution_status = 'url_backed_candidate',
                    r.source_status = 'candidate',
                    r.source_status_reason = 'imported_from_reviewed_url_backed_payload'
                RETURN count(r) AS n
                """
                compact_rows = [
                    {
                        "id": row["id"],
                        "src_id": row["src_id"],
                        "tgt_id": row["tgt_id"],
                        "evidence_url": row["evidence_url"],
                        "evidence_basis": row["evidence_basis"],
                        "evidence_confidence": row["props"].get("evidence_confidence"),
                    }
                    for row in rows
                ]
                touched = session.run(
                    query,
                    rows=compact_rows,
                    created_at=created_at,
                    run=RUN,
                    source_file=str(SOURCE_JSON),
                ).single()["n"]
                rel_counter[typ] += touched

            post = session.run(
                """
                MATCH ()-[r {review_run: $run}]->()
                RETURN count(r) AS n, collect(DISTINCT type(r)) AS types
                """,
                run=RUN,
            ).single()
            missing_r_ids = session.run(
                """
                MATCH ()-[r {review_run: $run}]->()
                WHERE r.id IS NULL
                RETURN count(r) AS n
                """,
                run=RUN,
            ).single()["n"]
            missing_endpoint_count = session.run(
                """
                MATCH (n {source_scope: $run})
                RETURN count(n) AS n
                """,
                run=RUN,
            ).single()["n"]

            report = {
                "run": RUN,
                "source_json": str(SOURCE_JSON),
                "selected_edges": len(selected),
                "imported_relationships_with_review_run": post["n"],
                "relationship_types": sorted(post["types"]),
                "relationship_counts": dict(rel_counter),
                "created_endpoint_nodes": missing_endpoint_count,
                "created_endpoint_node_labels": dict(node_label_counter),
                "missing_relationship_ids": missing_r_ids,
                "skipped": dict(skipped),
            }
            IMPORT_REPORT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
