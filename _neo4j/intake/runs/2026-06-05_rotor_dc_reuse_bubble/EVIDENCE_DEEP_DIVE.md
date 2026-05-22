# Evidence deep dive — Rotor DC reuse bubble

**Run:** `2026-06-05_rotor_dc_reuse_bubble`  
**Supersedes/extends:** [`INTERNET_RESEARCH_SUPPLEMENT.md`](INTERNET_RESEARCH_SUPPLEMENT.md)  
**Register:** [`EVIDENCE_REGISTER_SUPPLEMENT.csv`](EVIDENCE_REGISTER_SUPPLEMENT.csv) (W01–W45)

Second-pass web research focused on **verbatim quotes**, **donor-building cases**, **PREUSE pilot mesh**, and **FCRBE↔rotordc** links.

---

## 1. Ecosystem spine — additional quotes

### Opalis ↔ rotordc (dealer + case studies)

| ID | URL | Quote | Graph action |
|---|---|---|---|
| W05 | opalis.eu/en/dealers/rotor-deconstruction | *"Rotor Deconstruction started as an offshoot of… Rotor, and operates as a separate entity since 2016."* | `VERBUNDEN_MIT_AKTEUR` opalis↔rotordc |
| W05b | same | Dealer page lists **two** Generale Bank extraction case studies + *"66 tonnes"* natural stone | `BELEGT_IN` on rotordc; donor edges |
| W27 | rotordc.com/about-us | *"Since 2012, Rotor has been documenting… dealers… The results are published on opalis.eu."* | rotordc→opalis operational link (sidecar: directory publishes stock) |

### Opalis ↔ bellastock ↔ programmes

| ID | URL | Quote | Graph action |
|---|---|---|---|
| W04 | opalis.eu/en/about | *"Since 2019, the cooperative Bellastock has joined the project."* | opalis↔bellastock |
| W04b | same | *"Between 2024 and 2027, Opalis is maintained and updated by Rotor and Bellastock as part of… PREUSE."* | opalis context on prog_preuse |
| W04c | same | *"Rotor by Brussels Environment as part of the Renolution strategy"* | `brussels_environment` funder edge |
| W40 | renolution.brussels | Lists **Opalis** as documentation centre for reuse dealers BE/NL | `BELEGT_IN` opalis |

### PREUSE — launch, partners, pilots

| ID | URL | Quote | Graph action |
|---|---|---|---|
| W28 | preuse.nweurope.eu/…/official-launch… | *"our team of 8 organisations met at the **Rotor offices in Brussels**, the project's lead partner"* | Rotor lead anchor |
| W28b | same | Launch visits: Schaarbeek municipal depot + **In Limbo** reuse centre | optional site nodes (defer) |
| W32 | list.lu/…/preuse | Full partner list incl. *"La Fabrique des Quartiers – SPLA (FR)"* — **not** Bordeaux entity | new id `la_fabrique_des_quartiers` |
| W29 | preuse.nweurope.eu/…/pilots-operations | 3 pilots: **Utrecht**, **Lorient**, **Roubaix** (La Fabrique des Quartiers) | partner `BETEILIGT_AN` after nodes |
| W30 | preuse.nweurope.eu/…/utrecht-reuse-centre | *"Trechterweide"* opened **18 March 2025** | `city_of_utrecht` → prog_preuse |
| W31 | preuse.nweurope.eu/…/roubaix | Steering committee hosted in Roubaix; centre led by **La Fabrique des Quartiers** | `la_fabrique_des_quartiers` → prog_preuse |

### FCRBE ↔ Opalis ↔ rotordc

| ID | URL | Quote | Graph action |
|---|---|---|---|
| W06 | opalis.eu/en/documentation | *"documents published as part of the Interreg NWE FCRBE project"* | opalis–FCRBE enrichment |
| W34 | vb.nweurope.eu/…/fcrbe… | 37 pilot operations; **140 t** reclaimed / **186 t** reused | prog_fcrbe scope |
| W33 | rotordb.org/…/12-fcrbe-pilot-operations | Rotor led **12** of 37 pilots; lists extraction + integration sites | Rotor→prog_fcrbe upgrade |
| W35 | vb.nweurope.eu (Dance Center Paris pilot) | *"Supplier : **Rotor Déconstruction**"* | rotordc→prog_fcrbe `teilweise_belegt` via FCRBE pilot |

### Bellastock ↔ Rotor (FCRBE press layer)

| ID | URL | Quote | Graph action |
|---|---|---|---|
| W42 | vb.nweurope.eu FCRBE news | *"Hugo Topalov from Bellastock and Michaël Ghyoot from Rotor teamed up…"* | people edges exist; programme context |
| W42b | vb.nweurope.eu | *"Bellastock gives pride to FCRBE and **Opalis** through the pilot operation… Quimper station to Nantes"* | opalis↔bellastock corroboration |

