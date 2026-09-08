import random
import pygame


class ParallaxBackground:
    def __init__(self, settings, assets):
        self.width = settings.screen_width
        self.height = settings.screen_height
        base = assets.get_image("background")
        far = self._tile_vertical(base if base else self._solid_layer(settings.bg_color))
        self.layers = [
            {"surface": far, "speed": 0.35, "y": 0.0, "depth": 4},
            {"surface": self._star_layer(90, (140, 180, 220, 160), 1), "speed": 0.9, "y": 0.0, "depth": 12},
            {"surface": self._star_layer(35, (220, 240, 255, 220), 2), "speed": 1.8, "y": 0.0, "depth": 22},
        ]

    def _solid_layer(self, color):
        surface = pygame.Surface((self.width, self.height))
        surface.fill(color)
        return surface

    def _tile_vertical(self, image):
        if image.get_size() != (self.width, self.height):
            image = pygame.transform.smoothscale(image, (self.width, self.height))
        tile = pygame.Surface((self.width, self.height * 2)).convert()
        tile.blit(image, (0, 0))
        tile.blit(pygame.transform.flip(image, False, True), (0, self.height))
        return tile

    def _star_layer(self, count, color, radius):
        surface = pygame.Surface((self.width, self.height * 2), pygame.SRCALPHA)
        rng = random.Random(count * 31 + radius)
        for _ in range(count * 2):
            x = rng.randint(0, self.width - 1)
            y = rng.randint(0, surface.get_height() - 1)
            pygame.draw.circle(surface, color, (x, y), radius)
        return surface

    def update(self):
        for layer in self.layers:
            height = layer["surface"].get_height()
            layer["y"] = (layer["y"] + layer["speed"]) % height

    def draw(self, screen, drift_x=0.0):
        for layer in self.layers:
            surface = layer["surface"]
            height = surface.get_height()
            y = int(layer["y"])
            x = int(-drift_x * layer["depth"])
            screen.blit(surface, (x, y - height))
            screen.blit(surface, (x, y))
            if x != 0:
                screen.blit(surface, (x + self.width if x < 0 else x - self.width, y - height))
                screen.blit(surface, (x + self.width if x < 0 else x - self.width, y))
