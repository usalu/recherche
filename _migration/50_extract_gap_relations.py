#!/usr/bin/env python3
"""
50_extract_gap_relations.py - Promote selected gap relations from Gebaeude tables.

This script is intentionally batch-oriented. Each batch should be small enough
to inspect in a diff report before committing.

Current batch:
  50a_reuse_strategie
    Reads the explicit "Reuse-Strategie" rows in the Gebaeude Entitaeten-
    Mapping tables and adds has_reuse_strategie edges from concrete
    reuse_einsatz nodes to the existing Direkte_Wiederverwendung knot.
  50b_fuegung_verbindung
    Reads the "Verbindung" row text already promoted into reuse_einsatz
    index.md files and adds high-precision has_fuegung_verbindung edges.
  50c_reuse_einsatzstatus
    Reads the case-level "Projektstatus" bullet and adds one conservative
    has_reuse_einsatzstatus edge to substantive reuse_einsatz nodes.
  50d_prozessphase
    Reads the promoted "Eingriff/Aufbereitung" label and adds broad
    process-phase edges such as Rueckbau, Aufbereitung, and Wiedereinbau.
  50e_rueckbauverfahren
    Reads the same component-level label and adds precise
    has_rueckbauverfahren edges for named dismantling methods.
  50f_located_in_ort
    Reads the "Ort" row from each Gebaeude Entitaeten-Mapping table,
    derives a canonical city slug, creates the ort node folder + index.md
    if it doesn't yet exist, and emits one fallstudie -> located_in_ort
    -> ort edge per case. Bad/non-location Ort values are skipped.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "_database"
EDGES = DATABASE / "_edges" / "clean_confirmed_edges.csv"
NODE_INVENTORY = DATABASE / "_system" / "node_inventory.csv"
REPORT_DIR = ROOT / "_migration"

EDGE_COLUMNS = [
    "source", "source_entity", "source_id",
    "relation", "target", "target_entity", "target_id",
    "field", "raw_label", "confidence", "resolution_rule",
    "legacy_path", "original_source", "original_relation", "original_target",
    "edge_cleaning",
]

UNCERTAIN_VALUES = {
    "", "-", "--", "---", "?", "unbekannt", "unklar", "keine quelle",
    "nicht zutreffend", "n/a", "keine", "\u2014",
}

EXCLUSION_TOKENS = (
    "keine wiederverwendung",
    "keine reuse",
    "nicht belegt",
    "nicht ausreichend belegt",
    "nicht als reuse belegt",
    "nicht als wiederverwendung belegt",
    "nicht als direct reuse",
    "nicht reuse",
    "zaehlt nicht als reuse",
    "zahlt nicht als reuse",
    "direct reuse zaehlen",
    "direct reuse zahlen",
    "nicht direct reuse",
    "kein direct reuse",
    "nicht gezahlt",
    "nicht gezaehlt",
    "nicht gezaehlt",
    "nicht zaehlen",
    "nicht zahlen",
    "nicht wiederverwendet",
    "nicht teil der reuse-bewertung",
    "nicht score",
    "nicht als score",
    "score-relevant",
    "neues projekt",
    "neu, nicht",
    "tatsaechlich neu",
    "tatsachlich neu",
    "vermutlich neu",
    "keine belege",
    "materialexperiment",
    "neu / zementreduziert",
    "neu/vermutlich",
    "zementreduziert",
    "recycling, nicht reuse",
    "recyclingmaterial",
    "zerkleinert",
    "grober zuschlag",
    "zuschlag",
    "ausserhalb reuse-fokus",
    "ausserhalb reuse fokus",
    "reused? nein",
    "keine quelle",
)

NEW_SOURCE_TOKENS = (
    "neu",
    "neubau",
    "neubau/refurbishment",
    "neu ergaenzt",
    "neu gefertigt",
    "neu / unbekannt",
    "neu/unklar",
)

POSITIVE_SOURCE_TOKENS = (
    "reuse",
    "re-use",
    "wiederverwend",
    "reclaimed",
    "salvaged",
    "second-hand",
    "second hand",
    "gebraucht",
    "geliehen",
    "rotor",
    "rueckbau",
    "ruckbau",
    "bestand",
    "vor ort gefunden",
)

DIRECT_STRATEGY_TOKENS = (
    "direct reuse",
    "direkte wiederverwendung",
    "bauteilwiederverwendung",
    "bauteil-/produktwiederverwendung",
    "bauteil- und materialwiederverwendung",
    "material- und bauteilwiederverwendung",
    "materialwiederverwendung",
    "wiederverwendung von",
    "wiederverwendete",
    "wiederverwend",
    "ex-situ",
    "ex situ",
    "gebaudeversetzung",
    "remontage",
    "salvaged",
    "reclaimed",
    "second-hand",
    "second hand",
    "re-use",
    "reuse von",
    "reuse-first",
    "structural reuse",
    "steel reuse",
    "self-reuse",
    "on-site reuse",
    "on site reuse",
    "on-site selective deconstruction and reuse",
    "donorskelet",
    "material harvesting",
    "oogsten",
    "geerntet",
    "rueckbau",
    "ruckbau",
    "spolia",
    "reemploi",
    "bauteilsuche",
    "entwurf aus verfugbarkeit",
    "superuse",
    "reuse-pilot",
    "re-use-pilot",
    "borrowed building",
    "circular building site",
)

SUBSTANTIVE_FRONTMATTER_KEYS = (
    "material_label",
    "herkunft_label",
    "alte_funktion",
    "menge_umfang",
)

NON_DIRECT_ABGRENZUNG_TARGETS = (
    "bewertungslogik_abgrenzung/Bestandserhalt_Nicht_Direct_Reuse",
    "bewertungslogik_abgrenzung/Kein_Direct_Reuse_Nachweis",
    "bewertungslogik_abgrenzung/Moebel_Dekoration_Nicht_Direct_Reuse",
    "bewertungslogik_abgrenzung/Recycling_Nicht_Direct_Reuse",
    "bewertungslogik_abgrenzung/Reuse_Anteil_Unklar",
    "bewertungslogik_abgrenzung/Ungebaut_Nicht_Realisierte_Wiederverwendung",
    "bewertungslogik_abgrenzung/Zukunftsfaehigkeit_Nicht_Aktuelle_Wiederverwendung",
)

CONNECTION_UNCERTAIN_TOKENS = (
    "unbekannt",
    "nicht relevant",
    "nicht zutreffend",
    "n/a",
    "entfallt",
    "entfaellt",
    "details unbekannt",
    "vermutet",
    "vermutlich",
    "geplant",
    "genaue details",
    "beschlage unbekannt",
    "einbau unbekannt",
    "mortel/kleber unbekannt",
    "moertel/kleber unbekannt",
    "mortel unbekannt",
    "moertel unbekannt",
    "kleber unbekannt",
    "standardanschlusse",
    "future reuse",
)

CONNECTION_RULES = [
    (
        "fuegung_verbindung/Verschraubung",
        (
            "geschraubt",
            "verschraubt",
            "schrauben",
            "schraub-",
            "schraub/",
            "bolzen",
            "dubel",
            "flansch",
            "flansche",
        ),
    ),
    (
        "fuegung_verbindung/Verschweissung",
        (
            "schweiss",
            "geschweisst",
            "verschweisst",
        ),
    ),
    (
        "fuegung_verbindung/Verleimung",
        (
            "kleber",
            "geklebt",
            "verklebt",
            "leim",
            "verleim",
        ),
    ),
    (
        "fuegung_verbindung/Vermoertelung",
        (
            "mortel",
            "moertel",
            "kalkmortel",
            "kalkmoertel",
            "mauerwerk",
            "mauerverband",
            "ziegelverband",
            "ziegelschicht",
            "vermortel",
            "vermoertel",
        ),
    ),
    (
        "fuegung_verbindung/Steckverbindung",
        (
            "steck",
            "stabdubel",
            "buchenholzdubel",
            "dubel",
        ),
    ),
    (
        "fuegung_verbindung/Klemmverbindung",
        (
            "klemm",
            "spannband",
            "spannbander",
            "umreifungsband",
            "kabelbinder",
        ),
    ),
    (
        "fuegung_verbindung/Reversible_Fuegung",
        (
            "demontierbar",
            "losbar",
            "loesbar",
            "reversibel",
            "reversible",
            "kit-of-parts",
            "trockenmauer",
        ),
    ),
]

STATUS_TARGETS = {
    "Realisiert": "reuse_einsatzstatus/Realisiert",
    "Geplant": "reuse_einsatzstatus/Geplant",
    "Verworfen": "reuse_einsatzstatus/Verworfen",
    "Vorgeschlagen": "reuse_einsatzstatus/Vorgeschlagen",
    "Unklar": "reuse_einsatzstatus/Unklar",
    "Temporaer": "reuse_einsatzstatus/Temporaer",
    "Prototypisch": "reuse_einsatzstatus/Prototypisch",
}

STATUS_DISCARDED_TOKENS = (
    "aborted",
    "ungebaut",
    "ersetzt",
    "nicht gebaut",
    "abgebrochen",
    "projektabbruch",
    "gestoppt",
)

STATUS_TEMPORARY_TOKENS = (
    "temporar",
    "temporaer",
    "demontiert",
    "mobil",
)

STATUS_PROTOTYPE_TOKENS = (
    "prototyp",
    "demonstrator",
    "forschungsdemonstrator",
    "mini-pilot",
    "mock-up",
    "mockup",
)

STATUS_REALIZED_TOKENS = (
    "gebaut",
    "fertiggestellt",
    "completed",
    "brought online",
    "eroffnet",
    "wiedereroffnung",
    "bezogen",
    "in nutzung",
    "abgeschlossen",
    "eingebaut",
    "umgesetzt",
    "practical completion",
    "geliefert",
    "transloziert",
)

STATUS_PLANNED_TOKENS = (
    "geplant",
    "in entwicklung",
    "im bau",
    "ausfuhrung vorgesehen",
    "angekundigt",
    "scheduled",
    "expected",
    "construction",
    "on site",
    "live-projekt",
    "live",
)

STATUS_PROPOSED_TOKENS = (
    "proposal",
    "vorschlag",
    "vorgeschlagen",
    "konzept",
)

STATUS_MEDIUM_CONFIDENCE_TOKENS = (
    "unbekannt",
    "zu verifizieren",
    "vorgesehen",
    "angekundigt",
    "expected",
    "scheduled",
    "laut",
    "bzw",
)

PROCESS_PHASE_RULES = [
    (
        "prozessphase/Rueckbau",
        (
            "demontage",
            "demontiert",
            "ausbau",
            "ruckbau",
            "rueckbau",
            "abbau",
            "ernte",
            "ruckgewinnung",
            "rueckgewinnung",
            "ruckgewonnen",
            "rueckgewonnen",
            "zuruckgewonnen",
            "zurueckgewonnen",
            "geborgen",
            "ausgebaut",
        ),
    ),
    (
        "prozessphase/Transport",
        (
            "transport",
            "transportiert",
            "trailer",
        ),
    ),
    (
        "prozessphase/Lagerung",
        (
            "lagerung",
            "einlagerung",
            "stockpile",
            "zwischengelager",
        ),
    ),
    (
        "prozessphase/Identifikation",
        (
            "katalogisierung",
            "katalog",
            "auswahl",
            "erfassung",
            "identifikation",
            "sortierung",
            "sortieren",
        ),
    ),
    (
        "prozessphase/Aufbereitung",
        (
            "reinigung",
            "reinigen",
            "gereinigt",
            "aufbereitung",
            "anpassung",
            "zuschnitt",
            "zuschneiden",
            "sagen",
            "saegen",
            "gesagt",
            "gesaegt",
            "reparatur",
            "instandsetzung",
            "restaurierung",
            "beschichtung",
            "lackierung",
            "behandlung",
            "remanufacturing",
            "re-fabrication",
            "refabrication",
            "bearbeitung",
            "vorbereitung",
            "vorbereitet",
            "aufgearbeitet",
            "umfunktioniert",
            "umnutzung",
            "reaktivierung",
            "locher gefullt",
            "loecher gefuellt",
            "hot-cut",
            "casings entfernt",
            "sichten",
            "einfullen",
            "einfuellen",
            "verarbeitung",
            "ersetzt",
            "einpassung",
            "verstarkung",
            "verdopplung",
            "primerentfernung",
        ),
    ),
    (
        "prozessphase/Pruefung",
        (
            "getestet",
            "test",
            "tests",
            "rezertifizierung",
            "re-zertifizierung",
            "zertifiziert",
            "funktionsprufung",
            "funktionspruefung",
            "prufung",
            "pruefung",
            "ce markiert",
        ),
    ),
    (
        "prozessphase/Wiedereinbau",
        (
            "wiedereinbau",
            "wiedermontage",
            "montage",
            "einbau",
            "wiederaufbau",
            "wiederaufgebaut",
            "eingebaut",
            "neuverlegung",
            "verlegung",
            "wandmontage",
            "befestigung",
            "vermauerung",
            "integriert",
            "integration",
        ),
    ),
]

PROCESS_SKIP_SEGMENT_TOKENS = (
    "unbekannt",
    "nicht bewertet",
    "nicht detailliert",
    "keine",
    "neu/restposten",
    "neu restposten",
    "as found",
    "largely as found",
)

PROCESS_MEDIUM_CONFIDENCE_TOKENS = (
    "unbekannt",
    "geplant",
    "wahrscheinlich",
    "ggf",
    "moglich",
    "moeglich",
    "nicht detailliert",
    "details unbekannt",
)

def normalized(value: str) -> str:
    value = value or ""
    value = value.replace("\u00df", "ss").replace("\u00f8", "o").replace("\u00d8", "O")
    value = value.replace("\u00e6", "ae").replace("\u00c6", "AE")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    return re.sub(r"\s+", " ", value).strip()


def get_cell(row: dict[str, str], wanted_key: str) -> str:
    wanted = normalized(wanted_key)
    for key, value in row.items():
        if normalized(key) == wanted:
            return (value or "").strip()
    return ""


def gebaeude_dir() -> Path:
    candidates = [
        path for path in ROOT.iterdir()
        if path.is_dir() and path.name.startswith("Geb") and path.name != "gebaeude"
    ]
    if not candidates:
        raise FileNotFoundError("Could not find the Gebaeude/Gebaeude-with-umlaut source directory")
    return sorted(candidates, key=lambda path: path.name)[0]


def markdown_section(markdown: str, heading_keyword: str) -> str:
    lines = markdown.splitlines()
    keyword = normalized(heading_keyword)
    start = None
    for idx, line in enumerate(lines):
        if line.startswith("##") and keyword in normalized(line):
            start = idx + 1
            break
    if start is None:
        return ""

    end = len(lines)
    for idx in range(start, len(lines)):
        if lines[idx].startswith("## "):
            end = idx
            break
    return "\n".join(lines[start:end])


def split_markdown_table_row(line: str) -> list[str]:
    # The source tables do not use escaped pipes. Keep this parser deliberately
    # simple and transparent for review.
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_markdown_tables(section: str) -> list[dict[str, str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in section.splitlines():
        if line.strip().startswith("|"):
            current.append(line)
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)

    rows: list[dict[str, str]] = []
    for lines in blocks:
        if len(lines) < 2:
            continue
        headers = split_markdown_table_row(lines[0])
        separator = split_markdown_table_row(lines[1])
        has_separator = all(set(cell.strip()) <= set("-:") for cell in separator)
        data_lines = lines[2:] if has_separator else lines[1:]
        for line in data_lines:
            cells = split_markdown_table_row(line)
            if len(cells) < len(headers):
                cells.extend([""] * (len(headers) - len(cells)))
            rows.append(dict(zip(headers, cells[:len(headers)])))
    return rows


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_edges(rows: list[dict[str, str]]) -> None:
    tmp = EDGES.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=EDGE_COLUMNS,
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in EDGE_COLUMNS})
    tmp.replace(EDGES)


def load_existing_nodes() -> set[str]:
    nodes = set()
    for row in load_csv(NODE_INVENTORY):
        nodes.add(row["typed_path"])
    return nodes


def load_reuse_nodes() -> dict[str, list[dict[str, str]]]:
    rows_by_case: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in load_csv(NODE_INVENTORY):
        if row["entity"] != "reuse_einsatz":
            continue
        case_id = row["id"].split("__", 1)[0]
        rows_by_case[case_id].append(row)
    return rows_by_case


def parse_simple_frontmatter(markdown: str) -> dict[str, str]:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def load_reuse_frontmatter(node_row: dict[str, str]) -> dict[str, str]:
    index_path = ROOT / node_row["markdown_path"]
    if not index_path.exists():
        return {}
    return parse_simple_frontmatter(index_path.read_text(encoding="utf-8", errors="replace"))


def load_reuse_markdown(node_row: dict[str, str]) -> str:
    index_path = ROOT / node_row["markdown_path"]
    if not index_path.exists():
        return ""
    return index_path.read_text(encoding="utf-8", errors="replace")


def extract_markdown_bullet(markdown: str, label: str) -> str:
    pattern = re.compile(rf"^- \*\*{re.escape(label)}:\*\*\s*(.*)$", flags=re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return ""
    return match.group(1).strip()


def extract_strategy_rows() -> dict[str, dict[str, str]]:
    source_dir = gebaeude_dir()
    strategy_rows: dict[str, dict[str, str]] = {}
    for path in sorted(source_dir.glob("*.md")):
        markdown = path.read_text(encoding="utf-8", errors="replace")
        section = markdown_section(markdown, "ENTIT")
        for row in parse_markdown_tables(section):
            entity = get_cell(row, "Entitat")
            if "reuse" in normalized(entity) and "strategie" in normalized(entity):
                strategy_rows[path.stem] = {
                    "case_id": path.stem,
                    "legacy_path": str(path.relative_to(ROOT)),
                    "value": get_cell(row, "Wert"),
                    "relationship": get_cell(row, "Beziehung zur Fallstudie"),
                    "confidence_source": get_cell(row, "Vertrauensgrad"),
                    "note": get_cell(row, "Anmerkung"),
                }
                break
    return strategy_rows


def extract_project_status_rows() -> dict[str, dict[str, str]]:
    source_dir = gebaeude_dir()
    status_rows: dict[str, dict[str, str]] = {}
    for path in sorted(source_dir.glob("*.md")):
        markdown = path.read_text(encoding="utf-8", errors="replace")
        value = extract_markdown_bullet(markdown, "Projektstatus")
        if not value:
            continue
        status_rows[path.stem] = {
            "case_id": path.stem,
            "legacy_path": str(path.relative_to(ROOT)),
            "value": value,
            "relationship": "",
            "confidence_source": "",
            "note": "",
        }
    return status_rows


def map_strategy_targets(strategy_row: dict[str, str], existing_nodes: set[str]) -> list[str]:
    haystack = normalized(
        " | ".join([
            strategy_row.get("value", ""),
            strategy_row.get("relationship", ""),
            strategy_row.get("note", ""),
        ])
    )
    target = "reuse_strategie/Direkte_Wiederverwendung"
    if target in existing_nodes and any(token in haystack for token in DIRECT_STRATEGY_TOKENS):
        return [target]
    return []


def row_confidence(strategy_row: dict[str, str]) -> str:
    source_confidence = normalized(strategy_row.get("confidence_source", ""))
    if source_confidence == "belegt":
        return "rule_high"
    if "teilweise" in source_confidence:
        return "rule_medium"
    return "rule_low"


def is_uncertain(value: str) -> bool:
    return normalized(value) in UNCERTAIN_VALUES


def reusable_enough(frontmatter: dict[str, str]) -> bool:
    bauteil = normalized(frontmatter.get("bauteil_label", ""))
    material = normalized(frontmatter.get("material_label", ""))
    herkunft = normalized(frontmatter.get("herkunft_label", ""))
    alte_funktion = normalized(frontmatter.get("alte_funktion", ""))
    menge = normalized(frontmatter.get("menge_umfang", ""))
    huerde = normalized(frontmatter.get("huerde_label", ""))
    quelle = normalized(frontmatter.get("quelle_label", ""))
    joined = " | ".join([bauteil, material, herkunft, alte_funktion, menge, huerde, quelle])

    if not joined or joined in UNCERTAIN_VALUES:
        return False
    if any(token in joined for token in EXCLUSION_TOKENS):
        return False
    if all(is_uncertain(frontmatter.get(key, "")) for key in SUBSTANTIVE_FRONTMATTER_KEYS):
        return False
    if material.startswith("unbekannt") and all(is_uncertain(frontmatter.get(key, "")) for key in ("herkunft_label", "alte_funktion", "menge_umfang")):
        return False

    source_context = " | ".join([herkunft, alte_funktion, material, bauteil])
    has_new_source = any(token in source_context for token in NEW_SOURCE_TOKENS)
    has_positive_source = any(token in source_context for token in POSITIVE_SOURCE_TOKENS)
    if has_new_source and not has_positive_source:
        return False

    return True


def direct_reuse_exclusion_sources(edge_rows: list[dict[str, str]]) -> set[str]:
    sources = set()
    for row in edge_rows:
        if row["relation"] != "has_bewertungslogik_abgrenzung":
            continue
        if row["target"] in NON_DIRECT_ABGRENZUNG_TARGETS:
            sources.add(row["source"])
    return sources


def existing_edge_keys(rows: list[dict[str, str]]) -> set[tuple[str, str, str]]:
    return {(row["source"], row["relation"], row["target"]) for row in rows}


def build_reuse_strategy_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    strategy_rows = extract_strategy_rows()
    reuse_by_case = load_reuse_nodes()
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    for case_id, strategy_row in sorted(strategy_rows.items()):
        targets = map_strategy_targets(strategy_row, existing_nodes)
        if not targets:
            stats["cases_without_target"] += 1
            skipped.append({**strategy_row, "reason": "no_existing_strategy_target"})
            continue

        reuse_rows = reuse_by_case.get(case_id, [])
        if not reuse_rows:
            stats["cases_without_reuse_nodes"] += 1
            skipped.append({**strategy_row, "reason": "no_reuse_einsatz_nodes"})
            continue

        reusable_rows = []
        for node_row in reuse_rows:
            if node_row["typed_path"] in excluded_sources:
                stats["reuse_nodes_skipped_by_abgrenzung"] += 1
                continue
            frontmatter = load_reuse_frontmatter(node_row)
            if reusable_enough(frontmatter):
                reusable_rows.append((node_row, frontmatter))
            else:
                stats["reuse_nodes_skipped_not_reusable"] += 1

        if not reusable_rows:
            stats["cases_without_reusable_rows"] += 1
            skipped.append({**strategy_row, "reason": "no_reusable_inventory_rows"})
            continue

        raw_label = "; ".join(
            part for part in (
                strategy_row.get("value", ""),
                strategy_row.get("relationship", ""),
            )
            if part
        )
        confidence = row_confidence(strategy_row)
        for node_row, _frontmatter in reusable_rows:
            source = node_row["typed_path"]
            for target in targets:
                key = (source, "has_reuse_strategie", target)
                if key in existing_keys:
                    stats["duplicates_skipped"] += 1
                    continue
                target_entity, target_id = target.split("/", 1)
                addition = {
                    "source": source,
                    "source_entity": "reuse_einsatz",
                    "source_id": node_row["id"],
                    "relation": "has_reuse_strategie",
                    "target": target,
                    "target_entity": target_entity,
                    "target_id": target_id,
                    "field": "Entitaeten-Mapping:Reuse-Strategie",
                    "raw_label": raw_label,
                    "confidence": confidence,
                    "resolution_rule": "table_50a_reuse_strategie_entity_mapping",
                    "legacy_path": strategy_row["legacy_path"],
                    "original_source": source,
                    "original_relation": "has_reuse_strategie",
                    "original_target": target,
                    "edge_cleaning": "added_gap_50a",
                }
                additions.append(addition)
                existing_keys.add(key)

    stats["strategy_rows"] = len(strategy_rows)
    stats["additions"] = len(additions)
    stats["cases_with_additions"] = len({row["legacy_path"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


def map_connection_targets(raw_label: str, existing_nodes: set[str]) -> list[str]:
    label = normalized(raw_label)
    if not label or label in UNCERTAIN_VALUES:
        return []
    if any(token in label for token in CONNECTION_UNCERTAIN_TOKENS):
        return []
    if "ohne mortel" in label or "ohne moertel" in label:
        # This is an explicit negative clue, not a Vermoertelung edge.
        return []

    targets: list[str] = []
    for target, tokens in CONNECTION_RULES:
        if target not in existing_nodes:
            continue
        if any(token in label for token in tokens) and target not in targets:
            targets.append(target)
    return targets


def connection_confidence(raw_label: str) -> str:
    label = normalized(raw_label)
    if any(token in label for token in ("laut quelle", "laut quellen", "je quelle", "erwahnt", "allgemein")):
        return "rule_medium"
    return "rule_high"


def map_status_targets(raw_label: str, existing_nodes: set[str]) -> list[str]:
    label = normalized(raw_label)
    if not label or label in UNCERTAIN_VALUES:
        return []

    target_id = "Unklar"
    if any(token in label for token in STATUS_DISCARDED_TOKENS):
        target_id = "Verworfen"
    elif label.startswith("unklar") or "projektstatus unsicher" in label:
        target_id = "Unklar"
    elif any(token in label for token in STATUS_TEMPORARY_TOKENS):
        target_id = "Temporaer"
    elif any(token in label for token in STATUS_PROTOTYPE_TOKENS):
        target_id = "Prototypisch"
    elif any(token in label for token in STATUS_REALIZED_TOKENS):
        target_id = "Realisiert"
    elif any(token in label for token in STATUS_PLANNED_TOKENS):
        target_id = "Geplant"
    elif any(token in label for token in STATUS_PROPOSED_TOKENS):
        target_id = "Vorgeschlagen"

    target = STATUS_TARGETS[target_id]
    if target in existing_nodes:
        return [target]
    return []


def status_confidence(raw_label: str, target: str) -> str:
    if target.endswith("/Unklar"):
        return "rule_high"
    label = normalized(raw_label)
    if any(token in label for token in STATUS_MEDIUM_CONFIDENCE_TOKENS):
        return "rule_medium"
    return "rule_high"


def process_segments(raw_label: str) -> list[str]:
    label = normalized(raw_label)
    if not label or label in UNCERTAIN_VALUES:
        return []
    if "/" in raw_label and "," not in raw_label and ";" not in raw_label and label.endswith("unbekannt"):
        return []

    segments: list[str] = []
    for segment in re.split(r"[,;/]+", raw_label):
        normalized_segment = normalized(segment)
        if not normalized_segment or normalized_segment in UNCERTAIN_VALUES:
            continue
        if any(token in normalized_segment for token in PROCESS_SKIP_SEGMENT_TOKENS):
            continue
        segments.append(normalized_segment)
    return segments


def process_token_matches(segment: str, token: str) -> bool:
    if token == "montage":
        return bool(re.search(r"(?<![a-z])montage(?![a-z])", segment))
    if token == "lagerung" and "auflagerung" in segment:
        return False
    return token in segment


def word_matches(segment: str, token: str) -> bool:
    return bool(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", segment))


def map_process_targets(raw_label: str, existing_nodes: set[str]) -> list[str]:
    targets: list[str] = []
    for segment in process_segments(raw_label):
        for target, tokens in PROCESS_PHASE_RULES:
            if target not in existing_nodes:
                continue
            if target == "prozessphase/Lagerung" and "auflagerung" in segment:
                continue
            if any(process_token_matches(segment, token) for token in tokens) and target not in targets:
                targets.append(target)
    return targets


def process_confidence(raw_label: str) -> str:
    label = normalized(raw_label)
    if any(token in label for token in PROCESS_MEDIUM_CONFIDENCE_TOKENS):
        return "rule_medium"
    return "rule_high"


def map_rueckbauverfahren_targets(raw_label: str, existing_nodes: set[str]) -> list[str]:
    targets: list[str] = []
    for segment in process_segments(raw_label):
        if (
            "selektiver ruckbau" in segment
            or "selektiver rueckbau" in segment
            or "selektive demontage" in segment
            or "selektiver ausbau" in segment
            or word_matches(segment, "selektiv")
        ):
            target = "rueckbauverfahren/Selektiver_Rueckbau"
            if target in existing_nodes and target not in targets:
                targets.append(target)
            continue

        if (
            "demontage" in segment
            or "demontiert" in segment
            or "demontier" in segment
            or word_matches(segment, "abbau")
        ):
            target = "rueckbauverfahren/Demontage"
            if target in existing_nodes and target not in targets:
                targets.append(target)

        if (
            word_matches(segment, "ausbau")
            or "ausgebaut" in segment
            or word_matches(segment, "entnahme")
        ):
            target = "rueckbauverfahren/Ausbau_von_Bauteilen"
            if target in existing_nodes and target not in targets:
                targets.append(target)

        if (
            "schonender ruckbau" in segment
            or "schonender rueckbau" in segment
            or "zerstoerungsarme bergung" in segment
            or "zerstorungsarme bergung" in segment
            or "bergung" in segment
            or "geborgen" in segment
            or "bergen" in segment
            or "harvesting" in segment
            or "oogsten" in segment
            or "geerntet" in segment
            or word_matches(segment, "ernte")
        ):
            target = "rueckbauverfahren/Zerstoerungsarme_Bergung"
            if target in existing_nodes and target not in targets:
                targets.append(target)

    return targets


def build_connection_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_rows = [
        row for row in load_csv(NODE_INVENTORY)
        if row["entity"] == "reuse_einsatz"
    ]

    for node_row in sorted(reuse_rows, key=lambda row: row["typed_path"]):
        markdown = load_reuse_markdown(node_row)
        raw_label = extract_markdown_bullet(markdown, "Verbindung")
        if not raw_label:
            stats["rows_without_connection_label"] += 1
            continue

        if node_row["typed_path"] in excluded_sources:
            stats["connection_rows_skipped_by_abgrenzung"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "legacy_path": "",
                "raw_label": raw_label,
                "reason": "non_direct_reuse_abgrenzung",
            })
            continue

        frontmatter = parse_simple_frontmatter(markdown)
        if not reusable_enough(frontmatter):
            stats["connection_rows_skipped_not_reusable"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "legacy_path": "",
                "raw_label": raw_label,
                "reason": "not_reusable_enough_for_connection_edge",
            })
            continue

        targets = map_connection_targets(raw_label, existing_nodes)
        if not targets:
            stats["connection_labels_skipped"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "legacy_path": "",
                "raw_label": raw_label,
                "reason": "no_precise_connection_target",
            })
            continue

        confidence = connection_confidence(raw_label)
        for target in targets:
            key = (node_row["typed_path"], "has_fuegung_verbindung", target)
            if key in existing_keys:
                stats["duplicates_skipped"] += 1
                continue
            target_entity, target_id = target.split("/", 1)
            addition = {
                "source": node_row["typed_path"],
                "source_entity": "reuse_einsatz",
                "source_id": node_row["id"],
                "relation": "has_fuegung_verbindung",
                "target": target,
                "target_entity": target_entity,
                "target_id": target_id,
                "field": "BAUTEIL-INVENTAR:Verbindung",
                "raw_label": raw_label,
                "confidence": confidence,
                "resolution_rule": "table_50b_fuegung_verbindung_label",
                "legacy_path": "",
                "original_source": node_row["typed_path"],
                "original_relation": "has_fuegung_verbindung",
                "original_target": target,
                "edge_cleaning": "added_gap_50b",
            }
            additions.append(addition)
            existing_keys.add(key)

    stats["reuse_rows_scanned"] = len(reuse_rows)
    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


def build_status_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    status_rows = extract_project_status_rows()
    reuse_by_case = load_reuse_nodes()
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    for case_id, status_row in sorted(status_rows.items()):
        targets = map_status_targets(status_row["value"], existing_nodes)
        if not targets:
            stats["cases_without_target"] += 1
            skipped.append({**status_row, "reason": "no_existing_status_target"})
            continue

        reuse_rows = reuse_by_case.get(case_id, [])
        if not reuse_rows:
            stats["cases_without_reuse_nodes"] += 1
            skipped.append({**status_row, "reason": "no_reuse_einsatz_nodes"})
            continue

        reusable_rows = []
        for node_row in reuse_rows:
            frontmatter = load_reuse_frontmatter(node_row)
            if reusable_enough(frontmatter):
                reusable_rows.append((node_row, frontmatter))
                if node_row["typed_path"] in excluded_sources:
                    stats["status_rows_kept_with_abgrenzung"] += 1
            else:
                stats["status_rows_skipped_not_reusable"] += 1

        if not reusable_rows:
            stats["cases_without_reusable_rows"] += 1
            skipped.append({**status_row, "reason": "no_reusable_inventory_rows"})
            continue

        for node_row, _frontmatter in reusable_rows:
            source = node_row["typed_path"]
            for target in targets:
                key = (source, "has_reuse_einsatzstatus", target)
                if key in existing_keys:
                    stats["duplicates_skipped"] += 1
                    continue
                target_entity, target_id = target.split("/", 1)
                addition = {
                    "source": source,
                    "source_entity": "reuse_einsatz",
                    "source_id": node_row["id"],
                    "relation": "has_reuse_einsatzstatus",
                    "target": target,
                    "target_entity": target_entity,
                    "target_id": target_id,
                    "field": "Projektstatus",
                    "raw_label": status_row["value"],
                    "confidence": status_confidence(status_row["value"], target),
                    "resolution_rule": "case_50c_reuse_einsatzstatus_project_status",
                    "legacy_path": status_row["legacy_path"],
                    "original_source": source,
                    "original_relation": "has_reuse_einsatzstatus",
                    "original_target": target,
                    "edge_cleaning": "added_gap_50c",
                }
                additions.append(addition)
                existing_keys.add(key)

    stats["project_status_rows"] = len(status_rows)
    stats["additions"] = len(additions)
    stats["cases_with_additions"] = len({row["legacy_path"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


def build_process_phase_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    existing_keys = existing_edge_keys(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_rows = [
        row for row in load_csv(NODE_INVENTORY)
        if row["entity"] == "reuse_einsatz"
    ]

    for node_row in sorted(reuse_rows, key=lambda row: row["typed_path"]):
        markdown = load_reuse_markdown(node_row)
        raw_label = extract_markdown_bullet(markdown, "Eingriff/Aufbereitung")
        if not raw_label:
            stats["rows_without_process_label"] += 1
            continue

        frontmatter = parse_simple_frontmatter(markdown)
        if not reusable_enough(frontmatter):
            stats["process_rows_skipped_not_reusable"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "legacy_path": "",
                "raw_label": raw_label,
                "reason": "not_reusable_enough_for_process_phase_edge",
            })
            continue

        targets = map_process_targets(raw_label, existing_nodes)
        if not targets:
            stats["process_labels_skipped"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "legacy_path": "",
                "raw_label": raw_label,
                "reason": "no_precise_process_phase_target",
            })
            continue

        confidence = process_confidence(raw_label)
        for target in targets:
            key = (node_row["typed_path"], "has_prozessphase", target)
            if key in existing_keys:
                stats["duplicates_skipped"] += 1
                continue
            target_entity, target_id = target.split("/", 1)
            addition = {
                "source": node_row["typed_path"],
                "source_entity": "reuse_einsatz",
                "source_id": node_row["id"],
                "relation": "has_prozessphase",
                "target": target,
                "target_entity": target_entity,
                "target_id": target_id,
                "field": "BAUTEIL-INVENTAR:Eingriff/Aufbereitung",
                "raw_label": raw_label,
                "confidence": confidence,
                "resolution_rule": "label_50d_prozessphase_eingriff_aufbereitung",
                "legacy_path": "",
                "original_source": node_row["typed_path"],
                "original_relation": "has_prozessphase",
                "original_target": target,
                "edge_cleaning": "added_gap_50d",
            }
            additions.append(addition)
            existing_keys.add(key)

    stats["reuse_rows_scanned"] = len(reuse_rows)
    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


def build_rueckbauverfahren_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    existing_keys = existing_edge_keys(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_rows = [
        row for row in load_csv(NODE_INVENTORY)
        if row["entity"] == "reuse_einsatz"
    ]

    for node_row in sorted(reuse_rows, key=lambda row: row["typed_path"]):
        markdown = load_reuse_markdown(node_row)
        raw_label = extract_markdown_bullet(markdown, "Eingriff/Aufbereitung")
        if not raw_label:
            stats["rows_without_process_label"] += 1
            continue

        frontmatter = parse_simple_frontmatter(markdown)
        if not reusable_enough(frontmatter):
            stats["rueckbau_rows_skipped_not_reusable"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "legacy_path": "",
                "raw_label": raw_label,
                "reason": "not_reusable_enough_for_rueckbauverfahren_edge",
            })
            continue

        targets = map_rueckbauverfahren_targets(raw_label, existing_nodes)
        if not targets:
            stats["rueckbau_labels_skipped"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "legacy_path": "",
                "raw_label": raw_label,
                "reason": "no_precise_rueckbauverfahren_target",
            })
            continue

        confidence = process_confidence(raw_label)
        for target in targets:
            key = (node_row["typed_path"], "has_rueckbauverfahren", target)
            if key in existing_keys:
                stats["duplicates_skipped"] += 1
                continue
            target_entity, target_id = target.split("/", 1)
            addition = {
                "source": node_row["typed_path"],
                "source_entity": "reuse_einsatz",
                "source_id": node_row["id"],
                "relation": "has_rueckbauverfahren",
                "target": target,
                "target_entity": target_entity,
                "target_id": target_id,
                "field": "BAUTEIL-INVENTAR:Eingriff/Aufbereitung",
                "raw_label": raw_label,
                "confidence": confidence,
                "resolution_rule": "label_50e_rueckbauverfahren_eingriff_aufbereitung",
                "legacy_path": "",
                "original_source": node_row["typed_path"],
                "original_relation": "has_rueckbauverfahren",
                "original_target": target,
                "edge_cleaning": "added_gap_50e",
            }
            additions.append(addition)
            existing_keys.add(key)

    stats["reuse_rows_scanned"] = len(reuse_rows)
    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


# ---------------------------------------------------------------------------
# 50f helpers — located_in_ort
# ---------------------------------------------------------------------------

# Raw Ort values that are not usable location strings.
ORT_SKIP_TOKENS = (
    "reuse stammt",
    "nicht aus fertigteilen",
    "ortbeton",
    "gesagte",
    "keine angabe",
    "unbekannt",
    "unklar",
)

# Country suffixes (lowercased) to strip when extracting the city name.
COUNTRY_SUFFIXES_LOW = (
    ", uk", ", gb", ", deutschland", ", germany", ", schweiz",
    ", switzerland", ", belgien", ", belgium", ", frankreich",
    ", france", ", niederlande", ", netherlands", ", finnland",
    ", finland", ", norwegen", ", norway", ", japan", ", usa",
    ", luxemburg", ", luxembourg", ", danemark", ", dk",
)


def slugify_ort(city_name: str) -> str:
    """Turn a city display name into a safe folder-name slug."""
    slug = city_name.strip()
    replacements = [
        ("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"),
        ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"),
        ("é", "e"), ("è", "e"), ("ê", "e"), ("ë", "e"),
        ("à", "a"), ("â", "a"), ("á", "a"),
        ("î", "i"), ("ï", "i"), ("í", "i"),
        ("ô", "o"), ("ó", "o"), ("ø", "oe"), ("Ø", "Oe"),
        ("û", "u"), ("ú", "u"),
        ("ñ", "n"), ("ç", "c"),
        ("æ", "ae"), ("Æ", "Ae"),
        ("ł", "l"), ("ğ", "g"),
    ]
    for src, dst in replacements:
        slug = slug.replace(src, dst)
    slug = unicodedata.normalize("NFKD", slug)
    slug = "".join(ch for ch in slug if not unicodedata.combining(ch))
    slug = re.sub(r"[\s\-]+", "_", slug)
    slug = re.sub(r"[^A-Za-z0-9_]", "", slug)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug


# City override map for cases where automatic extraction gives wrong results.
# Key = case_id (Gebaeude filename stem), value = (display_name, slug).
ORT_OVERRIDES: dict[str, tuple[str, str]] = {
    "CRCLR_House_Impact_Hub_Berlin":                           ("Berlin", "Berlin"),
    "Circular_Pavilion_Paris":                                 ("Paris", "Paris"),
    "Ferme_du_Rail_Paris":                                     ("Paris", "Paris"),
    "Resilience_La_Ferme_des_Possibles_Stains":                ("Stains", "Stains"),
    "Grande_Halle_de_Colombelles":                             ("Colombelles", "Colombelles"),
    "Recypark_Demets_Anderlecht":                              ("Bruessel", "Bruessel"),
    "Musee_de_Folklore_Mouscron":                              ("Mouscron", "Mouscron"),
    "Lo_Reninge_Town_Hall_Facade":                             ("Lo_Reninge", "Lo_Reninge"),
    "Grubenstrasse_29_Werkhof_29_Zuerich":                     ("Zuerich", "Zuerich"),
    "Juch_Areal_Recyclingzentrum_Zuerich":                     ("Zuerich", "Zuerich"),
    "Kindergarten_Moeoeslistrasse_Manegg_Zuerich":             ("Zuerich", "Zuerich"),
    "KA13_Kristian_Augusts_gate_13_Oslo":                      ("Oslo", "Oslo"),
    "PLP_London_HQ_Circular_Studio_Fitout":                    ("London", "London"),
    "BioPartner_5_Leiden_Oegstgeest":                          ("Leiden", "Leiden"),
    "Plattenpalast_Berlin":                                    ("Berlin", "Berlin"),
    "Plattenvereinigung_Berlin":                               ("Berlin", "Berlin"),
    "Europa_Building_Brussels":                                ("Bruessel", "Bruessel"),
    "Multi_Brussels_Reuse_in_MULTI":                           ("Bruessel", "Bruessel"),
    "Charles_Malis_Molenbeek":                                 ("Bruessel", "Bruessel"),
    "Zinneke_Feder_Masui4ever_Brussels":                       ("Bruessel", "Bruessel"),
    "Verbiest_Karreveld_Brussels":                             ("Bruessel", "Bruessel"),
    "Maison_Vignette_Auderghem":                               ("Bruessel", "Bruessel"),
    "Chiro_d_Itterbeek_Dilbeek":                               ("Dilbeek", "Dilbeek"),
    "Holbein_Gardens_London":                                  ("London", "London"),
    "Brighton_Waste_House_Brighton":                           ("Brighton", "Brighton"),
    "Timber_Square_London":                                    ("London", "London"),
    "Maison_des_Canaux_Paris":                                 ("Paris", "Paris"),
    "BlueCity_Offices_Rotterdam":                              ("Rotterdam", "Rotterdam"),
    "CascadeUp_London_secondary_timber_glulam_demonstrator":   ("London", "London"),
    "Christ_Pavilion_Volkenroda":                              ("Volkenroda", "Volkenroda"),
    "Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere":      ("Tampere", "Tampere"),
    "Lokomotion_Technology_Centre_mini_pilot_Tampere":         ("Tampere", "Tampere"),
    "Melkinlaituri_Primary_School_Daycare_Centre_Helsinki":    ("Helsinki", "Helsinki"),
    "ELYS_Kultur_Gewerbehaus_Basel":                           ("Basel", "Basel"),
    "K118_Kopfbau_Halle_118_Winterthur":                      ("Winterthur", "Winterthur"),
    "Brent_Cross_Town_Primary_Substation_London":              ("London", "London"),
    "Recyclinghaus_Hannover":                                  ("Hannover", "Hannover"),
    "Upcycle_Studios_Copenhagen":                              ("Copenhagen", "Copenhagen"),
    "Thoravej_29_Copenhagen":                                  ("Copenhagen", "Copenhagen"),
    "Resource_Rows_Copenhagen":                                ("Copenhagen", "Copenhagen"),
    "Villa_Welpeloo_Enschede":                                 ("Enschede", "Enschede"),
    "Peoples_Pavilion_Eindhoven":                              ("Eindhoven", "Eindhoven"),
}


def extract_city_from_ort(raw_ort: str, case_id: str = "") -> tuple[str, str]:
    """Return (city_display_name, city_slug) or ('', '') if unusable."""
    # Check manual override first.
    if case_id in ORT_OVERRIDES:
        return ORT_OVERRIDES[case_id]

    raw = raw_ort.strip()
    if not raw or raw in ("-", "\u2014", "\u2013"):
        return "", ""

    low = normalized(raw)
    if any(token in low for token in ORT_SKIP_TOKENS):
        return "", ""

    # For multi-event strings separated by ";" take the last segment
    # (permanent location is usually listed last).
    if ";" in raw:
        raw = raw.split(";")[-1].strip()

    # Strip trailing country suffix so it doesn't end up in the city name.
    working = raw
    low_working = normalized(working)
    for suffix in COUNTRY_SUFFIXES_LOW:
        if low_working.endswith(suffix):
            working = working[:len(working) - len(suffix)].strip().rstrip(",")
            break

    # Walk through comma/slash segments and pick the first that looks like a city.
    segments = [s.strip() for s in re.split(r"\s*/\s*|,", working) if s.strip()]
    city = ""
    for seg in segments:
        seg_low = normalized(seg)
        # Skip segments that start with a digit (street number or postal code).
        if re.match(r"^\d", seg):
            continue
        # Skip postal-code-like segments.
        if re.match(r"^[A-Z]{1,2}\d", seg):
            continue
        # Skip segments containing street-type words.
        if any(word in seg_low for word in (
            " strasse", " strase", " straat", " street", " rue ",
            " avenue", " boulevard", " laan", " weg ", " allee",
            " gasse", " gate ", " road", " drive", " lane",
        )):
            continue
        # Skip event / venue / campus strings.
        if any(word in seg_low for word in (
            "festival", "expo ", "design festival", "futurebuild",
            "university of", "campus", "plein", "parvis", "feld ",
            "bio science park",
        )):
            continue
        city = seg
        break

    if not city or len(city) < 2:
        return "", ""

    slug = slugify_ort(city)
    if not slug:
        return "", ""

    return city, slug


def ensure_ort_node(slug: str, display_name: str, raw_ort: str, case_id: str) -> bool:
    """Create ort/<slug>/index.md if it doesn't exist. Returns True if created."""
    node_dir = DATABASE / "ort" / slug
    index_path = node_dir / "index.md"
    if index_path.exists():
        return False
    node_dir.mkdir(parents=True, exist_ok=True)
    content = (
        f"---\n"
        f'entity: "ort"\n'
        f'id: "{slug}"\n'
        f'title: "{display_name}"\n'
        f'build_status: "created_50f"\n'
        f'node_kind: "knot"\n'
        f'legacy_type: "Ort"\n'
        f"---\n"
        f"\n"
        f"# {display_name}\n"
        f"\n"
        f"## Herkunft\n"
        f"\n"
        f"Dieser Ort-Knoten wurde automatisch aus dem Fallstudien-Datenbestand\n"
        f"extrahiert (Batch 50f, Quelle: `Geb\u00e4ude/{case_id}.md`).\n"
        f"\n"
        f"**Roher Ort-Wert aus der Quelle:** {raw_ort}\n"
        f"\n"
        f"## Inhalt\n"
        f"\n"
        f"<!-- Bitte erg\u00e4nze hier einen deutschen Flie\u00dftext zur Bedeutung dieses\n"
        f"     Standorts im Kontext der Bauteil-Wiederverwendung. -->\n"
    )
    index_path.write_text(content, encoding="utf-8")
    return True


