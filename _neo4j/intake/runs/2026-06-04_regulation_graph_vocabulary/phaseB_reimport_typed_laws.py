"""Phase B: re-import typed law nodes (Variant B, 11-label taxonomy).

Dry-run by default. Commit mode:
  1. snapshots NF property arrays and overlay target reltypes,
  2. MERGEs 91 typed law nodes (multi-label from Regulierungsfrage mapping),
  3. creates GESTUETZT_AUF_REGELWERK + GILT_IN_LAND from vocab_edges.csv,
  4. archives Variant A arrays on Nachweisforderung, then removes active copies.

Does NOT modify TRIGGERS_REGULIERUNGSFRAGE / ERFORDERT_NACHWEIS edges.
Does NOT create :Regelwerk nodes or BETRIFFT_* component edges.

Usage:
  python phaseB_reimport_typed_laws.py
  python phaseB_reimport_typed_laws.py --commit
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
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

OUT = Path(__file__).resolve().parent
RUN = "regulation_graph_vocab_2026_06_04_phaseB"
NOW = datetime.now(timezone.utc).isoformat()

spec = importlib.util.spec_from_file_location("bvg", OUT / "build_vocabulary_graph.py")
bvg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bvg)
REGELWERK: list[dict[str, Any]] = bvg.REGELWERK

DROPPED_NF = {
    "nf_mikrobielle_belastung_check",
    "nf_pak_check",
    "nf_radonmessung",
    "nf_voc_emissionsnachweis",
    "nf_kmf_check",
    "nf_pcb_check",
}
FOLD_NF_TARGET = "nf_schadstoffpruefung"

RF_TO_LABEL = {
    "rf_reusedokumentationfrage": "ReuseDokumentationsrecht",
    "rf_rueckbau_und_bauteilernte_frage": "RueckbauUndAbbruchrecht",
    "rf_bauproduktstatus_frage": "Bauproduktrecht",
    "rf_tragwerkssicherheit_frage": "Tragwerksrecht",
    "rf_brandschutz_frage": "Brandschutzrecht",
    "rf_bauphysik_frage": "Bauphysikrecht",
    "rf_schadstoff_frage": "Schadstoffrecht",
    "rf_hygiene_elektro_funktion_frage": "HygieneElektroFunktionsrecht",
    "rf_genehmigungs_frage": "Genehmigungsrecht",
    "rf_haftung_gewaehrleistung_frage": "Haftungsrecht",
    "rf_umweltvertraeglichkeit_oekobilanz_frage": "UmweltUndOekobilanzrecht",
}
ALLOWED_LAW_LABELS = set(RF_TO_LABEL.values())
TARGET_RELTYPES = ["GESTUETZT_AUF_REGELWERK", "GILT_IN_LAND"]


def normalize_nf(node_id: str) -> str:
    return FOLD_NF_TARGET if node_id in DROPPED_NF else node_id


def as_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def law_labels(rw: dict[str, Any]) -> list[str]:
    labels = sorted({RF_TO_LABEL[rf] for rf in rw.get("rf", []) if rf in RF_TO_LABEL})
    if not labels:
        raise ValueError(f"no labels for {rw['id']}")
    return labels


def label_clause(labels: list[str]) -> str:
    for label in labels:
        if label not in ALLOWED_LAW_LABELS:
            raise ValueError(f"invalid label {label}")
    return ":".join(labels)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def build_law_nodes() -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for rw in sorted(REGELWERK, key=lambda item: item["id"]):
        labels = law_labels(rw)
        nodes.append(
            {
                "id": rw["id"],
                "labels": labels,
                "name": rw["name"],
                "source_url": rw["url"],
                "source_quote": rw.get("quote"),
                "evidence_status": rw.get("status", "rule_documented"),
                "confidence": rw.get("conf"),
                "rechtsbereiche": labels,
            }
        )
    return nodes


def dedupe_edges(rows: list[dict[str, Any]], key_fn) -> tuple[list[dict[str, Any]], int]:
    best: dict[tuple[Any, ...], dict[str, Any]] = {}
    dropped = 0
    for row in rows:
        key = key_fn(row)
        existing = best.get(key)
        if existing is None:
            best[key] = row
            continue
        dropped += 1
        if (row.get("confidence") or 0) >= (existing.get("confidence") or 0):
            best[key] = row
    return sorted(best.values(), key=lambda r: (r["edge_type"], r["from_id"], r["to_id"])), dropped


def build_overlay_edges() -> tuple[list[dict[str, Any]], dict[str, int]]:
    raw: list[dict[str, Any]] = []
    stats = Counter()
    for row in load_csv(OUT / "vocab_edges.csv"):
        edge_type = row["edge_type"]
        if edge_type not in TARGET_RELTYPES:
            continue
        from_id = row["from_node_id"]
        to_id = row["to_node_id"]
        if edge_type == "GESTUETZT_AUF_REGELWERK":
            from_id = normalize_nf(from_id)
        raw.append(
            {
                "edge_type": edge_type,
                "from_id": from_id,
                "to_id": to_id,
                "evidence_status": row.get("evidence_status") or "rule_documented",
                "source_url": row.get("source_url") or None,
                "source_quote": row.get("source_quote") or None,
                "applicability_reason": row.get("applicability_reason") or "",
                "confidence": as_float(row.get("confidence")),
            }
        )
        stats[f"raw_{edge_type}"] += 1

    gest, gest_dropped = dedupe_edges(
        [r for r in raw if r["edge_type"] == "GESTUETZT_AUF_REGELWERK"],
        lambda r: (r["from_id"], r["to_id"]),
    )
    gilt, gilt_dropped = dedupe_edges(
        [r for r in raw if r["edge_type"] == "GILT_IN_LAND"],
        lambda r: (r["from_id"], r["to_id"]),
    )
    edges = gest + gilt
    stats["deduped_GESTUETZT_AUF_REGELWERK"] = len(gest)
    stats["deduped_GILT_IN_LAND"] = len(gilt)
    stats["dropped_duplicate_gest"] = gest_dropped
    stats["dropped_duplicate_gilt"] = gilt_dropped
    return edges, dict(stats)


def snapshot(session, path: Path) -> dict[str, int]:
    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "nachweisforderung_properties": [
            r.data()
            for r in session.run(
                """
                MATCH (nf:Nachweisforderung)
                WHERE nf.rechtsgrundlagen IS NOT NULL
                   OR nf.rechtsgrundlagen_urls IS NOT NULL
                   OR nf.jurisdiktion IS NOT NULL
                RETURN nf.id AS id, properties(nf) AS properties
                ORDER BY nf.id
                """
            )
        ],
        "relationships": [
            r.data()
            for r in session.run(
                """
                MATCH (a)-[rel]->(b)
                WHERE type(rel) IN $reltypes
                RETURN elementId(rel) AS element_id,
                       type(rel) AS type,
                       a.id AS from_id,
                       labels(a) AS from_labels,
                       b.id AS to_id,
                       labels(b) AS to_labels,
                       properties(rel) AS properties
                ORDER BY type(rel), elementId(rel)
                """,
                reltypes=TARGET_RELTYPES,
            )
        ],
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return {
        "nachweisforderung_with_arrays": len(payload["nachweisforderung_properties"]),
        "relationships": len(payload["relationships"]),
    }


def graph_counts(session) -> dict[str, int]:
    return {
        "nodes": session.run("MATCH (n) RETURN count(n) AS c").single()["c"],
        "relationships": session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"],
        "labels": session.run("MATCH (n) UNWIND labels(n) AS l RETURN count(DISTINCT l) AS c").single()["c"],
        "reltypes": session.run("CALL db.relationshipTypes() YIELD relationshipType RETURN count(*) AS c").single()["c"],
    }


def counts(session) -> dict[str, Any]:
    law_label_counts = {
        label: session.run(f"MATCH (n:`{label}`) RETURN count(n) AS c").single()["c"]
        for label in sorted(ALLOWED_LAW_LABELS)
    }
    return {
        "graph": graph_counts(session),
        "law_label_counts": law_label_counts,
        "Regelwerk": session.run("MATCH (n:Regelwerk) RETURN count(n) AS c").single()["c"],
        "typed_law_nodes": session.run(
            "MATCH (n) WHERE any(l IN labels(n) WHERE l IN $labels) RETURN count(DISTINCT n) AS c",
            labels=sorted(ALLOWED_LAW_LABELS),
        ).single()["c"],
        "GESTUETZT_AUF_REGELWERK": session.run(
            "MATCH ()-[r:GESTUETZT_AUF_REGELWERK]->() RETURN count(r) AS c"
        ).single()["c"],
        "GILT_IN_LAND": session.run("MATCH ()-[r:GILT_IN_LAND]->() RETURN count(r) AS c").single()["c"],
        "TRIGGERS_REGULIERUNGSFRAGE": session.run(
            "MATCH ()-[r:TRIGGERS_REGULIERUNGSFRAGE]->() RETURN count(r) AS c"
        ).single()["c"],
        "ERFORDERT_NACHWEIS": session.run("MATCH ()-[r:ERFORDERT_NACHWEIS]->() RETURN count(r) AS c").single()["c"],
        "NF_with_active_rechtsgrundlagen": session.run(
            "MATCH (n:Nachweisforderung) WHERE n.rechtsgrundlagen IS NOT NULL RETURN count(n) AS c"
        ).single()["c"],
    }


def validate(session, law_nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> list[str]:
    problems: list[str] = []
    live_nf = {r["id"] for r in session.run("MATCH (n:Nachweisforderung) RETURN n.id AS id")}
    live_land = {r["id"] for r in session.run("MATCH (n:Land) RETURN n.id AS id")}
    rw_ids = {n["id"] for n in law_nodes}

    missing_nf = sorted({e["from_id"] for e in edges if e["edge_type"] == "GESTUETZT_AUF_REGELWERK"} - live_nf)
    if missing_nf:
        problems.append(f"missing Nachweisforderung targets: {missing_nf}")

    missing_rw = sorted({e["to_id"] for e in edges if e["edge_type"] == "GESTUETZT_AUF_REGELWERK"} - rw_ids)
    if missing_rw:
        problems.append(f"unknown law ids in overlay: {missing_rw}")

    missing_rw_from = sorted({e["from_id"] for e in edges if e["edge_type"] == "GILT_IN_LAND"} - rw_ids)
    if missing_rw_from:
        problems.append(f"unknown law ids in GILT_IN_LAND: {missing_rw_from}")

    missing_land = sorted({e["to_id"] for e in edges if e["edge_type"] == "GILT_IN_LAND"} - live_land)
    if missing_land:
        problems.append(f"missing Land targets: {missing_land}")

    rw_by_name = {rw["name"]: rw["id"] for rw in REGELWERK}
    gest_pairs = {(e["from_id"], e["to_id"]) for e in edges if e["edge_type"] == "GESTUETZT_AUF_REGELWERK"}
    prop_pairs: set[tuple[str, str]] = set()
    unmatched_names: list[str] = []
    for row in session.run(
        """
        MATCH (nf:Nachweisforderung)
        UNWIND coalesce(nf.rechtsgrundlagen, []) AS rg_name
        RETURN nf.id AS nf_id, rg_name
        """
    ):
        rw_id = rw_by_name.get(row["rg_name"])
        if rw_id:
            prop_pairs.add((row["nf_id"], rw_id))
        else:
            unmatched_names.append(row["rg_name"])

    if unmatched_names:
        problems.append(f"unmatched rechtsgrundlagen names: {sorted(set(unmatched_names))[:20]}")
    only_props = sorted(prop_pairs - gest_pairs)
    only_gest = sorted(gest_pairs - prop_pairs)
    if only_props:
        problems.append(f"property pairs without planned GESTUETZT edge ({len(only_props)}): {only_props[:10]}")
    if only_gest:
        problems.append(f"planned GESTUETZT pairs without property backing ({len(only_gest)}): {only_gest[:10]}")

    if session.run("MATCH (n:Regelwerk) RETURN count(n) AS c").single()["c"]:
        problems.append("Regelwerk nodes already exist")

    existing_gest = session.run("MATCH ()-[r:GESTUETZT_AUF_REGELWERK]->() RETURN count(r) AS c").single()["c"]
    existing_gilt = session.run("MATCH ()-[r:GILT_IN_LAND]->() RETURN count(r) AS c").single()["c"]
    if existing_gest or existing_gilt:
        problems.append(f"overlay reltypes already present: GESTUETZT={existing_gest}, GILT_IN_LAND={existing_gilt}")

    return problems


def merge_law_node(session, node: dict[str, Any]) -> None:
    labels = label_clause(node["labels"])
    session.run(
        f"""
        MERGE (n:{labels} {{id:$id}})
        SET n.name = $name,
            n.source_url = $source_url,
            n.source_quote = $source_quote,
            n.evidence_status = $evidence_status,
            n.confidence = $confidence,
            n.rechtsbereiche = $rechtsbereiche,
            n.source_scope = $run,
            n.review_run = $run,
            n.updated_at_utc = $now
        """,
        **node,
        run=RUN,
        now=NOW,
    ).consume()


def merge_overlay_edge(session, edge: dict[str, Any]) -> None:
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
            r.confidence = $confidence,
            r.updated_at_utc = $now
        """,
        from_id=edge["from_id"],
        to_id=edge["to_id"],
        run=RUN,
        evidence_status=edge["evidence_status"],
        source_url=edge["source_url"],
        source_quote=edge["source_quote"],
        applicability_reason=edge["applicability_reason"],
        confidence=edge["confidence"],
        now=NOW,
    ).consume()


