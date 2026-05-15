"""LEGACY REVIEW REQUIRED.

Write NODE_CATALOG_BY_ENTITY.md and NODE_CATALOG_BY_NEO4J_LABEL.md from the retired
folder-first `node_inventory.csv`.

To refresh per-label examples inside the schema plan (§5.2), run:
`python _scripts/generate_plan_section_5_2.py`
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from akteur_org_neo4j_label import SLUG_TO_LABEL, neo4j_label_for_akteur_folder
from akteur_person_split import split_akteur_ids
from ort_geo_label import neo4j_label_for_ort_id
from software_tool_label import neo4j_label_for_software_digitaltool_id

# Same order as `SLUG_TO_LABEL` insertion (plan §6.1 typed organisation primaries).
_ORG_TYPED_PRIMARY_LABELS_ORDER: tuple[str, ...] = tuple(SLUG_TO_LABEL.values())

_ORG_CATALOG_DISPLAY_TO_INTERNAL: dict[str, str] = {
    f":{lab}": lab for lab in _ORG_TYPED_PRIMARY_LABELS_ORDER
}
_ORG_CATALOG_DISPLAY_TO_INTERNAL[":Akteur"] = "Akteur"


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    db = repo / "research"
    inv_path = db / "_system" / "node_inventory.csv"
    by_entity: dict[str, list[str]] = defaultdict(list)
    with inv_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            by_entity[row["entity"]].append(row["id"])
    for ent in by_entity:
        by_entity[ent].sort()

    person_from_akteur, org_from_akteur = split_akteur_ids(db, by_entity.get("akteur", []))
    person_all_ids = sorted(set(by_entity.get("person", [])) | set(person_from_akteur))

    ENTITY_TO_NEO4J = {
        "fallstudie": ":Fallbeispiel",
        "projekt": ":Fallbeispiel",
        "bauobjekt": ":Bauwerk",
        "bauteilgruppe": ":Bauteilgruppe",
        "reuse_einsatz": ":Bauteilgruppe",
        "akteur": ":Person or §6.1 organisation label + :Akteur fallback (`akteur_org_neo4j_label.py`)",
        "person": ":Person",
        "quelle": ":Quelle",
        "software_digitaltool": ":Software / :Tool (`software_tool_label.py`; plan §5.6)",
        "reuse_kette": ":Wiederverwendungskette",
        "bauteiltyp": ":Bauteiltyp",
        "material": ":Material",
        "bauteilebene": ":Bauteilebene",
        "bauteilzustand": ":Bauteilzustand",
        "funktionswechsel": ":Funktionswechsel",
        "fuegung_verbindung": ":Verbindungstechnik (subset of folders)",
        "bauweise": ":Bauweise",
        "bausystem": ":Bausystem",
        "tragwerksprinzip": ":Tragwerksprinzip",
        "reuse_einsatzstatus": ":Status",
        "bauobjektstatus": ":Status",
        "bewertungslogik_abgrenzung": ":WiederverwendungsArt",
        "reuse_strategie": ":WiederverwendungsArt (axis reuse_strategie)",
        "ressourcenquelle": ":Ressourcenquelle",
        "beschaffungsweg": ":Beschaffungsweg",
        "prozessphase": ":Prozessphase",
        "rueckbauverfahren": ":Rueckbauverfahren",
        "aufbereitungsverfahren": ":Aufbereitungsverfahren",
        "logistik": ":Logistik",
        "methode": ":Methode",
        "huerde": ":Huerde",
        "schadstoff": ":Schadstoff",
        "pruefung_nachweis": ":PruefungNachweis",
        "leistungsanforderung": ":Leistungsanforderung",
        "norm": ":Norm",
        "rechtliche_bedingung": ":RechtlicheBedingung",
        "nutzung": ":Nutzung",
        "bauaufgabe_intervention": ":BauaufgabeIntervention",
        "ort": ":Land / :Stadt (`ort_geo_label.py`; no :Ort)",
        "akteurrolle": ":Akteurrolle (21 folders → 8 canonical ids)",
        "datenqualitaet": ":Datenqualitaet",
        "tooltyp": "(no label — property on :Tool / :Software)",
        "zertifizierung_bewertungssystem": ":ZertifizierungBewertungssystem",
        "wirtschaft": ":Wirtschaft",
        "foerderprogramm": ":Programm",
        "programm_kontext": ":Programm",
        "datenpunkt": "(measurements on nodes)",
        "datenmodell": "(skipped in Neo4j)",
        "kennwertdefinition": "(property keys)",
        "bauobjektklasse": "(values on :Bauwerk / :Fallbeispiel)",
        "bauobjektrolle": "(GEHÖRT_ZU roles)",
        "dokumenttyp": "(:Quelle.art)",
        "tragwerkstyp": "(folded)",
        "kontextmerkmal": ":Programm / strategy vocabulary",
        "reuse_kettenstation": "(GEHÖRT_ZU edges only)",
        "akteur_beteiligung": "(HAT art akteur)",
        "bauobjekt_beteiligung": "(HAT art akteur)",
    }

    out1 = db / "_system" / "NODE_CATALOG_BY_ENTITY.md"
    lines1: list[str] = []
    lines1.append("# Node catalog by `_database` entity (inventory)")
    lines1.append("")
    lines1.append("Source: `_database/_system/node_inventory.csv` — one row per folder-backed instance.")
    lines1.append(
        "Neo4j targets: `.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md` (52 labels)."
    )
    lines1.append("")
    lines1.append("| Entity (folder) | Count | Typical Neo4j label(s) |")
    lines1.append("| --- | ---: | --- |")
    for ent in sorted(by_entity.keys(), key=str.lower):
        neo = ENTITY_TO_NEO4J.get(ent, "_(see plan §5)_")
        lines1.append(f"| `{ent}/` | {len(by_entity[ent])} | {neo} |")
    lines1.append("")
    lines1.append("---")
    lines1.append("")
    for ent in sorted(by_entity.keys(), key=str.lower):
        neo = ENTITY_TO_NEO4J.get(ent, "")
        lines1.append(f"## `{ent}/` ({len(by_entity[ent])} nodes)")
        if neo:
            lines1.append(f"*Neo4j:* {neo}")
        lines1.append("")
        for nid in by_entity[ent]:
            lines1.append(f"- `{nid}`")
        lines1.append("")
    out1.write_text("\n".join(lines1), encoding="utf-8")

    org_actor_groups: list[tuple[str, list[str]]] = [
        (f":{lab}", ["akteur"]) for lab in _ORG_TYPED_PRIMARY_LABELS_ORDER
    ]
    GROUPS: list[tuple[str, list[str]]] = [
        (":Fallbeispiel", ["fallstudie", "projekt"]),
        (":Bauwerk", ["bauobjekt"]),
        (":Bauteilgruppe", ["bauteilgruppe", "reuse_einsatz"]),
        *org_actor_groups,
        (":Akteur", ["akteur"]),
        (":Person", ["person"]),
        (":Quelle", ["quelle"]),
        (":Software", ["software_digitaltool"]),
        (":Tool", ["software_digitaltool"]),
        (":Wiederverwendungskette", ["reuse_kette"]),
        (":Bauteiltyp", ["bauteiltyp"]),
        (":Material", ["material"]),
        (":Bauteilebene", ["bauteilebene"]),
        (":Bauteilzustand", ["bauteilzustand"]),
        (":Funktionswechsel", ["funktionswechsel"]),
        (":Verbindungstechnik (from `fuegung_verbindung/`)", ["fuegung_verbindung"]),
        (":Bauweise", ["bauweise"]),
        (":Bausystem", ["bausystem"]),
        (":Tragwerksprinzip", ["tragwerksprinzip"]),
        (":Status", ["reuse_einsatzstatus", "bauobjektstatus"]),
        (":WiederverwendungsArt", ["bewertungslogik_abgrenzung", "reuse_strategie"]),
        (":Ressourcenquelle", ["ressourcenquelle"]),
        (":Beschaffungsweg", ["beschaffungsweg"]),
        (":Prozessphase", ["prozessphase"]),
        (":Rueckbauverfahren", ["rueckbauverfahren"]),
        (":Aufbereitungsverfahren", ["aufbereitungsverfahren"]),
        (":Logistik", ["logistik"]),
        (":Methode", ["methode"]),
        (":Huerde", ["huerde"]),
        (":Schadstoff", ["schadstoff"]),
        (":PruefungNachweis", ["pruefung_nachweis"]),
        (":Leistungsanforderung", ["leistungsanforderung"]),
        (":Norm", ["norm"]),
        (":RechtlicheBedingung", ["rechtliche_bedingung"]),
        (":Nutzung", ["nutzung"]),
        (":BauaufgabeIntervention", ["bauaufgabe_intervention"]),
        (":Land", ["ort"]),
        (":Stadt", ["ort"]),
        (":Akteurrolle", ["akteurrolle"]),
        (":Datenqualitaet", ["datenqualitaet"]),
        (":ZertifizierungBewertungssystem", ["zertifizierung_bewertungssystem"]),
        (":Wirtschaft", ["wirtschaft"]),
        (":Programm", ["foerderprogramm", "programm_kontext", "kontextmerkmal"]),
    ]

    used: set[str] = set()
    for _, ents in GROUPS:
        used.update(ents)
    dropped = sorted(set(by_entity.keys()) - used)

    out2 = db / "_system" / "NODE_CATALOG_BY_NEO4J_LABEL.md"
    lines2: list[str] = []
    lines2.append("# Node catalog by Neo4j label (from inventory)")
    lines2.append("")
    lines2.append(
        "Rows from `node_inventory.csv` grouped toward the **52** labels in "
        "`neo4j_schema_catalogue_3bc01035.plan.md`."
    )
    lines2.append(
        "Labels **:Entwurfsentscheidung** and **:Reversibilitaet** have no inventory folders here."
    )
    lines2.append("")
    for label, ents in GROUPS:
        lines2.append(f"## {label}")
        lines2.append("")
        if label in _ORG_CATALOG_DISPLAY_TO_INTERNAL:
            internal = _ORG_CATALOG_DISPLAY_TO_INTERNAL[label]
            if internal == "Akteur":
                lines2.append(
                    "*Inventory:* `akteur/` — §6.1 **fallback** when no typed organisation slug resolves "
                    "(not natural persons; see `akteur_org_neo4j_label.py`)."
                )
            else:
                lines2.append(
                    f"*Inventory:* `akteur/` — organisation primary label **{internal}** (plan §6.1)."
                )
            lines2.append("")
            ids = sorted(
                aid
                for aid in org_from_akteur
                if neo4j_label_for_akteur_folder(db, aid) == internal
            )
        elif label == ":Person":
            lines2.append(
                "*Inventory:* `person/`; plus person-classified rows under `akteur/` (plan §5.2)"
            )
            lines2.append("")
            ids = person_all_ids
        elif label == ":Land":
            lines2.append("*Inventory:* `ort/` — primary label `Land` (`ort_geo_label.py`).")
            lines2.append("")
            ids = sorted(
                oid
                for oid in by_entity.get("ort", [])
                if neo4j_label_for_ort_id(oid) == "Land"
            )
        elif label == ":Stadt":
            lines2.append("*Inventory:* `ort/` — primary label `Stadt` (`ort_geo_label.py`).")
            lines2.append("")
            ids = sorted(
                oid
                for oid in by_entity.get("ort", [])
                if neo4j_label_for_ort_id(oid) == "Stadt"
            )
        elif label in {":Software", ":Tool"}:
            want = label[1:]
            lines2.append(
                "*Inventory:* `software_digitaltool/` — primary label "
                f"`{want}` (`software_tool_label.py`; plan §5.6)."
            )
            lines2.append("")
            ids = sorted(
                sid
                for sid in by_entity.get("software_digitaltool", [])
                if neo4j_label_for_software_digitaltool_id(sid) == want
            )
        else:
            lines2.append(
                "*Inventory:* "
                + ", ".join(f"`{e}/`" for e in ents)
            )
            lines2.append("")
            ids = []
            for e in ents:
                ids.extend(by_entity.get(e, []))
            ids = sorted(set(ids))
        lines2.append(f"*Instance count:* {len(ids)}")
        lines2.append("")
        for nid in ids:
            lines2.append(f"- `{nid}`")
        lines2.append("")

    lines2.append("## Inventory entities without a dedicated Neo4j label row above")
    lines2.append("")
    lines2.append(
        "These folders exist in `_database/` and in `node_inventory.csv` but map to "
        "properties, edges, merges, or skips — not to a separate label in the 52-type catalogue."
    )
    lines2.append("")
    for ent in dropped:
        lines2.append(f"### `{ent}/` ({len(by_entity[ent])} nodes)")
        lines2.append("")
        for nid in by_entity[ent]:
            lines2.append(f"- `{nid}`")
        lines2.append("")
    out2.write_text("\n".join(lines2), encoding="utf-8")

    print("Wrote", out1.relative_to(repo), len(lines1), "lines")
    print("Wrote", out2.relative_to(repo), len(lines2), "lines")
    print("entities", len(by_entity), "nodes", sum(len(v) for v in by_entity.values()))


if __name__ == "__main__":
    main()
