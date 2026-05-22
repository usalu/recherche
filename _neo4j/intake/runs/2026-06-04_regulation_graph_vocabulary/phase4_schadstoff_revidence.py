"""Phase 4: re-evidence Schadstoff screening and retire generic pollutant spray.

Dry-run by default. Commit mode:
  1. snapshots Phase-4 pollutant relationships to phase4_before.json,
  2. enriches existing Schadstoff -> Era/Material/Bauteiltyp screening rules,
  3. connects each Schadstoff to the regulation overlay (rf_schadstoff_frage and Nachweisforderung),
  4. adds case-documented-internal KMF proof edges for the four audited mineral-wool components,
  5. deletes legacy HAS_RISK_POLLUTANT / REQUIRES_VERIFICATION_FOR only when a sourced replacement path exists,
  6. tags remaining legacy pollutant spray as screening_unverified and writes phase4_screening_report.json.

Internal case docs are kept as low-priority provenance properties; the primary
evidence URL remains the authoritative rule URL (TRGS/LfU/REACH/etc.).

Usage:
  python phase4_schadstoff_revidence.py
  python phase4_schadstoff_revidence.py --commit
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
from build_vocabulary_graph import REGELWERK  # noqa: E402

OUT = Path(__file__).resolve().parent
RUN = "regulation_graph_vocab_2026_06_04_phase4"
NOW = datetime.now(timezone.utc).isoformat()

SCREENING_RELTYPES = ["TYPISCH_BEI_ERA", "TYPISCH_BEI_MATERIAL", "TYPISCH_BEI_BAUTEILTYP"]
LEGACY_RELTYPES = ["HAS_RISK_POLLUTANT", "REQUIRES_VERIFICATION_FOR"]
RF_SCHADSTOFF = "rf_schadstoff_frage"
NF_GENERAL = "nf_schadstoffpruefung"

RW = {rw["id"]: rw for rw in REGELWERK}

POLLUTANT_TO_RULE = {
    "s_asbest": "rw_trgs_519",
    "s_kmf": "rw_trgs_521",
    "s_pcb": "rw_pcb_richtlinie",
    "s_pak": "rw_pop_2019_1021",
    "s_holzschutzmittel": "rw_din_68800_altholzv",
    "s_bleifarbe": "rw_reach_annex_xvii",
    "s_formaldehyd": "rw_agbb_voc",
    "s_schwermetalle": "rw_reach_annex_xvii",
    "s_radon": "rw_strlschg_radon",
    "s_schimmel": "rw_uba_schimmelleitfaden",
    "s_chlorid": "rw_vdi_6202",
    "s_salze": "rw_vdi_6202",
    "s_mineraloel": "rw_vdi_6202",
}

POLLUTANT_TO_NF = {
    "s_asbest": "nf_asbest_check",
    "s_bleifarbe": "nf_schwermetall_oder_bleifarbe_check",
    "s_chlorid": NF_GENERAL,
    "s_formaldehyd": "nf_formaldehyd_oder_emissionsnachweis",
    "s_holzschutzmittel": "nf_holzschutzmittel_check",
    "s_kmf": NF_GENERAL,  # nf_kmf_check was folded per the user's <4-edge rule.
    "s_mineraloel": NF_GENERAL,
    "s_pak": NF_GENERAL,  # nf_pak_check was folded.
    "s_pcb": NF_GENERAL,  # nf_pcb_check was folded.
    "s_radon": NF_GENERAL,  # nf_radonmessung was folded.
    "s_salze": NF_GENERAL,
    "s_schimmel": NF_GENERAL,  # nf_mikrobielle_belastung_check was folded.
    "s_schwermetalle": "nf_schwermetall_oder_bleifarbe_check",
}

CASE_AUDIT = OUT / "phase4_case_evidence_audit.json"


def rule_props(pollutant_id: str) -> dict[str, Any]:
    rw = RW[POLLUTANT_TO_RULE[pollutant_id]]
    return {
        "source_url": rw["url"],
        "source_quote": rw["quote"],
        "rechtsgrundlage": rw["name"],
        "confidence": float(rw["conf"]),
    }


def load_case_candidates() -> list[dict[str, Any]]:
    if not CASE_AUDIT.exists():
        return []
    data = json.loads(CASE_AUDIT.read_text(encoding="utf-8"))
    return data.get("candidates", [])


def snapshot(session, path: Path) -> dict[str, int]:
    rels = [
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
            ORDER BY elementId(rel)
            """,
            reltypes=SCREENING_RELTYPES + LEGACY_RELTYPES + ["ERFORDERT_NACHWEIS", "TRIGGERS_REGULIERUNGSFRAGE"],
        )
    ]
    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "relationships": rels,
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return {"relationships": len(rels)}


