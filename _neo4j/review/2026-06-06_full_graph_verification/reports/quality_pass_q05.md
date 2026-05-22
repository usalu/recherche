# Quality Pass Q5 — Actor/Participation + Aggregator

**Database:** `mit-bestand` · **Ledger:** [`ledger/quality_pass_q05.csv`](../ledger/quality_pass_q05.csv)
**Patch:** [`patches/quality_pass_q05.patch.jsonl`](../patches/quality_pass_q05.patch.jsonl)
**Apply:** applied

## Scope A — EP-09 non-PROVEN actor edges

| Prior verdict | Count |
|---|---:|
| MISSING_EVIDENCE | 9 |
| PARTIAL | 7 |

## Scope B — external claim residuals

Rows processed: **123** (DEAD_LINK, UNVERIFIABLE fixable subset, UNSUPPORTED, residual SCHEMA)

| New verdict | Count |
|---|---:|
| SCHEMA_VIOLATION | 47 |
| UNVERIFIABLE | 40 |
| PROVEN | 36 |

## Upgrades to PROVEN: 36 (ledger; 38 patched — 2 geo-token BETEILIGT_AN reverted)

**Scope A residual:** 5 PARTIAL + 9 MISSING `VERBUNDEN_MIT_AKTEUR` + 1 self-loop `NUTZT_SOFTWARE` (deleted). Strict two-endpoint gate failed for Superuse/ZRS/HarvestMAP team edges → **ESCALATE_HUMAN**.

**Reverted after apply:** `EP09-r-0011` / `EP09-r-0012` — tu.berlin/basel.ch matched shared geo token only, not actor+project.

- `AG01-r-0019` (DEAD_LINK→PROVEN): cirkla — VERBUNDEN_MIT_AKTEUR (Cirkla committee → ROTO-Reuse)
- `agent07-rel-0708` (DEAD_LINK→PROVEN): bw_ka13_existing_building — ERFORDERT_NACHWEIS
- `agent07-rel-0709` (DEAD_LINK→PROVEN): bw_ka13_existing_building — ERFORDERT_NACHWEIS
- `agent07-rel-0710` (DEAD_LINK→PROVEN): bw_lycee_block_3000 — ERFORDERT_NACHWEIS
- `agent07-rel-0711` (DEAD_LINK→PROVEN): bw_lycee_block_3000 — ERFORDERT_NACHWEIS
- `agent07-rel-0712` (DEAD_LINK→PROVEN): bw_lycee_block_6000 — ERFORDERT_NACHWEIS
- `agent07-rel-0713` (DEAD_LINK→PROVEN): bw_lycee_block_6000 — ERFORDERT_NACHWEIS
- `agent07-rel-0714` (DEAD_LINK→PROVEN): bw_multi_brouckere_tower — ERFORDERT_NACHWEIS
- `agent07-rel-0715` (DEAD_LINK→PROVEN): bw_multi_brouckere_tower — ERFORDERT_NACHWEIS
- `agent07-rel-0716` (DEAD_LINK→PROVEN): bw_rws_districtskantoor_terneuzen — ERFORDERT_NACHWEIS
- `agent07-rel-0717` (DEAD_LINK→PROVEN): bw_rws_districtskantoor_terneuzen — ERFORDERT_NACHWEIS
- `agent07-rel-0718` (DEAD_LINK→PROVEN): bw_suutarila_community_centre_donor — ERFORDERT_NACHWEIS
- `agent07-rel-0719` (DEAD_LINK→PROVEN): bw_suutarila_community_centre_donor — ERFORDERT_NACHWEIS
- `agent07-rel-0720` (DEAD_LINK→PROVEN): bw_werkhof_moeoeslistrasse — ERFORDERT_NACHWEIS
- `agent07-rel-0721` (DEAD_LINK→PROVEN): bw_werkhof_moeoeslistrasse — ERFORDERT_NACHWEIS
- `agent07-rel-0722` (DEAD_LINK→PROVEN): la_schadstofffreiheit — ERFORDERT_NACHWEIS
- `agent07-rel-1706` (DEAD_LINK→PROVEN): pn_biozid_screening — ERFUELLT_NACHWEIS
- `agent07-rel-1707` (DEAD_LINK→PROVEN): pn_chlorid — ERFUELLT_NACHWEIS
- `agent07-rel-1708` (DEAD_LINK→PROVEN): pn_pcp_lindan — ERFUELLT_NACHWEIS
- `agent07-rel-1709` (DEAD_LINK→PROVEN): pn_schadstoffanalyse — ERFUELLT_NACHWEIS
- `agent07-rel-1710` (DEAD_LINK→PROVEN): pn_schadstoffanalyse_beschichtung — ERFUELLT_NACHWEIS
- `agent07-rel-1711` (DEAD_LINK→PROVEN): pn_schadstoffanalyse_holz — ERFUELLT_NACHWEIS
- `agent07-rel-1712` (DEAD_LINK→PROVEN): pn_schadstoffanalyse_kitt — ERFUELLT_NACHWEIS
- … and 13 more

## Apply log (tail)

```
, offset: 22} for query: 'MATCH ()-[r]-() WHERE id(r) = $rid SET r += $props'
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.FeatureDeprecationWarning} {category: DEPRECATION} {title: This feature is deprecated and will be removed in future versions.} {description: The query used a deprecated function. ('id' has been replaced by 'elementId or consider using an application-generated id')} {position: line: 1, column: 23, offset: 22} for query: 'MATCH ()-[r]-() WHERE id(r) = $rid SET r += $props'
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.FeatureDeprecationWarning} {category: DEPRECATION} {title: This feature is deprecated and will be removed in future versions.} {description: The query used a deprecated function. ('id' has been replaced by 'elementId or consider using an application-generated id')} {position: line: 1, column: 23, offset: 22} for query: 'MATCH ()-[r]-() WHERE id(r) = $rid SET r += $props'
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.FeatureDeprecationWarning} {category: DEPRECATION} {title: This feature is deprecated and will be removed in future versions.} {description: The query used a deprecated function. ('id' has been replaced by 'elementId or consider using an application-generated id')} {position: line: 1, column: 23, offset: 22} for query: 'MATCH ()-[r]-() WHERE id(r) = $rid SET r += $props'

```
