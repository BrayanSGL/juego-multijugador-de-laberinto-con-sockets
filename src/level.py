import pygame
from settings import *
from tile import Tile

class Level:
    def __init__(self):
        # Sprite groups setup
        self.p2Pos = None
        self.string = None
        self.visible_sprite = YSortCameraGroup()
        self.obstacle_sprite = pygame.sprite.Group()
        # Sockets part self.net = Network()
        self.p1 = []

        # Sprite group
        self.create_map()
    
    def create_map(self):
        # Create map
        for row_index, row in enumerate(WORLD_MAP):
            for column_index, col in enumerate(row):
                x = column_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'X':
                    Tile((x, y),[self.visible_sprite, self.obstacle_sprite])
                    pass
                elif col == 'P':
                    # Create player
                    pass
                elif col == 'C':
                    # Create chest
                    pass

    def read_pos(self, string):
        string = string.split(",") # string = [x, y]
        return int(string[0]), int(string[1]) #nos regresa la posicion del jugador 

    def make_pos(self, tuple):
        return str(tuple[0]) + "," + str(tuple[1]) #nos regresa la posicion del jugador en string

    def run(self):
        # Draw map
        #self.visible_sprite.draw(self.player1, self.player2)
        #self.visible_sprite.custome_draw(self.screen)
        pass


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #General setup
        super().__init__()

        #Get the display surface
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()