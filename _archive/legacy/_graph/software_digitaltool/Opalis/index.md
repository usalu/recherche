---
id: "Opalis"
entity: "software_digitaltool"
node_kind: "core"
migration_status: "migrated_phase3_core_entities"
title: "Opalis"
source_count: 3
legacy_paths:
  - "dokument\\Opalis_Datenbank.md"
  - "fallstudie\\Opalis.md"
  - "werkzeug\\Opalis_Plattform.md"
raw_targets:
  - "software_digitaltool/Opalis"
  - "software_digitaltool/Opalis_Plattform"
migration_actions:
  - "keep_or_split_case"
  - "move_as_knot"
  - "semantic_move"
risk_flags:
  - "may_duplicate_bauteilboerse_or_akteur"
---
# Opalis

## Migration

- Canonical target: software_digitaltool/Opalis
- Legacy source count: 3
- Semantic note: Digitales Werkzeug oder Plattform. Bauteilboersen werden hier als Plattformprofile gefuehrt, nicht als eigene Entitaet.

## Legacy Content

### Legacy Source: fallstudie\Opalis.md

- Map action: keep_or_split_case
- Target role in map: primary
- Raw mapped target: software_digitaltool/Opalis
- Original primary target: software_digitaltool/Opalis
- Original secondary targets: fallstudie/Opalis_Plattformfall

---
type: Fallstudie
logistik: ["[[logistik/Transport]]", "[[logistik/Zwischenlagerung]]"]
verwandt: ["[[fallstudie/CRCLR_House]]", "[[fallstudie/Haus_der_Materialisierung]]", "[[fallstudie/Kunst_Stoffe_Berlin]]"]
---

## Verknüpfungen

- **Übergeordnete Themen**
  - Fallstudien / Marktplätze
  - Bauteilwiederverwendung
  - Wiederverwendungsplattformen
  - Materialkatalogisierung
  - Re-Use-Baustoffhandel
  - Zirkuläre Beschaffung
  - Rückbau- und Wiederverwendungslogistik
- **Verwandte Dateien**
  - `fallstudie/CRCLR_House.md`
  - `fallstudie/Haus_der_Materialisierung.md`
  - `fallstudie/Kunst_Stoffe_Berlin.md`
  - `akteur/Rotor.md`
  - `akteur/RotorDC.md`
  - `akteur/Bellastock.md`
  - `akteur/Atelier_4_5.md`
  - `akteur/Salvo.md`
  - `akteur/Build_Reuse.md`
  - `werkzeug/Bauteilkatalog.md`
  - `werkzeug/Materialpass.md`
  - `werkzeug/ReUse_Audit.md`
  - `werkzeug/Reuse_Rate.md`
  - `werkzeug/Haendlerverzeichnis.md`
  - `dokument/FCRBE_Material_Sheets.md`
  - `dokument/FCRBE_Procurement_Strategies.md`
  - `dokument/FCRBE_Reclamation_Audit.md`
  - `dokument/Product_or_Waste.md`
  - `logistik/Rueckbau.md`
  - `logistik/Demontage.md`
  - `logistik/Aufbereitung.md`
  - `logistik/Transport.md`
  - `logistik/Zwischenlagerung.md`
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
  - Akteure: Rotor vzw/asbl, Bellastock, Atelier 4/5, Bruxelles Environnement, OVAM, ADEME, Région Île-de-France, Interreg North-West Europe, FCRBE, PREUSE, professionelle Re-Use-Händler.
  - Fallstudientyp: **Plattform-/Marktplatz-Fallstudie** und Katalogisierungsmodell, nicht lokales Werkstattzentrum und nicht Gebäude.
  - Materialien: wiedergewonnene Bauelemente aus Rückbau, u. a. Holztragwerk, Stahl, Ziegel, Naturstein, Dachziegel, Fenster, Türen, Treppen, Parkett, Fliesen, Büroausbau, Sanitärobjekte, Radiatoren, Leuchten, Metallbauteile, architektonische Antiquitäten.
  - Methoden: Händlerverzeichnis, Materialsteckbriefe, Projektbeispiele, technische Dokumentation, Wiederverwendungs-Audits, Beschaffungsstrategien, Quotenmethodik, Versicherungs- und Risikodokumentation, Produkt-vs.-Abfall-Kriterien.

## Kurzdefinition

Opalis ist eine digitale Plattform für wiedergewonnene Baumaterialien und professionelle Re-Use-Händler. Sie wurde von Rotor gegründet und dient dazu, Wiederverwendung im Bauwesen planbarer zu machen. Opalis ist kein einzelner Online-Shop, sondern ein Katalogisierungs- und Vermittlungsmodell: Die Plattform zeigt Händler, Materialkategorien, typische Verfügbarkeiten, technische Informationen, Beispielprojekte und Dokumente zu Beschaffung, Rückbau, Audits, Versicherungsfragen und Wiederverwendungsquoten.

Die Plattform begann mit einem Fokus auf Händler im Umfeld von Brüssel und wurde später auf Belgien, Frankreich und die Niederlande ausgeweitet. Zwischen 2019 und 2023 wurde sie im Rahmen des Interreg-NWE-Projekts FCRBE weiterentwickelt; seit 2024–2027 wird sie im Kontext des PREUSE-Projekts von Rotor und Bellastock weiter gepflegt. Für den deutschsprachigen Forschungsstand ist Opalis besonders wichtig, weil es zeigt, wie Marktwissen, Händlerwissen und technische Dokumentation in eine wiederverwendungsfähige Planungsinfrastruktur übersetzt werden können.

