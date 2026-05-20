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
// END OF PRE-FLIGHT VALIDATION
// =============================================================================
//
// After running S1-S40, transcribe every "EXPECTED but got X" into
// CORRECTIONS_2026-05-20.md and amend PLAN_v2.md / patch generator accordingly
// BEFORE any backup or live apply.
// =============================================================================
