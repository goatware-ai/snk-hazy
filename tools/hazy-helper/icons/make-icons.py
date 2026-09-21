#!/usr/bin/env python3
"""Regenerate the extension's icons.

    .venv/bin/python tools/hazy-helper/icons/make-icons.py

A rounded square with a form-row glyph: three filled rows and a short fourth, which is
what the popup does to a page. Drawn at 8x and downsampled so the small sizes stay clean.
"""
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SIZES = (16, 32, 48, 128)
BG = (47, 111, 79, 255)        # the popup's accent green
FG = (255, 255, 255, 255)
SS = 8                         # supersample factor


def draw(px: int) -> Image.Image:
    n = px * SS
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * 0.22), fill=BG)

    pad = n * 0.24
    width = n - 2 * pad
    row_h = n * 0.085
    gap = n * 0.075
    y = pad
    for i in range(4):
        w = width if i < 3 else width * 0.45      # the last row is short: still filling
        d.rounded_rectangle(
            [pad, y, pad + w, y + row_h], radius=row_h / 2, fill=FG
        )
        y += row_h + gap
    return img.resize((px, px), Image.LANCZOS)


def main() -> int:
    for px in SIZES:
        path = HERE / f"icon{px}.png"
        draw(px).save(path)
        print(f"wrote {path.relative_to(HERE.parents[2])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
