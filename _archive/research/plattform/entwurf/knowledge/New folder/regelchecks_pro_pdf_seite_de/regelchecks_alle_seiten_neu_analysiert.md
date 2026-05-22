# Regelchecks aus dem PDF - neu analysiert

**Arbeitsstand:** Ein einziges Markdown-Dokument für alle 13 PDF-Seiten. Die alten Markdown-Dateien und die frühere Übersetzung wurden nicht als Struktur übernommen. Die Analyse unten startet pro Seite neu aus dem Text der PDF-Seite.

**Wichtige Modellannahme:**

```text
Konnektor = getypte Verbindungsfunktion mit Eigenschaften.
Port = die konkrete anschließbare Schnittstelle innerhalb eines Konnektors.
Kompatibilität = Port-zu-Port.
Risiko-, Schadens-, No-Drill-, Blocked- und Thermal-Bridge-Zonen sind keine Konnektoren, sondern Eigenschaften oder Overlays, die Ports blockieren, warnen oder herabstufen.
```

**Originalquelle im PDF:** Jede Seite verweist auf `Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf`. Die exakten PDF-Seitentexte sind unter jeder Regel als Referenz zitiert.

---

## 01 - SG-01 - Struktureller Bauteilstatus

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 1
STRUCTURAL GRAMMAR: SG-01 - Structural role passport
Source image: Abbau Aufbau handbook, printed pp. 31-33
  STRUCTURAL GRAMMAR  
Exact source taken from handbook
The handbook asks the structural engineer to read the existing structural system: relevant
reinforced-concrete elements, load-transfer concept, spans, span directions and reinforcement
layout.
Translation to already-sliced component-pool design
For a ready-sliced component pool, this becomes the structural identity of each piece. A slab,
wall, column or beam must keep information about how it can carry load and where it can be
supported.
Rule
A component can enter the structural grammar only when it has a structural
passport: type, load direction, span direction, reinforcement direction, support
zones, connection/no-drill zones and permitted orientation.
Minimum checks
- component type is fixed: S, W, C, B, F or adapter
- original top/bottom and main span direction are known
- support and bearing zones are identified
- reinforcement or no-drill zones are mapped
- structural-use status is assigned before placement
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite beschreibt keinen endgültigen statischen Nachweis, sondern den Einstieg in die strukturelle Modellierbarkeit eines Bauteils. Ein Bauteil darf strukturelle Konnektoren erst anbieten, wenn seine minimale strukturelle Abstraktion und sein Evidenzstatus bekannt sind.

### Minimaler Regelcheck

- **Ebene:** Bauteil
- **Paket(e):** Structural + Evidence
- **Repräsentation:** Typabhängig: Träger -> 1D-Linie; Stütze -> 1D-vertikale Linie; Decke/Platte -> 2D-Plattenfläche; Wand/Scheibe -> 2D-Wandfläche; monolithischer Fragmenttyp -> zerlegter Strukturgraph aus Haupt-Elementen.
- **Konnektoren und Ports:**
  - `structural.bearing_support` - bearing_side, support_side
  - `structural.node_joint` - joint_side
  - `structural.restraint_fixing` - fixing_side, receiving_side
- **Prüfschritte:**
  - Typ und strukturelle Rolle sind festgelegt.
  - Trag-/Spannrichtung oder plausible Richtung ist dokumentiert.
  - Konnektorbereiche liegen auf der passenden Abstraktion, nicht auf beliebiger Rohgeometrie.
  - Kapazitätsstatus ist known, conservative oder unknown.
  - Evidence Overlay kann betroffene Ports blockieren oder warnen.
- **Output:** pass = strukturelle Konnektoren aktiv; warning = aktiv, aber evidenzabhängig; blocked = keine strukturellen Ports für Tragwerk.

---

## 02 - SG-02 - Kompositionsgrammatik aus dem Bauteilpool

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 2
STRUCTURAL GRAMMAR: SG-02 - Bay grammar from the component pool
Source image: Abbau Aufbau handbook, printed pp. 60-63
  STRUCTURAL GRAMMAR  
