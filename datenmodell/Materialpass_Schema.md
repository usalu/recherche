---
type: Datenmodell
---

# Materialpass_Schema

## Verknüpfungen

**Übergeordnete Themen**
- Materialpass, Gebäuderessourcenpass, Digital Product Passport, Urban Mining, Kreislaufwirtschaft
- Datenmodellierung für Bauteile, Materialien, Kennwerte, Nachweise, Rückbau und Wiederverwendung
- Schnittstelle zwischen Bestandserfassung, BIM/IFC, LCA, Dokumentenmanagement, Marktplatz und Logistik

**Verwandte Dateien**
- `datenmodell/Bauteil_ID.md`
- `datenmodell/IFC.md`
- `datenmodell/Klassifikation.md`
- `datenmodell/Ontologie.md`
- `datenmodell/Taxonomie.md`
- `werkzeug/Madaster_Plattform.md`, `werkzeug/Concular_Plattform.md`, `werkzeug/Materialdatenbank.md`, `werkzeug/BIM.md`, `werkzeug/Dataview.md`, `werkzeug/Obsidian.md`
- `dokument/`: Materialpass, Gebäuderessourcenpass, Rückbauaudit, EPD, Prüfbericht, CE-/DoP-/DoPC-Unterlagen, Fotos, Wartungsdokumente
- `logistik/`: Ausbau, Verpackung, Lagerung, Transport, Verfügbarkeit, Reservierung
- `kennwert/`: Masse, Volumen, GWP, Primärenergie, Restwert, Zustand, Rückbauaufwand, Wiederverwendungspotenzial
- `meta/`: Datenqualität, Quellen, Schema-Versionierung, Pflichtfelder, Rollen und Zugriffsrechte

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- BAMB Materials Passports, DGNB Gebäuderessourcenpass, Madaster, Concular, EU-Digital-Product-Passport, Level(s)
- EN 15804, EN 15978, ISO 14040/14044, ISO 12006, ISO 23386/23387, IFC, IDS, bSDD, DIN SPEC 91484

## Kurzdefinition

Ein **Materialpass_Schema** ist die strukturierte Vorlage, nach der Materialpassdaten erfasst, gespeichert, geprüft und ausgetauscht werden. Es definiert Felder, Datentypen, Pflichtangaben, Einheiten, kontrollierte Vokabulare, Verknüpfungen, Qualitätsstufen und Versionierungsregeln.

Der Materialpass selbst ist ein konkreter Datensatz. Das Materialpass_Schema ist das Datenmodell dahinter. Im ReUse-Kontext muss es nicht nur Materialien beschreiben, sondern auch Bauteilidentität, Herkunft, Zustand, Demontierbarkeit, Prüfstatus, rechtliche Nachweise, ökologische Kennwerte und logistische Anschlussfähigkeit.

## Relevanz für Wiederverwendung im Bauwesen

Materialpässe sollen verhindern, dass Gebäude am Ende ihres ersten Nutzungszyklus wieder zu anonymen Abfallströmen werden. Für Wiederverwendung ist entscheidend, ob Informationen zu konkreten Bauteilen rechtzeitig, maschinenlesbar und belastbar verfügbar sind.

Ein gutes Schema ermöglicht:

- **Langfristige Lesbarkeit**: Daten bleiben über Projektphasen, Softwarewechsel und Eigentümerwechsel interpretierbar.
- **Bauteilorientierung**: ReUse-relevante Informationen werden nicht nur auf Gebäude- oder Materialebene aggregiert.
- **Nachweisführung**: Prüfberichte, Fotos, EPDs, technische Dokumente und Herkunftsnachweise werden verlinkt.
- **Bewertung**: CO₂-Einsparung, Masse, Restwert, Schadstoffrisiko und Wiederverwendungspotenzial können berechnet werden.
- **Interoperabilität**: Daten können mit IFC, Marktplätzen, LCA-Tools, Lagerlisten und Dokumenten verknüpft werden.
- **Datenqualität**: Unsicherheiten im Bestand werden sichtbar statt verdeckt.

## Fachinhalt

### Ebenen eines Materialpasses

