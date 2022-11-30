import pygame
from pygame.locals import *
from settings import TILE_SIZE, WORLD_MAP
import player

class Level:
    def __init__(self, screen):
        self.screen = screen
        self.wall_list = pygame.sprite.Group()
        self.image_map = pygame.transform.scale(pygame.image.load('assets/map/wall.png'), (TILE_SIZE, TILE_SIZE))
        self.image_chest = pygame.transform.scale(pygame.image.load('assets/map/chest.png'), (TILE_SIZE, TILE_SIZE))
        
    
        #self.draw_map()


    def draw_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, tile in enumerate(row):
                if tile == 'X':
                    self.screen.blit(self.image_map, (col_index * TILE_SIZE, row_index * TILE_SIZE))
                elif tile == 'C':
                    self.screen.blit(self.image_chest, (col_index * TILE_SIZE, row_index * TILE_SIZE))
                elif tile == 'P':
                    self.screen.blit(self.image_chest, (col_index * TILE_SIZE, row_index * TILE_SIZE))
