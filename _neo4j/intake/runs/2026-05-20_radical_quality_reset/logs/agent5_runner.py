"""Wave-2 migration runner for Phases 2.1, 2.2, 2.3, 2.5 (Agent 5).

Applies the four Cypher migration files from
``migrations/mig_2_{1,2,3,5}_*.cypher`` against the ``mit-bestand`` database.

Design (mirrors ``migrate_helper_p1_2_3.py`` from Agent 3):

  - Each migration file runs inside a single ``execute_write`` transaction —
    every statement commits together or the whole file rolls back.
  - Pre-flight snapshot + post-condition assertion per phase.
  - Idempotent skip when the post-state already matches expectations.
  - Pre-merge / pre-delete journaling to ``deleted/phase2_*.jsonl`` so the
    32 node casualties (2 status + 1 role + 28 demoted) are fully replayable.
  - Per-phase DONE flag at ``logs/PHASE_2_X_DONE.flag`` plus a consolidated
    progress log at ``logs/agent5_progress.log`` and a JSON snapshot of
    counters at ``logs/phase2_result.json``.
"""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-20_radical_quality_reset"
MIG_DIR = RUN_ROOT / "migrations"
LOG_DIR = RUN_ROOT / "logs"
DEL_DIR = RUN_ROOT / "deleted"
PROGRESS_LOG = LOG_DIR / "agent5_progress.log"
RESULT_JSON = LOG_DIR / "phase2_result.json"

MIG_FILES = {
    "2.1": MIG_DIR / "mig_2_1_status_consolidation.cypher",
    "2.2": MIG_DIR / "mig_2_2_wva_facet.cypher",
    "2.3": MIG_DIR / "mig_2_3_role_unification.cypher",
    "2.5": MIG_DIR / "mig_2_5_label_demotions.cypher",
}

FLAGS = {
    "2.1": LOG_DIR / "PHASE_2_1_DONE.flag",
    "2.2": LOG_DIR / "PHASE_2_2_DONE.flag",
    "2.3": LOG_DIR / "PHASE_2_3_DONE.flag",
    "2.5": LOG_DIR / "PHASE_2_5_DONE.flag",
}

JOURNAL_2_1 = DEL_DIR / "phase2_1_status_merges.jsonl"
JOURNAL_2_3 = DEL_DIR / "phase2_3_role_merges.jsonl"
JOURNAL_2_5_NODES = DEL_DIR / "phase2_5_demoted_nodes.jsonl"
JOURNAL_2_5_TOOLS = DEL_DIR / "phase2_5_tool_relabels.jsonl"


