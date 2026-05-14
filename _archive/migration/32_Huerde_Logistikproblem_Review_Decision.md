# Phase 32 Huerde Logistikproblem Review Decision

## Decision

Keep huerde/Logistikproblem out of the clean database.

Reason: Logistikproblem is too broad. The clean graph needs the concrete barrier behind the logistics issue.

## Database Change

No database nodes or clean edges were added. Existing concrete hurdle edges remain the clean representation where already present.

## Counts

- Held huerde/Logistikproblem edges reviewed: 20

| decision | rows |
|---|---:|
| covered_by_existing_concrete_huerden | 9 |
| candidate_review_split | 7 |
| keep_review_logistics_too_broad | 3 |
| candidate_precise_huerde | 1 |

## Sample Rows

| raw label | existing clean hurdle edges | decision | suggested target |
|---|---|---|---|
| Programm-/Lieferkettenprobleme bei reclaimed doors |  | candidate_precise_huerde | huerde/Verfuegbarkeitsproblem |
| Fügung/Transport |  | candidate_review_split | huerde/Kompatibilitaetsproblem or huerde/Anschlussproblem |
| Gewicht, Transport, Plattenzustand |  | candidate_review_split | huerde/Kompatibilitaetsproblem or huerde/Toleranzen |
| heavy lifting / transport |  | candidate_review_split | huerde/Kompatibilitaetsproblem or huerde/Toleranzen |
| Logistik / Gewicht |  | candidate_review_split | huerde/Kompatibilitaetsproblem or huerde/Toleranzen |
| Logistik Gewicht |  | candidate_review_split | huerde/Kompatibilitaetsproblem or huerde/Toleranzen |
| Transport/Gewicht |  | candidate_review_split | huerde/Kompatibilitaetsproblem or huerde/Toleranzen |
| Transportgewicht |  | candidate_review_split | huerde/Kompatibilitaetsproblem or huerde/Toleranzen |
| Bruch/Transport | huerde/Bruch_Beschaedigungsrisiko | covered_by_existing_concrete_huerden |  |
| Demontage, Tests, Transport, Kosten | huerde/Anschlussproblem | covered_by_existing_concrete_huerden |  |
| Integration in Montagefolge/Logistik | huerde/Anschlussproblem | covered_by_existing_concrete_huerden |  |
| Logistik/Lagerung | huerde/Fehlende_Lagerflaeche | covered_by_existing_concrete_huerden |  |

## Output

- _migration/32_huerde_logistikproblem_edge_review_decisions.csv
