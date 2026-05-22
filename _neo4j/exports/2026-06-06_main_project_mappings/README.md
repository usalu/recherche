# Main Project Mappings Export

- Generated: `2026-06-06T07:43:15.288412+00:00`
- Database: `mit-bestand`
- Source of truth: live Neo4j graph
- Graph counts: `2304` nodes / `15486` relationships
- Retired label checks: `Quelle=0`, `Regelwerk=0`, `Status=0`
- Projects exported: `83`
- Project-actor-country rows: `474`

## Files

| File | Meaning |
| --- | --- |
| `main_projects.csv` | Ranked project list with summarized key mappings. |
| `project_actor_country_mappings.csv` | Detailed project-to-actor rows with country context and evidence properties where present. |
| `project_mapping_type_counts.csv` | Coverage counts for mapping relationship types around projects. |
| `main_projects.json` | Structured export with full mapping lists. |

## Top Projects By Graph Degree

| Rank | Project | Countries | Actors | Components | Materials | Degree |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| 1 | Impact Hub Berlin | Deutschland | 5 | 7 | 5 | 76 |
| 2 | CRCLR House | Deutschland | 7 | 6 | 5 | 72 |
| 3 | Chiro d’Itterbeek | Belgien | 8 | 12 | 7 | 67 |
| 4 | Ferme du Rail Paris | Frankreich | 7 | 8 | 0 | 64 |
| 5 | Recyclinghaus Hannover | Deutschland | 4 | 9 | 0 | 64 |
| 6 | House of Fraser | Vereinigtes Königreich | 10 | 3 | 4 | 63 |
| 7 | Résilience | Frankreich | 7 | 7 | 0 | 62 |
| 8 | AWM Münster – zirkulärer… | Deutschland | 5 | 5 | 4 | 61 |
| 9 | Grande Halle de Colombel… | Frankreich | 7 | 7 | 0 | 61 |
| 10 | Grubenstrasse 29 | Schweiz | 5 | 9 | 7 | 61 |
| 11 | MedUni Campus Wien | Österreich | 6 | 20 | 3 | 60 |
| 12 | K.118 Winterthur | Schweiz | 7 | 16 | 0 | 58 |
| 13 | Multi Brussels | Belgien | 7 | 9 | 3 | 58 |
| 14 | Circl | Niederlande | 14 | 5 | 3 | 57 |
| 15 | Plattenvereinigung Berlin | Deutschland | 4 | 4 | 0 | 56 |
| 16 | Holbein Gardens, London | Vereinigtes Königreich | 7 | 3 | 5 | 55 |
| 17 | Timber Square London | Vereinigtes Königreich | 10 | 3 | 3 | 53 |
| 18 | BlueCity Offices… | Niederlande | 5 | 7 | 0 | 52 |
| 19 | Haus HOS | Deutschland | 4 | 3 | 0 | 50 |
| 20 | Plattenpalast Berlin | Deutschland | 3 | 2 | 0 | 50 |
| 21 | Circular Centre Netherla… | Niederlande | 6 | 3 | 0 | 49 |
| 22 | Christus-Pavillon | Deutschland | 7 | 6 | 0 | 48 |
| 23 | Liander | Niederlande | 4 | 8 | 0 | 48 |
| 24 | Svanen | Dänemark | 7 | 7 | 0 | 48 |
| 25 | BioPartner 5 | Niederlande | 8 | 6 | 0 | 47 |
| 26 | Circular Pavilion Paris | Frankreich | 6 | 6 | 0 | 47 |
| 27 | SUPERLOCAL Expogebouw | Niederlande | 8 | 4 | 0 | 47 |
| 28 | Brent Cross Town… | Vereinigtes Königreich | 10 | 2 | 1 | 46 |
| 29 | Recypark Demets | Belgien | 7 | 1 | 0 | 46 |
| 30 | Jeugdkliniek Ithaka | Niederlande | 8 | 6 | 0 | 45 |

## Mapping Coverage

| Field | Relationship | Target | Edges | Projects |
| --- | --- | --- | ---: | ---: |
| actors | `BETEILIGT_AN` | `Akteur` | 474 | 77 |
| evidence_requirements | `ERFORDERT_NACHWEIS` | `Nachweisforderung` | 415 | 72 |
| component_groups | `HAT_BAUTEILGRUPPE` | `Bauteilgruppe` | 360 | 79 |
| regulatory_questions | `TRIGGERS_REGULIERUNGSFRAGE` | `Regulierungsfrage` | 320 | 72 |
| buildings | `HAT_BAUWERK` | `Bauwerk` | 177 | 81 |
| uses | `HAT_NUTZUNG` | `Nutzung` | 135 | 77 |
| process_phases | `HAT_PROZESSPHASE` | `Prozessphase` | 112 | 25 |
| logistics | `HAT_LOGISTIK` | `Logistik` | 97 | 42 |
| component_types | `HAT_BAUTEILTYP` | `Bauteiltyp` | 94 | 16 |
| barriers | `HAT_HUERDE` | `Huerde` | 93 | 46 |
| cities | `LIEGT_IN_STADT` | `Stadt` | 84 | 80 |
| countries | `LIEGT_IN_LAND` | `Land` | 81 | 81 |
| methods | `HAT_METHODE` | `Methode` | 80 | 23 |
| architecture_results | `HAT_ARCHITEKTURERGEBNIS` | `Architekturergebnis` | 79 | 79 |
| design_methods | `HAT_ENTWURFSMETHODIK` | `Entwurfsmethodik` | 79 | 79 |
| materials | `NUTZT_MATERIAL` | `Material` | 62 | 16 |
| procurement_paths | `HAT_BESCHAFFUNGSWEG` | `Beschaffungsweg` | 60 | 34 |
| pollutants | `ERFORDERT_SCHADSTOFFPRUEFUNG` | `Schadstoff` | 37 | 14 |
| programs | `TEIL_VON_PROGRAMM` | `Programm` | 28 | 23 |
| software | `NUTZT_SOFTWARE` | `Software` | 16 | 13 |
| funding_programs | `ERHALT_FOERDERUNG_DURCH` | `Programm` | 3 | 3 |
