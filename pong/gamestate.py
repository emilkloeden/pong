import pygame

from utils import is_quit_requested

class GameState:
    def __init__(self, application):
        self.application = application
        self.loop()

    def loop(self):
        while True:
            self.handle_input()
            self.process_logic()
            self.draw()

    def handle_input(self):
        for event in pygame.event.get():
            if is_quit_requested(event):
                self.application._save_and_quit()

    def process_logic(self):
        pass
    
    def draw(self):
        pass