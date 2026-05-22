"""Apply entwurfsqualitaet v2 literature-backed vocabulary to mit-bestand.

Dry-run by default. --commit MERGEs v2 nodes (with beschreibung), repoints edges,
deprecates orphan v1 vocab nodes.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[4]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

RUN = "entwurfsqualitaet_v2_2026_06_05"
NOW = datetime.now(timezone.utc).isoformat()
OUT = Path(__file__).resolve().parent
CONTRACTS = REPO / "_neo4j" / "contracts"
SOURCE = REPO / "_neo4j" / "intake" / "archive" / "2026-06-05_entwurfsqualitaet" / "designQuality.md"
VOCAB_SEED = CONTRACTS / "entwurfsqualitaet_vokabular_v2.seed.kg.jsonl"
LEGACY_MAP = CONTRACTS / "entwurfsqualitaet_v2_legacy_map.json"
ASSIGN_CSV = OUT / "projekt_begriff_zuordnungen_v2.csv"


def load_vocab() -> list[dict[str, Any]]:
    nodes = []
    for line in VOCAB_SEED.read_text(encoding="utf-8").splitlines():
        if line.strip():
            nodes.append(json.loads(line))
    return nodes


def load_legacy() -> dict[str, Any]:
    return json.loads(LEGACY_MAP.read_text(encoding="utf-8"))


def parse_design_quality(md: str) -> dict[str, dict[str, Any]]:
    blocks = re.split(r"\n---\n", md)
    entries: dict[str, dict[str, Any]] = {}
    for block in blocks:
        m_id = re.search(r"Project ID:\s*`(p_[a-z0-9_]+)`", block)
        if not m_id:
            continue
        project_id = m_id.group(1)
        m_desc = re.search(
            r"DESIGN_DESCRIPTION_CONTEXT.*?\n(?:<!--.*?-->\n)?(.*?)\n<!-- AGENT_IGNORE_END -->",
            block,
            re.S,
        )
        entwurfsbeschreibung = m_desc.group(1).strip() if m_desc else ""
        m_em = re.search(
            r"### EXTRACT: DesignMethodology node candidate\s*\n- \*\*Extraction status:\*\* (.+?)\n- \*\*Candidate text:\*\* (.+?)(?:\n\n|<!--)",
            block,
            re.S,
        )
        m_ae = re.search(
            r"### EXTRACT: ArchitecturalOutput node candidate\s*\n- \*\*Extraction status:\*\* (.+?)\n- \*\*Candidate text:\*\* (.+?)(?:\n\n|<!--)",
            block,
            re.S,
        )
        m_conf = re.search(r"Evidence confidence for the two new nodes:\*\*\s*([^\n]+)", block)
        urls = re.findall(r"https?://[^\s)>\"]+", block)
        entries[project_id] = {
            "project_id": project_id,
            "entwurfsbeschreibung": entwurfsbeschreibung,
            "em_kandidatentext": m_em.group(2).strip() if m_em else "",
            "ae_kandidatentext": m_ae.group(2).strip() if m_ae else "",
            "em_extraktionsstatus": m_em.group(1).strip() if m_em else "",
            "ae_extraktionsstatus": m_ae.group(1).strip() if m_ae else "",
            "belegkonfidenz": m_conf.group(1).strip() if m_conf else "",
            "quell_urls": sorted(set(urls)),
        }
    return entries


def load_assignments() -> list[dict[str, str]]:
    with ASSIGN_CSV.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def graph_stats(session) -> dict[str, Any]:
    row = session.run(
        """
        MATCH (n) WITH count(n) AS nodes
        MATCH ()-[r]->() WITH nodes, count(r) AS rels
        MATCH (p:Projekt) WITH nodes, rels, count(p) AS projekte
        OPTIONAL MATCH (em:Entwurfsmethodik) WITH nodes, rels, projekte, count(em) AS em
        OPTIONAL MATCH (ae:Architekturergebnis) WITH nodes, rels, projekte, em, count(ae) AS ae
        RETURN nodes, rels, projekte, em, ae
        """
    ).single()
    return dict(row)


def apply(commit: bool) -> dict[str, Any]:
    vocab = load_vocab()
    legacy = load_legacy()
    md_entries = parse_design_quality(SOURCE.read_text(encoding="utf-8"))
    assignments = load_assignments()
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "run": RUN,
        "commit": commit,
        "vokabular_version": "v2",
        "source": str(SOURCE),
        "vocab_seed": str(VOCAB_SEED),
    }
    try:
        with driver.session(database=database) as session:
            report["before"] = graph_stats(session)
            matched = [a for a in assignments if a.get("status") == "matched"]
            report["csv_rows"] = len(assignments)
            report["matched"] = len(matched)
            report["skip_edges"] = sum(1 for a in matched if a.get("skip_edges") == "true")
            report["active_edges"] = sum(1 for a in matched if a.get("skip_edges") != "true")

            if commit:
                for node in vocab:
                    props = {
                        **node["properties"],
                        "vokabular_version": "v2",
                        "intake_run": RUN,
                        "aktualisiert_am_utc": NOW,
                    }
                    session.run(
                        f"MERGE (n:{node['labels'][0]} {{id: $id}}) SET n += $props",
                        id=node["id"],
                        props=props,
                    ).consume()

                proj_updated = 0
                em_edges = 0
                ae_edges = 0
                edges_removed = 0
                for row in matched:
                    pid = row["project_id"]
                    md = md_entries.get(pid, {})
                    text = md.get("entwurfsbeschreibung", "")
                    if text:
                        session.run(
                            """
                            MATCH (p:Projekt {id: $id})
                            SET p.entwurfsbeschreibung = $text,
                                p.entwurfsbeschreibung_quelle = $quelle,
                                p.entwurfsqualitaet_run = $run,
                                p.entwurfsqualitaet_am_utc = $now,
                                p.entwurfsqualitaet_vokabular_version = 'v2'
                            """,
                            id=pid,
                            text=text,
                            quelle=str(SOURCE.relative_to(REPO)).replace("\\", "/"),
                            run=RUN,
                            now=NOW,
                        ).consume()
                        proj_updated += 1

                    session.run(
                        """
                        MATCH (p:Projekt {id: $pid})
                        OPTIONAL MATCH (p)-[old_em:HAT_ENTWURFSMETHODIK]->(:Entwurfsmethodik)
                        DELETE old_em
                        WITH p
                        OPTIONAL MATCH (p)-[old_ae:HAT_ARCHITEKTURERGEBNIS]->(:Architekturergebnis)
                        DELETE old_ae
                        """,
                        pid=pid,
                    ).consume()
                    edges_removed += 2

                    if row.get("skip_edges") == "true":
                        continue

                    session.run(
                        """
                        MATCH (p:Projekt {id: $pid}), (em:Entwurfsmethodik {id: $em_id})
                        MERGE (p)-[r:HAT_ENTWURFSMETHODIK]->(em)
                        SET r.kandidatentext = $em_text,
                            r.extraktionsstatus = $em_status,
                            r.belegkonfidenz = $conf,
                            r.quell_urls = $urls,
                            r.zuordnung_quelle = 'manual_v2',
                            r.zuordnung_pruefung = $review,
                            r.begruendung = $note,
                            r.integration_phase = $phase,
                            r.integration_layer = $layer,
                            r.vokabular_version = 'v2',
                            r.intake_run = $run,
                            r.aktualisiert_am_utc = $now
                        """,
                        pid=pid,
                        em_id=row["em_id"],
                        em_text=md.get("em_kandidatentext", ""),
                        em_status=md.get("em_extraktionsstatus", ""),
                        conf=md.get("belegkonfidenz", row.get("belegkonfidenz", "")),
                        urls=md.get("quell_urls", []),
                        review=row.get("em_zuordnung_pruefung", "False") == "True",
                        note=row.get("begruendung", ""),
                        phase=row.get("integration_phase") or None,
                        layer=row.get("integration_layer") or None,
                        run=RUN,
                        now=NOW,
                    ).consume()
                    em_edges += 1

                    session.run(
                        """
                        MATCH (p:Projekt {id: $pid}), (ae:Architekturergebnis {id: $ae_id})
                        MERGE (p)-[r:HAT_ARCHITEKTURERGEBNIS]->(ae)
                        SET r.kandidatentext = $ae_text,
                            r.extraktionsstatus = $ae_status,
                            r.belegkonfidenz = $conf,
                            r.quell_urls = $urls,
                            r.zuordnung_quelle = 'manual_v2',
                            r.zuordnung_pruefung = $review,
                            r.begruendung = $note,
                            r.integration_phase = $phase,
                            r.integration_layer = $layer,
                            r.vokabular_version = 'v2',
                            r.intake_run = $run,
                            r.aktualisiert_am_utc = $now
                        """,
                        pid=pid,
                        ae_id=row["ae_id"],
                        ae_text=md.get("ae_kandidatentext", ""),
                        ae_status=md.get("ae_extraktionsstatus", ""),
                        conf=md.get("belegkonfidenz", row.get("belegkonfidenz", "")),
                        urls=md.get("quell_urls", []),
                        review=row.get("ae_zuordnung_pruefung", "False") == "True",
                        note=row.get("begruendung", ""),
                        phase=row.get("integration_phase") or None,
                        layer=row.get("integration_layer") or None,
                        run=RUN,
                        now=NOW,
                    ).consume()
                    ae_edges += 1

                for dep_id in legacy.get("deprecated_v1_ids", []):
                    session.run(
                        """
                        MATCH (n {id: $id})
                        WHERE n:Entwurfsmethodik OR n:Architekturergebnis
                        OPTIONAL MATCH ()-[r]->(n)
                        WITH n, count(r) AS deg
                        WHERE deg = 0
                        SET n:DEPRECATED, n.deprecated_am_utc = $now, n.deprecated_reason = 'v2_vocab_replacement'
                        """,
                        id=dep_id,
                        now=NOW,
                    ).consume()

                report["vocab_nodes_written"] = len(vocab)
                report["projekte_updated"] = proj_updated
                report["em_edges_written"] = em_edges
                report["ae_edges_written"] = ae_edges
                report["edges_cleared"] = edges_removed

            report["after"] = graph_stats(session)
            if commit:
                report["em_distribution"] = [
                    dict(r)
                    for r in session.run(
                        """
                        MATCH (em:Entwurfsmethodik)
                        WHERE NOT em:DEPRECATED
                        OPTIONAL MATCH ()-[:HAT_ENTWURFSMETHODIK]->(em)
                        RETURN em.name AS begriff, em.beschreibung AS beschreibung, count(*) AS projekte
                        ORDER BY projekte DESC
                        """
                    )
                ]
                report["ae_distribution"] = [
                    dict(r)
                    for r in session.run(
                        """
                        MATCH (ae:Architekturergebnis)
                        WHERE NOT ae:DEPRECATED
                        OPTIONAL MATCH ()-[:HAT_ARCHITEKTURERGEBNIS]->(ae)
                        RETURN ae.name AS begriff, ae.beschreibung AS beschreibung, count(*) AS projekte
                        ORDER BY projekte DESC
                        """
                    )
                ]
                report["deprecated_orphans"] = [
                    dict(r)
                    for r in session.run(
                        """
                        MATCH (n)
                        WHERE (n:Entwurfsmethodik OR n:Architekturergebnis) AND n:DEPRECATED
                        RETURN n.id AS id, labels(n) AS labels
                        ORDER BY id
                        """
                    )
                ]
    finally:
        driver.close()

    out_name = "apply_v2_report.json" if commit else "dry_run_v2_report.json"
    (OUT / out_name).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    report = apply(args.commit)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
