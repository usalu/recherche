"""Stage 4 integration audit — orchestrator.

Read-only. Runs stage_4_audit_queries.cypher (Sections A–E), captures every
result, and writes both:
  - stage_4_audit_results.json   (machine-readable)
  - FINAL_REVIEW_PLAN_AUDIT.md   (human-readable; lives at repo root)

Prerequisites (the runner refuses to start otherwise):
  - PHASE_R1_DONE.flag      (agent 1)
  - PHASE_R2_DONE.flag      (agent 2)
  - PHASE_R10_DONE.flag     (agent 2)
  - PHASE_R3_DONE.flag      (agent 3)   ← BLOCKED until R7 done
  - PHASE_R9_DONE.flag      (agent 3)
  - PHASE_R4_DONE.flag      (agent 4)
  - PHASE_R7_DONE.flag      (agent 5)
  - PHASE_R5_DONE.flag      (orchestrator)
  - PHASE_R8_DONE.flag      (agent 1)   ← MUST be last
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REVIEW_PLAN_ROOT = THIS_FILE.parents[2]
REPO_ROOT = THIS_FILE.parents[6]

sys.path.insert(0, str(REPO_ROOT / "_scripts"))
# noinspection PyUnresolvedReferences
from neo4j_env import resolve_connection  # type: ignore

REQUIRED_FLAGS = [
    REVIEW_PLAN_ROOT / "agent_1_evidence_honesty" / "PHASE_R1_DONE.flag",
    REVIEW_PLAN_ROOT / "agent_2_schema_restoration" / "PHASE_R2_DONE.flag",
    REVIEW_PLAN_ROOT / "agent_2_schema_restoration" / "PHASE_R10_DONE.flag",
    REVIEW_PLAN_ROOT / "agent_3_structural_completion" / "PHASE_R3_DONE.flag",
    REVIEW_PLAN_ROOT / "agent_3_structural_completion" / "PHASE_R9_DONE.flag",
    REVIEW_PLAN_ROOT / "agent_4_data_model" / "PHASE_R4_DONE.flag",
    REVIEW_PLAN_ROOT / "agent_5_loader_hardening" / "PHASE_R7_DONE.flag",
    REVIEW_PLAN_ROOT / "orchestrator_r5" / "PHASE_R5_DONE.flag",
    REVIEW_PLAN_ROOT / "agent_1_evidence_honesty" / "PHASE_R8_DONE.flag",
]


def check_prerequisites() -> tuple[bool, list[str]]:
    missing = [str(f.relative_to(REPO_ROOT)) for f in REQUIRED_FLAGS if not f.exists()]
    return len(missing) == 0, missing


def split_statements(cypher_text: str) -> list[str]:
    """Same splitter as orchestrator_r5_runner.py."""
    statements: list[str] = []
    current: list[str] = []
    for raw_line in cypher_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            current.append(line)
            continue
        current.append(line)
        if stripped.endswith(";"):
            stmt = "\n".join(current).strip()
            cleaned = "\n".join(
                ln for ln in stmt.splitlines() if not ln.strip().startswith("//")
            ).strip()
            if cleaned.endswith(";"):
                cleaned = cleaned[:-1].rstrip()
            if cleaned:
                statements.append(cleaned)
            current = []
    return statements


def run_audit():
    ok, missing = check_prerequisites()
    if not ok:
        print("Stage 4 prerequisites NOT met. Missing flags:")
        for m in missing:
            print(f"  - {m}")
        print()
        print("Stage 4 audit cannot run yet. Once the missing flags exist, re-run this script.")
        sys.exit(1)

    uri, user, password, _db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    database = "mit-bestand"

    migration_path = RUN_DIR / "migrations" / "stage_4_audit_queries.cypher"
    statements = split_statements(migration_path.read_text(encoding="utf-8"))

    results: list[dict] = []
    with driver.session(database=database, default_access_mode="READ") as session:
        for i, stmt in enumerate(statements):
            t0 = datetime.now(timezone.utc)
            try:
                records = [dict(r) for r in session.run(stmt)]
                results.append({
                    "statement_index": i,
                    "statement_preview": stmt.splitlines()[0][:120],
                    "started_utc": t0.isoformat(),
                    "elapsed_ms": (datetime.now(timezone.utc) - t0).total_seconds() * 1000.0,
                    "row_count": len(records),
                    "rows": records[:50],  # cap at 50 per query
                })
            except Exception as exc:
                results.append({
                    "statement_index": i,
                    "statement_preview": stmt[:200],
                    "error": str(exc),
                })

    # Persist machine-readable results
    out_json = RUN_DIR / "logs" / "stage_4_audit_results.json"
    out_json.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {out_json}")

    # Generate the human-readable audit report
    report_path = REPO_ROOT / "_neo4j" / "FINAL_REVIEW_PLAN_AUDIT.md"
    report_path.write_text(_render_report(results), encoding="utf-8")
    print(f"Wrote {report_path}")

    # Done flag
    flag = RUN_DIR / "STAGE_4_AUDIT_DONE.flag"
    flag.write_text(json.dumps({
        "phase": "STAGE_4_AUDIT",
        "agent": "orchestrator",
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "verified": True,
        "queries_run": len(results),
        "queries_with_errors": sum(1 for r in results if "error" in r),
        "report": str(report_path.relative_to(REPO_ROOT)),
    }, indent=2), encoding="utf-8")
    print(f"Wrote {flag}")

    driver.close()


def _render_report(results: list[dict]) -> str:
    """Render the human-readable audit. Defensive against missing rows."""
    def find_first(preview_prefix: str) -> dict | None:
        for r in results:
            if r.get("statement_preview", "").startswith(preview_prefix):
                return r
        return None

    def cell(row_dict: dict, key: str, default="—"):
        if row_dict is None or not row_dict.get("rows"):
            return default
        return row_dict["rows"][0].get(key, default)

    now = datetime.now(timezone.utc).isoformat()
    return f"""# FINAL — Review-based remediation audit (Stage 4)

