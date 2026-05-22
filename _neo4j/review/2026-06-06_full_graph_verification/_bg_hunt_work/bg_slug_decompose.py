"""Decompose bg_* slugs into material, component, project anchor tokens."""

from __future__ import annotations

import json
import re
from pathlib import Path

ALIAS_TABLES = json.loads(
    (Path(__file__).resolve().parent / "alias_tables.json").read_text(encoding="utf-8")
)

STOPWORDS = {
    "reused", "candidate", "external", "core", "elements", "batch", "mehrere",
    "and", "the", "for", "from", "with", "do", "doors", "partitions", "tiles",
    "floor", "slabs", "brick", "bricks", "profiles", "shelves", "lights", "trays",
    "builtins", "fixed", "wc", "cable", "roof", "wall", "facade", "fassade",
}

COMPONENT_HINTS = set(ALIAS_TABLES["component"].keys()) | {
    "boden", "wand", "fassade", "gelaender", "dach", "fenster", "decke", "tuer",
    "treppe", "ausbau", "technik", "fundament", "daemmung", "fenster",
}


def decompose_bg_id(bg_id: str, bg_name: str = "") -> dict:
    """Parse bg_* id per BAUTEILGRUPPE_EVIDENCE_HUNTING_PLAN §2.1."""
    tokens = bg_id.replace("bg_", "").split("_")
    material_token = tokens[0] if tokens else ""
    component_tokens: list[str] = []
    project_anchor = ""
    detail_tokens: list[str] = []

    if len(tokens) >= 2 and tokens[1] == "mehrere":
        # bg_{material}_mehrere_{project...}_{detail...}
        detail_start = 2
        if detail_start < len(tokens) and tokens[detail_start] != "mehrere":
            # project anchor: next 1-2 tokens until detail English tokens
            rest = tokens[detail_start:]
            proj_parts: list[str] = []
            detail_parts: list[str] = []
            for i, t in enumerate(rest):
                if t in COMPONENT_HINTS and not proj_parts:
                    detail_parts = rest[i:]
                    break
                if len(proj_parts) >= 2 and t not in STOPWORDS and len(t) >= 4:
                    detail_parts = rest[i:]
                    break
                proj_parts.append(t)
            if proj_parts and not detail_parts:
                if len(proj_parts) >= 2:
                    project_anchor = "_".join(proj_parts[:2])
                    detail_parts = proj_parts[2:] + rest[len(proj_parts):]
                else:
                    project_anchor = proj_parts[0]
                    detail_parts = rest[1:]
            elif proj_parts:
                project_anchor = "_".join(proj_parts[:2]) if len(proj_parts) >= 2 else proj_parts[0]
            detail_tokens = [t for t in detail_parts if t not in STOPWORDS and len(t) >= 3]
    elif len(tokens) >= 3:
        # bg_{material}_{component}_{project...}
        comp = tokens[1]
        if comp in COMPONENT_HINTS or comp != "mehrere":
            component_tokens.append(comp)
        project_anchor = tokens[2] if len(tokens) > 2 else ""
        detail_tokens = [t for t in tokens[3:] if t not in STOPWORDS and len(t) >= 3]
    else:
        detail_tokens = [t for t in tokens[1:] if t not in STOPWORDS]

    # infer component from detail tokens / name
    for t in detail_tokens + tokens:
        if t in COMPONENT_HINTS and t not in component_tokens:
            component_tokens.append(t)
    if bg_name:
        name_lower = bg_name.lower()
        for hint in COMPONENT_HINTS:
            aliases = []
            for lang in ALIAS_TABLES["component"].get(hint, {}).values():
                aliases.extend(lang)
            if hint.replace("_", " ") in name_lower or any(a.lower() in name_lower for a in aliases[:3]):
                if hint not in component_tokens:
                    component_tokens.append(hint)

    # material aliases
    material_aliases: list[str] = []
    mat_table = ALIAS_TABLES["material"].get(material_token, {})
    for lang_aliases in mat_table.values():
        material_aliases.extend(lang_aliases)
    material_aliases.append(material_token)

    comp_aliases: list[str] = []
    for ct in component_tokens:
        ct_table = ALIAS_TABLES["component"].get(ct, {})
        for lang_aliases in ct_table.values():
            comp_aliases.extend(lang_aliases)
        comp_aliases.append(ct)
    comp_aliases.extend(detail_tokens)

    projekt_id_guess = f"p_{project_anchor}" if project_anchor and not project_anchor.startswith("p_") else project_anchor
    if project_anchor and "_" in project_anchor:
        projekt_id_guess = f"p_{project_anchor}"

    return {
        "bg_id": bg_id,
        "material_token": material_token,
        "component_tokens": list(dict.fromkeys(component_tokens + detail_tokens[:6])),
        "project_anchor": project_anchor,
        "projekt_id_guess": projekt_id_guess,
        "detail_tokens": detail_tokens,
        "material_aliases": list(dict.fromkeys(material_aliases)),
        "component_aliases": list(dict.fromkeys(comp_aliases)),
    }


def project_aliases_from_geo(projekt_id: str, projekt_name: str, geo_index: dict) -> list[str]:
    aliases: list[str] = []
    if projekt_name:
        aliases.append(projekt_name)
        for part in re.split(r"[\s_/()-]+", projekt_name):
            if len(part) >= 3:
                aliases.append(part)
    if projekt_id:
        aliases.append(projekt_id.replace("p_", "").replace("_", " "))
        for part in projekt_id.replace("p_", "").split("_"):
            if len(part) >= 4:
                aliases.append(part)
    geo = geo_index.get(projekt_id) or {}
    for loc in geo.get("locations", []):
        for field in ("linked_projekt_name", "address", "source"):
            val = loc.get(field, "")
            if val and isinstance(val, str):
                aliases.append(val)
                for part in re.split(r"[\s,]+", val):
                    if len(part) >= 4:
                        aliases.append(part)
    return list(dict.fromkeys(a for a in aliases if a))


if __name__ == "__main__":
    samples = [
        "bg_keramik_mehrere_maison_vignette_terracotta_floor_tiles",
        "bg_stahl_gelaender_verbiest_charleroi",
        "bg_ziegel_fassade_maison_vignette_reused_facing_bricks",
    ]
    for s in samples:
        print(json.dumps(decompose_bg_id(s), ensure_ascii=False, indent=2))