Exact source taken from handbook
The handbook proposes basic reuse concepts such as single columns and slabs, or column
pairs with connecting beams. It also states that elements should be placed on a fixed
raster/grid and iterated against the floor-plan sketch.
Translation to already-sliced component-pool design
Ignoring cutting, this becomes a library of legal assembly types generated from available
pieces and repeated dimensions.
Rule
Generate bays only from allowed component formulas: W + S, C + S, C + B + S, B
+ S, W + W, S + S. The grid is extracted from the most repeated component
dimensions, not drawn freely first.
Minimum checks
- dominant slab lengths, wall widths and column heights are clustered
- each bay has vertical support plus horizontal spanning
- room modules are matched to valid bay sizes
- mismatches are solved by component substitution or adapter zones
- no bay is accepted without a connection family
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite verweist auf wiederholbare Grundkonzepte und Raster. Daraus folgt keine starre Formelgrammatik, sondern eine Port-Kompatibilitätsgrammatik: Bauteile dürfen nur zusammengesetzt werden, wenn ihre abstrahierten Konnektoren zusammenpassen und ein sinnvolles Raster entsteht.

### Minimaler Regelcheck

- **Ebene:** Assembly / Typkombination
- **Paket(e):** Structural + Semantic/Architectural
- **Repräsentation:** Struktureller Graph plus Raster-/Modulmodell: horizontale Tragelemente, vertikale/transferierende Stützen, Wiederholungsmaße.
- **Konnektoren und Ports:**
  - `structural.bearing_support` - bearing_side <-> support_side
  - `structural.node_joint` - joint_side <-> joint_side
  - `semantic.alignment_relation` - alignment_side <-> alignment_side
- **Prüfschritte:**
  - Jedes horizontale Element hat einen kompatiblen vertikalen oder transferierenden Support-Port.
  - Raster entsteht aus realen wiederkehrenden Bauteilmaßen.
  - Formelpaare wie W+S oder C+B+S sind nur Beispiele, keine harte Hauptregel.
  - Adapterzonen werden als explizite Konnektoren oder Zusatzbauteile geführt.
  - Keine Komposition ohne mindestens eine passende Port-zu-Port-Beziehung.
- **Output:** pass = gültige Komposition; warning = Adapter/Transfer nötig; blocked = keine kompatible tragende Portbeziehung.

---

## 03 - SG-03 - Lastpfad und vertikales Stapeln

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 3
STRUCTURAL GRAMMAR: SG-03 - Continuous load path and vertical stacking
Source image: Abbau Aufbau handbook, printed pp. 111-115
  STRUCTURAL GRAMMAR  
Exact source taken from handbook
The handbook notes that the new building must be stable as a whole and in each part, and that
structural calculations, positions, dimensions, loads, material quality and special construction
features must be documented.
Translation to already-sliced component-pool design
For component-pool design, every generated arrangement must show how loads move through
reused elements, connectors, adapters and finally into the foundation.
Rule
Prefer W over W and C over C. If a wall or column lands on a slab, the design must
introduce a transfer element or prove the slab/local bearing can carry it.
Minimum checks
- all gravity loads reach the foundation
- vertical structural lines are stacked where possible
- transfer beams or slabs are explicit when stacking breaks
- component capacities are not assumed from geometry alone
- the structural model matches the component IDs used in the plan
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite ist im Kern eine Lastpfadregel. Nicht "W über W" als Geschmacksregel ist entscheidend, sondern ob die Lasten als durchgehender Graph über Bearing/Support-Ports bis zum Fundament verfolgt werden können.

### Minimaler Regelcheck

- **Ebene:** Assembly / Gebäude
- **Paket(e):** Structural
- **Repräsentation:** Lastpfadgraph: belastete Fläche oder Linie -> bearing_support -> support -> tieferes Tragelement -> Fundament.
- **Konnektoren und Ports:**
  - `structural.bearing_support` - bearing_side <-> support_side
  - `structural.node_joint` - joint_side <-> joint_side
