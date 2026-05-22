"""Phase 8: relationship-type deduplication and naming normalization.

Dry-run by default. Commit mode:
  1. snapshots Phase-8 target relationships,
  2. demotes ReuseRule applicability edges to properties,
  3. rewires ANGEWENDET_AUF into existing HAT_METHODE direction,
  4. merges duplicate defect/building edge types,
  5. renames surviving English reltypes to German names.

Usage:
  python phase8_reltype_dedup_normalize.py
  python phase8_reltype_dedup_normalize.py --commit
"""

from __future__ import annotations

import argparse
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
RUN = "regulation_graph_vocab_2026_06_04_phase8"
NOW = datetime.now(timezone.utc).isoformat()

APPLICABILITY_RELTYPES = ["APPLIES_IN", "APPLIES_TO", "RELEVANT_FOR"]
MERGE_RELTYPES = [
    "ANGEWENDET_AUF",
    "HAT_DEFEKT_BEFUND",
    "NUTZT_BAUWERK",
    "HAS_BAUWERK",
    "HAS_RISK_POLLUTANT",
    "FROM_DONOR",
    "INTO_RECEIVER",
    "BUILT_IN_ERA",
    "REQUIRES_VERIFICATION_FOR",
]
TARGET_RELTYPES = APPLICABILITY_RELTYPES + MERGE_RELTYPES

RENAME_SAME_DIRECTION = {
    "HAT_DEFEKT_BEFUND": "HAT_DEFEKT",
    "NUTZT_BAUWERK": "HAT_BAUWERK",
    "HAS_BAUWERK": "HAT_BAUWERK",
    "HAS_RISK_POLLUTANT": "HAT_SCHADSTOFFRISIKO",
    "FROM_DONOR": "AUS_SPENDER",
    "INTO_RECEIVER": "IN_EMPFANGSOBJEKT",
    "BUILT_IN_ERA": "GEBAUT_IN_ERA",
    "REQUIRES_VERIFICATION_FOR": "ERFORDERT_SCHADSTOFFPRUEFUNG",
}

APPLICABILITY_PROPS = {
    "APPLIES_IN": ("applies_in_land_ids", "applies_in_land_names"),
    "APPLIES_TO": ("applies_to_material_ids", "applies_to_material_names"),
    "RELEVANT_FOR": ("relevant_for_project_ids", "relevant_for_project_names"),
}


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v is not None and str(v).strip()]
    text = str(value).strip()
    return [text] if text else []


def name_from_props(props: dict[str, Any], fallback: str | None = None) -> str:
    for key in ("name", "title", "titel", "id"):
        value = props.get(key)
        if value:
            return str(value)
    return str(fallback or "")


def snapshot(session, path: Path) -> dict[str, int]:
    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
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
                       properties(a) AS from_properties,
                       b.id AS to_id,
                       labels(b) AS to_labels,
                       properties(b) AS to_properties,
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
    return {"relationships": len(payload["relationships"])}


def count_reltype(session, reltype: str) -> int:
    return session.run(f"MATCH ()-[r:`{reltype}`]->() RETURN count(r) AS c").single()["c"]


def graph_counts(session) -> dict[str, int]:
    return {
        "nodes": session.run("MATCH (n) RETURN count(n) AS c").single()["c"],
        "relationships": session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"],
        "labels": session.run("MATCH (n) UNWIND labels(n) AS l RETURN count(DISTINCT l) AS c").single()["c"],
        "reltypes": session.run("CALL db.relationshipTypes() YIELD relationshipType RETURN count(*) AS c").single()["c"],
    }


def counts(session) -> dict[str, Any]:
    reltypes = set(TARGET_RELTYPES) | set(RENAME_SAME_DIRECTION.values()) | {"HAT_METHODE", "HAT_DEFEKT"}
    return {
        "graph": graph_counts(session),
        "reltypes": {reltype: count_reltype(session, reltype) for reltype in sorted(reltypes)},
    }


