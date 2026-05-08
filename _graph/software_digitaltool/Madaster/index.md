---
id: "Madaster"
entity: "software_digitaltool"
node_kind: "core"
migration_status: "migrated_phase3_core_entities"
title: "Madaster — vertieftes Forschungsdossier"
source_count: 2
legacy_paths:
  - "akteur\\08_digitale_plattformen_daten\\Madaster.md"
  - "werkzeug\\Madaster_Plattform.md"
raw_targets:
  - "software_digitaltool/Madaster"
  - "software_digitaltool/Madaster_Plattform"
migration_actions:
  - "semantic_move"
  - "semantic_split"
risk_flags:
  - "hybrid_actor_platform_profile;duplicate_with_werkzeug_Madaster_Plattform"
  - "may_duplicate_bauteilboerse_or_akteur"
---
# Madaster — vertieftes Forschungsdossier

## Migration

- Canonical target: software_digitaltool/Madaster
- Legacy source count: 2
- Semantic note: Digitales Werkzeug oder Plattform. Bauteilboersen werden hier als Plattformprofile gefuehrt, nicht als eigene Entitaet.

## Legacy Content

### Legacy Source: akteur\08_digitale_plattformen_daten\Madaster.md

- Map action: semantic_split
- Target role in map: primary
- Raw mapped target: software_digitaltool/Madaster
- Original primary target: software_digitaltool/Madaster
- Original secondary targets: akteur/Madaster; datenmodell/Materialpass; dokumenttyp/Gebaeuderessourcenpass; tooltyp/Materialkataster

## Verknüpfungen

**Übergeordnete Themen**
- Digitale Materialkataster und Gebäuderessourcenpässe
- Dateninfrastruktur für Urban Mining
- Kreislauffähigkeit, Trennbarkeit, gebundener Kohlenstoff und materieller Restwert
- BIM/IFC, Excel-Import und objektbezogene Ressourceninventare

**Verwandte Dateien**
- `akteur/Concular.md`
- `werkzeug/Materialpass.md`
- `werkzeug/Gebaeuderessourcenpass.md`
- `werkzeug/BIM_IFC.md`
- `werkzeug/Bauteilkatalog.md`
- `werkzeug/Oekobilanz_LCA.md`
- `wirtschaft/Restwert_Bauteile.md`
- `wirtschaft/Datenoekonomie_Plattformen.md`
- `foerderprogramm/Gebaeuderessourcenpass_Pilotprogramme.md`
- `standard/DGNB_Gebaeuderessourcenpass.md`
- `standard/EN_15804.md`
- `standard/Level_s.md`

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- Akteure: Madaster, Madaster Foundation, Gebäudeeigentümer, Projektentwickler, Kommunen, Städte, BIM-Manager, Planende, DGNB, DIN, CEN/TC 350.
- Fallstudien / Projektkontexte: Materialpass- und Gebäuderessourcenpassprojekte im Neubau und Bestand; Pilotphase für Ressourcenpässe in Logistikprojekten; kommunale Materialkataster.
- Materialien: alle im Objekt erfassten Bauprodukte und Materialien, insbesondere Massivbaustoffe, Metalle, Holz, Ausbauprodukte, TGA-Komponenten und Fassaden.
- Standards / Methoden: Materialpass, Gebäuderessourcenpass, BIM/IFC, As-Built-Modell, Excel-Erfassung, LOD 300, Zirkularitätsindikatoren, Trennbarkeitsbewertung, CO₂-Bilanz, Materialwertberechnung.

## Kurzdefinition

Madaster ist eine digitale Plattform bzw. ein Materialkataster für Gebäude, Infrastruktur und andere Objekte. In Madaster werden Informationen über verbaute Materialien, Produkte und Bauteile registriert, um sichtbar zu machen, welche Ressourcen sich wo befinden, welche Kreislauffähigkeit sie besitzen, welchen gebundenen Kohlenstoff sie repräsentieren, welche Schadstoff- oder Toxizitätsrisiken bestehen können und ob sie später wiederverwendet werden können.

Für Wiederverwendung ist Madaster vor allem Dateninfrastruktur. Die Plattform vermittelt nicht primär Bauteile wie eine Börse, sondern erzeugt und strukturiert Gebäudedaten, aus denen spätere Wiederverwendungs-, Rückbau-, Sanierungs- und Bilanzierungsentscheidungen abgeleitet werden können.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung beginnt nicht erst beim Rückbau, sondern bei der Kenntnis darüber, was in Gebäuden verbaut ist. Madaster adressiert dieses Grundproblem: In vielen Bestandsgebäuden sind Materialien, Mengen, Verbindungen, Produktdaten, Schadstoffe und Demontierbarkeit unvollständig dokumentiert. Ohne solche Daten lassen sich Bauteile erst sehr spät, meist kurz vor dem Rückbau, erfassen. Dann fehlen Zeit, Marktanschluss und Planungsfreiheit.

Madaster ist relevant, weil es Ressourceninformationen über den Lebenszyklus eines Gebäudes verfügbar machen kann:

- **Neubau:** As-Built-BIM-Modelle, Leistungsverzeichnisse und Produktdaten werden in einen Material- oder Gebäuderessourcenpass überführt. Dadurch entsteht ein zukünftiger Rückbau- und Wiederverwendungsdatensatz.
- **Bestand:** Vorhandene Pläne, BIM-Modelle oder Excel-Erfassungen können genutzt werden, um ein digitales Ressourceninventar aufzubauen.
- **Portfolio:** Viele Objekte können zu einem Materialkataster zusammengeführt werden. Dadurch wird sichtbar, welche Materialien in einem Quartier, einer Kommune oder einem Portfolio vorhanden sind.
- **Bilanzierung:** Daten zu CO₂, Umweltauswirkungen, Zirkularität und finanziellen Restwerten können Nachhaltigkeitsentscheidungen unterstützen.
- **Marktvorbereitung:** Wenn Bauteile früh dokumentiert sind, können spätere Anschlussnutzungen vor Rückbau geplant werden.

Die Plattform ist also besonders stark in der Vorbereitungsphase der Wiederverwendung. Sie ersetzt jedoch nicht die bautechnische Prüfung, Demontageplanung, Logistik, Haftungsprüfung oder konkrete Vermittlung.

## Fachinhalt

### Akteursprofil

Madaster wurde 2017 in den Niederlanden von Thomas Rau gegründet. Der Name verbindet „Material“ und „Kataster“. In Deutschland wird Madaster als Cloud-Plattform für zirkuläres Bauen beschrieben, die dokumentiert, in welchen Gebäuden welche Materialien und Bauteile stecken. Nach einer DIN-Magazin-Darstellung nutzten in Deutschland rund 160 aktive Anwenderinnen und Anwender die Plattform; es wurden insgesamt etwa 5.500 Gebäude, davon etwa 1.600 in Deutschland, genannt. Diese Zahlen sind zeitgebundene Angaben und müssen bei aktueller Verwendung überprüft werden.

Madaster beschreibt sich selbst als Plattform, auf der Gebäude auf Basis von BIM-/IFC-Dateien oder Excel-Dokumenten hochgeladen werden können. Die Plattform ergänzt die Daten mit Informationen über Kreislauffähigkeit, Nachhaltigkeit und finanziellen Wert. Auf Gebietsebene kann daraus ein digitales Materialkataster entstehen.

### Rolle im ReUse-Ökosystem

