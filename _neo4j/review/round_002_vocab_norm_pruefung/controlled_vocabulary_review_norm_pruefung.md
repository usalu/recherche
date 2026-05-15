# Round 002 Controlled Vocabulary Review: Norm + PruefungNachweis + Leistungsanforderung

**Generated:** 2026-05-15
**Baseline reference:** [`../round_002_baseline/global_audit_report.md`](../round_002_baseline/global_audit_report.md)

## Result in Context

Three findings:

1. **`norm_sci_p427`** is already canonicalized in the live graph
   (name = "SCI P427 protocol", aliases = ["SCI P427 Structural Steel Reuse"]).
   The round-001 needs_review item carries forward as an idempotent record.
2. **`norm_crow_cur_4_2023`** (2 inbound) and
   **`norm_crow_cur_guideline_4_2023`** (1 inbound) are two ids for the same
   CROW-CUR Guideline 4:2023. Merge.
3. **`la_brandschutz`** (93 inbound) and **`la_brandschutzanforderung`**
   (1 inbound) are two Leistungsanforderung nodes for the same fire
   protection requirement. Merge into the canonical short form.

Plus 10 orphans (5 Norm, 2 PruefungNachweis, 3 Leistungsanforderung): all
domain-specialty terms kept as proposed seed for future precision.

## Norm hub snapshot (live `mit-bestand`)

| id | name | inbound | classification |
| --- | --- | ---: | --- |
| norm_tek_norway | Norwegian building regulation TEK / documentation context | 5 | canonical |
| norm_sci_p427 | SCI P427 protocol | 5 | canonical |
| norm_sia_schweiz | SIA / Swiss building standards context | 4 | canonical |
| norm_crow_cur_4_2023 | CROW-CUR Guideline 4:2023 Reuse of hollow core slabs | 2 | canonical |
| norm_en_1168 | EN 1168 Precast concrete products - Hollow core slabs | 2 | canonical |
| norm_en_1090 | EN_1090 | 2 | canonical |
| norm_ns_3682 | NS 3682 Reuse of hollow-core slabs / Norwegian reuse standard | 2 | canonical |
| norm_sci_p440 | SCI P440 Reuse of Structural Steel | 2 | canonical |
| norm_crow_cur_guideline_4_2023 | CROW-CUR Guideline 4:2023 | 1 | **merge** → `norm_crow_cur_4_2023` |
| norm_historic_sections_book | Historic Sections Book | 1 | canonical |
| norm_iso_20887 | ISO_20887 | 1 | canonical |
| norm_rt_2012 | RT 2012 | 1 | canonical |
| norm_din_18940 | DIN_18940 | 0 | seed |
| norm_din_en_15804 | DIN_EN_15804 | 0 | seed |
| norm_din_en_15978 | DIN_EN_15978 | 0 | seed |
| norm_iso_14040 | ISO_14040 | 0 | seed |
| norm_iso_14044 | ISO_14044 | 0 | seed |

## PruefungNachweis hub snapshot (live `mit-bestand`)

| id | name | inbound | classification |
| --- | --- | ---: | --- |
| pr_zustandsbewertung | Zustandsbewertung | 150 | canonical |
| pr_sichtpruefung | Sichtpruefung | 59 | canonical |
| pr_statische_nachweisfuehrung | Statische_Nachweisfuehrung | 46 | canonical |
| pr_materialpruefung | Materialpruefung | 33 | canonical |
| pr_geometrische_vermessung | Geometrische_Vermessung | 12 | canonical |
| pr_schweissbarkeitspruefung | Schweissbarkeitspruefung | 7 | canonical |
| pr_zugversuch | Zugversuch | 6 | canonical |
| pr_schadstoffscreening | Schadstoffscreening | 4 | canonical |
| pr_brandschutznachweis | Brandschutznachweis | 3 | canonical |
| pr_abbrandbemessung | Abbrandbemessung | 0 | seed |
| pr_eignungspruefung_baulehm | Eignungspruefung_Baulehm | 0 | seed |

## Leistungsanforderung hub snapshot (live `mit-bestand`)

| id | name | inbound | classification |
| --- | --- | ---: | --- |
| la_dauerhaftigkeit | Dauerhaftigkeit | 142 | canonical |
| la_tragfaehigkeit | Tragfaehigkeit | 119 | canonical |
| la_brandschutz | Brandschutz | 93 | canonical |
| la_feuchteschutz | Feuchteschutz | 60 | canonical |
| la_waermeschutz | Waermeschutz | 44 | canonical |
| la_schallschutz | Schallschutz | 28 | canonical |
| la_rueckbaubarkeit | Rueckbaubarkeit | 9 | canonical |
| la_schadstofffreiheit | Schadstofffreiheit | 7 | canonical |
| la_feuerwiderstand | Feuerwiderstand | 3 | canonical (distinct from Brandschutz) |
| la_brandschutzanforderung | Brandschutzanforderung | 1 | **merge** → `la_brandschutz` |
| la_f90 | F90 | 0 | seed (Feuerwiderstandsklasse) |
| la_r90 | R90 | 0 | seed (Feuerwiderstandsklasse) |
| la_rei90 | REI90 | 0 | seed (Feuerwiderstandsklasse) |

## Same-name duplicates

None — the two CROW-CUR nodes have slightly different `name` strings
(distinguished from the same-name check).

## Orphan check

10 orphans, all kept as proposed seed (LCA standards, German fire-class
codes, specialty checks).

## Candidate patch

`patches/controlled_vocabulary_norm_pruefung.patch.jsonl` — 3 active operations:

| op | id / from→to | severity |
| --- | --- | --- |
| canonicalize_node | norm_sci_p427 | LOW |
| merge_node | norm_crow_cur_guideline_4_2023 → norm_crow_cur_4_2023 | LOW |
| merge_node | la_brandschutzanforderung → la_brandschutz | LOW |

The norm_sci_p427 canonicalize is idempotent against the current live state
(the canonical name and alias are already set).

## Human decision queue

- `la_feuerwiderstand` vs `la_brandschutz`: distinct concepts (fire
  protection broadly vs fire resistance specifically). Currently treated
  as separate — no patch action recommended unless the user wants to
  flatten them.

## Acceptance status

- Live DB reachable: yes (`mit-bestand`).
- Active patch is UTF-8 LF, dry-run safe.
- No deferred ops.
