from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self, xcor, ycor):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.goto(xcor, ycor)
        self.score = 0
        self.color("white")
        self.write(arg = "Score: " + str(self.score), align="center", move=False, font= ("Arial", 14, "normal"))

    def add_score(self, brick):
        self.clear()
        self.score += brick.points
        self.write(arg = "Score: " + str(self.score), align="center", move=False, font= ("Arial", 14, "normal"))

    def update_score(self):
        self.clear()
        self.write(arg="Score: " + str(self.score), align="center", move=False, font=("Arial", 14, "normal"))