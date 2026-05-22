# Leitlinien & Workflows für skalierbare Bauteil‑Wiederverwendung

> **Design-Vertiefung.** Eine eigene, projektübergreifende Entwurfs-/Design-Perspektive
> (Design-Herausforderungen, umgekehrter Workflow D0–D7, Werkzeugkasten inkl. Phoenix3D/DGBC/Madaster,
> zehn Design-Muster und Design-Steckbriefe je Projekt) steht in
> [`DESIGN_MIT_REUSE_PROJEKTE.md`](DESIGN_MIT_REUSE_PROJEKTE.md).

**Grundlage.** Abgeleitet aus (a) der Auswertung von 83 dokumentierten Reuse‑Projekten mit dem
Reuse‑Scalability Index **v3** ([`PROJEKT_SKALIERBARKEIT_ANALYSE.md`](PROJEKT_SKALIERBARKEIT_ANALYSE.md)),
(b) etablierten Rahmenwerken — für **Design**: **Durmisevic (Transformation Capacity)**, die
**DGBC/Alba‑Concepts‑Disassembly‑Potential‑Methode**, **Brands Shearing Layers**, ISO 20887;
für Bewertung/Skalierung: MCI, EU Level(s), RVI, BCR‑Feasibility, Reuse Market Dynamics,
Küpfer/Fivet‑MCDA, **Multi‑Level‑Perspektive** (siehe
[`REUSE_SCALABILITY_FRAMEWORK.md`](REUSE_SCALABILITY_FRAMEWORK.md)) — und (c) extern verifizierten
Projektbelegen ([`verified_enrichment.json`](verified_enrichment.json)).

**Kernbotschaft.** Zwei Hebel entscheiden über Skalierung: **Bezug** (Reverse‑Logistik als
Marktmodell) und **zirkuläres Design** (reproduzierbare, demontier‑ und austauschbare Bauweise) —
beglaubigt durch **Nachweis** (Legitimation) und **Wirkung** (CO₂). Wiederverwendung *einbauen*
ist gelöst; sie **rechtzeitig, in Menge und in belegter Qualität zu beschaffen** und **so zu
entwerfen, dass die nächste Runde möglich bleibt**, ist der Engpass. Priorität deshalb:
**Bezug ↔ Design → Nachweis → Wirkung**.

---

## Teil A — Acht Leitlinien (Design Principles)

Jede Leitlinie nennt: *Regel · Evidenz aus den Daten · Rahmenwerk · Anti‑Muster.*

### L1 — Aggregieren statt Einzelfund: baue ein Bezugs‑Portfolio
- **Regel:** Plane von Beginn an **≥3–5 Spenderquellen** (Abbruch, Umbau, Überschuss‑Lager,
  Händler, öffentliche Bestände) parallel; behandle Beschaffung als eigenes Gewerk.
- **Evidenz:** Nur 7 von 83 Projekten sind echte Aggregatoren; **KA13** (25+ Quellen) führt
  die Rangliste (RSI 79,8) an, gerade weil sein Bezugsmodell wiederholbar ist. **Circl** (7 Quellen,
  Urban Mining + 16 000 Mitarbeiter‑Jeans) und **Kamikatsu** (~700 Fenster von Einwohnern) zeigen
  zwei Beschaffungs‑Varianten: professionelles Urban Mining und **Community‑Spenden**.
- **Rahmenwerk:** Reverse‑Logistik‑Barriere (Reuse Market Dynamics 2024); BCR‑Geschäftsmodell.
- **Anti‑Muster:** „Tiefen‑Pilot" mit 95–100 % Quote aus **einer** glücklichen Quelle
  (SUPERLOCAL, BedZED) — hohe Tiefe, kaum übertragbar.

### L2 — Früh und flexibel entwerfen: „form follows availability"
- **Regel:** Verankere Bauteil‑Voruntersuchung (Pre‑Demolition‑/Bestandsaudit) **vor** dem
  Entwurf; halte Raster, Spannweiten und Anschlüsse **tolerant** gegenüber realen Fundmaßen.
- **Evidenz:** K.118 und TRÆ dokumentieren explizit „entkoppelte, geschichtete" Bauweise,
  weil Fundteile selten dem Sollmaß entsprechen.
- **Rahmenwerk:** Level(s) 2.3 (Adaptability); ISO 20887 (Versatility/Convertibility).
- **Anti‑Muster:** fixes Detail zuerst, Bauteilsuche danach → teure Sonderanfertigung.

