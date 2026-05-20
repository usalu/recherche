// =============================================================================
// PRE-FLIGHT VALIDATION — 2026-05-20 batch2 inbox import
// =============================================================================
//
// Purpose: Every relationship type, controlled-vocabulary id, and existing-node
//          reference used by PLAN_v2.md is verified against the live `mit-bestand`
//          graph BEFORE any patch is generated. Every block returns a count or a
//          list; a non-zero rows-where-expected-empty (or an empty list-where-
//          expected-non-empty) means the plan must be amended.
//
// Run order:
//   1.  Execute this entire file against `mit-bestand` (cypher-shell or Browser).
//   2.  Compare each result row against the inline `// EXPECTED:` comment.
//   3.  Record mismatches in CORRECTIONS_2026-05-20.md under "Pre-flight findings".
//   4.  Amend the patch generator (or PLAN_v2.md) before proceeding to Phase 0.
//
// Conventions:
//   - Sections labelled S1-Sn are intentionally idempotent / read-only.
//   - Every block ends with a comment "EXPECTED: <description>".
//   - Lists are returned ORDER BY id for diff-friendliness.
// =============================================================================


// -----------------------------------------------------------------------------
// S1 — Graph state at plan freeze
// -----------------------------------------------------------------------------

MATCH (n) WITH count(n) AS nodes
MATCH ()-[r]->() WITH nodes, count(r) AS rels
RETURN nodes, rels;
// EXPECTED: ~2298 nodes / ~17035 rels (post-Phase R as of 2026-05-19).
//           Any drift means another phase landed in between; reconcile before
//           continuing.


// -----------------------------------------------------------------------------
// S2 — All relationship types Plan v2 will USE must actually exist
// -----------------------------------------------------------------------------

CALL db.relationshipTypes() YIELD relationshipType
WITH collect(relationshipType) AS live_rels,
     [
       // Core structural
       'BETEILIGT_AN', 'ASSOZIIERT_MIT_PROJEKT',
       'HAT_AKTEURROLLE', 'HAT_AKTEURTYP',
       'GEHÖRT_ZU', 'VERBUNDEN_MIT_AKTEUR',
       // Geographic
       'LIEGT_IN_STADT', 'LIEGT_IN_LAND',
       // Bauteilgruppe internal vocab
       'HAT_BAUTEILTYP', 'HAT_MATERIALGRUPPE', 'HAT_WIEDERVERWENDUNGSART',
       'HAT_BESCHAFFUNGSWEG', 'HAT_VERBINDUNGSTECHNIK', 'HAT_RUECKBAUVERFAHREN',
       'HAT_AUFBEREITUNG', 'HAT_PRUEFUNG', 'HAT_DEFEKT', 'HAT_LEISTUNGSANFORDERUNG',
       'HAT_BAUPRODUKTSTATUS', 'HAT_METHODE', 'HAT_LOGISTIK', 'HAT_SCHADSTOFF',
       'HAT_MARKTMODELL', 'HAT_BAUTEILEBENE', 'HAT_RESSOURCENQUELLE',
       'HAT_STATUS', 'HAT_BAUOBJEKTROLLE', 'HAT_BAUOBJEKTKLASSE',
       // BG-Bauwerk
       'AUS_BAUWERK', 'EINGEBAUT_IN',
       // Projekt-level
       'HAT_BAUTEILGRUPPE', 'HAT_INTERVENTION', 'HAT_NUTZUNG',
       'HAT_DOMINANT_MARKTMODELL', 'HAT_DOMINANT_AKZEPTANZ',
       'HAT_WIRTSCHAFT', 'HAT_HUERDE', 'HAT_MATCHINGQUALITAET',
       'HAT_ZERTIFIZIERUNG', 'REFERENZIERT_NORM', 'NUTZT_BAUWERK',
       // Programme / Tool / Software
       'TEIL_VON_PROGRAMM', 'ERHALT_FOERDERUNG_DURCH',
       'NUTZT_SOFTWARE', 'NUTZT_TOOL',
       // Material fine-grained
       'NUTZT_MATERIAL',
       // Quelle
       'BELEGT_IN', 'ZITIERT_QUELLE',
       // Wiederverwendungskette
       'TEIL_VON_KETTE',
       // Norm-related
       'BERECHNET_NACH_MODUL', 'METHODENGRUNDLAGE_NORM',
       // ZustandsKlasse (NEW — first use in this run)
       'HAT_ZUSTANDSKLASSE'
     ] AS planned_rels
UNWIND planned_rels AS r
WITH r, live_rels
RETURN r AS planned_rel_type,
       (r IN live_rels) AS exists_in_graph
ORDER BY exists_in_graph, planned_rel_type;
// EXPECTED:
//   exists_in_graph=true  for everything except possibly HAT_ZUSTANDSKLASSE
//                         (intentional first use; document in CORRECTIONS).
//   Any other 'false' row = a fabricated rel type. Plan_v2 MUST replace it.


// -----------------------------------------------------------------------------
// S3 — Relationship types Plan 2 INCORRECTLY used (sanity check: confirm absent)
// -----------------------------------------------------------------------------

CALL db.relationshipTypes() YIELD relationshipType
WITH collect(relationshipType) AS live_rels,
     ['HAT_SOFTWARE', 'HAT_TOOL', 'HAT_NORM', 'HAT_BAUAUFGABE',
      'HAT_AKZEPTANZ', 'HAT_AUFBEREITUNGSVERFAHREN', 'HAT_PRUEFUNG_NACHWEIS',
      'HAT_PRUEFUNGNACHWEIS', 'LIEFERT_MATERIAL_AUS', 'VERBUNDEN_MIT',
      'LIEGT_IN'] AS bad_rels
UNWIND bad_rels AS r
WITH r, live_rels
RETURN r AS plan_2_uses_this,
       (r IN live_rels) AS exists_in_graph,
       CASE r
         WHEN 'HAT_SOFTWARE' THEN 'use NUTZT_SOFTWARE'
         WHEN 'HAT_TOOL' THEN 'use NUTZT_TOOL'
         WHEN 'HAT_NORM' THEN 'use REFERENZIERT_NORM'
         WHEN 'HAT_BAUAUFGABE' THEN 'use HAT_INTERVENTION'
         WHEN 'HAT_AKZEPTANZ' THEN 'use HAT_DOMINANT_AKZEPTANZ'
         WHEN 'HAT_AUFBEREITUNGSVERFAHREN' THEN 'use HAT_AUFBEREITUNG'
         WHEN 'HAT_PRUEFUNG_NACHWEIS' THEN 'use HAT_PRUEFUNG'
         WHEN 'HAT_PRUEFUNGNACHWEIS' THEN 'use HAT_PRUEFUNG'
         WHEN 'LIEFERT_MATERIAL_AUS' THEN 'use AUS_BAUWERK'
         WHEN 'VERBUNDEN_MIT' THEN 'use TEIL_VON_PROGRAMM or ERHALT_FOERDERUNG_DURCH or VERBUNDEN_MIT_AKTEUR (target-dependent)'
         WHEN 'LIEGT_IN' THEN 'use LIEGT_IN_STADT or LIEGT_IN_LAND (target-dependent)'
       END AS replacement;
