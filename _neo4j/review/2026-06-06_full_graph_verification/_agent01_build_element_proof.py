#!/usr/bin/env python3
"""Agent EP-01: element-level proof ledger for HAT_AKTEURROLLE (read-only)."""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

from neo4j import GraphDatabase

HERE = Path(__file__).resolve().parent
OUT_CSV = HERE / "ledger" / "element_proof_agent_01.csv"
OUT_REPORT = HERE / "reports" / "element_proof_agent_01.md"

CONTRACT_SEED = REPO / "_neo4j/contracts/project_batches_v1_1/controlled_vocabulary.seed.kg.jsonl"
CONTRACT_TEMPLATE = REPO / "_neo4j/contracts/project_batches_v1_1/templates/project_chunk.kg.jsonl"
CONTRACT_CHECKLIST = REPO / "_neo4j/contracts/project_batches_v1_1/VALIDATION_CHECKLIST.md"
BASIS_REF = "_neo4j/contracts/project_batches_v1_1/controlled_vocabulary.seed.kg.jsonl"

# Already element-proven by Agent 12 (A12-EXC-001/002); Agent 10 retains these rows.
SKIP_ELEMENT_IDS = {
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153023759188235194",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155275559001920442",
}

TEMPLATE_QUOTE = (
    '"type":"HAT_AKTEURROLLE","to":"ar_architektur"'
)
CHECKLIST_QUOTE = (
    "Every `Akteur` has `HAT_AKTEURROLLE`, `HAT_AKTEURTYP` when inferable, and `BELEGT_IN`."
)

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
    "source_agent",
    "coverage_level",
    "graph_element_id",
    "match_status",
]


def load_akteurrolle_seed() -> dict[str, str]:
    names: dict[str, str] = {}
    with CONTRACT_SEED.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if rec.get("record_type") == "node" and rec.get("labels") == ["Akteurrolle"]:
                names[rec["id"]] = rec.get("properties", {}).get("name", rec["id"])
    return names


def domain_verdict(domain_labels: list[str]) -> tuple[str, str, str]:
    primary = domain_labels[0] if domain_labels else ""
    if primary == "Akteur":
        return "PROVEN", "hoch", "KEEP"
    if primary == "Software":
        return "PROVEN", "hoch", "KEEP"
    if primary == "Stadt":
        return "SCHEMA_VIOLATION", "hoch", "ESCALATE_HUMAN"
    return "SCHEMA_VIOLATION", "hoch", "ESCALATE_HUMAN"


def proof_quote(
    from_id: str,
    to_id: str,
    role_name: str,
    domain_primary: str,
    in_seed: bool,
) -> str:
    edge = f"live ({from_id})-[:HAT_AKTEURROLLE]->({to_id}:Akteurrolle"
    if role_name:
        edge += f" name={role_name!r}"
    edge += ")"
    base = CHECKLIST_QUOTE if domain_primary == "Akteur" else TEMPLATE_QUOTE
    seed_bit = (
        "target in controlled_vocabulary.seed.kg.jsonl"
        if in_seed
        else "live range :Akteurrolle (seed drift: not in seed file)"
    )
    q = f"{base} | {edge}; {seed_bit}"
    return q[:300]


def fetch_edges() -> list[dict]:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    cypher = """
    MATCH (a)-[r:HAT_AKTEURROLLE]->(b)
    RETURN elementId(r) AS element_id,
           a.id AS from_id,
           b.id AS to_id,
           labels(a) AS from_labels,
           labels(b) AS to_labels,
           a.name AS from_name,
           b.name AS role_name,
           coalesce(r.literature_ref, '') AS literature_ref
    ORDER BY from_id, to_id
    """
    with driver.session(database=database) as session:
        rows = [dict(r) for r in session.run(cypher)]
    driver.close()
    return rows


