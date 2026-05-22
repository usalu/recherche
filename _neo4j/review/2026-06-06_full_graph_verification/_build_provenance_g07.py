"""Build ledger/provenance_g07.csv for Git provenance Agent G7."""

from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

REDIRECT_MAP: dict[str, tuple[str, str, str]] = {
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155243673164709898": (
        "Q02",
        "merge_node bw_externe_stahl_donor_stockholder→bw_cleveland_steel_and_tubes_stock",
        "quality_pass_q02_deprecate.patch.jsonl:1",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153025958211485706": (
        "Q02",
        "merge redirect inherited geo from bw_cleveland_steel_reclaimed_stock",
        "quality_pass_q02_deprecate.patch.jsonl:1",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153027057723113482": (
        "Q02",
        "merge redirect inherited LIEGT_IN_LAND",
        "quality_pass_q02_deprecate.patch.jsonl:1",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155341529699582285": (
        "Q02",
        "add_rel AUS_SPENDER redirect bw_wbs70_donor_groeditz→bw_school_type_dresden_donor",
        "quality_pass_q02_deprecate.patch.jsonl:2",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155341529699582431": (
        "Q02",
        "merge redirect AUS_SPENDER from bw_externe_stahl_donor_stockholder",
        "quality_pass_q02_deprecate.patch.jsonl:1",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153084232327762353": (
        "Q01",
        "merge_node bt_hohlkoerperdecke→bt_decke rel redirect",
        "quality_pass_q01.patch.jsonl:6",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155336032141447601": (
        "Q01",
        "merge_node bt_hohlkoerperdecke→bt_decke rel redirect",
        "quality_pass_q01.patch.jsonl:6",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1157587831955132849": (
        "Q01",
        "merge_node bt_hohlkoerperdecke→bt_decke rel redirect",
        "quality_pass_q01.patch.jsonl:6",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153085331839390129": (
        "Q01",
        "merge_node bt_hohlkoerperdecke→bt_decke rel redirect",
        "quality_pass_q01.patch.jsonl:6",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1155337131653075377": (
        "Q01",
        "merge_node bt_hohlkoerperdecke→bt_decke rel redirect",
        "quality_pass_q01.patch.jsonl:6",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1157587831955132850": (
        "Q01",
        "merge_node bt_mauerstein→bt_fassade rel redirect",
        "quality_pass_q01.patch.jsonl:5",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1159840731280445874": (
        "Q01",
        "merge_node bt_mauerstein→bt_fassade rel redirect",
        "quality_pass_q01.patch.jsonl:5",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1157587831955132851": (
        "Q01",
        "merge_node bt_verglasung→bt_fenster rel redirect",
        "quality_pass_q01.patch.jsonl:7",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1159839631768818099": (
        "Q01",
        "merge_node bt_glasscheibe→bt_verglasung→bt_fenster rel redirect",
        "quality_pass_q01.patch.jsonl:2,7",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1162091431582503347": (
        "Q01",
        "merge_node bt_verglasung→bt_fenster rel redirect",
        "quality_pass_q01.patch.jsonl:7",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1157588931466760627": (
        "Q01",
        "merge_node bt_verglasung→bt_fenster rel redirect",
        "quality_pass_q01.patch.jsonl:7",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1159839631768818199": (
        "Q01",
        "merge_node mat_drahtglas→mat_glas rel redirect",
        "quality_pass_q01.patch.jsonl:8",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1157588931466760727": (
        "Q01",
        "merge_node mat_drahtglas→mat_glas rel redirect",
        "quality_pass_q01.patch.jsonl:8",
    ),
    "5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1159842930303702695": (
        "Q02",
        "merge redirect HAT_BAUWERK from bw_externe_stahl_donor_stockholder",
        "quality_pass_q02_deprecate.patch.jsonl:1",
    ),
}


def patch_time(name: str) -> str:
    p = HERE / "apply_reports" / f"{name}.apply_report.json"
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8")).get("generated_at_utc", "")
    return ""


def git_status(path: Path) -> str:
    r = subprocess.run(
        ["git", "status", "--porcelain", str(path)],
        capture_output=True,
        text=True,
        cwd=HERE.parents[2],
    )
    line = r.stdout.strip()
    if not line:
        return "tracked"
    if line.startswith("??"):
        return "untracked"
    return line[:2]


