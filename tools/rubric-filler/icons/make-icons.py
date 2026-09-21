#!/usr/bin/env python3
"""Generate the extension's toolbar icons.

Kept in the repo so the icons can be regenerated rather than being three opaque
binaries: a rounded square in the popup's accent purple, carrying three bars for
the criterion list with the last one in the highlight yellow the preview uses for
a row this run wrote.

    python3 icons/make-icons.py
"""
import struct
import zlib
from pathlib import Path

BG = (108, 99, 224, 255)      # #6c63e0, the Fill button
BAR = (255, 255, 255, 255)
ACCENT = (255, 211, 102, 255)  # #ffd366, the "changed row" highlight
CLEAR = (0, 0, 0, 0)

BARS = [(0.30, 0.24, 0.78, BAR), (0.50, 0.24, 0.70, BAR), (0.70, 0.24, 0.58, ACCENT)]


def rounded(x, y, size, radius):
    """Is pixel (x, y) inside a rounded square of side `size`?"""
    cx = min(max(x, radius), size - radius)
    cy = min(max(y, radius), size - radius)
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius**2


def render(size):
    radius = size * 0.22
    thickness = max(2.0, size * 0.10)
    rows = []
    for y in range(size):
        row = []
        for x in range(size):
            px = BG if rounded(x + 0.5, y + 0.5, size, radius) else CLEAR
            for cy, x0, x1, color in BARS:
                if abs((y + 0.5) - cy * size) <= thickness / 2 and x0 * size <= x + 0.5 <= x1 * size:
                    px = color
            row.append(px)
        rows.append(row)
    return rows


def write_png(path, rows):
    size = len(rows)
    raw = b"".join(b"\x00" + b"".join(bytes(px) for px in row) for row in rows)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    Path(path).write_bytes(png)


if __name__ == "__main__":
    here = Path(__file__).parent
    for size in (16, 32, 48, 128):
        write_png(here / f"icon{size}.png", render(size))
        print(f"wrote icon{size}.png")
