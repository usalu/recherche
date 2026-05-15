"""
Cleanup leftover `a_` prefix actor nodes from pre-transformer direct imports.

Two operations:
  1. RENAME  — nodes where canonical ID does not yet exist in the graph.
               Just SET n.id = canonical_id; all relationships auto-follow.
  2. MERGE   — nodes where canonical ID *already* exists (true duplicates or
               known-collision actors).  Redirect all rels to the canonical
               node, then DETACH DELETE the old `a_` node.

Idempotent: running twice has no effect (after the first run no `a_` actors
remain).

Known collision map (matches transform_registry_jsonl_to_canonical.py):
  a_slug  →  Canonical_ID  (when strip would give wrong casing/form)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _scripts.neo4j_env import resolve_connection
from neo4j import GraphDatabase

# ---------------------------------------------------------------------------
# Known ID collisions — must match _KNOWN_COLLISIONS in transformer
# ---------------------------------------------------------------------------
_KNOWN_COLLISIONS: dict[str, str] = {
    "a_patrick_teuffel":             "patrick_teuffel",
    "a_dirk_hebel":                  "Dirk_Hebel",
    "a_werner_sobek":                "Werner_Sobek",
    "a_superuse_studios":            "Superuse_Studios",
    "a_natural_building_lab":        "Natural_Building_Lab",
    "a_zrs_architekten_ingenieure":  "ZRS_Architekten_Ingenieure",
    "a_lendager":                    "Lendager",
    "a_cityfoerster":                "CITYFOERSTER",
    "a_bellastock":                  "Bellastock",
    "a_rotor":                       "Rotor",
}


def _canonical(old_id: str) -> str:
    """Compute canonical ID for an a_-prefix actor node."""
    if old_id in _KNOWN_COLLISIONS:
        return _KNOWN_COLLISIONS[old_id]
    result = old_id
    while result.startswith("a_"):
        result = result[2:]
    return result


def _run(tx, query: str, **params):
    return tx.run(query, **params).consume()


def _merge_node(session, old_id: str, canonical_id: str) -> None:
    """
    Redirect all relationships from old_id to canonical_id, then delete old_id.
    Uses MERGE for each relationship to avoid duplicates.
    """
    # Collect all outgoing rels from old node
    out_rels = session.run(
        "MATCH (n {id: $id})-[r]->(m) "
        "RETURN type(r) AS reltype, properties(r) AS props, m.id AS mid",
        id=old_id
    ).data()

    # Collect all incoming rels to old node
    in_rels = session.run(
        "MATCH (m)-[r]->(n {id: $id}) "
        "RETURN type(r) AS reltype, properties(r) AS props, m.id AS mid",
        id=old_id
    ).data()

    # Redirect outgoing
    for rec in out_rels:
        reltype = rec["reltype"]
        target_id = rec["mid"]
        # Drop 'id' — rel IDs embed the old a_ node slug and would violate uniqueness constraints
        props = {k: v for k, v in (rec["props"] or {}).items() if k != "id"}
        if props:
            q = (
                f"MATCH (a {{id: $canonical}}), (b {{id: $target}}) "
                f"MERGE (a)-[r:{reltype}]->(b) "
                f"ON CREATE SET r += $props"
            )
            session.execute_write(
                lambda tx, q=q, c=canonical_id, t=target_id, p=props:
                    _run(tx, q, canonical=c, target=t, props=p)
            )
        else:
            q = (
                f"MATCH (a {{id: $canonical}}), (b {{id: $target}}) "
                f"MERGE (a)-[:{reltype}]->(b)"
            )
            session.execute_write(
                lambda tx, q=q, c=canonical_id, t=target_id:
                    _run(tx, q, canonical=c, target=t)
            )

    # Redirect incoming
    for rec in in_rels:
        reltype = rec["reltype"]
        source_id = rec["mid"]
        props = {k: v for k, v in (rec["props"] or {}).items() if k != "id"}
        if props:
            q = (
                f"MATCH (a {{id: $source}}), (b {{id: $canonical}}) "
                f"MERGE (a)-[r:{reltype}]->(b) "
                f"ON CREATE SET r += $props"
            )
            session.execute_write(
                lambda tx, q=q, s=source_id, c=canonical_id, p=props:
                    _run(tx, q, source=s, canonical=c, props=p)
            )
        else:
            q = (
                f"MATCH (a {{id: $source}}), (b {{id: $canonical}}) "
                f"MERGE (a)-[:{reltype}]->(b)"
            )
            session.execute_write(
                lambda tx, q=q, s=source_id, c=canonical_id:
                    _run(tx, q, source=s, canonical=c)
            )

    # Delete old node
    session.execute_write(
        lambda tx: _run(tx, "MATCH (n {id: $id}) DETACH DELETE n", id=old_id)
    )


def main() -> None:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session(database=database) as s:

        # ---------------------------------------------------------------
        # 1. Fetch all a_ prefix actor nodes
        # ---------------------------------------------------------------
        rows = s.run(
            "MATCH (n:Akteur) WHERE n.id STARTS WITH 'a_' "
            "RETURN n.id AS old_id"
        ).data()
        old_ids = [r["old_id"] for r in rows]
        print(f"Found {len(old_ids)} `a_` prefix actor nodes")

        if not old_ids:
            print("Nothing to do.")
            return

        # ---------------------------------------------------------------
        # 2. Classify each node as RENAME or MERGE
        # ---------------------------------------------------------------
        rename_pairs: list[tuple[str, str]] = []
        merge_pairs:  list[tuple[str, str]] = []

        for old_id in old_ids:
            canon = _canonical(old_id)
            if canon == old_id:
                # Shouldn't happen, but skip if strip has no effect
                print(f"  SKIP (no change): {old_id}")
                continue
            # Check if canonical node already exists
            exists = s.run(
                "MATCH (n {id: $id}) RETURN count(n) AS cnt", id=canon
            ).single()["cnt"]
            if exists:
                merge_pairs.append((old_id, canon))
            else:
                rename_pairs.append((old_id, canon))

        print(f"  → RENAME: {len(rename_pairs)}, MERGE: {len(merge_pairs)}")

        # ---------------------------------------------------------------
        # 3. RENAME: just update the id property
        #    All relationships auto-follow because Neo4j uses internal IDs.
        # ---------------------------------------------------------------
        print("\n=== RENAME phase ===")
        renamed = 0
        for old_id, canon in rename_pairs:
            s.execute_write(
                lambda tx, oid=old_id, c=canon:
                    _run(tx, "MATCH (n {id: $old}) SET n.id = $new", old=oid, new=c)
            )
            renamed += 1
            if renamed % 50 == 0:
                print(f"  renamed {renamed}/{len(rename_pairs)} ...")
        print(f"  Done. Renamed {renamed} nodes.")

        # ---------------------------------------------------------------
        # 4. MERGE: redirect rels to canonical node, then delete old node
        # ---------------------------------------------------------------
        print("\n=== MERGE phase ===")
        merged = 0
        for old_id, canon in merge_pairs:
            print(f"  Merging {old_id} → {canon}")
            _merge_node(s, old_id, canon)
            merged += 1
        print(f"  Done. Merged {merged} duplicate nodes.")

    driver.close()

    print("\n=== Verification ===")
    driver2 = GraphDatabase.driver(uri, auth=(user, password))
    with driver2.session(database=database) as s:
        remaining = s.run(
            "MATCH (n:Akteur) WHERE n.id STARTS WITH 'a_' RETURN count(n) AS cnt"
        ).single()["cnt"]
        total_akteur = s.run(
            "MATCH (n:Akteur) RETURN count(n) AS cnt"
        ).single()["cnt"]
    driver2.close()
    print(f"  Remaining a_ prefix actors : {remaining}  (should be 0)")
    print(f"  Total Akteur nodes          : {total_akteur}")


if __name__ == "__main__":
    main()
