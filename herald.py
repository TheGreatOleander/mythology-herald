
import json, shutil
from pathlib import Path

EP = Path("input/episode_bundle")
MEDIA = Path("input/media_bundle")
OUT = Path("output/promo_bundle")

# deterministic run
if OUT.exists():
    shutil.rmtree(OUT)

OUT.mkdir(parents=True, exist_ok=True)
WAVES = OUT/"waves"
WAVES.mkdir()

bundle=json.load(open(EP/"bundle.json"))
metadata=json.load(open(EP/"metadata.json"))
media=json.load(open(MEDIA/"media_manifest.json"))

title=bundle["title"]
tags=metadata["tags"]
episode_id=bundle["episode_id"]

youtube=f"{title}\n\n#mythology #story"
tiktok=f"{title} #shorts"
instagram=f"{title}\n#mythology"
x_thread=f"New episode: {title}"

(OUT/"youtube_description.txt").write_text(youtube)
(OUT/"tiktok_caption.txt").write_text(tiktok)
(OUT/"instagram_caption.txt").write_text(instagram)
(OUT/"x_thread.txt").write_text(x_thread)
(OUT/"hashtags.txt").write_text(" ".join(f"#{t}" for t in tags))

campaign=[
 {"wave":1,"asset":"youtube_description.txt"},
 {"wave":2,"asset":"tiktok_caption.txt"},
 {"wave":2,"asset":"instagram_caption.txt"},
 {"wave":3,"asset":"x_thread.txt"}
]

json.dump(campaign, open(OUT/"campaign_plan.json","w"), indent=2)

for wave in [1,2,3]:
    wd=WAVES/f"wave_{wave:02}"
    wd.mkdir()
    for c in campaign:
        if c["wave"]==wave:
            src=OUT/c["asset"]
            dst=wd/c["asset"]
            dst.write_text(src.read_text())

manifest={
 "bundle_version":"1.0",
 "source_episode_id":episode_id,
 "generated_by":"Mythology Herald"
}

json.dump(manifest, open(OUT/"promo_manifest.json","w"), indent=2)

print("promo_bundle v0.5 created (deterministic)")
