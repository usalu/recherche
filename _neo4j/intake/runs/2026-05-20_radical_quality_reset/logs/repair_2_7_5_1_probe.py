"""Probe the live state of Projekt nodes before the 2.7 / 5.1 repair.

Read-only.  Captures:
  - distinct key set across :Projekt,
  - exact list of `quality_tier_*` keys present,
  - per-node key counts (top sample),
  - p_circle_house property bag (so we can document the Tier 2 decision),
  - sanity for `_archive` presence.
"""
from __future__ import annotations

import json
from pathlib import Path

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ENTWERFENMITBESTAND")
DB = "mit-bestand"

RUN_DIR = Path(r"E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset")


def q(session, query, **params):
    return [dict(r) for r in session.run(query, **params)]


def main() -> dict:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    out: dict = {}
    with driver.session(database=DB, default_access_mode="READ") as s:
        out["projekt_total"] = q(s, "MATCH (p:Projekt) RETURN count(p) AS c")[0]["c"]

        out["distinct_keys"] = q(
            s,
            """
            MATCH (p:Projekt) UNWIND keys(p) AS k
            RETURN count(DISTINCT k) AS n_distinct
            """,
        )[0]["n_distinct"]

        out["all_keys_with_freq"] = q(
            s,
            """
            MATCH (p:Projekt) UNWIND keys(p) AS k
            RETURN k AS key, count(*) AS n
            ORDER BY key
            """,
        )

        out["quality_tier_keys"] = q(
            s,
            """
            MATCH (p:Projekt) UNWIND keys(p) AS k
            WITH k WHERE k STARTS WITH 'quality_tier'
            RETURN DISTINCT k AS key ORDER BY key
            """,
        )

        out["per_node_keys_sample"] = q(
            s,
            """
            MATCH (p:Projekt) WITH p ORDER BY p.id LIMIT 8
            RETURN p.id AS id,
                   size(keys(p)) AS n_keys,
                   [k IN keys(p) WHERE k STARTS WITH 'quality_tier' | k] AS qt_keys,
                   p.quality_tier AS tier
            """,
        )

        out["per_node_keys_max"] = q(
            s,
            """
            MATCH (p:Projekt)
            RETURN p.id AS id, size(keys(p)) AS n_keys
            ORDER BY n_keys DESC LIMIT 8
            """,
        )

        out["p_circle_house"] = q(
            s,
            """
            MATCH (p:Projekt {id:'p_circle_house'})
            RETURN labels(p) AS labels,
                   p.quality_tier AS quality_tier,
                   p.quality_tier_has_year AS has_year,
                   p.quality_tier_has_land AS has_land,
                   p.quality_tier_has_components AS has_components,
                   p.quality_tier_has_metric AS has_metric,
                   p.quality_tier_has_evidence AS has_evidence,
                   p.quality_tier_n_bg AS n_bg,
                   p.quality_tier_n_bg_quantified AS n_bg_quantified,
                   p.quality_tier_n_curated_evidence AS n_curated_evidence,
                   p.quality_tier_computed_by AS computed_by,
                   size(keys(p)) AS n_keys,
                   keys(p) AS all_keys,
                   (p._archive IS NOT NULL) AS has_archive
            """,
        )

        out["archive_facts_collision_check"] = q(
            s,
            """
            MATCH (p:Projekt) WHERE p.quality_tier_facts IS NOT NULL
            RETURN count(p) AS n
            """,
        )[0]["n"]

        out["tier_distribution"] = q(
            s,
            """
            MATCH (p:Projekt) RETURN p.quality_tier AS tier, count(p) AS n
            ORDER BY tier
            """,
        )

    driver.close()
    return out


if __name__ == "__main__":
    data = main()
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    (RUN_DIR / "logs" / "repair_2_7_5_1_probe.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )
