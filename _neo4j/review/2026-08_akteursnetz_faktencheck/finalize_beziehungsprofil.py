"""Apply the approved relationship-profile taxonomy to the LaTeX graph.

This is report-only.  It never writes to Neo4j.  The visible relationship set
comes from the same loader as the graph and therefore respects all endpoint
redirects and evidence-based edge removals.
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
PROPOSALS = BASE / "beziehungsprofil_review" / "profile_proposals.json"
OUT_JSON = BASE / "beziehungsprofil_final.json"
OUT_CSV = BASE / "beziehungsprofil_final.csv"
OUT_MD = BASE / "BEZIEHUNGSPROFIL_FINAL.md"
REVIEW_RUN = "2026-08-20_beziehungsprofil_approved"

ALLOWED = {
    "Projektübergreifend / institutionell",
    "Projektübergreifend / strategisch",
    "Projektübergreifend / operativ",
    "Vorhabenspezifisch / Vorhaben",
    "Vorhabenspezifisch / Leistung",
    "Vorhabenspezifisch / Ereignis",
}

LABELS = {
    "Übergreifend / institutionell": "Projektübergreifend / institutionell",
    "Übergreifend / strategisch": "Projektübergreifend / strategisch",
    "Übergreifend / operativ": "Projektübergreifend / operativ",
    "Einzelfall / Vorhaben": "Vorhabenspezifisch / Vorhaben",
    "Einzelfall / Leistung": "Vorhabenspezifisch / Leistung",
    "Einzelfall / Ereignis": "Vorhabenspezifisch / Ereignis",
}

PROFILE_OVERRIDES = {
    "CH:K007": "Vorhabenspezifisch / Ereignis",
    "CH:K026": "Vorhabenspezifisch / Ereignis",
    "CH:K036": "Projektübergreifend / institutionell",
}

TYPE_CORRECTIONS = {
    "AT:K023": {
        "beziehungsart": "Soziale Rückbauarbeit",
        "richtung": "B→A",
        "beschreibung": "Beschäftigte mit DRZ 25 Personen beim Rückbau.",
        "evidence_quote": (
            "Im Dusika-Stadion fanden durch die Zusammenarbeit mit Die KÜMMEREI "
            "(Trägerin: BFI Wien/Job-TransFair) und DRZ 25 Personen Beschäftigung."
        ),
        "reason": "Die OTS-Quelle nennt Träger, Tätigkeit und Beschäftigung im Projekt.",
    },
    "CH:K007": {
        "beziehungsart": "Gründungsimpuls",
        "richtung": "A→B",
        "beschreibung": "Gab den Impuls zur Gründung.",
        "reason": "Zirkular nennt ELYS als Auslöser seiner Gründung.",
    },
    "CH:K026": {
        "beziehungsart": "Gründungsimpuls",
        "richtung": "A→B",
        "beschreibung": "Gab den Impuls zur Gründung.",
        "reason": "Zirkular nennt K.118 als Auslöser seiner Gründung.",
    },
    "CH:K036": {
        "beziehungsart": "Plattformzugehörigkeit",
        "richtung": "A→B",
        "beschreibung": "Umfasst UMAR als Forschungsunit.",
        "reason": "Die Quelle bezeichnet UMAR ausdrücklich als NEST-Unit.",
    },
    "DE:K002": {
        "beziehungsart": "Testbau",
        "richtung": "B→A",
        "beschreibung": "Errichtete mit Biele drei Testbauten aus Platten.",
        "reason": "Die Quelle nennt Asams konkrete Errichtung der drei Testbauten.",
    },
    "DE:K005": {
        "beziehungsart": "Projektleitung",
        "richtung": "A→B",
        "beschreibung": "Leitete und initiierte das Pilotprojekt.",
        "reason": "Die Quelle nennt Asam als Leiter und Mitinitiator.",
    },
    "SE:K023": {
        "beziehungsart": "Konsortialpartnerschaft",
        "richtung": "—",
        "beschreibung": "Arbeiteten im schwedischen ReCreate-Pilot zusammen.",
        "reason": "KTH nennt beide als Beteiligte des schwedischen Piloten.",
    },
}

REMOVALS = {
    "AT:K004": (
        "Die Quelle nennt DRZ nur als operativen Partner; eine konkrete Aufgabe "
        "ist nicht belegt."
    ),
    "NL:K019": (
        "Die Quelle belegt wiederverwendete Träger, aber keine bilaterale "
        "Beziehung zwischen Leiden University und BioPartner 5."
    ),
}

DURATION_FIELDS = {
    "dauer",
    "dauer_status",
    "dauer_begruendung",
    "dauer_warnung",
    "dauer_review_run",
    "dauer_evidence_url",
    "dauer_evidence_quote",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _visible_rows():
    network = load_network()
    by_country = load_kanten(
        DEFAULT.kanten_klassifikation_path,
        network,
        DEFAULT.merge_strict_path,
    )
    rows = {row["id"]: row for values in by_country.values() for row in values}
    return network, rows


def main() -> None:
    classification = _load(CLASSIFICATION)
    proposals = {
        row["review_id"]: row
        for row in _load(PROPOSALS)["relationships"]
        if row["origin"] == "baseline_264"
    }

    for row in classification.values():
        for field in DURATION_FIELDS:
            row.pop(field, None)

    for rid, reason in REMOVALS.items():
        row = classification[rid]
        row["entfernen"] = True
        row["removal_reason"] = reason
        row["review_status"] = "reviewed_remove"
        row["profile_review_run"] = REVIEW_RUN

    for rid, correction in TYPE_CORRECTIONS.items():
        row = classification[rid]
        for field in ("beziehungsart", "richtung", "beschreibung", "evidence_quote"):
            if field in correction:
                row[field] = correction[field]
        row["type_correction_reason"] = correction["reason"]
        row["type_review_run"] = REVIEW_RUN

    network, visible = _visible_rows()
    if len(network.drawn) != 262 or len(visible) != 262:
        raise RuntimeError(
            f"evidence-pruned graph changed: {len(network.drawn)} edges, "
            f"{len(visible)} table rows; expected 262/262"
        )

    for rid in visible:
        proposal = proposals.get(rid)
        if not proposal:
            raise RuntimeError(f"missing profile proposal for visible relationship {rid}")
        profile = PROFILE_OVERRIDES.get(rid) or LABELS[proposal["profile_proposal"]]
        if profile not in ALLOWED:
            raise RuntimeError(f"invalid profile {profile!r} for {rid}")
        row = classification[rid]
        row["beziehungsprofil"] = profile
        row["beziehungsprofil_status"] = "approved"
        row["beziehungsprofil_begruendung"] = proposal["reason"]
        row["profile_review_run"] = REVIEW_RUN

    # Historical or filtered rows keep no stale profile from an earlier run.
    for rid, row in classification.items():
        if rid not in visible:
            row.pop("beziehungsprofil", None)
            row.pop("beziehungsprofil_status", None)
            row.pop("beziehungsprofil_begruendung", None)

    CLASSIFICATION.write_text(
        json.dumps(classification, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Reload from disk so the report proves the canonical values.
    network, visible = _visible_rows()
    public = []
    for rid in sorted(visible, key=lambda value: (visible[value]["cc"], value)):
        row = visible[rid]
        if not row.get("evidence_url", "").startswith(("http://", "https://")):
            raise RuntimeError(f"visible relationship {rid} has no source URL")
        if not row.get("evidence_quote", "").strip():
            raise RuntimeError(f"visible relationship {rid} has no evidence quotation")
        if not row.get("beschreibung", "").strip() or len(row["beschreibung"]) > 60:
            raise RuntimeError(
                f"visible relationship {rid} has invalid description length "
                f"{len(row.get('beschreibung', ''))}"
            )
        if row.get("beziehungsprofil") not in ALLOWED:
            raise RuntimeError(f"visible relationship {rid} has no approved profile")
        a, b = row["pair"]
        public.append({
            "id": rid,
            "land": row["cc"],
            "von": network.raw.name(a),
            "richtung": row["richtung"],
            "nach": network.raw.name(b),
            "beziehungsart": row["beziehungsart"],
            "beschreibung": row["beschreibung"],
            "beziehungsprofil": row["beziehungsprofil"],
            "evidence_url": row["evidence_url"],
            "evidence_quote": row["evidence_quote"],
        })

    payload = {
        "review_run": REVIEW_RUN,
        "approved_for_latex": True,
        "neo4j_changed": False,
        "visible_nodes": sum(len(p.actors) + len(p.projects) for p in network.panels.values()),
        "visible_edges": len(network.drawn),
        "classification_sha256": _sha256(CLASSIFICATION),
        "removed_relationships": REMOVALS,
        "relationships": public,
    }
    OUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(public[0]), delimiter=";")
        writer.writeheader()
        writer.writerows(public)

    counts = Counter(row["beziehungsprofil"] for row in public)
    lines = [
        "# Beziehungsprofil der aktuellen LaTeX-Kanten",
        "",
        "**Freigegeben und angewendet am 20.08.2026.**",
        "",
        f"- Sichtbare Knoten: **{payload['visible_nodes']}**",
        f"- Sichtbare Kanten: **{payload['visible_edges']}**",
        "- Neo4j geändert: **nein**",
        "- Jede sichtbare Kante besitzt Beschreibung, Belegzitat und URL: **ja**",
        "",
        "## Verteilung",
        "",
    ]
    for profile in sorted(ALLOWED):
        lines.append(f"- **{profile}:** {counts[profile]}")
    lines.extend([
        "",
        "## Entfernt",
        "",
        "- **AT:K004:** konkrete Aufgabe des DRZ nicht belegt.",
        "- **NL:K019:** Materialfluss belegt, bilaterale Beziehung nicht belegt.",
        "",
        "Die Endknoten bleiben im Graph sichtbar. Nur die unbelegten Kanten entfallen.",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {payload['visible_nodes']} nodes, {len(public)} sourced edges, {dict(counts)}")


if __name__ == "__main__":
    main()
