import pygame
from src.utils import load_image
from src.settings import Settings


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, settings: Settings):
        super().__init__()
        self.settings = settings
        image_path = f"{settings.images_dir}/explosions/explosion.png"
        self.image = load_image(image_path, (40, 40), (255, 140, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = 250  # milisegundos
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