def archive_and_remove_nf_arrays(session) -> dict[str, int]:
    archived = session.run(
        """
        MATCH (nf:Nachweisforderung)
        WHERE nf.rechtsgrundlagen IS NOT NULL
           OR nf.rechtsgrundlagen_urls IS NOT NULL
           OR nf.jurisdiktion IS NOT NULL
        SET nf.legacy_rechtsgrundlagen_from_variant_a = coalesce(nf.rechtsgrundlagen, []),
            nf.legacy_rechtsgrundlagen_urls_from_variant_a = coalesce(nf.rechtsgrundlagen_urls, []),
            nf.legacy_jurisdiktion_from_variant_a = coalesce(nf.jurisdiktion, []),
            nf.phaseB_property_migration = $run,
            nf.phaseB_updated_at_utc = $now
        REMOVE nf.rechtsgrundlagen, nf.rechtsgrundlagen_urls, nf.jurisdiktion
        RETURN count(nf) AS c
        """,
        run=RUN,
        now=NOW,
    ).single()["c"]
    return {"nachweisforderung_archived_and_cleared": archived}


def acceptance(session) -> dict[str, Any]:
    duplicate_gest = session.run(
        """
        MATCH (a)-[r:GESTUETZT_AUF_REGELWERK]->(b)
        WITH a,b,count(r) AS c WHERE c>1 RETURN count(*) AS c
        """
    ).single()["c"]
    duplicate_gilt = session.run(
        """
        MATCH (a)-[r:GILT_IN_LAND]->(b)
        WITH a,b,count(r) AS c WHERE c>1 RETURN count(*) AS c
        """
    ).single()["c"]
    parity_gaps = session.run(
        """
        MATCH (nf:Nachweisforderung)
        UNWIND coalesce(nf.legacy_rechtsgrundlagen_from_variant_a, []) AS rg_name
        OPTIONAL MATCH (rw {name: rg_name})
        WHERE any(l IN labels(rw) WHERE l IN $labels)
        WITH nf, rg_name, rw
        OPTIONAL MATCH (nf)-[rel:GESTUETZT_AUF_REGELWERK]->(rw)
        WITH count(*) AS total, count(rel) AS matched
        RETURN total, matched
        """,
        labels=sorted(ALLOWED_LAW_LABELS),
    ).single()
    return {
        **counts(session),
        "duplicate_GESTUETZT_pairs": duplicate_gest,
        "duplicate_GILT_IN_LAND_pairs": duplicate_gilt,
        "legacy_property_to_edge_total": parity_gaps["total"],
        "legacy_property_to_edge_matched": parity_gaps["matched"],
    }


