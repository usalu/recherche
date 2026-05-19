# Naming + property cleanup plan — graph-wide

**Decision recorded:** the canonical `name` property becomes the **short caption** (≤ 25 chars where applicable). Neo4j Browser displays it as the node label by default, so no `:style` config is needed. Long descriptive text moves to a sibling property `name_full` where it has real value.

This document covers:
1. The universal property convention (what every node label should carry)
2. Per-label property landscape (current state, 53 labels)
3. Per-label cleanup actions (Groups A–H)
4. **Quelle convention** — the two-channel source-tracking rule and current coverage
5. Concrete short-name tables for the labels where `name` is currently too long
6. The Bauteilgruppe id-restructuring convention (with amendments from CONFLICT_ANALYSIS.md)
7. A phased migration plan (Phases L → P plus deferred Phase Q for Quelle gaps)

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

The fix is deferred — see **Phase Q** in Section 7. Until then, the convention is unchanged: every new case-specific node MUST have a `BELEGT_IN` edge at creation time; every new inferred rel MUST have a `r.source` property.

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
bg_<project-slug>__<reuse-status>_<material>_<bauteiltyp>_<discriminator?>
```

| Slot | Vocabulary |
|---|---|
| `bg_` | fixed |
| `<project-slug>` | ≤ 3 tokens, stored on `Projekt.bg_slug` |
| `__` | double underscore separator (machine-parseable; no existing id uses `__`, verified) |
| `<reuse-status>` | `reuse / retained / planned / dismantled` |
| `<material>` | `stahl / holz / beton / stahlbeton / glas / keramik / ziegel / naturstein / daemmstoff / aluminium / kunststoff / mdf / recyclingbeton / mehrere / unbekannt` |
| `<bauteiltyp>` | `traeger / stuetze / wand / decke / dach / fassade / fenster / tuer / treppe / ausbau / belag / boden / daemmung / technik / mehrere` |
| `<discriminator>` | **mandatory when (project, material, bauteiltyp) collides** (≥ 15 collision groups confirmed); free-form ≤ 4 tokens (donor source, location, sub-component) |

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

1. Compute `Projekt.bg_slug` for all 76 + 23 projects (≤ 3 tokens each). Manual review of the slug list before any patch.
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

### Phase Q (DEFERRED) — Quelle gap filling for vocabulary nodes

**Status:** scoped but **not scheduled** — depends on a separate decision about how strict we want vocabulary-level provenance to be.

**Goal:** lift the ~340 controlled-vocabulary nodes from 0 % to ~100 % `BELEGT_IN` coverage by linking each vocab to the research file that introduced it.

#### Q1 — create research-source Quelle nodes (≈ 12)

One Quelle per research markdown file under `_neo4j/intake/inbox/research/`:

| Research file | Proposed Quelle id | quelltyp |
|---|---|---|
| `bauteilreuse_legal_regime_matrix.md` | `q_research_bauteilreuse_legal_regime` | `research_markdown` |
| `connection_techniques_bauteilreuse.md` | `q_research_connection_techniques` | `research_markdown` |
| `circular_construction_economics_kg.md` | `q_research_circular_economics` | `research_markdown` |
| `circular_construction_leistungsanforderungen.md` | `q_research_leistungsanforderungen` | `research_markdown` |
| `circular_construction_reuse_graph_gaps.md` | `q_research_reuse_graph_gaps` | `research_markdown` |
| `schadstoff_reuse_knowledge_graph_research.md` | `q_research_schadstoff_kg` | `research_markdown` |
| `energy_climate_reuse_research.md` | `q_research_energy_climate` | `research_markdown` |
| `aufbereitungsverfahren_reused_building_elements.md` | `q_research_aufbereitungsverfahren` | `research_markdown` |
| `missing_underused_norm_nodes_reuse_kg.md` | `q_research_norm_nodes` | `research_markdown` |
| `reuse_knowledge_graph_coverage_audit.md` | `q_research_coverage_audit` | `research_markdown` |
| `testing_verification_bauteilreuse_kg.md` | `q_research_testing_verification` | `research_markdown` |
| `graph_patch_validation.md` | `q_research_patch_validation` | `research_markdown` |

#### Q2 — bulk-attach research Quellen to vocabulary nodes (≈ 160 edges)

| Research Quelle | Attach via `BELEGT_IN` to |
|---|---|
| `q_research_bauteilreuse_legal_regime` | 15 Bauproduktstatus + 5 Akzeptanz |
| `q_research_connection_techniques` | 12 Verbindungstechnik |
| `q_research_circular_economics` | 12 Wirtschaft + 11 Marktmodell |
| `q_research_reuse_graph_gaps` | 10 Defekt + 9 MatchingQualitaet + 6 ZustandsKlasse |
| `q_research_schadstoff_kg` | 8 Schadstoff + 6 BauwerkEra |
| `q_research_aufbereitungsverfahren` | 45 Aufbereitungsverfahren |
| `q_research_norm_nodes` | the 27 currently-source-less Norms |
| `q_research_energy_climate` | 5 LebenszyklusModul + 6 Layer |
| `q_research_leistungsanforderungen` | 12 Leistungsanforderung |

#### Q3 — backfill case-specific gap (≈ 20 edges)

- 17 source-less Akteure: investigate per-actor (most likely actor-registry entries with no URL — add the registry markdown as Quelle)
- 3 source-less Lands: the 3 supranational scope-pseudo nodes (`land_eu`, `land_eea`, `land_international`) — could attach a Phase A research source or accept they don't need a Quelle (they're meta).

#### Q4 (optional, only if 100 % coverage is wanted) — structural-vocab nodes

The structural-vocab labels (Akteurrolle, Akteurtyp, Status, Nutzung, Prozessphase, Bauteiltyp, Materialgruppe, Bauobjektklasse, Bauobjektrolle, WiederverwendungsArt, Funktionswechsel, Bausystem, Bauweise, Tragwerksprinzip, Logistik, BauaufgabeIntervention, Ressourcenquelle, Beschaffungsweg, HuerdeKategorie) hold purely typological nodes that were defined in the contract's `controlled_vocabulary.seed.kg.jsonl`. If 100 % BELEGT_IN coverage is desired, create one Quelle (`q_controlled_vocab_seed`, `quelltyp: controlled_vocab_seed`) and attach all ~190 structural-vocab nodes to it.

**Phase Q total estimate:** ~12 new Quelle nodes + ~160 new BELEGT_IN edges (without Q4) or ~190 more with Q4 = ≈ 350 ops.

**Why deferred:** Q4 is the question — do we want a sourced provenance for typological vocabulary? If yes, ~190 more BELEGT_IN edges; if no, the structural-vocab labels stay un-sourced and Q3 lifts everything else to ~100 %. Decide this before scheduling Phase Q.

---

## 8. Open questions

### Structural

1. **`bg_slug` vs `slug_short`** — should the slug live on Projekt as `bg_slug` (specific to BGs) or as a general `slug_short` reusable for Bauwerk/Wiederverwendungskette ids too?
2. **Multi-material BGs** — when a BG has 3+ materials (37 BGs do), `primary_material_id` becomes `mehrere`. Should we instead pick the *dominant by mass / volume*, or stay with `mehrere` for honesty?
3. **`name_full` retention rule** — keep `name_full` only when meaningfully different from `name` (saves ~30 % of writes), or always set it for consistency?
4. **Phase ordering** — run Phase L first (hygiene) before any name changes? My recommendation: yes, get to a clean property baseline before introducing `name_full` everywhere.

### Quelle-specific (Phase Q decisions)

5. **Q4 — structural-vocab Quelle coverage** — do we want the ~190 structural-vocab nodes (Akteurrolle, Akteurtyp, Status, Nutzung, …) attached to a single `q_controlled_vocab_seed` Quelle (100 % coverage) or do we accept that pure typology stays un-sourced?
6. **Quelle short-name derivation** — three candidate strategies for the ~440 Quellen needing a ≤ 25-char `name`:
   - (a) Truncate `name_full` to 24 chars + ellipsis (current draft) — ugly but deterministic
   - (b) Derive from `id` suffix: `q_villa_welpeloo_enschede_s3` → `Welpeloo S3` — readable, requires id parsing
   - (c) Author + year tag: `Stricker 2022`, `MacArthur 2014` — most readable, needs per-Quelle parsing of `name_full` (laborious for 446 nodes)
   - Recommendation: **(b) for `external_link_from_actor_registry` and `case_markdown`, (c) for `external_reference` if author/year are extractable, (a) as a fallback**
7. **Inferred-rel source values — codify the enum?** The `r.source` property currently mixes formats: `archive:<file>`, `round_003_<sub>`, free text (`Same-site reuse (donor = receiver…)`). Should we enforce a small enum like `archive | research | inference | manual_curation`? Trade-off: enum lookup is fast; current free-form values are descriptive.
8. **Phase Q timing** — schedule alongside Phase O (when we already touch many vocab nodes) or as a follow-on after the naming pass? My recommendation: **after**, so Phase O stays scoped to renames.

### Next concrete deliverable

If you green-light the structure, the next deliverable is **the 306-row Bauteilgruppe rename table** (Phase O step 2) — a CSV/markdown sheet with the proposed `new_id`, `name`, `name_full`, `reuse_status`, `primary_material_id`, `primary_bauteiltyp_id`, `discriminator`, `aliases`, and a `manual_override?` flag for the ~30 ambiguous rows (multi-axis BGs, zero-material outliers, collision groups).
