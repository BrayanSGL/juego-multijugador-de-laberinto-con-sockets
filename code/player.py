import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacule_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets/delta/right.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -26)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacle_sprites = obstacule_sprites

        #cambio de mirada
        #mobimiento asdw
        def input(self):
            keys = pygame.key.get_pressed()
            #X axis
            if keys[pygame.K_a]:
                self.direction.x = -1
                self.image = pygame.image.load('assets/delta/left.png').convert_alpha()
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.image = pygame.image.load('assets/delta/right.png').convert_alpha()
            else:
                self.direction.x = 0
            #Y axis
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.image = pygame.image.load('assets/delta/back.png').convert_alpha()
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.image = pygame.image.load('assets/delta/front.png').convert_alpha()
            else:
                self.direction.y = 0

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision('Horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('Vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'Horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(sprite.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'Vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(sprite.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                   
           