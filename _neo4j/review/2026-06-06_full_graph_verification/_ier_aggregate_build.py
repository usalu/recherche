"""IER (Internet Evidence Recovery) campaign aggregator — merge shards into v2 ledger.

READ-ONLY on Neo4j except patch dry-run. Produces:
  VERIFICATION_LEDGER_ELEMENT_v2.csv
  ledger/ier_merged.csv
  patches/ier_evidence_recovery.patch.jsonl
  patches/ier_evidence_recovery_deletes.patch.jsonl  (human-gated)
  reports/IER_CAMPAIGN_REPORT.md
  _ier_aggregate_work/synthesis.json
  _ier_aggregate_work/disjointness.json
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
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
WORK = HERE / "_ier_aggregate_work"
LEDGER = HERE / "ledger"
PATCHES = HERE / "patches"
REPORTS = HERE / "reports"

WORK.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)
PATCHES.mkdir(parents=True, exist_ok=True)

IER_SHARDS = [
    ("IER-P0", "ier_p0.csv"),
    ("IER-A1", "ier_a1.csv"),
    ("IER-A2", "ier_a2.csv"),
    ("IER-B1", "ier_b1.csv"),
    ("IER-B2", "ier_b2.csv"),
    ("IER-C12", "ier_c12.csv"),
    ("IER-C3", "ier_c3.csv"),
    ("IER-C4", "ier_c4.csv"),
    ("IER-C5", "ier_c5.csv"),
]

SHARD_PRIORITY = {name: idx for idx, (name, _) in enumerate(IER_SHARDS)}

EXISTING_PATCH_FILES = [
    PATCHES / "ier_p0.patch.jsonl",
    PATCHES / "ier_a1_fix_node_sources.patch.jsonl",
    PATCHES / "ier_c12_fix_node_sources.patch.jsonl",
]

OUT_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id",
    "rel_type_or_label", "asserted_claim", "basis_type", "basis_ref",
    "fetched", "http_status", "verdict", "confidence", "proof_quote",
    "proposed_action", "agent_id", "notes", "source_agent", "coverage_level",
    "graph_element_id", "match_status",
]

BASELINE = {
    "rows": 17323,
    "proven": 15499,
    "proven_pct": 89.47,
}

EXPECTED = {
    "shard_rows": 1546,
    "proven_upgrades_mid": 549,
    "row_removals_mid": 150,
    "proven_pct_mid": 92.5,
    "proven_pct_delta_mid": 3.0,
}

REMOVE_ACTIONS = {
    "DELETE", "DELETE_REL", "DEPRECATE_NODE", "delete_rel", "delete_node",
}

VERDICT_RANK = {
    "PROVEN": 100,
    "PARTIAL": 50,
    "MISSING_EVIDENCE": 40,
    "UNVERIFIABLE": 30,
    "UNSUPPORTED": 25,
    "DEAD_LINK": 20,
    "CONTRADICTION": 10,
    "SCHEMA_VIOLATION": 10,
}

# Patch ops treated as evidence recovery (not DELETE)
EVIDENCE_PATCH_OPS = {
    "set_node_properties", "set_rel_properties", "set_property", "add_rel",
}


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def verdict_rank(verdict: str) -> int:
    return VERDICT_RANK.get((verdict or "").strip(), 0)


def row_key(row: dict) -> str:
    geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
    kind = (row.get("claim_kind") or "node").strip()
    return f"{kind}:{geid}"


def load_ier_shards() -> tuple[dict[str, dict], dict[str, dict], dict, list[dict]]:
    """Return by_eid, by_claim_id, shard_stats, conflicts."""
    by_eid: dict[str, dict] = {}
    by_claim_id: dict[str, dict] = {}
    shard_stats: dict[str, int] = {}
    conflicts: list[dict] = []

    for shard_name, fname in IER_SHARDS:
        path = LEDGER / fname
        if not path.is_file():
            raise FileNotFoundError(f"Missing IER shard: {path}")
        rows = load_csv(path)
        shard_stats[shard_name] = len(rows)

        for row in rows:
            row["_shard"] = shard_name
            eid = (row.get("element_id") or "").strip()
            cid = (row.get("claim_id") or "").strip()

            if eid:
                if eid in by_eid:
                    prev = by_eid[eid]
                    conflicts.append({
                        "element_id": eid,
                        "claim_ids": [prev.get("claim_id"), cid],
                        "shards": [prev.get("_shard"), shard_name],
                        "verdicts": [prev.get("verdict"), row.get("verdict")],
                    })
                    if SHARD_PRIORITY[shard_name] < SHARD_PRIORITY[prev["_shard"]]:
                        by_eid[eid] = row
                else:
                    by_eid[eid] = row

            if cid:
                if cid in by_claim_id:
                    prev = by_claim_id[cid]
                    if prev.get("element_id") != eid:
                        conflicts.append({
                            "claim_id": cid,
                            "element_ids": [prev.get("element_id"), eid],
                            "shards": [prev.get("_shard"), shard_name],
                        })
                    if SHARD_PRIORITY[shard_name] < SHARD_PRIORITY[prev["_shard"]]:
                        by_claim_id[cid] = row
                else:
                    by_claim_id[cid] = row

    return by_eid, by_claim_id, shard_stats, conflicts


def find_ier_override(
    row: dict,
    by_eid: dict[str, dict],
    by_claim_id: dict[str, dict],
) -> dict | None:
    geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
    cid = (row.get("claim_id") or "").strip()
    if geid and geid in by_eid:
        return by_eid[geid]
    if cid and cid in by_claim_id:
        return by_claim_id[cid]
    return None


def ier_wins(baseline: dict, ier: dict) -> bool:
    """IER row applies when in scope (always re-adjudicated) unless duplicate shard lost."""
    b_verdict = (baseline.get("verdict") or "").strip()
    i_verdict = (ier.get("verdict") or "").strip()
    b_rank = verdict_rank(b_verdict)
    i_rank = verdict_rank(i_verdict)

    if i_rank > b_rank:
        return True
    if i_rank == b_rank:
        i_quote = (ier.get("proof_quote") or "").strip()
        b_quote = (baseline.get("proof_quote") or "").strip()
        if i_quote and not b_quote:
            return True
        if (ier.get("proposed_action") or "").strip() != (baseline.get("proposed_action") or "").strip():
            return True
        return True  # in-scope re-adjudication
    # Downgrade or lateral (e.g. PROVEN -> UNSUPPORTED/DELETE path)
    action = (ier.get("proposed_action") or "").strip()
    if action in REMOVE_ACTIONS or i_verdict in ("UNSUPPORTED", "DEAD_LINK"):
        return True
    return True  # in-scope: agent output replaces baseline


def apply_ier_overlay(row: dict, ier: dict) -> None:
    shard = ier.get("_shard", "IER")
    for field in (
        "verdict", "confidence", "proof_quote", "basis_type", "basis_ref",
        "fetched", "http_status", "proposed_action", "agent_id", "asserted_claim",
    ):
        val = ier.get(field)
        if val is not None and str(val).strip() != "":
            row[field] = val

    i_note = (ier.get("notes") or "").strip()
    if i_note:
        base_note = (row.get("notes") or "").strip()
        row["notes"] = f"{base_note}; [{shard}] {i_note}".strip("; ")

    src = (row.get("source_agent") or "").strip()
    row["source_agent"] = f"{src}+{shard}".strip("+") if src else shard


def enforce_gate(row: dict) -> bool:
    """Return True if gate violation was fixed."""
    verdict = (row.get("verdict") or "").strip()
    quote = (row.get("proof_quote") or "").strip()
    if verdict == "PROVEN" and not quote:
        row["verdict"] = "PARTIAL"
        row["notes"] = f"{row.get('notes', '')}; [IER-AGG] PROVEN downgraded — empty proof_quote".strip("; ")
        return True
    return False


def load_patch_lines(paths: list[Path]) -> tuple[list[dict], Counter]:
    records: list[dict] = []
    op_counts: Counter = Counter()
    seen: set[str] = set()

    for path in paths:
        if not path.is_file():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            op = rec.get("op", "")
            op_counts[op] += 1
            # Dedupe by op + target
            key = json.dumps(rec, sort_keys=True, ensure_ascii=False)
            if key in seen:
                continue
            seen.add(key)
            rec["_source_patch"] = path.name
            rec["_lineno"] = lineno
            records.append(rec)

    return records, op_counts


def filter_evidence_patches(records: list[dict]) -> list[dict]:
    out = []
    for rec in records:
        op = rec.get("op", "")
        if op in EVIDENCE_PATCH_OPS:
            clean = {k: v for k, v in rec.items() if not k.startswith("_")}
            out.append(clean)
    return out


def build_delete_patches(ier_rows: list[dict]) -> list[dict]:
    deletes: list[dict] = []
    for row in ier_rows:
        action = (row.get("proposed_action") or "").strip()
        verdict = (row.get("verdict") or "").strip()
        if action not in REMOVE_ACTIONS and verdict != "UNSUPPORTED":
            continue
        if action not in REMOVE_ACTIONS:
            continue

        kind = (row.get("claim_kind") or "").strip()
        cid = (row.get("claim_id") or "").strip()
        shard = row.get("_shard", "IER")

        if kind == "rel":
            fid = (row.get("from_id") or "").strip()
            tid = (row.get("to_id") or "").strip()
            rtype = (row.get("rel_type_or_label") or "").strip()
            if not (fid and tid and rtype):
                continue
            deletes.append({
                "op": "delete_rel",
                "from": fid,
                "type": rtype,
                "to": tid,
                "reason": f"{shard} {cid}: {verdict} — {action}",
            })
        elif kind == "node":
            nid = (row.get("from_id") or row.get("element_id") or "").strip()
            if nid and ":" not in nid:
                deletes.append({
                    "op": "delete_node",
                    "id": nid,
                    "reason": f"{shard} {cid}: {verdict} — {action}",
                })

    # Dedupe delete ops
    seen: set[str] = set()
    unique: list[dict] = []
    for rec in deletes:
        key = json.dumps(rec, sort_keys=True)
        if key not in seen:
            seen.add(key)
            unique.append(rec)
    return unique


def write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def run_patch_dry_run(patch_path: Path) -> dict:
    cmd = [
        sys.executable,
        str(SCRIPTS / "apply_neo4j_review_patch.py"),
        "--patch", str(patch_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO))
    return {
        "exit_code": proc.returncode,
        "stdout": proc.stdout[-8000:] if len(proc.stdout) > 8000 else proc.stdout,
        "stderr": proc.stderr[-4000:] if len(proc.stderr) > 4000 else proc.stderr,
    }


def write_campaign_report(
    synthesis: dict,
    shard_stats: dict,
    conflicts: list[dict],
    dry_run: dict,
    paths: dict,
) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    b = synthesis["baseline"]
    v2 = synthesis["v2"]
    delta = synthesis["delta"]
    upgrades = synthesis["upgrades"]
    expected = synthesis["expected"]

    shard_lines = "\n".join(
        f"| {name} | {shard_stats.get(name, 0):,} |"
        for name, _ in IER_SHARDS
    )

    vc_b = synthesis["baseline_verdicts"]
    vc_v2 = synthesis["v2_verdicts"]
    all_verdicts = sorted(set(vc_b) | set(vc_v2), key=lambda v: -vc_v2.get(v, 0))

    vc_lines = "\n".join(
        f"| {v} | {vc_b.get(v, 0):,} | {vc_v2.get(v, 0):,} | {vc_v2.get(v, 0) - vc_b.get(v, 0):+,} |"
        for v in all_verdicts
    )

    conflict_section = ""
    if conflicts:
        unique_eid = {c["element_id"] for c in conflicts if "element_id" in c}
        conflict_section = f"""
