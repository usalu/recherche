"""
Generate the Neo4j Browser GraSS stylesheet with correct Unicode icon chars
and serve it on http://localhost:8765/neo4j_style.grass

Usage:
    python _scripts/serve_grass.py

Then in Neo4j Browser paste:
    :style http://localhost:8765/neo4j_style.grass
"""

import http.server
import socketserver
import threading

# Font Awesome 4 unicode characters (must be embedded as real chars, not escapes)
def fa(code: int) -> str:
    return chr(code)

ICONS = {
    "Projekt":                    fa(0xF275),  # industry
    "Bauwerk":                    fa(0xF1AD),  # building-o
    "Stadt":                      fa(0xF041),  # map-marker
    "Land":                       fa(0xF0AC),  # globe
    "Ort":                        fa(0xF041),  # map-marker
    "Akteur":                     fa(0xF007),  # user
    "Akteurrolle":                fa(0xF0C0),  # users
    "Akteurtyp":                  fa(0xF02B),  # tag
    "Bauteilgruppe":              fa(0xF1B2),  # cube
    "Bauteiltyp":                 fa(0xF0AD),  # wrench
    "Bauteilebene":               fa(0xF07B),  # folder
    "Bausystem":                  fa(0xF013),  # cog
    "Bauweise":                   fa(0xF085),  # cogs
    "Bauteilzustand":             fa(0xF080),  # bar-chart
    "Bauobjektklasse":            fa(0xF1B2),  # cube
    "Bauobjektrolle":             fa(0xF007),  # user
    "BauaufgabeIntervention":     fa(0xF0AD),  # wrench
    "Material":                   fa(0xF1B2),  # cube
    "Materialgruppe":             fa(0xF0B1),  # briefcase
    "Wiederverwendungskette":     fa(0xF0C1),  # chain/link
    "WiederverwendungsArt":       fa(0xF1B8),  # recycle
    "Prozessphase":               fa(0xF017),  # clock-o
    "Aufbereitungsverfahren":     fa(0xF021),  # refresh
    "Rueckbauverfahren":          fa(0xF0E2),  # undo
    "Beschaffungsweg":            fa(0xF07A),  # shopping-cart
    "Logistik":                   fa(0xF0D1),  # truck
    "Ressourcenquelle":           fa(0xF0E7),  # bolt
    "Funktionswechsel":           fa(0xF021),  # refresh
    "Huerde":                     fa(0xF071),  # exclamation-triangle
    "HuerdeKategorie":            fa(0xF05E),  # ban
    "Schadstoff":                 fa(0xF188),  # bug
    "Norm":                       fa(0xF0F6),  # file-text-o
    "RechtlicheBedingung":        fa(0xF0E3),  # gavel
    "ZertifizierungBewertungssystem": fa(0xF0A3),  # certificate
    "PruefungNachweis":           fa(0xF00C),  # check
    "Tragwerksprinzip":           fa(0xF0D0),  # magic
    "Tragwerkstyp":               fa(0xF0D0),  # magic
    "Verbindungstechnik":         fa(0xF0C1),  # link
    "Leistungsanforderung":       fa(0xF080),  # bar-chart
    "Software":                   fa(0xF109),  # laptop
    "Tool":                       fa(0xF0AD),  # wrench
    "Tooltyp":                    fa(0xF02B),  # tag
    "SoftwareDigitaltool":        fa(0xF0A0),  # hdd-o
    "Wirtschaft":                 fa(0xF155),  # eur
    "Foerderprogramm":            fa(0xF19C),  # university
    "Programm":                   fa(0xF0F6),  # file-text-o
    "Quelle":                     fa(0xF02D),  # book
    "Methode":                    fa(0xF0C3),  # flask
    "Nutzung":                    fa(0xF015),  # home
    "Status":                     fa(0xF111),  # circle
    "GraphVersion":               fa(0xF02E),  # bookmark
    "Kontextmerkmal":             fa(0xF129),  # info
    "Kennwertdefinition":         fa(0xF201),  # line-chart
    "BewertungslogikAbgrenzung":  fa(0xF200),  # pie-chart
    "Datenqualitaet":             fa(0xF1C0),  # database
    "Dokumenttyp":                fa(0xF0F6),  # file-text-o
}

