import time
import pygame
from game import Game
pygame.init()

# Générer une fenêtre de jeu #
pygame.display.set_caption("SpaceShoot")
screen = pygame.display.set_mode((400, 600))
#background#
background = pygame.image.load('assets/fond/backgroundSpace.png')

#Chargement de notre jeu#
game = Game()

# Boucle jeu #
running = True
while running :
    #appliquer arrière plan #
    screen.blit(background,(0,0))
    #Appliquer image de notre joueur#
    screen.blit(game.player.image, game.player.rect)
    #vérifier si le joueur souhaite bouger#
    if game.pressed.get(pygame.K_DOWN) and game.player.rect.y + game.player.rect.width < screen.get_height():
        game.player.move_down()
    elif game.pressed.get(pygame.K_UP) and game.player.rect.y > 0:
        game.player.move_up()
    elif game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + (game.player.rect.width)/2 < screen.get_width() :
        game.player.move_right()
    elif game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0-(game.player.rect.width)/2 :
        game.player.move_left()
    #mettre à jour l'écran #
    pygame.display.flip()
    #fermeture du jeu#
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
            pygame.quit()
            print("fermeture du jeu")
        elif event.type == pygame.KEYDOWN :
            game.pressed[event.key]=True
        elif event.type == pygame.KEYUP :
            game.pressed[event.key] = False
