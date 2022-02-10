import pygame

from constants import BLACK, GREEN, WHITE
from utils import FONT_MAP

class Button:
    def __init__(self, destination_surface, text, x, y, bg_color=BLACK, text_color=WHITE, selected=False, selected_bg_color=GREEN):
        self.destination_surface = destination_surface
        self.text = text
        self.x = x
        self.y = y
        self.font = FONT_MAP.get(64, pygame.font.Font(None, 64))

        self.bg_color = bg_color
        self.text_color = text_color
        self.selected_bg_color = selected_bg_color

        self.selected = selected
        
        button_bg_color = self.selected_bg_color if self.selected else self.bg_color
        self.text_surface = self.font.render(self.text, True, self.text_color, button_bg_color)
        self.rect = self.text_surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        

    def draw(self):
        button_bg_color = self.selected_bg_color if self.selected else self.bg_color
        self.text_surface = self.font.render(self.text, True, self.text_color, button_bg_color)
        self.destination_surface.blit(self.text_surface, (self.x, self.y))
        

    def __repr__(self):
        return f"<Button '{self.text}'>"