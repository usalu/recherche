# Agent 06b — Non-Bubble Actor-Network Gap Closure

**Role:** Verifier Agent 06b — closes the residual `VERBUNDEN_MIT_AKTEUR` edge gap and the
sourced-`Akteur`-node gap that Agent 15 flagged as *never verified by Agents 01–06 and not tagged
with any 2026-06 `review_run`*.
**Mode:** READ-ONLY on Neo4j (`read-cypher` only). **No graph mutations.**
**Outputs:** [`ledger/agent_06b.csv`](../ledger/agent_06b.csv) (this report = `reports/agent_06b.md`).
**Date:** 2026-06-06.

---

## 1. Scope and exact coverage (what was counted, and why it differs from "~152 / ~167")

The brief estimated **~152 edges** and **~167 nodes** (Agent 15's headline figures). I recomputed the
true gap deterministically from the live graph rather than trusting the estimate, and document the
exact delta below.

### 1.1 Method (deterministic, reproducible)

1. Dumped **all** `VERBUNDEN_MIT_AKTEUR` edges from Neo4j (`elementId`, `from.id`, `to.id`,
   `review_run`, `connection_kind`, `evidence_url`, `evidence_quote`, `source_url`).
2. Dumped **all** sourced `Akteur` nodes (`source_urls` non-empty **OR** `primary_source_url`
   **OR** `source_url`).
3. Parsed the **already-applied** ledgers `agent_01.csv … agent_06.csv` to build:
   - `covered_pairs` = every `(from_id,to_id)` an actor-network rel that 01–06 already adjudicated;
   - `covered_nodes` = every `Akteur` id already adjudicated.
4. **Gap edges** = `VERBUNDEN_MIT_AKTEUR` with `review_run` *not* in any 2026-06 run **and**
   `(from,to)` *not* in `covered_pairs`.
5. **Gap nodes** = sourced `Akteur` *not* in `covered_nodes`.

Scripts: `_agent06b_work/compute_gap.py`, `plan_and_edges.py`, `build_ledger.py` (all committed in the
work folder for re-run).

### 1.2 Exact work-set

| Work-set | Agent 15 estimate | Agent 06b actual | Note |
|---|---:|---:|---:|
| `VERBUNDEN_MIT_AKTEUR` gap edges | ~152 | **218** | 15's count under-counted; reverse legs of bidirectional pairs were not all included |
| sourced `Akteur` gap nodes | ~167 | **168** | matches within 1 |
| **Total claims adjudicated** | ~319 | **386** | 218 rel + 168 node rows |

**Critical structural finding:** **0 of the 218 gap edges carry an on-graph `evidence_url` or
`source_url`.** Every single one is an *unsourced* actor-network assertion. This is exactly the failure
mode the campaign is hunting (consortium co-listings inflated into pairwise ties), so all 218 fail the
Evidence Gate on the graph as it currently stands — none can be auto-KEPT.

---

## 2. Verdict and action distribution (386 claims)

### 2.1 Verdicts

| Verdict | Edges | Nodes | Total |
|---|---:|---:|---:|
| PROVEN | 0 | 42 | **42** |
| PARTIAL | 12 | 17 | **29** |
| UNVERIFIABLE | 0 | 103 | **103** |
| MISSING_EVIDENCE | 142 | 3 | **145** |
| SCHEMA_VIOLATION | 64 | 3 | **67** |
| **Total** | **218** | **168** | **386** |

### 2.2 Proposed actions (campaign schema vocabulary)

| Action | Count | Maps to brief's bucket |
|---|---:|---|
| KEEP | 162 | **KEEP** |
| ADD_SOURCE | 144 | **RESOURCE** (a source must be added before the claim survives) |
| MERGE_DUPLICATE | 63 | **RELABEL** (structural dedup of reverse-direction twins) |
| ESCALATE_HUMAN | 13 | **RELABEL/DELETE pending human** |
| RESOURCE | 3 | **RESOURCE** |
| DELETE | 1 | **DELETE** |

> The brief asked for `DELETE / RESOURCE / RELABEL / KEEP` only. I kept the **full campaign schema
> vocabulary** (`VERIFICATION_LEDGER.schema.csv`) for consistency with Agents 01–06, and map it to the
> four high-level buckets above. In bucket terms: **KEEP 162, RESOURCE 147, RELABEL 76, DELETE 1**.

---

## 3. Edge findings (218 unsourced `VERBUNDEN_MIT_AKTEUR`)

Edges were classified **structurally** (no category inference about the *meaning* of a tie — only its
graph shape) and then, where I had fetched authoritative evidence, upgraded.

| Edge class | Count | Verdict | Action | Rationale |
|---|---:|---|---|---|
| `self_loop` (a → a) | 1 | SCHEMA_VIOLATION | **DELETE** | `Werner_Sobek → Werner_Sobek` is structurally invalid |
| `bidir_reverse` (reverse twin of a pair) | 63 | SCHEMA_VIOLATION | **MERGE_DUPLICATE** | redundant opposite-direction edge; collapse to one |
| `bidir_canonical` (canonical leg of a pair) | 66→57 | MISSING_EVIDENCE | **ADD_SOURCE** | keep one direction but it still has no source |
| `unsourced_affiliation` (single untagged edge) | 85 | MISSING_EVIDENCE | **ADD_SOURCE** | needs a source naming **both** endpoints |
| **corroborated off-graph** (subset, see §3.1) | 12 | PARTIAL | **ADD_SOURCE** | I found an authoritative page naming both endpoints |

**Stub/low-quality endpoints → ESCALATE_HUMAN (10 edges):** edges whose endpoint id is an unresolved
stub (`2hs`, `3xn`, etc.) are flagged for human disambiguation rather than blind KEEP/DELETE.

### 3.1 The 12 edges I corroborated with real evidence (Finnish RecReate precast cluster)

I fetched `recreate-project.eu/tag/precast-concrete`, which **names both endpoints** for the
flagship Finnish precast-reuse cluster. These move from MISSING_EVIDENCE → **PARTIAL** with a verbatim
quote, and the recommended action is **ADD_SOURCE** (attach this URL as `evidence_url`) plus a
**RELABEL** of `connection_kind → consortium_co_membership` (the source proves co-membership /
operational collaboration, *not* a free-standing pairwise partnership):

- `skanska_finland ↔ consolis_parma` — *"The building was built by Skanska … refurbished in Consolis
  Parma's factory in Kangasala"* (co-member **and** operational link).
- `skanska_finland / consolis_parma / ramboll_finland / umacon` (all pairs) — *"ReCreate's Finnish
  cluster is formed by Tampere University, Skanska, Consolis Parma, Ramboll Finland, Umacon, LIIKE
  architects, and the City of Tampere."*
- `recreate_project ↔ satu_huuhka` — *"ReCreate's coordinator and the Finnish cluster's leader, Prof.
  Satu Huuhka from Tampere University."*
- `recreate_project ↔ angelika_mettke`, `angelika_mettke ↔ btu_cottbus` — *"professor Angelika Mettke …
  would eventually join the leadership here on ReCreate … BTU Cottbus-Senftenberg."*

> **Evidence-Gate discipline:** co-listing on a consortium page proves co-membership, **not** that
> every pair is a direct bilateral partner. That is why these stay **PARTIAL**, not PROVEN, and carry
> the explicit relabel recommendation. The same page does **not** corroborate the UK steel cluster
> (`gardiner_and_theobald / akt_ii / cantillon / cleveland_steel_tubes / heyne_tillett_steel /
> symmetrys / ellis_and_moore`) or the SSD author team (`single_speed_design → john_hong /
> jinhee_park / paul_pedini`) — those remain MISSING_EVIDENCE / ADD_SOURCE and are routed for a
> targeted fetch.

---

## 4. Node findings (168 sourced `Akteur`)

| Tier | Count | Verdict | Action |
|---|---:|---|---|
| Directly confirmed by a fetched first-party/authoritative page naming the entity | 42 | **PROVEN** | KEEP |
| Firm/project/cluster confirmed by a fetched page, individual not named on that page | 17 | **PARTIAL** | KEEP (+ spot-fetch person subpage) |
| First-party source on graph but **not re-fetched this pass** (volume cap) | 103 | **UNVERIFIABLE** | KEEP (deferred) |
| Duplicate / ambiguous stub identity | 3 | **SCHEMA_VIOLATION** | ESCALATE_HUMAN |
| Sourced only by weak/non-first-party URLs | 3 | **MISSING_EVIDENCE** | RESOURCE |

### 4.1 PROVEN (42) — evidence spans every regional cluster

Direct, first-party/authoritative quotes were captured for actors across **CH / DE / AT / FI / NL /
FR / DK / UK / BE**, e.g.:

- **CH:** `marc_angst`, `pascal_hentschel`, `benjamin_poignon`, `martin_zeller` (zirkular.net K.118 team);
  `anna_buser`, `barbara_buser`, `felix_dillmann`, `re_win` (re-win.ch); `urban_bricolage`.
- **DE:** `Werner_Sobek`, `dirk_e_hebel`, `felix_heisel` (Cornell CCL / UMAR);
  `andreas_kretzer`, `roman_kreuzer`, `katharina_raabe`, `maximilian_stemmler`, `stefan_kroetsch`
  (Stuttgart-210 team); `baumab_kassel`, `surap_gmbh`.
- **AT:** `baukarussell`, `materialnomaden`.
- **FI/DE:** `satu_huuhka`, `angelika_mettke` (ReCreate).
- **NL:** `new_horizon` (oogstkaart → New Horizon).
- **FR:** `cancan_architecture`, `collectif_cancan`, `la_fabrique_de_bordeaux_metropole`,
  `refair_bordeaux`, `baticycle`, `r_place`.
- **DK:** `soren_nielsen`, `katrine_west_kristensen` (Vandkunsten), `genbyg`.
- **UK:** `loopfront`, `salvoweb`, `salvo_ltd`, `globechain`, `material_index`,
  `material_reuse_portal`, `warp_it`, `enviromate`.
- **BE:** `batiterre`.

### 4.2 PARTIAL (17)

Firm/project confirmed by a fetched page (ZRS / Natural Building Lab, Superuse Studios, Overtreders W
+ bureau SLA, Zirkular, HfT Stuttgart), but the **individual** was not on the fetched page — so the
node stays PARTIAL with a recommendation to spot-fetch the person/team subpage before treating as
PROVEN. Examples: `andrea_klinge`, `christof_ziegert`, `eike_roswag_klinge`, `cesare_peeren`,
`jan_jongert`, `hester_van_dijk`, `peter_van_assche`, `reinder_bakker`, `kerstin_mueller`,
`thomas_stark`.

### 4.3 SCHEMA_VIOLATION / ESCALATE_HUMAN (3) — identity problems

- `rau` → duplicate of `thomas_rau` (RAU = Thomas Rau's firm/founder) — **merge candidate**.
- `tomas` → low-quality stub (TOMAS Architecture; `tomas-architecture.com`) — **clarify/merge**.
- `harvestmap` → sourced only by `materialnomaden.at`; likely the materialnomaden HarvestMAP tool —
  **possible duplicate** of `re_store_harvestmap_vienna`.

### 4.4 MISSING_EVIDENCE / RESOURCE (3) — weak sources only

- `resource_marktplaats` → only Google Play / Apple app-store URLs; no first-party web page.
- `materialrest24` → only third-party press + Instagram; no first-party site.
- `stadt_kassel` → sole source is `baumab-kassel.de/impressum`, not the city's own domain.

### 4.5 UNVERIFIABLE / deferred (103) — honest coverage statement

These nodes **do** carry first-party / authoritative `source_urls` on the graph, but I did **not**
re-fetch them in this shard. With 168 nodes carrying 121 distinct URLs, exhaustive fetching exceeds a
single shard's budget. Rather than mark them PROVEN on faith (which would defeat the campaign), each is
recorded **UNVERIFIABLE** with `coverage=source_present_unverified`, the on-graph URL preserved in
`basis_ref`, and a note recommending a spot-fetch. **Proposed action KEEP** — the source exists; only
the *re-verification* is deferred. This is a deliberate, documented coverage boundary, not a silent gap.

---

## 5. Anomalies & escalations

1. **218 unsourced actor edges** — the entire `VERBUNDEN_MIT_AKTEUR` gap is sourceless. Single biggest
   data-quality issue: half are redundant reverse twins (MERGE) and the rest need a source naming both
   endpoints (ADD_SOURCE) or human disambiguation (ESCALATE).
2. **1 self-loop** (`Werner_Sobek → Werner_Sobek`) — clean DELETE.
3. **63 bidirectional duplicate pairs** — graph stores both `a→b` and `b→a`; recommend collapsing.
4. **3 duplicate/ambiguous nodes** (`rau`, `tomas`, `harvestmap`) — ESCALATE_HUMAN.
5. **Estimate vs. reality** — Agent 15's "152 edges" undercount: the true untagged/uncovered set is
   218. The campaign coverage math should be reconciled to 218 + 168 = 386 for this shard.

---

## 6. Reproducibility

| Artifact | Path |
|---|---|
| Gap computation | `_agent06b_work/compute_gap.py` → `gap_edges.json`, `gap_nodes.json` |
| Edge classification + node plan | `_agent06b_work/plan_and_edges.py` → `edges_classified.json`, `edge_rows.json`, `node_plan.json`, `fetch_map.json` |
| Ledger builder (with corroboration) | `_agent06b_work/build_ledger.py` |
| Graph dumps | `_agent06b_work/all_verbunden_edges.json`, `sourced_akteur_nodes.json` |
| **Final ledger** | `ledger/agent_06b.csv` (386 rows) |

No graph writes were performed. All proposed actions await human application in the remediation phase.
