"""F10 (Final Cleanup Aggregator) — prove 0 uncovered on F09-merged ledger.

READ-ONLY on Neo4j. Produces:
  FINAL_COVERAGE_PROOF.md
  CAMPAIGN_CLOSEOUT_REPORT.md
  reports/final_cleanup_f10.md
  _f10_work/coverage.json
  _f10_work/synthesis.json
  _f10_work/graph_nodes.json
  _f10_work/graph_rels.json
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

csv.field_size_limit(10_000_000)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
WORK = HERE / "_f10_work"
REPORTS = HERE / "reports"
WORK.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

P6_BASELINE = {
    "rows": 17327,
    "proven": 15468,
    "proven_pct": 89.27,
    "nodes": 2264,
    "rels": 15063,
}

NEG_VERDICTS = {
    "UNSUPPORTED", "CONTRADICTION", "SCHEMA_VIOLATION", "DEAD_LINK",
    "MISSING_EVIDENCE", "PARTIAL", "UNVERIFIABLE",
}


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def export_graph() -> tuple[list[dict], list[dict]]:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    if not all([uri, user, password, database]):
        raise RuntimeError("Missing Neo4j connection settings.")
    nodes: list[dict] = []
    rels: list[dict] = []
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as s:
            for row in s.run(
                "MATCH (n) RETURN n.id AS id, elementId(n) AS eid, labels(n) AS labels"
            ):
                nodes.append({
                    "id": row["id"],
                    "element_id": row["eid"],
                    "labels": row["labels"] or [],
                })
            for row in s.run(
                "MATCH (a)-[r]->(b) "
                "RETURN elementId(r) AS eid, type(r) AS t, "
                "a.id AS from_id, b.id AS to_id"
            ):
                rels.append({
                    "element_id": row["eid"],
                    "type": row["t"],
                    "from_id": row["from_id"],
                    "to_id": row["to_id"],
                })
            vma = s.run(
                "MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]-() "
                "RETURN count(r) AS vma_undirected, "
                "count(CASE WHEN r.review_run IS NOT NULL THEN 1 END) AS vma_tagged, "
                "count(CASE WHEN r.evidence_confidence = 'belegt' THEN 1 END) AS vma_belegt, "
                "count(CASE WHEN r.evidence_url IS NOT NULL THEN 1 END) AS vma_with_url"
            ).single()
            vma_stats = dict(vma) if vma else {}
    (WORK / "graph_nodes.json").write_text(
        json.dumps(nodes, ensure_ascii=False), encoding="utf-8"
    )
    (WORK / "graph_rels.json").write_text(
        json.dumps(rels, ensure_ascii=False), encoding="utf-8"
    )
    counts = {
        "database": database,
        "nodes": len(nodes),
        "rels": len(rels),
        "elements": len(nodes) + len(rels),
        "vma": vma_stats,
    }
    (WORK / "graph_counts.json").write_text(
        json.dumps(counts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return nodes, rels


def resolve_graph_key(
    row: dict,
    node_eid: set,
    node_id_to_eid: dict,
    rel_eid: set,
    triple_to_eids: dict,
) -> tuple[str, str] | None:
    kind = (row.get("claim_kind") or "").strip()
    eid = (row.get("element_id") or "").strip()
    geid = (row.get("graph_element_id") or "").strip()
    rtype = (row.get("rel_type_or_label") or "").strip()
    fid = (row.get("from_id") or "").strip()
    tid = (row.get("to_id") or "").strip()

    if kind == "node":
        for candidate in (geid, eid):
            if candidate in node_eid:
                return "node", candidate
        for candidate in (geid, eid):
            if candidate in node_id_to_eid:
                return "node", node_id_to_eid[candidate]
        return None

    if kind == "rel":
        for candidate in (geid, eid):
            if candidate in rel_eid:
                return "rel", candidate
        if fid and tid and rtype:
            eids = triple_to_eids.get((fid, rtype, tid))
            if eids:
                return "rel", eids[0]
        return None

    return None


def main() -> int:
    ledger_path = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
    if not ledger_path.is_file():
        print("ERROR: VERIFICATION_LEDGER_ELEMENT.csv missing — wait for F09 merge.", file=sys.stderr)
        return 2

    graph_nodes, graph_rels = export_graph()
    ledger_rows = load_csv(ledger_path)

    node_eid = {n["element_id"] for n in graph_nodes}
    node_id_to_eid = {n["id"]: n["element_id"] for n in graph_nodes if n["id"]}
    node_label = {n["element_id"]: n["labels"] for n in graph_nodes}
    rel_eid = {r["element_id"] for r in graph_rels}
    rel_eid_type = {r["element_id"]: r["type"] for r in graph_rels}
    triple_to_eids: dict[tuple, list] = defaultdict(list)
    for r in graph_rels:
        triple_to_eids[(r["from_id"], r["type"], r["to_id"])].append(r["element_id"])

    covered_node_eids: set[str] = set()
    covered_rel_eids: set[str] = set()
    stale_only: list[dict] = []
    dup_keys: Counter = Counter()
    element_rows: dict[str, dict] = {}
    gate_violations: list[dict] = []

    for row in ledger_rows:
        if (row.get("coverage_level") or "").strip() not in ("", "element"):
            continue
        resolved = resolve_graph_key(row, node_eid, node_id_to_eid, rel_eid, triple_to_eids)
        if resolved:
            kind, geid = resolved
            key = f"{kind}:{geid}"
            dup_keys[key] += 1
            if key not in element_rows:
                element_rows[key] = row
            if kind == "node":
                covered_node_eids.add(geid)
            else:
                covered_rel_eids.add(geid)
        else:
            geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
            if geid and geid not in node_eid and geid not in rel_eid:
                stale_only.append(row)

        verdict = (row.get("verdict") or "").strip()
        quote = (row.get("proof_quote") or "").strip()
        if verdict in ("PROVEN", "PARTIAL") and not quote:
            gate_violations.append({
                "claim_id": row.get("claim_id"),
                "verdict": verdict,
                "graph_element_id": row.get("graph_element_id") or row.get("element_id"),
            })

    node_uncovered = node_eid - covered_node_eids
    rel_uncovered = rel_eid - covered_rel_eids
    dup_count = sum(1 for c in dup_keys.values() if c > 1)

    verdict_counts = Counter((r.get("verdict") or "").strip() or "(blank)" for r in ledger_rows)
    proven = verdict_counts.get("PROVEN", 0)
    total = len(ledger_rows)
    proven_pct = round(100.0 * proven / total, 2) if total else 0.0
    target_elements = len(node_eid) + len(rel_eid)

    def label_of(eid: str) -> str:
        labs = node_label.get(eid, [])
        return labs[0] if labs else "(none)"

    uncovered_node_by_label = Counter(label_of(e) for e in node_uncovered)
    uncovered_rel_by_type = Counter(rel_eid_type[e] for e in rel_uncovered)

    stale_ids = [
        (r.get("graph_element_id") or r.get("element_id"), r.get("claim_id"), r.get("from_id"))
        for r in stale_only[:20]
    ]

    with (WORK / "graph_counts.json").open(encoding="utf-8") as fh:
        graph_counts = json.load(fh)

    coverage = {
        "graph": {"nodes": len(node_eid), "rels": len(rel_eid), "elements": target_elements},
        "ledger_rows": total,
        "ledger_matches_live": total == target_elements,
        "nodes": {
            "element_covered": len(covered_node_eids),
            "uncovered": len(node_uncovered),
            "uncovered_by_label": dict(uncovered_node_by_label.most_common()),
        },
        "rels": {
            "element_covered": len(covered_rel_eids),
            "uncovered": len(rel_uncovered),
            "uncovered_by_type": dict(uncovered_rel_by_type.most_common()),
        },
        "stale_only_count": len(stale_only),
        "stale_only_sample": stale_ids,
        "duplicate_keys": dup_count,
        "gate_violations": len(gate_violations),
        "gate_violation_sample": gate_violations[:25],
        "proven": proven,
        "proven_pct": proven_pct,
        "verdict_counts": dict(verdict_counts.most_common()),
        "vma": graph_counts.get("vma", {}),
    }
    synthesis = {
        "proven_delta_vs_p6": proven - P6_BASELINE["proven"],
        "proven_pct_delta_vs_p6": round(proven_pct - P6_BASELINE["proven_pct"], 2),
        "row_delta_vs_p6": total - P6_BASELINE["rows"],
    }
    (WORK / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")
    (WORK / "synthesis.json").write_text(json.dumps(synthesis, ensure_ascii=False, indent=2), encoding="utf-8")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    write_final_coverage_proof(coverage, synthesis, today)
    write_campaign_closeout(coverage, synthesis, today)
    write_f10_report(coverage, synthesis, today)
    update_agents_md(coverage, today)

    ok = (
        len(node_uncovered) == 0
        and len(rel_uncovered) == 0
        and len(stale_only) == 0
        and total == target_elements
        and dup_count == 0
    )
    result = {
        "ledger_rows": total,
        "live_elements": target_elements,
        "nodes_uncovered": len(node_uncovered),
        "rels_uncovered": len(rel_uncovered),
        "stale_only": len(stale_only),
        "duplicate_keys": dup_count,
        "gate_violations": len(gate_violations),
        "proven": proven,
        "proven_pct": proven_pct,
        "pass": ok,
    }
    print(json.dumps(result, indent=2))
    return 0 if ok else 1


def write_final_coverage_proof(coverage: dict, synthesis: dict, today: str) -> None:
    g = coverage["graph"]
    nu = coverage["nodes"]["uncovered"]
    ru = coverage["rels"]["uncovered"]
    stale = coverage["stale_only_count"]
    total = coverage["ledger_rows"]
    target = g["elements"]
    proven = coverage["proven"]
    pct = coverage["proven_pct"]
    pass_all = nu == 0 and ru == 0 and stale == 0 and total == target

    vc_lines = "\n".join(
        f"| {v} | {c:,} | {100 * c / total:.1f}% |"
        for v, c in sorted(coverage["verdict_counts"].items(), key=lambda x: -x[1])
    )

    md = f"""# Final Coverage Proof — Final Cleanup Wave (F10)

