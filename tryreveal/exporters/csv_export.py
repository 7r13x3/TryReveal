import csv
from pathlib import Path


def export(results, target):
    safe = target.replace("@", "_at_").replace(".", "_").replace("/", "_")
    path = Path(f"results_{safe}.csv")
    hits = results.get("hits", [])
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["name", "url", "status", "confidence", "reason"],
            extrasaction="ignore"
        )
        writer.writeheader()
        for h in hits:
            writer.writerow(h)
    return str(path)
