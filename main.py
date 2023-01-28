import tkinter as tk
from tkinter import ttk

# code derived from: https://docs.python.org/3/library/tkinter.html#a-hello-world-program
def test_window():
    window = tk.Tk()
    frame = ttk.Frame(window, padding=10)

    frame.grid()
    
    ttk.Label(frame, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frame, text="Quit", command=window.destroy).grid(column=1, row=0)

    window.mainloop()


if __name__ == "__main__":
    test_window()