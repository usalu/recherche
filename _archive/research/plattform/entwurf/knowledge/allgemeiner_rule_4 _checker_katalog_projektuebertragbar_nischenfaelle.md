# Allgemeiner Rule-Checker-Katalog für Wiederverwendungs- und Bauteilpool-Projekte  
## Projektübertragbare Regeln mit Nischenfällen, Sonderformen und gemischten Bauteilen

**Ziel**  
Dieser Katalog beschreibt einen möglichst allgemeinen Rule Checker für das Entwerfen mit wiederverwendeten Bauteilen aus einem bestehenden Bauteilpool.

Er soll auf viele Projekte passen:

```text
Stahlbeton-Wiederverwendung
Fertigteil-Wiederverwendung
Holzbauteile
Stahlbauteile
Mauerwerkselemente
Fassadenelemente
Fenster / Türen
Treppen
TGA-Elemente
hybride Mischbauteile
Bauteile mit unbekannter Herkunft
Bauteile mit Teilnachweisen
Bauteile mit Sonderformen
Bauteile mit neuen Adaptern
```

---

# 0. Grundprinzip

Der Checker prüft nicht nur:

```text
Kann Bauteil A mit Bauteil B verbunden werden?
```

Sondern auch:

```text
Ist das Bauteil eindeutig?
Ist es verfügbar?
Ist die Geometrie verständlich?
Sind Ports und Zonen kompatibel?
Ist das Tragverhalten plausibel?
Welche Nachweise fehlen?
Ist die Nutzung räumlich sinnvoll?
Ist die Hülle bauphysikalisch beherrschbar?
Ist die Montage möglich?
Ist die Wiederverwendung ökologisch sinnvoll?
Bleibt das System reversibel und dokumentiert?
```

---

# 1. Systemtrennung

## 1.1 Geometrie-Generatoren

Geometrie-Generatoren erzeugen **nur geometriebezogene Daten**:

```text
Basisgeometrie
bereinigte Geometrie
Subzonen
Flächen
Kanten
Öffnungen
Bohrzonen-Kandidaten
Auflagerzonen
Port-Geometrien
Hüllflächen-Kandidaten
Sichtflächen-Kandidaten
Transporthüllkörper
Schwerpunkt
Volumen
Flächen
Bounding Boxes
Toleranzgeometrie
```

Sie entscheiden **nicht**:

```text
statische Freigabe
Brandschutzkonformität
LCA-Vollständigkeit
Bohrfreigabe
Genehmigungsfähigkeit
Nutzungserlaubnis
```

## 1.2 Systemmodule

Systemmodule erzeugen nicht-geometrische Zustände:

```text
Identität
Semio-Bindung
Katalogstatus
Verfügbarkeit
Nachweisstatus
Materialstatus
Tragwerksstatus
Brandschutzstatus
Bauphysikstatus
Logistikstatus
LCA-Status
Dokumentation
Warnungen
Regelbereitschaft
```

## 1.3 Rule Checker

Der Rule Checker prüft aktive Situationen:

```text
Bauteil wird platziert
Bauteil wird gedreht / gespiegelt
Bauteil wird verbunden
Bauteil wird gebohrt
Bauteil wird als Hülle genutzt
Bauteil wird einem Raumprogramm zugeordnet
Bauteil wird transportiert
Bauteil wird montiert
Bauteil wird in einer Sequenz verwendet
Bauteil wird in eine Gebäudestruktur integriert
```

---

# 2. Kompakter Hauptbaum

Der Rule Checker hat sechs Hauptkategorien:

```text
Rule Checker
│
├── 1. Identität + Nachweise
├── 2. Geometrie + Typologie
├── 3. Verbindung + Tragwerk
├── 4. Nutzung + Raumqualität
├── 5. Hülle + Bauphysik + Sicherheit
└── 6. Logistik + Ökobilanz + Prozess
```

Diese sechs Kategorien bleiben stabil, auch wenn sehr viele Nischenfälle ergänzt werden.

---

# 3. Statusmodell

Jede Regel gibt einen standardisierten Status zurück:

```yaml
status:
  - pass
  - warning
  - positive
  - engineering_required
  - invalid
  - not_applicable
  - blocked_by_missing_data
```

## 3.1 Bedeutung

```text
pass:
Die Regel ist erfüllt.

warning:
Die Situation ist möglich, aber riskant, unvollständig oder qualitätsrelevant.

positive:
Die Situation erzeugt einen räumlichen, konstruktiven, ökologischen oder gestalterischen Mehrwert.

engineering_required:
Die Regel kann geometrisch vorgeprüft werden, benötigt aber Fachnachweis.

invalid:
Die Aktion ist in dieser Form nicht zulässig.

not_applicable:
Die Regel ist für diesen Fall nicht relevant.

blocked_by_missing_data:
Die Prüfung kann nicht ausgeführt werden, weil notwendige Daten fehlen.
```

---

# 4. Allgemeines Rule-Result-Schema

Jede Regel sollte maschinenlesbar so zurückgeben:

```yaml
rule_result:
  rule_id: string
  category: string
  status: pass | warning | positive | engineering_required | invalid | not_applicable | blocked_by_missing_data
  affected_piece_ids: []
  affected_component_types: []
  affected_zones: []
  affected_ports: []
  affected_spaces: []
  message: string
  reason: string
  missing_data: []
  required_next_data: []
  suggested_actions: []
  severity: info | low | medium | high | critical
  confidence: low | medium | high
```

---

# 5. Universelle Eingaben

## 5.1 Bauteilinput

```yaml
component:
  component_id: required
  component_typology: required
  material_kind: required_or_unknown
  geometry_reference: required
  source_context: optional
  current_location: optional
  stock_status: required
  evidence_status: required
```

## 5.2 Geometrieinput

```yaml
geometry_outputs:
  physical_geometry: required
  sub_zone_map: optional
  face_map: required
  edge_map: required
  port_map: required_if_connectable
  opening_map: required
  support_zone_map: required_if_structural
  envelope_candidate_faces: optional
  semantic_face_candidates: optional
  transport_envelope: required
  center_of_gravity: recommended
  tolerance_model: recommended
```

## 5.3 Kontextinput

```yaml
context:
  active_design_graph: required_for_design_checking
  target_use: optional
  target_preferences: optional
  structural_context: optional
  fire_context: optional
  envelope_context: optional
  acoustic_context: optional
  logistics_context: optional
  lca_context: optional
  code_context: optional
```

---

# 6. Kategorie 1 — Identität + Nachweise

Diese Regeln gelten für jedes Bauteil, unabhängig von Material, Größe oder Nutzung.

---

## 1.1 Eindeutige Identität

```yaml
rule_id: identity_unique
category: Identität + Nachweise
type: hard_rule
general_rule: >
  Jedes reale Pool-Bauteil braucht eine eindeutige ID und darf nicht doppelt als dasselbe Einzelstück verwendet werden.
inputs:
  - component_id
  - type_id
  - stock_status
outputs:
  pass: ID eindeutig
  invalid: ID fehlt oder doppelt
  warning: ID vorhanden, aber Herkunft unklar
```

