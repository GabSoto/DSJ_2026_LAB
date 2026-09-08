import random
import pygame
from src.settings import Settings


class PowerUp(pygame.sprite.Sprite):
    TYPES = ("triple", "pierce")

    def __init__(self, x, settings: Settings, assets):
        super().__init__()
        self.settings = settings
        self.power_type = random.choice(self.TYPES)
        self.anim_frames = assets.get_animation(f"powerup_{self.power_type}")
        if not self.anim_frames:
            self.anim_frames = [pygame.Surface((32, 32), pygame.SRCALPHA)]
        self.image = self.anim_frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = -50
        self.speed = 2.0
        self.anim_start = pygame.time.get_ticks()
        self.frame_ms = 100

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.settings.screen_height:
            self.kill()
            return
        now = pygame.time.get_ticks()
        idx = ((now - self.anim_start) // self.frame_ms) % len(self.anim_frames)
        center = self.rect.center
        self.image = self.anim_frames[idx]
        self.rect = self.image.get_rect(center=center)
