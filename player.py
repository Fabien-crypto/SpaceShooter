import pygame

#Classe joueur #
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.max_health = 3
        self.attack = 10
        self.velocity = 2.7
        self.image = pygame.image.load('assets/vaisseaux/playerOne.png')
        self.rect = self.image.get_rect()
        self.rect.x = 135
        self.rect.y = 500
    def move_right(self):
        self.rect.x += self.velocity
    def move_left(self):
        self.rect.x -= self.velocity
    def move_up(self):
        self.rect.y -= self.velocity
    def move_down(self):
        self.rect.y += self.velocity