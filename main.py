# Tkinter
import tkinter as tk
from main_dashboard import MainDashBoard

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
        "interval": "1 Minutes",
        "current_order": "BID (BUYS)",
        "current_show": "ASK (SELLS)"
    }


def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)


load_set = load_settings()

# Run Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = MainDashBoard(root, load_set, save_settings)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
