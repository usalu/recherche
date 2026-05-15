---
entity: "software_digitaltool"
id: "Restado"
title: "Restado"
build_status: "promoted_phase42"
legacy_paths:
  - "akteur\\05_reuse_beratung_prozessdienstleister\\Concular.md"
  - "akteur\\06_bauteilboersen_marktplaetze_handel\\Restado.md"
  - "bauteilboerse\\restado.md"
  - "werkzeug\\Restado.md"
node_kind: "core"
---

# Restado

## Legacy Content

### Legacy Source: bauteilboerse\restado.md

- Map action: split_platform_profile
- Target role in map: primary
- Raw mapped target: software_digitaltool/restado
- Original primary target: software_digitaltool/restado
- Original secondary targets: akteur/<operator_if_named>; beschaffungsweg/Digitale_Plattform; ressourcenquelle/Bauteilboerse; plattformfunktion/Material_Matching

# Restado

## Kurzbeschreibung
Restado ist ein(e) digitaler B2B-Marktplatz / Online-Shop für zirkuläre Baustoffe mit Bezug zu Deutschland; DACH/Europa-Bezug durch Versand und Anbieter möglich. Im Reuse-Kontext liegt der Schwerpunkt auf: Direkte Wiederverwendung gebrauchter Baustoffe aus Rückbau.

## Land / Region
Deutschland; DACH/Europa-Bezug durch Versand und Anbieter möglich

## Betreiber
Concular GmbH; restado ist laut Impressum eine Marke der Concular GmbH

## Zielgruppe
gewerbliche Käufer und Verkäufer aus Architektur, Bau, Handwerk, Handel und Rückbau

## Plattformtyp
digitaler B2B-Marktplatz / Online-Shop für zirkuläre Baustoffe

## Bauteilkategorien
Türen und Zargen; Fenster; Fliesen und Steine; Dach; Fassade; Haustechnik und Sanitär; Innenausbau; Rohbau; Garten/Freianlagen; Werkzeuge/Maschinen; Altholz; Klinker; Restposten

## Art der Wiederverwendung
Direkte Wiederverwendung gebrauchter Baustoffe aus Rückbau; Nutzung von Überbestellungen, B-Ware und Baustellenresten; auch neue ökologische Baustoffe werden angeboten

## Funktionen
Suche nach Kategorien, Material und Region; Kauf/Verkauf über Listings; Händler können Baustoffe einstellen; Lieferung oder Abholung je nach Angebot

## Daten je Bauteil
öffentlich sichtbar typischerweise Produktbezeichnung, Kategorie, Standort, Preis, Einheit, Fotos und Anbieterhinweise; technische Nachweise je Angebot unterschiedlich

## Qualität / Prüfung
Restado wirbt mit hochwertigem Material; konkrete Prüfung, Gewährleistung und technische Dokumentation sind angebotsabhängig

## Logistik / Lagerung
Lieferung und Abholung möglich; Details je Verkäufer/Angebot

## Geschäftsmodell
Marktplatz für gewerbliche Käufer und Verkäufer; Einstellung laut Quelle kostenlos; weitere Gebühren/Kommissionen nicht angegeben

## Ökologische Bewertung
Ziel ist die Verlängerung von Produktlebenszyklen, weniger Abfall, Ressourceneinsparung und Emissionsminderung; bauteilbezogene Ökobilanzdaten sind nicht einheitlich angegeben

## Stärken
sehr direkter digitaler Zugang zu wiederverwendbaren Baustoffen; breite Kategorien; gewerbliche Ausrichtung; starker Reuse-Fokus

## Schwächen / Hemmnisse
opportunistische Verfügbarkeit; technische Nachweise und Garantie variieren; primär B2B, nicht für Verbraucher

## Relevanz für zirkuläres Bauen
hoch: Restado ist eine der wichtigsten digitalen deutschen Beschaffungsoptionen für wiederverwendbare und überschüssige Baustoffe.

## Quellen und Links
- https://restado.de/
- https://restado.de/ueber-restado/
- https://restado.de/materialreste/
- https://restado.de/hilfe/impressum/
- https://restado.de/haendler-auf-restado-werden/

type: Werkzeug
dokument: ["[[dokument/Pre_Demolition_Audit]]"]
logistik: ["[[logistik/Lagerung]]"]
verwandt: ["[[werkzeug/Concular_Plattform]]", "[[werkzeug/Material_Reuse_Portal]]"]

## Vertieftes Forschungsdossier

Quelle: `reuse/research/akteur/Research/Concular_detailed.md`

# Concular — vertieftes Forschungsdossier

