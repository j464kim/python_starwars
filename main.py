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
        self.speed(0)  # animation speed in the range 0..10
        self.penup()  # start drawing
        self.color(color)
        self.fd(0)
        self.goto(init_x, init_y)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        # Detect Boundary
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        if (self.xcor() >= other.xcor() - 20) and (self.xcor() <= other.xcor() + 20) and (
                self.ycor() >= other.ycor() - 20) and (self.ycor() <= other.ycor() + 20):
            return True
        else:
            return False


class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.lives = 3
        # define pen
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color('white')
        self.pen.pensize(3)
        self.pen.penup()

    def draw_border(self):
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()


# Player inherits Ufo
class Player(Ufo):
    def __init__(self, player_shape, color, init_x, init_y):
        Ufo.__init__(self, player_shape, color, init_x, init_y)
        self.speed = 2
        self.lives = 3

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
class Enemy(Ufo):
    def __init__(self, player_shape, color, init_x, init_y):
        Ufo.__init__(self, player_shape, color, init_x, init_y)
        self.speed = 6
        self.setheading(random.randint(0, 360))


# Create game object
game = Game()
game.draw_border()

# Create Ufo object which is the player
player = Player('triangle', 'white', 0, 0)
enemy = Enemy('circle', 'red', -100, 0)

# Keyboard bindings
screen.onkey(player.turn_left, "Left")
screen.onkey(player.turn_right, "Right")
screen.onkey(player.accelerate, "Up")
screen.onkey(player.decelerate, "Down")
screen.listen()

# Main Game Loop
while True:
    player.move()
    enemy.move()

    # Check for collision
    if player.is_collision(enemy):
        # Move the if player collides with it
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        enemy.goto(x, y)

delay = raw_input("Enter to finish")