- **Prüfschritte:**
  - Jeder Decken-/Träger-Port bearing_side findet einen kompatiblen support_side-Port.
  - Vertikale Linien sind gestapelt oder ein Transfer ist explizit modelliert.
  - Transferbauteile haben Kapazitätsstatus known/conservative oder erzeugen warning.
  - Lastpfad endet nicht auf einer nicht geprüften Platte.
  - Der berechnete Graph referenziert die tatsächlich platzierten Component IDs.
- **Output:** pass = durchgehender Lastpfad; warning = expliziter Transfer oder Nachweis nötig; blocked = Lastpfad bricht ab.

---

## 04 - SG-04 - Aussteifung

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 4
STRUCTURAL GRAMMAR: SG-04 - Lateral stability and bracing system
Source image: Abbau Aufbau handbook, printed pp. 165-167
  STRUCTURAL GRAMMAR  
Exact source taken from handbook
In execution planning, the handbook says reused concrete creates special requirements for
foundations, vertical and horizontal load-bearing elements, and that new bracing elements
may be required for stabilization.
Translation to already-sliced component-pool design
A pool of slabs, walls, columns and beams may solve gravity loading but does not
automatically solve lateral stability.
Rule
Every whole-building variant must define a lateral stability system: reused shear
walls, new core, steel bracing, moment frame or hybrid system. Gravity grammar
and stability grammar are checked separately.
Minimum checks
- bracing system is visible in plan and section
- stability elements continue down to the foundation
- temporary bracing during assembly is possible
- cores/services do not cut critical stability lines
- new bracing is minimized but not avoided when necessary
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite behandelt horizontale Stabilität als eigenes System. Schwerkraftlogik und Aussteifungslogik dürfen nicht vermischt werden. Ein Gebäude kann einen gültigen Lastpfad haben und trotzdem aussteifungstechnisch unvollständig sein.

### Minimaler Regelcheck

- **Ebene:** Gebäude
- **Paket(e):** Structural + Logistics/Assembly
- **Repräsentation:** Stabilitätsgraph: aussteifende Wände/Kerne/Verbände, Deckenscheiben, Anschluss an Fundament und temporäre Montagezustände.
- **Konnektoren und Ports:**
  - `structural.node_joint` - joint_side <-> joint_side
  - `structural.restraint_fixing` - fixing_side <-> receiving_side
  - `logistics.support_interface` - component_support_side <-> base_support_side für temporäre Zustände
- **Prüfschritte:**
  - Aussteifungssystem ist in beiden Hauptachsen vorhanden oder wird neu ergänzt.
  - Aussteifung ist bis zum Fundament durchgebunden.
  - Deckenscheiben/Tragebenen sind an aussteifende Elemente angebunden.
  - Serviceöffnungen schneiden keine kritischen Stabilitätslinien ohne Nachweis.
  - Temporäre Aussteifung während der Montage ist als Zustand modelliert.
- **Output:** pass = Aussteifungssystem definiert; warning = neues/hybrides System nötig; blocked = keine Stabilitätskette.

---

## 05 - SG-05 - Montage und Installierbarkeit

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 5
STRUCTURAL GRAMMAR: SG-05 - Structural assembly checklist
Source image: Abbau Aufbau handbook, printed pp. 219-223
  STRUCTURAL GRAMMAR  
Exact source taken from handbook
During shell construction the handbook lists checks for foundations, floor plates, vertical
load-bearing elements, slabs and roofs: supports, connectors, joints, service penetrations and
damage inspection.
Translation to already-sliced component-pool design
The grammar is not finished at drawing level. It must become a site-checkable assembly
sequence.
Rule
A structural composition is valid only if each component has an installation step
and each step checks support, connector, joint, service opening and damage
state.
Minimum checks
- component arrives in the correct order
- bearing surface and support are checked before placement
- connector and joint match the detail
- service openings are coordinated with the component passport
- damaged elements are re-assessed before installation
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite ist keine neue Strukturformel, sondern eine Sequenz- und Zugänglichkeitsregel. Konnektoren müssen nicht nur kompatibel sein, sondern vor Ort erreichbar, installierbar und prüfbar bleiben.

### Minimaler Regelcheck

