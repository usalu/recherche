# Reuse taxonomy coverage report — batches 01–09

Generated from Markdown batch files in `/mnt/data` plus the untouched topology JSON baseline. This is an audit/report only; it does not prepare import Cypher and it does not change the graph JSON.

## 1. Baseline graph scope

| Item | Count |
|---|---:|
| Projects in topology | 81 |
| Bauteilgruppe nodes in topology | 356 |
| Direct project→Bauteilgruppe edges in topology | 350 |
| Old WiederverwendungsArt edges still in topology | 425 |
| Old Aufbereitungsverfahren nodes in topology | 29 |

## 2. Markdown evidence coverage

| Metric | Count |
|---|---:|
| Parsed row-level Markdown evidence rows, batches 02–09 | 2101 |
| Batch 01 stated rows, summary-only in Markdown | 139 |
| Claimed rows across batches 01–09 | 2240 |
| Projects with row-level Markdown evidence | 79 / 81 |
| Projects with summary-level evidence only | 2 |
| Projects with at least basic component/outcome/source/location row-level mapping | 79 / 81 |
| Dense row-level mapped projects | 67 |
| Basic row-level mapped projects | 12 |

### Batch-level row audit

| Batch | File | Stated rows | Parsed row-level rows | Parsed projects | Note |
|---|---|---:|---:|---:|---|
| 01 | `reuse_taxonomy_v9_connection_expansion_batch_01.md` | 139 | 0 | 0 | summary only; needs row-level table |
| 02 | `reuse_taxonomy_v9_connection_expansion_batch_02.md` | 178 | 178 | 11 | OK |
| 03 | `reuse_taxonomy_v9_connection_expansion_batch_03.md` | 237 | 237 | 10 | OK |
| 04 | `reuse_taxonomy_v9_connection_expansion_batch_04.md` | 287 | 287 | 11 | OK |
| 05 | `reuse_taxonomy_v9_connection_expansion_batch_05.md` |  | 276 | 13 | OK |
| 06 | `reuse_taxonomy_v9_connection_expansion_batch_06.md` |  | 618 | 26 | OK |
| 07 | `reuse_taxonomy_v9_connection_expansion_batch_07.md` |  | 96 | 13 | OK |
| 08 | `reuse_taxonomy_v9_connection_expansion_batch_08.md` |  | 158 | 11 | OK |
| 09 | `reuse_taxonomy_v9_connection_expansion_batch_09.md` |  | 251 | 13 | OK |

## 3. What is mapped into which relationship/node dimensions

Relationship counts below are after normalizing older Batch 07/08 aliases such as `HAS_SOURCE` → `HAT_QUELLE`.

| Relationship | Row-level rows |
|---|---:|
| `HAT_ERGEBNIS` | 388 |
| `HAT_QUELLE` | 350 |
| `HAT_WIEDERVERWENDUNGSORT` | 344 |
| `HAT_BAUTEILGRUPPE` | 335 |
| `NUTZT_METHODE` | 269 |
| `HAT_AUFBEREITUNG` | 269 |
| `HAT_RUECKBAUVERFAHREN` | 132 |
| `ANGEWENDET_AUF` | 14 |

### Controlled taxonomy node usage after suggested v10.1 normalization

#### `Wiederverwendungsergebnis`
| Canonical node | Rows |
|---|---:|
| `Bestandserhalt` | 26 |
| `Wiederverwendung_gleiche_Funktion` | 174 |
| `Wiederverwendung_neue_Funktion` | 97 |
| `Modul_oder_Abschnittswiederverwendung` | 44 |
| `Material_Reprocessing` | 21 |
| `Geplant_oder_Gelagert` | 24 |
| **Needs manual correction / parser issue** | **2** |

#### `Quelle`
| Canonical node | Rows |
|---|---:|
| `Eigener_Bestand` | 55 |
| `Gleicher_Standort` | 17 |
| `Externer_Spenderbau` | 190 |
| `Bauteilmarkt_oder_Lager` | 19 |
| `Leihgabe_oder_Service` | 4 |
| `Restposten_Abfall_Unbekannt` | 65 |

