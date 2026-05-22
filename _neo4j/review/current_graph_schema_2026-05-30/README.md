# Current graph schema and inventory

**Generated:** 2026-05-30 from live Neo4j database `mit-bestand`.

Neo4j remains the source of truth. This folder is a reproducible export snapshot, not a replacement for the database.

## Source snapshot

- Backup directory: `../backups/2026-05-30_current_graph_export/`
- Backup created UTC: `2026-05-30T09:55:55.259981+00:00`
- Nodes: `39548`
- Relationships: `81031`
- Backup checksum file: `../backups/2026-05-30_current_graph_export/checksums.sha256`

## Files in this export

| File | Contents |
|---|---|
| `current_graph_schema.json` | Complete schema summary: labels, relationship types, counts, constraints, indexes, property summaries, and relationship label patterns |
| `nodes.current.jsonl` | All current nodes with labels, properties, id/name helpers, and backup key |
| `relationships.current.jsonl` | All current relationships with type, properties, endpoint ids, endpoint labels, and endpoint names |
| `node_labels.csv` | Label counts |
| `relationship_types.csv` | Relationship type counts |
| `relationship_label_patterns.csv` | Relationship type by from-label-set and to-label-set |

## Node labels

| Label | Count |
|---|---:|
| `Akteur` | 679 |
| `Akteurrolle` | 24 |
| `Akteurtyp` | 10 |
| `Akzeptanz` | 7 |
| `Aufbereitungsverfahren` | 62 |
| `BauaufgabeIntervention` | 10 |
| `Bauobjektklasse` | 8 |
| `Bauobjektrolle` | 6 |
| `Bauproduktstatus` | 15 |
| `Bausystem` | 9 |
| `Bauteilebene` | 6 |
| `Bauteilgruppe` | 369 |
| `Bauteiltyp` | 23 |
| `Bauweise` | 6 |
| `Bauwerk` | 186 |
| `BauwerkEra` | 6 |
| `Beschaffungsweg` | 10 |
| `DataIssue` | 29061 |
| `Defekt` | 10 |
| `DeprecatedType` | 13 |
| `Dossier` | 100 |
| `DossierEntityTarget` | 2591 |
| `ExternalLink` | 5026 |
| `Funktionswechsel` | 6 |
| `Huerde` | 28 |
| `HuerdeKategorie` | 10 |
| `Kennwert` | 258 |
| `LCAModule` | 5 |
| `Land` | 19 |
| `Layer` | 6 |
| `Leistungsanforderung` | 46 |
| `Logistik` | 10 |
| `Marktmodell` | 11 |
| `MatchingQualitaet` | 9 |
| `Material` | 26 |
| `Materialdepot` | 23 |
| `Materialgruppe` | 11 |
| `Methode` | 13 |
| `Norm` | 103 |
| `Nutzung` | 9 |
| `OntologyAnchor` | 2 |
| `Programm` | 29 |
| `Projekt` | 101 |
| `Prozessphase` | 10 |
| `PruefungNachweis` | 120 |
| `Quelle` | 5343 |
| `RechtlicheBedingung` | 15 |
| `ResearchDocument` | 403 |
| `Ressourcenquelle` | 16 |
| `ReuseRule` | 20 |
| `Rueckbauverfahren` | 5 |
| `Schadstoff` | 9 |
| `SectionRef` | 641 |
| `Software` | 19 |
| `Stadt` | 76 |
| `Status` | 9 |
| `Tool` | 8 |
| `Tragwerksprinzip` | 4 |
| `Verbindungstechnik` | 15 |
| `WiederverwendungsArt` | 11 |
| `Wiederverwendungskette` | 14 |
| `Wirtschaft` | 12 |
| `Zertifizierungssystem` | 8 |
| `ZustandsKlasse` | 6 |

## Relationship types

