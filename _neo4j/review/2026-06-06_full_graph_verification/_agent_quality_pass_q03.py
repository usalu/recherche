#!/usr/bin/env python3
"""Quality Pass Q03 — Compliance graph: dangling Nachweisforderung residuals (EP-08 + R02)."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]
_SCRIPTS = _REPO / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j import GraphDatabase  # noqa: E402
from neo4j_env import resolve_connection  # noqa: E402

ROOT = Path(__file__).resolve().parent
LEDGER_EP08 = ROOT / "ledger" / "element_proof_agent_08.csv"
LEDGER_R02 = ROOT / "ledger" / "remediation_r02.csv"
LEDGER_OUT = ROOT / "ledger" / "quality_pass_q03.csv"
REPORT_OUT = ROOT / "reports" / "quality_pass_q03.md"
PATCH_OUT = ROOT / "patches" / "quality_pass_q03.patch.jsonl"
RUN_DATE = "2026-06-06"
AGENT = "Q03"

# 11 CONTRADICTION dangling NF from EP-08 (post-R02 residuals)
SCOPE_NF_IDS = [
    "nf_oekobilanz_epd",
    "nf_materialpass_ressourcenpass",
    "nf_barrierefreiheit_nachweis",
    "nf_elektrosicherheitsnachweis",
    "nf_hygiene_und_reinigungsnachweis",
    "nf_befestigungsnachweis",
    "nf_schadstoffkataster_erkundung",
    "nf_dauerhaftigkeit_restlebensdauer",
    "nf_genehmigungs_oder_zustimmungsbedarf",
    "nf_rc_gesteinskoernung_eignung",
    "nf_mineralische_ersatzbaustoff_guete",
]

NEW_PN_NODES: list[dict] = [
    {
        "id": "pn_epd_oder_lca_nachweis",
        "name": "EPD- oder LCA-Nachweis",
        "nf_id": "nf_oekobilanz_epd",
        "evidence_basis": (
            "EN 15804/15978 environmental product declaration or building LCA "
            "(EU Taxonomy, national schemes)"
        ),
        "primary_source_url": (
            "https://www.gebaeudeforum.de/wissen/nachhaltiges-bauen-und-sanieren/"
            "lebenszyklusbetrachtung/oekobilanzierung-lca/"
        ),
    },
    {
        "id": "pn_materialpass_oder_dpp",
        "name": "Materialpass oder DPP",
        "nf_id": "nf_materialpass_ressourcenpass",
        "evidence_basis": (
            "Digital product passport / building resource passport "
            "(ESPR DPP, Madaster, DGNB Level(s))"
        ),
        "primary_source_url": (
            "https://green-forum.ec.europa.eu/"
            "implementing-ecodesign-sustainable-products-regulation_en"
        ),
    },
    {
        "id": "pn_barrierefreiheitsaudit",
        "name": "Barrierefreiheitsaudit",
        "nf_id": "nf_barrierefreiheit_nachweis",
        "evidence_basis": "Accessibility audit per DIN 18040 / DIN 18065",
        "primary_source_url": (
            "https://www.baunormenlexikon.de/norm/din-18040-1/"
            "c099c3ee-ecd0-48ed-9d9d-ec0f84970d53"
        ),
    },
    {
        "id": "pn_elektrosicherheitspruefung",
        "name": "Elektrosicherheitsprüfung",
        "nf_id": "nf_elektrosicherheitsnachweis",
        "evidence_basis": "Electrical safety initial/repeat inspection (DGUV V3 / VDE)",
        "primary_source_url": (
            "https://www.elektrofachkraft.de/pruefung/"
            "elektrotechnische-erstpruefung-wiederholungspruefung"
        ),
    },
    {
        "id": "pn_trinkwasser_hygiene_nachweis",
        "name": "Trinkwasser-Hygiene-Nachweis",
        "nf_id": "nf_hygiene_und_reinigungsnachweis",
        "evidence_basis": "Drinking-water hygiene inspection (VDI 6023 / VDI 6022)",
        "primary_source_url": (
            "https://www.vdi.de/mitgliedschaft/vdi-richtlinien/"
            "unsere-richtlinien-highlights/vdi-6023"
        ),
    },
]

MEDIUM_CONFIDENCE_FULFILLMENTS: list[tuple[str, str, str]] = [
    (
        "pn_ankerpruefung",
        "nf_befestigungsnachweis",
        "anchor pull-out test supports fastening proof (EN 1992-4 / facade anchorage)",
    ),
    (
        "pr_dokumentenpruefung_bestand",
        "nf_schadstoffkataster_erkundung",
        "pre-demolition document review / building pollutant register (VDI 6210 / ATV DIN 18459)",
    ),
    (
        "pr_zustandsbewertung",
        "nf_dauerhaftigkeit_restlebensdauer",
        "condition assessment informs remaining service life (DIN SPEC 91525 PUC)",
    ),
    (
        "pn_approval_process",
        "nf_genehmigungs_oder_zustimmungsbedarf",
        "approval / ZIE-ABZ pathway documentation (DIBt Zulassung)",
    ),
    (
        "pn_petrografie",
        "nf_rc_gesteinskoernung_eignung",
        "petrographic analysis for recycled aggregate suitability (DAfStb RC concrete)",
    ),
    (
        "pr_eignungspruefung_baulehm",
        "nf_rc_gesteinskoernung_eignung",
        "suitability testing for mineral secondary aggregates / RC materials",
    ),
    (
        "pr_eignungspruefung_baulehm",
        "nf_mineralische_ersatzbaustoff_guete",
        "EBV Ersatzbaustoff suitability / quality assessment",
    ),
]

MEDIUM_NF_IDS = sorted({nf for _, nf, _ in MEDIUM_CONFIDENCE_FULFILLMENTS})


def load_ep08_contradictions() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with LEDGER_EP08.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("verdict") == "CONTRADICTION" and row.get("rel_type_or_label") == "Nachweisforderung":
                out[row["element_id"]] = row
    return out


def load_r02_rows() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with LEDGER_R02.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["element_id"]] = row
    return out


def graph_context(driver) -> dict[str, dict]:
    q = """
    MATCH (nf:Nachweisforderung)
    WHERE nf.id IN $ids
    OPTIONAL MATCH (nf)<-[d:ERFORDERT_NACHWEIS]-()
    OPTIONAL MATCH (pn:PruefungNachweis)-[:ERFUELLT_NACHWEIS]->(nf)
    RETURN nf.id AS id, nf.name AS name,
           count(DISTINCT d) AS demands,
           count(DISTINCT pn) AS fulfillments,
           collect(DISTINCT pn.id) AS pn_ids
  """
    with driver.session(database="mit-bestand") as session:
        return {r["id"]: dict(r) for r in session.run(q, ids=SCOPE_NF_IDS)}


def existing_pn_ids(driver, pn_ids: list[str]) -> set[str]:
    q = "MATCH (pn:PruefungNachweis) WHERE pn.id IN $ids RETURN pn.id AS id"
    with driver.session(database="mit-bestand") as session:
        return {r["id"] for r in session.run(q, ids=pn_ids)}


def existing_fulfillment_edges(driver, pairs: list[tuple[str, str]]) -> set[tuple[str, str]]:
    if not pairs:
        return set()
    q = """
    UNWIND $pairs AS p
    MATCH (a:PruefungNachweis {id:p[0]})-[:ERFUELLT_NACHWEIS]->(b:Nachweisforderung {id:p[1]})
    RETURN a.id AS pn, b.id AS nf
  """
    with driver.session(database="mit-bestand") as session:
        return {(r["pn"], r["nf"]) for r in session.run(q, pairs=pairs)}


def build_patch_ops(existing_pns: set[str], existing_edges: set[tuple[str, str]]) -> list[dict]:
    ops: list[dict] = []
    for spec in NEW_PN_NODES:
        pn_id = spec["id"]
        if pn_id not in existing_pns:
            ops.append({
                "op": "add_node",
                "id": pn_id,
                "labels": ["PruefungNachweis"],
                "properties": {
                    "id": pn_id,
                    "name": spec["name"],
                    "primary_source_url": spec["primary_source_url"],
                    "evidence_basis": spec["evidence_basis"],
                    "review_run": f"quality_pass_q03_{RUN_DATE}",
                    "source_scope": "regulation_graph_vocab_extension",
                },
                "reason": f"Q03: new PruefungNachweis to satisfy {spec['nf_id']} (R02 DEFERRED_NEW_PN)",
            })
        nf_id = spec["nf_id"]
        if (pn_id, nf_id) not in existing_edges:
            ops.append({
                "op": "add_rel",
                "from": pn_id,
                "type": "ERFUELLT_NACHWEIS",
                "to": nf_id,
                "properties": {
                    "evidence_basis": spec["evidence_basis"],
                    "evidence_confidence": "high",
                    "review_run": f"quality_pass_q03_{RUN_DATE}",
                    "semantic_basis": "catalog_extension",
                },
                "reason": f"Q03 high-confidence: {pn_id} satisfies {nf_id}",
            })

    for pn_id, nf_id, basis in MEDIUM_CONFIDENCE_FULFILLMENTS:
        if (pn_id, nf_id) in existing_edges:
            continue
        ops.append({
            "op": "add_rel",
            "from": pn_id,
            "type": "ERFUELLT_NACHWEIS",
            "to": nf_id,
            "properties": {
                "evidence_basis": basis,
                "evidence_confidence": "medium",
                "review_run": f"quality_pass_q03_{RUN_DATE}",
                "semantic_basis": "method_mapped_partial",
            },
            "reason": f"Q03 medium-confidence (documented, not upgraded): {pn_id} → {nf_id}. {basis}",
        })
    return ops


def run_patch(dry_run: bool) -> str:
    cmd = [
        sys.executable,
        str(_SCRIPTS / "apply_neo4j_review_patch.py"),
        "--patch", str(PATCH_OUT),
        "--database", "mit-bestand",
    ]
    if not dry_run:
        cmd.extend([
            "--confirm",
            f"APPLY quality_pass_q03.patch.jsonl TO mit-bestand",
        ])
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(_REPO))
    output = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        raise SystemExit(f"patch {'dry-run' if dry_run else 'apply'} failed:\n{output[-3000:]}")
    return output[-2500:]


def main() -> None:
    ep08 = load_ep08_contradictions()
    r02 = load_r02_rows()
    missing_ep08 = [nf for nf in SCOPE_NF_IDS if nf not in ep08]
    if missing_ep08:
        raise SystemExit(f"EP-08 CONTRADICTION rows missing for: {missing_ep08}")
    if len(ep08) != 11:
        raise SystemExit(f"expected 11 EP-08 CONTRADICTION NF rows, got {len(ep08)}")

    uri, user, password, _database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    ctx = graph_context(driver)
    pn_ids = [s["id"] for s in NEW_PN_NODES]
    existing_pns = existing_pn_ids(driver, pn_ids)
    all_pairs = [(s["id"], s["nf_id"]) for s in NEW_PN_NODES] + MEDIUM_CONFIDENCE_FULFILLMENTS
    existing_edges = existing_fulfillment_edges(driver, all_pairs)
    patch_ops = build_patch_ops(existing_pns, existing_edges)
    driver.close()

    PATCH_OUT.parent.mkdir(parents=True, exist_ok=True)
    with PATCH_OUT.open("w", encoding="utf-8") as f:
        for op in patch_ops:
            f.write(json.dumps(op, ensure_ascii=False) + "\n")

    dry_output = run_patch(dry_run=True)
    apply_output = run_patch(dry_run=False)

    # Post-apply verification
    uri, user, password, _database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    ctx_after = graph_context(driver)
    driver.close()

    ledger_cols = [
        "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
        "asserted_claim", "basis_type", "basis_ref", "verdict_before", "verdict_after",
        "confidence", "demands", "fulfillments_before", "fulfillments_after",
        "q03_action", "patch_op", "agent_id", "notes", "ep08_claim_id", "r02_claim_id",
    ]
    ledger_rows: list[dict] = []
    action_counts: Counter = Counter()
    verdict_counts: Counter = Counter()

    for i, nf_id in enumerate(SCOPE_NF_IDS, 1):
        ep = ep08[nf_id]
        r2 = r02.get(nf_id, {})
        before = ctx.get(nf_id, {})
        after = ctx_after.get(nf_id, {})
        fb = int(before.get("fulfillments", 0))
        fa = int(after.get("fulfillments", 0))
        demands = int(after.get("demands", before.get("demands", 0)))

        new_pn = next((s for s in NEW_PN_NODES if s["nf_id"] == nf_id), None)
        medium_edges = [(pn, basis) for pn, target, basis in MEDIUM_CONFIDENCE_FULFILLMENTS if target == nf_id]

        if new_pn:
            q03_action = "ADD_PRUEFUNGNACHWEIS_AND_ERFUELLT"
            confidence = "belegt"
            verdict_after = "PROVEN" if fa >= 1 else "CONTRADICTION"
            patch_op = f"add_node:{new_pn['id']}; add_rel:{new_pn['id']}→{nf_id}"
            notes = (
                f"Created {new_pn['id']} ({new_pn['name']}); "
                f"high-confidence ERFUELLT_NACHWEIS. R02: {r2.get('notes', '')[:120]}"
            )
        elif nf_id in MEDIUM_NF_IDS:
            q03_action = "ADD_MEDIUM_ERFUELLT_DOCUMENTED"
            confidence = "teilweise_belegt"
            verdict_after = "PARTIAL_COVERAGE" if fa >= 1 else "CONTRADICTION"
            pns = "; ".join(pn for pn, _ in medium_edges)
            patch_op = "; ".join(f"add_rel:{pn}→{nf_id}" for pn, _ in medium_edges)
            notes = (
                f"Medium-confidence mapping documented (not upgraded to belegt): {pns}. "
                + (medium_edges[0][1] if medium_edges else "")
            )
        else:
            q03_action = "NOOP"
            confidence = "unbelegt"
            verdict_after = ep.get("verdict", "CONTRADICTION")
            patch_op = ""
            notes = "out of Q03 scope"

        action_counts[q03_action] += 1
        verdict_counts[verdict_after] += 1

        ledger_rows.append({
            "claim_id": f"Q03-nf-{i:04d}",
            "claim_kind": "node",
            "element_id": nf_id,
            "from_id": new_pn["id"] if new_pn else (medium_edges[0][0] if medium_edges else ""),
            "to_id": nf_id if (new_pn or medium_edges) else "",
            "rel_type_or_label": "Nachweisforderung",
            "asserted_claim": ep.get("asserted_claim", ""),
            "basis_type": "logic",
            "basis_ref": "element_proof_agent_08.csv + remediation_r02.csv + live graph",
            "verdict_before": "CONTRADICTION",
            "verdict_after": verdict_after,
            "confidence": confidence,
            "demands": str(demands),
            "fulfillments_before": str(fb),
            "fulfillments_after": str(fa),
            "q03_action": q03_action,
            "patch_op": patch_op,
            "agent_id": AGENT,
            "notes": notes,
            "ep08_claim_id": ep.get("claim_id", ""),
            "r02_claim_id": r2.get("claim_id", ""),
        })

    LEDGER_OUT.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ledger_cols, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(ledger_rows)

    n_add_node = sum(1 for op in patch_ops if op["op"] == "add_node")
    n_add_rel = sum(1 for op in patch_ops if op["op"] == "add_rel")
    n_high_rel = sum(
        1 for op in patch_ops
        if op["op"] == "add_rel" and op.get("properties", {}).get("evidence_confidence") == "high"
    )
    n_med_rel = sum(
        1 for op in patch_ops
        if op["op"] == "add_rel" and op.get("properties", {}).get("evidence_confidence") == "medium"
    )
    resolved = sum(1 for r in ledger_rows if r["verdict_after"] == "PROVEN")
    partial = sum(1 for r in ledger_rows if r["verdict_after"] == "PARTIAL_COVERAGE")

    lines = [
        "# Quality Pass Q03 — Compliance graph (Nachweisforderung residuals)",
        "",
        f"**Agent:** Q03 · **Date:** {RUN_DATE} · **Database:** `mit-bestand`",
        f"**Scope:** 11 `CONTRADICTION` dangling `Nachweisforderung` from EP-08 + R02 residuals",
        f"**Inputs:** [`ledger/element_proof_agent_08.csv`](../ledger/element_proof_agent_08.csv), "
        f"[`ledger/remediation_r02.csv`](../ledger/remediation_r02.csv)",
        f"**Output ledger:** [`ledger/quality_pass_q03.csv`](../ledger/quality_pass_q03.csv)",
        f"**Patch:** [`patches/quality_pass_q03.patch.jsonl`](../patches/quality_pass_q03.patch.jsonl)",
        "",
        "## Executive summary",
        "",
        f"- **New `PruefungNachweis` nodes created:** {n_add_node} (of 5 proposed; skipped if already present)",
        f"- **`ERFUELLT_NACHWEIS` edges added:** {n_add_rel} ({n_high_rel} high-confidence, {n_med_rel} medium-confidence)",
        f"- **Fully resolved (PROVEN):** {resolved} requirement types via new catalog procedures",
        f"- **Partial coverage (documented medium):** {partial} requirement types — satisfiable but `teilweise_belegt`",
        f"- **Destructive ops:** 0",
        "",
        "## Verdict transitions",
        "",
        "| Verdict after | Count |",
        "|---|---:|",
    ]
    for v, c in sorted(verdict_counts.items()):
        lines.append(f"| {v} | {c} |")

    lines.extend([
        "",
        "## Per-requirement outcomes",
        "",
        "| Nachweisforderung | Demands | F before → after | Q03 action | Confidence | Verdict after |",
        "|---|---:|---|---|---|---|",
    ])
    for row in ledger_rows:
        lines.append(
            f"| `{row['element_id']}` | {row['demands']} | "
            f"{row['fulfillments_before']} → {row['fulfillments_after']} | "
            f"{row['q03_action']} | {row['confidence']} | {row['verdict_after']} |"
        )

    lines.extend([
        "",
        "## New PruefungNachweis catalog entries",
        "",
        "| id | name | satisfies |",
        "|---|---|---|",
    ])
    for spec in NEW_PN_NODES:
        lines.append(f"| `{spec['id']}` | {spec['name']} | `{spec['nf_id']}` |")

    lines.extend([
        "",
        "## Medium-confidence mappings (documented, not upgraded to belegt)",
        "",
        "| PruefungNachweis → Nachweisforderung | Basis |",
        "|---|---|",
    ])
    for pn_id, nf_id, basis in MEDIUM_CONFIDENCE_FULFILLMENTS:
        lines.append(f"| `{pn_id}` → `{nf_id}` | {basis[:100]}… |")

    lines.extend([
        "",
        "## Patch operations",
        "",
        "```json",
        json.dumps(
            [{"op": o["op"], "id": o.get("id"), "from": o.get("from"), "to": o.get("to")}
             for o in patch_ops],
            indent=2,
            ensure_ascii=False,
        ),
        "```",
        "",
        "## Dry-run output",
        "",
        "```",
        dry_output.strip(),
        "```",
        "",
        "## Apply output",
        "",
        "```",
        apply_output.strip(),
        "```",
        "",
        f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}.",
    ])
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"patch_ops={len(patch_ops)} add_node={n_add_node} add_rel={n_add_rel}")
    print(f"resolved={resolved} partial={partial}")
    print(f"wrote {LEDGER_OUT}")
    print(f"wrote {REPORT_OUT}")
    print(f"wrote {PATCH_OUT}")


if __name__ == "__main__":
    main()