**Still no direct rotordc↔bellastock org link** — only Opalis joint maintenance + PREUSE + FCRBE press.

---

## 2. Projects — expanded evidence

### OXY (`p_oxy_centre_monnaie`)

| ID | URL | Quote |
|---|---|---|
| W07 | rotordb.org/…/oxy-centre-monnaie | Commissioners: **Whitewood, Immobel**; 89% retention; **4–6% reuse** |
| W08 | rotordb.org/…/works-oxy-well-underway | *"300 running meters of… aluminium facade profiles which will be **reconverted to lighting fixtures by RotorDC**"* |
| W36 | W07 | *"acquired by property developers Whitewood and Immobel"* → `whitewood`/`immobel` `BETEILIGT_AN` optional |
| W37 | rotordb.org/…/material-donnerie-oxy | *"second collaboration between Rotor and Whitewood/Immobel"* after Multi |

### Multi (`p_multi_brussels_reuse_in_multi`) — upgrade pack

| ID | URL | Quote |
|---|---|---|
| W12 | rotordb.org/…/multi-de-brouckere-tower | *"Flamed granite flooring, **salvaged by Rotor DC** from the Generale de Banque"* |
| W13 | triodos.be/…/multi… | Corroborates Rotor DC granite on public terrace landing |
| W21 | opalis.eu/fr/projets/ancien-siege-de-la-generale-de-banque | **66 t** granite; **230 t** total; *"83%… pris en stock par Rotor"* |

**Material path (now belegt):** `bw_generale_de_banque_brussels` → (salvage) → `rotordc` → (granite) → `p_multi_brussels_reuse_in_multi`

### Recypark — rotordc still deferred

| Source | Says |
|---|---|
| rotordb.org/recypark, 51N4E, RIBA | **Rotor** as materials salvage / design assistance |
| rotordc.com/blog/inspiration-4/recypark… | Inspiration post only — **not** participation |

### Caserne Trésignies

| ID | URL | Quote |
|---|---|---|
| W09 | rotordb.org/…/caserne-tresignies | Rotor: inventories, dismantling tests, specs; partners **City of Charleroi, Igretec** |
| Press (DHnet) | Dismantling by **Retrival** — do **not** attribute to rotordc |

### Boardwalk

| ID | URL | Quote |
|---|---|---|
| W10 | rotordb.org/…/boardwalk… | 300 m²; Van Hameren; Minerve Edegem |
| W11 | minerve.info/vlonder | *"Dankzij Rotor vond Revive… azobé"*; cites Opalis dealer directory |

---

## 3. Donor buildings — per-case unlocks (was bulk-deferred)

Dossier §9 caution still applies to **tag-only** names. These have **dedicated rotordc or Opalis case pages**:

| Proposed `bw_*` | Evidence ID | Source | Material / action | Confidence |
|---|---|---|---|---|
| `bw_generale_de_banque_brussels` (exists) | W21, W23 | Opalis project + rotordc blog | 230 t / 66 t granite; kick-started rotordc | **belegt** |
| `bw_cbr_building_watermaal` | W24, W24b | rotordc blog + shop | Windows from renovation; not demolition | **belegt** |
| `bw_borgerstein_sint_katelijne_waver` | W25, W26 | rotordc blog p.2 + shop | **>700 m²** ceramic tiles, May 2024 | **belegt** |
| `bw_ccn_brussels_groupe_structures` | W43 | rotordc blog p.2 | Salvaging from CCN ~1974 | **belegt** |
| `bw_georges_henri_playground_woluwe` | W38 | rotordc blog | ~1000 m² Douglas fir; commissioner **Brussels Environment** | **belegt** |

### Generale de Banque — Opalis extraction detail (W21)

