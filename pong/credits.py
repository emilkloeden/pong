import pygame

import intro
from constants import BLACK, FPS, WINDOW_CENTER_WIDTH
from debug import debug
from gamestate import GameState
from utils import FONT_MAP, is_quit_requested, is_return_to_main_screen_requested, print_text, print_screed


class CreditsScreen(GameState):
    def __init__(self, application):
        self.font = FONT_MAP.get(16)
        self.heading_font = FONT_MAP.get(64)
        
        self.credits_texts = [
        "Original game by Allan Alcorn",
        "(as per https://en.wikipedia.org/wiki/Pong)",
        "",
        "Amateur reproduction by ekdev",
        "",
        "All sounds from The Motion Monkey Free Retro Arcade Sounds Pack v1.0.5",
        "© 2015-2017 The Motion Monkey",
        "or (https://realpython.com/asteroids-game-python/#step-9-playing-sounds)",
        "Collision logic adapted from (https://github.com/clear-code-projects/Pong_in_Pygame) ",
        "Certain code adapted/reused from (https://realpython.com/asteroids-game-python/#step-9-playing-sounds)",
        ]


        super().__init__(application)
        
    def loop(self):
        while True:
            self.handle_input()
            self.draw()


    def handle_input(self):
        for event in pygame.event.get():
            if is_return_to_main_screen_requested(event):
                self.application.application_state = intro.IntroScreen(self.application)
            elif is_quit_requested(event):
                self.application._save_and_quit()
            
    def draw(self):
        self.application.screen.fill(BLACK)
        
        print_text(self.application.screen, "Credits", self.application.font,x=WINDOW_CENTER_WIDTH, y=160)
        print_screed(self.application.screen, self.credits_texts, self.font, x=WINDOW_CENTER_WIDTH, starting_y=230, padding = 5)
 
        pygame.display.update()
        self.application.clock.tick(FPS)
