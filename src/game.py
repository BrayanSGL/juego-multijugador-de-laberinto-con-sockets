import pygame
import random
from network import Network
from settings import WORLD_MAP, TILE_SIZE, FREE_COORDINATES, TITLE, FPS


class Player():
    width = height = TILE_SIZE

    def __init__(self, start_pos):
        self.x = start_pos[0]
        self.y = start_pos[1]
        print(self.x, self.y)


class Game:
    def __init__(self, width, height):
        #self.network = Network()
        self.width = width
        self.height = height
        self.player = Player(
            FREE_COORDINATES[random.randint(0, len(FREE_COORDINATES) - 1)])
        self.canvas = Canvas(self.width, self.height, TITLE)

    def run(self):
        print(self.width, self.height)
        clock = pygame.time.Clock()
        is_running = True
        while is_running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.K_ESCAPE:
                    is_running = False

            keys = pygame.key.get_pressed()

            # Player movement with WASD or arrow keys

            # Update canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        pass

class Canvas:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    @staticmethod 
    def update():
        pygame.display.update()

    def draw_text(self, text, size, color, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size, True)
        text = font.render(text, 1, color)

        self.screen.blit(text, (x, y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((0, 0, 0))
        for row in range(len(WORLD_MAP)):
            for col in range(len(WORLD_MAP[row])):
                tile = WORLD_MAP[row][col]
                self.screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))
