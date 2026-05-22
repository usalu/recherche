"""
Phase 5 — generate evidence MERGE Cypher from normalized batch markdowns.

Reads the normalized batches in
  _neo4j/intake/inbox/research/new taxonomy edit/_normalized/
parses every importable row, groups by relationship type, and emits a single
Cypher file with UNWIND blocks — one block per (relationship type) so the
output is readable and re-runnable.

Output:
  _neo4j/review/2026-06-03_taxonomy_integration_plan/phase5_evidence.cypher

Schema (one row per edge):
  edge_id            v10X-NNN[-NN[a]]            (batch id)
  project_id         p_*                          (anchor source for HAT_BAUTEILGRUPPE rows)
  source_node_id     bg_*|p_*                     (source of evidence edge)
  source_label       Bauteilgruppe|Projekt
  rel                HAT_BAUTEILGRUPPE | HAT_ERGEBNIS | HAT_RESSOURCENQUELLE |
                     HAT_WIEDERVERWENDUNGSORT | HAT_METHODE | HAT_AUFBEREITUNG |
                     HAT_RUECKBAUVERFAHREN | ANGEWENDET_AUF
  target_node_id     new canonical id (post-normalization)
  target_label       new canonical label
  evidence_url
  evidence_summary   (truncated to 240 chars per schema guide)
  confidence         HIGH|MEDIUM|LOW -> belegt|wahrscheinlich|unsicher

Read-only on the graph. Writes only one Cypher file.
"""

from __future__ import annotations
import json
import re
import sys
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(r"E:/recherche")
BATCH_DIR = ROOT / "_neo4j/intake/inbox/research/new taxonomy edit/_normalized"
PLAN_DIR = ROOT / "_neo4j/review/2026-06-03_taxonomy_integration_plan"
OUT_CYPHER = PLAN_DIR / "phase5_evidence.cypher"

RUN_TAG = "taxonomy_integration_2026_06_03"
EVIDENCE_BASIS = "taxonomy_integration_2026_06_03"

CONFIDENCE_MAP = {"HIGH": "belegt", "MEDIUM": "wahrscheinlich", "LOW": "unsicher"}

# Only these rels go in Phase 5. ANGEWENDET_AUF is :Methode -> :Bauteilgruppe.
ACCEPTED_RELS = {
    "HAT_BAUTEILGRUPPE", "HAT_ERGEBNIS", "HAT_RESSOURCENQUELLE",
    "HAT_WIEDERVERWENDUNGSORT", "HAT_METHODE", "HAT_AUFBEREITUNG",
    "HAT_RUECKBAUVERFAHREN", "ANGEWENDET_AUF",
}


def parse_batches() -> list[dict]:
    rows = []
    for md in sorted(BATCH_DIR.glob("reuse_taxonomy_v9_connection_expansion_batch_*.md")):
        text = md.read_text(encoding="utf-8", errors="ignore")
        col_idx = None
        for line in text.splitlines():
            if not line.lstrip().startswith("|"):
                col_idx = None
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
                continue
            if "project_id" in cells and ("edge_id" in cells or "id" in cells or "row_id" in cells):
                col_idx = {n: i for i, n in enumerate(cells)}
                for alias in ("edge_id", "id", "row_id"):
                    if alias in col_idx and "edge_id" not in col_idx:
                        col_idx["edge_id"] = col_idx[alias]
                if "edge_id" not in col_idx and "id" in col_idx:
                    col_idx["edge_id"] = col_idx["id"]
                continue
            if not col_idx:
                continue
            if len(cells) <= max(col_idx.values()):
                continue
            edge_id = cells[col_idx["edge_id"]]
            if not re.fullmatch(r"v10[A-Z0-9]*-\d+(?:-\w+)?", edge_id):
                continue

            def get(name: str) -> str:
                i = col_idx.get(name, -1)
                return cells[i] if 0 <= i < len(cells) else ""

            rel = get("relationship") or get("edge_type") or get("relation")
            if rel not in ACCEPTED_RELS:
                continue

            row = {
                "edge_id": edge_id,
                "batch": md.name,
                "project_id": get("project_id"),
                "source_node": get("source_node"),
                "source_label": get("source_label"),
                "rel": rel,
                "target_node": get("target_node"),
                "target_label": get("target_label") or get("target_type") or get("node_type"),
                "bauteilgruppe": get("bauteilgruppe"),
                "evidence_url": get("evidence_url"),
                "evidence_summary": get("evidence_summary") or get("evidence") or get("detail"),
                "confidence": get("confidence"),
            }

            if not row["target_node"]:
                continue

            rows.append(row)
    return rows


