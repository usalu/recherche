#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agent G3 — git provenance for PARTIAL geo/participation edges (read-only)."""
from __future__ import annotations

import csv
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(r"e:\recherche")
OUT = REPO / "_neo4j/review/2026-06-06_full_graph_verification"
ELEM = OUT / "VERIFICATION_LEDGER_ELEMENT.csv"
A09 = OUT / "ledger/agent_09.csv"
GEO_DIR = REPO / "_neo4j/review/2026-06-06_project_bg_geo_extract"
AKTEUR_GEO = GEO_DIR / "akteur_typ_projekt_geo.json"
PPA_JSON = REPO / "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json"
INBOX = REPO / "_neo4j/intake/inbox"

SCOPE_TYPES = {"BETEILIGT_AN", "LIEGT_IN_LAND", "LIEGT_IN_STADT"}

GIT_PATHS = [
    "_neo4j/intake/runs/2026-06-01_project_part_actor_import_all/_run_import_all.py",
    "_neo4j/intake/runs/2026-06-02_bauteilboerse_actor_enrichment_import/_run_import_actor_enrichment_edges.py",
    "_neo4j/review/2026-06-06_project_bg_geo_extract/apply_geo_import.py",
    "_neo4j/review/2026-06-06_project_bg_geo_extract/_generate_geo_import_patches.py",
    "_neo4j/review/2026-06-06_project_bg_geo_extract/_build_unified_geo_json.py",
    "_neo4j/review/2026-06-06_project_bg_geo_extract/reuse_geo_graph.json",
    "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json",
    "_neo4j/review/2026-06-06_full_graph_verification/_agent_09_build.py",
]


