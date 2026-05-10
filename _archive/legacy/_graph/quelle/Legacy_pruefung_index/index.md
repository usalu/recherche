---
id: "Legacy_pruefung_index."
entity: "quelle"
node_kind: "source"
migration_status: "migrated_phase5_legacy_source"
title: "Prüfungen – Index"
legacy_path: "pruefung\\index.md"
migration_action: "merge_into_index"
legacy_type: "Prüfung"
target_primary: "pruefung_nachweis/index"
target_secondary: ""
risk_flags: "index_content_may_contain_unique_gaps_or_cluster_lists"
---
# Prüfungen – Index

## Migration

- Legacy path: pruefung\index.md
- Action in migration map: merge_into_index
- Reason: not already consumed by phase 1-4, so preserved as source/meta node.
- Original primary target: pruefung_nachweis/index
- Original secondary targets: 

## Legacy Content

---
type: Prüfung
---

# Prüfungen – Index

## Verknüpfungen

- [leistungsanforderung/](../leistungsanforderung/) – Prüfungen sind die Nachweisseite von Leistungsanforderungen: Tragfähigkeit wird durch statische Nachweisführung und Zugversuch belegt; Brandschutz durch Brandnachweis.
- [standard/](../standard/) – Prüfungen folgen normativen Prüfverfahren: EN ISO 6892-1 für den Zugversuch, DIN EN 13501 für Brandklassifizierung, DIN EN 13791 für Betondruckfestigkeit im Bestand.
- [material/](../material/) — Prüfungen sind materialspezifisch: Holz erfordert Sortierprüfung und ggf. Abbrandbemessung; Stahl Zugversuch und Schweißbarkeitsprüfung; Lehm Eignungsprüfung nach DIN 18940-Reihe.
- [recht/](../recht/) – Prüfungen erfüllen rechtliche Nachweisfunktionen: Bauordnungsrechtliche Verwendbarkeit, ZiE-Unterlagen, Abfallfreigabe, Gewährleistungsgrundlage.
- [prozessphase/](../prozessphase/) – Prüfungen sind phasenbezogen: Schadstoffscreening vor Rückbau, geometrische Vermessung und Sichtprüfung in der Bestandserfassung, Zustandsbewertung nach Aufbereitung, statische Nachweisführung vor Wiedereinbau.
- [dokument/](../dokument/) — Prüfungen erzeugen dokumentierte Nachweise: Prüfberichte, Gutachten, Klassifizierungsberichte, Zustandsklassen, Freimessungsprotokolle.

---

## Kurzüberblick zur Kategorie

Diese Kategorie dokumentiert die prüftechnischen Methoden und Bewertungsverfahren, die für die Freigabe, Qualifizierung und Nachweisführung wiederverwendbarer Bauteile erforderlich sind. Prüfungen sind im Reuse-Kontext kein bürokratischer Aufwand, sondern die epistemische Grundlage: Ein Bauteil ist nicht wiederverwendbar, weil man es für wiederverwendbar hält, sondern weil man es geprüft, bewertet und dokumentiert hat. Die Prüftiefe richtet sich nach Bauteilart, Einbausituation, Leistungsanforderung und verfügbarer Dokumentation.

---

## Zentrale Unterthemen

- **Erstaufnahme und Erkundung:** Sichtprüfung, geometrische Vermessung und Schadstoffscreening als erste Prüfstufe vor jeder weiteren Entscheidung.
- **Materialprüfung und Werkstoffkennwerte:** Zugversuch, Schweißbarkeitsprüfung und Materialprüfung für belastbare Festigkeitskennwerte bei fehlender Herstellerdokumentation.
- **Statische Nachweisführung:** Berechnung und Beweiskette für Tragfähigkeit gebrauchter Bauteile im neuen statischen Kontext.
- **Brandnachweis und Abbrandbemessung:** Nachweisführung für Brandschutzleistung, die bei gebrauchten Bauteilen häufig ohne ursprüngliche Klassifizierungsberichte auskommt.
- **Materialspezifische Eignungsprüfungen:** Eignungsprüfung Baulehm als Beispiel für nicht-konventionelle Baustoffe mit eigener Prüflogik.
- **Integrierte Zustandsbewertung:** Synthese aller Prüfergebnisse zu einer Wiederverwendungsentscheidung mit Qualitätsklasse und Empfehlung.

---

## Wichtige Dateien dieser Kategorie

