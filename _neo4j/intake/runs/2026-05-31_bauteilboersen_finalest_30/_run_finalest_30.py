"""
Executor for bauteilboersen_finalest_30_2026_05_31 migration.

Runs in three phases:
  1. PART A tests (preconditions). Abort if any FAIL.
  2. RUN_MIGRATION.cypher (STEPs 0 -> 6B).
  3. PART B tests (final-state validation). Report PASS/FAIL.

Connection: NEO4J_URI env override, defaults to neo4j://127.0.0.1:7687.
Password:   reads .neo4j_password from CWD (project root).
Database:   mit-bestand.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from neo4j import GraphDatabase

URI      = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
USER     = os.environ.get("NEO4J_USER", "neo4j").strip()
DATABASE = os.environ.get("NEO4J_DATABASE", "mit-bestand").strip()
PWPATH   = Path(".neo4j_password")

BASE          = Path("_neo4j/intake/runs/2026-05-31_bauteilboersen_finalest_30")
MIGRATION_F   = BASE / "RUN_MIGRATION.cypher"
TESTS_F       = BASE / "MIGRATION_TESTS.cypher"


def read_password() -> str:
    for line in PWPATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    raise RuntimeError("no password line found in .neo4j_password")


def strip_line_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        i = line.find("//")
        out.append(line if i < 0 else line[:i])
    return "\n".join(out)


def split_statements(text: str) -> list[str]:
    text = strip_line_comments(text)
    return [s.strip() for s in text.split(";") if s.strip()]


def split_tests_by_part(text: str) -> dict[str, list[str]]:
    """Group MIGRATION_TESTS by PART A / B / C using the '// PART X' markers."""
    sections: dict[str, list[str]] = {"A": [], "B": [], "C": []}
    current: str | None = None
    buf: list[str] = []
    for line in text.splitlines():
        if "PART A" in line and "--" in line and "PRE-MIGRATION" in line:
            if current and buf:
                sections[current].append("\n".join(buf)); buf = []
            current = "A"; continue
        if "PART B" in line and "--" in line and "POST-MIGRATION" in line:
            if current and buf:
                sections[current].append("\n".join(buf)); buf = []
            current = "B"; continue
        if "PART C" in line and "--" in line and "DIAGNOSTICS" in line:
            if current and buf:
                sections[current].append("\n".join(buf)); buf = []
            current = "C"; continue
        buf.append(line)
    if current and buf:
        sections[current].append("\n".join(buf))
    return {k: split_statements("\n".join(v)) for k, v in sections.items()}


def fmt_row(row: dict) -> str:
    tid    = row.get("test_id", "?")
    status = row.get("status", "?")
    mark   = {"PASS": "[PASS]", "INFO": "[INFO]", "WARN": "[WARN]", "FAIL": "[FAIL]"}.get(status, "[?]")
    keys_known = {"test_id", "status"}
    extra_items = [(k, v) for k, v in row.items() if k not in keys_known]
    extras = ", ".join(f"{k}={v!r}" for k, v in extra_items)
    return f"  {mark} {tid:40s} {extras}"


def run_section(session, label: str, statements: list[str]) -> tuple[int, int, dict]:
    """Run a list of read-only test queries. Return (n_run, n_fail, special_values)."""
    print(f"\n========== {label} ({len(statements)} queries) ==========")
    n_run, n_fail = 0, 0
    captured = {}
    for stmt in statements:
        result = session.run(stmt)
        for row in result:
            d = dict(row)
            print(fmt_row(d))
            n_run += 1
            if d.get("status") == "FAIL":
                n_fail += 1
            # capture special INFO values for cross-section reference
            if d.get("test_id", "").startswith("A.11"):
                captured["A.11"] = d.get("observed_baseline_count")
            if d.get("test_id", "").startswith("B.21"):
                captured["B.21"] = d.get("observed_final_count")
    return n_run, n_fail, captured


def run_migration_statements(session, statements: list[str]) -> int:
    print(f"\n========== MIGRATION ({len(statements)} statements) ==========")
    errors = 0
    for i, stmt in enumerate(statements, 1):
        preview = " ".join(stmt.split())
        if len(preview) > 100:
            preview = preview[:97] + "..."
        try:
            summary = session.run(stmt).consume()
            c = summary.counters
            changes = {
                "nodes_+": c.nodes_created,
                "nodes_-": c.nodes_deleted,
                "rels_+":  c.relationships_created,
                "rels_-":  c.relationships_deleted,
                "labels_+": c.labels_added,
                "props_+": c.properties_set,
                "constraints_+": c.constraints_added,
            }
            changes = {k: v for k, v in changes.items() if v}
            print(f"  [{i:2d}/{len(statements)}] {preview:100s}  {changes or '{}'}")
        except Exception as e:
            errors += 1
            print(f"  [{i:2d}/{len(statements)}] [FAIL] ERROR: {e}")
            print(f"      Failing statement:\n      {stmt[:500]}")
    return errors


def main() -> int:
    pw = read_password()
    print(f"Connecting: {URI}  db={DATABASE}  user={USER}")
    driver = GraphDatabase.driver(URI, auth=(USER, pw))
    try:
        driver.verify_connectivity()
    except Exception as e:
        print(f"[FAIL] Connection failed: {e}")
        return 2

    tests_text     = TESTS_F.read_text(encoding="utf-8")
    sections       = split_tests_by_part(tests_text)
    migration_text = MIGRATION_F.read_text(encoding="utf-8")
    migration_stmts = split_statements(migration_text)

    with driver.session(database=DATABASE) as s:
        n_a, fail_a, capA = run_section(s, "PART A --PRE-MIGRATION", sections["A"])
        if fail_a:
            print(f"\n[FAIL] PART A: {fail_a}/{n_a} FAIL. Aborting --no changes made.")
            return 1
        baseline = capA.get("A.11")
        print(f"\n[OK] PART A all-PASS. Baseline at_materialhub_bauteilboerse count: {baseline}")

        errs = run_migration_statements(s, migration_stmts)
        if errs:
            print(f"\n[FAIL] Migration had {errs} statement error(s). PART B may show partial state.")

        n_b, fail_b, capB = run_section(s, "PART B --POST-MIGRATION", sections["B"])
        final = capB.get("B.21")

        print("\n========== SUMMARY ==========")
        print(f"PART A: {n_a-fail_a}/{n_a} PASS")
        print(f"Migration statements: {len(migration_stmts)} run, {errs} error(s)")
        print(f"PART B: {n_b-fail_b}/{n_b} PASS")
        if baseline is not None and final is not None:
            diff = baseline - final
            print(f"materialhub_bauteilboerse actors: {baseline} -> {final} (delta {-diff:+d}, expected -9)")
        if fail_b == 0 and errs == 0:
            print("[OK] FINALIZED.")
            return 0
        else:
            print("[FAIL] Issues --consider rollback (see FINAL_IMPORT_PLAN.md).")
            return 1
    # driver will be closed by context
    driver.close()


if __name__ == "__main__":
    sys.exit(main())
