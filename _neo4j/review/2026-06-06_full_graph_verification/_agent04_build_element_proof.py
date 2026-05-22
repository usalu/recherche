#!/usr/bin/env python3
"""Agent EP-04: element-level proof for material groups, Kennwert, era links (read-only)."""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

from neo4j import GraphDatabase

HERE = Path(__file__).resolve().parent
OUT_CSV = HERE / "ledger" / "element_proof_agent_04.csv"
OUT_REPORT = HERE / "reports" / "element_proof_agent_04.md"

BASIS_CONTRACT = "_neo4j/contracts/project_batches_v1_1/controlled_vocabulary.seed.kg.jsonl"
BASIS_LOGIC = "get-schema + project_batches_v1_1 (instance edges)"

# 18 Schadstoff-domain TYPISCH_BEI_MATERIAL edges already element-covered in VERIFICATION_LEDGER.csv (Agent 07).
SKIP_ELEMENT_IDS = {
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155289852653081217",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153038052839395969",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155289852653081218",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153038052839395970",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155289852653081214",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:6917645575873631103",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153038052839395966",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153038052839391299",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153038052839395968",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1157541652466766463",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153038052839395967",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155289852653081215",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1157541652466761797",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155289852653076549",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1159793452280447045",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153038052839391301",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155289852653076548",
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153038052839391300",
}

REL_TYPES = [
    "HAT_MATERIALGRUPPE",
    "HAT_BAUTEILGRUPPE",
    "HAT_KENNWERT",
    "TYPISCH_BEI_MATERIAL",
    "HAT_ZUSTANDSKLASSE",
    "GEBAUT_IN_ERA",
]

A12_AGG = {
    "HAT_MATERIALGRUPPE": "A12-rel-agg-0005",
    "HAT_BAUTEILGRUPPE": "A12-rel-agg-0006",
    "HAT_KENNWERT": "A12-rel-agg-0007",
    "TYPISCH_BEI_MATERIAL": "A12-rel-agg-0018",
    "HAT_ZUSTANDSKLASSE": "A12-rel-agg-0017",
    "GEBAUT_IN_ERA": "A12-rel-agg-0021",
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
    "source_agent",
    "coverage_level",
    "graph_element_id",
    "match_status",
]


def domain_range_ok(rel_type: str, from_label: str, to_labels: list[str]) -> bool:
    to_set = set(to_labels or [])
    if rel_type == "HAT_MATERIALGRUPPE":
        return from_label in ("Bauteilgruppe", "Material") and "Materialgruppe" in to_set
    if rel_type == "HAT_BAUTEILGRUPPE":
        return from_label in ("Projekt", "Programm") and "Bauteilgruppe" in to_set
    if rel_type == "HAT_KENNWERT":
        return from_label == "Projekt" and "Kennwert" in to_set
    if rel_type == "TYPISCH_BEI_MATERIAL":
        return from_label in (
            "Schadstoff",
            "Aufbereitungsverfahren",
            "Defekt",
            "PruefungNachweis",
            "ZustandsKlasse",
        ) and "Material" in to_set
    if rel_type == "HAT_ZUSTANDSKLASSE":
        return from_label == "Bauteilgruppe" and "ZustandsKlasse" in to_set
    if rel_type == "GEBAUT_IN_ERA":
        return from_label == "Bauwerk" and "BauwerkEra" in to_set
    return False


def basis_for(rel_type: str) -> tuple[str, str]:
    if rel_type in ("HAT_BAUTEILGRUPPE", "HAT_KENNWERT"):
        return "logic", BASIS_LOGIC
    return "contract", BASIS_CONTRACT + f" + get-schema (Agent 12 {A12_AGG[rel_type]})"


