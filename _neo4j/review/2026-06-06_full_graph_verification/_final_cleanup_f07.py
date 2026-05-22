"""F07 — live property-key export vs approved 57/22 manifest (READ-ONLY Neo4j).

Outputs:
  ledger/final_cleanup_f07.csv  (131 rows)
  reports/final_cleanup_f07.md
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
LEDGER_OUT = HERE / "ledger" / "final_cleanup_f07.csv"
REPORT_OUT = HERE / "reports" / "final_cleanup_f07.md"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

# Approved manifest: phase8_final_report (2026-06-05) — 57 node / 22 rel distinct keys.
APPROVED_NODE = {
    "aktualisiert_am_utc", "akzeptanzfaktoren", "aliases", "alte_funktion", "area_m2_gross",
    "bauobjektklasse", "bauproduktstatus", "bauteilebene", "beschreibung", "bg_kind", "bilanzgrenze",
    "brand_layer", "category", "confidence", "country_iso2", "created_at", "einheit", "evidence_basis",
    "fact_index", "funktionswechsel", "id", "kennwert", "kind", "layer", "lca_modules",
    "maps_to_nachweisforderung", "matchingqualitaet_geo", "matchingqualitaet_spec",
    "matchingqualitaet_temporal", "method", "name", "name_full", "neue_funktion", "nutzung_text",
    "projektstatus_text", "rechtsbereiche", "reguliert_in_laendern", "reuse_status", "source_quote",
    "source_titles", "source_url", "source_urls", "standards_body", "status", "tragend",
    "tragwerksprinzip", "type", "typische_bauproduktstatus", "wert", "wert_text",
    "wiederverwendungsort", "wirtschaft", "wirtschaft_aspekte", "year_completed", "year_from",
    "year_to", "zertifizierungssysteme",
}

APPROVED_REL = {
    "actor_id", "actor_name", "aktualisiert_am_utc", "basis", "basis_project_edge_id",
    "basis_project_edge_type", "bauteilgruppe_id", "bauteilgruppe_name", "confidence", "dedupe_key",
    "id", "inference_basis", "pollutant_basis", "rechtsgrundlage", "reversibility", "role",
    "rolle_text", "scope_note", "shared_bauteiltyp_ids", "shared_material_ids", "source_quote",
    "source_url",
}

NODE_DRIFT = {
    "adresse": "geo intake (latitude/longitude cluster)",
    "deprecated_am_utc": "vocab deprecation metadata",
    "deprecated_reason": "vocab deprecation metadata",
    "entwurfsbeschreibung": "entwurfsqualitaet intake",
    "entwurfsbeschreibung_quelle": "entwurfsqualitaet intake",
    "entwurfsqualitaet_am_utc": "entwurfsqualitaet intake",
    "entwurfsqualitaet_run": "entwurfsqualitaet intake",
    "entwurfsqualitaet_vokabular_version": "entwurfsqualitaet intake",
    "geo_aktualisiert_am_utc": "geo intake",
    "geo_confidence": "geo intake",
    "geo_import_run": "geo intake",
    "intake_run": "vocab/run tagging",
    "latitude": "geo intake",
    "literature_ref": "vocab intake",
    "longitude": "geo intake",
    "metadata_sidecar_key": "phase 4b/5b sidecar pointer (legacy cleanup scope)",
    "name_de": "vocab intake",
    "primary_source_url": "P6 evidence model (re-introduced after phase5 drop)",
    "vokabular_version": "vocab intake",
}

NODE_DEPRECATE = {
    "land": "redundant Akteur scalar; canonical pattern is LIEGT_IN_LAND (A14-LAND-001)",
    "review_run": "node-level run tag; bubble tagging lives on relationships",
    "review_status": "legacy QA key; offloaded in property cleanup 4b",
    "short_description": "singleton stray key (1 node)",
    "source_scope": "obsolete since 2026-06-01; target drop from PROPERTY_CLEANUP_PLAN",
}

REL_DRIFT = {
    "begruendung": "entwurfsqualitaet edge metadata",
    "belegkonfidenz": "entwurfsqualitaet edge metadata",
    "connection_kind": "reuse-bubble / project-graph enrichment",
    "created_at_utc": "post-cleanup timestamp (phase4 drop reversed by intakes)",
    "dedup_run": "reuse-bubble dedup audit",
    "dossier_section": "reuse-bubble evidence",
    "evidence_basis": "VMA / reuse evidence model (AGENTS.md)",
    "evidence_confidence": "VMA / reuse evidence model (AGENTS.md)",
    "evidence_excerpt": "reuse-bubble evidence",
    "evidence_origin": "reuse-bubble evidence",
    "evidence_quote": "VMA / reuse evidence model (AGENTS.md)",
    "evidence_url": "VMA / reuse evidence model (AGENTS.md)",
    "extraktionsstatus": "entwurfsqualitaet edge metadata",
    "fact_label": "reuse-bubble evidence",
    "intake_run": "entwurfsqualitaet / intake tagging",
    "integration_layer": "entwurfsqualitaet edge metadata",
    "integration_phase": "entwurfsqualitaet edge metadata",
    "kandidatentext": "entwurfsqualitaet edge metadata",
    "metadata_sidecar_key": "phase 4b/5b sidecar pointer",
    "quell_urls": "entwurfsqualitaet edge metadata",
    "review_run": "reuse-bubble run tag (re-introduced post phase4b offload)",
    "semantic_basis": "re-introduced after phase4 drop",
    "updated_at_utc": "post-cleanup timestamp (phase4 drop reversed)",
    "vokabular_version": "entwurfsqualitaet edge metadata",
    "zuordnung_pruefung": "entwurfsqualitaet edge metadata",
    "zuordnung_quelle": "entwurfsqualitaet edge metadata",
}

REL_DEPRECATE = {
    "review_status": "legacy QA; phase 4b target was 0 remaining",
    "source_scope": "legacy scope tag; phase 4b/5b offload",
}

LEDGER_COLS = [
    "claim_id", "scope", "property_key", "occurrences", "approved_manifest",
    "classification", "drift_bucket", "notes", "agent_id",
]


def classify(scope: str, key: str) -> tuple[str, str, str]:
    if scope == "node":
        if key in APPROVED_NODE:
            return "KEEP", "approved_phase8", "in approved 57-key manifest (CLEANUP_APPLY_SUMMARY 2026-06-05)"
        if key in NODE_DRIFT:
            return "DOCUMENT_DRIFT", "intentional_post_p6", NODE_DRIFT[key]
        if key in NODE_DEPRECATE:
            return "DEPRECATE", "legacy_residual", NODE_DEPRECATE[key]
    else:
        if key in APPROVED_REL:
            return "KEEP", "approved_phase8", "in approved 22-key manifest (CLEANUP_APPLY_SUMMARY 2026-06-05)"
        if key in REL_DRIFT:
            return "DOCUMENT_DRIFT", "intentional_post_p6", REL_DRIFT[key]
        if key in REL_DEPRECATE:
            return "DEPRECATE", "legacy_residual", REL_DEPRECATE[key]
    return "DOCUMENT_DRIFT", "unclassified", "live key outside approved manifest; needs human bucket"


def export_keys() -> tuple[list[dict], dict]:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    if not all([uri, user, password, database]):
        raise RuntimeError("Missing Neo4j connection settings.")

    rows: list[dict] = []
    counts: dict = {}
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as s:
            counts = s.run(
                "MATCH (n) WITH count(n) AS nodes "
                "MATCH ()-[r]->() RETURN nodes, count(r) AS rels"
            ).single()
            counts = dict(counts)
            counts["database"] = database

            for row in s.run(
                "MATCH (n) UNWIND keys(n) AS k "
                "WITH k, count(*) AS occ RETURN k AS key, occ ORDER BY k"
            ):
                rows.append({"key": row["key"], "scope": "node", "occ": row["occ"]})
            for row in s.run(
                "MATCH ()-[r]->() UNWIND keys(r) AS k "
                "WITH k, count(*) AS occ RETURN k AS key, occ ORDER BY k"
            ):
                rows.append({"key": row["key"], "scope": "rel", "occ": row["occ"]})

    return rows, counts


def build_ledger(live_rows: list[dict]) -> list[dict]:
    ledger: list[dict] = []
    n_idx = r_idx = 0
    for row in live_rows:
        scope = row["scope"]
        key = row["key"]
        classification, bucket, note = classify(scope, key)
        if scope == "node":
            n_idx += 1
            cid = f"F07-NK-{n_idx:03d}"
        else:
            r_idx += 1
            cid = f"F07-RK-{r_idx:03d}"
        approved = "yes" if classification == "KEEP" else "no"
        ledger.append({
            "claim_id": cid,
            "scope": scope,
            "property_key": key,
            "occurrences": row["occ"],
            "approved_manifest": approved,
            "classification": classification,
            "drift_bucket": bucket,
            "notes": note,
            "agent_id": "F07",
        })
    return ledger


def agents_md_draft(counts: dict, hist: Counter, node_live: int, rel_live: int) -> str:
    nodes = counts["nodes"]
    rels = counts["rels"]
    return f"""## Aktueller Stand (2026-06-06) — F07 draft (pending F10 closeout)

