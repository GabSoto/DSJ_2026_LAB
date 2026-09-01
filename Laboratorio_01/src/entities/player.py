import pygame
from src.utils import load_image
from src.settings import Settings


class Player(pygame.sprite.Sprite):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        image_path = f"{settings.images_dir}/player/player.png"
        self.image = load_image(image_path, (48, 48), settings.player_color)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (settings.screen_width // 2, settings.screen_height - 20)
        self.speed = settings.player_speed
        self.lives = settings.player_lives
        self.last_shot_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Mantener dentro de la pantalla
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

    def can_shoot(self):
        now = pygame.time.get_ticks()
        return now - self.last_shot_time >= self.settings.player_shoot_cooldown

    def shoot(self):
        self.last_shot_time = pygame.time.get_ticks()

    def take_damage(self):
        self.lives -= 1

    def is_alive(self):
        return self.lives > 0
