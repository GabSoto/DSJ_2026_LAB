"""
Clase principal que controla el flujo del juego y las pantallas.
"""
import pygame
from src.managers.asset_manager import AssetManager
from src.managers.sound_manager import SoundManager
from src.entities.background import ParallaxBackground
from src.screens.menu_screen import MenuScreen


class Game:
    def __init__(self, screen, clock, settings):
        self.screen = screen
        self.clock = clock
        self.settings = settings
        self.running = True
        self.assets = AssetManager(settings)
        self.sounds = SoundManager(settings)
        self.parallax = ParallaxBackground(settings, self.assets)
        self.current_screen = MenuScreen(self)
        self.sounds.play_music("background.wav", volume=0.4)

    def run(self):
        while self.running:
            events = pygame.event.get()
            self.parallax.update()
            self.current_screen.handle_events(events)
            self.current_screen.update()
            self.current_screen.draw()

            if self.current_screen.done:
                next_screen_class = self.current_screen.next_screen
                self.current_screen = next_screen_class(self)

            self.clock.tick(self.settings.fps)

        self.sounds.stop_music()
