"""Q-EXT runner — Universal source surfacing.

Plan:          _neo4j/QUELLE_REMEDIATION/EXTENSION_universal_source_surfacing.md
v3 refactor:   _neo4j/QUELLE_REMEDIATION/REFACTOR_v3_decision.md
v4 refactor:   _neo4j/QUELLE_REMEDIATION/REFACTOR_v4_decision.md

Usage:
    python qext_runner.py research      # Q-EXT.A — ingest research folder URLs
    python qext_runner.py surface       # Q-EXT.B — source_urls on every domain node
    python qext_runner.py primary       # Q-EXT.C v1 (legacy)
    python qext_runner.py confirm       # Q-EXT.C v2 (deprecated by v4)
    python qext_runner.py rewiden       # Q-EXT.A v2 — re-extract wider context
    python qext_runner.py confirm3      # Q-EXT.C v3 (deprecated by v4)
    python qext_runner.py confirm4      # Q-EXT.C v4 — cross-confirmed (BOTH); RECOMMENDED
    python qext_runner.py all           # research → surface → confirm4
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[6]
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
# noinspection PyUnresolvedReferences
from neo4j_env import resolve_connection  # type: ignore

MIG_DIR = RUN_DIR / "migrations"
LOG_DIR = RUN_DIR / "logs"
REPORT_DIR = RUN_DIR / "reports"
DATABASE = "mit-bestand"

# Labels to denylist — sources themselves + internal + too-generic
DENYLIST_LABELS = {
    "Quelle", "Dossier", "ExternalLink", "ResearchDocument", "SectionRef",
    "OntologyAnchor", "DataIssue", "DeprecatedType", "GraphVersion",
    "Land", "Stadt",
}

MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
BARE_URL_RE = re.compile(r"(?<![\(\[\w])(https?://[^\s<>\"'\)]+)")
UTM_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "mc_cid", "mc_eid", "_ga",
}

RESEARCH_DIRS = [
    REPO_ROOT / "_neo4j" / "intake" / "inbox" / "research",
    REPO_ROOT / "_archive" / "research",
]


def normalise_url(raw: str) -> str:
    raw = raw.strip().rstrip(".,;:!?")
    try:
        parsed = urlparse(raw)
    except Exception:
        return raw
    scheme = (parsed.scheme or "https").lower()
    netloc = parsed.netloc.lower()
    if (scheme == "https" and netloc.endswith(":443")) or (scheme == "http" and netloc.endswith(":80")):
        netloc = netloc.rsplit(":", 1)[0]
    path = parsed.path.rstrip("/") or "/"
    query_pairs = [(k, v) for k, v in parse_qsl(parsed.query) if k.lower() not in UTM_PARAMS]
    query = urlencode(sorted(query_pairs))
    return urlunparse((scheme, netloc, path, parsed.params, query, ""))


def md5_hex(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def extract_urls(text: str):
    """Yield dicts {url, title, sref_label, surrounding_text} from markdown text."""
    seen = set()
    for m in MD_LINK_RE.finditer(text or ""):
        label = m.group(1).strip()
        raw_url = m.group(2).strip()
        norm = normalise_url(raw_url)
        if not norm or norm in seen:
            continue
        seen.add(norm)
        start = max(0, m.start() - 60)
        end = min(len(text), m.end() + 60)
        sref = label if re.match(r"^[SP]\d+$", label) else label[:40]
        yield {
            "url": norm,
            "url_hash": md5_hex(norm),
            "title": label[:300],
            "sref_label": sref,
            "surrounding_text": text[start:end].replace("\n", " ").strip()[:300],
        }
    for m in BARE_URL_RE.finditer(text or ""):
        raw_url = m.group(1).strip().rstrip(".,;:!?")
        norm = normalise_url(raw_url)
        if not norm or norm in seen:
            continue
        seen.add(norm)
        start = max(0, m.start() - 60)
        end = min(len(text), m.end() + 60)
        yield {
            "url": norm,
            "url_hash": md5_hex(norm),
            "title": "",
            "sref_label": "bare",
            "surrounding_text": text[start:end].replace("\n", " ").strip()[:300],
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_driver():
    uri, user, password, _db = resolve_connection()
    if not uri:
        sys.exit("Missing Neo4j connection. Check .cursor/mcp.json.")
    return GraphDatabase.driver(uri, auth=(user, password))


def log_line(progress_log: Path, msg: str):
    line = f"[{utc_now()}] {msg}"
    print(line)
    with progress_log.open("a", encoding="utf-8") as fp:
        fp.write(line + "\n")


# ----------------------------------------------------------------------- #
# Q-EXT.A — research folder URL ingestion
# ----------------------------------------------------------------------- #

MERGE_EXTERNAL_LINK = """
MERGE (ext:Quelle:ExternalLink {id: 'q_url_' + $url_hash})
ON CREATE SET
  ext.url = $url,
  ext.title = $title,
  ext.quelltyp = 'external_link',
  ext.url_origin = 'research_md_link',
  ext.first_seen_in_research = $research_file,
  ext.extracted_at = date(),
  ext.evidence_origin = 'source_curated',
  ext.evidence_basis = 'markdown_link_extraction',
  ext.evidence_confidence = 'belegt',
  ext.evidence_source_id = $research_doc_id,
  ext.migration_origin = 'mig_qext_a_research_urls'
