#!/usr/bin/env python3
"""
dedup_names.py — Clustert Namen-Varianten in Open-Vocabulary-Entitätstypen.

Open-Vocabulary-Typen sind Typen, deren Werte SELBST die Knoten sind (Eigennamen),
nicht Kategorien aus einer geschlossenen Taxonomie. Beispiele:
  Akteur, Ort, Projekt, Gebaeude, Fallstudie, Foerderprogramm, Bauteilboerse,
  Werkzeug, Dokument

Role-Typen (Bauherr, Architekt, Tragwerksplaner, Lehrstuhl) werden in Akteur
zusammengeführt mit zusätzlicher Spalte 'rollen', die alle Rollen listet.

Clustering:
  1. Normalisierung (lowercase, Umlaute aufgelöst, Sonderzeichen → Space).
  2. Token-Set ohne Stopwörter (Artikel, Rechtsformen, generische Worte).
  3. Union-Find-Merge bei: exakter Normalize-Match | Token-Subset (≥2 Tokens) |
     Single-Token-Containment (≥5 Zeichen) | Jaccard ≥ 0.66.

Output in _extract/name_clusters/:
  - <EntityType>.csv                    Cluster-Tabelle pro Typ
  - _summary.csv                        Übersicht
  - building_yaml_combined/<file>.yaml  Kombiniertes Frontmatter (controlled + open)
"""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
EXTRACT = ROOT / "_extract"
INPUT = EXTRACT / "all_pairs.csv"
OUT_DIR = EXTRACT / "name_clusters"
CONTROLLED_YAML_DIR = EXTRACT / "taxonomy_matched" / "building_yaml"

OPEN_VOCAB_TYPES = {
    "Akteur", "Ort", "Projekt", "Gebaeude", "Fallstudie",
    "Foerderprogramm", "Bauteilboerse", "Werkzeug", "Dokument",
    "Bericht", "Spendergebaeude",
}
ROLE_TYPES = {"Bauherr", "Architekt", "Tragwerksplaner", "Lehrstuhl"}

NAME_STOPS = {
    "the", "der", "die", "das", "den", "des", "dem", "und", "of", "and", "for",
    "in", "im", "am", "at", "auf", "an", "zu", "zur", "zum", "von", "vom",
    "ag", "gmbh", "kg", "ev", "bv", "ltd", "sa", "sarl", "spa", "inc",
    "co", "company", "corp", "studio", "office", "buero", "buros",
    "stadt", "city", "ville",
}
SKIP_VALUES = {"unbekannt", "unknown", "unklar", "fehlt", "n a", "tbd"}

JACCARD_THRESHOLD = 0.66
MIN_TOKEN_LEN = 3
SINGLE_TOKEN_MIN_CHARS = 5


def normalize(s: str) -> str:
    s = s.lower()
    s = (s.replace("ä", "ae").replace("ö", "oe")
          .replace("ü", "ue").replace("ß", "ss")
          .replace("²", "2").replace("³", "3")
          .replace("₂", "2").replace("₃", "3").replace("₄", "4"))
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def split_actor_value(v: str) -> list[str]:
    """Splittet Mehrfach-Akteur-Zellen in einzelne Akteurs-Strings.

    Trenner: ';' und ' / '. Kommas nur splitten, wenn ≥3 Kommas UND alle
    Segmente kurz UND keine 'und/and/et'-Indikatoren — sonst Risiko, echte
    Namen-mit-Komma zu zerreißen.
    """
    parts = [p.strip() for p in re.split(r"\s*;\s*", v) if p.strip()]
    expanded: list[str] = []
    for p in parts:
        sub = [s.strip() for s in re.split(r"\s+/\s+", p) if s.strip()]
        for s in sub:
            n_commas = s.count(",")
            if n_commas >= 3:
                segs = [seg.strip() for seg in s.split(",") if seg.strip()]
                if all(len(seg) <= 30 for seg in segs) and not any(
                    f" {kw} " in f" {seg.lower()} "
                    for seg in segs
                    for kw in ("und", "and", "et", "with")
                ):
                    expanded.extend(segs)
                    continue
            expanded.append(s)
    return expanded


def tokenize(s: str) -> set[str]:
    n = normalize(s)
    return {t for t in n.split() if len(t) >= MIN_TOKEN_LEN and t not in NAME_STOPS}


def safe_node_id(name: str) -> str:
    s = normalize(name)
    parts = [p.capitalize() for p in s.split() if p]
    return "_".join(parts) if parts else "Unbenannt"


def safe_filename(name: str) -> str:
    return re.sub(r'[\\/<>:"|?*\s]+', "_", name).strip("_") or "Unbenannt"


class UnionFind:
    def __init__(self, n: int):
        self.p = list(range(n))

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.p[rx] = ry


