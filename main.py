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
screen = turtle.Screen()


class Ufo(turtle.Turtle):
    def __init__(self, ufo_shape, color, init_x, init_y):
        turtle.Turtle.__init__(self, shape=ufo_shape)
        self.speed(0)   # animation speed in the range 0..10
        self.penup()    # start drawing
        self.color(color)
        self.fd(0)
        self.goto(init_x, init_y)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

    def turn_left(self):
        self.lt(45)
        print('turning left')

    def turn_right(self):
        self.rt(45)
        print('turning right')

    def accelerate(self):
        self.speed += 1
        print('faster')

    def decelerate(self):
        self.speed -= 1
        print('slower')


# Player inherits Ufo
class Player(Ufo):
    def __init__(self, player_shape, color, init_x, init_y):
        Ufo.__init__(self, player_shape, color, init_x, init_y)
        self.speed = 2
        self.lives = 3


# Create my Ufo
player = Player('triangle', 'white', 0, 0)

# Keyboard bindings
screen.onkey(player.turn_left, "Left")
screen.onkey(player.turn_right, "Right")
screen.onkey(player.accelerate, "Up")
screen.onkey(player.decelerate, "Down")
screen.listen()

# Main Game Loop
while True:
    player.move()


delay = raw_input("Enter to finish")