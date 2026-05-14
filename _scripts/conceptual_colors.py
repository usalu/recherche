"""
Conceptual Color Schema for Recherche Datenmodell
Based on semantic domains and interactions

Color Philosophy:
- Warm colors (red, orange, yellow) for energy, action, materials, process
- Cool colors (blue, teal, purple) for knowledge, data, people, governance
- Red = barriers, constraints, critical issues
- Green = circular economy, reuse, sustainability, feedback loops
- Purple = knowledge, methodology, learning
- Dark = structural, meta, governance
"""

# Semantic color mapping
CONCEPT_COLORS = {
    # DOMAIN 1: BARRIERS & CONSTRAINTS (Red family - problem/risk)
    "Huerde": "#E74C3C",           # bright red - immediate barriers
    "HuerdeKategorie": "#C0392B",  # dark red - category/classification
    "Schadstoff": "#E8655D",       # coral-red - contamination/hazard
    "Leistungsanforderung": "#DC7633", # orange-red - demands/requirements
    
    # DOMAIN 2: ACTORS & GOVERNANCE (Blue family - people/management)
    "Akteur": "#2E86C1",           # strong blue - primary actor
    "Akteurrolle": "#5DADE2",      # lighter blue - role/function
    "Akteurtyp": "#85C1E9",        # pale blue - type/category
    "RechtlicheBedingung": "#1B6FAA", # darker blue - legal/binding
    "Ressourcenquelle": "#3498DB", # bright blue - resource provider
    "Programm": "#2980B9",         # medium blue - program/initiative
    
    # DOMAIN 3: CIRCULAR ECONOMY & REUSE (Green family - sustainability)
    "Wiederverwendungskette": "#27AE60",     # bright green - reuse chain (hub)
    "WiederverwendungsArt": "#1ABC9C",      # teal-green - reuse type/method
    "Aufbereitungsverfahren": "#16A085",    # darker teal - preparation/processing
    "Rueckbauverfahren": "#48C774",         # lighter green - deconstruction method
    "Funktionswechsel": "#58D68D",          # medium green - adaptive reuse
    
    # DOMAIN 4: MATERIALS & COMPONENTS (Orange/Brown family - physical/tangible)
    "Material": "#D68910",         # burnt orange - raw material
    "Materialgruppe": "#E59866",   # lighter orange - material category
    "Bauteilgruppe": "#D2691E",    # chocolate - component group
    "Bauteiltyp": "#F39C12",       # warm orange - component type
    "Bauteilebene": "#E8B71B",     # golden-orange - hierarchical level
    "Bauteilzustand": "#D35400",   # dark orange - component condition
    "Bauobjekt": "#BF5A1D",        # darker brown - building object
    "Bauwerk": "#A04000",          # very dark brown - building structure (core)
    
    # DOMAIN 5: BUILDING STRUCTURE & DESIGN (Teal family - technical/structural)
    "Bausystem": "#17A2B8",        # teal - construction system
    "Bauweise": "#00BCD4",         # cyan - construction method
    "Tragwerksprinzip": "#0097A7", # dark teal - structural principle
    "Tragwerkstyp": "#00ACC1",     # medium cyan - structural type
    "Verbindungstechnik": "#26C6DA", # lighter cyan - connection technique
    "Bauobjektklasse": "#4DB8D8",  # pale cyan - object classification
    "Bauobjektrolle": "#2FBFAF",   # medium teal - object role
    "BauaufgabeIntervention": "#20B2AA", # sea green - intervention task
    
    # DOMAIN 6: PROCESS & TIMELINE (Yellow/Gold family - flow/energy)
    "Prozessphase": "#F1C40F",     # bright yellow - process step
    "Beschaffungsweg": "#F39C12",  # orange-yellow - procurement path
    "Logistik": "#E8B71B",         # golden - logistics/movement
    
    # DOMAIN 7: KNOWLEDGE & METHODOLOGY (Purple family - intellect/learning)
    "Quelle": "#8E44AD",           # purple - source/reference
    "Methode": "#9B59B6",          # bright purple - methodology
    "Kennwertdefinition": "#AF7AC5", # lighter purple - key value definition
    "Norm": "#D7BDE2",             # pale purple - standard/norm
    "PruefungNachweis": "#9D4EDD", # deep purple - verification/proof
    
    # DOMAIN 8: DIGITAL & DATA (Indigo family - information/technology)
    "Software": "#3F51B5",         # indigo - software tool
    "Tool": "#5C6BC0",             # lighter indigo - tool/instrument
    "Tooltyp": "#7986CB",          # pale indigo - tool category
    "SoftwareDigitaltool": "#512DA8", # dark indigo - digital tool
    "Datenqualitaet": "#455A64",   # blue-grey - data quality (meta)
    "Dokumenttyp": "#37474F",      # slate - document/record
    
    # DOMAIN 9: QUALITY & CERTIFICATION (Pink/Magenta family - standards/assurance)
    "ZertifizierungBewertungssystem": "#D81B60", # magenta - certification system
    "Nutzung": "#C2185B",          # dark pink - use/occupancy
    
    # DOMAIN 10: ECONOMIC & PROGRAMS (Green-Gold transition - growth/value)
    "Wirtschaft": "#E67E22",       # warm orange - economics/value
    "Foerderprogramm": "#27AE60",  # green - funding program (growth)
    
    # DOMAIN 11: SPATIAL & LOCATION (Dark Blue - anchoring/reference)
    "Projekt": "#E74C3C",          # bright RED - core project (special - central to all)
    "Ort": "#2C3E50",              # very dark blue - location/place
    "Stadt": "#34495E",            # dark slate - city/urban
    "Land": "#1B6FAA",             # darker blue - country/region
    
    # DOMAIN 12: META & GOVERNANCE (Dark Grey - structure/system)
    "Status": "#7F8C8D",           # grey - state/status
    "GraphVersion": "#95A5A6",     # lighter grey - versioning/meta
    "Kontextmerkmal": "#455A64",   # slate-grey - context marker
    "BewertungslogikAbgrenzung": "#37474F", # dark slate - evaluation boundary
}