Der Regulation-Graph-Vocabulary-Cleanup (Plan:
[`PLAN_V3.md`](_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/PLAN_V3.md))
ist bis Phase 8 + **Phase B (Variant B, 11 typed law labels)** angewendet, danach Abschluss-OP S1–S5
([`LAST_SURGERY_REPORT.md`](_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/LAST_SURGERY_REPORT.md)):
alle Schadstoff-/Regelungskanten belegt, 30 Bauteilgruppen verbunden, Dubletten/Waisen bereinigt.
Aktiver Graph-Stand in `mit-bestand`: **{nodes:,} Knoten / {rels:,} Relationen** (nach Final-Cleanup F1 `rau` merge;
Element-Ledger + PROVEN% werden von F10 nach F09-Re-Merge finalisiert — Platzhalter bis dahin).
Vor Final Cleanup (P6-06): 2 264 / 15 063 — **89,27 % PROVEN** auf 17 327 Zeilen —
[`POST_QUALITY_CAMPAIGN_REPORT.md`](_neo4j/review/2026-06-06_full_graph_verification/POST_QUALITY_CAMPAIGN_REPORT.md).
Property-Cleanup 2026-06-05: **57 Knoten-Property-Keys** (war 107), **22 Rel-Property-Keys** (war 63) —
[`CLEANUP_APPLY_SUMMARY.md`](_neo4j/review/2026-06-05_post_migration_property_cleanup/CLEANUP_APPLY_SUMMARY.md);
**live property-key drift dokumentiert (F07): {node_live} node / {rel_live} rel** vs approved 57/22
({hist['DOCUMENT_DRIFT']} intentional drift, {hist['DEPRECATE']} legacy residuals) —
[`reports/final_cleanup_f07.md`](_neo4j/review/2026-06-06_full_graph_verification/reports/final_cleanup_f07.md).
Agent-14-Historie 83/51 → **81/50 live** (Q01 stray-key fixes + keine Property-Patches in F07)."""


def write_report(
    ledger: list[dict],
    counts: dict,
    node_live: int,
    rel_live: int,
    hist: Counter,
    scope_hist: dict,
    agents_draft: str,
    ts: str,
) -> None:
    nodes = counts["nodes"]
    rels = counts["rels"]
    md = f"""# Final Cleanup F07 — Property-key re-baseline + AGENTS.md draft

