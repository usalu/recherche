#!/usr/bin/env python3
"""Create missing Tolaria type stubs for all entity types that lack one."""
import pathlib

ROOT = pathlib.Path(r'e:/recherche')

# (filename_stem, sidebar_label, icon, color)
STUBS = [
    ("reuse_einsatz",              "Reuse-Einsatz",              "puzzle",          "green"),
    ("datenpunkt",                 "Datenpunkt",                 "bar-chart-2",     "blue"),
    ("akteur",                     "Akteur",                     "user",            "purple"),
    ("akteur_beteiligung",         "Akteur-Beteiligung",         "users",           "purple"),
    ("akteurrolle",                "Akteurrolle",                "id-card",         "purple"),
    ("bauobjekt",                  "Bauobjekt",                  "building",        "orange"),
    ("bauobjektklasse",            "Bauobjektklasse",            "boxes",           "orange"),
    ("bauaufgabe_intervention",    "Bauaufgabe",                 "wrench",          "orange"),
    ("bausystem",                  "Bausystem",                  "grid-3x3",        "orange"),
    ("bauweise",                   "Bauweise",                   "ruler",           "orange"),
    ("bewertungslogik_abgrenzung", "Bewertungslogik",            "filter",          "red"),
    ("kontextmerkmal",             "Kontextmerkmal",             "tag",             "gray"),
    ("quelle",                     "Quelle",                     "book-marked",     "blue"),
    ("ressourcenquelle",           "Ressourcenquelle",           "warehouse",       "green"),
    ("reuse_einsatzstatus",        "Einsatzstatus",              "check-circle",    "green"),
    ("reuse_kette",                "Reuse-Kette",                "link-2",          "green"),
    ("reuse_kettenstation",        "Kettenstation",              "circle-dot",      "green"),
    ("tragwerksprinzip",           "Tragwerksprinzip",           "triangle",        "orange"),
]

created = 0
for stem, label, icon, color in STUBS:
    path = ROOT / f"{stem}.md"
    if path.exists():
        print(f"  SKIP (exists): {stem}.md")
        continue
    content = (
        f"---\n"
        f"type: Type\n"
        f"_sidebar_label: {label}\n"
        f"_icon: {icon}\n"
        f"color: {color}\n"
        f"---\n"
        f"# {label}\n"
    )
    path.write_text(content, encoding="utf-8")
    print(f"  CREATED: {stem}.md  [{icon}, {color}]")
    created += 1

print(f"\nCreated {created} new stubs.")
