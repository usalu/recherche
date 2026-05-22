# Verifier Agent 03 — Germany reuse cluster — Report

**Date:** 2026-06-06
**Database:** `mit-bestand` (READ-ONLY; only `read-cypher` + `WebFetch` used; no graph mutation)
**Ledger shard:** [`ledger/agent_03.csv`](../ledger/agent_03.csv)

## 1. Scope recap

Work-set enumerated by Cypher (no sampling):

1. **`review_run='germany_reuse_bubble_2026_06_05'`** relationships → **13** edges (all `VERBUNDEN_MIT_AKTEUR`).
2. **Germany-relevant `cross_bubble_extension_2026_06_06`** edges touching the German actor set → **5** edges
   (`concular→software_restado`, `circular_berlin→kunst_stoffe_ev`, `kunst_stoffe_ev→material_mafia`,
   `madaster→madaster_epea`, `insert_marketplace→madaster`). The last is cross-border (NL) and primary-owned by
   Agent 06; verified here because `madaster` is in my node scope.
3. **German cluster nodes** → **13** (`concular`, `software_restado`, `bauteilboerse_hannover`,
   `bauteilboerse_bremen`, `bauteilnetz_deutschland`, `haus_der_materialisierung`, `material_mafia`,
   `kunst_stoffe_ev`, `circular_berlin`, `tu_berlin`, `circular_structural_design`, `madaster`, `madaster_epea`).
4. **Legacy un-sourced `VERBUNDEN_MIT_AKTEUR`** edges touching those nodes (no `review_run`, only `id`+`confidence=0.6`)
   → **17** edges (mostly person↔org affiliations + a few reverse-direction duplicates).

**Total claims processed: 13 nodes + 35 relationships = 48.**

Confirmed the previously-purged fabrications do **not** resurrect: `concular→madaster`,
`concular→madaster_epea`, `bauteilboerse_bremen→concular` (Tier-1 removals in the cross-bubble
`EVIDENCE_AUDIT.md`) are absent from the surviving Germany set.

## 2. Counts by verdict

| Verdict | Nodes | Rels | Total |
|---|---:|---:|---:|
| PROVEN | 13 | 15 | 28 |
| PARTIAL | 0 | 3 | 3 |
| MISSING_EVIDENCE | 0 | 17 | 17 |
| UNSUPPORTED / DEAD_LINK / UNVERIFIABLE / CONTRADICTION / SCHEMA_VIOLATION | 0 | 0 | 0 |
| **Total** | **13** | **35** | **48** |

**Ledger row reconciliation:** 13 node rows + 18 evidence-bearing rel rows (incl. the cross-border
`insert_marketplace→madaster`, which is primary-owned by Agent 06) + 17 legacy un-sourced rel rows = **48 rows**.
The 3 PARTIAL are the Bremen↔Hannover peer edge and the two Kunst-Stoffe "consortium" cross-bubble edges.

Every Tier-A in-scope item has `fetched=true` with `http_status=200`. No dead links, no paywalls, nothing unverifiable.

## 3. Special checks (all requested facts confirmed)

- **Concular ↔ restado brand fact — PROVEN.** restado imprint:
  *"restado ist eine Marke der Concular GmbH und richtet sich ausschließlich an gewerbliche Käufer"*
  (`https://restado.de/hilfe/impressum/`). Also names GF Dominik Campanella + Julius Schäufele, Concular GmbH, Berlin.
- **restado / Bauteilbörse Hannover profile — PROVEN.** restado's own profile page
  *"Bauteilbörse Hannover - … im Baustoff-Shop | restado … Baustoffe von Bauteilbörse Hannover"*
  (`https://restado.de/profil/bauteilboerse-hannover/`). This grounds both `hannover→software_restado`
  and `hannover→concular`.
- **bauteilnetz lists Bremen + Hannover — PROVEN.** bauteilnetz's own partner directory names both
  *"## bauteilbörse bremen"* and *"## bauteilbörse hannover"* and states
  *"Die aufgeführten Bauteil-Börsen sind Partner des bauteilnetz Deutschland"*
  (`…/bauteilboersen.html`).
- **HdM consortium + operator links — PROVEN (with two refinements).** HdM info page names
  Kunst-Stoffe e.V. as *Projektleitung* of the Zentrum, and the DBU/Reallabor partners as
  *"Die ZKB eG, die Material Mafia, die Technische Universität Berlin sowie Circular City – Zirkuläre Stadt e.V."*.
  TU Berlin's own project page confirms the same consortium (Material Mafia, ZKB, Circular City, TU Berlin).

