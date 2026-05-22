#!/usr/bin/env python3
"""Build provenance_g04 ledger + report for UNVERIFIABLE rows (Agent G4)."""
from __future__ import annotations

import csv
import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
LEDGER_IN = ROOT / "VERIFICATION_LEDGER_ELEMENT.csv"
LEDGER_OUT = ROOT / "ledger" / "provenance_g04.csv"
REPORT_OUT = ROOT / "reports" / "provenance_g04.md"
PROV_JSONL = REPO / "_neo4j/processed/actor_registry/provenance/actor_registry.provenance.jsonl"
PATCH_06B = ROOT / "patches/agent06b_add_node_sources.patch.jsonl"
PATCH_15 = ROOT / "patches/agent15_add_node_sources.patch.jsonl"
SOURCED = ROOT / "_agent06b_work/sourced_akteur_nodes.json"
AKTEURLISTE = REPO / "_archive/research/person/akteursliste_master.md"

RESIDUAL_ACTORS = ["anja_rosen", "annabelle_von_reutern", "gxn", "jan_haerens"]

GIT_ANCHORS = {
    "actor_registry_seed": ("13c165fd", "2026-05-15", "restructure and double checking Data"),
    "q4_surface_urls": ("d37e5240", "2026-05-21", "Source Hunting — mig_q4_surface_urls.cypher"),
    "trace_zitiert": ("bd62286a", "2026-05-23", "source check 4 — trace_zitiert_quelle_to_urls"),
    "property_cleanup": ("323cd19b", "2026-06-05", "property cleanup phase 4b/5b"),
    "agent06b_verify": ("", "2026-06-06", "Agent 06b verification — volume-cap deferral"),
    "agent06b_patch": ("", "2026-06-06", "agent06b_add_node_sources.patch.jsonl (42 nodes, not residuals)"),
    "agent08_triage": ("", "2026-06-06", "Agent 08 unsourced-actor triage (477 nodes without source_urls)"),
    "agent15_patch": ("", "2026-06-06", "agent15_add_node_sources.patch.jsonl (17 Agent-08-PROVEN hubs)"),
    "final_f03_f04": ("", "2026-06-06", "F3/F4 re-adjudication — 4 actors remain UNVERIFIABLE"),
}

OUT_COLS = [
    "row_id",
    "ledger_claim_id",
    "claim_kind",
    "element_id",
    "entity_id",
    "rel_type_or_label",
    "verdict_shard",
    "root_cause_bucket",
    "source_urls_on_graph",
    "url_origin_chain",
    "git_anchor_run",
    "git_anchor_date",
    "in_agent06b_add_source_patch",
    "in_agent08_unsourced_scope",
    "agent06b_vs_agent08",
    "residual_actor_flag",
    "recommended_action",
    "notes",
]