## Relevanz für Wiederverwendung im Bauwesen

Opalis adressiert ein strukturelles Problem der Wiederverwendung: Materialien sind vorhanden, aber schwer auffindbar, schwer vergleichbar und für Planer:innen oft nicht verlässlich genug dokumentiert. Die Plattform reduziert diese Such- und Informationskosten.

Relevanzpunkte:

- **Sichtbarkeit professioneller Händler:** Wiedergewonnene Materialien zirkulieren häufig informell. Opalis macht professionelle Händler sichtbar und beschreibt ihre Spezialisierungen und Dienstleistungen.
- **Katalog statt Einzelfund:** Der Nutzen liegt nicht nur in einzelnen Produkten, sondern in Kategorien, Marktlogik und wiederkehrenden Materialtypen.
- **Verknüpfung von Material und Dienstleistung:** Händler bieten nicht nur Ware, sondern oft Demontage, Reinigung, Zuschnitt, Aufbereitung, Beratung, Transport oder Einbau.
- **Technische Materialsteckbriefe:** Opalis sammelt Informationen zu häufigen Re-Use-Baustoffen: Eigenschaften, Verfügbarkeit, typische Mengen, Preise, Risiken und Einsatzhinweise.
- **Projektbeispiele:** Realisierte Projekte zeigen, welche Materialien erfolgreich wiederverwendet wurden und wie gestalterische, technische und organisatorische Fragen gelöst wurden.
- **Beschaffung und Vergabe:** Die Dokumentationssammlung unterstützt öffentliche und private Bauherrschaften dabei, Wiederverwendungsziele in Ausschreibungen, Rückbauverträgen und Planungsprozessen zu formulieren.
- **Skalierung:** Im Unterschied zu lokalen Materialmärkten ist Opalis als sektorale Marktinfrastruktur angelegt. Es bildet professionelle Akteure, Regionen und Materialströme über einzelne Projekte hinaus ab.

## Fachinhalt

### Plattformlogik

Opalis ist in mehrere Bereiche gegliedert:

- **Dealers / Händler:** Verzeichnis professioneller Händler für gebrauchte Baumaterialien.
- **Materials / Materialien:** technische Informationen zu häufig vorkommenden Re-Use-Produkten.
- **Examples / Beispiele:** realisierte Projekte mit wiederverwendeten Materialien.
- **Documentation / Dokumentation:** Leitfäden, Audits, Beschaffungsstrategien, Materialblätter, Quotenmethodik, Versicherungsfragen und politische Empfehlungen.
- **FAQ / About:** Erläuterungen zu Ziel, Partnern, Haftung und Nutzung.

Die Plattform weist ausdrücklich darauf hin, dass sie ein Business Directory ist und dass Nutzer:innen für konkrete Fragen die jeweiligen Anbieter kontaktieren müssen. Ebenso enthält sie einen Haftungsausschluss: Die Informationen sind indikativ und ersetzen keine Expertise anerkannter Fachleute. Für Forschung und Praxis ist diese Einschränkung zentral, weil Plattformen Informationsasymmetrien reduzieren, aber keine Prüf-, Planungs- oder Gewährleistungsverantwortung übernehmen.

### Händlerverzeichnis

Das Händlerverzeichnis enthält professionelle Anbieter, die Bauelemente aus dem Rückbau verkaufen. Opalis beschreibt je Händler unter anderem:

- Materialschwerpunkte;
- weitere angebotene Materialtypen;
- Dienstleistungen;
- Adresse und Kontakt;
- teilweise Verlinkungen zur Anbieterwebsite;
- Zuordnung zu Suchfiltern und Kategorien.

Wichtige Dienstleistungskategorien sind Transport, Demontage, Entwurf/Design, Abbruch, Einbau und spezifische Aufbereitungsoperationen. Dadurch wird sichtbar, dass Wiederverwendung nicht nur Materialhandel ist, sondern ein Dienstleistungsökosystem.

### Materialkategorien

Die Plattform strukturiert wiedergewonnene Baumaterialien in Kategorien, die für Planung und Ausschreibung relevant sind. Auf Händler- und Materialseiten werden unter anderem genannt:

- Tragholz: Binder, Balken, Sparren, Brettschichtholz, antike Eichenbalken.
- Stahl: Baustahl, Stahlträger.
- Ziegel und Mauerwerk: Vollziegel, Terrakottaziegel.
- Hallen, Gewächshäuser, Scheunen.
- Dämmstoffe.
- Naturstein: Fensterbänke, Stufen, Schwellen, Abdeckungen, Bruchstein.
- Dach: Schiefer, Dachziegel, Mauerabdeckungen.
- Ausbauholz: Schalungsplatten, Tropenholz aus maritimen Anwendungen, Scheunenholz, Gerüstbohlen, Bahnschwellen, wieder aufgesägte Balken, Restholz.
- Bauelemente: Fenster, ältere Fenster, neuere Fenster, Buntglas, Klappläden, Türen, Beschläge, Treppen.
- Innenausbau: Parkett, Wandbekleidungen, Steinplatten, Fliesen, Büroausbau, Teppichfliesen, Doppelböden, Trennwände, abgehängte Decken, Plattenwerkstoffe.
- Ausstattung: Sanitärobjekte, technische Anlagen, Radiatoren, Leuchten.
- Metallbau: Gitterroste, Tore, Zäune, Handläufe, Geländer.
- Architektonische Antiquitäten: Kamine, Zierelemente und historische Bauteile.

