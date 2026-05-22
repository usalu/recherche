# Regelchecks aus zwei hochgeladenen PDFs — neu analysiert

**Sprache:** Deutsch  
**Arbeitsweise:** Die englischen Regeltexte/Übersetzungen in den hochgeladenen PDFs wurden nicht übernommen. Die Ableitung basiert auf den sichtbaren deutschen Quellenabbildungen, Diagramm-Beschriftungen und Tabellen aus den eingebetteten Abbau/Aufbau-Handbuchseiten.  
**Quellen-PDFs:**

1. `component_connection_rules_one_page_per_rule.pdf` — 7 Seiten, eingebettete Quellen aus Abbau/Aufbau, gedruckte S. 166–179.  
2. `design_composition_rules_one_page_per_rule.pdf` — 10 Seiten, eingebettete Quellen aus Abbau/Aufbau, gedruckte S. 58–69, 89–91, 123–125, 165–167.

**Modellregel:**

```text
Repräsentation → Eigenschaften → Konnektor → Port → Port-Kompatibilität → Prüfung
```

- **Konnektor** = getypte Verbindungs- oder Beziehungsfunktion mit Eigenschaften.
- **Port** = konkrete anschließbare Schnittstelle innerhalb eines Konnektors.
- **Kompatibilität** = Port-zu-Port.
- Risiko-, Schadens-, Sperr- und Wärmebrückenzonen sind keine Konnektoren, außer sie stellen eine echte anschließbare Schnittstelle bereit.

---

# Teil A — Component Connection Rules

---

## A-01 — Allgemeine Anschlussregel / Ausführungsplanung

**PDF-Seite:** `component_connection_rules_one_page_per_rule.pdf`, Seite 1  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 166–167

### Exakte Textreferenz

```text
21. AUSFÜHRUNGSPLANUNG
```

```text
individuelle Anschlussdetails an angrenzende Bauteile (Bodenplatte, Wände, Stützen) müssen geplant werden
```

```text
ggf. müssen neue aussteifende Elemente errichtet werden, um die wiederverwendeten Stahlbetonelemente auszusteifen
```

### Eigene Ableitung

Die Quelle zeigt keine generische Verbindung, sondern eine Planungsanforderung: wiederverwendete Stahlbetonelemente benötigen individuelle Anschlussdetails an angrenzende Bauteile. Die Regel ist deshalb kein einzelner Bauteilanschluss, sondern eine globale Vorbedingung für alle späteren Konnektoren.

### Regelcheck

```text
Jede bauteilübergreifende Verbindung ist ungültig, bis ein konkreter Konnektor mit Ports, Eigenschaften und Nachweisstatus definiert ist.
```

### Repräsentation

```text
Bauteil A + Bauteil B + geplanter Anschlussbereich
```

### Minimale Konnektoren und Ports

| Konnektor | Ports | Bedeutung |
|---|---|---|
| `structural.bearing_support` | `bearing_side`, `support_side` | Lastabtrag / Auflager |
| `structural.restraint_fixing` | `fixing_side`, `receiving_side` | Verankerung / Aussteifung / Sicherung |
| `logistics.access_interface` | `component_access_side`, `site_access_side` | Montierbarkeit / Zugänglichkeit |

### Minimaler Check

```text
Anschlussdetail vorhanden?
Konnektor-Typ definiert?
Ports auf beiden Bauteilen vorhanden?
Port-Kompatibilität gegeben?
Zugänglichkeit für Montage vorhanden?
Aussteifung / Stabilität während Montage geklärt?
```

### Output

```text
pass | warning_missing_detail | blocked_no_connector
```

---

## A-02 — Fundament–Bodenplatte

**PDF-Seite:** `component_connection_rules_one_page_per_rule.pdf`, Seite 2  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 168–169

### Exakte Textreferenz

```text
Anschlüsse und Verbinder
```

```text
Fundament - Bodenplatte
```

```text
Befestigung mit Schraubankern
```

### Eigene Ableitung

Die Quelle zeigt einen Fundament-Bodenplatte-Anschluss mit Schraubankern. Die minimale Systemregel ist nicht „Schraubanker ist immer gültig“, sondern: Eine Boden-/Plattenkomponente kann nur dann an ein Fundament angeschlossen werden, wenn Auflager und Fixierung getrennt modelliert und anschließend gemeinsam geprüft werden.

### Regelcheck

```text
Eine Bodenplatte darf auf ein Fundament gesetzt werden, wenn ein Auflager-Konnektor und, falls erforderlich, ein Fixierungs-Konnektor mit kompatiblen Ports vorhanden sind.
```

### Repräsentation

```text
Fundament → 3D/2D Auflagerfläche
Bodenplatte → 2D Plattenfläche mit unterseitiger Auflagerzone
```

### Minimale Konnektoren und Ports

| Konnektor | Port am Fundament | Port an der Bodenplatte |
|---|---|---|
| `structural.bearing_support` | `support_side` | `bearing_side` |
| `structural.restraint_fixing` | `receiving_side` | `fixing_side` |
| `energy.penetration_seal` | `seal_side` | `penetration_side`, falls Durchdringung der Abdichtung |

