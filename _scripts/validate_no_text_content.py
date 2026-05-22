"""validate_no_text_content.py — CI gate: fail if any :Dossier carries text_content.

Run after every ingestion batch. Add to the pre-flight in _neo4j/intake/README.md.

    python _scripts/validate_no_text_content.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, password, _db = resolve_connection()
with GraphDatabase.driver(uri, auth=(user, password)) as driver:
    with driver.session(database="mit-bestand", default_access_mode="READ") as s:
        result = s.run(
            "MATCH (d:Dossier) WHERE d.text_content IS NOT NULL RETURN count(d) AS c"
        ).single()
        n = result["c"]
        if n > 0:
            print(
                f"FAIL: {n} :Dossier node(s) carry text_content. "
                "Strip via S4 / mig_s4_b_text_strip before merging.",
                file=sys.stderr,
            )
            sys.exit(2)
        print(f"OK: no :Dossier carries text_content (checked {_db}).")
