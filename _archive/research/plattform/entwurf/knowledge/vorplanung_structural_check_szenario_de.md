# Structural Check in der Vorplanung  
## Szenario: User platziert Bauteile nacheinander und das System prüft die grobe Tragwerkslogik

**Ziel dieses Dokuments**  
Dieses Dokument erklärt den **Structural Check nur für die Vorplanung**.  
Es zeigt schrittweise, was passiert, wenn ein User Bauteile platziert, verbindet und eine grobe Tragstruktur aufbaut.

**Wichtige Grundlage**  
Die Geometrie-Generatoren sind bereits gelaufen.  
Beim Platzieren ist der Bauteilpass bereits vorhanden.

```text
Bauteilpass existiert
→ enthält Structural Geometry
→ enthält Subzonen
→ enthält Auflagerzonen
→ enthält Ports
→ enthält Massen / Volumen
→ enthält Nachweisstatus
→ enthält Warnungen

Beim Platzieren:
keine neuen Generatoren
nur Transformation + aktiver Structural Check
```

---

# 1. Was Structural Check in der Vorplanung bedeutet

## 1.1 Ziel

Der Structural Check in der Vorplanung beantwortet nicht:

```text
Ist das statisch endgültig nachgewiesen?
```

Sondern:

```text
Ist die Tragwerksidee grundsätzlich plausibel?
Gibt es erkennbare Auflager?
Gibt es einen groben Lastpfad?
Gibt es harte Konflikte?
Welche Nachweise fehlen?
Welche Verbindung braucht Engineering?
Welche Variante ist tragwerkslogisch besser?
```

## 1.2 Output in der Vorplanung

Der Structural Check liefert eine frühe Ampel:

```yaml
structural_preplanning_status:
  pass: geometrisch plausibel
  warning: tragwerkslogisch kritisch oder unvollständig
  engineering_required: Fachnachweis erforderlich
  invalid: grob unzulässig / harter Konflikt
  positive: Tragwerkslogik verbessert sich
  blocked_by_missing_data: Prüfung nicht möglich
```

## 1.3 Was er nicht macht

```text
keine finale Statik
keine Bemessung
keine Bewehrungsberechnung
keine Tragfähigkeitsfreigabe
keine Bohrfreigabe
keine Brandschutzfreigabe
keine Ausführungsplanung
```

---

# 2. Structural Check: Eingaben

## 2.1 Aus dem vorhandenen Bauteilpass

```yaml
from_bauteilpass:
  component_id: required
  typology: required
  material: required
  mass: estimated_or_measured
  structural_geometry: available
  sub_zone_map: available_if_mixed
  bearing_zones: available
  support_edges: available
  load_direction_candidates: available
  span_direction_candidates: available
  connector_ports: available
  opening_map: available
  damage_zones: optional
  evidence_status: required
```

## 2.2 Aus dem aktiven Entwurf

```yaml
from_design_graph:
  piece_instances: required
  transforms: required
  active_roles: optional
  connections: optional
  support_edges: derived
  adjacency: derived
  spaces: optional
  temporary_states: optional
```

## 2.3 Aus Projektdefaults

```yaml
project_defaults:
  gravity_direction: z_negative
  minimum_bearing_length_default: project_specific
  support_tolerance: project_specific
  allowable_preplanning_statuses:
    - pass
    - warning
    - positive
    - engineering_required
    - invalid
```

---

# 3. Structural Check: Hauptlogik

Der Structural Check arbeitet in fünf Ebenen:

```text
1. Bauteil-Ebene
   Ist das einzelne Bauteil strukturell verständlich?

2. Placement-Ebene
   Ist die Platzierung plausibel?

3. Connection-Ebene
   Ist die Verbindung geometrisch und tragwerkslogisch möglich?

4. Support-Graph-Ebene
   Gibt es einen durchgehenden Lastpfad?

5. Variant-Ebene
   Welche Variante ist tragwerkslogisch günstiger?
```

