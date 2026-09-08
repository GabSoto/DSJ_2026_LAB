import pygame
from src.settings import Settings


class Player(pygame.sprite.Sprite):
    POWERUP_DURATION = 7000  # ms

    def __init__(self, settings: Settings, assets):
        super().__init__()
        self.settings = settings
        self.assets = assets
        self.frames = assets.get_ship_frames("player")
        self.image = self.frames["idle"]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (settings.screen_width // 2, settings.screen_height - 20)
        self.speed = settings.player_speed
        self.lives = settings.player_lives
        self.last_shot_time = 0
        self.invulnerable_until = pygame.time.get_ticks() + settings.player_spawn_invulnerability
        self.powerup_type = None
        self.powerup_until = 0

    def is_invulnerable(self):
        return pygame.time.get_ticks() < self.invulnerable_until

    def has_powerup(self):
        return self.powerup_type is not None and pygame.time.get_ticks() < self.powerup_until

    def set_powerup(self, ptype):
        self.powerup_type = ptype
        self.powerup_until = pygame.time.get_ticks() + self.POWERUP_DURATION

    def update(self):
        keys = pygame.key.get_pressed()
        moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        if moving_left:
            self.rect.x -= self.speed
            self.image = self.frames["left"]
        if moving_right:
            self.rect.x += self.speed
            self.image = self.frames["right"]
        if moving_left == moving_right:
            self.image = self.frames["idle"]

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
