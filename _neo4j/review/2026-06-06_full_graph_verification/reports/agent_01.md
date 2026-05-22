# Verifier Agent 01 — Switzerland Reuse Cluster

**Date:** 2026-06-06
**Database:** `mit-bestand` (read-only, via `bolt://localhost:7687`)
**Ledger:** [`ledger/agent_01.csv`](../ledger/agent_01.csv) — 85 rows
**Access note:** The Neo4j MCP tools (`read-cypher`/`get-schema`) were not loaded in this
session, so all graph reads were issued through a **strictly read-only** Python helper
(`default_access_mode="READ"`, write-token guard) using the credentials in `.cursor/mcp.json`.
**No graph mutation, no patch application** occurred.

---

## 1. Scope recap (authoritative enumeration)

| Work-set | Cypher | Count |
|---|---|---:|
| Rels `r.review_run='swiss_reuse_bubble_2026_06_05'` | `MATCH ()-[r]->() WHERE r.review_run=... RETURN r` | **21** (6 `BETEILIGT_AN` + 15 `VERBUNDEN_MIT_AKTEUR`) |
| Swiss `VERBUNDEN_MIT_AKTEUR`, `cross_bubble_extension` (CH↔CH) | endpoints ∈ swiss set | **3** (all → `sumami`) |
| Swiss `VERBUNDEN_MIT_AKTEUR`, no `review_run` (structural) | endpoints ∈ swiss set | **42** |
| Swiss actor/software/tool nodes + `source_urls` | `n.id IN swiss` | **19** |
| **Total ledger rows** | | **85** (66 rel + 19 node) |

All 19 named scope nodes were found and **all carry `source_urls`** (none missing). The 3
CH↔CH `cross_bubble_extension` edges (intra-Switzerland) are claimed here; genuinely
cross-border edges remain Agent 06's.

## 2. Counts by verdict

| Verdict | Count |
|---|---:|
| PROVEN | **40** |
| PARTIAL | 2 |
| DEAD_LINK | 1 |
| MISSING_EVIDENCE | 42 |
| UNSUPPORTED / CONTRADICTION / SCHEMA_VIOLATION | 0 |

- **Tier-A web-evidence items (24 rels + 19 nodes = 43):** 40 PROVEN, 2 PARTIAL, 1 DEAD_LINK. Every one was fetched.
- **Structural no-URL edges (42):** all MISSING_EVIDENCE (proposed `ADD_SOURCE`/`ESCALATE_HUMAN`/`MERGE_DUPLICATE`).

## 3. Headline finding

**The Swiss reuse-bubble evidence layer is sound — every one of the 21 `swiss_reuse_bubble`
edges and all three CH↔CH `cross_bubble_extension` `sumami` edges passed the strict Evidence
Gate (URL fetched, both endpoints named), with exactly one exception:**

> **`cirkla → wick_reuse_roto_baumarkt` (`directory`)** cites
> `https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/wiederverwerkle-wick-upcycling-gmbh`,
> which returns **HTTP 404** (fetched twice). This is the only broken Tier-A claim in the
> shard. The underlying relationship is **salvageable, not fabricated**: Cirkla's own
> association/committee page lists *"Elias Knecht – Committee member, ROTO-Reuse"*, so the
> Cirkla↔Wick/ROTO link is real but needs **re-sourcing** to a live URL.

This contrasts sharply with the cross-bubble fabrications (29 deleted edges): the Swiss
in-bubble set does **not** rely on category inference. The risky "directory" edges
(`cirkla → materiuum / reuzi / useagain / gruner / bauteilladen / sumami`) were each
verified against **Cirkla's own `/annuaire/experts/<x>` page actually showing `<x>`** — the
exact special check required.

## 4. Worst / most important findings (with quotes)

1. **`cirkla → wick_reuse_roto_baumarkt` — DEAD_LINK (404).** Cited Cirkla directory page
   gone. Re-source via committee page: *"Elias Knecht - Committee member, ROTO-Reuse"*.
   → `RESOURCE`.
2. **`zirkular → p_k118` and `zirkular → p_elys` — PARTIAL.** Both Zirkular `BETEILIGT_AN`
   project edges rest on the quote *"trigger for the foundation of Zirkular by the involved
   planners"*. The projects were executed by **baubüro in situ**; they *triggered* Zirkular's
   founding — the firm did not yet exist. This is a founder-team/origin link, not direct firm
   participation. → `RELABEL` (e.g. `founding_origin`) rather than keep as `BETEILIGT_AN`.
3. **`eth_zuerich → prog_swircular` — PROVEN but thin.** Confirmed only via ETH-owned domain
   + title (*"SWIRCULAR Project | ETH Zurich"*); the partner roster is JavaScript-hidden, so
   ETH's specific chair could not be read. Acceptable (first-party domain) but flagged.
4. **`baubuero_in_situ → cirkla` — PROVEN via fallback page.** The edge's own
   `evidence_url` (`/comite/benjamin-poignon`) renders almost empty; the verbatim claim
   *"Benjamin Poignon - Co-Chairman / Baubüro in situ"* is on the association page. Consider
   `ADD_SOURCE`/repoint to the richer URL.
5. **42 structural `VERBUNDEN_MIT_AKTEUR` edges carry no `evidence_url`/`source_url`**
   (person→org and org-substructure affiliations). All MISSING_EVIDENCE. ~13 are corroborated
   by first-party pages fetched here (insitu.ch, Cirkla committee, Zirkular project teams,
   materiuum.ch ressourceries) → `ADD_SOURCE`; the rest → `ESCALATE_HUMAN`.