> Arbeitsstand: Dieses Dossier vertieft das bestehende Kurzprofil zu Concular um Plattformlogik, Datentiefen, Standardisierungsrolle, Audit-to-Passport-Prozess, CircularLCA, CPX, Governance- und Schnittstellenfragen sowie eine präzisere Einordnung für ein Forschungsvorhaben zu „Entwerfen mit Bestand“. Wo keine belastbaren Primärquellen auffindbar waren, ist das explizit als Lücke markiert.

## 1. Executive Summary

Concular ist für Entwerfen mit Bestand kein bloßer „Marktplatz für gebrauchte Baustoffe“, sondern ein **hybrider Akteur aus Standardisierung, Auditpraxis, Datentechnologie, Circularity-Beratung und digitaler Auswertung**. Gerade diese Hybridität macht Concular besonders relevant.

Der Fall ist wertvoll, weil hier mehrere Prozessschichten verbunden werden, die in anderen Fällen oft getrennt auftreten:

1. **Bestandserfassung vor Rückbau/Umbau**,
2. **strukturierte Bewertung des Anschlussnutzungspotenzials**,
3. **digitale Pass- und Berichtserzeugung**,
4. **Ökobilanzierung und Zirkularitätsbewertung**,
5. **Anbindung an BIM, Excel/CSV und Zertifizierungskontexte**,
6. **beratungs- und umsetzungsnahe Integration in reale Projekte**.

Concular ist deshalb ein Schlüsselfall für die Frage, wie aus Bestand **standardisierbare, vergleichbare und entscheidungsfähige Material- und Gebäudedaten** werden. Für das Forschungsthema von Entwerfen mit Bestand ist besonders wichtig: Concular adressiert die Kette von **Erheben → Bewerten → Dokumentieren → Bilanzieren → Berichten** sehr stark, während die letzte Übersetzung in **entwurfsaktive, generative oder interaktive Design-Interfaces** öffentlich deutlich weniger sichtbar bleibt.

Genau darin liegt der zentrale Forschungsgewinn: Concular zeigt sehr klar, wie weit die bestehende Standardisierung und Softwarelogik heute schon reicht — und wo für ein Tool zum „Entwerfen mit Bestand“ noch eine Lücke bleibt.

## 3. Warum Concular für Entwerfen mit Bestand besonders relevant ist

Concular ist für Entwerfen mit Bestand aus mindestens sieben Gründen hoch relevant:

### 3.1 Bestand wird in strukturierte Daten übersetzt

Concular adressiert die Frage, wie aus einem Bestandsgebäude ein **digital auswertbarer Bauteilkatalog** wird. Das ist unmittelbar anschlussfähig an dein Interesse an Metadaten und materialbezogenem Entwerfen.

### 3.2 Anschlussnutzung wird standardisiert bewertet

Mit DIN SPEC 91525 wird nicht nur Bestand dokumentiert, sondern systematisch gefragt, **welcher Anschlussnutzungspfad** für ein Produkt realistisch und sinnvoll ist.

### 3.3 Circularity und LCA werden gekoppelt

Concular verknüpft Zirkularitätsbewertung (CPX) und Ökobilanzierung (CircularLCA). Das ist wichtig, weil Re-Use im Planungsalltag zunehmend nicht nur qualitativ, sondern **metrisch** verargumentiert werden muss.

### 3.4 Zertifizierung und Compliance werden integriert

Concular bindet DGNB, QNG, BNB, Level(s), ENV 1.1, CSRD-/Reporting-Logiken und Gebäuderessourcenpass an. Für das Forschungsvorhaben Entwerfen mit Bestand zeigt das, wie Circularity in bestehende Governance- und Berichtssysteme übersetzt wird.

### 3.5 Digitale Anschlussfähigkeit an BIM und tabellarische Daten

Concular beschreibt Importwege über BIM-Schnittstelle, IFC, CSV/Excel und Bauteillisten. Das macht den Fall relevant für Fragen nach Datenschemata und Interoperabilität.

### 3.6 Audit-to-Passport als Prozessarchitektur

Concular spricht explizit von **Audit-to-Passport**. Das ist forschungslogisch interessant, weil hier ein kompletter Transformationspfad benannt wird: von der Erhebung im Bestand bis zum Pass bzw. Bericht.

### 3.7 Grenze zum entwerfenden Interface

Trotz aller Datentiefe bleibt öffentlich begrenzt sichtbar, wie stark Concular heterogene, unvollständige oder zeitlich unsichere Bestandsdaten in ein wirklich **interaktives, architektonisches Entwurfswerkzeug** übersetzt. Genau hier liegt eine wichtige Forschungslücke.

## 5. Pre-Deconstruction Audit nach DIN SPEC 91484

Der PDA ist einer der wichtigsten Bausteine im Concular-Modell.

### Öffentliche Kernaussagen