---

# 4. Beispiel-Szenario

Wir nutzen ein allgemeines Szenario mit wiederverwendeten Bauteilen.

```yaml
components:
  AA_MIX_001:
    type: mixed_fragment
    zones:
      - slab_zone
      - beam_zone
      - column_stub_zone
      - internal_transition_zones
    mass_status: estimated
    structural_capacity: unknown
    reinforcement: partial_or_missing

  WALL_001:
    type: wall_panel
    role_candidate: vertical_support
    structural_capacity: unknown_or_partial

  BEAM_NEW_001:
    type: new_adapter_beam
    role_candidate: support_adapter
    structural_capacity: assumed_engineerable_but_not_checked

  COLUMN_001:
    type: reclaimed_column
    role_candidate: vertical_point_support
    structural_capacity: unknown_or_partial
```

---

# 5. Structural Rule Tree

```text
Structural Check
│
├── 1. Component Structural Readiness
├── 2. Role Compatibility
├── 3. Bearing + Support Geometry
├── 4. Load Path Plausibility
├── 5. Connection + Intrusive Actions
├── 6. Temporary Stability
├── 7. Damage + Weak Zones
└── 8. Variant Structural Summary
```

---

# 6. Schritt 1 — User wählt ein Bauteil aus

## 6.1 User-Aktion

```yaml
action: select_component
component_id: AA_MIX_001
```

## 6.2 System intern

Das System lädt den vorhandenen Bauteilpass.

```yaml
loaded_from_bauteilpass:
  structural_geometry: available
  sub_zone_map: available
  bearing_zones: available
  ports: available
  mass: available_estimated
  structural_capacity: unknown
  reinforcement_status: partial_or_missing
```

## 6.3 Structural Rules

```yaml
rules_run:
  - structural_geometry_available
  - structural_typology_classified
  - mixed_component_subzone_required
  - structural_evidence_status
```

## 6.4 Ergebnis

```yaml
result:
  structural_geometry_available: pass
  structural_typology_classified: pass
  mixed_component_subzone_required: pass
  structural_evidence_status: engineering_required
  overall: selectable_for_structural_preplanning
```

## 6.5 UI

```text
Bauteil ist auswählbar.

Structural Badge:
"Strukturell vorprüfbar"

Warnung:
"Tragfähigkeit unbekannt. Bewehrung unvollständig."
```

---

# 7. Schritt 2 — User platziert das erste Bauteil frei im Raum

## 7.1 User-Aktion

```yaml
action: place_piece
piece: P001
source_component: AA_MIX_001
position: [0, 0, 0]
```

## 7.2 System intern

```text
Piece-Instanz P001 erzeugen
vorhandene Structural Geometry transformieren
Subzonen transformieren
Auflagerzonen transformieren
Ports transformieren
Design Graph aktualisieren
```

## 7.3 Structural Rules

```yaml
rules_run:
  - placement_has_support_context
  - self_weight_known
  - temporary_stability_precheck
  - mixed_component_not_simple_slab
```

## 7.4 Ergebnis

```yaml
result:
  placement_has_support_context: warning
  self_weight_known: pass
  temporary_stability_precheck: engineering_required
  mixed_component_not_simple_slab: pass
  overall: placed_but_structurally_unresolved
```

## 7.5 UI

```text
Bauteil wird platziert.

Meldung:
"Bauteil liegt im Entwurf, aber hat noch keinen definierten Tragkontext."

Status:
warning / engineering_required
```

## 7.6 Bedeutung

```text
Das Bauteil darf als Vorplanungsobjekt im Modell liegen.
Es ist aber noch kein tragendes System.
```

---

# 8. Schritt 3 — User weist dem Bauteil eine grobe Rolle zu

## 8.1 User-Aktion

```yaml
action: assign_structural_role
piece: P001
requested_role: horizontal_spanning_element
```

