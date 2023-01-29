import tkinter as tk


# Initialise coords list with first point
def init_coords(event):
    coords.append([event.x, event.y])


# Draws on canvas
def draw_line(event):
    if canvas.old_coords: # if canvas object has property 'old_coords'
        x1, y1 = canvas.old_coords
        canvas.create_line(event.x, event.y, x1, y1)
    coords.append([event.x, event.y])
    canvas.old_coords = event.x, event.y


# Reset the last coordinate after mouse release
def reset_canvas_coords(event):
    canvas.old_coords = None
    print(len(coords))


# Clear the canvas
def clear_canvas(event):
    canvas.delete('all')
    coords.clear()


win = tk.Tk()            # init window
win.geometry("400x400")  # set window dimensions

canvas = tk.Canvas(win, width=400, height=400)
canvas.pack()  # pack adds canvas to parent (window), and also can adjust scaling/sizing relative to parent
canvas.old_coords = None
coords = []  # store coordinates

win.bind('<ButtonPress-1>', init_coords)
win.bind('<B1-Motion>', draw_line)
win.bind('<ButtonRelease-1>', reset_canvas_coords)
win.bind('<ButtonPress-3>', clear_canvas)
win.mainloop()
# print(coords)