### Nischenfälle

```text
Bauteil hat alte ID und neue ID
Bauteil wurde geteilt und braucht neue Child-IDs
Bauteil wurde repariert und braucht neue Version
Bauteil ist Teil eines Sets
Bauteil ist visuell gleich, aber nicht identisch
Bauteil ist nur als Gruppe katalogisiert
```

---

## 1.2 Herkunft und Rückverfolgbarkeit

```yaml
rule_id: provenance_traceability
category: Identität + Nachweise
type: evidence_rule
general_rule: >
  Die Herkunft muss so weit bekannt sein, dass Risiken, Nachweise und Wiederverwendungsgrenzen nachvollziehbar bleiben.
inputs:
  - source_project
  - source_building
  - original_location
  - original_function
  - dismantling_date
  - storage_history
outputs:
  pass: Herkunft ausreichend dokumentiert
  warning: Herkunft teilweise unbekannt
  engineering_required: Herkunft relevant für Sicherheit, aber unklar
```

### Nischenfälle

```text
Bauteil aus unbekanntem Gebäude
Bauteil aus Brandereignis
Bauteil aus Hochwassergebiet
Bauteil aus Industriegebäude
Bauteil aus Parkhaus mit Chloridbelastung
Bauteil aus Fassade mit Schadstoffhistorie
Bauteil aus temporärem Bau
Bauteil aus nicht genehmigtem Bestand
```

---

## 1.3 Nachweisvollständigkeit

```yaml
rule_id: evidence_completeness
category: Identität + Nachweise
type: evidence_gate
general_rule: >
  Je kritischer die geplante Nutzung, desto höher muss die Nachweisvollständigkeit sein.
inputs:
  - material_evidence
  - structural_evidence
  - damage_evidence
  - fire_evidence
  - durability_evidence
  - pollutant_evidence
outputs:
  pass: Nachweise ausreichend
  warning: unkritische Nachweise fehlen
  engineering_required: sicherheitsrelevante Nachweise fehlen
  blocked_by_missing_data: Prüfung nicht möglich
```

### Nischenfälle

```text
Material bekannt, Festigkeit unbekannt
Festigkeit bekannt, Bewehrung unbekannt
Geometrie vollständig, Zustand unbekannt
Zustand gut, Schadstoffe unbekannt
Tragfähigkeit dokumentiert, Brandschutz unbekannt
Reparatur dokumentiert, Reparaturqualität unbekannt
```

---

## 1.4 Schadstoff- und Kontaminationsrisiko

```yaml
rule_id: contamination_risk
category: Identität + Nachweise
type: safety_gate
general_rule: >
  Bauteile mit möglicher Schadstoffbelastung dürfen nicht ohne Freigabe in Innenräume, Schleifprozesse, Bohrprozesse oder sensible Nutzungen gelangen.
inputs:
  - pollutant_screening
  - source_context
  - surface_coating
  - intended_use
outputs:
  pass: schadstofffrei oder freigegeben
  warning: Schadstoffstatus unklar
  engineering_required: Labornachweis erforderlich
  invalid: bekannte Kontamination ohne Sanierung
```

### Nischenfälle

```text
Asbest
PCB
PAK
Blei
Mineralwolle
Teerhaltige Beschichtungen
Chloride
Schimmel
Öl / Chemikalien
Industrieablagerungen
Brandschadensrückstände
Unbekannte Beschichtung
```

---

## 1.5 Zustandsnachweis

```yaml
rule_id: condition_evidence
category: Identität + Nachweise
type: evidence_rule
general_rule: >
  Sichtbarer Zustand, Kanten, Risse, Oberflächen und Reparaturen müssen für die geplante Nutzung bewertet sein.
inputs:
  - photos
  - scans
  - inspection_report
  - damage_records
outputs:
  pass: Zustand ausreichend bekannt
  warning: Zustand teilweise bekannt
  engineering_required: Zustand sicherheitsrelevant, aber unklar
```

### Nischenfälle

```text
Kantenabplatzung in Auflagerzone
Riss in Sichtfläche
Riss in Zugzone
freiliegende Bewehrung
Korrosionsspuren
alte Reparaturstelle
abgebrochener Hebepunkt
beschädigte Ecke
verformtes Bauteil
verschmutzte Sichtfläche
```

---

# 7. Kategorie 2 — Geometrie + Typologie

Diese Regeln prüfen, ob die Form erkannt, abstrahiert und sinnvoll nutzbar ist.

---

## 2.1 Geometrie lesbar

```yaml
rule_id: geometry_readable
category: Geometrie + Typologie
type: geometry_hard_rule
general_rule: >
  Die Geometrie muss für Platzierung, Kollision, Zonenbildung und Mengenberechnung lesbar sein.
inputs:
  - physical_geometry
  - unit_system
  - scale
  - mesh_or_solid_quality
outputs:
  pass: Geometrie lesbar
  warning: Geometrie lesbar, aber ungenau
  invalid: Geometrie nicht nutzbar
```

### Nischenfälle

```text
falsche Einheit
Skalierungsfehler
nicht geschlossener Mesh
fehlende Flächen
doppelte Geometrie
verdrehte Achsen
invertierte Normalen
sehr grober Scan
fehlende Dicke
unbekannte Öffnungen
```

---

## 2.2 Typologie erkannt

```yaml
rule_id: typology_classified
category: Geometrie + Typologie
type: geometry_precheck
general_rule: >
  Jedes Bauteil braucht eine erkannte oder bewusst als Sonderform markierte Typologie.
inputs:
  - shape_family
  - dimensions
  - aspect_ratio
  - sub_zone_map
outputs:
  pass: Typologie erkannt
  warning: Sonderform erkannt
  blocked_by_missing_data: Typologie unklar
```

### Allgemeine Typologien

```text
slab
beam
wall
column
mushroom_column
stair
landing
facade_panel
window
door
roof_panel
foundation
steel_profile
timber_beam
masonry_block_panel
service_module
adapter
mixed_fragment
special_fragment
```

### Nischenfälle

```text
Trapezplatte
Parallelogrammplatte
dreieckiger Rest
gekrümmtes Element
Bauteil mit Unterzug
Bauteil mit Stützenstumpf
Bauteil mit Kapitell
Bauteil mit Aussparung
Bauteil mit integrierter Fuge
Bauteil mit schrägen Kanten
Bauteil mit unregelmäßiger Dicke
```

---

## 2.3 Mischbauteil-Subzonen

```yaml
rule_id: mixed_component_subzones
category: Geometrie + Typologie
type: hard_rule
general_rule: >
  Ein Mischbauteil darf nicht als Einfachbauteil behandelt werden, wenn mehrere konstruktive Subzonen vorhanden sind.
inputs:
  - sub_zone_map
  - structural_zone_map
  - requested_role
outputs:
  pass: Subzonenlogik aktiv
  invalid: Mischbauteil als Einfachbauteil behandelt
```

### Nischenfälle