### L3 — Ziele auf die Hybridquote (~50–65 %), nicht auf 100 %
- **Regel:** Setze reuse‑seitig auf **strukturell wirksame** Mengen (Tragwerk, Fassade,
  Decken), nicht auf 100‑%‑Symbolik; ergänze mit bio‑/geo‑basierten Neubaustoffen.
- **Evidenz:** Küpfer/Fivet zeigen ~65 % als Optimum; KA13 (80 % *bei* 25 Quellen) und K.118
  (~50 % *als* Prinzip) skalieren besser als reine 100‑%‑Fälle.
- **Rahmenwerk:** Küpfer/Fivet MCDA (2021); Level(s) 2.2/2.4.
- **Anti‑Muster:** Quote als Selbstzweck; Scope‑Tricks (z. B. „97 %" nur auf ein Gewerk).

### L4 — Reuse zuerst am Tragwerk (höchster Hebel, höchste Hürde)
- **Regel:** Prüfe Stahl‑/Beton‑/Holz‑Tragglieder zuerst; sie tragen den größten
  CO₂‑ und Wert‑Hebel — und die härtesten Nachweise (Güte, Ermüdung, Statik).
- **Evidenz:** K.118 (Stahltragwerk aus Basel = 26 % der THG‑Reduktion, ‑91 % vs. RC‑Stahl);
  55 GSS (Stahlkern 97 % Reuse); Big‑Dig‑Häuser (Stahlträger).
- **Rahmenwerk:** ISO 20887 (System-/Element‑Ebene); RVI‑Technik (Normkonformität, Restwert).
- **Anti‑Muster:** Reuse nur bei Oberflächen/Mobiliar → gutes Bild, geringe Wirkung.

### L5 — Zirkuläres Design: Independence + Exchangeability (Durmisevic/DGBC) als Standard
- **Regel:** Maximiere die **Transformationskapazität** = *Unabhängigkeit* (funktionale
  Entkopplung der Schichten nach Brand) **×** *Austauschbarkeit* (Bauteile ohne Beschädigung der
  Umgebung lösbar). Konkret nach DGBC‑Kriterien: **reversibler Verbindungstyp** (schrauben/klemmen/
  stecken statt kleben/schweißen/vergießen), **Zugänglichkeit der Fügung**, **Unabhängigkeit**
  (keine durchdringenden Abhängigkeiten), **einfache Bauteilkanten‑Geometrie**. Es zählt das
  **schwächste Glied** — eine geklebte Schicht entwertet die ganze Kette.
- **Evidenz:** **People's Pavilion** (Design 100: nur Gurt‑/Spanngurt‑Fügung, kein Schrauben/
  Kleben/Sägen → nach 9 Tagen unbeschädigt zurück), Recyclinghaus (leimfrei, Buchendübel,
  typenrein), K.118 (geschichtet/entkoppelt, sichtbar demontierbar), Kindergarten Mööslistrasse
  (Stahl gecuttet/neu verplattet/verschraubt).
- **Rahmenwerk:** Durmisevic Transformation Capacity; DGBC/Alba‑Concepts DP‑Methode; Brand
  Shearing Layers; ISO 20887 (Zugänglichkeit, Unabhängigkeit, Einfachheit, Standardisierung).
- **Anti‑Muster:** Verbundbauteile/Klebeschichten und durchdringende Installationen, die späteres
  Reuse ausschließen; „geschichtet gezeichnet, aber monolithisch gefügt".

### L8 — Design ≠ Skalierbarkeit: mach die Methode zum Produkt
- **Regel:** Behandle nicht nur das Gebäude, sondern die **übertragbare Methode** als Ergebnis —
  Harvest‑Map/Bauteilkatalog, DGBC‑Checkliste, Rückbau‑Playbook, Musterverträge fürs Leihen.
  Ein voll reversibles, aber **temporäres/geliehenes oder einzelfund‑abhängiges** Objekt skaliert
  nur, wenn sein *Verfahren* wiederholbar dokumentiert ist.
- **Evidenz:** **People's Pavilion** (Design 100, aber #2 statt #1 — temporär/geliehen);
  **Villa Welpeloo** (als Einzelhaus mittelmäßig, aber die **Harvest‑Map/Oogstkaart** wurde zum
  Standard‑Workflow und ihr eigentlicher Skalierungsbeitrag).
