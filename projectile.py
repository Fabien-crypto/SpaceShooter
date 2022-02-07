import pygame
#classe projectile de notre vaisseau #
class Projectile(pygame.sprite.Sprite) :
    # Définir le constructeur de cette classe #
    def __init__(self, player):
        super().__init__()
        self.velocity = 3.5
        self.player = player
        self.image = pygame.image.load('assets/missiles/PlayProjectile.png')
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + (player.rect.width)/2 - self.image.get_width()/2
        self.rect.y = player.rect.y
    def remove(self):
        self.player.all_projectiles.remove(self)
    def move(self):
        self.rect.y -= self.velocity
        from main import screen
        if self.rect.y < -10:
            self.remove()

