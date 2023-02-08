import tkinter as tk
from unistroke import templates
import preprocess_dollar_one as dollar1


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
    canvas.delete('all')  # delete all objects on canvas
    coords.clear()  # empty coords list


def recognise_gesture(event):
    """

    :param event:
    :return:
    """

    # perform preprocessing
    if not coords:
        return
    resampled_points = dollar1.resample_points(coords, n=64)
    rotated_points = dollar1.rotate_to_zero(resampled_points)
    # scaled_and_translated_points = scale_and_translate(rotated_points)
    # label, score = recognise(coords)
    label = "Rectangle"
    score = "0.9"
    label_recognised_candidate["text"] = "Predicted Label: " + label + ", score: " + score


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

win.title("Hello world")
win.bind('<ButtonPress-1>', init_coords)  # on LeftClick, prepare for line drawing
win.bind('<B1-Motion>', draw_line)  # when LeftClick is held and mouse is moving, call draw_line() function
win.bind('<ButtonRelease-1>', reset_canvas_coords)  # resets line drawing variables
win.bind('<ButtonPress-3>', clear_canvas)  # on RightClick, clear canvas and coords list
win.bind('<space>', recognise_gesture)  # On pressing space bar, recognise the gesture

win.mainloop()  # start main event loop
# print(coords)

# new_points = resample_points(coords, 64)
# print(len(new_points))
# rotated_points = rotate_to_zero(new_points)
# lines = [(rotated_points[n][0], rotated_points[n][1]) for n in range(0, len(rotated_points))]
#
#
# # Test the new points on a new canvas
#
# # lines = [(new_points[n][0], new_points[n][1]) for n in range(0, len(new_points))]
# win2 = tk.Tk()            # init window
# win2.geometry("500x500")  # set window dimensions
# canvas = tk.Canvas(win2, width=500, height=500)
# canvas.pack()
# canvas.create_line(lines)
# win2.mainloop()
