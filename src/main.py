import tkinter as tk
from preprocess_dollar_one import recognize
from next_button import get_current_shape
from output_util import save_to_xml
import time
from templates import templates
from preprocess_dollar_one import preprocess_points_example


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

# global variables
DATA_COLLECTION_MODE = True
DATA_COLLECTION_USER = 'demo'

current_shape_number = 1
current_sample_number = 1
total_gestures = 16
total_sample_size = 2

total_gestures = 16
total_sample_size = 2


# Initialise coords list with first point
def init_coords(event):
    # clear_canvas(event)
    clear_canvas()
    current_time = int(round(time.time() * 1000))
    coords.append([event.x, event.y, current_time])


# Draws on canvas
def draw_line(event):
    if canvas.old_coords:  # if canvas object has property 'old_coords'
        x1, y1 = canvas.old_coords
        canvas.create_line(event.x, event.y, x1, y1)
        # canvas.itemconfig(label_current_coord, text="Current coordinate: x=" + str(event.x) + ", y=" + str(event.y))
        label_current_coord["text"] = "Current coordinate: x=" + str(event.x) + ", y=" + str(event.y)
    current_time = int(round(time.time() * 1000))
    coords.append([event.x, event.y, current_time])

    canvas.old_coords = event.x, event.y


def draw_line_temp_canvas():
    # if canvas.old_coords:  # if canvas object has property 'old_coords'
    #     x1, y1 = canvas.old_coords
    #     canvas.create_line(event.x, event.y, x1, y1)
    #     # canvas.itemconfig(label_current_coord, text="Current coordinate: x=" + str(event.x) + ", y=" + str(event.y))
    #     label_current_coord["text"] = "Current coordinate: x=" + str(event.x) + ", y=" + str(event.y)
    # current_time = int(round(time.time() * 1000))
    # coords.append([event.x, event.y, current_time])
    # canvas.old_coords = event.x, event.y
    points = []
    for t in templates:
        if t.label == get_current_shape(current_shape_number):
            points = t.points
    points = preprocess_points_example(points)
    lines = [(points[n][0], points[n][1]) for n in range(0, len(points))]
    canvas_temp.create_line(lines)


def draw_line_temp_canvas():
    # if canvas.old_coords:  # if canvas object has property 'old_coords'
    #     x1, y1 = canvas.old_coords
    #     canvas.create_line(event.x, event.y, x1, y1)
    #     # canvas.itemconfig(label_current_coord, text="Current coordinate: x=" + str(event.x) + ", y=" + str(event.y))
    #     label_current_coord["text"] = "Current coordinate: x=" + str(event.x) + ", y=" + str(event.y)
    # current_time = int(round(time.time() * 1000))
    # coords.append([event.x, event.y, current_time])
    # canvas.old_coords = event.x, event.y
    points = []
    for t in templates:
        if t.label == get_current_shape(current_shape_number):
            points = t.points
    points = preprocess_points_example(points)
    lines = [(points[n][0], points[n][1]) for n in range(0, len(points))]
    canvas_temp.create_line(lines)


# Reset the last coordinate after mouse release
def reset_canvas_coords(event):
    canvas.old_coords = None
    # print(len(coords))


def process_line(event):
    reset_canvas_coords(event)
    if len(coords) < 2:
        return
    
    # if we're collecting data
    if DATA_COLLECTION_MODE:
        return
    if len(coords) < 2:
        return
    
    # if we're collecting data
    if DATA_COLLECTION_MODE:
        return

    # $1 algorithm
    template, score = recognize(coords, 64)
    label_recognised_candidate["text"] = "Recognized Label: " + template.label + ", score: " + str(score)


# Clear the canvas
def clear_canvas():
    print("CLEARING")
    canvas.delete('all')  # delete all objects on canvas
    coords.clear()  # empty coords list


# process to next sample
def go_next_sample():
    global current_sample_number
    global current_shape_number
    global label_gesture_prompt

    draw_line_temp_canvas()

    # save current drawing
    current_shape = get_current_shape(current_shape_number)
    save_to_xml(coords, current_shape, DATA_COLLECTION_USER, current_sample_number)

    print(current_sample_number)
    current_sample_number = current_sample_number + 1
    label = f'Please draw the following shape : {current_shape}. Sample number: {current_sample_number}'
    label_gesture_prompt.config(text=label)

    # if reached end of samples
    if current_sample_number == total_sample_size + 1:
        next_button["state"] = "disabled"
        next_gesture_button["state"] = "normal"
        label_gesture_prompt.config(text="Click 'Next Gesture'")
        # return

    # if reached end of samples
    if current_sample_number == total_sample_size + 1:
        next_gesture_button["state"] = "normal"
        print(str(current_shape_number))
        if current_shape_number == 16:
            label_gesture_prompt.config(text="All done!! Thank you!")
            next_button["state"] = "disabled"
            next_gesture_button["state"] = "disabled"
        else:
            label_gesture_prompt.config(text="Click 'Next Gesture'")
        return
    clear_canvas()


