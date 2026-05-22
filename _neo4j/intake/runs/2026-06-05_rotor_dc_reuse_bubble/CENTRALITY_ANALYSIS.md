# Rotor DC reuse bubble — centrality analysis

**Run:** `2026-06-05_rotor_dc_reuse_bubble`  
**Evidence dossier:** `_knowledge/reuse_bubbles/rotor_dc_reuse_bubble_v2.md`  
**Live baseline:** `mit-bestand` (queried 2026-06-05) — see [`centrality_report.json`](centrality_report.json)

---

## 1. What “central” means here

Two lenses are combined:

| Lens | Question |
|---|---|
| **Document topology** | Which actors sit on the evidence-backed stack (§11 diagram) and score “very high” infrastructural potential (§13 matrix)? |
| **Graph connectivity** | Which nodes already have the most relationships, and where is the ecosystem mesh thin or broken? |

The bubble is **not** a flat star around Rotor DC. The document describes a **layered stack**:

```text
FCRBE + PREUSE + Opalis          ← European / directory / policy layer
        ↓
Rotor vzw/asbl                     ← research, design assistance, education
        ↓
Rotor DC                           ← cooperative: dismantling, processing, shop, Evere hub
        ↓
Supply (donor buildings, contractors) | Demand (architects, public clients, projects)
```

---

## 2. Tier-1 central elements (document)

These five nodes anchor almost every evidence claim. They should be the **first integration targets**.

| Rank | Element | Graph `id` | Role in bubble | Evidence | Infrastructural potential (doc §13) |
|---:|---|---|---|---|---|
| 1 | **Rotor vzw/asbl** | `Rotor` | Research, design assistance, policy, education; parent of Opalis; leads FCRBE & PREUSE | S06–S08, S11–S12, S16–S23 | Very high (indirect) |
| 2 | **Rotor DC** | `rotordc` | Operational cooperative: dismantling, processing, shop, 14k m² Evere hub | S01–S05, S14–S15, S22 | Very high |
| 3 | **Opalis** | `opalis` | Directory + documentation; bridges dealers and commissioners | S08–S10, S22 | Very high (indirect) |
| 4 | **FCRBE** | `prog_fcrbe` | Interreg NWE; audits, specs, 1500+ operator directory, 36 pilots | S11 | Very high (indirect) |
| 5 | **PREUSE** | **`prog_preuse` — missing** | Interreg NWE; public-authority reuse centres, training | S12–S13 | Very high (indirect) |

**Bridge actor (tier 1b):** `bellastock` — Opalis French section, FCRBE partner, PREUSE partner (S09, S11, S12). Not in the vertical stack but connects the European layer across FR/BE.

---

## 3. Tier-2 central elements (high connection count)

### 3.1 People as hidden hubs

| `id` | Bridges | Why central |
|---|---|---|
| `maarten_gielen` | Rotor, rotordc, opalis | Only person linking all three core actors via `VERBUNDEN_MIT_AKTEUR` |
| `lionel_devlieger` | Rotor (+ rotordc via Billiet network) | Rotor founding network |
| `michael_ghyoot` | Rotor, prog_fcrbe (stub) | FCRBE capitalisation link |
| `lionel_billiet` | Rotor, rotordc | Operational / research overlap |

### 3.2 Projects as demand-side hubs

| `id` | Doc role | Graph status |
|---|---|---|
| `p_multi_brussels_reuse_in_multi` | Rotor design assistance; rotordc salvaged Generale de Banque granite | Rotor + rotordc `BETEILIGT_AN` (unklar confidence) |
| `p_recypark_demets_anderlecht` | Rotor design assistance; glulam reuse | Rotor `BETEILIGT_AN` only — rotordc not linked |
| `p_chiro_d_itterbeek_dilbeek` | Not in bubble doc but **dominates rotordc graph degree** | rotordc `BETEILIGT_AN` ×23 Bauteilgruppen |
| OXY, Caserne Trésignies, Boardwalk | §10 design-assistance cases | **Not in graph** as `:Projekt` nodes |

### 3.3 Physical / supply nodes (doc-central, graph-weak)

| Concept | Doc evidence | Graph gap |
|---|---|---|
| Evere / Da Vinci site (14 000 m²) | S02, S04, S05 | No `:Bauwerk` / `:Standort` node; URL quelle exists (`q_url_3dbb1579…`) |
| Générale de Banque HQ | S01, S07, S18, S22 | `bw_generale_de_banque_brussels` exists; weak link to rotordc/Multi |
| CBR, BOMACO, Borgerstein, CCN, … | S01, S14 | Mostly absent as donor `:Bauwerk` nodes |

---

## 4. Live graph connectivity (mit-bestand)

### 4.1 Total relationship degree (all types)

