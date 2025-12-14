# Import Tkinter, config and api
import tkinter as tk
import config as C
from utils.api import RestAPI

# Candle stick drawing
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CandleStick(tk.Frame):
    def __init__(self, parent, symbol, interval_start):
        super().__init__(parent)
        # Setup api
        self.url = "https://api.binance.com/api/v3/klines"
        self.api = RestAPI(self.url)

        # For closing
        self.bind("<Destroy>", lambda e: plt.close(self.fig))

        # State
        self.display = symbol
        self.symbol = self.display.replace("/", "")
        self.interval = interval_start
        self.interval_update = self.interval.replace(" ", "")[:2].lower()
        self.limit = 50
        self.update_interval_ms = 5000  # 5s

        self.btn_frame = tk.Frame(self, bg=C.MAIN_BG)
        self.btn_frame.pack(fill=tk.X)

        # Text for candle stick
        self.text = tk.Label(self.btn_frame, text=f"{self.display} {self.interval} Candlestick (Last 50 {self.interval[2:]}s)",
                             bg=C.MAIN_BG, font=("Arial", 10), fg=C.WHITE)
        self.text.pack()

        # Button to change between 24H and 1m
        self.all_btn = []

        self.btn1 = tk.Button(
            self.btn_frame, text="1 Minute",
            command=lambda: self.change_interval(self.symbol, "1 Minute"), bg=C.BUTTON_BG, fg=C.BUTTON)
        self.btn1.pack(side=tk.LEFT, padx=(5, 0), pady=5)

        self.btn2 = tk.Button(
            self.btn_frame, text="1 Hour",
            command=lambda: self.change_interval(self.symbol, "1 Hour"), bg=C.BUTTON_BG, fg=C.BUTTON)
        self.btn2.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn3 = tk.Button(
            self.btn_frame, text="1 Day",
            command=lambda: self.change_interval(self.symbol, "1 Day"), bg=C.BUTTON_BG, fg=C.BUTTON)
        self.btn3.pack(side=tk.LEFT, padx=5, pady=5)

        self.all_btn.append(self.btn1)
        self.all_btn.append(self.btn2)
        self.all_btn.append(self.btn3)
        self.btn_click(self.interval)

        # Create Frame
        self.fig, (self.x_price, self.x_vol) = plt.subplots(
            2, 1,
            figsize=(8, 5),
            sharex=True,
            gridspec_kw={"height_ratios": [3, 1]}
        )
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().place(x=200, y=0)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update()

    def draw_candle_stick(self, klines):
        self.x_price.clear()
        self.x_vol.clear()

        # Get current data
        data = []
        for d in klines:
            date = datetime.fromtimestamp(d[0]/1000).strftime(f"%b %d, %H:%M")
            data.append([
                date,
                float(d[1]),  # Open Price
                float(d[2]),  # High Price
                float(d[3]),  # Low Price
                float(d[4]),  # Close Price
                float(d[5]),  # Volume
            ])

        candle_width = 0.6
        dates = []

        # Creat Candle Stick
        for i, (time, open, high, low, close, vol) in enumerate(data):
            dates.append(time)
            color = C.GREEN_2 if close >= open else C.RED
            color_vol = C.GREEN if close >= open else C.PURPLE

            # Wick
            self.x_price.vlines(i, low, high, color=color, linewidth=1)

            # Body
            body = plt.Rectangle(
                (i - candle_width/2, min(open, close)),
                candle_width,
                abs(open - close),
                facecolor=color,
                edgecolor="none"
            )
            self.x_price.add_patch(body)

            # Volume Bar
            self.x_vol.bar(
                i, vol,
                color=color_vol,
                width=0.6,
                alpha=0.6
            )

        # Set date on horizontal datas
        # Use only 10 date
        def filter_date(i, x): return x if i % 5 == 4 or i == 0 else ""
        dates_show = [filter_date(i, x) for i, x in enumerate(dates)]
        self.x_vol.set_xticks(np.arange(len(dates_show)))
        self.x_vol.set_xticklabels(dates_show, rotation=45, fontsize=8)

        # Set colors x price
        self.x_price.tick_params(axis='x', colors=C.WHITE)
        self.x_price.tick_params(axis='y', colors=C.WHITE)
        self.x_price.set_facecolor(C.MAIN_BG)
        self.fig.set_facecolor(C.MAIN_BG)

        # Set color x volume
        self.x_vol.tick_params(axis='x', colors=C.WHITE)
        self.x_vol.tick_params(axis='y', colors=C.WHITE)
        self.x_vol.set_facecolor(C.MAIN_BG)
        self.x_vol.set_ylabel("Volume", color=C.WHITE)

        # Customize Grid
        self.x_price.grid(
            True,
            color=C.WHITE,
            alpha=0.1,
            linestyle="--",
            linewidth=0.5
        )

        self.x_vol.grid(
            True,
            color=C.WHITE,
            alpha=0.1,
            linestyle="--",
            linewidth=0.5
        )

        self.fig.tight_layout()
        self.canvas.draw()

    def btn_click(self, interval_button):
        inuse = interval_button

        for i, btn in enumerate(self.all_btn):
            text = btn.cget("text")

            if text == inuse:
                button = tk.Label(
                    self.btn_frame, text=inuse, bg=C.TABLE_BG, fg=C.BACKGROUND)
            else:
                button = tk.Button(
                    self.btn_frame, text=text, bg=C.BUTTON_BG, fg=C.BUTTON,
                    command=lambda t = text: self.change_interval(self.symbol,t))
                
            button.pack(side=tk.LEFT, padx=(5, 0), pady=5)
            btn.destroy()
            self.all_btn[i] = button

    def change_interval(self, current, interval=None):
        self.display = current
        self.symbol = current.replace("/", "")

        # Set Interval
        if interval != None:
            self.interval = interval
        self.btn_click(self.interval)

        # Change text
        print(f"Changing Candlestick to {self.display} ({self.interval})")
        self.text.config(
            text=f"{self.display} {self.interval} Candlestick (Last 50 {self.interval[2:]}s)")

        self.interval_update = self.interval.replace(" ", "")[:2].lower()
        self.update(new=True)

    def update(self, new=False):
        try:
            klines = self.get_data()
            self.draw_candle_stick(klines)
        except Exception as e:
            print("Update Candle Stick Error:", e)

        # Next update
        try:
            if not new:
                # Contain after in var to close when using on_closing
                self.after_id = self.after(
                    self.update_interval_ms, self.update)
        except Exception:
            pass

    def get_data(self):
        params = {
            "symbol": self.symbol,
            "interval": self.interval_update,
            "limit": self.limit
        }

        return self.api.get_data(params)

    def on_closing(self):
        print("Closing Candle Stick")
        try:
            self.after_cancel(self.after_id)
        except:
            pass
        self.destroy()
