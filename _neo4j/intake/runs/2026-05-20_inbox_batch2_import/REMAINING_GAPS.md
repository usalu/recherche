# REMAINING_GAPS — what's still open after batch2 v2 + Phase 16-27

**Audience:** Any agent (or human) picking up the work after the batch2 v2 import is closed out.
**Status as of writing (2026-05-20):** Graph at **2 580 nodes / 19 989 rels** in `mit-bestand`. All mandatory consistency checks return 0. No blocking gaps. Everything below is *optional* — either parked decisions, design-by-intent patterns, or research candidates for the next batch.

This is the companion to [HANDOFF.md](HANDOFF.md) and [CLEANUP_PLAN.md](CLEANUP_PLAN.md). Read HANDOFF first.

---

## §0 — How to re-derive the gap list yourself

Before relying on the numbers below, re-run the survey:

```bash
python _scripts/_gap_survey.py
```

This prints every consistency check with a value and an `OK`/`FAIL` marker for the ones that must be 0. If anything new shows `FAIL`, treat that as a regression and investigate before doing anything else.

The numbers in this file are a point-in-time snapshot from 2026-05-20 evening, after Phase 27 applied. They will drift if anyone adds nodes; verify before acting.

---

## §1 — Classification of remaining gaps

| Category | Count | What it is | Action |
|---|---:|---|---|
| **A — Parked KEEP-STUB orphans** | 1 | True deg-0 Akteur intentionally retained per PARKED_DECISIONS | Leave alone; revisit when evidence arrives |
| **B — Single-rolle Akteure** | ~332 | Akteure with only one HAT_AKTEURROLLE rel | Heuristic data quality; fix opportunistically as dossiers cover them |
| **C — Pre-batch2 BG optional vocab** | ~300 | Older Bauteilgruppen without the full 12 optional vocab rels | Research-heavy; do as part of the next batch |
| **D — Quelle URL duplicate groups** | 10 groups | Multiple Quelle nodes share a URL (per-actor citation design) | Intentional — NOT a bug; documented for context |
| **E — Single Projekt without LIEGT_IN_STADT** | 1 | `p_recrete_footbridge_reused_concrete_blocks` | Add Lausanne (EPFL) link after one quick verify |
| **F — Batch3 research candidates** | 6 streams | Whole new dossier scope (Oberkampf, Stuttgart reallabs 2-5, FCRBE 37 pilots, regional gaps) | Multi-session research; not in batch2 v2 scope |
| **G — Deferred schema decisions** | 4 items | E1 (label strip done), E3 (GEHÖRT_ZU rename), E5 (Region label), E6 (bt_belag) | Decide when triggered by a downstream consumer |

None of the above blocks any downstream consumer today. The graph is internally consistent.

---

## §2 — Gap A: The single parked Akteur orphan

### A.1 — `glasfischer_glastec` (deg = 0)

**Identity:** Swiss/German glass-tech company (real entity — searchable on web; not fictional).

**Where it came from:** KEEP-STUB Akteure list in [`_neo4j/review/round_002_followup/PARKED_DECISIONS.md`](../../../review/round_002_followup/PARKED_DECISIONS.md). It was kept across earlier rounds because no dossier evidence yet ties it to a specific project, but the entity itself is verified-real.

**Why it's still deg 0:**
- None of the 21 batch2 dossiers reference it.
- The other 3 deg-≤-1 KEEP-STUBs from earlier rounds (`heinrich_boell_stiftung`, `koimo_development`, `mehr_als_wohnen`) were linked in Phase 18, so this is the last survivor.

**Why not delete:**
- Deleting a verified-real entity loses information. If a future dossier mentions a glass-reuse contribution, we'd recreate it from scratch.
- Cost of keeping is one node (negligible).

**Survey query to find it:**
```cypher
MATCH (a:Akteur) WHERE NOT EXISTS { (a)-[]-() } RETURN a.id;
// expected: ['glasfischer_glastec']
```

**Action:** Leave alone. Add `BETEILIGT_AN` when a dossier mentions glass reuse (likely candidate: a future SMS Zürich follow-up dossier — SMS reused historic glazing).