ON MATCH SET
  ext.also_in_research = apoc.coll.toSet(
    coalesce(ext.also_in_research, []) + [$research_file]
  )
"""

MERGE_ZITIERT = """
MATCH (rd:Quelle:ResearchDocument {id: $research_doc_id})
MATCH (ext:Quelle:ExternalLink {id: 'q_url_' + $url_hash})
MERGE (rd)-[z:ZITIERT_QUELLE]->(ext)
ON CREATE SET
  z.locator = $sref_label,
  z.evidence_origin = 'source_curated',
  z.evidence_basis = 'markdown_link_extraction',
  z.evidence_source_id = $research_doc_id,
  z.evidence_confidence = 'belegt',
  z.evidence_excerpt = $surrounding_text,
  z.migration_origin = 'mig_qext_a_research_urls'
"""


def run_research(driver):
    progress_log = LOG_DIR / "qext_research_progress.log"
    audit_jsonl = LOG_DIR / "qext_research_audit.jsonl"

    files = []
    for root in RESEARCH_DIRS:
        if root.exists():
            files.extend(root.rglob("*.md"))

    log_line(progress_log, f"Q-EXT.A scanning {len(files)} research markdown files")

    total_urls = 0
    per_file_counts = {}
    with audit_jsonl.open("w", encoding="utf-8") as audit_fp:
        with driver.session(database=DATABASE, default_access_mode="WRITE") as s:
            for f in files:
                try:
                    text = f.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    text = f.read_text(encoding="latin-1", errors="replace")

                slug = f.stem.lower().replace(" ", "_").replace("-", "_")
                research_doc_id = f"q_research_{slug}_md"

                # Ensure :ResearchDocument node exists (create if not)
                s.run(
                    "MERGE (rd:Quelle:ResearchDocument {id: $id}) "
                    "ON CREATE SET rd.quelltyp = 'research_markdown', "
                    "  rd.name = $name, "
                    "  rd.source_file = $path, "
                    "  rd.created_at = date(), "
                    "  rd.migration_origin = 'mig_qext_a_research_urls' "
                    "ON MATCH SET rd.source_file = coalesce(rd.source_file, $path)",
                    id=research_doc_id, name=f.stem, path=str(f.relative_to(REPO_ROOT)),
                ).consume()

                file_url_count = 0
                for rec in extract_urls(text):
                    rec["research_doc_id"] = research_doc_id
                    rec["research_file"] = str(f.relative_to(REPO_ROOT))
                    s.run(MERGE_EXTERNAL_LINK, **rec).consume()
                    s.run(MERGE_ZITIERT, **rec).consume()
                    file_url_count += 1

                per_file_counts[str(f.relative_to(REPO_ROOT))] = file_url_count
                total_urls += file_url_count
                audit_fp.write(json.dumps({
                    "file": str(f.relative_to(REPO_ROOT)),
                    "research_doc_id": research_doc_id,
                    "urls_extracted": file_url_count,
                }) + "\n")
                log_line(progress_log, f"  {f.name}: {file_url_count} URLs")

    log_line(progress_log, f"Q-EXT.A total URLs ingested: {total_urls}")

    flag = RUN_DIR / "PHASE_QEXT_A_DONE.flag"
    flag.write_text(json.dumps({
        "phase": "Q-EXT.A",
        "completed_at_utc": utc_now(),
        "files_scanned": len(files),
        "total_urls_extracted": total_urls,
        "per_file_top10": dict(sorted(
            per_file_counts.items(), key=lambda kv: -kv[1]
        )[:10]),
    }, indent=2), encoding="utf-8")
    log_line(progress_log, f"Flag: {flag}")


# ----------------------------------------------------------------------- #
# Q-EXT.B — universal source_urls
# ----------------------------------------------------------------------- #

def discover_target_labels(driver) -> list[str]:
    """Return every node label except those in DENYLIST_LABELS."""
    with driver.session(database=DATABASE, default_access_mode="READ") as s:
        rows = s.run(
            "CALL db.labels() YIELD label "
            "WHERE NOT label IN $deny "
            "RETURN label ORDER BY label",
            deny=list(DENYLIST_LABELS),
        )
        return [r["label"] for r in rows]


def run_surface(driver):
    progress_log = LOG_DIR / "qext_surface_progress.log"
    audit_jsonl = LOG_DIR / "qext_surface_audit.jsonl"

    labels = discover_target_labels(driver)
    log_line(progress_log, f"Q-EXT.B running on {len(labels)} labels: {labels}")

    migration_path = MIG_DIR / "mig_qext_b_universal_source_urls.cypher"
    cypher_text = migration_path.read_text(encoding="utf-8")

    # Extract just the UNWIND-CALL block (the rest are audit selects)
    # The body is the first statement in the file. Find it.
    statements = []
    current = []
    for line in cypher_text.splitlines():
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
    main_stmt = statements[0]

    per_label_results = {}
    with audit_jsonl.open("w", encoding="utf-8") as audit_fp:
        with driver.session(database=DATABASE, default_access_mode="WRITE") as s:
            # Process labels in chunks of 10 to keep transaction small
            for i in range(0, len(labels), 10):
                chunk = labels[i:i+10]
                t0 = datetime.now(timezone.utc)
                try:
                    rows = list(s.run(main_stmt, labels=chunk))
                    elapsed = (datetime.now(timezone.utc) - t0).total_seconds() * 1000
                    for row in rows:
                        per_label_results[row["label"]] = row["nodes_updated"]
                        audit_fp.write(json.dumps({
                            "label": row["label"],
                            "nodes_updated": row["nodes_updated"],
                        }) + "\n")
                    log_line(progress_log,
                             f"  chunk {i}–{i+len(chunk)} done in {elapsed:.0f} ms: "
                             f"{sum(r['nodes_updated'] for r in rows)} nodes updated")
                except Exception as exc:
                    log_line(progress_log, f"  ERROR on chunk {chunk}: {exc}")
                    raise

            # Run audit statements (the per-label ones in the migration file)
            for stmt in statements[1:]:
                try:
                    rows = list(s.run(stmt))
                    audit_fp.write(json.dumps({
                        "audit_statement_preview": stmt.splitlines()[0][:120],
                        "rows": [dict(r) for r in rows][:30],
                    }, default=str) + "\n")
                except Exception:
                    pass

    flag = RUN_DIR / "PHASE_QEXT_B_DONE.flag"
    flag.write_text(json.dumps({
        "phase": "Q-EXT.B",
        "completed_at_utc": utc_now(),
        "labels_processed": len(labels),
        "labels": labels,
        "per_label_nodes_updated": per_label_results,
        "total_nodes_updated": sum(per_label_results.values()),
    }, indent=2), encoding="utf-8")
    log_line(progress_log, f"Flag: {flag}; total nodes updated: "
                            f"{sum(per_label_results.values())}")


# ----------------------------------------------------------------------- #
# Q-EXT.C — primary_source_url
# ----------------------------------------------------------------------- #

def run_primary(driver):
    progress_log = LOG_DIR / "qext_primary_progress.log"
    audit_jsonl = LOG_DIR / "qext_primary_audit.jsonl"

    migration_path = MIG_DIR / "mig_qext_c_primary_source_url.cypher"
    cypher_text = migration_path.read_text(encoding="utf-8")

    statements = []
    current = []
    for line in cypher_text.splitlines():
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

    log_line(progress_log, f"Q-EXT.C running {len(statements)} statements")

    audit_results = {}
    with audit_jsonl.open("w", encoding="utf-8") as audit_fp:
        with driver.session(database=DATABASE, default_access_mode="WRITE") as s:
            for i, stmt in enumerate(statements):
                t0 = datetime.now(timezone.utc)
                rows = list(s.run(stmt))
                elapsed = (datetime.now(timezone.utc) - t0).total_seconds() * 1000
                audit_fp.write(json.dumps({
                    "stmt_index": i,
                    "elapsed_ms": elapsed,
                    "rows": [dict(r) for r in rows][:30],
                }, default=str) + "\n")
                audit_results[f"stmt_{i}"] = [dict(r) for r in rows][:20]
                preview = stmt.splitlines()[0][:80]
                log_line(progress_log,
                         f"  [{i+1}/{len(statements)}] {elapsed:.0f} ms — {preview}…")

    flag = RUN_DIR / "PHASE_QEXT_C_DONE.flag"
    flag.write_text(json.dumps({
        "phase": "Q-EXT.C",
        "completed_at_utc": utc_now(),
        "audit_results": audit_results,
    }, indent=2, default=str), encoding="utf-8")
    log_line(progress_log, f"Flag: {flag}")


# ----------------------------------------------------------------------- #
# Q-EXT.C v2 — confirmed_source_urls (multi-URL, strict)
# ----------------------------------------------------------------------- #

def run_confirm(driver):
    """Replace primary_source_url heuristic with confirmed_source_urls list.

    Each URL is confirmed iff:
      C1 — Dossier-grounded (node-direct BELEGT_IN → Dossier → ZITIERT_QUELLE → URL)
      C2 — Content-verified (S3 verification_status ∈ {verbatim,paraphrase,token})

    Multiple URLs per node OK. primary_source_url becomes confirmed[0] or NULL.
    """
    progress_log = LOG_DIR / "qext_confirm_progress.log"
    audit_jsonl = LOG_DIR / "qext_confirm_audit.jsonl"

    migration_path = MIG_DIR / "mig_qext_c_v2_confirmed_urls.cypher"
    cypher_text = migration_path.read_text(encoding="utf-8")

    statements = []
    current = []
    for line in cypher_text.splitlines():
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

    log_line(progress_log, f"Q-EXT.C v2 running {len(statements)} statements")

    audit_results = {}
    with audit_jsonl.open("w", encoding="utf-8") as audit_fp:
        with driver.session(database=DATABASE, default_access_mode="WRITE") as s:
            for i, stmt in enumerate(statements):
                t0 = datetime.now(timezone.utc)
                rows = list(s.run(stmt))
                elapsed = (datetime.now(timezone.utc) - t0).total_seconds() * 1000
                audit_fp.write(json.dumps({
                    "stmt_index": i,
                    "elapsed_ms": elapsed,
                    "rows": [dict(r) for r in rows][:30],
                }, default=str) + "\n")
                audit_results[f"stmt_{i}"] = [dict(r) for r in rows][:20]
                preview = stmt.splitlines()[0][:80]
                log_line(progress_log,
                         f"  [{i+1}/{len(statements)}] {elapsed:.0f} ms — {preview}…")

    flag = RUN_DIR / "PHASE_QEXT_C_V2_DONE.flag"
    flag.write_text(json.dumps({
        "phase": "Q-EXT.C-v2",
        "completed_at_utc": utc_now(),
        "audit_results": audit_results,
    }, indent=2, default=str), encoding="utf-8")
    log_line(progress_log, f"Flag: {flag}")


# ----------------------------------------------------------------------- #
# Q-EXT.A v2 — re-extract wider context per :ZITIERT_QUELLE
# ----------------------------------------------------------------------- #

def _find_context_for_url(text: str, url: str, char_radius_fallback: int = 400):
    """Find URL in text, return surrounding Markdown row OR paragraph."""
    pos = text.find(url)
    if pos == -1:
        return None
    line_start = text.rfind("\n", 0, pos) + 1
    line_end = text.find("\n", pos + len(url))
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end]
    if line.lstrip().startswith("|") and line.rstrip().endswith("|"):
        return line.strip()
    # Paragraph fallback
    start = max(0, pos - char_radius_fallback)
    end = min(len(text), pos + len(url) + char_radius_fallback)
    blank_before = text.rfind("\n\n", start, pos)
    if blank_before > -1:
        start = blank_before + 2
    blank_after = text.find("\n\n", pos + len(url), end)
    if blank_after > -1:
        end = blank_after
    return text[start:end].replace("\n", " ").strip()


def run_rewiden(driver):
    """Re-extract wider context for every :ZITIERT_QUELLE edge that S1 wrote."""
    progress_log = LOG_DIR / "qext_rewiden_progress.log"
    audit_jsonl = LOG_DIR / "qext_rewiden_audit.jsonl"

    log_line(progress_log, "Q-EXT.A v2 — re-widening :ZITIERT_QUELLE excerpts")

    with driver.session(database=DATABASE, default_access_mode="READ") as s:
        rows = list(s.run(
            "MATCH (src:Quelle)-[r:ZITIERT_QUELLE]->(ext:ExternalLink) "
            "WHERE r.evidence_excerpt IS NOT NULL "
            "  AND coalesce(r.evidence_excerpt_v2, false) = false "
            "  AND (src.source_file IS NOT NULL OR "
            "       src.quelltyp IN ['case_markdown','research_markdown']) "
            "RETURN id(r) AS rid, src.id AS src_id, src.source_file AS src_path, "
            "       src.quelltyp AS quelltyp, ext.url AS url"
        ))

    log_line(progress_log, f"  candidates: {len(rows)} edges to widen")

    # Group by source file so we only read each file once
    by_file: dict[str, list[dict]] = {}
    for r in rows:
        path = r["src_path"]
        if not path:
            # Fallback: guess from src_id (e.g. q_<slug>_md → look in archives)
            slug = r["src_id"].removeprefix("q_").removesuffix("_md")
            guesses = [
                REPO_ROOT / "_neo4j" / "intake" / "archive" /
                  "2026-05-20_inbox_batch2_import" / "raw_tree" / (slug + ".md"),
                REPO_ROOT / "_archive" / "research" / "gebaeude" / (slug + ".md"),
                REPO_ROOT / "_neo4j" / "intake" / "inbox" / "research" / (slug.removeprefix("research_") + ".md"),
            ]
            path = next((str(g.relative_to(REPO_ROOT)) for g in guesses if g.exists()), None)
        if not path:
            continue
        by_file.setdefault(path, []).append(r)

    updated = 0
    skipped_no_file = 0
    skipped_no_match = 0

    with audit_jsonl.open("w", encoding="utf-8") as audit_fp:
        with driver.session(database=DATABASE, default_access_mode="WRITE") as s:
            for path, edges in by_file.items():
                fp = REPO_ROOT / path
                if not fp.exists():
                    skipped_no_file += len(edges)
                    log_line(progress_log, f"  SKIP missing file: {path}")
                    continue
                try:
                    text = fp.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    text = fp.read_text(encoding="latin-1", errors="replace")

                for e in edges:
                    context = _find_context_for_url(text, e["url"])
                    if not context:
                        skipped_no_match += 1
                        audit_fp.write(json.dumps({
                            "rid": e["rid"], "url": e["url"], "src_id": e["src_id"],
                            "result": "url_not_found_in_file"
                        }) + "\n")
                        continue
                    s.run(
                        "MATCH ()-[r:ZITIERT_QUELLE]->() WHERE id(r) = $rid "
                        "SET r.evidence_excerpt = $context, "
                        "    r.evidence_excerpt_v2 = true, "
                        "    r.evidence_excerpt_width = size($context), "
                        "    r.migration_origin = coalesce(r.migration_origin,'') + "
                        "      ' | mig_qext_a_v2_widen_context'",
                        rid=e["rid"], context=context
                    ).consume()
                    updated += 1
                    audit_fp.write(json.dumps({
                        "rid": e["rid"], "url": e["url"], "src_id": e["src_id"],
                        "result": "widened", "width": len(context)
                    }) + "\n")

    log_line(progress_log, f"  updated: {updated}; no_file: {skipped_no_file}; "
                            f"no_url_match: {skipped_no_match}")

    flag = RUN_DIR / "PHASE_QEXT_A_V2_DONE.flag"
    flag.write_text(json.dumps({
        "phase": "Q-EXT.A-v2",
        "completed_at_utc": utc_now(),
        "edges_widened": updated,
        "skipped_no_file": skipped_no_file,
        "skipped_no_url_match": skipped_no_match,
    }, indent=2), encoding="utf-8")
    log_line(progress_log, f"Flag: {flag}")


# ----------------------------------------------------------------------- #
# Q-EXT.C v3 — confirmed_source_urls with synonym map
# ----------------------------------------------------------------------- #

SYNONYM_MAP_PATH = REPO_ROOT / "_neo4j" / "contracts" / "synonyms.json"


def _load_synonyms() -> dict[str, list[str]]:
    if not SYNONYM_MAP_PATH.exists():
        return {}
    data = json.loads(SYNONYM_MAP_PATH.read_text(encoding="utf-8"))
    return data.get("synonyms", {})


def _expand_terms(name: str | None, aliases: list | None,
                  node_id: str | None, synonyms: dict[str, list[str]]) -> list[str]:
    terms: set[str] = set()
    if name and isinstance(name, str):
        terms.add(name.lower().strip())
    for a in (aliases or []):
        if a and isinstance(a, str):
            terms.add(a.lower().strip())
    if node_id:
        import re as _re
        stem = _re.sub(r"^(mat|norm|bg|bt|p|q|s|huerde|akt|akr)_", "", node_id.lower())
        if stem and stem != node_id.lower():
            terms.add(stem.replace("_", " "))
    for t in list(terms):
        for syn in synonyms.get(t, []):
            if isinstance(syn, str):
                terms.add(syn.lower())
    return [t for t in terms if len(t) >= 4]


def run_confirm3(driver):
    """Recompute confirmed_source_urls using v3 logic (synonyms + escape + 3 criteria)."""
    progress_log = LOG_DIR / "qext_confirm3_progress.log"
    audit_jsonl = LOG_DIR / "qext_confirm3_audit.jsonl"

    synonyms = _load_synonyms()
    log_line(progress_log, f"Q-EXT.C v3 — loaded {len(synonyms)} synonym entries")

    # Discover labels (same denylist as surface)
    labels = discover_target_labels(driver)

    # Build per-node search terms
    log_line(progress_log, f"Building per-node search terms for {len(labels)} labels")
    node_search_terms: list[dict] = []
    with driver.session(database=DATABASE, default_access_mode="READ") as s:
        for lbl in labels:
            for row in s.run(
                f"MATCH (n:`{lbl}`) "
                "WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0 "
                "RETURN n.id AS id, n.name AS name, n.aliases AS aliases"
            ):
                terms = _expand_terms(row["name"], row["aliases"], row["id"], synonyms)
                if not terms:
                    continue
                node_search_terms.append({
                    "node_id": row["id"],
                    "name": row["name"],
                    "terms": terms,
                })

    log_line(progress_log, f"  {len(node_search_terms)} nodes have at least one search term")

    migration_path = MIG_DIR / "mig_qext_c_v3_confirmed_urls.cypher"
    cypher_text = migration_path.read_text(encoding="utf-8")
    statements: list[str] = []
    current: list[str] = []
    for line in cypher_text.splitlines():
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

    log_line(progress_log, f"v3 migration: {len(statements)} statements")

    # Statements 0-4 use $node_search_terms; statements 5+ are audits.
    # Step 0 (cleanup), then in chunks of 200 for the UNWIND statements.
    audit_results = {}
    with audit_jsonl.open("w", encoding="utf-8") as audit_fp:
        with driver.session(database=DATABASE, default_access_mode="WRITE") as s:
            # Statement 0 is the cleanup — run once with no params
            s.run(statements[0]).consume()
            log_line(progress_log, "  [0] cleanup done")

            # Statements 1-4 process $node_search_terms — chunk it
            for stmt_idx in (1, 2, 3, 4):
                if stmt_idx >= len(statements):
                    break
                stmt = statements[stmt_idx]
                chunk_size = 200
                for i in range(0, len(node_search_terms), chunk_size):
                    chunk = node_search_terms[i:i + chunk_size]
                    s.run(stmt, node_search_terms=chunk).consume()
                log_line(progress_log, f"  [{stmt_idx}] processed {len(node_search_terms)} nodes")

            # Statements 5+ are audits (no params)
            for i in range(5, len(statements)):
                stmt = statements[i]
                t0 = datetime.now(timezone.utc)
                rows = list(s.run(stmt))
                elapsed = (datetime.now(timezone.utc) - t0).total_seconds() * 1000
                audit_results[f"stmt_{i}"] = [dict(r) for r in rows][:30]
                audit_fp.write(json.dumps({
                    "stmt_index": i,
                    "elapsed_ms": elapsed,
                    "rows": [dict(r) for r in rows][:30],
                }, default=str) + "\n")
                log_line(progress_log, f"  [{i}] audit done ({elapsed:.0f} ms)")

    flag = RUN_DIR / "PHASE_QEXT_C_V3_DONE.flag"
    flag.write_text(json.dumps({
        "phase": "Q-EXT.C-v3",
        "completed_at_utc": utc_now(),
        "nodes_processed": len(node_search_terms),
        "synonym_entries": len(synonyms),
        "audit_results": audit_results,
    }, indent=2, default=str), encoding="utf-8")
    log_line(progress_log, f"Flag: {flag}")


# ----------------------------------------------------------------------- #
# Q-EXT.C v4 — cross-confirmed source URLs (BOTH dossier-text AND page-body)
# ----------------------------------------------------------------------- #

import gzip as _gzip

CACHE_DIR = REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-21_quelle_remediation" / "shared" / "url_bodies"

V4_TAG_RE = re.compile(r"<[^>]+>", re.DOTALL)
V4_SCRIPT_RE = re.compile(r"<(script|style|nav|footer)\b[^>]*>.*?</\1>",
                           re.IGNORECASE | re.DOTALL)
V4_WHITESPACE_RE = re.compile(r"\s+")


def _v4_build_url_cache_index() -> dict[str, str]:
    """URL → cache_path. Mirrors test_node_link.py's build_url_cache_index()."""
    index: dict[str, str] = {}
    for meta_path in CACHE_DIR.glob("*.meta.json"):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        url = meta.get("url")
        if not url:
            continue
        body_id = meta_path.stem.replace(".meta", "")
        for ext in (".html", ".html.gz", ".pdf", ".pdf.gz"):
            p = CACHE_DIR / f"{body_id}{ext}"
            if p.exists():
                index[normalise_url(url)] = str(p)
                break
    return index


