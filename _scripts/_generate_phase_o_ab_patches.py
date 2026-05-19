"""Generate Phase O.a (305 add_node) and Phase O.b (305 merge_node) patches.

Reads the rename CSV at _neo4j/review/round_002_followup/phase_o_rename_table_v3.csv
(305 rows after Phase O.0 — the 3 Verbiest split BGs are already schema-compliant and
excluded from the rename).

O.a: creates a new BG node for each row with the new id and all schema properties.
     Old BG keeps its rels until O.b runs.
O.b: merges each old BG into its new counterpart — apply tool's `merge_node`
     redirects all in/out rels onto the new node, rewrites outbound r.id strings
     from `r_<old>__TYPE__<x>` to `r_<new>__TYPE__<x>`, unions labels, merges
     properties, then DETACH DELETEs the old node.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


RENAME_CSV = Path("_neo4j/review/round_002_followup/phase_o_rename_table_v3.csv")
OUT_A = Path("_neo4j/review/round_002_followup/patches/phase_oa.patch.jsonl")
OUT_B = Path("_neo4j/review/round_002_followup/patches/phase_ob.patch.jsonl")


def main() -> None:
    with RENAME_CSV.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    a_records: list[dict] = []
    b_records: list[dict] = []
    for row in rows:
        old_id = row["old_id"]
        new_id = row["new_id"]
        short_name = row["name"]
        name_full = row["name_full"]

        props = {
            "id": new_id,
            "name": short_name,
            "reuse_status": row["reuse_status"],
            "primary_material_id": row["primary_material_id"],
            "primary_bauteiltyp_id": row["primary_bauteiltyp_id"],
            "aliases": [old_id],
        }
        # name_full only when meaningfully different (Q3 decision)
        if name_full:
            props["name_full"] = name_full

        a_records.append({
            "op": "add_node",
            "id": new_id,
            "labels": ["Bauteilgruppe"],
            "properties": props,
            "reason": f"Phase O.a — create Phase-O-schema-compliant BG (old id preserved in aliases)",
            "severity": "MEDIUM",
        })

        b_records.append({
            "op": "merge_node",
            "from": old_id,
            "to": new_id,
            "reason": f"Phase O.b — merge {old_id} → {new_id} (redirect rels + rewrite r.id outbound)",
            "severity": "HIGH",
        })

    OUT_A.parent.mkdir(parents=True, exist_ok=True)
    with OUT_A.open("w", encoding="utf-8") as f:
        for r in a_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with OUT_B.open("w", encoding="utf-8") as f:
        for r in b_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"O.a: wrote {len(a_records)} add_node ops to {OUT_A}")
    print(f"O.b: wrote {len(b_records)} merge_node ops to {OUT_B}")


if __name__ == "__main__":
    main()
