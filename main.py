import pygame
from pygame import mixer
from game import Game
from button import Button
import sys

def saveread(score):
    with open("scores.txt","r") as fichier:
        list = fichier.readlines()
        fichier.close()
    if score == "bestscore":
        return list[0].replace("\n","")
    elif score == "volume":
        return list[2].replace("\n","")
    elif score == "position":
        return list[3]
    else:
        return list[1].replace("\n","")

# Initialisation du jeu
pygame.init()
pygame.font.init()

#Définition de la police d'écriture #
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/menu/font.ttf", size)

#Musique de fond
mixer.init()
mixer.music.load('sounds/01_Title Screen.mp3')
volume = float(saveread("volume"))
volumejeux = 0.5
mixer.music.set_volume(volume)
mixer.music.play()

#Icone jeu#
icon = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
pygame.display.set_icon(icon)

#Background des boutons#
buttonimg = pygame.image.load("assets/menu/button.png")
buttonimg = pygame.transform.scale(buttonimg,(150,50))
screen = pygame.display.set_mode((400, 600))

def save(score,vol,pos):
    bestscore = saveread("bestscore")
    fichier = open("scores.txt","w+")
    if score > int(bestscore):
        fichier.write(str(score)+"\n"+str(score)+"\n"+str(vol)+"\n"+str(pos))
        fichier.close()
    else:
        fichier.write(bestscore+"\n"+str(score)+"\n"+str(vol)+"\n"+str(pos))
        fichier.close()

