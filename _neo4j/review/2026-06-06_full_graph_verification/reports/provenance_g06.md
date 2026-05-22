# Git Provenance Report — Agent G6

**Date:** 2026-06-06 · **Repo:** `e:\recherche` · **HEAD:** `ed1d81d9`  
**Ledger:** [`ledger/provenance_g06.csv`](ledger/provenance_g06.csv) (27 rows)  
**Scope:** 5 `CONTRADICTION` element rows · 17 malformed `verdict=200` (http_status leak) · column-shift root-cause trace

---

## 1. Executive summary

| Class | Count | Introducing agent/shard | CSV bug? |
|---|---:|---|:---:|
| **CONTRADICTION** (geo `LIEGT_IN_STADT`) | **5** | Agent **09** (`_agent_09_build.py` → `ledger/agent_09.csv`) | No — valid findings |
| **`verdict=200` http_status leak** | **17** | Final Cleanup **F04** (`ledger/final_cleanup_f04.csv`) | **Yes** |
| **Other column-shift shards** | **2 + 2 clusters** | Agents **13**, **14**; remediation **R01**, **R03** | Yes (cosmetic) |

The **17 malformed `verdict=200` rows** called out in F10 (`FINAL_COVERAGE_PROOF.md` §4) are **not** present in the canonical `VERIFICATION_LEDGER_ELEMENT.csv` after F09 merge (Python `csv.DictReader` reads correct verdicts). They **do** reproduce when parsing the **F04 shard** literally: an extra empty column on node rows shifts `http_status=200` into the `verdict` slot.

**Column-shift bug owner (primary):** Final Cleanup Agent **F04** — all 18 Scope-B actor re-proof rows written with `from_id,,,Akteur` (one comma too many). **17/18** misparsed rows show `verdict=200`; **F04-node-0014** (`gxn`, `fetched=false`) misparses to blank `verdict`.

