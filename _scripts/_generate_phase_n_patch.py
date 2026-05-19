"""Generate Phase N (short name + name_full on long-named entity labels) patch JSONL.

Targets: Projekt (99), Bauwerk (196), Wiederverwendungskette (63).

Heuristic per label:
  - Projekt / Bauwerk: take first chunk before ` / `, ` — `, or `, `; truncate to 25 with `…`
  - Wiederverwendungskette: take part AFTER ` → ` (receiver = chain endpoint); fall back to before-`/` chunk; truncate

Per Q3 decision: name_full is set when meaningfully different from name.
Override map handles plan-§3 explicit examples and known collisions (Association house Gröditz/Plauen).
"""

from __future__ import annotations

import json
from pathlib import Path
from neo4j import GraphDatabase
from _scripts.neo4j_env import resolve_connection


OUT = Path("_neo4j/review/round_002_followup/patches/phase_n.patch.jsonl")
LIMIT = 25
ELLIPSIS = "…"

# Hand-tuned short names from plan §3 Group D + known collisions
OVERRIDES: dict[str, str] = {
    # Plan §3 explicit examples (Projekt)
    "p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain": "House of Fraser",
    "p_fcrbe": "FCRBE",
    "p_boulder_fire_station_3": "Boulder FS-3",
    "p_charles_malis_molenbeek": "Charles Malis",
    "p_berlin_schildow_pilot_house": "Berlin-Schildow Pilot",
    "p_k118_kopfbau_halle_118_winterthur": "K.118 Winterthur",
    "p_resource_rows_copenhagen": "Resource Rows",
    "p_bedzed_london_hackbridge": "BedZED",
    # Collision-resolution: Association house — both Gröditz and Plauen would collapse to same prefix
    "p_association_house_groeditz": "Vereinshaus Gröditz",
    "p_association_house_plauen": "Vereinshaus Plauen",
    # Plan §3 explicit examples (Bauwerk)
    "bw_berlin_fitout_donor_sources": "Berlin donors",
    "bw_paris_regional_donor_sources_ferme_du": "Paris donors (Ferme)",
    "bw_ccn_heerde_receiver": "CCN Heerde",
    "bw_charles_malis_former_cigarette_factor": "Charles Malis (former)",
    # Plan §3 explicit examples (Wiederverwendungskette)
    "wk_waste_streams_to_brighton_waste_house": "Brighton-Waste streams",
    "wk_impact_hub_interior_reuse_chain": "Impact Hub fitout chain",
    "wk_villa_welpeloo_enschede_villa_welpelo": "Villa Welpeloo chain",
    # Collision-resolution: Gorlaeus pair (Leiden donor vs lab)
    "bw_biopartner_gorlaeus_hochhaus": "Gorlaeus (Biopartner)",
    "bw_gorlaeus_hochhaus": "Gorlaeus Hochhaus",
    # Collision-resolution: Boston Big Dig pair (I-93 vs CA/T)
    "bw_boston_big_dig_i_93_infrastructure": "Big Dig (I-93)",
    "bw_boston_big_dig_infrastructure": "Big Dig (CA/T)",
    # Collision-resolution: Cleveland Steel pair (near-duplicate descriptions)
    "bw_cleveland_steel_and_tubes_stock": "Cleveland S&T stock",
    "bw_cleveland_steel_reclaimed_stock": "Cleveland Steel reclaimed",
    # Collision-resolution: Lycée Michel Lucius trio
    "bw_lycee_block_3000": "Lycée Lucius B3000",
    "bw_lycee_block_6000": "Lycée Lucius B6000",
    "bw_lycee_michel_lucius_campus": "Lycée Lucius Campus",
    # Collision-resolution: Drill-Stem-Pipe chain pair
    "k_reuse_kette_drill_stem_pipe_dachtragwerk_nach_saxum_barn": "Drill-Stem-Pipe Dach",
    "k_reuse_kette_drill_stem_pipe_stutzen_nach_saxum_barn": "Drill-Stem-Pipe Stütze",
}

# Separators (in priority order) for first-chunk derivation
SPLIT_PROJEKT = [" / ", " — ", ", "]
SPLIT_BAUWERK = [" / ", ", "]


def shorten_word_aware(s: str, limit: int = LIMIT) -> str:
    """Truncate to ≤ limit chars; prefer cutting at a word boundary, then add ellipsis."""
    if len(s) <= limit:
        return s
    cut = limit - 1
    chunk = s[:cut]
    # Pull back to last space if there's one in the last 8 chars
    sp = chunk.rfind(" ")
    if sp >= cut - 8 and sp > 0:
        chunk = chunk[:sp]
    return chunk + ELLIPSIS


def first_chunk(name: str, seps: list[str]) -> str:
    """Return the part of `name` before the earliest occurrence of any separator in `seps`."""
    earliest = len(name)
    for sep in seps:
        i = name.find(sep)
        if i != -1 and i < earliest:
            earliest = i
    return name[:earliest].strip()


def derive_projekt_short(name: str) -> str:
    chunk = first_chunk(name, SPLIT_PROJEKT)
    return shorten_word_aware(chunk)


def derive_bauwerk_short(name: str) -> str:
    chunk = first_chunk(name, SPLIT_BAUWERK)
    return shorten_word_aware(chunk)


def derive_wk_short(name: str) -> str:
    # Receiver-after-arrow first
    if " → " in name:
        right = name.split(" → ")[-1].strip()
        return shorten_word_aware(right)
    chunk = first_chunk(name, [" / ", ", "])
    return shorten_word_aware(chunk)


def main() -> None:
    uri, user, password, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    records: list[dict] = []
    no_change = 0
    collisions: dict[tuple[str, str], list[str]] = {}

    with driver.session(database=db) as s:
        for label, deriver in (
            ("Projekt", derive_projekt_short),
            ("Bauwerk", derive_bauwerk_short),
            ("Wiederverwendungskette", derive_wk_short),
        ):
            seen: dict[str, list[str]] = {}
            rows = list(s.run(f"MATCH (n:{label}) RETURN n.id AS id, n.name AS name ORDER BY n.id"))
            for r in rows:
                node_id, cur_name = r["id"], r["name"]
                if node_id in OVERRIDES:
                    new_name = OVERRIDES[node_id]
                elif cur_name and len(cur_name) <= LIMIT:
                    # Already short → no change
                    no_change += 1
                    seen.setdefault(cur_name, []).append(node_id)
                    continue
                else:
                    new_name = deriver(cur_name or "")
                if new_name == cur_name:
                    no_change += 1
                    continue
                # Track collisions within this label
                seen.setdefault(new_name, []).append(node_id)
                records.append({
                    "op": "set_node_properties",
                    "id": node_id,
                    "properties": {"name": new_name, "name_full": cur_name},
                    "reason": f"Phase N: short name on {label} ({len(new_name)} chars)",
                    "severity": "LOW",
                })
            for short, ids in seen.items():
                if len(ids) > 1:
                    collisions[(label, short)] = ids

    driver.close()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} ops to {OUT}")
    print(f"  no-change (already short or unchanged): {no_change}")
    if collisions:
        print(f"\n⚠ {len(collisions)} short-name collisions detected:")
        for (label, short), ids in collisions.items():
            print(f"  {label} / {short!r} → {ids}")
    else:
        print("  no collisions")


if __name__ == "__main__":
    main()
