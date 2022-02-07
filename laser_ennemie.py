import pygame
#classe projectile de notre vaisseau #
class Laser_ennemie(pygame.sprite.Sprite) :
    # Définir le constructeur de cette classe #
    def __init__(self, monster):
        super().__init__()
        self.velocity = 3.5
        self.monster = monster
        self.image = pygame.image.load('assets/missiles/ennemie.png')
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = monster.rect.x + (monster.rect.width)/2 - self.image.get_width()/2
        self.rect.y = monster.rect.y
    def remove(self):
        self.monster.all_laser.remove(self)
    def move(self):
        self.rect.y += self.velocity
        from main import screen
        if self.rect.y >  screen.get_height():
            self.remove()

