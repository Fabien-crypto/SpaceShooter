import time 
import pygame
from pygame import mixer
from game import Game
from button import Button
import sys

def main():
    pygame.init()
    

    #Icone jeu#
    a = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
    image1 = pygame.image.load("assets/menu/Play Rect.png")
    image1 = pygame.transform.scale(image1,(150,50))
    pygame.display.set_icon(a)

    #Musique de fond#
    mixer.init()
    mixer.music.load('sounds/10 Drummed vaus.mp3')
    mixer.music.play()
    volumejeux = 0.5
    mixer.music.set_volume(volumejeux)

    #Temps du jeu #
    clock = pygame.time.Clock()
    # Générer une fenêtre de jeu #
    pygame.display.set_caption("SpaceShoot")
    screen = pygame.display.set_mode((400, 600))

    #background# 
    background = pygame.image.load('assets/fond/frameBackground.png')
    background = pygame.transform.scale(background,(400,600))
    y_background = 0

    #Définition de la police d'écriture #
    def get_font(size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/menu/font.ttf", size)

    def paused() :
        while pause:
            mixer.music.pause()
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            PLAY_BUTTON = Button(image=image1, pos=(200, 200), text_input="Reprendre", font=get_font(12), base_color="White", hovering_color="Green")
            PLAY_BUTTON.changeColor(OPTIONS_MOUSE_POS)
            PLAY_BUTTON.update(screen)
            pygame.display.update() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN :
                    if event.key==pygame.K_ESCAPE:
                        mixer.music.unpause()
                        return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        mixer.music.unpause() 
                        return 0


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
        clock.tick(60)
        
        #Appliquer l'ensemble de mon grp de projectiles en les dessinant#
        game.explosion_group.update()

        game.player.all_projectiles.draw(screen)
        game.all_monsters.draw(screen)
        game.explosion_group.draw(screen)


        #Affichage du score #
        Score_TEXT = get_font(14).render(("Score : "+ str(game.player.score)), True, "white" )
        Score_RECT = Score_TEXT.get_rect(center=(100, 20))
        screen.blit(Score_TEXT, Score_RECT)

        #récupérer tout les projectiles du joueur #
        for projectile in game.player.all_projectiles :
            projectile.move()

        for monster in game.all_monsters :
            monster.forward()
        
        game.player.update_health_bar(screen)
        game.spawn_monster()

        # vérifier si le joueur souhaite bouger ou tirer#
        if game.pressed.get(pygame.K_SPACE):
            game.player.launch_projectile()
        if (game.pressed.get(pygame.K_DOWN) or game.pressed.get(pygame.K_s)) and game.player.rect.y + (game.player.rect.height) < screen.get_height():
            game.player.move_down()
        if (game.pressed.get(pygame.K_UP) or game.pressed.get(pygame.K_z)) and game.player.rect.y > 0:
            game.player.move_up()
        if (game.pressed.get(pygame.K_RIGHT) or game.pressed.get(pygame.K_d)):
            game.player.move_right()
        if (game.pressed.get(pygame.K_LEFT) or game.pressed.get(pygame.K_q)):
            game.player.move_left()
        if not((game.pressed.get(pygame.K_DOWN) or game.pressed.get(pygame.K_s)) or  
            (game.pressed.get(pygame.K_UP) or game.pressed.get(pygame.K_z)) or 
            (game.pressed.get(pygame.K_RIGHT) or game.pressed.get(pygame.K_d)) or  
            (game.pressed.get(pygame.K_LEFT) or game.pressed.get(pygame.K_q)) ):
            game.player.no_move()
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
                if event.key==pygame.K_ESCAPE:
                    pause = True
                    paused()
            elif event.type == pygame.KEYUP :
                game.pressed[event.key] = False

main()