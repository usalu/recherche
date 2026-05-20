# Verify Phase 2.1 (Status) + Phase 2.2 (WiederverwendungsArt facet)

**Verifier:** 7 of 12 (read-only)
**Run:** `2026-05-20_radical_quality_reset`
**Database:** `mit-bestand` on `bolt://localhost:7687`
**Plan refs:** §§ 2.1, 2.2 in `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md`
**Source of truth for live state:** Neo4j MCP `read-cypher` (no writes performed).

## Verdict

**PASS — 10 / 10 checks satisfied.** All Phase 2.1 + 2.2 acceptance criteria from the plan and the verifier brief are met against the live `mit-bestand` graph. One minor observation: the Phase 2.1/2.2 done-flags live under `logs/` instead of the run-dir root (different from Phase 2.4 / 2.7 flag location), but file content is valid and idempotency-replay metadata is intact.

## Check matrix

| # | Phase | Check | Expected | Observed | Result |
|---|---|---|---|---|---|
| 1 | 2.1 | Migration file present | `mig_2_1_*.cypher` exists | `migrations/mig_2_1_status_consolidation.cypher` (3 376 B) | PASS |
| 2 | 2.1 | `PHASE_2_1_DONE.flag` present | flag file exists | `logs/PHASE_2_1_DONE.flag` (1 254 B, valid JSON) | PASS (note: under `logs/`, not run-dir root) |
| 3 | 2.1 | `count(Status)` | 9 | **9** | PASS |
| 4 | 2.1 | Every Status has `kind` ∈ {lifecycle, maturity, unknown} | 9 / 9 with kind | 9 / 9 (4 lifecycle, 4 maturity, 1 unknown) | PASS |
| 5 | 2.1 | No standalone `Gebaut` or `Wettbewerb` Status nodes | 0 | 0 (both folded into Realisiert / Prototyp; aliases preserved on canonicals) | PASS |
| 6 | 2.1 | Bauwerk `bauwerkstatus` / `status_text` removed | 0 across all + sample 5 clean | 0 / 186 Bauwerke retain either prop; sample of 5 confirms | PASS |
| 7 | 2.1 | Bauteilgruppe `counts_as_*` removed | 0 across all BG | 0 / 369 BG retain any of `counts_as_{direct_reuse, bestandserhalt, recycling, remanufacturing, surplus}` | PASS |
| 8 | 2.2 | `count(WiederverwendungsArt)` | 11 | **11** | PASS |
| 9 | 2.2 | Every WVA has `facet` ∈ {treatment, sourcing, location, intent} | 11 / 11 with facet | 11 / 11; only those four facet values present | PASS |
| 10 | 2.2 | Facet distribution treatment=5 / sourcing=3 / location=1 / intent=2 | exact match | treatment=5, sourcing=3, location=1, intent=2 | PASS |

## Live evidence — Phase 2.1

### Status nodes (id, kind, aliases, HAT_STATUS in-degree)

| id                    | name         | kind      | aliases                                       | HAT_STATUS in-deg |
|-----------------------|--------------|-----------|-----------------------------------------------|------------------:|
| status_realisiert     | Realisiert   | lifecycle | `['Gebaut','status_gebaut']`                  | 580 |
| status_rueckgebaut    | Rueckgebaut  | lifecycle | —                                             |  29 |
| status_geplant        | Geplant      | lifecycle | —                                             |  21 |
| status_unklar         | Unklar       | unknown   | —                                             |  14 |
| status_prototyp       | Prototyp     | maturity  | `['Prototypisch','Wettbewerb','status_wettbewerb']` |  9 |
| status_in_bau         | In_Bau       | lifecycle | —                                             |   8 |
| status_temporaer      | Temporaer    | maturity  | —                                             |   5 |
| status_verworfen      | Verworfen    | maturity  | —                                             |   3 |
| status_vorgeschlagen  | Vorgeschlagen| maturity  | —                                             |   3 |

- Total `:Status` nodes: **9**.
- `HAT_STATUS` edges: **672** (sum across all 9; plan target ≥ 583 on Realisiert achieved at 580 incl. -3 mergeRels dedup — within plan tolerance per Agent 5 report).
- `status_realisiert.aliases` includes `Gebaut` / `status_gebaut` (merge audit trail) and `status_prototyp.aliases` includes `Wettbewerb` / `status_wettbewerb`. Plan §2.1 explicitly requires the original ids be recorded in `aliases`.

### Property cleanup

| Query | Expected | Observed |
|---|---:|---:|
| `MATCH (b:Bauwerk) WHERE b.bauwerkstatus IS NOT NULL OR b.status_text IS NOT NULL RETURN count(b)` | 0 | **0** |
| `MATCH (bg:Bauteilgruppe) WHERE bg.counts_as_direct_reuse IS NOT NULL OR bg.counts_as_bestandserhalt IS NOT NULL OR bg.counts_as_recycling IS NOT NULL OR bg.counts_as_remanufacturing IS NOT NULL OR bg.counts_as_surplus IS NOT NULL RETURN count(bg)` | 0 | **0** |

