# Verifier Agent 06 — Cross-border / pan-European edges

**Database:** `mit-bestand` (READ-ONLY — only `read-cypher`/`get-schema` + `WebFetch`/`WebSearch` used; no graph mutation)
**Date:** 2026-06-06
**Scrutiny level:** HIGHEST — this is the exact edge class where all 29 fabrications occurred.
**Ledger:** [`ledger/agent_06.csv`](../ledger/agent_06.csv) (17 rows)

---

## 1. Scope recap & enumeration

My work-set is every `VERBUNDEN_MIT_AKTEUR` edge that (a) carries
`review_run='cross_bubble_extension_2026_06_06'`, OR (b) connects two actors that belong to
**different country clusters**, plus a mandated **regression scan** for any surviving
`*_peer` / `*_mesh` / `*_ecosystem` / `european_*` `connection_kind`.

**Country clusters** were derived from reuse-bubble membership (node `land` is null on almost
all actors), mapping `swiss→CH, germany→DE, france→FR, netherlands→NL, rotor_dc→BE`, plus the
`cross_bubble_extension` hubs.

| Scope segment | Edges |
|---|---:|
| `review_run='cross_bubble_extension_2026_06_06'` | 11 |
| Cross-country edges (not in the extension run) — all FR→BE, all to Opalis | 5 |
| Regression-scan hit (`*_peer`, intra-DE) | 1 |
| **Total processed** | **17** |

Determinism note: the cross-bubble run currently holds **11** live edges (planning-time
estimate was 12; the residual was reduced by the earlier tier-1/tier-2 removals). The
cross-country scan over **all** `VERBUNDEN_MIT_AKTEUR` returned only the 5 FR→BE Opalis edges —
confirming that the previously-deleted cross-border mesh edges (restado↔opalis, restado↔useagain,
the Dutch mesh, concular↔madaster, etc.) have **not** resurrected.

---

## 2. Counts by verdict

| Verdict | Count |
|---|---:|
| PROVEN | 15 |
| UNSUPPORTED | 2 |
| PARTIAL / DEAD_LINK / UNVERIFIABLE / other | 0 |

Proposed actions: **KEEP 15**, **DELETE 2**.

Every item was fetched live (`fetched=true`, all `http_status=200`). No paywalled or dead
links in this shard.

---

## 3. Regression-scan result (the explicit mandate)

Scan query matched `connection_kind` containing/ending `peer`, `mesh`, `ecosystem`, or starting
`european_`. **Exactly one edge survives graph-wide:**

- `bauteilboerse_bremen → bauteilboerse_hannover` · `bauteilnetz_peer_exchange` (intra-DE).
  The cited `bauteilnetz.de` page is the **network's own member directory** and lists *both*
  Bremen and Hannover as members of Bundesverband bauteilnetz Deutschland e.V. → direct evidence
  names both endpoints → **NOT a regression; PROVEN/KEEP.**

**Zero** `european_*`, `*_mesh`, or `*_ecosystem` pairwise edges remain. The purge from the
cross-bubble evidence audit held. ✅

---

## 4. The 2 worst findings (residual fabrications missed by earlier passes)

Both surviving `cross_bubble_extension` edges that assert **HdM DBU Reallabor research
consortium** membership for **`kunst_stoffe_ev`** fail the strict Evidence Gate. They escaped the
prior audit because their `connection_kind` (`hdm_research_consortium`) does **not** match the
purged `*_peer/_mesh/_ecosystem/european_*` vocabulary — but they are the **same failure mode**:
co-location in the Haus der Materialisierung dressed up as a formal consortium tie, with a URL
that names only one endpoint.

**Finding 1 — `kunst_stoffe_ev → material_mafia` (`hdm_research_consortium`) → UNSUPPORTED → DELETE**
- Cited URL `tu.berlin/circulareconomy/forschung/hdm` lists *Projektpartner: Material Mafia,
  Zusammenkunft Berlin e.V., Circular Berlin*. **Kunst-Stoffe is not named.**
- Corroboration: `dbu.de/projektdatenbank/35122-01` and `hausdermaterialisierung.org` both name
  the DBU consortium as **TU Berlin + ZUsammenKUNFT Berlin (ZKB) + Material Mafia + Circular City**.
- Kunst-Stoffe e.V. is an HdM **co-tenant** running the separate *Zentrum für klimaschonende
  Ressourcennutzung* — it is **not** a partner in the DBU research consortium. Claim contradicted.

**Finding 2 — `circular_berlin → kunst_stoffe_ev` (`hdm_research_consortium`) → UNSUPPORTED → DELETE**
- Same URL names **Circular Berlin** (an actual consortium partner) but **not Kunst-Stoffe**.
- The genuinely supportable consortium pairs (e.g. `circular_berlin ↔ material_mafia`) are *not*
  the edge that was drawn; the edge was instead wired to `kunst_stoffe_ev`, which the source does
  not place in the consortium.

