"""Generate Phase O.0 — structural cleanup patch (must apply BEFORE Phase O).

Tier 1: remove 8 wrong NUTZT_MATERIAL rels (Stahl/Stahlbeton + Beton/Stahlbeton conflicts)
Tier 2: add 4 NUTZT_MATERIAL rels to People's Pavilion borrowed_facade_elements
Tier 3: (no patch op — Big Dig Building reuse_status is handled via rename-table override)
Tier 4: split Verbiest Charleroi misc into 3 new BGs (Geländer / Fliesen / Steine)
"""

from __future__ import annotations

import json
from pathlib import Path
from neo4j import GraphDatabase
from _scripts.neo4j_env import resolve_connection


OUT_A = Path("_neo4j/review/round_002_followup/patches/phase_o0a.patch.jsonl")
OUT_B = Path("_neo4j/review/round_002_followup/patches/phase_o0b.patch.jsonl")

# ── Tier 1: wrong NUTZT_MATERIAL rels to delete ────────────────────────────
TIER1_DELETES = [
    ("bg_haus_hos_reused_wall_elements", "mat_stahl",
        "archive: Stahlbetonfertigteile / WBS70 only — bare Stahl is not a distinct material"),
    ("bg_haus_hos_reused_floor_elements", "mat_stahl",
        "archive: Stahlbetonfertigteile only"),
    ("bg_haus_hos_reused_stairs", "mat_stahl",
        "archive: 58 Stahlbeton-Wand-/Deckenelemente; 7 Treppen — all Stahlbeton"),
    ("bg_ccn_hollow_core_slabs", "mat_beton",
        "archive: Spannbeton (prestressed) — mat_stahlbeton is proxy"),
    ("bg_harmalanranta_reused_hollow_core_slabs", "mat_beton",
        "archive: Spannbeton; EN 1168"),
    ("bg_ccn_prefab_facade_elements", "mat_beton",
        "archive: Fertigbeton/Sandwich precast — Stahlbeton only"),
    ("bg_timber_square_print_building_retained_structure", "mat_stahl",
        "archive: Print Building material unclear; reused steel beams are a separate BG"),
    ("bg_lokomotion_hollow_core_slabs", "mat_beton",
        "archive: Spannbeton; 27 elements; EN 1168"),
]

# ── Tier 2: missing NUTZT_MATERIAL rels for People's Pavilion ──────────────
TIER2_ADDS = [
    ("bg_peoples_pavilion_borrowed_facade_elements", "mat_beton",
        "Betonpfähle / concrete beams — borrowed structural elements"),
    ("bg_peoples_pavilion_borrowed_facade_elements", "mat_holz",
        "Holzträger — borrowed timber load-bearing elements"),
    ("bg_peoples_pavilion_borrowed_facade_elements", "mat_glas",
        "Glasdach — borrowed glass roof"),
    ("bg_peoples_pavilion_borrowed_facade_elements", "mat_kunststoff",
        "Pretty Plastic shingles — recycled plastic facade cladding"),
]

# ── Tier 4: Verbiest Charleroi split ───────────────────────────────────────
VERBIEST_OLD_ID = "bg_verbiest_karreveld_brussels_verbiest_gelaender_fliesen_und_steine_aus_charleroi"
VERBIEST_PROJEKT = "p_verbiest_karreveld_brussels"

# New BG nodes with their post-Phase-O schema-compliant ids (so Phase O.a skips them)
VERBIEST_NEW_BGS = [
    {
        "id": "bg_reuse_stahl_gelaender_verbiest_charleroi",
        "name": "Geländer aus Charleroi",
        "name_full": "Verbiest-Geländer aus Palais des Expositions Charleroi",
        "raw_name": "Verbiest Geländer | Metall/Holz | Palais des Expositions Charleroi",
        "reuse_status": "reuse",
        "primary_material_id": "mat_stahl",
        "primary_bauteiltyp_id": "bt_gelaender",
        "material_rels": ["mat_stahl"],
        "bauteiltyp_rels": ["bt_gelaender"],
        "materialgruppe_rels": ["mg_metall"],
        "leistungsanforderung_rels": ["la_dauerhaftigkeit", "la_tragfaehigkeit"],
        "aliases": [VERBIEST_OLD_ID],
    },
    {
        "id": "bg_reuse_keramik_boden_verbiest_charleroi",
        "name": "Fliesen aus Charleroi",
        "name_full": "Verbiest-Fliesen (Keramik/Stein) aus Palais des Expositions Charleroi",
        "raw_name": "Verbiest Fliesen | keramisch/Stein | Palais des Expositions Charleroi",
        "reuse_status": "reuse",
        "primary_material_id": "mat_keramik",
        "primary_bauteiltyp_id": "bt_mehrere",  # boden + fassade
        "material_rels": ["mat_keramik"],
        "bauteiltyp_rels": ["bt_boden", "bt_fassade"],
        "materialgruppe_rels": ["mg_glas_keramik"],
        "leistungsanforderung_rels": ["la_dauerhaftigkeit"],
        "aliases": [VERBIEST_OLD_ID],
    },
    {
        "id": "bg_reuse_naturstein_wand_verbiest_charleroi",
        "name": "Steine aus Charleroi",
        "name_full": "Verbiest-Steine (Natur-/Mauersteine) aus Palais des Expositions Charleroi",
        "raw_name": "Verbiest Steine | Natur-/Mauersteine | Palais des Expositions Charleroi",
        "reuse_status": "reuse",
        "primary_material_id": "mat_naturstein",
        "primary_bauteiltyp_id": "bt_wand",
        "material_rels": ["mat_naturstein"],
        "bauteiltyp_rels": ["bt_wand"],
        "materialgruppe_rels": ["mg_mineralisch"],
        "leistungsanforderung_rels": ["la_dauerhaftigkeit"],
        "aliases": [VERBIEST_OLD_ID],
    },
]

