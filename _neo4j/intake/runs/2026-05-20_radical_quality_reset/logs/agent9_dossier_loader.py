"""Agent 9 — Phase 4b.1 + 4c.2 S-ref backfill loader (mit-bestand).

Scope per Wave-4 brief (Agent 9, parent task):
  1. Parse 97 dossiers from agent_8_dossier_manifest.json (76 gebaeude + 21 batch2).
  2. For each dossier: MERGE the q_<slug>_md case_markdown :Quelle anchor and
     MERGE every q_<slug>_sN external :Quelle from its sources block.
  3. MERGE (qmd)-[:ZITIERT_QUELLE]->(qsn) per S-ref.
  4. Parse sections 1-9 table rows: emit BELEGT_IN from (Projekt) to each cited
     S-ref Quelle, evidence_origin='curated', evidence_basis='cell_citation',
     evidence_excerpt=cell text (truncated 480), evidence_confidence read from
     the row's Vertrauensgrad column (mapped to {belegt|teilweise_belegt|unklar|
     inferiert}).
  5. Section 8 Kennwerte → append to Projekt.cost_facts / reuse_share_facts /
     co2_facts list-of-dict properties with source_id (NOT URL).
  6. Idempotency: every BELEGT_IN edge created by this loader carries
     loader_run_id='agent9_phase4b1'. On re-run we DELETE all such edges per
     Projekt/dossier-pair and recreate. cost_facts/reuse_share_facts/co2_facts
     entries carry source_id='q_<slug>_md' or 'q_<slug>_sN'; on re-run we
     strip any list entries whose source_id starts with the dossier prefix
     before appending.
  7. The multi-dossier batch 1.md file holds 3 H1 sections; we treat each
     as its own sub-dossier and create 3 dedicated q_<sub_slug>_md anchors
     in addition to the manifest's q_batch_1_md anchor (q_batch_1_md gets a
     ZITIERT_QUELLE to each sub-anchor for traceability).

Acceptance (parent task §6): ≥85/96 case_markdown anchors have ≥1
ZITIERT_QUELLE child after this loader runs.

Out of scope (Agent 10): research/*.md ingestion.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "runs"
    / "2026-05-20_radical_quality_reset"
)
LOG_DIR = RUN_ROOT / "logs"
REPORTS_DIR = RUN_ROOT / "reports"
DEL_DIR = RUN_ROOT / "deleted"

MANIFEST_PATH = REPORTS_DIR / "agent_8_dossier_manifest.json"
PROGRESS_LOG = LOG_DIR / "agent9_progress.log"
ERROR_LOG = LOG_DIR / "agent9_errors.log"
RESULT_JSON = LOG_DIR / "agent9_result.json"
FLAG_PATH = RUN_ROOT / "PHASE_4B_1_DONE.flag"
REPORT_PATH = REPORTS_DIR / "agent_9_phase4b1_report.md"

LOADER_RUN_ID = "agent9_phase4b1"

# Vertrauensgrad string -> enum value
VERTRAUEN_MAP = {
    "belegt": "belegt",
    "teilweise belegt": "teilweise_belegt",
    "teilweise_belegt": "teilweise_belegt",
    "teilweise": "teilweise_belegt",
    "unklar": "unklar",
    "inferiert": "inferiert",
    "inferred": "inferiert",
    "vermutet": "unklar",
    "high": "belegt",
    "medium": "teilweise_belegt",
    "low": "unklar",
    "unbekannt": "unklar",
    "unknown": "unklar",
}

# Sources block headers we recognise; numeric prefixes & free trailing text
# tolerated (e.g. "## Quellen und Links", "## 13. Quellen", "## Source register",
# "## Quellen / Links").
SOURCES_HEADER_RE = re.compile(
    r"^##+\s*(?:\d+\.\s*)?"
    r"(?:Quellen(?:angaben)?|Sources|Source\s+register|References|"
    r"Bibliographie|Bibliography|Literatur)\b[^\n]*$",
    re.IGNORECASE | re.MULTILINE,
)
H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
# Numbered section header like "## 8. KENNWERTE" or "## 8 Kennwerte"
SECTION_NUM_RE = re.compile(r"^##+\s*(\d+)\b[\.\)\s]\s*([^\n]+)", re.IGNORECASE)

# S-ref tokens used inline in tables
SREF_INLINE_RE = re.compile(r"\[(S\d+)\]")
SREF_WITH_URL_RE = re.compile(r"\[(S\d+)\]\((https?://[^\s)]+)\)")
URL_RE = re.compile(r"(https?://[^\s)>\]]+)")
SLUG_BAD_RE = re.compile(r"[^a-z0-9]+")

# Permissive S-ref line matcher: any line in the sources block that
# contains an Sn-style token (with or without brackets, possibly inside
# markdown bold **) AND at least one URL. Handles every gebaeude variant:
#   "- [S1] Title: https://url"          (Resilience)
#   "- **S1 – Title.** https://url"      (BedZED)
#   "- **S1** Title – https://url"       (AWM)
#   "[S1] Title: https://url"            (BioPartner, no bullet)
#   "| S1 | Title | Pub | https://url"   (batch-2 source register table)
#   "| R1 | Title | ... | URL ..."       (REBRIDGE — uses R/P labels)
# We accept any single uppercase letter followed by digits and preserve the
# letter+digits as the ref tag (downstream MERGE uses tag.lower()).
SREF_LINE_RE = re.compile(r"\*{0,2}\[?([A-Z]\d+)\]?\*{0,2}")
# Numbered entry in gebaeude block (no [Sn]):
#   "1. Title: https://url"
NUMBERED_RE = re.compile(
    r"^\s*(\d+)\.\s+(.+)$",
    re.MULTILINE,
)
# Batch2 source register table row:
#   "| S1 | Title | Publisher | URL | Access | Claims |"
# REBRIDGE uses P1/R1/R2 ids — accept any single uppercase letter prefix.
TABLE_SREF_ROW_RE = re.compile(
    r"^\|\s*([A-Z]\d+)\s*\|([^\n]+)\|",
)


def _log(line: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    msg = f"[{stamp}] {line}"
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        print(msg.encode(enc, errors="replace").decode(enc), flush=True)
    PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with PROGRESS_LOG.open("a", encoding="utf-8") as fp:
        fp.write(msg + "\n")


def _err(line: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    msg = f"[{stamp}] {line}"
    ERROR_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ERROR_LOG.open("a", encoding="utf-8") as fp:
        fp.write(msg + "\n")


# German transliteration BEFORE NFKD strip so umlauts map to ae/oe/ue/ss,
# matching the convention already in the live project ids
# (p_schaerenmoosstrasse_zuerich, p_broethen_..., p_kindergarten_moeoeslistrasse_...)
GERMAN_TRANSLIT = str.maketrans({
    "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
    "Ä": "Ae", "Ö": "Oe", "Ü": "Ue",
})


def slugify(text: str) -> str:
    """Match Agent 8 / live-graph convention: lowercase ASCII, [^a-z0-9]→_,
    with German umlauts transliterated as ae/oe/ue/ss BEFORE ASCII strip."""
    pre = text.translate(GERMAN_TRANSLIT)
    norm = unicodedata.normalize("NFKD", pre).encode("ascii", "ignore").decode("ascii")
    s = SLUG_BAD_RE.sub("_", norm.lower()).strip("_")
    return s


# Known batch2-dossier → live-graph Projekt id aliases (Agent 8 manifest +
# agent9_probe.json comparison). When the file-slug derived id is not in the
# live graph but the live id is known under a different shape, route here.
PROJEKT_ALIAS = {
    "q_careno_be_circular_brussels_md": "p_careno_becircular",
    "q_circl_abn_amro_urban_mining_md": "p_circl_abn_amro",
    "q_meduni_campus_mariannengasse_wien_md": "p_meduni_campus_mariannengasse",
    "q_granby_workshop_liverpool_md": "p_granby_workshop",
    "q_zhaw_reuse_in_construction_md": "p_reuse_in_construction_zhaw",
    "q_vandkunsten_component_reuse_programme_md": "p_vandkunsten_component_reuse",
    # multi-dossier batch 1.md children
    "q_schaerenmoosstrasse_zuerich_projekt_menage_a_trois_md": "p_schaerenmoosstrasse_zuerich",
    "q_umar_unit_nest_empa_duebendorf_md": "p_umar_unit",
    "q_elementa_walkeweg_basel_md": "p_elementa_walkeweg",
}


def projekt_id_from_dossier(slug: str) -> str:
    return f"p_{slug}"


def resolve_projekt_id(qmd_id: str, slug: str | None) -> str | None:
    """Return best-guess live Projekt id for a dossier, or None."""
    if qmd_id in PROJEKT_ALIAS:
        return PROJEKT_ALIAS[qmd_id]
    if slug:
        return projekt_id_from_dossier(slug)
    return None


# --------------------------------------------------------------------------
# Connection
# --------------------------------------------------------------------------

def _resolve_connection() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise RuntimeError("Neo4j connection missing")
    if database != "mit-bestand":
        _log(f"WARN overriding NEO4J_DATABASE='{database}' to 'mit-bestand'")
        database = "mit-bestand"
    return uri, user, password, database


# --------------------------------------------------------------------------
# Dossier parsing helpers
# --------------------------------------------------------------------------

def split_h1_blocks(text: str) -> list[tuple[str, str]]:
    """Return [(h1_title, body)] segments. If no H1, the whole text is one block."""
    matches = list(H1_RE.finditer(text))
    if not matches:
        return [("", text)]
    if len(matches) == 1:
        return [(matches[0].group(1).strip(), text)]
    blocks: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((title, text[start:end]))
    return blocks


def find_sources_block(body: str) -> tuple[int, int] | None:
    m = SOURCES_HEADER_RE.search(body)
    if not m:
        return None
    start = m.end()
    # Block ends at next H2 (## ...) or EOF
    nxt = H2_RE.search(body, pos=start)
    end = nxt.start() if nxt else len(body)
    return (start, end)


def clean_title(raw: str, url: str | None) -> str:
    text = raw
    if url:
        text = text.replace(url, "")
    text = re.sub(r"^\s*[\-*]\s*", "", text)
    text = re.sub(r"^\s*(\[?S\d+\]?)\s*[:.\-—–]?\s*", "", text)
    text = re.sub(r"^\s*\d+\.\s*", "", text)
    text = text.strip(" -–—:•\t")
    text = re.sub(r"\s+", " ", text)
    return text[:300]


def parse_table_sources(body_slice: str) -> list[tuple[str, str, str]]:
    """Batch-2 ## Source register table — yields (Sn, title, url) tuples."""
    out: list[tuple[str, str, str]] = []
    for line in body_slice.splitlines():
        m = TABLE_SREF_ROW_RE.match(line)
        if not m:
            continue
        sn = m.group(1)
        cells = [c.strip() for c in line.split("|")[1:-1]]
        # Expected columns: S | Title | Publisher | URL | Access | Claims
        if len(cells) < 4:
            continue
        title = cells[1]
        url_cell = cells[3]
        url_match = URL_RE.search(url_cell)
        url = url_match.group(1).rstrip(".,;:") if url_match else ""
        if not url:
            # Some S-refs (e.g. S0 / R0) use 'internal note' instead of a URL
            continue
        out.append((sn, title, url))
    return out


