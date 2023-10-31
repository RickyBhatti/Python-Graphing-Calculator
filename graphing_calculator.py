# Author: Ricky Bhatti
# License: GNU GPL v3
# Repository: https://github.com/RickyBhatti/Python-Graphing-Calculator
# Purpose: A simple graphing calculator. We ask the user for a origin point, and then render in the axis based off of that
#          origin point then the ticks related to the space between them determined by the user. After that, the user
#          can enter in a mathematical expression that will be rendered in on the graph just like a graphing calculator.
# Tested Python Version(s): 3.6.8, 3.7.4, 3.9.6
# Tested Operating System(s): Windows 10, Mac OS X, Fedora 26

# Example Usage:
# Enter pixel coordinates of origin: 400,300
# Enter ratio of pixels per step: 30
# Enter an arithmetic expression: x**2

# IMPORTS
from math import *
import turtle

# CONSTANTS
WIDTH, HEIGHT = 800, 600
WIDTH_HALF, HEIGHT_HALF = WIDTH / 2, HEIGHT / 2
TICK_LENGTH = 10  # Length of the ticks we'd like to render.
TICK_LENGTH_HALF = TICK_LENGTH / 2  # Half of the tick length so we can use this to render properly.
AXISCOLOR = "black"
COLORS = ["red", "green", "blue"]

#
#  Returns the screen (pixel based) coordinates of some (x, y) graph location base on configuration
#
#  Parameters:
#   xo, yo : the pixel location of the origin of the  graph
#   ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#   x, y: the graph location to change into a screen (pixel-based) location
#
#  Usage -> screen_coords(xo, yo, ratio, 1, 0)
#
#  Returns: (screenX, screenY) which is the graph location (x,y) as a pixel location in the window
#
def screen_coords(xo, yo, ratio, x, y):  # Finished.
    return (xo + (ratio * x), yo + (ratio * y))

#
#  Returns a string of the colour to use for the current expression being drawn
#  This colour is chosen based on which how many expression have previously been drawn
#  The counter starts at 0, the first or 0th expression, should be red, the second green, the third blue
#  then loops back to red, then green, then blue, again
#
#  Usage -> get_color(counter)
#
#  Parameters:
#  counter: an integer where the value is a count (starting at 0) of the expressions drawn
#
#  Returns: 0 -> "red", 1 -> "green", 2 -> "blue", 3 -> "red", 4 -> "green", etc.
#
def get_color(counter): 
    color_index = counter % len(COLORS)
    return COLORS[color_index]

#
#  Draw in the window an xaxis label (text) for a point at (screenX, screenY)
#  the actual drawing points will be offset from this location as necessary
#  Ex. for (x,y) = (1,0) or x-axis tick/label spot 1, draw a tick mark and the label 1
#
#  Usage -> draw_x_axis_label_tick(pointer, 1, 0, "1")
#
#  Parameters:
#  pointer: the turtle drawing object
#  screenX, screenY): the pixel screen location to drawn the label and tick mark for
#  text: the text of the label to draw
#
#  Returns: Nothing
#
def draw_x_axis_label_tick(pointer, screenX, screenY, text):
    pointer.penup()
    pointer.setpos(screenX, screenY - TICK_LENGTH_HALF)  # Setting the position to half the max tick length, before rendering the tick.
    pointer.pendown()
    pointer.goto(screenX, (screenY - TICK_LENGTH_HALF) + TICK_LENGTH)  # Drawing in the tick, with a specific length.
    pointer.penup()
    pointer.setpos(screenX, screenY - TICK_LENGTH - 8)  # Adjusting where we render the text, to account for font size.
    pointer.write(text, False, align="center")  # Rendering in the text
    pointer.penup()
    return

