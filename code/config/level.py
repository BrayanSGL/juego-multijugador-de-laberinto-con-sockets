import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):
        # Sprite groups setup
        self.positon_P2 = None
        self.string = None
        self.visible_sprite = Camera()
        self.obstacle_sprite = pygame.sprite.Group()
        ##Socket self.net
        self.P1 = []
        #Sprite setup
        self.create_mapa()
    
    def create_mapa(self):
        for rox_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = rox_index * TILE_SIZE
                if col == 'X':
                    Tile((x, y), [self.visible_sprite, self.obstacle_sprite])
                if col == 'P':
                    self.player1 = Player((x, y), [self.visible_sprite], self.obstacle_sprite)
                if col == 'Q':
                    self.player2 = Player((x, y), [self.visible_sprite], self.obstacle_sprite)
                    
    def read_pos(self, string):
        str = string.split(",")
        return int(str[0]), int(str[1])

    def make_pos(self, tup):
        return str(tup[0]) + "," + str(tup[1])

    def run(self):
        self.visible_sprite.custom.draw(self.player1, self.player2)
        #update and draw the game
        self.P1.insert(self.player1.rect.x, self.player1.rect.y)

        self.positon_P2 = self.read_pos(self.string)### network
        self.player2.hitbox.x = self.positon_P2[0]
        self.player2.hitbox.y = self.positon_P2[1]
        self.player2.update()
        self.visible_sprite.update()

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        
        #get the display surface
        self.display_superface = pygame.display.get_surface()
        self.half_width = self.display_superface.get_width() // 2
        self.half_height = self.display_superface.get_height() // 2
        self.offset = pygame.math.Vector2()