import time
import pygame
from pygame import mixer
from game import Game
pygame.init()

#Icone jeu#
a = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
pygame.display.set_icon(a)

#Musique de fond
mixer.init()
mixer.music.load('sounds/10 Drummed vaus.mp3')
mixer.music.play()

#Temps du jeu #
clock = pygame.time.Clock()
# Générer une fenêtre de jeu #
pygame.display.set_caption("SpaceShoot")
screen = pygame.display.set_mode((400, 600))
#background#
background = pygame.image.load('assets/fond/frameBackground.png')
background = pygame.transform.scale(background,(400,600))
y_background = 0

#Chargement de notre jeu#
game = Game()


# Boucle jeu #
running = True
pygame.key.set_repeat
while running :
    #appliquer arrière plan et défilement#
    y_background += 1/2
    if y_background < 600 :
        screen.blit(background,(0,y_background))
        screen.blit(background, (0, y_background-600))
    else :
        y_background = 0
        screen.blit(background, (0, y_background))
    #Appliquer image de notre joueur#
    screen.blit(game.player.image, game.player.rect)
    clock.tick(100)

    #récupérer tout les projectiles du joueur #
    for projectile in game.player.all_projectiles :
        projectile.move()

    for monster in game.monster.all_monsters :
        monster.forward()
        monster.update_health_bar(screen)
        touch = pygame.sprite.spritecollide(monster, game.player.all_projectiles,True)
        if touch:
            game.monster.damage(game.player.attack)
        game.player.all_projectiles.remove()

        contact = pygame.sprite.spritecollide(game.player, monster.all_monsters, True)
        if contact:
            game.player.damage(game.monster.attack)
    game.player.update_health_bar(screen)
    game.monster.spawn_monster()

    
    #Appliquer l'ensemble de mon grp de projectiles en les dessinant#
    game.player.all_projectiles.draw(screen)
    game.monster.all_monsters.draw(screen)

    # vérifier si le joueur souhaite bouger ou tirer#
    if game.pressed.get(pygame.K_SPACE):
        game.player.launch_projectile()
    if (game.pressed.get(pygame.K_DOWN) or game.pressed.get(pygame.K_s) ) and game.player.rect.y + (game.player.rect.height) < screen.get_height():
        game.player.move_down()
    if (game.pressed.get(pygame.K_UP) or game.pressed.get(pygame.K_z)) and game.player.rect.y > 0:
        game.player.move_up()
    if game.pressed.get(pygame.K_RIGHT) or game.pressed.get(pygame.K_d):
        game.player.move_right()
    if game.pressed.get(pygame.K_LEFT) or game.pressed.get(pygame.K_q):
        game.player.move_left()
    if (game.player.rect.x) > screen.get_width():
        game.player.rect.x = 0 - game.player.rect.width 
    if (game.player.rect.x) < -(game.player.rect.width) :
        game.player.rect.x = screen.get_width()

    #mettre à jour l'écran  #
    pygame.display.flip()
    #fermeture du jeu#
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN :
            game.pressed[event.key]=True
        elif event.type == pygame.KEYUP :
            game.pressed[event.key] = False
