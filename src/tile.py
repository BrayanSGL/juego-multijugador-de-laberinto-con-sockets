import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image_big = pygame.image.load('assets\environment\wall.png')
        self.image = pygame.transform.scale(self.image_big, (TILE_SIZE, TILE_SIZE)).convert_alpha() #convert_alpha() is used to make the image transparent
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        