Ein Schema sollte mehrere Granularitätsebenen zulassen:

1. **Gebäude / Bauwerk**: Gesamtmassen, Ressourcenzusammensetzung, Gebäudewert, Rückbaupotenzial.
2. **Bauteilgruppe / System**: Fassade, Tragwerk, Ausbau, TGA-Systeme.
3. **Einzelbauteil**: Tür, Fenster, Träger, Paneel, Leuchte, Sanitärobjekt.
4. **Produkt / Typ**: Herstellerprodukt, Typ, Leistungseigenschaften, DoP/DoPC, EPD.
5. **Material / Stoff**: Materialfraktionen, Inhaltsstoffe, Schadstoffe, Rezyklatanteile.
6. **Dokument / Nachweis**: Prüfberichte, Fotos, Datenblätter, Rückbauanleitungen.

Für direkte Wiederverwendung ist die Einzelbauteil- oder Set-Ebene entscheidend. Für Urban-Mining-Analysen reichen teilweise Gebäude- und Materialebenen.

### Pflichtbereiche eines ReUse-tauglichen Schemas

#### 1. Identität und Referenzen

```yaml
passport_id: "mp:projekt-abc:000123"
passport_schema_version: "reuse-materialpass-v1"
bauteil_id: "btl:projekt-abc:000123"
related_ifc_global_ids: []
classification: []
source_documents: []
created_by: "Organisation / Rolle"
created_at: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
```

#### 2. Objekt- und Herkunftsdaten

- Objektname und Kurzbeschreibung
- Granularität: Gebäude, System, Einzelbauteil, Set, Materialstrom
- Ursprung: Gebäude, Adresse/Projekt, Geschoss, Raum, Achse, Bauteilposition
- Eigentum, Verfügungsrechte, Ansprechpartner:innen soweit zulässig
- Erfassungsmethode: Plan, BIM, Scan, Aufmaß, Sichtprüfung, Laborprüfung
- Datenqualitätsstufe und Unsicherheiten

#### 3. Geometrie, Menge und Maße

- Stückzahl, Länge, Breite, Höhe, Dicke, Fläche, Volumen, Masse
- Toleranzen und Messmethode
- Geometriequelle: IFC, Laserscan, manuelles Aufmaß, Herstellerdaten
- Transport- und Verpackungsmaße
- Modul- oder Rasterbezug

#### 4. Material- und Produktdaten

- Hauptmaterial, Nebenmaterialien, Schichten, Verbundaufbau
- Materialanteile in Masse oder Volumen
- Oberflächen, Beschichtungen, Kleber, Dichtstoffe, Verbindungsmittel
- Hersteller, Produktname, Typ, Herstelljahr, Charge, Seriennummer soweit vorhanden
- Rezyklatanteil, biogener Anteil, kritische Rohstoffe soweit bekannt
- Schadstoffstatus: bekannt, geprüft, verdächtig, belastet, saniert, unbekannt

#### 5. Technische Leistungsdaten

- Tragfähigkeit, Brandschutz, Schallschutz, Wärmeschutz, Feuchteverhalten
- Normbezüge, Prüfdatum, Prüfstelle, Gültigkeit, Einschränkungen
- Restlebensdauer oder Bewertungszustand, sofern belastbar bestimmbar
- Kompatibilität mit Anschlussdetails oder Systemen

#### 6. Zustand und Wiederverwendung

- Zustandsklasse und Schadensbeschreibung
- Fotos mit Blickrichtung und Datum
- Reparaturbedarf, Reinigungsbedarf, Refurbishment-Empfehlung
- Demontierbarkeit, Verbindungstypen, erforderliche Werkzeuge
- Zerstörungsarme Ausbauwahrscheinlichkeit
- Anschlussnutzungsoption: Direktwiederverwendung, Reparatur, Upcycling, Ersatzteil, Recycling
- Freigabestatus: ungeprüft, in Prüfung, freigegeben, eingeschränkt, abgelehnt

#### 7. Ökologische und ökonomische Kennwerte