- **Ebene:** Assembly / Montage
- **Paket(e):** Logistics/Assembly + Structural + TGA + Evidence
- **Repräsentation:** Montagesequenzgraph: Bauteilreihenfolge, Hebepunkte, Zugangsvolumen, Konnektororte, Prüfzustände.
- **Konnektoren und Ports:**
  - `logistics.lifting_interface` - lifting_side <-> tool_side
  - `logistics.access_interface` - component_access_side <-> site_access_side
  - `structural.bearing_support` - bearing_side <-> support_side
  - `structural.restraint_fixing` - fixing_side <-> receiving_side
- **Prüfschritte:**
  - Bauteil kommt vor seinem Einbauschritt an.
  - Bearing/Support-Ports sind vor der Platzierung zugänglich und prüfbar.
  - Fixing-Ports werden nicht durch spätere Bauteile verdeckt, bevor sie ausgeführt sind.
  - TGA-Öffnungen kollidieren nicht mit tragenden Konnektoren.
  - Evidence-Zustand wird vor Einbau aktualisiert.
- **Output:** pass = montierbar; warning = Zugangs-/Sequenzrisiko; blocked = Konnektor nicht installierbar oder nicht prüfbar.

---

## 06 - PV-01 - Zustand und Nutzungsstatus

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 6
PERFORMANCE VALIDATION: PV-01 - Condition triage before design use
Source image: Abbau Aufbau handbook, printed pp. 35-37
  PERFORMANCE VALIDATION  
Exact source taken from handbook
The handbook requires visual inspection and preliminary testing to evaluate structural quality,
damage, cracks, spalling, corrosion, repairs and possible remaining service life.
Translation to already-sliced component-pool design
This becomes a filter on the pool before the designer can use a component as structure.
Rule
Every component receives a performance status: structural-use, limited
structural-use, repair-before-use, non-structural-use-only or rejected.
Minimum checks
- visible damage and deformation documented
- cracks, spalling and corrosion risk recorded
- past repairs identified if possible
- remaining service-life risk classified
- status is stored in the component passport
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite ist eine Eligibility-Regel. Schäden erzeugen keine eigenen Konnektoren, sondern verändern die Nutzbarkeit bestehender Konnektor-Ports.

### Minimaler Regelcheck

- **Ebene:** Bauteil / Evidence
- **Paket(e):** Evidence Overlay + Structural + Logistics + Semantic
- **Repräsentation:** Schadens-Overlay: Schadenszonen, Risslinien, Abplatzungen, Verformungen, Korrosionshinweise.
- **Konnektoren und Ports:**
  - `keine neuen Evidence-Konnektoren` - Evidence wirkt auf vorhandene Ports
  - `betroffen: structural.bearing_support` - bearing_side, support_side
  - `betroffen: structural.restraint_fixing` - fixing_side, receiving_side
  - `betroffen: logistics.lifting_interface` - lifting_side
  - `betroffen: semantic.visibility_relation` - visible_side
- **Prüfschritte:**
  - Schaden überlappt tragenden Bearing/Support-Port?
  - Schaden überlappt Fixing-/Drill-Port?
  - Schaden überlappt Hebe-Port?
  - Schaden reduziert sichtbare Wiederverwendungsqualität?
  - Schweregrad ist bekannt oder als unknown markiert.
- **Output:** structural-use, limited structural-use, repair-before-use, non-structural-only, rejected.

---

## 07 - PV-02 - Materialeigenschaften

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 7
PERFORMANCE VALIDATION: PV-02 - Material property validation
Source image: Abbau Aufbau handbook, printed pp. 38-39
  PERFORMANCE VALIDATION  
Exact source taken from handbook
The handbook lists tests for chloride content, pollutants, compressive/tensile strength,
E-modulus and density, including core samples and other test methods.
Translation to already-sliced component-pool design
Geometry alone cannot decide whether a component can be a slab, wall, column or beam in
the new building.
Rule
A component may carry structural load only when its material class is known or
conservatively assigned and the design loads fit that class.
Minimum checks
- compressive/tensile strength is tested or conservatively assigned
- E-modulus and density are known where needed
- chloride/pollutant risk is evaluated
- test data is linked to the exact component ID
- unknown properties trigger downgrade or additional testing
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite legt fest, ob strukturelle Konnektoren berechenbar sind. Materialwerte sind keine Ports, sondern Eigenschaften, die Connector Checks aktivieren, konservativ machen oder blockieren.

