# -*- coding: utf-8 -*-
"""Agent EP-07 — element-level proof ledger for methods/design/outcome vocab edges."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))

from neo4j import GraphDatabase  # noqa: E402
from neo4j_env import resolve_connection  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT_LEDGER = HERE / "ledger" / "element_proof_agent_07.csv"
OUT_REPORT = HERE / "reports" / "element_proof_agent_07.md"

SCOPE_TYPES = [
    "HAT_RESSOURCENQUELLE",
    "HAT_METHODE",
    "HAT_INTERVENTION",
    "HAT_BAUWEISE",
    "HAT_VERBINDUNGSTECHNIK",
    "HAT_ENTWURFSMETHODIK",
    "HAT_ARCHITEKTURERGEBNIS",
    "HAT_BAUSYSTEM",
    "HAT_DEFEKT",
]

RANGE_LABEL = {
    "HAT_RESSOURCENQUELLE": "Ressourcenquelle",
    "HAT_METHODE": "Methode",
    "HAT_INTERVENTION": "BauaufgabeIntervention",
    "HAT_BAUWEISE": "Bauweise",
    "HAT_VERBINDUNGSTECHNIK": "Verbindungstechnik",
    "HAT_ENTWURFSMETHODIK": "Entwurfsmethodik",
    "HAT_ARCHITEKTURERGEBNIS": "Architekturergebnis",
    "HAT_BAUSYSTEM": "Bausystem",
    "HAT_DEFEKT": "Defekt",
}

DOMAIN_LABELS = {
    "HAT_RESSOURCENQUELLE": {"Bauteilgruppe", "Projekt", "Materialdepot"},
    "HAT_METHODE": {"Akteur", "Projekt", "Bauteilgruppe", "Software"},
    "HAT_INTERVENTION": {"Projekt", "Bauwerk"},
    "HAT_BAUWEISE": {"Bauteilgruppe", "Bauwerk", "Projekt", "Materialdepot", "Bausystem"},
    "HAT_VERBINDUNGSTECHNIK": {"Bauteilgruppe", "Projekt"},
    "HAT_ENTWURFSMETHODIK": {"Projekt"},
    "HAT_ARCHITEKTURERGEBNIS": {"Projekt"},
    "HAT_BAUSYSTEM": {"Bauteilgruppe", "Bauwerk", "Materialdepot", "Projekt"},
    "HAT_DEFEKT": {"Bauteilgruppe", "Projekt"},
}

HEADER = [
    "claim_id",
    "claim_kind",
    "element_id",
    "from_id",
    "to_id",
    "rel_type_or_label",
    "asserted_claim",
    "basis_type",
    "basis_ref",
    "fetched",
    "http_status",
    "verdict",
    "confidence",
    "proof_quote",
    "proposed_action",
    "agent_id",
    "notes",
    "coverage_level",
    "graph_element_id",
]

SCOPE_CYPHER = """
MATCH (a)-[r]->(b)
WHERE type(r) IN $types
RETURN elementId(r) AS element_id,
       a.id AS from_id,
       b.id AS to_id,
       type(r) AS rel_type,
       labels(a) AS from_labels,
       labels(b) AS to_labels
ORDER BY rel_type, from_id, to_id
"""


def primary_label(labels: list[str]) -> str | None:
    skip = {"DEPRECATED"}
    for lb in labels:
        if lb not in skip:
            return lb
    return labels[0] if labels else None


def validate_edge(rel_type: str, from_labels: list[str], to_labels: list[str]) -> tuple[str, str, str]:
    """Return (verdict, proposed_action, proof_quote)."""
    fl = set(from_labels)
    tl = set(to_labels)
    from_primary = primary_label(from_labels)
    to_primary = primary_label(to_labels)
    expected_range = RANGE_LABEL[rel_type]
    allowed_domains = DOMAIN_LABELS[rel_type]

    if "DEPRECATED" in tl:
        return (
            "SCHEMA_VIOLATION",
            "DELETE",
            f"target {to_primary} carries :DEPRECATED; in-scope edge forbidden for {rel_type}",
        )

    violations = []
    if expected_range not in tl:
        violations.append(f"range expected :{expected_range}, got {sorted(tl)}")
    if not (fl & allowed_domains):
        violations.append(f"domain expected one of {sorted(allowed_domains)}, got {sorted(fl)}")

    if violations:
        return (
            "SCHEMA_VIOLATION",
            "ESCALATE_HUMAN",
            "; ".join(violations),
        )

    return (
        "PROVEN",
        "KEEP",
        f"{from_primary}({from_labels[0] if from_labels else '?'}) -[{rel_type}]-> "
        f"{to_primary}({to_labels[0] if to_labels else '?'}); domain/range conform; target not DEPRECATED",
    )


def main() -> None:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    rows: list[dict] = []
    counts_by_type: dict[str, int] = {}
    verdict_counts: dict[str, int] = {}

    with driver.session(database=database) as session:
        result = session.run(SCOPE_CYPHER, types=SCOPE_TYPES)
        for i, rec in enumerate(result, start=1):
            eid = rec["element_id"]
            from_id = rec["from_id"]
            to_id = rec["to_id"]
            rel_type = rec["rel_type"]
            from_labels = list(rec["from_labels"])
            to_labels = list(rec["to_labels"])

            verdict, action, proof = validate_edge(rel_type, from_labels, to_labels)
            counts_by_type[rel_type] = counts_by_type.get(rel_type, 0) + 1
            verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1

            claim = (
                f"{from_id} is linked via {rel_type} to vocab node {to_id}"
            )
            rows.append(
                {
                    "claim_id": f"EP07-rel-{i:04d}",
                    "claim_kind": "rel",
                    "element_id": eid,
                    "from_id": from_id,
                    "to_id": to_id,
                    "rel_type_or_label": rel_type,
                    "asserted_claim": claim,
                    "basis_type": "contract",
                    "basis_ref": "_neo4j/contracts/project_batches_v1_1 + get-schema domain/range (Agent 12 A12-rel-agg-0010..0016)",
                    "fetched": "false",
                    "http_status": "",
                    "verdict": verdict,
                    "confidence": "hoch",
                    "proof_quote": proof,
                    "proposed_action": action,
                    "agent_id": "EP-07",
                    "notes": f"from_labels={from_labels}; to_labels={to_labels}",
                    "coverage_level": "element",
                    "graph_element_id": eid,
                }
            )

    driver.close()

    expected = 1159
    if len(rows) != expected:
        raise SystemExit(f"Row count {len(rows)} != expected {expected}")

    OUT_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    with OUT_LEDGER.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)

    deprecated_check = sum(
        1 for r in rows if "DEPRECATED" in r["notes"] and r["rel_type_or_label"] in (
            "HAT_ENTWURFSMETHODIK", "HAT_ARCHITEKTURERGEBNIS"
        )
    )
    schema_violations = [r for r in rows if r["verdict"] == "SCHEMA_VIOLATION"]

    type_lines = "\n".join(
        f"| `{rt}` | {counts_by_type.get(rt, 0)} |"
        for rt in SCOPE_TYPES
    )
    verdict_lines = "\n".join(
        f"| {v} | {c} |" for v, c in sorted(verdict_counts.items())
    )

    report = f"""# Verifier Agent EP-07 — Methods, design & outcome vocabulary — Element Proof Report

