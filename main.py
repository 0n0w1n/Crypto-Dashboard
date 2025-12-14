import tkinter as tk
from main_dashboard import MainDashBoard
from utils.storage import load_set,save_settings

# Run Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = MainDashBoard(root, load_set, save_settings)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
