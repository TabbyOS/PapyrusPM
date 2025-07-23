import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "papyruspm_config.json"

def load_config():
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r") as f:
            return json.load(f)
    else:
        return {}

def save_config(config):
    with CONFIG_PATH.open("w") as f:
        json.dump(config, f, indent=4)