**Estimated effort to close (when evidence arrives):** 1-2 add_rel ops in a future batch.

---

## §3 — Gap B: Akteure with only one HAT_AKTEURROLLE

### B.1 — Why this matters (slightly)

Roles in this graph are often multi-valued in reality (a person can be an architect AND a teacher AND a researcher). The current corpus assigns one role per Akteur by default; "extra" roles get added only when a dossier explicitly highlights the secondary role.

A count of ~332 Akteure with `size((a)-[:HAT_AKTEURROLLE]-()) = 1` is high but not surprising — most actors only get characterized once.

### B.2 — Survey

```cypher
MATCH (a:Akteur)
WITH a, size((a)-[:HAT_AKTEURROLLE]->()) AS rolle_count
WHERE rolle_count = 1
RETURN count(a);  // expected ~332
```

To find candidates for enrichment (Akteure that have evidence of multiple roles in dossiers but only one HAT_AKTEURROLLE):

```cypher
MATCH (a:Akteur)-[:BETEILIGT_AN]->(p)
WITH a, count(DISTINCT p) AS proj_count, size((a)-[:HAT_AKTEURROLLE]->()) AS rolle_count
WHERE proj_count >= 3 AND rolle_count = 1
RETURN a.id, proj_count;
```

Akteure that participate in 3+ projects with only 1 role are good enrichment candidates — they're likely cross-functional.

### B.3 — Action

Not a defect — design choice. Address opportunistically when:
- A new dossier explicitly assigns a different role to a known Akteur, OR
- Cross-projekt analysis is added and would benefit from richer role data.

**Not worth a dedicated phase.** Roll into the next dossier-driven batch.

---

## §4 — Gap C: Pre-batch2 BGs with incomplete optional vocab

### C.1 — Context

Batch2 v2 created 61 new Bauteilgruppen in Phase 6 + 12, with full optional vocab coverage (HAT_BESCHAFFUNGSWEG, HAT_VERBINDUNGSTECHNIK, HAT_PRUEFUNG, HAT_LEISTUNGSANFORDERUNG, HAT_MARKTMODELL, HAT_LOGISTIK, HAT_AUFBEREITUNG, HAT_RUECKBAUVERFAHREN, HAT_ZUSTANDSKLASSE, HAT_BAUPRODUKTSTATUS, NUTZT_MATERIAL, HAT_DEFEKT, HAT_SCHADSTOFF).

The other ~300 BGs in the graph (older corpus from rounds 000-001) have varying coverage. They satisfy the *mandatory* rels (HAT_BAUTEILEBENE, HAT_STATUS, HAT_RESSOURCENQUELLE, HAT_BAUTEILTYP, HAT_MATERIALGRUPPE, HAT_WIEDERVERWENDUNGSART, BELEGT_IN) — those are enforced — but optional vocab is patchy.

### C.2 — Survey: how patchy?

```cypher
MATCH (bg:Bauteilgruppe)
WITH bg, [
  EXISTS{(bg)-[:HAT_BESCHAFFUNGSWEG]->()},
  EXISTS{(bg)-[:HAT_VERBINDUNGSTECHNIK]->()},
  EXISTS{(bg)-[:HAT_PRUEFUNG]->()},
  EXISTS{(bg)-[:HAT_LEISTUNGSANFORDERUNG]->()},
  EXISTS{(bg)-[:HAT_MARKTMODELL]->()},
  EXISTS{(bg)-[:HAT_LOGISTIK]->()},
  EXISTS{(bg)-[:HAT_AUFBEREITUNG]->()},
  EXISTS{(bg)-[:HAT_RUECKBAUVERFAHREN]->()},
  EXISTS{(bg)-[:HAT_ZUSTANDSKLASSE]->()},
  EXISTS{(bg)-[:HAT_BAUPRODUKTSTATUS]->()},
  EXISTS{(bg)-[:NUTZT_MATERIAL]->()},
  EXISTS{(bg)-[:HAT_DEFEKT]->()},
  EXISTS{(bg)-[:HAT_SCHADSTOFF]->()}
] AS flags
WITH bg, [x IN flags WHERE x] AS present
RETURN
  CASE
    WHEN size(present) >= 10 THEN 'rich (10+)'
    WHEN size(present) >= 5  THEN 'medium (5-9)'
    WHEN size(present) >= 1  THEN 'sparse (1-4)'
    ELSE 'bare (mandatory only)'
  END AS coverage,
  count(*) AS bg_count
ORDER BY bg_count DESC;
```

