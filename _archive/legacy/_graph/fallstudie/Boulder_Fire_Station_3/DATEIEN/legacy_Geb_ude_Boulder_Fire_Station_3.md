# Boulder Fire Station 3, Boulder, Colorado — Fallstudie Direct Reuse / zirkuläres Bauen

**Stand:** 2026-05-07  
**Sprache:** Deutsch  
**Arbeitsregel:** Gewertet werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Recycling des Krankenhauses und gespendete lose Innenausstattung zählen nicht für diese Fallstudie, außer sie wurden fest in Fire Station 3 eingebaut.

---

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Boulder Fire Station 3 ist ein gebauter öffentlicher Neubau mit substanzieller tragender Wiederverwendung: 89 geborgene Stahlbauteile / Wide-Flange-Stahlprofile mit zusammen ca. 25 tons wurden aus dem dekommissionierten Boulder Community Hospital als strukturelle Bauteile in der neuen Feuerwache wiederverwendet. Es ist ein klarer Direct-Reuse-Fall für Tragwerk, aber nur ein Teil des Gesamttragwerks; deshalb ★★★★☆, nicht ★★★★★.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** nein — Neubau; das Krankenhaus ist Donor Building, kein Bestandserhalt der Feuerwache.
- **Warnung Möbel/Dekoration:** nein — Krankenhausmöbel/Innenausstattung wurden teilweise gespendet/verkauft, zählen aber hier nicht.
- **Projektstatus:** gebaut / completed and brought online November 2024

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Boulder Fire Station 3 / City of Boulder Fire Rescue, Station #3 | untersuchter Fall | AISC; City of Boulder | belegt | öffentlicher Neubau mit reclaimed steel |
| Gebäude | Fire Station 3 & Fire Administration | neues Feuerwehr-/Verwaltungsgebäude | City of Boulder | belegt | 2967 Bluff Street laut City location page |
| Projekt | New Boulder Fire-Rescue Station 3 | Ersatz für alte, ineffiziente Station | City of Boulder | belegt | alte Station lag im 100-year flood plain |
| Ort | Boulder, Colorado, USA | Standort | City of Boulder; AISC | belegt | USA |
| People | Davis Partnership Architects | Architekt | AISC | belegt | Denver |
| People | KL&A Engineers and Builders | Tragwerksplanung / Stahlreuse-Koordination | AISC; Greenbuild/STRUCTURE | belegt | prüfte/selektierte Wiederverwendungsstahl |
| Projekt | City of Boulder | Bauherr / Eigentümer / Initiator | AISC; City of Boulder | belegt | Stadt hatte Krankenhaus-Stahlstockpile |
| People | Mark Young Construction | Builder | SE2050/AISC PDF-Snippet; sekundär | teilweise belegt | nicht aus AISC-Seite selbst detailliert übernommen |
| Bauteil | 89 salvaged wide-flange steel members | wiederverwendete Tragwerksbauteile | AISC Modern Steel; AISC Awards | belegt | ca. 25 tons |
| Material | Stahl | tragendes Material | AISC | belegt | aus Boulder Community Hospital |
| Gebäude | Boulder Community Hospital / Boulder Community Health hospital | Donor Building | AISC; AHA; Colorado Sun | belegt | 30-year-old decommissioned hospital laut AISC |
| Abbruchmethode | Deconstruction statt demolition | selektive Rückgewinnung | AISC; STRUCTURE; AHA | belegt | durch Boulder Deconstruction Ordinance beeinflusst |
| Recht | Boulder Deconstruction Ordinance 8366 / 2020 | 75 % Materialdiversion nach Gewicht | AISC; STRUCTURE | belegt | lokale Verordnung |
| Kennwert | 28.300 / 28.370 sq ft | Gebäudegröße | AISC Modern Steel / AISC Awards | belegt | Rundungs-/Quellenabweichung |
| Kennwert | 25 tons reused structural steel | Direct-Reuse-Masse Stahl | AISC Modern Steel | belegt | US tons; metrisch nicht umgerechnet im Quellenwert |
| Kennwert | 89 members | Anzahl wiederverwendeter Stahlprofile | AISC Modern Steel; AISC Awards | belegt | strukturelle Mitglieder |
| Kennwert | 161 tons salvaged structural steel from hospital | Gesamtstockpile Krankenhausstahl | AISC Modern Steel | belegt | davon 25 tons in Fire Station 3 |
| Kennwert | 21 other projects reused members from stockpile | Reuse-Kette | AISC Modern Steel | belegt | zusätzliche Projekte außerhalb dieser Fallstudie |
| Kennwert | 60.8 million pounds diverted from landfill | Deconstruction-Ergebnis Krankenhaus | AHA | belegt | bezieht sich auf Donor-Gelände, nicht nur Fire Station |
| Kennwert | 75 % diversion requirement | regulatorischer Grenzwert | AISC; STRUCTURE | belegt | Boulder-Verordnung |
| Reuse-Strategie | ex-situ Bauteilwiederverwendung | Stahl aus Krankenhaus in Feuerwache | AISC | belegt | tragend |
| Tragwerkssystem | Hybrid aus Glulam-Timber Columns und reclaimed steel beams | neues Tragwerk | AISC Awards | belegt | Beton/Deckensysteme zusätzlich |
| Prüfung | Auswahl, Dokumentation, Testing/Verification von reclaimed steel | technischer Nachweis | AISC; Greenbuild; STRUCTURE | belegt | Detailwerte unbekannt |
| Hürde | fehlende Industriestandards für Prüfung reclaimed steel | technische/rechtliche Hürde | AISC Awards | belegt | Testing/Documentation/Cleanup erforderlich |
| Hürde | hohe Front-End-Kosten und Logistikunsicherheit | Wirtschaft/Prozess | AISC Awards | belegt | Wiederverwendung trotzdem als machbar/finanziell vorteilhaft dargestellt |
| Software/Tool | stockpile catalog / member identification | Dokumentation | AISC Modern Steel; Colorado Sun | teilweise belegt | konkrete Software unbekannt |
| Schadstoff | unbekannt | Donor Hospital / Stahl | unbekannt | unbekannt | keine belastbare Angabe |
| Norm | unbekannt | Stahlprüfung/Code | unbekannt | unbekannt | keine Normnummern öffentlich im herangezogenen Material |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Donor Building | Reuse-Ketten brauchen ein Herkunftsgebäude als eigene Entität. | Boulder Community Hospital als Stahlquelle. | Gebäude, Bauteil, Logistik |
| Material Stockpile | Geborgene Bauteile werden katalogisiert und später mehreren Projekten zugeordnet. | 161 tons structural steel stockpile. | Bauteil, Logistik, Tool |
| Deconstruction Ordinance | Lokales Recht kann Reuse auslösen. | Boulder Ordinance 8366 / 75 % diversion. | Recht, Abbruchmethode |
| Essential Facility / Risk Category | Feuerwachen haben höhere Anforderungen als normale Gebäude. | Fire Station 3 als kritische Infrastruktur. | Leistungsanforderung, Recht, Prüfung |

