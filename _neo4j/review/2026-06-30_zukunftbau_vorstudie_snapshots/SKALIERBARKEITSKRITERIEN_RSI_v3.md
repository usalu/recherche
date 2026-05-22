# Skalierbarkeitskriterien — Reuse-Scalability Index (RSI v3)

> **Superseded:** Kanonische Methodik ist [**RSI v6**](SKALIERBARKEITSKRITERIEN_RSI_v6.md). v3-Scores sind historische Vergleichswerte und **nicht direkt** mit v6 vergleichbar (vgl. v6 §16.3).

**Stand:** 2026-07-01  
**Zweck:** Historische Referenz der v3-Bewertungskriterien (6 Dimensionen). Ergänzt die Forschungsanlage [`ANLAGE_Forschungssynthese_Plattform.md`](ANLAGE_Forschungssynthese_Plattform.md).

---

## 1. Begriff und Abgrenzung

### Was „skalierbar“ bedeutet

Ein Reuse-Ansatz gilt als **skalierbar**, wenn er **über den Einzelfall hinaus wiederholbar** ist — über Projekte, Regionen oder Bauteilfamilien hinweg — ohne dass jedes Mal dieselbe individuelle Bauteiljagd, Nachweislücke oder Einzelquelle neu gelöst werden muss.

### Was der RSI misst — und was nicht

| Misst der RSI | Misst der RSI nicht |
|---|---|
| Übertragbarkeit eines Projektansatzes als wiederholbares Modell | Architektonische Qualität allein |
| Bezug, Design-Methode, Nachweisreife, Maßstab, Tiefe, Wirkung | CO₂-Wirkung oder Fläche als Skalierungsersatz |
| Vergleichbarkeit von 83 internationalen Reuse-Projekten | Rentabilität oder Kosten (bewusst ausgelassen) |
| Transformationskapazität (Design-for-Disassembly) | Recycling-Quote ohne Element-Reuse-Kontext |

Gängige Zirkularitätskennzahlen (Material Circularity Indicator, Building Circularity Indicator, EU Level(s)) messen **Zustand und Wirkung**, nicht **Übertragbarkeit**. Der RSI schließt diese Lücke.

---

## 2. Index-Berechnung

### Formel

```
RSI = Σ (Gewichtᵢ × Scoreᵢ) / Σ (Gewichtᵢ)
```

- Jede **Dimension** wird auf **0–100** skaliert.
- Nur **belegte** Dimensionen fließen in den Nenner ein.
- **Konfidenz** (0–1) = Summe der Gewichte der vorhandenen Dimensionen.
- **Sortierung:** RSI absteigend, bei Gleichstand höhere Konfidenz bevorzugen.
- Konfidenz **< 0,6** = vorläufige Einschätzung.

### Gewichte und Begründung (Multi-Level-Perspective)

Skalierung eines Nischenansatzes ins Regime hängt zuerst an **Marktinfrastruktur** (Bezug) und **reproduzierbarer Technik/Design**; **Legitimation durch Evidenz** (Reife) ist der Durchsetzungshebel. Tiefe, Maßstab und Wirkung sind nachgelagerte Ergebnisgrößen.

| Dimension | Gewicht | Rolle in der Skalierungslogik |
|---|---:|---|
| Bezug & Reverse-Logistik | 22 % | Marktinfrastruktur — ohne Portfolio bleibt es Einzelfall |
| Zirkuläres Design / Transformationskapazität | 22 % | Reproduzierbare Bauweise als Methode |
| Informationsreife & Nachweis | 18 % | Legitimation und Planungssicherheit |
| Wiederverwendungstiefe & -umfang | 16 % | Tiefe allein ≠ Skalierung |
| Umweltwirkungs-Nachweis | 12 % | Landscape-Druck, Antragsreife |
| Maßstab | 10 % | Verlässt das Projekt den Reallabor-Maßstab? |

---

## 3. Die sechs Dimensionen — Kriterien und Scoring

### 3.1 Bezug & Reverse-Logistik (22 %)

**Frage:** Wie viele und wie diverse sind die dokumentierten Spenderquellen und Beschaffungswege?