Verbatim quantities from [Opalis project page](https://opalis.eu/fr/projets/ancien-siege-de-la-generale-de-banque):

- 2 500 m² suspended ceilings  
- **66 t** granite wall/floor cladding  
- 138 interior doors  
- **>230 t** finishing materials total  
- Implementers: **Rotor**, De Meuter, Art2Work  
- *"83%… pris en stock par Rotor afin d'être revendus"*  

Links `rotordc` stock role to donor building and downstream Multi granite (W12).

### rotordc blog index (page 2) — further cases for phase-2+ donor batch

Verified titles on https://rotordc.com/blog/salvaging-by-rotordc-3/page/2:

- PointCulture/ULB (88 plywood displays)  
- Durobor Soignies (wood moulds)  
- Braine-le-Château stonemason house  
- HF4/Carsid Charleroi  
- Belgacom Rue Lebeau  
- Villa Kavel 19 Maastricht  

Each needs individual post fetch before graph import (not tag-only).

---

## 4. Physical hub + landlords

| ID | URL | Quote | Node |
|---|---|---|---|
| W14–W16 | rotordc.com/about-us, contact, bma.brussels | 14 000 m²; Da Vinci; **Avenue de Bâle 3**; ERDF Circular Hub €2.9M | `bw_rotordc_evere_da_vinci_site` |
| W20 | brusiness.brussels | *"erfpacht van CityDev.brussels"* 14 000 m² | secondary |
| W45 | rotordc.com/about-us | *"Rotor DC is an autonomous side-project that emanates from Rotor vzw/asbl"* | enrich rotordc↔Rotor |

**citydev.brussels:** general erfpacht policy on citydev.brussels/nl — no page naming Rotor DC found in this pass. Keep `citydev_brussels` optional (`teilweise_belegt` via brusiness + rotordc contact).

---

## 5. Services + processing (operational evidence)

| ID | URL | What it supports |
|---|---|---|
| W46 | rotordc.com/service/depositsale | One-stop consignment/purchase for contractors, individuals, project owners |
| W47 | rotordc.com/blog/…/re-tile… | Tile mortar-removal service; BeCircular Brussels Region support |
| W05 | opalis dealer page | Workshops: tile cleaning, sanitary revision, lamp rewiring, wood denailing |

---

## 6. PREUSE / FCRBE partner import matrix (updated)

| Partner (official name) | Proposed graph `id` | In graph? | Evidence | Import now? |
|---|---|---|---|---|
| Rotor ASBL | `Rotor` | yes | W03, W28 | upgrade edges |
| Bellastock | `bellastock` | yes | W02, W04 | yes |
| City of Utrecht | `city_of_utrecht` | yes | W30, W29 | `BETEILIGT_AN` prog_preuse |
| Brussels Environment | `brussels_environment` | yes | W04c, W38, FCRBE export | funder + FCRBE (exists) |
| LIST | `list` or new | **no** | W32 | add node + edge |
| City of Mechelen | `city_of_mechelen` | **no** | W32, W31 LAP workshop | add node |
| Municipality of Wiltz | `municipality_wiltz` | **no** | W32 (LIST assists) | defer or add with LIST page |
| City of Lorient | `city_of_lorient` | **no** | W29 | add node |
| Greater Paris Metropolis | `greater_paris_metropolis` | **no** | W32 | defer (LAP only) |
| La Fabrique des Quartiers SPLA | `la_fabrique_des_quartiers` | **no** (≠ Bordeaux node) | W31, W32 | **new node** |
| Neighborhood Production | ? | **no** | partners page | verify = La Fabrique alias before import |

---

## 7. Claims promoted from deferred → importable

| Was deferred | Now | Evidence |
|---|---|---|
| opalis↔rotordc edge | **Import** | W05, W05b, W27 |
| opalis↔bellastock edge | **Import** | W04, W42b |
| Generale de Banque material path | **Import** | W21, W12, W23 |
| CBR / Borgerstein / CCN / Georges Henri donors | **Import** (4 nodes) | W24–W26, W38, W43 |
| OXY + rotordc participation | **Import** | W08 |
| `city_of_utrecht` → PREUSE | **Import** | W30 |
| `la_fabrique_des_quartiers` | **Import** (new id) | W31, W32 |
| rotordc → FCRBE pilot involvement | **teilweise_belegt** | W35 (Paris Dance Center supplier) |
| Atelier 4/5 → Opalis | optional | W44, W17 |

## 8. Still deferred

See updated [`DEFERRED_NO_EVIDENCE.md`](DEFERRED_NO_EVIDENCE.md).

---

## 9. Suggested claim IDs for sidecar (phase 1)

| claim_id | statement | evidence_ids |
|---|---|---|
| `claim_opalis_lists_rotordc_dealer` | Opalis publishes rotordc as professional dealer since 2016 spin-off | W05 |
| `claim_opalis_bellastock_preuse_2024_2027` | Opalis maintained by Rotor + Bellastock under PREUSE 2024–2027 | W04 |
| `claim_generale_banque_66t_granite_rotor` | 66 t granite + 230 t finishes salvaged from Generale de Banque HQ | W21, W23 |
| `claim_multi_granite_from_generale_rotordc` | Multi terrace granite salvaged by rotordc from Generale de Banque | W12, W13 |
| `claim_oxy_aluminium_reconversion_rotordc` | OXY facade aluminium reconverted to lighting by rotordc | W08 |
| `claim_borgerstein_700sqm_tiles` | rotordc dismantled >700 m² tiles from Borgerstein building | W25 |
| `claim_preuse_launch_rotor_brussels` | PREUSE launched at Rotor offices as lead partner | W28 |
| `claim_fcrbe_dance_center_supplier_rotordc` | FCRBE Paris Dance Center pilot supplier was Rotor Déconstruction | W35 |
