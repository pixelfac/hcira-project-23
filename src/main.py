import tkinter as tk
from unistroke import templates
import preprocess_dollar_one as dollar1


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
def reset_canvas_coords():
    canvas.old_coords = None
    print(len(coords))


def process_line(event):
    reset_canvas_coords()
    
    # $1 algoritmh
    template, score = dollar1.recognize(coords, 64) # 64 is arbitrary

    print (template.label)
    print(score)

    


# Clear the canvas
def clear_canvas(event):
    canvas.delete('all') # delete all objects on canvas
    coords.clear()       # empty coords list  


win = tk.Tk()            # init window
win.geometry("400x400")  # set window dimensions

canvas = tk.Canvas(win, width=400, height=400)
canvas.pack()  # pack adds canvas to parent (window), and also can adjust scaling/sizing relative to parent
canvas.old_coords = None
coords = []  # store coordinates

win.bind('<ButtonPress-1>', init_coords)    # on LeftClick, prepare for line drawing
win.bind('<B1-Motion>', draw_line)          # when LeftClick is held and mouse is moving, call draw_line() function
win.bind('<ButtonRelease-1>', process_line) # resets line drawing variables
win.bind('<ButtonPress-3>', clear_canvas)   # on RightClick, clear canvas and coords list
win.mainloop() # start main event loop
# print(coords)
