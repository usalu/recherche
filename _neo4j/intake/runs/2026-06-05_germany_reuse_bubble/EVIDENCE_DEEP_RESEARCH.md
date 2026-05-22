# Germany reuse bubble — deep evidence research

**Date:** 2026-06-06  
**Scope:** Post-apply audit of `bauteilboerse_hannover`, `haus_der_materialisierung`, and surrounding edges.  
**Method:** First-party pages, public-sector / university / funder sources, independent journalism.

---

## 1. Were Hannover and HdM “already there”?

| Layer | Hannover | Haus der Materialisierung |
|---|---|---|
| Legacy `_archive/research/akteur/` | `Bauteilboerse_Hannover` dossier | `Haus_der_Materialisierung` dossier |
| Old batch export | — | `p_haus_der_materialisierung_berlin` (Projekt placeholder, never live) |
| Live `mit-bestand` before 2026-06-05 apply | **missing** (`graph_probe.json`) | **missing** |
| Live after apply | `bauteilboerse_hannover` (`:Akteur`) | `haus_der_materialisierung` (`:Akteur`) |

**Conclusion:** Conceptually documented for years; **not** present as canonical `:Akteur` nodes until this run. The apply created the right entities but used new snake_case IDs — not duplicates of legacy PascalCase archive paths.

---

## 2. Entity evidence (existence + role)

### Bauteilbörse Hannover — **A/B**

| Source | URL | Key quote |
|---|---|---|
| First-party homepage | https://bauteilboerse-hannover.de/ | Regional market for used components; c/o Glocksee Bauhaus e.V., Calenberger Neustadt |
| restado seller profile | https://restado.de/profil/bauteilboerse-hannover/ | “Markt für gebrauchte Bauteile in Hannover und der Region”; Tue 15–19h |
| bauteilnetz partner listing | http://www.bauteilnetz.de/bauteilnetz/website/stdws_adresse/bauteilboersen.html | Listed partner Bauteilbörse alongside Bremen, Berlin-Brandenburg, etc. |
| restado cooperation page | https://restado.de/ueber-restado/kooperation/ | “Bauteilnetz / Bauteilbörsen Deutschland (u.a. Hannover und Brandenburg)” |
| restado homepage | https://restado.de/ | “arbeiten … mit den lokalen Bauteilbörsen … Bauteilbörse Hannover” |
| Heinrich Böll Stiftung (independent) | https://www.boell.de/de/2025/07/09/nachhaltiges-bauen-umbau-baustoffe/bauteile-recycling | restado and Concular as shared-founder digital reuse ecosystem |

**Operator detail (new):** Hannover runs under **Glocksee Bauhaus e.V.** (gemeinnützig), not a standalone GmbH.

### Haus der Materialisierung — **A**

| Source | URL | Key quote |
|---|---|---|
| HdM homepage | https://hausdermaterialisierung.org/ | Material cycles, workshops; part of Haus der Statistik since 2018 |
| HdM info / Koop5 | https://hausdermaterialisierung.org/info/ | Koop5 partners; Zentrum für klimaschonende Ressourcennutzung since 2021 |
| Kunst-Stoffe (Träger) | https://kunst-stoffe-berlin.de/haus-der-materialisierung/ | Operates Re-Use centre inside HdM; funded by SenUVK + Koop5 |
| TU Berlin research | https://www.tu.berlin/en/circulareconomy/research/hdm | “First multidisciplinary urban center for circular economy in Berlin”; real-world lab |
| DBU project database | https://www.dbu.de/projektdatenbank/35122-01/ | Funded Reallabor 2019–2023 at HdM |
| ZKU publication | https://www.zku-berlin.org/nc/de/publishing/haus-der-materialisierung/ | Independent book on HdM as transformation site |

**New structural detail:** HdM e.V. registered 2024 (gemeinnützig) per HdM info page.

---

## 3. Edge audit — what we applied vs what web evidence supports

### Strong — keep as `belegt`

| Edge | Evidence |
|---|---|
| `concular` ↔ `bauteilboerse_hannover` | restado profile + restado→Concular operator chain (Böll Stiftung corroborates shared ecosystem) |
| `software_restado` ↔ `bauteilboerse_hannover` | restado profile |
| `haus_der_materialisierung` ↔ `tu_berlin` | TU Berlin HdM project page (A) |
| All `BELEGT_IN` on Hannover / HdM | First-party URLs verified |

