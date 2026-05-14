"""
Generate neo4j_style_2026-5-14_light.grass
Light/pastel version of the harmonious color schema.

Design principles:
  Fill:   S 45-55%, L 86-90%  — soft pastel, legible on white Neo4j canvas
  Border: S 55-65%, L 48-56%  — medium-saturated, same hue → definition without heaviness
  Text:   S 60-70%, L 18-26%  — dark shade of same hue → legible on light fill
  Rels:   already light tints, slightly boosted for white-canvas contrast
"""

import re, shutil

SRC  = 'E:/recherche/_neo4j/neo4j_style_2026-5-14.grass'
DEST = 'E:/recherche/_neo4j/neo4j_style_2026-5-14_light.grass'

# (fill, border, diameter, text-color-internal)
LIGHT_NODES = {
    # ── PROJEKT  hue ≈ 350° warm-red ────────────────────────────────────────
    "Projekt":                    ("#F4C0C8", "#C04E64", 68, "#7A1828"),

    # ── GEOGRAPHY  hue ≈ 210° slate-blue ────────────────────────────────────
    "Bauwerk":                    ("#BFCBD8", "#547090", 55, "#223050"),
    "Stadt":                      ("#C2CDD8", "#577492", 55, "#253050"),
    "Land":                       ("#C6D0DC", "#5C7896", 60, "#283450"),
    "Ort":                        ("#C2CDD8", "#577492", 45, "#253050"),
    "Nutzung":                    ("#C2CDD8", "#577492", 45, "#253050"),

    # ── ACTORS  hue ≈ 210° steel-blue ───────────────────────────────────────
    "Akteur":                     ("#B8CCEC", "#4E88C0", 55, "#1C3C68"),
    "Akteurrolle":                ("#C0D4EE", "#5E9CC8", 45, "#223C68"),
    "Akteurtyp":                  ("#CADAEE", "#70AACC", 45, "#2A4268"),
    "Ressourcenquelle":           ("#BCCEEA", "#5290BC", 45, "#1E3C62"),
    "Programm":                   ("#B6C8E8", "#4880B4", 50, "#183460"),

    # ── REUSE  hue ≈ 155° emerald ───────────────────────────────────────────
    "Wiederverwendungskette":     ("#B2DAC8", "#3C9070", 60, "#124C38"),
    "WiederverwendungsArt":       ("#B8DEC8", "#469A78", 45, "#145438"),
    "Aufbereitungsverfahren":     ("#BCE2CC", "#50A680", 45, "#165838"),
    "Rueckbauverfahren":          ("#C0E4D0", "#5AB090", 45, "#165C3A"),
    "Funktionswechsel":           ("#C4E6D2", "#64B894", 45, "#186040"),

    # ── MATERIALS  hue ≈ 25° terracotta ─────────────────────────────────────
    "Materialgruppe":             ("#EAD8C0", "#B27848", 55, "#673810"),
    "Bauteilgruppe":              ("#EBD8BC", "#B47A48", 55, "#693A10"),
    "Material":                   ("#EEDCC4", "#B87E4E", 50, "#6C3C12"),
    "Bauteiltyp":                 ("#F0DEC8", "#BC8254", 45, "#703E12"),
    "Bauteilebene":               ("#F2E0CC", "#C08858", 45, "#744014"),
    "Bausystem":                  ("#F0DCC8", "#BC8050", 45, "#6E3E12"),
    "Bauweise":                   ("#F0DEC8", "#BE8252", 45, "#703E12"),
    "Bauteilzustand":             ("#F0DCC8", "#BA7E50", 45, "#6C3C12"),
    "Bauobjektklasse":            ("#F2DEC8", "#BE8050", 45, "#703E12"),
    "Bauobjektrolle":             ("#F4E0CC", "#C28458", 45, "#764014"),
    "BauaufgabeIntervention":     ("#ECDAC0", "#B67848", 45, "#6A3A10"),
    "Leistungsanforderung":       ("#F0DCC4", "#BC7E4E", 45, "#6E3C12"),

    # ── PROCESS  hue ≈ 40° amber ────────────────────────────────────────────
    "Prozessphase":               ("#EEE4B0", "#AE9838", 45, "#5A4A08"),
    "Beschaffungsweg":            ("#F0E4B4", "#B49C3A", 45, "#5C4C08"),
    "Logistik":                   ("#F0E4B4", "#B89E3C", 45, "#5E4E08"),

    # ── BARRIERS  hue ≈ 355° red ────────────────────────────────────────────
    "HuerdeKategorie":            ("#F2BCBC", "#C04258", 65, "#7C1028"),
    "Huerde":                     ("#F4C0C0", "#C44E60", 50, "#7E1828"),
    "Schadstoff":                 ("#F4C4C4", "#C46060", 45, "#7C2020"),

    # ── KNOWLEDGE  hue ≈ 270° violet ────────────────────────────────────────
    "Quelle":                     ("#D4CCEC", "#7C62B8", 45, "#3C2868"),
    "Methode":                    ("#D6CEEC", "#8268B8", 45, "#402A70"),
    "Norm":                       ("#DAD0EC", "#8870BC", 45, "#443070"),
    "PruefungNachweis":           ("#DED4F0", "#9078C4", 45, "#46327A"),
    "Kennwertdefinition":         ("#E2D6F0", "#9880C8", 45, "#4A367A"),

    # ── LEGAL  hue ≈ 335° deep-rose ─────────────────────────────────────────
    "RechtlicheBedingung":        ("#F0C0D0", "#B04870", 45, "#6C1C38"),
    "ZertifizierungBewertungssystem": ("#F4C4D8", "#B65080", 45, "#6E1C3C"),

    # ── DIGITAL  hue ≈ 230° indigo ──────────────────────────────────────────
    "SoftwareDigitaltool":        ("#C4CCF0", "#5468C0", 45, "#24286A"),
    "Software":                   ("#C6CEF2", "#5C70C8", 45, "#28306A"),
    "Tool":                       ("#C8D0F2", "#6278C8", 45, "#2A3270"),
    "Tooltyp":                    ("#CCDAF4", "#6A80C8", 45, "#2C3470"),

    # ── STRUCTURAL  hue ≈ 185° teal ─────────────────────────────────────────
    "Tragwerksprinzip":           ("#B8DCDE", "#3AAAB2", 45, "#0C4C54"),
    "Tragwerkstyp":               ("#BCDEe2", "#3EB0B8", 45, "#0C5058"),
    "Verbindungstechnik":         ("#C0E0E4", "#42B4BC", 45, "#0E5258"),

    # ── ECONOMY  hue ≈ 100° sage ────────────────────────────────────────────
    "Wirtschaft":                 ("#C8DEB8", "#689848", 45, "#284018"),
    "Foerderprogramm":            ("#CAE0BA", "#6CA04A", 45, "#2A4218"),

    # ── META  hue ≈ 220° blue-grey ───────────────────────────────────────────
    "Status":                     ("#C8CDD8", "#60708A", 35, "#30384A"),
    "GraphVersion":               ("#CCCDD8", "#64748C", 35, "#343A4C"),
    "Kontextmerkmal":             ("#C8CDD8", "#607088", 45, "#303848"),
    "BewertungslogikAbgrenzung":  ("#C4CAD8", "#5E6E84", 45, "#2E3646"),
    "Datenqualitaet":             ("#C8CDD8", "#62708A", 35, "#303848"),
    "Dokumenttyp":                ("#C6CBD8", "#606E86", 35, "#303848"),
}

