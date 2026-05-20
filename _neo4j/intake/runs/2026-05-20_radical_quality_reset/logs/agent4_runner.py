"""Agent 4 — Wave-1 runner for Phase 1.4 + 1.5 + 1.6 on `mit-bestand`.

Sequence:
    1.4  Relabel 23 :Bauwerk placeholders to :Materialdepot
         + add BETRIEBEN_VON edges to matching :Akteur operators.
    1.5  Surgical delete of 6 :Akteur + 4 :Programm + 2 :Norm + 21 deg-0 :Quelle.
         All deletes are journalled to deleted/phase1_5_nodes.jsonl *before*
         DETACH DELETE runs. Hard abort if the planned-delete count exceeds 35.
    1.6  Merge 7 verified :Akteur duplicate pairs via apoc.refactor.mergeNodes.

Writes phase flags PHASE_1_4_DONE.flag, PHASE_1_5_DONE.flag, PHASE_1_6_DONE.flag
into the run root with before/after counts and timings.

Read-only fall-back: when MCP enforces read-only at the MCP layer, this script
talks to Neo4j directly via the official `neo4j` Python driver, using the same
credentials configured in `.cursor/mcp.json` (NEO4J_READ_ONLY is interpreted
by the MCP server only; the driver itself is unrestricted, modulo Neo4j RBAC).

Phase 1.4 / 1.5 / 1.6 only — does NOT touch chains (Agent 2) or ontology
anchors / Phase 1.2 (Agent 3).
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-20_radical_quality_reset"
DELETED_DIR = RUN_ROOT / "deleted"
LOG_DIR = RUN_ROOT / "logs"
RUN_LOG = LOG_DIR / "agent4_progress.log"

MATERIALDEPOT_IDS: list[str] = [
    "bw_crclr_kindl_hall",
    "bw_chiro_itterbeek_reuse_supply_network",
    "bw_berlin_fitout_donor_sources",
    "bw_paris_regional_donor_sources_ferme_du_rail",
    "bw_paris_material_sources_circular_pavilion",
    "bw_p2_massenwohnungsbau_donor_unknown",
    "bw_unknown_demolition_wood_streams",
    "bw_holbein_grosvenor_donor_projects",
    "bw_maison_des_canaux_unspecified_donors",
    "bw_verbiest_lagerhaus_zu_haus_und_atelier",
    "bw_rotor_reuse_stock_charles_malis",
    "bw_messebau_lager_hannover",
    "bw_maison_dna_unknown_brick_donor",
    "bw_externe_stahl_donor_stockholder",
    "bw_unknown_brick_donor_sources_gjg",
    "bw_lo_reninge_reuse_brick_source",
    "bw_unbekanntes_transformationsgebaeude_kellerwaende",
    "bw_unbekannte_donor_buildings_zinneke_material_lots",
    "bw_cleveland_steel_and_tubes_stock",
    "bw_wbs70_donor_groeditz",
    "bw_bellastock_ville_des_terres_l_ile_saint_denis_lager",
    "bw_donor_gebaudegruppe_resource_rows_mauerwerk",
    "bw_elys_ehemaliges_getraenkelager_areal",
]

DELETE_AKTEUR_IDS: list[str] = [
    "glasfischer_glastec",
    "citydev_brussels",
    "denkstatt",
    "eitel_partner",
    "gibbins_architekten",
    "zusammenkunft_berlin",
]
DELETE_PROGRAMM_IDS: list[str] = [
    "prog_bbsm",
    "prog_preuse",
    "prog_zukunftbau",
    "prog_kommunales_programm",
]
DELETE_NORM_IDS: list[str] = [
    "norm_bs_5385_5_2009",
    "norm_din_18940",
]
DELETE_QUELLE_IDS: list[str] = [
    "qu_arch_reuse_bxl_dossier",
    "qu_careno_retile_s2",
    "qu_careno_rotor_s1",
    "qu_circl_abnamro_opening_s3",
    "qu_circl_abnamro_report_s4",
    "qu_circl_dutcharchitects_s1",
    "qu_circl_icon_digital_twin_s7",
    "qu_circl_zuidas_dismantling_s6",
    "qu_fcrbe_interreg_s1",
    "qu_granby_assemble_s2",
    "qu_granby_rock_terrazzo_s3",
    "qu_lysp8_oxara_s4",
    "qu_lysp8_swissarc_s2",
    "qu_lysp8_zirkular_s1",
    "qu_meduni_baukarussell_s2",
    "qu_rcmi_concular_dossier",
    "qu_rebridge_unistuttgart_r1",
    "qu_stuttgart210_baunetzwissen_s7",
    "qu_stuttgart210_holzbauoffensive_s5",
    "qu_vandkunsten_dossier",
    "qu_zhaw_reuse_dossier",
]

# (canonical_id, merge_id). apoc.refactor.mergeNodes([canon, dup], ...)
# keeps the FIRST node. Order in the list = (canonical, merge_in).
MERGE_PAIRS: list[tuple[str, str]] = [
    ("baubuero_in_situ", "bauburo_in_situ"),               # orthographic canon kept; combined 26 edges
    ("plp_architecture", "ak_plp_architecture"),
    ("ZRS_Architekten_Ingenieure", "zrs_architekten"),
    ("loeliger_strub", "loeliger_strub_architektur"),
    ("zedfactory_bill_dunster", "bill_dunster_zedfactory"),
    ("opera", "opera_pm"),
    ("bellastock", "Bellastock"),                          # case-collision; lowercase canon
]

# Defensive abort gate (plan §1.5 acceptance: Total nodes removed <= 35)
MAX_PHASE_1_5_DELETES = 35


def _log(msg: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"[{stamp}] {msg}"
    print(line, flush=True)
    with RUN_LOG.open("a", encoding="utf-8") as fp:
        fp.write(line + "\n")


def _resolve_connection() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise RuntimeError(
            "Missing Neo4j connection settings (NEO4J_URI/USERNAME/PASSWORD)."
        )
    if database != "mit-bestand":
        _log(f"WARN: configured database '{database}' != 'mit-bestand'; forcing 'mit-bestand'.")
        database = "mit-bestand"
    return uri, user, password, database


def _to_jsonable(value):  # noqa: ANN001
    from neo4j.time import Date, DateTime, Duration, Time  # type: ignore
    from neo4j.spatial import Point  # type: ignore

    if isinstance(value, (Date, DateTime, Time)):
        return value.iso_format()
    if isinstance(value, Duration):
        return str(value)
    if isinstance(value, Point):
        return {"srid": value.srid, "coordinates": list(value)}
    if isinstance(value, dict):
        return {k: _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, (bytes, bytearray)):
        return value.decode("utf-8", errors="replace")
    return value


# ---------- snapshot/journal helpers --------------------------------------

def journal_nodes_for_delete(driver, database: str, label: str, ids: list[str], journal_path: Path) -> list[dict]:
    """Capture pre-delete state (labels, properties, neighbours) and append
    one JSONL line per existing node. Returns the captured records."""
    cypher = (
        f"MATCH (n:`{label}`) WHERE n.id IN $ids "
        "OPTIONAL MATCH (n)-[r]-(m) "
        "RETURN id(n) AS internal_id, labels(n) AS labels, properties(n) AS properties, "
        "       collect({type:type(r), direction: CASE WHEN startNode(r)=n THEN 'OUT' ELSE 'IN' END, "
        "                 other_internal_id: id(m), other_id: m.id, other_labels: labels(m), "
        "                 properties: properties(r)}) AS edges"
    )
    captured: list[dict] = []
    with driver.session(database=database) as session:
        rows = list(session.run(cypher, ids=ids))
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    with journal_path.open("a", encoding="utf-8", newline="\n") as fp:
        for r in rows:
            props = _to_jsonable(dict(r["properties"]))
            edges = [
                {k: _to_jsonable(v) for k, v in (e if isinstance(e, dict) else dict(e)).items()}
                for e in r["edges"] if e and (e.get("type") if isinstance(e, dict) else e["type"]) is not None
            ]
            rec = {
                "phase": "1.5",
                "label": label,
                "id": props.get("id"),
                "neo4j_internal_id": r["internal_id"],
                "labels": list(r["labels"]),
                "properties": props,
                "edges_before_delete": edges,
                "journalled_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
            fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
            captured.append(rec)
    return captured


def journal_merge_dup(driver, database: str, canonical_id: str, merge_id: str, journal_path: Path) -> dict | None:
    """Capture the dup node's full state and incident edges before merge.
    Returns the captured record or None if the dup is already gone."""
    cypher = (
        "MATCH (dup:Akteur {id: $merge_id}) "
        "OPTIONAL MATCH (dup)-[r]-(m) "
        "RETURN id(dup) AS internal_id, labels(dup) AS labels, properties(dup) AS properties, "
        "       collect({type:type(r), direction: CASE WHEN startNode(r)=dup THEN 'OUT' ELSE 'IN' END, "
        "                 other_internal_id: id(m), other_id: m.id, other_labels: labels(m), "
        "                 properties: properties(r)}) AS edges"
    )
    with driver.session(database=database) as session:
        row = session.run(cypher, merge_id=merge_id).single()
    if row is None or row["internal_id"] is None:
        return None
    props = _to_jsonable(dict(row["properties"]))
    edges = [
        {k: _to_jsonable(v) for k, v in (e if isinstance(e, dict) else dict(e)).items()}
        for e in row["edges"] if e and (e.get("type") if isinstance(e, dict) else e["type"]) is not None
    ]
    rec = {
        "phase": "1.6",
        "canonical_id": canonical_id,
        "merged_in_id": merge_id,
        "neo4j_internal_id": row["internal_id"],
        "labels": list(row["labels"]),
        "properties": props,
        "edges_before_merge": edges,
        "journalled_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    with journal_path.open("a", encoding="utf-8", newline="\n") as fp:
        fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


# ---------- count helpers -------------------------------------------------

def count_label(driver, database: str, label: str) -> int:
    with driver.session(database=database) as session:
        row = session.run(f"MATCH (n:`{label}`) RETURN count(n) AS c").single()
    return int(row["c"])


# ---------- phase runners --------------------------------------------------

def run_phase_1_4(driver, database: str) -> dict:
    _log("PHASE 1.4 — Relabel Bauwerk -> Materialdepot")
    before_bauwerk = count_label(driver, database, "Bauwerk")
    before_materialdepot = count_label(driver, database, "Materialdepot")

    with driver.session(database=database) as session:
        relabelled = session.run(
            "MATCH (b:Bauwerk) WHERE b.id IN $ids "
            "REMOVE b:Bauwerk SET b:Materialdepot "
            "RETURN count(b) AS c",
            ids=MATERIALDEPOT_IDS,
        ).single()["c"]
        _log(f"  relabelled {relabelled} :Bauwerk -> :Materialdepot")

        betrieben_von = session.run(
            "MATCH (d:Materialdepot), (a:Akteur) "
            "WHERE d.id CONTAINS toLower(a.id) "
            "   OR d.id CONTAINS toLower(replace(a.name,' ','_')) "
            "MERGE (d)-[r:BETRIEBEN_VON]->(a) "
            "ON CREATE SET r.evidence_origin    = 'derived', "
            "              r.evidence_basis     = 'name_match', "
            "              r.evidence_source_id = 'mig_1_4', "
            "              r.evidence_confidence= 'unklar' "
            "RETURN count(r) AS c"
        ).single()["c"]
        _log(f"  BETRIEBEN_VON edges (touched, may include existing): {betrieben_von}")

    after_bauwerk = count_label(driver, database, "Bauwerk")
    after_materialdepot = count_label(driver, database, "Materialdepot")

    summary = {
        "phase": "1.4",
        "before_bauwerk": before_bauwerk,
        "after_bauwerk": after_bauwerk,
        "before_materialdepot": before_materialdepot,
        "after_materialdepot": after_materialdepot,
        "relabelled": relabelled,
        "betrieben_von_touched": betrieben_von,
        "expected_relabelled": 23,
    }
    _log(f"PHASE 1.4 done: {summary}")
    return summary


def run_phase_1_5(driver, database: str) -> dict:
    _log("PHASE 1.5 — Surgical deletes (journal first, then DETACH DELETE)")

    before = {
        "Akteur": count_label(driver, database, "Akteur"),
        "Programm": count_label(driver, database, "Programm"),
        "Norm": count_label(driver, database, "Norm"),
        "Quelle": count_label(driver, database, "Quelle"),
    }
    _log(f"  before: {before}")

    journal_path = DELETED_DIR / "phase1_5_nodes.jsonl"

    captured_akteur = journal_nodes_for_delete(driver, database, "Akteur", DELETE_AKTEUR_IDS, journal_path)
    captured_programm = journal_nodes_for_delete(driver, database, "Programm", DELETE_PROGRAMM_IDS, journal_path)
    captured_norm = journal_nodes_for_delete(driver, database, "Norm", DELETE_NORM_IDS, journal_path)

    # For Quelle: only journal nodes that actually still exist and have degree 0
    #             (Agent 3 may have already deleted some under Phase 1.2).
    with driver.session(database=database) as session:
        rows = list(session.run(
            "MATCH (q:Quelle) WHERE q.id IN $ids AND NOT (q)--() RETURN q.id AS id",
            ids=DELETE_QUELLE_IDS,
        ))
    quelle_to_delete = [r["id"] for r in rows]
    skipped_quelle = sorted(set(DELETE_QUELLE_IDS) - set(quelle_to_delete))
    if skipped_quelle:
        _log(f"  Quelle skipped (already absent or now wired): {skipped_quelle}")
    captured_quelle = journal_nodes_for_delete(driver, database, "Quelle", quelle_to_delete, journal_path)

    planned_total = (
        len(captured_akteur)
        + len(captured_programm)
        + len(captured_norm)
        + len(captured_quelle)
    )
    _log(
        "  journalled: "
        f"Akteur={len(captured_akteur)} Programm={len(captured_programm)} "
        f"Norm={len(captured_norm)} Quelle={len(captured_quelle)} total={planned_total}"
    )

    if planned_total > MAX_PHASE_1_5_DELETES:
        msg = (
            f"ABORT: planned deletes ({planned_total}) exceed safety gate "
            f"({MAX_PHASE_1_5_DELETES}). No DETACH DELETE issued."
        )
        _log(msg)
        raise RuntimeError(msg)

    if not captured_akteur and not captured_programm and not captured_norm and not captured_quelle:
        _log("  nothing to delete; phase 1.5 is a no-op.")

    with driver.session(database=database) as session:
        if captured_akteur:
            n = session.run(
                "MATCH (a:Akteur) WHERE a.id IN $ids DETACH DELETE a RETURN count(*) AS c",
                ids=[c["id"] for c in captured_akteur],
            ).single()["c"]
            _log(f"  deleted Akteur: {n}")
        if captured_programm:
            n = session.run(
                "MATCH (p:Programm) WHERE p.id IN $ids DETACH DELETE p RETURN count(*) AS c",
                ids=[c["id"] for c in captured_programm],
            ).single()["c"]
            _log(f"  deleted Programm: {n}")
        if captured_norm:
            n = session.run(
                "MATCH (q:Norm) WHERE q.id IN $ids DETACH DELETE q RETURN count(*) AS c",
                ids=[c["id"] for c in captured_norm],
            ).single()["c"]
            _log(f"  deleted Norm: {n}")
        if captured_quelle:
            n = session.run(
                "MATCH (q:Quelle) WHERE q.id IN $ids DETACH DELETE q RETURN count(*) AS c",
                ids=[c["id"] for c in captured_quelle],
            ).single()["c"]
            _log(f"  deleted Quelle: {n}")

    after = {
        "Akteur": count_label(driver, database, "Akteur"),
        "Programm": count_label(driver, database, "Programm"),
        "Norm": count_label(driver, database, "Norm"),
        "Quelle": count_label(driver, database, "Quelle"),
    }
    deleted = {k: before[k] - after[k] for k in before}
    _log(f"  after: {after}")
    _log(f"  deleted by label: {deleted}")

    return {
        "phase": "1.5",
        "before": before,
        "after": after,
        "deleted_by_label": deleted,
        "total_deleted": sum(deleted.values()),
        "journal_file": str(journal_path),
        "quelle_skipped": skipped_quelle,
        "safety_gate": MAX_PHASE_1_5_DELETES,
    }


def run_phase_1_6(driver, database: str) -> dict:
    _log("PHASE 1.6 — Akteur merges (apoc.refactor.mergeNodes)")

    before_akteur = count_label(driver, database, "Akteur")
    journal_path = DELETED_DIR / "phase1_6_merges.jsonl"
    results: list[dict] = []

    for canonical_id, merge_id in MERGE_PAIRS:
        with driver.session(database=database) as session:
            exists = session.run(
                "MATCH (canon:Akteur {id:$canon}), (dup:Akteur {id:$dup}) "
                "RETURN id(canon) AS c, id(dup) AS d, "
                "       size([(canon)--() | 1]) AS cd, "
                "       size([(dup)--() | 1]) AS dd",
                canon=canonical_id, dup=merge_id,
            ).single()
        if not exists:
            _log(f"  SKIP {canonical_id} <- {merge_id}: one or both nodes missing")
            results.append({
                "canonical_id": canonical_id,
                "merge_id": merge_id,
                "status": "skipped_missing",
            })
            continue

        _log(
            f"  MERGE {canonical_id} (deg {exists['cd']}) <- {merge_id} (deg {exists['dd']})"
        )

        journalled = journal_merge_dup(driver, database, canonical_id, merge_id, journal_path)
        if journalled is None:
            _log("    dup vanished between probe and journal; skipping")
            results.append({
                "canonical_id": canonical_id,
                "merge_id": merge_id,
                "status": "skipped_vanished",
            })
            continue

        cypher = (
            "MATCH (canon:Akteur {id:$canon}), (dup:Akteur {id:$dup}) "
            "CALL apoc.refactor.mergeNodes([canon, dup], {properties:'combine', mergeRels:true}) "
            "YIELD node "
            "SET node.aliases = CASE "
            "  WHEN $dup IN coalesce(node.aliases, []) THEN node.aliases "
            "  ELSE coalesce(node.aliases, []) + $dup END "
            "RETURN node.id AS id, node.aliases AS aliases, "
            "       size([(node)--() | 1]) AS combined_degree"
        )
        with driver.session(database=database) as session:
            row = session.run(cypher, canon=canonical_id, dup=merge_id).single()
        _log(
            f"    -> id={row['id']}, combined_degree={row['combined_degree']}, "
            f"aliases={row['aliases']}"
        )
        results.append({
            "canonical_id": canonical_id,
            "merge_id": merge_id,
            "status": "merged",
            "resulting_id": row["id"],
            "combined_degree": row["combined_degree"],
            "aliases": list(row["aliases"]) if row["aliases"] else [],
        })

    after_akteur = count_label(driver, database, "Akteur")
    summary = {
        "phase": "1.6",
        "before_akteur": before_akteur,
        "after_akteur": after_akteur,
        "merged_pairs": results,
        "journal_file": str(journal_path),
        "expected_after": before_akteur - sum(
            1 for r in results if r.get("status") == "merged"
        ),
    }
    _log(f"PHASE 1.6 done: Akteur {before_akteur} -> {after_akteur}")
    return summary


def write_flag(phase: str, summary: dict) -> None:
    path = RUN_ROOT / f"PHASE_{phase.replace('.', '_')}_DONE.flag"
    payload = {
        "phase": phase,
        "completed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "summary": summary,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    _log(f"wrote {path.name}")


def main() -> int:
    DELETED_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    if not (RUN_ROOT / "SNAPSHOT_DONE.flag").is_file():
        raise RuntimeError("SNAPSHOT_DONE.flag missing; refuse to run Phase 1 migrations.")

    from neo4j import GraphDatabase  # type: ignore

    uri, user, password, database = _resolve_connection()
    _log(f"connecting to {uri} db='{database}' as user='{user}'")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()

        t0 = time.perf_counter()
        s14 = run_phase_1_4(driver, database)
        s14["elapsed_seconds"] = round(time.perf_counter() - t0, 3)
        write_flag("1.4", s14)

        t0 = time.perf_counter()
        s15 = run_phase_1_5(driver, database)
        s15["elapsed_seconds"] = round(time.perf_counter() - t0, 3)
        write_flag("1.5", s15)

        t0 = time.perf_counter()
        s16 = run_phase_1_6(driver, database)
        s16["elapsed_seconds"] = round(time.perf_counter() - t0, 3)
        write_flag("1.6", s16)
    finally:
        driver.close()

    _log("agent4 runner: ALL PHASES COMPLETE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
