## Verknüpfungen

- **Übergeordnete Themen:** Materialpass; Gebäuderessourcenpass; digitale Gebäudedaten; zirkuläre Bewertung; Portfolioanalyse; ESG; LCA; Restwert.
- **Verwandte Dateien:** `werkzeug/BIM.md`; `werkzeug/IFC_Viewer.md`; `werkzeug/Materialdatenbank.md`; `werkzeug/Concular_Plattform.md`; `dokument/Materialpass.md`; `dokument/Gebäuderessourcenpass.md`; `datenmodell/IFC.md`; `methode/Bauteilkatalogisierung.md`; `methode/Oekobilanzierung.md`; `akteur/Bestandshalter.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Madaster; EPEA; Thomas Rau; Madaster Foundation; IFC; Excel; Material Passport; Circularity Indicator; detachability / demontability; residual value; environmental impact; DGNB; Level(s); EU Taxonomie; Gebäudelogbuch.

## Kurzdefinition

Madaster ist eine digitale Plattform zur Registrierung von Gebäuden, Bauteilen und Materialien als Material- bzw. Gebäudepässe. Die Plattform importiert Gebäudedaten, insbesondere BIM-/IFC-Dateien oder strukturierte Excel-Templates, verknüpft sie mit Material-, Produkt-, Umwelt-, Zirkularitäts- und Wertinformationen und erzeugt daraus Auswertungen zu Materialmassen, Kreislauffähigkeit, Umweltwirkung, Demontierbarkeit und finanziellen Restwerten.

Madaster ist damit weniger ein Marktplatz für den direkten Handel gebrauchter Bauteile als ein **Gebäude- und Materialregister**. Die Plattform macht materielle Bestände sichtbar, bewertbar und berichtsfähig.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung benötigt langfristige Information. Gebäude, die heute errichtet oder saniert werden, sind künftige Materiallager. Madaster adressiert diese Logik, indem Materialien und Produkte digital registriert werden. Dadurch können spätere Umbauten, Rückbauten, Materialpässe, ESG-Berichte und zirkuläre Beschaffungsentscheidungen besser vorbereitet werden.

Relevanz:

- **Bestands- und Neubauerfassung:** Materialien und Produkte werden mengenmäßig registriert.
- **Materialpass:** Gebäudedaten werden in ein dokumentierbares Passformat überführt.
- **Circularity Insights:** Zirkularität, Demontierbarkeit, Rezyklat- bzw. Wiederverwendungsanteile und Materialherkunft können bewertet werden.
- **Environmental Impact:** Umweltkennwerte können Bauteilen und Materialien zugeordnet werden, sofern Datenbasis vorhanden ist.
- **Residual Value:** Materialien werden als Vermögenswerte betrachtet, nicht nur als Abfall.
- **Portfolioebene:** Eigentümer und Kommunen können Gebäudebestände als Materiallager analysieren.
- **Compliance und Zertifizierung:** Daten können für Berichte, ESG, Taxonomie, DGNB oder nationale Anforderungen nutzbar sein.

## Fachinhalt

### Funktionsweise

Madaster arbeitet typischerweise in folgenden Schritten:

1. **Objekt anlegen:** Gebäude oder Portfolio wird in der Plattform registriert.
2. **Quelldaten importieren:** IFC-Dateien oder Madaster-Excel-Templates werden hochgeladen; zusätzliche Dokumente können ergänzen.
3. **Datenqualität prüfen:** Vollständigkeit von Geometrie, Material, Klassifikation und Mengen wird bewertet.
4. **Klassifizieren und verknüpfen:** Bauteile werden Klassifikationen, Materialfamilien, Produkten und Datenbanken zugeordnet.
5. **Aktive Quelldateien festlegen:** Nur aktive Dateien fließen in Berechnungen und Materialpass ein.
6. **Anreichern:** Fehlende Material-, Produkt-, Umwelt-, Zirkularitäts- oder Wertdaten werden ergänzt.
7. **Auswerten:** Plattform erzeugt Materialpass, Materialmassen, Zirkularitätsindikatoren, Umweltwirkung, Restwert und ggf. Zertifizierungsberichte.
8. **Exportieren / Berichten:** Ergebnisse können als Pass, Tabellen oder Berichte genutzt werden; API-Funktionen ermöglichen technische Integration.

### Datentypen

- **Geometrie:** Elementmengen aus IFC; Volumen, Fläche, Länge, Stückzahl.
- **Material:** Materialbeschreibung, Materialfamilie, Schichten, Produkte.
- **Klassifikation:** landes- oder projektspezifische Klassifikationsmethoden, z. B. NL/SfB, DIN 276 je nach Kontext.
- **Phasen:** Neubau, erhaltene Materialien, Rückbau/Demolition, je nach Template und Prozess.
- **Circularity:** Herkunft, Re-Use-Anteil, Recyclinganteil, Demontierbarkeit, erwartete Kreislaufführung.
- **Umwelt:** GWP/CO₂e, Umweltwirkung aus Datenbanken oder Produktinformationen.
- **Finanz:** Materialwert, Residual Value, Preissets, Wertannahmen.
- **Qualität:** Vollständigkeit und Plausibilität der Quelldaten.
- **Dokumente:** IFC, Excel, PDFs, Nachweise, Berichte.

### IFC- und Excel-Logik

Madaster nutzt BIM-/IFC-Modelle bevorzugt, weil daraus Geometrie, Objektstruktur und Mengen automatisiert abgeleitet werden können. Für Bestandsgebäude ohne belastbares BIM kann das Excel-Template verwendet werden. Der Unterschied ist wesentlich:

- **IFC:** ermöglicht 3D-Darstellung, objektbasierte Auswertung und automatisierte Mengenübernahme, benötigt aber saubere Modellierung.
- **Excel:** ermöglicht strukturierte Dateneingabe auch ohne Modell, ist für Audits und Bestand oft pragmatisch, bietet aber keine 3D-Repräsentation.
- **Kombination:** IFC kann durch Excel- oder manuelle Daten ergänzt werden, etwa bei fehlenden Material- oder Produktdaten.

### Materialpass und Circularity Indicator

Der Materialpass dokumentiert Materialmengen, Quelle der Daten, Klassifikationsmethoden, verwendete Datenbanken und Auswertungen. Der Circularity Indicator ist eine Plattformbewertung, die verschiedene Material- und Produktinformationen zusammenführt. Für Forschungszwecke ist wichtig: Ergebnisse hängen stark von Datenqualität, Modellierungsgrad, Klassifikationsmapping, Datenbankabdeckung und Plattformannahmen ab.

### Plattform als Dateninfrastruktur

Madaster kann als Infrastruktur zwischen folgenden Ebenen verstanden werden:

- **Gebäudeebene:** einzelner Materialpass.
- **Portfolioebene:** Eigentümer, Banken, Versicherungen, Kommunen oder Bestandshalter analysieren viele Objekte.
- **Produktdatenebene:** Hersteller und Datenanbieter liefern Produktinformationen.
- **Regulatorische Ebene:** Berichte und Nachweise für ESG, Taxonomie, Zertifizierung oder nationale Vorgaben.
- **Künftiger Markt:** registrierte Materialien werden potenziell für spätere Wiederverwendung sichtbar, aber der Handel selbst ist nicht der primäre Plattformkern.

### Schnittstellen

- **IFC2x3 / IFC4:** Hauptschnittstelle für BIM-Import.
- **Madaster Excel Template:** strukturierter Import für Bestands- und Projektdaten.
- **API:** technische Interaktion mit Plattformressourcen; Funktionsumfang abhängig von Plattformversion und Berechtigung.
- **Datenbanken:** Produkt-, Material-, Umwelt- und Preisdatensätze; nutzbar je nach Land, Lizenz und Datenverfügbarkeit.
- **Exportformate:** Materialpass, Excel/PDF-Berichte, ggf. Datenauszüge.
- **IFC-Viewer-Prüfung:** BIMcollab ZOOM und Madaster Smart Views werden zur IFC-Vorprüfung empfohlen.

### Nutzen

- Strukturierter Einstieg in Gebäudematerialpässe.
- Verknüpfung von Mengen, Umweltwirkung, Zirkularität und Restwert.
- Nutzbar für Neubau, Sanierung, Bestand und Portfolio.
- Stärkt die Sichtweise von Gebäuden als Materialbanken.
- Kann Anforderungen von Zertifizierung, Berichtswesen und Beschaffung unterstützen.
- Verbindet BIM-Daten und tabellarische Daten in einem Passsystem.

### Grenzen

- Qualität der Ergebnisse hängt von Quellmodell, Klassifikation und Datenpflege ab.
- Viele Bestandsgebäude haben keine ausreichenden digitalen Daten.
- Verdeckte Schichten, Schadstoffe, reale Zustände und Verbindungen müssen extern erhoben werden.
- Plattformlogiken, Indikatoren und Datenbanken können proprietär oder länderspezifisch sein.
- Ein Materialpass bedeutet nicht automatisch, dass Bauteile technisch, rechtlich oder wirtschaftlich wiederverwendbar sind.
- Langfristige Datenhaltung über Jahrzehnte ist organisatorisch und wirtschaftlich ungeklärt.
- Der reale Wiedereinbau nach Rückbau muss gesondert nachverfolgt werden.

## Praxisbezug / Beispiele

- **Neubau mit BIM:** Planende exportieren IFC, prüfen Klassifikation und Base Quantities, laden das Modell hoch und erzeugen einen Materialpass. Frühzeitige Modellierungsregeln verbessern die Qualität.
- **Bestandsgebäude ohne BIM:** Ein Audit erfasst Materialien in Excel. Die Plattform kann daraus Mengen und Pässe ableiten, aber keine vollständige 3D-Struktur erzeugen.
- **Portfolio eines Bestandshalters:** Gebäude werden registriert, um Materialmassen, CO₂- und Restwertpotenziale sichtbar zu machen. Das ist nützlich für ESG- und Transformationsstrategien.
- **Zertifizierung / DGNB:** Material- und Ressourceninformationen können als Grundlage für Nachweise dienen, müssen aber mit den konkreten Zertifizierungsanforderungen abgeglichen werden.
- **Rückbauvorbereitung:** Madaster-Daten können Hinweise auf Materialmengen geben; für direkte Wiederverwendung sind zusätzlich Zustand, Demontierbarkeit, Schadstoffe, Markt und Logistik zu prüfen.

## Herausforderungen / offene Fragen

- Wie offen und exportierbar sind Gebäudematerialdaten langfristig?
- Welche Indikatoren sind transparent genug für wissenschaftliche Vergleiche?
- Wie werden proprietäre Datenbanken, nationale Klassifikationen und offene Standards ausbalanciert?
- Wie lassen sich Bauteilzustand und Demontagefähigkeit belastbar in die Plattform integrieren?
- Wer aktualisiert Materialpässe nach Umbauten, Reparaturen oder Nutzungsänderungen?
- Wie wird aus Materialregistrierung tatsächliche Wiederverwendung?
- Welche Datenanforderungen sollten Auftraggeber früh in BIM-/IFC-Modellen verankern?
- Wie werden sensible Portfolio- und Gebäudedaten geschützt?

## Quellen

- Madaster: How it works, https://madaster.com/how-it-works/
- Madaster Documentation: Material passports, https://docs.madaster.com/us/en/knowledge-base/material-passports
- Madaster Documentation: Set up objects, https://docs.madaster.com/us/en/get-started/set-up-objects
- Madaster Documentation: Preparing BIM IFC source files, https://docs.madaster.com/us/en/knowledge-base/preparing-bim-ifc-source-files
- Madaster Documentation: Dossier / source files, https://docs.madaster.com/us/en/platform-pages/building/files.html
- Madaster Documentation: API, https://docs.madaster.com/us/en/api/
- Madaster Documentation: Databases and products, https://docs.madaster.com/us/en/knowledge-base/databases
- Madaster Circularity Indicator Explained, https://docs.madaster.com/files/en/Madaster%20-%20Circularity%20Indicator%20explained.pdf
- HOUSEFUL project: BIM Models and Material Passport in Madaster, https://houseful.eu/
- Platform CB’23: Passports for the Construction Sector, https://platformcb23.nl/