def extract_ort_rows() -> dict[str, dict[str, str]]:
    """Return {case_id: {'raw_ort': ..., 'legacy_path': ...}} for each Gebaeude case."""
    source_dir = gebaeude_dir()
    ort_rows: dict[str, dict[str, str]] = {}
    for path in sorted(source_dir.glob("*.md")):
        md = path.read_text(encoding="utf-8", errors="replace")
        section = markdown_section(md, "ENTIT")
        for row in parse_markdown_tables(section):
            entity_cell = get_cell(row, "Entitat")
            if normalized(entity_cell).startswith("ort"):
                ort_rows[path.stem] = {
                    "case_id": path.stem,
                    "legacy_path": str(path.relative_to(ROOT)),
                    "raw_ort": get_cell(row, "Wert"),
                }
                break
    return ort_rows


def build_located_in_ort_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    ort_rows = extract_ort_rows()
    existing_keys = existing_edge_keys(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    # Supplement existing_nodes with ort folders already on disk.
    # The node_inventory.csv can be stale (e.g. after a previous dry-run
    # already created some ort/ folders but didn't rebuild the inventory).
    ort_dir = DATABASE / "ort"
    if ort_dir.exists():
        for ort_folder in ort_dir.iterdir():
            if ort_folder.is_dir() and (ort_folder / "index.md").exists():
                existing_nodes.add(f"ort/{ort_folder.name}")

    # Map case_id -> typed_path for fallstudie nodes
    fallstudie_by_id: dict[str, str] = {}
    for inv_row in load_csv(NODE_INVENTORY):
        if inv_row["entity"] == "fallstudie":
            fallstudie_by_id[inv_row["id"]] = inv_row["typed_path"]


    for case_id, ort_row in sorted(ort_rows.items()):
        raw_ort = ort_row["raw_ort"]
        city_name, slug = extract_city_from_ort(raw_ort, case_id)

        if not slug:
            stats["ort_rows_skipped_unusable"] += 1
            skipped.append({
                "case_id": case_id,
                "legacy_path": ort_row["legacy_path"],
                "raw_label": raw_ort,
                "reason": "unusable_ort_value",
            })
            continue

        fallstudie_path = fallstudie_by_id.get(case_id)
        if not fallstudie_path:
            stats["cases_without_fallstudie_node"] += 1
            skipped.append({
                "case_id": case_id,
                "legacy_path": ort_row["legacy_path"],
                "raw_label": raw_ort,
                "reason": "no_fallstudie_node",
            })
            continue

        target = f"ort/{slug}"
        # Create the ort node if it doesn't exist yet.
        was_created = ensure_ort_node(slug, city_name, raw_ort, case_id)
        if was_created:
            existing_nodes.add(target)
            stats["ort_nodes_created"] += 1

        if target not in existing_nodes:
            stats["ort_target_not_found"] += 1
            skipped.append({
                "case_id": case_id,
                "legacy_path": ort_row["legacy_path"],
                "raw_label": raw_ort,
                "reason": "ort_node_not_found_after_creation",
            })
            continue

        source = fallstudie_path
        key = (source, "located_in_ort", target)
        if key in existing_keys:
            stats["duplicates_skipped"] += 1
            continue

        target_entity, target_id = target.split("/", 1)
        addition = {
            "source": source,
            "source_entity": "fallstudie",
            "source_id": case_id,
            "relation": "located_in_ort",
            "target": target,
            "target_entity": target_entity,
            "target_id": target_id,
            "field": "Entitaeten-Mapping:Ort",
            "raw_label": raw_ort,
            "confidence": "rule_high",
            "resolution_rule": "table_50f_located_in_ort_entity_mapping",
            "legacy_path": ort_row["legacy_path"],
            "original_source": source,
            "original_relation": "located_in_ort",
            "original_target": target,
            "edge_cleaning": "added_gap_50f",
        }
        additions.append(addition)
        existing_keys.add(key)

    stats["ort_rows_scanned"] = len(ort_rows)
    stats["additions"] = len(additions)
    stats["cases_with_additions"] = len({row["legacy_path"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


def write_diff(batch_name: str, additions: list[dict[str, str]], skipped: list[dict[str, str]], stats: Counter[str]) -> None:
    diff_path = REPORT_DIR / f"50_gap_relation_diff_{batch_name}.csv"
    with diff_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source", "relation", "target", "raw_label", "confidence",
                "resolution_rule", "legacy_path",
            ],
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        for row in additions:
            writer.writerow({
                "source": row["source"],
                "relation": row["relation"],
                "target": row["target"],
                "raw_label": row["raw_label"],
                "confidence": row["confidence"],
                "resolution_rule": row["resolution_rule"],
                "legacy_path": row["legacy_path"],
            })

    skipped_path = REPORT_DIR / f"50_gap_relation_skipped_{batch_name}.csv"
    with skipped_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source", "case_id", "legacy_path", "value", "relationship",
                "confidence_source", "note", "raw_label", "reason",
            ],
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        for row in skipped:
            writer.writerow({
                "source": row.get("source", ""),
                "case_id": row.get("case_id", ""),
                "legacy_path": row.get("legacy_path", ""),
                "value": row.get("value", ""),
                "relationship": row.get("relationship", ""),
                "confidence_source": row.get("confidence_source", ""),
                "note": row.get("note", ""),
                "raw_label": row.get("raw_label", ""),
                "reason": row.get("reason", ""),
            })

    summary_path = REPORT_DIR / f"50_gap_relation_summary_{batch_name}.md"
    target_counts = Counter(row["target"] for row in additions)
    confidence_counts = Counter(row["confidence"] for row in additions)
    lines = [
        f"# Gap Relation Extraction {batch_name}",
        "",
        "## Result",
        "",
        f"- Added edges: {stats['additions']}",
        f"- Duplicate edges skipped: {stats['duplicates_skipped']}",
        "",
        "## Batch Stats",
        "",
    ]
    for key, value in sorted(stats.items()):
        lines.append(f"- `{key}`: {value}")
    lines.extend([
        "",
        "## Target Counts",
        "",
    ])
    if target_counts:
        lines.extend(f"- `{target}`: {count}" for target, count in sorted(target_counts.items()))
    else:
        lines.append("- none")
    lines.extend([
        "",
        "## Confidence Counts",
        "",
    ])
    if confidence_counts:
        lines.extend(f"- `{confidence}`: {count}" for confidence, count in sorted(confidence_counts.items()))
    else:
        lines.append("- none")
    lines.extend([
        "",
        "## Reports",
        "",
        f"- Diff: `{diff_path.relative_to(ROOT).as_posix()}`",
        f"- Skipped: `{skipped_path.relative_to(ROOT).as_posix()}`",
    ])
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Diff: {diff_path.relative_to(ROOT)}")
    print(f"  Skipped: {skipped_path.relative_to(ROOT)}")
    print(f"  Summary: {summary_path.relative_to(ROOT)}")


BATCHES = {
    "50a_reuse_strategie": build_reuse_strategy_edges,
    "50b_fuegung_verbindung": build_connection_edges,
    "50c_reuse_einsatzstatus": build_status_edges,
    "50d_prozessphase": build_process_phase_edges,
    "50e_rueckbauverfahren": build_rueckbauverfahren_edges,
    "50f_located_in_ort": build_located_in_ort_edges,
}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("batches", nargs="*", default=list(BATCHES.keys()))
    parser.add_argument("--dry-run", action="store_true", help="write reports but do not rewrite clean_confirmed_edges.csv")
    args = parser.parse_args(argv[1:])

    unknown = [batch for batch in args.batches if batch not in BATCHES]
    if unknown:
        print(f"Unknown batches: {unknown}", file=sys.stderr)
        print(f"Available: {list(BATCHES)}", file=sys.stderr)
        return 2

    rows = load_csv(EDGES)
    existing_nodes = load_existing_nodes()
    print(f"Loaded {len(rows)} edges from {EDGES.relative_to(ROOT)}")

    total_additions = 0
    for batch_name in args.batches:
        rows, additions, stats, skipped = BATCHES[batch_name](rows, existing_nodes)
        total_additions += len(additions)
        print(f"  Batch {batch_name}: {len(additions)} edges added")
        write_diff(batch_name, additions, skipped, stats)

    if args.dry_run:
        print("Dry run: edge file not rewritten.")
        return 0

    if total_additions == 0:
        print("No additions; not rewriting the edge file.")
        return 0

    write_edges(rows)
    print(f"Wrote {len(rows)} edges back to {EDGES.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