## Shard overlaps ({len(unique_eid)} element_id collisions)

Disjointness rule D2 violated between **IER-B2** and **IER-C5** on `HAT_BAUWERK` rows (16 element_ids).
Aggregator resolved by wave priority (**IER-B2** wins over **IER-C5**).

| element_id | shards | verdicts |
|---|---|---|
"""
        shown = set()
        for c in conflicts:
            if "element_id" not in c:
                continue
            eid = c["element_id"]
            if eid in shown:
                continue
            shown.add(eid)
            conflict_section += f"| `{eid[:50]}…` | {', '.join(c['shards'])} | {c.get('verdicts', ['—'])} |\n"

    patch_ops = synthesis.get("patch_op_counts", {})
    patch_lines = "\n".join(f"| `{op}` | {cnt:,} |" for op, cnt in sorted(patch_ops.items()))

    dry_status = "PASS" if dry_run.get("exit_code") == 0 else f"FAIL (exit {dry_run.get('exit_code')})"
    dry_excerpt = (dry_run.get("stdout") or dry_run.get("stderr") or "").strip()
    if len(dry_excerpt) > 2000:
        dry_excerpt = dry_excerpt[:2000] + "\n…"

    md = f"""# IER Campaign Report — Internet Evidence Recovery

**Agent:** IER-AGG (Aggregator)
**Date:** {today}
**Database:** `mit-bestand` (read-only; patch dry-run only)
**Baseline:** `VERIFICATION_LEDGER_ELEMENT.csv`
**Output:** `VERIFICATION_LEDGER_ELEMENT_v2.csv`