**Secondary column-shift sources** (campaign source shards, caught by Agent 15): Agent **13** `A13-node-pn-0001` (comma in `basis_ref`); Agent **14** `A14-INV-007` (commas in invariant text); remediation ledgers **R01**/**R03** (extended column layouts).

---

## 2. CONTRADICTION rows (5) — graph provenance

All five are Agent **09** `LIEGT_IN_STADT` checks (`09-lis-*`). They are **legitimate geo contradictions**, not ledger parse errors.

| claim_id | from → to | Issue |
|---|---|---|
| `09-lis-0006` | `bw_alte_kade_tiel` → `stadt_utrecht` | Address **Tiel**; edge says Utrecht |
| `09-lis-0078` | `bw_kerenzerbergtunnel` → `stadt_zuerich` | Address **Glarus**; edge says Zürich |
| `09-lis-0176` | `p_big_dig_building_boston` → `stadt_boston` | Address **Cambridge MA**; `stadt_cambridge_ma` exists |
| `09-lis-0190` | `p_circular_centre_netherlands_prinsenhof_a_reuse_pilot` → `stadt_arnhem` | Address **Heerde**; receiver at wrong Stadt |
| `09-lis-0204` | `p_haus_hos_mehrfamilienhaus_muehlhausen` → `stadt_leinefelde` | Address **Mühlhausen**; donor Leinefelde leaked |

### Git / intake chain

```mermaid
flowchart LR
  geo["2026-06-06_project_bg_geo_extract\nreuse_geo_graph.json / address_registry"]
  apply["apply_geo_import.py\ncommit ed1d81d9"]
  graph["mit-bestand LIEGT_IN_STADT edges"]
  a09["Agent 09 _agent_09_build.py"]
  ledger["agent_09.csv CONTRADICTION"]

  geo --> apply --> graph --> a09 --> ledger
```

| Stage | Artifact | Git |
|---|---|---|
| Geo property + `LIEGT_IN_*` backfill | `apply_geo_import.py` | `ed1d81d9` (2026-06-06) — **committed** |
| Address / donor-receiver pairing | `bauteilgruppe_projekt_addresses.csv`, `address_registry_draft.json` | same review folder |
| Verification adjudication | `_agent_09_build.py`, `ledger/agent_09.csv` | **untracked** (campaign workspace) |
| Element ledger | `VERIFICATION_LEDGER_ELEMENT.csv` | **untracked**; rows inherit `source_agent=09` |

**Root cause (graph):** multi-city dossier strings (`Boston;Cambridge`, `Arnhem;Heerde`, `Mühlhausen;Leinefelde`) and donor→receiver address propagation created `LIEGT_IN_STADT` edges to a **primary** `Stadt` node that disagrees with the node's `adresse` field. Agent 09's `CONTRA_OVERRIDE` dict explicitly encodes the first two cases.

**Remediation:** re-point or delete the five edges (see `reports/agent_09.md` §5) — **not** a ledger-CSV fix.

---

## 3. Malformed `verdict=200` (17 rows) — F04 shard

| Field | Detail |
|---|---|
| **Shard** | `ledger/final_cleanup_f04.csv` (18 Scope-B `Akteur` nodes, P6-04) |
| **Writer** | Final Cleanup Agent **F04** (2026-06-06) |
| **Bug** | Node rows: `{neo4j_eid},{node_id},,,Akteur` — **extra comma** before label → 18 parsed columns vs 17-header schema |
| **Symptom** | `http_status` value `200` lands in `verdict` column under strict positional parse |
| **F10 count** | **17** rows with `verdict=200` (excludes `F04-node-0014` where `fetched=false` yields blank misparsed verdict) |
| **Canonical ledger** | F09 merge wrote `VERIFICATION_LEDGER_ELEMENT.csv` with correct `PROVEN`/`PARTIAL`/`UNVERIFIABLE`; `graph_element_id` column holds true `elementId` |

Example (positional shift):

```
…,andreas_sonderegger,,,Akteur,…,true,200,PROVEN,…
                      ^ extra empty field
                              ^ misread as verdict when columns=18
```

---

## 4. Other column-shift shards (Agent 15 audit)

Documented in `COVERAGE_PROOF.md` §6 item 3 and `reports/agent_15.md`:

| Shard | Row | Agent | Root cause |
|---|---|---|---|
| `ledger/agent_13.csv` | `A13-node-pn-0001` | 13 | Comma inside `basis_ref` without quoting: `(pn_no_fulfill=0, pn_isolated=0)` |
| `ledger/agent_14.csv` | `A14-INV-007` | 14 | Commas in `asserted_claim` / `proof_quote` on invariant row |
| `ledger/remediation_r03.csv` | 27 rows | R03 | 23-column extended re-review layout |
| `ledger/remediation_r01.csv` | 5 rows | R01 | Trailing columns beyond 17-col schema |

These did **not** produce the F10 **17× `verdict=200`** metric; that metric is **F04-specific**.

---

## 5. Git history of ledger CSV writes

| Path | `git log --follow` | Notes |
|---|---|---|
| `VERIFICATION_LEDGER_ELEMENT.csv` | **no commits** | Untracked campaign output (F09 merge) |
| `ledger/final_cleanup_f04.csv` | **no commits** | F04 workspace artifact — **source of 17× shift** |
| `ledger/agent_09.csv` | **no commits** | Agent 09 campaign shard |
| `ledger/agent_13.csv`, `agent_14.csv` | **no commits** | 2-row shift bugs |
| `_agent_09_build.py` | **no commits** | Generator for agent_09 shard |
| `apply_geo_import.py` | `ed1d81d9` (2026-06-06) | Committed — introduces geo edges underlying CONTRADICTION |
| `VERIFICATION_LEDGER.schema.csv` | in repo plan commit | Schema reference only |

**Implication:** temporal provenance for ledger **writes** is anchored on **campaign artifact dates** (2026-06-06) and cross-references (F04 report, F09 merge log, Agent 15 aggregator), not git SHAs — same pattern as [G7 provenance](provenance_g07.md) §1.

---

## 6. Recommendations

1. **F04 / all ledger writers:** use `csv.DictWriter(..., quoting=csv.QUOTE_MINIMAL)`; node rows must be `element_id,from_id,,Label` (two commas, not three).
2. **Aggregators:** validate row width == schema width on ingest; reject or quarantine shards with `len(row) != len(header)`.
3. **CONTRADICTION geo:** apply graph patch to fix five `LIEGT_IN_STADT` edges (Agent 09 ESCALATE_HUMAN list) — separate from CSV hygiene.
4. **F10 doc:** clarify that 17× `verdict=200` refers to **F04 shard parse artifact**, not live ELEMENT ledger verdict counts.

---

## 7. Outputs

| File | Role |
|---|---|
| [`ledger/provenance_g06.csv`](ledger/provenance_g06.csv) | Row-level provenance (27 rows) |
| [`reports/provenance_g06.md`](reports/provenance_g06.md) | This report |
| [`_build_provenance_g06.py`](../_build_provenance_g06.py) | Regenerator |

*Agent G6 — read-only git + repo audit; no graph mutation.*
