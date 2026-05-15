"""Apply round-002 vocab cleanup decisions to the `_neo4j/processed/` payload.

After round 002 + its followup, the live Neo4j graph carries 19 node merges +
1 node delete that the processed JSONL files do not reflect. Re-importing the
payload onto a fresh database would resurrect the duplicates.

This script reads a merge/delete map and rewrites the payload in place:
  - Node records whose id is a merge SOURCE → dropped (target survives).
  - Node records whose id is the explicit delete set → dropped.
  - Rel records whose `from` or `to` is in the merge map → endpoint
    rewritten, and the rel's `id` property rewritten with the same scheme
    used by the live apply runner.
  - Duplicate rel records (same id, same endpoints, same type, same
    properties after rewrite) are deduplicated.

Output written next to the input as `<file>.converged.jsonl`. Apply the
change in place when satisfied:

  python _scripts/converge_payload_to_live.py --apply
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root  # noqa: E402


# (from_id, to_id) where from is merged INTO to. Order matches the live apply.
MERGE_MAP: dict[str, str] = {
    # Round 002 family runs
    "norm_crow_cur_guideline_4_2023": "norm_crow_cur_4_2023",
    "la_brandschutzanforderung": "la_brandschutz",
    "status_prototypisch": "status_prototyp",
    "ar_bauausfuehrung": "ar_bauausfuehrung_fertigung",
    "ar_materiallieferant": "ar_materiallieferung_markt",
    "ar_oeffentliche_hand": "ar_oeffentliche_hand_foerderung",
    "ar_projektbeteiligte_unbestimmt": "ar_unbestimmt",
    "ar_rueckbau_demontage": "ar_rueckbau_bauteilernte_logistik",
    "ar_betreiber_nutzer": "ar_betrieb_nutzung",
    "at_ngo_netzwerk": "at_ngo_verband_netzwerk",
    "at_verband_kammer": "at_ngo_verband_netzwerk",
    "land_vereinigtes_konigreich": "land_vereinigtes_koenigreich",
    "land_united_kingdom": "land_vereinigtes_koenigreich",
    "land_danemark": "land_daenemark",
    # Round 002 followup (parked vocab + actor registry)
    "ar_architektur": "ar_entwurf_planung",
    "ar_pruefung_qualitaetssicherung": "ar_fachplanung_nachweis",
    "cleveland_steel_and_tubes": "cleveland_steel_tubes",
    "cleveland_steel": "cleveland_steel_tubes",
    "rotor_deconstruction": "rotor_dc",
}

DELETE_SET: set[str] = {
    # Round 002 followup mat_metall fallback drop
    "mat_metall",
}


def rewrite_endpoint(node_id: str) -> str:
    while node_id in MERGE_MAP:
        node_id = MERGE_MAP[node_id]
    return node_id


def rewrite_rel_id(rel_id: str, rel_type: str, old_from: str, new_from: str, old_to: str, new_to: str) -> str:
    """Mirror the live apply runner's rel-id rewrite logic.

    Live rel id form: r_<from>__<TYPE>__<to>[__suffix]. After endpoint
    rewrite, the id must encode the new endpoints; otherwise it collides
    with another rel under the existing uniqueness constraints when
    re-imported.
    """
    if not isinstance(rel_id, str):
        return rel_id
    if old_from != new_from:
        prefix = f"r_{old_from}__{rel_type}__"
        if rel_id.startswith(prefix):
            rel_id = f"r_{new_from}__{rel_type}__" + rel_id[len(prefix):]
    if old_to != new_to:
        needle = f"__{rel_type}__{old_to}"
        if needle in rel_id:
            rel_id = rel_id.replace(needle, f"__{rel_type}__{new_to}", 1)
    return rel_id


def converge_file(path: Path, apply: bool) -> dict:
    stats = {
        "file": str(path.resolve().relative_to(repo_root())),
        "input_records": 0,
        "dropped_merge_source_nodes": 0,
        "dropped_delete_set_nodes": 0,
        "rewired_rels": 0,
        "deduped_rels": 0,
        "deduped_nodes": 0,
        "output_records": 0,
    }
    output: list[dict] = []
    seen_node_ids: set[str] = set()
    seen_rel_ids: set[str] = set()

    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            stats["input_records"] += 1
            rec = json.loads(line)

            rt = rec.get("record_type")
            if rt == "node":
                nid = rec.get("id")
                if nid in MERGE_MAP:
                    stats["dropped_merge_source_nodes"] += 1
                    continue
                if nid in DELETE_SET:
                    stats["dropped_delete_set_nodes"] += 1
                    continue
                if nid in seen_node_ids:
                    stats["deduped_nodes"] += 1
                    continue
                seen_node_ids.add(nid)
                output.append(rec)
            elif rt == "rel":
                old_from = rec.get("from")
                old_to = rec.get("to")
                new_from = rewrite_endpoint(old_from)
                new_to = rewrite_endpoint(old_to)
                # Drop rels pointing at deleted nodes
                if new_from in DELETE_SET or new_to in DELETE_SET:
                    continue
                if old_from != new_from or old_to != new_to:
                    rec = dict(rec)
                    rec["from"] = new_from
                    rec["to"] = new_to
                    props = dict(rec.get("properties") or {})
                    if "id" in props:
                        props["id"] = rewrite_rel_id(
                            props["id"], rec.get("type", ""), old_from, new_from, old_to, new_to
                        )
                    rec["properties"] = props
                    new_id = rewrite_rel_id(
                        rec.get("id", ""), rec.get("type", ""), old_from, new_from, old_to, new_to
                    )
                    if new_id != rec.get("id"):
                        rec["id"] = new_id
                    stats["rewired_rels"] += 1
                rel_id = rec.get("id")
                if rel_id and rel_id in seen_rel_ids:
                    stats["deduped_rels"] += 1
                    continue
                if rel_id:
                    seen_rel_ids.add(rel_id)
                output.append(rec)
            else:
                output.append(rec)

    stats["output_records"] = len(output)

    if apply:
        target = path
    else:
        target = path.with_suffix(path.suffix + ".converged.jsonl")
    with target.open("w", encoding="utf-8", newline="\n") as f:
        for rec in output:
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True))
            f.write("\n")

    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Rewrite files in place. Without this flag, writes to <file>.converged.jsonl side files.",
    )
    args = parser.parse_args()

    base = repo_root() / "_neo4j" / "processed"
    targets: list[Path] = []
    targets.extend(sorted((base / "projects" / "records").glob("p_*.kg.jsonl")))
    targets.append(base / "projects" / "vocabulary" / "controlled_vocabulary.seed.kg.jsonl")
    targets.append(base / "projects" / "vocabulary" / "controlled_terms.merged.kg.jsonl")
    targets.append(base / "actor_registry" / "actor_registry.canonical.kg.jsonl")

    totals = defaultdict(int)
    for path in targets:
        if not path.is_file():
            continue
        stats = converge_file(path, args.apply)
        for k, v in stats.items():
            if isinstance(v, int):
                totals[k] += v

    print(json.dumps({"files_processed": len(targets), "totals": dict(totals)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
