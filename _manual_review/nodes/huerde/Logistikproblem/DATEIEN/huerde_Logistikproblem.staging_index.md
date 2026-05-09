---
id: "Logistikproblem"
entity: "huerde"
node_kind: "knot"
migration_status: "migrated_phase1_stable_knots"
migration_action: "move_as_knot"
title: "Logistikproblem"
legacy_type: "Hürde"
legacy_paths:
  - "huerde\Logistikproblem.md"
target_primary: "huerde/Logistikproblem"
target_secondary: ""
risk_flags: ""
---
# Logistikproblem

## Migration

- Target: huerde/Logistikproblem
- Legacy source count: 1
- Legacy types: Hürde
- Migration actions: move_as_knot
- Secondary targets: 
- Risk flags: 

## Legacy Content: huerde\Logistikproblem.md

---
type: Hürde
logistik: ["[[logistik/Lagerung]]", "[[logistik/Transport]]"]
verwandt: ["[[huerde/Ausschreibungsproblem]]", "[[huerde/Datenluecke]]", "[[huerde/Fehlende_Lagerflaeche]]"]
---

## Verknüpfungen

**Übergeordnete Themen**
- Hürden / Technisch und organisatorisch
- Logistik / Rückbau, Transport, Sortierung, Lagerung, Lieferung, Baustellensteuerung
- Wirtschaft / Prozesskosten, Terminrisiko, Koordination, Skaleneffekte
- Datenmodell / Tracking, Verfügbarkeit, Lagerstatus, Bauteil-ID
- Recht / Abfallstatus, Eigentum, Transport, Arbeitsschutz, Haftung
- Standard / DIN SPEC 91484, FCRBE-Audit, Materialpässe, digitale Produktpässe

**Verwandte Dateien**
- `logistik/Rueckbauplanung.md`
- `logistik/Transport.md`
- `logistik/Lagerung.md`
- `logistik/Zwischenlager.md`
- `logistik/Baustellenlogistik.md`
- `logistik/Bauteiltracking.md`
- `huerde/Fehlende_Lagerflaeche.md`
- `huerde/Datenluecke.md`
- `huerde/Ausschreibungsproblem.md`
- `wirtschaft/Prozesskosten.md`
- `recht/Abfallrecht.md`
- `datenmodell/Bauteilpass.md`

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- Akteure: Rückbauunternehmen, Logistikunternehmen, Materialbroker, Bauteilbörsen, Re-Use-Hubs, Bauherrschaften, Projektsteuerung, Planende, Prüfstellen, Lagerbetreiber, ausführende Unternehmen.
- Fallstudien / Ansätze: FCRBE Reuse Toolkit; Re-Use-Hubs wie Ombygg und Rotor DC; Bauteilbörsen; projektinterne Urban-Mining-Ketten; direkte donor-to-recipient-Projektkopplung.
- Materialien: große und schwere Bauteile wie Stahlträger, Holzträger, Naturstein, Fassadenelemente; empfindliche Bauteile wie Fenster, Türen, Leuchten, TGA-Geräte; kleinteilige Bauteile wie Beschläge, Fliesen, Sanitärobjekte.
- Methoden: selektiver Rückbau, Rückbauinventur, Demontagesequenz, Verpackungskonzept, Transportgestelle, Bauteil-ID, Konsolidierungslager, Reservierung, Lieferfensterplanung, Qualitätssicherung, Rückverfolgbarkeit.

## Kurzdefinition

Das Logistikproblem bezeichnet die Barriere, dass Wiederverwendung im Bauwesen eine komplexe, rückwärts gerichtete und zeitkritische Materialkette benötigt, die im konventionellen Bauprozess kaum vorgesehen ist. Bauteile müssen nicht nur gekauft und geliefert, sondern aus einem bestehenden Gebäude identifiziert, zerstörungsarm ausgebaut, sortiert, geprüft, dokumentiert, verpackt, transportiert, zwischengelagert, reserviert, angepasst und termingerecht wieder eingebaut werden.

Das Problem liegt in der Synchronisierung von Angebot und Nachfrage: Rückbau produziert Bauteile aus einem konkreten Bestand; Bauprojekte benötigen Bauteile mit bestimmten Anforderungen zu einem bestimmten Zeitpunkt. Die beiden Seiten passen selten ohne Koordination zusammen.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung macht den Bauprozess zirkulär, aber dadurch auch logistisch anspruchsvoller. Neue Bauprodukte kommen aus etablierten Lieferketten mit Katalog, Verpackung, Lieferzeit, Gewährleistung und Ersatzteilen. Wiederverwendete Bauteile kommen aus heterogenen Rückbauquellen. Sie sind oft einmalig, schwer planbar und abhängig von Demontageerfolg, Prüfung und Lagerung.

