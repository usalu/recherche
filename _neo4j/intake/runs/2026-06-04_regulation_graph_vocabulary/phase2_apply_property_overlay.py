"""Phase 2: apply the regulation overlay with property-only evidence.

Dry-run by default. Commit mode:
  1. creates only Regulierungsfrage + surviving Nachweisforderung nodes,
  2. maps the six sparse Nachweisforderung ids to nf_schadstoffpruefung,
  3. creates only TRIGGERS_REGULIERUNGSFRAGE / ERFORDERT_NACHWEIS edges,
  4. folds Regelwerk citations into Nachweisforderung properties.

No Regelwerk/Quelle nodes and no GILT_IN_LAND/GESTUETZT_AUF_REGELWERK/
UNTERLIEGT_REGELWERK edges are created.

Usage:
  python phase2_apply_property_overlay.py
  python phase2_apply_property_overlay.py --commit
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[4]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402
from build_vocabulary_graph import (  # noqa: E402
    NACHWEISFORDERUNG,
    REGELWERK,
    REGULIERUNGSFRAGE,
    RUN as BASE_RUN,
    expand_land,
)

OUT = Path(__file__).resolve().parent
RUN = BASE_RUN
NOW = datetime.now(timezone.utc).isoformat()

DROPPED_NF = {
    "nf_mikrobielle_belastung_check",
    "nf_pak_check",
    "nf_radonmessung",
    "nf_voc_emissionsnachweis",
    "nf_kmf_check",
    "nf_pcb_check",
}
FOLD_NF_TARGET = "nf_schadstoffpruefung"
ALLOWED_EDGE_TYPES = {"TRIGGERS_REGULIERUNGSFRAGE", "ERFORDERT_NACHWEIS"}


def as_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def dedupe(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not value:
            continue
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        out.append(text)
    return out


def normalize_nf(node_id: str) -> str:
    return FOLD_NF_TARGET if node_id in DROPPED_NF else node_id


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def build_nodes() -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for node_id, name in REGULIERUNGSFRAGE.items():
        nodes.append({"id": node_id, "label": "Regulierungsfrage", "name": name})
    for node_id, name in NACHWEISFORDERUNG.items():
        if node_id in DROPPED_NF:
            continue
        nodes.append({"id": node_id, "label": "Nachweisforderung", "name": name})
    return nodes


def build_standard_props() -> dict[str, dict[str, list[str]]]:
    refs: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: {
            "rechtsgrundlagen": [],
            "rechtsgrundlagen_urls": [],
            "jurisdiktion": [],
        }
    )
    for rw in sorted(REGELWERK, key=lambda item: item["id"]):
        nf_ids = {normalize_nf(nf_id) for nf_id in rw["nf"]}
        lands = expand_land(rw["land"])
        for nf_id in nf_ids:
            refs[nf_id]["rechtsgrundlagen"].append(rw["name"])
            refs[nf_id]["rechtsgrundlagen_urls"].append(rw["url"])
            refs[nf_id]["jurisdiktion"].extend(lands)
    return {nf_id: {k: dedupe(v) for k, v in props.items()} for nf_id, props in refs.items()}


def edge_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (row["from_node_id"], row["edge_type"], row["to_node_id"])


def normalize_edge(row: dict[str, str], source: str) -> dict[str, Any] | None:
    edge_type = row["edge_type"]
    if edge_type not in ALLOWED_EDGE_TYPES:
        return None
    to_id = normalize_nf(row["to_node_id"])
    if edge_type == "TRIGGERS_REGULIERUNGSFRAGE" and not to_id.startswith("rf_"):
        return None
    if edge_type == "ERFORDERT_NACHWEIS" and not to_id.startswith("nf_"):
        return None
    return {
        "from_node_id": row["from_node_id"],
        "edge_type": edge_type,
        "to_node_id": to_id,
        "evidence_status": row.get("evidence_status") or "rule_documented",
        "source_url": row.get("source_url") or None,
        "source_quote": row.get("source_quote") or None,
        "applicability_reason": row.get("applicability_reason") or "",
        "support_rules": int(row.get("support_rules") or 1),
        "confidence": as_float(row.get("confidence")),
        "input_source": source,
    }


def build_edges() -> tuple[list[dict[str, Any]], dict[str, int]]:
    raw: list[dict[str, Any]] = []
    counters = Counter()
    for row in load_csv(OUT / "vocab_edges.csv"):
        edge = normalize_edge(row, "vocab_edges.csv")
        if edge:
            raw.append(edge)
        elif row["edge_type"] in {"GILT_IN_LAND", "GESTUETZT_AUF_REGELWERK", "BETRIFFT_MATERIAL", "BETRIFFT_BAUTEILTYP"}:
            counters[f"folded_or_skipped_{row['edge_type']}"] += 1
    for row in load_csv(OUT / "anchor_edges.csv"):
        if row["edge_type"] == "UNTERLIEGT_REGELWERK":
            counters["folded_or_skipped_UNTERLIEGT_REGELWERK"] += 1
            continue
        edge = normalize_edge(row, "anchor_edges.csv")
        if edge:
            raw.append(edge)

    best: dict[tuple[str, str, str], dict[str, Any]] = {}
    for edge in raw:
        key = edge_key(edge)
        existing = best.get(key)
        if existing is None or (edge["confidence"] or 0) > (existing["confidence"] or 0):
            best[key] = edge
        elif existing is not None:
            existing["support_rules"] = max(existing.get("support_rules", 1), edge.get("support_rules", 1))
    counters["raw_allowed_edges"] = len(raw)
    counters["deduped_edges"] = len(best)
    return sorted(best.values(), key=lambda e: (e["edge_type"], e["from_node_id"], e["to_node_id"])), dict(counters)


def snapshot_counts(session) -> dict[str, Any]:
    labels = [
        "Regulierungsfrage",
        "Nachweisforderung",
        "Regelwerk",
        "Quelle",
    ]
    reltypes = [
        "TRIGGERS_REGULIERUNGSFRAGE",
        "ERFORDERT_NACHWEIS",
        "GILT_IN_LAND",
        "GESTUETZT_AUF_REGELWERK",
        "UNTERLIEGT_REGELWERK",
    ]
    out: dict[str, Any] = {
        "nodes": session.run("MATCH (n) RETURN count(n) AS c").single()["c"],
        "relationships": session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"],
        "labels": {},
        "reltypes": {},
    }
    for label in labels:
        out["labels"][label] = session.run(f"MATCH (n:`{label}`) RETURN count(n) AS c").single()["c"]
    for reltype in reltypes:
        out["reltypes"][reltype] = session.run(f"MATCH ()-[r:`{reltype}`]->() RETURN count(r) AS c").single()["c"]
    return out


def validate(session, nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> list[str]:
    problems: list[str] = []
    node_ids = {n["id"] for n in nodes}
    for edge in edges:
        if edge["to_node_id"] not in node_ids:
            problems.append(f"edge target not in Phase 2 vocab nodes: {edge_key(edge)}")
    source_ids = sorted({e["from_node_id"] for e in edges if e["from_node_id"] not in node_ids})
    if source_ids:
        found = {
            r["id"]
            for r in session.run(
                "MATCH (n) WHERE n.id IN $ids RETURN n.id AS id",
                ids=source_ids,
            )
        }
        for missing in sorted(set(source_ids) - found):
            problems.append(f"missing live source node: {missing}")
    for edge in edges:
        if not edge.get("source_url"):
            problems.append(f"edge without source_url: {edge_key(edge)}")
    return problems


def merge_node(session, node: dict[str, Any], standards: dict[str, dict[str, list[str]]]) -> None:
    label = node["label"]
    props = standards.get(node["id"], {})
    session.run(
        f"""
        MERGE (n:`{label}` {{id:$id}})
        SET n.name = $name,
            n.source_scope = $run,
            n.review_run = $run,
            n.updated_at_utc = $now
        WITH n
        SET n.rechtsgrundlagen =
            coalesce(n.rechtsgrundlagen, []) + [x IN $rechtsgrundlagen WHERE NOT x IN coalesce(n.rechtsgrundlagen, [])],
            n.rechtsgrundlagen_urls =
            coalesce(n.rechtsgrundlagen_urls, []) + [x IN $rechtsgrundlagen_urls WHERE NOT x IN coalesce(n.rechtsgrundlagen_urls, [])],
            n.jurisdiktion =
            coalesce(n.jurisdiktion, []) + [x IN $jurisdiktion WHERE NOT x IN coalesce(n.jurisdiktion, [])]
        """,
        id=node["id"],
        name=node["name"],
        run=RUN,
        now=NOW,
        rechtsgrundlagen=props.get("rechtsgrundlagen", []),
        rechtsgrundlagen_urls=props.get("rechtsgrundlagen_urls", []),
        jurisdiktion=props.get("jurisdiktion", []),
    ).consume()


def merge_edge(session, edge: dict[str, Any]) -> None:
    reltype = edge["edge_type"]
    session.run(
        f"""
        MATCH (a {{id:$from_id}})
        MATCH (b {{id:$to_id}})
        MERGE (a)-[r:`{reltype}`]->(b)
        SET r.review_run = $run,
            r.evidence_status = $evidence_status,
            r.source_url = $source_url,
            r.source_quote = $source_quote,
            r.applicability_reason = $applicability_reason,
            r.support_rules = $support_rules,
            r.confidence = $confidence,
            r.input_source = $input_source,
            r.updated_at_utc = $now
        """,
        from_id=edge["from_node_id"],
        to_id=edge["to_node_id"],
        run=RUN,
        evidence_status=edge["evidence_status"],
        source_url=edge["source_url"],
        source_quote=edge["source_quote"],
        applicability_reason=edge["applicability_reason"],
        support_rules=edge["support_rules"],
        confidence=edge["confidence"],
        input_source=edge["input_source"],
        now=NOW,
    ).consume()


def acceptance(session) -> dict[str, Any]:
    duplicate_arrays = session.run(
        """
        MATCH (n:Nachweisforderung)
        WHERE size(coalesce(n.rechtsgrundlagen_urls, [])) <>
              size([x IN coalesce(n.rechtsgrundlagen_urls, []) WHERE single(y IN coalesce(n.rechtsgrundlagen_urls, []) WHERE y = x)])
        RETURN count(n) AS c
        """
    ).single()["c"]
    edge_without_source = session.run(
        """
        MATCH ()-[r:TRIGGERS_REGULIERUNGSFRAGE|ERFORDERT_NACHWEIS]->()
        WHERE r.review_run = $run AND r.source_url IS NULL
        RETURN count(r) AS c
        """,
        run=RUN,
    ).single()["c"]
    duplicate_edges = session.run(
        """
        MATCH (a)-[r:TRIGGERS_REGULIERUNGSFRAGE|ERFORDERT_NACHWEIS]->(b)
        WITH a,b,type(r) AS t,count(r) AS c
        WHERE c > 1
        RETURN count(*) AS c
        """
    ).single()["c"]
    return {
        "Regulierungsfrage": session.run("MATCH (n:Regulierungsfrage) RETURN count(n) AS c").single()["c"],
        "Nachweisforderung": session.run("MATCH (n:Nachweisforderung) RETURN count(n) AS c").single()["c"],
        "Regelwerk": session.run("MATCH (n:Regelwerk) RETURN count(n) AS c").single()["c"],
        "Quelle": session.run("MATCH (n:Quelle) RETURN count(n) AS c").single()["c"],
        "GESTUETZT_AUF_REGELWERK": session.run("MATCH ()-[r:GESTUETZT_AUF_REGELWERK]->() RETURN count(r) AS c").single()["c"],
        "UNTERLIEGT_REGELWERK": session.run("MATCH ()-[r:UNTERLIEGT_REGELWERK]->() RETURN count(r) AS c").single()["c"],
        "GILT_IN_LAND_edges_from_regelwerk_model": session.run(
            "MATCH (n:Regelwerk)-[r:GILT_IN_LAND]->() RETURN count(r) AS c"
        ).single()["c"],
        "review_run_edges": session.run(
            "MATCH ()-[r {review_run:$run}]->() RETURN count(r) AS c",
            run=RUN,
        ).single()["c"],
        "edge_without_source_url": edge_without_source,
        "duplicate_regulation_edges": duplicate_edges,
        "duplicate_rechtsgrundlagen_urls_arrays": duplicate_arrays,
    }


def run(commit: bool) -> dict[str, Any]:
    nodes = build_nodes()
    standards = build_standard_props()
    edges, edge_stats = build_edges()
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "phase": "phase2_apply_property_overlay",
        "database": database,
        "commit": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "planned": {
            "nodes_total": len(nodes),
            "regulierungsfrage_nodes": sum(1 for n in nodes if n["label"] == "Regulierungsfrage"),
            "nachweisforderung_nodes": sum(1 for n in nodes if n["label"] == "Nachweisforderung"),
            "dropped_nachweisforderung_mapped_to_schadstoffpruefung": sorted(DROPPED_NF),
            "edges_by_type": dict(Counter(e["edge_type"] for e in edges)),
            "edge_stats": edge_stats,
            "nachweisforderung_with_standard_properties": len(standards),
        },
    }
    with driver.session(database=database) as session:
        report["before"] = snapshot_counts(session)
        problems = validate(session, nodes, edges)
        report["validation_problems"] = problems[:100]
        report["validation_problem_count"] = len(problems)
        if problems:
            driver.close()
            return report
        if commit:
            (OUT / "phase2_before.json").write_text(
                json.dumps(report["before"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            for node in nodes:
                merge_node(session, node, standards)
            for edge in edges:
                merge_edge(session, edge)
            report["after"] = snapshot_counts(session)
            report["acceptance"] = acceptance(session)
    driver.close()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    report = run(args.commit)
    report_path = OUT / ("phase2_report.json" if args.commit else "phase2_dry_run_report.json")
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 1 if report.get("validation_problem_count") else 0


if __name__ == "__main__":
    raise SystemExit(main())
