"""
Read-only resolver + evidence puller for the 2026-05-31 reuse-project graph cleanup.

Reads a candidates.yaml (list of named projects with optional id/aliases), resolves
each against the live Neo4j graph by id / name / alias (exact first, fuzzy fallback),
then pulls reuse-evidence relationships per resolved candidate. Writes:
  - resolution.jsonl: one line per candidate with resolved id (or absent_from_graph)
  - evidence.jsonl:   one line per resolved candidate with reuse evidence
  - status_inventory.json: distinct status values seen on the matched + adjacent :Projekt set
  - duplicate_clusters.json: groups of :Projekt|:Programm nodes sharing a normalised name key

No mutations are performed. Database access mode is READ.

Usage:
  python _scripts/resolve_reuse_project_candidates.py \
    --candidates _neo4j/review/2026-05-31_project_reuse_focus_cleanup/candidates.yaml \
    --out-dir   _neo4j/review/2026-05-31_project_reuse_focus_cleanup/ \
    --password-file .neo4j_password
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def _read_password(password_file: Path | None) -> str:
    password = (os.environ.get("NEO4J_PASSWORD") or "").strip()
    if password or password_file is None:
        return password
    if not password_file.is_file():
        raise FileNotFoundError(f"--password-file not found: {password_file}")
    for line in password_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return ""


def _load_candidates(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    # Lightweight YAML loader — only handles the simple shape we emit (list of dicts
    # with scalar values + optional aliases list). Avoids adding pyyaml as a dep.
    entries: list[dict] = []
    cur: dict | None = None
    in_aliases = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("- "):
            if cur is not None:
                entries.append(cur)
            cur = {}
            in_aliases = False
            rest = line[2:].strip()
            if rest:
                k, _, v = rest.partition(":")
                cur[k.strip()] = v.strip().strip('"')
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if cur is None:
            continue
        if indent >= 2 and stripped.startswith("- "):
            if in_aliases:
                cur.setdefault("aliases", []).append(stripped[2:].strip().strip('"'))
            continue
        k, _, v = stripped.partition(":")
        key = k.strip()
        val = v.strip().strip('"')
        if key == "aliases":
            in_aliases = True
            cur["aliases"] = []
        else:
            in_aliases = False
            cur[key] = val
    if cur is not None:
        entries.append(cur)
    return entries


_NORM_RE = re.compile(r"[\s\(\)\-_/.,!]+")


def _norm_name(name: str | None) -> str:
    if not name:
        return ""
    return _NORM_RE.sub("", name).lower()


def resolve_candidate(session, entry: dict) -> dict:
    """Resolve one candidate against the graph. Returns a row for resolution.jsonl."""
    name = (entry.get("name") or "").strip()
    candidate_id = (entry.get("id") or "").strip() or None
    aliases = entry.get("aliases") or []
    needles: list[str] = [name] + [a for a in aliases if a]

    # 1) Exact match on id, name (case-insensitive), or alias array
    query_exact = (
        "MATCH (n) "
        "WHERE ($id IS NOT NULL AND n.id = $id) "
        "   OR ($name <> '' AND toLower(coalesce(n.name,'')) = toLower($name)) "
        "   OR ANY(a IN $aliases WHERE toLower(a) = toLower(coalesce(n.name,''))) "
        "   OR ANY(a IN coalesce(n.aliases, []) WHERE toLower(a) IN [x IN $needles | toLower(x)]) "
        "RETURN n.id AS id, labels(n) AS labels, n.name AS name, "
        "       coalesce(n.status, '') AS status, "
        "       coalesce(n.aliases, []) AS aliases"
    )
    rows = list(session.run(query_exact, id=candidate_id, name=name, aliases=aliases, needles=needles))
    if rows:
        return {
            "candidate_name": name,
            "candidate_id": candidate_id,
            "candidate_aliases": aliases,
            "resolution": "exact",
            "matches": [
                {
                    "id": r["id"],
                    "labels": list(r["labels"]),
                    "name": r["name"],
                    "status": r["status"],
                    "aliases": list(r["aliases"]),
                }
                for r in rows
            ],
        }

    # 2) Fuzzy fallback: CONTAINS on lowercased name + alias, LIMIT 5
    candidates_fuzzy: list[dict] = []
    for needle in needles:
        if not needle or len(needle) < 4:
            continue
        rows = list(
            session.run(
                "MATCH (n) WHERE toLower(coalesce(n.name,'')) CONTAINS toLower($needle) "
                "   OR ANY(a IN coalesce(n.aliases, []) WHERE toLower(a) CONTAINS toLower($needle)) "
                "RETURN n.id AS id, labels(n) AS labels, n.name AS name, coalesce(n.status,'') AS status "
                "LIMIT 5",
                needle=needle,
            )
        )
        for r in rows:
            candidates_fuzzy.append(
                {"id": r["id"], "labels": list(r["labels"]), "name": r["name"], "status": r["status"], "needle": needle}
            )
    if candidates_fuzzy:
        return {
            "candidate_name": name,
            "candidate_id": candidate_id,
            "candidate_aliases": aliases,
            "resolution": "fuzzy_review_required",
            "matches": candidates_fuzzy[:25],
        }

    return {
        "candidate_name": name,
        "candidate_id": candidate_id,
        "candidate_aliases": aliases,
        "resolution": "absent_from_graph",
        "matches": [],
    }


def pull_evidence(session, node_id: str) -> dict:
    """Pull reuse evidence per the plan's Phase 2 query."""
    cypher = """
    MATCH (p {id: $id})
    OPTIONAL MATCH (p)-[:AUS_BAUWERK]->(b1)
    OPTIONAL MATCH (p)-[:EINGEBAUT_IN]->(b2)
    OPTIONAL MATCH (p)-[:HAT_WIEDERVERWENDUNGSART]->(wva)
    OPTIONAL MATCH (p)-[:HAT_METHODE]->(m)
    OPTIONAL MATCH (p)<-[:BELEGT_IN]-(q:Quelle)
    OPTIONAL MATCH (p)-[:HAT_AUFBEREITUNG]->(a)
    OPTIONAL MATCH (p)-[:HAT_PROZESSPHASE]->(ph)
    OPTIONAL MATCH (p)-[:NUTZT_BAUWERK]->(nb)
    OPTIONAL MATCH (p)-[:FROM_DONOR]->(fd)
    OPTIONAL MATCH (p)-[:INTO_RECEIVER]->(ir)
    OPTIONAL MATCH (p)-[:HAT_INTERVENTION]->(iv)
    OPTIONAL MATCH (p)-[:HAT_FUNKTIONSWECHSEL]->(fw)
    OPTIONAL MATCH (p)-[:TEIL_VON_PROGRAMM]->(prog)
    RETURN labels(p) AS labels, coalesce(p.status,'') AS status,
           coalesce(p.name,'') AS name, coalesce(p.aliases, []) AS aliases,
           collect(DISTINCT b1.id) AS donor_bauwerks,
           collect(DISTINCT b2.id) AS receiver_bauwerks,
           collect(DISTINCT wva.id) AS wva,
           collect(DISTINCT m.id)   AS methoden,
           collect(DISTINCT q.id)   AS quellen,
           collect(DISTINCT a.id)   AS aufbereitung,
           collect(DISTINCT ph.id)  AS prozessphasen,
           collect(DISTINCT nb.id)  AS nutzt_bauwerk,
           collect(DISTINCT fd.id)  AS from_donor,
           collect(DISTINCT ir.id)  AS into_receiver,
           collect(DISTINCT iv.id)  AS interventionen,
           collect(DISTINCT fw.id)  AS funktionswechsel,
           collect(DISTINCT prog.id) AS programme
    """
    row = session.run(cypher, id=node_id).single()
    if row is None:
        return {"id": node_id, "found": False}

    def _clean(xs):
        return [x for x in xs if x is not None]

    donor = _clean(row["donor_bauwerks"])
    receiver = _clean(row["receiver_bauwerks"])
    aufb = _clean(row["aufbereitung"])
    nb = _clean(row["nutzt_bauwerk"])
    wva = _clean(row["wva"])
    from_donor = _clean(row["from_donor"])
    into_receiver = _clean(row["into_receiver"])
    quellen = _clean(row["quellen"])

    reclaimed_proof = bool(
        (donor and receiver)
        or aufb
        or nb
        or wva
        or (from_donor and into_receiver)
    )

    return {
        "id": node_id,
        "found": True,
        "labels": list(row["labels"]),
        "name": row["name"],
        "status": row["status"],
        "aliases": list(row["aliases"]),
        "donor_bauwerks": donor,
        "receiver_bauwerks": receiver,
        "wva": wva,
        "methoden": _clean(row["methoden"]),
        "quellen": quellen,
        "aufbereitung": aufb,
        "prozessphasen": _clean(row["prozessphasen"]),
        "nutzt_bauwerk": nb,
        "from_donor": from_donor,
        "into_receiver": into_receiver,
        "interventionen": _clean(row["interventionen"]),
        "funktionswechsel": _clean(row["funktionswechsel"]),
        "programme": _clean(row["programme"]),
        "incoming_quellen_count": len(quellen),
        "reclaimed_proof": reclaimed_proof,
    }