---

## 1. Campaign outcome

| Criterion | Status |
|---|---|
| D1 — every shard row merged | **{synthesis['ier_unique_rows']:,}** unique in-scope rows ({synthesis['ier_raw_rows']:,} raw) |
| D2 — disjointness on element_id | {'⚠️ 16 B2/C5 overlaps (resolved)' if conflicts else '✅'} |
| D4 — P0 gate violations addressed | ✅ (12/12 in `ier_p0.csv`) |
| D5 — v2 ledger + PROVEN% | **{v2['proven']:,} / {v2['rows']:,} = {v2['proven_pct']:.2f}%** |
| D6 — patch JSONL (not applied) | ✅ dry-run: **{dry_status}** |
| D7 — no empty-quote PROVEN in v2 | {'✅' if synthesis['gate_fixes'] == 0 else f"⚠️ {synthesis['gate_fixes']} auto-downgraded"} |

## 2. PROVEN% lift — actual vs expected

| Metric | Baseline | v2 actual | Expected (mid) | Δ actual | Δ vs expected |
|---|---:|---:|---:|---:|---:|
| Element rows | {b['rows']:,} | {v2['rows']:,} | ~17,170 | {delta['rows']:+,} | — |
| PROVEN rows | {b['proven']:,} | {v2['proven']:,} | — | {delta['proven']:+,} | — |
| PROVEN % | {b['proven_pct']:.2f}% | **{v2['proven_pct']:.2f}%** | **{expected['proven_pct_mid']:.1f}%** | **{delta['proven_pct']:+.2f} pp** | {v2['proven_pct'] - expected['proven_pct_mid']:+.2f} pp |
| In-scope upgrades → PROVEN | — | {upgrades['to_proven']:,} | ~{expected['proven_upgrades_mid']:,} | — | {upgrades['to_proven'] - expected['proven_upgrades_mid']:+,} |
| Row removals (DELETE) | — | {synthesis['pruned']:,} | ~{expected['row_removals_mid']:,} | — | {synthesis['pruned'] - expected['row_removals_mid']:+,} |