Concular beschreibt den PDA als standardisiertes Verfahren zur Erfassung von Bauprodukten vor Abbruch- und Renovierungsarbeiten. Es geht darum, bereits vor Rückbau oder Umbau die Potenziale hochwertiger Anschlussnutzung sichtbar zu machen.

Die öffentlich beschriebene Prozesslogik umfasst:

- Vorbewertung nach Abfallrangfolge,
- einen digital bereitgestellten Untersuchungsbericht,
- eine Vorprüfung etwa sechs Monate vor Rückbauausschreibung,
- eine Stufe-II-Erfassung mit detailliertem, bewerteten Bauteilkatalog,
- digitale Aufnahme von Produktdaten, Mengen, Verortung, Bemaßung, Zustand und Rückbaufähigkeit,
- Einordnung in Verwertungsströme.

### Zwei-Stufen-Modell

Concular erklärt die DIN SPEC 91484 als zweistufiges Verfahren:

#### Stufe 1: Vorprüfung

- grundlegende Informationen zum Gebäude,
- erste Begehung,
- grobe Potenzialeinschätzung,
- Identifikation von Bauteilen mit grundsätzlicher Eignung für hochwertige Anschlussnutzung.

#### Stufe 2: Detaillierte Erfassung

- Anreicherung der Informationen,
- tiefergehende Beschreibung der Bauteile,
- stärkere Grundlage für Bewertung der Anschlussnutzung,
- digitaler Bauteilkatalog mit relevanten Attributen.

### Was das methodisch bedeutet

Für das Forschungsvorhaben Entwerfen mit Bestand ist entscheidend, dass der PDA nicht nur als Inventarisierung erscheint, sondern als **Entscheidungsvorbereitung**. Bestand wird also nicht neutral erfasst, sondern bereits im Hinblick auf spätere Verwendungsoptionen gerahmt.

### Forschungsnutzen

Der PDA ist wahrscheinlich einer der stärksten öffentlich sichtbaren Fälle für die Frage:
**Welche Metadaten sind nötig, damit aus einem existierenden Bauteil eine potenzielle Ressource für Re-Use, Weiterverwendung oder hochwertiges Recycling wird?**

## 7. Audit-to-Passport: Conculars eigentliche Kernlogik

Concular benennt auf der Seite zur zirkulären Ökobilanzierung explizit „Audit-to-Passport“. Das wirkt klein, ist aber für die Forschung sehr groß: Es beschreibt die eigentliche Grundarchitektur des Unternehmens.

### Rekonstruierte Transformationskette

1. **Bestandserfassung**
2. **digitale Strukturierung im Bauteilkatalog**
3. **Bewertung von Anschlussnutzungspfaden**
4. **Verknüpfung mit Produkt- und Materialdaten**
5. **LCA / Circularity-Bewertung**
6. **Export in Pass-, Report- und Zertifizierungsformate**

### Warum das für Entwerfen mit Bestand so wichtig ist

Das Forschungsthema von Entwerfen mit Bestand fragt im Kern danach, wie man mit Bestand entwerfen kann. Concular zeigt, dass der Weg dorthin nicht bei „Material gefunden" endet, sondern über mehrere Übersetzungsschritte führt:

- Erfassung,
- Anreicherung,
- Bewertung,
- Vergleich,
- Berichtbarkeit,
- Weitergabe in andere Systeme.

### Die eigentliche Erkenntnis

Concular ist weniger als einzelnes Tool zu verstehen, sondern als **Prozess-Backbone**, das Material- und Gebäudedaten über mehrere Verwendungszusammenhänge hinweg kompatibel macht.

## 9. Gebäuderessourcenpass / Life-Cycle Passport

Concular bietet einen digitalen Gebäuderessourcenpass bzw. Life-Cycle Passport an und verknüpft diesen stark mit CircularLCA.

### Öffentlich erkennbare Funktionen

- detaillierte Erfassung verbauter Ressourcen,
- Zirkularität und Ökobilanz im Pass,
- Export als DGNB-konforme Exceldatei oder PDF,
- Erfüllung von DGNB TEC 1.6,
- automatisiertes oder vorausgefülltes Ausfüllen.

### Strategische Bedeutung

Der Ressourcenpass ist für Entwerfen mit Bestand nicht nur als Dokument interessant, sondern als **Persistenzschicht**. Er macht Ressourcen über den Moment der Planung hinaus dokumentierbar.

### Forschungsperspektive

Für ein Forschungsprojekt zu „Entwerfen mit Bestand“ ist besonders interessant, dass der Pass zwar Informationen konserviert und weitergibt, aber öffentlich wenig darüber verrät,

- wie granular Bauteile adressiert werden,
- wie Unsicherheiten gekennzeichnet sind,
- wie temporäre, spekulative oder nur teilweise bestätigte Daten abgebildet werden,
- wie dynamisch sich Passdaten im Projektverlauf verändern.

