Project for HCIRA, Spring '23

We have used the tkinter package in our submission. This is a standard GUI toolkit used in Python. 
We created a program in Python which accomplishes the following tasks. 

  a. Instantiation of Blank Canvas: 
  Lines 30-34 performs the action for instantiating a blank canvas set within a window. the mainloop() function on line 42 starts the application.
    
  b. Drawing on canvas:
  The draw_line() method on line 10 is used for drawing lines on the created canvas. It takes an event object as a parameter, which includes data like cursor position.

  c. Listening for Mouse or Touch Events:
  Lines 38-41 attach various functions to event listeners using the bind() function. Details about what each event is and what happens on each event are described in comments.

  d. Clearing the canvas:
  The clear_canvas() method on line 25 clears the canvas of all geometry and marks, which in our case is the various line segments added to the canvas in the draw_line() function.

  
