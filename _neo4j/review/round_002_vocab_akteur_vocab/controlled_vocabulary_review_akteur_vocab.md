# Round 002 Controlled Vocabulary Review: Akteurrolle + Akteurtyp

**Generated:** 2026-05-15
**Baseline reference:** [`../round_002_baseline/global_audit_report.md`](../round_002_baseline/global_audit_report.md)

> Scope reminder: this family covers the **vocab** roles and types
> (`ar_*` and `at_*`), **not** the project-content `a_*` actor-organization
> nodes (those belong to the actor-registry track — see
> [`processed/actor_registry/conflicts/node_conflicts.jsonl`](../../processed/actor_registry/conflicts/node_conflicts.jsonl)).

## Result in Context

Mostly clean structurally — no same-name duplicates — but the live graph
carries a layer of **legacy short-form vocab terms** that have been
superseded by consolidated long-form roles. Six `Akteurrolle` and two
`Akteurtyp` nodes are clear merge candidates: the modern term is in heavy
use and the legacy term retains only 0–2 inbound links.

A second tier (~4 `Akteurrolle` nodes) is **ambiguous**: the legacy term
still has 3–5 inbound references and could legitimately be either a
specialty role distinct from the consolidated parent, or a stragglers'
cluster to merge in. Defer to human.

A third tier (~7 `Akteurrolle` nodes) is **orphaned but specialty-named**
(`ar_fassade`, `ar_landschaftsplanung`, `ar_kunst_gestaltung`, etc.) and is
kept as proposed seed for future precision.

## Akteurrolle hub snapshot (live `mit-bestand`)

| id | name | inbound | classification |
| --- | --- | ---: | --- |
| ar_reuse_zirkularitaetsberatung | Reuse_Zirkularitaetsberatung | 203 | canonical |
| ar_entwurf_planung | Entwurf_Planung | 196 | canonical |
| ar_forschung_dokumentation | Forschung_Dokumentation | 126 | canonical |
| ar_fachplanung_nachweis | Fachplanung_Nachweis | 119 | canonical |
| ar_materiallieferung_markt | Materiallieferung_Markt | 88 | canonical |
| ar_bauherr_auftraggeber | Bauherr_Auftraggeber | 79 | canonical |
| ar_projektmanagement_koordination | Projektmanagement_Koordination | 75 | canonical |
| ar_bauausfuehrung_fertigung | Bauausfuehrung_Fertigung | 64 | canonical |
| ar_rueckbau_bauteilernte_logistik | Rueckbau_Bauteilernte_Logistik | 33 | canonical |
| ar_betrieb_nutzung | Betrieb_Nutzung | 31 | canonical |
| ar_oeffentliche_hand_foerderung | Oeffentliche_Hand_Foerderung | 29 | canonical |
| ar_bildung_wissenstransfer | Bildung_Wissenstransfer | 19 | canonical |
| ar_aufbereitung_refurbishment | Aufbereitung_Refurbishment | 18 | canonical |
| ar_unbestimmt | Unbestimmt | 15 | canonical |
| ar_architektur | Architektur | 5 | **NEEDS_REVIEW** — sub-specialty of `ar_entwurf_planung` or distinct? |
| ar_reuse_beratung | Reuse_Beratung | 4 | **NEEDS_REVIEW** — overlaps with `ar_reuse_zirkularitaetsberatung` |
| ar_nachhaltigkeitsberatung | Nachhaltigkeitsberatung | 3 | **NEEDS_REVIEW** — specialty or merge into reuse-zirkularität? |
| ar_tragwerksplanung | Tragwerksplanung | 3 | **NEEDS_REVIEW** — sub-specialty of `ar_fachplanung_nachweis`? |
| ar_betreiber_nutzer | Betreiber_Nutzer | 2 | **merge** → `ar_betrieb_nutzung` |
| ar_bauausfuehrung | Bauausfuehrung | 1 | **merge** → `ar_bauausfuehrung_fertigung` |
| ar_materiallieferant | Materiallieferant | 1 | **merge** → `ar_materiallieferung_markt` |
| ar_oeffentliche_hand | Oeffentliche_Hand | 1 | **merge** → `ar_oeffentliche_hand_foerderung` |
| ar_projektbeteiligte_unbestimmt | Projektbeteiligte_Unbestimmt | 1 | **merge** → `ar_unbestimmt` |
| ar_pruefung_qualitaetssicherung | Pruefung_Qualitaetssicherung | 1 | **NEEDS_REVIEW** — quality assurance distinct from `ar_fachplanung_nachweis`? |
| ar_rueckbau_demontage | Rueckbau_Demontage | 1 | **merge** → `ar_rueckbau_bauteilernte_logistik` |
| ar_brandschutz_barrierefreiheit | Brandschutz_Barrierefreiheit | 0 | keep as seed (specialty) |
| ar_fassade | Fassade | 0 | keep as seed (specialty) |
| ar_kunst_gestaltung | Kunst_Gestaltung | 0 | keep as seed (specialty) |
| ar_landschaftsplanung | Landschaftsplanung | 0 | keep as seed (specialty) |
| ar_software_digitalisierung | Software_Digitalisierung | 0 | keep as seed (specialty) |
| ar_stahlbau_fertigung | Stahlbau_Fertigung | 0 | keep as seed; sub-role of `ar_bauausfuehrung_fertigung` |
| ar_tga_gebaeudetechnik | TGA_Gebaeudetechnik | 0 | keep as seed (specialty) |

