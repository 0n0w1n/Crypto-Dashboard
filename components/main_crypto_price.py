# Tkinter
import tkinter as tk
from tkinter import ttk

# API
import websocket
import json
import threading
import requests

from .crypto_price import CryptoTicker
import config as C

class MainCryptoPrice:
    def __init__(self, parent,change):
        self.crypto_frame = parent    

        # Create crypto price
        self.button = []
        self.main_crypto_display = []
        for i, (symbol, display) in enumerate(C.TICKER_PAIRS[:5]):
            self.coin = CryptoTicker(self.crypto_frame, symbol, display)

            # Customize to fit main dashboard
            self.coin.border.configure(bg=C.BACKGROUND)
            self.coin.border.config(width=140, height=75)
            self.coin.border.propagate(False)
            self.coin.price_label.pack_configure(pady=0)
            self.coin.border.pack(
                pady=7, padx=11, side=tk.LEFT, fill=tk.X, expand=True)
            self.coin.title.config(
                font=("Arial", 10), background='black', anchor="center")
            self.coin.title.pack_configure(fill="x")
            self.coin.price_label.config(font=("Arial", 14))
            self.coin.change_label.config(font=("Arial", 8))

            self.main_crypto_display.append(self.coin)

            # Create button to change main coin
            self.btn = tk.Button(self.coin.frame, text="►", font=("Arial", 6),
                                 bg=C.BUTTON_BG, fg=C.BUTTON, command=lambda d=display: change(d))
            self.btn.place(x=4, y=52)

        # Start all coin
        print("Starting Main Crypto Price Connection")
        for i in self.main_crypto_display:
            i.start()