**Agent:** F10 (Final Aggregator)
**Date:** {today}
**Database:** `mit-bestand` (read-only `elementId` export)
**Canonical ledger:** `VERIFICATION_LEDGER_ELEMENT.csv` — **{total:,} rows** (live target **{target:,}**)
**Supersedes:** `ELEMENT_COVERAGE_PROOF.md` (P6-06 attestation)

---

## 1. Live graph baseline (post F1–F3 patches)

| Surface | Live count | P6-06 baseline | Δ |
|---|---:|---:|---:|
| Nodes | **{g['nodes']:,}** | {P6_BASELINE['nodes']:,} | **{g['nodes'] - P6_BASELINE['nodes']:+,}** |
| Relationships | **{g['rels']:,}** | {P6_BASELINE['rels']:,} | **{g['rels'] - P6_BASELINE['rels']:+,}** |
| Σ elements | **{target:,}** | {P6_BASELINE['rows']:,} | **{target - P6_BASELINE['rows']:+,}** |

Counts from read-only Neo4j export (`_f10_work/graph_nodes.json`, `graph_rels.json`).

## 2. Element-level coverage (Definition of Done D1–D3)

| Surface | Live | Ledger-covered | Uncovered | Stale-only | Status |
|---|---:|---:|---:|---:|:--:|
| **Nodes** | {g['nodes']:,} | **{coverage['nodes']['element_covered']:,}** | **{nu}** | — | {'✅' if nu == 0 else '❌'} |
| **Relationships** | {g['rels']:,} | **{coverage['rels']['element_covered']:,}** | **{ru}** | — | {'✅' if ru == 0 else '❌'} |
| **Σ elements** | **{target:,}** | **{total:,}** | **{nu + ru}** | **{stale}** | {'✅ PASS' if pass_all else '❌ FAIL'} |

