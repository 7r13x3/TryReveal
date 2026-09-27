from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
CONFIG_DIR = ROOT / "configs"

ARF_JSON = DATA_DIR / "arf.json"
RULES_JSON = DATA_DIR / "rules.json"
DEFAULT_CONFIG = CONFIG_DIR / "example.toml"
DB_PATH = ROOT / "tryreveal.db"
