#!/usr/bin/env python3
"""
align_taxonomy.py — Richtet taxonomy.json an existierenden User-Wurzelordnern aus.

Liest die User-Knoten aus bauteil/, material/, methode/ etc. und ersetzt meine
synthetischen Knoten-IDs durch die tatsächlichen User-Datei-Namen. Keywords:

1. SYNONYM-Map (kuratiert): User-Knoten → ein oder mehrere alte Knoten →
   übernimmt deren Keywords.
2. Falls kein Synonym: Auto-generiert aus dem Knoten-Namen (Tokens, Varianten).

Erzeugt eine neue taxonomy.json (Backup als taxonomy.json.bak).
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OLD_TAX = ROOT / "taxonomy.json"
BACKUP = ROOT / "taxonomy.json.bak"

# User-Wurzelordner pro Entitätstyp.
# Norm und Recht im User getrennt — wir behalten "Norm_Recht" als Match-Typ
# (extract_entities canonicalisiert beides darauf), aber lesen aus beiden Ordnern.
USER_FOLDERS = {
    "Bauteil": ["bauteil"],
    "Material": ["material"],
    "Methode": ["methode"],
    "Prozessphase": ["prozessphase"],
    "Aufbereitungsmethode": ["aufbereitungsmethode"],
    "Wirtschaft": ["wirtschaft"],
    "Leistungsanforderung": ["leistungsanforderung"],
    "Tragwerkssystem": ["tragwerkssystem"],
    "Verbindung": ["verbindung"],
    "Norm_Recht": ["norm", "recht"],
    "Pruefung": ["pruefung"],
    "Huerde": ["huerde"],
    "Abbruchmethode": ["abbruchmethode"],
    "Logistik": ["logistik"],
    "Kennwert": ["kennwert"],
    "Datenmodell": ["datenmodell"],
    "Schadstoff": ["schadstoff"],
    "Reuse_Strategie": ["reuse_strategie"],
}

# User-Knoten → Liste alter Knoten (aus meiner alten taxonomy), deren Keywords
# zusammengeführt werden. None = user-only, Keywords aus Name generieren.
# Mehrfach-Mapping = generischer User-Knoten umfasst mehrere meiner spezifischen.
SYNONYMS: dict[str, dict[str, list[str] | None]] = {
    "Bauteil": {
        "Betonfertigteil": ["Betonfertigteil_Decke"],
        "Brettschichtholzstuetze": ["Holz_Tragelement"],
        "Brettsperrholzdecke": None,
        "Dachtragwerk": ["Holz_Dachtragwerk"],
        "Deckenplatte": ["Betonfertigteil_Decke", "Hohlkoerperdecke"],
        "Fachwerktraeger": ["Stahlfachwerk"],
        "Fassade": ["Fassadenpaneel", "Fassadenblech", "Holzfassade", "Glasfassade"],
        "Fenster": ["Fenster", "Fensterrahmen"],
        "Feuerschutztuer": ["Tuer"],
        "Holzrahmenelement": None,
        "Leuchte": ["Leuchte"],
        "Pfette": ["Holz_Tragelement"],
        "Sanitaerobjekt": ["Sanitaerobjekt"],
        "Stuetze": ["Stahlstuetze", "Stahlbetonstuetze", "Holz_Tragelement"],
        "Traeger": ["Stahltraeger", "Stahlbetontraeger", "Holz_Tragelement"],
        "Treppe": ["Treppe"],
        "Treppenwange": None,
        "Wand": ["Plattenbau_Aussenwand", "Plattenbau_Innenwand", "Innenwand", "Aussenwand_Mauerwerk"],
    },
    "Material": {
        "Beton": ["Beton_Ortbeton", "Stahlbeton", "Stahlbetonfertigteil"],
        "Brettschichtholz": ["Brettschichtholz"],
        "Brettsperrholz": ["Brettsperrholz_CLT"],
        "Composite_Verbindungen": None,
        "Glas": ["Glas_Material"],
        "Holz": ["Vollholz", "Sekundaerholz"],
        "Holz_Verbindungen": None,
        "Keramik": ["Keramik"],
        "Lehm": ["Lehm"],
        "Recyclingbeton": ["Recyclingbeton"],
        "Sanitarkeramik": ["Sanitaerkeramik_Material"],
        "Sekundaerstahl": ["Baustahl"],
        "Stahl": ["Baustahl", "Edelstahl"],
        "Stahl_Verbindungen": None,
        "Stroh": ["Daemmstoff_Bio"],
    },
    "Methode": {
        "Bauteilkatalogisierung": ["Material_Mapping", "Kataloge_Datenbank"],
        "Bestandserhalt": None,
        "Building_Material_Scouting": ["Component_Hunting", "Urban_Mining"],
        "Design_for_Disassembly": ["Design_for_Disassembly"],
        "Form_Follows_Availability": ["Reversed_Planning"],
        "Materialinventur": ["Material_Mapping"],
        "Materialpass": ["Stockmatcher"],
        "ReUse_Assessment": ["Pre_Demolition_Audit", "LCA_Oekobilanz"],
        "Reversibilitaet": ["Design_for_Disassembly"],
        "Urban_Mining": ["Urban_Mining"],
        "Zirkulaere_Ausschreibung": ["Specification_Method"],
    },
    "Prozessphase": {
        "Aufbereitung": ["Aufbereitung_Phase"],
        "Ausschreibung": None,
        "Bestandserfassung": ["Bestandsaufnahme", "Bauteilinventar_Phase"],
        "Betrieb_und_Rueckbauplanung": ["Nutzungsphase"],
        "Entwurf": ["Planung_Design_Phase"],
        "Lagerung": ["Lagerung_Phase"],
        "Rueckbau": ["Rueckbau_Phase"],
        "Transport": ["Transport_Phase"],
        "Wiedereinbau": ["Wiedereinbau_Phase"],
    },
    "Aufbereitungsmethode": {
        "Drahtglasschneiden": ["Drahtglasschneiden"],
        "Entmoertelung_von_Fliesen": ["Entmoertelung_Klinker"],
        "Holzaufbereitung": ["Refurbishment_Holz"],
        "Leuchten_Refurbishment": ["Refurbishment_Sanitaer"],
        "Qualitaetssicherung": ["Pruefung_Freigabe"],
        "Rekonditionierung": ["Refurbishment_Holz", "Anpassung_Bearbeitung"],
        "Reparatur": ["Lochverschluss_Reparatur"],
    },
    "Wirtschaft": {
        # User-only — alle aus Namen generiert, plus zusätzliche Keywords
        "Finanzierung": None,
        "Geschaeftsmodell": None,
        "Kostenvergleich": ["Kostenparitaet_Neubau"],
        "Lebenszykluskosten": None,
        "Preisbildung": None,
        "Restwert": None,
    },
    "Leistungsanforderung": {
        "Brandschutz": ["Brandschutz"],
        "Dauerhaftigkeit": ["Dauerhaftigkeit"],
        "Feuchteschutz": None,
        "Rueckbaubarkeit": None,
        "Schadstofffreiheit": None,
        "Schallschutz": ["Schallschutz"],
        "Tragfaehigkeit": ["Tragfaehigkeit"],
        "Waermeschutz": ["Waermeschutz_U_Wert"],
    },
    "Tragwerkssystem": {
        "Aufstockung_in_Holzbauweise": ["Holz_Skelettbau_BSH"],
        "Betonfertigteil_System": ["Stahlbeton_Fertigteil_System"],
        "Dachtragwerk_und_Fachwerk": None,
        "Design_for_Disassembly": None,
        "Holz_Skelettbau": ["Holz_Skelettbau_BSH", "Holz_Rahmenbau"],
        "Reversible_Fuegung": None,
        "Skelettbauweise": ["Stahl_Skelettbau", "Stahlbeton_Skelettbau"],
        "Stahl_Skelettbau": ["Stahl_Skelettbau"],
        "Tragende_Wand": ["Mauerwerksbau"],
    },
    "Verbindung": {
        "Klemmverbindung": ["Geklemmte_Verbindung"],
        "Stahlseil": None,
        "Steckverbindung": ["Gesteckte_Verbindung"],
        "Verleimung": ["Klebeverbindung"],
        "Vermoertelung": ["Moertelfuge"],
        "Verschraubung": ["Schraubverbindung"],
        "Verschweissung": ["Stahlbau_Schweissverbindung"],
    },
    "Norm_Recht": {
        # norm/
        "Brandschutzanforderung": None,
        "DIN_18940": ["DIN_18940_Lehm"],
        "DIN_EN_15804": None,
        "DIN_EN_15978": None,
        "EN_15804": None,
        "EU_Taxonomie": None,
        "F90": None,
        "Feuerwiderstand": None,
        "ISO_14040": None,
        "ISO_14044": None,
        "ISO_20887": None,
        "R90": None,
        "REI90": None,
        "Wiederverwendungskriterien": None,
        # recht/
        "Bauordnungsrecht": ["Bauordnung_nicht_angepasst"],
        "Gewaehrleistung": ["Haftung_Gewaehrleistung"],
        "Produkthaftung": ["Haftung_Gewaehrleistung"],
        "Vergaberecht": None,
        "Zulassung_im_Einzelfall": ["Werkszeugnis_Konformitaetserklaerung"],
    },
    "Pruefung": {
        "Abbrandbemessung": ["Brandschutzpruefung"],
        "Brandnachweis": ["Brandschutzpruefung"],
        "Eignungspruefung_Baulehm": None,
        "Geometrische_Vermessung": ["Massaufnahme"],
        "Materialpruefung": ["Materialpruefung_Beton", "Materialpruefung_Stahl", "Materialpruefung_Holz"],
        "Schadstoffscreening": ["Schadstoffpruefung"],
        "Schweissbarkeitspruefung": None,
        "Sichtpruefung": ["Sichtpruefung"],
        "Statische_Nachweisfuehrung": ["Tragwerksnachweis"],
        "Zugversuch": ["Festigkeitspruefung"],
        "Zustandsbewertung": ["Zustandsbewertung"],
    },
    "Huerde": {
        "Ausschreibungsproblem": ["Beschaffungsmodell_fehlt"],
        "Brandschutzkonflikt": ["Bauphysik_Hinderung"],
        "Datenluecke": ["Datenluecke"],
        "Fehlende_Datenstandards": None,
        "Fehlende_Lagerflaeche": ["Lagerung_Hinderung"],
        "Fehlende_Standardisierung": None,
        "Gewaehrleistung": ["Haftung_Gewaehrleistung"],
        "Haftung": ["Haftung_Gewaehrleistung"],
        "Logistikproblem": ["Transport_Hinderung", "Lagerung_Hinderung"],
        "Schadstoffbelastung": None,
        "Terminunsicherheit": ["Donor_Empfaenger_Timing"],
        "Toleranzen": ["Toleranz_Massabgleich"],
        "Verfuegbarkeitsproblem": ["Verfuegbarkeit_Profile"],
    },
    "Abbruchmethode": {
        "Ausbau_von_Bauteilen": ["Stueckweise_Demontage"],
        "Betonfräsen": ["Saegen_Beton"],
        "Demontage": ["Demontage_Lift_off"],
        "Selektiver_Rueckbau": ["Selektiver_Rueckbau"],
        "Zerstoerungsarme_Bergung": ["Selektiver_Rueckbau"],
    },
    "Logistik": {
        "Lagerflaeche": ["Stockholder_Reuse_Lieferant"],
        "Lagerung": ["Zwischenlagerung"],
        "Materialmatching": None,
        "Materialverfuegbarkeit": ["Regionale_Beschaffung"],
        "ReUse_Centre": None,
        "Transport": ["Schwertransport", "Long_Distance_Reuse"],
        "Zwischenlagerung": ["Zwischenlagerung"],
    },
    "Kennwert": {
        "CO2_Einsparung": ["CO2_Reduktion_absolut", "CO2_Reduktion_prozent"],
        "Demontagegrad": None,
        "Graue_Energie": ["Embodied_Carbon"],
        "Materialwert": None,
        "Wiederverwendungsquote": ["Wiederverwendungsrate_Gewicht", "Wiederverwendungsrate_Volumen"],
    },
    "Datenmodell": {
        "Bauteil_ID": None,
        "IFC": ["IFC_BIM"],
        "Klassifikation": ["Klassifikation_System"],
        "Materialpass_Schema": ["Madaster_Materialpass", "Materialenpaspoort_NL"],
        "Ontologie": ["Ontologie_RDF"],
        "Taxonomie": None,
    },
    "Schadstoff": {
        "Asbest": ["Asbest"],
        "Bleifarbe": ["Blei"],
        "Holzschutzmittel": ["Holzschutzmittel"],
        "PAK": ["PAK_Klebstoff"],
        "PCB": ["PCB"],
    },
    "Reuse_Strategie": {
        "Adaptives_ReUse": ["Adaptive_Reuse_Bestand"],
        "Design_for_Disassembly": None,
        "Direkte_Wiederverwendung": ["Tragend_Bauteil_Wiederverwendung", "Huelle_Bauteil_Wiederverwendung",
                                      "Innenausbau_Wiederverwendung", "TGA_Wiederverwendung"],
        "Refurbishment": ["Remanufacturing"],
        "Umnutzung": ["Adaptive_Reuse_Bestand"],
        "Weiterbauen_im_Bestand": ["Tragwerk_Wiederverwendung_Gesamt", "Adaptive_Reuse_Bestand"],
    },
}

# Stopwords für Auto-Keyword-Generation aus Knotennamen
NAME_STOPS = {
    "der", "die", "das", "und", "oder", "von", "mit", "fuer", "im", "am",
    "in", "an", "auf", "zu", "als", "the", "and", "or", "of", "to",
}


def auto_keywords_from_name(name: str) -> list[str]:
    """Generiert Standard-Keywords aus dem Knoten-Namen."""
    kws: set[str] = set()
    # Voller Name lowercased
    full = name.lower().replace("_", " ")
    kws.add(full)
    # Variante mit ae/oe/ue → ä/ö/ü (für Deutsch-Mapping)
    full_umlaut = full.replace("ae", "ä").replace("oe", "ö").replace("ue", "ü").replace("ss", "ß")
    if full_umlaut != full:
        kws.add(full_umlaut)
    # Tokens (mind. 4 Zeichen, keine Stopwords)
    tokens = [t.lower() for t in re.split(r"[_\s]+", name)
              if len(t) >= 4 and t.lower() not in NAME_STOPS]
    for t in tokens:
        kws.add(t)
        # Umlaut-Variante
        t_umlaut = t.replace("ae", "ä").replace("oe", "ö").replace("ue", "ü").replace("ss", "ß")
        if t_umlaut != t:
            kws.add(t_umlaut)
    return sorted(kws)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    # Backup
    if OLD_TAX.exists() and not BACKUP.exists():
        shutil.copy(OLD_TAX, BACKUP)
        print(f"Backup: {BACKUP.name}")

    old_tax = json.loads(OLD_TAX.read_text(encoding="utf-8"))

    new_tax: dict = {
        "_meta": {
            "schema_version": "0.3",
            "stand": "2026-05-08",
            "purpose": "User-aligned: Knoten-IDs entsprechen den Datei-Namen in den Wurzelordnern bauteil/, material/, methode/, etc. Keywords aus Synonym-Mapping zur alten Taxonomie + Auto-Generation aus Namen.",
        }
    }

    summary = []
    for et, folders in USER_FOLDERS.items():
        new_tax[et] = {}
        # Datenluecke wie zuvor: catch-all für 'unbekannt'
        new_tax[et]["Datenluecke"] = {
            "kategorie": "Datenluecke",
            "definition": "Datenlücke — Wert nicht angegeben oder unbekannt.",
            "keywords": ["unbekannt", "unklar", "nicht angegeben", "n/a", "fehlt",
                         "unspezifiziert", "tbd", "to be determined"],
        }

        # Sammle alle .md-Dateien aus allen User-Ordnern dieses Typs
        user_nodes: set[str] = set()
        for folder_name in folders:
            folder = ROOT / folder_name
            if not folder.exists():
                continue
            for md in folder.glob("*.md"):
                if md.stem == "index":
                    continue
                user_nodes.add(md.stem)

        synonym_map = SYNONYMS.get(et, {})
        for user_id in sorted(user_nodes):
            old_ids = synonym_map.get(user_id)
            keywords: set[str] = set()
            kategorie = ""
            definition = ""

            # 1. Synonym-Lookup
            if old_ids:
                for oid in old_ids:
                    old_node = old_tax.get(et, {}).get(oid, {})
                    keywords.update(old_node.get("keywords", []))
                    if not kategorie:
                        kategorie = old_node.get("kategorie", "")
                    if not definition:
                        definition = old_node.get("definition", "")

            # 2. Auto-Keywords aus Namen
            for kw in auto_keywords_from_name(user_id):
                keywords.add(kw)

            new_tax[et][user_id] = {
                "kategorie": kategorie,
                "definition": definition,
                "keywords": sorted(keywords),
                "synonym_to_old": old_ids if old_ids else [],
            }

        # Stats
        n_total = len(user_nodes)
        n_synonym = sum(1 for u in user_nodes if synonym_map.get(u))
        n_auto = n_total - n_synonym
        summary.append((et, n_total, n_synonym, n_auto))

    # Schreibe
    OLD_TAX.write_text(
        json.dumps(new_tax, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n{'Typ':<22} {'Knoten':>7} {'Synonym':>8} {'Auto':>5}")
    print("-" * 46)
    total = 0
    for et, n_total, n_syn, n_auto in summary:
        total += n_total
        print(f"{et:<22} {n_total:>7} {n_syn:>8} {n_auto:>5}")
    print("-" * 46)
    print(f"{'TOTAL':<22} {total:>7}")
    print()
    print(f"Neue taxonomy.json mit User-Knoten geschrieben.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
