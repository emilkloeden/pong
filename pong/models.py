import pygame
from pygame.math import Vector2

from constants import RIGHT, WHITE, WIN_SCORE, WINDOW_CENTER_HEIGHT, WINDOW_HEIGHT
from utils import load_sound

class GameObject:
    # def __init__(self, position, sprite):
    #     self.position = Vector2(position)
    #     self.sprite = sprite
    #     self.radius = sprite.get_width() // 2


    # def draw(self, surface):
    #     surface.blit(self.sprite, self.position)
    def __init__(self, x, y, surface):
        self.surface = surface
        self.rect = surface.get_rect()
        self.radius = surface.get_width() // 2
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.surface, (self.rect.x, self.rect.y))
        


class Paddle(GameObject):
    WIDTH = 10
    HEIGHT = 100
    SPEED = 5
    
    def __init__(self, x, y):
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.sound = load_sound("laser")
        self.score = 0
        self.rect = pygame.rect.Rect((x, y), (self.width, self.height))
        self.surface = pygame.Surface((self.width, self.height))
        
        self.surface.fill(WHITE)

        self.rect = self.surface.get_rect()

        self.rect.x = x
        self.rect.y = y
        # super().__init__((x, y), self.surface)
        super().__init__(x, y, self.surface)

    
    def move(self, direction):
        if self._can_move(direction):
            self._move(direction)


    def _can_move(self, direction):
        if direction.y > 0:
            return self._can_move_down()
        return self._can_move_up()


    def _can_move_down(self):
        return self.rect.bottom < WINDOW_HEIGHT

    def _can_move_up(self):
        return self.rect.top > 0

    def _move(self, direction):
        # x is redundant here
        # self.position += direction
        self.rect.y += direction.y


    def wins(self):
        return self.score >= WIN_SCORE


class AIPaddle(Paddle):
    def __init__(self, x, y, match):
        self.match = match
        self.SPEED = 5
        super().__init__(x, y)

    def move(self, _=None):
        # If ball is moving towards the AI player, track Ball on Y axis (assumes AI player is on the right)
        if self.match.ball.is_moving_right():
            self._move_towards_ball()
        # Else move towards the center
        else:
            self._move_towards_center()


    def _the_ball_is_moving_right(self):
        return self.match.ball.x_speed > 0
        

    def _move_towards_ball(self):
        if self._is_above_ball(): # and self.rect.bottom >= WINDOW_HEIGHT:
            if self._can_move_down():
                self._move_down(self.SPEED)
        elif self._is_below_ball(): # and self.rect.top >= 0:
            if self._can_move_up():
                self._move_up(self.SPEED)
        

    def _is_above_ball(self):
        return self.rect.centery < self.match.ball.rect.bottom 

    
    def _is_below_ball(self):
        return self.rect.centery > self.match.ball.rect.top


    def _move_down(self, magnitude):
        # self.position.y += magnitude
        self.rect.y += magnitude
    
    
    def _move_up(self, magnitude):
        # self.position.y -= magnitude
        self.rect.y -= magnitude

        
    def _move_towards_center(self):
        desired_speed = self.SPEED // 2
        if self._is_above_window_center():
            if self._can_move_down():
                self._move_down(desired_speed)
        elif self._is_below_window_center():
            if self._can_move_up():
                self._move_up(desired_speed)
    
    
    def _is_above_window_center(self):
        return self.rect.centery < WINDOW_CENTER_HEIGHT

    
    def _is_below_window_center(self):
        return self.rect.centery > WINDOW_CENTER_HEIGHT
                    

class Ball(GameObject): 
    WIDTH = 10
    HEIGHT = 10
    DEFAULT_X_SPEED = 5
    DEFAULT_Y_SPEED = 5
    
    def __init__(self, x, y, initial_movement_direction):
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.rect = pygame.rect.Rect((x, y), (self.width, self.height))
        self.surface = pygame.Surface((self.width, self.height))
        
        self.surface.fill(WHITE)

        self.rect = self.surface.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.x_speed = self.DEFAULT_X_SPEED if initial_movement_direction == RIGHT else self.DEFAULT_X_SPEED * -1
        self.y_speed = self.DEFAULT_Y_SPEED if initial_movement_direction == RIGHT else self.DEFAULT_Y_SPEED * -1

        # super().__init__((x, y), self.surface)
        super().__init__(x, y, self.surface)


    def move(self):
        if self._will_hit_ceiling_or_floor():
            self._reflect() 
        
        self._move()

    
    def _move(self):
        # self.position += self.velocity
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        # self.position.x += self.x_speed
        # self.position.y += self.y_speed

    def is_moving_left(self) -> bool:
        return self.x_speed < 0

    
    def is_moving_right(self) -> bool:
        return self.x_speed > 0

    def _will_hit_ceiling_or_floor(self) -> bool:
        return self.rect.bottom > WINDOW_HEIGHT or 0 > self.rect.top
        
    
    def _reflect(self):
        self.y_speed *= -1

    
