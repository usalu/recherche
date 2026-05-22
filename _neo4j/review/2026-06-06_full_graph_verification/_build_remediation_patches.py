#!/usr/bin/env python3
"""Build fix_property + merge_duplicate_edges_remaining patches for remediation pass."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PATCHES = ROOT / "patches"


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_fix_property() -> list[dict]:
    rows: list[dict] = []

    def rel_role(from_id: str, rel_type: str, to_id: str, old_key: str, role: str, claim: str) -> None:
        rows.append({
            "op": "set_rel_properties",
            "from": from_id,
            "type": rel_type,
            "to": to_id,
            "properties": {"role": role},
            "reason": f"Agent 14 {claim}: rename {old_key} to canonical role={role!r}",
        })
        rows.append({
            "op": "remove_rel_properties",
            "from": from_id,
            "type": rel_type,
            "to": to_id,
            "properties": [old_key],
            "reason": f"Agent 14 {claim}: drop off-canonical {old_key}",
        })

    rel_role(
        "rotordc", "NUTZT_BAUWERK", "bw_generale_de_banque_brussels",
        "nutzung_role", "salvage_source", "A14-RELKEY-001",
    )
    rel_role(
        "p_multi_brussels_reuse_in_multi", "HAT_BAUWERK", "bw_generale_de_banque_brussels",
        "bauwerk_role", "donor_source", "A14-RELKEY-002",
    )

    rows.append({
        "op": "remove_node_properties",
        "id": "enviromate",
        "properties": ["additional_marktmodelle"],
        "reason": "Agent 14 A14-NODEKEY-001: stray enrichment key not in Akteur schema",
    })
    rows.append({
        "op": "remove_node_properties",
        "id": "mobius_reemploi",
        "properties": ["needs_evidence_urls", "evidence_urls_target"],
        "reason": "Agent 14 A14-NODEKEY-002: drop TODO-marker keys after evidence resolved on-graph",
    })

    vocab_names = {
        "bt_fassadenelement": "Fassadenelement",
        "bt_fassadenmodul_mauerwerk": "Fassadenmodul (Mauerwerk)",
        "bt_glasscheibe": "Glasscheibe",
        "bt_hohlkoerperdecke": "Hohlkörperdecke",
        "bt_mauerstein": "Mauerstein",
        "bt_verglasung": "Verglasung",
        "mat_drahtglas": "Drahtglas",
        "mat_spannbeton": "Spannbeton",
    }
    for node_id, name in vocab_names.items():
        rows.append({
            "op": "set_node_properties",
            "id": node_id,
            "properties": {"name": name},
            "reason": f"Agent 12 vocab stub: set human-readable name (was name==id)",
        })

    rows.append({
        "op": "set_node_properties",
        "id": "land_liechtenstein",
        "properties": {"country_iso2": "LI"},
        "reason": "Agent 09 09-node-0191: Liechtenstein country node missing country_iso2",
    })
    rows.append({
        "op": "set_node_properties",
        "id": "stadt_paso_robles_templeton_gap",
        "properties": {"latitude": 35.6245, "longitude": -120.6910},
        "reason": "Agent 09 09-node-0342: Paso Robles city centroid coords for wine-region Stadt node",
    })

    # A14-LAND-001 deferred: 6 Akteur nodes have scalar land but no LIEGT_IN_LAND edge yet.
    # A10-N-058 prog_mas_dfab deferred: name/source mismatch needs human relabel.

    return rows


def build_merge_duplicate_edges() -> list[dict]:
    """Delete reverse leg per Agent 14 rules; escalate ambiguous pairs."""
    # (keep_from, keep_to, delete_from, delete_to, reason)
    decisions = [
        ("Rotor", "lionel_devlieger", "lionel_devlieger", "Rotor", "A14-BIDIR-005"),
        ("Rotor", "maarten_gielen", "maarten_gielen", "Rotor", "A14-BIDIR-006"),
        ("Rotor", "opalis", "opalis", "Rotor", "A14-BIDIR-007"),
        ("Rotor", "tristan_boniver", "tristan_boniver", "Rotor", "A14-BIDIR-008"),
        ("angelika_mettke", "btu_cottbus", "btu_cottbus", "angelika_mettke", "A14-BIDIR-012"),
        ("angelika_mettke", "recreate_project", "recreate_project", "angelika_mettke", "A14-BIDIR-013"),
        ("bauteilnetz_deutschland", "bauteilboerse_bremen", "bauteilboerse_bremen", "bauteilnetz_deutschland", "A14-BIDIR-018 evidence on reverse leg"),
        ("catherine_de_wolf", "eth_zuerich", "eth_zuerich", "catherine_de_wolf", "A14-BIDIR-026"),
        ("circular_material_systems", "tu_berlin", "tu_berlin", "circular_material_systems", "A14-BIDIR-032"),
        ("patrick_teuffel", "circular_structural_design", "circular_structural_design", "patrick_teuffel", "A14-BIDIR-034"),
        ("cirkla", "pascal_flammer_architekten", "pascal_flammer_architekten", "cirkla", "A14-BIDIR-035"),
        ("cirkla", "urban_bricolage", "urban_bricolage", "cirkla", "A14-BIDIR-036"),
        ("fabio_gramazio", "eth_zuerich", "eth_zuerich", "fabio_gramazio", "A14-BIDIR-037"),
        ("gramazio_kohler_research", "eth_zuerich", "eth_zuerich", "gramazio_kohler_research", "A14-BIDIR-038"),
        ("matthias_kohler", "eth_zuerich", "eth_zuerich", "matthias_kohler", "A14-BIDIR-039"),
        ("georg_hubmann", "tu_berlin", "tu_berlin", "georg_hubmann", "A14-BIDIR-040"),
        ("gruner_ag", "gruner_reuse_platform", "gruner_reuse_platform", "gruner_ag", "A14-BIDIR-041"),
        ("nicole_daehn", "gruner_reuse_platform", "gruner_reuse_platform", "nicole_daehn", "A14-BIDIR-042"),
        ("ullrich_dickgiesser", "gruner_reuse_platform", "gruner_reuse_platform", "ullrich_dickgiesser", "A14-BIDIR-043"),
        ("maarten_gielen", "opalis", "opalis", "maarten_gielen", "A14-BIDIR-044"),
        ("materiuum", "materiuum_geneve_ressourcerie", "materiuum_geneve_ressourcerie", "materiuum", "A14-BIDIR-045"),
        ("materiuum", "ressourcerie_lausanne_materiuum_ruul", "ressourcerie_lausanne_materiuum_ruul", "materiuum", "A14-BIDIR-046"),
        ("satu_huuhka", "recreate_project", "recreate_project", "satu_huuhka", "A14-BIDIR-047"),
    ]
    rows = []
    for kf, kt, df, dt, claim in decisions:
        rows.append({
            "op": "delete_rel",
            "from": df,
            "type": "VERBUNDEN_MIT_AKTEUR",
            "to": dt,
            "reason": (
                f"Agent 14 {claim}: bidirectional VERBUNDEN_MIT_AKTEUR — "
                f"collapse to canonical {kf}->{kt}; delete reverse leg"
            ),
        })
    return rows


def build_merge_nodes() -> list[dict]:
  # from -> to (merge from into to)
    pairs = [
        ("Superuse_Studios", "superuse_studios_2012architecten", "AKT-node-008 same firm; canonical has source URL"),
        ("ak_cityfoerster", "CITYFOERSTER", "AKT-node-023 same firm CITYFOERSTER"),
        ("artelia_group", "artelia", "AKT-node-057 Artelia Group = Artelia"),
        ("bureau_greisch", "greisch", "AKT-node-097 Bureau Greisch = Greisch"),
        ("graber_pulver_architektinnen", "graber_pulver", "AKT-node-197 Graber Pulver Architekt:innen = Graber Pulver"),
        ("fabrix_london", "fabrix", "AKT-node-175 Fabrix London = Fabrix"),
        ("lendager_group_lendager_architects", "Lendager", "AKT-node-277 Lendager Group = Lendager"),
        ("tool_qflow", "software_qflow", "A10-N-009/N-019 same Qflow entity (Qualis Flow); merge tool stub into software node"),
    ]
    return [
        {
            "op": "merge_node",
            "from": src,
            "to": dst,
            "reason": f"Agent 08/10 MERGE_DUPLICATE: {note}",
        }
        for src, dst, note in pairs
    ]


def main() -> None:
    fix = build_fix_property()
    edges = build_merge_duplicate_edges()
    nodes = build_merge_nodes()
    write_jsonl(PATCHES / "fix_property.patch.jsonl", fix)
    write_jsonl(PATCHES / "merge_duplicate_edges_remaining.patch.jsonl", edges)
    write_jsonl(PATCHES / "merge_duplicate_nodes_high_confidence.patch.jsonl", nodes)
    print(f"fix_property: {len(fix)} ops")
    print(f"merge_duplicate_edges_remaining: {len(edges)} ops")
    print(f"merge_duplicate_nodes_high_confidence: {len(nodes)} ops")


if __name__ == "__main__":
    main()
