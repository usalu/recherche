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
    if it doesn't yet exist,     and emits one fallstudie -> located_in_ort
    -> ort edge per case. Bad/non-location Ort values are skipped.
  50s_has_ressourcenquelle
    Maps the reuse_einsatz frontmatter `herkunft_label` to concrete `ressourcenquelle/`
    knots (physical source pools). Kept separate from 50i `has_beschaffungsweg`.
  50u_has_methode
    Maps the Eingriff/Aufbereitung bullet to `methode/*` knots (Urban Mining, audits, …).
  50l_has_wirtschaft
    Reads economic labels from Gebaeude mapping, kennwerte, hurdles, and
    "WIRTSCHAFT UND BESCHAFFUNG" sections and maps them to wirtschaft knots.
  50m_has_rechtliche_bedingung
    Reads component and case-level legal labels and maps them to concrete
    rechtliche_bedingung knots.
  50n_has_schadstoff
    Reads explicit contaminant labels and maps them to concrete schadstoff
    knots. This batch is intentionally stricter than the legal batch.
  50o_has_konstruktion
    Reads structural labels and maps reuse_einsatz nodes to concrete
    bauweise, bausystem, and tragwerksprinzip knots.
  50p_has_bauteilprofil
    Reads component labels and maps reuse_einsatz nodes to bauteilebene,
    bauteilzustand, and funktionswechsel knots.
  50q_has_digital_evidence
    Reads data-point method/quality labels, concrete component sourcing labels,
    and software tool profiles to add data-quality, data-model, software, and
    tool-type edges.
  50r_has_bauobjekt_context
    Reads live bauobjekt/projekt pages plus matching source case files and maps
    building class, role, status, use, and intervention edges.
  50v_has_kontextmerkmal
    Reads the case-level EINORDNUNG bullet "Warnung Bestandserhalt" and, when the
    primary clause is "ja", adds has_kontextmerkmal -> kontextmerkmal/Bestandserhalt_Policy
    on the matching fallstudie node.
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


# ---------------------------------------------------------------------------
# Generic factory for frontmatter-label → knot batches (50g, 50h, 50i, 50j)
# ---------------------------------------------------------------------------

def build_label_to_knot_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
    *,
    frontmatter_key: str,
    relation: str,
    rules: list[tuple[str, tuple[str, ...]]],
    batch_tag: str,
    field_label: str,
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    """Generic batch: reads `frontmatter_key` from each reuse_einsatz index.md,
    applies token-match rules to map to existing knot targets, emits edges."""
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_rows = [
        row for row in load_csv(NODE_INVENTORY)
        if row["entity"] == "reuse_einsatz"
    ]

    for node_row in sorted(reuse_rows, key=lambda r: r["typed_path"]):
        markdown = load_reuse_markdown(node_row)
        frontmatter = parse_simple_frontmatter(markdown)
        raw_label = frontmatter.get(frontmatter_key, "").strip().strip('"')

        if not raw_label or is_uncertain(raw_label):
            stats["rows_without_label"] += 1
            continue

        if not reusable_enough(frontmatter):
            stats["rows_skipped_not_reusable"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "raw_label": raw_label,
                "reason": f"not_reusable_enough_for_{relation}",
            })
            continue

        if node_row["typed_path"] in excluded_sources:
            stats["rows_skipped_by_abgrenzung"] += 1
            continue

        # Match tokens in each comma/semicolon segment
        targets: list[str] = []
        for segment in re.split(r"[,;]+", raw_label):
            seg = normalized(segment)
            if not seg or seg in UNCERTAIN_VALUES:
                continue
            for target, tokens in rules:
                if target not in existing_nodes:
                    continue
                if any(token in seg for token in tokens) and target not in targets:
                    targets.append(target)

        if not targets:
            stats["labels_without_match"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "raw_label": raw_label,
                "reason": "no_token_match",
            })
            continue

        for target in targets:
            key = (node_row["typed_path"], relation, target)
            if key in existing_keys:
                stats["duplicates_skipped"] += 1
                continue
            target_entity, target_id = target.split("/", 1)
            addition = {
                "source": node_row["typed_path"],
                "source_entity": "reuse_einsatz",
                "source_id": node_row["id"],
                "relation": relation,
                "target": target,
                "target_entity": target_entity,
                "target_id": target_id,
                "field": field_label,
                "raw_label": raw_label,
                "confidence": "rule_high",
                "resolution_rule": f"label_{batch_tag}_{relation}_frontmatter",
                "legacy_path": "",
                "original_source": node_row["typed_path"],
                "original_relation": relation,
                "original_target": target,
                "edge_cleaning": f"added_gap_{batch_tag}",
            }
            additions.append(addition)
            existing_keys.add(key)

    stats["reuse_rows_scanned"] = len(reuse_rows)
    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


# ---------------------------------------------------------------------------
# 50g — has_huerde (28 knots, frontmatter: huerde_label)
# ---------------------------------------------------------------------------

HUERDE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("huerde/Akzeptanzproblem",         ("akzeptanz", "ablehnung", "vorbehalte", "skeptisch", "kulturell", "bedenken")),
    ("huerde/Anschlussproblem",         ("anschluss", "kompatibel", "anpassen", "toleranz", "passt nicht", "mass", "abmessung", "detail")),
    ("huerde/Aufbereitungsaufwand",     ("aufbereitung", "reinigen", "reinigung", "behandlung", "aufwand", "nachbearbeitung", "instandsetzung", "arbeitsaufwand")),
    ("huerde/Ausschreibungsproblem",    ("ausschreibung", "vergabe", "vob", "oeffentlich", "offentlich", "bieter", "ausschreib")),
    ("huerde/Bauproduktstatus",         ("bauproduktstatus", "bauprodukt", "ce-markierung", "ce markierung", "marktreife", "zulassung", "zertifikat", "ce")),
    ("huerde/Brandschutzkonflikt",      ("brandschutz", "brand", "feuerwiderstand", "feuerbestandigkeit", "f30", "f60", "f90", "rei")),
    ("huerde/Bruch_Beschaedigungsrisiko", ("bruch", "beschadigung", "beschaedigung", "risiko", "fragil", "sprode", "sproede", "verlust")),
    ("huerde/Datenluecke",              ("datenluecke", "datenlucke", "dokumentation", "nachweis", "belege", "fehlende daten", "unbekannt", "nicht dokumentiert")),
    ("huerde/Dauerhaftigkeit_Restlebensdauer", ("dauerhaft", "restlebensdauer", "lebensdauer", "restnutzung", "alterung", "verschleiss", "ermudung", "ermuedung")),
    ("huerde/Entwurfsbindung",          ("entwurf", "planung", "mass", "geometrie", "format", "sonderanfertigung", "spezifisch", "individuell")),
    ("huerde/Fehlende_Datenstandards",  ("standard", "normen", "datenstandard", "format", "bim", "schnittstelle", "interoperabilitat")),
    ("huerde/Fehlende_Lagerflaeche",    ("lager", "lagerflache", "lagerflaeche", "lagerung", "zwischenlager", "platz", "flache", "flaeche")),
    ("huerde/Fehlende_Standardisierung",("standardisierung", "standard", "normierung", "norm", "serienmaßig", "serienmaessig")),
    ("huerde/Gewaehrleistung",          ("gewahrleisung", "gewahrleistung", "gewaehrleistung", "haftung", "garantie", "mangel")),
    ("huerde/Haftung",                  ("haftung", "verantwortung", "gewahrleisung", "gewahrleistung", "gewaehrleistung", "rechtlich")),
    ("huerde/Heterogenitaet_Chargen",   ("heterogen", "chargen", "charge", "varianz", "variation", "unterschiedlich", "chargen")),
    ("huerde/Hygieneanforderung",       ("hygiene", "sanitar", "sanitaer", "gesundheit", "kontamination", "schadstoff", "reinheit")),
    ("huerde/Kompatibilitaetsproblem",  ("kompatibel", "kompatibilitat", "kompatibilitaet", "verbindung", "anschluss", "schnittstelle", "system")),
    ("huerde/Materialqualitaet_Unklar", ("qualitat", "qualitaet", "zustand", "unbekannt", "unklar", "nicht gepruft", "ungepruft")),
    ("huerde/Mengenunsicherheit",       ("menge", "verfugbar", "verfuegbar", "bestand", "vorrat", "unsicherheit", "schwankung")),
    ("huerde/Schadstoffbelastung",      ("schadstoff", "kontamination", "asbest", "pcb", "blei", "kvoc", "voc", "schadstoffe")),
    ("huerde/Technische_Freigabe",      ("freigabe", "zulassung", "zertifizierung", "prufung", "pruefung", "gutachten", "statik")),
    ("huerde/Terminunsicherheit",       ("termin", "timing", "zeitplan", "verzogerung", "verzoegerung", "verfugbar", "verfuegbar", "lieferfenster")),
    ("huerde/Toleranzen",               ("toleranz", "mass", "abmessung", "passung", "spielraum", "fertigungs")),
    ("huerde/Unkonventionelles_Material",("unkonventionell", "sonder", "selten", "exotisch", "ungewohnt", "unbekannt material")),
    ("huerde/Verfuegbarkeitsproblem",   ("verfugbar", "verfuegbar", "verfugbarkeit", "verfuegbarkeit", "beschaffung", "markt", "angebot", "mangel")),
    ("huerde/Witterung_Feuchte",        ("witterung", "feuchte", "feuchtigkeit", "wasser", "regen", "frost", "temperatur", "klima")),
    ("huerde/Zustand_Unklar",           ("zustand", "unklar", "unbekannt", "nicht gepruft", "ungepruft", "bewertung fehlt")),
]


def build_huerde_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    return build_label_to_knot_edges(
        edge_rows, existing_nodes,
        frontmatter_key="huerde_label",
        relation="has_huerde",
        rules=HUERDE_RULES,
        batch_tag="50g",
        field_label="FRONTMATTER:huerde_label",
    )


# ---------------------------------------------------------------------------
# 50h — has_pruefung_nachweis (frontmatter: pruefung_label)
# ---------------------------------------------------------------------------

PRUEFUNG_RULES: list[tuple[str, tuple[str, ...]]] = [
    # Actual nodes: Abbrandbemessung, Brandschutznachweis, Eignungspruefung_Baulehm,
    #   Geometrische_Vermessung, Materialpruefung, Schadstoffscreening,
    #   Schweissbarkeitspruefung, Sichtpruefung, Statische_Nachweisfuehrung,
    #   Zugversuch, Zustandsbewertung
    ("pruefung_nachweis/Abbrandbemessung",            ("abbrandbemessung", "abbrand", "charring")),
    ("pruefung_nachweis/Brandschutznachweis",         ("brandschutz", "brandnachweis", "feuerwiderstand", "brand", "fire")),
    ("pruefung_nachweis/Eignungspruefung_Baulehm",    ("baulehm", "lehm", "earthen", "stampflehm")),
    ("pruefung_nachweis/Geometrische_Vermessung",     ("vermessung", "vermessen", "geometr", "scan", "3d scan", "aufmas", "aufmass")),
    ("pruefung_nachweis/Materialpruefung",            ("materialpruefung", "materialprufung", "materialtest", "werkstoff", "analyse",
                                                        "materialanalyse", "ce marking", "ce-marking", "ce markierung", "en 1090",
                                                        "getestet", "tested", "testing", "certificate", "zertifikat")),
    ("pruefung_nachweis/Schadstoffscreening",         ("schadstoff", "screening", "asbest", "pcb", "blei", "voc", "kontamination",
                                                        "umweltanalyse", "chemisch")),
    ("pruefung_nachweis/Schweissbarkeitspruefung",    ("schweissbarkeit", "schweissbarkeitsprufung", "weldability")),
    ("pruefung_nachweis/Sichtpruefung",               ("sichtprufung", "sichtpruefung", "visuelle prufung", "visual inspection",
                                                        "sichtbar", "augenschein", "inspection", "assessment")),
    ("pruefung_nachweis/Statische_Nachweisfuehrung",  ("statisch", "statiknachweis", "structural", "tragfahigkeit", "ingenieurburo",
                                                        "engineering", "statik", "ingenieur")),
    ("pruefung_nachweis/Zugversuch",                  ("zugversuch", "zugtest", "pull-off", "tensile")),
    ("pruefung_nachweis/Zustandsbewertung",           ("zustandsbewertung", "zustandsbewert", "condition assessment", "zustand",
                                                        "bewertung", "evaluierung", "gutachten", "befund")),
]


def build_pruefung_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    return build_label_to_knot_edges(
        edge_rows, existing_nodes,
        frontmatter_key="pruefung_label",
        relation="has_pruefung_nachweis",
        rules=PRUEFUNG_RULES,
        batch_tag="50h",
        field_label="FRONTMATTER:pruefung_label",
    )


# ---------------------------------------------------------------------------
# 50i — has_beschaffungsweg (frontmatter: no direct field — use herkunft_label)
# ---------------------------------------------------------------------------

BESCHAFFUNGSWEG_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("beschaffungsweg/Ausschreibung",      ("ausschreibung", "vergabe", "offentliche", "oeffentliche", "tender", "ausgeschrieben")),
    ("beschaffungsweg/Bauteilboerse",      ("boerse", "bauteilboerse", "bauteilborse", "marktplatz", "opalis", "rotor", "second hand laden", "secondhand", "restposten")),
    ("beschaffungsweg/Digitale_Plattform", ("plattform", "digital", "online", "datenbank", "matching", "material passort", "materialpass", "bim", "software")),
]


def build_beschaffungsweg_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    return build_label_to_knot_edges(
        edge_rows, existing_nodes,
        frontmatter_key="herkunft_label",
        relation="has_beschaffungsweg",
        rules=BESCHAFFUNGSWEG_RULES,
        batch_tag="50i",
        field_label="FRONTMATTER:herkunft_label",
    )


# ---------------------------------------------------------------------------
# 50s — has_ressourcenquelle (frontmatter herkunft_label → ressourcenquelle/)
# ---------------------------------------------------------------------------

RESSOURCENQUELLE_RULES: list[tuple[str, tuple[str, ...]]] = [
    (
        "ressourcenquelle/Baustelle",
        (
            "baustelle",
            "abbruchbaustelle",
            "demolition site",
            "spenderstandort",
            "abbruchort",
            "herkunftsort",
            "quellort",
            "ehemalige baustelle",
        ),
    ),
    (
        "ressourcenquelle/Bauteilboerse",
        (
            "bauteilboerse",
            "bauteilbörse",
            "bauteilborse",
            "marktplatz",
            "opalis",
            "rotor dc",
            "second hand laden",
            "secondhand laden",
        ),
    ),
    (
        "ressourcenquelle/Donorgebaeude",
        (
            "donorgebaeude",
            "donorgebäude",
            "spendergebaude",
            "spendergebäude",
            "donor building",
            "quellgebaeude",
            "quellgebäude",
            "spenderhochhaus",
            "spender-skelett",
            "spenderskelett",
        ),
    ),
    (
        "ressourcenquelle/Donor_Infrastruktur",
        (
            "bruecken",
            "brücken",
            "tunnel",
            "viadukt",
            "gleisanlage",
            "infrastrukturabbruch",
            "highway",
            "autobahnbruecke",
            "autobahnbrücke",
        ),
    ),
    (
        "ressourcenquelle/Haendler",
        (
            "handler",
            "haendler",
            "händler",
            "handelslager",
            "haendlerlager",
            "handlerlager",
        ),
    ),
    (
        "ressourcenquelle/Lager",
        (
            "zwischenlager",
            "material lager",
            "lagerhaltung",
            "lagerbestand",
            "einlagerung",
            "warehouse",
            "lagerflaeche",
            "lagerfläche",
        ),
    ),
    (
        "ressourcenquelle/Materialstockpile",
        (
            "materialstockpile",
            "stockpile",
            "materialpool",
            "fehlbestell",
            "fehlbestellung",
            "restmaterial",
        ),
    ),
    (
        "ressourcenquelle/Produktionsueberschuss",
        (
            "produktionsueberschuss",
            "produktionsüberschuss",
            "produktionsrest",
            "uberschuss",
            "überschuss",
            "surplus",
            "restposten",
        ),
    ),
]


def build_ressourcenquelle_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    return build_label_to_knot_edges(
        edge_rows,
        existing_nodes,
        frontmatter_key="herkunft_label",
        relation="has_ressourcenquelle",
        rules=RESSOURCENQUELLE_RULES,
        batch_tag="50s",
        field_label="FRONTMATTER:herkunft_label",
    )


# ---------------------------------------------------------------------------
# 50j — has_aufbereitungsverfahren (frontmatter: no direct field —
#        use the BAUTEIL-INVENTAR bullet "Eingriff/Aufbereitung" already parsed)
# ---------------------------------------------------------------------------

AUFBEREITUNG_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("aufbereitungsverfahren/Drahtglasschneiden",       ("drahtglas", "glasschneiden", "glasschnitt")),
    ("aufbereitungsverfahren/Entmoertelung_von_Fliesen",("entmoertelung", "entmortelung", "mortel entfernen", "moertel entfernen", "fliesen", "tile")),
    ("aufbereitungsverfahren/Holzaufbereitung",         ("holzaufbereitung", "holz", "hobeln", "schleifen", "sagen", "saegen", "trocknen", "holzbearbeitung")),
    ("aufbereitungsverfahren/Leuchten_Refurbishment",   ("leuchten", "lampe", "beleuchtung", "licht", "refurbishment", "refurbishing")),
    ("aufbereitungsverfahren/Qualitaetssicherung",      ("qualitaetssicherung", "qualitassicherung", "qualitats", "ce", "prufung", "pruefung", "testing", "test")),
    ("aufbereitungsverfahren/Rekonditionierung",        ("rekonditionierung", "recondition", "instandsetzung", "generaluberholung", "generalueberholung")),
    ("aufbereitungsverfahren/Reparatur",                ("reparatur", "repair", "ausbesserung", "flicken", "schweissen", "schweissung", "lochen gefult", "locher gefuellt")),
]


def build_aufbereitungsverfahren_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    """Reads the 'Eingriff/Aufbereitung' markdown bullet (same source as 50d/50e)."""
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_rows = [
        row for row in load_csv(NODE_INVENTORY)
        if row["entity"] == "reuse_einsatz"
    ]

    for node_row in sorted(reuse_rows, key=lambda r: r["typed_path"]):
        markdown = load_reuse_markdown(node_row)
        raw_label = extract_markdown_bullet(markdown, "Eingriff/Aufbereitung")

        if not raw_label or is_uncertain(raw_label):
            stats["rows_without_label"] += 1
            continue

        frontmatter = parse_simple_frontmatter(markdown)
        if not reusable_enough(frontmatter):
            stats["rows_skipped_not_reusable"] += 1
            continue

        if node_row["typed_path"] in excluded_sources:
            stats["rows_skipped_by_abgrenzung"] += 1
            continue

        targets: list[str] = []
        for segment in re.split(r"[,;/]+", raw_label):
            seg = normalized(segment)
            if not seg or seg in UNCERTAIN_VALUES:
                continue
            for target, tokens in AUFBEREITUNG_RULES:
                if target not in existing_nodes:
                    continue
                if any(token in seg for token in tokens) and target not in targets:
                    targets.append(target)

        if not targets:
            stats["labels_without_match"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "raw_label": raw_label,
                "reason": "no_aufbereitung_token_match",
            })
            continue

        for target in targets:
            key = (node_row["typed_path"], "has_aufbereitungsverfahren", target)
            if key in existing_keys:
                stats["duplicates_skipped"] += 1
                continue
            target_entity, target_id = target.split("/", 1)
            addition = {
                "source": node_row["typed_path"],
                "source_entity": "reuse_einsatz",
                "source_id": node_row["id"],
                "relation": "has_aufbereitungsverfahren",
                "target": target,
                "target_entity": target_entity,
                "target_id": target_id,
                "field": "BAUTEIL-INVENTAR:Eingriff/Aufbereitung",
                "raw_label": raw_label,
                "confidence": "rule_high",
                "resolution_rule": "label_50j_has_aufbereitungsverfahren_eingriff",
                "legacy_path": "",
                "original_source": node_row["typed_path"],
                "original_relation": "has_aufbereitungsverfahren",
                "original_target": target,
                "edge_cleaning": "added_gap_50j",
            }
            additions.append(addition)
            existing_keys.add(key)

    stats["reuse_rows_scanned"] = len(reuse_rows)
    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


# ---------------------------------------------------------------------------
# 50u — has_methode (Eingriff/Aufbereitung bullet → methode/)
# ---------------------------------------------------------------------------

METHODE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("methode/Abrissmonitoring", ("abbrissmonitoring", "abbruchmonitoring", "monitoring abriss", "abriss-monitoring")),
    ("methode/Bauteilkatalogisierung", ("bauteilkatalog", "katalogisierung", "bestandskatalog", "inventarkatalog")),
    (
        "methode/Building_Material_Scouting",
        ("material scouting", "bauteilsuche", "component hunting", "material scout"),
    ),
    (
        "methode/Design_for_Disassembly",
        ("design for disassembly", "dfd", "disassembly design", "demontierbares konstruktiv", "demontierbare konstrukt"),
    ),
    (
        "methode/Form_Follows_Availability",
        (
            "form follows availability",
            "entwurf aus verfugbarkeit",
            "entwurf aus verfügbarkeit",
            "design from stock",
            "design from availability",
        ),
    ),
    (
        "methode/Materialinventur",
        ("materialinventur", "materialinventar", "bestandsaufnahme", "inventur", "as-built inventar"),
    ),
    (
        "methode/Pre_Deconstruction_Audit",
        (
            "pre-deconstruction",
            "predeconstruction",
            "pre deconstruction",
            "abbruchaudit",
            "deconstruction audit",
            "vorabbruch",
            "preabbruch",
        ),
    ),
    (
        "methode/ReUse_Assessment",
        ("reuse assessment", "re-use assessment", "reuse-bewertung", "bewertung wiederverwend"),
    ),
    (
        "methode/ReUse_Ausschreibung",
        ("reuse-ausschreibung", "reuse ausschreibung", "ausschreibung reuse"),
    ),
    (
        "methode/Reversibilitaet",
        ("reversibilitaet", "reversibilität", "reversible konstruktion", "wiederausbaubar", "rueckbaubar geplant"),
    ),
    ("methode/Urban_Mining", ("urban mining", "urban-mining", "materialpass", "material passport")),
    (
        "methode/Wiederverwendungskriterien",
        ("wiederverwendungskriterien", "reuse kriterien", "kriterien wiederverwend"),
    ),
    (
        "methode/Zirkulaere_Ausschreibung",
        ("zirkulaere ausschreibung", "zirkuläre ausschreibung", "kreislauf ausschreibung", "circular tender"),
    ),
]


