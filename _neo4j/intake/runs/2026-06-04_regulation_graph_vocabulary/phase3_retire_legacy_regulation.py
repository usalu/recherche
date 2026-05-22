"""Phase 3: retire the legacy regulation layer without creating nodes.

Dry-run by default. Commit mode:
  1. snapshots all legacy regulation nodes and relationships to phase3_before.json,
  2. preserves net-new legacy facts as low-priority properties on surviving nodes,
  3. deletes the targeted legacy regulation relationship types,
  4. deletes legacy regulation/catalog nodes.

No Norm/Regelwerk/GAP/Quelle nodes are created. Standards and statuses become
properties only.

Usage:
  python phase3_retire_legacy_regulation.py
  python phase3_retire_legacy_regulation.py --commit
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

OUT = Path(__file__).resolve().parent
RUN = "regulation_graph_vocab_2026_06_04_phase3"
NOW = datetime.now(timezone.utc).isoformat()

LEGACY_LABELS = [
    "Norm",
    "RechtlicheBedingung",
    "Bauproduktstatus",
    "Geltungsbereich",
    "Zertifizierungssystem",
    "LCAModule",
]
TARGET_RELTYPES = [
    "REFERENZIERT_NORM",
    "HAT_RECHTLICHE_BEDINGUNG",
    "HAT_BAUPRODUKTSTATUS",
    "HAT_TYPISCHEN_BAUPRODUKTSTATUS",
    "HAT_GELTUNGSBEREICH",
    "HAT_ZERTIFIZIERUNG",
    "REGULIERT",
    "METHODENGRUNDLAGE_NORM",
]
EXTRA_INCIDENT_RELTYPES = [
    "GILT_IN_LAND",
    "BERECHNET_NACH_MODUL",
    "HAT_BAUTEILTYP",
    "HAT_METHODE",
    "HAT_LEISTUNGSANFORDERUNG",
]


def dedupe(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        out.append(text)
    return out


def display_name(props: dict[str, Any], fallback: str | None = None) -> str:
    for key in ("name", "titel", "title", "label", "id"):
        value = props.get(key)
        if value:
            return str(value)
    return str(fallback or "")


def legacy_label(labels: list[str]) -> str | None:
    for label in labels:
        if label in LEGACY_LABELS:
            return label
    return None


def load_rewire_map() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with (OUT / "rewire_map.csv").open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            out[row["old_id"]] = row
    return out


def append_update(updates: dict[str, dict[str, set[str]]], node_id: str | None, prop: str, value: str | None) -> None:
    if not node_id or not value:
        return
    updates[node_id][prop].add(str(value))


def append_many(updates: dict[str, dict[str, set[str]]], node_id: str | None, prop: str, values: list[str]) -> None:
    for value in values:
        append_update(updates, node_id, prop, value)


def snapshot(session, path: Path) -> dict[str, int]:
    labels = LEGACY_LABELS
    nodes = [
        r.data()
        for r in session.run(
            """
            MATCH (n)
            WHERE any(label IN labels(n) WHERE label IN $labels)
            RETURN elementId(n) AS element_id, labels(n) AS labels, properties(n) AS properties
            ORDER BY elementId(n)
            """,
            labels=labels,
        )
    ]
    rels = [
        r.data()
        for r in session.run(
            """
            MATCH (a)-[rel]-(b)
            WHERE type(rel) IN $target_reltypes
               OR any(label IN labels(a) WHERE label IN $labels)
               OR any(label IN labels(b) WHERE label IN $labels)
            RETURN elementId(rel) AS element_id,
                   type(rel) AS type,
                   elementId(a) AS from_element_id,
                   a.id AS from_id,
                   labels(a) AS from_labels,
                   properties(a) AS from_properties,
                   elementId(b) AS to_element_id,
                   b.id AS to_id,
                   labels(b) AS to_labels,
                   properties(b) AS to_properties,
                   properties(rel) AS properties
            ORDER BY elementId(rel)
            """,
            labels=labels,
            target_reltypes=TARGET_RELTYPES,
        )
    ]
    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "legacy_labels": labels,
        "target_reltypes": TARGET_RELTYPES,
        "nodes": nodes,
        "relationships": rels,
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return {"nodes": len(nodes), "relationships": len(rels)}


def build_preservation_plan(session) -> tuple[dict[str, dict[str, set[str]]], list[dict[str, Any]], dict[str, int]]:
    rewire = load_rewire_map()
    updates: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    gaps: list[dict[str, Any]] = []
    counters = Counter()

    # Handle all headline legacy reltypes that connect kept nodes to legacy concepts.
    query = """
    MATCH (a)-[r]->(b)
    WHERE type(r) IN $reltypes
    RETURN type(r) AS type,
           a.id AS from_id, labels(a) AS from_labels, properties(a) AS from_props,
           b.id AS to_id, labels(b) AS to_labels, properties(b) AS to_props
    """
    for rec in session.run(query, reltypes=TARGET_RELTYPES):
        reltype = rec["type"]
        from_legacy = legacy_label(rec["from_labels"])
        to_legacy = legacy_label(rec["to_labels"])
        from_id = rec["from_id"]
        to_id = rec["to_id"]
        from_name = display_name(rec["from_props"], from_id)
        to_name = display_name(rec["to_props"], to_id)
        map_row = rewire.get(to_id or "") or rewire.get(from_id or "") or {}
        evidence_url = map_row.get("evidence_url")
        target = map_row.get("new_target")

        if reltype == "REFERENZIERT_NORM" and not from_legacy:
            append_update(updates, from_id, "legacy_rechtsgrundlagen", to_name)
            append_update(updates, from_id, "legacy_rechtsgrundlagen_urls", evidence_url)
            counters["properties_REFERENZIERT_NORM"] += 1
        elif reltype == "HAT_RECHTLICHE_BEDINGUNG" and not from_legacy:
            append_update(updates, from_id, "legacy_rechtliche_bedingungen", to_name)
            append_update(updates, from_id, "legacy_rechtsgrundlagen_urls", evidence_url)
            counters["properties_HAT_RECHTLICHE_BEDINGUNG"] += 1
        elif reltype == "HAT_BAUPRODUKTSTATUS" and not from_legacy:
            append_update(updates, from_id, "bauproduktstatus", to_name)
            if target and target.startswith("rw_"):
                append_update(updates, from_id, "legacy_rechtsgrundlagen", target)
                append_update(updates, from_id, "legacy_rechtsgrundlagen_urls", evidence_url)
            counters["properties_HAT_BAUPRODUKTSTATUS"] += 1
        elif reltype == "HAT_TYPISCHEN_BAUPRODUKTSTATUS" and not from_legacy:
            append_update(updates, from_id, "typische_bauproduktstatus", to_name)
            counters["properties_HAT_TYPISCHEN_BAUPRODUKTSTATUS"] += 1
        elif reltype == "HAT_ZERTIFIZIERUNG" and not from_legacy:
            append_update(updates, from_id, "zertifizierungssysteme", to_name)
            counters["properties_HAT_ZERTIFIZIERUNG"] += 1
        elif reltype == "REGULIERT" and not to_legacy:
            append_update(updates, to_id, "reguliert_in_laendern", from_name)
            counters["properties_REGULIERT"] += 1
        else:
            gaps.append(
                {
                    "reltype": reltype,
                    "from_id": from_id,
                    "from_labels": rec["from_labels"],
                    "to_id": to_id,
                    "to_labels": rec["to_labels"],
                    "reason": "both endpoints legacy or no stable surviving property target",
                }
            )
            counters[f"logged_{reltype}"] += 1

    # Preserve the old project -> LCA module -> norm path on the project before deleting LCAModule.
    for rec in session.run(
        """
        MATCH (p:Projekt)-[:BERECHNET_NACH_MODUL]->(m:LCAModule)
        OPTIONAL MATCH (m)-[:METHODENGRUNDLAGE_NORM]->(n:Norm)
        RETURN p.id AS project_id,
               m.id AS module_id, properties(m) AS module_props,
               n.id AS norm_id, properties(n) AS norm_props
        """
    ):
        module_name = display_name(rec["module_props"], rec["module_id"])
        norm_name = display_name(rec["norm_props"] or {}, rec["norm_id"])
        append_update(updates, rec["project_id"], "lca_modules", module_name)
        append_update(updates, rec["project_id"], "lca_method_rechtsgrundlagen", norm_name)
        counters["properties_BERECHNET_NACH_MODUL"] += 1

    # Preserve the one CROW-CUR outgoing Norm context on its surviving targets.
    for reltype, prop in [
        ("HAT_BAUTEILTYP", "legacy_rechtsgrundlagen"),
        ("HAT_METHODE", "legacy_rechtsgrundlagen"),
        ("HAT_LEISTUNGSANFORDERUNG", "legacy_rechtsgrundlagen"),
    ]:
        for rec in session.run(
            f"""
            MATCH (n:Norm)-[r:`{reltype}`]->(target)
            RETURN n.id AS norm_id, properties(n) AS norm_props, target.id AS target_id
            """
        ):
            append_update(updates, rec["target_id"], prop, display_name(rec["norm_props"], rec["norm_id"]))
            counters[f"properties_{reltype}"] += 1

    return updates, gaps, dict(counters)


def merge_existing_props(session, node_id: str, props: dict[str, set[str]]) -> dict[str, list[str]]:
    keys = sorted(props)
    existing = session.run(
        "MATCH (n {id:$id}) RETURN properties(n) AS props",
        id=node_id,
    ).single()
    if existing is None:
        return {}
    current = existing["props"]
    merged: dict[str, list[str]] = {}
    for key in keys:
        old = current.get(key, [])
        old_values = old if isinstance(old, list) else [old]
        merged[key] = dedupe([str(v) for v in old_values if v is not None] + sorted(props[key]))
    return merged


def apply_updates(session, updates: dict[str, dict[str, set[str]]]) -> tuple[int, int]:
    nodes_updated = 0
    values_written = 0
    for node_id, props in sorted(updates.items()):
        merged = merge_existing_props(session, node_id, props)
        if not merged:
            continue
        merged["phase3_legacy_property_migration"] = RUN
        merged["phase3_updated_at_utc"] = NOW
        values_written += sum(len(v) for k, v in merged.items() if isinstance(v, list) and k in props)
        session.run("MATCH (n {id:$id}) SET n += $props", id=node_id, props=merged).consume()
        nodes_updated += 1
    return nodes_updated, values_written


def counts(session) -> dict[str, Any]:
    result: dict[str, Any] = {
        "nodes": session.run("MATCH (n) RETURN count(n) AS c").single()["c"],
        "relationships": session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"],
        "labels": {},
        "reltypes": {},
    }
    for label in LEGACY_LABELS + ["Regelwerk", "Quelle"]:
        result["labels"][label] = session.run(f"MATCH (n:`{label}`) RETURN count(n) AS c").single()["c"]
    for reltype in TARGET_RELTYPES + EXTRA_INCIDENT_RELTYPES:
        result["reltypes"][reltype] = session.run(f"MATCH ()-[r:`{reltype}`]->() RETURN count(r) AS c").single()["c"]
    return result


def delete_legacy_layer(session) -> None:
    for reltype in TARGET_RELTYPES:
        session.run(f"MATCH ()-[r:`{reltype}`]->() DELETE r").consume()
    session.run(
        """
        MATCH (n)
        WHERE any(label IN labels(n) WHERE label IN $labels)
        DETACH DELETE n
        """,
        labels=LEGACY_LABELS,
    ).consume()


def acceptance(session) -> dict[str, Any]:
    duplicate_arrays = session.run(
        """
        MATCH (n)
        WHERE any(k IN ['legacy_rechtsgrundlagen','legacy_rechtsgrundlagen_urls',
                        'legacy_rechtliche_bedingungen','bauproduktstatus',
                        'typische_bauproduktstatus','zertifizierungssysteme',
                        'reguliert_in_laendern','lca_modules','lca_method_rechtsgrundlagen']
                  WHERE n[k] IS NOT NULL AND
                        size(n[k]) <> size([x IN n[k] WHERE single(y IN n[k] WHERE y = x)]))
        RETURN count(n) AS c
        """
    ).single()["c"]
    return {
        "legacy_labels_remaining": {
            label: session.run(f"MATCH (n:`{label}`) RETURN count(n) AS c").single()["c"]
            for label in LEGACY_LABELS
        },
        "legacy_reltypes_remaining": {
            reltype: session.run(f"MATCH ()-[r:`{reltype}`]->() RETURN count(r) AS c").single()["c"]
            for reltype in TARGET_RELTYPES
        },
        "Regelwerk": session.run("MATCH (n:Regelwerk) RETURN count(n) AS c").single()["c"],
        "Quelle": session.run("MATCH (n:Quelle) RETURN count(n) AS c").single()["c"],
        "gap_nodes_created": session.run("MATCH (n) WHERE n.id STARTS WITH 'GAP_' RETURN count(n) AS c").single()["c"],
        "duplicate_preserved_property_arrays": duplicate_arrays,
    }


def run(commit: bool) -> dict[str, Any]:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "phase": "phase3_retire_legacy_regulation",
        "database": database,
        "commit": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    with driver.session(database=database) as session:
        report["before"] = counts(session)
        updates, gaps, preservation = build_preservation_plan(session)
        report["planned"] = {
            "nodes_to_receive_properties": len(updates),
            "property_values_to_preserve": sum(len(values) for props in updates.values() for values in props.values()),
            "preservation_counts": preservation,
            "logged_gaps_count": len(gaps),
            "logged_gaps_preview": gaps[:50],
        }
        if commit:
            report["snapshot"] = snapshot(session, OUT / "phase3_before.json")
            nodes_updated, values_written = apply_updates(session, updates)
            (OUT / "phase3_gaps.json").write_text(
                json.dumps(gaps, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
                encoding="utf-8",
            )
            delete_legacy_layer(session)
            report["properties_applied"] = {
                "nodes_updated": nodes_updated,
                "values_written_after_dedup": values_written,
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
    path = OUT / ("phase3_report.json" if args.commit else "phase3_dry_run_report.json")
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
