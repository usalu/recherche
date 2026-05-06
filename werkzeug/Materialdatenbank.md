---
type: Werkzeug
---

## Verknüpfungen

- **Übergeordnete Themen:** Dateninfrastruktur; Ökobilanzierung; Materialpass; Produktdaten; LCA; zirkuläre Bewertung; Kennwerte.
- **Verwandte Dateien:** `werkzeug/BIM.md`; `werkzeug/Madaster_Plattform.md`; `werkzeug/Concular_Plattform.md`; `werkzeug/IFC_Viewer.md`; `dokument/EPD.md`; `dokument/Materialpass.md`; `datenmodell/Materialkennwerte.md`; `methode/Oekobilanzierung.md`; `methode/Bauteilbewertung.md`; `standard/EN_15804.md`; `standard/ISO_14040.md`; `standard/ISO_14044.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** ÖKOBAUDAT; IBU; EPD International; INIES; EC3; One Click LCA; Madaster-Datenbanken; Herstellerdatenbanken; EN 15804; ISO 14025; ISO 14040/14044; LCA; DGNB; Level(s); CPR / Bauprodukteverordnung; Digital Product Passport.

## Kurzdefinition

Eine Materialdatenbank ist eine strukturierte Sammlung von Daten zu Materialien, Bauprodukten oder Bauteilen. Sie kann Umweltkennwerte, technische Eigenschaften, Produktinformationen, Mengenbezüge, Preise, Schadstoffinformationen, Recyclinganteile, Herkunftsdaten, EPDs, Verfügbarkeiten oder Wiederverwendungskriterien enthalten.

Für Wiederverwendung ist „Materialdatenbank“ kein einheitlicher Werkzeugtyp. Es gibt unterschiedliche Datenbankklassen:

- **LCA-Datenbanken:** Umweltwirkungen von Materialien und Produkten.
- **EPD-Datenbanken:** hersteller- oder produktspezifische Umweltproduktdeklarationen.
- **Produktdatenbanken:** technische Daten, Hersteller, Leistungserklärungen, Abmessungen.
- **Materialpass-Datenbanken:** Gebäude-, Bauteil- und Produktinformationen im Lebenszyklus.
- **Markt-/Plattformdatenbanken:** konkrete verfügbare wiederverwendbare Bauteile.
- **Forschungsdatenbanken:** Materialflüsse, Gebäudetypologien, Urban Mining, Kennwerte.

## Relevanz für Wiederverwendung im Bauwesen

Materialdatenbanken liefern die Vergleichs- und Bewertungsgrundlage für Re-Use-Entscheidungen. Ohne verlässliche Kennwerte lassen sich CO₂-Einsparungen, Schadstoffrisiken, technische Eignung, Kreislaufpotenziale, Kosten und Nachweise kaum belastbar bestimmen.

Relevanz:

- **Ökologische Bewertung:** Vergleich von Wiederverwendung, Recycling, Neuprodukt und Entsorgung.
- **Materialpass:** Anreicherung von BIM- oder Auditdaten mit Umwelt- und Produktkennwerten.
- **Bauteilauswahl:** Identifikation geeigneter Materialgruppen und kritischer Eigenschaften.
- **Nachweisführung:** Unterstützung für DGNB, Level(s), ESG, Gebäuderessourcenpass und LCA.
- **Risikoanalyse:** Hinweise auf Schadstoffe, normative Anforderungen und Prüfbedarf.
- **Markttransparenz:** Vergleich von Mengen, Qualitäten, Preisen und Verfügbarkeiten, sofern Marktdaten vorhanden sind.

## Fachinhalt

### Zentrale Datenarten

- **Identifikationsdaten:** Materialname, Produktname, Hersteller, Typ, Normbezug, Klassifikation, EPD-Nummer.
- **Technische Eigenschaften:** Dichte, Festigkeit, Brandverhalten, Wärmeleitfähigkeit, Schallschutz, Feuchteverhalten, Dauerhaftigkeit, Maße.
- **Umweltkennwerte:** GWP, Primärenergie, Versauerung, Eutrophierung, Ozonabbau, Ressourcenverbrauch, Abfall, Wasser, Module A1-C4/D nach EN 15804.
- **Zirkularitätsdaten:** Recyclinganteil, Re-Use-Anteil, Demontierbarkeit, Trennbarkeit, Schadstofffreiheit, Rücknahmesysteme.
- **Gesundheit / Schadstoffe:** VOC, Asbest, PCB, PAK, Schwermetalle, Flammschutzmittel, Biozide; meist nicht vollständig in generischen Datenbanken.
- **Wirtschaftsdaten:** Preis, Restwert, Entsorgungskosten, Aufbereitungskosten, Transportkosten.
- **Geografische Daten:** Produktionsregion, Datensatzregion, Transportannahmen, nationale Strommixe.
- **Datenqualität:** Quelle, Jahr, Gültigkeit, Repräsentativität, Unsicherheit, Verifizierungsstatus.

### Typen von Materialdatenbanken

#### ÖKOBAUDAT

Deutsche Datenbank für ökobilanzielle Baustoff- und Bauproduktdaten. Sie ist zentral für BNB, DGNB-Workflows und LCA in Deutschland. Enthält generische und spezifische Datensätze, die nach Normkontexten wie EN 15804 verwendet werden. Für Re-Use ist sie wichtig als Referenz für Neuproduktvergleiche und Ökobilanzierung, enthält aber nicht automatisch konkrete gebrauchte Bauteile.

#### EPD-Datenbanken

EPD-Programme wie IBU, EPD International oder nationale Datenbanken stellen verifizierte Umweltproduktdeklarationen bereit. Sie sind produktspezifischer als generische Datensätze, aber für gebrauchte Bauteile nur eingeschränkt direkt anwendbar, weil Zustand, Restlebensdauer, Ausbau, Transport und Aufbereitung separat zu bilanzieren sind.

#### INIES

Französische Datenbank für Umwelt- und Gesundheitsdeklarationen von Bauprodukten und Gebäudetechnik. Relevant für französische Bewertungs- und Regulierungskontexte.

#### EC3

EC3 ist ein Tool und eine Datenbank zur Bewertung von Embodied Carbon, besonders für Materialbeschaffung und Vergleich von EPDs. Relevanz vor allem für CO₂-orientierte Auswahl und Beschaffung, weniger für vollständige Re-Use-Logistik.

#### Plattform- und Passdatenbanken

Madaster, Concular und andere Plattformen nutzen Datenbanken, um konkrete Gebäude- oder Bauteildaten mit Umwelt-, Zirkularitäts- oder Marktdaten zu verknüpfen. Hier entsteht die Brücke zwischen allgemeinem Materialkennwert und konkretem Objekt.

### Datenbanklogik für Wiederverwendung

Für Re-Use reicht ein einzelner Umweltkennwert nicht aus. Nötig ist eine Kombination:

1. **Referenzprodukt:** Was würde ohne Wiederverwendung neu produziert?
2. **Restlebensdauer:** Wie lange kann das gebrauchte Bauteil noch genutzt werden?
3. **Funktionale Äquivalenz:** Erfüllt es dieselbe Funktion und Qualität?
4. **Zusatzaufwand:** Ausbau, Sortierung, Reinigung, Prüfung, Reparatur, Transport, Lagerung.
5. **Verlustquote:** Bruch, Beschädigung, nicht nutzbare Mengen.
6. **Nachweisfähigkeit:** technische, rechtliche und bauaufsichtliche Anforderungen.
7. **Systemgrenze:** Welche Lebenszyklusmodule werden berücksichtigt?
8. **Datenqualität:** generisch, projektspezifisch, herstellerbezogen, gemessen oder geschätzt.

### Schnittstellen

- **BIM / IFC:** Bauteile, Mengen und Materialien aus Modellen.
- **Excel / CSV:** häufigste Austauschform für Materiallisten, LCA-Importe und Audits.
- **EPD-Formate:** maschinenlesbare EPDs, InData, ILCD+EPD, openEPD je nach Ökosystem.
- **APIs:** Anbindung an LCA-Tools, Materialpässe, Beschaffungssysteme und Plattformen.
- **Klassifikationen:** DIN 276, eBKP, Uniclass, Omniclass, NL/SfB, ETIM, bSDD.
- **Dokumente:** EPD-PDFs, Sicherheitsdatenblätter, Leistungserklärungen, Prüfzeugnisse.

### Kriterien für belastbare Nutzung

- Datensatz muss zur Region und Zeit passen.
- Systemgrenzen und Module müssen klar sein.
- Funktionale Einheit muss mit dem Vergleich übereinstimmen.
- Generische Daten dürfen nicht wie produktspezifische Daten behandelt werden.
- Wiederverwendung darf nicht automatisch mit Null-Emissionen angesetzt werden; Ausbau, Transport, Prüfung und Aufbereitung sind zu berücksichtigen.
- Modul D und Gutschriften müssen transparent ausgewiesen werden.
- Datenbanken mit proprietären Algorithmen sollten nur mit dokumentierten Annahmen zitiert werden.
- Unsicherheit und Datenlücken müssen explizit markiert werden.

## Praxisbezug / Beispiele

- **Vergleich Re-Use-Tür vs. Neutür:** Neuproduktdaten aus EPD/ÖKOBAUDAT werden mit Aufwand für Demontage, Transport, Aufbereitung, Beschlagsprüfung und Wiedereinbau verglichen.
- **Stahlträger:** EPD- oder generische Stahldaten zeigen hohe Herstellungsenergie. Wiederverwendung kann ökologisch attraktiv sein, aber Prüfung, Rückverfolgbarkeit und Transport sind entscheidend.
- **Ziegel:** Wiederverwendung spart Brennprozess, benötigt aber Mörtelentfernung, Sortierung und Bruchverluste. Datenbankwerte müssen mit realen Aufbereitungsdaten ergänzt werden.
- **Madaster:** Materialdatenbank und Gebäudedaten werden gekoppelt, um Massen, Umweltwirkung und Restwert zu berechnen.
- **BIM-LCA:** Mengen aus IFC werden mit ÖKOBAUDAT- oder EPD-Daten verknüpft. Fehler im Materialmapping können Ergebnisse stark verzerren.
- **Beschaffung:** EPD-Datenbanken helfen, Neuprodukte mit niedrigerem CO₂-Fußabdruck zu wählen; Re-Use-Angebote brauchen zusätzliche Zustands- und Verfügbarkeitsdaten.

## Herausforderungen / offene Fragen

- Wie werden gebrauchte Bauteile als eigene Datensatzkategorie in LCA-Datenbanken abgebildet?
- Welche Allokationsregeln gelten zwischen Erstnutzung, Rückbau, Wiederverwendung und späterer Entsorgung?
- Wie wird Restlebensdauer zuverlässig abgeschätzt?
- Wie können Materialdatenbanken technische Eignung, Schadstoffe und Demontierbarkeit integrieren?
- Wie werden regionale Unterschiede bei Strommix, Transport, Entsorgung und Markt ersetzt?
- Wie lässt sich Datenqualität für kleine, heterogene Re-Use-Chargen wirtschaftlich erfassen?
- Wie werden maschinenlesbare EPDs, BIM, Materialpässe und digitale Produktpässe interoperabel?
- Wie wird verhindert, dass CO₂-Kennwerte andere Re-Use-Kriterien wie Toxizität, Reparierbarkeit oder soziale Aspekte verdrängen?

## Quellen

- ÖKOBAUDAT: Informationsportal Nachhaltiges Bauen / BMWSB-BBSR, https://www.oekobaudat.de/
- Institut Bauen und Umwelt e.V. (IBU): EPD-Programm, https://ibu-epd.com/
- The International EPD System: EPD Library, https://www.environdec.com/
- INIES: Base nationale des données environnementales et sanitaires, https://www.inies.fr/
- EC3 – Embodied Carbon in Construction Calculator, https://buildingtransparency.org/ec3/
- EN 15804: Sustainability of construction works — Environmental product declarations — Core rules for the product category of construction products.
- ISO 14025: Environmental labels and declarations — Type III environmental declarations.
- ISO 14040 / ISO 14044: Life cycle assessment principles, framework, requirements and guidelines.
- DGNB: Gebäuderessourcenpass und zirkuläres Bauen, https://www.dgnb.de/
- European Commission: Level(s) framework, https://environment.ec.europa.eu/topics/circular-economy/levels_en
- InData Network: International open data network for sustainable building, https://www.indata.network/
