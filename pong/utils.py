import pygame
from pygame import Color
from pygame.math import Vector2
from pygame.mixer import Sound

pygame.font.init()

FONT_MAP = {
            64: pygame.font.Font(None, 64),
            24: pygame.font.Font(None, 24),
            16: pygame.font.Font(None, 16),
        }

def is_quit_requested(event):
    return event.type == pygame.QUIT or (
        event.type == pygame.KEYDOWN 
        and event.key == pygame.K_ESCAPE
    )

def is_return_to_main_screen_requested(event):
    return  event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE

def print_text(surface, text, font, x=None, y=None, color=Color("white")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    if x and y: 
        rect.center = Vector2(x, y)
    else:
        rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text_surface, rect)


def print_screed(surface, text_strings, font, x, starting_y, padding=4, color=Color("white")):
    for i, text in enumerate(text_strings):
        print_text(surface, text, font, x, starting_y + i * (font.get_height() + padding), color)


def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)
