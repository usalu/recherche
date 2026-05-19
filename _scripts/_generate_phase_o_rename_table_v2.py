"""Generate the Phase O rename table v2 — short name as primary, new_id as semantic decoding.

Improvements over v1:
  A. Dedupe redundant material/bauteiltyp tokens from discriminator
  B. Promote dominant primary material from mat_mehrere when name keyword indicates one primary
  C. Trim the 17 verbose 80+ char discriminators with hand-curated alternatives
  D. Clean short name by stripping noise prefixes (Reused/Wiederverwendete/Erhaltene/Reclaimed/Mögliche)

Output: phase_o_rename_table.csv (overwrites v1)
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from neo4j import GraphDatabase
from _scripts.neo4j_env import resolve_connection


import os
_BASE = Path("_neo4j/review/round_002_followup/phase_o_rename_table.csv")
OUT_CSV = _BASE
if _BASE.exists():
    try:
        # Test writability
        with _BASE.open("a"): pass
    except PermissionError:
        OUT_CSV = _BASE.with_name("phase_o_rename_table_v3.csv")
SHORT_LIMIT = 25
ELLIPSIS = "…"

REUSE_STATUS_TOKENS = ("reused", "retained", "planned", "dismantled")
STATUS_MAP = {
    "reused": "reuse", "retained": "retained",
    "planned": "planned", "dismantled": "dismantled",
}

# Tokens redundant with material slot (lower-case)
MAT_REDUNDANT = {
    "stahl": "stahl", "steel": "stahl", "stahltraeger": "stahl", "stahlstuetzen": "stahl", "stahlprofile": "stahl",
    "holz": "holz", "wood": "holz", "wooden": "holz", "timber": "holz",
    "beton": "beton", "concrete": "beton",
    "stahlbeton": "stahlbeton",
    "glas": "glas", "glass": "glas",
    "ziegel": "ziegel", "brick": "ziegel", "bricks": "ziegel",
    "naturstein": "naturstein", "stone": "naturstein",
    "keramik": "keramik", "ceramic": "keramik",
    "aluminium": "aluminium",
    "kunststoff": "kunststoff",
    "daemmstoff": "daemmstoff",
    "lehm": "lehm",
    "textil": "textil",
    "recyclingbeton": "recyclingbeton",
    "bitumen": "bitumen",
}
# Tokens redundant with bauteiltyp slot
BT_REDUNDANT = {
    "stuetze": "stuetze", "stuetzen": "stuetze", "column": "stuetze", "columns": "stuetze",
    "traeger": "traeger", "beam": "traeger", "beams": "traeger", "girder": "traeger", "girders": "traeger",
    "wand": "wand", "waende": "wand", "wall": "wand", "walls": "wand",
    "boden": "boden", "floor": "boden", "fussboden": "boden", "fussboeden": "boden",
    "fassade": "fassade", "facade": "fassade",
    "decke": "decke", "ceiling": "decke",
    "dach": "dach", "roof": "dach",
    "treppe": "treppe", "stair": "treppe", "stairs": "treppe",
    "fenster": "fenster", "window": "fenster", "windows": "fenster",
    "tuer": "tuer", "tueren": "tuer", "door": "tuer", "doors": "tuer",
    "daemmung": "daemmung", "insulation": "daemmung",
    "technik": "technik",
    "gelaender": "gelaender", "balustrade": "gelaender", "balustraden": "gelaender",
    "ausbau": "ausbau",
    "belag": "belag",
    "panels": "wand", "paneele": "wand",  # often used as Bauteil
}
# Noise tokens to strip from discriminator (status-implied)
NOISE = {"wiederverwendet", "wiederverwendete", "wiederverwendung", "wiederverwendeter",
          "reclaimed", "reused", "salvaged", "neue", "neuer", "neuen",
          "moegliche", "moeglich", "uncertain"}

# Material keyword detection for B (dominant primary)
# Maps regex pattern → canonical mat_id slot (without prefix)
MAT_KEYWORDS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\b(stahltr[äa]ger|stahlst[üu]tzen|stahlprofil|stahlrahmen|stahl[\s-]frame|i-beam|wide[- ]flange|tubular|hollow section|tragwerksstahl|stahlfachwerk)", re.I), "stahl"),
    (re.compile(r"\b(glulam|brettschichtholz|cl[st]t?|clst|holzfenster|holzfassade|holzfussboden|holzbalken|holzrahmen|softwood|hardwood|brettsperrholz|dinesen|holzdecken|holzstuetzen|holzboeden|holzbo)", re.I), "holz"),
    (re.compile(r"\b(hollow[- ]core|hollowcore|h-?platten|hkp|hohlk[öo]rperdecke|hohlk[öo]rper|hohlkern|betonfertigteil|betonpaneel|betonblock|betonbloecke|betonplatte|ortbeton)", re.I), "beton"),
    (re.compile(r"\b(stahlbeton|reinforced concrete|rc[- ]frame|rc-rahmen)", re.I), "stahlbeton"),
    (re.compile(r"\b(ziegel|brick|mauerwerk|masonry|backstein|klinker)", re.I), "ziegel"),
    (re.compile(r"\b(blaustein|naturstein|pflaster|granit|granite|sandstein|stone slab|bruseleye)", re.I), "naturstein"),
    (re.compile(r"\b(glasfassade|glass facade|glass partition|verglasung)", re.I), "glas"),
    (re.compile(r"\b(dachziegel|roof tiles|terrassenfliese|fliese|tiles)", re.I), "keramik"),
]

# Hand-curated verbose-id trim overrides (Recommendation C). Keys = old_id (full).
DISCRIMINATOR_OVERRIDES = {
    "bg_verbiest_karreveld_brussels_verbiest_gelaender_fliesen_und_steine_aus_charleroi": "verbiest_karreveld_charleroi_misc",
    "bg_verbiest_karreveld_brussels_verbiest_dekorative_fliesen_aus_hanzinelle": "verbiest_hanzinelle_fliesen",
    "bg_verbiest_karreveld_brussels_karreveld_abgehaengte_decken_und_leuchten": "verbiest_karreveld_decken_leuchten",
    "bg_verbiest_karreveld_brussels_karreveld_modulares_innenwandsystem": "verbiest_karreveld_innenwand_modular",
    "bg_verbiest_karreveld_brussels_verbiest_dach_und_terrassenfliesen": "verbiest_karreveld_dach_terrasse",
    "bg_trae_high_rise_aarhus_holzboeden_aus_alten_fensterrahmen_und_gellerup_bauteilen": "trae_aarhus_holzboden_gellerup",
    "bg_woongroep_boschgaard_den_bosch_holz_dachspanten_brettschichtholz_kniespanten": "boschgaard_dachspanten",
    "bg_woongroep_boschgaard_den_bosch_aluminium_fassadensystem": "boschgaard_alu_fassade",
    "bg_woongroep_boschgaard_den_bosch_hsb_holz_balken_und_ausbauholz": "boschgaard_hsb_balken_ausbau",
    "bg_woongroep_boschgaard_den_bosch_tueren_und_innenausbau": "boschgaard_tueren_innenausbau",
    "bg_zinneke_feder_masui4ever_brussels_eichenparkett_und_azobe_terrassendielen": "zinneke_feder_eichenparkett_azobe",
    "bg_zinneke_feder_masui4ever_brussels_steinwolle_daemmplatten": "zinneke_feder_steinwolle",
    "bg_zinneke_feder_masui4ever_brussels_kompletter_lueftungsverbund": "zinneke_feder_lueftung",
    "bg_zinneke_feder_masui4ever_brussels_stahltraeger_als_stuerze": "zinneke_feder_stuerze",
    "bg_villa_welpeloo_enschede_polystyrol_daemmplatten_aus_restplatten": "welpeloo_polystyrol_restplatten",
    "bg_villa_welpeloo_enschede_stahltraeger_aus_paternoster_textilmaschine": "welpeloo_paternoster_textilmaschine",
    "bg_upcycle_studios_copenhagen_dinesen_offcuts_als_boeden_waende_fassaden": "upcycle_dinesen_offcuts",
    "bg_upcycle_studios_copenhagen_recyclingbeton_aus_copenhagen_metro": "upcycle_recyclingbeton_metro",
    "bg_trae_high_rise_aarhus_windturbinenfluegel_als_sonnenschutz": "trae_aarhus_windturbine_sonnenschutz",
    "bg_ziegelfassadenmodule_mauerwerksausschnitte_resource_rows": "resource_rows_ziegelfassade",
}

# Multi-material BGs where one is clearly dominant (Recommendation B)
# Generated by keyword-scan; user can review/edit.
# Use empty-string value ("") to force mat_mehrere (suppress incorrect promotion).
DOMINANT_MAT_OVERRIDES: dict[str, str] = {
    "bg_bedzed_reused_fixed_secondary_components": "",  # truly 4-material mix (Türen, Bordsteine, Stein, Gerüstrohre)
}

# BGs created in Phase O.0 with already-Phase-O-schema-compliant ids — Phase O.a skips these.
SKIP_BGS: set[str] = {
    "bg_reuse_stahl_gelaender_verbiest_charleroi",
    "bg_reuse_keramik_boden_verbiest_charleroi",
    "bg_reuse_naturstein_wand_verbiest_charleroi",
}

# Reuse-status overrides — archive-driven (e.g. unbuilt proposals = planned)
REUSE_STATUS_OVERRIDES: dict[str, str] = {
    "bg_big_dig_building_geplante_infrastrukturbauteile": "planned",  # SsD unbuilt proposal per Big_Dig_Building_Boston.md
}

# Short-name overrides for same-project collisions (where project hint cannot disambiguate)
SHORT_NAME_OVERRIDES: dict[str, str] = {
    "bg_ferme_window_frames_endgrain_floor": "Fensterrahmen→Pflaster",
    "bg_ferme_window_frames_roof_terrace": "Fensterrahmen→Akroterie",
}


# Short-name prefix patterns to strip (Recommendation D)
PREFIX_STRIP_PATTERNS = [
    re.compile(r"^(Wieder ?verwendete[rn]?\s+|Wiederverwendung\s+|Wiederverwendete[rn]?\s+)", re.I),
    re.compile(r"^(Reused|Reclaimed|Salvaged|Recovered|Möglicherweise|Mögliche[rn]?|Optional|Donor)\s+", re.I),
    re.compile(r"^(Erhaltene[srn]?|Retained|Existing|Bestehende[rn]?)\s+", re.I),
    re.compile(r"^(Neue[rn]?|New)\s+", re.I),
    re.compile(r"^(Geplante[rn]?|Planned)\s+", re.I),
    re.compile(r"^(Teilweise\s+wiederverwendete[rn]?\s+)", re.I),
    re.compile(r"^(Gebrauchte[rn]?)\s+", re.I),
    re.compile(r"^Zerkleinerter\s+", re.I),
]


def strip_prefix(name: str) -> str:
    s = name
    changed = True
    while changed:
        changed = False
        for pat in PREFIX_STRIP_PATTERNS:
            s2 = pat.sub("", s, count=1)
            if s2 != s:
                s = s2.strip()
                changed = True
                break
    return s.strip()


def shorten_word_aware(s: str, limit: int = SHORT_LIMIT) -> str:
    if not s or len(s) <= limit:
        return s or ""
    cut = limit - 1
    chunk = s[:cut]
    sp = chunk.rfind(" ")
    if sp >= cut - 8 and sp > 0:
        chunk = chunk[:sp]
    return chunk + ELLIPSIS


def derive_short_name(name: str) -> str:
    """Strip noise prefixes, capitalise first word, truncate."""
    s = strip_prefix(name or "")
    # If everything got stripped, fall back to original
    if not s:
        s = name or ""
    # Take the first ` / ` chunk or first ` — ` chunk for compactness
    for sep in [" / ", " — ", ", "]:
        if sep in s:
            first = s.split(sep)[0].strip()
            if first and len(first) >= 6:
                s = first
                break
    # Capitalise first letter
    if s and s[0].islower():
        s = s[0].upper() + s[1:]
    return shorten_word_aware(s)


def find_dominant_material(name: str, raw_name: str | None, mats: set[str]) -> str | None:
    """Return canonical mat token (e.g. 'stahl') if one is hinted by the name AND in mats."""
    text = ((name or "") + " " + (raw_name or "")).lower()
    candidates = []
    for pat, mat in MAT_KEYWORDS:
        if pat.search(text) and f"mat_{mat}" in mats:
            candidates.append(mat)
    if len(set(candidates)) == 1:
        return candidates[0]
    return None


def clean_discriminator(old_id_body: str, mat_slot: str, bt_slot: str) -> str:
    """Strip bg_ prefix, status tokens, redundant material/bauteiltyp tokens, and noise."""
    tokens = old_id_body.split("_")
    kept = []
    for t in tokens:
        tl = t.lower()
        if tl in REUSE_STATUS_TOKENS:
            continue
        if tl in NOISE:
            continue
        if tl in MAT_REDUNDANT and MAT_REDUNDANT[tl] == mat_slot and mat_slot not in ("mehrere", "unbekannt"):
            continue
        if tl in BT_REDUNDANT and BT_REDUNDANT[tl] == bt_slot and bt_slot not in ("mehrere", "unbekannt"):
            continue
        kept.append(t)
    return "_".join(kept) if kept else "uncategorised"


def strip_id_prefix(s: str, prefix: str) -> str:
    return s[len(prefix):] if s.startswith(prefix) else s


def find_reuse_status_token(old_id_body: str) -> str:
    tokens = old_id_body.split("_")
    for tok in tokens:
        if tok in REUSE_STATUS_TOKENS:
            return STATUS_MAP[tok]
    return "reuse"


def main() -> None:
    uri, user, password, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    rows = []
    with driver.session(database=db) as s:
        bg_rows = list(s.run(
            """MATCH (bg:Bauteilgruppe)
               OPTIONAL MATCH (bg)-[:NUTZT_MATERIAL]->(m:Material)
               OPTIONAL MATCH (bg)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
               WITH bg, collect(DISTINCT m.id) AS mats, collect(DISTINCT bt.id) AS bts
               RETURN bg.id AS id, bg.name AS name, bg.raw_name AS raw_name,
                      mats, bts ORDER BY bg.id"""
        ))

        for r in bg_rows:
            old_id = r["id"]
            if old_id in SKIP_BGS:
                continue
            current_name = r["name"] or ""
            raw_name = r["raw_name"]
            mats = [m for m in r["mats"] if m]
            bts = [b for b in r["bts"] if b]
            mats_set = set(mats)

            old_id_body = strip_id_prefix(old_id, "bg_")
            reuse_status = find_reuse_status_token(old_id_body)
            if old_id in REUSE_STATUS_OVERRIDES:
                reuse_status = REUSE_STATUS_OVERRIDES[old_id]

            # Material slot (B: dominant detection on multi-material BGs)
            if len(mats) == 0:
                mat_id, mat_slot = "mat_unbekannt", "unbekannt"
            elif len(mats) == 1:
                mat_id = mats[0]
                mat_slot = strip_id_prefix(mat_id, "mat_")
            else:
                # Override: empty string forces mehrere; explicit value overrides keyword detection
                if old_id in DOMINANT_MAT_OVERRIDES:
                    forced = DOMINANT_MAT_OVERRIDES[old_id]
                    if forced == "":
                        mat_id, mat_slot = "mat_mehrere", "mehrere"
                    else:
                        mat_id = f"mat_{forced}"
                        mat_slot = forced
                else:
                    dominant = find_dominant_material(current_name, raw_name, mats_set)
                    if dominant:
                        mat_id = f"mat_{dominant}"
                        mat_slot = dominant
                    else:
                        mat_id, mat_slot = "mat_mehrere", "mehrere"

            # Bauteiltyp slot
            if len(bts) == 0:
                bt_id, bt_slot = "bt_unbekannt", "unbekannt"
            elif len(bts) == 1:
                bt_id = bts[0]
                bt_slot = strip_id_prefix(bt_id, "bt_")
            else:
                bt_id, bt_slot = "bt_mehrere", "mehrere"

            # Discriminator (A + C)
            disc = clean_discriminator(old_id_body, mat_slot, bt_slot)
            if old_id in DISCRIMINATOR_OVERRIDES:
                disc = DISCRIMINATOR_OVERRIDES[old_id]
            else:
                # try the body without bg_ prefix for the override key lookup
                key2 = old_id  # keep as-is
                if key2 in DISCRIMINATOR_OVERRIDES:
                    disc = DISCRIMINATOR_OVERRIDES[key2]

            new_id = f"bg_{reuse_status}_{mat_slot}_{bt_slot}_{disc}"

            # Short name (D)
            if old_id in SHORT_NAME_OVERRIDES:
                short_name = SHORT_NAME_OVERRIDES[old_id]
            else:
                short_name = derive_short_name(current_name)
            name_full = current_name if short_name != current_name else ""

            rows.append({
                "old_id": old_id,
                "new_id": new_id,
                "name": short_name,
                "name_full": name_full,
                "reuse_status": reuse_status,
                "primary_material_id": mat_id,
                "primary_bauteiltyp_id": bt_id,
                "discriminator": disc,
                "n_materials": len(mats),
                "n_bauteiltypen": len(bts),
                "dominant_promoted": "yes" if (len(mats) >= 2 and mat_slot not in ("mehrere", "unbekannt")) else "no",
                "verbose_trimmed": "yes" if old_id in DISCRIMINATOR_OVERRIDES else "no",
            })

    driver.close()

    # ── Resolve short-name collisions by appending project hint ────────────
    # Project hint = first 1-2 tokens of old_id body (e.g. 'bg_chiro_...' → 'Chiro')
    PROJECT_TOKEN_OVERRIDES = {
        "bg": "",  # ignore
        "lo": "Lo-R.",  # lo_reninge
        "big": "Big Dig",  # big_dig
        "grande": "Grande Halle",
        "resource": "Resource Rows",
        "circular": "Circular Pav.",
        "ferme": "Ferme",
        "moeoeslistrasse": "Möösli.",
        "grubenstrasse": "Gruben.",
        "trae": "Træ Aarhus",
        "villa": "Welpeloo",
        "upcycle": "Upcycle",
        "verbiest": "Verbiest",
        "woongroep": "Boschgaard",
        "zinneke": "Zinneke",
    }
    def project_hint(old_id: str) -> str:
        toks = old_id.replace("bg_", "").split("_")
        first = toks[0]
        if first in PROJECT_TOKEN_OVERRIDES:
            return PROJECT_TOKEN_OVERRIDES[first]
        return first.capitalize()

    def squeeze_short(s: str, hint: str, limit: int = SHORT_LIMIT) -> str:
        base = s.rstrip(ELLIPSIS).rstrip()
        suffix = f" ({hint})"
        budget = limit - len(suffix)
        if len(base) > budget:
            base = base[: budget - 1].rstrip() + ELLIPSIS
        return base + suffix

    by_short: dict[str, list[int]] = {}
    for i, row in enumerate(rows):
        by_short.setdefault(row["name"], []).append(i)
    for short, idxs in by_short.items():
        if len(idxs) <= 1:
            continue
        for i in idxs:
            hint = project_hint(rows[i]["old_id"])
            rows[i]["name"] = squeeze_short(short, hint)

    # ── Check uniqueness after disambiguation ──────────────────────────────
    by_new: dict[str, list[str]] = {}
    for row in rows:
        by_new.setdefault(row["new_id"], []).append(row["old_id"])
    collisions = {nid: olds for nid, olds in by_new.items() if len(olds) > 1}

    by_short2: dict[str, list[str]] = {}
    for row in rows:
        by_short2.setdefault(row["name"], []).append(row["old_id"])
    name_collisions = {n: olds for n, olds in by_short2.items() if len(olds) > 1}

    # ── Write CSV ──────────────────────────────────────────────────────────
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows:
            w.writerow(row)

    # ── Summary ────────────────────────────────────────────────────────────
    by_status, by_mat, by_bt = {}, {}, {}
    dominant_promoted = 0
    verbose_trimmed = 0
    new_id_lens = []
    name_lens = []
    for row in rows:
        by_status[row["reuse_status"]] = by_status.get(row["reuse_status"], 0) + 1
        by_mat[row["primary_material_id"]] = by_mat.get(row["primary_material_id"], 0) + 1
        by_bt[row["primary_bauteiltyp_id"]] = by_bt.get(row["primary_bauteiltyp_id"], 0) + 1
        if row["dominant_promoted"] == "yes":
            dominant_promoted += 1
        if row["verbose_trimmed"] == "yes":
            verbose_trimmed += 1
        new_id_lens.append(len(row["new_id"]))
        name_lens.append(len(row["name"]))

    print(f"Wrote {len(rows)} rows to {OUT_CSV}")
    print(f"\nreuse_status: {by_status}")
    print(f"primary_material top: " + ", ".join(f"{k}={v}" for k, v in sorted(by_mat.items(), key=lambda x: -x[1])[:10]))
    print(f"primary_bauteiltyp top: " + ", ".join(f"{k}={v}" for k, v in sorted(by_bt.items(), key=lambda x: -x[1])[:10]))
    print(f"\nB: dominant material promoted (from mat_mehrere): {dominant_promoted}")
    print(f"C: verbose ids trimmed: {verbose_trimmed}")
    print(f"\nnew_id length: min={min(new_id_lens)}  max={max(new_id_lens)}  median={sorted(new_id_lens)[len(new_id_lens)//2]}")
    print(f"short name length: min={min(name_lens)}  max={max(name_lens)}  median={sorted(name_lens)[len(name_lens)//2]}")
    print(f"\nnew_id collisions: {len(collisions)}")
    if collisions:
        for nid, olds in collisions.items():
            print(f"  COLLISION {nid}: {olds}")
    print(f"\nshort-name collisions (within Bauteilgruppe): {len(name_collisions)}")
    if name_collisions:
        for n, olds in list(name_collisions.items())[:10]:
            print(f"  '{n}': {olds}")


if __name__ == "__main__":
    main()