Das deutet auf eine Spannung hin zwischen **statischer Dokumentation** und **dynamischer Entwurfslogik**.

## 11. Datenmodell: Was bei Concular öffentlich sichtbar wird

Concular veröffentlicht kein vollständiges technisches Datenmodell, aber aus der Produkt- und Leistungsbeschreibung lässt sich eine erstaunlich reichhaltige Struktur rekonstruieren.

## 11.1 Wahrscheinlich zentrale Datengruppen

### A. Bestands- und Gebäudeinformationen

- Gebäudekontext,
- Umbau-/Rückbaukontext,
- Zeitpunkt und Projektphase,
- Zielkontext des Audits.

### B. Bauteil- und Produktdaten

- Produktdaten,
- Materialien,
- Mengen,
- Verortung,
- Bemaßung,
- Zustand,
- Rückbaufähigkeit,
- Materialspezifizierungen.

### C. Bewertungsdaten

- Verwertungsstrom,
- Anschlussnutzungspfad,
- technische Machbarkeit,
- wirtschaftliche Zumutbarkeit,
- ökologisches Potenzial,
- Zirkularitätsfaktoren.

### D. Planungs- und Modellierungsdaten

- IFC/BIM-Zuordnung,
- PropertySets,
- Excel-/CSV-Strukturen,
- Bauteilebene,
- Komponenten-Editor.

### E. Nachhaltigkeits- und Berichtsdaten

- LCA-Werte,
- Zertifizierungszuordnung,
- Passdaten,
- Materialwert,
- Nachhaltigkeitsindikatoren.

### F. Prozess- und Governance-Daten

- Vergabe-/Ausschreibungsbezug,
- Wiedereinbau / Materialvermittlung,
- Versicherung & Gewährleistung,
- Reporting- und Compliance-Bezug.

## 11.2 Was öffentlich unklar bleibt

- Pflichtfelder vs. optionale Felder,
- Datenqualitätsstufen,
- Umgang mit Unsicherheiten,
- Versionierung von Bauteildaten,
- Reservierungs- / Statuslogiken,
- Audit-zu-BIM-Zuordnung im Detail,
- API-Strukturen,
- Rechte- und Rollenmodell.

### Zentrale Forschungsableitung

Concular scheint ein **mehrschichtiges Datenmodell** zu verfolgen, das zugleich für Audit, Bewertung, Bilanzierung und Bericht funktionieren muss. Für ein entwurfsbezogenes Forschungstool wäre die entscheidende Frage, welche dieser Schichten tatsächlich für frühe Entwurfsentscheidungen erforderlich sind — und welche nur für spätere Compliance- oder Nachweiszwecke gebraucht werden.

## 13. Concular als Standardisierungsakteur

Ein besonderer Forschungswert des Falls liegt darin, dass Concular nicht nur Standards anwendet, sondern an ihrer Formulierung aktiv mitwirkt.

### Öffentlich sichtbar

- Concular beschreibt sich als Initiatorin und Konsortialleiterin der DIN SPEC 91525.
- Auf der 91484-Seite beschreibt Concular sich ebenfalls als Initiator / Konsortialleiter der DIN SPEC 91484.
- Für 91484 wird eine breite Mitwirkung verschiedener Akteur:innen aus Wissenschaft, Baupraxis, Rückbau, Architektur und Verbänden genannt.

### Warum das relevant ist

Concular ist dadurch nicht nur Tool-Anbieter, sondern **Mitgestalter der Regelwerke**, auf denen Teile des eigenen Leistungsangebots beruhen. Das ist methodisch hochinteressant, denn es schafft eine Rückkopplung zwischen

- Praxisproblemen,
- Normierungsarbeit,
- Softwareanforderungen,
- Beratungsleistungen,
- Marktbildung.

### Forschungsthese

Concular könnte als Beispiel dafür gelesen werden, wie sich in der Circular Economy **Standards, Software und Projektpraxis ko-evolutionär** entwickeln.

---

## 14. Beratung, Materialvermittlung und Umsetzungsnähe

Mehrere Seiten von Concular machen deutlich, dass das Unternehmen nicht nur Daten erzeugt, sondern auch in reale Umsetzungsfragen hineinwirkt.

### Öffentlich genannte Umsetzungsnähe

- Materialvermittlung / Matchmaking,
- Vertrieb von Materialien,
- Urban Mining Hubs,
- rechtssicherer Wiedereinbau,
- Versicherung & Gewährleistung,
- Begleitung von Vergabe und Ausschreibung,
- zirkuläre Fachplanung von LP 0 bis 9.

### Warum das wichtig ist

