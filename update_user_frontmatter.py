#!/usr/bin/env python3
"""
update_user_frontmatter.py — Reichert die existierenden User-Knoten-Dateien
in den Wurzelordnern (bauteil/, material/, methode/ etc.) mit Korpus-Daten an.

Pro User-Datei wird das YAML-Frontmatter ergänzt um:
  - aliases_korpus:           Roh-Werte aus Mapping-Tabellen, die zu diesem
                              Knoten gematched haben (max 25)
  - n_files:                  Anzahl Fallstudien, die diesen Knoten referenzieren
  - verwendet_in_fallstudien: Liste der Fallstudien-Wikilinks
                              ([[Gebäude/<file>]]-Format)

Vorhandene Frontmatter-Felder bleiben UNANGETASTET. Body wird nicht angefasst.
Backup aller geänderten Dateien in .backup_pre_align/ (mit Pfad-Spiegelung).

Vor Ausführung: Pipeline ist neu gelaufen (extract → align → match).
"""

from __future__ import annotations

import csv
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
EXTRACT = ROOT / "_extract"
BACKUP_DIR = ROOT / ".backup_pre_align"

# Entitätstyp → User-Wurzelordner
USER_FOLDERS = {
    "Bauteil": ["bauteil"],
    "Material": ["material"],
    "Methode": ["methode"],
    "Prozessphase": ["prozessphase"],
    "Aufbereitungsmethode": ["aufbereitungsmethode"],
    "Wirtschaft": ["wirtschaft"],
    "Leistungsanforderung": ["leistungsanforderung"],
    "Tragwerkssystem": ["tragwerkssystem"],
    "Verbindung": ["verbindung"],
    "Norm_Recht": ["norm", "recht"],
    "Pruefung": ["pruefung"],
    "Huerde": ["huerde"],
    "Abbruchmethode": ["abbruchmethode"],
    "Logistik": ["logistik"],
    "Kennwert": ["kennwert"],
    "Datenmodell": ["datenmodell"],
    "Schadstoff": ["schadstoff"],
    "Reuse_Strategie": ["reuse_strategie"],
}


def safe_yaml_quote(v: str) -> str:
    v = str(v).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{v}"'


def yaml_list(items: list[str]) -> str:
    return "[" + ", ".join(safe_yaml_quote(i) for i in items) + "]"


def split_frontmatter(text: str) -> tuple[str, str] | None:
    """Returns (frontmatter_inner, body) oder None wenn kein FM existiert."""
    if not text.startswith("---"):
        return None
    try:
        end_idx = text.index("\n---", 3)
    except ValueError:
        return None
    fm = text[4:end_idx]  # zwischen erstem --- und schließendem ---
    body = text[end_idx + 4:]  # ab Zeile nach schließendem ---
    if body.startswith("\n"):
        body = body[1:]
    return fm, body


def existing_fm_keys(fm: str) -> set[str]:
    """Sammelt vorhandene Top-Level-Keys (vor ':') in der Frontmatter."""
    keys: set[str] = set()
    for line in fm.splitlines():
        if not line or line.startswith(" ") or line.startswith("-"):
            continue
        m = re.match(r"^([A-Za-z_][\w\-]*)\s*:", line)
        if m:
            keys.add(m.group(1))
    return keys


def load_match_data(et: str) -> dict[str, dict]:
    """Returns {seed_node: {n_files, raw_values, files}} aus _extract/taxonomy_matched/<Type>.csv"""
    p = EXTRACT / "taxonomy_matched" / f"{et}.csv"
    out: dict[str, dict] = {}
    if not p.exists():
        return out
    for r in csv.DictReader(p.open(encoding="utf-8")):
        node = r["seed_node"]
        # raw_values: "wert1 (n=2); wert2 (n=1); ..."
        aliases = []
        for chunk in (r.get("raw_values") or "").split("; "):
            v = re.sub(r"\s*\(n=\d+\)\s*$", "", chunk).strip()
            if v and v not in aliases:
                aliases.append(v)
        out[node] = {
            "n_files": int(r.get("n_files") or 0),
            "aliases": aliases[:25],
        }
    return out


