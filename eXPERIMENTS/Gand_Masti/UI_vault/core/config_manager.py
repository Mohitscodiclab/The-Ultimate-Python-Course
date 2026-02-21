import os, json

CONFIG_DIR = "system"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def config_exists():
    return os.path.exists(CONFIG_FILE)

def load_config():
    if not config_exists():
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)