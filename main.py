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
    #récupérer tout les projectiles du joueur #
    for projectile in game.player.all_projectiles :
        projectile.move()
    #Appliquer l'ensemble de mon grp de projectiles#
    game.player.all_projectiles.draw(screen) 

    #vérifier si le joueur souhaite bouger#
    if game.pressed.get(pygame.K_DOWN) and game.player.rect.y + (game.player.rect.height) < screen.get_height():
        game.player.move_down()
        if game.pressed.get(pygame.K_SPACE)  :
            game.player.launch_projectile()
    elif game.pressed.get(pygame.K_UP) and game.player.rect.y > 0:
        game.player.move_up()
        if game.pressed.get(pygame.K_SPACE)  :
            game.player.launch_projectile()
    elif game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + (game.player.rect.width)/2 < screen.get_width() :
        game.player.move_right()
        if game.pressed.get(pygame.K_SPACE) :
            game.player.launch_projectile()
    elif game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0-(game.player.rect.width)/2 :
        game.player.move_left()
        if game.pressed.get(pygame.K_SPACE) :
            game.player.launch_projectile()
    else:
        game.player.no_move()
        if game.pressed.get(pygame.K_SPACE) :
            game.player.launch_projectile()
    #mettre à jour l'écran  #
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
