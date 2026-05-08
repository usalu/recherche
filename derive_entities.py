#!/usr/bin/env python3
"""
derive_entities.py — Generiert die 6 abgeleiteten Entitätstypen aus existierenden
Daten (Mapping-Tabellen, Match-Output, Name-Cluster, Quellen-Sektionen):

  - Bauteilposition  (Tupel Fallstudie × Bauteiltyp × Material × Donor)
  - ReuseKette       (Donor → Empfänger Flow)
  - Datenpunkt       (Zahl + Einheit + Kennwertdefinition + Quelle)
  - Quelle           (URL/Beleg aus '## Quellen'-Sektion)
  - Quellenkonflikt  (mehrere Datenpunkte zum gleichen Kennwert mit divergierenden Werten)
  - Offene_Frage     (jede 'unbekannt'-Stelle als eigener Knoten)

Inputs:
  _extract/all_pairs.csv
  _extract/taxonomy_matched/building_links.csv
  _extract/name_clusters/Gebaeude.csv  (etc.)
  Gebäude/*.md, gebaeude/*.md          (für '## Quellen'-Parsing)

Outputs in _extract/derived/:
  - bauteilposition.csv, reusekette.csv, datenpunkt.csv,
    quelle.csv, quellenkonflikt.csv, offene_frage.csv
  - building_yaml_full/<file>.yaml  (komplette Frontmatter inkl. derived)
"""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
EXTRACT = ROOT / "_extract"
OUT_DIR = EXTRACT / "derived"
GEBAEUDE_DIRS = [ROOT / "Gebäude", ROOT / "gebaeude"]

SKIP_FILES = {
    "01_FINAL_DATABASE_STRUCTURE.md",
    "Final_Database_Folder_Contents_and_File_Inventory.md",
    "Analyse_Entitaeten_Erweiterung_Gebaeude_Fallstudien.md",
    "gebäude4_wiederverwendung_direct_reuse_examples.md",
    "Elementa.md",
    "index.md",
    "gebäude_wiederverwendung_direct_reuse_examples.md",
    "gebäude2_wiederverwendung_direct_reuse_examples.md",
    "gebäude3_wiederverwendung_direct_reuse_examples.md",
}


def normalize(s: str) -> str:
    s = s.lower()
    s = (s.replace("ä", "ae").replace("ö", "oe")
          .replace("ü", "ue").replace("ß", "ss")
          # Superscript- und Subscript-Ziffern (CO₂, m², m³, H₂O)
          .replace("²", "2").replace("³", "3")
          .replace("₂", "2").replace("₃", "3").replace("₄", "4"))
    return s


def safe_id(s: str, max_len: int = 60) -> str:
    s = re.sub(r"[^A-Za-z0-9_]+", "_", s).strip("_")
    return s[:max_len] or "Unbenannt"


def slugify(s: str) -> str:
    n = normalize(s)
    parts = [p.capitalize() for p in re.split(r"[^a-z0-9]+", n) if p]
    return "_".join(parts) or "Unbenannt"


# Wörter, die signalisieren: dieses Gebäude ist der Bestand des Empfängers, kein Donor
BESTAND_KEYWORDS = {
    "bestand", "bestandsbau", "bestehend", "bestehende", "bestehender",
    "vorhanden", "vorhandene", "existing", "bestandsgebaeude", "bestandshalle",
}
# Token-Stopwords für Jaccard-Vergleich Gebäude↔Fallstudie
NAME_OVERLAP_STOPS = {
    "the", "der", "die", "das", "und", "of", "and", "for", "von",
    "haus", "house", "building", "gebaeude", "ag", "gmbh",
}


def is_bestand_marker(g: str) -> bool:
    s = normalize(g)
    return any(kw in s for kw in BESTAND_KEYWORDS)


def name_token_overlap(a: str, b: str) -> float:
    """Jaccard-Ähnlichkeit zweier Namen über sinnvolle Tokens."""
    ta = {t for t in re.split(r"[^a-z0-9]+", normalize(a))
          if len(t) >= 3 and t not in NAME_OVERLAP_STOPS}
    tb = {t for t in re.split(r"[^a-z0-9]+", normalize(b))
          if len(t) >= 3 and t not in NAME_OVERLAP_STOPS}
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def is_likely_donor(gebaeude_name: str, fallstudie_id: str) -> bool:
    """True wenn Gebäude wahrscheinlich Donor ist (nicht Empfänger/Bestand)."""
    if is_bestand_marker(gebaeude_name):
        return False
    if name_token_overlap(gebaeude_name, fallstudie_id) >= 0.20:
        return False
    return True


