
import json
from pathlib import Path

REQUIRED=["bundle_version","run_id","project","generated_at","platforms"]

def validate(path: Path):
    data=json.loads(path.read_text())
    missing=[k for k in REQUIRED if k not in data]
    return missing

if __name__=="__main__":
    import sys
    p=Path(sys.argv[1])
    m=validate(p)
    if m:
        print("Missing:",m)
    else:
        print("Bundle OK")