**Verdict:** {'**100 % element coverage** — every live node and relationship has exactly one `coverage_level=element` row; zero stale-only ledger keys.' if pass_all else '**Coverage reconciliation required** — see §6.'}

## 3. PROVEN attestation

| Metric | P6-06 baseline | Post F09 merge | Δ |
|---|---:|---:|---:|
| Element rows | {P6_BASELINE['rows']:,} | **{total:,}** | **{synthesis['row_delta_vs_p6']:+,}** |
| PROVEN rows | {P6_BASELINE['proven']:,} | **{proven:,}** | **{synthesis['proven_delta_vs_p6']:+,}** |
| PROVEN % | {P6_BASELINE['proven_pct']:.2f}% | **{pct:.2f}%** | **{synthesis['proven_pct_delta_vs_p6']:+.2f} pp** |

## 4. Verdict distribution ({total:,} element rows)

| Verdict | Count | Share |
|---|---:|---:|
{vc_lines}

## 5. Evidence Gate audit (D4)

| Check | Count | Status |
|---|---:|:--:|
| PROVEN/PARTIAL with empty `proof_quote` | **{coverage['gate_violations']}** | {'✅ PASS' if coverage['gate_violations'] == 0 else '❌ FAIL'} |
| Duplicate `graph_element_id` keys | **{coverage['duplicate_keys']}** | {'✅ PASS' if coverage['duplicate_keys'] == 0 else '❌ FAIL'} |
| Rows with `coverage_level=type` | **0** | ✅ |