Madaster nimmt eine andere Rolle ein als operative Bauteilplattformen:

- **Datenregister:** Erfassung und Strukturierung verbauter Materialien und Produkte.
- **Pass-Infrastruktur:** Erstellung von Materialpässen und Gebäuderessourcenpässen.
- **Portfolioanalyse:** Zusammenführung vieler Objekte zu Material- und CO₂-Daten auf Portfolio- oder Gebietsebene.
- **Bewertungsinstrument:** Berechnung von Zirkularität, Trennbarkeit, gebundenem CO₂, Umweltauswirkung und Materialwert.
- **Normungs- und Diskursakteur:** Beteiligung am Aufbau eines gemeinsamen Verständnisses von Gebäuderessourcenpässen, ReUse und zirkulären Informationen.

Madaster ist damit ein Enabler für spätere Wiederverwendung. Die eigentliche Wiederverwendung hängt aber von zusätzlichen Akteuren ab: Rückbauunternehmen, Prüfstellen, Planende, Marktplätze, Bauherrschaften und Genehmigungsbehörden.

### Datenquellen und Detailtiefe

Madaster kann unterschiedliche Quelldaten verarbeiten:

- **BIM/IFC-Modelle:** bevorzugt für Neubau und gut dokumentierte Bestandsgebäude; sie erlauben räumliche und elementbezogene Zuordnung.
- **As-Built-BIM:** ideal bei Übergabe, da es die tatsächlich gebaute Situation abbildet.
- **Excel-Erfassung:** Alternative für Bestandsgebäude oder Projekte ohne BIM; weniger räumlich, aber niederschwelliger.
- **Leistungsverzeichnisse und Produktdaten:** können Materialmengen und Produktinformationen ergänzen.
- **Automatisierte oder manuelle Bestandserfassung:** relevant für Bestandsobjekte mit lückenhafter Dokumentation.

Der Madaster-Leitfaden beschreibt einen Mindestanspruch von LOD 300 für BIM-Modelle. Für ReUse reicht geometrische Detailtiefe allein aber nicht aus: Zusätzlich nötig sind Zustand, Verbindung, Demontierbarkeit, Zugang, Schadstofffreiheit, Prüfzeugnisse, Wartungshistorie und Restnutzungsdauer.

### Materialpass vs. Gebäuderessourcenpass

Ein Materialpass beschreibt die im Gebäude enthaltenen Materialien und Produkte. Ein Gebäuderessourcenpass geht weiter und ordnet diese Informationen in Ressourcennutzung, Klimawirkung, Kreislauffähigkeit und potenzielle spätere Nutzung ein. Für Wiederverwendung sind beide wichtig:

- Der **Materialpass** beantwortet: Was ist verbaut, wo, in welcher Menge und mit welchen Eigenschaften?
- Der **Gebäuderessourcenpass** beantwortet zusätzlich: Welche Ressourcenwerte, Umweltauswirkungen und Kreislaufpotenziale hat das Gebäude?

In der Praxis kann ein Pass nur dann ReUse-fähig sein, wenn er nicht nur Materialmassen, sondern bauteilbezogene Informationen enthält. Eine Angabe „Beton, 3.000 t“ hilft für Recycling; für Wiederverwendung braucht es z. B. Elementabmessungen, Bewehrung, Tragverhalten, Schadstoffstatus, Demontagezugänglichkeit und Anschlagpunkte.

### Belastbare Kriterien für Madaster-Einsatz

Für die Bewertung eines Madaster-basierten ReUse-Datensatzes sind folgende Kriterien zentral:

- **Bauteilgranularität:** Werden nur Materialmassen oder einzelne Bauteile erfasst?
- **IFC-Qualität:** Sind Bauteile korrekt klassifiziert, lokalisiert und mit Mengen verknüpft?
- **Produktdaten:** Sind Hersteller, Typ, Baujahr, Leistungserklärungen, EPDs oder Prüfzeugnisse hinterlegt?
- **Demontierbarkeit:** Sind Verbindungen, Schichten, Klebungen und reversible Fügungen dokumentiert?
- **Zustand:** Gibt es Informationen zu Alterung, Schäden, Wartung und Restnutzungsdauer?
- **Schadstoffe:** Werden Schadstoffverdacht und Prüfungsergebnisse geführt?
- **Datenhoheit:** Wer besitzt, teilt, exportiert und aktualisiert die Daten?
- **Aktualisierung:** Wird der Pass im Betrieb gepflegt oder ist er nur eine Übergabedokumentation?
- **Anschlussfähigkeit:** Können Daten in Bauteilbörsen, Ausschreibungen, LCA-Tools oder Rückbaukonzepte exportiert werden?

## Praxisbezug / Beispiele

### Neubau: Pass als zukünftige Urban Mine

Bei Neubauten ist Madaster besonders geeignet, weil Planungsdaten digital vorhanden sind. Wird ein As-Built-Modell erstellt und mit Produktdaten angereichert, entsteht ein Ressourceninventar für spätere Umbauten oder Rückbauphasen. Die Wiederverwendungswirkung entsteht erst langfristig, aber die Datenkosten sind im Neubau geringer als bei späterer Rekonstruktion.

### Bestand: Inventarisierung vor Sanierung

Bei Bestandsgebäuden kann Madaster als Zielsystem für eine Materialinventur dienen. Wenn keine BIM-Daten vorhanden sind, können Excel-Tabellen, Pläne und Begehungen genutzt werden. Für ReUse sollte die Erfassung nicht nur Massen, sondern konkrete Bauteile aufnehmen: Türen, Fenster, Fassadenmodule, Stahlträger, Deckenplatten, Leuchten, Sanitärgegenstände, Systemtrennwände und andere demontierbare Produkte.

### Kommunales Materialkataster

Die Plattformlogik wird besonders relevant, wenn viele Objekte erfasst werden. Eine Kommune oder ein großer Bestandshalter kann Materialströme aus Schulen, Verwaltungsgebäuden, Wohngebäuden und Infrastrukturen sichtbar machen. Daraus können interne Wiederverwendungsstrategien entstehen: Bauteile aus einem Umbau werden in einem anderen Projekt eingeplant, bevor sie auf dem offenen Markt landen.

## Herausforderungen / offene Fragen

- **Datenlücke im Bestand:** Gerade ältere Gebäude haben unvollständige Pläne, unbekannte Schichtaufbauten und Schadstoffrisiken. Eine digitale Plattform kann diese Lücken nicht automatisch schließen.
- **Abstraktion der Zirkularität:** Indikatoren zu Zirkularität und Trennbarkeit sind nützlich, aber methodisch abhängig von Annahmen. Für wissenschaftliche Vergleiche müssen Bewertungslogik und Datenquellen offengelegt werden.
- **ReUse vs. Recycling:** Materialmassen und Materialwerte fördern oft Recyclinglogiken. Bauteilwiederverwendung braucht feinere Informationen und frühere Integration in Planung.
- **Aktualisierungspflicht:** Gebäude ändern sich laufend. Ohne Pflege verliert ein Materialpass an Aussagekraft.
- **Datenschutz und Eigentum:** Gebäudedaten können sicherheits-, eigentums- und wettbewerbsrelevant sein. Eigentümer müssen steuern können, welche Informationen geteilt werden.
- **Proprietäre Plattform:** Für öffentliche Hand und Forschung sind Exportformate, offene Schnittstellen und langfristiger Zugang entscheidend.
- **Kosten-Nutzen-Frage:** Der Nutzen eines Ressourcenpasses entsteht oft erst Jahre später. Bauherrschaften benötigen daher regulatorische, ESG- oder wirtschaftliche Anreize.