Das Logistikproblem entscheidet in der Praxis über Machbarkeit. Ein Bauteil kann ökologisch sinnvoll, technisch geeignet und wirtschaftlich günstig sein; wenn es aber nicht rechtzeitig, unbeschädigt, dokumentiert und passend geliefert werden kann, wird es nicht eingesetzt. Logistik ist deshalb nicht nachgelagerter Transport, sondern Kernbestandteil des Entwerfens mit Bestand.

Besonders stark wirkt die Hürde bei:
- engen Baustellen ohne Pufferflächen,
- kurzen Rückbaufristen,
- großen oder empfindlichen Bauteilen,
- Bauteilen mit Prüfbedarf,
- öffentlichen Projekten mit langen Vergabezeiten,
- fehlender regionaler Re-Use-Infrastruktur,
- unsicherer Nachfrage nach spezifischen Beständen.

## Fachinhalt

### 1. Unterschied zur Neuproduktlogistik

Neuproduktlogistik basiert auf industrieller Standardisierung. Produkte sind reproduzierbar, verpackt, katalogisiert, lieferbar und mit Herstellerinformationen versehen. Re-Use-Logistik basiert auf Bestandsverfügbarkeit. Jedes Bauteil muss als konkretes Objekt behandelt werden.

Wichtige Unterschiede:

- **Quelle:** Baustelle / Bestand statt Fabrik oder Handel.
- **Menge:** begrenzte Charge statt nachbestellbare Serie.
- **Qualität:** zustandsabhängig statt fabrikneu.
- **Dokumentation:** oft rekonstruiert statt vollständig mitgeliefert.
- **Zeitpunkt:** abhängig von Rückbau statt Produktionsplanung.
- **Verpackung:** muss neu entwickelt werden statt standardisiert.
- **Risiko:** Bruch, Verlust, Verwechslung, Prüfversagen.
- **Planung:** Entwurf muss sich an Verfügbarkeit anpassen.

### 2. Prozesskette der Re-Use-Logistik

**1. Identifikation:** Bauteile werden im Bestand erkannt, priorisiert und erfasst. Ohne frühe Inventur kann keine logistische Kette geplant werden.

**2. Freigabe und Eigentum:** Vor Ausbau muss geklärt sein, wer das Bauteil nutzen, verkaufen oder lagern darf. Eigentums- und Vertragsfragen beeinflussen Logistik direkt.

**3. Demontageplanung:** Ausbaufolge, Werkzeuge, Schutzmaßnahmen, Hebezeuge, Personal, Sicherheitsmaßnahmen und Bruchrisiken werden geplant. Selektiver Rückbau ist langsamer als konventioneller Abbruch.

**4. Ausbau:** Bauteile werden zerstörungsarm demontiert, markiert und gesichert. Hier entscheidet sich oft, ob Wiederverwendung real bleibt.

**5. Sortierung und Erstprüfung:** Bauteile werden nach Typ, Zustand, Maß, Schadstoffverdacht und Zielnutzung getrennt. Ungeeignete oder gefährliche Bauteile werden ausgeschieden.

**6. Dokumentation und Tracking:** Jedes Bauteil oder jede Charge erhält eine ID, Fotos, Maße, Status und Dokumente. Ohne Tracking entstehen Verwechslungen.

**7. Reinigung / Aufbereitung:** Viele Bauteile müssen gereinigt, repariert, entnagelt, entschichtet, neu verpackt oder geprüft werden.

**8. Verpackung und Transport:** Transportgestelle, Paletten, Kisten, Schutzfolien, Kantenschutz und Ladungssicherung müssen bauteilspezifisch organisiert werden.

**9. Zwischenlagerung:** Falls kein direkter Einbau möglich ist, werden Bauteile gelagert. Lagerung benötigt Flächen, Schutz, Daten und Verwaltung.

**10. Reservierung und Vermarktung:** Bauteile werden einem Projekt zugeordnet, angeboten oder verkauft. Informationen müssen aktuell bleiben.

**11. Lieferung und Baustellenintegration:** Bauteile müssen in der richtigen Reihenfolge, Menge und Qualität zum Einbauort gelangen. Ersatz- und Reservequoten sind einzuplanen.

**12. Wiedereinbau und Dokumentation:** Einbau, Abnahme, Restmengen und neue Position im Gebäude werden dokumentiert, damit der nächste Lebenszyklus vorbereitet ist.

### 3. Typische Engpässe

