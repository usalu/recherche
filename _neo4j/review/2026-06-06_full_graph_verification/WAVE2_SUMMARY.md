# Wave 2 Remediation Summary — R01–R07

**Date:** 2026-06-06 · **Database:** `mit-bestand`
**Post-wave graph:** **2 284 nodes / 15 312 relationships** (unchanged after R07 property-only apply).

Wave 1 (campaign patches: dedup, unsupported deletes, agent15/06b sources) ended at **2 296 / 15 338**.
Wave 2 applied seven gated remediation batches; net structural delta **−12 nodes / −26 rels** (merges + deletes + adds).

---

## Applied (all live, 0 errors)

| Batch | Patch | Ops | Graph delta | Report |
|---|---|---:|---|---|
| **R01** Materialdepots | `remediation_r01_materialdepot_sources.patch.jsonl` | 5 `set_node_properties` | — | [`reports/remediation_r01.md`](reports/remediation_r01.md) |
| **R04** Madaster / RAU / HarvestMAP | `remediation_r04_madaster_rau_harvestmap.patch.jsonl` | 4 `delete_rel`, 1 `merge_node`, 1 `set_node_properties`, 1 `set_rel_properties` | 2296→2295 / 15338→15327 | [`reports/remediation_r04.md`](reports/remediation_r04.md) |
| **R06** Dead regulation URLs | `remediation_r06_regulation_urls.patch.jsonl` | 63 `set_rel_properties` | — | [`reports/remediation_r06.md`](reports/remediation_r06.md) |
| **R05** Orphan Akteur + vocab | `remediation_r05_connect_orphans.patch.jsonl` + `remediation_r05_fix_property.patch.jsonl` | 3 `add_rel`, 1 `remove_node_properties`, 8 `noop_reviewed` | +3 rels; `repurpose.land` dropped | [`reports/remediation_r05.md`](reports/remediation_r05.md) |
| **R02** Dangling Nachweisforderung | `remediation_r02_erfuellt_nachweis.patch.jsonl` | 10 `add_rel` `ERFUELLT_NACHWEIS` | +10 rels (7 NF types) | [`reports/remediation_r02.md`](reports/remediation_r02.md) |
| **R03** Deferred node duplicates | `remediation_r03_merge_nodes.patch.jsonl` | 11 `merge_node` | 2295→2284 / 15340→15312 | [`reports/remediation_r03.md`](reports/remediation_r03.md) |
| **R07** Rel source backlog (A14 subset) | `remediation_r07_add_rel_sources.patch.jsonl` | 137 `set_rel_properties` | — (property-only) | [`reports/remediation_r07.md`](reports/remediation_r07.md) |

Apply reports: [`apply_reports/`](apply_reports/).

---

## Pending / deferred (by batch)

| Batch | Remaining work |
|---|---|
| **R01** | **17** unsourced `Materialdepot` nodes → ESCALATE_HUMAN (placeholders / aggregates) |
| **R02** | **11** dangling `Nachweisforderung` (5 need new `PruefungNachweis`, 6 medium-confidence only) |
| **R03** | **17** deferred node-duplicate pairs (Paris STP, BIM triple, `rau`↔`rau_architects`, …) |
| **R04** | `rau`↔`rau_architects` firm merge; `rau`↔`thomas_rau` founder edge (ESCALATE_HUMAN) |
| **R05** | 3 vocab-stub **DEPRECATE** candidates; substantive actor mesh edges still need dual-endpoint sources |
| **R06** | — (63/63 scope fixed) |
| **R07** | **171** RESOURCE (PARTIAL — weak dossier/overlap proof); **6** MISSING_EVIDENCE (`new_horizon_urban_mining`, `tool_hts_stockmatcher`) |

---

## Suggested next steps

1. Human-gate remaining destructive batches (`delete_unsupported` already applied in wave 1; R03-deferred merges).
2. R07 residual RESOURCE / MISSING_EVIDENCE rows → dossier review or stronger project-level fetches.
3. R01 Materialdepot long tail + R02 dangling requirements.
4. Agent 14 hygiene re-run; re-baseline approved property-key ledger (`AGENTS.md` drift note).

See [`REMEDIATION_PLAN.md`](REMEDIATION_PLAN.md) §9 for ordered apply history.
