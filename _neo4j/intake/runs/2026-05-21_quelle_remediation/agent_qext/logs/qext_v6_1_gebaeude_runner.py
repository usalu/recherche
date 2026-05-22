"""Q-EXT v6.1 gebaeude importer.

Imports the measured per-row source triples emitted by unfold_all_gebaeude.py.
The importer deliberately does not auto-merge raw dossier names into existing
domain nodes by fuzzy name similarity. Instead, each raw (entity_type,
entity_value) target becomes a DossierEntityTarget node, and exact graph-node
matches are recorded as reviewable candidates.

Run from repo root:
    python _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/qext_v6_1_gebaeude_runner.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[6]
LOG_DIR = RUN_DIR / "logs"
REPORT_DIR = RUN_DIR / "reports"
TRIPLES_PATH = LOG_DIR / "unfold_all_gebaeude_triples.jsonl"
SUMMARY_PATH = LOG_DIR / "unfold_all_gebaeude_summary.json"
REPORT_JSON = REPORT_DIR / "qext_v6_1_gebaeude_import_report.json"
REPORT_MD = REPORT_DIR / "qext_v6_1_gebaeude_import_report.md"
FLAG_PATH = RUN_DIR / "PHASE_QEXT_V6_1_GEBAEUDE_DONE.flag"

sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


LABEL_CANDIDATES = {
    "Fallstudie": ["Projekt"],
    "Projekt": ["Projekt"],
    "Gebäude": ["Bauwerk"],
    "GebÃ¤ude": ["Bauwerk"],
    "People": ["Akteur"],
    "Bauherr": ["Akteur"],
    "Architekt": ["Akteur"],
    "Tragwerksplaner": ["Akteur"],
    "Ort": ["Stadt", "Land"],
    "Material": ["Material"],
    "Bauteil": ["Bauteilgruppe", "Bauteiltyp"],
    "bauteil": ["Bauteilgruppe", "Bauteiltyp"],
    "Hürde": ["Huerde"],
    "HÃ¼rde": ["Huerde"],
    "huerde": ["Huerde"],
    "Kennwert": ["Kennwert"],
    "kennwert": ["Kennwert"],
    "Prozessphase": ["Prozessphase"],
    "prozessphase": ["Prozessphase"],
    "Reuse-Strategie": ["Wiederverwendungsart"],
    "Methode": ["Methode"],
    "Logistik": ["Logistik"],
    "Prüfung": ["PruefungNachweis"],
    "PrÃ¼fung": ["PruefungNachweis"],
    "Norm": ["Norm"],
    "Norm/Recht": ["Norm", "RechtlicheBedingung"],
    "Recht": ["RechtlicheBedingung"],
    "Software": ["Software"],
    "Tool": ["Software"],
    "thema": [
        "Material",
        "Norm",
        "Methode",
        "PruefungNachweis",
        "Leistungsanforderung",
        "Bauweise",
        "Bausystem",
        "Tragwerkssystem",
    ],
}

INDEX_DENYLIST_LABELS = {
    "DossierEntityTarget",
    "Quelle",
    "Dossier",
    "ExternalLink",
    "UrlMetadata",
    "ResearchDocument",
    "SectionRef",
    "DataIssue",
    "OntologyAnchor",
    "GraphVersion",
    "DeprecatedType",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_hash(*parts: object) -> str:
    raw = "\n".join("" if p is None else str(p) for p in parts)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:24]


def norm_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("ß", "ss")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def section_slug(section: str) -> str:
    cleaned = unicodedata.normalize("NFKD", section)
    cleaned = "".join(ch for ch in cleaned if not unicodedata.combining(ch))
    cleaned = cleaned.upper()
    cleaned = re.sub(r"^\s*(\d+)\.\s*", r"\1.", cleaned)
    cleaned = re.sub(r"[^A-Z0-9.]+", "-", cleaned).strip("-")
    return cleaned[:80]


def make_locator(row: dict) -> str:
    sec = section_slug(row["section"])
    value = str(row["entity_value"]).replace("\n", " ").strip()
    value = re.sub(r"\s+", " ", value)[:80]
    if row.get("kind") == "entity_value":
        return (
            f"sec:{sec}/row:{row['row_idx']}/"
            f"typ:{row['entity_type']}/val:{value}"
        )
    return f"sec:{sec}/row:{row['row_idx']}/col:{row['kind']}:{value}"


def read_triples() -> list[dict]:
    if not TRIPLES_PATH.is_file():
        raise SystemExit(f"Missing triples file: {TRIPLES_PATH}")
    triples: list[dict] = []
    with TRIPLES_PATH.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                triples.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Bad JSON on line {lineno}: {exc}") from exc
    return triples


def build_node_index(session) -> dict[str, list[dict]]:
    index: dict[str, list[dict]] = defaultdict(list)
    rows = session.run(
        "MATCH (n) WHERE n.id IS NOT NULL "
        "WITH n, labels(n) AS labels "
        "WHERE none(label IN labels WHERE label IN $deny) "
        "RETURN n.id AS id, labels AS labels, n.name AS name, "
        "       n.raw_name AS raw_name, coalesce(n.aliases, []) AS aliases"
        ,
        deny=list(INDEX_DENYLIST_LABELS),
    )
    for row in rows:
        values = [row["id"], row["name"], row["raw_name"], *(row["aliases"] or [])]
        for value in values:
            key = norm_text(value)
            if key:
                index[key].append(
                    {
                        "id": row["id"],
                        "labels": list(row["labels"] or []),
                        "name": row["name"],
                    }
                )
    return index


def build_url_metadata(session) -> dict[str, dict]:
    metadata: dict[str, dict] = {}
    rows = session.run(
        "MATCH (u) WHERE (u:ExternalLink OR u:UrlMetadata) AND u.url IS NOT NULL "
        "RETURN u.url AS url, u.url_status AS status, "
        "       u.url_http_code AS http_code, "
        "       u.url_wayback_snapshot AS wayback, "
        "       u.url_last_checked_at AS checked"
    )
    for row in rows:
        url = row["url"]
        if not url or url in metadata:
            continue
        checked = row["checked"]
        if hasattr(checked, "iso_format"):
            checked = checked.iso_format()
        metadata[url] = {
            "source_url_status": row["status"],
            "source_url_http_code": row["http_code"],
            "source_url_wayback_snapshot": row["wayback"],
            "source_url_last_checked_at": checked,
        }
    return metadata


def exact_candidates(index: dict[str, list[dict]], entity_type: str, value: str) -> list[dict]:
    candidates = index.get(norm_text(value), [])
    allowed = LABEL_CANDIDATES.get(entity_type)
    if allowed:
        candidates = [
            c for c in candidates if any(label in allowed for label in c["labels"])
        ]
    seen: set[str] = set()
    deduped: list[dict] = []
    for candidate in candidates:
        if candidate["id"] in seen:
            continue
        seen.add(candidate["id"])
        deduped.append(candidate)
    return deduped


def prepare_rows(triples: list[dict], index: dict[str, list[dict]], url_meta: dict[str, dict]) -> tuple[list[dict], dict]:
    target_candidates: dict[str, list[dict]] = {}
    target_stats = Counter()
    rows: list[dict] = []
    seen_rel_ids: set[str] = set()

    for triple in triples:
        entity_type = str(triple["entity_type"])
        entity_value = str(triple["entity_value"])
        # Key raw dossier targets by the exact raw value, not by a normalised
        # form. Normalisation is only used for candidate lookup; it must not
        # silently collapse distinct dossier strings into one target node.
        target_id = "det_" + stable_hash(entity_type, entity_value)
        if target_id not in target_candidates:
            candidates = exact_candidates(index, entity_type, entity_value)
            target_candidates[target_id] = candidates
            if len(candidates) == 1:
                target_stats["exact_unique"] += 1
            elif len(candidates) > 1:
                target_stats["exact_ambiguous"] += 1
            else:
                target_stats["unresolved"] += 1
        else:
            candidates = target_candidates[target_id]

        if len(candidates) == 1:
            review_status = "exact_unique_candidate"
            match_node_id = candidates[0]["id"]
            match_label = next(
                (label for label in candidates[0]["labels"] if label not in {"Quelle"}),
                candidates[0]["labels"][0] if candidates[0]["labels"] else None,
            )
        elif len(candidates) > 1:
            review_status = "exact_ambiguous_candidates"
            match_node_id = None
            match_label = None
        else:
            review_status = "unresolved_no_exact_match"
            match_node_id = None
            match_label = None

        dossier_file_id = str(triple["dossier_id"])
        dossier_node_id = f"q_{dossier_file_id}_md"
        locator = make_locator(triple)
        source_url = str(triple["url"])
        rel_id = "r_qext_v6_1_" + stable_hash(
            target_id,
            dossier_node_id,
            locator,
            source_url,
            triple.get("sref"),
        )
        if rel_id in seen_rel_ids:
            continue
        seen_rel_ids.add(rel_id)

        rel_props = {
            "id": rel_id,
            "dossier_id": dossier_node_id,
            "dossier_file_id": dossier_file_id,
            "locator": locator,
            "section": triple["section"],
            "row_idx": int(triple["row_idx"]),
            "source_url": source_url,
            "source_url_title": triple.get("url_title"),
            "citation_ref": triple.get("sref"),
            "entity_type": entity_type,
            "entity_value": entity_value,
            "entity_kind": triple.get("kind"),
            "unfolding_kind": "dossier_row",
            "unfolding_origin": f"{dossier_node_id}/{locator}",
            "provenance_kind": "dossier_row + external_url",
            "review_status": review_status,
            "merge_policy": "raw_target_no_name_similarity_merge",
            "migration_origin": "qext_v6_1_gebaeude_unfolder",
            "imported_at_utc": utc_now(),
        }
        rel_props.update({k: v for k, v in url_meta.get(source_url, {}).items() if v is not None})

        rows.append(
            {
                "target_id": target_id,
                "target_props": {
                    "id": target_id,
                    "name": entity_value,
                    "entity_type": entity_type,
                    "entity_value": entity_value,
                    "entity_value_norm": norm_text(entity_value),
                    "source_scope": "dossier_entity_target",
                    "review_status": review_status,
                    "exact_match_node_id": match_node_id,
                    "exact_match_label": match_label,
                    "exact_match_candidate_ids": [c["id"] for c in candidates[:25]],
                    "unfolding_kind": "dossier_row",
                    "unfolding_origin": "qext_v6_1_gebaeude_unfolder",
                    "migration_origin": "qext_v6_1_gebaeude_unfolder",
                    "created_at_utc": utc_now(),
                },
                "dossier_node_id": dossier_node_id,
                "dossier_name": dossier_file_id + ".md",
                "rel_id": rel_id,
                "rel_props": rel_props,
                "match_node_id": match_node_id,
            }
        )

    stats = {
        "distinct_targets": len(target_candidates),
        **target_stats,
        "prepared_relationships": len(rows),
    }
    return rows, stats


WRITE_CITATIONS = """
UNWIND $rows AS row
MERGE (target:DossierEntityTarget {id: row.target_id})
SET target += row.target_props
MERGE (d:Quelle:Dossier {id: row.dossier_node_id})
ON CREATE SET
  d.name = row.dossier_name,
  d.quelltyp = 'case_markdown',
  d.source_scope = 'dossier',
  d.migration_origin = 'qext_v6_1_gebaeude_unfolder'
