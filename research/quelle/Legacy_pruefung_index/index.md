---
entity: "quelle"
id: "Legacy_pruefung_index"
title: "Prüfungen – Index"
build_status: "promoted_phase42"
node_kind: "source"
legacy_type: "Prüfung"
---

# Prüfungen – Index

## Legacy Content

# Prüfungen – Index

## Verknüpfungen

- [leistungsanforderung/](../leistungsanforderung/) – Prüfungen sind die Nachweisseite von Leistungsanforderungen: Tragfähigkeit wird durch statische Nachweisführung und Zugversuch belegt; Brandschutz durch Brandnachweis.
- [standard/](../standard/) – Prüfungen folgen normativen Prüfverfahren: EN ISO 6892-1 für den Zugversuch, DIN EN 13501 für Brandklassifizierung, DIN EN 13791 für Betondruckfestigkeit im Bestand.
- [material/](../material/) — Prüfungen sind materialspezifisch: Holz erfordert Sortierprüfung und ggf. Abbrandbemessung; Stahl Zugversuch und Schweißbarkeitsprüfung; Lehm Eignungsprüfung nach DIN 18940-Reihe.
- [recht/](../recht/) – Prüfungen erfüllen rechtliche Nachweisfunktionen: Bauordnungsrechtliche Verwendbarkeit, ZiE-Unterlagen, Abfallfreigabe, Gewährleistungsgrundlage.
- [prozessphase/](../prozessphase/) – Prüfungen sind phasenbezogen: Schadstoffscreening vor Rückbau, geometrische Vermessung und Sichtprüfung in der Bestandserfassung, Zustandsbewertung nach Aufbereitung, statische Nachweisführung vor Wiedereinbau.
- [dokument/](../dokument/) — Prüfungen erzeugen dokumentierte Nachweise: Prüfberichte, Gutachten, Klassifizierungsberichte, Zustandsklassen, Freimessungsprotokolle.

## Zentrale Unterthemen

- **Erstaufnahme und Erkundung:** Sichtprüfung, geometrische Vermessung und Schadstoffscreening als erste Prüfstufe vor jeder weiteren Entscheidung.
- **Materialprüfung und Werkstoffkennwerte:** Zugversuch, Schweißbarkeitsprüfung und Materialprüfung für belastbare Festigkeitskennwerte bei fehlender Herstellerdokumentation.
- **Statische Nachweisführung:** Berechnung und Beweiskette für Tragfähigkeit gebrauchter Bauteile im neuen statischen Kontext.
- **Brandnachweis und Abbrandbemessung:** Nachweisführung für Brandschutzleistung, die bei gebrauchten Bauteilen häufig ohne ursprüngliche Klassifizierungsberichte auskommt.
- **Materialspezifische Eignungsprüfungen:** Eignungsprüfung Baulehm als Beispiel für nicht-konventionelle Baustoffe mit eigener Prüflogik.
- **Integrierte Zustandsbewertung:** Synthese aller Prüfergebnisse zu einer Wiederverwendungsentscheidung mit Qualitätsklasse und Empfehlung.

## Querverbindungen zu anderen Kategorien

- **Leistungsanforderung:** Prüfungen sind die Nachweisseite von Anforderungen; jede Anforderung erfordert eine passende Prüfmethode und ein dokumentiertes Ergebnis.
- **Methode:** Prüfungen sind methodisch eingebettet: ReUse Assessment orchestriert Prüfschritte, Materialinventur löst Sichtprüfung und geometrische Vermessung aus.
- **Prozessphase:** Prüfungen sind zeitlich gebunden – manche Prüfungen können nur im Einbauzustand durchgeführt werden, andere nur nach dem Ausbau, andere nur im Labor.
- **Material:** Prüfverfahren sind materialspezifisch; Stahl, Holz, Beton, Lehm und Glas haben grundlegend unterschiedliche Prüflogiken, Normreferenzen und Aussagekräfte.
- **Dokument:** Jede Prüfung erzeugt einen Prüfbericht, ein Gutachten oder ein Messdatenblatt; ohne Dokumentation hat eine Prüfung keinen rechtlichen oder vertraglichen Wert.
- **Recht:** Prüfungen erfüllen rechtliche Funktionen: ZiE-Unterlagen, bauordnungsrechtliche Verwendbarkeitsnachweise, Abfallfreigaben, Gewährleistungsgrundlagen.

---

## Offene Lücken / Ausbaufelder

- **Probebelastung:** Direkte Belastungsprüfung eines Tragwerksteils vor Ort als Alternative zu Materialkennwertprüfungen; in `Statische_Nachweisfuehrung.md` erwähnt, aber nicht als eigenständige Prüfung dokumentiert.
- **Zerstörungsfreie Prüfmethoden (ZfP):** Ultraschall, Radiographie, Wirbelstrom, Impaktecho als standardisierte ZfP-Verfahren fehlen als eigenständige Prüfdatei; sie sind in `Materialpruefung.md` und `Geometrische_Vermessung.md` nur am Rande behandelt.
- **Prüfmatrix für Bauteiltypen:** Eine übergreifende Prüfmatrix, die für verschiedene Bauteiltypen (Stütze, Träger, Fenster, Deckenplatte) die relevanten Prüfschritte zusammenstellt, fehlt.
- **Schadstofffreigabe-Protokoll:** Der formelle Abschluss des Schadstoffscreenings mit Freigabe oder Sperrung für Wiederverwendung ist nicht als Prüfdokument ausgearbeitet.
- **Thermografische Untersuchung:** Infrarotthermografie als Prüfmethode für Feuchte, Wärmebrücken und versteckte Schäden in Fassaden und Dächern fehlt als eigenständige Prüfdatei.