### Minimaler Regelcheck

- **Ebene:** Bauteil / Evidence
- **Paket(e):** Structural + Evidence
- **Repräsentation:** Materialdatensatz pro Component ID: Festigkeit, Steifigkeit, Dichte, Schadstoff-/Chloridrisiko, Evidenzquelle.
- **Konnektoren und Ports:**
  - `betroffen: structural.bearing_support` - bearing_side, support_side
  - `betroffen: structural.node_joint` - joint_side
  - `betroffen: structural.restraint_fixing` - fixing_side, receiving_side
  - `betroffen: logistics.lifting_interface` - lifting_side bei gewichtsbasiertem Handling
- **Prüfschritte:**
  - Druck-/Zugfestigkeit bekannt oder konservativ angesetzt.
  - E-Modul bekannt, wenn Steifigkeitsberechnung nötig ist.
  - Dichte bekannt oder plausibel angenommen für Eigengewicht/Handling.
  - Chlorid-/Schadstoffrisiko ist klassifiziert.
  - Prüfdaten sind mit der exakten Component ID verbunden.
- **Output:** pass = berechenbar; warning = konservativ berechenbar; blocked = strukturelle Ports nicht nutzbar bis Evidenz vorliegt.

---

## 08 - PV-03 - Bewehrung und No-Drill-Zonen

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 8
PERFORMANCE VALIDATION: PV-03 - Reinforcement and no-drill zone validation
Source image: Abbau Aufbau handbook, printed pp. 40-43
  PERFORMANCE VALIDATION  
Exact source taken from handbook
The handbook says reinforcement drawings should be checked against actual reinforcement,
and when drawings are missing, reinforcement position and bar diameter must be detected
and documented with suitable methods.
Translation to already-sliced component-pool design
For component-pool assembly, this defines where connectors, anchors, dowels, service
openings and adapters may or may not be placed.
Rule
No connector, drilling or service opening is allowed until reinforcement location,
cover and critical zones are checked for that component.
Minimum checks
- rebar position and direction are documented
- bar diameter or reinforcement class is known where relevant
- allowed drill zones and no-drill zones are mapped
- connector positions avoid critical reinforcement
- service penetrations are coordinated before site work
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite betrifft nicht jeden strukturellen Kontakt. Reines Auflagern kann möglich bleiben. Betroffen sind alle Aktionen, die bohren, schneiden, dübeln, ankern oder eine neue Öffnung erzeugen.

### Minimaler Regelcheck

- **Ebene:** Bauteil / Konnektor
- **Paket(e):** Evidence + Structural + TGA + Logistics
- **Repräsentation:** Bewehrungs-Overlay: Rebar-Linien/Zonen, Betondeckung, unbekannte Zonen, No-Drill-Zonen.
- **Konnektoren und Ports:**
  - `structural.restraint_fixing` - fixing_side, receiving_side
  - `tga.penetration_connection` - penetration_side, service_side
  - `logistics.lifting_interface` - lifting_side, falls gebohrter Hebeeinsatz nötig ist
- **Prüfschritte:**
  - Port liegt nicht in bekannter Rebar-Konfliktzone.
  - Unbekannte Bewehrungszone wird nicht ohne Scan verwendet.
  - Randabstand und Betondeckung passen zur Verbindung.
  - Bohr-/Schnittrichtung ist zulässig.
  - Service-Penetration ist vor Baustellenarbeit koordiniert.
- **Output:** pass = Port nutzbar; warning = Scan/Nachweis nötig; blocked = Port gesperrt.

---

## 09 - PV-04 - Validierungsmatrix

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 9
PERFORMANCE VALIDATION: PV-04 - Approval performance matrix
Source image: Abbau Aufbau handbook, printed pp. 95-99
  PERFORMANCE VALIDATION  