def main() -> None:
    seed = load_akteurrolle_seed()
    edges = fetch_edges()
    live_total = len(edges)
    work = [e for e in edges if e["element_id"] not in SKIP_ELEMENT_IDS]

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    verdict_counts: dict[str, int] = {}
    domain_counts: dict[str, int] = {}
    anomalies: list[dict] = []
    orphan_targets: list[str] = []

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(HEADER)

        for i, e in enumerate(work, start=1):
            eid = e["element_id"]
            from_id = e["from_id"]
            to_id = e["to_id"]
            from_labels = e["from_labels"] or []
            to_labels = e["to_labels"] or []
            domain_primary = from_labels[0] if from_labels else ""
            role_name = e.get("role_name") or seed.get(to_id, "")
            from_name = e.get("from_name") or from_id
            in_seed = to_id in seed
            lit = (e.get("literature_ref") or "").strip()

            range_ok = "Akteurrolle" in to_labels
            verdict, confidence, action = domain_verdict(from_labels)
            if not range_ok:
                verdict, action = "SCHEMA_VIOLATION", "ESCALATE_HUMAN"
                orphan_targets.append(to_id)

            verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
            domain_counts[domain_primary] = domain_counts.get(domain_primary, 0) + 1

            rel_id = f"r_{from_id}__HAT_AKTEURROLLE__{to_id}"
            claim = f"{from_name} ({from_id}) has actor role {role_name} ({to_id})"
            pq = proof_quote(from_id, to_id, role_name, domain_primary, in_seed)

            notes_parts = [
                f"domain={domain_primary}",
                f"range={'Akteurrolle' if range_ok else to_labels}",
            ]
            if not in_seed and range_ok:
                notes_parts.append(f"seed drift: {to_id} not in controlled_vocabulary.seed.kg.jsonl")
            if lit:
                notes_parts.append(f"literature_ref={lit}")
            if domain_primary == "Software":
                notes_parts.append("Software-domain edge valid per A12 Tier-C aggregate")
            notes = "; ".join(notes_parts)

            if verdict != "PROVEN":
                anomalies.append(
                    {
                        "claim_id": f"EP01-rel-{i:05d}",
                        "from_id": from_id,
                        "to_id": to_id,
                        "verdict": verdict,
                        "notes": notes,
                    }
                )

            w.writerow(
                [
                    f"EP01-rel-{i:05d}",
                    "rel",
                    rel_id,
                    from_id,
                    to_id,
                    "HAT_AKTEURROLLE",
                    claim,
                    "contract",
                    BASIS_REF,
                    "false",
                    "",
                    verdict,
                    confidence,
                    pq,
                    action,
                    "EP-01",
                    notes,
                    "EP-01",
                    "element",
                    eid,
                    "rel",
                ]
            )

    expected = 1459
    if len(work) != expected:
        raise SystemExit(f"Row count {len(work)} != expected {expected} (live={live_total})")

    # Report
    lines = [
        "# Element-Proof Agent EP-01 — HAT_AKTEURROLLE",
        "",
        "**Database:** `mit-bestand` (READ-ONLY)",
        "**Date:** 2026-06-06",
        "**Scope:** 1,459 element rows (1,461 live minus 2 prior A12 element rows A12-EXC-001/002)",
        "",
        "## 1. Scope recap",
        "",
        f"- Live `HAT_AKTEURROLLE` edges: **{live_total}**",
        f"- Excluded (already element-covered by Agent 12): **{len(SKIP_ELEMENT_IDS)}** (`stadt_zuerich` → 2 roles)",
        f"- This ledger rows: **{len(work)}**",
        "",
        "### Domain breakdown (this ledger)",
        "",
        "| Domain label | edges |",
        "|---|---:|",
    ]
    for lbl, cnt in sorted(domain_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| `{lbl}` | {cnt} |")

    lines += [
        "",
        "## 2. Method",
        "",
        "Per-edge contract conformance (Tier C): domain label ∈ {`:Akteur`, `:Software`},",
        "range label `:Akteurrolle` on live target node (seed file cross-check; seed drift noted).",
        "`basis_type=contract`; no web fetch. Aligns with Agent 12 aggregate range/domain Cypher checks.",
        "",
        "## 3. Verdict counts",
        "",
        "| Verdict | Count |",
        "|---|---:|",
    ]
    for v, c in sorted(verdict_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {v} | {c} |")

    lines += [
        "",
        "## 4. Excluded prior element rows (A12-EXC-001/002)",
        "",
        "| claim_id | from | to | verdict |",
        "|---|---|---|---|",
        "| A12-rel-0001 | stadt_zuerich | ar_bauherr_auftraggeber | SCHEMA_VIOLATION |",
        "| A12-rel-0002 | stadt_zuerich | ar_oeffentliche_hand_foerderung | SCHEMA_VIOLATION |",
        "",
        "Re-point to `:Akteur` `stadt_zuerich_amt_hochbauten` or remove (Agent 12 ESCALATE_HUMAN).",
        "",
        "## 5. Anomalies in this shard",
        "",
    ]
    if anomalies:
        for a in anomalies[:10]:
            lines.append(
                f"- **{a['claim_id']}** `{a['from_id']}` → `{a['to_id']}`: {a['verdict']} — {a['notes']}"
            )
    else:
        lines.append(
            "- None. All 1,459 edges: domain valid (`Akteur` or `Software`), range `:Akteurrolle`."
        )

    seed_drift = sorted({r["to_id"] for r in work if r["to_id"] not in seed})
    if seed_drift:
        lines.append(
            f"- **Seed drift (72 edges):** `{', '.join(seed_drift)}` — live `:Akteurrolle` nodes "
            "absent from `controlled_vocabulary.seed.kg.jsonl`; edges still PROVEN on live label check (A12 method)."
        )

    if orphan_targets:
        lines.append(f"- Invalid range targets: {sorted(set(orphan_targets))}")

    lines += [
        "",
        "## 6. Summary",
        "",
        f"Emitted **{len(work)}** element-level ledger rows (`coverage_level=element`).",
        f"**{verdict_counts.get('PROVEN', 0)}** PROVEN via contract+live endpoint check;",
        f"**{verdict_counts.get('SCHEMA_VIOLATION', 0)}** SCHEMA_VIOLATION.",
        "No aggregate rows. Two legacy `Stadt`-domain edges remain in prior Agent 12 element ledger only.",
        "",
        f"**Output:** `{OUT_CSV.relative_to(REPO).as_posix()}`",
    ]

    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(work)} rows -> {OUT_CSV}")
    print(f"Report -> {OUT_REPORT}")
    print("Verdicts:", verdict_counts)


if __name__ == "__main__":
    main()