## 8.2 System intern

Das System vergleicht:

```text
angeforderte Rolle
gegen
Bauteiltypologie
gegen
Subzonen
gegen
vorhandene Structural Geometry
```

## 8.3 Structural Rules

```yaml
rules_run:
  - role_typology_compatibility
  - mixed_component_role_check
  - span_direction_candidate_check
  - required_support_condition_check
```

## 8.4 Ergebnis

```yaml
result:
  role_typology_compatibility: warning
  mixed_component_role_check: engineering_required
  span_direction_candidate_check: pass
  required_support_condition_check: warning
  overall: role_possible_but_not_simple
```

## 8.5 UI

```text
Meldung:
"Rolle als horizontales tragendes Element ist konzeptionell möglich,
aber das Bauteil ist ein Mischfragment und darf nicht wie eine einfache Platte behandelt werden."
```

---

# 9. Schritt 4 — User versucht, das Mischbauteil als einfache Platte zu deklarieren

## 9.1 User-Aktion

```yaml
action: assign_structural_role
piece: P001
requested_role: simple_slab
```

## 9.2 Structural Rules

```yaml
rules_run:
  - mixed_component_subzone_required
  - role_typology_compatibility
```

## 9.3 Ergebnis

```yaml
result:
  mixed_component_subzone_required: invalid
  role_typology_compatibility: invalid
  overall: invalid
```

## 9.4 UI

```text
Rote Meldung:
"Dieses Bauteil kann nicht als einfache Platte behandelt werden."

Grund:
"Es enthält Unterzug- und Stützen-Subzonen. Die strukturelle Prüfung muss subzonenbasiert erfolgen."
```

## 9.5 Systemaktion

```yaml
requested_role_rejected: true
active_role_remains: mixed_fragment_or_composite_candidate
```

---

# 10. Schritt 5 — User platziert eine Wand als mögliches Auflager

## 10.1 User-Aktion

```yaml
action: place_piece
piece: P002
source_component: WALL_001
near_piece: P001
```

## 10.2 System intern

```text
P002 erzeugen
P002 Structural Geometry transformieren
Nähe zu P001 prüfen
mögliche Auflagerbeziehungen suchen
```

## 10.3 System erkennt Kandidaten

```yaml
support_candidate:
  supported_piece: P001
  supported_port: slab-edge-bearing
  support_piece: P002
  support_port: wall-top-bearing
  relation: possible_line_support
```

## 10.4 Structural Rules

```yaml
rules_run:
  - support_candidate_detection
  - port_pair_structural_compatibility
  - bearing_overlap_precheck
  - support_orientation_check
```

## 10.5 Ergebnis

```yaml
result:
  support_candidate_detection: pass
  port_pair_structural_compatibility: pass
  bearing_overlap_precheck: warning
  support_orientation_check: pass
  overall: possible_support_candidate
```

## 10.6 UI

```text
System zeigt eine gelbe Auflagerlinie.

Meldung:
"Potentielles Linienauflager erkannt."
```

---

# 11. Schritt 6 — User bestätigt die Vorplanungs-Auflagerverbindung

## 11.1 User-Aktion

```yaml
action: create_preliminary_structural_connection
supported_piece: P001
support_piece: P002
```

## 11.2 System intern

Ein Preliminary Structural Connection Object wird erzeugt.

```yaml
preliminary_structural_connection:
  id: PSC001
  supported: P001
  supporter: P002
  relation: line_support_candidate
  status: preliminary
```

## 11.3 Structural Rules

```yaml
rules_run:
  - bearing_overlap_precheck
  - load_transfer_direction_check
  - support_piece_role_check
  - structural_capacity_evidence_check
  - connection_detail_need_check
```

## 11.4 Ergebnis

```yaml
result:
  bearing_overlap_precheck: warning
  load_transfer_direction_check: pass
  support_piece_role_check: pass
  structural_capacity_evidence_check: engineering_required
  connection_detail_need_check: engineering_required
  overall: structurally_plausible_but_unverified
```