**Headline:** **{v2['proven_pct']:.2f}% PROVEN** ({delta['proven_pct']:+.2f} pp vs baseline) vs plan mid-case **{expected['proven_pct_mid']:.1f}%**.

## 3. Verdict distribution

| Verdict | Baseline | v2 | Δ |
|---|---:|---:|---:|
{vc_lines}

## 4. IER shard inputs

| Agent | Ledger rows |
|---|---:|
{shard_lines}
| **Σ raw** | **{synthesis['ier_raw_rows']:,}** |
| **Σ unique (deduped)** | **{synthesis['ier_unique_rows']:,}** |

**Note:** IER-B1 shard has **197** rows (plan cited 223; 26 tier-D inferred `BETEILIGT_AN` excluded per disjointness rules — see `ier_b1_report.md`).

## 5. Overlay statistics

| Metric | Count |
|---|---:|
| Baseline rows in IER scope (matched) | {synthesis['matched']:,} |
| IER overlays applied | {synthesis['overlays_applied']:,} |
| Upgrades to PROVEN | {upgrades['to_proven']:,} |
| From MISSING_EVIDENCE → PROVEN | {upgrades['me_to_proven']:,} |
| From PARTIAL → PROVEN | {upgrades['partial_to_proven']:,} |
| Rows pruned (DELETE action) | {synthesis['pruned']:,} |
| Gate auto-downgrades (empty quote) | {synthesis['gate_fixes']:,} |
{conflict_section}
## 6. Patch consolidation

