# Entwerfen mit Wiederverwendung — Herausforderungen, Workflow, Werkzeuge, Projekt-Ansätze

**Zweck.** Dieses Dokument bündelt die **Entwurfs-/Design-Perspektive** über alle 21 verifizierten
Benchmark-Projekte (und einige einschlägige Graph-Fälle). Es beantwortet vier Fragen konkret:
**Welche Design-Herausforderungen** entstehen beim Bauen mit wiederverwendeten Bauteilen, **welcher
Workflow** beherrscht sie, **welche Werkzeuge** unterstützen ihn, und **welcher detaillierte Ansatz**
steckt hinter jedem Projekt.

**Kernthese.** Entwerfen mit Reuse ist kein Materialaustausch im fertigen Entwurf — es ist ein
**umgekehrter Entwurfsprozess**: *„form follows availability"*. Erst wird gesucht/geerntet, dann
entworfen; das verfügbare Lager ist **Entwurfs-Input**, nicht Entwurfs-Ergebnis. Die zwei
Design-Größen, die über Skalierbarkeit entscheiden, sind **Transformationskapazität** (wie leicht
lässt sich das Gebäude wieder zerlegen) und **Toleranz gegenüber realen Fundmaßen**.

**Verankerung.** Design-Dimension des [`REUSE_SCALABILITY_FRAMEWORK.md`](REUSE_SCALABILITY_FRAMEWORK.md)
(Durmisevic *Transformation Capacity*; DGBC/Alba-Concepts *Disassembly-Potential*; Brand *Shearing
Layers*; ISO 20887). Ergänzt die Rangliste [`PROJEKT_SKALIERBARKEIT_ANALYSE.md`](PROJEKT_SKALIERBARKEIT_ANALYSE.md),
die Akteure [`AKTEURE_KETTEN_UND_LERNMUSTER.md`](AKTEURE_KETTEN_UND_LERNMUSTER.md) und die
Leitlinien [`REUSE_GUIDELINES_UND_WORKFLOWS.md`](REUSE_GUIDELINES_UND_WORKFLOWS.md).

---

## Teil A — Die neun Design-Herausforderungen

