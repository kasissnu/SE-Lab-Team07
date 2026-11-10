"""
GameEngine: owns the helicopter and all obstacles.

Starter version: the helicopter moves and obstacles scroll by, but
there's no collision detection at all yet (the helicopter can fly
straight through obstacles harmlessly), no scoring, and no shield.
That's Tasks 2, 3, and 4. Movement also has known bugs (see
game/helicopter.py) that Task 1 asks you to fix.
"""

import random

import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3


class GameEngine:
    def __init__(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False
        self.distance = 0.0
        self.shield_active = False

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(margin + GAP_HEIGHT // 2, HEIGHT - margin - GAP_HEIGHT // 2)
        self.obstacles.append(Obstacle(
            x=WIDTH, gap_y=gap_y, gap_height=GAP_HEIGHT,
            wall_width=WALL_WIDTH, screen_height=HEIGHT, speed=SCROLL_SPEED,
        ))

    def handle_input(self, keys_pressed):
        self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()
        elif not self.game_over and key == pygame.K_s:
            self.shield_active = True

    def update(self):
        if self.game_over:
            return
        self.helicopter.update(HEIGHT)
        self.distance += SCROLL_SPEED

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]
        helicopter_rect = self.helicopter.get_rect()
        for obstacle in self.obstacles:
            if obstacle.collision_absorbed or not obstacle.collides_with(helicopter_rect):
                continue
            if self.shield_active:
                self.shield_active = False
                obstacle.collision_absorbed = True
            else:
                self.game_over = True
                break

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(
            surface, self.helicopter, self.obstacles, self.shield_active
        )
        renderer.draw_text(surface, font, f"Distance: {int(self.distance)} m", (12, 12))
        shield_status = "READY" if self.shield_active else "OFF"
        renderer.draw_text(surface, font, f"Shield: {shield_status}", (550, 12))
        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"GAME OVER - Distance: {int(self.distance)} m - Press R",
            )
