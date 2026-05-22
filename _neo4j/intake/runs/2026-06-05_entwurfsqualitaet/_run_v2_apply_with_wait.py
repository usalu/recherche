"""Wait for Neo4j, backup, apply v2 vocabulary, verify beschreibung on nodes."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))

from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT = Path(__file__).resolve().parent
APPLY = OUT / "apply_entwurfsqualitaet_v2.py"
BACKUP = REPO / "_scripts" / "backup_neo4j_graph.py"
WAIT_SEC = 180
POLL_SEC = 5


def can_connect() -> bool:
    uri, user, password, database = resolve_connection()
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session(database=database) as session:
            session.run("RETURN 1").single()
        driver.close()
        return True
    except Exception:
        return False


def wait_for_neo4j() -> bool:
    deadline = time.time() + WAIT_SEC
    while time.time() < deadline:
        if can_connect():
            return True
        print(f"Neo4j not ready, retry in {POLL_SEC}s...", flush=True)
        time.sleep(POLL_SEC)
    return False


def verify_beschreibung() -> dict:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session(database=database) as session:
            rows = list(
                session.run(
                    """
                    MATCH (n)
                    WHERE (n:Entwurfsmethodik OR n:Architekturergebnis) AND NOT n:DEPRECATED
                    RETURN n.id AS id, n.name AS name,
                           n.beschreibung IS NOT NULL AND trim(n.beschreibung) <> '' AS has_beschreibung,
                           n.vokabular_version AS version
                    ORDER BY id
                    """
                )
            )
            missing = [dict(r) for r in rows if not r["has_beschreibung"]]
            return {
                "active_vocab_nodes": len(rows),
                "all_have_beschreibung": len(missing) == 0,
                "missing_beschreibung": missing,
                "nodes": [dict(r) for r in rows],
            }
    finally:
        driver.close()


def main() -> int:
    print("Waiting for Neo4j on localhost:7687 (mit-bestand)...", flush=True)
    if not wait_for_neo4j():
        print("ERROR: Neo4j still unreachable. Start mit-bestand in Neo4j Desktop.", flush=True)
        return 1

    print("Neo4j up. Creating backup...", flush=True)
    backup_dir = REPO / "_neo4j" / "review" / "backups" / "20260605T_entwurfsqualitaet_pre_v2"
    subprocess.run(
        [sys.executable, str(BACKUP), "--out-dir", str(backup_dir)],
        check=True,
        cwd=str(REPO),
    )

    print("Applying v2 vocabulary (--commit)...", flush=True)
    subprocess.run([sys.executable, str(APPLY), "--commit"], check=True, cwd=str(REPO))

    report_path = OUT / "apply_v2_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    beschreibung_check = verify_beschreibung()
    report["beschreibung_verification"] = beschreibung_check
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"apply": report, "beschreibung": beschreibung_check}, ensure_ascii=False, indent=2))
    if not beschreibung_check["all_have_beschreibung"]:
        print("ERROR: Some vocab nodes missing beschreibung.", flush=True)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
