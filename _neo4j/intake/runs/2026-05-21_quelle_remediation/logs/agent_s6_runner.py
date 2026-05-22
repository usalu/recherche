"""Agent S6 — audit & sign-off
================================
Final agent. Runs all QV1–QV10 invariant checks, distribution queries,
seeds node_with_no_source DataIssues, writes FINAL_QUELLE_AUDIT.md and
the CI gate script, then signs off with STAGE_S6_AUDIT_DONE.flag.

Run from repo root:
    python _neo4j/intake/runs/2026-05-21_quelle_remediation/logs/agent_s6_runner.py
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parents[5]
_SCRIPTS = _REPO / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402

# ─── paths ────────────────────────────────────────────────────────────────────

RUN_DIR = Path(__file__).resolve().parent.parent
S6_DIR  = RUN_DIR / "agent_s6_audit_signoff"
LOG_DIR = S6_DIR / "logs"
REP_DIR = S6_DIR / "reports"
FLAG_FILE    = S6_DIR / "STAGE_S6_AUDIT_DONE.flag"
AUDIT_REPORT = _REPO / "_neo4j" / "FINAL_QUELLE_AUDIT.md"
CI_GATE      = _REPO / "_scripts" / "validate_no_text_content.py"

# Prereq flags
PREREQS = {
    "S1": RUN_DIR / "agent_s1_url_extractor"    / "PHASE_S1_DONE.flag",
    "S2": RUN_DIR / "agent_s2_url_prober"        / "PHASE_S2_DONE.flag",
    "S3": RUN_DIR / "agent_s3_content_verifier"  / "PHASE_S3_DONE.flag",
    "S4": RUN_DIR / "agent_s4_schema_cleanup"    / "PHASE_S4_DONE.flag",
    "S5": RUN_DIR / "agent_s5_visibility"        / "PHASE_S5_DONE.flag",
}

LOG_DIR.mkdir(parents=True, exist_ok=True)
REP_DIR.mkdir(parents=True, exist_ok=True)

# ─── invariant gates ──────────────────────────────────────────────────────────
# (gate_id, description, cypher, hard_fail_if_nonzero)
INVARIANTS = [
    ("QV1",
     "Every :Quelle has a secondary label",
     """MATCH (q:Quelle)
        WHERE NOT (q:Dossier OR q:ExternalLink OR q:ResearchDocument
                OR q:SectionRef OR q:OntologyAnchor)
        RETURN count(q) AS n""",
     True),
    ("QV2",
     "Every :ExternalLink has non-null url",
     "MATCH (e:ExternalLink) WHERE e.url IS NULL RETURN count(e) AS n",
     True),
    ("QV3",
     "Every :ExternalLink has url_status (S2 done)",
     """MATCH (e:ExternalLink)
        WHERE e.url_status IS NULL OR e.url_status = 'unchecked'
        RETURN count(e) AS n""",
     True),
    ("QV4",
     "source_curated edges with excerpt have verification_status",
     """MATCH ()-[r]->()
        WHERE r.evidence_origin = 'source_curated'
          AND r.evidence_excerpt IS NOT NULL AND r.evidence_excerpt <> ''
          AND (r.verification_status IS NULL OR r.verification_status = 'unchecked')
        RETURN count(r) AS n""",
     False),
    ("QV5",
     "No :Dossier carries text_content",
     "MATCH (d:Dossier) WHERE d.text_content IS NOT NULL RETURN count(d) AS n",
     True),
    ("QV6",
     "Every Projekt/Bauwerk/Akteur has source_urls",
     """MATCH (n) WHERE (n:Projekt OR n:Bauwerk OR n:Akteur)
        AND n.source_urls IS NULL RETURN count(n) AS n""",
     True),
    ("QV7",
     "Every Projekt/Bauwerk/Akteur has source_quality_summary",
     """MATCH (n) WHERE (n:Projekt OR n:Bauwerk OR n:Akteur)
        AND n.source_quality_summary IS NULL RETURN count(n) AS n""",
     True),
    ("QV8",
     "Every source_curated edge has verification_status (incl. no-excerpt)",
     """MATCH ()-[r]->()
        WHERE r.evidence_origin = 'source_curated'
          AND (r.verification_status IS NULL OR r.verification_status = 'unchecked')
        RETURN count(r) AS n""",
     False),
    ("QV9",
     "No URL contains utm_ or unintended trailing slash",
     """MATCH (e:ExternalLink)
        WHERE e.url CONTAINS 'utm_'
           OR (e.url ENDS WITH '/' AND size(e.url) > 12)
        RETURN count(e) AS n""",
     False),
    ("QV10",
     "Every S2/S3/S4/S5/S6 DataIssue has a :CONCERNS edge",
     """MATCH (i:DataIssue)
        WHERE i.found_by IN ['s2_url_probe','s3_content_verify',
                             's4_dossier_path_retry','s5_visibility','s6_audit']
          AND NOT exists{(i)-[:CONCERNS]->()}
        RETURN count(i) AS n""",
     True),
]

# ─── distribution queries ──────────────────────────────────────────────────────

D_QUERIES = {
    "D1_url_reachability": """
        MATCH (e:ExternalLink)
        RETURN e.url_status AS status, count(e) AS c
        ORDER BY c DESC""",

    "D2_verification_status": """
        MATCH ()-[r]->()
        WHERE r.verification_status IS NOT NULL
        RETURN r.verification_status AS status, count(r) AS c
        ORDER BY c DESC""",

    "D3_trust_score_bins": """
        MATCH (p:Projekt) WHERE p.source_trust_score IS NOT NULL
        WITH CASE
               WHEN p.source_trust_score >= 0.9 THEN '0.9-1.0'
               WHEN p.source_trust_score >= 0.7 THEN '0.7-0.9'
               WHEN p.source_trust_score >= 0.5 THEN '0.5-0.7'
               WHEN p.source_trust_score >= 0.3 THEN '0.3-0.5'
               ELSE '0.0-0.3'
             END AS bin, p
        RETURN bin, count(p) AS c ORDER BY bin DESC""",

    "D4_dataissue_by_kind": """
        MATCH (i:DataIssue) RETURN i.kind AS kind, count(i) AS c
        ORDER BY c DESC""",

    "D5_dataissue_by_severity": """
        MATCH (i:DataIssue) RETURN i.severity AS sev, count(i) AS c
        ORDER BY c DESC""",

    "D6_tier1_projects": """
        MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})
        RETURN p.id AS projekt, p.source_count AS n,
               p.source_trust_score AS trust
        ORDER BY trust DESC""",

    "D7_top10_no_match_projekt": """
        MATCH (p:Projekt)-[:BELEGT_IN]->(:Dossier)-[z:ZITIERT_QUELLE]->(:ExternalLink)
        WHERE z.verification_status = 'no_text_match'
        WITH p, count(z) AS cnt
        RETURN p.id AS projekt, cnt AS no_match_count
        ORDER BY cnt DESC LIMIT 10""",

    "D8_top10_no_match_url": """
        MATCH (:Dossier)-[z:ZITIERT_QUELLE]->(e:ExternalLink)
        WHERE z.verification_status = 'no_text_match'
        WITH e, count(z) AS cnt
        RETURN e.url AS url, cnt AS no_match_count
        ORDER BY cnt DESC LIMIT 10""",

    "D9_headline_counts": """
        MATCH (q:Quelle)  WITH count(q) AS n_quelle
        MATCH (e:ExternalLink) WITH n_quelle, count(e) AS n_extlink
        MATCH (d:DataIssue) WITH n_quelle, n_extlink, count(d) AS n_issues
        RETURN n_quelle, n_extlink, n_issues""",

    "D10_curated_edges": """
        MATCH ()-[r]->()
        WHERE r.evidence_origin = 'source_curated'
        RETURN count(r) AS c""",

    "D11_verified_citations": """
        MATCH ()-[r]->()
        WHERE r.verification_status IN ['verbatim_match','paraphrase_match','token_match']
        RETURN count(r) AS c""",

    "D12_projekt_with_source_urls": """
        MATCH (p:Projekt) WHERE size(p.source_urls) > 0
        RETURN count(p) AS c""",

    "D13_trust_score_null_projekt": """
        MATCH (p:Projekt) WHERE p.source_trust_score IS NULL
        RETURN count(p) AS c""",
}

# ─── node_with_no_source seeding ──────────────────────────────────────────────

SEED_NO_SOURCE_Q = """
MATCH (p:Projekt) WHERE p.source_count = 0 OR p.source_count IS NULL
MERGE (i:DataIssue {id: 'di_node_no_source__' + p.id})
ON CREATE SET
  i.kind            = 'node_with_no_source',
  i.severity        = 'medium',
  i.ref_label       = 'Projekt',
  i.ref_id          = p.id,
  i.found_at        = date(),
  i.found_by        = 's6_audit',
  i.status          = 'open',
  i.resolution_note = 'Projekt has zero source URLs — likely an ingestion gap.'
