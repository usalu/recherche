# Verbindungen – Index

## Verknüpfungen

- [tragwerkssystem/](../tragwerkssystem/) – Verbindungstechnik definiert die Demontierbarkeit eines Tragwerkssystems; reversible Fügung ist die Systemvoraussetzung für zukünftige Bauteilwiederverwendung.
- [bauteil/](../bauteil/) – Verbindungen sind in Bauteile integriert oder verbinden Bauteile miteinander; Schraubanschlüsse an BSH-Stützen oder Schweißknoten an Stahlträgern bestimmen den Rückbauweg.
- [methode/](../methode/) – Reversibilität als Methode und Design for Disassembly greifen auf die Verbindungstypologie dieser Kategorie zurück.
- [pruefung/](../pruefung/) – Verbindungen müssen geprüft werden: Schweißnahtprüfung, Schraubenanzugsmoment, Klebfugenbewertung, Verbindungsmittelzustand.
- [material/](../material/) — Verbindungstypen sind materialgebunden: Holz → Schrauben, Zapfen, Zimmermannsverbindungen; Stahl → Schrauben, Schweißen, Bolzen; Beton → Vergussmörtel, Stahleinlagen.
- [schadstoff/](../schadstoff/) — Verbindungen können Schadstoffe enthalten oder einschließen: Blei in alten Schweißnähten, PAK in Dichtstoffen, PCP in Klebern.

---

## Kurzüberblick zur Kategorie

Diese Kategorie beschreibt die Verbindungstechniken, die im Bauwesen eingesetzt werden, und bewertet sie hinsichtlich ihrer Reversibilität für spätere Wiederverwendung. Verbindungen entscheiden, ob ein Bauteil als Ganzes ausgebaut werden kann oder ob es beim Rückbau zerstört wird. Reversible Verbindungen (Schrauben, Stecken, Klemmen) sind die Voraussetzung für direkte Wiederverwendung; irreversible Verbindungen (Schweißen, Kleben, Vergießen) erzwingen Materialrecycling oder Bauteilzerstörung.

---

## Zentrale Unterthemen

- **Reversible mechanische Verbindungen:** Verschraubung, Klemmverbindung, Steckverbindung – lösbar mit Werkzeug und mit beherrschbaren Schäden an Verbindungsmitteln.
- **Irreversible stoffschlüssige Verbindungen:** Verschweißung, Verleimung, Vermörtelung – nicht oder nur mit Bauteilzerstörung lösbar; bestimmen das Ende der direkten Wiederverwendungskette.
- **Sonderverbindungen:** Stahlseil als Zugverbindung; konstruktiv eigenständig, aber im ReUse-Kontext kaum eigenständig dokumentiert.

---

## Wichtige Dateien dieser Kategorie

- [Verschraubung.md](Verschraubung.md) — Schrauben, Bolzen, Muttern, Holzschrauben, Ankerschrauben – lösbare Verbindung durch Lösen der Vorspannung oder des Gewindeeingriffs. Wichtigstes Verbindungsmittel für DfD; Protokoll über Anzugsmoment und Schraubenklasse für Wiederverwendung notwendig. EN 14399, EN 15048, ISO 898.

- [Klemmverbindung.md](Klemmverbindung.md) — Verbindung durch Anpressdruck und Reibschluss ohne Durchdringung des Hauptbauteils. Besonders attraktiv für Fassaden, Schienenprofile, Kabeltrassen und lösbare Ausbausysteme. Lösbar durch Entspannen der Klemmkraft; keine Beschädigung des Bauteils.

- [Steckverbindung.md](Steckverbindung.md) — Formschlüssige Verbindung durch Eingreifen, Einstecken, Einrasten. Zimmermannsverbindungen, Zapfen-Schlitz, Steckbolzen, Bajonett – werkzeugarm lösbar oder mit einfachen Mitteln. Japanische und moderne Interlocking-Systeme als Designinspiration für DfD.

- [Verschweissung.md](Verschweissung.md) — Stoffschlüssige Metallverbindung durch thermische Verbindung; nicht zerstörungsfrei lösbar. Im Bestand häufig; Trennschnitte erfordern Brennschnitt, Sägen oder Schleifen. Für Stahl-Skelettbau: je mehr Schweißnähte, desto geringer die ReUse-Chance. Schweißbarkeitsprüfung für Sekundärstahl notwendig.

- [Verleimung.md](Verleimung.md) — Klebstoffverbindung; meist stoffschlüssig und nicht reversibel. Bei BSH und BSP: strukturelle Verleimung nicht lösbar ohne Zerstörung der Schichten. Forschung zu Debonding-Technologien (thermisch, chemisch) noch in Entwicklung. Schadstoffrelevanz bei älteren Klebern (Formaldehyd, lösemittelhaltige Produkte).

- [Vermoertelung.md](Vermoertelung.md) — Mineralische Fügung mit Mörtel; Mauerwerk, Fertigteilfugen, Fliesenverlegung. Bei Ziegeln: mit weichem Kalkmörtel lösbar und für Wiederverwendung geeignet; mit hartem Zementmörtel kaum. Entmörtelung als eigenständige Aufbereitungsmethode. Fertigteilfugen aus Vergussmörtel meist irreversibel.

---

## Querverbindungen zu anderen Kategorien

- **Tragwerkssystem:** Verbindungsprinzipien definieren, ob ein Tragwerkssystem reversibel ist; reversible Fügung als Systemprinzip setzt lösbare Verbindungstypen voraus.
- **Bauteil:** Bauteile tragen die Verbindungsgeometrie; eine BSH-Stütze mit Schraubenanschluss ist demontierbar, eine in Beton eingegossene Stütze nicht.
- **Methode:** Design for Disassembly und Reversibilität beschreiben auf Methodenebene, was auf Verbindungsebene technisch umgesetzt wird.
- **Prüfung:** Verbindungen erfordern eigene Prüfschritte: Zugversuch für Verbindungsmittel, Schweißnahtprüfung (ZfP), Klebfugeninspektion (Bohrwiderstand, Ultraschall).
- **Aufbereitungsmethode:** Verbindungsreste müssen aufbereitet werden: Dübel entfernen, Schrauben nachschneiden, Mörtelrückstände entfernen, Schweißnähte schleifen.

---

## Offene Lücken / Ausbaufelder

- **Niete:** Historische Nietkonstruktionen in Stahltragwerken sind im Bestand häufig und für Wiederverwendung schwierig (nicht lösbar ohne Beschädigung); keine eigenständige Datei.
- **Bolzenverbindung:** Tragende Bolzenverbindung als eigenständige, häufig verwendete reversible Variante fehlt als eigenständige Datei; in anderen Dateien nur als Unterthema.
- **Einbetonierte Verbindungsmittel:** Dübelverbindungen, eingeklebte Stahlteile, Einmörtelankern – häufig im Bestand, für ReUse ein Hindernis; keine eigene Datei.
- **Stahlseil.md:** [Stahlseil.md](Stahlseil.md) ist nur ein Stub; als Zugverbindung in Fassaden, Geländern und Hängekonstruktionen relevant.
- **Zimmermannsmäßige Verbindungen:** Historische Holzverbindungen (Hakenblatt, Zapfen, Schwalbe) sind bei Dachstuhlrückbau relevant; keine eigenständige Datei.