---

## 3. FALLSTUDIE

- **Name:** Boulder Fire Station 3 / City of Boulder Fire Rescue Station #3
- **Ort:** Boulder, Colorado, USA; City page nennt 2967 Bluff Street, Boulder, CO 80301
- **Gebäude:** Feuerwache und Fire Administration
- **Projekt:** Neubau / Ersatzbau für alte Fire Station 3
- **Beteiligte People / Akteure:** City of Boulder; Davis Partnership Architects; KL&A Engineers and Builders; Mark Young Construction (sekundär belegt); Boulder Community Hospital/Health als Donor-Kontext; Full Metal Iron als Fabricator laut SE2050-Snippet, Details nicht weiter geprüft
- **Architekt:** Davis Partnership Architects
- **Tragwerksplaner:** KL&A Engineers and Builders
- **Bauherr:** City of Boulder
- **Zeitraum:** Planung vor/um 2023–2024; completed/brought online November 2024; Completion Date Q4 2024 laut City project page
- **Ursprüngliche Nutzung:** Donor-Stahl: Krankenhausstruktur des dekommissionierten Boulder Community Hospital
- **Neue Nutzung:** tragende Stahlbauteile in Feuerwache / öffentliche Sicherheitsinfrastruktur
- **Fläche / Maßstab:** 28.300 sq ft laut AISC Modern Steel; 28.370 sq ft laut AISC Awards
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** sehr gut für Stahlmenge, Anzahl Bauteile, Akteure, Status und Hürden; mittel für detaillierte Prüfmethoden, Kosten, Normen und CO₂

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; tragende Stahlwiederverwendung
- **Hauptniveau:** Tragwerk
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Fall zählt, weil Stahlträger/-profile aus dem Krankenhaus als tragende Elemente in einem neuen Gebäude wieder eingebaut wurden. Das Recycling von Beton/Backstein auf dem Krankenhausareal, die Spende/Veräußerung von Türen, Toiletten, Leuchten oder medizinischer Ausstattung und der generelle Krankenhaus-Rückbau zählen nicht für die Bewertung der Feuerwache, sofern nicht fest dort eingebaut.
- **Warum ist der Fall relevant?** Öffentliche kritische Infrastruktur demonstriert, dass strukturelle Wiederverwendung von Stahl auch bei hohen Anforderungen möglich ist, wenn Donor-Bauteile katalogisiert, ausgewählt, geprüft, gereinigt und neu bemessen werden.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Wide-flange beams / structural steel members | Stahl | Boulder Community Hospital Steel Stockpile | Krankenhaus-Tragwerk | tragende Stahlbauteile der neuen Feuerwache | 89 Mitglieder / ca. 25 tons | ja | ja | nein | nein | selektiver Rückbau, Katalogisierung, Reinigung, Vorbereitung, Re-Fabrication | geschraubt/geschweißt unbekannt | Testing/Verification belegt, Details unbekannt | Tragfähigkeit, Essential Facility, 100-year service life | lokale Bauordnung/IBC unbekannt; Deconstruction Ordinance relevant | fehlende Standards, Dokumentation, Kosten | AISC Modern Steel; AISC Awards | genaue Profile, Prüfwerte |
| Stahlstockpile gesamt | Stahl | dekommissioniertes Hospital | Tragwerk | Verteilung auf Fire Station 3 und weitere Projekte | 161 tons salvaged structural steel | ja | potenziell | nein | nein | Katalogisierung/Stockpile | unbekannt | unbekannt | je Folgeprojekt | Boulder ordinance | Matching von Bauteilen zu Projekten | AISC Modern Steel | Zuordnung |
| Glulam timber columns | Brettschichtholz | neu/unbekannt | nicht anwendbar | neue Stützen | unbekannt | ja | ja | nein | nein | neu | unbekannt | unbekannt | Tragfähigkeit | unbekannt | nicht Direct Reuse | AISC Awards | Menge |
| Concrete slab on metal deck / composite framing | Beton/Stahl | neu/unbekannt | nicht anwendbar | Decken-/Tragwerkssystem | unbekannt | ja | ja | nein | nein | neu/unbekannt | unbekannt | unbekannt | Tragfähigkeit | unbekannt | nicht Direct Reuse | AISC/SE2050-Snippet | Details |
| PV-Dach / große Dachfläche | Photovoltaik/Metall | neu/unbekannt | nicht anwendbar | Energieerzeugung | offset estimated 65 % annual electric consumption laut AISC | nein | nein | Hülle/Technik | ja | neu | unbekannt | unbekannt | Energie | CoBECC unbekannt | nicht Direct Reuse | AISC Awards | technische Daten |
| Türen, Leuchten, Toiletten, Cabinets aus Hospital | diverse | Hospital | Innenausstattung | gespendet/verkauft, nicht als Fire-Station-Reuse belegt | unbekannt | nein | ggf. | ggf. | ggf. | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nicht für diesen Fall zählen | AHA | ob Teile in Fire Station 3 eingebaut wurden |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Hospital-Stahl identifizieren | City of Boulder, KL&A, Rückbauteam | Deconstruction survey | stockpile catalog, konkrete Software unbekannt | deconstruction | Markieren/Katalogisieren | Maße/Specs aufgezeichnet | Hospitalareal | Stahl später passend einsetzen | jedes Bauteil labeln | AISC; Colorado Sun |
| Bauteilinventar | Stahlprofile dokumentieren | KL&A/Team | Fotos, Maße, Bolt-hole patterns laut sekundären Quellen | Katalog | selektiver Rückbau | unbekannt | Dokumentation | On-site stockpile | keine Standardprodukte | Katalogisierung | AISC; Colorado Sun |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | Hospitaldeconstruction | unbekannt | unbekannt | unbekannt | Krankenhausaltbau | unbekannt | unbekannt |
| Rückbau | Krankenhaus nicht demolieren, sondern dekonstruieren | City/Boulder Community Health/Rückbauakteure | Deconstruction | unbekannt | Deconstruction Ordinance | Stahl schonend ausbauen | unbekannt | vor Ort | Arbeitsschutz/Planung | selektiver Ausbau | AHA; STRUCTURE |
| Ausbau | Stahlträger schneiden/entnehmen | Rückbau-/Stahlteam | beam removal | unbekannt | selektiv | Zuschneiden am Ende laut Colorado Sun | unbekannt | Kran/Transport | Beschädigung, Markierung | Labeling | Colorado Sun |
| Transport | vom Hospital-Stockpile zur Feuerwache | City/Contractor | lokale Logistik | unbekannt | unbekannt | unbekannt | unbekannt | Boulder lokal | Timing, Lager | Stockpile bis Verwendung | AISC |
| Lagerung | Stahl auf Hospitalgelände/Stockpile | City of Boulder | stockpiling | Katalog | unbekannt | cleanup | unbekannt | on-site storage | Lagerplatz/Kosten | Lager am Donor-Ort | Colorado Sun; AISC |
| Aufbereitung | reinigen, dokumentieren, für Einbau vorbereiten | KL&A, Fabricator, Contractor | refabrication/prep | unbekannt | unbekannt | cleanup, preparation | Testing/verification | Werkstatt/Baustelle | front-end costs | koordinierte Aufbereitung | AISC Awards |
| Planung | Design nach neuem Entwurf, Ersatz geeigneter Neuprofile durch Salvage | Davis Partnership; KL&A | member matching | stockpile catalog | unbekannt | unbekannt | Auswahl potenzieller Mitglieder | zwischen Planung und Lager | Design war schon genehmigt | neue Bauteile durch passende gebrauchte ersetzen | AISC Modern Steel |
| Genehmigung | Nachweis gebrauchter Stahlteile | Planer/Behörden | unbekannt | unbekannt | unbekannt | unbekannt | Prüfung erforderlich | unbekannt | keine Industriestandards | detaillierte Dokumentation und Tests | AISC Awards |
| Wiedereinbau | Wiederverwendung als strukturelle Rahmen-/Trägerbauteile | Contractor/Fabricator | Montage im Hybridtragwerk | unbekannt | unbekannt | vorbereitet | statischer Nachweis | Baustelle | Konsistenz/Dimensionen | strategische Auswahl | AISC Awards |
| Monitoring | Prototype für Circular Design | City/Davis/KL&A | lessons learned | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Skalierung | Veröffentlichung/Auszeichnung | AISC Awards |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | hybrid steel-and-timber / glulam columns + reclaimed steel beams | Tragfähigkeit, 100-year service life | unbekannt | statische Bemessung | Secondhand-Stahl integrieren | KL&A wählte passende Member | AISC Awards; AISC Modern Steel |
| Lastabtragung | reclaimed steel als strukturelle Member | Lasten sicher abtragen | unbekannt | Testing/Verification | Profilgrößen müssen passen | Austausch ausgewählter Neuprofile durch salvaged members | AISC Modern Steel |
| Verbindung | unbekannt | Montage, Robustheit | unbekannt | unbekannt | alte Bohrungen/Geometrie | Dokumentation bolt-hole patterns laut sekundärer Quelle | AISC/Colorado Sun |
| Brandschutz | Feuerwache / kritische Infrastruktur | Brandschutz, Einsatzbereitschaft | unbekannt | unbekannt | Stahl/Glulam | unbekannt | unbekannt |
| Schallschutz | unbekannt | Nutzung Feuerwehr/Verwaltung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Feuchte | unbekannt | Korrosionsschutz | unbekannt | unbekannt | gebrauchte Stahloberflächen | cleanup/prep | AISC Awards |
| Wärmeschutz | Gebäude soll Energy Conservation Goals überschreiten | Energieperformance | CoBECC laut AISC | unbekannt | nicht Reuse-spezifisch | all-electric, PV, daylighting | AISC Awards |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | Stahlanschlüsse | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | Gebäudeenergie | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| TGA-Integration | all-electric station; PV offset estimated 65 % annual electricity | Betrieb/Energie | CoBECC | unbekannt | nicht Reuse-spezifisch | große Dachfläche/PV | AISC Awards |
| Barrierefreiheit | unbekannt | öffentliche Nutzung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Dauerhaftigkeit | 100-year building / service life Ziel | Lebensdauer | unbekannt | unbekannt | Gebrauchtstahlqualität | Testing/Verification | AISC Awards |
| Wartung | unbekannt | Wartbarkeit | unbekannt | unbekannt | heterogeneous reuse members | Dokumentation | AISC Awards |
| Zulassung | absence of industry standards for testing reclaimed steel | Code compliance | unbekannt | Tests und Dokumentation | fehlende Standards | Zusammenarbeit/technische Innovation | AISC Awards |
| Haftung | unbekannt | Verantwortlichkeit | unbekannt | unbekannt | Wiederverwendung in Essential Facility | unbekannt | unbekannt |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| wiederverwendete Stahlmember | 89 | Anzahl | stockpile catalog / Auswahl | Fire Station 3 | AISC Modern Steel; AISC Awards | belegt |
| wiederverwendete Stahlmasse | 25 | tons | unbekannt | Fire Station 3 | AISC Modern Steel | belegt |
| Gesamtmenge salvaged structural steel Hospital | 161 | tons | unbekannt | Donor Building / Stockpile | AISC Modern Steel | belegt |
| weitere Projekte mit Hospital-Stahl | 21 | Anzahl | unbekannt | Stockpile-Reuse-Kette | AISC Modern Steel | belegt |
| Gebäudefläche | 28.300 | sq ft | unbekannt | Fire Station | AISC Modern Steel | belegt |
| Gebäudefläche | 28.370 | sq ft | unbekannt | Fire Station | AISC Awards | belegt; Quellenabweichung |
| Fertigstellung / online | November 2024 | Datum | unbekannt | Gebäude | City of Boulder | belegt |
| Completion Date | Q4 2024 | Zeitraum | unbekannt | Projekt | City of Boulder | belegt |
| Diversion requirement | 75 | % by weight | Boulder Ordinance | Deconstruction projects | AISC; STRUCTURE | belegt |
| Hospitalmaterial vom Deponieren vermieden | 60.8 million | pounds | unbekannt | Hospital-Deconstruction, nicht Fire Station allein | AHA | belegt |
| PV-Stromanteil | ca. 65 | % annual electric consumption offset | unbekannt | Betrieb Fire Station | AISC Awards | teilweise belegt |
| CO₂-Einsparung Direct Reuse | unbekannt | kg CO₂e | unbekannt | Fire Station 3 | unbekannt | unbekannt |
| Kostenwirkung | unbekannt | USD | unbekannt | Projekt | AISC nennt Kosten-/Front-End-Hürden, keine Zahl | unbekannt |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| fehlende Industriestandards für Prüfung reclaimed steel | technisch/rechtlich | Reuse-Stahl unüblich | mehr Nachweisaufwand | Prüfung, Recht, Tragwerk | Tests, Dokumentation, Teamarbeit | Standards/Protokolle für Reuse-Stahl entwickeln | AISC Awards |
| hohe Front-End-Kosten | wirtschaftlich | Suche, Designanpassung, Reinigung, Dokumentation | Mehrkosten zu Projektbeginn | Wirtschaft, Planung | strategische Planung, Kollaboration | Kosten früh budgetieren | AISC Awards |
| Mengen-/Größenkonsistenz | technisch/logistisch | Profile aus Donor Building passen nicht automatisch | Design muss Member matchen | Bauteil, Tool, Tragwerk | KL&A selektiert passende Member aus Katalog | Reuse braucht Matching zwischen Lager und Bemessung | AISC Modern Steel |
| Logistik und Lagerung | logistisch | Stockpile bis Einbau | Zeit-/Flächenbedarf | Logistik, Material Stockpile | On-site stockpile | Donor- und Receiver-Projekt zeitlich koppeln | Colorado Sun; AISC |
| Reinigung und Aufbereitung | technisch/wirtschaftlich | gebrauchte Stahloberflächen/Anschlüsse | Zusatzarbeit | Aufbereitungsmethode | cleanup/prep | Aufbereitung als eigene Leistung planen | AISC Awards |
| Risiko kritischer Infrastruktur | technisch/rechtlich | Feuerwache/Essential Facility | höhere Anforderungen | Leistungsanforderung, Prüfung | Tests, detaillierte Statik | Reuse ist auch bei hohen Anforderungen möglich, aber nachweisintensiv | AISC Awards |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** städtisch initiierte Wiederverwendung aus eigenem Donor-Building/Stockpile.
- **Bauteilbörse / Quelle:** Boulder Community Hospital Steel Stockpile; keine kommerzielle Bauteilbörse belegt.
- **Kostenwirkung:** AISC nennt hohe Front-End-Kosten für Design, Vorbereitung und Dokumentation; konkrete Kostenwirkung unbekannt.
- **Zeitwirkung:** unbekannt; Planung war bereits fortgeschritten, als Reuse-Stahl integriert wurde.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** erhöht durch Katalogisierung, Auswahl, Tests, Cleanup und Re-Fabrication; konkrete Stunden unbekannt.
- **Lagerung:** Stahl wurde im Stockpile gelagert; Colorado Sun nennt on-site storage bis zur Verwendung, Details/Kosten unbekannt.
- **Marktbarrieren:** fehlende Prüfnormen/Standards, Materialmatching, Lagerlogistik, Kostenunsicherheit, Dokumentationsbedarf.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** mittel bis hoch; AISC zeigt Stahlträger im Apparatus Bay / Tragwerk als Teil der architektonischen Erzählung.
- **räumliche Transformation:** Donor-Stahl aus Krankenhaus wird Teil einer Feuerwache; starke öffentliche/kulturelle Transformation von Gesundheitsinfrastruktur zu Sicherheitsinfrastruktur.
- **Atmosphäre / Ausdruck:** robuste, öffentliche, technische Architektur mit hybrider Holz-Stahl-Tektonik.
- **Umgang mit Spuren:** unbekannt; ob alte Markierungen/Patina sichtbar bleiben, öffentlich nicht eindeutig belegt.
- **sozialer Wert:** Stadtinternes Kreislaufprojekt; Krankenhausmaterial unterstützt weiterhin öffentliche Gemeinschaftsfunktionen.
- **Denkmal- oder Bestandswert:** kein Denkmalstatus belegt; Wert liegt in Donor-Materialgeschichte.
- **Kritik / Grenzen:** Reuse-Anteil am Gesamttragwerk ist partiell; CO₂- und Kostenwerte nicht vollständig öffentlich; Krankenhaus-Recycling darf nicht als Fire-Station-Direct-Reuse überbewertet werden.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** konkrete Stahlprofile, Materialgüten, Prüfergebnisse, Norm-/Code-Pfade, CO₂-Bilanz, vollständiges Kostenmodell, Versicherungs-/Haftungsmodell.
- **Sinnvolle neue Entitäten:** Donor Building; Material Stockpile; Deconstruction Ordinance; Essential Facility.
- **Fehlende Daten:** genaue Anschlüsse, Re-Fabrication-Prozess, Brandschutznachweise, Gewährleistung, Transportdistanzen.
- **Zu prüfende Quellen:** STRUCTURE-Magazine-Fallstudie im Volltext, SE2050 PDF, KL&A-Projektdaten, City-of-Boulder-Bid/permit documents, AISC detail drawings.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja
- **5 wichtigste Fakten:**
  1. Fire Station 3 wurde im November 2024 in Betrieb genommen.
  2. 89 gebrauchte Stahlmember aus dem Boulder Community Hospital wurden eingebaut.
  3. Die wiederverwendete Stahlmenge beträgt ca. 25 tons.
  4. Das Donor-Hospital lieferte insgesamt ca. 161 tons salvaged structural steel.
  5. Boulder verlangt durch Deconstruction Ordinance 8366 eine 75-%-Materialdiversion nach Gewicht.