// EXPECTED: All rows have exists_in_graph = false. Confirms our diagnosis.


// -----------------------------------------------------------------------------
// S4 — All Akteurrolle ids enumerated (for HAT_AKTEURROLLE writes)
// -----------------------------------------------------------------------------

MATCH (ar:Akteurrolle)
RETURN ar.id AS akteurrolle_id, ar.name AS name
ORDER BY ar.id;
// EXPECTED: ~25 rows including ar_entwurf_planung, ar_tragwerksplanung,
//           ar_oeffentliche_hand_foerderung, ar_materialbroker, ar_betrieb_nutzung,
//           ar_forschung_dokumentation, ar_bauausfuehrung_fertigung, etc.


// -----------------------------------------------------------------------------
// S5 — All Akteurtyp ids enumerated (for HAT_AKTEURTYP writes)
// -----------------------------------------------------------------------------

MATCH (at:Akteurtyp)
RETURN at.id AS akteurtyp_id, at.name AS name
ORDER BY at.id;
// EXPECTED: ~9 rows: at_person, at_unternehmen, at_forschung_lehre,
//           at_oeffentliche_institution, at_foerdergeber_programmtraeger,
//           at_materialhub_bauteilboerse, at_software_tool_anbieter,
//           at_ngo_verband_netzwerk, at_organisation.


// -----------------------------------------------------------------------------
// S6 — All Aufbereitungsverfahren ids (avoid Plan 1's invented av_holzaufbereitung)
// -----------------------------------------------------------------------------

MATCH (av:Aufbereitungsverfahren)
RETURN av.id AS aufbereitungsverfahren_id, av.name AS name
ORDER BY av.id;
// EXPECTED: ~45 rows (4 parents + 30 Phase D children + originals). Critical to
//           sanity-check Plan 1 inherited ids: av_holzaufbereitung,
//           av_remanufacturing, av_reinigung, av_rekonditionierung,
//           av_qualitaetssicherung, av_entmoertelung_von_fliesen — all suspected
//           NOT to exist. The patch generator must substitute live ids.


// -----------------------------------------------------------------------------
// S7 — All PruefungNachweis ids (validate Plan 2's pr_* references)
// -----------------------------------------------------------------------------

MATCH (pr:PruefungNachweis)
RETURN pr.id AS pruefung_id, pr.name AS name
ORDER BY pr.id;
// EXPECTED: ~20 rows. Plan 2 references pr_zustandsbewertung, pr_sichtpruefung,
//           pr_statische_nachweisfuehrung, pr_geometrische_vermessung,
//           pr_dokumentenpruefung_bestand, pr_schadstoffpruefung,
//           pr_bohrkernpruefung_beton, pr_festigkeitssortierung_holz,
//           pr_korrosionspruefung — confirm each.


// -----------------------------------------------------------------------------
// S8 — All Material ids (for NUTZT_MATERIAL writes)
// -----------------------------------------------------------------------------

MATCH (m:Material)
RETURN m.id AS material_id, m.name AS name
ORDER BY m.id;
// EXPECTED: ~19 rows. Need explicit list so the BG patch generator can pick
//           per-BG `primary_material_id` and NUTZT_MATERIAL targets without guessing.


// -----------------------------------------------------------------------------
// S9 — All Materialgruppe ids (sanity check Plan 2's mg_* references)
// -----------------------------------------------------------------------------

MATCH (mg:Materialgruppe)
RETURN mg.id AS materialgruppe_id, mg.name AS name
ORDER BY mg.id;
// EXPECTED: ~10 rows: mg_metall, mg_mineralisch, mg_holz_biobasiert,
//           mg_glas_keramik, mg_daemmstoff, mg_kunststoff, mg_lehm_erde,
//           mg_verbundstoff, mg_recyclingmaterial, mg_unbekannt.


// -----------------------------------------------------------------------------
// S10 — All Bauteiltyp ids (verify bt_belag question raised in review)
// -----------------------------------------------------------------------------

MATCH (bt:Bauteiltyp)
RETURN bt.id AS bauteiltyp_id, bt.name AS name
ORDER BY bt.id;
// EXPECTED: ~15 rows. Critical: does `bt_belag` exist? Plan 2 uses it in BG ids
//           (`bg_reuse_*_belag_*`). GRAPH_SCHEMA documents only `bt_boden`. If
//           bt_belag is absent, Plan 2's BG ids using `belag` slot may be invalid;
//           either create bt_belag (intentional schema extension) or rewrite ids
//           to use `boden`.


// -----------------------------------------------------------------------------
// S11 — All Marktmodell ids (verify mm_* enum constraint)
// -----------------------------------------------------------------------------

MATCH (mm:Marktmodell)
RETURN mm.id AS marktmodell_id, mm.name AS name
ORDER BY mm.id;
// EXPECTED: ~11 rows per NAMING_AND_PROPERTIES_PLAN.md constraint:
//           mm_same_site, mm_plattform_vermittelt, mm_kauf_gebraucht,
//           mm_kauf_neu, mm_spende, mm_take_back_service, mm_leasing,
//           mm_rueckkauf, mm_forschungsprojekt_zuteilung, mm_intra_konzern,
//           mm_unbekannt.


// -----------------------------------------------------------------------------
// S12 — All Akzeptanz ids (verify ak_* enum constraint)
// -----------------------------------------------------------------------------

MATCH (ak:Akzeptanz)
RETURN ak.id AS akzeptanz_id, ak.name AS name
ORDER BY ak.id;
// EXPECTED: 5 rows: ak_dgnb_zertifizierung, ak_breeam_zertifizierung,
//           ak_leed_zertifizierung, ak_oeffentlicher_bauherr_pilot,
//           ak_aesthetik_patinakultur.


// -----------------------------------------------------------------------------
// S13 — All ZustandsKlasse ids (verify zk_* enum constraint)
// -----------------------------------------------------------------------------