def cypher_str(s: str) -> str:
    """Escape a string for inline Cypher."""
    if s is None:
        return "null"
    s = s.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{s}'"


# Six canonical method names -> meth_* id (for ANGEWENDET_AUF source resolution)
METHOD_NAME_TO_ID = {
    "Urban_Mining_und_Scouting":          "meth_urban_mining_und_scouting",
    "Bestands_und_ReUse_Assessment":      "meth_bestands_und_reuse_assessment",
    "Verfuegbarkeitsbasiertes_Design":    "meth_verfuegbarkeitsbasiertes_design",
    "Reversibles_Design":                 "meth_reversibles_design",
    "Zirkulaere_Beschaffung":             "meth_zirkulaere_beschaffung",
    "Dokumentation_und_Monitoring":       "meth_dokumentation_und_monitoring",
}

VALID_ID_PREFIXES = ("bg_", "p_", "meth_", "av_", "rq_", "rv_", "wver_", "wvo_")


def resolve_src_id(row: dict) -> str:
    """Map a row's source field to the actual graph node id.

    Across batches the `source_node` column may be:
      - an actual id (bg_*, p_*, meth_*, ...): use directly
      - a label literal ('Projekt' / 'Bauteilgruppe'): infer real source from
        project_id (for HAT_BAUTEILGRUPPE) or bauteilgruppe column (others)
      - a canonical method/vocab name (for ANGEWENDET_AUF rows): convert
    """
    rel = row["rel"]
    sn = (row.get("source_node") or "").strip()
    pid = (row.get("project_id") or "").strip()
    bg = (row.get("bauteilgruppe") or "").strip()

    # ANGEWENDET_AUF: source is a method (in source_node as canonical name)
    if rel == "ANGEWENDET_AUF":
        if sn in METHOD_NAME_TO_ID:
            return METHOD_NAME_TO_ID[sn]
        if sn.startswith("meth_"):
            return sn
        # Fallback: try lowercase prefix
        return "meth_" + sn.lower() if sn else ""

    # HAT_BAUTEILGRUPPE: source is always the project
    if rel == "HAT_BAUTEILGRUPPE":
        return pid

    # All other rels: source should be a BG (bg_*) or project (p_*)
    if sn.startswith(VALID_ID_PREFIXES):
        return sn
    # source_node is a label literal — derive from bauteilgruppe column or project_id
    if bg and bg.startswith(VALID_ID_PREFIXES):
        return bg
    return pid


def cypher_obj(row: dict) -> str:
    """Serialize a row dict as a Cypher map literal, only the fields we need."""
    items = []
    items.append(f"edge_id: {cypher_str(row['edge_id'])}")
    items.append(f"src_id: {cypher_str(resolve_src_id(row))}")
    items.append(f"tgt_id: {cypher_str(row['target_node'])}")
    items.append(f"conf: {cypher_str(CONFIDENCE_MAP.get(row['confidence'], 'unsicher'))}")
    if row["evidence_url"]:
        items.append(f"url: {cypher_str(row['evidence_url'])}")
    else:
        items.append("url: null")
    quote = (row["evidence_summary"] or "")[:240]
    items.append(f"quote: {cypher_str(quote)}")
    items.append(f"batch: {cypher_str(row['batch'])}")
    return "{" + ", ".join(items) + "}"


