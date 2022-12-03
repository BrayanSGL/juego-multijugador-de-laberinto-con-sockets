import pygame
import random
from network import Network
from settings import WORLD_MAP, TILE_SIZE, FREE_COORDINATES, TITLE, FPS


class Player():
    width = height = TILE_SIZE

    def __init__(self, start_pos):
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.image ={
            'up': pygame.transform.scale(pygame.image.load('assets/player/back.png'), (TILE_SIZE,TILE_SIZE)),
            'down': pygame.transform.scale(pygame.image.load('assets/player/front.png'), (TILE_SIZE,TILE_SIZE)),
            'left': pygame.transform.scale(pygame.image.load('assets/player/left.png'), (TILE_SIZE,TILE_SIZE)),
            'right': pygame.transform.scale(pygame.image.load('assets/player/right.png'), (TILE_SIZE,TILE_SIZE))
        }
        print(self.x, self.y)

    def draw(self, screen, direction):
        screen.blit(self.image[direction], (self.x, self.y))



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
        direction = ['up', 'down', 'left', 'right']
        direction_str = 'down'
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
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                direction_str = direction[2]
                self.player.x -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                direction_str = direction[3]
                self.player.x += 1
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                direction_str = direction[0]
                self.player.y -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                direction_str = direction[1]
                self.player.y += 1


            # Update canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas(),direction_str)
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
        # for row in range(len(WORLD_MAP)):
        #     for col in range(len(WORLD_MAP[row])):
        #         tile = WORLD_MAP[row][col]
        #         self.screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))
