import pygame
from button import Button
from constants import BLACK, CREDITS, FPS, ONE_PLAYER, QUIT, TITLE, TWO_PLAYERS, WINDOW_CENTER_HEIGHT, WINDOW_CENTER_WIDTH
from credits import CreditsScreen
from debug import debug
from utils import is_quit_requested, print_text
from gamestate import GameState
from game import OnePlayerGame, TwoPlayerGame


class IntroScreen(GameState):
    def __init__(self, application):
        self.one_player_button = Button(application.screen, ONE_PLAYER, WINDOW_CENTER_WIDTH - 120, WINDOW_CENTER_HEIGHT + 60)
        self.two_player_button = Button(application.screen, TWO_PLAYERS, WINDOW_CENTER_WIDTH -120, WINDOW_CENTER_HEIGHT + 120)
        self.credits_button = Button(application.screen, CREDITS, WINDOW_CENTER_WIDTH -120, WINDOW_CENTER_HEIGHT + 180)
        self.quit_button = Button(application.screen, QUIT, WINDOW_CENTER_WIDTH -120, WINDOW_CENTER_HEIGHT + 240)
        
        self.selected_button = self.one_player_button
        super().__init__(application)
    
    
    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        
        
        for event in pygame.event.get():
            if is_quit_requested(event):
                self.application._save_and_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.process_menu_item_selection()
                if event.key == pygame.K_DOWN:
                    self._switch_selected_button_down()
                elif event.key == pygame.K_UP:
                    self._switch_selected_button_up()
                if event.key == pygame.K_e:
                    self.application.debug_mode = not self.application.debug_mode
            for button in self._get_buttons():
                if button.rect.collidepoint(mouse_pos):
                    self.selected_button = button
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 ):
                        self.process_menu_item_selection()

    

    def process_logic(self):
        for button in self._get_buttons():
            button.selected = self.selected_button == button


    
    def draw(self):
        self.application.screen.fill(BLACK)
        print_text(self.application.screen, TITLE, self.application.font)
        
        for button in self._get_buttons():
            button.draw()
        
        if self.application.debug_mode:
            debug(pygame.mouse.get_pos())
            debug(self.selected_button, 30)
        
        pygame.display.update()
        self.application.clock.tick(FPS)


    def process_menu_item_selection(self):
        self.application.selection_sound.play()
        if self.selected_button == self.one_player_button:
            self.application.application_state = OnePlayerGame(self.application)
        elif self.selected_button == self.two_player_button:
            self.application.application_state = TwoPlayerGame(self.application)
        elif self.selected_button == self.credits_button:
            self.application.application_state = CreditsScreen(self.application)
        elif self.selected_button == self.quit_button:
            self.application._save_and_quit()

        
    def _switch_selected_button_down(self):
        buttons = self._get_buttons()
        
        currently_selected_button_index = [
            i for i, button 
            in enumerate(buttons)
            if button == self.selected_button
        ][0]
        new_index = (currently_selected_button_index + 1) % len(buttons)
        self.selected_button = buttons[new_index]

    def _switch_selected_button_up(self):
        buttons = self._get_buttons()
        
        currently_selected_button_index = [
            i for i, button 
            in enumerate(buttons)
            if button == self.selected_button
        ][0]
        new_index = (currently_selected_button_index - 1) % len(buttons)
        self.selected_button = buttons[new_index]


    def _get_buttons(self):
        return [self.one_player_button, self.two_player_button, self.credits_button, self.quit_button]