def _log(line: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    msg = f"[{stamp}] {line}"
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(msg.encode("utf-8", errors="replace") + b"\n")
        sys.stdout.flush()
    with PROGRESS_LOG.open("a", encoding="utf-8") as fp:
        fp.write(msg + "\n")


def _resolve_connection() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise RuntimeError("Neo4j connection settings missing (NEO4J_URI/USERNAME/PASSWORD).")
    if database != "mit-bestand":
        _log(f"WARN: configured NEO4J_DATABASE='{database}' — overriding to 'mit-bestand'.")
        database = "mit-bestand"
    return uri, user, password, database


_COMMENT_RE = re.compile(r"//[^\n]*")


def parse_cypher_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    stripped = _COMMENT_RE.sub("", text)
    stmts = [s.strip() for s in stripped.split(";")]
    return [s for s in stmts if s]


def _to_jsonable(value: Any) -> Any:
    from neo4j.time import Date, DateTime, Duration, Time  # type: ignore
    from neo4j.spatial import Point  # type: ignore
    from neo4j.graph import Node, Relationship, Path as NPath  # type: ignore

    if isinstance(value, (Date, DateTime, Time)):
        return value.iso_format()
    if isinstance(value, Duration):
        return str(value)
    if isinstance(value, Point):
        return {"srid": value.srid, "coordinates": list(value)}
    if isinstance(value, Node):
        return {
            "_element_id": value.element_id,
            "_labels": list(value.labels),
            **{k: _to_jsonable(v) for k, v in dict(value).items()},
        }
    if isinstance(value, Relationship):
        return {
            "_element_id": value.element_id,
            "_type": value.type,
            "_start": value.start_node.element_id if value.start_node else None,
            "_end": value.end_node.element_id if value.end_node else None,
            **{k: _to_jsonable(v) for k, v in dict(value).items()},
        }
    if isinstance(value, NPath):
        return {"nodes": [_to_jsonable(n) for n in value.nodes],
                "relationships": [_to_jsonable(r) for r in value.relationships]}
    if isinstance(value, dict):
        return {k: _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, (bytes, bytearray)):
        return value.decode("utf-8", errors="replace")
    return value


def run_migration(driver, database: str, label: str, path: Path) -> list[dict]:
    _log(f"--- {label}: parsing {path.name}")
    stmts = parse_cypher_file(path)
    _log(f"--- {label}: {len(stmts)} statements parsed")

    results: list[dict] = []
    with driver.session(database=database) as session:
        def _work(tx):
            collected = []
            for idx, stmt in enumerate(stmts, start=1):
                preview = " ".join(stmt.split())[:160]
                _log(f"    [{label} #{idx}/{len(stmts)}] {preview}")
                res = tx.run(stmt)
                rows = [{k: _to_jsonable(v) for k, v in r.items()} for r in res]
                summary = res.consume()
                ctrs = summary.counters
                ctr_dict = {
                    "nodes_created": ctrs.nodes_created,
                    "nodes_deleted": ctrs.nodes_deleted,
                    "relationships_created": ctrs.relationships_created,
                    "relationships_deleted": ctrs.relationships_deleted,
                    "labels_added": ctrs.labels_added,
                    "labels_removed": ctrs.labels_removed,
                    "properties_set": ctrs.properties_set,
                }
                _log(f"        rows={len(rows)}  counters={ctr_dict}")
                if rows:
                    _log(f"        first_row={json.dumps(rows[0], ensure_ascii=False)[:400]}")
                collected.append({
                    "statement_index": idx,
                    "statement_preview": preview,
                    "rows": rows,
                    "counters": ctr_dict,
                })
            return collected
        results = session.execute_write(_work)
    return results


# ---------------------------------------------------------------------------
# Snapshots
# ---------------------------------------------------------------------------


def snapshot_2_1(session) -> dict:
    def _q(c):
        return list(session.run(c))

    status_rows = _q(
        "MATCH (s:Status) RETURN s.id AS id, s.kind AS kind ORDER BY id"
    )
    return {
        "status_total": len(status_rows),
        "status_with_kind": sum(1 for r in status_rows if r["kind"] is not None),
        "status_ids_present": sorted([r["id"] for r in status_rows]),
        "status_gebaut_exists": sum(1 for r in status_rows if r["id"] == "status_gebaut"),
        "status_wettbewerb_exists": sum(1 for r in status_rows if r["id"] == "status_wettbewerb"),
        "bauwerk_with_bauwerkstatus_prop": _q(
            "MATCH (b:Bauwerk) WHERE b.bauwerkstatus IS NOT NULL RETURN count(b) AS c"
        )[0]["c"],
        "bauwerk_with_status_text_prop": _q(
            "MATCH (b:Bauwerk) WHERE b.status_text IS NOT NULL RETURN count(b) AS c"
        )[0]["c"],
        "bg_with_any_counts_as": _q(
            "MATCH (bg:Bauteilgruppe) WHERE "
            "bg.counts_as_direct_reuse IS NOT NULL OR "
            "bg.counts_as_bestandserhalt IS NOT NULL OR "
            "bg.counts_as_recycling IS NOT NULL OR "
            "bg.counts_as_remanufacturing IS NOT NULL OR "
            "bg.counts_as_surplus IS NOT NULL "
            "RETURN count(bg) AS c"
        )[0]["c"],
        "hat_status_total": _q("MATCH ()-[r:HAT_STATUS]->() RETURN count(r) AS c")[0]["c"],
    }


def snapshot_2_2(session) -> dict:
    def _q(c):
        return list(session.run(c))
    rows = _q("MATCH (n:WiederverwendungsArt) RETURN n.id AS id, n.facet AS facet")
    return {
        "wva_total": len(rows),
        "wva_with_facet": sum(1 for r in rows if r["facet"] is not None),
        "wva_missing_facet_ids": sorted([r["id"] for r in rows if r["facet"] is None]),
        "hat_wva_total": _q("MATCH ()-[r:HAT_WIEDERVERWENDUNGSART]->() RETURN count(r) AS c")[0]["c"],
    }


def snapshot_2_3(session) -> dict:
    def _q(c):
        return list(session.run(c))
    return {
        "beteiligt_an_with_rolle_text": _q(
            "MATCH ()-[r:BETEILIGT_AN]->() WHERE r.rolle_text IS NOT NULL RETURN count(r) AS c"
        )[0]["c"],
        "akteur_with_raw_role_evidence": _q(
            "MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL RETURN count(a) AS c"
        )[0]["c"],
        "akteurrolle_ar_reuse_beratung_exists": _q(
            "MATCH (n:Akteurrolle {id:'ar_reuse_beratung'}) RETURN count(n) AS c"
        )[0]["c"],
        "akteurrolle_ar_reuse_zirk_indeg": _q(
            "MATCH ()-[r:HAT_AKTEURROLLE]->(n:Akteurrolle {id:'ar_reuse_zirkularitaetsberatung'}) "
            "RETURN count(r) AS c"
        )[0]["c"],
        "akteurrolle_total": _q("MATCH (n:Akteurrolle) RETURN count(n) AS c")[0]["c"],
    }


def snapshot_2_5(session) -> dict:
    def _q(c):
        return list(session.run(c))
    return {
        "layer_count":            _q("MATCH (n:Layer)                          RETURN count(n) AS c")[0]["c"],
        "lzm_count":              _q("MATCH (n:LebenszyklusModul)              RETURN count(n) AS c")[0]["c"],
        "rb_count":               _q("MATCH (n:RechtlicheBedingung)            RETURN count(n) AS c")[0]["c"],
        "zert_count":             _q("MATCH (n:ZertifizierungBewertungssystem) RETURN count(n) AS c")[0]["c"],
        "tool_count":             _q("MATCH (n:Tool)                           RETURN count(n) AS c")[0]["c"],
        "software_count":         _q("MATCH (n:Software)                       RETURN count(n) AS c")[0]["c"],
        "software_with_kind":     _q("MATCH (n:Software) WHERE n.kind IS NOT NULL RETURN count(n) AS c")[0]["c"],
        "bauteiltyp_with_brand_layer": _q(
            "MATCH (b:Bauteiltyp) WHERE b.brand_layer IS NOT NULL RETURN count(b) AS c"
        )[0]["c"],
        "projekt_with_lca_module_scope": _q(
            "MATCH (p:Projekt) WHERE p.lca_module_scope IS NOT NULL RETURN count(p) AS c"
        )[0]["c"],
        "projekt_with_certifications": _q(
            "MATCH (p:Projekt) WHERE p.certifications IS NOT NULL RETURN count(p) AS c"
        )[0]["c"],
        "sources_with_legal_conditions": _q(
            "MATCH (n) WHERE n.legal_conditions IS NOT NULL RETURN count(n) AS c"
        )[0]["c"],
        "teilt_layer_edges": _q("MATCH ()-[r:TEILT_LAYER]->() RETURN count(r) AS c")[0]["c"],
        "berechnet_nach_modul_edges": _q("MATCH ()-[r:BERECHNET_NACH_MODUL]->() RETURN count(r) AS c")[0]["c"],
        "methodengrundlage_norm_edges": _q("MATCH ()-[r:METHODENGRUNDLAGE_NORM]->() RETURN count(r) AS c")[0]["c"],
        "hat_rechtliche_bedingung_edges": _q("MATCH ()-[r:HAT_RECHTLICHE_BEDINGUNG]->() RETURN count(r) AS c")[0]["c"],
        "gilt_in_land_from_rb_edges": _q(
            "MATCH (:RechtlicheBedingung)-[r:GILT_IN_LAND]->() RETURN count(r) AS c"
        )[0]["c"],
        "hat_zertifizierung_edges": _q("MATCH ()-[r:HAT_ZERTIFIZIERUNG]->() RETURN count(r) AS c")[0]["c"],
        "nutzt_tool_edges": _q("MATCH ()-[r:NUTZT_TOOL]->() RETURN count(r) AS c")[0]["c"],
        "nutzt_software_edges": _q("MATCH ()-[r:NUTZT_SOFTWARE]->() RETURN count(r) AS c")[0]["c"],
        "referenziert_norm_edges": _q("MATCH ()-[r:REFERENZIERT_NORM]->() RETURN count(r) AS c")[0]["c"],
        "referenziert_norm_lca_derived": _q(
            "MATCH ()-[r:REFERENZIERT_NORM]->() WHERE r.evidence_basis = 'lca_module_demote' "
            "RETURN count(r) AS c"
        )[0]["c"],
        "total_nodes": _q("MATCH (n) RETURN count(n) AS c")[0]["c"],
        "total_rels":  _q("MATCH ()-[r]->() RETURN count(r) AS c")[0]["c"],
    }


# ---------------------------------------------------------------------------
# Journals (pre-state capture for reversibility)
# ---------------------------------------------------------------------------


def _node_with_edges_payload(session, where_clause: str, params: dict | None = None) -> list[dict]:
    """Return a list of dicts each containing the node's full property set and
    every incident edge as ``{type, direction, other_id, props}``."""
    cypher = (
        f"MATCH (n) WHERE {where_clause} "
        "OPTIONAL MATCH (n)-[ro]->(t) "
        "WITH n, collect({direction:'out', type:type(ro), "
        "                 other_element_id: elementId(t), other_labels: labels(t), "
        "                 other_id: coalesce(t.id, t.name), props: properties(ro)}) AS out_edges "
        "OPTIONAL MATCH (n)<-[ri]-(s) "
        "RETURN n, labels(n) AS labels, properties(n) AS props, out_edges, "
        "       collect({direction:'in', type:type(ri), "
        "                other_element_id: elementId(s), other_labels: labels(s), "
        "                other_id: coalesce(s.id, s.name), props: properties(ri)}) AS in_edges"
    )
    rows = list(session.run(cypher, params or {}))
    out = []
    for r in rows:
        rec = {
            "labels": list(r["labels"]),
            "properties": _to_jsonable(dict(r["props"])),
            "edges_before": [
                _to_jsonable(e) for e in (list(r["out_edges"]) + list(r["in_edges"]))
                if e.get("type") is not None
            ],
        }
        out.append(rec)
    return out


def journal_2_1(session) -> int:
    """Capture pre-merge state of Status duplicates (Gebaut, Wettbewerb)."""
    payload = _node_with_edges_payload(
        session,
        "(n:Status) AND n.id IN ['status_gebaut','status_wettbewerb']",
    )
    DEL_DIR.mkdir(parents=True, exist_ok=True)
    with JOURNAL_2_1.open("w", encoding="utf-8") as fp:
        for rec in payload:
            fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
    _log(f"journal 2.1 wrote {len(payload)} records -> {JOURNAL_2_1.name}")
    return len(payload)


def journal_2_3(session) -> int:
    payload = _node_with_edges_payload(
        session,
        "(n:Akteurrolle) AND n.id = 'ar_reuse_beratung'",
    )
    DEL_DIR.mkdir(parents=True, exist_ok=True)
    with JOURNAL_2_3.open("w", encoding="utf-8") as fp:
        for rec in payload:
            fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
    _log(f"journal 2.3 wrote {len(payload)} records -> {JOURNAL_2_3.name}")
    return len(payload)


def journal_2_5(session) -> tuple[int, int]:
    """Capture pre-state of every node about to be deleted or relabelled."""
    DEL_DIR.mkdir(parents=True, exist_ok=True)
    payload_demoted = _node_with_edges_payload(
        session,
        "(n:Layer OR n:LebenszyklusModul OR n:RechtlicheBedingung OR n:ZertifizierungBewertungssystem)",
    )
    with JOURNAL_2_5_NODES.open("w", encoding="utf-8") as fp:
        for rec in payload_demoted:
            fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
    _log(f"journal 2.5 wrote {len(payload_demoted)} demoted-node records -> {JOURNAL_2_5_NODES.name}")

    payload_tools = _node_with_edges_payload(session, "(n:Tool)")
    with JOURNAL_2_5_TOOLS.open("w", encoding="utf-8") as fp:
        for rec in payload_tools:
            fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
    _log(f"journal 2.5 wrote {len(payload_tools)} tool-relabel records -> {JOURNAL_2_5_TOOLS.name}")
    return len(payload_demoted), len(payload_tools)


# ---------------------------------------------------------------------------
# Per-phase orchestration
# ---------------------------------------------------------------------------


def write_done_flag(flag_path: Path, phase: str, before: dict, after: dict, extra: dict | None = None) -> None:
    body = {
        "phase": phase,
        "completed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "before": before,
        "after": after,
        "extra": extra or {},
    }
    flag_path.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
    _log(f"wrote done flag: {flag_path.name}")


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    DEL_DIR.mkdir(parents=True, exist_ok=True)

    from neo4j import GraphDatabase  # type: ignore

    uri, user, password, database = _resolve_connection()
    _log(f"connecting to {uri} db='{database}' as user='{user}'")

    overall_started = time.perf_counter()
    started_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    aggregate: dict = {"started_at": started_iso, "phases": {}}

    try:
        driver.verify_connectivity()

        # ============================================================
        # Phase 2.1 — Status consolidation
        # ============================================================
        with driver.session(database=database) as s:
            before_21 = snapshot_2_1(s)
        _log(f"PHASE 2.1 precheck: {json.dumps(before_21)}")
        applied_2_1 = (
            before_21["status_total"] == 9
            and before_21["status_with_kind"] == 9
            and before_21["status_gebaut_exists"] == 0
            and before_21["status_wettbewerb_exists"] == 0
            and before_21["bauwerk_with_bauwerkstatus_prop"] == 0
            and before_21["bauwerk_with_status_text_prop"] == 0
            and before_21["bg_with_any_counts_as"] == 0
        )
        if applied_2_1:
            _log("PHASE 2.1 already applied — skipping migration; re-issuing flag.")
            aggregate["phases"]["2.1"] = {"skipped": True, "reason": "already_applied"}
        else:
            assert before_21["status_total"] == 11, before_21
            assert before_21["status_gebaut_exists"] == 1, before_21
            assert before_21["status_wettbewerb_exists"] == 1, before_21
            with driver.session(database=database) as s:
                journaled = journal_2_1(s)
            r = run_migration(driver, database, "Phase 2.1", MIG_FILES["2.1"])
            aggregate["phases"]["2.1"] = {"skipped": False, "statements": r, "journaled_nodes": journaled}

        with driver.session(database=database) as s:
            after_21 = snapshot_2_1(s)
        _log(f"PHASE 2.1 postcheck: {json.dumps(after_21)}")
        assert after_21["status_total"] == 9, after_21
        assert after_21["status_with_kind"] == 9, after_21
        assert after_21["status_gebaut_exists"] == 0, after_21
        assert after_21["status_wettbewerb_exists"] == 0, after_21
        assert after_21["bauwerk_with_bauwerkstatus_prop"] == 0, after_21
        assert after_21["bauwerk_with_status_text_prop"] == 0, after_21
        assert after_21["bg_with_any_counts_as"] == 0, after_21
        hat_status_dedup = before_21["hat_status_total"] - after_21["hat_status_total"]
        if not applied_2_1:
            # mergeRels:true legitimately collapses duplicate (src, type, target)
            # pairs when the same source had HAT_STATUS edges to both
            # Realisiert+Gebaut (or Prototyp+Wettbewerb). Allow up to 20 such
            # collapses (observed: 3). Only enforce on a fresh apply -- after
            # downstream agents run, HAT_STATUS counts can move legitimately.
            assert hat_status_dedup >= 0, after_21
            assert hat_status_dedup <= 20, (
                f"HAT_STATUS lost {hat_status_dedup} edges from merge dedup (>20 unexpected): "
                f"{before_21['hat_status_total']} -> {after_21['hat_status_total']}"
            )
        write_done_flag(
            FLAGS["2.1"], "2.1", before_21, after_21,
            extra={"hat_status_dedup_collapsed": hat_status_dedup},
        )

        # ============================================================
        # Phase 2.2 — WVA facet
        # ============================================================
        with driver.session(database=database) as s:
            before_22 = snapshot_2_2(s)
        _log(f"PHASE 2.2 precheck: {json.dumps(before_22)}")
        applied_2_2 = (
            before_22["wva_total"] == 11
            and before_22["wva_with_facet"] == 11
        )
        if applied_2_2:
            _log("PHASE 2.2 already applied — skipping migration; re-issuing flag.")
            aggregate["phases"]["2.2"] = {"skipped": True, "reason": "already_applied"}
        else:
            assert before_22["wva_total"] == 11, before_22
            r = run_migration(driver, database, "Phase 2.2", MIG_FILES["2.2"])
            aggregate["phases"]["2.2"] = {"skipped": False, "statements": r}

        with driver.session(database=database) as s:
            after_22 = snapshot_2_2(s)
        _log(f"PHASE 2.2 postcheck: {json.dumps(after_22)}")
        assert after_22["wva_total"] == 11, after_22
        assert after_22["wva_with_facet"] == 11, after_22
        if not applied_2_2:
            # 2.2 is purely property-set -- no merges, no edge change expected.
            # Only enforce on a fresh apply; parallel agents can move HAT_WVA
            # counts (e.g. by adding/removing edges in their own scope).
            assert after_22["hat_wva_total"] == before_22["hat_wva_total"], (
                f"HAT_WIEDERVERWENDUNGSART edges changed: "
                f"{before_22['hat_wva_total']} -> {after_22['hat_wva_total']}"
            )
        write_done_flag(FLAGS["2.2"], "2.2", before_22, after_22)

        # ============================================================
        # Phase 2.3 — Role unification
        # ============================================================
        with driver.session(database=database) as s:
            before_23 = snapshot_2_3(s)
        _log(f"PHASE 2.3 precheck: {json.dumps(before_23)}")
        applied_2_3 = (
            before_23["beteiligt_an_with_rolle_text"] == 0
            and before_23["akteurrolle_ar_reuse_beratung_exists"] == 0
            and before_23["akteur_with_raw_role_evidence"] > 0
        )
        if applied_2_3:
            _log("PHASE 2.3 already applied — skipping migration; re-issuing flag.")
            aggregate["phases"]["2.3"] = {"skipped": True, "reason": "already_applied"}
        else:
            assert before_23["beteiligt_an_with_rolle_text"] > 0, before_23
            assert before_23["akteurrolle_ar_reuse_beratung_exists"] == 1, before_23
            with driver.session(database=database) as s:
                journaled = journal_2_3(s)
            r = run_migration(driver, database, "Phase 2.3", MIG_FILES["2.3"])
            aggregate["phases"]["2.3"] = {"skipped": False, "statements": r, "journaled_nodes": journaled}

        with driver.session(database=database) as s:
            after_23 = snapshot_2_3(s)
        _log(f"PHASE 2.3 postcheck: {json.dumps(after_23)}")
        assert after_23["beteiligt_an_with_rolle_text"] == 0, after_23
        assert after_23["akteur_with_raw_role_evidence"] > 0, after_23
        assert after_23["akteurrolle_ar_reuse_beratung_exists"] == 0, after_23
        if not applied_2_3:
            # Only assert the +2 indegree gain on a fresh apply; downstream
            # agents may legitimately re-audit ar_reuse_zirkularitaetsberatung
            # and drop edges (plan note in 2.3 — Phase 4b expects ~198 -> ~60).
            assert after_23["akteurrolle_ar_reuse_zirk_indeg"] >= before_23["akteurrolle_ar_reuse_zirk_indeg"], (
                f"indegree of ar_reuse_zirkularitaetsberatung shrank: "
                f"{before_23['akteurrolle_ar_reuse_zirk_indeg']} -> {after_23['akteurrolle_ar_reuse_zirk_indeg']}"
            )
        write_done_flag(FLAGS["2.3"], "2.3", before_23, after_23)

        # ============================================================
        # Phase 2.5 — Label demotions
        # ============================================================
        with driver.session(database=database) as s:
            before_25 = snapshot_2_5(s)
        _log(f"PHASE 2.5 precheck: {json.dumps(before_25)}")
        applied_2_5 = (
            before_25["layer_count"] == 0
            and before_25["lzm_count"] == 0
            and before_25["rb_count"] == 0
            and before_25["zert_count"] == 0
            and before_25["tool_count"] == 0
            and before_25["bauteiltyp_with_brand_layer"] > 0
            and before_25["software_with_kind"] > 0
            and before_25["nutzt_tool_edges"] == 0
        )
        if applied_2_5:
            _log("PHASE 2.5 already applied — skipping migration; re-issuing flag.")
            aggregate["phases"]["2.5"] = {"skipped": True, "reason": "already_applied"}
        else:
            assert before_25["layer_count"] == 6, before_25
            assert before_25["lzm_count"] == 5, before_25
            assert before_25["rb_count"] == 9, before_25
            assert before_25["zert_count"] == 8, before_25
            assert before_25["tool_count"] == 8, before_25
            with driver.session(database=database) as s:
                demoted_n, tool_n = journal_2_5(s)
            r = run_migration(driver, database, "Phase 2.5", MIG_FILES["2.5"])
            aggregate["phases"]["2.5"] = {
                "skipped": False,
                "statements": r,
                "journaled_demoted_nodes": demoted_n,
                "journaled_tool_nodes": tool_n,
            }

        with driver.session(database=database) as s:
            after_25 = snapshot_2_5(s)
        _log(f"PHASE 2.5 postcheck: {json.dumps(after_25)}")
        # Always-true assertions: the demoted labels must stay absent and the
        # rewired edge types must stay rewired, regardless of who else has
        # touched the graph since this phase originally ran.
        assert after_25["layer_count"] == 0, after_25
        assert after_25["lzm_count"] == 0, after_25
        assert after_25["rb_count"] == 0, after_25
        assert after_25["zert_count"] == 0, after_25
        assert after_25["tool_count"] == 0, after_25
        assert after_25["software_with_kind"] == after_25["software_count"], after_25
        assert after_25["nutzt_tool_edges"] == 0, after_25
        assert after_25["teilt_layer_edges"] == 0, after_25
        assert after_25["berechnet_nach_modul_edges"] == 0, after_25
        assert after_25["methodengrundlage_norm_edges"] == 0, after_25
        assert after_25["hat_rechtliche_bedingung_edges"] == 0, after_25
        assert after_25["hat_zertifizierung_edges"] == 0, after_25
        if not applied_2_5:
            # These property-population checks only describe the immediate
            # post-migration state. Downstream agents (Agent 6 / Phase 2.4
            # property collapse) legitimately move lca_module_scope,
            # certifications, legal_conditions into Projekt._archive.
            assert after_25["bauteiltyp_with_brand_layer"] >= 13, after_25
            assert after_25["projekt_with_lca_module_scope"] >= 1, after_25
            assert after_25["projekt_with_certifications"] >= 1, after_25
            assert after_25["nutzt_software_edges"] >= before_25["nutzt_software_edges"], after_25
            assert after_25["referenziert_norm_lca_derived"] >= 1, after_25
        write_done_flag(FLAGS["2.5"], "2.5", before_25, after_25)

        aggregate["finished_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        aggregate["elapsed_seconds"] = time.perf_counter() - overall_started
        aggregate["after_snapshots"] = {
            "2.1": after_21,
            "2.2": after_22,
            "2.3": after_23,
            "2.5": after_25,
        }
        aggregate["before_snapshots"] = {
            "2.1": before_21,
            "2.2": before_22,
            "2.3": before_23,
            "2.5": before_25,
        }
        RESULT_JSON.write_text(json.dumps(aggregate, ensure_ascii=False, indent=2), encoding="utf-8")
        _log(
            f"DONE  total elapsed={aggregate['elapsed_seconds']:.2f}s  "
            f"nodes {before_25['total_nodes']} -> {after_25['total_nodes']}  "
            f"rels {before_25['total_rels']} -> {after_25['total_rels']}"
        )

    finally:
        driver.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