# === Loaders ===

def load_pairs() -> list[dict]:
    return list(csv.DictReader((EXTRACT / "all_pairs.csv").open(encoding="utf-8")))


def load_controlled_links() -> dict[str, dict[str, set[str]]]:
    p = EXTRACT / "taxonomy_matched" / "building_links.csv"
    out: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for r in csv.DictReader(p.open(encoding="utf-8")):
        out[r["file"]][r["entity_type"]].add(r["seed_node"])
    return out


def load_name_canonicals(et: str) -> dict[str, str]:
    """Returns variant → canonical map."""
    p = EXTRACT / "name_clusters" / f"{et}.csv"
    if not p.exists():
        return {}
    out = {}
    for r in csv.DictReader(p.open(encoding="utf-8")):
        canonical = r["canonical_name"]
        out[canonical] = canonical
        for v in r["variants"].split("; "):
            out[v.strip()] = canonical
    return out


# === 1. Bauteilposition ===

def derive_bauteilposition(file_controlled, all_pairs, gebaeude_canon):
    """Per Fallstudie × Bauteiltyp eine Bauteilposition."""
    # Sammle pro File alle Gebäude-Werte (Donor-Kandidaten)
    gebaeude_per_file = defaultdict(set)
    for r in all_pairs:
        if r["entity_type"] in ("Gebaeude", "Spendergebaeude"):
            v = r["value"]
            canonical = gebaeude_canon.get(v, v)
            gebaeude_per_file[r["file"]].add(canonical)

    items = []
    for file, etmap in file_controlled.items():
        bauteile = sorted(etmap.get("Bauteil", set()))
        materialien = sorted(etmap.get("Material", set()))
        fallstudie = file.replace(".md", "")
        all_gebs = gebaeude_per_file.get(file, set())
        donors = sorted(g for g in all_gebs if is_likely_donor(g, fallstudie))
        for bauteil in bauteile:
            items.append({
                "id": f"{fallstudie}__{bauteil}",
                "fallstudie": fallstudie,
                "bauteiltyp": bauteil,
                "materialien": materialien,
                "donor_gebaeude": donors,
                "n_materialien": len(materialien),
                "n_donors": len(donors),
            })
    return items


# === 2. ReuseKette ===

def derive_reusekette(file_controlled, all_pairs, gebaeude_canon):
    """Per (Donor, Empfänger, Material) eine Reuse-Kette."""
    gebaeude_per_file = defaultdict(set)
    for r in all_pairs:
        if r["entity_type"] in ("Gebaeude", "Spendergebaeude"):
            v = r["value"]
            canonical = gebaeude_canon.get(v, v)
            gebaeude_per_file[r["file"]].add(canonical)

    items = []
    for file, etmap in file_controlled.items():
        materialien = sorted(etmap.get("Material", set()))
        bauteile = sorted(etmap.get("Bauteil", set()))
        fallstudie = file.replace(".md", "")
        donors = [g for g in gebaeude_per_file.get(file, set())
                  if is_likely_donor(g, fallstudie)]
        if not donors:
            continue
        primary_material = materialien[0] if materialien else "unspecified"
        for donor in donors:
            kette_id = f"{slugify(donor)}__to__{fallstudie}__{primary_material}"
            items.append({
                "id": kette_id[:120],
                "donor": donor,
                "empfaenger_fallstudie": fallstudie,
                "material": primary_material,
                "bauteile": bauteile,
                "alle_materialien": materialien,
            })
    return items


# === 3. Datenpunkt ===

NUMBER_UNIT_RE = re.compile(
    r"(?P<num>\d+(?:[.,]\d+)*)\s*"
    r"(?P<unit>%|t\b|kg|m2|m3|km|m\b|jahre|years|monate|months|stk|stueck|"
    r"eur|euro|chf|gbp|pfund|kwh|kgco2e?)",
    re.IGNORECASE,
)