def _v4_read_body(cache_path: str) -> bytes:
    p = Path(cache_path)
    if p.suffix == ".gz":
        with _gzip.open(p, "rb") as f:
            return f.read()
    return p.read_bytes()


def _v4_html_to_text(html_bytes: bytes) -> str:
    try:
        html = html_bytes.decode("utf-8", errors="replace")
    except Exception:
        html = html_bytes.decode("latin-1", errors="replace")
    html = V4_SCRIPT_RE.sub("", html)
    text = V4_TAG_RE.sub(" ", html)
    text = V4_WHITESPACE_RE.sub(" ", text)
    return text.strip()


def _v4_extract_page_text(cache_path: str) -> str:
    if cache_path.endswith((".pdf", ".pdf.gz")):
        return ""    # PDF text extraction skipped in v4 (would need pdfplumber)
    return _v4_html_to_text(_v4_read_body(cache_path))[:80_000]


def _v4_norm_token_for(name: str) -> str | None:
    """For norm-style names ('CEN/TS 1090-201'), return strongest token."""
    m = re.search(r"(\d{3,5}(?:[-:]\d{1,4})?)", name)
    return m.group(1) if m else None


def _v4_terms_for_node(name: str, aliases: list, node_id: str,
                       label: str, synonyms: dict) -> list[str]:
    terms: set[str] = set()
    if name and isinstance(name, str):
        terms.add(name.lower().strip())
    for a in (aliases or []):
        if a and isinstance(a, str):
            terms.add(a.lower().strip())
    if node_id:
        stem = re.sub(r"^(mat|norm|bg|bt|p|q|s|huerde|akt|akr|cert|lcm)_", "",
                      node_id.lower())
        if stem and stem != node_id.lower():
            terms.add(stem.replace("_", " "))
    for t in list(terms):
        for syn in synonyms.get(t, []):
            if isinstance(syn, str):
                terms.add(syn.lower())
    # Norm-specific: add digit token
    if label == "Norm" and name:
        tok = _v4_norm_token_for(name)
        if tok:
            terms.add(tok.lower())
    return [t for t in terms if len(t) >= 4]