## Quellen

- Madaster Deutschland: Plattformbeschreibung, Materialkataster, Gebäuderessourcenpass, BIM-/Excel-Import. https://madaster.de/ (Abruf: 2026-04-27)
- Madaster: Leitfaden Materialpass / Ausschreibungstext für Materialpass und Bauakte. https://docs.madaster.com/files/ch/de/Tender%20Text%20Material%20Passport_CH-DE.pdf (Abruf: 2026-04-27)
- DIN-Magazin: „Ihren Gebäuderessourcenpass, bitte!“ mit Angaben zu Madaster, Plattform, Gebäudedaten und Normungsbezug. https://din-magazin.de/digitalisierung/bim/ihren-gebaeuderessourcenpass-bitte/ (Abruf: 2026-04-27)
- DGNB: Gebäuderessourcenpass, Diskussionsgrundlagen und Kriterien zur Ressourcennutzung, Klimawirkung und Kreislauffähigkeit.
- CEN/TC 350: Sustainability of construction works; europäische Normungsarbeit zu zirkulären Informationen im Bauwesen.
- EN 15804: Umweltproduktdeklarationen für Bauprodukte als Datenbasis für ökobilanzielle Bewertungen.

---

## Vertieftes Forschungsdossier

Quelle: `reuse/research/akteur/Research/Madaster_detailed.md`

---
tags:
  - madaster
  - material-passport
  - circularity-indicator
  - bim
  - ifc
  - api
  - residual-value
  - metadata
aliases:
  - Madaster
status: draft-researched
entity-type: Datenplattform / Materialpass-System
research-depth: very-deep
based-on: 03_Madaster.md
last-updated: 2026-04-23
---

# Madaster — vertieftes Forschungsdossier

> Arbeitsstand: Dieses Dossier vertieft das bestehende Profil zu Madaster um Datenarchitektur, Plattformlogik, Pass- und Dossierstruktur, Circularity- und Environmental-Bewertung, API-/Datenbankfragen sowie die spezifische Relevanz für ein Forschungsvorhaben zu „Entwerfen mit Bestand“. Wo Primärquellen keine belastbaren Details liefern, wird das explizit markiert.

## 1. Executive Summary

Madaster ist für Entwerfen mit Bestand vor allem als **persistente Dateninfrastruktur für Materialien, Produkte, Elemente und Gebäude** relevant. Im Unterschied zu materialflussorientierten Re-Use-Plattformen oder auditgetriebenen Pre-Demolition-Akteuren liegt seine Stärke öffentlich sichtbar weniger in der kurzfristigen Vermittlung verfügbarer Bauteile, sondern in der **langfristigen digitalen Dokumentation, Anreicherung, Bewertung und Berichterstattung** von Gebäuderessourcen.

Der Fall ist besonders wertvoll, weil Madaster mehrere Ebenen zusammenführt:

1. **Datenaufnahme über IFC oder Excel**,
2. **Klassifikations- und Mappinglogiken**,
3. **Verknüpfung mit Datenbanken für Materialien und Produkte**,
4. **Bewertung über Circularity, Environmental und Financial/Residual Value**, 
5. **Material Passport / Dossier / PDF- und Excel-Exporte**,
6. **API- und Datenbankstrukturen für längere Datenlebenszyklen**.

Madaster zeigt damit sehr gut, wie Gebäude als **dauerhafte Informationscontainer für Ressourcen** modelliert werden können. Für Entwerfen mit Bestand ist das zentral, weil hier ein Referenzfall entsteht für die Frage, wie aus Planungs- und Bestandsdaten eine **persistente Materialerinnerung** wird.

Gleichzeitig macht der Fall eine wichtige Grenze deutlich: Öffentlich ist Madaster viel stärker als **Pass-, Daten- und Bewertungsplattform** greifbar als als **verfügbarkeitsgetriebenes Entwurfswerkzeug**. Genau diese Differenz ist forschungsrelevant: Madaster speichert und bewertet Ressourcen sehr systematisch, aber die Übersetzung in ein dynamisches, unsicherheitsfähiges Re-Use-Design-Interface bleibt öffentlich nur begrenzt sichtbar.

---

## 2. Institutionelle Einordnung: Was für ein Akteur ist Madaster?

Madaster beschreibt sich als Plattform für „circular real estate and infrastructure“. Diese Selbstbeschreibung ist wichtig, weil sie zwei Dinge signalisiert:

- Der Fokus liegt nicht nur auf Gebäuden, sondern auch auf Infrastrukturen.
- Das System versteht sich nicht nur als Materialdatenbank, sondern als umfassendere Informations- und Bewertungsumgebung für zirkuläre Assets.

### Charakter des Akteurs
Madaster erscheint öffentlich als Kombination aus:
- **Plattformanbieter**,
- **Daten- und Bewertungsinfrastruktur**,
- **Materialpass-System**,
- **Circularity-/LCA-/Financial-Analytics-Umgebung**,
- **Schnittstellen- und Integrationslayer** zwischen BIM, Klassifikationen und Datenbanken.

### Was Madaster gerade nicht primär ist
Öffentlich weniger sichtbar ist Madaster als:
- akteursnahe Rückbaukoordination,
- Marktplatz für kurzfristig verfügbare Re-Use-Komponenten,
- bauteilscharfer Verfügbarkeitsmanager,
- primär ingenieurtechnische Prüfplattform.

### Warum das für Entwerfen mit Bestand entscheidend ist
Madaster ist kein Fall für „Wo finde ich morgen verfügbare Fenster?“, sondern eher ein Fall für:
**Wie speichere, klassifiziere, bewerte und exportiere ich Ressourceninformationen so, dass Gebäude langfristig als Materialbanken lesbar werden?**

---

## 3. Warum Madaster für „Entwerfen mit Bestand“ wichtig ist

Madaster ist für Entwerfen mit Bestand aus mindestens sechs Gründen hoch relevant:

### 3.1 Persistenz statt Momentaufnahme
Madaster adressiert nicht nur einen Rückbau- oder Planungsmoment, sondern die Idee, dass Ressourceninformationen über die Zeit verfügbar bleiben.

### 3.2 Trennung mehrerer Datenebenen
Material-, Produkt-, Element- und Objektebene werden sichtbar unterschieden. Diese Differenzierung ist methodisch sehr wichtig für reuse-orientierte Forschung.

### 3.3 Interoperabilität
Madaster verarbeitet IFC- und Excel-Quellen und koppelt diese mit Klassifikationen, Datenbanken, Exporten und APIs.

### 3.4 Circularity, Umweltwirkung und Restwert
Der Fall zeigt, wie Ressourceninformationen nicht nur archiviert, sondern über Kennzahlen und Berichte in Nachhaltigkeits- und Wirtschaftlichkeitslogiken überführt werden.

### 3.5 Qualitätsbewusstsein
Die Dokumentation betont immer wieder die Qualität des Quellbestands, Vollständigkeit und die Grenzen schlechter Inputs. Das ist forschungspraktisch extrem wichtig.

### 3.6 Gute Negativfolie für den Entwurfsdiskurs
Gerade weil Madaster so stark in Dokumentation und Bewertung ist, hilft der Fall dabei, die Frage zu schärfen, **was zusätzlich nötig wäre, damit Passdaten zu echtem Entwurfsinput werden**.