def collect_applicability_updates(session) -> tuple[dict[str, dict[str, set[str]]], dict[str, int]]:
    updates: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    stats = Counter()
    for reltype, (id_prop, name_prop) in APPLICABILITY_PROPS.items():
        for rec in session.run(
            f"""
            MATCH (rr:ReuseRule)-[rel:`{reltype}`]->(target)
            RETURN rr.id AS rr_id,
                   target.id AS target_id,
                   properties(target) AS target_props,
                   properties(rel) AS rel_props
            """
        ):
            rel_props = rec["rel_props"] or {}
            updates[rec["rr_id"]][id_prop].add(str(rec["target_id"]))
            updates[rec["rr_id"]][name_prop].add(name_from_props(rec["target_props"], rec["target_id"]))
            old_rel_id = rel_props.get("id")
            if old_rel_id:
                updates[rec["rr_id"]]["legacy_applicability_rel_ids"].add(str(old_rel_id))
            confidence = rel_props.get("confidence")
            if confidence is not None:
                updates[rec["rr_id"]]["legacy_applicability_confidences"].add(str(confidence))
            stats[reltype] += 1
    return updates, dict(stats)


def apply_property_updates(session, updates: dict[str, dict[str, set[str]]]) -> dict[str, int]:
    nodes_updated = 0
    values_written = 0
    for node_id, props in sorted(updates.items()):
        row = session.run("MATCH (n {id:$id}) RETURN properties(n) AS props", id=node_id).single()
        if row is None:
            continue
        current = row["props"]
        merged: dict[str, Any] = {"phase8_property_migration": RUN, "phase8_updated_at_utc": NOW}
        for key, values in props.items():
            out: list[str] = []
            seen: set[str] = set()
            for value in as_list(current.get(key)) + sorted(values):
                if value and value not in seen:
                    seen.add(value)
                    out.append(value)
            merged[key] = out
            values_written += len(out)
        session.run("MATCH (n {id:$id}) SET n += $props", id=node_id, props=merged).consume()
        nodes_updated += 1
    return {"nodes_updated": nodes_updated, "values_written_after_dedup": values_written}


def rows_for_reltype(session, reltype: str) -> list[dict[str, Any]]:
    return [
        rec.data()
        for rec in session.run(
            f"""
            MATCH (a)-[rel:`{reltype}`]->(b)
            RETURN elementId(rel) AS rel_eid,
                   elementId(a) AS from_eid,
                   elementId(b) AS to_eid,
                   properties(rel) AS props
            ORDER BY elementId(rel)
            """
        )
    ]


def merge_relationship(
    session,
    *,
    from_eid: str,
    to_eid: str,
    reltype: str,
    props: dict[str, Any],
    rel_eid: str,
    old_type: str,
) -> None:
    clean_props = dict(props or {})
    old_rel_id = clean_props.pop("id", None)
    session.run(
        f"""
        MATCH (a) WHERE elementId(a)=$from_eid
        MATCH (b) WHERE elementId(b)=$to_eid
        MERGE (a)-[new_rel:`{reltype}`]->(b)
        SET new_rel += $props,
            new_rel.review_run=$run,
            new_rel.updated_at_utc=$now,
            new_rel.merged_legacy_rel_ids =
              coalesce(new_rel.merged_legacy_rel_ids, []) +
              [x IN [$old_rel_id] WHERE x IS NOT NULL AND NOT x IN coalesce(new_rel.merged_legacy_rel_ids, [])],
            new_rel.merged_legacy_reltypes =
              coalesce(new_rel.merged_legacy_reltypes, []) +
              [x IN [$old_type] WHERE NOT x IN coalesce(new_rel.merged_legacy_reltypes, [])]
        WITH new_rel
        MATCH ()-[old_rel]->() WHERE elementId(old_rel)=$rel_eid
        DELETE old_rel
        """,
        from_eid=from_eid,
        to_eid=to_eid,
        rel_eid=rel_eid,
        props=clean_props,
        old_rel_id=old_rel_id,
        old_type=old_type,
        run=RUN,
        now=NOW,
    ).consume()


