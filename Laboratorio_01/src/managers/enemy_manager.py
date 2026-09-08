"""
Gestor de la formación de enemigos con patrones variados y enemigos especiales.
"""
import math
import random
import pygame
from src.entities.enemy import Enemy


class EnemyManager:
    FORMATIONS = ["grid", "wedge", "staggered", "checkerboard"]

    def __init__(self, settings, assets):
        self.settings = settings
        self.assets = assets
        self.enemies = pygame.sprite.Group()
        self.special_enemies = pygame.sprite.Group()
        self.direction = 1
        self.formation_name = "grid"
        self._create_formation()
        self._special_spawn_timer = 0
        self._special_spawn_interval = 12000  # ms

    def _create_formation(self):
        self.enemies.empty()
        self.formation_name = random.choice(self.FORMATIONS)
        builder = getattr(self, f"_build_{self.formation_name}")
        builder()

    def _is_checkerboard_gap(self, row, col):
        """Patrón intercalado tipo tablero de ajedrez: True = espacio vacío."""
        return (row + col) % 2 == 1

    def _build_grid(self):
        enemy_width = self.settings.enemy_cell_width
        enemy_height = self.settings.enemy_cell_height
        padding = self.settings.enemy_padding
        start_x = 60
        start_y = 50

        for row in range(self.settings.enemy_rows):
            for col in range(self.settings.enemy_cols):
                x = start_x + col * (enemy_width + padding)
                y = start_y + row * (enemy_height + padding)
                points = (self.settings.enemy_rows - row) * 10
                enemy_type = "ufo" if row == 0 and col % 3 == 0 else "basic"
                enemy = Enemy(x, y, self.settings, self.assets, enemy_type, points, (row, col))
                enemy.direction = self.direction
                self.enemies.add(enemy)

    def _build_wedge(self):
        enemy_width = self.settings.enemy_cell_width
        enemy_height = self.settings.enemy_cell_height
        padding = self.settings.enemy_padding
        start_y = 50
        cols = self.settings.enemy_cols

        for row in range(self.settings.enemy_rows):
            width = cols - row * 2
            if width < 1:
                break
            start_x = (self.settings.screen_width - width * (enemy_width + padding)) // 2
            for col in range(width):
                x = start_x + col * (enemy_width + padding)
                y = start_y + row * (enemy_height + padding)
                points = (self.settings.enemy_rows - row) * 15
                enemy_type = "ufo" if row == 0 and col == width // 2 else "basic"
                enemy = Enemy(x, y, self.settings, self.assets, enemy_type, points, (row, col))
                enemy.direction = self.direction
                self.enemies.add(enemy)

    # def _build_diamond(self):
    #     # Desactivada: con celdas de 64 px la formación queda muy grande
    #     # y los enemigos llegan al fondo demasiado rápido.
    #     pass

    def _build_staggered(self):
        enemy_width = self.settings.enemy_cell_width
        enemy_height = self.settings.enemy_cell_height
        padding = self.settings.enemy_padding
        start_x = 50
        start_y = 50

        for row in range(self.settings.enemy_rows):
            offset = (enemy_width + padding) // 2 if row % 2 == 1 else 0
            for col in range(self.settings.enemy_cols):
                x = start_x + col * (enemy_width + padding) + offset
                y = start_y + row * (enemy_height + padding)
                points = (self.settings.enemy_rows - row) * 10
                enemy_type = "ufo" if row == 0 and col % 4 == 0 else "basic"
                enemy = Enemy(x, y, self.settings, self.assets, enemy_type, points, (row, col))
                enemy.direction = self.direction
                self.enemies.add(enemy)

    def _build_checkerboard(self):
        """Formación pura de tablero de ajedrez."""
        enemy_width = self.settings.enemy_cell_width
        enemy_height = self.settings.enemy_cell_height
        padding = self.settings.enemy_padding
        start_x = 60
        start_y = 50

        for row in range(self.settings.enemy_rows):
            for col in range(self.settings.enemy_cols):
                if self._is_checkerboard_gap(row, col):
                    continue
                x = start_x + col * (enemy_width + padding)
                y = start_y + row * (enemy_height + padding)
                points = (self.settings.enemy_rows - row) * 10
                enemy_type = "ufo" if row == 0 and col % 3 == 0 else "basic"
                enemy = Enemy(x, y, self.settings, self.assets, enemy_type, points, (row, col))
                enemy.direction = self.direction
                self.enemies.add(enemy)

    def _spawn_special(self):
        """Crea un enemigo especial que cruza la parte superior de la pantalla."""
        y = 25
        direction = random.choice([-1, 1])
        if direction == 1:
            x = -50
        else:
            x = self.settings.screen_width + 50

        special = Enemy(
            x, y, self.settings, self.assets,
            enemy_type="ufo", points=25,
            cross_direction=direction
        )
        self.special_enemies.add(special)

    def update(self):
        time_now = pygame.time.get_ticks()

        # Lógica de borde de la formación principal
        move_down = False
        for enemy in self.enemies:
            if enemy.rect.right >= self.settings.screen_width or enemy.rect.left <= 0:
                move_down = True
                self.direction *= -1
                break

        for enemy in self.enemies:
            if move_down:
                enemy.drop()
            enemy.speed = self.settings.enemy_speed * enemy.speed_multiplier
            enemy.update(time_now, self.direction)

        # Enemigos especiales
        for special in self.special_enemies:
            special.update(time_now)
            if special.rect.right < -60 or special.rect.left > self.settings.screen_width + 60:
                special.kill()

        # Spawn de enemigo especial
        if time_now - self._special_spawn_timer > self._special_spawn_interval:
            if random.random() < 0.4:
                self._spawn_special()
            self._special_spawn_timer = time_now

    def try_shoot(self):
        if random.random() < self.settings.enemy_shoot_chance and len(self.enemies) > 0:
            shooter = random.choice(self.enemies.sprites())
            return shooter.shoot()
        return None

    def reset(self):
        self.enemies.empty()
        self.special_enemies.empty()
        self.direction = 1
        self._special_spawn_timer = pygame.time.get_ticks()
        self._create_formation()

    def clear_specials(self):
        self.special_enemies.empty()

    def is_empty(self):
        return len(self.enemies) == 0

    def reached_bottom(self):
        # El jugador está en ~y=516 (top). Game over cuando los enemigos
        # llegan casi a tocarlo, no antes.
        threshold = self.settings.screen_height - 70
        for enemy in self.enemies:
            if enemy.rect.bottom >= threshold:
                return True
        return False
