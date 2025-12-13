# Tkinter
import tkinter as tk
from tkinter import ttk

# API
import websocket
import json
import threading
import requests

import config as C

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

        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=lambda ws, err: print(
                f"───{self.symbol} Price Error: {err}"),
            on_close=lambda ws, s, m: print("", end=""),
            on_open=lambda ws: print(f"───{self.symbol} Price Connected")
        )

        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def stop(self):
        """Stop WebSocket connection."""
        if self.is_active and self.ws:
            self.ws.close()
            print(f"───{self.symbol} Price Closed")
            self.is_active = False
            self.ws = None

    def on_message(self, ws, message):
        """Handle price updates."""
        if not self.is_active:
            return

        try:
            if self.parent.winfo_exists():
                data = json.loads(message)
                # 'c' = close price, 'p' = price change, 'P' = percent change
                price = float(data['c'])
                change = float(data['p'])
                percent = float(data['P'])

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
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Dashboard")
        self.root.geometry("1000x600")
        self.is_active = True

        # List of currency to show
        self.TICKER_PAIRS = [
            ("BTCUSDT", "BTC/USDT"), ("ETHUSDT", "ETH/USDT"),
            ("XRPUSDT", "XRP/USDT"), ("BNBUSDT", "BNB/USDT"),
            ("SOLUSDT", "SOL/USDT"), ("TRXUSDT", "TRX/USDT"),
            ("DOGEUSDT", "DOGE/USDT"), ("ADAUSDT", "ADA/USDT"),
            ("BCHUSDT", "BCH/USDT")
        ]

        self.all_tickers = []

        # Create ticker panel
        ticker_frame = tk.Frame(root, bg=C.MAIN_BG)
        ticker_frame.pack(fill=tk.BOTH, expand=True)

        # Expand column and row equally
        for i in range(3):
            ticker_frame.grid_columnconfigure(i, weight=1)
            ticker_frame.grid_rowconfigure(i, weight=1)

        # Create and place the tickers in a 3x3
        for i, (symbol, display_name) in enumerate(self.TICKER_PAIRS):
            row = i // 3  # 0, 0, 0, 1, 1, 1, 2, 2, 2
            col = i % 3   # 0, 1, 2, 0, 1, 2, 0, 1, 2

            ticker = CryptoTicker(ticker_frame, symbol, display_name)

            ticker.pack(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.all_tickers.append(ticker)

        # Start all tickers
        print("\nStarting Crypto Price Connection (Full)")
        for ticker in self.all_tickers:
            ticker.start()

    def on_closing(self):
        print("Stopping Crypto Price Connection (Full)")
        self.is_active = False

        for ticker in self.all_tickers:
            ticker.stop()

        self.root.destroy()