MATCH (zk:ZustandsKlasse)
RETURN zk.id AS zustandsklasse_id, zk.name AS name
ORDER BY zk.id;
// EXPECTED: 6 rows: zk_neuwertig, zk_gebrauchsspuren_funktional,
//           zk_eingeschraenkt_nachbearbeitung,
//           zk_eingeschraenkt_nutzungsklasse_reduzieren,
//           zk_nicht_wiederverwendbar, zk_unbekannt_pruefung_offen.


// -----------------------------------------------------------------------------
// S14 — All Bauproduktstatus ids (verify bps_* enum constraint)
// -----------------------------------------------------------------------------

MATCH (bps:Bauproduktstatus)
RETURN bps.id AS bauproduktstatus_id, bps.name AS name
ORDER BY bps.id;
// EXPECTED: ~15 rows: bps_tracimat_be, bps_pemd_fr, bps_zie_vbg, bps_abz_abg,
//           bps_project_specific, bps_ce_hen, bps_ce_eta, bps_ukca, bps_nta_8713,
//           bps_baupg_ch, bps_ue_zeichen, bps_bestand_no_status, bps_unbekannt.


// -----------------------------------------------------------------------------
// S15 — All Status ids (HAT_STATUS targets)
// -----------------------------------------------------------------------------

MATCH (s:Status)
RETURN s.id AS status_id, s.name AS name
ORDER BY s.id;
// EXPECTED: Plan 2 references status_geplant, status_realisiert,
//           status_rueckgebaut — verify all three exist.


// -----------------------------------------------------------------------------
// S16 — All Bauteilebene ids
// -----------------------------------------------------------------------------

MATCH (be:Bauteilebene)
RETURN be.id AS bauteilebene_id, be.name AS name
ORDER BY be.id;
// EXPECTED: be_bauteilgruppe, be_einzelbauteil, be_gebaeudeteil,
//           be_materialcharge, be_oberflaechenschicht, be_system (6 rows).


// -----------------------------------------------------------------------------
// S17 — All Ressourcenquelle ids
// -----------------------------------------------------------------------------

MATCH (rq:Ressourcenquelle)
RETURN rq.id AS ressourcenquelle_id, rq.name AS name
ORDER BY rq.id;
// EXPECTED: Plan 2 references rq_donorgebaeude, rq_lager, rq_baustelle —
//           verify all three.


// -----------------------------------------------------------------------------
// S18 — All Bauobjektrolle ids (HAT_BAUOBJEKTROLLE targets)
// -----------------------------------------------------------------------------

MATCH (bor:Bauobjektrolle)
RETURN bor.id AS bauobjektrolle_id, bor.name AS name
ORDER BY bor.id;
// EXPECTED: 6 rows per GRAPH_SCHEMA: bor_donorobjekt, bor_empfaengerobjekt,
//           bor_bestandsobjekt, bor_same_site_donor_receiver, bor_referenzobjekt,
//           bor_zwischenlager.


// -----------------------------------------------------------------------------
// S19 — All Bauobjektklasse ids (HAT_BAUOBJEKTKLASSE targets)
// -----------------------------------------------------------------------------

MATCH (bok:Bauobjektklasse)
RETURN bok.id AS bauobjektklasse_id, bok.name AS name
ORDER BY bok.id;
// EXPECTED: 8 rows: bok_gebaeude, bok_gebaeudeteil, bok_pavillon,
//           bok_infrastruktur, bok_innenausbau, bok_depot_lager,
//           bok_quartier_areal, bok_reuse_centre.


// -----------------------------------------------------------------------------
// S20 — All Programm ids (verify existing + identify new)
// -----------------------------------------------------------------------------

MATCH (p:Programm)
RETURN p.id AS programm_id, p.name AS name
ORDER BY p.id;
// EXPECTED: 17 rows after Phase C. Plan v2 will introduce ~4 new:
//           prog_be_circular, prog_mas_dfab, prog_holzbau_offensive_bw,
//           prog_urban_bricolage (+ optional prog_prec, prog_abn_amro_mission_2030).
//           Confirm NONE of these new ids already exist.


// -----------------------------------------------------------------------------
// S21 — All Stadt ids (verify existing + identify new)
// -----------------------------------------------------------------------------

MATCH (s:Stadt)
RETURN s.id AS stadt_id, s.name AS name
ORDER BY s.id;
// EXPECTED: 62 rows. Plan v2 needs to introduce or reuse:
//           stadt_amsterdam, stadt_duebendorf, stadt_liverpool, stadt_bordeaux,
//           stadt_winterthur, stadt_fribourg, stadt_mérignac, stadt_dundee,
//           stadt_weil_am_rhein, stadt_ingersheim, stadt_stuttgart, stadt_wien,
//           stadt_anderlecht, stadt_canterbury, stadt_delft, stadt_eindhoven,
//           stadt_coimbra, stadt_utrecht, stadt_paris, stadt_esch_sur_alzette.
//           Verify each: which already exist, which need creating.


// -----------------------------------------------------------------------------
// S22 — All Land ids (Ukraine is the most likely new one)
// -----------------------------------------------------------------------------

MATCH (l:Land)
RETURN l.id AS land_id, l.name AS name, l.country_iso2 AS iso2
ORDER BY l.id;
// EXPECTED: 16 rows. Plan v2 may need to add: land_ukraine, land_portugal,
//           land_luxemburg, land_italien, land_polen, land_grossbritannien.
//           Verify which already exist.


// -----------------------------------------------------------------------------
// S23 — All Software ids (avoid duplicate creation)
// -----------------------------------------------------------------------------

MATCH (sw:Software)
RETURN sw.id AS software_id, sw.name AS name
ORDER BY sw.id;
// EXPECTED: ~5 rows: software_bim, software_concular, software_restado,
//           software_qflow, software_inies. Plan v2 will introduce
//           software_llmnt, software_ecotool, software_opalis, software_refair.


// -----------------------------------------------------------------------------
// S24 — All Tool ids (avoid duplicate creation)
// -----------------------------------------------------------------------------

MATCH (t:Tool)
RETURN t.id AS tool_id, t.name AS name
ORDER BY t.id;
// EXPECTED: ~5 rows: tool_bauteilkatalog, tool_bim_bauteilkatalog,
//           tool_oogstkaart_harvest_map, tool_hts_stockmatcher,
//           tool_material_passports_maconda. Plan v2 will introduce tool_retile,
//           tool_rcmi.


// -----------------------------------------------------------------------------
// S25 — All Norm ids (verify norm_* prefix convention)
// -----------------------------------------------------------------------------

MATCH (n:Norm)
RETURN n.id AS norm_id, n.name AS name
ORDER BY n.id;
// EXPECTED: ~30 rows. Plan 2 used `n_bs_5385_5_2009` (wrong prefix); replace with
//           `norm_bs_5385_5_2009`.