def _v4_text_mentions(text: str, terms: list[str]) -> list[str]:
    if not text or not terms:
        return []
    tl = text.lower()
    return [t for t in terms if re.search(rf"\b{re.escape(t)}\b", tl)]


def run_confirm4(driver):
    """v4: cross-confirmed source URLs.

    Runs PER NODE: pull (URL, dossier-text-near-URL) pairs from the graph;
    look up each URL in the cache; check term overlap in BOTH dossier-text
    and page-body. Only URLs with BOTH hits are confirmed.
    """
    progress_log = LOG_DIR / "qext_confirm4_progress.log"
    audit_jsonl = LOG_DIR / "qext_confirm4_audit.jsonl"

    log_line(progress_log, "Q-EXT.C v4 — cross-confirmed (BOTH) source URLs")

    synonyms = _load_synonyms()
    log_line(progress_log, f"  synonyms loaded: {len(synonyms)} entries")

    url_cache = _v4_build_url_cache_index()
    log_line(progress_log, f"  URL cache index: {len(url_cache)} URLs with cached body")

    # Page-text cache (lazy; one extraction per URL hit during the run)
    page_text_cache: dict[str, str] = {}

    def page_text_for(url: str) -> str:
        if url in page_text_cache:
            return page_text_cache[url]
        cp = url_cache.get(url)
        if not cp:
            page_text_cache[url] = ""
            return ""
        try:
            t = _v4_extract_page_text(cp)
        except Exception as e:
            log_line(progress_log, f"  page-extract error for {url}: {e}")
            t = ""
        page_text_cache[url] = t
        return t

    # Discover target labels (same denylist as surface)
    labels = discover_target_labels(driver)
    log_line(progress_log, f"  labels in scope: {len(labels)}")

    node_results: list[dict] = []
    confirmed_total = 0
    nodes_with_any = 0

    with audit_jsonl.open("w", encoding="utf-8") as audit_fp:
        with driver.session(database=DATABASE, default_access_mode="READ") as s:
            for lbl in labels:
                rows = list(s.run(
                    f"MATCH (n:`{lbl}`) "
                    "WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0 "
                    "RETURN n.id AS id, n.name AS name, n.aliases AS aliases, "
                    "       n.source_urls AS source_urls"
                ))
                for r in rows:
                    terms = _v4_terms_for_node(
                        r["name"], r["aliases"] or [], r["id"], lbl, synonyms
                    )
                    if not terms:
                        continue

                    # Pull every (URL, dossier_id, evidence_excerpt) triple
                    # for this node from the graph (limit 2 hops).
                    triples = list(s.run(
                        "MATCH (n {id: $id})-[:BELEGT_IN|HAS_SOURCE_LINK]->(d) "
                        "WHERE (d:Dossier OR d:ResearchDocument) "
                        "MATCH (d)-[zq:ZITIERT_QUELLE]->(ext:ExternalLink) "
                        "WHERE ext.url IN $urls "
                        "RETURN ext.url AS url, d.id AS dossier_id, "
                        "       zq.locator AS sref, "
                        "       coalesce(zq.evidence_excerpt, '') AS d_text",
                        id=r["id"], urls=r["source_urls"],
                    ))

                    confirmed_urls: dict[str, list[str]] = {}

                    # C1 — direct dossier-grounded
                    for t in triples:
                        url = t["url"]
                        reason = (f"c1_dossier_grounded:{t['dossier_id']}:"
                                  f"{t.get('sref') or 'bare'}")
                        confirmed_urls.setdefault(url, []).append(reason)

                    # C2 — S3 content-verified
                    c2_rows = list(s.run(
                        "MATCH (n {id: $id})-[:BELEGT_IN|HAS_SOURCE_LINK*1..3]->(ext:ExternalLink) "
                        "MATCH (:Dossier)-[zq:ZITIERT_QUELLE]->(ext) "
                        "WHERE zq.verification_status IN "
                        "  ['verbatim_match','paraphrase_match','token_match'] "
                        "  AND ext.url IN $urls "
                        "RETURN DISTINCT ext.url AS url, "
                        "       zq.verification_method AS m, "
                        "       zq.verification_score AS sc",
                        id=r["id"], urls=r["source_urls"],
                    ))
                    for c in c2_rows:
                        url = c["url"]
                        reason = (f"c2_content_verified:{c['m'] or 'unknown'}:"
                                  f"{c['sc'] or 0}")
                        confirmed_urls.setdefault(url, []).append(reason)

                    # C4 — cross-confirmed BOTH (D-text AND page-text)
                    for t in triples:
                        url = t["url"]
                        d_hits = _v4_text_mentions(t["d_text"], terms)
                        if not d_hits:
                            continue
                        p_hits = _v4_text_mentions(page_text_for(url), terms)
                        if not p_hits:
                            continue
                        reason = (f"c4_cross_confirmed:{t['dossier_id']}:"
                                  f"{','.join(d_hits)}:{','.join(p_hits)}")
                        confirmed_urls.setdefault(url, []).append(reason)

                    if confirmed_urls:
                        nodes_with_any += 1
                        confirmed_total += len(confirmed_urls)
                    node_results.append({
                        "node_id": r["id"],
                        "confirmed_urls": list(confirmed_urls.keys()),
                        "evidence": {u: rs for u, rs in confirmed_urls.items()},
                    })
                    audit_fp.write(json.dumps({
                        "node_id": r["id"], "label": lbl,
                        "terms": terms[:6],
                        "source_count": len(r["source_urls"]),
                        "confirmed_count": len(confirmed_urls),
                    }) + "\n")
                log_line(progress_log,
                         f"  {lbl}: {len(rows)} nodes processed; "
                         f"running totals — confirmed_urls={confirmed_total}, "
                         f"nodes_with_any={nodes_with_any}")

    log_line(progress_log,
             f"Computed: {len(node_results)} nodes; "
             f"{nodes_with_any} with at least one confirmed URL; "
             f"{confirmed_total} confirmed (node,URL) pairs total")

    # Apply via migration (chunks of 100)
    migration_path = MIG_DIR / "mig_qext_c_v4_confirmed_urls.cypher"
    cypher_text = migration_path.read_text(encoding="utf-8")
    statements: list[str] = []
    current: list[str] = []
    for line in cypher_text.splitlines():
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

    audit_results = {}
    with driver.session(database=DATABASE, default_access_mode="WRITE") as s:
        # Statement 0 = cleanup
        s.run(statements[0]).consume()
        # Statement 1 = UNWIND $node_results (chunked)
        chunk_size = 100
        for i in range(0, len(node_results), chunk_size):
            s.run(statements[1], node_results=node_results[i:i + chunk_size]).consume()
        # Statements 2+ = audits
        for i in range(2, len(statements)):
            t0 = datetime.now(timezone.utc)
            rows = list(s.run(statements[i]))
            elapsed = (datetime.now(timezone.utc) - t0).total_seconds() * 1000
            audit_results[f"stmt_{i}"] = [dict(r) for r in rows][:30]
            log_line(progress_log, f"  audit [{i}]: {elapsed:.0f} ms, {len(rows)} rows")

    flag = RUN_DIR / "PHASE_QEXT_C_V4_DONE.flag"
    flag.write_text(json.dumps({
        "phase": "Q-EXT.C-v4",
        "completed_at_utc": utc_now(),
        "nodes_processed": len(node_results),
        "nodes_with_confirmed": nodes_with_any,
        "confirmed_pairs_total": confirmed_total,
        "urls_in_cache": len(url_cache),
        "audit_results": audit_results,
    }, indent=2, default=str), encoding="utf-8")
    log_line(progress_log, f"Flag: {flag}")


