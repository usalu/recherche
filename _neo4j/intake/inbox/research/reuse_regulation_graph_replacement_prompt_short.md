# Short Research Prompt — Replace Weak Vocabularies with Regulation Graph Vocabulary

## Goal

Research all projects and create a compact replacement vocabulary for the regulation/proof layer.

The new target vocabulary is only:

```text
Regulierungsfrage
Nachweisforderung
Regelwerk
```

These should **replace / absorb** weak existing vocabularies such as:

```text
Huerde
Schadstoff
Norm
RechtlicheBedingung
PruefungNachweis
Bauproduktstatus
Leistungsanforderung
```

Do **not** replace these anchor nodes:

```text
Projekt
Bauteilgruppe
Bauteiltyp
Material
Land
```

These anchors should be connected to the new vocabulary.

Evidence stays **on edges**, not as separate evidence nodes.

---

## Migration rule

Map old vocabulary nodes into the new three vocabularies.

```text
Norm → Regelwerk
RechtlicheBedingung → Regulierungsfrage or Regelwerk
PruefungNachweis → Nachweisforderung
Bauproduktstatus → BauproduktstatusFrage + ProduktstatusUndLeistungserklaerung
Leistungsanforderung → Regulierungsfrage + Nachweisforderung
Huerde → Regulierungsfrage or Nachweisforderung
Schadstoff → SchadstoffFrage + specific Schadstoffpruefung / check node
```

The result should make the old vocabularies optional or parkable in the clean graph view.

---

## Target vocabulary

### Regulierungsfrage

```text
ReuseDokumentationFrage
RueckbauUndBauteilernteFrage
BauproduktstatusFrage
TragwerkssicherheitFrage
BrandschutzFrage
BauphysikFrage
SchadstoffFrage
HygieneElektroFunktionFrage
GenehmigungsFrage
HaftungGewaehrleistungFrage
```

### Nachweisforderung

```text
Bauteilidentifikation
HerkunftsUndRueckbaudokumentation
ZustandsUndMassaufnahme
Standsicherheitsnachweis
Materialpruefung
Brandschutznachweis
Bauphysiknachweis
Schadstoffpruefung
ProduktstatusUndLeistungserklaerung
GenehmigungsOderZustimmungsbedarf
Befestigungsnachweis
Elektrosicherheitsnachweis
HygieneUndReinigungsnachweis
FormaldehydOderEmissionsnachweis
AsbestCheck
KMFCheck
PCBCheck
PAKCheck
SchwermetallOderBleifarbeCheck
HolzschutzmittelCheck
SicherheitsglasInfo
U_WertOderEnergieInfo
DauerhaftigkeitRestlebensdauer
```

### Regelwerk

Research and extend from project evidence.

Seed list:

```text
DIN SPEC 91484
DIN SPEC 91525
VDI 6210
VDI/GVSS 6202
KrWG §6 / §45
MBO / LBO
MVV TB / VV TB
EU CPR 305/2011
EU CPR 2024/3110
BauPG
DIBt ZiE / vBG / abZ / aBG
GefStoffV
TRGS 519 / 521 / 524
REACH
POP Regulation
DIN EN 13501
DIN 4102 / 4108 / 4109
GEG
Eurocodes EN/DIN EN 1990–1999
EN/DIN EN 1090
CEN/TS 1090-201
SCI P427
SIA 269
SIA 380/1
UKCA / CE marking
OIB-Richtlinien
Dutch Bbl / Building Decree
Belgian regional building rules
```

Only connect country-specific rules to projects in the correct jurisdiction. Otherwise mark `comparative_only`.

---

## Replacement mapping examples

```text
Huerde: Bauproduktstatus
→ Regulierungsfrage: BauproduktstatusFrage
→ Nachweisforderung: ProduktstatusUndLeistungserklaerung

Huerde: Brandschutzkonflikt
→ Regulierungsfrage: BrandschutzFrage
→ Nachweisforderung: Brandschutznachweis

Huerde: Datenluecke
→ Regulierungsfrage: ReuseDokumentationFrage
→ Nachweisforderung: Bauteilidentifikation / HerkunftsUndRueckbaudokumentation

Huerde: Technische_Freigabe
→ Regulierungsfrage: GenehmigungsFrage
→ Nachweisforderung: GenehmigungsOderZustimmungsbedarf

Schadstoff: Asbest
→ Regulierungsfrage: SchadstoffFrage
→ Nachweisforderung: AsbestCheck
→ Regelwerk: GefStoffV / TRGS 519

Schadstoff: KMF
→ Regulierungsfrage: SchadstoffFrage
→ Nachweisforderung: KMFCheck
→ Regelwerk: TRGS 521

Schadstoff: Formaldehyd
→ Regulierungsfrage: SchadstoffFrage
→ Nachweisforderung: FormaldehydOderEmissionsnachweis
→ Regelwerk: REACH / ChemVerbotsV / product-emission rules

Leistungsanforderung: Tragfaehigkeit
→ Regulierungsfrage: TragwerkssicherheitFrage
→ Nachweisforderung: Standsicherheitsnachweis

Leistungsanforderung: Brandschutz
→ Regulierungsfrage: BrandschutzFrage
→ Nachweisforderung: Brandschutznachweis

Norm: EN 1090
→ Regelwerk: EN/DIN EN 1090

PruefungNachweis: Materialpruefung
→ Nachweisforderung: Materialpruefung
```

---

## Required graph pattern

Use anchor nodes only on the left.

```text
Projekt / Bauteilgruppe / Bauteiltyp / Material / Land
→ Regulierungsfrage
→ Nachweisforderung
→ Regelwerk
```

Recommended edge types:

```text
TRIGGERS_REGULIERUNGSFRAGE
ERFORDERT_NACHWEIS
GESTUETZT_AUF_REGELWERK
GILT_IN_LAND
```

Old vocabulary replacement edges:

```text
OLD_NODE_REPLACED_BY
OLD_NODE_MAPPED_TO
OLD_EDGE_MIGRATED_TO
```

---

## Evidence on edges

Every new or migrated edge needs:

```text
evidence_status
evidence_type
source_url
source_quote
applicability_reason
missing_info
confidence
```

Allowed status:

```text
case_documented
rule_documented
expert_inferred
missing_evidence
not_applicable
comparative_only
```

---

## Required output

Return compact Markdown with these tables.

### 1. Replacement vocabulary

```text
old_label | old_node | replacement_label | replacement_node | action | reason
```

### 2. Extended target vocabulary

```text
target_label | node_id | name | core/optional/park | replaces_old_nodes
```

### 3. Project mapping

```text
project | anchor_node | triggered_Regulierungsfrage | Nachweisforderung | Regelwerk | evidence_status | missing_info
```

### 4. Component mapping

```text
project | bauteilgruppe | bauteiltyp | material | Regulierungsfrage | Nachweisforderung | Regelwerk | evidence_status
```

### 5. CSV-ready edge import

```text
from_node_id | edge_type | to_node_id | evidence_status | source_url | source_quote | applicability_reason | missing_info | confidence
```

---

## Final instruction

Keep it short and graph-ready.

The research result should show how to **replace old weak vocabularies** with the three clean target vocabularies, while keeping `Projekt`, `Bauteilgruppe`, `Bauteiltyp`, `Material`, and `Land` as stable anchors.
