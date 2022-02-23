import pygame
from random import randint
from laser_ennemie import Laser_ennemie


#Classe du monstre#
class Monster(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 30
        self.max_health = 30
        self.attack = 30
        self.all_laser = pygame.sprite.Group()
        self.image = pygame.image.load('assets/vaisseaux/ennemies/enemy-01/nomove.png')
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.x = randint(-15,360)
        self.rect.y = -10
        self.velocity = 1

    def damage(self, amount) :
        self.health -= amount
        if self.health <= 0:
            self.game.all_monsters.remove(self)
            self.game.player.score += 5

    def forward(self):
        self.rect.y += self.velocity

    def launch_laser(self) :
        self.all_laser.add(Laser_ennemie(self))



