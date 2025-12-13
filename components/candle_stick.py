# Import Tkinter
import tkinter as tk
from tkinter import ttk

# For API
import websocket
import json
import threading
import requests

# Candle stick drawing
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config as C


class CandleStick(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.bind("<Destroy>", lambda e: plt.close(self.fig))

        # Setup url and params
        self.url = "https://api.binance.com/api/v3/klines"
        self.params = {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "limit": 10
        }
        self.klines = requests.get(self.url, params=self.params).json()

        # Get data
        self.data = []
        for data in self.klines:
            # Convert time from millisec to date
            date = datetime.fromtimestamp(data[0]/1000).strftime("%H:%M:%S")
            self.data.append([
                date,
                float(data[1]),  # open
                float(data[2]),  # high
                float(data[3]),  # low
                float(data[4]),  # close
                float(data[5])   # volume
            ])

        # Draw candle stick
        self.fig, self.x = plt.subplots(figsize=(8, 4))
        self.candle_width = 0.6
        self.dates = []

        for i, datas in enumerate(self.data):
            time, open_price, high_price, low_price, close_price, volume = datas
            self.dates.append(time)

            # Change color
            color = C.GREEN_2 if close_price >= open_price else C.RED

            # Wick of candle stick
            self.x.vlines(i, low_price, high_price, color=color, linewidth=1)

            # Body of candle stick
            bottom = min(open_price, close_price)
            height = abs(open_price-close_price)
            body = plt.Rectangle((i - self.candle_width/2, bottom),
                                 self.candle_width, height, facecolor=color, edgecolor="none")
            self.x.add_patch(body)

        # Set Axis
        self.x.set_xticks(np.arange(len(self.data)))
        self.x.set_xticklabels(self.dates, rotation=45, fontsize=8)

        # Set Color
        self.x.tick_params(axis='x', colors=C.WHITE)
        self.x.tick_params(axis='y', colors=C.WHITE)
        self.x.set_facecolor(C.MAIN_BG)
        self.fig.set_facecolor(C.MAIN_BG)

        self.canvas = FigureCanvasTkAgg(
            self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.canvas.draw()

    def on_closing(self):
        self.destroy()