// -----------------------------------------------------------------------------
// S26 — Existing project nodes Plan v2 will touch (PARKED_DECISIONS scope)
// -----------------------------------------------------------------------------

MATCH (p:Projekt) WHERE p.id IN [
  'p_obk_27', 'p_pavilion_circl_amsterdam', 'p_circl_abn_amro',
  'p_fcrbe', 'p_interreg_nwe_fcrbe', 'p_architecture_of_reuse_brussels',
  'p_eth_circular_construction_student_reuse', 'p_reuse_in_construction_zhaw',
  'p_vandkunsten_component_reuse', 'p_rebridge_structural_reuse_project',
  'p_re_use_hoefe', 'p_reuse_logistics', 'p_rcmi_concular',
  'p_refair_bordeaux_reemploi_platform', 'p_stuttgart_210',
  'p_lysp8_basel', 'p_reallabor_be_ware', 'p_schaerenmoosstrasse_zuerich',
  'p_meduni_campus_mariannengasse', 'p_granby_workshop', 'p_careno_becircular',
  'p_umar_unit', 'p_elementa_walkeweg'
]
OPTIONAL MATCH (p)-[r]-()
WITH p, count(r) AS degree
OPTIONAL MATCH (p)-[:BELEGT_IN]->(q:Quelle)
RETURN p.id AS projekt_id,
       p.name AS name,
       p.node_role AS node_role,
       p.aliases AS aliases,
       degree,
       collect(DISTINCT q.id) AS belegt_in_quellen
ORDER BY p.id;
// EXPECTED: All 23 ids present with degree > 0. ALIASES capture is critical
//           — patch generator must UNION with these when running canonicalize_node.


// -----------------------------------------------------------------------------
// S27 — Akteure that PARKED says are "already in graph"; verify each
// -----------------------------------------------------------------------------

MATCH (a:Akteur) WHERE a.id IN [
  // Stub akteure to KEEP per PARKED_DECISIONS
  'glasfischer_glastec','heinrich_boell_stiftung','koimo_development',
  'mehr_als_wohnen','stiftung_habitat','citydev_brussels','denkstatt',
  'edith_maryon_stift','eitel_partner','gibbins_architekten',
  'kunst_stoffe_ev','zusammenkunft_berlin',
  // Akteure used by dossiers, expected to exist already
  'rotor_asbl_vzw','rotor','rotor_dc','rotordc',
  'zirkular_gmbh','zirkular',
  'studio_trachsler_hoffmann','daniel_hoffmann','gian_trachsler',
  'dirk_e_hebel','felix_heisel','vanessa_propach',
  'carla_ferrando_costansa','pablo_garrido_arnaiz','parabase',
  'immobilien_basel_stadt','hochbauamt_basel_stadt','zirkular_gmbh',
  'lionel_billiet','sebastien_paulet','hans_hammink','michel_baars',
  'baubuero_in_situ','baubureau_in_situ',
  'kerstin_mueller','kerstin_müller','kevin_straub','marc_angst','marc_loeliger',
  'tu_delft','abn_amro','bam','bam_bouw_techniek',
  'de_architekten_cie','assemble','assemble_studio','lewis_jones',
  'andrea_klinge','christof_ziegert','eike_roswag_klinge','matthew_crabbe',
  'nina_pawlicki','uwe_seiler','nbl_studio',
  'andreas_kretzer','katharina_raabe','maximilian_stemmler','roman_kreuzer',
  'stefan_kroetsch','thomas_stark',
  'duncan_baker_brown','hugo_topalov','sarah_westerfeld','michael_ghyoot',
  'catherine_de_wolf','fabio_gramazio','matthias_kohler',
  'andreas_sonderegger','eva_stricker','guido_brandi',
  'katrine_west_kristensen','soren_nielsen','vandkunsten',
  'christine_conix','lionel_devlieger','maarten_gielen',
  'concular','la_fabrique_de_bordeaux_metropole','la_fab',
  'baukarussell','big_bundesimmobilien','meduni_wien',
  'madlen_kobi','university_of_fribourg','materialnomaden','urban_bricolage'
]
RETURN a.id AS akteur_id, a.name AS name, a.akteurtyp AS akteurtyp,
       size([(a)-[r]-() | r]) AS degree
ORDER BY a.id;
// EXPECTED: All ids that PARKED_DECISIONS / dossiers claim exist — confirm.
//           Missing rows = create as new Akteur in Phase 5. Present rows with
//           variant ids (e.g. kerstin_mueller vs kerstin_müller) = pick the
//           canonical and alias the other.


// -----------------------------------------------------------------------------
// S28 — Werner Sobek duplicate on UMAR (Plan 1 P0-A)
// -----------------------------------------------------------------------------

MATCH (p:Projekt {id:'p_umar_unit'})-[r:ASSOZIIERT_MIT_PROJEKT|BETEILIGT_AN]-(a:Akteur)
WHERE a.name CONTAINS 'Sobek' OR a.name CONTAINS 'sobek'
RETURN a.id AS akteur_id, a.name AS name, type(r) AS rel_type,
       size([(a)-[r2]-() | r2]) AS degree;
// EXPECTED: 2 rows (werner_sobek_p canonical + Werner_Sobek duplicate).
//           Resolution: remove the duplicate's UMAR rel, optionally merge.


// -----------------------------------------------------------------------------
// S29 — Rotor / RotorDC fragmentation (Plan 1 P0-C)
// -----------------------------------------------------------------------------

MATCH (a:Akteur)
WHERE a.name =~ '(?i).*rotor.*' OR a.id =~ 'rotor.*'
RETURN a.id AS akteur_id, a.name AS name,
       size([(a)-[r]-() | r]) AS degree
ORDER BY degree DESC;
// EXPECTED: At least 5 rows: Rotor, rotor_asbl_vzw, rotor_vzw, rotor_dc, rotordc.
//           Resolution per STUB_AKTEUR_DECISIONS: merge rotor_vzw → rotor_asbl_vzw
//           and verify rotor_dc vs rotordc duplication separately.


// -----------------------------------------------------------------------------
// S30 — Circl merge direction baseline (P0-B in Plan 1; Phase 1c in Plan 2)
// -----------------------------------------------------------------------------

MATCH (p:Projekt) WHERE p.id IN ['p_pavilion_circl_amsterdam','p_circl_abn_amro']
OPTIONAL MATCH (p)-[r]-(other)
WITH p, count(DISTINCT r) AS degree, collect(DISTINCT type(r)) AS rel_types
RETURN p.id AS projekt_id, p.name AS name, p.node_role AS node_role,
       degree, rel_types;