def apply_same_direction_renames(session) -> dict[str, int]:
    stats: dict[str, int] = {}
    for old_type, new_type in RENAME_SAME_DIRECTION.items():
        rows = rows_for_reltype(session, old_type)
        for row in rows:
            merge_relationship(
                session,
                from_eid=row["from_eid"],
                to_eid=row["to_eid"],
                reltype=new_type,
                props=row["props"],
                rel_eid=row["rel_eid"],
                old_type=old_type,
            )
        stats[f"{old_type}_to_{new_type}"] = len(rows)
    return stats


def apply_angewendet_auf(session) -> dict[str, int]:
    rows = rows_for_reltype(session, "ANGEWENDET_AUF")
    for row in rows:
        merge_relationship(
            session,
            from_eid=row["to_eid"],
            to_eid=row["from_eid"],
            reltype="HAT_METHODE",
            props=row["props"],
            rel_eid=row["rel_eid"],
            old_type="ANGEWENDET_AUF",
        )
    return {"ANGEWENDET_AUF_to_HAT_METHODE": len(rows)}


def delete_applicability_edges(session) -> dict[str, int]:
    stats: dict[str, int] = {}
    for reltype in APPLICABILITY_RELTYPES:
        stats[f"{reltype}_deleted"] = session.run(
            f"MATCH ()-[r:`{reltype}`]->() WITH count(r) AS c, collect(r) AS rels FOREACH (r IN rels | DELETE r) RETURN c"
        ).single()["c"]
    return stats


def planned(session) -> dict[str, Any]:
    updates, app_stats = collect_applicability_updates(session)
    rename_counts = {f"{old}_to_{new}": count_reltype(session, old) for old, new in RENAME_SAME_DIRECTION.items()}
    return {
        "applicability_edges_to_properties": app_stats,
        "reuse_rules_to_update": len(updates),
        "reuse_rule_property_values": sum(len(values) for props in updates.values() for values in props.values()),
        "ANGEWENDET_AUF_to_HAT_METHODE": count_reltype(session, "ANGEWENDET_AUF"),
        "same_direction_renames": rename_counts,
        "target_reltype_count_before": graph_counts(session)["reltypes"],
    }


def acceptance(session) -> dict[str, Any]:
    removed = {reltype: count_reltype(session, reltype) for reltype in TARGET_RELTYPES}
    duplicate_targets: dict[str, int] = {}
    for reltype in ["HAT_METHODE", "HAT_DEFEKT", "HAT_BAUWERK", "AUS_SPENDER", "IN_EMPFANGSOBJEKT"]:
        duplicate_targets[reltype] = session.run(
            f"MATCH (a)-[r:`{reltype}`]->(b) WITH a,b,count(r) AS c WHERE c>1 RETURN count(*) AS c"
        ).single()["c"]
    return {
        "removed_target_reltypes": removed,
        "new_reltypes": {reltype: count_reltype(session, reltype) for reltype in sorted(set(RENAME_SAME_DIRECTION.values()) | {"HAT_METHODE"})},
        "reuse_rules_with_applicability_props": session.run(
            """
            MATCH (rr:ReuseRule)
            WHERE rr.applies_in_land_ids IS NOT NULL
               OR rr.applies_to_material_ids IS NOT NULL
               OR rr.relevant_for_project_ids IS NOT NULL
            RETURN count(rr) AS c
            """
        ).single()["c"],
        "duplicate_target_pairs": duplicate_targets,
        "graph": graph_counts(session),
    }


def run(commit: bool) -> dict[str, Any]:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "phase": "phase8_reltype_dedup_normalize",
        "database": database,
        "commit": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    with driver.session(database=database) as session:
        updates, _ = collect_applicability_updates(session)
        report["before"] = counts(session)
        report["planned"] = planned(session)
        if commit:
            report["snapshot"] = snapshot(session, OUT / "phase8_before.json")
            report["applied"] = {
                "applicability_properties": apply_property_updates(session, updates),
                "applicability_edges_deleted": delete_applicability_edges(session),
                "angewendet_auf": apply_angewendet_auf(session),
                "same_direction_renames": apply_same_direction_renames(session),
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
    path = OUT / ("phase8_report.json" if args.commit else "phase8_dry_run_report.json")
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
