"""Agent S4 - Quelle schema cleanup.

Run from repo root:
    python _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_s4_schema_cleanup/logs/agent_s4_runner.py
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
AGENT_DIR = THIS_FILE.parents[1]
RUN_DIR = AGENT_DIR.parent
REPO_ROOT = THIS_FILE.parents[6]

if str(REPO_ROOT / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402

MIG_DIR = AGENT_DIR / "migrations"
LOG_DIR = AGENT_DIR / "logs"
REPORT_DIR = AGENT_DIR / "reports"
S1_FLAG = RUN_DIR / "agent_s1_url_extractor" / "PHASE_S1_DONE.flag"
S1_RUNNER = RUN_DIR / "logs" / "agent_s1_runner.py"
R7A_AUDIT = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "runs"
    / "2026-05-21_review_based_plan"
    / "agent_5_loader_hardening"
    / "logs"
    / "r7a_audit.jsonl"
)

CANONICAL_PATHS = [
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "archive"
    / "2026-05-20_inbox_batch2_import"
    / "raw_tree",
    REPO_ROOT / "_archive" / "research" / "gebaeude",
]

DATA_ISSUE_CYPHER = """
MATCH (d:Dossier {id: $dossier_id})
MERGE (i:DataIssue {id: 'di_dossier_path_unresolvable__' + d.id})
ON CREATE SET
  i.kind = 'dossier_path_unresolvable',
  i.severity = 'medium',
  i.ref_label = 'Dossier',
  i.ref_id = d.id,
  i.found_at = date(),
  i.found_by = 's4_dossier_path_retry',
  i.status = 'open',
  i.resolution_note = 'Dossier .md file could not be resolved with exact, case-insensitive, or fuzzy matching. Provide explicit path.',
  i.migration_origin = 'mig_s4_c_fu8_retry'
ON MATCH SET
  i.status = coalesce(i.status, 'open'),
  i.migration_origin = coalesce(i.migration_origin, 'mig_s4_c_fu8_retry')
