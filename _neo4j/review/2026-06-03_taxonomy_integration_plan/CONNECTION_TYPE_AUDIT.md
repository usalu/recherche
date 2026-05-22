# Connection-Type Audit — what gets deleted vs migrated

**Generated:** 2026-06-03
**Source:** [analyze_old_vocab_connections.py](analyze_old_vocab_connections.py) over the 2026-06-02 full-network export (2,603 nodes / 21,067 edges, anchored on `:Projekt`+`:Programm`).
**Full output:** [vocab_connection_analysis.txt](vocab_connection_analysis.txt).

This document supersedes the migrate-then-archive policy from the previous draft of [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md). The user's principle is:

> Batches are the source of truth. Old vocab nodes go away. No legacy labels in the graph. Only migrate connections from upstream node types that the batches do **not** re-supply — those would otherwise break.

So every old-vocab edge falls into exactly one of three buckets:

- **DELETE** — the batch re-supplies the same semantic edge from the same upstream type. Keeping the old one is duplication.
- **MIGRATE** — the upstream node type is not touched by the batches; the edge would otherwise dangle. Reattach to the new canonical, dedupe.
- **DELETE WITH PREJUDICE** — the upstream is the data-quality system itself (`:DataIssue`). Those issue records are themselves obsolete after integration; the issue has been resolved.

---

## Headline numbers (from 2026-06-02 full network export)

| Vocab | Active nodes | Total inbound edges | Outbound edges |
|---|---:|---:|---|
| `:Methode` | 13 | 665 | 0 |
| `:Aufbereitungsverfahren` | 33 (62 in baseline → 29 already pruned) | 473 | 47 (`BELEGT_IN` 25, `TYPISCH_BEI_MATERIAL` 22) |
| `:Ressourcenquelle` | 16 | 552 | 0 |
| `:WiederverwendungsArt` | 11 | 604 | 0 |
| `:Rueckbauverfahren` | 5 | 299 | 0 |

**Project coverage gap:** essentially zero. Every live `:Projekt` with old-vocab edges except 0–3 outliers is covered by batches.

| Vocab | Live projects with old edges | Not in batches | Real gap |
|---|---:|---:|---|
| `:Methode` | 80 | 1 (`p_umar_unit`) | **0** — UMAR IS in Batch 05 (matching artifact) |
| `:Aufbereitungsverfahren` | 75 | 3 | **0 real projects** + 2 `:Projekt`-mislabeled `prog_*` |
| `:Ressourcenquelle` | 84 | 4 | **0 real projects** + 3 `:Projekt`-mislabeled `prog_*` |
| `:WiederverwendungsArt` | 84 | 4 | same as above |
| `:Rueckbauverfahren` | 67 | 0 | clean |

`prog_re_use_hoefe`, `prog_reallabor_be_ware`, `prog_stuttgart_210` are nodes carrying `:Projekt` label but `prog_*` id — a data-quality issue (mislabeled :Programm). They have old-vocab edges that won't be re-supplied. **Migrate** those edges per the §"Mislabeled Projekt/Programm" rule below; do not delete in the project-coverage sweep.

**Conclusion: batches replace 100% of the genuine Bauteilgruppe→vocab and Projekt→vocab edges.** The delete-then-recreate strategy is safe.

---

## Live Ressourcenquelle ↔ batch Quelle semantic check

The previous audit (C1) claimed equivalence. Now verified with usage counts:

| Live `rq_*` (inbound) | Batch canonical |
|---|---|
| `rq_donorgebaeude` (240), `rq_donor_infrastruktur` (9) | `Externer_Spenderbau` |
| `rq_baustelle` (102) | splits to `Eigener_Bestand` / `Gleicher_Standort` depending on whether project = same building |
| `rq_bauteilboerse` (38), `rq_haendler` (25), `rq_lager` (60), `rq_supplier_stock` (3), `rq_materialstockpile` (4) | `Bauteilmarkt_oder_Lager` |
| `rq_borrowed_material_pool` (4) | `Leihgabe_oder_Service` |
| `rq_produktionsueberschuss` (40), `rq_reclaimed_stock` (3), `rq_surplus_stock` (2), `rq_construction_waste_stream` (2), `rq_demolition_waste_stream` (1), `rq_unbekannt` (14), `rq_unknown_documented_source` (5) | `Restposten_Abfall_Unbekannt` |

**Semantic axis:** identical (where the physical material came from).
**Granularity:** batches are strictly coarser. Live splits `Bauteilmarkt_oder_Lager` into market vs dealer vs stockpile; batches lump all three.

