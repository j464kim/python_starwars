# Starwars / Python 2.7

import os
import random
import time
from playsound import playsound

# turtle module: https://docs.python.org/2/library/turtle.html
import turtle

# Initial Setup
# required by MacOSX to show the window
turtle.fd(0)
# set the animation speed to max
turtle.speed(0)
turtle.bgcolor("black")
turtle.bgpic("starfield.gif")
turtle.title("StarWars")
# hide the default turtle
turtle.ht()
# This saves memory
turtle.setundobuffer(1)
# This speeds up drawing
turtle.tracer(0)
screen = turtle.Screen()

# Register shapes
turtle.register_shape("enemy.gif")
turtle.register_shape("ally.gif")


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
        self.check_boundary()

    def check_boundary(self):
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

    def re_generate(self):
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        self.goto(x, y)

    def remove(self):
        self.goto(1000, 1000)


# Player inherits Ufo
class Player(Ufo):
    def __init__(self, player_shape, color, init_x, init_y):
        Ufo.__init__(self, player_shape, color, init_x, init_y)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
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


# Enemy inherits Ufo
class Enemy(Ufo):
    def __init__(self, player_shape, color, init_x, init_y):
        Ufo.__init__(self, player_shape, color, init_x, init_y)
        self.speed = 6
        self.setheading(random.randint(0, 360))


# Ally inherits Ufo
class Ally(Ufo):
    def __init__(self, player_shape, color, init_x, init_y):
        Ufo.__init__(self, player_shape, color, init_x, init_y)
        self.speed = 8
        self.setheading(random.randint(0, 360))

    def check_boundary(self):
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)


# Missile inherits Ufo
class Missile(Ufo):
    def __init__(self, player_shape, color, init_x, init_y):
        Ufo.__init__(self, player_shape, color, init_x, init_y)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = 'fired'

    def move(self):
        if self.status == 'fired':
            self.fd(self.speed)
            self.check_boundary()
        elif self.status == 'standby':
            self.remove()

    def fired(self):
        if self.status == 'standby':
            # play the missile sound on fire in background
            # playsound('laser.mp3', False)
            self.goto(player.xcor(), player.ycor())
            self.status = 'fired'
            self.setheading(player.heading())

    def check_boundary(self):
        if self.xcor() > 290 or self.xcor() < -290 or self.ycor() > 290 or self.ycor() < -290:
            self.status = 'standby'
            self.remove()

    def is_collision(self, other):
        if Ufo.is_collision(self, other):
            self.status = 'standby'
            return True


class Debris(Ufo):
    def __init__(self, player_shape, color, init_x, init_y):
        Ufo.__init__(self, player_shape, color, init_x, init_y)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.frame = 0

    def explode(self, ufo):
        self.goto(ufo.xcor(), ufo.ycor())
        self.setheading(random.randint(0, 360))
        self.frame = 1

    def move(self):
        if self.frame:
            # for the better effect of debris falling apart
            self.fd((20 - self.frame) / 2)
            self.frame += 1

            if self.frame < 6:
                self.shapesize(stretch_wid=0.2, stretch_len=0.2, outline=None)
            elif self.frame < 11:
                self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
            else:
                self.shapesize(stretch_wid=0.05, stretch_len=0.05, outline=None)

            if self.frame > 18:
                self.frame = 0
                self.remove()

        # Border Check
        if self.xcor() > 290 or self.xcor() < -290 or self.ycor() > 290 or self.ycor() < -290:
            self.frame = 0
            self.remove()


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
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" % self.score
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=('Arial', 16, 'normal'))

    def update_score(self, score):
        self.score += score
        self.show_status()


# Create game object
game = Game()
game.draw_border()
game.show_status()

# Create Ufo object which is the player
player = Player('triangle', 'white', 0, 0)
missile = Missile('triangle', 'yellow', 1000, 1000)

enemies = []
allies = []
debris = []
for i in range(3):
    enemies.append(Enemy("enemy.gif", 'red', -100, 0))
    allies.append(Ally("ally.gif", 'blue', 100, 0))

for i in range(20):
    debris.append(Debris('circle', 'orange', 0, 0))

# Keyboard bindings
screen.onkey(player.turn_left, "Left")
screen.onkey(player.turn_right, "Right")
screen.onkey(player.accelerate, "Up")
screen.onkey(player.decelerate, "Down")
screen.onkey(missile.fired, "space")
screen.listen()

# Main Game Loop
while True:
    screen.update()
    time.sleep(0.02)
    player.move()
    missile.move()

    for enemy in enemies:
        enemy.move()
        # Check for collision
        if player.is_collision(enemy) or missile.is_collision(enemy):
            for deb in debris:
                deb.explode(enemy)
            enemy.re_generate()
            game.update_score(100)

    for ally in allies:
        ally.move()
        # Check for collision
        if player.is_collision(ally) or missile.is_collision(ally):
            ally.re_generate()
            game.update_score(-50)

    for deb in debris:
        deb.move()

delay = raw_input("Enter to finish")