```text
Platte + Unterzug
Platte + Stütze
Platte + Unterzug + Stütze
Wand + Deckenrest
Treppenlauf + Podest
Fassadenpanel + Fensterrahmen
Holzbalken + Stahlplatte
Stahlprofil + angeschweißte Konsole
```

---

## 2.4 Orientierung und Seitenlogik

```yaml
rule_id: orientation_side_logic
category: Geometrie + Typologie
type: reuse_constraint
general_rule: >
  Rotation, Spiegelung oder Umdrehen eines Bauteils darf nicht automatisch erlaubt sein, wenn Oberseite, Unterseite, Bewehrung, Witterungsseite oder Sichtseite relevant sind.
inputs:
  - local_axes
  - original_orientation
  - top_bottom_candidates
  - inside_outside_candidates
  - rotation_request
outputs:
  pass: Orientierung zulässig
  warning: Orientierung verändert Bedeutung
  engineering_required: Orientierung tragwerksrelevant
  invalid: Orientierung verboten
```

### Nischenfälle

```text
Deckenplatte wird umgedreht
Fassadenpanel wird innen verwendet
Wetterschale wird nach innen gedreht
Bewehrungsrichtung wird falsch gedreht
Treppenlauf wird gespiegelt
Türanschlag wird invertiert
Fensteraußenseite wird innen
Holzbalken wird gedreht und Risse liegen ungünstig
```

---

## 2.5 Ports und Anschlusszonen

```yaml
rule_id: ports_exist_and_typed
category: Geometrie + Typologie
type: geometry_precheck
general_rule: >
  Jede verbindbare Zone braucht einen Port mit Geometrie, Richtung, Rolle und Kompatibilitätslogik.
inputs:
  - port_map
  - connector_zone_geometry
  - port_role
outputs:
  pass: Ports vollständig
  warning: optionale Ports fehlen
  invalid: notwendiger Port fehlt
```

### Nischenfälle

```text
Port liegt auf beschädigter Kante
Port liegt in unbekannter Bewehrungszone
Port ist zu klein
Port ist gekrümmt
Port liegt auf schräger Fläche
Port kollidiert mit Öffnung
Port ist nur semantisch, nicht geometrisch erzeugt
Port ist intern und nicht extern anschließbar
```

---

## 2.6 Toleranzen und Passung

```yaml
rule_id: tolerance_fit
category: Geometrie + Typologie
type: construction_precheck
general_rule: >
  Wiederverwendete Bauteile brauchen Toleranzlogik, weil Abweichungen, Schäden und ungenaue Geometrien normal sind.
inputs:
  - geometry_tolerance
  - placement_tolerance
  - joint_tolerance
  - scan_confidence
  - connector_gap
outputs:
  pass: Toleranz innerhalb Grenze
  warning: Toleranz eng oder unklar
  engineering_required: Sondertoleranz braucht Detail
  invalid: Passung unmöglich
```

### Nischenfälle

```text
verzogene Platte
unebene Auflagerfläche
krumme Kante
Scanrauschen
Fuge zu groß
Fuge zu klein für Verguss
Bauteil kollidiert wegen Toleranz
Adapter nötig
Nivelliermörtel nötig
unterschiedliche Maßsysteme
```

---

## 2.7 Öffnungen, Aussparungen und Durchdringungen

```yaml
rule_id: openings_penetrations
category: Geometrie + Typologie
type: geometry_and_evidence_gate
general_rule: >
  Bestehende Öffnungen können wertvoll sein; neue Durchdringungen sind ohne Nachweis kritisch.
inputs:
  - opening_map
  - support_zone_map
  - rebar_or_internal_member_map
  - service_context
outputs:
  pass: Öffnung nutzbar
  warning: Zweck oder Qualität unklar
  engineering_required: neue Durchdringung braucht Nachweis
  invalid: Konflikt mit tragender Zone
```

### Nischenfälle

```text
alte Kernbohrung
nicht dokumentierte Öffnung
Aussparung nahe Kante
Öffnung im Unterzug
Öffnung in Stütze
Öffnung in Brandabschnitt
Öffnung als TGA-Schacht
Öffnung zu klein
Öffnung mit beschädigtem Rand
Öffnung trifft Bewehrung / Kabel / Vorspannung
```

---

## 2.8 Kollisionen

```yaml
rule_id: collision_check
category: Geometrie + Typologie
type: geometry_hard_rule
general_rule: >
  Bauteile, Adapter, Hüllen, Services und Bewegungsräume dürfen nicht ungewollt kollidieren.
inputs:
  - component_geometry
  - design_graph
  - clearance_volumes
outputs:
  pass: keine Kollision
  warning: nahe Kollision
  invalid: harte Kollision
```

### Nischenfälle

```text
Stütze schneidet Fenster
Unterzug schneidet Türhöhe
Bauteil kollidiert mit TGA-Trasse
Kranmontageraum blockiert
Wartungsraum blockiert
Öffnungsflügel kollidiert
Treppenlauf kollidiert mit Decke
Dämmung kollidiert mit Anschluss
```

---

# 8. Kategorie 3 — Verbindung + Tragwerk

Diese Regeln prüfen, ob Bauteile sicher verbunden und getragen werden können.

---

## 3.1 Auflagerüberdeckung

```yaml
rule_id: bearing_overlap
category: Verbindung + Tragwerk
type: structural_precheck
general_rule: >
  Tragende Bauteile brauchen ausreichende geometrische Auflagerüberdeckung.
inputs:
  - bearing_zone_A
  - bearing_zone_B
  - overlap_area
  - minimum_bearing_length
outputs:
  pass: Auflager geometrisch ausreichend
  warning: Auflager knapp
  engineering_required: Auflager plausibel, Nachweis fehlt
  invalid: keine ausreichende Überdeckung
```

### Nischenfälle

```text
schräges Auflager
punktförmiges Auflager
Linienauflager
teilweise beschädigtes Auflager
Auflager auf Adapter
Auflager auf Stahlträger
Auflager auf Bestand
Auflager auf neuem Träger
exzentrisches Auflager
Auflager mit Fuge / Mörtelbett
```

---

## 3.2 Lastpfad

```yaml
rule_id: load_path_continuity
category: Verbindung + Tragwerk
type: structural_precheck
general_rule: >
  Lasten müssen geometrisch nachvollziehbar bis in unterstützende Elemente oder Fundamente geführt werden.
inputs:
  - structural_zone_map
  - support_graph
  - load_direction
  - design_graph
outputs:
  pass: Lastpfad plausibel
  warning: Lastpfad lokal unklar
  engineering_required: statischer Nachweis erforderlich
  invalid: unterbrochener Lastpfad
```

### Nischenfälle

```text
schwebende Ecke
ununterstützte Kante
kurzer Kragarm
lange Auskragung
Stütze ohne Fundament
Wand ohne Auflager
Unterzug endet im Nichts
Lastpfad über Adapter
Lastpfad über neues Bauteil
Lastpfad über beschädigte Zone
```

---

