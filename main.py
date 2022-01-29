import time
import pygame
from game import Game
pygame.init()

#Temps du jeu #
clock = pygame.time.Clock()
# Générer une fenêtre de jeu #
pygame.display.set_caption("SpaceShoot")
screen = pygame.display.set_mode((400, 600))
#background#
background = pygame.image.load('pythonProject/assets/fond/frameBackground.png')
background = pygame.transform.scale(background,(400,600))
y_background = 0

#Chargement de notre jeu#
game = Game()
# Boucle jeu #
running = True
pygame.key.set_repeat
while running :
    #appliquer arrière plan et défilement#
    y_background += 1
    if y_background < 600 :
        screen.blit(background,(0,y_background))
        screen.blit(background, (0, y_background-600))
    else :
        y_background = 0
        screen.blit(background, (0, y_background))
    #Appliquer image de notre joueur#
    screen.blit(game.player.image, game.player.rect)
    clock.tick(130)
    #récupérer tout les projectiles du joueur #
    for projectile in game.player.all_projectiles :
        projectile.move()
    #Appliquer l'ensemble de mon grp de projectiles en les dessinant#
    game.player.all_projectiles.draw(screen)

    # vérifier si le joueur souhaite bouger ou tirer#
    if game.pressed.get(pygame.K_SPACE):
        game.player.launch_projectile()
    if game.pressed.get(pygame.K_DOWN) and game.player.rect.y + (game.player.rect.height) < screen.get_height():
        game.player.move_down()
        if game.pressed.get(pygame.K_SPACE):
            game.player.launch_projectile()
    if game.pressed.get(pygame.K_UP) and game.player.rect.y > 0:
        game.player.move_up()
        if game.pressed.get(pygame.K_SPACE):
            game.player.launch_projectile()
    if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + (game.player.rect.width) / 2 < screen.get_width():
        game.player.move_right()
        if game.pressed.get(pygame.K_SPACE):
            game.player.launch_projectile()
    if game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0 - (game.player.rect.width) / 2:
        game.player.move_left()
        if game.pressed.get(pygame.K_SPACE):
            game.player.launch_projectile()


    #mettre à jour l'écran  #
    pygame.display.flip()
    #fermeture du jeu#
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
            pygame.quit()
            print("fermeture du jeu")
        if event.type == pygame.KEYDOWN :
            game.pressed[event.key]=True
        elif event.type == pygame.KEYUP :
            game.pressed[event.key] = False
