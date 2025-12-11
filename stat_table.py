from setup import *


class Statistics:
    def __init__(self, parent, current):
        self.root = parent
        self.symbol = self.symbol = current.lower().replace("/", "")

        # Setup url
        self.last_trade_ws = f"{self.symbol}@trade"
        self.current_ticker_ws = f"{self.symbol}@ticker"
        self.kline1h = f"{self.symbol}@kline_1h"
        self.best_bid_ask_ws = f"{self.symbol}@bookTicker"
        # Combine 3 urls in one var
        self.multi_url = f"wss://stream.binance.com:9443/stream?streams={self.last_trade_ws}/{self.current_ticker_ws}/{self.kline1h}/{self.best_bid_ask_ws}"
        print(f"Generated Multi-URL: {self.multi_url}")
        # Create table
        self.table = tk.Frame(self.root, bg=TABLE_BG, height=200)
        self.table.propagate(False)
        self.table.pack(pady=10, padx=10, fill="x")
        self.table.grid_columnconfigure(0, minsize=100)
        self.table.grid_columnconfigure(1, weight=1)

        # Every Data in table
        data_structure = [
            ("Last Traded Price",   "00,000.00",    "last_trade_price"),
            ("24H Change",          "+-0.00%",      "change24"),
            ("24H Volume",          "00.00M",       "vol24"),
            ("1H Change",           "+-0.00%",      "change1"),
            ("1H Volume",           "00.00B",       "vol1"),
            ("Market Cap",          "0,000.00B",    "market_cap"),
            ("Best Bid",            "00,000.00",    "best_bid"),
            ("Best Ask",            "00,000.00",    "best_ask"),
        ]

        # Loop to create label
        for row, (name, val, var) in enumerate(data_structure):

            # First Column for name of each data
            name_label = tk.Label(self.table, text=name,
                                  font=("Arial", 7), fg=PURPLE, bg=TABLE_BG)
            name_label.grid(row=row, column=0, sticky="w")

            # Second column for value
            value_label = tk.Label(self.table, text=val,
                                   font=("Arial", 7), fg=WHITE, bg=TABLE_BG)
            value_label.grid(row=row, column=1, sticky="e")

            # Use setattr to create variable for label
            setattr(self, var, name_label)
            setattr(self, f"{var}2", value_label)

        self.start()

        # Start market cap
        self.marketcap()

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.multi_url,
            on_message=self.on_message,
            on_error=lambda ws, err: print(f"{self.symbol} error: {err}"),
            on_close=lambda ws, s, m: print(f"{self.symbol} closed"),
            on_open=lambda ws: print(f"{self.symbol} connected"))

        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def on_message(self, ws, message):
        data = json.loads(message)
        name = data['stream']
        stream_data = data['data']

        # Check name of each api for call different on_message
        if name == f"{self.symbol}@trade":
            self.on_message1(ws, stream_data)
        elif name == f"{self.symbol}@ticker":
            self.on_message2(ws, stream_data)
        elif name == f"{self.symbol}@kline_1h":
            self.on_message3(ws, stream_data)
        elif name == f"{self.symbol}@bookTicker":
            self.on_message4(ws, stream_data)

    def on_message1(self, ws, data):
        self.last_trade_price2.config(text=f"{float(data['p']):.2f}")

    def on_message2(self, ws, data):
        # 24h change
        self.change242.config(text=f"{float(data['P']):.2f}%")
        # Change colors
        if float(data['P']) < 0:
            self.change242.config(fg=RED)
        else:
            self.change12.config(text=f"+{float(data['P']):.2f}%", fg=GREEN)

        # 24h volume
        self.vol242.config(text=f"{float(data['q'])/1000000:.2f}M")

    def on_message3(self, ws, data):
        # 1H change
        kline = data['k']
        open_price = float(kline['o'])
        close_price = float(kline['c'])

        # Calculate 1h change
        change1hour = ((close_price-open_price)*100)/open_price
        self.change12.config(text=f"{change1hour:.2f}%")
        # Change colors
        if change1hour < 0:
            self.change12.config(fg=RED)
        else:
            self.change12.config(text=f"+{change1hour:.2f}%", fg=GREEN)

        # 1H volume
        self.vol12.config(text=f"{float(kline['q'])/1000000:.2f}M")

    def on_message4(self, ws, data):
        # Best bid price
        self.best_bid2.config(text=f"{float(data['b']):.2f}")

        # Best ask price
        self.best_ask2.config(text=f"{float(data['a']):.2f}")

    def marketcap(self):
        # Market cap data from REST API coingecko.com
        self.url = 'https://api.coingecko.com/api/v3/coins/markets'

        # Map coin format
        self.coin_ids = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "XRP": "ripple",
            "BNB": "binancecoin",
            "SOL": "solana"
        }
        for i in self.coin_ids:
            if self.symbol.replace("usdt", "").upper() == i:
                self.coin_id = self.coin_ids[i]
                break

        parameters = {
            'vs_currency': 'usd',
            'ids': self.coin_id,
            'order': 'market_cap_desc',
            'per_page': 1,
            'page': 1,
            'sparkline': 'false'
        }

        # request data from coingecko
        response = requests.get(self.url, params=parameters)
        data = response.json()
        market_cap = data[0]["market_cap"]

        # Display market 1 time when start program
        self.market_cap2.config(text=f"{float(market_cap)/1000000000:.2f}B")
