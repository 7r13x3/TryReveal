import json
from tryreveal.core.paths import ARF_JSON, RULES_JSON


def load_map(path=None):
    path = path or ARF_JSON
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_rules():
    try:
        with open(RULES_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_rules(rules):
    with open(RULES_JSON, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)
