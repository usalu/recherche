---
id: "REI90"
entity: "leistungsanforderung"
node_kind: "knot"
migration_status: "migrated_phase2_semantic_corrections"
migration_action: "semantic_move"
title: "REI90"
legacy_type: "Norm"
legacy_paths:
  - "norm\REI90.md"
target_primary: "leistungsanforderung/REI90"
target_roles: "phase2_primary"
risk_flags: "requirement_misfiled_as_norm"
---
# REI90

## Migration

- Target: leistungsanforderung/REI90
- Legacy source count: 1
- Legacy types: Norm
- Migration actions: semantic_move
- Target roles: phase2_primary
- Risk flags: requirement_misfiled_as_norm

## Legacy Content: norm\REI90.md

---
type: Norm
huerde: ["[[huerde/Brandschutzkonflikt]]"]
leistungsanforderung: ["[[leistungsanforderung/Brandschutz]]"]
pruefung: ["[[pruefung/Brandnachweis]]"]
recht: ["[[recht/Bauordnungsrecht]]"]
verwandt: ["[[norm/Brandschutzanforderung]]", "[[norm/F90]]", "[[norm/Feuerwiderstand]]", "[[norm/R90]]"]
---

# REI90

## Verknüpfungen

**Übergeordnete Themen**
- Europäische Feuerwiderstandsklassifikation
- Tragende und raumabschließende Bauteile
- Brandschutzanforderungen an Wände und Decken
- ReUse von tragenden Trennbauteilen

**Verwandte Dateien**
- `standard/Brandschutzanforderung.md`
- `standard/Feuerwiderstand.md`
- `standard/F90.md`
- `standard/R90.md`
- `pruefung/Brandnachweis.md`
- `huerde/Brandschutzkonflikt.md`
- `leistungsanforderung/Brandschutz.md`
- `recht/Bauordnungsrecht.md`

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- Akteure: Brandschutzplaner:innen, Tragwerksplaner:innen, Prüfingenieur:innen, Bauaufsicht, Materialprüfanstalten, Hersteller von Wand-, Decken- und Holzbausystemen, Rückbau- und ReUse-Planer:innen.
- Materialien / Bauteile: tragende Wände, Wohnungstrennwände, Brandabschnittswände, Decken, Dächer, Holzrahmenbau, Brettsperrholz, Stahlbeton, Mauerwerk, Verbundbauteile, bekleidete Stahltragwerke.
- Standards: DIN EN 13501-2, DIN EN 1363-1, DIN EN 1365-1, DIN EN 1365-2, DIN EN 1364 für nichttragende Bauteile, DIN 4102-2/4, MVV TB, Eurocodes im Brandfall.
- Methoden: Klassifizierungsbericht, direkte und erweiterte Anwendung, Ofenprüfung, Bemessung im Brandfall, Abgleich alter F-90-Nachweise mit europäischen Kriterien, Bauteil- und Anschlussdiagnostik.

## Kurzdefinition

**REI 90** ist eine europäische Feuerwiderstandsklasse nach DIN EN 13501-2. Sie bedeutet, dass ein Bauteil oder eine Bauart bei genormter Brandbeanspruchung für mindestens 90 Minuten drei Kriterien erfüllt:

- **R** = Tragfähigkeit
- **E** = Raumabschluss
- **I** = Wärmedämmung unter Brandbeanspruchung

REI 90 ist typisch für tragende und zugleich raumabschließende Bauteile, zum Beispiel tragende Wände und Decken zwischen Brandabschnitten oder Nutzungseinheiten. Die Schreibweise mit Leerzeichen (**REI 90**) ist normtypisch; in Dateinamen oder Kurznotizen erscheint oft **REI90**.

## Relevanz für Wiederverwendung im Bauwesen

REI 90 ist für Wiederverwendung anspruchsvoll, weil drei Leistungen gleichzeitig nachgewiesen werden müssen. Ein wiederverwendetes Bauteil muss im neuen Kontext:

1. Lasten im Brandfall tragen,
2. den Durchtritt von Flammen und heißen Gasen verhindern,
3. den Temperaturanstieg auf der feuerabgewandten Seite begrenzen.

