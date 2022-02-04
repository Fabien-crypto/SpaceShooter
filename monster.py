import pygame
from random import randint
from laser_ennemie import Laser_ennemie

class Monster(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 10
        self.max_health = 10
        self.attack = 5
        self.all_laser = pygame.sprite.Group()
        self.image = pygame.image.load('assets/vaisseaux/ennemies/enemy-01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = randint(0,400)
        self.rect.y = -10
        self.velocity = 1

    def forward(self):
        self.rect.y += self.velocity
    def launch_laser(self) :
        self.all_laser.add(Laser_ennemie(self))


