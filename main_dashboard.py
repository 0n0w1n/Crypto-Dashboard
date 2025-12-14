# Import conponents
from components.orderbook import OrderBookSnapshot
from components.stat_table import Statistics
from components.crypto_price import CryptoTicker
from components.main_crypto_price import MainCryptoPrice
from components.overall_crypto_price import Overall_price
from components.candle_stick import CandleStick

# Tkinter
import tkinter as tk

import config as C


class MainDashBoard:
    def __init__(self, root, load, save):
        self.load = load
        self.save = save
        self.current = load["current"]
        self.root = root
        self.root.title("Crypto Dashboard")
        self.root.geometry("1000x600")
        self.root.configure(bg=C.BACKGROUND)

        print("\nStarting Websocket Connection")  # Starting text

        # Title
        self.frame = tk.Frame(root, bg=C.MAIN_BG)
        self.frame.pack(fill="x")

        self.Title = tk.Label(self.frame, bg=C.MAIN_BG, text=" DashBoard",
                              font=("Arial", 30), fg='white')
        self.Title.pack(side=tk.LEFT)
        self.current_dashboard = tk.Label(self.frame, bg=C.MAIN_BG, text=self.current,
                                          font=("Arial", 13), fg='white')
        self.current_dashboard.pack(side=tk.LEFT, pady=(18, 0))

        # Left Menu Frame
        self.frame2 = tk.Frame(root, bg=C.MAIN_BG)
        self.frame2.pack(pady=1, side=tk.LEFT, fill="y")

        # Order book table
        self.orderbook = OrderBookSnapshot(self.frame2, self.current,
                                           load["current_order"], load["current_show"])

        # Stat table
        self.stat = Statistics(self.frame2, self.current)

        # Main Crypto Price
        self.crypto_frame = tk.Frame(
            self.root, relief="solid", bg=C.BACKGROUND)
        self.crypto_frame.pack(side='top', fill='x', padx=10, pady=10)

        self.main_crypto_display = MainCryptoPrice(
            self.crypto_frame, self.change_main_coin,self.current)

        # Candle stick Frame
        self.candle_stick_frame = tk.Frame(self.root, bg=C.MAIN_BG)
        self.candle_stick_frame.pack(
            side=tk.LEFT, fill=tk.BOTH, padx=21, pady=(0, 20), expand=True)
        self.candle_stick_frame.propagate(False)
        self.candle_stick = CandleStick(
            self.candle_stick_frame, self.current, load['interval'])
        self.candle_stick.pack(fill=tk.BOTH, expand=True)

        # Overall Price table
        self.overall_price = Overall_price(self.root,self.button_overall,load)

        # Button for show overall price
        self.show_overall = tk.Button(
            self.candle_stick.btn_frame, text="☰",
            command=self.overall_price.show, bg=C.BUTTON_BG, fg=C.BUTTON)
        
        # load save for overall price open or not
        if self.overall_price.oc == 0:
            self.overall_price.hide()            
        
    def button_overall(self,state):
        if state == "on":
            self.show_overall.place(relx=1,rely=0,anchor="ne")
        else:
            self.show_overall.place_forget()

    # Changing main coin from main crypto price button
    def change_main_coin(self, symbol):
        print("\n--Changing Main coin--")
        self.old = self.current
        self.current = symbol

        # Update button in use
        self.main_crypto_display.button_update(self.current,self.old,self.change_main_coin)

        # Update
        self.current_dashboard.config(text=self.current)
        self.orderbook.change_symbol(self.current)
        self.stat.change_symbol(self.current)
        self.candle_stick.change_interval(self.current)

        print(f"--Change Main coin to {self.current}--")

    def on_closing(self):
        print("\nStopping all WebSocket connections...")  # Stoping Text
        # Save Setting before close
        self.save({
            "current": self.current,
            "interval": self.candle_stick.interval,
            "current_order": self.orderbook.current_order_book,
            "current_show": self.orderbook.show,
            "overall": self.overall_price.oc,
            "full_price": self.overall_price.app.oc,
        })

        # Closing another window First
        try:  # use try in case that naver open it
            if self.overall_price.app.is_active == True:
                self.overall_price.app.on_closing()
        except:
            pass

        # Closing every websocket
        self.orderbook.on_closing()
        self.stat.on_closing()
        self.overall_price.on_closing()
        print("Stopping Main Crypto Price Connection")
        for ticker in self.main_crypto_display.main_crypto_display:
            ticker.stop()
        self.candle_stick.on_closing()

        self.root.destroy()