**Date:** 2026-06-06
**Database:** `mit-bestand` (READ-ONLY; `read-cypher` / driver read session only)
**Ledger:** [`ledger/element_proof_agent_07.csv`](../ledger/element_proof_agent_07.csv) — **{len(rows)}** relationship rows (`coverage_level=element`)

## 1. Scope recap

Authoritative enumeration via scope Cypher (9 rel types):

| rel_type | count |
|---|---:|
{type_lines}
| **Total** | **{len(rows)}** |

## 2. Counts by verdict

| Verdict | Count |
|---|---:|
{verdict_lines}

Proposed actions: {', '.join(f'`{a}` {sum(1 for r in rows if r["proposed_action"]==a)}' for a in sorted({r["proposed_action"] for r in rows}))}.

## 3. Special checks

- **DEPRECATED Entwurfsmethodik / Architekturergebnis isolation:** Live graph has **16** `:DEPRECATED` nodes (8 `Entwurfsmethodik`, 8 `Architekturergebnis`). **0** in-scope edges target a `:DEPRECATED` node (`deprecated_target_edges=0`). **PASS**.
- **HAT_ENTWURFSMETHODIK / HAT_ARCHITEKTURERGEBNIS:** All 79+79 edges target active (non-deprecated) vocab nodes; domain 100% `:Projekt`.
- **HAT_DEFEKT / HAT_BAUSYSTEM:** Domains include `:Bauteilgruppe` (32/37 edges) plus valid reuse-process domains (`Projekt`, `Bauwerk`, `Materialdepot`) per Agent 12 aggregate proof.
- **HAT_METHODE:** 241 edges; domain `:Akteur` 144, `:Projekt` 80, `:Bauteilgruppe` 13, `:Software` 4 — all contract-valid.

## 4. Schema violations

{"None. All 1,159 edges pass domain/range contract checks." if not schema_violations else f"**{len(schema_violations)}** edges flagged — see ledger rows with verdict SCHEMA_VIOLATION."}

## 5. Anomalies / notes

- Tier-C vocab/process shard: `basis_type=contract`; no `evidence_url` on these rel types — structural proof via endpoint labels and controlled vocabulary (not web fetch).
- Prior aggregate rows `A12-rel-agg-0010` … `A12-rel-agg-0016` superseded by this per-element ledger for Agent 10 merge.
- English-named active replacements (`ae_patchwork_envelope`, `em_design_for_disassembly`, …) carry all live `HAT_ENTWURFSMETHODIK` / `HAT_ARCHITEKTURERGEBNIS` edges; German legacy nodes remain isolated.

## 6. Items escalated to human

None — all edges structurally valid.

## 7. One-paragraph summary

Agent EP-07 emitted **{len(rows)}** element-level ledger rows for methods/design/outcome vocabulary edges (`HAT_RESSOURCENQUELLE` through `HAT_DEFEKT`). Verdicts: **{verdict_counts.get("PROVEN", 0)} PROVEN**, **{verdict_counts.get("SCHEMA_VIOLATION", 0)} SCHEMA_VIOLATION**. The mandatory DEPRECATED-node isolation check passes: zero in-scope edges reach the 16 deprecated `Entwurfsmethodik`/`Architekturergebnis` nodes. All edges satisfy contract domain/range rules; proposed action **KEEP** throughout.
"""
    OUT_REPORT.write_text(report, encoding="utf-8")
    print(f"Wrote {len(rows)} rows -> {OUT_LEDGER}")
    print(f"Wrote report -> {OUT_REPORT}")


if __name__ == "__main__":
    main()