## 3.3 Tragfähigkeit

```yaml
rule_id: capacity_proof
category: Verbindung + Tragwerk
type: engineering_gate
general_rule: >
  Geometrie kann Tragverhalten vorberechnen, aber Tragfähigkeit muss nachgewiesen werden.
inputs:
  - structural_role
  - material_strength
  - reinforcement_or_section_data
  - load_assumptions
outputs:
  pass: Nachweis liegt vor
  engineering_required: Nachweis fehlt
  invalid: Nachweis negativ
```

### Nischenfälle

```text
Bauteil wird tragend wiederverwendet
Bauteil wird nur nichttragend genutzt
Bauteil wird anders belastet als ursprünglich
Bauteil wird umgedreht
Bauteil wird gekürzt
Bauteil enthält alten Schaden
Bauteil war ursprünglich vorgespannt
Bauteil hat unbekannte Bewehrung
Bauteil wird in höherer Gebäudeklasse genutzt
```

---

## 3.4 Verbindungstyp

```yaml
rule_id: connector_family_match
category: Verbindung + Tragwerk
type: connection_precheck
general_rule: >
  Der Verbindungstyp muss zu Material, Portpaar, Lastrolle, Reversibilität und Nachweisniveau passen.
inputs:
  - port_A
  - port_B
  - material_A
  - material_B
  - connector_family
  - connection_role
outputs:
  pass: Verbindungstyp grundsätzlich passend
  warning: Detail fehlt
  engineering_required: tragender Anschluss braucht Nachweis
  invalid: Verbindungstyp unpassend
```

### Allgemeine Verbindungstypen

```text
Auflager
Vergussfuge
Mörtelbett
Schraubverbindung
Anker
Dübel
nachträglicher Bewehrungsanschluss
Stahlplatte
Winkel
Flachstahlhalter
Stahlträgerauflager
Holzverbinder
Klemme
Lasche
Bolzen
Schweißnaht
Klebeverbindung
Trockene reversible Verbindung
Adapter / Mediator
```

### Nischenfälle

```text
reversibler Anschluss gewünscht
nasser Anschluss gewünscht
Brandschutzbekleidung nötig
Korrosionsschutz nötig
Toleranzausgleich nötig
Montage von einer Seite
nicht zugängliche Rückseite
temporäre Verbindung
Demontierbarkeit als Ziel
```

---

## 3.5 Bohren / Ankern / Schneiden

```yaml
rule_id: intrusive_action_gate
category: Verbindung + Tragwerk
type: hard_gate
general_rule: >
  Bohren, Ankern, Fräsen, Schleifen oder Schneiden darf nur mit Nachweis der inneren Struktur und Materialrisiken erfolgen.
inputs:
  - action_type
  - target_zone
  - reinforcement_map
  - prestress_map
  - service_map
  - pollutant_status
outputs:
  pass: Eingriff freigegeben
  engineering_required: Nachweis erforderlich
  invalid: Eingriff in verbotener Zone
```

### Nischenfälle

```text
Bohrung in unbekannter Bewehrungszone
Bohrung in Vorspannung
Bohrung in Unterzug
Bohrung in Stütze
Bohrung nahe Kante
Bohrung in Risszone
Bohrung in Brandabschnitt
Schleifen bei Schadstoffverdacht
Schneiden bei unbekannter Bewehrung
Anker in beschädigtem Beton
```

---

## 3.6 Temporäre Zustände

```yaml
rule_id: temporary_state_stability
category: Verbindung + Tragwerk
type: construction_sequence_rule
general_rule: >
  Ein Entwurf kann im Endzustand stabil sein, aber während Montage, Transport oder Zwischenzustand instabil.
inputs:
  - assembly_sequence
  - temporary_supports
  - lifting_state
  - partial_connections
outputs:
  pass: temporäre Zustände gesichert
  warning: temporäre Sicherung unklar
  engineering_required: Montagezustand braucht Nachweis
  invalid: instabiler Zwischenzustand
```

### Nischenfälle

```text
Wand steht vor Deckenanschluss
Stütze steht ohne Aussteifung
Platte liegt einseitig auf
Adapter noch nicht vergossen
Anschluss noch nicht ausgehärtet
Kran hängt schief
Bauteil wird gedreht
Windlast während Montage
Transportgestell erforderlich
```

---

## 3.7 Ermüdung, Resttragfähigkeit und Nutzungsgeschichte

```yaml
rule_id: previous_life_structural_risk
category: Verbindung + Tragwerk
type: evidence_warning
general_rule: >
  Die bisherige Nutzung kann die Wiederverwendung beeinflussen, auch wenn das Bauteil geometrisch intakt wirkt.
inputs:
  - previous_use
  - load_history
  - exposure_history
  - inspection
outputs:
  pass: Nutzungsgeschichte unkritisch oder nachgewiesen
  warning: Nutzungsgeschichte unklar
  engineering_required: kritische Vornutzung braucht Nachweis
```

### Nischenfälle

```text
Parkhaus mit Tausalz
Industrieboden mit Chemikalien
Brandereignis
Erdbeben / Setzung
Überlastung
Vibrationsnutzung
Kranbahnträger
Wasser- oder Frostschaden
lange Außenlagerung
```

---

# 9. Kategorie 4 — Nutzung + Raumqualität

Diese Regeln stellen sicher, dass wiederverwendete Bauteile nicht nur technisch möglich sind, sondern gute Räume erzeugen.

---

## 4.1 Programmfit

```yaml
rule_id: program_fit
category: Nutzung + Raumqualität
type: architectural_performance
general_rule: >
  Die Geometrie und Position des Bauteils müssen mit der geplanten Nutzung vereinbar sein.
inputs:
  - target_use
  - room_geometry
  - obstacle_map
  - clearances
outputs:
  pass: Nutzung passt
  warning: Nutzung eingeschränkt
  positive: Bauteil stärkt Nutzung oder Atmosphäre
  invalid: Nutzung unmöglich
```

### Nischenfälle

```text
Wohnraum
Bad
Küche
Büro
Schule
Werkstatt
Atelier
Lager
Fluchtweg
Technikraum
öffentlicher Raum
barrierefreier Raum
Kindergarten
Labor
```

---

## 4.2 Nutzbare Fläche

```yaml
rule_id: usable_area
category: Nutzung + Raumqualität
type: spatial_quality
general_rule: >
  Nicht die Bruttofläche zählt allein, sondern die nutzbare Fläche nach Hindernissen, Stützen, Unterzügen, Winkeln und Restflächen.
inputs:
  - room_polygon
  - obstacle_geometry
  - usable_area_polygon
  - furniture_zones
outputs:
  pass: ausreichend nutzbar
  warning: eingeschränkt nutzbar
  positive: Hindernis erzeugt gute Zonierung
  invalid: Mindestnutzung nicht möglich
```

### Nischenfälle

```text
Stütze mitten im Raum
Unterzug reduziert Höhe
schräger Wandabschluss
spitze Ecke
tiefe Nische
Restdreieck
sehr lange schmale Zone
Möblierung passt nicht
Türschwenkbereich blockiert
Fensterzugang blockiert
```

