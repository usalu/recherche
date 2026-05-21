"""Repair Agent E — execute mig_repair_2_7_5_1_quality_tier_panel.cypher.

Folds the 9 Phase-5.1 audit scalars on every :Projekt into one
`quality_tier_facts` JSON string, restoring the Phase 2.7 panel targets.

Writes:
  - logs/repair_2_7_5_1_runner_before.json
  - logs/repair_2_7_5_1_runner_after.json
  - logs/repair_2_7_5_1_runner.log
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ENTWERFENMITBESTAND")
DB = "mit-bestand"

RUN_DIR = Path(r"E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset")
MIG_FILE = RUN_DIR / "migrations/mig_repair_2_7_5_1_quality_tier_panel.cypher"
LOG_FILE = RUN_DIR / "logs/repair_2_7_5_1_runner.log"
BEFORE_FILE = RUN_DIR / "logs/repair_2_7_5_1_runner_before.json"
AFTER_FILE = RUN_DIR / "logs/repair_2_7_5_1_runner_after.json"


KEYS_TO_FOLD = [
    "quality_tier_computed_by",
    "quality_tier_has_components",
    "quality_tier_has_evidence",
    "quality_tier_has_land",
    "quality_tier_has_metric",
    "quality_tier_has_year",
    "quality_tier_n_bg",
    "quality_tier_n_bg_quantified",
    "quality_tier_n_curated_evidence",
]


def snapshot(session) -> dict:
    out: dict = {}
    out["projekt_total"] = session.run(
        "MATCH (p:Projekt) RETURN count(p) AS c"
    ).single()["c"]
    out["distinct_keys"] = session.run(
        "MATCH (p:Projekt) UNWIND keys(p) AS k RETURN count(DISTINCT k) AS c"
    ).single()["c"]
    out["keys_with_freq"] = [
        dict(r)
        for r in session.run(
            "MATCH (p:Projekt) UNWIND keys(p) AS k "
            "RETURN k AS key, count(*) AS n ORDER BY key"
        )
    ]
    out["max_per_node"] = [
        dict(r)
        for r in session.run(
            "MATCH (p:Projekt) RETURN p.id AS id, size(keys(p)) AS n_keys "
            "ORDER BY n_keys DESC LIMIT 8"
        )
    ]
    out["sample_per_node"] = [
        dict(r)
        for r in session.run(
            "MATCH (p:Projekt) WITH p ORDER BY p.id LIMIT 5 "
            "RETURN p.id AS id, size(keys(p)) AS n_keys, p.quality_tier AS tier"
        )
    ]
    out["tier_distribution"] = [
        dict(r)
        for r in session.run(
            "MATCH (p:Projekt) RETURN p.quality_tier AS tier, count(p) AS n "
            "ORDER BY tier"
        )
    ]
    out["facts_present"] = session.run(
        "MATCH (p:Projekt) WHERE p.quality_tier_facts IS NOT NULL RETURN count(p) AS c"
    ).single()["c"]
    out["scalars_present"] = {
        k: session.run(
            f"MATCH (p:Projekt) WHERE p.{k} IS NOT NULL RETURN count(p) AS c"
        ).single()["c"]
        for k in KEYS_TO_FOLD
    }
    out["p_circle_house"] = dict(
        session.run(
            "MATCH (p:Projekt {id:'p_circle_house'}) "
            "RETURN labels(p) AS labels, p.quality_tier AS quality_tier, "
            "       p.quality_tier_facts AS quality_tier_facts, "
            "       size(keys(p)) AS n_keys"
        ).single()
    )
    return out


def main() -> int:
    log_lines: list[str] = []

    def log(msg: str) -> None:
        ts = datetime.now(timezone.utc).isoformat()
        line = f"[{ts}] {msg}"
        print(line)
        log_lines.append(line)

    driver = GraphDatabase.driver(URI, auth=AUTH)
    try:
        with driver.session(database=DB) as session:
            log("--- before snapshot ---")
            before = snapshot(session)
            BEFORE_FILE.write_text(
                json.dumps(before, indent=2, ensure_ascii=False, default=str),
                encoding="utf-8",
            )
            log(
                f"before: projekt_total={before['projekt_total']} "
                f"distinct_keys={before['distinct_keys']} "
                f"facts_present={before['facts_present']}"
            )

            if all(v == 0 for v in before["scalars_present"].values()):
                log(
                    "scalars_present is zero across all 9 fold keys — "
                    "migration is already applied or never created. "
                    "No write needed."
                )
                graph_changed = False
            else:
                # APOC sanity check.
                try:
                    apoc_ok = session.run(
                        "RETURN apoc.convert.toJson({a:1}) AS j"
                    ).single()["j"]
                    log(f"apoc.convert.toJson available: {apoc_ok}")
                except Exception as exc:  # noqa: BLE001
                    log(f"FATAL: APOC unavailable: {exc}")
                    return 2

                fold_cypher = """
                MATCH (p:Projekt)
                WHERE p.quality_tier_computed_by IS NOT NULL
                WITH p, apoc.convert.toJson({
                        computed_by:        p.quality_tier_computed_by,
                        has_components:     p.quality_tier_has_components,
                        has_evidence:       p.quality_tier_has_evidence,
                        has_land:           p.quality_tier_has_land,
                        has_metric:         p.quality_tier_has_metric,
                        has_year:           p.quality_tier_has_year,
                        n_bg:               p.quality_tier_n_bg,
                        n_bg_quantified:    p.quality_tier_n_bg_quantified,
                        n_curated_evidence: p.quality_tier_n_curated_evidence,
                        repaired_by:        'mig_repair_2_7_5_1_quality_tier_panel',
                        repaired_at:        '2026-05-21'
                }) AS facts_json
                SET p.quality_tier_facts = facts_json
                REMOVE p.quality_tier_computed_by,
                       p.quality_tier_has_components,
                       p.quality_tier_has_evidence,
                       p.quality_tier_has_land,
                       p.quality_tier_has_metric,
                       p.quality_tier_has_year,
                       p.quality_tier_n_bg,
                       p.quality_tier_n_bg_quantified,
                       p.quality_tier_n_curated_evidence
                RETURN count(p) AS n_updated
                """

                log("--- applying fold migration ---")
                result = session.run(fold_cypher).single()
                n_updated = result["n_updated"]
                log(f"fold migration updated {n_updated} :Projekt nodes")
                graph_changed = n_updated > 0

            log("--- after snapshot ---")
            after = snapshot(session)
            AFTER_FILE.write_text(
                json.dumps(after, indent=2, ensure_ascii=False, default=str),
                encoding="utf-8",
            )
            log(
                f"after:  projekt_total={after['projekt_total']} "
                f"distinct_keys={after['distinct_keys']} "
                f"facts_present={after['facts_present']}"
            )

            # Acceptance Q3 sanity (must still work).
            q3 = session.run(
                "MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'}) "
                "UNWIND p.reuse_share_facts AS rs RETURN count(*) AS rows"
            ).single()["rows"]
            log(f"acceptance Q3 rows after repair: {q3}")

            # Acceptance Q6 sanity (must still work).
            q6 = [
                dict(r)
                for r in session.run(
                    "MATCH (p:Projekt)-[r]-() "
                    "WITH r.evidence_origin AS origin, count(*) AS c "
                    "RETURN origin, c ORDER BY c DESC"
                )
            ]
            log(f"acceptance Q6 rows after repair: {q6}")

            # Tier distribution sanity.
            tiers = [
                dict(r)
                for r in session.run(
                    "MATCH (p:Projekt) RETURN p.quality_tier AS tier, "
                    "count(p) AS n ORDER BY tier"
                )
            ]
            log(f"tier distribution after repair: {tiers}")

            return 0 if graph_changed or all(
                v == 0 for v in before["scalars_present"].values()
            ) else 1
    finally:
        LOG_FILE.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
        driver.close()


if __name__ == "__main__":
    sys.exit(main())
