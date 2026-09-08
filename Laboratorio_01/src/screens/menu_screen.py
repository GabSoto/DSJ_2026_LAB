"""
Pantalla de menú principal.
"""
import pygame
from src.screens.base_screen import BaseScreen
from src.utils import draw_text


class MenuScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    from src.screens.game_screen import GameScreen
                    self.switch_to(GameScreen)

    def update(self):
        pass

    def draw(self):
        self.draw_background()

        draw_text(
            self.screen,
            self.settings.title,
            self.assets.get_font("large"),
            self.settings.text_color,
            self.settings.screen_width // 2,
            self.settings.screen_height // 3,
        )
        draw_text(
            self.screen,
            "Presiona ENTER o ESPACIO para jugar",
            self.assets.get_font("medium"),
            self.settings.text_color,
            self.settings.screen_width // 2,
            self.settings.screen_height // 2,
        )
        draw_text(
            self.screen,
            "Flechas / A-D para moverse, ESPACIO para disparar",
            self.assets.get_font("small"),
            self.settings.text_color,
            self.settings.screen_width // 2,
            self.settings.screen_height * 2 // 3,
        )
        pygame.display.flip()
