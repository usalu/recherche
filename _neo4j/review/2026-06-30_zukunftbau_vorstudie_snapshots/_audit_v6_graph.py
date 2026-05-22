"""Read-only Neo4j vs v6 JSON audit for verified projects."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from neo4j import GraphDatabase

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

HERE = Path(__file__).resolve().parent


def main() -> None:
    v6 = json.loads((HERE / "project_scalability_scores_v6.json").read_text(encoding="utf-8"))
    verified = [r for r in v6 if r.get("verified")]
    uri, user, password, database = resolve_connection()
    drv = GraphDatabase.driver(uri, auth=(user, password))
    lines = [
        "# RSI v6 — Neo4j-Double-Check (read-only)",
        "",
        f"Stand: 2026-07-01 · {len(verified)} verifizierte Projekte abgeglichen",
        "",
        "| Projekt | Feld | v6-Score | Graph | Status |",
        "|---|---|---:|---:|---|",
    ]
    mismatches = 0
    with drv.session(database=database) as s:
        for r in verified:
            pid = r["id"]
            row = s.run("""
                MATCH (p:Projekt {id: $id})
                OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:AUS_SPENDER]->(b)
                WHERE b:Bauwerk OR b:Materialdepot
                RETURN count(DISTINCT b) AS donors
            """, id=pid).single()
            g_donors = row["donors"] if row else None
            v_donors = r.get("donors")
            if g_donors is not None and v_donors is not None and g_donors != v_donors:
                lines.append(f"| {r['name'][:40]} | donors | {v_donors} | {g_donors} | Diskrepanz |")
                mismatches += 1
            else:
                lines.append(f"| {r['name'][:40]} | donors | {v_donors} | {g_donors} | OK |")
    drv.close()
    lines += [
        "",
        f"**Ergebnis:** {mismatches} Spender-Diskrepanz(en) bei verifizierten Projekten.",
        "Bewertung nutzt verifizierte v6-Werte; Graph-Updates bei Bedarf separat.",
        "",
        "Vollständige Graph-RSIAssessment-Knoten (v6 §17) sind noch nicht importiert — Scores liegen in `project_scalability_scores_v6.json`.",
    ]
    out = HERE / "scalability_v6_graph_audit.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({mismatches} mismatches)")


if __name__ == "__main__":
    main()
