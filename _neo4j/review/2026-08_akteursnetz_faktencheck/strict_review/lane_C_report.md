# Strict Review – Lane C (GB, NL, SE)

## Ergebnis

- Eingefrorener Umfang: **292** Datensätze
- Entscheidungen: **245 keep**, **46 prune**, **1 merge**
- Behaltene realisierte Projekte: **29**
- Review-Status: primary_complete
- Primärreview: C

| Land | Gesamt | keep | prune | merge |
|---|---:|---:|---:|---:|
| GB | 129 | 101 | 28 | 0 |
| NL | 117 | 101 | 15 | 1 |
| SE | 46 | 43 | 3 | 0 |

## Angewendetes Gate

Behalten wurden nur konkret belegte akteursspezifische Beiträge zur baulichen
Wiederverwendung oder ausdrücklich reuse-spezifische Enablerrollen. Projektknoten
wurden nur behalten, wenn tatsächlich wiederverwendete Bauteile oder Materialien
belegt sind. Partnerlisten, allgemeine Nachhaltigkeit, Recycling und ausschließlich
zukünftige Demontierbarkeit wurden nicht als ausreichend gewertet.

## Sonderfälle

- GB:P6 wurde als future_design_only ausgesondert.
- NL:P4 ist der kanonische Circl-Knoten; NL:P5 wird auf dessen EID gemergt.
- SE:I01 wurde als realisiertes Bauvorhaben typisiert und mit eingebauten
  Betonhohldielen aus dem früheren IKEA Kållered belegt.
- Die abgeschnittenen Projektnamen GB:P8, GB:P11, NL:P3, NL:P6,
  NL:P11 und NL:P16 wurden rekonstruiert.
- GB:U46 wurde als Opera Property & Asset Management identifiziert;
  NL:U42 als Pieters.

## Prune-Entscheidungen

- GB:I01 – strict_gate_failed
- GB:M07 – strict_gate_failed
- GB:N01 – strict_gate_failed
- GB:N04 – historical_or_closed_org
- GB:O01 – strict_gate_failed
- GB:O02 – strict_gate_failed
- GB:O04 – strict_gate_failed
- GB:P3 – strict_gate_failed
- GB:P6 – future_design_only
- GB:U03 – strict_gate_failed
- GB:U09 – historical_or_closed_org
- GB:U11 – strict_gate_failed
- GB:U12 – historical_or_closed_org
- GB:U13 – strict_gate_failed
- GB:U15 – strict_gate_failed
- GB:U18 – strict_gate_failed
- GB:U20 – strict_gate_failed
- GB:U22 – strict_gate_failed
- GB:U23 – strict_gate_failed
- GB:U24 – strict_gate_failed
- GB:U28 – strict_gate_failed
- GB:U34 – strict_gate_failed
- GB:U37 – strict_gate_failed
- GB:U39 – strict_gate_failed
- GB:U48 – strict_gate_failed
- GB:U50 – strict_gate_failed
- GB:U53 – strict_gate_failed
- GB:U57 – strict_gate_failed
- NL:U01 – strict_gate_failed
- NL:U04 – strict_gate_failed
- NL:U06 – strict_gate_failed
- NL:U20 – strict_gate_failed
- NL:U21 – strict_gate_failed
- NL:U24 – strict_gate_failed
- NL:U48 – historical_or_closed_org
- NL:U50 – strict_gate_failed
- NL:U54 – strict_gate_failed
- NL:U55 – strict_gate_failed
- NL:U57 – strict_gate_failed
- NL:U58 – strict_gate_failed
- NL:U60 – strict_gate_failed
- NL:U63 – strict_gate_failed
- NL:U64 – historical_or_closed_org
- SE:I03 – strict_gate_failed
- SE:U12 – strict_gate_failed
- SE:U18 – strict_gate_failed

## Behaltene Projekte

GB:P1, GB:P10, GB:P11, GB:P12, GB:P13, GB:P14, GB:P2, GB:P4, GB:P5, GB:P7, GB:P8, GB:P9, NL:P10, NL:P11, NL:P12, NL:P13, NL:P14, NL:P15, NL:P16, NL:P2, NL:P3, NL:P4, NL:P6, NL:P7, NL:P8, NL:P9, SE:I01, SE:P1, SE:P2.

## Primärquellen mit Zugriffseinschränkung

Bei den folgenden Primärseiten war der Direktzugriff nicht stabil, technisch
eingeschränkt oder der ursprüngliche Pfad nicht mehr verfügbar. Die Entscheidung
wurde deshalb mit einer geöffneten zusätzlichen Quelle beziehungsweise – wenn
hinreichend konkret – mit dem bereits gespeicherten exakten Quellenzitat abgesichert:

- GB:P4
- GB:S02
- GB:U33
- GB:X01
- NL:M11
- NL:M16
- NL:O06
- NL:S03
- NL:U34
- NL:U35
- NL:U61
- SE:F02
- SE:M01

Alle übrigen für keep verwendeten Evidenz-URLs waren im Review erreichbar.
Nicht erreichbare oder nur generische Quellen führten ohne hinreichende
akteursspezifische Evidenz zu prune.

## Korrekturen an Namen und Typen

- GB:P11 – Name: PLP Architecture London Studio Circular Fit-out
- GB:P8 – Name: Hastings Pier Visitor Centre
- GB:U46 – Name: Opera Property & Asset Management; Typ: Unternehmen
- NL:M01 – Typ: Unternehmen
- NL:P11 – Name: People’s Pavilion
- NL:P16 – Name: Woongroep Boschgaard
- NL:P3 – Name: BlueCity Offices
- NL:P6 – Name: Circular Centre Netherlands
- NL:U42 – Name: Pieters
- SE:I01 – Typ: Bauvorhaben

## Prüfstatus

Jeder Lane-C-Eintrag kommt genau einmal vor. Rollen sind auf höchstens drei
begrenzt, Fallbackrollen wurden entfernt, und jede behaltene Rolle besitzt
mindestens einen Evidenzbeleg mit URL, exaktem Kurzquote und Abrufdatum.
Die Cross-Review-Felder bleiben absichtlich offen (verified_by: null,
review_status: primary_complete).