Damit reicht ein reiner Tragfähigkeitsnachweis nicht aus. Ebenso reicht eine raumabschließende Bekleidung nicht aus, wenn die Tragfunktion unklar ist. Bei ReUse von Wänden, Decken und Dachbauteilen muss die gesamte Bauart betrachtet werden: Querschnitt, Schichten, Bekleidung, Fugen, Auflager, Anschlüsse, Öffnungen und Durchdringungen.

## Fachinhalt

### R, E und I als kumulative Kriterien

REI 90 bedeutet, dass alle drei Kriterien über die geforderte Zeit erfüllt werden. Die Klasse wird durch das schwächste maßgebende Kriterium bestimmt. Wenn ein Bauteil R 120, E 90 und I 60 erreicht, ist es nicht REI 90, sondern im kombinierten Sinn höchstens REI 60. Für ReUse muss daher jedes Kriterium einzeln betrachtet werden.

**R – Tragfähigkeit**
- Das Bauteil darf unter vorgegebener mechanischer Last im Brandfall nicht versagen.
- Relevant sind Lastniveau, Spannweite, Auflagerung, Materialfestigkeit, Restquerschnitt, Temperaturentwicklung und Anschlüsse.

**E – Raumabschluss**
- Flammen und heiße Gase dürfen nicht durch Fugen, Risse oder Öffnungen auf die feuerabgewandte Seite gelangen.
- Relevant sind Fugen, Stoßstellen, Durchdringungen, Bauteilanschlüsse und Verformungen.

**I – Wärmedämmung**
- Der Temperaturanstieg auf der feuerabgewandten Seite wird begrenzt, damit sich dort keine brennbaren Materialien entzünden und Rettungswege nutzbar bleiben.
- Relevant sind Materialdicke, Schichtenfolge, Hohlräume, Dämmstoffe, Bekleidungen und Wärmebrücken.

### Anwendungsbereich

REI 90 ist geeignet für tragende Bauteile mit trennender Funktion, zum Beispiel:

- tragende Brandabschnittswände;
- tragende Wohnungstrennwände;
- tragende Treppenraumwände, sofern die konkrete Anforderung dies verlangt;
- Decken zwischen Nutzungseinheiten oder Geschossen;
- Dächer, wenn sie tragend und raumabschließend im Brandfall bewertet werden.

REI 90 ist nicht die richtige Klasse für:

- reine Stützen oder Träger ohne trennende Funktion: hier ist R maßgebend;
- nichttragende Trennwände: hier ist EI maßgebend;
- Türen und Tore: eigene Tür-/Abschlussklassifikation;
- reine Baustoffe: Brandverhalten nach DIN EN 13501-1;
- Abschottungen: eigene Systemnachweise.

### Prüfung und Klassifizierung

Die Klassifizierung REI 90 erfolgt in der Regel auf Basis von Prüfungen nach den einschlägigen EN-Prüfnormen und Klassifizierung nach DIN EN 13501-2. Für tragende Wände ist DIN EN 1365-1 relevant, für Decken und Dächer DIN EN 1365-2. Die allgemeine Prüflogik wird in DIN EN 1363-1 geregelt.

Ein belastbarer REI-90-Nachweis umfasst typischerweise:

- Prüfbericht mit Aufbau, Abmessungen, Materialien, Last, Lagerung, Brandseite und Messwerten;
- Klassifizierungsbericht nach DIN EN 13501-2;
- Angabe des direkten Anwendungsbereichs;
- ggf. erweiterter Anwendungsbereich (EXAP);
- bauaufsichtliche Einordnung nach MVV TB bzw. landesspezifischer Verwaltungsvorschrift;
- Montage- und Ausführungsbedingungen.

Für ReUse muss geprüft werden, ob das wiederverwendete Bauteil innerhalb dieser Bedingungen liegt. Wird ein Bauteil zugeschnitten, anders gelagert, mit anderen Anschlüssen eingebaut oder durchdrungen, kann die Klassifikation nicht ohne Weiteres übernommen werden.

### REI 90 und F 90

