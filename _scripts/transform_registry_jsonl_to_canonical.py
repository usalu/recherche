"""Transform actor-registry JSONL batches to canonical Neo4j import format.

Transformation rules
--------------------
Labels:
  Akteur + HAT_AKTEURTYP → at_person  →  label becomes ["Person"]; HAT_AKTEURTYP edge dropped
  Akteur + HAT_AKTEURTYP → at_*       →  label stays ["Akteur"]; HAT_AKTEURTYP → IST
  Projekt, Land, Quelle, Akteurrolle  →  unchanged

Relationship types:
  HAT_AKTEURTYP  (org → Akteurtyp)    →  IST
  HAT_AKTEURTYP  (person → at_person) →  DROP
  HAT_AKTEURROLLE                     →  HAT { art: 'akteurrolle', rolle: <to_id> }
  LIEGT_IN_LAND                       →  GEHÖRT_ZU { rolle: 'land' }
  VERBUNDEN_MIT_AKTEUR                →  GEHÖRT_ZU { rolle: 'organisation' }
  ASSOZIIERT_MIT_PROJEKT (needs_verification=true) → DROP
  ZITIERT_QUELLE                      →  BELEGT_IN
  BELEGT_IN                           →  unchanged

IDs:
  Loaded from _neo4j/new/ID_RECONCILIATION.csv if present.
  Hard-coded known collisions applied next.
  Fallback: strip leading 'a_' prefix.

Usage:
  python _scripts/transform_registry_jsonl_to_canonical.py <input.registry.kg.jsonl> [...]

Output:
  _neo4j/new/canonical/<batch_dir>/<stem>.canonical.kg.jsonl
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_REPO = Path(__file__).resolve().parents[1]
_RECON_CSV = _REPO / "_neo4j" / "new" / "ID_RECONCILIATION.csv"

# ---------------------------------------------------------------------------
# Known ID collisions: batch actor ID → canonical research/akteur/ ID
# ---------------------------------------------------------------------------
_KNOWN_COLLISIONS: dict[str, str] = {
    "a_patrick_teuffel": "patrick_teuffel",
    "a_dirk_hebel": "Dirk_Hebel",
    "a_werner_sobek": "Werner_Sobek",
    "a_superuse_studios": "Superuse_Studios",
    "a_natural_building_lab": "Natural_Building_Lab",
    "a_zrs_architekten_ingenieure": "ZRS_Architekten_Ingenieure",
    "a_lendager": "Lendager",
    "a_cityfoerster": "CITYFOERSTER",
    "a_bellastock": "Bellastock",
    "a_rotor": "Rotor",
}

# Regex that matches an 'a_<slug>' segment inside a relationship ID
_A_SLUG_RE = re.compile(r'a_[a-z0-9_]+')


def _load_id_map() -> dict[str, str]:
    """Load optional ID_RECONCILIATION.csv → {batch_id: canonical_id}."""
    if not _RECON_CSV.is_file():
        return {}
    mapping: dict[str, str] = {}
    with _RECON_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            mapping[row["batch_id"]] = row["canonical_id"]
    return mapping


def _canonical_id(batch_id: str, id_map: dict[str, str]) -> str:
    """Resolve a batch node/rel ID to its canonical form."""
    if batch_id in id_map:
        return id_map[batch_id]
    if batch_id in _KNOWN_COLLISIONS:
        return _KNOWN_COLLISIONS[batch_id]
    # Actors new to the graph: strip 'a_' prefix
    if batch_id.startswith("a_"):
        return batch_id[2:]
    return batch_id


def _remap_rel_id(rel_id: str, id_map: dict[str, str]) -> str:
    """Rewrite 'a_<slug>' segments embedded in a relationship ID string."""
    def _replace(m: re.Match) -> str:
        return _canonical_id(m.group(0), id_map)
    return _A_SLUG_RE.sub(_replace, rel_id)


# ---------------------------------------------------------------------------
# Node transformation
# ---------------------------------------------------------------------------

def _transform_node(rec: dict, person_batch_ids: set[str], id_map: dict[str, str]) -> dict:
    new = dict(rec)
    new["id"] = _canonical_id(rec["id"], id_map)
    if rec["id"] in person_batch_ids:
        new["labels"] = ["Person"]
    return new


# ---------------------------------------------------------------------------
# Relationship transformation
# ---------------------------------------------------------------------------

def _transform_rel(
    rec: dict,
    person_batch_ids: set[str],
    id_map: dict[str, str],
) -> dict | None:
    rel_type = rec["type"]
    from_id = rec["from"]
    to_id = rec["to"]
    props = dict(rec.get("properties") or {})

    # --- DROP rules ---
    if rel_type == "HAT_AKTEURTYP" and to_id == "at_person":
        return None  # person type is now encoded in the label
    if rel_type == "ASSOZIIERT_MIT_PROJEKT" and props.get("needs_verification", False):
        return None

    # --- Remap endpoint and rel IDs ---
    new_from = _canonical_id(from_id, id_map)
    new_to = _canonical_id(to_id, id_map)
    new_rel_id = _remap_rel_id(rec["id"], id_map)

    # --- Fold relationship type and properties ---
    if rel_type == "HAT_AKTEURTYP":
        # Org → Akteurtyp: fold to IST (to_id is an Akteurtyp node, keep as-is)
        new_type = "IST"
        new_props = props

    elif rel_type == "HAT_AKTEURROLLE":
        new_type = "HAT"
        new_props = {**props, "art": "akteurrolle", "rolle": to_id}

    elif rel_type == "LIEGT_IN_LAND":
        new_type = "GEHÖRT_ZU"
        new_props = {**props, "rolle": "land"}

    elif rel_type == "VERBUNDEN_MIT_AKTEUR":
        new_type = "GEHÖRT_ZU"
        new_props = {**props, "rolle": "organisation"}

    elif rel_type == "ZITIERT_QUELLE":
        new_type = "BELEGT_IN"
        new_props = props

    else:
        # BELEGT_IN, ASSOZIIERT_MIT_PROJEKT (verified), others → unchanged
        new_type = rel_type
        new_props = props

    return {
        "record_type": "rel",
        "id": new_rel_id,
        "from": new_from,
        "type": new_type,
        "to": new_to,
        "properties": new_props,
    }


# ---------------------------------------------------------------------------
# File-level transform
# ---------------------------------------------------------------------------

def transform(input_path: Path, output_path: Path, id_map: dict[str, str]) -> tuple[int, int]:
    """Transform one registry JSONL file. Returns (nodes_written, rels_written)."""
    lines = input_path.read_text(encoding="utf-8").splitlines()
    records = [json.loads(ln) for ln in lines if ln.strip()]

    # Pass 1: collect batch IDs of person actors
    person_batch_ids: set[str] = {
        rec["from"]
        for rec in records
        if rec["record_type"] == "rel"
        and rec["type"] == "HAT_AKTEURTYP"
        and rec["to"] == "at_person"
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    nodes_written = rels_written = 0

    with output_path.open("w", encoding="utf-8") as fh:
        for rec in records:
            if rec["record_type"] == "node":
                result = _transform_node(rec, person_batch_ids, id_map)
            elif rec["record_type"] == "rel":
                result = _transform_rel(rec, person_batch_ids, id_map)
            else:
                result = rec  # pass through unknown record types

            if result is not None:
                fh.write(json.dumps(result, ensure_ascii=False) + "\n")
                if result["record_type"] == "node":
                    nodes_written += 1
                else:
                    rels_written += 1

    return nodes_written, rels_written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    id_map = _load_id_map()
    base_out = _REPO / "_neo4j" / "new" / "canonical"

    for arg in sys.argv[1:]:
        inp = Path(arg).resolve()
        batch_name = inp.parent.name
        # Remove .registry.kg from stem if present, then add .canonical.kg
        stem = re.sub(r'\.registry\.kg$', '', inp.stem)
        out = base_out / batch_name / f"{stem}.canonical.kg.jsonl"
        nodes, rels = transform(inp, out, id_map)
        rel_out = out.relative_to(_REPO)
        print(f"  {inp.name}")
        print(f"  → {rel_out}")
        print(f"     {nodes} nodes, {rels} rels written")


if __name__ == "__main__":
    main()
