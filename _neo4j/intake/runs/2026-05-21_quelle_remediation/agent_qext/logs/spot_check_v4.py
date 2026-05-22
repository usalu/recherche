"""spot_check_v4.py — verify the v4 run produced sensible results.

Run AFTER `qext_runner.py confirm4` finishes (i.e. once
PHASE_QEXT_C_V4_DONE.flag exists). Pulls live data back from the graph
and prints a per-label quality matrix, plus sample confirmed URLs for the
test fixtures used in test_node_link.py.

Read-only against the graph. No mutations.

Run:  python spot_check_v4.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[6]
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
# noinspection PyUnresolvedReferences
from neo4j_env import resolve_connection  # type: ignore

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATABASE = "mit-bestand"


# Same fixtures as test_node_link.py — but verified against the LIVE graph
# rather than against disk.
SPOT_CHECKS = [
    # (label, id, name_hint, source: dossier where this is anchored)
    ("Material",    "mat_stahl",                            "Stahl"),
    ("Material",    "mat_holz",                             "Holz"),
    ("Material",    "mat_beton",                            "Beton"),
    ("Norm",        None,                                    "CEN/TS 1090-201"),  # match by name
    ("Bauteilgruppe", None,                                  None),               # sample by label
    ("Akteur",      "rotordc",                              "RotorDC"),
    ("Akteur",      None,                                    "HTWG Konstanz"),
    ("Akteur",      None,                                    "Baubüro in situ"),
    ("Schadstoff",  "s_asbest",                             "Asbest"),
    ("Projekt",     "p_holbein_gardens_london",             "Holbein Gardens"),
    ("Projekt",     "p_stuttgart_210",                      "Stuttgart 210"),
    ("Projekt",     "p_k118_kopfbau_halle_118_winterthur",  "K118"),
    ("ReuseRule",   "rr_gb_stahl",                          "UK Stahl ReuseRule"),
]


def get_driver():
    uri, user, password, _db = resolve_connection()
    if not uri:
        sys.exit("Missing Neo4j connection. Check .cursor/mcp.json.")
    return GraphDatabase.driver(uri, auth=(user, password))


def per_label_matrix(s):
    print(f"{'=' * 84}")
    print("Per-label confirmation coverage (post-v4)")
    print(f"{'=' * 84}")
    rows = list(s.run(
        "MATCH (n) WHERE n.source_urls IS NOT NULL "
        "  AND n.confirmed_source_urls IS NOT NULL "
        "UNWIND labels(n) AS lbl "
        "WITH lbl, count(n) AS total, "
        "     sum(CASE WHEN n.confirmed_source_count > 0 THEN 1 ELSE 0 END) AS confirmed, "
        "     avg(n.confirmed_source_count) AS avg_confirmed, "
        "     max(n.confirmed_source_count) AS max_confirmed "
        "RETURN lbl, total, confirmed, "
        "       round(100.0 * confirmed / total, 1) AS pct, "
        "       round(avg_confirmed, 2) AS avg_c, max_confirmed "
        "ORDER BY confirmed DESC, pct DESC LIMIT 30"
    ))
    print(f"  {'label':30}  {'total':>6} {'with_conf':>10} {'pct':>5} {'avg':>5} {'max':>5}")
    print(f"  {'-' * 28:30}  {'-' * 6:>6} {'-' * 10:>10} {'-' * 5:>5} {'-' * 5:>5} {'-' * 5:>5}")
    for r in rows:
        print(f"  {r['lbl']:30}  {r['total']:>6} {r['confirmed']:>10} "
              f"{r['pct']:>4}% {r['avg_c']:>5} {r['max_confirmed']:>5}")


def criterion_distribution(s):
    print(f"\n{'=' * 84}")
    print("Confirmation reasons by criterion (c1/c2/c4)")
    print(f"{'=' * 84}")
    rows = list(s.run(
        "MATCH (n) WHERE n.confirmation_evidence IS NOT NULL "
        "UNWIND keys(n.confirmation_evidence) AS url "
        "UNWIND n.confirmation_evidence[url] AS reason "
        "WITH split(reason, ':')[0] AS criterion, count(*) AS c "
        "RETURN criterion, c ORDER BY c DESC"
    ))
    for r in rows:
        print(f"  {r['criterion']:30}  {r['c']:>8}")


def spot_check_node(s, label, node_id, name_hint):
    """Pull confirmed URLs for one node and pretty-print."""
    if node_id:
        match_clause = f"MATCH (n:`{label}` {{id: $id}})"
        params = {"id": node_id}
    elif name_hint:
        match_clause = f"MATCH (n:`{label}`) WHERE toLower(coalesce(n.name,'')) = toLower($name)"
        params = {"name": name_hint}
    else:
        # Sample 3 nodes of this label that have any confirmed URL
        rows = list(s.run(
            f"MATCH (n:`{label}`) WHERE n.confirmed_source_count > 0 "
            "RETURN n.id AS id, n.name AS name, n.confirmed_source_urls AS urls, "
            "       n.confirmation_evidence AS evidence "
            "ORDER BY n.confirmed_source_count DESC LIMIT 3"
        ))
        if not rows:
            print(f"  No {label} nodes have any confirmed URL.")
            return
        for r in rows:
            print(f"\n  {label}({r['id']})  name={r['name']!r}")
            for u in (r["urls"] or [])[:5]:
                reasons = (r["evidence"] or {}).get(u, [])
                print(f"    URL: {u}")
                for reason in reasons[:3]:
                    print(f"        because: {reason}")
        return

    row = s.run(
        f"{match_clause} "
        "RETURN n.id AS id, n.name AS name, "
        "       n.source_count AS broad, n.confirmed_source_count AS confirmed, "
        "       n.confirmed_source_urls AS urls, "
        "       n.confirmation_evidence AS evidence",
        **params,
    ).single()
    if not row:
        print(f"  {label} not found: id={node_id!r}, name={name_hint!r}")
        return
    print(f"\n  {label}({row['id']})  name={row['name']!r}")
    print(f"    broad: {row['broad']}    confirmed: {row['confirmed']}")
    for u in (row["urls"] or [])[:5]:
        reasons = (row["evidence"] or {}).get(u, [])
        print(f"    URL: {u}")
        for reason in reasons[:3]:
            print(f"        because: {reason}")
    if (row["urls"] or []) and len(row["urls"]) > 5:
        print(f"    … and {len(row['urls']) - 5} more confirmed URLs")


def honesty_report(s):
    """Report nodes that have a wide gap between broad and confirmed.
    A wide gap means the broad citation graph claims many URLs, but very
    few hold up under cross-confirmation. The drop is THE honest signal."""
    print(f"\n{'=' * 84}")
    print("Honesty gap — top 10 nodes by (broad - confirmed) where broad > 5")
    print(f"{'=' * 84}")
    rows = list(s.run(
        "MATCH (n) WHERE n.source_count > 5 "
        "  AND n.confirmed_source_count IS NOT NULL "
        "WITH n, n.source_count - n.confirmed_source_count AS gap "
        "RETURN labels(n)[0] AS lbl, n.id AS id, n.name AS name, "
        "       n.source_count AS broad, n.confirmed_source_count AS conf, gap "
        "ORDER BY gap DESC LIMIT 10"
    ))
    for r in rows:
        print(f"  {r['lbl']:15}  {r['id']:50}  broad={r['broad']:3}  conf={r['conf']:3}  gap={r['gap']:3}")


def main():
    flag = (REPO_ROOT / "_neo4j" / "intake" / "runs" /
            "2026-05-21_quelle_remediation" / "agent_qext" /
            "PHASE_QEXT_C_V4_DONE.flag")
    if not flag.exists():
        print(f"PHASE_QEXT_C_V4_DONE.flag not found at {flag}.")
        print("Run `qext_runner.py confirm4` first.")
        sys.exit(2)

    print("v4 done flag found. Pulling live graph state for spot checks...\n")
    driver = get_driver()
    try:
        with driver.session(database=DATABASE, default_access_mode="READ") as s:
            per_label_matrix(s)
            criterion_distribution(s)

            print(f"\n{'=' * 84}")
            print("Spot checks on test fixtures (same nodes as test_node_link.py)")
            print(f"{'=' * 84}")
            for label, node_id, name_hint in SPOT_CHECKS:
                spot_check_node(s, label, node_id, name_hint)

            honesty_report(s)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
