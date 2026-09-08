import math
import random
import pygame
from src.settings import Settings


class Enemy(pygame.sprite.Sprite):
    COLORS = ("r", "g", "b")

    def __init__(self, x, y, settings: Settings, assets, enemy_type="basic", points=10,
                 formation_index=(0, 0), cross_direction=None):
        super().__init__()
        self.settings = settings
        self.assets = assets
        self.enemy_type = enemy_type
        self.formation_index = formation_index
        self.frames = None
        self.anim_frames = None
        self.anim_start = pygame.time.get_ticks()
        self.frame_ms = 80
        self.is_special = cross_direction is not None
        self.cross_direction = cross_direction

        row, col = formation_index
        color = self.COLORS[row % 3]

        if enemy_type == "ufo":
            self.frames = assets.get_ship_frames("enemy_2", color)
            self.image = self.frames["idle"]
            self.speed_multiplier = 1.6
            self.points = points * 2
        else:
            self.frames = assets.get_ship_frames("enemy_1", color)
            self.image = self.frames["idle"]
            self.speed_multiplier = 1.0
            self.points = points

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.base_x = x
        self.base_y = y
        self.direction = 1
        self.speed = settings.enemy_speed * self.speed_multiplier
        if self.is_special:
            self.speed = 3.0

        self.wave_offset = col * 0.4 + row * 0.2
        self.wave_speed = 0.002
        self.wave_amplitude = random.uniform(0.5, 1.5)

    def update(self, time_now=None, group_direction=1):
        if time_now is None:
            time_now = pygame.time.get_ticks()

        if self.is_special:
            self.base_x += self.speed * self.cross_direction
            self.rect.x = round(self.base_x)
            self.rect.y = round(self.base_y)
            self._update_visual(time_now)
            return

        self.direction = group_direction
        self.base_x += self.speed * self.direction
        wave_y = math.sin(time_now * self.wave_speed + self.wave_offset) * self.wave_amplitude
        self.rect.x = round(self.base_x)
        self.rect.y = round(self.base_y + wave_y)
        self._update_visual(time_now)

    def _update_visual(self, time_now):
        if self.frames:
            facing = self.cross_direction if self.is_special else self.direction
            if facing < 0:
                self.image = self.frames["left"]
            elif facing > 0:
                self.image = self.frames["right"]
            else:
                self.image = self.frames["idle"]

    def drop(self):
        self.base_y += self.settings.enemy_drop
        self.direction *= -1

    def shoot(self):
        from src.entities.bullet import Bullet
        bullet = Bullet(
            self.rect.centerx,
            self.rect.bottom,
            self.settings.enemy_bullet_speed,
            (255, 50, 50),
            self.settings,
            self.assets,
            owner="enemy"
        )
        return bullet

    def set_position(self, x, y):
        self.base_x = x
        self.base_y = y
        self.rect.topleft = (round(x), round(y))