## 11.5 UI

```text
Verbindung wird als Vorplanungsauflager gespeichert.

Status:
"tragwerkslogisch plausibel, aber nicht nachgewiesen"

Fehlende Daten:
- Tragfähigkeit Wand
- Tragfähigkeit Mischbauteil
- Mindestauflagerlänge
- Anschlussdetail
```

---

# 12. Schritt 7 — System baut einen Support Graph

## 12.1 System intern

Nach jeder tragwerksrelevanten Verbindung wird ein Support Graph aktualisiert.

```yaml
support_graph:
  nodes:
    - P001
    - P002
  edges:
    - P002_supports_P001
```

## 12.2 Structural Rules

```yaml
rules_run:
  - load_path_graph_update
  - unsupported_zone_detection
  - support_count_check
  - eccentric_support_warning
```

## 12.3 Ergebnis

```yaml
result:
  load_path_graph_update: pass
  unsupported_zone_detection: warning
  support_count_check: warning
  eccentric_support_warning: warning
  overall: partial_load_path
```

## 12.4 UI

```text
System zeigt:
"Teilweiser Lastpfad vorhanden."

Warnung:
"Einige Zonen des Mischbauteils sind noch nicht unterstützt."
```

---

# 13. Schritt 8 — User fügt Adapterträger hinzu

## 13.1 User-Aktion

```yaml
action: place_piece
piece: P003
source_component: BEAM_NEW_001
role: support_adapter
under_piece: P001
```

## 13.2 System intern

```text
P003 wird als neuer Support / Adapter erkannt
Ports von P003 werden mit Auflagerzonen von P001 verglichen
Support Graph wird erweitert
```

## 13.3 Structural Rules

```yaml
rules_run:
  - adapter_as_valid_support_component
  - bearing_overlap_precheck
  - load_path_continuity_precheck
  - support_redundancy_check
  - tolerance_fit_precheck
```

## 13.4 Ergebnis

```yaml
result:
  adapter_as_valid_support_component: pass
  bearing_overlap_precheck: pass_or_warning
  load_path_continuity_precheck: positive
  support_redundancy_check: positive
  tolerance_fit_precheck: warning
  overall: structural_logic_improved
```

## 13.5 UI

```text
Blaue / positive Meldung:
"Adapterträger verbessert die Auflager- und Lastpfadlogik."

Orange:
"Nachweis und Anschlussdetail bleiben erforderlich."
```

---

# 14. Schritt 9 — User verbindet Mischbauteil mit Adapterträger

## 14.1 User-Aktion

```yaml
action: create_preliminary_structural_connection
supported_piece: P001
support_piece: P003
connection_type: support_on_new_beam
```

## 14.2 Structural Rules

```yaml
rules_run:
  - port_pair_structural_compatibility
  - bearing_overlap_precheck
  - load_path_continuity_precheck
  - connector_family_preselection
  - post_installed_rebar_risk
  - grout_gap_tolerance_precheck
```

## 14.3 Ergebnis

```yaml
result:
  port_pair_structural_compatibility: pass
  bearing_overlap_precheck: pass_or_warning
  load_path_continuity_precheck: positive
  connector_family_preselection: warning
  post_installed_rebar_risk: engineering_required
  grout_gap_tolerance_precheck: warning
  overall: structurally_preferred_but_engineering_required
```

## 14.4 UI

```text
Meldung:
"Auflager auf neuem Träger ist als Vorplanungsstrategie sinnvoll."

Fehlende nächste Daten:
- Anschlussdetail
- Verguss- / Fugenstrategie
- Bewehrungs- oder Ankerkonzept
- statischer Nachweis
```

---

# 15. Schritt 10 — User platziert eine Stütze unter den Adapterträger

## 15.1 User-Aktion

