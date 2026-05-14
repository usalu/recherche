import re

NEW_COLORS = {
    "Projekt":                    ("#B83040", "#8E2030", 68, "#FFFFFF"),
    "Bauwerk":                    ("#385068", "#263C50", 55, "#FFFFFF"),
    "Stadt":                      ("#3F5872", "#2C4458", 55, "#FFFFFF"),
    "Land":                       ("#46607E", "#324C62", 60, "#FFFFFF"),
    "Ort":                        ("#3F5872", "#2C4458", 45, "#FFFFFF"),
    "Nutzung":                    ("#3F5872", "#2C4458", 45, "#FFFFFF"),
    "Akteur":                     ("#3470A4", "#245884", 55, "#FFFFFF"),
    "Akteurrolle":                ("#4A84B4", "#3470A4", 45, "#FFFFFF"),
    "Akteurtyp":                  ("#6098C4", "#4A84B4", 45, "#FFFFFF"),
    "Ressourcenquelle":           ("#3C78AC", "#2C5E8C", 45, "#FFFFFF"),
    "Programm":                   ("#2A629A", "#1C4A7C", 50, "#FFFFFF"),
    "Wiederverwendungskette":     ("#1A7A5A", "#125A40", 60, "#FFFFFF"),
    "WiederverwendungsArt":       ("#28906C", "#1A7A5A", 45, "#FFFFFF"),
    "Aufbereitungsverfahren":     ("#36A07A", "#288C6A", 45, "#FFFFFF"),
    "Rueckbauverfahren":          ("#44AC84", "#36A07A", 45, "#FFFFFF"),
    "Funktionswechsel":           ("#52B690", "#44AC84", 45, "#FFFFFF"),
    "Materialgruppe":             ("#A05428", "#7C3E1C", 55, "#FFFFFF"),
    "Bauteilgruppe":              ("#AC5C2E", "#884422", 55, "#FFFFFF"),
    "Material":                   ("#B46030", "#8E4820", 50, "#FFFFFF"),
    "Bauteiltyp":                 ("#C07038", "#A25828", 45, "#FFFFFF"),
    "Bauteilebene":               ("#C87C40", "#AC6430", 45, "#FFFFFF"),
    "Bausystem":                  ("#BC6E38", "#9E5628", 45, "#FFFFFF"),
    "Bauweise":                   ("#C47238", "#A65A28", 45, "#FFFFFF"),
    "Bauteilzustand":             ("#BC6C40", "#9E5430", 45, "#FFFFFF"),
    "Bauobjektklasse":            ("#C47840", "#A66030", 45, "#FFFFFF"),
    "Bauobjektrolle":             ("#CC8448", "#AE6C38", 45, "#FFFFFF"),
    "BauaufgabeIntervention":     ("#BA6C38", "#9C5428", 45, "#FFFFFF"),
    "Leistungsanforderung":       ("#BE7038", "#A05828", 45, "#FFFFFF"),
    "Prozessphase":               ("#9E7820", "#7C6018", 45, "#FFFFFF"),
    "Beschaffungsweg":            ("#A88828", "#846C20", 45, "#FFFFFF"),
    "Logistik":                   ("#B09030", "#8C7222", 45, "#FFFFFF"),
    "HuerdeKategorie":            ("#A42C3C", "#801E2A", 65, "#FFFFFF"),
    "Huerde":                     ("#C04048", "#9A2C36", 50, "#FFFFFF"),
    "Schadstoff":                 ("#C85858", "#A24040", 45, "#FFFFFF"),
    "Quelle":                     ("#644898", "#4A3478", 45, "#FFFFFF"),
    "Methode":                    ("#6C50A0", "#523C80", 45, "#FFFFFF"),
    "Norm":                       ("#785CA8", "#604888", 45, "#FFFFFF"),
    "PruefungNachweis":           ("#8464B0", "#6E50A0", 45, "#FFFFFF"),
    "Kennwertdefinition":         ("#9074B8", "#7860A8", 45, "#FFFFFF"),
    "RechtlicheBedingung":        ("#9A3054", "#781C3C", 45, "#FFFFFF"),
    "ZertifizierungBewertungssystem": ("#A83C60", "#882A48", 45, "#FFFFFF"),
    "SoftwareDigitaltool":        ("#36489A", "#283680", 45, "#FFFFFF"),
    "Software":                   ("#4460A8", "#324E90", 45, "#FFFFFF"),
    "Tool":                       ("#5070B0", "#4060A0", 45, "#FFFFFF"),
    "Tooltyp":                    ("#6080B8", "#5070AE", 45, "#FFFFFF"),
    "Tragwerksprinzip":           ("#168898", "#0C6878", 45, "#FFFFFF"),
    "Tragwerkstyp":               ("#1A98A8", "#107080", 45, "#FFFFFF"),
    "Verbindungstechnik":         ("#1EA4B0", "#167A86", 45, "#FFFFFF"),
    "Wirtschaft":                 ("#4A7230", "#365824", 45, "#FFFFFF"),
    "Foerderprogramm":            ("#527A34", "#3E5E28", 45, "#FFFFFF"),
    "Status":                     ("#4A5670", "#38425A", 35, "#FFFFFF"),
    "GraphVersion":               ("#546078", "#40505E", 35, "#FFFFFF"),
    "Kontextmerkmal":             ("#4E5A70", "#3C4A5A", 45, "#FFFFFF"),
    "BewertungslogikAbgrenzung":  ("#485468", "#364254", 45, "#FFFFFF"),
    "Datenqualitaet":             ("#4C5870", "#3A4458", 35, "#FFFFFF"),
    "Dokumenttyp":                ("#485266", "#364050", 35, "#FFFFFF"),
}

