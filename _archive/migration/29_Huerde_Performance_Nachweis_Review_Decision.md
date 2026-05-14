# Phase 29 Huerde Performance Nachweis Review Decision

## Decision

Keep huerde/Performance_Nachweis out of the clean database.

Reason: the label mixes three levels: a barrier, a proof/check, and a performance requirement. Clean import needs concrete targets.

## Database Change

No database nodes or clean edges were added. Existing concrete hurdle edges remain the clean representation where already present.

## Counts

- Held huerde/Performance_Nachweis edges reviewed: 33

| decision | rows |
|---|---:|
| covered_by_existing_concrete_huerden | 25 |
| candidate_precise_huerde | 4 |
| candidate_review_split | 2 |
| keep_review_split_needed | 1 |
| candidate_non_huerde_requirement | 1 |

## Sample Rows

| raw label | existing clean hurdle edges | decision | suggested target |
|---|---|---|---|
| Energieanforderungen |  | candidate_non_huerde_requirement | leistungsanforderung/Waermeschutz |
| Eignung als Baufolie |  | candidate_precise_huerde | huerde/Technische_Freigabe |
| Eignung als Boden |  | candidate_precise_huerde | huerde/Technische_Freigabe |
| nötig zur Begrenzung von Tests/Stabilitätsaufwand |  | candidate_precise_huerde | huerde/Technische_Freigabe |
| unbekannte Werte |  | candidate_precise_huerde | huerde/Technische_Freigabe |
| Dichtheit, Befestigung |  | candidate_review_split | huerde/Dauerhaftigkeit_Restlebensdauer |
| Korrosion, Dichtheit |  | candidate_review_split | huerde/Dauerhaftigkeit_Restlebensdauer |
| Akzeptanz Installateur, Gewährleistung | huerde/Akzeptanzproblem; huerde/Gewaehrleistung | covered_by_existing_concrete_huerden |  |
| Alter, Leistung, Dichtheit | huerde/Zustand_Unklar | covered_by_existing_concrete_huerden |  |
| Aufbereitung, Gewährleistung | huerde/Aufbereitungsaufwand; huerde/Gewaehrleistung | covered_by_existing_concrete_huerden |  |
| Brandschutz/Energieanforderungen komplizierter als Sanitär | huerde/Brandschutzkonflikt | covered_by_existing_concrete_huerden |  |
| experimentelle Eignung | huerde/Unkonventionelles_Material | covered_by_existing_concrete_huerden |  |

## Output

- _migration/29_huerde_performance_nachweis_edge_review_decisions.csv