# Semantic color schema by domain
SEMANTIC_COLORS = {
    # BARRIERS (Red) - problems, constraints, risks
    "Huerde": ("#E74C3C", "#C0392B", 50, "name"),
    "HuerdeKategorie": ("#C0392B", "#A93226", 65, "name"),
    "Schadstoff": ("#E8655D", "#CB4335", 45, "name"),
    
    # ACTORS & GOVERNANCE (Blue) - people, management, legal
    "Akteur": ("#2E86C1", "#1B5A96", 55, "name"),
    "Akteurrolle": ("#5DADE2", "#3498DB", 45, "name"),
    "Akteurtyp": ("#85C1E9", "#6BA3D6", 45, "name"),
    "RechtlicheBedingung": ("#1B6FAA", "#0D47A1", 45, "name"),
    "Ressourcenquelle": ("#3498DB", "#2980B9", 45, "name"),
    "Programm": ("#2980B9", "#1F618D", 50, "name"),
    
    # CIRCULAR ECONOMY & REUSE (Green/Teal) - sustainability
    "Wiederverwendungskette": ("#27AE60", "#1D7E4E", 60, "id"),
    "WiederverwendungsArt": ("#1ABC9C", "#117A65", 45, "name"),
    "Aufbereitungsverfahren": ("#16A085", "#0D6B52", 45, "name"),
    "Rueckbauverfahren": ("#48C774", "#229954", 45, "name"),
    "Funktionswechsel": ("#58D68D", "#52BE80", 45, "name"),
    
    # MATERIALS & COMPONENTS (Orange/Brown) - physical tangible
    "Material": ("#D68910", "#B8641D", 50, "name"),
    "Materialgruppe": ("#E59866", "#D68054", 55, "name"),
    "Bauteilgruppe": ("#D2691E", "#A04000", 55, "name"),
    "Bauteiltyp": ("#F39C12", "#D68910", 45, "name"),
    "Bauteilebene": ("#E8B71B", "#D4AF37", 45, "name"),
    "Bauteilzustand": ("#D35400", "#BA4A00", 45, "name"),
    "Bauobjekt": ("#BF5A1D", "#8B4513", 45, "name"),
    "Bauwerk": ("#A04000", "#6B3410", 55, "name"),
    "Bauobjektklasse": ("#CD853F", "#B8860B", 45, "name"),
    "Bauobjektrolle": ("#DAA520", "#C79900", 45, "name"),
    "BauaufgabeIntervention": ("#CC8844", "#A0522D", 45, "name"),
    
    # BUILDING STRUCTURE (Teal/Cyan) - technical, structural
    "Bausystem": ("#17A2B8", "#0D7C8F", 45, "name"),
    "Bauweise": ("#00BCD4", "#0097A7", 45, "name"),
    "Tragwerksprinzip": ("#0097A7", "#00838F", 45, "name"),
    "Tragwerkstyp": ("#00ACC1", "#00838F", 45, "name"),
    "Verbindungstechnik": ("#26C6DA", "#00BCD4", 45, "name"),
    
    # PROCESS & TIMELINE (Yellow/Gold) - flow, energy, progression
    "Prozessphase": ("#F1C40F", "#D4AF37", 45, "name"),
    "Beschaffungsweg": ("#F39C12", "#D68910", 45, "name"),
    "Logistik": ("#E8B71B", "#D4AF37", 45, "name"),
    
    # KNOWLEDGE & METHODOLOGY (Purple) - intellect, learning, standards
    "Quelle": ("#8E44AD", "#6C3483", 45, "name"),
    "Methode": ("#9B59B6", "#76448A", 45, "name"),
    "Kennwertdefinition": ("#AF7AC5", "#8B4FB8", 45, "name"),
    "Norm": ("#D7BDE2", "#C39BD3", 45, "name"),
    "PruefungNachweis": ("#9D4EDD", "#7B2CBF", 45, "name"),
    "ZertifizierungBewertungssystem": ("#D81B60", "#AD1457", 45, "name"),
    
    # DIGITAL & DATA (Indigo/Slate) - information, technology
    "Software": ("#3F51B5", "#283593", 45, "name"),
    "Tool": ("#5C6BC0", "#3F51B5", 45, "name"),
    "Tooltyp": ("#7986CB", "#5C6BC0", 45, "name"),
    "SoftwareDigitaltool": ("#512DA8", "#311B92", 45, "name"),
    "Datenqualitaet": ("#455A64", "#37474F", 35, "name"),
    "Dokumenttyp": ("#37474F", "#263238", 35, "name"),
    
    # SPATIAL & LOCATION (Dark Blue) - anchoring, reference
    "Projekt": ("#E74C3C", "#C0392B", 68, "name"),
    "Stadt": ("#34495E", "#1B2F42", 55, "name"),
    "Land": ("#1B6FAA", "#0D3B66", 60, "name"),
    "Ort": ("#2C3E50", "#1A252F", 45, "name"),
    
    # META & GOVERNANCE (Grey) - structure, system, versioning
    "Status": ("#7F8C8D", "#566573", 35, "name"),
    "GraphVersion": ("#95A5A6", "#7F8C8D", 35, "version"),
    "Kontextmerkmal": ("#455A64", "#37474F", 45, "name"),
    "BewertungslogikAbgrenzung": ("#37474F", "#263238", 45, "name"),
    
    # ECONOMIC & GROWTH (Green-Gold) - value, programs
    "Wirtschaft": ("#E67E22", "#D35400", 45, "name"),
    "Foerderprogramm": ("#27AE60", "#1D7E4E", 45, "name"),
    
    # UTILITY & USE (Teal accent)
    "Nutzung": ("#00ACC1", "#00838F", 45, "name"),
    
    # ADDITIONAL
    "Leistungsanforderung": ("#DC7633", "#BA4A00", 45, "name"),
}

