# Keep-list decision matrix summary

Target: ~4 properties per label. `keep_core`+`keep_semantic` = core survivors.
`domain_review` = surplus domain fields you decide to keep or drop.
Fact/reference labels may justifiably exceed 4.

| Label | Nodes | Core survivors | Keep list | domain_review | Flag |
|---|---:|---:|---|---|---|
| DataIssue | 28729 | 1 | `id` | - | meta (separate) |
| Quelle | 5330 | 4 | `id`, `quelltyp`, `title`, `url` | - |  |
| ExternalLink | 5017 | 4 | `id`, `quelltyp`, `title`, `url` | - |  |
| DossierEntityTarget | 2591 | 2 | `id`, `name` | - | meta (separate) |
| Akteur | 669 | 2 | `id`, `name` | - |  |
| SectionRef | 636 | 3 | `id`, `name`, `url` | - |  |
| ResearchDocument | 402 | 4 | `id`, `name`, `quelltyp`, `source_file` | - |  |
| Bauteilgruppe | 356 | 7 | `alte_funktion`, `bg_kind`, `id`, `name`, `neue_funktion`, `reuse_status`, `tragend` | - | OVER (trim) |
| Kennwert | 255 | 9 | `bilanzgrenze`, `category`, `einheit`, `fact_index`, `id`, `kennwert`, `method`, `wert`, `wert_text` | - | justified (fact/reference) |
| Bauwerk | 184 | 4 | `id`, `name`, `name_full`, `nutzung_text` | - |  |
| PruefungNachweis | 120 | 3 | `id`, `name`, `scope_note` | - |  |
| Norm | 103 | 5 | `country_short`, `id`, `name`, `name_full`, `scope_note` | - | justified (fact/reference) |
| Dossier | 97 | 3 | `id`, `name`, `quelltyp` | - |  |
| Projekt | 86 | 7 | `area_m2_gross`, `id`, `name`, `name_full`, `nutzung_text`, `projektstatus_text`, `year_completed` | - | OVER (trim) |
| Stadt | 74 | 2 | `id`, `name` | - |  |
| Aufbereitungsverfahren | 62 | 3 | `id`, `name`, `scope_note` | - |  |
| Leistungsanforderung | 46 | 2 | `id`, `name` | - |  |
| Programm | 29 | 7 | `aliases`, `id`, `name`, `name_full`, `scope_note`, `short_description`, `type` | - | OVER (trim) |
| Huerde | 28 | 2 | `id`, `name` | - |  |
| Material | 26 | 2 | `id`, `name` | - |  |
| Akteurrolle | 24 | 3 | `aliases`, `id`, `name` | - |  |
| Bauteiltyp | 23 | 3 | `brand_layer`, `id`, `name` | - |  |
| Materialdepot | 22 | 4 | `id`, `name`, `name_full`, `nutzung_text` | - |  |
| ReuseRule | 20 | 2 | `id`, `name` | - | meta (separate) |
| Software | 18 | 3 | `id`, `kind`, `name` | - |  |
| Land | 16 | 9 | `aliases`, `asbest_neshap_year`, `asbest_note`, `asbest_verbot_jahr`, `country_iso2`, `id`, `kmf_grenzwert_jahr`, `name`, `pcb_verbot_jahr` | - | justified (fact/reference) |
| RechtlicheBedingung | 16 | 4 | `id`, `is_universal`, `name`, `scope_note` | - |  |
| Ressourcenquelle | 16 | 3 | `beschreibung`, `id`, `name` | - |  |
| Bauproduktstatus | 15 | 4 | `id`, `name`, `name_full`, `scope_note` | - |  |
| Verbindungstechnik | 15 | 3 | `id`, `name`, `scope_note` | - |  |
| Wiederverwendungskette | 14 | 3 | `id`, `name`, `name_full` | - |  |
| DeprecatedType | 13 | 1 | `id` | - | meta (separate) |
| Methode | 13 | 2 | `id`, `name` | - |  |
| Wirtschaft | 12 | 3 | `id`, `name`, `scope_note` | - |  |
| Marktmodell | 11 | 4 | `id`, `name`, `name_full`, `scope_note` | - |  |
| Materialgruppe | 11 | 3 | `id`, `name`, `scope_note` | - |  |
| WiederverwendungsArt | 11 | 3 | `facet`, `id`, `name` | - |  |
| Akteurtyp | 10 | 3 | `aliases`, `id`, `name` | - |  |
| BauaufgabeIntervention | 10 | 2 | `id`, `name` | - |  |
| Beschaffungsweg | 10 | 3 | `beschreibung`, `id`, `name` | - |  |
| Defekt | 10 | 4 | `id`, `name`, `name_full`, `scope_note` | - |  |
| HuerdeKategorie | 10 | 2 | `id`, `name` | - |  |
| Logistik | 10 | 2 | `id`, `name` | - |  |
| Prozessphase | 10 | 2 | `id`, `name` | - |  |
| Bausystem | 9 | 3 | `definition`, `id`, `name` | - |  |
| MatchingQualitaet | 9 | 4 | `id`, `name`, `name_full`, `scope_note` | - |  |
| Nutzung | 9 | 2 | `id`, `name` | - |  |
| Schadstoff | 9 | 3 | `id`, `name`, `standards_body` | - |  |
| Status | 9 | 4 | `aliases`, `id`, `kind`, `name` | - |  |
| Bauobjektklasse | 8 | 2 | `id`, `name` | - |  |
| Zertifizierungssystem | 8 | 3 | `id`, `name`, `scheme_kind` | - |  |
| Akzeptanz | 7 | 4 | `id`, `name`, `name_full`, `scope_note` | - |  |
| Tool | 7 | 3 | `id`, `kind`, `name` | - |  |
| Bauobjektrolle | 6 | 2 | `id`, `name` | - |  |
| Bauteilebene | 6 | 2 | `id`, `name` | - |  |
| Bauweise | 6 | 2 | `id`, `name` | - |  |
| BauwerkEra | 6 | 5 | `id`, `name`, `notes`, `year_from`, `year_to` | - | justified (fact/reference) |
| Funktionswechsel | 6 | 2 | `id`, `name` | - |  |
| Geltungsbereich | 6 | 5 | `id`, `name`, `scope_note`, `scope_system`, `scope_type` | - | justified (fact/reference) |
| Layer | 6 | 3 | `brand_position`, `id`, `name` | - |  |
| ZustandsKlasse | 6 | 4 | `id`, `name`, `name_full`, `scope_note` | - |  |
| Geschaeftsmodell | 5 | 2 | `id`, `name` | - |  |
| LCAModule | 5 | 4 | `en15978_code`, `id`, `name`, `scope_note` | - |  |
| Rueckbauverfahren | 5 | 2 | `id`, `name` | - |  |
| Tragwerksprinzip | 4 | 2 | `id`, `name` | - |  |
| OntologyAnchor | 2 | 2 | `id`, `name` | - | meta (separate) |

## Verdict totals

| Verdict | Pairs |
|---|---:|
| `drop` | 465 |
| `keep_core` | 127 |
| `keep_semantic` | 89 |
| `meta_separate` | 74 |
| `migrate_then_drop` | 7 |
| `migrate_edge_then_drop` | 4 |
| `move_to_relationship` | 1 |

Labels over the 4-property budget: Bauteilgruppe, Projekt, Programm