# Relationship colors — slightly more saturated than dark-theme tints for white canvas
LIGHT_REL_COLORS = {
    "BETEILIGT_AN":              "#7AAABB",
    "HAT_AKTEURROLLE":           "#88B4C8",
    "HAT_AKTEURTYP":             "#96BED0",
    "LIEGT_IN_STADT":            "#82A0B0",
    "LIEGT_IN_LAND":             "#82A0B0",
    "NUTZT_MATERIAL":            "#CCA880",
    "HAT_MATERIALGRUPPE":        "#C49C74",
    "TEIL_VON_KETTE":            "#70B098",
    "HAT_WIEDERVERWENDUNGSART":  "#74B8A4",
    "HAT_AUFBEREITUNG":          "#74B8A4",
    "HAT_RUECKBAUVERFAHREN":     "#82C0B0",
    "HAT_FUNKTIONSWECHSEL":      "#82C0B0",
    "HAT_BAUTEILTYP":            "#CCA880",
    "HAT_BAUTEILEBENE":          "#C49C74",
    "HAT_BAUSYSTEM":             "#CCA880",
    "HAT_BAUWEISE":              "#C49C74",
    "HAT_TRAGWERKSPRINZIP":      "#70B4BC",
    "HAT_TRAGWERKSTYP":          "#7ABCC4",
    "HAT_VERBINDUNGSTECHNIK":    "#84C4CC",
    "HAT_BAUTEILGRUPPE":         "#C49C74",
    "HAT_HUERDE":                "#C48898",
    "HAT_HUERDEKATEGORIE":       "#BC8890",
    "HAT_SCHADSTOFF":            "#C49898",
    "HAT_PROZESSPHASE":          "#C4B478",
    "HAT_BESCHAFFUNGSWEG":       "#BCAC74",
    "HAT_LOGISTIK":              "#C0B078",
    "ZITIERT_QUELLE":            "#A898C4",
    "HAT_METHODE":               "#AEA0CC",
    "REFERENZIERT_NORM":         "#B2A4CC",
    "HAT_PRUEFUNG":              "#B6A8CC",
    "HAT_ZERTIFIZIERUNG":        "#C48CA4",
    "HAT_LEISTUNGSANFORDERUNG":  "#CCA880",
    "HAT_RECHTLICHE_BEDINGUNG":  "#BC90A4",
    "HAT_RESSOURCENQUELLE":      "#7AAABB",
    "HAT_WIRTSCHAFTSASPEKT":     "#8CB488",
    "TEIL_VON_PROGRAMM":         "#7AAABB",
    "NUTZT_SOFTWARE":            "#8CA4CC",
    "NUTZT_TOOL":                "#94ACCG",
    "HAT_NUTZUNG":               "#82A0B0",
    "HAT_STATUS":                "#8C9CAE",
    "HAT_KONTEXTMERKMAL":        "#909CB4",
    "HAT_INTERVENTION":          "#CCA880",
    "HAT_BAUOBJEKTKLASSE":       "#CCA880",
    "HAT_BAUOBJEKTROLLE":        "#C49C74",
    "NUTZT_BAUWERK":             "#82A0B0",
    "AUS_BAUWERK":               "#82A0B0",
    "EINGEBAUT_IN":              "#82A0B0",
    "BELEGT_IN":                 "#A898C4",
}


