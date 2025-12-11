from setup import *


class OrderBookSnapshot:
    def __init__(self,parent,current):
        self.root = parent
        self.current_order_book = "BID (BUYS)" # Set default
        self.show = "ASK (SELLS)" # Set default

        self.order = tk.Label(self.root,bg=INNER_BG, text="Order Book Snapshot",font=("Arial",10),fg='white')
        self.order.pack(padx=20,pady=(0,5))

        self.title = tk.Button(self.root ,command=self.ask_bid,text=f"▶ {self.show}",font=("Arial",8),bg=INNER_BG, fg='white')
        self.title.pack(side=tk.TOP)

        self.hl = tk.Label(self.root,text="HIGH → LOW",bg=MAIN_BG,fg=WHITE,font=("Arial",8))
        self.hl.pack(anchor="nw")

        # Top 10 BID/ASK table
        self.table = tk.Frame(self.root,bg=TABLE_BG,height=235)
        self.table.propagate(False)
        self.table.pack(padx=10,fill="x")

        self.tablename = tk.Label(self.table,text=self.current_order_book,bg=TABLE_BG,fg=WHITE,font=("Arial",12))
        self.tablename.pack(padx=10,fill="x")
        self.line = tk.Label(self.table,text="━"*11,fg=WHITE,background=TABLE_BG)
        self.line.place(x=6,y=15)

        self.colname = tk.Label(self.table,text=f"{"Price":<20} Quantity",font=("Arial",10),fg=WHITE,bg=TABLE_BG)
        self.colname.pack(pady=5)

        # Arrange layer
        self.tablename.tkraise()

        # Data
        self.symbol = current.lower().replace("/","")
        self.ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@depth10"
        self.start()
        self.data = []
        for _ in range(10):
            lbl = tk.Label(self.table,text=f"{f"---,--":<33} ---,--", bg=TABLE_BG, font=("Arial", 7), fg=WHITE)
            self.data.append(lbl)
            lbl.pack()

    def on_message(self,ws,message):
        # Incoming Order Book data and updates the list
        data = json.loads(message)

        # Update in list
        if self.current_order_book == "BID (BUYS)":
            bids_sells = data['bids']
        elif self.current_order_book == "ASK (SELLS)":
            bids_sells =data['asks']

        self.bid_sell = [[float(y) for y in x] for x in bids_sells[:10]]

        for i,lbl in enumerate(self.data):
            lbl.config(text=f"{self.bid_sell[i][0]:<33.2f} {self.bid_sell[i][1]:.2f}")

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self.on_message,
            on_error=lambda ws, err: print(f"{self.symbol} error: {err}"),
            on_close=lambda ws, s, m: print(f"{self.symbol} closed"),
            on_open=lambda ws: print(f"{self.symbol} connected"))
        
        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    # Switch between ask and bid
    def ask_bid(self):
        if self.current_order_book == "BID (BUYS)":
            self.show = "BID (BUYS)"
            self.current_order_book = "ASK (SELLS)"
            self.hl_text = "LOW → HIGH"
        elif self.current_order_book == "ASK (SELLS)":
            self.show = "ASK (SELLS)"
            self.current_order_book = "BID (BUYS)"
            self.hl_text = "HIGH → LOW"
        self.update(self.show,self.hl_text)

    def update(self,show,hl):
        self.title.config(text=f"▶ {show}")
        self.tablename.config(text=self.current_order_book)
        self.hl.config(text=hl)
