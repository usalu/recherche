"""Generate Phase L (property hygiene) patch JSONL.

L1: drop stray intake props on Material/Methode/Aufbereitungsverfahren/PruefungNachweis/Programm
L2: drop usage_project_count/usage_countries/usage_project_ids on Norm
L3: drop stars_ignored on Akteur
L4: normalize Quelle (titel/name/name_full + filename/dateiname → source_file)
L5: add country_iso2 to sovereign Land nodes
"""

from __future__ import annotations

import json
from pathlib import Path
from neo4j import GraphDatabase
from _scripts.neo4j_env import resolve_connection


OUT = Path("_neo4j/review/round_002_followup/patches/phase_l.patch.jsonl")

L1_KEYS = ["scope", "topic", "classified_at", "not_yet_referenced_in_corpus", "standards_body"]
L1_LABELS = ["Material", "Methode", "Aufbereitungsverfahren", "PruefungNachweis", "Programm"]

L2_KEYS = ["usage_project_count", "usage_countries", "usage_project_ids"]

# ISO 3166-1 alpha-2 codes; supranational nodes (land_eu/eea/international) intentionally skipped
LAND_ISO2 = {
    "land_belgien": "BE",
    "land_daenemark": "DK",
    "land_deutschland": "DE",
    "land_finnland": "FI",
    "land_frankreich": "FR",
    "land_japan": "JP",
    "land_luxemburg": "LU",
    "land_niederlande": "NL",
    "land_norwegen": "NO",
    "land_oesterreich": "AT",
    "land_schweiz": "CH",
    "land_usa": "US",
    "land_vereinigtes_koenigreich": "GB",
}

ELLIPSIS = "…"


def short_from(long: str, limit: int = 25) -> str:
    """Truncate `long` to <=limit chars using ellipsis."""
    if len(long) <= limit:
        return long
    return long[: limit - 1] + ELLIPSIS


def emit(records: list[dict], op: dict) -> None:
    records.append(op)


def main() -> None:
    uri, user, password, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    records: list[dict] = []

    with driver.session(database=db) as s:
        # ── L1: drop stray intake props ─────────────────────────────────────
        for label in L1_LABELS:
            q = (
                f"MATCH (n:{label}) WHERE "
                + " OR ".join(f"n.{k} IS NOT NULL" for k in L1_KEYS)
                + " RETURN n.id AS id"
            )
            for row in s.run(q):
                emit(records, {
                    "op": "remove_node_properties",
                    "id": row["id"],
                    "properties": L1_KEYS,
                    "reason": f"L1: drop stray intake props on {label}",
                    "severity": "LOW",
                })

        # ── L2: Norm derivable usage_* props ────────────────────────────────
        for row in s.run(
            "MATCH (n:Norm) WHERE n.usage_project_count IS NOT NULL OR n.usage_countries IS NOT NULL OR n.usage_project_ids IS NOT NULL RETURN n.id AS id"
        ):
            emit(records, {
                "op": "remove_node_properties",
                "id": row["id"],
                "properties": L2_KEYS,
                "reason": "L2: drop derivable usage_* props on Norm",
                "severity": "LOW",
            })

        # ── L3: Akteur stars_ignored ────────────────────────────────────────
        for row in s.run("MATCH (n:Akteur) WHERE n.stars_ignored IS NOT NULL RETURN n.id AS id"):
            emit(records, {
                "op": "remove_node_properties",
                "id": row["id"],
                "properties": ["stars_ignored"],
                "reason": "L3: drop stale CSV column stars_ignored",
                "severity": "LOW",
            })

        # ── L4 Quelle normalization ─────────────────────────────────────────
        # 4a. both name+titel (1 node, same value): drop titel + dateiname if duplicate of source_file
        for row in s.run(
            "MATCH (q:Quelle) WHERE q.name IS NOT NULL AND q.titel IS NOT NULL RETURN q.id AS id, q.name AS name, q.titel AS titel, q.dateiname AS dateiname, q.source_file AS sf"
        ):
            drop = []
            if row["titel"] == row["name"]:
                drop.append("titel")
            if row["dateiname"] is not None and row["sf"] is not None and row["dateiname"] == row["sf"]:
                drop.append("dateiname")
            if drop:
                emit(records, {
                    "op": "remove_node_properties",
                    "id": row["id"],
                    "properties": drop,
                    "reason": "L4: drop duplicate titel/dateiname (same value as name/source_file)",
                    "severity": "LOW",
                })

        # 4b. titel_only ≤ 25 chars: rename titel → name
        for row in s.run(
            "MATCH (q:Quelle) WHERE q.titel IS NOT NULL AND q.name IS NULL AND size(q.titel) <= 25 RETURN q.id AS id"
        ):
            emit(records, {
                "op": "rename_property",
                "id": row["id"],
                "from": "titel",
                "to": "name",
                "reason": "L4: titel ≤ 25 chars becomes the canonical name",
                "severity": "LOW",
            })

        # 4c. titel_only > 25 chars: rename titel → name_full, then set short name
        for row in s.run(
            "MATCH (q:Quelle) WHERE q.titel IS NOT NULL AND q.name IS NULL AND size(q.titel) > 25 RETURN q.id AS id, q.titel AS titel"
        ):
            emit(records, {
                "op": "rename_property",
                "id": row["id"],
                "from": "titel",
                "to": "name_full",
                "reason": "L4: long titel becomes name_full",
                "severity": "LOW",
            })
            emit(records, {
                "op": "set_node_properties",
                "id": row["id"],
                "properties": {"name": short_from(row["titel"])},
                "reason": "L4: derive short name from name_full (truncation)",
                "severity": "LOW",
            })

        # 4d. name_only > 25 chars: set name_full = current name, set short name
        for row in s.run(
            "MATCH (q:Quelle) WHERE q.name IS NOT NULL AND q.titel IS NULL AND size(q.name) > 25 RETURN q.id AS id, q.name AS name"
        ):
            emit(records, {
                "op": "set_node_properties",
                "id": row["id"],
                "properties": {"name_full": row["name"], "name": short_from(row["name"])},
                "reason": "L4: long name becomes name_full; derive short name (truncation)",
                "severity": "LOW",
            })

        # 4e. filename → source_file
        for row in s.run(
            "MATCH (q:Quelle) WHERE q.filename IS NOT NULL AND q.source_file IS NULL RETURN q.id AS id"
        ):
            emit(records, {
                "op": "rename_property",
                "id": row["id"],
                "from": "filename",
                "to": "source_file",
                "reason": "L4: unify filename → source_file",
                "severity": "LOW",
            })

        # ── L5: country_iso2 on sovereign Land nodes ────────────────────────
        for land_id, iso2 in LAND_ISO2.items():
            emit(records, {
                "op": "set_node_properties",
                "id": land_id,
                "properties": {"country_iso2": iso2},
                "reason": f"L5: add ISO 3166-1 alpha-2 code ({iso2})",
                "severity": "LOW",
            })

    driver.close()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    by_op: dict[str, int] = {}
    for r in records:
        by_op[r["op"]] = by_op.get(r["op"], 0) + 1
    print(f"Wrote {len(records)} ops to {OUT}")
    for op, c in sorted(by_op.items()):
        print(f"  {op}: {c}")


if __name__ == "__main__":
    main()