def build_methode_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    """Reads the Eingriff/Aufbereitung bullet (same source as 50d/50e/50j)."""
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_rows = [
        row for row in load_csv(NODE_INVENTORY)
        if row["entity"] == "reuse_einsatz"
    ]

    for node_row in sorted(reuse_rows, key=lambda r: r["typed_path"]):
        markdown = load_reuse_markdown(node_row)
        raw_label = extract_markdown_bullet(markdown, "Eingriff/Aufbereitung")

        if not raw_label or is_uncertain(raw_label):
            stats["rows_without_label"] += 1
            continue

        frontmatter = parse_simple_frontmatter(markdown)
        if not reusable_enough(frontmatter):
            stats["rows_skipped_not_reusable"] += 1
            continue

        if node_row["typed_path"] in excluded_sources:
            stats["rows_skipped_by_abgrenzung"] += 1
            continue

        targets: list[str] = []
        for segment in re.split(r"[,;/]+", raw_label):
            seg = normalized(segment)
            if not seg or seg in UNCERTAIN_VALUES:
                continue
            for target, tokens in METHODE_RULES:
                if target not in existing_nodes:
                    continue
                if any(token in seg for token in tokens) and target not in targets:
                    targets.append(target)

        if not targets:
            stats["labels_without_match"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "raw_label": raw_label,
                "reason": "no_methode_token_match",
            })
            continue

        for target in targets:
            key = (node_row["typed_path"], "has_methode", target)
            if key in existing_keys:
                stats["duplicates_skipped"] += 1
                continue
            target_entity, target_id = target.split("/", 1)
            addition = {
                "source": node_row["typed_path"],
                "source_entity": "reuse_einsatz",
                "source_id": node_row["id"],
                "relation": "has_methode",
                "target": target,
                "target_entity": target_entity,
                "target_id": target_id,
                "field": "BAUTEIL-INVENTAR:Eingriff/Aufbereitung",
                "raw_label": raw_label,
                "confidence": "rule_high",
                "resolution_rule": "label_50u_has_methode_eingriff",
                "legacy_path": "",
                "original_source": node_row["typed_path"],
                "original_relation": "has_methode",
                "original_target": target,
                "edge_cleaning": "added_gap_50u",
            }
            additions.append(addition)
            existing_keys.add(key)

    stats["reuse_rows_scanned"] = len(reuse_rows)
    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


# ---------------------------------------------------------------------------
# 50k -- has_logistik
# ---------------------------------------------------------------------------

LOGISTIK_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("logistik/Bauteiltracking", (
        "bauteiltracking", "track-and-trace", "track and trace", "tracking",
        "barcode", "qr", "bauteil-id", "bauteil id", "chain of custody",
        "materialpass", "material passport",
    )),
    ("logistik/Just_in_Time", (
        "just-in-time", "just in time", "justintime", "direkttransport",
        "direktanlieferung", "source-to-site", "direct-to-site",
        "donor-to-site", "ohne zwischenlager", "ohne lager",
    )),
    ("logistik/Lagerflaeche", (
        "lagerflaeche", "lagerflache", "lagerflächen", "lagerflachen",
        "lagerplatz", "lagerplaetze", "lagerplatze", "platzbedarf",
        "wenig platz", "flaechenbedarf", "flachenbedarf", "storage space",
    )),
    ("logistik/Lokale_Wiederverwendung", (
        "lokal", "lokale", "lokaler", "lokales", "regional", "regionale",
        "vor ort", "am ort", "same-site", "same site", "on-site", "onsite",
        "in situ", "projektgebiet", "kurze distanz", "kurze wege",
        "kurze lokale", "lokale materialkreislaeufe", "lokale materialkreislaufe",
    )),
    ("logistik/Materialmatching", (
        "materialmatching", "matching", "materialsuche", "bauteilsuche",
        "component hunting", "design from availability", "entwurf folgt",
        "geeignete profile", "geeignete bauteile",
        "urban mining nach", "bauteile gesucht", "quellen gesucht",
    )),
    ("logistik/Materialverfuegbarkeit", (
        "materialverfuegbarkeit", "materialverfugbarkeit", "verfuegbar",
        "verfugbar", "verfuegbarkeit", "verfugbarkeit", "available",
        "availability", "illiquide", "lieferzeit", "vor produktion verfuegbar",
        "vor produktion verfugbar", "stockholder als puffer",
    )),
    ("logistik/Transport", (
        "transport", "transportiert", "transportkette", "trailer",
        "tieflader", "lkw", "truck", "spedition", "anlieferung",
        "lieferung", "baustelle bewegt", "donor ->",
        "spender ->", "stockholder ->", "quelle ->",
    )),
    ("logistik/Transportdistanz", (
        "transportdistanz", "transportentfernung", "kilometer",
        "fahrstrecke", "radius", " km", "km ", "miles", "mile",
    )),
    ("logistik/Zwischenlagerung", (
        "zwischenlager", "zwischengelagert", "zwischenlagerung",
        "pufferlager", "stockpile", "stockpiling", "stockholder",
    )),
    ("logistik/Lagerung", (
        "lagerung", "gelagert", "lagern", "einlagerung", "lagerverwaltung",
        "lager", "storage", "stockholder", "warehouse", "materiallager",
        "bereitstellung",
    )),
]

LOGISTIK_DISTANCE_RE = re.compile(r"\b\d+(?:[,.]\d+)?\s*(?:km|kilometer|mile|miles)\b")

LOGISTIK_CASE_WIDE_TOKENS = (
    "gesamtprojekt",
    "alle wiederverwend",
    "alle reuse",
    "materialien und herkunft",
    "materialien aus unterschiedlichen",
    "materialien aus verschiedenen",
    "unterschiedliche quellen",
    "verschiedene quellen",
    "mehrere quellen",
    "projektgebiet",
    "lokale materiallager",
    "materiallager",
    "materialbank",
    "gebaeudestock",
    "gebaudestock",
    "materialpasse",
    "produktpasse",
    "delivery and waste tickets",
    "bis einbau gelagert",
)

LOGISTIK_COMPONENT_STOPWORDS = {
    "aber", "alle", "alte", "alter", "bauteil", "bauteile", "bestand",
    "direct", "direkte", "einsatz", "fallstudie", "funktion", "gesamt",
    "herkunft", "keine", "label", "material", "materialien", "menge",
    "neue", "neuer", "neues", "projekt", "quelle", "quellen", "reclaim",
    "reclaimed", "reuse", "umfang", "unbekannt", "unklar", "verschiedene",
    "wiederverwendung",
}


def extract_logistik_rows() -> dict[str, list[dict[str, str]]]:
    """Return case-level rows from each Gebaeude "PROZESS UND LOGISTIK" table."""
    source_dir = gebaeude_dir()
    rows_by_case: dict[str, list[dict[str, str]]] = defaultdict(list)
    for path in sorted(source_dir.glob("*.md")):
        markdown = path.read_text(encoding="utf-8", errors="replace")
        section = markdown_section(markdown, "PROZESS UND LOGISTIK")
        if not section:
            continue
        for row in parse_markdown_tables(section):
            values = {
                "case_id": path.stem,
                "legacy_path": str(path.relative_to(ROOT)),
                "prozessphase": get_cell(row, "Prozessphase"),
                "handlung": get_cell(row, "Handlung"),
                "methode": get_cell(row, "Methode"),
                "werkzeug": get_cell(row, "Werkzeug/Tool/Software"),
                "logistik": get_cell(row, "Logistik"),
                "huerde": get_cell(row, "Huerde"),
                "loesung": get_cell(row, "Loesung"),
            }
            raw_label = " | ".join(
                part for part in (
                    values["prozessphase"],
                    values["handlung"],
                    values["methode"],
                    values["werkzeug"],
                    values["logistik"],
                    values["huerde"],
                    values["loesung"],
                )
                if part and not is_uncertain(part)
            )
            match_label = " | ".join(
                part for part in (
                    values["handlung"],
                    values["methode"],
                    values["werkzeug"],
                    values["logistik"],
                    values["huerde"],
                    values["loesung"],
                )
                if part and not is_uncertain(part)
            )
            if not raw_label:
                continue
            values["raw_label"] = raw_label
            values["match_label"] = match_label
            rows_by_case[path.stem].append(values)
    return rows_by_case


def map_logistik_targets(raw_label: str, existing_nodes: set[str]) -> list[str]:
    label = normalized(raw_label)
    if not label or label in UNCERTAIN_VALUES:
        return []

    targets: list[str] = []

    def add(target: str) -> None:
        if target in existing_nodes and target not in targets:
            targets.append(target)

    if LOGISTIK_DISTANCE_RE.search(label):
        add("logistik/Transportdistanz")

    for target, tokens in LOGISTIK_RULES:
        if any(token in label for token in tokens):
            add(target)

    # Avoid redundant general Lagerung when the source only says Zwischenlager.
    if "logistik/Zwischenlagerung" in targets and "logistik/Lagerung" in targets:
        if "lagerflaeche" not in label and "lagerflache" not in label and "lagerung" not in label:
            targets.remove("logistik/Lagerung")
    if "logistik/Lagerung" in targets and "auflagerung" in label:
        if not any(token in label for token in ("einlagerung", "gelagert", "lagern", "lagerbestand", "lagerrest")):
            targets.remove("logistik/Lagerung")

    return targets


def logistics_confidence(raw_label: str, source_kind: str) -> str:
    label = normalized(raw_label)
    if source_kind == "component":
        if any(token in label for token in PROCESS_MEDIUM_CONFIDENCE_TOKENS):
            return "rule_medium"
        return "rule_high"
    return "rule_medium"


def component_tokens_for_logistik(frontmatter: dict[str, str]) -> set[str]:
    text = " | ".join([
        frontmatter.get("bauteil_label", ""),
        frontmatter.get("material_label", ""),
        frontmatter.get("herkunft_label", ""),
        frontmatter.get("alte_funktion", ""),
        frontmatter.get("neue_funktion", ""),
    ])
    tokens = set()
    for token in re.findall(r"[a-z0-9]+", normalized(text)):
        if len(token) < 4:
            continue
        if token in LOGISTIK_COMPONENT_STOPWORDS:
            continue
        tokens.add(token)
    return tokens


def process_logistik_applies_to_reuse(match_label: str, frontmatter: dict[str, str]) -> bool:
    label = normalized(match_label)
    if any(token in label for token in LOGISTIK_CASE_WIDE_TOKENS):
        return True
    tokens = component_tokens_for_logistik(frontmatter)
    return any(token in label for token in tokens)


def build_logistik_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_by_case = load_reuse_nodes()
    reuse_rows = [
        row for rows in reuse_by_case.values()
        for row in rows
    ]

    reusable_by_case: dict[str, list[tuple[dict[str, str], dict[str, str], str]]] = defaultdict(list)
    for node_row in sorted(reuse_rows, key=lambda row: row["typed_path"]):
        markdown = load_reuse_markdown(node_row)
        frontmatter = parse_simple_frontmatter(markdown)
        case_id = node_row["id"].split("__", 1)[0]

        if not reusable_enough(frontmatter):
            stats["rows_skipped_not_reusable"] += 1
            continue
        if node_row["typed_path"] in excluded_sources:
            stats["rows_skipped_by_abgrenzung"] += 1
            continue

        reusable_by_case[case_id].append((node_row, frontmatter, markdown))

        component_labels = [
            ("FRONTMATTER:herkunft_label", frontmatter.get("herkunft_label", "")),
            ("FRONTMATTER:huerde_label", frontmatter.get("huerde_label", "")),
            ("BAUTEIL-INVENTAR:Eingriff/Aufbereitung", extract_markdown_bullet(markdown, "Eingriff/Aufbereitung")),
        ]

        for field, raw_label in component_labels:
            raw_label = (raw_label or "").strip()
            if not raw_label or is_uncertain(raw_label):
                stats["component_labels_empty"] += 1
                continue
            targets = map_logistik_targets(raw_label, existing_nodes)
            if not targets:
                stats["component_labels_without_match"] += 1
                continue

            for target in targets:
                key = (node_row["typed_path"], "has_logistik", target)
                if key in existing_keys:
                    stats["duplicates_skipped"] += 1
                    continue
                target_entity, target_id = target.split("/", 1)
                additions.append({
                    "source": node_row["typed_path"],
                    "source_entity": "reuse_einsatz",
                    "source_id": node_row["id"],
                    "relation": "has_logistik",
                    "target": target,
                    "target_entity": target_entity,
                    "target_id": target_id,
                    "field": field,
                    "raw_label": raw_label,
                    "confidence": logistics_confidence(raw_label, "component"),
                    "resolution_rule": "label_50k_has_logistik_component_label",
                    "legacy_path": "",
                    "original_source": node_row["typed_path"],
                    "original_relation": "has_logistik",
                    "original_target": target,
                    "edge_cleaning": "added_gap_50k",
                })
                existing_keys.add(key)

    logistik_rows = extract_logistik_rows()
    for case_id, case_rows in sorted(logistik_rows.items()):
        case_reuse_rows = reusable_by_case.get(case_id, [])
        if not case_reuse_rows:
            stats["process_cases_without_reusable_rows"] += 1
            continue

        for process_row in case_rows:
            raw_label = process_row["raw_label"]
            match_label = process_row.get("match_label", raw_label)
            targets = map_logistik_targets(match_label, existing_nodes)
            if not targets:
                stats["process_rows_without_match"] += 1
                skipped.append({
                    "case_id": case_id,
                    "legacy_path": process_row["legacy_path"],
                    "raw_label": raw_label,
                    "reason": "no_logistik_token_match",
                })
                continue

            for node_row, frontmatter, _markdown in case_reuse_rows:
                if not process_logistik_applies_to_reuse(match_label, frontmatter):
                    stats["process_source_rows_skipped_no_component_match"] += 1
                    continue
                for target in targets:
                    key = (node_row["typed_path"], "has_logistik", target)
                    if key in existing_keys:
                        stats["duplicates_skipped"] += 1
                        continue
                    target_entity, target_id = target.split("/", 1)
                    additions.append({
                        "source": node_row["typed_path"],
                        "source_entity": "reuse_einsatz",
                        "source_id": node_row["id"],
                        "relation": "has_logistik",
                        "target": target,
                        "target_entity": target_entity,
                        "target_id": target_id,
                        "field": "PROZESS UND LOGISTIK",
                        "raw_label": raw_label,
                        "confidence": logistics_confidence(raw_label, "process"),
                        "resolution_rule": "table_50k_has_logistik_process_logistik",
                        "legacy_path": process_row["legacy_path"],
                        "original_source": node_row["typed_path"],
                        "original_relation": "has_logistik",
                        "original_target": target,
                        "edge_cleaning": "added_gap_50k",
                    })
                    existing_keys.add(key)

    stats["reuse_rows_scanned"] = len(reuse_rows)
    stats["process_cases_scanned"] = len(logistik_rows)
    stats["process_rows_scanned"] = sum(len(rows) for rows in logistik_rows.values())
    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


# ---------------------------------------------------------------------------
# 50l -- has_wirtschaft
# ---------------------------------------------------------------------------

WIRTSCHAFT_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("wirtschaft/Finanzierung", (
        "finanzierung", "foerderung", "foerderprogramm",
        "grant", "subvention", "hlf", "ausfuehrungskredit",
        "ausfuhrungskredit", "kredit", "foerdermittel",
        "fordermittel", "finanziert", "investor", "investment",
    )),
    ("wirtschaft/Geschaeftsmodell", (
        "geschaeftsmodell", "geschaftsmodell", "business model",
        "business case", "stockholder", "stockist", "stockholder model",
        "reuse centre", "reuse-center", "reuse haendler", "reuse handler",
        "haendler", "handler", "direktdeal", "direct deal", "free-issue",
        "free issue", "bauteilboerse", "bauteilborse", "marktplatz",
        "plattform", "materialpool", "materialpools", "stockholder als puffer",
        "take-back", "take back", "leasing", "product-as-a-service",
    )),
    ("wirtschaft/Kostenvergleich", (
        "kostenvergleich", "kostenwirkung", "kostenneutral",
        "kostenneutr", "vergleichbar", "vergleichspreis", "einspar",
        "erspar", "mehrkosten", "kostenvorteil", "kostennachteil",
        "rohbaukostenvorteil", "kosteneinspar", "guenstiger",
        "gunstiger", "billiger", "teurer", "niedriger",
        "keine gesamtersparnis", "keine echte gesamtersparnis",
        "keine gesamtkosteneinsparung", "gesamteinsparung",
        "materialkosten", "baukosten", "projektkosten", "kostenstruktur",
        "arbeitsaufwand", "aufbereitungskosten", "lagerkosten",
        "budget", "wirtschaftlichkeit", "wirtschaftlich",
    )),
    ("wirtschaft/Lebenszykluskosten", (
        "lebenszykluskosten", "lcc", "life-cycle cost", "life cycle cost",
        "lifecycle cost", "whole life", "betriebskosten", "wartungskosten",
        "unterhaltskosten", "maintenance cost", "nutzungsdauer",
        "nutzungszeitraum",
    )),
    ("wirtschaft/Preisbildung", (
        "preisbildung", "materialpreis", "neupreis", "marktpreis",
        "vergleichspreis", "preisvorteil", "preisreduktion", "preis",
        "marginally cheaper", "cheaper", "free-issue", "free issue",
        "verkauf", "kaufpreis", "ankauf", "angebotspreis",
        "marktliquiditaet", "marktliquiditat", "illiquider markt",
        "liquider markt", "preisaufschlag", "risikoaufschlag",
    )),
    ("wirtschaft/Restwert", (
        "restwert", "materialwert", "marktwert", "wiederverkaufswert",
        "residual value", "schrottwert", "vermoegenswert",
        "vermogenswert", "asset", "werterhalt", "wert der bauteile",
    )),
]

WIRTSCHAFT_SKIP_PHRASES = (
    "kosten unbekannt",
    "kostenwirkung unbekannt",
    "genaue kosten unbekannt",
    "keine kostenwerte",
    "keine kostenkennwerte",
    "keine kostendaten",
    "keine kosten erfinden",
    "keine bauteilborse belegt",
    "keine bauteilboerse belegt",
    "keine klassische bauteilborse",
    "keine klassische bauteilboerse",
    "keine bestehende bauteilborse",
    "keine bestehende bauteilboerse",
    "keine belastbaren daten",
    "keine belastbaren werte",
    "keine reuse-kostenzahlen",
    "keine reuse kostenzahlen",
    "nicht belastbar",
    "nicht reuse-spezifisch",
    "nicht reuse spezifisch",
    "nicht gefunden",
    "unbekannt | kosten",
    "unbekannt | kostenwirkung",
)

WIRTSCHAFT_HARD_SKIP_PHRASES = (
    "kostenwirkung reuse nicht belastbar",
    "gesamtprojekt, nicht reuse",
    "gesamtprojekt nicht reuse",
    "nicht reuse-spezifisch",
    "nicht reuse spezifisch",
    "direct-reuse-fall nicht gebaut",
    "direct reuse fall nicht gebaut",
    "nicht mit realisierter direct-reuse",
    "nicht mit realisierter direct reuse",
    "keine kostenkennwerte gefunden",
)

WIRTSCHAFT_STRONG_TOKENS = (
    "einspar", "erspar", "mehrkosten", "kostenneutral", "vergleichbar",
    "vergleichspreis", "guenstiger", "gunstiger", "billiger", "teurer",
    "niedriger", "preis", "budget", "foerder", "kredit",
    "finanz", "business case", "stockholder", "free-issue", "free issue",
    "marktliquid", "illiquider markt", "restwert", "materialwert",
    "projektkosten", "baukosten", "rohbaukostenvorteil", "kostenstruktur",
    "arbeitsaufwand", "aufbereitungskosten", "lagerkosten",
)

WIRTSCHAFT_RELEVANT_BULLET_LABELS = {
    "beschaffungsmodell",
    "bauteilborse / quelle",
    "bauteilboerse / quelle",
    "kostenwirkung",
    "arbeitsaufwand",
    "marktbarrieren",
}

WIRTSCHAFT_CASE_WIDE_TOKENS = (
    "gesamtprojekt",
    "projektkosten",
    "baukosten",
    "kostenrahmen",
    "ausfuehrungskredit",
    "ausfuhrungskredit",
    "budget sozialer wohnungsbau",
    "vergleichbare kosten gegenueber konventioneller bauweise",
    "vergleichbare kosten gegenuber konventioneller bauweise",
    "kosten etwa vergleichbar",
    "kosten im rahmen eines vergleichbaren neubaus",
    "kostenstudie",
    "wirtschaftsauswertung",
)

WIRTSCHAFT_COMPONENT_MARKERS = (
    "stahl", "steel", "hcs", "hohlkorper", "hollow", "fenster",
    "window", "ziegel", "brick", "holz", "timber", "tuer", "tur",
    "door", "platte", "platten", "slab", "beton", "concrete",
    "aluminium", "glas", "glass", "pflaster", "naturstein", "stone",
    "granit", "radiator", "leuchten", "sanitar", "treppe", "trager",
    "stuetze", "stutze", "fassade", "dach", "decke", "wand",
    "fliesen", "tile", "profile", "profil",
)

WIRTSCHAFT_BROAD_ROW_PREFIXES = (
    "beschaffungsmodell:",
    "bauteilborse / quelle:",
    "bauteilboerse / quelle:",
    "arbeitsaufwand:",
    "marktbarrieren:",
)


def wirtschaft_label_is_useful(raw_label: str) -> bool:
    label = normalized(raw_label)
    if not label or label in UNCERTAIN_VALUES:
        return False
    if any(phrase in label for phrase in WIRTSCHAFT_HARD_SKIP_PHRASES):
        return False
    if any(phrase in label for phrase in WIRTSCHAFT_SKIP_PHRASES):
        if not any(token in label for token in WIRTSCHAFT_STRONG_TOKENS) and not re.search(r"\d", label):
            return False
    if "unbekannt" in label or "unklar" in label:
        if not any(token in label for token in WIRTSCHAFT_STRONG_TOKENS) and not re.search(r"\d", label):
            return False
    return True


def map_wirtschaft_targets(raw_label: str, existing_nodes: set[str]) -> list[str]:
    label = normalized(raw_label)
    if not wirtschaft_label_is_useful(raw_label):
        return []

    targets: list[str] = []

    def add(target: str) -> None:
        if target in existing_nodes and target not in targets:
            targets.append(target)

    for target, tokens in WIRTSCHAFT_RULES:
        if any(token in label for token in tokens):
            add(target)

    if re.search(r"\bforder(ung|mittel|programm)\b", label):
        add("wirtschaft/Finanzierung")

    # If a source gives hard cost numbers but only says "Kosten", keep it as
    # project-level cost comparison rather than leaving it unmapped.
    if not targets and re.search(r"\d", label) and any(token in label for token in ("kosten", "eur", "euro", "gbp", "usd", "chf")):
        add("wirtschaft/Kostenvergleich")

    return targets