### Eigenschaften des Konnektors

```yaml
structural.restraint_fixing:
  method_family: [screw_anchor]
  drilling_required: true
  edge_distance_required: true
  waterproofing_relevant: true
```

### Minimaler Check

```text
Auflagerfläche vorhanden?
Bodenplatte liegt geometrisch auf Fundament?
Schraubankerzone innerhalb erlaubter Bohrbereiche?
Fundament kann Ankerkräfte aufnehmen?
Abdichtung / Feuchteebene nicht unkontrolliert durchdrungen?
Montagezugang für Anker vorhanden?
```

### Output

```text
pass | warning_waterproofing_detail | blocked_no_support | blocked_no_drill_zone
```

---

## A-03 — Bodenplatte–Wand

**PDF-Seite:** `component_connection_rules_one_page_per_rule.pdf`, Seite 3  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 170–171

### Exakte Textreferenz

```text
Bodenplatte - Wand
```

```text
Befestigung über nachträglich montierte Edelstahldorne
```

```text
Befestigung über Winkelverbinder
```

```text
Winkelverbinder müssen aus Brandschutzgründen durch den FB-Aufbau verdeckt werden.
```

### Eigene Ableitung

Die Quelle zeigt zwei Varianten: Edelstahldorne und Winkelverbinder. Beide Varianten lösen nicht das gleiche Problem wie reines Auflager: Die Wand steht auf der Platte und muss gegen Verschieben, Kippen oder Abheben gesichert werden. Brandschutz ist bei Winkelverbindern Teil der Anschlussbedingung.

### Regelcheck

```text
Eine Wand darf auf einer Bodenplatte stehen, wenn ein tragfähiges Auflager und ein Fixierungs-/Sicherungs-Konnektor mit kompatiblen Ports vorhanden sind.
```

### Repräsentation

```text
Bodenplatte → 2D Plattenfläche mit oberseitiger Support-Zone
Wand → 2D Wandfläche mit unterer Bearing-Zone
```

### Minimale Konnektoren und Ports

| Konnektor | Port Bodenplatte | Port Wand |
|---|---|---|
| `structural.bearing_support` | `support_side` | `bearing_side` |
| `structural.restraint_fixing` | `receiving_side` | `fixing_side` |
| `logistics.support_interface` | `base_support_side` | `component_support_side` |

### Eigenschaften des Konnektors

```yaml
structural.restraint_fixing:
  method_family: [dowel, angle_connector]
  drilling_required: true
  rebar_evidence_required: true
  fire_relevant: true
```

### Minimaler Check

```text
Wandfuß hat ausreichende Auflagerzone?
Wand steht lotrecht auf der Support-Zone?
Dorne/Winkel liegen in erlaubten Rand- und Bohrzonen?
Brandschutzabdeckung für Winkelverbinder vorhanden?
Temporäre Aussteifung während Montage möglich?
Toleranzausgleich am Wandfuß definiert?
```

### Output

```text
pass | warning_fire_cover_required | warning_temporary_bracing | blocked_no_bearing | blocked_rebar_unknown
```

---

## A-04 — Bodenplatte–Stütze

**PDF-Seite:** `component_connection_rules_one_page_per_rule.pdf`, Seite 4  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 172–173

### Exakte Textreferenz

```text
Bodenplatte - Stütze
```

```text
Befestigung über nachträglich montierten Edelstahldorn
```

```text
Befestigung über Winkelverbinder
```

```text
Winkelverbinder müssen aus Brandschutzgründen durch den FB-Aufbau verdeckt werden.
```

### Eigene Ableitung

Die Quelle zeigt eine punktförmige vertikale Komponente auf einer Platte. Daher ist die abstrakte Regel nicht dieselbe wie Wand–Platte: Hier wird eine lokale Punkt-/Flächenauflagerung mit Zentrierung, Exzentrizität und temporärer Stabilisierung geprüft.

### Regelcheck

```text
Eine Stütze darf auf einer Bodenplatte stehen, wenn lokale Auflagerfläche, vertikale Ausrichtung und Fixierung gegen horizontale Verschiebung/Kippen definiert sind.
```

### Repräsentation

```text
Stütze → 1D vertikales Linienelement mit Fußpunkt und Fußfläche
Bodenplatte → 2D Plattenfläche mit lokaler Support-Patch-Zone
```

### Minimale Konnektoren und Ports

| Konnektor | Port Bodenplatte | Port Stütze |
|---|---|---|
| `structural.bearing_support` | `support_side` | `bearing_side` |
| `structural.node_joint` | `joint_side` | `joint_side` |
| `structural.restraint_fixing` | `receiving_side` | `fixing_side` |
| `logistics.fixation_interface` | `fixation_tool_side` | `component_fixing_side` |

### Eigenschaften des Konnektors

```yaml
structural.bearing_support:
  support_mode: point
  load_type: compression
  eccentricity_relevant: true

structural.restraint_fixing:
  method_family: [dowel, angle_connector]
  drilling_required: true
  fire_relevant: true
```

### Minimaler Check