Diese Kategorien zeigen, dass Re-Use im Bauwesen nicht auf dekorative Antiquitäten begrenzt ist. Es umfasst tragende, ausbaunahe, technische, raumbildende und ausstattungsbezogene Elemente. Gleichzeitig variiert die Nachweisintensität stark: Ein historischer Kamin stellt andere Anforderungen als ein Stahlträger oder eine Brandschutztür.

### Produktoperationen und Aufbereitung

Opalis macht die Rolle von Aufbereitungsleistungen sichtbar. Genannte Operationen sind unter anderem:

- Entnageln, Sägen und grundlegende Holzbearbeitung;
- Mörtelreste entfernen;
- Tischlerarbeiten, Reinigung, Dimensionierung, Trocknung, Oberflächenbehandlung;
- Naturstein schneiden und oberflächenbehandeln;
- historische Materialrestaurierung;
- Herstellung von Möbeln aus wiedergewonnenem Material;
- Schleifen und Abbeizen;
- Pflasterstein sägen oder spalten;
- Türen und Fenster umrahmen oder anpassen;
- Radiatoren aufarbeiten;
- Metallprofile zuschneiden;
- Sanitärobjekte reinigen;
- technische Anlagen aufbereiten.

Diese Operationen sind für Wiederverwendung entscheidend. Ein geborgener Baustoff ist nicht automatisch ein marktfähiges Produkt. Marktfähigkeit entsteht durch Sichtung, Sortierung, Aufarbeitung, Mengenbündelung, Dokumentation und Logistik.

### Dokumentationsmodell

Die Opalis-Dokumentation ist einer der wichtigsten Beiträge zur Professionalisierung. Sie enthält unter anderem:

- Strategien für Beschaffung und Ausschreibung;
- Reclamation Audits zur Erhebung wiederverwendbarer Materialien im Bestand;
- Handbücher für Off-site-Reuse und Rückgewinnung aus öffentlichen Gebäuden;
- allgemeine Einführung und Materialsteckbriefe für 36 Materialgruppen;
- Berichte zu Pilotprojekten;
- Methoden zur Festlegung, Messung und Berichterstattung von Wiedergewinnungs- und Wiederverwendungsquoten;
- FutuREuse-Booklets, u. a. zu Umweltwirkungen, technischer Leistungsbewertung, Oberflächenbehandlungen, Produkt-oder-Abfall-Kriterien, Roadmaps, urbanen Lagerbeständen und Rückgewinnungsdesign;
- Praxisleitfäden für Generalunternehmen, Ausbauunternehmen, Holzbau, Dachdecker, Rückbauunternehmen und Infrastrukturunternehmen;
- Dokumente zu Versicherungspraxis und Wiederverwendung;
- Analysen des Re-Use-Sektors und öffentlicher Unterstützung.

Diese Dokumentation macht Opalis zu mehr als einer Händlerliste. Es ist eine Wissensinfrastruktur, die Planer:innen, Bauherrschaften, öffentliche Stellen und Unternehmen in konkreten Prozessschritten unterstützt.

### Marktplatzmodell und Grenzen

Opalis zeigt kein vollständig automatisiertes E-Commerce-Modell, sondern einen kuratierten Marktüberblick. Die eigentliche Transaktion bleibt bei den Händler:innen. Das ist aus mehreren Gründen sinnvoll:

- Zustand, Menge und Eignung gebrauchter Bauteile müssen projektspezifisch geprüft werden.
- Preise, Lagerbestände und Transportmöglichkeiten ändern sich.
- Häufig sind Beratung, Besichtigung und Nacharbeit erforderlich.
- Viele Bauteile sind einmalig oder nur in begrenzter Menge verfügbar.
- Haftung und Gewährleistung bleiben zwischen Käufer, Händler, Planer, Prüfer und Bauherr zu klären.

Für Forschung ist diese Grenze zentral: Digitale Plattformen können Wiederverwendung erleichtern, aber sie ersetzen nicht die physische und rechtliche Infrastruktur von Rückbau, Lagerung, Aufbereitung, Prüfung und Einbau.

## Praxisbezug / Beispiele

### Einordnung als Marktplatz-/Katalog-Fallstudie

Opalis unterscheidet sich klar von den anderen Fallstudien in dieser Gruppe:

- **CRCLR House:** konkretes Gebäudeprojekt mit realer Wiederverwendung.
- **Haus der Materialisierung:** lokale Infrastruktur, Werkstätten, Materialmarkt, Quartier.
- **Kunst-Stoffe Berlin:** gemeinnützige lokale Materialdrehscheibe.
- **Opalis:** digitale und sektorale Marktinfrastruktur für professionelle Händler, Materialkategorien und Dokumentation.

Damit ist Opalis besonders geeignet, um Fragen der Skalierung, Standardisierung, Auffindbarkeit und Markttransparenz zu untersuchen.

### Nutzung durch Planer:innen

Planer:innen können Opalis in mehreren Projektphasen nutzen:

