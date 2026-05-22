# Post Quality Pass P6-04 — BETEILIGT_AN + UNVERIFIABLE + prog_mas_dfab

**Date:** 2026-06-06 · **Database:** `mit-bestand`
**Ledger:** [`ledger/post_quality_p06_04.csv`](../ledger/post_quality_p06_04.csv)
**Patch:** [`patches/post_quality_p06_04.patch.jsonl`](../patches/post_quality_p06_04.patch.jsonl)
**Apply:** applied

## Scope A — 5 Q5 PARTIAL BETEILIGT_AN (dossier recovery)

| New verdict | Count |
|---|---:|
| PROVEN | 5 |

## Scope B — fixable UNVERIFIABLE / DEAD_LINK (element ledger residuals)

Rows processed: **50**

| New verdict | Count |
|---|---:|
| UNVERIFIABLE | 26 |
| PROVEN | 24 |

## Scope C — prog_mas_dfab (A10-N-058 relabel)

- `A10-N-058`: PARTIAL→**PROVEN** (FIX_PROPERTY) — Coordinator and tutor of the MAS ETH Architecture and Digital Fabrication

## Upgrades to PROVEN: **30**

- `EP09-r-0003` (PARTIAL→PROVEN): albert_and_co — BETEILIGT_AN
- `EP09-r-0004` (PARTIAL→PROVEN): archipel_zero — BETEILIGT_AN
- `EP09-r-0010` (PARTIAL→PROVEN): greisch — BETEILIGT_AN
- `EP09-r-0011` (PARTIAL→PROVEN): iemb_tu_berlin — BETEILIGT_AN
- `EP09-r-0012` (PARTIAL→PROVEN): pirmin_jung_schweiz_ag — BETEILIGT_AN
- `A06B-node-0002` (UNVERIFIABLE→PROVEN): anders_lendager — Akteur
- `A06B-node-0003` (UNVERIFIABLE→PROVEN): andrea_kessler — Akteur
- `A06B-node-0012` (UNVERIFIABLE→PROVEN): archipel_sion_ressourcerie — Akteur
- `A06B-node-0013` (UNVERIFIABLE→PROVEN): articonnex — Akteur
- `A06B-node-0018` (UNVERIFIABLE→PROVEN): batrecup — Akteur
- `A06B-node-0021` (UNVERIFIABLE→PROVEN): baumatpool_ch — Akteur
- `A06B-node-0022` (UNVERIFIABLE→PROVEN): bauteilkatalog_immobilien_basel_stadt — Akteur
- `A06B-node-0023` (UNVERIFIABLE→PROVEN): bauteilverwertung_koeppel_klein — Akteur
- `A06B-node-0025` (UNVERIFIABLE→PROVEN): btvz_zuerichsee_oberland — Akteur
- `A06B-node-0026` (UNVERIFIABLE→PROVEN): building_spares_market — Akteur
- `A06B-node-0028` (UNVERIFIABLE→PROVEN): carla_ferrando_costansa — Akteur
- `A06B-node-0033` (UNVERIFIABLE→PROVEN): christine_conix — Akteur
- `A06B-node-0035` (UNVERIFIABLE→PROVEN): clara_simay — Akteur
- `A06B-node-0037` (UNVERIFIABLE→PROVEN): corentin_fivet — Akteur
- `A06B-node-0038` (UNVERIFIABLE→PROVEN): cornermat_retrival — Akteur
- `A06B-node-0039` (UNVERIFIABLE→PROVEN): cycle_zero — Akteur
- `A06B-node-0040` (UNVERIFIABLE→PROVEN): daniel_hoffmann — Akteur
- `A06B-node-0042` (UNVERIFIABLE→PROVEN): dominik_campanella — Akteur
- `A06B-node-0043` (UNVERIFIABLE→PROVEN): duncan_baker_brown — Akteur
- `A06B-node-0052` (UNVERIFIABLE→PROVEN): gebruiktebouwmaterialen — Akteur
- `A06B-node-0055` (UNVERIFIABLE→PROVEN): ggzatwork_laden2_bauteile_zug — Akteur
- `A06B-node-0056` (UNVERIFIABLE→PROVEN): gian_trachsler — Akteur
- `A06B-node-0063` (UNVERIFIABLE→PROVEN): hiltbrunner_reuse_riedtwil_wiederverwendung — Akteur
- `A06B-node-0068` (UNVERIFIABLE→PROVEN): julia_krafft — Akteur
- `A10-N-058` (PARTIAL→PROVEN): prog_mas_dfab — Programm

## Apply log (tail)

```
e: This feature is deprecated and will be removed in future versions.} {description: The query used a deprecated function. ('id' has been replaced by 'elementId or consider using an application-generated id')} {position: line: 1, column: 70, offset: 69} for query: 'MATCH (a {id: $from_id})-[r:`BETEILIGT_AN`]->(b {id: $to_id}) RETURN id(r) AS rid_internal, a.id AS from_id, b.id AS to_id, type(r) AS rel_type, properties(r) AS props'
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.FeatureDeprecationWarning} {category: DEPRECATION} {title: This feature is deprecated and will be removed in future versions.} {description: The query used a deprecated function. ('id' has been replaced by 'elementId or consider using an application-generated id')} {position: line: 1, column: 70, offset: 69} for query: 'MATCH (a {id: $from_id})-[r:`BETEILIGT_AN`]->(b {id: $to_id}) RETURN id(r) AS rid_internal, a.id AS from_id, b.id AS to_id, type(r) AS rel_type, properties(r) AS props'
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.FeatureDeprecationWarning} {category: DEPRECATION} {title: This feature is deprecated and will be removed in future versions.} {description: The query used a deprecated function. ('id' has been replaced by 'elementId or consider using an application-generated id')} {position: line: 1, column: 23, offset: 22} for query: 'MATCH ()-[r]-() WHERE id(r) = $rid SET r += $props'

```
