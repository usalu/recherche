"""Generate Phase M (short name + name_full on long-named vocab labels) patch JSONL.

Targets: Defekt (10), MatchingQualitaet (9), ZustandsKlasse (6), Bauproduktstatus (15),
LebenszyklusModul (5), Akzeptanz (5), Marktmodell (11), Norm (30).

Per Q3 decision: name_full is only set when meaningfully different from name (already-short
names skip name_full entirely).

Mapping tables are transcribed from NAMING_AND_PROPERTIES_PLAN.md §3 Groups C+D. Norm short
names are derived as "standard number" (the prefix before ` — ` separator or before the title
words). The 5 already-clean short Norm names (DIN_18940 etc.) are normalized to space-form.
"""

from __future__ import annotations

import json
from pathlib import Path
from neo4j import GraphDatabase
from _scripts.neo4j_env import resolve_connection


OUT = Path("_neo4j/review/round_002_followup/patches/phase_m.patch.jsonl")

# ── Mappings (id → short_name). name_full = current name (set only if meaningfully different).
# A None value means "no change" (already short and clean).
MAPPINGS: dict[str, str | None] = {
    # Defekt (10)
    "def_korrosion": None,  # already 'Korrosion'
    "def_brandschaden": None,  # already 'Brandschaden'
    "def_riss": "Risse",
    "def_verformung": "Verformung",
    "def_karbonatisierung": "Karbonatisierung",
    "def_holzwurm_pilzbefall": "Holzwurm/Pilz",
    "def_hohlraum_delamination": "Delamination",
    "def_oberflaechenmangel": "Oberfläche",
    "def_chemische_belastung": "Chemisch belastet",
    "def_keine_befunde": "Keine Befunde",
    # MatchingQualitaet (9)
    "mq_temporal_easy": "Temporal: unproblematisch",
    "mq_temporal_storage": "Temporal: Zwischenlager",
    "mq_temporal_planned": "Temporal: geplant",
    "mq_geographic_local": "Geo: lokal (<50 km)",
    "mq_geographic_regional": "Geo: regional",
    "mq_geographic_intl": "Geo: international",
    "mq_spec_exact": "Spec: exakt",
    "mq_spec_anpassung": "Spec: Anpassung",
    "mq_spec_zweckaenderung": "Spec: Zweckänderung",
    # ZustandsKlasse (6)
    "zk_neuwertig": "Neuwertig",
    "zk_gebrauchsspuren_funktional": "Gebraucht, funktional",
    "zk_eingeschraenkt_nachbearbeitung": "Eingeschränkt: Nacharbeit",
    "zk_eingeschraenkt_nutzungsklasse_reduzieren": "Eingeschränkt: downgrade",
    "zk_nicht_wiederverwendbar": "Nicht reusable",
    "zk_unbekannt_pruefung_offen": "Prüfung offen",
    # Bauproduktstatus (15) — note: plan uses bps_ueh_zeichen / bps_bauproduktstatus_unbekannt
    # but live ids are bps_ue_zeichen / bps_unbekannt. Live ids are authoritative.
    "bps_ce_hen": "CE (hEN)",
    "bps_ce_eta": "CE (ETA)",
    "bps_ukca": "UKCA",
    "bps_abz_abg": "abZ / aBG (DE)",
    "bps_zie_vbg": "ZiE / vBG (DE)",
    "bps_ue_zeichen": "Ü-Zeichen (DE)",
    "bps_tracimat_be": "Tracimat (BE)",
    "bps_pemd_fr": "PEMD (FR)",
    "bps_bestand_no_status": "Bestand vor Ort",
    "bps_unbekannt": "Status unbekannt",
    # The 5 "remaining" Bauproduktstatus not in plan's explicit table are actually 29-50 chars long.
    # Derive sensible short names for them.
    "bps_baupg_ch": "BauPG (CH)",
    "bps_ibc_104_11_alternative": "IBC 104.11 (USA)",
    "bps_jis_jas_mlit": "JIS/JAS/MLIT (JP)",
    "bps_nta_8713": "NTA 8713 (NL)",
    "bps_project_specific": "Projekt-Freigabe",
    # LebenszyklusModul (5)
    "lz_a1_a3": "A1–A3 Produkt",
    "lz_a4_a5": "A4–A5 Errichtung",
    "lz_b": "B1–B7 Nutzung",
    "lz_c": "C1–C4 End-of-Life",
    "lz_d": "D Beyond (Reuse)",
    # Akzeptanz (5)
    "ak_dgnb_zertifizierung": "DGNB",
    "ak_breeam_zertifizierung": "BREEAM",
    "ak_leed_zertifizierung": "LEED",
    "ak_oeffentlicher_bauherr_pilot": "Public-Bauherr Pilot",
    "ak_aesthetik_patinakultur": "Patina-Ästhetik",
    # Marktmodell (11)
    "mm_same_site": "Same-site",
    "mm_plattform_vermittelt": "Plattform-Kauf",
    "mm_kauf_gebraucht": "Kauf gebraucht",
    "mm_kauf_neu": "Kauf neu-äquiv.",
    "mm_spende": None,  # already 'Spende'
    "mm_take_back_service": "Take-Back",
    "mm_leasing": "Leasing",
    "mm_rueckkauf": "Rückkauf",
    "mm_forschungsprojekt_zuteilung": "Forschungs-Zuteilung",
    "mm_intra_konzern": "Intra-Konzern",
    "mm_unbekannt": "Unbekannt",
    # Norm (30) — short = standard number; name_full = full title (if different)
    "norm_cen_ts_1090_201_2024": "CEN/TS 1090-201:2024",
    "norm_cen_ts_17440": "CEN/TS 17440",
    "norm_crow_cur_4_2023": "CROW-CUR 4:2023",
    "norm_din_18008": "DIN 18008",
    "norm_din_18940": "DIN 18940",  # normalize underscore → space
    "norm_din_4074": "DIN 4074",
    "norm_din_68800": "DIN 68800",
    "norm_din_en_15804": "DIN EN 15804",  # normalize underscore → space
    "norm_din_en_15978": "DIN EN 15978",
    "norm_en_1090": "EN 1090",
    "norm_en_1168": "EN 1168",
    "norm_en_13162": "EN 13162",
    "norm_en_14081": "EN 14081",
    "norm_en_1992": "EN 1992 (Eurocode 2)",
    "norm_en_1993": "EN 1993 (Eurocode 3)",
    "norm_en_1995": "EN 1995 (Eurocode 5)",
    "norm_en_1996": "EN 1996 (Eurocode 6)",
    "norm_en_206": "EN 206",
    "norm_en_771": "EN 771",
    "norm_historic_sections_book": None,  # already 'Historic Sections Book' (22 chars)
    "norm_iso_14040": "ISO 14040",  # normalize underscore → space
    "norm_iso_14044": "ISO 14044",
    "norm_iso_20887": "ISO 20887",
    "norm_nen_8700": "NEN 8700",
    "norm_ns_3682": "NS 3682",
    "norm_rt_2012": None,  # already 'RT 2012' (7 chars)
    "norm_sci_p427": None,  # already 'SCI P427 protocol' (17 chars)
    "norm_sci_p440": "SCI P440",
    "norm_sia_schweiz": "SIA (CH)",
    "norm_tek_norway": "TEK (NO)",
}