MERGE (target)-[r:CITED_FROM_DOSSIER {id: row.rel_id}]->(d)
SET r += row.rel_props
RETURN count(r) AS written
"""


WRITE_EXACT_LINKS = """
UNWIND $rows AS row
MATCH (target:DossierEntityTarget {id: row.target_id})
MATCH (n {id: row.match_node_id})
MERGE (target)-[r:EXACT_MATCH_CANDIDATE {
  id: 'r_qext_v6_1_exact__' + row.target_id + '__' + row.match_node_id
}]->(n)
SET r.review_status = 'candidate_exact_unique',
    r.match_basis = 'normalized_exact_entity_value',
    r.merge_policy = 'candidate_only_no_auto_merge',
    r.migration_origin = 'qext_v6_1_gebaeude_unfolder',
    r.unfolding_kind = 'dossier_row',
    r.unfolding_origin = 'qext_v6_1_gebaeude_unfolder'
RETURN count(r) AS written
"""


AUDIT_QUERY = """
MATCH (:DossierEntityTarget)-[r:CITED_FROM_DOSSIER]->(:Dossier)
WHERE r.migration_origin = 'qext_v6_1_gebaeude_unfolder'
RETURN count(r) AS cited_edges,
       count(DISTINCT r.source_url) AS distinct_urls,
       count(DISTINCT r.dossier_id) AS dossiers,
       count(DISTINCT r.entity_type + '\\u001f' + r.entity_value) AS distinct_targets