Exact source taken from handbook
For ZiE/vBG documentation, the handbook lists required proofs across load-bearing capacity,
serviceability, fire, hygiene/health/environment, accessibility, acoustic protection, energy
saving and thermal protection.
Translation to already-sliced component-pool design
The component grammar needs an approval filter. A layout that fits spatially still fails if it
cannot satisfy the required performance categories.
Rule
Each assembly and whole-building variant must pass a validation matrix:
structure, serviceability, fire, health/environment, accessibility, acoustics, energy
and thermal protection.
Minimum checks
- proof exists for load-bearing capacity and serviceability
- fire and escape-route logic are checked
- acoustic and thermal requirements are assigned
- accessibility and use safety are not broken by component placement
- missing proofs are listed as design blockers
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite ist keine einzelne Fachregel, sondern eine Aggregation. Sie sammelt Ergebnisse aus Struktur, Brand, Energie, Akustik, Barrierefreiheit, Gesundheit/Umwelt und Nachweisen.

### Minimaler Regelcheck

- **Ebene:** Variante / Gebäude
- **Paket(e):** Aggregator über alle Packages
- **Repräsentation:** Validierungsmatrix mit Status je Leistungsfeld und Liste fehlender Nachweise.
- **Konnektoren und Ports:**
  - `keine eigenen Konnektoren` - liest Status aus allen Package-Konnektoren und Evidence-Effekten
- **Prüfschritte:**
  - Tragfähigkeit und Gebrauchstauglichkeit nicht blocked.
  - Brandschutzstatus für relevante Assemblies vorhanden.
  - Hülle/Energie nur dort geprüft, wo Bauteile envelope role haben.
  - TGA-Penetrationen sind abgedichtet oder als offen markiert.
  - Fehlende Nachweise sind blocker oder warning, nicht unsichtbar.
- **Output:** variant_pass, variant_warning, variant_blocked, missing_evidence_list.

---

## 10 - PV-05 - Brandschutz auf Assembly-Ebene

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 10
PERFORMANCE VALIDATION: PV-05 - Fire performance belongs to the assembly
Source image: Abbau Aufbau handbook, printed pp. 117-119
  PERFORMANCE VALIDATION  
Exact source taken from handbook
The handbook states that reinforced concrete is non-combustible, but fire performance
depends on function, cross-section, concrete cover and installation context. A beam on
lower-rated steel consoles follows the weaker support rating.
Translation to already-sliced component-pool design
A reused concrete element cannot be approved by material identity alone. Its new support and
connector can govern the fire rating.
Rule
Assembly fire rating = component rating + connector/support rating + installation
context. The lowest-performing part controls the rule.
Minimum checks
- required fire class is assigned per zone
- connectors and steel adapters are protected where needed
- concrete cover and cross-section are checked
- fire compartments and escape routes follow the component layout
- fire proof is updated after connection changes
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite zeigt: Brandverhalten entsteht in der Assembly. Betonmaterial allein reicht nicht. Der schwächste relevante Anschluss, Support oder Schutzaufbau kann die Bewertung bestimmen.

### Minimaler Regelcheck

- **Ebene:** Assembly / Brandvalidierung
- **Paket(e):** Fire Validation liest Structural + Energy/Layer
- **Repräsentation:** Brandkette: Bauteil -> Support/Konnektor -> Schutzlage -> Nutzung/Brandabschnitt.
- **Konnektoren und Ports:**
  - `liest: structural.bearing_support` - bearing_side, support_side
  - `liest: structural.restraint_fixing` - fixing_side, receiving_side
  - `optional: energy.layer_continuity` - layer_side, falls Brandschutzlage anschließt
  - `optional: energy.penetration_seal` - penetration_side, seal_side
- **Prüfschritte:**
  - Geforderte Feuerwiderstandsklasse ist dem Bereich zugeordnet.
  - Support/Konnektor/Adapter ist bewertet oder geschützt.
  - Stahlteile sind geschützt, wenn sie brandrelevant sind.
  - Betondeckung/Querschnitt ist belegt oder als Nachweisbedarf markiert.
  - Fluchtwege/Brandabschnitte werden durch Layout nicht verschlechtert.
