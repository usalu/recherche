#!/usr/bin/env python3
"""
match_taxonomy.py — Matcht Roh-Werte aus _extract/all_pairs.csv gegen kuratierte
Seed-Knoten in taxonomy.json.

Strategie:
  - Pro Roh-Wert wird normalisiert (lowercase, Umlaut-Auflösung, Sonderzeichen → Space).
  - Pro Knoten in der typgleichen Taxonomie wird die Summe der Match-Bytes berechnet:
    jedes Keyword, das als Substring im normalisierten Roh-Wert vorkommt,
    bringt `len(keyword)` Punkte (längere Keywords gewichten stärker — 'stahlbeton'
    schlägt 'stahl').
  - Knoten mit Score > 0 werden zugeordnet. Mehrfachzuordnung erlaubt, wenn
    Sekundär-Score ≥ 80 % des Top-Scores erreicht.
  - Werte ohne Match → '_unmatched'.

Output in _extract/taxonomy_matched/:
  - <EntityType>.csv          Pro Knoten: n_files, n_raw_values, raw_values
  - _coverage.csv             Pro Typ: matched/unmatched/Pct
  - _unmatched.csv            Alle nicht gematchten Roh-Werte (Kandidaten für neue Knoten)
  - _multi_match.csv          Werte, die ≥2 Knoten erreicht haben (zur Disambiguierung)
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
EXTRACT = ROOT / "_extract"
INPUT = EXTRACT / "all_pairs.csv"
TAXONOMY_PATH = ROOT / "taxonomy.json"
OUT_DIR = EXTRACT / "taxonomy_matched"

SECONDARY_RATIO = 0.8  # Sekundär-Match wenn Score ≥ 80 % vom Top


def normalize(s: str) -> str:
    s = s.lower()
    s = (
        s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
         .replace("²", "2").replace("³", "3")
         .replace("₂", "2").replace("₃", "3").replace("₄", "4")
    )
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_keyword(kw: str) -> str:
    return normalize(kw)


def match_value(value_norm: str, nodes: dict) -> list[tuple[str, int]]:
    """Returns sorted [(node_name, score)] for nodes that matched.

    Substring-Match: jedes Keyword, das als Substring im normalisierten Wert
    vorkommt, bringt len(keyword) Punkte. Längere Keywords schlagen kürzere
    automatisch durch das Score-System (z. B. 'stahlbeton' > 'stahl').
    """
    results = []
    for node_name, node_data in nodes.items():
        if node_name.startswith("_"):
            continue
        score = 0
        for kw in node_data.get("keywords", []):
            kw_norm = normalize_keyword(kw)
            if not kw_norm or len(kw_norm) < 3:
                continue
            if kw_norm in value_norm:
                score += len(kw_norm)
        if score > 0:
            results.append((node_name, score))
    results.sort(key=lambda x: -x[1])
    return results


def reclassify_pair(et: str, val: str) -> tuple[str, str]:
    """Korrigiert Fehlklassifizierungen aus dem Extrakt.

    'ReUse_Fenster' im Material-Bucket gehört semantisch zu Bauteil/Fenster.
    Diese Werte stammen aus älteren gebaeude/-Frontmatter-Konventionen.
    """
    if et == "Material" and val.lower().startswith("reuse_"):
        # Behalte Wert; verschiebe in Bauteil-Bucket. Matcher erkennt 'reuse_x'-Keywords.
        return ("Bauteil", val)
    return (et, val)


def safe_filename(name: str) -> str:
    return re.sub(r'[\\/<>:"|?*\s]+', "_", name).strip("_") or "Unbenannt"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if not INPUT.exists():
        print(f"FEHLER: {INPUT} nicht gefunden. Erst extract_entities.py laufen.")
        return 1
    if not TAXONOMY_PATH.exists():
        print(f"FEHLER: {TAXONOMY_PATH} nicht gefunden.")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    taxonomy = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    typed_taxonomies = {k: v for k, v in taxonomy.items() if not k.startswith("_")}

    pairs: list[tuple[str, str, str]] = []
    with INPUT.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            et, val = reclassify_pair(row["entity_type"], row["value"])
            pairs.append((row["file"], et, val))

    # Aggregation
    node_files: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    node_values: dict[str, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    unmatched: dict[str, list[tuple[str, str]]] = defaultdict(list)
    multi_matches: list[tuple[str, str, str, list[str]]] = []  # (et, file, value, [nodes])
    type_total: Counter = Counter()
    type_matched: Counter = Counter()

    for file, et, val in pairs:
        if et not in typed_taxonomies:
            continue
        type_total[et] += 1
        nodes = typed_taxonomies[et]
        val_norm = normalize(val)
        results = match_value(val_norm, nodes)

        if not results:
            unmatched[et].append((file, val))
            continue

        type_matched[et] += 1
        top_score = results[0][1]
        threshold = max(1, int(top_score * SECONDARY_RATIO))
        assigned: list[str] = []
        for node_name, score in results:
            if score < threshold:
                break
            node_files[et][node_name].add(file)
            node_values[et][node_name][val] += 1
            assigned.append(node_name)
        if len(assigned) >= 2:
            multi_matches.append((et, file, val, assigned))

    # Pro-Typ-CSVs
    for et, nodes in typed_taxonomies.items():
        path = OUT_DIR / f"{safe_filename(et)}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([
                "seed_node", "kategorie", "definition",
                "n_files", "n_raw_values", "raw_values",
            ])
            # Sortiert nach n_files absteigend, dann Knotenname
            sorted_nodes = sorted(
                nodes.items(),
                key=lambda kv: (-len(node_files[et].get(kv[0], set())), kv[0]),
            )
            for node_name, node_data in sorted_nodes:
                files = node_files[et].get(node_name, set())
                vals = node_values[et].get(node_name, Counter())
                raw = "; ".join(
                    f"{v} (n={c})"
                    for v, c in sorted(vals.items(), key=lambda kv: -kv[1])
                )
                w.writerow([
                    node_name,
                    node_data.get("kategorie", ""),
                    node_data.get("definition", ""),
                    len(files),
                    len(vals),
                    raw,
                ])

    # _coverage.csv
    coverage_rows = []
    for et in typed_taxonomies:
        total = type_total[et]
        matched = type_matched[et]
        pct = round(100 * matched / max(1, total), 1)
        coverage_rows.append([et, total, matched, total - matched, pct])
    with (OUT_DIR / "_coverage.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entity_type", "total", "matched", "unmatched", "match_pct"])
        w.writerows(coverage_rows)

    # _unmatched.csv (Kandidaten für neue Knoten oder fehlende Keywords)
    with (OUT_DIR / "_unmatched.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entity_type", "file", "raw_value"])
        for et in sorted(unmatched):
            for file, val in unmatched[et]:
                w.writerow([et, file, val])

    # _multi_match.csv (Mehrfachzuordnung — manchmal korrekt, manchmal Disambiguierung nötig)
    with (OUT_DIR / "_multi_match.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entity_type", "file", "raw_value", "matched_nodes"])
        for et, file, val, nodes_list in multi_matches:
            w.writerow([et, file, val, " | ".join(nodes_list)])

    # Building-Output: pro Fallstudie alle Knoten-Verbindungen
    # Aggregation: file -> entity_type -> {nodes}
    building_links: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for et, nfiles in node_files.items():
        for node, files in nfiles.items():
            for file in files:
                building_links[file][et].add(node)

    # building_links.csv — flach abfragbar
    with (OUT_DIR / "building_links.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "entity_type", "seed_node"])
        for file in sorted(building_links):
            for et in sorted(building_links[file]):
                for node in sorted(building_links[file][et]):
                    w.writerow([file, et, node])

    # building_yaml/<file>.yaml — Tolaria-Frontmatter-Snippet pro Fallstudie
    yaml_dir = OUT_DIR / "building_yaml"
    yaml_dir.mkdir(exist_ok=True)
    for file in sorted(building_links):
        yaml_lines = ["beziehungen:"]
        for et in sorted(building_links[file]):
            nodes = sorted(building_links[file][et])
            # Tolaria-Konvention: typname kleingeschrieben, Wikilinks
            field = et.lower()
            links = ", ".join(f'"[[{field}/{n}]]"' for n in nodes)
            yaml_lines.append(f"  {field}: [{links}]")
        out_name = file.replace(".md", ".yaml")
        (yaml_dir / out_name).write_text("\n".join(yaml_lines), encoding="utf-8")

    # Konsolen-Report
    print(f"Taxonomien geladen: {list(typed_taxonomies.keys())}")
    print(f"Output: {OUT_DIR.relative_to(ROOT)}/")
    print()
    print(f"{'Typ':<20} {'Total':>6} {'Match':>6} {'Unmat':>6} {'%':>5} {'#Knoten':>8} {'#leer':>6}")
    print("-" * 60)
    for et, total, matched, unm, pct in coverage_rows:
        n_nodes = len(typed_taxonomies[et])
        empty = sum(1 for n in typed_taxonomies[et] if not node_files[et].get(n))
        print(f"{et:<20} {total:>6} {matched:>6} {unm:>6} {pct:>4}% {n_nodes:>8} {empty:>6}")

    print(f"\nMulti-Matches: {len(multi_matches)} (siehe _multi_match.csv)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
