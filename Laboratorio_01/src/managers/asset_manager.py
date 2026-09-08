"""
Gestor de carga de assets de imagen y fuentes.
"""
import os
import pygame
from src.utils import load_image, load_font, load_frame_sequence


class AssetManager:
    def __init__(self, settings):
        self.settings = settings
        self.images = {}
        self.animations = {}
        self.ship_frames = {}
        self.fonts = {}
        self.spacerage_dir = os.path.join(settings.images_dir, "spacerage")
        self._load_common_images()
        self._load_fonts()

    def _sr(self, *parts):
        return os.path.join(self.spacerage_dir, *parts)

    def _load_with_fallback(self, preferred, fallback, fallback_size, fallback_color, size=None):
        path = preferred if os.path.exists(preferred) else fallback
        return load_image(path, fallback_size, fallback_color, size=size)

    def _load_bank(self, folder, prefix, fallback_size, fallback_color):
        return {
            "left": load_image(os.path.join(folder, f"{prefix}_l2.png"), fallback_size, fallback_color),
            "idle": load_image(os.path.join(folder, f"{prefix}_m.png"), fallback_size, fallback_color),
            "right": load_image(os.path.join(folder, f"{prefix}_r2.png"), fallback_size, fallback_color),
        }

    def _load_common_images(self):
        screen_size = (self.settings.screen_width, self.settings.screen_height)
        self.images["background"] = self._load_with_fallback(
            self._sr("BG.png"),
            os.path.join(self.settings.images_dir, "backgrounds", "background.jpg"),
            screen_size,
            self.settings.bg_color,
            size=screen_size,
        )

        player_dir = self._sr("Player")
        self.ship_frames["player"] = self._load_bank(
            player_dir, "player_b", (64, 64), self.settings.player_color
        )
        self.images["player_idle"] = self.ship_frames["player"]["idle"]
        self.images["player_left"] = self.ship_frames["player"]["left"]
        self.images["player_right"] = self.ship_frames["player"]["right"]

        enemy_dir = self._sr("Enemies")
        for ship in ("enemy_1", "enemy_2"):
            for color in ("r", "g", "b"):
                key = f"{ship}_{color}"
                self.ship_frames[key] = self._load_bank(
                    enemy_dir, f"{ship}_{color}", (64, 64), self.settings.enemy_color
                )

        fx_dir = self._sr("FX")
        self.images["player_bullet"] = self._load_with_fallback(
            os.path.join(fx_dir, "vulcan_1.png"),
            os.path.join(self.settings.images_dir, "bullets", "bullet.png"),
            (6, 22),
            self.settings.bullet_color,
        )
        enemy_bullet = self._load_with_fallback(
            os.path.join(fx_dir, "plasma_1.png"),
            os.path.join(self.settings.images_dir, "bullets", "bullet.png"),
            (6, 21),
            (255, 50, 50),
        )
        self.images["enemy_bullet"] = pygame.transform.flip(enemy_bullet, False, True)

        explosion_dir = self._sr("Explosions")
        self.animations["explosion"] = load_frame_sequence(
            explosion_dir, "explosion_1", 11, pad=2, fallback_size=(52, 51), fallback_color=(255, 140, 0)
        )
        self.animations["powerup_triple"] = load_frame_sequence(
            enemy_dir, "mine_1", 9, pad=2, fallback_size=(48, 48), fallback_color=(80, 220, 180)
        )
        self.animations["powerup_pierce"] = load_frame_sequence(
            enemy_dir, "mine_11", 9, pad=2, fallback_size=(48, 48), fallback_color=(255, 180, 60)
        )

        self.images["pierce_bullet"] = self._load_with_fallback(
            os.path.join(fx_dir, "exhaust_01.png"),
            os.path.join(self.settings.images_dir, "bullets", "bullet.png"),
            (8, 20),
            self.settings.bullet_color,
        )


    def _load_fonts(self):
        default_font = os.path.join(self.settings.fonts_dir, "pixel.ttf")
        self.fonts["small"] = load_font(default_font, 18)
        self.fonts["medium"] = load_font(default_font, 32)
        self.fonts["large"] = load_font(default_font, 48)

    def get_image(self, key):
        return self.images.get(key)

    def get_animation(self, key):
        return self.animations.get(key, [])

    def get_ship_frames(self, ship, color=None):
        key = f"{ship}_{color}" if color else ship
        return self.ship_frames.get(key) or self.ship_frames.get("player")

    def get_font(self, key):
        return self.fonts.get(key)
