from __future__ import annotations

import csv
import re
import shutil
import unicodedata
from dataclasses import dataclass
from pathlib import Path


IMAGES_ROOT = Path(r"e:\recherche\_neo4j\review\2026-05-31_project_direct_topology_export_mit-bestand\images")
REGISTER_FILE = IMAGES_ROOT / "image_research_register_67.md"
MANIFEST_FILE = IMAGES_ROOT / "MANIFEST.csv"
NOTE_FILENAME = "image_research_links.md"
GENERATED_MARKER = "<!-- generated: missing-image-research-note -->"
OUTSIDE_REGISTER_DIR = IMAGES_ROOT / "outside_register_projects"
OUTSIDE_REGISTER_WITH_IMAGES_DIR = OUTSIDE_REGISTER_DIR / "with_images"
OUTSIDE_NOTE_PREFIX = "outside_register_"
OUTSIDE_FOLDER_NOTE = "outside_register.md"
IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".avif",
    ".svg",
}

PROJECT_TO_FOLDER = {
    "K.118 / Kopfbau Halle 118": "049_p_k118_kopfbau_halle_118_winterthur",
    "BedZED (Beddington Zero Energy Development)": "005_p_bedzed_london_hackbridge",
    "BioPartner 5": "010_p_biopartner_5_leiden_oegstgeest",
    "KA13 / Kristian Augusts gate 13": "050_p_ka13_kristian_augusts_gate_13_oslo",
    "Recypark Demets / Anderlecht": "081_p_recypark_demets_anderlecht",
    "Svanen / The Swan Kindergarten": "090_p_svanen_kindergarten_gladsaxe",
    "Villa Welpeloo": "099_p_villa_welpeloo_enschede",
    "Holbein Gardens": "040_p_holbein_gardens_london",
    "Grubenstrasse 29 / Werkhof 29": "037_p_grubenstrasse_29_werkhof_29_zuerich",
    "Haus HOS": "039_p_haus_hos_mehrfamilienhaus_muehlhausen",
    "Mehrow Pilot House": "063_p_mehrow_pilot_house",
    "Broethen Twin-House": "015_p_broethen_twin_house_hoyerswerda",
    "CRCLR House / Impact Hub": "025_p_crclr_house_impact_hub_berlin",
    "Recyclinghaus Hannover": "080_p_recyclinghaus_hannover",
    "Thoravej 29": "092_p_thoravej_29_copenhagen",
    "Timber Square": "093_p_timber_square_london",
    "House of Fraser → TBC.London": "041_p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain",
    "55 Great Suffolk Street": "001_p_55_great_suffolk_street_london",
    "Brent Cross Town Substation": "013_p_brent_cross_town_primary_substation_london",
    "Boulder Fire Station 3": "012_p_boulder_fire_station_3",
    "Big Dig House": "009_p_big_dig_house_lexington_massachusetts",
    "Saxum Vineyard Equipment Barn": "086_p_saxum_vineyard_equipment_barn_paso_robles",
    "Europa Building (Résidence Palace)": "031_p_europa_building_brussels",
    "ELYS Kultur- & Gewerbehaus": "028_p_elys_kultur_gewerbehaus_basel",
    "Lycée Michel Lucius Conversion": "056_p_lycee_michel_lucius_conversion_luxembourg",
    "Jeugdkliniek Ithaka / Emergis": "046_p_jeugdkliniek_ithaka_emergis_kloetinge",
    "gjG House": "034_p_gjg_house_gentbrugge",
    "Maison DnA": "060_p_maison_dna_asse",
    "Association House, Gröditz": "002_p_association_house_groeditz",
    "Association House, Plauen": "003_p_association_house_plauen",
    "Berlin-Schildow Pilot House": "006_p_berlin_schildow_pilot_house",
    "Circular Centre NL / Prinsenhof A": "023_p_circular_centre_netherlands_prinsenhof_a_reuse_pilot",
    "Juch-Areal Recyclingzentrum": "047_p_juch_areal_recyclingzentrum_zuerich",
    "Melkinlaituri School & Day-care": "064_p_melkinlaituri_primary_school_daycare_centre_helsinki",
    "Härmälänranta / A-Kruunu ReCreate": "042_p_harmalanranta_a_kruunu_recreate_mini_pilot_tampere",
    "Lokomotion Technology Centre": "055_p_lokomotion_technology_centre_mini_pilot_tampere",
    "Grande Halle de Colombelles / Le WIP": "036_p_grande_halle_de_colombelles",
    "La Ferme du Rail": "033_p_ferme_du_rail_paris",
    "Résilience / La Ferme des Possibles": "085_p_resilience_la_ferme_des_possibles_stains",
    "Maison Vignette": "061_p_maison_vignette_auderghem",
    "MULTI Brussels": "066_p_multi_brussels_reuse_in_multi",
    "Musée de Folklore / MUSEF": "067_p_musee_de_folklore_mouscron",
    "Lo-Reninge Town Hall façade": "054_p_lo_reninge_town_hall_facade",
    "Institut de Botanique ULg": "044_p_institut_de_botanique_ulg_liege",
    "Chiro d’Itterbeek (sanitary block)": "019_p_chiro_d_itterbeek_dilbeek",
    "Verbiest + Karreveld": "098_p_verbiest_karreveld_brussels",
    "Zinneke / FEDER Masui4ever": "101_p_zinneke_feder_masui4ever_brussels",
    "Liander / Alliander HQ": "053_p_liander_alliander_hq_duiven",
    "The Green House": "091_p_the_green_house_utrecht",
    "Resource Rows": "083_p_resource_rows_copenhagen",
    "Upcycle Studios": "097_p_upcycle_studios_copenhagen",
    "TRÆ High-Rise": "094_p_trae_high_rise_aarhus",
    "Woongroep Boschgaard": "100_p_woongroep_boschgaard_den_bosch",
    "Kindergarten Mööslistrasse / Manegg": "052_p_kindergarten_moeoeslistrasse_manegg_zuerich",
    "Brighton Waste House": "014_p_brighton_waste_house_brighton",
    "Hastings Pier Visitor Centre": "038_p_hastings_pier_visitor_centre",
    "Kamikatsu Zero Waste Center / Hotel WHY": "051_p_kamikatsu_zero_waste_center_hotel_why",
    "People’s Pavilion": "070_p_peoples_pavilion_eindhoven",
    "Circular Pavilion (Pavillon Circulaire)": "024_p_circular_pavilion_paris",
    "Christ Pavilion": "020_p_christ_pavilion_volkenroda",
    "Plattenvereinigung": "072_p_plattenvereinigung_berlin",
    "Plattenpalast": "071_p_plattenpalast_berlin",
    "SUPERLOCAL Expogebouw": "089_p_superlocal_expogebouw_bleijerheide",
    "CascadeUp glulam demonstrator": "017_p_cascadeup_london_secondary_timber_glulam_demonstrator",
    "Re:Crete footbridge": "076_p_recrete_footbridge_reused_concrete_blocks",
    "Bestandverplanzung Pavilion": "007_p_bestandverplanzung_pavilion_muenchen",
    "Montessori Maassluis": "065_p_montessori_maassluis",
}


