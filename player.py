import pygame
from projectile import Projectile
#Classe joueur #
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.max_health = 3
        self.attack = 10
        self.velocity = 3
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/vaisseaux/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = 129
        self.rect.y = 500
        self.shoot_delay = 150
        self.last_shoot =  pygame.time.get_ticks()
    def launch_projectile(self):
        #Création nouvelle instance du projectile#
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.all_projectiles.add(Projectile(self))
            self.last_shoot = now
    def move_right(self):
        self.rect.x += self.velocity
        self.image = pygame.image.load('assets/vaisseaux/right.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
    def move_left(self):
        self.rect.x -= self.velocity
        self.image = pygame.image.load('assets/vaisseaux/left.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_up(self):
        self.rect.y -= self.velocity
        self.image = pygame.image.load('assets/vaisseaux/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_down(self):
        self.rect.y += self.velocity
        self.image = pygame.image.load('assets/vaisseaux/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def no_move(self):
        self.image = pygame.image.load('assets/vaisseaux/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))