```text
Stützenfuß hat ausreichend lokale Bearing-Zone?
Last liegt innerhalb zulässiger Exzentrizität?
Fixierung kann Querkräfte / Montagezustand aufnehmen?
Bohrbereiche und Bewehrungslage bekannt?
Brandschutzabdeckung für Winkelverbinder vorhanden?
Temporäre Aussteifung möglich?
```

### Output

```text
pass | warning_eccentricity | warning_fire_cover_required | blocked_no_local_bearing | blocked_no_bracing
```

---

## A-05 — Wand–Decke

**PDF-Seite:** `component_connection_rules_one_page_per_rule.pdf`, Seite 5  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 174–175

### Exakte Textreferenz

```text
Wand - Decke
```

```text
Befestigung über nachträglichen Bewehrungsanschluss und Verguss
```

```text
Befestigung über Schraubanker mit Flachstahlhalter
```

### Eigene Ableitung

Die Quelle zeigt Wand–Decke als linienförmige Unterstützung einer horizontalen Platte. Der Hauptkonnektor ist deshalb zuerst ein Auflager-Konnektor. Bewehrungsanschluss, Verguss, Schraubanker und Flachstahlhalter sind Varianten des Fixierungs-/Sicherungs-Konnektors.

### Regelcheck

```text
Eine Decke darf auf einer Wand aufliegen, wenn die Wand eine durchgehende Support-Linie anbietet und die Decke eine kompatible Bearing-Kante besitzt.
```

### Repräsentation

```text
Wand → 2D Wandfläche mit oberer Linien-Support-Zone
Decke → 2D Plattenfläche mit Kanten-Bearing-Zone
```

### Minimale Konnektoren und Ports

| Konnektor | Port Wand | Port Decke |
|---|---|---|
| `structural.bearing_support` | `support_side` | `bearing_side` |
| `structural.restraint_fixing` | `receiving_side` | `fixing_side` |
| `semantic.alignment_relation` | `alignment_side` | `alignment_side` |
| `logistics.access_interface` | `component_access_side` | `component_access_side` |

### Eigenschaften des Konnektors

```yaml
structural.bearing_support:
  support_mode: line
  min_bearing_length_mm: unknown

structural.restraint_fixing:
  method_family: [post_installed_rebar, grout, screw_anchor, flat_steel_holder]
  rebar_evidence_required: true
  fire_relevant: true
```

### Minimaler Check

```text
Decken-Spannrichtung passt zur Wand-Support-Linie?
Auflagerlänge und Auflagerbreite ausreichend?
Fixierung gegen Verschieben / Abheben / Horizontalkräfte geklärt?
Verguss- oder Trockenfuge definiert?
Einbauzugang zu Anker-/Bewehrungszonen vorhanden?
Fugenanforderungen für Brandschutz, Schallschutz oder Akustik geklärt?
```

### Output

```text
pass | warning_joint_detail | warning_fire_acoustic | blocked_no_support_line | blocked_no_access
```

---

## A-06 — Stütze–Decke, direkter Punktauflager-Fall

**PDF-Seite:** `component_connection_rules_one_page_per_rule.pdf`, Seite 6  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 176–177

### Exakte Textreferenz

```text
Stütze - Decke
```

```text
Befestigung über nachträglich montierten Edelstahldorn
```

```text
Befestigung über Winkelverbinder
```

```text
Winkelverbinder müssen mit einer Brandschutzbekleidung verdeckt werden.
```

### Eigene Ableitung

Die Quelle zeigt Decke auf Stütze. Das ist kein normales Linienauflager, sondern ein lokales Punktauflager. Daher müssen lokale Lagerpressung, Durchstanzen bzw. lokale Lastkonzentration und horizontale Sicherung geprüft werden.

### Regelcheck

```text
Eine Decke darf direkt auf einer Stütze liegen, wenn die Decke für lokale Punktauflagerung geeignet ist oder ein zusätzlicher Lastverteil-/Auflagerkörper vorhanden ist.
```

### Repräsentation

```text
Stütze → 1D vertikales Linienelement mit Kopfpunkt und Kopfauflagerfläche
Decke → 2D Plattenfläche mit lokaler Bearing-Patch-Zone
```

### Minimale Konnektoren und Ports

| Konnektor | Port Stütze | Port Decke |
|---|---|---|
| `structural.bearing_support` | `support_side` | `bearing_side` |
| `structural.node_joint` | `joint_side` | `joint_side` |
| `structural.restraint_fixing` | `receiving_side` | `fixing_side` |
| `logistics.support_interface` | `base_support_side` | `component_support_side` |

### Eigenschaften des Konnektors

```yaml
structural.bearing_support:
  support_mode: point
  punching_relevant: true
  local_bearing_relevant: true

structural.restraint_fixing:
  method_family: [dowel, angle_connector]
  fire_relevant: true
```

### Minimaler Check

```text
Stützenkopf bietet ausreichende Auflagerfläche?
Decke ist für Punktauflager geeignet oder erhält Lastverteilung?
Durchstanzen / lokale Pressung als Nachweisstatus markiert?
Horizontaler Halt / Verschiebesicherung definiert?
Brandschutzbekleidung für Winkelverbinder vorhanden?
Temporäre Unterstützung während Montage geklärt?
```

