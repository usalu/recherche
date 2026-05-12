"""Regenerate plan §5.2 table: all labels in one table with ≤20 example ids per row from node_inventory.csv."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from akteur_org_neo4j_label import neo4j_label_for_akteur_folder
from akteur_person_split import split_akteur_ids
from ort_geo_label import neo4j_label_for_ort_id
from software_tool_label import neo4j_label_for_software_digitaltool_id

MAX_N = 20

# Organisation-actor labels (plan §6.1) — example ids from `neo4j_label_for_akteur_folder`.
ORG_ACTOR_SPECS: list[tuple[str, str, str]] = [
    (
        ":PlanungArchitekturIngenieurwesen",
        "Organisations whose `index.md` resolves to slug `planung_architektur_ingenieurwesen` (§6.1); not natural persons",
        "PlanungArchitekturIngenieurwesen",
    ),
    (
        ":ForschungLehreWissenstransfer",
        "Slug `forschung_lehre_wissenstransfer`",
        "ForschungLehreWissenstransfer",
    ),
    (
        ":OeffentlicheInstitutionenFoerderung",
        "Slug `oeffentliche_institutionen_foerderung`",
        "OeffentlicheInstitutionenFoerderung",
    ),
    (
        ":KammernVerbaendeNgosNetzwerke",
        "Slug `kammern_verbaende_ngos_netzwerke`",
        "KammernVerbaendeNgosNetzwerke",
    ),
    (
        ":UnternehmerverbandHistorischeBaustoffeUHBMd",
        "Slug `Unternehmerverband_Historische_Baustoffe_UHB_md` (§6.1)",
        "UnternehmerverbandHistorischeBaustoffeUHBMd",
    ),
    (
        ":MaterialinitiativenHubs",
        "Slug `materialinitiativen_hubs`",
        "MaterialinitiativenHubs",
    ),
    (
        ":ReuseBeratungProzessdienstleister",
        "Slug `reuse_beratung_prozessdienstleister`",
        "ReuseBeratungProzessdienstleister",
    ),
    (":Professur", "Slug `professur` (after optional alias pass)", "Professur"),
    (
        ":Akteur",
        "**Fallback only:** organisation in `akteur/` when **no** §6.1 slug resolves—not used for persons",
        "Akteur",
    ),
]

# (Neo4j label, inventory entity slugs, notes, kind[, org_internal_label])
# kind: "normal" | "bauteilgruppe" | "entwurf" | "revers" | "land" | "stadt" | "software" | "tool"
#       | "org_actor" | "person"
LABEL_BLOCKS: list[tuple] = [
    *[(lab, ["akteur"], note, "org_actor", internal) for lab, note, internal in ORG_ACTOR_SPECS],
    (
        ":Akteurrolle",
        ["akteurrolle"],
        "Twenty-one legacy folders → eight canonical `id`s (§5.5); cells show folder names.",
        "normal",
    ),
    (":Aufbereitungsverfahren", ["aufbereitungsverfahren"], "", "normal"),
    (":BauaufgabeIntervention", ["bauaufgabe_intervention"], "", "normal"),
    (":Bauteilebene", ["bauteilebene"], "", "normal"),
    (
        ":Bauteilgruppe",
        [],
        "Physical component group **and** reuse-episode anchor: `reuse_einsatz/` (canonical), optional `bauteilgruppe/`; mass + reuse KPIs (e.g. CO₂) on the same node (§5.8). **Individual `id` (folder slug) is *bauteil-centric*: the readable tail names the Bauteil / Baugruppe / homogenes Los; a leading `{fall}__{nnn}__` segment is only for uniqueness and traceability—full case or supplier narrative stays in Markdown / edges, not in the tail.** Examples = current inventory (may still carry legacy narrative tails).",
        "bauteilgruppe",
    ),
    (":Bauteiltyp", ["bauteiltyp"], "", "normal"),
    (":Bauteilzustand", ["bauteilzustand"], "", "normal"),
    (
        ":Bauwerk",
        ["bauobjekt"],
        "Physical built work + building-level measurements; `GEHÖRT_ZU { rolle: 'fallbeispiel' }` → `:Fallbeispiel`",
        "normal",
    ),
    (":Bauweise", ["bauweise"], "", "normal"),
    (":Bausystem", ["bausystem"], "", "normal"),
    (":Beschaffungsweg", ["beschaffungsweg"], "", "normal"),
    (":Datenqualitaet", ["datenqualitaet"], "", "normal"),
    (
        ":Entwurfsentscheidung",
        [],
        "Curated (no folder); `HAT { art: 'entwurf' }` from `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`",
        "entwurf",
    ),
    (
        ":Fallbeispiel",
        ["fallstudie", "projekt"],
        "Case / project **record** (not the physical asset); merged on matching ids",
        "normal",
    ),
    (":Funktionswechsel", ["funktionswechsel"], "", "normal"),
    (":Huerde", ["huerde"], "General hurdles; not chemical substance nodes", "normal"),
    (
        ":Land",
        ["ort"],
        "`ort/` rows classified as country / macro-region → `:Land` (`ort_geo_label.py`, §5.1a)",
        "land",
    ),
    (":Leistungsanforderung", ["leistungsanforderung"], "", "normal"),
    (":Logistik", ["logistik"], "", "normal"),
    (":Material", ["material"], "", "normal"),
    (
        ":Methode",
        ["methode"],
        "Includes `methode/Reversibilitaet/` — distinct from `:Reversibilitaet` label",
        "normal",
    ),
    (":Norm", ["norm"], "", "normal"),
    (":Nutzung", ["nutzung"], "", "normal"),
    (
        ":Person",
        ["person", "akteur"],
        "`person/` when present; plus classified `akteur/<id>/`; label from `legacy_type: Person` or `akteurtyp/Person` in `index.md` (no separate `akteurtyp` property—`:Person` is the discriminator)",
        "person",
    ),
    (
        ":Programm",
        ["foerderprogramm", "programm_kontext", "kontextmerkmal"],
        "`programm_typ`: `foerderung` | `forschungskontext`; `Pilotprojekt` merges with `kontextmerkmal/`",
        "normal",
    ),
    (":Prozessphase", ["prozessphase"], "", "normal"),
    (":PruefungNachweis", ["pruefung_nachweis"], "", "normal"),
    (":Quelle", ["quelle"], "Citation target", "normal"),
    (
        ":RechtlicheBedingung",
        ["rechtliche_bedingung"],
        "Single node for `Gewaehrleistung`; no duplicate under `:Huerde`",
        "normal",
    ),
    (":Ressourcenquelle", ["ressourcenquelle"], "", "normal"),
    (
        ":Reversibilitaet",
        [],
        "Four fixed nodes; `HAT { art: 'reversibilitaet' }` only; no `fuegung_verbindung/` provenance",
        "revers",
    ),
    (":Rueckbauverfahren", ["rueckbauverfahren"], "", "normal"),
    (":Schadstoff", ["schadstoff"], "Stammdaten per substance folder; `HAT { art: \"schadstoff\" }`", "normal"),
    (
        ":Software",
        ["software_digitaltool"],
        "First 20 slugs from `software_digitaltool/` (α) — **illustration**; export assigns `:Software` vs `:Tool` (§5.6)",
        "software",
    ),
    (
        ":Stadt",
        ["ort"],
        "`ort/` rows not classified as `:Land` → `:Stadt` (`ort_geo_label.py`)",
        "stadt",
    ),
    (
        ":Status",
        ["reuse_einsatzstatus", "bauobjektstatus"],
        "Seven canonical `id`s after export; examples are legacy folder names",
        "normal",
    ),
    (
        ":Tool",
        ["software_digitaltool"],
        "Slugs 21–40 from `software_digitaltool/` (α) — **illustration** only (§5.6)",
        "tool",
    ),
    (":Tragwerksprinzip", ["tragwerksprinzip"], "", "normal"),
    (
        ":Verbindungstechnik",
        ["fuegung_verbindung"],
        "Six technique folders only (§5.10); `Reversible_Fuegung/` excluded from examples",
        "normal",
    ),
    (
        ":WiederverwendungsArt",
        ["bewertungslogik_abgrenzung", "reuse_strategie"],
        "`axis`: `einordnung` | `grundtyp` | `reuse_strategie`; strategy: Appendix E",
        "normal",
    ),
    (
        ":Wiederverwendungskette",
        ["reuse_kette"],
        "Optional named chain; `reuse_kettenstation/` → `GEHÖRT_ZU` edges, not nodes",
        "normal",
    ),
    (":Wirtschaft", ["wirtschaft"], "", "normal"),
    (":ZertifizierungBewertungssystem", ["zertifizierung_bewertungssystem"], "", "normal"),
]

CURATED_ENTWURF = [
    "Etagenhoehe_durch_Bauteilmass",
    "Fassadenschicht_als_Toleranzpuffer",
    "Doppelfenster_als_Kastenfenster",
    "Achsraster_nach_Bestand",
    "Grundriss_nach_Bauteillaenge",
    "Deckenhoehe_nach_Traegerhoehe",
    "Anschlussdetail_angepasst",
    "Erschliessungskern_verschoben",
]

REVERS_IDS = ["Reversibel", "Teilweise_reversibel", "Irreversibel", "Unbekannt"]


def collect_ids(by_entity: dict[str, list[str]], entities: list[str]) -> list[str]:
    out: list[str] = []
    for e in entities:
        out.extend(by_entity.get(e, []))
    return sorted(set(out))


def examples_cell(ids: list[str], max_n: int = MAX_N) -> str:
    take = ids[:max_n]
    if not take:
        return "—"
    return ", ".join(take)


def folder_cell(ents: list[str], kind: str) -> str:
    if kind == "bauteilgruppe":
        return "`bauteilgruppe/` (optional), `reuse_einsatz/`, inventory"
    if kind == "entwurf":
        return "_(curated)_"
    if kind == "person":
        return "`person/` (optional); `akteur/` (subset — see Notes)"
    if kind == "org_actor":
        return "`akteur/`"
    if not ents:
        return "—"
    return ", ".join(f"`{e}/`" for e in ents)


def escape_cell(s: str) -> str:
    return s.replace("\n", " ").replace("|", "\\|")


def build_section(by_entity: dict[str, list[str]], repo: Path) -> str:
    lines: list[str] = []
    lines.append("### 5.2 All node labels (52)")
    lines.append("")
    lines.append(
        "Every label is a **primary** node type: one Neo4j `:Label`, `UNIQUE` on `id`, same authoring rules. "
        "There is **no** `:Tooltyp` label (`tooltyp/` → properties on `:Tool` / `:Software`, §5.4)."
    )
    lines.append("")
    lines.append(
        f"The **Examples** column lists up to **{MAX_N}** instance `id` values from "
        "`_database/_system/node_inventory.csv` (sorted, unique per label) where applicable; "
        "`akteur/` rows split into **`:Person`** vs **organisation-actor labels** using `index.md` heuristics "
        "and the slug→label map (§6.1). Regenerate: `python _scripts/generate_plan_section_5_2.py` "
        "(generator emits one §5.2 row per organisation-actor label and per-label examples)."
    )
    lines.append("")
    lines.append("| Label | Folder(s) / provenance | Notes | Examples (≤20 `id`s) |")
    lines.append("| --- | --- | --- | --- |")

    ort_all = sorted(by_entity.get("ort", []))
    land_ids = sorted(oid for oid in ort_all if neo4j_label_for_ort_id(oid) == "Land")
    stadt_ids = sorted(oid for oid in ort_all if neo4j_label_for_ort_id(oid) == "Stadt")
    sd_all = sorted(by_entity.get("software_digitaltool", []))
    sd_soft = sorted(s for s in sd_all if neo4j_label_for_software_digitaltool_id(s) == "Software")
    sd_tool = sorted(s for s in sd_all if neo4j_label_for_software_digitaltool_id(s) == "Tool")
    akteur_all = sorted(by_entity.get("akteur", []))
    person_ids, _org_ids = split_akteur_ids(repo / "_database", akteur_all)

    for block in LABEL_BLOCKS:
        if len(block) == 5:
            label, ents, note, kind, org_internal = block
        else:
            label, ents, note, kind = block
            org_internal = None
        fcell = folder_cell(ents, kind)
        if kind == "normal":
            ids = collect_ids(by_entity, ents)
            if label == ":Verbindungstechnik":
                ids = [i for i in ids if i != "Reversible_Fuegung"]
            ex = examples_cell(ids)
        elif kind == "bauteilgruppe":
            ex = examples_cell(collect_ids(by_entity, ["reuse_einsatz", "bauteilgruppe"]))
        elif kind == "entwurf":
            ex = examples_cell(CURATED_ENTWURF)
        elif kind == "revers":
            ex = examples_cell(REVERS_IDS)
        elif kind == "land":
            ex = examples_cell(land_ids[:MAX_N])
        elif kind == "stadt":
            ex = examples_cell(stadt_ids[:MAX_N])
        elif kind == "software":
            ex = examples_cell(sd_soft[:MAX_N])
        elif kind == "tool":
            ex = examples_cell(sd_tool[:MAX_N])
        elif kind == "org_actor":
            db = repo / "_database"
            ex = examples_cell(
                sorted(
                    aid
                    for aid in akteur_all
                    if neo4j_label_for_akteur_folder(db, aid) == org_internal
                )
            )
        elif kind == "person":
            merged = sorted(set(by_entity.get("person", [])) | set(person_ids))
            ex = examples_cell(merged)
        else:
            raise ValueError(f"unknown kind {kind!r}")

        row = (
            f"| `{label}` | {escape_cell(fcell)} | {escape_cell(note)} | {escape_cell(ex)} |"
        )
        lines.append(row)

    return "\n".join(lines)


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    inv = repo / "_database" / "_system" / "node_inventory.csv"
    plan = repo / ".cursor" / "plans" / "neo4j_schema_catalogue_3bc01035.plan.md"

    by_entity: dict[str, list[str]] = defaultdict(list)
    with inv.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            by_entity[row["entity"]].append(row["id"])
    for k in by_entity:
        by_entity[k].sort()

    section = build_section(by_entity, repo)
    text = plan.read_text(encoding="utf-8")
    start = text.index("### 5.2 All node labels")
    end = text.index("### 5.4", start)
    new_text = text[:start] + section + "\n" + text[end:]
    plan.write_text(new_text, encoding="utf-8")
    print("Patched", plan.relative_to(repo), "§5.2 length", len(section))


if __name__ == "__main__":
    main()
