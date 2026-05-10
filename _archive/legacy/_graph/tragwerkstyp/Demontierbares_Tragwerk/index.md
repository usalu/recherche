---
id: "Demontierbares_Tragwerk"
entity: "tragwerkstyp"
node_kind: "knot"
migration_status: "migrated_phase2_semantic_corrections"
migration_action: "semantic_split"
title: "Demontierbares Tragwerk"
legacy_type: "Tragwerkssystem"
legacy_paths:
  - "tragwerkssystem\Design_for_Disassembly.md"
  - "tragwerkssystem\Reversible_Fuegung.md"
target_primary: "tragwerkstyp/Demontierbares_Tragwerk"
target_roles: "phase2_secondary"
risk_flags: "old_type_tragwerkssystem_overgeneralized"
---
# Demontierbares Tragwerk

## Migration

- Target: tragwerkstyp/Demontierbares_Tragwerk
- Legacy source count: 2
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

## Legacy Content: tragwerkssystem\Reversible_Fuegung.md

---
type: Tragwerkssystem
verbindung: ["[[verbindung/Klemmverbindung]]"]
verwandt: ["[[tragwerkssystem/Aufstockung_in_Holzbauweise]]", "[[tragwerkssystem/Betonfertigteil_System]]", "[[tragwerkssystem/Dachtragwerk_und_Fachwerk]]", "[[tragwerkssystem/Design_for_Disassembly]]", "[[tragwerkssystem/Holz_Skelettbau]]", "[[tragwerkssystem/Skelettbauweise]]", "[[tragwerkssystem/Stahl_Skelettbau]]", "[[tragwerkssystem/Tragende_Wand]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** Tragwerkssysteme; Design for Disassembly; Verbindungstechnik; Rückbauplanung; Bauteilwiederverwendung; Reparaturfähigkeit.
- **Verwandte Dateien:** `tragwerkssystem/Design_for_Disassembly.md`; `tragwerkssystem/Skelettbauweise.md`; `tragwerkssystem/Stahl_Skelettbau.md`; `tragwerkssystem/Holz_Skelettbau.md`; `tragwerkssystem/Betonfertigteil_System.md`; `verbindung/Schraubverbindung.md`; `verbindung/Bolzenverbindung.md`; `verbindung/Klemmverbindung.md`; `verbindung/Schweissverbindung.md`; `pruefung/Verbindungspruefung.md`; `reuse_strategie/Reparatur.md`; `reuse_strategie/Bauteilpass.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Tragwerksplanung; Produkthersteller; Holzbau, Stahlbau, Fertigteilbau; ISO 20887; BAMB Reversible Building Design; FCRBE; SCI P427; PROGRESS; BIM/Materialpass; Schraub-, Bolzen-, Steck-, Klemm- und Spannsysteme; Demontageanleitung.

## Kurzdefinition

Reversible Fügung ist ein Systemprinzip, bei dem Bauteile so verbunden werden, dass sie bei Wartung, Umbau oder Rückbau mit vertretbarem Aufwand gelöst werden können, ohne die Hauptbauteile wesentlich zu zerstören oder ihre Wiederverwendbarkeit zu verlieren. Reversibilität bedeutet nicht zwingend werkzeuglos, sondern kontrolliert lösbar, zugänglich, dokumentiert und mit beherrschbarem Schaden an austauschbaren Verbindungsmitteln.

## Relevanz für Wiederverwendung im Bauwesen

- **Direkter Hebel für ReUse:** Die Wiederverwendung von Tragwerksbauteilen scheitert häufig nicht am Material, sondern an irreversiblen oder unzugänglichen Verbindungen.
- **Reparatur und Austausch:** Reversible Fügungen ermöglichen Austausch einzelner Bauteile, Verlängerung der Nutzungsdauer und Anpassung an neue Nutzungen.
- **Sortenreinheit:** Lösbare Verbindungen trennen Stahl, Holz, Beton, Dämmung, Abdichtung und Ausbau besser als Verklebung, Verguss oder Verbund.
- **Wert der Verbindungsebene:** Verbindungsmittel sind oft klein im Materialanteil, aber entscheidend für den Restwert des gesamten Bauteilsystems.
- **System statt Detail:** Eine Verbindung ist nur dann reversibel, wenn auch Zugang, Montagefolge, Lastumlagerung, Brandschutz, Abdichtung und Dokumentation darauf abgestimmt sind.

## Fachinhalt

### Grundanforderungen

- **Lösbarkeit:** Verbindung kann mit üblichen Werkzeugen getrennt werden; Verbindungsmittel sind nicht dauerhaft verklebt, vergossen oder verdeckt.
- **Zugänglichkeit:** Schraubenköpfe, Muttern, Bolzen, Klemmen, Spannanker und Inspektionsöffnungen bleiben erreichbar.
- **Austauschbarkeit:** Verbindungsmittel dürfen als Verschleiß- oder Opferteile gedacht sein, Hauptbauteile sollen möglichst unbeschädigt bleiben.
- **Dokumentation:** Lage, Typ, Anzugsmoment, Material, Korrosionsschutz, Rückbaureihenfolge und Sicherheitszustände sind erfasst.
- **Robustheit:** Die Verbindung erfüllt Tragfähigkeit, Gebrauchstauglichkeit, Brand-, Schall-, Feuchte- und Dauerhaftigkeitsanforderungen über die Nutzungszeit.

### Verbindungstypen

- **Stahlbau:** Schraub- und Bolzenverbindungen, Laschen, Kopfplatten, Steckknoten, Klemmplatten. Geschweißte Knoten sind nur eingeschränkt reversibel; sie können durch Trennen wiederverwendbare Stäbe liefern, verlieren aber System- und Knotenwert.
- **Holzbau:** Schrauben, Bolzen, Stabdübel, außenliegende oder eingeschlitzte Stahlbleche, Auflagerkonsolen, Steckverbinder. Verklebte Anschlüsse und flächige Verbundschichten sind kritisch.
- **Betonfertigteilbau:** Auflager mit lösbaren Sicherungen, mechanische Kopplungen, Schraub-/Bolzenverbindungen über Einbauteile. Vergussfugen, Ortbetonergänzungen und Nassknoten sind nur begrenzt reversibel.
- **Fassade und Ausbau:** Clips, Schienensysteme, mechanische Halterungen, lösbare Dichtprofile, modulare Unterkonstruktionen. Verklebte Fassaden, Spachtelschichten und Verbundplatten erschweren ReUse.
- **Haustechnik:** Steckbare Leitungsführungen, zugängliche Schächte, demontierbare Trassen, lösbare Brandschotts und klare Trennung von Tragwerk und Technik.

### Entwurfsprinzipien

- Verbindungsmittel sichtbar oder auffindbar halten; verdeckte Verbindungen nur mit dauerhaftem Ortungsplan.
- Wartungs- und Rückbauzugang unabhängig von späterem Ausbau sichern.
- Korrosionsschutz und Feuchteschutz so planen, dass Verbindung auch nach Jahrzehnten lösbar bleibt.
- Toleranzen und Justierbarkeit integrieren; ReUse-Bauteile haben oft größere Maßabweichungen als Neuprodukte.
- Verbindungsmittel standardisieren; Sonderteile nur mit Ersatzteil- oder Nachfertigungsstrategie.
- Knoten nicht überfrachten: Tragwerk, Fassade, Abdichtung, Brandschutz und Installationen möglichst nicht in einem unlösbaren Detail verschmelzen.
- Demontagezustände statisch nachweisen: Beim Lösen einer Verbindung können temporäre Lastfälle kritischer sein als der Endzustand.

### Bewertungsfragen

- Kann die Verbindung gelöst werden, ohne Hauptbauteile zu schneiden, zu brechen oder stark zu schwächen?
- Sind Verbindungsmittel nach Abschluss des Ausbaus noch zugänglich?
- Bleiben Dichtheit, Schall- und Brandschutz mit demontierbaren Zusatzschichten lösbar?
- Wie viele verschiedene Werkzeuge, Gewerke und Rückbauschritte sind nötig?
- Sind Verbindungsmittel nach Demontage wiederverwendbar oder bewusst als ersetzbare Kleinteile geplant?
- Ist die Verbindung so dokumentiert, dass eine spätere Person sie erkennt und sicher löst?

## Praxisbezug / Beispiele

- **Geschraubter Stahlrahmen:** Hohe ReUse-Fähigkeit, wenn Profile standardisiert, Schrauben zugänglich, Brandschutz demontierbar und Korrosion gering ist.
- **Holzstütze mit außenliegendem Stahlknoten:** Gut prüf- und lösbar, wenn Schrauben-/Bolzenlöcher die Wiederverwendung nicht zu stark einschränken.
- **Betonfertigteil mit Nassfuge:** Montagefreundlich und robust, aber für ReUse oft problematisch, weil die Fuge nur durch Schneiden oder Stemmen getrennt werden kann.
- **Fassade mit Klebeverbund:** Wartungsarm, aber schlechte Trennbarkeit. Eine mechanisch geklemmte Fassade kann Platten, Unterkonstruktion und Dämmung besser trennen.
- **Temporäre Bauten:** Messe-, Pavillon- und Modulbauten zeigen, dass reversible Fügung technisch alltäglich ist, wenn Demontage von Anfang an Bestandteil des Geschäftsmodells ist.

## Herausforderungen / offene Fragen

- **Performancekonflikte:** Brandwiderstand, Schallschutz, Luftdichtheit, Wasserdichtheit und Tragfähigkeit werden oft mit nicht reversiblen Schichten hergestellt.
- **Dauerhaft lösbar:** Eine heute lösbare Schraube kann nach Jahrzehnten durch Korrosion, Beschichtung, Verformung oder Verschmutzung praktisch unlösbar sein.
- **Inspektion:** Reversible Fügungen benötigen Zugang und Kontrolle. Verdeckte, hoch belastete Knoten können ohne Monitoring Risiken erzeugen.
- **Kosten und Ästhetik:** Sichtbare oder zugängliche Knoten können gestalterisch und wirtschaftlich herausfordernd sein.
- **Normative Lücken:** Reversible Verbindungen für wiederverwendete Bauteile sind oft projektspezifisch nachzuweisen; standardisierte Zulassungs- und Haftungswege fehlen teilweise.
- **Übertragbarkeit:** Eine Verbindung kann in einem System reversibel sein, in einem anderen aber durch angrenzende Schichten unlösbar werden. Deshalb muss Reversibilität als Systemmerkmal bewertet werden.

## Quellen

- ISO 20887:2020: *Design for disassembly and adaptability*. https://www.iso.org/standard/69370.html
- BAMB: *Buildings as Material Banks* und *Reversible Building Design*. https://www.bamb2020.eu/
- BAMB: *Materials Passports*. https://www.bamb2020.eu/topics/materials-passports/
- Ottenhaus, L.-M. et al.: *Design for adaptability, disassembly and reuse – A review of reversible timber connection systems*, Construction and Building Materials, 2023.
- PROGRESS / ECCS: *European Recommendations for Reuse of Steel Products in Single-Storey Buildings*, 2020. https://www.steelconstruct.com/wp-content/uploads/PROGRESS_Design_guide_final-version.pdf
- Steel Construction Institute: *P427 Structural steel reuse: assessment, testing and design principles*. https://steel-sci.com/assets/downloads/steel-reuse-protocol-v06.pdf
- FCRBE / Rotor: *Reuse Toolkit: material sheets*. https://rotordb.org/en/projects/reuse-toolkit-material-sheets
- European Commission: *EU Construction & Demolition Waste Management Protocol*, 2024. https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en

