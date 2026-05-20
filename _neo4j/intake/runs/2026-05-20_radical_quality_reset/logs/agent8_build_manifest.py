"""Agent 8 — build Phase 4c.2 dossier manifest.

For Agent 9 / 10 (Phase 4b loader). Lists every dossier markdown file that
the loader should parse for the source-as-link contract (§4c.2):
  - 76 files under _archive/research/gebaeude/*.md  (German narrative format,
    sources block as section 13 "## Quellen und Links")
  - 21 files under _neo4j/intake/archive/2026-05-20_inbox_batch2_import/
    raw_tree/**/*.md  (English structured tables with inline [S\d](url)
    citations). One of these (`batch 1.md`) is actually a multi-dossier
    concatenation of 3 dossiers — flagged for Agent 9.

For every file we capture:
  - relative path (POSIX-style, from repo root)
  - absolute path (Windows-style)
  - file size in bytes
  - file mtime (UTC ISO)
  - SHA1 of contents (so Agent 9 can detect drift)
  - corpus tag ('gebaeude' | 'batch2')
  - format hint ('case_markdown' | 'case_markdown_multi')
  - inferred q_<slug>_md id (matches Agent 6 / Phase-1 case_markdown convention)
  - quelle_id_live: matched against the live :Quelle.id (case_markdown) if
    one exists; null otherwise (means Agent 9 must MERGE-create one)
  - sources_block_offset: byte offset of the first "## Quellen" or "## Sources"
    section if present (so Agent 9 can stream-parse without reloading)
  - sources_block_kind: 'quellen_und_links' | 'sources' | None
  - inline_url_hits: number of `https?://` occurrences in the file
  - sref_inline_hits: number of "[S\d+]" or "[S\d+](url)" matches
    (rough upper bound on S-ref slots Agent 9 must MERGE into ZITIERT_QUELLE)

The manifest is NOT a parse of full dossier content — Agent 9 / 10 own
that. Agent 8 only stubs the work.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(r"E:/recherche")
GEBAEUDE_DIR = REPO_ROOT / "_archive" / "research" / "gebaeude"
BATCH2_ROOT = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "archive"
    / "2026-05-20_inbox_batch2_import"
    / "raw_tree"
)
OUT_PATH = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "runs"
    / "2026-05-20_radical_quality_reset"
    / "reports"
    / "agent_8_dossier_manifest.json"
)

SLUG_RE = re.compile(r"[^a-z0-9]+")
URL_RE = re.compile(r"https?://", re.IGNORECASE)
SREF_RE = re.compile(r"\[S\d+\]")
HEADER_QUELLEN_RE = re.compile(
    r"^##+\s+(\d+\.\s+)?Quellen(?:\s+und\s+Links)?\s*$",
    re.IGNORECASE | re.MULTILINE,
)
HEADER_SOURCES_RE = re.compile(
    r"^##+\s+(\d+\.\s+)?Sources(?:\s+and\s+links)?\s*$",
    re.IGNORECASE | re.MULTILINE,
)
H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def slugify_filename(stem: str) -> str:
    """Replicate the q_<slug>_md convention used for case_markdown Quelle.

    Examples observed in the live graph:
      Holbein_Gardens_London.md -> q_holbein_gardens_london_md
      55_Great_Suffolk_Street_London.md -> q_55_great_suffolk_street_london_md
    """
    s = stem.lower()
    s = SLUG_RE.sub("_", s).strip("_")
    return f"q_{s}_md"


def _resolve_connection() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, password, database = resolve_connection()
    if database != "mit-bestand":
        database = "mit-bestand"
    return uri, user, password, database


def load_live_quelle_ids() -> set[str]:
    from neo4j import GraphDatabase  # type: ignore

    uri, user, password, database = _resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session(database=database) as s:
            return {
                r["id"] for r in s.run(
                    "MATCH (q:Quelle) WHERE q.quelltyp = 'case_markdown' RETURN q.id AS id"
                )
            }
    finally:
        driver.close()


def file_summary(path: Path, corpus: str, live_ids: set[str]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    sha1 = hashlib.sha1(text.encode("utf-8", errors="replace")).hexdigest()
    rel = path.relative_to(REPO_ROOT).as_posix()
    stem = path.stem
    qid = slugify_filename(stem)
    h1_titles = H1_RE.findall(text)
    multi = len(h1_titles) > 1
    block_kind: str | None = None
    block_offset: int | None = None
    m = HEADER_QUELLEN_RE.search(text)
    if m:
        block_kind = "quellen_und_links"
        block_offset = m.start()
    else:
        m2 = HEADER_SOURCES_RE.search(text)
        if m2:
            block_kind = "sources"
            block_offset = m2.start()
    inline_urls = len(URL_RE.findall(text))
    sref_inline = len(SREF_RE.findall(text))
    return {
        "rel_path": rel,
        "abs_path": str(path),
        "size_bytes": path.stat().st_size,
        "mtime_utc": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(timespec="seconds"),
        "sha1": sha1,
        "corpus": corpus,
        "format_hint": "case_markdown_multi" if multi else "case_markdown",
        "h1_titles": h1_titles,
        "expected_quelle_id": qid,
        "live_quelle_id": qid if qid in live_ids else None,
        "sources_block_kind": block_kind,
        "sources_block_offset": block_offset,
        "inline_url_count": inline_urls,
        "sref_inline_count": sref_inline,
    }


def main() -> int:
    try:
        live_ids = load_live_quelle_ids()
    except Exception as exc:
        print(f"WARN: could not load live Quelle ids: {exc}; "
              "live_quelle_id will be null for every entry", file=sys.stderr)
        live_ids = set()

    gebaeude_files = sorted(GEBAEUDE_DIR.glob("*.md"))
    batch2_files = sorted(BATCH2_ROOT.rglob("*.md"))

    entries: list[dict[str, Any]] = []
    for p in gebaeude_files:
        entries.append(file_summary(p, "gebaeude", live_ids))
    for p in batch2_files:
        entries.append(file_summary(p, "batch2", live_ids))

    # Overlap report — same expected_quelle_id across corpora
    by_qid: dict[str, list[str]] = {}
    for e in entries:
        by_qid.setdefault(e["expected_quelle_id"], []).append(
            f"{e['corpus']}::{e['rel_path']}"
        )
    overlaps = {qid: paths for qid, paths in by_qid.items() if len(paths) > 1}

    matched_live = sum(1 for e in entries if e["live_quelle_id"])
    block_present = sum(1 for e in entries if e["sources_block_kind"] is not None)
    multi_files = [e for e in entries if e["format_hint"] == "case_markdown_multi"]

    out = {
        "manifest_version": "agent_8_phase4c_2_prep",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generator": "agent8_build_manifest.py",
        "scope_note": (
            "Phase 4c.2 prep ONLY. Agent 8 lists every dossier file the "
            "Phase-4b loader (Agent 9 / 10) must process; no full parse is "
            "performed here. Each entry stubs the q_<slug>_md id, points at "
            "the sources block offset, and counts inline citation markers so "
            "the loader knows what to expect."
        ),
        "totals": {
            "gebaeude_files": len(gebaeude_files),
            "batch2_files": len(batch2_files),
            "total_dossier_files": len(entries),
            "live_case_markdown_quelle_in_graph": len(live_ids),
            "matched_live_quelle_id": matched_live,
            "unmatched_dossier_files": len(entries) - matched_live,
            "with_sources_block": block_present,
            "missing_sources_block": len(entries) - block_present,
            "multi_dossier_files": len(multi_files),
            "overlapping_expected_quelle_ids": len(overlaps),
        },
        "overlaps": overlaps,
        "multi_dossier_files": [
            {"rel_path": e["rel_path"], "h1_titles": e["h1_titles"]}
            for e in multi_files
        ],
        "phase_4b_loader_contract_hint": (
            "For each entry: MERGE (qmd:Quelle {id: expected_quelle_id}) "
            "ON CREATE SET qmd.quelltyp='case_markdown', qmd.source_file=rel_path; "
            "stream sources_block, MERGE one q_<slug>_sN per [Sn], then MERGE "
            "(qmd)-[:ZITIERT_QUELLE]->(q_sn) with evidence_basis='case_markdown_sources'."
        ),
        "entries": entries,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    print(f"wrote manifest: {OUT_PATH}")
    print(f"  total dossier files: {len(entries)} "
          f"({len(gebaeude_files)} gebaeude + {len(batch2_files)} batch2)")
    print(f"  matched live :Quelle case_markdown id: {matched_live}/{len(entries)}")
    print(f"  files with a sources block: {block_present}/{len(entries)}")
    if overlaps:
        print(f"  expected_quelle_id collisions: {len(overlaps)} (see manifest.overlaps)")
    if multi_files:
        print(f"  multi-dossier files: {len(multi_files)} (see manifest.multi_dossier_files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