### Output

```text
pass | warning_punching_check_required | warning_fire_cladding | blocked_no_point_support | blocked_no_load_distribution
```

---

## A-07 — Stütze–Decke über Adapterträger

**PDF-Seite:** `component_connection_rules_one_page_per_rule.pdf`, Seite 7  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 178–179

### Exakte Textreferenz

```text
Stütze - Decke
```

```text
Befestigung über nachträglichen Bewehrungsanschluss und Verguss auf neu herzustellenden Stahlbetonträger
```

```text
Befestigung über Auflager auf Stahlträger
```

### Eigene Ableitung

Die Quelle zeigt keine direkte Stütze–Decke-Verbindung, sondern eine vermittelnde Trägerlösung. Der Träger ist ein Adapter zwischen Stütze und Decke. Der Regelcheck muss daher aus zwei Anschlüssen bestehen: Stütze–Träger und Träger–Decke.

### Regelcheck

```text
Wenn direkte Punktauflagerung nicht geeignet ist, muss ein Adapterträger als eigener Bauteiltyp mit eigenen Ports und Nachweisen zwischen Stütze und Decke eingefügt werden.
```

### Repräsentation

```text
Stütze → 1D vertikales Linienelement
Adapterträger → 1D Trägerelement mit Auflagerlinie
Decke → 2D Plattenfläche mit Kanten- oder Flächen-Bearing-Zone
```

### Minimale Konnektoren und Ports

| Verbindung | Konnektor | Ports |
|---|---|---|
| Stütze–Träger | `structural.node_joint` oder `bearing_support` | `joint_side` ↔ `joint_side` / `support_side` ↔ `bearing_side` |
| Träger–Decke | `structural.bearing_support` | `support_side` ↔ `bearing_side` |
| Adapter-Sicherung | `structural.restraint_fixing` | `fixing_side` ↔ `receiving_side` |
| Brandschutz / Hülle | `energy.layer_continuity`, falls relevant | `layer_side` ↔ `layer_side` |

### Eigenschaften des Konnektors

```yaml
structural.bearing_support:
  support_mode: line
  adapter_element: true

structural.node_joint:
  node_type: beam_column_or_support_node

structural.restraint_fixing:
  method_family: [post_installed_rebar, grout, steel_support]
```

### Minimaler Check

```text
Adapterträger passt geometrisch in Raster und Raumhöhe?
Träger kann Last von Decke aufnehmen und zur Stütze übertragen?
Stütze–Träger-Detail definiert?
Decke–Träger-Auflager definiert?
Brandschutz des Stahlträgers oder Betondetails geklärt?
Adaptermaterial begründet und möglichst reduziert?
Spätere Demontierbarkeit nicht ausgeschlossen?
```

### Output

```text
pass | warning_adapter_required | warning_fire_protection | blocked_no_beam_capacity | blocked_no_adapter_detail
```

---

# Teil B — Design Composition Rules

---

## B-01 — Programm, Grundstück, Bestand und erste Planhypothese

**PDF-Seite:** `design_composition_rules_one_page_per_rule.pdf`, Seite 1  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 58–59

### Exakte Textreferenz

```text
Zunächst sollte eine grobe Skizze eines Grundrisses für den Neubau aus dem vorliegenden Raumprogramm erstellt werden.
```

```text
Das im Kapitel 3 erstellte 3D-Modell und die 2D-Grundrisse sollten nun genauer auf ihre Zerlegbarkeit hin untersucht werden.
```

```text
Der erste Zuschnittplan sollte zudem einem System folgen, dass den Transport schon mitdenkt.
```

### Eigene Ableitung

Die Quelle beschreibt keinen freien Entwurfsstart. Sie verbindet Raumprogramm, Standortbedingungen, Bestand/3D-Modell und Transportfähigkeit. Für unser Pool-System bedeutet das: Der Entwurf startet als Hypothese, die sofort gegen die verfügbaren Bauteile und deren Abstraktionen getestet wird.

### Regelcheck

```text
Ein erster Entwurf ist nur eine Hypothese, bis Programm, Standortgrenzen und verfügbare Bauteilabstraktionen gegeneinander geprüft wurden.
```

### Repräsentation

```text
Programm → Raum-/Nutzungsanforderungen
Standort → Baufeld, Abstände, Höhen, Erschließung
Bauteilpool → verfügbare Typen, Größen, Massen, Transportgrenzen
```

### Konnektoren / Ports

Keine bauteilbezogenen Ports. Diese Regel erzeugt noch keine physische Verbindung. Sie erzeugt Such- und Eignungsfilter für spätere Bauteil-Konnektoren.

### Minimaler Check

```text
Raumprogramm in Flächen, Spannweiten und Raumhöhen übersetzt?
Standortgrenzen vor Bauteilplatzierung bekannt?
Pool nach passenden Typen und Dimensionen abgefragt?
Transportgrenzen als harte oder weiche Bedingung markiert?
Nicht abgedeckte Nutzungen als Adapter-/Neubaubereich markiert?
```

