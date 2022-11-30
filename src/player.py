import pygame
from settings import TILE_SIZE


class Player():
    def __init__(self,screen) -> None:
        self.sprites = {
            'back': pygame.transform.scale(pygame.image.load('assets/player/back.png'), (TILE_SIZE, TILE_SIZE)),
            'front': pygame.transform.scale(pygame.image.load('assets/player/front.png'), (TILE_SIZE, TILE_SIZE)),
            'left': pygame.transform.scale(pygame.image.load('assets/player/left.png'), (TILE_SIZE, TILE_SIZE)),
            'right': pygame.transform.scale(pygame.image.load('assets/player/right.png'), (TILE_SIZE, TILE_SIZE))
        }
        self.screen = screen
        self.position = [0, 0]

    def input(self, x, y):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.screen.blit(self.sprites['back'], (x, y))
        elif keys[pygame.K_DOWN]:
            self.screen.blit(self.sprites['front'], (x, y))
        elif keys[pygame.K_LEFT]:
            self.screen.blit(self.sprites['left'], (x, y))
        elif keys[pygame.K_RIGHT]:
            self.screen.blit(self.sprites['right'], (x, y))