@dataclass
class RegisterEntry:
    number: int
    project: str
    location: str
    image_motif: str
    search_terms: str
    search_links: dict[str, str]
    rights_note: str
    target_filename: str


def slugify(value: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", ascii_text).strip("_")
    return slug.lower() or "project"


def parse_register() -> list[RegisterEntry]:
    lines = REGISTER_FILE.read_text(encoding="utf-8").splitlines()
    entries: list[RegisterEntry] = []

    for line in lines:
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8 or not cells[0].isdigit():
            continue

        number = int(cells[0])
        search_links = dict(re.findall(r"\[([^\]]+)\]\(([^)]+)\)", cells[5]))
        entries.append(
            RegisterEntry(
                number=number,
                project=cells[1],
                location=cells[2],
                image_motif=cells[3],
                search_terms=cells[4],
                search_links=search_links,
                rights_note=cells[6],
                target_filename=cells[7].strip("`") if cells[7] else "",
            )
        )

    return entries


def load_manifest() -> dict[str, dict[str, str]]:
    with MANIFEST_FILE.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        normalized_rows = []
        for row in reader:
            normalized_row = {key.lstrip("\ufeff").strip(): value for key, value in row.items()}
            normalized_rows.append(normalized_row)
        return {row["folder"]: row for row in normalized_rows}


def folder_has_images(folder: Path) -> bool:
    return any(path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS for path in folder.rglob("*"))


def generated_note_path(folder: Path) -> Path:
    return folder / NOTE_FILENAME


def cleanup_generated_note(folder: Path) -> bool:
    note_path = generated_note_path(folder)
    if not note_path.exists():
        return False
    content = note_path.read_text(encoding="utf-8")
    if GENERATED_MARKER not in content:
        return False
    note_path.unlink()
    return True


def build_note(entry: RegisterEntry, folder_name: str, manifest_name: str) -> str:
    lines = [
        GENERATED_MARKER,
        "# Missing Image Research Links",
        "",
        "This project folder currently has no image files. Use the links below to collect images for the repo.",
        "",
        "## Project",
        f"- Register No.: {entry.number}",
        f"- Source Project: {entry.project}",
        f"- Manifest Project: {manifest_name}",
        f"- Location: {entry.location}",
        f"- Repo Folder: {folder_name}",
        f"- Expected Filename: {entry.target_filename}",
        "",
        "## Research Brief",
        f"- Image Motif: {entry.image_motif}",
        f"- Search Terms: {entry.search_terms}",
        f"- Rights Check: {entry.rights_note}",
        "",
        "## Search Links",
    ]

    for label in ["offiziell", "Bing", "Google Bilder", "Commons"]:
        url = entry.search_links.get(label)
        if url:
            lines.append(f"- [{label}]({url})")

    remaining = [label for label in entry.search_links if label not in {"offiziell", "Bing", "Google Bilder", "Commons"}]
    for label in remaining:
        lines.append(f"- [{label}]({entry.search_links[label]})")

    lines.extend(
        [
            "",
            "## Source",
            "- Source Register: [image_research_register_67.md](../image_research_register_67.md)",
        ]
    )
    return "\n".join(lines) + "\n"


def build_unmatched_note(entry: RegisterEntry, reason: str) -> str:
    lines = [
        GENERATED_MARKER,
        "# No Corresponding Project Folder Found",
        "",
        reason,
        "",
        "## Project",
        f"- Register No.: {entry.number}",
        f"- Source Project: {entry.project}",
        f"- Location: {entry.location}",
        f"- Expected Filename: {entry.target_filename}",
        "",
        "## Research Brief",
        f"- Image Motif: {entry.image_motif}",
        f"- Search Terms: {entry.search_terms}",
        f"- Rights Check: {entry.rights_note}",
        "",
        "## Search Links",
    ]

    for label, url in entry.search_links.items():
        lines.append(f"- [{label}]({url})")

    lines.extend(
        [
            "",
            "## Source",
            "- Source Register: [image_research_register_67.md](image_research_register_67.md)",
        ]
    )
    return "\n".join(lines) + "\n"


def write_unmatched_note(entry: RegisterEntry, reason: str) -> None:
    note_name = f"unmatched_{entry.number:02d}_{slugify(entry.project)}.md"
    note_path = IMAGES_ROOT / note_name
    note_path.write_text(build_unmatched_note(entry, reason), encoding="utf-8")


def cleanup_outside_register_dir() -> int:
    removed = 0
    if not OUTSIDE_REGISTER_DIR.exists():
        return removed

    for path in OUTSIDE_REGISTER_DIR.glob("*.md"):
        content = path.read_text(encoding="utf-8")
        if GENERATED_MARKER in content:
            path.unlink()
            removed += 1

    return removed


def build_outside_register_note(row: dict[str, str], source_register_link: str, bucket_label: str) -> str:
    lines = [
        GENERATED_MARKER,
        "# Outside Source Register",
        "",
        "This repo project exists in the image inventory but is not part of image_research_register_67.md, so no per-folder collection note was created for it.",
        "",
        "## Project",
        f"- Manifest Order: {row['order']}",
        f"- Manifest Project: {row['project_name']}",
        f"- Project ID: {row['project_id']}",
        f"- Repo Folder: {row['folder']}",
        f"- Outside-Register Bucket: {bucket_label}",
        "",
        "## Reason",
        "- This project is outside the 67-project source markdown scope.",
        "- The generator only creates per-folder research notes for projects listed in image_research_register_67.md.",
        "",
        "## References",
        f"- Source Register: [image_research_register_67.md]({source_register_link})",
        f"- Original Project Folder Name: {row['folder']}",
    ]
    return "\n".join(lines) + "\n"


def locate_outside_register_folder(folder_name: str) -> Path | None:
    candidates = [
        IMAGES_ROOT / folder_name,
        OUTSIDE_REGISTER_DIR / folder_name,
        OUTSIDE_REGISTER_WITH_IMAGES_DIR / folder_name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def bucket_for_folder(folder_path: Path) -> tuple[Path, str, str]:
    has_images = folder_has_images(folder_path)
    if has_images:
        return OUTSIDE_REGISTER_WITH_IMAGES_DIR, "with_images", "../../../image_research_register_67.md"
    return OUTSIDE_REGISTER_DIR, "without_images", "../../image_research_register_67.md"


def move_outside_register_folder(folder_name: str) -> tuple[Path | None, bool, str, str]:
    current_path = locate_outside_register_folder(folder_name)
    if current_path is None:
        return None, False, "without_images", "../../image_research_register_67.md"

    target_parent, bucket_label, register_link = bucket_for_folder(current_path)
    target_parent.mkdir(exist_ok=True)
    target_path = target_parent / folder_name

    if current_path == target_path:
        return target_path, False, bucket_label, register_link

    shutil.move(str(current_path), str(target_path))
    return target_path, True, bucket_label, register_link


def write_outside_register_notes(manifest: dict[str, dict[str, str]]) -> tuple[int, int]:
    source_folders = set(PROJECT_TO_FOLDER.values())
    OUTSIDE_REGISTER_DIR.mkdir(exist_ok=True)
    OUTSIDE_REGISTER_WITH_IMAGES_DIR.mkdir(exist_ok=True)

    noted = 0
    moved = 0
    for folder_name, row in manifest.items():
        if folder_name in source_folders:
            continue

        moved_path, was_moved, bucket_label, register_link = move_outside_register_folder(folder_name)
        if moved_path is None:
            note_name = f"{OUTSIDE_NOTE_PREFIX}{int(row['order']):03d}_{row['project_id']}.md"
            note_path = OUTSIDE_REGISTER_DIR / note_name
            note_path.write_text(build_outside_register_note(row, "../image_research_register_67.md", "missing_folder"), encoding="utf-8")
            noted += 1
            continue

        if was_moved:
            moved += 1

        note_path = moved_path / OUTSIDE_FOLDER_NOTE
        note_path.write_text(build_outside_register_note(row, register_link, bucket_label), encoding="utf-8")
        noted += 1

    return noted, moved


def main() -> None:
    manifest = load_manifest()
    entries = parse_register()

    matched = 0
    created = 0
    covered = 0
    unmatched = 0
    cleaned = 0
    outside_cleaned = cleanup_outside_register_dir()

    for entry in entries:
        folder_name = PROJECT_TO_FOLDER.get(entry.project)
        if not folder_name:
            unmatched += 1
            write_unmatched_note(entry, "No canonical folder mapping is defined for this source project.")
            continue

        manifest_row = manifest.get(folder_name)
        if manifest_row is None:
            unmatched += 1
            write_unmatched_note(entry, "The mapped project folder is missing from MANIFEST.csv.")
            continue

        folder_path = IMAGES_ROOT / folder_name
        if not folder_path.exists():
            unmatched += 1
            write_unmatched_note(entry, "The mapped project folder path does not exist in the repo.")
            continue

        matched += 1
        if folder_has_images(folder_path):
            covered += 1
            if cleanup_generated_note(folder_path):
                cleaned += 1
            continue

        note_path = generated_note_path(folder_path)
        note_content = build_note(entry, folder_name, manifest_row["project_name"])
        note_path.write_text(note_content, encoding="utf-8")
        created += 1

    outside_created, outside_moved = write_outside_register_notes(manifest)

    print(f"Source projects: {len(entries)}")
    print(f"Matched folders: {matched}")
    print(f"Missing-image notes created: {created}")
    print(f"Already covered by images: {covered}")
    print(f"Unmatched source projects: {unmatched}")
    print(f"Obsolete generated notes removed: {cleaned}")
    print(f"Outside-register notes created: {outside_created}")
    print(f"Outside-register notes removed: {outside_cleaned}")
    print(f"Outside-register folders moved: {outside_moved}")


if __name__ == "__main__":
    main()