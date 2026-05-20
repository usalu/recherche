"""Agent 7 — Wave 3 runner for Phase 4.1 + 4.2.

Phases:
  4.1  Enforce canonical 5-field evidence shape on every claim edge.
       Hard rules:
         - evidence_origin='curated' requires non-null evidence_excerpt
         - evidence_confidence='bookkeeping' only legal with origin='derived'
         - evidence_excerpt may not contain 'propagated from'
         - no edge has NULL evidence_origin / basis / source_id / confidence
       Side-effects:
         - HAT_DEFEKT "propagated from …" excerpts moved to derivation_note,
           basis flipped to 'propagated', excerpt nulled.
         - HAT_MARKTMODELL legacy {source, evidence} keys removed after
           backfilling evidence_source_id from r.source.
         - Legacy {source_excerpt, datenqualitaet} keys removed if any.

  4.2  Rename relationship types:
         AUS_BAUWERK  → FROM_DONOR
         EINGEBAUT_IN → INTO_RECEIVER
       Uses apoc.refactor.rename.type (procedure presence verified at
       run time; the apoc list was captured in agent7_explore.json).

Boundaries respected:
  - Does NOT run Phase 4b (loader rewrite) or 4c (source-link backfill).
  - Does NOT touch Phase 3 (era / pollutant / decision shelf inference).
  - Does NOT touch ANCHORED_BY / HAT_MATCHINGQUALITAET / HAT_DEFEKT-BEFUND
    edges that already satisfy the canonical shape — they are simply
    not matched by the migration predicates.

Idempotency: every WRITE step is conditional on a not-yet-canonical
predicate; re-running yields zero writes and re-issues both flags.
"""

from __future__ import annotations

import json
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
REPORTS_DIR = RUN_ROOT / "reports"

PROGRESS_LOG = LOG_DIR / "agent7_progress.log"
RESULT_JSON = LOG_DIR / "agent7_result.json"
FLAG_4 = RUN_ROOT / "PHASE_4_DONE.flag"
FLAG_4_2 = RUN_ROOT / "PHASE_4_2_DONE.flag"

# Per-relationship evidence_basis defaults — keep in lockstep with the
# Cypher migration CASE block (see mig_4_1_canonical_evidence.cypher).
BASIS_DEFAULTS: dict[str, str] = {
    # BELEGT_IN edges that lack a Quelle id at creation time get
    # 'controlled_vocab' here; step 4_1_e backfills the id from the
    # destination :Quelle and step 4_1_f flips the basis to 'cell_citation'.
    "BELEGT_IN": "controlled_vocab",
    "BETEILIGT_AN": "controlled_vocab",
    "ASSOZIIERT_MIT_PROJEKT": "registry_stub",
    "AUS_BAUWERK": "controlled_vocab",
    "EINGEBAUT_IN": "controlled_vocab",
    "HAT_BAUTEILGRUPPE": "controlled_vocab",
    "HAT_HUERDE": "controlled_vocab",
    "HAT_AKTEURROLLE": "controlled_vocab",
    "REFERENZIERT_NORM": "standards_body",
}
BASIS_FALLBACK = "controlled_vocab"

# The 8 relationship types in the strict per-relationship enum group
# (plan §4.1):  cell_citation | registry_stub | propagated | controlled_vocab
ENUM_GROUP_CITATION = (
    "BELEGT_IN",
    "BETEILIGT_AN",
    "ASSOZIIERT_MIT_PROJEKT",
    "AUS_BAUWERK",     # pre-rename
    "FROM_DONOR",      # post-rename
    "EINGEBAUT_IN",    # pre-rename
    "INTO_RECEIVER",   # post-rename
    "HAT_BAUTEILGRUPPE",
    "HAT_HUERDE",
    "HAT_AKTEURROLLE",
)
ENUM_GROUP_CITATION_ALLOWED = {
    "cell_citation",
    "registry_stub",
    "propagated",
    "controlled_vocab",
}
# REFERENZIERT_NORM / APPLIES_IN / APPLIES_TO:
ENUM_GROUP_NORM = ("REFERENZIERT_NORM", "APPLIES_IN", "APPLIES_TO")
ENUM_GROUP_NORM_ALLOWED = {"research_file_row", "standards_body"}


