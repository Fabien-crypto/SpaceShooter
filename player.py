import pygame
from projectile import Projectile
#Classe joueur #
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 4
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/vaisseaux/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = 129
        self.rect.y = 500
        self.shoot_delay = 150
        self.last_shoot =  pygame.time.get_ticks()

    def update_health_bar(self,surface):
        bar_color = (35, 188, 27)
        bar_position = [self.rect.x -10, self.rect.y + self.rect.height, self.health, 5]
        back_bar_color = (212, 63, 23)
        back_bar_position = [self.rect.x -10, self.rect.y + self.rect.height, self.health, 5]
        pygame.draw.rect(surface, back_bar_color, back_bar_position) #dessin barre de vie rouge #
        pygame.draw.rect(surface, bar_color, bar_position)

        
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