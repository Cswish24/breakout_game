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

def brick_collision(ball, velocity, bricklist, scoreboard):
    for brick in bricklist:
        if abs(ball.xcor()-brick.xcor()) < 25 and abs(ball.ycor()-brick.ycor()) < 15:
            print(abs(ball.xcor()-brick.xcor()))
            if abs(ball.xcor() - brick.xcor())/ (5/3) < abs(ball.ycor() - brick.ycor()):
                velocity['yvelocity'] *= -1
                scoreboard.add_score(brick)
                brick.color("black")
                bricklist.remove(brick)
            elif abs(ball.xcor() - brick.xcor()) / (5/3) > abs(ball.ycor() - brick.ycor()):
                scoreboard.add_score(brick)
                velocity['xvelocity'] *= -1
                brick.color("black")
                bricklist.remove(brick)

def paddle_collision(ball, velocity, paddle):
    if ball.distance(paddle) < 100 and ball.ycor() < -300:
        velocity['total_velocity'] = sqrt(velocity['xvelocity']**2+velocity['yvelocity']**2)
        print(f"hyp={velocity['total_velocity']}")
        if ball.xcor()-paddle.xcor() > 0:
            theta = atan(50/(ball.xcor()-paddle.xcor()))
            velocity['xvelocity'] = velocity['total_velocity'] * cos(theta)
            velocity['yvelocity'] = velocity['total_velocity'] * sin(theta)
        elif ball.xcor()-paddle.xcor() < 0:
            theta = atan(50/(paddle.xcor()-ball.xcor()))
            velocity['xvelocity'] = velocity['total_velocity'] * -cos(theta)
            velocity['yvelocity'] = velocity['total_velocity'] * sin(theta)
        else:
            velocity['yvelocity'] = velocity['total_velocity']
            velocity['xvelocity'] = 0

def barriers(ball, velocity, starter, scoreboard):
    if ball.xcor() < -590:
        velocity['xvelocity'] *= -1
    if ball.xcor() > 580:
        velocity['xvelocity'] *= -1
    if ball.ycor() >= 340:
        velocity['yvelocity'] *= -1
    if ball.ycor() <= -320:
        scoreboard.score -= 10
        scoreboard.update_score()
        ball.goto(0, 0)
        paddle.goto(0, -320)
        starter.countdown()





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
    "total_velocity": 4
}

screen.listen()
screen.onkeypress(paddle.lt, "a")
screen.onkeypress(paddle.rt, "s")
game_is_on = True






while game_is_on == True:
    starter.countdown()
    while game_is_on == True:
        screen.update()
        time.sleep(0.001)

        ball_movement(ball, velocity)

        paddle_collision(ball, velocity, paddle)

        brick_collision(ball, velocity, bricklist_red, scoreboard)

        brick_collision(ball, velocity, bricklist_yellow, scoreboard)

        brick_collision(ball, velocity, bricklist_green, scoreboard)

        barriers(ball, velocity, starter, scoreboard)


        if len(bricklist_red) == 0 and len(bricklist_yellow) == 0 and len(bricklist_green) == 0:
            print(f"Game Over, Score = {scoreboard.score}")
            screen.exitonclick()