Für Entwerfen mit Bestand heißt das: Concular bewegt sich nicht nur im digitalen Vorfeld, sondern bis in die operative Umsetzung hinein. Das macht den Fall stärker als rein digitale Tools, weil hier die **Spannung zwischen Datensystem und Baustellenrealität** sichtbar werden kann.

### Aber: genaue operative Tiefe bleibt öffentlich begrenzt

Nicht klar ist öffentlich,

- ob Concular selbst Material hält oder nur vermittelt,
- wie Materialverfügbarkeit statuslogisch verwaltet wird,
- wie Gewährleistungs- und Versicherungsfragen im Einzelfall gelöst werden,
- wie eng Software und Materialhandel gekoppelt sind.

---

## 15. Entwurfsrelevanz: Wie nah ist Concular wirklich am Design?

Das ist vermutlich der wichtigste Abschnitt für Entwerfen mit Bestand.

### Was klar für Entwurfsnähe spricht

- Variantenvergleich in CircularLCA,
- Bauteilebene und Komponenten-Editor,
- frühe Leistungsphasen werden ausdrücklich adressiert,
- angereicherte Bauteildaten für einfache Modelle,
- BIM-basierte Analyse und Optimierung,
- Anschlussnutzungskonzepte als planungsnahe Entscheidungsgrundlage.

### Was eher auf Bewertungs- als auf Generierungslogik hinweist

- starke Fokussierung auf LCA, Zertifizierung, Berichtbarkeit und Pass-Export,
- öffentliche Betonung von Audit, Katalogisierung und Auswertung,
- wenig Hinweise auf Formfindung, geometrische Generierung oder entwerfendes Re-Use-Matching im Sinne eines kreativen Design-Interfaces.

### Forschungsschluss

Concular ist öffentlich erkennbar **nah an der frühen Planungsbewertung**, aber nicht eindeutig ein Tool für **architektonische Entwurfsgenese**. Es hilft offenbar sehr gut beim Bewerten, Vergleichen, Strukturieren und Berichten — weniger sichtbar ist die direkte Unterstützung des architektonischen „Was entwerfe ich aus genau diesen verfügbaren Beständen?“.

### Genau daraus ergibt sich deine Lücke

Ein künftiges Forschungs- oder Entwurfswerkzeug könnte auf Concular-artigen Daten- und Bewertungslogiken aufbauen, aber zusätzlich leisten:

- materialgetriebene Form- und Typologievorschläge,
- Visualisierung von Unsicherheiten im Entwurf,
- geometrisches Matching,
- statusabhängige Variantenräume,
- Interaktion mit Materialverfügbarkeiten in Echtzeit oder projektzeitlich.

---

## 16. Tragwerk, Prüfung und Nachweis

Hier liegt eine wichtige Grenze der öffentlichen Sichtbarkeit.

### Öffentlich erkennbar

Concular spricht über technische Machbarkeit, Kennwerte, Zulassungen, Produktdaten, Anschlussnutzung und professionelle Wiederaufarbeitung. Im CPX werden Wiederverwendungspotenziale und Schadstoffkriterien adressiert; in 91525 werden technische Rahmenbedingungen als Entscheidungsebene genannt.

### Öffentlich nicht erkennbar

Nicht belastbar auffindbar waren detaillierte öffentliche Informationen zu:

- tragwerksspezifischen Vorbemessungslogiken,
- statischen Nachweisworkflows,
- Klassifizierung tragender Re-Use-Bauteile,
- Prüfstandards für Strukturelemente,
- Integration von Prüfberichten in die Softwareoberfläche,
- Verantwortungsabgrenzung zwischen Plattform/Beratung und Fachplanung.

### Forschungseinordnung

Concular wirkt öffentlich stärker als **Strukturierer und Bewertungsanbieter** denn als sichtbar dokumentierter Tragwerksprüf-Stack. Das heißt nicht, dass solche Prüfpfade fehlen, sondern nur, dass sie in der öffentlichen Dokumentation kaum greifbar sind.

### Interviewrelevanz

Gerade hier wäre eine vertiefende Befragung sehr ergiebig:

- Wo endet Conculars technische Eignungsbewertung?
- Welche Prüftiefe ist Teil des Produkts, welche Teil der Beratung, welche externe Ingenieur:innenleistung?
- Wie werden unklare oder fehlende Nachweise im Datenmodell markiert?

---

## 17. LCA, Reporting, Zertifizierung, Governance

Concular ist stark in der Übersetzung von Circularity in Governance- und Reporting-Umgebungen.

### Öffentlich genannte Bezüge

- DGNB 2018 / 2023,
- QNG,
- BNB,
- Level(s),
- DGNB TEC 1.6,
- ENV 1.1,
- EU-Taxonomie / Reporting,
- CSRD-Bezüge in Selbstdarstellung und Materialien.

### Was das für die Forschung bedeutet