def next_gesture_button_handle():
    global current_sample_number
    global current_shape_number
    global label_gesture_prompt

    # iterate data tracking variables
    current_shape_number = current_shape_number + 1
    current_shape = get_current_shape(current_shape_number)
    current_sample_number = 1

    # reset buttons
    next_button["state"] = "normal"
    next_gesture_button["state"] = "disabled"

    label = f'Please draw the following shape : {current_shape}. Sample number: {current_sample_number}'
    label_gesture_prompt.config(text=label)
    clear_canvas()
    canvas_temp.delete('all')
    label_example_text = f'Example gesture: {current_shape}'
    label_example.config(text=label_example_text)
    draw_line_temp_canvas()

###################
# Program Start ##
###################



win = tk.Tk()  # init window
win.geometry("1000x600")  # set window dimensions


# Canvas
canvas = tk.Canvas(win, width=400, height=400, highlightthickness=1, highlightbackground="black")
# place adds canvas to parent (window), and also can adjust scaling/sizing relative to parent
canvas.place(relx=0.76, rely=0.5, anchor="center")
canvas.old_coords = None
coords = []  # store coordinates

canvas_temp = tk.Canvas(win, width=400, height=400, highlightthickness=1, highlightbackground="black")
# place adds canvas to parent (window), and also can adjust scaling/sizing relative to parent
canvas_temp.place(relx=0.255, rely=0.5, anchor="center")

# Labels
label_left_click = tk.Label(text="Click left mouse button to start drawing on canvas. Drag to draw gesture")
label_left_click.place(y=5, x=0)

label_right_click = tk.Label(text="Click right mouse button to clear the canvas")
label_right_click.place(y=25, x=0)

label_current_coord = tk.Label(text="")
label_current_coord.place(y=45, x=0)

if DATA_COLLECTION_MODE:
    # for data collection
    label_gesture_prompt = tk.Label(text='Please draw the following shape : {}. Sample number: {}'.format(get_current_shape(1), current_sample_number))
    label_gesture_prompt.place(y=70, x=600)
    label_example = tk.Label(text='Example gesture: {}'.format(get_current_shape(1)))
    label_example.place(y=70, x=150)
    draw_line_temp_canvas()
else:
    # for live recognition
    label_recognised_candidate = tk.Label(text="")
    label_recognised_candidate.place(y=65, x=0)

win.title("$1 gesture recognition")

######################
# creating buttons
######################

# button to add next sample
next_button = tk.Button(win, text="Next", fg="red", state="normal", command=go_next_sample, height=1, width=10)
next_button.place(y=520, x=410)

# button to prompt next gesture
next_gesture_button = tk.Button(win, text="Next Gesture", fg="red", state="disabled", command=next_gesture_button_handle)
next_gesture_button.place(y=560, x=460)

# button to reset the canvas
reset_button = tk.Button(win, text="Reset Canvas", fg="red", command=clear_canvas)
reset_button.place(y=520, x=510)

# set keybinds
canvas.bind('<ButtonPress-1>', init_coords)  # on LeftClick, prepare for line drawing
canvas.bind('<B1-Motion>', draw_line)  # when LeftClick is held and mouse is moving, call draw_line() function
canvas.bind('<ButtonRelease-1>', process_line)  # resets line drawing variables
# win.bind('<ButtonPress-3>', clear_canvas)  # on RightClick, clear canvas and coords list
# win.bind('<space>', process_line)  # On pressing space bar, recognise the gesture

win.mainloop()  # start main event loop


#
# # Testing methods
# win_res = tk.Tk()  # init window
# win_res.geometry("400x400")  # set window dimensions
#
# # Canvas
# canvas_res = tk.Canvas(win_res, width=400, height=400, highlightthickness=1, highlightbackground="black")
# # place adds canvas to parent (window), and also can adjust scaling/sizing relative to parent
# canvas_res.place(relx=0.5, rely=0.5, anchor="center")
# canvas_res.old_coords = None
# coords_res = dollar1.resample_points(coords, 64)
# line_res = [(coords_res[n][0], coords_res[n][1]) for n in range(0, len(coords_res))]
# canvas_res.create_line(line_res)
# win_res.mainloop()

# win_rot = tk.Tk()  # init window
# win_rot.geometry("400x400")  # set window dimensions
#
# # Canvas
# canvas_rot = tk.Canvas(win_rot, width=400, height=400, highlightthickness=1, highlightbackground="black")
# # place adds canvas to parent (window), and also can adjust scaling/sizing relative to parent
# canvas_rot.place(relx=0.5, rely=0.5, anchor="center")
# canvas_rot.old_coords = None
# coords_rot = dollar1.rotate_to_zero(coords)
# line_rot = [(coords_rot[n][0], coords_rot[n][1]) for n in range(0, len(coords_rot))]
# canvas_rot.create_line(line_rot)
# win_rot.mainloop()

# win_sc = tk.Tk()  # init window
# win_sc.geometry("400x400")  # set window dimensions
#
# # Canvas
# canvas_sc = tk.Canvas(win_sc, width=400, height=400, highlightthickness=1, highlightbackground="black")
# # place adds canvas to parent (window), and also can adjust scaling/sizing relative to parent
# canvas_sc.place(relx=0.5, rely=0.5, anchor="center")
# canvas_sc.old_coords = None
# coords_sc = dollar1.scale_to_square(coords, 300)
# line_sc = [(coords_sc[n][0], coords_sc[n][1]) for n in range(0, len(coords_sc))]
# canvas_sc.create_line(line_sc)
# win_sc.mainloop()