def parse_number(s: str) -> float | None:
    """Parst Zahl mit deutschen oder englischen Trennzeichen.

    Heuristik: Wenn Punkt von genau 3 Ziffern gefolgt wird (und keine andere
    Dezimalstelle existiert), wird als Tausendertrenner interpretiert.
      '3.404'   → 3404      (Tausender)
      '165.000' → 165000    (Tausender)
      '20.35'   → 20.35     (Dezimal, 2 Nachkommastellen)
      '20,5'    → 20.5      (Dezimal, Komma)
      '1.234.567' → 1234567 (Tausender, mehrfach)
    """
    if not s:
        return None
    # Reines Tausenderformat: '1.234.567' oder '55.000'
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", s):
        return float(s.replace(".", ""))
    # Komma als Dezimal, Punkte als Tausender: '1.234,5' → 1234.5
    if "," in s and "." in s:
        return float(s.replace(".", "").replace(",", "."))
    # Nur Komma → Dezimal
    if "," in s:
        return float(s.replace(",", "."))
    # Nur Punkt → Dezimal (z. B. 20.35)
    try:
        return float(s)
    except ValueError:
        return None

# Kennwert-Routing: (unit_match, context_keywords, target_user_knoten)
# Targets sind User-Knoten aus kennwert/-Ordner. Auto-Kennwerte (Bauzeit etc.)
# werden in Schritt I als neue User-Knoten ergänzt — bis dahin Datenluecke.
KENNWERT_ROUTING = [
    # CO2-bezogen — User-Knoten: CO2_Einsparung (umfasst absolut + prozent)
    ("%", ["co2", "treibhausgas"], "CO2_Einsparung"),
    ("t", ["co2", "treibhausgas"], "CO2_Einsparung"),
    ("kg", ["co2"], "CO2_Einsparung"),
    ("kgco2e", [], "CO2_Einsparung"),
    ("kgco2", [], "CO2_Einsparung"),
    # Embodied Carbon / Graue Energie
    ("m2", ["co2", "embodied", "graue energie", "emboldied"], "Graue_Energie"),
    ("kwh", ["energie", "energy", "graue"], "Graue_Energie"),
    # Wiederverwendungsquote (Gewicht, Volumen, Anteil) — User-Knoten Wiederverwendungsquote
    ("%", ["gewicht", "weight", "kg-rate"], "Wiederverwendungsquote"),
    ("%", ["volumen", "volume", "m3"], "Wiederverwendungsquote"),
    ("%", ["wiederverwend", "reuse", "reused", "ombruk"], "Wiederverwendungsquote"),
    ("t", ["wiederverwend", "reused", "reclaim", "salvaged", "stahl", "steel", "beton", "holz", "primaer", "primary"], "Wiederverwendungsquote"),
    ("kg", ["wiederverwend", "reused"], "Wiederverwendungsquote"),
    ("m3", ["volumen", "volume", "wiederverwend"], "Wiederverwendungsquote"),
    # Kosten/Geld — User-Knoten Materialwert
    ("%", ["kosten", "cost", "saving", "ersparnis"], "Materialwert"),
    ("eur", [], "Materialwert"),
    ("euro", [], "Materialwert"),
    ("chf", [], "Materialwert"),
    ("gbp", [], "Materialwert"),
    ("pfund", [], "Materialwert"),
    # Demontagegrad — User-Knoten
    ("%", ["demontage", "disassembly", "demountable"], "Demontagegrad"),
]

# Spread-Schwelle für Pseudo-Quellenkonflikte: Faktor max/min.
# > 30× heißt typischerweise verschiedene Bilanzgrenzen, kein Quellenwiderspruch.
PSEUDO_KONFLIKT_SPREAD_THRESHOLD = 30.0


def route_kennwert(unit: str, context: str) -> str:
    u = unit.lower()
    ctx = normalize(context)
    for u_match, kw_list, target in KENNWERT_ROUTING:
        if u != u_match.lower():
            continue
        if not kw_list:
            return target
        if any(kw in ctx for kw in kw_list):
            return target
    return "Datenluecke"


