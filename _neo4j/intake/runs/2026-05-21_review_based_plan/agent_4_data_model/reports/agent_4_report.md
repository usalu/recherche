# Agent 4 - Phase R4 Report

- **Agent:** agent_4_data_model
- **Database:** mit-bestand
- **Branch:** wip/kinan2 working tree
- **Completed (UTC):** 2026-05-21T11:03:56.880356+00:00
- **Verdict:** PASS

## Executive summary

R4 lifts `reuse_share_facts`, `co2_facts`, and `cost_facts` from JSON-string arrays on `:Projekt` into first-class `:Kennwert` nodes. The JSON mirrors remain untouched; `quality_tier_facts` remains untouched by design. `:HAT_KENNWERT` edges carry the canonical R1 evidence fields.

## Before / after counts

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Total nodes | 3849 | 4107 | 258 |
| Total relationships | 25107 | 25365 | 258 |
| Kennwert total | 0 | 258 | 258 |
| HAT_KENNWERT total | 0 | 258 | 258 |
| reuse_share Kennwert | 0 | 39 | 39 |
| co2_saving Kennwert | 0 | 46 | 46 |
| cost Kennwert | 0 | 173 | 173 |
| quality_tier_facts present | 101 | 101 | 0 |

## Acceptance gates

| Gate | Expected | Live | Verdict |
|---|---|---|---|
| kennwert_total | >= 12 | {"c": 258} | PASS |
| reuse_share_count | >= 4 | {"c": 39} | PASS |
| co2_saving_count | >= 5 | {"c": 46} | PASS |
| cost_count | >= 5 | {"c": 173} | PASS |
| kennwert_orphan | 0 | {"violations": 0} | PASS |
| reuse_share_count_mismatch | 0 | {"violations": 0} | PASS |
| co2_count_mismatch | 0 | {"violations": 0} | PASS |
| cost_count_mismatch | 0 | {"violations": 0} | PASS |
| hat_kennwert_origin_enum | 0 | {"violations": 0} | PASS |
| q3_tier1_reuse_projects | >= 3 | {"c": 3} | PASS |
| holbein_steel_34 | hits >= 1 and wert = 34 | {"hits": 1, "wert": 34.0} | PASS |
| jeugdkliniek_range | hits >= 1 and range 30..40 | {"hits": 1, "wert_min": 30.0, "wert_max": 40.0} | PASS |
| quality_tier_facts_untouched | > 0 | {"c": 101} | PASS |

## Issues raised

- Dependency status: `{"phase": "R4", "r1_done": true, "can_run": true, "missing": []}`.
- Parse errors: `0`.
- D4 resolved YES: `:Kennwert.category` is written.
- D5 resolved NO: `quality_tier_facts` was not lifted.
- JSON-string source properties were not stripped; that remains orchestrator-gated after Stage 4.

## Metrics