### Output

```text
program_pool_match | warning_gap | blocked_no_feasible_pool_basis
```

---

## B-02 — Raster aus wiederholbaren Bauteilen

**PDF-Seite:** `design_composition_rules_one_page_per_rule.pdf`, Seite 2  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 60–61

### Exakte Textreferenz

```text
grundlegendes Konzept
```

```text
einzelnen Stützen und einzelnen Deckenplatten
```

```text
Stützenpaaren mit verbindendem Unterzug
```

```text
festen Raster
```

### Eigene Ableitung

Die Quelle macht aus wiederholbaren Elementen ein Grundkonzept. Für den bereits vorhandenen Pool ist das kein Zuschnittproblem, sondern eine Raster-Extraktion: Häufige Längen, Breiten, Höhen und Stützabstände erzeugen die primäre Ordnung des Entwurfs.

### Regelcheck

```text
Das Haupt-Raster muss aus wiederholbaren und strukturell brauchbaren Pool-Dimensionen abgeleitet werden.
```

### Repräsentation

```text
Pool-Dimensionen → Cluster
Cluster → Rasterkandidaten
Rasterkandidat → mögliche Bay-/Raumstruktur
```

### Konnektoren / Ports

| Konnektor | Ports | Bedeutung |
|---|---|---|
| `semantic.alignment_relation` | `alignment_side` ↔ `alignment_side` | Raster-/Achsfortsetzung |
| `structural.bearing_support` | `bearing_side` ↔ `support_side` | nur bei strukturellem Raster relevant |

### Minimaler Check

```text
Wiederholte Plattenmaße geclustert?
Wand-/Stützenhöhen geclustert?
Tragfähige Spannweiten aus Clustern ableitbar?
Raster nutzt häufige statt seltene Dimensionen?
Sondermaße an Rand-, Service- oder Adapterzonen verschoben?
```

### Output

```text
valid_grid_candidate | warning_low_repetition | blocked_no_dominant_grid
```

---

## B-03 — Bay-Grammatik als räumliche Ordnung

**PDF-Seite:** `design_composition_rules_one_page_per_rule.pdf`, Seite 3  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 60–61

### Exakte Textreferenz

```text
einzelnen Stützen und einzelnen Deckenplatten
```

```text
Stützenpaaren mit verbindendem Unterzug
```

```text
wieder einsetzten zu können
```

### Eigene Ableitung

Die Quelle zeigt unterschiedliche Grundfiguren. Diese sind nicht nur Tragwerksvarianten, sondern erzeugen unterschiedliche Raumtypen. In unserem System sollen deshalb Bauteilkombinationen zuerst als abstrakte Bay-Typen gelesen werden, bevor konkrete Räume festgelegt werden.

### Regelcheck

```text
Eine Bauteilkombination muss als Bay-Typ klassifiziert werden, bevor sie als Raumstruktur verwendet wird.
```

### Repräsentation

```text
W + S → wandgetragenes Feld / zelliger oder linearer Raum
C + S → punktgestütztes Feld
C + B + S → Rahmen- oder Adapterfeld
W + W → Kern / Zelle / Aussteifungszone
```

### Konnektoren / Ports

| Bay-Typ | Notwendige Konnektoren | Ports |
|---|---|---|
| `W + S` | `bearing_support` | Wand `support_side`, Decke `bearing_side` |
| `C + S` | `bearing_support`, ggf. `restraint_fixing` | Stütze `support_side`, Decke `bearing_side` |
| `C + B + S` | `node_joint`, `bearing_support` | Stütze/Träger `joint_side`, Träger/Decke `support_side`/`bearing_side` |
| `W + W` | `boundary_relation`, ggf. `restraint_fixing` | `boundary_side`, `fixing_side`/`receiving_side` |

### Minimaler Check

```text
Bay-Typ eindeutig klassifiziert?
Räumliche Wirkung passt zur Nutzung?
Strukturelle Ports sind im Bay-Typ vorhanden?
Wiederholung möglich?
Sonder-Bays bleiben Ausnahme und werden markiert?
```

### Output

```text
valid_bay_type | warning_spatial_mismatch | blocked_no_structural_ports
```

---

## B-04 — Platzieren, Abweichung erkennen, Iteration erzwingen

**PDF-Seite:** `design_composition_rules_one_page_per_rule.pdf`, Seite 4  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 62–63

### Exakte Textreferenz

```text
Die im ersten Zuschnittplan erstellten Elemente müssen nun auf der Grundrissskizze des Neubaus platziert werden.
```

```text
Dafür muss festgestellt werden, an welchen Stellen von der Skizze abgewichen wird.
```

```text
mehrfach wiederholt werden
```

### Eigene Ableitung

Die Quelle beschreibt einen iterativen Abgleich zwischen geplanten Elementen und Grundriss. Für unseren Ansatz ohne Zuschnitt bedeutet das: echte Pool-Elemente werden mit ID platziert; jede Abweichung wird als Konfliktobjekt sichtbar gemacht.

### Regelcheck