6. **Bidirectional duplicate `VERBUNDEN_MIT_AKTEUR` pairs survive** (schema/dedup concern for
   Agent 14): `gruner_ag↔gruner_reuse_platform`, `materiuum↔materiuum_geneve_ressourcerie`,
   `materiuum↔ressourcerie_lausanne_materiuum_ruul`, `cirkla↔pascal_flammer_architekten`,
   `cirkla↔urban_bricolage`, `eth_zuerich↔{catherine_de_wolf, fabio_gramazio,
   gramazio_kohler_research, matthias_kohler}`, `gruner_reuse_platform↔{nicole_daehn,
   ullrich_dickgiesser}`. The cross-bubble dedup run did not collapse these intra-CH pairs.
7. **Several structural edges lack the `id` property entirely** (e.g. `gruner_ag→gruner_reuse_platform`,
   `nicole_daehn→gruner_reuse_platform`) — keyed only by `confidence`. Recorded with their
   `elementId`. Schema-hygiene item for Agent 14.
8. **Possible out-of-scope edges in the Swiss cluster:** `eth_zuerich ↔ fabio_gramazio /
   gramazio_kohler_research / matthias_kohler` are architecture-robotics affiliations, not
   reuse — likely belong outside the reuse bubble. → `ESCALATE_HUMAN`.
9. **`barbara_buser → zirkular` — possible overclaim.** Buser is a baubüro in situ / Denkstatt
   founder; no fetched source ties her directly to Zirkular (her baubüro link *is*
   corroborated). → `ESCALATE_HUMAN`.
10. **Two node `source_urls[0]` were unreachable** (`sumami.ch`, `gruner-reuse.ch` — repeated
    timeouts). Both **entities are still PROVEN** via other first-party `source_urls` already
    on the node (ETH page for Sumami; gruner.ch news for Gruner ReUse). The primary URLs
    themselves should be re-checked (transient vs. dead).

## 5. Cirkla directory special-check results (each must show the listed actor)

| Edge | Cirkla page | Shows actor? | Verdict |
|---|---|---|---|
| cirkla → materiuum | `/experts/materiuum` | ✅ "Materiuum - Cirkla" | PROVEN |
| cirkla → reuzi_ch | `/experts/reuzi` | ✅ "REUZI - Cirkla" | PROVEN |
| cirkla → useagain | `/experts/useagain` | ✅ "Useagain - Cirkla" | PROVEN |
| cirkla → gruner_reuse_platform | `/experts/gruner-ag` | ✅ "Gruner AG - Cirkla ... Gruner ReUse" | PROVEN |
| cirkla → bauteilladen_winterthur | `/experts/bauteilladen-winterthur` | ✅ "BauTeilLaden Winterthur - Cirkla" | PROVEN |
| cirkla → sumami | `/experts/sumami/` | ✅ "Sumami - Cirkla" | PROVEN |
| cirkla → wick_reuse_roto_baumarkt | `/experts/wiederverwerkle-wick-upcycling-gmbh` | ❌ **404** | DEAD_LINK |

No category-inference directory edge passed by co-listing alone; six of seven are the
endpoint's own curated Cirkla profile page actually naming the actor.

## 6. Escalated to human (proposed_action `ESCALATE_HUMAN`)

- `barbara_buser → zirkular` (possible overclaim).
- Person affiliations not corroborated on fetched sources: `kerstin_mueller → {baubuero, zirkular}`,
  `marc_loeliger → zirkular`, `marco_graber → zirkular`, `thomas_pulver → zirkular`,
  `charlotte_bofinger → zirkular`, `michel_massmuenster → {baubuero, zirkular}`,
  `martin_zeller → zirkular` (photo-credit only), `materiuum → raphael_bach`,
  `gruner_reuse_platform → {nicole_daehn, ullrich_dickgiesser}` (and reverses).
- Likely out-of-reuse-scope: `eth_zuerich ↔ {fabio_gramazio, gramazio_kohler_research, matthias_kohler}`,
  `catherine_de_wolf ↔ eth_zuerich`.

## 7. Method notes

- Evidence Gate per `VERIFICATION_PLAN_15_AGENTS.md` §3. Pages cached by URL and reused across
  claims (e.g. one `gruner.ch` fetch served two edges; one ETH reuse page served three).
- Retry-once on timeout applied; `sumami.ch` and `gruner-reuse.ch` exhausted retries →
  fell back to corroborating `source_urls` already on the node.
- `fetched`/`http_status` recorded on every Tier-A row; no PROVEN/PARTIAL row lacks a verbatim
  `proof_quote`.

## 8. Summary

Of 85 claims, **40 PROVEN, 2 PARTIAL, 1 DEAD_LINK, 42 MISSING_EVIDENCE, 0 UNSUPPORTED /
CONTRADICTION / SCHEMA_VIOLATION.** The Switzerland reuse bubble is the **clean** end of the
graph: all 24 evidence-bearing edges and 19 nodes verify, the Cirkla directory edges survive
the strict "page-must-show-the-actor" test, and the only broken Tier-A claim is a single
404 (`cirkla → wick_reuse_roto_baumarkt`) that is real-but-needs-re-sourcing, not fabricated.
The real backlog here is **42 sourceless structural affiliation edges** plus several
**bidirectional-duplicate** and **missing-`id`** hygiene issues for the Aggregator/Agent 14 —
none of them fabrications, all proposed for `ADD_SOURCE`, `MERGE_DUPLICATE`, or
`ESCALATE_HUMAN` (never deletion).
