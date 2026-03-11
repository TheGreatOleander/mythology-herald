import json
import shutil
from pathlib import Path

PROMO = Path("/sdcard/mythology-herald/output/promo_bundle")
PACKS = PROMO / "platform_packs"

def copy_if_exists(src: Path, dst: Path):
    if src.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

def main():
    if PACKS.exists():
        shutil.rmtree(PACKS)
    PACKS.mkdir(parents=True, exist_ok=True)

    mapping = {
        "youtube": ["youtube_description.txt", "hashtags.txt"],
        "youtube_shorts": ["youtube_shorts_caption.txt", "hashtags.txt"],
        "tiktok": ["tiktok_caption.txt", "hashtags.txt"],
        "instagram": ["instagram_caption.txt", "hashtags.txt"],
        "instagram_reels": ["instagram_reels_caption.txt", "hashtags.txt"],
        "x": ["x_thread.txt", "hashtags.txt"]
    }

    manifest = {}
    for platform, files in mapping.items():
        pdir = PACKS / platform
        pdir.mkdir(parents=True, exist_ok=True)
        manifest[platform] = []
        for name in files:
            src = PROMO / name
            dst = pdir / name
            if src.exists():
                copy_if_exists(src, dst)
                manifest[platform].append(name)

    (PROMO / "platform_packs_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("platform_packs created")

if __name__ == "__main__":
    main()