def count_rels(session) -> dict[str, int]:
    return {
        reltype: session.run(f"MATCH ()-[r:`{reltype}`]->() RETURN count(r) AS c").single()["c"]
        for reltype in SCREENING_RELTYPES + LEGACY_RELTYPES + ["ERFORDERT_NACHWEIS", "TRIGGERS_REGULIERUNGSFRAGE"]
    }


def pollutant_ids(session) -> list[str]:
    return [
        r["id"]
        for r in session.run("MATCH (s:Schadstoff) RETURN s.id AS id ORDER BY id")
        if r["id"] in POLLUTANT_TO_RULE
    ]


def replacement_exists(session, from_id: str, from_labels: list[str], pollutant_id: str) -> bool:
    if "Bauteilgruppe" in from_labels:
        return session.run(
            """
            MATCH (b:Bauteilgruppe {id:$from_id})
            MATCH (s:Schadstoff {id:$pollutant_id})
            WHERE EXISTS {
              MATCH (b)-[:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(s)
              WHERE EXISTS((s)-[:TYPISCH_BEI_MATERIAL]->(m))
            }
            OR EXISTS {
              MATCH (b)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)<-[:TYPISCH_BEI_BAUTEILTYP]-(s)
              WHERE EXISTS((s)-[:TYPISCH_BEI_BAUTEILTYP]->(bt))
            }
            OR EXISTS {
              MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(b)
              MATCH (p)-[:HAS_BAUWERK|NUTZT_BAUWERK]->(:Bauwerk)-->(e:BauwerkEra)<-[:TYPISCH_BEI_ERA]-(s)
              WHERE EXISTS((s)-[:TYPISCH_BEI_ERA]->(e))
            }
            RETURN count(b) AS c
            """,
            from_id=from_id,
            pollutant_id=pollutant_id,
        ).single()["c"] > 0
    if "Projekt" in from_labels:
        return session.run(
            """
            MATCH (p:Projekt {id:$from_id})
            MATCH (s:Schadstoff {id:$pollutant_id})
            WHERE EXISTS {
              MATCH (p)-[:HAS_BAUWERK|NUTZT_BAUWERK]->(:Bauwerk)-->(e:BauwerkEra)<-[:TYPISCH_BEI_ERA]-(s)
              WHERE EXISTS((s)-[:TYPISCH_BEI_ERA]->(e))
            }
            OR EXISTS {
              MATCH (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(s)
              WHERE EXISTS((s)-[:TYPISCH_BEI_MATERIAL]->(m))
            }
            OR EXISTS {
              MATCH (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)<-[:TYPISCH_BEI_BAUTEILTYP]-(s)
              WHERE EXISTS((s)-[:TYPISCH_BEI_BAUTEILTYP]->(bt))
            }
            RETURN count(p) AS c
            """,
            from_id=from_id,
            pollutant_id=pollutant_id,
        ).single()["c"] > 0
    return False


def build_legacy_plan(session) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    to_delete: list[dict[str, Any]] = []
    to_tag: list[dict[str, Any]] = []
    rows = session.run(
        """
        MATCH (a)-[r:HAS_RISK_POLLUTANT|REQUIRES_VERIFICATION_FOR]->(s:Schadstoff)
        RETURN elementId(r) AS rid, type(r) AS reltype,
               a.id AS from_id, labels(a) AS from_labels,
               s.id AS pollutant_id, properties(r) AS props
        ORDER BY type(r), a.id, s.id
        """
    )
    for row in rows:
        item = dict(row)
        if replacement_exists(session, item["from_id"], item["from_labels"], item["pollutant_id"]):
            to_delete.append(item)
        else:
            to_tag.append(item)
    return to_delete, to_tag