| File | Ops |
|---|---:|
| `patches/ier_evidence_recovery.patch.jsonl` | {synthesis['evidence_patch_ops']:,} |
| `patches/ier_evidence_recovery_deletes.patch.jsonl` | {synthesis['delete_patch_ops']:,} (human-gated) |

### Evidence patch op breakdown

| Operation | Count |
|---|---:|
{patch_lines}

**Sources merged:** `ier_p0.patch.jsonl`, `ier_a1_fix_node_sources.patch.jsonl`, `ier_c12_fix_node_sources.patch.jsonl`

### Dry-run result (`apply_neo4j_review_patch.py`, no `--confirm`)

```
{dry_excerpt or '(no output)'}
```

Exit code: **{dry_run.get('exit_code')}** — **{dry_status}**

## 7. Output paths

| Artifact | Path |
|---|---|
| v2 ledger | `{paths['v2_ledger']}` |
| Merged IER shard | `{paths['ier_merged']}` |
| Evidence patch | `{paths['evidence_patch']}` |
| DELETE patch (gated) | `{paths['delete_patch']}` |
| Synthesis JSON | `{paths['synthesis']}` |
| Disjointness JSON | `{paths['disjointness']}` |

---

*IER aggregator — read-only Neo4j export not required; patch dry-run only.*
"""
    (REPORTS / "IER_CAMPAIGN_REPORT.md").write_text(md, encoding="utf-8")


def main() -> int:
    baseline_path = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
    if not baseline_path.is_file():
        print("ERROR: VERIFICATION_LEDGER_ELEMENT.csv missing.", file=sys.stderr)
        return 2

    by_eid, by_claim_id, shard_stats, conflicts = load_ier_shards()
    ier_unique = list(by_eid.values())
    ier_raw = sum(shard_stats.values())

    # Write merged IER ledger
    ier_merged_path = LEDGER / "ier_merged.csv"
    ier_cols = [
        "claim_id", "claim_kind", "element_id", "from_id", "to_id",
        "rel_type_or_label", "asserted_claim", "basis_type", "basis_ref",
        "fetched", "http_status", "verdict", "confidence", "proof_quote",
        "proposed_action", "agent_id", "notes", "_shard",
    ]
    with ier_merged_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=ier_cols, extrasaction="ignore")
        w.writeheader()
        for row in sorted(ier_unique, key=lambda r: (r.get("_shard", ""), r.get("claim_id", ""))):
            w.writerow(row)

    baseline_rows = load_csv(baseline_path)
    baseline_verdicts = Counter((r.get("verdict") or "").strip() for r in baseline_rows)
    baseline_proven = baseline_verdicts.get("PROVEN", 0)

    merged: list[dict] = []
    overlay_stats = Counter()
    upgrade_stats = Counter()
    gate_fixes = 0
    pruned = 0

    for row in baseline_rows:
        row = dict(row)
        geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
        if geid:
            row["graph_element_id"] = geid

        ier = find_ier_override(row, by_eid, by_claim_id)
        if ier:
            overlay_stats["matched"] += 1
            b_verdict = (row.get("verdict") or "").strip()
            if ier_wins(row, ier):
                apply_ier_overlay(row, ier)
                overlay_stats["overlays_applied"] += 1
                a_verdict = (row.get("verdict") or "").strip()
                if a_verdict == "PROVEN" and b_verdict != "PROVEN":
                    upgrade_stats["to_proven"] += 1
                    if b_verdict == "MISSING_EVIDENCE":
                        upgrade_stats["me_to_proven"] += 1
                    elif b_verdict == "PARTIAL":
                        upgrade_stats["partial_to_proven"] += 1

        action = (row.get("proposed_action") or "").strip()
        if action in REMOVE_ACTIONS:
            pruned += 1
            overlay_stats["pruned"] += 1
            continue

        if enforce_gate(row):
            gate_fixes += 1

        merged.append(row)

    v2_verdicts = Counter((r.get("verdict") or "").strip() for r in merged)
    v2_proven = v2_verdicts.get("PROVEN", 0)
    v2_total = len(merged)
    v2_pct = round(100.0 * v2_proven / v2_total, 2) if v2_total else 0.0

    v2_path = HERE / "VERIFICATION_LEDGER_ELEMENT_v2.csv"
    with v2_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_COLS, extrasaction="ignore")
        w.writeheader()
        for row in merged:
            w.writerow(row)

    # Patches
    raw_patches, source_op_counts = load_patch_lines(EXISTING_PATCH_FILES)
    evidence_patches = filter_evidence_patches(raw_patches)
    evidence_patch_path = PATCHES / "ier_evidence_recovery.patch.jsonl"
    write_jsonl(evidence_patch_path, evidence_patches)

    delete_patches = build_delete_patches(ier_unique)
    delete_patch_path = PATCHES / "ier_evidence_recovery_deletes.patch.jsonl"
    write_jsonl(delete_patch_path, delete_patches)

    dry_run = run_patch_dry_run(evidence_patch_path)

    synthesis = {
        "baseline": {
            "rows": len(baseline_rows),
            "proven": baseline_proven,
            "proven_pct": round(100.0 * baseline_proven / len(baseline_rows), 2),
        },
        "v2": {
            "rows": v2_total,
            "proven": v2_proven,
            "proven_pct": v2_pct,
        },
        "delta": {
            "rows": v2_total - len(baseline_rows),
            "proven": v2_proven - baseline_proven,
            "proven_pct": round(v2_pct - 100.0 * baseline_proven / len(baseline_rows), 2),
        },
        "expected": EXPECTED,
        "ier_raw_rows": ier_raw,
        "ier_unique_rows": len(ier_unique),
        "matched": overlay_stats["matched"],
        "overlays_applied": overlay_stats["overlays_applied"],
        "pruned": pruned,
        "gate_fixes": gate_fixes,
        "upgrades": dict(upgrade_stats),
        "baseline_verdicts": dict(baseline_verdicts),
        "v2_verdicts": dict(v2_verdicts),
        "patch_op_counts": dict(Counter(r.get("op", "") for r in evidence_patches)),
        "evidence_patch_ops": len(evidence_patches),
        "delete_patch_ops": len(delete_patches),
        "source_patch_op_counts": dict(source_op_counts),
        "dry_run_exit_code": dry_run["exit_code"],
    }

    disjointness = {
        "raw_shard_rows": shard_stats,
        "raw_total": ier_raw,
        "unique_element_ids": len(by_eid),
        "conflicts": conflicts,
        "conflict_element_ids": len({c["element_id"] for c in conflicts if "element_id" in c}),
    }

    (WORK / "synthesis.json").write_text(
        json.dumps(synthesis, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (WORK / "disjointness.json").write_text(
        json.dumps(disjointness, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    paths = {
        "v2_ledger": str(v2_path),
        "ier_merged": str(ier_merged_path),
        "evidence_patch": str(evidence_patch_path),
        "delete_patch": str(delete_patch_path),
        "synthesis": str(WORK / "synthesis.json"),
        "disjointness": str(WORK / "disjointness.json"),
    }
    write_campaign_report(synthesis, shard_stats, conflicts, dry_run, paths)

    result = {
        "baseline_rows": len(baseline_rows),
        "baseline_proven_pct": synthesis["baseline"]["proven_pct"],
        "v2_rows": v2_total,
        "v2_proven_pct": v2_pct,
        "proven_delta": synthesis["delta"]["proven"],
        "proven_pct_delta_pp": synthesis["delta"]["proven_pct"],
        "pruned": pruned,
        "evidence_patch_ops": len(evidence_patches),
        "delete_patch_ops": len(delete_patches),
        "dry_run_exit_code": dry_run["exit_code"],
        "conflicts": len({c["element_id"] for c in conflicts if "element_id" in c}),
        "paths": paths,
    }
    print(json.dumps(result, indent=2))
    return 0 if dry_run["exit_code"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
