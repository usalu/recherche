"""Integrate entwurfsqualitaet from designQuality.md into mit-bestand.

Dry-run by default. --commit writes vocab nodes, Projekt.entwurfsbeschreibung,
and HAT_ENTWURFSMETHODIK / HAT_ARCHITEKTURERGEBNIS edges.
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

RUN = "entwurfsqualitaet_2026_06_05"
NOW = datetime.now(timezone.utc).isoformat()
OUT = Path(__file__).resolve().parent
CONTRACTS = REPO / "_neo4j" / "contracts"
SOURCE = REPO / "_neo4j" / "intake" / "archive" / "2026-06-05_entwurfsqualitaet" / "designQuality.md"
PHRASE_MAP = CONTRACTS / "entwurfsqualitaet_phrase_zuordnung.json"
VOCAB_SEED = CONTRACTS / "entwurfsqualitaet_vokabular.seed.kg.jsonl"


def load_vocab() -> list[dict[str, Any]]:
    nodes = []
    for line in VOCAB_SEED.read_text(encoding="utf-8").splitlines():
        if line.strip():
            nodes.append(json.loads(line))
    return nodes


def load_phrase_rules() -> dict[str, Any]:
    return json.loads(PHRASE_MAP.read_text(encoding="utf-8"))


def parse_design_quality(md: str) -> list[dict[str, Any]]:
    blocks = re.split(r"\n---\n", md)
    entries = []
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
        em_status = (m_em.group(1).strip() if m_em else "")
        em_text = (m_em.group(2).strip() if m_em else "")
        ae_status = (m_ae.group(1).strip() if m_ae else "")
        ae_text = (m_ae.group(2).strip() if m_ae else "")
        m_conf = re.search(r"Evidence confidence for the two new nodes:\*\*\s*([^\n]+)", block)
        belegkonfidenz = m_conf.group(1).strip() if m_conf else ""
        urls = re.findall(r"https?://[^\s)>\"]+", block)
        entries.append(
            {
                "project_id": project_id,
                "entwurfsbeschreibung": entwurfsbeschreibung,
                "em_kandidatentext": em_text,
                "ae_kandidatentext": ae_text,
                "em_extraktionsstatus": em_status,
                "ae_extraktionsstatus": ae_status,
                "belegkonfidenz": belegkonfidenz,
                "quell_urls": sorted(set(urls)),
            }
        )
    return entries


def score_match(text: str, patterns: list[str]) -> int:
    t = text.lower()
    score = 0
    for p in patterns:
        if p.lower() in t:
            score += 10 + len(p) // 10
    return score


def assign_vocab(text: str, rules: list[dict[str, Any]], fallback: str) -> tuple[str, bool, int]:
    best_id = fallback
    best_score = 0
    for rule in rules:
        s = score_match(text, rule["patterns"])
        if s > best_score:
            best_score = s
            best_id = rule["id"]
    review = best_score == 0
    return best_id, review, best_score


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


def build_assignments(entries: list[dict[str, Any]], graph_ids: set[str], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for e in entries:
        pid = e["project_id"]
        if pid not in graph_ids:
            e["status"] = "unmatched_no_projekt"
            out.append(e)
            continue
        em_pool = e["em_kandidatentext"]
        ae_pool = e["ae_kandidatentext"]
        em_id, em_review, em_score = assign_vocab(
            em_pool, rules["entwurfsmethodik"], rules["fallback"]["entwurfsmethodik"]
        )
        ae_id, ae_review, ae_score = assign_vocab(
            ae_pool, rules["architekturergebnis"], rules["fallback"]["architekturergebnis"]
        )
        if "DO NOT EXTRACT" in e["em_extraktionsstatus"].upper():
            em_review = True
        if "DO NOT EXTRACT" in e["ae_extraktionsstatus"].upper() or "no `architecturaloutput`" in ae_pool.lower():
            ae_review = True
        if "Low/DoNotExtract" in e["belegkonfidenz"]:
            em_review = ae_review = True
        e.update(
            {
                "status": "matched",
                "em_id": em_id,
                "ae_id": ae_id,
                "em_zuordnung_pruefung": em_review,
                "ae_zuordnung_pruefung": ae_review,
                "em_zuordnung_score": em_score,
                "ae_zuordnung_score": ae_score,
            }
        )
        out.append(e)
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "project_id", "status", "em_id", "ae_id", "em_zuordnung_pruefung", "ae_zuordnung_pruefung",
        "belegkonfidenz", "em_extraktionsstatus", "ae_extraktionsstatus",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def apply(commit: bool) -> dict[str, Any]:
    vocab = load_vocab()
    rules = load_phrase_rules()
    entries = parse_design_quality(SOURCE.read_text(encoding="utf-8"))
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {"run": RUN, "commit": commit, "source": str(SOURCE)}
    try:
        with driver.session(database=database) as session:
            report["before"] = graph_stats(session)
            graph_ids = {r["id"] for r in session.run("MATCH (p:Projekt) RETURN p.id AS id")}
            assigned = build_assignments(entries, graph_ids, rules)
            matched = [a for a in assigned if a.get("status") == "matched"]
            unmatched = [a for a in assigned if a.get("status") != "matched"]
            report["parsed_entries"] = len(entries)
            report["matched"] = len(matched)
            report["unmatched"] = len(unmatched)
            report["unmatched_ids"] = [u["project_id"] for u in unmatched]
            report["em_review_count"] = sum(1 for m in matched if m.get("em_zuordnung_pruefung"))
            report["ae_review_count"] = sum(1 for m in matched if m.get("ae_zuordnung_pruefung"))

            write_csv(OUT / "projekt_begriff_zuordnungen.csv", assigned)

            if commit:
                for node in vocab:
                    props = {**node["properties"], "intake_run": RUN, "aktualisiert_am_utc": NOW}
                    session.run(
                        f"MERGE (n:{node['labels'][0]} {{id: $id}}) SET n += $props",
                        id=node["id"],
                        props=props,
                    ).consume()
                vocab_written = len(vocab)
                proj_updated = 0
                em_edges = 0
                ae_edges = 0
                for m in matched:
                    session.run(
                        """
                        MATCH (p:Projekt {id: $id})
                        SET p.entwurfsbeschreibung = $text,
                            p.entwurfsbeschreibung_quelle = $quelle,
                            p.entwurfsqualitaet_run = $run,
                            p.entwurfsqualitaet_am_utc = $now
                        """,
                        id=m["project_id"],
                        text=m["entwurfsbeschreibung"],
                        quelle=str(SOURCE.relative_to(REPO)).replace("\\", "/"),
                        run=RUN,
                        now=NOW,
                    ).consume()
                    proj_updated += 1
                    session.run(
                        """
                        MATCH (p:Projekt {id: $pid}), (em:Entwurfsmethodik {id: $em_id})
                        OPTIONAL MATCH (p)-[old:HAT_ENTWURFSMETHODIK]->(:Entwurfsmethodik)
                        DELETE old
                        MERGE (p)-[r:HAT_ENTWURFSMETHODIK]->(em)
                        SET r.kandidatentext = $text,
                            r.extraktionsstatus = $status,
                            r.belegkonfidenz = $conf,
                            r.quell_urls = $urls,
                            r.zuordnung_pruefung = $review,
                            r.zuordnung_score = $score,
                            r.intake_run = $run,
                            r.aktualisiert_am_utc = $now
                        """,
                        pid=m["project_id"],
                        em_id=m["em_id"],
                        text=m["em_kandidatentext"],
                        status=m["em_extraktionsstatus"],
                        conf=m["belegkonfidenz"],
                        urls=m["quell_urls"],
                        review=bool(m["em_zuordnung_pruefung"]),
                        score=m["em_zuordnung_score"],
                        run=RUN,
                        now=NOW,
                    ).consume()
                    em_edges += 1
                    session.run(
                        """
                        MATCH (p:Projekt {id: $pid}), (ae:Architekturergebnis {id: $ae_id})
                        OPTIONAL MATCH (p)-[old:HAT_ARCHITEKTURERGEBNIS]->(:Architekturergebnis)
                        DELETE old
                        MERGE (p)-[r:HAT_ARCHITEKTURERGEBNIS]->(ae)
                        SET r.kandidatentext = $text,
                            r.extraktionsstatus = $status,
                            r.belegkonfidenz = $conf,
                            r.quell_urls = $urls,
                            r.zuordnung_pruefung = $review,
                            r.zuordnung_score = $score,
                            r.intake_run = $run,
                            r.aktualisiert_am_utc = $now
                        """,
                        pid=m["project_id"],
                        ae_id=m["ae_id"],
                        text=m["ae_kandidatentext"],
                        status=m["ae_extraktionsstatus"],
                        conf=m["belegkonfidenz"],
                        urls=m["quell_urls"],
                        review=bool(m["ae_zuordnung_pruefung"]),
                        score=m["ae_zuordnung_score"],
                        run=RUN,
                        now=NOW,
                    ).consume()
                    ae_edges += 1
                report["vocab_nodes_written"] = vocab_written
                report["projekte_updated"] = proj_updated
                report["em_edges_written"] = em_edges
                report["ae_edges_written"] = ae_edges

            report["after"] = graph_stats(session)
            # distribution
            if commit:
                report["em_distribution"] = [
                    dict(r)
                    for r in session.run(
                        """
                        MATCH (em:Entwurfsmethodik)
                        OPTIONAL MATCH ()-[:HAT_ENTWURFSMETHODIK]->(em)
                        RETURN em.name AS begriff, count(*) AS projekte
                        ORDER BY projekte DESC
                        """
                    )
                ]
                report["ae_distribution"] = [
                    dict(r)
                    for r in session.run(
                        """
                        MATCH (ae:Architekturergebnis)
                        OPTIONAL MATCH ()-[:HAT_ARCHITEKTURERGEBNIS]->(ae)
                        RETURN ae.name AS begriff, count(*) AS projekte
                        ORDER BY projekte DESC
                        """
                    )
                ]
    finally:
        driver.close()

    out_name = "apply_report.json" if commit else "dry_run_report.json"
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

