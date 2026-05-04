# Klassifikation

## Verknüpfungen

**Übergeordnete Themen**
- Ordnungssysteme für Bauwerksinformationen, BIM, Materialpässe, Bauteilkataloge und ReUse-Marktplätze
- Datenstrukturierung für Suche, Vergleichbarkeit, Mengenermittlung, Kostengruppen, LCA und Logistik
- Schnittstelle zwischen Taxonomie, Ontologie, IFC, bSDD und Data Templates

**Verwandte Dateien**
- `datenmodell/Taxonomie.md`
- `datenmodell/Ontologie.md`
- `datenmodell/IFC.md`
- `datenmodell/Bauteil_ID.md`
- `datenmodell/Materialpass_Schema.md`
- `werkzeug/BIM.md`, `werkzeug/IFC_Viewer.md`, `werkzeug/Materialdatenbank.md`, `werkzeug/Madaster_Plattform.md`, `werkzeug/Opalis_Plattform.md`, `werkzeug/Concular_Plattform.md`
- `dokument/`: Bauteillisten, Materialpässe, Rückbauaudit, Ausschreibung, Prüfberichte
- `logistik/`: Sortierung, Bündelung, Lagerzonen, Transportklassen, Gefahren-/Schadstofftrennung
- `kennwert/`: Mengen, Kostengruppen, GWP, Materialfraktionen, Wiederverwendungspotenzial
- `meta/`: kontrollierte Vokabulare, Mappingtabellen, Datenqualitätsregeln

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- ISO 12006-2, ISO 12006-3, ISO 23386, ISO 23387, bSDD, IFC, IDS
- DIN 276, eClass, ETIM, Uniclass, OmniClass, Uniformat, lokale ReUse-Taxonomien
- Plattformbetreiber, Bestandserfasser:innen, BIM-Koordination, LCA-Bearbeitung, Ausschreibung, Rückbau und Lagerlogistik

## Kurzdefinition

**Klassifikation** ist die Zuordnung von Objekten, Bauteilen, Materialien oder Informationen zu definierten Klassen eines Ordnungssystems. Eine Klasse besitzt in der Regel Code, Bezeichnung, Definition, Geltungsbereich und Version. Im ReUse-Kontext dient Klassifikation dazu, Bauteile und Materialien suchbar, vergleichbar, auswertbar und austauschbar zu machen.

Abgrenzung:
- **Taxonomie**: hierarchisches Begriffs- oder Kategoriengerüst, oft zur Navigation und Tag-Struktur.
- **Klassifikation**: Anwendung eines definierten Schemas auf konkrete Objekte, häufig mit Codes und Facetten.
- **Ontologie**: formales semantisches Modell mit Klassen, Eigenschaften und Beziehungen, das mehr als Hierarchie ausdrücken kann.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung braucht eine gemeinsame Sprache. Ohne Klassifikation wird ein Objekt in verschiedenen Systemen unterschiedlich benannt: „Tür“, „Innentür“, „Holztür“, „Bauelement“, „IfcDoor“, „Ausbauobjekt“, „Produktgruppe 08“ oder „Wiederverwendungsartikel“. Solche Unterschiede erschweren Suche, Bilanzierung, Datenexport, Ausschreibung und Matching zwischen Angebot und Bedarf.

Klassifikation unterstützt:

- **Inventarisierung**: Bauteile werden konsistent erfasst und gruppiert.
- **Marktplatzsuche**: Suchfilter wie Bauteiltyp, Material, Dimension, Zustand oder Verfügbarkeit funktionieren nur mit kontrollierten Kategorien.
- **Mengen- und Kennwertbildung**: GWP, Masse, Kosten, Restwert oder Wiederverwendungspotenzial lassen sich nach Klassen aggregieren.
- **Interoperabilität**: IFC-Klassen, nationale Systeme, Plattformkategorien und Materialpässe können gemappt werden.
- **Ausschreibung und Planung**: ReUse-Bauteile können als definierte Bauteilgruppen in Leistungsverzeichnisse und Entwürfe eingehen.
- **Logistik**: Klassen helfen bei Ausbauprioritäten, Verpackung, Lagerung und Transport.

## Fachinhalt

### Bausteine einer Klassifikation

Ein ReUse-tauglicher Klassifikationsdatensatz sollte mindestens enthalten:

```yaml
classification_system: "Uniclass 2015 | OmniClass | eClass | DIN 276 | IFC | lokale ReUse-Klassifikation"
classification_version: "YYYY-MM / Versionsnummer"
class_code: "z. B. EF_25_30 oder IfcDoor"
class_label: "Innentür / Door / ..."
class_definition: "kurze Definition oder Link auf Definition"
classification_facet: "Element | Produkt | Material | Funktion | Kosten | Logistik | Zustand"
assigned_by: "Person / Tool / Regel"
assignment_method: "manuell | halbautomatisch | automatisiert | importiert"
confidence: "hoch | mittel | niedrig"
source: "IFC-Modell | Aufmaß | Foto | Prüfbericht | Plattform"
```

