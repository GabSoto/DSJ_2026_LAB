import pygame
from src.utils import load_image
from src.settings import Settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, color, settings: Settings, owner="player"):
        super().__init__()
        self.settings = settings
        self.owner = owner
        bullet_filename = "bullet.png"
        image_path = f"{settings.images_dir}/bullets/{bullet_filename}"
        self.image = load_image(image_path, (6, 14), color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed if self.owner == "player" else -self.speed
        if self.rect.bottom < 0 or self.rect.top > self.settings.screen_height:
            self.kill()