Concular zeigt, dass Circularity in der Baupraxis zunehmend dann handlungsrelevant wird, wenn sie an **Zertifizierung, Berichtspflichten, Finanzierungs- und Compliance-Logiken** anschlussfähig wird.

### Starke Seite von Concular

Gerade hier scheint Concular besonders stark: nicht nur Daten sammeln, sondern sie in **governancefähige Outputs** überführen.

### Kritische Perspektive

Für ein entwurfsorientiertes Forschungsvorhaben ist diese Stärke ambivalent:

- Sie erhöht praktische Relevanz,
- kann aber dazu führen, dass Circularity vorrangig als **Nachweis- und Optimierungsproblem** und weniger als **gestalterische Praxis des Arbeitens mit Bestand** erscheint.

---

## 18. Concular als Datenregime für zirkuläres Bauen

Der vielleicht wichtigste theoretische Zugriff besteht darin, Concular als **Datenregime** zu lesen.

### Ebene A: Erhebungsdaten

Bestand wird vor Ort oder digital aufgenommen.

### Ebene B: strukturierte Material- und Bauteildaten

Produkte, Mengen, Zustand, Verortung, Bemaßung, Rückbaufähigkeit usw. werden katalogisierbar.

### Ebene C: Bewertungsdaten

Anschlussnutzung, technische Plausibilität, wirtschaftliche Zumutbarkeit, ökologische Potenziale.

### Ebene D: Simulations- und Vergleichsdaten

LCA, Variantenvergleich, Circularity-Scoring, Materialwert.

### Ebene E: Dokumentations- und Governance-Daten

Ressourcenpass, Compliance-Report, Zertifizierungsexporte.

### Ebene F: Umsetzungsdaten

Vergabe, Materialvermittlung, Wiedereinbau, Gewährleistung, Baustellenprozesse.

### Forschungsableitung

Für Entwerfen mit Bestand ist vermutlich nicht „ein Datenmodell“ die richtige Zielvorstellung, sondern eine **mehrlagige Informationsarchitektur**, die unterschiedliche Nutzungsmodi zulässt:

- auditiv,
- planerisch,
- bilanziell,
- regulatorisch,
- operativ.

Concular ist hierfür einer der besten öffentlich sichtbaren Referenzfälle.

---

## 19. Kritische Lücken und offene Fragen

Trotz der hohen Sichtbarkeit bleiben wesentliche Punkte offen.

### 19.1 Internes Datenmodell

Nicht öffentlich dokumentiert sind Datenfelddefinitionen, Pflichtlogiken, Hierarchien, Unsicherheitsklassen, Objektbeziehungen und Versionierung.

### 19.2 API und technische Offenheit

Offene Excel-Exporte und BIM-Anbindungen werden benannt; konkrete öffentliche API-Dokumentation war aber nicht belastbar auffindbar.

### 19.3 Materialverfügbarkeit als dynamischer Zustand

Unklar bleibt, wie Verfügbarkeit, Reservierung, Verkauf, Wiedereinbau und zeitliche Unsicherheit in der Plattformlogik tatsächlich modelliert werden.

### 19.4 Rollenmodell

Unklar bleibt, wie Verantwortlichkeiten zwischen Audit, Beratung, Software, Materialvermittlung, Ingenieurplanung und Bauherr:innenschaft verteilt sind.

### 19.5 Tragwerks- und Prüftiefe

Hier gibt es öffentliche Hinweise auf technische Bewertung, aber wenig belastbare Einsicht in konkrete Prüfpfade.

### 19.6 Markt-/Wirtschaftslogik

Es bleibt offen, welche Erlös- und Geschäftslogiken auf welchen Produkt- oder Projektteilen beruhen: Audit, Softwarelizenz, Beratung, Matchmaking, Zertifizierungsunterstützung, Datenmapping etc.

---

## 20. Konkrete Forschungsableitungen für Entwerfen mit Bestand

## 20.1 Concular als Referenz für Standardisierung

Wenn du einen Überblick darüber brauchst, wie Bestand in **formal beschreibbare Re-Use-Daten** übersetzt werden kann, ist Concular einer der stärksten Fälle.

## 20.2 Concular als Referenz für Audit + Pass + LCA-Kopplung

Für die Frage, wie materialbezogene Erhebung mit Nachhaltigkeits- und Reportinglogik zusammengeführt wird, ist der Fall fast ideal.

## 20.3 Concular als Negativ-/Grenzfall für Entwurfsinteraktivität

Gerade weil Concular daten- und nachweisstark ist, zeigt der Fall gut, was für ein entwurfsorientiertes Tool zusätzlich nötig wäre:

- Unsicherheitsdarstellung,
- Verfügbarkeitslogik,
- Geometrie-Matching,
- materialgetriebener Variantenraum,
- Re-Use als gestalterischer Input statt nur Bewertungsgegenstand.

