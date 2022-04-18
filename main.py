import time
from math import *
from bricks import RedBrick, YellowBrick, GreenBrick
from ball import Ball
from paddle import Paddle
from turtle import Screen
from starter import Starter
from scoreboard import Scoreboard


def ball_movement(ball, velocity):
    ball.goto((ball.xcor() + velocity['xvelocity']), (ball.ycor() + velocity['yvelocity']))


def brick_collision(ball, velocity, bricklist, scoreboard, previous_ball_coordinates):
    for brick in bricklist:
        if abs(ball.xcor() - brick.xcor()) < 25 and abs(ball.ycor() - brick.ycor()) < 15:

            # vertical brick bounce
            if abs(ball.xcor() - brick.xcor()) / (5 / 3) < abs(ball.ycor() - brick.ycor()):

                #ball moves in increments or jumps rather than sliding. this checks to make sure
                #the ball does not jump a brick boundary and bounce off the inside of the brick
                if abs(previous_ball_coordinates["xcor"] - brick.xcor()) / (5 / 3) > abs(
                        previous_ball_coordinates["ycor"]- brick.ycor()):
                    scoreboard.add_score(brick)
                    velocity['xvelocity'] *= -1
                    brick.color("black")
                    bricklist.remove(brick)
                    break

                velocity['yvelocity'] *= -1
                scoreboard.add_score(brick)
                brick.color("black")
                bricklist.remove(brick)

            # horizontal brick bounce
            elif abs(ball.xcor() - brick.xcor()) / (5 / 3) > abs(ball.ycor() - brick.ycor()):

                if abs(previous_ball_coordinates["xcor"] - brick.xcor()) / (5 / 3) < abs(
                        previous_ball_coordinates["ycor"]- brick.ycor()):

                    velocity['yvelocity'] *= -1
                    scoreboard.add_score(brick)
                    brick.color("black")
                    bricklist.remove(brick)
                    break

                scoreboard.add_score(brick)
                velocity['xvelocity'] *= -1
                brick.color("black")
                bricklist.remove(brick)


def paddle_collision(ball, velocity, paddle):
    if ball.distance(paddle) < 100 and ball.ycor() < -300:

        # paddle physics function. for theta, modify the constant integer x in atan(x/y) to set limits on
        # the angle a ball can bounce at
        velocity['total_velocity'] = sqrt(velocity['xvelocity'] ** 2 + velocity['yvelocity'] ** 2)

        # ball bounce on right side of paddle
        if ball.xcor() - paddle.xcor() > 0:
            theta = atan(50 / (ball.xcor() - paddle.xcor()))
            velocity['xvelocity'] = velocity['total_velocity'] * cos(theta)
            velocity['yvelocity'] = velocity['total_velocity'] * sin(theta)

        # ball bounce on left side of paddle
        elif ball.xcor() - paddle.xcor() < 0:
            theta = atan(50 / (paddle.xcor() - ball.xcor()))
            velocity['xvelocity'] = velocity['total_velocity'] * -cos(theta)
            velocity['yvelocity'] = velocity['total_velocity'] * sin(theta)

        # atan(x/0) may not be effectively by python without additional packages? this covers the perfect center
        # of the paddle where ball.xcor - paddle.xcor = 0
        else:
            velocity['yvelocity'] = velocity['total_velocity']
            velocity['xvelocity'] = 0


def barriers(ball, velocity, starter, scoreboard):

    # left barrier
    if ball.xcor() < -590:
        velocity['xvelocity'] *= -1

    # right barrier
    if ball.xcor() > 580:
        velocity['xvelocity'] *= -1

    # top barrier
    if ball.ycor() >= 340:
        velocity['yvelocity'] *= -1

    # bottom barrier and reset
    if ball.ycor() <= -320:
        scoreboard.score -= 10
        scoreboard.update_score()
        ball.goto(0, 0)
        paddle.goto(0, -320)
        starter.countdown()

# Object instances/board set up

screen = Screen()

screen.setup(width=1200, height=700)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)

bricklist_red = []
bricklist_yellow = []
bricklist_green = []

for x in range(-580, 600, 50):
    brick_red = RedBrick()
    brick_yellow = YellowBrick()
    brick_green = GreenBrick()
    brick_red.goto(x, 200)
    brick_yellow.goto(x, 150)
    brick_green.goto(x, 100)
    bricklist_red.append(brick_red)
    bricklist_yellow.append(brick_yellow)
    bricklist_green.append(brick_green)

scoreboard = Scoreboard(540, 300)

paddle = Paddle()
paddle.goto(0, -320)

starter = Starter()

ball = Ball()

velocity = {
    "xvelocity": 4,
    "yvelocity": -4,
    "total_velocity": 0
}

previous_ball_coordinates = {
    "xcor": 0,
    "ycor": 0
}

screen.listen()
screen.onkeypress(paddle.lt, "a")
screen.onkeypress(paddle.rt, "s")
game_is_on = True


starter.countdown()
while game_is_on == True:
    screen.update()
    time.sleep(0.001)

    previous_ball_coordinates["xcor"] = ball.xcor()
    previous_ball_coordinates["ycor"] = ball.ycor()

    ball_movement(ball, velocity)

    paddle_collision(ball, velocity, paddle)

    brick_collision(ball, velocity, bricklist_red, scoreboard, previous_ball_coordinates)

    brick_collision(ball, velocity, bricklist_yellow, scoreboard, previous_ball_coordinates)

    brick_collision(ball, velocity, bricklist_green, scoreboard, previous_ball_coordinates)

    barriers(ball, velocity, starter, scoreboard)

    if len(bricklist_red) == 0 and len(bricklist_yellow) == 0 and len(bricklist_green) == 0:
        print(f"Game Over, Score = {scoreboard.score}")
        screen.exitonclick()