def main() -> None:
    uri, user, password, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    records: list[dict] = []
    no_change = 0
    name_only = 0
    name_plus_full = 0

    with driver.session(database=db) as s:
        for node_id, new_name in MAPPINGS.items():
            row = s.run(
                "MATCH (n {id: $id}) RETURN n.name AS cur_name, n.name_full AS cur_nf, labels(n) AS labels",
                id=node_id,
            ).single()
            if row is None:
                print(f"  WARN: node {node_id} not found, skipping")
                continue
            cur_name = row["cur_name"]
            label = next(
                (l for l in row["labels"] if l not in {"_Vocab", "_Concept", "_Source"}),
                row["labels"][0] if row["labels"] else "?",
            )
            if new_name is None:
                no_change += 1
                continue
            if cur_name == new_name:
                no_change += 1
                continue
            # Per Q3: only set name_full if meaningfully different (i.e. if new short ≠ old).
            # By definition we're here because cur_name != new_name.
            props = {"name": new_name, "name_full": cur_name}
            records.append({
                "op": "set_node_properties",
                "id": node_id,
                "properties": props,
                "reason": f"Phase M: short name on {label} ({len(new_name)} chars); preserve full as name_full",
                "severity": "LOW",
            })
            name_plus_full += 1

    driver.close()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} ops to {OUT}")
    print(f"  set_node_properties (name+name_full): {name_plus_full}")
    print(f"  no-change (already short or unchanged): {no_change}")


if __name__ == "__main__":
    main()