def emit_unwind_block(out: list, rel: str, rows: list[dict], header_comment: str) -> None:
    """Emit one UNWIND block for a given rel type, splitting into chunks to avoid huge literals."""
    chunk_size = 200
    out.append(f"\n\n// ---------- {header_comment} ({rel}: {len(rows)} rows) ----------\n")

    for i in range(0, len(rows), chunk_size):
        chunk = rows[i : i + chunk_size]
        out.append(f"\n// {rel} chunk {i//chunk_size + 1}/{(len(rows)+chunk_size-1)//chunk_size}")
        out.append("UNWIND [")
        for j, row in enumerate(chunk):
            sep = "," if j < len(chunk) - 1 else ""
            out.append(f"  {cypher_obj(row)}{sep}")
        out.append("] AS row")

        if rel == "HAT_BAUTEILGRUPPE":
            # MERGE the Bauteilgruppe (creates if new candidate), then link to Projekt
            out.append("MATCH (proj:Projekt {id: row.src_id})")
            out.append("MERGE (bg:Bauteilgruppe {id: row.tgt_id})")
            out.append("ON CREATE SET bg.name = row.tgt_id,")
            out.append(f"              bg.bg_kind = 'partial_batch',")
            out.append(f"              bg.review_run = '{RUN_TAG}',")
            out.append("              bg.created_at = datetime()")
            out.append("MERGE (proj)-[r:HAT_BAUTEILGRUPPE]->(bg)")
            out.append("ON CREATE SET r.id = row.edge_id,")
            out.append(f"              r.evidence_basis = '{EVIDENCE_BASIS}',")
            out.append("              r.evidence_confidence = row.conf,")
            out.append("              r.evidence_url = row.url,")
            out.append("              r.evidence_quote = row.quote,")
            out.append(f"              r.review_run = '{RUN_TAG}',")
            out.append("              r.batch_id = row.batch,")
            out.append("              r.created_at = datetime();")
        else:
            # Anchor source by id (label-agnostic per schema-guide convention)
            out.append("MATCH (src {id: row.src_id}), (tgt {id: row.tgt_id})")
            out.append(f"MERGE (src)-[r:{rel}]->(tgt)")
            out.append("ON CREATE SET r.id = row.edge_id,")
            out.append(f"              r.evidence_basis = '{EVIDENCE_BASIS}',")
            out.append("              r.evidence_confidence = row.conf,")
            out.append("              r.evidence_url = row.url,")
            out.append("              r.evidence_quote = row.quote,")
            out.append(f"              r.review_run = '{RUN_TAG}',")
            out.append("              r.batch_id = row.batch,")
            out.append("              r.created_at = datetime();")
        out.append("")


def main() -> int:
    rows = parse_batches()
    by_rel = defaultdict(list)
    for r in rows:
        by_rel[r["rel"]].append(r)

    print(f"Parsed {len(rows)} importable evidence rows.")
    for rel, lst in sorted(by_rel.items(), key=lambda kv: -len(kv[1])):
        print(f"  {rel:<28} {len(lst):>5}")

    out: list[str] = [
        "// =====================================================================",
        "// Phase 5 — evidence MERGE",
        "//",
        f"// Generated from normalized batches in {BATCH_DIR.relative_to(ROOT)}",
        f"// Total importable rows: {len(rows)}",
        f"// review_run: {RUN_TAG}",
        "//",
        "// Run order within this file:",
        "//   1. HAT_BAUTEILGRUPPE chunks first (so Bauteilgruppe nodes exist before",
        "//      other rels anchor to them)",
        "//   2. Then all other rel types in size order",
        "//",
        "// Idempotent — re-running this file is safe (every MERGE/ON CREATE).",
        "// Rollback: MATCH ()-[r {review_run: '" + RUN_TAG + "'}]-() DELETE r;",
        "//           plus the corresponding `new candidate` BG nodes:",
        "//           MATCH (bg:Bauteilgruppe {review_run: '" + RUN_TAG + "'})",
        "//             WHERE bg.bg_kind = 'partial_batch' AND NOT (bg)<-[:HAT_BAUTEILGRUPPE]-()",
        "//           DELETE bg;",
        "// =====================================================================",
    ]

    # HAT_BAUTEILGRUPPE first (creates BG nodes), then other rels
    rel_order = ["HAT_BAUTEILGRUPPE"] + sorted(
        [r for r in by_rel if r != "HAT_BAUTEILGRUPPE"],
        key=lambda r: -len(by_rel[r]),
    )

    for rel in rel_order:
        if rel not in by_rel:
            continue
        emit_unwind_block(out, rel, by_rel[rel], f"§{rel_order.index(rel)+1}. {rel}")

    OUT_CYPHER.write_text("\n".join(out), encoding="utf-8")
    print(f"\nWrote {OUT_CYPHER} ({OUT_CYPHER.stat().st_size//1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