// EXPECTED: Both ids present. PARKED_DECISIONS recommends merge p_pavilion_*
//           → p_circl_abn_amro. PLAN_v2 will follow this direction.


// -----------------------------------------------------------------------------
// S31 — Quelle nodes Plan v2 will reuse vs. create
// -----------------------------------------------------------------------------

MATCH (q:Quelle)
WHERE q.id CONTAINS 'circl' OR q.id CONTAINS 'pavilion'
   OR q.id CONTAINS 'baars' OR q.id CONTAINS 'akteursliste'
   OR q.id CONTAINS 'lysp8' OR q.id CONTAINS 'careno'
RETURN q.id AS quelle_id, q.name AS name, q.url AS url, q.quelltyp AS quelltyp
ORDER BY q.id;
// EXPECTED: Variable. Critical: identify existing Circl-related Quellen so the
//           merge step (Phase 1c) doesn't duplicate them, and so PLAN_v2's new
//           per-source external_reference Quellen don't collide on id.


// -----------------------------------------------------------------------------
// S32 — Wiederverwendungskette existing prefix (k_* vs wk_*)
// -----------------------------------------------------------------------------

MATCH (k:Wiederverwendungskette)
RETURN substring(k.id, 0, 2) AS id_prefix, count(*) AS count
ORDER BY count DESC;
// EXPECTED: 63 rows total. Confirm prefix is `k_` (not `wk_`). PLAN_v2 must
//           emit new ketten with k_* prefix to match.


// -----------------------------------------------------------------------------
// S33 — Rel type used to attach Bauteilgruppe to Wiederverwendungskette
// -----------------------------------------------------------------------------

MATCH (bg:Bauteilgruppe)-[r]->(k:Wiederverwendungskette)
RETURN type(r) AS rel_type, count(*) AS count
ORDER BY count DESC;
// EXPECTED: TEIL_VON_KETTE dominant. PLAN_v2 uses this rel type.


// -----------------------------------------------------------------------------
// S34 — Rel type used to attach Bauwerk to Wiederverwendungskette (if any)
// -----------------------------------------------------------------------------

MATCH (bw:Bauwerk)-[r]-(k:Wiederverwendungskette)
RETURN type(r) AS rel_type, count(*) AS count
ORDER BY count DESC;
// EXPECTED: Reveals whether the graph has a Bauwerk→Kette rel. If not, the BG
//           is the only entry-point; PLAN_v2 must reflect this.


// -----------------------------------------------------------------------------
// S35 — Already-linked actors that PARKED_DECISIONS notes as having aliases
// -----------------------------------------------------------------------------

MATCH (a:Akteur) WHERE a.id IN [
  'imd_raadgevende_ingenieurs','cleveland_steel_tubes','rotor_dc',
  'duncan_baker_brown','land_daenemark'
]
RETURN a.id AS akteur_id, a.name AS name, a.aliases AS current_aliases;
// EXPECTED: All 5 present with non-empty aliases. PLAN_v2 must UNION new
//           aliases with these when running canonicalize_node.


// -----------------------------------------------------------------------------
// S36 — Already-linked Projekt nodes that have aliases
// -----------------------------------------------------------------------------

MATCH (p:Projekt) WHERE p.id IN [
  'p_lysp8_basel','p_eth_circular_construction_student_reuse'
]
RETURN p.id AS projekt_id, p.name AS name, p.aliases AS current_aliases;
// EXPECTED: Both with aliases. PLAN_v2 patch generator MUST read these and
//           append, never overwrite.


// -----------------------------------------------------------------------------
// S37 — `mq_*` MatchingQualitaet hub (for HAT_MATCHINGQUALITAET writes)
// -----------------------------------------------------------------------------

MATCH (mq:MatchingQualitaet)
RETURN mq.id AS matchingqualitaet_id, mq.name AS name,
       size([(mq)<-[r]-() | r]) AS incoming_count
ORDER BY incoming_count DESC;
// EXPECTED: 9 rows including mq_spec_zweckaenderung. PLAN_v2 will add new edges
//           to these hubs (especially mq_spec_zweckaenderung for the
//           Funktionswechsel cases).


// -----------------------------------------------------------------------------
// S38 — Sanity: existing rel-id naming pattern
// -----------------------------------------------------------------------------

MATCH ()-[r]->() WHERE r.id IS NOT NULL
WITH r, startNode(r) AS s, endNode(r) AS e
WHERE r.id <> 'r_' + s.id + '__' + type(r) + '__' + e.id
RETURN type(r) AS rel_type, count(*) AS stale_rid_count
ORDER BY stale_rid_count DESC
LIMIT 20;
// EXPECTED: 0 rows after Phase R. If any non-zero count appears, Phase R hygiene
//           has regressed; re-run before applying batch2.


// -----------------------------------------------------------------------------
// S39 — Case-specific nodes without BELEGT_IN (regression test)
// -----------------------------------------------------------------------------

MATCH (n)
WHERE any(l IN labels(n) WHERE l IN
  ['Projekt','Bauteilgruppe','Bauwerk','Wiederverwendungskette','Stadt'])
  AND NOT EXISTS { (n)-[:BELEGT_IN]->(:Quelle) }
RETURN labels(n)[0] AS label, n.id, n.name LIMIT 20;
// EXPECTED: 0 rows. After PLAN_v2 apply, this stays 0 (every new case-specific
//           node carries BELEGT_IN at creation).


// -----------------------------------------------------------------------------
// S40 — Final count freeze (compare against post-apply numbers in PLAN_v2)
// -----------------------------------------------------------------------------

MATCH (n) WITH count(n) AS nodes_before
MATCH ()-[r]->() WITH nodes_before, count(r) AS rels_before
RETURN nodes_before, rels_before;
// EXPECTED: ~2298 / ~17035. PLAN_v2 projects ~2298 + 220 = ~2518 nodes after
//           full apply (78 new from Plan 2 + ~40 receiving Bauwerk / restored
//           UMAR+ELEMENTA actors + ~80 new dossier actors + ~20 typed
//           Programm/Quelle nodes).


// =============================================================================
// END OF PRE-FLIGHT VALIDATION (PART A: tabular checks S1-S40)
// =============================================================================
//
// After running S1-S40, transcribe every "EXPECTED but got X" into
// CORRECTIONS_2026-05-20.md and amend PLAN_v2.md / patch generator accordingly
// BEFORE any backup or live apply.
// =============================================================================


