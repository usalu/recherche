#!/usr/bin/env python3
"""Agent G6 — provenance for CONTRADICTION rows + malformed verdict=200 CSV shifts."""
from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(r"e:\recherche")
OUT = REPO / "_neo4j/review/2026-06-06_full_graph_verification"
ELEM = OUT / "VERIFICATION_LEDGER_ELEMENT.csv"
F04 = OUT / "ledger/final_cleanup_f04.csv"
A09 = OUT / "ledger/agent_09.csv"
A13 = OUT / "ledger/agent_13.csv"
A14 = OUT / "ledger/agent_14.csv"

SCHEMA = [
    "provenance_id",
    "issue_class",
    "claim_id",
    "source_shard",
    "introducing_agent",
    "column_shift_root_cause",
    "misparsed_verdict",
    "canonical_verdict",
    "graph_element_id",
    "from_id",
    "to_id",
    "rel_type_or_label",
    "git_intro_commit",
    "git_intro_date",
    "git_intro_artifact",
    "git_file_status",
    "remediation_status",
    "notes",
]

CONTRADICTION_IDS = [
    "09-lis-0006",
    "09-lis-0078",
    "09-lis-0176",
    "09-lis-0190",
    "09-lis-0204",
]

GEO_COMMIT = "ed1d81d9"
GEO_DATE = "2026-06-06"
GEO_ARTIFACT = "_neo4j/review/2026-06-06_project_bg_geo_extract/apply_geo_import.py"


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return "unknown"


def load_index(path: Path, key: str = "claim_id") -> dict[str, dict]:
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return {r[key]: r for r in csv.DictReader(fh) if r.get(key)}


def f04_misparsed_verdict(row: list[str], vi: int) -> str:
    return row[vi] if len(row) > vi else "(short)"