---

## 4.3 Hindernisse als Qualität oder Problem

```yaml
rule_id: obstacle_quality
category: Nutzung + Raumqualität
type: spatial_interpretation
general_rule: >
  Wiederverwendete Bauteile können Hindernisse sein, aber auch räumliche Qualität erzeugen.
inputs:
  - obstacle_geometry
  - room_context
  - target_preferences
outputs:
  warning: Hindernis reduziert Nutzung
  positive: Hindernis erzeugt Nische, Schwelle, Rhythmus oder Identität
  invalid: Hindernis blockiert Pflichtfunktion
```

### Nischenfälle

```text
Stütze vor Fenster
Nische hinter Stütze
große Stütze im kleinen Raum
Unterzug als Raumteiler
Balken als Lichtregal
Stützenreihe als Rhythmus
schräge Kante als Sitznische
Bauteil als Schwelle
Bauteil als Ausstellungsobjekt
```

---

## 4.4 Tageslicht und Sicht

```yaml
rule_id: daylight_view
category: Nutzung + Raumqualität
type: architectural_performance
general_rule: >
  Bauteile dürfen Tageslicht, Sichtbeziehungen und Fensterfunktionen nicht ungewollt blockieren.
inputs:
  - window_geometry
  - facade_openings
  - obstacle_geometry
  - daylight_path
outputs:
  pass: Licht und Sicht ausreichend
  warning: Licht oder Sicht reduziert
  positive: Schatten / Tiefe / räumlicher Filter gewünscht
  invalid: notwendige Belichtung oder Öffnung blockiert
```

### Nischenfälle

```text
Stütze vor Fenster
Unterzug vor Oberlicht
Bauteil blockiert Lüftungsflügel
Bauteil erzeugt tiefe Laibung
Bauteil verschattet Nachbarraum
Fenster kann nicht geöffnet werden
Sichtschutz als positive Qualität
```

---

## 4.5 Erschließung und Barrierefreiheit

```yaml
rule_id: circulation_accessibility
category: Nutzung + Raumqualität
type: access_rule
general_rule: >
  Wege, Bewegungsflächen, Türen und Fluchtwege müssen trotz wiederverwendeter Bauteile funktionieren.
inputs:
  - circulation_paths
  - clearance_volumes
  - door_swings
  - obstacle_map
outputs:
  pass: Wege frei
  warning: Wege eng
  invalid: Weg, Tür oder Fluchtfunktion blockiert
```

### Nischenfälle

```text
Stütze im Flur
Unterzug in Kopfhöhe
Türflügel kollidiert
Rollstuhlwendekreis blockiert
Treppenlauf zu eng
Fluchtwegbreite unterschritten
Wartungszugang blockiert
Schachtzugang blockiert
```

---

## 4.6 Patio, Hof, Lücke und Restvoid

```yaml
rule_id: void_patio_courtyard
category: Nutzung + Raumqualität
type: spatial_topology
general_rule: >
  Lücken sind nicht automatisch Fehler. Sie können Hof, Patio, Lichtschacht, TGA-Schacht, Fuge oder unbrauchbarer Restvoid sein.
inputs:
  - void_geometry
  - open_to_sky
  - adjacent_rooms
  - access
  - drainage_context
outputs:
  pass: Void klassifiziert
  warning: Restvoid unklar
  positive: Patio verbessert Licht, Luft oder Atmosphäre
  invalid: gefährlicher oder unzugänglicher Void
```

### Nischenfälle

```text
Innenhof
Lichthof
schmaler Patio
TGA-Schacht
Brandabschnittsfuge
Bewegungsfuge
unzugängliche Resttasche
Entwässerungsproblem
zu enger Hof
verschatteter Hof
```

---

## 4.7 Gestalterische Zielpräferenzen

```yaml
rule_id: target_preference_alignment
category: Nutzung + Raumqualität
type: preference_rule
general_rule: >
  Manche Situationen sind weder objektiv gut noch schlecht, sondern abhängig von Zielpräferenzen.
inputs:
  - target_preferences
  - spatial_condition
  - visible_reuse_intent
outputs:
  positive: Zustand passt zur Präferenz
  warning: Zustand widerspricht Präferenz
  neutral: keine Präferenz gesetzt
```

### Präferenzen

```text
maximale Wiederverwendung
minimale Eingriffe
sichtbare Wiederverwendung
glatte neutrale Räume
robuste Low-Tech-Ästhetik
präzise Fugen
hohe Reversibilität
minimales CO₂
maximale Nutzfläche
kompakte Wohnungen
großzügige Räume
hohe Tageslichtqualität
```

---

# 10. Kategorie 5 — Hülle + Bauphysik + Sicherheit

Diese Regeln prüfen thermische, feuchte-, akustische, brandschutz- und sicherheitsbezogene Aspekte.

---

## 5.1 Hüllrelevanz

```yaml
rule_id: envelope_relevance
category: Hülle + Bauphysik + Sicherheit
type: building_physics_precheck
general_rule: >
  Sobald ein Bauteil Teil der Gebäudehülle wird, gelten zusätzliche Regeln für Wärme, Feuchte, Luftdichtheit, Brandschutz und Dauerhaftigkeit.
inputs:
  - envelope_context
  - interior_exterior_faces
  - thermal_boundary
outputs:
  pass: Hüllanforderungen geklärt
  warning: Hüllrolle unklar
  engineering_required: Hüllnachweis fehlt
```

### Nischenfälle

```text
alte Decke wird Dach
alte Innenwand wird Außenwand
Fassadenteil wird innen genutzt
Bauteil durchstößt Dämmung
Stütze kreuzt Hülle
Unterzug außen sichtbar
Fensterrahmen wiederverwendet
```

---

## 5.2 Wärmebrücken

```yaml
rule_id: thermal_bridge_risk
category: Hülle + Bauphysik + Sicherheit
type: energy_warning
general_rule: >
  Komplexe Kanten, Anschlüsse, Stahlteile und Bauteildurchdringungen können Wärmebrücken erzeugen.
inputs:
  - thermal_boundary_faces
  - connector_zones
  - material_continuity
  - edge_complexity
outputs:
  pass: Wärmebrücken unkritisch oder berechnet
  warning: Wärmebrückenrisiko
  engineering_required: detaillierte Berechnung erforderlich
```

### Nischenfälle

```text
Zickzackfassade
viele Außenecken
Stahlanker durch Dämmung
Betonsteg durch Dämmung
auskragende Platte
Stütze in Außenwand
Bestandsfenster ohne thermische Trennung
Dämmung kollidiert mit Anschluss
```

---

## 5.3 Feuchte, Wasser, Frost

```yaml
rule_id: moisture_weathering
category: Hülle + Bauphysik + Sicherheit
type: durability_precheck
general_rule: >
  Exponierte, horizontale, erdberührte oder beschädigte Flächen brauchen Feuchteschutz.
inputs:
  - exposure_context
  - horizontal_faces
  - ground_contact
  - drainage_strategy
  - surface_condition
outputs:
  pass: Feuchteschutz definiert
  warning: Feuchte- oder Witterungsrisiko
  engineering_required: Nachweis erforderlich
```