| # | Herausforderung | Kern des Problems | Projekt-Beleg |
|---|---|---|---|
| **C1** | **Umgekehrter Entwurfsprozess** | Der Entwurf muss *offen bleiben*, bis Bezug gesichert ist (Dynamic Final Design). Baubehörden/Ästhetik-Kommissionen sind darauf nicht eingestellt. | Superuse (BlueCity: Welstand lehnte ab, weil finaler Entwurf vor Baustart unbekannt war); in situ K.118 |
| **C2** | **Maß- & Toleranz-Unsicherheit** | Fundmaße stehen erst spät fest; Raster/Anschlüsse müssen „atmen". | in situ-Prinzipien *„Puffer"* & *„Überlappen"*; Kamikatsu (jedes Fenster einzeln vermessen) |
| **C3** | **Nachweis-/Statik-Lücke** | Für Gebraucht­bauteile fehlen Daten (Güte, Ermüdung, Statik) → Genehmigungs-/Versicherungs­risiko. | Recyclinghaus (Stahl-Rohbau verworfen, Güte fehlte → Ausweichen auf leimfreies Holz); 55 GSS (gelöst via SCI P427); ReCreate (Produktzulassung) |
| **C4** | **Transformationskapazität der Fügung** | Reversibel fügen (schrauben/klemmen/stecken) statt kleben/schweißen/vergießen; es zählt das **schwächste Glied**. | People's Pavilion (0 Schrauben/Kleber → Spanngurte); Recyclinghaus (Buchendübel, leimfrei) |
| **C5** | **Zustand & Schadstoffe** | Alter/Belastung je Charge prüfen; Aufbereitung entwerfen (reinigen, neu beschichten, nachschneiden). | Mööslistrasse (Stahl gecuttet/neu verplattet/beschichtet); Consolis Parma (Werk-Aufbereitung) |
| **C6** | **Brandschutz & Bauphysik** | F90/Akustik/Wärme mit Gebraucht­teilen belegen, ohne Materialreinheit zu opfern. | CRCLR (F90 *ohne* Kapselung → abbrennende Holzkonstruktion); Green House (perforiertes Stahlblech für Akustik) |
| **C7** | **Ästhetik** | *„Abfall darf nicht wie Abfall aussehen"* — bewusst gestalten: Patchwork ausdrücken **oder** Reuse unsichtbar machen. | Kamikatsu (Fenster-Patchwork als Signatur); Europa (Eichenfassade als Symbol); in situ (Reuse unsichtbar möglich) |
| **C8** | **Logistik/Timing im Entwurf** | Rückbaufenster ↔ Bauzeit, Zwischenlager, Reihenfolge — der Entwurf muss die **Beschaffungszeit** mitplanen. | Zirkular („Bauteiljagd": oft nur Tage bis Entscheid + Ausbau + Lagerung); Thoravej (in-situ = kein Lager nötig) |
| **C9** | **Design ≠ Skalierbarkeit** | Perfekte Fügung nutzt nichts, wenn Modell temporär/geliehen/einzelfund­abhängig ist → **Methode als Produkt**. | People's Pavilion (Design 100, aber temporär → #2); Villa Welpeloo (Harvest-Map als eigentlicher Beitrag) |

> **Roter Faden.** C1–C2 sind *Prozess*-Herausforderungen, C3–C6 *technische*, C7 *gestalterische*,
> C8 *organisatorische*, C9 *strategische*. Ein gutes Reuse-Design adressiert **alle neun bewusst**.

---

## Teil B — Der Design-Workflow (D0–D7, werkzeuggestützt)

Der Ablauf kehrt die konventionelle Reihenfolge um: **Beschaffung und Bewertung laufen dem Entwurf
voraus bzw. parallel**, und der Entwurf bleibt *dynamisch* bis zur gesicherten Beschaffung.

```
D0 Ambition/Ziel ─► D1 Bestands-/Pre-Demolition-Audit ─► D2 Harvest Map + dyn. Stückliste
      ▲                                                              │
      │                                                              ▼
D7 Rückbaukonzept ◄─ D6 LCA/Wirkung ◄─ D5 Nachweis/Materialpass ◄─ D4 TC-Design ◄─ D3 Dynamic Final Design
```

| Schritt | Was passiert (Design-Sicht) | Werkzeuge | Rolle | Vorbild |
|---|---|---|---|---|
| **D0 Ambition** | Reuse-Ziel + Hybridquote festlegen; Reuse als eigenes *Gewerk* verankern | Zielvereinbarung, Förderkriterien | Bauherr + Architekt | KA13 (FutureBuilt-Kriterien) |
| **D1 Bestands-/Pre-Demolition-Audit** | Verfügbare Bauteile *vor* dem Entwurf erfassen (Menge, Maß, Zustand, Schadstoffe) | DIN SPEC 91484, Bauteilerfassung, Fotos/Scan | Bauteiljäger:in / Urban Miner | in situ *Bauteilerfassung*; Rotor |
| **D2 Harvest Map + dyn. Stückliste** | Fundmaterial verorten & in Bauteilgruppen zerlegen; Entscheidungsbaum (CO₂) | **Harvest Map/Oogstkaart**, **Concular/Restado/Madaster-Marktplatz** | Reuse-Berater | Superuse *Dynamic Final Design* |
| **D3 Dynamic Final Design** | Entwurf offen halten: *Puffer* + *Überlappen*; Raster tolerant; Entwurf bis Kauf änderbar | Rhino/Grasshopper (parametrisch), BIM | Architekt (Harvest-Design) | in situ; Superuse |
| **D4 Transformationskapazitäts-Design** | Fügung & Schichten so entwerfen, dass die *nächste* Runde möglich bleibt | **Phoenix3D** (Tragwerk aus Stock), **DGBC-Detachability** (4 Kriterien), One Click LCA Circularity | Architekt + Tragwerk | People's Pavilion; K.118; Re:Crete |
| **D5 Nachweis/Materialpass** | Herkunft, Zustandsklasse, Prüf-/Konformitätsstatus je Charge dokumentieren | **Madaster**/**Concular** Materialpass, SCI P427, ISO 20887 | Reuse-Berater + Prüfer | 55 GSS; Recyclinghaus (Gegenbeispiel) |
| **D6 LCA/Wirkung** | A1–A5 GWP + Reuse-Gutschrift (Modul D) gegen Neubau-Benchmark | **One Click LCA**, EPD, Level(s) 1.2 | Forschungs-/LCA-Partner | K.118 (ZHAW); Thoravej (DTU) |
| **D7 Rückbaukonzept** | Demontagereihenfolge, Werkzeug, Wiederverwendbarkeit als Teil des Entwurfs mitliefern | DfD-Checkliste, Rückbau-Playbook | Architekt | Green House; CRCLR |

**Zwei Design-Muster machen D3 überhaupt möglich** (baubüro in situ, K. Müller):
- **Puffer:** Für ein fixes Fundelement (z. B. Fenster) mit noch unbekanntem Maß eine **anpassungsfähige
  Umgebung** (Wand) entwerfen, die Toleranz aufnimmt.
- **Überlappen:** Bauteile überlappen lassen, damit Maßabweichungen aufgefangen werden.
- Zusatzregel: **Ein Bauteil nicht mit zu vielen Funktionen überladen** (erhält Austauschbarkeit).

---

## Teil C — Der Werkzeugkasten (Tools)

### C.1 Beschaffung & Harvest Mapping
| Werkzeug | Was es tut | Einsatzphase | Beleg |
|---|---|---|---|
| **Harvest Map / Oogstkaart** | Grafische Verortung von Rest-/Fundmaterial + Quellen; „Shopping-Liste" für den Bauunternehmer | D1–D2 | Superuse (2012 gegründet, 2019 an New Horizon) |
| **Concular / Restado** (DE) | Bauteilbörse + Doku + Restwert/Disassembly-Potential | D2, D5 | DE-Marktinfrastruktur |
| **Madaster-Marktplatz** | Register + Track-&-Trace + Materialpass | D2, D5 | NL/DE/CH |
| **Bauteilbörsen/Depots** | regionale Zwischenlager, Vermittlung | D2, D8 | Zirkular; Rotor DC; bauteilclick |

### C.2 Computational / parametrisches Entwerfen aus Lager
| Werkzeug | Was es tut | Einsatzphase | Beleg |
|---|---|---|---|
| **Phoenix3D** (EPFL SXL) | **Open-Source Rhino+Grasshopper-Plugin**: weist einen *Bestand* reversibel verfügbarer Elemente optimal einer Tragstruktur zu. MILP (globales Optimum) + Best-Fit-Heuristik (Echtzeit). Bis **60 % weniger Umweltwirkung** vs. Neu-Minimalgewicht | D4 | Warmuth/Brütting/Fivet 2021; >600 Downloads, Praxis + Lehre |
| **Rhino + Grasshopper** | parametrische Basis; Toleranz-/Variantenstudien; Verknüpfung mit Stock-Daten | D3–D4 | Standard in Reuse-Studios |
| **BIM (Revit/Archicad/Bentley)** | Bauteil-Datenmodell; Anbindung an Madaster (Detachability, Materialpass) | D3–D5 | Circl (Digital Twin); Madaster-BIM-Integration |

### C.3 Design-for-Disassembly-Bewertung
| Werkzeug/Methode | Was es tut | Einsatzphase | Beleg |
|---|---|---|---|
| **DGBC-Detachability-Methode** | Score aus **4 Faktoren**: *Verbindungstyp · Zugänglichkeit der Fügung · Durchdringungen (cross-linkages) · Bauteilkanten-Abschluss*; je Bauteil → 1 Score | D4 | DGBC/Alba Concepts; von Madaster validiert |
| **Madaster Detachability** | automatisiert die DGBC-Methode über BIM; BREEAM-tauglich | D4–D5 | DGBC-anerkannt |
| **One Click LCA — Building Circularity** | DfD-/Adaptivitäts-Scoring, dismountable fasteners vs. Kleber; London-Plan Circular-Economy-Statement | D4, D6 | BREEAM/HQE/London Plan |
| **Reversible Building Index / BAMB** | Transformationskapazität = Independence × Exchangeability | D4 | Durmisevic/BAMB |

### C.4 Nachweis, Norm & Wirkung
| Werkzeug/Norm | Was es tut | Einsatzphase | Beleg |
|---|---|---|---|
| **SCI P427** (UK) | Prüf-/Rezertifizierungs­protokoll für tragenden Reuse-Stahl → CE/UKCA (EN 1090) | D5 | 55 GSS (praktisch gelöst) |
| **DIN SPEC 91484/91525** (DE) | Pre-Deconstruction-Audit + Bauteil-Weitergabe | D1, D5 | DE-Förderkontext |
| **ISO 20887:2020** | Prinzipien DfD/Adaptabilität (Zugänglichkeit, Unabhängigkeit, Einfachheit, Standardisierung) | D4, D7 | Rahmenwerk |
| **Madaster/Concular Materialpass** | maschinenlesbare Bauteil-Provenienz + Restwert | D5 | Circl; CRCLR |
| **One Click LCA / EPD** | A1–A5-GWP + Modul-D-Gutschrift | D6 | KA13, K.118 |

### C.5 Methoden-Artefakte (der eigentliche Transferwert)
Dynamic Final Design (Superuse) · Bauteiljagd-Playbook (Zirkular) · REPAR-Katalog (Bellastock) ·
DGBC-Checkliste · Rückbau-Playbook · Musterverträge fürs Leihen (People's Pavilion) ·
„CCTP à trous"/Lot 01 (Grande Halle, Vergabe). → siehe Muster **P4** in
[`AKTEURE_KETTEN_UND_LERNMUSTER.md`](AKTEURE_KETTEN_UND_LERNMUSTER.md).

---

## Teil D — Die zehn Design-Ansätze (Muster)

| Muster | Prinzip | Am reinsten bei |
|---|---|---|
| **1 Form follows availability** | Lager zuerst, Form danach | Villa Welpeloo, K.118, TRÆ |
| **2 Puffer & Überlappen** | Toleranz baulich vorhalten für unbekannte Fundmaße | baubüro in situ (alle) |
| **3 Ein Bauteil — wenige Funktionen** | Entkopplung erhält Austauschbarkeit | in situ; DGBC-Logik |
| **4 Schichtentrennung (Brand)** | Site/Structure/Skin/Services/Space/Stuff unabhängig, je eigene Lebensdauer | K.118; CRCLR; Circl |
| **5 Reversible Fügung / schwächstes Glied** | schrauben/klemmen/stecken statt kleben/schweißen | People's Pavilion; Recyclinghaus |
| **6 Zero-damage / geliehen** | kein Eingriff ins Fundteil; Product-as-Service | People's Pavilion; Green House (Leasing) |
| **7 Gebäude als Materialbank (in situ)** | das Bestandsgebäude verwertet sich selbst | Thoravej 29 |
| **8 Panelisierung nicht-trennbaren Materials** | untrennbares (Zement-Mörtel-Ziegel) in neue Module überführen | Resource Rows |
| **9 Kit-of-parts / Trockenbau** | vorgefertigt, trocken gefügt, demontierbar | Green House; Ferme du Rail; Résilience |
| **10 Stock-constrained computational design** | Algorithmus weist Bestand optimal der Struktur zu | Re:Crete / EPFL-Ansatz (Phoenix3D) |

**Ästhetik-Strategie (C7) als eigene Design-Entscheidung.** Zwei legitime Pole:
*ausdrücken* (Kamikatsu-Patchwork, Europa-Eichenhaut, TRÆ-Alu-„Birkenrinde", Thoravej-Treppen aus
TT-Platten) **oder** *unsichtbar machen* (in situ: „man kann Wiederverwertung auch unsichtbar machen").
Beide sind gültig — nur **unbewusst** darf die Entscheidung nicht sein.

---

## Teil E — Design-Steckbriefe je Projekt

Format: **Design-Score** (0–100, Durmisevic/DGBC/Brand-Anker) · **Herausforderung** ·
**Design-Antwort/Ansatz** · **Werkzeuge/Methoden** · **Übertragbare Lehre**.

### People's Pavilion, Eindhoven — Design 100 (DfD-Referenz)
- **Herausforderung:** C4/C9 — maximale Reversibilität für ein *temporäres* Gebäude (100 % geliehen).
- **Ansatz:** **Zero-damage**-Fügung — kein Schrauben/Kleben/Sägen/Bohren; Stahlbänder + Spanngurte
  halten alles; Originalmaße bleiben unversehrt; nach 9 Tagen unbeschädigt zurückgegeben.
- **Werkzeuge:** Musterverträge fürs Leihen; „Materialchoreografie"; Pretty-Plastic-Fassadenschindeln.
- **Lehre:** Die **Design-Referenz für Independence + Exchangeability** — aber Muster 6 (geliehen)
  begrenzt Skalierung → Methode dokumentieren (C9).

### The Green House, Utrecht — Design 90 (System-Pilot, Geschäftsmodell)
- **Herausforderung:** C6/C9 — demontierbar *und* wirtschaftlich (15 J + 1 Tag).
- **Ansatz:** **Kit-of-parts** (verzinkter, verschraubter Stahl; sogar lösbare Fertigteil-Fundamente);
  Tragraster **nach dem Maß der geernteten Rauchglaspaneele** dimensioniert (C2 elegant gelöst);
  Teile unabhängig wiederverwendbar/recycelbar. Perforiertes Stahlblech für Akustik.
- **Werkzeuge:** Leasing/Rückkauf-Business-Case; Materialleasing; cepezed-Detaillierung.
- **Lehre:** Muster 6+9 — **Demontierbarkeit bepreisen** macht Design wirtschaftlich (→ Leitlinie L10).

### Recyclinghaus Hannover — Design 88 (System-Pilot)
- **Herausforderung:** C3 — für den Gebraucht-Stahl-Rohbau fehlten **Materialgüte-Daten** → verworfen.
- **Ansatz:** Ausweichen auf **leimfreie, typenreine Holzkonstruktion** (Buchendübel), vollständig
  zerstörungsfrei demontierbar; ~90 % Fassade wiederverwendet; alle Fenster/Türen reused.
- **Werkzeuge:** Gundlach-Bestand (~4000 Whg.) als Quelle; Lindner-Aufbereitung.
- **Lehre:** Die Nachweislücke (C3) kann den Entwurf **umlenken** — leimfrei = zukunftssicher (Muster 5).

### K.118 Kopfbau Halle 118, Winterthur — Design 85 (System-Pilot)
- **Herausforderung:** C1/C2 — Entwurf aus Materialkatalog statt Materialkatalog aus Entwurf.
- **Ansatz:** **Geschichtete, entkoppelte** Bauweise (Brand); sichtbar/zugänglich demontierbar;
  Stahltragwerk aus Teilrückbau ELYS Basel; *Puffer/Überlappen* für Fundmaße.
- **Werkzeuge:** Materialkatalog zuerst; ZHAW-LCA; Buch *Bauteile wiederverwenden*.
- **Lehre:** **Muster 1+2+4** in Reinform; „Data is usually not readily available" (Müller).

### Circl / ABN AMRO, Amsterdam — Design 85 (Aggregator)
- **Herausforderung:** C3/C7 — viele heterogene Fundquellen zu einem hochwertigen Bild fügen.
- **Ansatz:** **leimfrei geschraubt/geklickt**; Larix-Skelett bewusst **überdimensioniert**, damit
  Träger später zu Standardbrettern re-cut werden können; Aufzüge/Licht geleast; **voller Digital Twin**.
- **Werkzeuge:** Digital Twin/Materialregister; New Horizon (Urban Mining); Materia-Beratung.
- **Lehre:** **Design für die übernächste** Runde (re-cut-Reserve) — antizipierte Austauschbarkeit.

### CRCLR House, Berlin — Design 80 / Fit-out 78 (System-Pilot)
- **Herausforderung:** C6 — F90-Brandschutz *ohne* Materialverunreinigung (Kapselung).
- **Ansatz:** **reversible Verbinder**, in Schichten geplant; **abbrennende** Holzkonstruktion (F90 ohne
  Kapselung); eigene Stahlpfetten der Halle → tragende Treppenwangen; Fit-out ~70 % Reuse, DIY-gebaut.
- **Werkzeuge:** **Materialpässe**; baubüro-in-situ-Beratung (CH→DE-Transfer); ZRS-Tragwerk.
- **Lehre:** Brandschutz (C6) lösbar **ohne** Design-Kompromiss; Materialpass als Standard.

### Thoravej 29, Kopenhagen — Design 78 (Großmaßstab)
- **Herausforderung:** C8 — Reuse ohne Zwischenlager/Logistik.
- **Ansatz:** **Gebäude als Materialbank** (Muster 7): TT-Platten geschnitten & gekippt → Treppen,
  Ziegel → Pflaster, Türen → Tischplatten; „preserve first, reuse next, recycle when it adds value".
- **Werkzeuge:** **Originalstatik der TT-Platten-Hersteller** (löst C3!); DTU-LCA; Drittprüfer.
- **Lehre:** In-situ-Reuse umgeht Logistik/Nachweis-Barrieren — aber Zukunfts-Demontierbarkeit moderat.

### KA13, Oslo — Design 72 (Aggregator, RSI #1)
- **Herausforderung:** C2/C5 — 25+ Quellen mit unterschiedlichen Maßen/Zuständen integrieren.
- **Ansatz:** Ziegel in **Kalkmörtel** (einzeln lösbar); demontierbare Erweiterungs-Einheiten; viel
  In-situ-Integration (begrenzt die spätere Trennbarkeit).
- **Werkzeuge:** Resirqel-Ombrukskartierung; *Erfaringsrapport* (Bauteil für Bauteil).
- **Lehre:** Bezug-Exzellenz + solides (nicht maximales) Design = **skalierbarster Gesamtfall**.

### TRÆ High-Rise, Aarhus — Design 70 (Großmaßstab)
- **Herausforderung:** C2/C7 — Reuse an einem Hochhaus sichtbar & wirtschaftlich.
- **Ansatz:** **Massivholz-Stützen + CLT-Decken** (demontierbar), Beton nur im Kern; zwei Ökosysteme
  (zirkulär + biogen); Alt-Alu-Fassade („Birkenrinde"), reused Fenster, Windradflügel als Verschattung.
- **Werkzeuge:** a:gain Viddø-Fenster (mit EPD/Rücknahme); Lendager-LCA.
- **Lehre:** Trockene Holz-Hybride heben Reuse in den **Großmaßstab** (Muster 9).

### 55 Great Suffolk Street, London — Design 70 (System-Pilot)
- **Herausforderung:** C3 — tragenden Reuse-Stahl **normkonform** nachweisen.
- **Ansatz:** **verschraubter externer Stahlkern**; bestehende Geschossdecken bleiben ungestört
  (Schicht-Unabhängigkeit); 97 % des neuen Kernstahls reclaimed.
- **Werkzeuge:** **SCI-Protokoll P427** → Labortest → CE/EN 1090; Cleveland-Steel-Stockholder.
- **Lehre:** Das **gelöste Nachweismuster** für tragenden Stahl — Blaupause (C3).

### Kindergarten Mööslistrasse, Zürich — Design 70 (Aggregator)
- **Herausforderung:** C5 — Fundstahl zustandsgerecht aufbereiten & wieder einbaufähig machen.
- **Ansatz:** Stahl **gecuttet / neu verplattet / neu beschichtet & verschraubt**; Bauteile bewusst
  nach Reversibilität gewählt; „Bauteiljagd" (Brandtüren, WCs, Träger).
- **Werkzeuge:** Zirkular-Bauteiljagd; Stadt-Zürich-Gebrauchtmobiliar.
- **Lehre:** **Aufbereitung ist Entwurf** (C5) — Bearbeitungsschritte gehören in den Materialpass.

### Ferme du Rail, Paris — Design 70 (System-Pilot)
- **Herausforderung:** C2 — Trockenbau mit gemischten bio-/Reuse-Elementen.
- **Ansatz:** **Filière sèche** — vorgefertigter Holzrahmen + Stroh-Kassetten (hohe Adaptivität/
  Trennbarkeit); diskrete Reuse-Elemente (Fenster, Pflaster, Fliesen, Granit).
- **Werkzeuge:** Vaninetti-Vorfertigung; Bellastock/REPAR-nahe Beschaffung.
- **Lehre:** Muster 9; **Vorsicht Datenklarheit** — „90 %" war biosourced+Reuse, reiner Reuse ~15 %.

### Kamikatsu Zero Waste Center — Design 68 (Aggregator)
- **Herausforderung:** C2/C7 — ~700 Einwohner-Fenster unterschiedlichster Maße fügen.
- **Ansatz:** jedes Fenster **vermessen/positioniert per Software** → präzises Patchwork-Bild;
  rohe Zedernstämme, **verschraubte, demontierbare Fachwerke**; Reuse als Community-Signatur.
- **Werkzeuge:** Software-gestützte Fenster-Platzierung; Yamada-Noriaki-Tragwerk.
- **Lehre:** Software löst C2 (Maß-Chaos) **und** erzeugt die Ästhetik (C7); Community als Quelle.

### Résilience / La Ferme des Possibles, Stains — Design 65 (Aggregator)
- **Herausforderung:** C2 — diffuse Quellen (Bellastock, leboncoin, Mairie de Paris).
- **Ansatz:** Trockenbau-Holzrahmen (Glulam + CLT), Stroh+Lehm-Ausfachung; diskrete Reuse.
- **Werkzeuge:** Bellastock + Métabolisme Urbain + Réavie; SOCOTEC-Kontrolle.
- **Lehre:** Aggregator-Bezug + Trockenbau (Muster 9), Reuse-Tiefe aber gering.

### Villa Welpeloo, Enschede — Design 62 (Superuse)
- **Herausforderung:** C1 — der Ur-Fall des umgekehrten Entwurfs.
- **Ansatz:** **verschraubter Altstahl** aus *einer* Textilmaschine; Fassade aus Kabeltrommeln;
  „Dynamic Final Design" = Zeichnung + Harvest-Map + dynamische Stückliste.
- **Werkzeuge:** **Harvest Map / Oogstkaart** (der eigentliche Beitrag); Buch *Superuse*.
- **Lehre:** **Muster 1**; die *Methode* (Harvest Map) skaliert, nicht das Haus (C9).

### Härmälänranta / ReCreate, Tampere — Design 60 (Konsortium)
- **Herausforderung:** C3 — tragender Vorfertigbeton, **nicht** für Demontage entworfen.
- **Ansatz:** Hohldecken ganz ausgebaut, **im Werk aufbereitet + QC + Produktzulassung**; neuer Rahmen
  vollständig vorgefertigt → Zukunfts-Reuse-Potenzial; Montage „wie mit Neuteilen".
- **Werkzeuge:** Ramboll-Zustands-/Tragwerksanalyse; Consolis-Parma-Werk; EU-Horizon-Konsortium.
- **Lehre:** **Value-chain-Konsortium** löst C3 kollektiv (→ Leitlinie L11).

### Resource Rows, Kopenhagen — Design 55 (Großmaßstab)
- **Herausforderung:** C4 — Zement-Mörtel-Ziegel sind **einzeln nicht trennbar** (Mörtel härter als Ziegel).
- **Ansatz:** **Panelisierung** (Muster 8): 1×1-m-Ziegelmodule herausgesägt, an Vorfertigbeton/Holzrahmen;
  Patchwork-Ästhetik als Ausdruck (C7).
- **Werkzeuge:** Lendager UP (Materialsparte); LCA (29 % CO₂ Gebäudeebene).
- **Lehre:** Wenn Trennbarkeit fehlt (C4), ist **Panelisierung** der pragmatische Design-Weg — aber
  die neue Fügung ist selbst nicht reversibel (niedrige TC).

### Upcycle Studios, Kopenhagen — Design 55
- **Herausforderung:** C4 — Recycling (Betonzuschlag) vs. echter Element-Reuse.
- **Ansatz:** Recyclingbeton **in situ gegossen** (nicht demontierbar) + 75 % reused Fenster + Holzverschnitt;
  DfD-Prinzipien beansprucht.
- **Werkzeuge:** Lendager; Metro-Betonabfall als Zuschlag.
- **Lehre:** **Recycling ist nicht Reuse** — gegossener Zuschlag entwertet die Transformationskapazität.

### Grande Halle de Colombelles — Design 55 (Aggregator, Vergabe-Innovation)
- **Herausforderung:** C1/C8 — Reuse im öffentlichen ERP-Bau planbar machen.
- **Ansatz:** Betonstruktur **erhalten**; reversibler Innenausbau; Innovation liegt in der **Beschaffung**
  (Lot 01 + „CCTP à trous"), nicht im DfD.
- **Werkzeuge:** Le WIP (Reuse-Los); CCTP à trous (Varianten-LV).
- **Lehre:** Nicht jedes Reuse-Vorbild ist ein *Design*-Vorbild — hier skaliert das **Vergabe-Instrument** (L9).

### Europa Building, Brüssel — Design 55 (Aggregator, Legitimation)
- **Herausforderung:** C7 — 3 750 Eichenfenster aus allen EU-Staaten zu einem Bild fügen.
- **Ansatz:** abgeschliffen/restauriert/lackiert, in **Edelstahlrahmen** montiert (mechanisch fixiert);
  dekorative Doppelfassaden-Haut; 30 % weniger Stahl als Standardfassade.
- **Werkzeuge:** Samyn-Detaillierung; Jan-De-Nul-Ausführung.
- **Lehre:** **Große Aggregation ≠ hohe Transformationskapazität** — die Haut ist dekorativ, nicht systemisch.

### Einschlägige Graph-Fälle (nicht verifiziert, aber design-relevant)
- **Re:Crete Footbridge (CH, EPFL) — Design 74:** Fußgängerbrücke aus **wiederverwendeten
  Betonsäge-Blöcken** — direkte Anwendung des **stock-constrained** Ansatzes (Muster 10, Phoenix3D-Umfeld).
- **Juch-Areal Recyclingzentrum, Zürich — Design 90 (graph-gekappt):** breite reversible/vorgefertigte
  Signale; Demontage-Bauweise als Methode.
- **Lokomotion Technology Centre (FI) — Design 89:** hohe Reversibilitäts-/Vorfertigungssignale.

---

## Teil F — Design-Reifegrad & Empfehlung

**Design-Reifegrad-Leiter (an Transformationskapazität orientiert):**
1. **Reuse in situ ohne DfD** (Thoravej, Grande Halle) — Reuse hoch, Zukunfts-Demontierbarkeit gering.
2. **Panelisierung/Aufbereitung** (Resource Rows, Mööslistrasse) — pragmatisch, neue Fügung oft irreversibel.
3. **Reversible Fügung + Schichtentrennung** (K.118, Recyclinghaus, CRCLR, Circl) — der **skalierbare Standard**.
4. **Kit-of-parts / Trockenbau** (Green House, TRÆ, Ferme du Rail) — vorgefertigt, demontierbar, großmaßstabsfähig.
5. **Zero-damage / stock-constrained** (People's Pavilion; Re:Crete/Phoenix3D) — Design-Spitze; nur mit
   dokumentierter Methode skalierbar (C9).

**Empfehlung für das Vorhaben.**
1. **Prozess umkehren (C1):** Bestands-/Pre-Demolition-Audit *vor* dem Entwurf; Entwurf als
   **Dynamic Final Design** offen halten; Baubehörde früh über den offenen Prozess informieren.
2. **Toleranz einbauen (C2):** **Puffer + Überlappen** als Entwurfsstandard; Raster tolerant.
3. **Reversibel fügen (C4):** DGBC-4-Kriterien je Verbindung prüfen; schwächstes Glied vermeiden.
4. **Werkzeuge setzen:** **Harvest Map/Concular** (Beschaffung), **Phoenix3D** (tragende Struktur aus
   Lager), **Madaster/Concular-Materialpass + One Click LCA** (Nachweis/Wirkung), **DGBC-Detachability**
   (Design-Score) — alle in D2–D6 verankert.
5. **Nachweis absichern (C3):** für tragende Teile **SCI-P427-Muster** bzw. **Werk-Veredler-Konsortium**
   (ReCreate) einplanen; **DIN SPEC 91484/91525** für den DE-Kontext.
6. **Methode als Produkt (C9):** Harvest-Map, DGBC-Checkliste und Rückbau-Playbook als übertragbare
   Ergebnisse mitliefern — sie sind der eigentliche Skalierungswert.

---

## Quellen (Auswahl)

- **Stock-constrained / computational design:** EPFL SXL *Optimum Reuse* & **Phoenix3D**
  (Warmuth, Brütting, Fivet, 2021; food4rhino/GitHub); Brütting/Senatore/Fivet, *Design of Truss
  Structures Through Reuse*, Structures (2019) 10.1016/j.istruc.2018.11.006.
- **DfD-Tools & Materialpass:** DGBC/Alba-Concepts Detachability-Methode (4 Kriterien);
  Madaster (DGBC-validiert, BIM-Integration); One Click LCA Building Circularity; Concular/Restado.
- **Studio-Methoden:** baubüro in situ / Zirkular (wbw.ch, Interview K. Müller: „Puffer"/„Überlappen";
  Holcim Foundation *Designing from end to beginning*); Superuse *Harvest! Collect! Re-use!* &
  *Dynamic Final Design* (superuse-studios.com; Oogstkaart→New Horizon); Rotor (tlmagazine).
- **Design-Prozess-Barrieren:** conceptfollowscircularity.nl (BlueCity/Welstand; „legal codes don't fit").
- **Normen:** ISO 20887:2020; SCI P427 (UK); DIN SPEC 91484/91525 (DE).
- **Projekt-Design-Belege:** je Projekt in [`verified_enrichment.json`](verified_enrichment.json),
  Feld `design_note` + `sources`.
