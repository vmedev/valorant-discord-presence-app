import json
import os

def _get_config_path():
    app_data = os.getenv("APPDATA") 
    app_dir = os.path.join(app_data, "MyApp")
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, "config.json")

CONFIG_FILE = _get_config_path()

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)