---

## 4. Die Grundlogik von Madaster: von Quelldaten zu Pässen und Kennzahlen

Die öffentlich dokumentierte Plattformlogik lässt sich als Pipeline lesen:

1. **Objekt anlegen**
2. **Quelldateien vorbereiten**
3. **IFC oder Excel hochladen**
4. **Klassifikationsmethode wählen**
5. **Datenbanken zur Anreicherung auswählen**
6. **Datenqualität und Vollständigkeit prüfen**
7. **Kennzahlen berechnen**
8. **Materialpässe, Dossiers und Exporte erzeugen**
9. **Daten über Plattform, Dateien und API weiterverwenden**

### Warum diese Logik wichtig ist
Madaster ist kein „nur anzeigen“-Tool. Es ist eine **Transformationskette**:
- Rohdaten werden strukturiert,
- Strukturen werden angereichert,
- angereicherte Daten werden interpretiert,
- Interpretationen werden in Berichts- und Austauschformate übersetzt.

### Forschungsperspektive
Für Entwerfen mit Bestand ist dies ein sehr gutes Beispiel für die Frage, wie aus Bestands- und Planungsdaten nicht nur Sichtbarkeit, sondern **persistente Entscheidungs- und Dokumentationsfähigkeit** entsteht.

---

## 5. Objekte, Konten, Ordner, Gebäude: die Plattformhierarchie

Ein auffällig wichtiger Aspekt bei Madaster ist die hierarchische Plattformstruktur.

### Öffentlich sichtbare Ebenen
Die Dokumentation beschreibt eine flexible Struktur aus:
- **Account**,
- **Folder**,
- **Subfolder**,
- **Buildings / Infra Objects / Projects**.

Außerdem können Datenbanken auf unterschiedlichen Ebenen hängen:
- Account-Level,
- Folder-Level,
- Project/Object-Level.

### Warum das für Forschung relevant ist
Diese Hierarchie ist kein Nebenprodukt, sondern ein Hinweis auf die eigentliche Zielsetzung der Plattform: nicht nur ein Einzelgebäude dokumentieren, sondern **Portfolios und Objektlandschaften** strukturieren.

### Forschungsableitung
Madaster ist deshalb nicht nur für ein Objekt interessant, sondern für Fragen wie:
- Wie lassen sich Ressourceninformationen über Portfolios organisieren?
- Wie wird Wissen zwischen Projekten geteilt?
- Wie können Datenbanken objektübergreifend oder projektspezifisch wirken?

Gerade für Eigentümer:innen, Bestandshalter:innen und größere öffentliche/private Portfolios ist das ein starkes Modell.

---

## 6. Datenquellen: IFC und Excel sind nicht gleichwertig

Die Dokumentation ist hier ungewöhnlich klar.

### IFC als bevorzugte Quelle
Madaster betont, dass BIM/IFC für Neubau und Renovierung die größten Vorteile bietet. IFC ermöglicht vor allem die Berechnung von Mengen und eine räumlich / modellbezogene Verarbeitung der Elemente.

### Excel als pragmatische Alternative
Für Bestandsobjekte können Zeichnungen und Leistungsverzeichnisse auch in die Madaster-Excelvorlage übertragen werden. Die Dokumentation sagt jedoch klar: **Wenn Excel als Quelle genutzt wird, kann auf der Plattform keine 3D-Repräsentation des Objekts erzeugt werden.**

### Forschungsbedeutung
Das ist für Entwerfen mit Bestand zentral, denn es macht deutlich:
- Passlogik ist auch **ohne** 3D-Modell möglich.
- Entwurfs- und Geometrieinteraktion profitieren aber stark von modellbasierten Quellen.

### Wichtige Schlussfolgerung
Madaster trennt implizit zwischen:
- **dokumentationsfähigem Ressourcenwissen** und
- **modellierbarem/geometrisch verortetem Ressourcenwissen**.

Das ist eine sehr wichtige Unterscheidung für Entwerfen mit Bestand.

---

## 7. IFC-Anforderungen: was Madaster wirklich von Modellen erwartet

Die IFC-Dokumentation ist besonders ergiebig, weil sie konkrete Anforderungen nennt.

### Grundanforderungen an IFC-Modelle
Alle Elemente sollen enthalten:
- **Unique GUIDs**,
- **geometrische Eigenschaften / base quantities**,
- **Material description**,
- **classification coding**.

Außerdem empfiehlt Madaster:
- korrekten IFC-Type,
- Vermeidung von „Building element proxy“ und „Building element part“,
- Export von Renovation Status / Phasing,
- bevorzugt IFC4 Design Transfer View, alternativ IFC2x3,
- lokale Modellkoordinaten nahe dem Ursprung.

### CPset_Madaster
Besonders relevant ist, dass Madaster eigene IFC-Property-Logiken ausliest. In der aktuellen Doku werden im `CPset_Madaster` u. a. genannt:
- Classification,
- Phase,
- BuildingNumbers,
- DetachabilityConnectionType,
- DetachabilityAccessibility,
- DetachabilityIntersection,
- DetachabilityProductEdge,
- LifeSpan,
- InstallationDate,
- SerialNumber,
- TechnicalCondition,
- AestheticCondition,
- Comment,
- AvailableForReuse,
- WasteCodes,
- AssumedConstructionWaste,
- OverOrdering,
- MaterialOrProductId,
- externaldatabaseId,
- GTIN,
- MaterialOrProductName,
- MaterialOrProductRatio.

### Warum diese Liste forschungslogisch so stark ist
Diese Felder zeigen, dass Madaster nicht nur klassische BIM-Mengenlogik verfolgt, sondern versucht, zusätzliche reuse- und zirkularitätsrelevante Eigenschaften abzubilden, z. B.:
- technische und ästhetische Zustandsbewertung,
- Loslösbarkeit / Detachability,
- Verfügbarkeit für Wiederverwendung,
- Abfallcodes,
- Produktidentität,
- Installation / Lebensdauer.

### Forschungsthese
Madaster ist damit deutlich näher an einer **zirkulären Informationsanreicherung** von BIM, als es die Kurzbeschreibung zunächst vermuten lässt. Gleichzeitig bleibt offen, wie tief und konsequent diese Felder in realen Projekten tatsächlich gepflegt werden.

---

## 8. Material-, Produkt-, Element- und Gebäudeebene

Einer der stärksten analytischen Punkte bei Madaster ist die erkennbare Unterscheidung mehrerer Informationsebenen.

### 8.1 Materialebene
Hier geht es um Stoffe, Zusammensetzungen, Massen, Umweltwirkungen, Rezyklat-/Reuse-Anteile usw.

### 8.2 Produktebene
Hier werden konkrete Produkte oder Produktdatensätze relevant, etwa mit IDs, GTIN, Bill of Materials, Environmental-, Circularity- und Financial-Tabs.

### 8.3 Elementeebene
Elemente sind die im Modell oder in der Datei verorteten Objekte eines Gebäudes. Sie sind Träger von Mengen, Klassifikation, Phaseninformationen und Zuordnungen.

### 8.4 Gebäude-/Objektebene
Hier aggregiert Madaster zu Pass, Dossier, Performance, Circularity, Umweltwirkung, Vergleich und Portfolioeinsicht.

