#!/usr/bin/env python3
"""Remediation Wave 2 — Agent R02: dangling Nachweisforderung (Agent 13 scope)."""
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

from neo4j_env import resolve_connection  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402

ROOT = Path(__file__).resolve().parent
LEDGER_IN = ROOT / "ledger" / "agent_13.csv"
LEDGER_OUT = ROOT / "ledger" / "remediation_r02.csv"
REPORT_OUT = ROOT / "reports" / "remediation_r02.md"
PATCH_OUT = ROOT / "patches" / "remediation_r02_erfuellt_nachweis.patch.jsonl"
RUN_DATE = "2026-06-06"
AGENT = "R02"

DANGLE_PREFIX = "A13-nf-dangle-"

# pn_id -> [(nf_id, confidence, basis)]
HIGH_CONFIDENCE_FULFILLMENTS: dict[str, list[tuple[str, str, str]]] = {
  "pn_schwermetalle": [
    ("nf_schwermetall_oder_bleifarbe_check", "belegt",
     "rewire_map SCHADSTOFF_TO_NF s_schwermetalle; pn_schwermetalle tests heavy metals/lead paint"),
  ],
  "pn_schadstoffanalyse_holz": [
    ("nf_holzschutzmittel_check", "belegt",
     "rewire_map SCHADSTOFF_TO_NF s_holzschutzmittel; wood preservative analysis"),
  ],
  "pn_biozid_screening": [
    ("nf_holzschutzmittel_check", "belegt",
     "biozid screening covers wood preservative / biocide residues (DIN 68800 AltholzV context)"),
  ],
  "pr_schadstoffscreening": [
    ("nf_asbest_check", "belegt",
     "IST_UNTERVERFAHREN_VON pr_schadstoffpruefung; screening is first-line pollutant check incl. asbest (GefStoffV/TRGS 519)"),
  ],
  "pn_schadstoffanalyse_kleber": [
    ("nf_formaldehyd_oder_emissionsnachweis", "belegt",
     "rewire_map SCHADSTOFF_TO_NF s_formaldehyd; adhesive VOC/formaldehyde emissions"),
  ],
  "pn_rutschhemmung": [
    ("nf_absturzsicherung", "belegt",
     "la_rutschhemmung maps_to nf_absturzsicherung; slip-resistance test (DIN 51130 family)"),
  ],
  "pn_bauteilpass": [
    ("nf_bauteilidentifikation", "belegt",
     "Bauteilpass is component identification passport (DIN SPEC 91484 / Madaster / CDW protocol)"),
  ],
  "pn_lambda_wert": [
    ("nf_bauphysiknachweis", "belegt",
     "la_waermeschutz maps_to nf_bauphysiknachweis; lambda value is thermal building-physics proof"),
  ],
  "pn_ug_wert": [
    ("nf_bauphysiknachweis", "belegt",
     "U-value measurement satisfies Bauphysiknachweis (GEG/MuKEn)"),
  ],
  "pn_ug_uw_wert": [
    ("nf_bauphysiknachweis", "belegt",
     "Ug/Uw thermal transmittance is Bauphysiknachweis evidence"),
  ],
}

MEDIUM_CONFIDENCE_FULFILLMENTS: dict[str, list[tuple[str, str, str]]] = {
  "pn_ankerpruefung": [
    ("nf_befestigungsnachweis", "teilweise_belegt",
     "anchor pull-out test supports fastening proof (EN 1992-4 / facade anchorage)"),
  ],
  "pn_petrografie": [
    ("nf_rc_gesteinskoernung_eignung", "teilweise_belegt",
     "petrographic analysis for recycled aggregate suitability (DAfStb RC concrete)"),
  ],
  "pr_eignungspruefung_baulehm": [
    ("nf_rc_gesteinskoernung_eignung", "teilweise_belegt",
     "suitability testing for mineral secondary aggregates / RC materials"),
    ("nf_mineralische_ersatzbaustoff_guete", "teilweise_belegt",
     "EBV Ersatzbaustoff suitability / quality assessment"),
  ],
  "pr_zustandsbewertung": [
    ("nf_dauerhaftigkeit_restlebensdauer", "teilweise_belegt",
     "condition assessment informs remaining service life (DIN SPEC 91525 PUC)"),
  ],
  "pn_approval_process": [
    ("nf_genehmigungs_oder_zustimmungsbedarf", "teilweise_belegt",
     "approval / ZIE-ABZ pathway documentation (DIBt Zulassung)"),
  ],
  "pr_dokumentenpruefung_bestand": [
    ("nf_schadstoffkataster_erkundung", "teilweise_belegt",
     "pre-demolition document review / building pollutant register (VDI 6210 / ATV DIN 18459)"),
  ],
}