def derive_datenpunkte(all_pairs):
    items = []
    for r in all_pairs:
        if r["entity_type"] != "Kennwert":
            continue
        text = r["value"]
        text_norm = normalize(text)
        file_id = r["file"].replace(".md", "")
        for m in NUMBER_UNIT_RE.finditer(text_norm):
            num_str = m.group("num")
            unit = m.group("unit")
            value = parse_number(num_str)
            if value is None:
                continue
            # Voller Wert als Kontext — Mapping-Zellen sind kurz, volle Sicht > Window.
            context = text_norm
            kw_def = route_kennwert(unit, context)
            dp_id = safe_id(f"{file_id}__{kw_def}__{value}_{unit}", 100)
            items.append({
                "id": dp_id,
                "fallstudie": file_id,
                "kennwertdefinition": kw_def,
                "wert": value,
                "einheit": unit,
                "raw_kontext": text[:160],
            })
    return items


# === 4. Quelle ===

QUELLEN_SECTION_RE = re.compile(r"\n##\s+Quellen\s*\n(.+?)(?=\n##\s|\Z)", re.DOTALL | re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s\)\]]+")


def derive_quellen():
    """Eine Quelle pro unique URL/Label, mit Liste aller verwendenden Fallstudien.
    Wenn dieselbe URL in mehreren Fallstudien auftaucht: ein Knoten, mehrere
    Verweise — statt N Duplikate."""
    raw_entries: list[dict] = []
    for d in GEBAEUDE_DIRS:
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            if f.name in SKIP_FILES:
                continue
            text = f.read_text(encoding="utf-8")
            m = QUELLEN_SECTION_RE.search(text)
            if not m:
                continue
            block = m.group(1)
            file_id = f.name.replace(".md", "")
            for raw_line in block.splitlines():
                line = raw_line.strip()
                if not line or not (line.startswith("-") or line.startswith("*")):
                    continue
                line = line.lstrip("-*").strip()
                if not line:
                    continue
                line = re.sub(r"^\[?S\d+\]?\s*[:\.\-]?\s*", "", line)
                url_match = URL_RE.search(line)
                url = url_match.group(0).rstrip(".,;)") if url_match else ""
                label = line
                if url:
                    label = label.replace(url, "").strip(" ,.;:-")
                if not label and not url:
                    continue
                raw_entries.append({
                    "fallstudie": file_id,
                    "label": label,
                    "url": url,
                })

    # Dedup-Key: URL bevorzugt, sonst Label (genormt).
    by_key: dict[str, dict] = {}
    for e in raw_entries:
        key = e["url"] if e["url"] else e["label"].lower().strip()
        if key not in by_key:
            short_label = (e["label"] or e["url"])[:60]
            by_key[key] = {
                "id": safe_id(short_label, 90),
                "label": e["label"],
                "url": e["url"],
                "fallstudien": set(),
            }
        by_key[key]["fallstudien"].add(e["fallstudie"])

    # IDs auf eindeutigkeit prüfen (gleicher safe_id-Output bei unterschiedlichen URLs möglich)
    seen_ids: set[str] = set()
    result = []
    for q in by_key.values():
        base_id = q["id"]
        suffix = 1
        unique_id = base_id
        while unique_id in seen_ids:
            suffix += 1
            unique_id = f"{base_id}_{suffix}"
        seen_ids.add(unique_id)
        result.append({
            "id": unique_id,
            "label": q["label"],
            "url": q["url"],
            "fallstudien": sorted(q["fallstudien"]),
            "n_fallstudien": len(q["fallstudien"]),
        })
    return result


# === 5. Quellenkonflikt ===

def derive_quellenkonflikt(datenpunkte):
    """Echte Konflikte = mehrere Datenpunkte mit gleichem Kennwert+Einheit aber
    unterschiedlichen Werten. Spread > 30× wird als Pseudo-Konflikt geflaggt
    (verschiedene Bilanzgrenzen, kein Quellenwiderspruch)."""
    by_key = defaultdict(list)
    for dp in datenpunkte:
        if dp["kennwertdefinition"] == "Datenluecke":
            continue
        key = (dp["fallstudie"], dp["kennwertdefinition"], dp["einheit"])
        by_key[key].append(dp)
    items = []
    for (fs, kw, unit), dps in by_key.items():
        values = sorted({d["wert"] for d in dps})
        if len(values) < 2:
            continue
        spread = max(values) / min(values) if min(values) > 0 else float("inf")
        if spread > PSEUDO_KONFLIKT_SPREAD_THRESHOLD:
            continue  # Pseudo — verschiedene Bilanzgrenzen
        items.append({
            "id": safe_id(f"{fs}__{kw}__conflict_{values[0]}_vs_{values[-1]}", 100),
            "fallstudie": fs,
            "kennwertdefinition": kw,
            "einheit": unit,
            "werte": values,
            "spread": round(spread, 1),
            "datenpunkte": [d["id"] for d in dps],
            "n_datenpunkte": len(dps),
        })
    return items