### Warum das so wichtig ist
Viele Re-Use-Diskurse vermischen Material, Produkt und Bauteil. Madaster macht diese Trennung systematisch sichtbarer. Für das Forschungsprojekt Entwerfen mit Bestand ist das extrem relevant, weil unterschiedliche Fragen unterschiedliche Ebenen brauchen:
- Entwurfsfrage: eher Element-/Bauteilebene,
- Stofffrage: Materialebene,
- Produktverantwortung: Produktebene,
- Reporting/Portfolio: Gebäudeebene.

---

## 9. Klassifikation als zentrales Rückgrat

Madaster betont mehrfach, dass eine Klassifikation notwendig ist, damit Elemente den richtigen Gebäudeschichten bzw. „shearing layers“ zugeordnet werden können.

### Warum Klassifikation hier zentral ist
Klassifikation ist bei Madaster nicht bloß Ordnung, sondern Voraussetzung für:
- Auswertung nach Schichten,
- Vergleichbarkeit,
- Mapping auf Datenbanken,
- Kennzahlenbildung,
- Dossier- und Passportstruktur.

### Forschungsperspektive
Für Entwerfen mit Bestand ist das wichtig, weil jede reuse-orientierte Datenplattform irgendwann entscheiden muss, **welche Ordnungssysteme** sie benutzt. Madaster zeigt sehr gut, dass diese Ordnungen nicht neutral sind: Sie strukturieren, was später sichtbar, vergleichbar und bewertbar wird.

### Offene Frage
Was für frühe reuse-basierte Entwurfsprozesse am hilfreichsten ist, bleibt offen. Klassifikationen, die gut für LCA und Reporting funktionieren, sind nicht automatisch optimal für materialgetriebenes Entwerfen.

---

## 10. Datenbanken: verified, supplier, customer

Die Datenbanklogik von Madaster ist ungewöhnlich wichtig.

### Öffentlich unterscheidbare Typen
Madaster unterscheidet:
- **Verified databases**,
- **Supplier databases**,
- **Customer databases**.

### Verified databases
Diese wirken wie system- oder qualitätsgesicherte Datenquellen, z. B. mit Verweis auf EPEA oder Ökobaudat-Bezüge.

### Supplier databases
Diese können produktbezogene Informationen, Produktdateien und Track-&-Trace-relevante Rückkopplungen enthalten.

### Customer databases
Kund:innen können eigene Datenbanken anlegen und für Gebäude oder Projekte verwenden.

### Besonders interessant: Sharing-Logiken
Für Supplier-Datenbanken nennt Madaster Sharing-Optionen wie:
- Open,
- Sharing with opt-out,
- Datasharing.

Außerdem können Rechte an bestimmten Produktinformationen gesteuert werden, etwa Sichtbarkeit von:
- Bill of Materials,
- Circularity tab,
- Environmental tab,
- Financial tab,
- Product files.

### Forschungsperspektive
Das zeigt, dass Madaster nicht nur ein Berechnungstool ist, sondern eine **Daten-Governance-Plattform**. Daten haben hier Herkunft, Eigentum, Sichtbarkeit, Teilbarkeit und Nutzungsrechte.

Das ist für Entwerfen mit Bestand hoch relevant, denn materialbasierte Entwurfs- und Re-Use-Systeme scheitern oft nicht an Rechenlogik, sondern an **Datenzugang und Rechtestruktur**.

---

## 11. Source file quality: Qualität ist kein Nebenthema

Madaster macht ungewöhnlich deutlich, dass die Aussagekraft der Plattform von der Güte des Quellbestands abhängt.

### Dokumentierte Qualitätslogik
Die Doku zur Quellbestandsqualität betont, dass geringe Datenqualität und Unvollständigkeit direkt die Genauigkeit und Vollständigkeit der Plattformresultate mindern.

### Sichtbare Qualitätsaspekte
Öffentlich erkennbar sind u. a. Bewertungen nach:
- Klassifikationsabdeckung,
- Vollständigkeit von Informationen,
- Abdeckung nach Anzahl/Volumen,
- unbekannte Elemente als eigene Problemkategorie.

### Warum das methodisch wichtig ist
Madaster ist damit ein starker Fall gegen die Illusion, dass digitale Pässe automatisch präzise seien. Die Plattform macht explizit, dass Outputqualität vom Input abhängt.

### Forschungsschluss
Für Entwerfen mit Bestand könnte daraus folgen, dass ein reuse-orientiertes Entwurfswerkzeug immer auch eine **Datenqualitätsanzeige** oder Unsicherheitsvisualisierung braucht — nicht nur schöne Materiallisten.

---

## 12. Material Passports: Formate, Tiefe, Funktion

Die Pass-Logik gehört zum Kern von Madaster.

### Dokumentierte Passport-Typen
Madaster nennt mehrere Formate:
- **One-pager**,
- **Executive summary**,
- **Passport**,
- **Web-based Passport**.

### Unterschiedliche Detailstufen
- One-pager: minimale Verdichtung auf einer Seite,
- Executive summary: etwas detaillierter,
- Full passport: weitgehend vollständige PDF-Übersetzung der Plattforminformationen,
- Web-based passport: teilbarer Weblink ohne Login in die Plattform.

### Technischer Anhang / Excel
Materialpässe können einen technischen Annex mit Basisdaten als Excel enthalten. Außerdem können Informationen wie Circularity, Materials, Financial und Environmental KPIs gezielt in den Pass aufgenommen werden.

### Was das zeigt
Der Pass ist bei Madaster kein starres Dokument, sondern ein **konfigurierbarer Ausgabemodus** für unterschiedliche Öffentlichkeiten:
- schnelle Kommunikation,
- Managementzusammenfassung,
- technische Tiefe,
- externe Teilbarkeit.

### Forschungsperspektive
Für dein Thema bedeutet das: Ein Pass ist weniger ein „einziges Dokument“ als eine **Interface-Familie zwischen Datenhaltung und Kommunikation**.

---

## 13. Das Dossier als Dateispeicher und Evidenzschicht

Das Dossier ist ein weiterer wichtiger Baustein.

### Was im Dossier sichtbar ist
Die Doku beschreibt, dass dort verschiedene Dateitypen verwaltet werden:
- **Source files** (IFC/Excel),
- **General files**,
- **Material passports**.

General files können auch Management- und Arbeitsdokumente, Zertifikate oder Garantien sein.

### Forschungsperspektive
Das ist sehr interessant, weil Madaster damit nicht nur numerische Auswertung betreibt, sondern eine **Dokumenten- und Evidenzschicht** anbietet. Für zirkuläres Bauen ist das zentral: Materialinformationen sind oft auf mehrere Dokumente verteilt.

### Relevanz für Re-Use-Forschung
Ein Dossier kann langfristig wichtig werden, wenn Bauteile oder Produkte später wieder in neue Re-Use-Kontexte übergehen. Öffentlich bleibt jedoch offen, wie bauteilscharf solche Dokumente mit konkreten Elementen verknüpft werden.

---

## 14. Circularity Indicator: was gemessen wird — und was nicht

Madasters Circularity Indicator ist einer der sichtbarsten Bewertungsbausteine.

### Öffentliche Logik
Die Doku beschreibt die Circularity Indicator / MCI-Logik mit einer Skala von 0–100 %. Ein vollständig linearer Bau aus neuen Materialien mit Deponie-/Verbrennungsende läge bei 0 %, ein vollständig aus wiederverwendeten/recycelten Materialien aufgebautes und künftig vollständig wiederverwendbares Gebäude bei 100 %.