- Masse je Materialfraktion
- GWP nach EPD/LCA, soweit verfügbar
- eingesparte Primärmaterialmenge / vermiedene Emissionen als Szenariowert
- Restwert, Wiederbeschaffungskosten, Rückbaukosten, Lagerkosten
- Unsicherheits- und Quellenangabe zu jedem Kennwert

#### 8. Logistik und Markt

- Ausbauzeitfenster, Verfügbarkeitsdatum
- Lagerort, Packeinheit, Stapelbarkeit, Schutzanforderungen
- Transportklasse, Gewicht, Volumen, Hebepunkte
- Angebotsstatus, Reservierung, Preis, Mindestabnahmemenge
- Wiedereinbauprojekt oder Zielort, falls bekannt

### Schema-Designprinzipien

- **Bauteil_ID als Schlüssel**: Jedes konkrete Objekt oder Set braucht eine stabile Verknüpfung.
- **Schema-Versionierung**: Änderungen an Pflichtfeldern und Definitionen müssen nachvollziehbar sein.
- **Kontrollierte Werte**: Zustand, Status, Materialklassen und Anschlussnutzung nicht als beliebige Freitexte führen.
- **Einheiten verbindlich definieren**: kg, m², m³, mm, kgCO₂e usw. konsistent speichern.
- **Quellen je Feld**: Besonders im Bestand müssen Wert, Quelle, Methode, Datum und Vertrauensgrad zusammengeführt werden.
- **Dokumente referenzieren, nicht duplizieren**: Prüfberichte und EPDs als verlinkte Dokumente mit Metadaten verwalten.
- **Maschinenlesbare Formate**: JSON, CSV, YAML, RDF/JSON-LD oder Datenbanktabellen; PDF allein genügt nicht.
- **IFC-kompatibel, aber nicht IFC-abhängig**: IFC liefert Struktur und Mengen; der Pass enthält zusätzliche ReUse-Informationen.
- **Exportfähigkeit**: Marktplatz-, LCA-, Lager- und BIM-Exporte von Beginn an mitdenken.

### Beispielhafter Schemaausschnitt

```yaml
passport_id: "mp:haus-a:tuer:000314"
bauteil_id: "btl:haus-a:000314"
object_type: "Innentür"
classification:
  - system: "IFC"
    code: "IfcDoor"
  - system: "repo-taxonomie-v1"
    code: "ausbau.tuer.innentuer"
quantity:
  count: 1
  width_mm: 885
  height_mm: 2110
  mass_kg: 38
materials:
  - material: "Holzwerkstoff"
    share_mass_percent: 80
    source: "Sichtprüfung / Herstelleretikett"
condition:
  grade: "B"
  description: "gebrauchsfähig, leichte Gebrauchsspuren"
  verified_by: "Sichtprüfung"
reuse:
  status: "freigegeben mit Einschränkung"
  recommended_use: "Innenausbau, nicht brandschutzrelevant"
  dismantling_method: "Aushängen, Beschläge demontieren"
logistics:
  current_location: "Lager 2 / Regal T-04"
  packaging: "stehend geschützt"
data_quality:
  overall: "mittel"
  open_issues:
    - "kein vollständiger Herstellerdatensatz vorhanden"
```

## Praxisbezug / Beispiele

### BAMB Materials Passports

Das EU-Horizon-2020-Projekt BAMB definierte Materialpässe als digitale Datensätze, die definierte Eigenschaften von Materialien und Komponenten beschreiben, damit ihr Wert für aktuelle Nutzung, Rückgewinnung und Wiederverwendung sichtbar wird. Für das Repo ist BAMB wichtig, weil dort die Materialpass-Idee ausdrücklich auf Wiederverwendung und Rückgewinnung bezogen wird.

### DGNB Gebäuderessourcenpass

Der DGNB-Gebäuderessourcenpass arbeitet auf Gebäudeebene und macht Materialien, Bauteile, Schadstoffe, Werte und Kreislaufpotenziale systematisch dokumentierbar. Für ein ReUse-Repo ist er besonders relevant als Aggregations- und Reportingebene, während die Bauteil_ID und das Materialpass_Schema die objektgenaue Datenbasis liefern.

### EU Digital Product Passport und Bauprodukte

