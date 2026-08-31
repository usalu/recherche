import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


src = Path(sys.argv[1])
dest = Path(sys.argv[2])
dest.mkdir(parents=True, exist_ok=True)
paths = sorted(src.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
thumb_w = 700
gap = 36
label_h = 42
font = ImageFont.load_default(size=24)

for batch_idx in range(0, len(paths), 4):
    batch = paths[batch_idx : batch_idx + 4]
    thumbs = []
    for path in batch:
        with Image.open(path) as im:
            im = im.convert("RGB")
            thumb_h = round(im.height * thumb_w / im.width)
            thumb = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            thumbs.append((path, thumb))
    row_heights = []
    for row in range(2):
        current = thumbs[row * 2 : row * 2 + 2]
        row_heights.append(max((im.height for _, im in current), default=0) + label_h)
    sheet_w = gap * 3 + thumb_w * 2
    sheet_h = gap * 3 + sum(row_heights)
    sheet = Image.new("RGB", (sheet_w, sheet_h), "#d9d9d9")
    draw = ImageDraw.Draw(sheet)
    y = gap
    for row in range(2):
        x = gap
        current = thumbs[row * 2 : row * 2 + 2]
        for path, im in current:
            page_num = int(path.stem.split("-")[-1])
            draw.rectangle((x, y, x + thumb_w, y + label_h - 4), fill="white")
            draw.text((x + 8, y + 6), f"PDF page {page_num}", font=font, fill="black")
            sheet.paste(im, (x, y + label_h))
            x += thumb_w + gap
        y += row_heights[row] + gap
    first = int(batch[0].stem.split("-")[-1])
    last = int(batch[-1].stem.split("-")[-1])
    sheet.save(dest / f"contact-{first:02d}-{last:02d}.jpg", quality=90, optimize=True)

print(f"Created {(len(paths) + 3) // 4} contact sheets")
