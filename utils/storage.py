# for save/load
import json
import os

SETTINGS_FILE = "settings.json"


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)

    # Default Setting
    return {
        "current": "BTC/USDT",
        "interval": "1 Minute",
        "current_order": "BID (BUYS)",
        "current_show": "ASK (SELLS)",
        "overall": 1,
        "full_price": 0,
    }


def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)


load_set = load_settings()
