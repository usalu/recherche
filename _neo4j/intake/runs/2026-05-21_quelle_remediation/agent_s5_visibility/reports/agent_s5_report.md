# Agent S5 visibility report

Completed UTC: 2026-05-22T07:32:50.559880+00:00
Database: mit-bestand
Verified: True

## Summary

| Label   | Total | With sources | Avg source count | Avg trust score | Trust=NULL |
|---------|------:|-------------:|-----------------:|----------------:|-----------:|
| Projekt | 101 | 91 | 8.01 | 0.0127 | 10 |
| Bauwerk | 186 | 186 | 9.92 | 0.0086 | 0 |
| Akteur  | 648 | 511 | 7.13 | 0.0072 | 137 |

Excessive-sources DataIssues: 2

## Acceptance gates
  [PASS] Every :Projekt has source_urls: 0
  [PASS] Every :Projekt has source_quality_summary: 0
  [PASS] Every :Projekt has source_freshness_summary: 0
  [PASS] Every :Bauwerk has source_urls: 0
  [PASS] Every :Akteur has source_urls: 0

## Spot-checks
  Stuttgart 210: source_count=0, trust_score=None
  Holbein Gardens: source_count=16, trust_score=0.0306

## Top 10 Projekt by trust score
  1. p_resilience_la_ferme_des_possibles_stains  ts=0.171
  2. p_chiro_d_itterbeek_dilbeek  ts=0.109
  3. p_grande_halle_de_colombelles  ts=0.0885
  4. p_brighton_waste_house_brighton  ts=0.0607
  5. p_zinneke_feder_masui4ever_brussels  ts=0.0543
  6. p_svanen_kindergarten_gladsaxe  ts=0.049
  7. p_haus_hos_mehrfamilienhaus_muehlhausen  ts=0.0479
  8. p_melkinlaituri_primary_school_daycare_centre_helsinki  ts=0.0417
  9. p_recrete_footbridge_reused_concrete_blocks  ts=0.0417
  10. p_k118_kopfbau_halle_118_winterthur  ts=0.0398

## Bottom 10 Projekt by trust score
  1. p_association_house_groeditz  ts=0.0
  2. p_association_house_plauen  ts=0.0
  3. p_bedzed_london_hackbridge  ts=0.0
  4. p_jugendtreff_ingersheim  ts=0.0
  5. p_eggshell_pavilion  ts=0.0
  6. p_up_sticks_dundee  ts=0.0
  7. p_reallabor_be_ware  ts=0.0
  8. p_interreg_nwe_fcrbe  ts=0.0
  9. p_rcmi_concular  ts=0.0
  10. p_55_great_suffolk_street_london  ts=0.0

## Logs
- E:\recherche\_neo4j\intake\runs\2026-05-21_quelle_remediation\agent_s5_visibility\logs\s5_audit.jsonl
- E:\recherche\_neo4j\intake\runs\2026-05-21_quelle_remediation\agent_s5_visibility\reports\S5_REPORT.json
