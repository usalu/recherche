"""Run Phase 0.3 pre-deletion scan and dump results to JSON for forensic review."""
from __future__ import annotations
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[3] / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

PLAN_DIR = Path(__file__).resolve().parent
OUT_DIR = PLAN_DIR / "snapshot_pre_integration"
OUT_DIR.mkdir(exist_ok=True)
OUT_JSON = OUT_DIR / "pre_deletion_scan.json"


QUERIES = {
    "old_vocab_nodes": """
        MATCH (n)
        WHERE n:Methode OR n:Aufbereitungsverfahren OR n:Ressourcenquelle
           OR n:WiederverwendungsArt
           OR (n:Rueckbauverfahren AND n.id = 'rv_betonfraesen')
        RETURN labels(n) AS labels, n.id AS id, n.name AS name,
               count{ (n)<-[]-() } AS inbound_edges,
               count{ (n)-[]->() } AS outbound_edges
        ORDER BY labels[0], id
    """,
    "inbound_edge_summary": """
        MATCH (src)-[r]->(t)
        WHERE t:Methode OR t:Aufbereitungsverfahren OR t:Ressourcenquelle
           OR t:WiederverwendungsArt
           OR (t:Rueckbauverfahren AND t.id = 'rv_betonfraesen')
        RETURN labels(src) AS src_labels,
               type(r) AS rel_type,
               labels(t) AS target_labels,
               count(r) AS edge_count
        ORDER BY edge_count DESC
    """,
    "outbound_edge_summary": """
        MATCH (n)-[r]->(tgt)
        WHERE n:Aufbereitungsverfahren OR n:Methode OR n:Ressourcenquelle
           OR n:WiederverwendungsArt
           OR (n:Rueckbauverfahren AND n.id = 'rv_betonfraesen')
        RETURN labels(n) AS source_labels,
               type(r) AS rel_type,
               labels(tgt) AS target_labels,
               count(r) AS edge_count
        ORDER BY edge_count DESC
    """,
    "bg_reuse_orphans_count": """
        MATCH (bg:Bauteilgruppe)
        WHERE bg.id STARTS WITH 'bg_reuse_'
        RETURN count(bg) AS total_bg_reuse
    """,
    "bg_non_reuse_count": """
        MATCH (bg:Bauteilgruppe)
        WHERE bg.id STARTS WITH 'bg_retained_'
           OR bg.id STARTS WITH 'bg_planned_'
           OR bg.id STARTS WITH 'bg_dismantled_'
           OR bg.id STARTS WITH 'bg_candidate_'
        RETURN bg.id STARTS WITH 'bg_retained_' AS is_retained,
               bg.id STARTS WITH 'bg_planned_' AS is_planned,
               bg.id STARTS WITH 'bg_dismantled_' AS is_dismantled,
               bg.id STARTS WITH 'bg_candidate_' AS is_candidate,
               count(bg) AS n
    """,
    "bg_non_reuse_full_list": """
        MATCH (bg:Bauteilgruppe)
        WHERE bg.id STARTS WITH 'bg_retained_'
           OR bg.id STARTS WITH 'bg_planned_'
           OR bg.id STARTS WITH 'bg_dismantled_'
           OR bg.id STARTS WITH 'bg_candidate_'
        RETURN bg.id AS id, bg.name AS name,
               bg.alte_funktion AS alte_funktion,
               bg.neue_funktion AS neue_funktion,
               count{ (bg)<-[]-() } AS inbound_edges,
               count{ (bg)-[]->() } AS outbound_edges
        ORDER BY id
    """,
    "dataissue_count": "MATCH (di:DataIssue) RETURN count(di) AS n",
    "current_constraints": "SHOW CONSTRAINTS YIELD name, labelsOrTypes, properties RETURN name, labelsOrTypes, properties ORDER BY name",
}


def main() -> int:
    from neo4j import GraphDatabase
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password), connection_timeout=30)

    out = {}
    try:
        with driver.session(database=database) as session:
            for label, q in QUERIES.items():
                print(f"\n--- {label} ---")
                rows = []
                for r in session.run(q):
                    rec = dict(r)
                    # Convert non-JSON-serialisable types
                    for k, v in list(rec.items()):
                        if hasattr(v, "isoformat"):
                            rec[k] = v.isoformat()
                    rows.append(rec)
                out[label] = rows
                # Print sample
                for r in rows[:10]:
                    print(f"  {r}")
                if len(rows) > 10:
                    print(f"  ... +{len(rows)-10} more")
                print(f"  total rows: {len(rows)}")
    finally:
        driver.close()

    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"\n=> Wrote {OUT_JSON} ({OUT_JSON.stat().st_size//1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