### Nischenfälle

```text
alte Decke als Dach
Betonkante außen exponiert
Bauteil liegt im Spritzwasserbereich
Stützenfuß am Boden
Fuge ohne Abdichtung
Innenhof ohne Entwässerung
Frost-Tau-Wechsel
Außenlagerung
Riss in wasserführender Fläche
```

---

## 5.4 Brandschutz

```yaml
rule_id: fire_safety
category: Hülle + Bauphysik + Sicherheit
type: fire_gate
general_rule: >
  Materialklasse allein reicht nicht. Bauteil, Anschluss, Oberfläche, Nutzung und Gebäudeanforderung müssen zusammen geprüft werden.
inputs:
  - fire_context
  - material_fire_class
  - connection_detail
  - exposed_steel
  - compartment_role
outputs:
  pass: Brandschutz nachgewiesen
  warning: Brandschutzrolle unklar
  engineering_required: Brandschutznachweis erforderlich
  invalid: bekannte Anforderung nicht erfüllt
```

### Nischenfälle

```text
exponierter Stahlverbinder
alter Brandschaden
Holzbauteil in höherer Gebäudeklasse
Bauteil als Brandwand
Fuge in Brandabschnitt
Durchdringung ohne Abschottung
gebrauchte Tür als Brandschutztür
gebrauchtes Fenster in Brandwand
Beschichtung unbekannt
```

---

## 5.5 Akustik

```yaml
rule_id: acoustic_performance
category: Hülle + Bauphysik + Sicherheit
type: acoustic_precheck
general_rule: >
  Masse kann akustisch helfen, ersetzt aber keinen Aufbau- und Anschlussnachweis.
inputs:
  - mass_per_area
  - assembly_layers
  - flanking_paths
  - target_acoustic_class
outputs:
  pass: Akustik nachgewiesen
  warning: akustische Leistung unklar
  engineering_required: Nachweis erforderlich
```

### Nischenfälle

```text
alte Deckenplatte als Wohnungstrenndecke
harte Verbindung erzeugt Flankenübertragung
Fuge überträgt Schall
Trittschallaufbau fehlt
Unterzug leitet Schall
Hohlraum erzeugt Resonanz
gebrauchte Tür mit unbekanntem Schalldämmmaß
```

---

## 5.6 Dauerhaftigkeit

```yaml
rule_id: durability_service_life
category: Hülle + Bauphysik + Sicherheit
type: durability_gate
general_rule: >
  Restnutzungsdauer muss zur neuen Nutzung und Exposition passen.
inputs:
  - material_condition
  - exposure_class
  - carbonation
  - chloride
  - corrosion
  - repair_status
outputs:
  pass: Dauerhaftigkeit ausreichend
  warning: Dauerhaftigkeit unklar
  engineering_required: Modell / Prüfung erforderlich
  invalid: Nutzung bei Zustand nicht zulässig
```

### Nischenfälle

```text
Chloride in Parkhausbauteil
Karbonatisierung bis Bewehrung
freiliegende Bewehrung
alte Risse
Frostschäden
Holzfäule
Stahlkorrosion
beschädigte Beschichtung
Außenlagerung ohne Schutz
```

---

## 5.7 Nutzungssicherheit

```yaml
rule_id: user_safety
category: Hülle + Bauphysik + Sicherheit
type: safety_rule
general_rule: >
  Wiederverwendete Bauteile dürfen keine direkten Nutzungsrisiken erzeugen.
inputs:
  - exposed_edges
  - sharp_corners
  - falling_parts
  - surface_condition
  - user_accessibility
outputs:
  pass: sicher
  warning: Schutzdetail nötig
  invalid: direkte Gefahr
```

### Nischenfälle

```text
scharfe Betonkante
abplatzende Oberfläche
lose Beschichtung
freiliegende Bewehrung
niedriger Unterzug in Kopfhöhe
Quetschstelle
Stolperkante
unbeabsichtigtes Klettern
Kinderzugänglichkeit
```

---

# 11. Kategorie 6 — Logistik + Ökobilanz + Prozess

Diese Regeln prüfen, ob das Projekt mit vielen Einzelstücken praktisch, ökologisch und prozessual funktioniert.

---

## 6.1 Bestand und eindeutige Nutzung

```yaml
rule_id: inventory_unique_use
category: Logistik + Ökobilanz + Prozess
type: inventory_hard_rule
general_rule: >
  Ein reales Einzelbauteil darf nicht mehrfach verwendet werden, außer es existieren mehrere physische Exemplare.
inputs:
  - component_id
  - stock_total
  - active_instances
outputs:
  pass: Nutzung eindeutig
  invalid: Bauteil doppelt verwendet
```

### Nischenfälle

```text
einziges Unikat
Serienbauteil mit mehreren Exemplaren
visuell gleiche, aber unterschiedliche Stücke
Bauteil geteilt in mehrere Child-Pieces
Bauteil reserviert
Bauteil blockiert
Bauteil verloren
```

---

## 6.2 Lagerung

```yaml
rule_id: storage_strategy
category: Logistik + Ökobilanz + Prozess
type: logistics_precheck
general_rule: >
  Lagerung muss Geometrie, Gewicht, Zustand, Witterung und spätere Montagereihenfolge berücksichtigen.
inputs:
  - geometry
  - mass
  - center_of_gravity
  - support_points
  - weather_exposure
  - assembly_sequence
outputs:
  pass: Lagerstrategie definiert
  warning: Lagerung unklar
  engineering_required: Sonderlagerung nötig
  invalid: instabile oder schädigende Lagerung
```

### Nischenfälle

```text
flache Platte
Wand stehend
Stütze liegend
Mischbauteil mit Stützenstumpf
empfindliche Sichtfläche
Außenlagerung
Stapelung
Zwischenhölzer
Transportgestell
Lagerreihenfolge passt nicht zur Montage
```

---

## 6.3 Heben und Montage

```yaml
rule_id: lifting_assembly
category: Logistik + Ökobilanz + Prozess
type: logistics_engineering_gate
general_rule: >
  Masse, Schwerpunkt, Hebepunkte und temporäre Zustände müssen vor Montage geklärt sein.
inputs:
  - mass
  - center_of_gravity
  - lifting_points
  - crane_capacity
  - temporary_support
outputs:
  pass: Hebe- und Montagekonzept nachgewiesen
  warning: schwer oder exzentrisch
  engineering_required: Hebepunkte / Montagekonzept fehlen
  invalid: bekannte Grenze überschritten
```

### Nischenfälle

```text
unbekannte Hebepunkte
alte Hebeanker
beschädigte Hebeanker
exzentrischer Schwerpunkt
sehr langes Bauteil
sehr dünnes Bauteil
Bauteil muss gedreht werden
Montage nur von einer Seite möglich
Kranreichweite unklar
```

