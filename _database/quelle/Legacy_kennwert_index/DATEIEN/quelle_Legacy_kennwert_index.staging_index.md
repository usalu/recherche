---
id: "Legacy_kennwert_index."
entity: "quelle"
node_kind: "source"
migration_status: "migrated_phase5_legacy_source"
title: "Kennwerte – Index"
legacy_path: "kennwert\\index.md"
migration_action: "merge_into_index"
legacy_type: "Kennwert"
target_primary: "kennwertdefinition/index"
target_secondary: ""
risk_flags: "index_content_may_contain_unique_gaps_or_cluster_lists"
---
# Kennwerte – Index

## Migration

- Legacy path: kennwert\index.md
- Action in migration map: merge_into_index
- Reason: not already consumed by phase 1-4, so preserved as source/meta node.
- Original primary target: kennwertdefinition/index
- Original secondary targets: 

## Legacy Content

---
type: Kennwert
---

# Kennwerte – Index

## Verknüpfungen

- [methode/](../methode/) – Kennwerte sind das Messinstrumentarium von Methoden wie ReUse Assessment und LCA; ohne quantifizierte Kennwerte bleibt die Bewertung von Wiederverwendung qualitativ und nicht vergleichbar.
- [wirtschaft/](../wirtschaft/) – Wirtschaftliche Kennzahlen (Kostenvergleich, LCC, Restwert) und ökologische Kennwerte (CO₂-Einsparung, graue Energie) werden in der Gesamtbewertung zusammengeführt; ökologische Kennwerte sind monetarisierbar.
- [dokument/](../dokument/) – LCA-Berichte, EPDs und Materialpässe sind die Dokumente, in denen Kennwerte erfasst, berechnet und nachgewiesen werden; ohne belastbare Dokumentation sind Kennwerte nicht verwendbar.
- [standard/](../standard/) – EN 15978, EN 15804, ISO 20887 und SIA 2032 sind die normativen Rahmen, die Kennwert-Definitionen, Berechnungsmethoden und Systemgrenzen festlegen.
- [pruefung/](../pruefung/) – Kennwerte müssen prüfbar sein; ohne Prüfverfahren für Demontagegrad, Wiederverwendungsquote und Materialkennwerte sind Angaben im Materialpass nicht belastbar.
- [reuse_strategie/](../reuse_strategie/) – Kennwerte machen Strategievergleiche möglich; CO₂-Einsparung je Strategie, Demontagegrad als DfD-Bewertungsindikator, Wiederverwendungsquote als Projekterfolgsmaß.

---

## Kurzüberblick zur Kategorie

Diese Kategorie beschreibt die quantitativen Indikatoren, mit denen die Nachhaltigkeit, die Rückbaubarkeit und die Wiederverwendungsleistung von Bauteilen und Projekten bewertet werden. Kennwerte sind die Sprache, in der ReUse-Leistung kommuniziert, verglichen und zertifiziert wird. Sie reichen von der CO₂-Einsparung durch Wiederverwendung über den Demontagegrad als Konstruktionsbewertung bis zur Wiederverwendungsquote als Projekterfolgsmaß. Ohne Kennwerte ist kein Benchmarking, kein Zertifizierungsnachweis und keine politische Steuerung möglich.

---

## Zentrale Unterthemen

- **Treibhausgasminderung:** CO₂-Einsparung als zentraler ökologischer Vorteilsnachweis für Wiederverwendung; Modulstruktur nach EN 15978 (A1–D) als Berechnungsrahmen.
- **Graue Energie:** Embodied Energy (PENRT/PERT) als zweiter ökologischer Schlüsselindikator neben CO₂; SIA 2032 und KBOB als Schweizer Referenzsystem.
- **Rückbaubarkeit:** Demontagegrad (D0–D4) als konstruktionsbezogener Indikator für zukünftige Wiederverwendbarkeit; ISO 20887 und Level(s) 2.4 als Bewertungsrahmen.
- **Wiederverwendungsquote:** Fünf Quotentypen (Input, Output, Erhalt, Potenzial, CO₂-gewichtet); Level(s) 2.1/2.2 und EU C&D-Waste-Protocol als Bezugsrahmen.
- **Materialwert:** Sechs Wertformen von Materialwert bis ökologischem Restwert; Netto-Materialwert-Formel und Madaster als Bewertungswerkzeuge.

---

## Wichtige Dateien dieser Kategorie

- [CO2_Einsparung.md](CO2_Einsparung.md) — CO₂-Einsparung durch Bauteilwiederverwendung im Vergleich zu Neubau; Modulstruktur nach EN 15978 (Herstellung A1–A3, Entsorgung C1–C4, Gutschrift Modul D). Berechnungsbeispiel K.118 Winterthur mit ca. 60 % Einsparung an grauer Energie gegenüber konventionellem Neubau; Systemgrenze und Referenzgebäude als kritische Variablen jeder Vergleichsrechnung.

