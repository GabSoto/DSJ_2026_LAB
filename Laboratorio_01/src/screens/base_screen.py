"""
Pantalla base para todas las escenas del juego.
"""
import pygame


class BaseScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.assets = game.assets
        self.sounds = game.sounds
        self.done = False
        self.next_screen = None

    def handle_events(self, events):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def draw_background(self, drift_x=0.0):
        self.screen.fill(self.settings.bg_color)
        self.game.parallax.draw(self.screen, drift_x)

    def switch_to(self, screen_class):
        self.done = True
        self.next_screen = screen_class