#
#  Draw in the window an yaxis label (text) for a point at (screenX, screenY)
#  the actual drawing points will be offset from this location as necessary
#  Ex. for (x,y) = (0,1) or y-axis tick/label spot 1, draw a tick mark and the label 1
#
#  Usage -> draw_y_axis_label_tick(pointer, 0, 1, "1")
#
#  Parameters:
#  pointer: the turtle drawing object
#  screenX, screenY): the pixel screen location to drawn the label and tick mark for
#  text: the text of the label to draw
#
#  Returns: Nothing
#
def draw_y_axis_label_tick(pointer, screenX, screenY, text):
    pointer.penup()
    pointer.setpos(screenX - TICK_LENGTH_HALF, screenY)  # Setting the position to half the max tick length, before rendering the tick.
    pointer.pendown()
    pointer.goto((screenX - TICK_LENGTH_HALF) + TICK_LENGTH, screenY)  # Drawing in the tick, with a specific length.
    pointer.penup()
    pointer.setpos(screenX - TICK_LENGTH - 2, screenY - 4)  # Adjusting where we render the text, to account for font size.
    pointer.write(text, False, align="center")  # Rendering in the text
    pointer.penup()
    return

#
#  Draw in the window an xaxis (secondary function is to return the minimum and maximum graph locations drawn at)
#
#  Usage -> draw_x_axis(pointer, xo, yo, ratio)
#
#  Parameters:
#  pointer: the turtle drawing object
#  xo, yo : the pixel location of the origin of the  graph
#  ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#
#  Returns: (xmin, ymin) where xmin is minimum x location drawn at and xmax is maximum x location drawn at
#
def draw_x_axis(pointer, xo, yo, ratio):
    pointer.penup()
    pointer.home()
    positiveX = WIDTH - xo  # We're finding the positive section pixels for calculations related to ticks and axis.
    negativeX = WIDTH - positiveX  # We're finding the negative section pixels for calculations related to ticks and axis.
    pointer.sety(yo)  # Set the Y coordinate to yo to draw the x-axis.
    pointer.pendown()
    pointer.setx(WIDTH)  # Set the X coordinate to WIDTH, so the Turtle goes to the right to render in the axis.
    pointer.penup()
    totalPositiveXTicks = floor(positiveX / ratio)
    totalNegativeXTicks = floor(negativeX / ratio)
    xmin, xmax = -totalNegativeXTicks, totalPositiveXTicks  # Returning the total positive and negative ticks for the x-axis.
    for i in range(totalNegativeXTicks):  # Looping through the totalNegativeXTicks.
        currentTick = i + 1
        draw_x_axis_label_tick(pointer, negativeX - (ratio * currentTick), yo, f"-{currentTick}")  # Render in the negative x tick.
    for i in range(totalPositiveXTicks):  # Looping through the totalPositiveXTicks.
        currentTick = i + 1
        draw_x_axis_label_tick(pointer, negativeX + (ratio * currentTick), yo, f"{currentTick}")  # Render in the positive x tick.
    pointer.home()
    return xmin, xmax

#
#  Draw in the window an yaxis 
#
#  Usage -> draw_y_axis(pointer, xo, yo, ratio)
#
#  Parameters:
#  pointer: the turtle drawing object
#  xo, yo : the pixel location of the origin of the  graph
#  ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#
#  Returns: Nothing
#
def draw_y_axis(pointer, xo, yo, ratio):
    pointer.penup()
    pointer.home()
    positiveY = HEIGHT - yo  # We're finding the positive section pixels for calculations related to ticks and axis.
    negativeY = HEIGHT - positiveY  # We're finding the negative section pixels for calculations related to ticks and axis.
    pointer.setx(xo)  # Set the X coordinate to xo to draw the y-axis.
    pointer.pendown()
    pointer.sety(HEIGHT)  # Set the Y coordinate to HEIGHT, so the Turtle goes to the top to render in the axis.
    pointer.penup()
    totalPositiveYTicks = floor(positiveY / ratio)  # Total x ticks by flooring (Don't want to round, want the lowest) positiveY / ratio, to find positive ticks.
    totalNegativeYTicks = floor(negativeY / ratio)  # Total x ticks by flooring (Don't want to round, want the lowest) negativeY / ratio, to find negative ticks.
    for i in range(0, totalNegativeYTicks):  # Looping through the totalNegativeYTicks.
        currentTick = i + 1
        draw_y_axis_label_tick(pointer, xo, negativeY - (ratio * currentTick), f"-{currentTick}")  # Render in the negative y tick.
    for i in range(0, totalPositiveYTicks):  # Looping through the totalPositiveYTicks.
        currentTick = i + 1
        draw_y_axis_label_tick(pointer, xo, negativeY + (ratio * currentTick), f"{currentTick}")  # Render in the positive y tick.
    pointer.home()
    return