# ----------------------------------------------------------------------- #
# Entrypoint
# ----------------------------------------------------------------------- #

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    phase = sys.argv[1].lower()
    driver = get_driver()
    try:
        if phase == "research":
            run_research(driver)
        elif phase == "surface":
            run_surface(driver)
        elif phase == "primary":
            run_primary(driver)
        elif phase == "confirm":
            # Q-EXT.C v2 — multi-URL confirmed_source_urls.
            run_confirm(driver)
        elif phase == "rewiden":
            # Q-EXT.A v2 — re-extract wider context from source files.
            run_rewiden(driver)
        elif phase == "confirm3":
            # Q-EXT.C v3 — synonym-expanded, properly-escaped 3-criterion match.
            run_confirm3(driver)
        elif phase == "confirm4":
            # Q-EXT.C v4 — cross-confirmed (BOTH dossier-side AND page-side).
            # RECOMMENDED. Replaces v1/v2/v3 confirm logic.
            run_confirm4(driver)
        elif phase == "all":
            run_research(driver)
            run_surface(driver)
            run_confirm4(driver)  # use v4 in the all-bundle
        else:
            sys.exit(f"Unknown phase: {phase}. "
                     f"Use: research | surface | primary | confirm | "
                     f"rewiden | confirm3 | confirm4 | all")
    finally:
        driver.close()


if __name__ == "__main__":
    main()
