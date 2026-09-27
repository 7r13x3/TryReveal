import json
from pathlib import Path


def export(results, target):
    safe = target.replace("@", "_at_").replace(".", "_").replace("/", "_")
    path = Path(f"results_{safe}.json")
    path.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    return str(path)