#### `Wiederverwendungsort`
| Canonical node | Rows |
|---|---:|
| `In_situ` | 32 |
| `Im_selben_Gebaeude_versetzt` | 30 |
| `Auf_demselben_Standort_versetzt` | 18 |
| `Extern_importiert` | 255 |
| `Temporär_oder_zurueckgegeben` | 5 |
| `Gelagert_oder_Unbekannt` | 4 |

#### `Methode`
| Canonical node | Rows |
|---|---:|
| `Bestands_und_ReUse_Assessment` | 51 |
| `Urban_Mining_und_Scouting` | 53 |
| `Verfuegbarkeitsbasiertes_Design` | 81 |
| `Reversibles_Design` | 26 |
| `Zirkulaere_Beschaffung` | 24 |
| `Dokumentation_und_Monitoring` | 34 |

#### `Rueckbauverfahren`
| Canonical node | Rows |
|---|---:|
| `Ausbau_von_Bauteilen` | 4 |
| `Demontage` | 38 |
| `Selektiver_Rueckbau` | 29 |
| `Zerstoerungsarme_Bergung` | 48 |
| `Schneidender_Rueckbau` | 3 |
| `Integrierter_Rueckbau_und_Lagerung` | 7 |
| **Needs manual correction / parser issue** | **3** |

#### `Aufbereitungsverfahren`
| Canonical node | Rows |
|---|---:|
| `Reinigung_und_Oberflaeche` | 34 |
| `Zuschnitt_und_Vereinzelung` | 45 |
| `Pruefung_Sortierung_QS` | 106 |
| `Reparatur_und_Refurbishment` | 32 |
| `Remanufacturing_und_Upcycling` | 45 |
| `Verstaerkung_und_Schutz` | 6 |
| **Needs manual correction / parser issue** | **1** |

### Component rows

- Row-level `HAT_BAUTEILGRUPPE` mappings: **335**
- Distinct Bauteilgruppe/component target strings in row-level MD: **295**
- These are intentionally not capped at six because project component groups are real instance nodes, not controlled taxonomy buckets.

## 4. Confidence and review load

| Confidence | Rows |
|---|---:|
| `HIGH` | 1504 |
| `MEDIUM` | 356 |
| `LOW` | 241 |

Main interpretation: HIGH rows are good evidence candidates, MEDIUM rows usually need component-binding or source/detail review, and LOW rows should remain search leads only.

## 5. What is left

### A. Two projects are covered only in Batch 01 summary, not in a row-level Markdown evidence table

| Project ID | Project | What is missing |
|---|---|---|
| `p_k118_kopfbau_halle_118_winterthur` | K118 Kopfbau Halle 118 Winterthur | Convert Batch 01 summary evidence into explicit row-level MD rows for component, outcome, source, location, method, dismantling/preparation where supported. |
| `p_meduni_campus_mariannengasse` | MedUni Campus Mariannengasse Wien — BauKarussell pre-demolition reuse | Convert Batch 01 summary evidence into explicit row-level MD rows for component, outcome, source, location, method, dismantling/preparation where supported. |

### B. Older relation aliases still appear in the raw Markdown

These are easy normalizations before any future import-prep pass:

| Raw relation | Rows | Normalize to |
|---|---:|---|
| `HAS_METHOD` | 55 | `NUTZT_METHODE` |
| `HAS_REUSE_RESULT` | 52 | `HAT_ERGEBNIS` |
| `HAS_SOURCE` | 48 | `HAT_QUELLE` |
| `HAS_LOCATION` | 47 | `HAT_WIEDERVERWENDUNGSORT` |
| `HAS_PROCESSING` | 42 | `HAT_AUFBEREITUNG` |
| `HAS_DISMANTLING` | 9 | `HAT_RUECKBAUVERFAHREN` |
| `HAS_DECONSTRUCTION` | 1 | `HAT_RUECKBAUVERFAHREN` |

### C. Raw target labels exceeding the six-node taxonomy

Some older batches still contain pre-v10.1 labels. They are not fatal, but they must be normalized or reviewed before import-prep.

