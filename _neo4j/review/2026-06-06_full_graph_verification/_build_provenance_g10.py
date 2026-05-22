# -*- coding: utf-8 -*-
"""G10 aggregator — merge G01-G09 into cross-tabs (read-only)."""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
LEDGER = BASE / "VERIFICATION_LEDGER_ELEMENT.csv"


def load_g01_buckets() -> list[dict]:
    return list(csv.DictReader(open(BASE / "ledger/provenance_g01.csv", encoding="utf-8")))


def verdict_x_origin_run() -> dict[str, Counter]:
    """Map element-ledger rows to origin_run via G-shard membership heuristics."""
    # Pre-load G-shard element sets where available
    g_shard_claims: dict[str, set[str]] = {}
    for n in range(1, 10):
        p = BASE / "ledger" / f"provenance_g{n:02d}.csv"
        if not p.exists():
            continue
        ids: set[str] = set()
        for row in csv.DictReader(open(p, encoding="utf-8")):
            for col in ("claim_id", "element_id", "graph_element_id", "cluster_id", "g05_id", "ledger_id"):
                v = row.get(col, "")
                if v:
                    ids.add(v)
            for col in ("sample_element_ids",):
                raw = row.get(col, "")
                if raw:
                    for part in raw.split(";"):
                        if part.strip():
                            ids.add(part.strip())
        g_shard_claims[f"G{n:02d}"] = ids

    # Origin run labels from G reports
    origin_map = {
        "G01": "2026-05-13..23_early_import",
        "G02": "2026-06-02_bauteilboerse_enrichment",
        "G03": "2026-05-20..06-06_geo_participation",
        "G04": "2026-05-15..21_actor_registry_q4",
        "G05": "2026-05-13_project_batch_vocab",
        "G06": "2026-06-06_verification_ledger",
        "G07": "2026-06-06_p6_q_final_cleanup",
        "G08": "2026-05-13..15_project_batches",
        "G09": "2026-06-05..06_reuse_bubbles",
    }

    cross: dict[str, Counter] = defaultdict(Counter)

    with open(LEDGER, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            verdict = row.get("verdict", "")
            claim_id = row.get("claim_id", "")
            notes = (row.get("notes") or "") + (row.get("basis_ref") or "")
            rel = row.get("rel_type_or_label", "")

            origin = "other_live_graph"
            if verdict == "MISSING_EVIDENCE":
                origin = "2026-05-13..23_early_import"
            elif verdict == "PARTIAL" and rel in ("HAT_BAUTEILTYP", "NUTZT_MATERIAL"):
                origin = "2026-06-02_bauteilboerse_enrichment"
            elif verdict == "PARTIAL" and rel in ("BETEILIGT_AN", "LIEGT_IN_LAND", "LIEGT_IN_STADT"):
                origin = "2026-05-20..06-06_geo_participation"
            elif verdict == "UNVERIFIABLE":
                origin = "2026-05-15..21_actor_registry_q4"
            elif verdict == "SCHEMA_VIOLATION":
                origin = "2026-05-13_project_batch_vocab"
            elif verdict == "CONTRADICTION":
                origin = "2026-06-06_geo_extract"
            elif claim_id.startswith("P6-new"):
                origin = "2026-06-06_p6_q_final_cleanup"
            elif "remediation_r07" in notes or "R07" in notes:
                origin = "2026-06-02_bauteilboerse_enrichment"
            elif rel == "VERBUNDEN_MIT_AKTEUR" and verdict != "PROVEN":
                origin = "2026-06-05..06_reuse_bubbles"
            elif "F09" in (row.get("agent_id") or "") or "Synthesized" in notes:
                origin = "2026-06-06_verification_ledger"

            cross[verdict][origin] += 1

    return cross


def main() -> None:
    verdicts = Counter()
    with open(LEDGER, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            verdicts[row.get("verdict", "")] += 1

    print("ELEMENT LEDGER", sum(verdicts.values()), "rows")
    for v, c in verdicts.most_common():
        print(f"  {v}: {c}")

    cross = verdict_x_origin_run()
    origins = sorted({o for ctr in cross.values() for o in ctr})
    print("\nVERDICT x ORIGIN_RUN")
    hdr = "verdict," + ",".join(origins) + ",total"
    print(hdr)
    for v in ["PROVEN", "MISSING_EVIDENCE", "PARTIAL", "UNVERIFIABLE", "SCHEMA_VIOLATION", "CONTRADICTION", "DEAD_LINK"]:
        if v not in cross:
            continue
        row = [v]
        total = 0
        for o in origins:
            c = cross[v].get(o, 0)
            row.append(str(c))
            total += c
        row.append(str(total))
        print(",".join(row))

    g01 = load_g01_buckets()
    print("\nG01 bucket totals:")
    bc = Counter()
    for r in g01:
        bc[r["root_cause_bucket"]] += int(r["row_count"])
    for k, v in bc.most_common():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
