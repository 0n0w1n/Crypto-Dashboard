# Tkinter
import tkinter as tk

import config as C
from .crypto_price import CryptoTicker, MultiTickerApp


class Overall_price:
    def __init__(self, parent):
        self.root = parent

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
        self.btn = tk.Button(self.frame, command=self.open_crypto_price, text="☰", font=(
            "Arial", 10), fg=C.BUTTON, bg=C.BUTTON_BG)
        self.btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.c = 0

    def open_crypto_price(self):
        if self.c == 0 or self.app.active == False:
            self.c += 1
            self.root = tk.Tk()
            self.app = MultiTickerApp(self.root)
            self.root.protocol("WM_DELETE_WINDOW", self.app.on_closing)
            self.root.mainloop()
        else:
            print("Crypto Price is already open")

    def on_closing(self):
        print("Stopping Overall Crypto Price Connection")
        for ticker in self.all_tickers:
            ticker.stop()
