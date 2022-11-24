# game setup

# screen
WIDTH = 800
HEIGHT = 600
TITLE = "Laberinto"
FPS = 60
TILE_SIZE = 50
BLACK = (0, 0, 0)

# Map is a matrix of 12x12
WORLD_MAP = [
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'P', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
    ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', 'X', 'X'],
    ['X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
    ['X', ' ', ' ', ' ', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X'],
    ['X', ' ', 'X', ' ', ' ', 'C', ' ', ' ', ' ', ' ', ' ', 'X'],
    ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
    ['X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', ' ', 'X', ' ', 'X'],
    ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ', 'X', ' ', 'X'],
    ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', ' ', 'X'],
    ['X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
]