# Shared outbound rels — every new Verbiest BG gets all of these
VERBIEST_SHARED_OUT = [
    ("AUS_BAUWERK", "bw_palais_des_expositions_charleroi"),
    ("EINGEBAUT_IN", "bw_verbiest_lagerhaus_zu_haus_und_atelier"),
    ("TEIL_VON_KETTE", "wk_verbiest_karreveld_brussels_verbiest_karreveld_in_situ_und_projektuebergreifende_reuse_kette"),
    ("HAT_BAUTEILEBENE", "be_bauteilgruppe"),
    ("HAT_STATUS", "status_realisiert"),
    ("HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
    ("HAT_PROZESSPHASE", "phase_rueckbau"),
    ("HAT_PROZESSPHASE", "phase_wiedereinbau"),
    ("HAT_METHODE", "meth_reuse_assessment"),
    ("HAT_RUECKBAUVERFAHREN", "rv_zerstoerungsarme_bergung"),
    ("HAT_AUFBEREITUNG", "av_reinigung"),
    ("HAT_AUFBEREITUNG", "av_zuschnitt"),
    ("HAT_BESCHAFFUNGSWEG", "bweg_rueckbauprojekt"),
    ("HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
    ("HAT_LOGISTIK", "log_transport"),
    ("HAT_PRUEFUNG", "pr_zustandsbewertung"),
    ("HAT_HUERDE", "h_materialqualitaet_unklar"),
    ("HAT_HUERDE", "h_technische_freigabe"),
    ("HAT_HUERDEKATEGORIE", "hk_technisch"),
    ("HAT_HUERDEKATEGORIE", "hk_daten_evidenz"),
    ("BELEGT_IN", "q_verbiest_karreveld_brussels_md"),
    ("HAT_MARKTMODELL", "mm_same_site"),
    ("HAT_MARKTMODELL", "mm_plattform_vermittelt"),
]


def rel_id(from_id: str, rel_type: str, to_id: str) -> str:
    return f"r_{from_id}__{rel_type}__{to_id}"


def main() -> None:
    uri, user, password, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    records: list[dict] = []

    # ── Tier 1: delete wrong NUTZT_MATERIAL rels ────────────────────────────
    for bg, mat, reason in TIER1_DELETES:
        records.append({
            "op": "delete_rel",
            "id": rel_id(bg, "NUTZT_MATERIAL", mat),
            "from": bg,
            "to": mat,
            "type": "NUTZT_MATERIAL",
            "reason": f"Tier 1 — {reason}",
            "severity": "MEDIUM",
        })

    # ── Tier 2: add People's Pavilion NUTZT_MATERIAL rels ──────────────────
    for bg, mat, why in TIER2_ADDS:
        records.append({
            "op": "add_rel",
            "from": bg,
            "to": mat,
            "type": "NUTZT_MATERIAL",
            "properties": {
                "id": rel_id(bg, "NUTZT_MATERIAL", mat),
                "evidence": "BELEGT",
                "source": "archive:Peoples_Pavilion_Eindhoven.md ENTITÄTEN-MAPPING",
            },
            "reason": f"Tier 2 — {why}",
            "severity": "MEDIUM",
        })

    # ── Tier 4: split Verbiest Charleroi misc ──────────────────────────────
    # Step 4a — create 3 new BG nodes
    for new in VERBIEST_NEW_BGS:
        records.append({
            "op": "add_node",
            "id": new["id"],
            "labels": ["Bauteilgruppe"],
            "properties": {
                "id": new["id"],
                "name": new["name"],
                "name_full": new["name_full"],
                "raw_name": new["raw_name"],
                "reuse_status": new["reuse_status"],
                "primary_material_id": new["primary_material_id"],
                "primary_bauteiltyp_id": new["primary_bauteiltyp_id"],
                "aliases": new["aliases"],
            },
            "reason": "Tier 4 — Verbiest Charleroi misc split: create dedicated BG per archive sub-component",
            "severity": "MEDIUM",
        })

    # Step 4b — add inbound HAT_BAUTEILGRUPPE from Projekt to each new BG
    for new in VERBIEST_NEW_BGS:
        records.append({
            "op": "add_rel",
            "from": VERBIEST_PROJEKT,
            "to": new["id"],
            "type": "HAT_BAUTEILGRUPPE",
            "properties": {
                "id": rel_id(VERBIEST_PROJEKT, "HAT_BAUTEILGRUPPE", new["id"]),
                "source": "archive:Verbiest_Karreveld_Brussels.md ENTITÄTEN-MAPPING",
            },
            "reason": "Tier 4 — attach split BG to Projekt",
            "severity": "LOW",
        })

    # Step 4c — for each new BG: shared outbound rels + distinctive (material/bauteiltyp/materialgruppe/leistungsanforderung)
    for new in VERBIEST_NEW_BGS:
        bg_id = new["id"]
        # Shared
        for rel_type, to_id in VERBIEST_SHARED_OUT:
            records.append({
                "op": "add_rel",
                "from": bg_id,
                "to": to_id,
                "type": rel_type,
                "properties": {
                    "id": rel_id(bg_id, rel_type, to_id),
                    "source": "archive:Verbiest_Karreveld_Brussels.md (replicated from pre-split BG)",
                },
                "reason": "Tier 4 — replicate shared rel from pre-split BG",
                "severity": "LOW",
            })
        # Distinctive: materials
        for mat in new["material_rels"]:
            records.append({
                "op": "add_rel",
                "from": bg_id, "to": mat, "type": "NUTZT_MATERIAL",
                "properties": {
                    "id": rel_id(bg_id, "NUTZT_MATERIAL", mat),
                    "source": "archive:Verbiest_Karreveld_Brussels.md (split-specific material)",
                },
                "reason": "Tier 4 — distinctive material per archive sub-component",
                "severity": "LOW",
            })
        # Distinctive: bauteiltypen
        for bt in new["bauteiltyp_rels"]:
            records.append({
                "op": "add_rel",
                "from": bg_id, "to": bt, "type": "HAT_BAUTEILTYP",
                "properties": {
                    "id": rel_id(bg_id, "HAT_BAUTEILTYP", bt),
                    "source": "archive:Verbiest_Karreveld_Brussels.md (split-specific function)",
                },
                "reason": "Tier 4 — distinctive bauteiltyp per archive sub-component",
                "severity": "LOW",
            })
        # Distinctive: materialgruppen
        for mg in new["materialgruppe_rels"]:
            records.append({
                "op": "add_rel",
                "from": bg_id, "to": mg, "type": "HAT_MATERIALGRUPPE",
                "properties": {
                    "id": rel_id(bg_id, "HAT_MATERIALGRUPPE", mg),
                    "source": "archive:Verbiest_Karreveld_Brussels.md (split-specific material group)",
                },
                "reason": "Tier 4 — distinctive material group",
                "severity": "LOW",
            })
        # Distinctive: leistungsanforderungen
        for la in new["leistungsanforderung_rels"]:
            records.append({
                "op": "add_rel",
                "from": bg_id, "to": la, "type": "HAT_LEISTUNGSANFORDERUNG",
                "properties": {
                    "id": rel_id(bg_id, "HAT_LEISTUNGSANFORDERUNG", la),
                    "source": "archive:Verbiest_Karreveld_Brussels.md (replicated from pre-split BG)",
                },
                "reason": "Tier 4 — leistungsanforderung",
                "severity": "LOW",
            })

    # Step 4d — delete the old merged BG's BELEGT_IN first (apply-tool safety guard
    # refuses delete_node if BELEGT_IN rels remain). Evidence is preserved on the
    # 3 new BGs which each got their own BELEGT_IN in the shared-rels block above.
    records.append({
        "op": "delete_rel",
        "id": rel_id(VERBIEST_OLD_ID, "BELEGT_IN", "q_verbiest_karreveld_brussels_md"),
        "from": VERBIEST_OLD_ID,
        "to": "q_verbiest_karreveld_brussels_md",
        "type": "BELEGT_IN",
        "reason": "Tier 4 — remove evidence rel from to-be-deleted BG (preserved on split BGs)",
        "severity": "HIGH",
    })

    # Step 4e — delete_node of old Verbiest goes into a SEPARATE patch (O.0b) because
    # the apply tool's planner runs against live state and rejects delete_node while
    # any BELEGT_IN is still attached. After O.0a applies and removes that rel,
    # O.0b can replan and succeed.
    delete_node_op = {
        "op": "delete_node",
        "id": VERBIEST_OLD_ID,
        "reason": "Tier 4 — replaced by 3 split BGs created in O.0a",
        "severity": "HIGH",
    }

    driver.close()
    OUT_A.parent.mkdir(parents=True, exist_ok=True)
    with OUT_A.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with OUT_B.open("w", encoding="utf-8") as f:
        f.write(json.dumps(delete_node_op, ensure_ascii=False) + "\n")

    by_op = {}
    for r in records:
        by_op[r["op"]] = by_op.get(r["op"], 0) + 1
    print(f"O.0a: wrote {len(records)} ops to {OUT_A}")
    for op, c in sorted(by_op.items()):
        print(f"  {op}: {c}")
    print(f"O.0b: wrote 1 op (delete_node) to {OUT_B}")


if __name__ == "__main__":
    main()