---

## 6.4 Transport

```yaml
rule_id: transport_feasibility
category: Logistik + Ökobilanz + Prozess
type: logistics_precheck
general_rule: >
  Bauteil muss mit realistischem Fahrzeug, Route, Schutz und Ladungssicherung transportierbar sein.
inputs:
  - transport_envelope
  - mass
  - route
  - vehicle_type
  - permit_status
outputs:
  pass: transportierbar
  warning: nahe Grenze oder Route unklar
  engineering_required: Sondertransport / Gestell nötig
  invalid: Transport unmöglich
```

### Nischenfälle

```text
Überbreite
Überhöhe
zu hohes Gewicht
Sondergenehmigung
enge Innenstadt
Brücke mit Gewichtslimit
Bauteil braucht Transportgestell
empfindliche Sichtfläche
Witterungsschutz während Transport
```

---

## 6.5 Montagefolge

```yaml
rule_id: assembly_sequence
category: Logistik + Ökobilanz + Prozess
type: process_rule
general_rule: >
  Die Montagefolge muss Verfügbarkeit, Lagerreihenfolge, temporäre Stabilität und Zugänglichkeit berücksichtigen.
inputs:
  - dependency_graph
  - piece_sequence
  - storage_order
  - crane_access
outputs:
  pass: Sequenz definiert
  warning: Sequenz unvollständig
  invalid: Sequenz unmöglich
```

### Nischenfälle

```text
440 Einzelteile
viele Unikate
falsche Reihenfolge im Lager
Bauteil hinter anderem Bauteil blockiert
temporäre Abstützung fehlt
Anschluss später nicht mehr erreichbar
Verguss muss aushärten
Witterungsfenster
```

---

## 6.6 Ökobilanz-Vorprüfung

```yaml
rule_id: lca_precheck
category: Logistik + Ökobilanz + Prozess
type: environmental_precheck
general_rule: >
  Wiederverwendung sollte ökologisch bewertet werden, aber Vorprüfung und vollständige LCA müssen getrennt bleiben.
inputs:
  - reused_mass
  - transport_distance
  - transport_factor
  - new_equivalent_reference
  - connector_impacts
  - adapter_impacts
  - dataset_status
outputs:
  positive: vermiedenes Neumaterialpotenzial
  warning: nur Vorprüfung
  pass: vollständige LCA
  engineering_required: Datensatz oder Bilanzgrenze fehlt
```

### Nischenfälle

```text
kurzer lokaler Transport
sehr langer Transport
schweres Bauteil mit wenig Nutzen
viele neue Stahladapter
viel Vergussmörtel
aufwendige Reparatur
neue Dämmung nötig
Wiederverwendung spart kaum Material
Bauteil ersetzt hochwertigen Neubau
```

---

## 6.7 Reversibilität und zukünftige Wiederverwendung

```yaml
rule_id: future_reuse_reversibility
category: Logistik + Ökobilanz + Prozess
type: circularity_rule
general_rule: >
  Neue Anschlüsse sollten zukünftige Demontage, Sortenreinheit und Dokumentation möglichst unterstützen.
inputs:
  - connection_type
  - material_mix
  - documentation
  - disassembly_access
outputs:
  positive: reversible und dokumentiert
  warning: spätere Demontage erschwert
  invalid: irreversible Lösung widerspricht Projektziel, falls Reversibilität Pflicht ist
```

### Nischenfälle

```text
trockene Schraubverbindung
vergossener Anschluss
Klebeverbindung
verschweißte Verbindung
eingebettete Stahlteile
unzugänglicher Anschluss
keine Dokumentation
Materialmix nicht trennbar
```

---

## 6.8 Kosten- und Aufwandssensitivität

```yaml
rule_id: effort_cost_sensitivity
category: Logistik + Ökobilanz + Prozess
type: project_feasibility_warning
general_rule: >
  Ein Bauteil kann technisch möglich sein, aber wegen Prüf-, Transport-, Anpassungs- oder Montageaufwand unpraktisch werden.
inputs:
  - repair_need
  - testing_need
  - adapter_need
  - transport_complexity
  - installation_complexity
outputs:
  pass: Aufwand angemessen
  warning: hoher Aufwand
  positive: hoher Aufwand lohnt wegen hohem Wiederverwendungswert
```

### Nischenfälle

```text
kleines Bauteil mit vielen Prüfkosten
schweres Bauteil mit wenig Masseersatz
komplizierte Sonderform
viele neue Adapter
aufwendige Schadstoffprüfung
lange Lagerzeit
teure Kranmontage
```

---

# 12. Nischenregel-Matrix

Diese Matrix hilft, seltene Fälle systematisch abzudecken.

| Nischenfall | Kategorie | Checker-Reaktion |
|---|---|---|
| Bauteil hat unbekannte Herkunft | Identität + Nachweise | warning / engineering_required |
| Bauteil aus Parkhaus | Identität + Nachweise | chloride / corrosion evidence required |
| Bauteil aus Brandereignis | Identität + Nachweise / Brandschutz | engineering_required |
| Bauteil hat Asbestverdacht | Identität + Nachweise | invalid until clearance |
| Bauteil ist vorgespannt | Tragwerk | no cutting/drilling without proof |
| Bauteil hat unbekannte Bewehrung | Tragwerk | no drilling, engineering_required |
| Bauteil ist Mischfragment | Geometrie + Typologie | subzone logic required |
| Bauteil ist trapezförmig | Geometrie + Nutzung | irregular usability warning |
| Bauteil wird gespiegelt | Geometrie + Tragwerk | orientation check |
| Bauteil wird umgedreht | Geometrie + Tragwerk | orientation / reinforcement warning |
| Port liegt auf beschädigter Kante | Geometrie + Tragwerk | invalid or engineering_required |
| Anschluss ist nicht erreichbar | Verbindung + Prozess | invalid / sequence warning |
| neue Adapter nötig | Verbindung + LCA | engineering_required + LCA warning |
| Stütze vor Fenster | Nutzung | warning or positive |
| Nische hinter Stütze | Nutzung | positive or warning |
| große Stütze in Bad | Nutzung | warning / invalid |
| unklassifizierte Lücke | Nutzung | classify as patio/void/service |
| Bauteil bildet Fassade | Hülle | envelope proof required |
| viele Außenecken | Bauphysik | thermal/moisture warning |
| Stahlverbinder im Brandbereich | Brandschutz | fire proof required |
| Bauteil sehr schwer | Logistik | lifting and crane check |
| kein Hebepunkt bekannt | Logistik | engineering_required |
| lange Transportdistanz | LCA | environmental warning |
| viele neue Stahladapter | LCA | adapter impact warning |
| irreversible Verbindung | Kreislauffähigkeit | circularity warning |
| Bauteil doppelt platziert | Bestand | invalid |

---

# 13. Trigger-Logik

Der Checker läuft nicht nur einmal, sondern ereignisbasiert.

## 13.1 Beim Import in den Bauteilpool

