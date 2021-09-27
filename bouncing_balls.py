import pygame  # pip install pygame
import sys
import random
import math
from math import pi


def random_bright_color():
    import colorsys
    hue = random.random()
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    return round(255 * r), round(255 * g), round(255 * b)


class Vector2D:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    @staticmethod
    def from_polar(mag, direction, angle_mode='deg'):
        if angle_mode == 'rad':
            return Vector2D(mag * math.cos(direction), mag * math.sin(direction))
        elif angle_mode == 'deg':
            direction *= math.pi / 180
            return Vector2D(mag * math.cos(direction), mag * math.sin(direction))
        else:
            raise ValueError("angle_mode must be 'deg' or 'rad'")

    def direction(self, angle_mode='deg') -> float:
        if angle_mode == 'rad':
            return math.atan2(self.y, self.x)
        elif angle_mode == 'deg':
            return math.atan2(self.y, self.x) / math.pi * 180
        else:
            raise ValueError("angle_mode must be 'deg' or 'rad'")

    def mag(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def __mul__(self, other: float):
        return Vector2D(self.x * other, self.y * other)

    def __add__(self, other: 'Vector2D'):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iter__(self):
        yield self.x
        yield self.y


class Ball:
    ball_radius = 1
    mass = 1

    def __init__(self, min_speed, max_speed, gravity, screen_width, screen_height):
        self.pos = Vector2D(random.random() * (screen_width - 2 * Ball.ball_radius) + Ball.ball_radius,
                            random.random() * screen_height / 2 + Ball.ball_radius)

        self.velocity = Vector2D.from_polar(random.uniform(min_speed, max_speed),
                                            random.uniform(0, 2*pi), angle_mode='rad')

        self.ball_color = random_bright_color()

    def draw(self, surface):
        pygame.draw.circle(surface, self.ball_color, tuple(self.pos), Ball.ball_radius)

    def tick(self, time_step, gravity, screen_width, screen_height):
        self.velocity += gravity * time_step
        self.pos += self.velocity * time_step
        if self.pos.x - Ball.ball_radius < 0:
            self.pos.x = Ball.ball_radius
            self.velocity.x *= -1
        elif self.pos.x + Ball.ball_radius > screen_width - 1:
            self.pos.x = screen_width - 1 - Ball.ball_radius
            self.velocity.x *= -1
        if self.pos.y - Ball.ball_radius< 0:
            self.pos.y = Ball.ball_radius
            self.velocity.y *= -1
        elif self.pos.y + Ball.ball_radius > screen_height - 1:
            self.pos.y = screen_height - 1 - Ball.ball_radius
            self.velocity.y *= -1


def draw_scene(surface, balls, window_width, window_height):
    game_window.fill(background_color)
    for ball in balls:
        ball.draw(surface)
    pygame.display.update()


def move_balls(time_step, gravity, balls, window_width, window_height):
    for ball in balls:
        ball.tick(time_step, gravity, window_width, window_height)


if __name__ == '__main__':
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()

    pygame.init()

    background_color = (0, 0, 0)
    fps = 30
    window_width = 3000
    window_height = 2000
    Ball.ball_radius = window_width / 200
    time_step = 1 / fps

    # from pygame docs:
    MOUSE_LEFT_CLICK = 1
    MOUSE_MIDDLE_CLICK = 2
    MOUSE_RIGHT_CLICK = 3
    MOUSE_SCROLL_UP = 4
    MOUSE_SCROLL_DOWN = 5

    pygame.display.set_caption('Bouncing Balls')
    game_window = pygame.display.set_mode((window_width, window_height))
    fps_controller = pygame.time.Clock()

    max_particle_speed_pixels_per_sec = (window_width / 500) * fps
    min_particle_speed_pixels_per_sec = (window_width / 2000) * fps
    gravity = Vector2D(0, window_height / 5)
    NUM_BALLS = 50
    balls = [Ball(min_particle_speed_pixels_per_sec, max_particle_speed_pixels_per_sec, gravity, window_width, window_height) for _ in range(NUM_BALLS)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # if space bar is released, end setup phase
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT_CLICK:
                    # gravity *= -1
                    gravity = Vector2D(gravity.y, -gravity.x)

        move_balls(time_step, gravity, balls, window_width, window_height)
        draw_scene(game_window, balls, window_width, window_height)
        fps_controller.tick(fps)
