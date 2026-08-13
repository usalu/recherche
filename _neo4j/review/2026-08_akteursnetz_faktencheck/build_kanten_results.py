# -*- coding: utf-8 -*-
"""Build the complete, evidence-backed 570-edge result set.

The 445 previously checked records are reclassified from their stored evidence
and relationship descriptions. Every one of the 125 previously unchecked
records has an explicit decision below (directory groups are expanded by ID).
The script fails closed if the current batch register differs from this reviewed
decision set.
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys
import unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(BASE, "kanten_batches", "_index.json")
INVENTORY = os.path.join(BASE, "kanten_review_inventory.json")
OUTDIR = os.path.join(BASE, "kanten_results")
DECISIONS = os.path.join(BASE, "kanten_decisions.json")

NO_EVIDENCE = (
    "Kein Beleg für eine Beziehung", "—",
    "Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung.", "—", "—",
)


def d(art, direction, description, url, quote):
    return {
        "beziehungsart": art, "richtung": direction,
        "beschreibung": description, "beleg": url, "belegzitat": quote,
    }


def no_evidence():
    return d(*NO_EVIDENCE)


# Every non-directory UNGEPRUEFT edge is decided explicitly.
UNCHECKED = {
    "AT:K016": no_evidence(),
    "AT:K017": d("Konsortialpartner", "—", "Beide arbeiteten im Forschungsprojekt BuildReUse zusammen.",
        "https://www.aee.at/gebaeude/114-zeitschrift/zeitschriften/nt-02-2022-waermenetze-im-wandel/1399-social-urban-mining-kreislaufwirtschaft-und-beschaeftigung-im-gebaeuderueckbau",
        "BauKarussell agiert ... gemeinsam mit dem Projektteam (AEE INTEC, FH Salzburg, IBO, Spar, KAGES und ATP sustain)."),
    "AT:K018": d("Konsortialpartner", "—", "Beide waren Projektpartner im Forschungsprojekt BuildReUse.",
        "https://www.aee-intec.at/project/build-re-use-100-prozent-re-use-und-recycling-bei-gebaeuden-mit-kurzen-nutzungszyklen/",
        "Projektpartner: Österreichisches Ökologie-Institut, ATP sustain, IBO ..."),
    "AT:K022": d("Kooperationsvereinbarung", "—", "ATP sustain ist formaler Partner von Madaster Austria.",
        "https://www.atp.ag/en/atp/responsibility/", "Since 2021, ATP has been a partner of Madaster."),

    "BE:K014": no_evidence(),
    "BE:K026": d("Fachplanung", "A→B", "Greisch übernahm Tragwerksleistungen für Recypark Demets.",
        "https://www.greisch.com/recypark-demets-a-anderlecht-recompense-aux-belgian-timber-construction-awards-2024/",
        "Bureau d'études : Greisch"),
    "BE:K045": d("Dienstleistungsbeziehung", "A→B", "Rotor beriet den CCRI-Pilot Uppsala zur Wiederverwendung.",
        "https://ecobuild.brussels/wp-content/uploads/2026/03/ccri-pilot-solutions-ki0125232enn.pdf",
        "As an advisory service provider, ROTOR supported the City Council with CCRI funding."),
    "BE:K046": d("Trägerschaft", "B→A", "Brussels Environment unterstützte die Entwicklung von Opalis.",
        "https://opalis.eu/en/about", "Opalis was developed with the support of Brussels Environment."),
    "BE:K073": d("Konsortialpartner", "—", "Beide arbeiteten am Bericht zum veränderungsgerichteten Umbau.",
        "https://researchportal.vub.be/en/publications/aanbevelingen-veranderingsgericht-verbouwen-eindrapportage-deelop",
        "The work was performed by VITO, Buildwise, UHasselt and VUB."),
    "BE:K075": d("Trägerschaft", "B→A", "Die Stadt Kassel initiierte BauMaB im Rahmen ihrer Klimastrategie.",
        "https://baumab-kassel.de/konzept/", "Das Projekt wurde im Rahmen der Klimaschutzstrategie der Stadt Kassel initiiert."),
    "BE:K083": no_evidence(),
    "BE:K086": d("Zusammenarbeit, Art unklar", "—", "OVAM und Tracimat arbeiten bei der Abbruchnachverfolgung zusammen.",
        "https://ovam.vlaanderen.be/bouw-sloopopvolging", "Voor de sloopopvolging worden de standaarddocumenten van Tracimat gebruikt."),

    "CH:K004": d("Dienstleistungsbeziehung", "B→A", "Stiftung Chance übernimmt Prüfung, Ausbau und Transport für die BTVZ.",
        "https://www.btvz.ch/portraet/", "Fachleute der Stiftung Chance prüfen die Bauteile, demontieren sie und übernehmen den Transport."),
    "CH:K008": d("Entwurf", "A→B", "baubüro in situ entwarf das Projekt Grubenstrasse 29.",
        "https://www.bauwelt.de/rubriken/bauten/Werkhof-29-Zuerich-baubuero-in-situ-ag-4385137.html",
        "Architekten: baubüro in situ ag"),
    "CH:K009": d("Entwurf", "A→B", "baubüro in situ entwarf das Projekt K.118.",
        "https://circularmaterialsystems.com/de/case/06_k-118/", "Architektur: Baubüro in situ"),
    "CH:K010": no_evidence(),
    "CH:K011": d("Zusammenarbeit, Art unklar", "—", "Beide unterstützen gemeinsam das RE-WIN-Netzwerk.",
        "https://re-win.ch/verein/ueber/", "Zusammenarbeit mit Baubüro in situ"),
    "CH:K014": no_evidence(),
    "CH:K045": d("Fachplanung", "B→A", "Monotti Ingegneri übernahm die Tragwerksplanung für ELEMENTA.",
        "https://media.bs.ch/original_file/8e80b99a92a09ee372ff54721421eb6497819e1f/bvd-jurybericht-walkeweg-komprimiert-1.pdf",
        "Bauingenieurwesen: Monotti Ingegneri Consulenti SA"),

    "DE:K025": d("Bauherrschaft", "B→A", "Die Gemeinde Ingersheim war Bauherrin des Jugendtreffs.",
        "https://klingelhoefer-kroetsch.de/projekte/jugendtreff-ingersheim/", "Bauherr: Gemeinde Ingersheim"),

    "DK:K010": d("Zusammenarbeit, Art unklar", "—", "Tscherning und GreenDozer stärkten ihre Zusammenarbeit.",
        "https://regnskaber.cvrapi.dk/34487362/amNsb3VkczovLzAzL2RkL2MxLzBjLzRlLzM1ZjUtNDdiNy1hYzYxLTU3NjA1MzRmMDQxYg.pdf",
        "styrket samarbejdet med GreenDozer"),
    "DK:K015": d("Bauteillieferung", "B→A", "a:gain lieferte wiederverwendete Produkte für TRÆ.",
        "https://www.again.dk/da/project-references/trae", "Leverede produkter til TRÆ"),
    "DK:K017": d("Fachplanung", "B→A", "Artelia übernahm Ingenieurleistungen für TRÆ.",
        "https://www.arteliagroup.com/fr/project/trae-a-wooden-tower-at-the-highest-level/", "Artelia is the engineer on TRÆ."),
    "DK:K023": d("Konzernbindung", "B→A", "GXN ist die Forschungs- und Entwicklungsabteilung von 3XN.",
        "https://en.wikipedia.org/wiki/3XN", "In 2007, 3XN established the research and development department GXN."),

    "FI:K006": no_evidence(),
    "FI:K023": d("Dienstleistungsbeziehung", "A→B", "Ramboll realisiert mit Espoo eine ausgewählte Wiederverwendungslösung.",
        "https://www.espoo.fi/en/we-are-looking-solutions-reuse-building-elements-joint-innovation-challenge-helsinki-metropolitan",
        "Ramboll was selected as one of the winners and will pilot the solution with the City of Espoo."),
    "FI:K026": d("Forschungsbegleitung", "B→A", "Tampere University begleitet den Lokomotion-Reuse-Piloten.",
        "https://recreate-project.eu/2026/02/24/second-reuse-mini-pilot-successful-in-finland/",
        "The Finnish ReCreate cluster and Lokomotion Technology completed the second reuse mini-pilot."),
    "FI:K027": d("Bauherrschaft", "B→A", "Die Stadt Helsinki verantwortet das Schulprojekt Melkinlaituri.",
        "https://paatokset.hel.fi/fi/asia/hel-2024-003973", "Melkinlaiturin peruskoulu ... Helsingin kaupunki"),
    "FI:K031": d("Kooperationsvereinbarung", "—", "Universität und Stadt schlossen eine strategische Partnerschaft.",
        "https://www.tampere.fi/en/current/2026/02/19/strategic-partnership-between-tampere-universities-and-city-tampere",
        "Strategic partnership between Tampere Universities and the City of Tampere"),
    "FI:K032": d("Kooperationsvereinbarung", "—", "Aalto University und VTT haben eine strategische Partnerschaft.",
        "https://www.aalto.fi/en/corporate-collaboration/strategic-research-institute-partner-vtt",
        "Aalto University and VTT have signed a strategic partnership agreement."),
    "FI:K037": no_evidence(),

    "FR:K031": d("Dienstleistungsbeziehung", "B→A", "Collectif CANCAN arbeitete im Auftrag von La Fab Bordeaux.",
        "https://www.collectifcancan.fr/project/promenade/", "Commanditaire : La Fab"),
    "FR:K034": d("Zusammenarbeit, Art unklar", "—", "REFAIR Bordeaux begleitete CANCAN beim Wiederverwendungsvorhaben.",
        "https://refair-bm.fr/le-reemploi-cest-la-base/", "REFAIR accompagne CANCAN Architecture sur le réemploi."),
    "FR:K038": d("Konsortialpartner", "—", "CSTB und INEC gehörten zum LIFE-Waste2Build-Konsortium.",
        "https://www.cstb.fr/toutes-les-actualites/economie-circulaire-batiment",
        "Le CSTB a rejoint le consortium ... avec l'Institut National de l'Économie Circulaire."),
    "FR:K041": d("Konzernbindung", "A→B", "Lascombes Sud-Ouest ist ein regionales Nebendepot des Unternehmens.",
        "https://www.lascombes-sud-ouest.fr/p-infos-pratiques_fr.htm",
        "Lascombes Sud-Ouest est le dépôt régional secondaire de l'entreprise."),

    "GB:K025": d("Bauteillieferung", "B→A", "Cleveland lieferte wiederverwendeten Stahl für Brent Cross Town.",
        "https://asbp.org.uk/case-studies/brent-cross-town-primary-substation",
        "Cleveland Steel & Tubes supplied the reclaimed steel."),
    "GB:K042": d("Bauteillieferung", "B→A", "Cleveland lieferte wiederverwendeten Stahl für Holbein Gardens.",
        "https://terc.org.uk/54-2/", "Steel supplier: Cleveland Steel & Tubes"),
    "GB:K046": d("Lieferbeziehung", "B→A", "Cleveland liefert wiederverwendeten Stahl für HTS-Projekte.",
        "https://hts.uk.com/news-views/the-future-of-steel-reuse/", "We work closely with Cleveland Steel & Tubes."),
    "GB:K047": d("Gründung", "A→B", "HTS ist Gründungsmitglied des Engineers Reuse Collective.",
        "https://hts.uk.com/news-views/introducing-the-engineers-reuse-collective/", "Founding members include Heyne Tillett Steel."),
    "GB:K048": d("Bauteillieferung", "A→B", "Cleveland lieferte wiederverwendeten Stahl für Timber Square.",
        "https://timberdevelopment.uk/print-and-ink-buildings-timber-square/", "125 tonnes of reused steel were sourced from Cleveland Steel & Tubes."),
    "GB:K049": d("Bauteillieferung", "A→B", "Cleveland lieferte Stahl für 55 Great Suffolk Street.",
        "https://asbp.org.uk/case-studies/55-great-suffolk-street", "11.1 tonnes of steel were procured from Cleveland Steel & Tubes."),
    "GB:K059": d("Fachplanung", "B→A", "Civic Engineers übernahm die Tragwerksplanung für House of Fraser.",
        "https://www.building.co.uk/buildings/its-mandss-oxford-street-neighbour-and-its-being-refurbished-not-demolished/5129238.article",
        "Structural engineer: Civic Engineers"),
    "GB:K060": d("Entwurf", "B→A", "Studio PDP übernahm den Entwurf für House of Fraser.",
        "https://studiopdp.com/blog/oxford-streets-sleeping-giant-awakens", "Studio PDP is leading the transformation of 318 Oxford Street."),
    "GB:K061": d("Gründung", "A→B", "Webb Yates ist Gründungsmitglied von TERC.",
        "https://hts.uk.com/news-views/introducing-the-engineers-reuse-collective/", "Founding members include Webb Yates Engineers."),
    "GB:K063": d("Gründung", "A→B", "Civic Engineers ist Gründungsmitglied von TERC.",
        "https://hts.uk.com/news-views/introducing-the-engineers-reuse-collective/", "Founding members include Civic Engineers."),
    "GB:K082": d("Bauherrschaft", "B→A", "Fabrix entwickelte das Projekt Roots in the Sky.",
        "https://www.knightfrank.com/research/article/2022-10-26-esg-in-real-estate-roots-in-the-sky-fabrix-case-study",
        "Roots in the Sky is being built speculatively by Fabrix."),
    "GB:K083": d("Prüfung und Nachweis", "A→B", "AKT II prüfte und plante den Stahlreuse für 55 Great Suffolk Street.",
        "https://www.architectsjournal.co.uk/news/developer-urban-mines-broadgate-steel-frame-for-southwark-retrofits",
        "AKT II was involved in assessing and repurposing the steel."),
    "GB:K084": d("Fachplanung", "A→B", "Symmetrys übernahm Tragwerks- und Tiefbauplanung für das Projekt.",
        "https://symmetrys.com/project/great-suffolk-street/", "Symmetrys was employed as structural and civil engineer."),
    "GB:K085": d("Bauausführung", "A→B", "Mace wurde als Hauptauftragnehmer für Timber Square beauftragt.",
        "https://www.macegroup.com/en-us/news/mace-to-deliver-landsecs-timber-square-a-grade-a-office-redevelopment-in-central-london/",
        "Mace has been appointed to deliver Timber Square."),
    "GB:K095": d("Gründung", "B→A", "Elliott Wood ist Gründungsmitglied von TERC.",
        "https://hts.uk.com/news-views/introducing-the-engineers-reuse-collective/", "Founding members include Elliott Wood."),

    "NL:K002": d("Entwurf", "B→A", "cepezed entwarf das Circular Centre in Heerde.",
        "https://www.cepezed.com/recent/flexibel-ontwerpproces-circulair-centrum-bouwen-met-de-stenen-die-je-hebt/",
        "cepezed and client Lagemaat worked closely together on the Circular Centre in Heerde."),
    "NL:K005": d("Fachplanung", "B→A", "IMd verantwortet Tragwerksentwurf und Bauteilnachweise für das Zentrum.",
        "https://imdbv.nl/nieuws/koninklijk-bezoek-circulair-centrum-heerde",
        "IMd is verantwoordelijk voor het constructief ontwerp en het onderzoek naar de constructieve capaciteit."),
    "NL:K010": d("Gründung", "A→B", "cepezedprojects gründete lcp-circulair gemeinsam mit Lagemaat.",
        "https://iconrealestate.com/news/landmark-for-circular-innovation-circl-dismantling-to-commence/",
        "Lcp circulair, a joint venture between cepezedprojects and Lagemaat."),
    "NL:K012": d("Fachplanung", "A→B", "IMd gehörte zum Planungsteam von Montessori Maassluis.",
        "https://www.kraaijvanger.nl/nl/projecten/montessori-maassluis", "Designteam: IMd Raadgevende Ingenieurs"),
    "NL:K076": d("Konzernbindung", "B→A", "Icon Real Estate ist ein Geschäftsbereich der Victory Group.",
        "https://zuidas.nl/en/construction-project/mahler-1/", "Icon Real Estate, a division of Victory Group"),

    "NO:K014": no_evidence(),
    "NO:K017": no_evidence(),
    "NO:K021": d("Konsortialpartner", "—", "TOBB und Rehub sind Partner im Forschungsprojekt Vendom.",
        "https://tobb.no/itobb/tobb-med-i-vendom-veien-mot-en-sirkulaer-byggenaering/",
        "Partnere i Vendom: ... Rehub ... TOBB ..."),
    "NO:K022": no_evidence(),

    "SE:K011": d("Trägerschaft", "B→A", "Byggåterbruket ist ein Projekt innerhalb der Stadt Umeå.",
        "https://www.umea.se/download/18.1de870d7195cb1f57ec433c/1743065440894/KSHU_2025-01-28_protokoll.pdf",
        "Byggåterbruket startade genom ett politiskt initiativ och är en del av Umeå kommun."),
    "SE:K018": d("Konsortialpartner", "—", "Contiga und Zengun waren Partner im Forschungsprojekt Återhus.",
        "https://www.fabege.se/om-fabege/pressrum/nyheter/2022/hallbarhetshuset/",
        "Samverkansparter i projektet Återhus: ... Contiga ... Zengun."),
    "SE:K023": d("Konsortialpartner", "—", "Helsingborgshem und KTH arbeiteten im ReCreate-Pilotprojekt zusammen.",
        "https://www.kth.se/om/nyheter/centrala-nyheter/gammal-betong-far-nytt-liv-1.1077230",
        "I den svenska piloten är Helsingborgshem huvudsaklig partner ... och KTH deltar."),
}


DIRECTORY_GROUPS = {
    "BE": (range(47, 72), "https://opalis.eu/en", "Opalis is a business directory."),
    "DE": (range(37, 48), "https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf",
           "Bremen, Berlin, Oldenburg, Saarbrücken, Gießen, Nordhausen, Augsburg, Weißenburg, Köln"),
    "DK": ([26, 27, 28, 29, *range(32, 43)], "https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121",
           "Landsdækkende guide: Her kan du købe genbrugsmaterialer"),
    "GB": (range(7, 16), "https://www.salvoweb.com/salvo-directory",
           "The world's most comprehensive architectural salvage directory."),
    "NO": (range(23, 26), "https://byggogbevar.no/ressurser/",
           "Forhandlere ombruk: Det er flere forhandlere som har spesialisert seg på omsetning av brukte byggevarer."),
}


# Overrides for GEPRUEFT actor-actor records and the handful of unusual roles.
CHECKED = {
    "AT:K001": ("Betreiberschaft", "B→A"), "AT:K002": ("Dienstleistungsbeziehung", "B→A"),
    "AT:K003": ("Gemeinsames Bauvorhaben", "—"), "AT:K007": NO_EVIDENCE[:2],
    "AT:K009": ("Gründung", "B→A"), "AT:K030": NO_EVIDENCE[:2],
    "BE:K043": ("Gründung", "A→B"), "BE:K044": ("Zusammenarbeit, Art unklar", "—"),
    "BE:K072": ("Zusammenarbeit, Art unklar", "—"), "BE:K085": ("Konsortialpartner", "—"),
    "CH:K001": ("Konzernbindung", "B→A"), "CH:K002": ("Gemeinsames Bauvorhaben", "—"),
    "CH:K003": ("Dienstleistungsbeziehung", "B→A"), "CH:K005": ("Konzernbindung", "B→A"),
    "CH:K006": ("Dienstleistungsbeziehung", "A→B"), "CH:K012": ("Gemeinsames Bauvorhaben", "—"),
    "CH:K037": ("Konsortialpartner", "—"), "CH:K040": ("Gemeinsames Bauvorhaben", "—"),
    "CH:K041": ("Gründung", "A→B"), "CH:K042": ("Dienstleistungsbeziehung", "A→B"),
    "CH:K044": ("Konsortialpartner", "—"), "CH:K046": ("Dienstleistungsbeziehung", "A→B"),
    "DE:K031": ("Konsortialpartner", "—"), "DE:K032": NO_EVIDENCE[:2],
    "DE:K033": ("Kooperationsvereinbarung", "—"), "DE:K034": ("Trägerschaft", "B→A"),
    "DE:K035": ("Kooperationsvereinbarung", "—"), "DE:K036": ("Betreiberschaft", "A→B"),
    "DK:K009": ("Konsortialpartner", "—"), "DK:K024": ("Kooperationsvereinbarung", "—"),
    "DK:K025": ("Trägerschaft", "A→B"), "DK:K030": ("Konzernbindung", "B→A"),
    "DK:K031": ("Konzernbindung", "B→A"),
    "FI:K016": ("Konsortialpartner", "—"), "FI:K029": ("Gemeinsames Bauvorhaben", "—"),
    "FI:K030": ("Konsortialpartner", "—"), "FI:K033": ("Dienstleistungsbeziehung", "B→A"),
    "FI:K034": ("Konsortialpartner", "—"), "FI:K035": ("Konsortialpartner", "—"),
    "FI:K036": ("Trägerschaft", "A→B"), "FI:K039": ("Dienstleistungsbeziehung", "B→A"),
    "FI:K040": ("Betreiberschaft", "B→A"),
    "FR:K001": ("Verzeichniseintrag", "—"), "FR:K002": NO_EVIDENCE[:2],
    "FR:K003": ("Verzeichniseintrag", "—"), "FR:K004": ("Verzeichniseintrag", "—"),
    "FR:K005": ("Verzeichniseintrag", "—"), "FR:K006": ("Kooperationsvereinbarung", "—"),
    "FR:K007": ("Verzeichniseintrag", "—"), "FR:K008": ("Kooperationsvereinbarung", "—"),
    "FR:K009": NO_EVIDENCE[:2], "FR:K010": ("Mitgliedschaft", "A→B"),
    "FR:K024": ("Betreiberschaft", "A→B"), "FR:K032": ("Gründung", "A→B"),
    "FR:K033": ("Konsortialpartner", "—"), "FR:K042": ("Trägerschaft", "A→B"),
    "FR:K043": NO_EVIDENCE[:2], "FR:K044": ("Kooperationsvereinbarung", "—"),
    "GB:K005": NO_EVIDENCE[:2], "GB:K006": NO_EVIDENCE[:2],
    "GB:K026": ("Gründung", "A→B"), "GB:K031": ("Gemeinsames Bauvorhaben", "—"),
    "GB:K050": ("Konsortialpartner", "—"), "GB:K051": ("Lieferbeziehung", "A→B"),
    "GB:K062": ("Gemeinsames Bauvorhaben", "—"), "GB:K072": ("Gemeinsames Bauvorhaben", "—"),
    "GB:K073": ("Gemeinsames Bauvorhaben", "—"), "GB:K074": ("Lieferbeziehung", "A→B"),
    "GB:K075": ("Lieferbeziehung", "A→B"),
    "NL:K007": ("Gründung", "A→B"), "NL:K008": NO_EVIDENCE[:2],
    "NL:K034": ("Bauteilinventarisierung", "B→A"),
    "NL:K067": ("Zusammenarbeit, Art unklar", "—"),
    "NL:K069": ("Kooperationsvereinbarung", "—"), "NL:K075": ("Dienstleistungsbeziehung", "A→B"),
    "NL:K077": ("Betreiberschaft", "A→B"),
    "NO:K001": ("Gründung", "A→B"), "NO:K009": NO_EVIDENCE[:2],
    "NO:K010": ("Trägerschaft", "A→B"), "NO:K011": ("Mitgliedschaft", "A→B"),
    "NO:K012": ("Dienstleistungsbeziehung", "B→A"), "NO:K013": ("Kooperationsvereinbarung", "—"),
    "NO:K015": ("Gründung", "A→B"), "NO:K016": ("Mitgliedschaft", "A→B"),
    "NO:K018": ("Mitgliedschaft", "B→A"), "NO:K019": ("Mitgliedschaft", "B→A"),
    "NO:K020": ("Betreiberschaft", "B→A"), "NO:K026": NO_EVIDENCE[:2],
    "NO:K027": ("Betreiberschaft", "A→B"),
    "SE:K001": ("Gründung", "A→B"), "SE:K008": ("Konsortialpartner", "—"),
    "SE:K009": ("Gründung", "A→B"), "SE:K010": NO_EVIDENCE[:2],
    "SE:K012": ("Gründung", "B→A"), "SE:K013": ("Gründung", "B→A"),
    "SE:K014": ("Gründung", "B→A"), "SE:K015": ("Gründung", "B→A"),
    "SE:K026": ("Betreiberschaft", "A→B"), "SE:K027": ("Konsortialpartner", "—"),
}


PROJECT_BLANK = {
    "AT:K008": "Reuse-Konzept", "AT:K011": "Reuse-Konzept",
    "AT:K023": "Projektbeteiligung, Aufgabe unklar",
    "AT:K028": "Projektbeteiligung, Aufgabe unklar",
    "BE:K004": "Kein Beleg für eine Beziehung", "BE:K011": "Fachplanung",
    "BE:K013": "Projektbeteiligung, Aufgabe unklar", "BE:K015": "Bauherrschaft",
    "BE:K020": "Bauherrschaft", "BE:K021": "Bauherrschaft",
    "BE:K027": "Entwurf", "BE:K028": "Entwurf", "BE:K030": "Aufarbeitung",
    "BE:K007": "Entwurf", "BE:K031": "Entwurf", "BE:K032": "Entwurf",
    "BE:K033": "Fachplanung", "BE:K034": "Fachplanung", "BE:K035": "Fachplanung",
    "BE:K036": "Bauherrschaft", "CH:K007": "Projektbeteiligung, Aufgabe unklar",
    "CH:K016": "Bauteilinventarisierung", "CH:K025": "Bauausführung",
    "CH:K026": "Projektbeteiligung, Aufgabe unklar", "CH:K043": "Bauteillieferung",
    "CH:K028": "Fachplanung", "CH:K032": "Fachplanung",
    "CH:K034": "Forschungsbegleitung", "CH:K035": "Bauausführung",
    "DE:K004": "Fachplanung", "DE:K005": "Projektbeteiligung, Aufgabe unklar",
    "DE:K011": "Kein Beleg für eine Beziehung", "DE:K017": "Betrieb",
    "DE:K018": "Forschungsbegleitung", "DE:K028": "Bauausführung",
    "DE:K029": "Reuse-Konzept", "DK:K004": "Fachplanung", "DK:K005": "Rückbau",
    "DK:K007": "Kein Beleg für eine Beziehung", "DK:K012": "Prüfung und Nachweis",
    "FI:K014": "Aufarbeitung", "FI:K015": "Aufarbeitung",
    "FR:K014": "Bauausführung", "FR:K020": "Fachplanung",
    "FR:K026": "Prüfung und Nachweis", "GB:K003": "Fachplanung",
    "GB:K019": "Bauherrschaft", "GB:K020": "Bauherrschaft",
    "GB:K030": "Bauausführung", "GB:K037": "Aufarbeitung", "GB:K044": "Reuse-Konzept",
    "GB:K052": "Bauherrschaft", "GB:K053": "Bauausführung",
    "GB:K069": "Bauausführung", "GB:K090": "Fachplanung", "GB:K092": "Fachplanung",
    "NL:K024": "Bauherrschaft", "NL:K025": "Entwurf", "NL:K026": "Entwurf",
    "NL:K027": "Fachplanung", "NL:K028": "Fachplanung", "NL:K029": "Bauteillieferung",
    "NL:K030": "Bauausführung", "NL:K031": "Bauausführung",
    "NL:K006": "Prüfung und Nachweis", "NL:K018": "Fachplanung",
    "NL:K021": "Bauausführung", "NL:K022": "Bauausführung",
    "NL:K033": "Reuse-Konzept", "NL:K034": "Bauteilinventarisierung",
    "NL:K038": "Fachplanung", "NL:K045": "Bauteillieferung",
    "NL:K046": "Bauteillieferung", "NL:K047": "Entwurf", "NL:K048": "Entwurf",
    "NL:K049": "Bauteillieferung",
    "NL:K052": "Reuse-Konzept", "NL:K053": "Reuse-Konzept",
    "NL:K055": "Prüfung und Nachweis", "NL:K057": "Bauausführung",
    "NL:K058": "Forschungsbegleitung",
    "NL:K070": "Bauherrschaft", "NL:K074": "Fachplanung",
    "NO:K006": "Reuse-Konzept", "NO:K007": "Entwurf", "NO:K008": "Betrieb",
    "GB:K089": "Fachplanung",
    "SE:K031": "Entwurf", "SE:K032": "Bauausführung",
}


DESCRIPTION = {
    "Bauherrschaft": "Der Akteur verantwortete das Vorhaben als Bauherr.",
    "Entwurf": "Der Akteur übernahm den architektonischen Entwurf.",
    "Fachplanung": "Der Akteur übernahm eine benannte Fachplanung.",
    "Reuse-Konzept": "Der Akteur entwickelte das Wiederverwendungskonzept.",
    "Bauteilinventarisierung": "Der Akteur inventarisierte Bauteile und Materialien.",
    "Rückbau": "Der Akteur führte den selektiven Rückbau aus.",
    "Bauteillieferung": "Der Akteur lieferte wiederverwendete Bauteile.",
    "Aufarbeitung": "Der Akteur arbeitete wiederverwendete Bauteile auf.",
    "Logistik": "Der Akteur übernahm Lagerung oder Transport.",
    "Bauausführung": "Der Akteur führte benannte Bauleistungen aus.",
    "Prüfung und Nachweis": "Der Akteur prüfte oder zertifizierte Bauteile.",
    "Forschungsbegleitung": "Der Akteur begleitete das Vorhaben wissenschaftlich.",
    "Förderung": "Der Akteur finanzierte oder förderte das Vorhaben.",
    "Betrieb": "Der Akteur betrieb das Vorhaben oder die Einrichtung.",
    "Projektbeteiligung, Aufgabe unklar": "Die Quelle belegt die Beteiligung, aber keine genaue Aufgabe.",
    "Konsortialpartner": "Beide sind als Partner desselben Konsortiums belegt.",
    "Kooperationsvereinbarung": "Die Quelle belegt eine formalisierte Zusammenarbeit.",
    "Gemeinsames Bauvorhaben": "Beide arbeiteten nachweislich am selben Bauvorhaben.",
    "Gründung": "Die Quelle belegt die Gründungsbeziehung.",
    "Übernahme": "Die Quelle belegt die Übernahmebeziehung.",
    "Konzernbindung": "Die Quelle belegt die organisatorische Zugehörigkeit.",
    "Betreiberschaft": "Die Quelle belegt, wer die Einrichtung betreibt.",
    "Mitgliedschaft": "Die Quelle belegt die Mitgliedschaft im Netzwerk.",
    "Trägerschaft": "Die Quelle belegt institutionelle Trägerschaft oder Finanzierung.",
    "Lieferbeziehung": "Die Quelle belegt eine konkrete Lieferbeziehung.",
    "Dienstleistungsbeziehung": "Die Quelle belegt eine konkrete Auftragsleistung.",
    "Personelle Verflechtung": "Die Quelle belegt eine personelle Verflechtung.",
    "Zusammenarbeit, Art unklar": "Die Zusammenarbeit ist belegt; ihre Form bleibt unklar.",
    "Verzeichniseintrag": "Die Kante beruht nur auf einer Verzeichnislistung.",
}


def ascii_lower(value):
    return "".join(c for c in unicodedata.normalize("NFKD", value or "")
                   if not unicodedata.combining(c)).lower()


def project_role(record):
    if record["id"] in PROJECT_BLANK:
        return PROJECT_BLANK[record["id"]]
    if record.get("prior_relation_code") == "BETREIBER":
        return "Betrieb"
    text = ascii_lower(record.get("prior_relation_description", ""))
    rules = [
        ("Förderung", r"forder|foerder|funding|finanz|grant|zuschuss|realdania|stotte"),
        ("Bauherrschaft", r"bauherr|auftraggeber|client|owner|developer|byggher|opdrachtgever|bestaller"),
        ("Entwurf", r"architekt|architect|entwurf|design|ontwerp|tegnet"),
        ("Bauteilinventarisierung", r"inventar|materialpass|scan|kartier|audit|catalog"),
        ("Reuse-Konzept", r"reuse.konzept|wiederverwendungskonzept|circularity concept|reuse strategy|reemploi"),
        ("Rückbau", r"ruckbau|rueckbau|demont|dismant|deconstruct|demolition|purku|nedriv|salvage"),
        ("Bauteillieferung", r"liefer|suppl|sourced|bereitstell|materialbereit|donor|procure"),
        ("Aufarbeitung", r"aufarbeit|refurb|recondition|repair|repar|upcycl"),
        ("Logistik", r"logistik|transport|lagerung|storage"),
        ("Prüfung und Nachweis", r"pruf|pruef|nachweis|zertifiz|test|assess|certif|quality|brandveilig"),
        ("Forschungsbegleitung", r"forsch|research|wissenschaft|monitoring|universit|hochschule|kth|ntnu"),
        ("Fachplanung", r"ingenieur|engineer|fachplan|tragwerk|structur|consult|beratung|akust|landscape|landschaft|planung|quantity survey|cost management"),
        ("Bauausführung", r"bauausfuhr|bauausfuehr|ausfuhr|ausfuehr|contractor|entrepren|construction|erricht|built|install|montage|ausbau|main works"),
        ("Betrieb", r"betrieb|operate|drift"),
        ("Projektbeteiligung, Aufgabe unklar", r"partner|beteilig|projektteam|project team|involved|mitwirk|collabor"),
    ]
    for art, pattern in rules:
        if re.search(pattern, text):
            return art
    raise ValueError(f"keine Projektrolle aus Beschreibung ableitbar: {record['id']} {text}")


def actor_project_direction(record):
    return "B→A" if record["node_a"]["is_project"] else "A→B"


def short_quote(value):
    value = " ".join((value or "").split())
    if len(value) <= 240:
        return value
    return value[:240].rsplit(" ", 1)[0]


def checked_decision(record):
    rid, kind = record["id"], record["kind"]
    if kind == "AKTEUR-BAUVORHABEN":
        art = project_role(record)
        direction = actor_project_direction(record)
    elif rid in CHECKED:
        art, direction = CHECKED[rid]
    else:
        code = record.get("prior_relation_code")
        fixed = {
            "KONSORTIUM": ("Konsortialpartner", "—"),
            "GRUENDER": ("Gründung", None),
            "KONZERN": ("Konzernbindung", None),
            "UEBERNAHME": ("Übernahme", None),
            "BETREIBER": ("Betreiberschaft", None),
        }.get(code)
        if not fixed:
            raise ValueError(f"ungeklärte GEPRUEFT-Kante: {rid} code={code!r}")
        art, direction = fixed
        if direction is None:
            raise ValueError(f"gerichtete GEPRUEFT-Kante braucht Override: {rid}")

    if art == NO_EVIDENCE[0]:
        return no_evidence()
    return d(art, direction, DESCRIPTION[art], "vorhanden", short_quote(record["evidence_quote"]))


def expand_directory_decisions():
    out = {}
    for cc, (numbers, url, quote) in DIRECTORY_GROUPS.items():
        for number in numbers:
            rid = f"{cc}:K{number:03d}"
            out[rid] = d("Verzeichniseintrag", "—", DESCRIPTION["Verzeichniseintrag"], url, quote)
    return out


def safe_cell(value):
    return " ".join(str(value).replace("|", "/").split())


def main():
    idx = json.load(open(INDEX, encoding="utf-8"))
    inv = json.load(open(INVENTORY, encoding="utf-8"))
    records = {r["id"]: r for r in inv["records"]}
    expected = {e["id"] for b in idx["batches"] for e in b["edges"]}
    if set(records) != expected:
        raise SystemExit("ABBRUCH: Inventar und aktuelles Kantenregister stimmen nicht überein.")

    explicit_unchecked = dict(UNCHECKED)
    overlap = set(explicit_unchecked) & set(expand_directory_decisions())
    if overlap:
        raise SystemExit(f"ABBRUCH: doppelte UNGEPRUEFT-Entscheidungen: {sorted(overlap)}")
    explicit_unchecked.update(expand_directory_decisions())
    actual_unchecked = {rid for rid, r in records.items() if r["status"] == "UNGEPRUEFT"}
    if set(explicit_unchecked) != actual_unchecked:
        missing = sorted(actual_unchecked - set(explicit_unchecked))
        extra = sorted(set(explicit_unchecked) - actual_unchecked)
        raise SystemExit(f"ABBRUCH: UNGEPRUEFT-Abdeckung falsch; fehlt={missing}, extra={extra}")

    decisions = {}
    for rid, record in records.items():
        decision = explicit_unchecked[rid] if record["status"] == "UNGEPRUEFT" else checked_decision(record)
        decision = {**decision, "id": rid, "kind": record["kind"],
                    "status_vorher": record["status"], "pair": record["pair"],
                    "node_a": record["node_a"], "node_b": record["node_b"]}
        decisions[rid] = decision

    os.makedirs(OUTDIR, exist_ok=True)
    for name in os.listdir(OUTDIR):
        if name.endswith(".md"):
            os.unlink(os.path.join(OUTDIR, name))
    for batch in idx["batches"]:
        lines = ["| ID | Beziehungsart | Richtung | Beschreibung | Beleg | Belegzitat |",
                 "|---|---|---|---|---|---|"]
        for edge in batch["edges"]:
            row = decisions[edge["id"]]
            fields = [row["id"], row["beziehungsart"], row["richtung"], row["beschreibung"],
                      row["beleg"], row["belegzitat"]]
            lines.append("| " + " | ".join(safe_cell(v) for v in fields) + " |")
        with open(os.path.join(OUTDIR, batch["batch"]), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + "\n")

    with open(DECISIONS, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"review_run": idx["review_run"], "total": len(decisions),
                   "decisions": decisions}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    counts = collections.Counter(row["beziehungsart"] for row in decisions.values())
    print(f"Entscheidungen: {len(decisions)}")
    print(f"Ergebnisdateien: {len(idx['batches'])}")
    print("Arten:")
    for art, count in sorted(counts.items()):
        print(f"  {art}: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
