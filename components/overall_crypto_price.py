# Tkinter
import tkinter as tk

import config as C
from .crypto_price import CryptoTicker, MultiTickerApp


class Overall_price:
    def __init__(self, parent,button,load):
        self.root = parent
        self.button = button
        self.oc = load["overall"]

        # Create main frame
        self.frame = tk.Frame(self.root, width=180, bg=C.MAIN_BG)
        self.frame.pack(side=tk.LEFT, pady=(0, 20), padx=(0, 21), fill="y")
        self.frame.propagate(False)
        self.label = tk.Label(self.frame, text="PRICE",
                              font=("Arial", 15), fg=C.WHITE, bg=C.MAIN_BG)
        self.label.grid(row=0, column=0, padx=(5, 0))

        # place ticker in vertical line
        self.all_tickers = []
        for i, (symbol, display_name) in enumerate(C.TICKER_PAIRS):

            # Create ticker price from CryptoTicker class
            ticker = CryptoTicker(self.frame, symbol, display_name)

            ticker.pack(row=i+1, column=0, padx=10, pady=10, sticky="nsew")
            self.all_tickers.append(ticker)

        # Set grid weight to 1 for fit window in expand
        num_tickers = len(C.TICKER_PAIRS)
        for i in range(1, num_tickers + 1):
            self.frame.grid_rowconfigure(i, weight=1)

        # customize ticker from CryptoTicker class
        print("Starting Overall Crypto Price Connection")
        for ticker in self.all_tickers:
            ticker.border.config(bg=C.MAIN_BG)

            ticker.title.config(font=("Arial", 8))
            ticker.title.pack_configure(side=tk.LEFT)

            ticker.price_label.config(font=("Arial", 8))
            ticker.price_label.pack_configure(side=tk.RIGHT, pady=0)

            ticker.change_label.pack_forget()
            ticker.start()

        # Create button to open crypto_price
        self.app = MultiTickerApp(self.root,load)
        self.btn = tk.Button(self.frame, command=self.open_crypto_price, text="☰", 
                             font=("Arial", 10), fg=C.BUTTON, bg=C.BUTTON_BG)
        self.btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.c = 0
        
        # load save for show crypto_price
        if self.app.oc == 1:
            self.open_crypto_price()

        # Create button to hide overall price in candlestick frame
        self.btn = tk.Button(self.frame, command=self.hide, text="─", 
                             font=("Arial", 10), fg=C.BUTTON, bg=C.BUTTON_BG)
        self.btn.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    def open_crypto_price(self):
        self.app.ticker_frame.place(
                relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor="center")
        self.app.oc = 1
        
    def hide(self):
        self.frame.pack_forget()
        self.button("on")
        self.oc = 0

    def show(self):
        self.frame.pack(side=tk.LEFT, pady=(0, 20), padx=(0, 21), fill="y")
        self.button("off")
        self.oc = 1

    def on_closing(self):
        print("Stopping Overall Crypto Price Connection")
        for ticker in self.all_tickers:
            ticker.stop()