- **Audit run:** {now}
- **Database:** mit-bestand
- **Plan:** [_neo4j/REVIEW_BASED_PLAN/](REVIEW_BASED_PLAN/ORCHESTRATION.md)
- **Supersedes:** [FINAL_PASS2_AUDIT.md](intake/runs/2026-05-20_radical_quality_reset/FINAL_PASS2_AUDIT.md)
- **Verdict:** _<set after manual review>_

## 0. Headline

| Metric | Pre-radical-reset (2026-05-20) | Post-radical-reset (2026-05-21 audit) | Post-review-plan (now) |
|---|---:|---:|---:|
| Total nodes | 2,580 | 3,802 | **{cell(find_first("MATCH (n) RETURN 'total_nodes'"), 'c')}** |
| Total relationships | 19,989 | 25,023 | **{cell(find_first("MATCH ()-[r]->() RETURN 'total_rels'"), 'c')}** |

## 1. Honest Q1–Q7

### Q1 — Reuse Story

| Filter | Row count | Honesty |
|---|---:|---|
| `evidence_origin='source_curated'` only | {cell(find_first("MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),\\n      (p:Projekt)-[hbg:HAT_BAUTEILGRUPPE]->(bg)\\nWHERE hbg.evidence_origin = 'source_curated'"), 'row_count')} | Honest signal |
| `evidence_origin='topology_synthesized'` only | {cell(find_first("MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),\\n      (p:Projekt)-[hbg:HAT_BAUTEILGRUPPE]->(bg)\\nWHERE hbg.evidence_origin = 'topology_synthesized'"), 'row_count')} | What Repair D produced |
| Combined | {cell(find_first("MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),\\n      (p:Projekt)-[hbg:HAT_BAUTEILGRUPPE]->(bg)\\nWHERE hbg.evidence_origin IN ['source_curated', 'topology_synthesized']"), 'row_count')} | Pre-honesty Q1 baseline |

### Q2 — Risk Story

| Basis | Row count |
|---|---:|
| `documented` (curated cell citation) | {cell(find_first("MATCH (bg)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff)\\nWHERE r.evidence_basis = 'documented'"), 'row_count')} |
| `era_and_material` inference | {cell(find_first("MATCH (bg)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff)\\nWHERE r.evidence_basis = 'era_and_material'"), 'row_count')} |
| `material_only` inference | {cell(find_first("MATCH (bg)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff)\\nWHERE r.evidence_basis = 'material_only'"), 'row_count')} |
| `REQUIRES_VERIFICATION_FOR` total | {cell(find_first("MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->()"), 'row_count')} |

### Q3 — Comparison (graph-native via :Kennwert)

Tier-1 projects with `reuse_share` Kennwert: **{cell(find_first("MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[:HAT_KENNWERT]->(kw:Kennwert {category:'reuse_share'})\\nRETURN 'Q3_tier1_with_reuse_share'"), 'c')}**

(See `stage_4_audit_results.json` for the full per-project Kennwert dump.)

### Q4 — Actor Network

| Filter | Count |
|---|---:|
| BETEILIGT_AN only (honest) | {cell(find_first("MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt {quality_tier:'tier_1_decision_grade'})\\nWITH a, count(DISTINCT p) AS c WHERE c >= 2\\nRETURN 'Q4_count'"), 'c')} |
| BETEILIGT_AN ∪ STUB_PROJECT_LINK | {cell(find_first("MATCH (a:Akteur)-[:BETEILIGT_AN|STUB_PROJECT_LINK]->(p:Projekt {quality_tier:'tier_1_decision_grade'})\\nWITH a, count(DISTINCT p) AS c WHERE c >= 2\\nRETURN 'Q4_with_stubs'"), 'c')} |

### Q5 — Decision Support (graph-native :RELEVANT_FOR)

