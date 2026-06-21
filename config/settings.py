import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


def load_settings():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