> Recommendation: DELETE both. If a Kunst-Stoffe↔HdM tie is wanted, it must be **re-sourced** and
> **re-typed** as a co-tenancy/HdM-actor relationship (e.g. `hdm_co_tenant`), *not* a research
> consortium, with a URL that names Kunst-Stoffe (e.g. `hausdermaterialisierung.org` lists the
> Zentrum under Kunst-Stoffe's leadership).

---

## 5. The verified backbone (15 PROVEN, KEEP)

All confirmed by fetching the live page; each names **both** endpoints or is one endpoint's own
curated listing of the other:

- **brussels_environment → opalis** — Opalis/about: "Rotor by Brussels Environment as part of the
  Renolution strategy" (PREUSE maintenance funder). ✅
- **bellastock → opalis** — Opalis/about: "Since 2019, the cooperative Bellastock has joined the
  project. They updated the section on French salvage dealers". ✅ (FR→BE)
- **immobel → rotordc** and **rotordc → whitewood** — rotordb.org OXY Centre Monnaie:
  "acquired by property developers Whitewood and Immobel … Rotor was asked to join the project". ✅
- **insert_marketplace → madaster** — madaster.com: "Insert … and Madaster Services signed a
  partner agreement". ✅
- **madaster → madaster_epea** — madaster.com: "EPEA and Madaster have joined forces … Linking the
  EPEA material and product database to the Madaster Platform". ✅ (cross-border NL↔DE; EPEA GmbH
  is German, part of Drees & Sommer).
- **concular → software_restado** — restado imprint: "restado ist eine Marke der Concular GmbH". ✅
- **cirkla → sumami** — cirkla.ch's own `/annuaire/experts/sumami/` directory page. ✅
- **circular_hub_zurich → sumami** — circularhub.ch use-case article on sumami. ✅
- **eth_zuerich → sumami** — ETH page: "Together with ETH Zurich, methods are being developed …
  Sumami … is a start-up …". ✅
- **association_reavie / backacia / cycle_up / mineka → opalis** — each is that dealer's own Opalis
  supplier directory page (`opalis.eu/fr/fournisseurs/<x>`); `supplier_listing` correctly typed. ✅
  (4 × FR→BE)
- **bauteilboerse_bremen → bauteilboerse_hannover** — bauteilnetz.de member directory lists both. ✅

---

## 6. Anomalies & notes for the Aggregator

1. **Two residual category-inference fabrications** (`kunst_stoffe_ev` HdM edges) survived because
   they wear a credible-sounding `connection_kind`. Recommend the campaign add a check beyond the
   `*_peer/_mesh/_ecosystem/european_*` vocabulary: **any** consortium/partnership edge whose
   `evidence_url` does not name one endpoint must be flagged, regardless of `connection_kind` wording.
2. **No cross-border mesh resurrection.** The deleted Dutch mesh, restado↔opalis/useagain, and
   concular↔madaster edges are confirmed absent from the live graph.
3. **`supplier_listing` model is sound:** the FR→BE dealer→Opalis edges are each backed by the
   dealer's own Opalis directory entry — the correct place for the "co-listed in Opalis" fact (as
   the prior audit recommended), not as fabricated dealer-to-dealer partnerships.
4. **Country attribution caveat:** clusters were derived from bubble membership because node-level
   `land` is populated on only ~5 actors. `madaster_epea` is classed NL via its parent but is in
   fact a German entity (EPEA GmbH); its single cross-bubble edge is verified regardless.

---

## 7. Items escalated to human

None. The 2 UNSUPPORTED edges have a clear proposed action (`DELETE`, optionally `RESOURCE`+`RELABEL`
as HdM co-tenancy). No paywalled/ambiguous items required escalation.

---

### One-paragraph summary

Of 17 in-scope cross-border / cross-bubble `VERBUNDEN_MIT_AKTEUR` edges, **15 are PROVEN/KEEP** and
**2 are UNSUPPORTED/DELETE**. The regression scan is clean — only one `*_peer` edge survives
graph-wide (intra-DE `bauteilnetz_peer_exchange`), and it is legitimately backed by the network's
own member directory; zero `european_*`/`*_mesh`/`*_ecosystem` pairwise edges remain. **The single
most important finding:** the two surviving `hdm_research_consortium` edges touching
`kunst_stoffe_ev` (`→ material_mafia` and `circular_berlin →`) are residual fabrications of the same
category/co-location type that triggered this campaign — the TU Berlin DBU page (and DBU/HdM
corroboration) names the consortium as TU Berlin + ZUsammenKUNFT + Material Mafia + Circular City and
**never names Kunst-Stoffe**, which is merely an HdM co-tenant. They slipped past the earlier purge
only because their `connection_kind` was not in the purged peer/mesh/ecosystem vocabulary.