```yaml
action: place_piece
piece: P004
source_component: COLUMN_001
under_piece: P003
```

## 15.2 System intern

```text
Stütze wird als vertikales Punktauflager erkannt
P003 kann Lasten zu P004 übertragen
Support Graph wird erweitert
```

## 15.3 Structural Rules

```yaml
rules_run:
  - vertical_support_alignment
  - column_base_support_check
  - load_path_continuity_precheck
  - support_eccentricity_check
  - column_capacity_evidence_check
```

## 15.4 Ergebnis

```yaml
result:
  vertical_support_alignment: pass_or_warning
  column_base_support_check: engineering_required
  load_path_continuity_precheck: positive
  support_eccentricity_check: warning
  column_capacity_evidence_check: engineering_required
  overall: load_path_improved_but_unverified
```

## 15.5 UI

```text
System zeigt Lastpfad:

P001 Mischbauteil
↓
P003 Adapterträger
↓
P004 Stütze
↓
Fundament / Boden noch offen

Status:
"Lastpfad verbessert, aber noch nicht vollständig bis Fundament."
```

---

# 16. Schritt 11 — User platziert Fundament / Basis

## 16.1 User-Aktion

```yaml
action: place_piece
piece: P005
source_component: FOUNDATION_OR_BASE
under_piece: P004
```

## 16.2 Structural Rules

```yaml
rules_run:
  - column_to_base_support_check
  - load_path_to_ground_check
  - bearing_overlap_precheck
  - foundation_capacity_status
```

## 16.3 Ergebnis

```yaml
result:
  column_to_base_support_check: pass_or_warning
  load_path_to_ground_check: pass
  bearing_overlap_precheck: warning
  foundation_capacity_status: engineering_required
  overall: complete_preliminary_load_path
```

## 16.4 UI

```text
System zeigt:
"Durchgehender vorläufiger Lastpfad erkannt."

Status:
pass für geometrische Lastpfad-Plausibilität
engineering_required für Tragfähigkeitsnachweise
```

---

# 17. Schritt 12 — System prüft ununterstützte Zonen

## 17.1 Trigger

```yaml
trigger: support_graph_updated
```

## 17.2 System intern

Das System vergleicht:

```text
alle Auflagerzonen des Bauteils
gegen
tatsächliche Support-Graph-Kanten
```

## 17.3 Structural Rules

```yaml
rules_run:
  - unsupported_edge_detection
  - cantilever_precheck
  - span_length_precheck
  - subzone_support_coverage
```

## 17.4 Ergebnis

```yaml
result:
  unsupported_edge_detection: warning
  cantilever_precheck: warning
  span_length_precheck: engineering_required
  subzone_support_coverage: warning
  overall: partial_unresolved_support_zones
```

## 17.5 UI

```text
System markiert:
- nicht unterstützte Kanten
- mögliche Kragarme
- Subzonen ohne klaren Auflagerbezug

Hinweis:
"Diese Bereiche in nächster Phase prüfen oder mit weiteren Auflagern / Adaptern lösen."
```

---

# 18. Schritt 13 — User versucht in eine tragwerksrelevante Zone zu bohren

## 18.1 User-Aktion

```yaml
action: request_drilling
piece: P001
zone: beam_column_transition
```

## 18.2 Structural Rules

```yaml
rules_run:
  - intrusive_action_gate
  - no_drill_zone_enforcement
  - reinforcement_evidence_check
  - structural_zone_sensitivity
```

## 18.3 Ergebnis

```yaml
result:
  intrusive_action_gate: invalid
  no_drill_zone_enforcement: invalid
  reinforcement_evidence_check: engineering_required
  structural_zone_sensitivity: critical
  overall: invalid
```

## 18.4 UI

```text
Rote Meldung:
"Nicht in diese Zone bohren."

Grund:
"Übergangszone Unterzug/Stütze ist tragwerksrelevant. Bewehrungslage unbekannt."
```