// #############################################################################
// PART B — GRAPH-PRODUCING MEGA-PATTERN QUERIES (G1-G20)
// #############################################################################
//
// Purpose: 20 multi-pattern queries that connect 3-9 node types each so Neo4j
//          Browser renders rich, semantically meaningful subgraphs.
//
// ALL 20 QUERIES TESTED 2026-05-20 against live `mit-bestand`:
//          GRAPH:20  TABLE:0  EMPTY:0  ERROR:0
//          (verified via _scripts/_test_graph_queries.py)
//          Measured `full_rows` recorded in each block's header.
//
// Browser setup (run once in Browser, NOT via _run_cypher_file.py):
//     :config initialNodeDisplay: 5000
//     :config maxNeighbours: 1000
//   Then run each Gn block individually in Browser. Make sure the result
//   panel is on the "Graph" tab (not "Table" / "Text").
//
// Pattern shape used throughout:
//     MATCH path1 = (anchor)-[:REL]->(target)
//     OPTIONAL MATCH path2 = (target)-[:REL]->(...)
//     ...
//     RETURN path1, path2, path3, ...
//     LIMIT 5000;
//   Returning multiple paths per row makes Browser merge them into one
//   layout so the joins between node types are visible as edges.
// #############################################################################


// -----------------------------------------------------------------------------
// G1 — All Akteure × Projekte × Stadt × Land (+ Bauwerk overlay)         [1377]
// -----------------------------------------------------------------------------
//   The user's prototype query: "all actors in all lands and cities that work
//   on all projects". Every actor's participation path, with the project's
//   geography (Stadt → Land) and any directly used Bauwerk overlaid.

MATCH path1 = (a:Akteur)-[:BETEILIGT_AN|ASSOZIIERT_MIT_PROJEKT]->(proj:Projekt)
OPTIONAL MATCH path2 = (proj)-[:LIEGT_IN_STADT]->(:Stadt)-[:LIEGT_IN_LAND]->(:Land)
OPTIONAL MATCH path3 = (proj)-[:NUTZT_BAUWERK]->(:Bauwerk)
RETURN path1, path2, path3
LIMIT 5000;


// -----------------------------------------------------------------------------
// G2 — All Materials × Bauteilgruppen × Projekte (+ Materialgruppe + BT)  [1529]
// -----------------------------------------------------------------------------
//   The user's second prototype: "all materials of all Bauteilgruppen from all
//   projects". Materials anchored, BGs as connective tissue, projects on top,
//   plus the BG's Materialgruppe and Bauteiltyp classification.

MATCH path1 = (m:Material)<-[:NUTZT_MATERIAL]-(bg:Bauteilgruppe)<-[:HAT_BAUTEILGRUPPE]-(proj:Projekt)
OPTIONAL MATCH path2 = (bg)-[:HAT_MATERIALGRUPPE]->(:Materialgruppe)
OPTIONAL MATCH path3 = (bg)-[:HAT_BAUTEILTYP]->(:Bauteiltyp)
RETURN path1, path2, path3
LIMIT 5000;


// -----------------------------------------------------------------------------
// G3 — Full reuse pipeline: donor Bauwerk → BG → receiver Bauwerk          [392]
//      + each Bauwerk's Stadt + the BG's Projekt + Material
// -----------------------------------------------------------------------------
//   The defining transaction of the database. Each row pulls in two Bauwerken
//   (donor + receiver), their cities, the connecting BG with its project and
//   material — so a single query draws the full physical-flow story.

MATCH path1 = (donor:Bauwerk)<-[:AUS_BAUWERK]-(bg:Bauteilgruppe)-[:EINGEBAUT_IN]->(receiver:Bauwerk)
OPTIONAL MATCH path2 = (bg)<-[:HAT_BAUTEILGRUPPE]-(:Projekt)
OPTIONAL MATCH path3 = (donor)-[:LIEGT_IN_STADT]->(:Stadt)
OPTIONAL MATCH path4 = (receiver)-[:LIEGT_IN_STADT]->(:Stadt)
OPTIONAL MATCH path5 = (bg)-[:NUTZT_MATERIAL]->(:Material)
RETURN path1, path2, path3, path4, path5
LIMIT 5000;


// -----------------------------------------------------------------------------
// G4 — Programme funding cluster: Programm × Projekt × Akteur × Land       [202]
// -----------------------------------------------------------------------------
//   Programme as funding/affiliation hubs. Each funded Projekt with its
//   participating Akteure and country, in one frame.

MATCH path1 = (prog:Programm)<-[:TEIL_VON_PROGRAMM|ERHALT_FOERDERUNG_DURCH]-(proj:Projekt)
OPTIONAL MATCH path2 = (a:Akteur)-[:BETEILIGT_AN]->(proj)
OPTIONAL MATCH path3 = (proj)-[:LIEGT_IN_LAND]->(:Land)
RETURN path1, path2, path3
LIMIT 5000;


// -----------------------------------------------------------------------------
// G5 — Norm references cascading down to Bauwerk                            [79]
// -----------------------------------------------------------------------------
//   Each Norm and the BGs that reference it, expanded to the BG's project,
//   donor/receiver Bauwerk and Bauteiltyp. Reveals norms anchoring the
//   reuse-quality argument.

MATCH path1 = (n:Norm)<-[:REFERENZIERT_NORM]-(bg:Bauteilgruppe)
OPTIONAL MATCH path2 = (bg)<-[:HAT_BAUTEILGRUPPE]-(:Projekt)
OPTIONAL MATCH path3 = (bg)-[:AUS_BAUWERK|EINGEBAUT_IN]->(:Bauwerk)
OPTIONAL MATCH path4 = (bg)-[:HAT_BAUTEILTYP]->(:Bauteiltyp)
RETURN path1, path2, path3, path4
LIMIT 5000;


// -----------------------------------------------------------------------------
// G6 — Marktmodell adoption: Projekt + its BGs both pinning to same MM     [370]
// -----------------------------------------------------------------------------
//   The commercial structure: each Projekt's dominant Marktmodell, plus the
//   member BGs that share it, plus the project's Stadt and Land.

MATCH path1 = (proj:Projekt)-[:HAT_DOMINANT_MARKTMODELL]->(mm:Marktmodell)
OPTIONAL MATCH path2 = (proj)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_MARKTMODELL]->(mm)
OPTIONAL MATCH path3 = (proj)-[:LIEGT_IN_STADT]->(:Stadt)-[:LIEGT_IN_LAND]->(:Land)
RETURN path1, path2, path3
LIMIT 5000;


// -----------------------------------------------------------------------------
// G7 — Digital tooling ecosystem: Software/Tool × Projekt × Akteur         [760]
// -----------------------------------------------------------------------------
//   Every NUTZT_SOFTWARE / NUTZT_TOOL edge, plus the project context each
//   software/tool consumer participates in.