def replace_in_block(text, block_selector, replacements):
    search = block_selector + ' {'
    start = text.find(search)
    if start == -1:
        return text, False
    end = text.find('\n}', start)
    if end == -1:
        return text, False
    end += 2
    block = text[start:end]
    new_block = block
    for prop, new_val in replacements.items():
        if prop == 'diameter':
            new_block = re.sub(
                rf'(\b{re.escape(prop)}: )\d+px;',
                rf'\g<1>{new_val}px;',
                new_block
            )
        else:
            new_block = re.sub(
                rf'(\b{re.escape(prop)}: )#[0-9A-Fa-f]+;',
                rf'\g<1>{new_val};',
                new_block
            )
    changed = new_block != block
    return text[:start] + new_block + text[end:], changed


shutil.copy2(SRC, DEST)
content = open(DEST, 'r', encoding='utf-8').read()

# Default node
content, _ = replace_in_block(content, 'node', {
    'color':                '#CBCDD6',
    'border-color':         '#888EA0',
    'text-color-internal':  '#2A2E3A',
})

# Default relationship
content, _ = replace_in_block(content, 'relationship', {
    'color': '#9DA4B2',
    'text-color-external': '#555555',
})

# Named nodes
for node_name, (fill, border, diameter, text_col) in LIGHT_NODES.items():
    content, ok = replace_in_block(content, f'node.{node_name}', {
        'color':               fill,
        'border-color':        border,
        'diameter':            str(diameter),
        'text-color-internal': text_col,
    })
    if not ok:
        print(f'WARNING: no match for node.{node_name}')

# Named relationships
for rel_name, color in LIGHT_REL_COLORS.items():
    pat = rf'(relationship\.{re.escape(rel_name)} \{{ color: )#[0-9A-Fa-f]+(;)'
    new_content = re.sub(pat, rf'\g<1>{color}\g<2>', content)
    if new_content == content:
        print(f'WARNING: no match for relationship.{rel_name}')
    else:
        content = new_content

open(DEST, 'w', encoding='utf-8').write(content)
print(f'Written: {DEST}')
