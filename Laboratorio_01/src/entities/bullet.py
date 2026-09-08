import pygame
from src.settings import Settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, color, settings: Settings, assets, owner="player", piercing=False):
        super().__init__()
        self.settings = settings
        self.owner = owner
        self.piercing = piercing
        self.pierced = 0
        self.max_pierce = 3

        if owner == "player" and piercing:
            key = "pierce_bullet"
        else:
            key = "player_bullet" if owner == "player" else "enemy_bullet"

        self.image = assets.get_image(key)
        if self.image is None:
            self.image = pygame.Surface((6, 14), pygame.SRCALPHA)
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed if self.owner == "player" else -self.speed
        if self.rect.bottom < 0 or self.rect.top > self.settings.screen_height:
            self.kill()

    def register_hit(self):
        if not self.piercing:
            self.kill()
            return True
        self.pierced += 1
        if self.pierced > self.max_pierce:
            self.kill()
            return True
        return False