- **5 wichtigste Bauteile:**
  1. reclaimed wide-flange steel beams
  2. reclaimed steel structural members
  3. steel stockpile / donor profiles
  4. glulam columns als neues Hybridtragwerkselement
  5. composite framing/decking als nicht-reused Kontext
- **5 wichtigste Hürden:**
  1. fehlende Standards für reclaimed steel testing
  2. hohe Front-End-Kosten
  3. Matching von Profilgrößen
  4. Lagerung und Timing
  5. Dokumentation/Cleanup/Re-Fabrication
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Ein Donor-Building muss früh katalogisiert werden.
  2. Stockpile + Design müssen technisch gematcht werden.
  3. Reuse in kritischer Infrastruktur ist möglich, aber nachweisintensiv.
  4. Lokale Deconstruction-Ordinances können Reuse aktivieren.
  5. Recyclingquote und Direct-Reuse-Menge müssen getrennt bilanziert werden.
- **5 offene Fragen:**
  1. Welche genauen Materialtests wurden durchgeführt?
  2. Welche Profile/Güten wurden wiederverwendet?
  3. Wie hoch war die CO₂-Einsparung der 25 tons Stahl?
  4. Welche Kosten entstanden für Reuse gegenüber Neubaustahl?
  5. Welche Haftungs- und Gewährleistungsregelungen wurden vereinbart?

