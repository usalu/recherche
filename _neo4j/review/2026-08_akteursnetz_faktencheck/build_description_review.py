# -*- coding: utf-8 -*-
"""Build the review-only proposal set for all 570 relationship descriptions.

This script never edits the canonical relationship classification or LaTeX
outputs.  It produces a complete, hash-locked proposal package that must be
approved before a separate apply step may use it.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parent
CLASSIFICATION = BASE / "kanten_klassifikation.json"
INVENTORY = BASE / "kanten_review_inventory.json"
DECISIONS = BASE / "kanten_decisions.json"
OUT = BASE / "relationship_description_review"
BATCHES = OUT / "batches"

MAX_DESCRIPTION = 60
REVIEW_RUN = "2026-08-15_relationship_description_normalization"

BANNED = (
    "die quelle belegt",
    "der akteur",
    "beide sind als",
    "die kante",
    "die zusammenarbeit ist",
)

ACTOR_PROJECT_TYPES = {
    "Bauherrschaft", "Entwurf", "Fachplanung", "Reuse-Konzept",
    "Bauteilinventarisierung", "Rückbau", "Bauteillieferung",
    "Aufarbeitung", "Logistik", "Bauausführung", "Prüfung und Nachweis",
    "Forschungsbegleitung", "Förderung", "Betrieb",
    "Projektbeteiligung, Aufgabe unklar",
}

ACTOR_ACTOR_TYPES = {
    "Konsortialpartner", "Kooperationsvereinbarung",
    "Gemeinsames Bauvorhaben", "Gründung", "Übernahme", "Konzernbindung",
    "Betreiberschaft", "Mitgliedschaft", "Trägerschaft", "Lieferbeziehung",
    "Dienstleistungsbeziehung", "Personelle Verflechtung",
    "Zusammenarbeit, Art unklar", "Verzeichniseintrag",
    "Kein Beleg für eine Beziehung", "Beziehung nicht prüfbar",
}

ALIASES = {
    "Regionalt ombruksnettverk for byggematerialer": "Reuse-Netz Oslo–Trondheim",
    "The Engineers Reuse Collective": "TERC",
    "Facilitating the Circulation of Reclaimed Building Elements": "FCRBE",
    "ReCreate project consortium": "ReCreate",
    "Buildings as Material Banks": "BAMB",
    "Plateforme de réemploi des matériaux de voirie": "Pariser Straßenbau-Depot",
    "Bauteilkatalog Immobilien Basel-Stadt": "Basler Bauteilkatalog",
    "München Bauteilbörse": "Bauteilbörse München",
    "Stiftung Chance BauTeile Zürich": "BauTeile Zürich",
    "Ressourcerie Lausanne": "Ressourcerie Lausanne",
    "IBO – Österr. Institut": "IBO",
    "INEB – FHNW": "INEB/FHNW",
    "Tampereen kaupunki": "Stadt Tampere",
    "City of Tampere": "Stadt Tampere",
    "City of Helsinki": "Stadt Helsinki",
    "City of Espoo": "Stadt Espoo",
    "Hastings Pier Visitor": "Hastings Pier Visitor Centre",
    "PLP London HQ circular": "PLP London HQ",
    "BlueCity Offices": "BlueCity Offices",
    "People’s Pavilion": "People’s Pavilion",
    "Brent Cross Town": "Brent Cross Town",
    "Kindergarten Mööslistras": "Kindergarten Mööslistrasse",
    "Musée de Folklore Vie": "Musée du Folklore de Mouscron",
    "ELYS Kultur- und": "ELYS Kultur- und Gewerbezentrum",
    "Juch-Areal Recyclingzent": "Recyclingzentrum Juch-Areal",
    "AWM Münster – zirkulärer": "zirkulärer AWM-Büroumbau",
    "Upcycle Studios Copenhag": "Upcycle Studios Copenhagen",
    "Lokomotion Technology": "Lokomotion-Reuse-Pilot",
    "Melkinlaituri Primary": "Melkinlaituri-Schule",
    "Circular Centre Netherla": "Circular Centre Heerde",
    "Kv Återbruket": "Kv Återbruket",
    "Grande Halle de Colombel": "Grande Halle de Colombelles",
    "Woongroep Boschgaard": "Boschgaard",
}

CONTEXT_PATTERNS = (
    (r"meduni|mariannengasse", "MedUni-Campus"),
    (r"buildreuse|build.re.use", "BuildReUse"),
    (r"baukarussell", "BauKarussell"),
    (r"bamb|material banks", "BAMB"),
    (r"återhus|aterhus", "Återhus"),
    (r"recreate", "ReCreate"),
    (r"fcrbe", "FCRBE"),
    (r"spirou", "SPIROU"),
    (r"waste2build", "LIFE-Waste2Build"),
    (r"säilö|sailo", "SÄILÖ"),
    (r"kielo", "KIELO"),
    (r"bygcirk", "BygCirkulært"),
    (r"green.ai|ai pilot|matching algorithms", "Green-AI-Hub"),
    (r"urban mining hub", "Urban Mining Hub Berlin"),
    (r"re.?win", "RE-WIN"),
    (r"walkeweg|schliengerweg", "Basler Wettbewerben"),
    (r"hobelwerk", "Hobelwerk Haus D"),
    (r"schärenmoos|scharenmoos", "Schärenmoosstrasse"),
    (r"circl", "Circl-Pavillon"),
    (r"reframe", "ReFrame"),
    (r"318 oxford|house of fraser", "318 Oxford Street"),
    (r"brighton waste house|waste house", "Brighton Waste House"),
    (r"krets", "KRETS"),
    (r"handslag", "Handslag"),
    (r"reboost", "Reboost"),
    (r"regionalt ombruksnettverk|oslo.*trondheim", "Reuse-Netz Oslo–Trondheim"),
    (r"ccri", "CCRI"),
    (r"vendom", "Vendom"),
    (r"circular retrofit", "Circular Retrofit Lab"),
    (r"bauteilkatalog", "Basler Bauteilkatalog"),
    (r"montessori maassluis", "Montessori Maassluis"),
    (r"reuse stahl|stahlbeton|leitfaden", "Reuse-Leitfaden Stahl/Beton"),
    (r"institut.*économie circulaire|inec", "LIFE-Waste2Build"),
)

TYPE_CONFLICTS = {
    # The quotations describe membership, not a generic consortium relation.
    "AT:K010": ("Mitgliedschaft", "B→A", "Nimmt an der BauKarussell-Genossenschaft teil."),
    "AT:K012": ("Mitgliedschaft", "B→A", "Nimmt an der BauKarussell-Genossenschaft teil."),
    "AT:K013": ("Mitgliedschaft", "B→A", "Nimmt an der BauKarussell-Genossenschaft teil."),
    "AT:K014": ("Mitgliedschaft", "B→A", "Nimmt an der BauKarussell-Genossenschaft teil."),
    "AT:K015": ("Mitgliedschaft", "B→A", "Nimmt an der BauKarussell-Genossenschaft teil."),
    "DE:K048": ("Mitgliedschaft", "A→B", "Nimmt als Mitglied am UHB teil."),
    "DE:K049": ("Mitgliedschaft", "A→B", "Nimmt als Mitglied am UHB teil."),
    "SE:K003": ("Mitgliedschaft", "A→B", "Nimmt am Handslag teil."),
    "SE:K019": ("Mitgliedschaft", "A→B", "Trat Reboost bei und übergab den eigenen Reuse-Hub."),
    "SE:K020": ("Mitgliedschaft", "B→A", "Nimmt am Handslag teil."),
    "SE:K021": ("Mitgliedschaft", "B→A", "Nimmt am Handslag teil."),
    "SE:K022": ("Mitgliedschaft", "B→A", "Nimmt am Handslag teil."),
    # Brussels Environment is explicitly the programme coordinator.
    "BE:K074": ("Trägerschaft", "A→B", "Koordinierte das BAMB-Programm."),
    # The stored evidence says Lagemaat realised the centre, not that it runs it.
    "NL:K001": ("Bauausführung", "B→A", "Baute das Circular Centre Heerde aus Reuse-Material."),
    # The stored rows describe different relations than their current labels.
    "AT:K026": ("Kein Beleg für eine Beziehung", "—", "Keine Quelle belegt eine direkte Verbindung."),
    "AT:K029": ("Fachplanung", "B→A", "Übernahm das Projektmanagement des Stadionrückbaus."),
    "FI:K013": ("Dienstleistungsbeziehung", "B→A", "Bestimmte die Aufarbeitung der Reuse-Bauteile."),
    "FR:K034": ("Dienstleistungsbeziehung", "B→A", "Begleitete CANCAN beim Reuse-Vorhaben."),
}

SOURCE_RECHECKS = {
    "DK:K019": {
        "checked_at": "2026-08-15",
        "url": "https://www.linkedin.com/posts/a-gain_circulareconomy-upcyclestudios-sustainablearchitecture-activity-7264578680549490688-_FwC",
        "reachable": True,
        "finding": (
            "Ein offizieller a:gain-Beitrag ordnet Upcycle Studios eine Viddø-Prototyplieferung zu."
        ),
        "result": "clearer_relation_specific_passage_found",
        "proposed_evidence_url": "https://www.linkedin.com/posts/a-gain_circulareconomy-upcyclestudios-sustainablearchitecture-activity-7264578680549490688-_FwC",
        "proposed_evidence_quote": "We delivered a pre-development mock-up project delivery of Viddø.",
    },
    "FI:K031": {
        "checked_at": "2026-08-15",
        "url": "https://www.tampere.fi/en/current/2026/02/19/strategic-partnership-between-tampere-universities-and-city-tampere",
        "reachable": True,
        "finding": "Die Partnerschaft stärkt Tampere als Bildungs- und Wissenschaftsstandort.",
        "result": "clearer_relation_specific_passage_found",
    },
    "FI:K032": {
        "checked_at": "2026-08-15",
        "url": "https://www.aalto.fi/en/corporate-collaboration/strategic-research-institute-partner-vtt",
        "reachable": True,
        "finding": "Die Kooperation bündelt Forschung zur grünen und digitalen Transformation.",
        "result": "clearer_relation_specific_passage_found",
    },
}

REVIEW_REASONS = {
    "AT:K010": "Das Zitat nennt eine Mitgliedschaft in der BauKarussell-Genossenschaft.",
    "AT:K012": "Die gespeicherte Beziehung ist eine Genossenschaftsmitgliedschaft.",
    "AT:K013": "Die gespeicherte Beziehung ist eine Genossenschaftsmitgliedschaft.",
    "AT:K014": "Partnerteam und Genossenschaftsmitgliedschaft sind keine Konsortialrolle.",
    "AT:K015": "Die gespeicherte Beziehung ist eine Genossenschaftsmitgliedschaft.",
    "AT:K026": "Die Quelle nennt TEAMwork; die Identität mit TEAWork wurde nicht bestätigt.",
    "AT:K029": "Das Zitat belegt Bauprojektmanagement, nicht den Betrieb des Vorhabens.",
    "BE:K074": "Die Quelle nennt Brussels Environment als BAMB-Koordination.",
    "DE:K048": "Das UHB-Verzeichnis bezeichnet den Akteur ausdrücklich als Mitglied.",
    "DE:K049": "Das UHB-Verzeichnis bezeichnet den Akteur ausdrücklich als Mitglied.",
    "FI:K013": "Ramboll bestimmte Aufarbeitungsmaßnahmen für Consolis; das ist eine Leistung.",
    "FR:K034": "REFAIR begleitet CANCAN gerichtet; das ist eine Dienstleistungsbeziehung.",
    "NL:K001": "Die Quelle sagt, dass Lagemaat das Zentrum realisiert, nicht betreibt.",
    "SE:K003": "Die Quelle führt Akademiska Hus als angeschlossenen Handslag-Akteur.",
    "SE:K019": "Die Quelle nennt Fabege als neues Reboost-Mitglied.",
    "SE:K020": "Die Quelle führt HSB Göteborg als angeschlossenen Handslag-Akteur.",
    "SE:K021": "Die Quelle führt Serneke als angeschlossenen Handslag-Akteur.",
    "SE:K022": "Die Quelle nennt Vasakronan als Handslag-Mitglied.",
}

# Evidence-specific wording where a type-only sentence would hide the actual
# relationship.  Recurring consortium rows are handled by CONTEXT_PATTERNS.
SPECIAL = {
    "AT:K001": "Betreibt re:store als Herausgeberin.",
    "AT:K002": "Führte Social Urban Mining am MedUni-Campus durch.",
    "AT:K003": "Arbeiteten am MedUni-Campus zusammen.",
    "AT:K009": "Gründete die BauKarussell-Genossenschaft mit.",
    "AT:K022": "Schlossen eine Partnerschaft für Madaster Austria.",
    "AT:K005": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K006": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K020": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K021": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K024": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K025": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K027": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "BE:K043": "Gründete RotorDC als Spin-off.",
    "BE:K044": "Tauschten bei einem Rotor-Besuch Reuse-Wissen aus.",
    "BE:K045": "Beriet den CCRI-Piloten Uppsala zu Reuse.",
    "BE:K046": "Unterstützte die Entwicklung von Opalis.",
    "BE:K072": "Entwickelten das Tool Circulair Gebouwd gemeinsam.",
    "BE:K073": "Erarbeiteten gemeinsam einen Reuse-Umbau-Bericht.",
    "BE:K075": "Initiierte BauMaB in der Kasseler Klimastrategie.",
    "BE:K085": "Arbeiteten im Circular Retrofit Lab zusammen.",
    "BE:K086": "Kooperierten bei der Abbruchnachverfolgung.",
    "CH:K001": "Führt die Ressourcerie Lausanne als Zweigbetrieb.",
    "CH:K002": "Inventarisierten und vermarkteten Reuse-Bauteile.",
    "CH:K003": "Stellt den Marktplatz für ihren Bauteilverkauf.",
    "CH:K004": "Prüft, demontiert und transportiert BTVZ-Bauteile.",
    "CH:K005": "Führt Gruner ReUse als eigene Abteilung.",
    "CH:K006": "Vermittelt Bauteile an den Bauteilladen Winterthur.",
    "CH:K011": "Unterstützten gemeinsam das RE-WIN-Netzwerk.",
    "CH:K012": "Wählten Reuse-Bauteile für Hobelwerk Haus D aus.",
    "CH:K040": "Arbeiteten an der Schärenmoosstrasse zusammen.",
    "CH:K041": "Initiierten die erste RE-WIN-Fenstersammlung.",
    "CH:K042": "Katalogisierte Bauteile für Basler Wettbewerbe.",
    "CH:K046": "Programmierte den Basler Bauteilkatalog.",
    "DE:K031": "Entwickelten Matching-Algorithmen im Green-AI-Hub.",
    "DE:K033": "Starteten einen Ausbau-Stegreif am KIT.",
    "DE:K034": "Entwickelte den Urban Mining Index zur Software.",
    "DE:K035": "Betreiben den Urban Mining Hub Berlin gemeinsam.",
    "DE:K036": "Entwickelt die Bauteilbörse München mit.",
    "DK:K010": "Vertieften ihre Zusammenarbeit bei GreenDozer.",
    "DK:K023": "Führt GXN als Forschungsabteilung von 3XN.",
    "DK:K024": "Verknüpften GreenDozer-Materialien mit Revit.",
    "DK:K025": "Förderte das Hverringe Restaurierungszentrum.",
    "DK:K030": "Investierte in GreenDozer.",
    "DK:K031": "Investierte in GreenDozer.",
    "FI:K013": "Bestimmten die Aufarbeitung von Reuse-Bauteilen.",
    "FI:K016": "Erprobten demontierbare Betonverbindungen.",
    "FI:K023": "Pilotiert mit Espoo eine Reuse-Lösung.",
    "FI:K029": "Erprobten wiederlösbare Fliesen in Helsinki.",
    "FI:K031": "Stärken Tampere als Bildungs- und Wissenschaftsstandort.",
    "FI:K032": "Forschen zur grünen und digitalen Transformation.",
    "FI:K033": "Führte den Schulrückbau in Pohjois-Tapiola aus.",
    "FI:K036": "Trägt das SÄILÖ-Projekt federführend.",
    "FI:K038": "Tragen das KIELO-Projekt gemeinsam.",
    "FI:K039": "Führte den Rückbau im KIELO-Piloten aus.",
    "FI:K040": "Betreibt den Marktplatz Purkutori.fi.",
    "FR:K006": "Entwickelten eine Reuse-Lösung für Teppichfliesen.",
    "FR:K008": "Verbessern gemeinsam den Bodenbelag-Reuse.",
    "FR:K010": "Nimmt als Mitglied am CD2E-Netzwerk teil.",
    "FR:K024": "Betreibt das Pariser Straßenbau-Depot.",
    "FR:K031": "Arbeitete im Auftrag von La Fab Bordeaux.",
    "FR:K032": "Gründete das Reuse-Büro REMIX mit.",
    "FR:K034": "Begleitete CANCAN beim Reuse-Vorhaben.",
    "FR:K041": "Führt Lascombes Sud-Ouest als Regionaldepot.",
    "FR:K042": "Fördert die Arbeitsgruppen des Booster du Réemploi.",
    "FR:K044": "Organisieren den lokalen Reuse-Booster gemeinsam.",
    "GB:K031": "Bauten das Brighton Waste House gemeinsam.",
    "GB:K046": "Liefert Reuse-Stahl für HTS-Projekte.",
    "GB:K050": "Arbeiteten am ReFrame-Stahlpiloten zusammen.",
    "GB:K051": "Liefert Reuse-Stahl für Elliott-Wood-Projekte.",
    "GB:K062": "Planten 318 Oxford Street gemeinsam.",
    "GB:K072": "Bauten das PLP-Projekt gemeinsam.",
    "GB:K073": "Fertigten Tischlerarbeiten für das PLP-Projekt.",
    "GB:K074": "Lieferte Terrazzo für das PLP-Projekt.",
    "GB:K075": "Lieferte Reuse-Marmor für das PLP-Projekt.",
    "NL:K050": "Arbeiten im Urban Mining Collective zusammen.",
    "NL:K067": "Vereinbarten Verkauf und Rückmiete des Hauptsitzes.",
    "NL:K069": "Führen Oogstkaart.nl nach der Übernahme fort.",
    "NL:K075": "Demontiert den Circl-Pavillon im Auftrag.",
    "NL:K076": "Führt Icon Real Estate als Geschäftsbereich.",
    "NL:K077": "Betreibt das Urban Mining Collective mit.",
    "NL:K078": "Arbeiten im Urban Mining Collective zusammen.",
    "NO:K001": "Gründete das Reuse-Netz Oslo–Trondheim mit.",
    "NO:K010": "Trägt den CCRI-Piloten Asker.",
    "NO:K011": "Nimmt am Reuse-Netz Oslo–Trondheim teil.",
    "NO:K012": "Erprobte Sirkens Reuse-Container in Asker.",
    "NO:K013": "Erforschen Bürgerbeteiligung in Bodø gemeinsam.",
    "NO:K015": "Gründete das Reuse-Netz Oslo–Trondheim mit.",
    "NO:K016": "Nimmt am Reuse-Netz Oslo–Trondheim teil.",
    "NO:K018": "Nimmt am Reuse-Netz Oslo–Trondheim teil.",
    "NO:K019": "Nimmt am Reuse-Netz Oslo–Trondheim teil.",
    "NO:K020": "Betreibt das Reuse-Kaufhaus Resirkula.",
    "NO:K027": "Betreibt den Reuse-Handel der Ressourcenzentrale.",
    "SE:K001": "Gründete Bygghubben mit.",
    "SE:K009": "Gründete Bygghubben mit.",
    "SE:K011": "Trägt das Reuse-Zentrum Byggåterbruket.",
    "SE:K012": "Gründete Bygghubben mit.",
    "SE:K013": "Gründete Bygghubben mit.",
    "SE:K014": "Beteiligte sich als Miteigentümer an Bygghubben.",
    "SE:K015": "Gründete Bygghubben mit.",
    "SE:K019": "Trat Reboost bei und übergab den eigenen Reuse-Hub.",
    "SE:K026": "Betreibt den Reuse-Dienst Reboost.",
    "SE:K023": "Arbeiteten im schwedischen ReCreate-Piloten zusammen.",
}

PROJECT_SPECIAL = {
    "AT:K005": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K006": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K020": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K021": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K024": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K025": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "AT:K027": "Führte den Rückbau des Ferry-Dusika-Stadions aus.",
    "BE:K022": "Beauftragte das Musée du Folklore de Mouscron.",
    "CH:K007": "War am ELYS-Zentrum beteiligt; Aufgabe offen.",
    "DE:K001": "Beauftragte den zirkulären AWM-Büroumbau.",
    "DE:K026": "Führte den Innenausbau beim AWM-Büroumbau aus.",
    "DE:K027": "Entwarf den zirkulären AWM-Büroumbau.",
    "DE:K028": "Führte den Innenausbau beim AWM-Büroumbau aus.",
    "DE:K029": "Beschaffte Reuse-Material für den AWM-Büroumbau.",
    "GB:K001": "Beriet 55 Great Suffolk Street zur Nachhaltigkeit.",
    "DK:K019": "Lieferte einen Viddø-Fensterprototyp für Upcycle Studios.",
    "GB:K034": "Übernahm die Ingenieurplanung für Hastings Pier.",
    "GB:K036": "Lieferte CLT für Hastings Pier Visitor Centre.",
    "GB:K033": "Beauftragte den Bau des Hastings Pier Visitor Centre.",
    "GB:K068": "Führte Ausbauarbeiten am PLP London HQ aus.",
    "GB:K069": "Fertigte Tischlerarbeiten für das PLP London HQ.",
    "GB:K070": "Lieferte Terrazzo für das PLP London HQ.",
    "GB:K088": "Beriet Timber Square zur Nachhaltigkeit.",
    "NL:K018": "Steuerte das Projekt BioPartner 5.",
    "NL:K061": "Plante das Tragwerk für The Green House Utrecht.",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def currently_visible_ids() -> set[str]:
    netz_root = BASE.parents[1] / "netz"
    sys.path.insert(0, str(netz_root))
    from netz.cli import load_network  # noqa: PLC0415
    from netz.render.latex.table_grid import load_kanten  # noqa: PLC0415

    net = load_network()
    by_country = load_kanten(
        CLASSIFICATION, net, BASE / "merge_redirects_strict.json"
    )
    ids = {row["id"] for rows in by_country.values() for row in rows}
    if len(ids) != 268:
        raise SystemExit(f"expected 268 currently visible relationship IDs, found {len(ids)}")
    return ids


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def short_name(name: str, budget: int = 38) -> tuple[str, bool]:
    original = normalized(name)
    value = original.replace(chr(0x2026), "")
    for needle, replacement in ALIASES.items():
        if needle.casefold() in value.casefold():
            value = replacement
            break
    value = re.sub(r"\s*\([^)]*\)\s*", " ", value).strip()
    value = value.split(" / ")[0].strip()
    value = re.sub(
        r"\s+(?:GmbH|AG|AB|ApS|Oy|vzw|e\.V\.|Ltd\.?|SA|AS)$", "", value,
        flags=re.IGNORECASE,
    )
    if len(value) > budget:
        words = value.split()
        kept = []
        for word in words:
            trial = " ".join(kept + [word])
            if len(trial) > budget and kept:
                break
            kept.append(word)
        value = " ".join(kept)
    return value, value != original


def acting_endpoint(record: dict, direction: str) -> tuple[str, str]:
    if direction == "A→B":
        return record["node_a"]["name"], record["node_b"]["name"]
    if direction == "B→A":
        return record["node_b"]["name"], record["node_a"]["name"]
    return "beide Endpunkte", "beide Endpunkte"


def concrete_context(record: dict, classification: dict) -> str | None:
    haystack = " ".join(
        normalized(x) for x in (
            record.get("prior_relation_description"),
            classification.get("evidence_quote"),
            record["node_a"]["name"], record["node_b"]["name"],
            classification.get("evidence_url"),
        ) if x
    ).casefold()
    for pattern, label in CONTEXT_PATTERNS:
        if re.search(pattern, haystack, flags=re.IGNORECASE):
            return label
    return None


def material_from(record: dict, classification: dict) -> str:
    text = " ".join(
        normalized(x).casefold() for x in (
            record.get("prior_relation_description"),
            classification.get("evidence_quote"),
        ) if x
    )
    for pattern, label in (
        (r"steel|stahl", "Reuse-Stahl"),
        (r"brick|ziegel", "Reuse-Ziegel"),
        (r"timber|holz", "Reuse-Holz"),
        (r"carpet|textil|teppich", "Reuse-Teppichfliesen"),
        (r"concrete|beton", "Reuse-Betonbauteile"),
        (r"glass|glas", "Reuse-Glas"),
        (r"marble|marmor", "Reuse-Marmor"),
        (r"terrazzo", "Reuse-Terrazzo"),
    ):
        if re.search(pattern, text):
            return label
    return "Reuse-Bauteile"


def fit(prefix: str, name: str, suffix: str = ".") -> tuple[str, bool]:
    sentence = f"{prefix}{name}{suffix}"
    shortened = False
    if len(sentence) > MAX_DESCRIPTION:
        budget = MAX_DESCRIPTION - len(prefix) - len(suffix)
        name, shortened = short_name(name, max(10, budget))
        sentence = f"{prefix}{name}{suffix}"
    if len(sentence) > MAX_DESCRIPTION:
        raise ValueError(f"cannot fit description: {sentence!r}")
    return sentence, shortened


def actor_project_description(record: dict, c: dict) -> tuple[str, list[str]]:
    if record["id"] in PROJECT_SPECIAL:
        return PROJECT_SPECIAL[record["id"]], []
    project_node = record["node_a"] if record["node_a"]["is_project"] else record["node_b"]
    project, shortened = short_name(project_node["name"])
    art = c["beziehungsart"]
    material = material_from(record, c)
    warnings = ["project_name_shortened"] if shortened else []
    templates = {
        "Bauherrschaft": ("Verantwortete ", " als Bauherrschaft."),
        "Entwurf": ("Entwarf ", "."),
        "Fachplanung": (
            "Plante das Tragwerk für " if re.search(
                r"tragwerk|structur|ingenieur|engineer", " ".join((record.get("prior_relation_description") or "", c.get("evidence_quote") or "")), re.I
            ) else "Übernahm die Fachplanung für ", "."
        ),
        "Reuse-Konzept": ("Erarbeitete das Reuse-Konzept für ", "."),
        "Bauteilinventarisierung": ("Erfasste Reuse-Bauteile für ", "."),
        "Rückbau": ("Führte den Rückbau von ", " aus."),
        "Bauteillieferung": (f"Lieferte {material} für ", "."),
        "Aufarbeitung": (f"Arbeitete {material} für ", " auf."),
        "Logistik": ("Übernahm die Reuse-Logistik für ", "."),
        "Bauausführung": ("Führte die Bauarbeiten an ", " aus."),
        "Prüfung und Nachweis": ("Prüfte Reuse-Bauteile für ", "."),
        "Forschungsbegleitung": ("Begleitete ", " wissenschaftlich."),
        "Förderung": ("Förderte ", "."),
        "Betrieb": ("Betreibt ", "."),
        "Projektbeteiligung, Aufgabe unklar": ("War an ", " beteiligt; Aufgabe offen."),
    }
    prefix, suffix = templates[art]
    sentence, fitted = fit(prefix, project, suffix)
    if fitted and "project_name_shortened" not in warnings:
        warnings.append("project_name_shortened")
    return sentence, warnings


def actor_actor_description(record: dict, c: dict) -> tuple[str, list[str]]:
    rid = record["id"]
    if rid in SPECIAL:
        return SPECIAL[rid], []
    art = c["beziehungsart"]
    acting, target = acting_endpoint(record, c["richtung"])
    target, shortened = short_name(target)
    warnings = ["endpoint_name_shortened"] if shortened else []
    context = concrete_context(record, c)
    material = material_from(record, c)

    if art == "Konsortialpartner":
        if context:
            label = context if context.endswith("Verbund") else f"{context}-Verbund"
            return f"Arbeiteten im {label} zusammen.", warnings
        return "Arbeiteten in einem benannten Verbund zusammen.", warnings + ["context_not_named"]
    if art == "Kooperationsvereinbarung":
        if context:
            return f"Vereinbarten eine Kooperation für {context}.", warnings
        return "Schlossen eine formale Kooperationsvereinbarung.", warnings + ["context_not_named"]
    if art == "Gemeinsames Bauvorhaben":
        if context:
            return f"Arbeiteten am Vorhaben {context} zusammen.", warnings
        return "Arbeiteten an einem benannten Bauvorhaben zusammen.", warnings + ["context_not_named"]
    if art == "Gründung":
        return fit("Gründete ", target, " mit.")[0], warnings
    if art == "Übernahme":
        return fit("Übernahm ", target, ".")[0], warnings
    if art == "Konzernbindung":
        return fit("Führt ", target, " als Organisationseinheit.")[0], warnings
    if art == "Betreiberschaft":
        return fit("Betreibt ", target, ".")[0], warnings
    if art == "Mitgliedschaft":
        return fit("Nimmt als Mitglied an ", target, " teil.")[0], warnings
    if art == "Trägerschaft":
        return fit("Trägt ", target, ".")[0], warnings
    if art == "Lieferbeziehung":
        return fit(f"Liefert {material} für ", target, ".")[0], warnings
    if art == "Dienstleistungsbeziehung":
        if context:
            return f"Erbrachte eine Leistung für {context}.", warnings
        return fit("Erbrachte eine Auftragsleistung für ", target, ".")[0], warnings + ["task_not_named"]
    if art == "Personelle Verflechtung":
        return fit("Teilten Leitungspersonal mit ", target, ".")[0], warnings
    if art == "Zusammenarbeit, Art unklar":
        if context:
            return f"Kooperierten bei {context}; Form offen.", warnings
        return "Kooperierten in einem benannten Kontext; Form offen.", warnings + ["context_not_named"]
    raise KeyError(f"unhandled actor-actor type {art!r} for {rid}")


def directory_name(record: dict) -> str:
    text = f"{record['node_a']['name']} {record['node_b']['name']}".casefold()
    for needle, label in (
        ("opalis", "Opalis"), ("bauteilnetz", "bauteilnetz"),
        ("salvoweb", "SalvoWEB"), ("bolius", "Bolius"),
        ("byggogbevar", "byggogbevar"),
        ("skop marketplace", "Skop Marketplace"),
        ("cycle up", "Cycle Up"),
    ):
        if needle in text:
            return label
    return "nicht benannten"


def evidence_status(record: dict, c: dict, warnings: list[str]) -> tuple[str, list[str]]:
    if c.get("entfernen"):
        return "removal", warnings
    quote = normalized(c.get("evidence_quote"))
    url = normalized(c.get("evidence_url"))
    if not quote or quote == "—" or not url or url == "—":
        return "needs_source", warnings + ["missing_evidence"]
    if len(quote.split()) < 4:
        warnings = warnings + ["short_credit_quote"]
    if "context_not_named" in warnings or "task_not_named" in warnings:
        return "needs_source", warnings
    return "ready", warnings


def make_proposal(record: dict, c: dict) -> dict:
    art = c["beziehungsart"]
    if c.get("entfernen"):
        if art == "Verzeichniseintrag":
            directory = directory_name(record)
            description = f"Sind nur gemeinsam im {directory}-Verzeichnis gelistet."
            warnings = [] if directory != "nicht benannten" else ["directory_not_named"]
        elif art == "Beziehung nicht prüfbar":
            description = "Die gespeicherte Quelle war nicht überprüfbar."
            warnings = []
        else:
            description = "Keine Quelle belegt eine direkte Verbindung."
            warnings = []
    elif record["kind"] == "AKTEUR-BAUVORHABEN":
        description, warnings = actor_project_description(record, c)
    else:
        description, warnings = actor_actor_description(record, c)

    status, warnings = evidence_status(record, c, warnings)
    proposed_type = art
    proposed_direction = c["richtung"]
    proposed_remove = bool(c.get("entfernen"))
    if record["id"] in TYPE_CONFLICTS:
        proposed_type, proposed_direction, description = TYPE_CONFLICTS[record["id"]]
        proposed_remove = proposed_type in {
            "Kein Beleg für eine Beziehung", "Beziehung nicht prüfbar", "Verzeichniseintrag"
        }
        status = "type_conflict"
        warnings = warnings + ["explicit_type_or_direction_change_requires_approval"]
    if (record["id"] in SOURCE_RECHECKS and
            SOURCE_RECHECKS[record["id"]]["result"] == "no_clearer_relation_specific_passage"):
        status = "needs_source"
        warnings = warnings + ["source_reopened_no_relation_specific_passage"]
    acting, _ = acting_endpoint(record, c["richtung"])
    proposed_acting, _ = acting_endpoint(record, proposed_direction)
    proposal = {
        "id": record["id"],
        "country": record["country"],
        "batch": record["batch"],
        "kind": record["kind"],
        "node_a": record["node_a"]["name"],
        "node_b": record["node_b"]["name"],
        "type": art,
        "direction": c["richtung"],
        "acting_endpoint": acting,
        "proposed_type": proposed_type,
        "proposed_direction": proposed_direction,
        "proposed_acting_endpoint": proposed_acting,
        "current_remove": bool(c.get("entfernen")),
        "proposed_remove": proposed_remove,
        "current_description": c["beschreibung"],
        "prior_relation_description": record.get("prior_relation_description") or "—",
        "proposed_description": description,
        "character_count": len(description),
        "evidence_quote": c.get("evidence_quote") or "—",
        "evidence_url": c.get("evidence_url") or "—",
        "proposed_evidence_quote": SOURCE_RECHECKS.get(record["id"], {}).get(
            "proposed_evidence_quote", c.get("evidence_quote") or "—"
        ),
        "proposed_evidence_url": SOURCE_RECHECKS.get(record["id"], {}).get(
            "proposed_evidence_url", c.get("evidence_url") or "—"
        ),
        "review_status": status,
        "warnings": sorted(set(warnings)),
        "source_recheck": SOURCE_RECHECKS.get(record["id"]),
        "approved": False,
    }
    return proposal


def validate(proposals: list[dict], expected_ids: set[str]) -> list[str]:
    errors = []
    ids = [p["id"] for p in proposals]
    if len(ids) != 570:
        errors.append(f"expected 570 proposals, found {len(ids)}")
    if len(set(ids)) != len(ids):
        errors.append("duplicate proposal IDs")
    if set(ids) != expected_ids:
        errors.append("proposal ID set differs from classification")
    for p in proposals:
        text = p["proposed_description"]
        if not text or len(text) > MAX_DESCRIPTION:
            errors.append(f"{p['id']}: description length {len(text)}")
        if text[-1] not in ".!?":
            errors.append(f"{p['id']}: missing terminal punctuation")
        if any(term in text.casefold() for term in BANNED):
            errors.append(f"{p['id']}: banned phrase")
        if "\n" in text or "|" in text:
            errors.append(f"{p['id']}: unsafe table character")
        if chr(0x2026) in text or "benannten" in text.casefold():
            errors.append(f"{p['id']}: clipped or non-concrete wording")
        if "Verbund-Verbund" in text:
            errors.append(f"{p['id']}: duplicated context suffix")
        if "Aufgabe offen" in text and p["type"] != "Projektbeteiligung, Aufgabe unklar":
            errors.append(f"{p['id']}: Aufgabe offen used for wrong type")
        if p["type"] == "Verzeichniseintrag" and "Verzeichnis" not in text:
            errors.append(f"{p['id']}: directory removal lacks directory wording")
        allowed = ACTOR_PROJECT_TYPES if p["kind"] == "AKTEUR-BAUVORHABEN" else ACTOR_ACTOR_TYPES
        if p["proposed_type"] not in allowed and p["proposed_type"] not in {
            "Kein Beleg für eine Beziehung", "Beziehung nicht prüfbar", "Verzeichniseintrag"
        }:
            errors.append(f"{p['id']}: proposed type not allowed for kind")
    return errors


def md_escape(value: object) -> str:
    return normalized(str(value)).replace("|", "\\|")


def render_batch(batch_name: str, rows: list[dict]) -> str:
    lines = [
        f"# Beschreibungsreview: {batch_name}", "",
        "Status: review-only; keine kanonische Datei wurde geändert.", "",
    ]
    for row in rows:
        warnings = ", ".join(row["warnings"]) or "—"
        lines.extend([
            f"## {row['id']} — {md_escape(row['node_a'])} ↔ {md_escape(row['node_b'])}", "",
            f"- Art / Richtung: `{row['type']}` / `{row['direction']}`",
            f"- Aktuell im Semio-Netz sichtbar: `{row['currently_visible']}`",
            f"- Handelnder Endpunkt: {md_escape(row['acting_endpoint'])}",
            f"- Vorgeschlagene Art / Richtung: `{row['proposed_type']}` / `{row['proposed_direction']}`",
            f"- Vorgeschlagener handelnder Endpunkt: {md_escape(row['proposed_acting_endpoint'])}",
            f"- Entfernen aktuell / vorgeschlagen: `{row['current_remove']}` / `{row['proposed_remove']}`",
            f"- Aktuell: {md_escape(row['current_description'])}",
            f"- Vorschlag ({row['character_count']} Zeichen): **{md_escape(row['proposed_description'])}**",
            f"- Frühere Beziehungsbeschreibung: {md_escape(row['prior_relation_description'])}",
            f"- Belegzitat: “{md_escape(row['evidence_quote'])}”",
            f"- Quelle: {md_escape(row['evidence_url'])}",
            f"- Vorgeschlagenes Belegzitat: “{md_escape(row['proposed_evidence_quote'])}”",
            f"- Vorgeschlagene Quelle: {md_escape(row['proposed_evidence_url'])}",
            f"- Nachprüfung: {md_escape(row['source_recheck']['finding']) if row['source_recheck'] else '—'}",
            f"- Reviewstatus: `{row['review_status']}`; Warnung: `{warnings}`",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    classifications = load(CLASSIFICATION)
    inventory_doc = load(INVENTORY)
    decisions = load(DECISIONS)
    records = inventory_doc["records"]
    by_id = {r["id"]: r for r in records}

    if len(classifications) != 570 or len(by_id) != 570:
        raise SystemExit("input does not contain exactly 570 unique IDs")
    if set(classifications) != set(by_id):
        raise SystemExit("classification/inventory ID mismatch")

    proposals = [make_proposal(by_id[rid], classifications[rid]) for rid in sorted(by_id)]
    visible_ids = currently_visible_ids()
    for proposal in proposals:
        proposal["currently_visible"] = proposal["id"] in visible_ids
    errors = validate(proposals, set(classifications))
    if errors:
        raise SystemExit("proposal validation failed:\n" + "\n".join(errors))

    OUT.mkdir(exist_ok=True)
    BATCHES.mkdir(exist_ok=True)
    proposal_doc = {
        "schema_version": 1,
        "review_run": REVIEW_RUN,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "canonical_outputs_modified": False,
        "approved_for_apply": False,
        "max_description_characters": MAX_DESCRIPTION,
        "records": proposals,
    }
    proposal_path = OUT / "proposals.json"
    proposal_path.write_text(json.dumps(proposal_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    grouped = defaultdict(list)
    for row in proposals:
        grouped[row["batch"]].append(row)
    if len(grouped) != 34 or any(len(rows) > 20 for rows in grouped.values()):
        raise SystemExit("expected exactly 34 source-aligned batches of at most 20 rows")
    for batch_name, rows in sorted(grouped.items()):
        (BATCHES / batch_name).write_text(render_batch(batch_name, rows), encoding="utf-8")

    status_counts = Counter(p["review_status"] for p in proposals)
    country_counts = Counter(p["country"] for p in proposals)
    historical_kept_ids = {
        row["id"] for row in proposals if not classifications[row["id"]].get("entfernen")
    }
    summary = [
        "# Reviewindex: normalisierte Beziehungsbeschreibungen", "",
        "Dieser Ordner ist ein Review-Artefakt. Kanonische Ergebnisse, LaTeX-Fragmente",
        "und Neo4j bleiben bis zur ausdrücklichen Freigabe unverändert.", "",
        "## Abdeckung", "",
        f"- Vorschläge: **{len(proposals)}/570**",
        f"- Batches: **{len(grouped)}/34**, jeweils höchstens 20 Einträge",
        f"- Aktuell im Semio-Netz sichtbar: **{len(visible_ids)}**",
        f"- Historisch behaltene Kandidaten im 570er-Satz: **{len(historical_kept_ids)}**",
        f"- Zeichenlimit: **{MAX_DESCRIPTION}**; Überschreitungen: **0**",
        f"- Freigabe: **gesperrt** (`approved_for_apply: false`)", "",
        "## Reviewstatus", "",
    ]
    for status in ("ready", "needs_source", "type_conflict", "removal"):
        summary.append(f"- `{status}`: **{status_counts.get(status, 0)}**")
    visible_status = Counter(p["review_status"] for p in proposals if p["currently_visible"])
    summary.extend(["", "## Aktuell sichtbare 268 Beziehungen", ""])
    for status in ("ready", "needs_source", "type_conflict", "removal"):
        summary.append(f"- `{status}`: **{visible_status.get(status, 0)}**")
    summary.extend(["", "## Länder", ""])
    for cc, count in sorted(country_counts.items()):
        summary.append(f"- {cc}: {count}")
    summary.extend(["", "## Batches", ""])
    for batch_name, rows in sorted(grouped.items()):
        counts = Counter(r["review_status"] for r in rows)
        summary.append(
            f"- [{batch_name}](batches/{batch_name}) — {len(rows)} Einträge; "
            f"ready {counts.get('ready', 0)}, needs_source {counts.get('needs_source', 0)}, "
            f"type_conflict {counts.get('type_conflict', 0)}, removal {counts.get('removal', 0)}"
        )
    flagged = [p for p in proposals if p["review_status"] in {"needs_source", "type_conflict"}]
    summary.extend(["", "## Vor Freigabe zu klären", ""])
    if not flagged:
        summary.append("Keine automatisch markierten Quell- oder Typkonflikte.")
    else:
        for row in flagged:
            summary.append(
                f"- `{row['id']}` — {md_escape(row['node_a'])} ↔ {md_escape(row['node_b'])}: "
                f"`{row['review_status']}`; sichtbar `{row['currently_visible']}`; "
                f"`{row['type']} {row['direction']}` → "
                f"`{row['proposed_type']} {row['proposed_direction']}`; "
                f"entfernen `{row['current_remove']}` → `{row['proposed_remove']}` "
                f"({', '.join(row['warnings'])}) — "
                f"{md_escape(row['proposed_description'])}"
            )
    (OUT / "README.md").write_text("\n".join(summary).rstrip() + "\n", encoding="utf-8")

    decision_lines = [
        "# Offene Freigabeentscheidungen", "",
        f"Diese {len(flagged)} Fälle sind bewusst nicht automatisch angewendet. Jeder Fall muss",
        "bestätigt, korrigiert oder abgelehnt werden.", "",
    ]
    for row in flagged:
        decision_lines.extend([
            f"## {row['id']} — {md_escape(row['node_a'])} ↔ {md_escape(row['node_b'])}", "",
            f"- Aktuell sichtbar: `{row['currently_visible']}`",
            f"- Befund: {REVIEW_REASONS[row['id']]}",
            f"- Aktuell: `{row['type']} {row['direction']}`; entfernen `{row['current_remove']}`",
            f"- Vorschlag: `{row['proposed_type']} {row['proposed_direction']}`; entfernen `{row['proposed_remove']}`",
            f"- Textvorschlag: **{md_escape(row['proposed_description'])}**",
            f"- Belegzitat: “{md_escape(row['evidence_quote'])}”",
            f"- Quelle: {md_escape(row['evidence_url'])}",
            "",
        ])
    (OUT / "FLAGGED_DECISIONS.md").write_text(
        "\n".join(decision_lines).rstrip() + "\n", encoding="utf-8"
    )

    source_hashes = {
        str(path.relative_to(BASE)): sha256(path)
        for path in (CLASSIFICATION, INVENTORY, DECISIONS)
    }
    protected_paths = [
        BASE / "build_kanten_results.py",
        BASE / "KANTEN_TAXONOMIE.md",
        BASE / "validate_kanten.py",
        BASE / "KANTEN_ABSCHLUSSBERICHT_FINAL.md",
        BASE / "KANTEN_LATEX_AUDIT_FINAL.md",
        BASE / "strict_cleanup_network_audit.json",
        BASE.parents[1] / "netz" / "figs" / "frag_abb_netz.tex",
        BASE.parents[1] / "netz" / "figs" / "frag_tables_grid.tex",
        *sorted((BASE / "kanten_results").glob("kanten_*.md")),
    ]
    missing_protected = [str(path) for path in protected_paths if not path.is_file()]
    if missing_protected:
        raise SystemExit("missing protected outputs: " + ", ".join(missing_protected))
    protected_output_hashes = {
        path.resolve().as_posix(): sha256(path) for path in protected_paths
    }
    manifest = {
        "schema_version": 1,
        "review_run": REVIEW_RUN,
        "generated_at": proposal_doc["generated_at"],
        "source_hashes": source_hashes,
        "protected_output_hashes": protected_output_hashes,
        "coverage": {
            "expected": 570,
            "actual": len(proposals),
            "unique_ids": len({p["id"] for p in proposals}),
            "batch_count": len(grouped),
            "max_batch_size": max(map(len, grouped.values())),
        },
        "status_counts": dict(sorted(status_counts.items())),
        "proposal_sha256": sha256(proposal_path),
        "approved_for_apply": False,
        "approval": None,
        "canonical_outputs_modified": False,
    }
    (OUT / "approval_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
