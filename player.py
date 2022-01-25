import pygame
from projectile import Projectile
#Classe joueur #
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.max_health = 3
        self.attack = 10
        self.velocity = 2.7
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/vaisseaux/_0000_Layer-1.png')
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = 129
        self.rect.y = 500
    def launch_projectile(self):
        #Création nouvelle instance du projectile#
        self.all_projectiles.add(Projectile(self))

    def move_right(self):
        self.rect.x += self.velocity
        self.image = pygame.image.load('assets/vaisseaux/_0003_Layer-3.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_left(self):
        self.rect.x -= self.velocity
        self.image = pygame.image.load('assets/vaisseaux/_0001_Layer-2.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_up(self):
        self.rect.y -= self.velocity
        self.image = pygame.image.load('assets/vaisseaux/_0000_Layer-1.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_down(self):
        self.rect.y += self.velocity
        self.image = pygame.image.load('assets/vaisseaux/_0000_Layer-1.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def no_move(self):
        self.image = pygame.image.load('assets/vaisseaux/_0000_Layer-1.png')
        self.image = pygame.transform.scale(self.image, (80,80))