def wirtschaft_row_applies_to_reuse(raw_label: str, frontmatter: dict[str, str]) -> bool:
    label = normalized(raw_label)
    if "nicht gesamtprojekt" not in label and any(token in label for token in WIRTSCHAFT_CASE_WIDE_TOKENS):
        return True

    component_tokens = component_tokens_for_logistik(frontmatter)
    if any(token in label for token in component_tokens):
        return True

    # If the row names a concrete component/material but this reuse item does
    # not share that component token, do not copy the edge to every item.
    if any(marker in label for marker in WIRTSCHAFT_COMPONENT_MARKERS):
        return False

    if label.startswith(WIRTSCHAFT_BROAD_ROW_PREFIXES):
        return True

    return True


def wirtschaft_confidence(raw_label: str, confidence_source: str = "") -> str:
    source_confidence = normalized(confidence_source)
    label = normalized(raw_label)
    if source_confidence == "belegt":
        return "rule_high"
    if "teilweise" in source_confidence or "quellenkonflikt" in source_confidence:
        return "rule_medium"
    if any(token in label for token in ("unbekannt", "unklar", "wahrscheinlich", "nicht belastbar")):
        return "rule_low"
    return "rule_medium"


def parse_markdown_bullets(section: str) -> list[tuple[str, str]]:
    bullets: list[tuple[str, str]] = []
    for line in section.splitlines():
        match = re.match(r"^-\s+\*\*(.+?):\*\*\s*(.*)$", line.strip())
        if match:
            bullets.append((match.group(1).strip(), match.group(2).strip()))
    return bullets


def extract_wirtschaft_rows() -> dict[str, list[dict[str, str]]]:
    source_dir = gebaeude_dir()
    rows_by_case: dict[str, list[dict[str, str]]] = defaultdict(list)

    for path in sorted(source_dir.glob("*.md")):
        markdown = path.read_text(encoding="utf-8", errors="replace")
        case_id = path.stem
        legacy_path = str(path.relative_to(ROOT))

        ent_section = markdown_section(markdown, "ENTIT")
        for row in parse_markdown_tables(ent_section):
            entity = normalized(get_cell(row, "Entitat"))
            if "wirtschaft" not in entity:
                continue
            raw_label = " | ".join(
                part for part in (
                    get_cell(row, "Wert"),
                    get_cell(row, "Beziehung zur Fallstudie"),
                    get_cell(row, "Anmerkung"),
                )
                if part and not is_uncertain(part)
            )
            if raw_label:
                rows_by_case[case_id].append({
                    "case_id": case_id,
                    "legacy_path": legacy_path,
                    "field": "ENTITAETEN-MAPPING:Wirtschaft",
                    "raw_label": raw_label,
                    "confidence_source": get_cell(row, "Vertrauensgrad"),
                })

        wirtschaft_section = markdown_section(markdown, "WIRTSCHAFT")
        for label, value in parse_markdown_bullets(wirtschaft_section):
            label_norm = normalized(label)
            if label_norm not in {normalized(item) for item in WIRTSCHAFT_RELEVANT_BULLET_LABELS}:
                continue
            if not value or is_uncertain(value):
                continue
            rows_by_case[case_id].append({
                "case_id": case_id,
                "legacy_path": legacy_path,
                "field": f"WIRTSCHAFT UND BESCHAFFUNG:{label}",
                "raw_label": f"{label}: {value}",
                "confidence_source": "",
            })

        kennwerte_section = markdown_section(markdown, "KENNWERTE")
        for row in parse_markdown_tables(kennwerte_section):
            raw_label = " | ".join(value for value in row.values() if value and not is_uncertain(value))
            raw_norm = normalized(raw_label)
            if not any(token in raw_norm for token in ("kosten", "preis", "budget", "finanz", "restwert", "marktwert")):
                continue
            rows_by_case[case_id].append({
                "case_id": case_id,
                "legacy_path": legacy_path,
                "field": "KENNWERTE",
                "raw_label": raw_label,
                "confidence_source": get_cell(row, "Datenqualitat") or get_cell(row, "Datenqualitaet"),
            })

        huerden_section = markdown_section(markdown, "HURDEN")
        for row in parse_markdown_tables(huerden_section):
            raw_label = " | ".join(value for value in row.values() if value and not is_uncertain(value))
            raw_norm = normalized(raw_label)
            if not any(token in raw_norm for token in ("wirtschaft", "kosten", "preis", "markt", "finanz", "budget", "restwert")):
                continue
            rows_by_case[case_id].append({
                "case_id": case_id,
                "legacy_path": legacy_path,
                "field": "HUERDEN-MATRIX",
                "raw_label": raw_label,
                "confidence_source": "",
            })

    return rows_by_case


def build_wirtschaft_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_by_case = load_reuse_nodes()
    wirtschaft_rows = extract_wirtschaft_rows()

    reusable_by_case: dict[str, list[tuple[dict[str, str], dict[str, str]]]] = defaultdict(list)
    for case_id, rows in sorted(reuse_by_case.items()):
        for node_row in sorted(rows, key=lambda row: row["typed_path"]):
            markdown = load_reuse_markdown(node_row)
            frontmatter = parse_simple_frontmatter(markdown)
            if not reusable_enough(frontmatter):
                stats["rows_skipped_not_reusable"] += 1
                continue
            if node_row["typed_path"] in excluded_sources:
                stats["rows_skipped_by_abgrenzung"] += 1
                continue
            reusable_by_case[case_id].append((node_row, frontmatter))

            component_labels = [
                ("FRONTMATTER:huerde_label", frontmatter.get("huerde_label", "")),
                ("BAUTEIL-INVENTAR:Eingriff/Aufbereitung", extract_markdown_bullet(markdown, "Eingriff/Aufbereitung")),
            ]
            for field, raw_label in component_labels:
                raw_label = (raw_label or "").strip()
                if not raw_label or is_uncertain(raw_label):
                    stats["component_labels_empty"] += 1
                    continue
                targets = map_wirtschaft_targets(raw_label, existing_nodes)
                if not targets:
                    stats["component_labels_without_match"] += 1
                    continue
                for target in targets:
                    key = (node_row["typed_path"], "has_wirtschaft", target)
                    if key in existing_keys:
                        stats["duplicates_skipped"] += 1
                        continue
                    target_entity, target_id = target.split("/", 1)
                    additions.append({
                        "source": node_row["typed_path"],
                        "source_entity": "reuse_einsatz",
                        "source_id": node_row["id"],
                        "relation": "has_wirtschaft",
                        "target": target,
                        "target_entity": target_entity,
                        "target_id": target_id,
                        "field": field,
                        "raw_label": raw_label,
                        "confidence": wirtschaft_confidence(raw_label),
                        "resolution_rule": "label_50l_has_wirtschaft_component_label",
                        "legacy_path": "",
                        "original_source": node_row["typed_path"],
                        "original_relation": "has_wirtschaft",
                        "original_target": target,
                        "edge_cleaning": "added_gap_50l",
                    })
                    existing_keys.add(key)

    for case_id, rows in sorted(wirtschaft_rows.items()):
        case_reuse_rows = reusable_by_case.get(case_id, [])
        if not case_reuse_rows:
            stats["wirtschaft_cases_without_reusable_rows"] += 1
            continue
        for wirtschaft_row in rows:
            raw_label = wirtschaft_row["raw_label"]
            targets = map_wirtschaft_targets(raw_label, existing_nodes)
            if not targets:
                stats["wirtschaft_rows_without_match"] += 1
                skipped.append({
                    "case_id": case_id,
                    "legacy_path": wirtschaft_row["legacy_path"],
                    "raw_label": raw_label,
                    "reason": "no_wirtschaft_token_match_or_unusable_label",
                })
                continue
            for node_row, frontmatter in case_reuse_rows:
                if not wirtschaft_row_applies_to_reuse(raw_label, frontmatter):
                    stats["wirtschaft_source_rows_skipped_no_component_match"] += 1
                    continue
                for target in targets:
                    key = (node_row["typed_path"], "has_wirtschaft", target)
                    if key in existing_keys:
                        stats["duplicates_skipped"] += 1
                        continue
                    target_entity, target_id = target.split("/", 1)
                    additions.append({
                        "source": node_row["typed_path"],
                        "source_entity": "reuse_einsatz",
                        "source_id": node_row["id"],
                        "relation": "has_wirtschaft",
                        "target": target,
                        "target_entity": target_entity,
                        "target_id": target_id,
                        "field": wirtschaft_row["field"],
                        "raw_label": raw_label,
                        "confidence": wirtschaft_confidence(raw_label, wirtschaft_row.get("confidence_source", "")),
                        "resolution_rule": "table_50l_has_wirtschaft_case_economy",
                        "legacy_path": wirtschaft_row["legacy_path"],
                        "original_source": node_row["typed_path"],
                        "original_relation": "has_wirtschaft",
                        "original_target": target,
                        "edge_cleaning": "added_gap_50l",
                    })
                    existing_keys.add(key)

    stats["reuse_rows_scanned"] = sum(len(rows) for rows in reuse_by_case.values())
    stats["wirtschaft_cases_scanned"] = len(wirtschaft_rows)
    stats["wirtschaft_rows_scanned"] = sum(len(rows) for rows in wirtschaft_rows.values())
    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


# ---------------------------------------------------------------------------
# 50m -- has_rechtliche_bedingung
# ---------------------------------------------------------------------------

RECHT_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("rechtliche_bedingung/EU_Taxonomie", (
        "eu-taxonomie", "eu taxonomie", "taxonomy", "taxonomie",
        "taxonomy regulation", "dnsh",
    )),
    ("rechtliche_bedingung/Vergaberecht", (
        "vergaberecht", "vergabe", "ausschreibung", "ausschreibungs",
        "leistungsbeschreibung", "offentliche beschaffung",
        "oeffentliche beschaffung", "public procurement", "procurement",
        "tender", "bidding", "vergabedokument",
    )),
    ("rechtliche_bedingung/Gewaehrleistung", (
        "gewahrleistung", "warranty", "warranties", "garantie",
        "garantien", "standardgarantie", "mangelrechte",
        "mangelfrei", "beschaffenheitsvereinbarung",
    )),
    ("rechtliche_bedingung/Produkthaftung", (
        "produkthaftung", "produzentenhaftung", "product liability",
        "produktsicherheit", "inverkehrbringen", "herstellerrolle",
        "quasi-hersteller", "marktuberwachung", "marktueberwachung",
    )),
    ("rechtliche_bedingung/Zulassung_im_Einzelfall", (
        "zustimmung im einzelfall", "zulassung im einzelfall",
        "einzelfallzulassung", "einzelfallnachweis",
        "vorhabenbezogene bauartgenehmigung", "einzelfall",
        "zulassung", "bauproduktzulassung", "approval", "permitting",
        "ce marking", "ce/ukca", "ukca", "ce markiert",
        "ce-kennzeichnung", "ce konform", "konformitats",
        "konformitaets", "rezertifizierung", "re-zertifizierung",
    )),
    ("rechtliche_bedingung/Bauordnungsrecht", (
        "bauordnungs", "bauaufsicht", "baugenehmigung", "bauantrag",
        "baubewilligung", "baurecht", "baurechtlich", "bauvorschrift",
        "bauvorschriften",
        "building code", "building regulation", "regulatory",
        "regulation", "regulatorisch", "regulatorische", "ordinance",
        "verordnung", "regelwerk", "regelwerks", "behoerde", "behorde", "authorities",
        "genehmigung", "genehmigungs", "denkmalschutz", "heritage",
        "listed",
    )),
]

RECHT_SOURCE_TOKENS = tuple(
    sorted({token for _target, tokens in RECHT_RULES for token in tokens})
)

RECHT_HARD_SKIP_PATTERNS = (
    re.compile(r"^(?:versicherung / )?haftung:?\s*unbekannt\.?$"),
    re.compile(r"^gewahrleistung:?\s*unbekannt\.?$"),
    re.compile(r"^recht\s*\|\s*unbekannt\s*\|.*keine .*gefunden"),
)

RECHT_LOW_CONFIDENCE_TOKENS = (
    "unbekannt", "unklar", "keine details", "nicht dokumentiert",
    "nicht offentlich dokumentiert", "nicht oeffentlich dokumentiert",
    "vermutlich",
)

RECHT_EINZELFALL_ACRONYM_RE = re.compile(r"\b(?:zie|vbg)\b")

RECHT_SKIP_PHRASES = (
    "nicht reuse-spezifisch",
    "nicht reuse spezifisch",
)

RECHT_CERTIFICATION_CONTEXT_TOKENS = (
    "ecolabel", "nordic swan", "svanemaerket", "dgbc",
    "breeam", "leed", "dgnb", "well", "nabers", "paris proof",
)

RECHT_CERTIFICATION_LEGAL_OVERRIDE_TOKENS = (
    "baurecht", "bauaufsicht", "bauordnungs", "building regulation",
    "building regulations", "genehmigung", "genehmigungs", "haftung",
    "gewahrleistung", "insurance", "versicher", "brandschutz",
    "fire", "ce marking", "ce/ukca", "ukca", "en 1090",
)

RECHT_CASE_WIDE_TOKENS = (
    "gesamtprojekt", "reuse-bauteile", "reuse bauteile",
    "wiederverwendete bauteile", "gebrauchte bauteile",
    "gebrauchte materialien", "reuse-material", "reuse material",
    "genehmigung", "bauantrag", "bauaufsicht", "bauordnungs",
    "baurecht", "vergabe", "offentliche beschaffung",
    "oeffentliche beschaffung", "public procurement", "procurement",
    "zulassung/haftung", "zulassung und haftung", "haftung",
    "gewahrleistung", "warranty", "regulatory pathways",
    "regulatory", "building code",
)

RECHT_COMPONENT_MARKERS = WIRTSCHAFT_COMPONENT_MARKERS + (
    "brustung", "bruestung", "gelander", "gelaender", "kozijnen",
    "heizkorper", "heizkoerper", "lueftung", "luftung",
    "brandschutztuer", "brandschutztur", "aufzug", "lift",
    "fassadenelement", "doppelboden", "bodenelement",
)


def legal_text_is_unknown_only(raw_label: str) -> bool:
    label = normalized(raw_label).strip(" .;:-")
    if not label or label in UNCERTAIN_VALUES:
        return True
    return any(pattern.search(label) for pattern in RECHT_HARD_SKIP_PATTERNS)


def recht_label_is_useful(raw_label: str) -> bool:
    label = normalized(raw_label)
    if legal_text_is_unknown_only(raw_label):
        return False
    if any(phrase in label for phrase in RECHT_SKIP_PHRASES):
        return False
    if not any(token in label for token in RECHT_SOURCE_TOKENS):
        return False
    return True


def recht_certification_only(label: str) -> bool:
    if not any(token in label for token in RECHT_CERTIFICATION_CONTEXT_TOKENS):
        return False
    return not any(token in label for token in RECHT_CERTIFICATION_LEGAL_OVERRIDE_TOKENS)


def map_recht_targets(raw_label: str, existing_nodes: set[str]) -> list[str]:
    label = normalized(raw_label)
    if not recht_label_is_useful(raw_label):
        return []

    targets: list[str] = []

    def add(target: str) -> None:
        if target in existing_nodes and target not in targets:
            targets.append(target)

    certification_only = recht_certification_only(label)
    for target, tokens in RECHT_RULES:
        if target == "rechtliche_bedingung/Zulassung_im_Einzelfall" and certification_only:
            continue
        if any(token in label for token in tokens):
            add(target)

    if RECHT_EINZELFALL_ACRONYM_RE.search(label):
        add("rechtliche_bedingung/Zulassung_im_Einzelfall")

    return targets


def recht_confidence(raw_label: str, confidence_source: str = "") -> str:
    source_confidence = normalized(confidence_source)
    label = normalized(raw_label)
    if source_confidence == "belegt":
        return "rule_high"
    if "teilweise" in source_confidence or "quellenkonflikt" in source_confidence:
        return "rule_medium"
    if any(token in label for token in RECHT_LOW_CONFIDENCE_TOKENS):
        return "rule_low"
    return "rule_medium"


def extract_recht_rows() -> dict[str, list[dict[str, str]]]:
    source_dir = gebaeude_dir()
    rows_by_case: dict[str, list[dict[str, str]]] = defaultdict(list)

    for path in sorted(source_dir.glob("*.md")):
        markdown = path.read_text(encoding="utf-8", errors="replace")
        case_id = path.stem
        legacy_path = str(path.relative_to(ROOT))

        ent_section = markdown_section(markdown, "ENTIT")
        for row in parse_markdown_tables(ent_section):
            entity = normalized(get_cell(row, "Entitat"))
            if "recht" not in entity:
                continue
            raw_label = " | ".join(
                part for part in (
                    get_cell(row, "Wert"),
                    get_cell(row, "Beziehung zur Fallstudie"),
                    get_cell(row, "Anmerkung"),
                )
                if part and not is_uncertain(part)
            )
            if raw_label:
                rows_by_case[case_id].append({
                    "case_id": case_id,
                    "legacy_path": legacy_path,
                    "field": "ENTITAETEN-MAPPING:Recht",
                    "raw_label": raw_label,
                    "confidence_source": get_cell(row, "Vertrauensgrad"),
                })

        technik_section = markdown_section(markdown, "TECHNIK")
        for row in parse_markdown_tables(technik_section):
            raw_label = " | ".join(value for value in row.values() if value and not is_uncertain(value))
            if not raw_label:
                continue
            raw_norm = normalized(raw_label)
            if not any(token in raw_norm for token in RECHT_SOURCE_TOKENS):
                continue
            rows_by_case[case_id].append({
                "case_id": case_id,
                "legacy_path": legacy_path,
                "field": "TECHNIK, LEISTUNG, NORMEN",
                "raw_label": raw_label,
                "confidence_source": "",
            })

        huerden_section = markdown_section(markdown, "HURDEN")
        for row in parse_markdown_tables(huerden_section):
            raw_label = " | ".join(value for value in row.values() if value and not is_uncertain(value))
            if not raw_label:
                continue
            raw_norm = normalized(raw_label)
            if not any(token in raw_norm for token in RECHT_SOURCE_TOKENS):
                continue
            rows_by_case[case_id].append({
                "case_id": case_id,
                "legacy_path": legacy_path,
                "field": "HUERDEN-MATRIX",
                "raw_label": raw_label,
                "confidence_source": "",
            })

        wirtschaft_section = markdown_section(markdown, "WIRTSCHAFT")
        for label, value in parse_markdown_bullets(wirtschaft_section):
            if not value or legal_text_is_unknown_only(f"{label}: {value}"):
                continue
            raw_label = f"{label}: {value}"
            raw_norm = normalized(raw_label)
            if not any(token in raw_norm for token in RECHT_SOURCE_TOKENS):
                continue
            rows_by_case[case_id].append({
                "case_id": case_id,
                "legacy_path": legacy_path,
                "field": f"WIRTSCHAFT UND BESCHAFFUNG:{label}",
                "raw_label": raw_label,
                "confidence_source": "",
            })

    return rows_by_case


def recht_row_applies_to_reuse(raw_label: str, frontmatter: dict[str, str]) -> bool:
    label = normalized(raw_label)
    if any(token in label for token in RECHT_CASE_WIDE_TOKENS):
        return True

    component_tokens = component_tokens_for_logistik(frontmatter)
    if any(token in label for token in component_tokens):
        return True

    if any(marker in label for marker in RECHT_COMPONENT_MARKERS):
        return False

    return True


def build_rechtliche_bedingung_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_by_case = load_reuse_nodes()
    recht_rows = extract_recht_rows()

    reusable_by_case: dict[str, list[tuple[dict[str, str], dict[str, str]]]] = defaultdict(list)
    for case_id, rows in sorted(reuse_by_case.items()):
        for node_row in sorted(rows, key=lambda row: row["typed_path"]):
            markdown = load_reuse_markdown(node_row)
            frontmatter = parse_simple_frontmatter(markdown)
            if not reusable_enough(frontmatter):
                stats["rows_skipped_not_reusable"] += 1
                continue
            if node_row["typed_path"] in excluded_sources:
                stats["rows_skipped_by_abgrenzung"] += 1
                continue
            reusable_by_case[case_id].append((node_row, frontmatter))

            component_labels = [
                ("FRONTMATTER:norm_recht_label", frontmatter.get("norm_recht_label", "")),
                ("FRONTMATTER:huerde_label", frontmatter.get("huerde_label", "")),
                ("FRONTMATTER:pruefung_label", frontmatter.get("pruefung_label", "")),
                ("BAUTEIL-INVENTAR:Norm/Recht", extract_markdown_bullet(markdown, "Norm/Recht")),
                ("BAUTEIL-INVENTAR:Eingriff/Aufbereitung", extract_markdown_bullet(markdown, "Eingriff/Aufbereitung")),
            ]
            for field, raw_label in component_labels:
                raw_label = (raw_label or "").strip()
                if not raw_label or is_uncertain(raw_label):
                    stats["component_labels_empty"] += 1
                    continue
                targets = map_recht_targets(raw_label, existing_nodes)
                if not targets:
                    stats["component_labels_without_match"] += 1
                    continue
                for target in targets:
                    key = (node_row["typed_path"], "has_rechtliche_bedingung", target)
                    if key in existing_keys:
                        stats["duplicates_skipped"] += 1
                        continue
                    target_entity, target_id = target.split("/", 1)
                    additions.append({
                        "source": node_row["typed_path"],
                        "source_entity": "reuse_einsatz",
                        "source_id": node_row["id"],
                        "relation": "has_rechtliche_bedingung",
                        "target": target,
                        "target_entity": target_entity,
                        "target_id": target_id,
                        "field": field,
                        "raw_label": raw_label,
                        "confidence": recht_confidence(raw_label),
                        "resolution_rule": "label_50m_has_rechtliche_bedingung_component_label",
                        "legacy_path": "",
                        "original_source": node_row["typed_path"],
                        "original_relation": "has_rechtliche_bedingung",
                        "original_target": target,
                        "edge_cleaning": "added_gap_50m",
                    })
                    existing_keys.add(key)

    for case_id, rows in sorted(recht_rows.items()):
        case_reuse_rows = reusable_by_case.get(case_id, [])
        if not case_reuse_rows:
            stats["recht_cases_without_reusable_rows"] += 1
            continue
        for recht_row in rows:
            raw_label = recht_row["raw_label"]
            targets = map_recht_targets(raw_label, existing_nodes)
            if not targets:
                stats["recht_rows_without_match"] += 1
                skipped.append({
                    "case_id": case_id,
                    "legacy_path": recht_row["legacy_path"],
                    "raw_label": raw_label,
                    "reason": "no_recht_token_match_or_unusable_label",
                })
                continue
            for node_row, frontmatter in case_reuse_rows:
                if not recht_row_applies_to_reuse(raw_label, frontmatter):
                    stats["recht_source_rows_skipped_no_component_match"] += 1
                    continue
                for target in targets:
                    key = (node_row["typed_path"], "has_rechtliche_bedingung", target)
                    if key in existing_keys:
                        stats["duplicates_skipped"] += 1
                        continue
                    target_entity, target_id = target.split("/", 1)
                    additions.append({
                        "source": node_row["typed_path"],
                        "source_entity": "reuse_einsatz",
                        "source_id": node_row["id"],
                        "relation": "has_rechtliche_bedingung",
                        "target": target,
                        "target_entity": target_entity,
                        "target_id": target_id,
                        "field": recht_row["field"],
                        "raw_label": raw_label,
                        "confidence": recht_confidence(raw_label, recht_row.get("confidence_source", "")),
                        "resolution_rule": "table_50m_has_rechtliche_bedingung_case_law",
                        "legacy_path": recht_row["legacy_path"],
                        "original_source": node_row["typed_path"],
                        "original_relation": "has_rechtliche_bedingung",
                        "original_target": target,
                        "edge_cleaning": "added_gap_50m",
                    })
                    existing_keys.add(key)

    stats["reuse_rows_scanned"] = sum(len(rows) for rows in reuse_by_case.values())
    stats["recht_cases_scanned"] = len(recht_rows)
    stats["recht_rows_scanned"] = sum(len(rows) for rows in recht_rows.values())
    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


