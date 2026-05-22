"""check_neo4j.py — report whether the Neo4j connection is usable.

Shows where each setting came from (environment variable or `.cursor/mcp.json`),
verifies connectivity, and prints the size of the target database. Read-only.

    python _scripts/check_neo4j.py
    python _scripts/check_neo4j.py --database mit-bestand
    python _scripts/check_neo4j.py --json

Exit codes: 0 = usable, 1 = reachable but the database looks wrong, 2 = cannot connect.
The password is never printed — only whether one was found.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import load_mcp_neo4j_env, resolve_connection  # noqa: E402


def origin(env_names: tuple[str, ...], mcp: dict, mcp_key: str) -> str:
    for name in env_names:
        if os.environ.get(name, "").strip():
            return f"env {name}"
    if mcp.get(mcp_key, "").strip():
        return ".cursor/mcp.json"
    return "default"


def build_report(database_override: str | None) -> dict:
    uri, user, password, database = resolve_connection()
    mcp = load_mcp_neo4j_env()
    report: dict = {
        "uri": uri,
        "user": user,
        "password_found": bool(password),
        "database": database_override or database,
        "origins": {
            "uri": origin(("NEO4J_URI",), mcp, "NEO4J_URI"),
            "user": origin(("NEO4J_USERNAME", "NEO4J_USER"), mcp, "NEO4J_USERNAME"),
            "password": origin(("NEO4J_PASSWORD",), mcp, "NEO4J_PASSWORD"),
            "database": origin(("NEO4J_DATABASE",), mcp, "NEO4J_DATABASE"),
        },
        "driver": None,
        "connected": False,
        "server": None,
        "counts": {},
        "error": None,
    }

    if not (uri and user and password):
        report["error"] = (
            "Missing connection settings. Set NEO4J_URI / NEO4J_USERNAME / "
            "NEO4J_PASSWORD, or provide them in .cursor/mcp.json."
        )
        return report

    try:
        import neo4j
        from neo4j import GraphDatabase
    except ImportError:
        report["error"] = (
            "The neo4j Python driver is not installed. "
            "Run: python -m pip install -r requirements-neo4j.txt"
        )
        return report

    report["driver"] = neo4j.__version__
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        try:
            driver.verify_connectivity()
            report["connected"] = True
            with driver.session(
                database=report["database"], default_access_mode="READ"
            ) as session:
                report["counts"] = {
                    "nodes": session.run("MATCH (n) RETURN count(n) AS c").single()["c"],
                    "relationships": session.run(
                        "MATCH ()-[r]->() RETURN count(r) AS c"
                    ).single()["c"],
                    "labels": len(list(session.run("CALL db.labels()"))),
                    "relationship_types": len(
                        list(session.run("CALL db.relationshipTypes()"))
                    ),
                }
                # Enterprise returns several components; the first is the kernel.
                record = next(
                    iter(
                        session.run(
                            "CALL dbms.components() YIELD name, versions, edition "
                            "RETURN name, versions[0] AS version, edition"
                        )
                    ),
                    None,
                )
                if record:
                    report["server"] = f"{record['name']} {record['version']} ({record['edition']})"
        finally:
            driver.close()
    except Exception as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"

    return report


def format_text(report: dict) -> str:
    lines = ["Neo4j connection"]
    lines.append(f"  uri:        {report['uri'] or '(unset)'}   [{report['origins']['uri']}]")
    lines.append(f"  user:       {report['user'] or '(unset)'}   [{report['origins']['user']}]")
    lines.append(
        f"  password:   {'found' if report['password_found'] else 'MISSING'}"
        f"   [{report['origins']['password']}]"
    )
    lines.append(f"  database:   {report['database']}   [{report['origins']['database']}]")
    lines.append(f"  driver:     {report['driver'] or 'not installed'}")
    lines.append("")
    if report["error"]:
        lines.append(f"  connected:  NO")
        lines.append(f"  error:      {report['error']}")
        return "\n".join(lines)

    lines.append("  connected:  YES")
    if report["server"]:
        lines.append(f"  server:     {report['server']}")
    counts = report["counts"]
    lines.append(
        f"  content:    {counts.get('nodes', 0):,} nodes · "
        f"{counts.get('relationships', 0):,} relationships · "
        f"{counts.get('labels', 0)} labels · "
        f"{counts.get('relationship_types', 0)} relationship types"
    )
    return "\n".join(lines)


def exit_code(report: dict) -> int:
    if report["error"] or not report["connected"]:
        return 2
    return 0 if report["counts"].get("nodes", 0) > 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Report Neo4j connection status.")
    ap.add_argument("--database", help="Check a database other than the configured one")
    ap.add_argument("--json", action="store_true", help="Emit the report as JSON")
    args = ap.parse_args()

    report = build_report(args.database)
    print(json.dumps(report, indent=2) if args.json else format_text(report))
    return exit_code(report)


if __name__ == "__main__":
    sys.exit(main())
