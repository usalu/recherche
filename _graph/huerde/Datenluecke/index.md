---
id: "Datenluecke"
entity: "huerde"
node_kind: "knot"
migration_status: "migrated_phase1_stable_knots"
migration_action: "move_as_knot"
title: "Datenluecke"
legacy_type: "Hürde"
legacy_paths:
  - "huerde\Datenluecke.md"
target_primary: "huerde/Datenluecke"
target_secondary: ""
risk_flags: ""
---
# Datenluecke

## Migration

- Target: huerde/Datenluecke
- Legacy source count: 1
- Legacy types: Hürde
- Migration actions: move_as_knot
- Secondary targets: 
- Risk flags: 

## Legacy Content: huerde\Datenluecke.md

---
type: Hürde
verwandt: ["[[huerde/Brandschutzkonflikt]]", "[[huerde/Fehlende_Datenstandards]]", "[[huerde/Logistikproblem]]"]
---

## Verknüpfungen

**Übergeordnete Themen**
- Hürden / Technisch und organisatorisch
- Datenmodell / Bauteilpass / Materialinventar / Rückverfolgbarkeit
- Logistik / Sondierung, Ausbau, Lagerung, Marktplatz
- Recht / Nachweise, Bauprodukte, Haftung, Schadstoffe
- Wirtschaft / Bewertung, Risiko, Restwert, Prüfkosten
- Standard / DIN SPEC 91484, FCRBE Reclamation Audit, digitale Produktpässe

**Verwandte Dateien**
- `datenmodell/Bauteilpass.md`
- `datenmodell/Materialinventar.md`
- `datenmodell/Nachweisstruktur.md`
- `datenmodell/Geometrie_Daten.md`
- `standard/DIN_SPEC_91484.md`
- `standard/Digitaler_Produktpass.md`
- `logistik/Rueckbauinventur.md`
- `logistik/Bauteiltracking.md`
- `recht/Bauprodukterecht.md`
- `recht/Schadstoffrecht.md`
- `huerde/Fehlende_Datenstandards.md`

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- Akteure: Gebäudeeigentümer:innen, Facility Management, Planende, Rückbauunternehmen, Materialauditor:innen, Prüfstellen, Bauteilhändler, Plattformbetreiber, Behörden, Versicherer.
- Fallstudien / Ansätze: Pre-Demolition-Audit nach DIN SPEC 91484; FCRBE Reclamation Audit; BAMB Materials Passports; Madaster-ähnliche Materialpässe; digitale Gebäudelogbücher; Urban-Mining-Kataster.
- Materialien: alle wiederverwendbaren Bauprodukte, besonders kritisch: tragende Bauteile, Brandschutzbauteile, Fassaden, Dämmstoffe, technische Gebäudeausrüstung, ältere Holzbauteile, schadstoffverdächtige Materialien.
- Methoden: Bauaktenrecherche, Vor-Ort-Inventur, 3D-Scan, Fotodokumentation, Bauteilkennzeichnung, zerstörungsfreie Prüfung, Probenahme, Schadstoffscreening, Zustandsklassifizierung, Datenabgleich mit Produktdatenbanken.

## Kurzdefinition

Eine Datenlücke ist das Fehlen konkreter, belastbarer Informationen über ein bestimmtes vorhandenes Bauteil, Material, Gebäude oder Rückbauprojekt. Sie betrifft den Inhalt der Information: Was ist das Bauteil? Wo befindet es sich? In welchem Zustand ist es? Welche Abmessungen, Materialqualitäten, Nachweise, Schadstoffe, Mengen, Termine, Eigentumsverhältnisse und Wiederverwendungsoptionen liegen vor?

Datenlücke ist klar von fehlenden Datenstandards zu trennen: Bei der Datenlücke fehlen Informationen oder sind unsicher. Bei fehlenden Datenstandards existieren Informationen teilweise, sind aber nicht einheitlich strukturiert, vergleichbar oder austauschbar. In der Praxis treten beide Hürden gemeinsam auf, müssen aber getrennt bearbeitet werden.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung verlangt mehr Wissen über Bestandsbauteile als konventioneller Abriss oder Recycling. Für das Recycling genügt oft die Materialfraktion: Beton, Stahl, Holz, Gips, Kunststoff. Für Wiederverwendung muss das Bauteil als Produkt erhalten bleiben. Dafür sind Identität, Geometrie, technische Leistung, Zustand, Schadstofffreiheit, Demontierbarkeit, Transportfähigkeit und neue Einsatzmöglichkeit relevant.