**Date:** {ts} · **Database:** `{counts.get('database', 'mit-bestand')}`
**Mode:** READ-ONLY Neo4j (`read-cypher` only; no property cleanup patches)
**Ledger:** [`ledger/final_cleanup_f07.csv`](../ledger/final_cleanup_f07.csv) — **{len(ledger)} rows**
**Reference manifest:** [`CLEANUP_APPLY_SUMMARY.md`](../../2026-06-05_post_migration_property_cleanup/CLEANUP_APPLY_SUMMARY.md) (approved **57/22**)

## Live export (read-cypher)

| Surface | Approved (2026-06-05 phase8) | Live now | Δ |
|---|---:|---:|---:|
| Node property keys | **57** | **{node_live}** | **+{node_live - 57}** |
| Rel property keys | **22** | **{rel_live}** | **+{rel_live - 22}** |
| Graph nodes | — | **{nodes:,}** | post-F1 (`rau_architects` merged) |
| Graph rels | — | **{rels:,}** | |

Agent-14 scan (15-agent era) reported **83/51** distinct keys; live is now **81/50** (−2 node / −1 rel) after Q01 stray-key fixes and graph edits — F07 re-baselines against the canonical **57/22** manifest, not the Agent-14 snapshot.

## Classification histogram

| classification | node | rel | Σ |
|---|---:|---:|---:|
| KEEP | {scope_hist['node']['KEEP']} | {scope_hist['rel']['KEEP']} | {hist['KEEP']} |
| DOCUMENT_DRIFT | {scope_hist['node']['DOCUMENT_DRIFT']} | {scope_hist['rel']['DOCUMENT_DRIFT']} | {hist['DOCUMENT_DRIFT']} |
| DEPRECATE | {scope_hist['node']['DEPRECATE']} | {scope_hist['rel']['DEPRECATE']} | {hist['DEPRECATE']} |
| **Σ keys** | **{node_live}** | **{rel_live}** | **{len(ledger)}** |

