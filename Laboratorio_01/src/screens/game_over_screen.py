"""
Pantalla de fin de juego.
"""
import pygame
from src.screens.base_screen import BaseScreen
from src.screens.menu_screen import MenuScreen
from src.utils import draw_text


class GameOverScreen(BaseScreen):
    def __init__(self, game, score):
        super().__init__(game)
        self.score = score

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    from src.screens.game_screen import GameScreen
                    self.switch_to(GameScreen)
                if event.key == pygame.K_m:
                    self.switch_to(MenuScreen)
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.settings.bg_color)
        bg = self.assets.get_image("background")
        if bg:
            self.screen.blit(bg, (0, 0))

        draw_text(
            self.screen,
            "GAME OVER",
            self.assets.get_font("large"),
            (255, 50, 50),
            self.settings.screen_width // 2,
            self.settings.screen_height // 3,
        )
        draw_text(
            self.screen,
            f"Puntaje final: {self.score}",
            self.assets.get_font("medium"),
            self.settings.text_color,
            self.settings.screen_width // 2,
            self.settings.screen_height // 2,
        )
        draw_text(
            self.screen,
            "R: Reintentar  |  M: Menú  |  ESC: Salir",
            self.assets.get_font("small"),
            self.settings.text_color,
            self.settings.screen_width // 2,
            self.settings.screen_height * 2 // 3,
        )
        pygame.display.flip()