"""


def chunks(rows: list[dict], size: int) -> list[list[dict]]:
    return [rows[i : i + size] for i in range(0, len(rows), size)]


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    triples = read_triples()
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8")) if SUMMARY_PATH.is_file() else {}
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()

    try:
        with driver.session(database=database) as session:
            print("[1/4] Building exact node index...")
            index = build_node_index(session)
            url_meta = build_url_metadata(session)

            print("[2/4] Preparing import rows...")
            rows, stats = prepare_rows(triples, index, url_meta)

            print(f"[3/4] Writing {len(rows)} CITED_FROM_DOSSIER edges...")
            written = 0
            for chunk in chunks(rows, 500):
                rec = session.run(WRITE_CITATIONS, rows=chunk).single()
                written += rec["written"] if rec else 0

            exact_seen: set[tuple[str, str]] = set()
            exact_rows = []
            for row in rows:
                if not row.get("match_node_id"):
                    continue
                key = (row["target_id"], row["match_node_id"])
                if key in exact_seen:
                    continue
                exact_seen.add(key)
                exact_rows.append(row)
            exact_written = 0
            for chunk in chunks(exact_rows, 500):
                rec = session.run(WRITE_EXACT_LINKS, rows=chunk).single()
                exact_written += rec["written"] if rec else 0

            print("[4/4] Auditing import...")
            audit = dict(session.run(AUDIT_QUERY).single())
            by_status = session.run(
                "MATCH (t:DossierEntityTarget) "
                "WHERE t.migration_origin = 'qext_v6_1_gebaeude_unfolder' "
                "RETURN t.review_status AS status, count(t) AS count "
                "ORDER BY count DESC"
            ).data()
            by_entity_type = session.run(
                "MATCH (:DossierEntityTarget)-[r:CITED_FROM_DOSSIER]->(:Dossier) "
                "WHERE r.migration_origin = 'qext_v6_1_gebaeude_unfolder' "
                "RETURN r.entity_type AS entity_type, count(r) AS edges "
                "ORDER BY edges DESC LIMIT 30"
            ).data()
    finally:
        driver.close()

    report = {
        "completed_at_utc": utc_now(),
        "database": database,
        "input_triples_file": str(TRIPLES_PATH.relative_to(REPO_ROOT)),
        "input_summary_grand_total": summary.get("grand_total_triples"),
        "input_summary_distinct_urls": summary.get("distinct_urls"),
        "input_summary_distinct_entities": summary.get("distinct_entities"),
        "prepared": stats,
        "written_edges_returned": written,
        "exact_candidate_relationships_returned": exact_written,
        "audit": audit,
        "target_review_status": by_status,
        "top_entity_types": by_entity_type,
        "baseline_note": (
            "_scripts/_gap_survey.py had pre-existing FAIL rows before this "
            "import; see run transcript."
        ),
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    status_lines = "\n".join(
        f"- {row['status']}: {row['count']}" for row in by_status
    )
    type_lines = "\n".join(
        f"- {row['entity_type']}: {row['edges']}" for row in by_entity_type[:15]
    )
    REPORT_MD.write_text(
        f"""# Q-EXT v6.1 gebaeude import report

