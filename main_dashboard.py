from setup import *
from orderbook import OrderBookSnapshot
from stat_table import Statistics


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


if __name__ == "__main__":
    root = tk.Tk()
    app = MainDashBoard(root)
    root.mainloop()
