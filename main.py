import time

import pygame
pygame.init()

# Générer une fenêtre de jeu #
pygame.display.set_caption("SpaceShoot")
screen = pygame.display.set_mode((400, 600))

#background#
background = pygame.image.load('assets/fond/backgroundSpace.png')

# Boucle jeu #
running = True
while running :
    #appliquer arrière plan #
    screen.blit(background,(0,0))
    #mettre à jour l'écran #
    pygame.display.flip()

    #fermeture du jeu#
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
            pygame.quit()
            print("fermeture du jeu")

