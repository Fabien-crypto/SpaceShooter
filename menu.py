import pygame
import sys
from button import Button
from pygame import mixer
 

#Icone jeu#
a = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
image1 = pygame.image.load("assets/menu/Play Rect.png")
image1 = pygame.transform.scale(image1,(150,50))
pygame.display.set_icon(a)

#Musique de fond
mixer.init()
mixer.music.load('sounds/01_Title Screen.mp3')
mixer.music.set_volume(0.05)
mixer.music.play()

pygame.init()

SCREEN = pygame.display.set_mode((400, 600))
pygame.display.set_caption("SpaceShoot")

BG = pygame.image.load("assets/menu/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/menu/font.ttf", size)

def play():
    while True:
        import main 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        OPTIONS_TEXT = get_font(12).render("Choisir tes paramètres.", True, "white")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(200, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_BACK = Button(image=None, pos=(200, 460), 
                            text_input="BACK", font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

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

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()