def build_rows() -> list[dict]:
    elem = load_index(ELEM)
    a09 = load_index(A09)
    rows: list[dict] = []
    n = 0

    contra_meta = {
        "09-lis-0006": (
            "bw_alte_kade_tiel",
            "stadt_utrecht",
            "LIEGT_IN_STADT",
            "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153025958211491465",
            "Address Tiel; edge to Utrecht — donor bg_mehrere_boden_green_house links bw_alte_kade_tiel",
            "bauteilgruppe_projekt_addresses.csv; geo extract city propagation",
        ),
        "09-lis-0078": (
            "bw_kerenzerbergtunnel",
            "stadt_zuerich",
            "LIEGT_IN_STADT",
            "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153025958211491001",
            "Address Glarus/Kerenzerberg; edge to Zürich — Juch-Areal project city leak",
            "donor_bauwerke_addresses; bw_kerenzerbergtunnel area_only Glarus",
        ),
        "09-lis-0176": (
            "p_big_dig_building_boston",
            "stadt_boston",
            "LIEGT_IN_STADT",
            "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153025958211490485",
            "Address Cambridge MA; edge to Boston — projekte.csv staedte=Boston;Cambridge",
            "address_registry_draft.json p_big_dig_building_boston",
        ),
        "09-lis-0190": (
            "p_circular_centre_netherlands_prinsenhof_a_reuse_pilot",
            "stadt_arnhem",
            "LIEGT_IN_STADT",
            "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153025958211490597",
            "Address Heerde; edge to Arnhem — receiver at Heerde, donor Prinsenhof Arnhem",
            "bauteilgruppe_projekt_addresses.csv Heerde vs Arnhem donor",
        ),
        "09-lis-0204": (
            "p_haus_hos_mehrfamilienhaus_muehlhausen",
            "stadt_leinefelde",
            "LIEGT_IN_STADT",
            "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155277758025176142",
            "Address Mühlhausen; edge to Leinefelde — donor-site city leaked onto receiver project",
            "bauteilgruppe_projekt_addresses.csv bw_leinefelde_plattenbau_donor",
        ),
    }

    for cid in CONTRADICTION_IDS:
        n += 1
        src = a09.get(cid, {})
        frm, to, rt, eid, note, artifact = contra_meta[cid]
        rows.append({
            "provenance_id": f"G06-{n:03d}",
            "issue_class": "CONTRADICTION_GEO",
            "claim_id": cid,
            "source_shard": "ledger/agent_09.csv",
            "introducing_agent": "09",
            "column_shift_root_cause": "none — valid CSV; genuine geo mismatch",
            "misparsed_verdict": "",
            "canonical_verdict": "CONTRADICTION",
            "graph_element_id": src.get("element_id") or eid,
            "from_id": frm,
            "to_id": to,
            "rel_type_or_label": rt,
            "git_intro_commit": GEO_COMMIT,
            "git_intro_date": GEO_DATE,
            "git_intro_artifact": artifact,
            "git_file_status": "committed",
            "remediation_status": "ESCALATE_HUMAN — re-point LIEGT_IN_STADT or drop donor leak",
            "notes": note,
        })

    with F04.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        vi = header.index("verdict")
        for f04_row in reader:
            if not f04_row:
                continue
            cid = f04_row[0]
            n += 1
            mal = f04_misparsed_verdict(f04_row, vi)
            canon = elem.get(cid, {}).get("verdict", "")
            rows.append({
                "provenance_id": f"G06-{n:03d}",
                "issue_class": "MALFORMED_CSV_VERDICT_200",
                "claim_id": cid,
                "source_shard": "ledger/final_cleanup_f04.csv",
                "introducing_agent": "F04",
                "column_shift_root_cause": "extra empty field: node rows use from_id,,,Akteur (3 commas) shifting http_status into verdict column",
                "misparsed_verdict": mal,
                "canonical_verdict": canon,
                "graph_element_id": elem.get(cid, {}).get("graph_element_id", f04_row[2] if len(f04_row) > 2 else ""),
                "from_id": f04_row[3] if len(f04_row) > 3 else "",
                "to_id": "",
                "rel_type_or_label": "Akteur",
                "git_intro_commit": "",
                "git_intro_date": "2026-06-06",
                "git_intro_artifact": "ledger/final_cleanup_f04.csv (workspace-local)",
                "git_file_status": "untracked",
                "remediation_status": "F09 merge preserved canonical verdict; shard CSV still malformed",
                "notes": f"parsed_cols={len(f04_row)} expected=17; F10 closeout counts 17 verdict=200 (excludes F04-node-0014 blank shift)",
            })

    shard_bugs = [
        (
            "A13-node-pn-0001",
            "ledger/agent_13.csv",
            "13",
            "unquoted comma in basis_ref: pn coverage query (pn_no_fulfill=0, pn_isolated=0)",
            "(blank)",
            "PROVEN",
        ),
        (
            "A14-INV-007",
            "ledger/agent_14.csv",
            "14",
            "unquoted commas in asserted_claim and proof_quote fields on invariant row",
            "false",
            "PROVEN",
        ),
    ]
    for cid, shard, agent, cause, mal, canon in shard_bugs:
        n += 1
        rows.append({
            "provenance_id": f"G06-{n:03d}",
            "issue_class": "MALFORMED_CSV_COLUMN_SHIFT",
            "claim_id": cid,
            "source_shard": shard,
            "introducing_agent": agent,
            "column_shift_root_cause": cause,
            "misparsed_verdict": mal,
            "canonical_verdict": canon,
            "graph_element_id": "",
            "from_id": "",
            "to_id": "",
            "rel_type_or_label": "",
            "git_intro_commit": "",
            "git_intro_date": "2026-06-06",
            "git_intro_artifact": shard,
            "git_file_status": "untracked",
            "remediation_status": "cosmetic in VERIFICATION_LEDGER.csv merge; finding intact in notes",
            "notes": "Flagged by Agent 15 aggregator COVERAGE_PROOF.md §6 item 3",
        })

    for cluster_id, shard, agent, count, cause in [
        (
            "R03-EXTENDED-COLS",
            "ledger/remediation_r03.csv",
            "R03",
            "27",
            "23-col extended re-review schema appended after notes; 27 rows misparsed verdict=200",
        ),
        (
            "R01-EXTENDED-COLS",
            "ledger/remediation_r01.csv",
            "R01",
            "5",
            "18-col rows with trailing re-proof columns beyond 17-col schema",
        ),
    ]:
        n += 1
        rows.append({
            "provenance_id": f"G06-{n:03d}",
            "issue_class": "MALFORMED_CSV_CLUSTER",
            "claim_id": cluster_id,
            "source_shard": shard,
            "introducing_agent": agent,
            "column_shift_root_cause": cause,
            "misparsed_verdict": "200 (subset)",
            "canonical_verdict": "n/a",
            "graph_element_id": "",
            "from_id": "",
            "to_id": "",
            "rel_type_or_label": "",
            "git_intro_commit": "",
            "git_intro_date": "2026-06-06",
            "git_intro_artifact": shard,
            "git_file_status": "untracked",
            "remediation_status": "not merged into ELEMENT ledger as-is",
            "notes": f"{count} rows affected in shard; manual CSV or DictReader with extra columns",
        })

    return rows


def write_csv(rows: list[dict]) -> Path:
    path = OUT / "ledger" / "provenance_g06.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=SCHEMA, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)
    return path


