"""Agent 9 — local dry run of dossier parsing (no Neo4j).

Checks Source-block extraction, S-ref enumeration, section table parsing,
and Section-8 categorisation against representative dossiers BEFORE we
touch the live graph.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from agent9_dossier_loader import (  # type: ignore
    build_per_dossier_plan,
    categorise_kennwert,
    extract_sref_tokens,
    find_column,
    find_section,
    find_sources_block,
    gather_sources,
    map_vertrauensgrad,
    parse_md_table,
    projekt_id_from_dossier,
    row_to_excerpt,
    slugify,
    split_h1_blocks,
    REPORTS_DIR,
)


SAMPLES = [
    # gebaeude bullet style, rich Section 8 + sources
    "_archive/research/gebaeude/Resilience_La_Ferme_des_Possibles_Stains.md",
    # gebaeude numbered list, no [Sn] tokens — synthetic Sn from numbering
    "_archive/research/gebaeude/55_Great_Suffolk_Street_London.md",
    # gebaeude with quellen_und_links + many [Sn] inline
    "_archive/research/gebaeude/Holbein_Gardens_London.md",
    # batch2 with Source register table
    "_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/BE_NL_graph_ready_dossiers/Careno_Be_Circular_Brussels.md",
    "_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/BE_NL_graph_ready_dossiers/Circl_Pavilion_Amsterdam.md",
    # multi-dossier
    "_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/batch 1.md",
]


def main() -> int:
    manifest_path = REPORTS_DIR / "agent_8_dossier_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_rel = {e["rel_path"]: e for e in manifest["entries"]}
    plan = build_per_dossier_plan(manifest)
    plan_by_qmd: dict[str, dict] = {u["qmd_id"]: u for u in plan}

    print(f"manifest entries: {len(manifest['entries'])}")
    print(f"plan units (after multi-dossier expansion): {len(plan)}")
    print()

    for rel in SAMPLES:
        entry = by_rel[rel]
        print("=" * 78)
        print(f"FILE: {rel}")
        print(f"  expected_quelle_id: {entry['expected_quelle_id']}")
        print(f"  manifest sref_inline_count: {entry['sref_inline_count']}")
        text = Path(entry["abs_path"]).read_text(encoding="utf-8", errors="replace")
        h1_blocks = split_h1_blocks(text)
        print(f"  H1 blocks: {len(h1_blocks)}")
        for h1, body in h1_blocks:
            slug = slugify(h1)[:60]
            pid = projekt_id_from_dossier(slug) if slug else "—"
            sb = find_sources_block(body)
            srcs = gather_sources(body)
            sec_slice = find_section(body, range(1, 10))
            rows = parse_md_table(sec_slice) if sec_slice else []
            be_rows = 0
            sample_excerpt = None
            sample_sn = None
            sample_conf = None
            for r in rows:
                qcell = find_column(r, ["Quelle", "Quelle/Beleg", "Source"]) or ""
                toks = extract_sref_tokens(qcell)
                if toks:
                    be_rows += 1
                    if sample_excerpt is None:
                        sample_excerpt = row_to_excerpt(r)
                        sample_sn = toks
                        sample_conf = map_vertrauensgrad(
                            find_column(r, ["Vertrauensgrad", "Confidence"])
                        )
            sec8 = find_section(body, [8])
            kennwert_counts = {"cost": 0, "reuse_share": 0, "co2": 0, "other": 0}
            if sec8:
                for r in parse_md_table(sec8):
                    kw = find_column(r, ["Kennwert", "Property", "Field"])
                    if not kw:
                        continue
                    cat = categorise_kennwert(kw)
                    if cat == "cost_facts":
                        kennwert_counts["cost"] += 1
                    elif cat == "reuse_share_facts":
                        kennwert_counts["reuse_share"] += 1
                    elif cat == "co2_facts":
                        kennwert_counts["co2"] += 1
                    else:
                        kennwert_counts["other"] += 1
            print(f"  -- H1: {h1!r}")
            print(f"     slug={slug!r} pid_guess={pid!r}")
            print(f"     sources_block_offset={sb}  sources_found={len(srcs)}")
            print(f"     first 3 sources: {srcs[:3]}")
            print(f"     section 1-9 rows={len(rows)} with [Sn] tokens={be_rows}")
            if sample_excerpt:
                print(f"     sample_excerpt={sample_excerpt[:120]!r}")
                print(f"     sample_sref_tokens={sample_sn}  conf={sample_conf}")
            print(f"     section 8 Kennwerte buckets={kennwert_counts}")
        print()

    print("=" * 78)
    print("Plan units summary:")
    multi_parents = [u for u in plan if u["is_parent_of_multi"]]
    print(f"  multi-dossier parent units: {len(multi_parents)}")
    for u in multi_parents:
        print(f"    parent qmd={u['qmd_id']} children={u['children_qmd_ids']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
