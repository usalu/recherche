---
marp: true
theme: default
paginate: true
title: ReUse-Plattform für Stahlbeton — Vom Bestand zur bewerteten Entwurfsvariante
---

<!-- _paginate: false -->

# ReUse-Plattform für Stahlbeton

### Vom realen Bestandsbauteil zur bewerteten Entwurfsvariante

Eine durchgängige Werkzeugkette: **Einspeisen → Generieren → Katalogisieren → Entwerfen**

---

## Worum es geht

Wiederverwendung beginnt im Chaos: Fotos, grobe Maße, unvollständiges Wissen, unsichere Verfügbarkeit.

Diese Plattform übersetzt **reale Stahlbetonressourcen in nutzbare Entwurfsintelligenz** — nicht nur ein Inventar, sondern ein Arbeitsfluss.

```text
unsicherer Bestand  →  strukturierte Daten  →  planbare Objekte  →  bewertete Varianten
```

Leitprinzip durchgehend: **Unsicherheit nicht verstecken, sondern bearbeitbar machen.**

---

## Systemarchitektur — der Gesamtablauf

Zwei Schnittstellen, vier Bausteine.

```text
Interface 1 — Einspeiseplattform
  1.1  Bauteil-Seed      (reales Bauteil → strukturierter Startdatensatz)
  1.2  Generator         (Seed → planbares Bauteilobjekt mit 5 Ebenen)

Interface 2 — Design Tool
  2.1  Bauteilkatalog    (Objekte werden lesbar, filterbar, vergleichbar)
  2.2  Playground        (Bauteile werden zu Varianten komponiert & bewertet)
```

Jeder Schritt reichert an, ohne den Kontakt zum realen Bauteil zu verlieren.

---

<!-- _class: lead -->

# Interface 1
## Einspeiseplattform

Hier kommen reale Bauteile an: Fotos, Aufnahmen, Angebote, grobe Maße.
Die Unordnung des Wiederverwendens wird in eine erste strukturierte Sprache übersetzt.

---

## Bauteil-Seed — die kleinste sinnvolle Starteinheit

Der Seed ist **kein geprüftes Produkt und kein Bauteilpass**. Er ist der minimale, strukturierte Datensatz, der präzise genug ist, damit der Generator weiterarbeiten kann.

Er beantwortet die Grundfragen:

```text
Was ist das Bauteil?      Wie viele gibt es?      Wie groß sind sie?
Woraus bestehen sie?      Woher stammen sie?      Wann verfügbar?
Welche Rolle möglich?     Welche Evidenz liegt vor?
```

Schnittstelle zwischen **physischem Bestand** und **digitalem Entwurfsprozess**.

---

## Eingabeprozess

Der Einstieg: Bildmaterial + kurze Beschreibung + wenige Pflichtangaben.

> „Stahlbeton-Wandplatte aus einem Rückbau, ca. 18 Stück, 3,20 × 1,20 × 0,18 m,
> aus Fertigteilbau — tragend oder raumbildend prüfbar.“

Zwei Eingangswege:

```text
User Input          Bild (Foto/Scan) + Prompt + nur nicht-erkennbare Pflichtfelder
API / Import        Listing-ID, Quelle, Standort, Menge, Status, Verfügbarkeit
```

Das System extrahiert eine erste Lesart: Typologie, Menge, Maße, Material, Zustand, Quelle, Zielrolle.

---

## Bedienkonzept (UI Concept)

Geführter Prozess mit niedriger Einstiegshürde:

```text
1. Bild hochladen   2. Beschreiben   3. Systemvorschlag prüfen
4. Fehlendes ergänzen   5. Seed bestätigen
```

| Baustein | Funktion |
|---|---|
| **Minimaler Input** | wenige Felder genügen für den Start |
| **KI-Erkennung** | Vorschlag für Typologie, Maße, Öffnungen, Zustand, Rolle |
| **Formular-Interface** | Vorschläge bestätigen / korrigieren / ergänzen |
| **Nachweis-Panel** | Dokumente sammeln, Lücken sichtbar machen |

Jeder Wert trägt einen Status: **bestätigt · geschätzt · unbekannt.**

---

## Bauteil-Daten

Der Seed erzeugt zwei Arten von Daten — Wissen vs. Schätzung bleibt unterscheidbar.

```text
A. Mindestdaten zum Entwerfen
   Typologie, Menge, Hauptmaße, Material, Quelle,
   Verfügbarkeit, Zustand, Zielrolle, Datenvertrauen

B. Abgeleitete / angereicherte Daten
   Volumen, Masse, Fläche, Transportdistanz, CO₂-Wirkung,
   mögliche Ports, fehlende Nachweise, ReUse-Reifegrad
```

Die Mindestdaten markieren die Schwelle: von der vagen ReUse-Chance zum **planbaren Objekt**.

---

## Output: Bauteil-Seed

Ergebnis von Interface 1 — ein kompakter, generatorfähiger Datensatz.

