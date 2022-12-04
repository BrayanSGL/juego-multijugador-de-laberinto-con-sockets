import pygame
import random
from network import Network
from settings import WORLD_MAP, TILE_SIZE, FREE_COORDINATES, TITLE, FPS


class Player():
    width = height = TILE_SIZE

    def __init__(self, start_pos):
        self.x = start_pos[0] * TILE_SIZE  # revisar + TILE_SIZE // 2
        self.y = start_pos[1] * TILE_SIZE + 10  # +10 to make it look better
        self.image = {
            'up': pygame.transform.scale(pygame.image.load('assets/player/back.png'), (TILE_SIZE, TILE_SIZE)),
            'down': pygame.transform.scale(pygame.image.load('assets/player/front.png'), (TILE_SIZE, TILE_SIZE)),
            'left': pygame.transform.scale(pygame.image.load('assets/player/left.png'), (TILE_SIZE, TILE_SIZE)),
            'right': pygame.transform.scale(pygame.image.load('assets/player/right.png'), (TILE_SIZE, TILE_SIZE))
        }
        self.status = 'intro'  # // intro, playing, win, lose

    def draw(self, screen, direction):
        screen.blit(self.image[direction], (self.x, self.y))

    def move(self, direction):
        if direction == 'up':
            self.y -= self.height
        elif direction == 'down':
            self.y += self.height
        elif direction == 'left':
            self.x -= self.width
        elif direction == 'right':
            self.x += self.width


class Game:
    def __init__(self, width, height):
        self.network = Network()
        self.width = width
        self.height = height
        self.player = Player(
            FREE_COORDINATES[random.randint(0, len(FREE_COORDINATES) - 1)])
        self.canvas = Canvas(self.width, self.height, TITLE)

    def intro(self, clock):
        pygame.init()
        is_running = True
        # fonts
        little = pygame.font.SysFont('comicsansms', 20)
        medium = pygame.font.SysFont('comicsansms', 40)
        big = pygame.font.SysFont('comicsansms', 55)
        while is_running:
            clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.K_ESCAPE:
                    is_running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_i] or self.player.status == 'playing':
                self.player.status = 'playing'
                is_running = False
                server_data = self.send_data() # 'id,playing:x,y' estraer playing
                server_data = server_data.split(':') # ['id,playing', 'x,y']
                server_data = server_data[0].split(',') # ['id', 'playing']
                print(server_data)
                if server_data[1] == 'playing':  # cambiar
                    # Cuenta regresiva de 15 segundos
                    for i in range(15, 0, -1):
                        self.canvas.draw_background()
                        text = big.render(
                            'Welcome to the game', 1, (255, 0, 0))
                        self.canvas.get_canvas().blit(text, (self.width // 2 - text.get_width() // 2, 200))
                        text = little.render(
                            f'Time to start {i} seconds', 1, (255, 255, 255))
                        self.canvas.get_canvas().blit(text, (self.width // 2 - text.get_width() // 2, 300))
                        self.canvas.update()
                        if keys[pygame.K_a]:
                            print('a')
                        pygame.time.delay(1000)

                return True
            if keys[pygame.K_q]:
                is_running = False
                return False
            
            if self.send_data() == 'p,playing:0,0':
                self.player.status = 'playing'

            self.canvas.draw_background()
            text = big.render('Welcome to the game', 1, (255, 0, 0))
            self.canvas.get_canvas().blit(text, (self.width // 2 - text.get_width() // 2, 200))
            text = medium.render('Press "i" to play', 1, (255, 255, 255))
            self.canvas.get_canvas().blit(text, (self.width // 2 - text.get_width() // 2, 300))
            text = medium.render('Press "q" to quit', 1, (255, 255, 255))
            self.canvas.get_canvas().blit(text, (self.width // 2 - text.get_width() // 2, 400))
            self.canvas.update()

    def run(self):
        direction = ['up', 'down', 'left', 'right']
        direction_str = direction[random.randint(0, 3)]
        print(self.width, self.height)
        clock = pygame.time.Clock()
        is_running = self.intro(clock)
        while is_running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.network.send('q')
                    is_running = False
                if event.type == pygame.K_ESCAPE:
                    self.network.send('q')
                    is_running = False

            keys = pygame.key.get_pressed()
            # Player movement with WASD or arrow keys
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                direction_str = direction[2]
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                direction_str = direction[3]
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                direction_str = direction[0]
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                direction_str = direction[1]

            # Que se mueva el player con espacio solo una vez y no se quede presionado
            if keys[pygame.K_SPACE]:
                self.player.move(direction_str)

            self.send_data()
            # Update canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas(), direction_str)
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        data = str(self.network.id) + ',' + str(self.player.status) + \
            ':' + str(self.player.x) + ',' + str(self.player.y)
        return self.network.send(data)

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0, 0


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