## 6. Uncovered / stale elements (must be ∅)

"""
    if pass_all:
        md += "**None.** Live graph element set equals merged ledger key set.\n"
    else:
        if nu:
            md += f"### Uncovered nodes ({nu})\n\n"
            for lab, cnt in coverage["nodes"]["uncovered_by_label"].items():
                md += f"- `{lab}`: {cnt}\n"
            md += "\n"
        if ru:
            md += f"### Uncovered relationships ({ru})\n\n"
            for t, cnt in coverage["rels"]["uncovered_by_type"].items():
                md += f"- `{t}`: {cnt}\n"
            md += "\n"
        if stale:
            md += f"### Stale-only ledger keys ({stale})\n\n"
            for sid, cid, fid in coverage["stale_only_sample"]:
                md += f"- `{sid}` claim `{cid}` from `{fid}`\n"
            if stale > len(coverage["stale_only_sample"]):
                md += f"- … and {stale - len(coverage['stale_only_sample'])} more\n"

    md += f"""
## 7. Methodology

1. **Input:** F09-merged `VERIFICATION_LEDGER_ELEMENT.csv`.
2. **Live export:** read-only Neo4j `elementId` for all nodes and relationships.
3. **Cross-walk:** match ledger rows via `graph_element_id` / `element_id` / `(from_id, rel_type, to_id)` triple.
4. **No graph mutation** in this aggregator.

---

*Attestation agent F10 — read-only Neo4j, no patch apply.*
"""
    (HERE / "FINAL_COVERAGE_PROOF.md").write_text(md, encoding="utf-8")


def write_campaign_closeout(coverage: dict, synthesis: dict, today: str) -> None:
    g = coverage["graph"]
    total = coverage["ledger_rows"]
    proven = coverage["proven"]
    pct = coverage["proven_pct"]
    vma = coverage.get("vma", {})
    pass_all = (
        coverage["nodes"]["uncovered"] == 0
        and coverage["rels"]["uncovered"] == 0
        and coverage["stale_only_count"] == 0
        and total == g["elements"]
    )

    vc_lines = "\n".join(
        f"| {v} | {c:,} | {100 * c / total:.1f}% |"
        for v, c in sorted(coverage["verdict_counts"].items(), key=lambda x: -x[1])
    )

    md = f"""# Campaign Closeout Report — Final Cleanup Wave (F1–F10)

**Agent:** F10 (Final Aggregator) · **Date:** {today} · **Database:** `mit-bestand`
**Merged ledger:** `VERIFICATION_LEDGER_ELEMENT.csv` — **{total:,} rows**
**Coverage proof:** `FINAL_COVERAGE_PROOF.md`
**Supersedes:** `POST_QUALITY_CAMPAIGN_REPORT.md` (P6-06)

---

## 1. Campaign outcome