Completed UTC: {report['completed_at_utc']}
Database: {database}

## Result

- Input triples: {len(triples)}
- `:CITED_FROM_DOSSIER` edges in this migration: {audit.get('cited_edges')}
- Distinct URLs: {audit.get('distinct_urls')}
- Distinct dossiers: {audit.get('dossiers')}
- Distinct raw targets: {audit.get('distinct_targets')}
- Exact-match candidate relationships: {exact_written}

## Target review status

{status_lines}

## Top entity types

{type_lines}

## Files

- `{TRIPLES_PATH.relative_to(REPO_ROOT)}`
- `{REPORT_JSON.relative_to(REPO_ROOT)}`
""",
        encoding="utf-8",
    )

    FLAG_PATH.write_text(
        json.dumps(
            {
                "phase": "Q-EXT v6.1 gebaeude",
                "completed_at_utc": report["completed_at_utc"],
                "cited_edges": audit.get("cited_edges"),
                "distinct_urls": audit.get("distinct_urls"),
                "distinct_targets": audit.get("distinct_targets"),
                "report": str(REPORT_JSON.relative_to(REPO_ROOT)),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(json.dumps(report["audit"], indent=2, ensure_ascii=False, default=str))
    print(f"Report: {REPORT_JSON.relative_to(REPO_ROOT)}")
    print(f"Flag:   {FLAG_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
