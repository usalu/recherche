"""Agent S1 — URL extractor
=========================
Discovers every URL in the graph (dossier text_content, existing Quelle.url,
edge evidence_excerpt, node URL properties) and creates / stamps
:Quelle :ExternalLink nodes with normalized URLs.

Run from repo root:
    python _neo4j/intake/runs/2026-05-21_quelle_remediation/logs/agent_s1_runner.py
"""
from __future__ import annotations

import hashlib
import re
import sys
import json
from pathlib import Path
from urllib.parse import (
    parse_qsl,
    urlencode,
    urlparse,
    urlunparse,
)

_REPO = Path(__file__).resolve().parents[5]
_SCRIPTS = _REPO / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402

# ─── constants ────────────────────────────────────────────────────────────────

UTM_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "mc_cid", "mc_eid", "_ga",
}

# Regex to find markdown links: [label](url)
MD_LINK_RE = re.compile(r'\[([^\]]*)\]\((https?://[^\s)]+)\)')
# Regex to find bare URLs (not preceded by '(' to avoid double-counting md links)
BARE_URL_RE = re.compile(r'(?<!\()(https?://[^\s\)\]>"\']+)')

RUN_DIR = Path(__file__).resolve().parent.parent / "agent_s1_url_extractor"
FLAG_FILE = RUN_DIR / "PHASE_S1_DONE.flag"
REPORT_FILE = RUN_DIR / "S1_REPORT.json"

# ─── URL helpers ─────────────────────────────────────────────────────────────

def normalise_url(raw: str) -> str | None:
    """Normalise URL: lowercase netloc, strip trailing slash, remove tracking params, drop fragment."""
    try:
        raw = raw.strip().rstrip(".,;:!?")  # strip trailing punctuation
        parsed = urlparse(raw)
        scheme = (parsed.scheme or "https").lower()
        if scheme not in ("http", "https"):
            return None
        netloc = parsed.netloc.lower()
        if not netloc:
            return None
        # Drop default ports
        if scheme == "https" and netloc.endswith(":443"):
            netloc = netloc[:-4]
        elif scheme == "http" and netloc.endswith(":80"):
            netloc = netloc[:-3]
        path = parsed.path.rstrip("/")
        # For root-level URLs, path is now "" — correct (gives https://host not https://host/)
        # Strip tracking params
        query_pairs = [
            (k, v) for k, v in parse_qsl(parsed.query)
            if k.lower() not in UTM_PARAMS
        ]
        query = urlencode(sorted(query_pairs))
        return urlunparse((scheme, netloc, path, parsed.params, query, ""))
    except Exception:
        return None


def url_hash(url: str) -> str:
    return hashlib.md5(url.encode("utf-8")).hexdigest()[:16]


def url_id(url: str) -> str:
    return "q_url_" + url_hash(url)


# ─── extraction helpers ───────────────────────────────────────────────────────

def extract_md_links(text: str) -> list[tuple[str, str]]:
    """Return list of (label, url) from markdown links in text."""
    return [(m.group(1).strip(), m.group(2).strip()) for m in MD_LINK_RE.finditer(text)]


def extract_bare_urls(text: str) -> list[str]:
    """Return list of bare URLs (not part of a markdown link) from text."""
    all_urls = {m.group(0) for m in BARE_URL_RE.finditer(text)}
    md_urls = {m.group(2) for m in MD_LINK_RE.finditer(text)}
    return list(all_urls - md_urls)


