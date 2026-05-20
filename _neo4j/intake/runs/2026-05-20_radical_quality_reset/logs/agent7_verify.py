"""Agent 7 — Wave-3 post-run verification snapshot.

Captures the post-Phase-4.1/4.2 state of the graph: rel counts,
evidence shape compliance, basis distribution per type for the
strictly-enumerated groups, and derivation_note coverage for the
provenance-preserving fields.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-20_radical_quality_reset"
OUT = RUN_ROOT / "logs" / "agent7_verify.json"

sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # type: ignore
from neo4j import GraphDatabase  # type: ignore


def main() -> int:
    uri, user, pwd, _ = resolve_connection()
    d = GraphDatabase.driver(uri, auth=(user, pwd))
    out: dict = {}
    with d.session(database="mit-bestand") as s:
        out["total_nodes"] = s.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        out["total_rels"] = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]

        out["rename_status"] = {
            r["rt"]: r["c"]
            for r in s.run(
                """
                CALL () {
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
        }

        out["evidence_shape"] = dict(
            s.run(
                """
                MATCH ()-[r]->() RETURN
                  count(r) AS total,
                  sum(CASE WHEN r.evidence_origin IS NULL THEN 1 ELSE 0 END) AS missing_origin,
                  sum(CASE WHEN r.evidence_basis IS NULL THEN 1 ELSE 0 END) AS missing_basis,
                  sum(CASE WHEN NOT 'evidence_excerpt' IN keys(r) THEN 1 ELSE 0 END) AS missing_excerpt_key,
                  sum(CASE WHEN r.evidence_source_id IS NULL THEN 1 ELSE 0 END) AS missing_source_id,
                  sum(CASE WHEN r.evidence_confidence IS NULL THEN 1 ELSE 0 END) AS missing_confidence,
                  sum(CASE WHEN r.source IS NOT NULL THEN 1 ELSE 0 END) AS legacy_source,
                  sum(CASE WHEN r.evidence IS NOT NULL THEN 1 ELSE 0 END) AS legacy_evidence,
                  sum(CASE WHEN r.source_excerpt IS NOT NULL THEN 1 ELSE 0 END) AS legacy_source_excerpt,
                  sum(CASE WHEN r.datenqualitaet IS NOT NULL THEN 1 ELSE 0 END) AS legacy_datenq,
                  sum(CASE WHEN r.evidence_origin='curated' AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='') THEN 1 ELSE 0 END) AS viol_curated_no_excerpt,
                  sum(CASE WHEN r.evidence_confidence='bookkeeping' AND coalesce(r.evidence_origin,'') <> 'derived' THEN 1 ELSE 0 END) AS viol_bk_not_derived,
                  sum(CASE WHEN r.evidence_excerpt IS NOT NULL AND toLower(r.evidence_excerpt) CONTAINS 'propagated from' THEN 1 ELSE 0 END) AS viol_excerpt_propagated
                """
            ).single()
        )

        out["evidence_origin_distribution"] = [
            dict(r) for r in s.run(
                "MATCH ()-[r]->() WHERE r.evidence_origin IS NOT NULL "
                "RETURN r.evidence_origin AS v, count(*) AS c ORDER BY c DESC"
            )
        ]
        out["evidence_confidence_distribution"] = [
            dict(r) for r in s.run(
                "MATCH ()-[r]->() WHERE r.evidence_confidence IS NOT NULL "
                "RETURN r.evidence_confidence AS v, count(*) AS c ORDER BY c DESC"
            )
        ]
        out["basis_citation_group"] = [
            dict(r) for r in s.run(
                """
                MATCH ()-[r]->()
                WHERE type(r) IN ['BELEGT_IN','BETEILIGT_AN','ASSOZIIERT_MIT_PROJEKT',
                                  'FROM_DONOR','INTO_RECEIVER','HAT_BAUTEILGRUPPE',
                                  'HAT_HUERDE','HAT_AKTEURROLLE']
                RETURN type(r) AS rt, r.evidence_basis AS basis, count(*) AS c
                ORDER BY rt, basis
                """
            )
        ]
        out["basis_norm_group"] = [
            dict(r) for r in s.run(
                """
                MATCH ()-[r:REFERENZIERT_NORM]->()
                RETURN r.evidence_basis AS basis, count(*) AS c ORDER BY c DESC
                """
            )
        ]
        out["derivation_note_per_type"] = [
            dict(r) for r in s.run(
                """
                MATCH ()-[r]->() WHERE r.derivation_note IS NOT NULL
                RETURN type(r) AS rt, count(*) AS c ORDER BY c DESC
                """
            )
        ]
        out["rel_type_counts"] = {
            r["t"]: r["c"]
            for r in s.run(
                "MATCH ()-[r]->() RETURN type(r) AS t, count(*) AS c ORDER BY c DESC"
            )
        }
        out["per_type_evidence"] = [
            dict(r) for r in s.run(
                """
                MATCH ()-[r]->()
                WITH type(r) AS rt, r
                RETURN rt,
                       count(*) AS total,
                       sum(CASE WHEN r.evidence_origin IS NULL THEN 1 ELSE 0 END) AS missing_origin,
                       sum(CASE WHEN r.evidence_excerpt IS NOT NULL THEN 1 ELSE 0 END) AS has_excerpt
                ORDER BY total DESC
                """
            )
        ]

    d.close()
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"total_nodes={out['total_nodes']}  total_rels={out['total_rels']}")
    print(f"rename_status={out['rename_status']}")
    print(f"evidence_shape={out['evidence_shape']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
