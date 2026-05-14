"""Split Round 001 global patch into accepted blockers and review candidates."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATCH_DIR = ROOT / "_neo4j" / "review" / "round_001" / "patches"
SOURCE = PATCH_DIR / "global_technical.patch.jsonl"
BLOCKERS = PATCH_DIR / "accepted_blockers.patch.jsonl"
CANDIDATES = PATCH_DIR / "canonicalization_candidates.patch.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def main() -> int:
    records = load_jsonl(SOURCE)
    blockers = [record for record in records if record.get("severity") == "BLOCKER"]
    candidates = [record for record in records if record.get("severity") != "BLOCKER"]
    write_jsonl(BLOCKERS, blockers)
    write_jsonl(CANDIDATES, candidates)
    print(
        json.dumps(
            {
                "source": str(SOURCE.relative_to(ROOT)),
                "accepted_blockers": {
                    "path": str(BLOCKERS.relative_to(ROOT)),
                    "records": len(blockers),
                },
                "canonicalization_candidates": {
                    "path": str(CANDIDATES.relative_to(ROOT)),
                    "records": len(candidates),
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
