# Laberinto + sockets + threads + pygame + python 3.10
# Autors: Brayan Galeano Lara y Paula Anagones Murcia
# Date: November 2022

import pygame
import sys
import settings
import level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = level.Level()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

            self.screen.fill(settings.BLACK)
            pygame.display.update()
            # LEVEL
            self.clock.tick(settings.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
