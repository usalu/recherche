# Was fällt weg / was wird umgeschrieben

**Datum:** 2026-08-06
Antwort auf die Nutzerfrage: „wenn es im Neuen etwas Ähnliches gibt, umschreiben — sag mir, was wegfällt."

---

## A. Hart gelöscht (verschwindet aus dem Live-Graph)

| Objekt | Menge | Verlust? |
|---|---|---|
| Flache `:Huerde`-Knoten | 11 | **Nein** — erst werden alle Kanten umgehängt, dann die leeren Knoten gelöscht. |
| `category`-String-Property (8 engl. Werte: `social_perception`, `logistics_storage`, `technical_quality`, `market_supply`, `economic_labour`, `procurement_regulatory`, `planning_organisational`, `organisational_timing`) | 11 | **Nein, ersetzt** — die Kategorisierung wird durch die A–H-Bereichshierarchie abgelöst (feiner + auf Deutsch). Die englischen Strings selbst werden verworfen. |
| Rel-Typ `HAT_HUERDEKATEGORIE` | 0 Instanzen | **Nein** — reiner Schema-Müll (genau das, was der `schema-cleanup`-Branch aufräumt). |
| `source_titles`/`source_urls` = „Rakhshan 2020" auf den 11 | 11 | **Nein** — Rakhshan bleibt als Beleg an den passenden neuen Knoten; zusätzlich kommen Thirumal 2024, Nordic 2023, buildingSMART D2R, Swiss-Inv, EU CPR/DPP dazu. |

**Keine Kollateralschäden:** Nur `:Projekt` (93) und `:Bauteilgruppe` (144) zeigen via `HAT_HUERDE` auf Hürden. Beide werden umgehängt — **0 Kanten gehen verloren.**

---

## B. Die 11 → Umschreibung (welcher neue Knoten übernimmt die Kanten)

Wichtig: die alten 11 sind **grob**, die neue Taxonomie ist **fein**. Wo die alte Bedeutung eindeutig ein Blatt trifft, hängen wir auf das **Blatt** um. Wo die alte Hürde mehrere Blätter überspannt, hängen wir bewusst auf die **Familie/Gruppe** (Ebene 3–4) um — sonst würden wir eine Präzision erfinden, die die Alt-Evidenz nicht hergibt.

| # | Alt-Hürde (Kanten) | → Neuer Anker | Ebene | Güte |
|---|---|---|---|---|
| 1 | Witterung_Feuchte (39) | `H5.3` Ungeeignete_Lagerbedingungen | Blatt | ✅ eindeutig |
| 2 | Fehlende_Lagerflaeche (14) | `H5.1` Keine_Lagerkapazitaet | Blatt | ✅ eindeutig |
| 3 | Mengenunsicherheit (29) | `G1.5` Menge_nicht_bestaetigt | Blatt | ✅ eindeutig |
| 4 | Heterogenitaet_Chargen (25) | `E5.6` Inkonsistente_Produktqualitaet | Blatt | ✅ eindeutig |
| 5 | Aufbereitungsaufwand (22) | `H4` Pruef_und_Aufbereitungskapazitaet | Familie | ⚠️ alt=Aufwand, neu=Kapazität — kein exaktes Aufwand-Blatt |
| 6 | Verfuegbarkeitsproblem (34) | `G4` Verfuegbarkeitsunsicherheit | Familie | ⚠️ überspannt auch `E5.2` Unregelmaessiges_Angebot |
| 7 | Terminunsicherheit (16) | `G5` Zeitliche_Diskrepanz | Familie | ⚠️ mehrere Blätter (G5.1–G5.5) |
| 8 | Entwurfsbindung (28) | `H7.1` Entwurfsanpassungsbedarf | Blatt | ⚠️ Doppel mit `G2.6` Entwurfsflexibilitaet_nicht_abgebildet |
| 9 | Unkonventionelles_Material (17) | `F6.5` Unsichere_Kompatibilitaet_mit_neuer_Nutzung | Blatt | ⚠️ Doppel mit `H1.6` Nichtstandardisierte_Fuegungen |
| 10 | Ausschreibungsproblem (5) | `E3.6` Keine_Wiederverwendungs_Beschaffungspflicht | Blatt | ⚠️ ungenau — kein eigenes „öff. Vergabe inkompatibel"-Blatt |
| 11 | Akzeptanzproblem (8) | `D6` Adoptionswiderstand | Familie | ⚠️ überspannt D6.1–D6.4 |

**6 saubere Blatt-Treffer, 5 unscharfe** (⚠️). Bei den 5 unscharfen bitte den Primäranker bestätigen bzw. das Doppel-Ziel wählen — das ist der eigentliche „was fällt weg"-Punkt: bei diesen 5 verlieren wir beim Umhängen entweder etwas Feinheit (Familie statt Blatt) oder wir treffen eine Ja/Nein-Entscheidung zwischen zwei plausiblen Blättern.

> Regel: **eine** Alt-Kante → **ein** neuer Anker. Wir fächern nicht 1→n auf (das würde Evidenz erfinden). Sekundärziele werden dokumentiert, aber nicht automatisch verkantet.

---

## C. Was hinzukommt (kein Wegfall, aber zur Erwartung)

Bei „volle 4-Ebenen-Taxonomie" entstehen **~390 neue Knoten**, davon der gesamte digitale Block **A/B/C** (Information, Interoperabilität, Governance) — bislang **komplett unbelegt** durch Projekte/Bauteilgruppen. Das ist gewollt (Referenzbaum für die Plattform-Forschung / Bauteilportal), heißt aber: direkt nach der Migration haben nur die ~11 Anker aus Abschnitt B echte Projekt-/BG-Evidenz; die restlichen ~380 sind zunächst reine Taxonomie ohne Fallbelege.