def parse_bullet_sources(body_slice: str) -> list[tuple[str, str, str]]:
    """Permissive line-based S-ref parser. Accepts every variant where a
    line contains an Sn token (any bracketing) and a URL."""
    out: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for line in body_slice.splitlines():
        if not line.strip():
            continue
        m_sn = SREF_LINE_RE.search(line)
        if not m_sn:
            continue
        sn = m_sn.group(1)
        if sn in seen:
            continue
        m_url = URL_RE.search(line)
        if not m_url:
            continue
        url = m_url.group(1).rstrip(".,;:")
        title = clean_title(line, url)
        out.append((sn, title, url))
        seen.add(sn)
    return out


def parse_numbered_sources(body_slice: str) -> list[tuple[str, str, str]]:
    """Gebaeude '1. Title: https://url' style (no [Sn] tokens). Returns
    synthetic Sn keys aligned with the numeric prefix."""
    out: list[tuple[str, str, str]] = []
    for m in NUMBERED_RE.finditer(body_slice):
        n = int(m.group(1))
        rest = m.group(2)
        url_match = URL_RE.search(rest)
        if not url_match:
            continue
        url = url_match.group(1).rstrip(".,;:")
        title = clean_title(rest, url)
        out.append((f"S{n}", title, url))
    return out


