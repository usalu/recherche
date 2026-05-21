"""Agent 12 — Phase 5 runner.

Executes mig_5_1_quality_tier.cypher and mig_5_3_relabel_programme.cypher
against the live mit-bestand graph, records before/after counts, and
runs the 7 plan acceptance queries + trust check + source drill-down.
"""
from __future__ import annotations

import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j/intake/runs/2026-05-20_radical_quality_reset"
MIG_DIR = RUN_ROOT / "migrations"
LOGS_DIR = RUN_ROOT / "logs"
RESULT = LOGS_DIR / "agent12_result.json"
PROG = LOGS_DIR / "agent12_progress.log"

MIG_5_1 = MIG_DIR / "mig_5_1_quality_tier.cypher"
MIG_5_3 = MIG_DIR / "mig_5_3_relabel_programme.cypher"


def _now() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


def _log(prog: list[str], msg: str) -> None:
    line = f"{_now()}  {msg}"
    prog.append(line)
    print(line, flush=True)


def _load_statements(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    stripped: list[str] = []
    for line in raw.splitlines():
        if line.lstrip().startswith("//"):
            continue
        idx = line.find("//")
        if idx >= 0:
            line = line[:idx].rstrip()
        stripped.append(line)
    body = "\n".join(stripped)
    parts = [s.strip() for s in body.split(";")]
    return [s for s in parts if s]


def _resolve() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore
    uri, user, pw, db = resolve_connection()
    if db != "mit-bestand":
        db = "mit-bestand"
    return uri, user, pw, db


def _counts(session) -> dict[str, Any]:
    def one(q, **p):
        r = session.run(q, **p).single()
        return r.value() if r else None

    def rows(q, **p):
        return [dict(r) for r in session.run(q, **p)]

    return {
        "total_nodes": one("MATCH (n) RETURN count(n)"),
        "total_rels": one("MATCH ()-[r]->() RETURN count(r)"),
        "projekt_total": one("MATCH (p:Projekt) RETURN count(p)"),
        "programm_total": one("MATCH (p:Programm) RETURN count(p)"),
        "projekt_with_quality_tier": one(
            "MATCH (p:Projekt) WHERE p.quality_tier IS NOT NULL RETURN count(p)"
        ),
        "tier_distribution": rows(
            "MATCH (p:Projekt) RETURN p.quality_tier AS tier, count(p) AS n "
            "ORDER BY tier"
        ),
        "referenziert_norm_mittel": one(
            "MATCH ()-[r:REFERENZIERT_NORM]->() "
            "WHERE r.evidence_confidence='mittel' RETURN count(r)"
        ),
        "referenziert_norm_teilweise_belegt_with_lca_note": one(
            "MATCH ()-[r:REFERENZIERT_NORM]->() "
            "WHERE r.evidence_confidence='teilweise_belegt' "
            "AND r.derivation_note CONTAINS 'mittel->teilweise_belegt' "
            "RETURN count(r)"
        ),
        "target_relabel_state": rows(
            "MATCH (n) WHERE n.id IN ["
            "'p_reuse_logistics','p_vandkunsten_component_reuse',"
            "'p_architecture_of_reuse_brussels','p_reuse_in_construction_zhaw',"
            "'p_circle_house'] "
            "RETURN n.id AS id, labels(n) AS labs, n.quality_tier AS tier, "
            "n.migration_origin AS mo, n.original_label AS ol ORDER BY id"
        ),
    }


def _exec_file(session, path: Path, params: dict[str, Any] | None, prog: list[str]) -> list[dict[str, Any]]:
    audits: list[dict[str, Any]] = []
    params = params or {}
    statements = _load_statements(path)
    _log(prog, f"running {path.name}: {len(statements)} statements")
    for i, stmt in enumerate(statements, start=1):
        try:
            result = session.run(stmt, **params)
            keys = result.keys()
            collected = []
            for rec in result:
                collected.append(dict(rec))
            audits.append({"file": path.name, "stmt": i, "keys": list(keys), "rows": collected[:50], "row_count": len(collected)})
        except Exception as exc:
            snippet = stmt[:280].replace("\n", " ")
            _log(prog, f"  stmt {i} FAILED: {snippet} -> {exc}")
            raise
    return audits


def _acceptance(session) -> dict[str, Any]:
    """Run the 7 plan acceptance queries + trust + drill-down, return rows + counts."""
    def rows(q, **p):
        return [dict(r) for r in session.run(q, **p)]

    def safe_rows(q, **p):
        try:
            return rows(q, **p), None
        except Exception as e:
            return [], str(e)

    out: dict[str, Any] = {}

    q1 = (
        "MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver), "
        "      (bg)-[r:HAT_BAUTEILGRUPPE]-(:Projekt) "
        "WHERE r.evidence_origin='curated' "
        "RETURN donor.id AS donor, bg.id AS bg, bg.menge_t AS menge_t, "
        "       receiver.id AS receiver, r.evidence_excerpt AS excerpt, "
        "       r.evidence_source_id AS source_id LIMIT 50"
    )
    r1, e1 = safe_rows(q1)
    out["q1_reuse_story"] = {"row_count": len(r1), "sample": r1[:5], "error": e1}

    q2 = (
        "MATCH (bg:Bauteilgruppe)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff) "
        "RETURN bg.id AS bg, s.id AS schadstoff, r.evidence_basis AS basis, "
        "       r.evidence_origin AS origin LIMIT 50"
    )
    r2, e2 = safe_rows(q2)
    out["q2_risk_story"] = {"row_count": len(r2), "sample": r2[:5], "error": e2}

    q3 = (
        "MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'}) "
        "UNWIND coalesce(p.reuse_share_facts,[]) AS rs_raw "
        "WITH p, apoc.convert.fromJsonMap(rs_raw) AS rs "
        "WITH p, rs, "
        "  coalesce(rs.value, toFloat(rs.wert)) AS value, "
        "  coalesce(rs.basis, rs.kennwert) AS basis, "
        "  coalesce(rs.unit, rs.einheit) AS unit, "
        "  rs.source_id AS source_id "
        "ORDER BY value DESC "
        "RETURN p.name AS name, value, basis, unit, source_id LIMIT 50"
    )
    try:
        r3 = rows(q3)
        out["q3_comparison"] = {"row_count": len(r3), "sample": r3[:5], "status": "ok"}
    except Exception as e:
        out["q3_comparison"] = {"row_count": 0, "sample": [], "status": "error", "error": str(e)}

    q4 = (
        "MATCH (a:Akteur)-[r:BETEILIGT_AN]->(p:Projekt {quality_tier:'tier_1_decision_grade'}) "
        "WITH a, count(DISTINCT p) AS c WHERE c>=2 "
        "RETURN a.id AS akteur, a.name AS name, c ORDER BY c DESC LIMIT 50"
    )
    r4, e4 = safe_rows(q4)
    out["q4_actor_network"] = {"row_count": len(r4), "sample": r4[:5], "error": e4}

    q5 = (
        "MATCH (rule:ReuseRule)-[:APPLIES_IN]->(l:Land {country_iso:$c}) "
        "WHERE $m IN rule.material "
        "RETURN rule.key_norms AS key_norms, rule.required_tests AS required_tests, "
        "       rule.pollutant_risks AS pollutant_risks, "
        "       rule.evidence_source_id AS source_id LIMIT 10"
    )
    r5, e5 = safe_rows(q5, c="GB", m="Stahl")
    out["q5_decision_support_GB_Stahl"] = {"row_count": len(r5), "sample": r5[:5], "error": e5}
    r5b, e5b = safe_rows(q5, c="CH", m="Holz")
    out["q5_decision_support_CH_Holz"] = {"row_count": len(r5b), "sample": r5b[:5], "error": e5b}

    # pick a tier_1 project for trust check + drill-down
    rec = session.run(
        "MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'}) "
        "RETURN p.id AS id LIMIT 1"
    ).single()
    pick_id = rec["id"] if rec else None
    out["acceptance_anchor_project_id"] = pick_id

    if pick_id:
        q6 = (
            "MATCH (p:Projekt {id:$pid})-[r]-() "
            "WITH r.evidence_origin AS origin, count(*) AS c "
            "RETURN origin, c ORDER BY c DESC"
        )
        r6, e6 = safe_rows(q6, pid=pick_id)
        out["q6_trust_check"] = {"row_count": len(r6), "rows": r6, "error": e6}

        q7 = (
            "MATCH (p:Projekt {id:$pid})-[bel:BELEGT_IN]->(q:Quelle) "
            "WHERE bel.evidence_origin='curated' "
            "RETURN bel.evidence_excerpt AS excerpt, "
            "       bel.evidence_confidence AS confidence, "
            "       q.id AS quelle_id, q.url AS url, q.title AS title, "
            "       q.source_file AS source_file "
            "ORDER BY bel.evidence_confidence, q.id LIMIT 25"
        )
        r7, e7 = safe_rows(q7, pid=pick_id)
        out["q7_source_drilldown"] = {"row_count": len(r7), "sample": r7[:5], "error": e7}
    else:
        out["q6_trust_check"] = {"row_count": 0, "rows": [], "note": "no tier_1 anchor available"}
        out["q7_source_drilldown"] = {"row_count": 0, "sample": [], "note": "no tier_1 anchor available"}

    # Trust check across whole tier-1 cohort
    q6_total = (
        "MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[r]-() "
        "WITH r.evidence_origin AS origin, count(*) AS c "
        "RETURN origin, c ORDER BY c DESC"
    )
    r6a, e6a = safe_rows(q6_total)
    out["q6_trust_check_aggregate"] = {"row_count": len(r6a), "rows": r6a, "error": e6a}

    return out


def main() -> int:
    from neo4j import GraphDatabase  # type: ignore

    progress: list[str] = []
    result: dict[str, Any] = {"agent": 12, "phase": "5", "started_at": _now()}
    try:
        uri, user, pw, db = _resolve()
        drv = GraphDatabase.driver(uri, auth=(user, pw))
        _log(progress, f"connect uri={uri} db={db}")
        with drv.session(database=db) as session:
            result["before"] = _counts(session)
            _log(progress, f"before counts: {json.dumps(result['before'], default=str)}")

            audits: dict[str, list[dict[str, Any]]] = {}
            _log(progress, "------- Phase 5.1 -------")
            audits["5.1"] = _exec_file(session, MIG_5_1, None, progress)
            result["after_5_1"] = _counts(session)
            _log(progress, f"after 5.1: tier_distribution={json.dumps(result['after_5_1']['tier_distribution'])}")

            _log(progress, "------- Phase 5.3 -------")
            audits["5.3"] = _exec_file(session, MIG_5_3, None, progress)
            result["after_5_3"] = _counts(session)
            _log(progress, f"after 5.3: tier_distribution={json.dumps(result['after_5_3']['tier_distribution'])}")
            _log(progress, f"after 5.3: target_relabel_state={json.dumps(result['after_5_3']['target_relabel_state'], default=str)}")

            result["audits"] = audits
            result["acceptance"] = _acceptance(session)
            _log(progress, "acceptance queries done")

        drv.close()
        result["completed_at"] = _now()
        result["status"] = "ok"
    except Exception:
        result["status"] = "error"
        result["error"] = traceback.format_exc()
        _log(progress, "FAILED")
        _log(progress, result["error"])
    finally:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        PROG.write_text("\n".join(progress) + "\n", encoding="utf-8")
        print(f"wrote {RESULT}")
        print(f"wrote {PROG}")
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