## 18.5 Systemaktion

```yaml
drilling_request:
  accepted: false
  suggested_alternatives:
    - alternative_port_zone
    - adapter_connection
    - dry_reversible_connection
    - request_rebar_scan
```

---

# 19. Schritt 14 — User wählt alternative trockene Verbindung

## 19.1 User-Aktion

```yaml
action: select_connection_strategy
connection: PSC002
strategy: dry_reversible_adapter
```

## 19.2 Structural Rules

```yaml
rules_run:
  - connector_family_match
  - reversibility_precheck
  - load_transfer_direction_check
  - local_bearing_stress_warning
  - fire_context_warning
```

## 19.3 Ergebnis

```yaml
result:
  connector_family_match: warning
  reversibility_precheck: positive
  load_transfer_direction_check: pass_or_warning
  local_bearing_stress_warning: engineering_required
  fire_context_warning: engineering_required_if_relevant
  overall: promising_strategy_for_preplanning
```

## 19.4 UI

```text
Positive Meldung:
"Trockene reversible Verbindung passt zur Wiederverwendungsstrategie."

Warnung:
"Lokale Druck- und Anschlussnachweise fehlen."
```

---

# 20. Schritt 15 — User verschiebt Bauteil und erzeugt Exzentrizität

## 20.1 User-Aktion

```yaml
action: move_piece
piece: P001
offset_from_support_axis: large
```

## 20.2 Structural Rules

```yaml
rules_run:
  - bearing_overlap_precheck
  - support_eccentricity_check
  - overturning_risk_precheck
  - load_path_continuity_precheck
```

## 20.3 Ergebnis

```yaml
result:
  bearing_overlap_precheck: warning
  support_eccentricity_check: warning_or_invalid
  overturning_risk_precheck: engineering_required
  load_path_continuity_precheck: warning
  overall: structurally_weaker_variant
```

## 20.4 UI

```text
System zeigt:
"Exzentrische Lagerung erhöht Risiko."

Variante wird nicht automatisch verboten,
aber schlechter bewertet als zentrische Lagerung.
```

---

# 21. Schritt 16 — User erstellt alternative Variante mit besserem Auflager

## 21.1 User-Aktion

```yaml
action: duplicate_variant
variant_A: eccentric_support
variant_B: aligned_support
```

## 21.2 System intern

Der Structural Checker vergleicht die Varianten.

## 21.3 Structural Rules

```yaml
rules_run:
  - variant_load_path_score
  - variant_support_coverage_score
  - variant_engineering_risk_count
  - variant_invalid_issue_count
```

## 21.4 Ergebnis

```yaml
variant_comparison:
  Variant_A:
    support_alignment: weak
    engineering_required_count: high
    warnings: high
    recommendation: only_develop_if_spatial_reason_strong

  Variant_B:
    support_alignment: better
    engineering_required_count: medium
    warnings: medium
    recommendation: structurally_preferred_for_next_phase
```

## 21.5 UI

```text
System empfiehlt:
"Variante B ist tragwerkslogisch günstiger."

Aber:
"Variante A kann weiterverfolgt werden, wenn räumliche oder architektonische Gründe stark sind."
```

---

# 22. Schritt 17 — Globaler Structural Check

## 22.1 User-Aktion

```yaml
action: run_global_structural_precheck
```

## 22.2 System intern

Der Checker analysiert den gesamten Design Graph.

```text
alle Pieces
alle Preliminary Connections
alle Support Relations
alle Adapter
alle ununterstützten Zonen
alle engineering_required Punkte
alle invalid Punkte
```

## 22.3 Structural Rules

```yaml
global_structural_rules:
  - all_load_paths_plausible
  - unsupported_zones_summary
  - invalid_structural_actions_summary
  - engineering_required_summary
  - temporary_stability_summary
  - adapter_dependency_summary
  - next_phase_structural_tasks
```

## 22.4 Ergebnis