In deutschen Bestandsunterlagen findet sich häufig F 90. Eine tragende raumabschließende F-90-Konstruktion kann funktional nahe bei REI 90 liegen. Dennoch ist keine automatische Gleichsetzung zulässig, weil:

- DIN 4102 und DIN EN 13501-2 unterschiedliche Klassifikationslogiken verwenden;
- F 90 nicht explizit R, E und I getrennt ausweist;
- Baustoffanforderungen im nationalen System anders mitgeführt werden können;
- der konkrete Anwendungsbereich aus Prüfzeugnis oder geregelter Konstruktion maßgeblich ist;
- heutige bauaufsichtliche Anforderungen ggf. europäische Klassen oder zusätzliche Kriterien verlangen.

Für Wiederverwendung ist eine nachvollziehbare Übersetzung nötig: Welche Funktion hatte das alte Bauteil? Welche Kriterien wurden tatsächlich geprüft oder geregelt? Welche Klasse wird im neuen Projekt gefordert?

### Besondere ReUse-Aspekte

**Anschlüsse**
REI 90 scheitert häufig nicht im Feld des Bauteils, sondern am Rand: Wand-Decken-Anschluss, Fassade-Wand-Anschluss, Auflagerfuge, Deckenstoß, Anschluss an Bestand. ReUse-Planung muss diese Details neu klassifizieren oder konstruktiv in ein nachgewiesenes System bringen.

**Öffnungen und Durchdringungen**
Türen, Klappen, Schächte, Kabel, Rohre und Lüftungsleitungen unterbrechen die trennende Funktion. Jedes Element benötigt einen passenden Nachweis, der zur REI-90-Anforderung der Wand oder Decke passt.

**Schichtaufbauten**
Bei Holz- und Trockenbaukonstruktionen hängt REI 90 stark von Bekleidung, Kapselung, Dämmung und Hohlraumdetails ab. Wiederverwendete Einzelkomponenten erzeugen noch keinen REI-90-Nachweis.

**Materialalterung**
Betonabplatzungen, korrodierte Bewehrung, beschädigte Brandschutzplatten, offene Fugen oder feuchte Dämmstoffe können R, E oder I mindern.

**Brandbeanspruchungsrichtung**
Bei asymmetrischen Bauteilen kann die Klassifikation von der Brandseite abhängen. Eine Wiederverwendung mit umgekehrter oder beidseitiger Beanspruchung muss gesondert geprüft werden.

## Praxisbezug / Beispiele

### Tragende Bestandswand als REI-90-Trennung

Eine massive Mauerwerkswand wird in einer Umnutzung als Wohnungstrennwand weiterverwendet. Möglicher Nachweisweg: Wanddicke, Steinart, Rohdichte, Mörtel, Putz und Lasten werden ermittelt; Schlitze und Öffnungen werden geschlossen oder nachgewiesen; Anschlüsse an Decke und Fassade werden brandschutztechnisch ertüchtigt. Erst die gesamte Wandlinie kann als REI-90-ähnliche Funktion bewertet werden.

### Wiederverwendete Stahlbetondecke

Eine Stahlbetondecke aus Fertigteilen soll in einem Neubau zwischen Nutzungseinheiten eingesetzt werden. REI 90 verlangt neben Tragfähigkeit auch Raumabschluss an Fugen und Wärmedämmung. Der Nachweis muss daher Plattenquerschnitt, Bewehrung, Fugenverguss, Auflager, Randfugen, Durchbrüche und neue Lasten umfassen. Einzelne Platten mit ausreichender Betonüberdeckung reichen nicht aus, wenn die Fugen nicht nachgewiesen sind.

### Holzbauwand REI 90

Eine Holzrahmen- oder Brettsperrholzwand kann REI 90 erreichen, wenn Querschnitt, Bekleidung, Dämmung, Verbindungsmittel und Anschlüsse als System nachgewiesen sind. Beim ReUse einzelner Holztafeln ist besonders zu prüfen, ob Beplankung, Kapselung, Fugen, Transportbeschädigungen und neue Anschlüsse noch dem Klassifizierungsbericht entsprechen.

### F-90-Bestand in europäischer Projektlogik