def surrounding_text(text: str, url: str, window: int = 120) -> str:
    """Return up to `window` chars around the first occurrence of url."""
    idx = text.find(url)
    if idx < 0:
        return ""
    start = max(0, idx - window // 2)
    end = min(len(text), idx + len(url) + window // 2)
    return text[start:end].replace("\n", " ")


# ─── Cypher templates ─────────────────────────────────────────────────────────

# S1.A — MERGE :ExternalLink node
S1_A = """
MERGE (ext:Quelle:ExternalLink {id: $ext_id})
ON CREATE SET
  ext.url              = $url,
  ext.title            = $title,
  ext.quelltyp         = 'external_link',
  ext.url_origin       = $url_origin,
  ext.first_seen_in_dossier = $first_seen_in_dossier,
  ext.extracted_at     = date(),
  ext.evidence_origin  = 'source_curated',
  ext.evidence_basis   = $evidence_basis,
  ext.evidence_confidence = 'belegt',
  ext.evidence_source_id  = $source_id,
  ext.migration_origin = 'mig_s1_url_extract'
ON MATCH SET
  ext.also_in_dossier = coll.distinct(
    coalesce(ext.also_in_dossier, []) +
    CASE WHEN $url_origin IN ['dossier_md_link','dossier_bare_url'] THEN [$source_id] ELSE [] END
  ),
  ext.also_in_node = coll.distinct(
    coalesce(ext.also_in_node, []) +
    CASE WHEN $url_origin = 'node_property' THEN [$source_id] ELSE [] END
  ),
  ext.also_in_edge = coll.distinct(
    coalesce(ext.also_in_edge, []) +
    CASE WHEN $url_origin = 'edge_property' THEN [$source_id] ELSE [] END
  )
"""

# S1.B — MERGE :ZITIERT_QUELLE from :Quelle source to :ExternalLink
S1_B = """
MATCH (source:Quelle {id: $source_id})
MATCH (ext:Quelle:ExternalLink {id: $ext_id})
MERGE (source)-[z:ZITIERT_QUELLE]->(ext)
ON CREATE SET
  z.locator              = $locator,
  z.evidence_origin      = 'source_curated',
  z.evidence_basis       = $evidence_basis,
  z.evidence_source_id   = $source_id,
  z.evidence_confidence  = 'belegt',
  z.evidence_excerpt     = $surrounding_text,
  z.migration_origin     = 'mig_s1_url_extract'
"""

# S1.B_existing — stamp existing :Quelle with .url and MERGE :ZITIERT_QUELLE from its citator
# For pre-existing nodes: just add :ExternalLink label and url_origin
S1_STAMP_EXISTING = """
MATCH (ext:Quelle {id: $existing_id})
WHERE NOT ext:ExternalLink
SET ext:ExternalLink
SET ext.url_origin = 'pre_existing_quelle',
    ext.migration_origin = 'mig_s1_url_extract',
    ext.extracted_at = date()
"""

# For pre-existing Quelle nodes: also MERGE a new :ExternalLink if URL normalises differently
S1_A_EXISTING = """
MERGE (ext:Quelle:ExternalLink {id: $ext_id})
ON CREATE SET
  ext.url              = $url,
  ext.title            = $title,
  ext.quelltyp         = 'external_link',
  ext.url_origin       = 'pre_existing_quelle',
  ext.first_seen_in_dossier = null,
  ext.extracted_at     = date(),
  ext.evidence_origin  = 'source_curated',
  ext.evidence_basis   = 'pre_existing_quelle_url',
  ext.evidence_confidence = 'belegt',
  ext.evidence_source_id  = $source_id,
  ext.migration_origin = 'mig_s1_url_extract'
ON MATCH SET
  ext.url_origin = coalesce(ext.url_origin, 'pre_existing_quelle')
"""

# S1.C — Link from non-Quelle node via :HAS_SOURCE_LINK
S1_C = """
MATCH (source) WHERE source.id = $source_id AND NOT source:Quelle
MATCH (ext:Quelle:ExternalLink {id: $ext_id})
MERGE (source)-[h:HAS_SOURCE_LINK]->(ext)
ON CREATE SET
  h.property_name     = $property_name,
  h.evidence_origin   = 'source_curated',
  h.evidence_basis    = 'node_property_extraction',
  h.evidence_source_id = source.id,
  h.evidence_confidence = 'belegt',
  h.migration_origin  = 'mig_s1_url_extract'
"""

# ─── main runner ──────────────────────────────────────────────────────────────

def run_s1() -> dict:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(
        uri, auth=(user, password),
        notifications_disabled_categories=["DEPRECATION", "UNRECOGNIZED"],
    )
    stats = {
        "stage1_dossier_links": 0,
        "stage1_dossier_bare_urls": 0,
        "stage2_pre_existing": 0,
        "stage3_edge_urls": 0,
        "stage4_node_prop_urls": 0,
        "errors": [],
    }

    with driver.session(database=database) as session:

        # ── Stage 1: Scan dossier / research text_content ────────────────────
        print("Stage 1: scanning dossier/research markdown text_content...")
        candidates = session.run(
            "MATCH (q:Quelle) WHERE q.quelltyp IN ['case_markdown','research_markdown'] "
            "  AND q.text_content IS NOT NULL "
            "RETURN q.id AS qid, q.text_content AS text, q.quelltyp AS qt"
        ).data()
        print(f"  Found {len(candidates)} nodes with text_content")

        for cand in candidates:
            qid = cand["qid"]
            text = cand["text"] or ""

            # markdown links
            for label, raw_url in extract_md_links(text):
                norm = normalise_url(raw_url)
                if not norm:
                    continue
                eid = url_id(norm)
                surr = surrounding_text(text, raw_url)
                try:
                    session.run(S1_A, ext_id=eid, url=norm, title=label,
                                url_origin="dossier_md_link",
                                first_seen_in_dossier=qid,
                                evidence_basis="markdown_link_extraction",
                                source_id=qid)
                    session.run(S1_B, source_id=qid, ext_id=eid,
                                locator="S1",
                                evidence_basis="markdown_link_extraction",
                                surrounding_text=surr[:240])
                    stats["stage1_dossier_links"] += 1
                except Exception as e:
                    stats["errors"].append(f"S1 dossier md_link {qid} {norm}: {e}")

            # bare URLs
            for raw_url in extract_bare_urls(text):
                norm = normalise_url(raw_url)
                if not norm:
                    continue
                eid = url_id(norm)
                surr = surrounding_text(text, raw_url)
                try:
                    session.run(S1_A, ext_id=eid, url=norm, title="",
                                url_origin="dossier_bare_url",
                                first_seen_in_dossier=qid,
                                evidence_basis="bare_url_extraction",
                                source_id=qid)
                    session.run(S1_B, source_id=qid, ext_id=eid,
                                locator="bare",
                                evidence_basis="bare_url_extraction",
                                surrounding_text=surr[:240])
                    stats["stage1_dossier_bare_urls"] += 1
                except Exception as e:
                    stats["errors"].append(f"S1 dossier bare_url {qid} {norm}: {e}")

        print(f"  Stage 1 done: {stats['stage1_dossier_links']} md_links, "
              f"{stats['stage1_dossier_bare_urls']} bare_urls processed")

        # ── Stage 2: Stamp existing :Quelle nodes that have .url ─────────────
        print("Stage 2: stamping pre-existing Quelle.url nodes as :ExternalLink...")
        existing_url_nodes = session.run(
            "MATCH (q:Quelle) WHERE q.url IS NOT NULL AND q.url <> '' "
            "RETURN q.id AS qid, q.url AS raw_url, "
            "       coalesce(q.name, q.title, '') AS title, "
            "       q.quelltyp AS qt"
        ).data()
        print(f"  Found {len(existing_url_nodes)} nodes with .url")

        for q in existing_url_nodes:
            raw_url = q["raw_url"]
            norm = normalise_url(raw_url)
            if not norm:
                continue
            eid = url_id(norm)
            title = q.get("title") or ""
            qid = q["qid"]

            try:
                # If the node's own id matches the derived id, just stamp it
                if qid == eid:
                    session.run(S1_STAMP_EXISTING, existing_id=qid)
                else:
                    # MERGE a canonical :ExternalLink and then link original to it
                    session.run(S1_A_EXISTING, ext_id=eid, url=norm, title=title,
                                source_id=qid)
                    # If the original node isn't the canonical node, link it
                    # (only if source is also :Quelle, which it is)
                    session.run(
                        "MATCH (src:Quelle {id: $src_id}) "
                        "MATCH (ext:ExternalLink {id: $ext_id}) "
                        "WHERE src.id <> ext.id "
                        "MERGE (src)-[z:ZITIERT_QUELLE]->(ext) "
                        "ON CREATE SET z.locator='pre_existing', "
                        "  z.evidence_basis='pre_existing_quelle_url', "
                        "  z.evidence_origin='source_curated', "
                        "  z.evidence_source_id=src.id, "
                        "  z.evidence_confidence='belegt', "
                        "  z.migration_origin='mig_s1_url_extract'",
                        src_id=qid, ext_id=eid
                    )
                    # Also stamp the original node itself as ExternalLink
                    session.run(S1_STAMP_EXISTING, existing_id=qid)
                stats["stage2_pre_existing"] += 1
            except Exception as e:
                stats["errors"].append(f"S2 pre-existing {qid}: {e}")

        print(f"  Stage 2 done: {stats['stage2_pre_existing']} pre-existing nodes stamped")

        # ── Stage 3: Scan edge evidence_excerpt for URLs ──────────────────────
        print("Stage 3: scanning edge evidence_excerpt for URLs...")
        edge_url_rows = session.run(
            "MATCH (a)-[r]->(b) "
            "WHERE r.evidence_excerpt IS NOT NULL "
            "  AND r.evidence_excerpt =~ '.*https?://.*' "
            "RETURN id(r) AS rid, type(r) AS rtype, "
            "       r.evidence_excerpt AS excerpt, "
            "       coalesce(a.id, toString(id(a))) AS aid"
        ).data()
        print(f"  Found {len(edge_url_rows)} edges with URL in evidence_excerpt")

        for e in edge_url_rows:
            excerpt = e["excerpt"] or ""
            aid = e["aid"]
            rid_str = str(e["rid"])
            for raw_url in BARE_URL_RE.findall(excerpt):
                norm = normalise_url(raw_url)
                if not norm:
                    continue
                eid = url_id(norm)
                try:
                    session.run(S1_A, ext_id=eid, url=norm, title="",
                                url_origin="edge_property",
                                first_seen_in_dossier=None,
                                evidence_basis="edge_excerpt_extraction",
                                source_id=rid_str)
                    # Link from the source node (a) of the edge if it's a :Quelle
                    session.run(
                        "MATCH (src) WHERE src.id = $aid "
                        "MATCH (ext:ExternalLink {id: $ext_id}) "
                        "MERGE (src)-[z:ZITIERT_QUELLE]->(ext) "
                        "ON CREATE SET z.locator='edge_excerpt', "
                        "  z.evidence_basis='edge_excerpt_extraction', "
                        "  z.evidence_origin='source_curated', "
                        "  z.evidence_source_id=$aid, "
                        "  z.evidence_confidence='belegt', "
                        "  z.evidence_excerpt=$excerpt, "
                        "  z.migration_origin='mig_s1_url_extract'",
                        aid=aid, ext_id=eid, excerpt=excerpt[:240]
                    )
                    stats["stage3_edge_urls"] += 1
                except Exception as ex:
                    stats["errors"].append(f"S3 edge {rid_str} {norm}: {ex}")

        print(f"  Stage 3 done: {stats['stage3_edge_urls']} edge URL references processed")

        # ── Stage 4: Scan node URL properties ────────────────────────────────
        print("Stage 4: scanning node URL properties (website, project_url, etc.)...")
        url_props = ["website", "link", "homepage", "project_url", "source_url", "official_url"]
        for prop in url_props:
            rows = session.run(
                f"MATCH (n) WHERE n.`{prop}` IS NOT NULL "
                f"  AND n.`{prop}` =~ '^https?://.*' "
                f"  AND NOT n:Quelle "
                f"RETURN n.id AS nid, labels(n) AS lbls, n.`{prop}` AS raw_url",
            ).data()
            for row in rows:
                raw_url = row["raw_url"]
                norm = normalise_url(raw_url)
                if not norm:
                    continue
                eid = url_id(norm)
                nid = row["nid"]
                try:
                    session.run(S1_A, ext_id=eid, url=norm, title="",
                                url_origin="node_property",
                                first_seen_in_dossier=None,
                                evidence_basis="node_property_extraction",
                                source_id=nid)
                    session.run(S1_C, source_id=nid, ext_id=eid, property_name=prop)
                    stats["stage4_node_prop_urls"] += 1
                except Exception as ex:
                    stats["errors"].append(f"S4 node_prop {nid}.{prop}: {ex}")

        print(f"  Stage 4 done: {stats['stage4_node_prop_urls']} node-property URLs processed")

        # ── Stage 5: Normalize all :ExternalLink.url in-place ────────────────
        print("Stage 5: normalizing all :ExternalLink.url values...")
        all_ext = session.run(
            "MATCH (e:ExternalLink) WHERE e.url IS NOT NULL RETURN e.id AS eid, e.url AS url"
        ).data()
        fixed = 0
        for node in all_ext:
            norm = normalise_url(node["url"])
            if norm and norm != node["url"]:
                session.run(
                    "MATCH (e:ExternalLink {id: $eid}) SET e.url = $url",
                    eid=node["eid"], url=norm
                )
                fixed += 1
        stats["stage5_url_normalized"] = fixed
        print(f"  Stage 5 done: {fixed} URLs normalized")

    driver.close()
    return stats


def run_acceptance_gates(session) -> dict:
    gates = {}
    gates["ext_links_without_url"] = session.run(
        "MATCH (e:ExternalLink) WHERE e.url IS NULL RETURN count(e) AS c"
    ).single()["c"]
    gates["new_ext_links_without_origin"] = session.run(
        "MATCH (e:ExternalLink) WHERE e.migration_origin CONTAINS 'mig_s1' "
        "  AND e.url_origin IS NULL RETURN count(e) AS c"
    ).single()["c"]
    gates["new_ext_links_without_citation"] = session.run(
        "MATCH (e:ExternalLink) WHERE e.migration_origin CONTAINS 'mig_s1' "
        "  AND NOT exists {()-[:ZITIERT_QUELLE|HAS_SOURCE_LINK]->(e)} "
        "RETURN count(e) AS c"
    ).single()["c"]
    gates["distinct_urls"] = session.run(
        "MATCH (e:ExternalLink) RETURN count(DISTINCT e.url) AS c"
    ).single()["c"]
    gates["url_with_utm"] = session.run(
        "MATCH (e:ExternalLink) WHERE e.url CONTAINS 'utm_' RETURN count(e) AS c"
    ).single()["c"]
    gates["url_with_trailing_slash"] = session.run(
        "MATCH (e:ExternalLink) WHERE e.url ENDS WITH '/' "
        "  AND size(e.url) > 12 RETURN count(e) AS c"
    ).single()["c"]
    url_origin_dist = session.run(
        "MATCH (e:ExternalLink) RETURN e.url_origin AS origin, count(e) AS cnt"
    ).data()
    gates["url_origin_distribution"] = url_origin_dist
    return gates


def main() -> int:
    print("=" * 60)
    print("Agent S1 — URL extractor")
    print("=" * 60)

    RUN_DIR.mkdir(parents=True, exist_ok=True)

    stats = run_s1()

    print("\nRunning acceptance gates...")
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(
        uri, auth=(user, password),
        notifications_disabled_categories=["DEPRECATION", "UNRECOGNIZED"],
    )
    with driver.session(database=database) as session:
        gates = run_acceptance_gates(session)
    driver.close()

    print("\n── Acceptance gates ──────────────────────────────────────")
    passed = True
    for k, v in gates.items():
        if k == "url_origin_distribution":
            print(f"  url_origin_distribution: {v}")
            if len(v) < 3:
                print("  WARN: fewer than 3 origin categories")
        elif k == "distinct_urls":
            ok = v >= 500
            print(f"  {k}: {v}  {'OK' if ok else 'WARN (expected ≥500)'}")
            if not ok:
                print(f"  NOTE: below target of 500 distinct URLs")
        elif k in ("ext_links_without_url", "new_ext_links_without_origin",
                   "url_with_utm", "url_with_trailing_slash"):
            ok = v == 0
            print(f"  {k}: {v}  {'OK' if ok else 'FAIL'}")
            if not ok:
                passed = False
        elif k == "new_ext_links_without_citation":
            ok = v == 0
            print(f"  {k}: {v}  {'OK' if ok else 'WARN (orphan ExternalLinks)'}")
            if not ok:
                print(f"  NOTE: {v} ExternalLinks without citation (may be acceptable for node-prop origins)")
        else:
            print(f"  {k}: {v}")

    report = {"stats": stats, "gates": {k: (v if k != "url_origin_distribution" else v) for k, v in gates.items()}}
    REPORT_FILE.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(f"\nReport written to {REPORT_FILE}")

    if stats["errors"]:
        print(f"\nErrors ({len(stats['errors'])}):")
        for err in stats["errors"][:20]:
            print(f"  {err}")
        if len(stats["errors"]) > 20:
            print(f"  ... and {len(stats['errors']) - 20} more (see report)")

    # Write flag
    FLAG_FILE.write_text(
        f"PHASE_S1_DONE\nextracted_at: 2026-05-21\n"
        f"stage1_dossier_links: {stats['stage1_dossier_links']}\n"
        f"stage1_bare_urls: {stats['stage1_dossier_bare_urls']}\n"
        f"stage2_pre_existing: {stats['stage2_pre_existing']}\n"
        f"stage3_edge_urls: {stats['stage3_edge_urls']}\n"
        f"stage4_node_props: {stats['stage4_node_prop_urls']}\n"
        f"stage5_url_normalized: {stats.get('stage5_url_normalized', 0)}\n"
        f"distinct_urls: {gates.get('distinct_urls', '?')}\n"
        f"errors: {len(stats['errors'])}\n",
        encoding="utf-8"
    )
    print(f"Flag written to {FLAG_FILE}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