def run(commit: bool) -> dict[str, Any]:
    law_nodes = build_law_nodes()
    edges, edge_stats = build_overlay_edges()
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "phase": "phaseB_reimport_typed_laws",
        "variant": "B_option_1_11_labels",
        "database": database,
        "commit": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "planned": {
            "law_nodes": len(law_nodes),
            "multi_label_law_nodes": sum(1 for n in law_nodes if len(n["labels"]) > 1),
            "edges_by_type": dict(Counter(e["edge_type"] for e in edges)),
            "edge_stats": edge_stats,
            "dropped_nf_fold_target": FOLD_NF_TARGET,
            "dropped_nf_ids": sorted(DROPPED_NF),
        },
    }
    with driver.session(database=database) as session:
        report["before"] = counts(session)
        problems = validate(session, law_nodes, edges)
        report["validation_problems"] = problems
        report["validation_problem_count"] = len(problems)
        if problems:
            driver.close()
            return report
        if commit:
            report["snapshot"] = snapshot(session, OUT / "phaseB_before.json")
            for node in law_nodes:
                merge_law_node(session, node)
            for edge in edges:
                merge_overlay_edge(session, edge)
            report["applied"] = {
                "law_nodes_written": len(law_nodes),
                "edges_written": len(edges),
                "nf_property_archive": archive_and_remove_nf_arrays(session),
            }
            report["after"] = counts(session)
            report["acceptance"] = acceptance(session)
    driver.close()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    report = run(args.commit)
    path = OUT / ("phaseB_report.json" if args.commit else "phaseB_dry_run_report.json")
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True, default=str))
    return 1 if report.get("validation_problem_count") else 0


if __name__ == "__main__":
    raise SystemExit(main())
