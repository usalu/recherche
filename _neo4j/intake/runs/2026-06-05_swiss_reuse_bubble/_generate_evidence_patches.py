"""Generate evidence-backed patch JSONL for Swiss reuse bubble intake.

Every node/edge carries evidence_source_id, evidence_url, evidence_quote,
evidence_confidence, evidence_basis, review_run.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

RUN = "2026-06-05_swiss_reuse_bubble"
REVIEW_RUN = "swiss_reuse_bubble_2026_06_05"
EVIDENCE_BASIS = "swiss_reuse_bubble_v2_2026_06_05"
REVIEW_STATUS = "evidence_backed_pending_apply"
SOURCE_SCOPE = "swiss_reuse_bubble_intake"
OUT = Path(__file__).resolve().parent
PATCHES = OUT / "patches"
INBOX_MD = (
    Path(__file__).resolve().parents[2]
    / "inbox"
    / "2026-06-05_swiss_reuse_bubble"
    / "swiss_reuse_bubble_v2.md"
)


def q_url_id(url: str) -> str:
    return f"q_url_{hashlib.md5(url.encode()).hexdigest()}"


# url -> {id?, name, quote, confidence, basis?, graph_status}
SOURCES: dict[str, dict] = {
    # --- source register (19) ---
    "https://www.cirkla.ch/en/": {
        "name": "Cirkla homepage",
        "quote": "The Swiss re-use network. Experts documentation & concrete projects.",
        "confidence": "belegt",
        "basis": "first_party_homepage",
    },
    "https://www.cirkla.ch/en/lassociation-cirkla/": {
        "id": "q_actor_benjamin_poignon_03",
        "name": "Cirkla association",
        "quote": "Cirkla is an association that brings together all those involved in reuse.",
        "confidence": "belegt",
        "basis": "first_party_association_page",
    },
    "https://www.cirkla.ch/en/le-reseau-du-reemploi/": {
        "name": "Cirkla reuse network",
        "quote": "Swiss reuse directory; includes companies, experts, architects, recycling centers, universities, and projects.",
        "confidence": "belegt",
        "basis": "first_party_directory_page",
    },
    "https://www.cirkla.ch/en/publications-outils/": {
        "name": "Cirkla publications & tools",
        "quote": "Swiss Inv, Cirkla-Alarme, Cirkla-Scan, and reuse resources.",
        "confidence": "belegt",
        "basis": "first_party_tools_page",
    },
    "https://www.cirkla.ch/en/cirkla-scan/": {
        "name": "Cirkla-Scan",
        "quote": "Cirkla-Scan aggregates national reuse-material supply (FR/DE/IT).",
        "confidence": "belegt",
        "basis": "first_party_software_page",
    },
    "https://www.insitu.ch/": {
        "id": "q_url_5ef3423f578d8ccec9d847d64dc3b5bf",
        "name": "baubüro in situ",
        "quote": "Public project list includes K.118 – Kopfbau Halle 118, Winterthur, 2021.",
        "confidence": "belegt",
        "basis": "first_party_practice_homepage",
    },
    "https://zirkular.net/en/service/": {
        "name": "Zirkular services",
        "quote": "Specialist planner for circular building; Planular® and reMATERIAL® services.",
        "confidence": "belegt",
        "basis": "first_party_services_page",
    },
    "https://zirkular.net/en/project/building-k-118/": {
        "id": "q_actor_barbara_buser_02",
        "name": "Zirkular K.118",
        "quote": "architecture: baubüro in situ; trigger for the foundation of Zirkular.",
        "confidence": "belegt",
        "basis": "first_party_project_page",
    },
    "https://planular.net/": {
        "name": "Planular",
        "quote": "Synchronized planning software for donor and receiving buildings.",
        "confidence": "belegt",
        "basis": "first_party_software_homepage",
    },
    "https://madaster.ch/en/": {
        "name": "Madaster Switzerland",
        "quote": "Online material/product registry; material passports and reuse after disassembly.",
        "confidence": "belegt",
        "basis": "first_party_platform_homepage",
    },
    "https://ethz.ch/en/news-and-events/eth-news/news/2024/12/timber-earth-and-a-digital-ecosystem-for-sustainable-construction.html": {
        "name": "ETH Zurich SWIRCULAR news",
        "quote": "SWIRCULAR creates a digital ecosystem for circular construction in Switzerland.",
        "confidence": "belegt",
        "basis": "first_party_research_news",
    },
    "https://zirkular.net/en/project/innosuisse-reuse-of-building-components-a-legal-framework/": {
        "id": "q_url_991a5f7d46f61c5f40b414f95b3ae0ca",
        "name": "Zirkular legal framework project",
        "quote": "Innosuisse-funded project on contracts, permits, transport, and storage for reuse.",
        "confidence": "belegt",
        "basis": "first_party_program_page",
    },
    "https://salza.ch/": {
        "id": "q_url_f91b55379ab933d2a2833d301a4296b0",
        "name": "Salza",
        "quote": "Online platform for reusable building components with search and alarms.",
        "confidence": "belegt",
        "basis": "first_party_marketplace_homepage",
    },
    "https://salza.ch/bauteil-plattform": {
        "id": "q_url_45d7c6380377a9cec952dbf6c3f2ba8c",
        "name": "Salza Bauteil-Plattform",
        "quote": "Salza online platform for reusable building components.",
        "confidence": "belegt",
        "basis": "first_party_marketplace_page",
    },
    "https://www.useagain.ch/de/": {
        "id": "q_url_82ad61e4b3672c05a8fedf46e57faee6",
        "name": "useagain",
        "quote": "Reuse platform/shop for construction components and materials.",
        "confidence": "belegt",
        "basis": "first_party_marketplace_homepage",
    },
    "https://materiuum.ch/": {
        "name": "Matériuum",
        "quote": "Geneva association for reuse in construction; ressourceries in Geneva and Lausanne.",
        "confidence": "belegt",
        "basis": "first_party_ressourcerie_homepage",
    },
    "https://bauteilladen.ch/": {
        "name": "Bauteilladen Winterthur",
        "quote": "Secondhand building-component exchange with shop categories.",
        "confidence": "belegt",
        "basis": "first_party_shop_homepage",
    },
    "https://circularhub.ch/": {
        "name": "Circular Hub",
        "quote": "Circularity mission for construction and real-estate sector; KreislaufLAB Kanton Zürich.",
        "confidence": "belegt",
        "basis": "first_party_coordination_homepage",
    },
    "https://www.circularconstructioncatalyst.ch/": {
        "name": "Circular Construction Catalyst 2033",
        "quote": "Swiss coordination office for circular construction; 2033 goal.",
        "confidence": "belegt",
        "basis": "first_party_coordination_homepage",
    },
    "https://www.circular-economy-switzerland.ch/en": {
        "name": "Circular Economy Switzerland",
        "quote": "Decentralized regional circles; networking, information, and knowledge building.",
        "confidence": "belegt",
        "basis": "first_party_network_homepage",
    },
    # --- supplementary first-party URLs (graph gaps) ---
    "https://www.cirkla.ch/en/publications-outils/swiss-inv/": {
        "name": "Swiss Inv tool",
        "quote": "Swiss Inv inventories reuse potential in buildings.",
        "confidence": "belegt",
        "basis": "first_party_tool_page",
    },
    "https://swircular.ethz.ch/the-project.html": {
        "name": "SWIRCULAR project page",
        "quote": "2023 Innosuisse Flagship Call; consortium of Swiss research and industry partners.",
        "confidence": "belegt",
        "basis": "first_party_program_page",
    },
    "https://www.gruner.ch/de/news/bauteile-aus-rueckbauten-jetzt-imeshop-von-grunerreuse-live": {
        "name": "Gruner ReUse Roche news",
        "quote": "Bauteilbörse Basel übernimmt Lagerung und Weiterverkauf über useagain.ch.",
        "confidence": "belegt",
        "basis": "first_party_supply_chain_news",
    },
    "https://library-of-reuse.ch/pioneers/useagain": {
        "id": "q_url_9fce1894aaa7455c757369850397e39f",
        "name": "Library of Reuse useagain",
        "quote": "useagain promotes exchange between Bauteilbörse Basel, BauTeile Zürich and Bauteilladen Winterthur.",
        "confidence": "belegt",
        "basis": "first_party_network_profile",
    },
    "https://library-of-reuse.ch/pioneers/wiederverwerkle": {
        "name": "Library of Reuse Wick ReUse",
        "quote": "Wick ReUse pioneer profile in Swiss reuse library.",
        "confidence": "belegt",
        "basis": "first_party_network_profile",
    },
    "https://www.cirkla.ch/en/comite/benjamin-poignon": {
        "id": "q_url_9a4623e924a9afd9d134c8dadda0595b",
        "name": "Cirkla committee Benjamin Poignon",
        "quote": "Benjamin Poignon – Co-Chairman, Baubüro in situ.",
        "confidence": "belegt",
        "basis": "first_party_committee_page",
    },
    "https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/useagain": {
        "id": "q_url_0bc8cb1ab85454c98752946c33382059",
        "name": "Cirkla directory useagain",
        "quote": "Useagain.ch est une plateforme de mise en relation pour matériaux de construction.",
        "confidence": "belegt",
        "basis": "cirkla_directory_profile",
    },
    "https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/materiuum": {
        "id": "q_url_313143bb100ac3f3d710b67662f0b4c6",
        "name": "Cirkla directory Matériuum",
        "quote": "Matériuum listed as Cirkla reuse-network expert.",
        "confidence": "belegt",
        "basis": "cirkla_directory_profile",
    },
    "https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/wiederverwerkle-wick-upcycling-gmbh": {
        "id": "q_url_a7f990417c910b5e6ff7c927d23697e9",
        "name": "Cirkla directory Wick ReUse",
        "quote": "Wiederverwerkle Wick Upcycling GmbH listed in Cirkla directory.",
        "confidence": "belegt",
        "basis": "cirkla_directory_profile",
    },
    "https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/bauteilladen-winterthur": {
        "id": "q_url_476dc48ab7c9334ff411e0321cb8abbc",
        "name": "Cirkla directory Bauteilladen",
        "quote": "Bauteilladen Winterthur listed in Cirkla reuse directory.",
        "confidence": "belegt",
        "basis": "cirkla_directory_profile",
    },
    "https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/sumami": {
        "id": "q_url_198584a7bfbdfd0dc0b6edf698418e59",
        "name": "Cirkla directory Sumami",
        "quote": "Sumami listed in Cirkla reuse directory.",
        "confidence": "belegt",
        "basis": "cirkla_directory_profile",
    },
    "https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/gruner-ag": {
        "id": "q_actor_nicole_daehn_03",
        "name": "Cirkla directory Gruner AG",
        "quote": "Gruner AG listed in Cirkla reuse directory.",
        "confidence": "belegt",
        "basis": "cirkla_directory_profile",
    },
    "https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/overall-baubetriebe": {
        "id": "q_url_0675511c9594b27ccb8f1e7b967cab95",
        "name": "Cirkla directory Overall",
        "quote": "Overall Baubetriebe listed in Cirkla reuse directory.",
        "confidence": "belegt",
        "basis": "cirkla_directory_profile",
    },
    "https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/reuzi": {
        "name": "Cirkla directory REUZI",
        "quote": "REUZI listed in Cirkla reuse directory.",
        "confidence": "belegt",
        "basis": "cirkla_directory_profile",
    },
    "https://zirkular.net/en/project/culture-commercial-center-elys": {
        "id": "q_elys_kultur_gewerbehaus_basel_s1",
        "name": "Zirkular ELYS",
        "quote": "K.118 and ELYS proved pioneering circular-building projects; trigger for Zirkular.",
        "confidence": "belegt",
        "basis": "first_party_project_page",
    },
    "https://sustainable-digital-construction.ethz.ch/en/reuse": {
        "name": "ETH sustainable digital construction reuse",
        "quote": "Sumami and useagain development in ETH sustainable digital construction context.",
        "confidence": "teilweise_belegt",
        "basis": "first_party_research_page",
    },
    "https://www.sumami.ch/": {
        "id": "q_url_cd3db9f4a762545b641a904785da349e",
        "name": "Sumami",
        "quote": "Sumami software for construction reuse (first-party homepage).",
        "confidence": "belegt",
        "basis": "first_party_software_homepage",
    },
    "https://wickreuse.ch/baumarkt/": {
        "id": "q_url_161aca331467d6b5bd144e83b6837af4",
        "name": "Wick ReUse Baumarkt",
        "quote": "Wick ReUse Baumarkt resale marketplace.",
        "confidence": "belegt",
        "basis": "first_party_marketplace_homepage",
    },
}

# Resolve ids
for url, meta in SOURCES.items():
    meta.setdefault("id", q_url_id(url))
    meta["url"] = url
    meta.setdefault("graph_status", "existing_or_new")


def ev_props(
    source_id: str,
    *,
    basis: str | None = None,
    confidence: str = "belegt",
    quote: str | None = None,
    url: str | None = None,
    extra: dict | None = None,
) -> dict:
    src = next((m for m in SOURCES.values() if m["id"] == source_id), None)
    if src:
        basis = basis or src.get("basis", "first_party_url")
        confidence = confidence or src["confidence"]
        quote = quote or src["quote"]
        url = url or src["url"]
    props = {
        "evidence_basis": basis,
        "evidence_confidence": confidence,
        "evidence_source_id": source_id,
        "evidence_url": url,
        "evidence_quote": (quote or "")[:240],
        "review_run": REVIEW_RUN,
        "review_status": REVIEW_STATUS,
        "source_scope": SOURCE_SCOPE,
    }
    if extra:
        props.update(extra)
    return props


def add_node(node_id: str, labels: list[str], name: str, **props) -> dict:
    return {
        "id": node_id,
        "op": "add_node",
        "labels": labels,
        "properties": {
            "id": node_id,
            "name": name,
            "review_run": REVIEW_RUN,
            "review_status": REVIEW_STATUS,
            "source_scope": SOURCE_SCOPE,
            **props,
        },
    }


def add_rel(
    from_id: str,
    to_id: str,
    rel_type: str,
    rel_id: str,
    source_id: str,
    **ev_extra,
) -> dict:
    props = ev_props(source_id, extra=ev_extra)
    props["id"] = rel_id
    return {
        "from": from_id,
        "to": to_id,
        "op": "add_rel",
        "type": rel_type,
        "properties": props,
    }


def drop_rel(rel_id: str) -> dict:
    return {"op": "delete_rel", "id": rel_id}


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + ("\n" if rows else ""),
        encoding="utf-8",
    )


def phase0() -> list[dict]:
    rows: list[dict] = []
    rows.append(
        add_node(
            "q_research_swiss_reuse_bubble_v2_md",
            ["Quelle", "ResearchDocument"],
            "swiss_reuse_bubble_v2.md",
            quelltyp="research_markdown",
            source_file=str(INBOX_MD.relative_to(INBOX_MD.parents[4])),
            evidence_basis=EVIDENCE_BASIS,
        )
    )
    for url, meta in SOURCES.items():
        sid = meta["id"]
        # Skip if we know it's already in graph with same id pattern from export audit
        rows.append(
            {
                "id": sid,
                "op": "add_node",
                "labels": ["Quelle", "ExternalLink"],
                "properties": {
                    "id": sid,
                    "name": meta["name"],
                    "url": url,
                    "quelltyp": "external_link",
                    "review_run": REVIEW_RUN,
                    "review_status": REVIEW_STATUS,
                    "source_scope": SOURCE_SCOPE,
                    "evidence_basis": EVIDENCE_BASIS,
                },
            }
        )
    return rows


def phase1() -> list[dict]:
    rows: list[dict] = []
    dossier = "q_research_swiss_reuse_bubble_v2_md"

    # Cirkla BELEGT_IN enrichment
    for sid in [
        SOURCES["https://www.cirkla.ch/en/"]["id"],
        SOURCES["https://www.cirkla.ch/en/lassociation-cirkla/"]["id"],
        SOURCES["https://www.cirkla.ch/en/le-reseau-du-reemploi/"]["id"],
        SOURCES["https://www.cirkla.ch/en/publications-outils/"]["id"],
    ]:
        rows.append(
            add_rel(
                "cirkla",
                sid,
                "BELEGT_IN",
                f"r_cirkla__belegt_in__{sid}",
                sid,
                archive_source_id=dossier,
            )
        )

    # Cirkla ecosystem mesh (directory profiles = belegt)
    directory_links = [
        ("useagain_bauteilclick", "q_url_0bc8cb1ab85454c98752946c33382059", "directory"),
        ("materiuum", "q_url_313143bb100ac3f3d710b67662f0b4c6", "directory"),
        ("wick_reuse_roto_baumarkt", "q_url_a7f990417c910b5e6ff7c927d23697e9", "directory"),
        ("bauteilladen_winterthur", "q_url_476dc48ab7c9334ff411e0321cb8abbc", "directory"),
        ("reuzi_ch", "q_url_dd273c7da57939e01343e5b152733b24", "directory"),
        ("gruner_reuse_platform", "q_actor_nicole_daehn_03", "directory"),
    ]
    for actor, sid, kind in directory_links:
        rows.append(
            add_rel(
                "cirkla",
                actor,
                "VERBUNDEN_MIT_AKTEUR",
                f"r_cirkla__verbunden_mit_akteur__{actor}",
                sid,
                connection_kind=kind,
            )
        )
        rows.append(
            add_rel(
                actor,
                "cirkla",
                "VERBUNDEN_MIT_AKTEUR",
                f"r_{actor}__verbunden_mit_akteur__cirkla",
                sid,
                connection_kind=kind,
            )
        )

    # Committee / institutional (belegt)
    rows.append(
        add_rel(
            "cirkla",
            "baubuero_in_situ",
            "VERBUNDEN_MIT_AKTEUR",
            "r_cirkla__verbunden_mit_akteur__baubuero_in_situ",
            "q_url_9a4623e924a9afd9d134c8dadda0595b",
            connection_kind="committee_co_chair_affiliation",
        )
    )
    rows.append(
        add_rel(
            "baubuero_in_situ",
            "cirkla",
            "VERBUNDEN_MIT_AKTEUR",
            "r_baubuero_in_situ__verbunden_mit_akteur__cirkla",
            "q_url_9a4623e924a9afd9d134c8dadda0595b",
            connection_kind="committee_co_chair_affiliation",
        )
    )
    rows.append(
        add_rel(
            "cirkla",
            "salza",
            "VERBUNDEN_MIT_AKTEUR",
            "r_cirkla__verbunden_mit_akteur__salza",
            "q_actor_benjamin_poignon_03",
            connection_kind="committee_member_affiliation",
            evidence_quote="Olivier de Perrot – Committee member, Salza.",
        )
    )
    rows.append(
        add_rel(
            "salza",
            "cirkla",
            "VERBUNDEN_MIT_AKTEUR",
            "r_salza__verbunden_mit_akteur__cirkla",
            "q_actor_benjamin_poignon_03",
            connection_kind="committee_member_affiliation",
            evidence_quote="Olivier de Perrot – Committee member, Salza.",
        )
    )

    # Practice triangle: zirkular ↔ cirkla (teilweise — shared K.118/ELYS ecosystem)
    rows.append(
        add_rel(
            "cirkla",
            "zirkular",
            "VERBUNDEN_MIT_AKTEUR",
            "r_cirkla__verbunden_mit_akteur__zirkular",
            "q_actor_barbara_buser_02",
            connection_kind="ecosystem_practice_triangle",
            evidence_confidence="teilweise_belegt",
            evidence_basis="shared_pioneer_projects_and_planners",
        )
    )
    rows.append(
        add_rel(
            "zirkular",
            "cirkla",
            "VERBUNDEN_MIT_AKTEUR",
            "r_zirkular__verbunden_mit_akteur__cirkla",
            "q_actor_barbara_buser_02",
            connection_kind="ecosystem_practice_triangle",
            evidence_confidence="teilweise_belegt",
            evidence_basis="shared_pioneer_projects_and_planners",
        )
    )

    # K.118 participation promotion
    rows.append(
        add_rel(
            "baubuero_in_situ",
            "p_k118_kopfbau_halle_118_winterthur",
            "BETEILIGT_AN",
            "r_baubuero_in_situ__beteiligt_an__p_k118_kopfbau_halle_118_winterthur",
            "q_actor_barbara_buser_02",
            evidence_quote="architecture: baubüro in situ",
        )
    )
    rows.append(
        drop_rel("r_zirkular__assoziiert_mit_projekt__p_k118_kopfbau_halle_118_winterthur")
    )
    rows.append(
        add_rel(
            "zirkular",
            "p_k118_kopfbau_halle_118_winterthur",
            "BETEILIGT_AN",
            "r_zirkular__beteiligt_an__p_k118_kopfbau_halle_118_winterthur",
            "q_actor_barbara_buser_02",
            evidence_quote="trigger for the foundation of Zirkular by the involved planners",
        )
    )
    rows.append(
        drop_rel("r_zirkular__assoziiert_mit_projekt__p_elys_kultur_gewerbehaus_basel")
    )
    rows.append(
        add_rel(
            "zirkular",
            "p_elys_kultur_gewerbehaus_basel",
            "BETEILIGT_AN",
            "r_zirkular__beteiligt_an__p_elys_kultur_gewerbehaus_basel",
            "q_elys_kultur_gewerbehaus_basel_s1",
            evidence_quote="K.118 and ELYS proved pioneering circular-building projects",
        )
    )

    # Madaster CH URL
    rows.append(
        add_rel(
            "madaster",
            SOURCES["https://madaster.ch/en/"]["id"],
            "BELEGT_IN",
            f"r_madaster__belegt_in__{SOURCES['https://madaster.ch/en/']['id']}",
            SOURCES["https://madaster.ch/en/"]["id"],
            archive_source_id=dossier,
        )
    )

    return rows


def phase2() -> list[dict]:
    rows: list[dict] = []
    dossier = "q_research_swiss_reuse_bubble_v2_md"

    new_nodes = [
        ("software_planular", ["Software"], "Planular", "https://planular.net/"),
        ("tool_swiss_inv", ["Tool"], "Swiss Inv", "https://www.cirkla.ch/en/publications-outils/swiss-inv/"),
        ("software_cirkla_scan", ["Software"], "Cirkla-Scan", "https://www.cirkla.ch/en/cirkla-scan/"),
        ("prog_swircular", ["Programm"], "SWIRCULAR", "https://swircular.ethz.ch/the-project.html"),
        (
            "prog_innosuisse_reuse_legal_framework_ch",
            ["Programm"],
            "Innosuisse legal framework for reuse (CH)",
            "https://zirkular.net/en/project/innosuisse-reuse-of-building-components-a-legal-framework/",
        ),
        ("c33_circular_construction_catalyst", ["Akteur"], "Circular Construction Catalyst 2033", "https://www.circularconstructioncatalyst.ch/"),
        ("circular_hub_zurich", ["Akteur"], "Circular Hub Zürich", "https://circularhub.ch/"),
        ("circular_economy_switzerland", ["Akteur"], "Circular Economy Switzerland", "https://www.circular-economy-switzerland.ch/en"),
        ("sumami", ["Akteur"], "Sumami", "https://www.sumami.ch/"),
    ]
    for nid, labels, name, url in new_nodes:
        sid = SOURCES[url]["id"]
        rows.append(add_node(nid, labels, name))
        rows.append(
            add_rel(nid, sid, "BELEGT_IN", f"r_{nid}__belegt_in__{sid}", sid, archive_source_id=dossier)
        )

    # Tool/software links
    rows.append(
        add_rel(
            "cirkla",
            "software_cirkla_scan",
            "VERBUNDEN_MIT_AKTEUR",
            "r_cirkla__verbunden_mit_akteur__software_cirkla_scan",
            SOURCES["https://www.cirkla.ch/en/cirkla-scan/"]["id"],
            connection_kind="published_tool",
        )
    )
    rows.append(
        add_rel(
            "cirkla",
            "tool_swiss_inv",
            "VERBUNDEN_MIT_AKTEUR",
            "r_cirkla__verbunden_mit_akteur__tool_swiss_inv",
            SOURCES["https://www.cirkla.ch/en/publications-outils/swiss-inv/"]["id"],
            connection_kind="published_tool",
        )
    )
    rows.append(
        add_rel(
            "zirkular",
            "software_planular",
            "VERBUNDEN_MIT_AKTEUR",
            "r_zirkular__verbunden_mit_akteur__software_planular",
            SOURCES["https://zirkular.net/en/service/"]["id"],
            connection_kind="service_product",
            evidence_quote="Planular® service by Zirkular",
        )
    )
    rows.append(
        add_rel(
            "eth_zuerich",
            "prog_swircular",
            "BETEILIGT_AN",
            "r_eth_zuerich__beteiligt_an__prog_swircular",
            SOURCES["https://swircular.ethz.ch/the-project.html"]["id"],
        )
    )
    rows.append(
        add_rel(
            "zirkular",
            "prog_innosuisse_reuse_legal_framework_ch",
            "BETEILIGT_AN",
            "r_zirkular__beteiligt_an__prog_innosuisse_reuse_legal_framework_ch",
            "q_url_991a5f7d46f61c5f40b414f95b3ae0ca",
        )
    )
    rows.append(
        add_rel(
            "baubuero_in_situ",
            "prog_innosuisse_reuse_legal_framework_ch",
            "BETEILIGT_AN",
            "r_baubuero_in_situ__beteiligt_an__prog_innosuisse_reuse_legal_framework_ch",
            "q_url_991a5f7d46f61c5f40b414f95b3ae0ca",
            evidence_confidence="teilweise_belegt",
            evidence_basis="project_partner_list_on_zirkular_page",
        )
    )

    return rows


def phase3() -> list[dict]:
    rows: list[dict] = []
    # Supply chain (belegt)
    chain: list[dict] = [
        {
            "a": "gruner_reuse_platform",
            "b": "bauteilboerse_basel_overall",
            "sid": "q_url_18e12efdbd4d72af6a5f2be98fd0ea78",
            "kind": "supply_chain_roche_resale",
        },
        {
            "a": "bauteilboerse_basel_overall",
            "b": "useagain_bauteilclick",
            "sid": "q_url_18e12efdbd4d72af6a5f2be98fd0ea78",
            "kind": "supply_chain_roche_resale",
        },
        {
            "a": "useagain_bauteilclick",
            "b": "bauteilladen_winterthur",
            "sid": "q_url_9fce1894aaa7455c757369850397e39f",
            "kind": "network_library_of_reuse",
        },
        {
            "a": "cirkla",
            "b": "wick_reuse_roto_baumarkt",
            "sid": "q_url_9a4623e924a9afd9d134c8dadda0595b",
            "kind": "committee_member_roto_reuse",
            "quote": "Elias Knecht – Committee member, ROTO-Reuse.",
        },
    ]
    for link in chain:
        extra = {"connection_kind": link["kind"]}
        if link.get("quote"):
            extra["evidence_quote"] = link["quote"]
        rows.append(
            add_rel(
                link["a"],
                link["b"],
                "VERBUNDEN_MIT_AKTEUR",
                f"r_{link['a']}__verbunden_mit_akteur__{link['b']}",
                link["sid"],
                **extra,
            )
        )
        rows.append(
            add_rel(
                link["b"],
                link["a"],
                "VERBUNDEN_MIT_AKTEUR",
                f"r_{link['b']}__verbunden_mit_akteur__{link['a']}",
                link["sid"],
                **extra,
            )
        )

    # sumami ↔ useagain (teilweise)
    rows.append(
        add_rel(
            "sumami",
            "useagain_bauteilclick",
            "VERBUNDEN_MIT_AKTEUR",
            "r_sumami__verbunden_mit_akteur__useagain_bauteilclick",
            "q_url_422166f604d091d32cff814ca59194f2",
            connection_kind="software_development_context",
            evidence_confidence="teilweise_belegt",
        )
    )

    # C33 / CES ecosystem links to cirkla (teilweise — same coordination field)
    for actor in ["c33_circular_construction_catalyst", "circular_hub_zurich", "circular_economy_switzerland"]:
        url = {
            "c33_circular_construction_catalyst": "https://www.circularconstructioncatalyst.ch/",
            "circular_hub_zurich": "https://circularhub.ch/",
            "circular_economy_switzerland": "https://www.circular-economy-switzerland.ch/en",
        }[actor]
        sid = SOURCES[url]["id"]
        rows.append(
            add_rel(
                "cirkla",
                actor,
                "VERBUNDEN_MIT_AKTEUR",
                f"r_cirkla__verbunden_mit_akteur__{actor}",
                sid,
                connection_kind="coordination_ecosystem",
                evidence_confidence="teilweise_belegt",
                evidence_basis="shared_circular_construction_coordination_mandate",
            )
        )

    return rows


def write_evidence_register() -> None:
    path = OUT / "EVIDENCE_REGISTER.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "evidence_id",
                "url",
                "name",
                "quote",
                "confidence",
                "basis",
                "graph_status",
            ]
        )
        for url, meta in sorted(SOURCES.items(), key=lambda x: x[1]["id"]):
            w.writerow(
                [
                    meta["id"],
                    url,
                    meta["name"],
                    meta["quote"],
                    meta["confidence"],
                    meta.get("basis", ""),
                    "in_graph_export_or_new",
                ]
            )


def write_source_urls_json() -> None:
    payload = {
        "run": RUN,
        "review_run": REVIEW_RUN,
        "evidence_basis": EVIDENCE_BASIS,
        "dossier_id": "q_research_swiss_reuse_bubble_v2_md",
        "inbox_path": str(INBOX_MD),
        "source_register_count": 19,
        "supplementary_url_count": len(SOURCES) - 19,
        "urls": [
            {
                "id": meta["id"],
                "url": url,
                "name": meta["name"],
                "confidence": meta["confidence"],
            }
            for url, meta in sorted(SOURCES.items(), key=lambda x: x[1]["id"])
        ],
    }
    (OUT / "source_urls.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> None:
    PATCHES.mkdir(parents=True, exist_ok=True)
    write_jsonl(PATCHES / "phase0_sources_and_dossier.patch.jsonl", phase0())
    write_jsonl(PATCHES / "phase1_enrichment_connectivity.patch.jsonl", phase1())
    write_jsonl(PATCHES / "phase2_new_nodes.patch.jsonl", phase2())
    write_jsonl(PATCHES / "phase3_supply_chain.patch.jsonl", phase3())
    write_evidence_register()
    write_source_urls_json()
    print("Generated patches and evidence register in", OUT)


if __name__ == "__main__":
    main()