```yaml
global_structural_precheck:
  structural_concept_plausible: true
  complete_final_proof: false
  approval_ready: false

  pass:
    - component_geometries_readable
    - preliminary_support_graph_exists
    - load_path_to_base_detected

  positive:
    - adapter_beam_improves_support_logic
    - aligned_support_variant_is_better

  warnings:
    - some_edges_under_supported
    - eccentric_support_in_variant_A
    - tolerance_and_joint_details_missing
    - temporary_stability_not_defined

  engineering_required:
    - structural_capacity_all_reclaimed_components
    - bearing_length_proof
    - connector_capacity
    - reinforcement_scan_before_drilling
    - column_base_and_foundation_check
    - adapter_beam_design

  invalid:
    - drilling_in_beam_column_transition
    - treating_mixed_fragment_as_simple_slab
```

## 22.5 UI

```text
Structural Dashboard:

Grün:
"Vorläufiger Lastpfad vorhanden"

Blau:
"Adapterträger verbessert System"

Gelb:
"Einige Zonen / Toleranzen / temporäre Zustände offen"

Orange:
"Statische Nachweise erforderlich"

Rot:
"Bohrung in Übergangszone verboten"
"AA_MIX_001 nicht als einfache Platte behandeln"
```

---

# 23. Structural Check als Algorithmus

## 23.1 Pseudocode

```pseudo
on_piece_placed(piece):
    load bauteilpass
    transform structural_geometry
    add piece to design_graph

    run component_structural_readiness(piece)
    run role_typology_check(piece)
    run placement_support_context(piece)
    run temporary_stability_precheck(piece)

    update structural_dashboard
```

```pseudo
on_connection_candidate(piece_A, port_A, piece_B, port_B):
    check port_pair_compatibility
    check bearing_overlap
    check support_direction
    check collision_and_tolerance
    estimate load_path_relation

    if geometry plausible:
        create preliminary_connection
    else:
        mark invalid_or_warning
```

```pseudo
on_support_graph_update():
    build support_graph from structural connections
    find unsupported_edges
    find cantilever_zones
    find load_path_to_ground
    find eccentric_supports
    find adapter_dependencies

    classify:
        pass
        warning
        engineering_required
        invalid
```

```pseudo
on_intrusive_action(piece, zone, action):
    if zone is no_drill:
        return invalid

    if reinforcement unknown:
        return engineering_required_or_invalid

    if action affects structural zone:
        return engineering_required

    else:
        return warning_or_pass
```

---

# 24. Structural Rule Result Schema

```yaml
structural_rule_result:
  rule_id: string
  category: structural
  status: pass | warning | positive | engineering_required | invalid | blocked_by_missing_data
  affected_piece_ids: []
  affected_zones: []
  affected_ports: []
  affected_connections: []
  message: string
  reason: string
  missing_data: []
  required_next_data: []
  suggested_actions: []
  severity: info | low | medium | high | critical
  confidence: low | medium | high
```

## Beispiel

```yaml
structural_rule_result:
  rule_id: load_path_continuity_precheck
  category: structural
  status: engineering_required
  affected_piece_ids:
    - P001
    - P003
    - P004
    - P005
  affected_connections:
    - PSC002
    - PSC003
  message: Vorläufiger Lastpfad erkannt, aber nicht statisch nachgewiesen.
  reason: Lasten können geometrisch von Mischbauteil über Adapterträger und Stütze zur Basis geführt werden.
  missing_data:
    - Tragfähigkeit Mischbauteil
    - Tragfähigkeit Adapterträger
    - Stützenkapazität
    - Fundamentnachweis
    - Anschlusskapazitäten
  required_next_data:
    - statisches Konzept
    - Bewehrungsscan
    - Auflagerlängen
    - Anschlussdetails
  suggested_actions:
    - Auflagerachsen besser ausrichten
    - zusätzliche Unterstützung prüfen
    - trockene Adapterverbindung prüfen
  severity: high
  confidence: medium
```