def _log(line: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    msg = f"[{stamp}] {line}"
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


def _ensure_dirs() -> None:
    for d in (LOG_DIR, REPORTS_DIR):
        d.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Snapshots
# ---------------------------------------------------------------------------

EVIDENCE_FIELDS_SQL = """
MATCH ()-[r]->()
WITH r
RETURN
  count(r) AS total,
  sum(CASE WHEN r.evidence_origin IS NULL THEN 1 ELSE 0 END) AS missing_origin,
  sum(CASE WHEN r.evidence_basis IS NULL THEN 1 ELSE 0 END) AS missing_basis,
  sum(CASE WHEN NOT 'evidence_excerpt' IN keys(r) THEN 1 ELSE 0 END) AS missing_excerpt_key,
  sum(CASE WHEN r.evidence_source_id IS NULL THEN 1 ELSE 0 END) AS missing_source_id,
  sum(CASE WHEN r.evidence_confidence IS NULL THEN 1 ELSE 0 END) AS missing_confidence,
  sum(CASE WHEN r.source IS NOT NULL THEN 1 ELSE 0 END) AS legacy_source,
  sum(CASE WHEN r.evidence IS NOT NULL THEN 1 ELSE 0 END) AS legacy_evidence,
  sum(CASE WHEN r.source_excerpt IS NOT NULL THEN 1 ELSE 0 END) AS legacy_source_excerpt,
  sum(CASE WHEN r.datenqualitaet IS NOT NULL THEN 1 ELSE 0 END) AS legacy_datenqualitaet,
  sum(CASE WHEN r.evidence_origin='curated'
                AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
            THEN 1 ELSE 0 END) AS viol_curated_no_excerpt,
  sum(CASE WHEN r.evidence_confidence='bookkeeping'
                AND coalesce(r.evidence_origin,'') <> 'derived'
            THEN 1 ELSE 0 END) AS viol_bk_not_derived,
  sum(CASE WHEN r.evidence_excerpt IS NOT NULL
                AND toLower(r.evidence_excerpt) CONTAINS 'propagated from'
            THEN 1 ELSE 0 END) AS viol_excerpt_propagated
"""

RENAME_STATUS_SQL = """
CALL () {
  MATCH ()-[r:AUS_BAUWERK]->() RETURN 'AUS_BAUWERK' AS rt, count(r) AS c
  UNION ALL
  MATCH ()-[r:EINGEBAUT_IN]->() RETURN 'EINGEBAUT_IN' AS rt, count(r) AS c
  UNION ALL
  MATCH ()-[r:FROM_DONOR]->() RETURN 'FROM_DONOR' AS rt, count(r) AS c
  UNION ALL
  MATCH ()-[r:INTO_RECEIVER]->() RETURN 'INTO_RECEIVER' AS rt, count(r) AS c
}
RETURN rt, c
"""


def snapshot_state(session) -> dict[str, Any]:
    state: dict[str, Any] = {
        "total_nodes": session.run("MATCH (n) RETURN count(n) AS c").single()["c"],
        "total_rels": session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"],
    }
    state["evidence"] = dict(session.run(EVIDENCE_FIELDS_SQL).single())
    state["rename_status"] = {
        r["rt"]: r["c"] for r in session.run(RENAME_STATUS_SQL)
    }
    state["per_type"] = {
        r["t"]: r["c"]
        for r in session.run(
            "MATCH ()-[r]->() RETURN type(r) AS t, count(*) AS c ORDER BY t"
        )
    }
    return state


# ---------------------------------------------------------------------------
# Phase 4.1 steps
# ---------------------------------------------------------------------------

def step_4_1_a_propagated_excerpts(session) -> dict[str, int]:
    """Move 'propagated from' lineage notes from excerpt → derivation_note."""
    res = session.run(
        """
        MATCH ()-[r]->()
        WHERE r.evidence_excerpt IS NOT NULL
          AND toLower(r.evidence_excerpt) CONTAINS 'propagated from'
        WITH r
        SET r.derivation_note     = r.evidence_excerpt,
            r.evidence_basis      = 'propagated',
            r.evidence_excerpt    = NULL,
            r.evidence_origin     = coalesce(r.evidence_origin, 'derived'),
            r.evidence_source_id  = coalesce(r.evidence_source_id, 'mig_4_1'),
            r.evidence_confidence = coalesce(r.evidence_confidence, 'unklar')
        RETURN count(r) AS touched
        """
    ).single()
    return {"touched": res["touched"]}


def step_4_1_b_legacy_keys(session) -> dict[str, int]:
    """Strip legacy {source, evidence} after backfilling source_id."""
    res_se = session.run(
        """
        MATCH ()-[r]->()
        WHERE r.source IS NOT NULL OR r.evidence IS NOT NULL
        WITH r
        SET r.evidence_source_id  = coalesce(r.evidence_source_id, r.source, 'mig_4_1'),
            r.evidence_origin     = coalesce(r.evidence_origin, 'derived'),
            r.evidence_basis      = coalesce(r.evidence_basis, 'propagated'),
            r.evidence_confidence = coalesce(r.evidence_confidence, 'bookkeeping')
        REMOVE r.source, r.evidence
        RETURN count(r) AS touched
        """
    ).single()

    res_extra = session.run(
        """
        MATCH ()-[r]->()
        WHERE r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL
        WITH r
        SET r.evidence_excerpt = coalesce(r.evidence_excerpt, r.source_excerpt),
            r.evidence_confidence = coalesce(
                r.evidence_confidence,
                CASE r.datenqualitaet
                  WHEN 'belegt'           THEN 'belegt'
                  WHEN 'teilweise_belegt' THEN 'teilweise_belegt'
                  WHEN 'unklar'           THEN 'unklar'
                  WHEN 'inferiert'        THEN 'inferiert'
                  ELSE 'unklar'
                END
            )
        REMOVE r.source_excerpt, r.datenqualitaet
        RETURN count(r) AS touched
        """
    ).single()
    return {
        "source_evidence_stripped": res_se["touched"],
        "source_excerpt_datenq_stripped": res_extra["touched"],
    }


def step_4_1_c_canonical_backfill(session) -> dict[str, int]:
    """Apply canonical 5-field shape to every edge that has no origin yet."""
    cypher_basis_case = "\n".join(
        f"           WHEN '{t}' THEN '{b}'"
        for t, b in BASIS_DEFAULTS.items()
    )
    res = session.run(
        f"""
        MATCH ()-[r]->()
        WHERE r.evidence_origin IS NULL
        WITH r,
             CASE type(r)
{cypher_basis_case}
               ELSE '{BASIS_FALLBACK}'
             END AS basis_default
        SET r.evidence_origin     = 'derived',
            r.evidence_basis      = basis_default,
            r.evidence_source_id  = 'mig_4_1',
            r.evidence_confidence = 'unklar',
            r.evidence_excerpt    = CASE
              WHEN r.evidence_excerpt IS NULL THEN NULL
              WHEN toLower(r.evidence_excerpt) CONTAINS 'propagated from' THEN NULL
              ELSE r.evidence_excerpt
            END
        RETURN count(r) AS touched
        """
    ).single()

    # Make sure every edge has the evidence_excerpt KEY (even if NULL).
    res_key = session.run(
        """
        MATCH ()-[r]->()
        WHERE NOT 'evidence_excerpt' IN keys(r)
        SET r.evidence_excerpt = NULL
        RETURN count(r) AS touched
        """
    ).single()
    return {
        "canonical_filled": res["touched"],
        "excerpt_key_added": res_key["touched"],
    }


def step_4_1_d_audit(session) -> dict[str, int]:
    """Return zero-violation counts for the four hard rules."""
    rows = session.run(
        """
        MATCH ()-[r]->()
        RETURN
          sum(CASE WHEN r.evidence_origin='curated'
                        AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
                    THEN 1 ELSE 0 END) AS viol_curated_no_excerpt,
          sum(CASE WHEN r.evidence_confidence='bookkeeping'
                        AND coalesce(r.evidence_origin,'') <> 'derived'
                    THEN 1 ELSE 0 END) AS viol_bk_not_derived,
          sum(CASE WHEN r.evidence_excerpt IS NOT NULL
                        AND toLower(r.evidence_excerpt) CONTAINS 'propagated from'
                    THEN 1 ELSE 0 END) AS viol_excerpt_propagated,
          sum(CASE WHEN r.evidence_origin     IS NULL
                     OR r.evidence_basis      IS NULL
                     OR r.evidence_source_id  IS NULL
                     OR r.evidence_confidence IS NULL
                    THEN 1 ELSE 0 END) AS viol_missing_field
        """
    ).single()
    return dict(rows)


def step_4_1_d_enum_audit(session) -> dict[str, int]:
    """Check the per-relationship enum constraints.

    - Citation group (8 listed types): basis ∈ {cell_citation, registry_stub,
      propagated, controlled_vocab}.
    - REFERENZIERT_NORM / APPLIES_IN / APPLIES_TO: basis ∈ {research_file_row,
      standards_body}.

    Returns offending counts per type to surface any residual issues.
    """
    cit_rows = list(session.run(
        f"""
        MATCH ()-[r]->()
        WHERE type(r) IN {list(ENUM_GROUP_CITATION)}
          AND NOT r.evidence_basis IN {list(ENUM_GROUP_CITATION_ALLOWED)}
        RETURN type(r) AS rt, r.evidence_basis AS basis, count(*) AS c
        ORDER BY rt, basis
        """
    ))
    norm_rows = list(session.run(
        f"""
        MATCH ()-[r]->()
        WHERE type(r) IN {list(ENUM_GROUP_NORM)}
          AND NOT r.evidence_basis IN {list(ENUM_GROUP_NORM_ALLOWED)}
        RETURN type(r) AS rt, r.evidence_basis AS basis, count(*) AS c
        ORDER BY rt, basis
        """
    ))
    return {
        "citation_group_violations": [dict(r) for r in cit_rows],
        "norm_group_violations": [dict(r) for r in norm_rows],
        "total_citation_violations": sum(r["c"] for r in cit_rows),
        "total_norm_violations": sum(r["c"] for r in norm_rows),
    }


# ---------------------------------------------------------------------------
# Phase 4.2 steps
# ---------------------------------------------------------------------------

def step_4_2_rename(session, old_type: str, new_type: str) -> dict[str, Any]:
    rows = session.run(
        f"""
        MATCH ()-[r:`{old_type}`]->()
        WITH collect(r) AS rels
        CALL apoc.refactor.rename.type('{old_type}', '{new_type}', rels)
        YIELD batches, total, timeTaken, committedOperations,
              failedOperations, failedBatches, retries, errorMessages
        RETURN batches, total, timeTaken, committedOperations,
               failedOperations, failedBatches, retries, errorMessages
        """
    ).single()
    return {} if rows is None else dict(rows)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def write_flag(flag_path: Path, phase: str, before: dict, after: dict, payload: dict) -> None:
    body = {
        "phase": phase,
        "completed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "before": before,
        "after": after,
        "payload": payload,
    }
    flag_path.write_text(
        json.dumps(body, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    _log(f"wrote done flag: {flag_path.name}")


def run_phase_4_1(driver, database: str) -> dict[str, Any]:
    _log("PHASE 4.1 — canonical 5-field evidence shape")
    payload: dict[str, Any] = {}
    with driver.session(database=database) as session:
        with session.begin_transaction() as tx:
            payload["a_propagated_excerpts"] = tx.run(
                """
                MATCH ()-[r]->()
                WHERE r.evidence_excerpt IS NOT NULL
                  AND toLower(r.evidence_excerpt) CONTAINS 'propagated from'
                WITH r
                SET r.derivation_note     = r.evidence_excerpt,
                    r.evidence_basis      = 'propagated',
                    r.evidence_excerpt    = NULL,
                    r.evidence_origin     = coalesce(r.evidence_origin, 'derived'),
                    r.evidence_source_id  = coalesce(r.evidence_source_id, 'mig_4_1'),
                    r.evidence_confidence = coalesce(r.evidence_confidence, 'unklar')
                RETURN count(r) AS touched
                """
            ).single()["touched"]
            payload["b_source_evidence_stripped"] = tx.run(
                """
                MATCH ()-[r]->()
                WHERE r.source IS NOT NULL OR r.evidence IS NOT NULL
                WITH r
                SET r.evidence_source_id  = coalesce(r.evidence_source_id, r.source, 'mig_4_1'),
                    r.evidence_origin     = coalesce(r.evidence_origin, 'derived'),
                    r.evidence_basis      = coalesce(r.evidence_basis, 'propagated'),
                    r.evidence_confidence = coalesce(r.evidence_confidence, 'bookkeeping')
                REMOVE r.source, r.evidence
                RETURN count(r) AS touched
                """
            ).single()["touched"]
            payload["b_extra_legacy_stripped"] = tx.run(
                """
                MATCH ()-[r]->()
                WHERE r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL
                WITH r
                SET r.evidence_excerpt = coalesce(r.evidence_excerpt, r.source_excerpt),
                    r.evidence_confidence = coalesce(
                        r.evidence_confidence,
                        CASE r.datenqualitaet
                          WHEN 'belegt'           THEN 'belegt'
                          WHEN 'teilweise_belegt' THEN 'teilweise_belegt'
                          WHEN 'unklar'           THEN 'unklar'
                          WHEN 'inferiert'        THEN 'inferiert'
                          ELSE 'unklar'
                        END
                    )
                REMOVE r.source_excerpt, r.datenqualitaet
                RETURN count(r) AS touched
                """
            ).single()["touched"]

            cypher_basis_case = "\n".join(
                f"           WHEN '{t}' THEN '{b}'"
                for t, b in BASIS_DEFAULTS.items()
            )
            payload["c_canonical_filled"] = tx.run(
                f"""
                MATCH ()-[r]->()
                WHERE r.evidence_origin IS NULL
                WITH r,
                     CASE type(r)
{cypher_basis_case}
                       ELSE '{BASIS_FALLBACK}'
                     END AS basis_default
                SET r.evidence_origin     = 'derived',
                    r.evidence_basis      = basis_default,
                    r.evidence_source_id  = 'mig_4_1',
                    r.evidence_confidence = 'unklar',
                    r.evidence_excerpt    = CASE
                      WHEN r.evidence_excerpt IS NULL THEN NULL
                      WHEN toLower(r.evidence_excerpt) CONTAINS 'propagated from' THEN NULL
                      ELSE r.evidence_excerpt
                    END
                RETURN count(r) AS touched
                """
            ).single()["touched"]
            payload["c_excerpt_key_added"] = tx.run(
                """
                MATCH ()-[r]->()
                WHERE NOT 'evidence_excerpt' IN keys(r)
                SET r.evidence_excerpt = NULL
                RETURN count(r) AS touched
                """
            ).single()["touched"]

            # 4_1.e — BELEGT_IN: backfill evidence_source_id from the
            # destination :Quelle node's id. By definition a BELEGT_IN
            # edge cites the destination Quelle, so target.id IS the
            # canonical source identifier.
            payload["e_belegt_source_id_backfill"] = tx.run(
                """
                MATCH (a)-[r:BELEGT_IN]->(b:Quelle)
                WHERE r.evidence_source_id IS NULL OR r.evidence_source_id = ''
                SET r.evidence_source_id = b.id
                RETURN count(r) AS touched
                """
            ).single()["touched"]

            # 4_1.f — Remap 'legacy_migration' basis on the 8 enumerated
            # citation-group types to the per-relationship enum values.
            # BELEGT_IN edges (now with a Quelle source_id) become
            # 'cell_citation'; everything else in the group becomes
            # 'controlled_vocab'.
            payload["f_belegt_basis_normalised"] = tx.run(
                """
                MATCH ()-[r:BELEGT_IN]->()
                WHERE r.evidence_basis = 'legacy_migration'
                SET r.evidence_basis = 'cell_citation'
                RETURN count(r) AS touched
                """
            ).single()["touched"]
            payload["f_other_citation_basis_normalised"] = tx.run(
                """
                MATCH ()-[r]->()
                WHERE type(r) IN [
                  'BETEILIGT_AN','ASSOZIIERT_MIT_PROJEKT',
                  'AUS_BAUWERK','EINGEBAUT_IN',
                  'HAT_BAUTEILGRUPPE','HAT_HUERDE','HAT_AKTEURROLLE'
                ]
                AND r.evidence_basis = 'legacy_migration'
                SET r.evidence_basis = 'controlled_vocab'
                RETURN count(r) AS touched
                """
            ).single()["touched"]

            # 4_1.g — REFERENZIERT_NORM: enum is {research_file_row, standards_body}.
            # Existing non-enum values (legacy_migration, lca_module_demote)
            # are remapped to 'standards_body'; the prior basis is preserved
            # on derivation_note for traceability.
            payload["g_norm_basis_normalised"] = tx.run(
                """
                MATCH ()-[r:REFERENZIERT_NORM]->()
                WHERE NOT r.evidence_basis IN ['research_file_row','standards_body']
                SET r.derivation_note = coalesce(r.derivation_note,
                                                 'former_basis=' + r.evidence_basis),
                    r.evidence_basis  = 'standards_body'
                RETURN count(r) AS touched
                """
            ).single()["touched"]

            # 4_1.h — Phase-1.1 'demoted_from_kette' provenance on
            # HAT_HUERDE violates the citation-group enum. Remap to
            # 'propagated' (chain-demote conceptually propagates the
            # hurdle from the parent Wiederverwendungskette down onto the
            # connected Bauteilgruppe) and preserve the original signal
            # on derivation_note. Other rel types carrying the same
            # basis (HAT_LOGISTIK, HAT_METHODE, HAT_PROZESSPHASE) are
            # outside the strict-enum group so the literal value is kept.
            payload["h_huerde_demote_normalised"] = tx.run(
                """
                MATCH ()-[r:HAT_HUERDE]->()
                WHERE r.evidence_basis = 'demoted_from_kette'
                SET r.derivation_note = coalesce(r.derivation_note,
                                                 'former_basis=demoted_from_kette'),
                    r.evidence_basis  = 'propagated'
                RETURN count(r) AS touched
                """
            ).single()["touched"]

            tx.commit()

        payload["d_audit"] = step_4_1_d_audit(session)
        payload["d_enum_audit"] = step_4_1_d_enum_audit(session)

    _log(f"PHASE 4.1 — payload {json.dumps(payload, default=str)}")
    return payload


def run_phase_4_2(driver, database: str) -> dict[str, Any]:
    _log("PHASE 4.2 — rename AUS_BAUWERK / EINGEBAUT_IN")
    payload: dict[str, Any] = {}
    with driver.session(database=database) as session:
        # APOC sanity-check
        apoc_present = session.run(
            "SHOW PROCEDURES YIELD name WHERE name='apoc.refactor.rename.type' "
            "RETURN count(*) AS c"
        ).single()["c"]
        if apoc_present == 0:
            raise RuntimeError(
                "apoc.refactor.rename.type missing — cannot rename "
                "relationship types per plan §4.2."
            )

        before_aus = session.run(
            "MATCH ()-[r:AUS_BAUWERK]->() RETURN count(r) AS c"
        ).single()["c"]
        before_ein = session.run(
            "MATCH ()-[r:EINGEBAUT_IN]->() RETURN count(r) AS c"
        ).single()["c"]
        payload["before_AUS_BAUWERK"] = before_aus
        payload["before_EINGEBAUT_IN"] = before_ein

        if before_aus > 0:
            payload["rename_AUS_BAUWERK"] = step_4_2_rename(
                session, "AUS_BAUWERK", "FROM_DONOR"
            )
        else:
            payload["rename_AUS_BAUWERK"] = {"skipped": True}

        if before_ein > 0:
            payload["rename_EINGEBAUT_IN"] = step_4_2_rename(
                session, "EINGEBAUT_IN", "INTO_RECEIVER"
            )
        else:
            payload["rename_EINGEBAUT_IN"] = {"skipped": True}

        post = {
            r["rt"]: r["c"] for r in session.run(RENAME_STATUS_SQL)
        }
        payload["post_status"] = post

    _log(f"PHASE 4.2 — payload {json.dumps(payload, default=str)}")
    return payload


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
        _log(
            f"BEFORE  rels={before['total_rels']}  "
            f"missing_origin={before['evidence']['missing_origin']}  "
            f"viol_excerpt_propagated={before['evidence']['viol_excerpt_propagated']}  "
            f"legacy_source={before['evidence']['legacy_source']}  "
            f"AUS_BAUWERK={before['rename_status'].get('AUS_BAUWERK',0)}  "
            f"EINGEBAUT_IN={before['rename_status'].get('EINGEBAUT_IN',0)}"
        )

        # ---------------- Idempotency short-circuit ----------------
        # Probe the enum audit against the LIVE state so that a partial
        # prior run (which canonicalised the 5-field shape but didn't yet
        # remap legacy_migration basis to the per-relationship enum) is
        # NOT mistaken for a finished migration.
        with driver.session(database=database) as session:
            before_enum_audit = step_4_1_d_enum_audit(session)

        already_done_4_1 = (
            before["evidence"]["missing_origin"] == 0
            and before["evidence"]["missing_basis"] == 0
            and before["evidence"]["missing_source_id"] == 0
            and before["evidence"]["missing_confidence"] == 0
            and before["evidence"]["legacy_source"] == 0
            and before["evidence"]["legacy_evidence"] == 0
            and before["evidence"]["legacy_source_excerpt"] == 0
            and before["evidence"]["legacy_datenqualitaet"] == 0
            and before["evidence"]["viol_curated_no_excerpt"] == 0
            and before["evidence"]["viol_bk_not_derived"] == 0
            and before["evidence"]["viol_excerpt_propagated"] == 0
            and before_enum_audit["total_citation_violations"] == 0
            and before_enum_audit["total_norm_violations"] == 0
        )
        already_done_4_2 = (
            before["rename_status"].get("AUS_BAUWERK", 0) == 0
            and before["rename_status"].get("EINGEBAUT_IN", 0) == 0
        )
        if already_done_4_1 and already_done_4_2:
            _log("Phase 4.1 + 4.2 already satisfied — re-issuing flags only.")
            with driver.session(database=database) as session:
                after = snapshot_state(session)
            write_flag(FLAG_4, "4.1", before, after, {"skipped": True})
            write_flag(FLAG_4_2, "4.2", before, after, {"skipped": True})
            return 0

        # PHASE 4.1
        payload_41 = run_phase_4_1(driver, database)
        with driver.session(database=database) as session:
            mid = snapshot_state(session)
        _log(
            f"MID     rels={mid['total_rels']}  "
            f"missing_origin={mid['evidence']['missing_origin']}  "
            f"viol_excerpt_propagated={mid['evidence']['viol_excerpt_propagated']}"
        )

        # Hard-rule assertions for 4.1
        ev = mid["evidence"]
        assert ev["missing_origin"] == 0, f"missing_origin={ev['missing_origin']}"
        assert ev["missing_basis"] == 0, f"missing_basis={ev['missing_basis']}"
        assert ev["missing_source_id"] == 0, f"missing_source_id={ev['missing_source_id']}"
        assert ev["missing_confidence"] == 0, f"missing_confidence={ev['missing_confidence']}"
        assert ev["legacy_source"] == 0, f"legacy_source={ev['legacy_source']}"
        assert ev["legacy_evidence"] == 0, f"legacy_evidence={ev['legacy_evidence']}"
        assert ev["legacy_source_excerpt"] == 0, f"legacy_source_excerpt={ev['legacy_source_excerpt']}"
        assert ev["legacy_datenqualitaet"] == 0, f"legacy_datenqualitaet={ev['legacy_datenqualitaet']}"
        assert ev["viol_curated_no_excerpt"] == 0, f"viol_curated_no_excerpt={ev['viol_curated_no_excerpt']}"
        assert ev["viol_bk_not_derived"] == 0, f"viol_bk_not_derived={ev['viol_bk_not_derived']}"
        assert ev["viol_excerpt_propagated"] == 0, f"viol_excerpt_propagated={ev['viol_excerpt_propagated']}"

        # Per-relationship enum compliance (strict subset of types in plan §4.1)
        enum_audit = payload_41.get("d_enum_audit", {})
        assert enum_audit.get("total_citation_violations", -1) == 0, (
            f"citation-group enum violations: "
            f"{enum_audit.get('citation_group_violations')}"
        )
        assert enum_audit.get("total_norm_violations", -1) == 0, (
            f"norm-group enum violations: "
            f"{enum_audit.get('norm_group_violations')}"
        )

        # PHASE 4.2
        payload_42 = run_phase_4_2(driver, database)
        with driver.session(database=database) as session:
            after = snapshot_state(session)
        _log(
            f"AFTER   rels={after['total_rels']}  "
            f"AUS_BAUWERK={after['rename_status'].get('AUS_BAUWERK',0)}  "
            f"EINGEBAUT_IN={after['rename_status'].get('EINGEBAUT_IN',0)}  "
            f"FROM_DONOR={after['rename_status'].get('FROM_DONOR',0)}  "
            f"INTO_RECEIVER={after['rename_status'].get('INTO_RECEIVER',0)}"
        )

        # Hard-rule assertions for 4.2
        assert after["rename_status"].get("AUS_BAUWERK", 0) == 0, (
            f"AUS_BAUWERK still present after rename: "
            f"{after['rename_status'].get('AUS_BAUWERK')}"
        )
        assert after["rename_status"].get("EINGEBAUT_IN", 0) == 0, (
            f"EINGEBAUT_IN still present after rename: "
            f"{after['rename_status'].get('EINGEBAUT_IN')}"
        )
        # the rename must preserve total rel count (rename, not delete)
        assert after["total_rels"] == mid["total_rels"], (
            f"total_rels changed during rename: mid={mid['total_rels']} "
            f"after={after['total_rels']}"
        )
        # FROM_DONOR / INTO_RECEIVER must exist with the pre-rename counts
        pre_aus = before["rename_status"].get("AUS_BAUWERK", 0)
        pre_ein = before["rename_status"].get("EINGEBAUT_IN", 0)
        assert after["rename_status"].get("FROM_DONOR", 0) == pre_aus, (
            f"FROM_DONOR count {after['rename_status'].get('FROM_DONOR')} "
            f"!= pre AUS_BAUWERK {pre_aus}"
        )
        assert after["rename_status"].get("INTO_RECEIVER", 0) == pre_ein, (
            f"INTO_RECEIVER count {after['rename_status'].get('INTO_RECEIVER')} "
            f"!= pre EINGEBAUT_IN {pre_ein}"
        )

        write_flag(FLAG_4, "4.1", before, mid, payload_41)
        write_flag(FLAG_4_2, "4.2", mid, after, payload_42)

        elapsed = time.perf_counter() - started
        result = {
            "started_at": started_iso,
            "finished_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "elapsed_seconds": elapsed,
            "before": before,
            "after_phase_4_1": mid,
            "after_phase_4_2": after,
            "phase_4_1_payload": payload_41,
            "phase_4_2_payload": payload_42,
        }
        RESULT_JSON.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        _log(
            f"DONE  rels {before['total_rels']}->{after['total_rels']}  "
            f"elapsed={elapsed:.2f}s"
        )
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
