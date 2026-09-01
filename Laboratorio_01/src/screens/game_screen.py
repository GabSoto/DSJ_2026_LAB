"""
Pantalla de juego principal.
"""
import pygame
from src.screens.base_screen import BaseScreen
from src.entities.player import Player
from src.entities.bullet import Bullet
from src.entities.explosion import Explosion
from src.managers.enemy_manager import EnemyManager
from src.utils import draw_text


class GameScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player(self.settings)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.enemy_manager = EnemyManager(self.settings)
        self.score = 0
        self.level = 1

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
        if self.player.can_shoot():
            bullet = Bullet(
                self.player.rect.centerx,
                self.player.rect.top,
                self.settings.bullet_speed,
                self.settings.bullet_color,
                self.settings,
                owner="player"
            )
            self.bullets.add(bullet)
            self.player.shoot()
            self.sounds.play("shoot")

    def update(self):
        self.player_group.update()
        self.bullets.update()
        self.enemy_bullets.update()
        self.explosions.update()
        self.enemy_manager.update()

        enemy_bullet = self.enemy_manager.try_shoot()
        if enemy_bullet:
            self.enemy_bullets.add(enemy_bullet)

        self._check_collisions()
        self._check_game_over()
        self._check_level_complete()

    def _check_collisions(self):
        # Bala del jugador impacta enemigo de la formación
        hits = pygame.sprite.groupcollide(
            self.enemy_manager.enemies, self.bullets, True, True
        )
        for enemy, bullets in hits.items():
            self.score += enemy.points
            self.explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery, self.settings))
            self.sounds.play("explosion")

        # Bala del jugador impacta enemigo especial
        special_hits = pygame.sprite.groupcollide(
            self.enemy_manager.special_enemies, self.bullets, True, True
        )
        for enemy, bullets in special_hits.items():
            self.score += enemy.points
            self.explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery, self.settings))
            self.sounds.play("explosion")

        # Bala enemiga impacta jugador
        if pygame.sprite.spritecollideany(self.player, self.enemy_bullets):
            self.enemy_bullets.empty()
            self.player.take_damage()
            self.explosions.add(Explosion(self.player.rect.centerx, self.player.rect.centery, self.settings))
            self.sounds.play("player_hit")

        # Enemigo choca con jugador
        if pygame.sprite.spritecollideany(self.player, self.enemy_manager.enemies):
            self.player.lives = 0
            self.sounds.play("player_hit")

        # Enemigo especial choca con jugador
        if pygame.sprite.spritecollideany(self.player, self.enemy_manager.special_enemies):
            self.player.lives = 0
            self.sounds.play("player_hit")

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
        self.screen.fill(self.settings.bg_color)
        bg = self.assets.get_image("background")
        if bg:
            self.screen.blit(bg, (0, 0))

        self.player_group.draw(self.screen)
        self.enemy_manager.enemies.draw(self.screen)
        self.enemy_manager.special_enemies.draw(self.screen)
        self.bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.explosions.draw(self.screen)

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
        pygame.display.flip()
