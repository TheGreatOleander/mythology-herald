
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime

def _read_text(p: Path):
    return p.read_text(encoding="utf-8").strip() if p.exists() else ""

def _read_json(p: Path, default):
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))

def _hashtags(txt):
    return [x for x in txt.replace(",", " ").split() if x.startswith("#")]

def _thread(txt):
    lines=[l.strip() for l in txt.splitlines() if l.strip()]
    return lines if lines else ([txt] if txt else [])

def build_bundle(promo_dir: Path):
    manifest=_read_json(promo_dir/"promo_manifest.json",{})
    plan=_read_json(promo_dir/"campaign_plan.json",[])

    ig=_read_text(promo_dir/"instagram_caption.txt")
    tk=_read_text(promo_dir/"tiktok_caption.txt")
    x=_read_text(promo_dir/"x_thread.txt")
    yt=_read_text(promo_dir/"youtube_description.txt")
    tags=_hashtags(_read_text(promo_dir/"hashtags.txt"))

    title=yt.split("—")[0].strip() if "—" in yt else yt

    bundle={
        "bundle_version":"2.0",
        "run_id":manifest.get("source_episode_id","engine_run"),
        "project":"Mythology Engine",
        "generated_at":datetime.utcnow().isoformat()+"Z",
        "generated_by":manifest.get("generated_by","Mythology Herald"),
        "title":title,
        "summary":yt or ig or tk or x,
        "assets":{"images":[],"videos":[]},
        "platforms":{
            "facebook":{"text":ig,"hashtags":tags,"media":[]},
            "instagram":{"caption":ig,"hashtags":tags,"media":[]},
            "tiktok":{"caption":tk,"hashtags":tags,"media":[]},
            "x":{"posts":_thread(x)},
            "youtube":{"title":yt,"description":yt,"tags":[t.lstrip("#") for t in tags]}
        },
        "campaign_plan":plan,
        "approval":{"status":"draft"},
        "publish_results":{}
    }
    return bundle

def write_bundle(promo_dir: Path):
    bundle=build_bundle(promo_dir)
    out=promo_dir/"promo_bundle.json"
    out.write_text(json.dumps(bundle,indent=2),encoding="utf-8")
    return out

if __name__=="__main__":
    import sys
    promo=Path(sys.argv[1])
    print(write_bundle(promo))