Die überarbeitete EU-Bauproduktenverordnung führt einen digitalen Produktpass für Bauprodukte ein. Dieser adressiert vor allem Produktinformationen, technische Leistung, Umweltinformationen und Konformitätsunterlagen. Für wiederverwendete Bauteile ist zusätzlich eine gebrauchs- und zustandsbezogene Ebene nötig: Wo war das Bauteil eingebaut, wie wurde es genutzt, wie wurde es ausgebaut, geprüft und gelagert?

### DIN SPEC 91484 / Pre-Demolition-Audit

DIN SPEC 91484 ist praxisnah, weil sie Anforderungen an die Erfassung von Bauprodukten vor Abbruch- und Renovierungsarbeiten formuliert. Das Materialpass_Schema sollte so aufgebaut sein, dass Ergebnisse aus solchen Audits ohne Informationsverlust übernommen werden können.

## Herausforderungen / offene Fragen

- **Harmonisierung**: Es gibt noch kein allgemein verpflichtendes, durchgängig genutztes Materialpass-Schema für Gebäude- und Bauteilwiederverwendung.
- **Produktpass vs. Gebäudepass**: Herstellerdaten und Bestandsdaten liegen auf unterschiedlichen Ebenen und müssen zusammengeführt werden.
- **Bestandsunsicherheit**: Alter, Materialzusammensetzung, Schadstoffe und Leistungswerte sind oft nicht vollständig bekannt.
- **Haftung**: Ein Pass dokumentiert Informationen, ersetzt aber keine rechtliche Freigabe oder technische Zulassung.
- **Datenaufwand**: Vollständige Pässe sind teuer; reduzierte Mindestpässe müssen sinnvoll definiert werden.
- **Datenalterung**: Zustand, Lagerort, Eigentum und Verfügbarkeit ändern sich laufend.
- **Geschützte Informationen**: Herstellerdaten, Preise, Eigentumsverhältnisse oder Schadstoffinformationen können zugriffsbeschränkt sein.
- **PDF-Falle**: Ein formal schöner Pass als PDF ist für ReUse nur begrenzt nützlich, wenn die Daten nicht strukturiert auslesbar sind.
- **Kennwertlogik**: CO₂-Einsparungen hängen von Annahmen zu Substitution, Transport, Aufbereitung und Lebensdauer ab; diese Annahmen müssen mitgespeichert werden.

## Quellen

- BAMB: Framework for Materials Passports, Deliverable 5. https://www.bamb2020.eu/wp-content/uploads/2018/01/Framework-for-Materials-Passports-for-the-webb.pdf
- BAMB project website. https://www.bamb2020.eu/
- DGNB: Building Resource Passport / Gebäuderessourcenpass. https://www.dgnb.de/en/sustainable-building/circular-building/building-resource-passport
- DIN Media: DIN SPEC 91484:2023-09, Pre-Demolition-Audit. https://www.dinmedia.de/de/technische-regel/din-spec-91484/371235753
- EUR-Lex: Regulation (EU) 2024/3110 on construction products. https://eur-lex.europa.eu/eli/reg/2024/3110/oj/eng
- European Commission: Level(s), European framework for sustainable buildings. https://environment.ec.europa.eu/topics/circular-economy/levels_en
- EN 15804: Sustainability of construction works — Environmental product declarations — Core rules for construction products. https://standards.iteh.ai/catalog/standards/cen/5fbe6d9e-4562-4f63-8f69-6d38f8b719ff/en-15804-2012a2-2019
- EN 15978: Sustainability of construction works — Assessment of environmental performance of buildings. https://standards.iteh.ai/catalog/standards/cen/62c22cef-5666-4719-91f9-c21cb6aa0ab2/en-15978-2011
- ISO 23386:2020, Methodology to describe, author and maintain properties in interconnected data dictionaries. https://www.iso.org/standard/75401.html
- ISO 23387:2020, Data templates for construction objects used in the life cycle of built assets. https://www.iso.org/standard/75403.html
- buildingSMART Technical: IFC. https://technical.buildingsmart.org/standards/ifc/
- buildingSMART: buildingSMART Data Dictionary (bSDD). https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/
