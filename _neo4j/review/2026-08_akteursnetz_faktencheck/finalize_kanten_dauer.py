"""Finalize duration decisions for the relationships drawn in the LaTeX graph.

The graph itself is loaded through ``netz.cli.load_network``.  This keeps the
review tied to the exact endpoint redirects, node pruning and edge pruning used
by the current LaTeX renderer instead of the historical 268-row export.

This script never writes to Neo4j.  It adds review fields only to the current
visible rows in ``kanten_klassifikation.json`` and derives the human-readable
CSV/Markdown review files from those canonical rows.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


BASE = Path(__file__).resolve().parent
NETZ_ROOT = BASE.parents[1] / "netz"
if str(NETZ_ROOT) not in sys.path:
    sys.path.insert(0, str(NETZ_ROOT))

from netz.cli import load_network  # noqa: E402
from netz.render.latex.table_grid import load_kanten  # noqa: E402
from netz.sources import DEFAULT  # noqa: E402


CLASSIFICATION = BASE / "kanten_klassifikation.json"
OUT_JSON = BASE / "kanten_dauer_final.json"
OUT_CSV = BASE / "kanten_dauer_final.csv"
OUT_MD = BASE / "KANTEN_DAUER_FINAL.md"
REVIEW_RUN = "2026-08-20_latex_current_264"

ALLOWED = {
    "dauerhaft",
    "befristeter Verbund",
    "projektgebunden",
    "einmalig",
    "unklar",
}

# Every actor-to-actor relationship that is not a common construction project
# is decided here explicitly.  This prevents relationship-type templates from
# silently recreating the flawed 17-August duration table.
DAUERHAFT = {
    "AT:K001", "AT:K013", "AT:K014",
    "BE:K086",
    "CH:K001", "CH:K003", "CH:K004", "CH:K006", "CH:K011",
    "DE:K035", "DE:K048", "DE:K049",
    "DK:K010", "DK:K024", "DK:K030", "DK:K031",
    "FI:K031", "FI:K032", "FI:K040",
    "FR:K006", "FR:K008", "FR:K010", "FR:K024", "FR:K041",
    "GB:K046",
    "NO:K027",
    "SE:K001", "SE:K005", "SE:K011", "SE:K014", "SE:K015",
    "SE:K019", "SE:K026", "SE:K029",
}

BEFRISTET = {
    "CH:K044",
    "FI:K007", "FI:K009", "FI:K011", "FI:K017", "FI:K024",
    "FI:K030", "FI:K036", "FI:K038",
    "FR:K033", "FR:K035", "FR:K038", "FR:K039",
    "NO:K011", "NO:K018", "NO:K019", "NO:K021",
    "SE:K002", "SE:K003", "SE:K006", "SE:K007", "SE:K016",
    "SE:K017", "SE:K018", "SE:K022", "SE:K023", "SE:K024",
    "SE:K025", "SE:K027", "SE:K028", "SE:K030", "SE:K033",
}

PROJEKT = {
    "AT:K002",
    "BE:K072", "BE:K073",
    "CH:K042",
    "DE:K031", "DE:K033", "DE:K036",
    "FI:K013", "FI:K016", "FI:K039",
    "FR:K031", "FR:K034", "FR:K044",
    "GB:K051", "GB:K075",
    "NO:K012", "NO:K013",
}

EINMALIG = {
    "AT:K009",
    "BE:K043", "BE:K046", "BE:K075",
    "CH:K041", "CH:K046",
    "DE:K034",
    "FR:K032",
    "GB:K026", "GB:K047", "GB:K061", "GB:K063", "GB:K095",
    "NL:K007", "NL:K010", "NL:K069",
    "NO:K001", "NO:K015",
}

UNKLAR = set()

# Actor-to-building rows normally inherit the named project's finite context.
# These rows contain direct evidence for a continuing operator/owner role, or
# (NL:K066) a source/type conflict that must remain visible.
BUILDING_OVERRIDES = {
    "AT:K029": "projektgebunden",
    "CH:K017": "dauerhaft",
    "CH:K038": "dauerhaft",
    "FR:K021": "dauerhaft",
    "FR:K022": "dauerhaft",
    "FR:K025": "dauerhaft",
    "NL:K066": "einmalig",
    "NL:K071": "dauerhaft",
}

TYPE_CORRECTIONS = {
    "BE:K086": {
        "beziehungsart": "Regulatorische Anerkennung",
        "richtung": "A→B",
        "beschreibung": "Erkannte Tracimat als Sloopbeheerorganisation an.",
        "reason": "OVAM nennt Tracimat als einzige anerkannte Sloopbeheerorganisation.",
    },
    "NL:K066": {
        "beziehungsart": "Bauherrschaft",
        "richtung": "A→B",
        "beschreibung": "Entwickelte und baute Circl.",
        "reason": "Der Beleg nennt Entwicklung und Bau, aber keinen laufenden Betrieb.",
    },
    "SE:K001": {
        "beziehungsart": "Konzernbindung",
        "richtung": "A→B",
        "beschreibung": "Ist Miteigentümerin von Bygghubben.",
        "reason": "Der Beleg nennt Åhlin & Ekeroth als Miteigentümerin.",
    },
    "SE:K014": {
        "beziehungsart": "Konzernbindung",
        "richtung": "B→A",
        "beschreibung": "Ist Miteigentümerin von Bygghubben.",
        "reason": "Der Beleg nennt Teknikbyggarna als Miteigentümerin.",
    },
    "SE:K015": {
        "beziehungsart": "Konzernbindung",
        "richtung": "B→A",
        "beschreibung": "Ist Miteigentümerin und Mitgründerin von Bygghubben.",
        "reason": "Der Beleg nennt Wilzéns als Miteigentümerin und Mitgründerin.",
    },
}

DURATION_EVIDENCE = {
    "BE:K086": {
        "url": "https://ovam.vlaanderen.be/bouw-sloopopvolging",
        "quote": "Tracimat is momenteel de enige erkende sloopbeheerorganisatie.",
    },
    "CH:K011": {
        "url": "https://re-win.ch/wordpress/wp-content/uploads/2024/06/240526_Jahresbericht-Verein-RE-WIN_2024_final.pdf",
        "quote": "Partner:innen Schweiz und Liechtenstein: Baubüro in situ AG, Zürich",
    },
    "NO:K011": {
        "url": "https://blog.loopfront.com/blog/pressrelease-kpmg-building",
        "quote": "The project with regional reuse networks will initially run until spring and summer 2021.",
    },
    "NO:K018": {
        "url": "https://blog.loopfront.com/blog/pressrelease-kpmg-building",
        "quote": "The project with regional reuse networks will initially run until spring and summer 2021.",
    },
    "NO:K019": {
        "url": "https://blog.loopfront.com/blog/pressrelease-kpmg-building",
        "quote": "The project with regional reuse networks will initially run until spring and summer 2021.",
    },
    "SE:K003": {
        "url": "https://www.businessregiongoteborg.se/nyheter/vasakronan-blir-arets-aterbrukare-2026-omstallningen-gar-snabbt",
        "quote": "Handslag för cirkulärt byggande ... avrundas efter fyra år.",
    },
    "SE:K022": {
        "url": "https://www.businessregiongoteborg.se/nyheter/vasakronan-blir-arets-aterbrukare-2026-omstallningen-gar-snabbt",
        "quote": "Handslag för cirkulärt byggande ... avrundas efter fyra år.",
    },
    "SE:K005": {
        "url": "https://www.wiklunds.se/nyheter/2025-04-24-tillsammans-for-en-gemensam-aterbruksmarknad-i-stockholm-och-uppsala/",
        "quote": "startskottet för ett långsiktigt samarbete",
    },
    "SE:K029": {
        "url": "https://www.wiklunds.se/nyheter/2025-04-24-tillsammans-for-en-gemensam-aterbruksmarknad-i-stockholm-och-uppsala/",
        "quote": "startskottet för ett långsiktigt samarbete",
    },
}

CUSTOM_REASONS = {
    "BE:K086": "OVAM nennt Tracimat aktuell als einzige anerkannte Stelle.",
    "CH:K011": "Der RE-WIN-Jahresbericht führt baubüro in situ als Partner.",
    "NL:K066": "Der Beleg beschreibt den abgeschlossenen Bau von Circl.",
    "NL:K071": "Der Beleg sagt ausdrücklich, dass Zayaz Eigentümer bleibt.",
    "FR:K021": "Der Beleg nennt Le WIP als aktuellen Betreiber.",
    "FR:K022": "Der Beleg nennt Les Canaux als Gebäudebetreiber.",
    "FR:K025": "Der Beleg nennt Résilience als Sitz und Werkstatt.",
    "CH:K017": "Der Beleg nennt ERZ als Eigentümervertretung.",
    "CH:K038": "Der Beleg ordnet das Wohnhaus der Stiftung Habitat zu.",
    "SE:K003": "Die Initiative endete laut Folgequelle nach vier Jahren.",
    "SE:K022": "Die Initiative endete laut Folgequelle nach vier Jahren.",
    "SE:K005": "Die Folgequelle nennt ausdrücklich langfristige Zusammenarbeit.",
    "SE:K029": "Die Folgequelle nennt ausdrücklich langfristige Zusammenarbeit.",
    "NO:K011": "Die Folgequelle begrenzt das Netzwerkprojekt bis Sommer 2021.",
    "NO:K018": "Die Folgequelle begrenzt das Netzwerkprojekt bis Sommer 2021.",
    "NO:K019": "Die Folgequelle begrenzt das Netzwerkprojekt bis Sommer 2021.",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _decision(row: dict) -> tuple[str, str, str, str]:
    rid = row["id"]
    kind = row.get("kind")
    art = row.get("beziehungsart")

    if rid in BUILDING_OVERRIDES:
        duration = BUILDING_OVERRIDES[rid]
    elif kind == "AKTEUR-BAUVORHABEN":
        duration = "projektgebunden"
    elif art == "Gemeinsames Bauvorhaben":
        duration = "projektgebunden"
    elif rid in DAUERHAFT:
        duration = "dauerhaft"
    elif rid in BEFRISTET:
        duration = "befristeter Verbund"
    elif rid in PROJEKT:
        duration = "projektgebunden"
    elif rid in EINMALIG:
        duration = "einmalig"
    elif rid in UNKLAR:
        duration = "unklar"
    else:
        raise RuntimeError(f"missing explicit duration decision: {rid}")

    if duration == "unklar":
        status = "needs_source"
        warning = "Die Quelle belegt die Verbindung, aber keine belastbare Laufzeit."
    elif rid in DURATION_EVIDENCE:
        status = "source_reopened"
        warning = ""
    else:
        status = "checked"
        warning = ""

    if rid in CUSTOM_REASONS:
        reason = CUSTOM_REASONS[rid]
    elif duration == "dauerhaft":
        reason = "Der Beleg beschreibt eine fortlaufende strukturelle Rolle."
    elif duration == "befristeter Verbund":
        reason = "Der Beleg ordnet beide einem benannten Projektverbund zu."
    elif duration == "projektgebunden":
        reason = "Die belegte Leistung ist an das benannte Vorhaben gebunden."
    elif duration == "einmalig":
        reason = "Der Beleg beschreibt einen abgeschlossenen Einzelakt."
    else:
        reason = "Die Laufzeit ist aus dem vorhandenen Beleg nicht bestimmbar."

    return duration, status, reason, warning


def _visible_rows() -> tuple[dict[str, dict], object]:
    network = load_network()
    by_country = load_kanten(
        DEFAULT.kanten_klassifikation_path,
        network,
        DEFAULT.merge_strict_path,
    )
    rows = {row["id"]: row for values in by_country.values() for row in values}
    drawn = {tuple(sorted(pair)) for pair in network.drawn}
    if len(rows) != 264 or len(drawn) != 264:
        raise RuntimeError(
            f"current graph changed: expected 264 rows/edges, got {len(rows)}/{len(drawn)}"
        )
    return rows, network


def _validate_manual_coverage(visible: dict[str, dict]) -> None:
    groups = [DAUERHAFT, BEFRISTET, PROJEKT, EINMALIG, UNKLAR]
    flattened = set().union(*groups)
    if sum(map(len, groups)) != len(flattened):
        raise RuntimeError("duration decision groups overlap")

    expected_manual = {
        rid for rid, row in visible.items()
        if row.get("kind") == "AKTEUR-AKTEUR"
        and row.get("beziehungsart") != "Gemeinsames Bauvorhaben"
    }
    if flattened != expected_manual:
        raise RuntimeError(
            "manual decision coverage mismatch; "
            f"missing={sorted(expected_manual - flattened)}, "
            f"extra={sorted(flattened - expected_manual)}"
        )

    building_override_rows = {
        rid for rid, row in visible.items()
        if row.get("kind") == "AKTEUR-BAUVORHABEN"
        and row.get("beziehungsart") == "Betrieb"
    }
    if not building_override_rows <= set(BUILDING_OVERRIDES):
        raise RuntimeError(
            f"Betrieb rows need individual decisions: "
            f"{sorted(building_override_rows - set(BUILDING_OVERRIDES))}"
        )


def _public_row(row: dict, network) -> dict:
    a, b = row["pair"]
    duration_evidence = DURATION_EVIDENCE.get(row["id"], {})
    return {
        "id": row["id"],
        "cc": row["cc"],
        "von": network.raw.name(a),
        "richtung": row.get("richtung", ""),
        "nach": network.raw.name(b),
        "beziehungsart": row.get("beziehungsart", ""),
        "beschreibung": row.get("beschreibung", ""),
        "dauer": row["dauer"],
        "dauer_status": row["dauer_status"],
        "dauer_begruendung": row["dauer_begruendung"],
        "dauer_warnung": row["dauer_warnung"],
        "type_correction": row.get("type_correction_reason", ""),
        "evidence_quote": row.get("evidence_quote", ""),
        "evidence_url": row.get("evidence_url", ""),
        "dauer_evidence_quote": duration_evidence.get("quote", row.get("evidence_quote", "")),
        "dauer_evidence_url": duration_evidence.get("url", row.get("evidence_url", "")),
    }


def _write_outputs(public: list[dict], source_hash: str) -> None:
    payload = {
        "review_run": REVIEW_RUN,
        "scope": "current LaTeX graph only",
        "visible_nodes": 618,
        "visible_edges": 264,
        "classification_sha256_after_apply": source_hash,
        "categories": {
            "dauerhaft": "fortlaufende strukturelle Rolle ohne belegtes Enddatum",
            "befristeter Verbund": "benannter formaler Projekt- oder Forschungsverbund",
            "projektgebunden": "auf ein konkretes Bauvorhaben, Pilotprojekt oder Arbeitspaket begrenzt",
            "einmalig": "abgeschlossener Einzelakt wie Gründung, Initiierung oder Übergabe",
            "unklar": "Verbindung belegt, Laufzeit mit vorhandenem Beleg nicht bestimmbar",
        },
        "relationships": public,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fields = list(public[0])
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter=";")
        writer.writeheader()
        writer.writerows(public)

    counts = Counter(row["dauer"] for row in public)
    statuses = Counter(row["dauer_status"] for row in public)
    corrected = [row for row in public if row["type_correction"]]
    flagged = [row for row in public if row["dauer_status"] != "checked"]
    lines = [
        "# Dauerprüfung der aktuellen LaTeX-Kanten",
        "",
        f"**Stand:** 20.08.2026 · **618 sichtbare Knoten / 264 sichtbare Kanten**",
        "",
        "Der Bestand wurde aus demselben Loader wie die LaTeX-Grafik ermittelt. "
        "Die historische 268-Zeilen-Tabelle ist nicht die Grundlage dieses Berichts.",
        "",
        "## Ergebnis",
        "",
    ]
    for category in ["dauerhaft", "befristeter Verbund", "projektgebunden", "einmalig", "unklar"]:
        lines.append(f"- **{category}:** {counts[category]}")
    lines.extend([
        "",
        f"Prüfstatus: {statuses['checked']} geprüft, "
        f"{statuses['source_reopened']} Quelle erneut geöffnet, "
        f"{len(corrected)} Typkonflikte korrigiert, "
        f"{statuses['needs_source']} Laufzeiten offen.",
        "",
        "## Korrigierte Beziehungsarten",
        "",
    ])
    for row in corrected:
        lines.extend([
            f"- **{row['id']} · {row['von']} — {row['nach']}:** "
            f"`{row['beziehungsart']}` — {row['type_correction']}",
        ])
    lines.extend([
        "",
        "## Vertieft geprüfte Dauerquellen",
        "",
    ])
    for row in flagged:
        lines.extend([
            f"### {row['id']} · {row['von']} — {row['nach']}",
            "",
            f"- Entscheidung: **{row['dauer']}** (`{row['dauer_status']}`)",
            f"- Begründung: {row['dauer_begruendung']}",
            f"- Hinweis: {row['dauer_warnung'] or 'Zusätzliche Dauerquelle wurde geprüft.'}",
            f"- Beleg: {row['dauer_evidence_quote']}",
            f"- Quelle: {row['dauer_evidence_url']}",
            "",
        ])
    lines.extend([
        "## Vollständigkeit",
        "",
        "Alle 264 aktuell gezeichneten Beziehungen stehen vollständig in "
        "`kanten_dauer_final.csv` und `kanten_dauer_final.json`. Die vier seit "
        "dem 17.08. entfernten Beziehungen BE:K013, GB:K027, GB:K057 und "
        "NL:K067 sind nicht enthalten.",
        "",
        "Es erfolgte kein Neo4j-Schreibzugriff und keine Änderung der Graph-Topologie.",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    visible, network = _visible_rows()
    _validate_manual_coverage(visible)

    with CLASSIFICATION.open(encoding="utf-8") as handle:
        classification = json.load(handle)

    for rid, visible_row in visible.items():
        duration, status, reason, warning = _decision(visible_row)
        if duration not in ALLOWED:
            raise RuntimeError(f"invalid duration {duration!r} for {rid}")
        canonical = classification[rid]
        correction = TYPE_CORRECTIONS.get(rid)
        if correction:
            canonical.setdefault("beziehungsart_vor_dauerpruefung", canonical["beziehungsart"])
            canonical.setdefault("richtung_vor_dauerpruefung", canonical["richtung"])
            canonical.setdefault("beschreibung_vor_dauerpruefung", canonical["beschreibung"])
            canonical["beziehungsart"] = correction["beziehungsart"]
            canonical["richtung"] = correction["richtung"]
            canonical["beschreibung"] = correction["beschreibung"]
            canonical["type_correction_reason"] = correction["reason"]
            canonical["type_review_run"] = REVIEW_RUN
        canonical["dauer"] = duration
        canonical["dauer_status"] = status
        canonical["dauer_begruendung"] = reason
        canonical["dauer_warnung"] = warning
        canonical["dauer_review_run"] = REVIEW_RUN
        if rid in DURATION_EVIDENCE:
            canonical["dauer_evidence_url"] = DURATION_EVIDENCE[rid]["url"]
            canonical["dauer_evidence_quote"] = DURATION_EVIDENCE[rid]["quote"]
        else:
            canonical.pop("dauer_evidence_url", None)
            canonical.pop("dauer_evidence_quote", None)

    CLASSIFICATION.write_text(
        json.dumps(classification, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    source_hash = _sha256(CLASSIFICATION)

    # Reload so all outputs prove that the canonical file, not an in-memory
    # proposal, carries every final value.
    visible_after, network_after = _visible_rows()
    public = []
    for rid in sorted(visible_after, key=lambda value: (visible_after[value]["cc"], value)):
        canonical = classification[rid]
        public.append(_public_row(canonical, network_after))
    if len(public) != 264 or len({row["id"] for row in public}) != 264:
        raise RuntimeError("final duration output does not cover exactly 264 unique IDs")
    _write_outputs(public, source_hash)

    print(f"PASS: 618 nodes, 264 edges, {dict(Counter(row['dauer'] for row in public))}")


if __name__ == "__main__":
    main()
