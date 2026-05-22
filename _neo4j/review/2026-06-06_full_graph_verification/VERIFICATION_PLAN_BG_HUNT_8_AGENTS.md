# BG Hunt — 8-Agent Verification Plan

**Date:** 2026-06-07 · **Database:** `mit-bestand` · **Baseline ledger:** `VERIFICATION_LEDGER_ELEMENT_v6.csv`

**Plans:** [`BAUTEILGRUPPE_EVIDENCE_HUNTING_PLAN.md`](BAUTEILGRUPPE_EVIDENCE_HUNTING_PLAN.md), [`BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md`](BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md)

**Orchestrator:** `_bg_hunt_orchestrate.py`

```powershell
cd e:\recherche\_neo4j\review\2026-06-06_full_graph_verification
python _bg_hunt_orchestrate.py
```

## Fleet

| Agent | Role | Scope | Batch | Ledger | Report |
|---|---|---|---:|---|---|
| **BG-00** | Tooling | `bg_slug_decompose.py`, `alias_tables.json`, `quote_scorer.py`, `scope_*.json` | — | — | `reports/bg_hunt_00_report.md` |
| **BG-01** | H1 catalogue A | `HAT_BAUTEILTYP`, `NUTZT_MATERIAL` ∧ bg_ ; v6 UNSUPPORTED | ~200 | `ledger/bg_hunt_01.csv` | `reports/bg_hunt_01_report.md` |
| **BG-02** | H1 catalogue B | same, offset 200 | ~200 | `ledger/bg_hunt_02.csv` | `reports/bg_hunt_02_report.md` |
| **BG-03** | H2 process | `HAT_PROZESSPHASE`, `HAT_BESCHAFFUNGSWEG`, `HAT_LOGISTIK` | ~150 | `ledger/bg_hunt_03.csv` | `reports/bg_hunt_03_report.md` |
| **BG-04** | H3 regulation | `ERFORDERT_NACHWEIS`, `TRIGGERS_REGULIERUNGSFRAGE` | ~150 | `ledger/bg_hunt_04.csv` | `reports/bg_hunt_04_report.md` |
| **BG-05** | H4 spatial | `AUS_SPENDER`, `IN_EMPFANGSOBJEKT`, inbound `HAT_BAUTEILGRUPPE` | all UNSUPPORTED | `ledger/bg_hunt_05.csv` | `reports/bg_hunt_05_report.md` |
| **BG-06** | H5 material | `HAT_MATERIALGRUPPE`, `HAT_RUECKBAUVERFAHREN`, `HAT_AUFBEREITUNG` | all UNSUPPORTED | `ledger/bg_hunt_06.csv` | `reports/bg_hunt_06_report.md` |
| **BG-07** | Aggregator | merge 01–06 → patches + v7 | — | `ledger/bg_hunt_merged.csv` | `reports/BG_HUNT_CAMPAIGN_REPORT.md` |

## Hunting protocol

1. **Multi-wording:** decompose `bg_*` slug; DE/FR/NL/EN alias queries — not literal slug search.
2. **PROVEN gate:** project/listing anchor AND component family in verbatim quote; score per hunting plan §2.4.
3. `evidence_basis` = `bg_hunt_alias_match` on upgrades.
4. **NO auto-delete** on bg_ edges.
5. **NO category co-listing** false PROVEN.
6. Cache fetches per project URL across edges.

## Apply policy

- BG-07 emits `patches/bg_hunt_upgrades.patch.jsonl` (upgrade only).
- Dry-run: `python _scripts/apply_neo4j_review_patch.py --patch patches/bg_hunt_upgrades.patch.jsonl --database mit-bestand`
- **Do NOT** `--confirm` apply unless dry-run 100% clean and human sign-off.

## Outputs

| Artifact | Path |
|---|---|
| Tooling | `_bg_hunt_work/` |
| Merged ledger | `ledger/bg_hunt_merged.csv` |
| v7 overlay | `VERIFICATION_LEDGER_ELEMENT_v7.csv` |
| Patches | `patches/bg_hunt_upgrades.patch.jsonl` |
| Campaign report | `reports/BG_HUNT_CAMPAIGN_REPORT.md` |

## v6 baseline (bg_ rels)

| Metric | Value |
|---|---:|
| bg_ rel rows | 6,684 |
| UNSUPPORTED | 852 |
| PROVEN | 5,768 |

Note: all 852 v6 UNSUPPORTED are catalogue edges (`HAT_BAUTEILTYP` / `NUTZT_MATERIAL`); missions H2–H5 have 0 UNSUPPORTED in v6.
