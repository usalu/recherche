# Naming + property cleanup plan — graph-wide

**Decision recorded:** the canonical `name` property becomes the **short caption** (≤ 25 chars where applicable). Neo4j Browser displays it as the node label by default, so no `:style` config is needed. Long descriptive text moves to a sibling property `name_full` where it has real value.

This document covers:
1. The universal property convention (what every node label should carry)
2. Per-label cleanup actions
3. Concrete short-name tables for the labels where `name` is currently too long
4. The Bauteilgruppe id-restructuring convention (unchanged from earlier draft)
5. A phased migration plan

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

Currently only 128/447 Quelle nodes have a `name`. The other 319 use `titel` for the same purpose. Action:

```cypher
// 1. Where titel exists and name does not, copy titel → name
MATCH (q:Quelle) WHERE q.name IS NULL AND q.titel IS NOT NULL
SET q.name_full = q.titel;

// 2. Compute a short name from the source-scope label or id suffix
MATCH (q:Quelle) WHERE q.name IS NULL
SET q.name = coalesce(q.name_full[..25] + '…', q.id);

// 3. Verify
MATCH (q:Quelle) WHERE q.name IS NULL RETURN count(q) AS still_unnamed;
```

Also: unify `filename` (5 nodes) + `dateiname` (1) → existing `source_file` (320 nodes).

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

## 4. Bauteilgruppe id convention (unchanged from earlier draft)

```
bg_<project-slug>__<reuse-status>_<material>_<bauteiltyp>_<discriminator?>
```

| Slot | Vocabulary |
|---|---|
| `bg_` | fixed |
| `<project-slug>` | ≤ 3 tokens, stored on `Projekt.bg_slug` |
| `__` | double underscore separator (machine-parseable) |
| `<reuse-status>` | `reuse / retained / planned / dismantled` |
| `<material>` | `stahl / holz / beton / stahlbeton / glas / keramik / ziegel / naturstein / daemmstoff / aluminium / kunststoff / mdf / recyclingbeton / mehrere` |
| `<bauteiltyp>` | `traeger / stuetze / wand / decke / dach / fassade / fenster / tuer / treppe / ausbau / belag / boden / daemmung / technik / mehrere` |
| `<discriminator>` | optional free-form ≤ 4 tokens (donor source, location) |

Companion properties on every Bauteilgruppe:
- `reuse_status` (enum string)
- `primary_material_id` (string)
- `primary_bauteiltyp_id` (string)

---

## 5. Phased migration plan

The cleanup is sequenced so each phase is small enough to dry-run + apply + verify independently. All phases follow the standard backup → patch → dry-run → live-apply protocol.

### Phase L — property hygiene (low-risk, no id changes)

- L1: Drop stray intake props (`scope`, `topic`, `classified_at`, `not_yet_referenced_in_corpus`, `standards_body` on 1-7 nodes per label) on Material, Methode, Aufbereitungsverfahren, PruefungNachweis, Programm.
- L2: Drop `usage_*` derived props on Norm (16 nodes).
- L3: Drop `stars_ignored` on Akteur (85 nodes).
- L4: Normalize Quelle: `titel → name_full`, derive short `name`, unify `filename` / `dateiname` → `source_file`.
- L5: Add `country_iso2` to all 16 Land nodes.

**Estimated:** ~120 property writes + drops, 0 node renames, 0 rel changes. One patch.

### Phase M — short `name` + `name_full` on long-named vocab labels

For each of: Defekt (10), MatchingQualitaet (9), ZustandsKlasse (6), Bauproduktstatus (15), LebenszyklusModul (5), Akzeptanz (5), Marktmodell (11), Norm (30).

For each affected node: `set_node_properties { name_full: <current name>, name: <new short name> }`. ~90 nodes total.

### Phase N — short `name` + `name_full` on long-named entity labels

For each of: Projekt (99), Bauwerk (196), Wiederverwendungskette (63). ~358 nodes.

This is the largest in row-count but lowest in risk (only setting two properties per node, no rels touched).

### Phase O — Bauteilgruppe rename + property additions (the big one)

The 306-row rename. Sequence:

1. Compute `Projekt.bg_slug` for all 76 + 23 projects. Manual review of the slug list first.
2. Compute proposed `id`, `reuse_status`, `primary_material_id`, `primary_bauteiltyp_id`, short `name`, `name_full` for each of 306 BGs.
3. **Manual review** of the 306-row rename table — there will be ~10-20 ambiguous cases.
4. Emit one `canonicalize_node` patch (306 records, each handles id rename + property additions in one op, redirecting all incoming rels automatically).
5. Standard apply protocol.

### Phase P — backfill optional properties

- Backfill `counts_as_direct_reuse` on the 40 BGs where it's missing.
- Backfill `alte_funktion` / `neue_funktion` on the 19 BGs where they're missing.
- Backfill the Projekt "best-effort optional" set on projects with archive evidence.

---

## 6. Open questions

1. **`bg_slug` vs `slug_short`** — should the slug live on Projekt as `bg_slug` (specific to BGs) or as a general `slug_short` reusable for Bauwerk/Wiederverwendungskette ids too?
2. **Multi-material BGs** — when a BG has 3+ materials (37 BGs do), `primary_material_id` becomes `mehrere`. Should we instead pick the *dominant by mass / volume*, or stay with `mehrere` for honesty?
3. **`name_full` retention rule** — keep `name_full` only when meaningfully different from `name` (saves ~30 % of writes), or always set it for consistency?
4. **Quelle `name` derivation** — automatic truncation of `titel` to 25 chars feels ugly. Better: derive from `id` suffix (e.g. `q_villa_welpeloo_enschede_s3` → `Welpeloo S3`)? Or accept a leading author + year (e.g. `MacArthur 2014`) and parse out manually?
5. **Phase ordering** — run Phase L first (hygiene) before any name changes? My recommendation: yes, get to a clean property baseline before introducing `name_full` everywhere.

If you green-light the structure, the next concrete deliverable is **the 306-row Bauteilgruppe rename table** (Phase O step 2) — a CSV/markdown sheet you can mark up before the patch runs.