def write_report(rows: list[dict], csv_path: Path) -> Path:
    head = git_head()
    contra = [r for r in rows if r["issue_class"] == "CONTRADICTION_GEO"]
    mal = [r for r in rows if r["issue_class"] == "MALFORMED_CSV_VERDICT_200"]
    shift = [r for r in rows if r["issue_class"].startswith("MALFORMED_CSV")]
    mal200 = [r for r in mal if r["misparsed_verdict"] == "200"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    md = f"""# Git Provenance Report — Agent G6

**Date:** {today} · **Repo:** `e:\\recherche` · **HEAD:** `{head}`  
**Ledger:** [`ledger/provenance_g06.csv`](ledger/provenance_g06.csv) ({len(rows)} rows)  
**Scope:** 5 `CONTRADICTION` element rows · 17 malformed `verdict=200` (http_status leak) · column-shift root-cause trace

---

## 1. Executive summary

| Class | Count | Introducing agent/shard | CSV bug? |
|---|---:|---|:---:|
| **CONTRADICTION** (geo `LIEGT_IN_STADT`) | **5** | Agent **09** (`_agent_09_build.py` → `ledger/agent_09.csv`) | No — valid findings |
| **`verdict=200` http_status leak** | **17** | Final Cleanup **F04** (`ledger/final_cleanup_f04.csv`) | **Yes** |
| **Other column-shift shards** | **2 + 2 clusters** | Agents **13**, **14**; remediation **R01**, **R03** | Yes (cosmetic) |

The **17 malformed `verdict=200` rows** called out in F10 (`FINAL_COVERAGE_PROOF.md` §4) are **not** present in the canonical `VERIFICATION_LEDGER_ELEMENT.csv` after F09 merge (Python `csv.DictReader` reads correct verdicts). They **do** reproduce when parsing the **F04 shard** literally: an extra empty column on node rows shifts `http_status=200` into the `verdict` slot.

**Column-shift bug owner (primary):** Final Cleanup Agent **F04** — all 18 Scope-B actor re-proof rows written with `from_id,,,Akteur` (one comma too many). **17/18** misparsed rows show `verdict=200`; **F04-node-0014** (`gxn`, `fetched=false`) misparses to blank `verdict`.

**Secondary column-shift sources** (campaign source shards, caught by Agent 15): Agent **13** `A13-node-pn-0001` (comma in `basis_ref`); Agent **14** `A14-INV-007` (commas in invariant text); remediation ledgers **R01**/**R03** (extended column layouts).

---

## 2. CONTRADICTION rows (5) — graph provenance

All five are Agent **09** `LIEGT_IN_STADT` checks (`09-lis-*`). They are **legitimate geo contradictions**, not ledger parse errors.

| claim_id | from → to | Issue |
|---|---|---|
| `09-lis-0006` | `bw_alte_kade_tiel` → `stadt_utrecht` | Address **Tiel**; edge says Utrecht |
| `09-lis-0078` | `bw_kerenzerbergtunnel` → `stadt_zuerich` | Address **Glarus**; edge says Zürich |
| `09-lis-0176` | `p_big_dig_building_boston` → `stadt_boston` | Address **Cambridge MA**; `stadt_cambridge_ma` exists |
| `09-lis-0190` | `p_circular_centre_netherlands_prinsenhof_a_reuse_pilot` → `stadt_arnhem` | Address **Heerde**; receiver at wrong Stadt |
| `09-lis-0204` | `p_haus_hos_mehrfamilienhaus_muehlhausen` → `stadt_leinefelde` | Address **Mühlhausen**; donor Leinefelde leaked |

### Git / intake chain

```mermaid
flowchart LR
  geo["2026-06-06_project_bg_geo_extract\\nreuse_geo_graph.json / address_registry"]
  apply["apply_geo_import.py\\ncommit ed1d81d9"]
  graph["mit-bestand LIEGT_IN_STADT edges"]
  a09["Agent 09 _agent_09_build.py"]
  ledger["agent_09.csv CONTRADICTION"]

  geo --> apply --> graph --> a09 --> ledger
```

| Stage | Artifact | Git |
|---|---|---|
| Geo property + `LIEGT_IN_*` backfill | `apply_geo_import.py` | `ed1d81d9` (2026-06-06) — **committed** |
| Address / donor-receiver pairing | `bauteilgruppe_projekt_addresses.csv`, `address_registry_draft.json` | same review folder |
| Verification adjudication | `_agent_09_build.py`, `ledger/agent_09.csv` | **untracked** (campaign workspace) |
| Element ledger | `VERIFICATION_LEDGER_ELEMENT.csv` | **untracked**; rows inherit `source_agent=09` |

**Root cause (graph):** multi-city dossier strings (`Boston;Cambridge`, `Arnhem;Heerde`, `Mühlhausen;Leinefelde`) and donor→receiver address propagation created `LIEGT_IN_STADT` edges to a **primary** `Stadt` node that disagrees with the node's `adresse` field. Agent 09's `CONTRA_OVERRIDE` dict explicitly encodes the first two cases.

**Remediation:** re-point or delete the five edges (see `reports/agent_09.md` §5) — **not** a ledger-CSV fix.

---

## 3. Malformed `verdict=200` (17 rows) — F04 shard

| Field | Detail |
|---|---|
| **Shard** | `ledger/final_cleanup_f04.csv` (18 Scope-B `Akteur` nodes, P6-04) |
| **Writer** | Final Cleanup Agent **F04** (2026-06-06) |
| **Bug** | Node rows: `{{neo4j_eid}},{{node_id}},,,Akteur` — **extra comma** before label → 18 parsed columns vs 17-header schema |
| **Symptom** | `http_status` value `200` lands in `verdict` column under strict positional parse |
| **F10 count** | **17** rows with `verdict=200` (excludes `F04-node-0014` where `fetched=false` yields blank misparsed verdict) |
| **Canonical ledger** | F09 merge wrote `VERIFICATION_LEDGER_ELEMENT.csv` with correct `PROVEN`/`PARTIAL`/`UNVERIFIABLE`; `graph_element_id` column holds true `elementId` |

Example (positional shift):

```
…,andreas_sonderegger,,,Akteur,…,true,200,PROVEN,…
                      ^ extra empty field
                              ^ misread as verdict when columns=18
```

---

## 4. Other column-shift shards (Agent 15 audit)

Documented in `COVERAGE_PROOF.md` §6 item 3 and `reports/agent_15.md`:

| Shard | Row | Agent | Root cause |
|---|---|---|---|
| `ledger/agent_13.csv` | `A13-node-pn-0001` | 13 | Comma inside `basis_ref` without quoting: `(pn_no_fulfill=0, pn_isolated=0)` |
| `ledger/agent_14.csv` | `A14-INV-007` | 14 | Commas in `asserted_claim` / `proof_quote` on invariant row |
| `ledger/remediation_r03.csv` | 27 rows | R03 | 23-column extended re-review layout |
| `ledger/remediation_r01.csv` | 5 rows | R01 | Trailing columns beyond 17-col schema |

These did **not** produce the F10 **17× `verdict=200`** metric; that metric is **F04-specific**.

---

## 5. Git history of ledger CSV writes

| Path | `git log --follow` | Notes |
|---|---|---|
| `VERIFICATION_LEDGER_ELEMENT.csv` | **no commits** | Untracked campaign output (F09 merge) |
| `ledger/final_cleanup_f04.csv` | **no commits** | F04 workspace artifact — **source of 17× shift** |
| `ledger/agent_09.csv` | **no commits** | Agent 09 campaign shard |
| `ledger/agent_13.csv`, `agent_14.csv` | **no commits** | 2-row shift bugs |
| `_agent_09_build.py` | **no commits** | Generator for agent_09 shard |
| `apply_geo_import.py` | `ed1d81d9` (2026-06-06) | Committed — introduces geo edges underlying CONTRADICTION |
| `VERIFICATION_LEDGER.schema.csv` | in repo plan commit | Schema reference only |

**Implication:** temporal provenance for ledger **writes** is anchored on **campaign artifact dates** (2026-06-06) and cross-references (F04 report, F09 merge log, Agent 15 aggregator), not git SHAs — same pattern as [G7 provenance](provenance_g07.md) §1.

---

## 6. Recommendations

1. **F04 / all ledger writers:** use `csv.DictWriter(..., quoting=csv.QUOTE_MINIMAL)`; node rows must be `element_id,from_id,,Label` (two commas, not three).
2. **Aggregators:** validate row width == schema width on ingest; reject or quarantine shards with `len(row) != len(header)`.
3. **CONTRADICTION geo:** apply graph patch to fix five `LIEGT_IN_STADT` edges (Agent 09 ESCALATE_HUMAN list) — separate from CSV hygiene.
4. **F10 doc:** clarify that 17× `verdict=200` refers to **F04 shard parse artifact**, not live ELEMENT ledger verdict counts.

---

## 7. Outputs

| File | Role |
|---|---|
| [`ledger/provenance_g06.csv`](ledger/provenance_g06.csv) | Row-level provenance ({len(rows)} rows) |
| [`reports/provenance_g06.md`](reports/provenance_g06.md) | This report |
| [`_build_provenance_g06.py`](../_build_provenance_g06.py) | Regenerator |

*Agent G6 — read-only git + repo audit; no graph mutation.*
"""
    path = OUT / "reports" / "provenance_g06.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(md, encoding="utf-8")
    return path


def main() -> int:
    rows = build_rows()
    csv_path = write_csv(rows)
    report_path = write_report(rows, csv_path)
    print(f"Wrote {csv_path} ({len(rows)} rows)")
    print(f"Wrote {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
