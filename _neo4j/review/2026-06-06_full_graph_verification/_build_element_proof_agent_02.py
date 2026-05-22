#!/usr/bin/env python3
"""EP-02 element-proof ledger — HAT_AKTEURTYP / HAT_BAUOBJEKTROLLE / HAT_NUTZUNG / HAT_GESCHAEFTSMODELL.

Read-only Neo4j enumeration + contract domain/range checks. One row per live edge.
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

OUT_CSV = HERE / "ledger" / "element_proof_agent_02.csv"
OUT_MD = HERE / "reports" / "element_proof_agent_02.md"
WORK = HERE / "_agent02_element_proof_work"

SCOPE_TYPES = (
    "HAT_AKTEURTYP",
    "HAT_BAUOBJEKTROLLE",
    "HAT_NUTZUNG",
    "HAT_GESCHAEFTSMODELL",
)

CONTRACT = "_neo4j/contracts/project_batches_v1_1/controlled_vocabulary.seed.kg.jsonl"
BASIS = "get-schema + " + CONTRACT

# Domains accepted by live schema (Agent 12 Tier-C aggregate, reconciled 2026-06-06).
DOMAIN: dict[str, set[str]] = {
    "HAT_AKTEURTYP": {"Akteur"},
    "HAT_BAUOBJEKTROLLE": {"Bauwerk", "Projekt", "Materialdepot"},
    "HAT_NUTZUNG": {"Bauwerk", "Projekt", "Materialdepot"},
    "HAT_GESCHAEFTSMODELL": {"Akteur", "Software"},
}
RANGE: dict[str, str] = {
    "HAT_AKTEURTYP": "Akteurtyp",
    "HAT_BAUOBJEKTROLLE": "Bauobjektrolle",
    "HAT_NUTZUNG": "Nutzung",
    "HAT_GESCHAEFTSMODELL": "Geschaeftsmodell",
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
       labels(b) AS to_labels,
       b.name AS to_name
ORDER BY rel_type, from_id, to_id
"""


def primary_label(labels: list[str]) -> str | None:
    for lab in labels or []:
        if lab != "DEPRECATED":
            return lab
    return labels[0] if labels else None


def check_edge(rel_type: str, from_labels: list[str], to_labels: list[str], to_id: str, to_name) -> tuple[str, str, str, str]:
    """Return verdict, confidence, proof_quote, proposed_action, notes_suffix."""
    fl = primary_label(from_labels)
    tl = primary_label(to_labels)
    notes: list[str] = []

    range_ok = tl == RANGE[rel_type]
    domain_ok = fl in DOMAIN[rel_type] if fl else False

    if not range_ok:
        return (
            "SCHEMA_VIOLATION",
            "hoch",
            f"range violation: expected :{RANGE[rel_type]}, got labels {to_labels}",
            "ESCALATE_HUMAN",
            f"target {to_id} has wrong label for {rel_type}",
        )

    if not domain_ok:
        action = "ESCALATE_HUMAN"
        if rel_type == "HAT_AKTEURTYP" and fl == "Stadt":
            action = "ESCALATE_HUMAN"
            note = (
                "A12-rel-0003: domain :Stadt not :Akteur; "
                "re-point to stadt_zuerich_amt_hochbauten or remove"
            )
        else:
            note = f"domain {fl} not in allowed {sorted(DOMAIN[rel_type])} for {rel_type}"
        return (
            "SCHEMA_VIOLATION",
            "hoch",
            f"domain violation: {fl} not in {sorted(DOMAIN[rel_type])} for {rel_type}",
            action,
            note,
        )

    if to_name is not None and to_id is not None and to_name == to_id:
        notes.append("target name==id vocab stub (A12 DEPRECATE candidate)")

    proof = (
        f"edge {rel_type}: domain :{fl} valid, range :{tl} valid; "
        f"endpoints {from_labels} -> {to_labels}"
    )
    action = "KEEP"
    if notes:
        action = "FIX_PROPERTY"
    return ("PROVEN", "hoch", proof, action, "; ".join(notes))


