---
entity: "quelle"
id: "Legacy_prozessphase_index"
title: "Prozessphasen – Index"
build_status: "promoted_phase42"
node_kind: "source"
legacy_type: "Prozessphase"
---

# Prozessphasen – Index

## Legacy Content

# Prozessphasen – Index

## Verknüpfungen

- [methode/](../methode/) – Methoden werden in Prozessphasen eingesetzt: Materialinventur in der Bestandserfassung, Zirkuläre Ausschreibung in der Ausschreibungsphase.
- [reuse_strategie/](../reuse_strategie/) – Strategien bestimmen, welche Phasen durchlaufen werden und welche Tiefe der Eingriff hat.
- [dokument/](../dokument/) – Jede Prozessphase erzeugt charakteristische Dokumente: Bestandsaufnahme → Materialinventar, Rückbau → Rückbaukataster, Wiedereinbau → Einbaudokumentation.
- [pruefung/](../pruefung/) – Prüfungen sind phasenspezifisch: Schadstoffscreening vor Rückbau, Materialprüfung vor Wiedereinbau, Zustandsbewertung nach Aufbereitung.
- [logistik/](../logistik/) – Transport, Lagerung und Materialmatching sind eigenständige Logistikphasen, die parallel zur Hauptprozessphase laufen.
- [recht/](../recht/) – Rechtliche Anforderungen begleiten jede Phase: Abfallrecht im Rückbau, Vergaberecht in der Ausschreibung, Produkthaftung im Wiedereinbau.

## Zentrale Unterthemen

- **Vorbereitung und Dokumentation:** Bestandserfassung und Pre-Demolition Audit als Grundlage für alle nachfolgenden Entscheidungen.
- **Entwurf und Planung:** Bauteilgetriebener Entwurf, Ausschreibung und Vergabe als zirkuläre Planungsarbeit.
- **Physischer Rückbau:** Selektive Demontage als Bauteilgewinnung, nicht als Abbruch.
- **Aufbereitung, Lagerung, Transport:** Die Zwischenphasen, die Rückbau und Wiedereinbau verbinden und häufig unterschätzt werden.
- **Wiedereinbau:** Integration geprüfter Bauteile in die neue Baustruktur mit Nachweis, Abnahme und Dokumentation.
- **Betrieb und Rückbauplanung:** Lebenszyklusphase nach Fertigstellung, in der ReUse-Potenzial erhalten oder zerstört wird.

## Querverbindungen zu anderen Kategorien

- **Methode:** Jede Phase wendet Methoden an: Bestandserfassung nutzt Materialinventur und ReUse Assessment; Rückbau setzt selektiven Rückbau und Schadstoffscreening voraus.
- **Dokument:** Phasen erzeugen und konsumieren Dokumente: Bestandserfassung → Materialinventar und Bestandsaufnahme; Ausschreibung → Ausschreibungstext und Bauteilkatalog; Wiedereinbau → Materialpass und Einbaudokumentation.
- **Logistik:** Transport, Lagerung und Materialverfügbarkeit sind eigenständige Logistikprozesse, die mehrere Phasen überspannen und oft als Flaschenhals wirken.
- **Prüfung:** Prüfungen sind phasenspezifisch gebunden: Schadstoffscreening vor Rückbau, geometrische Vermessung und Zustandsbewertung nach Aufbereitung, statische Nachweisführung vor Wiedereinbau.
- **Recht:** Jede Phase ist rechtlich eingebettet: Rückbau unter Abfall- und Arbeitsschutzrecht, Ausschreibung unter Vergaberecht, Wiedereinbau unter Bauordnungsrecht und Gewährleistung.

---

## Offene Lücken / Ausbaufelder

- **Übergabe und Abnahme:** Die formelle Abnahme wiederverwendeter Bauteile und die Gewährleistungsregelung sind noch nicht als eigenständige Prozessphase abgebildet.
- **Marktvermittlung:** Der Schritt zwischen Lagerung und Wiedereinbau – Vermarktung, Matching, Plattformnutzung – fehlt als eigene Phase; er liegt zwischen `logistik/` und `prozessphase/`.
- **Rückbauplanung als eigenständige frühe Phase:** Rückbauplanung findet vor dem Rückbau statt und gehört eigentlich in die Vorplanungsphase; sie ist derzeit unter `Betrieb_und_Rueckbauplanung.md` eingeordnet.
- **Monitoring und Qualitätssicherung im Betrieb:** Systematische Inspektion, Schadenserfassung und Bauteilzustandspflege im Betrieb sind nicht als Subprozess dokumentiert.