# Interaction patterns (for relationship styling)
DOMAIN_INTERACTIONS = {
    # Cross-domain relationships
    "Projekt → Akteur (BETEILIGT_AN)": "bridge between red (project) and blue (people)",
    "Projekt → Bauwerk": "red to dark brown - central to physical structure",
    "Projekt → Stadt (LIEGT_IN_STADT)": "red to dark blue - project anchored in location",
    "Bauteilgruppe → Material (NUTZT_MATERIAL)": "chocolate to burnt orange - physical composition",
    "Bauteilgruppe → Huerde (HAT_HUERDE)": "chocolate to red - constraint identification",
    "Wiederverwendungskette → Bauteilgruppe → Projekt": "green circle loop - closed reuse chain",
    "Akteur → Foerderprogramm": "blue to green - people enabling circular programs",
    "Prozessphase → Aufbereitungsverfahren": "yellow to teal - process leading to treatment",
    "Material → Norm → PruefungNachweis": "orange → purple → purple - material compliance chain",
}

PALETTE_HARMONIES = {
    "Warm Group": ["Material", "Bauteilgruppe", "Leistungsanforderung", "Wirtschaft"],
    "Cool Group": ["Akteur", "Programm", "Bausystem", "Software"],
    "Reuse Cycle": ["Wiederverwendungskette", "WiederverwendungsArt", "Aufbereitungsverfahren"],
    "Barrier Group": ["Huerde", "HuerdeKategorie", "Schadstoff"],
    "Process Flow": ["Prozessphase", "Beschaffungsweg", "Logistik"],
    "Knowledge Chain": ["Quelle", "Methode", "Norm", "PruefungNachweis"],
}

print("Semantic Color Schema Applied")
print(f"Total nodes: {len(CONCEPT_COLORS)}")
print(f"Domain groups: {len(PALETTE_HARMONIES)}")
