"""
Configuración global del juego.
"""
import os


class Settings:
    def __init__(self):
        # Pantalla
        self.screen_width = 800
        self.screen_height = 600
        self.fps = 60
        self.title = "Space Invaders"

        # Colores
        self.bg_color = (15, 15, 35)
        self.player_color = (0, 255, 100)
        self.enemy_color = (255, 80, 80)
        self.bullet_color = (255, 255, 0)
        self.text_color = (255, 255, 255)

        # Jugador
        self.player_speed = 5
        self.player_lives = 3
        self.player_shoot_cooldown = 250  # milisegundos

        # Enemigos
        self.enemy_speed = 1.5
        self.enemy_drop = 25
        self.enemy_rows = 4
        self.enemy_cols = 8
        self.enemy_shoot_chance = 0.003

        # Bala
        self.bullet_speed = 7
        self.enemy_bullet_speed = 4

        # Rutas de assets
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = os.path.join(base_dir, "assets")
        self.images_dir = os.path.join(self.assets_dir, "images")
        self.audio_dir = os.path.join(self.assets_dir, "audio")
        self.fonts_dir = os.path.join(self.assets_dir, "fonts")
