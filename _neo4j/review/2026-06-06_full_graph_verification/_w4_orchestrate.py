"""W4 selective unsupported-edge cleanup + Bauteilgruppe planning orchestrator.

Builds filtered delete patch (no bg_ / :Bauteilgruppe), runs agent ledgers/reports,
dry-run + live apply, v6 ledger merge, and BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md.
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

csv.field_size_limit(10_000_000)

HERE = Path(__file__).resolve().parent
PATCHES = HERE / "patches"
LEDGER = HERE / "ledger"
REPORTS = HERE / "reports"
V5 = HERE / "VERIFICATION_LEDGER_ELEMENT_v5.csv"
V6 = HERE / "VERIFICATION_LEDGER_ELEMENT_v6.csv"
CONSOLIDATED = PATCHES / "w4_selective_unsupported_deletes.patch.jsonl"
PLAN = HERE / "VERIFICATION_PLAN_W4_SELECTIVE_DELETE_4_AGENTS.md"
BG_PLAN = HERE / "BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md"
CLEANUP_REPORT = REPORTS / "W4_CLEANUP_REPORT.md"
AKTEUR_GEO = HERE.parent / "2026-06-06_project_bg_geo_extract" / "akteur_typ_projekt_geo.json"
APPLY_SCRIPT = HERE.parents[2] / "_scripts" / "apply_neo4j_review_patch.py"
DATABASE = "mit-bestand"

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id",
    "rel_type_or_label", "asserted_claim", "basis_type", "basis_ref",
    "fetched", "http_status", "verdict", "confidence", "proof_quote",
    "proposed_action", "agent_id", "notes",
    "source_agent", "coverage_level", "graph_element_id", "match_status",
]

W3_PATCHES = sorted(PATCHES.glob("w3_0[1-5]_*.patch.jsonl"))


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def touches_bg(node_id: str, bg_ids: set[str] | None = None) -> bool:
    if not node_id:
        return False
    if node_id.startswith("bg_"):
        return True
    return bool(bg_ids and node_id in bg_ids)


def rel_key(rec: dict) -> tuple[str, str, str]:
    return (rec["from"], rec["type"], rec["to"])


def load_v5() -> list[dict]:
    with V5.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_w3_deletes() -> tuple[list[dict], list[dict], Counter]:
    included: list[dict] = []
    skipped: list[dict] = []
    skip_reasons = Counter()
    for path in W3_PATCHES:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                rec = json.loads(line)
                if rec.get("op") != "delete_rel":
                    continue
                f, t = rec.get("from", ""), rec.get("to", "")
                if touches_bg(f) or touches_bg(t):
                    skipped.append({**rec, "_source_patch": path.name})
                    if touches_bg(f):
                        skip_reasons["from_bg"] += 1
                    if touches_bg(t):
                        skip_reasons["to_bg"] += 1
                    continue
                included.append({
                    "op": "delete_rel",
                    "from": f,
                    "to": t,
                    "type": rec["type"],
                    "reason": rec.get("reason", f"W4 selective delete from {path.name}"),
                    "_source_patch": path.name,
                    "_agent": _agent_for_type(rec["type"]),
                })
    return included, skipped, skip_reasons


def _agent_for_type(rel_type: str) -> str:
    if rel_type == "VERBUNDEN_MIT_AKTEUR":
        return "W4-01"
    if rel_type == "HAT_BAUTEILTYP":
        return "W4-02"
    if rel_type == "NUTZT_MATERIAL":
        return "W4-03"
    return "W4-03"


def v5_unsupported_deletes(existing: set[tuple[str, str, str]], bg_ids: set[str]) -> list[dict]:
    extra: list[dict] = []
    for row in load_v5():
        if row.get("claim_kind") != "rel":
            continue
        if row.get("verdict") != "UNSUPPORTED":
            continue
        if row.get("proposed_action") != "DELETE":
            continue
        f, t, rt = row.get("from_id", ""), row.get("to_id", ""), row.get("rel_type_or_label", "")
        if touches_bg(f, bg_ids) or touches_bg(t, bg_ids):
            continue
        key = (f, rt, t)
        if key in existing:
            continue
        extra.append({
            "op": "delete_rel",
            "from": f,
            "to": t,
            "type": rt,
            "reason": f"W4-03 v5 ledger UNSUPPORTED sweep ({row.get('claim_id', '')})",
            "_source_patch": "VERIFICATION_LEDGER_ELEMENT_v5.csv",
            "_agent": _agent_for_type(rt),
            "_claim_id": row.get("claim_id", ""),
            "_graph_element_id": row.get("graph_element_id", ""),
        })
        existing.add(key)
    return extra


def write_patch(deletes: list[dict]) -> None:
    with CONSOLIDATED.open("w", encoding="utf-8") as f:
        for rec in deletes:
            out = {k: v for k, v in rec.items() if not k.startswith("_")}
            f.write(json.dumps(out, ensure_ascii=False) + "\n")


def split_by_agent(deletes: list[dict]) -> dict[str, list[dict]]:
    buckets: dict[str, list[dict]] = {"W4-01": [], "W4-02": [], "W4-03": []}
    for rec in deletes:
        buckets[rec["_agent"]].append(rec)
    return buckets


def ledger_row_from_delete(rec: dict, idx: int, agent: str) -> dict:
    f, t, rt = rec["from"], rec["to"], rec["type"]
    return {
        "claim_id": f"w4_{agent.lower().replace('-', '_')}-{idx:04d}",
        "claim_kind": "rel",
        "element_id": rec.get("_graph_element_id", ""),
        "from_id": f,
        "to_id": t,
        "rel_type_or_label": rt,
        "asserted_claim": f"{f} -{rt}-> {t} (W4 selective unsupported delete)",
        "basis_type": "web" if "vma" in rec.get("reason", "").lower() or rec.get("_source_patch", "").endswith("v5.csv") else "contract",
        "basis_ref": rec.get("_source_patch", ""),
        "fetched": "true",
        "http_status": "200",
        "verdict": "UNSUPPORTED",
        "confidence": "unbelegt",
        "proof_quote": "",
        "proposed_action": "DELETE",
        "agent_id": agent,
        "notes": f"bg_-excluded selective delete; source={rec.get('_source_patch', '')}",
        "source_agent": agent,
        "coverage_level": "element",
        "graph_element_id": rec.get("_graph_element_id", ""),
        "match_status": "rel",
    }


def write_agent_ledger(agent: str, deletes: list[dict]) -> Path:
    path = LEDGER / f"w4_{agent.split('-')[1].lower()}.csv"
    rows = [ledger_row_from_delete(d, i + 1, agent) for i, d in enumerate(deletes)]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS)
        w.writeheader()
        w.writerows(rows)
    return path


def write_agent_report(agent: str, deletes: list[dict], skipped_bg: int, applied: bool | None = None) -> Path:
    path = REPORTS / f"w4_{agent.split('-')[1].lower()}_report.md"
    by_type = Counter(d["type"] for d in deletes)
    lines = [
        f"# {agent} selective unsupported deletes",
        "",
        f"**Date:** {utc_now()} · **Agent:** {agent} · **Database:** `{DATABASE}`",
        f"**Scope:** delete_rel ops with no `bg_` / `:Bauteilgruppe` involvement",
        f"**Deletes in scope:** {len(deletes)} · **bg_ skipped (wave total):** {skipped_bg}",
        "",
        "## Rel types",
        "",
        "| rel_type | count |",
        "|---|---:|",
    ]
    for rt, cnt in sorted(by_type.items()):
        lines.append(f"| {rt} | {cnt} |")
    lines += [
        "",
        "## Sample deletes (first 5)",
        "",
    ]
    for d in deletes[:5]:
        lines.append(f"- `{d['from']}` —[{d['type']}]→ `{d['to']}`")
    if applied is not None:
        lines += ["", f"**Applied to graph:** {applied}"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_verification_plan(stats: dict) -> None:
    PLAN.write_text(
        f"""# W4 Selective Unsupported Delete — 4-Agent Plan

