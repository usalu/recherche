# Content Split Audit

Comparison of the restored original file `entwurf` against the 21 clustered Markdown files generated from it.

## Result

- Result: **no missing original direct body text found**.
- Original file: `entwurf`, SHA256 `605866E8EF1A17355094840B4BEB1ABD1365C400144FEB024DA9071E040EAF5C`, `57936` bytes.
- Cluster files compared: `21`.
- Original headings checked: `100`; `96` have direct body text and `4` have no direct body text.
- Direct body sections found exactly once: `96`.
- Direct body sections found multiple times: `0`.
- Missing or changed direct body sections: `0`.

## File Set

- Expected cluster files: `21`.
- Present cluster files: `21`.
- Leaf-only files still present at the top level: `0`.
- Missing expected cluster files: none.
- Extra `.md` files in comparison set: none.
- Remaining leaf-only files: none.

## Structural Changes Seen

- New numbered headings in cluster files replace the original local headings.
- Every cluster file adds a leading `## Struktur` outline.
- Some unmapped original sections are grouped under `Review-Hinweis` headings.
- These additions are structural wrappers, not original prose changes.

## Missing Or Changed Original Direct Body Text

None. Every non-empty direct body section from `entwurf` was found exactly in at least one cluster file.

## Duplicate Original Direct Body Text

None. Every non-empty original direct body section was found exactly once.

## Section Coverage