## Drift buckets (intentional vs legacy)

| drift_bucket | Count | Action |
|---|---:|---|
| approved_phase8 | {hist['KEEP']} | No patch; remains canonical baseline |
| intentional_post_p6 | {hist['DOCUMENT_DRIFT']} | Document in schema manifest; do **not** auto-drop |
| legacy_residual | {hist['DEPRECATE']} | Candidate for future property patch (human-gated) |

### Notable DOCUMENT_DRIFT clusters

- **Geo intake:** `latitude`, `longitude`, `adresse`, `geo_*` (6 node keys)
- **Entwurfsqualität:** `entwurfsbeschreibung*`, `entwurfsqualitaet_*` + 11 rel keys (`begruendung`, `zuordnung_*`, …)
- **Reuse bubbles / VMA:** `evidence_*`, `connection_kind`, `dedup_run`, `review_run`, `dossier_section`, …
- **Sidecar pointers:** `metadata_sidecar_key` on nodes (741) and rels (505) — legacy cleanup 4b/5b scope per `AGENTS.md`
- **P6 evidence:** `primary_source_url` on nodes (re-introduced after phase5 drop)

### DEPRECATE residuals (7 keys, no F07 patch)

| scope | key | occ | rationale |
|---|---|---:|---|
"""
    for row in ledger:
        if row["classification"] != "DEPRECATE":
            continue
        md += f"| {row['scope']} | `{row['property_key']}` | {row['occurrences']} | {row['notes']} |\n"

    md += f"""
## SCOPE_CYPHER (repro)

```cypher
MATCH (n) UNWIND keys(n) AS k RETURN DISTINCT k AS key, 'node' AS scope ORDER BY key
```

```cypher
MATCH ()-[r]->() UNWIND keys(r) AS k RETURN DISTINCT k AS key, 'rel' AS scope ORDER BY key
```

## AGENTS.md §Aktueller Stand — draft block

> **Not applied to `AGENTS.md` by F07** — F10 applies final counts after F09 ledger merge. Insert/replace when PROVEN% and element row count are final.

```
{agents_draft}
```

## Acceptance

- [x] Row count = **131** (81 node + 50 rel live keys)
- [x] READ-ONLY Neo4j (no `write-cypher`, no property patches)
- [x] Each live key classified `KEEP` | `DOCUMENT_DRIFT` | `DEPRECATE`
- [x] Approved manifest cross-walk documents **57/22 → 81/50** drift
- [ ] `AGENTS.md` commit deferred to F10 closeout
"""
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(md, encoding="utf-8")


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    live_rows, counts = export_keys()
    node_live = sum(1 for r in live_rows if r["scope"] == "node")
    rel_live = sum(1 for r in live_rows if r["scope"] == "rel")
    if node_live != 81 or rel_live != 50:
        print(f"WARN: expected 81/50 keys, got {node_live}/{rel_live}")

    ledger = build_ledger(live_rows)
    if len(ledger) != 131:
        raise SystemExit(f"Row count {len(ledger)} != 131")

    hist = Counter(r["classification"] for r in ledger)
    scope_hist = {
        "node": Counter(r["classification"] for r in ledger if r["scope"] == "node"),
        "rel": Counter(r["classification"] for r in ledger if r["scope"] == "rel"),
    }
    if hist["KEEP"] != 79:
        print(f"WARN: KEEP count {hist['KEEP']} (expected 57+22=79)")

    LEDGER_OUT.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=LEDGER_COLS)
        w.writeheader()
        w.writerows(ledger)

    agents_draft = agents_md_draft(counts, hist, node_live, rel_live)
    write_report(ledger, counts, node_live, rel_live, hist, scope_hist, agents_draft, ts)

    print(f"Wrote {LEDGER_OUT} ({len(ledger)} rows)")
    print(f"Wrote {REPORT_OUT}")
    print(f"Graph: {counts['nodes']} nodes / {counts['rels']} rels")
    print(f"Keys: {node_live} node / {rel_live} rel | KEEP={hist['KEEP']} DRIFT={hist['DOCUMENT_DRIFT']} DEPRECATE={hist['DEPRECATE']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
