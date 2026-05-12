"""`:Software` vs `:Tool` for `software_digitaltool/<id>/` (plan §5.6 illustration sets + default Software)."""

from __future__ import annotations

# Illustration slugs from plan §5.2 `:Software` row (first 20 α).
PLAN_SOFTWARE_EXAMPLES: frozenset[str] = frozenset(
    {
        "Abriss_Atlas",
        "BIM",
        "Bauteilboerse_Bremen",
        "Bauteilboerse_Hannover",
        "Bauteilnetz_Deutschland",
        "Bonsai_BlenderBIM",
        "CMEx",
        "Concular_Plattform",
        "Cycle_Up",
        "Dataview",
        "Excess_Materials_Exchange",
        "GIS_Urban_Mining",
        "Globechain",
        "IFC_Viewer",
        "IfcOpenShell",
        "Klimaschutz_Konfigurator",
        "Library_of_Reuse",
        "Lindner_Group_ReUsed_Products",
        "Loopfront",
        "Maconda_Materialpass",
    }
)

# Illustration slugs from plan §5.2 `:Tool` row (slugs 21–40 α).
PLAN_TOOL_EXAMPLES: frozenset[str] = frozenset(
    {
        "Maconda_ROMULUS",
        "Madaster",
        "Material_Index",
        "Material_Reuse_Portal",
        "One_Click_LCA",
        "One_Click_LCA_Building_Circularity",
        "Opalis",
        "Platform_CB23",
        "Pre_Demolition_Audit_Tools",
        "QR_RFID_Materialtracking",
        "Qflow",
        "Restado",
        "Reusefully_LINK",
        "Rheaply",
        "Rhino",
        "RotorDB",
        "RotorDC",
        "SalvoWEB",
        "Speckle",
        "Superyard",
    }
)


def neo4j_label_for_software_digitaltool_id(sid: str) -> str:
    """Prefer explicit plan illustration sets; unknown corpus slugs default to Software."""
    if sid in PLAN_TOOL_EXAMPLES:
        return "Tool"
    if sid in PLAN_SOFTWARE_EXAMPLES:
        return "Software"
    # Heuristic: small artefacts / CAD / calculators often named like tools
    low = sid.lower()
    if any(
        x in low
        for x in (
            "rhino",
            "revit",
            "excel",
            "grasshopper",
            "script",
            "plug",
            "lca",
            "speckle",
            "qgis",
        )
    ):
        return "Tool"
    return "Software"
