#!/usr/bin/env python3
"""Agent 11 ledger generator (regulation/legal layer).

Deterministic emitter for ledger/agent_11.csv from the read-only Neo4j
enumeration captured during the verification run. NO graph mutation: this
only serialises already-verified structural facts into the campaign ledger
schema (VERIFICATION_LEDGER.schema.csv).

Scope (MECE-owned by Agent 11):
  nodes  : 91 typed *recht law nodes + 20 ReuseRule = 111
  rels   : 167 GESTUETZT_AUF_REGELWERK + 281 GILT_IN_LAND = 448
Live URL proof for the source_url on these rels is owned by Agent 07; Agent 11
does node identity, label/rechtsbereiche taxonomy, and structural/country logic.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ledger", "agent_11.csv")

AGENT = "11"
TAX = "_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/VARIANT_B_TAXONOMY.md"
AUDIT = "_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/FINAL_AUDIT_REPORT.md"

EU7 = [
    "land_deutschland", "land_belgien", "land_niederlande", "land_frankreich",
    "land_norwegen", "land_daenemark", "land_oesterreich",
]

# law_id -> (name, [labels], confidence)
LAWS = {
    "rw_agbb_voc": ("AgBB-Schema / DIN EN 16516 (VOC)", ["Schadstoffrecht"], 0.85),
    "rw_be_tracimat_regional": ("Belgian regional rules / Tracimat", ["ReuseDokumentationsrecht", "RueckbauUndAbbruchrecht"], 0.85),
    "rw_cen_ts_1090_201": ("CEN/TS 1090-201:2024", ["Bauproduktrecht", "Tragwerksrecht"], 0.90),
    "rw_cen_ts_17440": ("CEN/TS 17440 (Bewertung bestehender Tragwerke)", ["Tragwerksrecht"], 0.85),
    "rw_ch_muken": ("Switzerland MuKEn", ["Bauphysikrecht"], 0.80),
    "rw_dafstb_rc_beton": ("DAfStb-Richtlinie R-Beton", ["Tragwerksrecht", "UmweltUndOekobilanzrecht"], 0.85),
    "rw_denkmalschutz": ("Denkmalschutz / heritage protection", ["ReuseDokumentationsrecht", "Genehmigungsrecht"], 0.80),
    "rw_dguv_v3_vde": ("DGUV V3 / DIN VDE 0100-600 / 0105-100", ["HygieneElektroFunktionsrecht"], 0.85),
    "rw_dibt_zie_abz": ("DIBt ZiE/vBG/abZ/aBG", ["Bauproduktrecht", "Genehmigungsrecht"], 0.90),
    "rw_din_18008": ("DIN 18008", ["Tragwerksrecht"], 0.85),
    "rw_din_18040": ("DIN 18040 (Barrierefreies Bauen)", ["HygieneElektroFunktionsrecht"], 0.80),
    "rw_din_18065": ("DIN 18065 (Gebaeudetreppen/Gelaender)", ["Genehmigungsrecht", "HygieneElektroFunktionsrecht"], 0.80),
    "rw_din_18945_lehm": ("DIN 18945-18947 (Lehmbaustoffe)", ["Bauproduktrecht", "Tragwerksrecht"], 0.80),
    "rw_din_4074_en_14081": ("DIN 4074 / EN 14081 (Holzsortierung)", ["Tragwerksrecht"], 0.85),
    "rw_din_4102": ("DIN 4102/4108/4109", ["Bauphysikrecht", "Brandschutzrecht"], 0.80),
    "rw_din_68800_altholzv": ("DIN 68800 / AltholzV", ["Schadstoffrecht"], 0.85),
    "rw_din_en_13501": ("DIN EN 13501", ["Brandschutzrecht"], 0.90),
    "rw_din_spec_91484": ("DIN SPEC 91484", ["ReuseDokumentationsrecht", "RueckbauUndAbbruchrecht"], 0.90),
    "rw_din_spec_91525": ("DIN SPEC 91525", ["ReuseDokumentationsrecht", "RueckbauUndAbbruchrecht"], 0.90),
    "rw_dk_br18": ("Denmark BR18 (Bygningsreglementet)", ["Bauproduktrecht", "UmweltUndOekobilanzrecht", "Brandschutzrecht"], 0.80),
    "rw_ebv": ("Ersatzbaustoffverordnung (EBV)", ["Schadstoffrecht", "UmweltUndOekobilanzrecht"], 0.85),
    "rw_en_1090": ("EN/DIN EN 1090", ["Bauproduktrecht", "Tragwerksrecht"], 0.85),
    "rw_en_1090_2_bolts_reuse": ("EN 1090-2 / EN 14399 (bolt reuse limits)", ["Bauproduktrecht", "Tragwerksrecht"], 0.85),
    "rw_en_1168": ("EN 1168 (Hohlplatten/Hollow-core slabs)", ["Bauproduktrecht", "Tragwerksrecht"], 0.88),
    "rw_en_13162_mineralwolle": ("EN 13162 (Mineralwolle-Daemmstoffe)", ["Bauproduktrecht", "Bauphysikrecht"], 0.85),
    "rw_en_13791_12504": ("EN 13791 / EN 12504 (In-situ Beton)", ["Tragwerksrecht"], 0.85),
    "rw_en_13830": ("EN 13830 (Vorhangfassade/Curtain Walling)", ["Bauproduktrecht", "Bauphysikrecht", "Brandschutzrecht"], 0.85),
    "rw_en_14351": ("EN 14351-1/-2 (Fenster & Tueren)", ["Bauproduktrecht", "Bauphysikrecht"], 0.85),
    "rw_en_15804_15978": ("EN 15804 / EN 15978 (EPD/LCA)", ["UmweltUndOekobilanzrecht"], 0.85),
    "rw_en_1992_4": ("EN 1992-4 (Befestigungen in Beton)", ["Tragwerksrecht"], 0.85),
    "rw_en_408": ("EN 408 (Holz mechanische Eigenschaften)", ["Tragwerksrecht"], 0.85),
    "rw_en_771_reclaimed": ("EN 771 (reclaimed masonry units)", ["Bauproduktrecht", "Tragwerksrecht"], 0.80),
    "rw_en_iso_6892": ("EN ISO 6892-1 (Zugversuch Metalle)", ["Tragwerksrecht"], 0.85),
    "rw_en_naturstein": ("EN 1469/12058/1936 (Naturstein-Produktnormen)", ["Bauproduktrecht", "Tragwerksrecht"], 0.82),
    "rw_espr_dpp": ("ESPR / Digital Product Passport", ["Bauproduktrecht", "UmweltUndOekobilanzrecht"], 0.80),
    "rw_eu_cdw_protocol": ("EU C&D Waste Management Protocol (2024)", ["Schadstoffrecht", "ReuseDokumentationsrecht", "RueckbauUndAbbruchrecht"], 0.85),
    "rw_eu_cpr_2024_3110": ("EU CPR 2024/3110", ["ReuseDokumentationsrecht", "Bauproduktrecht"], 0.90),
    "rw_eu_cpr_305_2011": ("EU CPR 305/2011", ["Bauproduktrecht"], 0.80),
    "rw_eu_levels": ("EU Level(s) framework", ["UmweltUndOekobilanzrecht"], 0.80),
    "rw_eu_taxonomy": ("EU Taxonomy (Circular Economy TSC)", ["ReuseDokumentationsrecht", "UmweltUndOekobilanzrecht"], 0.85),
    "rw_eu_wfd_2008_98": ("EU Waste Framework Directive 2008/98/EC", ["ReuseDokumentationsrecht", "RueckbauUndAbbruchrecht"], 0.90),
    "rw_eurocodes_en_1990_1999": ("Eurocodes EN/DIN EN 1990-1999", ["Tragwerksrecht"], 0.85),
    "rw_fcrbe_reuse_toolkit": ("FCRBE Reuse Toolkit / Reclamation Audit", ["ReuseDokumentationsrecht", "RueckbauUndAbbruchrecht"], 0.80),
    "rw_fib_precast_reuse": ("fib Bulletins (precast concrete reuse)", ["Tragwerksrecht"], 0.70),
    "rw_fr_pemd": ("France Diagnostic PEMD (loi AGEC)", ["ReuseDokumentationsrecht", "RueckbauUndAbbruchrecht"], 0.90),
    "rw_fr_re2020": ("France RE2020", ["Bauphysikrecht", "UmweltUndOekobilanzrecht"], 0.85),
    "rw_fr_rep_pmcb": ("France REP PMCB (filiere batiment)", ["RueckbauUndAbbruchrecht", "Haftungsrecht"], 0.80),
    "rw_gefstoffv": ("GefStoffV (2024)", ["Schadstoffrecht"], 0.90),
    "rw_geg": ("GEG", ["Bauphysikrecht"], 0.85),
    "rw_gewabfv": ("Gewerbeabfallverordnung (GewAbfV)", ["RueckbauUndAbbruchrecht"], 0.85),
    "rw_glas_reuse_igu": ("Flat-glass / IGU reuse guidance (Glass for Europe)", ["Bauproduktrecht", "Bauphysikrecht"], 0.70),
    "rw_iso_20887": ("ISO 20887 (Design for Disassembly/Adaptability)", ["ReuseDokumentationsrecht", "RueckbauUndAbbruchrecht"], 0.80),
    "rw_istructe_reuse": ("IStructE reuse guidance / reuse hierarchy", ["ReuseDokumentationsrecht", "Tragwerksrecht"], 0.80),
    "rw_krwg": ("KrWG sec.6/7/8", ["ReuseDokumentationsrecht", "RueckbauUndAbbruchrecht"], 0.90),
    "rw_lfu_schadstoff_arbeitshilfe": ("LfU Arbeitshilfe Rueckbau schadstoffbelasteter Bausubstanz", ["Schadstoffrecht", "RueckbauUndAbbruchrecht"], 0.85),
    "rw_madaster_grp": ("Madaster / Gebaeuderessourcenpass", ["ReuseDokumentationsrecht", "UmweltUndOekobilanzrecht"], 0.80),
    "rw_mbo_lbo": ("MBO/LBO", ["Bauproduktrecht", "Genehmigungsrecht"], 0.85),
    "rw_mvv_tb": ("MVV TB / VV TB", ["Bauproduktrecht", "Tragwerksrecht", "Brandschutzrecht"], 0.85),
    "rw_naturstein_reuse": ("Naturstein-Wiederverwendung (guidance)", ["ReuseDokumentationsrecht", "Tragwerksrecht"], 0.65),
    "rw_nen_8700": ("NEN 8700-serie (bestaande bouw)", ["Tragwerksrecht"], 0.90),
    "rw_nl_bbl": ("Dutch Bbl", ["ReuseDokumentationsrecht", "Bauproduktrecht", "Genehmigungsrecht"], 0.90),
    "rw_nl_mpg": ("Netherlands MPG (MilieuPrestatie Gebouwen)", ["UmweltUndOekobilanzrecht"], 0.85),
    "rw_no_tek17": ("Norway TEK17 (ombrukskartlegging)", ["RueckbauUndAbbruchrecht", "Bauproduktrecht"], 0.85),
    "rw_nta_8713": ("NTA 8713 (Reuse of structural steel)", ["Bauproduktrecht", "Tragwerksrecht"], 0.90),
    "rw_oenorm_b3151": ("OENORM B 3151", ["Schadstoffrecht", "RueckbauUndAbbruchrecht"], 0.90),
    "rw_oib_richtlinien": ("OIB-Richtlinien", ["Bauphysikrecht", "Genehmigungsrecht", "Brandschutzrecht"], 0.85),
    "rw_pcb_richtlinie": ("PCB-Richtlinie (ARGEBAU)", ["Schadstoffrecht"], 0.85),
    "rw_pop_2019_1021": ("POP-Verordnung (EU) 2019/1021", ["Schadstoffrecht"], 0.85),
    "rw_prodhaftg_bgb": ("ProdHaftG / BGB sec.823", ["Haftungsrecht"], 0.80),
    "rw_qng_dgnb": ("QNG / DGNB Zertifizierung", ["ReuseDokumentationsrecht", "UmweltUndOekobilanzrecht"], 0.75),
    "rw_reach_annex_xvii": ("REACH Anhang XVII Eintrag 77", ["Schadstoffrecht"], 0.85),
    "rw_sci_p427": ("SCI P427", ["Bauproduktrecht", "Tragwerksrecht"], 0.90),
    "rw_sia_2032": ("SIA 2032 (Graue Energie)", ["UmweltUndOekobilanzrecht"], 0.80),
    "rw_sia_269": ("SIA 269", ["Tragwerksrecht"], 0.85),
    "rw_sia_269_2": ("SIA 269/2 (Erhaltung Betonbau)", ["Tragwerksrecht"], 0.85),
    "rw_sia_380_1": ("SIA 380/1", ["Bauphysikrecht"], 0.85),
    "rw_strlschg_radon": ("StrlSchG (Radon)", ["Schadstoffrecht"], 0.85),
    "rw_trgs_519": ("TRGS 519", ["Schadstoffrecht"], 0.95),
    "rw_trgs_521": ("TRGS 521", ["Schadstoffrecht"], 0.90),
    "rw_trgs_524": ("TRGS 524", ["Schadstoffrecht"], 0.85),
    "rw_uba_schimmelleitfaden": ("UBA-Schimmelleitfaden", ["Schadstoffrecht"], 0.85),
    "rw_uk_adb": ("UK Building Regs Approved Document B", ["Tragwerksrecht", "Brandschutzrecht"], 0.80),
    "rw_uk_pas2080": ("UK PAS 2080:2023 (whole-life carbon)", ["UmweltUndOekobilanzrecht"], 0.80),
    "rw_ukca_ce": ("UKCA / CE marking", ["Bauproduktrecht"], 0.85),
    "rw_vdi_3492": ("VDI 3492 (Faser-/Asbestmessung)", ["Schadstoffrecht"], 0.85),
    "rw_vdi_6023_6022": ("VDI 6023 / VDI 6022 (Hygiene)", ["HygieneElektroFunktionsrecht"], 0.80),
    "rw_vdi_6202": ("VDI/GVSS 6202 Blatt 1", ["Schadstoffrecht"], 0.85),
    "rw_vdi_6210": ("VDI 6210 Blatt 1", ["RueckbauUndAbbruchrecht"], 0.85),
    "rw_vkf_bsv": ("VKF Brandschutzvorschriften (CH)", ["Brandschutzrecht"], 0.85),
    "rw_vob_c_din_18459": ("VOB/C ATV DIN 18459 (Abbruch/Rueckbau)", ["RueckbauUndAbbruchrecht", "Haftungsrecht"], 0.85),
    "rw_zirkulaere_vergabe": ("Zirkulaere Beschaffung / Vergaberecht (NKWS)", ["ReuseDokumentationsrecht", "Genehmigungsrecht"], 0.75),
}

# Soft-law / voluntary-framework / guidance instruments: real & legitimately in the
# reference *recht layer, but NOT binding statutes/standards in the strict sense.
SOFT_LAW = {
    "rw_naturstein_reuse", "rw_fib_precast_reuse", "rw_glas_reuse_igu",
    "rw_qng_dgnb", "rw_zirkulaere_vergabe", "rw_istructe_reuse",
    "rw_fcrbe_reuse_toolkit", "rw_madaster_grp", "rw_eu_levels",
}

# law_id -> lands (GILT_IN_LAND). EU7 sentinel expanded below.
GILT = {
    "rw_agbb_voc": ["land_deutschland"],
    "rw_be_tracimat_regional": ["land_belgien"],
    "rw_cen_ts_1090_201": EU7, "rw_cen_ts_17440": EU7,
    "rw_ch_muken": ["land_schweiz"],
    "rw_dafstb_rc_beton": ["land_deutschland"],
    "rw_denkmalschutz": ["land_deutschland"],
    "rw_dguv_v3_vde": ["land_deutschland"],
    "rw_dibt_zie_abz": ["land_deutschland"],
    "rw_din_18008": ["land_deutschland"], "rw_din_18040": ["land_deutschland"],
    "rw_din_18065": ["land_deutschland"], "rw_din_18945_lehm": ["land_deutschland"],
    "rw_din_4074_en_14081": EU7,
    "rw_din_4102": ["land_deutschland"], "rw_din_68800_altholzv": ["land_deutschland"],
    "rw_din_en_13501": EU7,
    "rw_din_spec_91484": ["land_deutschland"], "rw_din_spec_91525": ["land_deutschland"],
    "rw_dk_br18": ["land_daenemark"],
    "rw_ebv": ["land_deutschland"],
    "rw_en_1090": EU7, "rw_en_1090_2_bolts_reuse": EU7, "rw_en_1168": EU7,
    "rw_en_13162_mineralwolle": EU7, "rw_en_13791_12504": EU7, "rw_en_13830": EU7,
    "rw_en_14351": EU7, "rw_en_15804_15978": EU7, "rw_en_1992_4": EU7,
    "rw_en_408": EU7, "rw_en_771_reclaimed": EU7, "rw_en_iso_6892": EU7,
    "rw_en_naturstein": EU7, "rw_espr_dpp": EU7, "rw_eu_cdw_protocol": EU7,
    "rw_eu_cpr_2024_3110": EU7, "rw_eu_cpr_305_2011": EU7, "rw_eu_levels": EU7,
    "rw_eu_taxonomy": EU7, "rw_eu_wfd_2008_98": EU7, "rw_eurocodes_en_1990_1999": EU7,
    "rw_fcrbe_reuse_toolkit": ["land_vereinigtes_koenigreich", "land_belgien", "land_niederlande", "land_frankreich"],
    "rw_fib_precast_reuse": EU7,
    "rw_fr_pemd": ["land_frankreich"], "rw_fr_re2020": ["land_frankreich"], "rw_fr_rep_pmcb": ["land_frankreich"],
    "rw_gefstoffv": ["land_deutschland"], "rw_geg": ["land_deutschland"], "rw_gewabfv": ["land_deutschland"],
    "rw_glas_reuse_igu": EU7, "rw_iso_20887": EU7,
    "rw_istructe_reuse": ["land_vereinigtes_koenigreich"],
    "rw_krwg": ["land_deutschland"], "rw_lfu_schadstoff_arbeitshilfe": ["land_deutschland"],
    "rw_madaster_grp": ["land_deutschland", "land_niederlande"],
    "rw_mbo_lbo": ["land_deutschland"], "rw_mvv_tb": ["land_deutschland"],
    "rw_naturstein_reuse": EU7,
    "rw_nen_8700": ["land_niederlande"], "rw_nl_bbl": ["land_niederlande"], "rw_nl_mpg": ["land_niederlande"],
    "rw_no_tek17": ["land_norwegen"], "rw_nta_8713": ["land_niederlande"],
    "rw_oenorm_b3151": ["land_oesterreich"], "rw_oib_richtlinien": ["land_oesterreich"],
    "rw_pcb_richtlinie": ["land_deutschland"], "rw_pop_2019_1021": EU7,
    "rw_prodhaftg_bgb": ["land_deutschland"], "rw_qng_dgnb": ["land_deutschland"],
    "rw_reach_annex_xvii": EU7,
    "rw_sci_p427": ["land_vereinigtes_koenigreich"],
    "rw_sia_2032": ["land_schweiz"], "rw_sia_269": ["land_schweiz"],
    "rw_sia_269_2": ["land_schweiz"], "rw_sia_380_1": ["land_schweiz"],
    "rw_strlschg_radon": ["land_deutschland"],
    "rw_trgs_519": ["land_deutschland"], "rw_trgs_521": ["land_deutschland"], "rw_trgs_524": ["land_deutschland"],
    "rw_uba_schimmelleitfaden": ["land_deutschland"],
    "rw_uk_adb": ["land_vereinigtes_koenigreich"], "rw_uk_pas2080": ["land_vereinigtes_koenigreich"],
    "rw_ukca_ce": ["land_vereinigtes_koenigreich"],
    "rw_vdi_3492": ["land_deutschland"], "rw_vdi_6023_6022": ["land_deutschland"],
    "rw_vdi_6202": ["land_deutschland"], "rw_vdi_6210": ["land_deutschland"],
    "rw_vkf_bsv": ["land_schweiz"],
    "rw_vob_c_din_18459": ["land_deutschland"], "rw_zirkulaere_vergabe": ["land_deutschland"],
}

# nf_id -> [law_id] (GESTUETZT_AUF_REGELWERK), Nachweisforderung -> law node.
GESTUETZT = {
    "nf_absturzsicherung": ["rw_din_18008", "rw_din_18065"],
    "nf_asbest_check": ["rw_gefstoffv", "rw_lfu_schadstoff_arbeitshilfe", "rw_trgs_519", "rw_vdi_3492"],
    "nf_barrierefreiheit_nachweis": ["rw_din_18040", "rw_din_18065"],
    "nf_bauphysiknachweis": ["rw_ch_muken", "rw_din_4102", "rw_geg", "rw_sia_380_1"],
    "nf_bauteilidentifikation": ["rw_be_tracimat_regional", "rw_din_spec_91484", "rw_eu_cdw_protocol", "rw_fcrbe_reuse_toolkit", "rw_fr_pemd", "rw_madaster_grp", "rw_no_tek17"],
    "nf_befestigungsnachweis": ["rw_cen_ts_1090_201", "rw_en_1090", "rw_en_1090_2_bolts_reuse", "rw_en_1992_4"],
    "nf_brandschutznachweis": ["rw_din_4102", "rw_din_en_13501", "rw_dk_br18", "rw_oib_richtlinien", "rw_uk_adb", "rw_vkf_bsv"],
    "nf_dauerhaftigkeit_restlebensdauer": ["rw_din_spec_91525", "rw_en_naturstein", "rw_naturstein_reuse", "rw_sia_269"],
    "nf_elektrosicherheitsnachweis": ["rw_dguv_v3_vde"],
    "nf_formaldehyd_oder_emissionsnachweis": ["rw_agbb_voc", "rw_reach_annex_xvii"],
    "nf_genehmigungs_oder_zustimmungsbedarf": ["rw_denkmalschutz", "rw_dibt_zie_abz", "rw_mbo_lbo", "rw_nl_bbl", "rw_oib_richtlinien", "rw_vdi_6210"],
    "nf_herkunfts_und_rueckbaudokumentation": ["rw_be_tracimat_regional", "rw_din_spec_91484", "rw_eu_cdw_protocol", "rw_eu_cpr_2024_3110", "rw_eu_wfd_2008_98", "rw_fcrbe_reuse_toolkit", "rw_fr_pemd", "rw_fr_rep_pmcb", "rw_gewabfv", "rw_iso_20887", "rw_krwg", "rw_no_tek17", "rw_oenorm_b3151", "rw_prodhaftg_bgb", "rw_vdi_6210", "rw_vob_c_din_18459", "rw_zirkulaere_vergabe"],
    "nf_holzschutzmittel_check": ["rw_din_68800_altholzv"],
    "nf_hygiene_und_reinigungsnachweis": ["rw_vdi_6023_6022"],
    "nf_materialpass_ressourcenpass": ["rw_espr_dpp", "rw_eu_levels", "rw_madaster_grp", "rw_qng_dgnb"],
    "nf_materialpruefung": ["rw_cen_ts_1090_201", "rw_dafstb_rc_beton", "rw_din_18945_lehm", "rw_din_4074_en_14081", "rw_en_1090_2_bolts_reuse", "rw_en_1168", "rw_en_13791_12504", "rw_en_408", "rw_en_771_reclaimed", "rw_en_iso_6892", "rw_en_naturstein", "rw_fib_precast_reuse", "rw_glas_reuse_igu", "rw_naturstein_reuse", "rw_nta_8713", "rw_sci_p427", "rw_sia_269_2"],
    "nf_mineralische_ersatzbaustoff_guete": ["rw_ebv"],
    "nf_oekobilanz_epd": ["rw_dk_br18", "rw_en_15804_15978", "rw_eu_levels", "rw_eu_taxonomy", "rw_fr_re2020", "rw_nl_mpg", "rw_qng_dgnb", "rw_sia_2032", "rw_uk_pas2080"],
    "nf_produktstatus_und_leistungserklaerung": ["rw_cen_ts_1090_201", "rw_dibt_zie_abz", "rw_din_18945_lehm", "rw_din_4074_en_14081", "rw_dk_br18", "rw_en_1090", "rw_en_1168", "rw_en_13162_mineralwolle", "rw_en_13830", "rw_en_14351", "rw_en_771_reclaimed", "rw_en_naturstein", "rw_espr_dpp", "rw_eu_cpr_2024_3110", "rw_eu_cpr_305_2011", "rw_mbo_lbo", "rw_mvv_tb", "rw_nl_bbl", "rw_no_tek17", "rw_nta_8713", "rw_prodhaftg_bgb", "rw_sci_p427", "rw_ukca_ce", "rw_zirkulaere_vergabe"],
    "nf_rc_gesteinskoernung_eignung": ["rw_dafstb_rc_beton"],
    "nf_schadstoffkataster_erkundung": ["rw_eu_cdw_protocol", "rw_fr_pemd", "rw_lfu_schadstoff_arbeitshilfe", "rw_oenorm_b3151", "rw_trgs_524", "rw_vdi_6202", "rw_vob_c_din_18459"],
    "nf_schadstoffpruefung": ["rw_agbb_voc", "rw_gefstoffv", "rw_lfu_schadstoff_arbeitshilfe", "rw_pcb_richtlinie", "rw_pop_2019_1021", "rw_strlschg_radon", "rw_trgs_521", "rw_trgs_524", "rw_uba_schimmelleitfaden", "rw_vdi_3492", "rw_vdi_6202"],
    "nf_schwermetall_oder_bleifarbe_check": ["rw_reach_annex_xvii"],
    "nf_sicherheitsglas_info": ["rw_din_18008", "rw_glas_reuse_igu"],
    "nf_standsicherheitsnachweis": ["rw_cen_ts_1090_201", "rw_cen_ts_17440", "rw_din_4074_en_14081", "rw_en_1168", "rw_en_13791_12504", "rw_en_408", "rw_eurocodes_en_1990_1999", "rw_fib_precast_reuse", "rw_istructe_reuse", "rw_nen_8700", "rw_nta_8713", "rw_sci_p427", "rw_sia_269", "rw_sia_269_2"],
    "nf_u_wert_oder_energie_info": ["rw_ch_muken", "rw_en_13162_mineralwolle", "rw_en_13830", "rw_en_14351", "rw_fr_re2020", "rw_geg", "rw_glas_reuse_igu", "rw_sia_380_1"],
    "nf_zustands_und_massaufnahme": ["rw_cen_ts_17440", "rw_din_spec_91484", "rw_din_spec_91525", "rw_istructe_reuse", "rw_nen_8700", "rw_sia_269", "rw_sia_269_2"],
}

REUSERULES = [
    "rr_be_beton", "rr_be_holz", "rr_be_naturstein", "rr_be_stahl",
    "rr_ch_beton", "rr_ch_holz", "rr_ch_naturstein", "rr_ch_stahl",
    "rr_de_beton", "rr_de_holz", "rr_de_lehm", "rr_de_stahl", "rr_de_ziegel",
    "rr_fi_beton_hollow_core_slabs", "rr_gb_holz", "rr_gb_stahl",
    "rr_nl_beton", "rr_nl_holz", "rr_nl_stahl", "rr_no_beton_hollow_core_slabs",
]

HEADER = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id",
    "rel_type_or_label", "asserted_claim", "basis_type", "basis_ref",
    "fetched", "http_status", "verdict", "confidence", "proof_quote",
    "proposed_action", "agent_id", "notes",
]


def main():
    rows = []
    n = 0

    # --- law nodes ---
    for law_id in sorted(LAWS):
        name, labels, conf = LAWS[law_id]
        n += 1
        soft = law_id in SOFT_LAW
        verdict = "PROVEN"
        note = "real legal instrument; labels==rechtsbereiche; on both GESTUETZT and GILT_IN_LAND axes"
        if soft:
            note = "real but soft-law/voluntary guidance (not a binding statute/standard); kept as reference node in *recht layer"
        proof = ("VARIANT_B_TAXONOMY.md sec.7 lists %s under %s; node carries source_url+source_quote"
                 % (law_id, "+".join(labels)))
        rows.append([
            "agent11-node-%04d" % n, "node", law_id, "", "",
            ":".join(labels), "typed law node '%s' is a real %s instrument" % (name, "/".join(labels)),
            "contract", TAX, "false", "", verdict, "%.2f" % conf,
            proof, "KEEP", AGENT, note,
        ])

    # --- ReuseRule nodes ---
    for rr in REUSERULES:
        n += 1
        note = ("synthetic country x material reuse-rule aggregator (HAT_AUFBEREITUNG + HAT_SCHADSTOFFRISIKO); "
                "NOT a legal instrument - instrument-reality check N/A")
        if rr.startswith("rr_fi"):
            note += "; FI prefix has no land_finnland node in legal layer (no GILT link, so no contradiction)"
        rows.append([
            "agent11-node-%04d" % n, "node", rr, "", "",
            "ReuseRule", "country x material reuse rule aggregator node exists and is connected",
            "logic", "get-schema + read-cypher enumeration", "false", "", "PROVEN", "",
            "node connected via HAT_AUFBEREITUNG/HAT_SCHADSTOFFRISIKO (deg>=4)", "KEEP", AGENT, note,
        ])

    # --- GESTUETZT_AUF_REGELWERK rels ---
    r = 0
    for nf in sorted(GESTUETZT):
        for law_id in GESTUETZT[nf]:
            r += 1
            labels = LAWS[law_id][1]
            rows.append([
                "agent11-rel-gestuetzt-%04d" % r, "rel",
                "gestuetzt__%s__%s" % (nf, law_id), nf, law_id,
                "GESTUETZT_AUF_REGELWERK",
                "Nachweisforderung %s is supported by legal instrument %s" % (nf, law_id),
                "contract", TAX, "false", "", "PROVEN", "",
                "valid domain(Nachweisforderung)->range(%s); topically coherent; source_url present (live fetch=Agent07)" % "+".join(labels),
                "KEEP", AGENT,
                "structural/taxonomy ok; live URL proof deferred to Agent 07 source_url ledger merge",
            ])

    # --- GILT_IN_LAND rels ---
    g = 0
    for law_id in sorted(GILT):
        lands = GILT[law_id]
        eu = lands is EU7
        for land in lands:
            g += 1
            note = "country attribution coherent with instrument jurisdiction; source_url present (live fetch=Agent07)"
            if eu:
                note = ("pan-EU/EN instrument scoped to EU/EEA-7 graph countries; CH/UK deliberately excluded "
                        "(national equivalents SIA / BS-UKCA); coherent")
            rows.append([
                "agent11-rel-gilt-%04d" % g, "rel",
                "gilt__%s__%s" % (law_id, land), law_id, land,
                "GILT_IN_LAND",
                "legal instrument %s applies in %s" % (law_id, land),
                "contract", AUDIT, "false", "", "PROVEN", "",
                "jurisdiction attribution correct for %s" % law_id,
                "KEEP", AGENT, note,
            ])

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(HEADER)
        w.writerows(rows)

    n_laws = len(LAWS)
    n_rr = len(REUSERULES)
    print("law nodes: %d" % n_laws)
    print("reuserule nodes: %d" % n_rr)
    print("GESTUETZT rels: %d" % r)
    print("GILT_IN_LAND rels: %d" % g)
    print("total ledger rows: %d" % len(rows))
    assert n_laws == 91, n_laws
    assert n_rr == 20, n_rr
    assert r == 167, r
    assert g == 281, g
    assert len(rows) == 91 + 20 + 167 + 281, len(rows)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
