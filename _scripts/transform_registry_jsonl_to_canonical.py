"""Transform actor-registry JSONL batches to canonical Neo4j import format.

Transformation rules
--------------------
Labels:
  All actors stay ["Akteur"] — no Person label conversion.
  Person type is conveyed by HAT_AKTEURTYP → at_person on the edge.

Relationship types:
  HAT_AKTEURTYP              →  keep; remap 'to' ID via AKTEURTYP_REMAP
  HAT_AKTEURROLLE            →  keep; remap 'to' ID via AKTEURROLLE_REMAP
  VERBUNDEN_MIT_AKTEUR       →  pass through unchanged
  ASSOZIIERT_MIT_PROJEKT     →  pass through unchanged
  LIEGT_IN_LAND              →  GEHÖRT_ZU { rolle: 'land' }
  ZITIERT_QUELLE             →  BELEGT_IN
  BELEGT_IN                  →  unchanged

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
# Vocab remap tables (mirrored from _scripts/remap_akteur_vocab.py)
# ---------------------------------------------------------------------------
_AKTEURTYP_REMAP: dict[str, str] = {
    "at_person":                         "at_person",
    "at_organisation":                   "at_organisation",
    "at_unternehmen":                    "at_unternehmen",
    "at_oeffentliche_institution":       "at_oeffentliche_institution",
    "at_forschung_lehre":                "at_forschung_lehre",
    "at_ngo_verband_netzwerk":           "at_ngo_verband_netzwerk",
    "at_materialhub_bauteilboerse":      "at_materialhub_bauteilboerse",
    "at_foerdergeber_programmtraeger":   "at_foerdergeber_programmtraeger",
    "at_software_tool_anbieter":         "at_software_tool_anbieter",
    "at_unbekannt":                      "at_unbekannt",
    # remaps
    "at_ngo_netzwerk":                   "at_ngo_verband_netzwerk",
    "at_verband_kammer":                 "at_ngo_verband_netzwerk",
    "at_architekturburo":                "at_unternehmen",
    "at_ingenieurburo":                  "at_unternehmen",
    "at_bauunternehmen":                 "at_unternehmen",
    "at_rueckbauunternehmen":            "at_unternehmen",
    "at_materiallieferant_hersteller":   "at_unternehmen",
    "at_reuse_consultancy_zirkularitaet":"at_unternehmen",
    "at_developer_immobilien":           "at_unternehmen",
    "at_wohnungsbau_genossenschaft":     "at_organisation",
    "at_universitaet_forschungsinstitut":"at_forschung_lehre",
    "at_kultur_bildung_ausstellung":     "at_organisation",
    "at_betreiber_nutzerorganisation":   "at_organisation",
    "at_zertifizierer_pruefstelle":      "at_organisation",
}

_AKTEURROLLE_REMAP: dict[str, str] = {
    "ar_architektur":                           "ar_entwurf_planung",
    "ar_fassade":                               "ar_entwurf_planung",
    "ar_kunst_gestaltung":                      "ar_entwurf_planung",
    "ar_landschaftsplanung":                    "ar_entwurf_planung",
    "ar_entwurf_bauende_praxis":                "ar_entwurf_planung",
    "ar_tragwerksplanung":                      "ar_fachplanung_nachweis",
    "ar_pruefung_qualitaetssicherung":          "ar_fachplanung_nachweis",
    "ar_brandschutz_barrierefreiheit":          "ar_fachplanung_nachweis",
    "ar_tga_gebaeudetechnik":                   "ar_fachplanung_nachweis",
    "ar_bauausfuehrung":                        "ar_bauausfuehrung_fertigung",
    "ar_stahlbau_fertigung":                    "ar_bauausfuehrung_fertigung",
    "ar_produkt_bausystementwicklung":          "ar_bauausfuehrung_fertigung",
    "ar_rueckbau_demontage":                    "ar_rueckbau_bauteilernte_logistik",
    "ar_bauteilernte_materialakquise":          "ar_rueckbau_bauteilernte_logistik",
    "ar_logistik_transport":                    "ar_rueckbau_bauteilernte_logistik",
    "ar_materiallieferant":                     "ar_materiallieferung_markt",
    "ar_vermittlung_marktplatz":                "ar_materiallieferung_markt",
    "ar_materialhub_bauteilboerse":             "ar_materiallieferung_markt",
    "ar_bauteilboerse_bauteilernte_markt":      "ar_materiallieferung_markt",
    "ar_aufbereitung_refurbishment":            "ar_aufbereitung_refurbishment",
    "ar_reuse_beratung":                        "ar_reuse_zirkularitaetsberatung",
    "ar_nachhaltigkeitsberatung":               "ar_reuse_zirkularitaetsberatung",
    "ar_zertifizierung_bewertung":              "ar_reuse_zirkularitaetsberatung",
    "ar_konzept_future_reuse_system":           "ar_reuse_zirkularitaetsberatung",
    "ar_forschung_dokumentation":               "ar_forschung_dokumentation",
    "ar_technik_forschung_nachweis":            "ar_forschung_dokumentation",
    "ar_materialpass_digitalisierung":          "ar_software_digitalisierung",
    "ar_software_tool":                         "ar_software_digitalisierung",
    "ar_bauherr_auftraggeber":                  "ar_bauherr_auftraggeber",
    "ar_betreiber_nutzer":                      "ar_betrieb_nutzung",
    "ar_oeffentliche_hand":                     "ar_oeffentliche_hand_foerderung",
    "ar_foerderung_programmsteuerung":          "ar_oeffentliche_hand_foerderung",
    "ar_bildung_wissenstransfer":               "ar_bildung_wissenstransfer",
    "ar_organisation_bildung_wissenstransfer":  "ar_bildung_wissenstransfer",
    "ar_ausstellung_kuration":                  "ar_bildung_wissenstransfer",
    "ar_projektmanagement_koordination":        "ar_projektmanagement_koordination",
    "ar_projektbeteiligte_unbestimmt":          "ar_unbestimmt",
    # new canonical IDs (identity mapping)
    "ar_entwurf_planung":                       "ar_entwurf_planung",
    "ar_fachplanung_nachweis":                  "ar_fachplanung_nachweis",
    "ar_bauausfuehrung_fertigung":              "ar_bauausfuehrung_fertigung",
    "ar_rueckbau_bauteilernte_logistik":        "ar_rueckbau_bauteilernte_logistik",
    "ar_materiallieferung_markt":               "ar_materiallieferung_markt",
    "ar_reuse_zirkularitaetsberatung":          "ar_reuse_zirkularitaetsberatung",
    "ar_oeffentliche_hand_foerderung":          "ar_oeffentliche_hand_foerderung",
    "ar_betrieb_nutzung":                       "ar_betrieb_nutzung",
    "ar_software_digitalisierung":              "ar_software_digitalisierung",
    "ar_unbestimmt":                            "ar_unbestimmt",
}

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
# Node transformation — ID remap only, no label changes
# ---------------------------------------------------------------------------

def _transform_node(rec: dict, id_map: dict[str, str]) -> dict:
    new = dict(rec)
    new["id"] = _canonical_id(rec["id"], id_map)
    return new


# ---------------------------------------------------------------------------
# Relationship transformation
# ---------------------------------------------------------------------------

def _transform_rel(rec: dict, id_map: dict[str, str]) -> dict:
    rel_type = rec["type"]
    from_id = rec["from"]
    to_id = rec["to"]
    props = dict(rec.get("properties") or {})

    new_from = _canonical_id(from_id, id_map)
    new_rel_id = _remap_rel_id(rec["id"], id_map)

    # Vocab remaps: keep rel type, remap target node ID only
    if rel_type == "HAT_AKTEURTYP":
        new_to = _AKTEURTYP_REMAP.get(to_id, to_id)
        return {"record_type": "rel", "id": new_rel_id, "from": new_from,
                "type": rel_type, "to": new_to, "properties": props}

    if rel_type == "HAT_AKTEURROLLE":
        new_to = _AKTEURROLLE_REMAP.get(to_id, to_id)
        return {"record_type": "rel", "id": new_rel_id, "from": new_from,
                "type": rel_type, "to": new_to, "properties": props}

    # Folds
    if rel_type == "LIEGT_IN_LAND":
        new_to = _canonical_id(to_id, id_map)
        return {"record_type": "rel", "id": new_rel_id, "from": new_from,
                "type": "GEHÖRT_ZU", "to": new_to, "properties": {**props, "rolle": "land"}}

    if rel_type == "ZITIERT_QUELLE":
        new_to = _canonical_id(to_id, id_map)
        return {"record_type": "rel", "id": new_rel_id, "from": new_from,
                "type": "BELEGT_IN", "to": new_to, "properties": props}

    # Pass through: VERBUNDEN_MIT_AKTEUR, ASSOZIIERT_MIT_PROJEKT, BELEGT_IN, others
    new_to = _canonical_id(to_id, id_map)
    return {"record_type": "rel", "id": new_rel_id, "from": new_from,
            "type": rel_type, "to": new_to, "properties": props}


# ---------------------------------------------------------------------------
# File-level transform
# ---------------------------------------------------------------------------

def transform(input_path: Path, output_path: Path, id_map: dict[str, str]) -> tuple[int, int]:
    """Transform one registry JSONL file. Returns (nodes_written, rels_written)."""
    lines = input_path.read_text(encoding="utf-8").splitlines()
    records = [json.loads(ln) for ln in lines if ln.strip()]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    nodes_written = rels_written = 0

    with output_path.open("w", encoding="utf-8") as fh:
        for rec in records:
            if rec["record_type"] == "node":
                result = _transform_node(rec, id_map)
            elif rec["record_type"] == "rel":
                result = _transform_rel(rec, id_map)
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
