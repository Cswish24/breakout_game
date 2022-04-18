import time
from turtle import Turtle

class Starter(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.goto(0, 0)
        self.color("white")


    def countdown(self):
        self.clear()
        self.write(arg="Ready", align="center", move=False, font= ("Arial", 14, "normal"))
        time.sleep(1)
        self.clear()
        self.write(arg="Set", align="center", move=False, font=("Arial", 14, "normal"))
        time.sleep(1)
        self.clear()
        self.write(arg="Go!!!", align="center", move=False, font=("Arial", 14, "normal"))
        time.sleep(1)
        self.clear()