- [Zustandsbewertung.md](Zustandsbewertung.md) — Fachliche Gesamtbeurteilung eines Bauteils oder Bauteilkollektivs für eine definierte Anschlussnutzung. Integriert Sichtprüfung, Vermessung, Materialprüfung, Schadstoffscreening, Dokumentenlage und Logistik. Ergebnis ist eine nachvollziehbare Entscheidung: direkte Wiederverwendung, Aufbereitung, andere Nutzung oder Entsorgung.

- [Sichtpruefung.md](Sichtpruefung.md) — Systematische, überwiegend zerstörungsfreie visuelle Untersuchung. Erster Prüfschritt im Wiederverwendungsprozess; erfasst sichtbare Schäden, Gebrauchsspuren, Verbindungssituationen und Schadstoffverdachte. Beweisniveau niedrig, aber unverzichtbar als Vorselektion.

- [Geometrische_Vermessung.md](Geometrische_Vermessung.md) — Erfassung von Form, Lage, Abmessungen, Verformung und Anschlussgeometrie. Beantwortet nicht nur „Wie groß?", sondern: Ist das Bauteil demontierbar, transportierbar, kompatibel und mit vertretbarem Aufwand wiedereinbaubar?

- [Schadstoffscreening.md](Schadstoffscreening.md) — Systematische Vorerkundung und Analyse potenziell gefährlicher Stoffe vor Rückbau oder Wiederverwendung. Ein tragfähiges Bauteil kann durch Asbest, PCB, PAK oder Holzschutzmittel vollständig ausgeschlossen werden; Schadstofffreiheit ist eine Mindestvoraussetzung.

- [Materialpruefung.md](Materialpruefung.md) — Zerstörungsfreie, zerstörungsarme oder zerstörende Untersuchung von Werkstoffeigenschaften. Liefert belastbare Materialkennwerte für Festigkeit, Dauerhaftigkeit, Korrosionszustand und Zusammensetzung, wenn Herstellerdokumentation fehlt.

- [Statische_Nachweisfuehrung.md](Statische_Nachweisfuehrung.md) — Rechnerische, prüftechnische und dokumentarische Begründung für Tragfähigkeit, Gebrauchstauglichkeit und Dauerhaftigkeit. Bei Wiederverwendung: Beweiskette aus Identifikation, Prüfung, Klassifizierung, Bemessung, Ausführung und Qualitätssicherung statt bloßer Berechnung mit Normkennwerten.

- [Brandnachweis.md](Brandnachweis.md) — Dokumentierte Begründung für Erfüllung brandschutzrechtlicher Anforderungen. Bei gebrauchten Bauteilen ohne Klassifizierungsberichte: gutachterliche Stellungnahmen, neue Brandprüfungen oder projektbezogene Kompensationsmaßnahmen. Weiter gefasst als Abbrandbemessung.

- [Abbrandbemessung.md](Abbrandbemessung.md) — Brandschutztechnische Bemessung von Holzbauteilen über zeitabhängigen Querschnittsverlust im Brandfall. Bei wiederverwendeten Holzteilen: Ausgangspunkt ist der geprüfte Ist-Zustand mit vorhandenen Rissen, Bohrungen, Ausklinkungen und unbekannten Sortierklassen; nicht der Neubauquerschnitt.

- [Zugversuch.md](Zugversuch.md) — Zerstörende Materialprüfung für mechanische Kennwerte von Stahl: Streckgrenze, Zugfestigkeit, Bruchdehnung, Duktilität. Unverzichtbar für Sekundärstahl ohne Werkszeugnisse; kein alleiniger Eignungsnachweis – Schweißbarkeit, Kerbschlagzähigkeit und Geometrie müssen ergänzend bewertet werden.

- [Schweissbarkeitspruefung.md](Schweissbarkeitspruefung.md) — Untersuchung, ob ein Metallbauteil unter definierten Bedingungen sicher geschweißt werden kann. Bei Sekundärstahl aus unbekannter Herkunft oder historischen Stahlsorten besonders kritisch; ältere Stähle, Gusseisen und kaltverformte Profile können nur eingeschränkt oder gar nicht schweißgeeignet sein.

- [Eignungspruefung_Baulehm.md](Eignungspruefung_Baulehm.md) — Material- und anwendungsbezogene Prüfung lehmhaltiger Baustoffe für einen neuen Einsatz. Drei Herkunftsarten: direkt wiederverwendbare Lehmteile, rezyklierbare Lehmbaustoffe und Bauaushub; je unterschiedliche Prüfanforderungen nach DIN 18940-Reihe.

---

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