```text
Eine Komposition ist erst prüfbar, wenn alle platzierten Bauteile konkrete IDs haben und Abweichungen als Konflikte dokumentiert sind.
```

### Repräsentation

```text
Layout → platzierte Pieces mit IDs
Konflikt → Abweichung zwischen Plan, Bauteilgeometrie und Anschlusslogik
Iteration → Entscheidung: Plan ändern, Bauteil ersetzen, Adapter einfügen, Zone umwidmen
```

### Konnektoren / Ports

Keine neuen Konnektoren. Diese Regel prüft, ob bestehende Konnektoren nach der Platzierung überhaupt erreichbar und kompatibel bleiben.

### Minimaler Check

```text
Alle Elemente mit ID platziert?
Abweichungen explizit markiert?
Jeder Konflikt hat Entscheidungspfad?
Adapterzonen lokalisiert?
Nach Änderung erneut strukturell und räumlich geprüft?
```

### Output

```text
iteration_complete | warning_unresolved_conflicts | blocked_generic_elements
```

---

## B-05 — Verbinder / Adapter als Entwurfsmittel

**PDF-Seite:** `design_composition_rules_one_page_per_rule.pdf`, Seite 5  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 62–63

### Exakte Textreferenz

```text
Konzept entwickelt werden, wie die gebrauchten Elemente wieder zusammengefügt werden können.
```

```text
neue Auflager aus Stahlträgern oder Stahlbetonfertigteilen
```

```text
für einen zukünftigen Rückbau demontierbar
```

### Eigene Ableitung

Die Quelle fordert ein Konzept des Wieder-Zusammenfügens und erwähnt neue Auflager. Daraus folgt: Adapter sind nicht Fehler, sondern kontrollierte Vermittler zwischen nicht perfekt passenden Reuse-Bauteilen.

### Regelcheck

```text
Jede nicht direkt lösbare A–B-Beziehung muss als A–X–B modelliert werden, wobei X ein Adapter, Auflager, Verbinder oder Toleranzelement ist.
```

### Repräsentation

```text
A → bestehendes Bauteil
B → bestehendes Bauteil
X → neues / ergänzendes Adapterelement oder Anschlussdetail
```

### Konnektoren / Ports

| Relation | Konnektor | Ports |
|---|---|---|
| A–X | `bearing_support`, `node_joint` oder `restraint_fixing` | A-Port ↔ X-Port |
| X–B | `bearing_support`, `node_joint` oder `restraint_fixing` | X-Port ↔ B-Port |
| Demontierbarkeit | Eigenschaft des Konnektors | `demountable: true/false/unknown` |

### Minimaler Check

```text
Adapter X konkret benannt?
Adapter besitzt eigene Repräsentation und Ports?
A–X und X–B separat prüfbar?
Toleranz über X gelöst, nicht durch geometrisches Erzwingen?
Demontierbarkeit als Eigenschaft gesetzt?
Neumaterialmenge begründet?
```

### Output

```text
valid_adapter_strategy | warning_adapter_overuse | blocked_missing_X
```

---

## B-06 — Bauteilkatalog als Entwurfsinventar

**PDF-Seite:** `design_composition_rules_one_page_per_rule.pdf`, Seite 6  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 89–91

### Exakte Textreferenz

```text
individueller Bauteilkatalog mit individueller Kennzeichnung der Elemente
```

```text
ID
```

```text
Maße
```

```text
Öffnungsmaße
```

```text
Volumen
```

```text
Masse
```

```text
Tracking + Tracing
```

### Eigene Ableitung

Die Quelle macht den Katalog zur Grundlage von Logistik, Lagerung und Wiedereinbau. Für den Entwurf bedeutet das: Ein Element darf nicht als anonymer Typ platziert werden, sondern nur als konkrete Piece-ID mit passbezogenen Daten.

### Regelcheck

```text
Ein planbares Bauteil muss als katalogisierte Piece-ID mit Geometrie-, Masse-, Öffnungs-, Status- und Portdaten vorliegen.
```

### Repräsentation

```text
Katalogeintrag → Piece
Piece → Typologie + Geometrie + Paket-Repräsentationen + Konnektoren/Ports + Evidenzstatus
```

### Konnektoren / Ports

Keine neuen Konnektoren; der Katalog speichert die Konnektoren/Ports der Package-Repräsentationen.

### Minimaler Check

```text
Jedes platzierte Element hat eindeutige ID?
Typ, Maße, Volumen und Masse vorhanden?
Öffnungen und Randbedingungen sichtbar?
Konnektoren/Ports paketweise erzeugt oder als fehlend markiert?
Evidenzstatus für strukturelle Nutzung bekannt?
Ähnliche Bauteile werden nicht ohne Passprüfung ersetzt?
```

### Output

```text
catalogue_ready | warning_missing_pass_data | blocked_no_id
```

---

## B-07 — Raumzonierung und Aufnahme von Reststücken

**PDF-Seite:** `design_composition_rules_one_page_per_rule.pdf`, Seite 7  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 62–63

### Exakte Textreferenz

```text
an welchen Stellen von der Skizze abgewichen wird
```

```text
mehrfach wiederholt werden
```