def main() -> int:
    ledger = {
        r["claim_id"]: r
        for r in csv.DictReader(
            (HERE / "VERIFICATION_LEDGER_ELEMENT.csv").open(encoding="utf-8")
        )
    }
    f02 = {
        r["element_id"]: r
        for r in csv.DictReader((HERE / "ledger/final_cleanup_f02.csv").open(encoding="utf-8"))
    }
    f03 = {
        r["element_id"]: r
        for r in csv.DictReader((HERE / "ledger/final_cleanup_f03.csv").open(encoding="utf-8"))
        if r["claim_id"].startswith("F03-rel-0")
    }

    q03_rels: dict[str, int] = {}
    for i, line in enumerate(
        (HERE / "patches/quality_pass_q03.patch.jsonl").read_text(encoding="utf-8").splitlines(),
        1,
    ):
        if not line.strip():
            continue
        op = json.loads(line)
        if op.get("op") == "add_rel" and op.get("type") == "ERFUELLT_NACHWEIS":
            q03_rels[f"{op['from']}|{op['to']}"] = i

    patch_times = {
        "Q01": patch_time("quality_pass_q01.patch"),
        "Q02": patch_time("quality_pass_q02_deprecate.patch"),
        "Q03": patch_time("quality_pass_q03.patch"),
    }

    rows_out: list[dict] = []
    seq = 0
    for cid in sorted(ledger.keys()):
        if not cid.startswith("P6-new"):
            continue
        r = ledger[cid]
        seq += 1
        eid = r["graph_element_id"]
        pq = (r.get("proof_quote") or "").strip()
        empty = not pq and r["verdict"] in ("PROVEN", "PARTIAL")

        origin_pass = ""
        patch_ref = ""
        graph_mutation = ""
        if r["claim_kind"] == "rel" and eid in REDIRECT_MAP:
            origin_pass, graph_mutation, patch_ref = REDIRECT_MAP[eid]
        elif r["claim_kind"] == "rel":
            key = f"{r['from_id']}|{r['to_id']}"
            if key in q03_rels:
                origin_pass = "Q03"
                patch_ref = f"quality_pass_q03.patch.jsonl:{q03_rels[key]}"
                graph_mutation = f"add_rel ERFUELLT_NACHWEIS {r['from_id']}→{r['to_id']}"
        elif r["claim_kind"] == "node":
            origin_pass = "Q03"
            patch_ref = "quality_pass_q03.patch.jsonl"
            graph_mutation = f"add_node {r['from_id']}"

        f2_row = f02.get(eid) or f03.get(eid)
        if empty:
            attestation = "RESIDUAL_EMPTY_QUOTE"
        elif f2_row and pq:
            attestation = (
                "F2_WEB_REPROOF"
                if f2_row.get("basis_type") == "web"
                else "F2_MIXED_REPROOF"
            )
        elif pq and "F08 FIXED_REL_QUOTE" in (r.get("notes") or ""):
            attestation = "F8_GRAPH_QUOTE_BACKFILL"
        elif pq:
            attestation = "F2_OR_F8_QUOTE"
        else:
            attestation = "UNKNOWN"

        rows_out.append(
            {
                "provenance_id": f"G07-{seq:03d}",
                "claim_id": cid,
                "claim_kind": r["claim_kind"],
                "graph_element_id": eid,
                "from_id": r.get("from_id", ""),
                "to_id": r.get("to_id", ""),
                "rel_type_or_label": r.get("rel_type_or_label", ""),
                "origin_quality_pass": origin_pass,
                "patch_ref": patch_ref,
                "patch_applied_utc": patch_times.get(origin_pass, ""),
                "graph_mutation": graph_mutation,
                "synthetic_invented_by": "P6-06",
                "synthetic_script": "_post_quality_p6_06_aggregate.py",
                "synthetic_function": "synthesize_row() L259-326",
                "synthetic_basis_type": r.get("basis_type", ""),
                "synthetic_initial_verdict": "PROVEN",
                "synthetic_initial_proof_quote": "empty",
                "f2_reproof": "yes" if f2_row else "no",
                "f2_ledger": (
                    "final_cleanup_f02.csv"
                    if eid in f02
                    else ("final_cleanup_f03.csv" if eid in f03 else "")
                ),
                "f2_verdict": f2_row["verdict"] if f2_row else "",
                "current_verdict": r.get("verdict", ""),
                "current_proof_quote_empty": str(empty).lower(),
                "attestation_class": attestation,
                "git_file_status": git_status(HERE / "VERIFICATION_LEDGER_ELEMENT.csv"),
                "notes": (r.get("notes") or "")[:160],
            }
        )

    out = HERE / "ledger" / "provenance_g07.csv"
    cols = list(rows_out[0].keys())
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows_out)

    print(
        json.dumps(
            {
                "rows": len(rows_out),
                "redirect": sum(1 for r in rows_out if r["origin_quality_pass"] in ("Q01", "Q02")),
                "q03": sum(1 for r in rows_out if r["origin_quality_pass"] == "Q03"),
                "empty_quote": sum(1 for r in rows_out if r["current_proof_quote_empty"] == "true"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