- **Output:** pass, warning = Schutzdetail nötig, blocked = schwächste Stelle unter Anforderung.

---

## 11 - PV-06 - Hülle und Energie

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 11
PERFORMANCE VALIDATION: PV-06 - Envelope and thermal validation
Source image: Abbau Aufbau handbook, printed pp. 123-125
  PERFORMANCE VALIDATION  
Exact source taken from handbook
The handbook requires thermal conductivity, U-value, insulation thickness and energy concept
checks when reused reinforced-concrete elements touch exterior climate, roof or ground
conditions.
Translation to already-sliced component-pool design
A component can be excellent structurally but weak as an envelope element without added
layers.
Rule
When a reused concrete component becomes facade, roof or ground-contact
element, it must be paired with an envelope build-up that meets U-value,
condensation and thermal-bridge requirements.
Minimum checks
- thermal role is tagged: interior, envelope, roof or ground contact
- U-value is calculated for the full build-up
- insulation and moisture layers are defined
- thermal bridges at connectors are checked
- energy concept is updated around the component layout
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite gilt nur für Bauteile mit Hüllenrolle. Innenliegende Bauteile brauchen keine Hüllen-Konnektoren. Thermische Brücken sind Risiko-Zonen, nicht automatisch Konnektoren.

### Minimaler Regelcheck

- **Ebene:** Bauteil / Assembly
- **Paket(e):** Energy / Envelope
- **Repräsentation:** Thermisches Boundary-Modell: Boundary-Flächen, Layer-Flächen, Penetrationszonen, thermische Risikozonen.
- **Konnektoren und Ports:**
  - `energy.boundary_continuity` - boundary_side <-> boundary_side
  - `energy.layer_continuity` - layer_side <-> layer_side
  - `energy.penetration_seal` - penetration_side <-> seal_side
- **Prüfschritte:**
  - Hüllenrolle ist gesetzt: interior, envelope, roof oder ground.
  - U-Wert wird für den gesamten Aufbau berechnet, nicht für Beton allein.
  - Dämm-/Feuchte-/Schutzlagen sind definiert.
  - Penetrationen haben Seal-Ports oder bleiben blocker.
  - Thermal bridge risk zones sind gelistet und behandelt.
- **Output:** not_applicable, pass, warning = Aufbau fehlt, blocked = Hüllenrolle ohne gültiges Boundary-/Layer-Modell.

---

## 12 - PV-07 - LCA und Umwelt

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 12
PERFORMANCE VALIDATION: PV-07 - Environmental and LCA validation
Source image: Abbau Aufbau handbook, printed pp. 135-141
  PERFORMANCE VALIDATION  
Exact source taken from handbook
The handbook describes LCA through quantities, life-cycle modules and GWP. For reused
elements, data and comparisons with conventional new-concrete variants are needed to
calculate avoided impacts.
Translation to already-sliced component-pool design
Component-pool design should be ranked not only by fit and structure, but also by
embodied-carbon benefit and added adapter/logistics burden.
Rule
Each design variant receives an environmental score: reused mass, avoided new
concrete, new adapter material, transport effort, connector count and potential
future disassembly.
Minimum checks
- reused element quantities are extracted from the model
- new material added for adapters is quantified
- transport and handling assumptions are recorded
- variant is compared to a new-concrete baseline
- high-carbon savings are not cancelled by excessive adapters
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite beschreibt eine Variantenbewertung, keinen Port-Check. Konnektoren sind relevant, wenn sie Zusatzmaterial, Transport, Montageaufwand oder spätere Demontierbarkeit beeinflussen.

### Minimaler Regelcheck

- **Ebene:** Variante / Gebäude
- **Paket(e):** LCA Aggregator liest Quantities + Connector Properties
- **Repräsentation:** Mengen- und Szenariomodell: wiederverwendete Masse, neues Material, Adapter/Konnektoren, Transport, Baseline, Disassembly-Annahme.
- **Konnektoren und Ports:**
  - `liest: structural.restraint_fixing` - method_family, material, reversibility
  - `liest: structural.bearing_support` - adapter_required, steel_support_required
  - `liest: logistics.*` - transport distance, fixation, handling