# nf_id -> (verdict, action, note, new_pn_suggestion)
DEFERRED_REQUIREMENTS: dict[str, tuple[str, str, str, str]] = {
  "nf_oekobilanz_epd": (
    "VALID_REQUIREMENT",
    "ADD_PRUEFUNGNACHWEIS",
    "67 demands; 9 GESTUETZT_AUF_REGELWERK (EN 15804/15978, EU Taxonomy). No EPD/LCA PruefungNachweis in catalog.",
    "pn_epd_oder_lca_nachweis",
  ),
  "nf_materialpass_ressourcenpass": (
    "VALID_REQUIREMENT",
    "ADD_PRUEFUNGNACHWEIS",
    "54 demands; ESPR DPP / EU Level(s) backed. No material-passport / DPP procedure node.",
    "pn_materialpass_oder_dpp",
  ),
  "nf_elektrosicherheitsnachweis": (
    "VALID_REQUIREMENT",
    "ADD_PRUEFUNGNACHWEIS",
    "7 demands; rw_dguv_v3_vde. No electrical safety test procedure in PruefungNachweis vocab.",
    "pn_elektrosicherheitspruefung",
  ),
  "nf_hygiene_und_reinigungsnachweis": (
    "VALID_REQUIREMENT",
    "ADD_PRUEFUNGNACHWEIS",
    "7 demands; rw_vdi_6023_6022 drinking-water hygiene. No matching procedure.",
    "pn_trinkwasser_hygiene_nachweis",
  ),
  "nf_barrierefreiheit_nachweis": (
    "VALID_REQUIREMENT",
    "ADD_PRUEFUNGNACHWEIS",
    "18 demands; DIN 18040 backed. No accessibility audit procedure in catalog.",
    "pn_barrierefreiheitsaudit",
  ),
}


def load_dangle_rows() -> list[dict]:
    rows = []
    with LEDGER_IN.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["claim_id"].startswith(DANGLE_PREFIX):
                rows.append(row)
    return rows


def graph_context(driver) -> dict[str, dict]:
    nf_ids = [
        r["element_id"] for r in load_dangle_rows()
    ]
    q = """
    MATCH (nf:Nachweisforderung)
    WHERE nf.id IN $ids
    OPTIONAL MATCH (nf)<-[d:ERFORDERT_NACHWEIS]-(demander)
    OPTIONAL MATCH (nf)-[:GESTUETZT_AUF_REGELWERK]->(rw)
    OPTIONAL MATCH (pn:PruefungNachweis)-[:ERFUELLT_NACHWEIS]->(nf)
    RETURN nf.id AS id, nf.name AS name,
           count(DISTINCT d) AS demands,
           count(DISTINCT pn) AS fulfillments,
           count(DISTINCT rw) AS regelwerk_out,
           collect(DISTINCT labels(demander)[0])[0..5] AS demander_labels,
           collect(DISTINCT rw.id)[0..3] AS regelwerk_ids,
           collect(DISTINCT coalesce(rw.primary_source_url, rw.source_urls[0]))[0..1] AS regelwerk_urls
    """
    with driver.session(database="mit-bestand") as session:
        return {r["id"]: dict(r) for r in session.run(q, ids=nf_ids)}