MATCH path1 = (sw:Software)<-[:NUTZT_SOFTWARE]-(n1)
OPTIONAL MATCH path2 = (t:Tool)<-[:NUTZT_TOOL]-(n2)
OPTIONAL MATCH path3 = (n1)-[:BETEILIGT_AN|ASSOZIIERT_MIT_PROJEKT]-(:Projekt)
OPTIONAL MATCH path4 = (n2)-[:BETEILIGT_AN|ASSOZIIERT_MIT_PROJEKT]-(:Projekt)
RETURN path1, path2, path3, path4
LIMIT 5000;


// -----------------------------------------------------------------------------
// G8 — BG quality stack + its Projekt (the "is this reusable?" view)      [1164]
// -----------------------------------------------------------------------------
//   For each BG: Bauteiltyp, Materialgruppe, Bauproduktstatus, Pruefung-
//   nachweis, ZustandsKlasse, and its parent Projekt — six overlays on one
//   anchor. The full quality-evidence frame in one query.

MATCH path1 = (bg:Bauteilgruppe)-[:HAT_BAUTEILTYP]->(:Bauteiltyp)
OPTIONAL MATCH path2 = (bg)-[:HAT_MATERIALGRUPPE]->(:Materialgruppe)
OPTIONAL MATCH path3 = (bg)-[:HAT_BAUPRODUKTSTATUS]->(:Bauproduktstatus)
OPTIONAL MATCH path4 = (bg)-[:HAT_PRUEFUNG]->(:PruefungNachweis)
OPTIONAL MATCH path5 = (bg)-[:HAT_ZUSTANDSKLASSE]->(:ZustandsKlasse)
OPTIONAL MATCH path6 = (bg)<-[:HAT_BAUTEILGRUPPE]-(:Projekt)
RETURN path1, path2, path3, path4, path5, path6
LIMIT 5000;


// -----------------------------------------------------------------------------
// G9 — Akteurrolle / Akteurtyp identity + Projekt + Land                  [1466]
// -----------------------------------------------------------------------------
//   Every Akteur with its role(s) and type, plus the projects it works on
//   and the countries those projects belong to.

MATCH path1 = (a:Akteur)-[:HAT_AKTEURROLLE]->(:Akteurrolle)
OPTIONAL MATCH path2 = (a)-[:HAT_AKTEURTYP]->(:Akteurtyp)
OPTIONAL MATCH path3 = (a)-[:BETEILIGT_AN]->(:Projekt)-[:LIEGT_IN_LAND]->(:Land)
RETURN path1, path2, path3
LIMIT 5000;


// -----------------------------------------------------------------------------
// G10 — Quelle citation web: every Akteur/Projekt/BG/Bauwerk → same Quelle [5000+]
// -----------------------------------------------------------------------------
//   Each row anchors on an Akteur→Quelle citation and overlays the Projekte,
//   BGs, and Bauwerken that cite the SAME source. Highlights evidence hubs.

MATCH path1 = (a:Akteur)-[:BELEGT_IN]->(q:Quelle)
OPTIONAL MATCH path2 = (p:Projekt)-[:BELEGT_IN]->(q)
OPTIONAL MATCH path3 = (bg:Bauteilgruppe)-[:BELEGT_IN]->(q)
OPTIONAL MATCH path4 = (bw:Bauwerk)-[:BELEGT_IN]->(q)
RETURN path1, path2, path3, path4
LIMIT 5000;


// -----------------------------------------------------------------------------
// G11 — Wiederverwendungskette explosion                                   [555]
// -----------------------------------------------------------------------------
//   Each named reuse chain (k_*) with member BGs, their donor + receiver
//   Bauwerken, the BGs' projects, and the Bauteiltyp involved. The narrative
//   unit of the database in one frame.

MATCH path1 = (k:Wiederverwendungskette)<-[:TEIL_VON_KETTE]-(bg:Bauteilgruppe)
OPTIONAL MATCH path2 = (bg)-[:AUS_BAUWERK]->(:Bauwerk)
OPTIONAL MATCH path3 = (bg)-[:EINGEBAUT_IN]->(:Bauwerk)
OPTIONAL MATCH path4 = (bg)<-[:HAT_BAUTEILGRUPPE]-(:Projekt)
OPTIONAL MATCH path5 = (bg)-[:HAT_BAUTEILTYP]->(:Bauteiltyp)
RETURN path1, path2, path3, path4, path5
LIMIT 5000;


// -----------------------------------------------------------------------------
// G12 — Cross-border reuse: donor → receiver chains with both Länder       [339]
// -----------------------------------------------------------------------------
//   Forces both donor- and receiver-Land into the result so cross-country
//   reuse is visible at a glance. Material overlay tags the chain.

MATCH path1 = (donor:Bauwerk)-[:LIEGT_IN_LAND]->(:Land)
MATCH path2 = (donor)<-[:AUS_BAUWERK]-(bg:Bauteilgruppe)-[:EINGEBAUT_IN]->(receiver:Bauwerk)
MATCH path3 = (receiver)-[:LIEGT_IN_LAND]->(:Land)
OPTIONAL MATCH path4 = (bg)-[:NUTZT_MATERIAL]->(:Material)
RETURN path1, path2, path3, path4
LIMIT 5000;


// -----------------------------------------------------------------------------
// G13 — Bauobjekt typology: Bauwerk × Rolle × Klasse × Stadt × Projekt     [242]
// -----------------------------------------------------------------------------
//   Each Bauwerk with its Bauobjektrolle (donor/receiver/…), Bauobjektklasse
//   (Gebäude / Pavillon / …), location, and the Projekt that uses it.

MATCH path1 = (bw:Bauwerk)-[:HAT_BAUOBJEKTROLLE]->(:Bauobjektrolle)
OPTIONAL MATCH path2 = (bw)-[:HAT_BAUOBJEKTKLASSE]->(:Bauobjektklasse)
OPTIONAL MATCH path3 = (bw)-[:LIEGT_IN_STADT]->(:Stadt)
OPTIONAL MATCH path4 = (bw)<-[:NUTZT_BAUWERK]-(:Projekt)
RETURN path1, path2, path3, path4
LIMIT 5000;


// -----------------------------------------------------------------------------
// G14 — Materialgruppe × Marktmodell cross-tab as a graph                 [1152]
// -----------------------------------------------------------------------------
//   For each Materialgruppe: its BGs, the Marktmodelle those BGs use, the
//   underlying Material, and the BGs' projects. Reveals which material
//   classes flow via which commercial models.

MATCH path1 = (mg:Materialgruppe)<-[:HAT_MATERIALGRUPPE]-(bg:Bauteilgruppe)
OPTIONAL MATCH path2 = (bg)-[:HAT_MARKTMODELL]->(:Marktmodell)
OPTIONAL MATCH path3 = (bg)-[:NUTZT_MATERIAL]->(:Material)
OPTIONAL MATCH path4 = (bg)<-[:HAT_BAUTEILGRUPPE]-(:Projekt)
RETURN path1, path2, path3, path4
LIMIT 5000;