| Node type | Raw target | Rows | Suggested action |
|---|---|---:|---|
| `Wiederverwendungsergebnis` | `https://www.jablonicka.com/work/95%2C6%25-circular-reconstruction-of-offices-for-awm-m%C3%BCnster-` | 1 | Parser/table-cell shift or malformed row: inspect row manually. |
| `Wiederverwendungsergebnis` | `https://awm.stadt-muenster.de/gemeinsam-nachhaltig/klima-technik-innovation/kreislauffaehiges-bauen` | 1 | Parser/table-cell shift or malformed row: inspect row manually. |
| `Aufbereitungsverfahren` | `Rekonfiguration_und_Vormontage` | 16 | Normalize to `Remanufacturing_und_Upcycling`. |
| `Aufbereitungsverfahren` | `Zuschnitt_und_Anpassung` | 14 | Normalize to `Zuschnitt_und_Vereinzelung`. |
| `Aufbereitungsverfahren` | `Keine_wesentliche_Aufbereitung` | 3 | Normalize to `Pruefung_Sortierung_QS`. |
| `Aufbereitungsverfahren` | `Integrierter_Rueckbau_und_Lagerung` | 1 | Review; no safe canonical mapping yet. |
| `Wiederverwendungsort` | `Lokal_oder_Regional_importiert` | 84 | Normalize to `Extern_importiert`. |
| `Wiederverwendungsort` | `Auf_demselben_Areal` | 1 | Normalize to `Auf_demselben_Standort_versetzt`. |
| `Quelle` | `Lager_und_Bauteilboerse` | 9 | Normalize to `Bauteilmarkt_oder_Lager`. |
| `Quelle` | `Baustellenrest_oder_Ueberproduktion` | 5 | Normalize to `Restposten_Abfall_Unbekannt`. |
| `Quelle` | `Nicht_bestimmbar` | 3 | Normalize to `Restposten_Abfall_Unbekannt`. |
| `Methode` | `Design_for_Disassembly` | 5 | Normalize to `Reversibles_Design`. |
| `Methode` | `Dekonstruktion_mit_Inventar` | 2 | Normalize to `Dokumentation_und_Monitoring`. |
| `Rueckbauverfahren` | `Sortierung_und_Bergung` | 41 | Normalize to `Zerstoerungsarme_Bergung`. |
| `Rueckbauverfahren` | `Dekonstruktion_mit_Inventar` | 28 | Normalize to `Selektiver_Rueckbau`. |
| `Rueckbauverfahren` | `Demontage_von_Modulen` | 22 | Normalize to `Demontage`. |
| `Rueckbauverfahren` | `Nicht_dokumentiert` | 3 | Review; no safe canonical mapping yet. |

### D. Rows that should remain non-import-ready

- All batches still intentionally use `import_ready = FALSE`; this is correct for the current research phase.
- LOW-confidence rows: keep as search leads.
- MEDIUM-confidence rows: keep for human review, especially when evidence is project-level rather than component-level.
- Rows using `Nicht_dokumentiert` or `Keine_wesentliche_Aufbereitung` should usually become notes/review flags, not hard taxonomy edges, unless a source explicitly supports them.

## 6. Project-by-project coverage

