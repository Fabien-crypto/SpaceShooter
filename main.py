import time
import sys
from pip import main 
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
volume = 0.5
mixer.music.set_volume(volume)

#Temps du jeu #
clock = pygame.time.Clock()
# Générer une fenêtre de jeu #
pygame.display.set_caption("SpaceShoot")
screen = pygame.display.set_mode((400, 600))
#background# 
background = pygame.image.load('assets/fond/frameBackground.png')
background = pygame.transform.scale(background,(400,600))
y_background = 0



def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/menu/font.ttf", size)

def pause():
    paused = True

    while paused:
        from menu import SCREEN,Button,image1,BG,best_score,prec_score, options,main_menu

        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(23).render("Pause", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 80))
        REPRENDRE = Button(image=image1, pos=(200, 200), 
                            text_input="REPRENDRE", font=get_font(12), base_color="White", hovering_color="Green")
        OPTIONS = Button(image=image1, pos=(200, 280), 
                            text_input="OPTIONS", font=get_font(12), base_color="White", hovering_color="Green")
        MENU = Button(image=image1, pos=(200, 360), 
                            text_input="MENU", font=get_font(12), base_color="White", hovering_color="Green")

        Best_Score_TEXT = get_font(12).render("Meilleur Score: 1290", True, "white")
        Best_Score_RECT = Best_Score_TEXT.get_rect(center=(215, 450))
        Prec_Score_TEXT = get_font(12).render("Score Précédent: 798", True, "white")
        Prec_Score_RECT = Prec_Score_TEXT.get_rect(center=(215, 500))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(Best_Score_TEXT, Best_Score_RECT)
        SCREEN.blit(Prec_Score_TEXT, Prec_Score_RECT)
        SCREEN.blit(best_score,(55,438))
        SCREEN.blit(prec_score,(55,488))

        for button in [REPRENDRE, OPTIONS, MENU]:
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REPRENDRE.checkForInput(MENU_MOUSE_POS):
                    paused = False
                if OPTIONS.checkForInput(MENU_MOUSE_POS):
                    options()
                if MENU.checkForInput(MENU_MOUSE_POS):
                    main_menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        clock.tick(5)
        pygame.display.update()



def game():
    #Chargement de notre jeu#
    game = Game()
    background = pygame.image.load('assets/fond/frameBackground.png')
    background = pygame.transform.scale(background,(400,600))
    y_background = 0

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
        #Appliquer l'ensemble de mon grp de projectiles en les dessinant#
        game.player.all_projectiles.draw(screen)
        game.all_monsters.draw(screen)

        #récupérer tout les projectiles du joueur #
        for projectile in game.player.all_projectiles :
            projectile.move()

        for monster in game.all_monsters :
            monster.forward()
        
        game.player.update_health_bar(screen)
        game.spawn_monster()
        
        # vérifier si le joueur souhaite bouger ou tirer#
        if game.pressed.get(pygame.K_ESCAPE):
            pause()
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
            elif event.type == pygame.KEYUP :
                game.pressed[event.key] = False


import menu