---

## Quellen und Links

- AISC Modern Steel – Inside Davis Partnership's reuse of steel in a new fire station: https://www.aisc.org/modern-steel/news/inside-davis-partnerships-reuse-of-steel-in-a-new-fire-station/
- AISC IDEAS Awards – City of Boulder Fire Rescue, Station #3: https://www.aisc.org/awards-and-honors/ideas-awards-archive/city-of-boulder-fire-rescue-station-3/
- City of Boulder – Fire Station 3 & Fire Administration: https://bouldercolorado.gov/locations/fire-station-3-fire-administration
- City of Boulder – New Fire Station 3: https://bouldercolorado.gov/projects/new-fire-station-3
- AHA – What do you do with an old hospital? In Boulder, you recycle it.: https://www.aha.org/role-hospitals-boulder-community-health-hospital-recycled
- STRUCTURE Magazine – Circular Construction: https://www.structuremag.org/article/circular-construction-2/
- Colorado Sun – Boulder deconstructs and recycles an entire old hospital: https://coloradosun.com/2023/10/29/boulder-community-hospital-deconstruction-recycled/
- Greenbuild 2025 – Circularity in Action: https://attend.greenbuild.informaconnect.com/event/greenbuild2025/planning/UGxhbm5pbmdfMjY4OTQ1OQ%3D%3D
- SE2050 / SEI Circular Economy Case Study PDF – Boulder Fire Station 3: https://se2050.org/wp-content/uploads/2025/11/SEI-CE-WG-Circular-Economy-Case-Studies_15-Boulder-Fire-Station-3_2025.pdf
