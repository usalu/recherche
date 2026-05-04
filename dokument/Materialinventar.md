## Verknüpfungen

- **Übergeordnete Themen:** Urban Mining, Ressourcenerfassung, Materialflüsse, Kreislaufwirtschaft, Bestandsdaten, Rückbauplanung, Wiederverwendung, Recycling, Ökobilanzierung.
- **Verwandte Dateien:** `dokument/Bestandsaufnahme.md`, `dokument/Materialpass.md`, `dokument/Rueckbaukataster.md`, `dokument/Pre_Demolition_Audit.md`, `dokument/Bauwerksdiagnose.md`, `dokument/Auditbericht.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Bauherrschaft, Bestandshalter, BIM-Management, Ökobilanzierung, Rückbauplanung, Schadstoffgutachter:innen, Entsorger, Reuse-Plattformen, IÖR-Materialkataster, Madaster, DGNB Gebäuderessourcenpass, BAMB, DIN SPEC 91484, Level(s), ÖKOBAUDAT, EN 15804, AVV/EAK-Abfallcodes, IFC; `methode/` für Mengenermittlung, Bauteilklassifikation, Materialmapping, Datenqualitätsstufen; `prozessphase/` für Grundlagenermittlung, Vorplanung, Rückbauvorbereitung, Ausschreibung; `pruefung/` für Stoffprüfung, Schadstoffprüfung, Produktidentifikation; `datenmodell/` für Bauteil-ID, Materiallayer, Klassifikationen, BIM/IFC, Tabellenstruktur; `logistik/` für Losbildung, Ausbau, Lagerung, Transport und Verwertungsketten.

## Kurzdefinition

Ein **Materialinventar** ist ein strukturiertes Verzeichnis der in einem Gebäude, Bauteil, Areal oder Portfolio vorhandenen Materialien, Bauteile und Mengen zu einem bestimmten Zeitpunkt. Es beantwortet primär: **Was ist wo in welcher Menge und mit welcher Datenqualität vorhanden?**

Das Materialinventar ist klar vom **Materialpass** zu unterscheiden. Das Inventar ist eine objekt- und standortbezogene Erfassung des aktuellen Bestands. Der Materialpass ist ein fortschreibbarer, stärker lebenszyklus- und identitätsbezogener Datensatz für Materialien, Produkte, Bauteile oder Gebäude, der Eigenschaften, Herkunft, Kreislauffähigkeit, Nachweise und zukünftige Nutzungsmöglichkeiten dokumentiert. Kurz: Das Materialinventar ist die Mengen- und Ortsgrundlage; der Materialpass ist der qualifizierte Informations- und Nachweiscontainer.

## Relevanz für Wiederverwendung im Bauwesen

Materialinventare machen den Gebäudebestand als Rohstoff- und Bauteillager sichtbar. Sie schaffen die Grundlage für:

- Erhaltungs- und Umbauentscheidungen,
- Identifikation wiederverwendungsfähiger Bauteile,
- Mengen- und Terminplanung für selektiven Rückbau,
- Materialfluss- und CO₂-Bilanzierung,
- Ausschreibung von Reuse-Losen,
- Prüfung von Recycling- und Entsorgungswegen,
- Aufbau von Materialpässen und Gebäuderessourcenpässen,
- regionale Urban-Mining-Strategien.

Für Wiederverwendung ist die räumliche Verortung entscheidend. Eine reine Massenbilanz „10 t Stahl“ reicht nicht. Nötig ist die Zuordnung zu konkreten Bauteilen, Geschossen, Achsen, Befestigungen, Zuständen, Ausbaubedingungen und Prüfbedarfen.

## Fachinhalt

### Dokumenttyp

- **Zweck:** Strukturierte, auswertbare Erfassung von Materialien, Bauteilen und Mengen als Grundlage für Planung, Rückbau, Wiederverwendung, Recycling, Ökobilanz und Ressourcenbewertung.
- **Inhalt:** Material- und Bauteillisten, Mengen, Einheiten, Positionen, Bauteil-IDs, Materialgruppen, Schichten, Produktinformationen, Zustand, Schadstoffhinweise, Demontierbarkeit, Datenquelle, Datenqualität, potenzielle Anschlussnutzung.
- **Autorenschaft:** BIM-/Datenmanagement, Architekt:innen, Fachplaner:innen, Rückbauplanung, Mengenermittlung, Auditor:innen; Qualitätssicherung durch Fachgutachten für Schadstoffe, Tragwerk oder Produktleistung.
- **Einsatzzeitpunkt:** Früh als vorläufiges Inventar aus Bestandsaufnahme und Plänen; verfeinert durch Diagnose, Bauteilöffnungen, Pre-Demolition Audit und Rückbau; fortgeschrieben im Betrieb oder nach Umbauten.
- **Mindestinhalte:** Objekt-ID, Bauteil-ID, Ort, Materialgruppe, Bauteiltyp, Menge, Einheit, Erfassungsmethode, Datenqualität, Zustand, Schadstoffstatus, Wiederverwendungs-/Recyclinghinweis, Foto-/Planbezug, Bearbeitungsdatum.
- **Datenlogik:** Objekt → Zone/Raum → System/Bauteil → Materialschicht/Produkt → Menge → Qualität/Zustand → Risiko → Anschlussoption. Die Struktur sollte Export in Tabellen, BIM, Materialpass und Rückbaukataster ermöglichen.
- **Anschlussfähigkeit:** Materialpass, Gebäuderessourcenpass, Rückbaukataster, Pre-Demolition Audit, Ausschreibung, Materialmarktplatz, LCA, Kosten- und Terminplanung, Abfallbilanz, CDE/BIM.

### Abgrenzung: Materialinventar vs. Materialpass

| Aspekt | Materialinventar | Materialpass |
|---|---|---|
| Hauptfrage | Was ist wo und wie viel vorhanden? | Welche Identität, Qualität und Kreislauffähigkeit hat ein Material/Bauteil über den Lebenszyklus? |
| Bezug | Gebäude, Areal, Portfolio, Bauabschnitt | Produkt, Bauteil, Material, Gebäude oder Ressourcenpaket |
| Zeitpunkt | Zustand zu einem Erfassungszeitpunkt | fortschreibbar über Planung, Bau, Betrieb, Umbau, Rückbau |
| Detailtiefe | Mengen, Orte, Bauteiltypen, Materialgruppen, Zustände | Herkunft, Zusammensetzung, technische Daten, Umweltinformationen, Prüfungen, Wartung, Demontage, Kreislaufoptionen |
| Funktion | Planungs- und Mengengrundlage | Nachweis-, Informations- und Wertträger |
| Typische Ausgabe | Tabelle, Modell, Katasterauszug, Massenbilanz | digitaler Pass, Gebäuderessourcenpass, Produktdatenblatt, Datenobjekt |
| Risiko bei Verwechslung | Mengen werden als geprüfte Qualität missverstanden | Pass bleibt ohne reale Mengen- und Ortsgrundlage abstrakt |

### Mindestdatenfelder

Ein projektbezogenes Materialinventar sollte mindestens folgende Felder enthalten:

- eindeutige ID,
- Gebäude/Teilgebäude/Geschoss/Raum/Achse,
- Bauteilkategorie und Bauteilname,
- Materialgruppe und, soweit bekannt, Materialart,
- Menge und Einheit mit Mengenermittlungsmethode,
- Abmessungen oder Schichtaufbau,
- Erfassungsquelle: Plan, Sichtprüfung, Scan, Öffnung, Labor, Herstellerdaten,
- Datenqualitätsstufe und Unsicherheit,
- Zustand und Beschädigungen,
- Verbindung und Demontierbarkeit,
- Schadstoffverdacht oder geprüfter Schadstoffstatus,
- Wiederverwendungs-, Reparatur-, Recycling- oder Entsorgungsoption,
- notwendige Folgeprüfung,
- Foto, Planbezug, Modellreferenz,
- Bearbeitungsdatum und Verantwortliche.

### Datenqualitätslogik

Für Wiederverwendung ist es problematisch, wenn geschätzte Mengen und geprüfte Bauteile in derselben Tabelle gleichwertig erscheinen. Daher sollte das Inventar Datenqualität ausweisen:

- **Q0 – Annahme:** typologische Schätzung, keine Objektprüfung.
- **Q1 – Planbasiert:** aus Bestands- oder Ausführungsplan übernommen.
- **Q2 – Vor Ort sichtbar:** visuell bestätigt und fotografiert.
- **Q3 – Vermessen/modelliert:** geometrisch oder mengenmäßig erhoben.
- **Q4 – geöffnet/geprüft:** Schicht, Material oder Bauteil durch Öffnung/Probe bestätigt.
- **Q5 – qualifiziert:** technische Leistung, Schadstoffstatus oder Produktdaten nachgewiesen.

### Verhältnis zu regionalen Materialkatastern

Regionale oder nationale Materialkataster wie das IÖR-Materialkataster liefern strategische, typisierte Informationen über Materialmengen im Gebäudebestand. Sie sind wertvoll für Stadt- und Ressourcenplanung, ersetzen aber kein projektbezogenes Materialinventar. Für Wiederverwendung einzelner Bauteile braucht es objektbezogene Daten zu Ort, Zustand, Demontierbarkeit, Schadstoffen und Zeitfenstern.

## Praxisbezug / Beispiele

- **Projektinventar vor Umbau:** Aus Laserscan, Bestandsplänen und Begehung entsteht eine Tabelle mit Bauteilen und Materialien. Sichtbare Reuse-Kandidaten werden markiert, unsichtbare Schichten als unbekannt gekennzeichnet.
- **Materialinventar für Rückbau:** Das Inventar wird um AVV-Codes, Schadstoffstatus, Verwertungswege und Reuse-Lose ergänzt. Es bildet die Datengrundlage für Rückbaukataster und Ausschreibung.
- **Inventar für Ökobilanz:** Mengen aus dem Inventar werden mit ÖKOBAUDAT- oder EPD-Datensätzen verknüpft. Zu beachten ist, dass Umweltwirkungen nicht automatisch Wiederverwendungsfähigkeit bedeuten.
- **Portfolio-Inventar:** Eigentümer:innen erfassen mehrere Gebäude nach einheitlicher Klassifikation, um Sanierungs-, Rückbau- und Reuse-Potenziale strategisch zu priorisieren.
- **Bauteilbörse:** Wiederverwendungsfähige Lose aus dem Inventar werden mit Fotos, Abmessungen, Mengen, Ausbauzeitpunkt und Kontakt in Marktplätze überführt.

## Herausforderungen / offene Fragen

- **Datenlücken im Bestand:** Baualter, Umbauten und fehlende Herstellerinformationen erschweren genaue Materialidentifikation.
- **Schichtaufbauten:** Verdeckte Materialien sind oft erst nach Öffnung oder Rückbau erkennbar.
- **Mengengenauigkeit:** Modellmengen, Planmengen und Rückbaumengen können deutlich abweichen.
- **Schadstoffe:** Ein Inventar ohne Schadstoffstatus kann Wiederverwendung suggerieren, obwohl Ausschleusung nötig ist.
- **Klassifikationen:** Unterschiedliche Systeme für Bauteile, Materialien, Kosten, Abfall und BIM erschweren Datenaustausch.
- **Marktbezug:** Wiederverwendungspotenzial hängt von Nachfrage, Lagerung, Ausbaukosten, Zeitfenster und Prüfkosten ab; das Inventar allein entscheidet nicht.
- **Aktualisierung:** Sobald Bauteile ausgebaut, beschädigt, verkauft oder entsorgt werden, muss das Inventar fortgeschrieben werden.

## Quellen

- BAMB – Buildings As Material Banks: *Materials Passports*. https://www.bamb2020.eu/topics/materials-passports/
- BAMB (2019): *Materials Passports – Best Practice*. https://www.bamb2020.eu/wp-content/uploads/2019/02/BAMB_MaterialsPassports_BestPractice.pdf
- DGNB: *Gebäuderessourcenpass*. https://www.dgnb.de/de/nachhaltiges-bauen/zirkulaeres-bauen/gebaeuderessourcenpass
- DIN SPEC 91484:2023-09: *Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen des Anschlussnutzungspotentials vor Abbruch- und Renovierungsarbeiten*. https://www.dinmedia.de/de/technische-regel/din-spec-91484/371235753
- Europäische Kommission (2024): *EU Construction & Demolition Waste Management Protocol including guidelines for pre-demolition and pre-renovation audits*. https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- FCRBE / Interreg NWE: *A guide for identifying the reuse potential of construction products*. https://vb.nweurope.eu/media/10132/en-fcrbe_wpt2_d12_a_guide_for_identifying_the_reuse_potential_of_construction_products.pdf
- Leibniz-Institut für ökologische Raumentwicklung: *Materialkataster Deutschland / IÖR-Materialkataster*. https://www.ioer.de
- Madaster: *Material Passports for circular construction*. https://madaster.com/material-passport/
- EN 15804+A2: *Sustainability of construction works — Environmental product declarations — Core rules for the product category of construction products*.
- ÖKOBAUDAT: Datenbank für Umweltproduktdaten im Bauwesen. https://www.oekobaudat.de
