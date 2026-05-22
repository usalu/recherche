from __future__ import annotations

from pathlib import Path
import re


IMAGES_ROOT = Path(r"e:\recherche\_neo4j\review\2026-05-31_project_direct_topology_export_mit-bestand\images")
JPEG_EXTENSIONS = {".jpg", ".jpeg"}
CONVERTIBLE_EXTENSIONS = {".png", ".webp", ".gif", ".bmp", ".tif", ".tiff", ".avif"}


def load_pillow() -> tuple[object, object]:
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise SystemExit(
            "Pillow is required. Install it with: py -3 -m pip install Pillow pillow-avif-plugin"
        ) from exc

    try:
        import pillow_avif  # noqa: F401
    except ImportError:
        pass

    return Image, ImageOps


def resolve_target_path(source: Path) -> Path:
    normalized_stem = re.sub(r"(\.jpe?g)+$", "", source.stem, flags=re.IGNORECASE)
    if not normalized_stem:
        normalized_stem = source.stem

    base_target = source.with_name(f"{normalized_stem}.jpg")
    if not base_target.exists() or base_target == source:
        return base_target

    suffix_name = source.suffix.lstrip(".").lower() or "converted"
    candidate = source.with_name(f"{normalized_stem}_{suffix_name}.jpg")
    index = 1
    while candidate.exists() and candidate != source:
        candidate = source.with_name(f"{normalized_stem}_{suffix_name}_{index}.jpg")
        index += 1
    return candidate


def ensure_rgb(image, image_module):
    if image.mode in {"RGBA", "LA"}:
        background = image.getchannel("A")
        flattened = image.convert("RGBA")
        canvas = image_module.new("RGB", flattened.size, (255, 255, 255))
        canvas.paste(flattened, mask=background)
        return canvas

    if image.mode == "P":
        converted = image.convert("RGBA")
        alpha = converted.getchannel("A")
        canvas = image_module.new("RGB", converted.size, (255, 255, 255))
        canvas.paste(converted, mask=alpha)
        return canvas

    if image.mode != "RGB":
        return image.convert("RGB")

    return image


def convert_file(source: Path, image_module, image_ops_module) -> tuple[bool, Path | None]:
    suffix = source.suffix.lower()
    if suffix == ".jpg":
        return False, None

    if suffix == ".jpeg":
        target = resolve_target_path(source)
        source.rename(target)
        return True, target

    if suffix not in CONVERTIBLE_EXTENSIONS:
        return False, None

    target = resolve_target_path(source)
    with image_module.open(source) as image:
        image = image_ops_module.exif_transpose(image)
        image = ensure_rgb(image, image_module)
        image.save(target, format="JPEG", quality=95, optimize=True)

    source.unlink()
    return True, target


def iter_images(root: Path):
    valid_extensions = JPEG_EXTENSIONS | CONVERTIBLE_EXTENSIONS
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in valid_extensions:
            yield path


def main() -> None:
    image_module, image_ops_module = load_pillow()

    converted = []
    skipped = []

    for source in sorted(iter_images(IMAGES_ROOT)):
        changed, target = convert_file(source, image_module, image_ops_module)
        if changed:
            converted.append((source, target))
        else:
            skipped.append(source)

    print(f"Converted or renamed to .jpg: {len(converted)}")
    print(f"Already .jpg or unsupported: {len(skipped)}")
    for source, target in converted:
        print(f"{source} -> {target}")


if __name__ == "__main__":
    main()