"""Generate the Bauteilgruppe rename table for Phase O (pre-step 2).

New id schema: bg_<reuse-status>_<material>_<bauteiltyp>_<discriminator>
Companion props every BG gets: reuse_status, primary_material_id, primary_bauteiltyp_id, name (short), name_full, aliases=[old_id]

Output: CSV at _neo4j/review/round_002_followup/phase_o_rename_table.csv
"""

from __future__ import annotations

import csv
from pathlib import Path
from neo4j import GraphDatabase
from _scripts.neo4j_env import resolve_connection


OUT_CSV = Path("_neo4j/review/round_002_followup/phase_o_rename_table.csv")
SHORT_LIMIT = 25
ELLIPSIS = "…"

REUSE_STATUS_TOKENS = ("reused", "retained", "planned", "dismantled")
STATUS_MAP = {
    "reused": "reuse",
    "retained": "retained",
    "planned": "planned",
    "dismantled": "dismantled",
}


def strip_id_prefix(node_id: str, prefix: str) -> str:
    if node_id.startswith(prefix):
        return node_id[len(prefix):]
    return node_id


def find_reuse_status_token(old_id_stripped: str) -> str:
    """Return canonical reuse_status from old id tokens; default 'reuse'."""
    tokens = old_id_stripped.split("_")
    for tok in tokens:
        if tok in REUSE_STATUS_TOKENS:
            return STATUS_MAP[tok]
    return "reuse"


def strip_status_tokens(old_id_stripped: str) -> str:
    tokens = old_id_stripped.split("_")
    kept = [t for t in tokens if t not in REUSE_STATUS_TOKENS]
    return "_".join(kept)


def shorten_word_aware(s: str, limit: int = SHORT_LIMIT) -> str:
    if not s or len(s) <= limit:
        return s or ""
    cut = limit - 1
    chunk = s[:cut]
    sp = chunk.rfind(" ")
    if sp >= cut - 8 and sp > 0:
        chunk = chunk[:sp]
    return chunk + ELLIPSIS


def main() -> None:
    uri, user, password, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    rows: list[dict] = []
    with driver.session(database=db) as s:
        bg_rows = list(s.run(
            """MATCH (bg:Bauteilgruppe)
               OPTIONAL MATCH (bg)-[:NUTZT_MATERIAL]->(m:Material)
               OPTIONAL MATCH (bg)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
               WITH bg, collect(DISTINCT m.id) AS mats, collect(DISTINCT bt.id) AS bts
               RETURN bg.id AS id, bg.name AS name, mats, bts ORDER BY bg.id"""
        ))

        for r in bg_rows:
            old_id = r["id"]
            current_name = r["name"] or ""
            mats = [m for m in r["mats"] if m]
            bts = [b for b in r["bts"] if b]

            # ── reuse_status ────────────────────────────────────────────────
            old_id_body = strip_id_prefix(old_id, "bg_")
            reuse_status = find_reuse_status_token(old_id_body)

            # ── material slot ───────────────────────────────────────────────
            if len(mats) == 0:
                mat_id = "mat_unbekannt"
                mat_slot = "unbekannt"
            elif len(mats) == 1:
                mat_id = mats[0]
                mat_slot = strip_id_prefix(mat_id, "mat_")
            else:
                mat_id = "mat_mehrere"
                mat_slot = "mehrere"

            # ── bauteiltyp slot ─────────────────────────────────────────────
            if len(bts) == 0:
                bt_id = "bt_unbekannt"
                bt_slot = "unbekannt"
            elif len(bts) == 1:
                bt_id = bts[0]
                bt_slot = strip_id_prefix(bt_id, "bt_")
            else:
                bt_id = "bt_mehrere"
                bt_slot = "mehrere"

            # ── discriminator ───────────────────────────────────────────────
            discriminator = strip_status_tokens(old_id_body)

            # Compose new id
            new_id = f"bg_{reuse_status}_{mat_slot}_{bt_slot}_{discriminator}"

            # ── short name ──────────────────────────────────────────────────
            short_name = shorten_word_aware(current_name)
            name_full = current_name if short_name != current_name else ""

            rows.append({
                "old_id": old_id,
                "new_id": new_id,
                "name": short_name,
                "name_full": name_full,
                "reuse_status": reuse_status,
                "primary_material_id": mat_id,
                "primary_bauteiltyp_id": bt_id,
                "discriminator": discriminator,
                "n_materials": len(mats),
                "n_bauteiltypen": len(bts),
                "manual_override": "yes" if (len(mats) == 0 or len(mats) >= 2 or len(bts) >= 2) else "no",
            })

    driver.close()

    # ── Check uniqueness of new_id ──────────────────────────────────────────
    by_new: dict[str, list[str]] = {}
    for row in rows:
        by_new.setdefault(row["new_id"], []).append(row["old_id"])
    collisions = {nid: olds for nid, olds in by_new.items() if len(olds) > 1}

    # ── Write CSV ──────────────────────────────────────────────────────────
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows:
            w.writerow(row)

    print(f"Wrote {len(rows)} rows to {OUT_CSV}")
    # Summary stats
    by_status: dict[str, int] = {}
    by_mat: dict[str, int] = {}
    by_bt: dict[str, int] = {}
    manual = 0
    for row in rows:
        by_status[row["reuse_status"]] = by_status.get(row["reuse_status"], 0) + 1
        by_mat[row["primary_material_id"]] = by_mat.get(row["primary_material_id"], 0) + 1
        by_bt[row["primary_bauteiltyp_id"]] = by_bt.get(row["primary_bauteiltyp_id"], 0) + 1
        if row["manual_override"] == "yes":
            manual += 1
    print(f"\nreuse_status: {by_status}")
    print(f"\nprimary_material_id top: " + ", ".join(f"{k}={v}" for k, v in sorted(by_mat.items(), key=lambda x: -x[1])[:8]))
    print(f"\nprimary_bauteiltyp_id top: " + ", ".join(f"{k}={v}" for k, v in sorted(by_bt.items(), key=lambda x: -x[1])[:8]))
    print(f"\nmanual_override (multi-axis or zero-material): {manual} rows")
    print(f"\nnew_id collisions: {len(collisions)}")
    if collisions:
        for nid, olds in collisions.items():
            print(f"  {nid}: {olds}")


if __name__ == "__main__":
    main()