## 20.4 Für dein mögliches Tool

Ein entwurfsorientiertes Re-Use-Tool könnte auf Concular-artigen Inputs aufbauen, aber andere Ausgaben priorisieren:

- räumliche Komposition,
- Bauteil-Matching,
- alternatives Fügen,
- gestalterische Varianten,
- sichtbare Unsicherheiten,
- Zeitfenster der Verfügbarkeit.

---

## 21. Präzisierte Interviewfragen

### Zu Organisation und Strategie

1. Wie verteilen sich bei Concular Beratung, Softwareprodukt und operative Materialvermittlung organisatorisch?
2. Wo verortet ihr euch selbst: eher Audit- und Datenanbieter, eher Circular-Consulting, eher Plattform oder eher integrierte Lösung?
3. Welche Leistungsbestandteile sind standardisiert, welche stark projektspezifisch?

### Zu DIN SPEC 91484

4. Welche Datenfelder sind in Stufe 1 praktisch unverzichtbar?
5. Welche Felder aus Stufe 2 entscheiden am häufigsten darüber, ob ein Bauteil in hochwertige Anschlussnutzung geht?
6. Wie wird Datenqualität oder Unsicherheit im PDA gekennzeichnet?
7. Wie geht ihr mit fehlender Produktidentität, unlesbaren Typenschildern oder unklaren Materialschichten um?

### Zu DIN SPEC 91525

8. Wie operationalisiert ihr „technische Machbarkeit“ und „wirtschaftliche Zumutbarkeit“?
9. Welche Kriterien führen am häufigsten zum Ausschluss eines Anschlussnutzungspfads?
10. Wie stark ist das Anschlussnutzungskonzept regelbasiert und wie stark expertenbasiert?
11. Werden Ergebnisse eher diskret (geeignet / ungeeignet) oder graduell (mehrere plausible Pfade) modelliert?

### Zu Datenmodell und Software

12. Welche Kernobjekte existieren in eurem Datenmodell: Gebäude, Räume, Bauteile, Produkte, Materialien, Chargen, Varianten?
13. Gibt es eindeutige IDs und Versionen je Bauteil / Datensatz?
14. Wie werden BIM-Daten, Auditdaten und LCA-Daten zusammengeführt?
15. Welche Schnittstellen oder APIs gibt es real für externe Forschung oder Planungssoftware?
16. Wie werden PropertySets definiert und gepflegt?

### Zu CircularLCA und CPX

17. Wie geht CircularLCA mit frühen Planungsphasen und geringer Datentiefe um?
18. Welche Datensätze oder Annahmen werden automatisiert gemappt und wo braucht es manuelle Eingriffe?
19. Wie robust ist der CPX bei unscharfen oder unvollständigen Inputs?
20. Welche Faktoren im CPX sind empirisch am sensibelsten?
21. Wie verhindert ihr, dass Kennzahlen projektspezifische Re-Use-Qualitäten zu stark glätten?

### Zu Entwurf und Planung

22. Welche Funktionen von Concular werden tatsächlich schon im Vorentwurf benutzt?
23. Was fehlt, damit Planende mit Bestand wirklich entwerfen statt nur bewerten?
24. Wie werden Verfügbarkeiten, Reservierungen und zeitliche Unsicherheiten planungsseitig sichtbar gemacht?
25. Welche Interaktion zwischen Architekt:innen und euren Datensätzen wäre ideal, existiert aber noch nicht?

### Zu Prüfung und Tragwerk

26. Wo endet eure technische Eignungsbewertung und wo beginnt externe Ingenieurprüfung?
27. Wie markiert ihr Bauteile, deren Wiederverwendung fachlich plausibel, aber noch nicht nachgewiesen ist?
28. Welche Rolle spielen Zulassungen, Zertifikate und Prüfberichte in eurem Datenmodell?

---

## 22. Arbeits-Hypothesen für die weitere Forschung

1. **Concular ist einer der stärksten öffentlich sichtbaren Fälle für die Standardisierung der Bestand-zu-Daten-Kette.**
2. **Die eigentliche Stärke liegt weniger im einzelnen Marktplatzobjekt als in der Kopplung von Audit, Bewertung, LCA, Pass und Reporting.**
3. **DIN SPEC 91525 ist für entwurfsnahe Forschung wahrscheinlich wichtiger als 91484 allein, weil sie den Entscheidungsschritt formalisiert.**
4. **CircularLCA bringt Concular bis in die frühe Planung hinein, bleibt aber öffentlich eher ein Bewertungs- als ein Generierungstool.**
5. **Die größte Forschungslücke liegt in der Übersetzung standardisierter Bestandsdaten in architektonische Entwurfsinteraktion unter Unsicherheit.**
6. **Concular ist ein Beispiel dafür, wie Circular-Economy-Praxis über Normierung, Software und Beratung gleichzeitig skaliert wird.**

