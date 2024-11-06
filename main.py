# main.py
from wrestling_matchup.gui import WrestlingMatchUpApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = WrestlingMatchUpApp(root)
    root.mainloop()  