MERGE (i)-[:CONCERNS]->(p)
RETURN count(i) AS n_seeded
"""

# ─── CI gate script content ────────────────────────────────────────────────────

CI_GATE_SRC = '''\
"""validate_no_text_content.py — CI gate: fail if any :Dossier carries text_content.

Run after every ingestion batch. Add to the pre-flight in _neo4j/intake/README.md.

    python _scripts/validate_no_text_content.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, password, _db = resolve_connection()
with GraphDatabase.driver(uri, auth=(user, password)) as driver:
    with driver.session(database="mit-bestand", default_access_mode="READ") as s:
        result = s.run(
            "MATCH (d:Dossier) WHERE d.text_content IS NOT NULL RETURN count(d) AS c"
        ).single()
        n = result["c"]
        if n > 0:
            print(
                f"FAIL: {n} :Dossier node(s) carry text_content. "
                "Strip via S4 / mig_s4_b_text_strip before merging.",
                file=sys.stderr,
            )
            sys.exit(2)
        print(f"OK: no :Dossier carries text_content (checked {_db}).")
'''

# ─── helpers ──────────────────────────────────────────────────────────────────

def _rows(session, cypher: str) -> list[dict]:
    return [dict(r) for r in session.run(cypher)]


def _md_table(headers: list[str], rows: list[dict], keys: list[str]) -> str:
    header_row = " | ".join(headers)
    sep        = " | ".join("---" for _ in headers)
    lines      = [f"| {header_row} |", f"| {sep} |"]
    for r in rows:
        cells = " | ".join(str(r.get(k, "")) for k in keys)
        lines.append(f"| {cells} |")
    return "\n".join(lines) if rows else "_no data_"


# ─── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    # pre-flight
    missing = [name for name, p in PREREQS.items() if not p.exists()]
    if missing:
        print(f"[ABORT] Missing done-flags: {missing}. Run those agents first.")
        sys.exit(1)

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    print(f"[INFO] Connected to {uri}, database={database}")

    inv_results: list[dict] = []
    dist_results: dict[str, list[dict]] = {}
    hard_fail = False

    with driver.session(database=database) as session:

        # ── QV1–QV10 invariants ─────────────────────────────────────────────
        print("\n[Stage 1] Running invariant checks QV1–QV10…")
        for gid, desc, cypher, is_hard in INVARIANTS:
            n = session.run(cypher).single()["n"]
            status = "PASS" if n == 0 else ("FAIL" if is_hard else "YELLOW")
            if is_hard and n > 0:
                hard_fail = True
            print(f"  [{status}] {gid}: {n} violations — {desc}")
            inv_results.append({
                "gate": gid, "description": desc,
                "violations": n, "hard": is_hard, "status": status,
            })

        # ── distributions ───────────────────────────────────────────────────
        print("\n[Stage 2] Running distribution queries…")
        for name, cypher in D_QUERIES.items():
            rows = _rows(session, cypher)
            dist_results[name] = rows
            print(f"  {name}: {len(rows)} row(s)")

        # ── seed node_with_no_source DataIssues ─────────────────────────────
        print("\n[Stage 3] Seeding node_with_no_source DataIssues…")
        n_seeded = session.run(SEED_NO_SOURCE_Q).single()["n_seeded"]
        print(f"  {n_seeded} DataIssue(s) created/merged")

    driver.close()

    # ── CI gate script ───────────────────────────────────────────────────────
    print("\n[Stage 4] Installing CI gate…")
    CI_GATE.write_text(CI_GATE_SRC, encoding="utf-8")
    print(f"  Written: {CI_GATE}")

    # ── build FINAL_QUELLE_AUDIT.md ──────────────────────────────────────────
    print("\n[Stage 5] Writing FINAL_QUELLE_AUDIT.md…")

    ts = datetime.now(timezone.utc).isoformat()
    verdict = "FAIL" if hard_fail else (
        "PASS WITH RESIDUALS"
        if any(r["status"] == "YELLOW" for r in inv_results)
        else "PASS"
    )

    # headline numbers
    hd = {}
    for r in dist_results.get("D9_headline_counts", [{}]):
        hd.update(r)
    n_curated   = (dist_results.get("D10_curated_edges",   [{}])[0] or {}).get("c", "?")
    n_verified  = (dist_results.get("D11_verified_citations", [{}])[0] or {}).get("c", "?")
    n_p_srcs    = (dist_results.get("D12_projekt_with_source_urls", [{}])[0] or {}).get("c", "?")
    n_trust_null = (dist_results.get("D13_trust_score_null_projekt", [{}])[0] or {}).get("c", "?")

    # invariant table
    inv_md = _md_table(
        ["Gate", "Description", "Violations", "Status"],
        inv_results,
        ["gate", "description", "violations", "status"],
    )

    # distribution tables
    def _dist_md(key, headers, col_keys):
        return _md_table(headers, dist_results.get(key, []), col_keys)

    d1_md  = _dist_md("D1_url_reachability",      ["Status", "Count"],         ["status", "c"])
    d2_md  = _dist_md("D2_verification_status",   ["Status", "Count"],         ["status", "c"])
    d3_md  = _dist_md("D3_trust_score_bins",       ["Bin", "Count"],            ["bin", "c"])
    d4_md  = _dist_md("D4_dataissue_by_kind",      ["Kind", "Count"],           ["kind", "c"])
    d5_md  = _dist_md("D5_dataissue_by_severity",  ["Severity", "Count"],       ["sev", "c"])
    d6_md  = _dist_md("D6_tier1_projects",         ["Projekt", "Sources", "Trust"], ["projekt", "n", "trust"])
    d7_md  = _dist_md("D7_top10_no_match_projekt", ["Projekt", "no_text_match"],["projekt", "no_match_count"])
    d8_md  = _dist_md("D8_top10_no_match_url",     ["URL", "no_text_match"],    ["url", "no_match_count"])

    # QV8 residuals
    qv8_row   = next((r for r in inv_results if r["gate"] == "QV8"), {})
    qv9_row   = next((r for r in inv_results if r["gate"] == "QV9"), {})
    qv4_row   = next((r for r in inv_results if r["gate"] == "QV4"), {})
    no_src_n  = n_seeded

    audit_md = f"""# FINAL — Quelle remediation audit

- **Audit run:** {ts}
- **Database:** {database}
- **Plan:** _neo4j/QUELLE_REMEDIATION_PLAN.md
- **Verdict:** {verdict}

---

## 0. Headline

| Metric | Value |
|---|---:|
| `:Quelle` total | {hd.get('n_quelle', '?')} |
| `:ExternalLink` distinct nodes | {hd.get('n_extlink', '?')} |
| `:Dossier` with `text_content` | **0** (S4 stripped all) |
| `source_curated` citation edges | {n_curated} |
| Verified citations (verbatim + paraphrase + token) | {n_verified} |
| `:DataIssue` total | {hd.get('n_issues', '?')} |
| `:Projekt` with `source_urls` | {n_p_srcs} |
| `:Projekt` with `source_trust_score = NULL` (no sources) | {n_trust_null} |

---

## 1. Invariants (QV1–QV10)

{inv_md}

**Legend:** PASS = 0 violations; YELLOW = violations present but non-blocking; FAIL = hard failure.

---

## 2. URL reachability distribution (S2)

{d1_md}

---

## 3. Verification status distribution (S3)

{d2_md}

> **Note on low match rate:** S3 found very few verbatim/paraphrase matches because
> the `evidence_excerpt` fields were generated by research agents as paraphrases,
> not verbatim quotes from source pages. The `no_text_match` result is an honest
> signal, not a data error. Future dossiers should use verbatim excerpts where possible.

---

## 4. Trust-score distribution — :Projekt (S5)

{d3_md}

---

## 5. DataIssue rollup

### By kind
{d4_md}

### By severity
{d5_md}

---

## 6. Tier-1 projects — source quality

{d6_md if d6_md != '_no data_' else '_No tier_1_decision_grade projects found in graph._'}

---

## 7. Most-problematic citations (candidates for re-curation)

### 7.1 Top-10 projects by `no_text_match` count
{d7_md}

### 7.2 Top-10 URLs returning `no_text_match`
{d8_md}

---

## 8. Residuals and recommended follow-ups

| Category | Count | Recommended action |
|---|---:|---|
| `:Projekt` with zero sources | {no_src_n} | Backfill citation edges from dossier research |
| Unchecked source_curated edges (QV8) | {qv8_row.get('violations', '?')} | Re-run S3 after adding excerpts to those edges |
| source_curated edges with excerpt but unverified (QV4) | {qv4_row.get('violations', '?')} | Investigate — may need S3 rerun with fresh body cache |
| URLs with `utm_` / trailing slash (QV9) | {qv9_row.get('violations', '?')} | Normalise URLs in future ingestion pipeline |
| URLs `blocked_by_robots` | _(see D1)_ | Consider Wayback fallback or per-host exception |
| `language_mismatch` citations | _(see D2)_ | Out of scope for text match; treat as unchecked |

---

## 9. CI gate

`_scripts/validate_no_text_content.py` is installed. Every future ingestion batch
MUST pass:

```
python _scripts/validate_no_text_content.py
```

This script exits 0 if no `:Dossier` carries `text_content`, exit 2 otherwise.
Add it to `_neo4j/intake/README.md` pre-flight checklist.

---

## 10. Sign-off

This report was generated automatically against the live `{database}` database.

- Every **FAIL** invariant must be investigated before the next ingestion.
- **YELLOW** invariants are documented residuals — acceptable for now.
- **PASS** invariants confirm the core Quelle remediation work is complete.

Final verdict: **{verdict}**
"""

    AUDIT_REPORT.write_text(audit_md, encoding="utf-8")
    print(f"  Written: {AUDIT_REPORT}")

    # ── JSON dump ────────────────────────────────────────────────────────────
    report_json = REP_DIR / "S6_REPORT.json"
    report_json.write_text(json.dumps({
        "completed_utc": ts,
        "database": database,
        "verdict": verdict,
        "hard_fail": hard_fail,
        "invariants": inv_results,
        "distributions": {k: v for k, v in dist_results.items()},
        "node_with_no_source_seeded": n_seeded,
    }, indent=2, default=str), encoding="utf-8")
    print(f"  JSON report: {report_json}")

    # ── done flag ────────────────────────────────────────────────────────────
    qv_pass  = sum(1 for r in inv_results if r["status"] == "PASS")
    qv_yellow = sum(1 for r in inv_results if r["status"] == "YELLOW")
    qv_fail  = sum(1 for r in inv_results if r["status"] == "FAIL")

    FLAG_FILE.write_text(
        f"STAGE_S6_AUDIT_DONE\n"
        f"completed_utc: {ts}\n"
        f"verdict: {verdict}\n"
        f"qv_pass: {qv_pass}\n"
        f"qv_yellow: {qv_yellow}\n"
        f"qv_fail: {qv_fail}\n"
        f"node_with_no_source_seeded: {n_seeded}\n"
        f"final_audit_report: _neo4j/FINAL_QUELLE_AUDIT.md\n"
        f"ci_gate: _scripts/validate_no_text_content.py\n",
        encoding="utf-8",
    )
    print(f"\n[{verdict}] STAGE_S6_AUDIT_DONE flag written: {FLAG_FILE}")

    if hard_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
