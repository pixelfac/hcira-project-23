import tkinter as tk
import numpy as np
import preprocess_dollar_one as dollar1
from preprocess_dollar_one import square_size, angle_range, angle_step, phi

"""
Project 1 for HCIRA, Spring '23

Group Members :
Aravind S
Nathan Harris
Shashanka Bhat

Description:
This file creates and controls the application window that
the user interacts with, recording gestures and outputting the results
of the implemented gesture recognition algorithms
"""


# Initialise coords list with first point
def init_coords(event):
    clear_canvas(event)
    coords.append([event.x, event.y])


# Draws on canvas
def draw_line(event):
    if canvas.old_coords:  # if canvas object has property 'old_coords'
        x1, y1 = canvas.old_coords
        canvas.create_line(event.x, event.y, x1, y1)
        # canvas.itemconfig(label_current_coord, text="Current coordinate: x=" + str(event.x) + ", y=" + str(event.y))
        label_current_coord["text"] = "Current coordinate: x=" + str(event.x) + ", y=" + str(event.y)
    coords.append([event.x, event.y])
    canvas.old_coords = event.x, event.y


# Reset the last coordinate after mouse release
def reset_canvas_coords(event):
    canvas.old_coords = None
    # print(len(coords))


def process_line(event):
    reset_canvas_coords(event)

    # $1 algorithm
    template, score = dollar1.recognize(coords, 64, angle_range=angle_range, angle_step=angle_step,
                                        phi=phi, square_size=square_size)
    label_recognised_candidate["text"] = "Recognized Label: " + template.label + ", score: " + str(score)


# Clear the canvas
def clear_canvas(event):
    canvas.delete('all')  # delete all objects on canvas
    coords.clear()  # empty coords list


win = tk.Tk()  # init window
win.geometry("600x600")  # set window dimensions

# Canvas
canvas = tk.Canvas(win, width=600, height=400, highlightthickness=1, highlightbackground="black")
# place adds canvas to parent (window), and also can adjust scaling/sizing relative to parent
canvas.place(relx=0.5, rely=0.5, anchor="center")
canvas.old_coords = None
coords = []  # store coordinates

# Labels
label_left_click = tk.Label(text="Click left mouse button to start drawing on canvas. Drag to draw gesture")
label_left_click.place(y=5, x=0)
label_right_click = tk.Label(text="Click right mouse button to clear the canvas")
label_right_click.place(y=25, x=0)
label_current_coord = tk.Label(text="")
label_current_coord.place(y=45, x=0)
label_recognised_candidate = tk.Label(text="")
label_recognised_candidate.place(y=65, x=0)

win.title("$1 gesture recognition")
win.bind('<ButtonPress-1>', init_coords)  # on LeftClick, prepare for line drawing
win.bind('<B1-Motion>', draw_line)  # when LeftClick is held and mouse is moving, call draw_line() function
win.bind('<ButtonRelease-1>', process_line)  # resets line drawing variables
win.bind('<ButtonPress-3>', clear_canvas)  # on RightClick, clear canvas and coords list
win.bind('<space>', process_line)  # On pressing space bar, recognise the gesture

win.mainloop()  # start main event loop