**Zeitfenster:** Rückbaufristen sind kurz. Wenn Bauteile nicht schnell gesichert werden, gehen sie in Entsorgung oder Recycling. Gleichzeitig sind Abnehmerprojekte oft noch nicht bereit.

**Mengen- und Qualitätsunsicherheit:** Vor Ausbau ist nicht vollständig klar, wie viele Bauteile beschädigungsfrei gewonnen werden können. Projekte brauchen daher Reservequoten oder flexible Planung.

**Handling empfindlicher Bauteile:** Fenster, Verglasungen, Türen, Fassadenelemente oder Leuchten können beim Ausbau oder Transport leicht beschädigt werden. Sie brauchen spezielle Verpackung und geschultes Personal.

**Schwere und sperrige Bauteile:** Stahlträger, Betonfertigteile, Naturstein oder Holzträger benötigen Kräne, Spezialtransporte, Genehmigungen und tragfähige Lagerflächen.

**Sortenreinheit und Kennzeichnung:** Wenn Bauteile unmarkiert gestapelt werden, gehen Maße, Prüfstatus und Herkunft verloren. Logistik ohne Datenmanagement erzeugt spätere technische und rechtliche Probleme.

**Schnittstellen zwischen Gewerken:** Rückbau, Aufbereitung, Transport, Lagerung und Einbau liegen oft bei unterschiedlichen Akteuren. Ohne Koordination entstehen Lücken, Doppelarbeiten und Haftungsstreit.

**Abfallstatus:** Je nach rechtlicher Einordnung kann ein ausgebautes Bauteil als Produkt, Nebenprodukt oder Abfall behandelt werden. Diese Einordnung beeinflusst Transport, Lagerung, Dokumentation und Vermarktung. Sie ist rechtsraum- und fallabhängig.

### 4. Systemische Lösungsansätze

**Frühe Rückbauinventur:** Logistik beginnt mit dem Audit. Bauteile, die erst beim Abbruch entdeckt werden, können selten in anspruchsvolle Projekte integriert werden.

**Materialbroker / Re-Use-Koordination:** Eine zentrale Rolle kann Angebot, Nachfrage, technische Prüfung, Reservierung und Logistik verbinden. Ohne Koordinationsfunktion bleibt Wiederverwendung Zusatzaufgabe einzelner Planender.

**Donor-to-recipient-Matching:** Projekte sollten mögliche Spender- und Empfängergebäude früh koppeln. Direkter Transfer reduziert Lagerkosten, verlangt aber flexible Entwurfs- und Terminplanung.

**Regionale Re-Use-Hubs:** Hubs bündeln Lagerung, Aufbereitung, Verkauf und Qualitätssicherung. Sie schaffen Skaleneffekte und erhöhen Marktsichtbarkeit.

**Standardisierte Verpackung und Transporthilfen:** Wiederverwendete Bauteile brauchen wiederholbare Handling-Lösungen, z. B. Türgestelle, Fensterrahmen, Langguttraversen, Stapelboxen oder Palettierung nach Bauteiltyp.

**Bauteiltracking:** QR-Codes, RFID oder stabile Lager-IDs verknüpfen physisches Bauteil und Datensatz. Dies reduziert Verwechslung und erleichtert Nachweisführung.

**Flexible Planung:** Entwurf und Ausführung müssen Toleranzen, alternative Bauteile und Ersatzmengen zulassen. Logistikprobleme sind weniger gravierend, wenn das Projekt nicht auf exakt ein Produkt fixiert ist.

**Vergütete Prozessleistungen:** Suche, Demontage, Transport, Lagerung und Prüfung müssen als eigene Leistungen anerkannt werden. Andernfalls werden sie als unvergütetes Risiko wahrgenommen.

**Regionale Kreisläufe:** Kurze Distanzen, lokale Lager und regionale Nachfrage verringern Kosten und Koordinationsaufwand. Dennoch ist Transportwirkung bauteilabhängig zu bewerten: Für viele materialintensive Bauteile bleibt vermiedene Neuproduktion ökologisch wichtiger als zusätzlicher Transport, aber dies ist nicht pauschal gültig.

## Praxisbezug / Beispiele

**Direkte Kopplung zweier Projekte:** Ein Abbruchgebäude liefert Ziegel, Türen oder Stahlprofile direkt an ein Neubauprojekt. Erfolgsfaktoren sind identische Zeitfenster, flexible Planung, frühe Reservierung und klare Verantwortlichkeiten. Scheitern kann der Ansatz an Verzögerungen, Bruchquote oder fehlenden Nachweisen.