```json
{
  "seed_id": "SEED-RC-WP-001",
  "typology": "WallPanel",
  "material_family": "ReinforcedConcrete",
  "quantity": 18,
  "geometry_hint": { "height_m": 3.2, "width_m": 1.2, "thickness_m": 0.18 },
  "source": { "type": "demolition_inventory", "location": "Basel" },
  "availability": { "status": "available_from", "date": "2027-Q2" },
  "target_role": ["spatial_partition", "structural_check_possible"],
  "missing_evidence": ["reinforcement_layout", "concrete_strength", "fire_resistance"],
  "ready_for_generator": true
}
```

---

<!-- _class: lead -->

# Generator
## Vom Seed zum planbaren Bauteilobjekt

Die Übersetzungsschicht zwischen unordentlichem Bestand und Entwurfslogik.

---

## Rolle des Generators

Aus den Grunddaten des Seeds erzeugt der Generator alle vorplanungsrelevanten Informationen — **nicht nur Geometrie**.

```text
Input:   Wandplatte, 18 Stück, 3,20 × 1,20 × 0,18 m, aus Rückbau
Output:  saubere Geometrie · Fläche · Volumen · Masse
         Auflager- & Anschlusskanten · strukturelle Vorprüfung
         CO₂-Schätzung · fehlende Nachweise · Ports & Connectoren
```

**Grammatiklogik:** jede Typologie hat eine eigene Generatorfamilie
(`HollowCoreSlabGenerator`, `RCWallPanelGenerator`, `RCBeamGenerator`, `RCColumnGenerator` …).

Der Generator ersetzt keine Fachplanung — er macht das Bauteil sofort nutzbar.

---

## Klassifikationslogik

Vier Ebenen verbinden Entwurfssprache und physische Realität:

```text
Typologie          breite Bauteilfamilie / Grammatik-Kategorie
                   (Slab, Beam, Column, Wall, Panel, Stair, FacadeSandwichPanel …)

Generatorgrammatik konkrete Erzeugungslogik innerhalb der Typologie
                   (HollowCoreSlab- vs. SolidRCSlab- vs. CutSlabSegmentGenerator)

Typ                Gruppe ähnlicher Pieces mit gemeinsamem Kontext
                   (z. B. „Hohlkörperdecke 7,20 × 1,20 m aus Spendergebäude A")

Piece              das tatsächliche physische Bauteil
                   (Herkunft, Zustand, Verfügbarkeit, Unsicherheit, Nachweise)
```

Entscheidend ist nicht *Fertigteil vs. Zuschnitt*, sondern **Herkunft vs. digitale Repräsentation**.

---

## Bauteil-Seed → generiertes Bauteilobjekt

Aus dem Seed entstehen **fünf parallele Planungsebenen** — gemeinsam gespeichert.

```text
Geometrie    saubere, planungsrelevante 2D/3D-Geometrie
Struktur     Achsen, Auflager, Spannrichtung, mögliche Tragrolle
Energie/CO₂  Masse, graue Emissionen, Hüllrelevanz, thermische Masse
Semantik     Ports & Connectoren, zulässige Rollen und Verbindungen
Evidence     Quelle, Piece-ID, Nachweise, Datenvertrauen, Verfügbarkeit
```

Das Bauteil wird damit nicht nur ein 3D-Objekt, sondern ein **planbares ReUse-Objekt** — jederzeit auf sein reales Gegenstück rückführbar.

---

<!-- _class: lead -->

# Interface 2
## Design Tool

Generierte Objekte stehen bereit. Die Frage verschiebt sich:
von *„Wie kommt ein Bauteil ins System?"* zu *„Wie wird es Teil eines Entwurfs?"*

---

## Bauteilkatalog — die Entwurfsbibliothek

Keine neutrale BIM-Bibliothek, keine reine Bauteilbörse, sondern eine **kuratierte Sammlung real verfügbarer ReUse-Bauteile**.

```text
Bauteilbörse:    Wo existiert ein reales Bauteil?
Generator:       Wie wird daraus ein planbares Objekt?
Bauteilkatalog:  Welche dieser Bauteile sind für meinen Entwurf relevant?
```

Drei Bausteine: **Bauteilkarte · Filterstruktur · Katalog-Aktionen.**

---

## Bauteilkarte

Zeigt ein Bauteil als ReUse-Objekt mit Herkunft, Menge, Reifegrad und Prüfstatus — in lesbaren Schichten:

| Ebene | Inhalt |
|---|---|
| **Visuell** | Foto · generierte Geometrie · schematische Abstraktion |
| **Daten** | Typologie, Menge, Maße, Material, Quelle, Verfügbarkeit, Datenvertrauen |
| **Reifegrad** | Idee → entwurfsfähig → prüfbedürftig → ausschreibungsnah → einbaufähig |
| **Prüfstatus** | offene Nachweise (Bewehrung, Druckfestigkeit, Brandschutz, Schadstoffe …) |

Der Reifegrad verhindert, dass ein unsicheres Bauteil wie ein fertiges Produkt wirkt.

---

## Filterstruktur

Filter sind **Entwurfsfragen**, keine Einkaufskategorien:

```text
Typologie / Typ      Welche Bauteilfamilie / Grammatik?
Geometrie            Maße, Raster, Spannweite, Öffnungen
Funktion             Was kann es HIER leisten? (tragend, raumbildend, Fassade …)
Semantik             Welche Ports / Connectoren sind kompatibel?
Tragwerk             mögliche Tragrolle, fehlende Statikdaten
Energie              Masse, Hüllrelevanz, thermische Masse, Dämmbedarf
Verfügbarkeit/Menge  sofort / ab Datum / reserviert · Serie vs. Einzelstück
Risiko / Nachweise   Datenvertrauen, offene Prüfungen
CO₂ / Transport      Masse, ReUse-Effekt, Distanz, Vergleich zum Neubau
```

Ziel ist nicht, Unsicheres auszuschließen — sondern Unsicherheit **sichtbar** zu machen.

---

## Katalog-Aktionen

Der Katalog bereitet den Wechsel in den Entwurfsraum vor.

```text
Auswählen / Vergleichen   nach Geometrie, Menge, Reifegrad, CO₂, Verfügbarkeit
Platzieren im Playground  Geometrie + Ports + Struktur + Evidence wandern mit
Reservieren / Anfrage     verfügbar · angefragt · reserviert · nicht mehr verfügbar
```

Die Reservierung ist **Teil der Entwurfssicherung** — sonst basiert der Entwurf auf Bauteilen, die später verschwinden können.

---

<!-- _class: lead -->

# Playground
## Der regelbasierte ReUse-Entwurfsraum

Aus Einzelbauteilen wird ein System. Aus dem Katalogobjekt wird eine Variante.

---

## Idee + Komposition · Target-Entwurf

Der Entwurf beginnt mit einer Zielvorstellung und einem **Target-Entwurf** — der Rahmen für alle Bewertungen:

```text
Nutzung · Gebäudetyp · ReUse-Ziel · Tragwerksstrategie
Raster & Geometrie · energetische Strategie · Projektanforderungen · Verfügbarkeit
```

Nicht das einzelne Bauteil steht im Mittelpunkt, sondern die **Übereinstimmung zwischen Entwurfszielen und verfügbaren Bauteilen**.

```text
Hohlkörperdecke allein:        Spannrichtung & Auflager bekannt, prüfbedürftig
Hohlkörperdecke im Playground: Liegt sie auf passenden Trägern? Passt die Spannweite?
                               Reicht die Menge? Entsteht ein sinnvolles Raster?
```

---

## Kompatibilitätsprüfung

Kompatibilität ist mehr als geometrische Passung — sechs Ebenen müssen plausibel sein:

```text
1 semantisch       dürfen diese Bauteilarten verbunden werden?
2 geometrisch      passen Maße, Achsen, Auflager, Toleranzen?
3 tragwerklich     ist der Lastabtrag plausibel?
4 energetisch      Hülle, Innenbauteil oder thermische Masse sinnvoll?
5 realwelt-basiert verfügbar, ausreichende Menge, reservierbar?
6 nachweisbezogen  sind fehlende Nachweise akzeptabel oder kritisch?
```

Regelquellen: **regelbasiert · energetisch · tragwerklich · realwelt-basiert · semantisch.**

Semantik verhindert Verbindungen, die nur entstehen, weil Bauteile geometrisch nahe liegen.

---

## Entwurfsfeedback

ReUse wird **während** der Entscheidung begleitet — nicht erst am Ende geprüft.

**Live-Warnungen:** fehlende Nachweise · Zeitkonflikte · riskante Verbindungen · unvollständige Mengen · Datenvertrauen.

**Visuelle Statuslogik:**

```text
Grün  plausibel    Gelb  prüfbedürftig    Orange  hohes Risiko
Rot   blockiert    Grau  Daten fehlen
```

**Variantenbewertung:** ReUse-Anteil · CO₂-Vergleich · System-Kompatibilität · Alternativvorschläge.
→ Unvollständige Mengen werden zum **Entwurfsparameter**, nicht zum Fehler.

---

## Export

Kein fertiges Ausführungspaket, sondern eine **dokumentierte, bewertete Entwurfsvariante** für die nächste Phase.

```text
Entwurfsvariante + Bauteilliste (Piece-IDs)
platzierte Bauteilgruppen + Connectoren
offene Nachweise + Prüfpfade
ReUse-Anteil + CO₂-Vorabschätzung
Verfügbarkeits- & Reservierungsstatus + Alternativvorschläge
```

Zeigt nicht nur, *wie* der Entwurf aussieht, sondern **auf welchen realen Bauteilen, Annahmen und Risiken er beruht**.

---

<!-- _class: lead -->

## Kernbotschaft

Die Plattform macht aus unsicherem Stahlbetonbestand **planbare, nachvollziehbare Entwurfsvarianten** — ohne die Unsicherheiten zu verstecken.

```text
Bestand  →  Seed  →  generiertes Objekt  →  Katalog  →  Variante
                  durchgehend mit Evidence Link zur realen Quelle
```
