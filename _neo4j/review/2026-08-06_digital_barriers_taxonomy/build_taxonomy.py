"""Build the German barrier-taxonomy import artifacts from the authored TSV fragments.

Reads  taxonomy_source_*.tsv  (columns: code, name_de, name_en, definition_de)
Writes taxonomy_source.tsv          (merged, code-sorted)
       taxonomy_de.kg.jsonl         (nodes + HAT_HUERDEKATEGORIE hierarchy, importer-ready)
       code_id_map.csv              (code, id, label, is_leaf, marker)

Model (see PLAN.md / plan file):
  - leaf  -> :Huerde          id h_<codeslug>_<nameslug>
  - inner -> :HuerdeKategorie id huek_<codeslug>_<nameslug>   (domains A-H have no parent)
  - every framework-only node also carries secondary label :BarriereReferenz
    EXCEPT h_h5_1_keine_lagerkapazitaet (the observed anchor that Fehlende_Lagerflaeche merges into).
  - hierarchy edge child-[:HAT_HUERDEKATEGORIE]->parent, id r_<from>__HAT_HUERDEKATEGORIE__<to>.

No database writes. Deterministic. Fails hard on any structural problem.

Usage:  python build_taxonomy.py
"""
from __future__ import annotations

import csv
import glob
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
REVIEW_RUN = "digital_barriers_2026_08_06"
# Every framework node is marked :BarriereReferenz. The observed layer is the 9
# pre-existing :Huerde nodes (no barriere_code) reclassified under families by the
# migration patch. Invariant: has barriere_code  <=>  :BarriereReferenz  <=>  framework.

# Framework provenance (the taxonomy synthesises these systematic reviews).
SOURCE_TITLES = [
    "Rakhshan et al. 2020 systematic review",
    "Thirumal et al. 2024 systematic review",
    "Nordic Council of Ministers 2023",
]
SOURCE_URLS = [
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC7472835/",
    "https://www.mdpi.com/2071-1050/16/8/3185",
    "https://pub.norden.org/nord2023-031/",
]

# The 8 family anchors that observed live hurdles classify under (H5 also takes
# Witterung_Feuchte and Fehlende_Lagerflaeche).
EXPECTED_ANCHOR_CODES = ["D6", "E5", "F6", "G1", "G4", "G5", "H4", "H5"]

UMLAUT = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
          "Ä": "ae", "Ö": "oe", "Ü": "ue"}


def die(msg: str) -> None:
    print(f"[FAIL] {msg}")
    sys.exit(1)


def slug(text: str) -> str:
    for k, v in UMLAUT.items():
        text = text.replace(k, v)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def code_slug(code: str) -> str:
    return code.lower().replace(".", "_")


def parent_code(code: str) -> str | None:
    if len(code) == 1:            # domain letter A-H
        return None
    if "." not in code:           # family, e.g. A1 -> A
        return code[0]
    return code.rsplit(".", 1)[0]  # A1.1 -> A1 ; H5.3 -> H5 ; A1.1.1 -> A1.1


def code_sort_key(code: str):
    letter = code[0]
    rest = code[1:]
    nums = [int(n) for n in re.findall(r"\d+", rest)]
    return (letter, nums)


