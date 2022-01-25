import time
import pygame
pygame.init()

#Classe joueur #
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.max_health = 3
        self.attack = 10
        self.velocity = 5
        self.image = pygame.image.load('assets/vaisseaux/playerOne.png')
        self.image.get_rect()


# Générer une fenêtre de jeu #
pygame.display.set_caption("SpaceShoot")
screen = pygame.display.set_mode((400, 600))
#background#
background = pygame.image.load('assets/fond/backgroundSpace.png')

#Chargement de notre joueur #
player = Player()

# Boucle jeu #
running = True
while running :
    #appliquer arrière plan #
    screen.blit(background,(0,0))
    #Appliquer image de notre joueur#
    screen.blit(player.image, (127,500))
    #mettre à jour l'écran #
    pygame.display.flip()

    #fermeture du jeu#
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
            pygame.quit()
            print("fermeture du jeu")

