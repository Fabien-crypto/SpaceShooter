import pygame
from random import randint
from laser_ennemie import Laser_ennemie


#Classe du monstre#
class Monster(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 50
        self.max_health = 50
        self.attack = 50
        self.all_monsters = pygame.sprite.Group()
        self.all_laser = pygame.sprite.Group()
        self.image = pygame.image.load('assets/vaisseaux/ennemies/enemy-01/nomove.png')
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.x = randint(-15,360)
        self.rect.y = -10
        self.velocity = 1
        self.delay_spawn = 900
        self.last_monster = pygame.time.get_ticks()



    def spawn_monster(self):
        now = pygame.time.get_ticks()
        monster = Monster(self)
        if now - self.last_monster > self.delay_spawn :
            self.all_monsters.add(monster)
            self.last_monster = now

    def remove(self):
        #on enlève les ennemies de la map#
        self.all_monsters.remove(self)

    def damage(self, amount) :
        self.health -= amount
        print("hello2")

    def forward(self):
        self.rect.y += self.velocity
        from main import screen
        if self.rect.y > 0:
            self.remove()
        
    def launch_laser(self) :
        self.all_laser.add(Laser_ennemie(self))