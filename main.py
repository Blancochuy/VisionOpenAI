# main.py
import tkinter as tk
from gui.gui_handler import GUIHandler

def main():
    root = tk.Tk()
    app = GUIHandler(root)
    root.mainloop()

if __name__ == "__main__":
    main()
