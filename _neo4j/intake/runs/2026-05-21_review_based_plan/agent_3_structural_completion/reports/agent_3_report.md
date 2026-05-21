# Agent 3 - Phase R3 Report

- **Agent:** agent_3_structural_completion
- **Database:** mit-bestand
- **Branch:** wip/kinan2 working tree
- **Completed (UTC):** 2026-05-21T10:56:43.565607+00:00
- **Verdict:** BLOCKED

## Executive summary

Agent 3 artefacts for R3/R9 are present under this run directory. R3 creates direct `:Projekt-[:HAS_BAUWERK]->:Bauwerk` edges from Bauteilgruppe topology and `:ReuseRule-[:RELEVANT_FOR]->:Projekt` edges from country/material topology. R9 renames `:ASSOZIIERT_MIT_PROJEKT` to `:STUB_PROJECT_LINK`, but is gated behind R3 completion.

## Before / after counts

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Total relationships | 25107 | 25107 | 0 |
| HAS_BAUWERK total | 0 | 0 | 0 |
| HAS_BAUWERK donor | 0 | 0 | 0 |
| HAS_BAUWERK receiver | 0 | 0 | 0 |
| RELEVANT_FOR | 0 | 0 | 0 |
| ASSOZIIERT_MIT_PROJEKT | 200 | 200 | 0 |
| STUB_PROJECT_LINK | 0 | 0 | 0 |

## Acceptance gates

| Gate | Expected | Live | Verdict |
|---|---|---|---|
| _not run_ | _dependency gate_ | _not run_ | BLOCKED |

## Issues raised

- Dependency status: `{"phase": "R3", "r1_done": true, "r7_done": false, "r7_ab_done": false, "r3_done": false, "can_run": false, "missing": ["agent_5_loader_hardening/PHASE_R7_DONE.flag or PHASE_R7_AB_DONE.flag"]}`.
- D3 is deferred: no `:Bauteilgruppe-[:DERIVED_FROM]->:Bauteilgruppe` edge added in this phase.

## Distribution snippets

```json
{
  "has_bauwerk_top20": [],
  "relevant_for_per_rule": [
    {
      "rule_id": "rr_be_beton",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_be_holz",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_be_naturstein",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_be_stahl",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_ch_beton",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_ch_holz",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_ch_naturstein",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_ch_stahl",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_de_beton",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_de_holz",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_de_lehm",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_de_stahl",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_de_ziegel",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_fi_beton_hollow_core_slabs",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_gb_holz",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_gb_stahl",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_nl_beton",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_nl_holz",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_nl_stahl",
      "projekt_count": 0
    },
    {
      "rule_id": "rr_no_beton_hollow_core_slabs",
      "projekt_count": 0
    }
  ]
}
```

## Artefacts

```
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_3_structural_completion/logs/agent_3_probe_pre.json
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_3_structural_completion/logs/agent_3_progress.log
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_3_structural_completion/logs/agent_3_runner.py
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_3_structural_completion/migrations/mig_r3_a_has_bauwerk.cypher
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_3_structural_completion/migrations/mig_r3_b_reuse_rule_relevant_for.cypher
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_3_structural_completion/migrations/mig_r9_stub_project_link_rename.cypher
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_3_structural_completion/reports/agent_3_report.md
```

## Handoff

Run `python _neo4j/intake/runs/2026-05-21_review_based_plan/agent_3_structural_completion/logs/agent_3_runner.py r3` after Agent 5 has written `PHASE_R7_DONE.flag` or `PHASE_R7_AB_DONE.flag`. Run R9 only after R3 is integrated and `PHASE_R3_DONE.flag` exists.
