# Final Verification — Phase 2.1 (Status) + Phase 2.2 (WiederverwendungsArt facet)

- **Phases**: 2.1 — add `kind` property on `:Status`; merge `Gebaut`→`Realisiert`, `Wettbewerb`→`Prototyp`; drop redundant `Bauwerk` / `Bauteilgruppe` props. 2.2 — add `facet` property on `:WiederverwendungsArt`.
- **Database**: `mit-bestand` on `bolt://localhost:7687` (live, read-only via Neo4j MCP `read-cypher`).
- **Run dir**: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Plan**: `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 2.1, 2.2
- **Verifier**: Final Verifier 4 of 12 — read-only (no writes performed)
- **Verified at**: 2026-05-21 (live MCP queries)

## Verdict

**PASS — 10 / 10 checks satisfied.** All Phase 2.1 + 2.2 acceptance criteria from the plan and the verifier brief are met against the live `mit-bestand` graph. One non-blocking note: the `PHASE_2_1_DONE.flag` and `PHASE_2_2_DONE.flag` artefacts live under `logs/` rather than the run-dir root (same convention drift already documented by earlier verifier 7). File contents are valid JSON.

## Check Results

| # | Phase | Check | Expected | Observed | Result |
|---|-------|-------|----------|----------|--------|
| 1 | 2.1 | `PHASE_2_1_DONE.flag` present | flag exists in run dir | `logs/PHASE_2_1_DONE.flag` (1 254 B, valid JSON; `before == after`; `status_with_kind=9`, `bg_with_any_counts_as=0`, `hat_status_total=672`) | **PASS** (note: under `logs/`) |
| 2 | 2.2 | `PHASE_2_2_DONE.flag` present | flag exists in run dir | `logs/PHASE_2_2_DONE.flag` (345 B, valid JSON; `wva_total=11`, `wva_with_facet=11`, `wva_missing_facet_ids=[]`, `hat_wva_total=621`) | **PASS** (note: under `logs/`) |
| 3 | 2.1 | `MATCH (s:Status) RETURN count(s)` == 9 | 9 | **9** | **PASS** |
| 4 | 2.1 | `MATCH (s:Status) WHERE s.kind IN ['lifecycle','maturity','unknown'] RETURN count(s)` == 9 | 9 | **9** (lifecycle=4, maturity=4, unknown=1) | **PASS** |
| 5 | 2.1 | No standalone `:Status` with id/name `Gebaut` or `Wettbewerb` | 0 | **0** (aliases preserved on canonicals — see below) | **PASS** |
| 6 | 2.1 | `MATCH (b:Bauwerk) WHERE b.bauwerkstatus IS NOT NULL OR b.status_text IS NOT NULL RETURN count(b)` == 0 | 0 | **0** | **PASS** |
| 7 | 2.1 | `MATCH (bg:Bauteilgruppe) WHERE bg.counts_as_direct_reuse IS NOT NULL OR bg.counts_as_bestandserhalt IS NOT NULL OR bg.counts_as_recycling IS NOT NULL OR bg.counts_as_remanufacturing IS NOT NULL OR bg.counts_as_surplus IS NOT NULL RETURN count(bg)` == 0 | 0 | **0** | **PASS** |
| 8 | 2.2 | `MATCH (w:WiederverwendungsArt) RETURN count(w)` == 11 | 11 | **11** | **PASS** |
| 9 | 2.2 | `MATCH (w:WiederverwendungsArt) WHERE w.facet IN ['treatment','sourcing','location','intent'] RETURN count(w)` == 11 | 11 | **11** | **PASS** |
| 10 | 2.2 | Facet distribution: treatment ≥ 4, sourcing ≥ 2, location ≥ 1, intent ≥ 1 | thresholds | treatment=**5**, sourcing=**3**, location=**1**, intent=**2** | **PASS** |

## Live Evidence — Phase 2.1

### `:Status` nodes (id, name, kind, aliases)

| id | name | kind | aliases |
|---|---|---|---|
| status_geplant | Geplant | lifecycle | — |
| status_in_bau | In_Bau | lifecycle | — |
| status_prototyp | Prototyp | maturity | `['Prototypisch','Wettbewerb','status_wettbewerb']` |
| status_realisiert | Realisiert | lifecycle | `['Gebaut','status_gebaut']` |
| status_rueckgebaut | Rueckgebaut | lifecycle | — |
| status_temporaer | Temporaer | maturity | — |
| status_unklar | Unklar | unknown | — |
| status_verworfen | Verworfen | maturity | — |
| status_vorgeschlagen | Vorgeschlagen | maturity | — |

- Total `:Status` nodes: **9** (matches plan target 11 → 9 after merges).
- Every `:Status` has `kind` (9 / 9). Distribution: lifecycle=4, maturity=4, unknown=1.
- Absorbed ids (`status_gebaut`, `status_wettbewerb`) do **not** appear as standalone nodes — their provenance is preserved only in `aliases` on the canonical Realisiert / Prototyp nodes, matching plan §2.1 explicitly.

### Property cleanup

| Query | Expected | Observed |
|---|---:|---:|
| `MATCH (b:Bauwerk) WHERE b.bauwerkstatus IS NOT NULL OR b.status_text IS NOT NULL RETURN count(b)` | 0 | **0** |
| `MATCH (bg:Bauteilgruppe) WHERE bg.counts_as_direct_reuse IS NOT NULL OR bg.counts_as_bestandserhalt IS NOT NULL OR bg.counts_as_recycling IS NOT NULL OR bg.counts_as_remanufacturing IS NOT NULL OR bg.counts_as_surplus IS NOT NULL RETURN count(bg)` | 0 | **0** |

### Artefacts

- Migration: `migrations/mig_2_1_status_consolidation.cypher` (3 347 B).
- Flag: `logs/PHASE_2_1_DONE.flag` — `phase=2.1`, `before.status_total=9`, `after.status_total=9`, `status_with_kind=9`, `status_gebaut_exists=0`, `status_wettbewerb_exists=0`, `bauwerk_with_bauwerkstatus_prop=0`, `bauwerk_with_status_text_prop=0`, `bg_with_any_counts_as=0`, `hat_status_total=672`, `extra.hat_status_dedup_collapsed=0` (idempotent replay; original 3-edge dedup is recorded in `agent_5_phase2_report.md`).

## Live Evidence — Phase 2.2

### `:WiederverwendungsArt` by `facet`

| facet | n | ids |
|---|--:|---|
| treatment | **5** | `wva_direkte_wiederverwendung`, `wva_upcycling`, `wva_recycling`, `wva_refurbishment`, `wva_remanufacturing` |
| sourcing | **3** | `wva_bestandserhalt`, `wva_urban_mining`, `wva_weiterbauen_im_bestand` |
| location | **1** | `wva_same_site_reuse` |
| intent | **2** | `wva_design_for_disassembly`, `wva_adaptives_reuse` |

- Total `:WiederverwendungsArt` nodes: **11**.
- Nodes with non-null `facet`: **11 / 11**.
- Distinct `facet` values present: exactly `{treatment, sourcing, location, intent}` — no rogue values.
- Distribution clears every plan threshold (treatment 5 ≥ 4, sourcing 3 ≥ 2, location 1 ≥ 1, intent 2 ≥ 1).

### Artefacts

- Migration: `migrations/mig_2_2_wva_facet.cypher` (1 204 B).
- Flag: `logs/PHASE_2_2_DONE.flag` — `phase=2.2`, `wva_total=11`, `wva_with_facet=11`, `wva_missing_facet_ids=[]`, `hat_wva_total=621`.

## Observations / Notes (non-blocking)

1. **Flag location convention drift.** `PHASE_2_1_DONE.flag` and `PHASE_2_2_DONE.flag` live under `logs/` (alongside `PHASE_2_3_DONE.flag` and `PHASE_2_5_DONE.flag`), while `PHASE_2_4_DONE.flag` and `PHASE_2_7_DONE.flag` sit at the run-dir root. Both content sets are valid; the task statement allows the flag "to be present" without specifying a fixed sub-path, so this is treated as PASS. Recommend the orchestrator standardise location in a follow-up run.
2. **Aliases preserved correctly.** `status_realisiert.aliases = ['Gebaut','status_gebaut']` and `status_prototyp.aliases = ['Prototypisch','Wettbewerb','status_wettbewerb']` — exactly the provenance the plan §2.1 requires.
3. **`hat_status_total=672`** matches the plan-conformant after-merge count (sum of in-degrees across 9 canonical Status nodes; 3 duplicate edges collapsed during the original Gebaut→Realisiert merge per `agent_5_phase2_report.md`).
4. **`hat_wva_total=621`** is unchanged across before/after — Phase 2.2 is a pure property-add migration, never touches edges.
5. **No regression from later phases.** Subsequent Phase 2.4/2.7/3.x/4.x/5 work did not alter the structural invariants verified here.

## Sources

- Plan: `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 2.1, 2.2 (lines 553–581).
- Migrations: `migrations/mig_2_1_status_consolidation.cypher`, `migrations/mig_2_2_wva_facet.cypher`.
- Flags: `logs/PHASE_2_1_DONE.flag`, `logs/PHASE_2_2_DONE.flag`.
- Author report (cross-checked, not relied upon for live numbers): `reports/agent_5_phase2_report.md`.
- Prior verifier (independent): `reports/verify_phase2_1_2.md` / `.json` (Verifier 7 of 12) — agrees on all 10 checks.
- Live state: Neo4j MCP `read-cypher` against `mit-bestand` (4 read-only queries, no writes).

— Final Verifier 4 of 12, read-only.