def load_rows() -> list[dict]:
    frags = sorted(glob.glob(str(HERE / "taxonomy_source_*.tsv")))
    if not frags:
        die("no taxonomy_source_*.tsv fragments found")
    rows: dict[str, dict] = {}
    for frag in frags:
        with open(frag, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            need = {"code", "name_de", "name_en", "definition_de"}
            if not need.issubset(set(reader.fieldnames or [])):
                die(f"{Path(frag).name}: header must be {sorted(need)}, got {reader.fieldnames}")
            for r in reader:
                code = (r["code"] or "").strip()
                if not code:
                    continue
                if code in rows:
                    die(f"duplicate code {code!r} (in {Path(frag).name} and earlier)")
                rows[code] = {
                    "code": code,
                    "name_de": (r["name_de"] or "").strip(),
                    "name_en": (r["name_en"] or "").strip(),
                    "definition_de": (r["definition_de"] or "").strip(),
                }
    return [rows[c] for c in sorted(rows, key=code_sort_key)]


def main() -> int:
    rows = load_rows()
    codes = {r["code"] for r in rows}

    # children map -> leaf detection
    children: dict[str, list[str]] = {c: [] for c in codes}
    domains = []
    for r in rows:
        c = r["code"]
        p = parent_code(c)
        if p is None:
            domains.append(c)
        else:
            if p not in codes:
                die(f"code {c!r} has parent {p!r} which is not in the source")
            children[p].append(c)

    if sorted(domains) != list("ABCDEFGH"):
        die(f"expected 8 domains A-H, got {sorted(domains)}")

    # assign id/label/marker
    meta: dict[str, dict] = {}
    seen_ids: dict[str, str] = {}
    for r in rows:
        c = r["code"]
        is_leaf = len(children[c]) == 0
        primary = "Huerde" if is_leaf else "HuerdeKategorie"
        prefix = "h_" if is_leaf else "huek_"
        node_id = f"{prefix}{code_slug(c)}_{slug(r['name_de'])}".rstrip("_")
        if not re.fullmatch(r"[a-z0-9_]+", node_id):
            die(f"non-ascii id {node_id!r} for code {c}")
        if node_id in seen_ids:
            die(f"duplicate id {node_id!r} (codes {seen_ids[node_id]} and {c})")
        seen_ids[node_id] = c
        meta[c] = {"id": node_id, "primary": primary, "is_leaf": is_leaf, "marker": True}

    # anchor sanity — every family the observed hurdles classify under must exist
    for ac in EXPECTED_ANCHOR_CODES:
        if ac not in meta:
            die(f"expected anchor code {ac} missing from source")

    # emit
    nodes, rels = [], []
    for r in rows:
        c = r["code"]
        m = meta[c]
        labels = [m["primary"]] + (["BarriereReferenz"] if m["marker"] else [])
        props = {
            "name": r["name_de"],
            "barriere_code": c,
            "name_en": r["name_en"],
            "definition_de": r["definition_de"],
            "review_run": REVIEW_RUN,
            "source_titles": SOURCE_TITLES,
            "source_urls": SOURCE_URLS,
        }
        nodes.append({"record_type": "node", "id": m["id"], "labels": labels, "properties": props})
        p = parent_code(c)
        if p is not None:
            cid, pid = m["id"], meta[p]["id"]
            rels.append({
                "record_type": "rel",
                "id": f"r_{cid}__HAT_HUERDEKATEGORIE__{pid}",
                "from": cid, "type": "HAT_HUERDEKATEGORIE", "to": pid,
                "properties": {"review_run": REVIEW_RUN, "evidence_basis": "taxonomie_struktur"},
            })

    # merged source tsv
    with open(HERE / "taxonomy_source.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("code\tname_de\tname_en\tdefinition_de\n")
        for r in rows:
            f.write(f"{r['code']}\t{r['name_de']}\t{r['name_en']}\t{r['definition_de']}\n")

    with open(HERE / "taxonomy_de.kg.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for rec in nodes + rels:
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

    with open(HERE / "code_id_map.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["code", "id", "label", "is_leaf", "marker"])
        for r in rows:
            m = meta[r["code"]]
            w.writerow([r["code"], m["id"], m["primary"], m["is_leaf"], m["marker"]])

    n_leaf = sum(1 for c in codes if meta[c]["is_leaf"])
    n_cat = len(codes) - n_leaf
    n_marked = sum(1 for c in codes if meta[c]["marker"])
    print("[OK] taxonomy built")
    print(f"     nodes total : {len(nodes)}  (domains 8, categories {n_cat}, leaves {n_leaf})")
    print(f"     :BarriereReferenz marked : {n_marked} (all framework nodes)")
    print(f"     hierarchy edges : {len(rels)}")
    print("     family anchor ids (observed hurdles classify here):")
    for ac in EXPECTED_ANCHOR_CODES:
        print(f"       {ac:5s} -> {meta[ac]['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
