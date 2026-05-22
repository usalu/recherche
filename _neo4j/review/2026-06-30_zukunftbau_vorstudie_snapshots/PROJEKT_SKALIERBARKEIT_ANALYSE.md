# Projekt-Skalierbarkeit — Ergebnisse je Projekt (RSI v6)

**Zweck.** Ergebnisse je Projekt des Reuse-Scalability Index v6 (Gates G1–G6, Kriterien K1–K14). Methodik: [`SKALIERBARKEITSKRITERIEN_RSI_v6.md`](SKALIERBARKEITSKRITERIEN_RSI_v6.md), Kurzüberblick: [`REUSE_SCALABILITY_FRAMEWORK.md`](REUSE_SCALABILITY_FRAMEWORK.md). Handlungsempfehlungen: [`REUSE_GUIDELINES_UND_WORKFLOWS.md`](REUSE_GUIDELINES_UND_WORKFLOWS.md).

> **RSI v6** gegenüber v3: (i) **Gate-System** mit Kappungsregeln vor Score; (ii) **14 Kriterien** statt 6 Dimensionen (Planung, Inventar, Qualität, Haftung, Logistik, Beschaffung, Kosten, DfD, …); (iii) **Konfidenz A/B/C** aus Evidenz je Kriterium; (iv) **10 Archetypen**; (v) **21 verifizierte** Projekte mit manueller K/G-Kalibrierung, 62 Proxy mit Konfidenz C. ✓ = verifiziert. **v3-Scores historisch** in `project_scalability_scores.json` — nicht mit v6 vergleichen.

---

## 1 Kernergebnisse in einem Satz

Von 83 Projekten erreicht **keines** die Einstufung „skalierbar“ (≥ 75 RSI final); der **Median liegt bei 36,2** (Einzelfall/Fallstudie). **62 Projekte** haben mindestens ein Gate = 0 — die Prozesskette (Haftung, Beschaffung, Inventar) limitiert, nicht das Entwerfen. Spitze: **55 Great Suffolk Street (74,2)** durch regulatorisch reifen Struktur-ReUse (K4=4); **KA13 (74,0)** als Systemischer Aggregator. **People's Pavilion** fällt von v3-Rang #2 (79,1) auf v6-Rang **#13 (56,8)** — K9=4, aber K13=1 und schwache Gates G4/G6: **perfektes DfD ≠ Skalierungsmodell**.

---

## 2 Interpretative Befunde

**(A) Gates dominieren.** G4 (Haftung) und G6 (Beschaffung) sind häufigste Blocker. K2 ≥ 3 (robuste Versorgung) nur bei **14/83**.

**(B) Design bleibt Feldstärke, System schwach.** **8/83** mit K9 = 4 (DfD-Referenz). Ohne K2–K7 bleibt Einstufung Pilot oder Einzelfall.

**(C) Organisatorische Hebel (Welle 2).** Grande Halle (K7=4, Lot 01), Green House (K5/K8 Leasing), ReCreate (K4/K5 strukturell).

**(D) Proxy-Transparenz.** 62/83 Konfidenzklasse C — K5, K7, K8 aus v3-Proxy; vorsichtig zitieren.

---

## 3 Rangliste — Top 15 (RSI v6 final)

Vollständige Tabelle (83 Zeilen): [`_scal_table_v6.md`](_scal_table_v6.md) · maschinenlesbar: `project_scalability_scores_v6.json` / `.csv`

| # | Projekt | Land | RSI final | Konf. | Klasse | Einstufung | Archetyp | K2 | K3 | K4 | K9 |
|---:|---|---|---:|---:|---|---|---|---:|---:|---:|---:|
| 1 | 55 Great Suffolk Street ✓ | UK | **74.2** | 0.84 | A | bedingt skalierbar | Struktur-ReUse | 2 | 3 | 4 | 3 |
| 2 | KA13 Oslo ✓ | NO | **74.0** | 0.77 | B | bedingt skalierbar | System. Aggregator | 4 | 3 | 3 | 3 |
| 3 | Circl / ABN AMRO ✓ | NL | **69.0** | 0.77 | B | bedingt skalierbar | System. Aggregator | 4 | 3 | 2 | 4 |
| 4 | K.118 Halle 118 ✓ | CH | **67.8** | 0.76 | B | bedingt skalierbar | DfD-Referenz | 2 | 3 | 3 | 4 |
| 5 | Härmälänranta / ReCreate ✓ | FI | **67.2** | 0.85 | A | bedingt skalierbar | Struktur-ReUse | 1 | 3 | 4 | 2 |
| 6 | The Green House ✓ | NL | **66.5** | 0.74 | B | bedingt skalierbar | DfD-Referenz | 2 | 2 | 2 | 4 |
| 7 | CRCLR House ✓ | DE | **63.2** | 0.66 | B | bedingt skalierbar | DfD-Referenz | 2 | 3 | 2 | 4 |
| 8 | Thoravej 29 ✓ | DK | **61.2** | 0.84 | A | bedingt skalierbar | Großmaßstab | 1 | 3 | 3 | 3 |
| 9 | Recyclinghaus ✓ | DE | **61.0** | 0.69 | B | bedingt skalierbar | DfD-Referenz | 2 | 2 | 3 | 4 |
| 10 | Grande Halle ✓ | FR | **58.8** | 0.73 | B | Pilot | ReUse-Hub | 3 | 2 | 2 | 2 |
| 11 | Kamikatsu ✓ | JP | **58.5** | 0.71 | B | Pilot | ReUse-Hub | 4 | 2 | 2 | 2 |
| 12 | Europa Building ✓ | BE | **57.5** | 0.74 | B | Pilot | Ökosystem | 4 | 2 | 2 | 1 |
| 13 | People's Pavilion ✓ | NL | **56.8** | 0.61 | B | Pilot | DfD-Referenz | 3 | 2 | 2 | 4 |
| 14 | Resource Rows ✓ | DK | **56.2** | 0.67 | B | Pilot | Großmaßstab | 3 | 2 | 2 | 2 |
| 15 | TRÆ High-Rise ✓ | DK | **55.5** | 0.67 | B | Pilot | Großmaßstab | 2 | 2 | 2 | 3 |

---

## 4 Archetyp- und Einstufungsverteilung

| Archetyp | n |
|---|---:|
| Fallstudie | 47 |
| Klein-Pilot / Reallabor | 9 |
| DfD-Systemreferenz | 7 |
| Großmaßstab-Demonstrator | 6 |
| Tiefen-Pilot | 6 |
| Professioneller ReUse-Hub | 3 |
| Regulatorisch reifer Struktur-ReUse | 2 |
| Systemischer Aggregator | 2 |
| Netzwerk-/Ökosystem-Enabler | 1 |

| Einstufung (RSI final) | n |
|---|---:|
| Einzelfall / Fallstudie (0–39) | 62 |
| Pilot / Reallabor (40–59) | 12 |
| bedingt skalierbar (60–74) | 9 |

---

## 5 Historischer Verweis v3

Rangliste und Sub-Scores der **6 v3-Dimensionen** (Median 46,9, Spitze KA13 79,8): `project_scalability_scores.json`, Dokumentation [`SKALIERBARKEITSKRITERIEN_RSI_v3.md`](SKALIERBARKEITSKRITERIEN_RSI_v3.md) (superseded).