def enrich_screening_edges(session, commit: bool) -> dict[str, int]:
    planned = Counter()
    for reltype in SCREENING_RELTYPES:
        rows = list(
            session.run(
                f"""
                MATCH (s:Schadstoff)-[r:`{reltype}`]->(target)
                RETURN s.id AS pollutant_id, target.id AS target_id
                ORDER BY s.id, target.id
                """
            )
        )
        planned[reltype] = len(rows)
        if not commit:
            continue
        for row in rows:
            props = rule_props(row["pollutant_id"])
            session.run(
                f"""
                MATCH (s:Schadstoff {{id:$pollutant_id}})-[r:`{reltype}`]->(target {{id:$target_id}})
                SET r.source_url = $source_url,
                    r.source_quote = $source_quote,
                    r.rechtsgrundlage = $rechtsgrundlage,
                    r.evidence_status = 'screening_rule_documented',
                    r.basis = 'taxonomy_derived',
                    r.confidence = $confidence,
                    r.review_run = $run,
                    r.updated_at_utc = $now
                """,
                pollutant_id=row["pollutant_id"],
                target_id=row["target_id"],
                run=RUN,
                now=NOW,
                **props,
            ).consume()
    return dict(planned)


def connect_overlay(session, commit: bool) -> dict[str, int]:
    planned = Counter()
    ids = pollutant_ids(session)
    planned["pollutants"] = len(ids)
    planned["TRIGGERS_REGULIERUNGSFRAGE"] = len(ids)
    planned["ERFORDERT_NACHWEIS"] = len(ids)
    if not commit:
        return dict(planned)
    for pollutant_id in ids:
        props = rule_props(pollutant_id)
        nf_id = POLLUTANT_TO_NF[pollutant_id]
        session.run(
            """
            MATCH (s:Schadstoff {id:$pollutant_id})
            MATCH (rf:Regulierungsfrage {id:$rf_id})
            MERGE (s)-[r:TRIGGERS_REGULIERUNGSFRAGE]->(rf)
            SET r.source_url=$source_url,
                r.source_quote=$source_quote,
                r.rechtsgrundlage=$rechtsgrundlage,
                r.evidence_status='rule_documented',
                r.basis='schadstoff_overlay',
                r.confidence=$confidence,
                r.review_run=$run,
                r.updated_at_utc=$now
            """,
            pollutant_id=pollutant_id,
            rf_id=RF_SCHADSTOFF,
            run=RUN,
            now=NOW,
            **props,
        ).consume()
        session.run(
            """
            MATCH (s:Schadstoff {id:$pollutant_id})
            MATCH (nf:Nachweisforderung {id:$nf_id})
            MERGE (s)-[r:ERFORDERT_NACHWEIS]->(nf)
            SET r.source_url=$source_url,
                r.source_quote=$source_quote,
                r.rechtsgrundlage=$rechtsgrundlage,
                r.evidence_status='rule_documented',
                r.basis='schadstoff_overlay',
                r.confidence=$confidence,
                r.review_run=$run,
                r.updated_at_utc=$now
            """,
            pollutant_id=pollutant_id,
            nf_id=nf_id,
            run=RUN,
            now=NOW,
            **props,
        ).consume()
    session.run("MATCH (s:Schadstoff {id:'s_radon'}) SET s.name='Radon'").consume()
    return dict(planned)


def apply_case_edges(session, commit: bool) -> dict[str, int]:
    candidates = load_case_candidates()
    planned = Counter({"candidate_nodes": len(candidates)})
    if not commit:
        return dict(planned)
    props = rule_props("s_kmf")
    for candidate in candidates:
        docs = candidate.get("legacy_internal_provenance_docs") or []
        snippets = [hit["snippet"] for hit in candidate.get("hits", [])]
        session.run(
            """
            MATCH (b:Bauteilgruppe {id:$bg_id})
            MATCH (nf:Nachweisforderung {id:$nf_id})
            MERGE (b)-[r:ERFORDERT_NACHWEIS]->(nf)
            SET r.source_url=$source_url,
                r.source_quote=$source_quote,
                r.rechtsgrundlage=$rechtsgrundlage,
                r.evidence_status='case_documented_internal_plus_rule',
                r.basis='case_documented_internal',
                r.legacy_internal_provenance_docs=$docs,
                r.case_evidence_snippets=$snippets,
                r.confidence=0.7,
                r.review_run=$run,
                r.updated_at_utc=$now
            """,
            bg_id=candidate["node_id"],
            nf_id=NF_GENERAL,
            docs=docs,
            snippets=snippets,
            run=RUN,
            now=NOW,
            **props,
        ).consume()
        planned["case_edges_written"] += 1
    return dict(planned)


