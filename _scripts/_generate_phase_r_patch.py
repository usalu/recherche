"""Generate Phase R — mechanical refinement patch.

Two fixes, both fully derivable from current graph state:

R-C: Backfill r.id on the 195 rels that lack it (BETEILIGT_AN / BELEGT_IN /
     HAT_RESSOURCENQUELLE / HAT_AKTEURROLLE / HAT_AKTEURTYP and a few others).
     Pre-check confirmed 0 parallel rels of same (from, type, to) — safe.
     Convention: r.id = 'r_<from-id>__<TYPE>__<to-id>'

R-D: Backfill HAT_MATERIALGRUPPE on the 134 BGs that have NUTZT_MATERIAL rels
     but 0 HAT_MATERIALGRUPPE. Materialgruppe is derived from Material via
     a many-to-many mapping read from the live graph (Material has its own
     HAT_MATERIALGRUPPE rels documenting the canonical assignment).
"""

from __future__ import annotations

import json
from pathlib import Path
from neo4j import GraphDatabase
from _scripts.neo4j_env import resolve_connection


OUT = Path("_neo4j/review/round_002_followup/patches/phase_r.patch.jsonl")


def rel_id(from_id: str, rel_type: str, to_id: str) -> str:
    return f"r_{from_id}__{rel_type}__{to_id}"


def main() -> None:
    uri, user, password, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    records: list[dict] = []

    with driver.session(database=db) as s:
        # ── R-C: Backfill r.id on rels missing it ──────────────────────────
        rid_targets = list(s.run(
            """MATCH (a)-[r]->(b)
               WHERE r.id IS NULL
               RETURN a.id AS from_id, type(r) AS rt, b.id AS to_id
               ORDER BY rt, from_id, to_id"""
        ))
        for row in rid_targets:
            from_id, rt, to_id = row["from_id"], row["rt"], row["to_id"]
            records.append({
                "op": "set_rel_properties",
                "from": from_id,
                "to": to_id,
                "type": rt,
                "properties": {"id": rel_id(from_id, rt, to_id)},
                "reason": "Phase R-C — backfill missing r.id (convention: r_<from>__<TYPE>__<to>)",
                "severity": "LOW",
            })

        # ── R-D: Add HAT_MATERIALGRUPPE rels derived from NUTZT_MATERIAL ──
        # Read the canonical Material → Materialgruppe map from the existing
        # rels on Material nodes (many-to-many: e.g. mat_bitumen → kunststoff + verbundstoff).
        mat_to_groups: dict[str, list[str]] = {}
        for r in s.run(
            "MATCH (m:Material)-[:HAT_MATERIALGRUPPE]->(g:Materialgruppe) "
            "RETURN m.id AS m, g.id AS g ORDER BY m.id, g.id"
        ):
            mat_to_groups.setdefault(r["m"], []).append(r["g"])

        # Find BGs that have at least one NUTZT_MATERIAL but 0 HAT_MATERIALGRUPPE
        candidates = list(s.run(
            """MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
               WITH bg, collect(DISTINCT m.id) AS mats
               WHERE NOT (bg)-[:HAT_MATERIALGRUPPE]->()
               RETURN bg.id AS id, mats ORDER BY bg.id"""
        ))
        for row in candidates:
            bg_id = row["id"]
            mats = row["mats"]
            # Derive group set as union of each material's groups
            groups: set[str] = set()
            for m in mats:
                groups.update(mat_to_groups.get(m, []))
            for g in sorted(groups):
                records.append({
                    "op": "add_rel",
                    "from": bg_id,
                    "to": g,
                    "type": "HAT_MATERIALGRUPPE",
                    "properties": {
                        "id": rel_id(bg_id, "HAT_MATERIALGRUPPE", g),
                        "source": "Phase R-D derived from Material→Materialgruppe canonical mapping",
                    },
                    "reason": f"Phase R-D — derived from {mats} → {sorted(groups)}",
                    "severity": "LOW",
                })

    driver.close()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    by_op: dict[str, int] = {}
    for r in records:
        by_op[r["op"]] = by_op.get(r["op"], 0) + 1
    print(f"Wrote {len(records)} ops to {OUT}")
    for op, c in sorted(by_op.items()):
        print(f"  {op}: {c}")
    print(f"\n  R-C r.id backfills: {by_op.get('set_rel_properties', 0)}")
    print(f"  R-D HAT_MATERIALGRUPPE adds: {by_op.get('add_rel', 0)}")


if __name__ == "__main__":
    main()