- **Rahmenwerk:** Strategic Niche Management (Legitimation + Wissenstransfer); MLP Niche→Regime.
- **Anti‑Muster:** spektakulärer Einzelbau ohne dokumentiertes, wiederholbares Verfahren.

### L6 — Alles nachweisen: Bauteilpass, Zustand, Konformität
- **Regel:** Führe je Bauteilcharge einen **Materialpass** (Herkunft, Menge, Zustandsklasse,
  Prüf-/Schadstoffstatus, Bearbeitungsschritte). Ohne Daten kein Wiederverkauf, keine Statik,
  keine Förderung.
- **Evidenz:** Das Recyclinghaus verwarf einen Stahl‑Rohbau, weil **Materialdaten (Güte)
  fehlten** — die Informationslücke kippte das Konzept.
- **Rahmenwerk:** Informationslücke (Reuse Market Dynamics); Madaster‑Materialpässe; RVI.
- **Anti‑Muster:** undokumentiertes Handwerk → nicht übertragbar, nicht auditierbar.

### L7 — Wirkung quantifizieren (CO₂), früh und vergleichbar
- **Regel:** Rechne **A1–A5 GWP** und die Reuse‑Einsparung gegen einen Neubau‑Benchmark,
  in kgCO₂e/m² *und* absolut (t) — das ist die verwertbarste Antragskennzahl.
- **Evidenz:** KA13 (70 %), K.118 (60 %/~494 t), 55 GSS (‑36 % vs. LETI, ~386 kgCO₂e/m²),
  TRÆ (26 %). Wo dieser Nachweis fehlt, sinkt die Konfidenz im RSI.
- **Rahmenwerk:** Level(s) 1.2 (GWP, Modul D); Embodied‑Carbon‑Benchmarks (LETI).
- **Anti‑Muster:** qualitative „nachhaltig"‑Aussagen ohne Bilanz.

---

## Teil A2 — Drei organisatorische Skalierungs‑Hebel (2. Projektwelle)

Die stärksten Hebel sind oft **nicht baulich, sondern kodifizierbar** — vertraglich, finanziell,
organisatorisch. Sie skalieren besser als jede Einzeltechnik, weil sie sich **wiederverwenden** lassen.
Herleitung: [`AKTEURE_KETTEN_UND_LERNMUSTER.md`](AKTEURE_KETTEN_UND_LERNMUSTER.md) (Teil B2, P9–P11).

