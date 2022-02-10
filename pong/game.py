import pygame
from pygame.math import Vector2

import intro
from constants import (BLACK, DOWN, FPS, GREY, LEFT, ONE_PLAYER, RIGHT, 
                       TWO_PLAYERS, UP, WHITE, WINDOW_CENTER_HEIGHT, WINDOW_CENTER_WIDTH,
                       WINDOW_HEIGHT, WINDOW_WIDTH)
from debug import debug
from gameover import GameOver
from gamestate import GameState
from models import AIPaddle, Ball, Paddle
from utils import (is_quit_requested, is_return_to_main_screen_requested,
                   print_text)


class Match:
    def __init__(self, turn, ball, message="") -> None:
        self.turn = turn
        self.ball = ball
        self.message = message

class MainGame(GameState):
    def __init__(self, application, game_type):
        self.paused = False
        self.application = application
        self.application.game_type = game_type
        super().__init__(application)
    
    def loop(self):
        self.setup()
        self.turn_loop()


    # Every play initialisation
    def setup(self):
        "Called on every (re)start"
        self.playing = True
        self.application.turn = LEFT
        
        
        self.ball = Ball(x=50, y=WINDOW_CENTER_HEIGHT, initial_movement_direction=RIGHT)
        self.match = Match(turn=LEFT, ball=self.ball)
        
        self._create_paddles()
        
        self.divisor_surface = pygame.Surface((2, WINDOW_HEIGHT))
        self.divisor_surface.fill(WHITE)
        self.application.screen.blit(self.divisor_surface, (WINDOW_CENTER_WIDTH, 0))


    def _create_paddles(self):
        self.left_paddle = Paddle(x=30, y=WINDOW_CENTER_HEIGHT)
        self.right_paddle = AIPaddle(x=WINDOW_WIDTH - 30, y=WINDOW_CENTER_HEIGHT, match=self.match)

    def _new_ball(self, turn):
        if turn == LEFT:
            ball = Ball(x=self.left_paddle.rect.right + self.left_paddle.width, y=self.left_paddle.rect.centery, initial_movement_direction=RIGHT)
        else:
            ball = Ball(x=self.right_paddle.rect.left - self.right_paddle.width, y=self.right_paddle.rect.centery, initial_movement_direction=LEFT)
        
        self.ball = ball
        self.match.ball = ball
        self.match.turn = turn
        
    def turn_loop(self):
        while True:
            self.handle_input()
            self.process_logic()
            self.draw()
            

    def handle_input(self):
        for event in pygame.event.get():
            if is_return_to_main_screen_requested(event):
                self.application.application_state = intro.IntroScreen(self.application)
            elif is_quit_requested(event):
                self.application._save_and_quit()

            if event.type == pygame.KEYUP and event.key == pygame.K_p:
                self.paused = not self.paused
            
            if event.type == pygame.KEYUP and event.key == pygame.K_e:
                self.application.debug_mode = not self.application.debug_mode

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_UP]:
            self.right_paddle.move(UP)
        
        elif is_key_pressed[pygame.K_DOWN]:
            self.right_paddle.move(DOWN)

        if is_key_pressed[pygame.K_w]:
            self.left_paddle.move(UP)
        
        elif is_key_pressed[pygame.K_s]:
            self.left_paddle.move(DOWN)


        

    def process_logic(self):
        if not self.paused:
            if self.ball:
                self.ball.move()
                if isinstance(self.right_paddle, AIPaddle):
                    self.right_paddle.move()
                if self.ball.rect.right < 0:
                    self._new_ball(RIGHT)
                    self.right_paddle.score += 1
                elif self.ball.rect.left > WINDOW_WIDTH:
                    self._new_ball(LEFT)
                    self.left_paddle.score += 1

                
                # This version of collision logic from: https://github.com/clear-code-projects/Pong_in_Pygame/blob/a35c19459ec82e8b7d5ec406b2e19d0b5f57cab8/Pong9_collision.py#L3

                # When moving right...
                if self.ball.rect.colliderect(self.right_paddle) and self.ball.is_moving_right():
                    self.right_paddle.sound.play()
                    # If the ball's right is past the paddle's left by < 10 pixels (not sure about that magic figure, but eh), reverse direction on the x axis (bounce back in play)
                    if abs(self.ball.rect.right - self.right_paddle.rect.left) < 10:
                        # If the ball hits the top third, send the ball back on an upwards trajectory
                        if self.ball.rect.centery < (self.right_paddle.rect.top + self.right_paddle.rect.height // 3):
                            if self.ball.y_speed == 0:
                                self.ball.y_speed = -self.ball.DEFAULT_Y_SPEED
                            else:
                                self.ball.y_speed = -abs(self.ball.y_speed)
                        # If the ball hits the bottom third send the ball back on a downwards trajectory
                        elif self.ball.rect.centery > (self.right_paddle.rect.top + 2 * (self.right_paddle.rect.height // 3)):
                            if self.ball.y_speed == 0:
                                self.ball.y_speed = self.ball.DEFAULT_Y_SPEED
                            else:
                                self.ball.y_speed = abs(self.ball.y_speed)
                        else:
                            self.ball.y_speed = 0
                        # Increases speed on flat shots (note there is nothing here to decrease it back!!!)
                        if self.ball.y_speed == 0:
                            self.ball.x_speed *= -3
                        else:
                            self.ball.x_speed *= -1
                    # Otherwise if the ball's bottom is past the paddle's top and the ball is on a downward trajectory, reverse direction on the y axis only (bounce off the top of the paddle)
                    elif abs(self.ball.rect.bottom - self.right_paddle.rect.top) < 10 and self.ball.y_speed > 0:
                        self.ball.y_speed *= -1
                    # Otherwise bounce off the bottom of the paddle
                    elif abs(self.ball.rect.top - self.right_paddle.rect.bottom) < 10 and self.ball.y_speed < 0:
                        self.ball.y_speed *= -1
                    # Otherwise go off-screen

                # When moving left...
                if self.ball.rect.colliderect(self.left_paddle) and self.ball.is_moving_left():
                    self.left_paddle.sound.play()
                    if abs(self.ball.rect.left - self.left_paddle.rect.right) < 10:
                        # If the ball hits the top third, send the ball back on an upwards trajectory
                        if self.ball.rect.centery < (self.right_paddle.rect.top + self.right_paddle.rect.height // 3):
                            if self.ball.y_speed == 0:
                                self.ball.y_speed = -self.ball.DEFAULT_Y_SPEED
                            else:
                                self.ball.y_speed = -abs(self.ball.y_speed)
                        # If the ball hits the bottom thirdm send the ball back on a downwards trajectory
                        elif self.ball.rect.centery > (self.right_paddle.rect.top + 2 * (self.right_paddle.rect.height // 3)):
                            if self.ball.y_speed == 0:
                                self.ball.y_speed = self.ball.DEFAULT_Y_SPEED
                            else:
                                self.ball.y_speed = abs(self.ball.y_speed)
                        else:
                            self.ball.y_speed = 0
                        # Increases speed on flat shots (note there is nothing here to decrease it back!!!)
                        if self.ball.y_speed == 0:
                            self.ball.x_speed *= -3
                        else:
                            self.ball.x_speed *= -1
                        
                    elif abs(self.ball.rect.bottom - self.left_paddle.rect.top) < 10 and self.ball.y_speed > 0:
                        self.ball.y_speed *= -1
                    elif abs(self.ball.rect.top - self.left_paddle.rect.bottom) < 10 and self.ball.y_speed < 0:
                        self.ball.y_speed *= -1
                    
        
            if self.left_paddle.wins():
                self.playing = False
                # TODO, pass this directly to the game over screen instead somehow
                self.match.message = "Player 1 Wins!"
                
            elif self.right_paddle.wins():
                self.playing = False
                # TODO, pass this directly to the game over screen instead somehow
                self.match.message = "You Lose" if isinstance(self.right_paddle, AIPaddle) else "Player 2 Wins!"

    def draw(self):
        self.application.screen.fill(GREY if self.paused else BLACK)
        self.application.screen.blit(self.divisor_surface, (WINDOW_CENTER_WIDTH, 0))
        
        for game_object in self._get_game_objects():
            if game_object:
                game_object.draw(self.application.screen)

        self._draw_scores()

        if not self.playing:\
            self.application.application_state = GameOver(self.application, self.match.message)
            
        if self.application.debug_mode:
            move_up_logic = self.ball.rect.top < self.right_paddle.rect.centery
            move_down_logic = self.ball.rect.bottom > self.right_paddle.rect.centery
            debug(f"{self.application.game_type=}")
            debug(f"{self.ball.rect.top=} {self.right_paddle.rect.centery=}, {move_up_logic=}", 30)
            debug(f"{self.ball.rect.bottom=}  {self.right_paddle.rect.centery=}, {move_down_logic=}", 60)
            debug(f"{self.ball.x_speed=}", 90)
            debug(f"{self.right_paddle.rect.top=}", 120)
            debug(f"{self.right_paddle.rect.bottom=}", 150)
            
        pygame.display.update()
        self.application.clock.tick(FPS)

    def _draw_scores(self):
        """Draw scores to screen"""
        self.left_score_surface = self.application.font.render(f"{self.left_paddle.score}", True, WHITE)
        self.application.screen.blit(self.left_score_surface, (WINDOW_CENTER_WIDTH - 70, 30))
        
        self.right_score_surface = self.application.font.render(f"{self.right_paddle.score}", True, WHITE)
        self.application.screen.blit(self.right_score_surface, (WINDOW_CENTER_WIDTH + 6, 30))

    def _get_game_objects(self):
        game_objects = [self.ball, self.left_paddle, self.right_paddle]
        
        return game_objects


class OnePlayerGame(MainGame):
    def __init__(self, application):
        super().__init__(application, ONE_PLAYER)
        
    def _create_paddles(self):
        super()._create_paddles()

class TwoPlayerGame(MainGame):
    def __init__(self, application):
        super().__init__(application, TWO_PLAYERS)
    
    def _create_paddles(self):
        self.left_paddle = Paddle(x=30, y=WINDOW_CENTER_HEIGHT)
        self.right_paddle = Paddle(x=WINDOW_WIDTH - 30, y=WINDOW_CENTER_HEIGHT)
