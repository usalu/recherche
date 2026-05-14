# Recherche Datenmodell - Semantic Color Schema

Generated for Neo4j Browser graph visualization. Organized by conceptual domain and semantic meaning.

Last updated: May 14, 2026

---

## Color Philosophy

The schema uses hue families to group related concepts by meaning, not just aesthetics:

- **Red** = Problems, Barriers, Constraints, Risks
- **Blue** = People, Organizations, Governance, Legal
- **Green/Teal** = Circular Economy, Reuse, Sustainability, Loops
- **Orange/Brown** = Physical Materials, Components, Tangible Objects
- **Yellow/Gold** = Process Flow, Timeline, Energy, Progression
- **Purple** = Knowledge, Standards, Methodology, Learning
- **Indigo/Slate** = Digital, Data, Information, Technology
- **Teal/Cyan** = Structural Systems, Technical, Engineering
- **Grey** = Meta, System, Versioning, Administrative

---

## Domain Groups

### DOMAIN 1: BARRIERS & CONSTRAINTS (Red)
Risk, problems, negative constraints that impede reuse

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Huerde | #E74C3C | #C0392B | 50px | Immediate barrier/obstacle |
| HuerdeKategorie | #C0392B | #A93226 | 65px | Barrier classification (hub) |
| Schadstoff | #E8655D | #CB4335 | 45px | Contamination/hazard |

---

### DOMAIN 2: ACTORS & GOVERNANCE (Blue)
People, organizations, roles, legal structures

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Akteur | #2E86C1 | #1B5A96 | 55px | Primary stakeholder (hub) |
| Akteurrolle | #5DADE2 | #3498DB | 45px | Role/function |
| Akteurtyp | #85C1E9 | #6BA3D6 | 45px | Actor category |
| RechtlicheBedingung | #1B6FAA | #0D47A1 | 45px | Legal requirement |
| Ressourcenquelle | #3498DB | #2980B9 | 45px | Resource provider |
| Programm | #2980B9 | #1F618D | 50px | Program/initiative (hub) |

---

### DOMAIN 3: CIRCULAR ECONOMY & REUSE (Green/Teal)
Sustainability, reuse chains, closed loops

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Wiederverwendungskette | #27AE60 | #1D7E4E | 60px | Reuse chain (central hub) |
| WiederverwendungsArt | #1ABC9C | #117A65 | 45px | Reuse type/method |
| Aufbereitungsverfahren | #16A085 | #0D6B52 | 45px | Preparation/treatment |
| Rueckbauverfahren | #48C774 | #229954 | 45px | Deconstruction method |
| Funktionswechsel | #58D68D | #52BE80 | 45px | Adaptive reuse/function change |

---

### DOMAIN 4: MATERIALS & COMPONENTS (Orange/Brown)
Physical, tangible objects and their composition

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Bauwerk | #A04000 | #6B3410 | 55px | Building structure (core entity) |
| Material | #D68910 | #B8641D | 50px | Raw material (hub) |
| Materialgruppe | #E59866 | #D68054 | 55px | Material category (hub) |
| Bauteilgruppe | #D2691E | #A04000 | 55px | Component group (hub) |
| Bauteiltyp | #F39C12 | #D68910 | 45px | Component type |
| Bauteilebene | #E8B71B | #D4AF37 | 45px | Hierarchical level |
| Bauteilzustand | #D35400 | #BA4A00 | 45px | Component condition |
| Bauobjekt | #BF5A1D | #8B4513 | 45px | Building object |
| Bauobjektklasse | #CD853F | #B8860B | 45px | Object class |
| Bauobjektrolle | #DAA520 | #C79900 | 45px | Object role |
| BauaufgabeIntervention | #CC8844 | #A0522D | 45px | Task/intervention |

---

### DOMAIN 5: BUILDING STRUCTURE & DESIGN (Teal/Cyan)
Technical, structural, and design principles

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Bausystem | #17A2B8 | #0D7C8F | 45px | Construction system |
| Bauweise | #00BCD4 | #0097A7 | 45px | Construction method |
| Tragwerksprinzip | #0097A7 | #00838F | 45px | Structural principle |
| Tragwerkstyp | #00ACC1 | #00838F | 45px | Structural type |
| Verbindungstechnik | #26C6DA | #00BCD4 | 45px | Connection technique |

---

### DOMAIN 6: PROCESS & TIMELINE (Yellow/Gold)
Flow, progression, energy, logistics

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Prozessphase | #F1C40F | #D4AF37 | 45px | Process step/phase |
| Beschaffungsweg | #F39C12 | #D68910 | 45px | Procurement path |
| Logistik | #E8B71B | #D4AF37 | 45px | Logistics/movement |

---