volume = float(saveread("volume"))
position=int(saveread("position"))
position2=250
def options(menu):
    global volume
    global volumejeux
    global position,position2
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("black")
        OPTIONS_TEXT = get_font(12).render("Choisir tes paramètres.", True, "white")
        OPTIONS_TEXT1 = get_font(12).render("Musique de fond", True, "white")
        OPTIONS_TEXT2 = get_font(12).render("Effets spéciaux ", True, "white")
        POURCENTAGE_FOND = get_font(12).render((str(int(200*(volume)))+"%"), True, "white")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(200, 50))
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(200, 150))
        OPTIONS_RECT2 = OPTIONS_TEXT1.get_rect(center=(200,300))
        OPTIONS_POURCENTAGE_FOND_RECT = POURCENTAGE_FOND.get_rect(center=(40, 205))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        screen.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        screen.blit(OPTIONS_TEXT2, OPTIONS_RECT2)
        screen.blit(POURCENTAGE_FOND,OPTIONS_POURCENTAGE_FOND_RECT )
        OPTIONS_BACK = Button(image=None, pos=(200, 460), 
                            text_input="BACK", font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_MOINS = Button(image=None, pos=(350, 205),
                            text_input="-",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_PLUS = Button(image=None, pos=(380, 205),
                            text_input="+",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_MOINS2 = Button(image=None, pos=(350, 355),
                        text_input="-",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_PLUS2 = Button(image=None, pos=(380, 355),
                        text_input="+",font=get_font(12), base_color="white", hovering_color="Green")
        buttonlist = [OPTIONS_MOINS,OPTIONS_MOINS2,OPTIONS_PLUS,OPTIONS_PLUS2,OPTIONS_BACK]

        for button in buttonlist:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)
        pygame.draw.rect(screen, (75,75,75), pygame.Rect(72, 197, 256, 16),3,5)
        pygame.draw.rect(screen, (140, 140, 140), pygame.Rect(75, 200, position, 10),0,2)
        pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(72, 347, 256, 16),3,5)
        pygame.draw.rect(screen, (140, 140, 140), pygame.Rect(75, 350, position2, 10),0,2) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    if menu == "menu":
                        main_menu()
                    else:
                        screen.blit(background, (0, 0))
                        return 0
                if OPTIONS_PLUS.checkForInput(OPTIONS_MOUSE_POS):
                    if volume<0.5 and position <250: 
                        volume += 0.05
                        volumejeux += 0.05
                        position += 25
                        volume = round(volume,2)
                        save(int(saveread("score")),volume,position)
                    mixer.music.set_volume(float(saveread("volume")))
                if OPTIONS_MOINS.checkForInput(OPTIONS_MOUSE_POS):
                    if volume>0 and position >0: 
                        volume -= 0.05
                        volumejeux -= 0.05
                        position -= 25
                        volume = round(volume,2)
                        save(int(saveread("score")),volume,position)
                    mixer.music.set_volume(float(saveread("volume")))
        pygame.display.update()

def paused() :
    while True:
        mixer.music.pause()
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BUTTON = Button(image=buttonimg, pos=(200, 200), text_input="Reprendre", font=get_font(12), base_color="White", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=buttonimg, pos=(200, 280), text_input="Options", font=get_font(12), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=buttonimg, pos=(200, 360), text_input="Menu", font=get_font(12), base_color="White", hovering_color="Green")
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)
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
                if OPTIONS_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    options("jeu")
                if QUIT_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    save(score,saveread("volume"),saveread("position"))
                    mixer.music.unpause()
                    main_menu()

def main_menu():
    while True:
        BG = pygame.image.load("assets/menu/Background.png")
        best_score = pygame.image.load('assets/icon/best_score.png')
        best_score = pygame.transform.scale(best_score,(20,20))
        prec_score = pygame.image.load('assets/icon/prec_score.png')
        prec_score = pygame.transform.scale(prec_score,(20,20))
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(23).render("SpaceShooter", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 80))
        PLAY_BUTTON = Button(image=buttonimg, pos=(200, 200), 
                            text_input="PLAY", font=get_font(12), base_color="White", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=buttonimg, pos=(200, 280), 
                            text_input="OPTIONS", font=get_font(12), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=buttonimg, pos=(200, 360), 
                            text_input="QUIT", font=get_font(12), base_color="White", hovering_color="Green")
        Best_Score_TEXT = get_font(12).render("Meilleur Score: "+ saveread("bestscore"), True, "white")
        Best_Score_RECT = Best_Score_TEXT.get_rect(center=(215, 450))
        Prec_Score_TEXT = get_font(12).render(("Score Précédent: "+ saveread("prec")), True, "white")
        Prec_Score_RECT = Prec_Score_TEXT.get_rect(center=(215, 500))
        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(Best_Score_TEXT, Best_Score_RECT)
        screen.blit(Prec_Score_TEXT, Prec_Score_RECT)
        screen.blit(best_score,(55,438))
        screen.blit(prec_score,(55,488))

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    jeu()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options("menu")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def over_menu():
    while True:
        BG = pygame.image.load("assets/menu/Background.png")
        best_score = pygame.image.load('assets/icon/best_score.png')
        best_score = pygame.transform.scale(best_score,(20,20))
        prec_score = pygame.image.load('assets/icon/prec_score.png')
        prec_score = pygame.transform.scale(prec_score,(20,20))
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(23).render("SpaceShooter", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 80))
        BACK_MENU_BUTTON = Button(image=buttonimg, pos=(200, 200), 
                            text_input="Menu", font=get_font(12), base_color="White", hovering_color="Green")
        Best_Score_TEXT = get_font(12).render("Meilleur Score: "+ saveread("bestscore"), True, "white")
        Best_Score_RECT = Best_Score_TEXT.get_rect(center=(215, 450))
        Prec_Score_TEXT = get_font(12).render(("Score Précédent: "+ saveread("prec")), True, "white")
        Prec_Score_RECT = Prec_Score_TEXT.get_rect(center=(215, 500))
        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(Best_Score_TEXT, Best_Score_RECT)
        screen.blit(Prec_Score_TEXT, Prec_Score_RECT)
        screen.blit(best_score,(55,438))
        screen.blit(prec_score,(55,488))

        for button in [BACK_MENU_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
        pygame.display.update()


def jeu():
    global score
    global volumejeux
    #Musique de fond#    
    mixer.init()
    mixer.music.load('sounds/10 Drummed vaus.mp3')
    mixer.music.play()

    #Temps du jeu #
    clock = pygame.time.Clock()
    # Générer une fenêtre de jeu #
    pygame.display.set_caption("SpaceShoot")

    #background# 
    global background
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
        if game.player.health <= 0 :
            over_menu()
        #mettre à jour l'écran  #
        pygame.display.flip()

        #fermeture du jeu#
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                running = False
                score = game.player.score
                save(score,saveread("volume"),saveread("position"))
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                game.pressed[event.key]=True
                if event.key==pygame.K_ESCAPE:
                    score = game.player.score
                    paused()
            elif event.type == pygame.KEYUP :
                game.pressed[event.key] = False
main_menu()