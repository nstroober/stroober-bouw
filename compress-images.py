#!/usr/bin/env python3
"""Comprimeer afbeeldingen in assets/img via de TinyPNG API.

Nieuwe projectfoto's toevoegen:
  python3 compress-images.py pad/naar/foto.jpg slug-1.jpg   (verkleint, maakt -sm variant, comprimeert)
Alles opnieuw comprimeren:
  python3 compress-images.py

Vereist TINYPNG_API_KEY in .env (pip3 install tinify python-dotenv pillow).
"""
import os
import sys
from pathlib import Path

import tinify
from dotenv import load_dotenv
from PIL import Image, ImageOps

ROOT = Path(__file__).parent
IMG = ROOT / "assets" / "img"


def compress(path):
    before = path.stat().st_size
    tinify.from_file(str(path)).to_file(str(path))
    after = path.stat().st_size
    print(f"{path.relative_to(ROOT)}: {before // 1024} KB -> {after // 1024} KB")
    return before, after


def add(source, name):
    """Zet een nieuwe foto klaar als assets/img/projecten/<name> (1600px) + -sm (800px)."""
    im = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    out = IMG / "projecten" / name
    for size, target in ((1600, out), (800, out.with_name(out.stem + "-sm.jpg"))):
        copy = im.copy()
        copy.thumbnail((size, size))
        copy.save(target, "JPEG", quality=88)
        compress(target)


def main():
    load_dotenv(ROOT / ".env")
    tinify.key = os.getenv("TINYPNG_API_KEY")
    if not tinify.key:
        sys.exit("TINYPNG_API_KEY ontbreekt in .env")

    if len(sys.argv) == 3:
        add(sys.argv[1], sys.argv[2])
    else:
        files = sorted(p for p in IMG.rglob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
        total_before = total_after = 0
        for f in files:
            b, a = compress(f)
            total_before += b
            total_after += a
        print(f"Totaal: {total_before // 1024} KB -> {total_after // 1024} KB")
    print(f"TinyPNG compressies deze maand: {tinify.compression_count}")


if __name__ == "__main__":
    main()
