"""test_gebaeude_unfolder.py — concrete proof of the per-row unfolder.

Tests against 5 real gebäude dossiers. For each:
  1. Parse the `## Quellen und Links` section → build {S0: url, S1: url, …}.
  2. Walk every table (§2 ENTITÄTEN-MAPPING, §5 BAUTEIL-INVENTAR,
     §6 PROZESS, §7 TECHNIK, §8 KENNWERTE, §9 HÜRDEN, §10 WIRTSCHAFT).
  3. For each row, extract:
       - the entity (column 1 or 2 depending on section)
       - the S-refs (in the "Quelle" / "Quelle/Beleg" column)
  4. For each (entity, S-ref), emit a TRIPLE: (entity, dossier_id, url, locator).
  5. Report: total triples, per-section counts, per-entity-type counts, sample.

Read-only. Does not touch graph.

Run:  python test_gebaeude_unfolder.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[6]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

GEBAEUDE_DIR = REPO_ROOT / "_archive" / "research" / "gebaeude"
TEST_DOSSIERS = [
    "Holbein_Gardens_London.md",
    "K118_Kopfbau_Halle_118_Winterthur.md",
    "Resource_Rows_Copenhagen.md",
    "Villa_Welpeloo_Enschede.md",
    "Ferme_du_Rail_Paris.md",
]


# --------------------------------------------------------------------------- #
# Parsers
# --------------------------------------------------------------------------- #

H2_RE = re.compile(r"^##+\s+(.+?)\s*$", re.MULTILINE)
# Accept both bracketed `[S1]` and bare `S1` (word-bounded) in table cells
SREF_RE = re.compile(r"\bS\d+\b")
URL_RE = re.compile(r"https?://[^\s<>\"'\)\]]+")
QUELLEN_LINE_RE = re.compile(r"^\s*-\s+\[?(S\d+)\]?\s+(.+?)(?:\s+(https?://\S+))?\s*$",
                              re.MULTILINE)


def split_sections(text: str) -> dict[str, str]:
    """Return ordered dict of {section_title: content}."""
    headers = [(m.start(), m.group(1).strip()) for m in H2_RE.finditer(text)]
    out: dict[str, str] = {}
    for i, (pos, title) in enumerate(headers):
        body_start = text.find("\n", pos) + 1
        body_end = headers[i + 1][0] if i + 1 < len(headers) else len(text)
        out[title] = text[body_start:body_end].strip()
    return out


SREF_LINE_RE = re.compile(r"\bS\d+\b")
URL_BACKTICKED_RE = re.compile(r"`(https?://[^`\s]+)`")
# A line in a Quellen list — bullet, numbered, or bare. We require a URL.
QUELLEN_NAMED_LINE_RE = re.compile(
    r"^\s*(?:[-*+]|\d+\.)\s+(.+?)(?:\s*[—–-]\s*|\s*:\s*)(.*?https?://\S+.*)$"
)


def _norm_token(s: str) -> str:
    """Normalise a citation token for fuzzy matching:
    lowercase, strip punctuation/whitespace, collapse spaces."""
    s = s.lower()
    s = re.sub(r"[^\w\s/&]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_quellen_table(section_text: str) -> dict[str, dict]:
    """Parse `## Quellen und Links` section. Handles 2 main citation styles:

    STYLE 1 — S-ref labelled list (Holbein, K118, etc.):
        - [S1] Title. https://...
        [S1] Title: https://...
        - **S1 — Title:** https://...
        - **S1 – Title.** `https://...`
        Output keys: 'S0', 'S1', ...

    STYLE 2 — Named-token list (55_Great_Suffolk, CRCLR, Recyclinghaus, ...):
        1. ASBP — 55 Great Suffolk Street: https://asbp.org.uk/...
        - CITYFÖRSTER – Recyclinghaus: https://www.cityfoerster.net/...
        Output keys: 'ASBP', 'CITYFÖRSTER', ... AND normalised aliases.

    Strategy:
      1. First pass — Style 1: find S-ref + URL on the line.
      2. Second pass for any line WITHOUT an S-ref but WITH a URL — Style 2:
         extract the head token (text before the em-dash/colon/dot) and map it.
    """
    out: dict[str, dict] = {}
    style2_entries: list[dict] = []  # for alias index

    for line in section_text.splitlines():
        line = line.strip()
        if not line:
            continue

        # --- STYLE 1 — S-ref labelled --------------------------------------
        sref_match = SREF_LINE_RE.search(line)
        if sref_match:
            sref = sref_match.group(0)
            bt = URL_BACKTICKED_RE.search(line)
            if bt:
                url = bt.group(1); url_pos = bt.start()
            else:
                um = URL_RE.search(line)
                url = um.group(0) if um else None
                url_pos = um.start() if um else None
            if url:
                url = url.rstrip(".,;:!?)`'\"")
            title = ""
            if url and url_pos is not None:
                between = line[sref_match.end():url_pos]
                title = re.sub(r"[\*\[\]:\-—–.`]+", " ", between).strip()
                title = re.sub(r"\s+", " ", title)[:200]
            if url:
                out[sref] = {"title": title, "url": url}
            continue

        # --- STYLE 2 — named-token list -------------------------------------
        um = URL_RE.search(line)
        if not um:
            continue
        url = um.group(0).rstrip(".,;:!?)`'\"")
        url_pos = um.start()

        # Strip leading list marker
        body = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", line)
        # Strip bold markers, then split head from URL portion
        head = body[: body.find(url) if url in body else url_pos]
        head = head.replace("**", "")
        # Cut head at first em-dash / en-dash / colon / pipe — keeps the org token
        sep_match = re.search(r"\s*[—–:|]\s*", head)
        token_str = head[: sep_match.start()] if sep_match else head
        token_str = token_str.strip(" \t.,;-—–")
        # Skip junk like a bare numeric (e.g. "1.") or empty
        if not token_str or len(token_str) > 80:
            continue
        if re.fullmatch(r"\d+\.?", token_str):
            continue
        title_str = head.strip(" \t.,;-—–:|").strip()
        title_str = re.sub(r"\s+", " ", title_str)[:200]

        entry = {"title": title_str, "url": url, "token": token_str}
        style2_entries.append(entry)
        # Primary key: the exact head token
        out[token_str] = {"title": title_str, "url": url}
        # Normalised alias key for fuzzy matching in tables
        norm = _norm_token(token_str)
        if norm and norm not in out:
            out[norm] = {"title": title_str, "url": url}
        # Also store first-word alias (e.g. "ASBP", "CITYFÖRSTER", "CMS")
        first = re.split(r"[\s/]", token_str, 1)[0].strip(".,;-")
        if first and first != token_str and first not in out:
            out[first] = {"title": title_str, "url": url}
        nf = _norm_token(first)
        if nf and nf not in out:
            out[nf] = {"title": title_str, "url": url}

    return out


def parse_markdown_table(content: str) -> tuple[list[str], list[list[str]]]:
    """Parse a Markdown table from a string. Returns (headers, rows)."""
    lines = [ln for ln in content.split("\n")
             if ln.strip().startswith("|") and ln.strip().endswith("|")]
    if len(lines) < 2:
        return ([], [])
    headers = [c.strip() for c in lines[0].strip("|").split("|")]
    rows: list[list[str]] = []
    for ln in lines[2:]:  # skip separator
        cells = [c.strip() for c in ln.strip("|").split("|")]
        rows.append(cells)
    return headers, rows


def find_quelle_column_idx(headers: list[str]) -> int | None:
    """Find the column containing source references. Common names:
    'Quelle', 'Quelle/Beleg', 'Quellen', 'Source'."""
    for i, h in enumerate(headers):
        if re.search(r"quelle", h, re.IGNORECASE):
            return i
        if re.search(r"^source", h, re.IGNORECASE):
            return i
    return None


def find_entity_columns(section_title: str, headers: list[str]) -> tuple[int | None, str]:
    """Return (column_index, semantic_kind) for the entity-identifying column(s).
    Different sections have different "main" columns:
      §2 ENTITÄTEN-MAPPING:  col 0 = entity type, col 1 = value     → use col 1
      §5 BAUTEIL-INVENTAR:   col 0 = Bauteil                         → use col 0
      §6 PROZESS:            col 0 = Prozessphase                    → use col 0
      §7 TECHNIK:            col 0 = Thema                           → use col 0
      §8 KENNWERTE:          col 0 = Kennwert                        → use col 0
      §9 HÜRDEN:             col 0 = Hürde                           → use col 0
      §10 WIRTSCHAFT:        col 0 = Aspekt                          → use col 0
    """
    section_lower = section_title.lower()
    if "entit" in section_lower:
        return (1, "entity_value")    # column 1 is the value
    if "bauteil" in section_lower and "inventar" in section_lower:
        return (0, "bauteil")
    if "prozess" in section_lower:
        return (0, "prozessphase")
    if "technik" in section_lower:
        return (0, "thema")
    if "kennwert" in section_lower:
        return (0, "kennwert")
    if "huerden" in section_lower or "hürden" in section_lower:
        return (0, "huerde")
    if "wirtschaft" in section_lower:
        return (0, "wirtschaft")
    # Default: first column
    return (0, "unknown")


# --------------------------------------------------------------------------- #
# Per-dossier unfolder
# --------------------------------------------------------------------------- #

def unfold_dossier(dossier_path: Path) -> dict:
    """Extract triples from one dossier. Returns a summary + sample triples."""
    text = dossier_path.read_text(encoding="utf-8")
    sections = split_sections(text)

    # Parse the Quellen master list
    quellen_section = next(
        (v for k, v in sections.items() if "quellen" in k.lower() and "link" in k.lower()),
        "",
    )
    s_ref_map = parse_quellen_table(quellen_section)

    # Walk tables in each table-bearing section
    table_sections = [
        "2. ENTITÄTEN-MAPPING",
        "5. BAUTEIL-INVENTAR",
        "6. PROZESS UND LOGISTIK",
        "7. TECHNIK, LEISTUNG, NORMEN",
        "8. KENNWERTE",
        "9. HÜRDEN-MATRIX",
        "10. WIRTSCHAFT UND BESCHAFFUNG",
    ]
    # Normalise section title lookup (the actual titles may have minor variants)
    section_lookup = {k.lower(): (k, v) for k, v in sections.items()}

    triples: list[dict] = []
    per_section: dict[str, int] = defaultdict(int)
    per_kind: dict[str, int] = defaultdict(int)
    per_entity_type: dict[str, int] = defaultdict(int)
    rows_with_no_quelle = 0
    rows_with_quelle_but_no_resolved_url = 0

    for needle in table_sections:
        # Find best matching section
        match = None
        for k, (orig, content) in section_lookup.items():
            if needle.lower() in k:
                match = (orig, content)
                break
        if not match:
            continue
        section_title, content = match

        headers, rows = parse_markdown_table(content)
        if not headers or not rows:
            continue
        quelle_idx = find_quelle_column_idx(headers)
        entity_idx, kind = find_entity_columns(section_title, headers)
        if quelle_idx is None or entity_idx is None:
            continue

        for row_idx, cells in enumerate(rows):
            if entity_idx >= len(cells) or quelle_idx >= len(cells):
                continue
            entity_value = cells[entity_idx].strip()
            quelle_cell = cells[quelle_idx]
            if not entity_value or entity_value in {"-", "—"}:
                continue

            resolved: list[tuple[str, dict]] = []   # (sref_or_token, info)

            # Strategy A — S-ref tokens (Style 1 dossiers)
            for sref in SREF_RE.findall(quelle_cell):
                info = s_ref_map.get(sref)
                if info and info.get("url"):
                    resolved.append((sref, info))

            # Strategy B — named tokens (Style 2 dossiers).
            # Only try this if no S-refs were resolved AND the cell looks like
            # a list of plain names (no S-ref pattern at all).
            if not resolved and not SREF_RE.search(quelle_cell):
                # Split on common separators
                raw_tokens = re.split(r"[,;/]| und |\|", quelle_cell)
                for raw_tok in raw_tokens:
                    tok = raw_tok.strip(" \t.-—–:")
                    if not tok or tok in {"-", "—", "unbekannt", "unklar"}:
                        continue
                    if len(tok) > 80:
                        continue
                    info = (
                        s_ref_map.get(tok)
                        or s_ref_map.get(_norm_token(tok))
                        or s_ref_map.get(tok.split()[0] if tok.split() else "")
                    )
                    # Last resort: substring match against any Style-2 token
                    if not info:
                        nt = _norm_token(tok)
                        for k, v in s_ref_map.items():
                            kk = _norm_token(k)
                            if kk and (kk == nt or kk.startswith(nt) or nt.startswith(kk)):
                                if len(nt) >= 3 and len(kk) >= 3:
                                    info = v
                                    break
                    if info and info.get("url"):
                        resolved.append((tok, info))

            if not resolved:
                if SREF_RE.search(quelle_cell):
                    rows_with_quelle_but_no_resolved_url += 1
                else:
                    rows_with_no_quelle += 1
                continue

            entity_type = (
                cells[0].strip()
                if "entit" in section_title.lower() and len(cells) > 0
                else kind
            )
            for sref_or_token, info in resolved:
                triple = {
                    "dossier_id": dossier_path.stem.lower(),
                    "section": section_title,
                    "row_idx": row_idx,
                    "kind": kind,
                    "entity_type": entity_type,
                    "entity_value": entity_value,
                    "sref": sref_or_token,
                    "url": info["url"],
                    "url_title": info["title"],
                }
                triples.append(triple)
                per_section[section_title] += 1
                per_kind[kind] += 1
                per_entity_type[entity_type] += 1

    return {
        "dossier_file": dossier_path.name,
        "sections_found": len(sections),
        "s_refs_in_quellen_list": len(s_ref_map),
        "urls_resolved": sum(1 for v in s_ref_map.values() if v["url"]),
        "total_triples_emitted": len(triples),
        "per_section": dict(per_section),
        "per_kind": dict(per_kind),
        "per_entity_type": dict(per_entity_type),
        "rows_with_quelle_but_no_resolved_url": rows_with_quelle_but_no_resolved_url,
        "rows_with_no_quelle": rows_with_no_quelle,
        "sample_triples": triples[:5],
        "triples": triples,
    }


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main():
    print("Testing gebäude unfolder on 5 sample dossiers...\n")

    all_results = []
    grand_total_triples = 0

    for name in TEST_DOSSIERS:
        p = GEBAEUDE_DIR / name
        if not p.exists():
            print(f"  SKIP missing: {p}")
            continue
        result = unfold_dossier(p)
        all_results.append(result)
        grand_total_triples += result["total_triples_emitted"]

        print(f"{'=' * 84}")
        print(f"  {result['dossier_file']}")
        print(f"{'=' * 84}")
        print(f"  Sections found:           {result['sections_found']}")
        print(f"  S-refs in 'Quellen' list: {result['s_refs_in_quellen_list']}")
        print(f"  URLs resolved:            {result['urls_resolved']}")
        print(f"  TOTAL TRIPLES EMITTED:    {result['total_triples_emitted']}")
        print(f"  Rows with no Quelle cell: {result['rows_with_no_quelle']}")
        print(f"  Rows with unresolved Quelle: {result['rows_with_quelle_but_no_resolved_url']}")
        print()
        print(f"  Per-section breakdown:")
        for sec, n in result["per_section"].items():
            print(f"    {sec:35}  {n:>4} triples")
        print()
        print(f"  Per-entity-type (top 10):")
        for et, n in sorted(result["per_entity_type"].items(),
                             key=lambda kv: -kv[1])[:10]:
            print(f"    {et:35}  {n:>4}")
        print()
        print(f"  Sample triples:")
        for t in result["sample_triples"]:
            print(f"    section='{t['section'][:30]}'  row={t['row_idx']}  "
                  f"kind={t['kind']}")
            print(f"      entity_type='{t['entity_type'][:30]}'  "
                  f"entity_value='{t['entity_value'][:40]}'")
            print(f"      sref={t['sref']}  url={t['url'][:80]}")
        print()

    print(f"{'=' * 84}")
    print(f"  GRAND TOTAL across {len(all_results)} dossiers: {grand_total_triples} triples")
    print(f"  Projected for all 76 gebäude dossiers: "
          f"~{int(grand_total_triples / max(len(all_results), 1) * 76)} triples")
    print(f"{'=' * 84}")

    # Persist
    out_path = THIS_FILE.parent / "test_gebaeude_unfolder_results.json"
    out_path.write_text(json.dumps(all_results, indent=2, default=str, ensure_ascii=False),
                         encoding="utf-8")
    print(f"\nDetailed results written to {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