Expected breakdown (approximate from earlier surveys):
- **rich (10+)**: ~80 BGs (the 61 batch2 v2 + ~19 pre-batch2 that were already richly annotated)
- **medium (5-9)**: ~150 BGs
- **sparse (1-4)**: ~100 BGs
- **bare**: ~30 BGs

### C.3 — Why this exists

Earlier rounds (000-001) seeded BGs from sparse evidence. The mandatory rels were enforced via Phase H/L; optional vocab was opportunistically added when dossiers had clear evidence. Most older BGs have no source dossier rich enough to derive all 13 optional rels.

### C.4 — Action

**Do not bulk-fill with defaults.** Filling HAT_PRUEFUNG with "unknown" or HAT_LOGISTIK with "n/a" creates fake data. Either:

1. **Wait for source dossier re-research** — when a future batch revisits a pre-batch2 project with a fresh dossier, enrich its BGs as part of that work.
2. **Targeted enrichment** — pick a single high-traffic BG (e.g., one referenced in 5+ Wiederverwendungsketten) and research its full vocab. Don't bulk-process.

### C.5 — Estimated effort to close

Hard to bound. If every pre-batch2 BG needs ~8 missing rels and you process 5 BGs per dossier session: ~60 dossier sessions. **Out of scope for any single batch — treat as ongoing.**

---

## §5 — Gap D: Quelle URL duplicate groups (intentional design pattern)

### D.1 — Why duplicates exist

The per-actor citation pattern means a single bibliographic source (e.g., a Rotor case study PDF) is referenced from multiple Akteure with their own `q_actor_<name>_<n>` Quelle node. The `url` property is the same, but the Quelle id is per-Akteur.

### D.2 — Survey

```cypher
MATCH (q:Quelle) WHERE q.url IS NOT NULL
WITH q.url AS url, collect(q.id) AS ids, count(*) AS n
WHERE n > 1
RETURN url, n, ids ORDER BY n DESC LIMIT 20;
```

Expected: ~10 URL groups with 2-5 Quelle nodes each.

### D.3 — Why NOT to dedupe

- Each per-actor Quelle carries `attributed_to_actor_id` (implicit via the Akteur it's BELEGT_IN'd to). Merging them loses provenance.
- The naming scheme `q_actor_<actor>_<n>` is explicitly per-actor (see [`_neo4j/review/round_002_followup/NAMING_AND_PROPERTIES_PLAN.md`](../../../review/round_002_followup/NAMING_AND_PROPERTIES_PLAN.md)).
- Frontend queries that ask "what does Rotor cite?" want to see Rotor's own Quelle list, not a deduped graph-wide list.

### D.4 — Action

**Leave alone.** Document the pattern in [HANDOFF.md §4](HANDOFF.md) (already done — Quelle row in the conceptual model table).

If a downstream consumer ever needs a canonical-URL view, build it as a query layer (Cypher view), not by collapsing the nodes.

---

## §6 — Gap E: One Projekt missing LIEGT_IN_STADT

### E.1 — The one Projekt

```cypher
MATCH (p:Projekt) WHERE NOT EXISTS { (p)-[:LIEGT_IN_STADT]->() } RETURN p.id, p.name;
```

Expected single row: `p_recrete_footbridge_reused_concrete_blocks` — the Re:Crete footbridge research-pilot Projekt (a 10 m pedestrian footbridge from reused concrete blocks, EPFL).

### E.2 — Why it's missing

The Re:Crete project is an EPFL research-pilot tied to the structural-xploration laboratory in Lausanne. The Projekt node was created in an earlier round before the Lausanne Stadt node existed in the graph, and was not patched in Phase 27 (which targeted batch2 BG projects).

### E.3 — Fix (single-edge patch, low risk)