---

## 23. Priorisierung für Entwerfen mit Bestand

### Priorität: sehr hoch

Concular sollte in der Akteurslandschaft von Entwerfen mit Bestand **sehr hoch priorisiert** werden, um Folgendes zu verstehen:

- welche Daten im Bestand erhoben werden müssen,
- wie Anschlussnutzung standardisiert bewertet werden kann,
- wie Re-Use mit LCA und Zertifizierung verknüpft wird,
- wie Pass- und Berichtsdokumente aus Projektdaten hervorgehen,
- wo die Grenze zwischen Datenaufbereitung und entwurfsorientiertem Tooling verläuft.

### Warum Concular besonders nützlich ist

Andere Fälle zeigen entweder

- Materialströme,
- politische Rahmen,
- Pilotarchitektur,
- informelle Re-Use-Praktiken,
- oder Nachweis-/Engineering-Expertise.

Concular bündelt in seltener Dichte:

- Standardisierung,
- Datenerhebung,
- Bewertungslogik,
- Software,
- LCA,
- Pass,
- Zertifizierung,
- Umsetzungsnähe.

---

## 24. Kompakte Schlussfolgerung

Concular ist ein Schlüsselfall dafür, wie zirkuläres Bauen **datenförmig, normierbar und auswertbar** gemacht wird. Das Unternehmen zeigt besonders klar, wie Bestand nicht nur inventarisiert, sondern in eine Kette aus Audit, Anschlussnutzung, Bewertung, Bericht und Projektintegration überführt wird.

Für das Forschungsvorhaben Entwerfen mit Bestand ist der Fall deshalb zentral, weil er die derzeit wohl sichtbarste Infrastruktur für **Bestand → Daten → Bewertung → Pass / LCA / Zertifizierung** darstellt. Gerade dadurch wird aber auch die verbleibende Lücke sichtbar: Die Übersetzung dieser strukturierten Daten in **entwurfsaktive, materialgetriebene Design-Interfaces**, die Unsicherheit, Verfügbarkeit, Heterogenität und architektonische Entscheidung zugleich verarbeiten.

Concular ist also weniger das Endziel für „Entwerfen mit Bestand“ als ein sehr starker Referenzfall für die **Daten- und Bewertungsgrundlage**, auf der ein solches Entwurfswerkzeug aufbauen könnte.

---

## 25. Primärquellen / Links

### Concular — Organisation und Einstieg

- Startseite: https://concular.de/
- Impressum: https://concular.de/impressum/
- Karriere: https://concular.de/karriere/

### Standards / Audit / Anschlussnutzung

- DIN SPEC 91484 / Pre-Deconstruction Audit: https://concular.de/din-spec-91484-pre-demolition-audit/
- PDA-Blog: https://concular.de/pre-deconstruction-audit-pda-nach-din-spec-91484-schluessel-zur-kreislaufwirtschaft-im-bauwesen/
- DIN SPEC 91525: https://concular.de/dinspec91525/

### Software / Auswertung / Pass

- CircularLCA: https://concular.de/circularlca/
- Zirkuläre Ökobilanzierung: https://concular.de/zirkulaere-oekobilanzierung/
- DGNB Gebäuderessourcenpass: https://concular.de/dgnb-gebauderessourcenpass/
- Gebäuderessourcenpass: https://concular.de/gebauderessourcenpass/
- Life-Cycle Passport: https://concular.de/life-cycle-passport/
- Circularity Performance Index: https://concular.de/circularity-performance-index/
- DGNB Zertifizierung und zirkuläres Bauen: https://concular.de/dgnb-zertifizierung-und-zirkulares-bauen/

---

## 26. Noch gezielt nachzurecherchieren

1. Gibt es öffentlich zugängliche Beispiel-Exports oder Schemas für Auditdaten, PropertySets oder Passportdaten?
2. Gibt es öffentliche Vorträge, Whitepaper oder Konferenzbeiträge, die das Concular-Datenmodell genauer erklären?
3. Welche Unterschiede bestehen praktisch zwischen Beratungsleistung und Softwarefunktionalität?
4. Gibt es Fallstudien mit offen dokumentierter Datentiefe von Audit bis Wiedereinbau?
5. Wie werden unklare oder nur teilweise verifizierte Bauteile im System gekennzeichnet?
6. Gibt es dokumentierte APIs oder standardisierte Drittsoftware-Schnittstellen jenseits von IFC/Excel?
7. Wie werden Prüfberichte, Zulassungen und Gewährleistungsfragen im konkreten Projektprozess verknüpft?