```text
Konzept entwickelt werden, wie die gebrauchten Elemente wieder zusammengefügt werden können.
```

### Eigene Ableitung

Die Quelle spricht über Abweichungen und Iteration. Daraus lässt sich eine Zonenregel ableiten: Der Entwurf muss unterscheiden, wo saubere Wiederholung nötig ist und wo Abweichungen, Restmaße oder Sonderstücke produktiv aufgenommen werden können.

### Regelcheck

```text
Hauptnutzungen sollen aus den stabilsten wiederholbaren Bay-Typen entstehen; Reststücke und Sonderteile werden bewusst Neben-, Puffer- oder Servicezonen zugeordnet.
```

### Repräsentation

```text
Bauteilqualität → strukturell / räumlich / logistich
Raumzone → Hauptzone / Nebenzone / Servicezone / Pufferzone / Randzone
Zuordnung → Piece-ID zu Raumzone
```

### Konnektoren / Ports

| Konnektor | Ports | Bedeutung |
|---|---|---|
| `semantic.boundary_relation` | `boundary_side` ↔ `boundary_side` | Raumgrenzen |
| `semantic.alignment_relation` | `alignment_side` ↔ `alignment_side` | Raster / Fuge / Ordnung |
| `structural.bearing_support` | `bearing_side` ↔ `support_side` | nur bei tragenden Zonen |

### Minimaler Check

```text
Bauteile nach räumlicher und struktureller Qualität bewertet?
Beste wiederholbare Bauteile in Hauptzonen?
Irreguläre / beschädigte / kurze Bauteile in Toleranzzonen?
Restflächen bewusst programmiert?
Primärräume nicht von vielen Einzelausnahmen abhängig?
```

### Output

```text
valid_zoning | warning_too_many_exceptions | blocked_primary_room_conflict
```

---

## B-08 — Gebäudehülle und TGA als Pufferstrategie

**PDF-Seite:** `design_composition_rules_one_page_per_rule.pdf`, Seite 8  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 123–125

### Exakte Textreferenz

```text
Bei der Wiederverwendung von Stahlbeton sind die Anforderungen zum Wärmeschutz nur dann besonders zu beachten
```

```text
Kontakt zum Außenklima (Außenluft oder Baugrund)
```

```text
Bestimmung des Wärmedurchgangskoeffizienten für die wiederverwendeten Stahlbetonelemente
```

```text
Stahlbetonwand (200mm, wiederverwendet, Wärmeleitwert ist anzunehmen oder festzustellen)
```

### Eigene Ableitung

Die Quelle bindet Energieanforderungen an Außenklima, Dach, Außenwand und Baugrund. Für die Komposition bedeutet das: Die wiederverwendete Struktur muss nicht automatisch die endgültige Wetterlinie sein. Hülle, Dämmung, Service- und Pufferschichten können zwischen unregelmäßiger Struktur und äußerer Gebäudegrenze vermitteln.

### Regelcheck

```text
Wenn wiederverwendete Stahlbetonbauteile eine Hüllrolle bekommen, muss ein vollständiges Boundary-/Layer-Modell mit Dämmung, Feuchte und Durchdringungen vorhanden sein.
```

### Repräsentation

```text
Strukturfeld → wiederverwendete Bauteile
Hüllenlinie → thermische / wasserführende / luftdichte Grenze
Pufferzone → Dämmung, Fassade, Installationsraum, Dachaufbau, Bodenaufbau
```

### Konnektoren / Ports

| Konnektor | Ports | Bedeutung |
|---|---|---|
| `energy.boundary_continuity` | `boundary_side` ↔ `boundary_side` | durchgehende Hüllgrenze |
| `energy.layer_continuity` | `layer_side` ↔ `layer_side` | Dämm-/Schutzschicht |
| `energy.penetration_seal` | `penetration_side` ↔ `seal_side` | Durchdringungen abdichten |
| `tga.route_connection` | `route_side` ↔ `route_side` | Services geführt, nicht zufällig gebohrt |

### Minimaler Check

```text
Bauteil hat Hüllrolle oder nicht?
Außenklima/Baugrund/Dachkontakt markiert?
Dämm- oder Schutzschicht als eigene Layer-Repräsentation vorhanden?
U-Wert nur für vollständigen Aufbau gerechnet?
Durchdringungen über geplante Ports geführt?
Unregelmäßige Bauteilkanten durch Pufferzone aufgenommen?
```

### Output

```text
not_applicable | pass | warning_missing_layer | blocked_envelope_without_boundary_model
```

---

## B-09 — Remontagezeichnungen als Entwurfsoutput

**PDF-Seite:** `design_composition_rules_one_page_per_rule.pdf`, Seite 9  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 69

### Exakte Textreferenz

```text
MILESTONE 3
```

```text
GEBÄUDEENTWURF
```

```text
Darstellungen des Zuschnitts und des Remontagekonzepts der geborgenen Elemente im Neubau
```

### Eigene Ableitung

