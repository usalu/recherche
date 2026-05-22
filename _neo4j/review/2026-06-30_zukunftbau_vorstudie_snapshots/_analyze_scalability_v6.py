"""Summarise RSI v6 scores for reports."""
from __future__ import annotations

import json
import statistics as st
import sys
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent


def main() -> None:
    rows = json.loads((HERE / "project_scalability_scores_v6.json").read_text(encoding="utf-8"))
    finals = [r["RSI_final"] for r in rows]
    gate_zero = sum(1 for r in rows if any(r["gates"][g] == 0 for g in r["gates"]))
    k2_ge3 = sum(1 for r in rows if r["K2_raw"] >= 3)
    k9_eq4 = sum(1 for r in rows if r["K9_raw"] == 4)
    m4_block = sum(1 for r in rows if r["K4_raw"] <= 1 and (r.get("n_tragend") or 0) > 0)

    out = {
        "version": "v6",
        "n": len(rows),
        "median_rsi_final": round(st.median(finals), 1),
        "max_rsi_final": max(finals),
        "min_rsi_final": min(finals),
        "gate_zero_count": gate_zero,
        "k2_ge_3": k2_ge3,
        "k9_eq_4": k9_eq4,
        "m4_structural_low_k4": m4_block,
        "archetypes": dict(Counter(r["archetyp"] for r in rows).most_common()),
        "einstufung": dict(Counter(r["einstufung"] for r in rows).most_common()),
        "confidence": dict(Counter(r["confidence_class"] for r in rows).most_common()),
        "top5": [
            {"rang": r["rang"], "name": r["name"], "RSI_final": r["RSI_final"],
             "archetyp": r["archetyp"], "verified": r["verified"]}
            for r in rows[:5]
        ],
        "peoples_pavilion": next(r for r in rows if "People" in r["name"]),
        "ka13": next(r for r in rows if "KA13" in r["name"]),
    }
    (HERE / "scalability_v6_results.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