NEW_REL_COLORS = {
    "BETEILIGT_AN":              "#96BCCF",
    "HAT_AKTEURROLLE":           "#A4C6D8",
    "HAT_AKTEURTYP":             "#B2D0E0",
    "LIEGT_IN_STADT":            "#9EB0C0",
    "LIEGT_IN_LAND":             "#9EB0C0",
    "NUTZT_MATERIAL":            "#DDB898",
    "HAT_MATERIALGRUPPE":        "#D4AC8C",
    "TEIL_VON_KETTE":            "#8CBFA8",
    "HAT_WIEDERVERWENDUNGSART":  "#90C8B4",
    "HAT_AUFBEREITUNG":          "#90C8B4",
    "HAT_RUECKBAUVERFAHREN":     "#9CCFBC",
    "HAT_FUNKTIONSWECHSEL":      "#9CCFBC",
    "HAT_BAUTEILTYP":            "#DDB898",
    "HAT_BAUTEILEBENE":          "#D4AC8C",
    "HAT_BAUSYSTEM":             "#DDB898",
    "HAT_BAUWEISE":              "#D4AC8C",
    "HAT_TRAGWERKSPRINZIP":      "#8CC4CC",
    "HAT_TRAGWERKSTYP":          "#94CCD4",
    "HAT_VERBINDUNGSTECHNIK":    "#9CD4DC",
    "HAT_BAUTEILGRUPPE":         "#D4AC8C",
    "HAT_HUERDE":                "#D4A0A8",
    "HAT_HUERDEKATEGORIE":       "#CCA0A4",
    "HAT_SCHADSTOFF":            "#D4ACAC",
    "HAT_PROZESSPHASE":          "#D4C490",
    "HAT_BESCHAFFUNGSWEG":       "#CCBC8C",
    "HAT_LOGISTIK":              "#D0C090",
    "ZITIERT_QUELLE":            "#BAB0D4",
    "HAT_METHODE":               "#C0B8D8",
    "REFERENZIERT_NORM":         "#C4B8DC",
    "HAT_PRUEFUNG":              "#C8BCDC",
    "HAT_ZERTIFIZIERUNG":        "#D4A0B4",
    "HAT_LEISTUNGSANFORDERUNG":  "#DDB898",
    "HAT_RECHTLICHE_BEDINGUNG":  "#CCA8B8",
    "HAT_RESSOURCENQUELLE":      "#96BCCF",
    "HAT_WIRTSCHAFTSASPEKT":     "#A4C498",
    "TEIL_VON_PROGRAMM":         "#96BCCF",
    "NUTZT_SOFTWARE":            "#A4B4D8",
    "NUTZT_TOOL":                "#ACC0DC",
    "HAT_NUTZUNG":               "#9EB0C0",
    "HAT_STATUS":                "#A4ACC0",
    "HAT_KONTEXTMERKMAL":        "#A8B0C4",
    "HAT_INTERVENTION":          "#DDB898",
    "HAT_BAUOBJEKTKLASSE":       "#DDB898",
    "HAT_BAUOBJEKTROLLE":        "#D4AC8C",
    "NUTZT_BAUWERK":             "#9EB0C0",
    "AUS_BAUWERK":               "#9EB0C0",
    "EINGEBAUT_IN":              "#9EB0C0",
    "BELEGT_IN":                 "#BAB0D4",
}

path = 'E:/recherche/_neo4j/neo4j_style_2026-5-14.grass'
content = open(path, 'r', encoding='utf-8').read()


def replace_in_block(text, block_selector, replacements):
    """Find a block starting with `block_selector {` and ending with a standalone `}`,
    then apply property replacements (prop -> new_value) within that block only."""
    # Find block start
    search = block_selector + ' {'
    start = text.find(search)
    if start == -1:
        return text, False
    # Find end: the next '\n}' after block start
    end = text.find('\n}', start)
    if end == -1:
        return text, False
    end += 2  # include the '\n}'
    block = text[start:end]
    new_block = block
    for prop, new_val in replacements.items():
        # Replace e.g. "  color: #AABBCC;" line within block
        new_block = re.sub(
            rf'(\b{re.escape(prop)}: )#[0-9A-Fa-f]+;',
            rf'\g<1>{new_val};',
            new_block
        )
        if prop == 'diameter':
            new_block = re.sub(
                rf'(\b{re.escape(prop)}: )\d+px;',
                rf'\g<1>{new_val}px;',
                new_block
            )
    if new_block == block:
        return text, False
    return text[:start] + new_block + text[end:], True


# Update default node block
content, _ = replace_in_block(content, 'node', {
    'color': '#6E7890',
    'border-color': '#565E78',
})

for node_name, (color, border, diameter, text_color) in NEW_COLORS.items():
    content, ok = replace_in_block(content, f'node.{node_name}', {
        'color': color,
        'border-color': border,
        'diameter': str(diameter),
        'text-color-internal': text_color,
    })
    if not ok:
        print(f'WARNING: no match for node.{node_name}')

for rel_name, color in NEW_REL_COLORS.items():
    pattern = rf'(relationship\.{re.escape(rel_name)} \{{ color: )#[0-9A-Fa-f]+(;)'
    new_content = re.sub(pattern, rf'\g<1>{color}\g<2>', content)
    if new_content == content:
        print(f'WARNING: no match for relationship.{rel_name}')
    else:
        content = new_content

open(path, 'w', encoding='utf-8').write(content)
print('Done - file updated.')