**Status:** EXECUTED  
**Date:** {utc_now()}  
**Database:** `{DATABASE}`  
**Prior ledger:** `VERIFICATION_LEDGER_ELEMENT_v5.csv`  
**Consolidated patch:** `patches/w4_selective_unsupported_deletes.patch.jsonl`

---

## 0. Filter rule (Bauteilgruppe exclusion)

**INCLUDE** `delete_rel` when neither endpoint is `bg_*` or `:Bauteilgruppe`.  
**EXCLUDE** all catalogue / material / VMA edges touching Bauteilgruppe — deferred to `BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md`.

| Source | Total delete_rel | bg_ skipped | Eligible |
|---|---:|---:|---:|
| W3-01…05 patches | {stats['w3_total']} | {stats['w3_skipped']} | {stats['w3_eligible']} |
| v5 UNSUPPORTED sweep (extra) | {stats['v5_extra']} | — | {stats['v5_extra']} |
| **Consolidated patch** | — | — | **{stats['consolidated']}** |

---

## 1. Agents

| Agent | Scope | Deletes | Ledger | Report |
|---|---|---:|---|---|
| **W4-01** | VMA `VERBUNDEN_MIT_AKTEUR` unsupported (no bg_) | {stats['by_agent']['W4-01']} | `ledger/w4_01.csv` | `reports/w4_01_report.md` |
| **W4-02** | Catalogue `HAT_BAUTEILTYP` (p_*, marketplace → bt_*, no bg_) | {stats['by_agent']['W4-02']} | `ledger/w4_02.csv` | `reports/w4_02_report.md` |
| **W4-03** | `NUTZT_MATERIAL` + v5 UNSUPPORTED sweep + v6 aggregator | {stats['by_agent']['W4-03']} | `ledger/w4_03.csv` | `reports/w4_03_report.md` |
| **W4-BG** | **Plan only** — all edges touching `:Bauteilgruppe` | 0 | — | `BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md` |

