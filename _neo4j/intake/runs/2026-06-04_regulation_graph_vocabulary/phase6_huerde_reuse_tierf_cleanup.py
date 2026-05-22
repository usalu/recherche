"""Phase 6: Huerde B-clean, reuse-chain re-expression, and Tier-F deletions.

Dry-run by default. Commit mode:
  1. snapshots Phase-6 target labels/relationships,
  2. keeps only the 11 approved Huerde nodes and evidences their retained edges,
  3. demotes HuerdeKategorie/MatchingQualitaet/Wirtschaft/Akzeptanz to properties where possible,
  4. re-expresses Wiederverwendungskette as direct BTG FROM_DONOR / INTO_RECEIVER edges,
  5. deletes scaffolding/noise labels and reltypes.

Usage:
  python phase6_huerde_reuse_tierf_cleanup.py
  python phase6_huerde_reuse_tierf_cleanup.py --commit
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
RUN = "regulation_graph_vocab_2026_06_04_phase6"
NOW = datetime.now(timezone.utc).isoformat()

RAKHSHAN_URL = "https://pmc.ncbi.nlm.nih.gov/articles/PMC7472835/"
RAKHSHAN_QUOTE = (
    "Components reuse in the building sector: systematic review identifies social, "
    "technical, economic, regulatory, organisational and market barriers."
)

HUERDE_KEEP = {
    "h_akzeptanzproblem",
    "h_mengenunsicherheit",
    "h_terminunsicherheit",
    "h_verfuegbarkeitsproblem",
    "h_fehlende_lagerflaeche",
    "h_aufbereitungsaufwand",
    "h_entwurfsbindung",
    "h_ausschreibungsproblem",
    "h_heterogenitaet_chargen",
    "h_witterung_feuchte",
    "h_unkonventionelles_material",
}

HUERDE_CATEGORY = {
    "h_akzeptanzproblem": "social_perception",
    "h_mengenunsicherheit": "market_supply",
    "h_verfuegbarkeitsproblem": "market_supply",
    "h_ausschreibungsproblem": "procurement_regulatory",
    "h_terminunsicherheit": "organisational_timing",
    "h_entwurfsbindung": "planning_organisational",
    "h_fehlende_lagerflaeche": "logistics_storage",
    "h_witterung_feuchte": "logistics_storage",
    "h_aufbereitungsaufwand": "economic_labour",
    "h_heterogenitaet_chargen": "technical_quality",
    "h_unkonventionelles_material": "technical_quality",
}

TARGET_LABELS = [
    "Huerde",
    "HuerdeKategorie",
    "Wiederverwendungskette",
    "Akzeptanz",
    "MatchingQualitaet",
    "Wirtschaft",
]
TARGET_RELTYPES = [
    "HAT_HUERDE",
    "HAT_HUERDEKATEGORIE",
    "TEIL_VON_KETTE",
    "STUB_PROJECT_LINK",
    "HAT_MATCHINGQUALITAET",
    "HAT_WIRTSCHAFT",
    "HAT_WIRTSCHAFTSASPEKT",
]


def phase6_reltypes(session) -> list[str]:
    reltypes = list(TARGET_RELTYPES)
    corrupt = [
        r["relationshipType"]
        for r in session.run(
            "CALL db.relationshipTypes() YIELD relationshipType "
            "WHERE relationshipType STARTS WITH 'GEH' AND relationshipType ENDS WITH 'RT_ZU' "
            "RETURN relationshipType"
        )
    ]
    for reltype in corrupt:
        if reltype not in reltypes:
            reltypes.append(reltype)
    return reltypes


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v is not None and str(v).strip()]
    text = str(value).strip()
    return [text] if text else []


def display_name(props: dict[str, Any], fallback: str | None = None) -> str:
    for key in ("name", "titel", "title", "id"):
        value = props.get(key)
        if value:
            return str(value)
    return str(fallback or "")


def add_prop(updates: dict[str, dict[str, set[str]]], node_id: str | None, key: str, value: str | None) -> None:
    if node_id and value:
        updates[node_id][key].add(value)


def snapshot(session, path: Path) -> dict[str, int]:
    reltypes = phase6_reltypes(session)
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
                reltypes=reltypes + ["FROM_DONOR", "INTO_RECEIVER", "GILT_IN_LAND"],
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
    for label in TARGET_LABELS + ["OntologyAnchor"]:
        result["labels"][label] = session.run(f"MATCH (n:`{label}`) RETURN count(n) AS c").single()["c"]
    for reltype in phase6_reltypes(session) + ["FROM_DONOR", "INTO_RECEIVER"]:
        result["reltypes"][reltype] = session.run(f"MATCH ()-[r:`{reltype}`]->() RETURN count(r) AS c").single()["c"]
    result["nodes"] = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
    result["relationships"] = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    return result


def build_property_demotions(session) -> tuple[dict[str, dict[str, set[str]]], dict[str, int]]:
    updates: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    stats = Counter()

    for rec in session.run(
        """
        MATCH (src)-[:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet)
        RETURN src.id AS src_id, mq.id AS mq_id, properties(mq) AS props
        """
    ):
        mq_id = rec["mq_id"] or ""
        name = display_name(rec["props"], mq_id)
        if mq_id.startswith("mq_geographic_"):
            add_prop(updates, rec["src_id"], "matchingqualitaet_geo", name)
        elif mq_id.startswith("mq_spec_"):
            add_prop(updates, rec["src_id"], "matchingqualitaet_spec", name)
        elif mq_id.startswith("mq_temporal_"):
            add_prop(updates, rec["src_id"], "matchingqualitaet_temporal", name)
        stats["matchingqualitaet_values"] += 1

    for reltype, prop in [("HAT_WIRTSCHAFT", "wirtschaft"), ("HAT_WIRTSCHAFTSASPEKT", "wirtschaft_aspekte")]:
        for rec in session.run(
            f"""
            MATCH (src)-[:`{reltype}`]->(w:Wirtschaft)
            RETURN src.id AS src_id, w.id AS w_id, properties(w) AS props
            """
        ):
            add_prop(updates, rec["src_id"], prop, display_name(rec["props"], rec["w_id"]))
            stats[f"{reltype}_values"] += 1

    for rec in session.run(
        """
        MATCH (land:Land)-[:GILT_IN_LAND]-(ak:Akzeptanz)
        RETURN land.id AS land_id, ak.id AS ak_id, properties(ak) AS props
        """
    ):
        add_prop(updates, rec["land_id"], "akzeptanzfaktoren", display_name(rec["props"], rec["ak_id"]))
        stats["akzeptanz_values"] += 1

    for rec in session.run(
        """
        MATCH (src)-[:HAT_HUERDEKATEGORIE]->(hk:HuerdeKategorie)
        WHERE NOT src:Huerde
        RETURN src.id AS src_id, hk.id AS hk_id, properties(hk) AS props
        """
    ):
        add_prop(updates, rec["src_id"], "legacy_huerde_categories", display_name(rec["props"], rec["hk_id"]))
        stats["legacy_huerde_category_values"] += 1

    return updates, dict(stats)


def apply_property_demotions(session, updates: dict[str, dict[str, set[str]]]) -> dict[str, int]:
    nodes_updated = 0
    values_written = 0
    for node_id, props in updates.items():
        existing = session.run("MATCH (n {id:$id}) RETURN properties(n) AS props", id=node_id).single()
        if existing is None:
            continue
        current = existing["props"]
        merged: dict[str, list[str] | str] = {"phase6_property_migration": RUN, "phase6_updated_at_utc": NOW}
        for key, values in props.items():
            old_values = as_list(current.get(key))
            out: list[str] = []
            seen: set[str] = set()
            for value in old_values + sorted(values):
                if value and value not in seen:
                    seen.add(value)
                    out.append(value)
            merged[key] = out
            values_written += len(out)
        session.run("MATCH (n {id:$id}) SET n += $props", id=node_id, props=merged).consume()
        nodes_updated += 1
    return {"nodes_updated": nodes_updated, "values_written_after_dedup": values_written}


def planned_reuse_chain_edges(session) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    query = """
    MATCH (btg:Bauteilgruppe)-[:TEIL_VON_KETTE]->(w:Wiederverwendungskette)
    OPTIONAL MATCH (w)-[:FROM_DONOR]->(donor)
    OPTIONAL MATCH (w)-[:INTO_RECEIVER]->(receiver)
    RETURN w.id AS chain_id,
           properties(w) AS chain_props,
           btg.id AS btg_id,
           donor.id AS donor_id,
           labels(donor) AS donor_labels,
           receiver.id AS receiver_id,
           labels(receiver) AS receiver_labels
    ORDER BY w.id
    """
    for rec in session.run(query):
        props = rec["chain_props"] or {}
        edge_props = {
            "basis": "reuse_chain_reexpressed",
            "review_run": RUN,
            "source_url": (as_list(props.get("source_urls")) or [None])[0],
            "legacy_internal_provenance_docs": as_list(props.get("legacy_internal_provenance_docs")),
            "source_chain_id": rec["chain_id"],
            "updated_at_utc": NOW,
        }
        if rec["donor_id"]:
            rows.append(
                {
                    "from_id": rec["btg_id"],
                    "to_id": rec["donor_id"],
                    "reltype": "FROM_DONOR",
                    "to_labels": rec["donor_labels"],
                    "props": edge_props,
                }
            )
        if rec["receiver_id"]:
            rows.append(
                {
                    "from_id": rec["btg_id"],
                    "to_id": rec["receiver_id"],
                    "reltype": "INTO_RECEIVER",
                    "to_labels": rec["receiver_labels"],
                    "props": edge_props,
                }
            )
    return rows


def apply_reuse_chain_edges(session, rows: list[dict[str, Any]]) -> int:
    written = 0
    for row in rows:
        reltype = row["reltype"]
        session.run(
            f"""
            MATCH (btg:Bauteilgruppe {{id:$from_id}})
            MATCH (target {{id:$to_id}})
            MERGE (btg)-[r:`{reltype}`]->(target)
            SET r += $props
            """,
            from_id=row["from_id"],
            to_id=row["to_id"],
            props=row["props"],
        ).consume()
        written += 1
    return written


def clean_huerde(session) -> dict[str, int]:
    # Set evidence/category on the controlled vocabulary.
    for h_id, category in HUERDE_CATEGORY.items():
        session.run(
            """
            MATCH (h:Huerde {id:$id})
            SET h.category=$category,
                h.source_urls=coalesce(h.source_urls, []) + [x IN [$url] WHERE NOT x IN coalesce(h.source_urls, [])],
                h.source_titles=coalesce(h.source_titles, []) + [x IN ['Rakhshan et al. 2020 systematic review'] WHERE NOT x IN coalesce(h.source_titles, [])],
                h.review_run=$run,
                h.updated_at_utc=$now
            """,
            id=h_id,
            category=category,
            url=RAKHSHAN_URL,
            run=RUN,
            now=NOW,
        ).consume()

    deleted_regulatory = session.run(
        """
        MATCH ()-[r:HAT_HUERDE]->(h:Huerde)
        WHERE NOT h.id IN $keep
        WITH count(r) AS c, collect(r) AS rels
        FOREACH (r IN rels | DELETE r)
        RETURN c
        """,
        keep=sorted(HUERDE_KEEP),
    ).single()["c"]
    evidenced_kept = session.run(
        """
        MATCH ()-[r:HAT_HUERDE]->(h:Huerde)
        WHERE h.id IN $keep
        SET r.source_url=$url,
            r.source_quote=$quote,
            r.evidence_status='taxonomy_derived',
            r.basis='taxonomy_derived_legacy_screening',
            r.confidence=0.45,
            r.review_run=$run,
            r.updated_at_utc=$now
        RETURN count(r) AS c
        """,
        keep=sorted(HUERDE_KEEP),
        url=RAKHSHAN_URL,
        quote=RAKHSHAN_QUOTE,
        run=RUN,
        now=NOW,
    ).single()["c"]
    deleted_nodes = session.run(
        """
        MATCH (h:Huerde)
        WHERE NOT h.id IN $keep
        WITH count(h) AS c, collect(h) AS nodes
        FOREACH (h IN nodes | DETACH DELETE h)
        RETURN c
        """,
        keep=sorted(HUERDE_KEEP),
    ).single()["c"]
    return {
        "regulatory_huerde_edges_deleted": deleted_regulatory,
        "kept_huerde_edges_evidenced": evidenced_kept,
        "regulatory_huerde_nodes_deleted": deleted_nodes,
    }


def delete_tier_f(session) -> dict[str, int]:
    stats: dict[str, int] = {}
    # Delete explicit noise/scaffold relationship types.
    reltypes = ["STUB_PROJECT_LINK", "HAT_MATCHINGQUALITAET", "HAT_WIRTSCHAFT", "HAT_WIRTSCHAFTSASPEKT", "HAT_HUERDEKATEGORIE"]
    reltypes.extend([r for r in phase6_reltypes(session) if r.startswith("GEH") and r.endswith("RT_ZU")])
    for reltype in reltypes:
        stats[f"{reltype}_deleted"] = session.run(
            f"MATCH ()-[r:`{reltype}`]->() WITH count(r) AS c, collect(r) AS rels FOREACH (r IN rels | DELETE r) RETURN c"
        ).single()["c"]
    # Remove labels now represented as properties.
    for label in ["HuerdeKategorie", "Akzeptanz", "MatchingQualitaet", "Wirtschaft"]:
        stats[f"{label}_deleted"] = session.run(
            f"MATCH (n:`{label}`) WITH count(n) AS c, collect(n) AS nodes FOREACH (n IN nodes | DETACH DELETE n) RETURN c"
        ).single()["c"]
    return stats


def delete_reuse_chain_nodes(session) -> dict[str, int]:
    deleted_edges = session.run(
        """
        MATCH ()-[r:TEIL_VON_KETTE]->()
        WITH count(r) AS c, collect(r) AS rels
        FOREACH (r IN rels | DELETE r)
        RETURN c
        """
    ).single()["c"]
    deleted_nodes = session.run(
        """
        MATCH (w:Wiederverwendungskette)
        WITH count(w) AS c, collect(w) AS nodes
        FOREACH (w IN nodes | DETACH DELETE w)
        RETURN c
        """
    ).single()["c"]
    return {"TEIL_VON_KETTE_deleted": deleted_edges, "Wiederverwendungskette_deleted": deleted_nodes}


def acceptance(session) -> dict[str, Any]:
    return {
        "Huerde": session.run("MATCH (h:Huerde) RETURN count(h) AS c").single()["c"],
        "Huerde_without_category": session.run("MATCH (h:Huerde) WHERE h.category IS NULL RETURN count(h) AS c").single()["c"],
        "HAT_HUERDE_without_source_or_basis": session.run(
            "MATCH ()-[r:HAT_HUERDE]->() WHERE r.source_url IS NULL OR r.basis IS NULL RETURN count(r) AS c"
        ).single()["c"],
        "inferiert_HAT_HUERDE": session.run(
            "MATCH ()-[r:HAT_HUERDE]->() WHERE r.evidence_status='inferiert' RETURN count(r) AS c"
        ).single()["c"],
        "Wiederverwendungskette": session.run("MATCH (w:Wiederverwendungskette) RETURN count(w) AS c").single()["c"],
        "TEIL_VON_KETTE": session.run("MATCH ()-[r:TEIL_VON_KETTE]->() RETURN count(r) AS c").single()["c"],
        "direct_reuse_chain_edges": session.run(
            "MATCH (:Bauteilgruppe)-[r:FROM_DONOR|INTO_RECEIVER]->() WHERE r.basis='reuse_chain_reexpressed' RETURN count(r) AS c"
        ).single()["c"],
        "removed_labels": {
            label: session.run(f"MATCH (n:`{label}`) RETURN count(n) AS c").single()["c"]
            for label in ["HuerdeKategorie", "Akzeptanz", "MatchingQualitaet", "Wirtschaft", "OntologyAnchor"]
        },
        "removed_reltypes": {
            reltype: session.run(f"MATCH ()-[r:`{reltype}`]->() RETURN count(r) AS c").single()["c"]
            for reltype in (
                ["STUB_PROJECT_LINK", "HAT_MATCHINGQUALITAET", "HAT_WIRTSCHAFT", "HAT_WIRTSCHAFTSASPEKT"]
                + [r for r in phase6_reltypes(session) if r.startswith("GEH") and r.endswith("RT_ZU")]
            )
        },
    }


def run(commit: bool) -> dict[str, Any]:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "phase": "phase6_huerde_reuse_tierf_cleanup",
        "database": database,
        "commit": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    with driver.session(database=database) as session:
        property_updates, demotion_stats = build_property_demotions(session)
        reuse_rows = planned_reuse_chain_edges(session)
        report["before"] = counts(session)
        report["planned"] = {
            "property_nodes_to_update": len(property_updates),
            "property_values_to_demote": sum(len(v) for props in property_updates.values() for v in props.values()),
            "demotion_stats": demotion_stats,
            "reuse_chain_direct_edges_to_merge": len(reuse_rows),
            "reuse_chain_edges_by_type": dict(Counter(r["reltype"] for r in reuse_rows)),
            "huerde_keep": len(HUERDE_KEEP),
        }
        if commit:
            report["snapshot"] = snapshot(session, OUT / "phase6_before.json")
            report["applied"] = {
                "property_demotions": apply_property_demotions(session, property_updates),
                "reuse_chain_direct_edges_written": apply_reuse_chain_edges(session, reuse_rows),
                "huerde": clean_huerde(session),
                "reuse_chain_delete": delete_reuse_chain_nodes(session),
                "tier_f_delete": delete_tier_f(session),
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
    path = OUT / ("phase6_report.json" if args.commit else "phase6_dry_run_report.json")
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
