"""
Utilidades compartidas del juego.
"""
import os
import pygame


def load_image(path, fallback_size=(32, 32), fallback_color=(255, 255, 255)):
    """Carga una imagen o devuelve una superficie de color si no existe."""
    if os.path.exists(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except pygame.error:
            pass
    surface = pygame.Surface(fallback_size, pygame.SRCALPHA)
    surface.fill(fallback_color)
    return surface


def load_font(path, size):
    """Carga una fuente o usa la fuente por defecto de pygame."""
    if path and os.path.exists(path):
        try:
            return pygame.font.Font(path, size)
        except pygame.error:
            pass
    return pygame.font.SysFont("arial", size)


def draw_text(surface, text, font, color, x, y, center=True):
    """Dibuja texto en una superficie."""
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)
    return rect