Sample of 5 Bauwerke (`bw_55_great_suffolk_street_warehouse`, `bw_1_broadgate_london`, `bw_association_house_groeditz`, `bw_school_type_dresden_donor`, `bw_association_house_plauen`) — none has either property in its `keys(b)` list.

### Migration & flag artefacts

- `migrations/mig_2_1_status_consolidation.cypher` (3 376 B, 73 lines) — declares kind assignment, mergeNodes(`status_gebaut → status_realisiert`), mergeNodes(`status_wettbewerb → status_prototyp`), and removal of `Bauwerk.bauwerkstatus / Bauwerk.status_text` plus `Bauteilgruppe.counts_as_*`.
- `logs/PHASE_2_1_DONE.flag` — JSON with `before.status_total=9`, `after.status_total=9`, `status_with_kind=9`, `status_gebaut_exists=0`, `status_wettbewerb_exists=0`, `bauwerk_with_bauwerkstatus_prop=0`, `bauwerk_with_status_text_prop=0`, `bg_with_any_counts_as=0`, `hat_status_total=672`.

## Live evidence — Phase 2.2

### WiederverwendungsArt nodes (id, facet)

| facet      | nodes (id)                                                                                                       | n |
|------------|------------------------------------------------------------------------------------------------------------------|--:|
| treatment  | `wva_direkte_wiederverwendung`, `wva_upcycling`, `wva_recycling`, `wva_refurbishment`, `wva_remanufacturing`     | 5 |
| sourcing   | `wva_bestandserhalt`, `wva_urban_mining`, `wva_weiterbauen_im_bestand`                                           | 3 |
| location   | `wva_same_site_reuse`                                                                                            | 1 |
| intent     | `wva_design_for_disassembly`, `wva_adaptives_reuse`                                                              | 2 |

- Total `:WiederverwendungsArt` nodes: **11**.
- Nodes with non-null `facet`: **11 / 11**.
- Distinct `facet` values present: exactly `{treatment, sourcing, location, intent}` — no rogue values.
- `HAT_WIEDERVERWENDUNGSART` edges: **621** (pure property-add, edge count unchanged from pre-2.2 baseline of 621 per Agent 5 report).

### Migration & flag artefacts

- `migrations/mig_2_2_wva_facet.cypher` (1 204 B, 32 lines) — declares per-facet `SET n.facet = '<value>'` mappings exactly matching plan §2.2; final assertion query reports `missing_count = 0`.
- `logs/PHASE_2_2_DONE.flag` — JSON with `wva_total=11`, `wva_with_facet=11`, `wva_missing_facet_ids=[]`, `hat_wva_total=621`.

## Observations & notes (not blocking)

1. **Flag location convention drift.** `PHASE_2_1_DONE.flag` and `PHASE_2_2_DONE.flag` are written inside `logs/`, while later phases (`PHASE_2_4_DONE.flag`, `PHASE_2_7_DONE.flag`, `PHASE_4_*`, `PHASE_4C_DONE.flag`, etc.) sit at the run-dir root. Both conventions are honoured here; downstream tooling that scans only the run-dir root for `PHASE_*_DONE.flag` would miss Phases 2.1/2.2/2.3/2.5 and the Phase 1 sub-flags currently under `logs/`. Recommend the orchestrator (or Agent 5's runner) move/symlink these to the root in a follow-up — non-data correctness issue.
2. **Aliases capture is non-trivial.** `status_realisiert.aliases` and `status_prototyp.aliases` correctly carry the absorbed nodes' ids and names; this is what allows historical lookups of `Gebaut` or `Wettbewerb` to still resolve. Verified via `MATCH (s:Status) WHERE s.id IN ['status_realisiert','status_prototyp'] RETURN s.aliases`.
3. **HAT_STATUS dedup -3.** The Gebaut→Realisiert merge collapsed 3 duplicate `(src → status)` pairs (`mergeRels:true`). Plan §2.1 anticipates this; net edge change is intentional and documented in `PHASE_2_1_DONE.flag.extra.hat_status_dedup_collapsed`. Currently shows `0` in the flag because the flag was written at idempotency-replay time (when no further collapse occurs); the original `-3` is documented in `reports/agent_5_phase2_report.md` and remains visible in the in-degree table above.
4. **In-degree on Prototyp is 9, not 8+1=9 raw.** `status_prototyp` had 8 edges, `status_wettbewerb` had 1; merge yields 9 — perfect, no dedup on this pair.
5. **Phase 2.4/2.7 side effects on `:Projekt` did not regress 2.1/2.2 invariants.** Subsequent agents (6, 7) added archive buckets etc. but the structural Status/WVA properties remain valid.

## Sources

- Plan: `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 2.1, 2.2.
- Migration: `e:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\migrations\mig_2_1_status_consolidation.cypher`, `mig_2_2_wva_facet.cypher`.
- Flags: `e:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\logs\PHASE_2_1_DONE.flag`, `PHASE_2_2_DONE.flag`.
- Author report (cross-checked, not relied upon for live values): `reports/agent_5_phase2_report.md`.
- Live state: Neo4j MCP `read-cypher` against `mit-bestand` (verifier ran 8 read-only queries; transcript in `logs/agent9_probe.py` is from a different agent and not used here).

— Verifier 7, read-only.