| Original line | Level | Original heading | Status | File(s) |
|---:|---:|---|---|---|
| 1 | 1 | Schritt 1 — Bauteil-Seed | no direct body text | - |
| 3 | 2 | Einspeiseplattform: Vom realen Stahlbetonbauteil zum generatorfähigen Input | found exactly | `1.1.4 - Output Bauteil-Seed.md` |
| 28 | 2 | 1. Rolle des Bauteil-Seeds | found exactly | `1.1.4 - Output Bauteil-Seed.md` |
| 38 | 2 | 2. Eingabeprozess | found exactly | `1.1.1 - Eingabeprozess.md` |
| 51 | 2 | 3. User Input | found exactly | `1.1.1 - Eingabeprozess.md` |
| 70 | 2 | 4. API / Import aus Bauteilbörsen | found exactly | `1.1.1 - Eingabeprozess.md` |
| 89 | 2 | 5. UI-Konzept | found exactly | `1.1.2 - UI Concept.md` |
| 116 | 2 | 6. Minimaler Input | found exactly | `1.1.2 - UI Concept.md` |
| 150 | 2 | 7. KI-Erkennung | found exactly | `1.1.2 - UI Concept.md` |
| 183 | 2 | 8. Formular-Interface | found exactly | `1.1.2 - UI Concept.md` |
| 213 | 2 | 9. Nachweis-Panel | found exactly | `1.1.2 - UI Concept.md` |
| 236 | 2 | 10. Bauteil-Daten | found exactly | `1.1.3 - Bauteil-Daten.md` |
| 260 | 2 | 11. Mindestdaten für die Vorplanung | found exactly | `1.1.3 - Bauteil-Daten.md` |
| 276 | 2 | 12. Abgeleitete Daten | found exactly | `1.1.3 - Bauteil-Daten.md` |
| 301 | 2 | 13. Output: Bauteil-Seed | found exactly | `1.1.4 - Output Bauteil-Seed.md` |
| 347 | 2 | 14. Beispiel A — Ortbeton-Zuschnitt | found exactly | `1.1.4 - Output Bauteil-Seed.md` |
| 378 | 2 | 15. Beispiel B — Fertigteil | found exactly | `1.1.4 - Output Bauteil-Seed.md` |
| 417 | 2 | 16. Kernaussage | found exactly | `1.1.4 - Output Bauteil-Seed.md` |
| 437 | 1 | Schritt 2 — Generator | no direct body text | - |
| 439 | 2 | Vom Bauteil-Seed zum planbaren Stahlbeton-Bauteilobjekt | found exactly | `1.2.2 - Klassifikationslogik.md` |
| 473 | 2 | 1. Rolle des Generators | found exactly | `1.2.1 - Rolle des Generators.md` |
| 483 | 2 | 2. Konzept: Seed → planbares Bauteilobjekt | found exactly | `1.2.1 - Rolle des Generators.md` |
| 511 | 2 | 3. Grammatiklogik | found exactly | `1.2.1 - Rolle des Generators.md` |
| 550 | 2 | 4. Klassifikationslogik | found exactly | `1.2.2 - Klassifikationslogik.md` |
| 554 | 3 | Typologie | found exactly | `1.2.2 - Klassifikationslogik.md` |
| 579 | 3 | Generatorgrammatik | found exactly | `1.2.2 - Klassifikationslogik.md` |
| 600 | 3 | Typ | found exactly | `1.2.2 - Klassifikationslogik.md` |
| 621 | 3 | Piece | found exactly | `1.2.2 - Klassifikationslogik.md` |
| 638 | 2 | 5. Standardisierung und Typisierung von Stahlbeton-Bauteilen | found exactly | `1.2.2 - Klassifikationslogik.md` |
| 658 | 3 | Fertigteile | found exactly | `1.2.2 - Klassifikationslogik.md` |
| 677 | 3 | Zuschnitt-Elemente | found exactly | `1.2.2 - Klassifikationslogik.md` |
| 699 | 2 | 6. Bauteil-Seed → generiertes Bauteilobjekt | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 719 | 2 | 7. Geometrisches Planungsmodell | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 748 | 2 | 8. Abstraktes Strukturmodell | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 777 | 2 | 9. Abstraktes Energiemodell | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 803 | 2 | 10. Semantisches Modell | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 820 | 2 | 11. Ports | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 860 | 2 | 12. Connectoren | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 893 | 2 | 13. Evidence Link | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 918 | 2 | 14. Datenvertrauen und fehlende Nachweise | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 951 | 2 | 15. Beispiel 1 — Hohlkörperdecke als Fertigteil | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 969 | 2 | 16. Beispiel 2 — Ortbeton-Deckenfeld als standardisiertes Segment | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 986 | 2 | 17. Beispiel 3 — Stahlbeton-Wandplatte | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 1004 | 2 | 18. Kernbotschaft | found exactly | `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md` |
| 1026 | 1 | Schritt 3 — Bauteilkatalog | no direct body text | - |
| 1028 | 2 | Vom generierten Stahlbeton-Bauteilobjekt zum auswählbaren Entwurfsbaustein | found exactly | `2.1.1 - Bauteilkarte.md` |
| 1058 | 2 | 1. Rolle des Bauteilkatalogs | found exactly | `2.1.1 - Bauteilkarte.md` |
| 1079 | 2 | 2. Übergang vom Generator in den Katalog | found exactly | `2.1.1 - Bauteilkarte.md` |
| 1107 | 2 | 3. Bauteilkarte | found exactly | `2.1.1 - Bauteilkarte.md` |
| 1142 | 2 | 4. Visuelle Ebene | found exactly | `2.1.1 - Bauteilkarte.md` |
| 1162 | 2 | 5. Datenlayer | found exactly | `2.1.1 - Bauteilkarte.md` |
| 1206 | 2 | 6. Reifegrad | found exactly | `2.1.1 - Bauteilkarte.md` |
| 1239 | 2 | 7. Prüfstatus | found exactly | `2.1.1 - Bauteilkarte.md` |
| 1289 | 2 | 8. Filterstruktur | found exactly | `2.1.2 - Filterstruktur.md` |
| 1297 | 3 | 8.1 Typologie / Typ | found exactly | `2.1.2 - Filterstruktur.md` |
| 1328 | 3 | 8.2 Geometrie | found exactly | `2.1.2 - Filterstruktur.md` |
| 1360 | 3 | 8.3 Funktion | found exactly | `2.1.2 - Filterstruktur.md` |
| 1385 | 3 | 8.4 Semantik / Kompatibilität | found exactly | `2.1.2 - Filterstruktur.md` |
| 1408 | 3 | 8.5 Tragwerk | found exactly | `2.1.2 - Filterstruktur.md` |
| 1430 | 3 | 8.6 Energie | found exactly | `2.1.2 - Filterstruktur.md` |
| 1452 | 3 | 8.7 Verfügbarkeit / Menge | found exactly | `2.1.2 - Filterstruktur.md` |
| 1483 | 3 | 8.8 Risiko / Nachweise | found exactly | `2.1.2 - Filterstruktur.md` |
| 1504 | 3 | 8.9 CO₂ / Transport | found exactly | `2.1.2 - Filterstruktur.md` |
| 1522 | 2 | 9. Katalog-Aktionen | found exactly | `2.1.3 - Katalog-Aktionen.md` |
| 1527 | 3 | Auswählen / Vergleichen | found exactly | `2.1.3 - Katalog-Aktionen.md` |
| 1559 | 3 | Platzieren im Playground | found exactly | `2.1.3 - Katalog-Aktionen.md` |
| 1581 | 3 | Reservieren / Anfrage an Bauteilbörse | found exactly | `2.1.3 - Katalog-Aktionen.md` |
| 1601 | 2 | 10. Beispielkarte A — Hohlkörperdecke | found exactly | `2.1.3 - Katalog-Aktionen.md` |
| 1636 | 2 | 11. Beispielkarte B — Stahlbeton-Wandplatte | found exactly | `2.1.3 - Katalog-Aktionen.md` |
| 1670 | 2 | 12. Beispielkarte C — ColumnBeamSlabAssembly | found exactly | `2.1.3 - Katalog-Aktionen.md` |
| 1704 | 2 | 13. Kernaussage | found exactly | `2.1.3 - Katalog-Aktionen.md` |
| 1725 | 1 | Schritt 4 — Playground | no direct body text | - |
| 1727 | 2 | Vom Bauteilkatalog zur komponierbaren Stahlbeton-ReUse-Entwurfsvariante | found exactly | `2.2.1 - Idee Komposition.md` |
| 1769 | 2 | 1. Rolle des Playgrounds | found exactly | `2.2.1 - Idee Komposition.md` |
| 1793 | 2 | 2. Idee + Komposition | found exactly | `2.2.1 - Idee Komposition.md` |
| 1826 | 2 | 3. Target-Entwurf | found exactly | `2.2.1 - Idee Komposition.md` |
| 1919 | 2 | 4. Kombination mehrerer Bauteile | found exactly | `2.2.1 - Idee Komposition.md` |
| 1944 | 2 | 5. Kompatibilitätsprüfung | found exactly | `2.2.2 - Kompatibilitaetspruefung.md` |
| 1974 | 2 | 6. Regelquellen | found exactly | `2.2.2 - Kompatibilitaetspruefung.md` |
| 1978 | 3 | Regelbasiert | found exactly | `2.2.2 - Kompatibilitaetspruefung.md` |
| 1996 | 3 | Energetisch | found exactly | `2.2.2 - Kompatibilitaetspruefung.md` |
| 2020 | 3 | Tragwerklich | found exactly | `2.2.2 - Kompatibilitaetspruefung.md` |
| 2045 | 3 | Realwelt-basiert | found exactly | `2.2.2 - Kompatibilitaetspruefung.md` |
| 2064 | 3 | Semantisch | found exactly | `2.2.2 - Kompatibilitaetspruefung.md` |
| 2100 | 2 | 7. Entwurfsfeedback | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2120 | 2 | 8. Live-Warnungen | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2124 | 3 | Fehlende Nachweise | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2140 | 3 | Zeitkonflikte | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2155 | 3 | Riskante Verbindungen | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2170 | 3 | Unvollständige Mengen | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2185 | 3 | Risiko / Datenvertrauen | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2201 | 2 | 9. Visuelle Statuslogik | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2240 | 2 | 10. Variantenbewertung | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2276 | 2 | 11. ReUse-Anteil | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2299 | 2 | 12. CO₂-Vergleich | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2320 | 2 | 13. System-Kompatibilität | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2341 | 2 | 14. Regelbasierte Alternativvorschläge | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2382 | 2 | 15. Umgang mit unvollständigen Mengen | found exactly | `2.2.3 - Entwurfsfeedback.md` |
| 2408 | 2 | 16. Export | found exactly | `2.2.4 - Export.md` |
| 2435 | 2 | 17. Beispiel: Bürogebäude aus Hohlkörperdecken, Stützen und Trägern | found exactly | `2.2.4 - Export.md` |

## Interpretation

The split did not lose or alter any original prose section according to this exact direct-body comparison. The visible changes are numbering, structure outlines, and review grouping labels.

## Method Note

This audit compares direct section body text, not the old headings themselves. Headings were intentionally changed to match the current numbered tree.
