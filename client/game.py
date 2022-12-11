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

    def draw(self, screen, direction) -> None:
        screen.blit(self.image[direction],
                    (self.x*TILE_SIZE, self.y*TILE_SIZE))

    def move(self, direction) -> None:
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

    def draw_intro(self, time) -> None:
        pygame.init()
        # fonts
        little = pygame.font.SysFont('comicsansms', 20)
        medium = pygame.font.SysFont('comicsansms', 40)
        big = pygame.font.SysFont('comicsansms', 55)
        self.canvas.draw_background()
        text = big.render('Welcome to the game', True, (255, 0, 0))
        self.canvas.get_canvas().blit(text, (self.width/2 - text.get_width()/2, 200))
        text = medium.render('Press "i" to play', True, (255, 255, 255))
        self.canvas.get_canvas().blit(text, (self.width/2 - text.get_width()/2, 300))
        text = medium.render('Press "q" to quit', True, (255, 255, 255))
        self.canvas.get_canvas().blit(text, (self.width/2 - text.get_width()/2, 400))
        text = little.render(f'time to start T-{time}', True, (255, 255, 255))
        self.canvas.get_canvas().blit(text, (self.width/2 - text.get_width()/2, 500))
        self.canvas.update()

    def intro(self, clock) -> bool:
        while True:
            clock.tick(FPS)
            msg_server = self.send_data()
            msg_server = msg_server.split(':')
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.player.msg = 'exit'
                        self.send_data()
                        pygame.quit()
                        return False

                print(msg_server[2], 'msg_server')
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_i):
                    self.player.msg = 'start'
                    self.send_data()
                    while True:
                        server_data_time = self.send_data().split(':')
                        print(server_data_time[2], 'server_data_time')
                        server_data_time = int(server_data_time[2])
                        if server_data_time == 1:
                            return True
                        self.draw_intro(int(server_data_time))
            if msg_server[2] == 'start':
                self.player.msg = 'start'
                self.send_data()
                while True:
                    server_data_time = self.send_data().split(':')
                    print(server_data_time[2], 'server_data_time')
                    server_data_time = int(server_data_time[2])
                    if server_data_time == 1:
                        return True
                    self.draw_intro(int(server_data_time))

            # Update canvas in intro
            self.draw_intro(15)

    def run(self) -> None:
        direction = ['up', 'down', 'left', 'right']
        direction_str = direction[random.randint(0, 3)]
        clock = pygame.time.Clock()
        is_running = self.intro(clock)
        self.player.msg = 'playing'
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

    def send_data(self) -> str:
        data = str(self.network.id)+':'+str(self.player.x) + \
            ','+str(self.player.y)+':'+self.player.msg
        return self.network.send(data)


class Canvas:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    @staticmethod
    def update() -> None:
        pygame.display.update()

    def draw_text(self, text, size, color, x, y) -> None:
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size, True)
        text = font.render(text, 1, color)

        self.screen.blit(text, (x, y))

    def get_canvas(self) -> pygame.Surface:
        return self.screen

    def draw_background(self) -> None:
        self.screen.fill((0, 0, 0))
        # for row in range(len(WORLD_MAP)):
        #     for col in range(len(WORLD_MAP[row])):
        #         tile = WORLD_MAP[row][col]
        #         self.screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))