## 4. The 3 PARTIAL findings (downgrade, do not delete)

1. **`circular_berlin → kunst_stoffe_ev`** (cross_bubble, `hdm_research_consortium`). The cited URL
   (`tu.berlin/circulareconomy/forschung/hdm`) lists the consortium as ZKB, Material Mafia, TU Berlin,
   Circular City — **Kunst-Stoffe is not named as a Reallabor member** (it leads the separate *Zentrum*).
   Both are real HdM co-located actors, so the link is genuine but the "DBU consortium co-membership"
   framing overstates. → **RELABEL** to HdM co-location.
2. **`kunst_stoffe_ev → material_mafia`** (cross_bubble, `hdm_research_consortium`). Same defect: page names
   Material Mafia as Reallabor partner but **not** Kunst-Stoffe. Both are on-site at HdM (co-location real),
   but "partners in TU Berlin HdM Reallabor" overstates Kunst-Stoffe's role. → **RELABEL**.
3. **`bauteilboerse_bremen → bauteilboerse_hannover`** (`bauteilnetz_peer_exchange`). Both are proven
   co-members of bauteilnetz, but a *bilateral* Bremen↔Hannover relationship is inferred from a third
   party's (bauteilnetz's) network directory, not from a source either endpoint curates. Co-membership is
   solid; the bilateral peer-exchange is weaker. → **RELABEL** to network co-membership (the two
   `network_member` edges already capture each one's membership).

These are not fabrications of the cross-bubble type (the endpoints are genuinely related); they are
over-specific `connection_kind` labels that should be softened.

## 5. Anomalies / hygiene flags (forwarded to Aggregator + Agent 14)

- **17 legacy `VERBUNDEN_MIT_AKTEUR` edges carry no URL evidence** (only `id` + `confidence=0.6`).
  They are mostly org↔person affiliations. Several are **bidirectional duplicate pairs** that the dedup
  should have collapsed:
  - `circular_material_systems ↔ tu_berlin`
  - `circular_structural_design ↔ patrick_teuffel`
  - `georg_hubmann ↔ tu_berlin`
  - `madaster ↔ rau` **and** `madaster ↔ thomas_rau`
- **Duplicate person node:** `rau` vs `thomas_rau` (both → Madaster; Thomas Rau is the Madaster founder).
  → **MERGE_DUPLICATE** candidate.
- **Reverse-direction duplicate of a sourced edge:** `bauteilboerse_bremen → bauteilnetz_deutschland`
  (unsourced) duplicates the evidence-bearing `bauteilnetz_deutschland → bauteilboerse_bremen`.
- **Low-quality stub:** `concular → tomas` — node id `tomas` looks like an incomplete/legacy person node.
  → **ESCALATE_HUMAN**.
- **Recoverable affiliations:** three unsourced person edges are independently provable from pages I already
  fetched and can simply receive `ADD_SOURCE`:
  - `concular → dominik_campanella` (restado imprint names him GF of Concular GmbH),
  - `circular_structural_design → patrick_teuffel` (Green-AI Hub names "Patrick Teuffel, Circular Structural Design"),
  - `madaster → thomas_rau` (Madaster founder).
- **Minor source discrepancy (no action):** the German TU page states DBU funding; the English TU page
  (`/en/circulareconomy/research/hdm`) states BMBF funding for the same project. Consortium membership is
  identical on both; only the named funder differs. Not graph-affecting.

## 6. Items escalated to human

- `concular → tomas` (`A03-rel-0027`) — stub node `tomas`, no evidence; needs human identification or removal.

## 7. Summary

Of 48 Germany-cluster claims: **29 PROVEN** (all 13 nodes + 16 reuse-bubble edges, each with a verbatim
quote from a page that names the entity or both endpoints), **3 PARTIAL** (two Kunst-Stoffe "consortium"
cross-bubble edges where the cited TU page never names Kunst-Stoffe, plus the Bremen↔Hannover peer edge built
on third-party network co-listing — all → RELABEL, none deleted), and **17 MISSING_EVIDENCE** legacy
person/affiliation edges with no URL (several bidirectional duplicates + the `rau`/`thomas_rau` duplicate
node → dedup/RESOURCE/ADD_SOURCE, one → ESCALATE_HUMAN). **Zero UNSUPPORTED, zero dead links.** The
single most important finding: the Germany evidence backbone is solid and the previously-purged fabricated
edges have not resurrected — the only weak spots are over-specific consortium labels on the Kunst-Stoffe
cross-bubble edges, which should be downgraded rather than removed.
