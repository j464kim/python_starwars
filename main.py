# Starwars / Python 2.7

import os
import random

# turtle module: https://docs.python.org/2/library/turtle.html
import turtle

# Initial Setup
# required by MacOSX to show the window
turtle.fd(0)
# set the animation speed to max
turtle.speed(0)
turtle.bgcolor("black")
# hide the default turtle
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(1)


class Ufo(turtle.Turtle):
    def __init__(self, ufo_shape, color, init_x, init_y):
        turtle.Turtle.__init__(self, shape = ufo_shape)
        self.speed(0) # animation speed in the range 0..10
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(init_x, init_y)
        self.speed = 1


# Create my Ufo
player = Ufo('triangle', 'white', 0, 0)


delay = raw_input("Enter to finish")