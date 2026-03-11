import json
from pathlib import Path

EP = Path("input/episode_bundle")
MEDIA = Path("input/media_bundle")
OUT = Path("output/promo_bundle")
OUT.mkdir(parents=True, exist_ok=True)

bundle = json.load(open(EP / "bundle.json"))
metadata = json.load(open(EP / "metadata.json")) if (EP / "metadata.json").exists() else {}
media = json.load(open(MEDIA / "media_manifest.json")) if (MEDIA / "media_manifest.json").exists() else {}

title = bundle.get("title", "Untitled Episode")
episode_id = bundle.get("episode_id", "unknown_episode")
topic = bundle.get("topic", title)
series = metadata.get("series", "Mythology")
tags = metadata.get("tags", [])
tone = metadata.get("tone", "cinematic")
video_path = media.get("paths", {}).get("final_video", "final_video.mp4")
thumbnail_path = media.get("paths", {}).get("thumbnail", "thumbnail.png")

youtube_description = f"""{title}

A new episode from Mythology Engine explores: {topic}.
Series: {series}
Tone: {tone}

This release includes visual assets prepared by Mythology Forge.

#mythology #mystery #cinematic
"""
tiktok_caption = f"{title} — hidden mystery from the archive. #{' #'.join(tags[:3])}" if tags else f"{title} — hidden mystery from the archive. #mythology #mystery"
instagram_caption = f"{title}\n\nA {tone} mystery from {series}.\n\n" + (" ".join(f"#{t}" for t in tags[:5]) if tags else "#mythology #archive")
x_thread = f"1/ A new Mythology Engine episode explores: {title}\n2/ Topic: {topic}\n3/ Visuals prepared by Mythology Forge."

(OUT / "youtube_description.txt").write_text(youtube_description, encoding="utf-8")
(OUT / "tiktok_caption.txt").write_text(tiktok_caption, encoding="utf-8")
(OUT / "instagram_caption.txt").write_text(instagram_caption, encoding="utf-8")
(OUT / "x_thread.txt").write_text(x_thread, encoding="utf-8")
(OUT / "hashtags.txt").write_text(" ".join(f"#{t}" for t in tags) if tags else "#mythology #mystery #cinematic", encoding="utf-8")

campaign_plan = {
    "episode_id": episode_id,
    "title": title,
    "campaign_waves": [
        {"platform": "youtube", "asset": "youtube_description.txt", "timing": "launch"},
        {"platform": "tiktok", "asset": "tiktok_caption.txt", "timing": "same_day"},
        {"platform": "instagram", "asset": "instagram_caption.txt", "timing": "same_day_evening"},
        {"platform": "x", "asset": "x_thread.txt", "timing": "same_day_evening"}
    ],
    "media_inputs": {
        "video": video_path,
        "thumbnail": thumbnail_path
    },
    "tone": tone,
    "tags": tags
}
json.dump(campaign_plan, open(OUT / "campaign_plan.json", "w"), indent=2)

manifest = {
    "bundle_version": "1.0",
    "source_episode_id": episode_id,
    "generated_by": "Mythology Herald",
    "derived_from": {
        "bundle": "input/episode_bundle/bundle.json",
        "metadata": "input/episode_bundle/metadata.json",
        "media_manifest": "input/media_bundle/media_manifest.json"
    },
    "paths": {
        "youtube_description": "youtube_description.txt",
        "tiktok_caption": "tiktok_caption.txt",
        "instagram_caption": "instagram_caption.txt",
        "x_thread": "x_thread.txt",
        "hashtags": "hashtags.txt",
        "campaign_plan": "campaign_plan.json"
    }
}
json.dump(manifest, open(OUT / "promo_manifest.json", "w"), indent=2)
print("promo_bundle v0.3 created")