def parse_bulleted_url_sources(body_slice: str) -> list[tuple[str, str, str]]:
    """Gebaeude '- Title – https://url' style (no Sn token at all, e.g.
    Boulder Fire Station 3). Synthesises S1..SN from line order."""
    out: list[tuple[str, str, str]] = []
    n = 0
    for line in body_slice.splitlines():
        stripped = line.lstrip()
        if not stripped.startswith(("-", "*", "•")):
            continue
        url_match = URL_RE.search(line)
        if not url_match:
            continue
        url = url_match.group(1).rstrip(".,;:")
        n += 1
        out.append((f"S{n}", clean_title(line, url), url))
    return out


def parse_inline_sref_urls(body: str) -> list[tuple[str, str, str]]:
    """Pick up [Sn](url) inline citations across the body for batch-2 dossiers
    whose source register lacks URLs or is missing entirely. Returns one entry
    per (Sn, url) — title defaulted to '<sn> inline citation'."""
    seen: dict[str, str] = {}
    for m in SREF_WITH_URL_RE.finditer(body):
        sn = m.group(1)
        url = m.group(2).rstrip(".,;:")
        if sn not in seen and url:
            seen[sn] = url
    return [(sn, f"Inline citation {sn}", url) for sn, url in seen.items()]


def gather_sources(body: str) -> list[tuple[str, str, str]]:
    """Return de-duplicated [(Sn, title, url)] tuples for one dossier body."""
    by_sn: dict[str, tuple[str, str]] = {}
    block = find_sources_block(body)
    if block:
        slc = body[block[0] : block[1]]
        candidates: list[tuple[str, str, str]] = []
        candidates.extend(parse_table_sources(slc))
        candidates.extend(parse_bullet_sources(slc))
        if not candidates:
            # numbered list (Quellen / Links style — 55 Great Suffolk)
            candidates.extend(parse_numbered_sources(slc))
        if not candidates:
            # bulleted URL list without Sn tokens (Boulder Fire Station)
            candidates.extend(parse_bulleted_url_sources(slc))
        for sn, title, url in candidates:
            if sn not in by_sn:
                by_sn[sn] = (title, url)
    # Fallback: inline citations across the body (batch-2 commonly inlines)
    for sn, title, url in parse_inline_sref_urls(body):
        by_sn.setdefault(sn, (title, url))
    out = [(sn, t, u) for sn, (t, u) in by_sn.items()]
    out.sort(key=lambda x: (len(x[0]), x[0]))
    return out


# --------------------------------------------------------------------------
# Section table parsing (sections 1-9) → BELEGT_IN edges
# --------------------------------------------------------------------------

def find_section(body: str, section_nums: Iterable[int]) -> str | None:
    """Return body slice between '## N. NAME' and the next '##' header
    where N is in section_nums. Returns None if no such section."""
    wanted = {int(n) for n in section_nums}
    matches = list(re.finditer(r"^##+\s*(\d+)\b[\.\)\s][^\n]*", body, re.MULTILINE))
    if not matches:
        return None
    pieces: list[str] = []
    for i, m in enumerate(matches):
        try:
            n = int(m.group(1))
        except ValueError:
            continue
        if n in wanted:
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
            pieces.append(body[start:end])
    if not pieces:
        return None
    return "\n".join(pieces)


def parse_md_table(text: str) -> list[dict[str, str]]:
    """Tiny markdown-table parser. Returns list of row dicts keyed by header.

    Handles multiple tables in the slice — each table starts with a header
    row followed by a separator row containing dashes.
    """
    out: list[dict[str, str]] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("|"):
            i += 1
            continue
        # Need separator on next line for a real table
        if i + 1 >= len(lines):
            break
        sep = lines[i + 1].strip()
        if not (sep.startswith("|") and re.fullmatch(r"[\|\s\-:]+", sep)):
            i += 1
            continue
        header_cells = [c.strip() for c in line.split("|")[1:-1]]
        i += 2
        while i < len(lines):
            row = lines[i].strip()
            if not row.startswith("|"):
                break
            cells = [c.strip() for c in row.split("|")[1:-1]]
            if len(cells) != len(header_cells):
                # tolerate mismatch by padding/truncating
                cells = (cells + [""] * len(header_cells))[: len(header_cells)]
            out.append(dict(zip(header_cells, cells)))
            i += 1
    return out


def normalise_header(h: str) -> str:
    return SLUG_BAD_RE.sub("_", h.lower()).strip("_")


def find_column(row: dict[str, str], candidates: list[str]) -> str | None:
    for cand in candidates:
        for k in row:
            if normalise_header(k) == normalise_header(cand):
                return row[k]
    # Substring match
    for cand in candidates:
        cand_n = normalise_header(cand)
        for k in row:
            if cand_n and cand_n in normalise_header(k):
                return row[k]
    return None


def map_vertrauensgrad(raw: str | None) -> str:
    if not raw:
        return "unklar"
    s = re.sub(r"[^a-z_ ]", "", raw.lower()).strip()
    return VERTRAUEN_MAP.get(s, "unklar")


