from setup import *
from orderbook import OrderBookSnapshot
from stat_table import Statistics
from crypto_price import CryptoTicker
from overall_crypto_price import Overall_price


class MainDashBoard:
    def __init__(self, root):
        self.current = "BTC/USDT"  # Starting Program with BTC/USDT
        self.root = root
        self.root.title("Crypto Dashboard")
        self.root.geometry("1000x600")
        self.root.configure(bg=BACKGROUND)

        # Title
        self.frame = tk.Frame(root, bg=MAIN_BG)
        self.frame.pack(fill="x")

        self.Title = tk.Label(self.frame, bg=MAIN_BG, text=" DashBoard",
                              font=("Arial", 30), fg='white')
        self.Title.pack(side=tk.LEFT)
        self.current_dashboard = tk.Label(self.frame, bg=MAIN_BG, text=self.current,
                                          font=("Arial", 13), fg='white')
        self.current_dashboard.pack(side=tk.LEFT, pady=(18, 0))

        # Left Menu
        self.frame2 = tk.Frame(root, bg=MAIN_BG)
        self.frame2.pack(pady=1, side=tk.LEFT, fill="y")

        # Order book table
        self.orderbook = OrderBookSnapshot(self.frame2, self.current)

        # Stat table
        self.stat = Statistics(self.frame2, self.current)

# Main Crypto Price Part

        # Main crypto Price
        self.main_crypto = [
            ("BTCUSDT", "BTC/USDT"), ("ETHUSDT", "ETH/USDT"),
            ("XRPUSDT", "XRP/USDT"), ("BNBUSDT", "BNB/USDT"),
            ("SOLUSDT", "SOL/USDT"),
        ]

        # Create frame
        self.crypto_frame = tk.Frame(self.root,relief="solid",bg=BACKGROUND)
        self.crypto_frame.pack(side='top', fill='x', padx=10, pady=10)
        
        # Create crypto price
        self.button = []
        for i,(symbol,display) in enumerate(self.main_crypto):
            self.coin = CryptoTicker(self.crypto_frame, symbol, display)

            # Customize to fit main dashboard
            self.coin.border.configure(bg=BACKGROUND)
            self.coin.border.config(width=140,height=75)
            self.coin.border.propagate(False)
            self.coin.price_label.pack_configure(pady=0)
            self.coin.border.pack(pady=7,padx=11,side=tk.LEFT,fill=tk.X,expand=True)
            self.coin.title.config(font=("Arial", 10))
            self.coin.price_label.config(font=("Arial", 14))
            self.coin.change_label.config(font=("Arial",8))
            self.coin.start()

            # Create button to change main coin
            self.btn = tk.Button(self.coin.frame,text="►",font=("Arial",6),
                                 bg=BUTTON_BG,fg=BUTTON,command=lambda d=display: self.change_main_coin(d))
            self.btn.place(x=4,y=52)

        # Candle stick Frame
        self.candle_stick_frame = tk.Frame(self.root,bg=MAIN_BG)
        self.candle_stick_frame.pack(side=tk.LEFT,fill=tk.BOTH,padx=21,pady=(0,20),expand=True)

        # Overall Price table
        self.overall_price = Overall_price(self.root)

    def change_main_coin(self,symbol):
        self.current = symbol

        # Update
        self.current_dashboard.config(text=self.current)
        self.orderbook.change_symbol(self.current)
        self.stat.change_symbol(self.current)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainDashBoard(root)
    root.mainloop()
