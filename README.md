# Mythology Herald v0.3

Consumes `episode_bundle` and `media_bundle` to produce a richer `promo_bundle`.

## New in v0.3
- Reads `metadata.json` for tags and tone
- Reads `media_manifest.json` for media references
- Produces platform-specific promo files
- Generates a simple campaign plan based on bundle + media manifest

## Run
```bash
python herald.py
```