```jsonl
{"op": "add_rel", "from": "p_recrete_footbridge_reused_concrete_blocks", "to": "stadt_lausanne", "type": "LIEGT_IN_STADT", "properties": {"source_scope": "derived", "id": "r_p_recrete_footbridge_reused_concrete_blocks__LIEGT_IN_STADT__stadt_lausanne"}}
{"op": "add_rel", "from": "p_recrete_footbridge_reused_concrete_blocks", "to": "land_schweiz", "type": "LIEGT_IN_LAND", "properties": {"source_scope": "derived", "id": "r_p_recrete_footbridge_reused_concrete_blocks__LIEGT_IN_LAND__land_schweiz"}}
```

**Prerequisites:**
- Verify `stadt_lausanne` exists (it does — earlier rounds).
- Verify `land_schweiz` exists (it does).
- Verify Lausanne is correct — the structural-xploration lab at EPFL is in Lausanne. The bridge prototype was built at the campus.

### E.4 — Action

This is a low-risk single patch. Defer to whoever runs the next batch — bundle with batch3. **Don't apply standalone** (overhead of a backup + apply cycle for 2 edges is not worth it).

---

## §7 — Gap F: Batch3 research candidates (multi-session research)

These need fresh dossier research and are out of scope for any followup to batch2 v2.

### F.1 — OBK_27 / Oberkampf social housing (Paris)

