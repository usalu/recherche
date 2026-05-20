"""Recovery: rebuild Akteur.raw_role_evidence from the Wave-1 snapshot.

Agent 5's Phase 2.3 stripped `BETEILIGT_AN.rolle_text` and populated
`Akteur.raw_role_evidence` with strings of the form
`"<rolle_text> @ <target_id>"`. Agent 6's Phase 2.7 then overwrote that
field with empty lists (because by the time Phase 2.7 ran the source
property no longer existed on the live graph).

This script rebuilds the rollup from `snapshot/relationships.jsonl`
(captured before Wave 1 began, so it has every original rolle_text +
end-node id intact).

Idempotent: setting raw_role_evidence to the rebuilt list is the same
operation each run; safe to re-execute.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "runs"
    / "2026-05-20_radical_quality_reset"
)
SNAPSHOT_RELS = RUN_ROOT / "snapshot" / "relationships.jsonl"
SNAPSHOT_NODES = RUN_ROOT / "snapshot" / "nodes.jsonl"


def _resolve_connection() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, pw, _db = resolve_connection()
    return uri, user, pw, "mit-bestand"


def main() -> int:
    # Build a (internal_id -> akteur_id) map from snapshot/nodes.jsonl
    internal_to_akteur: dict[int, str] = {}
    with SNAPSHOT_NODES.open("r", encoding="utf-8") as fp:
        for line in fp:
            rec = json.loads(line)
            labels = rec.get("labels") or []
            if "Akteur" not in labels:
                continue
            iid = rec.get("internal_id")
            aid = (rec.get("properties") or {}).get("id")
            if iid is None or aid is None:
                continue
            internal_to_akteur[iid] = aid

    # Build a (internal_id -> end_node_id_property) for everything (since
    # BETEILIGT_AN targets are Projekt / Bauteilgruppe / Programm / etc.)
    internal_to_id: dict[int, str] = {}
    with SNAPSHOT_NODES.open("r", encoding="utf-8") as fp:
        for line in fp:
            rec = json.loads(line)
            iid = rec.get("internal_id")
            xid = (rec.get("properties") or {}).get("id")
            if iid is not None and xid is not None:
                internal_to_id[iid] = xid

    # Now collect rolle_text per akteur_id
    akteur_roles: dict[str, list[str]] = defaultdict(list)
    with SNAPSHOT_RELS.open("r", encoding="utf-8") as fp:
        for line in fp:
            rec = json.loads(line)
            if rec.get("type") != "BETEILIGT_AN":
                continue
            props = rec.get("properties") or {}
            rolle = props.get("rolle_text")
            if rolle is None:
                continue
            start_iid = rec.get("start_node_internal_id")
            end_iid = rec.get("end_node_internal_id")
            akteur_id = (
                internal_to_akteur.get(start_iid)
                or rec.get("start_node_id_property")
            )
            target_id = (
                internal_to_id.get(end_iid)
                or rec.get("end_node_id_property")
            )
            if not akteur_id:
                continue
            entry = f"{rolle} @ {target_id}" if target_id else rolle
            akteur_roles[akteur_id].append(entry)

    print(f"reconstructed roles for {len(akteur_roles)} akteurs from snapshot")
    # Normalize: keep stable order, dedupe within Akteur
    akteur_payload: dict[str, list[str]] = {
        a: sorted(set(roles)) for a, roles in akteur_roles.items()
    }
    print(f"sample: {list(akteur_payload.items())[:3]}")

    # Push to live graph. Agent 4's actor merges renamed some ids
    # (e.g. bauburo_in_situ -> baubuero_in_situ). Apply same mapping.
    id_remap = {
        "bauburo_in_situ": "baubuero_in_situ",
        "ak_plp_architecture": "plp_architecture",
        "zrs_architekten": "ZRS_Architekten_Ingenieure",
        "loeliger_strub_architektur": "loeliger_strub",
        "bill_dunster_zedfactory": "zedfactory_bill_dunster",
        "opera_pm": "opera",
        "Bellastock": "bellastock",
    }
    # Merge by canonical id
    canonical_payload: dict[str, list[str]] = defaultdict(list)
    for aid, roles in akteur_payload.items():
        canon = id_remap.get(aid, aid)
        canonical_payload[canon].extend(roles)
    canonical_payload = {a: sorted(set(r)) for a, r in canonical_payload.items()}

    from neo4j import GraphDatabase  # type: ignore

    uri, user, pw, db = _resolve_connection()
    drv = GraphDatabase.driver(uri, auth=(user, pw))
    drv.verify_connectivity()
    applied = 0
    missing = []
    with drv.session(database=db) as ses:
        for aid, roles in canonical_payload.items():
            rec = ses.run(
                "MATCH (a:Akteur {id: $aid}) RETURN count(a) AS c",
                {"aid": aid},
            ).single()
            if rec["c"] == 0:
                missing.append(aid)
                continue
            with ses.begin_transaction() as tx:
                tx.run(
                    "MATCH (a:Akteur {id: $aid}) SET a.raw_role_evidence = $roles",
                    {"aid": aid, "roles": roles},
                )
                tx.commit()
            applied += 1
        # Also: set EMPTY raw_role_evidence to NULL (clean up the
        # noise my buggy rollup created on the 492 unrelated Akteurs)
        ses.run(
            "MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL "
            "AND size(a.raw_role_evidence) = 0 REMOVE a.raw_role_evidence"
        ).consume()
    drv.close()
    print(f"restored raw_role_evidence on {applied} Akteurs; missing: {missing}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