### Bewertete Phasen
Je nach Dokumentationsseite wird der Indicator über zwei bzw. teilweise drei Lebensphasen beschrieben:
- Materialien zur Herstellung / Konstruktion,
- Nutzungs-/Lebensdauerbezug,
- End-of-life mit Reuse, Recycling, Landfill/Incineration.

### Wichtige Hinweise
- Die Kennzahl basiert auf dem Material Circularity Indicator (MCI) der Ellen MacArthur Foundation.
- Sie wird aus den **aktiven Quelldateien** des Gebäudes berechnet.
- Die **Qualität der Quellinformationen** bestimmt die Zuverlässigkeit des Indicators.
- Werte können auf verschiedenen Ebenen und Schichten dargestellt werden.

### Forschungsperspektive
Der Circularity Indicator ist für Entwerfen mit Bestand wichtig, weil er komplexe Materialbiografien in eine handhabbare Kennzahl überführt. Gleichzeitig ist genau das auch die methodische Grenze: Er verdichtet Vielschichtigkeit zu einem Score.

### Offene Forschungsfragen
- Wie robust ist der Indicator bei unscharfen Bestandsinformationen?
- Wie stark nivelliert er Unterschiede zwischen sehr verschiedenartigen Re-Use-Szenarien?
- Hilft er wirklich im frühen Entwurf oder eher in Vergleich, Kommunikation und Reporting?

---

## 15. Environmental: embodied carbon und LCA-Perspektive

Madaster ist öffentlich auch stark als Environmental-Analytics-System präsent.

### Öffentlich sichtbare Inhalte
Die Environmental-Ansicht zeigt laut Doku:
- totale Umweltwirkung eines gewählten KPI,
- Umweltwirkung pro m² bzw. m²·Jahr,
- Vergleich mit Benchmarks,
- unbekannte Elemente als korrigierbare Kategorie,
- Auswertung nach Gesamtwert, Schichten und Material/Produkt.

### Lebenszyklusbezug
Die Dokumentation nennt LCA-Phasen entlang der Gebäudelebensdauer; A1-A3 wird besonders hervorgehoben, weil diese Daten meist am breitesten verfügbar sind und deshalb Vergleichbarkeit erleichtern.

### Forschungsperspektive
Madaster zeigt damit sehr gut, wie Material- und Produktdaten in **environmental performance views** überführt werden. Für das Forschungsprojekt Entwerfen mit Bestand ist das wichtig, weil Re-Use nicht nur über Verfügbarkeit, sondern auch über Embodied Carbon und Whole-Life-Argumente relevant wird.

### Wichtige Grenze
Öffentlich bleibt dennoch unklar, wie tief reuse-spezifische Sonderfälle modelliert sind, etwa:
- unvollständige Herkunftsdaten,
- teilweise wiederverwendete Baugruppen,
- variable Aufbereitungsaufwände,
- projektabhängige Substitutionslogiken.

---

## 16. Financial / Residual Value

Ein oft unterschätzter Aspekt bei Madaster ist die finanzielle Bewertung.

### Dokumentierte Logik
Die Berechnungsdokumentation beschreibt Residual-Value-/Financial-Logiken mit:
- Current value,
- Net present value (NPV),
- Trend Value,
- Korrekturfaktoren für Abbruch, Transport und weitere Einflüsse.

### Warum das für dein Thema relevant ist
Madaster behandelt Materialien nicht nur als ökologische, sondern auch als **zukünftige Wertträger**. Das ist ein Schlüsselmoment der Materialpass-Idee: Gebäude werden nicht nur als Kosten- oder Emissionsobjekte, sondern auch als **Ressourcenlager mit monetarisierbarem Restwert** gelesen.

### Forschungsperspektive
Für Entwerfen mit Bestand ist das doppelt interessant:
- Es erweitert Re-Use um eine ökonomische Argumentation.
- Es zeigt, dass Dateninfrastrukturen für zirkuläres Bauen zunehmend auch **Finanzialisierung von Materialwissen** ermöglichen.

### Kritische Frage
Wie stabil oder belastbar solche Wertannahmen über lange Zeithorizonte und heterogene Marktbedingungen sind, bleibt offen und wäre interviewwürdig.

---

## 17. API und technische Offenheit

Madaster hat öffentlich dokumentierte API-Zugänge.

### Was öffentlich klar ist
- Es gibt eine API mit dokumentiertem Endpoint.
- Zugriff erfolgt per `X-API-Key`.
- Tokens können im Plattformkontext auf verschiedenen Ebenen erzeugt werden.
- Die API deckt laut Doku **noch nicht alle Funktionen der Plattform vollständig** ab.
- Es existiert eine OpenAPI-Dokumentation und ein GitHub-Beispielbezug.

### Warum das wichtig ist
Madaster ist damit nicht bloß eine geschlossene GUI-Plattform, sondern zumindest teilweise programmatisch zugänglich. Für Forschung und Tool-Prototyping ist das ein entscheidender Unterschied.

### Gleichzeitig relevante Einschränkung
Dass die API nicht alle Plattformfunktionen abdeckt, ist forschungspraktisch wichtig. Es heißt:
- Nicht jede sichtbare Plattformfunktion ist automatisch integrierbar.
- Externe Forschungsworkflows sind möglich, aber vermutlich selektiv.

### Forschungsperspektive
Für Entwerfen mit Bestand eröffnet das die Frage, ob Madaster eher als:
- vollständige Integrationsplattform,
- teiloffene Datenquelle,
- oder Export-/Berichtssystem
verwendbar wäre.

---

## 18. Re-Use-Spezifität: überraschend vorhanden, aber nicht dominant

Auf den ersten Blick wirkt Madaster nicht wie eine Re-Use-Plattform. Bei genauerem Hinsehen tauchen jedoch reuse-nahe Attribute auf.

### Sichtbare reuse-/circularity-nahe Felder
- `AvailableForReuse`,
- Zustandsfelder (`TechnicalCondition`, `AestheticCondition`),
- `Detachability...`-Felder,
- `WasteCodes`,
- `InstallationDate`,
- `LifeSpan`,
- Produkt- und Materialidentitäten,
- End-of-life reuse/recycling-Logiken im Circularity Indicator.

### Was das bedeutet
Madaster ist nicht primär ein Marktplatz für gebrauchte Bauteile, aber die Plattform enthält öffentlich sichtbare Strukturen, die reuse-relevante Informationen aufnehmen können.

### Zentrale Forschungserkenntnis
Madaster ist deshalb ein guter Fall für **latent reuse-fähige Passlogik**: Viele der nötigen Datenfelder existieren oder sind andeutungsweise anschlussfähig, aber die Plattform ist öffentlich eher auf Persistenz, Bewertung und Reporting als auf dynamische Re-Use-Vermittlung und Entwurfsinteraktion ausgerichtet.

---

## 19. Entwurfsrelevanz: wie nah ist Madaster am Design?

Das ist die wichtigste Frage für Entwerfen mit Bestand.

### Was für Entwurfsnähe spricht
- IFC-Modelle und 3D-bezogene Verarbeitung,
- Material-/Produkt-/Elementstruktur,
- Varianten- und Performance-Sichten in der Plattform,
- environmental / circularity / financial insights,
- Portfolio- und Vergleichsfunktionen,
- Exportierbarkeit und Datenpersistenz.

