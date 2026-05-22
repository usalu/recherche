# France reuse bubble — deep evidence research

**Date:** 2026-06-06  
**Scope:** Post-apply audit of teilweise_belegt edges, deferred `mineka`, and `association_reavie` links.  
**Method:** Opalis supplier pages, ADEME/FCRBE study, public-sector profiles, independent journalism.

---

## 1. Edge audit — upgrades to `belegt`

| Edge | Old basis | New A-source |
|---|---|---|
| `opalis` ↔ `cycle_up` | ecosystem inference | [Opalis Cycle Up](https://opalis.eu/fr/fournisseurs/cycle) — full supplier profile |
| `bellastock` ↔ `backacia` | via-opalis inference | Opalis Backacia + Bellastock Opalis France maintainer |
| `cycle_up` ↔ `backacia` | peer marketplace | [ADEME 40 revendeurs](https://librairie.ademe.fr/economie-circulaire-et-dechets/5516-reemploi-des-materiaux-de-construction.html) — both in Opalis/FCRBE study |
| `bellastock` ↔ `cycle_up` | polycentric layer | [Le Moniteur](https://www.lemoniteur.fr/article/missionnaires-du-circulaire.2133509) + Opalis listing |
| `bellastock` ↔ `association_reavie` | Stains cluster inference | [Opalis RéaVie](https://opalis.eu/fr/fournisseurs/reavie) — directory co-maintained by Bellastock |

## 2. New high-value edges

| Edge / node | Evidence | Confidence |
|---|---|---|
| `opalis` ↔ `association_reavie` | Opalis supplier directory | **A** |
| `mineka` (`:Akteur`) | [Opalis Minéka](https://opalis.eu/fr/fournisseurs/mineka) + [mineka.fr](https://mineka.fr/) | **A** |
| `mineka` ↔ `opalis` / `bellastock` / `cycle_up` / `backacia` | ADEME 40-reseller Opalis study + directory peers | **A** |
| `association_reavie` BELEGT_IN | asso-reavie.fr, SSD département article, Opalis profile | **A** |
| `bellastock` BELEGT_IN Fabrique du Clos | [SSD Habitat visit](https://www.seinesaintdenishabitat.fr/notre-actualite/nos-actualites/visite-de-la-fabrique-du-clos-au-clos-saint-lazare-de-stains/) — piloted by SSD Habitat + Bellastock 2016 | **A** |

## 3. Dropped weak edges

| Edge | Problem |
|---|---|
| `mobius_reemploi` ↔ `cycle_up` | Independent IDF reconditioners; no co-project found |
| `raedificare` ↔ `backacia` | RAEDIFICARE **not** on Opalis; own marketplace only |
| `association_reavie` ↔ `mobius_reemploi` | Same département only; no direct partnership |

## 4. Deferred reassessment

| Item | Old verdict | New verdict |
|---|---|---|
| `mineka` | SKIP (Lyon local) | **IMPORT** — Opalis-listed + ADEME/FCRBE 40-reseller study; ≥4 spine edges |
| `association_reavie` ↔ `bellastock` | teilweise_belegt | **UPGRADE** — Opalis directory maintainer link |
| `p_fabrique_du_clos` as node | SKIP | **unchanged** — BELEGT_IN on `bellastock` only (SSD Habitat source) |
| `booster_du_reemploi`, demonstrators | SKIP | **unchanged** — still ≤2 direct spine links |
| `raedificare` ↔ marketplace mesh | weak peer edge | **DROP** `raedificare`↔`backacia`; keep `raedificare` isolated with homepage BELEGT_IN |

## 5. Key sources

- Opalis supplier pages: Cycle Up, Backacia, RéaVie, Minéka
- ADEME study: 40 professional resellers → Opalis directory (FCRBE)
- Le Moniteur: Bellastock SCIC, REPAR, FCRBE, Opalis France with Rotor
- Seine-Saint-Denis: RéaVie territorial profile; Fabrique du Clos = Bellastock + SSD Habitat

## 6. Files

- Patch: [`patches/phase1c_evidence_hardening.patch.jsonl`](patches/phase1c_evidence_hardening.patch.jsonl)
- Supplement: [`EVIDENCE_REGISTER_SUPPLEMENT.csv`](EVIDENCE_REGISTER_SUPPLEMENT.csv)
- Updated deferrals: [`DEFERRED_NO_EVIDENCE.md`](DEFERRED_NO_EVIDENCE.md)
