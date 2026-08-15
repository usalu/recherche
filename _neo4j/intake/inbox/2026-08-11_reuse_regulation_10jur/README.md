# Intake: Reuse-Regulierung, 10 Jurisdiktionen + EU/EEA (2026-08-11)

## Herkunft

Rohkorpus aus dem semio-Ticket `26/08/11/REGULATORISCHE-RAHMENBEDINGUNGEN-DER-WIEDERVERWENDUNG` (Projekt „Entwerfen mit Bestand", Az. 10.08.18.7-25.06, BBSR/Zukunft Bau, LUH Hannover + UdK Berlin).

- **Hauptlauf:** Workflow-Run `wf_09f66590-20c`, 72 Agenten geplant (W0 Pilot DE · W1 Taxonomie-Freeze + EU-Basis · W2 Länderharvest 10 Jurisdiktionen · W3 Materialfamilien), 55 automatisiert abgeschlossen. Das ursprünglich vorgesehene W3b (Querschnitts-Recht, 6 Agenten) und W4 (Synthese, 8 Agenten) wurden **nicht** ausgeführt — siehe `NICHT_VERARBEITEN.md`.
- **Teil-1-Nachzügler** (2026-08-14, innerhalb desselben Tickets, außerhalb des Workflow-Runs): `material-tga-ausbau.md`, `pruefung/w4-dedup-arbeitsmenge.md` und `pruefung/w4-pruefung-arbeitsmenge.md` wurden von je einem einzelnen, nicht-delegierenden Agenten erstellt. `material-baustahl.md` wurde nach zwei gescheiterten Sub-Delegationsversuchen direkt in der Sitzung verfasst, auf Basis dreier zuvor unabhängig gestarteter, aber vollständig zurückgekehrter Rechercheagenten (DACH, FR/Nordics, UK/NL/BE).
- Dieser Ordner ist eine **vollständige, unveränderte Kopie** von `roh/`, `pruefung/` und `schema/` aus dem Ticket — byte-identisch geprüft (`diff -rq`), Stand 2026-08-14.

## Methodik

- **Primärquellenpflicht.** Tier 1 = amtlicher Gesetzes-/Normtext/Gazette/Behörde; Tier 2 = peer-reviewed + EU-Projektberichte; Tier 3 = Branche/Presse — nur Suchhinweis, nie Beleg.
- **Beleg-Quelle B0–B4** (B0 Primärtext-Volltext … B4 nur Existenz-/Katalognachweis) **+ Zugänglichkeit** (frei-primär · paywalled-eingesehen · paywalled-nicht-eingesehen · frei-primär-blockiert) je Objekt.
- **Bindungsketten-Regel:** Ruht die Bindungswirkung auf einer kostenpflichtigen Norm (DIN/SIA/ÖNORM/NEN/BS/Eurocode), wird zusätzlich der freie amtliche Akt genannt, der sie bindend macht. `B4 + paywalled-nicht-eingesehen` darf nicht als Faktum stehen.
- **Sprache:** nationale Quellen in der Amtssprache gelesen und zitiert; englische Übersetzungen leiten nur die Suche.
- **Adversarische Prüfung** (Länderstufe + Teil 1d) mit sechs Pflichtchecks je Objekt: Supersession, Primärquellen-Pin, Kompetenz/Ebene, Wirkrichtungs-Falsifikation, Scope-Overreach, Quote-back. Status je Aussage: Bestätigt · Korrigiert · Widerlegt · Unbelegbar-paywalled · Fabriziert.

## Sieben-Achsen-Schema (Kurzform — vollständig in `schema/taxonomie-final.md`)

| Achse | Inhalt |
|---|---|
| A | Jurisdiktion/Ebene (EU/EEA · national · sub-national) + A-Ursprung, Downstream-Verifikationsstatus |
| B | Regelungsfeld, Primär-/Nebenfeld (1 Produktrecht · 2 Standsicherheit · 3 Abfallrecht · 4 Schutzziele · 5a Vergabe · 5b Anreize · 6 Normen · 7 Haftung) |
| C | Materialfamilie (10 Werte, mehrwertig, inkl. „Verbund-/Systembauteil") |
| D | Rechtsform (14-stufige Ordinalskala, Projektkonvention, KEINE Rechtshierarchie) |
| E | Prozessphase (8 Werte, mehrwertig, + E-Wirkung) |
| F1/F2 | Wirkrichtung — Rechtslage / Praxiswirkung |
| G | Nachweisanforderung (9 Werte + `entfällt`, ggf. Kaskaden-Notation) |

## Evidenzgrade

**F1, F2 und G-inferiert sind immer E3 — analytische Projektzuordnung, KEINE Quellenaussage.** E1 (textbelegt) gilt regelhaft für A, B, D, Fundstelle, Wortlautbeleg, G-explizit. E2 (Zuordnung ohne Wortlautbeleg) für C bei horizontalen Regeln und E an Phasengrenzen. Evidenzgrade werden je Achse einzeln vergeben, nicht als ein Wert pro Objekt.

---

## ✅ Bereinigung 2026-08-14 — Korpus jetzt vollständig dedupliziert

Alle verbliebenen ID-Kollisionen aus unabhängigen parallelen Agentenläufen sind aufgelöst, und der UK-Präfixbruch (`REG-UK-*` vs. `REG-GB-*` in `UK-F4-7.md`) ist vereinheitlicht. Vollständiges Protokoll: `pruefung/korpus-hygiene.md`.

**Vorher/Nachher:** 681 Regelungsobjekt-Blöcke (unverändert), 616 → **632 eindeutige ID-Strings**, 58 → **0 echte, ungelöste ID-Kollisionen**. 44 IDs erscheinen weiterhin doppelt im rohen Header-Zählwert, aber absichtlich: jeweils ein Verweis-Stub (`„Dublette zu <ID> in <Datei>, verworfen am 2026-08-14…"`) neben der einen kanonischen Fassung — keine Kollision mehr, sondern ein dokumentierter Cross-Reference.

Aufgelöst: 44 echte Dubletten (Verweis an Ort und Stelle, Original unangetastet in der jeweils anderen Datei) und 24 echte Kollisionen (zweites Vorkommen umnummeriert in den freien 090er-Nummernblock je Feld, Inhalt vollständig erhalten, `<!-- Umnummeriert … -->`-Kommentar im Roh-Korpus). Darunter auch die neun Kollisionen, die durch die UK-Präfixvereinheitlichung selbst neu entstanden (`UK-F4-7.md` REG-UK-* → REG-GB-*, kollidierte mit bereits bestehenden REG-GB-*-Objekten in `UK-4Nationen.md`).

**Nicht Gegenstand dieser Bereinigung** (bewusst offen gelassen, s. `pruefung/korpus-hygiene.md` Abschnitt 6): eine separate, kollisionsfreie `REG-UK-*`-Nummernkonvention (900er-Block) in sieben Materialfamilien-Dateien (`material-alu.md`, `material-baustahl.md`, `material-glas.md`, `material-holz.md`, `material-mauerwerk.md`, `material-stahlbeton.md`, `material-tga-ausbau.md`); die abweichende Feld-5-Schreibweise `REG-GB-5-*` (statt `5a`/`5b`) in `UK-4Nationen.md`; die Groß-/Kleinschreibung `5A`/`5B` in den umgestellten `UK-F4-7.md`-IDs; sowie mehrere Cross-ID-Themenüberschneidungen ohne ID-Kollision (unterschiedliche IDs, gleicher Sachverhalt — keine Kollision im technischen Sinn, daher außerhalb des Auftrags "keine Auswertung").

## Weitere bekannte Mängel

- **`abnick_verdacht = true` bei DE** (Länderprüfung, `pruefung/DE.md`): die Prüfquote war auffällig fehlerfrei trotz mehrerer gefundener und korrigierter Fehler (u. a. Zitatmontage REG-EU-1-002) — als Warnsignal für eine mögliche Nicht-Erschöpfung der Prüfung markiert, nicht aufgelöst.
- **18 von 61 Objekten `unbelegbar-paywalled` bei CH** (Länderprüfung, `pruefung/CH.md`) — knapp ein Drittel der Schweizer Objekte konnte in der Prüfstufe nicht über B2 hinaus verifiziert werden.

## Verweis auf die Plattform-relevante Ableitung

Der für die semio-Plattform (Bauteilportal/Wizard-Feldliste, Konfigurator, Bauteilobjekt-Schema) aufbereitete Auszug liegt **nicht** hier, sondern im semio-Repository unter `mit-bestand/bericht/zwischenbericht/temp/regulierung-*.md` (5 Dateien: `regulierung-plattformbezug.md`, `regulierung-belege.md`, `regulierung-achsen.md`, `regulierung-material-zeiger.md`, `regulierung-nachweiswege.md`). Diese fünf Dateien sind eine **Ableitung** dieses Korpus (Auszug + Redaktion nach der Leitregel „Plattform trägt und leitet weiter, stellt keinen Rechtsstatus fest"), keine Ersetzung — für jede rechtsdogmatische Nachfrage ist der vollständige Objektblock hier, nicht der dortige Auszug, maßgeblich.