# ---------------------------------------------------------------------------
# 50n -- has_schadstoff
# ---------------------------------------------------------------------------

SCHADSTOFF_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("schadstoff/Asbest", (
        "asbest", "asbestos", "asbestzement",
    )),
    ("schadstoff/PCB", (
        "pcb", "polychlorierte biphenyle", "polychlorinated biphenyl",
    )),
    ("schadstoff/PAK", (
        "pak", "polyzyklische aromatische", "polycyclic aromatic",
        "teer", "teerhalt", "karbolineum", "benzo[a]pyren",
    )),
    ("schadstoff/Bleifarbe", (
        "bleifarbe", "bleihalt", "bleiweiss", "bleimennige",
        "lead paint", "lead-based paint",
    )),
    ("schadstoff/Holzschutzmittel", (
        "holzschutzmittel", "pcp", "lindan", "ddt", "hylotox",
        "chlororganische pestizide", "pestizid",
    )),
]

SCHADSTOFF_SOURCE_TOKENS = tuple(
    sorted({token for _target, tokens in SCHADSTOFF_RULES for token in tokens})
)

SCHADSTOFF_NEGATIVE_PHRASES = (
    "asbeststatus nicht belegt",
    "asbest status nicht belegt",
    "asbest nicht belegt",
    "asbest nicht nachgewiesen",
    "kein asbest",
    "keine annahme",
    "keine konkreten schadstoffe",
    "keine spezifischen schadstoffe",
    "keine gesicherten schadstoffangaben",
    "keine belastbare angabe",
    "keine belastbaren angaben",
    "schadstoff nicht belegt",
)

SCHADSTOFF_LOW_CONFIDENCE_TOKENS = (
    "moglich", "moeglich", "potenziell", "potentielle",
    "unklar", "unbekannt", "verdacht", "kann",
)

SCHADSTOFF_COMPONENT_MARKERS = WIRTSCHAFT_COMPONENT_MARKERS + (
    "fensterrahmen", "rahmen", "faserzement", "eternit",
    "aussenwandplatten", "aussenwand", "fugen",
    "fuge", "kitt", "farbe", "anstrich", "beschichtung",
    "parkett", "bodenbelag", "dachstuhl", "balken", "dielen",
    "plattenbau", "betonplatten", "betonfertigteile",
)

SCHADSTOFF_ACRONYM_TOKENS = {"pak", "pcb", "pcp"}

SCHADSTOFF_COMPONENT_STOPWORDS = LOGISTIK_COMPONENT_STOPWORDS | {
    "beton", "bauteil", "bauteile", "fertigteil", "fertigteile",
    "material", "materialien", "platte", "platten", "teile", "teil",
    "wiederverwendet", "wiederverwendete", "reuse", "direct",
    "direkt", "direkte", "unbekannt", "stoff", "stoffe",
    "wbs70", "wand", "wande", "waende", "innenwand", "decke", "dach",
}


def schadstoff_token_matches(label: str, token: str) -> bool:
    if token in SCHADSTOFF_ACRONYM_TOKENS:
        return re.search(rf"\b{re.escape(token)}\b", label) is not None
    return token in label


def schadstoff_label_is_useful(raw_label: str) -> bool:
    label = normalized(raw_label)
    if not label or label in UNCERTAIN_VALUES:
        return False
    if any(phrase in label for phrase in SCHADSTOFF_NEGATIVE_PHRASES):
        return False
    return any(schadstoff_token_matches(label, token) for token in SCHADSTOFF_SOURCE_TOKENS)


def map_schadstoff_targets(raw_label: str, existing_nodes: set[str]) -> list[str]:
    label = normalized(raw_label)
    if not schadstoff_label_is_useful(raw_label):
        return []

    targets: list[str] = []

    def add(target: str) -> None:
        if target in existing_nodes and target not in targets:
            targets.append(target)

    for target, tokens in SCHADSTOFF_RULES:
        if any(schadstoff_token_matches(label, token) for token in tokens):
            add(target)

    return targets


def schadstoff_confidence(raw_label: str, confidence_source: str = "") -> str:
    source_confidence = normalized(confidence_source)
    label = normalized(raw_label)
    if source_confidence == "belegt":
        return "rule_high"
    if "teilweise" in source_confidence or "quellenkonflikt" in source_confidence:
        return "rule_medium"
    if any(token in label for token in SCHADSTOFF_LOW_CONFIDENCE_TOKENS):
        return "rule_low"
    return "rule_medium"


def extract_schadstoff_rows() -> dict[str, list[dict[str, str]]]:
    source_dir = gebaeude_dir()
    rows_by_case: dict[str, list[dict[str, str]]] = defaultdict(list)

    for path in sorted(source_dir.glob("*.md")):
        markdown = path.read_text(encoding="utf-8", errors="replace")
        case_id = path.stem
        legacy_path = str(path.relative_to(ROOT))

        ent_section = markdown_section(markdown, "ENTIT")
        for row in parse_markdown_tables(ent_section):
            entity = normalized(get_cell(row, "Entitat"))
            if "schadstoff" not in entity:
                continue
            raw_label = " | ".join(
                part for part in (
                    get_cell(row, "Wert"),
                    get_cell(row, "Beziehung zur Fallstudie"),
                    get_cell(row, "Anmerkung"),
                )
                if part and not is_uncertain(part)
            )
            if raw_label:
                rows_by_case[case_id].append({
                    "case_id": case_id,
                    "legacy_path": legacy_path,
                    "field": "ENTITAETEN-MAPPING:Schadstoff",
                    "raw_label": raw_label,
                    "confidence_source": get_cell(row, "Vertrauensgrad"),
                })

        technik_section = markdown_section(markdown, "TECHNIK")
        for row in parse_markdown_tables(technik_section):
            raw_label = " | ".join(value for value in row.values() if value and not is_uncertain(value))
            if not raw_label:
                continue
            raw_norm = normalized(raw_label)
            if not any(schadstoff_token_matches(raw_norm, token) for token in SCHADSTOFF_SOURCE_TOKENS):
                continue
            rows_by_case[case_id].append({
                "case_id": case_id,
                "legacy_path": legacy_path,
                "field": "TECHNIK, LEISTUNG, NORMEN",
                "raw_label": raw_label,
                "confidence_source": "",
            })

        huerden_section = markdown_section(markdown, "HURDEN")
        for row in parse_markdown_tables(huerden_section):
            raw_label = " | ".join(value for value in row.values() if value and not is_uncertain(value))
            if not raw_label:
                continue
            raw_norm = normalized(raw_label)
            if not any(schadstoff_token_matches(raw_norm, token) for token in SCHADSTOFF_SOURCE_TOKENS):
                continue
            rows_by_case[case_id].append({
                "case_id": case_id,
                "legacy_path": legacy_path,
                "field": "HUERDEN-MATRIX",
                "raw_label": raw_label,
                "confidence_source": "",
            })

    return rows_by_case


def schadstoff_row_applies_to_reuse(raw_label: str, frontmatter: dict[str, str]) -> bool:
    label = normalized(raw_label)
    component_tokens = component_tokens_for_schadstoff(frontmatter)
    if any(token in label for token in component_tokens):
        return True
    if any(marker in label for marker in SCHADSTOFF_COMPONENT_MARKERS):
        return False
    return False


def component_tokens_for_schadstoff(frontmatter: dict[str, str]) -> set[str]:
    text = " | ".join([
        frontmatter.get("bauteil_label", ""),
        frontmatter.get("alte_funktion", ""),
        frontmatter.get("neue_funktion", ""),
        frontmatter.get("huerde_label", ""),
    ])
    tokens = set()
    for token in re.findall(r"[a-z0-9]+", normalized(text)):
        if len(token) < 4:
            continue
        if token in SCHADSTOFF_COMPONENT_STOPWORDS:
            continue
        tokens.add(token)
    return tokens


def build_schadstoff_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_by_case = load_reuse_nodes()
    schadstoff_rows = extract_schadstoff_rows()

    reusable_by_case: dict[str, list[tuple[dict[str, str], dict[str, str]]]] = defaultdict(list)
    for case_id, rows in sorted(reuse_by_case.items()):
        for node_row in sorted(rows, key=lambda row: row["typed_path"]):
            markdown = load_reuse_markdown(node_row)
            frontmatter = parse_simple_frontmatter(markdown)
            if not reusable_enough(frontmatter):
                stats["rows_skipped_not_reusable"] += 1
                continue
            if node_row["typed_path"] in excluded_sources:
                stats["rows_skipped_by_abgrenzung"] += 1
                continue
            reusable_by_case[case_id].append((node_row, frontmatter))

            component_labels = [
                ("FRONTMATTER:huerde_label", frontmatter.get("huerde_label", "")),
                ("FRONTMATTER:pruefung_label", frontmatter.get("pruefung_label", "")),
                ("BAUTEIL-INVENTAR:Eingriff/Aufbereitung", extract_markdown_bullet(markdown, "Eingriff/Aufbereitung")),
            ]
            for field, raw_label in component_labels:
                raw_label = (raw_label or "").strip()
                if not raw_label or is_uncertain(raw_label):
                    stats["component_labels_empty"] += 1
                    continue
                targets = map_schadstoff_targets(raw_label, existing_nodes)
                if not targets:
                    stats["component_labels_without_match"] += 1
                    continue
                for target in targets:
                    key = (node_row["typed_path"], "has_schadstoff", target)
                    if key in existing_keys:
                        stats["duplicates_skipped"] += 1
                        continue
                    target_entity, target_id = target.split("/", 1)
                    additions.append({
                        "source": node_row["typed_path"],
                        "source_entity": "reuse_einsatz",
                        "source_id": node_row["id"],
                        "relation": "has_schadstoff",
                        "target": target,
                        "target_entity": target_entity,
                        "target_id": target_id,
                        "field": field,
                        "raw_label": raw_label,
                        "confidence": schadstoff_confidence(raw_label),
                        "resolution_rule": "label_50n_has_schadstoff_component_label",
                        "legacy_path": "",
                        "original_source": node_row["typed_path"],
                        "original_relation": "has_schadstoff",
                        "original_target": target,
                        "edge_cleaning": "added_gap_50n",
                    })
                    existing_keys.add(key)

    for case_id, rows in sorted(schadstoff_rows.items()):
        case_reuse_rows = reusable_by_case.get(case_id, [])
        if not case_reuse_rows:
            stats["schadstoff_cases_without_reusable_rows"] += 1
            continue
        for schadstoff_row in rows:
            raw_label = schadstoff_row["raw_label"]
            targets = map_schadstoff_targets(raw_label, existing_nodes)
            if not targets:
                stats["schadstoff_rows_without_match"] += 1
                skipped.append({
                    "case_id": case_id,
                    "legacy_path": schadstoff_row["legacy_path"],
                    "raw_label": raw_label,
                    "reason": "no_schadstoff_token_match_or_unusable_label",
                })
                continue
            for node_row, frontmatter in case_reuse_rows:
                if not schadstoff_row_applies_to_reuse(raw_label, frontmatter):
                    stats["schadstoff_source_rows_skipped_no_component_match"] += 1
                    continue
                for target in targets:
                    key = (node_row["typed_path"], "has_schadstoff", target)
                    if key in existing_keys:
                        stats["duplicates_skipped"] += 1
                        continue
                    target_entity, target_id = target.split("/", 1)
                    additions.append({
                        "source": node_row["typed_path"],
                        "source_entity": "reuse_einsatz",
                        "source_id": node_row["id"],
                        "relation": "has_schadstoff",
                        "target": target,
                        "target_entity": target_entity,
                        "target_id": target_id,
                        "field": schadstoff_row["field"],
                        "raw_label": raw_label,
                        "confidence": schadstoff_confidence(raw_label, schadstoff_row.get("confidence_source", "")),
                        "resolution_rule": "table_50n_has_schadstoff_case_contaminant",
                        "legacy_path": schadstoff_row["legacy_path"],
                        "original_source": node_row["typed_path"],
                        "original_relation": "has_schadstoff",
                        "original_target": target,
                        "edge_cleaning": "added_gap_50n",
                    })
                    existing_keys.add(key)

    stats["reuse_rows_scanned"] = sum(len(rows) for rows in reuse_by_case.values())
    stats["schadstoff_cases_scanned"] = len(schadstoff_rows)
    stats["schadstoff_rows_scanned"] = sum(len(rows) for rows in schadstoff_rows.values())
    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


# ---------------------------------------------------------------------------
# 50o -- has_bauweise / has_bausystem / has_tragwerksprinzip
# ---------------------------------------------------------------------------

KONSTRUKTION_TARGETS: list[tuple[str, str, tuple[str, ...]]] = [
    ("has_bauweise", "bauweise/Fertigteilbauweise", (
        "fertigteil", "fertigteile", "prefab", "precast",
        "prefabricated", "vorfertig", "modulbau", "plattenbau",
        "wbs70", "iw73", "iw73/6", "typ dresden",
    )),
    ("has_bauweise", "bauweise/Holzbauweise", (
        "holz", "altholz", "bauholz", "nadelholz", "timber", "wood",
        "glulam", "brettschichtholz",
        "brettsperrholz", "clt", "mass timber", "massivholz",
        "holztrager", "holztraeger", "holzstutzen", "holzstuetzen",
        "holzpfette", "holzpfetten", "holzbinder", "holzstander",
        "holzstaender", "holzrahmen", "hsb", "azobe", "rafters",
        "trusses",
    )),
    ("has_bauweise", "bauweise/Hybridbauweise", (
        "hybrid", "holz-beton", "holz beton", "holz/stahl",
        "stahl/holz", "stahl/clt", "clt/stahl", "steel/clt",
        "timber/steel", "steel and clt", "steel + clt",
        "holz-beton-hybrid", "betonkerne + holz",
    )),
    ("has_bauweise", "bauweise/Massivbauweise", (
        "beton", "stahlbeton", "concrete", "mauerwerk", "ziegel",
        "brick", "bricks", "massiv", "mineralisch", "naturstein",
    )),
    ("has_bauweise", "bauweise/Ortbetonbauweise", (
        "ortbeton", "cast-in-place", "cast in place",
        "in-situ concrete", "in situ concrete", "vor ort betoniert",
    )),
    ("has_bauweise", "bauweise/Stahlbauweise", (
        "stahl", "steel", "baustahl", "wide flange", "i-trager",
        "i-traeger", "stahlprofil", "stahlprofile", "steel profile",
        "steel member", "steel members", "metalltrager", "metalltraeger",
        "stahltrager", "stahltraeger", "stahlstutzen", "stahlstuetzen",
        "stahlrohr", "stahlrohre", "rohrtrager", "rohrtraeger",
    )),
    ("has_bausystem", "bausystem/Betonfertigteil_System", (
        "betonfertigteil", "stahlbetonfertigteil", "betonfertigteile",
        "concrete precast", "precast concrete", "fertigteilplatte",
        "fertigteilplatten", "fertigteil-paneel", "fertigteil-paneele",
        "hollow core", "hohlkorperdecke", "hohlkoerperdecke",
        "kanaalplaat", "kanaalplaatvloeren", "tt-decke", "tt decke",
    )),
    ("has_bausystem", "bausystem/Holzrahmenbau", (
        "holzrahmen", "holzrahmenbau", "hsb", "holzstander",
        "holzstaender", "timber frame", "wood frame",
    )),
    ("has_bausystem", "bausystem/Holz_Skelettbau", (
        "holzskelett", "holz-skelett", "timber skeleton",
        "wood skeleton", "post-and-beam timber", "holzstutzen",
        "holzstuetzen", "holztrager", "holztraeger",
    )),
    ("has_bausystem", "bausystem/Plattenbau", (
        "plattenbau", "plattenbausystem", "wbs70", "wbs 70",
        "iw73", "iw73/6", "typ dresden", "grossplatte",
        "grossplatten", "plattenbauteil", "plattenbauteile",
    )),
    ("has_bausystem", "bausystem/Stahl_Skelettbau", (
        "stahlskelett", "stahl-skelett", "steel skeleton",
        "steel frame", "stahlrahmen", "stahl frame", "wide flange",
        "i-trager", "i-traeger", "stahltrager", "stahltraeger",
        "stahlstutzen", "stahlstuetzen",
    )),
    ("has_tragwerksprinzip", "tragwerksprinzip/Fachwerk", (
        "fachwerk", "truss", "trusses", "dachbinder", "roof truss",
        "roof trusses",
    )),
    ("has_tragwerksprinzip", "tragwerksprinzip/Skeletttragwerk", (
        "skelett", "skeleton", "steel frame", "stahlrahmen",
        "tragrahmen", "rahmentragwerk", "frame structure",
        "post-and-beam", "post and beam", "stuetzen/trager",
        "stutzen/trager", "stuetzen/traeger", "stutzen/traeger",
        "columns and beams", "beams and columns", "pole barn",
        "portal", "portale", "portals",
    )),
    ("has_tragwerksprinzip", "tragwerksprinzip/Wandtragwerk", (
        "wandtrag", "wandbau", "tragende wand", "tragende waende",
        "tragende wande", "load-bearing wall", "load bearing wall",
        "wall-bearing", "wand-/deckensystem", "wand-/decken",
        "wandplatten", "wandelemente", "wand-elemente", "wall panels",
        "plattenbau",
    )),
    ("has_tragwerksprinzip", "tragwerksprinzip/Wand_Kern_Tragwerk", (
        "wand-kern", "wand/kern", "kerntrag", "betonkern",
        "betonkerne", "concrete core", "concrete cores", "core",
        "cores", "kern", "kerne", "servicekern", "erschliessungskern",
        "erschliessungskern", "external core",
    )),
]

KONSTRUKTION_SKIP_PHRASES = (
    "kein tragender reuse-fall",
    "kein direct-reuse-tragwerk",
    "kein direct reuse tragwerk",
    "nicht direct reuse",
    "nicht als direct reuse",
    "nicht reused",
    "nicht wiederverwendet",
    "nicht als zentraler reuse-fall",
    "nicht zentraler reuse-fall",
    "reuse nicht tragend",
    "neue aufstockung",
    "reuse nicht haupttragwerk",
    "reuse nicht als haupttragwerk",
    "nicht haupttragwerk",
    "nicht als haupttragwerk",
    "direct-reuse-tragwerk fehlt",
    "haupttragwerk neu",
    "haupttragwerk ist neu",
    "neues haupttragwerk",
    "neue holzstruktur",
    "neuer holzrohbau",
    "neubau-tragwerk",
    "new main structure",
)

KONSTRUKTION_POSITIVE_REUSE_TOKENS = (
    "reuse-stahl", "reuse stahl", "reused steel", "reused timber",
    "wiederverwendete", "wiederverwendeter", "wiederverwendetes",
    "gebrauchte", "gebrauchter", "gebrauchtes", "reclaimed",
    "salvaged", "direct reuse",
)

STRUCTURAL_NO_TOKENS = (
    "nein", "nicht tragend", "non-structural", "non structural",
    "kein tragwerk", "nicht haupttragwerk",
)

STRUCTURAL_YES_TOKENS = (
    "ja", "wahrscheinlich ja", "teilweise", "tragend",
    "structural", "load-bearing", "load bearing",
)

STRUCTURAL_LABEL_TOKENS = (
    "tragwerk", "tragstruktur", "tragfahigkeit", "tragfaehigkeit",
    "stabilitat", "stabilitaet", "lastabtragung", "lasten",
    "trager", "traeger", "stutze", "stuetze", "pfette", "binder",
    "dachbinder", "spant", "stuetzen", "stutzen", "trusses",
    "beam", "beams", "column", "columns", "girder", "joist",
    "slab", "slabs", "deck", "decke", "deckenplatte",
    "bodenplatte", "wandplatte", "wandelement", "wand-/decken",
    "aussteif", "bracing", "sturz", "portal", "portale",
    "pfeiler", "core", "kern", "dachtrag", "dachstruktur",
    "stahlrahmen", "holzrahmen", "structural steel", "massivholz",
)

NON_STRUCTURAL_LABEL_TOKENS = (
    "fensterrahmen", "window frame", "fenster", "tuer", "tur",
    "sanitar", "sanitaer", "heizkorper", "heizkoerper",
    "radiator", "leuchte", "beleuchtung", "fliese", "tile",
    "wc", "urinal", "waschbecken", "fassadenpaneel",
    "gipskarton", "innenausbau", "ausbauleistung", "unterkonstruktion",
)

STRUCTURAL_OVERRIDE_TOKENS = (
    "tragwerk", "tragstruktur", "lastabtragung", "dachtrag",
    "dachstruktur", "trager", "traeger", "stutze", "stuetze",
    "pfette", "binder", "stabilitat", "stabilitaet", "aussteif",
    "bodenplatte", "deckenplatte", "wandplatte", "wandelement",
    "stahlrahmen", "holzrahmen", "fachwerk", "skelett",
)


def konstruktion_text_is_useful(raw_label: str) -> bool:
    label = normalized(raw_label)
    if not label or label in UNCERTAIN_VALUES:
        return False
    if any(phrase in label for phrase in KONSTRUKTION_SKIP_PHRASES):
        return False
    return any(
        konstruktion_token_matches(label, token)
        for _relation, _target, tokens in KONSTRUKTION_TARGETS
        for token in tokens
    )