| `id` | Total rels | Primary rel types |
|---|---:|---|
| `rotordc` | **55** | BETEILIGT_AN (23), HAT_AKTEURROLLE (8), taxonomy |
| `opalis` | **34** | HAT_BAUTEILTYP (10), NUTZT_MATERIAL (7), taxonomy |
| `Rotor` | **28** | VERBUNDEN_MIT_AKTEUR (11), HAT_AKTEURROLLE (7), BETEILIGT_AN (6) |
| `bellastock` | **15** | HAT_AKTEURROLLE (5), VERBUNDEN_MIT_AKTEUR (4) |
| `prog_fcrbe` | **13** | inbound BETEILIGT_AN from many partners |

**Interpretation:** `rotordc` looks most connected, but **23 of 55** edges are Chiro-project Bauteilgruppen — operational taxonomy, not ecosystem topology. **`Rotor` is the real actor-network hub** (11 `VERBUNDEN_MIT_AKTEUR`).

### 4.2 Ecosystem mesh (`VERBUNDEN_MIT_AKTEUR` only)

| Node | Degree | Neighbors |
|---|---:|---|
| `Rotor` | 7 | opalis, rotordc, maarten_gielen, michael_ghyoot, lionel_billiet, lionel_devlieger, tristan_boniver |
| `rotordc` | 4 | Rotor, maarten_gielen, lionel_billiet, sebastien_paulet |
| `opalis` | 2 | Rotor, maarten_gielen |
| `bellastock` | 3 | hugo_topalov, sarah_westerfeld, frederic_denise (people only) |

### 4.3 Stack internal edges (present vs missing)

| Edge | Status | Evidence if missing |
|---|---|---|
| Rotor ↔ rotordc | **Present** (`teilweise_belegt`) | S07 |
| Rotor ↔ opalis | **Present** (duplicate edge pair) | S08, S09 |
| Rotor → prog_fcrbe | **Present** (`BETEILIGT_AN`, unklar) | S11 |
| bellastock → prog_fcrbe | **Present** | S11 |
| rotordc ↔ opalis | **Missing** | S22 (Opalis dealer page) |
| opalis ↔ bellastock | **Missing** | S09 |
| Rotor → prog_preuse | **Missing** (no `prog_preuse` node) | S12 |
| rotordc ↔ bellastock | **Missing** | indirect via FCRBE/PREUSE only |
| opalis ↔ prog_fcrbe | **Missing** | S09 (“developed within FCRBE”) |

---

## 5. Centrality ranking for graph integration

Combined score: document tier + ecosystem gap + evidence strength.

| Priority | Target | Action |
|---:|---|---|
| **P0** | Ecosystem spine | Wire Rotor ↔ rotordc ↔ opalis ↔ prog_fcrbe ↔ bellastock as `VERBUNDEN_MIT_AKTEUR` with S07–S11 quotes; add `prog_preuse` + Rotor `BETEILIGT_AN` (S12–S13) |
| **P1** | Opalis ↔ rotordc | Dealer listing edge (S22) — highest-value missing link in operational layer |
| **P1** | Project mesh | Upgrade/promote Multi + Recypark `BETEILIGT_AN` to `belegt` with Rotor project pages (S18, S20); add OXY + Caserne if nodes created |
| **P2** | Evere site node | `:Bauwerk` or `:Standort` anchored to S04/S05; link rotordc + Rotor |
| **P2** | Donor-building spokes | Generale de Banque → Multi material flow (S18); defer bulk §9 tag list per doc caution |
| **P3** | FCRBE partner roster | Many partners already `BETEILIGT_AN` prog_fcrbe; defer new partners without first-party URLs |
| **Defer** | §13 matrix scores, interpretive claims, blog-tag buildings without per-case verification | Off-graph / sidecar only |

---

## 6. Recommended seed set for visualization

Use this id list for a first-hop bubble view in Neo4j Browser:

```cypher
// Core stack + bridge + key projects
UNWIND [
  'Rotor','rotordc','opalis','bellastock','prog_fcrbe',
  'maarten_gielen','lionel_devlieger','michael_ghyoot',
  'p_multi_brussels_reuse_in_multi','p_recypark_demets_anderlecht',
  'p_chiro_d_itterbeek_dilbeek','bw_generale_de_banque_brussels'
] AS sid
MATCH (n {id: sid})
OPTIONAL MATCH (n)-[r]-(m)
WHERE m.id IN [
  'Rotor','rotordc','opalis','bellastock','prog_fcrbe',
  'maarten_gielen','lionel_devlieger','michael_ghyoot',
  'p_multi_brussels_reuse_in_multi','p_recypark_demets_anderlecht',
  'p_chiro_d_itterbeek_dilbeek','bw_generale_de_banque_brussels'
]
RETURN n, r, m
```

After integration, extend with `prog_preuse` and Opalis↔rotordc edge.

---

## 7. Key takeaway

**Rotor DC is the operational centre of the bubble in the evidence document, but Rotor vzw is the graph’s connectivity hub today.** The highest-value graph work is not adding more taxonomy edges to `rotordc` — it is **closing the missing European/policy mesh** (Opalis, FCRBE, PREUSE, Bellastock) and **promoting project participation** (Multi, Recypark, future OXY/Caserne) with first-party evidence.

Next step: [`INTEGRATION_PLAN.md`](INTEGRATION_PLAN.md) (phased patches, Swiss-bubble pattern).