## Akteurtyp hub snapshot (live `mit-bestand`)

| id | name | inbound | classification |
| --- | --- | ---: | --- |
| at_unternehmen | Unternehmen | 298 | canonical |
| at_person | Person | 143 | canonical |
| at_forschung_lehre | Forschung_Lehre | 36 | canonical |
| at_organisation | Organisation | 30 | canonical |
| at_oeffentliche_institution | Oeffentliche_Institution | 27 | canonical |
| at_ngo_verband_netzwerk | NGO_Verband_Netzwerk | 18 | canonical |
| at_materialhub_bauteilboerse | Materialhub_Bauteilboerse | 17 | canonical |
| at_software_tool_anbieter | Software_Tool_Anbieter | 8 | canonical |
| at_foerdergeber_programmtraeger | Foerdergeber_Programmtraeger | 4 | canonical |
| at_unbekannt | Unbekannt | 1 | canonical |
| at_ngo_netzwerk | NGO_Netzwerk | 0 | **merge** → `at_ngo_verband_netzwerk` |
| at_verband_kammer | Verband_Kammer | 0 | **merge** → `at_ngo_verband_netzwerk` |

## Same-name duplicates

None.

## Orphan check

9 orphans (Akteurrolle 7, Akteurtyp 2). Classified above. The 7 Akteurrolle
orphans are kept as deliberately reserved specialty roles. The 2 Akteurtyp
orphans are merge targets (covered by the patch).

## Candidate patch

`patches/controlled_vocabulary_akteur_vocab.patch.jsonl` — 8 active operations:

| op | from | to | severity |
| --- | --- | --- | --- |
| merge_node | ar_bauausfuehrung | ar_bauausfuehrung_fertigung | MEDIUM |
| merge_node | ar_materiallieferant | ar_materiallieferung_markt | MEDIUM |
| merge_node | ar_oeffentliche_hand | ar_oeffentliche_hand_foerderung | MEDIUM |
| merge_node | ar_projektbeteiligte_unbestimmt | ar_unbestimmt | MEDIUM |
| merge_node | ar_rueckbau_demontage | ar_rueckbau_bauteilernte_logistik | MEDIUM |
| merge_node | ar_betreiber_nutzer | ar_betrieb_nutzung | MEDIUM |
| merge_node | at_ngo_netzwerk | at_ngo_verband_netzwerk | LOW |
| merge_node | at_verband_kammer | at_ngo_verband_netzwerk | LOW |

All 8 are deterministic: the legacy id has at most 2 inbound rels, the
target id is the obvious survivor, and `merge_node` is now supported by
the runner (Step C).

## Human decision queue

Five Akteurrolle nodes need human judgment:

| id | inbound | candidate parent | question |
| --- | ---: | --- | --- |
| ar_architektur | 5 | ar_entwurf_planung | merge into Entwurf_Planung, or keep as specialty? |
| ar_reuse_beratung | 4 | ar_reuse_zirkularitaetsberatung | merge or keep? |
| ar_nachhaltigkeitsberatung | 3 | ar_reuse_zirkularitaetsberatung | merge or specialty? |
| ar_tragwerksplanung | 3 | ar_fachplanung_nachweis | merge or specialty? |
| ar_pruefung_qualitaetssicherung | 1 | ar_fachplanung_nachweis | merge or specialty? |

## Acceptance status

- Live DB reachable: yes (`mit-bestand`).
- Active patch is UTF-8 LF.
- All 8 merge_node ops will be dry-run verified.
- No deferred ops.