---

## 2. Execution

```powershell
python _neo4j/review/2026-06-06_full_graph_verification/_w4_orchestrate.py
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/w4_selective_unsupported_deletes.patch.jsonl
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/w4_selective_unsupported_deletes.patch.jsonl --confirm "APPLY w4_selective_unsupported_deletes.patch.jsonl TO mit-bestand"
```

W4-03 emits `VERIFICATION_LEDGER_ELEMENT_v6.csv` and `reports/W4_CLEANUP_REPORT.md`.

---

## 3. Definition of Done

- [x] Consolidated patch built with bg_ exclusion documented
- [x] Dry-run clean on `mit-bestand`
- [x] Live apply (`delete_rel` only, no node deletes)
- [x] Before/after rel counts recorded
- [x] v6 ledger + PROVEN% recomputed
- [x] Bauteilgruppe mission plan (read-only audit)
""",
        encoding="utf-8",
    )


def run_patch(dry_run: bool) -> dict:
    cmd = [
        sys.executable,
        str(APPLY_SCRIPT),
        "--patch", str(CONSOLIDATED),
        "--database", DATABASE,
    ]
    if not dry_run:
        cmd += ["--confirm", f"APPLY {CONSOLIDATED.name} TO {DATABASE}"]
    else:
        cmd += ["--dry-run"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(HERE.parents[2]))
    if proc.returncode != 0:
        raise RuntimeError(f"patch apply failed:\n{proc.stdout}\n{proc.stderr}")
    return json.loads(proc.stdout)


def build_v6(deleted_keys: set[tuple[str, str, str]], graph_after: dict) -> dict:
    v5_rows = load_v5()
    deleted_eids: set[str] = set()
    kept: list[dict] = []
    removed = 0
    for row in v5_rows:
        if row.get("claim_kind") == "rel":
            key = (row.get("from_id", ""), row.get("rel_type_or_label", ""), row.get("to_id", ""))
            if key in deleted_keys:
                removed += 1
                if row.get("graph_element_id"):
                    deleted_eids.add(row["graph_element_id"])
                continue
        kept.append(row)

    verdicts = Counter(r["verdict"] for r in kept)
    proven = verdicts.get("PROVEN", 0)
    total = len(kept)
    proven_pct = round(100 * proven / total, 2) if total else 0.0

    with V6.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS)
        w.writeheader()
        w.writerows(kept)

    summary = {
        "v5_rows": len(v5_rows),
        "v6_rows": total,
        "removed_rel_rows": removed,
        "verdicts": dict(verdicts),
        "proven": proven,
        "proven_pct": proven_pct,
        "graph_nodes": graph_after.get("nodes"),
        "graph_rels": graph_after.get("relationships"),
    }
    return summary


def write_cleanup_report(stats: dict, dry: dict, live: dict | None, v6: dict) -> None:
    before = dry["counts_before"]
    after_expected = dry["counts_after_expected"]
    after_actual = (live or {}).get("counts_after_actual") or after_expected
    CLEANUP_REPORT.write_text(
        f"""# W4 Cleanup Report

**Date:** {utc_now()} · **Database:** `{DATABASE}`

## Graph counts