Datenlücken wirken an mehreren Stellen als Stopper:
- **Entwurf:** Planende können Bauteile nicht einplanen, wenn Maße, Mengen und Eigenschaften unbekannt sind.
- **Nachweis:** Tragwerk, Brandschutz, Schallschutz, Wärmeschutz und Schadstofffreiheit können ohne Daten nicht belegt werden.
- **Kosten:** Such-, Prüf-, Anpassungs- und Ausfallrisiken sind schwer kalkulierbar.
- **Vergabe:** Leistungsbeschreibungen bleiben unpräzise oder riskant.
- **Logistik:** Ausbau, Lagerung und Lieferung lassen sich ohne Mengen-, Maß- und Terminwissen nicht koordinieren.
- **Markt:** Käufer:innen vertrauen Angeboten weniger, wenn Herkunft und Qualität unklar sind.

Datenlücken führen daher häufig dazu, dass technisch wiederverwendbare Bauteile vorsorglich recycelt oder entsorgt werden. Der ökologische Wert des Bauteils geht verloren, obwohl der physische Zustand noch ausreichend wäre.

## Fachinhalt

### 1. Typen von Datenlücken

**Identitätslücke:** Hersteller, Produktname, Baujahr, Charge, Materialzusammensetzung, Typenschild, ursprüngliche Leistungserklärung oder Zulassung sind unbekannt. Diese Lücke ist besonders kritisch bei Bauprodukten mit regulierten Leistungsmerkmalen.

**Geometrielücke:** Maße, Toleranzen, Querschnitte, Öffnungsrichtungen, Anschlussdetails, Befestigungspunkte oder Stückzahlen sind nicht exakt erfasst. Für Entwurf und Einbau sind Millimeter- und Detailinformationen oft entscheidend.

**Zustandslücke:** Beschädigungen, Korrosion, Feuchte, Risse, Verformungen, Abnutzung, Reparaturen, Alterung, Funktionsfähigkeit oder frühere Überlastungen sind nicht dokumentiert. Sichtprüfung reicht häufig nur für eine erste Einschätzung.

**Leistungslücke:** Tragfähigkeit, Feuerwiderstand, Schallschutz, Wärmedurchgang, Luftdichtheit, Dauerhaftigkeit, Emissionsverhalten oder elektrische Sicherheit sind nicht belegbar. Diese Lücke entscheidet häufig über die Zulässigkeit in einem neuen Bauwerk.

**Schadstofflücke:** Asbest, PCB, PAK, Holzschutzmittel, Blei, KMF, Formaldehyd, Flammschutzmittel oder andere Schadstoffe sind unbekannt. Gerade bei Bestandsbauten ist fehlendes Schadstoffwissen ein Sicherheits- und Haftungsrisiko.

**Demontagelücke:** Es ist unklar, ob das Bauteil zerstörungsarm ausgebaut werden kann, welche Werkzeuge nötig sind, ob Verbindungen lösbar sind, wie hoch Bruch- und Verlustquoten sind und welche Reihenfolge erforderlich ist.

**Zeit- und Verfügbarkeitslücke:** Rückbaudatum, Zugriffsmöglichkeit, Reservierungsstatus, Lagerdauer und Liefertermin sind nicht gesichert. Dadurch kann ein Bauteil zwar theoretisch geeignet, aber praktisch nicht nutzbar sein.

**Eigentums- und Rechtslücke:** Unklar ist, wem das Bauteil gehört, wann Eigentum übergeht, wer über Verkauf oder Wiederverwendung entscheidet, ob Abfallrecht greift und wer für Schäden haftet.

**Markt- und Nachfrage­lücke:** Es fehlen Informationen darüber, ob ein Bauteiltyp tatsächlich nachgefragt wird, welche Preisniveaus realistisch sind und welche Anforderungen potenzielle Abnehmer haben.

### 2. Ursachen von Datenlücken

**Gebäude wurden nicht als Materialbanken dokumentiert:** Bestandsbauten enthalten viele Bauteile, deren Produktdaten bei Planung, Betrieb und Sanierung nie systematisch fortgeschrieben wurden. Bauakten sind unvollständig, veraltet oder nicht digital verfügbar.

**Informationsverlust über Lebenszyklen:** Herstellerdaten, Montageunterlagen und Wartungsprotokolle gehen über Eigentümerwechsel, Umbauten, Sanierungen und Jahrzehnte verloren. Facility-Management-Daten konzentrieren sich oft auf Betrieb, nicht auf spätere Wiederverwendung.

**Verdeckte Konstruktionen:** Viele wiederverwendungsrelevante Bauteile sind hinter Bekleidungen, Estrichen, Decken, Fassaden oder Installationen verborgen. Ohne Öffnungen oder Scans bleiben sie unsicher.