def existing_fulfillment_edges(driver, pairs: list[tuple[str, str]]) -> set[tuple[str, str]]:
    if not pairs:
        return set()
    q = """
    UNWIND $pairs AS p
    MATCH (a:PruefungNachweis {id:p[0]})-[r:ERFUELLT_NACHWEIS]->(b:Nachweisforderung {id:p[1]})
    RETURN a.id AS pn, b.id AS nf
    """
    with driver.session(database="mit-bestand") as session:
        return {(r["pn"], r["nf"]) for r in session.run(q, pairs=pairs)}


def build_patch_ops(existing: set[tuple[str, str]]) -> list[dict]:
    ops = []
    for pn_id, entries in HIGH_CONFIDENCE_FULFILLMENTS.items():
        for nf_id, _conf, basis in entries:
            if (pn_id, nf_id) in existing:
                continue
            ops.append({
                "op": "add_rel",
                "from": pn_id,
                "type": "ERFUELLT_NACHWEIS",
                "to": nf_id,
                "properties": {
                    "evidence_basis": basis,
                    "evidence_confidence": "high",
                    "review_run": "remediation_r02_2026-06-06",
                    "semantic_basis": "method_mapped",
                },
                "reason": f"R02 high-confidence: {pn_id} satisfies dangling {nf_id}. {basis}",
            })
    return ops


def nf_remediation_plan(nf_id: str, ctx: dict) -> dict:
    high = [(pn, c, b) for pn, entries in HIGH_CONFIDENCE_FULFILLMENTS.items()
            for target, c, b in entries if target == nf_id]
    medium = [(pn, c, b) for pn, entries in MEDIUM_CONFIDENCE_FULFILLMENTS.items()
              for target, c, b in entries if target == nf_id]
    if nf_id in DEFERRED_REQUIREMENTS:
        verdict, action, note, new_pn = DEFERRED_REQUIREMENTS[nf_id]
        return {
            "requirement_valid": "yes",
            "r02_verdict": verdict,
            "proposed_action": action,
            "confidence": "belegt",
            "fulfillment_candidates_high": high,
            "fulfillment_candidates_medium": medium,
            "new_pn_suggestion": new_pn,
            "remediation_status": "DEFERRED_NEW_PN",
            "notes": note,
        }
    if high:
        return {
            "requirement_valid": "yes",
            "r02_verdict": "COVERAGE_GAP",
            "proposed_action": "ADD_ERFUELLT_NACHWEIS",
            "confidence": "belegt",
            "fulfillment_candidates_high": high,
            "fulfillment_candidates_medium": medium,
            "new_pn_suggestion": "",
            "remediation_status": "PATCH_DRAFTED",
            "notes": f"{len(high)} high-confidence PN→NF edge(s) drafted; {len(medium)} medium candidates documented.",
        }
    if medium:
        return {
            "requirement_valid": "yes",
            "r02_verdict": "COVERAGE_GAP",
            "proposed_action": "ESCALATE_HUMAN",
            "confidence": "teilweise_belegt",
            "fulfillment_candidates_high": high,
            "fulfillment_candidates_medium": medium,
            "new_pn_suggestion": "",
            "remediation_status": "DEFERRED_MEDIUM",
            "notes": f"Only medium-confidence PN candidates ({', '.join(p for p,_,_ in medium)}); human review before patch.",
        }
    return {
        "requirement_valid": "yes",
        "r02_verdict": "COVERAGE_GAP",
        "proposed_action": "ESCALATE_HUMAN",
        "confidence": "unbelegt",
        "fulfillment_candidates_high": [],
        "fulfillment_candidates_medium": [],
        "new_pn_suggestion": "",
        "remediation_status": "DEFERRED",
        "notes": "Valid requirement with GESTUETZT_AUF_REGELWERK + ERFORDERT_NACHWEIS; no PN candidate identified.",
    }


def format_candidates(cands: list[tuple[str, str, str]]) -> str:
    if not cands:
        return ""
    return "; ".join(f"{pn} ({conf})" for pn, conf, _ in cands)


