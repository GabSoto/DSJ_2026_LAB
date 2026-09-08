"""
Pantalla de juego principal.
"""
import random
import pygame
from src.screens.base_screen import BaseScreen
from src.entities.player import Player
from src.entities.bullet import Bullet
from src.entities.explosion import Explosion
from src.entities.powerup import PowerUp
from src.managers.enemy_manager import EnemyManager
from src.utils import draw_text


class GameScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.settings.enemy_speed = self.settings._base_enemy_speed
        self.settings.enemy_shoot_chance = self.settings._base_enemy_shoot_chance
        self.player = Player(self.settings, self.assets)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.enemy_manager = EnemyManager(self.settings, self.assets)
        self.score = 0
        self.level = 1
        self.flash_surface = pygame.Surface(
            (self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA
        )
        self.flash_surface.fill((255, 255, 255))
        self.flash_frames = 0
        self._powerup_timer = 0
        self._powerup_interval = 18000  # ms

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                if event.key == pygame.K_SPACE:
                    self._player_shoot()

    def _player_shoot(self):
        if not self.player.can_shoot():
            return
        x = self.player.rect.centerx
        y = self.player.rect.top
        speed = self.settings.bullet_speed
        color = self.settings.bullet_color
        assets = self.assets
        settings = self.settings

        if self.player.has_powerup() and self.player.powerup_type == "triple":
            offsets = (-20, 0, 20)
            for ox in offsets:
                self.bullets.add(Bullet(x + ox, y, speed, color, settings, assets, owner="player"))
        elif self.player.has_powerup() and self.player.powerup_type == "pierce":
            self.bullets.add(Bullet(x, y, speed, color, settings, assets, owner="player", piercing=True))
        else:
            self.bullets.add(Bullet(x, y, speed, color, settings, assets, owner="player"))

        self.player.shoot()
        self.sounds.play("shoot")

    def update(self):
        self.player_group.update()
        self.bullets.update()
        self.enemy_bullets.update()
        self.explosions.update()
        self.powerups.update()
        self.enemy_manager.update()

        enemy_bullet = self.enemy_manager.try_shoot()
        if enemy_bullet:
            self.enemy_bullets.add(enemy_bullet)

        self._spawn_powerups()
        self._check_collisions()
        self._check_game_over()
        self._check_level_complete()
        if self.flash_frames > 0:
            self.flash_frames -= 1

    def _spawn_powerups(self):
        now = pygame.time.get_ticks()
        if now - self._powerup_timer > self._powerup_interval:
            if random.random() < 0.35:
                x = random.randint(60, self.settings.screen_width - 60)
                self.powerups.add(PowerUp(x, self.settings, self.assets))
            self._powerup_timer = now

    def _check_collisions(self):
        # Bala del jugador impacta enemigo de la formación
        for bullet in list(self.bullets):
            if bullet.owner != "player":
                continue
            hits = pygame.sprite.spritecollide(bullet, self.enemy_manager.enemies, False)
            for enemy in hits:
                self.score += enemy.points
                enemy.kill()
                self.explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery, self.settings, self.assets))
                self.sounds.play("explosion")
                if bullet.register_hit():
                    break

        # Bala del jugador impacta enemigo especial
        for bullet in list(self.bullets):
            if bullet.owner != "player":
                continue
            hits = pygame.sprite.spritecollide(bullet, self.enemy_manager.special_enemies, False)
            for enemy in hits:
                self.score += enemy.points
                enemy.kill()
                self.explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery, self.settings, self.assets))
                self.sounds.play("explosion")
                if bullet.register_hit():
                    break

        # Bala enemiga impacta jugador
        if not self.player.is_invulnerable():
            if pygame.sprite.spritecollideany(self.player, self.enemy_bullets):
                self.enemy_bullets.empty()
                self.player.take_damage()
                self.explosions.add(Explosion(self.player.rect.centerx, self.player.rect.centery, self.settings, self.assets))
                self.sounds.play("player_hit")
                self.flash_frames = 3

            # Enemigo choca con jugador
            if pygame.sprite.spritecollideany(self.player, self.enemy_manager.enemies):
                self.player.lives = 0
                self.sounds.play("player_hit")
                self.flash_frames = 3

            # Enemigo especial choca con jugador
            if pygame.sprite.spritecollideany(self.player, self.enemy_manager.special_enemies):
                self.player.lives = 0
                self.sounds.play("player_hit")
                self.flash_frames = 3

        # Jugador recoge power-up
        picked = pygame.sprite.spritecollideany(self.player, self.powerups)
        if picked:
            self.player.set_powerup(picked.power_type)
            picked.kill()
            self.sounds.play("shoot")  # reutilizamos sonido de shoot como pickup

    def _check_game_over(self):
        if not self.player.is_alive() or self.enemy_manager.reached_bottom():
            from src.screens.game_over_screen import GameOverScreen
            self.switch_to(lambda game: GameOverScreen(game, self.score))

    def _check_level_complete(self):
        if self.enemy_manager.is_empty():
            self.level += 1
            self.settings.enemy_speed += 0.5
            self.settings.enemy_shoot_chance += 0.0005
            self.enemy_manager.reset()

    def draw(self):
        center = self.settings.screen_width / 2
        drift = (self.player.rect.centerx - center) / center
        self.draw_background(drift)

        if not self.player.is_invulnerable() or (pygame.time.get_ticks() // 100) % 2 == 0:
            self.player_group.draw(self.screen)
        self.enemy_manager.enemies.draw(self.screen)
        self.enemy_manager.special_enemies.draw(self.screen)
        self.bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.explosions.draw(self.screen)
        self.powerups.draw(self.screen)

        if self.flash_frames > 0:
            alpha = int(255 * (self.flash_frames / 3))
            self.flash_surface.set_alpha(alpha)
            self.screen.blit(self.flash_surface, (0, 0))

        hud_color = self.settings.text_color
        if self.player.has_powerup():
            hud_color = (255, 255, 0) if self.player.powerup_type == "triple" else (0, 255, 200)

        draw_text(
            self.screen,
            f"Puntos: {self.score}",
            self.assets.get_font("small"),
            self.settings.text_color,
            10,
            10,
            center=False,
        )
        draw_text(
            self.screen,
            f"Vidas: {self.player.lives}",
            self.assets.get_font("small"),
            self.settings.text_color,
            self.settings.screen_width - 10,
            10,
            center=False,
        )
        if self.player.has_powerup():
            remaining = max(0, (self.player.powerup_until - pygame.time.get_ticks()) // 1000)
            draw_text(
                self.screen,
                f"{self.player.powerup_type.upper()} {remaining}s",
                self.assets.get_font("small"),
                hud_color,
                self.settings.screen_width // 2,
                10,
                center=True,
            )
        pygame.display.flip()