| Project | Topology components | MD rows | Batches | Dimensions mapped | Status | Review rows |
|---|---:|---:|---|---|---|---:|
| 55 Great Suffolk Street, London | 1 | 13 | 09 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| AWM Münster – zirkulärer Büroausbau 3. OG | 5 | 33 | 03 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Association house, Gröditz | 2 | 31 | 06,07,08 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 14 |
| Association house, Plauen | 1 | 20 | 06,07,08 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 8 |
| BedZED / Beddington Zero Energy Development | 3 | 20 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Berlin-Schildow Pilot House / Berlin-Schildow 2nd pilot house | 1 | 30 | 06,07,08,09 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 9 |
| Bestandverplanzung Pavilion, München | 1 | 19 | 06,07,08 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 7 |
| Big Dig Building, Boston/Cambridge | 1 | 8 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Big Dig House, Lexington, Massachusetts | 3 | 14 | 05 | component, location, method, outcome, source | basic taxonomy mapped | 0 |
| BioPartner 5, Leiden / Oegstgeest | 5 | 29 | 09 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| BlueCity Offices Rotterdam | 4 | 17 | 02 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Boulder Fire Station 3 / City of Boulder Fire Rescue Station #3 | 4 | 20 | 03 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 1 |
| Brent Cross Town Primary Substation | 4 | 11 | 02 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Brighton Waste House / Brighton Wild House | 6 | 39 | 03 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Broethen Twin-House, Hoyerswerda | 2 | 29 | 06,07,08 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 14 |
| CRCLR House / Impact Hub Berlin | 6 | 34 | 04 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 1 |
| CascadeUp / London secondary-timber glulam demonstrator | 3 | 11 | 02 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Chiro d’Itterbeek / Sanitary block, Dilbeek | 13 | 50 | 05 | component, location, method, outcome, source | basic taxonomy mapped | 0 |
| Christus-Pavillon / Christ Pavilion Volkenroda | 6 | 38 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Circl / ABN AMRO urban mining context | 15 | 28 | 09 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Circular Centre Netherlands / Prinsenhof A reuse pilot | 3 | 22 | 04 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Circular Pavilion Paris | 6 | 33 | 04 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| ELEMENTA Walkeweg Basel — Wohnbau mit Wiederverwendung von Bestandskomponenten (Kanton Basel-Stadt Wettbewerb) | 4 | 27 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| ELYS Kultur- und Gewerbehaus Basel | 7 | 30 | 05 | component, location, method, outcome, source | basic taxonomy mapped | 0 |
| Europa Building Brussels / Résidence Palace – Europa | 2 | 10 | 05 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Ferme du Rail Paris | 8 | 16 | 02 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Grande Halle de Colombelles / Le WIP | 9 | 73 | 05,09 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Grubenstrasse 29 / Werkhof 29, Zürich | 9 | 39 | 05 | component, location, method, outcome, source | basic taxonomy mapped | 0 |
| Hastings Pier Visitor Centre / reclaimed timber cladding | 4 | 11 | 02 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 1 |
| Haus HOS / Mehrfamilienhaus Mühlhausen | 3 | 41 | 06,07,08 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 20 |
| Holbein Gardens, London | 4 | 21 | 03 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 2 |
| House of Fraser / 318 Oxford Street → TBC.London steel reuse chain | 5 | 18 | 05 | component, location, method, outcome, source | basic taxonomy mapped | 0 |
| Härmälänranta / A-Kruunu ReCreate mini-pilot Tampere | 2 | 14 | 04 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Impact Hub Berlin / CRCLR Fit-out | 7 | 38 | 04 | component, location, method, outcome, preparation, source | dense evidence mapped | 14 |
| Institut de Botanique de l’ULg, Liège | 2 | 24 | 06,07 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 13 |
| Jeugdkliniek Ithaka / Emergis Kloetinge | 7 | 45 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Juch-Areal Recyclingzentrum Zürich | 3 | 21 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Jugendtreff Ingersheim — CLT-Reuse Pilot (Stuttgart 210 first reallab, 2024) | 2 | 14 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| K118 Kopfbau Halle 118 Winterthur | 5 | 0 | 01-summary | batch01 summary only | summary-only MD, needs row table | 0 |
| KA13 / Kristian Augusts gate 13, Oslo | 5 | 30 | 04 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Kamikatsu Zero Waste Center / Hotel WHY | 5 | 32 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Kindergarten Mööslistrasse / Manegg Zürich | 7 | 45 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Liander / Alliander HQ, Duiven | 4 | 24 | 02 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Lo-Reninge Town Hall façade / Stadhuis Lo | 2 | 9 | 02 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Lokomotion Technology Centre mini-pilot Tampere | 1 | 9 | 04 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Lycée Michel Lucius Conversion, Luxembourg | 7 | 45 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| LysP8 — LysBüchelStrasse 8 Reuse Pilot Basel (Loeliger Strub / Zirkular / Stiftung Habitat) | 6 | 39 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Maison DnA / dnA House, Asse | 2 | 13 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Maison Vignette, Auderghem | 5 | 8 | 02 | component, location, method, outcome, preparation, source | dense evidence mapped | 1 |
| Maison des Canaux, Paris | 4 | 52 | 02,09 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| MedUni Campus Mariannengasse Wien — BauKarussell pre-demolition reuse | 6 | 0 | 01-summary | batch01 summary only | summary-only MD, needs row table | 0 |
| Mehrow Pilot House | 2 | 41 | 06,07,08,09 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 14 |
| Melkinlaituri Primary School and Day-care Centre Helsinki | 1 | 13 | 04 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 4 |
| Montessori Maassluis | 1 | 5 | 05 | component, location, method, outcome, source | basic taxonomy mapped | 0 |
| Multi Brussels / Reuse in MULTI | 4 | 27 | 02 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Musée de Folklore Vie Frontalière / MUSEF Mouscron | 1 | 24 | 06,07,08,09 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 8 |
| PLP London HQ circular studio fit-out | 4 | 18 | 05 | component, location, method, outcome, source | basic taxonomy mapped | 4 |
| People’s Pavilion Eindhoven | 5 | 28 | 09 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Plattenpalast Berlin | 2 | 32 | 06,07,08 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 13 |
| Plattenvereinigung Berlin | 4 | 60 | 06,07,08 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 26 |
| Re:Crete footbridge — reused concrete blocks | 1 | 9 | 05 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Recyclinghaus Hannover | 9 | 48 | 04 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Recypark Demets / Recypark Anderlecht | 1 | 10 | 09 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Resource Rows Copenhagen | 1 | 28 | 09 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Roots in the Sky / Blackfriars Crown Court | 2 | 9 | 05 | component, location, method, outcome, source | basic taxonomy mapped | 0 |
| Résilience / La Ferme des Possibles Stains | 7 | 56 | 06,07 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 44 |
| SUPERLOCAL Expogebouw / Superlocal Pavilion | 5 | 17 | 03 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 1 |
| Saxum Vineyard Equipment Barn | 3 | 13 | 05 | component, location, method, outcome, source | basic taxonomy mapped | 4 |
| Schärenmoosstrasse 115/117 Zürich — ménage à trois (Stiftung PWG Wettbewerb 2022) | 5 | 14 | 03 | component, location, method, outcome, source | basic taxonomy mapped | 4 |
| Svanen / The Swan Kindergarten Gladsaxe | 6 | 37 | 03 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| TRÆ High-Rise | 5 | 11 | 09 | component, location, method, outcome, source | basic taxonomy mapped | 0 |
| The Green House Utrecht | 6 | 27 | 09 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Thoravej 29 Copenhagen | 4 | 23 | 04 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Timber Square London | 5 | 20 | 03 | component, location, method, outcome, preparation, source | dense evidence mapped | 2 |
| UMAR Unit — Urban Mining and Recycling, NEST Empa Dübendorf | 8 | 18 | 05 | component, location, method, outcome, source | basic taxonomy mapped | 0 |
| Upcycle Studios Copenhagen | 3 | 14 | 02 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Verbiest + Karreveld | 7 | 104 | 06,07,08 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 44 |
| Villa Welpeloo Enschede | 4 | 23 | 04 | component, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| Woongroep Boschgaard Den Bosch | 4 | 26 | 03 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 1 |
| Zinneke / FEDER Masui4ever Brussels | 6 | 39 | 06 | component, deconstruction, location, method, outcome, preparation, source | dense evidence mapped | 0 |
| gjG House, Gentbrugge / Ghent | 2 | 10 | 03 | component, location, method, outcome, preparation, source | dense evidence mapped | 4 |

## 7. Recommended next work order

1. Convert the two Batch 01 summary-only projects, `K118` and `MedUni Campus Mariannengasse`, into explicit row-level Markdown evidence rows.
2. Normalize Batch 07/08 relation aliases to the v10.1 relationship names.
3. Normalize older raw target labels into the six-node taxonomy, especially `Lokal_oder_Regional_importiert`, `Sortierung_und_Bergung`, `Demontage_von_Modulen`, `Rekonfiguration_und_Vormontage`, and `Zuschnitt_und_Anpassung`.
4. Re-check MEDIUM/LOW rows for direct component-level evidence; promote only when evidence explicitly supports the component mapping.
5. After the research set is clean and row-level complete, create a deduplicated master Markdown evidence table. Do not prepare import until explicitly requested.