#
#  Draw in the window the given expression (expr) between [xmin, xmax] graph locations
#
#  Usage -> draw_expr(pointer, xo, yo, ratio, xmin, xmax, expr)
#
#  Parameters:
#  pointer: the turtle drawing object
#  xo, yo : the pixel location of the origin of the  graph
#  ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#  expr: the expression to draw (assumed to be valid)
#  xmin, ymin : the range for which to draw the expression [xmin, xmax]
#
#  Returns: Nothing
#
def draw_expr(pointer, xo, yo, ratio, xmin, xmax, expr):
    pointer.penup()
    pointer.setpos(xo, yo)  # Set our position to the origin.
    for x in range(xmin * 10, xmax * 10 + 1):  # Looping through our xmin and xmax times 10 + 1, so we can get curves and render until the xmax instead of cutting off 1 point early.
        x = x / 10  # Dividing our current x by 10, since we're timings x by 10 to get in detailed curves instead of lines.
        y = eval(expr)
        coordX, coordY = screen_coords(xo, yo, ratio, x, y)  # Converting the evaluated expression to screen coordinates.
        if x == xmin:  # If x is xmin, that means we'll be moving to that position and don't want to render us moving there.
            pointer.setpos(coordX, coordY)  # Setting it's position to the very left aka most negative x.
        else:  # Otherwise, we're in position and want to render us moving.
            pointer.pendown()
            pointer.goto(coordX, coordY)  # Going to the new point, to render in the graph.
            pointer.penup()
    return

#
#  Setup the handling of the quit event (when the user closes the window)
#
#  Returns: Nothing
#
def handle_quit():
    turtle.bye()
    print("\nWindow closed, exiting...")
    exit(0)

#
#  Setup of turtle screen before we draw
#
#  Returns: Nothing
#
def setup():
    pointer = turtle.Turtle()
    screen = turtle.getscreen()
    screen.title("Graphing Calculator")
    screen.setup(WIDTH, HEIGHT, 0, 0)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    screen.bgcolor("white")
    screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", handle_quit)
    pointer.hideturtle()
    screen.delay(delay=0)
    return pointer

#
#  Main function that attempts to graph a number of expressions entered by the user
#  The user is also able to designate the origin of the chart to be drawn, as well as the ratio of pixels to steps (shared by both x and y axes)
#  The window size is always 800 width by 600 height in pixels
#
#  Returns: Nothing
#
def main():
    # Setup window
    pointer = setup()

    # Get input from user
    try:
        xo, yo = eval(input("Enter pixel coordinates of origin: "))
        ratio = int(input("Enter ratio of pixels per step: "))
    except KeyboardInterrupt:
        print("\nUser interrupted, exiting...")
        exit(0)

    # Set color and draw axes (store discovered visible xmin/xmax to use in drawing expressions)
    pointer.color(AXISCOLOR)
    xmin, xmax = draw_x_axis(pointer, xo, yo, ratio)
    draw_y_axis(pointer, xo, yo, ratio)

    # Loop and draw expressions until empty string "" is entered, change expression colour based on how many expressions have been drawn
    try:
        expr = input("Enter an arithmetic expression: ")
        counter = 0
        while expr != "":
            pointer.color(get_color(counter))
            draw_expr(pointer, xo, yo, ratio, xmin, xmax, expr)
            expr = input("Enter an arithmetic expression: ")
            counter += 1
        print("\nUser entered empty string, exiting...")
    except KeyboardInterrupt:
        print("\nUser interrupted, exiting...")
        exit(0)

# Run the program
main()