**Abrisslogik statt Re-Use-Logik:** Klassische Rückbauplanung fokussiert auf Entsorgung, Arbeitsschutz und Stoffströme. Wiederverwendung erfordert frühere und detailliertere Erfassung, bevor Bauteile beschädigt werden.

**Fehlende Ressourcen für Inventur:** Sorgfältige Bestandsaufnahme kostet Zeit, Fachwissen und Geld. Wenn diese Leistungen nicht beauftragt sind, entstehen nur grobe Listen statt belastbarer Re-Use-Daten.

**Fragmentierte Zuständigkeiten:** Eigentümer, Planer:innen, Abbruchfirmen, Schadstoffgutachter, Facility Management und Bauteilhändler erfassen jeweils andere Informationen. Ohne koordinierte Datenverantwortung bleiben Lücken bestehen.

### 3. Mindestdaten für Wiederverwendungsentscheidungen

Für eine belastbare Re-Use-Entscheidung sollten mindestens folgende Datenfelder vorhanden sein:

- Bauteilgruppe und Funktion
- Standort im Gebäude, Geschoss, Raum, Einbaulage
- Anzahl, Maße, Toleranzen, Gewicht
- Material, Aufbau, sichtbare Kennzeichnungen
- Hersteller / Produkt / Baujahr, soweit ermittelbar
- Zustand und Schäden mit Fotodokumentation
- Verbindung und Demontierbarkeit
- relevante technische Eigenschaften und Nachweise
- Schadstoffverdacht und Prüfergebnisse
- Anforderungen an Ausbau, Transport, Lagerung und Verpackung
- potenzielle Anschlussnutzungen und Einschränkungen
- zeitliche Verfügbarkeit
- Eigentum, Freigabe und Ansprechpartner
- Prüfstatus: ungeprüft, vorbewertet, geprüft, freigegeben, gesperrt

Diese Mindestdaten sind bauteilabhängig zu erweitern. Ein Natursteinbelag benötigt andere Informationen als ein Stahlträger, eine Brandschutztür oder ein Lüftungsgerät.

### 4. Methoden zum Schließen von Datenlücken

**Pre-Demolition-Audit / Reclamation Audit:** Systematische Erfassung vor Abbruch oder Sanierung. DIN SPEC 91484 legt ein Verfahren zur Erfassung von Bauprodukten als Grundlage für die Bewertung des Anschlussnutzungspotenzials fest. FCRBE stellt ergänzend praxisnahe Audit-Methoden bereit.

**Bauakten- und Dokumentenrecherche:** Alte Pläne, Leistungsverzeichnisse, Revisionsunterlagen, Wartungsprotokolle, Brandschutzkonzepte und Produktordner können entscheidende Nachweise enthalten. Sie müssen vor Rückbau gesichert werden.

**Vor-Ort-Inventur:** Sichtung, Fotodokumentation, Maßaufnahme, Typenschildsuche, Bauteilnummerierung und erste Zustandseinstufung. Wichtig ist die Kombination aus technischer und logistischer Perspektive.

**Digitale Erfassung:** 3D-Scan, BIM-Abgleich, QR-/RFID-Kennzeichnung, Datenbanken und Materialpässe können Informationen stabilisieren. Digitalisierung ersetzt jedoch nicht die technische Prüfung.

**Prüfung und Probenahme:** Bei sicherheits- oder schadstoffrelevanten Bauteilen sind Laboranalysen, Materialtests, Festigkeitsprüfungen, elektrische Prüfungen oder Funktionsprüfungen erforderlich.

**Iterative Datentiefe:** Nicht jedes Bauteil braucht sofort maximale Datentiefe. Sinnvoll ist ein Stufenmodell: Grobscreening, Priorisierung, Detailprüfung, Freigabe. So werden Ressourcen auf wertvolle oder kritische Bauteile konzentriert.

### 5. Bewertung der Datenqualität

Daten sollten nicht nur gesammelt, sondern nach Verlässlichkeit klassifiziert werden:

- **A – dokumentiert:** belastbare Hersteller-, Prüf- oder Revisionsunterlagen vorhanden.
- **B – geprüft:** Eigenschaften durch aktuelle Prüfung oder Gutachten bestätigt.
- **C – plausibel:** Eigenschaften aus Sichtung, Bauzeit, Typologie oder Vergleich ableitbar, aber nicht vollständig belegt.
- **D – unsicher:** wesentliche Informationen fehlen; nur eingeschränkte Nutzung oder weitere Prüfung möglich.
- **E – ungeeignet / gesperrt:** Schadstoff, Schaden, fehlende Demontierbarkeit oder unvertretbare Unsicherheit.

Eine solche Klassifizierung verhindert, dass unvollständige Daten als scheinbar sicher erscheinen. Unsicherheit muss im Bauteilpass sichtbar bleiben.