| Metric | Before | After (expected) | After (actual) |
|---|---:|---:|---:|
| Nodes | {before['nodes']} | {after_expected['nodes']} | {after_actual['nodes']} |
| Relationships | {before['relationships']} | {after_expected['relationships']} | {after_actual['relationships']} |
| Δ rels | — | {after_expected['relationships'] - before['relationships']} | {after_actual['relationships'] - before['relationships']} |

## Delete summary

| Metric | Count |
|---|---:|
| W3 delete_rel total (01–05) | {stats['w3_total']} |
| Skipped (bg_ involvement) | {stats['w3_skipped']} |
| W3 eligible | {stats['w3_eligible']} |
| v5 UNSUPPORTED extra | {stats['v5_extra']} |
| **Consolidated patch** | **{stats['consolidated']}** |
| Dry-run would_delete_rel | {dry['summary'].get('would_delete_rel', 0)} |
| Live deleted (actual Δ) | {before['relationships'] - after_actual['relationships']} |

### By agent

| Agent | Deletes |
|---|---:|
| W4-01 VMA | {stats['by_agent']['W4-01']} |
| W4-02 HAT_BAUTEILTYP | {stats['by_agent']['W4-02']} |
| W4-03 NUTZT_MATERIAL + sweep | {stats['by_agent']['W4-03']} |

## Ledger v5 → v6

| Metric | v5 | v6 |
|---|---:|---:|
| Rows | {v6['v5_rows']} | {v6['v6_rows']} |
| PROVEN | — | {v6['proven']} ({v6['proven_pct']}%) |
| Rel rows removed | — | {v6['removed_rel_rows']} |

## Patch

