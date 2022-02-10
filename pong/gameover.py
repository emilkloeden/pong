import pygame

import game
import intro
from constants import BLACK, FPS, WINDOW_CENTER_WIDTH, WINDOW_HEIGHT
from debug import debug
from gamestate import GameState
from utils import FONT_MAP, is_quit_requested, is_return_to_main_screen_requested, print_text


class GameOver(GameState):
    def __init__(self, application, message):
        application.selection_sound.play()
        self.message = message
        self.font = FONT_MAP.get(64, pygame.font.Font(None, 64))
        self.continuing = True
        super().__init__(application)
    
    def loop(self):
        while self.continuing == True:
            self.handle_input()
            self.draw()
        self._restart_on_request()


    def handle_input(self):
        for event in pygame.event.get():
            if is_return_to_main_screen_requested(event):
                self.application.application_state = intro.IntroScreen(self.application)
            elif is_quit_requested(event):
                self.application._save_and_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.continuing = False
                if event.key == pygame.K_e:
                    self.application.debug_mode = not self.application.debug_mode 

    def draw(self):
        self.application.screen.fill(BLACK)
        
        if self.application.debug_mode:
            debug(f"{self.application.game_type=}")
        
        print_text(self.application.screen, self.message, self.font)
        print_text(self.application.screen, "Press SPACE to play again or ESCAPE to return to the main menu.", self.application.message_font, x=WINDOW_CENTER_WIDTH, y=WINDOW_HEIGHT * 0.75)
            
        pygame.display.update()
        self.application.clock.tick(FPS)

    def _restart_on_request(self):
        if self.application.game_type == "1 Player":
            self.application.application_state = game.OnePlayerGame(self.application)
        else:
            self.application.application_state = game.TwoPlayerGame(self.application)