```yaml
trigger: import_component
run_rules:
  - identity_unique
  - provenance_traceability
  - geometry_readable
  - typology_classified
  - evidence_completeness
  - contamination_risk
```

## 13.2 Beim Platzieren im Entwurf

```yaml
trigger: place_component
run_rules:
  - inventory_unique_use
  - orientation_side_logic
  - collision_check
  - program_fit
  - usable_area
  - temporary_state_stability
```

## 13.3 Beim Verbinden zweier Bauteile

```yaml
trigger: connect_components
run_rules:
  - ports_exist_and_typed
  - bearing_overlap
  - connector_family_match
  - load_path_continuity
  - capacity_proof
  - fire_safety
  - thermal_bridge_risk
```

## 13.4 Beim Bohren / Schneiden / Ankern

```yaml
trigger: intrusive_action
run_rules:
  - intrusive_action_gate
  - contamination_risk
  - openings_penetrations
  - capacity_proof
  - durability_service_life
```

## 13.5 Beim Zuweisen einer Nutzung

```yaml
trigger: assign_program
run_rules:
  - program_fit
  - usable_area
  - daylight_view
  - circulation_accessibility
  - obstacle_quality
```

## 13.6 Beim Zuweisen zur Gebäudehülle

```yaml
trigger: assign_envelope
run_rules:
  - envelope_relevance
  - thermal_bridge_risk
  - moisture_weathering
  - fire_safety
  - acoustic_performance
  - durability_service_life
```

## 13.7 Bei Logistik / Montageplanung

```yaml
trigger: plan_logistics
run_rules:
  - storage_strategy
  - lifting_assembly
  - transport_feasibility
  - assembly_sequence
```

## 13.8 Bei Ökobilanz-Auswertung

```yaml
trigger: calculate_lca
run_rules:
  - lca_precheck
  - future_reuse_reversibility
  - effort_cost_sensitivity
```

---

# 14. Anwendung auf `AA_MIX_001`

## 14.1 Allgemeine Klassifikation

```yaml
component_id: AA_MIX_001
general_typology: mixed_fragment
specific_subtypes:
  - slab_zone
  - beam_zone
  - column_stub_zone
  - internal_transition_zones
```

## 14.2 Erwartete Statusausgabe

```yaml
AA_MIX_001_rule_summary:
  identity_unique: pass
  provenance_traceability: warning
  evidence_completeness: engineering_required
  contamination_risk: warning
  geometry_readable: pass
  typology_classified: pass
  mixed_component_subzones: pass
  orientation_side_logic: warning
  ports_exist_and_typed: pass
  tolerance_fit: warning
  openings_penetrations: engineering_required
  bearing_overlap: engineering_required
  load_path_continuity: engineering_required
  capacity_proof: engineering_required
  connector_family_match: engineering_required
  intrusive_action_gate: invalid_without_rebar_scan
  temporary_state_stability: engineering_required
  program_fit: context_dependent
  usable_area: warning_or_positive
  obstacle_quality: warning_or_positive
  daylight_view: context_dependent
  void_patio_courtyard: context_dependent
  envelope_relevance: engineering_required_if_envelope
  thermal_bridge_risk: warning_if_envelope
  moisture_weathering: warning_if_exposed
  fire_safety: engineering_required
  acoustic_performance: warning
  storage_strategy: engineering_required
  lifting_assembly: engineering_required
  transport_feasibility: warning
  lca_precheck: positive_and_warning
  future_reuse_reversibility: depends_on_connection
```

## 14.3 Beispiel: User verbindet Deckenrand mit Wandkopf

```yaml
trigger: connect_components
piece_A: AA_MIX_001
port_A: slab-edge-bearing
piece_B: generic_wall_panel
port_B: wall-top-bearing
```

### Checker-Ergebnis

```yaml
result:
  port_compatibility: pass
  bearing_overlap: engineering_required
  load_path_continuity: engineering_required
  connector_family_match: engineering_required
  intrusive_action_gate: invalid_without_rebar_scan
  fire_safety: engineering_required_if_fire_relevant
  lca_precheck: warning_if_new_connector_material_missing
overall_status: engineering_required
```

## 14.4 Beispiel: User nutzt das Bauteil als reine Platte

```yaml
trigger: assign_role
piece: AA_MIX_001
requested_role: simple_slab
```

### Checker-Ergebnis

```yaml
result:
  mixed_component_subzones: invalid
  reason: >
    Das Bauteil enthält Unterzug- und Stützen-Subzonen
    und darf nicht als einfache Deckenplatte behandelt werden.
overall_status: invalid
```

## 14.5 Beispiel: User akzeptiert Stütze als räumliche Qualität

```yaml
trigger: assign_program
piece: AA_MIX_001
spatial_condition: column_creates_niche
target_preferences:
  visible_reuse: high
  spatial_complexity: accepted
```

### Checker-Ergebnis

```yaml
result:
  obstacle_quality: positive
  niche_behind_obstacle: positive
  usable_area: warning_if_clearance_low
overall_status: positive_with_checks
```

---

# 15. Allgemeiner Minimaldatensatz für robuste Regeln

Damit der Rule Checker in vielen Projekten funktioniert, sollte jedes Pool-Bauteil mindestens haben:

```yaml
minimum_component_data:
  component_id: required
  component_typology: required
  material_kind: required_or_unknown
  geometry_reference: required
  stock_status: required
  source_context: optional_but_recommended
  condition_status: unknown_allowed
  evidence_status: required
  generated_ports: required_if_connectable
  generated_zones: required
```

Für sicherheitsrelevante Nutzung zusätzlich:

```yaml
safety_required_data:
  structural_evidence: required_if_load_bearing
  reinforcement_or_internal_structure: required_if_drilling_or_anchoring
  fire_evidence: required_if_fire_relevant
  contamination_clearance: required_if_source_risk
  lifting_strategy: required_if_heavy_or_unique
  transport_strategy: required_if_moved
```

---

# 16. Schlussfolgerung

Der Rule Checker ist projektübertragbar, wenn er nicht auf einzelne Projektnamen oder feste Bauteiltypen reduziert wird.

Er muss allgemein arbeiten mit:

```text
Bauteilidentität
Typologie
Subzonen
Ports
Nachweisen
Nutzungskontext
Hüllkontext
Logistikkontext
LCA-Kontext
Zielpräferenzen
```

Dadurch deckt er einfache und sehr spezielle Fälle ab:

```text
rechteckige Platte
Trapezfragment
Mischbauteil
Bauteil mit Stütze
Bauteil mit Unterzug
Bauteil mit unbekannter Bewehrung
Bauteil aus Schadstoffkontext
Bauteil mit neuer Adapterstruktur
Bauteil als Fassade
Bauteil als Innenraumobjekt
Bauteil mit räumlicher Sonderqualität
```

Der wichtigste Grundsatz:

```text
Der Checker soll nicht Wiederverwendung verhindern.
Er soll sichtbar machen, was bereits passt,
was räumlich wertvoll sein kann,
was nachgewiesen werden muss
und was wirklich unzulässig ist.
```
