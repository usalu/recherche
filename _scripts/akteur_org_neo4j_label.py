"""Neo4j primary label for `akteur/<id>/` organisations (plan §6.1)."""

from __future__ import annotations

import re
from pathlib import Path

from akteur_person_split import is_person_akteur_folder

# Optional slug aliases (raw token after `akteurtyp/` → canonical slug key).
AKTEURTYP_ALIASES: dict[str, str] = {
    "Professur": "professur",
}

# Canonical slug (after alias pass) → Neo4j label (no `akteurtyp` property on node).
SLUG_TO_LABEL: dict[str, str] = {
    "planung_architektur_ingenieurwesen": "PlanungArchitekturIngenieurwesen",
    "forschung_lehre_wissenstransfer": "ForschungLehreWissenstransfer",
    "oeffentliche_institutionen_foerderung": "OeffentlicheInstitutionenFoerderung",
    "kammern_verbaende_ngos_netzwerke": "KammernVerbaendeNgosNetzwerke",
    "Unternehmerverband_Historische_Baustoffe_UHB_md": "UnternehmerverbandHistorischeBaustoffeUHBMd",
    "materialinitiativen_hubs": "MaterialinitiativenHubs",
    "reuse_beratung_prozessdienstleister": "ReuseBeratungProzessdienstleister",
    "professur": "Professur",
}

_RX = re.compile(r"akteurtyp/([A-Za-z0-9_]+)")


def _first_slug_from_markdown(text: str) -> str | None:
    m = _RX.search(text)
    return m.group(1) if m else None


def neo4j_label_for_akteur_folder(database_root: Path, actor_id: str) -> str:
    """
    Primary Neo4j label for one `akteur/<actor_id>/` inventory row.
    Persons → Person; organisations → §6.1 label or Akteur fallback.
    """
    if is_person_akteur_folder(database_root, actor_id):
        return "Person"
    idx = database_root / "akteur" / actor_id / "index.md"
    if not idx.is_file():
        return "Akteur"
    text = idx.read_text(encoding="utf-8", errors="replace")[:16000]
    raw = _first_slug_from_markdown(text)
    if raw is None:
        return "Akteur"
    if raw in AKTEURTYP_ALIASES:
        slug = AKTEURTYP_ALIASES[raw]
    else:
        slug = raw
    if slug.lower() == "person":
        return "Person"
    return SLUG_TO_LABEL.get(slug, "Akteur")
