# Tkinter and config
import tkinter as tk
from tkinter import ttk
import config as C

# API
from utils.api import BinanceAPI


class CryptoTicker:

    def __init__(self, parent, symbol, display_name):
        self.parent = parent
        self.symbol = symbol.lower()
        self.display_name = display_name
        self.is_active = False
        self.ws = None

        # Create UI
        self.border = tk.Frame(parent, bg='white')
        self.frame = tk.Frame(self.border, bg=C.MAIN_BG)
        self.frame.pack(padx=1, pady=1, fill=tk.BOTH, expand=True)

        # Title
        self.title = ttk.Label(self.frame, text=display_name,
                               font=("Arial", 26, "bold"),
                               background=C.MAIN_BG, foreground=C.WHITE)
        self.title.pack()

        # Price
        self.price_label = tk.Label(self.frame, text="--,---.--",
                                    font=("Arial", 35, "bold"),
                                    background=C.MAIN_BG)
        self.price_label.pack(pady=10)

        # Change
        self.change_label = ttk.Label(self.frame, text="--",
                                      font=("Arial", 18),
                                      background=C.MAIN_BG)
        self.change_label.pack()

    def start(self):
        """Start WebSocket connection."""
        if self.is_active:
            return

        self.is_active = True
        ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@ticker"

        self.api = BinanceAPI(ws_url)
        self.api.start(self.on_message,
                       lambda ws, err: print(
                           f"───{self.display_name} Price Error: {err}"),
                       lambda ws, s, m: print("", end=""),
                       lambda ws: print(
                           f"───{self.display_name} Price Connected")
                       )

    def stop(self):
        """Stop WebSocket connection."""
        if self.is_active and self.api.ws:
            self.api.ws.close()
            print(f"───{self.display_name} Price Closed")
            self.is_active = False
            self.ws = None

    def on_message(self):
        """Handle price updates."""
        if not self.is_active:
            return

        try:
            if self.parent.winfo_exists():
                # 'c' = close price, 'p' = price change, 'P' = percent change
                price = float(self.api.data['c'])
                change = float(self.api.data['p'])
                percent = float(self.api.data['P'])

                # Schedule GUI update on main thread
                self.parent.after(0, self.update_display,
                                  price, change, percent)
        except tk.TclError:
            pass

    def update_display(self, price, change, percent):
        try:
            # Check for label exist
            if not self.is_active or not self.price_label.winfo_exists():
                return

            # For Main price
            color = C.GREEN if change >= 0 else C.RED
            self.price_label.config(text=f"{price:,.2f}", fg=color)

            # For changing percent
            color = C.GREEN_2 if change >= 0 else C.RED_2
            sign = "+" if change >= 0 else ""
            self.change_label.config(
                text=f"{sign}{change:,.2f} ({sign}{percent:.2f}%)",
                foreground=color
            )
        except:
            pass

    def pack(self, **kwargs):
        """Allow easy placement of ticker."""
        self.border.grid(**kwargs)

    def pack_forget(self):
        """Hide the ticker."""
        self.frame.pack_forget()


class MultiTickerApp:
    def __init__(self, root,load):
        self.root = root
        self.is_active = True
        self.oc = load["full_price"]

        self.all_tickers = []

        # Create ticker panel
        self.ticker_frame = tk.Frame(root, bg=C.MAIN_BG)

        # Expand column and row equally
        for i in range(3):
            self.ticker_frame.grid_columnconfigure(i, weight=1)
            self.ticker_frame.grid_rowconfigure(i, weight=1)

        # Create and place the tickers in a 3x3
        for i, (symbol, display_name) in enumerate(C.TICKER_PAIRS):
            row = i // 3  # 0, 0, 0, 1, 1, 1, 2, 2, 2
            col = i % 3   # 0, 1, 2, 0, 1, 2, 0, 1, 2

            ticker = CryptoTicker(self.ticker_frame, symbol, display_name)

            ticker.pack(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.all_tickers.append(ticker)

        # Hide button
        self.hide_button = tk.Button(self.ticker_frame, font=("Arial", 10), fg=C.BUTTON,
                                     bg=C.BUTTON_BG, text="Hide", command=self.forget)
        self.hide_button.place(relx=1.0,rely=0.0,relheight=0.05,relwidth=0.05,anchor="ne")

        # Start all tickers
        print("\nStarting Crypto Price Connection (Full)")
        for ticker in self.all_tickers:
            ticker.start()

    def on_closing(self):
        print("Stopping Crypto Price Connection (Full)")
        self.is_active = False

        for ticker in self.all_tickers:
            ticker.stop()

        self.ticker_frame.destroy()

    def forget(self):
        self.ticker_frame.place_forget()
        self.oc = 0