- **Vorentwurf:** Einschätzung, welche Re-Use-Bauteile marktüblich verfügbar sind.
- **Entwurf:** Anpassung von Raster, Detail, Materialkonzept und Toleranzen an verfügbare Materialgruppen.
- **Ausschreibung:** Formulierung von Re-Use-Zielen, Materialqualitäten und Beschaffungswegen.
- **Rückbau:** Durchführung oder Beauftragung eines Reclamation Audits.
- **Beschaffung:** Kontaktaufnahme mit spezialisierten Händlern.
- **Nachweis:** Nutzung von Materialblättern und Leitfäden als Grundlage, nicht als Ersatz für projektspezifische Prüfungen.
- **Dokumentation:** Erfassung von Mengen, Herkunft, Zustand, Einbauort und späterer Demontierbarkeit.

### Nutzung durch öffentliche Auftraggeber

Öffentliche Auftraggeber können aus Opalis lernen:

- Re-Use braucht Ausschreibungswege, die gebrauchte Materialien zulassen.
- Zielquoten müssen messbar sein, dürfen aber nicht nur symbolisch bleiben.
- Rückbauleistungen sollten Materialerhalt, nicht nur Entsorgung, beauftragen.
- Händler- und Dienstleistungsstrukturen müssen früh einbezogen werden.
- Materialaudits im Bestand sind Grundlage für Verwertungshierarchien: Erhalt, Wiedereinbau vor Ort, Off-site-Reuse, Recycling, Entsorgung.
- Regionale Plattformen können Marktdaten und Anbieter sichtbar machen.

### Praktische Kriterien für eigene Plattformen

Eine übertragbare Re-Use-Plattform sollte mindestens enthalten:

- kuratiertes Händlerverzeichnis mit Kategorien und Dienstleistungen;
- Materialkategorien mit technischen Basisinformationen;
- Projektbeispiele;
- Suchfilter nach Region, Material, Dienstleistung und Operation;
- klare Haftungshinweise;
- Verbindung zu Re-Use-Audits und Ausschreibungsleitfäden;
- Angaben zur Verfügbarkeit, ohne falsche Liefersicherheit zu suggerieren;
- mehrsprachige oder regionale Anpassung;
- Pflegeverantwortung und Finanzierung;
- Schnittstellen zu Materialpässen, Bauteilkatastern und urban-mining-Datenbanken.

## Herausforderungen / offene Fragen

- **Aktualität der Bestände:** Händlerlisten und Materialkategorien sind nur nützlich, wenn sie gepflegt werden. Einzelbestände ändern sich schneller als redaktionelle Plattformen.
- **Haftung und Fachprüfung:** Opalis kann Informationen bündeln, übernimmt aber keine Verantwortung für konkrete Eignung. Fachliche Prüfung bleibt notwendig.
- **Regionale Übertragbarkeit:** Das Modell funktioniert nur, wenn es genügend Händler, Rückbauprojekte, Lagerflächen und Nachfrage gibt. Regionen ohne professionellen Re-Use-Handel benötigen zunächst Marktaufbau.
- **Spannung zwischen Katalog und Einmaligkeit:** Wiederverwendete Bauteile sind oft unikale oder chargenbezogene Produkte. Zu starke Standardisierung kann ihre Realität verdecken; zu wenig Standardisierung erschwert Planung.
- **Preistransparenz:** Indikative Preise helfen, können aber durch Qualität, Menge, Aufbereitung, Lagerung und Transport stark schwanken.
- **Nachweis- und Normenkompatibilität:** Materialsteckbriefe erleichtern Planung, ersetzen aber keine harmonisierten Verfahren für CE-Kennzeichnung, Leistungserklärungen, nationale Zulassungen oder projektspezifische Prüfungen.
- **Integration in BIM und Materialpässe:** Bisherige Plattformmodelle sind oft katalog- oder webseitenbasiert. Für größere Bauprojekte wären Schnittstellen zu BIM, digitalen Gebäudepässen und Ausschreibungssystemen wichtig.
- **Ökologische Bewertung:** Wiederverwendung ist nicht automatisch ökologisch vorteilhaft, wenn Transporte, Aufbereitung, Lagerung oder kurze Restnutzungsdauer ungünstig sind. Vergleichende Ökobilanzen bleiben notwendig.
- **Sozioökonomische Struktur:** Professionelle Händler sichern Qualität und Logistik, können aber andere Preisstrukturen haben als gemeinnützige Materialzentren. Die Rolle von sozialen Trägern, öffentlichen Re-Use-Zentren und privaten Händlern muss differenziert betrachtet werden.
- **Langfristige Finanzierung der Wissensinfrastruktur:** Eine Plattform wie Opalis braucht dauerhafte Pflege, redaktionelle Arbeit, Partnernetzwerke und Finanzierung. Projektförderung allein reicht selten für langfristige Markttransparenz.

## Quellen