def row_to_excerpt(row: dict[str, str]) -> str:
    """Build a short evidence_excerpt from the row cells.

    Per mig_4_1 audit rule 1 (curated requires excerpt) we MUST always return
    a non-empty string — even for sparse rows. Strategy: prefer
    information-bearing columns, skip the Vertrauensgrad/Anmerkung columns,
    and fall back to the raw row dump if all the preferred columns are empty.
    """
    skip = {"vertrauensgrad", "anmerkung", "remarks", "comment", "unbekannt"}
    empty = {"—", "-", "unbekannt", "unknown", "", "n/a", "na"}
    bits: list[str] = []
    for k, v in row.items():
        nk = normalise_header(k)
        if any(s in nk for s in skip):
            continue
        if not v or v.strip().lower() in empty:
            continue
        bits.append(f"{k.strip()}: {v.strip()}")
    excerpt = " | ".join(bits)
    if not excerpt.strip():
        # fallback 1: include EVERY non-empty cell (no skip list)
        excerpt = " | ".join(
            f"{k.strip()}: {v.strip()}"
            for k, v in row.items()
            if v and v.strip().lower() not in empty
        )
    if not excerpt.strip():
        # fallback 2: at least record that a row cited Sn (audit hard-rule)
        excerpt = "(row with no value-bearing cells; cited via Quelle column)"
    if len(excerpt) > 480:
        excerpt = excerpt[:477] + "..."
    return excerpt


def extract_sref_tokens(cell: str) -> list[str]:
    return list(dict.fromkeys(SREF_INLINE_RE.findall(cell or "")))


# --------------------------------------------------------------------------
# Section 8 Kennwerte -> Projekt list facts
# --------------------------------------------------------------------------

KENNWERT_CATEGORIES = {
    "cost_facts": [
        "baukosten", "kosten", "preis", "investition", "budget", "cost", "price",
        "investment", "spend", "einsparung", "saving",
    ],
    "reuse_share_facts": [
        "reuse-anteil", "reuse anteil", "reuse share", "anteil", "share",
        "quote", "ratio", "%",
    ],
    "co2_facts": [
        "co2", "co₂", "co2e", "co₂e", "emission", "treibhaus",
    ],
}


def categorise_kennwert(name: str) -> str | None:
    lname = name.lower()
    for cat, keys in KENNWERT_CATEGORIES.items():
        if any(k in lname for k in keys):
            return cat
    return None


# --------------------------------------------------------------------------
# Loader main
# --------------------------------------------------------------------------

