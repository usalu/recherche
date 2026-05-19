"""Phase R full repair — bulk r.id rebuild + HAT_MATERIALGRUPPE backfill.

Done with direct Cypher writes because the JSONL patch tool would generate
thousands of individual set_rel_properties / delete_rel ops for what is fundamentally
4 bulk operations:

  R-4:  delete 31 redundant parallel rels (same from-type-to, identical content)
  R-1a: REMOVE r.id from 2523 stale rels (id doesn't match canonical form)
  R-1b: SET r.id = canonical on all rels with null r.id (now 2603 = 2523 cleared + 80 original)
  R-3:  add HAT_MATERIALGRUPPE rels to 134 BGs (derived from NUTZT_MATERIAL via canonical map)

Outputs an audit report at _neo4j/review/round_002_followup/phase_r_full_report.json.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from neo4j import GraphDatabase
from _scripts.neo4j_env import resolve_connection


REPORT = Path("_neo4j/review/round_002_followup/phase_r_full_report.json")
CONFIRM = "APPLY phase_r_full TO mit-bestand"


def main() -> None:
    import sys
    if "--confirm" not in sys.argv or sys.argv[sys.argv.index("--confirm") + 1] != CONFIRM:
        dry_run = True
        print("DRY-RUN MODE — pass --confirm '" + CONFIRM + "' to apply")
    else:
        dry_run = False
        print("LIVE APPLY MODE — modifications will be committed")
    print()

    uri, user, password, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict = {"timestamp": datetime.utcnow().isoformat(), "dry_run": dry_run, "steps": []}

    with driver.session(database=db) as s:
        # Counts before
        before_nodes = s.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        before_rels = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
        report["before"] = {"nodes": before_nodes, "relationships": before_rels}
        print(f"BEFORE: nodes={before_nodes}, rels={before_rels}")

        # ── R-4: Delete redundant parallel rels (same from-type-to, multiple rels) ──
        print("\n── R-4: Delete redundant parallel rels ──")
        count_before = s.run("""
            MATCH (a)-[r]->(b)
            WITH a.id AS aid, type(r) AS rt, b.id AS bid, count(r) AS c
            WHERE c > 1
            RETURN sum(c - 1) AS total
        """).single()["total"]
        print(f"  Planned deletions: {count_before}")

        if not dry_run and count_before > 0:
            # Use elementId to identify unique rels — collect, keep first, delete rest
            result = s.run("""
                MATCH (a)-[r]->(b)
                WITH a.id AS aid, type(r) AS rt, b.id AS bid, collect(r) AS rels
                WHERE size(rels) > 1
                UNWIND rels[1..] AS dup
                DELETE dup
                RETURN count(dup) AS deleted
            """).single()
            print(f"  Deleted: {result['deleted']}")
            report["steps"].append({"step": "R-4 delete_parallel_dupes", "deleted": result["deleted"]})
        else:
            report["steps"].append({"step": "R-4 delete_parallel_dupes", "would_delete": count_before})

        # ── R-1a: REMOVE r.id from stale rels (id doesn't match canonical) ──
        print("\n── R-1a: REMOVE stale r.id ──")
        stale_before = s.run("""
            MATCH (a)-[r]->(b)
            WHERE r.id IS NOT NULL
            AND r.id <> 'r_' + a.id + '__' + type(r) + '__' + b.id
            RETURN count(r) AS c
        """).single()["c"]
        print(f"  Stale r.id rels: {stale_before}")

        if not dry_run and stale_before > 0:
            result = s.run("""
                MATCH (a)-[r]->(b)
                WHERE r.id IS NOT NULL
                AND r.id <> 'r_' + a.id + '__' + type(r) + '__' + b.id
                REMOVE r.id
                RETURN count(r) AS cleared
            """).single()
            print(f"  Cleared: {result['cleared']}")
            report["steps"].append({"step": "R-1a remove_stale_rids", "cleared": result["cleared"]})
        else:
            report["steps"].append({"step": "R-1a remove_stale_rids", "would_clear": stale_before})

        # ── R-1b + R-2: SET canonical r.id on all rels with null r.id ──
        print("\n── R-1b + R-2: SET canonical r.id where null ──")
        missing_before = s.run("MATCH ()-[r]->() WHERE r.id IS NULL RETURN count(r) AS c").single()["c"]
        print(f"  Rels with null r.id: {missing_before}")

        if not dry_run and missing_before > 0:
            result = s.run("""
                MATCH (a)-[r]->(b)
                WHERE r.id IS NULL
                SET r.id = 'r_' + a.id + '__' + type(r) + '__' + b.id
                RETURN count(r) AS set_count
            """).single()
            print(f"  Set: {result['set_count']}")
            report["steps"].append({"step": "R-1b+R-2 set_canonical_rids", "set": result["set_count"]})
        else:
            report["steps"].append({"step": "R-1b+R-2 set_canonical_rids", "would_set": missing_before})

        # ── R-3: Add HAT_MATERIALGRUPPE rels to 134 BGs ──
        print("\n── R-3: Add HAT_MATERIALGRUPPE on BGs with NUTZT_MATERIAL but no group ──")
        bg_before = s.run("""
            MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->()
            WITH bg WHERE NOT (bg)-[:HAT_MATERIALGRUPPE]->()
            RETURN count(DISTINCT bg) AS c
        """).single()["c"]
        print(f"  BGs to backfill: {bg_before}")

        if not dry_run and bg_before > 0:
            # Use the canonical Material -> Materialgruppe map and create rels with canonical r.id
            result = s.run("""
                MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)-[:HAT_MATERIALGRUPPE]->(g:Materialgruppe)
                WITH DISTINCT bg, g
                WHERE NOT (bg)-[:HAT_MATERIALGRUPPE]->(g)
                MERGE (bg)-[r:HAT_MATERIALGRUPPE]->(g)
                ON CREATE SET r.id = 'r_' + bg.id + '__HAT_MATERIALGRUPPE__' + g.id,
                              r.source = 'Phase R-3 derived from Material->Materialgruppe canonical map'
                RETURN count(r) AS created
            """).single()
            print(f"  Created HAT_MATERIALGRUPPE rels: {result['created']}")
            report["steps"].append({"step": "R-3 add_materialgruppe", "created": result["created"]})
        else:
            # Estimate count
            est = s.run("""
                MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)-[:HAT_MATERIALGRUPPE]->(g:Materialgruppe)
                WITH DISTINCT bg, g
                WHERE NOT (bg)-[:HAT_MATERIALGRUPPE]->(g)
                RETURN count(*) AS c
            """).single()["c"]
            print(f"  Would create HAT_MATERIALGRUPPE rels: {est}")
            report["steps"].append({"step": "R-3 add_materialgruppe", "would_create": est})

        # Counts after
        after_nodes = s.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        after_rels = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
        report["after"] = {"nodes": after_nodes, "relationships": after_rels}
        print(f"\nAFTER: nodes={after_nodes}, rels={after_rels} (delta: nodes={after_nodes-before_nodes}, rels={after_rels-before_rels})")

        # Post-checks
        print("\n── Verification ──")
        c = s.run("MATCH ()-[r]->() WHERE r.id IS NULL RETURN count(r) AS c").single()["c"]
        print(f"  Rels still missing r.id: {c} (expect 0 after live)")
        c = s.run("""MATCH (a)-[r]->(b) WHERE r.id IS NOT NULL
            AND r.id <> 'r_' + a.id + '__' + type(r) + '__' + b.id
            RETURN count(r) AS c""").single()["c"]
        print(f"  Rels with stale r.id: {c} (expect 0 after live)")
        c = s.run("""MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->()
            WITH bg WHERE NOT (bg)-[:HAT_MATERIALGRUPPE]->()
            RETURN count(DISTINCT bg) AS c""").single()["c"]
        print(f"  BGs with NUTZT_MATERIAL but 0 HAT_MATERIALGRUPPE: {c} (expect 0)")
        c = s.run("""MATCH (a)-[r1]->(b), (a)-[r2]->(b)
            WHERE elementId(r1) < elementId(r2) AND type(r1) = type(r2)
            RETURN count(*) AS c""").single()["c"]
        print(f"  Parallel rel pairs: {c} (expect 0)")
        c = s.run("""MATCH ()-[r]->() WITH r.id AS rid, type(r) AS rt, count(r) AS c
            WHERE c > 1 AND rid IS NOT NULL RETURN count(*) AS c""").single()["c"]
        print(f"  Duplicate r.id within same rel type: {c} (expect 0)")

    driver.close()

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nReport written to {REPORT}")


if __name__ == "__main__":
    main()