`rq_baustelle` is the only mildly ambiguous case (could map to `Eigener_Bestand` OR `Gleicher_Standort`) — but since batches re-supply this from row evidence, the ambiguity is resolved at the row level; we don't need to guess.

→ Decision (revised C1): **delete all 16 live `rq_*` nodes**, MERGE 6 new `rq_*` matching batch buckets with batch-canonical ids. Keep `:Ressourcenquelle` as the label and `HAT_RESSOURCENQUELLE` as the rel (those don't conflict with anything).

---

## The connection matrix (every edge, every action)

### `:Methode` (13 → 6 new canonical)

| Source label | Rel | Edges | Action | Why |
|---|---|---:|---|---|
| `:Bauteilgruppe` | `HAT_METHODE` | 397 | **DELETE** | Batches re-supply via `HAT_METHODE` on the Bauteilgruppe |
| `:Projekt` | `HAT_METHODE` | 194 | **DELETE** | Batches re-supply via `HAT_METHODE` on the Projekt (`NUTZT_METHODE` rows normalized to `HAT_METHODE`) |
| `:Akteur` | `HAT_METHODE` | 58 | **MIGRATE** | Batches don't model actor↔method. Would break "actor X uses urban mining" knowledge if deleted. |
| `:Software` | `HAT_METHODE` | 9 | **MIGRATE** | Software tools that implement methodologies — not in batches. |
| `:Software:Tool` | `HAT_METHODE` | 6 | **MIGRATE** | Same as `:Software`. |
| `:Norm` | `HAT_METHODE` | 1 | **MIGRATE** | Standard references a method — preserve. |
| `:DataIssue` | `CONCERNS` | ~621 | **DELETE WITH PREJUDICE** | Issue records about old `meth_*` are themselves obsolete. If a DataIssue ONLY concerns deleted vocab → delete the DataIssue too. If mixed → just delete the dangling CONCERNS edge. |

Migration target per old `meth_*` (see [SEMANTIC_CONFLICT_AUDIT.md §C2](SEMANTIC_CONFLICT_AUDIT.md#c2)):

| Old | → New canonical |
|---|---|
| `meth_urban_mining`, `meth_building_material_scouting` | `meth_urban_mining_und_scouting` |
| `meth_reuse_assessment`, `meth_pre_deconstruction_audit` | `meth_bestands_und_reuse_assessment` |
| `meth_form_follows_availability`, `meth_wiederverwendungskriterien` | `meth_verfuegbarkeitsbasiertes_design` |
| `meth_design_for_disassembly`, `meth_reversibilitaet` | `meth_reversibles_design` |
| `meth_reuse_ausschreibung`, `meth_zirkulaere_ausschreibung` | `meth_zirkulaere_beschaffung` |
| `meth_bauteilkatalogisierung`, `meth_materialinventur`, `meth_abrissmonitoring` | `meth_dokumentation_und_monitoring` |

### `:Aufbereitungsverfahren` (33 → 6 new canonical)

| Source label | Rel | Edges | Action | Why |
|---|---|---:|---|---|
| `:Bauteilgruppe` | `HAT_AUFBEREITUNG` | 411 | **DELETE** | Batches re-supply |
| `:Projekt` | `HAT_AUFBEREITUNG` | 22 | **DELETE** | Batches re-supply |
| `:ReuseRule` | `HAT_AUFBEREITUNG` | 40 | **MIGRATE** | Rule vocab references a processing step — preserve |
| `:DataIssue` | `CONCERNS` | ~676 | **DELETE WITH PREJUDICE** | Same logic as Methode |
| **OUT:** `:Aufbereitungsverfahren` → `:Material` | `TYPISCH_BEI_MATERIAL` | 22 | **MIGRATE + DEDUPE** | "this Aufbereitung is typically applied to that Material" — semantic association on the *outbound* side. New canonical inherits from collapsed nodes; MERGE dedupes. |
| **OUT:** `:Aufbereitungsverfahren` → `:Quelle:ResearchDocument` | `BELEGT_IN` | 25 | **MIGRATE + DEDUPE** | Evidence citations on old av_* — preserve on new canonical |

Migration target per old `av_*` (see [SEMANTIC_CONFLICT_AUDIT.md §C4](SEMANTIC_CONFLICT_AUDIT.md#c4)):

| Old | → New canonical |
|---|---|
| `av_reinigung`, `av_beton_anhaftungen_entfernen`, `av_glas_reinigung_entkitten`, `av_aluminium_reinigung_entdichtung`, `av_naturstein_reinigung_schleifen_zuschnitt`, `av_moertelentfernung_ziegel`, `av_lehm_sieben_mischen`, `av_hobeln_schleifen_holz`, `av_sandstrahlen`, `av_entrosten_korrosionsbehandlung`, `av_korrosionsschutz_beschichten`, `av_oberflaechenbehandlung_metall` | `av_reinigung_und_oberflaeche` |
| `av_zuschnitt`, `av_drahtglasschneiden`, `av_entmoertelung_von_fliesen`, `av_holz_zuschnitt_reparatur`, `av_betonfertigteil_saegen`, `av_mauerwerk_diamantsaegen_modul`, `av_stahl_zuschnitt_bohrung`, `av_daemmstoff_zuschnitt` | `av_zuschnitt_und_vereinzelung` |
| `av_qualitaetssicherung`, `av_holz_festigkeitssortierung`, `av_glas_pruefung_sortierung`, `av_betonfertigteil_tagging_sortierung`, `av_aluminiumfenster_pruefung_sortierung`, `av_holz_trocknung_feuchtekonditionierung` | `av_pruefung_sortierung_qs` |
| `av_reparatur`, `av_rekonditionierung`, `av_leuchten_refurbishment`, `av_fenster_refurbishment`, `av_aluminiumfenster_beschlag_dichtung` | `av_reparatur_und_refurbishment` |
| `av_remanufacturing`, `av_holzaufbereitung` | `av_remanufacturing_und_upcycling` |
| `av_verstaerkung` | `av_verstaerkung_und_schutz` |

### `:Ressourcenquelle` (16 → 6 new canonical with new ids)

| Source label | Rel | Edges | Action | Why |
|---|---|---:|---|---|
| `:Bauteilgruppe` | `HAT_RESSOURCENQUELLE` | 482 | **DELETE** | Batches re-supply |
| `:Projekt` | `HAT_RESSOURCENQUELLE` | 69 | **DELETE** | Batches re-supply |
| `:Materialdepot` | `HAT_RESSOURCENQUELLE` | 1 | **MIGRATE** | Materialdepot (`bw_*_stock`) is a material-stock node — preserve link |
| `:DataIssue` | `CONCERNS` | ~577 | **DELETE WITH PREJUDICE** | |

Migration target per old `rq_*`: see equivalence table above. New ids:
`rq_externer_spenderbau`, `rq_eigener_bestand`, `rq_gleicher_standort`, `rq_bauteilmarkt_oder_lager`, `rq_leihgabe_oder_service`, `rq_restposten_abfall_unbekannt`.

For `rq_baustelle` (the ambiguous one): default to `rq_eigener_bestand` during the Materialdepot migration. The 482 Bauteilgruppe edges are being deleted anyway, so we never have to disambiguate at the row level.

### `:WiederverwendungsArt` (11 → fully retired; axis split across `:Wiederverwendungsergebnis`/`:Wiederverwendungsort`/`:Methode`)

| Source label | Rel | Edges | Action | Why |
|---|---|---:|---|---|
| `:Bauteilgruppe` | `HAT_WIEDERVERWENDUNGSART` | 425 | **DELETE** | Batches re-supply on the correct split axis |
| `:Projekt` | `HAT_WIEDERVERWENDUNGSART` | 179 | **DELETE** | Same |
| `:DataIssue` | `CONCERNS` | ~624 | **DELETE WITH PREJUDICE** | |

No non-replaceable upstreams. `:WiederverwendungsArt` retires cleanly: every `wva_*` node hard-deleted, no migration to anything.

### `:Rueckbauverfahren` (5 → 6 new canonical)

| Source label | Rel | Edges | Action | Why |
|---|---|---:|---|---|
| `:Bauteilgruppe` | `HAT_RUECKBAUVERFAHREN` | 299 | **DELETE** | Batches re-supply |
| `:DataIssue` | `CONCERNS` | ~306 | **DELETE WITH PREJUDICE** | |

No non-replaceable upstreams. Of the 5 existing `rv_*`, 4 ids match batch canonicals exactly (`rv_selektiver_rueckbau`, `rv_ausbau_von_bauteilen`, `rv_demontage`, `rv_zerstoerungsarme_bergung`) and only `rv_betonfraesen` (4 inbound) needs replacement. Special handling:

- **Keep** the 4 matching `rv_*` nodes (delete all their edges, but keep the nodes; recreated content is identical).
- **Delete** `rv_betonfraesen` after edges are gone.
- **Add** `rv_schneidender_rueckbau` and `rv_integrierter_rueckbau_und_lagerung` (the 2 new canonical from the batches).

Result: 5 → 6 `:Rueckbauverfahren` nodes, exactly matching the batches.

---

## Mislabeled Projekt/Programm rule

The analysis revealed 3 nodes labeled `:Projekt` that carry `prog_*` ids (`prog_re_use_hoefe`, `prog_reallabor_be_ware`, `prog_stuttgart_210`). They have old-vocab edges and aren't in batches because the batches address `p_*` projects.

→ **Pre-flight fix:** detect any `(p:Projekt)` where `p.id STARTS WITH 'prog_'`. For each, either (a) **add** the missing `:Programm` label and **remove** `:Projekt` (data-quality fix, restoring the correct typing), or (b) leave as-is. Either way, their old-vocab edges follow the same MIGRATE rule we apply to `:Akteur` (since `:Programm` is not a replaceable upstream from the batches' perspective).

Recommend (a): correct the label first, then their old-vocab edges naturally fall under the `:Programm → vocab` non-replaceable migration path.

---

## DataIssue policy (3,824+ CONCERNS edges across all 5 vocabs)

Per user's "no legacy" instruction:

1. For each `:DataIssue` whose **only** outbound `CONCERNS` targets a to-be-deleted vocab node: **`DETACH DELETE`** the DataIssue.
2. For each `:DataIssue` with **mixed** targets (some still-alive, some about-to-be-deleted): delete only the dangling CONCERNS edges; the DataIssue node survives.
3. Audit count: report total DataIssue nodes deleted vs reduced. Should be in the 2,000–3,000 range based on the per-vocab CONCERNS totals.

This is consistent with the user's principle and prevents dangling CONCERNS edges (which Neo4j allows but would be a graph hygiene mess).

---

## Updated Phase 0 pre-flight scan list

The Phase 0.3 pre-deletion scan must enumerate, for each of the 5 vocab labels:

```cypher
MATCH (old)
WHERE old:Methode OR old:Aufbereitungsverfahren OR old:Ressourcenquelle
   OR old:WiederverwendungsArt OR old:Rueckbauverfahren
OPTIONAL MATCH (src)-[r_in]->(old)
WITH old, labels(src) AS src_labels, type(r_in) AS in_type, count(r_in) AS in_count
OPTIONAL MATCH (old)-[r_out]->(tgt)
WITH old, src_labels, in_type, in_count,
     labels(tgt) AS tgt_labels, type(r_out) AS out_type, count(r_out) AS out_count
RETURN old.id AS old_id, labels(old) AS old_labels,
       src_labels, in_type, in_count, tgt_labels, out_type, out_count
ORDER BY old.id, in_type, out_type;
```

Output goes to `_neo4j/review/2026-06-03_taxonomy_integration_plan/snapshot_pre_integration/pre_deletion_scan.json`. The migration sub-step Cypher (Phase 6.X) loads this scan to drive the precise reattachment per (old_id, upstream_type) pair.

---

## Summary table — what survives after integration

| Vocab | Old count | New count | Nodes hard-deleted | Edges migrated | Edges deleted |
|---|---:|---:|---:|---:|---:|
| `:Methode` | 13 | 6 | 13 | 74 | 591 + ~621 DataIssue |
| `:Aufbereitungsverfahren` | 33 | 6 | 33 | 40 inbound + 47 outbound | 433 + ~676 DataIssue |
| `:Ressourcenquelle` | 16 | 6 | 16 | 1 | 551 + ~577 DataIssue |
| `:WiederverwendungsArt` | 11 | 0 (label retired) | 11 | 0 | 604 + ~624 DataIssue |
| `:Rueckbauverfahren` | 5 | 6 | 1 (rv_betonfraesen) | 0 | 299 + ~306 DataIssue |

After integration the active graph contains, on the vocab axes:
- 6 `:Methode`
- 6 `:Aufbereitungsverfahren`
- 6 `:Ressourcenquelle`
- 0 `:WiederverwendungsArt` (label retired entirely)
- 6 `:Rueckbauverfahren`
- 6 `:Wiederverwendungsergebnis` (new)
- 6 `:Wiederverwendungsort` (new)

Plus all batch-supplied edges from `:Bauteilgruppe` and `:Projekt`, plus the 115 migrated non-Bauteilgruppe-upstream edges (Akteur/Software/Norm/ReuseRule/Materialdepot/Programm).
