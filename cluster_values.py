#!/usr/bin/env python3
"""
cluster_values.py — Halbautomatisches Token-Clustering der Roh-Werte pro Entitätstyp.

Liest:  _extract/all_pairs.csv  (von extract_entities.py erzeugt)
Schreibt nach _extract/clusters/:
  - <EntityType>.csv        Cluster pro Typ: cluster_label, n_files, n_raw_values, raw_values
  - _summary.csv            Pro Typ: n_clusters, n_unclustered_values, n_unclustered_files
  - _anchor_candidates.csv  Alle Token-Anker mit File-Coverage (zur Stopwort-Pflege)

Logik:
  1. Pro Wert Tokens extrahieren (alphanumerisch, Mindestlänge 3, keine reinen Zahlen).
  2. Stopwörter raus (DE/EN-Standard + Domain + der Entitätstyp selbst).
  3. Token = Anker-Kandidat, wenn er in Werten vorkommt, die zusammen ≥3 Files abdecken.
  4. Jeder Wert wird allen Ankern zugewiesen, deren Token er enthält. Werte ohne Anker →
     '_unclustered'.
  5. Mehrfachzuordnung ist erlaubt und gewollt — der User entscheidet im Review,
     wie er bei Mischwerten ('Stahlträger und Holzbalken') splittet.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
EXTRACT = ROOT / "_extract"
INPUT = EXTRACT / "all_pairs.csv"
OUT_DIR = EXTRACT / "clusters"

ANCHOR_MIN_FILES = 3
TOKEN_MIN_LEN = 3

STOPWORDS_DE = {
    "und", "oder", "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen",
    "eines", "einer", "einem", "mit", "von", "fuer", "fur", "in", "auf", "an", "bei",
    "zu", "aus", "nach", "vor", "ueber", "uber", "unter", "durch", "gegen", "ohne",
    "um", "im", "am", "zur", "zum", "beim", "vom", "ist", "sind", "war", "waren",
    "werden", "wird", "wurde", "wurden", "sein", "hat", "haben", "hatte", "hatten",
    "kann", "koennen", "konnen", "konnte", "konnten", "soll", "sollte", "muss",
    "muessen", "mussen", "dieser", "diese", "dieses", "alle", "alles", "jeder",
    "jede", "jedes", "viele", "manche", "einige", "wenige", "auch", "noch", "schon",
    "nur", "sowie", "bzw", "etc", "usw", "siehe", "siehe", "etwa", "rund", "ungefaehr",
    "ungefahr", "mehr", "weniger", "circa", "ca", "ggf", "bzw", "z.b", "zb",
    "zwischen", "innerhalb", "ausserhalb", "ausserhalb", "werden", "worden", "fuer",
}
STOPWORDS_EN = {
    "the", "and", "or", "of", "in", "on", "at", "by", "with", "for", "to", "from",
    "but", "that", "this", "these", "those", "is", "are", "was", "were", "be",
    "been", "being", "has", "have", "had", "as", "an", "a", "into", "than", "then",
    "so", "such", "out", "up", "down", "off", "via", "per", "vs",
}
STOPWORDS_DOMAIN = {
    "reuse", "re", "wiederverwendet", "wiederverwendete", "wiederverwendeter",
    "wiederverwendetes", "wiederverwendeten", "wiederverwendung", "wiederverwendungs",
    "neu", "neue", "neuer", "neuen", "neues", "alt", "alte", "alter", "alten", "altes",
    "bestand", "bestands", "bestandes", "weiter", "weitere", "weiteres", "weiteren",
    "ggf", "etc", "usw", "uvm", "incl", "inkl",
    "circular", "circularity", "ombruk", "harvested", "harvest", "reclaimed",
    "secondary", "primary", "donor", "doneor", "empfaenger", "empfanger",
    "fallstudie", "fallstudien", "projekt", "projekte", "project", "building", "buildings",
}


def normalize(s: str) -> str:
    s = s.lower()
    s = (s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss"))
    return s


def tokenize(s: str) -> list[str]:
    s = normalize(s)
    tokens = re.findall(r"[a-z0-9]+", s)
    return [t for t in tokens if len(t) >= TOKEN_MIN_LEN and not t.isdigit()]


def stopwords_for(entity_type: str) -> set[str]:
    sw = STOPWORDS_DE | STOPWORDS_EN | STOPWORDS_DOMAIN
    sw = set(sw)
    et_norm = normalize(entity_type)
    for t in tokenize(et_norm):
        sw.add(t)
    # Plural-/Variantenformen des Typs
    if et_norm.endswith("e"):
        sw.add(et_norm[:-1])
    if et_norm.endswith("en"):
        sw.add(et_norm[:-2])
    return sw


def safe_filename(name: str) -> str:
    return re.sub(r'[\\/<>:"|?*\s]+', "_", name).strip("_") or "Unbenannt"


def load_pairs() -> list[tuple[str, str, str]]:
    """Returns list of (file, entity_type, value)."""
    if not INPUT.exists():
        print(f"FEHLER: {INPUT} nicht gefunden. Erst extract_entities.py laufen lassen.")
        sys.exit(1)
    pairs = []
    with INPUT.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            pairs.append((row["file"], row["entity_type"], row["value"]))
    return pairs


def cluster_entity(
    entity_type: str,
    rows: list[tuple[str, str]],  # (file, value)
) -> tuple[dict[str, dict], list[tuple[str, set]], dict[str, int]]:
    """
    Returns:
      clusters: dict[anchor → {"files": set, "values": Counter[value→count]}]
      unclustered: list[(value, files)]
      anchor_files: dict[anchor → file_count]   (für Anker-Kandidaten-Liste)
    """
    sw = stopwords_for(entity_type)

    # Pro Wert die Files sammeln und Tokens berechnen
    value_files: dict[str, set[str]] = defaultdict(set)
    value_tokens: dict[str, set[str]] = {}
    for file, val in rows:
        value_files[val].add(file)

    for val in value_files:
        value_tokens[val] = {t for t in tokenize(val) if t not in sw}

    # Token → File-Coverage (Union über alle Werte, die dieses Token enthalten)
    token_files: dict[str, set[str]] = defaultdict(set)
    for val, tokens in value_tokens.items():
        for t in tokens:
            token_files[t] |= value_files[val]

    # Anker = Token mit ≥ ANCHOR_MIN_FILES File-Coverage
    anchors = {t for t, files in token_files.items() if len(files) >= ANCHOR_MIN_FILES}

    clusters: dict[str, dict] = {}
    for a in anchors:
        clusters[a] = {"files": set(), "values": Counter()}

    unclustered: list[tuple[str, set[str]]] = []
    for val, tokens in value_tokens.items():
        hit_anchors = tokens & anchors
        if not hit_anchors:
            unclustered.append((val, value_files[val]))
            continue
        for a in hit_anchors:
            clusters[a]["files"] |= value_files[val]
            clusters[a]["values"][val] += len(value_files[val])

    anchor_files = {t: len(token_files[t]) for t in anchors}
    return clusters, unclustered, anchor_files


def write_cluster_csv(entity_type: str, clusters: dict, unclustered: list) -> None:
    path = OUT_DIR / f"{safe_filename(entity_type)}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cluster_label", "n_files", "n_raw_values", "raw_values"])

        # Cluster nach Files absteigend
        sorted_anchors = sorted(
            clusters.keys(),
            key=lambda a: (-len(clusters[a]["files"]), a),
        )
        for a in sorted_anchors:
            files = clusters[a]["files"]
            vals = clusters[a]["values"]
            raw = "; ".join(
                f"{v} (n={c})" for v, c in sorted(vals.items(), key=lambda kv: -kv[1])
            )
            w.writerow([a, len(files), len(vals), raw])

        # Unclustered als Sonderzeile
        if unclustered:
            uf: set[str] = set()
            for _, files in unclustered:
                uf |= files
            raw = "; ".join(
                f"{v} (n={len(files)})"
                for v, files in sorted(unclustered, key=lambda kv: -len(kv[1]))
            )
            w.writerow(["_unclustered", len(uf), len(unclustered), raw])


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pairs = load_pairs()
    by_type: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for file, et, val in pairs:
        by_type[et].append((file, val))

    summary_rows = []
    anchor_rows = []
    for et in sorted(by_type):
        clusters, unclustered, anchor_files = cluster_entity(et, by_type[et])
        write_cluster_csv(et, clusters, unclustered)
        n_unclustered_files: set[str] = set()
        for _, fs in unclustered:
            n_unclustered_files |= fs
        summary_rows.append([
            et,
            len(by_type[et]),
            len(set(v for _, v in by_type[et])),
            len(clusters),
            len(unclustered),
            len(n_unclustered_files),
        ])
        for anchor, n_files in anchor_files.items():
            anchor_rows.append([et, anchor, n_files])

    # Summary
    with (OUT_DIR / "_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "entity_type", "total_rows", "unique_values",
            "n_clusters", "n_unclustered_values", "n_unclustered_files",
        ])
        w.writerows(summary_rows)

    # Anker-Kandidaten
    anchor_rows.sort(key=lambda r: (r[0], -r[2]))
    with (OUT_DIR / "_anchor_candidates.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entity_type", "anchor_token", "n_files"])
        w.writerows(anchor_rows)

    # Konsolen-Report — nur prominente Typen
    print(f"Clustering: {len(by_type)} Entitätstypen verarbeitet")
    print(f"Output: {OUT_DIR.relative_to(ROOT)}/")
    print()
    print(f"{'Typ':<24} {'Werte':>6} {'Cluster':>8} {'Unclust.':>9}")
    print("-" * 52)
    for row in sorted(summary_rows, key=lambda r: -r[1]):
        et, total, unique, ncl, nunc_v, nunc_f = row
        if total < 10:
            continue
        print(f"{et:<24} {unique:>6} {ncl:>8} {nunc_v:>9}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