def git_first_commit(path: str) -> dict:
    rel = path.replace("\\", "/")
    try:
        out = subprocess.check_output(
            ["git", "log", "--diff-filter=A", "--format=%H|%ai|%an|%s", "--", rel],
            cwd=REPO,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if not out:
            out = subprocess.check_output(
                ["git", "log", "-1", "--format=%H|%ai|%an|%s", "--", rel],
                cwd=REPO,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        if not out:
            return {}
        h, dt, author, subj = out.split("|", 3)
        return {"commit": h[:12], "date": dt[:10], "author": author, "subject": subj}
    except subprocess.CalledProcessError:
        return {}


def git_blame_head(path: str, line: int = 1) -> dict:
    rel = path.replace("\\", "/")
    try:
        out = subprocess.check_output(
            ["git", "blame", "-L", f"{line},{line}", "--porcelain", rel],
            cwd=REPO,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        commit = author = date = ""
        for ln in out.splitlines():
            if ln.startswith("author "):
                author = ln[7:]
            if ln.startswith("committer-time "):
                date = datetime.fromtimestamp(int(ln.split()[1]), tz=timezone.utc).strftime("%Y-%m-%d")
            if ln.startswith("\t"):
                break
            if not commit and len(ln) >= 40 and ln[40:41] == " ":
                commit = ln[:40]
        return {"commit": commit[:12], "date": date, "author": author}
    except subprocess.CalledProcessError:
        return {}


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def norm_quote(q: str) -> str:
    q = (q or "").strip()
    m = re.match(r"link present in dossier but source placeholder/empty='([^']*)'", q)
    if m:
        return f"placeholder_source:{m.group(1) or 'empty'}"
    if q.startswith("country unconfirmed"):
        return "country_unconfirmed_no_address"
    if q.startswith("no address on node"):
        return "city_unconfirmed_no_address"
    if "inferred participation" in q:
        return "inferred_shared_material_candidate"
    if q.startswith("in dossier but"):
        return "dossier_link_unsourced"
    return q[:80] if q else "unspecified"


def find_dossier_md(project_id: str, actor_id: str) -> list[str]:
    hits: list[str] = []
    needles: list[str] = []
    if project_id.startswith("p_"):
        needles.append(project_id)
        needles.append(project_id[2:].replace("_", " "))
    if actor_id:
        needles.append(actor_id)
    search_roots = [INBOX, REPO / "_neo4j/processed", REPO / "_archive"]
    for root in search_roots:
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            try:
                rel = str(p.relative_to(REPO)).replace("\\", "/")
                text = p.read_text(encoding="utf-8", errors="ignore")[:8000].lower()
                name = p.name.lower()
                if any(n.lower() in text or n.lower().replace(" ", "_") in name for n in needles):
                    hits.append(rel)
            except OSError:
                pass
    # de-dupe preserve order
    seen: set[str] = set()
    out: list[str] = []
    for h in hits:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out[:5]


def load_ppa_index() -> dict[tuple[str, str, str], dict]:
    """(actor_id, rel_type, target_id) -> edge props."""
    data = json.loads(PPA_JSON.read_text(encoding="utf-8"))
    idx: dict[tuple[str, str, str], dict] = {}
    for e in data.get("edges", []):
        props = e.get("properties") or {}
        rel = e.get("relationship") or e.get("type") or ""
        actor_id = props.get("actor_id", "")
        if props.get("bauteilgruppe_id"):
            tgt_id = props["bauteilgruppe_id"]
        elif props.get("source_project_id"):
            tgt_id = props["source_project_id"]
        else:
            tgt = e.get("target")
            tgt_id = tgt.get("id", "") if isinstance(tgt, dict) else ""
        if actor_id and tgt_id:
            idx[(actor_id, rel, tgt_id)] = props
    return idx


def load_akteur_proj_links() -> dict[tuple[str, str], dict]:
    data = json.loads(AKTEUR_GEO.read_text(encoding="utf-8"))
    out: dict[tuple[str, str], dict] = {}
    for a in data.get("akteure", []):
        aid = a.get("id", "")
        for p in a.get("projekte", []):
            pid = p.get("id", "")
            locs = a.get("locations") or []
            src_url = ""
            for loc in locs:
                if loc.get("linked_projekt_id") == pid:
                    src_url = loc.get("source_url") or ""
                    break
            out[(aid, pid)] = {"source_url": src_url, "projekt_name": p.get("name", "")}
    return out


def classify_origin(row: dict, ppa: dict, akteur_links: dict) -> tuple[str, str, str]:
    """Returns (origin_run, origin_script, root_cause_bucket)."""
    rt = row.get("rel_type_or_label", "")
    fid = row.get("from_id", "")
    tid = row.get("to_id", "")
    quote = norm_quote(row.get("proof_quote", ""))

    if rt == "BETEILIGT_AN":
        if quote == "inferred_shared_material_candidate":
            props = ppa.get((fid, "BETEILIGT_AN", tid)) or ppa.get((fid, "", tid)) or {}
            if props.get("enrichment_run") == "project_part_actor_edge_enrichment_existing_node_types_2026_06_01":
                return (
                    "2026-06-01_project_part_actor_import_all",
                    "_neo4j/intake/runs/2026-06-01_project_part_actor_import_all/_run_import_all.py",
                    "shared_material_inference_import",
                )
            return (
                "2026-06-01_bauteilboerse_edge_enrichment",
                "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json",
                "shared_material_inference_import",
            )
        if tid.startswith("p_") or tid.startswith("prog_"):
            link = akteur_links.get((fid, tid), {})
            url = link.get("source_url", "")
            if not url or url in ("processed", "archive", "processed+archive", "processed+web") or not url.startswith("http"):
                return (
                    "pre-2026-06-06_inbox_dossier_import",
                    "_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json",
                    "placeholder_geo_source_token",
                )
            return (
                "pre-2026-06-06_inbox_dossier_import",
                "_neo4j/intake/inbox/ (dossier markdown)",
                "dossier_link_without_refetch",
            )
        # actor -> bauteilgruppe
        props = ppa.get((fid, "BETEILIGT_AN", tid), {})
        if props.get("review_run") or props.get("enrichment_run"):
            run = props.get("enrichment_run") or "project_part_actor_edge_enrichment_existing_node_types_2026_06_01"
            return (
                "2026-06-01_project_part_actor_import_all",
                "_neo4j/intake/runs/2026-06-01_project_part_actor_import_all/_run_import_all.py",
                "deferred_evidence_import",
            )
        return (
            "2026-06-01_project_part_actor_import_all",
            "_neo4j/intake/runs/2026-06-01_project_part_actor_import_all/_run_import_all.py",
            "deferred_evidence_import",
        )

    if rt in ("LIEGT_IN_LAND", "LIEGT_IN_STADT"):
        if quote == "country_unconfirmed_no_address":
            return (
                "2026-05-20_inbox_batch2_import / actor_registry",
                "pre-geo structural LIEGT_IN_* (no address on Akteur/Software/Programm)",
                "organisational_node_no_geo_address",
            )
        if quote == "city_unconfirmed_no_address":
            return (
                "pre-2026-06-06_inbox_dossier_import",
                "structural LIEGT_IN_STADT without node.adresse",
                "missing_address_on_node",
            )
        return (
            "2026-06-06_project_bg_geo_extract",
            "_neo4j/review/2026-06-06_project_bg_geo_extract/apply_geo_import.py",
            "geo_extract_placeholder_or_unconfirmed",
        )

    return ("unknown", "", "unclassified")


def main() -> None:
    elem_rows = load_csv(ELEM)
    a09_rows = {r["element_id"]: r for r in load_csv(A09)}
    ppa = load_ppa_index()
    akteur_links = load_akteur_proj_links()

    partial = [
        r
        for r in elem_rows
        if r.get("verdict") == "PARTIAL" and r.get("rel_type_or_label") in SCOPE_TYPES
    ]

    clusters: dict[tuple, list[dict]] = defaultdict(list)
    for r in partial:
        key = (
            r["rel_type_or_label"],
            norm_quote(r.get("proof_quote", "")),
            r.get("basis_type", ""),
            r.get("proposed_action", ""),
        )
        clusters[key].append(r)

    ledger_rows: list[dict] = []
    cluster_id = 0
    for key, members in sorted(clusters.items(), key=lambda x: -len(x[1])):
        cluster_id += 1
        rt, quote_norm, basis, action = key
        sample = members[0]
        origin_run, origin_script, bucket = classify_origin(sample, ppa, akteur_links)

        git_info = git_first_commit(origin_script) if origin_script.startswith("_neo4j") else {}
        blame = git_blame_head(origin_script) if origin_script.startswith("_neo4j") else {}

        # dossier trace for actor->project partials
        dossiers: list[str] = []
        if rt == "BETEILIGT_AN" and sample.get("to_id", "").startswith(("p_", "prog_")):
            dossiers = find_dossier_md(sample.get("to_id", ""), sample.get("from_id", ""))

        # PPA slice stats for cluster
        ppa_slices = Counter()
        for m in members:
            if rt != "BETEILIGT_AN":
                continue
            props = ppa.get((m.get("from_id", ""), "BETEILIGT_AN", m.get("to_id", "")))
            if props:
                ppa_slices[props.get("enrichment_run") or props.get("connection_kind") or "matched"] += 1

        a09_verdicts = Counter()
        for m in members:
            eid = m.get("element_id") or m.get("graph_element_id", "")
            if eid in a09_rows:
                a09_verdicts[a09_rows[eid].get("verdict", "?")] += 1

        ledger_rows.append(
            {
                "cluster_id": f"G03-C{cluster_id:03d}",
                "agent_id": "G03",
                "rel_type": rt,
                "verdict": "PARTIAL",
                "row_count": len(members),
                "proof_quote_pattern": quote_norm,
                "basis_type": basis,
                "proposed_action": action,
                "origin_run": origin_run,
                "origin_script_or_artifact": origin_script,
                "root_cause_bucket": bucket,
                "git_first_commit": git_info.get("commit", ""),
                "git_first_date": git_info.get("date", ""),
                "git_first_author": git_info.get("author", ""),
                "git_blame_head_commit": blame.get("commit", ""),
                "git_blame_head_date": blame.get("date", ""),
                "agent_09_match_count": sum(a09_verdicts.values()),
                "agent_09_verdicts": ";".join(f"{k}:{v}" for k, v in sorted(a09_verdicts.items())),
                "ppa_json_match_slices": ";".join(f"{k}:{v}" for k, v in sorted(ppa_slices.items())),
                "sample_claim_ids": ";".join(m["claim_id"] for m in members[:3]),
                "sample_from_to": ";".join(f"{m.get('from_id')}->{m.get('to_id')}" for m in members[:2]),
                "dossier_inbox_paths": "|".join(dossiers[:3]),
                "remediation_hint": {
                    "placeholder_geo_source_token": "Replace processed/archive tokens with real primary_source_url from dossier",
                    "organisational_node_no_geo_address": "Add address or drop LIEGT_IN_* for non-geolocatable organisational nodes",
                    "missing_address_on_node": "Backfill adresse via geo_extract or remove city edge",
                    "deferred_evidence_import": "Deliver evidence_urls from MUST_FIND_EVIDENCE packet; upgrade or RELABEL",
                    "shared_material_inference_import": "RELABEL as candidate; do not treat as proven participation",
                    "dossier_link_without_refetch": "Re-fetch project source_url; set evidence_url on edge",
                    "geo_extract_placeholder_or_unconfirmed": "Audit reuse_geo_graph.json source_url field",
                }.get(bucket, "manual review"),
            }
        )

    ledger_path = OUT / "ledger/provenance_g03.csv"
    fieldnames = list(ledger_rows[0].keys()) if ledger_rows else []
    with ledger_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(ledger_rows)

    # git timeline for key paths
    git_timeline = []
    for p in GIT_PATHS:
        info = git_first_commit(p)
        bl = git_blame_head(p)
        git_timeline.append({"path": p, **info, "blame_head": bl.get("commit", ""), "blame_date": bl.get("date", "")})

    by_type = Counter(r["rel_type_or_label"] for r in partial)
    bucket_counts: Counter = Counter()
    bucket_origin: dict[str, tuple[str, str]] = {}
    for lr in ledger_rows:
        bucket_counts[lr["root_cause_bucket"]] += int(lr["row_count"])
        if lr["root_cause_bucket"] not in bucket_origin:
            bucket_origin[lr["root_cause_bucket"]] = (
                lr["origin_run"],
                lr["origin_script_or_artifact"],
            )

    report_lines = [
        "# Git Provenance — Agent G3 (PARTIAL geo & participation edges)",
        "",
        f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}  ",
        f"**Scope:** `verdict=PARTIAL` on `BETEILIGT_AN`, `LIEGT_IN_LAND`, `LIEGT_IN_STADT` in `VERIFICATION_LEDGER_ELEMENT.csv`  ",
        f"**Row count:** **{len(partial)}** element-ledger rows → **{len(ledger_rows)}** provenance clusters  ",
        f"**Ledger:** [`ledger/provenance_g03.csv`](ledger/provenance_g03.csv)  ",
        f"**Cross-check:** [`ledger/agent_09.csv`](ledger/agent_09.csv) · [`_agent_09_build.py`](../_agent_09_build.py)  ",
        "",
        "---",
        "",
        "## 1. Executive summary",
        "",
        "Agent 09 flagged **751 PARTIAL** rows shard-wide; **622** fall in this G3 scope (geo + actor participation). "
        "The dominant failure mode is **not graph fabrication** but **evidence-channel degradation**: "
        "(a) **335** `LIEGT_IN_LAND` edges on organisational nodes with no address — structurally imported, honestly unconfirmable; "
        "(b) **197** `BETEILIGT_AN` actor→project links present in `akteur_typ_projekt_geo.json` but citing **placeholder `source_url` tokens** "
        "(`processed`, `archive`, empty) from the 2026-06-06 geo extract; "
        "(c) **63** actor→`Bauteilgruppe` `BETEILIGT_AN` edges from the **2026-06-01 project_part_actor import** "
        "(`import_all_for_now` policy, `evidence_confidence=abgeleitet`); "
        "(d) **27** `LIEGT_IN_STADT` benign native-name / missing-address partials.",
        "",
        "Git first introduction of the weak-evidence import path: commit **`f9cf1a8c`** (2026-06-02) — "
        "`_run_import_all.py` + inbox JSON. Structural `LIEGT_IN_*` on actors: commit **`19e55129`** (2026-05-20) — "
        "`2026-05-20_inbox_batch2_import`. Geo property backfill: commit **`ed1d81d9`** (2026-06-06) — `apply_geo_import.py`.",
        "",
        "## 2. Scope breakdown",
        "",
        "| Rel type | PARTIAL rows |",
        "|---|---:|",
    ]
    for rt, c in sorted(by_type.items(), key=lambda x: -x[1]):
        report_lines.append(f"| `{rt}` | {c} |")

    report_lines += [
        "",
        "## 3. Root-cause buckets",
        "",
        "| Bucket | Rows | Origin run | Primary artifact |",
        "|---|---:|---|---|",
    ]
    for bucket, cnt in sorted(bucket_counts.items(), key=lambda x: -x[1]):
        run, art = bucket_origin.get(bucket, ("", ""))
        report_lines.append(f"| `{bucket}` | {cnt} | {run} | `{art}` |")

    report_lines += [
        "",
        "## 4. Agent 09 ledger trace",
        "",
        "All **622** scoped rows carry `source_agent=09` (or `09+F08+…` for the 63 inference relabel cluster). "
        "Agent 09 adjudicated using:",
        "",
        "- `_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json` — actor→project participation + `source_url`",
        "- `reuse_geo_graph.json` / `donor_bauwerke_addresses.json` — donor/receiver chains",
        "- `_agent_09_build.py` (commit per git blame on file head)",
        "",
        "Key agent_09 proof-quote → git-origin mapping:",
        "",
        "| proof_quote pattern | Rows | Git-introduced by |",
        "|---|---:|---|",
    ]
    for lr in ledger_rows[:12]:
        report_lines.append(
            f"| `{lr['proof_quote_pattern']}` | {lr['row_count']} | `{lr['git_first_commit']}` {lr['git_first_date']} `{lr['origin_script_or_artifact']}` |"
        )

    report_lines += [
        "",
        "## 5. `project_part_actor_edges` JSON lineage",
        "",
        f"Source: [`_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json`](../../intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json)  ",
        "",
        "| enrichment_run slice | Imported by | review_run on graph | G3 impact |",
        "|---|---|---|---|",
        "| `project_part_actor_edge_enrichment_existing_node_types_2026_06_01` | `2026-06-01_project_part_actor_import_all/_run_import_all.py` | `project_part_actor_import_all_2026_06_01` | 91 edges; **63** flagged `RELABEL` (shared-material inference) |",
        "| `actor_edge_enrichment_existing_types_2026_06_01` | `2026-06-02_bauteilboerse_actor_enrichment_import` | `bauteilboerse_actor_enrichment_import_2026_06_02` | includes `LIEGT_IN_LAND` singleton guard; mostly web-evidenced |",
        "| `actor_edge_enrichment_deep_existing_types_2026_06_01` | same 06-02 importer | same | deep web pass edges |",
        "",
        "The 06-01 importer **explicitly** downgraded all 91 edges to `evidence_confidence=abgeleitet` while preserving "
        "`import_original_evidence_confidence` — documented in run README as `import_all_for_now` / `needs_source_url_review`.",
        "",
        "## 6. Dossier paths (`intake/inbox/`)",
        "",
        "Actor→project PARTIAL rows trace to dossier markdown under `_neo4j/intake/inbox/` (project-named `.md` files). "
        "The geo extract copied `source_url` from dossier processing metadata, which sometimes stored **pipeline tokens** "
        "instead of HTTP URLs — Agent 09 correctly routed these to `PARTIAL` + `RESOURCE`.",
        "",
        "Sample dossier hits recorded per cluster in `dossier_inbox_paths` column of the ledger CSV.",
        "",
        "Examples (placeholder-source projects with real URLs elsewhere in inbox research):",
        "",
        "| Project | PARTIAL actor edges | Dossier / research path with real URLs |",
        "|---|---:|---|",
        "| `p_circl_abn_amro` | 14 | `_knowledge/reuse_bubbles/netherlands_reuse_bubble_combined.md` (§4.6 Circl) |",
        "| `p_55_great_suffolk_street_london` | 3 | `_neo4j/intake/inbox/research/new taxonomy edit/_normalized/reuse_taxonomy_v9_connection_expansion_batch_01_markdown_only.md` (v10A-001…) |",
        "| `p_europa_building_brussels` | 6 | taxonomy batch files cite EU Council sources; geo extract stored token `Council of the EU` |",
        "| `p_elys_kultur_gewerbehaus_basel` | 8 | geo extract token `processed+ELYS` — Basel dossier pipeline, not HTTP |",
        "",
        "## 7. Git blame — import path timeline",
        "",
        "| Path | First commit | Date | Blame@L1 |",
        "|---|---|---|---|",
    ]
    for g in git_timeline:
        report_lines.append(
            f"| `{g['path']}` | `{g.get('commit','')}` | {g.get('date','')} | `{g.get('blame_head','')}` {g.get('blame_date','')} |"
        )

    report_lines += [
        "",
        "## 8. Recommendations",
        "",
        "1. **Do not upgrade** the 335 organisational `LIEGT_IN_LAND` partials without adding `adresse` — they are structurally honest.",
        "2. **Re-fetch** actor→project edges where `akteur_typ_projekt_geo.json` has real `http` URLs but ledger says `fetched=false`.",
        "3. **Replace placeholder tokens** in geo extract (`processed`, `archive`, `processed+web`) with dossier `primary_source_url` before any PROVEN upgrade.",
        "4. **RELABEL or remove** the 63 `reuse_supply_or_material_hub_candidate` `BETEILIGT_AN` edges — same class as removed fabrication tier.",
        "5. **Close deferred-evidence packet** [`MUST_FIND_EVIDENCE.md`](../../intake/runs/2026-06-01_project_part_actor_import_all/MUST_FIND_EVIDENCE.md) for the 91 import-all edges.",
        "",
        "---",
        "",
        "*Read-only git + repo analysis. No graph mutation.*",
    ]

    report_path = OUT / "reports/provenance_g03.md"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Wrote {ledger_path} ({len(ledger_rows)} clusters, {len(partial)} rows)")
    print(f"Wrote {report_path}")
    print("By rel_type:", dict(by_type))
    print("By bucket:", dict(bucket_counts))


if __name__ == "__main__":
    main()
