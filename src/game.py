import pygame, random
from network import Network
from settings import WORLD_MAP,TILE_SIZE, FREE_COORDINATES, TITLE

class Player():
    width = height = TILE_SIZE
    def __init__(self, start_pos):
        self.x = start_pos[0]
        self.y = start_pos[1]
        print(self.x, self.y)

class Game:
    def __init__(self,width,height):
        self.network = Network()
        self.width = width
        self.height = height
        self.player = Player(FREE_COORDINATES[random.randint(0, len(FREE_COORDINATES) - 1)])
        self.canvas = Canvas(self.width, self.height, TITLE)

    def run(self):
        print(self.width,self.height)
        #print(WORLD_MAP)


class Canvas:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)