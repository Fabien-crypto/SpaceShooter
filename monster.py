import pygame
from random import randint
from laser_ennemie import Laser_ennemie
import time
from explosion import Explosion

#Classe du monstre#
class Monster(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.explosion = pygame.mixer.Sound('sounds/ennemy_explosion.aiff')
        self.explosion.set_volume(0.5)
        self.health = 30
        self.max_health = 30
        self.attack = 10
        self.velocity = 1.5
        self.all_laser = pygame.sprite.Group()
        self.image = pygame.image.load("assets/vaisseaux/ennemies/enemy-01/nomove_1.png")
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.x = randint(-15,360)
        self.rect.y = -10
        self.delay = 90
        self.counter = 0

    def damage(self, amount) :
        self.health -= amount
        if self.health <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            self.game.explosion_group.add(explosion)
            self.game.all_monsters.remove(self)
            self.game.player.score += 5

    def forward(self):
        self.rect.y += self.velocity
        if self.game.check_collision(self,self.game.all_players) :
            self.game.player.damage(self.attack)
            self.game.all_monsters.remove(self)

    def launch_laser(self) :
        self.all_laser.add(Laser_ennemie(self))