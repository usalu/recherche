#!/usr/bin/env python3
"""
materialize_derived.py — Schreibt die 6 derived-Entitätstypen als neue Wurzelordner.

Output (im Projekt-Root):
  bauteilposition/    175 Bauteilpositionen (Fallstudie × Bauteiltyp)
  reusekette/         70 Donor → Empfänger Flows
  datenpunkt/         170 Datenpunkte mit Kennwert-Routing
  quelle/             108 Quellen (URL-dedupliziert über Fallstudien)
  quellenkonflikt/    13 echte Quellenkonflikte (spread ≤ 30×)
  offene_frage/       86 Datenlücken pro Fallstudie+Typ

Wikilink-Konvention: User-Format `[[ordner/Name]]` (lowercase, ohne Nummerierung).
Frontmatter wie bei den Wurzelordnern: `type:` + Relations als Wikilink-Listen.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
EXTRACT = ROOT / "_extract"
DERIVED = EXTRACT / "derived"

# Entitätstyp → Ziel-Ordnername (lowercase, User-Konvention)
DERIVED_FOLDERS = {
    "Bauteilposition": "bauteilposition",
    "ReuseKette": "reusekette",
    "Datenpunkt": "datenpunkt",
    "Quelle": "quelle",
    "Quellenkonflikt": "quellenkonflikt",
    "Offene_Frage": "offene_frage",
}


def safe_filename(s: str, max_len: int = 100) -> str:
    s = re.sub(r'[\\/<>:"|?*\n\r\t]+', "_", s).strip("_. ")
    return (s[:max_len] or "Unbenannt") + ".md"


def yaml_quote(s) -> str:
    s = str(s).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def yaml_list_str(items: list[str]) -> str:
    return "[" + ", ".join(yaml_quote(i) for i in items) + "]"


def write_md(folder: Path, filename: str, frontmatter: dict, title: str = "") -> None:
    folder.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    for k, v in frontmatter.items():
        if v is None or v == "" or v == [] or v == {}:
            continue
        if isinstance(v, list):
            if all(isinstance(x, str) for x in v):
                lines.append(f"{k}: {yaml_list_str(v)}")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
        elif isinstance(v, (int, float, bool)):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f"{k}: {yaml_quote(v)}")
    lines.append("---")
    if title:
        lines.append("")
        lines.append(f"# {title}")
    (folder / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_csv(name: str) -> list[dict]:
    p = DERIVED / name
    return list(csv.DictReader(p.open(encoding="utf-8"))) if p.exists() else []


def materialize_bauteilposition() -> int:
    folder = ROOT / DERIVED_FOLDERS["Bauteilposition"]
    items = load_csv("bauteilposition.csv")
    for r in items:
        materialien = [m.strip() for m in r.get("materialien", "").split("; ") if m.strip()]
        donors = [d.strip() for d in r.get("donor_gebaeude", "").split("; ") if d.strip()]
        fm = {
            "type": "Bauteilposition",
            "name": r["id"],
            "fallstudie": [f"[[Gebäude/{r['fallstudie']}]]"],
            "bauteil": [f"[[bauteil/{r['bauteiltyp']}]]"],
            "material": [f"[[material/{m}]]" for m in materialien],
            "donor_gebaeude": [f"[[Gebäude/{d}]]" for d in donors],
        }
        write_md(folder, safe_filename(r["id"]), fm, r["id"])
    return len(items)


def materialize_reusekette() -> int:
    folder = ROOT / DERIVED_FOLDERS["ReuseKette"]
    items = load_csv("reusekette.csv")
    for r in items:
        bauteile = [b.strip() for b in r.get("bauteile", "").split("; ") if b.strip()]
        materialien = [m.strip() for m in r.get("alle_materialien", "").split("; ") if m.strip()]
        fm = {
            "type": "ReuseKette",
            "name": r["id"],
            "donor_gebaeude": [f"[[Gebäude/{r['donor']}]]"] if r.get("donor") else [],
            "empfaenger_fallstudie": [f"[[Gebäude/{r['empfaenger_fallstudie']}]]"],
            "material_primary": [f"[[material/{r['material']}]]"] if r.get("material") and r['material'] != 'unspecified' else [],
            "bauteil": [f"[[bauteil/{b}]]" for b in bauteile],
            "alle_materialien": [f"[[material/{m}]]" for m in materialien],
        }
        write_md(folder, safe_filename(r["id"]), fm, r["id"])
    return len(items)


def materialize_datenpunkt() -> int:
    folder = ROOT / DERIVED_FOLDERS["Datenpunkt"]
    items = load_csv("datenpunkt.csv")
    for r in items:
        fm = {
            "type": "Datenpunkt",
            "name": r["id"],
            "fallstudie": [f"[[Gebäude/{r['fallstudie']}]]"],
            "kennwert": [f"[[kennwert/{r['kennwertdefinition']}]]"],
            "wert": float(r["wert"]) if r.get("wert") else 0,
            "einheit": r.get("einheit", ""),
            "raw_kontext": (r.get("raw_kontext") or "")[:200],
        }
        write_md(folder, safe_filename(r["id"]), fm, r["id"])
    return len(items)


def materialize_quelle() -> int:
    folder = ROOT / DERIVED_FOLDERS["Quelle"]
    items = load_csv("quelle.csv")
    for r in items:
        fallstudien = [f.strip() for f in r.get("fallstudien", "").split("; ") if f.strip()]
        fm = {
            "type": "Quelle",
            "name": r.get("label", "")[:120] or r.get("id", ""),
            "url": r.get("url", ""),
            "verwendet_in_fallstudien": [f"[[Gebäude/{f}]]" for f in fallstudien],
            "n_fallstudien": int(r.get("n_fallstudien") or len(fallstudien)),
        }
        write_md(folder, safe_filename(r["id"]), fm, r.get("label", "Quelle")[:120])
    return len(items)


def materialize_quellenkonflikt() -> int:
    folder = ROOT / DERIVED_FOLDERS["Quellenkonflikt"]
    items = load_csv("quellenkonflikt.csv")
    for r in items:
        werte = [v.strip() for v in r.get("werte", "").split("; ") if v.strip()]
        dps = [d.strip() for d in r.get("datenpunkte", "").split("; ") if d.strip()]
        fm = {
            "type": "Quellenkonflikt",
            "name": r["id"],
            "fallstudie": [f"[[Gebäude/{r['fallstudie']}]]"],
            "kennwert": [f"[[kennwert/{r['kennwertdefinition']}]]"],
            "einheit": r.get("einheit", ""),
            "divergierende_werte": werte,
            "spread_faktor": float(r.get("spread", 0)),
            "datenpunkt": [f"[[datenpunkt/{d}]]" for d in dps],
        }
        write_md(folder, safe_filename(r["id"]), fm, r["id"])
    return len(items)


def materialize_offene_frage() -> int:
    folder = ROOT / DERIVED_FOLDERS["Offene_Frage"]
    items = load_csv("offene_frage.csv")
    seen: set[str] = set()
    count = 0
    for r in items:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        fm = {
            "type": "Offene_Frage",
            "name": r["id"],
            "fallstudie": [f"[[Gebäude/{r['fallstudie']}]]"],
            "betroffener_typ": r.get("entity_type", ""),
            "frage": r.get("frage", ""),
        }
        write_md(folder, safe_filename(r["id"]), fm, r["id"])
        count += 1
    return count


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    counts = {
        "bauteilposition": materialize_bauteilposition(),
        "reusekette": materialize_reusekette(),
        "datenpunkt": materialize_datenpunkt(),
        "quelle": materialize_quelle(),
        "quellenkonflikt": materialize_quellenkonflikt(),
        "offene_frage": materialize_offene_frage(),
    }
    print(f"{'Ordner':<22} {'Files':>6}")
    print("-" * 30)
    total = 0
    for folder, n in counts.items():
        print(f"{folder:<22} {n:>6}")
        total += n
    print("-" * 30)
    print(f"{'TOTAL':<22} {total:>6}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
