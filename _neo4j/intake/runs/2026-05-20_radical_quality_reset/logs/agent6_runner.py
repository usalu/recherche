"""Agent 6 — Wave-2 runner for Phase 2.4 + 2.7.

Phases:
  2.4  Projekt property collapse (year/area/cost/co2/reuse, counters→BG)
  2.7  Three-bucket panel cleanup for Projekt / Bauteilgruppe / Bauwerk /
       Materialdepot / Quelle / Akteur
       + Quelle.external_sources → :ZITIERT_QUELLE migration (60 Quellen)
       + Akteur.raw_role_evidence rollup from BETEILIGT_AN.rolle_text
       + Edge source pollution → canonical 5-field shape (partial)

Boundaries respected:
  - Does NOT run Phase 2.1 (Status merges) or 2.2 (WiederverwendungsArt)
    — those belong to Agent 5.
  - Does NOT promote inferred edges (Phase 3) or wire ZITIERT_QUELLE beyond
    the external_sources migration listed in this run.

Each migration runs inside its own write transaction. Pre/post counts are
captured against `mit-bestand` and journalled to `logs/agent6_*`. Done
flags are written at the run root.

Idempotency: every step re-checks live state before acting; running the
script twice produces no extra mutations and re-issues the flags.
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
RUN_ROOT = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "runs"
    / "2026-05-20_radical_quality_reset"
)
LOG_DIR = RUN_ROOT / "logs"
DEL_DIR = RUN_ROOT / "deleted"
REPORTS_DIR = RUN_ROOT / "reports"

PROGRESS_LOG = LOG_DIR / "agent6_progress.log"
RESULT_JSON = LOG_DIR / "agent6_result.json"
FLAG_2_4 = RUN_ROOT / "PHASE_2_4_DONE.flag"
FLAG_2_7 = RUN_ROOT / "PHASE_2_7_DONE.flag"
EXT_SRC_JOURNAL = DEL_DIR / "phase2_7_external_sources.jsonl"
ARCHIVE_PREVIEW = LOG_DIR / "agent6_archive_preview.json"


# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

# Year priority: jahr_fertigstellung > fertigstellung_jahr > jahr_eroeffnung > jahr > baujahr
YEAR_KEYS = [
    "jahr_fertigstellung",
    "fertigstellung_jahr",
    "jahr_beginn",
    "jahr",
    "jahr_fertigstellung_geplant",
    "jahr_eroeffnung",
    "fertigstellung_geplant_jahr",
    "jahr_start",
    "bau_jahr_von",
    "jahr_fertigstellung_max",
    "baujahr",
    "baujahr_von",
    "entwurfsjahr",
]
YEAR_PRIORITY = [
    "jahr_fertigstellung",
    "fertigstellung_jahr",
    "jahr_eroeffnung",
    "jahr",
    "baujahr",
]

AREA_KEYS = [
    "flaeche_m2",
    "flaeche_m2_min",
    "flaeche_m2_max",
    "bgf_m2",
    "flaeche_m2_alternative",
    "nutzflaeche_m2",
    "grundstueck_m2",
    "flaeche_sqft_min",
    "flaeche_sqft_max",
]
# hoehe_m / breite_m are NOT areas; they stay in _archive (Phase 2.7).

COST_KEYS = [
    "baukosten_eur",
    "kosten_eur",
    "kostenreduktion_prozent",
]
COST_UNIT = {
    "baukosten_eur": "EUR",
    "kosten_eur": "EUR",
    "kostenreduktion_prozent": "%",
}

CO2_KEYS = [
    "co2_einsparung_t",
    "co2_reduktion_prozent",
    "co2_reduktion_pct",
    "co2_einsparung_t_min",
    "co2_einsparung_t_max",
    "abfall_vermieden_t",
    "transportdistanz_km",
]
CO2_UNIT = {
    "co2_einsparung_t": "t",
    "co2_reduktion_prozent": "%",
    "co2_reduktion_pct": "%",
    "co2_einsparung_t_min": "t",
    "co2_einsparung_t_max": "t",
    "abfall_vermieden_t": "t",
    "transportdistanz_km": "km",
}

REUSE_KEYS = [
    "reuse_anteil_prozent",
    "reuse_anteil_volume",
    "material_passport",
]
REUSE_UNIT = {
    "reuse_anteil_prozent": "%",
    "reuse_anteil_volume": "m3",
    "material_passport": None,
}

# (counter_key_on_projekt, list_of_bg_name_substrings (lowercased))
# Conservative: only counters whose noun is unambiguously a BG name token.
COUNTER_TO_BG_PATTERNS: list[tuple[str, list[str]]] = [
    ("ursprungs_deckenplatten_anzahl", ["deckenplatte", "slab", "precast"]),
    ("reuse_deckenplatten_anzahl", ["deckenplatte", "slab", "precast"]),
    ("ursprungs_innenwandplatten_anzahl", ["innenwand", "wandplatte", "wall panel"]),
    ("reuse_wandplatten_anzahl", ["wandplatte", "wall panel", "wand"]),
    ("wiederverwendete_fertigteile_anzahl", ["fertigteil", "precast"]),
    ("fenster_anzahl", ["fenster", "window"]),
    ("fensterrahmen_anzahl", ["fensterrahmen", "window frame"]),
    ("holztueren_anzahl", ["holztuer", "wood door", "tür"]),
    ("leuchten_anzahl", ["leuchte", "luminaire", "light"]),
    ("stahltraeger_anzahl", ["stahltraeger", "steel beam", "i-beam", "steel profile"]),
    ("anzahl_stuetzen", ["stuetze", "column"]),
    ("anzahl_schalter", ["schalter", "switch"]),
    ("pv_paneele_anzahl", ["pv", "photovoltaic", "solar panel"]),
    ("led_light_tubes_anzahl", ["led", "light tube"]),
    ("teppichfliesen_anzahl", ["teppich", "carpet"]),
    ("granitfliesen_anzahl", ["granit"]),
    ("demontierte_bodenelemente_anzahl", ["boden", "floor"]),
    ("demontierte_fassadenelemente_anzahl", ["fassade", "facade"]),
    ("hcs_anzahl", ["hohlkoerper", "hollow core", "hcs"]),
    ("anzahl_reuse_slabs", ["slab", "deckenplatte"]),
    ("reuse_hohlkoerperdecken_anzahl", ["hohlkoerper", "hollow core"]),
    ("hohlkoerperdecken_anzahl", ["hohlkoerper", "hollow core"]),
]

# Panel keys per label (the only properties allowed to remain on the node;
# everything else is moved to ._archive).
PANEL_KEYS = {
    "Projekt": {
        "id",
        "name",
        "name_full",
        "quality_tier",
        "year_completed",
        "raw_year_fields",
        "area_m2_gross",
        "area_m2_range_min",
        "area_m2_range_max",
        "bewertung",
        "projektstatus_text",
        "nutzung_text",
        "node_role",
        "cost_facts",
        "reuse_share_facts",
        "co2_facts",
        "source_scope",
        "_archive",
    },
    "Bauteilgruppe": {
        "id",
        "name",
        "name_full",
        "reuse_status",
        "primary_material_id",
        "primary_bauteiltyp_id",
        "menge_t",
        "menge_stueck",
        "menge_m2",
        "menge_kg",
        "menge_m",
        "menge_unbekannt",
        "neue_funktion",
        "alte_funktion",
        "tragend",
        "raeumlich",
        "huelle",
        "technisch",
        "donor_unknown",
        "donor_resolution_status",
        "direct_reuse_relevant",
        "menge_source",
        "menge_original_key",
        "source_scope",
        "_archive",
    },
    "Bauwerk": {
        "id",
        "name",
        "name_full",
        "baujahr",
        "jahr_errichtet",
        "era_unknown",
        "bauwerkstatus",
        "nutzung_text",
        "schutzstatus_text",
        "flaeche_m2",
        "land",
        "is_material_depot",
        "source_scope",
        "_archive",
    },
    "Materialdepot": {
        "id",
        "name",
        "name_full",
        "baujahr",
        "jahr_errichtet",
        "era_unknown",
        "bauwerkstatus",
        "nutzung_text",
        "schutzstatus_text",
        "flaeche_m2",
        "land",
        "is_material_depot",
        "source_scope",
        "_archive",
    },
    "Quelle": {
        "id",
        "name",
        "quelltyp",
        "url",
        "source_file",
        "access_date",
        "title",
        "source_scope",
        "_archive",
    },
    "Akteur": {
        "id",
        "name",
        "name_full",
        "land",
        "stadt",
        "website",
        "aliases",
        "raw_role_evidence",
        "source_scope",
        "_archive",
    },
}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _log(line: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    msg = f"[{stamp}] {line}"
    # avoid cp1252 crashes on Windows consoles by replacing un-encodables
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        print(msg.encode(enc, errors="replace").decode(enc), flush=True)
    PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with PROGRESS_LOG.open("a", encoding="utf-8") as fp:
        fp.write(msg + "\n")


def _resolve_connection() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise RuntimeError("Neo4j connection missing.")
    if database != "mit-bestand":
        _log(f"WARN: overriding NEO4J_DATABASE='{database}' to 'mit-bestand'")
        database = "mit-bestand"
    return uri, user, password, database


URL_RE = re.compile(r"(https?://[^\s)>\]]+)", re.IGNORECASE)


def extract_url(raw: str) -> str | None:
    if not isinstance(raw, str):
        return None
    m = URL_RE.search(raw)
    if not m:
        return None
    url = m.group(1).rstrip(".,;:")
    return url


SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify_url(url: str) -> str:
    """Stable id from a URL — host + slugified path, trimmed to ~120 chars."""
    s = url.lower()
    s = re.sub(r"^https?://", "", s)
    s = re.sub(r"^www\.", "", s)
    s = SLUG_RE.sub("_", s).strip("_")
    if len(s) > 120:
        # keep last segment to retain distinctness across same-host links
        head = s[:60]
        tail = s[-55:]
        s = f"{head}__{tail}"
    return f"q_ext_{s}"


def extract_title(raw: str, url: str | None) -> str:
    if not isinstance(raw, str):
        return ""
    text = raw
    if url:
        text = text.replace(url, "")
    # drop leading citation marker like "[S1]", "**S1:**", "1." etc.
    text = re.sub(r"^\s*(\[?\*{0,2}S?\d+[\]:.]?\*{0,2})\s*[:\-—–]?\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip(" -–—:")
    return text[:240]


# --------------------------------------------------------------------------
# Pre/post snapshot helpers
# --------------------------------------------------------------------------

def snapshot_state(session) -> dict[str, Any]:
    out: dict[str, Any] = {}
    out["total_nodes"] = session.run(
        "MATCH (n) RETURN count(n) AS c"
    ).single()["c"]
    out["total_rels"] = session.run(
        "MATCH ()-[r]->() RETURN count(r) AS c"
    ).single()["c"]

    label_state: dict[str, dict[str, Any]] = {}
    for label in [
        "Projekt",
        "Bauteilgruppe",
        "Bauwerk",
        "Materialdepot",
        "Quelle",
        "Akteur",
    ]:
        nc = session.run(
            f"MATCH (n:{label}) RETURN count(n) AS c"
        ).single()["c"]
        if nc == 0:
            label_state[label] = {"node_count": 0, "distinct_keys": 0, "key_pairs": 0}
            continue
        rec = session.run(
            f"""
            MATCH (n:{label})
            UNWIND keys(n) AS k
            WITH k, count(*) AS c
            RETURN count(DISTINCT k) AS distinct_keys, sum(c) AS total_pairs
            """
        ).single()
        max_keys = session.run(
            f"""
            MATCH (n:{label})
            WITH size(keys(n)) AS nk
            RETURN max(nk) AS maxk, avg(nk) AS avgk
            """
        ).single()
        label_state[label] = {
            "node_count": nc,
            "distinct_keys": rec["distinct_keys"],
            "key_pairs": rec["total_pairs"],
            "max_keys_per_node": max_keys["maxk"],
            "avg_keys_per_node": float(max_keys["avgk"] or 0),
        }
    out["label_state"] = label_state

    out["projekt_year_completed_filled"] = session.run(
        "MATCH (p:Projekt) WHERE p.year_completed IS NOT NULL RETURN count(p) AS c"
    ).single()["c"]
    out["projekt_area_m2_gross_filled"] = session.run(
        "MATCH (p:Projekt) WHERE p.area_m2_gross IS NOT NULL RETURN count(p) AS c"
    ).single()["c"]
    out["projekt_cost_facts_filled"] = session.run(
        "MATCH (p:Projekt) WHERE size(coalesce(p.cost_facts,[])) > 0 RETURN count(p) AS c"
    ).single()["c"]
    out["projekt_co2_facts_filled"] = session.run(
        "MATCH (p:Projekt) WHERE size(coalesce(p.co2_facts,[])) > 0 RETURN count(p) AS c"
    ).single()["c"]
    out["projekt_reuse_share_facts_filled"] = session.run(
        "MATCH (p:Projekt) WHERE size(coalesce(p.reuse_share_facts,[])) > 0 RETURN count(p) AS c"
    ).single()["c"]
    out["projekt_archive_filled"] = session.run(
        "MATCH (p:Projekt) WHERE p._archive IS NOT NULL RETURN count(p) AS c"
    ).single()["c"]
    out["bg_archive_filled"] = session.run(
        "MATCH (bg:Bauteilgruppe) WHERE bg._archive IS NOT NULL RETURN count(bg) AS c"
    ).single()["c"]
    out["bauwerk_archive_filled"] = session.run(
        "MATCH (b:Bauwerk) WHERE b._archive IS NOT NULL RETURN count(b) AS c"
    ).single()["c"]
    out["materialdepot_archive_filled"] = session.run(
        "MATCH (b:Materialdepot) WHERE b._archive IS NOT NULL RETURN count(b) AS c"
    ).single()["c"]
    out["quelle_archive_filled"] = session.run(
        "MATCH (q:Quelle) WHERE q._archive IS NOT NULL RETURN count(q) AS c"
    ).single()["c"]
    out["akteur_archive_filled"] = session.run(
        "MATCH (a:Akteur) WHERE a._archive IS NOT NULL RETURN count(a) AS c"
    ).single()["c"]
    out["quelle_external_sources_count"] = session.run(
        "MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) AS c"
    ).single()["c"]
    out["akteur_raw_role_evidence_count"] = session.run(
        "MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL "
        "AND size(a.raw_role_evidence) > 0 RETURN count(a) AS c"
    ).single()["c"]
    out["zitiert_quelle_count"] = session.run(
        "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS c"
    ).single()["c"]
    out["polluted_edges_with_origin_null"] = session.run(
        "MATCH ()-[r]->() "
        "WHERE (r.source IS NOT NULL OR r.evidence IS NOT NULL "
        "  OR r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL) "
        "  AND r.evidence_origin IS NULL "
        "RETURN count(r) AS c"
    ).single()["c"]
    out["polluted_edges_total"] = session.run(
        "MATCH ()-[r]->() "
        "WHERE r.source IS NOT NULL OR r.evidence IS NOT NULL "
        "   OR r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL "
        "RETURN count(r) AS c"
    ).single()["c"]
    out["bg_with_menge_source_mig_2_4"] = session.run(
        "MATCH (bg:Bauteilgruppe) WHERE bg.menge_source = 'projekt_counter_migration_mig_2_4' "
        "RETURN count(bg) AS c"
    ).single()["c"]
    return out


# --------------------------------------------------------------------------
# PHASE 2.4
# --------------------------------------------------------------------------

def run_phase_2_4(driver, database: str) -> dict[str, Any]:
    _log("PHASE 2.4 — Projekt property collapse — START")
    res: dict[str, Any] = {}

    with driver.session(database=database) as session:
        # Read all Projekt nodes + relevant properties up-front.
        projekt_rows = list(session.run(
            """
            MATCH (p:Projekt)
            RETURN p.id AS id, properties(p) AS props
            """
        ))
        _log(f"  loaded {len(projekt_rows)} :Projekt nodes")

        # Build per-node mutation payload.
        mutations: list[dict[str, Any]] = []
        for row in projekt_rows:
            pid = row["id"]
            props = dict(row["props"] or {})

            present_year = {k: props[k] for k in YEAR_KEYS if k in props and props[k] is not None}
            year_completed = None
            for k in YEAR_PRIORITY:
                if k in present_year:
                    year_completed = present_year[k]
                    break
            raw_year_json = json.dumps(present_year, default=str, ensure_ascii=False) if present_year else None

            present_area = {k: props[k] for k in AREA_KEYS if k in props and props[k] is not None}
            area_gross = (
                props.get("flaeche_m2")
                if props.get("flaeche_m2") is not None
                else (
                    props.get("bgf_m2")
                    if props.get("bgf_m2") is not None
                    else props.get("nutzflaeche_m2")
                )
            )
            area_min = props.get("flaeche_m2_min")
            area_max = props.get("flaeche_m2_max")
            sqft_min = props.get("flaeche_sqft_min")
            sqft_max = props.get("flaeche_sqft_max")

            def build_facts(keys: list[str], unit_map: dict[str, str | None]) -> list[str]:
                facts: list[str] = []
                for k in keys:
                    v = props.get(k)
                    if v is None:
                        continue
                    facts.append(json.dumps({
                        "basis": k,
                        "value": v,
                        "unit": unit_map.get(k),
                        "source_id": None,
                    }, default=str, ensure_ascii=False))
                return facts

            cost_facts = build_facts(COST_KEYS, COST_UNIT)
            co2_facts = build_facts(CO2_KEYS, CO2_UNIT)
            reuse_facts = build_facts(REUSE_KEYS, REUSE_UNIT)

            present_cost = [k for k in COST_KEYS if k in props and props[k] is not None]
            present_co2 = [k for k in CO2_KEYS if k in props and props[k] is not None]
            present_reuse = [k for k in REUSE_KEYS if k in props and props[k] is not None]

            mutations.append({
                "id": pid,
                "year_completed": year_completed,
                "raw_year_fields": raw_year_json,
                "year_keys_to_remove": list(present_year.keys()),
                "area_m2_gross": area_gross,
                "area_m2_range_min": area_min,
                "area_m2_range_max": area_max,
                "area_sqft_min": sqft_min,
                "area_sqft_max": sqft_max,
                "area_keys_to_remove": list(present_area.keys()),
                "cost_facts": cost_facts,
                "cost_keys_to_remove": present_cost,
                "co2_facts": co2_facts,
                "co2_keys_to_remove": present_co2,
                "reuse_share_facts": reuse_facts,
                "reuse_keys_to_remove": present_reuse,
            })

        # Apply mutations one transaction per node (atomic per Projekt;
        # safer than UNWIND batches when keys-to-remove are per-node lists).
        # Idempotency: if no source keys are present for this Projekt, the
        # collapse was already applied in a previous run -> skip mutation
        # entirely (avoids zeroing out a previously-set year_completed).
        applied = 0
        skipped_already = 0
        for mu in mutations:
            keys_to_remove = (
                mu["year_keys_to_remove"]
                + mu["area_keys_to_remove"]
                + mu["cost_keys_to_remove"]
                + mu["co2_keys_to_remove"]
                + mu["reuse_keys_to_remove"]
            )
            if not keys_to_remove:
                skipped_already += 1
                continue
            with session.begin_transaction() as tx:
                tx.run(
                    """
                    MATCH (p:Projekt {id: $id})
                    SET p.year_completed     = $year_completed,
                        p.raw_year_fields    = $raw_year_fields,
                        p.area_m2_gross      = $area_m2_gross,
                        p.area_m2_range_min  = $area_m2_range_min,
                        p.area_m2_range_max  = $area_m2_range_max,
                        p.area_sqft_min      = $area_sqft_min,
                        p.area_sqft_max      = $area_sqft_max,
                        p.cost_facts         = $cost_facts,
                        p.co2_facts          = $co2_facts,
                        p.reuse_share_facts  = $reuse_share_facts
                    """,
                    {
                        "id": mu["id"],
                        "year_completed": mu["year_completed"],
                        "raw_year_fields": mu["raw_year_fields"],
                        "area_m2_gross": mu["area_m2_gross"],
                        "area_m2_range_min": mu["area_m2_range_min"],
                        "area_m2_range_max": mu["area_m2_range_max"],
                        "area_sqft_min": mu["area_sqft_min"],
                        "area_sqft_max": mu["area_sqft_max"],
                        "cost_facts": mu["cost_facts"],
                        "co2_facts": mu["co2_facts"],
                        "reuse_share_facts": mu["reuse_share_facts"],
                    },
                )
                tx.run(
                    """
                    MATCH (p:Projekt {id: $id})
                    CALL apoc.create.removeProperties(p, $keys) YIELD node
                    RETURN node
                    """,
                    {"id": mu["id"], "keys": keys_to_remove},
                )
                tx.commit()
            applied += 1
        _log(f"  applied collapse to {applied} :Projekt nodes "
             f"({skipped_already} already collapsed, idempotent skip)")
        res["projekt_collapse_applied"] = applied
        res["projekt_collapse_skipped_idempotent"] = skipped_already

        # Phase 2.4.d — counter→BG migrations
        counter_results: list[dict[str, Any]] = []
        successful_keys_by_pid: dict[str, set[str]] = {}
        for counter_key, substrings in COUNTER_TO_BG_PATTERNS:
            sub_filters = " OR ".join(
                [f"toLower(coalesce(bg.name,'')) CONTAINS $s{i}" for i in range(len(substrings))]
            )
            params = {f"s{i}": s.lower() for i, s in enumerate(substrings)}
            params["ck"] = counter_key
            with session.begin_transaction() as tx:
                rows = list(tx.run(
                    f"""
                    MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
                    WHERE p[$ck] IS NOT NULL
                      AND ({sub_filters})
                    WITH p, bg, p[$ck] AS cnt
                    SET bg.menge_stueck       = coalesce(bg.menge_stueck, cnt),
                        bg.menge_source       = coalesce(bg.menge_source, 'projekt_counter_migration_mig_2_4'),
                        bg.menge_original_key = coalesce(bg.menge_original_key, $ck)
                    RETURN p.id AS pid, bg.id AS bgid, cnt
                    """,
                    params,
                ))
                tx.commit()
            for r in rows:
                counter_results.append({
                    "counter_key": counter_key,
                    "projekt_id": r["pid"],
                    "bg_id": r["bgid"],
                    "menge_stueck": r["cnt"],
                })
                successful_keys_by_pid.setdefault(r["pid"], set()).add(counter_key)
        _log(f"  counter->BG: {len(counter_results)} migrations across "
             f"{len(successful_keys_by_pid)} projekte")

        # Remove counter keys from :Projekt only where a BG match succeeded
        # (failed ones survive for Phase 2.7 archive).
        removed_count = 0
        for pid, keys in successful_keys_by_pid.items():
            with session.begin_transaction() as tx:
                tx.run(
                    """
                    MATCH (p:Projekt {id: $id})
                    CALL apoc.create.removeProperties(p, $keys) YIELD node
                    RETURN node
                    """,
                    {"id": pid, "keys": list(keys)},
                )
                tx.commit()
            removed_count += len(keys)
        _log(f"  counter cleanup: removed {removed_count} keys from Projekt nodes")
        res["counter_migrations"] = counter_results
        res["counter_keys_removed_from_projekt"] = removed_count

    _log("PHASE 2.4 — done")
    return res


# --------------------------------------------------------------------------
# PHASE 2.7
# --------------------------------------------------------------------------

def _ensure_dirs() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    DEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _archive_label(session, label: str) -> dict[str, Any]:
    """Move every non-panel property on :label to ._archive (JSON string).

    Two-pass implementation to stay clear of `CALL { } IN TRANSACTIONS`
    (which requires auto-commit context):
      1. Read every (node_id, archive_keys, archive_json) tuple.
      2. For each, run a small write transaction that SETs ._archive and
         REMOVEs the archive_keys.
    Idempotency: a node whose only "non-panel" key is `_archive` itself is
    skipped (already cleaned).
    """
    panel = sorted(PANEL_KEYS[label])
    rows = list(session.run(
        f"""
        MATCH (n:{label})
        WITH n,
             [k IN keys(n) WHERE NOT k IN $panel] AS archive_keys
        WHERE size(archive_keys) > 0
        WITH n, archive_keys,
             apoc.map.fromPairs([k IN archive_keys | [k, n[k]]]) AS amap
        RETURN n.id AS id,
               archive_keys AS archive_keys,
               apoc.convert.toJson(amap) AS archive_json
        """,
        {"panel": panel},
    ))
    _log(f"  archive {label}: panel={len(panel)} keys, {len(rows)} nodes to clean")
    processed = 0
    for r in rows:
        nid = r["id"]
        akeys = r["archive_keys"]
        ajson = r["archive_json"]
        # If the existing _archive carries content and we're being called
        # twice, merge: parse existing, merge with new payload, set merged.
        existing = session.run(
            f"MATCH (n:{label} {{id: $id}}) RETURN n._archive AS a",
            {"id": nid},
        ).single()
        merged_json = ajson
        if existing and existing["a"]:
            try:
                old = json.loads(existing["a"])
                new = json.loads(ajson)
                if isinstance(old, dict) and isinstance(new, dict):
                    old.update(new)
                    merged_json = json.dumps(old, ensure_ascii=False, default=str)
            except (json.JSONDecodeError, TypeError):
                merged_json = ajson
        with session.begin_transaction() as tx:
            tx.run(
                f"""
                MATCH (n:{label} {{id: $id}})
                SET n._archive = $aj
                """,
                {"id": nid, "aj": merged_json},
            )
            tx.run(
                f"""
                MATCH (n:{label} {{id: $id}})
                CALL apoc.create.removeProperties(n, $keys) YIELD node
                RETURN node
                """,
                {"id": nid, "keys": akeys},
            )
            tx.commit()
        processed += 1
    return {"label": label, "nodes_processed": processed}


def run_phase_2_7(driver, database: str) -> dict[str, Any]:
    _log("PHASE 2.7 — three-bucket panel cleanup — START")
    res: dict[str, Any] = {}

    # --- 2.7.b external_sources → :ZITIERT_QUELLE (run BEFORE label
    # archive so the source :Quelle still carries `external_sources`)
    with driver.session(database=database) as session:
        ext_rows = list(session.run(
            """
            MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL
            RETURN q.id AS id, q.external_sources AS extsrc
            """
        ))
        _log(f"  external_sources migration: {len(ext_rows)} source :Quelle")

        EXT_SRC_JOURNAL.parent.mkdir(parents=True, exist_ok=True)
        EXT_SRC_JOURNAL.write_text("", encoding="utf-8")

        ext_total_links = 0
        ext_total_targets = 0
        with EXT_SRC_JOURNAL.open("a", encoding="utf-8") as journal:
            for src_row in ext_rows:
                src_id = src_row["id"]
                entries = src_row["extsrc"] or []
                migrated_links = []
                for raw in entries:
                    url = extract_url(raw)
                    if not url:
                        migrated_links.append({
                            "raw": raw,
                            "url": None,
                            "target_id": None,
                            "skipped_reason": "no_url_in_string",
                        })
                        continue
                    target_id = slugify_url(url)
                    title = extract_title(raw, url)
                    with session.begin_transaction() as tx:
                        tx.run(
                            """
                            MERGE (target:Quelle {id: $target_id})
                            ON CREATE SET target.url = $url,
                                          target.quelltyp = 'external_link',
                                          target.name = $title,
                                          target.source_scope = 'mig_2_7_external_sources',
                                          target._created_by  = 'mig_2_7'
                            WITH target
                            MATCH (src:Quelle {id: $src_id})
                            MERGE (src)-[r:ZITIERT_QUELLE]->(target)
                            ON CREATE SET r.evidence_origin     = 'derived',
                                          r.evidence_basis      = 'external_sources_array',
                                          r.evidence_source_id  = 'mig_2_7',
                                          r.evidence_confidence = 'unklar',
                                          r.evidence_excerpt    = $raw
                            """,
                            {
                                "target_id": target_id,
                                "url": url,
                                "title": title,
                                "src_id": src_id,
                                "raw": raw,
                            },
                        )
                        tx.commit()
                    migrated_links.append({
                        "raw": raw,
                        "url": url,
                        "target_id": target_id,
                    })
                    ext_total_links += 1
                # Distinct targets across this source
                ext_total_targets += len({m["target_id"] for m in migrated_links if m["target_id"]})

                # Now remove external_sources from the source :Quelle
                with session.begin_transaction() as tx:
                    tx.run(
                        """
                        MATCH (src:Quelle {id: $src_id})
                        REMOVE src.external_sources
                        """,
                        {"src_id": src_id},
                    )
                    tx.commit()

                journal.write(json.dumps({
                    "source_quelle_id": src_id,
                    "migrated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "raw_entries": entries,
                    "migrated_links": migrated_links,
                }, ensure_ascii=False) + "\n")

        _log(f"  external_sources migration: {ext_total_links} ZITIERT_QUELLE links created")
        res["external_sources_links_created"] = ext_total_links

    # --- 2.7.c Akteur.raw_role_evidence rollup
    #
    # Defensive: Agent 5 (Phase 2.3) is the canonical owner of this rollup
    # and it strips :BETEILIGT_AN.rolle_text immediately after populating
    # :Akteur.raw_role_evidence with entries shaped like
    # `"<rolle_text> @ <target_id>"`. If we observe that Agent 5 has
    # already populated the field on >= 100 Akteurs, we SKIP our own
    # rollup entirely to avoid clobbering the richer entries.
    #
    # If Agent 5 has not run yet, we fall back to a coalesce that only
    # writes when our computed list is non-empty (so a re-run after
    # Agent 5 also leaves Agent 5's content intact).
    with driver.session(database=database) as session:
        already = session.run(
            "MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL "
            "AND size(a.raw_role_evidence) > 0 RETURN count(a) AS c"
        ).single()["c"]
        if already >= 100:
            res["akteur_role_rollup_applied"] = 0
            res["akteur_role_rollup_skipped_owned_by_agent_5"] = already
            _log(f"  akteur raw_role_evidence rollup: SKIPPED "
                 f"(Agent 5 already populated {already} Akteurs)")
        else:
            rec = session.run(
                """
                MATCH (a:Akteur)
                OPTIONAL MATCH (a)-[r:BETEILIGT_AN]->()
                WITH a, [x IN collect(DISTINCT r.rolle_text) WHERE x IS NOT NULL] AS roles
                WHERE size(roles) > 0
                SET a.raw_role_evidence = coalesce(a.raw_role_evidence, roles)
                RETURN count(a) AS c
                """
            ).single()
            res["akteur_role_rollup_applied"] = rec["c"]
            _log(f"  akteur raw_role_evidence rollup: {rec['c']} nodes touched "
                 f"(fallback path; Agent 5 had populated {already})")

    # --- 2.7.a Mark Materialdepot.is_material_depot = true
    with driver.session(database=database) as session:
        rec = session.run(
            """
            MATCH (b:Materialdepot)
            SET b.is_material_depot = true
            RETURN count(b) AS c
            """
        ).single()
        res["materialdepot_flag_set"] = rec["c"]
        _log(f"  is_material_depot=true on {rec['c']} :Materialdepot")

    # --- 2.7.d Edge source pollution → canonical 5-field shape
    with driver.session(database=database) as session:
        rec = session.run(
            """
            MATCH ()-[r]->()
            WHERE (r.source IS NOT NULL OR r.evidence IS NOT NULL
                   OR r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL)
              AND r.evidence_origin IS NULL
            WITH r,
                 coalesce(r.evidence_excerpt, r.source_excerpt, r.evidence) AS excerpt,
                 coalesce(r.evidence_source_id, r.source) AS src_id
            SET r.evidence_origin     = 'derived',
                r.evidence_basis      = coalesce(r.evidence_basis, 'legacy_migration'),
                r.evidence_source_id  = src_id,
                r.evidence_confidence = coalesce(r.evidence_confidence, 'unklar'),
                r.evidence_excerpt    = excerpt
            REMOVE r.source, r.evidence, r.source_excerpt, r.datenqualitaet
            RETURN count(r) AS c
            """
        ).single()
        res["edges_pollution_canonicalised"] = rec["c"]
        _log(f"  canonicalised {rec['c']} polluted edges (Agent 7 completes the rest)")

    # --- 2.7.a Three-bucket cleanup per label
    label_results: list[dict[str, Any]] = []
    with driver.session(database=database) as session:
        for label in ["Projekt", "Bauteilgruppe", "Bauwerk", "Materialdepot", "Quelle", "Akteur"]:
            label_results.append(_archive_label(session, label))
    res["label_archive_results"] = label_results

    _log("PHASE 2.7 — done")
    return res


# --------------------------------------------------------------------------
# Main orchestration
# --------------------------------------------------------------------------

def write_flag(flag_path: Path, phase: str, before: dict, after: dict, payload: dict) -> None:
    body = {
        "phase": phase,
        "completed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "before": before,
        "after": after,
        "payload": payload,
    }
    flag_path.write_text(json.dumps(body, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    _log(f"wrote done flag: {flag_path.name}")


def main() -> int:
    _ensure_dirs()
    from neo4j import GraphDatabase  # type: ignore

    uri, user, password, database = _resolve_connection()
    _log(f"connecting to {uri} db='{database}' as user='{user}'")
    started = time.perf_counter()
    started_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()

        with driver.session(database=database) as session:
            before = snapshot_state(session)
        _log(f"BEFORE snapshot: nodes={before['total_nodes']} rels={before['total_rels']} "
             f"projekt_keys={before['label_state']['Projekt']['distinct_keys']} "
             f"bg_keys={before['label_state']['Bauteilgruppe']['distinct_keys']}")

        # Idempotency check
        projekt_collapsed_already = (
            before["projekt_year_completed_filled"] >= 1
            and before["projekt_archive_filled"] >= 1
        )
        ext_sources_done = before["quelle_external_sources_count"] == 0
        if projekt_collapsed_already and ext_sources_done and before["polluted_edges_with_origin_null"] == 0:
            _log("All Phase 2.4 + 2.7 markers already present — re-issuing flags only.")
            with driver.session(database=database) as session:
                after = snapshot_state(session)
            write_flag(FLAG_2_4, "2.4", before, after, {"skipped": True})
            write_flag(FLAG_2_7, "2.7", before, after, {"skipped": True})
            return 0

        # PHASE 2.4
        payload_24 = run_phase_2_4(driver, database)
        with driver.session(database=database) as session:
            mid = snapshot_state(session)

        # PHASE 2.7
        payload_27 = run_phase_2_7(driver, database)
        with driver.session(database=database) as session:
            after = snapshot_state(session)

        # ------------ Postcondition asserts ------------
        # 2.4 - at least 38 projects should have area_m2_gross (33 flaeche_m2 +
        # 3 bgf_m2 + 1 nutzflaeche_m2 with some overlap).
        assert after["projekt_area_m2_gross_filled"] >= 33, (
            f"expected area_m2_gross >= 33, got {after['projekt_area_m2_gross_filled']}"
        )
        # plan target: ~50 year_completed (31 jahr_fertigstellung + 7 fertigstellung_jahr + 2 jahr_eroeffnung + 5 jahr + 1 baujahr, with overlap)
        assert after["projekt_year_completed_filled"] >= 40, (
            f"expected year_completed >= 40, got {after['projekt_year_completed_filled']}"
        )
        # 2.7 - panel cleanup must have written _archive to most nodes that
        # had non-panel keys; at minimum every label that exists ends with
        # max keys per node <= 30 (panel cap is ~24).
        for label in ["Projekt", "Bauteilgruppe", "Bauwerk", "Materialdepot", "Quelle", "Akteur"]:
            ls = after["label_state"][label]
            if ls["node_count"] == 0:
                continue
            assert ls["max_keys_per_node"] is None or ls["max_keys_per_node"] <= 30, (
                f"{label}.max_keys_per_node={ls['max_keys_per_node']} (>30); panel cleanup failed"
            )
        # external_sources fully migrated
        assert after["quelle_external_sources_count"] == 0, (
            f"expected 0 :Quelle.external_sources remaining, got "
            f"{after['quelle_external_sources_count']}"
        )
        # edge source pollution with origin null reduced to 0
        assert after["polluted_edges_with_origin_null"] == 0, (
            f"expected 0 polluted edges with origin NULL, got "
            f"{after['polluted_edges_with_origin_null']}"
        )

        # Persist preview of a sample _archive payload
        with driver.session(database=database) as session:
            samples = list(session.run(
                """
                MATCH (p:Projekt) WHERE p._archive IS NOT NULL
                RETURN p.id AS id, p._archive AS archive
                ORDER BY size(p._archive) DESC LIMIT 3
                """
            ))
        ARCHIVE_PREVIEW.write_text(
            json.dumps([{"id": r["id"], "archive_preview": r["archive"][:1500] + ("…" if len(r["archive"]) > 1500 else "")} for r in samples], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # Done flags + JSON result
        write_flag(FLAG_2_4, "2.4", before, mid, payload_24)
        write_flag(FLAG_2_7, "2.7", mid, after, payload_27)

        elapsed = time.perf_counter() - started
        result = {
            "started_at": started_iso,
            "finished_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "elapsed_seconds": elapsed,
            "before": before,
            "after_phase_2_4": mid,
            "after_phase_2_7": after,
            "phase_2_4_payload": payload_24,
            "phase_2_7_payload": payload_27,
        }
        RESULT_JSON.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )
        _log(
            f"DONE  nodes {before['total_nodes']}->{after['total_nodes']}  "
            f"rels {before['total_rels']}->{after['total_rels']}  elapsed={elapsed:.2f}s"
        )
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