- [Demontagegrad.md](Demontagegrad.md) — Fünfstufige Klassifikation D0 (nicht demontierbar) bis D4 (vollständig werkzeugfrei demontierbar); ISO 20887 als internationaler Normrahmen, Level(s)-Indikator 2.4 als europäischer Bewertungsrahmen. Zehn Bewertungsdimensionen (Zugänglichkeit der Verbindungen, Lösbarkeit, Beschädigung beim Lösen, Entkopplung von Schichten u.a.); Demontagegrad ist Konstruktionskennwert, kein Zustandskennwert.

- [Graue_Energie.md](Graue_Energie.md) — Embodied Energy in PENRT (nicht erneuerbare Primärenergie) und PERT (erneuerbare Primärenergie) als Indikatoren; SIA 2032 (Schweiz) und KBOB-Ökobilanzdaten als verbreitetes europäisches Referenzsystem. Unterschied zwischen Herstellungsenergie (A1–A3) und Lebenszyklusenergie (A1–D); bei Wiederverwendung entfällt Herstellungsenergie teilweise, Aufbereitungsenergie wird gutgeschrieben oder verrechnet.

- [Materialwert.md](Materialwert.md) — Sechs Wertformen: Materialwert (Schrottpreis), Nutzungswert (Funktion), Marktwert (Nachfrage), Buchrestwert (bilanziell), Seltenheitswert (Marktknappheit) und ökologischer Restwert (graue Energie). Netto-Materialwert-Formel als einfache Annäherung; DGNB und Madaster als Bewertungsrahmen für Gebäude-als-Materiallager; Restwert als Anreizinstrument für frühe Rückbauplanung.

- [Wiederverwendungsquote.md](Wiederverwendungsquote.md) — Fünf Quotentypen: Input-Quote (Anteil Sekundärmaterial am Gesamteinsatz), Output-Quote (Anteil wiederverwendeter Bauteile am Rückbau), Erhaltungsquote (Anteil der nicht angetasteten Substanz), Potenzialquote (technisch möglicher Anteil) und CO₂-gewichtete Quote. Level(s)-Indikatoren 2.1 und 2.2 als EU-Bewertungsrahmen; Einheitenproblem (Masse, Volumen, Stückzahl, ökonomischer Wert) bei Vergleich von Quoten verschiedener Projekte.

---

## Querverbindungen zu anderen Kategorien

- **Methode:** Kennwerte sind Messgrößen für Methoden; ReUse Assessment, LCA und Materialpass erzeugen Kennwerte, die wiederum Methodenentscheidungen informieren.
- **Wirtschaft:** CO₂-Einsparung ist als CO₂-Preis monetarisierbar; graue Energie und Materialwert sind wirtschaftliche Größen, wenn Ressourcenknappheit eingepreist wird.
- **Standard:** Jeder Kennwert hat einen normativen Rahmen (EN 15978 für CO₂, ISO 20887 für Demontagegrad, EN 15804 für EPD); ohne Normreferenz ist kein Kennwert projektübergreifend vergleichbar.
- **Dokument:** Kennwerte werden in LCA-Berichten, EPDs, Materialpässen und Zertifizierungsnachweisen (DGNB, LEED) dokumentiert; Dokument-Kategorie enthält die Formate, Kennwert-Kategorie den Inhalt.
- **Reuse-Strategie:** Kennwerte machen Strategievergleiche möglich; welche Strategie erzeugt mehr CO₂-Einsparung, welche höheren Demontagegrad, welche bessere Wiederverwendungsquote?
- **Prüfung:** Kennwerte müssen prüfbar sein; Demontierbarkeit wird durch Konstruktionsanalyse geprüft, CO₂-Einsparung durch LCA-Berechnung, Wiederverwendungsquote durch Massenerfassung.

---

## Offene Lücken / Ausbaufelder

- **Lebensdauer als Kennwert:** Technische und funktionale Lebensdauer von Sekundärbauteilen im Vergleich zu Neubauteilen fehlt als eigenständiger Kennwert; kritisch für LCC und LCA.
- **Ressourcenintensität:** Material Input per Unit of Service (MIPS) und ähnliche Ressourcenintensitätskennwerte fehlen als Ergänzung zu CO₂ und grauer Energie.
- **Quantitative Benchmarks:** Vergleichswerte für gute und schlechte ReUse-Leistung fehlen; ohne Benchmark ist eine Wiederverwendungsquote von 30 % nicht einzuordnen.
- **Soziale Kennwerte:** Beschäftigungseffekte, lokale Wertschöpfung und soziale Nachhaltigkeitsindikatoren fehlen als Ergänzung zu ökologischen Kennwerten.
- **Kennwerte für Materialpass-Qualität:** Ein Index für die Vollständigkeit und Verlässlichkeit von Materialpässen fehlt; Datenlücke und Kennwertlücke sind oft synonym.
