import pygame
from player import Player
#Classe jeu #
class Game:
    def __init__(self):
        #Génère notre joueur#
        self.player = Player()
        self.pressed = {}