def cluster_values(items: list[tuple[str, set[str], set[str]]]) -> list[dict]:
    """items: [(raw_value, token_set, files_set), ...] → list of cluster dicts."""
    n = len(items)
    norms = [normalize(v) for v, _, _ in items]
    tokens_list = [t for _, t, _ in items]
    uf = UnionFind(n)

    for i in range(n):
        ni, ti = norms[i], tokens_list[i]
        for j in range(i + 1, n):
            nj, tj = norms[j], tokens_list[j]
            # 1. Exact normalized match
            if ni == nj:
                uf.union(i, j)
                continue
            if not ti or not tj:
                continue
            # 2. Token subset (both ≥2 tokens)
            if min(len(ti), len(tj)) >= 2 and (ti <= tj or tj <= ti):
                uf.union(i, j)
                continue
            # 3. Single distinctive token containment
            if len(ti) == 1 or len(tj) == 1:
                short, long_ = (ti, tj) if len(ti) <= len(tj) else (tj, ti)
                if len(short) == 1:
                    tok = next(iter(short))
                    if len(tok) >= SINGLE_TOKEN_MIN_CHARS and tok in long_:
                        uf.union(i, j)
                        continue
            # 4. Jaccard ≥ threshold (both ≥2 tokens)
            if len(ti) >= 2 and len(tj) >= 2:
                inter = len(ti & tj)
                uni = len(ti | tj)
                if uni > 0 and inter / uni >= JACCARD_THRESHOLD:
                    uf.union(i, j)

    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        groups[uf.find(i)].append(i)

    clusters = []
    for indices in groups.values():
        members = [items[i] for i in indices]
        # Canonical: variant mit meisten Files; Tiebreak längster Name
        canonical = max(members, key=lambda m: (len(m[2]), len(m[0])))[0]
        all_files: set[str] = set()
        variants = []
        for v, _, files in members:
            variants.append(v)
            all_files |= files
        clusters.append({
            "canonical": canonical,
            "variants": variants,
            "files": all_files,
            "n_files": len(all_files),
        })
    clusters.sort(key=lambda c: -c["n_files"])
    return clusters


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if not INPUT.exists():
        print(f"FEHLER: {INPUT} nicht gefunden.")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Lade pairs, gruppiere nach Typ und Wert
    by_type: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    role_per_value: dict[str, set[str]] = defaultdict(set)

    with INPUT.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            file = row["file"]
            et = row["entity_type"]
            val = row["value"].strip()
            if not val:
                continue
            if et in ROLE_TYPES:
                for sub in split_actor_value(val):
                    by_type["Akteur"][sub].add(file)
                    role_per_value[sub].add(et)
            elif et == "Akteur":
                for sub in split_actor_value(val):
                    by_type["Akteur"][sub].add(file)
            elif et in OPEN_VOCAB_TYPES:
                by_type[et][val].add(file)

    summary_rows = []
    all_clusters: dict[str, list[dict]] = {}

    for et in sorted(by_type):
        items = []
        for val, files in by_type[et].items():
            if normalize(val) in SKIP_VALUES:
                continue
            items.append((val, tokenize(val), files))
        if not items:
            continue

        clusters = cluster_values(items)
        all_clusters[et] = clusters

        # Pro-Typ-CSV
        path = OUT_DIR / f"{safe_filename(et)}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            cols = ["canonical_name", "node_id", "n_files", "n_variants"]
            if et == "Akteur":
                cols.append("rollen")
            cols += ["variants", "files"]
            w.writerow(cols)
            for c in clusters:
                vars_str = "; ".join(c["variants"])
                files_str = "; ".join(sorted(c["files"]))
                row = [
                    c["canonical"],
                    safe_node_id(c["canonical"]),
                    c["n_files"],
                    len(c["variants"]),
                ]
                if et == "Akteur":
                    roles: set[str] = set()
                    for v in c["variants"]:
                        roles |= role_per_value.get(v, set())
                    row.append("; ".join(sorted(roles)))
                row += [vars_str, files_str]
                w.writerow(row)

        n_total = sum(len(c["variants"]) for c in clusters)
        n_clusters = len(clusters)
        summary_rows.append([et, n_total, n_clusters, n_total - n_clusters])

    # _summary.csv
    with (OUT_DIR / "_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entity_type", "total_unique_values", "n_clusters", "n_merged"])
        w.writerows(summary_rows)

    # Building-Mapping: file → entity_type → set(canonical)
    building_open: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for et, clusters in all_clusters.items():
        for c in clusters:
            for file in c["files"]:
                building_open[file][et].add(c["canonical"])

    # Combined YAML: controlled (vom Matcher) + open (von hier)
    combined_dir = OUT_DIR / "building_yaml_combined"
    combined_dir.mkdir(exist_ok=True)

    all_files = set(building_open.keys())
    if CONTROLLED_YAML_DIR.exists():
        for cy in CONTROLLED_YAML_DIR.glob("*.yaml"):
            all_files.add(cy.name.replace(".yaml", ".md"))

    for file in sorted(all_files):
        controlled_path = CONTROLLED_YAML_DIR / file.replace(".md", ".yaml")
        if controlled_path.exists():
            controlled_text = controlled_path.read_text(encoding="utf-8").strip()
            if controlled_text.startswith("beziehungen:"):
                body = controlled_text[len("beziehungen:"):].lstrip("\n")
            else:
                body = controlled_text
        else:
            body = ""

        open_lines = []
        for et in sorted(building_open.get(file, {})):
            field = et.lower()
            nodes = sorted(building_open[file][et])
            slugs = [safe_node_id(n) for n in nodes]
            links = ", ".join(f'"[[{field}/{s}]]"' for s in slugs)
            open_lines.append(f"  {field}: [{links}]")

        full = "beziehungen:\n"
        if body:
            full += body.rstrip()
        if open_lines:
            if body:
                full += "\n"
            full += "\n".join(open_lines)
        out = combined_dir / file.replace(".md", ".yaml")
        out.write_text(full + "\n", encoding="utf-8")

    # Konsolen-Report
    print(f"Output: {OUT_DIR.relative_to(ROOT)}/")
    print()
    print(f"{'Typ':<22} {'Werte':>6} {'Cluster':>8} {'Merged':>7}")
    print("-" * 46)
    for row in sorted(summary_rows, key=lambda r: -r[1]):
        et, total, ncl, merged = row
        print(f"{et:<22} {total:>6} {ncl:>8} {merged:>7}")
    print()
    print(f"Combined YAML-Dateien: {len(all_files)} → {combined_dir.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
