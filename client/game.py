import pygame
import random
from network import Network
from settings_client import *


class Player():
    width = height = TILE_SIZE

    def __init__(self, start_pos):
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.image = {
            'up': pygame.transform.scale(pygame.image.load('assets/player/back.png'), (TILE_SIZE, TILE_SIZE)),
            'down': pygame.transform.scale(pygame.image.load('assets/player/front.png'), (TILE_SIZE, TILE_SIZE)),
            'left': pygame.transform.scale(pygame.image.load('assets/player/left.png'), (TILE_SIZE, TILE_SIZE)),
            'right': pygame.transform.scale(pygame.image.load('assets/player/right.png'), (TILE_SIZE, TILE_SIZE))
        }

        self.msg = 'intro'  # // exit, intro, playing, win, lose

    def draw(self, screen, direction):
        screen.blit(self.image[direction],
                    (self.x*TILE_SIZE, self.y*TILE_SIZE))

    def move(self, direction):
        if direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1


class Game:
    def __init__(self, width, height):
        self.network = Network()
        self.width = width
        self.height = height
        self.player = Player(self.network.free_coordinates[random.randint(
            0, len(self.network.free_coordinates) - 1)])
        self.canvas = Canvas(self.width, self.height, TITLE)

    def run(self):
        direction = ['up', 'down', 'left', 'right']
        direction_str = direction[random.randint(0, 3)]
        print(self.width, self.height)
        clock = pygame.time.Clock()
        is_running = True
        while is_running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                    is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction_str = 'up'
                    elif event.key == pygame.K_DOWN:
                        direction_str = 'down'
                    elif event.key == pygame.K_LEFT:
                        direction_str = 'left'
                    elif event.key == pygame.K_RIGHT:
                        direction_str = 'right'
                    elif event.key == pygame.K_SPACE:
                        self.player.move(direction_str)

            self.send_data()
            # Update canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas(), direction_str)
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        data = self.network.send(str(
            self.network.id)+':'+str(self.player.x)+','+str(self.player.y)+':'+self.player.msg)
        return self.network.send(data)


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
        # for row in range(len(WORLD_MAP)):
        #     for col in range(len(WORLD_MAP[row])):
        #         tile = WORLD_MAP[row][col]
        #         self.screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))
