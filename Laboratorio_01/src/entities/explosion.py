import pygame
from src.settings import Settings


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, settings: Settings, assets):
        super().__init__()
        self.settings = settings
        self.frames = assets.get_animation("explosion")
        if not self.frames:
            fallback = pygame.Surface((40, 40), pygame.SRCALPHA)
            fallback.fill((255, 140, 0))
            self.frames = [fallback]
        self.frame_index = 0
        self.frame_duration = 40
        self.last_update = pygame.time.get_ticks()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update < self.frame_duration:
            return
        self.last_update = now
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            self.kill()
            return
        center = self.rect.center
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=center)
