---
id: "Design_for_Disassembly"
entity: "methode"
node_kind: "knot"
migration_status: "migrated_phase2_semantic_corrections"
migration_action: "semantic_split"
title: "Design for Disassembly"
legacy_type: "Tragwerkssystem"
legacy_paths:
  - "tragwerkssystem\Design_for_Disassembly.md"
target_primary: "methode/Design_for_Disassembly"
target_roles: "phase2_secondary"
risk_flags: "old_type_tragwerkssystem_overgeneralized"
---
# Design for Disassembly

## Migration

- Target: methode/Design_for_Disassembly
- Legacy source count: 1
- Legacy types: Tragwerkssystem
- Migration actions: semantic_split
- Target roles: phase2_secondary
- Risk flags: old_type_tragwerkssystem_overgeneralized

## Legacy Content: tragwerkssystem\Design_for_Disassembly.md

---
type: Tragwerkssystem
verwandt: ["[[tragwerkssystem/Betonfertigteil_System]]", "[[tragwerkssystem/Holz_Skelettbau]]", "[[tragwerkssystem/Reversible_Fuegung]]", "[[tragwerkssystem/Skelettbauweise]]", "[[tragwerkssystem/Stahl_Skelettbau]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** Tragwerkssysteme; zirkuläres Bauen; Entwerfen mit Bestand; Kreislaufwirtschaft; Materialpass; Open Building; Lebenszyklusplanung.
- **Verwandte Dateien:** `tragwerkssystem/Reversible_Fuegung.md`; `tragwerkssystem/Skelettbauweise.md`; `tragwerkssystem/Stahl_Skelettbau.md`; `tragwerkssystem/Holz_Skelettbau.md`; `tragwerkssystem/Betonfertigteil_System.md`; `bauteil/Alle_Bauteile.md`; `verbindung/Verbindungsmittel.md`; `pruefung/Bauteilpass.md`; `reuse_strategie/Design_for_Reuse.md`; `reuse_strategie/Bauteilernte.md`; `projekt/BAMB.md`; `projekt/FCRBE.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** ISO 20887:2020; BAMB; FCRBE; EU Level(s); DGNB-Zirkularitätsindex; Gebäuderessourcenpass; Materialpass; BIM; Bauteilkataster; Rückbaukonzept; reversible Verbindungstechnik; Schichtenmodell nach Lebensdauer; Circular Economy Action Plan; Construction Products Regulation (EU) 2024/3110.

## Kurzdefinition

Design for Disassembly (DfD) bezeichnet die Planung von Gebäuden, Tragwerken, Bauteilen und Verbindungen so, dass sie am Ende einer Nutzungsphase zerstörungsarm demontiert, geprüft, repariert, angepasst und wiederverwendet werden können. Design for Disassembly ist kein einzelnes Detail, sondern eine Systemlogik aus reversiblen Fügungen, zugänglichen Verbindungspunkten, getrennten Materialschichten, standardisierten Bauteilen, dokumentierten Eigenschaften und vorausschauender Rückbauplanung.

## Relevanz für Wiederverwendung im Bauwesen

- **Voraussetzung für zukünftige Bauteilwiederverwendung:** Ohne DfD werden viele Bauteile beim Rückbau beschädigt, vermischt oder rechtlich/technisch nicht mehr nachweisbar.
- **Wertsteigerung der Materialbank Gebäude:** Gebäude werden nicht nur als Nutzobjekte, sondern als temporäre Lager hochwertiger Bauteile verstanden.
- **Adaptionsfähigkeit während der Nutzung:** DfD erleichtert Umbau, Reparatur, Austausch und Umnutzung. Wiederverwendung beginnt damit oft schon im Gebäude selbst, nicht erst nach Abriss.
- **Reduktion von Downcycling:** Sortenreine Trennung und zerstörungsarme Demontage erhöhen die Chance auf gleichwertige Wiederverwendung statt Recycling oder Entsorgung.
- **Planungsdisziplin über Gewerke hinweg:** Tragwerk, Ausbau, Fassade, Haustechnik, Brandschutz und Bauphysik müssen gemeinsam rückbaubar gedacht werden.

## Fachinhalt

### Grundprinzipien

- **Reversibilität:** Verbindungen können gelöst werden, ohne die Hauptbauteile wesentlich zu zerstören.
- **Zugänglichkeit:** Verbindungsmittel, Knoten und Installationen bleiben auffindbar und erreichbar; Wartungs- und Rückbauöffnungen sind eingeplant.
- **Trennbarkeit:** Tragwerk, Fassade, Ausbau, Haustechnik, Dämmung und Abdichtung werden nach Material, Funktion und Lebensdauer getrennt.
- **Standardisierung und Modularität:** Wiederkehrende Raster, Querschnitte, Verbindungsmittel und Bauteilgrößen erhöhen die Wahrscheinlichkeit einer zweiten Nutzung.
- **Einfachheit:** Wenige, robuste Verbindungstypen und klare Lastpfade sind rückbau- und prüffreundlicher als hochgradig optimierte Sonderlösungen.
- **Dokumentation:** Materialpass, Bauteilnummern, Prüfzeugnisse, Einbauorte, Verbindungsmittel, Wartungshistorie und Rückbauanleitungen bleiben digital und analog verfügbar.
- **Sicherer Rückbau:** Die Montagefolge ist grundsätzlich umkehrbar; temporäre Aussteifungen, Hebepunkte, Lastfälle und Demontagezustände sind mitgeplant.

### Entwurfsregeln für Tragwerkssysteme

- Primärtragwerk langlebig, nutzungsneutral und gut zugänglich planen.
- Sekundärstruktur, Fassade und Ausbau austauschbar und mit kürzerer Lebensdauer entkoppeln.
- Verbundwirkungen nur dort einsetzen, wo sie rückbaubar oder als bewusster Zielkonflikt dokumentiert sind.
- Raster und Spannweiten so wählen, dass Bauteile in unterschiedlichen Gebäuden wieder nutzbar bleiben.
- Übermäßige Spezialisierung vermeiden: Sonderformen, extreme Zuschnitte und objektspezifische Knoten reduzieren ReUse-Marktchancen.
- Verbindungsmittel möglichst sichtbar, lösbar, korrosionsgeschützt und normnah wählen.
- Schichten mit ähnlicher Lebensdauer koppeln; Schichten mit unterschiedlicher Lebensdauer entkoppeln.
- Bauteile mit ausreichenden Hebe-, Transport- und Lageroptionen planen.

### DfD auf Systemebene

- **Gebäudeebene:** flexible Grundrisse, ausreichend Geschosshöhe, Tragwerk/Fassade/Innenausbau getrennt, Nutzungsänderungen eingeplant.
- **Systemebene:** austauschbare Deckenfelder, Fassadenelemente, Module, Stützen-/Trägerachsen, Technikzonen.
- **Bauteilebene:** identifizierbare Elemente mit bekannten Material- und Leistungsdaten.
- **Verbindungsebene:** lösbare Knoten mit klarer Lastabtragung und geringem Beschädigungsrisiko.
- **Informationsebene:** Bauteilpass, Wartungsplan, Rückbauanleitung, digitale Produktdaten, Fotodokumentation, As-built-Modell.

### Bewertungskriterien

- Lösbarkeit der Verbindung ohne Zerstörung des Hauptbauteils.
- Anzahl und Zugänglichkeit der Verbindungsmittel.
- Sortenreinheit und Schadstofffreiheit.
- Standardisierungsgrad und Wiederverwendungsmarkt.
- Robustheit gegenüber Umbauten, Reparaturen und Nutzungsänderungen.
- Verfügbarkeit von Leistungsnachweisen und Prüfverfahren.
- Ökobilanz: Zusatzmaterial für Reversibilität darf den zukünftigen Nutzen nicht unverhältnismäßig übersteigen.

## Praxisbezug / Beispiele

- **BAMB:** Das Projekt hat Materialpässe und reversible Gebäudedesign-Ansätze als Instrumente für Gebäude als Materialbanken entwickelt.
- **FCRBE:** Das ReUse Toolkit zeigt, dass Wiederverwendung nicht nur aus Entwurfsdetails besteht, sondern aus Beschaffung, Spezifikation, Prüfung, Lagerung, Rückbau und rechtlicher Zuordnung.
- **Stahlhallen:** Geschraubte Stahlrahmen mit standardisierten Profilen und klarer Dokumentation können als ganze Struktur, als Teilrahmen oder als Einzelprofile wiederverwendet werden.
- **Holzmodulbau:** Module mit lösbaren Transport- und Anschlussknoten, getrennten Installationen und dokumentierten Bauteilen können an anderer Stelle erneut eingesetzt werden.
- **Fassaden- und Ausbaukomponenten:** Obwohl diese Datei Tragwerkssysteme fokussiert, zeigt der Ausbau oft die DfD-Probleme besonders deutlich: verklebte Schichten, Mischmaterialien und verdeckte Befestigungen verhindern hochwertige Wiederverwendung.

## Herausforderungen / offene Fragen

- **Zielkonflikte mit Bauphysik:** Luftdichtheit, Schallschutz, Feuchteschutz und Brandschutz werden häufig über Schichten, Verklebungen, Verguss und Bekleidungen hergestellt, die Demontierbarkeit erschweren.
- **Kosten und Verantwortlichkeiten:** DfD-Nutzen entsteht oft in der Zukunft, Kosten aber heute. Ohne Geschäftsmodelle, Restwertlogik oder Rücknahmeverträge bleibt DfD schwer durchsetzbar.
- **Normen und Zulassung:** Für neue Bauprodukte sind Nachweiswege etabliert; für wiederverwendete Bauteile sind Re-Qualifizierung, Leistungserklärung und Haftung häufig projektspezifisch.
- **Dokumentationsverlust:** Materialpässe nützen nur, wenn sie über Jahrzehnte gepflegt, zugänglich und rechtlich verwendbar bleiben.
- **Überdimensionierung:** Nutzungsneutrale und wiederverwendbare Bauteile können mehr Material benötigen. Dieser Mehraufwand muss über längere Nutzung, Anpassbarkeit und ReUse plausibel kompensiert werden.
- **Marktunsicherheit:** Wiederverwendung setzt Nachfrage, Lager, Standardmaße, Prüfstellen, Gewährleistung und Beschaffungsprozesse voraus. DfD allein schafft diesen Markt nicht, reduziert aber zukünftige Barrieren.

## Quellen

- ISO 20887:2020: *Sustainability in buildings and civil engineering works — Design for disassembly and adaptability — Principles, requirements and guidance*. https://www.iso.org/standard/69370.html
- ISO: *Tearing down the carbon footprint of buildings with new International Standard*, 2020. https://www.iso.org/news/ref2480.html
- BAMB: *Buildings as Material Banks*. https://www.bamb2020.eu/
- BAMB: *Materials Passports*. https://www.bamb2020.eu/topics/materials-passports/
- European Commission: *Level(s) — European framework for sustainable buildings*. https://green-forum.ec.europa.eu/green-business/levels_en
- FCRBE / Rotor: *Reuse Toolkit: material sheets*. https://rotordb.org/en/projects/reuse-toolkit-material-sheets
- European Commission: *EU Construction & Demolition Waste Management Protocol including guidelines for pre-demolition and pre-renovation audits of construction works*, 2024. https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- DGNB: *Circular building in the DGNB System*. https://www.dgnb.de/en/sustainable-building/circular-building/toolbox/circular-building-in-the-dgnb-system
- Regulation (EU) 2024/3110: *Construction Products Regulation*. https://eur-lex.europa.eu/eli/reg/2024/3110/oj/eng