// -----------------------------------------------------------------------------
// G15 — Akteurtyp landscape: type × Akteur × Projekt × Land × Rolle       [1571]
// -----------------------------------------------------------------------------
//   Each Akteurtyp with the Akteure of that type, their projects, the
//   countries those projects sit in, and the actor's role on each side.

MATCH path1 = (at:Akteurtyp)<-[:HAT_AKTEURTYP]-(a:Akteur)
OPTIONAL MATCH path2 = (a)-[:BETEILIGT_AN]->(proj:Projekt)
OPTIONAL MATCH path3 = (proj)-[:LIEGT_IN_LAND]->(:Land)
OPTIONAL MATCH path4 = (a)-[:HAT_AKTEURROLLE]->(:Akteurrolle)
RETURN path1, path2, path3, path4
LIMIT 5000;


// -----------------------------------------------------------------------------
// G16 — Funktionswechsel (Zweckaenderung) cluster                          [117]
// -----------------------------------------------------------------------------
//   Projekte pinned to mq_spec_zweckaenderung (the spec-change matching-
//   quality), with their BGs and the donor + receiver Bauwerken underneath.

MATCH path1 = (mq:MatchingQualitaet {id:'mq_spec_zweckaenderung'})<-[:HAT_MATCHINGQUALITAET]-(proj:Projekt)
OPTIONAL MATCH path2 = (proj)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
OPTIONAL MATCH path3 = (bg)-[:AUS_BAUWERK]->(:Bauwerk)
OPTIONAL MATCH path4 = (bg)-[:EINGEBAUT_IN]->(:Bauwerk)
RETURN path1, path2, path3, path4
LIMIT 5000;


// -----------------------------------------------------------------------------
// G17 — Flagship project deep-dive (8 projects, 2 hops out)              [5000+]
// -----------------------------------------------------------------------------
//   Pick 8 anchor projects and expand 2 hops in every direction. Returns the
//   full local star: actors, BGs, Bauwerken, sources, programme, geography,
//   ontology — everything within reach.

MATCH path = (proj:Projekt)-[*1..2]-(other)
WHERE proj.id IN [
  'p_umar_unit', 'p_elementa_walkeweg', 'p_circl_abn_amro',
  'p_lysp8_basel', 'p_obk_27', 'p_pavilion_circl_amsterdam',
  'p_re_use_hoefe', 'p_stuttgart_210'
]
RETURN path
LIMIT 5000;


// -----------------------------------------------------------------------------
// G18 — Geographic atlas: Stadt × Land × Bauwerken × Projekte             [375]
// -----------------------------------------------------------------------------
//   For every city: its country, the buildings located there, the projects
//   based there. A complete geographic carpet for the whole database.

MATCH path1 = (s:Stadt)-[:LIEGT_IN_LAND]->(:Land)
OPTIONAL MATCH path2 = (:Bauwerk)-[:LIEGT_IN_STADT]->(s)
OPTIONAL MATCH path3 = (:Projekt)-[:LIEGT_IN_STADT]->(s)
RETURN path1, path2, path3
LIMIT 5000;


// -----------------------------------------------------------------------------
// G19 — Cross-project Akteur bridges (+ Land + Rolle context)              [605]
// -----------------------------------------------------------------------------
//   Only actors active on ≥2 projects. For each: every project they touch,
//   each project's country, and the actor's controlled-vocab role. The
//   connective tissue of the reuse community.

MATCH (a:Akteur)-[:BETEILIGT_AN|ASSOZIIERT_MIT_PROJEKT]-(p:Projekt)
WITH a, count(DISTINCT p) AS proj_count
WHERE proj_count > 1
MATCH path1 = (a)-[:BETEILIGT_AN|ASSOZIIERT_MIT_PROJEKT]-(proj:Projekt)
OPTIONAL MATCH path2 = (proj)-[:LIEGT_IN_LAND]->(:Land)
OPTIONAL MATCH path3 = (a)-[:HAT_AKTEURROLLE]->(:Akteurrolle)
RETURN path1, path2, path3
LIMIT 5000;


// -----------------------------------------------------------------------------
// G20 — THE BIG ONE: Akteur + Projekt + Programm + BG + Material         [5000+]
//       + 2 Bauwerken + Stadt + Land + Quelle in one query
// -----------------------------------------------------------------------------
//   Single mega-pattern that draws the entire story shape behind a reuse
//   project: who participates, which programme funds it, where it is, which
//   BG carries the reused material, which Bauwerken supply and receive,
//   and which source documents the case.

MATCH path1 = (proj:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
OPTIONAL MATCH path2 = (:Akteur)-[:BETEILIGT_AN]->(proj)
OPTIONAL MATCH path3 = (proj)-[:TEIL_VON_PROGRAMM]->(:Programm)
OPTIONAL MATCH path4 = (proj)-[:LIEGT_IN_STADT]->(:Stadt)-[:LIEGT_IN_LAND]->(:Land)
OPTIONAL MATCH path5 = (bg)-[:NUTZT_MATERIAL]->(:Material)
OPTIONAL MATCH path6 = (bg)-[:AUS_BAUWERK]->(:Bauwerk)
OPTIONAL MATCH path7 = (bg)-[:EINGEBAUT_IN]->(:Bauwerk)
OPTIONAL MATCH path8 = (proj)-[:BELEGT_IN]->(:Quelle)
RETURN path1, path2, path3, path4, path5, path6, path7, path8
LIMIT 5000;


// =============================================================================
// END OF PART B — GRAPH-PRODUCING MEGA-PATTERNS (G1-G20)
// =============================================================================
//
// Tips for use in Neo4j Browser:
//   - Set node display ceiling: `:config initialNodeDisplay: 5000`
//   - Set per-node neighbour cap:  `:config maxNeighbours: 1000`
//   - Switch to "Graph" tab after each query (not "Table" / "Text").
//   - For very large results, drag the result panel to full screen and
//     use the layout button (force/hierarchy) to declutter.
//
// To re-verify these queries still return graphs (e.g. after a migration):
//   python _scripts/_test_graph_queries.py \
//       --cypher _neo4j/intake/runs/2026-05-20_inbox_batch2_import/pre_flight_validation.cypher \
//       --prefix G
//   Expected output:  GRAPH:20  TABLE:0  EMPTY:0  ERROR:0
//
// These queries are READ-ONLY. Safe to run in any database, any time.
// =============================================================================
