from turtle import position
import pygame
import sys
from button import Button
from pygame import mixer
from game import Game

pygame.init()

#Icone jeu#
a = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
image1 = pygame.image.load("assets/menu/Play Rect.png")
image1 = pygame.transform.scale(image1,(150,50))
pygame.display.set_icon(a)

#Musique de fond
mixer.init()
mixer.music.load('sounds/01_Title Screen.mp3')
volume = 0.5
mixer.music.set_volume(volume)
mixer.music.play()

game = Game()
#définition de notre menu #
SCREEN = pygame.display.set_mode((400, 600))
pygame.display.set_caption("SpaceShoot")

BG = pygame.image.load("assets/menu/Background.png")

# Définition des icons dans le menu#
best_score = pygame.image.load('assets/icon/best_score.png')
best_score = pygame.transform.scale(best_score,(20,20))
prec_score = pygame.image.load('assets/icon/prec_score.png')
prec_score = pygame.transform.scale(prec_score,(20,20))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/menu/font.ttf", size)



# Je comprends pas à quoi sert cette fonction (marche sans juste en important jeu)

# def play():                                                               
#     while True:
#         from main import jeu
#         jeu()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if pygame.PLAY_BACK.checkForInput(pygame.PLAY_MOUSE_POS):
#                     main_menu()
#         pygame.display.update()


def options(menu):
    global volume
    global position,position2
    position=300
    position2=300
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        OPTIONS_TEXT = get_font(12).render("Choisir tes paramètres.", True, "white")
        OPTIONS_TEXT1 = get_font(12).render("Musique de fond", True, "white")
        OPTIONS_TEXT2 = get_font(12).render("Effets spéciaux Fx", True, "white")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(200, 50))
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(200, 150))
        OPTIONS_RECT2 = OPTIONS_TEXT1.get_rect(center=(200,300))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        SCREEN.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        SCREEN.blit(OPTIONS_TEXT2, OPTIONS_RECT2)

        OPTIONS_BACK = Button(image=None, pos=(200, 460), 
                            text_input="BACK", font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_PLUS = Button(image=None, pos=(380, 185),
                            text_input="+",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_MOINS = Button(image=None, pos=(380, 235),
                            text_input="-",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_PLUS2 = Button(image=None, pos=(380, 330),
                        text_input="+",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_MOINS2 = Button(image=None, pos=(380, 380),
                        text_input="-",font=get_font(12), base_color="white", hovering_color="Green")


        buttonlist = [OPTIONS_MOINS,OPTIONS_MOINS2,OPTIONS_PLUS,OPTIONS_PLUS2,OPTIONS_BACK]

        for button in buttonlist:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        pygame.draw.rect(SCREEN, (127, 127, 127), pygame.Rect(45, 200, position, 10)) 
        pygame.draw.rect(SCREEN, (127, 127, 127), pygame.Rect(45, 350, position2, 10)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    if menu == "menu":
                        main_menu()
                    else:
                        from main import jeu
                        jeu()
                if OPTIONS_PLUS.checkForInput(OPTIONS_MOUSE_POS):
                    if volume<0.5 and position <300: 
                        volume += 0.05
                        position += 30

                    mixer.music.set_volume(volume)
                if OPTIONS_MOINS.checkForInput(OPTIONS_MOUSE_POS):
                    if volume>0 and position >0: 
                        volume -= 0.05
                        position -= 30
                    mixer.music.set_volume(volume)

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(23).render("SpaceShooter", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 80))
        PLAY_BUTTON = Button(image=image1, pos=(200, 200), 
                            text_input="PLAY", font=get_font(12), base_color="White", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=image1, pos=(200, 280), 
                            text_input="OPTIONS", font=get_font(12), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=image1, pos=(200, 360), 
                            text_input="QUIT", font=get_font(12), base_color="White", hovering_color="Green")
        from main import saveread
        Best_Score_TEXT = get_font(12).render("Meilleur Score: "+ saveread("bestscore"), True, "white")
        Best_Score_RECT = Best_Score_TEXT.get_rect(center=(215, 450))
        Prec_Score_TEXT = get_font(12).render(("Score Précédent: "+ saveread("prec")), True, "white")
        Prec_Score_RECT = Prec_Score_TEXT.get_rect(center=(215, 500))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(Best_Score_TEXT, Best_Score_RECT)
        SCREEN.blit(Prec_Score_TEXT, Prec_Score_RECT)
        SCREEN.blit(best_score,(55,438))
        SCREEN.blit(prec_score,(55,488))


        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    from main import jeu
                    jeu()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options("menu")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
main_menu()