# === 6. Offene_Frage ===

def derive_offene_fragen(all_pairs):
    items = []
    for r in all_pairs:
        val = r["value"].strip().lower()
        if val in {"unbekannt", "unklar", "nicht angegeben", "n/a", "fehlt"}:
            file_id = r["file"].replace(".md", "")
            of_id = safe_id(f"{file_id}__{r['entity_type']}_unbekannt", 80)
            items.append({
                "id": of_id,
                "fallstudie": file_id,
                "entity_type": r["entity_type"],
                "frage": f"{r['entity_type']} unbekannt — Quelle/Wert recherchieren",
            })
    return items


# === Output ===

def write_csv(name: str, items: list[dict], fields: list[str]) -> None:
    path = OUT_DIR / name
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for item in items:
            row = {k: item.get(k, "") for k in fields}
            for k, v in row.items():
                if isinstance(v, list):
                    row[k] = "; ".join(str(x) for x in v)
            w.writerow(row)


def write_full_yamls(file_controlled, name_canonicals, derived):
    """Erweitere die existierenden Building-YAMLs um derived-Entitäten."""
    yaml_dir = OUT_DIR / "building_yaml_full"
    yaml_dir.mkdir(exist_ok=True)

    # Aggregiere derived-Entitäten pro Fallstudie
    bp_per_file = defaultdict(list)
    for it in derived["bauteilpositionen"]:
        bp_per_file[it["fallstudie"]].append(it["id"])
    rk_per_file = defaultdict(list)
    for it in derived["reuse_ketten"]:
        rk_per_file[it["empfaenger_fallstudie"]].append(it["id"])
    dp_per_file = defaultdict(list)
    for it in derived["datenpunkte"]:
        dp_per_file[it["fallstudie"]].append(it["id"])
    q_per_file = defaultdict(list)
    for it in derived["quellen"]:
        for fs in it.get("fallstudien", []):
            q_per_file[fs].append(it["id"])
    qk_per_file = defaultdict(list)
    for it in derived["quellenkonflikte"]:
        qk_per_file[it["fallstudie"]].append(it["id"])
    of_per_file = defaultdict(list)
    for it in derived["offene_fragen"]:
        of_per_file[it["fallstudie"]].append(it["id"])

    # Lade existierende combined YAMLs
    combined_dir = EXTRACT / "name_clusters" / "building_yaml_combined"
    all_files: set[str] = set()
    if combined_dir.exists():
        for f in combined_dir.glob("*.yaml"):
            all_files.add(f.name.replace(".yaml", ".md"))
    all_files |= set(file_controlled.keys())

    for file in sorted(all_files):
        fallstudie = file.replace(".md", "")
        existing_path = combined_dir / f"{fallstudie}.yaml"
        if existing_path.exists():
            existing = existing_path.read_text(encoding="utf-8").rstrip()
            if existing.startswith("beziehungen:"):
                body = existing[len("beziehungen:"):].lstrip("\n")
            else:
                body = existing
        else:
            body = ""

        derived_lines = []
        if bp_per_file.get(fallstudie):
            ids = sorted(set(bp_per_file[fallstudie]))
            links = ", ".join(f'"[[bauteilposition/{i}]]"' for i in ids)
            derived_lines.append(f"  bauteilposition: [{links}]")
        if rk_per_file.get(fallstudie):
            ids = sorted(set(rk_per_file[fallstudie]))
            links = ", ".join(f'"[[reusekette/{i}]]"' for i in ids)
            derived_lines.append(f"  reusekette: [{links}]")
        if dp_per_file.get(fallstudie):
            ids = sorted(set(dp_per_file[fallstudie]))
            links = ", ".join(f'"[[datenpunkt/{i}]]"' for i in ids)
            derived_lines.append(f"  datenpunkt: [{links}]")
        if q_per_file.get(fallstudie):
            ids = sorted(set(q_per_file[fallstudie]))
            links = ", ".join(f'"[[quelle/{i}]]"' for i in ids)
            derived_lines.append(f"  quelle: [{links}]")
        if qk_per_file.get(fallstudie):
            ids = sorted(set(qk_per_file[fallstudie]))
            links = ", ".join(f'"[[quellenkonflikt/{i}]]"' for i in ids)
            derived_lines.append(f"  quellenkonflikt: [{links}]")
        if of_per_file.get(fallstudie):
            ids = sorted(set(of_per_file[fallstudie]))
            links = ", ".join(f'"[[offene_frage/{i}]]"' for i in ids)
            derived_lines.append(f"  offene_frage: [{links}]")

        full = "beziehungen:\n"
        if body:
            full += body.rstrip()
        if derived_lines:
            if body:
                full += "\n"
            full += "\n".join(derived_lines)
        out = yaml_dir / f"{fallstudie}.yaml"
        out.write_text(full + "\n", encoding="utf-8")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    all_pairs = load_pairs()
    file_controlled = load_controlled_links()
    name_canonicals = {
        et: load_name_canonicals(et)
        for et in ("Akteur", "Ort", "Projekt", "Gebaeude", "Fallstudie",
                   "Foerderprogramm", "Bauteilboerse", "Werkzeug", "Bericht")
    }

    bauteilpositionen = derive_bauteilposition(file_controlled, all_pairs, name_canonicals["Gebaeude"])
    reuse_ketten = derive_reusekette(file_controlled, all_pairs, name_canonicals["Gebaeude"])
    datenpunkte = derive_datenpunkte(all_pairs)
    quellen = derive_quellen()
    quellenkonflikte = derive_quellenkonflikt(datenpunkte)
    offene_fragen = derive_offene_fragen(all_pairs)

    write_csv("bauteilposition.csv", bauteilpositionen,
              ["id", "fallstudie", "bauteiltyp", "materialien", "donor_gebaeude", "n_materialien", "n_donors"])
    write_csv("reusekette.csv", reuse_ketten,
              ["id", "donor", "empfaenger_fallstudie", "material", "bauteile", "alle_materialien"])
    write_csv("datenpunkt.csv", datenpunkte,
              ["id", "fallstudie", "kennwertdefinition", "wert", "einheit", "raw_kontext"])
    write_csv("quelle.csv", quellen,
              ["id", "label", "url", "fallstudien", "n_fallstudien"])
    write_csv("quellenkonflikt.csv", quellenkonflikte,
              ["id", "fallstudie", "kennwertdefinition", "einheit", "werte", "spread", "datenpunkte", "n_datenpunkte"])
    write_csv("offene_frage.csv", offene_fragen,
              ["id", "fallstudie", "entity_type", "frage"])

    derived_bundle = {
        "bauteilpositionen": bauteilpositionen,
        "reuse_ketten": reuse_ketten,
        "datenpunkte": datenpunkte,
        "quellen": quellen,
        "quellenkonflikte": quellenkonflikte,
        "offene_fragen": offene_fragen,
    }
    write_full_yamls(file_controlled, name_canonicals, derived_bundle)

    print(f"Output: {OUT_DIR.relative_to(ROOT)}/")
    print()
    print(f"  Bauteilposition:  {len(bauteilpositionen):>4}")
    print(f"  ReuseKette:       {len(reuse_ketten):>4}")
    print(f"  Datenpunkt:       {len(datenpunkte):>4}")
    print(f"  Quelle:           {len(quellen):>4}")
    print(f"  Quellenkonflikt:  {len(quellenkonflikte):>4}")
    print(f"  Offene_Frage:     {len(offene_fragen):>4}")
    print()
    n_kennwert_routed = sum(1 for d in datenpunkte if d["kennwertdefinition"] != "Datenluecke")
    print(f"Datenpunkte mit erkanntem Kennwert: {n_kennwert_routed}/{len(datenpunkte)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
