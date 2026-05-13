"""Fold CSV `relation` tokens from clean_confirmed_edges.csv onto the five Neo4j rel types (plan §7.1).

Normative: `.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md` §7, §7.1, Appendix F/G.
"""

from __future__ import annotations

from ort_geo_label import neo4j_label_for_ort_id

# Exact Neo4j relationship type spellings (Unicode Ö in GEHÖRT_ZU).
NEO4J_REL_TYPES: frozenset[str] = frozenset(
    {"IST", "HAT", "BENUTZT", "GEHÖRT_ZU", "BELEGT_IN"}
)

# No graph edge (plan §7.1 drops / tooltyp property / datenmodell nodes).
# Appendix F: `located_in_ort` → GEHÖRT_ZU {rolle: land|stadt} only when the CSV source is
# fallstudie, projekt, or bauobjekt (Neo4j :Fallbeispiel / :Bauwerk after inventory mapping).
_LOCATED_IN_ORT_SOURCE_ENTITIES: frozenset[str] = frozenset(
    {"fallstudie", "projekt", "bauobjekt"}
)

SKIP_RELATIONS: frozenset[str] = frozenset(
    {
        "has_tooltyp",
        "has_projekt",
        "has_bauobjekt",
        "has_bauobjektklasse",
        "has_bauobjektrolle",
        "has_tragwerkstyp",
        "has_dokumenttyp",
        "measured_on_bauobjekt",
        "measures_kennwertdefinition",
        "involves_akteur",
        "has_datenmodell",
        "has_akteurrolle",
        "relates_to_bauobjekt",
    }
)


def fold_csv_relation(row: dict[str, str]) -> tuple[str | None, dict[str, str]]:
    """
    Map one CSV edge row to (neo4j_rel_type, extra_edge_props).

    `extra_edge_props` is merged on top of `row_to_rel_props` from the importer.
    Return (None, {}) to skip the edge entirely.
    """
    rel = (row.get("relation") or "").strip()
    if rel in SKIP_RELATIONS:
        return None, {}

    extra: dict[str, str] = {"csv_relation": rel}

    # --- IST (taxonomy on case / building / component / actors / …) ---
    if rel in {
        "has_bauteiltyp",
        "has_datenqualitaet",
        "has_bauteilebene",
        "has_bauteilzustand",
        "has_funktionswechsel",
        "has_bauweise",
        "has_bausystem",
        "has_tragwerksprinzip",
        "has_zertifizierung_bewertungssystem",
        "has_beschaffungsweg",
        "has_leistungsanforderung",
    }:
        return "IST", extra

    if rel == "has_bewertungslogik_abgrenzung":
        extra["axis"] = "einordnung"
        return "IST", extra

    if rel == "references_norm":
        extra["art"] = "norm"
        return "HAT", extra

    if rel == "has_entwurfsentscheidung":
        extra["art"] = "entwurf"
        return "HAT", extra

    # --- HAT (lifecycle :Status — same rel type as other HAT facets; plan §7 uses art "status") ---
    if rel in {"has_reuse_einsatzstatus", "has_bauobjektstatus"}:
        extra["art"] = "status"
        return "HAT", extra

    # --- BENUTZT ---
    if rel in {"uses_material", "uses_software_digitaltool", "has_methode", "has_rueckbauverfahren", "has_aufbereitungsverfahren"}:
        return "BENUTZT", extra

    # --- HAT (Appendix G `art` values; lifecycle `status` handled above) ---
    if rel == "has_reuse_strategie":
        extra["art"] = "wiederverwendungsart"
        extra["axis"] = "reuse_strategie"
        return "HAT", extra
    if rel == "has_huerde":
        extra["art"] = "huerde"
        return "HAT", extra
    if rel == "has_rechtliche_bedingung":
        extra["art"] = "recht"
        return "HAT", extra
    if rel == "has_logistik":
        extra["art"] = "logistik"
        return "HAT", extra
    if rel == "has_ressourcenquelle":
        extra["art"] = "ressourcenquelle"
        return "HAT", extra
    if rel == "has_wirtschaft":
        extra["art"] = "wirtschaft"
        return "HAT", extra
    if rel == "has_prozessphase":
        extra["art"] = "prozessphase"
        return "HAT", extra
    if rel == "has_nutzung":
        extra["art"] = "nutzung"
        return "HAT", extra
    if rel == "has_bauaufgabe_intervention":
        extra["art"] = "intervention"
        return "HAT", extra
    if rel == "has_pruefung_nachweis":
        extra["art"] = "pruefung"
        return "HAT", extra
    if rel == "has_schadstoff":
        extra["art"] = "schadstoff"
        return "HAT", extra
    if rel == "has_fuegung_verbindung":
        extra["art"] = "verbindungstechnik"
        return "HAT", extra
    if rel == "has_kontextmerkmal":
        extra["art"] = "kontextmerkmal"
        return "HAT", extra

    # --- GEHÖRT_ZU (Appendix F + case-anchor rows from §7.1) ---
    if rel in {"belongs_to_fallstudie", "belongs_to_projekt"}:
        extra["rolle"] = "fallbeispiel"
        return "GEHÖRT_ZU", extra

    if rel == "installed_in_bauobjekt":
        extra["rolle"] = "einbauort"
        return "GEHÖRT_ZU", extra

    if rel == "part_of_reuse_kette":
        extra["rolle"] = "kette"
        return "GEHÖRT_ZU", extra

    if rel == "located_in_ort":
        src_ent = (row.get("source_entity") or "").strip()
        if src_ent not in _LOCATED_IN_ORT_SOURCE_ENTITIES:
            return None, {}
        geo = neo4j_label_for_ort_id(row.get("target_id", "").strip())
        extra["rolle"] = geo.lower()  # `land` | `stadt` per Appendix F
        return "GEHÖRT_ZU", extra

    # --- Appendix F: Fallbeispiel → Programm (foerderprogramm/ + programm_kontext/ → :Programm) ---
    if rel in {"involves_foerderprogramm", "has_programm_kontext"}:
        extra["rolle"] = "programm"
        return "GEHÖRT_ZU", extra

    if rel == "documented_in_quelle":
        return "BELEGT_IN", extra

    # --- Unknown / not yet folded: skip (safer than inventing semantics) ---
    return None, {}