Ein Bestandsplan nennt eine tragende Wand „F 90“. Das neue Brandschutzkonzept arbeitet mit REI 90. Die Planungsaufgabe besteht nicht darin, F 90 pauschal umzubenennen, sondern den alten Nachweis zu prüfen, die Bauteilfunktion zu bestimmen und die Kriterien R, E und I für die neue Verwendung nachvollziehbar zu belegen.

## Herausforderungen / offene Fragen

- **Dreifacher Nachweisaufwand**: R, E und I müssen gleichzeitig erfüllt werden; ReUse-Nachweise werden dadurch komplex.
- **Systembindung**: REI 90 bezieht sich meist auf eine Bauart, nicht auf ein isoliertes Material.
- **Fugen und Anschlüsse**: Wiederverwendung verändert Randbedingungen; vorhandene Klassifizierungen decken neue Details oft nicht ab.
- **Asymmetrie**: Viele geprüfte Bauteile gelten nur für bestimmte Brandseiten oder Einbaurichtungen.
- **Alte Nachweise**: F-90-Unterlagen sind oft unvollständig oder nicht direkt in REI 90 übertragbar.
- **Sonderanforderungen**: Brandwände, Sonderbauten, Rettungswege oder Industriebauten können Anforderungen enthalten, die über REI 90 hinausgehen.
- **Regionale Unterschiede**: Die Akzeptanz von Klassifizierungsberichten, Altunterlagen, Gutachten und Abweichungen richtet sich nach Landesrecht und zuständiger Bauaufsicht.
- **Skalierung von ReUse**: Für einzelne Bauteile sind Nachweise teuer. Für zirkuläres Bauen werden standardisierte Bewertungs- und Dokumentationsprozesse für Bauteilgruppen benötigt.

## Quellen

- DIN EN 13501-2:2023-12: Klassifizierung von Bauprodukten und Bauarten zu ihrem Brandverhalten – Teil 2: Klassifizierung mit den Ergebnissen aus den Feuerwiderstandsprüfungen und/oder Rauchschutzprüfungen, mit Ausnahme von Lüftungsanlagen. Bibliografische Daten: https://www.dinmedia.de/de/norm/din-en-13501-2/367755282
- DIN EN 1363-1: Feuerwiderstandsprüfungen – Teil 1: Allgemeine Anforderungen.
- DIN EN 1365-1:2013-08: Feuerwiderstandsprüfungen für tragende Bauteile – Teil 1: Wände.
- DIN EN 1365-2:2015-02: Feuerwiderstandsprüfungen für tragende Bauteile – Teil 2: Decken und Dächer.
- DIN 4102-2: Brandverhalten von Baustoffen und Bauteilen – Bauteile; Begriffe, Anforderungen und Prüfungen.
- DIN 4102-4: Brandverhalten von Baustoffen und Bauteilen – Zusammenstellung und Anwendung klassifizierter Baustoffe, Bauteile und Sonderbauteile.
- DIBt: Muster-Verwaltungsvorschrift Technische Baubestimmungen (MVV TB) 2025/1. https://www.dibt.de/de/suche?q=tb1
- Bauministerkonferenz / DIBt: Musterbauordnung, zuletzt geändert September 2024. https://www.dibt.de/de/aktuelles/meldungen/nachricht-detail/meldung/aenderung-der-musterbauordnung-bekanntgemacht
- Beton.org / InformationsZentrum Beton: Feuerwiderstand von Bauteilen nach DIN EN 13501-2. https://www.betontechnische-daten.de/de/brandschutz/nach-din-13501/feuerwiderstand-von-bauteilen
- MFPA Leipzig: Beispiel eines Klassifizierungsberichts REI 60 / REI 90 nach DIN EN 13501-2 und DIN EN 1365-1, 2024. https://prd-media.crb.ch/media/121263/2024-04_Klassifiz.Bericht_3.2-23-146-3-Thflex%2BWallgf-RF-REI60-REI90.pdf
- Engel, T. u. a.: Nachweismöglichkeiten für den Brandfall im Holzbau, Technische Universität München, 2025. https://mediatum.ub.tum.de/doc/1796118/document.pdf