### Was gegen direkte Entwurfsorientierung spricht
- starke Betonung von Dokumentation, Bewertung und Reporting,
- keine öffentlich dominante Positionierung als Entwurfs- oder Formfindungswerkzeug,
- begrenzte Sichtbarkeit von Verfügbarkeits- und Reservierungslogiken,
- wenig öffentliche Hinweise auf architektonische Generierung oder aktives Re-Use-Matching.

### Forschungsschluss
Madaster ist eher eine **Design-unterstützende Wissensinfrastruktur** als ein entwurfsaktives Tool. Es ist stark in Fragen wie:
- Was ist vorhanden?
- Wie ist es klassifiziert?
- Wie vollständig sind die Daten?
- Welche Umwelt- und Circularity-Wirkungen ergeben sich?
- Was kann ich berichten und exportieren?

Weniger sichtbar ist:
- Was entwerfe ich aus diesen spezifischen vorhandenen Beständen?
- Wie gehe ich mit unscharfer Verfügbarkeit und Gestaltvarianz um?
- Wie beeinflusst Materialheterogenität meine architektonische Formfindung?

### Exakte Forschungslücke
Madaster ist ein sehr starker Referenzfall für **persistente Ressourcenintelligenz**, aber kein klarer Beleg für **availability-driven design interaction**.

---

## 20. Vergleich zu Concular, BIM Berlin und anderen Fällen

### Gegenüber Concular
Madaster ist stärker auf dauerhafte Pass- und Bewertungslogik, Objekt-/Portfoliostruktur und Plattformpersistenz ausgerichtet. Concular wirkt stärker audit-, Anschlussnutzungs- und umsetzungsnah.

### Gegenüber BIM Berlin
BIM Berlin ist materialquellen- und vermittlungsnäher. Madaster ist dateninfrastrukturell stärker, aber weniger als konkrete Re-Use-Börse sichtbar.

### Gegenüber Community-Re-Use-Akteuren
Im Unterschied zu Akteuren wie Kunst-Stoffe oder Haus der Materialisierung operiert Madaster viel systematischer auf Ebene von Datenschemata, Passformaten und Kennzahlen, nicht primär über physische Materialkuration.

### Gegenüber technischen Prüfern / Engineering-Akteuren
Madaster fokussiert öffentlich eher Datenstruktur und Bewertung als tragwerks- oder bauordnungsnahe Wiederverwendungsfreigabe.

---

## 21. Kritische Lücken und offene Fragen

Trotz guter Dokumentation bleiben wesentliche Punkte offen.

### 21.1 Offenes logisches Datenmodell
Die Doku zeigt viele Felder und Funktionen, aber kein vollständig offenes, forschungsfreundlich dokumentiertes Datenmodell mit Entitäten, Relationen, Pflichtfeldern und Versionierung.

### 21.2 Unsicherheitsmodellierung
Öffentlich nicht klar ist, wie Unsicherheiten bei Materialzuordnung, Zustandsannahmen, Schätzmengen oder fehlenden Produktdaten formal modelliert werden.

### 21.3 Re-Use-Verfügbarkeit als Zeitstatus
Felder wie `AvailableForReuse` existieren, aber eine ausgeprägte Statuslogik für Reservierung, Lagerung, Verfall, Verkauf oder terminliche Verfügbarkeit ist öffentlich nicht deutlich sichtbar.

### 21.4 Reale Nutzung der erweiterten IFC-Felder
Öffentlich unklar bleibt, wie häufig und in welcher Qualität Felder wie TechnicalCondition, Detachability oder WasteCodes in Praxisprojekten tatsächlich befüllt werden.

### 21.5 API-Tiefe
Es gibt API-Zugang, aber nicht volle Funktionsabdeckung. Für externe Forschung ist unklar, welche Teile der Plattform wirklich granular ausles- oder beschreibbar sind.

### 21.6 Tragwerk / Nachweis
Öffentlich liegt der Schwerpunkt nicht auf reuse-spezifischer technischer Freigabe oder strukturellem Nachweis.

---

## 22. Konkrete Forschungsableitungen für Entwerfen mit Bestand

## 22.1 Madaster als Referenz für Datenpersistenz
Um Folgendes zu verstehen: wie Ressourcenwissen über Jahre projekt- und objektbezogen gespeichert werden kann, ist Madaster ein sehr starker Fall.

## 22.2 Madaster als Referenz für Ebenentrennung
Die Plattform ist besonders hilfreich, um Material-, Produkt-, Element- und Gebäudeebene voneinander zu unterscheiden.

## 22.3 Madaster als Referenz für passfähige Exporte
Für Fragen nach Dokumentation, Berichtbarkeit, Austausch und Governance ist der Fall hoch relevant.

## 22.4 Madaster als unvollständige Antwort auf Re-Use-Entwurf
Für availability-driven design, Unsicherheit, dynamische Materialverfügbarkeit und entwerfende Materialinteraktion liefert Madaster öffentlich nicht die ganze Antwort. Genau deshalb ist der Fall forschungsstrategisch wertvoll.

## 22.5 Für ein eigenes Tool
Ein Tool zum „Entwerfen mit Bestand“ könnte Madaster-artige Daten- und Passlogiken übernehmen, müsste aber zusätzlich leisten:
- Unsicherheitsvisualisierung,
- Verfügbarkeitsstatus,
- Reservierungs- und Lagerlogik,
- geometrisches Matching,
- entwurfsaktive Variantenräume,
- Kopplung von Bestand und Gestaltbildung.

---

## 23. Präzisierte Interviewfragen

### Zu Datenmodell und Ebenen
1. Wie unterscheiden sich in Madaster Material-, Produkt-, Element- und Objektebene technisch und praktisch?
2. Welche minimale Datentiefe ist nötig, um einen belastbaren Materialpass zu erzeugen?
3. Welche Felder sind Pflicht, welche nur optional oder projektabhängig?
4. Gibt es formale Datenqualitätsstufen oder Confidence-Levels?

### Zu IFC und Excel
5. Wann ist Excel in der Praxis ausreichend und wann zwingt die Anforderung an Erkenntnistiefe zu IFC/BIM?
6. Welche Informationen gehen beim Wechsel von IFC zu Excel typischerweise verloren?
7. Wie stark werden CPset_Madaster-Felder in echten Projekten genutzt?
8. Welche Felder fehlen aus Sicht von Re-Use-Forschung heute noch?

### Zu Circularity / Environmental / Financial
9. Wie belastbar ist der Circularity Indicator bei lückenhaften Bestandsdaten?
10. Wie werden unbekannte Elemente behandelt, bevor sie in die Berechnungen einfließen?
11. Wie robust sind Residual-Value-Annahmen über lange Zeiträume?
12. Welche KPI-Konfigurationen sind für Re-Use-Projekte am nützlichsten?

### Zu Re-Use und Verfügbarkeit
13. Wie würde Madaster bauteilscharfe Wiederverwendungsoptionen, Zustand und Verfügbarkeit idealerweise modellieren?
14. Gibt es bereits reale Anwendungen mit `AvailableForReuse` und zustandsbezogenen Feldern?
15. Wie ließe sich Reservierung, Lagerstatus oder zeitliche Verfügbarkeit in die Plattform integrieren?

### Zu API und Offenheit
16. Welche Daten können heute real via API gelesen oder geschrieben werden?
17. Welche Plattformbereiche sind bewusst nicht per API verfügbar?
18. Wie offen ist Madaster für externe Forschungsworkflows oder Prototypen?