def load_links_per_node() -> dict[tuple[str, str], list[str]]:
    """Returns {(entity_type, seed_node): sorted list of fallstudie-files}."""
    p = EXTRACT / "taxonomy_matched" / "building_links.csv"
    out: dict[tuple[str, str], set[str]] = defaultdict(set)
    if not p.exists():
        return {}
    for r in csv.DictReader(p.open(encoding="utf-8")):
        out[(r["entity_type"], r["seed_node"])].add(r["file"])
    return {k: sorted(v) for k, v in out.items()}


def update_file(path: Path, et: str, match_data: dict[str, dict],
                links: dict[tuple[str, str], list[str]]) -> tuple[bool, str]:
    """Reichert einzelne User-Datei an. Returns (geändert, status_msg)."""
    node_id = path.stem
    info = match_data.get(node_id)
    file_links = links.get((et, node_id), [])

    if not info or info["n_files"] == 0:
        return False, "no-corpus-match"

    text = path.read_text(encoding="utf-8")
    parts = split_frontmatter(text)
    if parts is None:
        return False, "no-frontmatter"
    fm, body = parts

    existing = existing_fm_keys(fm)

    # Felder zum Ergänzen — nur wenn nicht vorhanden
    additions: list[str] = []
    if "n_files" not in existing:
        additions.append(f"n_files: {info['n_files']}")
    if "aliases_korpus" not in existing and info["aliases"]:
        additions.append(f"aliases_korpus: {yaml_list(info['aliases'])}")
    if "verwendet_in_fallstudien" not in existing and file_links:
        wikilinks = [f"[[Gebäude/{f.replace('.md', '')}]]" for f in file_links]
        additions.append(f"verwendet_in_fallstudien: {yaml_list(wikilinks)}")

    if not additions:
        return False, "already-enriched"

    # Backup
    rel = path.relative_to(ROOT)
    backup_path = BACKUP_DIR / rel
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    if not backup_path.exists():
        backup_path.write_text(text, encoding="utf-8")

    # Neu zusammensetzen: vorhandenes FM + neue Felder + body
    new_fm = fm.rstrip() + "\n" + "\n".join(additions)
    new_text = f"---\n{new_fm}\n---\n{body}"
    path.write_text(new_text, encoding="utf-8")
    return True, f"+{len(additions)} fields"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    BACKUP_DIR.mkdir(exist_ok=True)
    links = load_links_per_node()

    summary = []
    for et, folders in USER_FOLDERS.items():
        match_data = load_match_data(et)
        n_updated = 0
        n_skipped_no_match = 0
        n_skipped_no_fm = 0
        n_already = 0
        for folder_name in folders:
            folder = ROOT / folder_name
            if not folder.exists():
                continue
            for md in sorted(folder.glob("*.md")):
                if md.stem == "index":
                    continue
                changed, msg = update_file(md, et, match_data, links)
                if changed:
                    n_updated += 1
                elif msg == "no-corpus-match":
                    n_skipped_no_match += 1
                elif msg == "no-frontmatter":
                    n_skipped_no_fm += 1
                elif msg == "already-enriched":
                    n_already += 1
        summary.append((et, n_updated, n_skipped_no_match, n_skipped_no_fm, n_already))

    print(f"Backup-Verzeichnis: {BACKUP_DIR.relative_to(ROOT)}/")
    print()
    print(f"{'Typ':<22} {'Updated':>8} {'NoMatch':>8} {'NoFM':>5} {'Already':>8}")
    print("-" * 56)
    total_updated = 0
    for et, u, nm, nf, al in summary:
        total_updated += u
        print(f"{et:<22} {u:>8} {nm:>8} {nf:>5} {al:>8}")
    print("-" * 56)
    print(f"{'TOTAL':<22} {total_updated:>8}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
