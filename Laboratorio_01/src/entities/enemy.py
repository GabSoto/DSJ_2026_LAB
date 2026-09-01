import math
import random
import pygame
from src.utils import load_image
from src.settings import Settings


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, settings: Settings, enemy_type="basic", points=10, formation_index=(0, 0)):
        super().__init__()
        self.settings = settings
        self.enemy_type = enemy_type
        self.formation_index = formation_index

        if enemy_type == "ufo":
            image_path = f"{settings.images_dir}/enemies/ufo.png"
            self.base_image = load_image(image_path, (48, 24), (200, 50, 255))
            self.speed_multiplier = 1.6
            self.points = points * 2
        else:
            image_path = f"{settings.images_dir}/enemies/enemy.png"
            self.base_image = load_image(image_path, (36, 28), settings.enemy_color)
            self.speed_multiplier = 1.0
            self.points = points

        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.base_x = x
        self.base_y = y
        self.direction = 1
        self.speed = settings.enemy_speed * self.speed_multiplier

        # Movimiento de "respiración" muy suave, basado en la columna para coherencia de grupo
        row, col = formation_index
        self.wave_offset = col * 0.4 + row * 0.2
        self.wave_speed = 0.002
        self.wave_amplitude = random.uniform(0.5, 1.5)

    def update(self, time_now=None, group_direction=1):
        if time_now is None:
            time_now = pygame.time.get_ticks()

        self.direction = group_direction
        self.base_x += self.speed * self.direction

        # Ondulación vertical muy sutil para evitar temblor
        wave_y = math.sin(time_now * self.wave_speed + self.wave_offset) * self.wave_amplitude

        self.rect.x = round(self.base_x)
        self.rect.y = round(self.base_y + wave_y)

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
            owner="enemy"
        )
        return bullet

    def set_position(self, x, y):
        self.base_x = x
        self.base_y = y
        self.rect.topleft = (round(x), round(y))

    def _special_update(self, time_now, direction):
        """Movimiento para enemigos especiales que cruzan la pantalla."""
        self.base_x += self.speed * direction
        self.rect.x = round(self.base_x)
        self.rect.y = round(self.base_y)