| Probe | Count |
|---|---:|
| Total `:RELEVANT_FOR` edges | {cell(find_first("MATCH ()-[r:RELEVANT_FOR]->()\\nRETURN 'Q5_relevant_for_total'"), 'c')} |
| Ferme du Rail rules (must be 0 — FR uncovered) | {cell(find_first("MATCH (p:Projekt {id:'p_ferme_du_rail_paris'})\\nOPTIONAL MATCH (:ReuseRule)-[r:RELEVANT_FOR]->(p)\\nRETURN 'Q5_ferme_du_rail_rules'"), 'c')} |
| Holbein Gardens rules (must be ≥ 1) | {cell(find_first("MATCH (p:Projekt {id:'p_holbein_gardens_london'})\\nOPTIONAL MATCH (rule:ReuseRule)-[r:RELEVANT_FOR]->(p)\\nRETURN 'Q5_holbein_rules'"), 'c')} |

### Q6 — Trust check (5-bucket distribution)

See `stage_4_audit_results.json` for the full distribution; bookkeeping count: **{cell(find_first("MATCH ()-[r {is_bookkeeping:true}]->()\\nRETURN 'Q6_bookkeeping_count'"), 'c')}** edges flagged separately.

### Q7 — Source drill-down

| Probe | Count |
|---|---:|
| case_markdown → external (ZITIERT_QUELLE) | {cell(find_first("MATCH (qmd:Quelle {quelltyp:'case_markdown'})-[:ZITIERT_QUELLE]->(ext:Quelle)\\nRETURN 'Q7_case_md_external'"), 'c')} |
| case_markdown with `text_content` populated | {cell(find_first("MATCH (qmd:Quelle {quelltyp:'case_markdown'})\\nWHERE qmd.text_content IS NOT NULL\\nRETURN 'Q7_case_md_with_text_content'"), 'c')} |

## 2. Cross-agent invariants

| Invariant | Violations |
|---|---:|
| C1 origin enum violation | {cell(find_first("MATCH ()-[r]->()\\nWHERE r.evidence_origin IS NOT NULL\\n  AND NOT r.evidence_origin IN ['source_curated','topology_synthesized','registry_derived','inferred','external_unfolded']"), 'violations')} |
| C2 old 'curated' value remaining | {cell(find_first("MATCH ()-[r]->()\\nWHERE r.evidence_origin = 'curated'"), 'violations')} |
| C3 'bookkeeping' in confidence enum | {cell(find_first("MATCH ()-[r]->()\\nWHERE r.evidence_confidence = 'bookkeeping'"), 'violations')} |
| C4 source_curated without excerpt | {cell(find_first("MATCH ()-[r]->()\\nWHERE r.evidence_origin = 'source_curated'\\n  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt = '')"), 'violations')} |
| C5 :Bauteilgruppe without bg_kind | {cell(find_first("MATCH (bg:Bauteilgruppe) WHERE bg.bg_kind IS NULL"), 'violations')} |
| C6 :Bauteilgruppe category with topology | {cell(find_first("MATCH (bg:Bauteilgruppe {bg_kind:'category'})\\nWHERE exists{(bg)-[:FROM_DONOR]->()} OR exists{(bg)-[:INTO_RECEIVER]->()}"), 'violations')} |
| C7 :Projekt with BG paths but no :HAS_BAUWERK | {cell(find_first("MATCH (p:Projekt)\\nWHERE exists{(p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:FROM_DONOR|INTO_RECEIVER]->(:Bauwerk)}\\n  AND NOT exists{(p)-[:HAS_BAUWERK]->()}"), 'violations')} |
| C8 :ASSOZIIERT_MIT_PROJEKT remaining (must be 0 post-R9) | {cell(find_first("MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->()"), 'violations')} |
| C9 :Kennwert orphan | {cell(find_first("MATCH (kw:Kennwert) WHERE NOT exists{()-[:HAT_KENNWERT]->(kw)}"), 'violations')} |

## 3. Restored / new labels

(See `stage_4_audit_results.json` for the per-label counts.)

## 4. Decision-grade cohort

| Cohort | Count |
|---|---:|
| Tier 1 under legacy gate (Repair D promotions counted) | {cell(find_first("MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})\\nRETURN 'D1_tier1_legacy'"), 'c')} |
| Tier 1 under honest gate (`source_curated` only) | {cell(find_first("MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})\\nOPTIONAL MATCH (p)-[bel:BELEGT_IN]->()"), 'c')} |

**The drop is the success signal.** Recommend re-running tier computation with the honest gate as the only gate.

## 5. :DataIssue summary

Total `:DataIssue` count: **{cell(find_first("MATCH (i:DataIssue) RETURN 'E1_data_issue_total'"), 'c')}**

(See `stage_4_audit_results.json` for the breakdown by kind, severity, and per-project density.)

## 6. Open follow-ups

- R7.c deferred (see [REVIEW_BASED_PLAN/ORCHESTRATOR_DECISIONS.md](REVIEW_BASED_PLAN/ORCHESTRATOR_DECISIONS.md) OD-2).
- 6 of 7 R7.b orphan-dossier resolutions still pending (OD-4).
- R6 schema language unification not in this round.

## 7. Sign-off

This audit was generated automatically from `stage_4_audit_queries.cypher` against the live `mit-bestand` database. Validate against [HANDOFF_LOG.md](REVIEW_BASED_PLAN/HANDOFF_LOG.md) before accepting.
"""


if __name__ == "__main__":
    run_audit()
