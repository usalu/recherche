#!/usr/bin/env python3
"""
extract_entities.py — Extrahiert Entitäts-Wert-Paare aus den Fallstudien.

Quellen:
  - Gebäude/*.md   — neue Fallstudien mit Tabelle '## 2. ENTITÄTEN-MAPPING'
  - gebaeude/*.md  — ältere Fallstudien mit YAML-Frontmatter-Wikilinks
                     und 'Verknüpfungen'-Bullet-Liste

Ausgabe (nur in _extract/, Korpus bleibt unverändert):
  - all_pairs.csv               Roh-Paare: file, source_folder, entity_type, value
  - summary.csv                 Pro Typ: total_rows, unique_values
  - files_without_mapping.txt   Dateien ohne erkennbare Quelle
  - by_entity/<EntityType>.csv  Häufigkeitstabelle pro Typ (Schwelle ≥3 markiert)
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE_DIRS = [ROOT / "Gebäude", ROOT / "gebaeude"]
OUT_DIR = ROOT / "_extract"

# Meta-/Strukturdateien, keine Fallstudien
SKIP_FILES = {
    "01_FINAL_DATABASE_STRUCTURE.md",
    "Final_Database_Folder_Contents_and_File_Inventory.md",
    "Analyse_Entitaeten_Erweiterung_Gebaeude_Fallstudien.md",
    "gebäude4_wiederverwendung_direct_reuse_examples.md",
}

# Kanonische Schreibweisen für Entitätstypen.
# Ziel: 'People', 'Person', 'Akteur', 'Akteur-Rolle' kollabieren zu 'Akteur'.
TYPE_CANON = {
    "people": "Akteur",
    "person": "Akteur",
    "akteur": "Akteur",
    "akteur-rolle": "Akteur",
    "akteurrolle": "Akteur",
    "kennwert": "Kennwert",
    "kennwerte": "Kennwert",
    "norm/recht": "Norm_Recht",
    "norm": "Norm_Recht",
    "recht": "Norm_Recht",
    "norm_recht": "Norm_Recht",
    "bauteil": "Bauteil",
    "bauteile": "Bauteil",
    "material": "Material",
    "materialien": "Material",
    "reuse-strategie": "Reuse_Strategie",
    "reusestrategie": "Reuse_Strategie",
    "reuse strategie": "Reuse_Strategie",
    "wiederverwendung": "Reuse_Strategie",
    "methode": "Methode",
    "methoden": "Methode",
    "verbindung": "Verbindung",
    "verbindungen": "Verbindung",
    "fügung": "Verbindung",
    "fuegung": "Verbindung",
    "tragwerkssystem": "Tragwerkssystem",
    "tragwerk": "Tragwerkssystem",
    "hürde": "Huerde",
    "huerde": "Huerde",
    "hurde": "Huerde",
    "hindernis": "Huerde",
    "wirtschaft": "Wirtschaft",
    "ort": "Ort",
    "projekt": "Projekt",
    "fallstudie": "Fallstudie",
    "gebäude": "Gebaeude",
    "gebaeude": "Gebaeude",
    "prozessphase": "Prozessphase",
    "prozess": "Prozessphase",
    "logistik": "Logistik",
    "aufbereitungsmethode": "Aufbereitungsmethode",
    "aufbereitung": "Aufbereitungsmethode",
    "abbruchmethode": "Abbruchmethode",
    "abbruch": "Abbruchmethode",
    "rückbau": "Abbruchmethode",
    "rueckbau": "Abbruchmethode",
    "schadstoff": "Schadstoff",
    "schadstoffe": "Schadstoff",
    "werkzeug": "Werkzeug",
    "tool": "Werkzeug",
    "software": "Werkzeug",
    "förderprogramm": "Foerderprogramm",
    "foerderprogramm": "Foerderprogramm",
    "datenmodell": "Datenmodell",
    "materialpass": "Datenmodell",
    "dokument": "Dokument",
    "bauteilbörse": "Bauteilboerse",
    "bauteilboerse": "Bauteilboerse",
    "marktplatz": "Bauteilboerse",
    "leistungsanforderung": "Leistungsanforderung",
    "prüfung": "Pruefung",
    "pruefung": "Pruefung",
    "verwandt": "Gebaeude",  # frontmatter 'verwandt' linkt auf andere Gebäude
}


def normalize_entity_type(raw: str) -> str:
    key = raw.strip().lower()
    return TYPE_CANON.get(key, raw.strip())


def safe_filename(name: str) -> str:
    # Windows-verbotene Zeichen + Leerzeichen → Unterstrich
    return re.sub(r'[\\/<>:"|?*\s]+', "_", name).strip("_") or "Unbenannt"


def parse_mapping_table(text: str) -> list[tuple[str, str]]:
    """Parst die Tabelle nach '## 2. ENTITÄTEN-MAPPING' (Gebäude/*.md)."""
    m = re.search(r"##\s*2\.\s*ENTIT[ÄA]TEN[\s\-_]?MAPPING", text, re.IGNORECASE)
    if not m:
        return []
    after = text[m.end():]
    end = re.search(r"\n##\s+\d+\.", after)
    if end:
        after = after[: end.start()]

    rows: list[tuple[str, str]] = []
    for line in after.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        # Divider-Zeile (---|---|---)
        if all(re.fullmatch(r":?-+:?", c) or c == "" for c in cells):
            continue
        first = cells[0].lower()
        # Header-Zeile
        if first in {"entität", "entitat", "neue entität", "neue entitat", "entity"}:
            continue
        ent_type = cells[0]
        value = cells[1]
        if not ent_type or not value:
            continue
        rows.append((ent_type, value))
    return rows


def parse_frontmatter_wikilinks(text: str) -> list[tuple[str, str]]:
    """Parst YAML-Frontmatter und extrahiert [[typ/Name]]-Wikilinks (gebaeude/*.md)."""
    if not text.startswith("---"):
        return []
    try:
        end = text.index("\n---", 3)
    except ValueError:
        return []
    fm = text[3:end]

    rows: list[tuple[str, str]] = []
    for raw_line in fm.splitlines():
        line = raw_line.strip()
        # key: ["[[type/Name]]", "[[type/Name2]]"]   ODER   key: [[type/Name]]
        m = re.match(r"^([\w_äöüÄÖÜ]+)\s*:\s*(.+)$", line)
        if not m:
            continue
        key = m.group(1)
        rest = m.group(2)
        for link in re.findall(r"\[\[([^\]]+)\]\]", rest):
            if "/" in link:
                t, name = link.split("/", 1)
                rows.append((t, name))
            else:
                rows.append((key, link))
    return rows


def parse_verwandte_dateien(text: str) -> list[tuple[str, str]]:
    """Parst 'Verwandte Dateien'-Bullet in der Verknüpfungen-Sektion (gebaeude/*.md).

    Beispiel-Zeile:
      - **Verwandte Dateien:** `ort/Sulzerareal_Winterthur.md`; `material/ReUse_Stahl.md`; ...
    """
    m = re.search(r"\*\*Verwandte Dateien:\*\*(.+?)(?:\n\n|\n-\s\*\*|\Z)", text, re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    rows: list[tuple[str, str]] = []
    for ref in re.findall(r"`([\w/_\-äöüÄÖÜ\.]+)`", block):
        ref = ref.replace(".md", "")
        if "/" in ref:
            t, name = ref.split("/", 1)
            rows.append((t, name))
    return rows


def collect() -> tuple[list[tuple[str, str, str, str]], list[str]]:
    """Sammelt alle (file, folder, entity_type, value)-Paare und Dateien ohne Treffer."""
    all_pairs: list[tuple[str, str, str, str]] = []
    no_data: list[str] = []

    for folder in SOURCE_DIRS:
        if not folder.exists():
            print(f"warn: {folder} existiert nicht — übersprungen")
            continue
        for md in sorted(folder.glob("*.md")):
            if md.name in SKIP_FILES:
                continue
            text = md.read_text(encoding="utf-8")

            pairs = parse_mapping_table(text)
            if not pairs:
                pairs = parse_frontmatter_wikilinks(text) + parse_verwandte_dateien(text)
                # Frontmatter+Verwandte können doppelte Einträge liefern → dedupen pro Datei
                pairs = list(dict.fromkeys(pairs))

            if not pairs:
                no_data.append(str(md.relative_to(ROOT)))
                continue

            for et, val in pairs:
                all_pairs.append(
                    (md.name, folder.name, normalize_entity_type(et), val.strip())
                )
    return all_pairs, no_data


def write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main() -> int:
    # Windows-Konsole auf UTF-8 zwingen, damit Print mit Umlauten/≥ nicht crasht.
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "by_entity").mkdir(exist_ok=True)

    all_pairs, no_data = collect()

    # Roh-Paare
    write_csv(
        OUT_DIR / "all_pairs.csv",
        ["file", "source_folder", "entity_type", "value"],
        [list(p) for p in all_pairs],
    )

    # Aggregation
    by_value: dict[str, Counter] = defaultdict(Counter)
    by_value_files: dict[str, dict[str, set]] = defaultdict(lambda: defaultdict(set))
    for file, _folder, et, val in all_pairs:
        by_value[et][val] += 1
        by_value_files[et][val].add(file)

    # Pro Entitätstyp
    for et, counter in sorted(by_value.items()):
        rows = []
        for val, cnt in counter.most_common():
            files = sorted(by_value_files[et][val])
            schwelle = "JA" if len(files) >= 3 else ""
            rows.append([val, cnt, len(files), schwelle, "; ".join(files)])
        write_csv(
            OUT_DIR / "by_entity" / f"{safe_filename(et)}.csv",
            ["value", "count", "n_files", "knoten_kandidat_n>=3", "files"],
            rows,
        )

    # Summary
    summary_rows = []
    for et in sorted(by_value):
        total = sum(by_value[et].values())
        unique = len(by_value[et])
        kandidaten = sum(1 for v in by_value[et] if len(by_value_files[et][v]) >= 3)
        summary_rows.append([et, total, unique, kandidaten])
    write_csv(
        OUT_DIR / "summary.csv",
        ["entity_type", "total_rows", "unique_values", "knoten_kandidaten_n>=3"],
        summary_rows,
    )

    # Dateien ohne Mapping
    (OUT_DIR / "files_without_mapping.txt").write_text(
        "\n".join(no_data), encoding="utf-8"
    )

    # Konsolen-Report
    print(f"Quellordner:           {[str(p.relative_to(ROOT)) for p in SOURCE_DIRS]}")
    print(f"Verarbeitete Paare:    {len(all_pairs)}")
    print(f"Dateien ohne Treffer:  {len(no_data)}")
    print(f"Distinkte Typen:       {len(by_value)}")
    print(f"Output:                {OUT_DIR.relative_to(ROOT)}/")
    print()
    print(f"{'Typ':<24} {'Rows':>6} {'Unique':>7} {'>=3 Faelle':>11}")
    print("-" * 52)
    for et, total, unique, k in summary_rows:
        print(f"{et:<24} {total:>6} {unique:>7} {k:>11}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