MERGE (i)-[:CONCERNS]->(d)
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def split_statements(cypher_text: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    for raw_line in cypher_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            current.append(line)
            continue
        current.append(line)
        if stripped.endswith(";"):
            stmt = "\n".join(current).strip()
            cleaned = "\n".join(
                ln for ln in stmt.splitlines() if not ln.strip().startswith("//")
            ).strip()
            if cleaned.endswith(";"):
                cleaned = cleaned[:-1].rstrip()
            if cleaned:
                statements.append(cleaned)
            current = []
    return statements


def run_cypher_file(session, filename: str, audit_fp) -> dict[str, Any]:
    statements = split_statements((MIG_DIR / filename).read_text(encoding="utf-8"))
    results: dict[str, Any] = {}
    for idx, stmt in enumerate(statements):
        t0 = datetime.now(timezone.utc)
        rows = [dict(r) for r in session.run(stmt)]
        elapsed_ms = (datetime.now(timezone.utc) - t0).total_seconds() * 1000
        payload = {
            "file": filename,
            "statement_index": idx,
            "elapsed_ms": elapsed_ms,
            "rows": rows[:50],
        }
        audit_fp.write(json.dumps(payload, default=str, ensure_ascii=False) + "\n")
        results[f"{filename}:{idx}"] = rows
        print(f"  {filename} [{idx + 1}/{len(statements)}] OK ({elapsed_ms:.0f} ms)")
    return results


def load_s1_module():
    spec = importlib.util.spec_from_file_location("agent_s1_runner", S1_RUNNER)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot import S1 runner from {S1_RUNNER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalized_stem(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for base in CANONICAL_PATHS:
        if base.is_dir():
            files.extend([p for p in base.rglob("*") if p.is_file() and p.suffix.lower() == ".md"])
    return sorted(set(files), key=lambda p: str(p).lower())


def fuzzy_pick(slug: str, files: list[Path]) -> tuple[Path | None, float]:
    try:
        from rapidfuzz import process  # type: ignore

        choices = [f.stem for f in files]
        result = process.extractOne(slug, choices, score_cutoff=85)
        if result:
            match, score, _ = result
            for f in files:
                if f.stem == match:
                    return f, float(score)
    except Exception:
        pass

    best_file: Path | None = None
    best_score = 0.0
    norm_slug = normalized_stem(slug)
    for f in files:
        score = SequenceMatcher(None, norm_slug, normalized_stem(f.stem)).ratio() * 100
        if score > best_score:
            best_file = f
            best_score = score
    if best_file is not None and best_score >= 85:
        return best_file, best_score
    return None, best_score


def retry_resolve_dossier_path(dossier_id: str) -> tuple[Path | None, str, float | None]:
    slug = dossier_id
    if slug.startswith("q_"):
        slug = slug[2:]
    if slug.endswith("_md"):
        slug = slug[:-3]

    for base in CANONICAL_PATHS:
        for ext in [".md", ".MD"]:
            candidate = base / f"{slug}{ext}"
            if candidate.exists():
                return candidate, "exact", None

    files = iter_markdown_files()
    for f in files:
        if f.stem.lower() == slug.lower():
            return f, "case_insensitive", None

    norm_slug = normalized_stem(slug)
    for f in files:
        if normalized_stem(f.stem) == norm_slug:
            return f, "normalized_stem", None

    match, score = fuzzy_pick(slug, files)
    if match:
        return match, "fuzzy_85", score

    return None, "unresolved", score


def extract_for_dossier(session, s1, dossier_id: str, text: str) -> int:
    inserted = 0

    for label, raw_url in s1.extract_md_links(text):
        norm = s1.normalise_url(raw_url)
        if not norm:
            continue
        ext_id = s1.url_id(norm)
        surr = s1.surrounding_text(text, raw_url)[:240]
        session.run(
            s1.S1_A,
            ext_id=ext_id,
            url=norm,
            title=label,
            url_origin="dossier_md_link",
            first_seen_in_dossier=dossier_id,
            evidence_basis="markdown_link_extraction",
            source_id=dossier_id,
        ).consume()
        session.run(
            s1.S1_B,
            source_id=dossier_id,
            ext_id=ext_id,
            locator="S1",
            evidence_basis="markdown_link_extraction",
            surrounding_text=surr,
        ).consume()
        inserted += 1

    for raw_url in s1.extract_bare_urls(text):
        norm = s1.normalise_url(raw_url)
        if not norm:
            continue
        ext_id = s1.url_id(norm)
        surr = s1.surrounding_text(text, raw_url)[:240]
        session.run(
            s1.S1_A,
            ext_id=ext_id,
            url=norm,
            title="",
            url_origin="dossier_bare_url",
            first_seen_in_dossier=dossier_id,
            evidence_basis="bare_url_extraction",
            source_id=dossier_id,
        ).consume()
        session.run(
            s1.S1_B,
            source_id=dossier_id,
            ext_id=ext_id,
            locator="bare",
            evidence_basis="bare_url_extraction",
            surrounding_text=surr,
        ).consume()
        inserted += 1

    return inserted


def known_r7_alias_pairs() -> dict[str, str]:
    pairs: dict[str, str] = {}
    if not R7A_AUDIT.is_file():
        return pairs
    for line in R7A_AUDIT.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if item.get("status") == "merged" and item.get("old") and item.get("new"):
            pairs[str(item["new"])] = str(item["old"])
    return pairs


def repair_known_aliases(session) -> list[dict[str, str]]:
    fixed: list[dict[str, str]] = []
    for dossier_id, expected_alias in known_r7_alias_pairs().items():
        row = session.run(
            """
            MATCH (d:Dossier {id: $dossier_id})
            RETURN d.id AS id, coalesce(d.aliases, []) AS aliases
            """,
            dossier_id=dossier_id,
        ).single()
        if not row:
            continue
        if expected_alias in (row["aliases"] or []):
            continue
        session.run(
            """
            MATCH (d:Dossier {id: $dossier_id})
            SET d.aliases = apoc.coll.toSet(coalesce(d.aliases, []) + [$expected_alias]),
                d.migration_origin = coalesce(d.migration_origin, '') +
                    CASE WHEN d.migration_origin IS NULL OR d.migration_origin = ''
                         THEN 'mig_s4_d_alias_sanity'
                         ELSE ' | mig_s4_d_alias_sanity' END
            """,
            dossier_id=dossier_id,
            expected_alias=expected_alias,
        ).consume()
        fixed.append({"dossier_id": dossier_id, "expected_alias": expected_alias})
    return fixed


def collect_acceptance(session) -> dict[str, Any]:
    queries = {
        "dossier_count": "MATCH (d:Dossier) RETURN count(d) AS c",
        "external_link_count": "MATCH (e:ExternalLink) RETURN count(e) AS c",
        "research_document_count": "MATCH (r:ResearchDocument) RETURN count(r) AS c",
        "section_ref_count": "MATCH (s:SectionRef) RETURN count(s) AS c",
        "untyped_quelle": (
            "MATCH (q:Quelle) "
            "WHERE NOT (q:Dossier OR q:ExternalLink OR q:ResearchDocument OR q:SectionRef OR q:OntologyAnchor) "
            "RETURN count(q) AS c"
        ),
        "dossier_with_text_content": (
            "MATCH (d:Dossier) WHERE d.text_content IS NOT NULL RETURN count(d) AS c"
        ),
        "dossier_with_pre_strip_chars": (
            "MATCH (d:Dossier) WHERE d.text_content_chars_pre_strip IS NOT NULL RETURN count(d) AS c"
        ),
        "total_chars_stripped": (
            "MATCH (d:Dossier) WHERE d.text_content_chars_pre_strip IS NOT NULL "
            "RETURN coalesce(sum(d.text_content_chars_pre_strip), 0) AS c"
        ),
        "fu8_data_issues": (
            "MATCH (i:DataIssue {kind:'dossier_path_unresolvable'}) RETURN count(i) AS c"
        ),
        "known_qu_aliases": (
            "MATCH (d:Dossier) WHERE d.aliases IS NOT NULL "
            "AND any(a IN d.aliases WHERE a STARTS WITH 'qu_' AND a ENDS WITH '_dossier') "
            "RETURN count(d) AS c"
        ),
    }
    out: dict[str, Any] = {}
    for key, query in queries.items():
        out[key] = session.run(query).single()["c"]
    return out


def run_s4() -> dict[str, Any]:
    if not S1_FLAG.is_file():
        raise SystemExit(f"S1 done flag missing: {S1_FLAG}")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    uri, user, password, database = resolve_connection()
    database = database or "mit-bestand"
    driver = GraphDatabase.driver(
        uri,
        auth=(user, password),
        notifications_disabled_categories=["DEPRECATION", "UNRECOGNIZED"],
    )

    s1 = load_s1_module()
    audit_path = LOG_DIR / "s4_audit.jsonl"
    fu8_log_path = LOG_DIR / "fu8_retry_results.jsonl"

    summary: dict[str, Any] = {
        "started_at_utc": utc_now(),
        "database": database,
        "fu8_resolved": 0,
        "fu8_unresolved": 0,
        "fu8_url_records_reextracted": 0,
        "alias_repairs": [],
        "acceptance": {},
    }

    with driver.session(database=database) as session, audit_path.open("w", encoding="utf-8") as audit_fp:
        print("S4.A secondary labels")
        summary["secondary_label_results"] = run_cypher_file(
            session, "mig_s4_a_secondary_labels.cypher", audit_fp
        )

        unresolved = session.run(
            "MATCH (d:Dossier) WHERE d.text_content IS NULL RETURN d.id AS id ORDER BY d.id"
        ).data()

        print(f"S4.C FU-8 retry candidates: {len(unresolved)}")
        with fu8_log_path.open("w", encoding="utf-8") as fu8_fp:
            for row in unresolved:
                dossier_id = row["id"]
                path, method, score = retry_resolve_dossier_path(dossier_id)
                if path:
                    text = path.read_text(encoding="utf-8")
                    session.run(
                        """
                        MATCH (d:Dossier {id: $id})
                        SET d.text_content = $text,
                            d.text_content_retry_attempted_at = date(),
                            d.text_content_retry_result = 'resolved',
                            d.migration_origin = coalesce(d.migration_origin, '') +
                                CASE WHEN d.migration_origin IS NULL OR d.migration_origin = ''
                                     THEN 'mig_s4_c_fu8_retry'
                                     ELSE ' | mig_s4_c_fu8_retry' END
                        """,
                        id=dossier_id,
                        text=text,
                    ).consume()
                    url_records = extract_for_dossier(session, s1, dossier_id, text)
                    summary["fu8_resolved"] += 1
                    summary["fu8_url_records_reextracted"] += url_records
                    payload = {
                        "dossier_id": dossier_id,
                        "result": "resolved",
                        "method": method,
                        "score": score,
                        "path": str(path.relative_to(REPO_ROOT)),
                        "chars": len(text),
                        "url_records_reextracted": url_records,
                    }
                    print(f"  resolved {dossier_id} via {method}: {payload['path']} ({url_records} URLs)")
                else:
                    session.run(
                        """
                        MATCH (d:Dossier {id: $id})
                        SET d.text_content_retry_attempted_at = date(),
                            d.text_content_retry_result = 'unresolved',
                            d.migration_origin = coalesce(d.migration_origin, '') +
                                CASE WHEN d.migration_origin IS NULL OR d.migration_origin = ''
                                     THEN 'mig_s4_c_fu8_retry'
                                     ELSE ' | mig_s4_c_fu8_retry' END
                        """,
                        id=dossier_id,
                    ).consume()
                    session.run(DATA_ISSUE_CYPHER, dossier_id=dossier_id).consume()
                    summary["fu8_unresolved"] += 1
                    payload = {
                        "dossier_id": dossier_id,
                        "result": "unresolved",
                        "method": method,
                        "score": score,
                    }
                    print(f"  unresolved {dossier_id}")
                fu8_fp.write(json.dumps(payload, default=str, ensure_ascii=False) + "\n")

        gate = session.run(
            """
            MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
              AND NOT exists{(d)-[:ZITIERT_QUELLE]->(:ExternalLink)}
            RETURN count(d) AS violations, collect(d.id)[..20] AS sample
            """
        ).single()
        summary["pre_strip_gate"] = dict(gate)
        if gate["violations"] > 0:
            raise RuntimeError(
                f"Strip aborted: {gate['violations']} dossiers have text but no extracted URLs: "
                f"{gate['sample']}"
            )

        print("S4.B text_content strip")
        summary["text_strip_results"] = run_cypher_file(
            session, "mig_s4_b_text_strip.cypher", audit_fp
        )

        print("S4.D alias sanity")
        summary["alias_repairs"] = repair_known_aliases(session)
        summary["alias_audit_results"] = run_cypher_file(
            session, "mig_s4_d_alias_sanity.cypher", audit_fp
        )

        summary["acceptance"] = collect_acceptance(session)

    summary["completed_at_utc"] = utc_now()
    summary["verified"] = (
        summary["acceptance"]["dossier_count"] == 100
        and summary["acceptance"]["untyped_quelle"] <= 5
        and summary["acceptance"]["dossier_with_text_content"] == 0
        and summary["acceptance"]["dossier_with_pre_strip_chars"] >= 95
        and summary["acceptance"]["total_chars_stripped"] >= 2_000_000
        and summary["fu8_unresolved"] <= 5
    )

    report_path = REPORT_DIR / "agent_s4_report.md"
    report_path.write_text(render_report(summary), encoding="utf-8")
    (AGENT_DIR / "S4_REPORT.json").write_text(
        json.dumps(summary, indent=2, default=str, ensure_ascii=False),
        encoding="utf-8",
    )
    (AGENT_DIR / "PHASE_S4_DONE.flag").write_text(
        json.dumps(
            {
                "phase": "S4",
                "agent": "agent_s4_schema_cleanup",
                "completed_at_utc": summary["completed_at_utc"],
                "verified": summary["verified"],
                "report": str(report_path.relative_to(REPO_ROOT)),
                "acceptance": summary["acceptance"],
            },
            indent=2,
            default=str,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    driver.close()
    return summary


def render_report(summary: dict[str, Any]) -> str:
    acc = summary["acceptance"]
    alias_repairs = summary.get("alias_repairs", [])
    return "\n".join(
        [
            "# Agent S4 schema cleanup report",
            "",
            f"Completed UTC: {summary.get('completed_at_utc')}",
            f"Database: {summary.get('database')}",
            f"Verified: {summary.get('verified')}",
            "",
            "## Summary",
            "",
            f"- Dossier labels: {acc.get('dossier_count')}",
            f"- ExternalLink labels: {acc.get('external_link_count')}",
            f"- ResearchDocument labels: {acc.get('research_document_count')}",
            f"- SectionRef labels: {acc.get('section_ref_count')}",
            f"- Untyped Quelle residual: {acc.get('untyped_quelle')}",
            f"- FU-8 resolved: {summary.get('fu8_resolved')}",
            f"- FU-8 unresolved: {summary.get('fu8_unresolved')}",
            f"- FU-8 URL records re-extracted: {summary.get('fu8_url_records_reextracted')}",
            f"- Dossiers with text_content remaining: {acc.get('dossier_with_text_content')}",
            f"- Dossiers with pre-strip chars: {acc.get('dossier_with_pre_strip_chars')}",
            f"- Total chars stripped: {acc.get('total_chars_stripped')}",
            f"- DataIssue dossier_path_unresolvable: {acc.get('fu8_data_issues')}",
            f"- Known R7.a qu_* aliases present: {acc.get('known_qu_aliases')}",
            f"- Alias repairs applied: {len(alias_repairs)}",
            "",
            "## Logs",
            "",
            "- logs/s4_audit.jsonl",
            "- logs/fu8_retry_results.jsonl",
            "- S4_REPORT.json",
            "",
        ]
    )


def main() -> int:
    summary = run_s4()
    print(json.dumps(summary["acceptance"], indent=2, default=str, ensure_ascii=False))
    return 0 if summary["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