def konstruktion_token_matches(label: str, token: str) -> bool:
    if token == "stahl":
        return bool(re.search(r"(?<![a-z])stahl(?!beton|[a-z])", label))
    if token == "holz":
        return bool(re.search(r"(?<![a-z])holz(?![a-z])", label))
    if token in {"steel", "wood"}:
        return bool(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", label))
    return token in label


def add_konstruktion_target(
    targets: list[tuple[str, str]],
    relation: str,
    target: str,
    existing_nodes: set[str],
) -> None:
    if target in existing_nodes and (relation, target) not in targets:
        targets.append((relation, target))


def map_konstruktion_targets(raw_label: str, existing_nodes: set[str]) -> list[tuple[str, str]]:
    label = normalized(raw_label)
    if not konstruktion_text_is_useful(raw_label):
        return []

    targets: list[tuple[str, str]] = []
    for relation, target, tokens in KONSTRUKTION_TARGETS:
        if any(konstruktion_token_matches(label, token) for token in tokens):
            add_konstruktion_target(targets, relation, target, existing_nodes)

    target_set = {target for _relation, target in targets}

    if "bauweise/Ortbetonbauweise" in target_set:
        add_konstruktion_target(targets, "has_bauweise", "bauweise/Massivbauweise", existing_nodes)

    if "bausystem/Betonfertigteil_System" in target_set:
        add_konstruktion_target(targets, "has_bauweise", "bauweise/Fertigteilbauweise", existing_nodes)
        add_konstruktion_target(targets, "has_bauweise", "bauweise/Massivbauweise", existing_nodes)

    if "bausystem/Plattenbau" in target_set:
        add_konstruktion_target(targets, "has_bausystem", "bausystem/Betonfertigteil_System", existing_nodes)
        add_konstruktion_target(targets, "has_bauweise", "bauweise/Fertigteilbauweise", existing_nodes)
        add_konstruktion_target(targets, "has_bauweise", "bauweise/Massivbauweise", existing_nodes)
        add_konstruktion_target(targets, "has_tragwerksprinzip", "tragwerksprinzip/Wandtragwerk", existing_nodes)

    if "bausystem/Stahl_Skelettbau" in target_set:
        add_konstruktion_target(targets, "has_bauweise", "bauweise/Stahlbauweise", existing_nodes)
        add_konstruktion_target(targets, "has_tragwerksprinzip", "tragwerksprinzip/Skeletttragwerk", existing_nodes)

    if "bausystem/Holz_Skelettbau" in target_set:
        add_konstruktion_target(targets, "has_bauweise", "bauweise/Holzbauweise", existing_nodes)
        add_konstruktion_target(targets, "has_tragwerksprinzip", "tragwerksprinzip/Skeletttragwerk", existing_nodes)

    if "bausystem/Holzrahmenbau" in target_set:
        add_konstruktion_target(targets, "has_bauweise", "bauweise/Holzbauweise", existing_nodes)
        add_konstruktion_target(targets, "has_tragwerksprinzip", "tragwerksprinzip/Wandtragwerk", existing_nodes)

    if "nicht uber" in label and any(token in label for token in (
        "stutzen/trager", "stutzen/traeger", "stuetzen/trager",
        "stuetzen/traeger", "stutzen und trager", "stuetzen und traeger",
    )):
        targets = [
            (relation, target)
            for relation, target in targets
            if target != "tragwerksprinzip/Skeletttragwerk"
        ]

    return targets


def construction_target_supported_by_component(
    target: str,
    component_label: str,
    component_targets: set[str],
) -> bool:
    if target in component_targets:
        return True

    label = normalized(component_label)
    if target == "bauweise/Stahlbauweise":
        return any(konstruktion_token_matches(label, token) for token in (
            "stahl", "steel", "baustahl", "stahlprofil", "stahlprofile",
            "stahltrager", "stahltraeger", "stahlstutzen", "stahlstuetzen",
            "stahlrohr", "stahlrohre", "wide flange", "i-trager",
            "i-traeger",
        ))
    if target == "bauweise/Holzbauweise":
        return any(konstruktion_token_matches(label, token) for token in (
            "holz", "timber", "wood", "clt", "brettschichtholz",
            "brettsperrholz", "holztrager", "holztraeger",
            "holzstutzen", "holzstuetzen", "holzpfette",
            "holzpfetten", "holzbinder", "rafters", "trusses",
        ))
    if target == "bauweise/Massivbauweise":
        return any(konstruktion_token_matches(label, token) for token in (
            "beton", "stahlbeton", "concrete", "mauerwerk", "ziegel",
            "brick", "bricks", "naturstein",
        ))
    if target == "bauweise/Fertigteilbauweise":
        return any(konstruktion_token_matches(label, token) for token in (
            "fertigteil", "fertigteile", "prefab", "precast",
            "vorfertig", "wbs70", "iw73",
        ))
    if target == "bauweise/Hybridbauweise":
        return (
            ("bauweise/Stahlbauweise" in component_targets and "bauweise/Holzbauweise" in component_targets)
            or ("bauweise/Holzbauweise" in component_targets and "bauweise/Massivbauweise" in component_targets)
        )
    if target == "bauweise/Ortbetonbauweise":
        return "ortbeton" in label or "cast-in-place" in label or "cast in place" in label
    if target == "bausystem/Betonfertigteil_System":
        return any(token in label for token in (
            "betonfertigteil", "stahlbetonfertigteil", "precast concrete",
            "concrete precast", "fertigteilplatte", "fertigteilplatten",
            "hollow core", "tt-decke", "tt decke",
        ))
    if target == "bausystem/Plattenbau":
        return any(token in label for token in ("plattenbau", "wbs70", "wbs 70", "iw73", "grossplatte"))
    if target == "bausystem/Stahl_Skelettbau":
        return any(token in label for token in (
            "stahlrahmen", "stahlskelett", "stahl-skelett", "steel frame",
            "stahltrager", "stahltraeger", "stahlstutzen", "stahlstuetzen",
            "wide flange", "i-trager", "i-traeger",
        ))
    if target == "bausystem/Holz_Skelettbau":
        return any(token in label for token in (
            "holzskelett", "holz-skelett", "holztrager", "holztraeger",
            "holzstutzen", "holzstuetzen", "holzpfette", "holzpfetten",
            "holzbinder", "timber skeleton", "post-and-beam timber",
        ))
    if target == "bausystem/Holzrahmenbau":
        return any(token in label for token in (
            "holzrahmen", "holzrahmenbau", "holzstander", "holzstaender",
            "timber frame", "wood frame", "hsb",
        ))
    if target == "tragwerksprinzip/Fachwerk":
        return any(token in label for token in ("fachwerk", "truss", "trusses", "dachbinder", "binder"))
    if target == "tragwerksprinzip/Skeletttragwerk":
        return any(token in label for token in (
            "skelett", "stahlrahmen", "holzrahmen", "tragrahmen",
            "rahmen", "stutze", "stuetze", "stutzen", "stuetzen",
            "trager", "traeger", "pfette", "pfetten", "binder",
            "beam", "beams", "column", "columns", "rohrtrager",
            "rohrtraeger", "rohrstruktur", "aussteifung", "portal",
        ))
    if target == "tragwerksprinzip/Wandtragwerk":
        return any(token in label for token in (
            "tragwand", "wandtrag", "wandplatte", "wandplatten",
            "wandelement", "wandelemente", "tragende wand",
            "tragende waende", "tragende wande", "load-bearing wall",
            "load bearing wall", "plattenbau",
        ))
    if target == "tragwerksprinzip/Wand_Kern_Tragwerk":
        return any(token in label for token in (
            "kern", "kerne", "core", "cores", "servicekern",
            "erschliessungskern", "kerntrag",
        ))
    return False


def reuse_is_structural(frontmatter: dict[str, str], markdown: str) -> bool:
    bearing = normalized(extract_markdown_bullet(markdown, "tragend?"))
    if bearing and any(token in bearing for token in STRUCTURAL_NO_TOKENS):
        return False

    text = normalized(" | ".join([
        frontmatter.get("bauteil_label", ""),
        frontmatter.get("alte_funktion", ""),
        frontmatter.get("neue_funktion", ""),
        frontmatter.get("material_label", ""),
        frontmatter.get("huerde_label", ""),
        extract_markdown_bullet(markdown, "Leistungsanforderung"),
    ]))
    has_non_structural_label = any(token in text for token in NON_STRUCTURAL_LABEL_TOKENS)
    has_structural_override = any(token in text for token in STRUCTURAL_OVERRIDE_TOKENS)
    if has_non_structural_label and not has_structural_override:
        return False
    if bearing and any(token in bearing for token in STRUCTURAL_YES_TOKENS):
        return True
    return any(token in text for token in STRUCTURAL_LABEL_TOKENS)


def construction_component_label(frontmatter: dict[str, str], markdown: str) -> str:
    return " | ".join(
        part for part in (
            frontmatter.get("bauteil_label", ""),
            frontmatter.get("material_label", ""),
            frontmatter.get("alte_funktion", ""),
            frontmatter.get("neue_funktion", ""),
            extract_markdown_bullet(markdown, "Leistungsanforderung"),
            frontmatter.get("huerde_label", ""),
        )
        if part and not is_uncertain(part)
    )


def extract_konstruktion_rows() -> dict[str, list[dict[str, str]]]:
    source_dir = gebaeude_dir()
    rows_by_case: dict[str, list[dict[str, str]]] = defaultdict(list)

    for path in sorted(source_dir.glob("*.md")):
        markdown = path.read_text(encoding="utf-8", errors="replace")
        case_id = path.stem
        legacy_path = str(path.relative_to(ROOT))

        ent_section = markdown_section(markdown, "ENTIT")
        for row in parse_markdown_tables(ent_section):
            entity = normalized(get_cell(row, "Entitat"))
            if not any(token in entity for token in ("tragwerk", "bausystem", "bauweise")):
                continue
            raw_label = " | ".join(
                part for part in (
                    get_cell(row, "Wert"),
                    get_cell(row, "Beziehung zur Fallstudie"),
                    get_cell(row, "Anmerkung"),
                )
                if part and not is_uncertain(part)
            )
            if raw_label:
                rows_by_case[case_id].append({
                    "case_id": case_id,
                    "legacy_path": legacy_path,
                    "field": "ENTITAETEN-MAPPING:Konstruktion",
                    "raw_label": raw_label,
                    "confidence_source": get_cell(row, "Vertrauensgrad"),
                })

        technik_section = markdown_section(markdown, "TECHNIK")
        for row in parse_markdown_tables(technik_section):
            thema = normalized(get_cell(row, "Thema"))
            raw_label = " | ".join(value for value in row.values() if value and not is_uncertain(value))
            if not raw_label:
                continue
            if not any(token in thema for token in ("tragwerk", "lastabtragung", "tragstruktur")):
                continue
            if not konstruktion_text_is_useful(raw_label):
                continue
            rows_by_case[case_id].append({
                "case_id": case_id,
                "legacy_path": legacy_path,
                "field": "TECHNIK, LEISTUNG, NORMEN",
                "raw_label": raw_label,
                "confidence_source": "",
            })

    return rows_by_case


def konstruktion_confidence(raw_label: str, confidence_source: str = "") -> str:
    source_confidence = normalized(confidence_source)
    label = normalized(raw_label)
    if source_confidence == "belegt":
        return "rule_high"
    if "teilweise" in source_confidence or "quellenkonflikt" in source_confidence:
        return "rule_medium"
    if any(token in label for token in ("unbekannt", "unklar", "wahrscheinlich", "vermutlich", "nicht vollstandig")):
        return "rule_low"
    return "rule_medium"


def build_konstruktion_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_by_case = load_reuse_nodes()
    konstruktion_rows = extract_konstruktion_rows()

    reusable_structural_by_case: dict[str, list[tuple[dict[str, str], dict[str, str], str]]] = defaultdict(list)
    for case_id, rows in sorted(reuse_by_case.items()):
        for node_row in sorted(rows, key=lambda row: row["typed_path"]):
            markdown = load_reuse_markdown(node_row)
            frontmatter = parse_simple_frontmatter(markdown)
            if not reusable_enough(frontmatter):
                stats["rows_skipped_not_reusable"] += 1
                continue
            if node_row["typed_path"] in excluded_sources:
                stats["rows_skipped_by_abgrenzung"] += 1
                continue
            if not reuse_is_structural(frontmatter, markdown):
                stats["rows_skipped_not_structural"] += 1
                continue

            reusable_structural_by_case[case_id].append((node_row, frontmatter, markdown))
            raw_label = construction_component_label(frontmatter, markdown)
            targets = map_konstruktion_targets(raw_label, existing_nodes)
            if not targets:
                stats["component_labels_without_match"] += 1
                skipped.append({
                    "source": node_row["typed_path"],
                    "raw_label": raw_label,
                    "reason": "no_konstruktion_token_match",
                })
                continue

            for relation, target in targets:
                key = (node_row["typed_path"], relation, target)
                if key in existing_keys:
                    stats["duplicates_skipped"] += 1
                    continue
                target_entity, target_id = target.split("/", 1)
                additions.append({
                    "source": node_row["typed_path"],
                    "source_entity": "reuse_einsatz",
                    "source_id": node_row["id"],
                    "relation": relation,
                    "target": target,
                    "target_entity": target_entity,
                    "target_id": target_id,
                    "field": "REUSE_EINSATZ:combined_structure_labels",
                    "raw_label": raw_label,
                    "confidence": konstruktion_confidence(raw_label),
                    "resolution_rule": "label_50o_has_konstruktion_component_label",
                    "legacy_path": "",
                    "original_source": node_row["typed_path"],
                    "original_relation": relation,
                    "original_target": target,
                    "edge_cleaning": "added_gap_50o",
                })
                existing_keys.add(key)

    for case_id, rows in sorted(konstruktion_rows.items()):
        case_reuse_rows = reusable_structural_by_case.get(case_id, [])
        if not case_reuse_rows:
            stats["konstruktion_cases_without_structural_reuse_rows"] += 1
            continue
        for konstruktion_row in rows:
            raw_label = konstruktion_row["raw_label"]
            targets = map_konstruktion_targets(raw_label, existing_nodes)
            if not targets:
                stats["konstruktion_rows_without_match"] += 1
                skipped.append({
                    "case_id": case_id,
                    "legacy_path": konstruktion_row["legacy_path"],
                    "raw_label": raw_label,
                    "reason": "no_konstruktion_token_match_or_unusable_label",
                })
                continue
            for node_row, _frontmatter, _markdown in case_reuse_rows:
                component_label = construction_component_label(_frontmatter, _markdown)
                component_targets = {
                    target
                    for _relation, target in map_konstruktion_targets(component_label, existing_nodes)
                }
                for relation, target in targets:
                    if not construction_target_supported_by_component(target, component_label, component_targets):
                        stats["table_targets_skipped_component_mismatch"] += 1
                        continue
                    key = (node_row["typed_path"], relation, target)
                    if key in existing_keys:
                        stats["duplicates_skipped"] += 1
                        continue
                    target_entity, target_id = target.split("/", 1)
                    additions.append({
                        "source": node_row["typed_path"],
                        "source_entity": "reuse_einsatz",
                        "source_id": node_row["id"],
                        "relation": relation,
                        "target": target,
                        "target_entity": target_entity,
                        "target_id": target_id,
                        "field": konstruktion_row["field"],
                        "raw_label": raw_label,
                        "confidence": konstruktion_confidence(raw_label, konstruktion_row.get("confidence_source", "")),
                        "resolution_rule": "table_50o_has_konstruktion_case_structure",
                        "legacy_path": konstruktion_row["legacy_path"],
                        "original_source": node_row["typed_path"],
                        "original_relation": relation,
                        "original_target": target,
                        "edge_cleaning": "added_gap_50o",
                    })
                    existing_keys.add(key)

    stats["reuse_rows_scanned"] = sum(len(rows) for rows in reuse_by_case.values())
    stats["structural_reuse_rows"] = sum(len(rows) for rows in reusable_structural_by_case.values())
    stats["konstruktion_cases_scanned"] = len(konstruktion_rows)
    stats["konstruktion_rows_scanned"] = sum(len(rows) for rows in konstruktion_rows.values())
    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


# ---------------------------------------------------------------------------
# 50p -- has_bauteilebene / has_bauteilzustand / has_funktionswechsel
# ---------------------------------------------------------------------------

BAUTEILEBENE_PRIORITY = (
    "bauteilebene/Oberflaechenschicht",
    "bauteilebene/Materialcharge",
    "bauteilebene/System",
    "bauteilebene/Gebaeudeteil",
    "bauteilebene/Bauteilgruppe",
    "bauteilebene/Einzelbauteil",
)

BAUTEILEBENE_MATERIALCHARGE_TOKENS = (
    "stockpile", "stockpiling", "materialcharge", "charge",
    "gesamtmaterial", "gesamtbauteile", "materialpool", "materiallager",
    "produktionsrest", "produktionsuberschuss", "produktionueberschuss",
    "baustellenuberschuss", "baustellenueberschuss", "off-cut",
    "offcut", "reststucke", "reststuecke", "reste", "surplus",
    "schrott", "salvaged structural steel",
)

BAUTEILEBENE_SYSTEM_TOKENS = (
    "system", "tragwerk", "tragstruktur", "tragrahmen", "stahlrahmen",
    "holzrahmen", "fassadensystem", "curtain wall", "kerntragwerk",
    "servicekern", "erschliessungskern", "space-frame", "space frame",
    "rohrstruktur", "dachstruktur", "ausbausystem",
)

BAUTEILEBENE_GEBAEUDETEIL_TOKENS = (
    "gebaeude", "gebaude", "pavillon", "halle", "kern",
    "servicekern", "erschliessungskern", "treppenhaus", "vordach",
    "pergola", "dach", "fassade", "balkon", "gewaechshaus",
    "gewachshaus", "betriebsgebaeude", "betriebsgebaude",
)

BAUTEILEBENE_SURFACE_TOKENS = (
    "fliese", "fliesen", "tile", "tiles", "teppich", "carpet",
    "bodenbelag", "belag", "bekleidung", "verkleidung",
    "oberflaeche", "oberflache", "oberflaechenschicht",
    "oberflachenschicht", "finish", "cladding", "dachziegel",
    "ziegel als bekleidung", "fassadenbekleidung", "wandbekleidung",
    "fassadenmaterial", "fassadenziegel", "fassaden-claustra",
    "gabionenfullung", "gabionenfuellung",
)

BAUTEILEBENE_GROUP_TOKENS = (
    "elemente", "platten", "profile", "paneele", "module", "bauteile",
    "komponenten", "fenster", "tueren", "turen", "stuetzen",
    "stutzen", "traeger", "trager", "pfetten", "binder", "ziegel",
    "bricks", "leuchten", "sanitaer", "sanitar", "wc", "urinale",
    "waschbecken", "treppen", "dallettes", "parts", "members", "beams",
    "columns", "panels", "doors", "windows", "tiles",
)

BAUTEILEBENE_SINGLE_TOKENS = (
    "tuer", "tur", "door", "fenster", "window", "treppe", "stutze",
    "stuetze", "trager", "traeger", "pfette", "binder", "lift",
    "aufzug", "leuchte", "waschbecken", "urinal", "wc",
)

ZUSTAND_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("bauteilzustand/Beschaedigt", (
        "beschadigt", "beschadigte", "beschadigter", "beschadigten",
        "beschaedigt", "beschaedigte", "beschaedigter", "beschaedigten",
        "bruch", "gebrochen", "broken",
        "schaden", "schaeden", "damage", "riss", "risse", "crack",
        "cracked", "splitter", "abplat", "verlust",
    )),
    ("bauteilzustand/Korrodiert", (
        "korrodiert", "rost", "rostig", "entrostet", "scaling",
        "corroded", "oxidation",
    )),
    ("bauteilzustand/Patiniert", (
        "patina", "patiniert", "gebrauchsspuren", "altersspuren",
        "witterungsspuren", "spuren der vorgeschichte", "sichtbare spuren",
    )),
    ("bauteilzustand/Intakt", (
        "intakt", "intakte", "intakter", "intakten",
        "guter zustand", "gutem zustand", "good condition",
        "brauchbar", "geeignet", "salvageable", "starker als ursprunglich",
        "staerker als urspruenglich", "hohe qualitaet", "hohe qualitat",
    )),
    ("bauteilzustand/Ungeprueft", (
        "nicht gepruft", "nicht geprueft", "ungepruft", "ungeprueft",
        "keine prufung", "keine pruefung", "prufung fehlt",
        "pruefung fehlt", "ohne prufung", "ohne pruefung",
    )),
    ("bauteilzustand/Kontaminiert", (
        "kontaminiert", "kontamination", "schadstoffbelastung",
        "asbest", "pcb", "pak", "blei", "holzschutzmittel",
    )),
]

FUNCTION_CATEGORY_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("structure", (
        "tragwerk", "tragstruktur", "tragend", "stutze", "stuetze",
        "traeger", "trager", "pfette", "binder", "decke", "bodenplatte",
        "wandplatte", "dachtrag", "aussteif", "kerntrag", "stahlrahmen",
        "holzrahmen", "structure", "structural", "beam", "column",
    )),
    ("wall", ("wand", "waende", "wande", "wall")),
    ("roof", ("dach", "roof")),
    ("floor", ("boden", "decke", "floor", "slab")),
    ("facade", ("fassade", "hulle", "huelle", "facade", "envelope")),
    ("insulation", ("dammung", "daemmung", "insulation", "warmeschutz", "waermeschutz")),
    ("door", ("tuer", "tur", "tueren", "turen", "door", "doors")),
    ("window", ("fenster", "window", "windows")),
    ("stair", ("treppe", "treppen", "erschliessung", "stair", "stairs")),
    ("sanitary", ("sanitar", "sanitaer", "wc", "urinal", "waschbecken", "sanitary")),
    ("lighting", ("leuchte", "beleuchtung", "licht", "lighting", "lamp")),
    ("tga", ("tga", "heizung", "lueftung", "luftung", "elektro", "technik")),
    ("furniture", ("moebel", "mobel", "tisch", "tresen", "counter", "furniture")),
    ("surface", ("fliese", "fliesen", "belag", "bekleidung", "oberflaeche", "oberflache", "tile", "cladding")),
    ("decoration", ("dekor", "kunst", "artwork", "ornament", "ausdruck", "gestalterisch", "symbolisch")),
]

FUNCTION_TECHNICAL_TOKENS = (
    "tga", "heizung", "lueftung", "luftung", "elektro",
    "wc", "urinal", "waschbecken", "toilette", "toiletten",
    "sanitarobjekt", "sanitarobjekte", "sanitaranlage", "sanitaranlagen",
    "duschtasse", "duschtassen", "armatur", "armaturen",
    "leuchte", "beleuchtung", "aufzug", "lift", "technical",
)

