# Edge quality trace — automated run
- Edges file: `_database/_edges/clean_confirmed_edges.csv`
- Sample size: **18** rows

## Per-row checks

| # | relation | source_exists | target_exists | raw_in_source | note |
|---:|---|:---:|:---:|:---:|---|
| 1 | `belongs_to_fallstudie` | Y | Y | Y | substring_match; GEHÖRT_ZU {'csv_relation': 'belongs_to_fallstudie', 'rolle': 'fallbeispiel'}; field=`fallstudie` |
| 2 | `belongs_to_fallstudie` | Y | Y | Y | substring_match; GEHÖRT_ZU {'csv_relation': 'belongs_to_fallstudie', 'rolle': 'fallbeispiel'}; field=`fallstudie` |
| 3 | `installed_in_bauobjekt` | Y | Y | Y | substring_match; GEHÖRT_ZU {'csv_relation': 'installed_in_bauobjekt', 'rolle': 'einbauort'}; field=`bauobjekt` |
| 4 | `installed_in_bauobjekt` | Y | Y | Y | substring_match; GEHÖRT_ZU {'csv_relation': 'installed_in_bauobjekt', 'rolle': 'einbauort'}; field=`bauobjekt` |
| 5 | `has_huerde` | Y | Y | Y | substring_match; HAT {'csv_relation': 'has_huerde', 'art': 'huerde'}; field=`huerde_label` |
| 6 | `has_huerde` | Y | Y | Y | substring_match; HAT {'csv_relation': 'has_huerde', 'art': 'huerde'}; field=`huerde_label` |
| 7 | `has_rechtliche_bedingung` | Y | Y | Y | substring_match; HAT {'csv_relation': 'has_rechtliche_bedingung', 'art': 'recht'}; field=`FRONTMATTER:pruefung_label` |
| 8 | `has_rechtliche_bedingung` | Y | Y | Y | substring_match; HAT {'csv_relation': 'has_rechtliche_bedingung', 'art': 'recht'}; field=`BAUTEIL-INVENTAR:Eingriff/Aufbereitung` |
| 9 | `has_logistik` | Y | Y | Y | substring_match; HAT {'csv_relation': 'has_logistik', 'art': 'logistik'}; field=`FRONTMATTER:huerde_label` |
| 10 | `has_logistik` | Y | Y | Y | substring_match; HAT {'csv_relation': 'has_logistik', 'art': 'logistik'}; field=`BAUTEIL-INVENTAR:Eingriff/Aufbereitung` |
| 11 | `measured_on_bauobjekt` | Y | Y | Y | substring_match; Neo4j_SKIP(intended); field=`bauobjekt` |
| 12 | `measured_on_bauobjekt` | Y | Y | Y | substring_match; Neo4j_SKIP(intended); field=`bauobjekt` |
| 13 | `measures_kennwertdefinition` | Y | Y | Y | substring_match; Neo4j_SKIP(intended); field=`kennwert_label` |
| 14 | `measures_kennwertdefinition` | Y | Y | Y | substring_match; Neo4j_SKIP(intended); field=`kennwert_label` |
| 15 | `has_ressourcenquelle` | Y | Y | Y | substring_match; HAT {'csv_relation': 'has_ressourcenquelle', 'art': 'ressourcenquelle'}; field=`FRONTMATTER:herkunft_label` |
| 16 | `has_ressourcenquelle` | Y | Y | Y | substring_match; HAT {'csv_relation': 'has_ressourcenquelle', 'art': 'ressourcenquelle'}; field=`FRONTMATTER:herkunft_label` |
| 17 | `has_methode` | Y | Y | Y | substring_match; BENUTZT {'csv_relation': 'has_methode'}; field=`BAUTEIL-INVENTAR:Eingriff/Aufbereitung` |
| 18 | `has_methode` | Y | Y | Y | substring_match; BENUTZT {'csv_relation': 'has_methode'}; field=`BAUTEIL-INVENTAR:Eingriff/Aufbereitung` |

## Summary

- **Green count** (source `index.md` exists, target `index.md` exists, raw-label heuristic found in source body, Neo4j fold OK or intentional SKIP): **18 / 18**
- Rule of thumb from audit doc: **≥9/12** green → keep and extend; this run uses a slightly larger sample.