- Opalis: Homepage, https://opalis.eu/en — Selbstbeschreibung „Building and renovating with reclaimed materials“, Bereiche Händler, Materialien, Beispiele, Dokumentation. Zugriff: 2026-04-27.
- Opalis: „About“, https://opalis.eu/en/about — Ziel der Plattform, Händlerverzeichnis, Materialdokumentation, Beispiele, Partner, Entwicklung durch Rotor, FCRBE und PREUSE. Zugriff: 2026-04-27.
- Opalis: „Dealers“, https://opalis.eu/en/dealers — Materialkategorien, Händler, Dienstleistungen und Operationen. Zugriff: 2026-04-27.
- Opalis: „Materials“, https://opalis.eu/en/materials — technische Materialinformationen und Materialkategorien. Zugriff: 2026-04-27.
- Opalis: „Documentation“, https://opalis.eu/en/documentation — FCRBE- und PREUSE-Dokumente zu Beschaffung, Reclamation Audit, Materialsteckbriefen, Wiederverwendungsquoten, Versicherungen und Sektoranalysen. Zugriff: 2026-04-27.
- Rotor: „Opalis – An online inventory of the professional sector in salvaged building materials“, https://rotordb.org/en/projects/opalis — Entstehung, Ziel und Rolle von Opalis als Brücke zwischen Händler:innen, Bauherrschaften, Architekt:innen und Bauunternehmen. Zugriff: 2026-04-27.
- Interreg North-West Europe: „FCRBE – Facilitating the Circulation of Reclaimed Building Elements“, https://vb.nweurope.eu/projects/project-search/fcrbe-facilitating-the-circulation-of-reclaimed-building-elements-in-northwestern-europe/ — Projektkontext der Weiterentwicklung von Opalis und transnationalen Re-Use-Instrumenten. Zugriff: 2026-04-27.
- PREUSE / Interreg North-West Europe: https://preuse.nweurope.eu/ — Kontext der Weiterpflege und Entwicklung öffentlicher Re-Use-Zentren 2024–2027. Zugriff: 2026-04-27.

### Legacy Source: dokument\Opalis_Datenbank.md

- Map action: move_as_knot
- Target role in map: primary
- Raw mapped target: software_digitaltool/Opalis
- Original primary target: software_digitaltool/Opalis
- Original secondary targets: datenmodell/Materialdatenbank

---
type: Dokument
---

﻿## Verknüpfungen

**Übergeordnete Themen**
- [[../werkzeug/ReUse_Plattform]]
- [[../werkzeug/Materialboerse]]
- [[../reuse_strategie/Direkte_Wiederverwendung]]
- [[../reuse_strategie/Urban_Mining]]
- [[../reuse_strategie/Aufarbeitung]]
- [[../akteur/Rotor]]

**Verwandte Dateien**
- [[Materialsheet]]
- [[Materialdatenbank]]
- [[Bauteilkatalog]]
- [[ReUse_Toolkit]]
- [[Specification_Method]]
- [[Ausschreibungstext]]
- [[Publikation]]

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- Akteure: Rotor, Opalis, Rotor Deconstruction, FCRBE, Salvoweb, professionelle Re-Use-Händler.
- Fallstudien/Tools: Opalis-Händlerverzeichnis, Opalis-Projektbeispiele, FCRBE-Dokumentation, Materialsheets.
- Materialien: wiedergewonnene Bauprodukte aus professionellem Handel, u. a. Holz, Ziegel, Naturstein, Türen, Leuchten, Stahl, Doppelboden, Sanitärobjekte.
- Methoden: Händlerverzeichnis, Materialgruppenbeschreibung, Projektbeispieldatenbank, Markterkundung, Procurement Strategies.

## Kurzdefinition

Die **Opalis-Datenbank** ist eine digitale Plattform für Bauen und Renovieren mit wiedergewonnenen Materialien. Sie dokumentiert professionelle Händler, Materialgruppen, Projektbeispiele und Fachpublikationen zur Wiederverwendung. Opalis wurde von Rotor initiiert und im FCRBE-Kontext als Infrastruktur für den professionellen Re-Use-Sektor in Nordwesteuropa weiterentwickelt.

Opalis ist keine projektinterne Materialdatenbank und kein Bauteilkatalog. Es ist eine Markt- und Wissensplattform.

## Relevanz für Wiederverwendung im Bauwesen

Re-Use-Märkte sind oft fragmentiert. Viele Bauteile werden von kleinen spezialisierten Händlern gehandelt, die in konventionellen Produktkatalogen nicht sichtbar sind. Opalis schließt diese Lücke: Es macht Bezugsquellen, Materialwissen und Referenzprojekte auffindbar. Für Planung und Ausschreibung ist die Plattform besonders in frühen Phasen nützlich, um verfügbare Produktgruppen, Händlerdichte, typische Materialqualitäten und realistische Spezifikationen einzuschätzen.

## Fachinhalt

### Plattformstruktur
- **Dealers:** Suchbares Verzeichnis professioneller Händler mit Standort, Spezialisierung und Kontakt.
- **Materials:** Informationen zu gängigen wiederverwendbaren Material- und Produktgruppen.
- **Examples / Projects:** gebaute Referenzen mit wiedergewonnenen Materialien.
- **Documentation:** FCRBE- und weitere Dokumente, u. a. Procurement Strategies, Reclamation Audit, Materialsheets, FutuREuse Booklets und Roadmaps.
- **Operations:** Hinweise auf typische Prozesse wie Demontage, Reinigung, Reparatur, Anpassung und Wiederverkauf.

