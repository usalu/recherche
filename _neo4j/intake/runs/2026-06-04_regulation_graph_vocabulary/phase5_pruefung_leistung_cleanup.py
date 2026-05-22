"""Phase 5: PruefungNachweis dedup + Leistungsanforderung consolidation.

Dry-run by default. Commit mode:
  1. snapshots PruefungNachweis/Leistungsanforderung and their relationships,
  2. merges exact pn_/pr_ twins into the pr_ canonical node,
  3. names bare PruefungNachweis ids,
  4. adds PruefungNachweis-[:ERFUELLT_NACHWEIS]->Nachweisforderung,
  5. consolidates Leistungsanforderung nodes by mapped Nachweisforderung target,
  6. deletes generic HAT_PRUEFUNG and HAT_LEISTUNGSANFORDERUNG assignment edges.

Usage:
  python phase5_pruefung_leistung_cleanup.py
  python phase5_pruefung_leistung_cleanup.py --commit
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
RUN = "regulation_graph_vocab_2026_06_04_phase5"
NOW = datetime.now(timezone.utc).isoformat()

DROPPED_NF = {
    "nf_mikrobielle_belastung_check",
    "nf_pak_check",
    "nf_radonmessung",
    "nf_voc_emissionsnachweis",
    "nf_kmf_check",
    "nf_pcb_check",
}
NF_GENERAL = "nf_schadstoffpruefung"


def normalize_nf(node_id: str) -> str:
    return NF_GENERAL if node_id in DROPPED_NF else node_id


def humanize_id(node_id: str) -> str:
    text = node_id
    for prefix in ("pn_", "pr_", "la_"):
        if text.startswith(prefix):
            text = text[len(prefix):]
            break
    return "".join(part.capitalize() for part in text.split("_") if part)


def load_rewire() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with (OUT / "rewire_map.csv").open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["old_label"] in {"PruefungNachweis", "Leistungsanforderung"}:
                row["new_target"] = normalize_nf(row["new_target"])
                out[row["old_id"]] = row
    return out


def snapshot(session, path: Path) -> dict[str, int]:
    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "nodes": [
            r.data()
            for r in session.run(
                """
                MATCH (n)
                WHERE n:PruefungNachweis OR n:Leistungsanforderung
                RETURN elementId(n) AS element_id, labels(n) AS labels, properties(n) AS properties
                ORDER BY elementId(n)
                """
            )
        ],
        "relationships": [
            r.data()
            for r in session.run(
                """
                MATCH (a)-[rel]-(b)
                WHERE a:PruefungNachweis OR b:PruefungNachweis
                   OR a:Leistungsanforderung OR b:Leistungsanforderung
                   OR type(rel) IN ['HAT_PRUEFUNG','HAT_LEISTUNGSANFORDERUNG']
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
                """
            )
        ],
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return {"nodes": len(payload["nodes"]), "relationships": len(payload["relationships"])}


def counts(session) -> dict[str, int]:
    queries = {
        "PruefungNachweis": "MATCH (n:PruefungNachweis) RETURN count(n) AS c",
        "Leistungsanforderung": "MATCH (n:Leistungsanforderung) RETURN count(n) AS c",
        "HAT_PRUEFUNG": "MATCH ()-[r:HAT_PRUEFUNG]->() RETURN count(r) AS c",
        "HAT_LEISTUNGSANFORDERUNG": "MATCH ()-[r:HAT_LEISTUNGSANFORDERUNG]->() RETURN count(r) AS c",
        "ERFUELLT_NACHWEIS": "MATCH ()-[r:ERFUELLT_NACHWEIS]->() RETURN count(r) AS c",
    }
    return {k: session.run(q).single()["c"] for k, q in queries.items()}


def exact_pn_pr_pairs(session) -> list[dict[str, str]]:
    return [
        r.data()
        for r in session.run(
            """
            MATCH (pn:PruefungNachweis),(pr:PruefungNachweis)
            WHERE pn.id STARTS WITH 'pn_'
              AND pr.id STARTS WITH 'pr_'
              AND substring(pn.id,3)=substring(pr.id,3)
            RETURN pn.id AS duplicate_id, pr.id AS canonical_id
            ORDER BY duplicate_id
            """
        )
    ]


def redirect_and_delete_node(session, duplicate_id: str, canonical_id: str) -> None:
    rels = [
        r.data()
        for r in session.run(
            """
            MATCH (d {id:$duplicate_id})-[rel]-(other)
            RETURN elementId(rel) AS rel_eid,
                   type(rel) AS type,
                   startNode(rel).id AS start_id,
                   endNode(rel).id AS end_id,
                   elementId(other) AS other_eid,
                   properties(rel) AS properties
            """,
            duplicate_id=duplicate_id,
        )
    ]
    for rel in rels:
        reltype = rel["type"]
        props = dict(rel["properties"])
        old_rel_id = props.pop("id", None)
        if rel["start_id"] == duplicate_id:
            session.run(
                f"""
                MATCH (c {{id:$canonical_id}})
                MATCH (other) WHERE elementId(other)=$other_eid
                MERGE (c)-[new_rel:`{reltype}`]->(other)
                SET new_rel += $props,
                    new_rel.merged_legacy_rel_ids =
                    coalesce(new_rel.merged_legacy_rel_ids, []) +
                    [x IN [$old_rel_id] WHERE x IS NOT NULL AND NOT x IN coalesce(new_rel.merged_legacy_rel_ids, [])]
                WITH new_rel
                MATCH ()-[old_rel]->() WHERE elementId(old_rel)=$rel_eid
                DELETE old_rel
                """,
                canonical_id=canonical_id,
                other_eid=rel["other_eid"],
                rel_eid=rel["rel_eid"],
                props=props,
                old_rel_id=old_rel_id,
            ).consume()
        else:
            session.run(
                f"""
                MATCH (c {{id:$canonical_id}})
                MATCH (other) WHERE elementId(other)=$other_eid
                MERGE (other)-[new_rel:`{reltype}`]->(c)
                SET new_rel += $props,
                    new_rel.merged_legacy_rel_ids =
                    coalesce(new_rel.merged_legacy_rel_ids, []) +
                    [x IN [$old_rel_id] WHERE x IS NOT NULL AND NOT x IN coalesce(new_rel.merged_legacy_rel_ids, [])]
                WITH new_rel
                MATCH ()-[old_rel]->() WHERE elementId(old_rel)=$rel_eid
                DELETE old_rel
                """,
                canonical_id=canonical_id,
                other_eid=rel["other_eid"],
                rel_eid=rel["rel_eid"],
                props=props,
                old_rel_id=old_rel_id,
            ).consume()
    session.run(
        """
        MATCH (d {id:$duplicate_id})
        MATCH (c {id:$canonical_id})
        SET c.merged_legacy_pruefung_ids =
            coalesce(c.merged_legacy_pruefung_ids, []) + [x IN [$duplicate_id] WHERE NOT x IN coalesce(c.merged_legacy_pruefung_ids, [])],
            c.updated_at_utc = $now
        DETACH DELETE d
        """,
        duplicate_id=duplicate_id,
        canonical_id=canonical_id,
        now=NOW,
    ).consume()


def name_pruefung_nodes(session) -> int:
    rows = list(
        session.run(
            """
            MATCH (n:PruefungNachweis)
            WHERE n.name IS NULL OR n.name='' OR n.name=n.id
            RETURN n.id AS id
            ORDER BY n.id
            """
        )
    )
    for row in rows:
        session.run(
            "MATCH (n:PruefungNachweis {id:$id}) SET n.name=$name, n.updated_at_utc=$now",
            id=row["id"],
            name=humanize_id(row["id"]),
            now=NOW,
        ).consume()
    return len(rows)


def pruefung_target(row: dict[str, str], canonical_id_by_duplicate: dict[str, str]) -> tuple[str, dict[str, str]] | None:
    old_id = row["old_id"]
    canonical_id = canonical_id_by_duplicate.get(old_id, old_id)
    target = row.get("new_target")
    if not target or not target.startswith("nf_"):
        return None
    return canonical_id, row


def add_erfuellt_edges(session, rewire: dict[str, dict[str, str]], pairs: list[dict[str, str]], commit: bool) -> dict[str, int]:
    canonical_id_by_duplicate = {p["duplicate_id"]: p["canonical_id"] for p in pairs}
    planned: dict[tuple[str, str], dict[str, str]] = {}
    for row in rewire.values():
        if row["old_label"] != "PruefungNachweis":
            continue
        target = pruefung_target(row, canonical_id_by_duplicate)
        if not target:
            continue
        pn_id, mapped_row = target
        planned[(pn_id, mapped_row["new_target"])] = mapped_row
    if not commit:
        return {"planned_edges": len(planned)}
    for (pn_id, nf_id), row in planned.items():
        session.run(
            """
            MATCH (pn:PruefungNachweis {id:$pn_id})
            MATCH (nf:Nachweisforderung {id:$nf_id})
            MERGE (pn)-[r:ERFUELLT_NACHWEIS]->(nf)
            SET r.source_url=$source_url,
                r.evidence_status='method_mapped',
                r.confidence=$confidence,
                r.semantic_basis=$basis,
                r.review_run=$run,
                r.updated_at_utc=$now
            """,
            pn_id=pn_id,
            nf_id=nf_id,
            source_url=row.get("evidence_url") or None,
            confidence=float(row.get("confidence") or 0.7),
            basis=row.get("semantic_basis"),
            run=RUN,
            now=NOW,
        ).consume()
    return {"planned_edges": len(planned)}


def build_la_groups(rewire: dict[str, dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rewire.values():
        if row["old_label"] == "Leistungsanforderung" and row["new_target"].startswith("nf_"):
            groups[row["new_target"]].append(row)
    return groups


def choose_la_canonical(rows: list[dict[str, str]]) -> str:
    preferred = [
        "la_brandschutz",
        "la_feuerwiderstand",
        "la_waermeschutz",
        "la_schallschutz",
        "la_tragfaehigkeit",
        "la_schadstofffreiheit",
        "la_rueckverfolgbarkeit",
        "la_rueckbaubarkeit",
        "la_rutschhemmung",
        "la_dauerhaftigkeit",
    ]
    ids = {row["old_id"] for row in rows}
    for candidate in preferred:
        if candidate in ids:
            return candidate
    return sorted(ids)[0]


def consolidate_leistungsanforderung(session, rewire: dict[str, dict[str, str]], commit: bool) -> dict[str, Any]:
    groups = build_la_groups(rewire)
    canonicals = {nf_id: choose_la_canonical(rows) for nf_id, rows in groups.items()}
    to_delete: list[str] = []
    if not commit:
        return {
            "groups": len(groups),
            "canonical_nodes": len(set(canonicals.values())),
            "nodes_to_delete": sum(len(rows) - 1 for rows in groups.values()),
        }
    for nf_id, rows in groups.items():
        canonical = canonicals[nf_id]
        legacy_names = [row["old_id"] for row in rows]
        source_urls = [row["evidence_url"] for row in rows if row.get("evidence_url")]
        session.run(
            """
            MATCH (la:Leistungsanforderung {id:$canonical})
            SET la.name = CASE WHEN la.name IS NULL OR la.name='' OR la.name=la.id THEN $name ELSE la.name END,
                la.maps_to_nachweisforderung = $nf_id,
                la.merged_legacy_leistungsanforderungen =
                    coalesce(la.merged_legacy_leistungsanforderungen, []) +
                    [x IN $legacy_names WHERE NOT x IN coalesce(la.merged_legacy_leistungsanforderungen, [])],
                la.source_urls =
                    coalesce(la.source_urls, []) +
                    [x IN $source_urls WHERE NOT x IN coalesce(la.source_urls, [])],
                la.review_run = $run,
                la.updated_at_utc = $now
            """,
            canonical=canonical,
            name=humanize_id(canonical),
            nf_id=nf_id,
            legacy_names=legacy_names,
            source_urls=source_urls,
            run=RUN,
            now=NOW,
        ).consume()
        first_row = rows[0]
        session.run(
            """
            MATCH (la:Leistungsanforderung {id:$canonical})
            MATCH (nf:Nachweisforderung {id:$nf_id})
            MERGE (la)-[r:ERFORDERT_NACHWEIS]->(nf)
            SET r.source_url=$source_url,
                r.evidence_status='requirement_mapped',
                r.confidence=$confidence,
                r.review_run=$run,
                r.updated_at_utc=$now
            """,
            canonical=canonical,
            nf_id=nf_id,
            source_url=first_row.get("evidence_url") or None,
            confidence=float(first_row.get("confidence") or 0.7),
            run=RUN,
            now=NOW,
        ).consume()
        for row in rows:
            if row["old_id"] != canonical:
                to_delete.append(row["old_id"])
    for old_id in sorted(set(to_delete)):
        session.run("MATCH (la:Leistungsanforderung {id:$id}) DETACH DELETE la", id=old_id).consume()
    return {
        "groups": len(groups),
        "canonical_nodes": len(set(canonicals.values())),
        "nodes_deleted": len(set(to_delete)),
    }


def delete_generic_assignment_edges(session) -> None:
    session.run("MATCH ()-[r:HAT_PRUEFUNG]->() DELETE r").consume()
    session.run("MATCH ()-[r:HAT_LEISTUNGSANFORDERUNG]->() DELETE r").consume()


def acceptance(session) -> dict[str, Any]:
    exact_pairs = session.run(
        """
        MATCH (pn:PruefungNachweis),(pr:PruefungNachweis)
        WHERE pn.id STARTS WITH 'pn_'
          AND pr.id STARTS WITH 'pr_'
          AND substring(pn.id,3)=substring(pr.id,3)
        RETURN count(*) AS c
        """
    ).single()["c"]
    nameless = session.run(
        "MATCH (n:PruefungNachweis) WHERE n.name IS NULL OR n.name='' OR n.name=n.id RETURN count(n) AS c"
    ).single()["c"]
    method_without_nf = session.run(
        "MATCH (n:PruefungNachweis) WHERE NOT (n)-[:ERFUELLT_NACHWEIS]->(:Nachweisforderung) RETURN count(n) AS c"
    ).single()["c"]
    duplicate_edges = session.run(
        """
        MATCH (a)-[r:ERFUELLT_NACHWEIS|ERFORDERT_NACHWEIS]->(b)
        WITH a,b,type(r) AS t,count(r) AS c
        WHERE c > 1
        RETURN count(*) AS c
        """
    ).single()["c"]
    return {
        "PruefungNachweis": session.run("MATCH (n:PruefungNachweis) RETURN count(n) AS c").single()["c"],
        "Leistungsanforderung": session.run("MATCH (n:Leistungsanforderung) RETURN count(n) AS c").single()["c"],
        "HAT_PRUEFUNG": session.run("MATCH ()-[r:HAT_PRUEFUNG]->() RETURN count(r) AS c").single()["c"],
        "HAT_LEISTUNGSANFORDERUNG": session.run("MATCH ()-[r:HAT_LEISTUNGSANFORDERUNG]->() RETURN count(r) AS c").single()["c"],
        "ERFUELLT_NACHWEIS": session.run("MATCH ()-[r:ERFUELLT_NACHWEIS]->() RETURN count(r) AS c").single()["c"],
        "exact_pn_pr_pairs": exact_pairs,
        "nameless_or_id_named_pruefung": nameless,
        "method_without_erfuellt_nachweis": method_without_nf,
        "duplicate_requirement_edges": duplicate_edges,
    }


def run(commit: bool) -> dict[str, Any]:
    rewire = load_rewire()
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "phase": "phase5_pruefung_leistung_cleanup",
        "database": database,
        "commit": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    with driver.session(database=database) as session:
        pairs = exact_pn_pr_pairs(session)
        report["before"] = counts(session)
        report["planned"] = {
            "exact_pn_pr_pairs": pairs,
            "pruefung_erfuellt_edges": add_erfuellt_edges(session, rewire, pairs, commit=False),
            "leistungsanforderung_consolidation": consolidate_leistungsanforderung(session, rewire, commit=False),
        }
        if commit:
            report["snapshot"] = snapshot(session, OUT / "phase5_before.json")
            for pair in pairs:
                redirect_and_delete_node(session, pair["duplicate_id"], pair["canonical_id"])
            named = name_pruefung_nodes(session)
            report["applied"] = {
                "pn_pr_pairs_merged": len(pairs),
                "pruefung_nodes_named": named,
                "pruefung_erfuellt_edges": add_erfuellt_edges(session, rewire, pairs, commit=True),
                "leistungsanforderung_consolidation": consolidate_leistungsanforderung(session, rewire, commit=True),
            }
            delete_generic_assignment_edges(session)
            report["after"] = counts(session)
            report["acceptance"] = acceptance(session)
    driver.close()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    report = run(args.commit)
    path = OUT / ("phase5_report.json" if args.commit else "phase5_dry_run_report.json")
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