FUNCTION_DECORATIVE_TOKENS = (
    "dekor", "kunst", "artwork", "ornament", "ausdruck",
    "gestalterisch", "symbolisch", "skulptur",
)

FUNCTION_CONSTRUCTIVE_TOKENS = (
    "trag", "struktur", "stabilitat", "stabilitaet", "last",
    "aussteif", "decke", "boden", "wand", "dach", "fassade",
    "hulle", "huelle", "dammung", "daemmung", "brandschutz",
    "schallschutz", "warmeschutz", "waermeschutz", "raumtrennung",
    "raumbild", "kern", "stutze", "stuetze", "trager", "traeger",
)

FUNCTION_GENERIC_UNKNOWN = (
    "unbekannt", "unklar", "diverse", "keine", "neu", "neu/recycelt",
    "unterschiedlich", "verschiedene", "teils moglich", "teils moeglich",
    "potenziell", "vermutlich",
)


def add_profile_target(
    targets: list[tuple[str, str, str]],
    relation: str,
    target: str,
    confidence: str,
    existing_nodes: set[str],
) -> None:
    if target in existing_nodes and (relation, target, confidence) not in targets:
        if not any(existing_relation == relation and existing_target == target for existing_relation, existing_target, _ in targets):
            targets.append((relation, target, confidence))


def component_profile_label(frontmatter: dict[str, str], markdown: str) -> str:
    return " | ".join(
        part for part in (
            frontmatter.get("bauteil_label", ""),
            frontmatter.get("material_label", ""),
            frontmatter.get("herkunft_label", ""),
            frontmatter.get("alte_funktion", ""),
            frontmatter.get("neue_funktion", ""),
            frontmatter.get("menge_umfang", ""),
            extract_markdown_bullet(markdown, "tragend?"),
            extract_markdown_bullet(markdown, "raeumlich?"),
            extract_markdown_bullet(markdown, "Huelle?"),
            extract_markdown_bullet(markdown, "technisch?"),
            extract_markdown_bullet(markdown, "Eingriff/Aufbereitung"),
            frontmatter.get("pruefung_label", ""),
            extract_markdown_bullet(markdown, "Pruefung"),
            extract_markdown_bullet(markdown, "Leistungsanforderung"),
            frontmatter.get("huerde_label", ""),
        )
        if part and not is_uncertain(part)
    )


def component_condition_label(frontmatter: dict[str, str], markdown: str) -> str:
    return " | ".join(
        part for part in (
            frontmatter.get("bauteil_label", ""),
            frontmatter.get("material_label", ""),
            frontmatter.get("herkunft_label", ""),
            frontmatter.get("pruefung_label", ""),
            extract_markdown_bullet(markdown, "Eingriff/Aufbereitung"),
            extract_markdown_bullet(markdown, "Pruefung"),
        )
        if part and not is_uncertain(part)
    )


def profile_value_is_known(value: str) -> bool:
    label = normalized(value)
    if not label or label in UNCERTAIN_VALUES:
        return False
    return not any(label == token for token in FUNCTION_GENERIC_UNKNOWN)


def first_existing_profile_target(
    candidates: list[str],
    existing_nodes: set[str],
) -> str:
    for target in candidates:
        if target in existing_nodes:
            return target
    return ""


def map_bauteilebene_target(frontmatter: dict[str, str], markdown: str, existing_nodes: set[str]) -> tuple[str, str]:
    bauteil = normalized(frontmatter.get("bauteil_label", ""))
    material = normalized(frontmatter.get("material_label", ""))
    alte = normalized(frontmatter.get("alte_funktion", ""))
    neue = normalized(frontmatter.get("neue_funktion", ""))
    menge = normalized(frontmatter.get("menge_umfang", ""))
    text = " | ".join([bauteil, material, alte, neue, menge])

    candidates: list[str] = []
    if any(token in text for token in BAUTEILEBENE_SURFACE_TOKENS):
        candidates.append("bauteilebene/Oberflaechenschicht")
    if any(token in text for token in BAUTEILEBENE_MATERIALCHARGE_TOKENS):
        candidates.append("bauteilebene/Materialcharge")
    if any(token in text for token in BAUTEILEBENE_SYSTEM_TOKENS):
        candidates.append("bauteilebene/System")
    if any(token in bauteil for token in BAUTEILEBENE_GEBAEUDETEIL_TOKENS):
        if not any(token in bauteil for token in (
            "dachziegel", "fassadenbekleidung", "fassadenpaneel",
            "fassadenmaterial", "fassadenziegel", "fassaden-claustra",
            "gabionenfullung", "gabionenfuellung",
        )):
            candidates.append("bauteilebene/Gebaeudeteil")
    if any(token in text for token in BAUTEILEBENE_GROUP_TOKENS):
        candidates.append("bauteilebene/Bauteilgruppe")
    if any(token in bauteil for token in BAUTEILEBENE_SINGLE_TOKENS):
        candidates.append("bauteilebene/Einzelbauteil")

    ordered = [target for target in BAUTEILEBENE_PRIORITY if target in candidates]
    target = first_existing_profile_target(ordered, existing_nodes)
    confidence = "rule_medium" if target else ""
    if target in {"bauteilebene/Materialcharge", "bauteilebene/Oberflaechenschicht"}:
        confidence = "rule_high"
    return target, confidence


def map_bauteilzustand_targets(raw_label: str, existing_nodes: set[str]) -> list[tuple[str, str]]:
    label = normalized(raw_label)
    targets: list[tuple[str, str]] = []

    pruefung_known = False
    if any(token in label for token in (
        "gepruft", "geprueft", "prufung", "pruefung", "test",
        "sichtprufung", "sichtpruefung", "zugversuch", "zertifikat",
        "certificate", "materialanalyse", "zustandsbewertung",
    )):
        if not any(token in label for token in (
            "nicht gepruft", "nicht geprueft", "keine prufung",
            "keine pruefung", "prufung notig", "pruefung noetig",
            "prufung erforderlich", "pruefung erforderlich",
            "prufung fehlt", "pruefung fehlt", "prufung unbekannt",
            "pruefung unbekannt", "prufung moglich", "pruefung moeglich",
            "prufung geplant", "pruefung geplant", "test geplant",
            "tests geplant", "testing geplant", "prufung/reinigung unbekannt",
            "pruefung/reinigung unbekannt", "reinigung/prufung unbekannt",
            "reinigung/pruefung unbekannt", "funktionsprufung unbekannt",
            "funktionspruefung unbekannt",
        )):
            pruefung_known = True

    if pruefung_known:
        target = "bauteilzustand/Geprueft"
        if target in existing_nodes:
            targets.append((target, "rule_medium"))

    if "restlebensdauer" in label or "lebensdauer" in label or "service life" in label:
        known_life = (
            bool(re.search(r"restlebensdauer.{0,40}\b\d+\s*(?:jahr|jahre|years?)\b", label))
            or bool(re.search(r"\b\d+\s*(?:jahr|jahre|years?)\b.{0,40}restlebensdauer", label))
            or "restlebensdauer bekannt" in label
        )
        unknown_life = any(token in label for token in ("unklar", "unbekannt", "nicht bekannt", "prufung notig", "pruefung noetig", "erforderlich"))
        if known_life and "bauteilzustand/Restlebensdauer_Bekannt" in existing_nodes:
            targets.append(("bauteilzustand/Restlebensdauer_Bekannt", "rule_high"))
        if unknown_life and "bauteilzustand/Restlebensdauer_Unklar" in existing_nodes:
            targets.append(("bauteilzustand/Restlebensdauer_Unklar", "rule_medium"))

    for target, tokens in ZUSTAND_RULES:
        if target not in existing_nodes:
            continue
        if target == "bauteilzustand/Beschaedigt" and any(token in label for token in (
            "ohne schaden", "ohne schaeden", "ohne beschadigung",
            "ohne beschaedigung", "ohne damage",
        )):
            continue
        if any(zustand_token_matches(label, token) for token in tokens):
            confidence = "rule_medium"
            if target in {"bauteilzustand/Kontaminiert", "bauteilzustand/Beschaedigt", "bauteilzustand/Korrodiert"}:
                confidence = "rule_high"
            if (target, confidence) not in targets:
                targets.append((target, confidence))

    deduped: list[tuple[str, str]] = []
    for target, confidence in targets:
        if not any(existing_target == target for existing_target, _ in deduped):
            deduped.append((target, confidence))
    return deduped


def zustand_token_matches(label: str, token: str) -> bool:
    if " " in token or "-" in token:
        return token in label
    return bool(re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", label))


def function_categories(value: str) -> set[str]:
    label = normalized(value)
    categories: set[str] = set()
    if not profile_value_is_known(label):
        return categories
    for category, tokens in FUNCTION_CATEGORY_RULES:
        if any(token in label for token in tokens):
            categories.add(category)
    return categories


def functions_are_same(old_value: str, new_value: str) -> bool:
    old = normalized(old_value)
    new = normalized(new_value)
    if not profile_value_is_known(old) or not profile_value_is_known(new):
        return False
    if "gleiche funktion" in new or "bleibt" in new:
        return True
    old_categories = function_categories(old)
    new_categories = function_categories(new)
    if old_categories and new_categories and old_categories.intersection(new_categories):
        return True
    old_words = {token for token in re.findall(r"[a-z0-9]+", old) if len(token) >= 4}
    new_words = {token for token in re.findall(r"[a-z0-9]+", new) if len(token) >= 4}
    return bool(old_words and new_words and old_words.intersection(new_words))


def map_funktionswechsel_targets(frontmatter: dict[str, str], markdown: str, existing_nodes: set[str]) -> list[tuple[str, str]]:
    old_value = frontmatter.get("alte_funktion", "")
    new_value = frontmatter.get("neue_funktion", "")
    old = normalized(old_value)
    new = normalized(new_value)
    new_context = normalized(" | ".join([
        new_value,
        frontmatter.get("bauteil_label", ""),
        extract_markdown_bullet(markdown, "Leistungsanforderung"),
    ]))

    targets: list[tuple[str, str]] = []

    old_known = profile_value_is_known(old)
    new_known = profile_value_is_known(new)

    if not old_known or not new_known:
        if any(token in " | ".join([old, new]) for token in ("unbekannt", "unklar", "teils moglich", "teils moeglich", "potenziell")):
            if "funktionswechsel/Unbekannt" in existing_nodes:
                targets.append(("funktionswechsel/Unbekannt", "rule_low"))
    elif functions_are_same(old_value, new_value):
        if "funktionswechsel/Gleiche_Funktion" in existing_nodes:
            targets.append(("funktionswechsel/Gleiche_Funktion", "rule_high"))
    else:
        old_categories = function_categories(old_value)
        new_categories = function_categories(new_value)
        if old_categories and new_categories and not old_categories.intersection(new_categories):
            if "funktionswechsel/Neue_Funktion" in existing_nodes:
                targets.append(("funktionswechsel/Neue_Funktion", "rule_high"))
        elif old != new and "funktionswechsel/Neue_Funktion" in existing_nodes:
            targets.append(("funktionswechsel/Neue_Funktion", "rule_medium"))

    if any(function_specific_token_matches(new_context, token) for token in FUNCTION_TECHNICAL_TOKENS):
        if "funktionswechsel/Technische_Funktion" in existing_nodes:
            targets.append(("funktionswechsel/Technische_Funktion", "rule_medium"))
    if any(function_specific_token_matches(new_context, token) for token in FUNCTION_DECORATIVE_TOKENS):
        if "funktionswechsel/Dekorative_Funktion" in existing_nodes:
            targets.append(("funktionswechsel/Dekorative_Funktion", "rule_medium"))
    if any(token in new_context for token in FUNCTION_CONSTRUCTIVE_TOKENS):
        if "funktionswechsel/Konstruktive_Funktion" in existing_nodes:
            targets.append(("funktionswechsel/Konstruktive_Funktion", "rule_medium"))

    deduped: list[tuple[str, str]] = []
    for target, confidence in targets:
        if not any(existing_target == target for existing_target, _ in deduped):
            deduped.append((target, confidence))
    return deduped


def function_specific_token_matches(label: str, token: str) -> bool:
    if len(token) <= 3:
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", label))
    return token in label


def build_bauteilprofil_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    existing_keys = existing_edge_keys(edge_rows)
    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    reuse_rows = [
        row for rows in load_reuse_nodes().values()
        for row in rows
    ]

    for node_row in sorted(reuse_rows, key=lambda row: row["typed_path"]):
        markdown = load_reuse_markdown(node_row)
        frontmatter = parse_simple_frontmatter(markdown)
        stats["reuse_rows_scanned"] += 1

        if not reusable_enough(frontmatter):
            stats["rows_skipped_not_reusable"] += 1
            continue
        if node_row["typed_path"] in excluded_sources:
            stats["rows_skipped_by_abgrenzung"] += 1
            continue

        raw_label = component_profile_label(frontmatter, markdown)
        condition_label = component_condition_label(frontmatter, markdown)
        row_targets: list[tuple[str, str, str, str]] = []

        bauteilebene_target, bauteilebene_confidence = map_bauteilebene_target(frontmatter, markdown, existing_nodes)
        if bauteilebene_target:
            row_targets.append(("has_bauteilebene", bauteilebene_target, bauteilebene_confidence, "REUSE_EINSATZ:component_scale"))
        else:
            stats["bauteilebene_without_target"] += 1

        for target, confidence in map_bauteilzustand_targets(condition_label, existing_nodes):
            row_targets.append(("has_bauteilzustand", target, confidence, "REUSE_EINSATZ:component_condition"))

        function_targets = map_funktionswechsel_targets(frontmatter, markdown, existing_nodes)
        if function_targets:
            for target, confidence in function_targets:
                row_targets.append(("has_funktionswechsel", target, confidence, "REUSE_EINSATZ:old_new_function"))
        else:
            stats["funktionswechsel_without_target"] += 1

        if not row_targets:
            stats["rows_without_profile_targets"] += 1
            skipped.append({
                "source": node_row["typed_path"],
                "raw_label": raw_label,
                "reason": "no_bauteilprofil_target",
            })
            continue

        for relation, target, confidence, field in row_targets:
            key = (node_row["typed_path"], relation, target)
            if key in existing_keys:
                stats["duplicates_skipped"] += 1
                continue
            target_entity, target_id = target.split("/", 1)
            additions.append({
                "source": node_row["typed_path"],
                "source_entity": "reuse_einsatz",
                "source_id": node_row["id"],
                "relation": relation,
                "target": target,
                "target_entity": target_entity,
                "target_id": target_id,
                "field": field,
                "raw_label": raw_label,
                "confidence": confidence,
                "resolution_rule": "label_50p_has_bauteilprofil_component_profile",
                "legacy_path": "",
                "original_source": node_row["typed_path"],
                "original_relation": relation,
                "original_target": target,
                "edge_cleaning": "added_gap_50p",
            })
            existing_keys.add(key)

    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


# ---------------------------------------------------------------------------
# 50q -- uses_software_digitaltool / has_datenmodell / has_tooltyp /
#        has_datenqualitaet
# ---------------------------------------------------------------------------

DIGITAL_DATENMODELL_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("datenmodell/IFC", (
        "ifc", "bim/ifc", "building information model", "building information modelling",
    )),
    ("datenmodell/Materialpass_Schema", (
        "materialpass", "material passport", "gebaeuderessourcenpass",
        "gebauderessourcenpass", "ressourcenpass", "bauteilpass",
        "product passport",
    )),
    ("datenmodell/Materialdatenbank", (
        "materialdatenbank", "material database", "datenbank", "database",
        "falldatenbank", "fallstudiendatenbank", "materialinventar",
        "material inventory", "stockpile catalog", "bauteilkatalog",
    )),
    ("datenmodell/Bauteil_ID", (
        "bauteil-id", "bauteil id", "qr-code", "qr code", "qr",
        "rfid", "track-and-trace", "tracking", "barcode",
    )),
    ("datenmodell/Klassifikation", (
        "klassifikation", "classification", "stabu", "din 276", "din 277",
    )),
    ("datenmodell/Taxonomie", (
        "taxonomie", "taxonomy",
    )),
    ("datenmodell/Ontologie", (
        "ontologie", "ontology",
    )),
]

DATAQUALITY_TARGET_ORDER = (
    "datenqualitaet/Nicht_Belegt",
    "datenqualitaet/Unbekannt",
    "datenqualitaet/Widerspruechlich",
    "datenqualitaet/Geschaetzt",
    "datenqualitaet/Sekundaerquelle",
    "datenqualitaet/Primaerquelle",
    "datenqualitaet/Belegt",
)

DIGITAL_BAUTEILBOERSE_TOKENS = (
    "boerse", "bauteilboerse", "bauteilborse", "market", "marketplace",
    "marktplaats", "spares", "restado", "rotordc", "opalis", "backacia",
    "baticycle", "batiterre", "batrecup", "bauteilladen", "bauteilnetz",
    "materialrest", "genbyg", "globechain", "rheaply", "salvoweb",
    "salza", "superyard", "warp_it", "useagain", "enviromate",
    "insert", "raedificare", "resource", "re_store", "reuse_and_trade",
    "reusefully", "skop", "articonnex", "baukarussell", "excess_materials",
    "material_reuse_portal", "library_of_reuse", "oogstkaart",
    "sustainability_yard", "surplus_building", "upcyclea",
    "lindner_group_reused_products", "gebruiktebouwmaterialen",
    "materialenbank",
)

DIGITAL_MATERIALDATENBANK_TOKENS = (
    "database", "datenbank", "dataview", "rotordb",
    "library", "index", "catalog", "katalog",
    "qr_rfid", "materialtracking", "pre_demolition_audit", "cmex",
    "material_index", "madaster", "maconda", "qflow", "gis_urban_mining",
    "urban_mining_index", "materialpass",
)

DIGITAL_MATERIALKATASTER_TOKENS = (
    "madaster", "material_index", "urban_mining", "urban_mining_index",
    "gis_urban_mining", "maconda",
)

DIGITAL_SOFTWARE_DATENMODELL_BY_ID: list[tuple[str, str, tuple[str, ...]]] = [
    ("has_datenmodell", "datenmodell/IFC", (
        "bim", "bonsai_blenderbim", "ifc_viewer", "ifcopenshell", "speckle",
    )),
    ("has_datenmodell", "datenmodell/Materialpass_Schema", (
        "madaster", "maconda_materialpass", "maconda_romulus",
        "concular_plattform",
    )),
    ("has_datenmodell", "datenmodell/Materialdatenbank", (
        "madaster", "maconda_materialpass", "maconda_romulus",
        "material_index", "rotordb", "gis_urban_mining", "urban_mining_index",
        "pre_demolition_audit_tools", "dataview",
    )),
    ("has_datenmodell", "datenmodell/Bauteil_ID", (
        "qr_rfid_materialtracking", "qflow", "loopfront",
    )),
    ("has_datenmodell", "datenmodell/Klassifikation", (
        "qflow", "platform_cb23",
    )),
]

DIGITAL_SKIP_SOFTWARE_ALIASES = {
    "",
    "software",
    "tool",
    "plattform",
    "platform",
    "database",
    "datenbank",
    "materialdatenbank",
    "materialkataster",
    "bauteilboerse",
    "bauteilbörse",
}


def inventory_rows_for_entity(entity: str) -> list[dict[str, str]]:
    return [
        row for row in load_csv(NODE_INVENTORY)
        if row["entity"] == entity
    ]


def data_point_label(markdown: str) -> str:
    return " | ".join(
        part for part in (
            extract_markdown_bullet(markdown, "Kennwert"),
            extract_markdown_bullet(markdown, "Wert"),
            extract_markdown_bullet(markdown, "Methode/Datenmodell/Software"),
            extract_markdown_bullet(markdown, "Bilanzgrenze"),
            extract_markdown_bullet(markdown, "Quelle"),
            extract_markdown_bullet(markdown, "Vertrauensgrad"),
        )
        if part and not is_uncertain(part)
    )


def data_point_quality_label(markdown: str) -> str:
    return " | ".join(
        part for part in (
            extract_markdown_bullet(markdown, "Kennwert"),
            extract_markdown_bullet(markdown, "Wert"),
            extract_markdown_bullet(markdown, "Methode/Datenmodell/Software"),
            extract_markdown_bullet(markdown, "Bilanzgrenze"),
            extract_markdown_bullet(markdown, "Quelle"),
            extract_markdown_bullet(markdown, "Vertrauensgrad"),
        )
        if part
    )


def digital_token_matches(label: str, token: str) -> bool:
    token = normalized(token)
    if not token:
        return False
    if token in {"ifc", "qr", "bim"}:
        return re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", label) is not None
    if re.fullmatch(r"[a-z0-9]+", token):
        return re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", label) is not None
    return token in label


def map_datenmodell_targets(raw_label: str, existing_nodes: set[str]) -> list[tuple[str, str]]:
    label = normalized(raw_label)
    if not label or label in UNCERTAIN_VALUES:
        return []

    targets: list[tuple[str, str]] = []
    for target, tokens in DIGITAL_DATENMODELL_RULES:
        if target not in existing_nodes:
            continue
        if any(digital_token_matches(label, token) for token in tokens):
            confidence = "rule_high"
            if target == "datenmodell/Materialdatenbank" and any(token in label for token in ("datenbank", "database", "inventar", "catalog")):
                confidence = "rule_high"
            elif target == "datenmodell/Materialdatenbank":
                confidence = "rule_medium"
            targets.append((target, confidence))

    deduped: list[tuple[str, str]] = []
    for target, confidence in targets:
        if not any(existing_target == target for existing_target, _ in deduped):
            deduped.append((target, confidence))
    return deduped


def software_aliases_by_target(existing_nodes: set[str]) -> dict[str, list[str]]:
    aliases: dict[str, list[str]] = {}
    for row in inventory_rows_for_entity("software_digitaltool"):
        target = row["typed_path"]
        if target not in existing_nodes:
            continue
        raw_aliases = {
            row["id"],
            row["title"],
            row["id"].replace("_", " "),
            row["id"].replace("_", "-"),
        }
        if row["id"].endswith("_Plattform"):
            raw_aliases.add(row["id"][:-10])
            raw_aliases.add(row["id"][:-10].replace("_", " "))
        if row["id"] == "RotorDC":
            raw_aliases.update(("Rotor DC", "RotorDC"))
        if row["id"] == "Concular_Plattform":
            raw_aliases.add("Concular")
        if row["id"] == "QR_RFID_Materialtracking":
            raw_aliases.update(("QR/RFID", "QR-Code", "RFID"))

        clean_aliases: list[str] = []
        for alias in raw_aliases:
            clean = normalized(alias)
            clean = clean.replace("— vertieftes forschungsdossier", "").strip()
            clean = clean.replace("- vertieftes forschungsdossier", "").strip()
            if clean in DIGITAL_SKIP_SOFTWARE_ALIASES:
                continue
            if len(clean) < 4 and clean != "bim":
                continue
            clean_aliases.append(clean)
        aliases[target] = sorted(set(clean_aliases), key=len, reverse=True)
    return aliases