**Status:** The `p_obk_27` Projekt stub was deleted in Phase 1a-2 of batch2 v2 (the OBK_27 dossier turned out to be about a different research project that didn't have a built outcome at the time of writing).

**The OBK_27 dossier's leading candidate referent is Oberkampf social housing in massive stone (Paris) by Barrault Pressacco.** Two Akteure remain from that dossier:
- `cyril_pressacco` — currently linked only to `prog_fcrbe` via Phase 18
- `thibaut_barrault` — same

**Research needed:**
- Verify Oberkampf social housing is built (it should be — completed ~2023).
- Pull project details: BGs (massive stone façade), Bauwerk (the building itself), client, location (Paris XI).
- Create `p_oberkampf_paris` Projekt + `bw_oberkampf_paris` Bauwerk + actor links.

**Estimated effort:** 1 dossier (research + extraction + patch generation) ≈ 1 batch3 task.

### F.2 — Stuttgart 210 reallabs 2-5

**Status:** Phase 4a of batch2 v2 created `p_jugendtreff_ingersheim` as the **first** built reallab from the HTWG/Stuttgart 210 stockpile of 78 dismantled elements. The HTWG dossier mentions **four or five reallabs** in total — only the first is built.

**What's known (from the Stuttgart 210 dossier):**
- Reallab 1 = Jugendtreff Ingersheim — DONE (p_jugendtreff_ingersheim)
- Reallabs 2-5 = TBD — names, locations, statuses not in the current dossier.

**Research needed:**
- Track down updated Stuttgart 210 project page or HTWG publications listing the further reallabs.
- For each reallab that's been planned/built, create a child Projekt with `TEIL_VON_PROGRAMM → prog_stuttgart_210`.

**Estimated effort:** 1-2 dossier sessions per reallab; 4 reallabs ≈ 4-8 batch3 tasks.

### F.3 — FCRBE's 37 pilot operations

**Status:** The FCRBE programme (`prog_fcrbe`) is documented in the graph with a few named pilot Projekte. The FCRBE dossier mentions **37 pilot operations across NWE** total.

**Research needed:**
- Cross-check which of the 37 pilots are already in the graph (many may be in `_archive/research/` legacy material — but per AGENTS.md that's NOT canonical; verify against published FCRBE deliverables).
- For each pilot not yet in the graph, decide whether it has enough evidence to warrant a full Projekt or just an Akteur reference.
- Add `TEIL_VON_PROGRAMM → prog_fcrbe` for each.

**Estimated effort:** ~37 lookups × 5 min minimum = 3+ hours plus per-pilot Projekt creation when warranted. **Multi-batch.**

### F.4 — Regional dossier gaps

Geographic coverage today is centered on Switzerland + Belgium + Germany + Austria, with thin coverage elsewhere.

| Region | Current coverage | What's missing |
|---|---|---|
| **France** | REFAIR (deleted in batch2 — it's a platform, not a project), REBRIDGE (partner only), La Fabrique de Bordeaux Métropole as Akteur | Bellastock projects, La Fab pilot buildings, French Réemploi case studies, ICEB benchmark projects |
| **Iberia** | None | REBRIDGE has Coimbra partner; needs an actual Iberian project dossier |
| **Eastern Europe** | Ukraine added as Land in earlier round | No project dossier yet (war-context reconstruction is a thesis-adjacent angle) |
| **US / Canada** | Only Ecovative as supplier | No reuse-pilot projects |
| **Asia** | `stadt_kamikatsu` (Japan) exists with no dossier | Kamikatsu Zero Waste Center, Takeo project, etc. — unknown |

**Estimated effort:** Multi-session, per-region research. **Not a single batch3 task — an ongoing programme.**

### F.5 — Architecture-of-Reuse Brussels actor list (small win)

**Status:** The Projekt stayed as `cross_reference_stub` in batch2 v2 because the dossier says "identified_programme: no". Per [actor_extraction_per_dossier.md §15-§17](actor_extraction_per_dossier.md), the dossier names Rotor + RotorDC + CONIX RDBM + 3 Persons that should be linked.

**Why not done in batch2 v2:** Decision was to keep the stub as-is and skip actor enrichment since the underlying Projekt status was disputed.

**Fix (small, ~6 edges):**
```jsonl
{"op": "add_rel", "from": "Rotor", "to": "p_architecture_of_reuse_brussels", "type": "BETEILIGT_AN", "properties": {"rolle_text": "lead", "source_scope": "case_markdown", "id": "..."}}
// ... 5 more
```

Could be bundled with any small batch3 patch.

### F.6 — Vandkunsten + ZHAW Reuse in Construction actor enrichment

Same pattern as F.5 — Projekte stayed as `cross_reference_stub` but their dossiers name actors that should be linked. Total ~10 BETEILIGT_AN edges.

### F.7 — `bw_meduni_*` daughter Bauwerks (deferred during batch2 v2)

**Status:** MedUni Campus Mariannengasse Wien has multiple campus blocks (Block A, B, etc.). batch2 v2 created `bw_meduni_campus_mariannengasse` as a single Bauwerk; per-block daughter Bauwerks were deferred per dossier ambiguity.

**Research needed:** Verify campus has multiple constructionally-distinct buildings worth modeling separately. If yes, create child Bauwerks with `GEHÖRT_ZU → bw_meduni_campus_mariannengasse`. If no, leave as-is.

---

## §8 — Gap G: Deferred schema / tooling decisions

Same as [NEXT_STEPS_v2.md §E1, E3, E5, E6](NEXT_STEPS_v2.md), with current status:

### G.1 — E1: Strip `:Projekt` label from dual-labels — DONE

This was the original Phase 23 deferred item; it's now applied. Six nodes (`prog_fcrbe`, `prog_mas_dfab`, `prog_re_use_hoefe`, `prog_reallabor_be_ware`, `prog_rebridge`, `prog_stuttgart_210`) are `:Programm` only.

### G.2 — E3: Rename `GEHÖRT_ZU` → `GEHOERT_ZU` (still deferred)

**Pros:** Cleaner ASCII corpus; downstream tools (frontends, exports) avoid Unicode surprises.

**Cons:** 255+ rels to rewrite. Loss of German spelling fidelity (B2 decision was to **keep** umlauts).

**Current decision (B2):** KEEP umlauts. Don't rename.

**Trigger to revisit:** A downstream consumer (frontend, export pipeline, BI tool) chokes on Unicode in rel type names.

### G.3 — E5: Introduce `Region` label (defer)

**Status:** Defer until ≥10 region-level entities accumulate. Currently 2 (Brussels-Capital Region as Akteur; Nouvelle-Aquitaine unused).

**When to revisit:** If a future batch creates 8+ regional entities at once (e.g., a French regional réemploi dossier).

### G.4 — E6: Introduce `bt_belag` Bauteiltyp (defer)

**Status:** Currently all "Belag" (covering/finishing) slots use `bt_boden`. Adding `bt_belag` would let us distinguish floor-covering from structural floor.

**When to revisit:** If a future dossier needs the distinction (e.g., a parquet-reuse pilot where `bt_boden` is structural and `bt_belag` is the covering).

**Workaround in the meantime:** A `belag_oder_tragend` property on BG would work without a new vocab node.

### G.5 — `HAT_FUNKTIONSWECHSEL` rel type (DONE in Phase 26)

Originally flagged as E4. Phase 26 added the 7 inferred edges; survey now returns 0.

---

## §9 — Cross-reference: what's NOT in this file

These are documented elsewhere and should not be confused with "remaining gaps":

| Topic | Where it lives |
|---|---|
| What was applied, in what order | [APPLY_ORDER.md](APPLY_ORDER.md) + [rollback.md](../../../review/round_002_followup/rollback.md) |
| Live data state verified before patches | [pre_flight_validation.cypher](pre_flight_validation.cypher) + [pre_flight_results.json](pre_flight_results.json) |
| Issue catalog from batch2 v2 (C1-C15, O1-O14, F1-F27) | [CORRECTIONS_2026-05-20.md](CORRECTIONS_2026-05-20.md) |
| New vocab nodes from Phase 16 | [NEW_NODE_SUGGESTIONS.md](NEW_NODE_SUGGESTIONS.md) |
| All decisions (D1-D16, B1-B4) | [HANDOFF.md §7](HANDOFF.md) |
| Original pre-apply plan (now obsolete) | [PLAN.md](PLAN.md) (superseded by [PLAN_v2.md](PLAN_v2.md)) |
| Pre-apply NEXT_STEPS (now mostly obsolete; this file supersedes it) | [NEXT_STEPS_v2.md](NEXT_STEPS_v2.md) |

---

## §10 — Recommended next concrete actions (if any)

If a future agent asks "what's the smallest, highest-value thing I can do to close gaps?":

1. **Apply Gap E fix** (`p_recrete_footbridge` → Lausanne / Schweiz) — 2 edges, low risk. Bundle with batch3.
2. **Do F.5 + F.6** (Architecture-of-Reuse Brussels + Vandkunsten + ZHAW actor enrichment) — ~16 edges, low risk, closes pre-existing stubs.
3. **Define a Region-label trigger** (G.3) so future regional dossiers don't have to retro-fit.

If a future agent has 1 hour: do (1) + (2) above as a single small patch batch.

If a future agent has dossier-research time: pick **F.1 (Oberkampf Paris)** — highest-value single dossier because it rescues two stranded Akteure (`cyril_pressacco`, `thibaut_barrault`) and adds a real project to the France region.

---

## §11 — Re-verification checklist

After any of the above is applied, re-run the survey:

```bash
python _scripts/_gap_survey.py
```

Expected mandatory-zero rows (post-Phase 27):

```
  Nodes missing source_scope                                  0  OK
  r.id NULL                                                   0  OK
  Case-specific nodes missing BELEGT_IN                       0  OK
  BG missing HAT_BAUTEILEBENE                                 0  OK
  BG missing HAT_STATUS                                       0  OK
  BG missing HAT_RESSOURCENQUELLE                             0  OK
  BG missing HAT_BAUTEILTYP                                   0  OK
  BG missing HAT_MATERIALGRUPPE                               0  OK
  BG missing HAT_WIEDERVERWENDUNGSART                         0  OK
  Bauwerk missing HAT_STATUS                                  0  OK
```

If any of these flip to non-zero, that's a regression — diagnose before doing further work.

---

**End of REMAINING_GAPS.md.** Updated 2026-05-20.

Cross-references: [HANDOFF.md](HANDOFF.md), [CLEANUP_PLAN.md](CLEANUP_PLAN.md), [NEXT_STEPS_v2.md](NEXT_STEPS_v2.md), [rollback.md](../../../review/round_002_followup/rollback.md), [PARKED_DECISIONS.md](../../../review/round_002_followup/PARKED_DECISIONS.md).