def collect_status_inventory(session) -> dict:
    """Distinct status values currently seen on Projekt, Programm, Tool, Methode, Software, Marktmodell."""
    out: dict[str, list] = {}
    for lab in ("Projekt", "Programm", "Tool", "Methode", "Software", "Marktmodell"):
        result = session.run(
            f"MATCH (n:{lab}) WHERE n.status IS NOT NULL RETURN DISTINCT n.status AS status, count(*) AS c ORDER BY c DESC"
        )
        out[lab] = [{"status": r["status"], "count": r["c"]} for r in result]
    return out


def collect_duplicate_clusters(session) -> list[dict]:
    """Group :Projekt|:Programm|:Tool|:Methode|:Marktmodell nodes by normalised name key."""
    rows = list(
        session.run(
            "MATCH (n) WHERE 'Projekt' IN labels(n) OR 'Programm' IN labels(n) "
            "  OR 'Tool' IN labels(n) OR 'Methode' IN labels(n) OR 'Marktmodell' IN labels(n) "
            "RETURN n.id AS id, labels(n) AS labels, coalesce(n.name,'') AS name, "
            "       coalesce(n.aliases, []) AS aliases, "
            "       size([(n)<-[:BELEGT_IN]-() | 1]) AS belegt_in_count"
        )
    )
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        key = _norm_name(r["name"])
        if not key:
            continue
        buckets[key].append(
            {
                "id": r["id"],
                "labels": list(r["labels"]),
                "name": r["name"],
                "aliases": list(r["aliases"]),
                "belegt_in_count": r["belegt_in_count"],
            }
        )
    return [
        {"norm_key": k, "members": v}
        for k, v in sorted(buckets.items())
        if len(v) > 1
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--password-file", type=Path, default=Path(".neo4j_password"))
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    candidates = _load_candidates(args.candidates)
    if not candidates:
        print("No candidates parsed from YAML.", file=sys.stderr)
        return 1

    password = _read_password(args.password_file)
    if not password:
        print("NEO4J_PASSWORD not set; provide --password-file.", file=sys.stderr)
        return 1

    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("pip install -r requirements-neo4j.txt", file=sys.stderr)
        return 1

    uri = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
    user = os.environ.get("NEO4J_USER", "neo4j").strip()
    database = (os.environ.get("NEO4J_DATABASE") or "neo4j").strip() or "neo4j"

    resolution_path = args.out_dir / "resolution.jsonl"
    evidence_path = args.out_dir / "evidence.jsonl"
    status_path = args.out_dir / "status_inventory.json"
    dup_path = args.out_dir / "duplicate_clusters.json"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as sess:
            resolutions: list[dict] = []
            for entry in candidates:
                res = resolve_candidate(sess, entry)
                resolutions.append(res)

            evidence_rows: list[dict] = []
            for res in resolutions:
                if res["resolution"] != "exact":
                    continue
                for match in res["matches"]:
                    ev = pull_evidence(sess, match["id"])
                    ev["candidate_name"] = res["candidate_name"]
                    evidence_rows.append(ev)

            status_inventory = collect_status_inventory(sess)
            duplicate_clusters = collect_duplicate_clusters(sess)
    finally:
        driver.close()

    with resolution_path.open("w", encoding="utf-8") as fh:
        for row in resolutions:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    with evidence_path.open("w", encoding="utf-8") as fh:
        for row in evidence_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    status_path.write_text(
        json.dumps(
            {
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "database": database,
                "status_by_label": status_inventory,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    dup_path.write_text(
        json.dumps(
            {
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "database": database,
                "norm_regex": _NORM_RE.pattern,
                "clusters": duplicate_clusters,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {resolution_path}")
    print(f"Wrote {evidence_path}")
    print(f"Wrote {status_path}")
    print(f"Wrote {dup_path}")
    n_exact = sum(1 for r in resolutions if r["resolution"] == "exact")
    n_fuzzy = sum(1 for r in resolutions if r["resolution"] == "fuzzy_review_required")
    n_absent = sum(1 for r in resolutions if r["resolution"] == "absent_from_graph")
    print(f"Resolutions: exact={n_exact} fuzzy_review={n_fuzzy} absent={n_absent} total={len(resolutions)}")
    print(f"Evidence rows: {len(evidence_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
