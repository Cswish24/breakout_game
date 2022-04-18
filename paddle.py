from turtle import Turtle


class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=10)
        self.color("white")


    def rt(self):
        self.goto(self.xcor() + 10, self.ycor())

    def lt(self):
        self.goto(self.xcor() - 10, self.ycor())