# Label → (color, border, diameter, caption_prop)
NODES = {
    # default
    "_default": ("#A5ABB6", "#9AA1AC", 45, "name"),
    # spatial
    "Projekt":                    ("#E74C3C", "#C0392B", 68, "name"),
    "Bauwerk":                    ("#A04000", "#6B3410", 55, "name"),
    "Stadt":                      ("#34495E", "#1B2F42", 55, "name"),
    "Land":                       ("#1B6FAA", "#0D3B66", 60, "name"),
    "Ort":                        ("#2C3E50", "#1A252F", 45, "name"),
    # actors
    "Akteur":                     ("#2E86C1", "#1B5A96", 55, "name"),
    "Akteurrolle":                ("#5DADE2", "#3498DB", 45, "name"),
    "Akteurtyp":                  ("#85C1E9", "#6BA3D6", 45, "name"),
    # building components
    "Bauteilgruppe":              ("#D2691E", "#A04000", 55, "name"),
    "Bauteiltyp":                 ("#F39C12", "#D68910", 45, "name"),
    "Bauteilebene":               ("#E8B71B", "#D4AF37", 45, "name"),
    "Bausystem":                  ("#17A2B8", "#0D7C8F", 45, "name"),
    "Bauweise":                   ("#00BCD4", "#0097A7", 45, "name"),
    "Bauteilzustand":             ("#D35400", "#BA4A00", 45, "name"),
    "Bauobjektklasse":            ("#CD853F", "#B8860B", 45, "name"),
    "Bauobjektrolle":             ("#DAA520", "#C79900", 45, "name"),
    "BauaufgabeIntervention":     ("#CC8844", "#A0522D", 45, "name"),
    # materials
    "Material":                   ("#D68910", "#B8641D", 50, "name"),
    "Materialgruppe":             ("#E59866", "#D68054", 55, "name"),
    # reuse / process
    "Wiederverwendungskette":     ("#27AE60", "#1D7E4E", 60, "id"),
    "WiederverwendungsArt":       ("#1ABC9C", "#117A65", 45, "name"),
    "Prozessphase":               ("#F1C40F", "#D4AF37", 45, "name"),
    "Aufbereitungsverfahren":     ("#16A085", "#0D6B52", 45, "name"),
    "Rueckbauverfahren":          ("#48C774", "#229954", 45, "name"),
    "Beschaffungsweg":            ("#F39C12", "#D68910", 45, "name"),
    "Logistik":                   ("#E8B71B", "#D4AF37", 45, "name"),
    "Ressourcenquelle":           ("#3498DB", "#2980B9", 45, "name"),
    "Funktionswechsel":           ("#58D68D", "#52BE80", 45, "name"),
    # barriers
    "Huerde":                     ("#E74C3C", "#C0392B", 50, "name"),
    "HuerdeKategorie":            ("#C0392B", "#A93226", 65, "name"),
    "Schadstoff":                 ("#E8655D", "#CB4335", 45, "name"),
    # legal
    "Norm":                       ("#D7BDE2", "#C39BD3", 45, "name"),
    "RechtlicheBedingung":        ("#1B6FAA", "#0D47A1", 45, "name"),
    "ZertifizierungBewertungssystem": ("#D81B60", "#AD1457", 45, "name"),
    "PruefungNachweis":           ("#9D4EDD", "#7B2CBF", 45, "name"),
    # structural
    "Tragwerksprinzip":           ("#0097A7", "#00838F", 45, "name"),
    "Tragwerkstyp":               ("#00ACC1", "#00838F", 45, "name"),
    "Verbindungstechnik":         ("#26C6DA", "#00BCD4", 45, "name"),
    "Leistungsanforderung":       ("#DC7633", "#BA4A00", 45, "name"),
    # digital
    "Software":                   ("#3F51B5", "#283593", 45, "name"),
    "Tool":                       ("#5C6BC0", "#3F51B5", 45, "name"),
    "Tooltyp":                    ("#7986CB", "#5C6BC0", 45, "name"),
    "SoftwareDigitaltool":        ("#512DA8", "#311B92", 45, "name"),
    # economic
    "Wirtschaft":                 ("#E67E22", "#D35400", 45, "name"),
    "Foerderprogramm":            ("#27AE60", "#1D7E4E", 45, "name"),
    "Programm":                   ("#2980B9", "#1F618D", 50, "name"),
    # knowledge
    "Quelle":                     ("#8E44AD", "#6C3483", 45, "name"),
    "Methode":                    ("#9B59B6", "#76448A", 45, "name"),
    "Nutzung":                    ("#00ACC1", "#00838F", 45, "name"),
    # meta
    "Status":                     ("#7F8C8D", "#566573", 35, "name"),
    "GraphVersion":               ("#95A5A6", "#7F8C8D", 35, "version"),
    "Kontextmerkmal":             ("#455A64", "#37474F", 45, "name"),
    "Kennwertdefinition":         ("#AF7AC5", "#8B4FB8", 45, "name"),
    "BewertungslogikAbgrenzung":  ("#37474F", "#263238", 45, "name"),
    "Datenqualitaet":             ("#455A64", "#37474F", 35, "name"),
    "Dokumenttyp":                ("#37474F", "#263238", 35, "name"),
}