def software_bim_context(label: str) -> bool:
    if "berliner immobilienmanagement" in label:
        return False
    return any(token in label for token in (
        "ifc", "modell", "model", "digital", "as-built", "as built",
        "cde", "building information",
    ))


def map_software_targets(
    raw_label: str,
    existing_nodes: set[str],
    aliases_by_target: dict[str, list[str]],
) -> list[tuple[str, str]]:
    label = normalized(raw_label)
    if not label or label in UNCERTAIN_VALUES:
        return []

    targets: list[tuple[str, str]] = []
    for target, aliases in aliases_by_target.items():
        if target not in existing_nodes:
            continue
        for alias in aliases:
            if alias == "bim" and not software_bim_context(label):
                continue
            if digital_token_matches(label, alias):
                confidence = "rule_high"
                if target == "software_digitaltool/BIM":
                    confidence = "rule_medium"
                targets.append((target, confidence))
                break

    deduped: list[tuple[str, str]] = []
    for target, confidence in targets:
        if not any(existing_target == target for existing_target, _ in deduped):
            deduped.append((target, confidence))
    return deduped


def dataquality_targets(markdown: str, existing_nodes: set[str]) -> list[tuple[str, str, str]]:
    value = extract_markdown_bullet(markdown, "Wert")
    method = extract_markdown_bullet(markdown, "Methode/Datenmodell/Software")
    boundary = extract_markdown_bullet(markdown, "Bilanzgrenze")
    source = extract_markdown_bullet(markdown, "Quelle")
    confidence_label = extract_markdown_bullet(markdown, "Vertrauensgrad")
    raw_label = " | ".join(part for part in (value, method, boundary, source, confidence_label) if part)
    label = normalized(raw_label)
    confidence_norm = normalized(confidence_label)
    source_norm = normalized(source)
    targets: list[tuple[str, str, str]] = []

    def add(target: str, confidence: str, reason: str) -> None:
        if target in existing_nodes and not any(existing_target == target for existing_target, _confidence, _reason in targets):
            targets.append((target, confidence, reason))

    if any(token in label for token in (
        "nicht belegt", "nicht als reuse belegt", "kein beleg", "keine quelle",
        "ohne quelle", "kein reuse-nachweis", "nicht nachgewiesen",
    )):
        add("datenqualitaet/Nicht_Belegt", "rule_high", "negative_evidence_label")

    if (
        source_norm in {"", "-"}
        or any(token in label for token in (
            "unbekannt", "unklar", "nicht offentlich", "nicht oeffentlich",
            "details unbekannt", "methode unbekannt", "bilanzgrenze unbekannt",
        ))
    ):
        add("datenqualitaet/Unbekannt", "rule_medium", "unknown_or_missing_data_label")

    if any(token in label for token in (
        "quellenkonflikt", "widerspruch", "widerspruchlich", "widerspruechlich",
        "abweichende", "abweichend", "alternative angabe", "alternativangabe",
    )):
        add("datenqualitaet/Widerspruechlich", "rule_high", "source_conflict_label")

    if label_has_estimate_marker(label):
        add("datenqualitaet/Geschaetzt", "rule_medium", "estimate_label")

    if any(token in label for token in ("sekundar", "sekundaer", "secondary")):
        add("datenqualitaet/Sekundaerquelle", "rule_medium", "secondary_source_label")

    if any(token in label for token in (
        "primarquelle", "primaerquelle", "primary source", "primary-source",
    )):
        add("datenqualitaet/Primaerquelle", "rule_medium", "primary_source_label")

    if "nicht belegt" not in confidence_norm and (
        "belegt" in confidence_norm
        or (source_norm and source_norm != "-")
    ):
        confidence = "rule_high" if confidence_norm == "belegt" else "rule_medium"
        add("datenqualitaet/Belegt", confidence, "source_or_confidence_label")

    if not targets:
        add("datenqualitaet/Unbekannt", "rule_low", "no_quality_label")

    ordered_targets: list[tuple[str, str, str]] = []
    for target in DATAQUALITY_TARGET_ORDER:
        ordered_targets.extend(row for row in targets if row[0] == target)
    return ordered_targets


def label_has_estimate_marker(label: str) -> bool:
    if "~" in label:
        return True
    if any(token in label for token in (
        "geschätzt", "geschatzt", "geschaetzt", "schatzung", "schaetzung",
        "estimate", "estimated",
    )):
        return True
    return any(
        re.search(rf"(?<![a-z0-9]){token}(?![a-z0-9])", label) is not None
        for token in ("ca", "circa", "etwa", "rund", "ungefahr", "ungefaehr")
    )


def software_tooltyp_targets(node_row: dict[str, str], markdown: str, existing_nodes: set[str]) -> list[tuple[str, str]]:
    label = normalized(" ".join([node_row["id"], node_row["title"]]))
    text = normalized(markdown)
    targets: list[tuple[str, str]] = []

    def add(target: str, confidence: str) -> None:
        if target in existing_nodes and not any(existing_target == target for existing_target, _ in targets):
            targets.append((target, confidence))

    for target in ("tooltyp/Bauteilboerse", "tooltyp/Materialdatenbank", "tooltyp/Materialkataster"):
        if target in text:
            add(target, "rule_high")

    if any(token in label for token in DIGITAL_BAUTEILBOERSE_TOKENS):
        add("tooltyp/Bauteilboerse", "rule_medium")
    if any(token in label for token in DIGITAL_MATERIALDATENBANK_TOKENS):
        add("tooltyp/Materialdatenbank", "rule_medium")
    if any(token in label for token in DIGITAL_MATERIALKATASTER_TOKENS):
        add("tooltyp/Materialkataster", "rule_medium")

    return targets


def software_datenmodell_targets(node_row: dict[str, str], markdown: str, existing_nodes: set[str]) -> list[tuple[str, str]]:
    label = normalized(node_row["id"])
    targets: list[tuple[str, str]] = []

    def add(target: str, confidence: str) -> None:
        if target in existing_nodes and not any(existing_target == target for existing_target, _ in targets):
            targets.append((target, confidence))

    for _relation, target, tokens in DIGITAL_SOFTWARE_DATENMODELL_BY_ID:
        if any(token == label for token in tokens):
            add(target, "rule_medium")

    return targets


def add_digital_edge(
    additions: list[dict[str, str]],
    existing_keys: set[tuple[str, str, str]],
    *,
    source: str,
    source_entity: str,
    source_id: str,
    relation: str,
    target: str,
    field: str,
    raw_label: str,
    confidence: str,
    resolution_rule: str,
    legacy_path: str = "",
) -> bool:
    key = (source, relation, target)
    if key in existing_keys:
        return False
    target_entity, target_id = target.split("/", 1)
    additions.append({
        "source": source,
        "source_entity": source_entity,
        "source_id": source_id,
        "relation": relation,
        "target": target,
        "target_entity": target_entity,
        "target_id": target_id,
        "field": field,
        "raw_label": raw_label,
        "confidence": confidence,
        "resolution_rule": resolution_rule,
        "legacy_path": legacy_path,
        "original_source": source,
        "original_relation": relation,
        "original_target": target,
        "edge_cleaning": "added_gap_50q",
    })
    existing_keys.add(key)
    return True


