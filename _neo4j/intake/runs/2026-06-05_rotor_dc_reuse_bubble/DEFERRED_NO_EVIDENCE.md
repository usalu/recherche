# Deferred — insufficient first-party evidence for graph facts

Items from `rotor_dc_reuse_bubble_v2.md` and web research that stay **off-graph** until per-item verification.

## Interpretive / analytical (never import as facts)

| Item | Reason |
|---|---|
| §13 matrix scores (reuse intensity, infrastructural potential) | Analytical ratings, not sourced measurements |
| §12 "system-building reuse infrastructure" label | Synthesis conclusion; keep in ResearchDocument only |
| §0–§3 interpretive paragraphs | Labelled interpretation in dossier |
| "Infrastructural value" thesis (§0) | Interpretation grounded in facts but not a graph fact |

## Actor / node deferrals

| Proposed import | Why deferred | What would unblock |
|---|---|---|
| `greater_paris_metropolis`, `municipality_wiltz` | PREUSE LAP workshop only (W31/W32); no pilot lead URL yet | Dedicated PREUSE territory action-plan page |
| `city_of_mechelen`, `city_of_lorient` | On partner list (W32) but no pilot-opening post fetched | Mechelen/Lorient first-party PREUSE case page |
| `list` / LIST Luxembourg | W32 partner page only; no graph node yet | Import with `BETEILIGT_AN` prog_preuse in partner batch |
| `neighborhood_production` | PREUSE partners page label; entity unclear vs La Fabrique | Confirm legal entity name |
| `atelier_4_5` | W44/W17 belegt but 2017 contributor only | Import only if Opalis partner mesh batch requested |
| `citydev_brussels` as `:Akteur` | No citydev page naming Rotor DC (W20 brusiness secondary only) | citydev.brussels project file for Da Vinci/Bordet site |
| `van_hameren_houthandel` | Boardwalk supplier (W10/W11) | Supplier-network batch only |
| `retrival` | Caserne press names Retrival; not rotordc | Retrival first-party Caserne page |

**Promoted to importable (see [`EVIDENCE_DEEP_DIVE.md`](EVIDENCE_DEEP_DIVE.md)):** `la_fabrique_des_quartiers` (≠ `la_fabrique_de_bordeaux_metropole`), `city_of_utrecht` → PREUSE, donor nodes Generale/CBR/Borgerstein/CCN/Georges Henri.

## Edge deferrals

| Edge | Why deferred |
|---|---|
| `rotordc` `BETEILIGT_AN` `p_recypark_demets_anderlecht` | W18 names Rotor only; W19 inspiration blog ≠ participation |
| `rotordc` ↔ `bellastock` direct | No first-party direct org link (only Opalis/PREUSE/FCRBE press W42) |
| Bulk donor `:Bauwerk` from §9 **tag list only** | Tag index ≠ per-case proof — **but** per-post cases now unlocked (W24–W26, W38, W43) |
| BOMACO, Durobor, Belgacom, … | Blog index titles only; need per-post fetch before import |
| `opalis` → `prog_fcrbe` typed edge | W06/W39 programmatic hosting; enrich props + sidecar unless schema adds programme rel |
| FCRBE 37-pilot roster → individual `:Projekt` nodes | W34 registry exists; import selective (e.g. W35 Dance Center) not bulk |
| `whitewood` / `immobel` → OXY | W36/W37 belegt but optional commissioner batch |

## Phase deferrals

| Item | Status |
|---|---|
| Meta `:Wiederverwendungskette` for §0 reuse chain | Dossier synthesis; needs per-step actor URL |
| Internal Rotor DC teams (IN / Process / Shop / Support) | Organisational detail; no separate `:Akteur` nodes without HR/org-chart source |
| Kanal Museum, SAU Caserne, Permeke, Zinneke upgrades | Rotor projects list dates only in dossier |
| European FCRBE partner bulk beyond existing `BETEILIGT_AN` | Many already on `prog_fcrbe`; dedup before PREUSE overlap |