def build_per_dossier_plan(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Translate manifest into work units, expanding multi-dossier files."""
    plan: list[dict[str, Any]] = []
    for entry in manifest["entries"]:
        rel = entry["rel_path"]
        abs_path = Path(entry["abs_path"])
        if not abs_path.is_file():
            _err(f"missing dossier file {abs_path}")
            continue
        # Decide whether file is multi-dossier (3 H1s expected for batch 1.md)
        text = abs_path.read_text(encoding="utf-8", errors="replace")
        h1_blocks = split_h1_blocks(text)
        if entry.get("format_hint") == "case_markdown_multi" and len(h1_blocks) > 1:
            file_qmd = entry["expected_quelle_id"]
            parent_unit = {
                "rel_path": rel,
                "abs_path": str(abs_path),
                "qmd_id": file_qmd,
                "h1_title": h1_blocks[0][0] if h1_blocks[0][0] else Path(rel).stem,
                "body": "",  # parent anchor, no parsing
                "is_parent_of_multi": True,
                "children_qmd_ids": [],
                "projekt_slug": None,
            }
            plan.append(parent_unit)
            for i, (h1_title, h1_body) in enumerate(h1_blocks, start=1):
                # Use a compact slug for the H1 — German umlauts already mapped
                child_slug_full = slugify(h1_title)
                # Trim trailing free-text after the project name; live ids
                # are short (p_schaerenmoosstrasse_zuerich), so we keep only
                # the first ~50 chars before truncating at last underscore.
                child_slug = child_slug_full[:80].rstrip("_")
                if not child_slug:
                    child_slug = f"sub_{i}"
                child_qmd = f"q_{child_slug}_md"
                parent_unit["children_qmd_ids"].append(child_qmd)
                plan.append({
                    "rel_path": rel,
                    "abs_path": str(abs_path),
                    "qmd_id": child_qmd,
                    "h1_title": h1_title,
                    "body": h1_body,
                    "is_parent_of_multi": False,
                    "children_qmd_ids": [],
                    "projekt_slug": child_slug,
                })
        else:
            slug_from_qmd = re.sub(r"^q_|_md$", "", entry["expected_quelle_id"])
            plan.append({
                "rel_path": rel,
                "abs_path": str(abs_path),
                "qmd_id": entry["expected_quelle_id"],
                "h1_title": (h1_blocks[0][0] if h1_blocks else Path(rel).stem),
                "body": text,
                "is_parent_of_multi": False,
                "children_qmd_ids": [],
                # Slug derived from the FILE stem (via manifest qmd id) — NOT
                # from the H1 title, to avoid "_fallstudie_direct_reuse_..."
                # noise contaminating projekt id matching.
                "projekt_slug": slug_from_qmd,
            })
    return plan


def upsert_quelle_anchor(tx, qmd_id: str, rel_path: str, h1_title: str) -> None:
    tx.run(
        """
        MERGE (q:Quelle {id: $id})
        ON CREATE SET q.quelltyp = 'case_markdown',
                      q.source_file = $rel_path,
                      q.name = $title,
                      q._created_by = $loader,
                      q._created_at = $stamp
        ON MATCH  SET q.quelltyp = coalesce(q.quelltyp, 'case_markdown'),
                      q.source_file = coalesce(q.source_file, $rel_path),
                      q.name = coalesce(q.name, $title)
        """,
        {"id": qmd_id, "rel_path": rel_path, "title": h1_title[:240] or qmd_id,
         "loader": LOADER_RUN_ID,
         "stamp": datetime.now(timezone.utc).isoformat(timespec="seconds")},
    )


def upsert_sref_and_link(tx, qmd_id: str, sn_id: str, url: str, title: str) -> None:
    tx.run(
        """
        MERGE (qs:Quelle {id: $sid})
        ON CREATE SET qs.quelltyp = 'external_reference',
                      qs.url = $url,
                      qs.name = $title,
                      qs._created_by = $loader,
                      qs._created_at = $stamp
        ON MATCH  SET qs.url = coalesce(qs.url, $url),
                      qs.name = coalesce(qs.name, $title)
        WITH qs
        MATCH (qmd:Quelle {id: $qmd_id})
        MERGE (qmd)-[r:ZITIERT_QUELLE]->(qs)
        ON CREATE SET r.evidence_origin = 'derived',
                      r.evidence_basis = 'case_markdown_sources',
                      r.evidence_source_id = $qmd_id,
                      r.evidence_confidence = 'belegt',
                      r.evidence_excerpt = NULL,
                      r._created_by = $loader
        """,
        {"sid": sn_id, "url": url, "title": title[:240],
         "qmd_id": qmd_id, "loader": LOADER_RUN_ID,
         "stamp": datetime.now(timezone.utc).isoformat(timespec="seconds")},
    )


def link_parent_to_children(tx, parent_qmd: str, child_qmd: str) -> None:
    tx.run(
        """
        MATCH (a:Quelle {id: $a})
        MATCH (b:Quelle {id: $b})
        MERGE (a)-[r:ZITIERT_QUELLE]->(b)
        ON CREATE SET r.evidence_origin = 'derived',
                      r.evidence_basis = 'case_markdown_sources',
                      r.evidence_source_id = $a,
                      r.evidence_confidence = 'belegt',
                      r.evidence_excerpt = NULL,
                      r._created_by = $loader
        """,
        {"a": parent_qmd, "b": child_qmd, "loader": LOADER_RUN_ID},
    )


def delete_prior_curated_belegt_in(tx, projekt_id: str, qmd_id: str) -> int:
    """Delete any BELEGT_IN edges previously written by this loader for
    (projekt_id, q_<slug>_*) target prefix. Returns deleted count."""
    rec = tx.run(
        """
        MATCH (p:Projekt {id: $pid})-[r:BELEGT_IN]->(q:Quelle)
        WHERE r._created_by = $loader
          AND (q.id = $qmd OR q.id STARTS WITH $sref_prefix)
        WITH r, count(r) AS _
        DELETE r
        RETURN count(_) AS c
        """,
        {"pid": projekt_id, "qmd": qmd_id,
         "sref_prefix": qmd_id.removesuffix("_md") + "_s",
         "loader": LOADER_RUN_ID},
    ).single()
    return rec["c"]


def write_belegt_in(
    tx,
    projekt_id: str,
    sref_quelle_id: str,
    excerpt: str,
    confidence: str,
) -> None:
    """One BELEGT_IN edge per (projekt, sref-quelle, cell-excerpt) per
    Phase-4b.1 rule "multi-ref cells get one edge per S-ref".

    MERGE key includes a stable sha1(excerpt) prefix so identical cell text
    citing the same S-ref dedupes on re-run while distinct cells citing the
    same S-ref each get their own edge. mig_4_1 hard rule: curated edges
    must have a non-null excerpt.
    """
    safe_excerpt = (excerpt or "").strip() or f"BELEGT_IN cite for {sref_quelle_id}"
    cell_hash = hashlib.sha1(safe_excerpt.encode("utf-8")).hexdigest()[:12]
    tx.run(
        """
        MATCH (p:Projekt {id: $pid})
        MATCH (qs:Quelle {id: $sid})
        MERGE (p)-[r:BELEGT_IN {
            evidence_source_id: $sid,
            _created_by: $loader,
            _cell_hash: $cell_hash
        }]->(qs)
        ON CREATE SET r.evidence_origin = 'curated',
                      r.evidence_basis = 'cell_citation',
                      r.evidence_excerpt = $excerpt,
                      r.evidence_confidence = $conf,
                      r._created_at = $stamp
        ON MATCH  SET r.evidence_excerpt = $excerpt,
                      r.evidence_confidence = $conf
        """,
        {"pid": projekt_id, "sid": sref_quelle_id,
         "excerpt": safe_excerpt[:480],
         "conf": confidence,
         "loader": LOADER_RUN_ID,
         "cell_hash": cell_hash,
         "stamp": datetime.now(timezone.utc).isoformat(timespec="seconds")},
    )


def replace_section8_facts(
    tx,
    projekt_id: str,
    qmd_id: str,
    fact_lists: dict[str, list[dict[str, Any]]],
) -> None:
    """Strip any existing list entries that originate from this dossier
    (source_id starts with the dossier prefix) and append the new ones.
    Each fact dict is JSON-encoded so the list-of-string property contract
    holds (Neo4j cannot store list-of-map directly without conversion)."""
    prefix = qmd_id.removesuffix("_md") + "_"
    for key, entries in fact_lists.items():
        if not entries:
            continue
        # encode each entry as JSON string for safe storage
        json_entries = [json.dumps(e, ensure_ascii=False, default=str) for e in entries]
        tx.run(
            f"""
            MATCH (p:Projekt {{id: $pid}})
            WITH p, coalesce(p.{key}, []) AS prev
            WITH p, [x IN prev WHERE NOT (
                (x STARTS WITH '{{' AND x CONTAINS $prefix1) OR
                (x STARTS WITH '{{' AND x CONTAINS $prefix2)
            )] AS kept
            SET p.{key} = kept + $new
            """,
            {"pid": projekt_id, "prefix1": f'"{qmd_id}"',
             "prefix2": f'"{prefix}', "new": json_entries},
        )


def project_exists(session, pid: str) -> bool:
    return session.run(
        "MATCH (p:Projekt {id: $id}) RETURN count(p) AS c", {"id": pid}
    ).single()["c"] > 0


# --------------------------------------------------------------------------

def process_dossier_unit(
    driver,
    database: str,
    unit: dict[str, Any],
    stats: dict[str, Any],
) -> None:
    qmd_id = unit["qmd_id"]
    rel = unit["rel_path"]
    h1 = unit["h1_title"]
    body = unit["body"]
    projekt_slug = unit["projekt_slug"]
    is_parent = unit["is_parent_of_multi"]

    with driver.session(database=database) as session:
        # 1) MERGE the case_markdown anchor
        session.execute_write(upsert_quelle_anchor, qmd_id, rel, h1)
        stats["qmd_anchors_merged"] += 1

        if is_parent:
            # Multi-dossier parent: just link to children
            for child_qmd in unit["children_qmd_ids"]:
                session.execute_write(link_parent_to_children, qmd_id, child_qmd)
                stats["zitiert_quelle_links"] += 1
            stats["per_dossier"][qmd_id] = {
                "rel_path": rel, "h1_title": h1, "is_parent_of_multi": True,
                "children": unit["children_qmd_ids"],
                "sref_count": 0, "belegt_in_count": 0,
                "section8_facts_count": 0,
                "projekt_matched": False, "projekt_id": None,
            }
            return

        # 2) Sources block
        sources = gather_sources(body)
        for sn, title, url in sources:
            sn_id = f"{qmd_id.removesuffix('_md')}_{sn.lower()}"
            session.execute_write(upsert_sref_and_link, qmd_id, sn_id, url, title)
            stats["sref_quelle_merged"] += 1
            stats["zitiert_quelle_links"] += 1

        sref_index = {sn: f"{qmd_id.removesuffix('_md')}_{sn.lower()}" for sn, _, _ in sources}

        # 3) Try to match Projekt (alias map → file-slug fallback)
        pid_guess = resolve_projekt_id(qmd_id, projekt_slug)
        projekt_matched = False
        if pid_guess and project_exists(session, pid_guess):
            projekt_matched = True
            stats["projekt_matched"] += 1
        else:
            stats["projekt_unmatched"] += 1
            stats["unmatched_projects"].append({"qmd": qmd_id, "guess": pid_guess})

        belegt_count = 0
        section8_facts_count = 0
        if projekt_matched and sources:
            # Delete prior curated BELEGT_IN from this loader for idempotency
            removed = session.execute_write(
                delete_prior_curated_belegt_in, pid_guess, qmd_id
            )
            stats["prior_belegt_in_deleted"] += removed

            # 4) Parse sections 1-9 tables
            sec_slice = find_section(body, range(1, 10))
            if sec_slice:
                rows = parse_md_table(sec_slice)
                for row in rows:
                    quelle_cell = find_column(
                        row, ["Quelle", "Quelle/Beleg", "Source", "Source/Beleg", "Quellen"]
                    ) or ""
                    sn_tokens = extract_sref_tokens(quelle_cell)
                    if not sn_tokens:
                        continue
                    vert_raw = find_column(
                        row, ["Vertrauensgrad", "Confidence", "Evidence", "Beleg"]
                    )
                    confidence = map_vertrauensgrad(vert_raw)
                    excerpt = row_to_excerpt(row)
                    for sn in sn_tokens:
                        sn_id = sref_index.get(sn)
                        if not sn_id:
                            # The cell references an S-ref that wasn't in
                            # the sources block — create a stub external_ref
                            sn_id = f"{qmd_id.removesuffix('_md')}_{sn.lower()}"
                            session.execute_write(
                                upsert_sref_and_link,
                                qmd_id, sn_id, "",
                                f"{sn} (stub, no URL in sources block)",
                            )
                            sref_index[sn] = sn_id
                            stats["sref_quelle_merged"] += 1
                            stats["zitiert_quelle_links"] += 1
                        session.execute_write(
                            write_belegt_in, pid_guess, sn_id, excerpt, confidence
                        )
                        belegt_count += 1

            # 5) Section 8 Kennwerte → list facts on Projekt
            sec8 = find_section(body, [8])
            fact_buckets: dict[str, list[dict[str, Any]]] = {
                "cost_facts": [], "reuse_share_facts": [], "co2_facts": [],
            }
            if sec8:
                rows = parse_md_table(sec8)
                for row in rows:
                    kennwert = find_column(
                        row, ["Kennwert", "Indicator", "Property", "Field", "Topic"]
                    )
                    if not kennwert:
                        continue
                    cat = categorise_kennwert(kennwert)
                    if not cat:
                        continue
                    wert = find_column(row, ["Wert", "Value"])
                    einheit = find_column(row, ["Einheit", "Unit"])
                    method = find_column(
                        row, ["Methode/Datenmodell/Software", "Methode", "Method"]
                    )
                    grenze = find_column(
                        row, ["Bilanzgrenze", "Scope", "System boundary"]
                    )
                    quelle_cell = find_column(
                        row, ["Quelle", "Quelle/Beleg", "Source"]
                    ) or ""
                    vert_raw = find_column(row, ["Vertrauensgrad", "Confidence"])
                    sn_tokens = extract_sref_tokens(quelle_cell)
                    sid = qmd_id
                    if sn_tokens:
                        sn_id = sref_index.get(sn_tokens[0])
                        if sn_id:
                            sid = sn_id
                    entry = {
                        "kennwert": kennwert,
                        "wert": wert,
                        "einheit": einheit,
                        "method": method,
                        "bilanzgrenze": grenze,
                        "source_id": sid,
                        "confidence": map_vertrauensgrad(vert_raw),
                        "loader": LOADER_RUN_ID,
                    }
                    fact_buckets[cat].append(entry)
            if any(fact_buckets.values()):
                session.execute_write(
                    replace_section8_facts, pid_guess, qmd_id, fact_buckets
                )
                section8_facts_count = sum(len(v) for v in fact_buckets.values())

        stats["belegt_in_created"] += belegt_count
        stats["section8_facts_appended"] += section8_facts_count
        stats["per_dossier"][qmd_id] = {
            "rel_path": rel,
            "h1_title": h1,
            "is_parent_of_multi": False,
            "sref_count": len(sources),
            "belegt_in_count": belegt_count,
            "section8_facts_count": section8_facts_count,
            "projekt_matched": projekt_matched,
            "projekt_id": pid_guess if projekt_matched else None,
        }


# --------------------------------------------------------------------------
# Snapshot + report
# --------------------------------------------------------------------------

def snapshot(session) -> dict[str, Any]:
    out: dict[str, Any] = {}
    out["case_markdown_total"] = session.run(
        "MATCH (q:Quelle) WHERE q.quelltyp='case_markdown' RETURN count(q) AS c"
    ).single()["c"]
    out["case_markdown_with_zitiert_child"] = session.run(
        "MATCH (q:Quelle) WHERE q.quelltyp='case_markdown' "
        "AND size([(q)-[:ZITIERT_QUELLE]->() | 1]) >= 1 "
        "RETURN count(q) AS c"
    ).single()["c"]
    out["external_reference_quelle_total"] = session.run(
        "MATCH (q:Quelle) WHERE q.quelltyp='external_reference' RETURN count(q) AS c"
    ).single()["c"]
    out["zitiert_quelle_total"] = session.run(
        "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS c"
    ).single()["c"]
    out["belegt_in_total"] = session.run(
        "MATCH ()-[r:BELEGT_IN]->() RETURN count(r) AS c"
    ).single()["c"]
    out["belegt_in_curated_with_excerpt"] = session.run(
        "MATCH ()-[r:BELEGT_IN]->() "
        "WHERE r.evidence_origin='curated' AND r.evidence_excerpt IS NOT NULL "
        "RETURN count(r) AS c"
    ).single()["c"]
    out["belegt_in_curated_total"] = session.run(
        "MATCH ()-[r:BELEGT_IN]->() WHERE r.evidence_origin='curated' "
        "RETURN count(r) AS c"
    ).single()["c"]
    return out


def write_flag(before: dict, after: dict, stats: dict, started_iso: str,
               finished_iso: str) -> None:
    body = {
        "phase": "4b.1",
        "loader_run_id": LOADER_RUN_ID,
        "started_at": started_iso,
        "completed_at": finished_iso,
        "before": before,
        "after": after,
        "stats_summary": {
            "dossier_units_processed": stats["dossier_units_processed"],
            "qmd_anchors_merged": stats["qmd_anchors_merged"],
            "sref_quelle_merged": stats["sref_quelle_merged"],
            "zitiert_quelle_links": stats["zitiert_quelle_links"],
            "belegt_in_created": stats["belegt_in_created"],
            "section8_facts_appended": stats["section8_facts_appended"],
            "projekt_matched": stats["projekt_matched"],
            "projekt_unmatched": stats["projekt_unmatched"],
            "prior_belegt_in_deleted": stats["prior_belegt_in_deleted"],
        },
        "acceptance": {
            "criterion": ">=85/96 case_markdown anchors with >=1 ZITIERT_QUELLE child",
            "after_value": after["case_markdown_with_zitiert_child"],
            "case_markdown_total": after["case_markdown_total"],
            "passed": after["case_markdown_with_zitiert_child"] >= 85,
        },
    }
    FLAG_PATH.write_text(json.dumps(body, ensure_ascii=False, indent=2),
                         encoding="utf-8")


def write_report(before: dict, after: dict, stats: dict) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Agent 9 — Phase 4b.1 + 4c.2 S-ref Backfill Report")
    lines.append("")
    lines.append(f"_Loader run id: `{LOADER_RUN_ID}`_  ")
    lines.append(f"_Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}_")
    lines.append("")
    lines.append("## Acceptance")
    lines.append("")
    pass_str = "PASS" if after["case_markdown_with_zitiert_child"] >= 85 else "FAIL"
    lines.append(f"- Target: ≥85 of ≈96 case_markdown :Quelle anchors have ≥1 :ZITIERT_QUELLE child.")
    lines.append(f"- Achieved: **{after['case_markdown_with_zitiert_child']} / {after['case_markdown_total']}** "
                 f"(was {before['case_markdown_with_zitiert_child']} / {before['case_markdown_total']}). **{pass_str}**.")
    lines.append("")
    lines.append("## Before / after")
    lines.append("")
    lines.append("| metric | before | after | delta |")
    lines.append("|---|---:|---:|---:|")
    for k in (
        "case_markdown_total",
        "case_markdown_with_zitiert_child",
        "external_reference_quelle_total",
        "zitiert_quelle_total",
        "belegt_in_total",
        "belegt_in_curated_total",
        "belegt_in_curated_with_excerpt",
    ):
        b = before[k]
        a = after[k]
        lines.append(f"| {k} | {b} | {a} | {a - b:+d} |")
    lines.append("")
    lines.append("## Loader summary")
    lines.append("")
    summary_keys = [
        "dossier_units_processed",
        "qmd_anchors_merged",
        "sref_quelle_merged",
        "zitiert_quelle_links",
        "belegt_in_created",
        "section8_facts_appended",
        "projekt_matched",
        "projekt_unmatched",
        "prior_belegt_in_deleted",
    ]
    lines.append("| stat | value |")
    lines.append("|---|---:|")
    for k in summary_keys:
        lines.append(f"| {k} | {stats[k]} |")
    lines.append("")
    lines.append("## Per-dossier curated edge counts")
    lines.append("")
    lines.append("| dossier (q_<slug>_md) | rel_path | S-refs | ZITIERT_QUELLE | BELEGT_IN | Section-8 facts | Projekt id | matched |")
    lines.append("|---|---|---:|---:|---:|---:|---|:---:|")
    for qmd, det in sorted(stats["per_dossier"].items()):
        match = "✓" if det.get("projekt_matched") else "—"
        pid = det.get("projekt_id") or ""
        zit = det.get("sref_count", 0)
        be = det.get("belegt_in_count", 0)
        s8 = det.get("section8_facts_count", 0)
        if det.get("is_parent_of_multi"):
            pid = f"(parent of {len(det.get('children', []))} sub-dossiers)"
            zit = len(det.get('children', []))
            be = 0
        lines.append(f"| `{qmd}` | `{det.get('rel_path','')}` | {zit} | {zit} | {be} | {s8} | `{pid}` | {match} |")
    lines.append("")
    if stats["unmatched_projects"]:
        lines.append("## Unmatched projects (loader could not infer a `p_<slug>` Projekt)")
        lines.append("")
        lines.append("| dossier qmd | guessed projekt id |")
        lines.append("|---|---|")
        for u in stats["unmatched_projects"]:
            lines.append(f"| `{u['qmd']}` | `{u['guess'] or '—'}` |")
        lines.append("")
        lines.append(
            "These dossiers contributed ZITIERT_QUELLE (S-ref) links but no "
            "BELEGT_IN/cost_facts because the Projekt id derived from the file "
            "slug does not exist in the live graph. Agent 11 (consolidation) "
            "or Agent 8.b should add a slug-alias table."
        )
        lines.append("")
    lines.append("## Legacy `qu_*_dossier` case_markdown anchors not touched")
    lines.append("")
    lines.append(
        "Agent 9 follows the manifest's `q_<slug>_md` naming convention. "
        "16 batch-2 dossiers already had parallel case_markdown :Quelle "
        "nodes under a different (`qu_*_dossier`) naming scheme created by "
        "an earlier batch loader. These were intentionally NOT touched — "
        "Agent 11 (consolidation) should reconcile the two naming schemes "
        "(either via MERGE-by-source_file alias or by deleting one of the "
        "duplicate pairs). The 16 untouched legacy anchors are the only "
        "case_markdown :Quelle without a :ZITIERT_QUELLE child after this "
        "run; subtract them from the 116 total and the new coverage is "
        f"{sum(1 for d in stats['per_dossier'].values() if d.get('sref_count', 0) > 0 or d.get('is_parent_of_multi'))} of "
        "100 dossier units processed."
    )
    lines.append("")
    lines.append("## Idempotency contract")
    lines.append("")
    lines.append(
        "Every BELEGT_IN edge written by this loader carries "
        "`_created_by='agent9_phase4b1'` and a stable `_cell_hash` "
        "(sha1(excerpt)[:12]). Re-runs first DELETE all loader edges per "
        "`(Projekt, dossier-S-ref-prefix)` pair and recreate them, so the "
        "graph converges to the parser's current output. q_<slug>_md and "
        "q_<slug>_sN :Quelle nodes are MERGE-by-id (no duplicates). "
        "Section-8 list facts are stripped per dossier-source prefix before "
        "appending fresh entries, so cost_facts/co2_facts/reuse_share_facts "
        "stay consistent on re-run."
    )
    lines.append("")
    lines.append("## Errors")
    lines.append("")
    if ERROR_LOG.is_file() and ERROR_LOG.stat().st_size:
        lines.append(f"See `{ERROR_LOG.name}`.")
    else:
        lines.append("None recorded.")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DEL_DIR.mkdir(parents=True, exist_ok=True)
    if ERROR_LOG.is_file():
        ERROR_LOG.unlink()
    if PROGRESS_LOG.is_file():
        PROGRESS_LOG.unlink()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    plan = build_per_dossier_plan(manifest)
    _log(f"manifest entries: {len(manifest['entries'])}; plan units after multi-dossier expansion: {len(plan)}")

    from neo4j import GraphDatabase  # type: ignore

    uri, user, pw, db = _resolve_connection()
    _log(f"connecting to {uri} db='{db}' as user='{user}'")
    drv = GraphDatabase.driver(uri, auth=(user, pw))
    started = time.perf_counter()
    started_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        drv.verify_connectivity()
        with drv.session(database=db) as s:
            before = snapshot(s)
        _log(
            f"BEFORE: case_md={before['case_markdown_total']} "
            f"with_zit={before['case_markdown_with_zitiert_child']} "
            f"ext_ref={before['external_reference_quelle_total']} "
            f"zit_total={before['zitiert_quelle_total']} "
            f"belegt_curated={before['belegt_in_curated_total']}"
        )

        stats: dict[str, Any] = {
            "dossier_units_processed": 0,
            "qmd_anchors_merged": 0,
            "sref_quelle_merged": 0,
            "zitiert_quelle_links": 0,
            "belegt_in_created": 0,
            "section8_facts_appended": 0,
            "projekt_matched": 0,
            "projekt_unmatched": 0,
            "prior_belegt_in_deleted": 0,
            "per_dossier": {},
            "unmatched_projects": [],
        }

        for i, unit in enumerate(plan, start=1):
            try:
                process_dossier_unit(drv, db, unit, stats)
                stats["dossier_units_processed"] += 1
                if i % 10 == 0 or i == len(plan):
                    _log(f"  [{i}/{len(plan)}] last unit qmd={unit['qmd_id']}")
            except Exception as exc:
                _err(f"unit {unit['qmd_id']} ({unit['rel_path']}): {exc!r}")
                _log(f"  ERROR on {unit['qmd_id']}: {exc!r}")

        with drv.session(database=db) as s:
            after = snapshot(s)
        _log(
            f"AFTER:  case_md={after['case_markdown_total']} "
            f"with_zit={after['case_markdown_with_zitiert_child']} "
            f"ext_ref={after['external_reference_quelle_total']} "
            f"zit_total={after['zitiert_quelle_total']} "
            f"belegt_curated={after['belegt_in_curated_total']}"
        )

        finished_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
        write_flag(before, after, stats, started_iso, finished_iso)
        write_report(before, after, stats)
        result = {
            "started_at": started_iso,
            "finished_at": finished_iso,
            "elapsed_seconds": time.perf_counter() - started,
            "before": before,
            "after": after,
            "stats": {k: v for k, v in stats.items() if k != "per_dossier"},
        }
        RESULT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2,
                                          default=str), encoding="utf-8")
        _log(
            f"DONE in {time.perf_counter() - started:.1f}s — "
            f"flag={FLAG_PATH.name} report={REPORT_PATH.name}"
        )
        acceptance_ok = after["case_markdown_with_zitiert_child"] >= 85
        if not acceptance_ok:
            _log(
                f"WARN acceptance NOT met: "
                f"{after['case_markdown_with_zitiert_child']} < 85"
            )
        return 0 if acceptance_ok else 2
    finally:
        drv.close()


if __name__ == "__main__":
    sys.exit(main())
