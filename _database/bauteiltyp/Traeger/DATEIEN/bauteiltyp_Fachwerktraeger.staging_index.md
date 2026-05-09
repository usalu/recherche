---
id: "Fachwerktraeger"
entity: "bauteiltyp"
node_kind: "knot"
migration_status: "migrated_phase2_semantic_corrections"
migration_action: "move_as_knot; semantic_split"
title: "Fachwerktraeger"
legacy_type: "Bauteil; Tragwerkssystem"
legacy_paths:
  - "bauteil\Fachwerktraeger.md"
  - "tragwerkssystem\Dachtragwerk_und_Fachwerk.md"
target_primary: "bauteiltyp/Fachwerktraeger"
target_roles: "phase1_primary; phase2_secondary"
risk_flags: "old_type_tragwerkssystem_overgeneralized"
---
# Fachwerktraeger

## Migration

- Target: bauteiltyp/Fachwerktraeger
- Legacy source count: 2
- Legacy types: Bauteil; Tragwerkssystem
- Migration actions: move_as_knot; semantic_split
- Target roles: phase1_primary; phase2_secondary
- Risk flags: old_type_tragwerkssystem_overgeneralized

## Legacy Content: bauteil\Fachwerktraeger.md

---
type: Bauteil
material: ["[[material/Sekundaerstahl]]"]
verwandt: ["[[bauteil/Brettschichtholzstuetze]]", "[[bauteil/Dachtragwerk]]", "[[bauteil/Pfette]]", "[[bauteil/Stuetze]]", "[[bauteil/Traeger]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** Primärtragwerk; Tragwerksprinzipien; Dach- und Hallentragwerke; Holzbau; Stahlbau; hybride Tragwerke; Knoten und Verbindungsmittel; Bauteilprüfung; Rückbauplanung; Systemwiederverwendung.
- **Verwandte Dateien:** `bauteil/Dachtragwerk.md`; `bauteil/Traeger.md`; `bauteil/Pfette.md`; `bauteil/Stuetze.md`; `bauteil/Brettschichtholzstuetze.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Tragwerksplaner:innen; Prüfingenieur:innen; Stahlbau- und Holzbaubetriebe; Rückbauunternehmen; Bauteilbörsen; K.118 Winterthur; Industrie- und Hallenrückbau; DIN EN 1990; DIN EN 1991; DIN EN 1993; DIN EN 1995; DIN EN 1090 für Stahltragwerke; DIN EN 14080 für Brettschichtholz; DIN SPEC 91484; zerstörungsarme Demontage; Knotenprüfung; Schweißnaht- und Schraubenprüfung; visuelle Holzsortierung; NDT.

## Kurzdefinition

Ein **Fachwerkträger** ist ein tragendes Bauteil oder Bauteilsystem aus stabförmigen Elementen, die meist dreiecksförmig angeordnet sind. Die Stäbe tragen idealisiert überwiegend Normalkräfte: Obergurt und Untergurt übernehmen Druck- oder Zugkräfte, Diagonalen und Pfosten leiten Schub- und Umlenkkräfte. Fachwerkträger ermöglichen große Spannweiten bei geringem Materialeinsatz und sind häufig in Dachtragwerken, Hallen, Brücken, Vordächern und Industriebauten zu finden.

Für Wiederverwendung ist der Fachwerkträger zugleich attraktiv und anspruchsvoll: Er enthält viel tragende Materialleistung, ist aber stark abhängig von Knotengeometrie, Verbindungsmitteln, Aussteifung, Transportfähigkeit und ursprünglichem Lastsystem.

## Relevanz für Wiederverwendung im Bauwesen

Fachwerkträger sind wegen ihrer hohen strukturellen Effizienz wichtige Kandidaten für Re-Use. Eine Wiederverwendung kann erhebliche Material- und Emissionseinsparungen ermöglichen, vor allem bei Stahlfachwerken und großformatigen Holz- oder Brettschichtholzbindern. Gleichzeitig sind sie weniger frei einsetzbar als einfache Träger: Spannweite, Bauhöhe, Dachneigung, Knotenabstände, Anschlusskräfte und Aussteifung müssen zum neuen Entwurf passen.

Die beste Wiederverwendungsstrategie ist häufig die **System- oder Baugruppenwiederverwendung**: Der Fachwerkträger wird als Ganzes, mit definierten Auflagerpunkten und Knoten, erneut eingesetzt. Die Zerlegung in Einzelstäbe ist möglich, kann aber die wirtschaftliche und technische Qualität stark verringern, weil Stabenden, Bohrungen, Nagelplatten oder Schweißnähte oft nicht ohne Querschnittsverlust entfernt werden können.

## Fachinhalt

### Typen und Materialien

Häufige Fachwerkträger im Bestand:

- **Stahlfachwerk:** Walzprofile, Winkel, Hohlprofile, Rundstäbe, Zugstangen; Verbindungen geschraubt, genietet oder geschweißt.
- **Holzfachwerk / Holzfachwerkträger:** Vollholz, KVH, Brettschichtholz; Verbindungen mit Bolzen, Stabdübeln, Schlitzblechen, Nagelplatten, Schrauben, Versätzen, Zapfen oder Stahlteilen.
- **Nagelplattenbinder:** industriell gefertigte Dachbinder mit eingepressten Metallnagelplatten; weit verbreitet bei leichten Dachkonstruktionen.
- **Hybridfachwerk:** Holz- oder BSH-Gurte mit Stahlzugstäben, Stahlknoten, Druckstäben oder Spannsystemen.
- **Historische Fachwerke:** Zimmermannsmäßige Konstruktionen mit Zapfen, Holznägeln, Versätzen, Streben und Schwellen.

Die Wiederverwendbarkeit hängt weniger vom Trägerprinzip als von Verbindung und Zustand ab. Geschraubte und gebolzte Fachwerke sind grundsätzlich besser demontierbar als geschweißte, genagelte, geklebte oder mit Nagelplatten verbundene Systeme.

### Tragverhalten

Fachwerkträger funktionieren über Stabkräfte und Knoten. Für den zweiten Einsatz sind zu prüfen:

- Druckstäbe auf Knicken und lokale Schäden;
- Zugstäbe auf Querschnittsverlust, Anschlusslöcher, Rissbildung, Korrosion oder Faserverlauf;
- Gurte auf Biegung aus Nebenwirkungen, Dachlasten zwischen Knoten oder Anschlussmomente;
- Knoten auf Lochleibung, Ausreißen, Schweißnahtqualität, Schrauben- oder Dübeltragfähigkeit;
- Auflagerknoten auf Querdruck, Lagerpressung, Exzentrizität und Montagebeschädigung;
- Aussteifung gegen seitliches Ausweichen des Obergurts;
- Gebrauchstauglichkeit durch Durchbiegung und Schwingung;
- Brandschutz, insbesondere bei Stahlknoten in Holzfachwerken.

Ein Fachwerkträger ist nicht automatisch wiederverwendbar, nur weil seine Stäbe unbeschädigt wirken. Knoten, Aussteifung und geometrische Imperfektionen sind häufig maßgebend.

### Bewertung im Bestand

Ein Pre-Demolition-Audit sollte folgende Informationen erfassen:

- Spannweite, Bauhöhe, Systemtyp, Knotenabstände, Dachneigung, Auflagerart;
- Material der Gurte, Diagonalen und Pfosten;
- Profil- oder Querschnittsabmessungen, Stückzahl und Wiederholbarkeit;
- Verbindungstypen und Zustand der Knoten;
- vorhandene Verstärkungen, Umbauten, abgeschnittene Stäbe, provisorische Reparaturen;
- Korrosion, Risse, Schweißnahtfehler, Holzfäule, Insektenbefall, Delamination;
- Beschichtungen, Brandschutzanstriche, Holzschutzmittel, mögliche Schadstoffe;
- Demontageweg, Kranbarkeit, Transportlänge, temporäre Stabilisierung;
- zugehörige Aussteifungsverbände und Pfetten, die für Systemwirkung erforderlich sind.

Bei Fachwerken ist die Zuordnung der Bauteile im neuen Entwurf besonders wichtig. Markierung und Dokumentation müssen Knoten- und Stabposition enthalten, nicht nur „Träger 1“ oder „Binder 2“.

### Rückbau und Zwischenzustände

Während des Rückbaus können Fachwerkträger instabil werden, sobald Dachscheibe, Pfetten oder Windverbände entfernt sind. Erforderlich sind:

- Montage- und Demontagestatik;
- temporäre Verbände oder Anschlagpunkte;
- kontrollierte Lastfreistellung vor dem Lösen der Auflager;
- Schutz der Knoten vor Verformung beim Kranhub;
- Vermeidung von Anschlagkräften, die nicht dem ursprünglichen Lastbild entsprechen;
- Lagerung in Ebenen, die Verwindung und lokale Eindrückungen verhindern.

Insbesondere große Holzfachwerkträger können bei unsachgemäßem Heben Verdrehungen oder Druckfalten entwickeln, die im eingebauten Zustand nicht vorhanden waren.

### Wiederverwendungsstrategien

1. **Direkte Systemwiederverwendung:** Der Träger wird in gleicher oder ähnlicher Spannweite erneut verwendet. Das ist tragwerkslogisch am einfachsten, verlangt aber Entwurfsanpassung an vorhandene Geometrie.
2. **Verkürzte Wiederverwendung:** beschädigte Enden oder Auflagerbereiche werden abgeschnitten; neue Auflagerdetails entstehen. Dies kann sinnvoll sein, wenn Querschnitt und Knotenabstand passen.
3. **Baugruppenreuse:** mehrere Binder mit Pfetten und Verbänden werden als Dachfeld übernommen. Dadurch bleibt Systemwissen erhalten.
4. **Stabreuse:** Einzelstäbe werden ausgebaut und als neue Stützen, Pfetten oder Streben verwendet. Das ist nur sinnvoll, wenn Knotenbereiche schadensarm entfernt werden können.
5. **Materialreuse / Remanufacturing:** Holzstäbe werden zu kürzeren Bauteilen oder nichttragenden Elementen umgearbeitet; Stahlprofile werden geprüft und neu konfektioniert.

### Knoten als Schlüsselstelle

Knoten bestimmen die Wiederverwendbarkeit. Bewertungskriterien:

- lösbar oder zerstörend zu öffnen;
- Resttragfähigkeit nach Lochbild, Riss, Korrosion oder Einkerbung;
- Möglichkeit, vorhandene Bohrungen erneut zu nutzen;
- Zugänglichkeit für Inspektion und spätere Demontage;
- Austauschbarkeit von Schrauben, Bolzen, Dübeln oder Stahlblechen;
- Korrosionsschutz bei Stahlteilen;
- Brandschutzverhalten der Verbindung;
- Toleranzausgleich für neue Einbausituationen.

Nagelplattenbinder sind problematisch: Die Metallplatten sind häufig nicht zerstörungsfrei lösbar, die Knotentragfähigkeit hängt vom Einpresszustand ab, und eine Re-Zertifizierung einzelner Binder ist aufwendig. Sie können als Ganzes eher wiederverwendbar sein als zerlegt.

## Praxisbezug / Beispiele

- **Stahlfachwerke aus Industriehallen:** Oft gut wiederverwendbar, wenn sie geschraubt sind, Korrosion begrenzt ist und Profilgüte geprüft oder nachgewiesen werden kann. Transportlängen und Brandschutz können die Wiederverwendung begrenzen.
- **Holzfachwerkträger in Dachhallen:** Gute Kandidaten bei trockener Innenraumexposition und gebolzten Knoten. Bei Nagelplatten, starken Anschlusslöchern oder unbekannter Feuchtegeschichte steigt der Prüfaufwand.
- **Historische Dachwerke:** Können hohe handwerkliche Qualität und robuste Querschnitte besitzen, sind aber häufig individuell, verformt und nicht nach heutigen Normen sortiert. Wiederverwendung erfordert denkmalpflegerische, materialtechnische und statische Bewertung.
- **K.118 Winterthur:** Das Projekt zeigt für wiederverwendete tragende Stahlbauteile, dass Re-Use die Entwurfslogik verändert: verfügbare Bauteile, Anschlüsse und Geometrien werden zu Planungsparametern.
- **Temporäre Bauten und Ausstellungshallen:** Fachwerke aus modularen Systemen haben besonders hohes Wiederverwendungspotenzial, wenn sie geschraubt, standardisiert und dokumentiert sind.

## Herausforderungen / offene Fragen

- **Knotennachweise:** Für wiederverwendete Fachwerke sind Knoten häufig kritischer als Stäbe.
- **Geometrische Passung:** Spannweite, Bauhöhe und Dachneigung sind schwer an neue Grundrisse anzupassen.
- **Transport und Lagerung:** Große Träger benötigen Sonderlogistik; falsches Heben kann Schäden erzeugen.
- **Systemabhängige Stabilität:** Ohne Aussteifung können Druckgurte und Binder seitlich instabil werden.
- **Unklare Materialkennwerte:** Besonders bei historischen Holzfachwerken und alten Stahlprofilen sind Festigkeitswerte, Duktilität, Schweißbarkeit oder Holzqualität unsicher.
- **Verbindungsmittelalterung:** Korrosion, Ermüdung, Lochaufweitung, Risse und Setzungen können die Anschlusskapazität reduzieren.
- **Zulassung und Verantwortung:** Wiederverwendung als tragendes System erfordert projektbezogene Nachweise und Abstimmung mit Prüf- und Genehmigungsstellen.

## Quellen

- DIN EN 1990: Eurocode – Grundlagen der Tragwerksplanung.
- DIN EN 1991: Eurocode 1 – Einwirkungen auf Tragwerke.
- DIN EN 1993: Eurocode 3 – Bemessung und Konstruktion von Stahlbauten.
- DIN EN 1995: Eurocode 5 – Bemessung und Konstruktion von Holzbauten.
- DIN EN 1090: Ausführung von Stahltragwerken und Aluminiumtragwerken.
- DIN EN 14080: Holzbauwerke – Brettschichtholz und Balkenschichtholz.
- DIN SPEC 91484:2023-09: Pre-Demolition-Audits.
- Ministerium für Landesentwicklung und Wohnen Baden-Württemberg: *Leitfaden zur Wiederverwendung tragender Bauteile*, 2025.
- Ottenhaus, L.-M. u. a.: *Design for adaptability, disassembly and reuse – A review of reversible timber connection systems*, Construction and Building Materials, 2023.
- Pozzi, L. E.: *Design for Disassembly with Structural Timber Connections*, TU Delft, 2019.
- Stricker, E. u. a.: *Case Study K.118 – The Reuse of Building Components in Winterthur, Switzerland*, Journal of Physics: Conference Series, 2023.
- VDI Zentrum Ressourceneffizienz: *Rückbau im Hochbau – Aktuelle Praxis und Potenziale der Ressourceneffizienz*, 2023.
- ECOS / Ridley-Ellis, D.: *Laying the foundations to safely reuse timber in Europe*, 2025.

## Legacy Content: tragwerkssystem\Dachtragwerk_und_Fachwerk.md

---
type: Tragwerkssystem
verwandt: ["[[tragwerkssystem/Holz_Skelettbau]]", "[[tragwerkssystem/Reversible_Fuegung]]", "[[tragwerkssystem/Stahl_Skelettbau]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** Tragwerkssysteme; Dächer; Fachwerke; weitgespannte Tragwerke; Rückbauplanung; Bauteilwiederverwendung.
- **Verwandte Dateien:** `tragwerkssystem/Holz_Skelettbau.md`; `tragwerkssystem/Stahl_Skelettbau.md`; `tragwerkssystem/Reversible_Fuegung.md`; `bauteil/Dach.md`; `bauteil/Holzbalken.md`; `bauteil/Stahltraeger.md`; `verbindung/Zimmermannsverbindung.md`; `verbindung/Bolzenverbindung.md`; `verbindung/Schweissverbindung.md`; `pruefung/Holzpruefung.md`; `pruefung/Stahlpruefung.md`; `reuse_strategie/Bauteilernte.md`; `projekt/Hallenumbau.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Zimmerer; Stahlbauer; Rückbauunternehmen; Kran- und Hebetechnik; Tragwerksplanung; Holzschutz- und Korrosionsgutachten; EN 1990/1991/1993/1995; ISO 20887; SCI P427 für Stahlbauteile; FCRBE-Materialblätter; historische Bauaufnahme; 3D-Scan; Bauteilkataster.

## Kurzdefinition

Dachtragwerke und Fachwerke sind Tragstrukturen, die Lasten aus Dachdeckung, Schnee, Wind, Eigengewicht, Installationen und gegebenenfalls Nutzlasten in Wände, Stützen oder Rahmen ableiten. Fachwerke bestehen aus stabförmigen Elementen, die über Knoten zu Dreiecks- oder Raumstrukturen verbunden sind. Für Wiederverwendung sind sie besonders interessant, weil viele Dach- und Hallentragwerke aus identifizierbaren, stabförmigen Holz- oder Stahlbauteilen bestehen und häufig relativ zugänglich sind.

## Relevanz für Wiederverwendung im Bauwesen

- **Bauteilqualität:** Pfetten, Sparren, Binder, Fachwerkträger, Stahlträger und Knotenbleche besitzen oft klare Geometrien und können nach Prüfung direkt oder kaskadiert wiederverwendet werden.
- **Zugänglichkeit:** Dächer sind meist von oben und innen zugänglich; die Demontage ist oft einfacher als bei eingebauten Decken- oder Wandtragwerken.
- **Hohe Spannweiten:** Wiederverwendete Binder und Fachwerke können in Hallen, Pavillons, Überdachungen, Werkstätten oder Aufstockungen wertvoll sein.
- **Systemabhängigkeit:** Der ReUse-Wert liegt nicht nur im Einzelstab, sondern im Knoten- und Gesamtsystem. Ein ganzer Binder ist oft wertvoller als einzelne herausgeschnittene Stäbe.
- **Risiko durch Umbauten:** Dachtragwerke wurden häufig durch Öffnungen, Installationen, Solaranlagen, Lüftungsgeräte, Brandschutzbekleidungen oder Feuchteschäden verändert. Diese Eingriffe müssen dokumentiert werden.

## Fachinhalt

### Typologien

- **Holz-Sparren- und Pfettendächer:** Einzelstäbe, traditionelle Zimmermannsverbindungen, Nägel, Schrauben und Stahlbleche. ReUse hängt von Querschnitt, Länge, Holzfeuchte, Befall und Verbindungsschäden ab.
- **Holzfachwerkbinder:** Dreiecksbinder, Nagelplattenbinder, Brettschichtholzbinder, historische Hänge- und Sprengwerke. Nagelplattenbinder sind oft leicht und effizient, aber beim Ausbau empfindlich; historische Binder können wegen Handwerksqualität und Dimensionen wertvoll sein.
- **Stahlfachwerke und Stahlbinder:** Genietete, geschraubte oder geschweißte Fachwerke; Hallenbinder; Dachverbände; Pfetten aus Walzprofilen oder Kaltprofilen. Geschraubte Systeme sind am besten wiederverwendbar.
- **Raumfachwerke:** Dreidimensionale Stab-Knoten-Systeme. Hohe ReUse-Chancen bei standardisierten Schraubknoten; problematisch bei Korrosion, Sondergeometrien und fehlender Knotenklassifizierung.
- **Hybriddächer:** Kombinationen aus Stahl, Holz, Beton, Zugstäben, Dachscheiben und Aufbeton. Leistungsfähig, aber bei flächigem Verbund und verdeckten Anschlüssen schwer trennbar.

### Fügungsprinzipien

- **Günstig für ReUse:** Bolzen, Schrauben, Passbolzen, Knotenbleche, Steck- oder Klemmknoten, traditionelle Holzzapfen mit lösbaren Sicherungen, aufgeschraubte Pfetten und abnehmbare Aussteifungen.
- **Ungünstig:** Verklebte Verbundschichten, eingeschäumte oder vergossene Anschlüsse, verschweißte Knoten ohne Schnittstrategie, verdeckte Nagelplatten, korrodierte Verbindungsmittel, Dachaufbauten mit flächiger Verklebung.
- **Knotenbewertung:** Knoten sind häufig maßgebend. Bei Fachwerken können kleine Schäden an Knotenblechen, Schraubenlöchern oder Stabdübeln die Wiederverwendung stärker begrenzen als der Zustand des Stabes.

### Demontage und Wiederverwendung

- **Vorbereitung:** Bauaufnahme, Lastpfad verstehen, temporäre Aussteifung planen, Montagefolge rekonstruieren, Hebepunkte definieren, Dachdeckung und Installationen getrennt erfassen.
- **Rückbaufolge:** Dachhaut und Auflasten entfernen; Verbände sichern; Binder einzeln stabilisieren; Knoten lösen; Bauteile nummerieren; Lagerung trocken, belüftet und verwindungsarm.
- **Wiederverwendungsvarianten:**
  - ganzer Binder oder Fachwerkträger in gleicher oder ähnlicher Spannweite;
  - Einzelstäbe als Pfetten, Balken, Unterzüge, Aussteifungen oder Ausbauholz;
  - Stahlprofile nach Prüfung als Sekundärträger oder in Nebentragwerken;
  - historische Bauteile in denkmalpflegerischen oder repräsentativen Anwendungen.

### Prüf- und Schadensbilder

- **Holz:** Feuchte, Pilzbefall, Insektenbefall, Rissbildung, Querschnittsschwächung durch alte Anschlüsse, Verformungen, Brandspuren, chemischer Holzschutz, Tragfähigkeitsklassifizierung.
- **Stahl:** Korrosion, Querschnittsverlust, Lochbilder, Kerben, Schweißnahtqualität, alte Nieten, Verformungen, Ermüdungsbeanspruchung, Beschichtungen mit Schadstoffen.
- **System:** fehlende Verbände, nachträglich entfernte Stäbe, unklare Auflager, Setzungen, unzureichende Robustheit im Demontagezustand.

## Praxisbezug / Beispiele

- **Industriehallen:** Stahlbinder, Pfetten und Verbände aus Hallen sind oft serienmäßig und trocken zugänglich. Bei geschraubten Verbindungen können ganze Rahmen oder Fachwerke demontiert und in ähnlichen Gebäuden wieder eingesetzt werden.
- **Landwirtschaftliche Gebäude:** Große Holz- oder Stahlträger sind häufig vorhanden, aber Feuchte, Ammoniakbelastung und Korrosion müssen geprüft werden.
- **Historische Dachwerke:** Alte Holztragwerke können handwerklich wertvoll sein. Bei Denkmalen steht oft Erhalt in situ im Vordergrund; Wiederverwendung außerhalb des Gebäudes ist nur bei unvermeidbarem Rückbau zu bewerten.
- **Umbau mit Dachöffnung:** Wenn ein Dach im Zuge einer Aufstockung entfernt wird, kann es als Bauteillager dienen: Ziegel, Lattung, Sparren, Pfetten, Stahlteile und Dämmstoffe werden getrennt inventarisiert.

## Herausforderungen / offene Fragen

- **Standsicherheit während des Rückbaus:** Fachwerke sind als Gesamtsystem stabil. Einzelne Stäbe oder Verbände dürfen nicht ohne temporäres Konzept entfernt werden.
- **Unvollständige Daten:** Historische Querschnitte, Holzarten, Stahlgüten, Verbindungsmittel und Lastannahmen sind häufig unbekannt.
- **Anpassung an neue Normlasten:** Schneelasten, Windlasten, Brandanforderungen, PV-Lasten und Nutzungsänderungen können Wiederverwendung begrenzen.
- **Maß- und Geometriebindung:** Ganze Binder sind wertvoll, aber stark an Spannweite, Dachneigung, Transport und Gebäuderaster gebunden.
- **Oberflächen und Schadstoffe:** Alte Holzschutzmittel, Bleimennige, PAK- oder asbesthaltige Beschichtungen können Ausbau und Wiederverwendung verhindern.
- **Knotenverlust:** Wird ein Fachwerk beim Rückbau zerschnitten, sinkt sein Systemwert stark. Rückbauplanung sollte daher zuerst System-ReUse prüfen und erst danach Einzelteil-ReUse.

## Quellen

- ISO 20887:2020: *Design for disassembly and adaptability*. https://www.iso.org/standard/69370.html
- Steel Construction Institute: *P427 Structural steel reuse: assessment, testing and design principles / protocol for reusing structural steel*. https://steel-sci.com/assets/downloads/steel-reuse-protocol-v06.pdf
- PROGRESS / ECCS: *European Recommendations for Reuse of Steel Products in Single-Storey Buildings*, 2020. https://www.steelconstruct.com/wp-content/uploads/PROGRESS_Design_guide_final-version.pdf
- FCRBE / Rotor: *Reuse Toolkit: material sheets*. https://rotordb.org/en/projects/reuse-toolkit-material-sheets
- Ottenhaus, L.-M. et al.: *Design for adaptability, disassembly and reuse – A review of reversible timber connection systems*, Construction and Building Materials, 2023.
- ECOS / Ridley-Ellis et al.: *Laying the foundations to safely reuse timber in Europe*, 2025. https://ecostandard.org/wp-content/uploads/2025/08/2025-08_ECOS-policy-standards-timber-reuse.pdf
- EN 1990, EN 1991, EN 1993, EN 1995 mit nationalen Anhängen; nationale Regeln für Bestandsbewertung, Holzschutz, Stahlbau und Rückbau.

