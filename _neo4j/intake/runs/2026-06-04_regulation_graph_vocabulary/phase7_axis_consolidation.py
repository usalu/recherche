"""Phase 7: consolidate duplicate axes and demote low-info vocabularies.

Dry-run by default. Commit mode:
  1. snapshots Phase-7 target labels/relationships,
  2. rewires Marktmodell to Beschaffungsweg,
  3. demotes Status/Layer/Bauteilebene/Wiederverwendungsort/Funktionswechsel/
     Tragwerksprinzip/Bauobjektklasse values to properties,
  4. optionally maps use-like Bauobjektklasse values to existing Nutzung nodes,
  5. removes the redundant Tool label from Software nodes,
  6. deletes retired vocabulary nodes and relationship types.

Usage:
  python phase7_axis_consolidation.py
  python phase7_axis_consolidation.py --commit
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
RUN = "regulation_graph_vocab_2026_06_04_phase7"
NOW = datetime.now(timezone.utc).isoformat()

TARGET_LABELS = [
    "Marktmodell",
    "Tragwerksprinzip",
    "Bauobjektklasse",
    "Layer",
    "Bauteilebene",
    "Wiederverwendungsort",
    "Funktionswechsel",
    "Tool",
    "Status",
]
TARGET_RELTYPES = [
    "HAT_MARKTMODELL",
    "HAT_TRAGWERKSPRINZIP",
    "HAT_BAUOBJEKTKLASSE",
    "TEILT_LAYER",
    "HAT_BAUTEILEBENE",
    "HAT_WIEDERVERWENDUNGSORT",
    "HAT_FUNKTIONSWECHSEL",
    "HAT_STATUS",
]

MARKTMODELL_TO_BESCHAFFUNGSWEG = {
    "mm_forschungsprojekt_zuteilung": "bweg_direktvermittlung",
    "mm_intra_konzern": "bweg_eigenbestand",
    "mm_kauf_gebraucht": "bweg_bauteilboerse",
    "mm_kauf_neu": "bweg_ausschreibung",
    "mm_leasing": "bweg_leihmodell",
    "mm_plattform_vermittelt": "bweg_digitale_plattform",
    "mm_rueckkauf": "bweg_rueckbauprojekt",
    "mm_same_site": "bweg_eigenbestand",
    "mm_spende": "bweg_spende",
    "mm_take_back_service": "bweg_rueckbauprojekt",
    "mm_unbekannt": None,
}

BAUOBJEKTKLASSE_TO_NUTZUNG = {
    "bok_depot_lager": "nut_lager_depot",
    "bok_infrastruktur": "nut_infrastruktur",
    "bok_reuse_centre": "nut_gewerbe",
}

DEMOTE_RELS = {
    "HAT_TRAGWERKSPRINZIP": "tragwerksprinzip",
    "HAT_BAUOBJEKTKLASSE": "bauobjektklasse",
    "TEILT_LAYER": "layer",
    "HAT_BAUTEILEBENE": "bauteilebene",
    "HAT_WIEDERVERWENDUNGSORT": "wiederverwendungsort",
    "HAT_FUNKTIONSWECHSEL": "funktionswechsel",
    "HAT_STATUS": "status",
}


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v is not None and str(v).strip()]
    text = str(value).strip()
    return [text] if text else []


def display_name(props: dict[str, Any], fallback: str | None = None) -> str:
    for key in ("name", "title", "titel", "id"):
        value = props.get(key)
        if value:
            return str(value)
    return str(fallback or "")


def snapshot(session, path: Path) -> dict[str, int]:
    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "nodes": [
            r.data()
            for r in session.run(
                """
                MATCH (n)
                WHERE any(label IN labels(n) WHERE label IN $labels)
                RETURN elementId(n) AS element_id, labels(n) AS labels, properties(n) AS properties
                ORDER BY elementId(n)
                """,
                labels=TARGET_LABELS,
            )
        ],
        "relationships": [
            r.data()
            for r in session.run(
                """
                MATCH (a)-[rel]-(b)
                WHERE type(rel) IN $reltypes
                   OR any(label IN labels(a) WHERE label IN $labels)
                   OR any(label IN labels(b) WHERE label IN $labels)
                RETURN elementId(rel) AS element_id,
                       type(rel) AS type,
                       a.id AS from_id,
                       labels(a) AS from_labels,
                       properties(a) AS from_properties,
                       b.id AS to_id,
                       labels(b) AS to_labels,
                       properties(b) AS to_properties,
                       properties(rel) AS properties
                ORDER BY elementId(rel)
                """,
                labels=TARGET_LABELS,
                reltypes=TARGET_RELTYPES,
            )
        ],
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return {"nodes": len(payload["nodes"]), "relationships": len(payload["relationships"])}


def counts(session) -> dict[str, Any]:
    result: dict[str, Any] = {"labels": {}, "reltypes": {}}
    for label in TARGET_LABELS + ["Beschaffungsweg", "Bauweise", "Nutzung", "Software"]:
        result["labels"][label] = session.run(f"MATCH (n:`{label}`) RETURN count(n) AS c").single()["c"]
    for reltype in TARGET_RELTYPES + ["HAT_BESCHAFFUNGSWEG", "HAT_BAUWEISE", "HAT_NUTZUNG"]:
        result["reltypes"][reltype] = session.run(f"MATCH ()-[r:`{reltype}`]->() RETURN count(r) AS c").single()["c"]
    result["nodes"] = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
    result["relationships"] = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    return result


def add_update(updates: dict[str, dict[str, set[str]]], node_id: str | None, prop: str, value: str | None) -> None:
    if node_id and value:
        updates[node_id][prop].add(value)


def build_property_demotions(session) -> tuple[dict[str, dict[str, set[str]]], dict[str, int]]:
    updates: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    stats = Counter()
    for reltype, prop in DEMOTE_RELS.items():
        for rec in session.run(
            f"""
            MATCH (src)-[:`{reltype}`]->(vocab)
            RETURN src.id AS src_id, vocab.id AS vocab_id, properties(vocab) AS props
            """
        ):
            add_update(updates, rec["src_id"], prop, display_name(rec["props"], rec["vocab_id"]))
            stats[f"{reltype}_values"] += 1
    for rec in session.run(
        """
        MATCH (src)-[:HAT_MARKTMODELL]->(m:Marktmodell)
        RETURN src.id AS src_id, m.id AS marktmodell_id, properties(m) AS props
        """
    ):
        add_update(updates, rec["src_id"], "legacy_marktmodell", display_name(rec["props"], rec["marktmodell_id"]))
        stats["legacy_marktmodell_values"] += 1
    return updates, dict(stats)


def apply_property_demotions(session, updates: dict[str, dict[str, set[str]]]) -> dict[str, int]:
    nodes_updated = 0
    values_written = 0
    for node_id, props in sorted(updates.items()):
        row = session.run("MATCH (n {id:$id}) RETURN properties(n) AS props", id=node_id).single()
        if row is None:
            continue
        current = row["props"]
        merged: dict[str, Any] = {"phase7_property_migration": RUN, "phase7_updated_at_utc": NOW}
        for key, values in props.items():
            out: list[str] = []
            seen: set[str] = set()
            for value in as_list(current.get(key)) + sorted(values):
                if value and value not in seen:
                    seen.add(value)
                    out.append(value)
            # Status is intentionally single when only one value existed.
            merged[key] = out[0] if key == "status" and len(out) == 1 else out
            values_written += len(out)
        session.run("MATCH (n {id:$id}) SET n += $props", id=node_id, props=merged).consume()
        nodes_updated += 1
    return {"nodes_updated": nodes_updated, "values_written_after_dedup": values_written}


def plan_marktmodell_rewire(session) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rec in session.run(
        """
        MATCH (src)-[r:HAT_MARKTMODELL]->(m:Marktmodell)
        RETURN elementId(r) AS rel_eid,
               src.id AS src_id,
               m.id AS marktmodell_id,
               properties(r) AS rel_props
        ORDER BY src.id, m.id
        """
    ):
        target = MARKTMODELL_TO_BESCHAFFUNGSWEG.get(rec["marktmodell_id"])
        rows.append({**rec.data(), "target_beschaffungsweg": target})
    return rows


def apply_marktmodell_rewire(session, rows: list[dict[str, Any]]) -> dict[str, int]:
    written = 0
    skipped_unknown = 0
    deleted = 0
    for row in rows:
        target = row["target_beschaffungsweg"]
        props = dict(row["rel_props"] or {})
        old_rel_id = props.pop("id", None)
        if target:
            session.run(
                """
                MATCH (src {id:$src_id})
                MATCH (b:Beschaffungsweg {id:$target})
                MERGE (src)-[new_rel:HAT_BESCHAFFUNGSWEG]->(b)
                SET new_rel += $props,
                    new_rel.review_run=$run,
                    new_rel.updated_at_utc=$now,
                    new_rel.merged_legacy_rel_ids =
                    coalesce(new_rel.merged_legacy_rel_ids, []) +
                    [x IN [$old_rel_id] WHERE x IS NOT NULL AND NOT x IN coalesce(new_rel.merged_legacy_rel_ids, [])]
                """,
                src_id=row["src_id"],
                target=target,
                props=props,
                old_rel_id=old_rel_id,
                run=RUN,
                now=NOW,
            ).consume()
            written += 1
        else:
            skipped_unknown += 1
        session.run("MATCH ()-[r]->() WHERE elementId(r)=$eid DELETE r", eid=row["rel_eid"]).consume()
        deleted += 1
    return {"rewired_edges": written, "unknown_only_edges_deleted": skipped_unknown, "HAT_MARKTMODELL_deleted": deleted}


def plan_bauobjekt_to_nutzung(session) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rec in session.run(
        """
        MATCH (src)-[r:HAT_BAUOBJEKTKLASSE]->(bok:Bauobjektklasse)
        RETURN src.id AS src_id, bok.id AS bok_id, elementId(r) AS rel_eid, properties(r) AS rel_props
        """
    ):
        target = BAUOBJEKTKLASSE_TO_NUTZUNG.get(rec["bok_id"])
        if target:
            rows.append({**rec.data(), "target_nutzung": target})
    return rows


def apply_bauobjekt_to_nutzung(session, rows: list[dict[str, Any]]) -> dict[str, int]:
    written = 0
    for row in rows:
        props = dict(row["rel_props"] or {})
        props.pop("id", None)
        session.run(
            """
            MATCH (src {id:$src_id})
            MATCH (n:Nutzung {id:$target})
            MERGE (src)-[r:HAT_NUTZUNG]->(n)
            SET r += $props,
                r.review_run=$run,
                r.updated_at_utc=$now
            """,
            src_id=row["src_id"],
            target=row["target_nutzung"],
            props=props,
            run=RUN,
            now=NOW,
        ).consume()
        written += 1
    return {"HAT_NUTZUNG_from_bauobjektklasse_written": written}


def delete_retired_rels_and_nodes(session) -> dict[str, int]:
    stats: dict[str, int] = {}
    for reltype in TARGET_RELTYPES:
        stats[f"{reltype}_deleted"] = session.run(
            f"MATCH ()-[r:`{reltype}`]->() WITH count(r) AS c, collect(r) AS rels FOREACH (r IN rels | DELETE r) RETURN c"
        ).single()["c"]
    # Remove Tool label only; its nodes are also Software and should survive.
    stats["Tool_label_removed"] = session.run(
        "MATCH (n:Tool) WITH count(n) AS c, collect(n) AS nodes FOREACH (n IN nodes | REMOVE n:Tool) RETURN c"
    ).single()["c"]
    for label in [l for l in TARGET_LABELS if l != "Tool"]:
        stats[f"{label}_deleted"] = session.run(
            f"MATCH (n:`{label}`) WITH count(n) AS c, collect(n) AS nodes FOREACH (n IN nodes | DETACH DELETE n) RETURN c"
        ).single()["c"]
    return stats


def acceptance(session) -> dict[str, Any]:
    return {
        "removed_labels": {
            label: session.run(f"MATCH (n:`{label}`) RETURN count(n) AS c").single()["c"]
            for label in TARGET_LABELS
        },
        "removed_reltypes": {
            reltype: session.run(f"MATCH ()-[r:`{reltype}`]->() RETURN count(r) AS c").single()["c"]
            for reltype in TARGET_RELTYPES
        },
        "Status": session.run("MATCH (n:Status) RETURN count(n) AS c").single()["c"],
        "HAT_STATUS": session.run("MATCH ()-[r:HAT_STATUS]->() RETURN count(r) AS c").single()["c"],
        "Software": session.run("MATCH (n:Software) RETURN count(n) AS c").single()["c"],
        "HAT_BESCHAFFUNGSWEG": session.run("MATCH ()-[r:HAT_BESCHAFFUNGSWEG]->() RETURN count(r) AS c").single()["c"],
        "HAT_NUTZUNG": session.run("MATCH ()-[r:HAT_NUTZUNG]->() RETURN count(r) AS c").single()["c"],
        "nodes_with_status_property": session.run("MATCH (n) WHERE n.status IS NOT NULL RETURN count(n) AS c").single()["c"],
        "duplicate_HAT_BESCHAFFUNGSWEG": session.run(
            "MATCH (a)-[r:HAT_BESCHAFFUNGSWEG]->(b) WITH a,b,count(r) AS c WHERE c>1 RETURN count(*) AS c"
        ).single()["c"],
    }


def run(commit: bool) -> dict[str, Any]:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "phase": "phase7_axis_consolidation",
        "database": database,
        "commit": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    with driver.session(database=database) as session:
        property_updates, demotion_stats = build_property_demotions(session)
        markt_rows = plan_marktmodell_rewire(session)
        bok_rows = plan_bauobjekt_to_nutzung(session)
        report["before"] = counts(session)
        report["planned"] = {
            "property_nodes_to_update": len(property_updates),
            "property_values_to_demote": sum(len(values) for props in property_updates.values() for values in props.values()),
            "demotion_stats": demotion_stats,
            "marktmodell_edges": len(markt_rows),
            "marktmodell_edges_rewirable": sum(1 for row in markt_rows if row["target_beschaffungsweg"]),
            "marktmodell_unknown_only": sum(1 for row in markt_rows if not row["target_beschaffungsweg"]),
            "bauobjektklasse_to_nutzung_edges": len(bok_rows),
        }
        if commit:
            report["snapshot"] = snapshot(session, OUT / "phase7_before.json")
            report["applied"] = {
                "property_demotions": apply_property_demotions(session, property_updates),
                "marktmodell_rewire": apply_marktmodell_rewire(session, markt_rows),
                "bauobjektklasse_to_nutzung": apply_bauobjekt_to_nutzung(session, bok_rows),
                "deleted": delete_retired_rels_and_nodes(session),
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
    path = OUT / ("phase7_report.json" if args.commit else "phase7_dry_run_report.json")
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
