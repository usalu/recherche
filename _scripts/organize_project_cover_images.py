from __future__ import annotations

import shutil
from pathlib import Path


IMAGES_ROOT = Path(r"e:\recherche\_neo4j\review\2026-05-31_project_direct_topology_export_mit-bestand\images")
OUTSIDE_REGISTER_DIR = IMAGES_ROOT / "outside_register_projects"
OUTSIDE_REGISTER_WITH_IMAGES_DIR = OUTSIDE_REGISTER_DIR / "with_images"
COVER_FILENAME = "cover.jpg"
EXTRA_IMAGES_DIRNAME = "additional_images"
IMAGE_EXTENSION = ".jpg"

PRIMARY_IMAGE_OVERRIDES = {
    "009_p_big_dig_house_lexington_massachusetts": "big-dig-house_garden-house_3255-Custom.jpg",
    "010_p_biopartner_5_leiden_oegstgeest": "PTSA-Biopartner-5-20210601050.jpg",
    "012_p_boulder_fire_station_3": "16_boulder-station-3-green-roof_photo-by-thomas-ellis_davis-partnership-architects.jpg",
    "023_p_circular_centre_netherlands_prinsenhof_a_reuse_pilot": "Depot-2048x1154.jpg",
    "028_p_elys_kultur_gewerbehaus_basel": "elys_7r205811-5829_martin_zeller.jpg",
    "046_p_jeugdkliniek_ithaka_emergis_kloetinge": "aangepast-20190501_EW41351-HDR_PHOTO-©-EDDY-WESTVEER-1-600x480.jpg",
    "098_p_verbiest_karreveld_brussels": "MAL2020_AgwA_Verbiest_Final_25LT.jpg",
    "011_p_bluecity_offices_rotterdam": "BlueCity-Offices-1.jpg",
    "027_p_elementa_walkeweg": "Walkeweg-Visualisierung-scaled.jpg",
}

NEGATIVE_KEYWORDS = {
    "screenshot": 50,
    "whatsapp": 40,
    "thumb": 30,
    "images": 20,
    "corridor": 20,
    "small": 15,
    "mezzanine": 15,
    "pdf": 30,
    "detail": 10,
    "interior": 10,
}

POSITIVE_KEYWORDS = {
    "visualisierung": 25,
    "overview": 10,
    "facade": 10,
    "garden": 8,
    "roof": 8,
    "office": 6,
    "offices": 6,
    "public": 4,
}


def iter_project_folders() -> list[Path]:
    folders: list[Path] = []

    for child in sorted(IMAGES_ROOT.iterdir()):
        if child.is_dir() and child.name != OUTSIDE_REGISTER_DIR.name:
            folders.append(child)

    if OUTSIDE_REGISTER_DIR.exists():
        for child in sorted(OUTSIDE_REGISTER_DIR.iterdir()):
            if not child.is_dir():
                continue
            if child.name == OUTSIDE_REGISTER_WITH_IMAGES_DIR.name:
                for nested in sorted(child.iterdir()):
                    if nested.is_dir():
                        folders.append(nested)
                continue
            folders.append(child)

    return folders


def iter_images(folder: Path) -> list[Path]:
    return sorted(
        path for path in folder.rglob(f"*{IMAGE_EXTENSION}")
        if path.is_file()
    )


def candidate_score(folder: Path, image: Path) -> tuple[int, int, int, str]:
    name = image.name.lower()
    score = 0

    for keyword, penalty in NEGATIVE_KEYWORDS.items():
        if keyword in name:
            score -= penalty

    for keyword, bonus in POSITIVE_KEYWORDS.items():
        if keyword in name:
            score += bonus

    if image.parent == folder:
        score += 5

    return score, image.stat().st_size, len(name) * -1, name


def select_primary_image(folder: Path, images: list[Path]) -> Path:
    existing_cover = folder / COVER_FILENAME
    if existing_cover.exists():
        return existing_cover

    override_name = PRIMARY_IMAGE_OVERRIDES.get(folder.name)
    if override_name:
        for image in images:
            if image.name == override_name:
                return image

    if len(images) == 1:
        return images[0]

    return max(images, key=lambda image: candidate_score(folder, image))


def unique_path(target: Path) -> Path:
    if not target.exists():
        return target

    stem = target.stem
    suffix = target.suffix
    index = 1
    while True:
        candidate = target.with_name(f"{stem}_{index}{suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def move_to_extras(folder: Path, source: Path) -> Path:
    extras_dir = folder / EXTRA_IMAGES_DIRNAME
    extras_dir.mkdir(exist_ok=True)
    target = unique_path(extras_dir / source.name)
    if source == target:
        return source
    source.rename(target)
    return target


def ensure_cover(folder: Path, primary: Path) -> Path:
    cover_path = folder / COVER_FILENAME
    if primary == cover_path:
        return cover_path

    if cover_path.exists():
        move_to_extras(folder, cover_path)

    if primary.parent != folder:
        shutil.move(str(primary), str(cover_path))
        return cover_path

    primary.rename(cover_path)
    return cover_path


def cleanup_empty_extras(folder: Path) -> None:
    extras_dir = folder / EXTRA_IMAGES_DIRNAME
    if extras_dir.exists() and not any(extras_dir.iterdir()):
        extras_dir.rmdir()


def organize_folder(folder: Path) -> tuple[bool, int, str | None]:
    images = iter_images(folder)
    if not images:
        return False, 0, None

    primary = select_primary_image(folder, images)
    cover_path = ensure_cover(folder, primary)

    moved = 0
    for image in sorted(iter_images(folder)):
        if image == cover_path:
            continue
        if image.parent == folder / EXTRA_IMAGES_DIRNAME:
            continue
        move_to_extras(folder, image)
        moved += 1

    cleanup_empty_extras(folder)
    return True, moved, cover_path.name


def main() -> None:
    total_folders = 0
    image_folders = 0
    skipped_without_images = 0
    extras_moved = 0

    for folder in iter_project_folders():
        total_folders += 1
        has_image, moved, cover_name = organize_folder(folder)
        if not has_image:
            skipped_without_images += 1
            print(f"SKIP {folder}: no jpg images")
            continue

        image_folders += 1
        extras_moved += moved
        print(f"OK   {folder}: {cover_name}, moved extras={moved}")

    print(f"Project folders scanned: {total_folders}")
    print(f"Folders with images normalized: {image_folders}")
    print(f"Folders without images skipped: {skipped_without_images}")
    print(f"Extra images moved: {extras_moved}")


if __name__ == "__main__":
    main()