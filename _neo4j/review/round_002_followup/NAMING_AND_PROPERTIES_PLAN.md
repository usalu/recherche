# Naming + property cleanup plan — graph-wide

> **✅ Migration completed 2026-05-19.** Phases L → M → N → O.0 → O.a → O.b → P → R all applied. Final state: 2 298 nodes / 17 035 relationships / 308 Bauteilgruppen. See [rollback.md](rollback.md) for what landed in each phase. The plan below is preserved as the migration's design document; the body is unchanged from the pre-execution version.

## 0. Execution context (read first if you're starting fresh)

**State at plan freeze:** 2 296 nodes / 16 822 relationships in Neo4j database `mit-bestand` (bolt://localhost:7687). Verify before starting any phase:

```cypher
MATCH (n) WITH count(n) AS nodes
MATCH ()-[r]->() WITH nodes, count(r) AS rels
RETURN nodes, rels;
// Expected: 2296 / 16822 (drift would mean someone applied something in between)
```

### Companion docs you'll want open

| File | Purpose |
|---|---|
| **[NAMING_AND_PROPERTIES_PLAN.md](NAMING_AND_PROPERTIES_PLAN.md)** *(this file)* | The plan — naming, properties, BG id rename |
| **[QUELLE_PLAN.md](QUELLE_PLAN.md)** | The source-coverage companion plan — schedule after Phase P |
| [CONFLICT_ANALYSIS.md](CONFLICT_ANALYSIS.md) | Pre-flight conflict scan; the 7 plan amendments are already baked in here |
| [rollback.md](rollback.md) | Ledger of every applied phase A–K + Round 003 with backup paths |
| [VERIFICATION_QUERIES.cypher](VERIFICATION_QUERIES.cypher) | 18 graph-output queries to sanity-check each phase post-apply |
| [EXPLORATION_QUERIES.cypher](EXPLORATION_QUERIES.cypher) | 20 rich-combination queries for exploring the live graph |
| [PARKED_DECISIONS.md](PARKED_DECISIONS.md) | 23 stub Projekte awaiting promotion (handled in `stub_research/`) |
| [STUB_AKTEUR_DECISIONS.md](STUB_AKTEUR_DECISIONS.md) | 16 stub Akteure (decisions written, removals deferred to future prompts) |
| [stub_research/README.md](stub_research/README.md) | 7 batched research prompts for the 23 stub Projekte |

Historical / audit-trail (don't act on, just read for context if needed): `phase_a_execution_plan.md`, `reuse_knowledge_map.md`, `reuse_schema_proposals.md`, `phase_k_audit_report.md`, `phase_g_*.json`, `belegt_in_*`, `vocab_*`, `deep_reuse_scan.json`.

### Apply-tool workflow

Every phase follows the same protocol (Phases A–K were all done this way; see [rollback.md](rollback.md) for examples):

1. **Backup** the live graph to `_neo4j/review/backups/<phase>_pre_apply/`:
   ```bash
   rm -rf _neo4j/review/backups/phase_X_pre_apply
   python _scripts/backup_neo4j_graph.py --out-dir _neo4j/review/backups/phase_X_pre_apply
   ```
2. **Generate** the JSONL patch under `_neo4j/review/round_002_followup/patches/phase_X.patch.jsonl` (write a small generator script under `_scripts/_generate_phase_X_patch.py`, commit-and-delete pattern).
3. **Dry-run** the patch — confirm op counts, zero errors:
   ```bash
   python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/round_002_followup/patches/phase_X.patch.jsonl --dry-run
   ```
4. **Live apply** with the explicit confirmation phrase:
   ```bash
   python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/round_002_followup/patches/phase_X.patch.jsonl --confirm "APPLY phase_X.patch.jsonl TO mit-bestand"
   ```
5. **Verify** with the relevant section of [VERIFICATION_QUERIES.cypher](VERIFICATION_QUERIES.cypher) — expected counts shown inline in comments.
6. **Update** [rollback.md](rollback.md) — append a new section using the existing template (before/after counts, ops table, rollback Cypher, capabilities unlocked).
7. **Commit** small batches with 3-word imperative subjects (`Apply Phase L`, `Add Quelle convention`, etc.), no AI co-author trailers, using `git -c core.longpaths=true add ... && git -c core.longpaths=true commit -m "..."`.

### Apply-tool ops reference (`_scripts/apply_neo4j_review_patch.py`)

Supported ops: `add_node`, `set_node_properties`, `canonicalize_node`, `set_property`, `add_rel`, `noop_reviewed`, `merge_node`, `delete_node`, `delete_rel`, `set_rel_properties`, `remove_node_properties`, `remove_rel_properties`, `rename_property`, `move_property`, `replace_rel_type`.

**Critical gotchas** (caught in [CONFLICT_ANALYSIS.md](CONFLICT_ANALYSIS.md)):

- `canonicalize_node` only sets `name` and `aliases`. It **does NOT rename the node id**. For id renames, use the **`add_node` → `merge_node`** sequence — see Phase O.a + O.b below. `merge_node` is the only op that rewrites outgoing `r.id` properties via `rewrite_id_outbound`.
- `set_node_properties` and `set_rel_properties` **overwrite** the named properties. For `aliases` (or any list-valued property) you must first read the current value and emit the union, otherwise existing entries are lost. Nodes with existing aliases today: `imd_raadgevende_ingenieurs`, `cleveland_steel_tubes`, `rotor_dc`, `duncan_baker_brown`, `p_lysp8_basel`, `p_eth_circular_construction_student_reuse`, `land_daenemark`.
- `remove_node_properties` takes a `properties: ["key1", "key2", …]` list — use this for Phase L hygiene drops.
- `rename_property` takes `{id, from, to}` for a node-scoped property rename — used in Phase L Quelle handling (`titel → name_full`).

### Phase ordering (recommended)

```
L (hygiene) → M (vocab name+name_full) → N (entity name+name_full) → O.a (BG add_node) → O.b (BG merge_node) → P (backfill)
              ──────────── do these first; lowest risk ────────────  ── biggest ──   ── final polish ──
```

`Q (Quelle gap)` is **deferred** — schedule after Q4 decision (whether to source structural-vocab labels).

### Conventions recap

- Commits: 3-word imperative subjects, no AI co-author trailers, no `--no-verify`, never push without explicit ask
- Always `git -c core.longpaths=true` when adding files under `_database/` or large json dumps
- No interactive git ops (no `-i` flags)
- Confirmation phrase for live apply must match the patch file name and database name exactly: `APPLY <patch-file-name> TO mit-bestand`

---

**Decision recorded:** the canonical `name` property becomes the **short caption** (≤ 25 chars where applicable). Neo4j Browser displays it as the node label by default, so no `:style` config is needed. Long descriptive text moves to a sibling property `name_full` where it has real value.

This document covers:
0. Execution context (read this first if starting a new chat)
1. The universal property convention (what every node label should carry)
2. Per-label property landscape (current state, 53 labels)
3. Per-label cleanup actions (Groups A–H)
4. **Quelle convention** — the two-channel source-tracking rule and current coverage
5. Concrete short-name tables for the labels where `name` is currently too long *(in §3 Groups C+D)*
6. The Bauteilgruppe id-restructuring convention (with amendments from [CONFLICT_ANALYSIS.md](CONFLICT_ANALYSIS.md))
7. A phased migration plan (Phases L → P plus deferred Phase Q for Quelle gaps)
8. Open questions


---

## 1. Universal property convention

Every node carries the same core. Type-specific properties live alongside.

| Property | Status | Purpose |
|---|---|---|
| `id` | **required** | machine handle / slug — globally unique |
| `name` | **required** | short caption shown in graph view, ≤ 25 chars where the label is normally long |
| `name_full` | optional | long descriptive form — only kept where it adds real information beyond `name` |
| `aliases` | optional, list | alternate names / spellings |
| `note` | optional | 1-line editor note |
| `scope_note` | **required on controlled-vocab labels** | definition: what this node means |
| `source_scope` | optional | provenance bucket (`actor_registry`, `case_markdown`, `controlled_vocab_seed`, `archive_scan`) |
| `source_file` | optional | specific source document |

Type-specific properties (e.g. `bewertung`, `flaeche_m2`, `co2_reduktion_pct` on Projekt; `country_iso2`, `standards_body` on Norm; `asbest_verbot_jahr` on Land) stay as they are — the universal core sits on top of them, not in place of them.

**Quelle is never a property.** Provenance is tracked through two dedicated channels — see Section 4 below. Don't put a Quelle reference into any of the properties above; it belongs on the `BELEGT_IN` edge or the rel's `r.source` property.

---

## 2. Current state — property landscape (53 labels)

| Label | Nodes | `name` 100%? | Median `name` length | Distinct props | Issue |
|---|---:|---:|---:|---:|---|
| **Akteur** | 582 | ✓ | 15 | 13 | OK length; clean `stars_ignored` leftover (85) |
| **Quelle** | 447 | **✗ 28.6 %** | 34 | 11 | `titel` is the actual short title; needs `titel → name_full` rename |
| **Bauteilgruppe** | 306 | ✓ | 39 | 136 | names too long; id convention needed |
| **Bauwerk** | 196 | ✓ | 38 | 46 | names often too long |
| **Projekt** | 99 | ✓ | 33 | **429** | quant props are per-project (expected); just shorten `name` |
| **Wiederverwendungskette** | 63 | ✓ | 51 | 10 | names too long |
| **Stadt** | 62 | ✓ | 9 | 3 | clean |
| **Aufbereitungsverfahren** | 45 | ✓ | 33 | 8 | stray `scope/topic/classified_at` on 1-2 nodes |
| **Norm** | 30 | ✓ | 42 | 15 | `name` = full title; needs short `name` (standard number) + `name_full` (title) |
| **Huerde** | 28 | ✓ | 19 | 2 | clean |
| **Akteurrolle** | 25 | ✓ | 23 | 4 | OK |
| **PruefungNachweis** | 20 | ✓ | 24 | 9 | stray intake props on 1-2 nodes |
| **Material** | 19 | ✓ | 7 | 8 | stray intake props on 1 node; OK length |
| **Programm** | 17 | ✓ | 15 | 12 | stray intake props |
| **Land** | 16 | ✓ | 10 | 10 | add `country_iso2` |
| **Bauproduktstatus** | 15 | ✓ | 47 | 3 | needs short `name` |
| **Bauteiltyp** | 15 | ✓ | 7 | 2 | clean |
| **Methode** | 13 | ✓ | 22 | 6 | stray intake props on 1 node |
| **Verbindungstechnik** | 12 | ✓ | 16 | 4 | OK |
| **Marktmodell** | 11 | ✓ | 24 | 3 | one outlier needs shortening |
| **Defekt** | 10 | ✓ | 29 | 3 | needs short `name` |
| **MatchingQualitaet** | 9 | ✓ | 37 | 3 | needs short `name` |
| **Akzeptanz** | 5 | ✓ | 36 | 3 | needs short `name` |
| **ZustandsKlasse** | 6 | ✓ | 40 | 3 | needs short `name` |
| **LebenszyklusModul** | 5 | ✓ | 50 | 3 | needs short `name` |
| _(other 28 small vocab labels)_ | — | mostly ✓ | ≤ 24 | ≤ 5 | mostly clean |

---

## 3. Per-label cleanup actions

### Group A — drop stray intake properties

These properties appear on 1-7 nodes and are leftover from earlier intake runs. They convey nothing useful and add noise to detail panels:

- `scope`, `topic`, `classified_at`, `not_yet_referenced_in_corpus`, `standards_body` on **Material, Methode, Aufbereitungsverfahren, PruefungNachweis, Programm**: drop on 1-7 affected nodes per label.
- `usage_project_count`, `usage_countries`, `usage_project_ids` on **Norm** (53 % coverage): these are derivable via Cypher whenever needed — drop them (≈ 16 nodes affected).
- `stars_ignored` on **Akteur** (85 nodes): drop — it was a stale CSV import column.
- `quelle_merge_note`, `quellen_konflikt_note` on **Projekt** (a couple of nodes): keep — these document real editorial decisions, just move to `note` if generic.

### Group B — rename + canonicalize Quelle

Today's three-state landscape (verified in CONFLICT_ANALYSIS.md B7):

| State | Count | Action |
|---:|---:|---|
| `name` only | 127 | length-check: if > 25 chars set `name_full = name` then derive short `name`; else keep |
| `titel` only | 319 | rename `titel` → `name_full`; derive short `name` from `name_full` or id |
| both `name` and `titel` (same value) | 1 | drop `titel` |
| neither | 0 | — |

Plus: unify `filename` (5 nodes) + `dateiname` (1) → existing `source_file` (320 nodes).

```cypher
// 1. titel-only nodes: rename titel → name_full
MATCH (q:Quelle) WHERE q.name IS NULL AND q.titel IS NOT NULL
SET q.name_full = q.titel
REMOVE q.titel;

// 2. derive short name where missing (≤ 25 chars from name_full, fallback to id)
MATCH (q:Quelle) WHERE q.name IS NULL
SET q.name = CASE
  WHEN q.name_full IS NOT NULL AND size(q.name_full) <= 25 THEN q.name_full
  WHEN q.name_full IS NOT NULL THEN substring(q.name_full, 0, 24) + '…'
  ELSE q.id
END;

// 3. name-already-long nodes (current name > 25): move to name_full, derive shorter
MATCH (q:Quelle) WHERE q.name IS NOT NULL AND size(q.name) > 25 AND q.name_full IS NULL
SET q.name_full = q.name,
    q.name = substring(q.name, 0, 24) + '…';

// 4. duplicate titel (= name) node: drop titel
MATCH (q:Quelle) WHERE q.titel IS NOT NULL AND q.name = q.titel
REMOVE q.titel;

// 5. filename / dateiname → source_file
MATCH (q:Quelle) WHERE q.filename IS NOT NULL AND q.source_file IS NULL
SET q.source_file = q.filename REMOVE q.filename;
MATCH (q:Quelle) WHERE q.dateiname IS NOT NULL AND q.source_file IS NULL
SET q.source_file = q.dateiname REMOVE q.dateiname;

// 6. verify
MATCH (q:Quelle) WHERE q.name IS NULL OR q.titel IS NOT NULL OR q.filename IS NOT NULL OR q.dateiname IS NOT NULL
RETURN count(q) AS still_dirty;  // expect 0
```

The short-name derivation is admittedly crude (truncate + ellipsis). A nicer pattern — using the Quelle's `id` suffix or its author-year prefix (e.g. `q_villa_welpeloo_enschede_s3` → `Welpeloo S3`) — is an open question, see Section 8.

### Group C — short name + `name_full` on long-named vocab labels

For each label below: keep the existing long `name` value, just move it to `name_full`, then write a short `name`. No id changes.

#### MatchingQualitaet (9 nodes)

| id | new short `name` | `name_full` (= current name) |
|---|---|---|
| `mq_temporal_easy` | `Temporal: unproblematisch` | Temporales Matching unproblematisch |
| `mq_temporal_storage` | `Temporal: Zwischenlager` | Temporales Matching durch Zwischenlagerung |
| `mq_temporal_planned` | `Temporal: geplant` | Temporales Matching durch geplante Beschaffung |
| `mq_geographic_local` | `Geo: lokal (<50 km)` | Lokales geografisches Matching (<50 km) |
| `mq_geographic_regional` | `Geo: regional` | Regional geografisches Matching (50–500 km) |
| `mq_geographic_intl` | `Geo: international` | International / interkontinental |
| `mq_spec_exact` | `Spec: exakt` | Exakte Spezifikations-Übereinstimmung |
| `mq_spec_anpassung` | `Spec: Anpassung` | Spezifikations-Anpassung nötig |
| `mq_spec_zweckaenderung` | `Spec: Zweckänderung` | Zweckänderung (Funktionswechsel) |

#### ZustandsKlasse (6)

| id | short `name` | `name_full` |
|---|---|---|
| `zk_neuwertig` | `Neuwertig` | Neuwertig / wie neu |
| `zk_gebrauchsspuren_funktional` | `Gebraucht, funktional` | Gebrauchsspuren, funktional unbeeinträchtigt |
| `zk_eingeschraenkt_nachbearbeitung` | `Eingeschränkt: Nacharbeit` | Eingeschränkt, Nachbearbeitung nötig |
| `zk_eingeschraenkt_nutzungsklasse_reduzieren` | `Eingeschränkt: downgrade` | Eingeschränkt, Nutzungsklasse reduzieren |
| `zk_nicht_wiederverwendbar` | `Nicht reusable` | Nicht wiederverwendbar (Recycling/Entsorgung) |
| `zk_unbekannt_pruefung_offen` | `Prüfung offen` | Unbekannt (Prüfung offen) |

#### Bauproduktstatus (15)

| id | short `name` | `name_full` |
|---|---|---|
| `bps_ce_hen` | `CE (hEN)` | CE-Marking unter harmonisierter EN-Norm (hEN) |
| `bps_ce_eta` | `CE (ETA)` | CE-Marking via Europäische Technische Bewertung (ETA) |
| `bps_ukca` | `UKCA` | UKCA-Marking (UK post-Brexit) |
| `bps_abz_abg` | `abZ / aBG (DE)` | abZ / aBG (DE, allgemeine bauaufsichtliche Zulassung) |
| `bps_zie_vbg` | `ZiE / vBG (DE)` | ZiE / vBG (DE, project-specific approval) |
| `bps_ueh_zeichen` | `Ü-Zeichen (DE)` | Ü-Zeichen (DE, nationale Konformität) |
| `bps_tracimat_be` | `Tracimat (BE)` | Tracimat-zertifiziert (BE, traceable deconstruction) |
| `bps_pemd_fr` | `PEMD (FR)` | PEMD-erfasst (FR, diagnostic produit/matériau/déchet) |
| `bps_bestand_no_status` | `Bestand vor Ort` | Bestand vor Ort weiterverwendet (kein neues Inverkehrbringen) |
| `bps_bauproduktstatus_unbekannt` | `Status unbekannt` | _existing_ |
| _(remaining 5 already short)_ | _keep current_ | — |

#### LebenszyklusModul (5)

| id | short `name` | `name_full` |
|---|---|---|
| `lz_a1_a3` | `A1–A3 Produkt` | Produkt (A1–A3: Rohstoffe, Transport, Herstellung) |
| `lz_a4_a5` | `A4–A5 Errichtung` | Errichtung (A4 Transport, A5 Bauphase) |
| `lz_b` | `B1–B7 Nutzung` | Nutzung (B1–B7: Erhaltung, Reparatur, Betrieb, Operational Energy) |
| `lz_c` | `C1–C4 End-of-Life` | End of Life (C1–C4: Rückbau, Transport, Verarbeitung, Deponie) |
| `lz_d` | `D Beyond (Reuse)` | Module D — Beyond System Boundary (Reuse Credits) |

#### Akzeptanz (5)

| id | short `name` | `name_full` |
|---|---|---|
| `ak_dgnb_zertifizierung` | `DGNB` | DGNB-Zertifizierung akzeptiert Reuse |
| `ak_breeam_zertifizierung` | `BREEAM` | BREEAM-Zertifizierung akzeptiert Reuse |
| `ak_leed_zertifizierung` | `LEED` | LEED-Zertifizierung akzeptiert Reuse |
| `ak_oeffentlicher_bauherr_pilot` | `Public-Bauherr Pilot` | Öffentlicher Bauherr (Pilotprojekt-Akzeptanz) |
| `ak_aesthetik_patinakultur` | `Patina-Ästhetik` | Ästhetik-/Patinakultur akzeptiert |

#### Marktmodell (11)

| id | short `name` | `name_full` |
|---|---|---|
| `mm_same_site` | `Same-site` | Same-site Wiedereinbau (kein Markttransaktion) |
| `mm_plattform_vermittelt` | `Plattform-Kauf` | Plattform-vermittelter Kauf (Madaster/Concular/Restado/Rotor DC/Opalis) |
| `mm_kauf_gebraucht` | `Kauf gebraucht` | Kauf als Gebrauchtware |
| `mm_kauf_neu` | `Kauf neu-äquiv.` | Kauf als Bauprodukt (Neuware-äquivalent) |
| `mm_spende` | `Spende` | Spende |
| `mm_take_back_service` | `Take-Back` | Take-Back Service-Modell |
| `mm_leasing` | `Leasing` | Leasing / Mietverhältnis |
| `mm_rueckkauf` | `Rückkauf` | Rückkauf-Vereinbarung |
| `mm_forschungsprojekt_zuteilung` | `Forschungs-Zuteilung` | Forschungsprojekt-Zuteilung |
| `mm_intra_konzern` | `Intra-Konzern` | Intra-Konzern-Transfer |
| `mm_unbekannt` | `Unbekannt` | Marktmodell unbekannt |

#### Defekt (10)

| id | short `name` | `name_full` |
|---|---|---|
| `def_korrosion` | `Korrosion` | _identical_ |
| `def_riss` | `Risse` | Riss / Rissbildung |
| `def_verformung` | `Verformung` | Verformung / Setzung / Verzug |
| `def_karbonatisierung` | `Karbonatisierung` | Karbonatisierung (Beton) |
| `def_holzwurm_pilzbefall` | `Holzwurm/Pilz` | Holzwurm / Pilzbefall / Schimmel |
| `def_hohlraum_delamination` | `Delamination` | Hohlraum / Delamination |
| `def_oberflaechenmangel` | `Oberfläche` | Oberflächenmangel / Verfärbung |
| `def_chemische_belastung` | `Chemisch belastet` | Chemische Belastung (Salze, Säuren, Öle) |
| `def_brandschaden` | `Brandschaden` | _identical_ |
| `def_keine_befunde` | `Keine Befunde` | Keine relevanten Defekte (positive Befund) |

#### Norm (30) — strategy

Norm `name` currently holds the full title (e.g. *"EN 206 — Concrete specification, performance, production and conformity"*). The standard number is what we want in the graph view:

| id | short `name` | `name_full` |
|---|---|---|
| `norm_en_206` | `EN 206` | EN 206 — Concrete specification, performance, production and conformity |
| `norm_din_4074` | `DIN 4074` | DIN 4074 — Visual strength grading of structural timber (DE) |
| `norm_cen_ts_1090_201_2024` | `CEN/TS 1090-201:2024` | CEN/TS 1090-201:2024 — Assessment of Reclaimed Structural Steel |
| `norm_din_68800` | `DIN 68800` | DIN 68800 — Wood preservation and durability classes (DE) |
| `norm_ns_3682` | `NS 3682` | NS 3682 Reuse of hollow-core slabs / Norwegian reuse standard |
| _(remaining 25 similarly: standard number = name, full title = name_full)_ | | |

Already-short standard ids stay as-is.

### Group D — short name on long-named entity labels

#### Projekt (99) — pattern

Current `name` examples like *"House of Fraser / 318 Oxford Street → TBC.London steel reuse chain"* (66 chars) become two columns:

| id | short `name` | `name_full` |
|---|---|---|
| `p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain` | `House of Fraser` | House of Fraser / 318 Oxford Street → TBC.London steel reuse chain |
| `p_fcrbe` | `FCRBE` | FCRBE — Facilitating the Circulation of Reclaimed Building Elements |
| `p_boulder_fire_station_3` | `Boulder FS-3` | Boulder Fire Station 3 / City of Boulder Fire Rescue Station #3 |
| `p_charles_malis_molenbeek` | `Charles Malis` | Charles Malis / Antenne administrative de Molenbeek-Saint-Jean |
| `p_berlin_schildow_pilot_house` | `Berlin-Schildow Pilot` | Berlin-Schildow Pilot House / Berlin-Schildow 2nd pilot house |
| `p_k118_kopfbau_halle_118_winterthur` | `K.118 Winterthur` | K.118 / Kopfbau Halle 118, Winterthur |
| `p_resource_rows_copenhagen` | `Resource Rows` | Resource Rows, Copenhagen |
| `p_bedzed_london_hackbridge` | `BedZED` | BedZED / Beddington Zero Energy Development |
| _(remaining ~90 follow same recipe — first-token of project name + optional city)_ | | |

#### Bauwerk (196)

| id | short `name` | `name_full` (= existing) |
|---|---|---|
| `bw_berlin_fitout_donor_sources` | `Berlin donors` | Aggregierte Donorquellen: Boros/Berghain-Ausstellung, andere Baustellen, Tischlereireste |
| `bw_paris_regional_donor_sources_ferme_du` | `Paris donors (Ferme)` | Aggregierte Pariser und regionale Reuse-Gisements fuer La Ferme du Rail |
| `bw_ccn_heerde_receiver` | `CCN Heerde` | Circulair Centrum Nederland / Circular Centre Netherlands, Heerde |
| `bw_charles_malis_former_cigarette_factor` | `Charles Malis (former)` | Ehemalige Zigarettenfabrik / Charles Malis administrative antenna |
| _(remaining ~190 follow same recipe)_ | | |

#### Wiederverwendungskette (63)

| id | short `name` | `name_full` |
|---|---|---|
| `wk_waste_streams_to_brighton_waste_house` | `Brighton-Waste streams` | Household, industrial and construction waste streams → Brighton Waste House |
| `wk_impact_hub_interior_reuse_chain` | `Impact Hub fitout chain` | Baustellen-/Ausstellungs-/Offcut-Materialien → Impact Hub Berlin Fit-out |
| `wk_villa_welpeloo_enschede_villa_welpelo` | `Villa Welpeloo chain` | Villa Welpeloo materialgetriebene Tragwerks- und Hüllenreuse-Kette |
| _(remaining ~60)_ | | |

### Group E — Bauteilgruppe (306)

Both **id restructuring** AND **short `name` + `name_full`**. Detail in section 4 below.

| current `name` (avg 39 chars) | short `name` (≤ 25) | `name_full` |
|---|---|---|
| "Stahlträger / Stützen / Profilbleche Verbunddecken" | `Stahl-Träger K.118` | (= existing name) |
| "Ziegelfassadenmodule / Mauerwerksausschnitte" | `Ziegelfassade RR` | (= existing name) |
| "Reused structural steel" | `Stahl-Träger BedZED` | (= existing name) |
| "Gemeinsame Überdachung / Atriumhülle als Transformationsbauteil" | `Atriumdach Alliander` | (= existing name) |

### Group F — Akteur (582)

Already mostly short (median 15 chars). Two small cleanups:
- Drop `stars_ignored` property on 85 nodes (stale CSV column).
- Backfill `name_full` where `aliases` or `raw_name` shows a fuller form (4 nodes).
- Keep `actor_registry_section/order` + `akteur_kontext_text` + `reuse_relevanz_text` as actor-specific properties.

### Group G — Projekt (99) — special handling

Projekt has **429 distinct quantitative properties** across 99 nodes. These are per-project facts (m², t, %, € figures, year counts) and not all 99 have the same set — that's *by design*. So:

- **Define a "core required" subset** every Projekt must have: `id`, `name` (short), `name_full`, `bewertung`, `node_role`, `projektstatus_text`, `source_scope`.
- **Best-effort optional** (backfill where evidenced): `jahr_fertigstellung`, `flaeche_m2`, `note`.
- **Per-project quantitative props** stay as-is — don't force normalization; their absence on other projects is correct.
- Drop the duplicate-ish year fields where redundant: there are 30+ `jahr_*` variants — they exist because different sources use different yearly milestones. Worth a separate review later, but not in this pass.

### Group H — Land (16) — add ISO 2-letter code

Land has 10 props including `asbest_verbot_jahr`, but no ISO code. Add `country_iso2`:

| id | name | country_iso2 |
|---|---|---|
| `land_deutschland` | Deutschland | `DE` |
| `land_schweiz` | Schweiz | `CH` |
| `land_oesterreich` | Österreich | `AT` |
| `land_niederlande` | Niederlande | `NL` |
| `land_belgien` | Belgien | `BE` |
| _(remaining 11)_ | | _per ISO 3166_ |

Useful for cross-system joins (Madaster country codes, GDP datasets, ISO-aware Cypher).

---

## 4. Quelle convention — two-channel source tracking

Provenance is a first-class concern: every fact in the graph must be traceable to a source. The graph already uses two distinct mechanisms; this section codifies them as the standing convention.

### Channel 1 — Node-level Quelle via `BELEGT_IN`

Every **case-specific node** (a project, building, Bauteilgruppe, actor, reuse-chain, city, country) must have at least one outgoing `BELEGT_IN` edge to a `Quelle` node. The Quelle node carries the actual source metadata: `titel` / `name`, `url`, `quelltyp`, `source_file`.

This is already the working convention. **Current coverage (good):**

| Label | Coverage | Avg Quellen/node |
|---|---|---:|
| Projekt | 99/99 (100 %) | **4.0** |
| Bauteilgruppe | 306/306 (100 %) | 1.0 |
| Bauwerk | 196/196 (100 %) | 1.0 |
| Wiederverwendungskette | 63/63 (100 %) | 1.0 |
| Stadt | 62/62 (100 %) | 1.5 |
| Akteur | 565/582 (97 %) | 1.7 |
| Land | 13/16 (81 %) | 5.4 |

### Channel 2 — Rel-level evidence via `r.source`

For **inferred / propagated edges** (Phase G archive scan, Phase I orphan rescue, Phase J Wirtschaft scan, Round 003 BG-level propagation, future similar passes), the source lives on the relationship itself as a `source` property — pointing at the archive file or research file it was derived from.

This is already in use:

| `r.source` value | Edge count |
|---|---:|
| `round_003_project_propagation` | 321 |
| `manual_orphan_rescue` | 37 |
| `round_003_material_propagation` | 31 |
| `archive:<filename.md>` (≈ 150 distinct files) | several hundred total |
| `Research legal-regime matrix (typical jurisdiction)` | 19 |

Each inferred edge is auditable back to its origin.

### The principle — Quelle is never a property of a fact node

Don't denormalize. If a node has multiple sources, that's an array of `BELEGT_IN` edges; if a rel was inferred, that's a `r.source` value. Putting "the source" into the fact node's own property bag would lose the ability to cite the same Quelle from many facts, and would hide source URLs / titles / quelltyp in property strings.

### Current gaps — controlled-vocabulary nodes have 0 % Quelle coverage

The ~340 controlled-vocabulary nodes (Defekt, Marktmodell, ZustandsKlasse, Akzeptanz, MatchingQualitaet, Material, Methode, Aufbereitungsverfahren, PruefungNachweis, Schadstoff, BauwerkEra, Bauproduktstatus, LebenszyklusModul, Layer, Wirtschaft, plus the structural-vocab labels Akteurrolle/Akteurtyp/Status/Nutzung/Prozessphase/Bauteiltyp/Materialgruppe…) carry **no `BELEGT_IN` edge** — by accident of how they were seeded, not by design. Most were introduced by the research files under `_neo4j/intake/inbox/research/` and could legitimately point at those.

The fix is the subject of [QUELLE_PLAN.md](QUELLE_PLAN.md), scheduled to run after Phase P. Until then, the convention is unchanged: every new case-specific node MUST have a `BELEGT_IN` edge at creation time; every new inferred rel MUST have a `r.source` property.

### Verification queries

Regression check — any case-specific node without a Quelle:

```cypher
MATCH (n)
WHERE any(l IN labels(n) WHERE l IN
  ['Projekt','Bauteilgruppe','Bauwerk','Wiederverwendungskette','Stadt'])
  AND NOT EXISTS { (n)-[:BELEGT_IN]->(:Quelle) }
RETURN labels(n)[0] AS label, n.id, n.name LIMIT 20;
// Expected: 0 rows.
```

Regression check — any inferred rel without an `r.source`:

```cypher
MATCH (p:Projekt)-[r:HAT_DEFEKT_BEFUND|HAT_MATCHINGQUALITAET|HAT_DOMINANT_MARKTMODELL|HAT_DOMINANT_AKZEPTANZ|HAT_WIRTSCHAFT]->()
WHERE r.source IS NULL
RETURN count(r) AS rels_without_source;
// Expected: 0.

MATCH (bg:Bauteilgruppe)-[r:HAT_DEFEKT|HAT_MARKTMODELL]->()
WHERE r.source IS NULL
RETURN count(r) AS rels_without_source;
// Expected: ≤ 34 (the pre-Round-003 HAT_MARKTMODELL edges; everything Round-003-added carries r.source).
```

### Quelle node — quelltyp enum (codify)

| `quelltyp` value | Count | What it represents |
|---|---:|---|
| `external_link_from_actor_registry` | 319 | URL cited in the actor registry (an actor's homepage, news article, project page) |
| `case_markdown` | 76 | One per archive case-study `.md` file in `_archive/research/gebaeude/` |
| `external_reference` | 51 | URL / publication cited inside an archive case study |
| `actor_registry_markdown` | 1 | The `akteursliste_master.md` file itself |
| _(future)_ `research_markdown` | — | one per research file under `_neo4j/intake/inbox/research/` — introduced by Phase Q (see Section 7) |
| _(future)_ `controlled_vocab_seed` | — | the contract's `controlled_vocabulary.seed.kg.jsonl` itself — for structural-vocab nodes if you want 100 % coverage |

The five values become the **canonical enum** for the `quelltyp` property. Reject anything outside this list at intake.

---

## 5. Short-name tables — see Section 3 Groups C+D

The concrete tables (MatchingQualitaet, ZustandsKlasse, Bauproduktstatus, LebenszyklusModul, Akzeptanz, Marktmodell, Defekt, Norm, Projekt, Bauwerk, Wiederverwendungskette) are already in Section 3, Groups C and D above. No duplication here.

---

## 6. Bauteilgruppe id convention (with amendments from CONFLICT_ANALYSIS.md)

```
bg_<reuse-status>_<material>_<bauteiltyp>_<discriminator>
```

**No project slug in the id.** Project ownership lives in the `HAT_BAUTEILGRUPPE` relationship — queries find a BG's project trivially via `MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)`. We don't add a `slug_short` / `bg_slug` property anywhere.

| Slot | Vocabulary |
|---|---|
| `bg_` | fixed |
| `<reuse-status>` | `reuse / retained / planned / dismantled` |
| `<material>` | `stahl / holz / beton / stahlbeton / glas / keramik / ziegel / naturstein / daemmstoff / aluminium / kunststoff / mdf / recyclingbeton / mehrere / unbekannt` |
| `<bauteiltyp>` | `traeger / stuetze / wand / decke / dach / fassade / fenster / tuer / treppe / ausbau / belag / boden / daemmung / technik / mehrere` |
| `<discriminator>` | **mandatory and globally unique.** Free-form ≤ 5 tokens — typically a project hint + donor source + sub-component. Examples: `k118_aus_elys_basel`, `resource_rows_module`, `alliander_atrium`, `55gss_external_core`. |

Without the project slug separator (`__`), the discriminator is the only thing making BG ids globally unique. The rename-table generator must verify uniqueness during ID generation; any collision forces a longer / more specific discriminator.

Companion properties on every Bauteilgruppe:
- `reuse_status` (enum string)
- `primary_material_id` (string; `mat_mehrere` for multi-material BGs; `mat_unbekannt` for the 5 zero-material BGs — luminaires, wind-turbine blades, borrowed elements)
- `primary_bauteiltyp_id` (string; `bt_mehrere` for multi-bauteiltyp BGs — 189 out of 306)
- `aliases` includes the **old BG id** for historical traceability (873 references in past patch JSONLs stay resolvable)

**Multi-axis policy (37 % of BGs have ≥ 2 materials, 62 % have ≥ 2 Bauteiltypen):**
- Default: `mat_mehrere` / `bt_mehrere` slots; honest, machine-parseable
- Per-BG manual override allowed in the rename table for cases where a dominant primary is documented in the archive (e.g. K.118 has steel girders as the structural primary even though the BG also lists glass and timber finishes)
- The 0-material outliers (5 BGs: ROTOR-Leuchten, Leuchten, reused lights, borrowed facade elements, wind-turbine blades) use `mat_unbekannt` rather than dropping the material slot

---

## 7. Phased migration plan

The cleanup is sequenced so each phase is small enough to dry-run + apply + verify independently. All phases follow the standard backup → patch → dry-run → live-apply protocol.

### Phase L — property hygiene (low-risk, no id changes)

- L1: Drop stray intake props (`scope`, `topic`, `classified_at`, `not_yet_referenced_in_corpus`, `standards_body` on 1-7 nodes per label) on Material, Methode, Aufbereitungsverfahren, PruefungNachweis, Programm.
- L2: Drop `usage_project_count`, `usage_countries`, `usage_project_ids` derived props on Norm (16 nodes; verified derivable via Cypher).
- L3: Drop `stars_ignored` on Akteur (85 nodes; all carry value `'True'`).
- L4: Normalize Quelle (3-state handling per CONFLICT_ANALYSIS.md B7):
  - 1 node with both `name`+`titel` (values equal) → drop `titel`
  - 319 nodes with `titel` only → `rename_property` `titel → name_full`, derive short `name` (≤ 25 chars) from the title or id
  - 127 nodes with `name` only → length check; if > 25 chars, set `name_full = name` then derive new short `name`; if ≤ 25 chars, no change
  - Unify `filename` (5 nodes) + `dateiname` (1) → `source_file` (already 320 nodes)
- L5: Add `country_iso2` to all 16 Land nodes.
- L6 (carryover from existing Land cleanup): no-op — Land already has its asbestos / PCB / KMF properties from Phase A; just verify.

**Estimated:** ~150 property writes + drops, 0 node renames, 0 rel changes. One patch.

### Phase M — short `name` + `name_full` on long-named vocab labels

For each of: Defekt (10), MatchingQualitaet (9), ZustandsKlasse (6), Bauproduktstatus (15), LebenszyklusModul (5), Akzeptanz (5), Marktmodell (11), Norm (30).

For each affected node: `set_node_properties { name_full: <current name>, name: <new short name> }`. ~90 nodes total. **Aliases preservation:** none of these nodes currently carry aliases — no overwrite risk.

### Phase N — short `name` + `name_full` on long-named entity labels

For each of: Projekt (99), Bauwerk (196), Wiederverwendungskette (63). ~358 nodes.

**Aliases-append rule applies** to the 2 Projekte that already have aliases (`p_lysp8_basel`, `p_eth_circular_construction_student_reuse`) — the patch must include the existing aliases array, then append, never overwrite. Same precaution for `land_daenemark` if it gets touched in Phase L.

**Projekt short-name disambiguation rule:** when the project name leads with a generic noun (`Association house`, `Pilot house`, `Maison`) AND another project shares that prefix, the city/year token is mandatory in the short name. Known collision today: `p_association_house_groeditz` (→ `Vereinshaus Gröditz`) vs `p_association_house_plauen` (→ `Vereinshaus Plauen`).

### Phase O — Bauteilgruppe rename + property additions (SPLIT INTO O.a + O.b)

⚠️ Per CONFLICT_ANALYSIS.md B1: the apply tool's `canonicalize_node` op **does NOT rename ids** — it only sets `name` and `aliases`. The id rename therefore uses **`merge_node`**, which has working rel-id rewriting via `rewrite_id_outbound` (lines 788–793 in `_scripts/apply_neo4j_review_patch.py`).

#### Pre-Phase work

1. _(Skipped — per the Section 8 decision we don't add a slug property to Projekt.)_
2. Compute, for each of 306 BGs:
   - `new_id` per the schema in Section 6 (with mandatory discriminator for the 15 colliding tuples)
   - `reuse_status` (derived from existing reuse-status tokens in current id; defaults `reuse` if absent)
   - `primary_material_id`, `primary_bauteiltyp_id` (default `mat_mehrere` / `bt_mehrere` for multi-axis BGs; `mat_unbekannt` for 5 zero-material BGs)
   - short `name` (≤ 25 chars)
   - `name_full` (= current name)
   - `aliases` = `[<old_id>]` for historical traceability of 873 patch-file references
3. **Manual review** of the 306-row rename table — ≈ 30 ambiguous rows flagged (multi-axis BGs + zero-material outliers + collision groups).

#### Phase O.a — create new BG nodes

For each of 306 BGs: emit one `add_node` op with the new id and all new properties. **The old BG still exists and keeps all its rels.** This is a one-way commit — failure aborts and the new shells can be cleaned up trivially.

**Estimated:** 306 `add_node` ops, 1 patch, separate backup taken first.

#### Phase O.b — merge old into new

For each of 306 BGs: emit one `merge_node { from: <old_id>, to: <new_id> }` op. The apply tool:
- redirects every inbound rel onto the new BG
- redirects every outbound rel onto the new BG **and rewrites `r.id`** from `r_<old_bg>__TYPE__<x>` to `r_<new_bg>__TYPE__<x>` (verified — 7 882 such rels)
- unions labels onto the new BG
- merges all properties from the old BG onto the new BG (so `raw_name`, `alte_funktion`, `neue_funktion`, `counts_as_direct_reuse` survive)
- detach-deletes the old BG

**Estimated:** 306 `merge_node` ops, 1 patch, separate backup taken first.

**Total Phase O:** 612 ops across 2 patches.

### Phase P — backfill optional properties

- Backfill `counts_as_direct_reuse` on the 40 BGs where it's missing (review-required — could be `false`, `true`, or `unknown`).
- Backfill `alte_funktion` / `neue_funktion` on the 19 BGs where they're missing.
- Backfill the Projekt "best-effort optional" set (`jahr_fertigstellung`, `flaeche_m2`, `note`) on projects with archive evidence.

### Quelle gap filling — separate plan

The Quelle gap-filling work (~12 new Quelle nodes + ~350 BELEGT_IN edges to link every vocab node to a source) has been **moved to its own document:** [QUELLE_PLAN.md](QUELLE_PLAN.md).

That work happens **after Phase P** and is sequenced independently of the naming work.

---

## 8. Decisions recorded

The 8 design questions are answered. The rest of the plan reflects these answers throughout.

| # | Question | Decision |
|---|---|---|
| 1 | Project slug property name | **No slug property.** Drop `slug_short` / `bg_slug` entirely. Project ownership lives in `HAT_BAUTEILGRUPPE` — no need to also encode it in a separate property or in the BG id's project-slug slot. |
| 2 | Multi-material BG handling | **Default `mat_mehrere` + per-BG manual override** for the ~30 cases where one material is clearly dominant. Same for multi-Bauteiltyp. |
| 3 | Always set `name_full`? | **No.** Only when meaningfully different from `name`. Browser falls back to `name` automatically. |
| 4 | Run hygiene first? | **Yes.** Phase L → M → N → O → P. |
| 5 | Source for structural-vocab nodes? | **Whatever source is available, link it.** Any node that can be traced to an originating source (research file, controlled-vocab seed, project archive) gets a `BELEGT_IN` edge. Detail in [QUELLE_PLAN.md](QUELLE_PLAN.md). |
| 6 | Quelle short-name strategy | **Hybrid** — id-suffix for archive + registry Quellen (`Welpeloo S3`), author + year for academic refs (`MacArthur 2014`), truncation as fallback. |
| 7 | Codify `r.source` values? | **No.** Keep `r.source` as a single free-text pointer. The only requirement: every inferred edge has *some* source pointer. No enum split, no separate `source_detail`. The verification query in Section 4 catches missing values. |
| 8 | Quelle gap-filling work | **Separate document** — see [QUELLE_PLAN.md](QUELLE_PLAN.md). Schedule after Phase P; not part of this plan. |

### Next concrete deliverable

The **306-row Bauteilgruppe rename table** (Phase O pre-step 2 — see Section 7) — a CSV/markdown sheet with columns:

`old_id | new_id | name | name_full | reuse_status | primary_material_id | primary_bauteiltyp_id | discriminator | aliases | manual_override?`

About 30 rows will be flagged `manual_override = true` (the multi-axis BGs + the 5 zero-material outliers + the 15 colliding (project, material, bauteiltyp) groups). Mark those rows up before the patch is generated.

<!-- legacy open-questions section (kept for reference) -->
<details><summary>Legacy: original question framing with options + rationale</summary>

### Structural

#### Q1 — What do we call the short project slug?

We need a ≤ 3-token slug on every Projekt so Bauteilgruppe ids can use it (`bg_<slug>__…`).

| Option | Detail |
|---|---|
| **A** | Property name = `bg_slug` (specific to BG ids) |
| **B** *(recommended)* | Property name = `slug_short` (same slug can also seed Bauwerk and Wiederverwendungskette ids later) |

**Why B:** reusing the slug elsewhere costs nothing now and saves work later.

#### Q2 — When a Bauteilgruppe contains many materials, what's "the" material?

113 BGs (37 %) use 2 or more materials. The new id schema and `primary_material_id` property need a single value.

| Option | Detail |
|---|---|
| **A** *(recommended)* | Default to `mat_mehrere` ("multiple"); allow per-BG manual override for the ~30 cases where one material is clearly dominant (e.g. K.118 = steel-primary despite also listing glass and timber) |
| B | Pick the dominant by mass / volume for all 113 — accurate but means manual review of every multi-material BG |
| C | Pick the alphabetically-first material — deterministic, but arbitrary |

**Why A:** honesty by default, fix the obvious cases, don't over-invest in the rest.

(Same answer applies to multi-Bauteiltyp BGs — 189 of them, ~62 %.)

#### Q3 — Always store `name_full`, or only when it adds info?

Some short names are already complete (`Brandschaden`, `Spende`, `EN 206`). Do we still write a redundant `name_full` copy?

| Option | Detail |
|---|---|
| A | Always set `name_full = name` — uniform, predictable |
| **B** *(recommended)* | Only set `name_full` when meaningfully different — leaner, saves ~30 % of writes |

**Why B:** `name_full` is for the *long* form, not a duplicate. Neo4j Browser falls back to `name` when `name_full` is missing — no display difference.

#### Q4 — Run hygiene cleanup before the rename work?

Phase L drops stray intake properties, normalises Quelle, etc. The rename phases (M / N / O) happen after.

| Option | Detail |
|---|---|
| **A** *(recommended)* | Phase L first, then M → N → O → P |
| B | Bundle hygiene into the rename patches to reduce phase count |

**Why A:** small patches dry-run faster, fail more gracefully, and the verification queries stay focused.

---

### Quelle-specific (Phase Q decisions)

#### Q5 — Do "category" nodes need a source too?

About 190 nodes are pure structural typology: Akteurrolle ("architect", "structural engineer"), Status ("built", "in planning"), Nutzung ("office", "residential"), Bauteiltyp ("beam", "column"), Akteurtyp ("person", "company"), etc. These came from the contract's controlled-vocabulary seed file.

| Option | Detail |
|---|---|
| A | Attach all 190 to a single `q_controlled_vocab_seed` Quelle → 100 % source coverage on every node |
| **B** *(recommended)* | Leave structural typology un-sourced; only the ~90 *conceptual* vocab nodes (Defekt, MatchingQualitaet, ZustandsKlasse, Marktmodell, Schadstoff, Aufbereitungsverfahren, etc.) get linked to the research file that introduced them |

**Why B:** pure typology is universal vocabulary, not a research finding. A Quelle for "the concept of 'architect'" is meaningless. The 90 conceptual vocabs *are* research findings → those do earn a Quelle.

#### Q6 — How do we shorten Quelle names?

About 440 Quelle nodes need a ≤ 25-char `name`. The current full title is often a long bibliographic entry.

| Option | Detail | Example |
|---|---|---|
| A | Truncate the long title to 24 chars + "…" | "Steukers, Ghyoot, Devliege…" |
| B | Use the id suffix as the short name | `q_villa_welpeloo_enschede_s3` → `Welpeloo S3` |
| C | Use author + year extracted from the title | "MacArthur 2014" |
| **Hybrid** *(recommended)* | **B** for the 320 `external_link_from_actor_registry` + 76 `case_markdown` Quellen (their ids are already clean) · **C** for the 51 `external_reference` Quellen where author/year is parseable from the title · **A** as a fallback if neither pattern matches |

**Why hybrid:** readable, mostly automatic, doesn't require manually editing 440 rows.

#### Q7 — Should we standardise the rel-source values?

The `r.source` property on inferred edges is currently a mix:

- `archive:<filename>` — ~150 distinct values
- `round_003_project_propagation` / `round_003_material_propagation` — fixed strings
- `manual_orphan_rescue` — fixed string
- Free text like `"Same-site reuse (donor=receiver Bauwerk); no market transaction"` — descriptive

| Option | Detail |
|---|---|
| **A** *(recommended)* | Split into two properties: `source_type` (small enum: `archive` \| `research` \| `inference` \| `manual_curation`) and `source_detail` (free text — the filename or the descriptive sentence) — fast filtering AND human-readable |
| B | Keep the current mixed format — descriptive but needs fuzzy string matching to filter |

**Why A:** the cost of splitting is small (one-time `set_rel_properties` pass on ~600 edges); the gain is queries like `MATCH ()-[r {source_type: 'archive'}]-() …` that don't need a regex.

#### Q8 — When do we do the Quelle gap work?

Phase Q is ~350 ops total (the 12 research Quellen + ~160 BELEGT_IN edges + ~20 case-specific backfills).

| Option | Detail |
|---|---|
| A | Alongside Phase O (we're already touching many vocab nodes) |
| **B** *(recommended)* | After all naming + property work is done (after Phase P) |

**Why B:** Phase O is the riskiest of the lot (BG renames). Don't mix it with anything else.

---

### TL;DR — if you accept all my recommendations

| # | Question | Answer |
|---|---|---|
| Q1 | Slug property name | `slug_short` |
| Q2 | Multi-material BG handling | Default `mehrere` + manual overrides for the ~30 obvious cases |
| Q3 | Always set `name_full`? | Only when meaningfully different |
| Q4 | Run hygiene before renames? | Yes — Phase L → M → N → O → P |
| Q5 | Source for structural typology? | No — only the conceptual vocab nodes get sources |
| Q6 | Quelle short-name strategy | Hybrid: id-suffix + author-year + truncation fallback |
| Q7 | Codify `r.source` values? | Yes — split into `source_type` (enum) + `source_detail` (text) |
| Q8 | Phase Q timing | After Phase P |

If you accept all 8 as recommended: the only thing left to discuss before execution is the 306-row Bauteilgruppe rename table (next deliverable below).

### Next concrete deliverable

The **306-row Bauteilgruppe rename table** (Phase O pre-step 2 — see Section 7) — a CSV/markdown sheet with columns:

`old_id | new_id | name | name_full | reuse_status | primary_material_id | primary_bauteiltyp_id | discriminator | aliases | manual_override?`

About 30 rows will be flagged `manual_override = true` (the multi-axis BGs + the 5 zero-material outliers + the 15 colliding (project, material, bauteiltyp) groups). You mark those rows up before the patch is generated.

</details>
