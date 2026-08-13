# -*- coding: utf-8 -*-
"""Surface semantically thin evidence for mandatory cross-review.

This is a risk report, not an automatic keep/prune decision.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
THIN_TERMS = re.compile(
    r"\b(partner|partners|mitglied|membership|member|signator|unterzeichn|"
    r"sustainab|nachhalt|circular economy|kreislaufwirtschaft)\b", re.I
)


def records(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data["records"]


def main() -> None:
    risks = []
    for path in sorted(HERE.glob("lane_[ABC].json")):
        for rec in records(path):
            if not isinstance(rec, dict) or rec.get("decision") != "keep":
                continue
            for index, ev in enumerate(rec.get("evidence") or []):
                quote = (ev.get("quote") or "").strip()
                supported = ev.get("supports_roles") or []
                flags = []
                if len(quote) < 55:
                    flags.append("short_quote")
                if len(supported) >= 3 and len(quote) < 160:
                    flags.append("many_roles_thin_quote")
                if THIN_TERMS.search(quote):
                    flags.append("generic_or_affiliation_language")
                if flags:
                    risks.append({
                        "lane": path.stem[-1],
                        "eid": rec["eid"],
                        "audit_id": rec["audit_id"],
                        "name": rec["current_name"],
                        "evidence_index": index,
                        "flags": flags,
                        "supports_roles": supported,
                        "url": ev.get("url"),
                        "quote": quote,
                    })
    (HERE / "thin_evidence_risks.json").write_text(
        json.dumps(risks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"thin-evidence review flags: {len(risks)}")


if __name__ == "__main__":
    main()
