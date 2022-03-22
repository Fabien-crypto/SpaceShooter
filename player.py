import pygame
from projectile import Projectile
#Classe joueur #


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 15
        self.velocity = 7
        self.score = 0
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = 160
        self.rect.y = 500
        self.shoot_delay = 250
        self.last_shoot =  pygame.time.get_ticks()

    def damage(self, amount) :
        self.health -= amount

    def update_health_bar(self,surface):
        bar_color = (35, 188, 27)
        bar_position = [self.rect.x -10, self.rect.y + self.rect.height, self.health, 5]
        back_bar_color = (212, 63, 23)
        back_bar_position = [self.rect.x -10, self.rect.y + self.rect.height, self.max_health, 5]
        pygame.draw.rect(surface, back_bar_color, back_bar_position,0,3) #dessin barre de vie rouge #
        pygame.draw.rect(surface, bar_color, bar_position,0,3) #dessin barre de vie verte#

    def launch_projectile(self):
        #Création nouvelle instance du projectile et intervalle de temps#
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.all_projectiles.add(Projectile(self))
            self.last_shoot = now

    def move_right(self):
        self.rect.x += self.velocity
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/right.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
    def move_left(self):
        self.rect.x -= self.velocity
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/left.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_up(self):
        self.rect.y -= self.velocity
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_down(self):
        self.rect.y += self.velocity
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def no_move(self):
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))