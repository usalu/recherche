# -*- coding: utf-8 -*-
"""Final fail-safe audit of every current prune before user approval."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TODAY = "2026-08-13"
RESTORE = {}


def add(aid, roles, relevance, url, quote, scope="direct_enabler", **extra):
    RESTORE[aid] = dict(
        roles=roles, relevance=relevance, url=url, quote=quote, scope=scope, **extra
    )


# Only records with explicit actor/project-specific reuse evidence are restored.
# Roles are narrowed to the tasks stated in the cited passage.
add("AT:I02", ["Programmmanagement", "Reuse-Strategie"],
    "Steuert Wiens Programm für zirkuläres Bauen und die Wiederverwendung von Bauteilen.",
    "https://viecycle.wien.gv.at/documents/1555117/1742684/dtcc30-kurzbeschreibung.pdf/a5d3f629-03bc-dac2-65cf-fae951a9c704?t=1641381863187",
    "Das Programm verfolgt strategische und operative Ziele, darunter 80% Wiederverwendungsrate.")
add("CH:M01", ["Selektiver Rückbau", "Sortierung", "Bauteilhandel"],
    "Baut Bauteile schonend aus, sortiert sie und verkauft sie für eine zweite Nutzung.",
    "https://archipelsion.ch/ressourcerie/",
    "Nos équipes trient, préservent et réinjectent vos matériaux dans le circuit du réemploi.", scope="actual_reuse")
add("CH:M07", ["Demontage", "Bauteilhandel"],
    "Demontiert gebrauchte Bauteile und vermittelt sie für neue Anwendungen.",
    "https://www.bauteilverwertung.ch/",
    "Aus alt mach neu – Gebrauchte Bauteile und was daraus wieder gemacht wurde.", scope="actual_reuse")
add("CH:M09", ["Demontage", "Lagerung", "Bauteilhandel"],
    "Baut historische Bauteile aus, lagert sie und gibt sie für neue Einbauten weiter.",
    "https://www.historisches-bauteillager.ch/",
    "Wir bauen erhaltenswerte Objekte aus ... zum Wiedereinbau an einem neuen Ort.", scope="actual_reuse")
add("CH:M15", ["Demontage"],
    "Demontiert Bauteile und Baumaterial ausdrücklich für ihre Wiederverwendung.",
    "https://www.chance.ch/dienstleistungen/bauteile",
    "Wir demontieren ... Bauteile und Baumaterial für die Wiederverwendung.", scope="actual_reuse")
add("DE:U13", ["Tragwerksplanung", "Reuse-Audit", "Potenzialbewertung"],
    "Plant Tragwerke und bewertet Bestandsbauteile für Demontage und Wiedereinbau.",
    "https://circular-structural-design.eu/en/",
    "Tasks: inventory, quality assessment and element catalogue for components to be reused.")
add("DE:U14", ["Architektur", "Reuse-Beratung"],
    "Plant Reuse-Projekte und berät Bauherren zur Wiederverwendbarkeit von Bauteilen.",
    "https://www.cityfoerster.net/expertise/re_use-622-2.html",
    "We advise our builders on components and offer conception, planning and implementation services.")
add("DE:S02", ["Umweltbewertung", "Softwareentwicklung"],
    "Liefert LCA-Daten und Software-Schnittstellen für Bauteilbörsen und Reuse-Plattformen.",
    "https://www.surap.de/service/",
    "Ökobilanzdaten direkt in Ihre Bauteilbörse integrieren – für ReUse-Plattformen via API.")
add("DE:U47", ["Innenarchitektur", "Reuse-Planung", "Fertigung mit Reuse-Material"],
    "Plant und fertigt Innenausbau mit geernteten und bereits gebrauchten Bauteilen.",
    "https://www.urselmann-interior.de/zirkul%C3%A4res-handwerk",
    "ReUse first ... wiedergewonnenes Holz ... geerntete Marmorplatten.", scope="actual_reuse", status="active")
add("FI:F01", ["Angewandte Forschung"],
    "Erforscht im Department of Architecture zirkuläres Bauen und Wiederverwendung.",
    "https://www.aalto.fi/en/housing-design",
    "The research and design efforts concentrate on circular construction.")
add("FI:G01", ["Programmmanagement", "Methodenentwicklung"],
    "Entwickelt und pilotiert ein Modell für Lagerung und Wiederverwendung von Bauteilen.",
    "https://ekokumppanit.fi/projektit/sailo/",
    "SÄILÖ pilotoida toimintamalli välivarastointiin ja uudelleenkäyttöön.")
add("FI:F04", ["Pilotierung", "Angewandte Forschung"],
    "Erforscht und pilotiert Demontage und Wiederverwendung von Betonfertigteilen.",
    "https://www.tuni.fi/en/tau/research/recreate",
    "ReCreate is focused on deconstruction and reuse of precast concrete elements.", name="ReCreate / Tampere University")
add("FI:F05", ["Methodenentwicklung", "Angewandte Forschung"],
    "Entwickelt Methoden, damit Bauteile über mehrere Lebenszyklen wiederverwendet werden.",
    "https://www.vttresearch.com/en/ourservices/circularity-built-environment",
    "The built environment becomes a bank of resources designed to be reused and repurposed.",
    name="VTT – Circularity in the Built Environment")
add("NO:I01", ["Programmmanagement", "Reuse-Strategie"],
    "Steuert kommunale Wiederverwendung von Möbeln und Überschuss aus Bauprojekten.",
    "https://www.asker.kommune.no/klima-og-miljo/ombruk/",
    "Overskuddsmateriell fra bygg- og anleggsprosjekter skal brukes på nytt.", name="Asker kommune – Ombruk")
add("NO:M03", ["Lagerung", "Bauteilhandel"],
    "Lagert und verkauft gebrauchte Baustoffe für neue Bauvorhaben.",
    "https://iris-ombruksentral.no/",
    "Vi gjør det enkelt å velge brukt når du skal bygge noe nytt. Lager: Bodø.", scope="actual_reuse")
add("NO:U07", ["Demontage", "Bauteilhandel"],
    "Gewinnt gebrauchte Baustoffe aus Gebäuden und stellt sie über eine Materialbank bereit.",
    "https://www.jcs-as.no/materialbank",
    "Materialbank ... Demontering ... Bygga på lager finn du direkte og kan bestille online.", scope="actual_reuse")
add("NO:N04", ["Rücknahme", "Bauteilhandel"],
    "Nimmt gebrauchte Bauwaren und Restposten an und verkauft sie erneut.",
    "https://remiks.no/rebell/proffrebell/",
    "Brukte byggevarer og restpartier blir tilgjengelige for salg.", scope="actual_reuse", name="ProffRebell / Remiks")
add("NO:M07", ["Methodenentwicklung", "Wissenstransfer", "Netzwerkkoordination"],
    "Entwickelt Reuse-Strukturen und leitet eine nationale Wissensarena für Bauprodukte.",
    "https://www.ressurssentral.no/",
    "Aktiv utvikler ... Nasjonal kunnskapsarena for ombruk ledes av Sirkulær Ressurssentral.")
add("BE:F09", ["Demontagegerechtes Design", "Methodenentwicklung", "Angewandte Forschung"],
    "Erforscht und entwickelt reversible Lösungen zur Wiederverwendung von Bauteilen.",
    "https://www.vub.be/arch/page/circulardesign",
    "Circular design qualities enable more effective reuse of building components.")
add("BE:P2", ["Referenzprojekt"],
    "Verbaut geborgene Ziegel, Schulfliesen, Sanitärteile, Leuchten und Spiegel erneut.",
    "https://rotordb.org/en/projects/sanitary-block-itterbeek-chiro",
    "The interior is mainly made of reuse materials; bricks, tiles and sanitary appliances were recovered.",
    scope="actual_reuse", status="project", objects=["Ziegel", "Schulfliesen", "Sanitärteile", "Leuchten", "Spiegel"])
add("BE:S01", ["Materialpass", "Bauteilkataster", "Datenplattform"],
    "Registriert Bauprodukte digital und macht Wiederverwendbarkeit und Restwert sichtbar.",
    "https://madaster.be/en/platform/",
    "Create comprehensive material passports, facilitating future reuse.", name="Madaster")
add("FR:M21", ["Bauteilhandel"],
    "Verkauft geborgene Baustoffe aus dem eigenen Rückbaugeschäft zur erneuten Nutzung.",
    "https://demolition-perreault.fr/",
    "La seconde vie des matériaux ... site de vente de matériaux.", scope="actual_reuse")
add("FR:M44", ["Aufarbeitung", "Bauteilhandel", "Wiedereinbau"],
    "Birgt, restauriert, verkauft und montiert historische Bauteile für neue Projekte.",
    "https://materiauxdantan.fr/fr/",
    "Nous récupérons, restaurons et posons des éléments d'architecture anciens.", scope="actual_reuse")
add("GB:U17", ["Bauteilhandel"],
    "Kauft und verkauft überschüssigen Stahl für die erneute Nutzung in Bauprojekten.",
    "https://cleveland-steel.com/we-want-buy-steel-reuse",
    "We are steel reuse experts ... Our site is ready to take your surplus steel.", scope="actual_reuse")
add("GB:U21", ["Tragwerksplanung", "Beschaffungsplanung"],
    "Plant Tragwerke mit wiedergewonnenem Stahl und organisiert dessen Einsatz.",
    "https://www.elliottwood.co.uk/latest/180-piccadilly-londons-largest-steel-reuse-project",
    "Sourced from Cleveland Steel Stock, 4% of the steel is reclaimed and 1% is recovered.")
add("GB:U33", ["Tragwerksplanung", "Bauteilsuche", "Softwareentwicklung"],
    "Entwickelt Stockmatcher, um verfügbaren Baustahl für Wiederverwendung zuzuordnen.",
    "https://hts.uk.com/research-innovation/stockmatcher/",
    "The HTS Reused Steel Stockmatcher ... matches reused stock with a design list.")
add("GB:U58", ["Reuse-Beratung", "Reuse-Planung", "Umweltbewertung"],
    "Berät Bauprojekte zu Wiederverwendung und bewertet Material- und Kohlenstoffwirkungen.",
    "https://www.tftconsultants.com/services/circular-economy",
    "We support clients ... apply circular economy principles from concept and design through construction.")
add("GB:U65", ["Projektsteuerung", "Reuse-Planung", "Bauausführung"],
    "Identifiziert Reuse-Bauteile und verbaut Ziegel, Stahl und Ausstattung erneut.",
    "https://www.willmottdixon.co.uk/now-or-never/case-studies/tower-bridge-court-sets-standard-for-reuse-of-building-materials",
    "We repurposed bricks, handrails, fixtures and incorporated reclaimed steel.", scope="actual_reuse")
add("NL:F04", ["Methodenentwicklung", "Angewandte Forschung"],
    "Entwickelt und erprobt Methoden für Wiederverwendung und zirkuläre Bautechnologien.",
    "https://surd.nl/",
    "Circular Building Technologies – ontwikkelen wij nieuwe kennis en oplossingen.", name="SURD Research Centre / Zuyd")
add("NL:M01", ["Materialberatung", "Bauteilhandel"],
    "Berät zu zirkulären Innenräumen und bietet Urban-Mining-Materialien an.",
    "https://www.baars-bloemhoff.nl/new-horizon-interieurmaterialen-uit-urban-mining-cms-newhorizon-materialen-urbanmining",
    "Onze specialisten helpen met materiaalwensen; aanbod interieurmaterialen uit Urban Mining.", scope="actual_reuse")
add("NL:P12", ["Referenzprojekt"],
    "Nutzt Bauteile aus bestehenden Wohnblöcken für neue Häuser und Teilwiederaufbau.",
    "https://www.superlocal.eu/superlocal/",
    "Het Expogebouw bestaat voor 95% uit materialen uit een flat; aluminium, radiatoren en kozijnen zijn hergebruikt.",
    scope="actual_reuse", status="project", objects=["Bauteile aus Wohnhochhäusern", "Wohnungsmodule"])
add("NL:U23", ["Beschaffungsplanung"],
    "Prüft verfügbare zirkuläre Materialien früh und plant ihren Einsatz im Projekt.",
    "https://dwtgroep.nl/innovatie/circulair",
    "Bij projecten kijken we in het voorontwerp naar beschikbare materialen en zetten deze in.")
add("NL:U32", ["Tragwerksplanung", "Demontagegerechtes Design", "Normung"],
    "Plant Reuse-Tragwerke, lösbare Verbindungen und wirkt an der NTA 8713 mit.",
    "https://imdbv.nl/expertises",
    "Het donorskelet is circulaire werkelijkheid; IMd werkte mee aan NTA 8713.")
add("NL:U36", ["Projektentwicklung"],
    "Entwickelt Projekte zur hochwertigen Wiederverwendung geborgener Bauteile.",
    "https://lcp-circulair.nl/",
    "cepezedprojects en Lagemaat bundelen innovatieve projectontwikkeling en hoogwaardig hergebruik.")
add("NL:U38", ["Reuse-Beratung", "Bauteilinventarisierung", "Wertermittlung"],
    "Scannt Gebäude und bewertet Bauteile und Materialwerte für Wiederverwendung.",
    "https://newhorizon.nl/",
    "We scannen verborgen materialen, berekenen de waarde en adviseren tijdens de oogst.")
add("NL:U43", ["Wissensvermittlung"],
    "Vermittelt praxiserprobtes Wissen zum Entwerfen mit wiederverwendeten Bauteilen.",
    "https://ptsa.nl/reuse-to-reduce/",
    "Het boek Reuse to Reduce geeft concrete voorbeelden en benut hergebruik van materialen.")
add("NL:U48", ["Bauteilhandel"],
    "Verkauft gebrauchte Fenster, Beschläge und Holzprodukte als Urban-Mining-Materialien.",
    "https://www.stiho.nl/duurzaamheid/circulair",
    "Stiho verkoopt materialen uit slooppanden onder het label Urban Mining.", scope="actual_reuse", status="active", name="Stiho")
add("NL:X01", ["Reuse-Beratung", "Bauteilinventarisierung", "Vermittlungsplattform"],
    "Scannt Bestandsgebäude und vermittelt wiederverwendbare Bauprodukte in neue Projekte.",
    "https://repurpose.nl/",
    "We scannen gebouwen op hergebruikkansen; Madopt is de vraaggestuurde Bouwmarktplaats.")
add("SE:U02", ["Gebäudeeigentum"],
    "Stellt ein eigenes Rückbaugebäude als großmaßstäblichen Reuse-Demonstrator bereit.",
    "https://www.akademiskahus.se/om-oss/aktuellt/Nyheter/2023/december/samverkan-for-aterbruk-av-lastbarande-konstruktionsdelar/",
    "Teknikhöjden ... ägs av Akademiska Hus och blir nu ett demonterings- och innovationsprojekt.")
add("SE:U03", ["Umweltbewertung", "Datenanalyse", "Methodenentwicklung"],
    "Entwickelt ein Klimamodell für inventarisierte, wiederverwendete Bauprodukte.",
    "https://www.anthesisgroup.com/se/referensprojekt/aterbruk-i-byggsektorn/",
    "Anthesis utvecklade en Excelbaserad modell för återbrukade byggprodukter.")
add("SE:U09", ["Demontage", "Anpassung", "Wiedereinbau"],
    "Demontiert, passt Hohlplatten an und montiert sie in einem neuen Gebäude erneut.",
    "https://www.precastcontiga.heidelbergmaterials.se/sv/contiga-deltar-i-innovationsprojekt-for-aterbruk-av-tunga-byggnadsdelar",
    "Vi har fått i uppdrag att demontera, anpassa och återmontera håldäcken och takplåten.", scope="actual_reuse")
add("SE:U11", ["Gebäudeeigentum", "Pilotierung"],
    "Erprobt den Ausbau und Wiedereinbau gebrauchter Betontragteile im ReCreate-Pilot.",
    "https://helsingborgshem.se/artikel/vart-miljoarbete",
    "Vi demonterade betongelement ... de ska testas och återbrukas inom EU-projektet ReCreate.", scope="actual_reuse")
add("SE:U22", ["Demontage", "Zwischenlagerung", "Transport"],
    "Demontiert, lagert und liefert gebrauchte Baustoffe für neue Bauprojekte.",
    "https://www.wiklunds.se/affarsomraden/cirkulart-byggande/",
    "Inventering, Demontering, Rekonditionering, Mellanlager, Leverans av återbrukat material.", scope="actual_reuse")


def confirm_code(rec):
    codes = " ".join(rec.get("reason_codes") or []).lower()
    if "histor" in codes or "closed" in codes:
        return "confirmed_historical_or_closed"
    if "future" in codes:
        return "confirmed_future_or_design_only"
    if "entity" in codes or "mismatch" in codes:
        return "confirmed_identity_or_entity_unresolved"
    if "partner" in codes or "credit" in codes:
        return "confirmed_partner_credit_or_generic_only"
    if "no_direct" in codes:
        return "confirmed_no_direct_reuse_role"
    return "confirmed_no_concrete_reuse_evidence"


def main():
    lanes, records = {}, []
    for lane in "ABC":
        lanes[lane] = json.loads((HERE / f"lane_{lane}.json").read_text(encoding="utf-8"))
        records.extend(lanes[lane]["records"])
    if len(records) != 859 or len({r["eid"] for r in records}) != 859:
        raise SystemExit("Expected 859 unique records")
    by_id = {r["audit_id"]: r for r in records}
    if set(RESTORE) - set(by_id):
        raise SystemExit(f"Unknown restore IDs: {sorted(set(RESTORE) - set(by_id))}")

    snapshot = HERE / "pre_final_delete_audit_lanes.json"
    if not snapshot.exists():
        snapshot.write_text(json.dumps(lanes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pre_audit_lanes = json.loads(snapshot.read_text(encoding="utf-8"))
    current_prunes = [
        r for lane in "ABC" for r in pre_audit_lanes[lane]["records"]
        if r["decision"] == "prune"
    ]
    if len(current_prunes) != 269:
        raise SystemExit(f"Expected 269 pre-audit prunes, got {len(current_prunes)}")

    audit = []
    for rec in current_prunes:
        aid = rec["audit_id"]
        item = dict(eid=rec["eid"], audit_id=aid,
                    name=rec.get("corrected_name") or rec["current_name"],
                    decision_before="prune", previous_reason_codes=rec.get("reason_codes") or [])
        cfg = RESTORE.get(aid)
        if not cfg:
            item.update(final_check="confirm_prune", final_reason_code=confirm_code(rec),
                        rationale="No actor-specific, concrete and role-bearing reuse evidence survived the final gate.")
            audit.append(item)
            continue
        evidence = [{"url": cfg["url"], "quote": cfg["quote"],
                     "supports_roles": list(cfg["roles"]), "accessed_at": TODAY}]
        target = by_id[aid]
        target.update(decision="keep", merge_target_eid=None,
                   reason_codes=["final_delete_audit_direct_evidence_recovered"],
                   corrected_name=cfg.get("name", target.get("corrected_name")),
                   current_status=cfg.get("status", "active"), reuse_scope=cfg["scope"],
                   roles=cfg["roles"], relevance=cfg["relevance"],
                   reuse_objects=cfg.get("objects", []), evidence=evidence,
                   verified_by="root-final-delete-audit", review_status="cross_review_complete")
        item.update(final_check="restore_keep",
                    final_reason_code="direct_actor_specific_reuse_evidence",
                    rationale="The source explicitly documents the actor's own reuse activity or enabling task.",
                    final_roles=cfg["roles"], evidence_urls=[cfg["url"]])
        audit.append(item)

    for lane, data in lanes.items():
        (HERE / f"lane_{lane}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = Counter(r["decision"] for r in records)
    country = defaultdict(Counter)
    for rec in records:
        cc = rec.get("corrected_country") or rec["audit_id"].split(":", 1)[0]
        country[cc][rec["decision"]] += 1
    result = {
        "schema_version": 1, "reviewer": "root-final-delete-audit",
        "policy": "research-only; direct actor/project evidence; conservative prune",
        "pre_audit_prunes": 269,
        "restored": sum(a["final_check"] == "restore_keep" for a in audit),
        "confirmed_prunes": sum(a["final_check"] == "confirm_prune" for a in audit),
        "final_decisions": dict(counts),
        "countries": {cc: dict(c) for cc, c in sorted(country.items())}, "audit": audit,
    }
    (HERE / "final_delete_audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    restored = [a for a in audit if a["final_check"] == "restore_keep"]
    confirmed = [a for a in audit if a["final_check"] == "confirm_prune"]
    reason_counts = Counter(a["final_reason_code"] for a in confirmed)
    lines = ["# Finaler Lösch-Audit", "", "**Status: vollständig geprüft, noch nicht für Semio aktiviert.**", "",
             f"- Vorherige Löschkandidaten: {len(current_prunes)}",
             f"- Falsche Löschungen korrigiert: {len(restored)}",
             f"- Löschungen bestätigt: {len(confirmed)}",
             f"- Final: {counts['keep']} behalten, {counts['prune']} entfernen, {counts['merge']} zusammenführen", "",
             "## Wiederhergestellt", "", "| ID | Name | Rolle(n) |", "|---|---|---|"]
    for a in sorted(restored, key=lambda x: x["audit_id"]):
        rec = by_id[a["audit_id"]]
        lines.append(f"| {a['audit_id']} | {rec.get('corrected_name') or rec['current_name']} | {' / '.join(rec['roles'])} |")
    lines += ["", "## Bestätigte Löschgründe", "", "| Grund | Anzahl |", "|---|---:|"]
    for code, n in sorted(reason_counts.items()):
        lines.append(f"| {code} | {n} |")
    lines += ["", "Die Einzelprüfung aller 269 früheren Löschkandidaten steht in `final_delete_audit.json`.", ""]
    (HERE / "FINAL_DELETE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"restored": len(restored), "confirmed_prunes": len(confirmed), "final": dict(counts)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