```json
{
  "kennwert_by_category": [
    {
      "category": "co2_saving",
      "c": 46
    },
    {
      "category": "cost",
      "c": 173
    },
    {
      "category": "reuse_share",
      "c": 39
    }
  ],
  "tier1_kennwerte": [
    {
      "projekt_id": "p_biopartner_5_leiden_oegstgeest",
      "category": "co2_saving",
      "kennwert": "co2_reduktion_prozent",
      "wert": 40.0,
      "wert_text": "40",
      "wert_min": null,
      "wert_max": null,
      "einheit": "%",
      "source_id": null
    },
    {
      "projekt_id": "p_biopartner_5_leiden_oegstgeest",
      "category": "co2_saving",
      "kennwert": "CO\u2082-Reduktion",
      "wert": 40.0,
      "wert_text": "ca. 40",
      "wert_min": null,
      "wert_max": null,
      "einheit": "%",
      "source_id": "q_biopartner_5_leiden_oegstgeest_s2"
    },
    {
      "projekt_id": "p_biopartner_5_leiden_oegstgeest",
      "category": "cost",
      "kennwert": "Kosten",
      "wert": null,
      "wert_text": "unbekannt",
      "wert_min": null,
      "wert_max": null,
      "einheit": "\u2014",
      "source_id": "q_biopartner_5_leiden_oegstgeest_md"
    },
    {
      "projekt_id": "p_chiro_d_itterbeek_dilbeek",
      "category": "co2_saving",
      "kennwert": "vermiedenes CO\u2082",
      "wert": 4572.0,
      "wert_text": "4.572,702786",
      "wert_min": null,
      "wert_max": null,
      "einheit": "kg CO\u2082",
      "source_id": "q_chiro_d_itterbeek_dilbeek_s2"
    },
    {
      "projekt_id": "p_chiro_d_itterbeek_dilbeek",
      "category": "cost",
      "kennwert": "kosten_eur",
      "wert": 55000.0,
      "wert_text": "55000",
      "wert_min": null,
      "wert_max": null,
      "einheit": "EUR",
      "source_id": null
    },
    {
      "projekt_id": "p_chiro_d_itterbeek_dilbeek",
      "category": "cost",
      "kennwert": "Kosten Bau/Renovierung",
      "wert": 55000.0,
      "wert_text": "55.000",
      "wert_min": null,
      "wert_max": null,
      "einheit": "\u20ac",
      "source_id": "q_chiro_d_itterbeek_dilbeek_s2"
    },
    {
      "projekt_id": "p_chiro_d_itterbeek_dilbeek",
      "category": "cost",
      "kennwert": "Kosten/m\u00b2",
      "wert": 3666.0,
      "wert_text": "3.666,67",
      "wert_min": null,
      "wert_max": null,
      "einheit": "\u20ac/m\u00b2",
      "source_id": "q_chiro_d_itterbeek_dilbeek_s2"
    },
    {
      "projekt_id": "p_ferme_du_rail_paris",
      "category": "cost",
      "kennwert": "Baukosten",
      "wert": 3.3,
      "wert_text": "3,3",
      "wert_min": null,
      "wert_max": null,
      "einheit": "Mio. \u20ac HT",
      "source_id": "q_ferme_du_rail_paris_s2"
    },
    {
      "projekt_id": "p_ferme_du_rail_paris",
      "category": "cost",
      "kennwert": "CO\u2082-Einsparung",
      "wert": null,
      "wert_text": "unbekannt",
      "wert_min": null,
      "wert_max": null,
      "einheit": "\u2014",
      "source_id": "q_ferme_du_rail_paris_md"
    },
    {
      "projekt_id": "p_ferme_du_rail_paris",
      "category": "cost",
      "kennwert": "Kostenwirkung Reuse",
      "wert": null,
      "wert_text": "ohne Mehrkosten insgesamt behauptet",
      "wert_min": null,
      "wert_max": null,
      "einheit": "\u2014",
      "source_id": "q_ferme_du_rail_paris_s2"
    },
    {
      "projekt_id": "p_ferme_du_rail_paris",
      "category": "reuse_share",
      "kennwert": "Anteil biosourc\u00e9 und/oder r\u00e9employ\u00e9",
      "wert": 90.0,
      "wert_text": "90",
      "wert_min": null,
      "wert_max": null,
      "einheit": "%",
      "source_id": "q_ferme_du_rail_paris_s2"
    },
    {
      "projekt_id": "p_grande_halle_de_colombelles",
      "category": "co2_saving",
      "kennwert": "abfall_vermieden_t",
      "wert": 19.0,
      "wert_text": "19",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t",
      "source_id": null
    },
    {
      "projekt_id": "p_grande_halle_de_colombelles",
      "category": "cost",
      "kennwert": "baukosten_eur",
      "wert": 5800000.0,
      "wert_text": "5800000",
      "wert_min": null,
      "wert_max": null,
      "einheit": "EUR",
      "source_id": null
    },
    {
      "projekt_id": "p_grande_halle_de_colombelles",
      "category": "cost",
      "kennwert": "Baukosten",
      "wert": 5.8,
      "wert_text": "5,8",
      "wert_min": null,
      "wert_max": null,
      "einheit": "Mio. \u20ac",
      "source_id": "q_grande_halle_de_colombelles_s3"
    },
    {
      "projekt_id": "p_grande_halle_de_colombelles",
      "category": "cost",
      "kennwert": "Baukosten alternative",
      "wert": 5.5,
      "wert_text": "5,5",
      "wert_min": null,
      "wert_max": null,
      "einheit": "Mio. \u20ac HT",
      "source_id": "q_grande_halle_de_colombelles_s6"
    },
    {
      "projekt_id": "p_grande_halle_de_colombelles",
      "category": "cost",
      "kennwert": "Studienkosten",
      "wert": 320000.0,
      "wert_text": "320.000",
      "wert_min": null,
      "wert_max": null,
      "einheit": "\u20ac",
      "source_id": "q_grande_halle_de_colombelles_s3"
    },
    {
      "projekt_id": "p_grande_halle_de_colombelles",
      "category": "cost",
      "kennwert": "CO\u2082-Einsparung",
      "wert": null,
      "wert_text": "unbekannt",
      "wert_min": null,
      "wert_max": null,
      "einheit": "\u2014",
      "source_id": "q_grande_halle_de_colombelles_s2"
    },
    {
      "projekt_id": "p_haus_hos_mehrfamilienhaus_muehlhausen",
      "category": "co2_saving",
      "kennwert": "transportdistanz_km",
      "wert": 30.0,
      "wert_text": "30",
      "wert_min": null,
      "wert_max": null,
      "einheit": "km",
      "source_id": null
    },
    {
      "projekt_id": "p_haus_hos_mehrfamilienhaus_muehlhausen",
      "category": "cost",
      "kennwert": "Herstellungskosten",
      "wert": 300000.0,
      "wert_text": "ca. 300.000",
      "wert_min": null,
      "wert_max": null,
      "einheit": "EUR",
      "source_id": "q_haus_hos_mehrfamilienhaus_muehlhausen_s7"
    },
    {
      "projekt_id": "p_haus_hos_mehrfamilienhaus_muehlhausen",
      "category": "cost",
      "kennwert": "Kosteneinsparung",
      "wert": 25.0,
      "wert_text": "ca. 25",
      "wert_min": null,
      "wert_max": null,
      "einheit": "%",
      "source_id": "q_haus_hos_mehrfamilienhaus_muehlhausen_s7"
    },
    {
      "projekt_id": "p_haus_hos_mehrfamilienhaus_muehlhausen",
      "category": "cost",
      "kennwert": "CO\u2082-Einsparung",
      "wert": null,
      "wert_text": "unbekannt",
      "wert_min": null,
      "wert_max": null,
      "einheit": "kg CO\u2082e",
      "source_id": "q_haus_hos_mehrfamilienhaus_muehlhausen_md"
    },
    {
      "projekt_id": "p_holbein_gardens_london",
      "category": "cost",
      "kennwert": "CO\u2082-Einsparung Stahlreuse",
      "wert": 35.0,
      "wert_text": "35",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t CO\u2082e",
      "source_id": "q_holbein_gardens_london_s3"
    },
    {
      "projekt_id": "p_holbein_gardens_london",
      "category": "cost",
      "kennwert": "CO\u2082-Einsparung Stahlreuse",
      "wert": 45.0,
      "wert_text": "45",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t CO\u2082e",
      "source_id": "q_holbein_gardens_london_s2"
    },
    {
      "projekt_id": "p_holbein_gardens_london",
      "category": "cost",
      "kennwert": "CO\u2082-Einsparung Stahlreuse",
      "wert": 60.0,
      "wert_text": "60",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t CO\u2082e",
      "source_id": "q_holbein_gardens_london_s1"
    },
    {
      "projekt_id": "p_holbein_gardens_london",
      "category": "cost",
      "kennwert": "operational carbon savings",
      "wert": 69.0,
      "wert_text": "69",
      "wert_min": null,
      "wert_max": null,
      "einheit": "%",
      "source_id": "q_holbein_gardens_london_s7"
    },
    {
      "projekt_id": "p_holbein_gardens_london",
      "category": "cost",
      "kennwert": "Kosten",
      "wert": null,
      "wert_text": "unbekannt",
      "wert_min": null,
      "wert_max": null,
      "einheit": "GBP",
      "source_id": "q_holbein_gardens_london_md"
    },
    {
      "projekt_id": "p_holbein_gardens_london",
      "category": "reuse_share",
      "kennwert": "Anteil reused steel an Stahltonnage",
      "wert": 34.0,
      "wert_text": "34 / ca. ein Drittel",
      "wert_min": null,
      "wert_max": null,
      "einheit": "%",
      "source_id": "q_holbein_gardens_london_s9"
    },
    {
      "projekt_id": "p_jeugdkliniek_ithaka_emergis_kloetinge",
      "category": "cost",
      "kennwert": "CO\u2082-Einsparung",
      "wert": null,
      "wert_text": "unbekannt",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t CO\u2082e",
      "source_id": "q_jeugdkliniek_ithaka_emergis_kloetinge_md"
    },
    {
      "projekt_id": "p_jeugdkliniek_ithaka_emergis_kloetinge",
      "category": "cost",
      "kennwert": "Kosten",
      "wert": null,
      "wert_text": "unbekannt",
      "wert_min": null,
      "wert_max": null,
      "einheit": "EUR",
      "source_id": "q_jeugdkliniek_ithaka_emergis_kloetinge_md"
    },
    {
      "projekt_id": "p_jeugdkliniek_ithaka_emergis_kloetinge",
      "category": "reuse_share",
      "kennwert": "Materialanteil aus RWS",
      "wert": null,
      "wert_text": "30\u201340",
      "wert_min": 30.0,
      "wert_max": 40.0,
      "einheit": "%",
      "source_id": "q_jeugdkliniek_ithaka_emergis_kloetinge_s6"
    },
    {
      "projekt_id": "p_jeugdkliniek_ithaka_emergis_kloetinge",
      "category": "reuse_share",
      "kennwert": "Ziel Reuse-Anteil Neubau",
      "wert": 50.0,
      "wert_text": "50",
      "wert_min": null,
      "wert_max": null,
      "einheit": "%",
      "source_id": "q_jeugdkliniek_ithaka_emergis_kloetinge_s13"
    },
    {
      "projekt_id": "p_k118_kopfbau_halle_118_winterthur",
      "category": "co2_saving",
      "kennwert": "co2_einsparung_t",
      "wert": 494.0,
      "wert_text": "494",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t",
      "source_id": null
    },
    {
      "projekt_id": "p_k118_kopfbau_halle_118_winterthur",
      "category": "co2_saving",
      "kennwert": "co2_reduktion_prozent",
      "wert": 59.0,
      "wert_text": "59",
      "wert_min": null,
      "wert_max": null,
      "einheit": "%",
      "source_id": null
    },
    {
      "projekt_id": "p_k118_kopfbau_halle_118_winterthur",
      "category": "co2_saving",
      "kennwert": "co2_einsparung_t_min",
      "wert": 500.0,
      "wert_text": "500",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t",
      "source_id": null
    },
    {
      "projekt_id": "p_k118_kopfbau_halle_118_winterthur",
      "category": "co2_saving",
      "kennwert": "co2_einsparung_t_max",
      "wert": 500.0,
      "wert_text": "500",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t",
      "source_id": null
    },
    {
      "projekt_id": "p_k118_kopfbau_halle_118_winterthur",
      "category": "co2_saving",
      "kennwert": "CO\u2082-Reduktion",
      "wert": 59.0,
      "wert_text": "59",
      "wert_min": null,
      "wert_max": null,
      "einheit": "%",
      "source_id": "q_k118_kopfbau_halle_118_winterthur_s3"
    },
    {
      "projekt_id": "p_k118_kopfbau_halle_118_winterthur",
      "category": "co2_saving",
      "kennwert": "CO\u2082-Reduktion absolut",
      "wert": 494.0,
      "wert_text": "494",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t CO\u2082",
      "source_id": "q_k118_kopfbau_halle_118_winterthur_s3"
    },
    {
      "projekt_id": "p_k118_kopfbau_halle_118_winterthur",
      "category": "co2_saving",
      "kennwert": "CO\u2082-Beitrag Stahlreuse",
      "wert": 80.0,
      "wert_text": "ca. 80",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t CO\u2082 / 16 %",
      "source_id": "q_k118_kopfbau_halle_118_winterthur_s3"
    },
    {
      "projekt_id": "p_k118_kopfbau_halle_118_winterthur",
      "category": "cost",
      "kennwert": "Kostenwirkung",
      "wert": null,
      "wert_text": "vergleichbar mit \u00e4hnlichem Neubau",
      "wert_min": null,
      "wert_max": null,
      "einheit": "qualitativ",
      "source_id": "q_k118_kopfbau_halle_118_winterthur_s3"
    },
    {
      "projekt_id": "p_lycee_michel_lucius_conversion_luxembourg",
      "category": "co2_saving",
      "kennwert": "co2_einsparung_t_min",
      "wert": 458.0,
      "wert_text": "458",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t",
      "source_id": null
    },
    {
      "projekt_id": "p_lycee_michel_lucius_conversion_luxembourg",
      "category": "co2_saving",
      "kennwert": "co2_einsparung_t_max",
      "wert": 792.0,
      "wert_text": "792",
      "wert_min": null,
      "wert_max": null,
      "einheit": "t",
      "source_id": null
    },
    {
      "projekt_id": "p_lycee_michel_lucius_conversion_luxembourg",
      "category": "cost",
      "kennwert": "baukosten_eur",
      "wert": 6500000.0,
      "wert_text": "6500000",
      "wert_min": null,
      "wert_max": null,
      "einheit": "EUR",
      "source_id": null
    },
    {
      "projekt_id": "p_lycee_michel_lucius_conversion_luxembourg",
      "category": "cost",
      "kennwert": "Kosten",
      "wert": 6500.0,
      "wert_text": "6.500.000",
      "wert_min": null,
      "wert_max": null,
      "einheit": "EUR ohne MwSt",
      "source_id": "q_lycee_michel_lucius_conversion_luxembourg_s2"
    },
    {
      "projekt_id": "p_lycee_michel_lucius_conversion_luxembourg",
      "category": "cost",
      "kennwert": "CO\u2082-Einsparung",
      "wert": null,
      "wert_text": "458\u2013792",
      "wert_min": 458.0,
      "wert_max": 792.0,
      "einheit": "t CO\u2082e",
      "source_id": "q_lycee_michel_lucius_conversion_luxembourg_s6"
    },
    {
      "projekt_id": "p_maison_vignette_auderghem",
      "category": "cost",
      "kennwert": "CO\u2082-Einsparung",
      "wert": null,
      "wert_text": "unbekannt",
      "wert_min": null,
      "wert_max": null,
      "einheit": "kg CO\u2082e",
      "source_id": "q_maison_vignette_auderghem_md"
    },
    {
      "projekt_id": "p_maison_vignette_auderghem",
      "category": "cost",
      "kennwert": "Kosten",
      "wert": null,
      "wert_text": "unbekannt",
      "wert_min": null,
      "wert_max": null,
      "einheit": "\u20ac",
      "source_id": "q_maison_vignette_auderghem_md"
    },
    {
      "projekt_id": "p_trae_high_rise_aarhus",
      "category": "co2_saving",
      "kennwert": "a:gain CO\u2082-Footprint",
      "wert": 130096.0,
      "wert_text": "130.096",
      "wert_min": null,
      "wert_max": null,
      "einheit": "kg CO\u2082e",
      "source_id": "q_trae_high_rise_aarhus_s10"
    }
  ],
  "hat_kennwert_origin_distribution": [
    {
      "origin": "source_curated",
      "confidence": "belegt",
      "c": 48
    },
    {
      "origin": "source_curated",
      "confidence": "teilweise_belegt",
      "c": 50
    },
    {
      "origin": "source_curated",
      "confidence": "unklar",
      "c": 118
    },
    {
      "origin": "topology_synthesized",
      "confidence": "unklar",
      "c": 42
    }
  ]
}
```

## Parse Errors

```json
[]
```

## Artefacts

```
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/logs/agent_4_audit.jsonl
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/logs/agent_4_audit_summary.json
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/logs/agent_4_gates.json
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/logs/agent_4_metrics.json
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/logs/agent_4_normalized_rows.json
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/logs/agent_4_parse_errors.json
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/logs/agent_4_probe_post.json
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/logs/agent_4_probe_pre.json
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/logs/agent_4_progress.log
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/logs/agent_4_runner.py
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/migrations/mig_r4_kennwert_lift.cypher
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/PHASE_R4_DONE.flag
_neo4j/intake/runs/2026-05-21_review_based_plan/agent_4_data_model/reports/agent_4_report.md
```

## Handoff

Agent 5 R7.c can use this schema after `PHASE_R4_DONE.flag` is present. The runner is idempotent; rerunning R4 rewrites the same deterministic `kw_<projekt>_<category>_<i>` nodes and `:HAT_KENNWERT` edges.