Die Quelle nennt den Gebäudeentwurf als Meilenstein und verlangt neben typischen Zeichnungen auch Darstellungen von Zuschnitt und Remontagekonzept. In unserem Ansatz entfällt Zuschnitt als Entwurfsschritt; zwingend bleibt aber die Remontage-/Kompositionslogik mit ID, Sequenz und Anschlussdetails.

### Regelcheck

```text
Ein Entwurfsstand ist unvollständig, wenn er keine Bauteil-ID-Pläne, Anschluss-/Adapterlogik und Remontagesequenz zeigt.
```

### Repräsentation

```text
Zeichnungssatz → Grundriss, Schnitt, Ansicht, Diagramm
Bauteilebene → Piece-ID, Typ, Paketstatus, Anschlussfamilie
Montageebene → Reihenfolge, Zugang, temporäre Zustände
```

### Konnektoren / Ports

Keine neuen Konnektoren. Der Output muss aber alle verwendeten Konnektoren/Ports sichtbar referenzieren.

### Minimaler Check

```text
Pläne zeigen Piece-IDs und Typen?
Schnitte zeigen Auflager, Stapelung und Lastpfad?
Ansichten zeigen Verhältnis von Hülle und Reuse-Struktur?
Adapter und neue Bauteile getrennt dargestellt?
Montagereihenfolge und Anschlusszugang sichtbar?
```

### Output

```text
drawing_set_complete | warning_missing_remounting_logic | blocked_no_component_ids
```

---

## B-10 — Ausführungsdetails zurück in die Komposition koppeln

**PDF-Seite:** `design_composition_rules_one_page_per_rule.pdf`, Seite 10  
**Eingebettete Originalquelle:** Abbau/Aufbau-Handbuch, gedruckte S. 165–167

### Exakte Textreferenz

```text
Ausführungsplanung
```

```text
individuelle Anschlussdetails an angrenzende Bauteile
```

```text
vertikale tragende Elemente (Wände, Stützen)
```

```text
horizontale tragende Elemente (Bodenplatte, Decken, Dach)
```

### Eigene Ableitung

Die Quelle zeigt, dass Ausführungsdetails nicht nachträglich neutral sind. Sie betreffen Gründung, vertikale und horizontale Tragglieder, Aussteifung und Hülle. Für die Komposition heißt das: Layouts dürfen nicht eingefroren werden, bevor ihre wiederholbaren Detailfamilien bekannt sind.

### Regelcheck

```text
Eine Komposition darf erst fixiert werden, wenn alle wichtigen Schnittstellen einer wiederholbaren Detailfamilie zugeordnet sind.
```

### Repräsentation

```text
Komposition → Felder, Zonen, Bauteil-IDs
Detailfamilie → Fundament/Boden, Wand/Decke, Stütze/Decke, Adapter, Hülle, Service
```

### Konnektoren / Ports

| Detailfamilie | Konnektor | Ports |
|---|---|---|
| Fundament/Boden | `bearing_support`, `restraint_fixing` | `support_side` ↔ `bearing_side`, `fixing_side` ↔ `receiving_side` |
| Wand/Decke | `bearing_support`, `restraint_fixing` | Wand `support_side`, Decke `bearing_side` |
| Stütze/Decke | `bearing_support`, `node_joint` | Stütze `support_side`/`joint_side`, Decke `bearing_side`/`joint_side` |
| Hülle | `boundary_continuity`, `layer_continuity` | `boundary_side`, `layer_side` |
| Service | `route_connection`, `penetration_connection` | `route_side`, `penetration_side`, `service_side` |

### Minimaler Check

```text
Alle Hauptschnittstellen einer Detailfamilie zugeordnet?
Anzahl einmaliger Details minimiert?
Konnektorzugang während Montage möglich?
Aussteifungs- und Kernpositionen früh gesetzt?
Serviceöffnungen als Zonen geplant?
Hüll- und Energiedetails mit Komposition kompatibel?
```

### Output

```text
composition_freeze_allowed | warning_unique_detail_count | blocked_unassigned_interfaces
```

---

# Zusammenfassung der korrigierten Regelstruktur

## Minimal notwendige Konnektoren

```text
structural.bearing_support
structural.node_joint
structural.restraint_fixing
energy.boundary_continuity
energy.layer_continuity
energy.penetration_seal
tga.route_connection
tga.penetration_connection
semantic.boundary_relation
semantic.alignment_relation
semantic.visibility_relation
logistics.access_interface
logistics.support_interface
logistics.lifting_interface
logistics.fixation_interface
```

## Was bewusst kein Konnektor ist

```text
Thermal bridge risk zone
Blocked zone
Damage zone
Protection zone
Monolithic continuity inside one real component
Generic mismatch
Drawing output
Catalogue ID
```

Diese Dinge sind Eigenschaften, Overlays, Risiken oder Repräsentationsdaten. Sie beeinflussen Ports, aber sie sind keine eigenständigen anschließbaren Schnittstellen.

## Endlogik

```text
Bauteil aus Katalog
→ Package-Repräsentation
→ Konnektor mit Eigenschaften
→ Port als tatsächlicher Anschluss-Socket
→ Port-zu-Port-Kompatibilität
→ Paket-spezifischer Check
→ pass | warning | blocked
```