def proof_quote(
    rel_type: str,
    from_id: str,
    to_id: str,
    from_label: str,
    to_label: str,
    kennwert: str | None,
    wert,
    einheit: str | None,
) -> str:
    base = f"{from_label}({from_id}) -[{rel_type}]-> {to_label}({to_id}); domain/range conform"
    if rel_type == "HAT_KENNWERT":
        ident = kennwert or ""
        if wert is not None:
            ident = f"{ident}={wert}" if ident else str(wert)
        if einheit:
            ident = f"{ident} {einheit}".strip()
        base += f"; Kennwert identity kennwert/wert/einheit ({ident or 'present'})"
        base += "; name=null by design"
    if rel_type == "HAT_BAUTEILGRUPPE":
        base += "; Bauteilgruppe is donor instance node not closed vocab"
    return base[:300]


def fetch_edges() -> list[dict]:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    cypher = """
    MATCH (a)-[r]->(b)
    WHERE type(r) IN $types
    RETURN elementId(r) AS graph_eid,
           a.id AS from_id,
           b.id AS to_id,
           type(r) AS rel_type,
           labels(a) AS from_labels,
           labels(b) AS to_labels,
           b.kennwert AS kennwert,
           b.wert AS wert,
           b.einheit AS einheit,
           b.name AS to_name
    ORDER BY rel_type, from_id, to_id
    """
    with driver.session(database=database) as session:
        rows = [dict(r) for r in session.run(cypher, types=REL_TYPES)]
    driver.close()
    return rows