## Praxisbezug / Beispiele

**Fenster aus Bestandsgebäuden:** Häufig fehlen U-Wert, Glasaufbau, Beschläge, Dichtungen, Alter und Wartungszustand. Ohne diese Daten sind Einsatzbereiche begrenzt. Für unbeheizte Bereiche oder Innenverglasungen kann Wiederverwendung trotzdem möglich sein.

**Stahlträger:** Relevante Daten sind Profiltyp, Stahlgüte, Länge, Korrosion, Bohrungen, Schweißnähte, frühere Belastung und Demontageschäden. Wenn Stahlgüte nicht dokumentiert ist, können Materialproben oder konservative Annahmen erforderlich sein.

**Doppelböden:** Oft gut wiederverwendbar, wenn Raster, Plattenmaß, Tragklasse, Oberflächenzustand, Stützenhöhe und Menge bekannt sind. Datenlücken liegen häufig in Tragklasse und kompatiblen Systemteilen.

**Technische Gebäudeausrüstung:** Lüftungsgeräte, Leuchten oder Sanitärprodukte benötigen Funktions-, Hygiene-, Energie- und Sicherheitsdaten. Ohne Wartungs- und Prüfprotokolle wird Wiederverwendung schwierig.

**Schadstoffverdächtige Bauteile:** Alte Bodenbeläge, Kleber, Dämmstoffe, Brandschutzplatten oder Beschichtungen können formal wiederverwendbar erscheinen, sind aber ohne Schadstoffprüfung riskant. Schadstofffreiheit ist oft eine zentrale Datenanforderung.

## Herausforderungen / offene Fragen

- Wer finanziert die Erfassung, wenn noch unklar ist, ob Bauteile tatsächlich wiederverwendet werden?
- Welche Datentiefe ist für welche Bauteilgruppe wirtschaftlich und regulatorisch angemessen?
- Wie können Daten über Jahrzehnte erhalten bleiben, wenn Gebäude mehrfach umgebaut und verkauft werden?
- Wie wird Unsicherheit transparent dargestellt, ohne Bauteile pauschal auszuschließen?
- Wie lassen sich Prüfkosten und ökologischer Nutzen gegeneinander abwägen?
- Welche Daten müssen öffentlich zugänglich sein, welche bleiben eigentums- oder sicherheitsrelevant?
- Wie können kleine Rückbauunternehmen und Bauteilhändler Daten erfassen, ohne überfordert zu werden?
- Unsicher / regional unterschiedlich: Anforderungen an Nachweise hängen von Bauteil, Nutzung, Land, Bauaufsicht und Versicherer ab. Eine allgemeine Datenliste ersetzt keine projektspezifische Bewertung.

## Quellen

- DIN Media: *DIN SPEC 91484:2023-09 – Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen des hochwertigen Anschlussnutzungspotentials vor Abbruch- und Renovierungsarbeiten*. https://www.dinmedia.de/de/technische-regel/din-spec-91484/371235753
- FCRBE / Interreg North-West Europe: *The Reclamation Audit*, 2023. https://www.cstb.fr/getmedia/365c639a-3f3a-4e19-b2d0-e55f202414a2/Guide-reclamation-audit.pdf
- FCRBE / Interreg North-West Europe: *A guide for identifying the reuse potential of construction products*, 2020. https://vb.nweurope.eu/media/10132/en-fcrbe_wpt2_d12_a_guide_for_identifying_the_reuse_potential_of_construction_products.pdf
- Umweltbundesamt: *Instrumente zur Wiederverwendung von Bauteilen und hochwertigen Verwertung von Baustoffen*, Texte 93/2015. https://www.umweltbundesamt.de/publikationen/instrumente-zur-wiederverwendung-von-bauteilen
- BAMB / Buildings as Material Banks: *Materials Passports – Best Practice*, 2019. https://globalabc.org/sustainable-materials-hub/resources/bamb-materials-passports-best-practice
- BAMB: Übersicht Berichte und Publikationen zu Material Passports und Reversible Building Design. https://www.bamb2020.eu/library/overview-reports-and-publications/
- Europäische Union: *Regulation (EU) 2024/3110 laying down harmonised rules for the marketing of construction products*, insbesondere Digital Product Passport. https://eur-lex.europa.eu/eli/reg/2024/3110/oj/eng
- Bundesregierung / Nationale Kreislaufwirtschaftsstrategie, Handlungsfeld Bau- und Gebäudebereich. https://www.kreislaufwirtschaft-deutschland.de/kreislaufwirtschaftsstrategie/handlungsfelder/bau-und-gebaeudebereich
- Rakhshan, K. et al.: *Components reuse in the building sector – A systematic review*, Waste Management & Research / PMC, 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7472835/