| Eingabe | Beschreibung |
|---|---|
| Spenderzahl | Distinkte Spenderbauwerke oder Materialdepots |
| Beschaffungswege | Dokumentierte Wege (z. B. Börse, Direktbezug, Urban Mining, Community) |

**Score-Regel (0–100):**

```
Basis = 20 + 30 × log₂(Spenderzahl)
+ 5 Punkte bei ≥ 2 Beschaffungswegen
+ 10 Punkte bei ≥ 3 Beschaffungswegen
→ auf 0–100 begrenzt
```

**Interpretation:**

| Score-Bereich | Bedeutung |
|---|---|
| < 40 | Einzelquelle oder undokumentierter Bezug |
| 40–70 | Mehrere Quellen, noch kein Aggregator |
| ≥ 70 | Portfolio-Logik; Aggregator-Kandidat ab ≥ 5 Quellen |

**Aggregator-Schwelle:** ≥ 5 distinkte Spenderquellen.

---

### 3.2 Wiederverwendungstiefe & -umfang (16 %)

**Frage:** Wie tief und in welchem Geltungsbereich wird wiederverwendet?

| Eingabe | Beschreibung |
|---|---|
| `reuse_share` | Reuse-Quote in Prozent |
| `reuse_scope` | Geltungsbereich der Quote (Pflicht für Vergleichbarkeit) |
| Fallback | Tragende Bauteilgruppen, Anzahl Bauteilgruppen |

**Scope-Faktoren (`reuse_scope`):**

| Wert | Faktor | Beispiel |
|---|---:|---|
| `whole_building` | 1,0 | KA13: ~80 % am Gesamtgebäude |
| `structural` | 1,0 | Tragende Anteile |
| `facade` | 0,8 | Fassaden-Gewerk |
| `single_gewerk` | 0,75 | 55 GSS: 97 % Stahl ≠ 97 % Gebäude |
| `temporary_borrowed` | 0,9 | People's Pavilion: geliehen, nicht gekauft |
| nicht angegeben | 0,9 | Konservativ angenommen |

**Score-Regel:**

```
Mit Quote:  Score = reuse_share × Scope-Faktor  (max. 100)
Ohne Quote: Proxy aus tragenden Bauteilgruppen (55) und/oder Bauteilgruppenanzahl (bis 50)
```

**Wichtige Abgrenzung:** Recycling (Zuschlag, Downcycling) ≠ Element-Reuse. Upcycle Studios und ähnliche Fälle sind über scope und Materialpfad zu prüfen.

---

### 3.3 Maßstab (10 %)

**Frage:** Verlässt das Projekt den Reallabor-Maßstab?

| Eingabe | Beschreibung |
|---|---|
| `area_m2_gross` | Bruttogrundfläche in m² |

**Score-Regel (log-normiert):**

```
Bereich: 50 m² → 80.000 m²
Score = linear interpoliert auf Log-Skala, 0–100
```

| Fläche (Orientierung) | Score (ca.) |
|---:|---:|
| < 500 m² | Reallabor / Klein-Pilot |
| 500–5.000 m² | Mittlerer Maßstab |
| ≥ 5.000 m² | Großmaßstab-Demonstrator-Kandidat |

Großmaßstab allein erzeugt keine Skalierungslogik (z. B. Europa Building: viele Quellen, niedrige Transformationskapazität).

---

### 3.4 Zirkuläres Design / Transformationskapazität (22 %)

**Frage:** Ist die Bauweise demontierbar, austauschbar und als Methode reproduzierbar?

**Wissenschaftliche Verankerung:**

- **Durmisevic** — Independence + Exchangeability; reversibles Zerlegen ohne Beschädigung der Umgebung
- **DGBC/Alba-Concepts** — Disassembly Potential: Verbindungstyp, Zugänglichkeit, Unabhängigkeit, Bauteilkante; **schwächstes Glied** zählt
- **Brand** — Shearing Layers: Site, Structure, Skin, Services, Space, Stuff entkoppeln
- **ISO 20887** — Zugänglichkeit, Unabhängigkeit, Standardisierung

**Score-Regel aus Projektsignalen (0–100, Summe):**