### L9 — Reuse als eigenes Vergabe‑Los ausschreiben (öffentliche Bauherren)
- **Regel:** Richte ein **dediziertes Reuse‑Gewerk („Lot 01")** ein und schreibe mit einem
  **Varianten-/Lücken‑Leistungsverzeichnis („CCTP à trous")** aus, das reale Fundmaße zulässt,
  statt Neuprodukte zu spezifizieren.
- **Evidenz:** **Grande Halle de Colombelles** — erstes Gebäude mit Lot 01 (Le WIP); Reuse‑Kosten
  nur 2 % der Operation, 3 dauerhafte Stellen. Vertragsmuster ist copy‑paste‑fähig.
- **Rahmenwerk:** öffentliche Beschaffung als Regime‑Hebel (MLP/SNM). **Anti‑Muster:** Reuse als
  unverbindliche „Option" im Standard‑LV → fällt bei Zeitdruck als Erstes heraus.

### L10 — Demontierbarkeit bepreisen: Geschäftsmodell vor Technik
- **Regel:** Sichere den **Restwert** über **Leasing / pay‑per‑use / Rückkaufgarantie**; dann wird
  Demontierbarkeit zum Bilanz‑Argument, nicht nur zum Umwelt‑Argument.
- **Evidenz:** **The Green House** (15 J + 1 Tag; ROI 2–3 statt 5 J.; Kit‑of‑parts inkl. lösbarer
  Fundamente), **Circl** (geleaste Aufzüge/Beleuchtung als Product‑as‑Service).
- **Rahmenwerk:** BCR‑Feasibility; Product‑as‑Service. **Anti‑Muster:** DfD als reine
  Absichtserklärung ohne Restwert‑ oder Rücknahmevereinbarung.

### L11 — Für tragende/heikle Bauteile: Wertschöpfungsketten‑Konsortium bilden
- **Regel:** Bündle Uni + Rückbau + **Werk‑Veredler mit Produktzulassung** + Ingenieur + Architekt +
  GU + Behörde in *einem* Vorhaben, um die Nachweis‑/Zulassungsbarriere **kollektiv** zu lösen.
- **Evidenz:** **Härmälänranta/ReCreate** — tragender Vorfertigbeton (nicht DfD‑entworfen), im Werk
  aufbereitet, mit Produktzulassung + Umweltgenehmigung; Assembly „wie mit Neuteilen".
- **Rahmenwerk:** SNM (kollektive Legitimation); erzeugt Normen‑Input statt Einzelfall‑Workaround.
- **Anti‑Muster:** Einzelbüro versucht tragenden Reuse ohne Werk-/Zulassungspartner → scheitert am Nachweis.

---

## Teil B — Fünf operative Workflows

Jeder Workflow: *Auslöser · Schritte · Rollen · Output/Nachweis · RSI‑Dimension · Vorbild.*

### W1 — Reverse‑Logistik‑ & Bezugs‑Workflow  → RSI‑Dimension **Bezug**
**Auslöser:** Projektstart / Vorentwurf.
1. **Bedarfs‑Grobliste** je Bauteilgruppe (Menge, Maßtoleranz, Funktion) aufstellen.
2. **Quellen‑Scan** parallel: (a) Abbruch-/Umbaukataster der Region, (b) Bauteilbörsen &
   Händler, (c) öffentliche/eigene Bestände, (d) Überschuss der Hersteller.
3. **Bauteiljäger:in** beauftragen (eigene Rolle), Pre‑Demolition‑Audits anstoßen.
4. **Zwischenlager/Timing** klären: Lagerfläche, Rückbaufenster ↔ Bauzeit synchronisieren.
5. **Portfolio‑Regel:** kein Gewerk aus nur einer Quelle; Ausfallreserve je kritischem Bauteil.
- **Output/Nachweis:** Quellenliste mit ≥3 Spendern je kritischem Gewerk, Beschaffungswege
  dokumentiert. **Vorbild:** KA13, Kindergarten Mööslistrasse.

### W2 — Bauteil‑Audit, Bewertung & Materialpass  → RSI **Reife**
**Auslöser:** Kandidat‑Bauteil identifiziert.
1. **Aufnehmen:** Typ, Material, Maße, Menge, Herkunft/Baujahr, Fotos.
2. **Zustandsklasse** vergeben (visuell + ggf. Prüfung); Schadstoff‑Screening.
3. **Konformität** klären: Norm/Statik‑Nachweis, ggf. „End‑of‑Waste"-Status, Gewährleistung.
4. **Aufbereitungsbedarf** und -kosten festhalten; Rest‑/Marktwert schätzen (RVI‑Logik).
5. **Materialpass** anlegen (maschinenlesbar) → in den Graphen zurückspeisen.
- **Output/Nachweis:** Bauteilpass je Charge; Zustands-/Prüfstatus. **Vorbild:** Madaster‑Logik;
  Gegenbeispiel Recyclinghaus (fehlende Stahlgüte → verworfen).

### W3 — Transformationskapazitäts‑Prüfung (Durmisevic / DGBC / ISO 20887)  → RSI **Design**
**Auslöser:** Entwurf/Detaillierung.
1. **Schichten‑Check nach Brand** (Site/Structure/Skin/Services/Space/Stuff): jede Schicht so
   entkoppeln, dass sie unabhängig von den anderen austauschbar ist (unterschiedliche Lebensdauern).
2. **Independence‑Bewertung:** funktionale Cluster/Zonen bilden; durchdringende Abhängigkeiten
   (Installationen quer durch Struktur/Skin) vermeiden.
3. **Exchangeability‑Bewertung (DGBC‑Kriterien):** je Verbindung **Verbindungstyp** (reversibel?),
   **Zugänglichkeit der Fügung**, **Unabhängigkeit**, **Geometrie der Bauteilkante** einstufen;
   Disassembly‑Potential über das **schwächste Glied** (harmonisches Mittel) bilden.
4. **Verbindungswahl:** schrauben/klemmen/stecken statt kleben/schweißen/vergießen; Fügeteile
   und Toleranzen dokumentieren; Standardraster/‑maße bevorzugen.
5. **Rückbau‑Szenario** mitliefern (Demontagereihenfolge, Werkzeug, Wiederverwendbarkeit).
- **Output/Nachweis:** DP‑Bewertung + DfD‑Checkliste + Rückbaukonzept. **Vorbild:** People's
  Pavilion (Referenz), Recyclinghaus, K.118, Grubenstrasse 29.

### W4 — Wirkungs‑ & Compliance‑Nachweis (LCA/GWP)  → RSI **Wirkung** + **Reife**
**Auslöser:** Vorentwurf (früh!) und As‑built.
1. **Benchmark** definieren (konventioneller Neubau; LETI/Level(s)-Zielwert).
2. **A1–A5 GWP** rechnen; Reuse als Modul‑D‑Gutschrift/als vermiedene Primärproduktion.
3. **Doppelte Kennzahl** ausweisen: kgCO₂e/m² **und** absolute t‑Einsparung.
4. **Regel‑Fit** dokumentieren (nationale LCA‑Pflicht, Zertifizierung, Fördervorgaben).
- **Output/Nachweis:** GWP‑Bilanz + Prozent-/t‑Einsparung. **Vorbild:** KA13, K.118, 55 GSS.

### W5 — RSI‑Entscheidungs‑Workflow (Priorisieren & Vergleichen)  → alle Dimensionen
**Auslöser:** Projektauswahl, Referenzsuche, Antrag, Review.
1. **Scoren:** `_score_scalability_v6.py` laufen lassen (v3-Proxy + `verified_enrichment_v6.json`).
2. **Filtern** nach Ziel: Versorgung → K2 ≥ 3 + Archetyp *Aggregator*; Nachweis tragend → K4, G3/G4;
   DfD-Vorbild → K9 = 4 (nicht als Skalierungsgarantie).
3. **Lücken lesen:** niedrigste K-Scores und Gates = konkrete To-dos (meist K2, K3, G4, G6).
4. **Verifizieren:** Konfidenzklasse C mit Primärquellen anreichern (`verified_enrichment_v6.json`).
5. **Iterieren:** RSI final + Gates als Steuerungs-Dashboard; v3-Werte nicht mischen.
- **Output/Nachweis:** priorisierte Shortlist + Maßnahmenliste je Projekt.

---

## Teil C — Von der Diagnose zur Maßnahme (Schnellzuordnung)

| Wenn der niedrigste Sub‑Score … | dann Workflow | typische Maßnahme |
|---|---|---|
| **Bezug** | W1 | zusätzliche Spenderquellen, Bauteiljäger:in, Börsen/Depots einbinden |
| **Reife** | W2 | Materialpässe, Zustandsklassen, Prüf-/Schadstoffnachweise nachziehen |
| **Design** | W3 | reversible Verbindungen, Schichten entkoppeln, DP/DfD‑Checkliste, Rückbaukonzept |
| **Wirkung** | W4 | A1–A5‑GWP‑Bilanz + t/%‑Einsparung gegen Benchmark rechnen |
| **Maßstab/Tiefe** | L3/L4 | Reuse an Tragwerk/Fassade verlagern, Hybridquote anpeilen |
| **Bezug (öffentlich)** | L9 | Reuse als eigenes Vergabe‑Los + CCTP à trous ausschreiben |
| **Wirtschaftlichkeit** | L10 | Restwert über Leasing/Rückkauf sichern (Demontierbarkeit bepreisen) |
| **Nachweis (tragend)** | L11 | Value‑chain‑Konsortium mit Werk‑Veredler/Produktzulassung bilden |

---

## Teil D — Reifegrad‑Leiter (wohin skalieren?)

1. **Klein‑Pilot / Reallabor** — Prinzip testen, Bauteilpass etablieren.
2. **DfD‑Referenz (Design‑Vorbild)** — schadenfreie, voll reversible Fügung als Detail‑Standard.
3. **System‑Pilot** — reproduzierbare, entkoppelte Bauweise + Rückbaukonzept (Methode als Produkt).
4. **Tiefen‑Pilot** — hohe Quote, aber Quelle verbreitern (sonst Sackgasse).
5. **Großmaßstab‑Demonstrator** — Pilotmaßstab verlassen, Wirkung belegen.
6. **Aggregator** — Reverse‑Logistik als **wiederholbares Marktmodell** (Zielzustand).

> Der Weg nach oben führt fast immer über **Teil A/L1 (Bezug verbreitern)** und
> **Teil B/W4 (Wirkung belegen)** — die zwei Dimensionen, in denen das Feld heute am
> schwächsten ist. Gutes **Design (L5/W3)** ist die Voraussetzung, aber allein kein Aufstieg:
> erst mit skalierbarem Bezug **und** dokumentierter Methode (L8) wird es übertragbar.
