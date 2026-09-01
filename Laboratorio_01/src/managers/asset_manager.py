"""
Gestor de carga de assets de imagen y fuentes.
"""
import os
import pygame
from src.utils import load_image, load_font


class AssetManager:
    def __init__(self, settings):
        self.settings = settings
        self.images = {}
        self.fonts = {}
        self._load_common_images()
        self._load_fonts()

    def _load_common_images(self):
        """Precarga imágenes usadas frecuentemente."""
        image_files = {
            "player": "player/player.png",
            "enemy": "enemies/enemy.png",
            "player_bullet": "bullets/bullet.png",
            "enemy_bullet": "bullets/bullet.png",
            "explosion": "explosions/explosion.png",
            "background": "backgrounds/background.jpg",
        }
        for key, relative_path in image_files.items():
            full_path = os.path.join(self.settings.images_dir, relative_path)
            self.images[key] = load_image(full_path)

    def _load_fonts(self):
        default_font = os.path.join(self.settings.fonts_dir, "pixel.ttf")
        self.fonts["small"] = load_font(default_font, 18)
        self.fonts["medium"] = load_font(default_font, 32)
        self.fonts["large"] = load_font(default_font, 48)

    def get_image(self, key):
        return self.images.get(key)

    def get_font(self, key):
        return self.fonts.get(key)