### Rolle in Projektphasen
- **Frühphase:** Markterkundung, Plausibilisierung von Re-Use-Zielen, Händlerrecherche.
- **Entwurf:** Referenzprojekte, Materialästhetik, Toleranzen, verfügbare Formate.
- **Ausschreibung:** neutrale Anforderungen formulieren, ohne einzelne Anbieter unzulässig zu bevorzugen.
- **Ausführung:** Händlerkontakt, Chargenprüfung, Bemusterung, Lieferabstimmung.
- **Wissensaufbau:** Zugang zu FCRBE-Dokumentation und Materialsheets.

### Abgrenzung
- Gegenüber `Bauteilkatalog`: Opalis listet keine projektspezifischen Bauteile eines konkreten Gebäudes.
- Gegenüber `Materialdatenbank`: Opalis ist nicht primär Asset-Datenbank mit LCA- und Bauteil-ID-Daten.
- Gegenüber `Materialsheet`: Opalis hostet und verknüpft Materialsheets, ersetzt aber keine projektbezogene Prüfung.
- Gegenüber Marktplatz: Konkrete tagesaktuelle Einzelangebote liegen häufig bei Händler:innen; Opalis dient als Verzeichnis und Wissensportal.

## Praxisbezug / Beispiele

- **Markterkundung Innenausbau:** Ein Team sucht Türen, Leuchten und Sanitärobjekte. Opalis zeigt mögliche Händler und typische Materialgruppen; danach folgen direkte Anfragen und Bemusterung.
- **Ausschreibungsgrundlage:** Die FCRBE-Dokumente auf Opalis helfen, funktionale Spezifikationen und Nachweise zu formulieren.
- **Projektbeispiele:** Referenzen zeigen, wie Re-Use ästhetisch und technisch eingesetzt wurde, und erleichtern Akzeptanz bei Bauherrschaft.
- **Händler als Risikominderung:** Professionelle Händler übernehmen Demontage, Sortierung, Reinigung, Lagerung und Beschreibung, was Wiederverwendung planbarer macht.

## Herausforderungen / offene Fragen

- Händlerbestände ändern sich; Opalis ersetzt keine aktuelle Verfügbarkeitsprüfung.
- Geografische Abdeckung ist stark, aber nicht vollständig für alle Märkte.
- Plattformdaten sind informativ, nicht automatisch technische Eignungsnachweise.
- Öffentliche Ausschreibungen dürfen nicht auf einzelne Opalis-Händler zugeschnitten werden.
- Produkt-/Abfallstatus, Gewährleistung und Normen bleiben national unterschiedlich.
- Händlerprofile sind nicht gleich Materialpässe; projektbezogene Daten müssen ergänzt werden.

## Quellen

- FCRBE / Interreg NWE: Facilitating the circulation of reclaimed building elements in Northwestern Europe, Projektoutputs und Final Report. https://vb.nweurope.eu/projects/project-search/fcrbe-facilitating-the-circulation-of-reclaimed-building-elements-in-northwestern-europe/
- Opalis: Documentation, Material Sheets, Procurement Strategies, Reclamation Audit, FutuREuse Booklets. https://opalis.eu/en/documentation
- European Commission: EU construction & demolition waste management protocol including guidelines for pre-demolition and pre-renovation audits of construction works, Updated edition 2024. https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- DIN SPEC 91484:2023-09: Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen des hochwertigen Anschlussnutzungspotentials vor Abbruch- und Renovierungsarbeiten. https://www.dinmedia.de/de/technische-regel/din-spec-91484/371235753
- ISO 20887:2020: Sustainability in buildings and civil engineering works — Design for disassembly and adaptability. https://www.iso.org/standard/69370.html
- Opalis: Building and renovating with reclaimed materials. https://opalis.eu/en
- Opalis: About. https://opalis.eu/en/about
- Rotor: Opalis — online inventory of the professional sector in salvaged building materials. https://rotordb.org/en/projects/opalis
- European Circular Economy Stakeholder Platform: Opalis. https://circulareconomy.europa.eu/platform/en/dialogue/existing-eu-platforms/opalis
- Salvoweb. https://www.salvoweb.com/
- Rotor Deconstruction. https://rotordc.com/

---

---
id:
name: Opalis Datenbank
type:
status: seed
aliases: []
tags: []
source_notes: []
links:
  related_akteure: []
  related_fallstudien: []
  related_gebaeude: []
  related_bauteile: []
  related_tragwerkssysteme: []
  related_materialien: []
  related_methoden: []
  related_abbruchmethoden: []
  related_aufbereitungsmethoden: []
  related_pruefungen: []
  related_logistiken: []
  related_dokumente: []
  related_standards: []
  related_huerden: []
  related_foerderprogramme: []
  related_orte: []
  related_werkzeuge: []
  related_interviews: []
  related_berichte: []
---

# Opalis Datenbank

## Kurzdefinition

## Warum relevant fuer Reuse

## Wichtige Verbindungen

## Evidenz / Beispiele

## Offene Fragen

### Legacy Source: werkzeug\Opalis_Plattform.md

- Map action: semantic_move
- Target role in map: primary
- Raw mapped target: software_digitaltool/Opalis_Plattform
- Original primary target: software_digitaltool/Opalis_Plattform
- Original secondary targets: 