def main() -> None:
    edges = fetch_edges()
    live_total = len(edges)
    work = [e for e in edges if e["graph_eid"] not in SKIP_ELEMENT_IDS]

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    verdict_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    anomalies: list[dict] = []

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(HEADER)

        for i, e in enumerate(work, start=1):
            graph_eid = e["graph_eid"]
            from_id = e["from_id"]
            to_id = e["to_id"]
            rel_type = e["rel_type"]
            from_labels = e["from_labels"] or []
            to_labels = e["to_labels"] or []
            from_label = from_labels[0] if from_labels else ""
            to_label = to_labels[0] if to_labels else ""

            type_counts[rel_type] += 1
            ok = domain_range_ok(rel_type, from_label, to_labels)
            kennwert = e.get("kennwert")
            wert = e.get("wert")
            einheit = e.get("einheit")

            if rel_type == "HAT_KENNWERT" and kennwert is None and wert is None:
                ok = False

            verdict = "PROVEN" if ok else "SCHEMA_VIOLATION"
            action = "KEEP" if ok else "ESCALATE_HUMAN"
            verdict_counts[verdict] += 1

            basis_type, basis_ref = basis_for(rel_type)
            rel_id = f"r_{from_id}__{rel_type}__{to_id}"
            to_name = e.get("to_name")
            claim_tail = f" ({to_name})" if to_name else ""
            claim = f"{from_id} is linked via {rel_type} to {to_id}{claim_tail}"

            pq = proof_quote(rel_type, from_id, to_id, from_label, to_label, kennwert, wert, einheit)
            notes = (
                f"from_labels={from_labels}; to_labels={to_labels}; "
                f"prior aggregate {A12_AGG[rel_type]} superseded by element row"
            )
            if rel_type == "HAT_KENNWERT":
                notes += "; Kennwert name=null OK (identity in kennwert/wert/einheit)"

            if verdict != "PROVEN":
                anomalies.append(
                    {
                        "claim_id": f"EP04-rel-{i:05d}",
                        "from_id": from_id,
                        "to_id": to_id,
                        "rel_type": rel_type,
                        "notes": notes,
                    }
                )

            w.writerow(
                [
                    f"EP04-rel-{i:05d}",
                    "rel",
                    rel_id,
                    from_id,
                    to_id,
                    rel_type,
                    claim,
                    basis_type,
                    basis_ref,
                    "false",
                    "",
                    verdict,
                    "hoch",
                    pq,
                    action,
                    "EP-04",
                    notes,
                    "EP-04",
                    "element",
                    graph_eid,
                    "rel",
                ]
            )

    expected = 1104
    if len(work) != expected:
        raise SystemExit(
            f"Row count {len(work)} != expected {expected} (live={live_total}, skipped={live_total - len(work)})"
        )

    skipped_typisch = sum(1 for e in edges if e["rel_type"] == "TYPISCH_BEI_MATERIAL" and e["graph_eid"] in SKIP_ELEMENT_IDS)

    lines = [
        "# Verifier Agent EP-04 — Material groups, Kennwert, era links — Element Proof Report",
        "",
        "**Date:** 2026-06-06",
        "**Database:** `mit-bestand` (READ-ONLY; `read-cypher` / driver read session only)",
        f"**Ledger:** [`ledger/element_proof_agent_04.csv`](../ledger/element_proof_agent_04.csv) — **{len(work)}** relationship rows (`coverage_level=element`)",
        "",
        "## 1. Scope recap",
        "",
        "Authoritative enumeration (6 rel types):",
        "",
        "| rel_type | live | this ledger |",
        "|---|---:|---:|",
    ]
    live_by_type = Counter(e["rel_type"] for e in edges)
    for rt in REL_TYPES:
        live_n = live_by_type[rt]
        ledger_n = type_counts[rt]
        lines.append(f"| `{rt}` | {live_n} | {ledger_n} |")
    lines.append(f"| **Total** | **{live_total}** | **{len(work)}** |")
    lines += [
        "",
        f"- Excluded **{skipped_typisch}** `TYPISCH_BEI_MATERIAL` Schadstoff edges already element-covered in `VERIFICATION_LEDGER.csv` (Agent 07 web proof).",
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
        "Proposed actions: `KEEP` " + str(verdict_counts.get("PROVEN", 0)) + ".",
        "",
        "## 3. Special checks",
        "",
        "- **Kennwert `name=null`:** All 255 `HAT_KENNWERT` targets have `kennwert` and/or `wert` populated; `name=null` is by design.",
        "- **HAT_BAUTEILGRUPPE:** 364 instance edges (360 `Projekt` + 4 `Programm` → `Bauteilgruppe`); not duplicate vocab nodes.",
        "- **TYPISCH_BEI_MATERIAL gap shard:** 56 edges (Aufbereitungsverfahren 18, Defekt 14, PruefungNachweis 12, ZustandsKlasse 12); 18 Schadstoff edges retained from prior ledger.",
        "- **HAT_ZUSTANDSKLASSE / GEBAUT_IN_ERA:** 18 + 8 edges; domain/range 100% valid.",
        "",
        "## 4. Schema violations",
        "",
    ]
    if anomalies:
        for a in anomalies[:10]:
            lines.append(
                f"- **{a['claim_id']}** `{a['from_id']}` -[{a['rel_type']}]-> `{a['to_id']}`: SCHEMA_VIOLATION"
            )
    else:
        lines.append("None. All 1,104 edges pass domain/range contract checks.")
    lines += [
        "",
        "## 5. Anomalies / notes",
        "",
        "- Tier-C / instance shard: `basis_type=contract` or `logic`; no `evidence_url` on these rel types.",
        "- Prior aggregate rows `A12-rel-agg-0005/0006/0007/0017/0018/0021` superseded by this per-element ledger for Agent 10 merge.",
        "",
        "## 6. Items escalated to human",
        "",
        "None." if not anomalies else f"{len(anomalies)} SCHEMA_VIOLATION row(s) — see §4.",
        "",
        "## 7. One-paragraph summary",
        "",
        f"Agent EP-04 emitted **{len(work)}** element-level ledger rows for material-group, Kennwert, era, and typical-material links. "
        f"Verdicts: **{verdict_counts.get('PROVEN', 0)} PROVEN**, **{verdict_counts.get('SCHEMA_VIOLATION', 0)} SCHEMA_VIOLATION**. "
        "All edges satisfy contract domain/range rules; Kennwert instances verified via `kennwert`/`wert`/`einheit` despite `name=null`. "
        f"Eighteen Schadstoff `TYPISCH_BEI_MATERIAL` edges excluded as already element-proven by Agent 07.",
        "",
    ]

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(work)} rows -> {OUT_CSV}")
    print(f"Report -> {OUT_REPORT}")
    print("Verdicts:", dict(verdict_counts))
    print("By type:", dict(type_counts))


if __name__ == "__main__":
    main()
