# bouncing_balls_gravity.py
import turtle as t
import random
import time
import math

# --- Screen setup ---
WIDTH, HEIGHT = 800, 600
screen = t.Screen()
screen.title("Gravity Balls — Physics Sandbox 🌍")
screen.bgcolor("black")
screen.setup(WIDTH, HEIGHT)
screen.tracer(0)

# --- Config ---
NUM_BALLS = 12
BALL_SIZE = 20
GRAVITY = 0.3         # how strong gravity pulls
BOUNCE_LOSS = 0.8     # energy lost on bounce (1 = perfect, <1 = damped)
FRICTION = 0.98       # friction on ground
WALL_BOUNCE_LOSS = 0.9
SPEED_RANGE = (2, 5)

# --- Ball class ---
class Ball(t.Turtle):
    def __init__(self):
        super().__init__(shape="circle")
        self.penup()
        self.color(random.random(), random.random(), random.random())
        self.speed(0)
        self.goto(random.randint(-WIDTH//3, WIDTH//3),
                  random.randint(HEIGHT//4, HEIGHT//2))
        # Random velocity
        self.dx = random.choice([-1, 1]) * random.uniform(*SPEED_RANGE)
        self.dy = random.choice([-1, 1]) * random.uniform(*SPEED_RANGE)

    def move(self):
        # Apply gravity
        self.dy -= GRAVITY

        x, y = self.xcor(), self.ycor()
        x += self.dx
        y += self.dy

        # Floor collision
        if y < -HEIGHT//2 + BALL_SIZE:
            y = -HEIGHT//2 + BALL_SIZE
            self.dy *= -BOUNCE_LOSS
            self.dx *= FRICTION  # friction on ground

            # stop tiny jittering when very slow
            if abs(self.dy) < 0.5:
                self.dy = 0
            if abs(self.dx) < 0.3:
                self.dx = 0

        # Wall collision
        if x > WIDTH//2 - BALL_SIZE or x < -WIDTH//2 + BALL_SIZE:
            self.dx *= -WALL_BOUNCE_LOSS
            x = max(min(x, WIDTH//2 - BALL_SIZE), -WIDTH//2 + BALL_SIZE)

        # Ceiling bounce (lightly)
        if y > HEIGHT//2 - BALL_SIZE:
            y = HEIGHT//2 - BALL_SIZE
            self.dy *= -WALL_BOUNCE_LOSS

        self.goto(x, y)

# --- Create balls ---
balls = [Ball() for _ in range(NUM_BALLS)]

# --- Collision check (same as before) ---
def check_collisions():
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            b1, b2 = balls[i], balls[j]
            dist = math.hypot(b1.xcor() - b2.xcor(), b1.ycor() - b2.ycor())
            if dist < BALL_SIZE * 2:
                # Swap velocities for simple elastic collision
                b1.dx, b2.dx = b2.dx, b1.dx
                b1.dy, b2.dy = b2.dy, b1.dy

                # Push them apart slightly to avoid overlap
                overlap = 0.5 * (BALL_SIZE * 2 - dist + 1)
                angle = math.atan2(b2.ycor() - b1.ycor(), b2.xcor() - b1.xcor())
                b1.goto(b1.xcor() - math.cos(angle) * overlap,
                        b1.ycor() - math.sin(angle) * overlap)
                b2.goto(b2.xcor() + math.cos(angle) * overlap,
                        b2.ycor() + math.sin(angle) * overlap)

# --- Main loop ---
while True:
    for ball in balls:
        ball.move()
    check_collisions()
    screen.update()
    time.sleep(0.02)
