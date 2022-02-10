
import pygame
import sys

from constants import TITLE, WINDOW_HEIGHT, WINDOW_WIDTH
from intro import IntroScreen
from utils import FONT_MAP, load_sound


class Pong:
    # First play initialisation
    def __init__(self):
        "Called on first instantiation only"
        pygame.init()
        pygame.display.set_caption(TITLE)
        
        self.playing = False
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = FONT_MAP.get(64, pygame.font.Font(None, 64))
        self.message_font = FONT_MAP.get(24, pygame.font.Font(None, 24))
        self.bounce_sound = load_sound("laser")
        self.selection_sound = load_sound("Hiss1")
        self.game_type = None  # Set upon choosing 1 or 2 players
        self.debug_mode = False
        self.application_state = IntroScreen(self)



    def _save_and_quit(self):
        pygame.quit()
        sys.exit()
    