**Re-Use-Hub als Puffer:** Ein regionaler Hub nimmt Bauteile aus mehreren Rückbauprojekten auf, katalogisiert sie und verkauft sie an verschiedene Projekte. Dies reduziert die Notwendigkeit direkter Synchronisierung, erfordert aber Fläche, Personal, Kapital und Datenmanagement.

**Innenausbau:** Türen, Leuchten, Doppelböden, Sanitärobjekte und Trennwände sind logistisch oft einfacher als Tragwerke, weil sie kleiner, standardisierter und leichter zu transportieren sind. Trotzdem entstehen Aufwand für Sortierung, Reinigung, Prüfung und Lagerung.

**Schwere Tragwerkselemente:** Stahl- oder Holzträger haben hohen ökologischen Wert, aber auch hohe Anforderungen an Demontage, Kranlogistik, Transport, Lagerung, Prüfung und neue Planung. Hier lohnt sich Wiederverwendung vor allem bei früh gesicherter Nachfrage.

**Pflaster, Naturstein und Ziegel:** Diese Materialien sind robust, aber massenreich. Logistik entscheidet über Wirtschaftlichkeit: kurze Wege, gute Palettierung, sortierte Chargen und gesicherter Absatz sind zentral.

## Herausforderungen / offene Fragen

- Wie können Rückbau- und Neubautermine systematisch gekoppelt werden?
- Welche Rolle sollen Kommunen bei regionalen Re-Use-Hubs und Materialflüssen übernehmen?
- Wie lassen sich Bruchquoten, Reservequoten und Prüfversagen in Termin- und Kostenplänen abbilden?
- Welche Transport- und Verpackungsstandards sind für häufige Bauteilgruppen sinnvoll?
- Wie kann der Abfallstatus während Transport und Lagerung rechtssicher geklärt werden?
- Welche digitalen Tools verbinden Audit, Lager, Marktplatz, Ausschreibung und Baustellenlogistik?
- Wie lassen sich kleine Bauteilchargen wirtschaftlich bündeln?
- Wie werden ökologische Vorteile durch zusätzliche Transporte belastbar bilanziert?
- Unsicher / regional unterschiedlich: Infrastruktur, Abfallrechtspraxis, Verfügbarkeit von Rückbauunternehmen, Lagerflächen und Marktnachfrage unterscheiden sich stark zwischen Regionen.

## Quellen

- FCRBE / Interreg North-West Europe: *A guide for facilitating the integration of reclaimed building materials*, 2020. https://vb.nweurope.eu/media/9955/20200331_fcrbe_wpt3_d1_1_a_guide_for_the_integration_of_reclaimed_building_materials.pdf
- FCRBE / Interreg North-West Europe: *The Reclamation Audit*, 2023. https://www.cstb.fr/getmedia/365c639a-3f3a-4e19-b2d0-e55f202414a2/Guide-reclamation-audit.pdf
- FCRBE / Interreg North-West Europe: *Reuse Toolkit – Procurement Strategies*, 2021/2022. https://vb.nweurope.eu/media/16916/wpt3_d_2_2_procurement_strategies_20220208.pdf
- FCRBE / Interreg North-West Europe: Projektbeschreibung und Zielsetzung. https://vb.nweurope.eu/projects/project-search/fcrbe-facilitating-the-circulation-of-reclaimed-building-elements-in-northwestern-europe/
- BBSR: John, V.; Stark, T. u. a.: *Wieder- und Weiterverwendung von Baukomponenten (RE-USE)*, BBSR-Online-Publikation 27/2021. https://www.bbsr.bund.de/BBSR/DE/veroeffentlichungen/bbsr-online/2021/bbsr-online-27-2021-dl.pdf
- Umweltbundesamt: *Instrumente zur Wiederverwendung von Bauteilen und hochwertigen Verwertung von Baustoffen*, Texte 93/2015. https://www.umweltbundesamt.de/publikationen/instrumente-zur-wiederverwendung-von-bauteilen
- Arup / Circular Buildings Toolkit: *The Reuse Playbook*, 2025. https://ce-toolkit.dhub.arup.com/assets/reuse_playbook--cqdY42X.pdf
- Opalis: Dokumentation zur Wiederverwendung und FCRBE-Materialblätter. https://opalis.eu/en/documentation
- Rakhshan, K. et al.: *Components reuse in the building sector – A systematic review*, 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7472835/
- Bundesregierung / Nationale Kreislaufwirtschaftsstrategie, Handlungsfeld Bau- und Gebäudebereich. https://www.kreislaufwirtschaft-deutschland.de/kreislaufwirtschaftsstrategie/handlungsfelder/bau-und-gebaeudebereich

