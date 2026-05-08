#!/usr/bin/env python3
"""
suggest_new_nodes.py — Identifiziert Korpus-Werte, die nicht zu User-Knoten matchen,
und schlägt neue User-Knoten vor mit Begründung.

Liest _extract/taxonomy_matched/_unmatched.csv, gruppiert nach Entitätstyp,
clustert ähnliche Werte (einfacher Token-Anker), gibt Markdown-Report aus.

Output: _extract/suggested_new_user_nodes.md
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
EXTRACT = ROOT / "_extract"
OUT = EXTRACT / "suggested_new_user_nodes.md"

# Entitätstyp → User-Wurzelordner für Vorschlag
TYPE_TO_FOLDER = {
    "Bauteil": "bauteil",
    "Material": "material",
    "Methode": "methode",
    "Prozessphase": "prozessphase",
    "Aufbereitungsmethode": "aufbereitungsmethode",
    "Wirtschaft": "wirtschaft",
    "Leistungsanforderung": "leistungsanforderung",
    "Tragwerkssystem": "tragwerkssystem",
    "Verbindung": "verbindung",
    "Norm_Recht": "norm/ oder recht/",
    "Pruefung": "pruefung",
    "Huerde": "huerde",
    "Abbruchmethode": "abbruchmethode",
    "Logistik": "logistik",
    "Kennwert": "kennwert",
    "Datenmodell": "datenmodell",
    "Schadstoff": "schadstoff",
    "Reuse_Strategie": "reuse_strategie",
}

ANKER_STOPS = {
    "und", "oder", "der", "die", "das", "mit", "von", "fuer", "the", "and", "of",
    "wiederverwend", "reuse", "wiederverwendet", "wiederverwendete", "neue",
    "alte", "etwa", "ungefaehr", "circa",
    "stahl", "holz", "beton",  # zu generisch
}


def normalize(s: str) -> str:
    s = s.lower()
    s = (s.replace("ä", "ae").replace("ö", "oe")
          .replace("ü", "ue").replace("ß", "ss")
          .replace("²", "2").replace("³", "3")
          .replace("₂", "2").replace("₃", "3"))
    return s


def tokens(s: str) -> set[str]:
    n = normalize(s)
    return {t for t in re.findall(r"[a-z]{4,}", n) if t not in ANKER_STOPS}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    unmatched_path = EXTRACT / "taxonomy_matched" / "_unmatched.csv"
    if not unmatched_path.exists():
        print(f"FEHLER: {unmatched_path} fehlt.")
        return 1

    by_type: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for r in csv.DictReader(unmatched_path.open(encoding="utf-8")):
        by_type[r["entity_type"]].append((r["file"], r["raw_value"]))

    lines: list[str] = [
        "# Empfohlene neue User-Knoten",
        "",
        "Aus dem Korpus extrahierte Werte, die nicht zu existierenden User-Knoten gematched haben.",
        "Token-Anker mit ≥3 Files-Coverage: Vorschlag für neue User-Knoten in den Wurzelordnern.",
        "",
        "Skip-Werte: 'unbekannt', 'unklar', 'n/a', 'fehlt' werden vom Datenluecke-Knoten abgedeckt.",
        "",
    ]

    suggestions_count = 0
    for et in sorted(by_type):
        folder = TYPE_TO_FOLDER.get(et, "unknown")
        unmatched = [(f, v) for f, v in by_type[et]
                     if normalize(v) not in {"unbekannt", "unklar", "n a", "fehlt", "tbd"}]
        if not unmatched:
            continue

        # Token → set of files (Coverage)
        token_files: dict[str, set[str]] = defaultdict(set)
        token_examples: dict[str, list[str]] = defaultdict(list)
        for f, v in unmatched:
            for t in tokens(v):
                token_files[t].add(f)
                if v not in token_examples[t]:
                    token_examples[t].append(v)

        # Anker mit ≥3 Files
        anchors = [(t, len(fs)) for t, fs in token_files.items() if len(fs) >= 3]
        anchors.sort(key=lambda x: -x[1])
        if not anchors:
            continue

        lines.append(f"## {et}  →  `{folder}/`")
        lines.append("")
        lines.append(f"{len(unmatched)} unmatched Korpus-Werte. {len(anchors)} Anker mit ≥3 Files-Coverage:")
        lines.append("")
        for tok, n_files in anchors[:15]:
            examples = token_examples[tok][:5]
            example_str = " · ".join(f"`{e[:60]}`" for e in examples)
            suggested_name = tok.capitalize()
            lines.append(f"### `{folder}/{suggested_name}.md`")
            lines.append(f"")
            lines.append(f"- **Token-Coverage:** {n_files} Files")
            lines.append(f"- **Korpus-Beispiele:** {example_str}")
            lines.append(f"- **Vorschlag-Keywords:** `{tok}`, plus Varianten je nach Begriff")
            lines.append("")
            suggestions_count += 1

    lines.append("---")
    lines.append("")
    lines.append(f"**Gesamt:** {suggestions_count} Knoten-Vorschläge.")
    lines.append("")
    lines.append("Manuelles Vorgehen: Pro relevantem Vorschlag eine .md-Datei im genannten Ordner anlegen,")
    lines.append("Frontmatter analog zu existierenden Dateien (`type:`, `id:`, `name:`, evtl. relations),")
    lines.append("dann `align_taxonomy.py` und `update_user_frontmatter.py` neu laufen lassen.")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Output: {OUT.relative_to(ROOT)}")
    print(f"Vorschläge: {suggestions_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
