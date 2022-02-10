from pygame import Vector2

# Some basics
FPS = 60
WIN_SCORE = 5


# Some dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_CENTER_WIDTH = WINDOW_WIDTH // 2
WINDOW_CENTER_HEIGHT = WINDOW_HEIGHT // 2
WINDOW_CENTER = (WINDOW_CENTER_WIDTH, WINDOW_CENTER_HEIGHT)


# Some colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (204, 204, 204)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


# Some mathy stuff
PADDLE_SPEED = 10
BALL_SPEED = 5

Y_MAGNITUDE = 10
UP = Vector2(0, -Y_MAGNITUDE)
DOWN = Vector2(0, Y_MAGNITUDE)


# Some strings
TITLE = "Pong!"
LEFT = "left"
RIGHT = "right"
ONE_PLAYER = "1 Player"
TWO_PLAYERS = "2 Players"
CREDITS = "Credits"
QUIT = "Quit"