def apply_legacy_plan(session, to_delete: list[dict[str, Any]], to_tag: list[dict[str, Any]], commit: bool) -> None:
    if not commit:
        return
    for item in to_delete:
        session.run(
            "MATCH ()-[r]->() WHERE elementId(r)=$rid DELETE r",
            rid=item["rid"],
        ).consume()
    for item in to_tag:
        session.run(
            """
            MATCH ()-[r]->() WHERE elementId(r)=$rid
            SET r.evidence_status='screening_unverified',
                r.basis='screening_unverified',
                r.review_run=$run,
                r.updated_at_utc=$now
            """,
            rid=item["rid"],
            run=RUN,
            now=NOW,
        ).consume()


def acceptance(session) -> dict[str, Any]:
    duplicate_typisch = session.run(
        """
        MATCH (a)-[r:TYPISCH_BEI_ERA|TYPISCH_BEI_MATERIAL|TYPISCH_BEI_BAUTEILTYP]->(b)
        WITH a,b,type(r) AS t,count(r) AS c
        WHERE c > 1
        RETURN count(*) AS c
        """
    ).single()["c"]
    unsourced_kept_screening = session.run(
        """
        MATCH (s:Schadstoff)-[r:TYPISCH_BEI_ERA|TYPISCH_BEI_MATERIAL|TYPISCH_BEI_BAUTEILTYP]->()
        WHERE r.source_url IS NULL AND coalesce(r.evidence_status,'') <> 'screening_unverified'
        RETURN count(r) AS c
        """
    ).single()["c"]
    legacy_unmarked = session.run(
        """
        MATCH ()-[r:HAS_RISK_POLLUTANT|REQUIRES_VERIFICATION_FOR]->()
        WHERE coalesce(r.evidence_status,'') <> 'screening_unverified'
        RETURN count(r) AS c
        """
    ).single()["c"]
    return {
        "Schadstoff": session.run("MATCH (s:Schadstoff) RETURN count(s) AS c").single()["c"],
        "Schadstoff_with_trigger": session.run(
            "MATCH (s:Schadstoff)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:$id}) RETURN count(DISTINCT s) AS c",
            id=RF_SCHADSTOFF,
        ).single()["c"],
        "Schadstoff_with_nachweis": session.run(
            "MATCH (s:Schadstoff)-[:ERFORDERT_NACHWEIS]->(:Nachweisforderung) RETURN count(DISTINCT s) AS c"
        ).single()["c"],
        "duplicate_typisch_pairs": duplicate_typisch,
        "unsourced_kept_schadstoff_screening_edges": unsourced_kept_screening,
        "legacy_pollutant_edges_not_marked_unverified": legacy_unmarked,
        "remaining_HAS_RISK_POLLUTANT": session.run("MATCH ()-[r:HAS_RISK_POLLUTANT]->() RETURN count(r) AS c").single()["c"],
        "remaining_REQUIRES_VERIFICATION_FOR": session.run("MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->() RETURN count(r) AS c").single()["c"],
    }


def run(commit: bool) -> dict[str, Any]:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "phase": "phase4_schadstoff_revidence",
        "database": database,
        "commit": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    with driver.session(database=database) as session:
        report["before"] = count_rels(session)
        to_delete, to_tag = build_legacy_plan(session)
        report["planned"] = {
            "screening_edges_to_enrich": enrich_screening_edges(session, commit=False),
            "overlay_edges": connect_overlay(session, commit=False),
            "case_edges": apply_case_edges(session, commit=False),
            "legacy_edges_to_delete_with_replacement": len(to_delete),
            "legacy_edges_to_tag_screening_unverified": len(to_tag),
            "legacy_to_delete_by_type": dict(Counter(i["reltype"] for i in to_delete)),
            "legacy_to_tag_by_type": dict(Counter(i["reltype"] for i in to_tag)),
        }
        if commit:
            report["snapshot"] = snapshot(session, OUT / "phase4_before.json")
            report["applied"] = {
                "screening_edges": enrich_screening_edges(session, commit=True),
                "overlay_edges": connect_overlay(session, commit=True),
                "case_edges": apply_case_edges(session, commit=True),
            }
            apply_legacy_plan(session, to_delete, to_tag, commit=True)
            screening_report = {
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "deleted_with_replacement": to_delete,
                "screening_unverified_remaining": to_tag,
            }
            (OUT / "phase4_screening_report.json").write_text(
                json.dumps(screening_report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
                encoding="utf-8",
            )
            report["after"] = count_rels(session)
            report["acceptance"] = acceptance(session)
    driver.close()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    report = run(args.commit)
    path = OUT / ("phase4_report.json" if args.commit else "phase4_dry_run_report.json")
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