# Relationships with semantic colors from their connected nodes (lighter shades)
REL_COLORS = {
    # ACTOR relationships (Very Light Blue - almost white)
    "BETEILIGT_AN":         "#D9EEF7",
    "HAT_AKTEURROLLE":      "#DFF5F9",
    "HAT_AKTEURTYP":        "#E6F7FB",
    
    # LOCATION relationships (Very Light Blue)
    "LIEGT_IN_STADT":       "#D9EEF7",
    "LIEGT_IN_LAND":        "#D9EEF7",
    
    # MATERIAL relationships (Very Light Orange/Cream)
    "NUTZT_MATERIAL":       "#F8E8D8",
    "HAT_MATERIALGRUPPE":   "#FBF0E5",
    
    # REUSE relationships (Very Light Green/Teal)
    "TEIL_VON_KETTE":       "#D8F0E5",
    "HAT_WIEDERVERWENDUNGSART": "#D9F3F0",
    "HAT_AUFBEREITUNG":     "#D9F3F0",
    "HAT_RUECKBAUVERFAHREN": "#E5F8F4",
    "HAT_FUNKTIONSWECHSEL": "#E5F8F4",
    
    # BUILDING STRUCTURE relationships (Very Light Teal)
    "HAT_BAUTEILTYP":       "#F8E8D8",
    "HAT_BAUTEILEBENE":     "#FBF0E5",
    "HAT_BAUSYSTEM":        "#D9F3F0",
    "HAT_BAUWEISE":         "#E5F8F9",
    "HAT_TRAGWERKSPRINZIP": "#D9F3F0",
    "HAT_TRAGWERKSTYP":     "#E5F8F9",
    "HAT_VERBINDUNGSTECHNIK": "#E5F8F9",
    "HAT_BAUTEILGRUPPE":    "#F8E8D8",
    
    # BARRIER relationships (Very Light Red/Rose)
    "HAT_HUERDE":           "#F9D5D7",
    "HAT_HUERDEKATEGORIE":  "#FCE0E1",
    "HAT_SCHADSTOFF":       "#FCDAD7",
    
    # PROCESS relationships (Very Light Yellow/Cream)
    "HAT_PROZESSPHASE":     "#FEFCF0",
    "HAT_BESCHAFFUNGSWEG":  "#F8E8D8",
    "HAT_LOGISTIK":         "#FBF0E5",
    
    # KNOWLEDGE relationships (Very Light Purple)
    "ZITIERT_QUELLE":       "#E8D9F5",
    "HAT_METHODE":          "#EFE5FB",
    "REFERENZIERT_NORM":    "#F5EDFE",
    "HAT_PRUEFUNG":         "#EFE5FB",
    "HAT_ZERTIFIZIERUNG":   "#F5EDFE",
    
    # QUALITY relationships (Very Light Orange)
    "HAT_LEISTUNGSANFORDERUNG": "#F8E8D8",
    
    # LEGAL relationships (Very Light Blue)
    "HAT_RECHTLICHE_BEDINGUNG": "#D9EEF7",
    "HAT_RESSOURCENQUELLE": "#D9EEF7",
    
    # ECONOMIC relationships (Very Light Green)
    "HAT_WIRTSCHAFTSASPEKT": "#FBF0E5",
    "TEIL_VON_PROGRAMM":    "#E5F8F4",
    
    # DIGITAL relationships (Very Light Indigo)
    "NUTZT_SOFTWARE":       "#DDE5F8",
    "NUTZT_TOOL":           "#E6EEF9",
    
    # UTILITY relationships (Very Light Teal)
    "HAT_NUTZUNG":          "#E5F8F9",
    
    # META relationships (Very Light Grey)
    "HAT_STATUS":           "#E5E9F0",
    "HAT_KONTEXTMERKMAL":   "#EFF0F5",
    
    # GENERAL structural (Very Light Brown/Tan)
    "HAT_INTERVENTION":     "#F0E5D8",
    "HAT_BAUOBJEKTKLASSE":  "#F8E8D8",
    "HAT_BAUOBJEKTROLLE":   "#FBF0E5",
    "NUTZT_BAUWERK":        "#F0E5D8",
    "AUS_BAUWERK":          "#F0E5D8",
    "EINGEBAUT_IN":         "#F0E5D8",
    "BELEGT_IN":            "#E8D9F5",
}