| Signal | Punkte | Verankerung |
|---|---:|---|
| Anteil reversibler Verbindungen | bis 35 | Reversibel-Anteil × 35 (Verschraubung, Klemm, Steck, Bolzen vs. Schweißen, Mörtel, Kleben) |
| Zerstörungsarme Demontage | 20 (sonst 10 bei anderem Rückbau) | ISO 20887 Zugänglichkeit |
| Funktionswechsel belegt | 15 | Durmisevic Exchangeability |
| Vorfertigung / Trockenbau | 15 | Brand-Schichten; Prefab |
| ≥ 2 Gebäudeschichten | 8 | Brand Shearing Layers |
| ≥ 5 Bauteiltypen | 7 (≥ 2 Typen: 4) | ISO 20887 Standardisierung |

**Kappung und Referenz-Grad:**

- Graphisch abgeleitetes Design: **max. 90**
- Werte **> 90** nur mit verifizierter `design_quality` (z. B. People's Pavilion = 100: Zero-damage-Fügung mit Spanngurten, kein Schrauben/Kleben/Sägen)

**Kernlehre:** Design ≠ Skalierung. Perfektes DfD kann als Modell dennoch schlecht skalieren (`temporary_borrowed`, Einzelquelle).

---

### 3.5 Informationsreife & Nachweis (18 %)

**Frage:** Ist der Ansatz durch Daten, Nachweise und Zertifikate planungs- und marktfähig legitimiert?

| Signal | Punkte |
|---|---:|
| Kennwerte vorhanden | 30 |
| LCA dokumentiert | 20 |
| Zertifizierung | 15 |
| Nachweisanforderungen erfüllt | 20 |
| Zustandsklassen | 15 |
| **Maximum** | **100** |

Dokumentationslücken bei Materialpass und Zustandsklassen sind im Feld verbreitet — Reife ist oft der billigste Hebel zur „Antragsreife".

---

### 3.6 Umweltwirkungs-Nachweis (12 %)

**Frage:** Ist die ökologische Wirkung belegt?

| Eingabe | Score-Regel |
|---|---|
| CO₂-Reduktion in % | Prozent × 1,25 (max. 100) |
| CO₂-Einsparung in Tonnen (ohne %) | mindestens 55 |

CO₂-Nachweis stützt Legitimation, garantiert aber keine Übertragbarkeit.

---

## 4. Projekt-Archetypen

Archetypen ordnen Projekte nach **Skalierungslogik**, nicht nach Architekturpreis. Die Zuordnung erfolgt in dieser **Prioritätsreihenfolge**:

| Priorität | Archetyp | Regel | Skalierungsbedeutung |
|---:|---|---|---|
| 1 | **DfD-Referenz (Design-Vorbild)** | Design ≥ 92 (belegt) | Entwurfsreferenz — nicht automatisch skalierbar |
| 2 | **Aggregator** | ≥ 5 distinkte Spenderquellen | Reverse-Logistik als wiederholbares Bezugsmodell |
| 3 | **Großmaßstab-Demonstrator** | ≥ 5.000 m² und (Reuse ≥ 40 % oder Design ≥ 70 oder CO₂ ≥ 25 %) | Verlässt Pilotmaßstab |
| 4 | **Tiefen-Pilot** | Reuse ≥ 75 % und ≤ 1 Quelle | Maximale Tiefe, Einzelfund-Abhängigkeit |
| 5 | **System-Pilot** | Design ≥ 65 | Reproduzierbare, demontierbare Bauweise |
| 6 | **Klein-Pilot / Reallabor** | < 500 m² | Lernfall |
| 7 | **Fallstudie** | sonst / dünn dokumentiert | Aussagekraft begrenzt |

**Korpus-Verteilung (83 Projekte, Orientierung):** 7 Aggregatoren · 13 System-Piloten · 45 Fallstudien · übrige Archetypen s. Einzelfälle.

---

## 5. Verifikation und Datenqualität

### Zwei Ebenen

1. **Ersterfassung** — strukturierte Recherche über Akteure, Bauteilgruppen, Normen, Projektberichte
2. **Externe Verifikation** — 21 Projekte mit Projektquellen, Presse, Förder- und Nachweisberichten; Korrektur systematischer Fehler

### Typische Korrekturen in der Verifikation

| Fehlertyp | Beispiel | Konsequenz |
|---|---|---|
| Falsche Reuse-Quote | Ferme du Rail: „90 %" = biosourced + Reuse; reiner Element-Reuse ~15 % | Scope und Materialpfad prüfen |
| Fehlende Spenderzahl | Thoravej: Fläche und CO₂ ergänzt | Bezug vs. Wirkung trennen |
| Design ohne Zero-damage-Beleg | Graph-Score > 90 ohne Evidenz | Auf 90 kappen |
| Scope nicht angegeben | 97 %-Stahl vs. 80 %-Gebäude | `reuse_scope` Pflicht |

**62 von 83** Projekte stützen sich teilweise auf nicht extern verifizierte Erstauswertung — Konfidenz immer nennen.

### Kritische Selbstprüfung

| Prüfpunkt | Befund | Konsequenz |
|---|---|---|
| Design ≠ RSI | People's Pavilion Design 100, RSI Rang #2 | Dimensionen getrennt interpretieren |
| Groß ≠ skalierbar | Europa: 12 Quellen, niedrige TC | Aggregation ≠ Planungsreife |
| Scope ohne Angabe | Einzelgewerk-Quote als Gebäudequote | Tiefe verzerrt |
| Kein Kostensignal | Ökonomie uneinheitlich | RSI misst Skalierbarkeit, nicht Rentabilität |
| Recycling vs. Reuse | Betonzuschlag ≠ Element-Reuse | scope und Materialpfad unterscheiden |

---

## 6. Referenzwerte aus dem Korpus (83 Projekte)

| Kennzahl | Wert |
|---|---:|
| Median RSI | 46,9 |
| RSI Maximum | 79,8 (KA13, Oslo) |
| RSI Minimum | 0,0 (undokumentiert) |
| Echte Aggregatoren (≥ 5 Quellen) | 7 |
| Design-Dimension belegbar | 76/83 |
| Extern verifiziert | 21 |

**Kontrastpaare zur Kalibrierung:**

- **KA13 (#1)** ↔ **People's Pavilion (#2):** Skalierung braucht Bezug **und** Methode
- **Thoravej (Wirkung)** ↔ **KA13 (Wiederholbarkeit):** Einzelfall-Impact vs. übertragbares Modell
- **Recyclinghaus (Nachweis scheitert)** ↔ **55 GSS (Nachweis gelöst):** gleiche Herausforderung, unterschiedliche Folge

---

## 7. Grenzen des Rahmenwerks

1. **Design-Proxy** — Verbindungstyp und Rückbau nähern DGBC an; echte DP-Bewertung bräuchte Bauteil-für-Bauteil-Detaildaten
2. **Datenabhängigkeit** — Außerhalb der 21 verifizierten Projekte spiegeln Werte die Ersterfassung
3. **Kein Kostensignal** — RVI/BCR-Ökonomie bewusst ausgelassen; Erweiterungspunkt
4. **Kontextabhängigkeit** — Benchmarks sind Referenz, keine Checkliste
5. **Organisatorische Skalierung** — Vergabe, Leasing, Konsortium (Lot 01, Green House, ReCreate) nur indirekt im RSI erfasst

---

## 8. Wissenschaftliche Verankerung (Auswahl)

**Design / DfD:** Durmisevic (Transformation Capacity, Reversible Building Design); DGBC/Alba-Concepts Disassembly Potential; Brand (Shearing Layers); ISO 20887.

**Zirkularität / Bewertung:** EMF Material Circularity Indicator; EU Level(s); Küpfer/Brütting/Fivet MCDA (2021); Reuse Viability Index (2025); BCR-Feasibility (2026).

**Skalierung / Transition:** Geels (Multi-Level-Perspective); Reuse Market Dynamics (2024); Chalmers (2024, Reuse upscaling Sweden).

**Entwurfspraxis:** Brütting, Fivet, Senatore (EPFL) — *form follows availability*.

---

*Ende der Skalierbarkeitskriterien. RSI v3 — methodische Referenz für die Forschungsanlage zur Skalierbarkeit von Bauteil-Wiederverwendung.*
