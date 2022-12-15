import pygame
import random
import sys
from network import Network
from settings_client import *


class Player():
    width = height = TILE_SIZE

    def __init__(self, free_coordinates, wall_coordinates, chest_coordinates):
        self.free_coordinates = free_coordinates
        self.wall_coordinates = wall_coordinates
        self.chest_coordinates = chest_coordinates
        self.x = random.choice(free_coordinates)[0]
        self.y = random.choice(free_coordinates)[1]
        self.image = {
            'up': pygame.transform.scale(pygame.image.load('assets/player/back.png'), (TILE_SIZE, TILE_SIZE)),
            'down': pygame.transform.scale(pygame.image.load('assets/player/front.png'), (TILE_SIZE, TILE_SIZE)),
            'left': pygame.transform.scale(pygame.image.load('assets/player/left.png'), (TILE_SIZE, TILE_SIZE)),
            'right': pygame.transform.scale(pygame.image.load('assets/player/right.png'), (TILE_SIZE, TILE_SIZE))
        }
        self.wall_image = pygame.transform.scale(
            pygame.image.load('assets/map/wall.png'), (TILE_SIZE, TILE_SIZE))
        self.chest_image = pygame.transform.scale(
            pygame.image.load('assets/map/chest.png'), (TILE_SIZE, TILE_SIZE))

        self.msg = 'intro'  # // exit, intro, playing, win, lose
        self.found_walls = []
        self.found_chest = []

    def draw(self, screen, direction) -> None:
        screen.blit(self.image[direction],
                    (self.x*TILE_SIZE, self.y*TILE_SIZE))
        for wall in self.found_walls:
            screen.blit(self.wall_image,
                        (wall[0]*TILE_SIZE, wall[1]*TILE_SIZE))
        for chest in self.found_chest:
            screen.blit(self.chest_image,
                        (chest[0]*TILE_SIZE, chest[1]*TILE_SIZE))

    def move(self, direction) -> None:
        move = pygame.mixer.Sound('assets/sounds/move.wav')
        move.play()
        free_coordinates = self.free_coordinates
        chest_coordinates = self.chest_coordinates
        wall_coordinates = self.wall_coordinates

        if direction == 'up' and (self.x, self.y - 1) in free_coordinates:
            self.y -= 1
        elif direction == 'down' and (self.x, self.y + 1) in free_coordinates:
            self.y += 1
        elif direction == 'left' and (self.x - 1, self.y) in free_coordinates:
            self.x -= 1
        elif direction == 'right' and (self.x + 1, self.y) in free_coordinates:
            self.x += 1
        else:
            if direction == 'up' and (self.x, self.y - 1) in wall_coordinates:
                self.found_walls.append((self.x, self.y - 1))
            elif direction == 'down' and (self.x, self.y + 1) in wall_coordinates:
                self.found_walls.append((self.x, self.y + 1))
            elif direction == 'left' and (self.x - 1, self.y) in wall_coordinates:
                self.found_walls.append((self.x - 1, self.y))
            elif direction == 'right' and (self.x + 1, self.y) in wall_coordinates:
                self.found_walls.append((self.x + 1, self.y))

            if direction == 'up' and (self.x, self.y - 1) in chest_coordinates:
                self.found_chest.append((self.x, self.y - 1))
                self.msg = 'win'
            elif direction == 'down' and (self.x, self.y + 1) in chest_coordinates:
                self.found_chest.append((self.x, self.y + 1))
                self.msg = 'win'
            elif direction == 'left' and (self.x - 1, self.y) in chest_coordinates:
                self.found_chest.append((self.x - 1, self.y))
                self.msg = 'win'
            elif direction == 'right' and (self.x + 1, self.y) in chest_coordinates:
                self.found_chest.append((self.x + 1, self.y))
                self.msg = 'win'


class Game:
    def __init__(self, width, height):
        self.network = Network()
        self.width = width
        self.height = height
        self.player = Player(self.network.free_coordinates,
                             self.network.wall_coordinates, self.network.chest_coordinates)
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

    def draw_win_or_lose(self, msg, winner) -> None:
        pygame.init()
        # fonts
        medium = pygame.font.SysFont('comicsansms', 40)
        big = pygame.font.SysFont('comicsansms', 55)
        self.canvas.draw_background()
        text = big.render(f'{msg}', True, (255, 0, 0))
        self.canvas.get_canvas().blit(text, (self.width/2 - text.get_width()/2, 200))
        text = medium.render(f'The winner is {winner}', True, (255, 255, 255))
        self.canvas.get_canvas().blit(text, (self.width/2 - text.get_width()/2, 300))
        text = medium.render('Press "q" to quit', True, (255, 255, 255))
        self.canvas.get_canvas().blit(text, (self.width/2 - text.get_width()/2, 400))
        self.canvas.update()

    def run(self) -> None:
        pygame.init()
        pygame.mixer.init()
        ambient = pygame.mixer.Sound('assets/sounds/ambient.wav')
        ambient.play(-1)

        direction = ['up', 'down', 'left', 'right']
        direction_str = direction[random.randint(0, 3)]
        clock = pygame.time.Clock()
        #is_running = self.intro(clock)
        is_running = True
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

            info_server = self.send_data()
            info_server = info_server.split(':')
            print(info_server, 'info_server')
            if info_server[2] == 'won':
                # self.player.found_chest.append(self.player.network.chest_coordinates)
                self.player.draw(self.canvas.get_canvas(), direction_str)
                self.canvas.update()
                if info_server[3] == str(self.network.id):
                    ambient.stop()
                    winner = pygame.mixer.Sound('assets/sounds/winner.wav')
                    winner.play()
                    pygame.time.delay(500)
                    while True:
                        self.draw_win_or_lose('You win', info_server[3])
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                                is_running = False
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                    is_running = False
                                    pygame.quit()
                                    sys.exit()
                else:
                    ambient.stop()
                    loser = pygame.mixer.Sound('assets/sounds/loser.wav')
                    loser.play()
                    while True:
                        self.draw_win_or_lose('You lose', info_server[3])
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                                is_running = False
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                    is_running = False
                                    pygame.quit()

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
