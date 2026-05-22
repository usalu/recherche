# Präsentation: Schema für die Bauteilbörse

## 1. Ziel

Das Schema ordnet Informationen über wiederverwendbare Bauteile semantisch.

Es trennt Bauteilidentität, Inserat, Verfügbarkeit, Zustand, Risiko, Logistik, Dokumentation, Umweltwerte, technische Attribute und kontrollierte Vokabulare.

Kernprinzip:

> Eine Information gehört dorthin, wo sie fachlich entsteht.

---

## 2. Warum ein semantisches Schema?

Ein Bauteil ist nicht dasselbe wie ein Inserat.

Ein Preis ist keine dauerhafte Eigenschaft des Bauteils.

Ein Zustand ist nicht dasselbe wie ein Risiko.

Ein Stahlprofil braucht andere technische Felder als ein Fenster, ein Holzbauteil oder ein Betonbauteil.

Darum wird das Schema nicht als flache Tabelle gedacht, sondern als fachlicher Baum.

---

## 3. Hierarchie

```text
Domänenschema
  Entitätstyp
    Eigenschaft / Feld
      Attributgruppe
        Technisches Attribut
```

Für kontrollierte Vokabulare:

```text
Kontrolliertes Vokabularfeld
  Erlaubter Wert
```

---

## 4. Universelle Entitätstypen

```text
Item
= stabile Identität des Bauteils

Listing
= Inserat oder Quelle

AvailabilitySnapshot
= zeitbezogene Verfügbarkeit, Menge und Preis

Condition
= physischer Zustand

RiskAssessment
= Risiken und Unsicherheiten

Logistics
= Rückbau, Demontage und Transport

DocumentationAsset
= Fotos, Dateien und Nachweise

EnvironmentalData
= Umwelt- und Einsparwerte

TechnicalAttribute
= technische Eigenschaften je Kategorie
```

---

## 5. Kontrollierte Vokabulare

Kontrollierte Vokabulare definieren erlaubte Werte für Felder.

Sie machen Daten vergleichbar und verhindern freie Schreibvarianten.

Beispiele aus dem Schema:

```text
condition_normalized
  new
  like_new
  used_good
  damaged_repairable
  untested
  unknown

availability_status
  available
  reserved
  sold
  on_request
  unknown

risk_level
  low
  medium
  high
  critical
  unknown
```

Semantisch gilt:

```text
condition_normalized = kontrolliertes Vokabularfeld
used_good = erlaubter Wert
```

---

## 6. TechnicalAttribute

Technische Eigenschaften sind kategoriespezifisch.

Darum trennt `TechnicalAttribute` zwei Ebenen:

```text
record_fields
= Speicherlogik eines technischen Wertes

attribute_groups
= fachliche Attributpakete je Bauteilkategorie
```

Beispiele für Attributgruppen:

```text
Tragende Betonbauteile
Holz
Metall / Stahl
Fenster / Glas / Fassade
```

---

## 7. Beispiel Attributgruppen

```text
Tragende Betonbauteile
  concrete_type
  reinforcement_type
  compressive_strength_mpa
  carbonation_depth_mm
  chloride_content

Metall / Stahl
  metal_type
  steel_grade
  profile_type
  corrosion_level
  bolted_connections

Fenster / Glas / Fassade
  frame_material
  glazing_type
  u_value_w_m2k
  sound_reduction_db
  seal_condition
```

Diese Felder beschreiben technische Wiederverwendbarkeit, nicht das Inserat selbst.

---

## 8. Nutzen

Das Schema schafft:

- klare Bedeutung jedes Feldes
- bessere Vergleichbarkeit
- weniger Dubletten
- Trennung von Rohdaten und normalisierten Werten
- Erweiterbarkeit für neue Bauteilkategorien
- eine saubere Grundlage für Graph, Suche und Import

Kurz:

> Aus heterogenen Bauteildaten wird ein semantisch geordnetes Datenmodell.