def build_digital_evidence_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    existing_keys = existing_edge_keys(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()
    software_aliases = software_aliases_by_target(existing_nodes)

    for node_row in sorted(inventory_rows_for_entity("datenpunkt"), key=lambda row: row["typed_path"]):
        index_path = ROOT / node_row["markdown_path"]
        if not index_path.exists():
            stats["datenpunkt_missing_index"] += 1
            continue
        markdown = index_path.read_text(encoding="utf-8", errors="replace")
        raw_label = data_point_label(markdown)
        quality_label = data_point_quality_label(markdown)
        stats["datenpunkt_rows_scanned"] += 1

        for target, confidence, reason in dataquality_targets(markdown, existing_nodes):
            if add_digital_edge(
                additions, existing_keys,
                source=node_row["typed_path"],
                source_entity="datenpunkt",
                source_id=node_row["id"],
                relation="has_datenqualitaet",
                target=target,
                field=f"DATENPUNKT:quality:{reason}",
                raw_label=quality_label,
                confidence=confidence,
                resolution_rule="label_50q_has_datenqualitaet_datenpunkt",
            ):
                stats["datenqualitaet_edges"] += 1
            else:
                stats["duplicates_skipped"] += 1

        method_label = " | ".join(
            part for part in (
                extract_markdown_bullet(markdown, "Kennwert"),
                extract_markdown_bullet(markdown, "Wert"),
                extract_markdown_bullet(markdown, "Methode/Datenmodell/Software"),
                extract_markdown_bullet(markdown, "Quelle"),
            )
            if part and not is_uncertain(part)
        )
        datenmodell_targets = map_datenmodell_targets(method_label, existing_nodes)
        if not datenmodell_targets:
            stats["datenpunkt_without_datenmodell"] += 1
        for target, confidence in datenmodell_targets:
            if add_digital_edge(
                additions, existing_keys,
                source=node_row["typed_path"],
                source_entity="datenpunkt",
                source_id=node_row["id"],
                relation="has_datenmodell",
                target=target,
                field="DATENPUNKT:Methode/Datenmodell/Software",
                raw_label=method_label,
                confidence=confidence,
                resolution_rule="label_50q_has_datenmodell_datenpunkt_method",
            ):
                stats["datenmodell_edges"] += 1
            else:
                stats["duplicates_skipped"] += 1

        software_targets = map_software_targets(method_label, existing_nodes, software_aliases)
        if not software_targets:
            stats["datenpunkt_without_software"] += 1
        for target, confidence in software_targets:
            if add_digital_edge(
                additions, existing_keys,
                source=node_row["typed_path"],
                source_entity="datenpunkt",
                source_id=node_row["id"],
                relation="uses_software_digitaltool",
                target=target,
                field="DATENPUNKT:Methode/Datenmodell/Software",
                raw_label=method_label,
                confidence=confidence,
                resolution_rule="label_50q_uses_software_datenpunkt_method",
            ):
                stats["software_edges"] += 1
            else:
                stats["duplicates_skipped"] += 1

    excluded_sources = direct_reuse_exclusion_sources(edge_rows)
    for rows in load_reuse_nodes().values():
        for node_row in sorted(rows, key=lambda row: row["typed_path"]):
            markdown = load_reuse_markdown(node_row)
            frontmatter = parse_simple_frontmatter(markdown)
            stats["reuse_rows_scanned"] += 1
            if not reusable_enough(frontmatter):
                stats["reuse_rows_skipped_not_reusable"] += 1
                continue
            if node_row["typed_path"] in excluded_sources:
                stats["reuse_rows_skipped_by_abgrenzung"] += 1
                continue
            raw_label = " | ".join(
                part for part in (
                    frontmatter.get("herkunft_label", ""),
                    frontmatter.get("quelle_label", ""),
                )
                if part and not is_uncertain(part)
            )
            software_targets = map_software_targets(raw_label, existing_nodes, software_aliases)
            if not software_targets:
                stats["reuse_without_software"] += 1
                continue
            for target, confidence in software_targets:
                if add_digital_edge(
                    additions, existing_keys,
                    source=node_row["typed_path"],
                    source_entity="reuse_einsatz",
                    source_id=node_row["id"],
                    relation="uses_software_digitaltool",
                    target=target,
                    field="REUSE_EINSATZ:herkunft_quelle",
                    raw_label=raw_label,
                    confidence=confidence,
                    resolution_rule="label_50q_uses_software_reuse_source",
                ):
                    stats["software_edges"] += 1
                else:
                    stats["duplicates_skipped"] += 1

    for node_row in sorted(inventory_rows_for_entity("software_digitaltool"), key=lambda row: row["typed_path"]):
        index_path = ROOT / node_row["markdown_path"]
        if not index_path.exists():
            stats["software_missing_index"] += 1
            continue
        markdown = index_path.read_text(encoding="utf-8", errors="replace")
        raw_label = " | ".join(part for part in (node_row["title"], node_row["id"]) if part)
        stats["software_nodes_scanned"] += 1

        for target, confidence in software_tooltyp_targets(node_row, markdown, existing_nodes):
            if add_digital_edge(
                additions, existing_keys,
                source=node_row["typed_path"],
                source_entity="software_digitaltool",
                source_id=node_row["id"],
                relation="has_tooltyp",
                target=target,
                field="SOFTWARE_DIGITALTOOL:type_profile",
                raw_label=raw_label,
                confidence=confidence,
                resolution_rule="label_50q_has_tooltyp_software_profile",
            ):
                stats["tooltyp_edges"] += 1
            else:
                stats["duplicates_skipped"] += 1

        for target, confidence in software_datenmodell_targets(node_row, markdown, existing_nodes):
            if add_digital_edge(
                additions, existing_keys,
                source=node_row["typed_path"],
                source_entity="software_digitaltool",
                source_id=node_row["id"],
                relation="has_datenmodell",
                target=target,
                field="SOFTWARE_DIGITALTOOL:data_model_profile",
                raw_label=raw_label,
                confidence=confidence,
                resolution_rule="label_50q_has_datenmodell_software_profile",
            ):
                stats["datenmodell_edges"] += 1
            else:
                stats["duplicates_skipped"] += 1

    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


# ---------------------------------------------------------------------------
# 50r -- has_bauobjektklasse / has_bauobjektrolle / has_bauobjektstatus /
#        has_nutzung / has_bauaufgabe_intervention
# ---------------------------------------------------------------------------

BUILDING_SOURCE_DIR_NAMES = {"gebaude", "gebaeude"}


def extract_markdown_bullet_normalized(markdown: str, wanted_label: str) -> str:
    wanted = normalized(wanted_label)
    pattern = re.compile(r"^- \*\*(.+?):\*\*\s*(.*)$", flags=re.MULTILINE)
    for match in pattern.finditer(markdown):
        if normalized(match.group(1)) == wanted:
            return match.group(2).strip()
    return ""


def matching_building_source_texts(case_id: str) -> list[tuple[str, str]]:
    matches: list[tuple[str, str]] = []
    for folder in sorted(ROOT.iterdir(), key=lambda path: path.name.lower()):
        if not folder.is_dir():
            continue
        if normalized(folder.name) not in BUILDING_SOURCE_DIR_NAMES:
            continue
        source_path = folder / f"{case_id}.md"
        if source_path.exists():
            matches.append((
                str(source_path.relative_to(ROOT)),
                source_path.read_text(encoding="utf-8", errors="replace"),
            ))
    return matches


def focused_source_excerpt(markdown: str) -> str:
    if not markdown:
        return ""
    title = ""
    for line in markdown.splitlines():
        if line.startswith("# "):
            title = line.lstrip("#").strip()
            break
    kurzdefinition = markdown_section(markdown, "Kurzdefinition")
    kurzdefinition = "\n".join(kurzdefinition.splitlines()[:8])
    return compact_join([
        title,
        extract_markdown_bullet_normalized(markdown, "Ubergeordnete Themen"),
        kurzdefinition[:1400],
        extract_inline_bold_label(markdown, "Statushinweis"),
    ])


def extract_inline_bold_label(markdown: str, wanted_label: str) -> str:
    wanted = normalized(wanted_label)
    pattern = re.compile(r"\*\*(.+?):\*\*\s*([^*\n]+)")
    for match in pattern.finditer(markdown):
        if normalized(match.group(1)) == wanted:
            return match.group(2).strip()
    return ""


def source_focus_for_label(source_focus: str, max_length: int = 1800) -> str:
    if len(source_focus) <= max_length:
        return source_focus
    return source_focus[:max_length].rsplit(" ", 1)[0]


def context_fallback(context: dict[str, str]) -> str:
    return source_focus_for_label(context["source_focus"]) if not context["has_object_context"] else ""


def context_label_for_mapping(context: dict[str, str], *keys: str, include_fallback: bool = True) -> str:
    parts = [context[key] for key in keys]
    if include_fallback:
        parts.append(context_fallback(context))
    return compact_join(parts)


def context_label_for_report(context: dict[str, str], *keys: str) -> str:
    return compact_join([context[key] for key in keys] + [context_fallback(context)])


def likely_areal_label(label: str, object_label: str) -> bool:
    return (
        text_has(object_label, ("areal", "quartier", "district", "estate", "campus", "ensemble", "siedlung"))
        or text_has(label, ("kein einzelnes gebaeude", "kein einzelnes gebaude", "kommunales entwicklungsgebiet", "grosses areal", "quartiersentwicklung"))
    )


def building_context_label_parts(markdown: str) -> dict[str, str]:
    labels = {
        "name": "Name",
        "gebaeude": "Gebaude",
        "projekt": "Projekt",
        "zeitraum": "Zeitraum",
        "urspruengliche_nutzung": "Ursprungliche Nutzung",
        "neue_nutzung": "Neue Nutzung",
        "projektstatus": "Projektstatus",
        "statushinweis": "Statushinweis",
        "kurzurteil": "Kurzurteil",
        "themen": "Ubergeordnete Themen",
    }
    return {
        key: extract_markdown_bullet_normalized(markdown, label)
        for key, label in labels.items()
    }


def compact_join(parts: list[str]) -> str:
    seen: set[str] = set()
    clean_parts: list[str] = []
    for part in parts:
        part = (part or "").strip()
        if not part:
            continue
        norm = normalized(part)
        if norm in seen:
            continue
        seen.add(norm)
        clean_parts.append(part)
    return " | ".join(clean_parts)


def building_context_for_bauobjekt(node_row: dict[str, str]) -> dict[str, str]:
    index_path = ROOT / node_row["markdown_path"]
    index_markdown = index_path.read_text(encoding="utf-8", errors="replace") if index_path.exists() else ""
    index_parts = building_context_label_parts(index_markdown)
    source_texts = matching_building_source_texts(node_row["id"])
    source_parts: list[dict[str, str]] = []
    source_excerpt_parts: list[str] = []
    source_paths: list[str] = []
    for legacy_path, markdown in source_texts:
        source_paths.append(legacy_path)
        source_parts.append(building_context_label_parts(markdown))
        source_excerpt_parts.append(focused_source_excerpt(markdown))

    def value(key: str) -> str:
        return compact_join(
            [index_parts.get(key, "")]
            + [parts.get(key, "") for parts in source_parts]
        )

    title = node_row.get("title", "")
    object_label = compact_join([title, node_row.get("id", ""), value("gebaeude")])
    project_label = compact_join([title, value("projekt"), value("themen"), value("kurzurteil")])
    use_label = compact_join([title, value("neue_nutzung")])
    status_label = compact_join([title, value("projektstatus"), value("statushinweis"), value("zeitraum"), value("kurzurteil")])
    source_focus = compact_join(source_excerpt_parts)
    has_object_context = any(
        value(key)
        for key in ("gebaeude", "projekt", "urspruengliche_nutzung", "neue_nutzung", "zeitraum", "projektstatus", "statushinweis")
    )
    broad_label = compact_join([
        title,
        value("gebaeude"),
        value("projekt"),
        value("urspruengliche_nutzung"),
        value("neue_nutzung"),
        value("zeitraum"),
        value("projektstatus"),
        value("statushinweis"),
        value("kurzurteil"),
        value("themen"),
        source_focus_for_label(source_focus) if not has_object_context else "",
    ])
    return {
        "title": title,
        "legacy_path": source_paths[0] if source_paths else node_row["markdown_path"],
        "object_label": object_label,
        "project_label": project_label,
        "use_label": use_label,
        "status_label": status_label,
        "origin_label": value("urspruengliche_nutzung"),
        "new_use_label": value("neue_nutzung"),
        "source_focus": source_focus,
        "broad_label": broad_label,
        "has_object_context": "yes" if has_object_context else "",
    }


def project_rows_by_id() -> dict[str, dict[str, str]]:
    return {
        row["id"]: row
        for row in inventory_rows_for_entity("projekt")
    }


def installed_bauobjekt_targets(edge_rows: list[dict[str, str]]) -> set[str]:
    return {
        row["target"]
        for row in edge_rows
        if row["relation"] == "installed_in_bauobjekt"
        and row["target_entity"] == "bauobjekt"
    }


def add_context_target(
    targets: list[tuple[str, str, str]],
    existing_nodes: set[str],
    target: str,
    confidence: str,
    reason: str,
) -> None:
    if target in existing_nodes and not any(existing_target == target for existing_target, _confidence, _reason in targets):
        targets.append((target, confidence, reason))


def text_has(label: str, tokens: tuple[str, ...]) -> bool:
    return any(token in label for token in tokens)


def label_has_word(label: str, token: str) -> bool:
    return re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", label) is not None


def map_bauobjektklasse_targets(context: dict[str, str], existing_nodes: set[str]) -> list[tuple[str, str, str]]:
    raw_label = context_label_for_mapping(context, "object_label", "project_label")
    label = normalized(raw_label)
    object_label = normalized(context["object_label"])
    direct_label = normalized(compact_join([context["object_label"], context["project_label"]]))
    targets: list[tuple[str, str, str]] = []

    if text_has(label, ("reuse centre", "reuse center", "circular centre", "circular center", "ressurssentral", "materialisierung", "bauteilboerse", "materialhub", "material hub")):
        add_context_target(targets, existing_nodes, "bauobjektklasse/Reuse_Centre", "rule_medium", "reuse_centre_label")
    if text_has(label, ("pavillon", "pavilion")):
        add_context_target(targets, existing_nodes, "bauobjektklasse/Pavillon", "rule_high", "pavilion_label")
    if likely_areal_label(label, object_label):
        add_context_target(targets, existing_nodes, "bauobjektklasse/Quartier_Areal", "rule_medium", "district_or_areal_label")
    if text_has(direct_label, ("innenausbau", "fit-out", "fit out", "office fit", "bueroausbau", "3. og", "dritten obergeschoss", "interior fit")):
        add_context_target(targets, existing_nodes, "bauobjektklasse/Innenausbau", "rule_high", "interior_fitout_label")
    infrastructure_object_match = text_has(object_label, ("substation", "umspann", "highway", "tunnel", "footbridge", "pipeline", "parkhaus", "parking garage", "primary substation"))
    if label_has_word(object_label, "bruecke"):
        infrastructure_object_match = True
    if infrastructure_object_match:
        add_context_target(targets, existing_nodes, "bauobjektklasse/Infrastruktur", "rule_medium", "infrastructure_label")
    if text_has(object_label, ("depot", "materialdepot", "lagerhalle", "lagerhaus", "warehouse", "equipment barn", "geraetebau", "stockpile")):
        add_context_target(targets, existing_nodes, "bauobjektklasse/Depot_Lager", "rule_medium", "depot_or_storage_label")
    if text_has(object_label, ("gebaeudeteil", "gebaudeteil", "gebaeudeabschnitt", "gebaudeabschnitt", "kopfbau", "facade", "fassade", "dach", "geschoss", "floor", "screen")):
        add_context_target(targets, existing_nodes, "bauobjektklasse/Gebaeudeteil", "rule_medium", "building_part_label")

    if not targets and text_has(label, (
        "gebaeude", "gebaude", "building", "haus", "house", "wohnhaus", "schule",
        "kindergarten", "museum", "villa", "office", "buero", "buro", "halle",
        "tower", "zentrum", "centre", "center",
    )):
        add_context_target(targets, existing_nodes, "bauobjektklasse/Gebaeude", "rule_medium", "generic_building_label")

    return targets


def map_nutzung_targets(context: dict[str, str], existing_nodes: set[str]) -> list[tuple[str, str, str]]:
    raw_label = context_label_for_mapping(context, "use_label")
    label = normalized(raw_label)
    targets: list[tuple[str, str, str]] = []

    if text_has(label, ("mixed-use", "mixed use", "mischnutzung", "gemischt genutzt", "nutzungsmischung", "wohn- und", "wohnen und arbeiten", "buero-/mixed", "buro-/mixed")):
        add_context_target(targets, existing_nodes, "nutzung/Mischnutzung", "rule_high", "explicit_mixed_use_label")
    housing_match = text_has(label, ("wohnung", "wohnungen", "wohnhaus", "wohnungsbau", "housing", "residential", "einfamilienhaus", "reihenhaus", "doppelhaus", "studentenwohn", "studierendenwohn", "collectief", "woongroep"))
    if label_has_word(label, "wohnen") and "mehr als wohnen" not in label:
        housing_match = True
    if housing_match:
        add_context_target(targets, existing_nodes, "nutzung/Wohnen", "rule_high", "housing_label")
    if text_has(label, ("schule", "kindergarten", "kita", "daycare", "primary school", "montessori", "bildung", "lern-", "lehr", "forschung", "research", "labor fuer", "labor fur")):
        add_context_target(targets, existing_nodes, "nutzung/Schule_Bildung", "rule_high", "education_label")
    office_match = text_has(label, ("office", "arbeitsplatz", "arbeitsplaetze", "arbeitsplatze", "coworking", "workspace", "meeting", "verwaltung", "administrative", "startup", "studios", "arbeitsraeume", "arbeitsraume"))
    if label_has_word(label, "buero") or label_has_word(label, "buro"):
        office_match = True
    if office_match:
        add_context_target(targets, existing_nodes, "nutzung/Buero", "rule_high", "office_label")
    if text_has(label, ("kultur", "museum", "atelier", "ausstellung", "veranstaltung", "theater", "folklore", "design week", "kunst", "galerie", "community space")):
        add_context_target(targets, existing_nodes, "nutzung/Kultur", "rule_high", "culture_label")
    if text_has(label, ("gewerbe", "commercial", "retail", "laden", "shop", "restaurant", "cafe", "cafeteria", "gastronomie", "werkstatt", "workshop", "produktion", "labor", "vineyard", "farm", "markt")):
        add_context_target(targets, existing_nodes, "nutzung/Gewerbe", "rule_medium", "commercial_label")
    if text_has(label, ("sozial", "social housing", "sozialbau", "nachbarschaft", "community centre", "community center", "gemeinwohl")):
        add_context_target(targets, existing_nodes, "nutzung/Sozialbau", "rule_medium", "social_use_label")
    infrastructure_use_match = text_has(label, ("substation", "umspann", "feuerwache", "fire station", "highway", "tunnel", "footbridge", "pipeline", "energieversorgung", "stromversorgung", "versorgungsinfrastruktur"))
    if label_has_word(label, "bruecke"):
        infrastructure_use_match = True
    if infrastructure_use_match:
        add_context_target(targets, existing_nodes, "nutzung/Infrastruktur", "rule_medium", "infrastructure_use_label")
    if text_has(label, ("lager", "depot", "warehouse", "equipment barn", "materialbank", "materiallager", "bauteillager", "stockpile")):
        add_context_target(targets, existing_nodes, "nutzung/Lager_Depot", "rule_medium", "storage_use_label")

    return targets


def map_bauobjektstatus_targets(context: dict[str, str], existing_nodes: set[str]) -> list[tuple[str, str, str]]:
    label = normalized(context["status_label"])
    targets: list[tuple[str, str, str]] = []

    if text_has(label, ("temporaer", "temporar", "temporary", "zwischennutzung", "9 tage", "9 days", "15 jahre")):
        add_context_target(targets, existing_nodes, "bauobjektstatus/Temporaer", "rule_high", "temporary_label")
    if text_has(label, ("prototyp", "prototype", "pilot", "demonstrator", "testbau", "mock-up", "mockup")):
        add_context_target(targets, existing_nodes, "bauobjektstatus/Prototyp", "rule_medium", "prototype_label")
    if text_has(label, ("wettbewerb", "competition", "wettbewerbsbeitrag", "competition entry")):
        add_context_target(targets, existing_nodes, "bauobjektstatus/Wettbewerb", "rule_high", "competition_label")
    if text_has(label, ("rueckgebaut", "ruckgebaut", "zurueckgebaut", "zuruckgebaut", "demolished", "decommissioned", "abgebrochen", "abbruch")):
        add_context_target(targets, existing_nodes, "bauobjektstatus/Rueckgebaut", "rule_medium", "demolished_or_decommissioned_label")

    planned_tokens = (
        "geplant", "planung", "planungs", "expected", "erwartet", "voraussichtlich",
        "soll", "sollen", "nicht gebaut", "nicht realisiert", "nicht gesichert",
        "keine gebaute", "project entry", "entwurf", "design 2024",
        "fertigstellung geplant", "completion geplant", "baustart erwartet",
    )
    in_bau_tokens = ("in bau", "im bau", "under construction", "on site", "baustelle", "construction started", "baustart")
    built_tokens = (
        "gebaut", "fertigstellung", "fertiggestellt", "completed", "completion",
        "eroeffnung", "eroffnung", "bezug", "uebergabe",
        "ubergabe", "lieferung", "delivered", "inbetriebnahme", "brought online",
        "realisiert", "baujahr",
    )

    strong_planned_tokens = (
        "nicht gebaut", "nicht realisiert", "nicht gesichert", "keine gebaute",
        "expected", "erwartet", "voraussichtlich", "fertigstellung geplant",
        "completion geplant", "baustart erwartet", "project entry",
    )
    built_match = text_has(label, built_tokens)
    planned_match = text_has(label, planned_tokens)
    strong_planned_match = text_has(label, strong_planned_tokens)

    if strong_planned_match or (planned_match and not built_match):
        add_context_target(targets, existing_nodes, "bauobjektstatus/Geplant", "rule_medium", "planned_label")
    elif text_has(label, in_bau_tokens):
        add_context_target(targets, existing_nodes, "bauobjektstatus/In_Bau", "rule_medium", "construction_label")
    elif built_match:
        add_context_target(targets, existing_nodes, "bauobjektstatus/Gebaut", "rule_medium", "built_label")

    if not targets and text_has(label, ("unbekannt", "unklar", "zu verifizieren")):
        add_context_target(targets, existing_nodes, "bauobjektstatus/Unklar", "rule_low", "unclear_status_label")

    return targets


def map_bauobjektrolle_targets(
    context: dict[str, str],
    existing_nodes: set[str],
    *,
    is_receiver_from_installed_edge: bool,
) -> list[tuple[str, str, str]]:
    object_label = normalized(compact_join([
        context["object_label"],
        context["project_label"],
        context_fallback(context),
    ]))
    direct_label = normalized(compact_join([context["object_label"], context["project_label"]]))
    object_only_label = normalized(context["object_label"])
    fallback_label = normalized(context_fallback(context))
    broad_label = normalized(context["broad_label"])
    targets: list[tuple[str, str, str]] = []

    if is_receiver_from_installed_edge:
        add_context_target(targets, existing_nodes, "bauobjektrolle/Empfaengerobjekt", "rule_high", "installed_in_bauobjekt_target")
    elif text_has(broad_label, ("empfaenger", "empfanger", "aufnahmegebaeude", "aufnahmegebaude", "receiver", "receiving building", "nimmt", "aufnimmt", "wiederverwendete bauteile", "re-use-bauteile", "reuse-bauteile")):
        add_context_target(targets, existing_nodes, "bauobjektrolle/Empfaengerobjekt", "rule_medium", "receiver_label")

    if text_has(object_label, ("spendergebaeude", "spendergebaude", "donorgebaeude", "donorgebaude", "donor building", "donorobjekt", "bauteilspender", "materialbank", "rueckbauobjekt", "ruckbauobjekt", "bauteilquelle", "source building")):
        add_context_target(targets, existing_nodes, "bauobjektrolle/Donorobjekt", "rule_medium", "donor_object_label")

    object_existing_match = text_has(object_only_label, ("bestandsgebaeude", "bestandsgebaude", "bestehend", "existing", "ehemalig", "altes", "alte "))
    project_existing_match = text_has(direct_label, ("retained", "adaptive reuse", "retrofit", "sanierung", "renovierung", "conservation", "rekonversion", "umbau des", "umbau der", "umbau eines", "umbau einer"))
    direct_existing_match = object_existing_match or project_existing_match
    fallback_existing_match = text_has(fallback_label, ("ist die erhaltene", "erhaltene ehemalige", "wurde umgenutzt", "wurde ertuechtigt", "wurde ertuchtigt", "wurde saniert", "wurde renoviert", "wurde instand gesetzt"))
    if direct_existing_match or fallback_existing_match:
        add_context_target(targets, existing_nodes, "bauobjektrolle/Bestandsobjekt", "rule_medium", "existing_building_label")

    if text_has(broad_label, ("same-site", "same site", "on-site", "onsite", "vor ort", "am standort", "aus dem bestand", "vom bestand", "vorgaengerbau", "vorgangerbau", "aus der alten", "from the old", "eigener bestand", "eigene bestands")):
        add_context_target(targets, existing_nodes, "bauobjektrolle/Same_Site_Donor_Receiver", "rule_medium", "same_site_label")

    if text_has(object_label, ("zwischenlager", "materialdepot", "materiallager", "bauteillager", "reuse centre", "reuse center", "ressurssentral", "stockpile")):
        add_context_target(targets, existing_nodes, "bauobjektrolle/Zwischenlager", "rule_medium", "storage_station_label")

    return targets


def map_bauaufgabe_intervention_targets(context: dict[str, str], existing_nodes: set[str]) -> list[tuple[str, str, str]]:
    label = normalized(context_label_for_mapping(context, "project_label", "object_label"))
    targets: list[tuple[str, str, str]] = []

    if text_has(label, ("aufstockung", "aufstock", "additional storey", "additional story", "roof extension")):
        add_context_target(targets, existing_nodes, "bauaufgabe_intervention/Aufstockung", "rule_high", "vertical_extension_label")
    if text_has(label, ("neubau", "ersatzneubau", "new build", "new construction", "neu errichtet", "neu gebaut")):
        add_context_target(targets, existing_nodes, "bauaufgabe_intervention/Neubau", "rule_high", "new_build_label")
    if text_has(label, ("umbau", "transformation", "transformations", "adaptive reuse", "retrofit", "rekonversion", "conversion", "weiterbau")):
        add_context_target(targets, existing_nodes, "bauaufgabe_intervention/Umbau", "rule_medium", "conversion_or_retrofit_label")
    if text_has(label, ("umnutzung", "umgenutzt", "nutzungswechsel", "neue nutzung", "conversion to", "converted into")):
        add_context_target(targets, existing_nodes, "bauaufgabe_intervention/Umnutzung", "rule_medium", "change_of_use_label")
    if text_has(label, ("sanierung", "renovierung", "renovation", "refurbishment", "ertuechtigung", "ertuchtigung", "instandsetzung")):
        add_context_target(targets, existing_nodes, "bauaufgabe_intervention/Sanierung", "rule_medium", "renovation_label")
    if text_has(label, ("erweiterung", "extension", "anbau", "addition", "ergaenzung", "erganzung", "ergaenzungsbau", "erganzungsbau")):
        add_context_target(targets, existing_nodes, "bauaufgabe_intervention/Erweiterung", "rule_medium", "extension_label")
    if text_has(label, ("innenausbau", "fit-out", "fit out", "bueroausbau", "buroausbau", "office fit")):
        add_context_target(targets, existing_nodes, "bauaufgabe_intervention/Fit_out", "rule_medium", "fitout_label")
    if text_has(label, ("translozierung", "translocation", "versetzt", "umgesetzt", "relocation", "verpflanzung")):
        add_context_target(targets, existing_nodes, "bauaufgabe_intervention/Translozierung", "rule_high", "translocation_label")
    rueckbau_match = text_has(label, ("rueckbau", "ruckbau", "teilrueckbau", "teilruckbau", "abbruch", "demontage", "dismantling", "deconstruction"))
    if rueckbau_match and (
        text_has(label, ("spender", "donor", "bauteilernte", "rueckbau statt abbruch", "ruckbau statt abbruch", "rueckbauprojekt", "ruckbauprojekt"))
        or "neubau" not in label
    ):
        add_context_target(targets, existing_nodes, "bauaufgabe_intervention/Rueckbau", "rule_medium", "deconstruction_label")
    if text_has(label, ("wiederaufbau", "wieder aufgebaut", "reassembled", "reconstruction", "rebuilt")):
        add_context_target(targets, existing_nodes, "bauaufgabe_intervention/Wiederaufbau", "rule_medium", "rebuild_label")

    return targets


def add_building_context_edge(
    additions: list[dict[str, str]],
    existing_keys: set[tuple[str, str, str]],
    *,
    source: str,
    source_entity: str,
    source_id: str,
    relation: str,
    target: str,
    field: str,
    raw_label: str,
    confidence: str,
    resolution_rule: str,
    legacy_path: str,
) -> bool:
    key = (source, relation, target)
    if key in existing_keys:
        return False
    target_entity, target_id = target.split("/", 1)
    additions.append({
        "source": source,
        "source_entity": source_entity,
        "source_id": source_id,
        "relation": relation,
        "target": target,
        "target_entity": target_entity,
        "target_id": target_id,
        "field": field,
        "raw_label": raw_label,
        "confidence": confidence,
        "resolution_rule": resolution_rule,
        "legacy_path": legacy_path,
        "original_source": source,
        "original_relation": relation,
        "original_target": target,
        "edge_cleaning": "added_gap_50r",
    })
    existing_keys.add(key)
    return True


def build_bauobjekt_context_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    existing_keys = existing_edge_keys(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()
    project_by_id = project_rows_by_id()
    receiver_targets = installed_bauobjekt_targets(edge_rows)

    for node_row in sorted(inventory_rows_for_entity("bauobjekt"), key=lambda row: row["typed_path"]):
        stats["bauobjekt_rows_scanned"] += 1
        context = building_context_for_bauobjekt(node_row)
        source = node_row["typed_path"]
        legacy_path = context["legacy_path"]

        mapping_groups = [
            (
                "has_bauobjektklasse",
                "BAUOBJEKT:object_context",
                context_label_for_report(context, "object_label", "project_label"),
                map_bauobjektklasse_targets(context, existing_nodes),
                "label_50r_has_bauobjektklasse_bauobjekt_context",
            ),
            (
                "has_nutzung",
                "BAUOBJEKT:use_context",
                context_label_for_report(context, "use_label"),
                map_nutzung_targets(context, existing_nodes),
                "label_50r_has_nutzung_bauobjekt_context",
            ),
            (
                "has_bauobjektstatus",
                "BAUOBJEKT:status_context",
                context_label_for_report(context, "status_label"),
                map_bauobjektstatus_targets(context, existing_nodes),
                "label_50r_has_bauobjektstatus_bauobjekt_context",
            ),
            (
                "has_bauobjektrolle",
                "BAUOBJEKT:role_context",
                context_label_for_report(context, "broad_label"),
                map_bauobjektrolle_targets(
                    context,
                    existing_nodes,
                    is_receiver_from_installed_edge=source in receiver_targets,
                ),
                "label_50r_has_bauobjektrolle_bauobjekt_context",
            ),
        ]

        for relation, field, raw_label, targets, rule in mapping_groups:
            if not targets:
                stats[f"{relation}_without_match"] += 1
                skipped.append({
                    "source": source,
                    "legacy_path": legacy_path,
                    "raw_label": raw_label,
                    "reason": f"no_{relation}_target",
                })
                continue
            for target, confidence, reason in targets:
                if add_building_context_edge(
                    additions, existing_keys,
                    source=source,
                    source_entity="bauobjekt",
                    source_id=node_row["id"],
                    relation=relation,
                    target=target,
                    field=f"{field}:{reason}",
                    raw_label=raw_label,
                    confidence=confidence,
                    resolution_rule=rule,
                    legacy_path=legacy_path,
                ):
                    stats[f"{relation}_edges"] += 1
                else:
                    stats["duplicates_skipped"] += 1

        intervention_targets = map_bauaufgabe_intervention_targets(context, existing_nodes)
        project_row = project_by_id.get(node_row["id"])
        if not intervention_targets:
            stats["has_bauaufgabe_intervention_without_match"] += 1
            skipped.append({
                "source": source,
                "legacy_path": legacy_path,
                "raw_label": context_label_for_report(context, "project_label", "object_label"),
                "reason": "no_has_bauaufgabe_intervention_target",
            })
            continue
        if not project_row:
            stats["intervention_without_project_node"] += 1
            skipped.append({
                "source": source,
                "legacy_path": legacy_path,
                "raw_label": context_label_for_report(context, "project_label", "object_label"),
                "reason": "no_project_node_for_intervention",
            })
            continue
        for target, confidence, reason in intervention_targets:
            if add_building_context_edge(
                additions, existing_keys,
                source=project_row["typed_path"],
                source_entity="projekt",
                source_id=project_row["id"],
                relation="has_bauaufgabe_intervention",
                target=target,
                field=f"PROJEKT:intervention_context:{reason}",
                raw_label=context_label_for_report(context, "project_label", "object_label"),
                confidence=confidence,
                resolution_rule="label_50r_has_bauaufgabe_intervention_project_context",
                legacy_path=legacy_path,
            ):
                stats["has_bauaufgabe_intervention_edges"] += 1
            else:
                stats["duplicates_skipped"] += 1

    stats["additions"] = len(additions)
    stats["sources_with_additions"] = len({row["source"] for row in additions})
    return edge_rows + additions, additions, stats, skipped


def _warnung_bestandserhalt_primary_clause_positive(bullet: str) -> bool:
    """True when the first clause of the EINORDNUNG bullet affirms the warning (ja), not nein."""
    if not bullet or is_uncertain(bullet):
        return False
    primary = bullet.split(";")[0].strip()
    n = normalized(primary)
    if n.startswith("nein"):
        return False
    if n.startswith("ja"):
        return True
    return False


def build_kontextmerkmal_edges(
    edge_rows: list[dict[str, str]],
    existing_nodes: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], Counter[str], list[dict[str, str]]]:
    """50v — has_kontextmerkmal from EINORDNUNG bullet Warnung Bestandserhalt -> kontextmerkmal/Bestandserhalt_Policy."""
    existing_keys = existing_edge_keys(edge_rows)
    additions: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    target = "kontextmerkmal/Bestandserhalt_Policy"
    if target not in existing_nodes:
        stats["missing_target_node"] = 1
        return edge_rows, additions, stats, skipped

    fall_by_id = {row["id"]: row for row in inventory_rows_for_entity("fallstudie")}
    source_dir = gebaeude_dir()

    for path in sorted(source_dir.glob("*.md")):
        case_id = path.stem
        stats["gebaeude_files_scanned"] += 1
        fs_row = fall_by_id.get(case_id)
        if not fs_row:
            stats["cases_without_fallstudie_node"] += 1
            skipped.append({
                "case_id": case_id,
                "legacy_path": str(path.relative_to(ROOT)),
                "reason": "no_fallstudie_inventory_row",
            })
            continue

        markdown = path.read_text(encoding="utf-8", errors="replace")
        bullet = extract_markdown_bullet(markdown, "Warnung Bestandserhalt")
        if not _warnung_bestandserhalt_primary_clause_positive(bullet):
            stats["cases_without_ja_warnung"] += 1
            continue

        source = fs_row["typed_path"]
        key = (source, "has_kontextmerkmal", target)
        if key in existing_keys:
            stats["duplicates_skipped"] += 1
            continue

        target_entity, target_id = target.split("/", 1)
        additions.append({
            "source": source,
            "source_entity": "fallstudie",
            "source_id": fs_row["id"],
            "relation": "has_kontextmerkmal",
            "target": target,
            "target_entity": target_entity,
            "target_id": target_id,
            "field": "EINORDNUNG:Warnung Bestandserhalt",
            "raw_label": bullet,
            "confidence": "structural",
            "resolution_rule": "bullet_50v_has_kontextmerkmal_warnung_bestandserhalt",
            "legacy_path": str(path.relative_to(ROOT)),
            "original_source": source,
            "original_relation": "has_kontextmerkmal",
            "original_target": target,
            "edge_cleaning": "added_gap_50v",
        })
        existing_keys.add(key)
        stats["has_kontextmerkmal_edges"] += 1

    stats["additions"] = len(additions)
    return edge_rows + additions, additions, stats, skipped


BATCHES = {
    "50a_reuse_strategie": build_reuse_strategy_edges,
    "50b_fuegung_verbindung": build_connection_edges,
    "50c_reuse_einsatzstatus": build_status_edges,
    "50d_prozessphase": build_process_phase_edges,
    "50e_rueckbauverfahren": build_rueckbauverfahren_edges,
    "50f_located_in_ort": build_located_in_ort_edges,
    "50g_has_huerde": build_huerde_edges,
    "50h_has_pruefung_nachweis": build_pruefung_edges,
    "50i_has_beschaffungsweg": build_beschaffungsweg_edges,
    "50s_has_ressourcenquelle": build_ressourcenquelle_edges,
    "50j_has_aufbereitungsverfahren": build_aufbereitungsverfahren_edges,
    "50u_has_methode": build_methode_edges,
    "50k_has_logistik": build_logistik_edges,
    "50l_has_wirtschaft": build_wirtschaft_edges,
    "50m_has_rechtliche_bedingung": build_rechtliche_bedingung_edges,
    "50n_has_schadstoff": build_schadstoff_edges,
    "50o_has_konstruktion": build_konstruktion_edges,
    "50p_has_bauteilprofil": build_bauteilprofil_edges,
    "50q_has_digital_evidence": build_digital_evidence_edges,
    "50r_has_bauobjekt_context": build_bauobjekt_context_edges,
    "50v_has_kontextmerkmal": build_kontextmerkmal_edges,
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
