## Verknüpfungen

- **Übergeordnete Themen:** Kreislauffähigkeit, Materialidentität, Gebäuderessourcenpass, digitaler Produktpass, Urban Mining, Rückverfolgbarkeit, Lebenszyklusdaten, Wiederverwendungsnachweis.
- **Verwandte Dateien:** `dokument/Materialinventar.md`, `dokument/Bestandsaufnahme.md`, `dokument/Bauwerksdiagnose.md`, `dokument/Pre_Demolition_Audit.md`, `dokument/Rueckbaukataster.md`, `dokument/Auditbericht.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Hersteller, Bauherrschaft, Planer:innen, BIM-Management, DGNB, BAMB, Madaster, EPEA, ÖKOBAUDAT, EPD-Programmbetreiber, Rückbauunternehmen, Reuse-Händler, Prüfstellen; DGNB Gebäuderessourcenpass, BAMB Materials Passports, EN 15804, ISO 14025, ISO 19650, IFC, EU Digital Product Passport im weiteren regulatorischen Umfeld, Level(s), DIN SPEC 91484; `methode/` für Datenaufnahme, Datenvalidierung, Kreislauffähigkeitsbewertung, Bauteil-ID; `prozessphase/` für Planung, Bau, Betrieb, Umbau, Rückbau; `pruefung/` für Material-, Schadstoff-, Leistungs- und Konformitätsnachweise; `datenmodell/` für Passstruktur, Objekt-ID, Produktdatenvorlagen, IFC, API; `logistik/` für Ausbau, Eigentumswechsel, Lagerung, Marktplatz und Rückverfolgbarkeit.

## Kurzdefinition

Ein **Materialpass** ist ein strukturierter, idealerweise digitaler Datensatz, der Materialien, Produkte, Bauteile oder Gebäude über ihren Lebenszyklus identifizierbar macht und Informationen bereitstellt, die ihre Instandhaltung, Reparatur, Demontage, Wiederverwendung, Vorbereitung zur Wiederverwendung, Wiederaufbereitung oder hochwertige Verwertung ermöglichen. In der Bauwirtschaft wird der Begriff sowohl für Produkt- oder Bauteilpässe als auch für Gebäude- oder Ressourcenpässe verwendet; die genaue Bedeutung ist daher projekt- und systemabhängig zu definieren.

Ein Materialpass unterscheidet sich vom **Materialinventar**: Das Inventar erfasst primär „was wo in welcher Menge vorhanden ist“. Der Materialpass ergänzt diese Orts- und Mengendaten um qualifizierte Eigenschaften, Nachweise, Herkunft, Zusammensetzung, Kreislaufbewertung, Demontageinformationen und Aktualisierung über den Lebenszyklus.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung scheitert häufig an fehlenden Informationen: unbekannte Materialien, unsichere Schadstofflage, fehlende Herstellerdaten, ungeklärte Leistungsmerkmale, nicht dokumentierte Umbauten, fehlende Demontagehinweise. Materialpässe adressieren genau diese Informationsverluste.

Für Wiederverwendung sind Materialpässe relevant, weil sie:

- Materialien und Bauteile aus der Anonymität holen,
- technische und ökologische Informationen langfristig sichern,
- Demontage und zukünftige Nutzung bereits in Planung und Betrieb vorbereiten,
- Werte von Bauteilen sichtbar machen,
- Schnittstellen zu Marktplätzen und Rückbauplanung schaffen,
- den Übergang vom Abfallstatus zur Produkt- oder Bauteilnutzung erleichtern können, sofern rechtliche und technische Voraussetzungen erfüllt sind,
- ökologische Bewertungen, Gebäuderessourcenpässe und zirkuläre Beschaffung unterstützen.

## Fachinhalt

### Dokumenttyp

- **Zweck:** Identifikation, Dokumentation und Fortschreibung relevanter Material-, Produkt- und Bauteilinformationen zur Sicherung von Wert, Qualität und Kreislauffähigkeit.
- **Inhalt:** Identität, Hersteller- oder Herkunftsdaten, Materialzusammensetzung, Mengen, technische Eigenschaften, Umweltinformationen, Prüf- und Zertifikatsnachweise, Schadstoffinformationen, Reparatur- und Demontagehinweise, Wartung, Austauschhistorie, Kreislaufoptionen, Verantwortlichkeiten, Datenqualität.
- **Autorenschaft:** Bei Neubauten idealerweise Hersteller, Planer:innen, Ausführende und Bauherrschaft gemeinsam; im Bestand oft rekonstruiert durch Bestandsaufnahme, Materialinventar, Bauwerksdiagnose, Auditor:innen und Sachverständige. Plattformen können Struktur und Datenhaltung bereitstellen, ersetzen aber nicht die fachliche Verantwortung.
- **Einsatzzeitpunkt:** Idealerweise ab Planung und Beschaffung; bei Bestandsgebäuden nachträglich aus Bestandsaufnahme, Inventar und Prüfungen; fortzuschreiben im Betrieb, bei Umbau und Rückbau.
- **Mindestinhalte:** eindeutige Objekt-/Produkt-/Bauteil-ID, Zuordnung im Gebäude, Material- und Produktbeschreibung, Menge, Datenquelle, Datenqualität, technische Leistungsdaten, Umwelt- und Gesundheitsinformationen, Demontagehinweise, Wiederverwendungs- oder Verwertungsoption, Aktualisierungsdatum.
- **Datenlogik:** Identifizierbares Objekt → Eigenschaften → Nachweise → Nutzungshistorie → Zustand → Kreislaufoption → Übergabe-/Folgeprozess. Ein Pass sollte nicht nur beschreiben, sondern Belege und Versionen mitführen.
- **Anschlussfähigkeit:** Materialinventar, BIM/IFC, Gebäuderessourcenpass, EPDs, ÖKOBAUDAT, CDE, Instandhaltungsmanagement, Rückbaukataster, digitale Marktplätze, Vergabe, ESG-/Taxonomie- und Nachhaltigkeitsberichte.

### Inhaltliche Mindestfelder

Ein belastbarer Materialpass für Wiederverwendung sollte mindestens enthalten:

- eindeutige ID und Version,
- Pass-Typ: Material, Produkt, Bauteil, System oder Gebäude,
- Standort und Einbauort,
- Menge, Maße, Gewicht und Einheit,
- Materialzusammensetzung und relevante Schichten,
- Hersteller, Produktname, Charge oder Baujahr, soweit bekannt,
- technische Leistungsmerkmale: Festigkeit, Brandverhalten, Schallschutz, Wärmeleitfähigkeit, Tragfähigkeit oder andere produktspezifische Daten,
- Umweltinformationen: EPD, ÖKOBAUDAT-Verknüpfung, CO₂-/LCA-Daten, Recyclinganteile, Rückbau- und Entsorgungsinformationen,
- Gesundheits- und Schadstoffinformationen: SVHC, Asbest-/PCB-/PAK-/KMF-Risiken, Prüfergebnisse, Beschichtungen,
- Einbau- und Verbindungstechnik,
- Demontageanleitung und benötigte Werkzeuge,
- Wartungs-, Reparatur- und Schadenshistorie,
- Fotos, Pläne, Modellreferenzen,
- Eigentums- und Verantwortlichkeitsinformationen, soweit projektbezogen zulässig,
- Datenquelle, Prüftiefe und Unsicherheiten,
- mögliche Wiederverwendungs-, Reparatur-, Refurbishment-, Recycling- oder Entsorgungswege.

### Abgrenzung und Zusammenspiel mit Materialinventar

Materialinventar und Materialpass sollten nicht konkurrieren, sondern eine Datenkette bilden:

1. **Bestandsaufnahme:** erkennt und verortet Bauteile.
2. **Materialinventar:** strukturiert Mengen und Materialgruppen.
3. **Bauwerksdiagnose / Prüfung:** qualifiziert Zustand und Leistungsfähigkeit.
4. **Materialpass:** bündelt identitäts- und lebenszyklusbezogene Nachweise.
5. **Rückbaukataster:** übersetzt diese Daten in Ausbau-, Los-, Logistik- und Verwertungsprozesse.

Ein Materialpass ohne Inventar sagt wenig über reale Bestandsmengen aus. Ein Inventar ohne Pass sagt wenig über Qualität, Herkunft und zukünftige Einsatzfähigkeit aus.

### Gebäude-, Bauteil- und Produktpässe

Der Begriff Materialpass wird in der Praxis auf verschiedenen Ebenen genutzt:

- **Produktpass:** vom Hersteller für ein Bauprodukt, mit technischen Daten, Materialzusammensetzung, EPD und Rücknahme- oder Recyclinginformationen.
- **Bauteilpass:** für ein konkretes Bauteil oder Bauteillos, etwa Fenster, Träger, Fassadenelemente, Türen oder Doppelbodenplatten.
- **Gebäudepass / Gebäuderessourcenpass:** aggregiert Material-, Emissions- und Kreislaufdaten eines Gebäudes und schafft Transparenz über Ressourcennutzung und Kreislauffähigkeit.
- **Digitaler Produktpass:** regulatorisch im EU-Kontext breiter angelegt; für Bauprodukte ist die konkrete Umsetzung im Wandel und nicht für alle Produktgruppen abschließend geklärt.

## Praxisbezug / Beispiele

- **Neubau mit Kreislaufziel:** Herstellerdaten, EPDs, IFC-Objekte und Montageinformationen werden schon bei Beschaffung als Passdaten angelegt. Spätere Rückbau- und Wiederverwendungsoptionen sind dadurch nicht nur theoretisch, sondern dokumentiert.
- **Bestandsgebäude:** Materialpässe werden nachträglich aus Bestandsaufnahme, Bauteilöffnungen, alten Produktunterlagen und Laborprüfungen aufgebaut. Unsichere Felder bleiben markiert.
- **DGNB Gebäuderessourcenpass:** Dient als Dokumentationsformat, um Materialien, Treibhausgasemissionen und Kreislauffähigkeit eines Gebäudes transparenter zu machen. Er ist besonders anschlussfähig an Nachhaltigkeitsbewertung und Planung.
- **BAMB Materials Passports:** Das EU-Forschungsprojekt beschreibt Materialpässe als Datensätze mit Eigenschaften, die Materialien und Komponenten Wert für Rückgewinnung und Wiederverwendung geben.
- **Madaster:** Plattformansatz, bei dem Gebäudematerialien registriert und in Materialpässe überführt werden, um sie für zukünftige Nutzungen sichtbar zu machen.

## Herausforderungen / offene Fragen

- **Standardisierung:** Es gibt mehrere Passkonzepte, aber noch keine universell durchgesetzte, für alle Bauprodukte verpflichtende Datenstruktur.
- **Aktualisierungspflicht:** Ein Pass verliert Wert, wenn Umbauten, Schäden, Austausch und Wartung nicht fortgeschrieben werden.
- **Datenverantwortung:** Unklar ist häufig, wer Passdaten erstellt, prüft, besitzt, aktualisiert und bei Verkauf oder Rückbau übergibt.
- **Datenqualität im Bestand:** Für alte Bauteile fehlen oft Hersteller, Chargen, Prüfzeugnisse oder Einbaudetails.
- **Vertraulichkeit und Offenheit:** Produktdaten, Preise, Lieferketten und Eigentumsdaten sind teils sensibel, während Kreislaufprozesse offene Schnittstellen benötigen.
- **Rechtliche Wirkung:** Ein Materialpass ersetzt keine Zulassung, keinen statischen Nachweis und keine Schadstofffreigabe. Er kann diese Nachweise nur verlinken oder dokumentieren.
- **Interoperabilität:** Passdaten müssen mit BIM, CDE, Materialinventar, LCA, Marktplätzen und Rückbaukataster kompatibel sein. Proprietäre Plattformen können Lock-in-Risiken erzeugen.
- **Marktanschluss:** Der Pass schafft Information, aber noch keine Nachfrage. Wiederverwendung erfordert zusätzlich Planung, Ausschreibung, Prüfprozesse, Lagerung und Haftungsmodelle.

## Quellen

- BAMB – Buildings As Material Banks: *Materials Passports*. https://www.bamb2020.eu/topics/materials-passports/
- BAMB (2019): *Materials Passports – Best Practice*. https://www.bamb2020.eu/wp-content/uploads/2019/02/BAMB_MaterialsPassports_BestPractice.pdf
- BAMB: *Framework for Materials Passports*. https://www.bamb2020.eu/wp-content/uploads/2018/01/Framework-for-Materials-Passports-for-the-webb.pdf
- DGNB: *Gebäuderessourcenpass*. https://www.dgnb.de/de/nachhaltiges-bauen/zirkulaeres-bauen/gebaeuderessourcenpass
- DGNB: *Zirkularitätsindizes für Bauwerke*. https://www.dgnb.de/de/nachhaltiges-bauen/zirkulaeres-bauen/zirkularitaetsindizes-fuer-bauwerke
- Madaster: *Material Passports for circular construction*. https://madaster.com/material-passport/
- Europäische Kommission: *Level(s) – European framework for sustainable buildings*. https://environment.ec.europa.eu/topics/circular-economy/levels_en
- EN 15804+A2: *Sustainability of construction works — Environmental product declarations — Core rules for the product category of construction products*.
- ISO 14025: *Environmental labels and declarations — Type III environmental declarations*.
- ISO 19650, Normenreihe: Informationsmanagement mit BIM. https://www.iso.org
- Çetin, S. et al. (2023): *Data requirements and availabilities for material passports*. Resources, Conservation & Recycling Advances. https://www.sciencedirect.com/science/article/pii/S2352550923001665
- van Capelleveen, G. et al. (2023): *The anatomy of a passport for the circular economy*. Circular Economy and Sustainability / Elsevier. https://www.sciencedirect.com/science/article/pii/S2667378923000032