def text_color(hex_color: str) -> str:
    """Pick white or dark text based on background luminance."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#FFFFFF" if luminance < 0.55 else "#333333"


def build_grass() -> str:
    lines = []

    # default node
    d = NODES["_default"]
    lines.append(f"""node {{
  diameter: {d[2]}px;
  color: {d[0]};
  border-color: {d[1]};
  border-width: 2px;
  text-color-internal: #FFFFFF;
  font-size: 9px;
  caption: "{{{d[3]}}}";
}}
""")

    # per-label node styles
    for label, (color, border, diam, cap) in NODES.items():
        if label == "_default":
            continue
        icon = ICONS.get(label, "")
        tc = text_color(color)
        icon_line = f'  icon-code: "{icon}";\n' if icon else ""
        lines.append(
            f"node.{label} {{\n"
            f"  color: {color};\n"
            f"  border-color: {border};\n"
            f"  diameter: {diam}px;\n"
            f"  caption: \"{{{cap}}}\";\n"
            f"  text-color-internal: {tc};\n"
            f"{icon_line}"
            f"}}\n"
        )

    # default relationship
    lines.append("""relationship {
  color: #A5ABB6;
  shaft-width: 1px;
  font-size: 8px;
  text-color-external: #777777;
  caption: type;
}
""")

    # per-type relationship styles
    for rel, color in REL_COLORS.items():
        lines.append(f"relationship.{rel} {{ color: {color}; shaft-width: 2px; }}\n")

    return "".join(lines)


GRASS_CONTENT = build_grass()

# Save to file
import pathlib
out = pathlib.Path(__file__).parent.parent / "_neo4j" / "neo4j_style.grass"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(GRASS_CONTENT, encoding="utf-8")
print(f"Saved: {out}")

# Serve it
PORT = 8765

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/neo4j_style.grass":
            data = GRASS_CONTENT.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # silence logs

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"\nServing style at: http://localhost:{PORT}/neo4j_style.grass")
    print("\nIn Neo4j Browser, run:")
    print(f"  :style http://localhost:{PORT}/neo4j_style.grass")
    print("\nPress Ctrl+C to stop.\n")
    httpd.serve_forever()
