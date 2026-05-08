---
id: "Statische_Nachweisfuehrung"
entity: "pruefung_nachweis"
node_kind: "knot"
migration_status: "migrated_phase1_stable_knots"
migration_action: "move_as_knot"
title: "Statische Nachweisfuehrung"
legacy_type: "PrÃ¼fung"
legacy_paths:
  - "pruefung\Statische_Nachweisfuehrung.md"
target_primary: "pruefung_nachweis/Statische_Nachweisfuehrung"
target_secondary: ""
risk_flags: ""
---
# Statische Nachweisfuehrung

## Migration

- Target: pruefung_nachweis/Statische_Nachweisfuehrung
- Legacy source count: 1
- Legacy types: PrÃ¼fung
- Migration actions: move_as_knot
- Secondary targets: 
- Risk flags: 

## Legacy Content: pruefung\Statische_Nachweisfuehrung.md

---
type: Prüfung
leistungsanforderung: ["[[leistungsanforderung/Dauerhaftigkeit]]", "[[leistungsanforderung/Tragfaehigkeit]]", "[[leistungsanforderung/index]]"]
material: ["[[material/Holz]]", "[[material/Sekundaerstahl]]"]
norm: ["[[norm/index]]"]
tragwerkssystem: ["[[tragwerkssystem/Holztragwerk]]"]
verbindung: ["[[verbindung/Klemmverbindung]]"]
verwandt: ["[[pruefung/Abbrandbemessung]]", "[[pruefung/Brandnachweis]]", "[[pruefung/Eignungspruefung_Baulehm]]", "[[pruefung/Schweissbarkeitspruefung]]", "[[pruefung/Zugversuch]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** Prüfung; Tragwerksplanung; Bestandserhalt; Bauteilwiederverwendung; Sicherheit; Gebrauchstauglichkeit; Dauerhaftigkeit; Dokumentation.
- **Verwandte Dateien:** `pruefung/Zugversuch.md`; `pruefung/Schweissbarkeitspruefung.md`; `pruefung/Abbrandbemessung.md`; `pruefung/Brandnachweis.md`; `pruefung/Eignungspruefung_Baulehm.md`; `material/Sekundaerstahl.md`; `material/Holz.md`; `material/Betonfertigteil.md`; `material/Baulehm.md`; `material/Mauerwerk.md`; `verbindung/Bolzenverbindung.md`; `verbindung/Schraubenverbindung.md`; `verbindung/Schweissverbindung.md`; `verbindung/Klemmverbindung.md`; `tragwerkssystem/Stahltragwerk.md`; `tragwerkssystem/Holztragwerk.md`; `tragwerkssystem/Massivbau.md`; `tragwerkssystem/Hybridtragwerk.md`; `leistungsanforderung/Tragfaehigkeit.md`; `leistungsanforderung/Gebrauchstauglichkeit.md`; `leistungsanforderung/Robustheit.md`; `leistungsanforderung/Dauerhaftigkeit.md`; `leistungsanforderung/Demontierbarkeit.md`; `standard/Eurocode_0.md`; `standard/Eurocode_1.md`; `standard/Eurocode_2.md`; `standard/Eurocode_3.md`; `standard/Eurocode_5.md`; `standard/Eurocode_6.md`; `standard/ISO_13822.md`; `standard/MVV_TB.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Tragwerksplaner:innen; Prüfingenieur:innen; Sachverständige; Materialprüfanstalten; Rückbauunternehmen; Bauherrschaft; Bauaufsicht; Stahlbau- und Holzbauunternehmen; Betonfertigteilwerke; Materialbörsen; Bestandstragwerke; DIN EN 1990 bis 1999 mit Nationalen Anhängen; DIN EN 1991 für Einwirkungen; ISO 13822 für Bestandsbewertung; MVV TB; CEN/TS 1090-201; SCI Steel Reuse Protocol; FCRBE; BAMB; Bauteilpass; zerstörende und zerstörungsarme Prüfung; visuelle Sortierung; Probebelastung; Sicherheits- und Teilsicherheitskonzept; statistische Auswertung; Rückbau- und Einbaukontrolle.

## Kurzdefinition

Statische Nachweisführung ist die rechnerische, prüftechnische und dokumentarische Begründung, dass ein Tragwerk oder Bauteil unter den maßgebenden Einwirkungen ausreichend sicher, gebrauchstauglich, robust und dauerhaft ist. Bei wiederverwendeten Bauteilen umfasst sie zusätzlich die Bewertung des vorhandenen Zustands, der Materialherkunft, der Rückbau- und Transportgeschichte, der Restlebensdauer und der Eignung für den neuen statischen Kontext.

Im Neubau stützt sich die Nachweisführung oft auf normgerechte Bauprodukte mit bekannten Kennwerten. Bei Wiederverwendung müssen diese Kennwerte häufig rekonstruiert, geprüft oder konservativ angesetzt werden. Der Nachweis ist damit nicht nur eine Berechnung, sondern eine Beweiskette aus Identifikation, Prüfung, Klassifizierung, Bemessung, Ausführung und Qualitätssicherung.

## Relevanz für Wiederverwendung im Bauwesen

Die statische Nachweisführung ist der zentrale Gatekeeper für tragende Wiederverwendung. Viele Bauteile besitzen physisch ausreichende Tragfähigkeit, können aber ohne nachvollziehbaren Nachweis nicht in neuen Gebäuden eingesetzt werden. Besonders relevant ist dies für:

- Sekundärstahlprofile aus Hallen, Brücken, Industrie- oder Bürogebäuden;
- alte Vollholz- und Brettschichtholzträger;
- Betonfertigteile, Spannbetonplatten, Fassadenplatten und Treppen;
- Mauerwerks- und Lehmbauteile;
- historische Bauteile mit unbekannter Normbasis;
- Verbindungsmittel und Knoten, die im neuen Tragwerk maßgebend werden.

Die Nachweisführung entscheidet, ob Wiederverwendung hochwertig im Primärtragwerk, eingeschränkt in Nebentragwerken oder nur nichttragend möglich ist. Sie beeinflusst auch Entwurf, Logistik und Beschaffung: Bauteile müssen früh inventarisiert werden, damit das neue Tragwerk auf vorhandene Längen, Querschnitte und Qualitäten abgestimmt werden kann.

## Fachinhalt

### Nachweisebenen

Für wiederverwendete tragende Bauteile sind drei Ebenen zu unterscheiden:

1. **Bauteilnachweis:** Tragfähigkeit und Gebrauchstauglichkeit des einzelnen Bauteils, z. B. Stahlträger, Holzstütze, Betonplatte.
2. **Systemnachweis:** Verhalten im neuen Tragwerk, einschließlich Lagerung, Aussteifung, Lastumlagerung, Stabilität, Brandsituation, Bauzustände und Robustheit.
3. **Prozessnachweis:** Sicherstellung, dass das geprüfte Bauteil tatsächlich identisch, unbeschädigt und korrekt eingebaut wird. Dazu gehören Bauteil-ID, Rückbauprotokoll, Transport, Lagerung, Bearbeitung und Einbaukontrolle.

Ein Bauteil kann auf Ebene 1 geeignet sein, auf Ebene 2 aber scheitern, wenn es nicht in die Aussteifung, Brandschutzanforderung oder Anschlussgeometrie passt. Ebenso kann ein rechnerisch geeigneter Träger unzulässig werden, wenn seine Identität nach Lagerung nicht mehr nachvollziehbar ist.

### Grundnormen und Bewertungsrahmen

In Deutschland und Europa beruht die Tragwerksbemessung im Regelfall auf den Eurocodes mit Nationalen Anhängen. DIN EN 1990 regelt Grundlagen, Grenzzustände, Teilsicherheitskonzept, Zuverlässigkeit und Kombinationen; DIN EN 1991 die Einwirkungen; die Material-Eurocodes regeln Beton, Stahl, Verbund, Holz, Mauerwerk, Aluminium und Geotechnik. Für bestehende Strukturen ist ISO 13822 eine wichtige internationale Grundlage zur Bewertung vorhandener Tragwerke auf Basis von Zuverlässigkeit, Konsequenzklassen, Inspektion und aktualisierten Informationen.

Bei Wiederverwendung ist die normative Einordnung projektspezifisch:

- Wird ein gebrauchtes Bauteil als Bauprodukt erneut bereitgestellt?
- Wird ein vorhandenes Bauteil innerhalb desselben Gebäudes umgenutzt?
- Entsteht durch Bearbeitung ein neues Bauteil?
- Liegt eine geregelte Bauart vor oder ist eine vorhabenbezogene Genehmigung nötig?
- Gelten zusätzliche Anforderungen aus MVV TB, Sonderbauvorschriften, Denkmalpflege, Versicherung oder Bauherrschaft?

Unsicherheiten sind offen zu markieren und mit Prüfplan, konservativen Annahmen oder bauaufsichtlicher Abstimmung zu behandeln.

### Beweiskette für Wiederverwendung

Eine belastbare statische Nachweisführung folgt einer nachvollziehbaren Beweiskette:

1. **Anforderungsdefinition:** neue Nutzung, Gebäudeklasse, Nutzlasten, Brandschutz, Exposition, Dauerhaftigkeit, Demontierbarkeit, Entwurfslastfälle.
2. **Inventarisierung:** Bauteiltyp, Abmessungen, Stückzahl, Fotos, Markierungen, Lage im Herkunftsgebäude, Bestandspläne, Alter, ursprüngliche Bemessungsnorm.
3. **Zustandsbewertung:** Schäden, Korrosion, Risse, Verformung, Abplatzungen, Feuchte, biologische Schädigung, Ermüdung, Brand- oder Anprallschäden.
4. **Materialidentifikation:** Festigkeitsklasse, chemische Zusammensetzung, Holzsortierung, Betonfestigkeit, Bewehrung, Lehm- oder Mauerwerksfestigkeit.
5. **Prüfplan:** Auswahl zerstörungsarmer und zerstörender Prüfungen; Stichprobenumfang; Chargenbildung; Akzeptanzkriterien.
6. **Kennwertableitung:** charakteristische Werte, Teilsicherheitsbeiwerte, Abminderungen für Schäden, Streuung und Restlebensdauer.
7. **Rechnerischer Nachweis:** Grenzzustände der Tragfähigkeit und Gebrauchstauglichkeit, Stabilität, Ermüdung, Brand, Robustheit, Bauzustände.
8. **Verbindungsnachweis:** neue und alte Anschlüsse, Lochleibung, Schweißbarkeit, Schrauben, Bolzen, Klemmung, Auflagerpressung.
9. **Ausführungsplanung:** Bearbeitungsgrenzen, Bohr- und Schnittverbote, Oberflächenbehandlung, Korrosions-/Holzschutz, Brandschutz.
10. **Qualitätssicherung:** Kennzeichnung, Lagerung, Transport, Montagekontrolle, Prüfprotokolle, Abnahme.
11. **Dokumentation:** Bauteilpass, Materialpass, Prüfberichte, Nachweise, Einbauort, Wartungs- und Rückbauhinweise.

### Materialbezogene Besonderheiten

#### Sekundärstahl

Für Stahl sind Querschnitt, Stahlgüte, Streckgrenze, Zugfestigkeit, Duktilität, Kerbschlagzähigkeit, Korrosion und Schweißbarkeit maßgebend. Häufig sind Zugversuch, chemische Analyse, Härteprüfung und zerstörungsfreie Prüfungen erforderlich. Alte Bohrungen oder Schnitte können die Querschnittsklasse, Ermüdungsfestigkeit und Anschlussnachweise beeinflussen. Bei dynamischer Beanspruchung, Kranbahnen, Brücken oder stark wechselnden Lasten ist Ermüdung besonders kritisch.

CEN/TS 1090-201 und Steel-Reuse-Protokolle liefern strukturierte Vorgehensweisen zur Klassifizierung, Prüfung und Dokumentation wiederverwendeter Stahlprodukte. Sie ersetzen nicht den projektbezogenen statischen Nachweis, erleichtern aber die Beweiskette.

#### Holz

Für Holz sind Holzart, Sortierklasse, Feuchte, Risse, Astigkeit, Faserverlauf, Insekten- und Pilzbefall, frühere Ausklinkungen, Brandschutz und Anschlüsse maßgebend. Wiederverwendete Hölzer benötigen visuelle Sortierung und gegebenenfalls ergänzende Prüfungen. Die Abbrandbemessung ist bei Feuerwiderstandsanforderungen ein Teil der statischen Nachweisführung im Brandfall. Historische Zimmermannsverbindungen dürfen nicht ohne Prüfung als heutige Tragverbindungen angesetzt werden.

#### Betonfertigteile

Bei Betonfertigteilen sind Betonfestigkeit, Bewehrungslage, Betondeckung, Karbonatisierung, Chloride, Risse, Vorspannung, Auflagerdetails und Transportzustände relevant. Der Rückbau kann neue Risse oder Abplatzungen verursachen. Bei Spannbeton sind Informationen zu Vorspannsystem, Spannkraft, Schnittstellen und Korrosion zwingend. Ohne ausreichende Daten kann nur eingeschränkte oder nichttragende Wiederverwendung möglich sein.

#### Mauerwerk und Baulehm

Mauerwerk und Lehmbauteile sind stark systemabhängig: Stein, Mörtel, Verband, Feuchte, Auflast und Ausführung bestimmen Tragfähigkeit. Wiederverwendete Lehmsteine oder Ziegel benötigen Prüfungen von Festigkeit, Maßhaltigkeit, Wasserempfindlichkeit und Mörtelverträglichkeit. Tragendes Lehmsteinmauerwerk ist an DIN 18940 und die dortigen Einsatzgrenzen gebunden.

#### Verbindungsmittel

Verbindungsmittel sind oft der begrenzende Faktor. Wiederverwendete Schrauben, Bolzen oder Niete dürfen nicht automatisch erneut tragend angesetzt werden. Alte Verbindungslöcher können Querschnittsschwächungen darstellen. Neue Anschlüsse sollten möglichst demontierbar, prüfbar und brandschutztechnisch beherrschbar sein.

### Umgang mit Unsicherheit

Bei wiederverwendeten Bauteilen sind Unsicherheiten höher als bei Neuprodukten. Möglichkeiten der Behandlung:

- konservative Festigkeitsannahmen;
- größere Stichproben und Chargenbildung;
- Reduktion der zulässigen Ausnutzung;
- Einsatz in weniger kritischen Bauteilen;
- redundante Tragwerkskonzepte;
- Monitoring oder Inspektionsplan;
- Probebelastung bei geeigneten Bauteilen;
- bauaufsichtliche Abstimmung vor Genehmigungsplanung;
- Ausschlusskriterien für beschädigte oder nicht identifizierbare Bauteile.

Die Sicherheitsphilosophie sollte transparent sein: Es ist nicht fachgerecht, fehlende Informationen durch optimistische Annahmen zu ersetzen. Umgekehrt kann ein gut dokumentiertes, geprüftes Reuse-Bauteil sicherer bewertet werden als ein schlecht dokumentierter Bestand.

### Dokumentation und Bauteilpass

Der Bauteilpass ist kein Ersatz für den statischen Nachweis, aber die Grundlage für Nachvollziehbarkeit. Er sollte enthalten:

- eindeutige Bauteil-ID;
- Herkunft, Ausbauort, Fotos, Baujahr;
- Abmessungen, Masse, Geometrie, Besonderheiten;
- Materialkennwerte und Prüfberichte;
- Schäden und Reparaturen;
- zulässige Bearbeitung und Schnittstellen;
- Nachweise, Bemessungswerte, Einsatzgrenzen;
- Einbauort im neuen Projekt;
- Brandschutz-, Korrosions-, Feuchte- und Wartungshinweise;
- Rückbau- und Wiederverwendungshinweise für den nächsten Lebenszyklus.

## Praxisbezug / Beispiele

### Sekundärstahlhalle

Eine bestehende Stahlhalle wird demontiert und die Profile sollen in einem Neubau eingesetzt werden. Die statische Nachweisführung beginnt mit Profilinventar, Bestandsstatik, Schadenskartierung und Stahlgütenprüfung. Anschließend wird das neue Tragwerk so entworfen, dass vorhandene Längen und Querschnitte möglichst ohne Schweißen nutzbar bleiben. Kritisch sind neue Anschlüsse, Aussteifung, Brandschutzanforderung und Korrosion. Ein Bauteilpass pro Träger verhindert Verwechslungen.

### Wiederverwendete Holzbalken in einer Geschossdecke

Alte Holzbalken werden visuell sortiert, auf Holzfeuchte und Schäden geprüft und in Festigkeitsgruppen eingeteilt. Die neue Decke wird mit begrenzten Spannweiten entworfen. Nachgewiesen werden Biegung, Schub, Durchbiegung, Schwingung, Auflager und Brandfall. Balken mit Zapfenlöchern im hochbeanspruchten Bereich werden ausgeschlossen oder nur gekürzt eingesetzt.

### Betonfertigteilplatten aus Rückbau

Betonplatten können nur wiederverwendet werden, wenn Bewehrung, Betondeckung, Plattengeometrie, Auflagerung und Transportzustand geklärt sind. Bei unbekannter Vorspannung ist besondere Vorsicht erforderlich. Eine neue Nutzung mit höheren Lasten oder geänderten Auflagern kann die Wiederverwendung ausschließen. Häufig sind zerstörungsarme Bewehrungsortung, Kernbohrungen, Karbonatisierungs- und Chloridprüfung notwendig.

### Lehmsteinmauerwerk

Wiederverwendete Lehmsteine können in nichttragenden Innenwänden relativ einfach eingesetzt werden, wenn Feuchte und Hygiene stimmen. Für tragende Wände müssen die Steine und der Mörtel den Anforderungen entsprechen, und die Bemessung muss nach DIN 18940 bzw. projektspezifisch erfolgen. Die statische Nachweisführung ist eng mit Feuchteschutz verbunden.

### Hybridtragwerk

Ein hybrides Tragwerk aus Sekundärstahl, neuen Holzdecken und Lehmbauteilen erfordert systemische Nachweise: unterschiedliche Verformungen, Feuchte, Brandschutz, Anschlüsse und Demontierbarkeit müssen zusammen betrachtet werden. Der Nachweis einzelner Materialien reicht nicht aus.

## Herausforderungen / offene Fragen

- **Fehlende Produktdaten:** Ohne Werkszeugnisse oder Herstellernachweise müssen Kennwerte über Prüfungen abgeleitet werden.
- **Stichprobenumfang:** Zu wenige Proben unterschätzen Streuung; zu viele Proben beschädigen Bauteile und erhöhen Kosten.
- **Normative Schnittstellen:** Eurocodes sind primär für neue Konstruktionen geschrieben; Bestandsbewertung und Bauteilwiederverwendung erfordern ergänzende Interpretation.
- **Bauaufsichtliche Akzeptanz:** Prüfingenieur:innen und Behörden verlangen nachvollziehbare, projektspezifische Begründungen. Frühzeitige Abstimmung ist entscheidend.
- **Rückbau als Tragwerksphase:** Bauteile können beim Ausbau höhere oder andere Beanspruchungen erfahren als im späteren Neubau.
- **Transport und Lagerung:** Verformungen, Korrosion, Feuchteaufnahme oder mechanische Schäden nach Prüfung können die Nachweise ungültig machen.
- **Versicherung und Haftung:** Verantwortlichkeiten zwischen Rückbau, Materialhandel, Planung, Ausführung und Bauherrschaft sind oft ungeklärt.
- **Brandschutz und Dauerhaftigkeit:** Ein im Kaltzustand geeigneter Träger kann wegen Feuerwiderstand, Korrosion oder Feuchte ungeeignet sein.
- **Entwurf mit begrenztem Inventar:** Reuse-Bauteile sind nicht frei bestellbar; Tragwerksentwurf muss mit vorhandenen Querschnitten, Längen und Qualitäten arbeiten.
- **Nächster Lebenszyklus:** Schweißen, Verguss, Verklebung oder irreversible Beschichtungen können die spätere Wiederverwendung verschlechtern.

## Quellen

- DIN EN 1990: Eurocode – Grundlagen der Tragwerksplanung, einschließlich Nationalem Anhang.
- DIN EN 1991-Reihe: Eurocode 1 – Einwirkungen auf Tragwerke, einschließlich Nationaler Anhänge.
- DIN EN 1992 bis DIN EN 1999: Material-Eurocodes für Beton, Stahl, Verbund, Holz, Mauerwerk, Aluminium und Geotechnik, jeweils mit Nationalen Anhängen.
- ISO 13822:2010: Bases for design of structures – Assessment of existing structures; 2021 bestätigt. Online: https://www.iso.org/standard/46556.html
- Deutsches Institut für Bautechnik (DIBt): Muster-Verwaltungsvorschrift Technische Baubestimmungen, aktuelle Ausgabe 2025/1 und landesspezifische Umsetzung. Online: https://www.dibt.de/de/wir-bieten/technische-baubestimmungen
- CEN/TS 1090-201: Execution of steel structures and aluminium structures – Reuse of structural steel products.
- The Steel Construction Institute (SCI): Structural Steel Reuse Protocol / SCI P427.
- PROGRESS: European Recommendations for Reuse of Steel Products in Single-Storey Buildings.
- FCRBE – Facilitating the Circulation of Reclaimed Building Elements: Leitfäden zu Prüfung, Dokumentation und Wiederverwendung von Bauteilen. Online: https://www.nweurope.eu/projects/project-search/fcrbe-facilitating-the-circulation-of-reclaimed-building-elements/
- BAMB – Buildings as Material Banks: Materialpässe und reversible Konstruktion. Online: https://www.bamb2020.eu/
- Verordnung (EU) 2024/3110 über harmonisierte Vorschriften für die Vermarktung von Bauprodukten. Online: https://eur-lex.europa.eu/eli/reg/2024/3110/oj
- DIN 18940:2023-06: Tragendes Lehmsteinmauerwerk – Konstruktion, Bemessung und Ausführung.
- DIN EN ISO 6892-1: Metallische Werkstoffe – Zugversuch – Teil 1: Prüfverfahren bei Raumtemperatur.

