import tkinter as tk
from tkinter import ttk

def main():
    window = tk.Tk()
    frame = ttk.Frame(window, padding=10)
    frame.grid()
    
    ttk.Label(frame, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frame, text="Quit", command=window.destroy).grid(column=1, row=0)

    window.mainloop()


if __name__ == "__main__":
    main()