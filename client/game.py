import pygame
import random
import sys
from client_setup import *
from network import Network


class Player:
    width = height = TILE_SIZE

    def __init__(self, free_coordinates, wall_coordinates, chest_coordinates):
        self.free_coordinates = free_coordinates
        self.wall_coordinates = wall_coordinates
        self.chest_coordinates = chest_coordinates
        self.x = random.choice(self.free_coordinates)[0]
        self.y = random.choice(self.free_coordinates)[1]
        self.image = {
            "up": pygame.transform.scale(pygame.image.load("Client/assets/player/back.png"), (TILE_SIZE, TILE_SIZE)),
            "down": pygame.transform.scale(pygame.image.load("Client/assets/player/front.png"), (TILE_SIZE, TILE_SIZE)),
            "left": pygame.transform.scale(pygame.image.load("Client/assets/player/left.png"), (TILE_SIZE, TILE_SIZE)),
            "right": pygame.transform.scale(pygame.image.load("Client/assets/player/right.png"), (TILE_SIZE, TILE_SIZE))
        }
        self.wall_image = pygame.transform.scale(pygame.image.load(
            "Client/assets/map/wall.png"), (TILE_SIZE, TILE_SIZE))
        self.chest_image = pygame.transform.scale(pygame.image.load(
            "Client/assets/map/chest.png"), (TILE_SIZE, TILE_SIZE))

        # Utilizables
        self.msg = "intro"
        self.found_walls = []
        self.found_chests = []

    def draw(self, window, direction) -> None:
        window.blit(self.image[direction],
                    (self.x*TILE_SIZE, self.y*TILE_SIZE))

        for wall in self.found_walls:
            window.blit(self.wall_image,
                        (wall[0]*TILE_SIZE, wall[1]*TILE_SIZE))

        for chest in self.found_chests:
            window.blit(self.chest_image,
                        (chest[0]*TILE_SIZE, chest[1]*TILE_SIZE))

    def move(self, direction) -> None:
        move_sound = pygame.mixer.Sound("Client/assets/sounds/move.wav")
        move_sound.play()

        free_coordinates = self.free_coordinates
        wall_coordinates = self.wall_coordinates
        chest_coordinates = self.chest_coordinates

        if direction == "up" and (self.x, self.y-1) in free_coordinates:
            self.y -= 1
        elif direction == "down" and (self.x, self.y+1) in free_coordinates:
            self.y += 1
        elif direction == "left" and (self.x-1, self.y) in free_coordinates:
            self.x -= 1
        elif direction == "right" and (self.x+1, self.y) in free_coordinates:
            self.x += 1
        else:
            if direction == "up" and (self.x, self.y-1) in wall_coordinates:
                self.found_walls.append((self.x, self.y-1))
            elif direction == "down" and (self.x, self.y+1) in wall_coordinates:
                self.found_walls.append((self.x, self.y+1))
            elif direction == "left" and (self.x-1, self.y) in wall_coordinates:
                self.found_walls.append((self.x-1, self.y))
            elif direction == "right" and (self.x+1, self.y) in wall_coordinates:
                self.found_walls.append((self.x+1, self.y))

            if direction == "up" and (self.x, self.y-1) in chest_coordinates:
                self.found_chests.append((self.x, self.y-1))
                self.msg = "chest"
            elif direction == "down" and (self.x, self.y+1) in chest_coordinates:
                self.found_chests.append((self.x, self.y+1))
                self.msg = "chest"
            elif direction == "left" and (self.x-1, self.y) in chest_coordinates:
                self.found_chests.append((self.x-1, self.y))
                self.msg = "chest"
            elif direction == "right" and (self.x+1, self.y) in chest_coordinates:
                self.found_chests.append((self.x+1, self.y))
                self.msg = "chest"


class Game:
    def __init__(self, width, height) -> None:
        pygame.init()
        self.width = width
        self.height = height
        self.network = Network()
        self.player = Player(self.network.free_coordinates,
                             self.network.wall_coordinates, self.network.chest_coordinates)
        self.canvas = Canvas(self.width, self.height, TITLE)

    # Intro
    def intro(self) -> bool:
        self.canvas.draw_intro(15)
        pygame.display.update()
        clock = pygame.time.Clock()
        while True:
            clock.tick(1)
            msg_server = self.send_data().split(":")[2]
            print(msg_server)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    self.player.msg = "start"
                    self.send_data()
                    # cuenta regresiva de 15 segundos
                    self.canvas.draw_intro(15)
                    for i in range(15):
                        self.canvas.draw_intro(15-i)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        self.canvas.draw_background()
                        # Procesamiento de eventos del juego dentro del bucle de cuenta regresiva
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    return True

    def run(self) -> None:
        directions = ["up", "down", "left", "right"]
        direction = random.choice(directions)
        ambinet_sound = pygame.mixer.Sound("Client/assets/sounds/ambient.wav")
        ambinet_sound.play(-1)
        clock = pygame.time.Clock()
        run = self.intro()
        self.player.msg = "playing"
        while run:
            clock.tick(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        direction = "up"
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        direction = "down"
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        direction = "left"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        direction = "right"
                    elif event.key == pygame.K_SPACE:
                        self.player.move(direction)

            self.send_data()
            self.canvas.draw_background()
            self.player.draw(self.canvas.window, direction)
            self.canvas.update()

        ambinet_sound.stop()
        pygame.quit()

    def send_data(self) -> str:
        data = str(self.network.id)+':'+str(self.player.x)+',' + \
            str(self.player.y)+':'+str(self.player.msg)
        return self.network.send(data)


class Canvas:
    def __init__(self, width, height, title) -> None:
        self.width = width
        self.height = height
        self.title = title
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    @staticmethod
    def update() -> None:
        pygame.display.update()

    def draw_text(self, txt, size, color, y) -> None:
        font = pygame.font.SysFont("comicsansms", size)
        text = font.render(txt, 1, color)
        self.window.blit(text, (WIDTH/2-text.get_width()/2, y))

    def get_canvas(self) -> pygame.display:
        return self.window

    def draw_background(self) -> None:
        self.window.fill(BLACK)

    def draw_intro(self, time_left) -> None:
        if time_left != 15:
            self.draw_text("Maze Game", 55, RED, 150)
            self.draw_text("Tiempo restante: "+str(time_left), 40, WHITE, 350)
        else:
            self.draw_text("Maze Game", 55, RED, 150)
            self.draw_text("Presione 'i' para iniciar", 40, WHITE, 300)
            self.draw_text("Presione ESC para salir", 40, WHITE, 400)

    def draw_winner(self, winner) -> None:
        self.draw_text("Winner: "+winner, 55, RED, 150)
        self.draw_text("Press ESC to Exit", 40, WHITE, 400)

    def draw_loser(self, loser) -> None:
        self.draw_text("Loser: "+loser, 55, RED, 150)
        self.draw_text("Press ESC to Exit", 40, WHITE, 400)
