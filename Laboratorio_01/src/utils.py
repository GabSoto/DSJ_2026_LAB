"""
Utilidades compartidas del juego.
"""
import os
import pygame


def load_image(path, fallback_size=(32, 32), fallback_color=(255, 255, 255), size=None):
    """Carga una imagen o devuelve una superficie de color si no existe."""
    image = None
    if os.path.exists(path):
        try:
            image = pygame.image.load(path).convert_alpha()
        except pygame.error:
            image = None
    if image is None:
        image = pygame.Surface(fallback_size, pygame.SRCALPHA)
        image.fill(fallback_color)
    if size:
        image = pygame.transform.smoothscale(image, size)
    return image


def load_frame_sequence(directory, prefix, count, pad=2, fallback_size=(32, 32), fallback_color=(255, 140, 0)):
    """Carga frames numerados: prefix_01.png, prefix_02.png, ..."""
    frames = []
    for index in range(1, count + 1):
        filename = f"{prefix}_{index:0{pad}d}.png"
        frames.append(load_image(os.path.join(directory, filename), fallback_size, fallback_color))
    return frames


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