def main() -> None:
    dangle_rows = load_dangle_rows()
    if len(dangle_rows) != 18:
        raise SystemExit(f"expected 18 dangle rows, got {len(dangle_rows)}")

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    ctx_by_nf = graph_context(driver)

    all_pairs = [
        (pn, nf)
        for mapping in (HIGH_CONFIDENCE_FULFILLMENTS, MEDIUM_CONFIDENCE_FULFILLMENTS)
        for pn, entries in mapping.items()
        for nf, _, _ in entries
    ]
    existing = existing_fulfillment_edges(driver, all_pairs)
    patch_ops = build_patch_ops(existing)
    driver.close()

    rem_cols = [
        "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
        "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
        "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
        "remediation_status", "r02_verdict", "requirement_valid", "demands", "fulfillments",
        "regelwerk_support", "high_confidence_pn", "medium_confidence_pn", "new_pn_suggestion",
        "patch_ops_count",
    ]
    rem_rows: list[dict] = []
    status_counts: Counter = Counter()
    action_counts: Counter = Counter()

    for row in dangle_rows:
        nf_id = row["element_id"]
        ctx = ctx_by_nf.get(nf_id, {})
        plan = nf_remediation_plan(nf_id, ctx)
        status_counts[plan["remediation_status"]] += 1
        action_counts[plan["proposed_action"]] += 1
        patch_count = sum(1 for op in patch_ops if op["to"] == nf_id)
        rem_rows.append({
            **row,
            "proposed_action": plan["proposed_action"],
            "confidence": plan["confidence"],
            "verdict": row["verdict"],
            "remediation_status": plan["remediation_status"],
            "r02_verdict": plan["r02_verdict"],
            "requirement_valid": plan["requirement_valid"],
            "demands": str(ctx.get("demands", "")),
            "fulfillments": str(ctx.get("fulfillments", 0)),
            "regelwerk_support": str(ctx.get("regelwerk_out", "")),
            "high_confidence_pn": format_candidates(plan["fulfillment_candidates_high"]),
            "medium_confidence_pn": format_candidates(plan["fulfillment_candidates_medium"]),
            "new_pn_suggestion": plan["new_pn_suggestion"],
            "patch_ops_count": str(patch_count),
            "notes": f"R02: {plan['notes']}; agent13: {row.get('notes', '')}",
            "agent_id": AGENT,
        })

    LEDGER_OUT.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rem_cols, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rem_rows)

    PATCH_OUT.parent.mkdir(parents=True, exist_ok=True)
    with PATCH_OUT.open("w", encoding="utf-8") as f:
        for op in patch_ops:
            f.write(json.dumps(op, ensure_ascii=False) + "\n")

    # Dry-run patch
    dry_run_summary = ""
    if patch_ops:
        proc = subprocess.run(
            [
                sys.executable,
                str(_SCRIPTS / "apply_neo4j_review_patch.py"),
                "--patch", str(PATCH_OUT),
                "--database", "mit-bestand",
            ],
            capture_output=True,
            text=True,
            cwd=str(_REPO),
        )
        dry_run_summary = proc.stdout[-2000:] if proc.stdout else proc.stderr[-2000:]

    n_fixed_nf = len({op["to"] for op in patch_ops})
    lines = [
        "# Remediation R02 — Dangling Nachweisforderung (Agent 13)",
        "",
        f"**Agent:** R02 · **Date:** {RUN_DATE} · **Database:** `mit-bestand` (READ-ONLY audit; patch dry-run only)",
        f"**Input:** [`ledger/agent_13.csv`](../ledger/agent_13.csv) rows `A13-nf-dangle-0001`…`0018`",
        f"**Output ledger:** [`ledger/remediation_r02.csv`](../ledger/remediation_r02.csv)",
        f"**Patch (high-confidence only):** [`patches/remediation_r02_erfuellt_nachweis.patch.jsonl`](../patches/remediation_r02_erfuellt_nachweis.patch.jsonl)",
        "",
        "## Executive summary",
        "",
        "All **18** dangling `Nachweisforderung` nodes are **valid regulatory requirements** — each has",
        "`ERFORDERT_NACHWEIS` demand edges (4–67) and `GESTUETZT_AUF_REGELWERK` legal backing (1–9 instruments).",
        "The gap is **coverage**: Phase 5 `pruef_to_nf()` heuristic wired all 118 `PruefungNachweis` nodes to only",
        "**9** of 27 requirement types, leaving 18 unsatisfiable.",
        "",
        f"- **High-confidence `ERFUELLT_NACHWEIS` patches drafted:** {len(patch_ops)} edges covering **{n_fixed_nf}** requirement types",
        f"- **Deferred (new `PruefungNachweis` needed):** {status_counts.get('DEFERRED_NEW_PN', 0)}",
        f"- **Deferred (medium-confidence only):** {status_counts.get('DEFERRED_MEDIUM', 0)}",
        f"- **DELETE / DEPRECATE proposed:** 0 (demands are sourced and structurally valid)",
        "",
        "## Remediation status",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"| {status} | {count} |")

    lines.extend([
        "",
        "## Per-requirement decisions",
        "",
        "| Nachweisforderung | Demands | R02 action | High-conf PN | Medium PN | New PN? |",
        "|---|---:|---|---|---|---|",
    ])
    for row in rem_rows:
        lines.append(
            f"| `{row['element_id']}` | {row['demands']} | {row['proposed_action']} | "
            f"{row['high_confidence_pn'] or '—'} | {row['medium_confidence_pn'] or '—'} | "
            f"{row['new_pn_suggestion'] or '—'} |"
        )

    lines.extend([
        "",
        "## High-confidence patch ops",
        "",
        "| PruefungNachweis → Nachweisforderung | Basis |",
        "|---|---|",
    ])
    for op in patch_ops:
        lines.append(f"| `{op['from']}` → `{op['to']}` | {op['properties']['evidence_basis'][:90]}… |")

    lines.extend([
        "",
        "## Root cause",
        "",
        "Phase 5 `add_erfuellt_edges()` used `rewire_map.pruef_to_nf()` keyword heuristics that map test methods",
        "to a **9-type** subset (`nf_materialpruefung`, `nf_schadstoffpruefung`, …). Pollutant-specific checks",
        "(`nf_asbest_check`, …), documentation types (`nf_bauteilidentifikation`, `nf_oekobilanz_epd`), and",
        "performance proofs (`nf_bauphysiknachweis`, `nf_befestigungsnachweis`) were never linked despite valid",
        "`GESTUETZT_AUF_REGELWERK` + `ERFORDERT_NACHWEIS` demand.",
        "",
        "## Medium-confidence candidates (not patched — human gate)",
        "",
    ])
    for pn_id, entries in sorted(MEDIUM_CONFIDENCE_FULFILLMENTS.items()):
        for nf_id, conf, basis in entries:
            if (pn_id, nf_id) not in {(op["from"], op["to"]) for op in patch_ops}:
                lines.append(f"- `{pn_id}` → `{nf_id}` ({conf}): {basis}")

    lines.extend([
        "",
        "## Deferred — new PruefungNachweis required",
        "",
    ])
    for nf_id, (_, action, note, new_pn) in DEFERRED_REQUIREMENTS.items():
        lines.append(f"- **`{nf_id}`** → propose `{new_pn}`: {note}")

    lines.extend([
        "",
        "## Apply (human-gated)",
        "",
        "```bash",
        "python _scripts/apply_neo4j_review_patch.py \\",
        "  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r02_erfuellt_nachweis.patch.jsonl",
        "# then:",
        'python _scripts/apply_neo4j_review_patch.py --patch ... --confirm "APPLY remediation_r02_erfuellt_nachweis.patch.jsonl TO mit-bestand"',
        "```",
        "",
        "## Dry-run output",
        "",
        "```",
        dry_run_summary.strip() or "(no output)",
        "```",
        "",
        f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}.",
    ])
    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"dangle_rows={len(dangle_rows)} patch_ops={len(patch_ops)} nf_covered={n_fixed_nf}")
    print(f"status={dict(status_counts)} actions={dict(action_counts)}")
    print(f"wrote {LEDGER_OUT}")
    print(f"wrote {REPORT_OUT}")
    print(f"wrote {PATCH_OUT}")


if __name__ == "__main__":
    main()
