from tkinter import ttk

def draw_line(event):
    if canvas.old_coords: # if canvas object has property 'old_coords'
        x1, y1 = canvas.old_coords
        canvas.create_line(event.x, event.y, x1, y1)
    canvas.old_coords = event.x, event.y

win = tk.Tk()           # init window
win.geometry("400x400") # set window dimensions

canvas = tk.Canvas(win, width=400, height=400)
canvas.pack() # pack adds canvas to parent (window), and also can adjust scaling/sizing relative to parent
canvas.old_coords = None



win.bind('<ButtonPress-1>', draw_line)
win.mainloop()
