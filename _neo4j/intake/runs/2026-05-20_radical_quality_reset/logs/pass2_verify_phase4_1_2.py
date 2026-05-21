"""Pass-2 Detailed Verifier 9 of 12 — Phase 4.1 + 4.2 (incl. curated-excerpt repair).

Read-only verification against live `mit-bestand`. Produces:
- logs/pass2_verify_phase4_1_2.json (machine-readable verdict + matrix)
- reports/pass2_verify_phase4_1_2.md (human-readable report)

15 checks defined by the orchestrator prompt:

Phase 4.1 deep:
  1. mig_4_1_canonical_evidence.cypher + mig_repair_4_1_curated_excerpts_and_q1.cypher present
  2. PHASE_4_DONE.flag + PHASE_4_1_Q1_REPAIR_DONE.flag present
  3. claim-edge types with evidence_origin IS NULL -> 0 per type
  4. evidence_origin enum strict
  5. evidence_confidence enum strict
  6. evidence_origin='curated' AND evidence_excerpt IS NULL -> 0
  7. evidence_confidence='bookkeeping' AND evidence_origin <> 'derived' -> 0
  8. evidence_excerpt CONTAINS 'propagated from' -> 0
  9. Breakdown by edge type AND evidence_origin: full matrix dump

Phase 4.2 deep:
  10. PHASE_4_2_DONE.flag present
  11. AUS_BAUWERK==0; EINGEBAUT_IN==0
  12. FROM_DONOR>=280; INTO_RECEIVER>=340
  13. Sample 5 FROM_DONOR and 5 INTO_RECEIVER: full property dump

Additional rigor:
  14. HAT_BAUTEILGRUPPE with evidence_origin='curated' >= 200
  15. Sample 5 promoted HAT_BAUTEILGRUPPE: confirm donor+receiver topology backed,
      evidence_basis='cell_citation', evidence_confidence in {belegt, teilweise_belegt}.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j/intake/runs/2026-05-20_radical_quality_reset"
OUT_JSON = RUN_ROOT / "logs/pass2_verify_phase4_1_2.json"
OUT_MD = RUN_ROOT / "reports/pass2_verify_phase4_1_2.md"

CLAIM_TYPES = [
    "BELEGT_IN",
    "HAT_BAUTEILGRUPPE",
    "BETEILIGT_AN",
    "FROM_DONOR",
    "INTO_RECEIVER",
    "HAS_RISK_POLLUTANT",
    "REQUIRES_VERIFICATION_FOR",
    "REFERENZIERT_NORM",
    "HAT_AKTEURROLLE",
    "HAT_HUERDE",
    "APPLIES_IN",
    "APPLIES_TO",
    "BUILT_IN_ERA",
    "ANCHORED_BY",
    "HAT_MARKTMODELL",
    "ZITIERT_QUELLE",
    "ASSOZIIERT_MIT_PROJEKT",
]

ORIGIN_ENUM = ["curated", "inferred", "derived"]
CONFIDENCE_ENUM = ["belegt", "teilweise_belegt", "unklar", "inferiert", "bookkeeping"]


def _resolve() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, pw, db = resolve_connection()
    if db != "mit-bestand":
        db = "mit-bestand"
    return uri, user, pw, db


def _to_jsonable(v):
    if isinstance(v, dict):
        return {k: _to_jsonable(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_to_jsonable(x) for x in v]
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    return str(v)


def main() -> int:
    from neo4j import GraphDatabase  # type: ignore

    uri, user, pw, db = _resolve()
    drv = GraphDatabase.driver(uri, auth=(user, pw))

    res: dict = {
        "verifier": "pass2_detailed_verifier_9_of_12",
        "scope": "phase_4_1_and_4_2_full_with_curated_excerpt_repair",
        "database": db,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "checks": {},
        "matrix_edge_type_x_origin": {},
        "samples": {},
    }

    with drv.session(database=db) as s:
        # --------------------------------------------------------------
        # Check 1: migration files present
        # --------------------------------------------------------------
        mig_a = (
            RUN_ROOT / "migrations/mig_4_1_canonical_evidence.cypher"
        ).is_file()
        mig_b = (
            RUN_ROOT
            / "migrations/mig_repair_4_1_curated_excerpts_and_q1.cypher"
        ).is_file()
        res["checks"]["1_migrations_present"] = {
            "mig_4_1_canonical_evidence.cypher": mig_a,
            "mig_repair_4_1_curated_excerpts_and_q1.cypher": mig_b,
            "pass": mig_a and mig_b,
        }

        # --------------------------------------------------------------
        # Check 2: flags present
        # --------------------------------------------------------------
        flag_4 = (RUN_ROOT / "PHASE_4_DONE.flag").is_file()
        flag_q1 = (RUN_ROOT / "PHASE_4_1_Q1_REPAIR_DONE.flag").is_file()
        res["checks"]["2_flags_present"] = {
            "PHASE_4_DONE.flag": flag_4,
            "PHASE_4_1_Q1_REPAIR_DONE.flag": flag_q1,
            "pass": flag_4 and flag_q1,
        }

        # --------------------------------------------------------------
        # Check 3: claim-edge types with evidence_origin IS NULL
        # --------------------------------------------------------------
        rows = list(
            s.run(
                """
                MATCH ()-[r]->()
                WHERE type(r) IN $types AND r.evidence_origin IS NULL
                RETURN type(r) AS t, count(*) AS c
                """,
                types=CLAIM_TYPES,
            )
        )
        c3 = {row["t"]: row["c"] for row in rows}
        c3_total = sum(c3.values())
        res["checks"]["3_claim_edges_evidence_origin_null"] = {
            "by_type": c3,
            "total": c3_total,
            "expected": 0,
            "pass": c3_total == 0,
        }

        # --------------------------------------------------------------
        # Check 4: evidence_origin enum strict
        # --------------------------------------------------------------
        rec = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.evidence_origin IS NOT NULL
              AND NOT r.evidence_origin IN $enum
            RETURN count(r) AS c
            """,
            enum=ORIGIN_ENUM,
        ).single()
        c4 = rec["c"] if rec else 0
        rec_dist = list(
            s.run(
                """
                MATCH ()-[r]->()
                WHERE r.evidence_origin IS NOT NULL
                RETURN r.evidence_origin AS v, count(*) AS c
                ORDER BY c DESC
                """
            )
        )
        res["checks"]["4_evidence_origin_enum_strict"] = {
            "violations": c4,
            "expected": 0,
            "distribution": {row["v"]: row["c"] for row in rec_dist},
            "pass": c4 == 0,
        }

        # --------------------------------------------------------------
        # Check 5: evidence_confidence enum strict
        # --------------------------------------------------------------
        rec = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.evidence_confidence IS NOT NULL
              AND NOT r.evidence_confidence IN $enum
            RETURN count(r) AS c
            """,
            enum=CONFIDENCE_ENUM,
        ).single()
        c5 = rec["c"] if rec else 0
        rec_dist = list(
            s.run(
                """
                MATCH ()-[r]->()
                WHERE r.evidence_confidence IS NOT NULL
                RETURN r.evidence_confidence AS v, count(*) AS c
                ORDER BY c DESC
                """
            )
        )
        res["checks"]["5_evidence_confidence_enum_strict"] = {
            "violations": c5,
            "expected": 0,
            "distribution": {row["v"]: row["c"] for row in rec_dist},
            "pass": c5 == 0,
        }

        # --------------------------------------------------------------
        # Check 6: curated requires excerpt
        # --------------------------------------------------------------
        rec = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.evidence_origin='curated'
              AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt = '')
            RETURN count(r) AS c
            """
        ).single()
        c6 = rec["c"] if rec else 0
        res["checks"]["6_curated_requires_excerpt"] = {
            "violations": c6,
            "expected": 0,
            "pass": c6 == 0,
        }

        # --------------------------------------------------------------
        # Check 7: bookkeeping only with derived origin
        # --------------------------------------------------------------
        rec = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.evidence_confidence='bookkeeping'
              AND coalesce(r.evidence_origin, '') <> 'derived'
            RETURN count(r) AS c
            """
        ).single()
        c7 = rec["c"] if rec else 0
        res["checks"]["7_bookkeeping_requires_derived"] = {
            "violations": c7,
            "expected": 0,
            "pass": c7 == 0,
        }

        # --------------------------------------------------------------
        # Check 8: evidence_excerpt may not contain 'propagated from'
        # --------------------------------------------------------------
        rec = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.evidence_excerpt IS NOT NULL
              AND r.evidence_excerpt CONTAINS 'propagated from'
            RETURN count(r) AS c
            """
        ).single()
        c8 = rec["c"] if rec else 0
        res["checks"]["8_excerpt_no_propagated_from"] = {
            "violations": c8,
            "expected": 0,
            "pass": c8 == 0,
        }

        # --------------------------------------------------------------
        # Check 9: full matrix edge type x evidence_origin
        # --------------------------------------------------------------
        rows = list(
            s.run(
                """
                MATCH ()-[r]->()
                RETURN type(r) AS t,
                       coalesce(r.evidence_origin, '__NULL__') AS o,
                       count(*) AS c
                ORDER BY t, o
                """
            )
        )
        matrix: dict = {}
        for row in rows:
            matrix.setdefault(row["t"], {})[row["o"]] = row["c"]
        res["matrix_edge_type_x_origin"] = matrix
        # Also compute a column total summary
        column_totals: dict = {}
        for type_dict in matrix.values():
            for o, c in type_dict.items():
                column_totals[o] = column_totals.get(o, 0) + c
        res["checks"]["9_matrix_dump"] = {
            "edge_types_count": len(matrix),
            "column_totals": column_totals,
            "pass": True,  # informational
        }

        # --------------------------------------------------------------
        # Check 10: PHASE_4_2_DONE.flag present
        # --------------------------------------------------------------
        flag_4_2 = (RUN_ROOT / "PHASE_4_2_DONE.flag").is_file()
        res["checks"]["10_phase_4_2_done_flag"] = {
            "present": flag_4_2,
            "pass": flag_4_2,
        }

        # --------------------------------------------------------------
        # Check 11: AUS_BAUWERK == 0; EINGEBAUT_IN == 0
        # --------------------------------------------------------------
        rec = s.run(
            """
            CALL { MATCH ()-[r:AUS_BAUWERK]->() RETURN count(r) AS aus }
            CALL { MATCH ()-[r:EINGEBAUT_IN]->() RETURN count(r) AS ein }
            RETURN aus, ein
            """
        ).single()
        c11_aus = rec["aus"] if rec else None
        c11_ein = rec["ein"] if rec else None
        res["checks"]["11_legacy_donor_receiver_zero"] = {
            "AUS_BAUWERK": c11_aus,
            "EINGEBAUT_IN": c11_ein,
            "expected": {"AUS_BAUWERK": 0, "EINGEBAUT_IN": 0},
            "pass": c11_aus == 0 and c11_ein == 0,
        }

        # --------------------------------------------------------------
        # Check 12: FROM_DONOR >= 280; INTO_RECEIVER >= 340
        # --------------------------------------------------------------
        rec = s.run(
            """
            CALL { MATCH ()-[r:FROM_DONOR]->() RETURN count(r) AS fd }
            CALL { MATCH ()-[r:INTO_RECEIVER]->() RETURN count(r) AS ir }
            RETURN fd, ir
            """
        ).single()
        c12_fd = rec["fd"] if rec else None
        c12_ir = rec["ir"] if rec else None
        res["checks"]["12_new_donor_receiver_thresholds"] = {
            "FROM_DONOR": c12_fd,
            "INTO_RECEIVER": c12_ir,
            "expected": {"FROM_DONOR_min": 280, "INTO_RECEIVER_min": 340},
            "pass": (c12_fd is not None and c12_fd >= 280)
            and (c12_ir is not None and c12_ir >= 340),
        }

        # --------------------------------------------------------------
        # Check 13: sample 5 FROM_DONOR and 5 INTO_RECEIVER with full property dump
        # --------------------------------------------------------------
        fd_samples = list(
            s.run(
                """
                MATCH (src)-[r:FROM_DONOR]->(dst)
                RETURN labels(src) AS src_labels,
                       coalesce(src.id, src.name, '?') AS src_id,
                       labels(dst) AS dst_labels,
                       coalesce(dst.id, dst.name, '?') AS dst_id,
                       properties(r) AS props
                ORDER BY src_id
                LIMIT 5
                """
            )
        )
        ir_samples = list(
            s.run(
                """
                MATCH (src)-[r:INTO_RECEIVER]->(dst)
                RETURN labels(src) AS src_labels,
                       coalesce(src.id, src.name, '?') AS src_id,
                       labels(dst) AS dst_labels,
                       coalesce(dst.id, dst.name, '?') AS dst_id,
                       properties(r) AS props
                ORDER BY src_id
                LIMIT 5
                """
            )
        )
        fd_dump = [
            {
                "src_labels": row["src_labels"],
                "src_id": row["src_id"],
                "dst_labels": row["dst_labels"],
                "dst_id": row["dst_id"],
                "props": _to_jsonable(dict(row["props"])),
            }
            for row in fd_samples
        ]
        ir_dump = [
            {
                "src_labels": row["src_labels"],
                "src_id": row["src_id"],
                "dst_labels": row["dst_labels"],
                "dst_id": row["dst_id"],
                "props": _to_jsonable(dict(row["props"])),
            }
            for row in ir_samples
        ]
        res["samples"]["13_FROM_DONOR_sample_5"] = fd_dump
        res["samples"]["13_INTO_RECEIVER_sample_5"] = ir_dump
        res["checks"]["13_donor_receiver_samples"] = {
            "FROM_DONOR_sampled": len(fd_dump),
            "INTO_RECEIVER_sampled": len(ir_dump),
            "pass": len(fd_dump) >= 5 and len(ir_dump) >= 5,
        }

        # --------------------------------------------------------------
        # Check 14: HAT_BAUTEILGRUPPE curated >= 200
        # --------------------------------------------------------------
        rec = s.run(
            """
            MATCH ()-[r:HAT_BAUTEILGRUPPE]->()
            WHERE r.evidence_origin='curated'
            RETURN count(r) AS c
            """
        ).single()
        c14 = rec["c"] if rec else 0
        res["checks"]["14_hat_bauteilgruppe_curated_min_200"] = {
            "count": c14,
            "expected_min": 200,
            "pass": c14 >= 200,
        }

        # --------------------------------------------------------------
        # Check 15: sample 5 promoted HAT_BAUTEILGRUPPE — confirm topology
        # backed, basis cell_citation, confidence in {belegt, teilweise_belegt}
        # --------------------------------------------------------------
        promoted_samples = list(
            s.run(
                """
                MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
                WHERE r.evidence_origin='curated'
                OPTIONAL MATCH (bg)-[fd:FROM_DONOR]->(donor)
                WITH p, r, bg,
                     count(DISTINCT donor) AS donor_count,
                     collect(DISTINCT coalesce(donor.id, donor.name, '?'))[..3] AS donor_sample
                OPTIONAL MATCH (bg)-[ir:INTO_RECEIVER]->(receiver)
                WITH p, r, bg, donor_count, donor_sample,
                     count(DISTINCT receiver) AS receiver_count,
                     collect(DISTINCT coalesce(receiver.id, receiver.name, '?'))[..3] AS receiver_sample
                RETURN coalesce(p.id, p.name, '?') AS projekt_id,
                       bg.id AS bg_id,
                       donor_count, donor_sample,
                       receiver_count, receiver_sample,
                       properties(r) AS props
                ORDER BY projekt_id, bg.id
                LIMIT 5
                """
            )
        )
        promoted_dump = []
        all_pass = True
        for row in promoted_samples:
            props = _to_jsonable(dict(row["props"]))
            ok_basis = props.get("evidence_basis") == "cell_citation"
            ok_conf = props.get("evidence_confidence") in (
                "belegt",
                "teilweise_belegt",
            )
            ok_topo = (row["donor_count"] or 0) > 0 and (row["receiver_count"] or 0) > 0
            ok = ok_basis and ok_conf and ok_topo
            if not ok:
                all_pass = False
            promoted_dump.append(
                {
                    "projekt_id": row["projekt_id"],
                    "bg_id": row["bg_id"],
                    "donor_count": row["donor_count"],
                    "donor_sample": row["donor_sample"],
                    "receiver_count": row["receiver_count"],
                    "receiver_sample": row["receiver_sample"],
                    "props": props,
                    "checks_per_sample": {
                        "basis_cell_citation": ok_basis,
                        "confidence_in_enum": ok_conf,
                        "topology_donor_and_receiver": ok_topo,
                        "ok": ok,
                    },
                }
            )
        res["samples"]["15_promoted_HAT_BAUTEILGRUPPE_sample_5"] = promoted_dump
        res["checks"]["15_promoted_hat_bauteilgruppe_attributes"] = {
            "sampled": len(promoted_dump),
            "all_topology_basis_conf_ok": all_pass and len(promoted_dump) >= 5,
            "pass": all_pass and len(promoted_dump) >= 5,
        }

        # --------------------------------------------------------------
        # Aggregate verdict
        # --------------------------------------------------------------
        all_keys = sorted(res["checks"].keys())
        verdicts = {k: bool(res["checks"][k].get("pass", False)) for k in all_keys}
        overall = all(verdicts.values())
        res["verdict_per_check"] = verdicts
        res["overall_verdict"] = "PASS" if overall else "FAIL"
        res["fail_count"] = sum(1 for v in verdicts.values() if not v)
        res["pass_count"] = sum(1 for v in verdicts.values() if v)

    drv.close()

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    print("WROTE", OUT_JSON)
    print("VERDICT", res["overall_verdict"], "pass/fail =", res["pass_count"], "/", res["fail_count"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
