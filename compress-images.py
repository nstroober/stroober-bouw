#!/usr/bin/env python3
"""Comprimeer afbeeldingen in assets/img via de TinyPNG API.

  python3 compress-images.py            comprimeer alleen nieuwe/gewijzigde afbeeldingen
  python3 compress-images.py --all      alles opnieuw comprimeren

Welke bestanden al gecomprimeerd zijn staat in assets/img/.tinypng.json (pad -> sha1),
zodat nieuwe foto's die via /beheer/ zijn geüpload maar één keer door TinyPNG gaan.
Draait automatisch in de GitHub Action; lokaal vereist het TINYPNG_API_KEY in .env.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import tinify

ROOT = Path(__file__).parent
IMG = ROOT / "assets" / "img"
MANIFEST = IMG / ".tinypng.json"


def sha1(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()


def main():
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass
    tinify.key = os.getenv("TINYPNG_API_KEY")
    if not tinify.key:
        print("TINYPNG_API_KEY ontbreekt, compressie overgeslagen")
        return

    done = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    files = sorted(p for p in IMG.rglob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    todo = [f for f in files if "--all" in sys.argv or done.get(str(f.relative_to(IMG))) != sha1(f)]

    total_before = total_after = 0
    for f in todo:
        before = f.stat().st_size
        try:
            tinify.from_file(str(f)).to_file(str(f))
        except tinify.Error as e:
            print(f"{f.relative_to(ROOT)}: overgeslagen ({e})")
            continue
        after = f.stat().st_size
        total_before += before
        total_after += after
        done[str(f.relative_to(IMG))] = sha1(f)
        print(f"{f.relative_to(ROOT)}: {before // 1024} KB -> {after // 1024} KB")

    # Verwijderde bestanden uit het manifest halen
    existing = {str(f.relative_to(IMG)) for f in files}
    done = {k: v for k, v in sorted(done.items()) if k in existing}
    MANIFEST.write_text(json.dumps(done, indent=1) + "\n")
    print(f"{len(todo)} afbeelding(en) gecomprimeerd: {total_before // 1024} KB -> {total_after // 1024} KB "
          f"(TinyPNG deze maand: {tinify.compression_count})")


if __name__ == "__main__":
    main()
