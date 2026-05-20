"""Agent 7 — Wave 3 Phase 4 + 4.2 — read-only pre-flight exploration.

Captures:
  - all relationship types + counts
  - per-type counts of edges missing any of the 5 evidence fields
  - per-type counts of edges still carrying legacy keys (datenqualitaet, source, source_excerpt, evidence)
  - per-type counts of edges with policy violations:
       curated without excerpt
       bookkeeping without origin='derived'
       evidence_excerpt containing 'propagated from'
  - AUS_BAUWERK / EINGEBAUT_IN / FROM_DONOR / INTO_RECEIVER counts
  - APOC presence check (for apoc.refactor.rename.typeOf)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-20_radical_quality_reset"
LOG_DIR = RUN_ROOT / "logs"
OUT = LOG_DIR / "agent7_explore.json"

sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # type: ignore
from neo4j import GraphDatabase  # type: ignore


def main() -> int:
    uri, user, password, database = resolve_connection()
    database = "mit-bestand"
    driver = GraphDatabase.driver(uri, auth=(user, password))
    out: dict = {"database": database}

    with driver.session(database=database) as s:
        out["total_nodes"] = s.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        out["total_rels"] = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]

        # rel type census
        rel_types = list(s.run(
            "MATCH ()-[r]->() RETURN type(r) AS t, count(*) AS c ORDER BY c DESC"
        ))
        out["rel_type_counts"] = {r["t"]: r["c"] for r in rel_types}

        # Per type: missing evidence + legacy keys + policy violations
        per_type: dict = {}
        for t in out["rel_type_counts"]:
            row = s.run(
                f"""
                MATCH ()-[r:`{t}`]->()
                WITH r,
                     CASE WHEN r.evidence_origin IS NULL THEN 1 ELSE 0 END AS m_origin,
                     CASE WHEN r.evidence_basis IS NULL THEN 1 ELSE 0 END AS m_basis,
                     CASE WHEN NOT 'evidence_excerpt' IN keys(r) THEN 1 ELSE 0 END AS m_excerpt,
                     CASE WHEN r.evidence_source_id IS NULL THEN 1 ELSE 0 END AS m_src,
                     CASE WHEN r.evidence_confidence IS NULL THEN 1 ELSE 0 END AS m_conf,
                     CASE WHEN r.source IS NOT NULL THEN 1 ELSE 0 END AS l_source,
                     CASE WHEN r.evidence IS NOT NULL THEN 1 ELSE 0 END AS l_evidence,
                     CASE WHEN r.source_excerpt IS NOT NULL THEN 1 ELSE 0 END AS l_source_excerpt,
                     CASE WHEN r.datenqualitaet IS NOT NULL THEN 1 ELSE 0 END AS l_datenq,
                     CASE
                       WHEN r.evidence_origin='curated' AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
                       THEN 1 ELSE 0 END AS v_curated_no_excerpt,
                     CASE
                       WHEN r.evidence_confidence='bookkeeping' AND coalesce(r.evidence_origin,'') <> 'derived'
                       THEN 1 ELSE 0 END AS v_bk_not_derived,
                     CASE
                       WHEN r.evidence_excerpt IS NOT NULL AND
                            toLower(r.evidence_excerpt) CONTAINS 'propagated from'
                       THEN 1 ELSE 0 END AS v_excerpt_propagated
                RETURN
                  count(r) AS total,
                  sum(m_origin) AS missing_origin,
                  sum(m_basis) AS missing_basis,
                  sum(m_excerpt) AS missing_excerpt_key,
                  sum(m_src) AS missing_source_id,
                  sum(m_conf) AS missing_confidence,
                  sum(l_source) AS legacy_source,
                  sum(l_evidence) AS legacy_evidence,
                  sum(l_source_excerpt) AS legacy_source_excerpt,
                  sum(l_datenq) AS legacy_datenqualitaet,
                  sum(v_curated_no_excerpt) AS viol_curated_no_excerpt,
                  sum(v_bk_not_derived) AS viol_bk_not_derived,
                  sum(v_excerpt_propagated) AS viol_excerpt_propagated
                """
            ).single()
            per_type[t] = dict(row)
        out["per_type"] = per_type

        # totals
        totals = s.run(
            """
            MATCH ()-[r]->()
            WITH r
            RETURN
              count(r) AS total,
              sum(CASE WHEN r.evidence_origin IS NULL THEN 1 ELSE 0 END) AS missing_origin,
              sum(CASE WHEN r.evidence_basis IS NULL THEN 1 ELSE 0 END) AS missing_basis,
              sum(CASE WHEN NOT 'evidence_excerpt' IN keys(r) THEN 1 ELSE 0 END) AS missing_excerpt_key,
              sum(CASE WHEN r.evidence_source_id IS NULL THEN 1 ELSE 0 END) AS missing_source_id,
              sum(CASE WHEN r.evidence_confidence IS NULL THEN 1 ELSE 0 END) AS missing_confidence,
              sum(CASE WHEN r.source IS NOT NULL THEN 1 ELSE 0 END) AS legacy_source,
              sum(CASE WHEN r.evidence IS NOT NULL THEN 1 ELSE 0 END) AS legacy_evidence,
              sum(CASE WHEN r.source_excerpt IS NOT NULL THEN 1 ELSE 0 END) AS legacy_source_excerpt,
              sum(CASE WHEN r.datenqualitaet IS NOT NULL THEN 1 ELSE 0 END) AS legacy_datenqualitaet,
              sum(CASE WHEN r.evidence_origin='curated' AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='') THEN 1 ELSE 0 END) AS viol_curated_no_excerpt,
              sum(CASE WHEN r.evidence_confidence='bookkeeping' AND coalesce(r.evidence_origin,'') <> 'derived' THEN 1 ELSE 0 END) AS viol_bk_not_derived,
              sum(CASE WHEN r.evidence_excerpt IS NOT NULL AND toLower(r.evidence_excerpt) CONTAINS 'propagated from' THEN 1 ELSE 0 END) AS viol_excerpt_propagated
            """
        ).single()
        out["totals"] = dict(totals)

        # Sample edges with policy violations
        out["samples_curated_no_excerpt"] = [
            dict(r) for r in s.run(
                """
                MATCH (a)-[r]->(b)
                WHERE r.evidence_origin='curated' AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
                RETURN type(r) AS rt, a.id AS aid, labels(a) AS al, b.id AS bid, labels(b) AS bl,
                       r{.*} AS props
                LIMIT 25
                """
            )
        ]
        out["samples_bk_not_derived"] = [
            dict(r) for r in s.run(
                """
                MATCH (a)-[r]->(b)
                WHERE r.evidence_confidence='bookkeeping' AND coalesce(r.evidence_origin,'') <> 'derived'
                RETURN type(r) AS rt, a.id AS aid, labels(a) AS al, b.id AS bid, labels(b) AS bl,
                       r{.*} AS props
                LIMIT 25
                """
            )
        ]
        out["samples_excerpt_propagated"] = [
            dict(r) for r in s.run(
                """
                MATCH (a)-[r]->(b)
                WHERE r.evidence_excerpt IS NOT NULL AND toLower(r.evidence_excerpt) CONTAINS 'propagated from'
                RETURN type(r) AS rt, a.id AS aid, labels(a) AS al, b.id AS bid, labels(b) AS bl,
                       r{.*} AS props
                LIMIT 25
                """
            )
        ]

        # Legacy-key samples (Agent 7 closure target)
        out["samples_legacy_keys"] = [
            dict(r) for r in s.run(
                """
                MATCH (a)-[r]->(b)
                WHERE r.source IS NOT NULL OR r.evidence IS NOT NULL
                   OR r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL
                RETURN type(r) AS rt, a.id AS aid, b.id AS bid,
                       r.evidence_origin AS origin,
                       r.evidence_basis AS basis,
                       r.evidence_excerpt AS excerpt,
                       r.evidence_source_id AS sid,
                       r.evidence_confidence AS conf,
                       r.source AS legacy_source,
                       r.evidence AS legacy_evidence,
                       r.source_excerpt AS legacy_source_excerpt,
                       r.datenqualitaet AS legacy_datenq
                LIMIT 25
                """
            )
        ]

        # AUS_BAUWERK / EINGEBAUT_IN — pre-rename audit
        rename_counts = s.run(
            """
            CALL {
              MATCH ()-[r:AUS_BAUWERK]->() RETURN 'AUS_BAUWERK' AS rt, count(r) AS c
              UNION ALL
              MATCH ()-[r:EINGEBAUT_IN]->() RETURN 'EINGEBAUT_IN' AS rt, count(r) AS c
              UNION ALL
              MATCH ()-[r:FROM_DONOR]->() RETURN 'FROM_DONOR' AS rt, count(r) AS c
              UNION ALL
              MATCH ()-[r:INTO_RECEIVER]->() RETURN 'INTO_RECEIVER' AS rt, count(r) AS c
            }
            RETURN rt, c
            """
        )
        out["rename_status"] = {r["rt"]: r["c"] for r in rename_counts}

        # endpoint label triplets for AUS_BAUWERK / EINGEBAUT_IN
        out["endpoint_labels_aus"] = [
            dict(r) for r in s.run(
                """
                MATCH (a)-[r:AUS_BAUWERK]->(b)
                RETURN labels(a) AS al, labels(b) AS bl, count(*) AS c
                ORDER BY c DESC
                """
            )
        ]
        out["endpoint_labels_ein"] = [
            dict(r) for r in s.run(
                """
                MATCH (a)-[r:EINGEBAUT_IN]->(b)
                RETURN labels(a) AS al, labels(b) AS bl, count(*) AS c
                ORDER BY c DESC
                """
            )
        ]

        # distinct values of legacy datenqualitaet (we'll use this for the
        # datenqualitaet -> evidence_confidence map).
        out["datenq_values"] = [
            dict(r) for r in s.run(
                """
                MATCH ()-[r]->() WHERE r.datenqualitaet IS NOT NULL
                RETURN r.datenqualitaet AS v, count(*) AS c ORDER BY c DESC
                """
            )
        ]

        # distinct values of evidence_confidence
        out["evidence_confidence_values"] = [
            dict(r) for r in s.run(
                """
                MATCH ()-[r]->() WHERE r.evidence_confidence IS NOT NULL
                RETURN r.evidence_confidence AS v, count(*) AS c ORDER BY c DESC
                """
            )
        ]

        # distinct evidence_origin values
        out["evidence_origin_values"] = [
            dict(r) for r in s.run(
                """
                MATCH ()-[r]->() WHERE r.evidence_origin IS NOT NULL
                RETURN r.evidence_origin AS v, count(*) AS c ORDER BY c DESC
                """
            )
        ]

        # APOC availability for refactor.rename.typeOf
        try:
            apoc_check = s.run(
                "CALL dbms.procedures() YIELD name WHERE name = 'apoc.refactor.rename.type' RETURN count(*) AS c"
            ).single()
            out["apoc_rename_type_available"] = apoc_check["c"] > 0
        except Exception as e:
            out["apoc_rename_type_available"] = False
            out["apoc_rename_type_error"] = str(e)

        try:
            apoc_check2 = s.run(
                "SHOW PROCEDURES YIELD name WHERE name CONTAINS 'refactor' RETURN collect(name) AS names"
            ).single()
            out["apoc_refactor_procedures"] = apoc_check2["names"]
        except Exception as e:
            out["apoc_refactor_procedures"] = []
            out["apoc_refactor_procedures_error"] = str(e)

    driver.close()
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"total_rels={out['total_rels']}, distinct_types={len(out['rel_type_counts'])}")
    print(f"missing_origin={out['totals']['missing_origin']}")
    print(f"viol_curated_no_excerpt={out['totals']['viol_curated_no_excerpt']}")
    print(f"viol_bk_not_derived={out['totals']['viol_bk_not_derived']}")
    print(f"viol_excerpt_propagated={out['totals']['viol_excerpt_propagated']}")
    print(f"legacy_datenqualitaet={out['totals']['legacy_datenqualitaet']}")
    print(f"AUS_BAUWERK={out['rename_status'].get('AUS_BAUWERK',0)}, "
          f"EINGEBAUT_IN={out['rename_status'].get('EINGEBAUT_IN',0)}, "
          f"FROM_DONOR={out['rename_status'].get('FROM_DONOR',0)}, "
          f"INTO_RECEIVER={out['rename_status'].get('INTO_RECEIVER',0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
