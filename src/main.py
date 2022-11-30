import pygame
import sys
from settings import TITLE,WIDTH,HEIGHT,FPS,BLACK
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.level = Level(self.screen)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.events()
            self.screen.fill(BLACK)
            self.level.draw_map()
            pygame.display.update()  # permite que se actualice la pantalla
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