### Upgrade candidate — currently `teilweise_belegt`, now **A**

| Edge | Better source |
|---|---|
| `bauteilboerse_bremen` ↔ `bauteilboerse_hannover` | bauteilnetz.de lists **both** as partner Bauteilbörsen; BauNetz Wissen describes shared DBU-backed network |
| `bauteilboerse_hannover` ↔ `bauteilnetz_deutschland` | **missing in graph** — should add via same listing |

### Missing — high value, **not in graph**

| Edge / node | Evidence | Confidence |
|---|---|---|
| `kunst_stoffe_ev` ↔ `haus_der_materialisierung` | Kunst-Stoffe operates Zentrum inside HdM; HdM info names Kunst-Stoffe as Projektleitung | **A** |
| `material_mafia` (new node) ↔ `haus_der_materialisierung` | HdM homepage lists MaterialMafia on-site; DBU + TU Berlin name Material Mafia as consortium partner | **A** |
| `material_mafia` ↔ `tu_berlin` | Same DBU/TU consortium | **A** |
| `circular_berlin` (or `circular_city_berlin`) ↔ `haus_der_materialisierung` | TU Berlin + HdM info: “Circular City – Zirkuläre Stadt e.V.” in DBU Reallabor | **A** |
| `bauteilboerse_hannover` ↔ `bauteilnetz_deutschland` | bauteilnetz partner page | **A** |

### Weak / overclaimed — consider downgrade or remove

| Edge | Problem |
|---|---|
| `circular_structural_design` ↔ `bauteilboerse_hannover` | No direct co-mention; only generic “German reuse ecosystem” inference |
| `haus_der_materialisierung` ↔ `bauteilboerse_bremen` / `hannover` | No co-citation; different layers (civic hub vs component depots); network inference only |
| `haus_der_materialisierung` ↔ `madaster_epea` | No direct Berlin co-project found; EPEA/Madaster cases are other buildings (Huthmacher, PHV) |
| `concular` ↔ `madaster` | DGNB lists both as **parallel** passport providers — ecosystem peers, not partners; Heidelberg pilot is Madaster+EPEA+Heidelberg Materials, not Concular joint venture |

---

## 4. Deferred items — reassessment

| Item | Old verdict | New verdict |
|---|---|---|
| `material_mafia` | SKIP (1 edge) | **IMPORT** — DBU consortium + on-site tenant; ≥4 seed edges (HdM, TU, Circular City, ZKB if in graph) |
| `circular_berlin` | SKIP | **IMPORT as HdM research partner** — TU Berlin + HdM info name Circular City e.V.; link to HdM, not Concular spine |
| `kunst_stoffe_ev` link | not considered | **ENRICH** — already in graph; add VERBUNDEN + BELEGT_IN to HdM |
| Concular project cases (TXL, ICE, …) | SKIP | **unchanged** — still ≤1–2 spine links each; keep sidecar |
| `concular` ↔ `madaster` | applied teilweise | **keep but relabel** — `ecosystem_peer_dgnb_passport_providers`, not operational partnership |

---

## 5. Recommended follow-up patch (`phase1c_evidence_hardening`)

1. Add quellen: bauteilnetz partner page, Kunst-Stoffe HdM page, DBU 35122-01, restado kooperation, TU Berlin HdM (DE).
2. Add `kunst_stoffe_ev` ↔ `haus_der_materialisierung` (both directions).
3. Add `bauteilboerse_hannover` ↔ `bauteilnetz_deutschland`; upgrade bremen↔hannover evidence props.
4. Add `material_mafia` node + edges to HdM, TU Berlin (DBU/TU sources).
5. Add `circular_berlin` node (or map to existing ID if found) + HdM edge from TU/DBU.
6. **Do not add** without new sources: HdM↔Bauteilbörsen, CDS↔Hannover, HdM↔madaster_epea.

---

## 6. Files

- Supplement register: [`EVIDENCE_REGISTER_SUPPLEMENT.csv`](EVIDENCE_REGISTER_SUPPLEMENT.csv)
- Updated deferrals: [`DEFERRED_NO_EVIDENCE.md`](DEFERRED_NO_EVIDENCE.md)