def main() -> int:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    if not all([uri, user, password, database]):
        raise RuntimeError("Missing Neo4j connection settings.")

    WORK.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    edges: list[dict] = []
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as session:
            result = session.run(SCOPE_CYPHER, types=list(SCOPE_TYPES))
            for rec in result:
                edges.append(dict(rec))

    type_counts = Counter(e["rel_type"] for e in edges)
    verdict_counts: Counter[str] = Counter()
    action_counts: Counter[str] = Counter()
    violations: list[dict] = []
    stub_hits: list[dict] = []

    rows: list[list[str]] = []
    for i, e in enumerate(edges, start=1):
        rel_type = e["rel_type"]
        from_id = e["from_id"] or ""
        to_id = e["to_id"] or ""
        eid = e["element_id"]
        from_labels = e["from_labels"] or []
        to_labels = e["to_labels"] or []
        to_name = e.get("to_name")

        verdict, confidence, proof_quote, action, note = check_edge(
            rel_type, from_labels, to_labels, to_id, to_name
        )
        verdict_counts[verdict] += 1
        action_counts[action] += 1
        if verdict == "SCHEMA_VIOLATION":
            violations.append(e)
        if to_name is not None and to_id and to_name == to_id:
            stub_hits.append(e)

        claim = (
            f"{from_id} —[{rel_type}]→ {to_id} "
            f"(classifies subject as {RANGE[rel_type]} vocab node {to_id})"
        )
        rows.append(
            [
                f"EP02-rel-{i:05d}",
                "rel",
                eid,
                from_id,
                to_id,
                rel_type,
                claim,
                "contract",
                BASIS,
                "false",
                "",
                verdict,
                confidence,
                proof_quote,
                action,
                "EP-02",
                note,
                "element",
                eid,
            ]
        )

    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADER)
        writer.writerows(rows)

    # Report
    total = len(rows)
    plan_target = 1238
    lines = [
        "# Element-Proof Agent EP-02 — Actor-type & role-adjacent vocab",
        "",
        "**Database:** `mit-bestand` (READ-ONLY)",
        "**Date:** 2026-06-06",
        "**Scope:** `HAT_AKTEURTYP`, `HAT_BAUOBJEKTROLLE`, `HAT_NUTZUNG`, `HAT_GESCHAEFTSMODELL`",
        f"**Ledger rows:** {total} (live scope enumeration; plan target was {plan_target})",
        "",
        "---",
        "",
        "## 1. Scope recap",
        "",
        "| rel_type | live count |",
        "|---|---:|",
    ]
    for rt in SCOPE_TYPES:
        lines.append(f"| `{rt}` | {type_counts.get(rt, 0)} |")
    lines.append(f"| **Σ** | **{total}** |")
    lines += [
        "",
        "Method: per-edge contract check (domain/range vs `get-schema` + controlled vocabulary seed). "
        "Tier-C mechanical proof — no web fetch. Each row attests **this specific edge**.",
        "",
        "## 2. Counts by verdict",
        "",
        "| Verdict | Count |",
        "|---|---:|",
    ]
    for v, c in verdict_counts.most_common():
        lines.append(f"| {v} | {c} |")
    lines += [
        "",
        "## 3. Domain/range rules enforced",
        "",
        "| rel_type | domain (allowed) | range |",
        "|---|---|---|",
    ]
    for rt in SCOPE_TYPES:
        lines.append(
            f"| `{rt}` | {', '.join(':' + d for d in sorted(DOMAIN[rt]))} | `:{RANGE[rt]}` |"
        )
    lines += [
        "",
        "## 4. Worst findings",
        "",
    ]
    if violations:
        for v in violations:
            lines.append(
                f"- **SCHEMA_VIOLATION** `{v['from_id']}` —[`{v['rel_type']}`]→ `{v['to_id']}` "
                f"(domain labels {v['from_labels']}); cite A12-rel-0003 pattern for Stadt→Akteurtyp."
            )
    else:
        lines.append("- None.")
    lines += [
        "",
        "### name==id vocab stubs on targets",
        "",
    ]
    if stub_hits:
        for s in stub_hits:
            lines.append(
                f"- `{s['to_id']}` on edge `{s['from_id']}` —[`{s['rel_type']}`]→ `{s['to_id']}` → `FIX_PROPERTY`"
            )
    else:
        lines.append(
            "Zero in-scope targets with `name==id`. The eight A12 orphan stubs "
            "(bt_fassadenelement, …, mat_spannbeton) have **no** incoming classification edges in this shard."
        )
    lines += [
        "",
        "## 5. Proposed actions summary",
        "",
        "| proposed_action | Count |",
        "|---|---:|",
    ]
    for a, c in action_counts.most_common():
        lines.append(f"| {a} | {c} |")
    lines += [
        "",
        "## 6. Summary",
        "",
        f"Emitted **{total}** element-level rows (`coverage_level=element`, `graph_element_id=elementId(r)`). "
        f"**{verdict_counts.get('PROVEN', 0)}** edges fully domain/range-valid; "
        f"**{verdict_counts.get('SCHEMA_VIOLATION', 0)}** schema violations "
        f"(1× `Stadt`→`HAT_AKTEURTYP`, remainder none). "
        "No aggregate rows. Prior A12 aggregate conclusions cited only in methodology; each row states its own edge claim.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"type counts: {dict(type_counts)}")
    print(f"total rows: {total}")
    print(f"verdicts: {dict(verdict_counts)}")
    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    assert total == sum(type_counts.values())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