- **Prüfschritte:**
  - Wiederverwendete Menge ist aus dem Modell extrahiert.
  - Zusatzmaterial für Adapter/Konnektoren ist quantifiziert.
  - Transport-/Handlingannahmen sind dokumentiert.
  - Vergleich mit Neubau-Baseline ist vorhanden.
  - Hohe Einsparung wird nicht durch Adapter/Logistik aufgehoben.
- **Output:** GWP estimate, avoided impact estimate, adapter/logistics burden, variant ranking.

---

## 13 - PV-08 - Finale Prüfung vor Montage

<details>
<summary>Exakte Textreferenz aus der PDF-Seite</summary>

```text
Abbau Aufbau translated rulebook - Structural grammar + Performance validation - one page per rule
Page 13
PERFORMANCE VALIDATION: PV-08 - Final pre-installation validation
Source image: Abbau Aufbau handbook, printed pp. 219-223
  PERFORMANCE VALIDATION  
Exact source taken from handbook
The handbook states that if elements are damaged during storage or transport, they must be
assessed again before installation using the investigation methods described earlier.
Translation to already-sliced component-pool design
Approval at catalogue stage is not enough. Component status can change during storage,
transport and handling.
Rule
Before installation, every component receives a final go/no-go check: undamaged,
repair-required, downgraded to non-structural use, substituted or rejected.
Minimum checks
- visual condition is checked on delivery
- transport/storage damage is documented
- component ID matches the installation drawing
- repair or downgrade decision is recorded
- no component is installed with unresolved damage status
Source PDF: https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

</details>

### Eigene Ableitung

Die Seite ist ein letzter Evidence-Refresh. Sie erzeugt keine neue Designlogik, sondern prüft, ob Bauteil und kritische Ports seit Katalogisierung, Lagerung und Transport unverändert nutzbar sind.

### Minimaler Regelcheck

- **Ebene:** Installation / Evidence
- **Paket(e):** Evidence + Logistics + Structural
- **Repräsentation:** Delivery-/Pre-Install-Overlay: aktueller Zustand, ID-Match, Transportschaden, Status kritischer Konnektor-Ports.
- **Konnektoren und Ports:**
  - `betroffen: structural.bearing_support` - bearing_side, support_side
  - `betroffen: structural.restraint_fixing` - fixing_side, receiving_side
  - `betroffen: logistics.lifting_interface` - lifting_side
  - `betroffen: logistics.support_interface` - component_support_side
- **Prüfschritte:**
  - Component ID passt zum Montageplan.
  - Bearing/Support/Fixing/Lifting-Port-Zonen sind unbeschädigt.
  - Transport-/Lagerschäden sind dokumentiert.
  - Reparatur, Downgrade, Ersatz oder Ablehnung ist entschieden.
  - Kein Einbau mit unresolved damage status.
- **Output:** install_ok, repair_before_install, downgrade_use, substitute_component, reject.

---

# Kompakte Endstruktur

Die 13 Seiten ergeben nicht 13 gleichartige Konnektor-Familien. Sie lassen sich minimal so ordnen:

```text
A. Component Eligibility: Seite 1, 6, 7, 8, 13
B. Structural Composition: Seite 2, 3, 4
C. Assembly / Installability: Seite 5, 10
D. Envelope / Services / Performance: Seite 9, 11
E. Environmental Variant Evaluation: Seite 12
```

Minimaler Systemablauf:

```text
Bauteil
-> Paket-Abstraktion
-> Konnektor mit Eigenschaften
-> Port innerhalb des Konnektors
-> Port-zu-Port-Kompatibilität
-> Package-spezifischer Check
-> pass / warning / blocked / needs_evidence
```

Nicht als Konnektoren modellieren:

```text
monolithische Kontinuität
Schadenszonen
No-Drill-Zonen
Blocked Zones
Thermal Bridges
Materialwerte
LCA-Scores
Validierungsmatrix
```

Diese Dinge sind Repräsentationsrelationen, Eigenschaften, Overlays oder Aggregationsergebnisse. Sie beeinflussen Ports, sind aber nicht selbst anschließbare Ports.