# File structure:
# snake_game/
# ├── __init__.py
# ├── screen.py
# ├── snake.py
# ├── food.py
# ├── controls.py
# └── game.py

# snake_game/screen.py
import turtle

class GameScreen:
    def __init__(self, width=600, height=600, bg_color="black", title="Snake Game"):
        self.screen = turtle.Screen()
        self.screen.title(title)
        self.screen.bgcolor(bg_color)
        self.screen.setup(width=width, height=height)
        self.screen.tracer(0)

    def update(self):
        self.screen.update()

    def listen(self):
        self.screen.listen()

    def onkey(self, func, key):
        self.screen.onkey(func, key)

# snake_game/snake.py
import turtle

class Snake:
    def __init__(self, shape="square", color="white", start_pos=(0, 0)):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape(shape)
        self.head.color(color)
        self.head.penup()
        self.head.goto(start_pos)
        self.head.direction = "stop"
        self.segments = []

    def move(self, distance=20):
        if self.head.direction == "up":
            self.head.sety(self.head.ycor() + distance)
        if self.head.direction == "down":
            self.head.sety(self.head.ycor() - distance)
        if self.head.direction == "left":
            self.head.setx(self.head.xcor() - distance)
        if self.head.direction == "right":
            self.head.setx(self.head.xcor() + distance)

    def go_up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    def go_down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    def go_left(self):
        if self.head.direction != "right":
            self.head.direction = "left"

    def go_right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def add_segment(self, shape="square", color="grey"):
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape(shape)
        new_segment.color(color)
        new_segment.penup()
        self.segments.append(new_segment)

    def reset(self):
        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()
        self.head.goto(0, 0)
        self.head.direction = "stop"

# snake_game/food.py
import turtle
import random

class Food:
    def __init__(self, shape="circle", color="red", start_pos=(0, 100)):
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape(shape)
        self.food.color(color)
        self.food.penup()
        self.food.goto(start_pos)

    def move(self, boundary):
        self.food.goto(random.randint(-boundary, boundary), 
                       random.randint(-boundary, boundary))

# snake_game/controls.py
class Controls:
    def __init__(self, screen, snake):
        self.screen = screen
        self.snake = snake

    def setup(self):
        self.screen.listen()
        self.screen.onkey(self.snake.go_up, "w")
        self.screen.onkey(self.snake.go_down, "s")
        self.screen.onkey(self.snake.go_left, "a")
        self.screen.onkey(self.snake.go_right, "d")

# snake_game/game.py
import time

class Game:
    def __init__(self, screen, snake, food, controls, delay=0.1, boundary=290):
        self.screen = screen
        self.snake = snake
        self.food = food
        self.controls = controls
        self.delay = delay
        self.boundary = boundary

    def check_collision(self):
        # Check for collision with border
        if (abs(self.snake.head.xcor()) > self.boundary or 
            abs(self.snake.head.ycor()) > self.boundary):
            return True
        
        # Check for collision with body
        for segment in self.snake.segments:
            if segment.distance(self.snake.head) < 20:
                return True
        
        return False

    def check_food_collision(self):
        if self.snake.head.distance(self.food.food) < 20:
            self.food.move(self.boundary)
            self.snake.add_segment()
            return True
        return False

    def move_snake(self):
        # Move the end segments first in reverse order
        for index in range(len(self.snake.segments)-1, 0, -1):
            x = self.snake.segments[index-1].xcor()
            y = self.snake.segments[index-1].ycor()
            self.snake.segments[index].goto(x, y)

        # Move segment 0 to where the head is
        if self.snake.segments:
            x = self.snake.head.xcor()
            y = self.snake.head.ycor()
            self.snake.segments[0].goto(x, y)

        self.snake.move()

    def run(self):
        self.controls.setup()
        while True:
            self.screen.update()

            if self.check_collision():
                time.sleep(1)
                self.snake.reset()

            self.check_food_collision()
            self.move_snake()

            time.sleep(self.delay)