| Type | Count |
|---|---:|
| `ANCHORED_BY` | 703 |
| `APPLIES_IN` | 20 |
| `APPLIES_TO` | 20 |
| `BELEGT_IN` | 4906 |
| `BERECHNET_NACH_MODUL` | 8 |
| `BETEILIGT_AN` | 576 |
| `BETRIEBEN_VON` | 6 |
| `BUILT_IN_ERA` | 8 |
| `CITED_FROM_DOSSIER` | 6150 |
| `CONCERNS` | 49111 |
| `ERHALT_FOERDERUNG_DURCH` | 4 |
| `EXACT_MATCH_CANDIDATE` | 306 |
| `FROM_DONOR` | 286 |
| `GEHÖRT_ZU` | 256 |
| `GILT_IN_LAND` | 40 |
| `HAS_BAUWERK` | 184 |
| `HAS_DATA_ISSUE` | 921 |
| `HAS_RISK_POLLUTANT` | 803 |
| `HAS_SOURCE_LINK` | 20 |
| `HAT_AKTEURROLLE` | 1327 |
| `HAT_AKTEURTYP` | 693 |
| `HAT_AUFBEREITUNG` | 448 |
| `HAT_BAUOBJEKTKLASSE` | 227 |
| `HAT_BAUOBJEKTROLLE` | 230 |
| `HAT_BAUPRODUKTSTATUS` | 67 |
| `HAT_BAUSYSTEM` | 64 |
| `HAT_BAUTEILEBENE` | 372 |
| `HAT_BAUTEILGRUPPE` | 369 |
| `HAT_BAUTEILTYP` | 607 |
| `HAT_BAUWEISE` | 129 |
| `HAT_BESCHAFFUNGSWEG` | 285 |
| `HAT_DEFEKT` | 45 |
| `HAT_DEFEKT_BEFUND` | 25 |
| `HAT_FUNKTIONSWECHSEL` | 299 |
| `HAT_HUERDE` | 1068 |
| `HAT_HUERDEKATEGORIE` | 167 |
| `HAT_INTERVENTION` | 148 |
| `HAT_KENNWERT` | 258 |
| `HAT_LEISTUNGSANFORDERUNG` | 561 |
| `HAT_LOGISTIK` | 500 |
| `HAT_MARKTMODELL` | 384 |
| `HAT_MATCHINGQUALITAET` | 187 |
| `HAT_MATERIALGRUPPE` | 516 |
| `HAT_METHODE` | 602 |
| `HAT_NUTZUNG` | 216 |
| `HAT_PROZESSPHASE` | 812 |
| `HAT_PRUEFUNG` | 410 |
| `HAT_RECHTLICHE_BEDINGUNG` | 12 |
| `HAT_RESSOURCENQUELLE` | 567 |
| `HAT_RUECKBAUVERFAHREN` | 301 |
| `HAT_STATUS` | 672 |
| `HAT_TRAGWERKSPRINZIP` | 72 |
| `HAT_TYPISCHEN_BAUPRODUKTSTATUS` | 19 |
| `HAT_VERBINDUNGSTECHNIK` | 131 |
| `HAT_WIEDERVERWENDUNGSART` | 621 |
| `HAT_WIRTSCHAFT` | 46 |
| `HAT_WIRTSCHAFTSASPEKT` | 11 |
| `HAT_ZERTIFIZIERUNG` | 12 |
| `HAT_ZUSTANDSKLASSE` | 40 |
| `INTO_RECEIVER` | 349 |
| `IST_UNTERVERFAHREN_VON` | 28 |
| `LIEGT_IN_LAND` | 554 |
| `LIEGT_IN_STADT` | 261 |
| `METHODENGRUNDLAGE_NORM` | 8 |
| `NUTZT_BAUWERK` | 169 |
| `NUTZT_MATERIAL` | 475 |
| `NUTZT_SOFTWARE` | 51 |
| `REFERENZIERT_NORM` | 145 |
| `RELEVANT_FOR` | 103 |
| `REQUIRES_VERIFICATION_FOR` | 347 |
| `STUB_PROJECT_LINK` | 200 |
| `TEILT_LAYER` | 15 |
| `TEIL_VON_KETTE` | 14 |
| `TEIL_VON_PROGRAMM` | 38 |
| `TYPISCH_BEI_BAUTEILTYP` | 10 |
| `TYPISCH_BEI_ERA` | 15 |
| `TYPISCH_BEI_MATERIAL` | 91 |
| `VERBUNDEN_MIT_AKTEUR` | 310 |

## Notes

- Import chunks and batches remain transport units only; semantic truth is the live graph.
- Archived `research/` or `_database/` material is not used as authority for this export.
- Relationship endpoints in `relationships.current.jsonl` are resolved to node `properties.id` when present; otherwise the export backup key is used.