### DOMAIN 7: KNOWLEDGE & METHODOLOGY (Purple)
Intellect, learning, standards, verification

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Quelle | #8E44AD | #6C3483 | 45px | Source/reference (hub) |
| Methode | #9B59B6 | #76448A | 45px | Methodology |
| Kennwertdefinition | #AF7AC5 | #8B4FB8 | 45px | Key value definition |
| Norm | #D7BDE2 | #C39BD3 | 45px | Standard/norm |
| PruefungNachweis | #9D4EDD | #7B2CBF | 45px | Verification/proof |
| ZertifizierungBewertungssystem | #D81B60 | #AD1457 | 45px | Certification system |

---

### DOMAIN 8: DIGITAL & DATA (Indigo/Slate)
Information, technology, data quality

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Software | #3F51B5 | #283593 | 45px | Software tool |
| Tool | #5C6BC0 | #3F51B5 | 45px | General tool |
| Tooltyp | #7986CB | #5C6BC0 | 45px | Tool category |
| SoftwareDigitaltool | #512DA8 | #311B92 | 45px | Digital tool (hub) |
| Dokumenttyp | #37474F | #263238 | 35px | Document type |
| Datenqualitaet | #455A64 | #37474F | 35px | Data quality (meta) |

---

### DOMAIN 9: SPATIAL & LOCATION (Dark Blue)
Geographic anchoring, reference frames

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Projekt | #E74C3C | #C0392B | 68px | Central project node (SPECIAL - red override) |
| Stadt | #34495E | #1B2F42 | 55px | City/urban location |
| Land | #1B6FAA | #0D3B66 | 60px | Country/region (hub) |
| Ort | #2C3E50 | #1A252F | 45px | Place/location |

---

### DOMAIN 10: ECONOMIC & VALUE (Green-Gold)
Economics, funding, growth

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Wirtschaft | #E67E22 | #D35400 | 45px | Economic aspects |
| Foerderprogramm | #27AE60 | #1D7E4E | 45px | Funding program |

---

### DOMAIN 11: UTILITY & USE (Teal)
Occupancy and use

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Nutzung | #00ACC1 | #00838F | 45px | Use/occupancy |
| Leistungsanforderung | #DC7633 | #BA4A00 | 45px | Performance requirement |

---

### DOMAIN 12: META & GOVERNANCE (Grey)
System-level, administrative, versioning

| Label | Color | Border | Size | Meaning |
|-------|-------|--------|------|---------|
| Status | #7F8C8D | #566573 | 35px | State/status (meta) |
| GraphVersion | #95A5A6 | #7F8C8D | 35px | Version/snapshot (meta) |
| Kontextmerkmal | #455A64 | #37474F | 45px | Context marker |
| BewertungslogikAbgrenzung | #37474F | #263238 | 45px | Evaluation boundary |

---

## Relationship Color Mapping

Relationships inherit dominant domain colors to show interaction direction:

**Within-Domain Relationships** (same color family):
- BETEILIGT_AN (Blue) - Actor involvement
- NUTZT_MATERIAL (Orange) - Material usage
- HAT_HUERDE (Red) - Barrier attachment
- TEIL_VON_KETTE (Green) - Reuse chain membership
- HAT_PROZESSPHASE (Yellow) - Process sequence

**Cross-Domain Relationships** (bridge colors):
- LIEGT_IN_STADT / LIEGT_IN_LAND (Red to Dark Blue) - Project to location
- NUTZT_BAUWERK (Red to Brown) - Project to structure
- HAT_MATERIALGRUPPE (Orange hub)
- ZITIERT_QUELLE (Purple hub - knowledge reference)
- TEIL_VON_PROGRAMM (Green hub - sustainability initiative)

---

## How to Apply

In Neo4j Browser:

1. Run any Cypher query that returns nodes
2. Paste this command into the query editor:
   ```
   :style http://localhost:8765/neo4j_style.grass
   ```
3. The stylesheet loads and persists for the session

To serve the file locally:
```bash
python _scripts/serve_grass.py
```

---

## Design Rationale

- **Saturation**: Hub nodes (Projekt, Akteur, Material, Quelle) are larger and more saturated
- **Brightness**: Lighter shades for categories and types, darker for core entities
- **Complementarity**: Red (barriers) vs Green (solutions) creates visual tension where they interact
- **Semantic Consistency**: Moving through the graph, color shifts indicate domain changes
- **Accessibility**: Colors chosen to be distinguishable in grayscale and colorblind-friendly

---

## File Information

- Generated: 2026-05-14
- Total labels: 77
- Total relationship types: 46
- Primary tool: Neo4j Browser GraSS stylesheet
- Served from: `_neo4j/neo4j_style.grass`
- Python generator: `_scripts/serve_grass.py`