---
type: Werkzeug
datenmodell: ["[[datenmodell/Klassifikation]]"]
logistik: ["[[logistik/Lagerung]]", "[[logistik/Transport]]"]
methode: ["[[methode/Bauteilkatalogisierung]]"]
verwandt: ["[[werkzeug/Concular_Plattform]]", "[[werkzeug/Cycle_Up]]", "[[werkzeug/Material_Reuse_Portal]]", "[[werkzeug/Materialdatenbank]]", "[[werkzeug/ReUse_Toolkit]]", "[[werkzeug/RotorDB]]", "[[werkzeug/RotorDC]]", "[[werkzeug/SalvoWEB]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** Re-Use-Plattformen; Händlerverzeichnis; Sekundärbaustoffmarkt; Materialwissen; Fallstudien; FCRBE; europäische Wiederverwendungspraxis.
- **Verwandte Dateien:** `werkzeug/ReUse_Toolkit.md`; `werkzeug/Concular_Plattform.md`; `werkzeug/Materialdatenbank.md`; `methode/Bauteilkatalogisierung.md`; `methode/Pre_Demolition_Audit.md`; `akteur/Bauteilhaendler.md`; `akteur/Rueckbauunternehmen.md`; `logistik/Lagerung.md`; `logistik/Transport.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Opalis.eu; Rotor; Atelier 4/5; Bellastock; FCRBE; professionelle Händler gebrauchter Baustoffe; Material Sheets; Reclamation Audit; Materialkategorien wie Ziegel, Naturstein, Türen, Holz, Fliesen, Sanitär, Leuchten.

## Kurzdefinition

Opalis ist eine europäische Online-Plattform für Wiederverwendung im Bauwesen. Sie dokumentiert professionelle Händler und Dienstleister für rückgebaute Baustoffe, stellt technische Materialinformationen bereit, zeigt realisierte Projekte mit Re-Use-Materialien und verweist auf weiterführende Dokumente. Die Plattform wurde von Rotor initiiert und im Kontext europäischer Wiederverwendungsnetzwerke weiterentwickelt.

Opalis ist primär ein **Informations-, Orientierungs- und Netzwerkwerkzeug**, nicht ein vollständig transaktionaler Marktplatz wie ein Webshop. Die Plattform erleichtert die Suche nach Händlern, Materialgruppen, Praxiswissen und Beispielen.

## Relevanz für Wiederverwendung im Bauwesen

Opalis adressiert ein zentrales Problem der Wiederverwendung: Viele Planende und Auftraggeber wissen nicht, welche wiedergewonnenen Materialien marktüblich verfügbar sind, welche Händler existieren und welche technischen Besonderheiten zu berücksichtigen sind. Die Plattform macht den bestehenden professionellen Wiederverwendungssektor sichtbar.

Relevanz:

- Sichtbarmachung von Händlern, Lagerbetrieben, Demontage- und Aufbereitungsdienstleistern.
- Orientierung zu Materialgruppen, üblichen Qualitäten, Preisen, Verfügbarkeiten und Einsatzmöglichkeiten.
- Unterstützung von Planenden bei früher Re-Use-Integration.
- Verbindung von praktischer Marktkenntnis mit technischen Materialblättern.
- Referenz für Fallstudien und europäische Re-Use-Praxis.
- Ergänzung zu normativen, BIM- oder LCA-basierten Werkzeugen durch marktnahes Wissen.

## Fachinhalt

### Funktionsweise

Opalis gliedert sich im Kern in mehrere Bereiche:

- **Händlerverzeichnis:** professionelle Anbieter von rückgebauten Baustoffen und Bauteilen, mit Standort, Spezialisierungen und Dienstleistungen.
- **Materialinformationen:** technische Dokumentationen zu gängigen Re-Use-Produkten, z. B. Eigenschaften, Verfügbarkeit, Rückbau, Aufbereitung und Wiedereinbau.
- **Projektreferenzen:** realisierte Projekte, in denen wiederverwendete Materialien eingesetzt wurden.
- **Dokumente und Links:** Leitfäden, Toolkits, FCRBE-Materialien und weiterführende Ressourcen.

Die Plattform bringt nicht nur digitale Informationen zusammen, sondern bildet ein reales Ökosystem von Akteuren ab: Händler, Rückbauunternehmen, Planende, öffentliche Auftraggeber, Forschung und Aktivisten.

### Datentypen

- Händlername, Standort, Kontakt und geografischer Tätigkeitsbereich.
- Material- und Produktspezialisierungen.
- angebotene Dienstleistungen: Demontage, Reinigung, Zuschnitt, Aufarbeitung, Transport, Beratung.
- Materialkategorien und typische Produkte.
- technische Materialinformationen, z. B. Maße, Qualität, Leistung, Risiken, Einbauhinweise.
- Preis- und Verfügbarkeitsindikationen, soweit dokumentiert.
- Projektbeispiele und Fotos.
- Dokumente wie Material Sheets, Reclamation Audit und Procurement Guides.

### Plattform als Marktinfrastruktur

Opalis wirkt als Marktinfrastruktur, indem es Suchkosten reduziert und Vertrauen aufbaut:

- **Akteurstransparenz:** Wer handelt mit welchen Materialien?
- **Marktwissen:** Welche Bauteile sind regelmäßig verfügbar?
- **Planbarkeit:** Planende können früh erkennen, ob Materialgruppen grundsätzlich realistisch sind.
- **Professionalisierung:** Händler und Dienstleister werden als Teil einer legitimen Bauwirtschaft sichtbar.
- **Wissensstandardisierung:** Material Sheets beschreiben wiederkehrende Anforderungen und Hinweise.
- **Regionale Netzwerke:** Wiederverwendung ist transport- und lagerabhängig; regionale Anbieter sind entscheidend.

### Materialgruppen

Auf Opalis und in den zugehörigen FCRBE-Materialblättern finden sich u. a.:

- Natursteinpflaster, Bordsteine, Platten.
- Ziegel, Klinker, Naturstein.
- Holzbauteile, Parkett, Treppen, Türen.
- Fliesen, Bodenbeläge, Wandverkleidungen.
- Dachziegel, Schiefer, Fassadenelemente.
- Sanitärkeramik, Leuchten, Heizkörper, technische Elemente.
- Metallarbeiten, Geländer, Beschläge, historische Bauteile.
- Innenausbauprodukte, Möbel und Ausstattung.

Die tatsächliche Verfügbarkeit ist regional, zeitlich und chargenabhängig.

### Abgrenzung

- **Gegenüber Concular:** Opalis ist stärker Informations- und Händlerverzeichnis; Concular stärker projektbezogene Erfassung, Matching, Audit, Umsetzung und Marktplatz im DACH-Kontext.
- **Gegenüber Madaster:** Opalis dokumentiert Marktakteure und Materialien; Madaster registriert Gebäude und Materialpässe.
- **Gegenüber Materialdatenbank:** Opalis bietet technische und marktnahe Produktinformationen, aber keine vollständige LCA- oder EPD-Datenbank.
- **Gegenüber BIM:** Opalis arbeitet nicht primär modellbasiert; die Schnittstelle zur Planung ist eher material- und akteursorientiert.

### Schnittstellen

- **Planung / Ausschreibung:** Opalis kann Hinweise auf verfügbare Materialien und Händler liefern, die in Leistungsbeschreibungen und Materialrecherchen einfließen.
- **ReUse Toolkit:** Material Sheets, Reclamation Audit und Procurement-Dokumente ergänzen die Plattform.
- **Rückbau / Logistik:** Händlerprofile zeigen Dienstleistungen wie Demontage, Reinigung, Zuschnitt oder Transport.
- **Forschung:** Plattformdaten können Marktreife, regionale Akteursdichte und Materialgruppen analysierbar machen; Daten müssen jedoch vorsichtig interpretiert werden.
- **Materialpass / BIM:** direkte technische Schnittstellen sind begrenzt; Daten können aber manuell in Materialkataloge und Projektlisten übertragen werden.

## Praxisbezug / Beispiele

- **Materialrecherche in Entwurfsphase:** Ein Planungsteam prüft, ob wiederverwendete Ziegel, Natursteinplatten oder Türen in erreichbarer Region von professionellen Händlern angeboten werden.
- **Händlerintegration:** Ein Händler wird früh in die Planung eingebunden, um Maße, Qualitäten, Aufbereitung und Lieferfähigkeit abzuklären.
- **Ausschreibung:** Material Sheets und Händlerwissen helfen, Leistungsbeschreibungen für gebrauchte Bauteile realistischer zu formulieren.
- **Fallstudienanalyse:** Realisierte Projekte zeigen, welche Materialien tatsächlich eingesetzt wurden und welche Gestaltungsstrategien möglich sind.
- **Rückbaukonzept:** Opalis kann potenzielle Abnehmer oder Aufbereiter für ausgebaute Bauteile sichtbar machen.
- **Forschung zum Markt:** Anzahl und Spezialisierung von Händlern können Hinweise auf Marktreife einzelner Materialgruppen geben; die Daten sind aber nicht vollständig repräsentativ.

## Herausforderungen / offene Fragen

- Wie aktuell sind Händlerprofile, Materialangaben und Preisindikationen?
- Wie vollständig bildet Opalis den europäischen Wiederverwendungsmarkt ab?
- Gibt es ausreichende Transaktionsdaten, um reale Nachfrage, Preise und Mengen zu analysieren?
- Wie lassen sich Plattforminformationen mit BIM, Materialpässen oder Ausschreibungssoftware verbinden?
- Wie wird Qualitätssicherung bei einzelnen Händlern dokumentiert?
- Wie können öffentliche Auftraggeber Opalis-konforme Materialrecherche rechtssicher in Vergaben integrieren?
- Wie wird der Unterschied zwischen verfügbarer Materialart und konkreter lieferbarer Charge kommuniziert?
- Wie lassen sich Transportdistanzen und Lagerkapazitäten in Planungsentscheidungen einbeziehen?

## Quellen

- Opalis: About, https://opalis.eu/en/about
- Opalis: Dealers directory, https://opalis.eu/en/dealers
- Opalis: Materials and documentation, https://opalis.eu/
- Rotor: Reuse Toolkit – Material sheets, https://rotordb.org/en/projects/reuse-toolkit-material-sheets
- Rotor: We proudly present the Reuse Toolkit, https://rotordb.org/en/news/we-proudly-present-reuse-toolkit
- Interreg NWE FCRBE: Facilitating the Circulation of Reclaimed Building Elements, https://vb.nweurope.eu/projects/project-search/fcrbe-facilitating-the-circulation-of-reclaimed-building-elements-in-northwestern-europe/
- FCRBE / Opalis: The Reclamation Audit – A guide to inventory, https://opalis.eu/
- European Circular Economy Stakeholder Platform: Procurement strategies integrating reuse, https://circulareconomy.europa.eu/platform/