def git_first_touch(path_glob: str, needle: str) -> tuple[str, str, str]:
    """Return (hash, date, subject) for first commit touching needle in path."""
    try:
        out = subprocess.check_output(
            [
                "git", "log", "--format=%h|%ai|%s", "-S", needle, "--all", "--", path_glob,
            ],
            cwd=REPO,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if not out:
            return ("", "", "")
        line = out.splitlines()[-1]
        h, dt, subj = line.split("|", 2)
        return (h, dt[:10], subj)
    except (subprocess.CalledProcessError, ValueError):
        return ("", "", "")


def load_jsonl_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    if not path.exists():
        return ids
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(json.loads(line)["id"])
    return ids


def load_provenance() -> dict[str, dict]:
    m: dict[str, dict] = {}
    if not PROV_JSONL.exists():
        return m
    for line in PROV_JSONL.read_text(encoding="utf-8").splitlines():
        o = json.loads(line)
        if o.get("record_type") == "node_provenance":
            m[o["id"]] = o
    return m


def load_sourced_actors() -> dict[str, dict]:
    if not SOURCED.exists():
        return {}
    return {n["id"]: n for n in json.loads(SOURCED.read_text(encoding="utf-8"))}


def bucket_row(row: dict, node_id: str = "") -> str:
    aid = row.get("agent_id", "")
    notes = row.get("notes", "")
    eid = node_id or row.get("from_id") or row.get("element_id", "")
    if aid == "08":
        if "aggregate" in notes.lower():
            return "miscast_aggregate_cluster"
        if "privacy" in notes.lower() or "private" in notes.lower():
            return "miscast_private_anonymised"
        if "generic" in notes.lower() or "not an identifiable" in notes.lower():
            return "miscast_generic_group"
        return "miscast_escalate_human"
    if aid == "10":
        if "timeout" in notes.lower() or "re-fetch" in notes.lower():
            return "fetch_timeout_or_deferred"
        return "software_program_source_weak"
    # 06b sourced actors
    if "F04" in notes and node_id in RESIDUAL_ACTORS:
        return "f04_strict_gate_residual"
    if "DEFERRED (volume cap)" in notes:
        return "06b_volume_cap_deferred"
    if "F04" in notes or "prior_claim_id=P604" in notes:
        return "f04_strict_gate_residual"
    return "06b_source_present_unverified"


def url_origin_chain(entity_id: str, prov: dict, sourced: dict) -> str:
    if entity_id in RESIDUAL_ACTORS or entity_id in sourced:
        p = prov.get(entity_id, {})
        chunks = ",".join(p.get("source_chunks", []))
        return (
            f"akteursliste_master.md → actor_registry ({chunks or '?'}) "
            f"→ BELEGT_IN q_actor_* → mig_q4_surface_urls (2026-05-21) → graph source_urls"
        )
    if entity_id.startswith("recreate_"):
        return "ReCreate integration — aggregate sub-group node, no URL surface"
    if "private" in entity_id or entity_id in {
        "familie_lange", "haus_hos_privater_bauherr", "kamikatsu_residents",
        "maison_dna_private_owner", "maison_vignette_private_owner",
        "private_bauherrschaft_villa_welpeloo", "studierende_freiwillige",
    }:
        return "Legacy geo/project intake — anonymised private actor stub"
    return "varies — see notes"


def agent06b_vs_08(entity_id: str, patch06b: set[str], has_urls: bool) -> str:
    in06b = entity_id in patch06b
    if in06b:
        return "06b ADD_SOURCE patch wrote source_urls after live PROVEN fetch"
    if has_urls:
        return "06b verified scope (had source_urls pre-patch); 08 OUT OF SCOPE (sourced actor)"
    if entity_id in {
        "recreate_dutch_cluster", "recreate_finnish_cluster", "familie_lange",
        "haus_hos_privater_bauherr", "kamikatsu_residents", "maison_dna_private_owner",
        "maison_vignette_private_owner", "private_bauherrschaft_villa_welpeloo",
        "studierende_freiwillige",
    }:
        return "08 IN SCOPE (unsourced) — triaged UNVERIFIABLE miscast; 06b never touched"
    return "10 or regulation shard — neither 06b actor-source nor 08 unsourced tail"


def main() -> None:
    patch06b = load_jsonl_ids(PATCH_06B)
    patch15 = load_jsonl_ids(PATCH_15)
    prov = load_provenance()
    sourced = load_sourced_actors()

    unv_rows: list[dict] = []
    with open(LEDGER_IN, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("verdict") == "UNVERIFIABLE":
                unv_rows.append(row)

    out_rows: list[dict] = []
    for i, row in enumerate(unv_rows, 1):
        node_id = row.get("from_id") or row.get("element_id") or ""
        if row.get("claim_kind") == "rel":
            entity_id = f"{row.get('from_id')}->{row.get('to_id')}:{row.get('rel_type_or_label')}"
        else:
            entity_id = node_id
        bucket = bucket_row(row, node_id)
        snode = sourced.get(node_id, {})
        urls = snode.get("source_urls") or []
        if not urls and row.get("basis_ref"):
            urls = [row["basis_ref"]]
        has_urls = bool(urls)

        anchor_key = "actor_registry_seed"
        if bucket.startswith("06b") or bucket.startswith("f04"):
            anchor_key = "q4_surface_urls"
        elif bucket.startswith("miscast"):
            anchor_key = "agent08_triage"
        elif bucket.startswith("fetch") or bucket.startswith("software"):
            anchor_key = "agent06b_verify"

        anchor = GIT_ANCHORS[anchor_key]
        out_rows.append({
            "row_id": f"G04-{i:04d}",
            "ledger_claim_id": row.get("claim_id", ""),
            "claim_kind": row.get("claim_kind", ""),
            "element_id": row.get("graph_element_id") or row.get("element_id", ""),
            "entity_id": entity_id,
            "rel_type_or_label": row.get("rel_type_or_label", ""),
            "verdict_shard": row.get("agent_id", ""),
            "root_cause_bucket": bucket,
            "source_urls_on_graph": "|".join(urls),
            "url_origin_chain": url_origin_chain(node_id, prov, sourced),
            "git_anchor_run": anchor[2],
            "git_anchor_date": anchor[1],
            "in_agent06b_add_source_patch": str(node_id in patch06b).lower(),
            "in_agent08_unsourced_scope": str(
                not has_urls and row.get("agent_id") == "08"
            ).lower(),
            "agent06b_vs_agent08": agent06b_vs_08(node_id, patch06b, has_urls),
            "residual_actor_flag": str(node_id in RESIDUAL_ACTORS).lower(),
            "recommended_action": row.get("proposed_action", "KEEP"),
            "notes": (row.get("notes") or "")[:500],
        })

    LEDGER_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=OUT_COLS)
        w.writeheader()
        w.writerows(out_rows)

    # Report
    buckets = Counter(r["root_cause_bucket"] for r in out_rows)
    shards = Counter(r["verdict_shard"] for r in out_rows)
    residuals = [r for r in out_rows if r["residual_actor_flag"] == "true"]

    lines = [
        "# Git Provenance — Agent G4 (UNVERIFIABLE rows)",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}  ",
        f"**Ledger:** [`ledger/provenance_g04.csv`](../ledger/provenance_g04.csv)  ",
        f"**Input:** `VERIFICATION_LEDGER_ELEMENT.csv` — **{len(out_rows)}** `UNVERIFIABLE` rows",
        "",
        "## Executive summary",
        "",
        "Almost all UNVERIFIABLE rows (**89/102**) are **sourced `:Akteur` nodes** that Agent 06b",
        "deferred under a **volume cap** (`DEFERRED: not re-fetched`). Their `source_urls` were **not**",
        "written by Agent 06b or Agent 08 — they were denormalized earlier by **Q4 `mig_q4_surface_urls`**",
        "(2026-05-21) from `BELEGT_IN → :Quelle/ExternalLink` URLs originating in the **2026-05-15 actor",
        "registry** import of `_archive/research/person/akteursliste_master.md`.",
        "",
        "**Agent 08** accounts for **9** UNVERIFIABLE rows: unsourced-actor triage of **miscast** entities",
        "(private clients, aggregate ReCreate clusters, generic volunteer groups). None of the four residual",
        "actors appear in Agent 08's scope because they already carried `source_urls`.",
        "",
        "**Agent 10** accounts for **4** UNVERIFIABLE rows (software/program/reallab fetch timeouts).",
        "",
        "The **four F3/F4 residual actors** (`anja_rosen`, `annabelle_von_reutern`, `gxn`, `jan_haerens`)",
        "share one systemic pattern: **registry-curated affiliation URLs** (tool/org/project pages) were",
        "surfaced as `source_urls` but fail the **strict person-naming Evidence Gate** on re-fetch.",
        "",
        "## Counts",
        "",
        "| Shard | UNVERIFIABLE rows |",
        "|---|---:|",
    ]
    for k, v in sorted(shards.items(), key=lambda x: -x[1]):
        lines.append(f"| `{k}` | {v} |")
    lines += ["", "| Root-cause bucket | Count |", "|---|---:|"]
    for k, v in buckets.most_common():
        lines.append(f"| {k} | {v} |")

    lines += [
        "",
        "## Timeline: when `source_urls` were set",
        "",
        "| Date | Run / commit | What happened |",
        "|---|---|---|",
        "| 2026-05-15 | `13c165fd` actor_registry_seed | Actors + `q_actor_*` ExternalLink nodes from `akteursliste_master.md`; URLs live on Quelle nodes via `BELEGT_IN`, not yet on `:Akteur`. |",
        "| 2026-05-21 | `d37e5240` Q4 Source Hunting | `mig_q4_surface_urls.cypher` §Q4.C copies `BELEGT_IN → ExternalLink.url` onto `:Akteur.source_urls` (`migration_origin=mig_q4_surface_urls`). |",
        "| 2026-05-23 | `bd62286a` trace_zitiert | URL binding cleanup; broadens/trims `source_urls` on some labels — actor registry URLs largely stable. |",
        "| 2026-06-05 | property cleanup 4b/5b | `source_urls` preserved (404 nodes unchanged per cleanup summary); Quelle nodes later dropped in reuse-bubble cleanup. |",
        "| 2026-06-06 | Agent **06b** | Audited **sourced** actors (218 gap nodes); **89** marked UNVERIFIABLE without re-fetch (volume cap). **`agent06b_add_node_sources`** added URLs to **42** previously-unsourced actors only — **not** the four residuals. |",
        "| 2026-06-06 | Agent **08** | Scoped to **477 unsourced** actors (`source_urls IS NULL`). Residual four **excluded** (already sourced). Nine miscast unsourced actors → UNVERIFIABLE. |",
        "| 2026-06-06 | Agent **15** patch | `agent15_add_node_sources` — **17** Agent-08-PROVEN hubs; separate from 06b patch. |",
        "| 2026-06-06 | F3/F4 | Re-adjudicated 18+8+1 Scope-B items; four actors remain UNVERIFIABLE under strict graph-URL gate. |",
        "",
        "## 06b vs Agent 08 — import boundary",
        "",
        "| Path | Scope | Effect on `source_urls` | UNVERIFIABLE in G4 |",
        "|---|---|---|---:|",
        "| **06b verification** | `:Akteur` in 06b gap set with existing `source_urls` | Read-only audit; deferred fetch → UNVERIFIABLE | **89** |",
        "| **06b patch** (`agent06b_add_node_sources`) | 42 actors **without** URLs that 06b proved live | `set_node_properties` writes `primary_source_url` + `source_urls` | **0** (patch targets were unsourced) |",
        "| **08 triage** (`ledger/agent_08.csv`) | 477 actors **without** `source_urls` | Proposals only (`ADD_SOURCE` / `ESCALATE_HUMAN`); no graph write in 08 | **9** (miscast only) |",
        "| **15 patch** (`agent15_add_node_sources`) | 17 Agent-08-PROVEN hubs | Graph write for high-confidence unsourced hubs | **0** |",
        "",
        "**Key distinction:** 06b and 08 are **complementary shards** — 06b audited actors that *already had*",
        "registry-derived URLs; 08 hunted actors that *lacked* URLs. The four residuals sit entirely in the",
        "06b/F4 path, not the 08 unsourced tail.",
        "",
        "## Four residual actors (deep trace)",
        "",
    ]

    residual_detail = {
        "anja_rosen": (
            "Registry chunk `actor_registry_061_070`; `q_actor_anja_rosen_01` → `https://urban-mining-index.de/`. "
            "Akteursliste cites UMI **tool** page, not a person bio. Q4 copied URL to `source_urls`. "
            "06b deferred; F4 fetch: homepage names UMI methodology only — **no 'Anja Rosen' string**."
        ),
        "annabelle_von_reutern": (
            "Registry chunk `actor_registry_091_100`; URLs from `q_actor_annabelle_von_reutern_01/02` "
            "(TOMAS + Concular org homepages). F4: `concular.de` loads but **does not name** actor; "
            "`tomas-architecture.com` timeout. Affiliation URLs ≠ person attestation."
        ),
        "gxn": (
            "Registry chunk `actor_registry_101_110`; stub org node (`source_scope=actor_registry_context`). "
            "URL inherited via `r_gxn__BELEGT_IN__q_actor_kasper_guldager_jensen_01` (Circle House PDF from "
            "Kasper Guldager Jensen row). Q4 surfaced PDF URL on `gxn`. F4: PDF fetch timeout; "
            "gxn.3xn.com cookie wall — no verbatim quote under strict gate."
        ),
        "jan_haerens": (
            "Registry chunk `actor_registry_031_040`; three `q_actor_jan_haerens_*` Zinneke/project URLs. "
            "F4: `rotordb.org` Zinneke page credits **Renaud Haerlingen**, not Jan Haerens; "
            "`vai.be` / FCRBE news omit Jan. Off-graph attestation exists but is **not on graph `source_urls`**."
        ),
    }
    for aid in RESIDUAL_ACTORS:
        matches = [x for x in out_rows if x["entity_id"] == aid]
        if not matches:
            continue
        r = matches[0]
        lines += [
            f"### `{aid}`",
            "",
            f"- **Graph `source_urls`:** `{r['source_urls_on_graph']}`",
            f"- **Origin chain:** {r['url_origin_chain']}",
            f"- **06b patch:** {r['in_agent06b_add_source_patch']} · **08 unsourced scope:** {r['in_agent08_unsourced_scope']}",
            f"- **Detail:** {residual_detail[aid]}",
            "",
        ]

    lines += [
        "## Systemic root cause",
        "",
        "1. **Q4 denormalization without person-level validation** — `mig_q4_surface_urls` treats any",
        "   `BELEGT_IN → ExternalLink` as authoritative for `:Akteur`, including org/tool/project pages",
        "   from a curated markdown table.",
        "2. **06b volume cap** — sourced actors were classified UNVERIFIABLE without HTTP re-proof,",
        "   blocking automatic upgrade even when URLs are first-party for the *affiliation*, not the *person*.",
        "3. **Evidence Gate mismatch** — registry stars/links encode **reuse relevance**, not biographical",
        "   proof; F3/F4 strict gate correctly refuses PROVEN but leaves rows permanently UNVERIFIABLE",
        "   until graph URLs are replaced with person-naming sources.",
        "",
        "## Recommendations",
        "",
        "1. **Residual four:** add person-naming URLs to graph (`source_urls`) before re-running F3 — e.g.",
        "   bibliographic sources for Rosen, TOMAS team page for von Reutern, gxn.3xn.com about page for GXN,",
        "   ouest.be / Brussels Architecture Prize for Haerens — then re-fetch.",
        "2. **Bulk 06b deferred (85 actors):** batch spot-fetch pass; many are org-homepage URLs that may",
        "   PROVEN for organisations but stay UNVERIFIABLE for *person* nodes — split person vs org gate.",
        "3. **Agent 08 miscast (9):** do not ADD_SOURCE; remodel as project parts or drop private stubs.",
        "4. **Provenance guard:** new intakes should set `primary_source_url` only from URLs that name the",
        "   entity; keep affiliation URLs on `VERBUNDEN_MIT_AKTEUR` edges with `evidence_url`.",
        "",
        f"---\n\n*Builder:* `_build_provenance_g04.py` · rows: **{len(out_rows)}**",
    ]

    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(out_rows)} rows -> {LEDGER_OUT}")
    print(f"Wrote report -> {REPORT_OUT}")


if __name__ == "__main__":
    main()