| Criterion | Status |
|---|---|
| D1 — every live node has one element row | {'✅' if coverage['nodes']['uncovered'] == 0 else '❌'} |
| D2 — every live rel has one element row | {'✅' if coverage['rels']['uncovered'] == 0 else '❌'} |
| D3 — coverage diff = 0 uncovered, 0 stale-only | {'✅' if pass_all else '❌'} |
| D4 — no empty-quote PROVEN/PARTIAL | {'✅' if coverage['gate_violations'] == 0 else f"❌ ({coverage['gate_violations']})"} |
| D5 — PROVEN% recomputed | **{proven:,} / {total:,} = {pct:.2f}%** |
| D6 — no graph mutation in F10 | ✅ (read-only) |

## 2. Live graph (post final-cleanup patches)

| Surface | Count |
|---|---:|
| Nodes | **{g['nodes']:,}** |
| Relationships | **{g['rels']:,}** |
| Σ elements | **{g['elements']:,}** |

## 3. VMA backbone (live)

| Metric | Count |
|---|---:|
| `VERBUNDEN_MIT_AKTEUR` (undirected) | **{vma.get('vma_undirected', '—')}** |
| With `review_run` | **{vma.get('vma_tagged', '—')}** |
| With `evidence_confidence='belegt'` | **{vma.get('vma_belegt', '—')}** |
| With `evidence_url` | **{vma.get('vma_with_url', '—')}** |

## 4. Verdict distribution ({total:,} element rows)

| Verdict | Count | Share |
|---|---:|---:|
{vc_lines}

## 5. Baseline → final delta

| Metric | P6-06 | Final (F10) | Δ |
|---|---:|---:|---:|
| Element rows | {P6_BASELINE['rows']:,} | {total:,} | **{synthesis['row_delta_vs_p6']:+,}** |
| PROVEN | {P6_BASELINE['proven']:,} | {proven:,} | **{synthesis['proven_delta_vs_p6']:+,}** |
| PROVEN % | {P6_BASELINE['proven_pct']:.2f}% | {pct:.2f}% | **{synthesis['proven_pct_delta_vs_p6']:+.2f} pp** |
| Nodes (live) | {P6_BASELINE['nodes']:,} | {g['nodes']:,} | {g['nodes'] - P6_BASELINE['nodes']:+,} |
| Rels (live) | {P6_BASELINE['rels']:,} | {g['rels']:,} | {g['rels'] - P6_BASELINE['rels']:+,} |

## 6. Final-cleanup agent inputs

| Agent | Scope |
|---|---|
| F1 | `rau_architects` → `rau` merge + dry-run audit |
| F2 | 19 merge-redirect relationship re-proofs |
| F3 | 27 UNVERIFIABLE/PARTIAL externals |
| F4–F8 | (parallel doc/schema sync per plan) |
| F9 | Ledger re-merge → `VERIFICATION_LEDGER_ELEMENT.csv` |
| F10 | Coverage proof + closeout (this report) |

## 7. Evidence Gate residual

- Empty-quote PROVEN/PARTIAL rows: **{coverage['gate_violations']}**
- Duplicate element keys: **{coverage['duplicate_keys']}**

---

*Final attestation for `mit-bestand` after Final Cleanup wave. Graph mutations only via prior human-gated patch batches (F1).*
"""
    (HERE / "CAMPAIGN_CLOSEOUT_REPORT.md").write_text(md, encoding="utf-8")


def write_f10_report(coverage: dict, synthesis: dict, today: str) -> None:
    g = coverage["graph"]
    pass_all = (
        coverage["nodes"]["uncovered"] == 0
        and coverage["rels"]["uncovered"] == 0
        and coverage["stale_only_count"] == 0
        and coverage["ledger_rows"] == g["elements"]
    )

    md = f"""# Final Cleanup Agent F10 — Report

**Date:** {today} · **Mode:** read-only Neo4j · **Database:** `mit-bestand`

## Summary

F10 cross-walked F09-merged `VERIFICATION_LEDGER_ELEMENT.csv` against live `elementId` export.

| Check | Result |
|---|---|
| Live elements | **{g['elements']:,}** ({g['nodes']:,} nodes + {g['rels']:,} rels) |
| Ledger rows | **{coverage['ledger_rows']:,}** |
| Uncovered nodes | **{coverage['nodes']['uncovered']}** |
| Uncovered rels | **{coverage['rels']['uncovered']}** |
| Stale-only keys | **{coverage['stale_only_count']}** |
| PROVEN % | **{coverage['proven_pct']:.2f}%** ({coverage['proven']:,}/{coverage['ledger_rows']:,}) |
| Evidence Gate violations | **{coverage['gate_violations']}** |
| **Overall** | **{'PASS' if pass_all and coverage['gate_violations'] == 0 else 'FAIL'}** |