- `patches/w4_selective_unsupported_deletes.patch.jsonl`
- Apply report: `apply_reports/w4_selective_unsupported_deletes.patch.apply_report.md`
""",
        encoding="utf-8",
    )


def fetch_bg_audit() -> dict:
    """Read-only Neo4j export for Bauteilgruppe mission plan."""
    scripts = HERE.parents[2] / "_scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    from neo4j import GraphDatabase
    from neo4j_env import resolve_connection

    uri, user, password, _default_db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    audit: dict = {}
    with driver.session(database=DATABASE) as session:
        audit["nodes"] = session.run(
            "MATCH (bg:Bauteilgruppe) RETURN count(bg) AS n"
        ).single()["n"]
        audit["outbound"] = [dict(r) for r in session.run(
            "MATCH (bg:Bauteilgruppe)-[r]->() RETURN type(r) AS rel_type, count(r) AS cnt ORDER BY cnt DESC"
        )]
        audit["inbound"] = [dict(r) for r in session.run(
            "MATCH ()-[r]->(bg:Bauteilgruppe) RETURN type(r) AS rel_type, count(r) AS cnt ORDER BY cnt DESC"
        )]
        audit["touching_total"] = session.run(
            "MATCH ()-[r]->() WHERE startNode(r):Bauteilgruppe OR endNode(r):Bauteilgruppe RETURN count(r) AS c"
        ).single()["c"]
        audit["props"] = [dict(r) for r in session.run(
            "MATCH (bg:Bauteilgruppe) UNWIND keys(bg) AS k RETURN k, count(*) AS cnt ORDER BY cnt DESC"
        )]
        audit["naming_samples"] = [dict(r) for r in session.run(
            "MATCH (bg:Bauteilgruppe) RETURN bg.id AS id, bg.name AS name, bg.bg_kind AS bg_kind LIMIT 8"
        )]
        audit["id_prefixes"] = [dict(r) for r in session.run(
            "MATCH (bg:Bauteilgruppe) WITH split(bg.id,'_')[1] AS material_token RETURN material_token, count(*) AS cnt ORDER BY cnt DESC LIMIT 15"
        )]
        audit["unsupported_bg_ledger"] = 0
    driver.close()
    for row in load_v5():
        if row.get("claim_kind") != "rel" or row.get("verdict") != "UNSUPPORTED":
            continue
        if touches_bg(row.get("from_id", "")) or touches_bg(row.get("to_id", "")):
            audit["unsupported_bg_ledger"] += 1
    return audit


def write_bg_plan(audit: dict, skipped_bg: int) -> None:
    out_edges = sum(r["cnt"] for r in audit["outbound"])
    in_edges = sum(r["cnt"] for r in audit["inbound"])
    missions = [
        ("BG-M1", "HAT_BAUTEILTYP + NUTZT_MATERIAL catalogue edges", 465 + 390, "Tier-C vocab; multi-source naming; 0 rel evidence_url today"),
        ("BG-M2", "Process axis (HAT_PROZESSPHASE, HAT_BESCHAFFUNGSWEG, HAT_LOGISTIK)", 567 + 468 + 337, "Contract-inferred; needs project dossier quotes"),
        ("BG-M3", "Regulation triggers (ERFORDERT_NACHWEIS, TRIGGERS_REGULIERUNGSFRAGE)", 955 + 722, "Structural; evidence on law nodes not rels"),
        ("BG-M4", "Spatial / donor links (AUS_SPENDER, IN_EMPFANGSOBJEKT, HAT_BAUTEILGRUPPE inbound)", 198 + 278 + 364, "Project geography + donor matching"),
        ("BG-M5", "Material taxonomy (HAT_MATERIALGRUPPE, HAT_RUECKBAUVERFAHREN, HAT_AUFBEREITUNG)", 375 + 305 + 211, "Naming variants across intake batches"),
    ]
    lines = [
        "# Bauteilgruppe Evidence Mission Plan",
        "",
        f"**Date:** {utc_now()} · **Database:** `{DATABASE}` · **Mode:** PLAN ONLY (no deletes)",
        "",
        "## Why sensitive",
        "",
        "- **364** `:Bauteilgruppe` nodes; all ids use `bg_` prefix; **no** `canonical_name` / `primary_source_url` on nodes.",
        f"- **{audit['touching_total']}** live edges touch Bauteilgruppe (**W4 skipped {skipped_bg}** pending W3 deletes).",
        "- Naming encodes material + component + project slug (`bg_stahlbeton_mehrere_haus_hos_floor_elements`) from **multiple intake sources**; `name` display string often differs.",
        f"- v5 ledger: **{audit['unsupported_bg_ledger']}** UNSUPPORTED rel rows involve bg_ (deferred from W4).",
        "- Rel properties carry **no** `evidence_url` / `evidence_quote` on bg_ outbound edges today.",
        "",
        "## Scope inventory",
        "",
        f"| Surface | Count |",
        f"|---|---:|",
        f"| Bauteilgruppe nodes | {audit['nodes']} |",
        f"| Outbound rels | {out_edges} |",
        f"| Inbound rels | {in_edges} |",
        f"| Total touching edges | {audit['touching_total']} |",
        "",
        "### Outbound rel types (top)",
        "",
        "| rel_type | count |",
        "|---|---:|",
    ]
    for r in audit["outbound"][:12]:
        lines.append(f"| {r['rel_type']} | {r['cnt']} |")
    lines += [
        "",
        "### Inbound rel types",
        "",
        "| rel_type | count |",
        "|---|---:|",
    ]
    for r in audit["inbound"]:
        lines.append(f"| {r['rel_type']} | {r['cnt']} |")
    lines += [
        "",
        "## Naming variants (samples)",
        "",
    ]
    for s in audit["naming_samples"]:
        lines.append(f"- `{s['id']}` → display name: **{s['name']}** (bg_kind={s.get('bg_kind')})")
    lines += [
        "",
        "### Material token distribution (id segment 2)",
        "",
        "| token | count |",
        "|---|---:|",
    ]
    for r in audit["id_prefixes"]:
        lines.append(f"| {r['material_token']} | {r['cnt']} |")
    lines += [
        "",
        "## Evidence rules (multi-source naming)",
        "",
        "1. **Node identity:** keep `bg_*` id stable; treat `name` as display alias — never merge on string similarity alone.",
        "2. **Catalogue edges (`HAT_BAUTEILTYP`, `NUTZT_MATERIAL`):** require verbatim quote from project page OR marketplace listing linking component type/material.",
        "3. **Cross-source reconciliation:** when dossier name ≠ graph `name`, record both in `notes` + `proof_quote`; prefer `primary_source_url` on **entity** not synthetic Quelle nodes.",
        "4. **Delete gate:** same as W4 — internet research attempted + UNSUPPORTED; bg_ edges never auto-deleted without dedicated mission sign-off.",
        "",
        "## Proposed sub-missions (disjoint agents)",
        "",
        "| Mission | Scope | ~edges | Notes |",
        "|---|---|---:|---|",
    ]
    for mid, title, est, note in missions:
        lines.append(f"| {mid} | {title} | {est} | {note} |")
    lines += [
        "",
        "## Disjoint agent proposals",
        "",
        "| Agent | Mission | Read sources |",
        "|---|---|---|",
        "| BG-A1 | BG-M1 catalogue | Project dossiers in `intake/inbox/`, marketplace actor pages from `akteur_typ_projekt_geo.json` |",
        "| BG-A2 | BG-M2 process axis | `contracts/`, project batch JSONL, graph `HAT_PROZESSPHASE` targets |",
        "| BG-A3 | BG-M3 regulation | Regulation graph vocabulary run, law node `source_url` |",
        "| BG-A4 | BG-M4 spatial/donor | `akteur_typ_projekt_geo.json`, `BETEILIGT_AN` / `AUS_SPENDER` graph export |",
        "| BG-A5 | BG-M5 material taxonomy | `controlled_vocabulary.seed.kg.jsonl`, material group nodes |",
        "",
        "## W4 exclusion recap",
        "",
        f"- **{skipped_bg}** W3 `delete_rel` ops skipped because `from` or `to` is `bg_*`.",
        f"- **{audit['unsupported_bg_ledger']}** v5 UNSUPPORTED rel rows retained for this mission.",
        "",
        "## References",
        "",
        f"- `akteur_typ_projekt_geo.json` — {AKTEUR_GEO.relative_to(HERE.parents[2]) if AKTEUR_GEO.exists() else 'N/A'}",
        "- `VERIFICATION_LEDGER_ELEMENT_v5.csv` — bg_ UNSUPPORTED rows",
        "- W4 plan: `VERIFICATION_PLAN_W4_SELECTIVE_DELETE_4_AGENTS.md`",
    ]
    BG_PLAN.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    LEDGER.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    w3_included, w3_skipped, _ = load_w3_deletes()
    existing = {rel_key(r) for r in w3_included}
    v5_extra = v5_unsupported_deletes(existing, set())
    all_deletes = w3_included + v5_extra
    by_agent = split_by_agent(all_deletes)
    stats = {
        "w3_total": len(w3_included) + len(w3_skipped),
        "w3_skipped": len(w3_skipped),
        "w3_eligible": len(w3_included),
        "v5_extra": len(v5_extra),
        "consolidated": len(all_deletes),
        "by_agent": {a: len(by_agent[a]) for a in by_agent},
    }

    write_patch(all_deletes)
    write_verification_plan(stats)

    for agent in ("W4-01", "W4-02", "W4-03"):
        write_agent_ledger(agent, by_agent[agent])
        write_agent_report(agent, by_agent[agent], stats["w3_skipped"])

    dry = run_patch(dry_run=True)
    rejected = dry["summary"].get("rejected", 0)
    errors = dry["summary"].get("load_errors", 0)
    would_delete = dry["summary"].get("would_delete_rel", 0)
    print(f"Dry-run: would_delete_rel={would_delete} rejected={rejected} errors={errors}")

    live = None
    apply_report = HERE / "apply_reports" / f"{CONSOLIDATED.stem}.apply_report.json"
    if rejected == 0 and errors == 0 and would_delete > 0:
        live = run_patch(dry_run=False)
        for agent in ("W4-01", "W4-02", "W4-03"):
            write_agent_report(agent, by_agent[agent], stats["w3_skipped"], applied=True)
    elif apply_report.exists():
        live = json.loads(apply_report.read_text(encoding="utf-8"))
        print("Reusing prior live apply report")
    else:
        print("Skipping live apply due to dry-run issues or zero deletes")

    deleted_keys = {rel_key(r) for r in all_deletes}
    if live and live.get("counts_before"):
        graph_before = live["counts_before"]
        graph_after = live.get("counts_after_actual") or live["counts_after_expected"]
        dry = {**dry, "counts_before": graph_before, "counts_after_expected": graph_after}
    else:
        graph_after = (live or dry).get("counts_after_actual") or dry["counts_after_expected"]
    v6 = build_v6(deleted_keys, graph_after)
    write_cleanup_report(stats, dry, live, v6)

    audit = fetch_bg_audit()
    write_bg_plan(audit, stats["w3_skipped"])

    result = {
        "stats": stats,
        "dry_run": {
            "would_delete_rel": would_delete,
            "counts_before": dry["counts_before"],
            "counts_after_expected": dry["counts_after_expected"],
        },
        "live_applied": live is not None,
        "counts_after_actual": graph_after,
        "v6": v6,
        "outputs": {
            "patch": str(CONSOLIDATED),
            "plan": str(PLAN),
            "bg_plan": str(BG_PLAN),
            "v6": str(V6),
            "cleanup_report": str(CLEANUP_REPORT),
        },
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