### Zu Entwurf und Planung
19. Wird Madaster heute schon aktiv in Vorentwurfsprozessen genutzt oder eher in Dokumentation und Nachweis?
20. Was müsste sich ändern, damit Passdaten zu echtem Entwurfsinput werden?
21. Welche Darstellung von Unsicherheit oder Verfügbarkeit wäre für Planende am nützlichsten?

---

## 24. Arbeits-Hypothesen für die weitere Forschung

1. **Madaster ist einer der stärksten Referenzfälle für datenpersistente Passlogik im zirkulären Bauen.**
2. **Die eigentliche Stärke liegt in Klassifikation, Anreicherung, KPI-Bildung und Export, nicht primär in kurzfristiger Re-Use-Vermittlung.**
3. **Die klare Trennung von Material-, Produkt-, Element- und Gebäudeebene ist methodisch besonders wertvoll für reuse-orientierte Forschung.**
4. **Die Plattform ist reuse-fähiger, als sie auf den ersten Blick wirkt, weil sie bereits zustands-, loslösbarkeits- und verfügbarkeitsnahe Felder vorsieht.**
5. **Trotzdem bleibt öffentlich eine Lücke zwischen Pass-/KPI-Logik und wirklich entwurfsaktiver Arbeit mit verfügbaren Beständen.**
6. **Ein künftiges Forschungswerkzeug könnte Madaster als Datenrückgrat nutzen, müsste aber Unsicherheit, Geometrie und Verfügbarkeit viel stärker nach vorn holen.**

---

## 25. Priorisierung für Entwerfen mit Bestand

### Priorität: sehr hoch
Madaster sollte in der Akteurslandschaft von Entwerfen mit Bestand **sehr hoch priorisiert** werden, wenn fur Entwerfen mit Bestand folgende Themen zentral sind:
- Materialpass,
- Datenpersistenz,
- Interoperabilität,
- Klassifikation,
- Export-/Berichtssysteme,
- KPI- und Bewertungslogik,
- Portfolio- und Objektstruktur.

### Etwas geringer priorisiert, wenn …
… dein Hauptinteresse auf kurzfristiger physischer Re-Use-Verfügbarkeit, materialbasierter Entwurfsinteraktion oder bauteilspezifischer Vermittlung liegt. Dort liefern materialflussnahe Akteure oft direktere Einsichten.

### Warum Madaster trotzdem so wichtig bleibt
Weil das Forschungsthema von Entwerfen mit Bestand nicht nur Verfügbarkeit, sondern auch **strukturiertes Ressourcenwissen über Zeit** betrifft. Genau hier ist Madaster außergewöhnlich nützlich.

---

## 26. Kompakte Schlussfolgerung

Madaster ist ein Schlüsselfall für die Frage, wie Gebäude und Infrastrukturen als **langfristig auswertbare Ressourcenarchive** modelliert werden können. Die Plattform verbindet IFC- und Excel-Import, Klassifikation, Datenbankanreicherung, Circularity-, Environmental- und Financial-Bewertungen sowie Materialpass- und Dossier-Exporte in einer relativ kohärenten Informationsarchitektur.

Für das Forschungsvorhaben Entwerfen mit Bestand ist Madaster deshalb besonders wichtig, weil der Fall sehr klar zeigt, wie aus Bauwerksdaten **persistente, auswertbare und berichtsfähige Materialinformationen** werden. Gerade dadurch wird aber auch sichtbar, was noch fehlt, wenn man nicht nur dokumentieren und bewerten, sondern wirklich **mit Bestand entwerfen** will: Unsicherheit, Verfügbarkeit, geometrisches Matching, Reservierungslogik und gestalterische Interaktion.

Madaster ist somit weniger die Antwort auf „Wo finde ich ein konkretes wiederverwendbares Bauteil für morgen?“ als auf die Frage: **Wie bleibt Ressourcenwissen über ein Gebäude langfristig strukturiert, anschlussfähig und auswertbar?**

---

## 27. Primärquellen / Links

### Einstieg / Plattform
- Plattform: https://madaster.com/
- How it works: https://madaster.com/how-it-works/

### Dokumentation / Setup / Dateiquellen
- Set up objects: https://docs.madaster.com/us/en/get-started/set-up-objects
- Preparing BIM IFC source files: https://docs.madaster.com/no/en/knowledge-base/preparing-bim-ifc-source-files
- Material passports: https://docs.madaster.com/us/en/knowledge-base/material-passports
- Dossier / Files: https://docs.madaster.com/us/en/platform-pages/building/files.html
- Databases: https://docs.madaster.com/no/en/knowledge-base/databases
- API: https://docs.madaster.com/lu/en/api/

### Circularity / Environmental / Financial
- Circularity: https://docs.madaster.com/us/en/platform-pages/building/circularity.html
- Circularity detail level: https://docs.madaster.com/us/en/platform-pages/building/circularity-details.html
- Environmental: https://docs.madaster.com/us/en/platform-pages/building/environmental.html
- Calculations / Financial: https://docs.madaster.com/nl/en/knowledge-base/calculations
- Circularity Indicator explained (PDF): https://docs.madaster.com/files/en/Madaster%20-%20Circularity%20Indicator%20explained.pdf

---

## 28. Noch gezielt nachzurecherchieren

1. Gibt es öffentlich zugängliche OpenAPI-Endpunkte oder Schemas, die Entitäten und Relationen genauer zeigen?
2. Gibt es konkrete Fallstudien, in denen CPset_Madaster-Felder systematisch für Re-Use gepflegt wurden?
3. Wie werden unbekannte Elemente praktisch bearbeitet, bevor Kennzahlen belastbar werden?
4. Welche Rechte- und Governance-Fragen entstehen, wenn Supplier- und Customer-Datenbanken kombiniert werden?
5. Wie lässt sich ein Materialpass in Vorentwurfswerkzeuge rückkoppeln, statt nur im Nachweis zu enden?
6. Wie könnten zeitliche Verfügbarkeit, Lagerstatus und Re-Use-Reservierungen in Madaster-artige Datenmodelle integriert werden?

### Legacy Source: werkzeug\Madaster_Plattform.md

- Map action: semantic_move
- Target role in map: primary
- Raw mapped target: software_digitaltool/Madaster_Plattform
- Original primary target: software_digitaltool/Madaster_Plattform
- Original secondary targets: 

---
type: Werkzeug
datenmodell: ["[[datenmodell/Bauteil_ID]]", "[[datenmodell/IFC]]", "[[datenmodell/Klassifikation]]", "[[datenmodell/Materialpass_Schema]]", "[[datenmodell/Taxonomie]]"]
dokument: ["[[dokument/Materialpass]]"]
methode: ["[[methode/Bauteilkatalogisierung]]"]
verwandt: ["[[werkzeug/BIM]]", "[[werkzeug/Concular_Plattform]]", "[[werkzeug/Cycle_Up]]", "[[werkzeug/DGNB_Gebaeuderessourcenpass]]", "[[werkzeug/IFC_Viewer]]", "[[werkzeug/Maconda_Materialpass]]", "[[werkzeug/Maconda_ROMULUS]]", "[[werkzeug/Material_Index]]", "[[werkzeug/Materialdatenbank]]", "[[werkzeug/One_Click_LCA_Building_Circularity]]", "[[werkzeug/Platform_CB23]]", "[[werkzeug/Qflow]]", "[[werkzeug/Upcyclea]]", "[[werkzeug/Urban_Mining_Index]]"]
---

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
