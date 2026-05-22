# What's Happening — Plain-Language Integration Summary

**One page.** This is the simple version of [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) + [CONNECTION_TYPE_AUDIT.md](CONNECTION_TYPE_AUDIT.md).

Four tags throughout:

- **[NEW]** — comes from the new batches (creating it for the first time)
- **[KEEP]** — already in the live graph, stays as-is
- **[DELETE]** — already in the live graph, getting hard-deleted (gone)
- **[REROUTE]** — already in the live graph, edge gets pointed at the new canonical (node it was attached to disappears; the connection survives)

---

## TL;DR — the whole change in one paragraph

The batches give us evidence-backed mappings for 81 projects across 7 dimensions of reuse (component, outcome, origin, location, method, dismantling, processing). The old graph has 5 vocab labels covering those dimensions in a messier way. We **keep the labels** (`:Methode`, `:Ressourcenquelle`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`), **delete the old node contents** (because batches are the source of truth), **create new canonical nodes** matching what the batches say, and **add 2 brand-new labels** (`:Wiederverwendungsergebnis`, `:Wiederverwendungsort`). The old `:WiederverwendungsArt` label retires entirely — its meaning is split across the new dimensions. The 2,478 edges from `:Bauteilgruppe` and `:Projekt` to old vocab get **deleted** (batches re-supply them). The 162 edges from upstream types that batches *don't* cover (Akteur, Software, Norm, ReuseRule, Materialdepot, Programm, plus 47 outbound from `:Aufbereitungsverfahren`) get **rerouted** to the new canonical so nothing breaks.

---

## What stays untouched

These graph structures are not part of the integration. **[KEEP]** as-is.

- `:Projekt` nodes (86) — already use `p_*` slugs that match batches
- All 350 live `:Bauteilgruppe` nodes — full property bag and non-vocab edges preserved (see Bauteilgruppe section below for handling of slug overlaps)
- All labels not listed below (Akteur, Bauwerk, Material, Materialgruppe, Bauteiltyp, Bauteilebene, Bauweise, Beschaffungsweg, Marktmodell, Geschaeftsmodell, Logistik, Huerde, Schadstoff, Quelle/ExternalLink/ResearchDocument, Land, Stadt, Dossier, …)
- The label `:Quelle` (2,956 nodes per fresh export) — this is the **evidence/citation** label (URLs, research docs). Confusing name, but unrelated to material origin. Stays.
- The 4 `rv_*` ids that already match batch canonicals (`rv_selektiver_rueckbau`, `rv_ausbau_von_bauteilen`, `rv_demontage`, `rv_zerstoerungsarme_bergung`)

---

## Per-vocab breakdown

### `:Methode` — methodology / approach

Live now: 13 nodes (`meth_form_follows_availability`, `meth_reuse_assessment`, `meth_urban_mining`, etc.). Old vocab is too generic and lacks row-level evidence.

| Item | Tag | Detail |
|---|---|---|
| Label `:Methode` | [KEEP] | Same label, same `HAT_METHODE` rel name |
| All 13 old `meth_*` nodes | [DELETE] | Hard-delete after edges resolved |
| `meth_urban_mining_und_scouting`, `meth_bestands_und_reuse_assessment`, `meth_verfuegbarkeitsbasiertes_design`, `meth_reversibles_design`, `meth_zirkulaere_beschaffung`, `meth_dokumentation_und_monitoring` | [NEW] | 6 new canonical from batches |
| 397 `:Bauteilgruppe → :Methode` edges | [DELETE] | Batches re-supply at row level |
| 194 `:Projekt → :Methode` edges | [DELETE] | Batches re-supply project-wide |
| 58 `:Akteur → :Methode` edges | [REROUTE] | Akteurs aren't in batches; preserve the link |
| 9 `:Software → :Methode` + 6 `:Software:Tool → :Methode` | [REROUTE] | Tools that implement methods |
| 1 `:Norm → :Methode` | [REROUTE] | Standard references method |
| ~621 `:DataIssue -[CONCERNS]→ :Methode` | [DELETE] | Issue records about retired vocab are themselves obsolete; trim or delete the DataIssue |

**Reroute mapping (old → new):**
- `meth_urban_mining`, `meth_building_material_scouting` → `meth_urban_mining_und_scouting`
- `meth_reuse_assessment`, `meth_pre_deconstruction_audit` → `meth_bestands_und_reuse_assessment`
- `meth_form_follows_availability`, `meth_wiederverwendungskriterien` → `meth_verfuegbarkeitsbasiertes_design`
- `meth_design_for_disassembly`, `meth_reversibilitaet` → `meth_reversibles_design`
- `meth_reuse_ausschreibung`, `meth_zirkulaere_ausschreibung` → `meth_zirkulaere_beschaffung`
- `meth_bauteilkatalogisierung`, `meth_materialinventur`, `meth_abrissmonitoring` → `meth_dokumentation_und_monitoring`

---

### `:Aufbereitungsverfahren` — processing / treatment

Live now: 33 nodes (`av_reinigung`, `av_zuschnitt`, `av_drahtglasschneiden`, etc.). Detailed but unevidenced.

| Item | Tag | Detail |
|---|---|---|
| Label `:Aufbereitungsverfahren` | [KEEP] | Same label, same `HAT_AUFBEREITUNG` rel |
| All 33 old `av_*` nodes | [DELETE] | Hard-delete after edges resolved |
| `av_reinigung_und_oberflaeche`, `av_zuschnitt_und_vereinzelung`, `av_pruefung_sortierung_qs`, `av_reparatur_und_refurbishment`, `av_remanufacturing_und_upcycling`, `av_verstaerkung_und_schutz` | [NEW] | 6 new canonical from batches |
| 411 `:Bauteilgruppe → :Aufbereitungsverfahren` | [DELETE] | Batches re-supply |
| 22 `:Projekt → :Aufbereitungsverfahren` | [DELETE] | Batches re-supply |
| 40 `:ReuseRule → :Aufbereitungsverfahren` | [REROUTE] | ReuseRule vocab isn't in batches |
| 22 `:Aufbereitungsverfahren -[TYPISCH_BEI_MATERIAL]→ :Material` | [REROUTE + DEDUPE] | "this processing is typical for that material" — preserve onto new canonical; MERGE dedupes when several old nodes collapse to one |
| 25 `:Aufbereitungsverfahren -[BELEGT_IN]→ :Quelle:ResearchDocument` | [REROUTE + DEDUPE] | Evidence citations on old av_*; preserve on new |
| ~676 `:DataIssue -[CONCERNS]→ :Aufbereitungsverfahren` | [DELETE] | Obsolete |

**Reroute mapping (old → new):** see full table in [CONNECTION_TYPE_AUDIT.md §Aufbereitungsverfahren](CONNECTION_TYPE_AUDIT.md#aufbereitungsverfahren-33--6-new-canonical). Examples:
- `av_reinigung`, `av_sandstrahlen`, `av_entrosten_korrosionsbehandlung`, `av_glas_reinigung_entkitten`, … → `av_reinigung_und_oberflaeche`
- `av_zuschnitt`, `av_drahtglasschneiden`, `av_betonfertigteil_saegen`, `av_stahl_zuschnitt_bohrung`, … → `av_zuschnitt_und_vereinzelung`
- `av_qualitaetssicherung`, `av_holz_festigkeitssortierung`, `av_glas_pruefung_sortierung`, … → `av_pruefung_sortierung_qs`
- `av_reparatur`, `av_rekonditionierung`, `av_leuchten_refurbishment`, … → `av_reparatur_und_refurbishment`
- `av_remanufacturing`, `av_holzaufbereitung` → `av_remanufacturing_und_upcycling`
- `av_verstaerkung` → `av_verstaerkung_und_schutz`

---

### `:Ressourcenquelle` — material origin (the "Quelle" the user worried about)

Live now: 16 nodes (`rq_donorgebaeude`, `rq_baustelle`, `rq_bauteilboerse`, etc.). Same semantic axis as batch "Quelle"; live ids don't match batch canonicals.

| Item | Tag | Detail |
|---|---|---|
| Label `:Ressourcenquelle` | [KEEP] | Same label, same `HAT_RESSOURCENQUELLE` rel — no `:Herkunft` invented |
| All 16 old `rq_*` nodes | [DELETE] | Hard-delete; new ids match batch canonicals |
| `rq_externer_spenderbau`, `rq_eigener_bestand`, `rq_gleicher_standort`, `rq_bauteilmarkt_oder_lager`, `rq_leihgabe_oder_service`, `rq_restposten_abfall_unbekannt` | [NEW] | 6 new canonical from batches |
| 482 `:Bauteilgruppe → :Ressourcenquelle` | [DELETE] | Batches re-supply |
| 69 `:Projekt → :Ressourcenquelle` | [DELETE] | Batches re-supply |
| 1 `:Materialdepot → :Ressourcenquelle` | [REROUTE] | Materialdepot is a `bw_*_stock` material-stock node |
| ~577 `:DataIssue -[CONCERNS]→ :Ressourcenquelle` | [DELETE] | Obsolete |

**Reroute mapping (old → new):**
- `rq_donorgebaeude`, `rq_donor_infrastruktur` → `rq_externer_spenderbau`
- `rq_baustelle` → `rq_eigener_bestand` (default for ambiguous case)
- `rq_bauteilboerse`, `rq_haendler`, `rq_lager`, `rq_supplier_stock`, `rq_materialstockpile` → `rq_bauteilmarkt_oder_lager`
- `rq_borrowed_material_pool` → `rq_leihgabe_oder_service`
- `rq_produktionsueberschuss`, `rq_reclaimed_stock`, `rq_surplus_stock`, `rq_construction_waste_stream`, `rq_demolition_waste_stream`, `rq_unbekannt`, `rq_unknown_documented_source` → `rq_restposten_abfall_unbekannt`

---

### `:WiederverwendungsArt` — type of reuse (retires entirely)

Live now: 11 nodes. The old single axis mixed outcome, method, and location. Batches split this into three clean axes.

| Item | Tag | Detail |
|---|---|---|
| Label `:WiederverwendungsArt` | [DELETE] | Label retires entirely; constraint dropped |
| All 11 `wva_*` nodes | [DELETE] | Hard-delete |
| 425 `:Bauteilgruppe → :WiederverwendungsArt` | [DELETE] | Batches re-supply on the correct split axis |
| 179 `:Projekt → :WiederverwendungsArt` | [DELETE] | Same |
| ~624 `:DataIssue -[CONCERNS]→ :WiederverwendungsArt` | [DELETE] | Obsolete |

**No rerouting needed.** Every `wva_*` meaning is fully covered by one of the new axes (`:Wiederverwendungsergebnis`, `:Wiederverwendungsort`, or `:Methode`), and the batches supply those directly per row.

---

### `:Rueckbauverfahren` — dismantling method

Live now: 5 nodes. Already mostly matches batch canonicals.

| Item | Tag | Detail |
|---|---|---|
| Label `:Rueckbauverfahren` | [KEEP] | Same label, same `HAT_RUECKBAUVERFAHREN` rel |
| `rv_selektiver_rueckbau`, `rv_ausbau_von_bauteilen`, `rv_demontage`, `rv_zerstoerungsarme_bergung` | [KEEP] | Already match batch canonicals; ids stay |
| `rv_betonfraesen` (4 inbound) | [DELETE] | Folded into the new `rv_schneidender_rueckbau` |
| `rv_schneidender_rueckbau`, `rv_integrierter_rueckbau_und_lagerung` | [NEW] | 2 new canonical from batches |
| 299 `:Bauteilgruppe → :Rueckbauverfahren` | [DELETE] | Batches re-supply |
| ~306 `:DataIssue -[CONCERNS]→ :Rueckbauverfahren` | [DELETE] | Obsolete |

---

## Brand-new labels (no live equivalent)

### `:Wiederverwendungsergebnis` — what happened to the material

| Item | Tag |
|---|---|
| Label `:Wiederverwendungsergebnis` | [NEW] |
| `wver_bestandserhalt`, `wver_wv_gleiche_funktion`, `wver_wv_neue_funktion`, `wver_modul_oder_abschnittswv`, `wver_material_reprocessing`, `wver_geplant_oder_gelagert` | [NEW] 6 canonical seed nodes |
| Rel `HAT_ERGEBNIS` (`:Bauteilgruppe → :Wiederverwendungsergebnis`) | [NEW] |
| Constraint `wiederverwendungsergebnis_id` | [NEW] |

### `:Wiederverwendungsort` — where the material ended up

| Item | Tag |
|---|---|
| Label `:Wiederverwendungsort` | [NEW] |
| `wvo_in_situ`, `wvo_im_selben_gebaeude_versetzt`, `wvo_auf_demselben_standort_versetzt`, `wvo_extern_importiert`, `wvo_temporaer_oder_zurueckgegeben`, `wvo_gelagert_oder_unbekannt` | [NEW] 6 canonical seed nodes |
| Rel `HAT_WIEDERVERWENDUNGSORT` (`:Bauteilgruppe → :Wiederverwendungsort`) | [NEW] |
| Constraint `wiederverwendungsort_id` | [NEW] |

### `ANGEWENDET_AUF` — Methode applied to component

| Item | Tag |
|---|---|
| Rel `ANGEWENDET_AUF` (`:Methode → :Bauteilgruppe`) | [NEW] ~14 edges from batches |
| Constraint `rel_angewendet_auf_id` | [NEW] |

---

## Project-level fix (data quality)

| Item | Tag |
|---|---|
| 3 nodes labeled `:Projekt` with `prog_*` ids (`prog_re_use_hoefe`, `prog_reallabor_be_ware`, `prog_stuttgart_210`) | [REROUTE label] add `:Programm`, drop `:Projekt` |

After relabeling, their old-vocab edges follow the `:Programm → vocab` reroute path (same as Akteur/Software/Norm).

## Bauteilgruppe handling (FINAL — 2026-06-03)

Decision: **`:Bauteilgruppe` label is reserved for reused components (`bg_reuse_*` only).** Batches are canonical within that scope. Non-reuse prefixes (`bg_retained_*` / `bg_planned_*` / `bg_dismantled_*`) get hard-deleted — they're a different semantic dimension that doesn't belong to `:Bauteilgruppe`. Skip the manual resolver — auto-confirm `needs_review` pairs.

| Live BG bucket | Count | Tag | What happens |
|---|---:|---|---|
| Exact slug match, both `bg_reuse_*` | ~251 | [KEEP] + [MERGE evidence] | Same node; batch evidence MERGEs on top |
| Exact slug match, non-reuse prefix | 22 | [DELETE] | Out of `:Bauteilgruppe` scope; live node + matching batch rows dropped |
| `needs_review` pair `bg_reuse_*` (auto-confirmed) | 29 | [KEEP] + [MERGE evidence] | Live node stays, batch evidence attached |
| `bg_reuse_*` no batch match | 35 | [DELETE] | Replaced by batches' evidence-backed set |
| Non-reuse no batch match (retained/planned/dismantled) | 13 | [DELETE] | Out of `:Bauteilgruppe` scope |
| Batch `bg_reuse_*` new candidate | 24 | [NEW] | Created as new node with `bg_kind = partial_batch` |
| Batch non-reuse / `bg_candidate_*` new candidate | 4 | [SKIP] | Not imported (out of scope) |

**Net BG count: 350 − 35 (bg_reuse_ orphans) − 35 (non-reuse) + 24 (batch new) = 304** after integration. All survivors are `bg_reuse_*`.

**Phase 2 filter:** 85 batch rows (4.9% of 1,734) that anchor on non-`bg_reuse_*` BGs get filtered out. Examples dropped:
- ELEMENTA Brettstapel design intent (`bg_planned_*`)
- LysP8 DfD timber frame (`bg_planned_*`)
- Circl Tarkett C2C planned floor (`bg_planned_*`)
- Elys, Grande Halle, Botanique retained concrete structures (`bg_retained_*`)
- Circl dismantled larch structure (`bg_dismantled_*`)
- MedUni Mariannengasse retained Art Nouveau ceiling (`bg_retained_*`)

**Cost:** roughly 600–800 non-vocab edges + 70 property bags + 85 batch findings. Per [RICHNESS_AUDIT.md](RICHNESS_AUDIT.md), the deleted edges are predominantly `topology_synthesized` / `unklar` placeholders.

**Alternative if data preservation matters more:** relabel the 35 non-reuse live BGs to dedicated labels (`:Bestand` / `:GeplantesBauteil` / `:Dekonstruktion`) instead of deleting. Not the current plan.

**Slug-drift redirection in practice:** some of the 35 reuse-orphan deletions correspond to a batch-new pair (same physical component, different slug). Example:
- DELETE: `bg_reuse_mehrere_mehrere_bluecity_red_cedar_fensterrahmen_trennwaende` (live, generic slug)
- CREATE: `bg_reuse_glas_innenwand_bluecity_reused_window_frames` (batch, evidence-backed)

The Phase 3.2 resolver work ([BAUTEILGRUPPE_COMPARISON.md](BAUTEILGRUPPE_COMPARISON.md), [bauteilgruppe_id_map.csv](bauteilgruppe_id_map.csv), [RESOLVER_USAGE.md](RESOLVER_USAGE.md)) is preserved as informational; not required for execution.

---

## Property contract on every new or rerouted edge

Every edge created or rerouted in this run carries:

```
review_run         = 'taxonomy_integration_2026_06_03'
evidence_basis     = 'taxonomy_integration_2026_06_03'
evidence_confidence ∈ {belegt, wahrscheinlich, unsicher}   // HIGH→belegt, MEDIUM→wahrscheinlich, LOW→unsicher
evidence_url       = batch row's evidence_url (when present)
evidence_quote     = batch row's evidence_summary, truncated to 240 chars
created_at         = datetime()
```

Rerouted edges additionally carry:

```
legacy_methode_id           // or legacy_aufbereitung_id / legacy_ressourcenquelle_id
legacy_methode_name         // human-readable old name for forensic traceability
migrated_at                 = datetime()
```

---

## Before vs after — vocab axis shape

```
BEFORE                                      AFTER
:Methode                  13 nodes          :Methode                  6 nodes (all new)
:Aufbereitungsverfahren   62 nodes          :Aufbereitungsverfahren   6 nodes (all new)
:Ressourcenquelle         16 nodes          :Ressourcenquelle         6 nodes (all new)
:Rueckbauverfahren         5 nodes          :Rueckbauverfahren        6 nodes (4 kept + 2 new)
:WiederverwendungsArt     11 nodes          :WiederverwendungsArt     0 (label retired)
:Bauteilgruppe           350 nodes          :Bauteilgruppe           304 nodes (−35 bg_reuse_ orphans, −35 non-reuse, +24 batch-new)
                          —                 :Wiederverwendungsergebnis  6 nodes (brand new)
                          —                 :Wiederverwendungsort       6 nodes (brand new)
```

```
HAT_METHODE             665 edges  → ~298 (74 rerouted + ~224 from batches)
HAT_AUFBEREITUNG        473 edges  → ~283 (40 rerouted + ~243 from batches)
HAT_RESSOURCENQUELLE    552 edges  → ~380 (1 rerouted + ~379 from batches)
HAT_RUECKBAUVERFAHREN   299 edges  → ~136 (0 rerouted + ~136 from batches)
HAT_WIEDERVERWENDUNGSART 604 edges → 0 (rel retired)
HAT_ERGEBNIS              0 edges  → ~423 (all from batches)
HAT_WIEDERVERWENDUNGSORT  0 edges  → ~367 (all from batches)
ANGEWENDET_AUF            0 edges  → ~14  (all from batches)

TYPISCH_BEI_MATERIAL    (from :Aufbereitungsverfahren) 22 → ≤22 (rerouted, dedup)
BELEGT_IN               (from :Aufbereitungsverfahren) 25 → ≤25 (rerouted, dedup)
DataIssue.CONCERNS      ~3,824 across 5 vocabs → ~0 (DataIssues deleted or trimmed)
```

---

## Phase order — what runs when

| Phase | What | Touches graph? |
|---|---|---|
| 0 | Snapshot + pre-deletion scan + relabel `:Projekt`-with-`prog_*` | Read + tiny label fix |
| 1 | Decisions (done) | No |
| 2 | Normalize batch Markdown (alias rel-types, target labels) | No |
| 3 | Build [bauteilgruppe_id_map.csv](bauteilgruppe_id_map.csv) (resolver) | No |
| 4 | Create constraints + 6+6+6+6+2 new canonical seed nodes | Add only |
| 5 | Stage Cypher per batch, MERGE all evidence edges | Add only |
| 6 | Delete old vocab edges + nodes + DataIssues per [CONNECTION_TYPE_AUDIT.md](CONNECTION_TYPE_AUDIT.md) | Reroute + Delete |
| 7 | Run [verify_integration.cypher](verify_integration.cypher); must pass | Read only |

**Rollback:** Phase 4+5 edge by edge via `review_run` tag. Phase 6 is destructive — only path back is the Phase 0 database dump.
