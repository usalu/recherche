"""Agent G9 — build provenance_g09 ledger from patch JSONL + git history."""
from __future__ import annotations

import csv
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # _neo4j
RUNS = ROOT / "intake/runs"
REVIEW = ROOT / "review/2026-06-06_cross_bubble_extension"
OUT_DIR = ROOT / "review/2026-06-06_full_graph_verification"
REPO = ROOT.parent


def git_first(path: str) -> tuple[str, str, str]:
    try:
        out = subprocess.check_output(
            ["git", "log", "--format=%H|%ci|%s", "--reverse", "-1", "--", path],
            cwd=REPO,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if not out:
            return "", "", ""
        h, d, s = out.split("|", 2)
        return h[:8], d[:10], s
    except Exception:
        return "", "", ""


def load_removals() -> dict[str, str]:
    removed: dict[str, str] = {}
    for tier, fname in (
        ("T1", "unsupported_edges_removal.patch.jsonl"),
        ("T2", "unsupported_edges_tier2_removal.patch.jsonl"),
    ):
        p = REVIEW / "patches" / fname
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                removed[json.loads(line)["id"]] = tier
    return removed


PATCH_MAP: list[tuple[str, Path, str]] = [
    (
        "2026-05-28_bauteilboersen_integration_plan",
        RUNS / "2026-06-05_germany_reuse_bubble/patches/phase1_ecosystem_spine.patch.jsonl",
        "germany_reuse_bubble",
    ),
]
# rebuilt below in main


MESH_RE = re.compile(
    r"mesh|ecosystem|peer|polycentric|infrastructure_peer|marketplace_peer|"
    r"digital_physical|resource_passport|coordination_ecosystem|practice_triangle|"
    r"idf_reuse|french_reuse|french_marketplace|dutch_reuse|european_reuse|"
    r"european_marketplace|opalis_directory",
    re.I,
)

EVIDENCE_KINDS = {
    "directory",
    "cirkla_directory",
    "committee_co_chair_affiliation",
    "committee_member_affiliation",
    "marketplace_brand_operator",
    "marketplace_listing",
    "formal_partnership",
    "platform_family",
    "oogstkaart_lineage",
    "project_commissioner",
    "programme_funder_platform",
    "research_industry_partner",
    "hdm_research_consortium",
    "research_programme",
    "spirou_consortium",
    "supplier_listing",
    "reuse_matching_pilot",
    "swiss_reuse_media_network",
}


def classify(ck: str, eb: str, conf: str) -> str:
    if "interpretive_conclusion" in eb:
        return "category_inference"
    if MESH_RE.search(ck) or MESH_RE.search(eb):
        if conf == "belegt" and ck in EVIDENCE_KINDS:
            return "evidence_backed"
        return "actor_mesh"
    if ck in EVIDENCE_KINDS or conf == "belegt":
        return "evidence_backed"
    if conf == "teilweise_belegt":
        return "actor_mesh"
    return "mixed"


def pattern_for(from_id: str, to_id: str, ck: str) -> str:
    ids = {from_id, to_id}
    if {"software_restado", "cirkla"} <= ids or {"software_restado", "opalis"} <= ids:
        return "restado_cirkla_hub_pattern"
    if "software_restado" in ids and ("useagain" in ids or "insert_marketplace" in ids):
        return "restado_cross_border_peer_pattern"
    if ck.startswith("dutch_"):
        return "dutch_country_mesh"
    if "opalis_directory" in ck:
        return "opalis_co_listing_mesh"
    if ck == "coordination_ecosystem":
        return "swiss_ecosystem_inference"
    if ck in ("resource_passport_ecosystem", "ecosystem_peer_resource_passport"):
        return "passport_category_mesh"
    return ""


def iter_vma_ops(path: Path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        o = json.loads(line)
        op = o.get("op")
        if op == "delete_rel":
            continue
        if op == "add_rel" and o.get("type") == "VERBUNDEN_MIT_AKTEUR":
            yield o
        elif op == "set_rel_properties":
            rid = o.get("id", "")
            if "verbunden_mit_akteur" in rid:
                yield o


def main():
    removed = load_removals()

    patch_entries: list[tuple[str, Path, str]] = [
        ("2026-05-28_bauteilboersen", RUNS / "2026-05-28_bauteilboersen_integration_plan/patches/bauteilboersen_integration_graph_only.patch.jsonl", "legacy_bauteilboersen"),
        ("2026-06-05_swiss", RUNS / "2026-06-05_swiss_reuse_bubble/patches/phase1_enrichment_connectivity.patch.jsonl", "swiss_reuse_bubble"),
        ("2026-06-05_swiss", RUNS / "2026-06-05_swiss_reuse_bubble/patches/phase3_supply_chain.patch.jsonl", "swiss_reuse_bubble"),
        ("2026-06-05_germany", RUNS / "2026-06-05_germany_reuse_bubble/patches/phase1_ecosystem_spine.patch.jsonl", "germany_reuse_bubble"),
        ("2026-06-05_germany", RUNS / "2026-06-05_germany_reuse_bubble/patches/phase2_bauteilboerse_hannover.patch.jsonl", "germany_reuse_bubble"),
        ("2026-06-05_germany", RUNS / "2026-06-05_germany_reuse_bubble/patches/phase2b_hdm_civic_hub.patch.jsonl", "germany_reuse_bubble"),
        ("2026-06-05_netherlands", RUNS / "2026-06-05_netherlands_reuse_bubble/patches/phase1_dutch_urban_mining_spine.patch.jsonl", "netherlands_reuse_bubble"),
        ("2026-06-05_netherlands", RUNS / "2026-06-05_netherlands_reuse_bubble/patches/phase2_repurpose_demand_layer.patch.jsonl", "netherlands_reuse_bubble"),
        ("2026-06-05_france", RUNS / "2026-06-05_france_reuse_bubble/patches/phase1_france_marketplace_spine.patch.jsonl", "france_reuse_bubble"),
        ("2026-06-05_france", RUNS / "2026-06-05_france_reuse_bubble/patches/phase1c_evidence_hardening.patch.jsonl", "france_reuse_bubble"),
        ("2026-06-05_france", RUNS / "2026-06-05_france_reuse_bubble/patches/phase2_idf_civic_links.patch.jsonl", "france_reuse_bubble"),
        ("2026-06-05_rotor_dc", RUNS / "2026-06-05_rotor_dc_reuse_bubble/patches/phase1_ecosystem_spine.patch.jsonl", "rotor_dc_reuse_bubble"),
        ("2026-06-06_cross_bubble", REVIEW / "patches/cross_bubble_extension.patch.jsonl", "cross_bubble_extension"),
        ("2026-06-06_cross_bubble", REVIEW / "patches/cross_bubble_extension_phase2.patch.jsonl", "cross_bubble_extension"),
    ]

    rows: list[dict] = []
    run_stats: dict[str, dict] = {}

    for run_label, path, scope in patch_entries:
        if not path.exists():
            continue
        rel_path = str(path.relative_to(REPO)).replace("\\", "/")
        gh, gd, gs = git_first(rel_path)
        for o in iter_vma_ops(path):
            props = o.get("properties", {})
            rid = o.get("id") or props.get("id", "")
            from_id = o.get("from", "")
            to_id = o.get("to", "")
            if not from_id and rid:
                m = re.match(r"r_(.+?)__verbunden_mit_akteur__(.+)", rid)
                if m:
                    from_id, to_id = m.group(1), m.group(2)
            ck = props.get("connection_kind", "")
            eb = props.get("evidence_basis", "")
            conf = props.get("evidence_confidence", "")
            rr = props.get("review_run", run_label)
            fab = classify(ck, eb, conf)
            rem = removed.get(rid, "")
            status = f"removed_{rem.lower()}" if rem else "surviving"
            pat = pattern_for(from_id, to_id, ck)

            rows.append(
                {
                    "rel_id": rid,
                    "from_id": from_id,
                    "to_id": to_id,
                    "connection_kind": ck,
                    "evidence_confidence": conf,
                    "fabrication_class": fab,
                    "origin_run": rr,
                    "origin_scope": scope,
                    "origin_patch": rel_path,
                    "git_commit": gh,
                    "git_commit_date": gd,
                    "git_commit_subject": gs,
                    "remediation_status": status,
                    "fabrication_pattern": pat,
                    "evidence_basis": eb,
                }
            )
            st = run_stats.setdefault(scope, {"vma_ops": 0, "mesh": 0, "inference": 0, "removed": 0, "surviving": 0})
            st["vma_ops"] += 1
            if fab == "actor_mesh":
                st["mesh"] += 1
            if fab == "category_inference":
                st["inference"] += 1
            if rem:
                st["removed"] += 1
            else:
                st["surviving"] += 1

    # First origin wins (country bubble before cross-bubble overwrite)
    seen: set[str] = set()
    deduped: list[dict] = []
    for r in rows:
        if r["rel_id"] in seen:
            continue
        seen.add(r["rel_id"])
        r["ledger_id"] = f"G09-{len(deduped)+1:04d}"
        deduped.append(r)

    fieldnames = [
        "ledger_id",
        "rel_id",
        "from_id",
        "to_id",
        "connection_kind",
        "evidence_confidence",
        "fabrication_class",
        "origin_run",
        "origin_scope",
        "origin_patch",
        "git_commit",
        "git_commit_date",
        "git_commit_subject",
        "remediation_status",
        "fabrication_pattern",
        "evidence_basis",
    ]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ledger = OUT_DIR / "ledger" / "provenance_g09.csv"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(deduped)

    # Run summary rows appended
    summary_path = OUT_DIR / "ledger" / "provenance_g09_run_summary.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["origin_scope", "vma_ops", "actor_mesh", "category_inference", "removed", "surviving"],
        )
        w.writeheader()
        for scope, st in sorted(run_stats.items()):
            w.writerow(
                {
                    "origin_scope": scope,
                    "vma_ops": st["vma_ops"],
                    "actor_mesh": st["mesh"],
                    "category_inference": st["inference"],
                    "removed": st["removed"],
                    "surviving": st["surviving"],
                }
            )

    print(f"Wrote {len(deduped)} edges -> {ledger}")
    print(f"Removed: {sum(1 for r in deduped if r['remediation_status'].startswith('removed'))}")
    for scope, st in sorted(run_stats.items()):
        print(scope, st)


if __name__ == "__main__":
    main()