---

# 25. Was der User sieht

## 25.1 In der 3D-Szene

```text
grüne Linien:
plausible Auflager / Lastpfade

gelbe Linien:
kritische oder unklare Auflager

orange Linien:
engineering_required Verbindungen

rote Zonen:
invalid / no-drill / harte Konflikte

blaue Markierungen:
strukturell positive Verbesserung, z.B. Adapterträger
```

## 25.2 Im Structural Panel

```text
Piece-Level:
- strukturelle Typologie
- Subzonen
- Masse
- bekannte / unbekannte Nachweise

Connection-Level:
- Portpaar
- Auflagerüberdeckung
- Anschlussfamilie
- Nachweisbedarf

Graph-Level:
- Lastpfad
- ununterstützte Zonen
- temporäre Stabilität
- Variantenvergleich
```

## 25.3 Im Vorplanungs-Dashboard

```text
Structural Concept:
plausibel / kritisch / nicht geeignet

Main Risks:
Nachweise, Auflager, Bohrungen, Temporärzustände

Next Phase Tasks:
Statisches Konzept
Bewehrungsscan
Tragfähigkeitsnachweis
Anschlussdetail
Hebe- und Montagekonzept
```

---

# 26. Was in der Vorplanung bewusst offen bleibt

```text
Momententragfähigkeit
Querkrafttragfähigkeit
Durchstanznachweis
Bewehrungsnachweis
Ankerbemessung
Verbundnachweis
Brandverhalten des Anschlusses
Montagezustandsnachweis
Fundamentbemessung
Gebrauchstauglichkeit
Schwingungen
Durchbiegung
Rissbreiten
```

Diese Punkte werden nicht versteckt.  
Sie erscheinen als:

```yaml
status: engineering_required
```

---

# 27. Typische Structural-Check-Szenarien

## 27.1 Bauteil frei platziert

```yaml
status: warning
message: Bauteil hat noch keinen Tragkontext.
```

## 27.2 Bauteil mit plausibler Auflagerkante

```yaml
status: engineering_required
message: Auflager geometrisch plausibel, Tragfähigkeit fehlt.
```

## 27.3 Mischbauteil als einfache Platte

```yaml
status: invalid
message: Mischbauteil braucht Subzonenlogik.
```

## 27.4 Neuer Adapterträger hinzugefügt

```yaml
status: positive_with_engineering_required
message: Lastpfad verbessert, Adapter muss nachgewiesen werden.
```

## 27.5 Lastpfad bis Fundament erkannt

```yaml
status: pass_for_preplanning
message: Vorläufiger Lastpfad vorhanden.
```

## 27.6 Bohrung in unbekannter Bewehrungszone

```yaml
status: invalid_or_engineering_required
message: Nicht bohren ohne Bewehrungsnachweis.
```

## 27.7 Exzentrische Lagerung

```yaml
status: warning
message: Exzentrizität erhöht Risiko.
```

## 27.8 Beschädigte Auflagerkante

```yaml
status: engineering_required_or_invalid
message: Schaden liegt in Auflagerzone.
```

---

# 28. Kernaussage

Der Structural Check in der Vorplanung ist kein Statikprogramm.

Er ist ein **tragwerkslogischer Plausibilitäts- und Risikoprüfer**:

```text
Er nutzt vorhandene Bauteilpässe.
Er transformiert vorhandene Structural Geometry.
Er prüft Subzonen, Ports, Auflager und Lastpfade.
Er erkennt harte Fehler.
Er markiert sinnvolle Strategien.
Er sammelt offene Nachweise.
Er hilft Varianten zu vergleichen.
```

Die zentrale Frage ist:

```text
Ist diese Tragwerksidee sinnvoll genug,
um sie in die nächste Planungsphase mitzunehmen?
```

Nicht:

```text
Ist sie schon baubar freigegeben?
```
