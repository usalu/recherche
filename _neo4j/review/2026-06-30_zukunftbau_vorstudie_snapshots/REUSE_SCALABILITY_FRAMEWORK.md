# Reuse-Scalability Index — Methodik

> **Kanonisch: RSI v6** (Gates G1–G6, Kriterien K1–K14). Vollständige Systemfassung:
> [`SKALIERBARKEITSKRITERIEN_RSI_v6.md`](SKALIERBARKEITSKRITERIEN_RSI_v6.md)

**Stand:** 2026-07-01  
**Engine:** `_score_scalability_v6.py` · Anreicherung: `verified_enrichment.json` (21 verifiziert, v6-Felder) · Ergebnisse: `project_scalability_scores_v6.json` / `.csv`, `_scal_table_v6.md`

---

## RSI v6 — Kurzüberblick

| Baustein | Inhalt |
|---|---|
| **Gates G1–G6** | Mindestbedingungen vor Score (Planung, Inventar, Qualität, Haftung, Logistik, Beschaffung) |
| **K1–K14** | Gewichtete Skalierungskriterien (Rohscore 0–4, normiert × 25) |
| **RSI brutto / final** | Gewichteter Mittelwert; final nach Gate-Kappung (59 / 39) |
| **Konfidenz A/B/C** | Evidenzqualität pro Kriterium |
| **Archetypen** | 10 Skalierungslogiken (Aggregator, Hub, Struktur-ReUse, …) |

**Merksatz:** Skalierbarkeit = wiederholbare Kette aus Quelle, Inventar, Nachweis, Risiko, Logistik, Beschaffung, Design, Kosten, Kompetenz, Nachfrage.

---

## Migration von v3

RSI v3 (6 Dimensionen: Bezug, Tiefe, Maßstab, Design, Reife, Wirkung) wurde für den Korpus 83/21 angewendet. v3-Scores in `project_scalability_scores.json` bleiben als **historische Referenz**.

**Nicht direkt vergleichbar** mit v6 (v6 §16.3). Proxy-Mapping in `_score_scalability_v6.py` leitet v6-Kriterien für nicht verifizierte Projekte aus v3-Dimensionen ab.

Historische v3-Dokumentation: [`SKALIERBARKEITSKRITERIEN_RSI_v3.md`](SKALIERBARKEITSKRITERIEN_RSI_v3.md) · Engine: `_score_scalability_v3.py`

---

## Wissenschaftliche Verankerung (Auswahl)

**Design / DfD:** Durmisevic; DGBC/Alba-Concepts Disassembly Potential; Brand Shearing Layers; ISO 20887; Brütting/Fivet/Senatore (*form follows availability*).

**Zirkularität:** EMF MCI; EU Level(s); Küpfer/Brütting/Fivet MCDA; Reuse Viability Index; BCR-Feasibility.

**Skalierung:** Geels Multi-Level-Perspective; Reuse Market Dynamics (2024); Chalmers upscaling reuse (2024).

Details und Scoring-Regeln: [`SKALIERBARKEITSKRITERIEN_RSI_v6.md`](SKALIERBARKEITSKRITERIEN_RSI_v6.md).
