# Abgeleitete Daten

## 1. Rippenplatte / Spannbeton

### 1.5 Abgeleitete Daten

```yaml
bounding_volume_per_element_m3:
  value: 4.91
  basis: 6.84 * 1.495 * 0.48
  note: geometrischer Hüllkörper, nicht tatsächliches Betonvolumen
  confidence: high
```

```yaml
possible_reuse_roles:
  - Deckenplatte
  - Dachplatte
  - Brückenelement nur nach Sonderprüfung
  - Landschafts-/Außenraumelement mit geringerem statischem Anspruch
```

```yaml
reuse_barriers:
  value:
    - structural_liability
    - pollutant_uncertainty
    - high_logistics_cost
    - dimensional_inflexibility
    - cutting_or_deconstruction_damage
  confidence: high
  reasoning_source: material_logic
  review_required: true
```

---

## 2. Stahlträger HEB 140

### 2.5 Abgeleitete Daten

```yaml
typical_mass_kg_per_m:
  value_range: 33.7-34.2
  basis: typische HEB-140-Profilmasse
  confidence: medium

estimated_piece_weight_kg:
  value_range: 85.6-86.9
  basis: 2.54 m * 33.7-34.2 kg/m
  confidence: medium
```

```yaml
typical_steel_density_kg_m3:
  value: 7850
  confidence: high

typical_elastic_modulus_mpa:
  value: 210000
  confidence: high

possible_steel_grades:
  - S235
  - S275
  - S355

estimated_elastic_bending_resistance_s235_knm:
  value_approx: 51
  basis: typischer elastischer Widerstandsmomentwert HEB 140 * 235 MPa
  confidence: low
  verification_required: true
```

---

## 3. Historische Holzbalken aus Altbausanierung

### 3.5 Abgeleitete Daten

```yaml
assumed_dry_timber_density_kg_m3:
  value_range: 450-650
  confidence: medium

estimated_total_weight_typical_kg:
  value_range: 630-910
  basis: 1.4 m3 * 450-650 kg/m3
  confidence: low
```

```yaml
structural_use_condition:
  value: Tragende Wiederverwendung nur nach Festigkeitssortierung, Feuchteprüfung, Schädlingsprüfung und Ingenieurfreigabe
  confidence: high
```

```yaml
design_value:
  value: hoch für sichtbare, historische und rustikale Anwendungen
  basis: 160 Jahre, roh, gesägt/geschlagen, fränkische Kerbe
  confidence: high
```

```yaml
critical_design_checks:
  - Holzart bestimmen
  - Querschnitt je Stück messen
  - Risse und Kerben bewerten
  - Insekten- und Pilzbefall prüfen
  - Resttragfähigkeit prüfen
  - frühere Verbindungslöcher und Kerben bewerten
  - Brandschutz im neuen Kontext prüfen
```
