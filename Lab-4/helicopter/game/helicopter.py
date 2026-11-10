"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.4
MAX_VERTICAL_SPEED = 6.0


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.0

    def handle_input(self, keys_pressed):
        if keys_pressed[pygame.K_UP]:
            if self.vy > 0:
                self.vy = 0
            self.vy -= THRUST
        elif keys_pressed[pygame.K_DOWN]:
            if self.vy < 0:
                self.vy = 0
            self.vy += THRUST
        self.vy = max(-MAX_VERTICAL_SPEED, min(MAX_VERTICAL_SPEED, self.vy))

    def update(self, height_bound):
        self.y += self.vy
        min_y = self.height / 2
        max_y = height_bound - self.height / 2
        if self.y < min_y:
            self.y = min_y
            self.vy = 0
        elif self.y > max_y:
            self.y = max_y
            self.vy = 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
