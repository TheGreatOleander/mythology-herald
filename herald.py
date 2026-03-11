import json, os
EP="input/episode_bundle/bundle.json"
OUT="output/promo_bundle"
os.makedirs(OUT,exist_ok=True)
bundle=json.load(open(EP))
open(f"{OUT}/youtube_description.txt","w").write(bundle["title"])
open(f"{OUT}/hashtags.txt","w").write("#mythology #story")
manifest={
 "bundle_version":"1.0",
 "source_episode_id":bundle["episode_id"],
 "generated_by":"Mythology Herald",
 "paths":{"youtube_description":"youtube_description.txt","hashtags":"hashtags.txt"}
}
json.dump(manifest,open(f"{OUT}/promo_manifest.json","w"),indent=2)
print("promo_bundle created")
