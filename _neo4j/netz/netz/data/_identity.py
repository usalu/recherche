"""Canonical identity-resolution tables needed to INTERPRET data (overlay JSON
stores country codes like "BE" and role slugs that must resolve to the same
strings the raw Neo4j export uses). This is NOT display vocabulary -- German
short labels for tables/legends live in render/latex/vocab.py. Duplicated
verbatim from net_lib.py for now (data/ must not import the legacy module,
which also carries esc()/TYPE_ABBR); becomes the single source once net_lib.py
is retired in Stage 6.
"""

# the single-letter Typ code: part of the public ID printed on graph circles
# AND used as the table row key -- this is identity, not presentation (a
# different renderer would still need the SAME code to cross-reference the
# same actor). No collisions: U/M/F/N/I/S/O/G/X/P/E all distinct.
TYPE_LETTER = {"Unternehmen": "U", "Materialhub_Bauteilboerse": "M", "Forschung_Lehre": "F",
               "NGO_Verband_Netzwerk": "N", "Oeffentliche_Institution": "I",
               "Software_Tool_Anbieter": "S", "Organisation": "O",
               "Foerdergeber_Programmtraeger": "G", "Unbekannt": "X", "Person": "E"}

ISO = {"Schweiz": "CH", "Deutschland": "DE", "Belgien": "BE", "Niederlande": "NL",
       "Frankreich": "FR", "Vereinigtes Königreich": "GB", "Österreich": "AT",
       "Dänemark": "DK", "Liechtenstein": "LI", "Finnland": "FI", "Norwegen": "NO",
       "USA": "US", "Japan": "JP", "Schweden": "SE", "Irland": "IE", "Luxemburg": "LU",
       "Estland": "EE", "Lettland": "LV", "Litauen": "LT", "Portugal": "PT", "Spanien": "ES",
       "Polen": "PL", "Tschechien": "CZ", "Slowenien": "SI", "Slowakei": "SK",
       "Ungarn": "HU", "Kroatien": "HR", "Italien": "IT", "Rumänien": "RO", "Griechenland": "GR"}
ISO_INV = {v: k for k, v in ISO.items()}

ROLE_DE = {
    "Reuse_Zirkularitaetsberatung": "Reuse-/Zirkularitätsberatung",
    "Entwurf_Planung": "Entwurf/Planung", "Materiallieferung_Markt": "Materiallieferung/Markt",
    "Forschung_Dokumentation": "Forschung/Dokumentation", "Fachplanung_Nachweis": "Fachplanung/Nachweis",
    "Bauherr_Auftraggeber": "Bauherr/Auftraggeber", "Projektmanagement_Koordination": "Projektmgmt./Koordination",
    "Rueckbau_Bauteilernte_Logistik": "Rückbau/Bauteilernte/Logistik", "Bauausfuehrung_Fertigung": "Bauausführung/Fertigung",
    "Software_Digitalisierung": "Software/Digitalisierung",
    "Materialbroker / Reuse-Marketplace-Betreiber": "Materialbroker/Marketplace",
    "Aufbereitung_Refurbishment": "Aufbereitung/Refurbishment", "Bildung_Wissenstransfer": "Bildung/Wissenstransfer",
    "Betrieb_Nutzung": "Betrieb/Nutzung", "Oeffentliche_Hand_Foerderung": "Öffentliche Hand/Förderung",
    "Unbestimmt": "Unbestimmt", "Tragwerksplanung": "Tragwerksplanung", "Nachhaltigkeitsberatung": "Nachhaltigkeitsberatung",
    "Landschaftsplanung": "Landschaftsplanung", "TGA_Gebaeudetechnik": "TGA/Gebäudetechnik",
    "Fassade": "Fassade", "Kunst_Gestaltung": "Kunst/Gestaltung"}
ROLE_INV = {v: k for k, v in ROLE_DE.items()}
