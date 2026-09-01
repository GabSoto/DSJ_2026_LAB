"""
Punto de entrada principal del juego Space Invaders.
"""
import pygame
from src.game import Game
from src.settings import Settings


def main():
    pygame.init()
    pygame.mixer.init()

    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption(settings.title)
    clock = pygame.time.Clock()

    game = Game(screen, clock, settings)
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