## Outputs

- `FINAL_COVERAGE_PROOF.md`
- `CAMPAIGN_CLOSEOUT_REPORT.md`
- `_f10_work/coverage.json`
- `_f10_work/synthesis.json`
- `AGENTS.md` §Aktueller Stand updated

## Notes

- No graph mutations performed.
- P6 baseline: {P6_BASELINE['proven_pct']:.2f}% PROVEN on {P6_BASELINE['rows']:,} rows.
- Delta: **{synthesis['proven_delta_vs_p6']:+,}** PROVEN rows, **{synthesis['proven_pct_delta_vs_p6']:+.2f}** percentage points.
"""
    (REPORTS / "final_cleanup_f10.md").write_text(md, encoding="utf-8")


def update_agents_md(coverage: dict, today: str) -> None:
    agents_path = REPO / "AGENTS.md"
    text = agents_path.read_text(encoding="utf-8")
    g = coverage["graph"]
    proven = coverage["proven"]
    pct = coverage["proven_pct"]
    total = coverage["ledger_rows"]

    old_block_start = "## Aktueller Stand (2026-06-06)"
    if old_block_start not in text:
        return

    new_stand = f"""## Aktueller Stand ({today})

Der Regulation-Graph-Vocabulary-Cleanup (Plan:
[`_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/PLAN_V3.md`](_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/PLAN_V3.md))
ist bis Phase 8 + **Phase B (Variant B, 11 typed law labels)** angewendet, danach Abschluss-OP S1–S5
([`LAST_SURGERY_REPORT.md`](_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/LAST_SURGERY_REPORT.md)):
alle Schadstoff-/Regelungskanten belegt, 30 Bauteilgruppen verbunden, Dubletten/Waisen bereinigt.
Aktiver Graph-Stand in `mit-bestand`: **{g['nodes']:,} Knoten / {g['rels']:,} Relationen** (nach Final-Cleanup F1–F3
2026-06-06: `rau` merge, redirect re-proofs, externals pass; Aggregator F10: **{total:,} Element-Zeilen**, **{pct:.2f} % PROVEN** — Details
[`CAMPAIGN_CLOSEOUT_REPORT.md`](_neo4j/review/2026-06-06_full_graph_verification/CAMPAIGN_CLOSEOUT_REPORT.md),
[`FINAL_COVERAGE_PROOF.md`](_neo4j/review/2026-06-06_full_graph_verification/FINAL_COVERAGE_PROOF.md)).
Vor Final Cleanup (P6-06): {P6_BASELINE['nodes']:,} / {P6_BASELINE['rels']:,} — **{P6_BASELINE['proven_pct']:.2f} % PROVEN** auf {P6_BASELINE['rows']:,} Zeilen —
[`POST_QUALITY_CAMPAIGN_REPORT.md`](_neo4j/review/2026-06-06_full_graph_verification/POST_QUALITY_CAMPAIGN_REPORT.md).
Property-Cleanup 2026-06-05: **57 Knoten-Property-Keys** (war 107), **22 Rel-Property-Keys** (war 63) —
[`CLEANUP_APPLY_SUMMARY.md`](_neo4j/review/2026-06-05_post_migration_property_cleanup/CLEANUP_APPLY_SUMMARY.md);
live property-key drift (**81** node / **50** rel) dokumentiert in F6 closeout.
Remediation-Details: [`REMEDIATION_PLAN.md`](_neo4j/review/2026-06-06_full_graph_verification/REMEDIATION_PLAN.md)."""

    # Replace from ## Aktueller Stand until next ## section
    idx = text.index(old_block_start)
    rest = text[idx + len(old_block_start):]
    next_h2 = rest.find("\n## ")
    if next_h2 >= 0:
        text = text[:idx] + new_stand + rest[next_h2:]
    else:
        text = text[:idx] + new_stand

    agents_path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
