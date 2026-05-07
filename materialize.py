#!/usr/bin/env python3
"""
materialize.py — Erzeugt alle Knoten als Tolaria-konforme .md-Dateien
in reuse_database/. Baut die finale Ordnerstruktur nach Inventory:

  reuse_database/
    01_Fallstudie/        87 Fallstudien mit vollem beziehungen-Frontmatter
    03_Gebaeude/          ~85 Gebäude (open-vocab, Donor + Empfänger)
    04_Ort/               ~67 Orte
    05_Akteur/            ~328 Akteure (mit Rollen-Annotation)
    06_Bauteiltyp/        ~34 controlled Bauteil-Knoten
    07_Bauteilposition/   175 derived (Fallstudie × Bauteiltyp)
    08_Material/          ~23 Material-Knoten
    09_ReuseStrategie/    10 Strategien
    10_ReuseKette/        70 Donor → Empfänger Flows
    11..32                Methode, Prüfung, Hürde, ... (alle controlled)
    27_Quelle/            191 Quellen
    33_Quellenkonflikt/   17 dokumentierte Konflikte
    34_Offene_Frage/      86 Datenlücken

Inputs (alle aus _extract/):
  - all_pairs.csv
  - taxonomy_matched/<Type>.csv         (controlled-vocab Knoten)
  - taxonomy_matched/building_links.csv (Fallstudie ↔ Knoten)
  - name_clusters/<Type>.csv            (open-vocab Cluster)
  - derived/*.csv                       (Bauteilposition etc.)
  - derived/building_yaml_full/*.yaml   (Fallstudie-Frontmatter)
  - taxonomy.json                       (Definitionen)

Output: reuse_database/<NN_Type>/<id>.md
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
EXTRACT = ROOT / "_extract"
OUT = ROOT / "reuse_database"
TAXONOMY = ROOT / "taxonomy.json"

# Inventory-Ordnernamen pro Typ
FOLDER_MAP = {
    "Fallstudie": "01_Fallstudie",
    "Projekt": "02_Projekt",
    "Gebaeude": "03_Gebaeude",
    "Ort": "04_Ort",
    "Akteur": "05_Akteur",
    "Bauteil": "06_Bauteiltyp",
    "Bauteilposition": "07_Bauteilposition",
    "Material": "08_Material",
    "Reuse_Strategie": "09_ReuseStrategie",
    "ReuseKette": "10_ReuseKette",
    "Prozessphase": "11_Prozessphase",
    "Methode": "12_Methode",
    "Abbruchmethode": "13_Abbruchmethode",
    "Aufbereitungsmethode": "14_Aufbereitungsmethode",
    "Pruefung": "15_Pruefung",
    "Leistungsanforderung": "16_Leistungsanforderung",
    "Tragwerkssystem": "17_Tragwerkssystem",
    "Verbindung": "18_Verbindung",
    "Norm_Recht": "19_Norm_Recht",
    "Huerde": "20_Huerde",
    "Logistik": "21_Logistik",
    "Wirtschaft": "22_Wirtschaft",
    "Kennwert": "23_Kennwertdefinition",
    "Datenpunkt": "24_Datenpunkt",
    "Datenmodell": "25_Datenmodell",
    "Dokument": "26_Dokument",
    "Quelle": "27_Quelle",
    "Werkzeug": "28_Tool_Software",
    "Bauteilboerse": "29_Bauteilboerse",
    "Foerderprogramm": "30_Foerderprogramm",
    "Schadstoff": "31_Schadstoff",
    "Quellenkonflikt": "33_Quellenkonflikt",
    "Offene_Frage": "34_Offene_Frage",
    "Bericht": "26_Dokument",
}


def safe_filename(s: str, max_len: int = 100) -> str:
    s = re.sub(r'[\\/<>:"|?*\n\r\t]+', "_", s).strip("_. ")
    return (s[:max_len] or "Unbenannt") + ".md"


def yaml_escape(s: str) -> str:
    """Einfaches YAML-Quoting für String-Werte."""
    s = str(s).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def write_md(folder: Path, filename: str, frontmatter: dict, title: str,
             body: str = "") -> None:
    folder.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    for k, v in frontmatter.items():
        if v is None or v == "" or v == [] or v == {}:
            continue
        if isinstance(v, list):
            if all(isinstance(x, str) for x in v):
                escaped = ", ".join(yaml_escape(x) for x in v)
                lines.append(f"{k}: [{escaped}]")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
        elif isinstance(v, dict):
            lines.append(f"{k}:")
            for ik, iv in v.items():
                if isinstance(iv, list):
                    escaped = ", ".join(yaml_escape(x) for x in iv)
                    lines.append(f"  {ik}: [{escaped}]")
                else:
                    lines.append(f"  {ik}: {yaml_escape(iv)}")
        elif isinstance(v, (int, float, bool)):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f"{k}: {yaml_escape(v)}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    if body:
        lines.append("")
        lines.append(body)
    (folder / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")


def folder_for(et: str) -> Path:
    return OUT / FOLDER_MAP.get(et, et)


# === Loaders ===

def load_taxonomy() -> dict:
    return json.loads(TAXONOMY.read_text(encoding="utf-8"))


def load_controlled_nodes(et: str) -> list[dict]:
    """Aus _extract/taxonomy_matched/<Type>.csv die Match-Daten."""
    p = EXTRACT / "taxonomy_matched" / f"{et}.csv"
    if not p.exists():
        return []
    return list(csv.DictReader(p.open(encoding="utf-8")))


def load_open_clusters(et: str) -> list[dict]:
    p = EXTRACT / "name_clusters" / f"{et}.csv"
    if not p.exists():
        return []
    return list(csv.DictReader(p.open(encoding="utf-8")))


def load_derived(name: str) -> list[dict]:
    p = EXTRACT / "derived" / f"{name}.csv"
    if not p.exists():
        return []
    return list(csv.DictReader(p.open(encoding="utf-8")))


def load_full_yaml(filename: str) -> str:
    p = EXTRACT / "derived" / "building_yaml_full" / filename
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


# === Writers ===

def write_controlled(taxonomy: dict, et: str) -> int:
    """Schreibt einen Knoten pro controlled-vocab-Eintrag."""
    if et not in taxonomy:
        return 0
    matched = {r["seed_node"]: r for r in load_controlled_nodes(et)}
    folder = folder_for(et)
    count = 0
    for nid, ndata in taxonomy[et].items():
        if nid.startswith("_"):
            continue
        m = matched.get(nid, {})
        files = m.get("files", "")
        fallstudien_links = []
        if files:
            for f in files.split("; "):
                f = f.strip()
                if f.endswith(".md"):
                    fallstudien_links.append(f"[[01_Fallstudie/{f.replace('.md', '')}]]")
        # Aliase aus den Roh-Werten extrahieren
        aliases = []
        raw = m.get("raw_values", "")
        if raw:
            for chunk in raw.split("; "):
                # "<wert> (n=N)"
                w = re.sub(r"\s*\(n=\d+\)\s*$", "", chunk).strip()
                if w and w not in aliases:
                    aliases.append(w)
        fm = {
            "type": et,
            "name": nid,
            "kategorie": ndata.get("kategorie", ""),
            "definition": ndata.get("definition", ""),
            "keywords": ndata.get("keywords", []),
            "aliases_korpus": aliases[:20],
            "n_files": int(m.get("n_files", 0)) if m else 0,
            "verwendet_in_fallstudien": fallstudien_links,
        }
        write_md(folder, safe_filename(nid), fm, nid)
        count += 1
    return count


def write_open_vocab(et: str) -> int:
    """Schreibt einen Knoten pro Cluster (Akteur, Ort, Projekt, Gebaeude, …)."""
    clusters = load_open_clusters(et)
    folder = folder_for(et)
    count = 0
    for r in clusters:
        node_id = r.get("node_id", "")
        if not node_id:
            continue
        canonical = r.get("canonical_name", node_id)
        variants = [v.strip() for v in r.get("variants", "").split("; ") if v.strip()]
        # Files mappen auf Fallstudie-Wikilinks
        files = [f.strip() for f in r.get("files", "").split("; ") if f.strip()]
        fallstudien_links = [f"[[01_Fallstudie/{f.replace('.md', '')}]]"
                             for f in files]
        fm = {
            "type": et,
            "name": canonical,
            "aliases": variants,
            "n_files": int(r.get("n_files", 0)),
            "verwendet_in_fallstudien": fallstudien_links,
        }
        if et == "Akteur":
            roles = [s.strip() for s in r.get("rollen", "").split("; ") if s.strip()]
            if roles:
                fm["rollen"] = roles
        write_md(folder, safe_filename(node_id), fm, canonical)
        count += 1
    return count


def rewrite_wikilinks(text: str) -> str:
    """Ersetzt [[bauteil/X]] → [[06_Bauteiltyp/X]] etc. (lowercase → Inventory-Ordner)."""
    mapping = {
        "bauteil": "06_Bauteiltyp",
        "material": "08_Material",
        "methode": "12_Methode",
        "huerde": "20_Huerde",
        "kennwert": "23_Kennwertdefinition",
        "akteur": "05_Akteur",
        "ort": "04_Ort",
        "projekt": "02_Projekt",
        "gebaeude": "03_Gebaeude",
        "fallstudie": "01_Fallstudie",
        "reuse_strategie": "09_ReuseStrategie",
        "tragwerkssystem": "17_Tragwerkssystem",
        "pruefung": "15_Pruefung",
        "aufbereitungsmethode": "14_Aufbereitungsmethode",
        "abbruchmethode": "13_Abbruchmethode",
        "norm_recht": "19_Norm_Recht",
        "verbindung": "18_Verbindung",
        "logistik": "21_Logistik",
        "wirtschaft": "22_Wirtschaft",
        "leistungsanforderung": "16_Leistungsanforderung",
        "schadstoff": "31_Schadstoff",
        "prozessphase": "11_Prozessphase",
        "datenmodell": "25_Datenmodell",
        "werkzeug": "28_Tool_Software",
        "foerderprogramm": "30_Foerderprogramm",
        "bauteilboerse": "29_Bauteilboerse",
        "bericht": "26_Dokument",
        "bauteilposition": "07_Bauteilposition",
        "reusekette": "10_ReuseKette",
        "datenpunkt": "24_Datenpunkt",
        "quelle": "27_Quelle",
        "quellenkonflikt": "33_Quellenkonflikt",
        "offene_frage": "34_Offene_Frage",
    }

    def replace(m: re.Match) -> str:
        prefix, rest = m.group(1), m.group(2)
        if prefix.lower() in mapping:
            return f"[[{mapping[prefix.lower()]}/{rest}]]"
        return m.group(0)

    return re.sub(r"\[\[([^/\]]+)/([^\]]+)\]\]", replace, text)


def write_fallstudien(taxonomy: dict) -> int:
    """Pro Fallstudie eine .md mit kompletter beziehungen-Frontmatter."""
    yaml_dir = EXTRACT / "derived" / "building_yaml_full"
    folder = folder_for("Fallstudie")
    if not yaml_dir.exists():
        return 0
    count = 0
    for yaml_file in sorted(yaml_dir.glob("*.yaml")):
        content = yaml_file.read_text(encoding="utf-8")
        # Wikilinks von 'bauteil/...' auf '06_Bauteiltyp/...' umschreiben
        content = rewrite_wikilinks(content)
        # Strip "beziehungen:" prefix; we'll wrap in proper frontmatter
        if content.startswith("beziehungen:"):
            beziehungen_block = content[len("beziehungen:"):].lstrip("\n").rstrip()
        else:
            beziehungen_block = content.rstrip()
        fallstudie = yaml_file.stem
        # Build frontmatter manually since beziehungen has nested structure
        lines = [
            "---",
            f"type: Fallstudie",
            f"name: {yaml_escape(fallstudie)}",
            "beziehungen:",
        ]
        # beziehungen_block already has 2-space indented entries
        lines.append(beziehungen_block)
        lines.append("---")
        lines.append("")
        lines.append(f"# {fallstudie}")
        lines.append("")
        lines.append("## Original-Quelle")
        lines.append("")
        # Look up in original Gebäude/ folders
        original_paths = [
            ROOT / "Gebäude" / f"{fallstudie}.md",
            ROOT / "gebaeude" / f"{fallstudie}.md",
        ]
        for op in original_paths:
            if op.exists():
                rel = op.relative_to(ROOT).as_posix()
                lines.append(f"- Originaldatei: `{rel}`")
                break
        out = folder / safe_filename(fallstudie)
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        count += 1
    return count


def write_bauteilposition() -> int:
    items = load_derived("bauteilposition")
    folder = folder_for("Bauteilposition")
    for r in items:
        materialien = [m.strip() for m in r.get("materialien", "").split("; ") if m.strip()]
        donors = [d.strip() for d in r.get("donor_gebaeude", "").split("; ") if d.strip()]
        fallstudie = r.get("fallstudie", "")
        bauteiltyp = r.get("bauteiltyp", "")
        fm = {
            "type": "Bauteilposition",
            "name": r["id"],
            "fallstudie": [f"[[01_Fallstudie/{fallstudie}]]"] if fallstudie else [],
            "bauteiltyp": [f"[[06_Bauteiltyp/{bauteiltyp}]]"] if bauteiltyp else [],
            "material": [f"[[08_Material/{m}]]" for m in materialien],
            "donor_gebaeude": [f"[[03_Gebaeude/{d}]]" for d in donors],
        }
        write_md(folder, safe_filename(r["id"]), fm, r["id"])
    return len(items)


def write_reusekette() -> int:
    items = load_derived("reusekette")
    folder = folder_for("ReuseKette")
    for r in items:
        donor = r.get("donor", "")
        empfaenger = r.get("empfaenger_fallstudie", "")
        material = r.get("material", "")
        bauteile = [b.strip() for b in r.get("bauteile", "").split("; ") if b.strip()]
        fm = {
            "type": "ReuseKette",
            "name": r["id"],
            "donor_gebaeude": [f"[[03_Gebaeude/{donor}]]"] if donor else [],
            "empfaenger_fallstudie": [f"[[01_Fallstudie/{empfaenger}]]"] if empfaenger else [],
            "material": [f"[[08_Material/{material}]]"] if material else [],
            "bauteiltyp": [f"[[06_Bauteiltyp/{b}]]" for b in bauteile],
        }
        write_md(folder, safe_filename(r["id"]), fm, r["id"])
    return len(items)


def write_datenpunkt() -> int:
    items = load_derived("datenpunkt")
    folder = folder_for("Datenpunkt")
    for r in items:
        fm = {
            "type": "Datenpunkt",
            "name": r["id"],
            "fallstudie": [f"[[01_Fallstudie/{r.get('fallstudie', '')}]]"],
            "kennwertdefinition": [f"[[23_Kennwertdefinition/{r.get('kennwertdefinition', '')}]]"],
            "wert": float(r["wert"]) if r.get("wert") else 0,
            "einheit": r.get("einheit", ""),
            "raw_kontext": r.get("raw_kontext", "")[:200],
        }
        write_md(folder, safe_filename(r["id"]), fm, r["id"])
    return len(items)


def write_quelle() -> int:
    items = load_derived("quelle")
    folder = folder_for("Quelle")
    for r in items:
        fm = {
            "type": "Quelle",
            "name": r.get("label", "")[:120] or r.get("id", ""),
            "fallstudie": [f"[[01_Fallstudie/{r.get('fallstudie', '')}]]"],
            "url": r.get("url", ""),
        }
        write_md(folder, safe_filename(r["id"]), fm, r.get("label", "Quelle")[:120])
    return len(items)


def write_quellenkonflikt() -> int:
    items = load_derived("quellenkonflikt")
    folder = folder_for("Quellenkonflikt")
    for r in items:
        werte = [v.strip() for v in r.get("werte", "").split("; ") if v.strip()]
        dps = [d.strip() for d in r.get("datenpunkte", "").split("; ") if d.strip()]
        fm = {
            "type": "Quellenkonflikt",
            "name": r["id"],
            "fallstudie": [f"[[01_Fallstudie/{r.get('fallstudie', '')}]]"],
            "kennwertdefinition": [f"[[23_Kennwertdefinition/{r.get('kennwertdefinition', '')}]]"],
            "einheit": r.get("einheit", ""),
            "divergierende_werte": werte,
            "datenpunkte": [f"[[24_Datenpunkt/{d}]]" for d in dps],
        }
        write_md(folder, safe_filename(r["id"]), fm, r["id"])
    return len(items)


def write_offene_frage() -> int:
    items = load_derived("offene_frage")
    folder = folder_for("Offene_Frage")
    seen: set[str] = set()
    count = 0
    for r in items:
        key = r["id"]
        if key in seen:
            continue
        seen.add(key)
        fm = {
            "type": "Offene_Frage",
            "name": r["id"],
            "fallstudie": [f"[[01_Fallstudie/{r.get('fallstudie', '')}]]"],
            "betroffener_typ": r.get("entity_type", ""),
            "frage": r.get("frage", ""),
        }
        write_md(folder, safe_filename(r["id"]), fm, r["id"])
        count += 1
    return count


# === Main ===

def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    OUT.mkdir(exist_ok=True)
    taxonomy = load_taxonomy()

    counts: dict[str, int] = {}

    # Controlled vocab — alle 18 Typen
    for et in ("Bauteil", "Material", "Reuse_Strategie", "Methode",
               "Tragwerkssystem", "Verbindung", "Pruefung", "Aufbereitungsmethode",
               "Abbruchmethode", "Logistik", "Wirtschaft", "Leistungsanforderung",
               "Schadstoff", "Prozessphase", "Norm_Recht", "Datenmodell",
               "Kennwert", "Huerde"):
        counts[et] = write_controlled(taxonomy, et)

    # Open vocab — alle 9 Typen
    for et in ("Akteur", "Ort", "Projekt", "Gebaeude", "Fallstudie",
               "Foerderprogramm", "Bauteilboerse", "Werkzeug", "Bericht"):
        n = write_open_vocab(et)
        counts[et] = counts.get(et, 0) + n

    # Fallstudien (überschreibt das open-vocab Fallstudie mit vollem YAML)
    counts["Fallstudie_full"] = write_fallstudien(taxonomy)

    # Derived
    counts["Bauteilposition"] = write_bauteilposition()
    counts["ReuseKette"] = write_reusekette()
    counts["Datenpunkt"] = write_datenpunkt()
    counts["Quelle"] = write_quelle()
    counts["Quellenkonflikt"] = write_quellenkonflikt()
    counts["Offene_Frage"] = write_offene_frage()

    print(f"Output: {OUT.relative_to(ROOT)}/")
    print()
    print(f"{'Typ':<24} {'Dateien':>8}")
    print("-" * 36)
    total = 0
    for k, v in sorted(counts.items()):
        print(f"{k:<24} {v:>8}")
        total += v
    print("-" * 36)
    print(f"{'TOTAL':<24} {total:>8}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