### Facetten statt Ein-System-Denken

Ein einzelnes Klassifikationssystem reicht für ReUse selten aus. Ein Bauteil hat mehrere relevante Perspektiven:

| Facette | Beispiel | ReUse-Nutzen |
|---|---|---|
| IFC-Objektklasse | `IfcDoor`, `IfcWindow`, `IfcBeam` | BIM-Interoperabilität und Modellprüfung. |
| Bauteil-/Elementklasse | Tür, Fenster, Träger, Fassadenpaneel | Inventar, Suche, Ausschreibung. |
| Materialklasse | Holz, Stahl, Aluminium, Glas, Beton | LCA, Schadstoffprüfung, Sortierung, Recycling/Wiederverwendung. |
| Funktion | tragend, nichttragend, abschließend, haustechnisch | Planung und technische Eignung. |
| Kosten-/Leistungsstruktur | DIN 276, Leistungsverzeichnis-Kategorien | Wirtschaftlichkeit und Vergabe. |
| Zustand | neuwertig, gebraucht, beschädigt, prüfpflichtig | Angebot, Preis, Freigabe. |
| Logistikklasse | sperrig, zerbrechlich, gefährlich, palettierbar | Ausbau, Lager und Transport. |
| Anschlussnutzung | Direktwiederverwendung, Reparatur, Upcycling, Recycling | Strategie und Kennwerte. |

### Verhältnis zu IFC

IFC-Entitäten sind keine vollständige Klassifikation für Wiederverwendung. Sie definieren Modellobjekte, aber nicht zwingend Markt-, Material-, Zustands- oder Logistikkategorien. Ein `IfcWall` kann Mauerwerk, Trockenbau, Betonfertigteil oder historische Trennwand sein; ein `IfcDoor` kann Brandschutztür, Wohnungseingangstür, Innentür oder historisches Bauteil sein.

Empfehlung:
- IFC-Klasse als technische Modellklasse speichern.
- Zusätzlich mindestens eine Bauteil-/Produktklassifikation führen.
- Material- und Zustandsklassifikation separat führen.
- Klassifikationen mit Version und Quelle dokumentieren.
- Bei Unsicherheit `confidence` statt falscher Präzision nutzen.

### Verhältnis zu Taxonomie und Ontologie

- Eine **Taxonomie** kann im Repo als Navigationsstruktur dienen: `Ausbau > Türen > Innentüren`.
- Eine **Klassifikation** weist einem konkreten Objekt einen Code aus einem System zu: `class_code = IfcDoor` oder `Uniclass ...`.
- Eine **Ontologie** beschreibt zusätzlich Beziehungen: `Türblatt ist Teil von Türelement`, `Türelement befindet sich in Raum`, `Türelement besitzt Brandschutznachweis`, `Türelement hat Material Holz`.

Klassifikation ist damit die pragmatische Ebene für Listen, Filter, Auswertung und Austausch; Ontologie ist die semantische Integrationsschicht; Taxonomie ist die navigierbare Begriffshierarchie.

### Klassifikationssysteme und ihre Rollen

| System / Ansatz | Rolle | Eignung für ReUse |
|---|---|---|
| ISO 12006-2 | Internationaler Rahmen für Klassifikationssysteme der gebauten Umwelt | Wichtig als Meta-Rahmen; kein fertiges operatives ReUse-System. |
| ISO 12006-3 | Objektorientierter Informationsrahmen, Grundlage für semantische Wörterbücher | Relevant für bSDD, Data Dictionaries und Ontologien. |
| IFC | Modellobjekt- und Austauschstruktur | Sehr wichtig für BIM, aber nicht ausreichend als ReUse-Klassifikation. |
| bSDD | Service für Definitionen von Klassen und Eigenschaften | Nützlich zur semantischen Harmonisierung. |
| DIN 276 | Kostenstruktur im Hochbau | Nützlich für Kostenbezug, aber nur begrenzt für Bauteilzustand und ReUse-Fähigkeit. |
| eClass / ETIM | Produkt- und technische Merkmalsklassifikation | Stark für Produktdaten; ReUse-Zustand und Herkunft müssen ergänzt werden. |
| Uniclass / OmniClass | Facettierte Bauklassifikationen | Nützlich für internationale Projekte; Mappingaufwand beachten. |
| Lokale ReUse-Taxonomie | Projekt- oder Plattformkategorien | Praktisch, aber nur interoperabel, wenn gemappt und dokumentiert. |

### ReUse-spezifische Pflichtdimensionen

Für Wiederverwendung sollte Klassifikation nicht bei Bauteiltyp enden. Sinnvolle zusätzliche Klassifikationsachsen sind:

- **Wiederverwendungsstatus**: potenziell, geprüft, freigegeben, reserviert, verkauft, wiedereingebaut, ausgeschieden.
- **Qualitätsstatus**: ungeprüft, visuell geprüft, technisch geprüft, mit Nachweis, nur dekorativ nutzbar.
- **Zustand**: A/B/C/D oder definierte Zustandsklassen.
- **Demontierbarkeit**: zerstörungsfrei, teilweise zerstörend, zerstörend, unbekannt.
- **Schadstoffstatus**: unkritisch, prüfpflichtig, belastet, saniert, unbekannt.
- **Anschlussnutzung**: direkte Wiederverwendung, Reparatur, Refurbishment, Upcycling, Ersatzteil, Recycling.
- **Datenqualität**: Modellwert, Schätzwert, gemessen, geprüft, dokumentiert.

## Praxisbezug / Beispiele

### Beispiel 1: Klassifikation einer Innentür

```yaml
bauteil_id: "btl:haus-a:000314"
ifc_class: "IfcDoor"
local_taxonomy: "ausbau.tuer.innentuer"
material_class: "holzwerkstoff"
reuse_status: "geprüft"
condition_class: "B - gebrauchsfähig mit leichten Gebrauchsspuren"
dismantling_class: "zerstörungsarm demontierbar"
data_quality: "gemessen und fotografisch belegt"
```

Diese Kombination ist für ReUse aussagekräftiger als allein `IfcDoor`.

### Beispiel 2: Fassadenpaneele

Fassadenpaneele können als Element, Produkt, Materialverbund, Brandschutzbauteil und logistisches Packstück klassifiziert werden. Für ReUse ist relevant, ob sie typengleich, sortenrein, beschädigungsfrei, geometrisch wiederholbar und mit Befestigungssystem dokumentiert sind. Eine reine Kostengruppe reicht nicht.

### Beispiel 3: Marktplatz-Mapping

Eine lokale Kategorie `fassade.metallpaneel` muss für einen externen Marktplatz auf dessen Kategorien gemappt werden. Das Mapping sollte als eigene Tabelle geführt werden:

```yaml
source_system: "repo-taxonomie-v1"
source_code: "fassade.metallpaneel"
target_system: "plattform-x"
target_code: "cladding_metal_panel"
mapping_type: "exact | broad | narrow | related"
confidence: "mittel"
notes: "Zustand und Befestigung separat übertragen"
```

## Herausforderungen / offene Fragen

- **Mehrdeutigkeit**: Ein Bauteil kann je nach Blickwinkel Element, Produkt, Materialverbund oder Ausstattung sein.
- **Regionale Unterschiede**: DIN-, britische, US-amerikanische, europäische und plattformspezifische Systeme passen nicht 1:1 zusammen.
- **Versionswechsel**: Klassifikationscodes ändern sich; Altbestände müssen nachvollziehbar bleiben.
- **Scheingenauigkeit**: Automatische Klassifizierung aus BIM oder Fotos kann plausibel wirken, aber falsch sein.
- **Gemischte Bauteile**: Verbundmaterialien, historische Bauteile und Sonderanfertigungen sprengen einfache Klassen.
- **ReUse-Zustand**: Klassifikationen aus Neubau- und Produktdaten enthalten oft keine ausreichenden Zustands- und Demontageinformationen.
- **Mappingaufwand**: Interoperabilität entsteht nicht durch viele Codes, sondern durch gepflegte Mappingregeln und Definitionen.
- **Governance**: Wer darf Klassen hinzufügen, umbenennen, mappen oder stilllegen?

## Quellen

- ISO 12006-2:2015, Building construction — Organization of information about construction works — Part 2: Framework for classification. https://www.iso.org/standard/61753.html
- ISO 12006-3:2022, Building construction — Organization of information about construction works — Part 3: Framework for object-oriented information. https://www.iso.org/standard/74932.html
- ISO 23386:2020, Methodology to describe, author and maintain properties in interconnected data dictionaries. https://www.iso.org/standard/75401.html
- ISO 23387:2020, Data templates for construction objects used in the life cycle of built assets. https://www.iso.org/standard/75403.html
- buildingSMART: buildingSMART Data Dictionary (bSDD). https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/
- buildingSMART Technical: IFC. https://technical.buildingsmart.org/standards/ifc/
- buildingSMART: Information Delivery Specification (IDS). https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/
- DIN 276: Kosten im Bauwesen, Normenreihe. https://www.dinmedia.de/
- NBS: Uniclass. https://www.thenbs.com/our-tools/uniclass
- Construction Specifications Institute: OmniClass. https://www.csiresources.org/standards/omniclass
- eClass Standard. https://eclass.eu/
- ETIM International. https://www.etim-international.com/
