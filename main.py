import tkinter as tk
from interface import Interface


def main():
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()